---
title: "North Mini Code Agentic Coding Note"
source: https://sebastianraschka.com/blog/2026/north-mini-code-agentic-coding.html
crawled: 2026-09-06
---

# North Mini Code Agentic Coding Note

[North Mini Code](https://huggingface.co/CohereLabs/North-Mini-Code-1.0) is an open-weight model by Cohere for agentic coding tasks. It has 30 billion total parameters, activates 3 billion for each token, and uses the Apache 2.0 license.

The model is relatively compact for a coding agent, but the training target is ambitious. Cohere optimized it for terminal work, repository-level software engineering, and tool use across multiple agent harnesses. That focus matters when reading the benchmark table because a coding agent is evaluated together with its [prompt format](https://sebastianraschka.com/glossary/#prompt-template "Prompt Template"), tools, parser, and execution environment.

## A narrow, deep parallel transformer

North Mini Code builds on Cohere’s parallel transformer design. In a conventional transformer block, [self-attention](https://sebastianraschka.com/glossary/#mha "Multi-Head Attention (MHA)") updates the hidden state before the feed-forward module receives it. Here, the attention and feed-forward branches operate from the same normalized input and their outputs are added to the residual stream together.

The model uses 49 layers with a hidden size of 2,048. The first layer has a dense feed-forward module with an intermediate size of 3,072. The remaining layers use sparse MoE modules with 128 experts and select eight for each token. Each selected expert has an intermediate size of 768, uses [SwiGLU](https://sebastianraschka.com/glossary/#swiglu "SwiGLU"), and receives its routing score through a sigmoid gate.

Attention alternates in a 3:1 local-to-global schedule. The stack contains 36 sliding-window layers and 13 global layers. Sliding-window attention covers 4,096 tokens and uses RoPE. Global attention uses no explicit [position embeddings](https://sebastianraschka.com/glossary/#positional-encoding "Positional Encoding").

Each attention layer has 32 query heads and four key-value heads, giving an 8:1 grouped-query attention ratio. A new token adds about 98 KiB of logical [bf16](https://sebastianraschka.com/glossary/#bfloat16 "bfloat16") K/V entries across all 49 layers. The local caches stop growing after 4,096 tokens, while the 13 global layer caches continue across the retained context.

The model card supports 256K input tokens and up to 64K output tokens. This is useful for repository context and long agent trajectories, although the serving memory still depends on the global attention cache, local windows, batch size, and output length.

## Agentic coding versus code generation

The release combines three broad types of coding evaluation that exercise different behavior.

[Terminal-Bench](https://www.tbench.ai/) gives the model a terminal and an environment. The agent has to run commands, inspect their output, revise its plan, and eventually leave the environment in the requested state.

[SWE-bench](https://www.swebench.com/) starts from a software issue and a real repository. The agent has to locate the relevant code, edit one or more files, and produce a patch that passes the task’s tests. Repository navigation and [tool use](https://sebastianraschka.com/glossary/#tool-use "Tool Use") are part of the evaluation.

[SciCode](https://scicode-bench.github.io/) and [LiveCodeBench](https://livecodebench.github.io/) are closer to prompt-to-code evaluation. They can require substantial mathematical or algorithmic reasoning, but they do not contain the same long interaction loop with a repository and terminal.

I find this distinction more useful than grouping all six rows under one coding label. A model can be strong at generating a self-contained solution and less reliable at maintaining state across dozens of tool calls. The reverse is possible as well.

## Training across coding harnesses

Cohere uses two supervised-finetuning stages followed by [reinforcement learning with verifiable rewards](https://sebastianraschka.com/glossary/#rlvr "RLVR (Reinforcement Learning with Verifiable Rewards)"). The first SFT stage uses a broad mixture at a 64K context length. Code accounts for 70 percent of the trainable tokens, split into 43 percent agentic tool-use data and 27 percent single-turn programming data.

The second stage uses 4.5 billion tokens at a 128K [context length](https://sebastianraschka.com/glossary/#context-length "Context Length"). It keeps only agentic and reasoning-oriented samples, with code accounting for 61 percent of the mixture. Cohere reports more than 70,000 verifiable tasks from roughly 5,000 repositories. The training environments were deduplicated against the repository sources used by SWE-bench and SWE-bench Pro.

Harness diversity is an important part of this setup. SWE-Agent exposes specialized commands and structured observations. Mini-SWE-Agent reduces the interface to a single shell tool. OpenCode uses separate typed tools for editing, search, task tracking, and other actions. Terminal-Bench’s Terminus 2 communicates through plain-text turns.

The release reports that adding a small amount of alternative-harness data improved OpenCode evaluation by 10 percent without reducing the SWE-Agent result. This is Cohere’s own ablation, but it illustrates why a model trained around one tool schema may struggle when the same task is presented through another.

## What reinforcement learning changed

Agent rollouts have highly variable lengths. Cohere therefore separates rollout generation from learning instead of waiting for every trajectory in a synchronous batch. A vLLM sidecar samples continuously while the trainer periodically exports updated policy weights. A windowed queue drains some completed trajectories early without switching the complete workload to completion order.

The reinforcement-learning run combines terminal and software-engineering environments. Each batch contains 512 rollouts with eight attempts per prompt and a 128K context limit. Terminal tasks use a simple ReAct harness with one terminal tool. Software-engineering tasks use SWE-Agent. Unit tests provide binary rewards, and invalid tool calls receive zero reward.

Relative to the SFT checkpoint, Cohere reports absolute pass@1 improvements of 7.9 percentage points on Terminal-Bench v2 and 3.0 points on SWE-bench. The final model also produced shorter trajectories and fewer malformed tool calls in Cohere’s analysis. These measurements compare checkpoints within the same training setup, which makes them more informative about the RL stage than the cross-model table.

## Reading the release [benchmark](https://sebastianraschka.com/glossary/#benchmark "Benchmark") table

North Mini Code scores 36.0 on Terminal-Bench v2, 31.1 on Terminal-Bench Hard, 67.6 on SWE-bench Verified, and 40.2 on SWE-bench Pro in Cohere’s table. Qwen3.6-35B-A3B is higher on all four agentic rows, with scores of 51.5, 35.0, 73.4, and 49.5.

The ordering changes on the shorter code-generation tasks. North Mini Code scores 38.2 on SciCode compared with 35.8 for Qwen3.6. On LiveCodeBench v6, Qwen3.6 leads 80.4 to 70.3.

Gemma 4 shows the opposite pattern in this table. Its SciCode and LiveCodeBench scores are 40.0 and 77.1, while its SWE-bench scores are much lower. North Mini Code’s training focus is a plausible explanation for part of that difference. The table does not provide an architecture or training-data ablation that can assign the gap to one cause.

The cross-model values also come from a mixture of sources. Cohere uses public reports or Artificial Analysis where available and runs missing results internally. The Gemma 4 agentic scores are attributed to the Qwen team. These are useful release-time numbers as of June 12, 2026, but they are not one uniform evaluation run. Harness versions, tool schemas, prompts, inference settings, timeouts, and hardware limits can all affect agentic results.

## A deployment detail that matters

The model card recommends preserving the model’s reasoning content between tool calls. When the assistant returns both a reasoning block and a tool call, both should be appended to the conversation before adding the tool result. Dropping the reasoning state can force the model to reconstruct its plan on the next turn.

At release time, local serving required recent vLLM code plus Cohere’s Melody parser for tool calls and reasoning blocks. Cohere provides bf16 and FP8 checkpoints. The [LLM Architecture Gallery card](https://sebastianraschka.com/llm-architecture-gallery/#card-north-mini-code-30b-a3b) links to the configuration and a higher-resolution architecture figure.

[![North Mini Code architecture and benchmark overview](https://sebastianraschka.com/images/blog/2026/north-mini-code/hero.webp)](https://substack.com/@rasbt/note/c-275332436)

Figure 1. North Mini Code uses a 49-layer parallel transformer with top-8 routing over 128 experts and a 3:1 sliding-window-to-global attention schedule. The benchmark table combines Cohere results, public reports, Artificial Analysis values, and several internally measured missing entries.

Source: expanded website version of my [Substack note](https://substack.com/@rasbt/note/c-275332436), with architecture, training, and evaluation details from Cohere’s [release post](https://huggingface.co/blog/CohereLabs/introducing-north-mini-code), [model card](https://huggingface.co/CohereLabs/North-Mini-Code-1.0), and [configuration](https://huggingface.co/CohereLabs/North-Mini-Code-1.0/blob/main/config.json).
