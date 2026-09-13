---
title: "Gated Attention"
source: https://sebastianraschka.com/llm-architecture-gallery/gated-attention/
crawled: 2026-09-06
---

# Gated Attention

Gated attention keeps the familiar scaled dot-product attention computation and adds a learned sigmoid gate to its output. At each token, this gate controls how strongly the attention result flows into the output projection and residual stream.

The placement is important. The gate acts after softmax attention has mixed the value vectors. It does not alter the attention weights, reduce the KV cache, or change the quadratic cost of a full-attention layer. It gives the layer an extra way to suppress an unhelpful attention result.

I find it useful to separate this small operation from the larger architecture around it. Qwen uses gated attention as the expensive part of a recurrent hybrid. Trinity Large applies the same basic idea throughout a local/global attention stack.

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[Hybrid Attention](https://sebastianraschka.com/llm-architecture-gallery/hybrid-attention/)
[Qwen3.5 from-scratch Nb](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/16_qwen3.5/qwen3.5.ipynb)

![Trinity Large architecture and gated attention code snippet](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gated-attention-trinity-large.webp)

Figure 1. Trinity Large multiplies the scaled dot-product attention output by an elementwise sigmoid gate before
the output projection. Its local/global layer schedule is a separate design choice. (Original source
[*A Dream of Spring for Open-Weight LLMs*](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)).

What changes

A learned sigmoid gate scales the attention output before the output projection

What stays the same

Softmax attention, the KV cache, and the attention layer's sequence-length complexity

Example architectures

[Qwen3-Next 80B-A3B](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-next-80b-a3b),
[Qwen3.5 397B](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-5-397b),
[Trinity Large 400B](https://sebastianraschka.com/llm-architecture-gallery/#card-arcee-ai-trinity-large-400b), and
[Tencent Hy4-preview](https://sebastianraschka.com/llm-architecture-gallery/#card-tencent-hy4-preview-770b-a49b)

## The gate after attention

Let \(X\) be the normalized hidden state and let \(A\) be the usual attention output. A simplified gated block can be written as

\[A = \operatorname{SDPA}(Q,K,V), \qquad
G = \sigma(XW\_g), \qquad
Y = (A \odot G)W\_o.\]

The sigmoid keeps each gate value between zero and one. A value near zero suppresses that part of the attention output, while a value near one passes it through. Depending on the implementation, the model can learn one gate value for a whole head or separate values for the head’s feature channels.

The [original gated-attention study](https://arxiv.org/abs/2505.06708) compared 30 variants, including several gate locations and granularities. In its experiments, applying a sigmoid gate after scaled dot-product attention worked best. The authors also observed fewer attention sinks, better long-context extrapolation, and more stable training. These are empirical results from their matched model studies, not guarantees for every architecture.

## How Qwen implements it

[Qwen3-Next 80B-A3B](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct) has 48 layers. It repeats three Gated DeltaNet layers followed by one gated softmax-attention layer, giving 36 recurrent layers and 12 attention layers. The attention part uses grouped-query attention. Qwen3.5 carries the 3:1 pattern into the main Qwen model line. Its 397B-A17B variant has 45 Gated DeltaNet layers and 15 attention layers.

A quick code-level check makes the gate concrete. In the [Qwen3-Next implementation](https://github.com/huggingface/transformers/blob/main/src/transformers/models/qwen3_next/modular_qwen3_next.py), the query projection produces both query features and gate features. After attention is computed and the heads are reshaped, the code multiplies the result by `sigmoid(gate)` and then applies the output projection.

The easiest detail to miss is that Qwen also uses zero-centered QK-Norm and partial RoPE in this block. Those are nearby stability and position-encoding choices. The sigmoid output gate is the feature that makes it gated attention.

![Qwen3-Next architecture showing gated attention in a hybrid stack](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gated-attention-qwen3-next.webp)

Figure 2. Qwen3-Next periodically inserts a gated softmax-attention layer among runs of three Gated DeltaNet
layers. Only the attention layers maintain a sequence-length-dependent KV cache. (Original source
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)).

## Trinity uses the gate in an attention-only stack

[Trinity Large](https://arxiv.org/abs/2602.17004) has 60 grouped-query attention layers arranged as 45 local and 15 global layers. The local layers use a 4,096-token sliding window with RoPE. Every fourth layer is global and uses NoPE. Each attention layer applies an elementwise sigmoid gate to the attention output before its output projection.

This is a helpful counterexample to the Qwen layout. Gated attention does not require Gated DeltaNet or another recurrent sequence module. The gate can sit inside local attention, global attention, or a mixture of both.

The extra work consists mainly of the gate projection, sigmoid, and elementwise multiplication. The gated-attention paper reported less than 2% additional wall-clock latency in its experimental setup. The exact overhead depends on the implementation, hardware, and surrounding model, while the KV-cache and full-attention costs remain.

Sources

[Gated Attention paper](https://arxiv.org/abs/2505.06708)
[Qwen3-Next model card](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct)
[Qwen3-Next implementation](https://github.com/huggingface/transformers/blob/main/src/transformers/models/qwen3_next/modular_qwen3_next.py)
[Trinity Large technical report](https://arxiv.org/abs/2602.17004)
[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
[A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)
[Qwen3.5 implementation notes](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch05/16_qwen3.5/qwen3.5.ipynb)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
