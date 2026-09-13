---
title: "专家混合（MoE）"
title_en: "Mixture of experts (MoE)"
source: https://sebastianraschka.com/llm-architecture-gallery/moe/
crawled: 2026-09-06
translated: 2026-09-06
---

# 专家混合（MoE）

> 原文：[Mixture of experts (MoE)](https://sebastianraschka.com/llm-architecture-gallery/moe/)

MoE 的核心思想是，把 transformer 块中的每个 FeedForward 模块替换为多个专家层，而每个专家层本身也是一个 FeedForward 模块。也就是说，我们把单个 FeedForward 块换成了多个 FeedForward 块。

然后由路由器（router）为每个 token 只选出一小部分专家。这正是 MoE 模型可以在总参数量很大的同时，不必在每次推理时使用全部参数的原因。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[从零实现章节](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/07_moe)

![DeepSeek V3 与 R1 中的专家混合模块与标准前馈块对比](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/moe-deepseek-v3-vs-ffn.webp)

标准 FeedForward 块（左）与 DeepSeek V3 和 R1 中使用的路由式 MoE 模块（右）
（原始出处：[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)）。

## 为什么总参数与激活参数不同

transformer 块内部的 FeedForward 块通常占据模型总参数量的很大一部分。（注意，transformer 块以及其中的 FeedForward 块在 LLM 中会重复很多次；DeepSeek V3 重复了 61 次。）

因此，用多个 FeedForward 块替换单个 FeedForward 块（MoE 正是如此）会大幅增加模型的总参数量。不过关键技巧在于：我们并不对每个 token 使用（“激活”）所有专家，而是由路由器为每个 token 只选出一小部分专家。

由于每次只有少数专家处于激活状态，MoE 模块常被称为“稀疏”模块，与之相对的是始终使用全部参数集的“稠密”模块。不过，MoE 带来的庞大总参数量提升了 LLM 的容量，这意味着它在训练中可以吸收更多知识；同时稀疏性让推理保持高效，因为我们不会同时使用所有参数。

![专家混合层中总参数与激活参数的差异](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/moe-active-vs-total.webp)

随着专家数量增长，总参数量的增长速度远快于每个 token 的激活参数量（原始出处：
[*LLMs-from-scratch* MoE 材料](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/07_moe)）。

## 以 DeepSeek V3 为具体例子

DeepSeek V3 的每个 MoE 模块有 256 个专家，总参数量为 6710 亿。但在推理时，每次只有 9 个专家处于激活状态（1 个共享专家加上路由器选出的 8 个）。这意味着每个推理步骤只使用 370 亿参数，而不是全部 6710 亿。

这种“总量对激活”的区分，正是 MoE 模型名称常常同时包含两个数字的原因。例如，标注为 235B-A22B 的模型有 2350 亿总参数，每个 token 激活约 220 亿参数。

## 共享专家

DeepSeek V3 的 MoE 设计有一个值得注意的特点：使用共享专家。这是一个对每个 token 都始终激活的专家。这个想法并不新鲜，早在 [DeepSeek 2024 MoE](https://arxiv.org/abs/2401.06066) 和 [2022 DeepSpeedMoE](https://arxiv.org/abs/2201.05596) 论文中就已提出。

共享专家的好处最早在 DeepSpeedMoE 论文中被指出：他们发现与不设共享专家相比，它能提升整体建模性能。这很可能是因为常见或重复的模式不必由多个个体专家分别学习，从而为它们留出了更多空间去学习更专门化的模式。

来源

[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
[LLMs-from-scratch MoE 章节](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/07_moe)
[DeepSeekMoE 论文](https://arxiv.org/abs/2401.06066)
[DeepSpeedMoE 论文](https://arxiv.org/abs/2201.05596)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
