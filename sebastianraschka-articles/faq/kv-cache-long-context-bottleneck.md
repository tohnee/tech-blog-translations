---
title: "Why Long Contexts Make the KV Cache a Memory Bottleneck"
source: https://sebastianraschka.com/faq/docs/kv-cache-long-context-bottleneck.html
crawled: 2026-09-06
---

# Why Long Contexts Make the KV Cache a Memory Bottleneck

The **KV cache** trades computation for memory. During autoregressive generation, each attention layer stores the key and value vectors from earlier tokens. Reusing them avoids running the full prefix through the key and value projections at every decoding step. The prompt fills the cache during prefill, and each generated token appends another entry.

![Attention reuses cached keys and values from earlier tokens while computing a new query for the current token](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/kv-cache/kv-cache-attn-1.png)

For a standard attention layer, the logical cache added by one token is:

`2 x KV heads x head dimension x bytes per element`

The factor 2 accounts for the key and value tensors. Multiply this amount by the cache-producing layers, retained tokens, and active sequences. Queries are computed for the current step and are not stored in the growing cache.

The scaling becomes large quickly. Qwen3 8B has 36 GQA layers, 8 KV heads per layer, and a head dimension of 128. With bf16 values, it adds 144 KiB of logical cache per token and sequence. A context of 32,768 tokens therefore occupies about 4.5 GiB. Eight equally long sequences need about 36 GiB before allocator overhead, temporary buffers, and other serving state.

This is different from model-weight memory. A server can share one loaded copy of the weights across requests, while every active sequence has its own KV cache. Longer contexts and larger continuous batches therefore reduce how many requests fit on the same accelerator.

The cache also affects decoding speed. At each step, attention reads the retained keys and values to compare them with the new query. A larger cache increases memory traffic and the attention work for each generated token. The cache avoids recomputing the prefix, but it does not make a long prefix free.

![The GQA memory curves show the linear growth of KV-cache storage with retained context length and the reduction from using fewer KV heads](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/gqa-memory/3.webp)

Several optimizations reduce different factors in the calculation. [Grouped-query attention](https://sebastianraschka.com/faq/docs/grouped-query-attention.html) and multi-query attention reduce the number of KV heads. Lower-precision caches reduce the bytes per element. Sliding-window attention or cache eviction limits the number of retained tokens. Cross-layer KV sharing reduces how many layers create distinct cache entries, while multi-head latent attention stores a compressed representation.

Memory-management methods such as paged attention improve allocation and reduce fragmentation. They help a serving system pack requests efficiently, although they do not change the model’s logical cache size for a given sequence.

The KV cache grows linearly with retained context length. Other long-context costs follow different scaling rules. Full-attention prefill has quadratic attention work in the sequence length, and decoding attention work per new token grows linearly with the retained prefix. These costs should be measured separately from the cache-capacity calculation.

The [gallery calculation page](https://sebastianraschka.com/llm-architecture-gallery/kv-cache-calculations/) reports logical bf16 cache growth per token so architectures can be compared under one convention. Measured runtime memory may differ because of cache quantization, padding, allocator behavior, and kernel-specific layouts.
