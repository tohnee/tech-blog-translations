---
title: "Attention Residuals (AttnRes)"
source: https://sebastianraschka.com/llm-architecture-gallery/attention-residuals/
crawled: 2026-09-06
---

# Attention Residuals (AttnRes)

Attention Residuals are a way to improve the residual path, but they work a bit differently from other recent residual-path changes. [mHC](https://sebastianraschka.com/llm-architecture-gallery/mhc/) made the residual path wider. Attention Residuals (also already part of Kimi Linear) connect the residuals across layers; the connection itself uses an attention score for an importance/contribution weight.

In a regular transformer, residual connections add all earlier updates with a contribution weight of 1. Attention Residuals, or AttnRes for short, replace these fixed weights with learned ones. The [Attention Residuals paper](https://arxiv.org/abs/2603.15031) reports consistent (but modest) improvements in validation loss and downstream performance, with about 4% in training cost and 2% in inference cost.

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[Attention Residuals paper](https://arxiv.org/abs/2603.15031)
[Official repository](https://github.com/MoonshotAI/Attention-Residuals)

![Standard residuals compared with Full and Block Attention Residuals](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/attention-residuals-overview.webp)

Standard residuals (left), Full AttnRes (center), and Block AttnRes (right). Full AttnRes learns weights over
all preceding outputs. The block version keeps regular additions within a block and attends over the block
representations (Original source
[Moonshot AI Attention Residuals repository](https://github.com/MoonshotAI/Attention-Residuals)).

## From a fixed sum to learned weights

In a standard PreNorm transformer, the input to sublayer \(l\) is the sum of the embedding and all preceding attention and feed-forward updates:

\[h\_l = \sum\_{i=0}^{l-1} v\_i\]

The first value, \(v\_0\), is the token embedding. Each later \(v\_i\) is an output from an earlier sublayer. AttnRes uses the same values but learns how much each one should contribute:

\[h\_l = \sum\_{i=0}^{l-1} \alpha\_{i \rightarrow l} \cdot v\_i\]

Here, the earlier outputs are the values, and their RMS-normalized versions serve as keys.

As illustrated in the figure above, we compute each weight as the dot product between the normalized key and a learned pseudo-query for the destination sublayer. We normalize these weights by applying the softmax function across model depth, which gives us the normalized weights \(\alpha\).

Finally, the last step is to compute \(h\_l\), which is an attention-weighted version of the embedding and earlier sublayer outputs.

The pseudo-query is shared across tokens for a given destination sublayer. The keys remain token-dependent, so the weights can still vary by token. Zero-initialized pseudo-queries give all available outputs the same weight at the beginning of training.

## Full and Block AttnRes

For regular self-attention, the weights connect positions in the input sequence. AttnRes instead mixes earlier sublayer outputs for the same token across model depth. The regular sequence layer, such as [Kimi Delta Attention](https://sebastianraschka.com/llm-architecture-gallery/hybrid-attention/) or [MLA](https://sebastianraschka.com/llm-architecture-gallery/mla/), remains unchanged.

Full AttnRes keeps the embedding and every earlier sublayer output. This list grows with model depth. Block AttnRes keeps regular additions inside each block and stores one representation at the boundary. For \(L\) sublayers grouped into \(N\) blocks, the storage per token goes from \(O(Ld)\) to \(O(Nd)\). The large experiments use about eight blocks.

## How Attention Residuals and mHC differ

Both methods change the residual path, but they act along different axes.

- Attention Residuals: select and combine outputs from earlier depths.
- mHC: maintain and mix several residual streams at the current depth.

In Attention Residuals, the learned pseudo-query vector decides how much each earlier depth contributes to the current representation. In [mHC](https://sebastianraschka.com/llm-architecture-gallery/mhc/), the model keeps several residual streams alive at the same depth and learns constrained mappings between those streams.

## Experiments

The full-scale comparison uses two 48B models with 3B active parameters. They have the same architecture and training setup except for the residual connections and are trained from scratch on 1.4 trillion tokens, including 1 trillion pretraining tokens and about 400 billion higher-quality mid-training tokens.

![Training dynamics for the 48B Kimi Linear baseline and Block Attention Residuals model](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/attention-residuals-kimi-linear-training-dynamics.webp)

Training dynamics over the first 1 trillion tokens (Original source
[*Attention Residuals*](https://arxiv.org/abs/2603.15031)).

After the complete recipe, Block AttnRes matches or outperforms the regular-residual baseline on every reported downstream benchmark.

![Table comparing benchmark scores for the Kimi Linear baseline and Attention Residuals model](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/attention-residuals-kimi-linear-results.webp)

Downstream benchmark comparison (Original source
[*Attention Residuals*](https://arxiv.org/abs/2603.15031)).

Sources

[Attention Residuals paper](https://arxiv.org/abs/2603.15031)
[Official implementation and figures](https://github.com/MoonshotAI/Attention-Residuals)
[Kimi Linear paper](https://arxiv.org/abs/2510.26692)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
