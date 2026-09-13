---
title: "Why Transformer LLMs Use Multi-Head Attention"
source: https://sebastianraschka.com/faq/docs/multi-head-attention.html
crawled: 2026-09-06
---

# Why Transformer LLMs Use Multi-Head Attention

Transformer-based LLMs use **multi-head attention** so that each token can form several independent attention distributions at the same time. A single attention head produces one distribution over the other tokens. Multiple heads let the model compare and combine several such distributions in parallel.

Importantly, the heads usually split a fixed projection width. They are not full-width copies of the entire attention mechanism.

Suppose the input tensor has shape (B \times T \times d\_{\text{model}}), where (B) is the batch size and (T) is the sequence length. In standard multi-head attention, learned linear layers project this input into query, key, and value tensors. Each projected tensor initially has shape

[
B \times T \times d\_{\text{model}}.
]

The implementation then reshapes each tensor into

[
B \times H \times T \times d\_{\text{head}},
]

where (H) is the number of heads and

[
d\_{\text{head}} = \frac{d\_{\text{model}}}{H}.
]

For example, a layer with (d\_{\text{model}} = 4096) and 32 heads uses (d\_{\text{head}} = 128). The query projection is still 4,096 dimensions wide. It is reshaped into 32 heads with 128 dimensions each.

![Multi-head attention applies several attention heads to the same input sequence. Each head uses separate query, key, and value projections.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch03_compressed/24.webp)

Within head (h), scaled dot-product attention is

[
\text{head}*h = \operatorname{softmax}\left(\frac{Q\_h K\_h^\top}{\sqrt{d*{\text{head}}}} + M\right)V\_h,
]

where (M) is an optional mask. GPT-style LLMs use a causal mask that prevents tokens from attending to future positions. I discuss this masking step separately in [What is causal attention, and how is it implemented?](https://sebastianraschka.com/faq/docs/causal-attention.html)

Each head has its own projected queries, keys, and values, so it can produce a different (T \times T) attention matrix. These heads are not assigned fixed jobs such as syntax, formatting, or long-range reference. Such patterns may emerge during training, but they are not guaranteed, and some heads can be partly redundant.

After attention, each head produces (T \times d\_{\text{head}}) output features. The implementation concatenates the head outputs to recover (T \times d\_{\text{model}}), then applies a learned output projection:

[
\operatorname{MultiHead}(X)
= \operatorname{Concat}(\text{head}\_1, \ldots, \text{head}\_H)W\_O.
]

This output projection is important because it mixes information from the different heads before the result enters the residual connection and the next transformer sublayer.

![An efficient multi-head attention implementation computes large query, key, and value projections before reshaping the projected channels into separate heads.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch03_compressed/26.webp)

At a fixed model width, multi-head attention does not multiply the query, key, and value parameter count by the number of heads. A classic implementation has one (d\_{\text{model}} \times d\_{\text{model}}) matrix for each of the query, key, value, and output projections, similar to a full-width single-head implementation. The heads determine how the projected channels are partitioned for the attention calculation.

The main attention computation also remains proportional to (T^2 d\_{\text{model}}). There are (H) attention calculations, but each uses only (d\_{\text{head}} = d\_{\text{model}}/H) features. A basic implementation does create (H) separate (T \times T) attention-weight matrices, which adds memory overhead. Optimized kernels can reduce how much of this intermediate data must be stored.

More heads are not always better. Increasing (H) makes each head narrower, and very small head dimensions can limit what an individual head represents. Additional heads can also increase implementation overhead. The head count and head dimension are therefore architecture choices that must be balanced with the model width.

Standard multi-head attention, often abbreviated **MHA**, uses the same number of query, key, and value heads. Newer LLMs sometimes keep many query heads while sharing fewer key and value heads:

- MHA uses (H) query heads and (H) key-value heads.
- Grouped-query attention uses (H) query heads and fewer key-value heads.
- Multi-query attention uses (H) query heads and one key-value head.

These variants preserve multiple query-dependent attention distributions while reducing the key-value cache used during autoregressive generation. The differences are explained in [What is grouped-query attention, and why is it used in LLMs?](https://sebastianraschka.com/faq/docs/grouped-query-attention.html)

In short, multi-head attention gives a transformer several independent ways to route information between tokens while keeping the total projection width fixed. The concatenation and output projection then combine those routes into the representation passed through the rest of the transformer block.
