---
title: "Why do some LLMs remove bias terms from linear layers?"
source: https://sebastianraschka.com/faq/docs/bias-terms-modern-llms.html
crawled: 2026-09-06
---

# Why do some LLMs remove bias terms from linear layers?

Several modern LLMs, including Llama-style models, omit the bias vectors in their attention and feed-forward linear layers. The practical reason is that these large projections have worked well without learned offsets. Once an architecture and training recipe have demonstrated that the biases are unnecessary, leaving them out saves a little work in every transformer block.

A usual linear layer computes `xW + b`, where `W` is a weight matrix and `b` is the bias vector. Setting `bias=False` removes the addition of `b`. The parameter saving is small relative to the matrix. For a square layer with width 4,096, for example, the matrix contains about 16.8 million weights and the bias contains 4,096 values.

The same comparison applies to the computation. Matrix multiplication dominates the cost of the layer. Adding a bias is cheap, although it still requires an extra vector addition and may complicate a fused implementation. Across many projections and transformer blocks, model designers may prefer to omit a component that has not provided a clear benefit in their setup.

It is tempting to explain this choice by saying that RMSNorm or the residual connection replaces the bias. That statement would be too strong. A bias can shift the pre-activations of a layer, including the inputs to a SwiGLU gate, and neither normalization nor a residual path makes this effect disappear in general. Bias-free projections are an empirical architecture choice rather than a mathematical requirement.

![The repo's architecture comparison shows how modern Llama-style models keep the same broad decoder structure while simplifying several block-level details](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/gpt-to-llama/gpt-and-all-llamas.webp)

The figure above places bias-free layers in the broader GPT-to-Llama transition. They often appear alongside RMSNorm, rotary position embeddings, and SwiGLU. These are separate design decisions, even though modern model families frequently adopt them as a package.

Whether a model uses biases also depends on the exact implementation. A family may omit them from the large attention and MLP projections while retaining other learned offsets elsewhere. Likewise, a model with bias terms is not automatically less efficient or outdated.

So I would view `bias=False` as a small, evidence-based simplification. It removes a learned offset that a particular architecture has shown it can do without. The savings are modest for any single layer, but the change is easy to apply consistently throughout a large transformer.
