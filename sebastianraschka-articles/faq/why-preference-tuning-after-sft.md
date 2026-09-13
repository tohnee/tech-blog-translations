---
title: "Why preference tuning often follows SFT"
source: https://sebastianraschka.com/faq/docs/why-preference-tuning-after-sft.html
crawled: 2026-09-06
---

# Why preference tuning often follows SFT

Preference tuning can improve a supervised-finetuned model because the two stages provide different training signals. **Supervised finetuning (SFT)** increases the likelihood of a demonstrated response. **Preference tuning** compares plausible responses to the same prompt and teaches the model which one should be more likely.

The common order is SFT first and preference optimization second. SFT establishes basic instruction following, response formatting, and task behavior. The preference stage then adjusts choices among responses the model can already produce. This order is useful, although it is not a mathematical requirement of every preference objective.

## A demonstration and a preference pair say different things

An SFT record contains a prompt \(x\) and a target response \(y^\*\). The token-level objective increases \(\log \pi\_\theta(y^\* \mid x)\). The target can demonstrate the desired tone, format, facts, and level of detail, but it does not identify which parts distinguish it from another acceptable answer.

A preference record contains the same prompt with a chosen response \(y\_w\) and a rejected response \(y\_l\). The label says that \(y\_w\) is better under the annotation criteria. It does not claim that \(y\_w\) is the only valid answer or that \(y\_l\) is entirely wrong.

![A preference example places two plausible responses to the same prompt side by side so a reviewer can choose between their response styles](https://sebastianraschka.com/images/LLMs-from-scratch-images/dpo/2.webp)

Suppose both answers correctly explain gradient descent. One follows the requested two-sentence limit, while the other gives a page-long derivation. An SFT example can show the concise answer. A chosen-rejected pair additionally states that concision is preferred over the particular verbose alternative for this prompt.

This relative information is useful for qualities with several valid realizations. Common examples include response length, organization, tone, refusal boundaries, uncertainty wording, and how directly the answer addresses the question. Preference data can also target factual or task correctness when reviewers or automatic checks can identify the better response.

## Why SFT is a useful starting policy

Starting preference optimization from an instruction-tuned checkpoint solves several practical problems.

First, the model already knows the chat template and basic assistant role. Preference learning can focus on narrower behavioral distinctions instead of spending its limited comparison data on elementary formatting and instruction-following failures.

Second, an SFT model can generate the candidate responses used to construct preference pairs. These candidates tend to be plausible enough that reviewers compare meaningful differences. If every rejected response is obviously broken, the preference dataset teaches an easy separation and provides little information about subtle quality boundaries.

Third, common preference methods use the SFT checkpoint as an anchor. Standard Direct Preference Optimization (DPO) compares the chosen-rejected likelihood ratio under the trainable policy with the same ratio under a frozen reference policy. Classic reinforcement learning from human feedback (RLHF) commonly adds a KL penalty against a reference policy during policy optimization. In both cases, an SFT checkpoint is a sensible reference because it already has behavior worth retaining.

Finally, SFT provides a baseline. The team can measure exactly what preference tuning improves and what it degrades. Without that comparison, a polished response style can hide losses in factual accuracy, coding ability, calibration, or instruction adherence.

| Stage | Typical training record | Main signal | Useful for |
| --- | --- | --- | --- |
| SFT | Prompt and target response | Increase likelihood of the demonstrated tokens | Basic instruction following, formats, and task behavior |
| Preference tuning | Prompt, chosen response, and rejected response | Increase the relative preference for the chosen response | Choosing among plausible behaviors under a rubric |

## Preference tuning changes relative likelihoods

The difference is easiest to see with DPO. For each pair, standard DPO raises the policy’s relative odds of the chosen response compared with the rejected response, measured against a frozen reference model. The loss therefore uses both responses. Training on the chosen response alone would be another SFT update and would omit the explicit comparison.

Classic RLHF uses the preference data differently. It first trains a reward model to predict which response people prefer. The policy then generates responses and is optimized against that learned reward, often with Proximal Policy Optimization (PPO). The reference-policy penalty controls how far the new policy moves.

![Classic RLHF learns a reward model and performs policy optimization, while DPO applies a direct objective to chosen-rejected response pairs](https://sebastianraschka.com/images/LLMs-from-scratch-images/dpo/5.webp)

DPO and RLHF can both follow SFT, yet they have different data flow and systems requirements. The [RLHF and DPO comparison](https://sebastianraschka.com/faq/docs/rlhf-vs-dpo.html) explains those differences and gives the standard DPO objective.

## SFT can already teach style

Preference optimization is not required for every style change. If the SFT demonstrations consistently use concise paragraphs, valid JSON, or a particular professional tone, the model can learn those patterns directly. A well-designed SFT dataset may solve the application problem by itself.

Preference data becomes attractive when the target is easier to judge than to demonstrate exhaustively. Reviewers may find it easier to choose the clearer of two explanations than to write an ideal answer from scratch. Comparisons can also expose boundaries. A chosen response and a slightly too verbose rejected response say more about the desired length than one isolated target response.

I would add preference tuning only for a measured failure that pairwise data represents well. If the SFT model already meets the held-out criteria, another stage introduces annotation, training, and regression risk without a clear benefit.

## Pair quality determines what the model learns

A preference label is only as specific as its rubric and candidate pair. If one response is shorter, more accurate, friendlier, and better formatted, the model cannot know which difference caused the preference. Pairs that isolate the intended criterion provide a cleaner signal.

The rejected response should also be plausible. Comparisons between an excellent answer and random text are easy to label but weak for refining an already competent model. Harder pairs can reveal whether reviewers truly prefer concision, stronger evidence, a safer refusal, or closer instruction adherence.

Preference sources have their own biases. Reviewers may favor longer answers because they appear more thorough, confident answers because they sound polished, or familiar phrasing because it is easier to read. A chosen answer can still contain a factual error if it was merely better than the alternative.

Synthetic preferences from another model can reduce annotation cost, although they inherit that judge model’s biases and blind spots. Verifiable signals are preferable when available. Unit tests, numerical answer checks, schema validation, and citation support can distinguish responses without relying entirely on subjective style judgments.

## Preference optimization can overshoot

Stronger optimization does not imply better behavior. A model can exaggerate a rewarded pattern, such as producing unnecessarily long answers, adding repetitive disclaimers, or refusing benign requests. RLHF can exploit weaknesses in a learned reward model. DPO avoids that separate reward model, but it can still overfit artifacts in the fixed preference pairs.

The reference policy, learning rate, preference strength, training duration, and data mixture all affect how far the policy moves. Conservative updates are often sensible when SFT performance is already good. Some recipes also retain an SFT loss or mix demonstration data into preference training to reduce regression.

Evaluation should compare the SFT and preference-tuned checkpoints on the same held-out prompts. I would report the targeted preference win rate together with factual correctness, format compliance, response length, false refusals, and important capabilities from the starting model. A style improvement should not compensate for a correctness regression hidden by an aggregate score.

The practical division of labor is straightforward. Use SFT to establish the behavior the model should be capable of producing. Add preference tuning when chosen-rejected comparisons capture a remaining decision boundary more clearly than additional demonstrations. The [DPO and SFT FAQ](https://sebastianraschka.com/faq/docs/dpo-vs-supervised-finetuning.html) provides a direct comparison of their training records and losses.
