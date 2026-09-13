---
title: "Per-Layer Embeddings (PLE)"
source: https://sebastianraschka.com/llm-architecture-gallery/per-layer-embeddings/
crawled: 2026-09-06
---

# Per-Layer Embeddings (PLE)

The Gemma 4 E2B and E4B variants include a second efficiency-oriented design choice called per-layer embeddings (PLE). This is separate from the [cross-layer KV-sharing](https://sebastianraschka.com/llm-architecture-gallery/kv-sharing/) scheme.

KV sharing reduces the KV cache. PLE is instead about parameter efficiency, where it lets the small Gemma 4 models use more token-specific information without making the main transformer stack as expensive as a dense model with the same total parameter count.

For instance, the “E” in Gemma 4 E2B and E4B stands for “effective”. Concretely, Gemma 4 E2B is listed as 2.3B effective parameters, or 5.1B parameters when the embeddings are counted. Similarly, Gemma 4 E4B is listed as 4.5B effective parameters, or 8B parameters with embeddings.

In short, in the “E” models, the main transformer-stack compute is closer to the smaller number, while the larger number includes the additional embedding-table layers.

Conceptually, the new PLE path looks like this.

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[Article section](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures#%C2%A72-per-layer-embeddings-and-effective-size-gemma-4-e2be4b)
[From-scratch code](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch05/17_gemma4)

![Simplified Gemma 4 block with the per-layer embedding residual path](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gemma4-ple-residual-path.webp)

Figure 6: Simplified Gemma 4 block with the PLE residual path. The normal block first computes the attention
and feed-forward residual updates. The resulting hidden state gates the layer-specific PLE vector, and the
projected PLE update is added as an extra residual update at the end of the block.

## How the PLE path works

The PLE vectors themselves are prepared outside the repeated transformer blocks. First, the token IDs go through a per-layer embedding lookup. Second, the normal token embeddings go through a linear projection into the same packed PLE space. These two pieces are added, scaled, and reshaped into a tensor with one slice per layer.

Inside the transformer block, the regular attention and feed-forward branches run as usual. The resulting hidden state gates the layer-specific PLE vector. That vector is then projected back to the model hidden size, normalized, and added as one extra residual update.

![Simplified construction of Gemma 4 per-layer embeddings](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gemma4-ple-construction.webp)

Figure 7: The token IDs provide a per-layer embedding lookup, while the normal
token embeddings are projected into the same space. The two contributions are combined and reshaped so that
each transformer block receives its own layer-specific PLE slice.

## Why use PLE?

We have to take Google’s word here that this is an effective and worthwhile design choice. It would be interesting to see how E2B compares with a regular 2.3B model and a regular 5.1B model.

Also, PLE is not inherently limited to small models. We could attach per-layer embedding slices to larger models, too. However, larger models may already have sufficient capacity where these extra embeddings would not help much. For larger models, we also have MoE designs as a way to increase capacity while keeping the compute footprint smaller.

By the way, if you are interested in a relatively simple and readable code implementation, I implemented the Gemma 4 E2B and E4B models from scratch [here](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch05/17_gemma4).

Sources

[Recent Developments in LLM Architectures](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures#%C2%A72-per-layer-embeddings-and-effective-size-gemma-4-e2be4b)
[Gemma 4 model card](https://ai.google.dev/gemma/docs/core/model_card_4)
[LLMs-from-scratch Gemma 4 materials](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch05/17_gemma4)
[Embedding layers vs. linear layers notebook](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch02/03_bonus_embedding-vs-matmul/embeddings-and-linear-layers.ipynb)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
