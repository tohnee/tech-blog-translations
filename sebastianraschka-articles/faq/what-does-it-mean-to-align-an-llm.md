---
title: "What LLM alignment means"
source: https://sebastianraschka.com/faq/docs/what-does-it-mean-to-align-an-llm.html
crawled: 2026-09-06
---

# What LLM alignment means

To **align an LLM** means to make its behavior more reliably match an explicit specification for its intended use. That specification may cover instruction following, factual accuracy, uncertainty, response style, safety policies, and tool-use boundaries.

Alignment is always relative to a target. Users, application developers, annotators, and affected third parties can want different things. Calling a model “aligned” is therefore incomplete unless we also say whose instructions or preferences it should follow, under which conditions, and how conflicts are resolved.

## Alignment is a behavioral objective

A base model is trained to predict the next token in text drawn from its pretraining distribution. It may have broad knowledge and useful capabilities, yet still continue the wording of a request, imitate an undesirable passage, or give a confident answer when the evidence is weak.

Post-training changes the probabilities of these possible responses. For a benign question, the desired behavior may be a direct and accurate answer. For a harmful request, the desired behavior may be a refusal that still offers safe information. For an ambiguous prompt, the model may need to state an assumption or ask for clarification.

This behavioral view makes two distinctions useful. **Finetuning describes a training method. Alignment describes a training or system objective.** A domain finetune that teaches legal vocabulary is not automatically an alignment step. Also, safety is one alignment target among several. A model that refuses every request may score well on a narrow harmful-request test while being poorly aligned for normal users.

The boundaries between capability and alignment are not clean. Instruction data can teach a model new procedures, and reinforcement learning with verifiable rewards can improve problem solving. Still, the term alignment usually emphasizes which available behavior the model selects and how consistently it follows the intended specification.

| Target | Example of an undesirable behavior |
| --- | --- |
| Instruction adherence | Ignores the requested format or completes the prompt as plain text |
| Helpfulness | Gives an irrelevant, evasive, or needlessly long response |
| Truthfulness and calibration | States an unsupported claim with high confidence |
| Safety | Assists with a harmful request or refuses a benign one |
| Control | Ignores tool permissions, role instructions, or application constraints |

The classic [InstructGPT paper](https://arxiv.org/abs/2203.02155) framed this problem as aligning language models with user intent. Its pipeline used demonstrations and ranked model outputs to improve instruction following, truthfulness, and toxicity-related behavior. The paper operationalized alignment through measurable targets for one deployment setting. Those targets do not exhaust the possible meanings of human values.

## Instruction finetuning establishes the basic policy

Supervised instruction finetuning usually provides the first post-training stage. Each example contains a prompt and a desired response. The next-token loss increases the likelihood of that response when the model sees a similar prompt.

![Instruction finetuning uses demonstrations that pair a request with the response behavior the model should learn.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/instruction-following.webp)

This stage teaches basic assistant behavior, task formats, response style, and the chat template. It can show how to answer a question, summarize a document, produce JSON, or refuse a prohibited request. The [pretraining and instruction-finetuning FAQ](https://sebastianraschka.com/faq/docs/pretraining-vs-finetuning-vs-instruction-finetuning.html) explains how this differs from the base model’s original objective.

A demonstration gives one target answer. It does not directly express that one response is better than another plausible response. This is where preference data adds information.

## Preference optimization refines choices among responses

A preference record presents the same prompt with two or more responses and indicates which one is preferred. The difference might concern correctness, clarity, concision, tone, or policy compliance.

Classic reinforcement learning from human feedback (RLHF) fits a reward model to these rankings and then optimizes the language model against that learned reward. Direct Preference Optimization (DPO) updates the policy directly from chosen and rejected responses, using a reference policy as an anchor. The [RLHF and DPO comparison](https://sebastianraschka.com/faq/docs/rlhf-vs-dpo.html) covers the two objectives in detail.

![A classic RLHF pipeline combines supervised finetuning, human response rankings, a reward model, and policy optimization.](https://sebastianraschka.com/images/LLMs-from-scratch-images/dpo/4.webp)

The feedback does not have to come from one source. Human reviewers can apply a rubric. A model can critique responses using written principles, as demonstrated in [Constitutional AI](https://arxiv.org/abs/2212.08073). Code tests, mathematical answer checkers, and format validators can provide verifiable rewards for narrower tasks. Each source encodes a different proxy for the desired behavior.

At the model level, all of these methods eventually alter token probabilities. They do not install a symbolic rule that is guaranteed to fire in every context. A response pattern that worked on the training distribution can fail under a new language, unusual framing, long conversation, or adversarial prompt.

## The reward signal can be wrong

Human preferences are noisy and context dependent. Reviewers may disagree or lack the expertise needed to verify a technical answer. Pairwise labels can favor a polished but incorrect response, and a chosen answer may simply be less bad than its rejected alternative.

A learned reward model adds another approximation. If it rewards length, confidence, or a familiar writing pattern, strong policy optimization may exploit that shortcut. This behavior is often called **reward hacking** or **overoptimization**. DPO avoids a separate reward model. It can still learn artifacts and biases present in its preference pairs.

Several visible alignment failures follow from imperfect targets.

- **Sycophancy** occurs when the model agrees with a user’s premise instead of correcting it.
- **Overrefusal** occurs when safety training blocks harmless requests that resemble risky ones.
- **Style over substance** occurs when a polished format receives preference even though correctness does not improve.
- **Capability regression** occurs when post-training degrades useful behavior from the starting checkpoint.

Regularization against a reference model, conservative training, balanced data, and capability-retention tests can reduce these failures. They do not eliminate the need to inspect actual outputs.

## Model alignment is one layer of system safety

Weight updates are one part of a deployed assistant. System prompts specify roles and priorities at inference time. Retrieval can ground an answer in approved sources. Tool permissions and sandboxing limit which actions are possible. Input and output filters, rate limits, logging, and human escalation address risks that the model policy alone cannot reliably control.

These components should be evaluated together. A model may follow tool instructions well in isolation and still be unsafe if the application grants excessive permissions. Conversely, a strong access-control boundary can prevent an action even when the model proposes it.

## How alignment should be evaluated

There is no single alignment score. I would translate the intended specification into separate evaluations for task success, factual correctness, calibration, instruction conflicts, harmful-request handling, false refusals, and retained capabilities. Human reviewers are useful for open-ended judgments, while unit tests, citations, schemas, and other direct checks should be used whenever the result is verifiable.

The evaluation set also needs prompts outside the post-training distribution. Multilingual inputs, long conversations, prompt injection attempts, subtle policy boundaries, and unfamiliar domains often reveal failures hidden by average benchmark scores. The [LLM evaluation FAQ](https://sebastianraschka.com/faq/docs/evaluating-llm-outputs.html) discusses how to combine direct checks, human review, and model-based judging.

In practical LLM development, alignment is an iterative process. A team writes a behavioral specification, collects demonstrations or preferences, trains the model, evaluates failures, and updates both the data and the surrounding system. The resulting model can be better aligned for that application while remaining imperfect or unsuitable for another one.
