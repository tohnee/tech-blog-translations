---
title: "Grouped-Query Attention (GQA) in Modern LLMs"
source: https://sebastianraschka.com/faq/docs/grouped-query-attention.html
crawled: 2026-09-06
---

# Grouped-Query Attention (GQA) in Modern LLMs

**Grouped-query attention (GQA)** keeps the usual set of query heads but uses fewer key and value heads. Several query heads therefore read from the same key-value pair. This reduces the size of the KV cache and the amount of cached data that must be read during autoregressive generation.

The head counts place GQA between two familiar endpoints. Standard multi-head attention (MHA) uses the same number of query and key-value heads. Multi-query attention (MQA) uses many query heads and a single key-value head. GQA uses more than one key-value head but fewer key-value heads than query heads.

For example, a layer may have 32 query heads and 8 key-value heads. Each key-value head is shared by a group of 4 query heads. The queries remain distinct, so every head can form its own attention weights.

![Grouped-query attention with four query heads and two key-value heads, where each key-value pair serves a group of two query heads](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/gqa-memory/1.webp)

The cache savings follow directly from the number of key-value heads. For one layer and one retained token, a standard attention cache stores a key and a value for every KV head:

`cache bytes = 2 x KV heads x head dimension x bytes per element`

With bf16 values, 8 KV heads, and a head dimension of 128, this is 4,096 bytes per layer and token. Qwen3 8B has 36 such layers, which gives 144 KiB of logical bf16 KV-cache growth per retained token. An MHA version with 32 KV heads and the same dimensions would require four times as much cache.

This matters most during decoding. Every generated token adds keys and values to the cache, and later decoding steps read the stored tensors. The memory requirement grows with context length and batch size. Reading a smaller cache can also reduce memory-bandwidth pressure, which is often a practical bottleneck in token-by-token generation.

![The KV-cache comparison shows how reducing the number of key-value heads lowers memory growth as the retained context becomes longer](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/gqa-memory/3.webp)

GQA still performs full attention over the retained sequence. It does not shorten the context, make the attention matrix sparse, or remove the sequence-length dependence of full attention. [Sliding-window attention](https://sebastianraschka.com/faq/docs/when-gqa-and-swa.html) changes how many earlier tokens remain available, so it addresses a different part of the cost.

Why stop between MHA and MQA? Sharing one key-value head across every query head provides the largest cache reduction, but it also removes more of the head-specific key-value capacity. The original 2023 [GQA paper](https://arxiv.org/abs/2305.13245) found that intermediate grouping could approach MHA quality while retaining much of MQA’s inference benefit in its evaluated settings. The exact tradeoff depends on the model and training recipe.

Llama 3 8B, Qwen3 8B, and Gemma 3 27B are examples of models that use GQA. Their query-to-KV head ratios differ, but the mechanism is the same. Multiple query heads retain separate attention patterns while sharing a smaller set of cached keys and values.
