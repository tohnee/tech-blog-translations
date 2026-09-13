---
title: "MiniMax M2 Technical Report Notes"
source: https://sebastianraschka.com/blog/2026/minimax-m2-technical-report.html
crawled: 2026-09-06
---

# MiniMax M2 Technical Report Notes

The [MiniMax M2 series](https://arxiv.org/abs/2605.26494) was one of the more visible open-weight LLM families earlier this year. I initially knew it mainly as a capable coding-model series. The technical report is interesting because it connects the model architecture to the less visible work behind agent training and deployment.

Several of the design decisions are fairly conventional on their own. The combination is more revealing. MiniMax kept full attention, used a highly sparse mixture-of-experts layout, trained on executable software-engineering tasks, and incorporated tool latency into reinforcement learning.

## The M2 architecture in brief

The flagship M2 is a 62-layer decoder-only transformer with 229.9 billion total parameters. Only 9.8 billion parameters are active for each token. It uses 256 fine-grained experts per [MoE](https://sebastianraschka.com/glossary/#moe "Mixture of Experts (MoE)") layer and routes each token to eight of them with sigmoid gating.

All 62 layers use grouped-query attention. Each layer has 48 query heads and eight key-value heads, along with QK-Norm and partial RoPE. The [context window](https://sebastianraschka.com/glossary/#context-length "Context Length") is 196,608 tokens, usually rounded to 192K. MiniMax reports pretraining the model on 29.2 trillion tokens.

The original M2 also trains a multi-token prediction module. M2.5 and M2.7 expand this to three modules, which can provide draft tokens for speculative decoding. The serving stack still needs explicit support to realize the resulting speedup.

The [MiniMax M2](https://sebastianraschka.com/llm-architecture-gallery/#card-minimax-m2-230b), [MiniMax M2.5](https://sebastianraschka.com/llm-architecture-gallery/#card-minimax-m2-5-230b), and [MiniMax M2.7](https://sebastianraschka.com/llm-architecture-gallery/#card-minimax-m2-7-230b) cards in the LLM Architecture Gallery summarize the three releases.

## Why MiniMax kept full attention

The attention ablation was the part that caught my eye. Many recent models mix full attention with sliding-window or linear-attention layers to reduce long-context costs. MiniMax tested a hybrid sliding-window setup and ultimately retained full attention in every layer.

The result is more nuanced than a simple win for full attention. At 32K tokens, both versions scored 99 on the two reported RULER tasks. The supervised-finetuning benchmarks were mixed as well. The sliding-window model did better on IFBench and two agent evaluations, while the full-attention model did better on GPQA Diamond, SWE-bench Verified, Terminal-Bench, and several other tasks.

The larger gaps appeared in long-context [pretraining](https://sebastianraschka.com/glossary/#pretraining "Pretraining") evaluations. On a 128K RULER common-word-extraction task, the full-attention model scored 90 compared with 72 for the sliding-window version. The full-attention model also led by 15 and 17.6 points on the two reported many-to-one translation evaluations.

The report gives an additional deployment reason for this choice. Recurrent or compressed attention states can be sensitive to lower precision. Some implementations also lack native prefix caching and a clear integration path for speculative decoding. Prefix caching is especially valuable for coding agents because many rollouts reuse the same repository context and tool history. These are implementation constraints rather than inherent limits of every efficient-attention method, but they help explain MiniMax’s decision.

## A controlled fine-grained MoE comparison

The MoE ablation is useful because MiniMax holds total parameters, active parameters, and training tokens constant. Both tested models have 17.8 billion total parameters, activate 2 billion per token, and train on 500 billion tokens.

The baseline has 32 larger experts and selects two. The fine-grained version splits the expert capacity into 128 smaller experts and selects eight. This keeps the active parameter budget similar while allowing each token to combine a more specific set of experts.

The largest reported improvements are on MATH, from 19.6 to 24.1, and [HumanEval](https://sebastianraschka.com/glossary/#benchmark "Benchmark"), from 29.7 to 32.5. The differences are much smaller on MMLU, ARC-Challenge, and KorBench. I read this as evidence that finer expert granularity can help at a fixed compute budget, with the size of the benefit depending on the task.

## Turning GitHub pull requests into agent tasks

The software-engineering data pipeline starts with merged GitHub pull requests that include tests. An agent builds a runnable Docker environment, and the pipeline extracts tests that should fail before the patch and pass afterward. Additional checks make sure the problem description, repository state, and reward are consistent.

MiniMax then derives more tasks from the same repositories. The transformations include bug injection, commit merging, test writing, and code review. The report says the resulting environments span more than ten programming languages.

This pipeline is a large part of the model recipe. A coding agent needs more than code completion data. It must inspect a repository, run commands, interpret failures, edit multiple files, and satisfy a [verifier](https://sebastianraschka.com/glossary/#verifier "Verifier"). Runnable environments turn those behaviors into training trajectories with concrete rewards.

## Interleaved thinking and wall-clock rewards

MiniMax preserves the model’s reasoning blocks across tool-use turns. In the report’s ablation, removing earlier reasoning blocks consistently reduced agent performance, with the largest effects on deep-search and software-engineering tasks. This makes intuitive sense. A long agent trajectory contains partial conclusions, rejected hypotheses, and constraints that may be expensive to reconstruct after every tool call.

The reinforcement-learning objective also includes a task-completion-time reward. It compares a rollout’s wall-clock time with a reference time and assigns a decreasing reward as completion time rises. The reward can favor parallel [tool use](https://sebastianraschka.com/glossary/#tool-use "Tool Use") when several independent actions are available. It can also discourage a correct agent from taking an unnecessarily slow route through a task.

This detail is easy to overlook because most model evaluations focus on correctness and token counts. For an interactive agent, elapsed time is a separate cost. Two trajectories can use similar numbers of tokens and still feel very different if one serializes every tool call.

## What the self-evolution result means

The report’s strongest self-evolution claims concern M2.7 and MiniMax’s internal Model Iteration System. After researchers define an experiment, the model can inspect training runs, read logs, diagnose metric changes, debug code, and adjust configurations. MiniMax estimates that this system handles 30 to 50 percent of its daily RL iteration workload.

In a separate experiment, M2.7 completed 100 autonomous rounds of work on an internal programming scaffold. MiniMax reports a 30 percent improvement on its in-house evaluations after the model modified code and tuned parameters.

Both numbers are internal measurements, and the report does not provide enough detail for an independent reproduction. I would therefore treat them as examples of how MiniMax uses the model inside its own development loop. They are still noteworthy because the target of the optimization is the infrastructure used by subsequent model runs.

For me, the full-attention decision is the clearest thread running through the report. Architecture, training data, the agent harness, and the serving system are evaluated together. A cheaper attention mechanism is less attractive if it weakens long-context behavior or prevents prefix reuse. Likewise, a coding benchmark is more informative when the training setup contains executable environments and reliable tests.

[![MiniMax M2 technical report takeaways](https://sebastianraschka.com/images/blog/2026/minimax-m2-report/hero.webp)](https://substack.com/@rasbt/note/c-266029305)

Figure 1. The report's sliding-window attention ablation, fine-grained MoE comparison, and software-engineering data pipeline. The benchmark values come from MiniMax's own experiments rather than an independent evaluation.

Source: expanded website version of my [Substack note](https://substack.com/@rasbt/note/c-266029305), with architecture and training details from the [MiniMax M2 technical report](https://arxiv.org/abs/2605.26494).
