---
title: "Sliding-window attention"
source: https://sebastianraschka.com/faq/docs/sliding-window-attention.html
crawled: 2026-09-06
---

# Sliding-window attention

**Sliding-window attention (SWA)** is self-attention in which each query can access only a fixed local range of keys and values. In a causal LLM, this usually means the current token and a bounded number of preceding tokens. Standard causal attention can access the complete preceding context.

For a sequence position \(i\) and a window containing \(W\) positions, a simple causal local mask is

\[M\_{ij} =
\begin{cases}
0, & 0 \leq i-j < W, \\
-\infty, & \text{otherwise}.
\end{cases}\]

The mask is added to the query-key scores before softmax. Future positions and sufficiently old positions then receive zero attention weight. Implementations differ on whether the named window size counts the current token, so an off-by-one test near the boundary is worthwhile.

![Sliding-window attention gives each query a moving local neighborhood rather than the complete causal prefix.](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/swa-memory/1.webp)

The window moves with the query position. This differs from splitting the sequence into independent chunks. Two tokens on opposite sides of a fixed chunk boundary can still interact if they fall inside the same sliding window.

For sequence length \(T\), full attention computes on the order of \(T^2\) query-key scores. Causal sliding-window attention computes about \(TW\) scores when \(T\) is much larger than \(W\). This turns the attention-score calculation from quadratic to linear growth in \(T\) for a fixed window.

The saving depends on the implementation. Creating a dense \(T \times T\) score matrix and masking most entries afterwards produces the local result but retains most of the full-attention cost. An efficient local-attention kernel computes only the allowed bands. FlashAttention improves the memory behavior of exact attention, but full FlashAttention still computes full attention unless a local-window option is used.

Training and inference benefit in different ways. During training or prompt prefill, a local kernel reduces the number of score pairs. During autoregressive decoding, a local layer only needs keys and values from its most recent window. Older entries can be evicted from that layer’s KV cache, which bounds its cache length by \(W\).

Again, eviction has to be implemented. A runtime can apply the local mask while retaining the complete KV history, in which case it saves attention work but little cache capacity. Evicting old entries also changes the output of a model trained for full attention. SWA is an architecture property that should match the checkpoint, not a lossless serving switch for an arbitrary model.

![The KV-cache advantage of local layers grows with context length because each layer can stop retaining keys and values beyond its window.](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/swa-memory/4.webp)

One local layer cannot directly retrieve a token outside its window. Stacking layers expands the receptive field because a nearby token can already contain information gathered in the previous layer. With a causal window of \(W\) positions, \(L\) consecutive local layers have a theoretical receptive field of roughly \(1 + L(W-1)\) positions. This is indirect propagation through intermediate hidden states. It is different from one global-attention layer that can compare the current query directly with every retained key.

Architectures therefore often alternate local and global layers. The local layers handle most token interactions at lower cost, while a periodic global layer restores direct full-context lookup. The local-to-global ratio and the window size are separate choices.

Gemma illustrates this design. Gemma 2 alternates local and global attention in a 1-to-1 pattern and uses a 4,096-token local window. Gemma 3 uses five local layers per global layer and reduces the local window to 1,024 tokens. The [Gemma 3 report](https://arxiv.org/abs/2503.19786) includes an ablation in which this more aggressive local pattern had little effect on perplexity for the tested model and setup. That result should not be read as a guarantee for tasks requiring exact retrieval over distant tokens.

SWA and grouped-query attention address different dimensions of the KV cache. SWA limits how many token positions a local layer retains. GQA reduces how many key and value heads are stored at each retained position. A model can use either method independently or combine them.

Local attention is a good fit when nearby context carries most of the useful signal, context lengths make full attention expensive, or cache capacity limits concurrent serving. It is a weaker fit when every layer needs direct access to arbitrary earlier details. Long-document comparison, repository-wide code queries, and exact retrieval can expose this limitation, especially if the stack has no global layers or other long-range mechanism.

The configured context window can still be much larger than the local window. Positional encodings cover the longer sequence, and information can move through stacked local layers or periodic global layers. The exact pattern needs to be included in evaluation because two models with the same maximum context length can have very different direct-access paths.

Sliding-window attention is therefore useful when its locality bias matches the workload and the system realizes the sparse computation and bounded cache. I would check the attention mask at window boundaries, compare a local kernel with a dense reference on a short sequence, measure the retained cache length, and evaluate retrieval at distances both inside and outside the local window.

The [Sliding Window Attention gallery page](https://sebastianraschka.com/llm-architecture-gallery/swa/) shows several local-to-global layer schedules. For related foundations, see [What is self-attention, and why is it the core mechanism behind modern LLMs?](https://sebastianraschka.com/faq/docs/self-attention.html) and [Why is the KV cache such a big memory bottleneck at long context lengths?](https://sebastianraschka.com/faq/docs/kv-cache-long-context-bottleneck.html).
