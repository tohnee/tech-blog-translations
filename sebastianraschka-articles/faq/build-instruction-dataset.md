---
title: "What are good ways to build an instruction dataset from scratch?"
source: https://sebastianraschka.com/faq/docs/build-instruction-dataset.html
crawled: 2026-09-06
---

# What are good ways to build an instruction dataset from scratch?

Start by writing down the behavior that the finetuned model should learn. A dataset for summarizing scientific articles needs different prompts and answers than one for customer support or code generation. This scope determines which tasks belong in the dataset and what a good response looks like.

Next, choose one record format and use it consistently. The chapter 7 examples in the repo use fields such as `instruction`, `input`, and `output`. The input field can be empty when the instruction contains all required context. During preprocessing, each record should map to the same chat template so the model can reliably distinguish the request from the desired response.

I would build a small seed set that is still practical to inspect line by line. The examples should come from real tasks the model is expected to handle. Within that scope, it helps to vary the prompt wording, response length, and difficulty. These variations should reflect actual use rather than artificial diversity for its own sake.

![Instruction tuning works best when examples consistently teach the model what a user request looks like and what a good response should look like](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/instruction-following.webp)

Create the training and evaluation splits early. Examples derived from the same source or prompt template should stay in one split. Otherwise, a synthetic paraphrase of a training prompt can leak into the evaluation set and make the results look better than they are.

Once the seed data is in good shape, an LLM can help expand it. The repo’s chapter 7 utilities include examples for generating instruction data with Llama 3 and Ollama, creating variants, and refining responses through reflection tuning. Synthetic output still needs quality control. I check for factual errors, ignored constraints, broken formatting, and answers that merely restate the prompt.

Deduplication should happen before training. Exact string matching catches repeated records, while similarity-based checks are useful for paraphrases and lightly edited copies. Duplicate prompts can overweight one behavior, and duplicates across splits contaminate the evaluation.

![The repo's reflection-tuning material shows an iterative dataset workflow in which generated responses are inspected and refined](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/reflection-tuning/reflection-tuning.webp)

Before starting a long finetuning run, I would do one more manual pass. Random samples help reveal systematic formatting problems. Difficult examples are useful for checking whether the expected answers are actually correct. It is also worth verifying that the data contains no private material and that its sources permit the intended use.

A modest set of reviewed examples is a reasonable first version. After training, error analysis can show which task types or response patterns are missing. That gives the next round of data collection a concrete purpose instead of increasing the row count blindly.
