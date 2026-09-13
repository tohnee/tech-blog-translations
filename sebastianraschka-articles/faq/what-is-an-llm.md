---
title: "What is a large language model?"
source: https://sebastianraschka.com/faq/docs/what-is-an-llm.html
crawled: 2026-09-06
---

# What is a large language model?

A **large language model (LLM)** is a neural network trained to model token sequences using large amounts of data and compute. Given a sequence of tokens, a text-generating LLM produces a probability distribution over possible next tokens.

There is no official parameter count at which a language model becomes “large.” The term is relative to the models and hardware of its time. In current usage, it usually refers to a broadly pretrained model with enough capacity to support many language tasks instead of one model developed for each task.

Most current text LLMs use a decoder-only transformer architecture and learn through next-token prediction. These are common design choices, not requirements built into the definition. Encoder-only models such as BERT have also been described as large pretrained language models, and large language models can use architectures other than transformers.

## What a text-generating LLM computes

Suppose the prompt is `Every effort moves you`. A GPT-style model processes it as follows.

1. A tokenizer converts the text into token IDs. The tokenizer belongs to the model pipeline, but it usually sits outside the neural network itself.
2. Embedding tables convert each token ID into a vector and add information about its position in the sequence.
3. A stack of transformer blocks updates those vectors. Causal self-attention lets each position use earlier tokens, while the feed-forward layers transform each position separately.
4. A final linear layer produces one **logit** for every vocabulary token at every input position.
5. During generation, the logits at the last position are converted into probabilities. The decoder selects one token, appends it to the input, and repeats the process.

![A GPT-style language model maps input text to token IDs, produces vocabulary logits, and decodes selected token IDs back into text](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/gpt-process.webp)

The model therefore generates text one token at a time. A token can be a word, part of a word, punctuation, whitespace, or another symbol, depending on the tokenizer. The [tokenization FAQ](https://sebastianraschka.com/faq/docs/tokenization-bpe.html) explains why this representation is used, and the [autoregressive generation FAQ](https://sebastianraschka.com/faq/docs/autoregressive-text-generation.html) covers the decoding loop in more detail.

## How next-token pretraining works

During pretraining, the targets come from the text itself. For a token sequence (x\_1, x\_2, \ldots, x\_T), the model learns conditional probabilities such as

[
p(x\_t \mid x\_1, \ldots, x\_{t-1}).
]

Each training example is shifted by one position. The input may contain tokens (x\_1) through (x\_{T-1}), while the targets contain (x\_2) through (x\_T). A cross-entropy loss measures how much probability the model assigned to the actual next tokens, and gradient-based optimization adjusts the model’s parameters.

Training can evaluate all target positions in a sequence in parallel because the causal mask prevents a position from seeing future tokens. Generation remains sequential because the next model input depends on the token that was just selected. This distinction is covered in the [next-token prediction FAQ](https://sebastianraschka.com/faq/docs/next-token-prediction.html).

Learning this objective across books, articles, code, and other text gives the model a strong incentive to represent syntax, semantics, factual associations, writing formats, and recurring problem-solving patterns. These regularities are distributed across numerical parameters. They do not provide the exact retrieval guarantees of a database, which is one reason an LLM can produce fluent but incorrect text.

## How modern LLMs differ from earlier language models

Language modeling predates transformers by decades. The main model families differ in how they represent context and how efficiently they can learn from large datasets.

| Model family | How it uses context | Practical limitation |
| --- | --- | --- |
| *n*-gram model | Counts how often short token sequences occur | Uses a fixed, short window and needs smoothing for unseen sequences |
| Feed-forward neural language model | Learns embeddings but still reads a fixed-size window | Cannot directly use tokens outside that window |
| RNN or LSTM | Processes tokens sequentially and carries a hidden state forward | Sequential training is harder to parallelize, and long-range information can be difficult to preserve |
| Transformer language model | Uses self-attention over the available context | Scales well on parallel hardware, although standard attention becomes costly as the context grows |

Transformers made it practical to train larger models on larger datasets. Their learned token representations also allow statistical evidence to be shared across related contexts. Scaling the same general architecture then produced models that could perform many tasks through prompting or modest additional training.

The GPT-2 family illustrates how parameter count can change within one architecture family. Its four standard sizes ranged from 124 million to 1.558 billion parameters by changing the width, number of attention heads, and number of repeated transformer blocks.

![The GPT-2 family scales one decoder-only transformer design by varying its width, attention heads, layers, and total parameter count](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/gpt-sizes.webp)

Those models were considered large when released. Current model families span a much wider range, including compact models with a few billion parameters and mixture-of-experts models with many total parameters but fewer active parameters per token. Parameter count is therefore most useful when it is reported together with the architecture, training data and compute, and evaluation results.

## An LLM is not automatically a chat assistant

Broad next-token pretraining produces a **base model**. A base model can answer some questions and follow patterns present in its prompt, but its training objective is text continuation. It has not necessarily been trained to interpret every prompt as a user request.

Instruction finetuning and preference optimization can turn that base checkpoint into an **instruct model** that follows requests more reliably. Additional training can emphasize tool use, safety policies, coding, or multi-step reasoning. The [base, instruct, and reasoning model FAQ](https://sebastianraschka.com/faq/docs/base-vs-instruct-vs-reasoning-model.html) explains these labels.

![Pretraining produces a foundation model that can later be finetuned for a classifier or an instruction-following assistant](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/chapter-overview.webp)

This also explains why the same pretrained model can support summarization, classification, question answering, code generation, and many other tasks. Pretraining creates reusable internal representations. Prompting, finetuning, or a task-specific output layer then steers those representations toward a particular use.

## What the LLM label does not tell us

Calling a system an LLM leaves several important questions unanswered.

- **Quality:** A larger parameter count does not by itself guarantee better accuracy, reasoning, or efficiency.
- **Freshness:** The model’s parameters reflect its training process. Current information requires updated training data or an external source.
- **Memory:** The context window is temporary input, not persistent memory across independent conversations.
- **Reliability:** Next-token prediction can produce plausible statements that are unsupported or wrong.
- **Access:** Open-weight, hosted API, and proprietary models can all be LLMs.
- **Modality:** A system that also processes images or audio is often called a multimodal LLM, although **large multimodal model** is the more precise term for the complete system.

For a current generative model, the most informative description includes its architecture, parameterization, context length, pretraining objective, post-training stage, and intended use. The acronym alone identifies a broad model class rather than a complete technical specification.
