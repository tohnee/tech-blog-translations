---
title: "Hybrid Attention"
source: https://sebastianraschka.com/llm-architecture-gallery/hybrid-attention/
crawled: 2026-09-06
---

# Hybrid Attention

Hybrid attention mixes different sequence-processing mechanisms within one model stack. In the architectures covered here, most layers use a recurrent linear-attention or state-space module. A smaller number retain softmax attention for direct content lookup.

The combination addresses two costs of long contexts. During prefill, standard self-attention compares all token positions and its score computation grows quadratically with sequence length. During autoregressive decoding, each attention layer also keeps a key-value (KV) cache that grows with the context. Recurrent layers such as [Gated DeltaNet](https://arxiv.org/abs/2412.06464) or [Mamba-2](https://arxiv.org/abs/2405.21060) carry a fixed-size state instead.

Keeping some full-attention layers gives the model periodic access to individual cached tokens. The recurrent layers handle most of the sequence at lower cost. For this reason, I find the layer ratio more informative than the label “hybrid attention” alone. Qwen uses three recurrent layers per attention layer, while other models choose different mechanisms and ratios.

[Architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
[Gated Attention](https://sebastianraschka.com/llm-architecture-gallery/gated-attention/)
[From-scratch chapter](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/08_deltanet)

![Overview of linear-attention hybrid architectures](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gated-deltanet-hybrid-overview.webp)

Figure 1. Qwen3-Next repeats three Gated DeltaNet blocks followed by one
[Gated Attention](https://arxiv.org/abs/2505.06708) block.
Most layers use a recurrent state, and every fourth layer performs softmax attention over a KV cache.
(Original source
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)).

Summary

Most blocks use a cheaper recurrent sequence module, while periodic attention layers retain direct token lookup

Why keep attention

A recurrent state compresses the past; attention layers can revisit individual cached tokens

Example architectures

[Qwen3-Next 80B-A3B](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-next-80b-a3b),
[Qwen3.5 397B](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-5-397b),
[Kimi Linear 48B-A3B](https://sebastianraschka.com/llm-architecture-gallery/#card-kimi-linear-48b-a3b),
[Ling 2.5 1T](https://sebastianraschka.com/llm-architecture-gallery/#card-ling-2-5-1t),
[Ling 3.0 Flash](https://sebastianraschka.com/llm-architecture-gallery/#card-ling-3-0-flash),
[Nemotron 3 Nano 30B-A3B](https://sebastianraschka.com/llm-architecture-gallery/#card-nemotron-3-nano-30b-a3b), and
[Nemotron 3 Super 120B-A12B](https://sebastianraschka.com/llm-architecture-gallery/#card-nemotron-3-super-120b-a12b)

## How the Qwen pattern works

[Qwen3-Next 80B-A3B](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct) has 48 layers arranged as 12 repetitions of the 3:1 pattern. Three Gated DeltaNet blocks are followed by one [Gated Attention](https://sebastianraschka.com/llm-architecture-gallery/gated-attention/) block. This means 36 layers use recurrent linear attention and 12 layers retain softmax attention.

Inside a Gated DeltaNet block, the model computes query, key, and value vectors together with two learned gates (alpha and beta). It writes to a small fast-weight memory using a delta-rule update. The state acts as a running summary of the past. One gate controls memory decay, and the other controls how strongly the new value updates that state.

The state size does not grow with the sequence. A Gated Attention layer has the familiar token-to-token attention path and keeps a KV cache, so it remains more expensive at long context lengths. Only one quarter of Qwen’s layers pay that cost.

![Memory comparison between full attention and Gated DeltaNet hybrids](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gated-deltanet-memory-savings.webp)

Figure 2. The memory curves compare full attention with stacks that replace most attention layers with
Gated DeltaNet. The remaining attention layers still require a growing KV cache, but far fewer layers
contribute to it. (Original source
[*LLMs-from-scratch* DeltaNet materials](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/08_deltanet)).

Qwen3.5 keeps the same 3:1 backbone in Qwen’s main model family. For example, the 60-layer Qwen3.5 397B-A17B model repeats the four-layer group 15 times. The model differs from Qwen3-Next in scale and other parts of its architecture, but the sequence-mixing schedule remains recognizable.

![Qwen3.5 compared to the Qwen3-Next architectures](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gated-deltanet-qwen35.webp)

Figure 3. Qwen3.5 carries the 3:1 Gated DeltaNet and Gated Attention schedule from Qwen3-Next into
the main Qwen model line. (Original source
[*A Dream of Spring for Open-Weight LLMs*](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)).

## Kimi Linear changes both halves

[Kimi Linear](https://arxiv.org/abs/2510.26692) uses 20 Kimi Delta Attention (KDA) layers and 7 gated [Multi-Head Latent Attention (MLA)](https://sebastianraschka.com/llm-architecture-gallery/mla/) layers. This is approximately the same 3:1 schedule as Qwen3-Next.

KDA refines the Gated DeltaNet memory update. Qwen3-Next uses one scalar decay gate per head. KDA learns a separate decay value for each feature channel, giving the recurrent state more control over what it retains. The periodic MLA layers provide softmax attention while compressing their keys and values into a smaller latent representation.

The useful comparison is the division of work. KDA compresses the processed history into a fixed-size state. MLA can revisit specific earlier tokens, although its KV cache still grows with the sequence.

![Qwen3-Next and Kimi Linear side by side](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/hybrid-attention-kimi-vs-qwen.webp)

Figure 4. Kimi Linear keeps an approximately 3:1 schedule and changes both layer types. KDA replaces
Gated DeltaNet, and gated MLA replaces Gated Attention. (Original source
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)).

## Ling 2.5 uses Lightning Attention

[Ling 2.5](https://huggingface.co/inclusionAI/Ling-2.5-1T) uses another recurrent linear-attention mechanism called Lightning Attention. Its stack has one MLA layer for every seven Lightning Attention layers. This 1:7 ratio places even more of the sequence processing on the recurrent path than the Qwen and Kimi layouts.

The MLA layers compress the KV representation and retain direct content lookup. Lightning Attention carries the remaining layers with a recurrent state. Ling therefore follows the same general recipe with a different lightweight mechanism and a different ratio.

![Ling 2.5 compared to Qwen3.5](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/hybrid-attention-ling-vs-qwen.webp)

Figure 5. Ling 2.5 pairs Lightning Attention with MLA, while Qwen3.5 pairs Gated DeltaNet with
Gated Attention. Both reserve a minority of layers for KV-cache-based attention. (Original source
[*A Dream of Spring for Open-Weight LLMs*](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)).

The Ling team reports 3.5 times the throughput of Kimi K2 at a 32k-token sequence length. Both models have roughly one trillion total parameters, although their active parameter counts and architectures differ. This is a vendor-reported system comparison. It measures the complete Ling implementation and does not isolate Lightning Attention.

![Ling 2.5 throughput comparison](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/hybrid-attention-ling-throughput.webp)

Figure 6. The published 32k-token throughput chart normalizes Kimi K2 to 1x and reports Ling 2.5 at
about 3.5x. The result includes the full model and inference system. (Original source
[*Ling 2.5 model hub page*](https://huggingface.co/inclusionAI/Ling-2.5-1T)).

## Nemotron uses Mamba-2 layers

The Nemotron 3 models use [Mamba-2](https://arxiv.org/abs/2405.21060) as the cheaper sequence module. Mamba-2 is a state-space model and serves a similar role in the hybrid. It maintains a recurrent state and avoids a sequence-length-dependent KV cache.

Nemotron 3 Nano has a 52-layer stack with 23 Mamba-2 layers, 23 sparse mixture-of-experts layers, and 6 attention layers. The attention layers are only a small part of the stack. Mamba-2 handles most of the sequence processing, and the MoE layers handle the feed-forward computation.

![Nemotron 3 Nano architecture](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/hybrid-attention-nemotron-nano.webp)

Figure 7. Nemotron 3 Nano interleaves Mamba-2, sparse MoE, and six attention layers in a 52-layer stack.
Its attention layers provide occasional direct retrieval. (Original source
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)).

[Nemotron 3 Super](https://arxiv.org/abs/2604.12374) scales this layout to 40 Mamba-2 layers, 40 [Latent MoE](https://sebastianraschka.com/llm-architecture-gallery/latent-moe/) layers, and 8 attention layers. It also adds shared-weight [Multi-Token Prediction (MTP)](https://sebastianraschka.com/llm-architecture-gallery/mtp/). Latent MoE affects expert computation, while MTP supports speculative decoding. Both are separate from the choice to interleave recurrent and attention layers.

![Nemotron 3 Super architecture](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/hybrid-attention-nemotron-super.webp)

Figure 8. Nemotron 3 Super retains the Mamba-2 and attention backbone and adds Latent MoE and
shared-weight MTP. Those components change other parts of the model. (Original source
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)).

## What the hybrid trades away

A recurrent state has fixed size, so it cannot preserve every earlier token as a separate entry. The state must decide what to retain as new tokens arrive. Periodic attention layers compensate by giving the model direct access to their cached history, but they do not remove this compression from the intervening recurrent layers.

The design also reduces KV-cache growth without eliminating it. The remaining attention or MLA layers still cache past tokens. Their number, placement, and attention type determine how much memory the hybrid saves.

Model-level results include many other choices, including training data, MoE design, numerical precision, and optimized kernels. Without matched ablations, a throughput or quality comparison cannot be assigned to the hybrid schedule alone.

Sources

[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
[A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)
[Qwen3-Next model card](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct)
[Gated Delta Networks paper](https://arxiv.org/abs/2412.06464)
[Kimi Linear paper](https://arxiv.org/abs/2510.26692)
[Mamba-2 paper](https://arxiv.org/abs/2405.21060)
[Gated Attention paper](https://arxiv.org/abs/2505.06708)
[Ling 2.5 model card](https://huggingface.co/inclusionAI/Ling-2.5-1T)
[Ling 3.0 Flash model card](https://huggingface.co/inclusionAI/Ling-3.0-flash)
[Nemotron 3 Nano model card](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16)
[Nemotron 3 Super report](https://arxiv.org/abs/2604.12374)
[LLMs-from-scratch DeltaNet chapter](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/08_deltanet)

[Back to architecture gallery](https://sebastianraschka.com/llm-architecture-gallery/)
