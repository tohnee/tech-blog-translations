---
title: "How Instruction Finetuning Improves Base Models"
source: https://sebastianraschka.com/faq/docs/instruction-finetuning-practical-usefulness.html
crawled: 2026-09-06
---

# How Instruction Finetuning Improves Base Models

Instruction finetuning makes a base model easier to use by teaching it that a formatted user message should lead to an appropriate response. A base checkpoint has learned next-token prediction from broad text. If a prompt looks like the beginning of a web page or forum thread, the model may continue that pattern instead of answering the request directly.

The finetuning data supplies demonstrations. Each record contains an instruction, optional context, and a target response. Before training, these fields are serialized with the model’s chat template so role markers and separators appear exactly as they will at inference time.

![Instruction records are converted into a consistent prompt-response format before they are used for supervised finetuning](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/04.webp)

The optimization remains next-token prediction. Given the formatted prompt and the preceding response tokens, supervised finetuning increases the probability of the demonstrated response. Many implementations compute the direct loss only on assistant tokens. The system and user tokens still condition the response, but the training objective does not ask the model to reproduce those prompt tokens.

![Prompt-token targets can be masked so the loss directly scores the desired assistant response](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/13.webp)

This produces several practical changes. The model is more likely to answer instead of continuing the prompt, follow constraints such as “return valid JSON,” and use the expected chat roles. A diverse instruction dataset can also teach one checkpoint to switch among summarization, extraction, rewriting, classification, and question answering without a separate finetune for every task.

The response distribution reflects the demonstrations. If concise answers dominate the dataset, the model tends to become concise. If the records consistently include headings or step-by-step solutions, those patterns become more likely. This is why [dataset construction](https://sebastianraschka.com/faq/docs/build-instruction-dataset.html) and the chat template matter as much as the training loop. A checkpoint can perform poorly when inference uses a different template from the one used during finetuning.

Instruction finetuning mainly changes how pretrained capabilities are elicited and presented. It can teach narrow domain information contained in the responses, but it is not a dependable replacement for broad pretraining or retrieval. It also does not remove hallucinations or guarantee that a requested constraint will always be followed.

Preference methods such as [DPO](https://sebastianraschka.com/faq/docs/dpo-vs-supervised-finetuning.html) often come later. Supervised instruction finetuning shows the model one response to imitate. Preference optimization compares alternatives and adjusts which response characteristics the model favors. Tool-use and reasoning training are additional axes rather than automatic consequences of instruction tuning.

The amount and quality of finetuning still need control. Repetitive examples can imprint unwanted phrases, narrow data can reduce performance outside its domain, and aggressive optimization can move the checkpoint too far from useful pretrained behavior. A held-out set should test instruction following, formatting, factual accuracy, and the original capabilities that need to be retained.
