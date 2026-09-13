---
title: "What LLM pretraining teaches"
source: https://sebastianraschka.com/faq/docs/what-pretraining-teaches.html
crawled: 2026-09-06
---

# What LLM pretraining teaches

Pretraining teaches an LLM to predict likely continuations of token sequences. To do this well across many kinds of text, the model learns useful representations of language structure, meaning, factual associations, writing formats, and recurring procedures.

The word “teach” is convenient shorthand. The model is not given a lesson about grammar or a table of facts. Gradient-based optimization changes its numerical parameters whenever its next-token predictions disagree with the text in a training batch. The resulting representations emerge from many such updates.

## Where the training signal comes from

For a token sequence (x\_1, x\_2, \ldots, x\_T), a causal language model estimates

[
p(x\_t \mid x\_1, \ldots, x\_{t-1}).
]

The input and target sequences are offset by one token. If the input is `[The, sky, is]`, the corresponding targets are `[sky, is, blue]`. The prediction at each position is scored against the token that actually followed that prefix in the corpus.

![A token sequence supplies its own training targets by shifting the token IDs one position to the left](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/inputs-targets.webp)

Cross-entropy assigns a larger loss when the model gives the observed token a low probability. Backpropagation computes how each parameter contributed to that loss, and the optimizer applies a small update. A chunk containing (T+1) token IDs can supply (T) next-token targets in one forward pass because causal masking prevents each position from reading later tokens.

This setup is called **self-supervised learning**. Human annotators do not have to write a label for every token. The continuation already present in the text supplies the target. Calling the data “unlabeled” does not mean the dataset appeared without human decisions. Collection, filtering, deduplication, language balance, document boundaries, and removal policies all influence what the model can learn.

The [input-target construction FAQ](https://sebastianraschka.com/faq/docs/input-target-pretraining-examples.html) follows the batching and shifting process in more detail.

## Why next-token prediction teaches more than local word order

The correct continuation often depends on information at several levels. Predicting a verb ending may require grammatical agreement with an earlier noun. Completing a function may require tracking variable names and indentation. Continuing a technical explanation may require the definition introduced several paragraphs earlier.

A model that reduces next-token loss across a broad corpus can acquire several kinds of regularities.

| Regularity | What the model can use it for | Important boundary |
| --- | --- | --- |
| Syntax and morphology | Word order, agreement, inflection, and well-formed sentences | Rare constructions and unfamiliar languages may remain difficult |
| Semantics | Relations among words, phrases, entities, and concepts | Similar wording does not guarantee the same meaning |
| Factual associations | Common names, dates, properties, and relationships found in text | Associations can be outdated, conflicting, or wrong |
| Discourse and style | Paragraph structure, tone, genre, and document format | Style imitation does not establish factual accuracy |
| Task patterns | Question answering, translation, classification, summarization, and code completion | Prompting can expose a pattern without making it reliable |
| Procedures | Multi-step calculations, algorithms, and recurring problem-solving traces | Approximate pattern learning can fail on a new combination or longer sequence |

These categories are connected. To predict the next token in `The capital of France is`, the model needs the phrase pattern and an association between France and Paris. To continue a Python function, it may need syntax, local variable relationships, and procedural patterns at the same time.

![A pretrained GPT-style model turns each token prefix into a distribution over possible vocabulary continuations](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/gpt-process.webp)

Large and varied datasets provide many overlapping examples of the same underlying relationship. Parameter sharing lets an update from one context affect predictions in related contexts. This is how a model can produce a sensible continuation that never appeared verbatim in its training data.

## Generalization and memorization can both occur

Pretraining is sometimes described as statistical compression. The model cannot retain an ordinary searchable copy of a very large corpus in its weights. It learns parameter configurations that predict many sequences well. Common patterns therefore tend to be represented in ways that apply across examples.

Exact memorization can still occur. A model may reproduce a frequently repeated passage, a distinctive rare string, or a training example that received enough effective exposure. Model size, repetition, data duplication, and sequence uniqueness all affect this behavior.

The two outcomes are not cleanly separable. A generated sentence can combine a memorized fragment with a generalized grammatical or factual pattern. This is why dataset deduplication, contamination checks, and held-out evaluation matter. A low next-token loss alone does not show which mechanism produced a correct answer.

## What pretraining does not directly optimize

The pretraining objective rewards probability assigned to observed continuations. Several properties that users care about are outside that objective.

- **Truthfulness:** Training text includes errors, fiction, outdated material, and conflicting claims. The loss does not mark each statement as true or false.
- **Source attribution:** The model is usually trained to predict text without returning the document that supported each token.
- **Calibration:** Fluent text can receive high probability even when the model lacks reliable evidence for its claim.
- **Instruction adherence:** A base model learns many document and dialogue formats, but it is not consistently rewarded for satisfying a user’s request.
- **Safety and application policy:** The corpus does not define one policy for what a deployed assistant should produce.
- **Persistent memory:** Pretraining stores statistical information in model parameters. It does not remember a new conversation after that context is removed unless another system records it.

The dataset also limits what can be learned. Information absent from the corpus cannot be recovered reliably from the objective, and information after the training cutoff is unavailable unless the model receives it through updated training, retrieval, or tools. More parameters and compute can improve the fit to the available signal. They cannot correct every error in the source data.

## Why a pretrained model is called a base model

Pretraining produces a **base model** whose central behavior is text continuation. A prompt such as `Question: What is the capital of France? Answer:` resembles a familiar document pattern, so the model may continue it correctly. A less familiar request with several formatting constraints may produce inconsistent results.

Instruction finetuning supplies explicit prompt-response demonstrations. Preference optimization can then favor responses that better match criteria such as correctness, helpfulness, or style. These post-training stages change how the pretrained capabilities are selected and presented.

![Instruction finetuning pairs a user request with a desired response to teach behavior that broad text pretraining does not specify consistently](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/instruction-following.webp)

Post-training can also add narrow knowledge or skills, so the stages are not perfectly isolated. The useful distinction concerns the main training signal. Pretraining learns a broad distribution over text. Instruction and preference data shape the response policy expected from an assistant. The [base-model instruction-following FAQ](https://sebastianraschka.com/faq/docs/pretrained-answer-questions-but-bad-instructions.html) examines that difference with concrete prompt examples.

When evaluating what a particular pretrained model learned, I would therefore inspect more than generated samples. Validation loss measures predictive fit, task benchmarks probe selected capabilities, contamination checks test evaluation integrity, and targeted prompts reveal behavioral limits. Together, these checks give a more accurate picture than treating next-token prediction as either simple memorization or a guarantee of general intelligence.
