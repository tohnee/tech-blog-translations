---
title: "Gated Residuals (GR)"
source: https://sebastianraschka.com/llm-architecture-gallery/gated-residuals/
crawled: 2026-09-06
---

# Gated Residuals (GR)

The Gated Residuals (GR) mechanism is in spirit related to [mHC](https://sebastianraschka.com/llm-architecture-gallery/mhc/), which both replace the residual connection in a transformer block with four parallel ones. In the case of GR, there are two units or modules, GR Read and GR Write. For example, before each MoE sublayer, a GR Read module compresses the 4 streams into one normal-width input. Then, afterwards, a GR Write module then adds the sublayer output back to all four streams (this uses a learned scalar gate for each stream).

This is kind of like [mHC](https://sebastianraschka.com/llm-architecture-gallery/mhc/) because where each sublayer still uses a normal hidden width. Nowever, Qwen 3.8-Flash-Next, which introduced this concept, does not use mHC’s separate constrained matrix for mixing the residual streams.

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[mHC explainer](https://sebastianraschka.com/llm-architecture-gallery/mhc/)
[Model card](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)

![Qwen3.8-Flash-Next architecture showing GR Read and GR Write around the sequence and MoE sublayers](https://sebastianraschka.com/llm-architecture-gallery/images/architectures/qwen3-8-flash-next.webp)

Figure 1. Qwen3.8-Flash-Next places GR Read and GR Write around both the sequence sublayer and the MoE sublayer in each transformer block. Architecture details come from the
[model card](https://huggingface.co/Qwen/Qwen3.8-Flash-Next),
[released configuration](https://huggingface.co/Qwen/Qwen3.8-Flash-Next/blob/main/config.json), and
[implementation](https://github.com/huggingface/transformers/blob/main/src/transformers/models/qwen4_exp/modeling_qwen4_exp.py#L920-L947).

Residual width

Four parallel streams

Read and write gates

Element-wise read gates and one scalar write gate per stream

Example architectures

[Qwen3.8-Flash-Next 125B-A6B](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-8-flash-next-125b-a6b)

## GR Read

Let \(R\_1, \ldots, R\_4\) denote the four individual residual streams. Here, GR Read normalizes each individual residual stream independently and then predicts an element-wise gate \(g\_i\) for each of these streams. Next, it computes the average over these gated streams to compute the normal-width sublayer input:

\[x = \frac{1}{4}\sum\_{i=1}^{4} g\_i \odot \operatorname{RMSNorm}(R\_i).\]

Here, the gate network reads the (concatenated) four-stream state. In Qwen3.8-Flash-Next, it projects the 10,240-dimensional state down to a 320-dim representation and back up to 10,240 element-wise gates. A sigmoid function (“gate”) keeps each Read gate in the range 0 and 1.

## GR Write

After an certain module (attention module, or Gated DeltaNet, or MoE sublayer) produces its output \(y\), a GR Write module predicts one scalar gate \(s\_i\) for each of the streams and applies the regular residual addition separately:

\[R\_i' = R\_i + s\_i y.\]

The GR Write module computes the write gates as \(2\,\sigma(\cdot)\), so each value lies in the range between 0 and 2. The raw residual streams remain intact, and each receives a differently scaled copy of the same sublayer output.

Qwen applies this read-sublayer-write sequence twice in every transformer block. The first instance surrounds Gated DeltaNet or [Qwen Sparse Attention](https://sebastianraschka.com/llm-architecture-gallery/qwen-sparse-attention/), and the second surrounds the MoE sublayer. A final GR Read collapses the four streams back to one model output after the last layer.

## How GR and mHC differ

Both methods widen the residual path while keeping the attention and MoE sublayers at the usual hidden width. Their stream updates differ.

- [mHC](https://sebastianraschka.com/llm-architecture-gallery/mhc/) includes a residual-stream mixing matrix. The manifold constraint makes this matrix doubly stochastic.
- GR carries each residual stream forward directly. The streams meet when GR Read forms the sublayer input, and GR Write adds the sublayer output back with one scalar gate per stream.
- GR uses sigmoid-bounded read and write gates. It does not apply the doubly stochastic projection used by mHC.

Sources

[Qwen3.8-Flash-Next model card](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)
[Qwen3.8-Flash-Next configuration](https://huggingface.co/Qwen/Qwen3.8-Flash-Next/blob/main/config.json)
[Qwen3.8-Flash-Next technical report](https://github.com/QwenLM/Qwen3.8-Flash-Next/blob/main/tech_report.pdf)
[Transformers GR implementation](https://github.com/huggingface/transformers/blob/main/src/transformers/models/qwen4_exp/modeling_qwen4_exp.py#L920-L947)
[mHC paper](https://arxiv.org/abs/2512.24880)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
