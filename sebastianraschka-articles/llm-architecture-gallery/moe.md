---
title: "Mixture of experts (MoE)"
source: https://sebastianraschka.com/llm-architecture-gallery/moe/
crawled: 2026-09-06
---

# Mixture of experts (MoE)

The core idea in MoE is to replace each FeedForward module in a transformer block with multiple expert layers, where each of these expert layers is also a FeedForward module. This means that we swap a single FeedForward block for multiple FeedForward blocks.

The router then selects only a small subset of experts for each token. This is how an MoE model can have a high total parameter count without using all of these parameters for every inference step.

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[From-scratch chapter](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/07_moe)

![Mixture-of-Experts module in DeepSeek V3 and R1 compared with a standard feed-forward block](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/moe-deepseek-v3-vs-ffn.webp)

A standard FeedForward block (left) and the routed MoE module used in DeepSeek V3 and R1 (right)
(Original source
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)).

## Why total and active parameters differ

The FeedForward block inside a transformer block typically contains a large number of the model’s total parameters. (Note that the transformer block, and thereby the FeedForward block, is repeated many times in an LLM; in the case of DeepSeek V3, 61 times.)

So, replacing a single FeedForward block with multiple FeedForward blocks (as done in a MoE setup) substantially increases the model’s total parameter count. However, the key trick is that we don’t use (“activate”) all experts for every token. Instead, a router selects only a small subset of experts per token.

Because only a few experts are active at a time, MoE modules are often referred to as sparse, in contrast to dense modules that always use the full parameter set. However, the large total number of parameters via an MoE increases the capacity of the LLM, which means it can take up more knowledge during training. The sparsity keeps inference efficient, though, as we don’t use all the parameters at the same time.

![Difference between total and active parameters in Mixture of Experts layers](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/moe-active-vs-total.webp)

As the number of experts grows, the total parameter count increases much faster than the active parameter count
per token (Original source
[*LLMs-from-scratch* MoE materials](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/07_moe)).

## DeepSeek V3 as a concrete example

DeepSeek V3 has 256 experts per MoE module and a total of 671 billion parameters. Yet during inference, only 9 experts are active at a time (1 shared expert plus 8 selected by the router). This means just 37 billion parameters are used per inference step as opposed to all 671 billion.

This total-versus-active distinction is why MoE model names often include both numbers. For example, a model labeled 235B-A22B has 235 billion total parameters and about 22 billion active parameters per token.

## Shared experts

One notable feature of DeepSeek V3’s MoE design is the use of a shared expert. This is an expert that is always active for every token. This idea is not new and was already introduced in the [DeepSeek 2024 MoE](https://arxiv.org/abs/2401.06066) and [2022 DeepSpeedMoE](https://arxiv.org/abs/2201.05596) papers.

The benefit of having a shared expert was first noted in the DeepSpeedMoE paper, where they found that it boosts overall modeling performance compared to no shared experts. This is likely because common or repeated patterns don’t have to be learned by multiple individual experts, which leaves them with more room for learning more specialized patterns.

Sources

[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
[LLMs-from-scratch MoE chapter](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/07_moe)
[DeepSeekMoE paper](https://arxiv.org/abs/2401.06066)
[DeepSpeedMoE paper](https://arxiv.org/abs/2201.05596)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
