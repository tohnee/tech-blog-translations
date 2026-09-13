---
title: "GQA vs. sliding-window attention"
source: https://sebastianraschka.com/faq/docs/when-gqa-and-swa.html
crawled: 2026-09-06
---

# GQA vs. sliding-window attention

Use **grouped-query attention (GQA)** alone when the model can afford full attention over its target context and the main bottleneck is KV-cache capacity or bandwidth. Add **sliding-window attention (SWA)** when the number of retained token positions still makes full attention too expensive.

The two mechanisms reduce different dimensions of attention cost. GQA stores fewer key and value heads at every retained position. SWA lets a local layer discard positions older than its window. They can be used independently or together.

## GQA preserves full-context access

Standard multi-head attention uses the same number of query and key-value heads. GQA keeps many query heads and shares a smaller set of key and value heads across them. A layer with 32 query heads and 8 KV heads assigns four query heads to each key-value pair.

For one layer and one retained token, the logical cache size is

`2 x KV heads x head dimension x bytes per element`

The factor 2 accounts for the key and value tensors. Reducing the KV-head count from 32 to 8 cuts this part of the cache by a factor of four. The same reduction applies at every context length.

![Grouped-query attention reduces KV-cache growth by storing fewer key and value heads for every retained token](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/gqa-memory/3.webp)

Every query head can still attend to every retained token. GQA therefore preserves direct global lookup in each attention layer. This is useful for workloads that may need an exact detail from anywhere in the prompt, such as comparing distant sections of a document or tracing a symbol across a code repository.

GQA does not remove the sequence-length dependence of full attention. During prefill, the model still evaluates query-key interactions across the complete context. During decoding, each query still attends over the retained prefix. The smaller cache reduces memory traffic, but the number of accessible token positions continues to grow.

The [GQA FAQ](https://sebastianraschka.com/faq/docs/grouped-query-attention.html) explains the head sharing and cache calculation in more detail.

## SWA also limits retained token positions

In causal sliding-window attention, a query can access only the most recent (W) positions. Once the sequence length (T) exceeds (W), an efficiently implemented local layer computes about (TW) attention scores during prefill instead of (T^2). During decoding, that layer can evict keys and values older than the window.

For example, a local window of 4,096 positions limits the cache of that layer to 4,096 tokens even if the model processes a 32,768-token sequence. This reduces the retained-token term by a factor of eight at the end of that sequence.

![Sliding-window attention bounds the retained context of local layers, so its cache advantage grows after the sequence exceeds the window](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/swa-memory/4.webp)

The saving requires an appropriate implementation. A dense (T \times T) attention matrix with a local mask gives the correct values but keeps most of the full-attention work. A runtime that masks old tokens without evicting their KV entries also misses the cache-capacity benefit. The checkpoint, local-attention kernel, and cache manager all need to support the same window pattern.

SWA changes the model’s information path. One local layer cannot directly compare its current query with a token outside the window. Information can propagate through successive local layers, but this is different from direct content lookup over the complete prefix. Architectures often keep periodic global-attention layers for that reason.

## The cache equation gives a practical decision rule

For a model in which all attention layers have the same KV dimensions, the logical cache size is approximately

`2 x batch size x layers x retained tokens x KV heads x head dimension x bytes per element`

GQA reduces `KV heads`. SWA reduces `retained tokens` in local layers. A hybrid model with (L\_g) global layers, (L\_l) local layers, full context (T), and local window (W) has the following logical cache size:

`2 x batch size x KV heads x head dimension x bytes per element x (L_g x T + L_l x min(T, W))`

This formula makes the choice easier to evaluate.

- **GQA is enough** if the resulting full-context cache fits the memory budget, decode bandwidth is acceptable, and full-attention prefill meets the latency target.
- **Add SWA** if long sequences still exceed the cache budget, reduce serving batch size too much, or make prefill and decoding attention too expensive.
- **Keep more global layers** if evaluations show that exact long-range retrieval degrades under a mostly local schedule.
- **Use a more local schedule** if the workload is dominated by nearby context and additional global layers provide little measured benefit.

The threshold depends on the complete workload. Context length, concurrent sequences, output length, precision, hardware memory, and latency targets all contribute. A 128K context advertised by a model does not mean that 128K is economical for the intended batch size.

## How the options compare

| Design | KV heads per token | Positions retained per layer | Direct reach of one layer | Main advantage |
| --- | --- | --- | --- | --- |
| Full MHA | Same as query heads | Full context | Full context | Maximum per-head KV capacity |
| Full GQA | Fewer than query heads | Full context | Full context | Smaller cache with global access preserved |
| MHA with SWA | Same as query heads | Local window in local layers | Local window | Fewer token positions and attention scores |
| GQA with SWA | Fewer than query heads | Local window in local layers | Local window | Reduces both cache dimensions |

This comparison also shows why GQA and SWA are not competing replacements. One can reduce the cache by four times through KV-head sharing and by another eight times in a local layer whose context is eight times longer than its window. Relative to full MHA at that context, the local layer’s logical cache is then 32 times smaller.

## When the quality tradeoff matters

GQA usually makes a milder architectural change because every query retains access to the full context. The original [GQA paper](https://arxiv.org/abs/2305.13245) found that intermediate KV sharing could approach multi-head-attention quality while retaining much of the inference benefit of multi-query attention in its evaluated settings.

SWA introduces a locality bias. This can be a good match for natural language and code, where many useful dependencies are nearby. It can be a poor match for tasks that require frequent, exact retrieval from arbitrary earlier positions. Long-context evaluation should therefore include retrieval distance, multi-document comparison, and the actual local-to-global layer schedule instead of reporting only average perplexity.

Gemma 3 provides a concrete hybrid example. It uses GQA and places one global-attention layer after every five local layers, with a local window of 1,024 tokens. The [Gemma 3 report](https://arxiv.org/abs/2503.19786) found little perplexity change from this more aggressive local pattern in its reported ablation. That result applies to the tested model and setup; it does not guarantee equal performance on every long-range retrieval task.

## This choice belongs to the model architecture

For an existing checkpoint, GQA and SWA are generally not interchangeable serving switches. The projection shapes determine the KV-head count, and the attention pattern used during training determines how the model learned to move information between positions. Converting MHA to GQA usually requires additional training, while imposing a local window on a model trained for full attention changes its outputs.

If I were selecting a checkpoint, I would first calculate its per-sequence cache at the intended context and precision. I would then benchmark prefill latency, decode throughput, and concurrent batch size. If GQA meets those system targets, full attention keeps the simpler information path. If it does not, a GQA-plus-SWA checkpoint is a reasonable next choice, followed by retrieval tests inside and outside the local window.

The [sliding-window attention FAQ](https://sebastianraschka.com/faq/docs/sliding-window-attention.html) covers local masks, receptive fields, and implementation checks. The [KV-cache bottleneck FAQ](https://sebastianraschka.com/faq/docs/kv-cache-long-context-bottleneck.html) covers the serving-memory calculation across layers and concurrent sequences.
