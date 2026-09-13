---
title: "Multi-Head Latent Attention (MLA)"
source: https://sebastianraschka.com/llm-architecture-gallery/mla/
crawled: 2026-09-06
---

# Multi-Head Latent Attention (MLA)

The motivation behind Multi-head Latent Attention (MLA) is similar to [Grouped-Query Attention (GQA)](https://sebastianraschka.com/llm-architecture-gallery/gqa/). Both are solutions for reducing [KV-cache](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms) memory requirements. The difference between GQA and MLA is that MLA shrinks the cache by compressing what gets stored rather than by reducing how many K/Vs are stored by sharing heads.

MLA, originally proposed in the [DeepSeek-V2](https://arxiv.org/abs/2405.04434) paper, became such a defining DeepSeek-era idea (especially after DeepSeek-V3 and R1). It is more complicated to implement than GQA, more complicated to serve, but nowadays also often more compelling once model size and context length get large enough that cache traffic starts to dominate, because at the same rate of memory reduction, it could maintain better modeling performance (more on that later).

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[From-scratch chapter](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/05_mla)

![Comparison between multi-head latent attention and regular multi-head attention](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/mla-vs-mha.webp)

Unlike GQA, MLA does not reduce KV cost by grouping heads.
It reduces it by caching a compressed latent representation. Note that it is also applied to the query, which is
not shown for simplicity (Original source:
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)).

Core move

Compress keys and values before they enter the [KV cache](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms)

Practical benefit

It can save [KV-cache](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms) memory aggressively without the quality drop often associated with more extreme sharing schemes

Example architectures

[DeepSeek V3](https://sebastianraschka.com/llm-architecture-gallery/#card-deepseek-v3),
[Kimi K2](https://sebastianraschka.com/llm-architecture-gallery/#card-kimi-k2),
[GLM-5](https://sebastianraschka.com/llm-architecture-gallery/#card-glm-5-744b),
[Ling 2.5](https://sebastianraschka.com/llm-architecture-gallery/#card-ling-2-5-1t),
[LongCat-Flash-Lite](https://sebastianraschka.com/llm-architecture-gallery/#card-longcat-flash-lite-68-5b-a3b),
[Mistral Large 3](https://sebastianraschka.com/llm-architecture-gallery/#card-mistral-large-3),
[Sarvam 105B](https://sebastianraschka.com/llm-architecture-gallery/#card-sarvam-105b), and
[Tencent Hy4-preview](https://sebastianraschka.com/llm-architecture-gallery/#card-tencent-hy4-preview-770b-a49b)

## Compression, Not Sharing

Instead of caching full-resolution key and value tensors as in MHA and GQA, MLA stores a latent representation and reconstructs the usable state when needed. Essentially, it is a cache compression strategy embedded inside attention, as illustrated in the previous figure.

The figure below shows the savings compared to regular MHA.

![Memory savings of multi-head latent attention versus multi-head attention](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/mla-memory-savings.webp)

Once context length grows, the savings from caching a latent
representation instead of full K/V tensors become very visible (Original source:
[*LLMs-from-scratch* MLA chapter](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/05_mla)).

## Ablation Studies

The DeepSeek-V2 paper provided some ablations where GQA looked worse than MHA in terms of modeling performance, while MLA held up much better and could even outperform MHA when tuned carefully. That is a much stronger justification than “it saves memory.”

In other words, MLA is a preferable attention mechanism for DeepSeek not just because it was efficient, but because it looked like a quality-preserving efficiency move at large scale. (But colleagues tell me that MLA only works well at a certain size. For smaller models, let’s say <100B, GQA seems to work better, or, is at least easier to tune and get right.)

![Annotated DeepSeek-V2 ablation table comparing modeling performance for GQA, MHA, and MLA](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/mla-deepseek-v2-ablation.webp)

GQA drops below MHA here, while MLA remains competitive and can even slightly outperform it. Underlying paper:
[DeepSeek-V2 paper](https://arxiv.org/abs/2405.04434) (Original source:
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)).

![Relative efficiency comparison between grouped-query attention, multi-head latent attention, and multi-head attention](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gqa-vs-mla-relative-efficiency.webp)

GQA and MLA are solving the same bottleneck from different directions. The tradeoff is simplicity versus stronger
compression (Original source:
[*A Dream of Spring for Open-Weight LLMs*](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)).

## How It Spread After DeepSeek

Once DeepSeek V3/R1, V3.1 etc. normalized the design after its introduction in V2, it started showing up in a second wave of architectures. Kimi K2 kept the DeepSeek recipe and scaled it up. GLM-5 adopted MLA together with [DeepSeek Sparse Attention](https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/) (from DeepSeek V3.2). Ling 2.5 paired MLA with a linear-attention hybrid. Sarvam released two models where the 30B model stayed with classic GQA and the 105B model switched to MLA.

That last pair is particularly useful as it puts the technical-complexity discussion aside. I.e., the Sarvam team implemented both variants and deliberately chose to then use GQA for one variant and MLA for the other. So, in a sense, that makes MLA feel less like a theoretical alternative and more like a concrete architectural upgrade path once a family scales up.

Sources

[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
[A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)
[LLMs-from-scratch MLA chapter](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/05_mla)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
