---
title: "混合注意力"
title_en: "Hybrid Attention"
source: https://sebastianraschka.com/llm-architecture-gallery/hybrid-attention/
crawled: 2026-09-06
translated: 2026-09-06
---

# 混合注意力

> 原文：[Hybrid Attention](https://sebastianraschka.com/llm-architecture-gallery/hybrid-attention/)

混合注意力（Hybrid Attention）在同一个模型堆叠中混用不同的序列处理机制。在本文涵盖的架构中，大多数层使用循环的线性注意力或状态空间模块，少数层保留 softmax 注意力以进行直接的内容查找。

这种组合针对的是长上下文的两大开销。在预填充（prefill）阶段，标准自注意力要比较所有 token 位置，其分数计算随序列长度呈平方增长。在自回归解码阶段，每个注意力层还要维护一个随上下文增长的键值（KV）缓存。而 [Gated DeltaNet](https://arxiv.org/abs/2412.06464) 或 [Mamba-2](https://arxiv.org/abs/2405.21060) 这类循环层携带的则是固定大小的状态。

保留部分全注意力层，让模型可以周期性地直接访问缓存中的单个 token；循环层则以更低的成本处理大部分序列。正因如此，我认为相比单纯的"混合注意力"标签，层的比例信息量更大。Qwen 每个注意力层搭配三个循环层，而其他模型则选择了不同的机制和比例。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[门控注意力](https://sebastianraschka.com/llm-architecture-gallery/gated-attention/)
[从零实现章节](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/08_deltanet)

![线性注意力混合架构概览](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gated-deltanet-hybrid-overview.webp)

图 1. Qwen3-Next 重复"三个 Gated DeltaNet 块 + 一个
[门控注意力](https://arxiv.org/abs/2505.06708)块"的组合。
大多数层使用循环状态，每四层才有一层在 KV 缓存上执行 softmax 注意力。
（原始出处：
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)。）

概要

大多数块使用更廉价的循环序列模块，而周期性的注意力层保留直接的 token 查找

为什么保留注意力

循环状态会压缩过去的信息；注意力层则可以回访缓存中的单个 token

示例架构

[Qwen3-Next 80B-A3B](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-next-80b-a3b)、
[Qwen3.5 397B](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-5-397b)、
[Kimi Linear 48B-A3B](https://sebastianraschka.com/llm-architecture-gallery/#card-kimi-linear-48b-a3b)、
[Ling 2.5 1T](https://sebastianraschka.com/llm-architecture-gallery/#card-ling-2-5-1t)、
[Ling 3.0 Flash](https://sebastianraschka.com/llm-architecture-gallery/#card-ling-3-0-flash)、
[Nemotron 3 Nano 30B-A3B](https://sebastianraschka.com/llm-architecture-gallery/#card-nemotron-3-nano-30b-a3b) 以及
[Nemotron 3 Super 120B-A12B](https://sebastianraschka.com/llm-architecture-gallery/#card-nemotron-3-super-120b-a12b)

## Qwen 模式的工作方式

[Qwen3-Next 80B-A3B](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct) 共有 48 层，按 3:1 模式重复 12 次排列：三个 Gated DeltaNet 块之后跟一个[门控注意力](https://sebastianraschka.com/llm-architecture-gallery/gated-attention/)块。这意味着 36 层使用循环线性注意力，12 层保留 softmax 注意力。

在 Gated DeltaNet 块内部，模型计算查询、键和值向量，并同时计算两个可学习的门（alpha 和 beta）。它通过 delta 规则更新向一个小型快速权重记忆中写入内容。这个状态相当于对过去信息的一个滚动摘要：一个门控制记忆衰减，另一个门控制新值对状态更新的强度。

状态大小不随序列增长。门控注意力层则拥有我们熟悉的 token 到 token 的注意力路径，并维护一个 KV 缓存，因此在长上下文长度下依然更昂贵。Qwen 的层中只有四分之一需要支付这笔成本。

![全注意力与 Gated DeltaNet 混合架构的内存对比](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gated-deltanet-memory-savings.webp)

图 2. 内存曲线对比了全注意力与用 Gated DeltaNet 替换大多数注意力层后的堆叠。
剩余的注意力层仍然需要不断增长的 KV 缓存，但贡献这条曲线的
层要少得多。（原始出处：
[*LLMs-from-scratch* DeltaNet 材料](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/08_deltanet)。）

Qwen3.5 在 Qwen 主模型线中保留了同样的 3:1 骨干。例如，60 层的 Qwen3.5 397B-A17B 模型将这个四层组重复了 15 次。该模型在规模和架构的其他部分与 Qwen3-Next 不同，但序列混合的编排方式仍然一眼可辨。

![Qwen3.5 与 Qwen3-Next 架构的对比](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gated-deltanet-qwen35.webp)

图 3. Qwen3.5 把源自 Qwen3-Next 的 3:1 Gated DeltaNet 与门控注意力编排
带入了 Qwen 主模型线。（原始出处：
[*A Dream of Spring for Open-Weight LLMs*](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)。）

## Kimi Linear 同时更换了两种层

[Kimi Linear](https://arxiv.org/abs/2510.26692) 使用 20 层 Kimi Delta Attention（KDA）和 7 层带门控的[多头潜在注意力（MLA）](https://sebastianraschka.com/llm-architecture-gallery/mla/)。这与 Qwen3-Next 的编排大致相同，也接近 3:1。

KDA 是对 Gated DeltaNet 记忆更新的改良。Qwen3-Next 每个头只使用一个标量衰减门，而 KDA 为每个特征通道学习单独的衰减值，让循环状态对"保留什么"有更细的控制。周期性出现的 MLA 层提供 softmax 注意力，同时把键和值压缩成更小的潜在表示。

有意义的对比是两者的分工。KDA 把已处理的历史压缩进固定大小的状态；MLA 则可以回访较早的特定 token，尽管它的 KV 缓存仍会随序列增长。

![Qwen3-Next 与 Kimi Linear 的并排对比](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/hybrid-attention-kimi-vs-qwen.webp)

图 4. Kimi Linear 保持了大致 3:1 的编排，但更换了两种层类型：KDA 替换
Gated DeltaNet，带门控的 MLA 替换门控注意力。（原始出处：
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)。）

## Ling 2.5 使用 Lightning Attention

[Ling 2.5](https://huggingface.co/inclusionAI/Ling-2.5-1T) 使用了另一种循环线性注意力机制，称为 Lightning Attention。它的堆叠中每 7 层 Lightning Attention 配 1 层 MLA。这个 1:7 的比例把比 Qwen 和 Kimi 布局更多的序列处理工作压到了循环路径上。

MLA 层压缩 KV 表示并保留直接的内容查找；Lightning Attention 则用循环状态承担其余的层。因此，Ling 遵循的是同一套总体配方，只是换用了不同的轻量机制和不同比例。

![Ling 2.5 与 Qwen3.5 的对比](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/hybrid-attention-ling-vs-qwen.webp)

图 5. Ling 2.5 将 Lightning Attention 与 MLA 配对，而 Qwen3.5 将 Gated DeltaNet 与
门控注意力配对。两者都为基于 KV 缓存的注意力保留少数层。（原始出处：
[*A Dream of Spring for Open-Weight LLMs*](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)。）

Ling 团队报告称，在 32k token 序列长度下，吞吐量达到 Kimi K2 的 3.5 倍。两个模型的总参数量都在 1 万亿左右，但它们的激活参数量和架构各不相同。注意，这是一项厂商自行报告的系统级对比：它衡量的是完整的 Ling 实现，并没有单独隔离出 Lightning Attention 的贡献。

![Ling 2.5 吞吐量对比](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/hybrid-attention-ling-throughput.webp)

图 6. 公布的 32k token 吞吐量图表把 Kimi K2 归一化为 1 倍，并报告 Ling 2.5 约为
3.5 倍。该结果包含完整的模型和推理系统。（原始出处：
[*Ling 2.5 模型主页*](https://huggingface.co/inclusionAI/Ling-2.5-1T)。）

## Nemotron 使用 Mamba-2 层

Nemotron 3 系列模型使用 [Mamba-2](https://arxiv.org/abs/2405.21060) 作为更廉价的序列模块。Mamba-2 是一个状态空间模型，在这个混合架构中扮演类似的角色：它维护一个循环状态，从而避免随序列长度增长的 KV 缓存。

Nemotron 3 Nano 拥有一个 52 层的堆叠：23 层 Mamba-2、23 层稀疏专家混合层和 6 层注意力层。注意力层只占堆叠的一小部分：Mamba-2 处理大部分序列处理，MoE 层处理前馈计算。

![Nemotron 3 Nano 架构](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/hybrid-attention-nemotron-nano.webp)

图 7. Nemotron 3 Nano 在 52 层堆叠中交错排列 Mamba-2、稀疏 MoE 和六个注意力层。
其注意力层提供偶发性的直接检索。（原始出处：
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)。）

[Nemotron 3 Super](https://arxiv.org/abs/2604.12374) 把这一布局扩展为 40 层 Mamba-2、40 层[潜在 MoE](https://sebastianraschka.com/llm-architecture-gallery/latent-moe/) 和 8 层注意力层，并加入了共享权重的[多 token 预测（MTP）](https://sebastianraschka.com/llm-architecture-gallery/mtp/)。潜在 MoE 影响的是专家计算，MTP 支持的是投机解码，两者都与"循环层与注意力层交错"这一选择相互独立。

![Nemotron 3 Super 架构](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/hybrid-attention-nemotron-super.webp)

图 8. Nemotron 3 Super 保留了 Mamba-2 与注意力层骨干，并加入潜在 MoE 和
共享权重的 MTP。这些组件改变的是模型的其他部分。（原始出处：
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)。）

## 混合架构牺牲了什么

循环状态的大小是固定的，因此它无法把每个较早的 token 都作为独立条目保留下来。随着新 token 不断到来，状态必须决定保留什么。周期性的注意力层通过让模型可以直接访问自己缓存的历史来弥补这一点，但这并没有消除中间那些循环层所做的压缩。

这种设计还只是减缓而非消除 KV 缓存的成长：剩余的注意力层或 MLA 层仍会缓存过去的 token。这些层的数量、位置和注意力类型，决定了混合架构能节省多少内存。

模型层面的结果还包含许多其他选择，包括训练数据、MoE 设计、数值精度和优化过的内核。如果没有匹配的消融实验，就不能把某项吞吐量或质量对比单独归因于混合编排本身。

参考资料

[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
[A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)
[Qwen3-Next 模型卡](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct)
[门控 Delta 网络论文](https://arxiv.org/abs/2412.06464)
[Kimi Linear 论文](https://arxiv.org/abs/2510.26692)
[Mamba-2 论文](https://arxiv.org/abs/2405.21060)
[门控注意力论文](https://arxiv.org/abs/2505.06708)
[Ling 2.5 模型卡](https://huggingface.co/inclusionAI/Ling-2.5-1T)
[Ling 3.0 Flash 模型卡](https://huggingface.co/inclusionAI/Ling-3.0-flash)
[Nemotron 3 Nano 模型卡](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16)
[Nemotron 3 Super 报告](https://arxiv.org/abs/2604.12374)
[LLMs-from-scratch DeltaNet 章节](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/08_deltanet)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
