---
title: "What role does positional information play in a transformer-based LLM?"
source: https://sebastianraschka.com/faq/docs/positional-information-transformer.html
crawled: 2026-09-06
---

# What role does positional information play in a transformer-based LLM?

Positional information lets a transformer distinguish the same token content at different sequence locations and represent order, direction, and distance. These distinctions matter because “dog bites man” and “man bites dog” contain the same three tokens but express different events.

The precise issue is that plain, unmasked self-attention without any position-dependent input is **permutation-equivariant**. If the input tokens are permuted, the output representations are permuted in the same way. Attention can compare token content, but it has no coordinate that says one token occurred before another or that two tokens were three positions apart.

This is sometimes described as permutation invariance, although equivariance is the more accurate term. The sequence output is still reordered when the input is reordered. What is missing is sensitivity to the meaning of that order.

A token embedding lookup illustrates the problem. The token ID for “dog” maps to the same vector whether it appears at position 1 or position 100. Repeated occurrences also begin with the same token vector. A position mechanism gives the network additional information for telling these cases apart.

![A token embedding identifies token content but does not, by itself, identify the token's sequence position.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch02_compressed/17.webp)

The small GPT-style model implemented in the repo uses **learned absolute positional embeddings**. For token (x\_t) at position (t), the transformer input is

[
z\_t = E\_{\text{token}}(x\_t) + E\_{\text{position}}(t).
]

The token table supplies content, while the position table supplies a learned vector for index (t). The two vectors have the same width and are added before the first transformer block.

![The GPT-style input adds one learned position vector to each token embedding.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch02_compressed/18.webp)

Absolute embeddings are easy to inspect and implement. A learned table also creates a hard architectural limit because it contains only a fixed number of position rows. Extending the table introduces positions that were not trained. Fixed sinusoidal encodings, used in the original Transformer, avoid a learned lookup table but still add an absolute position-dependent vector at the input.

Modern LLMs use several other approaches:

- **Rotary position embeddings (RoPE)** rotate pairs of query and key channels by angles determined by their positions. The resulting query-key dot product depends on the relative offset between tokens.
- **Relative position biases** add a learned or fixed term to attention scores based on the distance and direction between a query and a key. T5-style bucketed biases and ALiBi are examples.
- **Partial or hybrid schemes** apply a position method only to some channels or layers. Different attention layers can therefore use different positional treatments.
- **NoPE** omits an explicit position embedding, rotation, or bias from selected attention layers.

RoPE differs structurally from the GPT-style approach because it does not add a position vector to the residual-stream input. It modifies queries and keys inside attention. This gives attention a direct representation of relative offsets while retaining absolute phase information in the rotated vectors. [What is RoPE, and why did many models move away from learned absolute positional embeddings?](https://sebastianraschka.com/faq/docs/rope-vs-absolute-positional-embeddings.html) covers that mechanism in more detail.

These approaches also differ in how they behave beyond the context lengths seen during training. A model can technically evaluate RoPE at larger position indices, but good long-context behavior is not automatic. RoPE scaling, interpolation, additional training, and the frequency configuration can all matter. Relative biases have their own extrapolation behavior, and learned absolute tables must be resized or otherwise adapted.

Decoder-only LLMs add one important nuance. Their [causal attention mask](https://sebastianraschka.com/faq/docs/causal-attention.html) already supplies a directional structural signal. Position (t) can read only positions up to (t), so different locations have different visible prefixes. This breaks the full permutation symmetry of unmasked attention and explains how a causal model can learn some order information without explicit positional embeddings.

NoPE uses this observation. A NoPE attention layer receives no absolute embedding and applies no RoPE or explicit relative bias, while the causal mask remains. The model can learn from the nested prefix structure, although it has no direct coordinate for exact positions or distances. Some recent architectures mix RoPE and NoPE layers rather than using one choice throughout. The [NoPE gallery explainer](https://sebastianraschka.com/llm-architecture-gallery/nope/) discusses this setup and the current evidence for length generalization.

Position handling also matters in the implementation of generation. Each newly decoded token needs the next position index, and cached keys and values must retain the position treatment used when they were created. Batched sequences with different padding or cache lengths need consistent position IDs. An indexing mistake can produce plausible tensor shapes while silently changing the attention relationships.

Positional information therefore tells the transformer how token relationships depend on sequence location. The architecture may add vectors, rotate attention features, bias attention scores, or rely partly on causal structure. The right description depends on the exact model rather than on the family name alone.
