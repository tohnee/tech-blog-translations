---
title: "No Positional Embeddings (NoPE)"
source: https://sebastianraschka.com/llm-architecture-gallery/nope/
crawled: 2026-09-06
---

# No Positional Embeddings (NoPE)

NoPE removes explicit positional information injection from an attention layer. The layer receives no absolute position embedding and applies no RoPE rotation. In an autoregressive model, the causal attention mask remains in place, so the computation still has a direction even without an explicit position coordinate.

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[Tiny Aya from-scratch Nb](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/15_tiny-aya/standalone-tiny-aya.ipynb)

![Annotated NoPE figure about length generalization](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/nope-length-generalization.webp)

Figure 1. An annotated figure from the
[2023 NoPE paper](https://arxiv.org/abs/2305.19466) showing better length generalization with
NoPE. The experiments used models around 100 million parameters (Original source
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)).

## What NoPE removes

NoPE is, in LLM contexts, an older idea that goes back to the 2023 paper [The Impact of Positional Encoding on Length Generalization in Transformers](https://arxiv.org/abs/2305.19466). The idea is to remove explicit positional information injection, such as classic absolute positional embedding layers in early GPT architectures or nowadays RoPE.

In transformer-based LLMs, positional encoding is typically necessary because self-attention treats tokens independently of order. Absolute position embeddings solve this by adding an additional embedding layer that adds information to the token embeddings.

RoPE, on the other hand, solves this by rotating the query and key vectors relative to their token position.

In NoPE layers, however, no such positional signal is added at all. It is not fixed, learned, or relative. There is no explicit position term.

## Why causal order survives

For a sequence of `T` tokens, attention needs one row of weights per token, so overall we get a `T × T` matrix. Each row answers a simple question. When updating this token, how much should each visible token matter? In a decoder-only LLM, future positions are masked out.

Even though there is no positional embedding, the model still knows which tokens come before, thanks to the causal attention mask. This mask prevents each token from attending to future ones. As a result, a token at position `t` can only see tokens at positions `≤ t`, which preserves the autoregressive ordering.

So while there is no positional information that is explicitly added, there is still an implicit sense of direction baked into the model’s structure, and the LLM, in the regular gradient-descent-based training, can learn to exploit it if it finds it beneficial for the optimization objective.

## What the length results show

The 2023 NoPE paper found better length generalization, which means that model performance deteriorated less as the tested sequence length increased.

Note that these experiments were conducted with a relatively small GPT-style model of approximately 100 million parameters and relatively small context sizes. It is unclear how well these findings generalize to larger, contemporary LLMs.

## Selective NoPE in recent models

SmolLM3 uses a mixed design and omits RoPE in every fourth layer. In the Tiny Aya from-scratch implementation, RoPE is applied only to [sliding-window attention](https://sebastianraschka.com/llm-architecture-gallery/swa/) layers. The global layers omit it. Arcee Trinity uses a similar local-global pattern.

The omission of the RoPE box in the Kimi Linear figure is intentional. Kimi applies NoPE in its [MLA](https://sebastianraschka.com/llm-architecture-gallery/mla/) global-attention layers. According to the Kimi Linear report, this lets MLA run as pure multi-query attention at inference and avoids RoPE retuning for long-context scaling.

![SmolLM3 architecture showing periodic NoPE layers](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/nope-smollm3-3b.webp)

Figure 2. SmolLM3 omits RoPE in every fourth transformer block (Original source
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)).

## Kimi K3 uses NoPE throughout

Kimi K3 is a different recent example. Interestingly, it got rid of all RoPE layers and uses NoPE everywhere instead. This is inherited from Kimi Linear. Other recent architectures tend to use RoPE in local attention layers and NoPE in the global layers.

Sources

[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
[A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)
[Tiny Aya implementation notes](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/15_tiny-aya/README.md)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
