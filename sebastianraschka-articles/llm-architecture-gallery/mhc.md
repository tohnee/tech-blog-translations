---
title: "Manifold-constrained hyper-connections"
source: https://sebastianraschka.com/llm-architecture-gallery/mhc/
crawled: 2026-09-06
---

# Manifold-constrained hyper-connections

Manifold-constrained hyper-connections (mHC) change the residual connections inside a transformer block. They replace the single residual stream with several parallel residual streams and learned mappings between them, then constrain those mappings to keep signal mixing stable.

This goes back to a research paper that the DeepSeek team shared on 31 Dec 2025. However, in this paper, the technique was only tested on an experimental 27B scale model. Now, we see it in their flagship release, which is a good sign that this idea actually works well in production.

The main idea behind mHC here is to modernize the design of the residual connections inside the transformer block, which is refreshing, because architecture tweaks are usually focused on the attention mechanism, normalization layer placement, and MoE parts.

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[Gated Residuals](https://sebastianraschka.com/llm-architecture-gallery/gated-residuals/)
[Article section](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures#%C2%A751-manifold-constrained-hyper-connections-mhc)
[mHC paper](https://arxiv.org/abs/2512.24880)
[Hyper-connections paper](https://arxiv.org/abs/2409.19606)

![DeepSeek V4-Pro architecture with mHC mixers](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/deepseek-v4-mhc-architecture.webp)

Figure 17. DeepSeek V4-Pro places mHC mixers around the attention and MoE sublayers. The model uses
4 parallel residual streams while keeping the attention and MoE sublayers at their normal hidden width
(Original source
[*Recent Developments in LLM Architectures*](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures)).

## From residual connections to hyper-connections

mHC is based on previous work on hyper-connections by Zhu et al. from 2024. Hyper-connections essentially modify the single residual stream inside the transformer block by replacing it with several parallel residual streams and learned mappings between them.

(For those new to residual connections, I made a [video on residual neural networks](https://www.youtube.com/watch?v=q_IlqYlYhlo) many years ago, where I explained the general mechanism.)

The idea behind hyper-connections is to widen the residual stream. We can think of this as keeping several parallel residual streams, with an additional Res Mapping linear transformation that mixes them across layers. Since the attention or MoE layer itself still operates on the normal hidden size, hyper-connections also add a Pre Mapping that combines the parallel residual streams into one normal hidden vector for the layer, and a Post Mapping that distributes the layer output back across the parallel residual streams.

![Regular transformer block compared with a transformer block using hyper-connections](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/mhc-hyper-connections.webp)

Figure 18. Regular transformer block compared with a transformer block using hyper-connections. Pre Mapping
reads from the widened state, the sublayer runs at the normal width, and Post Mapping writes the output
back into the widened state (Original source
[*mHC: Manifold-Constrained Hyper-Connections*](https://arxiv.org/abs/2512.24880)).

The figure focuses on the attention-layer portion of the transformer block, but the same concept applies to the second residual branch around the MoE layer.

The purpose of hyper-connections is to make the residual pathway more expressive without making the actual attention or MoE layer wider. This is only mildly more expensive in FLOPs because the extra mappings operate over the small residual-stream axis, for example, n = 4 in DeepSeek V4, not over a huge hidden dimension.

In the original hyper-connections paper, the 7B OLMo MoE experiment goes from 13.36G to 13.38G FLOPs per token, which is basically unchanged. In terms of reported gains, there were modest (but consistent) improvements.

(However, only looking at FLOPs is a bit simplistic. The widened residual state still has to be stored, moved through memory, mixed, etc. So the practical overhead can come more from memory traffic and implementation complexity than from arithmetic, which is not explicitly measured.)

## How Attention Residuals and mHC differ

Both methods change the residual path, but they do it in different directions.

- Attention Residuals: select and combine outputs from earlier depths.
- mHC: maintain and mix several residual streams at the current depth.

[Attention Residuals](https://sebastianraschka.com/llm-architecture-gallery/attention-residuals/) use learned attention weights over earlier sublayer outputs for the same token. mHC keeps several residual streams at the current depth and constrains how those streams exchange information.

## What the manifold constraint adds

The main change from regular hyper-connections (HC) to manifold-constrained hyper-connections (mHC) is that the mappings are no longer left unconstrained. In regular HC, the Res Mapping is a learned matrix that mixes the parallel residual streams, but stacking many such matrices can amplify or shrink signals unpredictably.

In mHC, this residual mapping is projected onto the manifold of doubly stochastic matrices, meaning all entries are non-negative and each row and column sums to 1. This makes the residual mixing behave more like a stable redistribution of information across streams. The Pre Mapping and Post Mapping are also constrained to be non-negative and bounded, which avoids cancellation when reading from and writing back into the widened residual state.

![Hyper-connections compared with manifold-constrained hyper-connections](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/mhc-manifold-constraint.webp)

Figure 20. mHC keeps the parallel residual streams from hyper-connections but constrains the stream-mixing
weights. The Res Mapping becomes doubly stochastic, while the Pre Mapping and Post Mapping are bounded
and non-negative (Original source
[*mHC: Manifold-Constrained Hyper-Connections*](https://arxiv.org/abs/2512.24880)).

In the mHC paper, using a 27B parameter model for the experiments, the DeepSeek team’s optimized implementation (with fusion, recomputation, and pipeline scheduling) adds only 6.7% additional training time overhead for 4 residual streams (n = 4) throughout all transformer blocks compared to the single-stream baseline.

To sum up, HC/mHC changes how information is carried around these layers by replacing the single residual stream with several interacting residual streams, with additional stability constraints in mHC. It pairs with the CSA/HCA attention changes, which modify other parts of the transformer block.

Sources

[Recent Developments in LLM Architectures](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures#%C2%A751-manifold-constrained-hyper-connections-mhc)
[mHC paper](https://arxiv.org/abs/2512.24880)
[Hyper-connections paper](https://arxiv.org/abs/2409.19606)
[DeepSeek V4 technical report](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/DeepSeek_V4.pdf)
[DeepSeek V4-Pro config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/config.json)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
