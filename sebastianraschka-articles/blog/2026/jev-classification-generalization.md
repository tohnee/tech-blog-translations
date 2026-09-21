---
title: "Jev and Generalization"
source: https://sebastianraschka.com/blog/2026/jev-classification-generalization.html
crawled: 2026-09-21
---

# Jev and Generalization

It’s easy to hype and dunk on [Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev). I saw a lot of interesting demos in the last few days. And I also read a lot of dismissals in the last few days. I think the truth lies somewhere between these two extremes.

I.e., it’s easy to dismiss Jev as “just a classifier.”

The exact model and training algorithm are not disclosed. But if I had to make an educated guess, it’s likely:

1. a small encoder-style model like [(Modern)BERT](https://arxiv.org/abs/2412.13663);
2. trained with something similar to Reinforcement Learning with Calibration Reward (from the [Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty](https://arxiv.org/abs/2507.16806) paper).

Many people (me included) have been training encoder-style models for classification for many years. Fact is that they were usually special-purpose and limited in some way.

Jev’s impressive breakthrough is that it generalizes so well (you can use it to classify emails, play video games, trade stocks…).

And I’d say the secret sauce is probably more in the data than in the training algorithm. (Plus a nice API design on top of it.)

Yeah, it’s not the first project where someone applied RL to a (likely) non-autoregressive, encoder-style model.

But what’s impressive is that it works and generalizes so well, which can make all the difference. I.e., we saw the same thing with Stable Diffusion (based on an [existing research paper](https://arxiv.org/abs/2112.10752)) not too long ago, or even with the 2022 ChatGPT launch itself (an improved version of [InstructGPT](https://arxiv.org/abs/2203.02155), where the data made all the difference).

[![Jev API examples for Choice and Noul, with request inputs and annotated outputs showing selected options, confidence, probabilities, and token usage](https://sebastianraschka.com/images/blog/2026/jev-classification-generalization/jev.webp)](https://sebastianraschka.com/images/blog/2026/jev-classification-generalization/jev.png)

Jev API examples for Choice and Noul. Click the figure to view the full-resolution image.

Source: website version of my [LinkedIn post](https://www.linkedin.com/posts/sebastianraschka_its-easy-to-hype-and-dunk-on-jev-i-saw-activity-7507457962425110529-Z_KJ).
