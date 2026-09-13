---
title: "门控注意力（Gated Attention）"
title_en: "Gated Attention"
source: https://sebastianraschka.com/llm-architecture-gallery/gated-attention/
crawled: 2026-09-06
translated: 2026-09-06
---

# 门控注意力（Gated Attention）

> 原文：[Gated Attention](https://sebastianraschka.com/llm-architecture-gallery/gated-attention/)

门控注意力保留了熟悉的缩放点积注意力计算，并在其输出上增加一个可学习的 sigmoid 门。在每个 token 处，这个门控制注意力结果以多大强度流入输出投影和残差流。

位置很关键：该门作用在 softmax 注意力混合完 value 向量之后。它不改变注意力权重，不减少 KV 缓存，也不改变全注意力层的平方复杂度。它只是给该层提供了一种额外的手段，用来抑制无益的注意力结果。

我发现把这个小操作与它周围的更大架构区分开来看会很有帮助。Qwen 将门控注意力用作循环混合架构中的昂贵部分；Trinity Large 则在整个局部/全局注意力堆栈中应用同一个基本思路。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[混合注意力](https://sebastianraschka.com/llm-architecture-gallery/hybrid-attention/)
[Qwen3.5 从零实现 Nb](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/16_qwen3.5/qwen3.5.ipynb)

![Trinity Large 架构与门控注意力代码片段](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gated-attention-trinity-large.webp)

图 1. Trinity Large 在输出投影之前，将缩放点积注意力的输出乘以一个逐元素的 sigmoid 门。其局部/全局层调度则是另一个独立的设计选择。（原始出处：[*A Dream of Spring for Open-Weight LLMs*](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)）。

变化点

一个可学习的 sigmoid 门在输出投影之前对注意力输出进行缩放

保持不变之处

softmax 注意力、KV 缓存以及注意力层关于序列长度的复杂度

示例架构

[Qwen3-Next 80B-A3B](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-next-80b-a3b)、
[Qwen3.5 397B](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-5-397b)、
[Trinity Large 400B](https://sebastianraschka.com/llm-architecture-gallery/#card-arcee-ai-trinity-large-400b) 与
[Tencent Hy4-preview](https://sebastianraschka.com/llm-architecture-gallery/#card-tencent-hy4-preview-770b-a49b)

## 注意力之后的门

设 \(X\) 为归一化后的隐藏状态，\(A\) 为通常的注意力输出。一个简化的门控块可以写作

\[A = \operatorname{SDPA}(Q,K,V), \qquad
G = \sigma(XW\_g), \qquad
Y = (A \odot G)W\_o.\]

sigmoid 使每个门值保持在 0 到 1 之间：接近 0 的值会抑制注意力输出的对应部分，接近 1 的值则让它通过。取决于具体实现，模型可以为整个注意力头学习一个门值，也可以为该头的各个特征通道学习不同的值。

[最初的门控注意力研究](https://arxiv.org/abs/2505.06708)比较了 30 种变体，包括多种门的位置与粒度。在其实验中，在缩放点积注意力之后施加 sigmoid 门效果最好。作者还观察到注意力汇聚（attention sink）现象减少、长上下文外推能力更好、训练更稳定。这些是他们匹配模型对照研究的经验结果，并非对每个架构都成立的保证。

## Qwen 的实现方式

[Qwen3-Next 80B-A3B](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct) 共 48 层，重复“三层 Gated DeltaNet 加一层门控 softmax 注意力”的模式，得到 36 个循环层和 12 个注意力层。注意力部分使用分组查询注意力。Qwen3.5 把 3:1 模式延续到 Qwen 主力模型线上，其 397B-A17B 变体有 45 个 Gated DeltaNet 层和 15 个注意力层。

从代码层面快速核查可以让这个门变得具体。在 [Qwen3-Next 实现](https://github.com/huggingface/transformers/blob/main/src/transformers/models/qwen3_next/modular_qwen3_next.py)中，query 投影同时产生 query 特征与门特征；注意力计算完成、各头完成重排之后，代码将结果乘以 `sigmoid(gate)`，再施加输出投影。

最容易忽略的细节是：Qwen 在这个块中还使用了零中心化的 QK-Norm 和部分 RoPE。那些是相邻的稳定性与位置编码选择；而 sigmoid 输出门才是让这个块成为“门控注意力”的那个特征。

![Qwen3-Next 架构，在混合堆栈中展示门控注意力](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gated-attention-qwen3-next.webp)

图 2. Qwen3-Next 在每三连 Gated DeltaNet 层之间周期性插入一个门控 softmax 注意力层。只有注意力层维护随序列长度变化的 KV 缓存。（原始出处：[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)）。

## Trinity 在纯注意力堆栈中使用门

[Trinity Large](https://arxiv.org/abs/2602.17004) 有 60 个分组查询注意力层，按 45 个局部层与 15 个全局层排布。局部层使用带 RoPE 的 4,096-token 滑动窗口；每第四层为全局层并使用 NoPE。每个注意力层都在输出投影之前对注意力输出施加逐元素 sigmoid 门。

这是对 Qwen 布局的一个有用反例：门控注意力并不需要 Gated DeltaNet 或其他循环序列模块。门可以放在局部注意力、全局注意力或两者的混合之中。

额外的工作主要是门投影、sigmoid 和逐元素乘法。门控注意力论文在其实验设置中报告了不到 2% 的额外实际时延。确切开销取决于实现、硬件与周围的模型，而 KV 缓存与全注意力的成本依然存在。

来源

[门控注意力论文](https://arxiv.org/abs/2505.06708)
[Qwen3-Next 模型卡片](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct)
[Qwen3-Next 实现](https://github.com/huggingface/transformers/blob/main/src/transformers/models/qwen3_next/modular_qwen3_next.py)
[Trinity Large 技术报告](https://arxiv.org/abs/2602.17004)
[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
[A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)
[Qwen3.5 实现笔记](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/16_qwen3.5/qwen3.5.ipynb)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
