---
title: "Nemotron 3 Ultra Latent MoE Note"
source: https://sebastianraschka.com/blog/2026/nemotron-3-ultra-latent-moe.html
crawled: 2026-09-06
---

# Nemotron 3 Ultra Latent MoE Note

A good week for open-weight LLMs. Some of the new releases fit on a laptop or workstation. [Nemotron 3 Ultra](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-NVFP4) sits at the other end of the spectrum.

Ultra has 550 billion total parameters and activates 55 billion for each token. Even the NVFP4 checkpoint is about 330 GiB according to NVIDIA’s [technical report](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Ultra-Technical-Report.pdf). This is a server-scale model, but it is still interesting from a performance-efficiency perspective.

At a high level, Ultra is the larger sibling of [Nemotron 3 Super](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16). It retains the hybrid Mamba-Transformer stack, [Latent MoE](https://sebastianraschka.com/glossary/#latent-moe "Latent MoE") layers, and multi-token prediction. NVIDIA increased the model width, depth, and active expert capacity while keeping the same 4x latent bottleneck.

## The 108-layer hybrid stack

The model has 108 layers. These are split into 48 Mamba-2 layers, 48 Latent [MoE](https://sebastianraschka.com/glossary/#moe "Mixture of Experts (MoE)") layers, and 12 grouped-query attention layers. The sparse attention anchors provide global token-to-token interaction, while the Mamba layers handle most of the sequence processing with a fixed-size recurrent state.

The model width is 8,192. Each attention layer uses 64 query heads, two key-value heads, and a head dimension of 128. Across 12 attention layers, this works out to 12 KiB of logical bf16 [KV cache](https://sebastianraschka.com/glossary/#kv-cache "KV Cache") per token and sequence. The Mamba layers maintain a recurrent state instead of appending another KV entry for every retained token.

This layout expands the 88-layer Super model, which has 40 Mamba-2, 40 Latent MoE, and eight attention layers. The ratio stays similar even though Ultra is more than four times larger by total parameter count.

## How Latent MoE scales

The part I find most interesting is the [Latent MoE](https://sebastianraschka.com/llm-architecture-gallery/latent-moe/) path. A regular MoE layer sends the model-width representation directly through the selected experts. Latent MoE first down-projects that representation, runs the routed experts in a narrower space, and projects the combined result back to the model width.

For Super, the routed path is `4096 -> 1024 -> 4096`. Ultra doubles each width and uses `8192 -> 2048 -> 8192`. Both models therefore use the same 4x compression ratio.

Each Ultra MoE layer contains 512 routed experts and selects 22 for each token. The routed experts use an intermediate dimension of 5,120. A separate shared expert has an intermediate dimension of 10,240 and processes every token.

The latent bottleneck and sparse routing save compute in different ways. Routing limits the number of experts that run. The bottleneck reduces the width of the selected expert path. The down- and up-projections add work, so the 4x bottleneck does not imply a 4x speedup for an MoE layer or for the complete model.

The scale change is still substantial. Super has 120 billion total and 12 billion active parameters. Ultra grows to 550 billion total and 55 billion active parameters while retaining roughly the same 10 percent active-parameter ratio and the same latent compression factor.

## MTP and the mixed-precision recipe

Ultra trains with two multi-token prediction heads. The heads share parameters, and the shared draft module consists of one attention layer followed by one MoE layer. During inference, this module can propose future tokens for speculative decoding. The runtime must support this path, and the realized speedup depends on how often the main model accepts the draft tokens.

NVIDIA pretrained the base model on 20 trillion text tokens. The first 15 trillion emphasized broad domain coverage, followed by 5 trillion higher-quality tokens during the learning-rate decay phase. A subsequent 33-billion-token phase extended the [context length](https://sebastianraschka.com/glossary/#context-length "Context Length") to one million tokens.

The phrase “pretrained in NVFP4” needs a qualification. NVIDIA kept the final 16 layers, Mamba output projections, latent projections, attention projections, MTP layers, and embeddings at higher precision. The released quantized checkpoint also mixes formats. Routed expert matrix multiplications use NVFP4, shared experts and Mamba linear layers use FP8, and attention and latent projections remain in [bf16](https://sebastianraschka.com/glossary/#bfloat16 "bfloat16").

This is a targeted precision recipe. The report’s evaluation compares a selected 5.03-bits-per-element configuration with the bf16 checkpoint and finds similar results across its test suite. The two versions also use different vLLM releases in that comparison, so small score differences should not be assigned to quantization alone.

## Memory and context caveats

Hybrid Mamba models reduce the KV-cache growth that comes with full attention in every layer. The recurrent state is not free, though. NVIDIA reports that Ultra’s FP32 Mamba cache is larger than its FP8 KV cache at sequence lengths up to 64K tokens. The released NVFP4 setup stores the Mamba state in FP16 with stochastic rounding.

The checkpoint size makes the practical scale clearer. On an eight-H100 node with 640 GiB of aggregate memory, NVIDIA estimates about 330 GiB for the NVFP4 weights and roughly 540 GiB for an FP8 checkpoint. The smaller weight footprint leaves much more room for activations, caches, batching, and the MTP module.

Ultra supports contexts up to one million tokens. Context capacity and useful throughput remain separate questions. Long prompts still require cache memory, prefill compute, and a serving stack that handles the hybrid Mamba and attention states efficiently.

## Reading the throughput results

NVIDIA reports 5.9x, 4.8x, and 1.6x higher maximum throughput than GLM-5.1-754B-A40B, Kimi-K2.6-1T-A32B, and Qwen3.5-397B-A17B for an 8K-token input followed by 64K output tokens. All models use NVFP4 on GB200 hardware.

This is a demanding long-generation workload. The comparison also uses TensorRT-LLM for Nemotron 3 Ultra and vLLM for the other models, taking the better result with or without speculative decoding. It measures the complete architecture and serving stack rather than isolating the effect of Latent MoE.

The lower panels in Figure 1 use an independent Artificial Analysis snapshot from June 4, 2026. Those values answer a somewhat different question because they reflect the providers and inference configurations available on that date. Leaderboard positions and output rates can change as inference software and serving settings improve.

For me, Ultra is most useful as a scaling example. NVIDIA kept the same basic Latent MoE bottleneck used in Super, then increased the width from 4,096 to 8,192 and the layer count from 88 to 108. The rest of the efficiency story comes from the hybrid sequence layers, sparse expert routing, [mixed precision](https://sebastianraschka.com/glossary/#mixed-precision "Mixed Precision"), MTP, and a serving system designed around the model.

The [LLM Architecture Gallery card](https://sebastianraschka.com/llm-architecture-gallery/#card-nemotron-3-ultra-550b-a55b) has a higher-resolution architecture figure and links to the released configuration.

[![Nemotron 3 Ultra architecture and benchmark overview](https://sebastianraschka.com/images/blog/2026/nemotron-3-ultra/hero.webp)](https://substack.com/@rasbt/note/c-270588404)

Figure 1. Nemotron 3 Ultra combines 48 Mamba-2, 48 Latent MoE, and 12 grouped-query attention layers. The upper-right diagrams show several smaller open-weight releases from the same week. The lower panels are an Artificial Analysis snapshot from June 4, 2026.

Source: expanded website version of my [Substack note](https://substack.com/@rasbt/note/c-270588404), with architecture, training, and inference details from NVIDIA’s [Nemotron 3 Ultra technical report](https://arxiv.org/abs/2606.15007) and [released configuration](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16/blob/main/config.json).
