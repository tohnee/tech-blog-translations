---
title: "GPT, Llama, Qwen, and Gemma Architectures Compared"
source: https://sebastianraschka.com/faq/docs/gpt-llama-qwen-gemma-comparison.html
crawled: 2026-09-06
---

# GPT, Llama, Qwen, and Gemma Architectures Compared

At a high level, these architectures are close relatives. Documented GPT-style models, Llama, Qwen, and Gemma use an autoregressive decoder-only transformer. They repeat causal self-attention and feed-forward layers around residual connections, then predict the next token.

The family name alone is not enough for an exact comparison because every family changes between generations. In addition, OpenAI has not published complete block-level specifications for recent proprietary GPT models. I therefore use the public GPT-2 and GPT-3 design as the older GPT-style reference and named open-weight checkpoints for the newer families.

![The repo's GPT-to-Llama material follows the documented progression from the GPT-2-style decoder to Llama 2 and Llama 3](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/gpt-to-llama/gpt2-to-llama2-llama3.webp)

This representative comparison captures the main block-level differences:

| Representative design | Normalization | Position information | Attention | Feed-forward layer | Parameter layout |
| --- | --- | --- | --- | --- | --- |
| GPT-2/3 style | LayerNorm | Learned absolute embeddings | Multi-head attention | GELU MLP | Dense |
| Llama 3 | RMSNorm | RoPE | Grouped-query attention | SwiGLU | Dense |
| Qwen3 8B | RMSNorm | RoPE | GQA with QK-Norm | SwiGLU | Dense |
| Gemma 3 27B | RMSNorm with additional norm placements | RoPE | GQA with QK-Norm and local/global layers | GeGLU | Dense |

The older GPT-style design is useful as a clean baseline. It adds learned position embeddings to token embeddings, uses LayerNorm, and gives every attention head its own key and value projections. Its feed-forward block uses GELU. The small GPT implementation in the repo follows this pattern because each part is straightforward to inspect and implement.

Llama keeps the same decoder structure while changing several components. RMSNorm replaces LayerNorm, RoPE moves position information into attention, and SwiGLU replaces the plain GELU MLP. Llama 3 also uses [grouped-query attention](https://sebastianraschka.com/faq/docs/grouped-query-attention.html), which shares key and value heads across groups of query heads and reduces KV-cache memory during generation.

Qwen3’s dense models look similar to this Llama-style recipe. Qwen3 8B adds QK-Norm inside attention and uses a larger vocabulary. The family also includes mixture-of-experts models, where each token activates only a subset of the available feed-forward experts. Dense and MoE are genuine architecture differences. Labels such as base, instruct, coder, and reasoning usually describe training or intended use, so they should not be treated as transformer-block features.

![The Qwen overview separates dense and MoE architectures from base, instruct, coder, and reasoning-oriented releases](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/qwen/qwen-overview.webp)

Gemma 3 makes a different set of choices. It uses GeGLU rather than SwiGLU and places RMSNorm at more points around the attention and feed-forward sublayers. Gemma 3 27B combines sliding-window attention with periodic global-attention layers in a 5-to-1 pattern. Most layers process a local context, while the global layers allow information to travel across the full sequence.

![The Gemma 3 and Qwen3 comparison shows two modern decoder families with different attention schedules, normalization layouts, and feed-forward activations](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/gemma3/gemma3-vs-qwen3.webp)

These component choices affect memory use, training stability, and inference cost, but the architecture alone does not determine model quality. Parameter count, tokenizer, training data, optimization, context-length training, and post-training can matter at least as much. For a practical comparison, it is better to name the exact checkpoints and separate their architecture from their training recipe and measured behavior.
