---
title: "Latent MoE"
source: https://sebastianraschka.com/llm-architecture-gallery/latent-moe/
crawled: 2026-09-06
---

# Latent MoE

Latent MoE runs the routed feed-forward experts in a smaller latent space. It is still a sparse mixture-of-experts ([MoE](https://sebastianraschka.com/llm-architecture-gallery/moe/)) layer. A router selects a few experts for each token, and only those experts process it. Nemotron 3 and Kimi K3 use different compression ratios, but they share this basic layout.

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[MoE from-scratch materials](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/07_moe)

![Nemotron 3 Super architecture showing latent MoE layers](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/latent-moe-nemotron-super.webp)

Figure 1. Nemotron 3 Super 120B-A12B combines Latent MoE with multi-token prediction and a hybrid
Mamba-Transformer stack. The routed experts operate after a 4096-to-1024 projection
(Original source
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)).

Basic idea

Run the selected experts in a narrower latent space

Compression

Nemotron 3: 4x  
Kimi K3: 2x

Example architectures

[Nemotron 3 Super 120B-A12B](https://sebastianraschka.com/llm-architecture-gallery/#card-nemotron-3-super-120b-a12b)  
[Nemotron 3 Ultra 550B-A55B](https://sebastianraschka.com/llm-architecture-gallery/#card-nemotron-3-ultra-550b-a55b)  
[Kimi K3](https://sebastianraschka.com/llm-architecture-gallery/#card-kimi-k3)

## From regular MoE to Latent MoE

An MoE, or Mixture of Experts, is an ensemble model that combines several smaller “expert” subnetworks inside the GPT-like decoder architecture. A router assigns each token to a subset of these experts. The idea here is that by using multiple smaller subnetworks instead of one large network, MoEs aim to allocate computational resources more efficiently.

“Sparse” in the context of a “Sparse Mixture of Experts” refers to the fact that at any given time, only a subset of the expert layers are actively used for processing a token.

In a regular MoE layer, the routed experts operate directly at the model width. In Latent MoE, the routed path is first projected down into a smaller latent space, the experts operate there, and the result is projected back up.

Routing and the latent bottleneck affect different parts of the computation. Routing controls how many experts run. The bottleneck controls the width at which the selected experts run. The projection layers also cost compute, so a 4x narrower latent space does not imply a 4x speedup for the whole model.

## Scaling the bottleneck in Nemotron 3

The part I find most interesting is the Latent MoE idea introduced in Nemotron 3 Super.

For Super, this was `4096 -> 1024 -> 4096`. For Ultra, it is `8192 -> 2048 -> 8192`.

So the 4x compression ratio stays the same, but the model is scaled up substantially. Super has 120B total and 12B active parameters. Ultra grows to 550B total and 55B active parameters while retaining the same bottleneck ratio.

## Kimi K3’s Stable LatentMoE

The one new component compared to Kimi Linear is the LatentMoE. I omitted it in the Kimi K3 overview figure since it was already very crowded, but that’s essentially the same idea as in Nemotron 3 Ultra. The idea here is to compress (down-project) large linear layers similar to [multi-head latent attention](https://sebastianraschka.com/llm-architecture-gallery/mla/).

Kimi K3 uses a `7168 -> 3584 -> 7168` path. This halves the width, giving it a 2x bottleneck instead of Nemotron’s 4x bottleneck. Moonshot calls it Stable LatentMoE. It also applies RMSNorm before the up-projection, uses SiTU-GLU activations, and routes each token to 16 of 896 experts with Quantile Balancing.

Sources

[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
[LLMs-from-scratch MoE chapter](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/07_moe)
[Nemotron 3 Ultra note](https://sebastianraschka.com/blog/2026/nemotron-3-ultra-latent-moe.html)
[Kimi K3 technical report](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
