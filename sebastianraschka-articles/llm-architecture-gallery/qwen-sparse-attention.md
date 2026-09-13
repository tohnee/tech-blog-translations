---
title: "Qwen Sparse Attention"
source: https://sebastianraschka.com/llm-architecture-gallery/qwen-sparse-attention/
crawled: 2026-09-06
---

# Qwen Sparse Attention

Qwen Sparse Attention (QSA) is a attention mechansism inspired by the sparse selection in [DeepSeek Sparse Attention](https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/) (DSA). Similar to DSA, QSA uses a learned indexer. However, instead of choosing (or learning to choose) individual tokens, it chooses complete four-token micro-blocks from the visible prefix. So here, QSA reads every token in the selected blocks, plus the visible tokens in the current incomplete block.

Again, the selection unit is the main difference from [DeepSeek Sparse Attention](https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/), which, in contrast ranks individual token positions.

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[Model card](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)
[Technical report](https://github.com/QwenLM/Qwen3.8-Flash-Next/blob/main/tech_report.pdf)

![Qwen3.8-Flash-Next architecture showing Qwen Sparse Attention and Gated DeltaNet layers](https://sebastianraschka.com/llm-architecture-gallery/images/architectures/qwen3-8-flash-next.webp)

Figure 1. Qwen3.8-Flash-Next uses 12 QSA layers and 36 Gated DeltaNet layers in a 3:1 schedule. Architecture details come from the
[model card](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) and
[released configuration](https://huggingface.co/Qwen/Qwen3.8-Flash-Next/blob/main/config.json).

Selection unit

Complete four-token micro-blocks

Selection budget

Up to 512 blocks, or 2,048 selected tokens, plus the current tail

Example architecture

[Qwen3.8-Flash-Next 125B-A6B](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-8-flash-next-125b-a6b)

## How block selection works

The indexer in QSA creates groups of 4 tokens, for the keys preceeding the query (since it’s still autoregressive) and averages the keys within each complete block. Then, there’s a normalization step for these pooled keys, followed by RoPE (using the first position in each block), and then followed by scores them against the current query. The highest-scoring blocks are expanded back into their four token positions before the main attention operation.

```python
complete_blocks = group(visible_prefix, block_size=4)
block_keys      = mean(keys in each complete block)
scores          = sum(relu(query_head @ block_key) for each indexer head)
selected_blocks = top_k(scores, k=512)
attention_input = flatten(selected_blocks) + current_incomplete_block
```

If we consider a 2,048-token budget and four tokens per block, QSA can select up to 512 complete blocks since 2,048/4 =512.

## QSA versus DeepSeek Sparse Attention

|  | Qwen Sparse Attention | DeepSeek Sparse Attention |
| --- | --- | --- |
| Selection unit | Complete four-token block | Individual token position |
| 2,048-token budget | Up to 512 selected blocks | Up to 2,048 selected tokens |
| Current incomplete block | Included directly | No corresponding block-tail rule |
| Selection pattern | Learned from the current query | Learned from the current query |

QSA uses a coarser index. Selecting one relevant token also brings the other tokens in its four-token block. DSA can select token positions independently.

## Where QSA sits in the model

In total, to look at the model where it was first introduced, namely, [Qwen3.8-Flash-Next](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-8-flash-next-125b-a6b), the model has 48 transformer blocks. Each group contains three [Gated DeltaNet](https://sebastianraschka.com/llm-architecture-gallery/hybrid-attention/) layers followed by one QSA layer, giving 36 recurrent layers and 12 sparse-attention layers.

The important note here is that only the QSA layers contribute to the growing KV cache. But due to the sparse selection, this is more efficient than standard attention. I.e., for a given 1M token context, only 2,048 tokens are selected for a given query (similar to DeepSeek Sparse Attention, but using a more efficient block-wise selection mechanism).

Sources

[Qwen3.8-Flash-Next model card](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)
[Qwen3.8-Flash-Next configuration](https://huggingface.co/Qwen/Qwen3.8-Flash-Next/blob/main/config.json)
[Qwen3.8-Flash-Next technical report](https://github.com/QwenLM/Qwen3.8-Flash-Next/blob/main/tech_report.pdf)
[Transformers QSA implementation](https://github.com/huggingface/transformers/blob/main/src/transformers/models/qwen4_exp/modeling_qwen4_exp.py#L622-L718)
[DeepSeek Sparse Attention explainer](https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
