---
title: "What are the main building blocks of a GPT-style model?"
source: https://sebastianraschka.com/faq/docs/gpt-style-model-building-blocks.html
crawled: 2026-09-06
---

# What are the main building blocks of a GPT-style model?

A GPT-style model has an input embedding stage, a stack of decoder blocks, and an output layer that scores the next token. The tokenizer runs immediately before the model. It converts text into token IDs and defines the vocabulary, but it is usually treated as preprocessing rather than as a neural-network layer.

Suppose a batch contains `B` sequences of `T` token IDs and the model width is `d`. A token-embedding table maps every ID to a learned vector, producing a tensor with shape `B x T x d`. The GPT-2-style implementation in the repo adds a learned position embedding to each token vector. Newer models may supply [positional information](https://sebastianraschka.com/faq/docs/positional-information-transformer.html) inside attention through RoPE instead.

![A GPT-style model maps tokenized text to embeddings, processes them with repeated transformer blocks, and projects the final representations to vocabulary logits](https://sebastianraschka.com/images/blog/2024/building-a-gpt-style-llm-classifier/image2.png)

The repeated transformer block does most of the work. In the pre-normalization design used by the repo, its two updates can be summarized as:

`x = x + attention(norm(x))`

`x = x + feed_forward(norm(x))`

The attention sublayer mixes information across token positions. Its [causal mask](https://sebastianraschka.com/faq/docs/causal-attention.html) lets position `t` use positions `0` through `t` while blocking later tokens. Multi-head attention performs several such mixtures in parallel, allowing different heads to focus on different token relationships.

The feed-forward sublayer works differently. It applies the same small neural network to every position independently. In a GPT-2-style block, this network expands the hidden dimension, applies a nonlinear activation such as GELU, and projects the result back to width `d`. Attention communicates across positions, whereas the feed-forward layer transforms the features stored at each position.

Normalization and residual connections are part of both updates. Normalization controls the scale of the inputs entering each sublayer. The residual addition preserves a direct path for the existing representation and makes a deep stack easier to optimize. The tensor retains its `B x T x d` shape as it passes through all transformer blocks.

![Each transformer block contains causal multi-head attention and a position-wise feed-forward network, with normalization and residual paths around both sublayers](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch04_compressed/03.webp)

After the last block, a final normalization layer prepares the hidden states for the output head. This linear projection maps each `d`-dimensional vector to `V` scores, where `V` is the vocabulary size. The result has shape `B x T x V`. These raw scores are the logits. Some implementations tie the output projection weights to the token-embedding table, while others learn a separate matrix.

During training, the logits at every position are compared with the next token through cross-entropy loss. During generation, only the logits at the final available position are needed to choose the next token. The new token is appended to the sequence and the process repeats.

GPT is called **decoder-only** because this stack uses causal self-attention and has no separate encoder or encoder-decoder cross-attention module. Modern LLMs may replace LayerNorm with RMSNorm, learned position embeddings with RoPE, or standard multi-head attention with GQA. Those changes preserve the same overall path from token IDs to contextual representations and vocabulary logits.
