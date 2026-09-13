---
title: "Nemotron 3 Super Throughput Notes"
source: https://sebastianraschka.com/blog/2026/nemotron-3-super-throughput.html
crawled: 2026-09-06
---

# Nemotron 3 Super Throughput Notes

Another week, another noteworthy open-weight LLM release. NVIDIA’s [Nemotron 3 Super 120B-A12B](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16) looks competitive on the reported benchmarks, and the more interesting part is its throughput-oriented design.

After reading the [technical report](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Super-Technical-Report.pdf) and [model configuration](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16/blob/main/config.json), I like how the design addresses three different inference costs. Mamba-2 reduces the amount of full attention, [Latent MoE](https://sebastianraschka.com/glossary/#latent-moe "Latent MoE") compresses the routed expert path, and multi-token prediction provides an internal draft mechanism for speculative decoding.

## What is inside the 120B-A12B model

The exact counts are 120.6 billion total parameters and 12.7 billion active parameters per forward pass, or 12.1 billion when embeddings are excluded. The 88-layer stack contains 40 Mamba-2 layers, 40 Latent [MoE](https://sebastianraschka.com/glossary/#moe "Mixture of Experts (MoE)") layers, and 8 grouped-query attention layers.

Using only eight attention layers keeps the attention-side cache relatively small. Each attention layer has 2 [KV heads](https://sebastianraschka.com/glossary/#gqa "Grouped-Query Attention (GQA)") with a head dimension of 128. In bf16, that works out to 8 KiB of logical KV cache per token and sequence across the attention layers. The Mamba-2 layers use a recurrent state during generation instead of adding another KV entry for every retained token.

This hybrid design does not remove full attention. It confines it to a small set of global anchor layers while Mamba-2 handles most of the sequence stack. That is a sensible arrangement for long prompts and long generated traces, where a standard transformer accumulates a [KV cache](https://sebastianraschka.com/glossary/#kv-cache "KV Cache") in every layer.

The sparse part is more unusual. Each Latent MoE layer contains 512 routed experts and selects 22 for each token. Before the routed expert computation, the model projects the 4096-dimensional hidden state down to a 1024-dimensional latent representation. The expert outputs are then combined and projected back to 4096 dimensions. A separate shared expert remains at the full width.

The 4x smaller routed dimension reduces expert-weight reads and all-to-all communication payloads. NVIDIA uses those savings to activate more small experts at a similar inference budget. The full 120B parameter checkpoint still has to be stored or distributed, so the 12B active label should be read as a compute estimate rather than a weight-memory estimate.

The third component is multi-token prediction (MTP). Nemotron 3 Super has two shared-weight MTP layers. During inference, the MTP path proposes future tokens and the main model verifies them together. Reusing one prediction head across offsets also allows longer recursive drafts without adding an independent head for every offset. This can reduce decoding latency when the serving engine supports the MTP path and enough draft tokens are accepted.

## Reading the throughput result

NVIDIA reports up to 2.2x higher inference throughput than GPT-OSS-120B and 7.5x higher throughput than Qwen3.5-122B for an 8K-token input followed by 64K output tokens. The measurements use B200 GPUs and report output tokens per second per GPU. The report takes the better result from vLLM or TensorRT-LLM for each model.

The precision settings matter. The 2.2x comparison uses Nemotron 3 Super in NVFP4 and GPT-OSS-120B with MXFP4 weights. Qwen3.5-122B is shown in [bf16](https://sebastianraschka.com/glossary/#bfloat16 "bfloat16"), so the 7.5x figure combines architecture, quantization, and serving-stack differences. In the same normalized chart, bf16 Nemotron 3 Super is about 2x the throughput of bf16 Qwen3.5-122B.

I would not treat these numbers as a universal speed ranking. A 64K-token output is a demanding long-generation workload, and the best backend can change across hardware and software releases. Short chat responses, different batch sizes, or a runtime without optimized Latent MoE and MTP kernels may produce a different ordering.

The result is still useful. It shows what the complete architecture and optimized serving stack can do under a workload relevant to long reasoning traces and agent loops. The [benchmark](https://sebastianraschka.com/glossary/#benchmark "Benchmark") scores in the same report are broadly competitive with GPT-OSS-120B and Qwen3.5-122B rather than a clear sweep across every task. My read is therefore a throughput-focused release that keeps accuracy in a similar range.

## A practical local-model caveat

The original note called Nemotron 3 Super an interesting local model for agentic applications. Here, *local* means a substantial workstation or on-prem server. The bf16 model card lists 8 H100 80 GB GPUs as its minimum configuration. NVIDIA also provides FP8 and NVFP4 checkpoints, and the lower-precision versions reduce the weight footprint substantially.

The model supports contexts up to one million tokens, while the default Hugging Face configuration uses 256K because longer contexts require more memory. Context support, checkpoint fit, and useful throughput are separate questions. For an agentic application, I would benchmark the chosen quantization and serving engine with the actual prompt lengths, tool-call frequency, and output lengths.

The [architecture card](https://sebastianraschka.com/llm-architecture-gallery/#card-nemotron-3-super-120b-a12b) has the high-resolution model diagram and configuration summary. The [Latent MoE explainer](https://sebastianraschka.com/llm-architecture-gallery/latent-moe/) focuses on the compressed expert path.

[![Nemotron 3 Super 120B-A12B architecture diagram and benchmark comparison](https://sebastianraschka.com/images/blog/2026/nemotron-3-super/hero.webp)](https://substack.com/@rasbt/note/c-226718041)

Composite figure from the original [Substack note](https://substack.com/@rasbt/note/c-226718041). It summarizes the 88-layer hybrid architecture, the Latent MoE path, and NVIDIA's release-time benchmark and throughput comparison.

Source: expanded website version of my [Substack note](https://substack.com/@rasbt/note/c-226718041), with architecture and benchmark details from NVIDIA’s technical report.
