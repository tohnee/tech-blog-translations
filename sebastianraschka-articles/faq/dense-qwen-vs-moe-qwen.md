---
title: "Dense Qwen vs. Mixture-of-Experts Qwen Models"
source: https://sebastianraschka.com/faq/docs/dense-qwen-vs-moe-qwen.html
crawled: 2026-09-06
---

# Dense Qwen vs. Mixture-of-Experts Qwen Models

The difference between a **dense Qwen model** and a **mixture-of-experts (MoE) Qwen model** is mainly in the feed-forward part of each transformer block. The attention layers and the overall decoder structure can remain similar.

In a dense model, every token passes through the same feed-forward module. All weights in that module participate in the calculation for every token. This gives the model a regular execution pattern and makes its parameter count relatively easy to interpret.

An MoE layer stores several feed-forward modules, called experts, plus a router. The router assigns each token to a small subset of those experts. Experts that were not selected for that token do not take part in its feed-forward calculation.

![The Qwen overview in the repo shows that the family includes both dense and MoE-style variants rather than one single architecture form](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/qwen/qwen-overview.webp)

Qwen3 makes the naming convention concrete. Its original series included dense checkpoints ranging from 0.6B to 32B parameters, along with Qwen3 30B-A3B and Qwen3 235B-A22B MoE models. In `30B-A3B`, 30B refers to the approximate total parameter count and A3B indicates that roughly 3B parameters are active for one token. The second number is an active-parameter estimate, rather than the size of the checkpoint stored in memory.

This separation lets an MoE model increase its total expert capacity without multiplying per-token computation by the same factor. It still has to load or distribute the full set of expert weights. A 30B-A3B checkpoint therefore needs memory appropriate for its total weights, even though its arithmetic per token is closer to the active subset.

![The MoE figure in the repo explains the underlying mechanism: many experts are stored, but routing keeps token-level compute sparse](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/moe-memory/1.webp)

The active-parameter count is also an approximation of cost, since attention, embeddings, routing, and other shared parts of the model remain active. Actual speed depends on the implementation. Expert routing can introduce communication between devices, uneven expert loads, and less convenient memory access. Good MoE kernels and expert parallelism matter a great deal in practice.

For a local setup or straightforward finetuning, I would usually find the dense model easier to work with. An MoE model becomes attractive when the available hardware can hold all expert weights and the serving stack handles sparse routing efficiently. It offers more total parameter capacity at a lower active-compute budget, with additional deployment complexity as the tradeoff.

Both variants are still decoder-only transformers. The architectural change is localized primarily to the feed-forward modules, where dense computation is replaced by token-dependent expert routing.
