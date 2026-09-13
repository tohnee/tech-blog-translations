---
title: "DeepSeek Sparse Attention"
source: https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/
crawled: 2026-09-06
---

# DeepSeek Sparse Attention

DeepSeek Sparse Attention uses an indexer and token selector to keep a learned subset of the visible prefix. A selected token can be far outside a fixed local window.

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)

![GLM-5 versus GLM-4.5 architecture comparison showing the adoption of DeepSeek Sparse Attention](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/deepseek-sparse-attention-glm5-vs-glm45.webp)

Figure 1. GLM-5 combines DeepSeek Sparse Attention with
[Multi-head Latent Attention](https://sebastianraschka.com/llm-architecture-gallery/mla/) (Original source
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)).

Summary

Learn a sparse attention pattern

Practical benefit

Reduce long-context attention work

Example architectures

[DeepSeek V3.2](https://sebastianraschka.com/llm-architecture-gallery/#card-deepseek-v3-2),
[GLM-5](https://sebastianraschka.com/llm-architecture-gallery/#card-glm-5-744b),
[GLM-5.2](https://sebastianraschka.com/llm-architecture-gallery/#card-glm-5-2), and
[Tencent Hy4-preview](https://sebastianraschka.com/llm-architecture-gallery/#card-tencent-hy4-preview-770b-a49b)

## Learned sparsity versus a fixed window

![Side-by-side comparison of regular causal attention, sliding-window attention, and DeepSeek Sparse Attention](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/deepseek-sparse-attention-comparison.webp)

Figure 2. Full causal attention reads the visible prefix,
[sliding-window attention](https://sebastianraschka.com/llm-architecture-gallery/swa/) keeps a local block, and DSA learns a subset (Original source
[*From DeepSeek V3 to V3.2: Architecture, Sparse Attention, and RL Updates*](https://magazine.sebastianraschka.com/p/technical-deepseek)).

## The indexer and selector

The lightning indexer scores an earlier position `s` for the current position `t` as follows:

\[I\_{t,s} = \sum\_{j=1}^{H^I} w\_{t,j}\,\operatorname{ReLU}\!\left(q\_{t,j}\cdot k\_s\right).\]

```python
# t = current position, s = earlier positions, j = indexer head
scores[s] = sum(w[t,j] * relu(dot(q[t,j], k[s])) for j in heads)
selected  = top_k(scores, k=2048)
output    = sparse_attention(query_t, selected)  # O(Lk) over the sequence
```

![DeepSeek Sparse Attention flowchart from the DeepSeek V3.2 article](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/deepseek-sparse-attention-flow.webp)

Figure 3. The indexer scores the prefix before the selector retains the top entries (Original source
[*From DeepSeek V3 to V3.2: Architecture, Sparse Attention, and RL Updates*](https://magazine.sebastianraschka.com/p/technical-deepseek)).

## How DSA and MLA fit together

[MLA](https://sebastianraschka.com/llm-architecture-gallery/mla/) compresses what is stored in the [KV cache](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms). DSA changes which stored positions the attention operation reads.

![DeepSeek V3.2 architecture figure](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/deepseek-sparse-attention-deepseek-v3-2.webp)

Figure 4. DeepSeek V3.2 pairs MLA with DSA (Original source
[*From DeepSeek V3 to V3.2: Architecture, Sparse Attention, and RL Updates*](https://magazine.sebastianraschka.com/p/technical-deepseek)).

The `k` in top-`k`, not to be confused with the `k` used for keys in the equation, is set to 2048 in the [released model code](https://huggingface.co/deepseek-ai/DeepSeek-V3.2-Exp/blob/main/inference/model.py#L90). The indexer and token selector result in each token attending to a few past tokens that the model has learned to consider most relevant, rather than all tokens or a fixed local window.

The goal was not to improve performance over the dense base model but to reduce performance degradation from the sparse attention mechanism while benefiting from improved efficiency. GLM-5 later adopted DSA and MLA. GLM-5.2 adds [IndexShare](https://sebastianraschka.com/llm-architecture-gallery/indexshare/) so that nearby layers can reuse selected positions.

Sources

[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
[A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)
[DeepSeek V3.2 technical article](https://magazine.sebastianraschka.com/p/technical-deepseek)
[DeepSeek V3.2 paper](https://arxiv.org/pdf/2512.02556)
[GLM-5 paper](https://arxiv.org/pdf/2602.15763)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
