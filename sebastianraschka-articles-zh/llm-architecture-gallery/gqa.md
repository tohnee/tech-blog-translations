---
title: "分组查询注意力（GQA）"
title_en: "Grouped-Query Attention (GQA)"
source: https://sebastianraschka.com/llm-architecture-gallery/gqa/
crawled: 2026-09-06
translated: 2026-09-06
---

# 分组查询注意力（GQA）

> 原文：[Grouped-Query Attention (GQA)](https://sebastianraschka.com/llm-architecture-gallery/gqa/)

分组查询注意力（GQA）是从标准多头注意力派生出来的一种注意力变体。它由 Joshua Ainslie 及其同事在 2023 年的论文《[*GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints*](https://arxiv.org/abs/2305.13245)》中提出。

与 MHA 中每个头拥有自己的一组键和值不同，GQA 将多个查询头分组，让它们共享同一组键和值投影。这减少了推理期间需要从 [KV 缓存](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms)中存储和读取的键值数量。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[从零实现代码](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/04_gqa)

![多头注意力与分组查询注意力的对比](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gqa-mha-vs-gqa.webp)

MHA 与 GQA 的对比。这里的组大小为 2，即一组键值对由
2 个查询头共享（原始出处
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)。）

变化点

多个查询头共享同一组键和值投影

使用理由

更少的 K/V 头让 [KV 缓存](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms)更小，并降低内存带宽占用

示例架构

稠密模型：
[Llama 3 8B](https://sebastianraschka.com/llm-architecture-gallery/#card-llama-3-8b)、
[Qwen3 4B](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-4b)、
[Gemma 3 27B](https://sebastianraschka.com/llm-architecture-gallery/#card-gemma-3-27b)、
[Mistral Small 3.1 24B](https://sebastianraschka.com/llm-architecture-gallery/#card-mistral-small-3-1-24b)、
[SmolLM3 3B](https://sebastianraschka.com/llm-architecture-gallery/#card-smollm3-3b) 以及
[Tiny Aya 3.35B](https://sebastianraschka.com/llm-architecture-gallery/#card-tiny-aya-3-35b)。
  
稀疏模型：
[Llama 4 Maverick](https://sebastianraschka.com/llm-architecture-gallery/#card-llama-4-maverick)、
[Qwen3 235B-A22B](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-235b-a22b)、
[Step 3.5 Flash 196B](https://sebastianraschka.com/llm-architecture-gallery/#card-step-3-5-flash-196b) 以及
[Sarvam 30B](https://sebastianraschka.com/llm-architecture-gallery/#card-sarvam-30b)。

## GQA 为何流行

GQA 的核心思想是让多个查询头共享键头和值头，从而减少键值头的数量。这 (1) 降低了模型的参数量，并且 (2) 减少了推理期间键值张量对内存带宽的占用，因为需要从 [KV 缓存](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms)中存储和读取的键值更少了。

（如果你好奇 GQA 在代码中是什么样子，可以看我的 [GPT-2 到 Llama 3 转换指南](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/07_gpt_to_llama/converting-llama2-to-llama3.ipynb)，其中有一个不带 KV 缓存的版本；带 KV 缓存的变体在[这里](https://github.com/rasbt/LLMs-from-scratch/blob/main/pkg/llms_from_scratch/llama3.py)。）

虽然 GQA 主要是针对 MHA 的一种计算效率上的变通方案，但消融研究（例如[原始 GQA 论文](https://arxiv.org/abs/2305.13245)和 [Llama 2 论文](https://arxiv.org/abs/2307.09288)中的实验）表明，在大语言模型的建模性能上，它与标准 MHA 表现相当。

## 内存节省是如何实现的

对于 bf16 精度的键和值，每层的缓存大小为：

```python
2 × sequence length × number of K/V heads × head dimension × 2 bytes
```

MHA 使用与查询头数量相同的 K/V 头，而多查询注意力（MQA）只使用 1 个。GQA 介于两者之间。这也是为什么上下文越长，节省越显著。

![分组查询注意力相对多头注意力的内存节省](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gqa-memory-savings.webp)

越低越好。随着上下文窗口增长，
[KV 缓存](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms)
的节省变得更加显著（原始出处
[*LLMs-from-scratch* GQA 材料](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/04_gqa)。）

## 为什么 GQA 在 2026 年依然重要

根据 [DeepSeek-V2 论文](https://arxiv.org/abs/2405.04434)中的消融研究，[多头潜在注意力（MLA）](https://sebastianraschka.com/llm-architecture-gallery/mla/)这类更高级的变体可以在相同的 KV 效率水平上提供更好的建模性能。不过，MLA 的实现更复杂。

GQA 依然有吸引力，因为它稳健、更容易实现，也更容易训练（根据我的经验，需要调的超参数更少）。

在我 [Spring Architectures](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight) 一文涉及的各次发布中，只有 MiniMax M2.5 和 Nanbeige 4.1 在这一点上保持得非常经典：使用 GQA 而没有叠加任何其他效率改进。较小的 Sarvam 30B 模型也使用经典 GQA，而较大的 105B 版本则切换到了 DeepSeek 风格的 MLA。

![分组查询注意力、多头潜在注意力与多头注意力的相对效率对比](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gqa-vs-mla-relative-efficiency.webp)

GQA 共享键值头，而 MLA 压缩缓存中存储的状态。两者以不同的方式缓解同一个
内存瓶颈（原始出处
[*A Dream of Spring for Open-Weight LLMs*](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)。）

参考资料

[Ainslie et al. (2023), *GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints*](https://arxiv.org/abs/2305.13245)
[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
[A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)
[LLMs-from-scratch GQA 材料](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/04_gqa)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
