---
title: "无位置嵌入（NoPE）"
title_en: "No Positional Embeddings (NoPE)"
source: https://sebastianraschka.com/llm-architecture-gallery/nope/
crawled: 2026-09-06
translated: 2026-09-06
---

# 无位置嵌入（NoPE）

> 原文：[No Positional Embeddings (NoPE)](https://sebastianraschka.com/llm-architecture-gallery/nope/)

NoPE 从注意力层中移除显式的位置信息注入。该层不接收绝对位置嵌入，也不施加 RoPE 旋转。在自回归模型中，因果注意力掩码仍然保留，因此即便没有显式的位置坐标，计算依然有方向。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[Tiny Aya 从零实现 Nb](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/15_tiny-aya/standalone-tiny-aya.ipynb)

![关于长度泛化的 NoPE 标注图](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/nope-length-generalization.webp)

图 1. 来自[2023 年 NoPE 论文](https://arxiv.org/abs/2305.19466)的标注图，展示了 NoPE 带来更好的长度泛化。实验使用的模型参数量约为 1 亿（原始出处：[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)）。

## NoPE 移除了什么

在 LLM 语境中，NoPE 是一个较早的想法，可以追溯到 2023 年的论文 [The Impact of Positional Encoding on Length Generalization in Transformers](https://arxiv.org/abs/2305.19466)。其思路是移除显式的位置信息注入，例如早期 GPT 架构中经典的绝对位置嵌入层，或如今常用的 RoPE。

在基于 transformer 的 LLM 中，位置编码通常是必需的，因为自注意力对 token 的处理与顺序无关。绝对位置嵌入的解决方式是增加一个额外的嵌入层，把位置信息加到 token 嵌入上。

RoPE 则通过按 token 位置旋转 query 和 key 向量来解决这一问题。

而在 NoPE 层中，完全不添加任何此类位置信号。它不是固定的，不是可学习的，也不是相对的。没有任何显式的位置项。

## 为什么因果顺序仍然存在

对一个长度为 `T` 个 token 的序列，注意力需要为每个 token 生成一行权重，因此整体上得到一个 `T × T` 矩阵。每一行回答一个简单的问题：在更新这个 token 时，每个可见 token 应该占多大分量？在仅解码器（decoder-only）LLM 中，未来位置被掩码屏蔽。

即使没有位置嵌入，模型依然知道哪些 token 在前面，这要归功于因果注意力掩码。该掩码阻止每个 token 关注未来的 token。因此，位置 `t` 的 token 只能看到位置 `≤ t` 的 token，从而保住了自回归顺序。

所以，虽然没有显式加入任何位置信息，模型结构中仍然内建了一种隐式的方向感；在常规的基于梯度下降的训练中，如果这种方向感对优化目标有帮助，LLM 就能学会利用它。

## 长度实验结果说明了什么

2023 年的 NoPE 论文发现了更好的长度泛化，也就是说，随着测试序列长度增加，模型性能的退化更少。

请注意，这些实验使用的是参数量约 1 亿、上下文长度也相对较小的 GPT 风格模型。这些结论能在多大程度上推广到更大的当代 LLM，尚不清楚。

## 近期模型中的选择性 NoPE

SmolLM3 采用混合设计，每四层中省略一层 RoPE。在 Tiny Aya 的从零实现中，RoPE 只应用于[滑动窗口注意力](https://sebastianraschka.com/llm-architecture-gallery/swa/)层，全局层则省略。Arcee Trinity 使用类似的局部-全局模式。

Kimi Linear 图中省略 RoPE 框是有意为之：Kimi 在其 [MLA](https://sebastianraschka.com/llm-architecture-gallery/mla/) 全局注意力层中使用 NoPE。根据 Kimi Linear 报告，这让 MLA 在推理时可以作为纯多查询注意力运行，并避免为长上下文扩展重新调整 RoPE。

![SmolLM3 架构，展示周期性出现的 NoPE 层](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/nope-smollm3-3b.webp)

图 2. SmolLM3 在每四个 transformer 块中省略一次 RoPE（原始出处：[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)）。

## Kimi K3 全面使用 NoPE

Kimi K3 是另一个近期例子。有意思的是，它去掉了所有 RoPE 层，改为处处使用 NoPE。这一点继承自 Kimi Linear。其他近期架构则倾向于在局部注意力层使用 RoPE、在全局层使用 NoPE。

来源

[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
[A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)
[Tiny Aya 实现笔记](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/15_tiny-aya/README.md)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
