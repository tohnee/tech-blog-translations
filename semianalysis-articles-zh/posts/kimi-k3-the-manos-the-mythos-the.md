---
title: "Kimi K3：其人、其神话、其传奇"
title_en: "Kimi K3, The Manos, The Mythos, The Legendos"
subtitle: "Kimi K3 的架构：压缩记忆、跨深度注意力、潜空间专家路由与服务性能"
date: 2026-08-03
source: https://newsletter.semianalysis.com/p/kimi-k3-the-manos-the-mythos-the
crawled: 2026-09-15
authors: ["Kimbo Chen", "Shubham Choudhari", "Bryan Shan", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Kimi K3：其人、其神话、其传奇

> 原文：[Kimi K3, The Manos, The Mythos, The Legendos](https://newsletter.semianalysis.com/p/kimi-k3-the-manos-the-mythos-the) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Kimi K3 的架构：压缩记忆、跨深度注意力、潜空间专家路由与服务性能**

Kimi K3 一经发布便横扫各大排行榜，确立了自己作为开放前沿模型的地位，掀起了一场风暴。社区迫切想理解 Kimi K3 的工作原理，而其性能背后的非常规技术让许多人感到意外。本文是理解 Kimi K3 模型架构核心技术的入门指南。

# Kimi Delta Attention

Kimi Delta Attention（KDA）是 Kimi K3 混合注意力机制中的线性注意力层。我们将追溯 KDA 的起源：从线性注意力（linear attention）、DeltaNet、Gated DeltaNet（GDN），一路到 KDA。

## 线性注意力（Linear Attention）

线性注意力的推导源自**移除标准 softmax 注意力中的 softmax 操作**。下面我们对比迭代推理公式，它们展示了在 token 位置 t 处输出向量的计算：

![](https://substack-post-media.s3.amazonaws.com/public/images/73a632f4-14a0-4e77-a79c-ce3c768e6862_632x427.png)
*来源：DeltaNet Explained (Part I)*

移除 softmax 操作后，我们可以重排运算顺序，把注意力的计算复杂度从二次降为线性：

![](https://substack-post-media.s3.amazonaws.com/public/images/1a57a950-d9ad-4821-b2b6-18fed3b3b61a_459x692.png)
*来源：Linear Attention and Beyond（与 Songlin Yang 的互动教程）*

新方程如下：

![](https://substack-post-media.s3.amazonaws.com/public/images/0987f5cb-9c34-4591-87a5-ae67ca6eb10b_439x121.png)
*来源：Linear Attention and Beyond（与 Songlin Yang 的互动教程）*

向量 q、k、v 的维度为 *L* × *d*。两个方程的计算复杂度均为 O(*Ld*²)，因此计算是线性的。把新方程与 softmax 注意力的方程对比可见：**softmax 注意力需要访问所有过去的 key 和 value 向量**，而**线性注意力把所有过去的 key 和 value 向量压缩进一个隐藏状态 S**。

我们可以把新方程重新解读为一个**在线学习目标**。把矩阵 S 视为存储 key 向量 k 与 value 向量 v 之间关联的联想记忆（associative memory），用 S 乘以 k 即可取出 v。于是第一个方程可解读为**在每个位置持续更新矩阵 S 以完善检索**。最后，vt @ kt.T 项可解读为损失函数 -(S @ kt.T) @ vt 对 S 的梯度。

## DeltaNet

在在线学习目标的视角下，矩阵 S 的取值会无界增长：随着序列变长，新旧信息在 S 中混作一团，破坏训练稳定性。没有 softmax 提供尺度良好且有界的输出，线性注意力在长程召回任务上通常落后于 softmax 注意力。

DeltaNet 对线性注意力的改进在于**把损失函数改为最小化 value 检索的 L2 范数**。与线性注意力的损失函数不同，DeltaNet 的损失函数会约束 S 的增长。由此得到一条新的矩阵 S 更新规则，即 Delta 规则（Delta Rule），如下：

来源：[Linear Attention and Beyond（与 Songlin Yang 的互动教程）](https://www.youtube.com/watch?v=d0HJvGSWw8A)

Delta 规则成为 DeltaNet 注意力方程的基础：

从概念上讲，Sₜ-1 @ kₜ - vₜ 表示与当前 key 和 value 无关的关联，DeltaNet 会对这些关联执行定向移除。

## Gated DeltaNet

GDN 和 KDA 都是 DeltaNet 的变体。Gated DeltaNet 在矩阵 S 上施加 LSTM 遗忘门 *alpha*，使模型能够通过权重衰减控制记忆寿命。KDA 进一步把 *alpha* 扩展为对角矩阵，实现细粒度的逐通道记忆衰减和位置感知。

![](https://substack-post-media.s3.amazonaws.com/public/images/fbf7f177-b0a4-4c28-b958-de5b04fa57a9_866x129.png)
*来源：Kimi Linear*

感谢阅读 SemiAnalysis！本文为公开文章，欢迎分享。

[分享](https://newsletter.semianalysis.com/p/kimi-k3-the-manos-the-mythos-the?utm_source=substack&utm_medium=email&utm_content=share&action=share)

## FlashKDA 算法

Moonshot 为 KDA 开发了自定义 kernel——FlashKDA，并已[开源](https://github.com/MoonshotAI/FlashKDA/tree/master)。本节解释其算法并推导算术强度（arithmetic intensity）。

### 算法

首先，从递推公式的一种等价形式出发：

```
u_t = beta_t * (v_t - (D_t @ S_t-1).T @ k_t)
S_t = D_t @ S_t-1 + k_t @ u_t.T
o_t.T = q_t.T @ S_t
```

其中 D_t 是 alpha 遗忘门的对角矩阵，u_t 是 delta 规则中的 delta。解码（decode）时，kernel 基本按此公式执行。预填充（prefill）时，我们按 token 块（chunk）展开递推公式来并行化操作，以便在 GPU 上高效执行。假设展开 token i 到 j，起始状态为 S_i-1，得到：

```
S_j = D_j:i @ S_i-1 + sum(D_j:t+1 @ k_t @ u_t.T, t=i:j)
o_j.T = q_j.T @ S_j
      = q_j.T @ D_j:i @ S_i-1 + sum(q_j.T @ D_j:t+1 @ k_t @ u_t.T, t=i:j)
```

D_j:i 指从 token i 到 j 的累积衰减：D_j @ D_j-1 @ D_j-2 @ … @ D_i。写成 FlashKDA 的矩阵形式，公式变为：

```
S_out = D_j:i @ S_in + K_restore.T @ U
M_qk = tril(Q_decay @ K_inv.T)
O = Q_decay @ S_in + M_qk @ U
```

向量到矩阵的映射关系如下：

- S_in 指一个 chunk 起始位置的状态
- S_out 指一个 chunk 结束位置的状态
- K_restore 是 D_j:t+1 @ k_t 的矩阵形式
- Q_decay 是 q_j.T @ D_j:i 的矩阵形式
- Q_decay @ K_inv.T 是 q_j.T @ D_j:t+1 @ k_t 的矩阵形式，由 (q_j.T @ D_j:i) @ (D_t:i^-1 @ k_t) 推导而来
- M_qk 是因果掩码，因此是一个下三角矩阵

U 是展开后的 u_t 的矩阵形式。为计算 U，我们应用 UT 变换并计算以下内容：

```
B = Diag(beta) @ (V - K_decay @ S_in)
L = StrictTril(Diag(beta) @ K_decay @ K_inv.T)
U = (I + L)^-1 @ B
```

完整推导请参阅 [Songlin Yang 的博客文章](https://sustcsonglin.github.io/blog/2024/deltanet-2/)和 [Kimi Linear 论文 3.1 节](https://arxiv.org/abs/2510.26692)。注意这里的 U 对应 Kimi Linear 论文中的伪 value（pseudo-value）项。

在实现上，FlashKDA 启动两个 kernel：K1 和 K2。K1 并行准备 chunk 级张量，包括：

```
a = exp2(cumsum(g))
K_decay = Diag(a) @ K
Q_decay = Diag(a) @ Q
K_inv = Diag(a)^-1 @ K
K_restore = a[-1] * K_inv
L = StrictTril(Diag(beta) @ K_decay @ K_inv.T); INV = (I + L)^-1
M_qk = tril(Q_decay @ K_inv.T)
```

其中 `a` 是累积衰减，每个元素是某个 token 位置处的累积衰减。

K2 执行 chunk 级循环计算：

```
U = INV @ Diag(beta) @ (V - K_decay @ S)
O = Q_decay @ S + M_qk @ U
S = Diag(a[-1]) @ S + K_restore.T @ U
```

### 复杂度分析

这里我们分析单个注意力头的复杂度。解码时，关键路径计算为：

- D_t @ S_t-1：逐元素乘法，D × D
- S_t-1.T @ k_t：D × D × 1
- k_t @ u_t.T：D × 1 × D
- q_t.T @ S_t：1 D × D

解码 kernel 大约执行 7*D² FLOPs。

FP32 循环状态的读写主导了内存流量，因此内存流量约为 8*D² 字节。

预填充时，K1 的关键路径在计算 L、INV 和 M_qk。

- L：C × D × C
- INV：[Neumann 分解](https://github.com/MoonshotAI/FlashKDA/blob/1ce47ea3bb22c84eb9cc665028399cf35e8ffb0b/csrc/smxx/utils.cuh#L190)，执行 6 次 C × C × C 矩阵乘法
- M_qk：C × D × C

对于 K2：

- K_decay @ S：C × D × D
- Q_decay @ S：C × D × D
- M_qk @ U：C × C × D
- INV @ B：C × C × D
- K_restore.T @ U：D × C × D

K1 与 K2 合计，FlashKDA 执行 12*C^3 + 8*C²*D + 6*C*D² FLOPs。由于我们是在 chunk 级别（chunk 大小为 C）分析的，假设序列长度 T >> C，总 FLOPs 为 T/C * O(C*D²) = O(T*D²)。

内存流量方面：

- K1 读 Q、K、g：C × D
- K1 写、K2 读 Q_decay、K_decay、K_restore：C × D
- K1 写、K2 读 INV、M_qk：C × C
- K2 读 V、写 O：C × D
- K2 每个 kernel 读写 S 一次：D × D

总计，FlashKDA 访问 3 * 2*C*D + 2 * (3 * 2*C*D + 2 * 2*C*C) + 2 * 2*C*D = 8*C² + 22*C*D 字节。在 kernel 层面，访问量为 T/C * (8*C² + 22*C*D) + 8*D² ~ O(TC + TD + D²)。

这具体说明了 KDA 的计算复杂度：

- 预填充：计算与内存均随序列长度线性增长
- 解码：计算与内存均与序列长度无关（恒定）

# Kimi Linear

Moonshot 训练 Kimi Linear 系列模型作为其 KDA 设计的概念验证，因此我们可以从 Kimi Linear 推断 Kimi K3 的架构设计。对比 K3 发布技术博客与 Kimi Linear 可以看到，Kimi K3 沿用了相同的共享专家数量、混合线性注意力比例以及大体一致的注意力模块设计。

![](https://substack-post-media.s3.amazonaws.com/public/images/e7d326f1-65b9-47da-9fff-eebe83dadfc3_786x403.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/7308e58c-da14-4949-b093-0474f2b458b0_1554x1380.png)
*来源：Kimi K3 技术博客*

上图展示了作用在 KDA 输入上的操作。对 query、key 和 value，我们施加线性变换和短卷积（short convolution）。短卷积能有效捕捉局部 token 依赖，采用左填充卷积可避免破坏因果性。我们还对 query 和 key 施加 L2 归一化，以稳定转移矩阵和输出矩阵的特征向量。衰减记忆门方面，alpha 是低秩投影，beta 是降维投影。KDA 输出逐头归一化，并受输出遗忘门控制——在 K3 中实现为线性变换，而 Kimi Linear 中是低秩投影。最后，我们用一个线性层混合各头的信息。

Kimi Linear 将 KDA 与全注意力 Multi-head Latent Attention（MLA）交错排列。Kimi Linear 表明，3:1 是平衡性能与效率的理想 KDA:MLA 比例。KDA 还是强大的位置感知算子，取代了 MLA 中的 RoPE。

Moonshot 让 MLA 层保持全注意力，这与此前使用 MLA 的实验室不同：智谱（Zhipu）现在采用 DeepSeek Sparse Attention（DSA），DeepSeek 则进一步把 DSA 演进为 Compressed Sparse Attention 和 Heavily Compressed Attention。Moonshot 最著名的研究者之一 Jianlin [给出了两点理由](https://kexue.fm/archives/11848)：他们还没找到更好的注意力设计，而且不想一次性做太多模型架构改动。**MLA 不适合智能体工作负载**，下文解释原因。

## Multi-head Latent Attention（MLA）

MLA 在预填充和解码时执行不同的操作。**[DeepSeek V3.2 论文](https://arxiv.org/abs/2512.02556)定义了 MLA 的两种模式：多头注意力（MHA）模式和多查询注意力（MQA）模式。**为简单起见，这里省略 RoPE 维度，并以 DeepSeek V3 配置为例。

### 多头注意力（MHA）模式

![](https://substack-post-media.s3.amazonaws.com/public/images/8a1b150c-8878-4941-81c5-85dcb76d0a36_4720x2477.png)
*来源：SemiAnalysis*

MHA 模式是 MLA 在预填充阶段的默认模式。在 MHA 模式下：

- 对隐藏状态 `h_t` 做低秩投影，生成 query `q`
- 对 `h_t` 做降维投影，生成 kv 条目 `kv`
- 对 `kv` 分别做升维投影，生成多头的 key `k` 和 value `v`
- 经过缩放点积注意力（SDPA）后，输出 `o` 的各头经线性投影得到注意力输出 `out`

MHA 模式与 MQA 模式之间的关键联系在于用什么充当 KV 缓存。我们把 KV 条目 `kv` 而非 key 和 value 保存为解码用的 KV 缓存。**通过保存 KV 条目，我们把每 token 的内存占用降低了 42.67 倍。**

### 多查询注意力（MQA）模式

![](https://substack-post-media.s3.amazonaws.com/public/images/c01b192a-72e4-4853-b902-de6f9862d37c_6437x2912.png)
*来源：SemiAnalysis*

MQA 模式是 MLA 在解码阶段的默认模式。为避免重新物化完整 KV 缓存，我们重排注意力周围的运算顺序，推导如下：

![](https://substack-post-media.s3.amazonaws.com/public/images/57b3dbf7-be00-4b0b-91ce-429b437dc3d2_617x304.jpeg)

重排后，差异如下：

- query 与 key 升维投影矩阵 `W_UK` 的转置相乘
- 在 SDPA 中，key 和 value 均使用 KV 条目（记作 `C`）
- 在 SDPA 之后施加 `W_UV`

如图所示，query 是多头的，而 KV 条目是单头的。这实际上就是多查询注意力，名字由此而来。

### FLOP 对比

比较 MHA 与 MQA 模式的 FLOPs：首先可以消去 query 低秩投影和输出线性投影。然后可以观察到，KV 升维投影产生的 FLOPs 大致相等，无论投影施加在哪个位置。

剩下的就是 SDPA。SDPA 执行三次矩阵乘法：`(Q @ K.T) @ V`，因此 FLOP 计数为 `L * d * L + L * L * d = 2*d*L^2`。MHA 模式在标准的模型头维度 128 下计算，而 MQA 模式在潜空间维度 512 下计算。**这意味着 MQA 模式的 SDPA 大约产生 4 倍 FLOPs，总体上每 token 的 FLOPs 最多可达 MHA 模式的 3.4 倍。**

![](https://substack-post-media.s3.amazonaws.com/public/images/db8fee87-e77a-4b5d-af28-391daf3a5898_2276x1372.png)

### 追加预填充（Append-Prefill）

MLA 非常适合推理（reasoning）工作负载。推理任务通常以较短的输入序列开始，随后是大量输出 token。每个输出 token 是一步解码，MLA 降低了每 token 的 KV 缓存大小，从而降低内存带宽需求，加快解码步骤。

然而，智能体工作负载的表现不同。智能体工作负载包含工具调用，而工具调用会返回很长的输出。**这意味着模型经常处于这种情形：序列是一段长缓存输入，后接一段需要预填充的长序列。**这类工作负载被称为追加预填充（append-prefill，又称 extend、append、incremental prefill）。

![](https://substack-post-media.s3.amazonaws.com/public/images/cf636d50-799c-407c-a11b-e5c8aef2de42_6365x5040.png)

**MLA 的两种模式都不适合追加预填充。**MHA 模式不理想，因为物化完整 KV 缓存的内存开销太大；而 MQA 模式由于 3.4 倍的 FLOP 成本也不合适。正如[这条推特讨论串](https://x.com/yifanzhang_/status/2023084633534136500)所言，现代推理引擎（[vLLM](https://github.com/vllm-project/vllm/blob/d8eabdbfbe93ecc8a8d5cb8a55c5067a443a8796/vllm/model_executor/layers/attention/mla_attention.py#L121-L199)、[SGLang](https://github.com/sgl-project/sglang/pull/5113)）选择 MHA 模式，但采用分块预填充技术来避免物化整个上下文的 KV 缓存。为了解决这一智能体工作负载问题，**DeepSeek 和智谱选择把 MQA 模式适配到稀疏注意力以降低 FLOPs**。我们猜测 Moonshot 未来的模型（如 Kimi K4）将采用取代 MLA 的注意力机制。

# KV 缓存效率

我们认为**不应仅凭 KV 缓存空间复杂度来判断 KV 缓存效率**。KV 缓存大小不是孤立因素，而是模型设计的属性：没有任何开放权重模型带着静态 KV 缓存压缩技术发布，且模型架构的推理效率会影响 KV 缓存效率。KV 缓存大小的影响也因部署模型实例的总内存容量而异。例如，以宽专家并行部署模型与以张量并行部署的内存画像大不相同，这会影响留给 KV 缓存的内存容量。因此，我们建议把模型架构的系统效率与 KV 缓存大小放在一起考量来理解 KV 缓存效率，并用 **KV 吞吐**来量化。

## KV 吞吐

KV 吞吐定义为：给定特定序列长度，KV 缓存大小除以预填充时间（首 token 时间，TTFT）。KV 吞吐代表以 PD 分离方式可靠服务一个模型所需的最低带宽，同时也是理解 KV 缓存效率的良好代理指标。预填充时间浓缩了模型架构的效率，且随着序列长度增加，我们会看到内存受限与计算受限两种情形。如下表所示，混合线性注意力的优势随序列长度增加而更加显著。

![](https://substack-post-media.s3.amazonaws.com/public/images/a76fcf50-b8d1-4a79-9ea5-c82d063d8de9_969x196.png)
*来源：Prefill-as-a-Service: KVCache of Next-Generation Models Could Go Cross-Datacenter*

这也是理解集群内 KV 缓存卸载到不同内存层所需带宽的好方法。

## KV 缓存驻留

KV 缓存的存放位置遵循内存层级。首先，KV 缓存驻留在 HBM——GPU 集群中最快的内存——消耗模型权重和激活之后剩余的容量。当 KV 缓存大小超过 HBM 容量时，溢出到服务器 DRAM——容量更大但带宽更低的内存池。最后，当 KV 缓存超过 DRAM 容量时，溢出到 SSD 等磁盘存储。这类似于计算机体系结构的缓存层级：寄存器、缓存、主存、磁盘存储。

内存一致性上也延续着这一类比。流行的分布式 KV 缓存框架 Mooncake Store 支持 KV 缓存加载的写穿透（write-through）与写回（write-back）策略。Mooncake Store 的分布式 KV 缓存池让所有 worker 都能看到全部 KV 缓存。在 DRAM 与下层分布式 KV 缓存池之间实现写穿透策略，在多节点场景下有多重好处：跨节点共享前缀缓存、避免张量并行 MLA 的 KV 缓存重复，以及在节点宕机时的 KV 缓存冗余。

![](https://substack-post-media.s3.amazonaws.com/public/images/6fa02cfa-82d5-4087-86a7-008218392006_2090x1196.png)
*来源：SemiAnalysis*

## KDA 前缀缓存管理

在请求的每个 token 位置，Kimi K3 KDA 的循环状态大小固定，而标准注意力的 KV 缓存随序列长度增长。这种 KV 缓存空间的缩减是以复杂化前缀缓存为代价的，尤其是 Kimi K3 还是 KDA 与 MLA 的混合注意力。

粗略地说，现代推理引擎通过匹配现有缓存中最长的 token 前缀来识别前缀缓存命中。

![](https://substack-post-media.s3.amazonaws.com/public/images/d68abe8c-bb64-4416-8ec6-1be51e20a40f_2635x628.png)
*来源：SemiAnalysis*

识别最长前缀对 KDA 这类线性注意力成了问题。在不知道前缀边界在哪的情况下，我们将不得不在每个 token 位置缓存 KDA 的循环状态。这意味着每个 token 都有一份缓存，KV 缓存内存用量退化为随序列长度增长，与使用线性注意力的初衷背道而驰。为解决这一问题，Moonshot 以较粗的粒度保存循环状态，例如 vLLM 每 32K token 缓存一次。vLLM 还在提示词边界处额外缓存，因为对智能体工作负载而言，新的一轮通常从提示词末尾开始。

![基于区间的 KDA 缓存保留](https://substack-post-media.s3.amazonaws.com/public/images/9dbec0b8-4469-4de0-a6eb-8f902a7d2b81_1396x378.png)
*来源：Kimi K3 Is Here: Efficient Day-0 Support on vLLM*

这说明：尽管 KDA 等线性注意力大幅削减了 KV 缓存内存消耗，**但在实际服务中，它们消耗的 KV 缓存内存并非恒定**。

# 注意力残差（Attention Residuals）

## 残差连接

残差连接是让我们得以通过扩展模型深度构建更大深度神经网络的关键创新之一。神经网络越深，表达能力越强，但直接朴素地训练很难。来自浅层的信号需要保存到最后一层，梯度需要从输出层存活到第一层而不消失。

残差网络不再把整个网络建模为单一函数、只通过非线性变换传递信息，而是用恒等路径连接较小的块。每个块 fᵢ 学习对其输入 xᵢ 的改变，由如下递推式给出：

恒等映射让特征可以从浅层单元直达任意更深的单元，并为梯度提供了一条高速公路，使其不至于消失。

残差连接让我们能构建更深的网络，但也带来挑战。

浅层要影响最终输出，就会强烈地作用于残差流。因此，随着深度增加，残差流会发生不可逆的信息损失。后面的层则要提高输出增益才能作用于这条已被改变的残差流，这会破坏训练稳定性。highway network 等其他变体允许对信息流施加门控，但面临同样关键的问题：各层无法有选择地访问来自浅层的信息。

## 时间与深度上的循环

由循环神经网络主导的序列建模有着同样的递推形式。

每一步都与前一状态存在恒等映射以实现直接的信息流动，而序列模型面临同样的挑战：时间轴上的深度会稀释信号。

![](https://substack-post-media.s3.amazonaws.com/public/images/83378ab0-db07-496f-abf4-18561c9759bf_1628x1116.png)
*来源：SemiAnalysis*

Transformer 这一注意力机器通过强大而昂贵的注意力机制检索过去的任意 token，解除了这一限制。

## 残差流上的注意力

受序列建模中注意力机制的启发，Kimi 开发了注意力残差（attention residual）——在深度方向的块之间做注意力：

![](https://substack-post-media.s3.amazonaws.com/public/images/72173975-fcd2-47f6-936c-3bdf39a4d0f3_2378x472.png)
*来源：Attention Residuals*

标准因果自注意力把 token $t$ 的输出计算为先前各 token 表示的加权和：

注意力残差使用同样的注意力机制，但把序列维度换成深度维度。不是对先前的 token 做注意力，而是每层对先前各层产生的表示做注意力。

![](https://substack-post-media.s3.amazonaws.com/public/images/5b221ce1-738f-4cb4-85b0-a190f1160f84_1736x1068.png)
*来源：SemiAnalysis*

与标准注意力不同，query 是每层学出来的参数，而不是由当前 token 生成。

对每一层 ℓ，我们定义：

每个色块代表来自先前某个 transformer 层的输出 token 表示。正如标准因果自注意力对序列中的 token 做 softmax 注意力，注意力残差对先前各层产生的表示做 softmax 注意力。

![](https://substack-post-media.s3.amazonaws.com/public/images/d4cfe58a-5bee-4008-baef-88b21d9ac602_1438x995.png)
*来源：SemiAnalysis*

注意力残差让模型能够细粒度地控制从过去各层挑选哪些输入，从而提升模型的表达能力。

## 块注意力残差（Block Attention Residuals）

注意力残差做注意力需要全部先前层的输出。对于分布在众多 GPU 上的大模型，这带来 O(Ld) 的通信开销。为克服这一问题，块注意力残差把 L 层划分为 N 个由 S 层组成的块。Block AttnRes 对已完成块的输出做注意力，对当前块则关注其不断演化的部分和。

![](https://substack-post-media.s3.amazonaws.com/public/images/f4feee85-669a-47f5-a5c4-dc6bf7625d5a_1327x736.png)
*来源：SemiAnalysis*

块注意力相对全注意力残差只有极小的性能折损，却把通信从 O*(Ld)* 削减到 O*(Nd)*。

令 bₙⁱ 表示块 n 中前 *i* 层的部分和，使得：

对块 $n$ 中的第 i 层，可用的块表示为：

与标准注意力不同，query 不依赖于输入。每层学习一个 query 向量：

对可用块表示的注意力权重计算如下：

输出是先前各层表示的加权和：

不再仅依赖残差流来保存信息，注意力残差让每一层都能直接、有选择地访问先前的表示。这种基于块的注意力残差变体在保持有竞争力的性能的同时，大幅降低了通信开销。

与标准残差连接相比，块残差展现出更好的扩展性，实现了 1.25 倍的计算效率。验证损失持续低于基线，且差距在衰减阶段进一步拉大。与输出幅度随深度增加而增大的标准残差网络不同，块注意力的选择性聚合输出有界，且梯度幅度保持一致。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

## 训练

与标准残差网络不同，注意力残差计算第 N 层需要全部 N-1 个块的输入。这对流水线并行是个问题，因为所有 N 个层的输出都需要跨阶段传输。

通过巧妙的跨阶段缓存与激活重计算（activation checkpointing），Kimi 把流水线并行的额外开销相对标准架构降到只有 4%。

### 跨阶段缓存

设 P 个物理阶段、V 个虚拟阶段。每个块 N 对每个 chunk 需要 C=PV 次通信。朴素做法需要为每个阶段传输所有已累积的块，这带来随物理与虚拟阶段数二次增长的开销。

可以通过跨虚拟阶段缓存输入来降低这种高通信量。较早层算出的块可以存放在本地内存中：

![](https://substack-post-media.s3.amazonaws.com/public/images/65fc610b-cae9-4264-8577-4b98067dc436_2048x1041.png)
*来源：SemiAnalysis*

对第一个虚拟阶段，所有块嵌入都需要在物理阶段内传输，每个完成的块存储在对应的 rank 上。对后续所有虚拟阶段，所有已缓存的块都可以复用于计算。只有本 rank 上不存在的块才需要传输，用于注意力残差计算。

![](https://substack-post-media.s3.amazonaws.com/public/images/7f98bacd-b59d-4383-afcc-d6b0284f52c6_2048x1152.png)
*来源：SemiAnalysis*

这把第一个与后续虚拟阶段的通信成本分开了。第一个虚拟阶段仍需为所有物理层承担同样的二次方成本；而在后续虚拟阶段，我们使用本地设备上的缓存输入，只需传输 PNp 个 chunk，把总通信量从 O*(C)* 降到 O*(P)*。

通信削减量与虚拟阶段数 V 成正比。正因如此，在一个完整阶段的前向与反向传播中，所有计算与通信都可以重叠。

### 内存开销

由于跨阶段缓存，所有块在全部 V 个虚拟阶段中只存储一次。配合激活重计算，用于注意力的所有块间 chunk 都被消除。每个阶段的激活重计算 *Pl* 与标准架构的 *H*l* 内存大小相当，没有额外内存成本。

## 推理

由于注意力残差计算注意力需要所有先前块的输出，朴素实现会产生过多内存访问。为降低开销，推理被分为两个阶段，对应自回归注意力的预填充与解码阶段。计算被划分为：对已完成块的块间（inter-block）注意力，以及对运行中块不断演化的注意力的块内（intra-block）注意力。

#### 阶段 1：并行块间注意力

![](https://substack-post-media.s3.amazonaws.com/public/images/5ebdae8b-b839-408d-baff-306bb81a433b_1389x947.png)
*来源：SemiAnalysis*

解码期间，我们要输出已完成块和每层学到的 query 向量。所有块间层同时用单个批量 query 对已完成块的表示做注意力，同时返回输出和 softmax 统计量，后者可复用于后续计算。这一阶段类似预填充阶段。

#### 阶段 2：串行块内注意力

![](https://substack-post-media.s3.amazonaws.com/public/images/930ae3ce-f4f2-4149-bf3d-e6e611c08f27_1236x961.png)
*来源：SemiAnalysis*

这一阶段类似于解码阶段。与 flash attention 类似，可以用在线 softmax 结合预计算的块间结果来计算块内不断演化的求和，从而减少冗余内存访问。

采用这种两阶段设计，IO 足迹与标准残差架构相近，只是多了阶段 1 的块间计算，而它通过把块内所有 query 批处理摊薄。

# LatentMoE

LatentMoE 在分发（dispatch）操作之前压缩被路由的 token，再在聚合（combine）操作之后解压。在 Kimi K3 的 Stable LatentMoE 中，他们在升维投影（解压）操作之前施加 RMSNorm，以降低对尺度变化的敏感度、提升模型性能。

![](https://substack-post-media.s3.amazonaws.com/public/images/8a0740fb-3e21-4bac-bf28-00122c5b985d_1504x1022.png)
*来源：Kimi K3 技术报告*

这里我们解释 LatentMoE 在 MoE 通信方面的设计原理。如 LatentMoE 论文所示，通信量与总路由 token 数 *t*、激活专家数 *K* 和专家输入维度 *d* 成正比，与专家并行规模 *E* 成反比。这很可能就是 Kimi K3 潜空间 MoE 维度大小与激活专家数配置背后的原因。Kimi K2 系列有 8 个激活专家、输入维度 7168，因此 Kimi K3 的潜空间输入维度取 3584（7168 的一半），就能让激活专家数翻倍到 16 而不增加通信量。

不过，**通信与计算时间的比值**对于估算系统效率可以说更重要（讨论见[这里](https://x.com/chhillee/status/2077966168304787769)和[这里](https://x.com/chhillee/status/2078130513546723531)）。该比值指示了吞吐受限状态下 MoE kernel 能把通信与计算重叠到什么程度的 roofline，而**专家中间层维度大小**是唯一影响该比值的模型配置。具体来说，增大专家中间层维度会降低该比值，意味着理论上可被隐藏的通信比例上限更高。下面我们推导公式：

- *t*：专家并行（EP）域内的总输入 token 数
- *K*：每 token 的激活专家数
- *N*：专家总数
- *E*：EP 域内的 rank 数
- *d*：专家输入维度
- *m*：专家中间层维度
- *P*：每个激活元素通信的总字节数（分发 + 聚合）
- *F*：每 GPU 的有效 FFN 专家（按 SwiGLU 建模）计算吞吐，FLOP/s
- *B*：每 GPU 的有效单向网络带宽，B/s

1. 假设专家路由均匀，每块 GPU 被分配 *t * K / E* 个 token
2. 假设专家路由均匀，平均有 1 / E 的 token 对源 GPU 而言是本地的，因此每块 GPU 分发 *(t*K/E) * (1-1/E)* 个 token
3. 每个 token 是一个 d 维向量，因此每 token 通信量为 *d * P*
4. 每 GPU 通信量为 *(t*K/E) * (1-1/E) * d * P*
5. 通信时间 T_comm = *(t * K * d * P) / (E * B) * (1-1/E)*
6. SwiGLU 计算包含三次矩阵乘法：

   1. Up（第一次）投影：d 到 m
   2. Gate 投影：d 到 m
   3. Down（第二次）投影：m 到 d

因此每个 token 的计算量为 *2*d*m + 2*d*m + 2*m*d = 6*d*m* FLOPs

7. 每 GPU 的计算时间为 *T_comp = (6*d*m) * (t*K/E) / F*
8. 通信与计算时间之比为

   *T_comm / T_comp*

   *= ((t * K * d * P) / (E * B) * (1-1/E)) / ((6*d*m) * (t*K/E) / F)*

   *= (P*F) / (6*m*B) * (1-1/E)*

我们相信，这一公式不仅推动了 Kimi 从 K2 到 K3 将专家中间层维度提高到 3072，也推动了近期所有开放权重模型，包括 DeepSeek V4 Pro、MiniMax M3、MiMo V2.5 Pro 和 Inkling。随着硬件改进、专家权重精度降低以节省内存容量，计算吞吐上升，因此降低该比值的一条途径就是增大专家中间层维度。

## 分位数负载均衡（Quantile load balancing, QB）

![](https://substack-post-media.s3.amazonaws.com/public/images/2c5c38d2-7d7f-4f2b-9d8a-c469ae99b1d5_2322x716.png)
*来源：Kimi K3 报告*

许多既有负载均衡方法需要仔细调超参。分位数均衡是 Jianlin Su 在 [2026 年 2 月的博客文章](https://kexue.fm/archives/11619)中提出的免超参、免辅助损失（aux-loss free）负载均衡技术。

QB 的基本原理与 aux-free 负载均衡相同：路由器偏置根据系统负载动态更新。但与 aux-free 负载均衡用某个小系数更新偏置不同，QB 直接根据路由器得分相对于路由截止阈值的分布计算下一个偏置。当路由器把负载分摊均匀时，偏置更新自然变小。

![](https://substack-post-media.s3.amazonaws.com/public/images/864e9183-2fd3-4784-9389-4e54f8b24b4d_1848x564.png)
*来源：Kimi K3 报告*

QB 试图找到这样的偏置：在当前截止阈值与当前 batch 的路由下，它本可以实现近似均衡——求解约束优化问题，并把更新应用到下一个 batch。第一个约束是每个 token 恰好路由到 k 个专家。第二个约束是：m 个 token 的 batch 每个选 k 个专家，共产生 (mk) 次分配；要在 n 个专家间均匀分摊负载，每个专家应处理 $q=mk/n$ 个 token。

每个 token 以带偏置路由器得分中第 (k+1) 高的值作为截止阈值，并用它计算每个专家实现负载均衡所需的偏置更新。对每个专家，QB 对其路由器得分与每个 token 截止阈值之间的裕量（margin）排序。它把负偏置设到第 q+1 大的裕量处，恰好留下 q 个裕量高于阈值。由于 q/m=k/n，这就是裕量的 (1-k/n) 分位数，故名分位数均衡（Quantile Balancing）。

# 推理性能

我们正在 [InferenceX](https://inferencex.semianalysis.com/) 上持续追踪 Kimi K3 的推理性能。

截至 7 月 30 日，OpenRouter 上所有提供商的底价为每百万输入 token $3、每百万输出 token $15。NVIDIA 和 AMD 都在 vLLM 上提供了 Day 0 配方，支持 DRAM 卸载和 DSpark 投机解码。

![](https://substack-post-media.s3.amazonaws.com/public/images/d9ea604c-17df-4cf2-9de0-c904388cac1d_2002x926.png)
*来源：OpenRouter*

在 InferenceX 上，我们直接用录制的内部 Claude Code 轨迹对 Kimi K3 的服务性能进行基准测试。我们重放一小时的轨迹直至达到稳态。每轮输入 token 中位数为 142k，输出 token 中位数为 444，每个会话中位数 65 轮。每轮输出 token 偏短是智能体框架上工作负载的典型特征：智能体频繁调用工具，连编辑也是工具调用。

这一基准比我们之前的 8k1k/1k1k 基准前进了一大步，因为它真正反映了现实世界的智能体用例。从系统角度看，它也更真实、最接近生产系统。它能反映 KV 缓存行为，包括前缀缓存和 KV 卸载到 DRAM。

![](https://substack-post-media.s3.amazonaws.com/public/images/9acbb1f7-14fe-49ed-a70f-2a90061ed6c6_2048x1103.png)
*来源：InferenceX*

对 Kimi K3 而言，Day 0 起服比 DSv4 更容易，这得益于权重发布前更充分的文档和准备。相应的镜像和投机解码器模型与权重同步发布。

在 NVIDIA 上，起服很简单。但由于模型体量太大，单台 B200 节点装不下，我们不得不使用流水线并行（PP）才能跑起来。DSpark 也无法与 PP 一起工作。

![](https://substack-post-media.s3.amazonaws.com/public/images/cef9190d-c48a-4482-9789-41607d1f1624_2048x1214.png)
*来源：InferenceX*

在 B300 上，模型可以装进单节点并良好服务。扣除权重后，GPU HBM 只能容纳 3.25M token 的缓存。在下图中，吞吐随批大小增加而上升，直到并发超过 8。这与 3.25M token 的 KV 缓存预算大致对应——缓存开始剧烈抖动（thrash），命中率在理论命中率为 95% 的情况下跌到 < 10%。
