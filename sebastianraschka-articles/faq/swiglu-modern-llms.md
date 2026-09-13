---
title: "SwiGLU in modern LLMs"
source: https://sebastianraschka.com/faq/docs/swiglu-modern-llms.html
crawled: 2026-09-06
---

# SwiGLU in modern LLMs

**SwiGLU** is a gated feed-forward layer. It computes two projections of the same token representation, applies the SiLU activation to one projection, multiplies the two paths element by element, and projects the result back to the model width.

This differs from using SiLU by itself. **SiLU**, also called Swish, is the activation function

\[\operatorname{SiLU}(z)=z\,\sigma(z).\]

**SwiGLU** is the complete three-projection block built around this activation. One common formulation is

\[\operatorname{SwiGLU}(x)
= W\_{\text{down}}
\left[
\operatorname{SiLU}(W\_{\text{gate}}x)
\odot
(W\_{\text{up}}x)
\right].\]

The names `gate` and `up` are implementation conventions and can be swapped without changing the operation. Bias terms are omitted in the equation because many Llama-style implementations leave them out. SwiGLU itself does not require a bias-free design.

A plain GPT-2-style feed-forward layer uses two projections:

\[\operatorname{FFN}(x)
= W\_2\,\operatorname{GELU}(W\_1x).\]

The first matrix expands the model width, GELU supplies the nonlinearity, and the second matrix returns to the residual-stream width. SwiGLU replaces the one expanded path with two paths. The activated gate can suppress, pass, or rescale features in the other path before the down projection.

| Block | Expanded representation | Multiplicative gate | Weight matrices |
| --- | --- | --- | --- |
| GELU FFN | \(\operatorname{GELU}(W\_1x)\) | No | 2 |
| GLU | \(\sigma(W\_gx) \odot (W\_ux)\) | Sigmoid | 3 |
| GEGLU | \(\operatorname{GELU}(W\_gx) \odot (W\_ux)\) | GELU | 3 |
| SwiGLU | \(\operatorname{SiLU}(W\_gx) \odot (W\_ux)\) | SiLU | 3 |

SwiGLU belongs to the family studied in [GLU Variants Improve Transformer](https://arxiv.org/abs/2002.05202). In those experiments, gated variants improved Transformer language-modeling results compared with plain ReLU or GELU feed-forward layers under matched training setups. Later Llama-style architectures adopted SwiGLU as part of a larger collection of changes.

Three matrices can sound more expensive than two, but the intermediate dimensions have to be compared. Ignoring bias terms, a plain feed-forward block with model width \(d\) and intermediate width \(m\) contains approximately

\[2dm\]

weights. A SwiGLU block with gated intermediate width \(m\_g\) contains approximately

\[3dm\_g.\]

Setting \(m\_g \approx 2m/3\) gives the two blocks a similar weight count and matrix-multiplication budget. For a plain expansion of \(m=4d\), the matched gated width is about \(8d/3\). Actual model configurations often round the intermediate width to a hardware-friendly multiple or deliberately choose a different feed-forward budget, so the architecture configuration remains the source of truth.

![The plain feed-forward block uses two projections, while the gated version uses separate content and activated-gate paths before the output projection.](https://sebastianraschka.com/images/blog/2025/from-gpt-2-to-gpt-oss/8.png)

The extra path gives the layer a learned multiplicative interaction. A plain GELU block transforms each expanded feature through one nonlinear path. SwiGLU lets one learned feature control the contribution of another. This added selectivity is a plausible reason for its empirical advantage, although the exact gain depends on the model size, width, optimizer, data, and training budget.

SwiGLU does not reduce the attention matrix, context length, or KV cache. It changes the feed-forward sublayer that follows attention in each transformer block. The feed-forward weights are often a large share of a dense LLM’s parameters, so its intermediate width has a noticeable effect on checkpoint size and per-token computation.

The runtime comparison is also implementation dependent. SwiGLU has two input projections rather than one, but each can be narrower under a matched budget. Fused kernels can combine the activation and elementwise multiplication. A useful benchmark keeps model width, effective feed-forward parameter count, precision, batch shape, and hardware fixed.

![The GPT-to-Llama progression includes SwiGLU alongside separate changes to normalization, position handling, and attention.](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/gpt-to-llama/gpt2-to-llama2-llama3.webp)

SwiGLU also appears inside many mixture-of-experts models. Each expert can be a SwiGLU feed-forward network. Its internal gate acts on feature channels for every token sent to that expert. The MoE router is a separate mechanism that decides which experts receive the token. Calling both operations “gating” should not obscure this difference.

The widespread use of SwiGLU supports a measured conclusion. Gated feed-forward variants have performed well in controlled studies and successful training recipes, and their cost can be kept close to a plain MLP by adjusting the intermediate width. Comparisons between complete models cannot assign a quality difference to SwiGLU alone because normalization, attention, model scale, data, and training also change.

For the broader block-level transition, see [What architectural changes turned GPT-style models into Llama-style models?](https://sebastianraschka.com/faq/docs/gpt-style-to-llama-style.html). The related [mixture-of-experts FAQ](https://sebastianraschka.com/faq/docs/mixture-of-experts.html) explains the separate expert-routing mechanism.
