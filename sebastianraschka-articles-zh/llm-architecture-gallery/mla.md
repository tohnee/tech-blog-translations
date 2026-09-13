---
title: "多头潜在注意力（MLA）"
title_en: "Multi-Head Latent Attention (MLA)"
source: https://sebastianraschka.com/llm-architecture-gallery/mla/
crawled: 2026-09-06
translated: 2026-09-06
---

# 多头潜在注意力（MLA）

> 原文：[Multi-Head Latent Attention (MLA)](https://sebastianraschka.com/llm-architecture-gallery/mla/)

多头潜在注意力（MLA）背后的动机与[分组查询注意力（GQA）](https://sebastianraschka.com/llm-architecture-gallery/gqa/)类似：两者都是为了降低 [KV 缓存](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms)的内存需求。GQA 与 MLA 的区别在于，MLA 通过压缩存储内容来缩减缓存，而不是像 GQA 那样通过共享头来减少存储的 K/V 数量。

MLA 最初由 [DeepSeek-V2](https://arxiv.org/abs/2405.04434) 论文提出，后来成为 DeepSeek 时代极具标志性的设计（尤其在 DeepSeek-V3 和 R1 之后）。它比 GQA 更难实现、部署服务也更麻烦，但在模型规模和上下文长度大到缓存传输开始占据主导时，它如今往往更具吸引力：因为在相同的内存压缩率下，它能保持更好的建模性能（后面会细说）。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[从零实现章节](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/05_mla)

![多头潜在注意力与常规多头注意力的对比](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/mla-vs-mha.webp)

与 GQA 不同，MLA 不是通过分组头来降低 KV 开销，
而是通过缓存一个压缩的潜在表示来做到这一点。注意，同样的压缩也应用于 query，为简化起见图中未画出。（原始出处：
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)。）

核心操作

在键和值进入 [KV 缓存](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms)之前先进行压缩

实际收益

可以大幅节省 [KV 缓存](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms)内存，而不会出现更极端共享方案中常见的那种质量下降

示例架构

[DeepSeek V3](https://sebastianraschka.com/llm-architecture-gallery/#card-deepseek-v3)、
[Kimi K2](https://sebastianraschka.com/llm-architecture-gallery/#card-kimi-k2)、
[GLM-5](https://sebastianraschka.com/llm-architecture-gallery/#card-glm-5-744b)、
[Ling 2.5](https://sebastianraschka.com/llm-architecture-gallery/#card-ling-2-5-1t)、
[LongCat-Flash-Lite](https://sebastianraschka.com/llm-architecture-gallery/#card-longcat-flash-lite-68-5b-a3b)、
[Mistral Large 3](https://sebastianraschka.com/llm-architecture-gallery/#card-mistral-large-3)、
[Sarvam 105B](https://sebastianraschka.com/llm-architecture-gallery/#card-sarvam-105b) 以及
[Tencent Hy4-preview](https://sebastianraschka.com/llm-architecture-gallery/#card-tencent-hy4-preview-770b-a49b)

## 压缩，而非共享

MHA 和 GQA 缓存的是全分辨率的键、值张量，而 MLA 存储的是一个潜在表示，并在需要时重建出可用的状态。本质上，这是一种嵌入在注意力内部的缓存压缩策略，如前图所示。

下图展示了与常规 MHA 相比所能节省的内存。

![多头潜在注意力相对于多头注意力的内存节省](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/mla-memory-savings.webp)

一旦上下文长度增长，用潜在表示代替完整 K/V 张量进行缓存所带来的节省就变得非常明显（原始出处：
[*LLMs-from-scratch* MLA 章节](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/05_mla)）。

## 消融研究

DeepSeek-V2 论文给出了一些消融实验：在建模性能上，GQA 表现得比 MHA 更差，而 MLA 则保持得好得多，经过仔细调优甚至可以超过 MHA。这比"它能省内存"是一个有力得多的理由。

换句话说，DeepSeek 之所以偏爱 MLA，不仅因为它高效，更因为它在大规模下看起来是一种保持质量的效率选择。（不过同行告诉我，MLA 只在达到一定规模后才工作得好。对于较小的模型，比如 <100B，GQA 似乎效果更好，或者至少更容易调到理想状态。）

![标注版 DeepSeek-V2 消融表：比较 GQA、MHA 和 MLA 的建模性能](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/mla-deepseek-v2-ablation.webp)

在这里 GQA 落到了 MHA 之下，而 MLA 仍然具有竞争力，甚至可以略微超过 MHA。所依据的论文：
[DeepSeek-V2 论文](https://arxiv.org/abs/2405.04434)（原始出处：
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)。）

![分组查询注意力、多头潜在注意力与多头注意力之间的相对效率比较](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gqa-vs-mla-relative-efficiency.webp)

GQA 和 MLA 从不同方向解决同一个瓶颈。权衡在于简单性与更强的压缩之间。（原始出处：
[*A Dream of Spring for Open-Weight LLMs*](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)。）

## DeepSeek 之后的传播

自 V2 中引入之后，随着 DeepSeek V3/R1、V3.1 等模型让这一设计成为常态，MLA 开始出现在第二波架构中。Kimi K2 沿用了 DeepSeek 的配方并将其放大；GLM-5 在采用 MLA 的同时也采用了 [DeepSeek 稀疏注意力](https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/)（来自 DeepSeek V3.2）；Ling 2.5 将 MLA 与线性注意力混合架构搭配；Sarvam 发布了两个模型，其中 30B 模型沿用经典 GQA，105B 模型则切换到 MLA。

最后一组对比特别有价值，因为它把"实现复杂度"的讨论放到了一边：也就是说，Sarvam 团队两种变体都实现了，然后有意地在一个模型上使用 GQA、在另一个上使用 MLA。因此从某种意义上说，这让 MLA 看起来不再是一个理论上的备选项，而更像一个模型家族规模化之后具体可行的架构升级路径。

参考资料

[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
[A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)
[LLMs-from-scratch MLA 章节](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/05_mla)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
