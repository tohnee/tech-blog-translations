---
title: "When to mask prompt tokens during SFT"
source: https://sebastianraschka.com/faq/docs/when-mask-prompt-tokens.html
crawled: 2026-09-06
---

# When to mask prompt tokens during SFT

Mask prompt tokens out of the loss when the training objective is to maximize the likelihood of the **assistant response conditioned on the prompt**. This is the usual choice for supervised instruction finetuning (SFT) on prompt-response examples.

Keep prompt-token loss when the model is also expected to generate that part of the sequence, as in ordinary language-model pretraining, transcript completion, or an auxiliary full-sequence objective.

The word “mask” needs care here. A **loss mask** excludes selected target positions from cross-entropy. It does not remove the prompt from the model input, and it does not block response tokens from attending to the prompt.

## What response-only loss computes

Suppose one training record is serialized as

`[system and user prompt] [assistant header] [response] [end token]`

For response-only SFT, the label sequence has the following conceptual form:

`[-100 ... -100] [-100] [response token IDs] [end-token ID]`

In PyTorch, `CrossEntropyLoss` uses `ignore_index=-100` by default. Positions with this label do not contribute to either the summed loss or the token count used by the mean reduction. The actual `input_ids` still contain the system message, user message, role markers, and assistant response.

![Prompt tokens remain in the input while their target labels are replaced by the ignore index so only response tokens contribute directly to the loss](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/mask-instructions.webp)

If `R` is the set of response-token positions, the objective is

\[\mathcal{L}\_{\text{response}}
= -\frac{1}{|R|}\sum\_{t \in R} \log p\_\theta(x\_t \mid x\_{<t}).\]

The model still processes the prompt to predict every response token. Gradients from the response loss flow through the response-token computation into prompt-token hidden states and the parameters that produced them. Masking therefore removes the **direct next-token targets** in the prompt region. It does not stop the model from learning how the prompt affects the answer.

It also does not save the forward-pass computation or activation memory for those tokens. The full prompt is still needed as conditioning context.

## Why prompt masking is often useful

Instruction examples commonly contain a long request and a much shorter answer. If a record has 1,000 prompt tokens and 50 response tokens, full-sequence loss assigns about 95% of its token-level terms to the prompt. The model is then optimized mostly to reproduce user-provided context and template boilerplate.

Response-only loss makes the metric and gradient weighting match the intended conditional task more closely. It is especially useful when:

- the system and user text are supplied by the application at inference time
- the assistant response is the behavior being evaluated
- prompt lengths vary substantially across examples
- fixed role markers or template text would otherwise dominate short answers
- training data packs several prompt-response examples into one sequence

Masking can also make per-token loss easier to interpret. The reported value then summarizes answer-token prediction rather than a mixture of easy template tokens, arbitrary user wording, and answer tokens.

## When full-sequence loss can be reasonable

Prompt masking is an objective choice rather than a universal requirement. Full-sequence loss is appropriate when every segment belongs to the distribution the model should generate.

Examples include continued pretraining on plain documents, dialogue models trained to generate either side of a conversation, and transcript completion without fixed user-assistant roles. A project may also mix a response-only objective with a smaller full-sequence language-modeling term to preserve broader continuation behavior.

Leaving the prompt unmasked can be a practical baseline for a small, uniformly formatted dataset. It uses every available next-token target. However, the apparent loss may be driven by repeated template text. I would compare held-out response quality rather than choosing the objective from training loss alone.

A weighted loss is another option. Prompt positions can receive a small nonzero weight while assistant positions receive full weight. Standard `ignore_index` implements a binary decision, so token-level weighting requires an unreduced cross-entropy followed by an explicit weighted reduction.

## Multi-turn conversations need span-aware masks

For a single-turn record, masking everything before the assistant response is straightforward. Multi-turn chat data has several user and assistant spans:

`system, user 1, assistant 1, user 2, assistant 2`

The correct mask depends on the training example.

- If both assistant messages are demonstrations the model should learn to generate, include loss on `assistant 1` and `assistant 2` while masking the system and user spans.
- If the earlier turns are supplied only as context for the final answer, mask every earlier span and include loss only on `assistant 2`.
- If the model should generate tool calls, include the assistant tool-call tokens. Tool results supplied by the environment usually remain context and are masked.

Do not identify these regions through a naive text search for strings such as `assistant`. The same word can appear inside a message, and role markers can tokenize into several IDs. Prefer span information from the chat-template renderer or token offsets produced during preprocessing. Some templates expose explicit generation spans for this purpose.

The end-of-response token normally remains unmasked. It teaches the model when to stop. Assistant role headers are usually masked when the application inserts them before generation. Include them only if the model is expected to emit them itself.

## Padding and packing require separate checks

Padding labels should always be excluded from the language-model loss. This is independent of prompt masking. A batch may therefore contain both prompt positions and padding positions labeled with `-100`.

![The ignore index excludes repeated padding positions from cross-entropy; the same label mechanism can exclude prompt spans](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/ignore-index.webp)

For packed training examples, concatenate the loss masks with the same boundaries used for `input_ids`. Each response span must remain aligned after adding separators, end tokens, or padding. If the implementation uses block-diagonal attention to isolate packed records, the attention boundaries and loss boundaries should be tested together.

The label shift is another source of off-by-one errors. Many causal-language-model implementations accept `labels` aligned with `input_ids` and shift the logits and labels internally. In that setup, the label stored at the first response-token position must be the first response token, while preceding prompt positions use `-100`. Applying an additional manual shift can drop the first response target or score the wrong boundary token.

## A small batch inspection catches most bugs

Before a long SFT run, I would decode one batch and print four aligned rows:

1. token positions
2. input token IDs or token strings
3. target labels
4. a Boolean indicator for positions included in the loss

Check that the first response token, the final response token, and the end token are included. Verify that system, user, padding, and any environment-provided tool-result spans are excluded under the chosen objective. Also confirm that each batch contains at least one valid target, since a sample with every label set to `-100` can produce an undefined mean loss in some implementations.

I would then report response-token loss using the number of unmasked tokens as the denominator. Comparing that value across masking schemes is still imperfect because the evaluated token sets differ. Generated responses on a held-out instruction set provide the more useful comparison.

The [instruction-finetuning FAQ](https://sebastianraschka.com/faq/docs/instruction-finetuning-practical-usefulness.html) explains how prompt-response demonstrations change a base model’s behavior. The [input-target construction FAQ](https://sebastianraschka.com/faq/docs/input-target-pretraining-examples.html) covers shifting, padding, stride, and tensor shapes for causal language modeling.
