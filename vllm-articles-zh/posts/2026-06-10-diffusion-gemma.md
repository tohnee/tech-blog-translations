---
title: "DiffusionGemma：首个在 vLLM 中获得原生支持的扩散 LLM（dLLM）"
title_en: "DiffusionGemma: The First Diffusion LLM (dLLM) Natively Supported in vLLM"
source: https://vllm.ai/blog/2026-06-10-diffusion-gemma
crawled: 2026-09-12
translated: 2026-09-13
---

# DiffusionGemma：首个在 vLLM 中获得原生支持的扩散 LLM（dLLM）

> 原文：[DiffusionGemma: The First Diffusion LLM (dLLM) Natively Supported in vLLM](https://vllm.ai/blog/2026-06-10-diffusion-gemma) · vLLM 博客

作者：vLLM 团队与 Google DeepMind 团队

[#模型](https://vllm.ai/blog/tags/model)[#生态系统](https://vllm.ai/blog/tags/ecosystem)[#推理](https://vllm.ai/blog/tags/inference)

> **提示：** 想要部署 DiffusionGemma？请参阅 [vLLM recipe](https://recipes.vllm.ai/Google/diffusiongemma-26B-A4B-it) 获取部署说明。

Google 的 DiffusionGemma 是一个基于 Gemma4 骨干构建的 26B 参数离散扩散语言模型，也是首个获得 vLLM 支持的 dLLM。把 DiffusionGemma 集成进 vLLM，需要支持一种根本不同的解码模式。dLLM 无法干净地套进标准的自回归服务路径：它需要双向注意力、迭代精化、基于块的生成，以及每个去噪步骤上的自定义采样行为。

我们使用 [model runner v2](https://vllm.ai/blog/2026-03-24-mrv2) 的全新 ModelState 抽象把 DiffusionGemma 集成进 vLLM。该抽象允许模型定义自己的输入准备逻辑，并提供管理每请求模型特定状态的钩子。其结果在准确率上与 Hugging Face 参考实现一致，同时支持高效的批量服务。

标准自回归 Transformer 从左到右一次生成一个 token；扩散语言模型则不同，它通过迭代去噪一个固定长度的画布（canvas）来生成 token。这让模型可以在多个去噪步骤中并行精化多个 token，实质上是用额外的计算换取显存带宽压力的缓解——在低批大小场景下这种取舍尤其有吸引力，因为此时算力富余而显存带宽才是瓶颈。一次前向传播生成大量 token 可以转化为极低延迟的响应。DiffusionGemma 具体来说每次对一个 256 token 的画布去噪。

![自回归 vs. 块扩散](https://vllm.ai/blog-assets/figures/2026-06-10-diffusion-gemma/ar-vs-diffusion.svg)

自回归 vs. 块扩散

自回归解码与块扩散解码的对比。

## DiffusionGemma 架构与采样循环

DiffusionGemma 构建在标准 Gemma4 骨干之上，但以共享同一套权重的两种模式运行它——同一组层，两种用法：

- **编码器模式**使用*因果*注意力并写入 KV 缓存。每个块运行两次：一次用于预填充提示，一次用于"提交"一个完成的块。
- **解码器模式**使用*双向*注意力且只读 KV 缓存。这就是去噪模式——画布中的每个位置都可以关注其他所有位置，这正是模型能够一次精化整块的原因。

由于编码器使用普通的因果注意力，且提交的 KV 的写入方式与自回归模型完全一致，vLLM 的自动前缀缓存开箱即用：共享的提示前缀可以在请求之间复用，无需任何扩散特定的改动。

单个 256 token 块的循环过程如下。提示预填充（编码器）之后，画布被初始化为随机 token，随后状态被置为去噪。每个去噪步骤都以解码器模式在完整画布上运行骨干网络，在每个位置采样一个候选 token，并决定保留哪些位置。一旦块不再变化，状态被置回编码，最后一轮编码器前向将其提交——写入它的 KV 并输出这 256 个 token——然后下一个块从一个全新的随机画布开始。

![DiffusionGemma 块采样循环](https://vllm.ai/blog-assets/figures/2026-06-10-diffusion-gemma/sampling-loop-horizontal.svg)

DiffusionGemma 块采样循环

DiffusionGemma 的每块采样循环。

在一个块内，所有 256 个位置并行去噪；跨块而言，生成仍然从左到右，因为每个新块都以所有此前已提交的 token 为条件。

### 熵约束去噪

每个去噪步骤都会对*全部*画布位置重新采样，但只有模型有信心的位置会被保留；其余位置被丢弃，并在下一步用新的随机 token 替换。置信度以每个位置预测分布的熵来度量——低熵意味着模型基本已经拿定主意。

DiffusionGemma 用一条**熵约束（entropy-bound）**规则来决定接受多少个位置：它从最自信的位置走到最不自信的位置，逐个接受 token，直到累计熵超过固定预算。早期模型对几乎所有位置都不确定，所以只有少数位置被锁定。随着这些锚点把上下文传播给邻近位置，分布变锐，更多位置落入预算之内，块在几步之内就聚焦成形。

![上下文中的块去噪](https://vllm.ai/blog-assets/figures/2026-06-10-diffusion-gemma/denoising-grid.svg)

上下文中的块去噪

跨若干步骤的熵约束去噪。

当画布的最佳猜测（argmax）预测连续几步不再变化，**并且**每个 token 的平均熵降到置信阈值以下时，就认为它**收敛**了——或者它达到了硬性的去噪步数上限。此时提交的 token 是那个干净的 argmax 预测，而不是各步之间携带的嘈杂采样画布。

### 自条件化

为了让去噪循环更稳定、收敛更快，DiffusionGemma 使用了**自条件化（self-conditioning）**：在步骤之间，模型以*自己上一步的预测*为条件。它不是回传硬 token，而是回传上一步的完整 softmax 分布，将其转换为 token 嵌入的概率加权平均，再通过一个小型门控 MLP 把它加到画布嵌入上，然后进入下一轮。

![自条件化](https://vllm.ai/blog-assets/figures/2026-06-10-diffusion-gemma/self-conditioning.svg)

自条件化

自条件化反馈路径。

这让每一步都带着对模型上次所持信念的记忆，因此即使是被重新加噪为随机 token 的位置，也能继承上一步的信息，而不必从头开始。自条件化只在解码器/去噪模式下生效——在编码器的预填充与提交前向中，反馈被置零，这些前向看到的就是普通的 token 嵌入。

## 在 vLLM 中的实现

### 复用投机解码数据路径

vLLM 引擎已经拥有一条非常成熟、稳定的投机解码路径。受 [RFC #36155](https://github.com/vllm-project/vllm/issues/36155) 启发，我们复用这条路径来实现 DiffusionGemma。对 vLLM 中的扩散 LLM 而言，复用投机解码路径是水到渠成的：每一步的当前画布可以看作一大批草稿 token，它们要么被整体拒绝，要么被整体接受。这使得对调度器、model runner 等核心 vLLM 组件的改动非常少。一个显著的例外是：投机解码路径总是会额外采样一个 token（在投机解码文献中通常称为 bonus token），为此我们增加了采样 0 个 token 的支持，该行为由 ModelState 控制。

具体而言，扩散模型按如下方式接入现有技术栈——调度器、model runner 与 Gemma4 骨干原样复用，只有 ModelState 和采样器是扩散专属的：

![DiffusionGemma 如何接入 vLLM 的投机解码技术栈](https://vllm.ai/blog-assets/figures/2026-06-10-diffusion-gemma/stack.svg)

DiffusionGemma 如何接入 vLLM 的投机解码技术栈

DiffusionGemma 在 vLLM 软件抽象中的位置。

### ModelState 接口

在 ModelState 之前，向 V1 添加一个非自回归模型需要分叉 model runner，并把扩散特有的状态穿过输入准备、注意力元数据和采样等环节。ModelState 通过定义一组由 runner 在前向循环各阶段调用的钩子避免了这一点：

| 钩子 | DiffusionGemma 用它来…… |
| --- | --- |
| `prepare_inputs()` | 嵌入画布 token 并应用自条件化 |
| `prepare_attn()` | 设置每请求的因果（编码器）或双向（去噪）注意力 |
| `custom_sampler()` | 用 `DiffusionSampler` 替换默认采样器 |
| `add_request()` / `remove_request()` | 初始化与拆除每请求的扩散状态（如画布与自条件化概率） |

模型通过在模型类上定义 `get_model_state_cls()` 来自行注册 ModelState。model runner 保持通用：每一步它调用 `prepare_attn(...)` 构建元数据，把 `prepare_inputs(...)` 合并进前向 kwargs，并把采样委托给 `custom_sampler()->DiffusionSampler` 安装的任何采样器。

这意味着添加一个新的块扩散模型只需实现一个 ModelState 加上模型类上的一行注册，无需改动 runner、调度器或任何共享基础设施。我们相信这可以成为未来把扩散语言模型干净地加入 vLLM 的蓝图。

### 组合起来：DiffusionGemmaModelState 与 DiffusionSampler

`DiffusionGemmaModelState` 是 `DiffusionGemma` 的 ModelState 实现。它持有每请求的状态（大多与扩散循环相关）：标识请求处于提交还是去噪阶段的相位标志、当前 `canvas`、用于收敛检查的历史、自条件化概率等。这些状态存放在预分配的 GPU 张量中并就地更新。`DiffusionGemmaModelState.prepare_inputs()` 嵌入画布 token 并应用自条件化：它取来自上一个去噪步骤的 softmax 分布（来自内部每请求状态），计算 token 嵌入的概率加权平均，并通过门控 MLP 喂给模型，让模型看到自己上一步的预测。`prepare_attn()` 构建注意力元数据，用相位标志决定注意力是因果（提交阶段/编码器）还是双向（去噪阶段/解码器）。由于单个批次可能同时包含预填充、去噪与提交请求的混合，且每请求的因果标志是在 GPU 上异步设置的，我们不得不对注意力内核做一些修改，后文会讨论。

`DiffusionSampler` 取代 vLLM 常规的 `(Sampler, RejectionSampler)` 组合，负责在相位切换时初始化与重置画布及每请求扩散状态。每步工作是一个单独的 `@torch.compile` 函数 `_compiled_sample_step`，对所有在途解码请求做向量化，覆盖三种情况：

- **预填充**：把画布初始化为随机 token，返回 `num_sampled = 0`。
- **去噪**：对 logits 做温度缩放，用 Gumbel-max 技巧（`argmax(logits/T + gumbel_noise)`）在每个画布位置抽取候选 token，接受最有信心的位置直至熵约束，并把其余位置重新加噪为随机 token。该步骤还记录 argmax 画布并检查收敛：argmax 画布已稳定保持配置的步数且平均熵低于阈值，或达到步数上限。
- **提交**：输出干净的 `argmax_canvas`（`num_sampled = 256`），为下一个块重新初始化画布，并重置每请求状态。

在去噪期间，采样器报告 `num_sampled = 0` 且 `num_rejected = query_len`，因此 KV 缓存位置不会前移；只有提交才会推进它。把每个画布位置都标记为拒绝，就是在告诉调度器保持序列原地不动，并在下一步重新调度同一个块——这让整个去噪循环留在现有投机解码的记账体系内，无需改动调度器。

### 动态的每序列因果注意力

如上所述，DiffusionGemma 以两种模式运行：使用因果注意力的**编码器**模式，以及使用双向注意力的**解码器**模式。在此之前，因果性是整个批次统一的单一属性——同一次前向传播中的每个请求共享同一种掩码类型。典型的解码器模型只用因果注意力，而 Whisper 这类编码器-解码器模型只在编码器层使用双向注意力。但 DiffusionGemma 的请求会在这些模式之间交替：先预填充提示，然后画布被迭代地去噪与接受。为了尽量降低延迟，vLLM 在每次前向传播中把处于不同阶段的请求混合进同一批次。因此我们实现了**动态的每序列因果注意力**，让注意力掩码适配每个请求的因果性。下图描绘了这种情况：这里展示一个包含三个请求的批次，每个请求处于不同阶段。

- 请求 0 是长度为 6 的预填充，因此使用因果注意力（"编码器"前向），对角线以上的条目被屏蔽——每个 query token 只关注直至并包含自身的 token 的 key。还要注意注意力是分块（tile）计算的（本例中形状为 2x2，实际中块要大得多，且根据硬件做了调优），只含被屏蔽条目的块会被完全跳过，既节省计算，也节省从 HBM 加载其 K/V 块的显存带宽。
- 请求 1 已完成长度为 6 的预填充，现在正以解码器模式生成新 token。在大小为 4 的画布内，所有 query 通过双向注意力关注画布中的所有 key。它们也关注上下文中的所有 key。没有任何条目被屏蔽，也没有任何块被跳过。
- 最后，请求 2 已完成去噪步骤，其画布准备好被接受。我们再运行一次编码器前向，使用因果注意力，把新接受 token 的条目写入 KV 缓存。同样，所有 query 也会关注缓存中的 key。

![动态的每序列因果注意力](https://vllm.ai/blog-assets/figures/2026-06-10-diffusion-gemma/per_seq_causal_attention.svg)

动态的每序列因果注意力

动态的每序列因果注意力。

我们在两个注意力后端中支持这种动态因果注意力：Triton Attention（`TRITON_ATTN`）与 FlashAttention 4（`FLASH_ATTN`）。在这两个后端中，单一布尔参数 `causal` 被替换为指示每个请求因果性的张量。掩码相应更新，分块行为保持不变。

### 滑动窗口注意力

最后，DiffusionGemma 的某些层使用滑动窗口注意力。对画布中的 token 来说，滑动窗口注意力还必须变成对称的：对于窗口大小 `W`，画布中的 token 不只关注自己和它之前的 `W` 个 token，还关注它之后的 `W` 个 token，总窗口大小为 `2*W + 1`。我们在下图中描绘了这一点：

![每序列滑动窗口注意力](https://vllm.ai/blog-assets/figures/2026-06-10-diffusion-gemma/per_seq_sliding_window.svg)

每序列滑动窗口注意力

动态因果滑动窗口注意力。

与前面一样，同样的三个请求展示在一个 `W=2` 的滑动窗口层上。请求 0 和请求 2（预填充与接受）保持单侧因果窗口——每个 query 关注自身及其之前的 `W` 个 key，把注意力收窄到沿对角线的一条带——而请求 1 的去噪画布使用对称窗口，关注两侧各 `W` 个 key，因此也只关注落在窗口内的上下文 token。

要在两个后端中都支持这一点，只需为双向请求修改窗口的右边界：因果请求保持仅左侧的窗口，而双向请求使用两侧各为 `W` 的对称窗口。

## 量化检查点支持

DiffusionGemma 模型的量化检查点使用 [LLM Compressor](https://github.com/vllm-project/llm-compressor) 创建，并以 [compressed-tensors](https://github.com/vllm-project/compressed-tensors) 格式保存。其中包含一个权重量化、激活值全动态的 FP8 模型，以及一个权重与激活值都量化为 NVFP4 格式的 NVFP4 模型。

量化检查点可在 RedHatAI hub 上找到：

1. <https://huggingface.co/RedHatAI/diffusiongemma-26B-A4B-it-NVFP4>
2. <https://huggingface.co/RedHatAI/diffusiongemma-26B-A4B-it-FP8-dynamic>

为验证模型准确率，我们使用 vLLM 在开启与关闭思考模式两种设置下，在 AIME 2025、GPQA Diamond 与 GSM8k 基准上进行了初步评估。评估结果与恢复分数（recovery scores）见模型卡片。

## 结果

DiffusionGemma 的架构支持极低延迟推理，非常适合交互式应用。为在这种场景下评估我们实现的性能，我们使用内置的 `vllm bench serve`，在单张 H100 与 H200 上以 batch size 1 对 vLLM 进行了基准测试。FP8 扩散模型达到 **H200 上每秒 1,288 个生成 token**（约为标准自回归基线的 6 倍、使用多 token 预测的基线的 3 倍）以及 **H100 上每秒 1,008 个 token**（分别约为 5 倍与 2.6 倍）。

![H100 与 H200 上的生成吞吐量：FP8 扩散 vs. 自回归基线](https://vllm.ai/blog-assets/figures/2026-06-10-diffusion-gemma/perf.svg)

H100 与 H200 上的生成吞吐量：FP8 扩散 vs. 自回归基线

H100 与 H200 上的生成吞吐量——FP8 扩散 vs. 自回归基线。[复现命令](https://gist.github.com/LucasWilkinson/89185e4dc05d300df33a4ce030973911)

## 致谢

感谢每一位为把 DiffusionGemma 带入 vLLM 做出贡献的人。这是 Google DeepMind 与 vLLM 团队的紧密合作。

- **Google DeepMind：** Martin Kukla、João Gante、Luciano Martins
- **vLLM：** Lucas Wilkinson、Matthew Bonanni、Nicolò Lucchesi、Dipika Sikka、Doug Smith、Edward Arthur Quarm Jnr、Alon Kellner（Red Hat）、Nick Hill（Inferact）
- **NVIDIA：** Dimitrios Bariamis、Alec Kohlhoff、Porras Huang、Eugene Rakhmatulin
