---
title: "RoPE vs. absolute positional embeddings"
source: https://sebastianraschka.com/faq/docs/rope-vs-absolute-positional-embeddings.html
crawled: 2026-09-06
---

# RoPE vs. absolute positional embeddings

**RoPE**, short for **rotary position embeddings**, encodes position by rotating query and key vectors inside self-attention. Learned absolute positional embeddings take a more direct approach. They learn one vector for every position and add it to the token embedding before the first transformer block.

RoPE became common in modern LLMs because it gives the query-key interaction a useful relative-position structure and avoids a fixed learned position table. It can evaluate position indices beyond those used during training, although this alone does not guarantee that the model will work well at longer lengths.

The learned absolute approach used by GPT-2 can be written as

\[h\_t = E\_{\text{token}}(x\_t) + P\_t.\]

Here, \(E\_{\text{token}}(x\_t)\) is the token embedding and \(P\_t\) is the learned vector for position \(t\). The two vectors have the same width. Their sum becomes the residual-stream input to the first transformer block.

![The GPT-style input adds one learned position vector to each token embedding.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch02_compressed/18.webp)

The position table has shape `maximum context length` by `embedding dimension`. GPT-2 small, for example, has 1,024 position vectors of width 768, which adds 786,432 parameters. The table is easy to understand and cheap to use. It also creates a hard architectural boundary. Position 1,024 has no row in a table that ends at position 1,023.

Increasing the table size solves the tensor-shape problem but leaves the new rows untrained. An implementation has to initialize, interpolate, or learn them through additional training. The model may also have learned behavior tied to the absolute indices it observed during pretraining.

RoPE moves the position operation from the model input into every attention layer. Within each attention head, adjacent query and key features are treated as two-dimensional pairs. A rotation matrix \(R\_t\) turns each pair by an angle determined by position \(t\) and a channel-specific frequency:

\[q'\_t = R\_t q\_t, \qquad k'\_t = R\_t k\_t.\]

The values are usually left unchanged. Attention then uses the dot product between a rotated query at position \(m\) and a rotated key at position \(n\):

\[(R\_m q\_m)^\mathsf{T}(R\_n k\_n)
= q\_m^\mathsf{T} R\_{n-m} k\_n.\]

The second form follows from the rotation matrices. It shows why RoPE is associated with relative position. The positional term in the attention score depends on the offset \(n-m\), including its direction, rather than requiring a separately learned vector for every absolute slot. The rotated query and key still have position-specific phases, so describing RoPE as purely relative would be slightly misleading.

| Property | Learned absolute embeddings | RoPE |
| --- | --- | --- |
| Applied to | Token embeddings before the first block | Queries and keys in attention |
| Position parameters | One learned vector per supported position | Usually none |
| Relative offset in the query-key score | Must be learned from the added vectors | Built into the rotation identity |
| Positions beyond the configured table | Undefined until the table is extended | Angles can be computed, but quality is not guaranteed |
| Attention complexity | Unchanged | Unchanged |

RoPE uses several rotation frequencies across the head dimension. High-frequency pairs change quickly between nearby positions, while low-frequency pairs change more slowly. The base frequency, head dimension, and fraction of rotated channels are architecture choices. Some models apply RoPE to every query and key channel. Others use partial RoPE and leave part of each head unchanged.

![The GPT-to-Llama progression replaces the learned input position table with RoPE inside attention.](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/gpt-to-llama/gpt2-to-llama2-llama3.webp)

Long-context claims need care. RoPE can generate rotations for position 100,000 without allocating 100,000 learned position vectors. A model trained only on much shorter sequences has not necessarily learned to use those unfamiliar phases. Retrieval accuracy and language-model loss can deteriorate even though the forward pass runs successfully.

Methods such as position interpolation, frequency-base changes, NTK-aware scaling, and YaRN adjust the RoPE frequencies for a longer target context. Continued training on longer sequences can help the model adapt as well. The exact scaling recipe is part of the model configuration, and the same label “RoPE” can therefore describe models with different long-context behavior.

RoPE does not change the quadratic cost of full attention. It adds inexpensive elementwise rotations, while the query-key matrix and the attention probabilities still grow with sequence length. It also does not reduce KV-cache size. During autoregressive generation, implementations usually rotate a key using its position ID before storing it in the cache. Incorrect position IDs, especially with padding or a reused cache, can silently give the model the wrong relative offsets.

The move from GPT-2-style absolute embeddings to RoPE is therefore a change in how attention represents position. RoPE supplies relative-offset structure without a learned position table and is easier to adapt to new context lengths. Actual extrapolation still depends on the frequencies, training lengths, scaling method, and evaluation task.

For the broader motivation, see [Why do transformers need positional information?](https://sebastianraschka.com/faq/docs/positional-information-transformer.html). The FAQ [What architectural changes turned GPT-style models into Llama-style models?](https://sebastianraschka.com/faq/docs/gpt-style-to-llama-style.html) places RoPE alongside the other GPT-to-Llama component changes. The original method was introduced in the [RoFormer paper](https://arxiv.org/abs/2104.09864).
