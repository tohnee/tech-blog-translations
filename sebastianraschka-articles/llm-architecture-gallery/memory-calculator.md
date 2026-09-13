---
title: "LLM Memory Calculator"
source: https://sebastianraschka.com/llm-architecture-gallery/memory-calculator/
crawled: 2026-09-06
---

# LLM Memory Calculator

Estimate the memory occupied by model weights and the KV cache during inference. Change the context length or batch size to see how the cache grows while the weights stay fixed.

These are logical payload estimates. A running model also needs memory for activations, temporary buffers, and other runtime state.

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[KV-cache calculation notes](https://sebastianraschka.com/llm-architecture-gallery/kv-cache-calculations/)

Enable JavaScript to use the calculator. The formulas and assumptions below are available without JavaScript.

## Weights + KV cache

Waiting for settings

Estimated payload before runtime overhead.

### Weight memory

Unavailable

One resident copy of the model.

### KV-cache memory

Unavailable

Across all sequences.

[Model fact sheet](https://sebastianraschka.com/llm-architecture-gallery/)
Model configuration

Settings are saved in the page URL when you finish changing a control. Copy the address to share the estimate.

## How the estimate works

The calculator uses the gallery's rounded parameter counts and BF16 cache figures. M, B, and T mean million, billion, and trillion parameters. Memory is displayed in GiB (230 bytes); GB uses 109 bytes.

**Weight bytes** = parameter count × weight bits ÷ 8

**KV-cache bytes** = BF16 cache bytes per token × context tokens × batch size × cache bits ÷ 16

For example, Qwen3 8B has a gallery estimate of 144 KiB of BF16 cache per token. At 32,768 tokens and batch size 1, that gives 4.5 GiB of KV cache. Its 8 billion parameters occupy approximately 14.90 GiB at 16 bits per weight.

- **Resident weights.** All counted parameters remain in memory, including every MoE expert. Active parameters per token describe computation and do not replace the total weight count. Weights are shared across the batch.
- **Retained tokens.** Each sequence keeps its own cache, with no shared prefixes or beam search. Sliding-window and chunked models use a full-retention projection here because the gallery does not provide each layer's retention limit. A runtime that evicts old entries can use less cache.
- **Architecture scope.** Cache figures follow the gallery's logical representation. Fixed recurrent state, sparse-attention index buffers, and optional multi-token prediction paths are excluded. Special cases are called out beside the result.
- **Precision.** The selected bit width applies uniformly to the counted weights or cache. Quantization scales, zero points, padding, and tensors retained at higher precision add memory. Selecting a format here does not imply that a particular model or runtime supports it.
- **Runtime memory.** Activations, prefill workspace, allocator reserves, and other serving buffers are excluded. CPU offloading and distribution across GPUs are not modeled. The sum alone cannot determine whether a model fits on a GPU.

See the [gallery's per-layer formulas](https://sebastianraschka.com/llm-architecture-gallery/kv-cache-calculations/) for GQA, MLA, shared caches, and recurrent hybrids. The Transformers documentation explains [how caching works](https://huggingface.co/docs/transformers/cache_explanation) and [how cache strategies affect memory](https://huggingface.co/docs/transformers/kv_cache).
