---
title: "Embedding Layers as Linear Layers on One-Hot Tokens"
source: https://sebastianraschka.com/faq/docs/embedding-linear-onehot.html
crawled: 2026-09-06
---

# Embedding Layers as Linear Layers on One-Hot Tokens

An embedding lookup and a bias-free linear layer give the same result when the linear layer receives a one-hot encoded token. The two implementations store the same learned numbers and differ mainly in how they access them.

Suppose a tokenizer has a vocabulary of size \(V\), and we want an embedding dimension of \(d\). The embedding layer stores

\[E \in \mathbb{R}^{V \times d}.\]

For token ID \(i\), the lookup returns row \(i\) of \(E\). This is the usual view of an embedding layer as a learned table.

![Embedding lookup selects rows from the embedding matrix for a batch of token indices](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/embeddings-and-linear-layers/3.png)

We can also represent token ID \(i\) by the one-hot vector

\[e\_i \in \mathbb{R}^{V}.\]

Every entry in \(e\_i\) is zero except the entry at position \(i\). Multiplication with the embedding matrix gives

\[e\_i^\top E = E\_i.\]

The zeros remove all unselected rows from the sum, and the single 1 retains row \(i\). The result is therefore identical to `E[i]`.

For a batch or sequence, stack the one-hot vectors into a matrix. Multiplying that matrix by \(E\) selects one embedding row for each token position, which produces the same tensor as a batched embedding lookup.

![One-hot encoded token vectors multiplied by a weight matrix select the same rows as an embedding lookup](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/embeddings-and-linear-layers/4.png)

The transpose is usually the part that causes confusion in code. In PyTorch, `nn.Linear(V, d, bias=False)` stores its weight with shape \(d \times V\) and computes the input times the transposed weight. To match an embedding matrix with shape \(V \times d\), the linear-layer weight is therefore set to \(E^\top\).

In practice, we use the embedding operation because constructing the one-hot vectors would be wasteful. With a 50,000-token vocabulary, every token would become a length-50,000 vector containing 49,999 zeros. The embedding layer skips this representation and gathers the required rows directly.

The gradients follow the same equivalence. Only rows selected by tokens in the batch receive updates, and repeated token IDs accumulate contributions to the same row.

One qualification is worth keeping in mind. The lookup is linear with respect to the one-hot vector. It is not a linear function of the integer token ID, since token IDs are categorical labels and their numerical order has no geometric meaning.
