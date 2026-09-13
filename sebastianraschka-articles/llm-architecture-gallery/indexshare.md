---
title: "IndexShare"
source: https://sebastianraschka.com/llm-architecture-gallery/indexshare/
crawled: 2026-09-06
---

# IndexShare

IndexShare lets nearby layers reuse the token positions selected by a [DeepSeek Sparse Attention (DSA)](https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/) indexer.

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[GLM-5.2 note](https://sebastianraschka.com/blog/2026/glm-5-2-indexshare.html)
[Z.ai release post](https://huggingface.co/blog/zai-org/glm-52-blog)
[IndexCache paper](https://arxiv.org/abs/2603.12201)

![Standard DSA computes top-k token indices in every layer, while IndexShare computes them once and reuses them in three following layers](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/indexshare-four-layer-reuse.webp)

Figure 1. One full indexer result supplies four GLM-5.2 layers.

What is shared

Selected token positions

GLM-5.2 pattern

`full`, `shared`, `shared`, `shared`

Example architectures

[GLM-5.2](https://sebastianraschka.com/llm-architecture-gallery/#card-glm-5-2) and
[Tencent Hy4-preview](https://sebastianraschka.com/llm-architecture-gallery/#card-tencent-hy4-preview-770b-a49b)

## The DSA selection being reused

The `k` in top-`k`, not to be confused with the `k` that is used for the keys in the DSA equation, is a hyperparameter that is set to 2048 in the [DeepSeek model code](https://huggingface.co/deepseek-ai/DeepSeek-V3.2-Exp/blob/main/inference/model.py#L90). The indexer and token selector result in each token attending to a few past tokens that the model has learned to consider most relevant, rather than all tokens or a fixed local window.

The goal was not to improve performance over the dense base model but to reduce performance degradation from the sparse attention mechanism while benefiting from improved efficiency.

## The four-layer reuse pattern

```python
indexer_type = [full, shared, shared, shared]

if indexer_type == full:
    selected = top_k(indexer(hidden_state))
else:
    selected = previous_selected

output = attention(hidden_state, selected)  # New output in every layer
```

![GLM-5.2 architecture diagram with MLA, DeepSeek Sparse Attention, and IndexShare](https://sebastianraschka.com/llm-architecture-gallery/images/architectures/glm-5.2.webp)

Figure 2. GLM-5.2 marks each DSA indexer as `full` or `shared` across its
78-layer stack (Original source
[*GLM-5.2 and IndexShare for Long-Context Sparse Attention*](https://sebastianraschka.com/blog/2026/glm-5-2-indexshare.html)).

## Evidence and tradeoff

| Item | Reported detail | What it means |
| --- | --- | --- |
| Adjacent-layer overlap | The [IndexCache study](https://arxiv.org/abs/2603.12201) measured 70% to 100% overlap between adjacent top-`k` sets. | A new indexer often rediscovers positions selected one layer earlier. |
| GLM-5.2 training | The four-layer pattern was introduced during continued mid-training with 128K-token sequences. | Retained indexers can adapt to serving the following layers. |
| GLM-5.2 result | [Z.ai reports](https://huggingface.co/blog/zai-org/glm-52-blog) 2.9× fewer per-token FLOPs at a one-million-token context. | The reported gain is specific to GLM-5.2 and this context length. |
| IndexCache result | Removing 75% of indexer computations on a 30B DSA model produced up to a 1.82× prefill speedup and a 1.48× decode speedup at 200K. | These are separate system measurements and should not be compared directly with the GLM-5.2 FLOP result. |
| Tradeoff | A shared layer cannot select fresh positions from its current hidden states. | It uses the most recent full layer’s positions, while computing its own attention output. |

Sources

[GLM-5.2 release post](https://huggingface.co/blog/zai-org/glm-52-blog)
[GLM-5.2 configuration](https://huggingface.co/zai-org/GLM-5.2/blob/main/config.json)
[IndexCache paper](https://arxiv.org/abs/2603.12201)
[GLM-5.2 quick note](https://sebastianraschka.com/blog/2026/glm-5-2-indexshare.html)
[DeepSeek Sparse Attention explainer](https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
