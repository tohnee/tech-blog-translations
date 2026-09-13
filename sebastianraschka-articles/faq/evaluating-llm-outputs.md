---
title: "Evaluating LLM Outputs and Open-Ended Answers"
source: https://sebastianraschka.com/faq/docs/evaluating-llm-outputs.html
crawled: 2026-09-06
---

# Evaluating LLM Outputs and Open-Ended Answers

LLM outputs are difficult to evaluate because an open-ended prompt can have many acceptable answers. Two responses may use different wording and still be equally correct. A third response may sound fluent while containing a subtle factual error.

I would start by asking what kind of failure the evaluation needs to detect. If the output has a verifiable result, direct checks are usually preferable. Examples include exact match for a short factual answer, unit tests for generated code, schema validation for JSON, or task success in an application. These checks are reproducible and inexpensive.

Constrained benchmarks use the same idea. Multiple-choice and short-answer datasets can measure a defined capability at scale. Their scores are easy to compare, although they cover only the behavior represented by their questions. Public benchmarks may also suffer from training-data contamination or become less informative as models are tuned to them.

Reference-overlap metrics are another automatic option. They work best when matching the wording of a reference matters. For an explanation or summary, however, a low-overlap answer can still be good, and a high-overlap answer can copy the reference while missing the user’s actual request.

Human evaluation is useful once correctness or quality requires interpretation. Reviewers can apply a rubric, score individual responses, or compare two models side by side. Pairwise comparisons are often easier than assigning an absolute score. Human review also has costs: raters may disagree, domain experts are expensive, and a large evaluation set takes time.

An **LLM-as-a-judge** setup applies a similar rubric with another language model. The judge receives the prompt, the candidate output, and sometimes a reference answer. It then returns a score or preference. Chapter 7 of the repo demonstrates this workflow with a local model served through Ollama as well as an OpenAI API model.

![The local evaluation workflow in the repo uses an external LLM through Ollama as a judge](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/ollama-eval/ollama-serve.webp)

Model-based judging is convenient for running the same evaluation across thousands of outputs. Its scores are still model predictions. A judge may favor a particular writing style, longer responses, or answers that resemble its own output. It can also miss the same domain error as the model being evaluated.

For that reason, I would first test the judge on a smaller set reviewed by people who understand the task. The prompt and rubric should be fixed before comparing systems. For pairwise judging, swapping the response order is a useful check for position bias. Hiding model names avoids an unnecessary source of bias as well.

Application evaluation can add signals that offline benchmarks miss. A retrieval assistant might be measured by citation correctness and whether the cited passage supports the answer. A coding assistant can be judged by tests passed, edit acceptance, and time saved. Latency and serving cost should be tracked separately from response quality because a slower model may obtain a better quality score by using a much larger inference budget.

A useful evaluation suite therefore contains several measurements. Direct task checks cover what can be verified automatically. Human review establishes a trusted quality sample. LLM judges can extend that rubric to a larger set after their agreement with the trusted sample has been measured.
