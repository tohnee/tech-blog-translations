---
title: "Self-attention in LLMs"
source: https://sebastianraschka.com/faq/docs/self-attention.html
crawled: 2026-09-06
---

# Self-attention in LLMs

**Self-attention** lets each token form a new representation by taking a weighted sum of information from tokens in the same sequence. The weights depend on the current token representations, so the model can route information differently for every input and at every layer.

The word “self” distinguishes this mechanism from cross-attention. In self-attention, the queries, keys, and values all come from the same input sequence. Cross-attention forms queries from one sequence and keys and values from another, such as a text decoder attending to image features.

For an input matrix \(X\) containing \(T\) token representations, one attention head first applies three learned linear projections:

\[Q=XW\_q, \qquad K=XW\_k, \qquad V=XW\_v.\]

The **query** describes what a token is looking for. The **key** describes how a token can be matched, while the **value** contains the information that can be passed to the output. These descriptions are intuition for learned vectors, not separately programmed roles.

The complete scaled dot-product attention calculation is

\[A=\operatorname{softmax}\left(\frac{QK^\mathsf{T}}{\sqrt{d\_k}}+M\right),
\qquad Z=AV.\]

Here, \(d\_k\) is the key dimension and \(M\) is an optional mask. Softmax is applied across each row. This makes the entries in one row of \(A\) nonnegative and sum to one. Row \(i\) describes how token \(i\) mixes the value vectors from the visible token positions. The resulting row of \(Z\) is usually called a **context vector**.

![Self-attention first computes scores, normalizes them into weights, and uses the weights to form context vectors.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch03_compressed/12.webp)

The division by \(\sqrt{d\_k}\) matters because a dot product tends to grow in magnitude as the vector dimension increases. Large unscaled scores can push softmax into a saturated region with very small gradients. Scaling keeps the score range better behaved during optimization.

The attention matrix is dynamic. Suppose a sequence contains the word “bank.” Its query can assign weight to words related to money in one sentence and to “river” in another. The model learns these patterns from the training objective. No one labels a head as a finance head or specifies which token pair it should connect.

![A single attention head projects the input into queries, keys, and values, computes token-to-token weights, and mixes the values into context vectors.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch03_compressed/18.webp)

Decoder-only LLMs such as GPT and Llama use **causal self-attention**. Their mask \(M\) assigns negative infinity to score entries that point to later positions. After softmax, those entries have zero weight. A token can use itself and the preceding prefix, but it cannot read a future token that it is supposed to help predict.

This mask lets training process all positions of a sequence in parallel. Each row of the attention matrix still sees a different prefix. Generation remains sequential because the next input token does not exist until the model has sampled it. A KV cache avoids recomputing keys and values for the old tokens, although the new query still interacts with the cached keys.

One attention head produces one token-to-token weight matrix. Modern transformers usually run several heads in parallel. Each head works in a smaller learned subspace and can produce a different routing pattern. Their outputs are concatenated and passed through an output projection. The [multi-head attention FAQ](https://sebastianraschka.com/faq/docs/multi-head-attention.html) covers the tensor shapes, parameter count, and key-value sharing variants.

Position information is a separate requirement. Without a position-dependent signal, unmasked self-attention is permutation-equivariant. It compares token content but does not know whether one matching token came before another or how far apart they are. LLMs therefore combine attention with a mechanism such as learned absolute position embeddings, RoPE, or a relative position bias. A causal mask supplies direction through the visible-prefix structure, but it is not a precise distance coordinate.

Self-attention has two practical strengths. It gives every token a direct path to every visible token, which helps with long-range dependencies. It also expresses the calculations for all training positions as matrix operations that run efficiently on accelerators. Recurrent networks have to propagate information through a sequence of hidden-state updates, which creates a longer path between distant tokens and less parallel training.

The main cost comes from the \(T \times T\) score and weight matrices. For full attention, the score calculation grows quadratically with sequence length. FlashAttention reduces memory traffic and avoids materializing the complete matrix in slow device memory, but it computes the same exact attention result. Sliding-window attention, sparse attention, and recurrent or linear alternatives change which interactions are computed to reduce the long-context cost.

Attention weights also need cautious interpretation. A large weight means that one head routed more of a particular value vector into its output for that query. It is not a reliable standalone measure of which input token caused the model’s final prediction. The value projection, output projection, other heads, residual connections, feed-forward layers, and later transformer blocks can all change or redirect that information.

Self-attention is central to standard transformer LLMs because it provides content-dependent communication between token positions. The complete model still needs embeddings, position handling, feed-forward layers, normalization, residual connections, and an output layer. Newer hybrid architectures sometimes replace many attention layers with recurrent or state-space blocks, while keeping some full-attention layers for precise token retrieval.

For masking details, see [What is causal attention, and why can GPT-style models not look at future tokens?](https://sebastianraschka.com/faq/docs/causal-attention.html). The original scaled dot-product formulation appears in [Attention Is All You Need](https://arxiv.org/abs/1706.03762), and the [from-scratch implementation](https://sebastianraschka.com/blog/2023/self-attention-from-scratch.html) walks through the calculation in code.
