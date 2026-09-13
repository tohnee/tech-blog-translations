---
title: "Causal Attention in GPT-Style Language Models"
source: https://sebastianraschka.com/faq/docs/causal-attention.html
crawled: 2026-09-06
---

# Causal Attention in GPT-Style Language Models

**Causal attention** is self-attention with a rule that blocks information from later token positions. At position `t`, the model may attend to positions up to and including `t`. The resulting representation is then used to predict the token at position `t+1`.

For a small example, consider the token sequence “the cat sat”. When the model computes the representation for “cat”, it may use “the” and “cat”. It cannot use “sat”, since “sat” is the next-token target at that point.

![Causal attention masks future positions in the attention matrix](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch03_compressed/19.webp)

This restriction lets a GPT-style model train on complete sequences without seeing the answers to its own prediction tasks. The entire training sequence is available in memory, which makes it possible to process many positions in parallel. The attention mask still limits what each position can read.

Without the mask, the representation for “cat” could incorporate information from “sat” and then use that information to predict “sat”. The training loss would be low for the wrong reason. At generation time, the future token does not exist, so the same shortcut would be unavailable.

The implementation uses a triangular mask on the attention-score matrix. Entries that refer to later positions receive a value such as negative infinity before softmax. Their probabilities therefore become zero, while the entries on and below the diagonal remain available.

![The mask is applied before softmax so future-token weights become zero](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch03_compressed/21.webp)

One useful consequence is that all positions still contribute a training signal in the same forward pass. Position 5 can learn to predict position 6 while position 20 learns to predict position 21. The calculations run together, and each one observes a different-length prefix because of the mask.

At inference time, generation uses the same dependency pattern. The representation at the final position can use the prompt and all tokens generated so far. Its logits select the next token, which is appended before the model runs again. Earlier positions have access to shorter prefixes, so they cannot contain information introduced later in the sequence.

Transformer encoders such as BERT use bidirectional attention. BERT receives a complete input and lets a token attend to positions on both sides. This fits tasks where the full text is known, such as constructing a representation for classification. A decoder-only GPT model instead needs the left-to-right dependency required for text generation.

The phrase “cannot look at the future” refers to positions within the current sequence. It does not imply a short attention span. A token can still attend far back into the available prefix, up to the model’s context-window limit.
