---
title: "SGLang 与 Miles 为 Kimi K3 提供 Day-0 支持"
title_en: "SGLang and Miles Add Day-0 Support for Kimi K3"
author: "SGLang Team"
date: "July 27, 2026"
previewImg: /images/blog/kimi-k3-day0-support/cover-kimi-k3.png
source: https://lmsys.org/blog/2026-07-27-kimi-k3-day0-support/
translated: 2026-09-12
type: blog
---

# SGLang 与 Miles 为 Kimi K3 提供 Day-0 支持

> 原文：[SGLang and Miles Add Day-0 Support for Kimi K3](https://lmsys.org/blog/2026-07-27-kimi-k3-day0-support/) · LMSYS Blog · SGLang Team

我们很高兴地宣布，SGLang 与 Miles 已为 **[Kimi K3](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart)** 提供 Day-0 支持。K3 是首个三万亿参数量级的开源模型，其混合架构几乎在推理服务栈存在预设假设的每一处都打破了常规。在与 Moonshot AI 和 NVIDIA 团队的合作下，两者在发布日当天便完整覆盖了 K3：SGLang 负责推理，Miles 负责强化学习（RL）训练。本文介绍这一切是如何做到的。

**核心亮点**

- **全新混合架构。** 2.8T 参数，69 层 KDA 线性注意力与 24 层 MLA、LatentMoE 和注意力残差（Attention Residuals）交错排布；服务栈的大部分预设假设都会在某个环节被打破。
- **面向两类状态（two kinds of state）的内存管理**，包括一种会在原位自我覆写的循环状态（recurrent state），并在其上重建了前缀缓存、重叠调度与分页机制，以及一套消除最后一项容量猜测的统一内存池设计。
- **一条算子优化阶梯**，在投机解码之前于 batch 1 达到约 113 tok/s。
- **DSpark 投机解码**，配备[我们为 K3 训练的草稿模型](https://huggingface.co/RadixArk/Kimi-K3-DSpark)：batch-1 解码达到约 423 tok/s。ReplaySSM 处理 KDA 状态，不逐步快照，而是重放原始输入，使草稿窗口内存降低约 32 倍。
- **按阶段拆分的并行策略**：预填充（prefill）采用分块流水线并行，解码采用上下文并行，并在 PD 分离部署下组合，达到 2,808 tok/s/GPU。
- **在原生 MXFP4 检查点上用 Miles 进行 LoRA 强化学习**，训练器与 rollout 共置于同一批 GPU：AIME-2024 成绩在 12 小时训练中从 43.3% 提升到 76.7%。

启动命令与针对不同负载的配置指南见 [Kimi K3 cookbook](https://docs.sglang.io/cookbook/autoregressive/Moonshotai/Kimi-K3)。


## Kimi K3 的基础适配（bring-up）

[Kimi K3](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart) 是首个三万亿参数量级的开源模型：2.8T 参数、1M token 上下文窗口、原生视觉理解。其前身 K2.5 在架构上是 SGLang 已经服务得很成熟的那类模型的近亲，因此栈的大部分内容直接适用。K3 却不是这样——它同时在多个独立之处偏离了惯例：

| | Kimi K2.5 | Kimi K3 |
|---|---|---|
| 规模 | 约 1T 参数 | 2.8T 参数 |
| 注意力 | 全 MLA，61 层 | 混合：69 层 KDA 线性注意力 + 24 层 MLA，共 93 层 |
| 注意力残差（Attention Residuals） | 无 | 每个注意力输出都存入 bank，按块聚合 |
| MoE | 384 个专家，top-8 | LatentMoE：896 个专家，top-16，在 3584 维潜在空间中运行 |
| 专家激活 | SwiGLU | SiTU |
| 视觉塔 | MoonViT | MoonViT3d，一套全新的 K3 专用技术栈 |

表中每一行都是一个推理服务难题。混合注意力栈正是让 1M 上下文变得可负担的关键，但它意味着服务器要同时持有两类状态：每个请求一份固定大小的 KDA 状态，旁边是 MLA 的逐 token KV——下文的内存管理章节讲的正是这件事。注意力残差把一个注意力输出 bank 贯穿整个模型栈，打破了 SGLang 标准层间管线的假设，迫使 DP 注意力等处增加 K3 专用路径。LatentMoE 在降投影后的潜在空间内从 896 个专家中路由 16 个，并使用 SiTU 激活而非 SwiGLU，因此没有任何现成 MoE 算子可以开箱即用。而视觉通路——视觉塔、投影器、处理器以及 Kimi 的 XTML 媒体格式——则是从零搭建的。下面各章节都建立在这项基础适配工作之上。

## 混合 KDA 的内存管理

K3 的 KDA 与 MLA 混合架构带来了两个内存管理挑战。其一是让前缀缓存对可变的 KDA 循环状态既安全又高效；其二是在 KDA 状态与 MLA KV 之间动态共享容量。

### 安全高效的状态复用

注意力 KV 是只追加（append-only）的。一旦算出，永不改变，因此调度器可以在基数树（radix tree）中安全地跨请求共享缓存前缀。KDA 状态则不同。每一层维护一个固定大小的循环缓冲区，**在每个 token 处都被原位覆写**，因此前缀缓存必须管理可变状态而非不可变 KV。

在 SGLang 中，我们在基数树与请求的工作槽之间使用三种显式的状态移动来安全地缓存和复用可变 KDA 状态。**写时复制（copy-on-write）**在前向计算修改共享检查点之前，将其恢复（restore）到一个私有槽中。**快照（snapshot）**捕获推进后的状态，**移交（donate）**则把该快照转移给基数树。

<p align="center">
  <img src="/images/blog/kimi-k3-day0-support/fig1-state-flow.svg" width="98%" alt="The three KDA state moves, copy-on-write, snapshot and donate, and where each sits relative to the serial forward stream.">
</p>

<p align="center">
  <em><b>三种状态移动。</b>写时复制、快照与移交，以及它们各自相对于串行前向流的位置。</em>
</p>

这一设计**在构造上就是无竞态（race-free）的**。恢复与快照的拷贝被排入前向流中，位于产生和消费该状态的操作之间，因此流序（stream ordering）天然防止了与原位更新的竞态。快照在乒乓式额外缓冲区的两个槽之间交替进行，因此下一个快照不会覆写正在挂到树上的状态。移交只传递一个槽索引，不复制任何状态。第二个槽在边界处惰性分配并随即释放，避免每个请求永久占用一个槽位。这既不需要设备级同步，也不需要在热路径上加锁。

检查点的摆放位置决定了缓存命中率。循环状态无法倒着运行，必须从更早的检查点向前重放。我们只在对齐的基数树节点处取检查点——预填充期间在 chunk 边界处，解码期间按固定 token 间隔——并在每条路径上限与 LRU 的约束下保留一个稀疏的检查点集合。受 [Marconi](https://arxiv.org/abs/2411.19379) 启发，我们优先选取**分支点（branching points）**，因为它们的前缀被所有子分支共享。当请求在中途偏离某条边时，它从上方最近的检查点开始重放，并在对齐的分叉处植入一个新检查点，让后续分支可以直接从那里恢复。

<p align="center">
  <img src="/images/blog/kimi-k3-day0-support/fig2-radix-branching.svg" width="98%" alt="Sparse KDA state checkpoints overlaid on the radix tree, and the branching point where a new request diverges from a cached prefix.">
</p>

<p align="center">
  <em><b>基数树上的检查点。</b>稀疏的检查点叠加层与分支点。</em>
</p>

无竞态的状态移动加上感知分支的检查点摆放，提供了高复用的 KDA 前缀缓存，并且能与重叠调度器、投机解码和分页 KV 干净地组合。

### 统一内存：一个池容纳两类状态

上面的一切都在各自的池内管理两类状态，而这些池本身是设计中剩下的最后一项猜测。两个分配单元相差三个数量级：每个请求一个大 KDA 状态块（TP=8 下约 54 MB，覆盖全部 69 个 KDA 层），每个 token 一个小 MLA KV 块（约 27 KB，覆盖全部 24 个 MLA 层），因此目前它们分属两个在启动时定容的独立池。这种定容是对流量的一次押注：一旦押错，服务器一侧池内存耗尽，另一侧却仍有富余。

统一内存用单个池取代两个池：KDA 状态从一端填入，MLA KV 块从另一端填入，两者之间未使用的字节构成一个连续空闲区。

<p align="center">
  <img src="/images/blog/kimi-k3-day0-support/fig-unified-memory.svg" width="98%" alt="Unified memory: two static pools versus one pool holding both kinds of state, and the freeing sequence">
</p>

<p align="center">
  <em><b>统一内存。</b>上：目前两类状态各有独立池，启动时定容，一侧闲置而另一侧占满。中：统一内存让两类状态从同一个池的两端相向增长，中间留下一个空闲区。下：释放一个状态块会在中部留下空隙，此时将端部的一个块移入其中，空闲区保持为一片。</em>
</p>

释放同样简单。当请求完成、被中止或在压力下被撤回时，其块被释放。如果这在中部留下空隙，就把端部的一个块移入其中，使空闲区始终连成一片。

这种布局带给我们灵活的页大小且没有内存碎片：54 MB 的 KDA 状态块与 27 KB 的 MLA KV 块从同一批字节中分配，无需强加一个公共页大小；上述移动操作让两端各自保持紧凑，状态移动的代价可忽略不计，因此空闲空间始终是二者皆可使用的单个连续区域。于是容量跟随负载走，而不是跟随一个启动参数：大量短请求会把池填满状态块，少数长上下文会把它填满 KV，两种情形都不需要重新配置。

统一内存以可选方式发布，通过 `--enable-unified-memory` 启用。后续文章将详细讲解其实现。

## 基于 DSpark 的投机解码

K3 附带 DSpark 块级投机解码，由[我们为 K3 训练的草稿模型](https://huggingface.co/RadixArk/Kimi-K3-DSpark)驱动。集成工作中有两部分值得单独成篇：一是把验证预算只花在值得的地方，二是让 K3 的循环 KDA 状态能在投机解码下存活。

### 只验证值得验证的部分

DSpark 每步提出一个草稿 token 块，目标模型用一次前向验证整块。在 batch size 为 1 时，额外的验证位置几乎是免费的：该步受延迟约束，多带几个 token 顺路即可。随着 batch 填满，这不再成立。验证 token 开始与所有其他请求争夺同一步的时间，而且它们中的大多数本来也会输掉赌注：在聊天负载上接受长度约为 2.7，典型一步中 8 个被验证位置有 5 个会被拒绝。全量验证等于为服务器随后丢弃的 token 支付全额代价。

修复它的组件其实早已存在于系统中。草稿模型带有一个经过训练的置信度头（confidence head），按位置预测每个 token 存活到验证的概率。另一侧，对服务器的一次性性能画像记录了每个负载水平下额外一个验证 token 的真实成本。一个逐步规划器把两者结合起来：只要某个 token 的期望收益能覆盖其边际成本，请求就保留该验证 token，其余窗口在目标前向启动前被裁剪。剩下的部分完全按原样验证，因此输出保持无损。这笔交易的代价是接受长度略短，换来更便宜的一步。

<p align="center">
  <img src="/images/blog/kimi-k3-day0-support/f4-verify-all-vs-trim.svg" width="98%" alt="Decode throughput vs batch size, verify-all vs confidence-scheduled trim, on a chat panel and a few-shot math panel.">
</p>

<p align="center">
  <em><b>裁剪在负载下胜出。</b>解码吞吐量，全量验证 vs 裁剪，聊天面板（接受长度约 2.7，左）与少样本数学面板（接受长度约 5.0，右）。在 bs 8 之前打平，之后差距随 batch size 拉开：bs 256 时分别提升 +68% 和 +24%，接受长度相应从 2.7 降至 2.2、从 5.0 降至 4.3，而吞吐量持续攀升。</em>
</p>

实测成本曲线才是最有意思的部分。验证 token 的边际成本并不平滑。它是一条阶梯：平坦的台阶处，多一个 token 几乎免费地搭上当前内核波（kernel waves）；陡峭的立升处，它启动了新的一波。规划器读取这张曲面。当请求的下几个 token 落在便宜的台阶上时保留它们；一旦会触发立升就在那里裁断。在数据上，这表现为接受长度曲线上的小幅波动，而吞吐量保持平滑单调：规划器是在沿真实的硬件台阶冲浪，而非噪声。

在 batch size 8 以下几乎没有需要释放的压力，因此裁剪在该区间是打平到略有负收益；规划器中的小 batch 提前退出是已知的后续工作。

### ReplaySSM：KDA 状态的原始输入重放

投机解码一次验证 γ+1 个草稿 token，且可能只接受其中一个前缀，因此状态必须可回退。KDA 层的状态每个 token 都会自我覆写，基线做法是在每个草稿步之后快照整个 K×V 状态——在 K=V=128 时每请求、每层、每头 64 KB，再乘以 γ+1 步。摊到 K3 的 69 个 KDA 层上，这块暂存空间要为每个运行中的请求保留，于是它挤压持久状态池并限制了并发上限。

[ReplaySSM](https://tridao.me/blog/2026/replayssm/) 改为保留每个草稿步的原始输入 `Sᵢ = (vᵢ, kᵢ, gkᵢ, βᵢ)`，约 1 KB，由验证内核在执行途中顺带写入。采样器确定接受长度后，一个覆盖所有层与头的折叠内核（fold kernel）从已提交检查点出发只重放被接受的前缀，并原位推进状态。这次折叠是验证递推的逐字克隆，消费验证内核存储的门控值而非重新计算，因此重建出的状态与循环基线将提交的状态逐位一致（bit-identical）。

- **内存**：草稿窗口从 512 KB 降到 16 KB，约 32 倍。把这部分内存还给状态池，使并发上限提升数倍。
- **速度**：验证内核不再每步写快照，减少了它的内存访问；重放是对所有层与头的一次融合启动，因此即使在较小 batch size 下每步时间也会改善。

<p align="center">
  <img src="/images/blog/kimi-k3-day0-support/fig-replayssm-kda.svg" width="98%" alt="KDA ReplaySSM: the verify kernel reads the committed checkpoint and stores each draft step's raw inputs in a small per-slot buffer; after acceptance a single fold kernel replays only the accepted prefix and advances the state in place.">
</p>

<p align="center">
  <em><b>KDA ReplaySSM。</b>验证读取检查点 h₀ 但不写它，并把每个草稿步的原始输入存入每层每头一个的槽缓冲区。随后折叠内核只重放被接受的前缀并原位覆写该槽。</em>
</p>

## 算子（Kernels）

在 2.8T 混合模型上做单序列解码一步并不是算力受限的问题——而是一个启动次数与延迟问题：每个 token 要经过 93 个注意力层（69 KDA + 24 MLA）加 92 个潜在 MoE 层，而在基础适配完成之初，一步会触发数百个微小内核。这场优化战役以性能画像驱动：融合一件事，在固定协议上做 A/B 对比，以 GSM8K 把关，然后重复。

![bs=1 optimization-category waterfall](/images/blog/kimi-k3-day0-support/fig2-bs1-category-waterfall.svg)

**启动与拷贝消除（P1–P4，+19.9 tok/s）。** 让一步变小，而不是让内核更快：MoE 前向坍缩为一次 GEMM，KDA 的成对窄投影（paired skinny projections）合并（P1）；一次性能画像引导的清扫移除了逐层的上转型（upcast）、拷贝与多余启动（P2、P3）；路由变成对 [M, 896] logits 的单趟寄存器驻留基数选择（P4）。

**NVIDIA 计算内核（P5–P8，+10.3 tok/s）。** 四个阶段换入了与 NVIDIA 共同开发或由 NVIDIA 提供的内核，替换掉那些对 bs=1 形状不适用的默认实现：融合的 KDA 解码内核、位于我们路由旁路之后的 trtllm-gen W4A8 SiTU MoE cubin、TMA 注意力残差聚合，以及在小 M 场景取代 cuBLAS 的 CuTe-DSL TGV bf16 GEMM——每一项都经过与其他优化相同的 A/B 与精度把关。

**通信融合（P9、P12、P13，+27.6 tok/s）。** 收益最大的一段：面向 MNNVL 互联的融合 all-reduce 系列，构建在 CustomAllReduceV2 的对称内存平面之上——小消息用一次性组播存储（one-shot multicast stores），大消息用 NVLS 在交换机内归约，残差加法与 RMSNorm 也随集合通信一同完成（P9）。MoE 收尾随之移入集合通信的暂存步骤（P12），升投影从复制式改为列并行 GEMM，由组播 all-gather 收尾（P13）。

**重叠与序幕融合（P10、P11、P14、P15，+10.4 tok/s）。** 其余部分修剪剩余的关键链路：跨步输入的 MXFP8 量化（P10）、残差写回融合进上游内核尾部并在侧流上以独立分支执行（P11）、KDA 的 GEMV 链与 qkvg GEMM 重叠（P14），以及 MLA 解码序幕融合为单个内核并用 PDL 唤醒其后的注意力内核（P15）。

四根柱子背后的时间线阶梯：

![bs=1 decode throughput ladder](/images/blog/kimi-k3-day0-support/fig1-bs1-throughput-ladder.svg)

**可以推广的经验。** all-reduce 是一个同步点，因此在那里省下的一微秒会一比一地转化为步时；而一个落在其他流重叠空隙中的内核，只能以约十分之一的比率转化。在写内核之前先在 trace 里确认它是否位于关键路径上，是这场战役中杠杆率最高的单一习惯。

¹ 一次 rebase 将 P5 基线从 64.2 移到 63.8；该步相对 rebase 后的基线测量。
² P13 是合并窗口之后的重新校准规范基线，而非单一 PR 的归因。
³ 通向 P1–P4 的区段还包含后来被取代的过渡性优化（concat all-reduce → P9；tiny/1-CTA GEMV → P8；radix router v1 → P4；Marlin top-k-sum → P6/P12；早期注意力残差加法 → P7）；它们的瞬时收益体现在曲线中，但没有具名数据点。

## K3 的并行化

对 K3 的混合架构而言，常规的并行选择都站不住脚。张量并行无法切分 MLA 的 KV 缓存（只有一个 KV 头，无从按头拆分），因此每个 rank 都持有完整副本；它还会把每个 GEMM 切成八份并为每一层支付一次集合通信。纯 DP 注意力则改为在每个 rank 上复制注意力权重——KDA 约 61 GB、MLA 约 11 GB——占用的正是 KV 缓存和 KDA 状态所需要的内存。预填充与解码在这些代价下失利的方式各不相同，因此 K3 按阶段拆分答案：预填充用分块流水线并行，解码用上下文并行。

### 预填充：分块流水线并行

在 TP 预填充中，每一层都以一次 AllReduce 结束——这是一个无法与计算重叠的屏障。流水线并行改为按层切分模型：K3 的 93 层变成 8 个阶段（stage），提示词被切成多个 chunk，在其中流水式通过：

<p align="center">
  <img src="/images/blog/kimi-k3-day0-support/fig-pp-chunked.svg" width="98%" alt="Chunked pipeline-parallel prefill: a long prompt cut into chunks streaming through pipeline stages, with P2P hand-off arrows running under the next chunk's compute, contrasted with TP where every layer ends in an AllReduce barrier.">
</p>

<p align="center">
  <em><b>分块流水线并行预填充。</b>各阶段同时处理不同的 chunk。阶段间的交接在处理下一个 chunk 的计算期间运行，因此在 K3 上有 91% 被隐藏。TP（底部条带）下，每层都以一次所有 rank 都要等待的 AllReduce 结束。</em>
</p>

这样做有三重收益。仅剩的通信——向下一阶段的交接——隐藏在下一个 chunk 的计算之后。每个 rank 运行完整的层，因此 GEMM 宽了八倍、效率更高。而且每个阶段只为自己的约 12 层持有 KV 和激活值，使得超长提示词的预填充也游刃有余。但流水线必须足够深：浅的 PP4×TP2 无法掩盖其交接开销，还要支付 TP2 的 AllReduce，实测性能并不比 TEP8 好。

在 2×4 GB300 上以 8K 预填充测得，拓扑是唯一变量：

<p align="center">
  <img src="/images/blog/kimi-k3-day0-support/fig-pp-prefill.svg" width="98%" alt="Left: prefill throughput per GPU vs concurrency, TEP8 vs PP8xTP1. Right: cost decomposition per 1k tokens, compute plus exposed communication, for TP8 / PP4xTP2 / TEP8 / PP8xTP1.">
</p>

<p align="center">
  <em><b>深流水线在两个维度上都赢。</b>左：越过 c1–c4 交叉点后，PP8×TP1 攀升至约 1.7 倍 TEP8 的上限，且首 token 延迟（TTFT）更低。右：相同每 rank FLOPs 下每 1k 预填充 token 的成本；PP4×TP2 与 TEP8 在计算与通信之间互相抵消而打平，PP8 在两项上都是最便宜的。</em>
</p>

PP8 只在单请求时落败，而一个只会闲置的预填充 worker 本来就是配置错误。在 K3 的分离式服务部署中，预填充节点运行 PP8。它们每一个拥有 TEP8 节点 1.45 到 1.72 倍的预填充能力，因此一个预填充节点可以喂饱多个解码节点。解码节点运行 TP 或 DCP，下一小节将介绍。

### 解码：上下文并行

解码是复制式 KV 缓存成为瓶颈之处：多一个请求、或多一千个 token，都要在每个 rank 上多占同样的字节。解码上下文并行（DCP）改为按 token 位置而非按头切分 MLA 的 KV。当 p mod N 等于 r 时，rank r 拥有位置 p，于是每个 rank 交错持有每个请求上下文的 1/N，且这种切分在注意力内核之上是不可见的：

<p align="center">
  <img src="/images/blog/kimi-k3-day0-support/fig1-kv-layout.svg" width="98%" alt="TP replicates the same token positions on every rank; DCP stripes them round-robin, so the same GPUs hold N times the logical context.">
</p>

<p align="center">
  <em><b>按位置切分。</b>同样的 16 个 token 位置分布在 4 个 rank 上：TP 存储 64 份物理副本，DCP 只存 16 份。省出的字节变成逻辑 KV 容量，在 K3 上用 DCP8 约为 7.9 倍。</em>
</p>

按位置切分会破坏 softmax，因为每个 rank 只看到 1/N 的键，而部分 softmax 不可相加。解法是 FlashAttention 自身的那一套：每个 rank 返回其部分注意力输出以及每头的 log-sum-exp，每层用一次 all-to-all 交换它们，使每个 rank 最终在完整上下文上得到 1/N 的头。随后基于 log-sum-exp 的本地合并是精确的，且结果恰好就是 TP 下输出投影所期望的头布局。每层一次集合通信就是全部的通信代价：

<p align="center">
  <img src="/images/blog/kimi-k3-day0-support/fig2-dcp-dataflow.svg" width="98%" alt="Per-layer MLA decode dataflow on two DCP ranks: replicated query projection, local attention over owned positions producing partial output and LSE, one packed all-to-all, local LSE merge.">
</p>

<p align="center">
  <em><b>解码一步，逐层来看。</b>每个 rank 在本地投影全头查询，只对它拥有的位置做注意力，并用单次打包的 all-to-all 送出部分输出及其 log-sum-exp。本地合并之后留下标准的 TP 头布局；注意力下游的一切都不变。</em>
</p>

其余一切原封不动。DCP 组在 TP 组内部构建，因此 TP8 + DCP8 仍然是 8 张 GPU，MoE 沿用它已有的并行方式。KDA 是那条解释规则的例外：它的状态是每请求一个固定大小矩阵而非每 token 一个，没有位置轴可切分，因此 KDA 层保持按头做 TP 切分。整个功能就是一个 flag：`--dcp-size N`。

它的价值在智能体流量上显现，那里十万 token 级的会话在缓存中不断堆积。在 2×4 GB300 上重放真实的编程智能体会话，两侧都带主机内存 KV 层，DCP 是唯一差别：

<p align="center">
  <img src="/images/blog/kimi-k3-day0-support/fig4-dcp-vs-tp-hicache.svg" width="98%" alt="Aggregate decode throughput versus concurrent agent sessions, TP8 plus hicache versus DCP8 plus hicache: TP8 collapses at 16 sessions when the active set outgrows device KV, DCP8 keeps climbing to 541 tok/s at 48 sessions.">
</p>

<p align="center">
  <em><b>DCP 移除了活跃集合之墙。</b>主机内存层能救回重预填充流量，但在 16 个并发会话时，活跃工作集超出了 TP8 的设备端 KV，吞吐量崩塌。DCP8 把逻辑 KV 从 1.5M 提升到 12.2M token，让同一负载在 48 个会话时仍达到 541 tok/s。</em>
</p>

DCP 能与栈的其他部分组合。DSpark 的验证步就是一步解码，因此它走同样的复制 Q、单次 all-to-all 的路径；在 PD 分离部署下，预填充侧对 DCP 完全无感知，每个解码 rank 只需在传输边界拉取它拥有的位置——这正是 PP 或 TP 预填充能够喂 DCP 解码的原因。剩余的上限是 KDA：它的每请求状态无法按位置切分，因此一旦 DCP 抬高了 MLA 之墙，运行中请求数上限就成为新的约束；上文内存章节中的统一内存设计解决的正是这个问题。

### 组合所有策略

各部分如何组合最终要靠测量。把 PD 分离纳入实验，让预填充拓扑、解码拓扑和预填充：解码比例变化，得到服务前沿（serving frontier）：

<p align="center">
  <img src="/images/blog/kimi-k3-day0-support/fig-pareto-pd.svg" width="98%" alt="K3 serving frontier under PD disaggregation: total throughput per GPU versus per-user decode speed for PP8 and TP8 prefill feeding TP8, DCP8, EP and multi-instance TP8 decode arms; the frontier runs from PP8 to TP8 at the throughput end out to TP8 feeding three TP8 instances at the interactive end.">
</p>

<p align="center">
  <em><b>服务前沿。</b>在吞吐端，一个 PP8 预填充 worker 喂一个 TP8 解码节点，在 fp4 配置上达到 2,808 tok/s/GPU；DCP 组合——两个 PP8 预填充 worker 喂两个 DCP8 解码节点——以 2,633 紧随其后。向右移动是预填充：解码旋钮在起作用：一个预填充 worker 依次喂两个、三个、四个独立解码实例，用聚合吞吐换取每用户速度，一路走到每用户超过 116 tok/s。</em>
</p>

## RL：在原生 MXFP4 基座上进行 LoRA 训练

K3 的 Day-0 强化学习采用与 Miles 共置（colocated）的 LoRA 训练：BF16 训练器运行在 Miles 的 Megatron 后端上，原生打包 MXFP4 的 SGLang rollout 引擎与它共享同一批 64 台 GB300。后端覆盖 KDA、NoPE-MLA、注意力残差 bank 和潜在 MoE，支持 TP/SP/PP/CP/EP。

### LoRA 服务与权重同步

引擎按出厂原样服务检查点，从不改写它。每步只传输 BF16 LoRA 适配器，引擎把增量作为量化基座 GEMM 之上的独立 BF16 `B(Ax)` 项施加，因此策略更新以全精度作用在 4 比特基座权重之上。稠密投影走 SGLang 的 Triton LoRA 后端，896 个路由专家走 Marlin 路径上的融合 MoE-LoRA 内核，共享专家增量折叠进融合 MoE 前向 GEMM。适配器常驻 GPU 内存，因此同步只是原位替换，没有 rollout 侧的 BF16 拷贝，没有全量权重同步，循环里也没有重新量化步。

### 并行

**流水线并行。** K3 的注意力残差 bank 必须跨越阶段边界，但 Megatron 的点对点通信只携带一个隐状态张量，因此阶段边界把 `[prefix_sum, bank]` 打包进该张量，并在入口处解包。Megatron 本身未做任何改动。

**上下文并行。** bank 的切分是免费的，因为每个注意力残差操作都是逐 token 的。MLA 也不需要 K3 专用代码：旋转表（rotary table）切分是 Megatron 的 MLA 中唯一需要感知 CP 的部分，而 K3 没有旋转位置嵌入，因此它的投影直接落在原生 TE 注意力核心上并继承 CP。KDA 是需要下功夫的部分，它要经过 fla 的 CP 支持来处理循环状态和卷积 halo。它想要一段连续的 rank 本地分块，而 Megatron 存储的是 zigzag 顺序、ring attention 所期望的布局，因此重排只在 KDA 附近执行。

**专家并行。** 适配器把潜在侧因子在全部 896 个路由专家间共享，其余因子按专家保留，与引擎的融合 MoE-LoRA 契约相匹配。这个共享因子在 EP 上复制但被标记为专家并行参数，因此 DDP 只在专家 DP 范围内对它归约，而 EP 求和是框架额外自行添加的唯一梯度归约。

### 内存

原生 MXFP4 rollout 的峰值接近每 GPU 225 GiB，BF16 训练器在初始化时接近 155 GiB，而显存卡只有 277 GiB，因此两者绝不同时驻留：一方休眠时另一方运行，共置的前提是每次交接都不留残余。

**基座永不动。** 引擎在整个训练过程中把基座权重保留在 GPU 上，训练器工作期间只释放 KV 缓存和 CUDA 图。既然基座从不释放，也就从不需要恢复，LoRA 路径完全不传输任何基座字节：基座同步被完全跳过。

**进程组保持在线。** 训练器的 NCCL 通信器缓冲区不属于 torch 分配器内存，卸载机制无法释放它们，而显而易见的做法是休眠时销毁进程组、唤醒时重建。这用每轮一次的重建与 EP 预热换取常驻的几 GiB——只有当引擎确实需要那些字节时才值得支付，而在这里引擎并不需要，因为更新路径上不经过任何基座权重。进程组保持在线。

**适配器传输按 chunk 限界。** 适配器约含 2,800 个张量。每个 chunk 作为一个扁平化的 CUDA IPC 桶发送，共 278 个；一旦接收方确认且所有生产者 rank 都跨过引擎组屏障，它就被回收。这为每个 chunk 的瞬态 IPC 内存设定了上界，而不是让它随传输不断累积——在峰值时价值约 48 GiB/GPU。

**主机端拷贝只存在于有人读取之处。** 引擎在适配器装入 GPU 池后即释放其 CPU 拷贝，把调度器 RSS 从 76–88 GiB 降到约 17 GiB；CPU 拷贝已不存在的适配器无法重新装入，因此池驱逐会被报错拒绝，而不是静默服务一个过期槽位。训练器侧的 DDP 缓冲区按生命周期划分：适配器参数缓冲区留在 CPU 支撑区域，因为权重更新会在训练器休眠时读取它们；梯度缓冲区可以重建，进入休眠即丢弃的无备份区域。

### 验证

训练正确性是 RL 支持栈中最重要的部分。我们在配方工作之前就构建了这些检查。

**训练/rollout KL**，每次 rollout 都会记录，是关于 KL(rollout ‖ train) 的 Schulman k3 估计，在被采样 token 上由引擎返回的 log 概率与训练器重算的 log 概率计算得出。它只是一个诊断量，不属于目标函数，本配方不携带任何 KL 惩罚。它的下限约 2e-3，由以 MXFP4 服务基座决定；随步数增长则是发散的信号。

**金丝雀同步探针。** 一条轨迹从第一次 rollout 起就被固定，每一步都由引擎（在当前适配器下）和训练器（在同一策略版本下）同时打分。两条曲线的共动证明训练出的适配器真正到达了推理侧：传输校验和只能证明字节到达了，不能证明有人在读它们。

**张量级 dump 对比。** 相同的 token 跑过两个构建版本或两种并行布局，dump 每个前向激活和每个参数梯度，以相对 L2 和余弦相似度对照实测噪声底进行比对。逐位一致不是标准，因为同样的算术在两组不同 GPU 上本来就会在 ulp 级别产生差异。流水线边界和上下文并行布局正是这样验证的：在 CP=2 与 CP=1 构建出完全相同调用的地方两者逐位一致，一次前向内核替换落在余弦中位数 0.996。

**权重同步断言。** 训练器与引擎之间的逐张量 SHA256 清单、一个在适配器更新未改变任何导出张量时报错的验证器、一个检查版本 1 时所有 `B` 因子为零的检查，以及适配器梯度与优化器步检查。

### 训练结果

报告的这次运行是 16 节点 × 4 GB300 上的 DAPO 数学任务：BF16 训练器以 TP8 / PP8 / EP8 与原生 MXFP4 rollout 引擎共置，4096-token 响应，每次 rollout 采样 64 个样本，每次 rollout 一次优化器步，rank-32 / α-64 LoRA，学习率 1e-5，GRPO 不带 KL 项，运行至 12 小时墙钟上限。AIME-2024 贪心评测在 60 步内从 43.3% 攀升至 76.7%，30 题中从 13 题升至 23 题，且在截止时仍在上升；训练/rollout KL 则全程稳定在约 2e-3 的 MXFP4 量化下限。

<p align="center">
  <img src="/images/blog/kimi-k3-day0-support/rl-training-curves.svg" width="100%" alt="Three RL training curves side by side: rollout raw reward trending upward, AIME-2024 eval accuracy climbing, and train/rollout KL flat at the MXFP4 quantization floor.">
</p>

<p align="center">
  <em><b>12 小时 DAPO 运行。</b>左：每次 rollout 64 个采样响应的平均奖励，按响应通道打分；每次 rollout 抽取不同的 prompt 批次，因此趋势才是信号，单步数值是噪声。中：AIME-2024 贪心通过率，每 10 次 rollout 评测一次，使用与训练相同的 4096-token 限制，因此超限的正确解按未通过计分。右：在被采样 token 上关于 KL(rollout ‖ train) 的 Schulman k3 估计，仅作汇报、从不加进损失；平稳在量化下限是目标，单调增长则是发散的信号。</em>
</p>

## 致谢

这项工作是 RadixArk 的 SGLang & Miles 团队与 Moonshot AI 团队的合作成果，同时得到了 NVIDIA、AMD、Approaching AI、Baseten 和 Modal 的支持。

**AMD**：Wun-guo Huang, Xinyi Song, Hai Xiao, Soga Lin, Duyi Wang, Thomas Wang

**Approaching AI**：Huanming Shen, Xiaohao Zhang, Nan Li, Mingxing Zhang

感谢 DigitalOcean 为我们的测试提供 AMD 实例。

感谢 Google Cloud、DigitalOcean、Nebius、fal、RunPod、DeepInfra 和 GMI Cloud 在 SGLang 上服务 Kimi K3。
