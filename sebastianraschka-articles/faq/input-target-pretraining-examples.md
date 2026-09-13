---
title: "How are input-target training examples constructed for LLM pretraining?"
source: https://sebastianraschka.com/faq/docs/input-target-pretraining-examples.html
crawled: 2026-09-06
---

# How are input-target training examples constructed for LLM pretraining?

LLM pretraining examples come directly from tokenized text. For a training sequence length of `L`, the data loader first takes `L+1` consecutive token IDs. The first `L` tokens become the model input, and the last `L` become the targets.

For a five-token chunk, the split looks like this:

`tokens = [t0, t1, t2, t3, t4]`

`input = [t0, t1, t2, t3]`

`target = [t1, t2, t3, t4]`

The target at each array position is therefore the token that follows the corresponding input position. A context length of 256 requires 257 source tokens to create 256 inputs and 256 next-token targets.

![One tokenized sequence is shifted by one position to form aligned input and target arrays](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/inputs-targets.webp)

The target tensor is used by the loss function. It is not appended to the model input as a separate answer. The model processes the input array and returns one vocabulary-logit vector per position. A [causal mask](https://sebastianraschka.com/faq/docs/causal-attention.html) prevents position `j` from reading later input positions, and cross-entropy compares its logits with `target[j]`. This produces `L` supervised signals from one sequence.

The next decision is how to move through the token stream. The **stride** gives the distance between consecutive starting positions. With `L=4` and a stride of 4, neighboring examples do not overlap. A stride of 2 reuses part of the preceding context:

`example 1 source = [t0, t1, t2, t3, t4]`

`example 2 source = [t2, t3, t4, t5, t6]`

The chapter 2 data loader uses this sliding-window setup because it makes the relationship between context length and overlap easy to inspect.

![A sliding window can advance by the full context length or use a smaller stride that creates overlapping examples](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch02_compressed/13.webp)

Overlap gives a token more surrounding contexts, but it also repeats training targets and increases computation. Large pretraining pipelines often pack tokenized documents into mostly nonoverlapping fixed-length sequences for better data efficiency. An end-of-text token can mark document boundaries when several documents share one packed sequence.

Short final chunks need a policy as well. A pipeline may drop them, combine them with another document, or pad them to length `L`. If padding is used, the corresponding target positions should be excluded from the loss. Otherwise, the model spends capacity learning to predict artificial padding tokens.

The completed examples are stacked into input and target tensors with shape `B x L`, where `B` is the batch size. The model output has shape `B x L x V` for a vocabulary of size `V`, and the loss aggregates the valid next-token predictions across the batch.

![A mini-batch stacks several fixed-length token sequences so their next-token losses can be computed together](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/batching.webp)

This construction is called self-supervised because the continuation already present in the text supplies the label. Human annotators do not have to create a target for each token position.
