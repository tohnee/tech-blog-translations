---
title: "SGLang 中的高级 CUDA 图技术"
title_en: "Advanced CUDA Graph Techniques in SGLang"
author: "SGLang Team"
date: "August 17, 2026"
source: https://lmsys.org/blog/2026-08-17-advanced-cuda-graph/
translated: 2026-09-12
previewImg: /images/blog/breakable_cuda_graph/bcg-design.svg
type: blog
---

# SGLang 中的高级 CUDA 图技术

> 原文：[Advanced CUDA Graph Techniques in SGLang](https://lmsys.org/blog/2026-08-17-advanced-cuda-graph/) · LMSYS Blog · SGLang Team

## TL;DR

CUDA 图（CUDA Graph）有望消除内核启动开销，但要在真实的推理引擎中接近这一收益，就需要在不牺牲兼容性、启动时间和内存的前提下，把尽可能多的工作负载纳入图中。

在 SGLang 中，我们围绕统一的 runner/backend 接口重构了 CUDA 图支持，使不同的捕获策略能够跨执行路径复用。**可断式 CUDA 图（Breakable CUDA Graph，BCG）是一项源自 SGLang 的推理服务技术：它最早在 SGLang 中被提出、命名、实现并开源**，首个实现于 2026 年 2 月 21 日发布于 [[#19102](https://github.com/sgl-project/sglang/pull/19102)]，面向预填充（prefill）的扩展于 2026 年 4 月 24 日合入 [[#22218](https://github.com/sgl-project/sglang/pull/22218)]。SGLang 还率先在 FA4 与 FlashInfer 注意力后端上实现了面向 prefill 的完整 CUDA 图支持。我们还深入探讨了 CUDA 图的内存管理，包括跨形状与跨图段的内存复用——这正日益成为 SGLang 整体内存管理中越来越重要的一部分。

在 prefill 场景下，可断式 CUDA 图如今已是 SGLang 的默认方案。它以约四分之一的代码量（521 行 vs 1,771 行）实现了与基于 `torch.compile` 的分段后端相同的分段执行；由于完全不涉及编译，构建 prefill 图的速度快 3.8–5.2×，并且天然地对复杂功能具备更广的覆盖面。面向 prefill 的完整 CUDA 图则更进一步：借助请求填充，即便是动态的 prefill 负载也能捕获完整的前向计算。仅就 prefill 单独测量，BCG 比 eager 执行快 1.70×，完整捕获可达 1.93×。

## 背景

一次推理步骤并不是单个内核（kernel），而是一长串 GPU 操作。在现代 LLM 推理服务引擎中，从 CPU 反复启动这些操作会引入可观的 CPU 开销，对延迟敏感的负载尤其如此。CUDA 图通过把 GPU 工作记录一次、再以低得多的启动开销进行重放（replay），来降低这部分开销。

但在现代推理引擎中有效地应用 CUDA 图并非易事。图的设计必须适配不同的执行阶段，与复杂的内核以及依赖运行时状态的行为保持兼容，并控制图自身引入的捕获期开销与内存开销。随着推理栈日益复杂，妥善集成 CUDA 图变得越来越重要。

本文将梳理 SGLang 是如何构建 CUDA 图支持的，以及我们做了哪些改动：

<ul style="line-height: 1.75;">
  <li style="padding-top: 0.55em;"><a href="#cuda-graph-in-sglang-the-runnerbackend-split-and-flexible-combinations">SGLang 中的 CUDA 图：Runner/Backend 拆分与灵活组合</a></li>
  <li style="padding-top: 0.55em;"><a href="#breakable-cuda-graph-eager-breaks-without-a-compiler">可断式 CUDA 图：无需编译器的 eager 断开</a></li>
  <li style="padding-top: 0.55em;"><a href="#full-cuda-graph-for-prefill">面向 Prefill 的完整 CUDA 图</a></li>
  <li style="padding-top: 0.55em;"><a href="#memory-footprint-of-cuda-graphs">CUDA 图的内存占用</a></li>
  <li style="padding-top: 0.55em;"><a href="#bcg-as-a-standalone-library">作为独立库的 BCG</a></li>
</ul>

## SGLang 中的 CUDA 图：Runner/Backend 拆分与灵活组合

在这次重构之前，CUDA 图支持是围绕各条执行路径分别演化出来的。解码、prefill 和投机解码各自拥有独立的 CUDA 图 runner，在捕获形状、静态缓冲区、重放和图配置等方面存在大量重叠逻辑。随着执行模式和捕获策略不断增加，这种重复既加大了基础设施复用的难度，也让与 CUDA 图相关的服务端参数变得越来越含糊。

重构 [[#23906](https://github.com/sgl-project/sglang/pull/23906)] 将这些职责拆分为两层。**runner** 负责管理捕获与重放所需的执行相关状态：捕获的形状、静态输入缓冲区、注意力元数据，以及把真实 batch 填充进捕获形状的操作。**backend（后端）** 则决定这一执行如何被捕获：是作为一张完整的图、一串可断开的段，还是由编译器生成的片段。

由于 runner 只依赖统一的 backend 接口，各执行路径可以独立选择自己的捕获策略。Prefill 和解码各有一个 runner；投机解码在此基础上引入更多：EAGLE draft、draft-extend 与 frozen-KV MTP draft 等步骤各自拥有一个建立在解码 runner 之上的 runner，而 target verify 就是解码 runner 本身，只是每个请求捕获的 token 不止一个。

<img src="/images/blog/breakable_cuda_graph/bcg-design.svg" style="width: 80vw; max-width: 860px; min-width: 300px;" />

<p style="text-align: center; color: #666; font-style: italic;">runner 为每条执行路径做好捕获与重放的准备，backend 则决定前向计算如何变成可重放的图：整图捕获、捕获时切段，或先追踪再拆分。</p>

### 完整 CUDA 图

完整后端为每个选定的形状捕获一张 `torch.cuda.CUDAGraph`，不含任何 eager 区域，在三种后端中重放时的启动次数也最少。这对解码来说顺理成章：每个请求贡献一个 token，因此主要的形状变量是 batch size，可以用一组捕获好的 batch size 桶来覆盖。Prefill 沿更多个维度变化，因而更难处理；我们将在[专门章节](#full-cuda-graph-for-prefill)中讨论它。

### 可断式 CUDA 图（BCG）

可断式 CUDA 图（BCG）捕获图安全的区域，同时允许被选定的操作在图段之间以 eager 方式运行。不兼容的操作可以用 `@eager_on_graph` 标记；捕获会在被标记的函数之前停下，并在其后恢复，从而生成一串由 eager 区域分隔的 CUDA 图段。

与基于编译器的分段捕获不同，这些断开点是在捕获过程中直接插入的，而不是先追踪完整模型再被发现。我们将在下一节讨论其机制，以及 SGLang 转向这一设计的原因。

### TC 分段 CUDA 图

第三种后端通过编译器实现类似的分段。`torch.compile` 以 `fullgraph=True` 追踪前向计算，得到的 FX 图在注册的切分点处被拆分，每个片段分别编译并捕获。它是 SGLang 对部分 CUDA 图捕获的最初方案；在可断式捕获尚未完成验证的平台上，它至今仍随 SGLang 一同提供。

## 可断式 CUDA 图：无需编译器的 eager 断开

传统上，CUDA 图要求被捕获区域完全兼容图捕获。而在实践中，现代推理负载包含无法被直接捕获的操作。Prefill 注意力就是一个常见的例子：一些注意力后端依赖运行时元数据与主机侧的准备。因此，仅仅一个不兼容的操作，就可能让 CUDA 图无法覆盖前向计算中大得多的部分。

为了让捕获更加灵活，SGLang 提出并率先开源了**可断式 CUDA 图（Breakable CUDA Graph，BCG）**。BCG 不用编译器去追踪整个前向计算，而是在捕获进行之中插入显式的 eager 断开点：被选中的操作以 eager 方式运行，而它们周围图兼容的区域则恢复捕获。从宏观上看，前向计算变成了一串由显式 eager 断开点连接起来的 CUDA 图段。

### 起源与开源脉络

BCG 起源于 SGLang。其发展过程有公开、按时间排列的源码历史为证：

<ul style="line-height: 1.75;">
  <li style="padding-top: 0.55em;"><strong>2026 年 2 月 21 日：SGLang 发布了第一个 BCG 实现。</strong> <a href="https://github.com/sgl-project/sglang/pull/19102">#19102</a> 的<a href="https://github.com/sgl-project/sglang/commit/571035632b263240e8daba7467dc3472e7884877">初始提交</a>就已包含 <code>BreakableCUDAGraph</code>、一个 eager 断开装饰器，以及用于结束并恢复 CUDA 图捕获的运行时机制。该 PR 于 4 月 11 日合入。</li>
  <li style="padding-top: 0.55em;"><strong>2026 年 4 月：SGLang 将 BCG 扩展到 prefill。</strong> <a href="https://github.com/sgl-project/sglang/pull/22218">#22218</a> 明确以 #19102 为基础，将 BCG 构建为面向 prefill 的免编译器可断式分段后端，并于 4 月 24 日合入。此后，BCG 成为 SGLang 默认的 prefill CUDA 图策略。</li>
</ul>

这里的原创性主张特指这一面向开源 LLM 推理服务的运行时可断捕获/重放机制：在其他项目采用之前，SGLang 已经提出、命名、实现并开源了该机制。这并不是主张图切分或 eager 回退这些更宽泛的概念没有先例。

### 设计与机制

当重放沿着固定的 GPU 操作序列进行、无需主机参与时，CUDA 图的效果最好。然而，真实的推理前向计算包含一些天然不适合这种模式的操作：注意力后端可能要根据实际序列长度做规划，集合通信可能涉及运行时协调，服务功能也可能动态更新状态。

一旦出现某个这样的操作就放弃 CUDA 图，会让前向计算的大部分无法被捕获。BCG 则让开发者直接用 `@eager_on_graph` 标记不兼容的区域。捕获期间，当执行到达被标记的函数时，当前图段即告关闭，该函数以 eager 方式运行，随后捕获在新的一段中恢复。

重放时，记录下来的图段与 eager 函数按同样的顺序运行。捕获阶段，被标记的函数会在图段之间运行一次，它返回的张量被保留为持久化的边界缓冲区，其设备地址因此保持固定；紧随其后的图段正是针对该地址捕获的。每次重放时，eager 函数照常运行并返回一个新的张量，BCG 把它拷贝进保留的缓冲区，于是下一段就能从当初捕获时使用的地址读到更新后的值。BCG 从不检查或追踪 eager 区域内的操作：它们只需要正确执行。

从功能角度看，BCG 与早先基于 torch.compile 的分段后端产生的是同一种可重放结构：由 eager 区域分隔的 CUDA 图段。关键区别在于这一结构如何构建。TC 分段后端先让编译器理解完整的前向计算，再对得到的图进行拆分；而 BCG 则在捕获进行的同时直接放置切分点。

### 收益

**启动更快。** 对于基于编译器的分段图，准备阶段的主导成本是编译而非捕获：`torch.compile` 占据了准备 prefill 图总耗时的 78–86%，且随模型复杂度增长——在 235B 的 MoE 模型上达到 90 秒，在 GLM-5.2 上达到 158 秒。BCG 完全去掉了这一阶段，只需单次捕获即可进入分段执行。

<img src="/images/blog/breakable_cuda_graph/prefill-build.svg" style="width: 68vw; max-width: 780px; min-width: 300px;" />

<p style="text-align: center; color: #666; font-style: italic;">构建 prefill CUDA 图的耗时：42 个捕获形状，4×GB300 上 TP4。</p>

编译开销在日常开发中同样可见。在我们当时的 CI 环境中，编译常常在多次测试运行之间重复发生，使 CUDA 图测试明显变慢。更好的缓存可以缓解这一问题，但把编译器从捕获路径中移除，也同时把这一额外的复杂度来源从开发循环中清除了。

**兼容面更广。** SGLang 大量依赖自定义 CUDA、Triton 以及 JIT 编译的内核，它们并非原生 PyTorch 算子。为了让这些内核对 `torch.compile` 可见，我们往往需要通过 `torch.library` 对其进行包装，并为追踪提供 fake 实现。这在整个内核栈中引入了针对编译器的脚手架代码。

更重要的是，编译器还限制了**图边界可以放在哪里**。跨越已注册算子边界的输入和输出必须是编译器能够表示的。当自然边界涉及更特殊的运行时状态或返回类型时，我们有时不得不另寻切分点，或干脆扩大 eager 区域，只为暴露一个编译器能处理的接口。随着服务栈不断膨胀，编译器边界越来越多地影响到那些本与编译毫无关系的代码结构。

BCG 在 eager 断开点处消除了这一约束：图系统不需要理解被标记函数是如何实现的，也不需要追踪其内部，图边界因此可以跟随服务逻辑，而不是迁就编译器的追踪与类型要求。CUDA 图必须与 DP 注意力、MoE all-to-all 后端、LoRA、PD 分离、分层缓存、确定性推理等快速演进的功能共存，让 CUDA 图跑通的过程越来越像在做 torch.compile 集成项目：新内核往往意味着注册自定义算子并编写 fake 实现，新功能则可能迫使我们仅仅为了满足编译器而移动图边界。有了 BCG，不兼容的区域可以保持为普通的 eager 执行，大幅减少了这类编译器相关的工程开销。

**天然可调试。** 被捕获的 CUDA 图作为一个不透明的整体重放：普通的 Python 代码不会在其内部执行，print、断言和逐步检查因此变得困难。BCG 则天然保留了 eager 区域，每次重放时普通 Python 代码仍然可以在其中运行。

SGLang 通过 `--debug-cuda-graph` [[#19102](https://github.com/sgl-project/sglang/pull/19102)] 进一步延伸了这一思路：它实际上是把整个前向计算包裹进一个 eager 断开点。此时模型以 eager 方式执行，但仍会经过 CUDA 图 runner、静态缓冲区、重放路径和元数据准备。这提供了一个很有用的调试边界：如果问题依然存在，大概率出在模型或 runner 路径上；如果问题消失，捕获本身就成为头号嫌疑。

### BCG 在 Diffusion 中的应用

BCG 也被 SGLang 的扩散模型栈采用 [[#27436](https://github.com/sgl-project/sglang/pull/27436)]。扩散模型在去噪过程中反复执行同样的 DiT 前向计算，当这些前向包含大量小而受启动开销束缚的内核时，CUDA 图尤其有用。

<ul style="line-height: 1.75;">
  <li style="padding-top: 0.55em;"><strong>捕获真实服务的形状。</strong> 分辨率、视频帧数、prompt 条件长度、CFG 模式以及所选的 transformer 都会影响捕获签名。我们为实际服务的形状做预热，对未见过的签名则回退到 eager 执行。</li>
  <li style="padding-top: 0.55em;"><strong>围绕动态操作断开。</strong> 动态注意力、依赖运行时的元数据准备等操作保持 eager，而 BCG 捕获其周边稳定的计算，无需 <code>torch.compile</code> 去理解完整的 DiT 前向。</li>
  <li style="padding-top: 0.55em;"><strong>利用重复的去噪结构。</strong> 扩散模型在各去噪步中反复执行同样的 DiT 结构。BCG 只需捕获一次稳定区域，即可在整个去噪循环中重放，动态区域则保持 eager。</li>
</ul>

当执行处于启动瓶颈（launch-bound）时，这尤其有效。例如，预热之后，单张 B200 上 512×512 的 Qwen-Image 端到端延迟从 6.48 s 降到 2.45 s，Z-Image 从 1.231 s 降到 0.662 s。

<img src="/images/blog/breakable_cuda_graph/diffusion.svg" style="width: 80vw; max-width: 860px; min-width: 300px;" />

<p style="text-align: center; color: #666; font-style: italic;">预热后的端到端延迟。每对柱形使用相同的模型负载与随机种子。</p>

更宏观的启示是：BCG 消除的是启动开销，它不会减少模型 FLOPs，也不会降低计算受限内核的执行成本。只有当暴露出来的启动间隙在执行时间中占据可观比例时，它的优势才最大。

## 面向 Prefill 的完整 CUDA 图

对解码来说，完整 CUDA 图很直接，因为每个请求只贡献一个 token：主要变化的维度就是 batch size。Prefill 则更难，因为一个 batch 同时在两个维度上变化——token 总数，以及这些 token 所属的请求数——而被捕获的图要求两者都保持固定。再加上依赖运行时元数据的注意力后端，完整 CUDA 图一直难以应用于 prefill，这也是我们在 prefill 上采用可断式 CUDA 图的主要原因之一。

最近，我们找到了让 prefill 执行足够静态化、从而支持完整 CUDA 图的方法 [[#27988](https://github.com/sgl-project/sglang/pull/27988)]，包括重构请求槽位与注意力元数据的表示方式，使受支持的注意力后端不再必须留在图外。

### 让 prefill 静态化

SGLang 用 token 桶固定 token 维度：真实 batch 被填充到最近的已捕获 token 数，与解码把 batch size 填充到已捕获桶的做法类似。

请求维度则单独处理。每张捕获的图预留固定数量的请求槽位：真实请求占据前面的槽位，未使用的槽位被改写为零长度哨兵——序列长度与 extend 长度均为零，相关 offset 停放在真实 token 之后。如果一个 batch 中的请求数超过图的槽位数，就回退到 eager 执行。

<img src="/images/blog/breakable_cuda_graph/full-prefill.svg" style="width: 76vw; max-width: 860px; min-width: 300px;" />

<p style="text-align: center; color: #666; font-style: italic;">重放时，token 被填充到已捕获的桶，未使用的请求槽位则由零长度哨兵填充。</p>

哨兵元数据必须在每次重放时重写，因为被捕获的图仍会读取整张请求表。注意力元数据同样在图外针对填充后的 batch 重建，然后再重放。因此，目前的完整 prefill 捕获要求注意力后端支持这种元数据准备方式，包括 FlashAttention 和 FlashInfer。

### 填充的代价有多大？

这两种填充的代价截然不同。

填充的 token 是真实的工作量。它们会成为捕获 batch 中的真实行，作为同一批 GEMM 的一部分经过稠密投影。SGLang 单独携带真实的 token 数，使 MoE 路由、注意力以及线性注意力内核能跳过大部分填充区域，但稠密计算仍要为这些额外的行付出代价。

空请求槽位则便宜得多。在 FlashAttention 的变长调度器中，工作量由每条序列的实际长度推导而来，而不是给每个请求槽位分配固定的计算量。因此，零长度请求几乎不产生任何注意力计算，主要只是增加元数据和少量调度开销。

这种不对称性很重要：token 填充是昂贵的维度，而请求槽位填充相对便宜。

完整 prefill 捕获目前仍是实验性功能。它必须显式开启——引擎会警告 `full` 尚属实验特性，并建议生产负载使用 breakable 或 tc_piecewise——而且目前主要在 FlashAttention（fa4）和 FlashInfer 后端上工作，因为只有这两个后端按捕获路径需要的方式构建 extend 模式元数据。扩展后端支持、调优桶与槽位的选择，仍是我们接下来的工作。

### Prefill 基准测试

有了三种捕获 prefill 的方式和一条 eager 基线，剩下的问题就是各自在重放时的开销如何。在 gpt-oss-120b（TP4，4×GB300，四种路径均可运行的平台）上单独测量 prefill——固定输入长度、单 token 输出、每次一个请求、所有实验组均禁用解码图：完整捕获比 eager 快 1.93×，BCG 快 1.70×，TC 分段快 1.45×——也就是说，BCG 不仅构建时更快，重放时也比基于编译器的后端快 17%。差距来自每次前向中各自做了什么：BCG 直接重放其记录的图段，而 TC 分段每次都要回调编译后的可调用对象，在它自己的捕获片段运行之前，先付出 Torch Dynamo 的 guard 检查与分发开销。在 GLM-5.2 上只有 BCG 能完成捕获——TC 分段无法追踪其前向计算，完整捕获也没有适配其稀疏注意力的路径——在那里 BCG 比 eager 快 1.60×。所有曲线在 32× 的 prompt 长度范围内都保持平坦，这正是启动开销而非计算负载的典型特征。

<img src="/images/blog/breakable_cuda_graph/prefill-ttft.svg" style="width: 80vw; max-width: 860px; min-width: 300px;" />
<p style="text-align: center; color: #666; font-style: italic;">gpt-oss-120b 上的纯 prefill 延迟，四种后端均可运行。</p>

## CUDA 图的内存占用

内存带来两个相互独立的挑战：一是避免分段捕获成倍放大常驻内存，二是捕获得足够多，使常驻的图内存真正取代最坏情况下的 eager 激活峰值。

### 分段捕获内的复用

分段后端很容易让图内存成倍增长：每个捕获形状包含多个图段，而每个图段都有必须保持有效以供重放的中间结果。BCG 通过三种复用方式避免了这种成倍增长。

<ul style="line-height: 1.75;">
  <li style="padding-top: 0.55em;"><strong>所有图段共享同一个内存池。</strong> 同一捕获形状的每个图段都使用同一个 CUDA 图内存池，中间存储得以复用，而不必为每个图段单独固定一份。</li>
  <li style="padding-top: 0.55em;"><strong>eager 断开点处的弱引用。</strong> 当图内存池已拥有张量的底层存储时，传入断开点的张量以弱引用持有，避免不必要的 Python 引用延长张量生命周期。这种张量弱引用技术来自 vLLM [<a href="https://github.com/vllm-project/vllm/pull/9724">#9724</a>]，vLLM 引入它是为了让捕获的图能共享输出缓冲区，而不是各自固定一份。</li>
  <li style="padding-top: 0.55em;"><strong>所有捕获尺寸共享一个输出缓冲区。</strong> 各捕获尺寸共享一个按最大尺寸分配的输出缓冲区，按每个形状所需的行数切片使用，而不是为每个形状各分配一个输出缓冲区。</li>
</ul>

有一个值无法这样处理：跨 eager 断开点传递数据的那个张量。下一个图段是基于它的地址捕获的，因此该缓冲区必须一直存活，并在每次重放时就地更新。

借助这些复用机制，即便是很大的捕获表，占用也依然有限：在 78 层 MoE 的 GLM-5.2 上，42 个形状只增加 2.4 GB 图内存。

### 捕获覆盖到 chunked-prefill 尺寸

CUDA 图改变了 prefill 内存使用的形态。图内存是常驻的：在捕获时分配，并在服务器生命周期内一直保留。Eager 激活值则是瞬态的：每次 prefill 都分配工作内存，而受支持的最大 prefill 决定了峰值。

捕获一个 prefill 形状，等于把很大一部分瞬态工作集搬进图的常驻内存池。但这只对真正重放图的形状有帮助。如果捕获阶梯止步于最大 prefill 尺寸之下，最大的 prefill 仍会回退到 eager 执行、保留原有的激活峰值——与此同时，服务器还要为它之下所有常驻的图付费。

这使得捕获上限比捕获形状的数量更重要。由于 `chunked_prefill_size` 限定了单次 prefill 前向的最大规模，只要捕获覆盖到该尺寸，就能消除最坏情况下的 eager 激活峰值。

<img src="/images/blog/breakable_cuda_graph/cg-memory.svg" style="width: 76vw; max-width: 830px; min-width: 300px;" />

<p style="text-align: center; color: #666; font-style: italic;">高于无图常驻基线的 prefill 内存，在按恰好等于 chunked-prefill 尺寸执行一次 prefill 之后测得。</p>

低于分块尺寸的捕获上限会略*高于*无图基线：它们增加了常驻的图，而激活峰值原封不动。一旦捕获上限达到分块尺寸，最大的 prefill 终于能重放图，这一峰值随之崩落——在 gpt-oss-120b 上几乎归零（0.56 GB 降至 0.001 GB），在 GLM-5.2 上从 1.55 GB 降至 0.35 GB，后者的稀疏注意力索引器仍在某个断开点处以 eager 方式运行。

把捕获覆盖到 chunked-prefill 尺寸能换来两件事：

<ul style="line-height: 1.75;">
  <li style="padding-top: 0.55em;"><strong>总内存更低。</strong> 激活峰值不再按请求反复支付，总内存降到无图基线之下——gpt-oss-120b 低 0.51 GB，GLM-5.2 低 1.10 GB。相对于数百 GB 的内存占用而言不算多，但这是节省而不是开销。</li>
  <li style="padding-top: 0.55em;"><strong>内存用量可预测。</strong> 依赖负载的激活尖峰变成捕获时就确定的固定分配。引擎可以预先把这块内存计入账目，而不必为一个只在大 prefill 时才出现的瞬态峰值预留余量。</li>
</ul>

## 作为独立库的 BCG

可断捕获机制本身并不与 SGLang 绑定，因此我们与 Meta PyTorch 团队合作，把它抽取为一个独立的库：[meta-pytorch/breakable-cuda-graphs](https://github.com/meta-pytorch/breakable-cuda-graphs)。它以一个小巧的 PyTorch 风格 API 暴露同样的捕获模型：一个类似 `torch.cuda.graph` 的 `breakable_graph(...)` 上下文管理器，一个标记函数在图段之间以 eager 方式运行的 `@no_graph` 装饰器，以及一个按顺序重放捕获图段与 eager 区域的 `CUDAGraphSequence`。如果上下文内部没有发生 eager 断开，整个代码块会被捕获为单个图段——标准的 CUDA 图模式作为平凡情形自然成立。

如果你的系统需要部分 CUDA 图捕获——无论是在另一个推理引擎、训练循环还是研究原型中——都可以直接使用这个库，无需引入 SGLang 的 runner 栈，学术或工业工作均可。SGLang 会继续演进这一机制，我们期待独立库与仓库内实现随时间逐步趋同。

## 致谢

这项工作是 SGLang 团队与 Meta 团队合作的成果。

SGLang：Yuwei An*、Cheng Wan、Xiaoyu Zhang、Mick Qian、Baizhou Zhang、Yusheng Su、Ke Bao

Meta：Shiyang Chen*、Lianmin Zheng

同时感谢 NVIDIA、AMD、Thinking Machines Lab 和 Meta PyTorch 团队一路以来的帮助。

（\* 同等贡献）
