---
title: "What is a KV cache, and why does it make LLM inference faster?"
source: https://sebastianraschka.com/faq/docs/kv-cache.html
crawled: 2026-09-06
---

# What is a KV cache, and why does it make LLM inference faster?

A **KV cache** stores the key and value tensors produced by every attention layer for the tokens already in an autoregressive sequence. The cache lets the model reuse this layer-specific state instead of recomputing the complete prefix after each new token.

Consider the prompt `"Time flies"`. During **prefill**, the model processes both prompt tokens and stores their keys and values at every cache-producing layer. The final prompt representation produces logits for the next token.

![Prefill computes the key and value vectors for the prompt tokens and stores one pair at every attention layer](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/kv-cache/kv-cache-attn-1.png)

Suppose the decoding rule selects `"fast"`. On the next model call, the input can be just that new token together with the cache for `"Time flies"`. Each layer computes a query, key, and value for `"fast"`. Its query attends to the cached keys and values plus the new pair, and the new key and value are appended to the cache. The resulting logits predict the token after `"fast"`.

![The earlier key-value pairs remain unchanged when the new token is appended, so only the new pair has to be computed](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/kv-cache/kv-cache-attn-2.png)

Without caching, that second call would run `"Time flies fast"` through the entire model again. The hidden states and attention projections for `"Time"` and `"flies"` would repeat work from prefill. The same redundancy grows at every later step.

![The uncached path recomputes the prefix, while the cached path retrieves earlier keys and values and extends them with the newest token](https://sebastianraschka.com/images/blog/2025/coding-the-kv-cache-in-llms/8.png)

Queries are usually absent from the growing cache. A query represents the token whose attention output is being computed at the current step. Future tokens need earlier keys and values as the items they can attend to, but they do not reuse earlier queries.

The speedup has a boundary. The new query still has to interact with all retained keys and values in a full-attention layer. Caching removes repeated prefix projections and repeated processing of earlier token states. It does not remove the attention work or memory traffic over the retained prefix. This remaining cost becomes important at long context lengths.

A basic implementation keeps `cache_k` and `cache_v` tensors in each attention block. The tensors have a sequence dimension that grows as decoding proceeds. The implementation also tracks the absolute cache position so the causal mask and positional encoding, such as RoPE, line up with the stored prefix.

![The from-scratch implementation adds per-layer cache buffers, appends the newest keys and values, and tracks the current cache position](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/kv-cache/new-sections.png)

Independent generation requests normally start with an empty cache because their prefixes differ. Serving systems can reuse cached state for an identical shared prompt, but only when the model, tokenization, positions, and prefix tokens match.

KV caching is primarily an inference optimization. During causal-language-model training, the known sequence positions are processed together in one masked forward pass, and training needs activations for backpropagation. There is no repeated token-by-token prefix evaluation to eliminate.

The tradeoff is memory. Every retained token adds state for the relevant layers and KV heads of each active sequence. The [long-context KV-cache FAQ](https://sebastianraschka.com/faq/docs/kv-cache-long-context-bottleneck.html) gives the memory formula and a concrete Qwen3 8B calculation.
