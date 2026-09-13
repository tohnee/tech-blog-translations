---
title: "Sliding Window Attention (SWA)"
source: https://sebastianraschka.com/llm-architecture-gallery/swa/
crawled: 2026-09-06
---

# Sliding Window Attention (SWA)

So, what is sliding window attention? If we think of regular self-attention as a *global* attention mechanism, since each sequence element can access every other sequence element, then we can think of sliding window attention as *local* attention, because here we restrict the context size around the current query position.

Some architectures combine these local layers with occasional global attention layers so that information can still propagate across the entire sequence.

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[From-scratch chapter](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/06_swa)

![Comparison between global attention and sliding-window attention](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/swa-global-vs-local.webp)

A comparison between regular attention (left) and sliding window attention (right) (Original source
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)).

What changes

Selected layers only attend to a recent window instead of the entire context

Why use it

Local layers use less computation and keep less cached context; occasional global layers retain full-context access

Example architectures

[Gemma 3 27B](https://sebastianraschka.com/llm-architecture-gallery/#card-gemma-3-27b),
[OLMo 3 32B](https://sebastianraschka.com/llm-architecture-gallery/#card-olmo-3-32b),
[Xiaomi MiMo-V2-Flash](https://sebastianraschka.com/llm-architecture-gallery/#card-xiaomi-mimo-v2-flash-309b),
[Arcee Trinity](https://sebastianraschka.com/llm-architecture-gallery/#card-arcee-ai-trinity-large-400b),
[Step 3.5 Flash](https://sebastianraschka.com/llm-architecture-gallery/#card-step-3-5-flash-196b), and
[Tiny Aya](https://sebastianraschka.com/llm-architecture-gallery/#card-tiny-aya-3-35b)

## Gemma 3 as a reference point

For instance, Gemma 2 uses a hybrid attention mechanism that combines sliding window (local) and global attention in a 1:1 ratio. Each token can attend to a 4k-token window of nearby context.

Where Gemma 2 used sliding window attention in every other layer, Gemma 3 has a 5:1 ratio, meaning there is only 1 full attention layer for every 5 local layers. Gemma 3 also reduced the sliding window size from 4096 to 1024.

According to the Gemma 3 ablation study, this more aggressive use of sliding window attention has minimal impact on modeling performance.

![Gemma 3 sliding-window ablation showing little quality loss](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/swa-gemma-ablation.webp)

The Gemma 3 ablation study suggests that the smaller window and more aggressive local-to-global ratio have little
effect on perplexity. Underlying paper [Gemma 3 article](https://arxiv.org/abs/2503.19786)
(Original source
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)).

## The ratio and window size

The local-to-global layer pattern and the attention window size determine how aggressively a model uses SWA. The gallery includes several examples:

- Gemma 3 and Xiaomi use a 5:1 local-to-global pattern.
- OLMo 3 and Arcee Trinity use a 3:1 pattern.
- Xiaomi also uses a window size of 128, which is much smaller, and therefore more aggressive, than Gemma’s 1024.

SWA is essentially a knob that can be tuned more or less aggressively.

![Sliding-window attention memory savings compared to full attention](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/swa-memory-savings.webp)

The long-context savings come from turning many full-attention
layers into local ones, which reduces how much cached context those layers need to consider (Original source
[*LLMs-from-scratch* SWA materials](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/06_swa)).

## Why it often appears with GQA

Please note that sliding window attention can be used with both [multi-head attention](https://sebastianraschka.com/llm-architecture-gallery/mha/) and [grouped-query attention (GQA)](https://sebastianraschka.com/llm-architecture-gallery/gqa/); Gemma 3 uses GQA.

The two mechanisms change different parts of the cache. SWA limits how much context each local layer keeps. GQA reduces the number of cached key and value heads per token.

Sources

[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
[A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)
[LLMs-from-scratch SWA chapter](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/06_swa)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
