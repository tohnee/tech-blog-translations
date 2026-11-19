---
title: "Pre-Training Without Learning Rate Decay"
source: https://sebastianraschka.com/blog/2026/llm-pretraining-without-learning-rate-decay.html
crawled: 2026-11-19
---

# Pre-Training Without Learning Rate Decay

This could be the start of a trend in new pre-training recipes: No learning rate (LR) decay phase anymore. (Also seen in Kolibri.)

Instead, use a constant LR plus averaging the last N checkpoints (or a running weight average).

I guess that makes it easier in practice because you don’t have to commit to a total training length upfront.

[![Learning-rate schedules comparing cosine decay, warmup-stable-decay, and a constant learning rate with weights averaged over the last N checkpoints](/images/blog/2026/llm-pretraining-without-learning-rate-decay/pretraining-without-learning-rate-decay.webp)](/images/blog/2026/llm-pretraining-without-learning-rate-decay/pretraining-without-learning-rate-decay.jpg)

Cosine decay, warmup-stable-decay, and a constant learning rate with checkpoint averaging. Click the figure to view the full-resolution image.

A little meta analysis based on those who share training details.

* Classic cosine decay: Llama 3, OLMo 2, OLMo 3, GLM-4.5, GLM-5, Kimi K3, Phi-4.
* WSD (“Warmup-Stable-Decay”): DeepSeek V3, DeepSeek V4, DeepSeek V4.1-Flash, Kimi K2, Kimi Linear, Nemotron 3 Nano, Nemotron 3 Super, SmolLM3, MiniMax M2.
* No decay (constant LR plus checkpoint averaging): Kolibri-1 ([see architecture in the LLM gallery](/llm-architecture-gallery/#card-kolibri-1-78b)), DatologyAI’s models ([see architecture in the LLM gallery](/llm-architecture-gallery/#card-datology-xl-30b-a3b)).

Source: lightly edited website version of my [X post](https://x.com/rasbt/status/2122721652433715481), quoting [DatologyAI’s note on weight averaging](https://x.com/datologyai/status/2122366636472869015).
