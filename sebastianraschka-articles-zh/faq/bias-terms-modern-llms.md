---
title: "为什么一些 LLM 会去掉线性层中的偏置项？"
title_en: "Why do some LLMs remove bias terms from linear layers?"
source: https://sebastianraschka.com/faq/docs/bias-terms-modern-llms.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 为什么一些 LLM 会去掉线性层中的偏置项？

> 原文：[Why do some LLMs remove bias terms from linear layers?](https://sebastianraschka.com/faq/docs/bias-terms-modern-llms.html) · Sebastian Raschka's FAQ

若干现代 LLM（包括 Llama 风格的模型）在其注意力和前馈线性层中省略了偏置向量。实际原因在于：这些大型投影在没有学习偏移量的情况下已经表现得很好。一旦某种架构和训练方案证明了偏置是多余的，去掉它就能在每个 transformer 块中省下一点点开销。

通常的线性层计算 `xW + b`，其中 `W` 是权重矩阵，`b` 是偏置向量。设置 `bias=False` 就去掉了 `b` 的加法。相对于矩阵而言，省下的参数量很小。例如，对于一个宽度为 4,096 的方形层，矩阵包含约 1,680 万个权重，而偏置只有 4,096 个值。

同样的对比也适用于计算量。矩阵乘法主导了该层的成本。加上偏置的开销很小，尽管它仍然需要一次额外的向量加法，并可能使融合（fused）实现复杂化。面对如此多的投影和 transformer 块，模型设计者可能更愿意省掉一个在其设置中并未展现出明确收益的组件。

人们很容易用「RMSNorm 或残差连接取代了偏置」来解释这一选择。但这种说法过于绝对。偏置可以平移某一层的预激活值（pre-activation），包括 SwiGLU 门的输入，而归一化和残差路径一般来说都不能让这一效应消失。无偏置投影是一种经验性的架构选择，而不是数学上的必然要求。

![The repo's architecture comparison shows how modern Llama-style models keep the same broad decoder structure while simplifying several block-level details](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/gpt-to-llama/gpt-and-all-llamas.webp)

上图把无偏置层放在了 GPT 到 Llama 的更宏大演变背景中。它们常常与 RMSNorm、旋转位置嵌入以及 SwiGLU 一同出现。这些本是各自独立的设计决策，只是现代模型家族经常把它们作为一个组合一起采用。

模型是否使用偏置也取决于具体实现。某个家族可能在大型注意力和 MLP 投影中省略偏置，却在别处保留其他学习偏移量。同样地，一个带偏置项的模型也不见得就效率更低或更过时。

因此，我会把 `bias=False` 看作一种小型的、基于证据的简化。它去掉的是某一特定架构已被证明可以不需要的学习偏移量。对任何单层而言，节省都很有限，但这一改动很容易在整个大型 transformer 中一致地实施。
