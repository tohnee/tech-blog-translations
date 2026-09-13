---
title: "SGLang 与 Miles 为前沿多模态模型 Inkling 提供 Day-0 支持"
title_en: "SGLang and Miles Add Day-0 Support for Inkling, a Frontier Multimodal Model"
author: "SGLang Team & Thinking Machines Lab"
date: "July 15, 2026"
previewImg: /images/blog/inkling-day0-support/inkling-cover.png
type: blog
source: https://lmsys.org/blog/2026-07-15-inkling-day0-support/
translated: 2026-09-12
---

# SGLang 与 Miles 为前沿多模态模型 Inkling 提供 Day-0 支持

> 原文：[SGLang and Miles Add Day-0 Support for Inkling, a Frontier Multimodal Model](https://lmsys.org/blog/2026-07-15-inkling-day0-support/) · LMSYS Blog · SGLang Team & Thinking Machines Lab

我们很高兴与 Thinking Machines 团队合作，为 Inkling 带来 SGLang 与 Miles 的 Day-0 支持（首发日支持）——针对其新架构做了专门优化，特性覆盖也十分广泛；同时我们还与 Modal 合作，为 Inkling 训练了一个 DFlash 草稿模型。

**亮点**

- Inkling 是一个 975B 参数的多模态模型，上下文窗口最长可达 1M token，其特色包括短卷积（ShortConv）、带相对位置嵌入的注意力，以及一种带共享专家 sink（shared-expert sink）的新型 MoE 设计。
- 得益于针对 Inkling 架构的专门优化，SGLang 在 Nvidia Blackwell GPU 上实现了最高 71.7k tok/s 的输入吞吐量和 171.0 tok/s 的单用户解码速度。
- SGLang 为 Inkling 提供广泛的特性支持，包括投机解码（speculative decoding）、PD 分离（预填充-解码分离）、NVIDIA GPU 上的 bf16 + NVFP4 checkpoint 支持、AMD GPU 上的 bf16 checkpoint 支持、多 LoRA 推理服务，以及 HiCache。
- SGLang 支持 DFlash 投机解码，所用草稿模型由 Modal 专门为 Inkling 训练。
- Miles 在定制化的 Megatron 后端中实现了 Inkling，支持 DP/PP/TP/SP/EP/CP，可对文本和视觉语言任务进行全参数与 LoRA 强化学习（RL）。
- Miles 通过定制算子、路由重放（routing replay）与跨运行时参数同步来保证训练-推理一致性，并在纯文本和多模态推理任务上，以 LoRA 与全参数两种训练方式均带来稳定的 RL 提升。

SGLang 启动命令：**[Cookbook](https://docs.sglang.io/cookbook/autoregressive/ThinkingMachines/Inkling)**

Miles 启动命令：**[文档](https://miles.radixark.com/docs/models/thinkingmachines/inkling)** · Miles PR：**[miles#1683](https://github.com/radixark/miles/pull/1683)**

## Inkling 模型架构

Inkling 在标准 decoder-only Transformer 架构的基础上引入了三个组件：短卷积（ShortConv）、带相对位置嵌入的注意力，以及 MoE 中的共享专家 sink。

### 概览

<p align="center">
  <img src="/images/blog/inkling-day0-support/model_arch.png" width="98%" alt="Inkling model architecture: attention and MoE submodules with ShortConv, relative logits, and the shared-expert sink">
</p>

<p align="center">
  <em>图 1：Inkling 的模型架构。</em>
</p>

上图展示了 Inkling 在注意力和 MoE 上的设计，两者都以同一种新方式收尾：在残差连接之前接一个短卷积（`ShortConv`）。注意力还在 Q/K 归一化之前对 K 和 V 做短卷积，并用一个可学习的、以 query 为条件的相对位置偏置（`RelLogitsProj`）直接加到注意力 logits 上，以取代位置嵌入。MoE 则在 top-k 路由中引入共享专家 sink（`Sink`）。与传统的共享专家 MoE——在路由器之外叠加一条常开的共享路径、与路由互不干扰——不同，Inkling 的路由器同样会给共享专家打分，并把它们的权重与被选中路由专家的权重放在一起归一化，使两者从同一个共享权重预算中分配。

### 短卷积（ShortConv）

短卷积是在 token 维度上进行的短程逐通道因果卷积。对于位于位置 $t$、通道 $c$ 的隐藏状态，它会读取当前 token 以及同一通道上之前的 $W - 1$ 个位置。

$$
y_{t,c} = x_{t,c} + \sum_{d=0}^{W-1} w_{c,d}\, x_{t-d,\,c}
$$

当前的 Inkling 配置取 $W = 4$。ShortConv 在每个 decoder 层中出现四处：

* **K 流 ShortConv**——紧跟 K 投影之后、Q/K 归一化之前。
* **V 流 ShortConv**——紧跟 V 投影之后。
* **注意力输出 ShortConv**——作用于注意力的输出。
* **MLP/MoE 输出 ShortConv**——作用于 MLP/MoE 的输出。

### 带相对位置嵌入的注意力

在 Inkling 中，每个注意力层都会把一个可学习的、按注意力头划分的相对位置偏置直接加到 softmax 之前的 logits 上。除 $q_{t,h}$、$k_{t,h}$ 和 $v_{t,h}$ 之外，每个 query token 还携带一个相对特征 $r_{t,h}$。借助可学习投影 $P$，该特征被投影为一组按因果距离桶 $d$（从 $0$ 到 $\text{rel\_extent}-1$）索引的相对 logits 向量：

$$
\text{rel\_logits}(t,h,d) = r_{t,h}^{\top} P_{:,d}
$$

对于 query $i$、key $j$ 和注意力头 $h$，注意力 logit 会在缩放点积之上直接加一项相对位置偏置，该偏置按相对距离从 query 的相对 logits 中选取：

$$
\ell(i,j,h) = \alpha \cdot q_{i,h}^{\top} k_{j,h} + \mathbb{1}[0 \le i-j < \text{rel\_extent}] \cdot \text{rel\_logits}(i,h,\,i-j)
$$

其中 $\alpha$ 是注意力缩放因子。未来位置照常由因果掩码处理；在全注意力中，超出 $\text{rel\_extent}$ 的距离则贡献零偏置。

**注意力布局。** Inkling 在同一堆叠中混合使用滑窗注意力与全注意力层——两种变体都使用相对注意力，只是掩码方式不同。默认布局以「五个滑窗层 + 一个全注意力层」为一个周期循环（$\text{layer\_id} \bmod 6 = 5$），让模型在低成本的局部层之外，周期性地获得能处理远程信息的全上下文层。全注意力层还额外支持对 $q_{t,h}$ 和相对 logits 施加随长度变化的对数缩放因子，使模型可以随上下文增长调整 logit 的量级；局部层因窗口大小固定而不需要这一点。

### 带共享专家 sink 的 MoE

Inkling 的前馈模块是标准的 sigmoid 门控 top-k MoE——路由器打分、top-k 选择、对被选专家的权重重新归一化——只有一处例外：它的两个共享专家是如何融入的。大多数共享专家 MoE 设计会在其上叠加一条*独立*的稠密路径，这些常开专家从不与路由器竞争概率质量。Inkling 则把路由专家与共享专家*放在一起*打分：top-k 选择仍然只从路由专家池中挑选，但一旦选定，被选中路由专家的得分就会与共享专家的得分拼接为一个整体并重新归一化：

$$
(w_{\text{routed}}, w_{\text{shared}}) = \operatorname{normalize}\big(\log \sigma(s_{\text{routed}} \,\Vert\, s_{\text{shared}})\big)
$$

随后两组权重分别缩放各自专家的输出，并累加进同一个结果。

## SGLang 优化

Inkling 的三处架构改动，每一处都打破了标准 decoder-only 推理服务器赖以调优的某个假设。要让 Inkling 在 SGLang 上跑得快，就得为每一处设计新的算子和执行策略。

### ShortConv 优化

ShortConv 本身很小——就是一个 $W=4$ 的逐通道因果滤波器（见上文「短卷积（ShortConv）」一节）——但它出现在注意力内部两处（K、V）以及残差流周围两处（注意力输出、MLP 输出），遍布 Inkling 的每一个 decoder 层。

**KV ShortConv + QK-norm + KV 写入。** K 流与 V 流的 ShortConv 正好位于 Q/K 归一化和 KV 缓存写入之前。SGLang 把这三个步骤——K/V 卷积、Q/K RMSNorm 以及 KV 缓存写入——融合进一个注意力前置（prologue）算子。

**All-reduce + ShortConv（解码时还融合 RMSNorm 与残差）。** 注意力输出和 MLP 输出的 ShortConv 位于残差流上，恰好处在张量并行 all-reduce 已经运行的位置——而 all-reduce 本身开销不小。SGLang 构建了一系列定制 all-reduce 算子来削减这部分开销，比 torch 的 `multimem_all_reduce_` 最高快 **2.1×**。由于 ShortConv 紧随 all-reduce 之后，SGLang 将其直接融合进 all-reduce 算子，而不是单独启动。在解码阶段，RMSNorm 和残差相加也被折入同一个算子，因为解码的单 token 形状让这些额外步骤的代价很小。融合后的算子比未融合的调用链快 **2.08–3.60×**，在整个输入长度扫描范围内带来 **+5–8%** 的端到端吞吐量提升。

**预填充全量 CUDA 图。** 可中断 CUDA 图（BCG，Breakable CUDA Graph）与分段 CUDA 图（PCG，Piecewise CUDA Graph）是削减预填充阶段 CPU 启动开销的标准手段：一次性捕获前向计算的大部分内容，之后每步直接重放，无需重新派发 Python。但只要有算子需要实时的逐请求元数据，两者都得回退到 eager 执行；而 Inkling 每层有四处 ShortConv 恰恰如此，还不算注意力自身的那处。每处的 eager 回退都是一段真实的多层 Python 调用栈，而不是单次算子启动：

<p align="center">
  <img src="/images/blog/inkling-day0-support/prefill-full-cuda-graph.png" width="98%" alt="CPU call-stack trace under BCG replay, showing each ShortConv site's eager execution">
</p>

<p align="center">
  <em>图 2：在 BCG 下，Inkling 的四处 ShortConv（K 流、V 流、注意力输出、MLP/MoE 输出）各自回退到真实的多层 Python/Triton 调用栈，而非单次算子启动——正是这些 eager CPU 工作让 CUDA 图出现气泡。</em>
</p>

每层都有这么多 eager 工作，再加上约 66 层，BCG 与 PCG 仍会留下真实的 CUDA 气泡——即 CPU 处理未捕获片段时 GPU 的空转时间——在小批量、中等上下文的形状下最为明显，因为此时 CPU 派发与 GPU 算子在争抢时间。

全量 CUDA 图捕获则消除了这些气泡：它把包括 ShortConv 在内的整个前向过程捕获进一张图，图的规模按请求槽位上限（`full_prefill_max_req`）设定，重放时只需刷新缓冲区内容，不必重新派发任何 Python。全图预填充吞吐量在大形状下与 BCG 大致持平，在受启动开销制约的形状下则领先 **+14–17%**。

**分片 ShortConv。** 注意力输出与 MLP 输出的 ShortConv 运行在残差流上，如果不做分片，每个张量并行 rank 都会以完整宽度冗余地计算并缓存它们。SGLang 提供了一种分片策略：先对部分和做 reduce-scatter，让每个 rank 只持有其隐藏维度分片；再针对相应分片的缓存本地执行 ShortConv；最后通过 all-gather 把结果还原到完整宽度。这样可以释放 GPU 显存，但 reduce-scatter/all-gather 的往返通信是在普通 all-reduce 之外的额外开销，在解码每步规模很小的情况下得不偿失——因此它是一项可选策略，而非默认选项。

### 相对 logits 优化

**剪切偏置（sheared-bias）算子。** 相对偏置项需要在注意力算子内部加入。Inkling 的 FlashAttention-4 集成支持两种等价做法：*score-mod* 路径，由每个注意力 tile 在其 score 回调中计算 $i - j$ 并即时查表取 $\text{rel\_logits}$；以及*剪切偏置*路径，把相对 logits 提前剪切为一个按列对齐的偏置张量，

$$
\text{sheared\_bias}(i,h,j) = \text{rel\_logits}(i,h,\,i-j)
$$

这样算子就能通过普通的 tile 加载来加上偏置，而无需对每个 score 单独索引。剪切布局更快，但需要一个 Inkling 专用的 FA4 fork，并配套一致的 tile 对齐与填充约定，Inkling 出厂采用的就是这条路径。它也是注意力堆栈中唯一一处以缓冲区身份（而非内容）作为算子调度缓存键的地方，因此任何跨调用复用该缓冲区内存的机制——包括 CUDA 图重放——都必须确保缓存被刷新，而不是被悄悄复用。

<p align="center">
  <img src="/images/blog/inkling-day0-support/fig_fa4_warp_schedule.svg" width="98%" alt="FA4 warp-specialized schedule in the MXFP8 + sheared-bias configuration">
</p>

<p align="center">
  <em>图 3：MXFP8 + 剪切偏置配置下 FA4 的 warp 专用化（warp-specialized）调度。琥珀色标注的是该 fork 的增改：与既有 Q/K/V 加载一并排布的偏置与缩放因子 tile、在线 softmax 内部的偏置加法，以及校正 warp 的 V 反量化。</em>
</p>

**双流重叠。** rel_logits 投影——即通过 $P$ 把 $r$ 变换为 `rel_logits`——只依赖融合 QKVR 投影的输出，而不依赖注意力前置算子对 K、V 所做的 ShortConv/QK-norm 工作。SGLang 把它放在与该前置算子不同的另一条 CUDA 流上运行，从而与卷积/归一化重叠执行，而非串行排在后面。

**MXFP8 支持。** 用 MXFP8 而非 bf16 存储 K/V，可让 KV 缓存容量约翻一倍，而且 Blackwell 能以高于 bf16 的吞吐量原生执行 MXFP8 矩阵乘。FA4 fork 对此做了不对称处理：Q@Kᵀ 以原生 MXFP8 MMA 执行，而 P@V 保持在 bf16 以保护精度，V 在运行中即时反量化，使这一额外步骤与既有的加载/MMA 调度重叠，而不必单独多跑一遍。把 MXFP8 量化直接融合进同一个注意力前置算子，而不是单独的量化再存储步骤，可将代价控制在约 4.7–4.8 µs——与 bf16 基线相差约 14% 以内——同时保有 KV 缓存的内存收益。

### 共享专家 sink 优化

**Top-k。** 上文描述的共享 sink MoE 门控，是 sigmoid + 带偏置的 top-k 选择，再对选中的路由专家与共享专家得分做联合 logsigmoid 重归一化——若不融合，这条链路要串起 sigmoid+偏置算子、top-k 算子和重归一化算子。一个融合的 Triton 算子把整条链收进单次执行，在现实 token 规模下比未融合链路快 1.6–5.6×；针对特定形状的 CUDA-JIT 版本更进一步，例如 **T=4096 时 7.72 µs 对链路的 26.15 µs**（3.4×），**T=16384 时 20.09 µs 对 52.88 µs**（2.6×）。

**共享专家融合。** 共享 sink 的数学形式（路由与共享得分共用一次归一化）意味着共享专家作为一个完整的张量并行稠密块运行。每个 token 都会经过每个共享专家，因此把专家轴保留为批维度只会带来额外工作：直接实现会复制输入、在专家轴上运行批量 GEMM、为每个专家物化一份输出，再把这些输出求和。

我们改为把专家轴折叠进矩阵维度。gate/up 权重沿输出维度堆叠，而 down 权重沿输入（归约）维度拼接。我们把得到的二维权重表示称为**线性化布局（linearized layout）**：「线性化」指把专家维度折叠进两个稠密 GEMM；两者之间的 SwiGLU 仍保持非线性。其 down GEMM 在自身的归约过程中顺便完成专家求和，从而省去了输入复制、按专家的中间结果以及单独的求和步骤。

<p align="center">
  <img src="/images/blog/inkling-day0-support/fig_shared_expert_fusion.svg" width="98%" alt="Shared-expert fusion: from an expert-batched implementation to a linearized GEMM layout">
</p>

<p align="center">
  <em>图 4：共享专家融合把按专家分批的实现转换为线性化布局：gate/up 权重堆叠为一个稠密 GEMM，down 权重拼接为第二个稠密 GEMM，由第二个 GEMM 的归约完成专家求和。</em>
</p>

在 B200 W4A16 推理服务中，专家融合在 BS1–32 范围内将输入吞吐量提升 5.8–11.1%，将 TTFT（首 token 延迟）降低 5.5–10.0%。H200 输入吞吐量提升 2.2–4.5%，解码吞吐量保持稳定。

## 特性支持

### 基于 Multi-layer Eagle 的投机解码

Inkling 自带八个串联的 MTP（多 token 预测，multi-token-prediction）层用于投机解码——不是同一个草稿头重放八次，而是八个各自持有权重的层，每个草稿深度一层，每层消费上一层的输出。它们共同构成一种 EAGLE 式的递推：目标模型一次前向产生一个隐藏状态，草稿链把它向深处延伸八个 token，然后目标模型在单次前向中同时验证全部九个位置。草稿层共享目标模型的 embedding 与 unembedding——SGLang 让所有草稿层引用同一份副本。

<p align="center">
  <img src="/images/blog/inkling-day0-support/fig_mtp_chain.svg" width="98%" alt="One decode round of Inkling's multi-layer MTP">
</p>

<p align="center">
  <em>图 5：Inkling 多层 MTP 的一轮解码。目标模型的隐藏状态与根 token 引导出一条八层草稿链，整体捕获在单张 CUDA 图中；九个位置的块再交回目标模型做一次验证前向。</em>
</p>

**整条链一张 CUDA 图。** 基线设计是每个草稿步重放一张图，步与步之间靠 Python 采样 token、把它轮转成下一步的输入并重建注意力元数据——每轮要做八次图启动、留下七次主机间隙。SGLang 则按批次大小把整条链捕获进单张 CUDA 图：全部八个草稿前向、token 轮转、每步的注意力元数据以及采样本身，首尾相接地录制，中间没有 Python。这之所以可行，是因为链条在各步之间形状不变，且采样是图安全的（graph-safe），每次重放都会抽取新的随机数；草稿窗口宽度固定，接受 2 个 token 的请求与接受 7 个 token 的请求重放的是同一张图。一个融合算子从验证输出向图喂数据，取代了主机过去在验证与草稿之间发出的约 20 次小拷贝。

**分布精确的拒绝采样。** 温度为 0 时，验证步通过与目标模型的 argmax 匹配来接受。温度大于 0 时，Inkling 推理服务支持真正的投机拒绝采样（`--speculative-use-rejection-sampling`）：以概率 $\min(1, p_k(X_k)/q_k(X_k))$ 接受草稿 token $X_k$，被拒时从残差分布中重采样，从而精确保持目标分布，而非用接受阈值去近似它。这样验证就需要每一步完整的草稿分布 $q_k$，而不只是采样出的 token——因此图化的草稿链会在运行途中把每步的概率存入一个常驻的 `[bs, 8, vocab]` 缓冲区，验证算子再按链条顺序逐个取出 token 与这份存档比对。

**无同步的解码轮。** 上述各部分被衔接在一起，让解码循环完全重叠运行：整轮之中——草稿链、验证以及它们之间的粘合逻辑——SGLang 完全不发出任何设备同步。主机始终领先于 GPU，相邻阶段的算子背靠背连流而下，流水线从不排空。

### 使用 DFlash 的投机解码

SGLang 还支持搭配 [DFlash](https://lmsys.org/blog/2026-06-15-next-generation-speculative-decoding-dflash-v2/) 的投机解码。DFlash 是一种独立的草稿架构，而非串联在目标模型上的层。DFlash 草稿作为独立模型运行，拥有自己的 KV 缓存，单次前向即可填满一整块被掩码的未来位置，而不必自回归地逐个推进；它借用目标模型的 embedding 和 LM head 而非自行训练，目标模型则以一次线性（非树形）前向验证整块内容。我们与 Modal 团队合作为 Inkling 训练了一个 DFlash 草稿模型，为 Inkling 推理服务在上述原生多层 MTP 链之外提供了第二条投机解码路径（`--speculative-algorithm DFLASH`）。

### 预填充-解码分离（PD 分离）

Inkling 有三种异构状态类型：全注意力 KV、滑窗 KV，以及 ShortConv 卷积状态。三者都需要从预填充节点传输到解码节点。三组件内存池本就是为混合 SSM-注意力模型而建的，Inkling 的卷积状态可以直接套用同一套基础设施，因此分离部署路径上不需要新增传输逻辑。SGLang 的 `UnifiedRadixCache` 是对所有状态类型的统一抽象；分离部署层、HiCache 与投机解码都通过这同一个接口在三种组件之上组合。

### AMD GPU 支持

通过在 Triton 注意力后端中新增的通用 `score_mod` 接口，SGLang 支持 Inkling 运行在 AMD MI35X 上。该接口在编译时把调用方提供的 score 修改函数内联进 extend 与 decode 算子，使 Inkling 的相对位置嵌入无需依赖 NVIDIA 专有的 FlashAttention-4 路径即可在 ROCm 上工作。再配合额外的算子适配与 aiter MoE runner 集成，Inkling 可在 MI35X 上以 `--attention-backend triton --moe-runner-backend aiter` 端到端运行。

### LoRA 推理服务

对于投影 $y = Wx$，LoRA 保持基础权重 $W$ 不变，并附加一个低秩更新：

$$
y = Wx + \alpha B(Ax), \qquad r \ll d.
$$

$A$ 把 token 从模型维度压缩到秩 $r$，$B$ 再把它扩回去。Inkling 在注意力、稠密 MLP、专家和输出投影上都应用这类更新，如果每个更新都排在其基础 GEMM 之后执行，大量小型低秩运算就会变成暴露在外的延迟。

SGLang 改用双流调度：主 CUDA 流运行基础模型，LoRA 侧流为每个 token 所选的适配器计算秩为 $r$ 的部分。两条流只在需要增量（delta）的地方同步；融合的汇合（join）算子在施加周边激活的同时把增量扩展并加上。以 MLP 为例，gate/up 的低秩收缩与其基础 GEMM 重叠执行，直到两条流在下式处汇合：

$$
\operatorname{SiLU}(g + \Delta g) \odot (u + \Delta u).
$$

随后，降投影的基础路径与低秩路径继续奔向第二个汇合点。专家层复用基础模型的路由元数据，而不是对 LoRA 更新再路由一次。选择不同 LoRA 的请求保持在同一次算子启动中：一个逐 token 的适配器映射会选出相应的 $A$ 与 $B$ 因子，无需按适配器拆分批次。

<p align="center">
  <img src="/images/blog/inkling-day0-support/fig_lora_serving.svg" width="98%" alt="Inkling's two-stream LoRA serving schedule">
</p>

<p align="center">
  <em>图 5：Inkling 的双流 LoRA 调度把基础模型的 GEMM 留在主 CUDA 流上，并把所选适配器的低秩计算重叠到侧流上。融合的汇合算子在激活与输出依赖点处加上增量。</em>
</p>

即使一个批次中包含多个不同的 LoRA，结果仍接近无 LoRA 的基线。下表报告 TP8 输出吞吐量（输入 8192 / 输出 1024，开启对称内存，无投机解码）；单 LoRA 行使用 `--max-loras-per-batch 1`，4-LoRA 行使用 `--max-loras-per-batch 4`，批次中含 4 个不同的适配器：

| 配置 | 单 LoRA BS1 | 单 LoRA BS4 | 4-LoRA BS4 |
|---|---|---|---|
| B200 W4A16 TP8 | 123.20 | 383.57 | 380.17 |

在 B200 上，BS4 时从 1 个不同 LoRA 增加到 4 个，代价仅为 0.9%。

### 基数树缓存与 HiCache

在共享前缀的请求之间复用 KV 缓存，是 LLM 推理服务中最有效的优化之一，对多轮对话和长上下文负载尤其如此。SGLang 的基数树缓存（radix cache）把共享前缀组织成一棵基数树来实现这一点；HiCache 再把这棵树分层存放于多级存储（L1 GPU HBM、L2 主机 DRAM、L3 磁盘或远程存储），当工作集超出 HBM 时，被逐出的前缀可以从更便宜的层级重新加载，而不必重新计算。Inkling 让这两者都变得复杂，因为它并不提供前缀缓存所假设的那种单一同构的注意力 KV 池。它的大多数层使用滑窗注意力（SWA），其 ShortConv 分支则为每个请求保存一份小的卷积状态，SGLang 把它存放在为循环 Mamba/SSM 层构建的池中——尽管 Inkling 并没有 SSM。SGLang 为每种状态轴设有独立的基数树缓存：全注意力的 `RadixCache`、处理滑窗逐出的 `SWARadixCache`，以及管理循环状态的 `MambaRadixCache`。一个同时涉及多个状态轴的混合模型，需要把它们协调在同一棵树上——SGLang 的 `UnifiedRadixCache`（[#20415](https://github.com/sgl-project/sglang/issues/20415)）以单一树统一管理带类型的组件（`FULL`、`SWA`、`MAMBA`），并在其上原生支持 HiCache，而不必为每种变体分别重新实现。

Inkling 直接接入这条路径。它注册一个三组件内存池，统一缓存为其选择一种 SWA + Mamba 组合栈策略：在单一缓存控制器之下，为全部三个组件（全量 KV、SWA KV 和卷积状态池）构建一个主机端栈。由于这一集成是统一缓存的原生能力而非专用旁路，Inkling 天然继承了 HiCache 的分层复用，并能与推理服务栈的其他部分（包括投机解码）组合使用。

### 多模态优化

SGLang 把图像预处理中计算密集的部分（patch 切分、归一化和内容哈希）卸载到一个原生 Rust 扩展中，该扩展在服务进程内无 GIL 运行。这使得多图像并行成为可能，并把哈希计算移出调度器热路径，在图像密集负载下将 TTFT 降低 14-44%，推理服务吞吐量提升约 20%。该扩展围绕可扩展的处理器接口构建，目前支持 Inkling。

## 性能结果

我们在一个 B200 节点上对 Inkling 做端到端基准测试，在固定的序列形状（输入长度 8192、输出长度 1024）下分别于 TP=4 和 TP=8 扫描批次大小，全程开启对称内存与 CUDA 图。

<p align="center">
  <img src="/images/blog/inkling-day0-support/fig_performance_pareto.png" width="98%" alt="Inkling serving performance on B200: throughput-interactivity Pareto curve for TP=4 vs TP=8, and ITL bar comparison across batch sizes">
</p>

<p align="center">
  <em>图 7：ISL=8192/OSL=1024 下 Inkling 在 B200 上的推理服务性能。左：每 GPU 吞吐量与交互性（interactivity）的对比，随批次大小扫描。右：相同批次大小下的每 token 生成时间（ITL）。</em>
</p>

左图描绘了两种张量并行规模下的吞吐量-交互性 Pareto 前沿：沿任一条曲线移动，都是以单用户解码速度（交互性）换取每 GPU 的总吞吐量（每 GPU 每秒服务的输入加输出 token 总数），方式是接纳更多并发请求。在 TP=8 下，批次大小 1 时达到 171.0 tok/s/user，批次大小 32 时达到 71.7k tok/s 的总输入吞吐量。右图显示，在两种张量并行规模下，每 token 生成时间（ITL）直到批次大小 8 都保持在个位数毫秒，直到批次大小进入 30 及以上才攀升到几十毫秒。

## 基于 Miles 的强化学习

Miles 通过一个覆盖 DP/PP/TP/SP/EP/CP、支持全参数与 LoRA 优化的 Megatron 后端，为 Inkling 提供 Day-0 强化学习（RL）支持。为保持训练-推理一致性，该后端将定制的相对注意力、ShortConv 与 FP32 MoE 算子，与 rollout 路由重放相结合——后者在文本序列和经媒体扩展后的序列上重放共享 sink MoE 的路由决策。在此基础之上，原生 LoRA 覆盖 Inkling 的注意力、稠密 MLP/MoE 与 LM head 投影，并只需同步适配器；多模态流水线支持图像与音频输入。我们用 975B 全参数 GRPO、文本 LoRA 与视觉语言 LoRA 验证了完整的 RL 流水线。

完整的 Inkling RL 实现见 [Miles pull request #1683](https://github.com/radixark/miles/pull/1683)。开箱即用的 Inkling 镜像可通过 `docker pull radixark/miles:inkling` 获取。

### 支持 DP/PP/TP/SP/EP/CP 的 RL 训练后端

Miles 把 Inkling 实现为原生 Megatron 模型。该后端将 Inkling 的局部与全局相对注意力、四条残差短卷积路径、稠密层与 MoE 层的排布、共享 sink 路由器与专家，以及图像与音频编码器，重建为可微分的 Megatron 模块。它支持 Inkling 训练配方用到的全部六个并行维度：

- **DP。** 在多个副本间分发微批次并同步梯度。
- **PP。** 将 transformer 层划分到各流水线阶段。
- **TP。** 对融合的 $q$/$k$/$v$/$r$ 及输出投影做分片，$k$/$v$ ShortConv 与本地注意力头对齐。
- **SP。** 对残差 ShortConv 路径做分片，同时保持因果上下文。
- **EP。** 对路由专家及其可训练状态做划分。
- **CP。** 采用连续 all-gather：$q$ 与 $r$ 留在本地，$k$ 与 $v$ 则带全局偏移收集以支持相对注意力。ShortConv 收集完整序列，再把各 rank 的本地切片返回。

一个 Inkling 模型桥接器负责双向的 checkpoint 转换：它把发布的 Hugging Face 权重切分用于 Megatron 训练，再重建 checkpoint 导出与 rollout 权重更新所需的布局。同一后端同时驱动全参数与 LoRA 两种 RL。

### 全参数 RL

基于上述原生 Inkling 后端与并行体系，Miles 通过更新模型的每一个张量来运行全参数 GRPO。每轮迭代中，SGLang rollout worker 生成轨迹并记录 R3 所需的路由专家 ID；Miles 训练 rank 消费这些轨迹、重放路由决策，并施加全模型更新。模型桥接器再把更新后的分布式分片转换成 SGLang 的张量布局，以有界的桶为单位把下一版策略流回，供下一轮 rollout 使用。

在单个 GB300 机架有限的 GPU 显存内，完整策略、梯度与 FP32 优化器状态会带来额外的内存压力。为此，Miles 在有界的 GPU 工作集与节点本地 NVMe 之间流转 Megatron DistributedOptimizer 状态。这种 GPU-磁盘卸载只是改变了存储位置，并不改变优化器更新本身（[miles#1575](https://github.com/radixark/miles/pull/1575)、[torch_memory_saver#80](https://github.com/fzyzcjy/torch_memory_saver/pull/80)、[Megatron-LM#63](https://github.com/radixark/Megatron-LM/pull/63)）。

我们在 12 个节点（每节点 4 块 GB300 GPU）上运行 Inkling 975B 全参数 GRPO。训练采用 DP2/PP3/TP4/EP8，rollout 采用 TP8/EP16。运行使用全局批次大小 32、GRPO 组大小 8，最大响应长度为 4K（带截断）。运行开启路由重放，优化器使用 Adam，学习率为 $10^{-6}$。我们在 DAPO-Math-17K 上训练，在 AIME25 上评估。训练-rollout KL 保持在 $10^{-3}$ 左右，原始奖励与 AIME25 评估均稳步提升。

<div align="center">
  <img src="/images/blog/inkling-day0-support/full-para-kl.png" width="50%" alt="Train-rollout KL during full-parameter RL">
  <br><br>
  <img src="/images/blog/inkling-day0-support/full-para-reward.png" width="50%" alt="Raw reward during full-parameter RL">
  <br><br>
  <img src="/images/blog/inkling-day0-support/full-para-eval.png" width="50%" alt="AIME25 evaluation during full-parameter RL">
</div>

<p align="center">
  <em>图 8：Inkling 975B 全参数 GRPO：训练-rollout KL 保持在 10⁻³ 左右，原始奖励与 AIME25 评估均稳步提升。</em>
</p>

### 面向训练-推理一致性的定制高效算子

训练-推理一致性是 RL 中的一项核心正确性要求：训练器必须评估的，正是生成 rollout 的那个策略，尽管训练与推理服务跑在两套不同的分布式执行栈上。维持这种一致性并不容易，因为只要算子、累加精度、打包序列边界或归约顺序存在差异，同一个 checkpoint 就可能产生不同的 token 概率。Miles 在定义 Inkling 前向计算的那些算子上消除这种不一致，同时为分布式训练提供所需的反向实现。

**相对注意力。** 融合投影产出逐 token、逐头的特征 $q_{i,h}$、$k_{i,h}$、$v_{i,h}$ 与 $r_{i,h}$。Miles 采用与 SGLang 相同的固定相对投影 $P$ 和注意力 logit 定义：

  $$
  \text{rel\_logits}(i,h,d)=r_{i,h}^{\top}P_{:,d},
  \qquad
  \ell(i,j,h)=\alpha\,q_{i,h}^{\top}k_{j,h}+b(i,j,h).
  $$

  其中 $b(i,j,h)$ 按上文定义的同一因果距离规则选取 $\text{rel\_logits}(i,h,i-j)$。

  Miles 为 Inkling 提供三个训练侧注意力后端：FlexAttention、FA4 与 Transformer Engine，默认使用 FlexAttention。每次前向都先计算紧凑的相对 logits $rP$。Miles 用定制的 CUTE 算子实现相对 score 修改：在每个注意力 tile 内按相对距离索引 $rP$，并保留 SGLang 的因果或滑窗规则，而不必物化稠密的逐 token 偏置矩阵。Miles 会为每种注意力几何预先生成并缓存 score 修改器与块掩码，把构建开销摊销到反复出现的打包序列形状上。

  FlexAttention 对注意力分数和 $r_{i,h}$ 都提供可微分的前向与反向，同时 $P$ 保持冻结。在 GB300 上以 8K 打包序列、相对范围 1024 测试，它比 Transformer Engine 参考实现约快 $5\times$，峰值内存约省 $5\times$，且与其差异在 BF16 数值噪声范围内。FA4 仍可作为优化后的备选，Transformer Engine 则作为参考后端保留。

**短卷积。** Inkling 对 $k$、$v$ 流、注意力输出和 MLP 输出施加残差因果 ShortConv。Miles 用定制的 Triton 前向与反向算子实现该运算，把逐深度因果卷积与残差路径融合在一起。算子以 FP32 累加、最后加残差，先复现 SGLang 的运算顺序再转回模型 dtype。对打包序列，Miles 预先计算每个 token 所在片段的起止：前向算子屏蔽片段起点之前的左上下文读取，反向算子屏蔽片段终点之后的梯度读取，防止状态或梯度跨越样本边界。在序列并行下，Miles 先收集完整序列上下文再执行 ShortConv，然后把相应的输出与梯度分片交还给各 rank。

**FP32 MoE 激活与组合。** Inkling 的共享 sink MoE 对门控激活和加权专家归约两处的舍入都很敏感。Miles 以 FP32 执行这两个阶段。一个定制的可微分 Triton SwiGLU 算子完成激活与逐 token 的共享专家缩放，之后一次性转回模型 dtype；专家输出随后按 SGLang 的求和顺序以 FP32 累加，并在组合完成后一次性转换。这样就把训练与 rollout 之间的连续专家计算对齐了，与 R3 提供的离散路由对齐互为补充。

### 面向共享 sink MoE 的路由重放

除定制的精度对齐算子外，Rollout Routing Replay（R3）对 MoE RL 的训练-推理一致性同样重要。在 top-$k$ 边界附近的一个微小数值扰动就可能改变被选中的专家，进而改变计算图本身。SGLang 在 rollout 期间记录路由 top-$k$ 专家 ID，Miles 在训练前向中复用这些 ID。

对 token $t$，设 $e_1,\ldots,e_k$ 为重放的路由专家。Miles 重新计算它们当前的路由分数，并把它们放在所有常开共享专家的分数之前：

$$
s_t=\left[
\sigma(\ell^r_{t,e_1}),\ldots,\sigma(\ell^r_{t,e_k}),
\sigma(\ell^s_{t,1}),\ldots,\sigma(\ell^s_{t,N_s})
\right].
$$

随后所有条目共用一次归一化：

$$
w_{t,m}=c\frac{s_{t,m}}{\sum_n s_{t,n}}.
$$

前 $k$ 个权重属于重放的路由专家，其余 $N_s$ 个权重属于共享专家。其中 $c$ 合并了 Inkling 配置的路由缩放与可学习的全局缩放。R3 只重放专家 ID；连续权重由 Miles 从当前路由器重新计算，因此梯度仍能流经路由权重与共享权重两者。实现中对 log-sigmoid 分数取 softmax 以保证数值稳定。在专家子图对齐之后，剩余的概率漂移由截断重要性采样处理。

第二项 Inkling 专属适配是多模态索引。SGLang 记录路由时，序列已经因图像 patch 和音频特征扩展过 prompt，因此 Miles 使用引擎报告的扩展后长度，而非原始文本 token 数。随后，该轨迹按与训练批次相同的打包序列和序列并行布局做填充与切片，再注册到每个 MoE 层。

### Inkling 中的 LoRA 实现

Inkling 发布的 LoRA schema 覆盖注意力、稠密 MLP、MoE 与 LM head 投影。Miles 在 Megatron 中原生实现了同样的结构，包括感知 TP/EP 的执行和直接导出到 SGLang，因此 RL 只更新适配器，基础模型保持冻结。

对每个被适配的线性层，基础权重 $W$ 保持冻结，Miles 只训练低秩因子 $A$ 与 $B$：

$$
y=Wx+\frac{\alpha}{r}B(Ax).
$$

Inkling 特有的挑战在于，如何在其异构的注意力、稠密与专家投影上高效应用这一标准更新。

Inkling 的路由专家采用共享外积（shared-outer）分解，而不是为每个专家独立配置一对因子。对 $w_1$ 和 $w_3$，$A$ 在各专家间共享，而各专家专属的 $B$ 张量按 EP 分片；对 $w_2$，各专家专属的 $A$ 张量做分片，$B$ 则共享。

设 $\mathcal C$ 为所有被适配投影的索引。它们的低秩因子构成可训练的适配器状态

$$
\Phi_t = (A_{\ell,t}, B_{\ell,t})_{\ell\in\mathcal C}.
$$

以 $\Theta_0$ 表示冻结的基础模型，则第 $t$ 轮迭代的策略为

$$
\pi_t(\cdot\mid x)=\pi(\cdot\mid x;\Theta_0,\Phi_t).
$$

GRPO 在 $\Theta_0$ 不变的情况下把 $\Phi_t$ 更新为 $\Phi_{t+1}$。在下一轮 rollout 开始前，Miles 只同步 $\Phi_{t+1}$；基础权重在两个运行时中保持常驻。

### 端到端 LoRA RL 与仅适配器同步

图 9 展示了一轮完整的 LoRA RL 迭代。沿上方路径，SGLang 返回采样 token、rollout 的 log 概率、奖励与掩码，以及 R3 所需的路由专家 ID。Miles 对同一 token 序列求值，在每个路由器处注入记录的专家 ID，并只对适配器求导。在 MoE 层，低秩分支直接消费已分发好的专家-token 缓冲区，复用基础模型的专家分组，而不是对 LoRA 更新再单独路由一次。专家专属因子按 EP 分片，共享外层因子则被复制，其梯度在 EP 组内归约。

<div align="center">
  <img src="/images/blog/inkling-day0-support/moonrise_rl_lora.jpg" width="80%" alt="Bidirectional LoRA RL contract. SGLang sends rollout data to Miles; Miles updates and exports the adapter tensors back to SGLang.">
</div>

<p align="center">
  <em>图 9：共置（colocated）LoRA RL：SGLang 把 rollout 轨迹发给 Miles，Miles 只回传更新后的适配器，并让冻结的基础模型保持常驻。</em>
</p>

优化器更新之后，Miles 直接从分布式训练状态物化出可直接用于推理服务的适配器。导出器不是对每个张量各发一次集合通信，而是把所需的 TP 与 EP 碎片打包，对每个并行组执行一次扁平的 all-gather。随后重建 Inkling 的 SGLang 布局：融合投影的分片按服务顺序拆分并拼接，专家张量恢复为专家主序（expert-major）排列，LM head 的填充行被移除。最终得到一组连续的 BF16 张量，其名称与形状与 SGLang 消费的完全一致。

下方路径执行版本切换，无需把适配器数据经由主机内存中转。Miles 暂停生成、清空引擎缓存，把命名的 GPU 张量序列化为 CUDA IPC 句柄，并把每份数据发送给共享同一 GPU 的共置 SGLang worker。SGLang 卸载旧适配器，然后在单次调用中加载完整的新版本，并在生成恢复前把它切分到服务布局。冻结的基础模型要么在 rollout 侧保持常驻，要么在迭代式适配器更新开始前同步一次；后续步骤只传输适配器。已发布的 safetensors 格式 Inkling 适配器支持热启动，而原生按 rank 保存的适配器 checkpoint 保留了优化器与调度器状态，可精确恢复训练。

采用与全参数运行相同的实验设置，LoRA GRPO 的训练-rollout KL 保持在 $10^{-3}$ 量级，原始奖励在约 450 步内稳步提升。仅适配器同步把权重更新延迟从 49.4 秒降到 2.5 秒，提速 $20\times$；将反向传播与优化器工作限制在适配器上，则把每步训练时间降到全参数训练的 85%。

<p align="center">
  <img src="/images/blog/inkling-day0-support/lora-text-reward.png" width="48%" alt="Raw reward during LoRA RL">
</p>

<p align="center">
  <em>图 10：文本 LoRA GRPO：原始奖励在约 450 步内持续提升。</em>
</p>

### 基于扩展对齐路由重放的多模态 LoRA RL

Inkling 是 Thinking Machines Lab 发布的强大多模态模型，原生支持文本、图像和音频输入。Miles 把 RL 后端扩展到这些模态：全参数与 LoRA 配方都可接受结构化多模态 rollout，在 Megatron 中执行 Inkling 的视觉与音频塔，并在媒体扩展后的序列上保持路由重放。

图 11 展示了核心的数据变换。Miles 一直保留原始的结构化消息列表，直到 Inkling 专属渲染器输出模型的角色与内容标记，并为每个图像或音频项精确输出一个 sentinel。处理器校验 sentinel 数量与所提供的媒体一致，然后为每项记录 $p$ 个图像 patch 或 $f$ 个音频 d-mel 帧。训练之前，Miles 把一个图像 sentinel 替换为 $p$ 个词表内占位位置、一个音频 sentinel 替换为 $f$ 个位置，同时记录样本内的位置，即相应媒体嵌入必须插入的位置。

<div align="center">
  <img src="/images/blog/inkling-day0-support/moonrise_rl_mm.jpg" width="80%" alt="Image and audio sentinels expand into vision-patch and audio-frame positions, with R3 expert IDs indexed over the expanded sequence.">
</div>

<p align="center">
  <em>图 11：每个媒体 sentinel 展开为图像 patch 或音频帧所占据的模型位置，R3 路由轨迹则在扩展后的序列上建立索引。</em>
</p>

SGLang 在这次扩展之后才做 MoE 路由决策，因此 R3 轨迹包含扩展后每个位置的专家 ID，而不只是渲染后的文本序列。Miles 用文本长度加上记录的媒体扩展量来校验轨迹长度，在打包之前扩展 token 序列，并按训练 token 所用的相同布局对 R3 做填充与切片。由于媒体 sentinel 出现在 prompt 中，响应的 log 概率与损失掩码保持不变。分批时，记录的样本内媒体位置被平移进打包后的全局序列；Megatron 视觉塔与音频塔编码 patch 与 d-mel 张量，并把它们的嵌入散射（scatter）到这些位置上。在序列并行下，每个 rank 选取落在其本地序列分片内的位置。

在多模态 LoRA RL 中，当前的生产配方将视觉塔与音频塔保持冻结，围绕它们的嵌入训练语言模型的适配器或基础模型。训练媒体塔作为实验选项提供。

为验证多模态 RL 配方，我们在 Geo3K 上选择一个视觉+文本设定，把数据集划分为训练与评估子集，并使并行配置与优化超参数与前述 LoRA 实验完全一致。该运行在视觉数学题上检验了同样的 LoRA 执行、路由重放与适配器同步。Geo3K 评估从约 0.54 升至 0.58，整个训练过程中训练-rollout KL 保持在 $10^{-3}$ 量级。同一多模态路径也支持音频输入、全参数训练与分布式执行。

<p align="center">
  <img src="/images/blog/inkling-day0-support/lora-vision-eval.png" width="48%" alt="Geo3K evaluation during vision LoRA RL">
</p>

<p align="center">
  <em>图 12：视觉 LoRA GRPO：Geo3K 评估随训练步数提升。</em>
</p>

## 致谢

本工作由 SGLang & Miles 团队与 Thinking Machines Lab 合作完成。

**SGLang & Miles 团队**：Ke Bao, Cheng Wan, Chunan Zeng, Zhichen Zeng, Yanbin Jiang, Yuhao Yang, Qiaolin Yu, Mao Cheng, Yi Sun, Mingyi Lu, Haoguang Cai, Banghua Zhu, Ying Sheng

**Thinking Machines Lab**：Aurick Qiao, Paul Zhang, Shenxiu Liu

感谢 Modal 团队与我们合作，为 Inkling 训练了 DFlash 草稿模型。
