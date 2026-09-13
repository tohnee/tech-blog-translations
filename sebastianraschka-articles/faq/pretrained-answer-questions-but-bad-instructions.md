---
title: "Why Pretrained LLMs Struggle to Follow Instructions"
source: https://sebastianraschka.com/faq/docs/pretrained-answer-questions-but-bad-instructions.html
crawled: 2026-09-06
---

# Why Pretrained LLMs Struggle to Follow Instructions

A pretrained base model can answer many questions because next-token pretraining exposes it to factual statements, explanations, dialogues, code, and question-answer patterns. It may still follow instructions inconsistently because the pretraining objective does not specifically reward satisfying a user’s request, respecting every constraint, or returning a particular format.

Consider a prompt that ends with “Question: What is the capital of France? Answer:”. This resembles a common text pattern, so a base model may continue with “Paris.” The answer can emerge from ordinary continuation. If the request instead asks for a one-field JSON object with an exact key and no additional text, the model must also identify and obey several behavioral constraints. Broad pretraining may contain examples of those patterns, but it does not apply a dedicated penalty whenever the model ignores one.

The distinction is easier to understand as **capability versus response policy**. Pretraining supplies much of the language ability, factual association, and task knowledge. Post-training changes how those capabilities are selected and presented when the input comes from a user.

During pretraining, every document contributes next-token targets. The model learns to continue tutorials, news articles, forum threads, transcripts, and many other formats. These sources do not share one assistant policy. Some contain direct answers, while others contain debates, unfinished questions, quoted mistakes, or several conflicting viewpoints. The objective asks the model to approximate this broad text distribution.

![Next-token pretraining maps a text prefix to likely continuations, which can include question-answer patterns without defining a single assistant behavior.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/gpt-process.webp)

This explains several common base-model behaviors. The model may repeat the question, continue writing both sides of a conversation, add a second question, or imitate the style of a web page. These outputs can be plausible continuations even when they are poor responses to the user’s intent. A base checkpoint also has no guaranteed interpretation for the system, user, and assistant role markers used by a particular chat application.

Prompting can often reveal more of the pretrained capability. A question-answer prefix, a few worked examples, or a clear completion pattern gives the model a local format to continue. This is in-context learning. It can improve behavior without changing the weights, although reliability still depends on the prompt and the model’s capacity.

**Supervised instruction finetuning** provides a more direct training signal. Each example contains a formatted instruction and a desired response. The optimization usually remains next-token prediction, but the high-quality response tokens now receive probability in the exact prompt-to-response context expected at inference time.

![Instruction finetuning teaches a formatted user request to lead to an appropriate assistant response.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/instruction-following.webp)

Across many examples, the model learns recurring behavioral patterns. It becomes more likely to answer directly, respect requested formats, stop at the appropriate point, and switch between tasks based on the instruction. The underlying knowledge often came primarily from pretraining. Instruction finetuning makes that knowledge easier to elicit through a user-facing interface.

The **chat template** is part of this training distribution. It serializes roles and separators into tokens. An instruct checkpoint can perform much worse when inference uses a different template or omits required control tokens. The visible wording of a prompt may be correct while its token-level framing is unfamiliar to the model.

![A consistent prompt template connects the instruction records used during finetuning with the format supplied at inference time.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/prompt-style.webp)

Many pipelines add **preference optimization** after supervised finetuning. A preference dataset compares candidate responses and indicates which one better matches criteria such as helpfulness, concision, or tone. Methods such as [DPO](https://sebastianraschka.com/faq/docs/dpo-vs-supervised-finetuning.html) or reinforcement learning then shift probability toward preferred behavior. This stage addresses choices that a single reference response may not characterize well.

The stages are not perfectly separated. Pretraining data can contain instructions, supervised finetuning can teach narrow facts or skills, and preference training can affect task performance. Still, the decomposition is useful:

- pretraining learns a broad model of text and supplies general capabilities
- supervised instruction finetuning teaches prompt-to-response behavior
- preference or reinforcement-based training adjusts which acceptable behaviors the model favors

Instruction tuning cannot guarantee compliance. The model may still miss a constraint when instructions conflict, the context is long, the task exceeds its capabilities, or the requested format was poorly represented in the finetuning data. It can also produce a well-formatted incorrect answer. Factual accuracy and instruction adherence should therefore be evaluated separately.

For a practical comparison, use base and instruct checkpoints from the same family and tokenizer. Test direct factual questions, unfamiliar wording, multi-part constraints, and exact output formats under their intended templates. This separates knowledge that was already present from behavior made more reliable by post-training.

The related FAQ [How does instruction finetuning make a base model more useful in practice?](https://sebastianraschka.com/faq/docs/instruction-finetuning-practical-usefulness.html) follows the training setup in more detail. [What is the difference between a base model, an instruct model, and a reasoning model?](https://sebastianraschka.com/faq/docs/base-vs-instruct-vs-reasoning-model.html) places these checkpoints in the broader model-development pipeline.
