---
title: "Base, Instruct, and Reasoning Models Compared"
source: https://sebastianraschka.com/faq/docs/base-vs-instruct-vs-reasoning-model.html
crawled: 2026-09-06
---

# Base, Instruct, and Reasoning Models Compared

A **base model**, an **instruct model**, and a **reasoning model** often belong to the same model family. The labels indicate how a checkpoint was produced, how it is meant to be used, and what kind of behavior we should expect from it.

**Base model**

A base model is the checkpoint obtained from broad next-token pretraining. It can complete text and contains the general capabilities learned from the training corpus. However, a raw base model may continue the wording of a prompt instead of treating it as a request from a user. This makes base checkpoints useful for research and further finetuning, but usually inconvenient for a chat application.

**Instruct model**

An instruct model usually starts from the base checkpoint and receives additional training on instructions and desired responses. Many training pipelines also use preference data after this instruction-finetuning stage. The resulting model is more likely to answer a question directly, follow a requested format, and use the chat template expected by the model family.

**Reasoning model**

A reasoning model is a less standardized category. In current model families, it usually refers to a checkpoint or inference mode shaped for problems that require several intermediate steps. The post-training recipe may involve reinforcement learning on verifiable tasks, distillation from another reasoning model, or both. At inference time, these models often use a larger token budget before returning the final answer.

That extra budget can help with math, programming, and other multi-step tasks. It also increases latency and token cost, and it may add unnecessary work for a simple request.

![The Qwen overview in the repo shows how a modern family can expose multiple behavioral variants rather than just one monolithic model type](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/qwen/qwen-overview.webp)

The Qwen material in the repo provides a concrete example. Some releases offer separate base and instruct checkpoints, while others expose a thinking mode through the chat template or generation settings. The exact packaging changes between releases even though the broad distinction remains useful.

![The repo’s Qwen materials also include variants such as coder and flash-style models, which reinforces that modern model families are increasingly packaged around distinct use cases and response behaviors](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/qwen/qwen3-coder-flash-overview.webp)

Names such as *Coder* or *Flash* describe another axis, namely the intended use or deployment tradeoff. A coder model can still be a base, instruct, or reasoning-oriented checkpoint. Model-family labels therefore don’t form a strict three-box taxonomy.

For choosing a checkpoint, I use the following rule of thumb:

- choose a **base model** for custom finetuning, representation studies, or raw text continuation
- choose an **instruct model** for ordinary chat and prompt-following tasks
- choose a **reasoning model** when a difficult task benefits from a larger inference budget
