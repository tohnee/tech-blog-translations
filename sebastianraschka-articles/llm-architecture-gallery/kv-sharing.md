---
title: "Cross-Layer KV Sharing"
source: https://sebastianraschka.com/llm-architecture-gallery/kv-sharing/
crawled: 2026-09-06
---

# Cross-Layer KV Sharing

Cross-layer KV sharing is a shared KV cache scheme where later layers reuse key-value states from earlier layers. This reduces long-context memory and compute because fewer layers add their own keys and values to the cache.

This KV-sharing idea was not invented by Gemma 4. For instance, see Brandon *et al.*, [*Reducing Transformer Key-Value Cache Size with Cross-Layer Attention*](https://arxiv.org/abs/2405.12981) (NeurIPS 2024). But it’s the first popular architecture where I saw this concept applied. (Cross-layer attention is not to be confused with cross-attention.)

[Grouped-query attention (GQA)](https://sebastianraschka.com/llm-architecture-gallery/gqa/) already shares key-value heads across different query heads. Cross-layer KV sharing applies the sharing across transformer layers instead.

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[From-scratch code](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/10_kv-sharing)
[KV-cache calculations](https://sebastianraschka.com/llm-architecture-gallery/kv-cache-calculations/)

![Cross-layer KV sharing in Gemma 4](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gemma4-kv-sharing.webp)

Cross-layer KV sharing keeps query projections layer-local while reusing K/V tensors from selected producer
layers. The cache grows only for the producer layers, which lowers long-context memory use (Original source
[*LLMs-from-scratch* KV-sharing materials](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/10_kv-sharing)).

What changes

Only selected layers produce new key and value tensors for the cache

Practical benefit

It compounds with MQA or GQA because it reduces the number of cache-producing layers

Example architectures

[Gemma 4 E2B](https://sebastianraschka.com/llm-architecture-gallery/#card-gemma-4-e2b) and
[Gemma 4 E4B](https://sebastianraschka.com/llm-architecture-gallery/#card-gemma-4-e4b)

## Why reduce the KV cache?

Before explaining KV-sharing further, let’s briefly talk about the motivation. One of the main recent themes in LLM architecture design is KV cache size reduction. In turn, the motivation behind KV cache size reduction is to reduce the required memory, which allows us to work with longer contexts. For more background, see my [Understanding and Coding the KV Cache in LLMs from Scratch](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms) article.

To pick a classic example (that Gemma 4 still uses): GQA already shares key-value heads across different query heads to reduce the KV cache size. Multi-query attention (MQA) is the one-KV-head special case of GQA.

In regular attention with a KV cache, each attention layer stores one key tensor and one value tensor for every generated token. Cross-layer KV sharing changes the layer count in that calculation. Instead of caching K/V tensors for every layer, only the K/V-producing layers add entries to the cache.

For a standard KV cache:

```python
bytes = batch_size x seqlen x head_dim x n_kv_heads x n_layers x 2 x bytes_per_elem
```

With cross-layer KV sharing:

```python
bytes = batch_size x seqlen x head_dim x n_kv_heads x n_kv_producing_layers x 2 x bytes_per_elem
```

The rest of the transformer layer is still present. The second expression simply replaces the total layer count with the number of layers that produce new keys and values.

## How Gemma 4 applies KV sharing

As mentioned before, Gemma 4 uses GQA. However, in addition to the KV sharing among queries as part of GQA, Gemma 4 also shares KV projections across different layers instead of computing them as part of the attention module in each layer. This KV-sharing scheme is also called cross-layer attention.

In the case of GQA (or MQA), the KV-sharing works like this. Later layers no longer compute their own key and value projections but reuse the KV tensors from the most recent earlier non-shared layer of the same attention type. In other words, sliding-window layers share KV with a previous sliding-window layer. Full-attention layers share KV with a previous full-attention layer. The layers still compute their own query projections, so each layer can form its own attention pattern, but the expensive and memory-heavy KV cache is reused across several layers.

For example, Gemma 4 E2B has 35 transformer layers, but only the first 15 compute their own KV projections; the final 20 layers reuse KV tensors from the most recent earlier non-shared layer of the same attention type. Similarly, Gemma 4 E4B has 42 layers, with 24 layers computing their own KV and the final 18 layers sharing them.

How much does this actually save? Since Gemma 4 shares roughly half of the KVs across layers, it saves approximately half of the cache that remains after applying MQA or GQA. For E2B, this is about 2.7 GB at bfloat16 precision and a 128k context. For E4B, it is about 6 GB.

The plots below show the combined savings relative to an MHA baseline. At a 128k context and batch size 1, the E2B-like setup goes from 37.58 GB for MHA to 2.01 GB for MQA plus KV sharing. The E4B-like setup goes from 56.37 GB for MHA to 8.05 GB for GQA plus KV sharing. The plots don’t include the additional retained-cache savings from sliding-window attention.

![KV-cache memory comparison for a Gemma 4 E2B-like setup](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/kv-sharing-gemma4-e2b-memory.webp)

In the E2B-like setup, one KV head and 15 K/V-producing layers reduce the full-context cache from a
37.58 GB MHA baseline to 2.01 GB at 128k tokens, before counting sliding-window retention savings
(Original source [*LLMs-from-scratch* KV-sharing materials](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/10_kv-sharing)).

![KV-cache memory comparison for a Gemma 4 E4B-like setup](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/kv-sharing-gemma4-e4b-memory.webp)

In the E4B-like setup, two KV heads and 24 K/V-producing layers reduce the full-context cache from a
56.37 GB MHA baseline to 8.05 GB at 128k tokens, before counting sliding-window retention savings
(Original source [*LLMs-from-scratch* KV-sharing materials](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/10_kv-sharing)).

## The tradeoff

The downside of KV-sharing is, of course, that it is an approximation of the real thing. Or, more precisely, it reduces model capacity. Some layers now attend through reused K/V tensors rather than layer-specific ones.

However, the [cross-layer attention paper](https://arxiv.org/abs/2405.12981) reports that the impact can be minimal for the small models it tested. Gemma 4 combines this idea with MQA or GQA and sliding-window attention. Each method reduces a different part of the KV-cache cost.

Sources

[Brandon et al. (2024), *Reducing Transformer Key-Value Cache Size with Cross-Layer Attention*](https://arxiv.org/abs/2405.12981)
[LLMs-from-scratch KV-sharing materials](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/10_kv-sharing)
[Gemma 4 model card](https://ai.google.dev/gemma/docs/core/model_card_4)
[KV cache / token gallery calculations](https://sebastianraschka.com/llm-architecture-gallery/kv-cache-calculations/)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
