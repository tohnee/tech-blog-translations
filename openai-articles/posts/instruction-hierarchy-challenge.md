---
title: "Improving instruction hierarchy in frontier LLMs"
date: 2026-03-10
source: https://openai.com/index/instruction-hierarchy-challenge/
crawled: 2026-09-13
category: research
---

AI systems often receive instructions from multiple sources. These can include safety policies from system messages, product guidance from developers, requests from users, and information found online. Training models to reliably prioritize the most trusted instructions among these sources is a key part of safe deployment.

Many AI safety and reliability issues can arise when this prioritization breaks down. Models may receive requests for disallowed content, attempts to reveal private information, or prompt‑injection attacks embedded in online data. Failing to behave appropriately in each of these scenarios shares the same root cause: the model may follow the wrong instruction.

When these instructions conflict, the model has to decide which ones to prioritize. If it treats an untrusted instruction as authoritative, the model may behave in ways that violate policies or developer and user intent.

We demonstrate that properly designed instruction-hierarchy tasks, which train models to prioritize instructions according to their trust level, improve several real-world safety properties. Models trained on these tasks become more responsive to safety specifications in system prompts (improving safety steerability) and more robust to prompt-injection attacks embedded in tool outputs.

## What instruction hierarchy is—and why it matters

To handle conflicts, OpenAI's models are trained to follow a clear instruction hierarchy:

**System > developer > user > tool**

Higher‑priority instructions are more trusted. The model should only follow lower‑priority instructions when they do not conflict with higher‑priority constraints. These principles are outlined in the [OpenAI Model Spec](https://model-spec.openai.com/2025-12-18.html#chain_of_command).

For example, if a system message includes a safety policy and a user asks the model to violate it, the model should refuse. If a tool output contains malicious instructions, the model should ignore them rather than treat them as commands.

Getting this right is foundational to safety, security, and reliability.

The model on the right correctly follows the Developer’s instruction, which is higher-priority, over the User’s when the two instructions conflict.

## Why large-scale instruction hierarchy training can be hard

Reinforcement learning is a natural fit for teaching the instruction hierarchy. We can generate conversations with conflicting instructions, prompt the model to respond, and reward it when it follows the correct instruction.

We’ve identified three pitfalls of naively applying that recipe:

- Instruction-following failures can double as instruction hierarchy failures: the model might fail to resolve an instruction conflict, not because it doesn’t understand the hierarchy of roles, but because the instructions themselves are too complicated.
- Instruction conflicts can be nuanced and even subjective. A common approach is to let a separate LLM judge assign rewards to the LLM being trained, but judges themselves are fallible.
- Models tend to learn [shortcuts that result in high reward, but are useless in practice](https://arxiv.org/pdf/2210.10760). The classic example is overrefusals: models can learn to maximize safety by refusing even benign requests.

## Our approach

We design IH-Challenge, a reinforcement learning training dataset, to address each of those pitfalls. We adhere to the following principles:

- Tasks are instruction-following-simple
- They are objectively-gradable with a simple Python script
- There are no trivial shortcuts that guarantee high reward across all tasks

Each task in IH-Challenge is essentially a conversation with the following messages:

- An instruction message from a high-privilege role, e.g. “Only answer ‘Yes’ or ‘No’”.
- An instruction message from a lower-privilege role, which attempts to get the model to violate the instructions in the higher-privilege message.

The model being trained generates the next message. We write the tasks/environments so that it is possible to programmatically check whether the model's response satisfies the higher-level constraint.

## Results and robustness

We train a model on IH‑Challenge and produce an internal model, which we call GPT‑5 Mini-R, with the following improvements:

- Performs better on instruction‑hierarchy benchmarks
- Improved performance generalizes to held‑out and adversarial instruction hierarchy tests
- Maintains overall usefulness, without collapsing into over‑refusal

This is what makes the approach especially compelling for safety: by directly training models to resolve instruction conflicts correctly on IH-challenge tasks, we get IH improvements that generalize to new attacks and new situations.

### Robustness on academic benchmarks

| **Eval** | **GPT‑5‑Mini** | **GPT‑5 Mini-R** |
| Gandalf Password (sys-user) | 0.99 | 0.99 **(+0)** |
| Gandalf Password (dev-user) | 0.98 | 1.00 **(+0.02)** |
| TensorTrust (sys-user) | 0.86 | 0.94 **(+0.08)** |
| TensorTrust (dev-user) | 0.76 | 0.91 **(+0.15)** |
| RealGuardrails (Distractors) | 0.88 | 0.95 **(+0.07)** |
| RealGuardrails (Handwritten) | 0.82 | 0.89 **(+0.07)** |
| System IFEval | 0.92 | 0.96 **(+0.04)** |

### Robustness on internal benchmarks

| **Eval** | **GPT‑5‑Mini** | **GPT‑5 Mini-R** |
| TutorJailbreak (sys-user) | 0.96 | 0.99 **(+0.03)** |
| Tutor Jailbreak (dev-user) | 0.97 | 0.99**(+0.02)** |
| System <> User Conflict | 0.84 | 0.95 **(+0.11)** |
| System <> Developer Conflict | 0.86 | 0.86 **(+0)** |
| Developer <> User Conflict | 0.83 | 0.95**(+0.12)** |

### No capability regressions

| **Eval** | **GPT‑5‑Mini** | **GPT‑5 Mini-R** |
| IH-Challenge (overrefusal) | 0.79 | 1.00 **(+0.21)** |
| TensorTrust (overrefusal) | 0.91 | 0.90 **(-0.01)** |
| GPQA Diamond | 0.83 | 0.83**(+0)** |
| AIME 2024 | 0.93 | 0.94 **(+0.01)** |
| Chat WinRate vs. o1 | 0.71 | 0.66**(-0.05)** |
| Preference Score | 0.46 | 0.40**(-0.06)** |

## Why this improves real-world safety and security

Stronger instruction hierarchy delivers multiple safety benefits at once, including in safety steerability and prompt injection robustness.

### Safety steerability

We evaluate safety steerability by adding category-specific safety specifications to the system prompt and measuring behavior on OpenAI’s safety Production Benchmarks (a set of safety-sensitive conversations representative of ChatGPT in production).

The IH-trained model shows a consistent improvement: with the safety spec present, it achieves higher refusal and safe completion rates across disallowed categories, indicating that stronger instruction hierarchy behavior makes it better at resolving conflicts when unsafe requests come from lower-priority instructions. Notably, this improvement does not come with a corresponding decrease in helpfulness rate (i.e., it is not becoming less “helpful” by simply refusing more overall).

### Prompt injection robustness: stronger resistance to malicious tool instructions

Example of how the IH-trained model resists prompt injections that GPT‑5 Mini (Baseline) falls for.

Instruction hierarchy is also central in resisting prompt injection, when malicious instructions are embedded in tool outputs. We evaluate the IH-trained model on two prompt injection benchmarks—an academic benchmark CyberSecEval 2 and an OpenAI internal prompt injection benchmark consisting of attacks like the one demonstrated on an older version of [ChatGPT Atlas](https://openai.com/index/hardening-atlas-against-prompt-injection/).

Relative to the baseline, the IH-trained GPT‑5 Mini-R model improves prompt injection robustness on both benchmarks and substantially improves performance on our internal static prompt injection evaluation in these experiments.

## Looking ahead

As models become more agentic—calling tools, reading untrusted documents, and taking actions in the world—the ability to consistently prioritize trusted instructions over untrusted ones becomes a core safety property.

This work shows that several pitfalls of IH robustness training can be overcome by designing training environments that address those pitfalls. Though our IH-Challenge dataset seems simple, the IH behavior models learn from these environments generalizes to more realistic, often not-objectively-gradable benchmarks.

Strengthening instruction hierarchy not only improves reliability, but unlocks multiple safety and security gains at once—a foundation that becomes increasingly important as AI systems grow more capable and autonomous.

To support further research in this area, we are releasing the IH‑Challenge dataset [here](https://huggingface.co/datasets/openai/ih-challenge).
