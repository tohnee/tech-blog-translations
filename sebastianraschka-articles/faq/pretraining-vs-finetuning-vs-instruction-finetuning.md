---
title: "Pretraining vs. finetuning vs. instruction finetuning"
source: https://sebastianraschka.com/faq/docs/pretraining-vs-finetuning-vs-instruction-finetuning.html
crawled: 2026-09-06
---

# Pretraining vs. finetuning vs. instruction finetuning

**Pretraining** creates a general base model from a broad corpus. **Finetuning** is the umbrella term for adapting a pretrained checkpoint to a narrower purpose. **Instruction finetuning** is one type of supervised finetuning that uses prompt-response demonstrations to teach assistant-like behavior.

This hierarchy is important. Instruction finetuning is not a separate alternative to finetuning. It is a particular data format and training goal within the broader finetuning category.

| Stage | Typical starting point | Training data | Common output and loss | Result |
| --- | --- | --- | --- | --- |
| Pretraining | Randomly initialized model | Large tokenized text corpus | Vocabulary logits with next-token cross-entropy | Base model |
| Task finetuning | Pretrained checkpoint | Task inputs with labels or target outputs | Class loss or target-text loss | Specialized model |
| Instruction finetuning | Pretrained checkpoint | Formatted prompts and desired responses | Next-token loss, often on response tokens | Instruct model |

**Pretraining** uses self-supervision. A text sequence supplies its own labels because each observed token becomes the target for the preceding context. For a decoder-only LLM, the model produces vocabulary logits at every sequence position and minimizes average next-token cross-entropy. The [next-token-prediction FAQ](https://sebastianraschka.com/faq/docs/next-token-prediction.html) follows this calculation in detail.

![During pretraining, a GPT-style model maps token prefixes to vocabulary distributions for next-token prediction.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/gpt-process.webp)

Pretraining normally updates the full model over a very large and diverse corpus. The resulting base checkpoint has learned language structure, factual associations, code patterns, and other regularities found in the data. It is still optimized for text continuation rather than for one application or a consistent assistant policy.

**Task finetuning** starts from this pretrained representation and continues gradient-based training on a more focused dataset. The output interface depends on the task. Chapter 6 of the repo adapts a GPT model for spam classification by replacing the vocabulary head with a two-class output head. Cross-entropy then compares those class logits with spam and not-spam labels.

![Classification finetuning maps an input document to a fixed label set without requiring an instruction in the input.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch06_compressed/03.webp)

Classification is one example rather than the definition of finetuning. A summarization or translation finetune can keep the vocabulary head and train on input-output text pairs. Domain-specific continued pretraining can also start from an existing checkpoint and keep the original next-token objective on raw legal, medical, or code data. This latter procedure is often called **continued pretraining** or **domain-adaptive pretraining** because it adapts the model’s general text distribution before a task-specific stage.

**Instruction finetuning**, commonly called supervised finetuning or SFT in LLM post-training, also keeps the vocabulary output. Each record contains an instruction, optional input context, and a target response. A chat template serializes these fields with the same role markers and separators expected during inference.

![Instruction finetuning presents a task as a user request and trains the model to generate the desired response.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch06_compressed/02.webp)

The optimization can still be next-token cross-entropy. Many implementations mask the system and user target positions so that only assistant-response tokens contribute directly to the loss. The prompt remains visible as conditioning context. This data teaches the model to interpret a request, select an appropriate task behavior, and produce the expected response format.

Instruction datasets usually mix several tasks. One checkpoint may see examples for extraction, rewriting, classification, question answering, and structured output. This differs from a dedicated spam classifier, which maps every input into the same fixed label space. The [instruction-finetuning FAQ](https://sebastianraschka.com/faq/docs/instruction-finetuning-practical-usefulness.html) explains the prompt formatting and loss masking in more detail.

The boundaries are useful but not absolute. Instruction finetuning can introduce narrow domain knowledge contained in its responses. Task finetuning can also use natural-language instructions. The most reliable distinction comes from the intended behavior and the structure of the supervised targets.

Two other axes are often confused with these stages. **Full finetuning versus LoRA** describes which parameters are updated, not what task is learned. The same classification or instruction dataset can be used with full weight updates or a [parameter-efficient method such as LoRA](https://sebastianraschka.com/faq/docs/lora-vs-full-finetuning.html). **Preference optimization** uses chosen and rejected responses or reward signals. Methods such as [DPO](https://sebastianraschka.com/faq/docs/dpo-vs-supervised-finetuning.html) often follow SFT, but they use a different objective from demonstration-based instruction finetuning.

The amount of data is not the formal boundary either. Pretraining is usually much larger and more expensive than finetuning, although a long continued-pretraining run can be larger than a small model’s original training corpus. What matters is whether the process is creating a broad base model or adapting an existing checkpoint toward a target distribution or behavior.

For a practical choice, use continued pretraining when the model needs broad exposure to a new domain, task finetuning when the desired output has a narrow task definition, and instruction finetuning when one generative model should respond to varied user requests. A production instruct model may then receive preference or reasoning-oriented training as additional post-training stages.
