---
title: "Exact Match vs. LLM-as-a-Judge Evaluation"
source: https://sebastianraschka.com/faq/docs/exact-match-vs-llm-as-a-judge.html
crawled: 2026-09-06
---

# Exact Match vs. LLM-as-a-Judge Evaluation

Use **exact match** when the expected answer has one canonical representation. Classification labels are the clearest example. If the allowed outputs are `positive` and `negative`, comparing the generated label with the reference gives an unambiguous result.

Short factual answers can also work if the evaluation defines acceptable normalization in advance. For instance, case folding and removing surrounding whitespace may be reasonable when comparing `Madison` with `madison`. The normalization should reflect the task rather than be adjusted after seeing the model’s mistakes.

![Classification-style outputs are a good example of when constrained metrics are natural and reliable](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch06_compressed/class-argmax.webp)

Exact string matching is stricter than deterministic evaluation in general. Two JSON objects can be equivalent even when their key order or whitespace differs, so I would parse the JSON and compare the required fields. Generated code is better evaluated with unit tests. For a numerical problem, a tolerance or symbolic-equivalence check may be more appropriate than comparing character strings.

These automated checks are attractive because they are reproducible, inexpensive, and easy to audit. They become brittle when the surface form can vary. A correct explanation may use different examples, sentence order, or terminology than the reference answer and receive a score of zero under exact match.

An **LLM-as-a-judge** evaluator is useful for this open-ended case. The judge receives the original prompt and the candidate response, often together with a reference answer or supporting material. A rubric tells it what to evaluate. For a summary, the criteria might include factual consistency, coverage of the source, and adherence to the requested length.

![The repo's chapter 7 evaluation workflow uses an external model through Ollama as a judge for open-ended instruction responses](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/ollama-eval/ollama-serve.webp)

Judge scores need calibration. Language models can favor longer responses, respond differently when the candidate order is reversed, or miss specialized factual errors. I would compare the judge with a smaller human-reviewed set before using it at scale. Pairwise evaluations should randomize response order, and model names should be hidden from the judge.

Many evaluations benefit from both methods. A structured answer can first pass deterministic checks for valid syntax, required fields, and numerical constraints. The judge can then assess whether the explanation is relevant and well supported. Keeping these scores separate makes failures easier to diagnose than asking one judge for a single overall number.

My practical boundary is the answer representation. If correctness can be defined with a canonical form or an executable check, I use that direct evaluator. When valid responses differ in content and presentation, I add a rubric-based judge and retain human review as the calibration reference.
