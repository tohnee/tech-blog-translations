---
title: "KV Cache / Token (bf16)"
source: https://sebastianraschka.com/llm-architecture-gallery/kv-cache-calculations/
crawled: 2026-09-06
---

# KV Cache / Token (bf16)

KV-cache numbers are easy to compare incorrectly. The `144 KiB` listed for Qwen3 8B, for example, is the logical cache added by one token for one sequence. The gallery uses bf16 ([16-bit bfloat](https://en.wikipedia.org/wiki/Bfloat16_floating-point_format)), so every cached element occupies 2 bytes.

During autoregressive generation, an attention layer reuses the keys and values from earlier tokens. Keeping these tensors avoids recomputing them at every decoding step. Prompt tokens populate the cache during prefill, and each decoded token appends another entry.

I chose a per-token value because it makes architectures with very different attention stacks comparable on one card. Runtime memory will usually be higher due to allocator padding, serving buffers, and kernel-specific layouts.

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[Memory calculator](https://sebastianraschka.com/llm-architecture-gallery/memory-calculator/)
[GQA](https://sebastianraschka.com/llm-architecture-gallery/gqa/)
[MLA](https://sebastianraschka.com/llm-architecture-gallery/mla/)
[Hybrid attention](https://sebastianraschka.com/llm-architecture-gallery/hybrid-attention/)

What it means

Logical cache added by one retained token

Fixed assumptions

Batch size 1, bf16, and 2 bytes per cached element

Important caveat

Logical architecture estimate, separate from measured serving memory

## Start with one attention layer

The most general form of the calculation is:

```python
bytes_per_layer_per_token
= cached_tensors × num_kv_heads × head_dim × bytes_per_element
```

Standard attention stores a key tensor and a value tensor, so `cached_tensors = 2`. With bf16, the formula becomes:

```python
bytes_per_layer_per_token
= 2 × num_kv_heads × head_dim × 2
= 4 × num_kv_heads × head_dim
```

The query-head count enters indirectly through the attention type. Multi-head attention (MHA) has one KV head per query head. Grouped-query attention (GQA) uses fewer KV heads, and multi-query attention (MQA) uses one. This is why GQA and MQA reduce the cache without changing the number of query heads.

For the model-wide value, I add the contribution from every distinct layer that produces cache tensors:

```python
bytes_per_model_per_token
= sum(bytes_per_layer_per_token across cache-producing layers)
```

![Comparison of float32, float16, and bfloat16 bit layouts](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/kv-cache-precision.webp)

**Figure 1.** Bfloat16 uses 16 bits per element, the same storage size as float16. Its exponent occupies 8 bits and its fraction occupies 7 bits. The gallery uses 2 bytes per cached bf16 value.

## Retention and sharing affect different factors

Sliding-window attention uses the same cost per stored token as its underlying MHA, GQA, or MQA layer. It changes how long a token remains in the cache. Once the window is full, an old entry can be removed when a new one arrives.

Cross-layer KV sharing changes the number of distinct cache-producing layers. A layer that reuses keys and values from an earlier layer does not append another pair of tensors. The [Gemma 4 E2B and E4B models](https://sebastianraschka.com/llm-architecture-gallery/kv-sharing/) use this approach.

Looped depth needs an additional recurrence factor when every pass retains its own cache. [Ouro-Thinking 2.6B](https://huggingface.co/ByteDance/Ouro-2.6B-Thinking/blob/main/modeling_ouro.py) maps each of its four passes to separate cache entries across the shared 48-layer stack:

```python
4 passes × 48 layers × 16 KV heads × 128 head_dim × 4
= 1,572,864 bytes
= 1.5 MiB per token
```

The Ouro paper also evaluates decoding-time cache reuse that retains only one pass, reducing this logical growth to `384 KiB/token`. The released Hugging Face implementation keeps the full four-pass cache by default.

Unified keys and values change the tensor count from two to one:

```python
bytes_per_layer_per_token
= num_kv_heads × head_dim × 2
= 2 × num_kv_heads × head_dim
```

Gemma 4’s global full-attention layers use unified `K=V`. These layers also have their own `global_head_dim`, so I calculate their contribution separately from the sliding-window layers. The reductions from GQA, retention windows, cross-layer sharing, and unified `K=V` describe different parts of the cache calculation.

## MLA stores a compressed latent

Multi-head latent attention (MLA) keeps a compressed KV latent and a separate rotary-key component. For DeepSeek-style MLA, the gallery uses the compact representation described by the architecture:

Per MLA layer:

```python
bytes_per_layer_per_token
= (kv_lora_rank + qk_rope_head_dim) × 2
```

Across the model, this gives:

```python
bytes_per_model_per_token
= num_mla_layers × (kv_lora_rank + qk_rope_head_dim) × 2
```

The cache now depends on the latent dimensions and the number of MLA layers. Query-head count no longer appears in this compact formula. A serving implementation that expands the latent into full key and value tensors will have a different memory footprint.

## Hybrids need a layer inventory

Hybrid models are where a single layer count becomes misleading. I count only the layers that append to a growing KV cache.

- Qwen3-Next and Qwen3.5 contribute cache through their full-attention layers.
- Kimi Linear and Ling 2.5/2.6 contribute cache through MLA layers in the main decoder. Ling 2.6’s optional MTP path can add a small MLA cache when used.
- Nemotron hybrids contribute cache through their explicit GQA layers.
- DeltaNet, Lightning Attention, Mamba-2, and xLSTM layers add `0 B/token` to a growing KV cache.

The last group still needs inference state. Its state has a fixed size with respect to sequence length, so I keep it outside a metric that measures growth per token.

```python
sum(per-layer cache growth over the cache-growing layers only)
```

## Checks against published configurations

I verified the gallery values against the corresponding configuration files. These examples cover the main cases above.

[Qwen3 8B](https://huggingface.co/Qwen/Qwen3-8B/blob/main/config.json) has 36 GQA layers, 8 KV heads, and a head dimension of 128:

```python
36 layers × 8 KV heads × 128 head_dim × 4
= 147,456 bytes
= 144 KiB
```

[DeepSeek V3](https://huggingface.co/deepseek-ai/DeepSeek-V3/blob/main/config.json) has 61 MLA layers, a KV latent rank of 512, and a 64-dimensional rotary-key component:

```python
61 layers × (512 kv_lora_rank + 64 qk_rope_head_dim) × 2
= 70,272 bytes
= 68.6 KiB
```

[Qwen3-Next 80B-A3B](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct/blob/main/config.json) has 48 decoder layers with full attention every fourth layer. Only 12 layers enter the growing KV-cache calculation:

```python
12 full-attention layers × 2 KV heads × 256 head_dim × 4
= 24,576 bytes
= 24 KiB
```

[Gemma 4 31B](https://huggingface.co/google/gemma-4-31B-it/blob/main/config.json) has 50 sliding-window layers and 10 global layers. The global layers use unified `K=V` and four 512-dimensional KV heads:

```python
50 sliding-window layers × 16 KV heads × 256 head_dim × 4
+ 10 global layers × 4 KV heads × 512 global_head_dim × 2
= 819,200 + 40,960 bytes
= 860,160 bytes
= 840 KiB
```

The same calculation gives `210 KiB` for [Gemma 4 26B-A4B](https://huggingface.co/google/gemma-4-26B-A4B-it/blob/main/config.json) and `328 KiB` for [Gemma 4 12B](https://huggingface.co/google/gemma-4-12B-it/blob/main/config.json). [xLSTM 7B](https://arxiv.org/abs/2503.13427) has no attention layers, so its growing KV-cache value is `0 B/token`. Its recurrent matrix state is still present.

## From one token to a context

For a full-attention model, multiply the gallery number by the number of retained tokens. At 32,768 tokens, the `144 KiB/token` value for Qwen3 8B corresponds to `4.5 GiB` of logical bf16 KV cache for batch size 1.

Mixed stacks require the layer-wise form because different layers may retain different numbers of tokens:

```python
total_cache_bytes
= sum(bytes_per_layer_per_token × retained_tokens_for_that_layer)
```

A larger batch adds the cache for every active sequence. Paged serving, padding, cache quantization, and temporary buffers can move the measured memory above or below a simple bf16 estimate. This is why the gallery field is best read as an architecture comparison value.

## Gallery bands

The gallery and model-comparison tool attach a rough label to each numeric value:

- `0 B` -> `No cache`
- `> 0` and `<= 24 KiB` -> `Very low`
- `> 24 KiB` and `<= 72 KiB` -> `Low`
- `> 72 KiB` and `<= 160 KiB` -> `Moderate`
- `> 160 KiB` and `<= 300 KiB` -> `High`
- `> 300 KiB` -> `Very high`

These labels are only for quick scanning. Use the numeric value for calculations.

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
