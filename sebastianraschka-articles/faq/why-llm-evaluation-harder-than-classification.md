---
title: "Why LLM evaluation is harder"
source: https://sebastianraschka.com/faq/docs/why-llm-evaluation-harder-than-classification.html
crawled: 2026-09-06
---

# Why LLM evaluation is harder

Open-ended LLM evaluation is harder because the evaluator must define both the desired behavior and how to score it. In ordinary classification, the output belongs to a fixed label set. Once the reference label is accepted, computing accuracy or F1 is mechanical.

This distinction needs one qualification. An LLM evaluated on multiple-choice questions, exact numerical answers, or executable code can still have a clear score. The difficult case is free-form generation, where several responses can be valid and quality has several dimensions.

## Classification usually has a bounded output space

Consider a spam classifier with two allowed labels. The model returns one score for `not spam` and another for `spam`. Taking the larger score produces one predicted class, which can be compared with the reference label.

![A text classifier converts a fixed set of output scores into one predicted label through argmax](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch06_compressed/class-argmax.webp)

The dataset can still contain ambiguous examples, incorrect labels, class imbalance, or distribution shift. Those are substantial evaluation problems. However, once the labels and metric are fixed, two evaluators will calculate the same accuracy from the same predictions.

Open-ended generation changes the output space from a small label set to sequences of arbitrary length. A prompt asking for an explanation can have many correct answers with different wording, organization, examples, and level of detail. One reference response is a useful example, but it is rarely the only acceptable response.

| Property | Classification | Open-ended generation |
| --- | --- | --- |
| Output space | Fixed set of labels | Very large set of token sequences |
| Reference | Usually one class label | Often one of many valid responses |
| Typical score | Accuracy, precision, recall, or F1 | Several task checks or rubric criteria |
| Partial credit | Defined through the metric or label structure | Often requires judging which parts are correct or missing |
| Evaluator ambiguity | Low after labels and metric are fixed | Can remain high even with a rubric |

## A generated response can be good in one way and poor in another

Suppose a prompt asks for a three-bullet summary of a technical report. One response may be factually correct but omit the main limitation. Another may cover every result in five bullets and violate the requested format. A third may be concise and well structured while misstating one number.

A single `correct` or `incorrect` label hides these differences. Useful criteria may include:

- factual correctness and support from the supplied source
- coverage of the information needed for the task
- relevance to the request
- instruction and format adherence
- clarity for the intended reader
- safety or policy compliance where applicable

The criteria can conflict. Adding caveats may improve completeness while making the response longer than requested. A numerical average can also hide a serious failure. A response that scores well on style and coverage should not pass if its central claim is wrong.

For this reason, I prefer separate criterion scores and explicit hard-failure checks over one unexplained quality number.

## Exact match is often too strict

Exact match works when the answer has a canonical form. It can score a classification label, a normalized short answer, or a known identifier. It fails on valid paraphrases. `The capital is Madison` and `Madison` differ as strings even though both may answer the same question correctly.

Reference-overlap metrics are less strict because they compare words or subsequences. They are useful when matching the reference wording matters. For explanations, summaries, and rewrites, high overlap can reward copying while low overlap can penalize an equally good formulation.

The best automatic evaluator often comes from the task rather than from general text similarity. Parse JSON and validate its schema. Run generated code against unit tests. Compare numerical answers within a specified tolerance. Check whether cited passages contain the claimed evidence. These methods turn part of an open-ended task into a reproducible test.

The [exact-match and LLM-judge FAQ](https://sebastianraschka.com/faq/docs/exact-match-vs-llm-as-a-judge.html) gives more examples of this boundary.

## Language-model loss answers another question

Cross-entropy and perplexity measure how much probability the model assigns to observed reference tokens. They are useful for evaluating predictive fit on a fixed corpus. They do not directly measure whether one generated response is factual, follows an instruction, or solves a user’s task.

Two models can have similar perplexity and different assistant behavior after post-training. Conversely, an instruction-tuned model can become more useful without improving perplexity on an unrelated pretraining corpus. The [perplexity FAQ](https://sebastianraschka.com/faq/docs/perplexity-what-it-means.html) covers the controlled comparisons for which that metric is appropriate.

## Generation can vary between runs

A deterministic classifier normally returns the same label for the same input and checkpoint. LLM generation may sample from the next-token distribution. Temperature, top-k, top-p, maximum output length, random seed, stop conditions, system prompt, and chat template can all change the response.

An evaluation should therefore record the full generation configuration. If the product samples responses, one output per prompt may give a noisy estimate. Multiple samples can measure the probability of success, although `pass@k` and best-of-k results give the model more attempts than a single production request. The number of attempts belongs in the reported metric.

Hosted model versions can change as well. A reproducible comparison should pin the model version when possible and retain the evaluated outputs.

## Human and model judges also need evaluation

Human reviewers can apply a rubric to free-form responses, but their judgments are not automatic ground truth. Reviewers may interpret criteria differently, overlook a domain error, or prefer a familiar writing style. Domain experts are often needed for technical correctness, which raises the cost of evaluating a large set.

Pairwise comparison can be easier than assigning an absolute score. A reviewer answers which of two responses is better under a stated criterion. This provides a relative preference rather than proof that the winner is good enough for deployment.

An **LLM-as-a-judge** can apply the same rubric at larger scale. Its output remains a model prediction. Judges can favor verbosity, react to candidate order, or miss errors outside their expertise. Model names and other irrelevant source information should be hidden, and response order should be randomized in pairwise tests.

I would calibrate a model judge on a smaller human-reviewed set before using it for the complete evaluation. Agreement should be checked separately for each criterion and important data slice. A judge that agrees on writing quality may still be unreliable on mathematical correctness or citation support.

## The benchmark can become part of the training target

Public LLM benchmarks are susceptible to contamination because their prompts and answers may appear in pretraining data, finetuning data, or model-development feedback. Repeated optimization against a popular leaderboard can also overfit design decisions to that benchmark without literal data leakage.

Benchmark coverage matters as much as contamination. An average score can hide failures on long prompts, non-English inputs, uncommon domains, or adversarial wording. A production evaluation should include representative private examples and report results by meaningful slices rather than only as one aggregate.

Small score differences also need uncertainty estimates. Paired comparisons on the same prompts, confidence intervals, or bootstrap estimates help distinguish a repeatable improvement from sampling noise. Human and model-judge disagreement should be included in that uncertainty rather than discarded silently.

## A practical evaluation stack

The evaluation process begins before generating model outputs. I would use the following order:

1. Define the task distribution, expected behavior, hard failures, and quality criteria.
2. Freeze a held-out prompt set with representative difficulty, domains, and input lengths.
3. Apply deterministic checks wherever the result can be parsed, executed, or verified directly.
4. Write a criterion-specific rubric for the remaining open-ended qualities.
5. Create a trusted human-reviewed subset and measure reviewer agreement.
6. Calibrate any LLM judge against that subset before scaling it to more outputs.
7. Freeze the model, prompt template, tools, retrieval corpus, and decoding settings for the comparison.
8. Report criterion scores, data slices, uncertainty, latency, token use, and cost separately.

![Instruction-model evaluation adds response extraction, qualitative inspection, and scoring after the model has been trained](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/22.webp)

The final step is error analysis. Inspect deterministic failures, judge-human disagreements, and examples near the decision boundary. These cases reveal whether the next improvement should target the model, prompt, retrieval system, tool integration, or evaluator.

The broader [LLM output evaluation FAQ](https://sebastianraschka.com/faq/docs/evaluating-llm-outputs.html) compares direct checks, human review, pairwise preferences, and model-based judging in more detail.
