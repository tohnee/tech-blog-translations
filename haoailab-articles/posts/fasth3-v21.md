---
title: "FastH3-QAD-v2 and NVFP4 VAE Decoders: Better Quality, Faster Decoding, and Community LoRAs"
date: 2026-10-19
source: https://haoailab.com/blogs/fasth3-v21/
crawled: 2026-11-16
---

# FastH3-QAD-v2 and NVFP4 VAE Decoders: Better Quality, Faster Decoding, and Community LoRAs

> 原文：[FastH3-QAD-v2 and NVFP4 VAE Decoders: Better Quality, Faster Decoding, and Community LoRAs](https://haoailab.com/blogs/fasth3-v21/) · Hao AI Lab @ UCSD

# FastH3-QAD-v2 and NVFP4 VAE Decoders: Better Quality, Faster Decoding, and Community LoRAs

October 19, 2026 · 9 min · Aryan Kumar, Will Lin, Hao Zhang

![FastH3-QAD-v2](https://haoailab.com/blogs/fasth3-v21/img/cover.png)

[![](https://img.shields.io/github/stars/hao-ai-lab/FastVideo?style=social)](https://github.com/hao-ai-lab/FastVideo)[![](https://img.shields.io/badge/🤗%20huggingface--green.svg?style=social)](https://huggingface.co/collections/FastVideo/fastvideo-fasth3)[![Slack](https://img.shields.io/badge/Slack--4A154B?style=social&logo=slack&logoColor=blue)](https://join.slack.com/t/fastvideo/shared_invite/zt-3f4lao1uq-u~Ipx6Lt4J27AlD2y~IdLQ)

FastH3 V2 runs an eight-step video and audio model in NVFP4 on consumer GPUs. FastH3-QAD-v2 raises quality without changing the architecture, memory footprint or file layout by training the 4-bit model instead of only calibrating it.

We are releasing three pieces:

* **FastH3-QAD-v2**, the quantization-aware distillation (QAD) checkpoint of FastH3 V2. It keeps V2’s memory footprint and file layout, and it matches or beats V2 end to end with FP4 attention.
* **Two NVFP4 VAE decoders**, trained on FastH3’s own outputs. The 36-layer decoder matches the original H3 decoder. The 8-layer decoder runs 15× faster. Both beat LightVAE on its own benchmark.
* **Community LoRAs in FastVideo.** LoRAs trained for MiniMax H3 in ComfyUI and other common formats now load directly, including on NVFP4 models.

Together they form the foundation for tomorrow’s release of **FastH3 Omni**, which uses all three. More [at the end](#tomorrow-fasth3-omni).

[![
](img/cover.png)](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-v21--img--videos--world-tour.mp4#t=0.1)

Six 10 s clips generated on two DGX Sparks with FastH3-QAD-v2 and both NVFP4 decoders. Turn the audio on.

## FastH3-QAD-v2: QAD closes the PTQ quality gap[#](#fasth3-qad-v2-qad-closes-the-ptq-quality-gap)

FastH3-QAD-v2 is the quantization-aware distillation (QAD) checkpoint of FastH3 V2. V2 shipped with post-training quantization (PTQ): calibrate activation scales on 1,000 prompts, then round each weight to 4 bits. QAD goes one step further. The teacher is V2 in full precision. The student runs the deployed 4-bit weights and activations on all 350 linear layers and trains through the rounding, so the weights adapt to the quantized forward pass instead of carrying its error into the output.

* **Matching every step.** At each of the eight sampling steps, the student sees the teacher’s input and learns the teacher’s output. A quarter of the samples run on the student’s own trajectory, so it also learns to recover from its own small errors.
* **Text-only training.** The recipe uses 3,000 text prompts, 300 steps on two GB200 nodes, and about five hours.
* **A shared recipe.** The same QAD method is the training path for the next FastH3 models, including FastH3 Omni.

The result, measured as error against full-precision V2 on 30 held-out prompts (lower is better):

| Error vs full-precision V2 | V2 NVFP4 | FastH3-QAD-v2 NVFP4 | Change |
| --- | --- | --- | --- |
| Each sampling step, video + audio | 0.431 | 0.351 | −19% |
| Video | 0.471 | 0.382 | −19% |
| Audio | 0.391 | 0.319 | −18% |
| Final video after all 8 steps | 0.817 | 0.713 | −13% |
| Memory, file layout | unchanged | | |

### Why the VSA gates stay in BF16[#](#why-the-vsa-gates-stay-in-bf16)

Video Sparse Attention uses small gate projections to decide which video tiles each token attends to. Quantizing the linears changes the arithmetic. Changing the gates changes the selection itself, so the attention pattern no longer matches the one the model was trained with. FastH3-QAD-v2 keeps the gates and normalization layers in BF16, and trains only the q/k/v/out and FFN projections, the same set the NVFP4 export quantizes.

The result preserves tile selection while letting every quantized projection adapt to 4-bit arithmetic. We evaluate each QAD checkpoint on rendered clips through the deployed pipeline, in addition to teacher-forced metrics, before promoting it.

## NVFP4 VAE decoders[#](#nvfp4-vae-decoders)

Every FastH3 clip ends in the VAE decoder, which turns latents into pixels. After the transformer and the text encoder moved to NVFP4, the decoder was the last part of FastH3 not in 4-bit, and on a DGX Spark it had become a third of the total time: the INT8 lightweight VAE took **43 s** to decode a 5 s, 480p clip, next to 68 s of denoising.

![Video decode time for a 5 s 832x480 clip on one DGX Spark: INT8 light VAE 42.8 s, dense light VAE 9.6 s, our 8-layer NVFP4 decoder 1.6 s.](img/fig_spark_decode.svg)

Figure 1. Video decode time for a 5 s, 832×480 clip on one DGX Spark.

We trained two NVFP4 decoders, both distilled from the original 36-layer H3 decoder:

* **Quality, 36 layers.** The full decoder with every block in NVFP4. 1.29 GiB instead of 4.5 GiB, and within 0.1 dB of the original.
* **Fast, 8 layers.** 8 of the 36 blocks, distilled and quantized. 0.31 GiB and 15× faster than the original.

### Trained on FastH3’s own outputs[#](#trained-on-fasth3s-own-outputs)

A decoder only has to be good on the latents it is given. We train on **latents generated by FastH3** itself, mixed with encoded real video, so the decoder sees the same distribution at training and inference:

* **Teacher:** the original H3 decoder in full precision. **Loss:** pixel L1 plus LPIPS against the teacher’s output, on random latent tiles.
* **Students:** NVFP4 weights and activations in every transformer block; input/output projections and norms stay in higher precision.
* **What the error is:** with 4-bit weights alone the decoder is nearly lossless. What remains comes from 4-bit activations, spread evenly across the blocks.

### Fused FP4 kernels[#](#fused-fp4-kernels)

A 4-bit GEMM is only fast if everything around it is too. The decoder’s blocks run on fused Triton and CUTLASS FP4 kernels, which quantize activations, apply scales and run the GEMM without round trips through memory. CUDA graphs remove launch overhead, and weights stay packed in 4 bits on the GPU. The fused path is bit-exact with the unfused NVFP4 reference and cut the 36-layer decoder from 1.88 s to 0.53 s at 480p.

### Head to head with LightVAE[#](#head-to-head-with-lightvae)

[LightVAE](https://huggingface.co/lightx2v/LightVAE) is a widely used public lightweight decoder for H3. LightVAE-Lite keeps 12 of the 36 decoder layers and reports about 3× the original’s speed. We compared against it **on LightVAE’s own protocol**: 1344×768, 124 frames, bf16, eager mode, one warm-up and the median of three runs, on one GB200. LightVAE runs with its own code and weights, and every decoder receives the same latents from the original H3 encoder. The 20 test clips are 10 H3 generations and 10 live-action clips that no decoder has seen. Our harness reproduces LightVAE’s PSNR exactly, and their speed claims hold (2.85× vs their claimed 2.96×).

| Decoder | Decode FPS, eager | Decode FPS, best config | PSNR (dB) | LPIPS | Size |
| --- | --- | --- | --- | --- | --- |
| Original H3 | 17.9 | 62.1 | 33.73 | 0.071 | 4.5 GiB |
| LightVAE-Lite (decoder) | 51.0 (2.86×) | 183.7 | 31.74 (−2.0) | 0.109 | 1.5 GiB |
| LightVAE-Lite (encoder + decoder) | 49.3 | 183.1 | 30.57 (−3.2) | 0.140 | 1.5 GiB |
| Ours, 36-layer NVFP4 | 70.0 (3.9×) | 104.3 | 33.63 (−0.10) | 0.073 | 1.29 GiB |
| Ours, 8-layer NVFP4 | 274.6 (15.4×) | 418 | 31.73 (= Lite) | 0.096 | 0.31 GiB |

best in column ours, better than LightVAE-Lite "Best config" puts all spatial tiles in one call and adds `torch.compile`, applied equally to every model.

![Decode latency against PSNR for the original H3 decoder, LightVAE-Lite, TAEH3 and our two NVFP4 decoders.](img/fig_vae_pareto.svg)

Figure 2. Quality against decode latency for H3 VAE decoders on LightVAE’s protocol (1344×768, one GB200). Lower latency and higher PSNR are better.

* **36-layer vs LightVAE-Lite:** 1.9 dB better and essentially lossless (−0.10 dB against the original, where Lite loses 2.0), faster on their protocol (70 vs 51 FPS) and smaller. The one place it trails: in the best config, Lite’s decoder is faster (184 vs 104 FPS), at 1.9 dB lower quality.
* **8-layer vs LightVAE-Lite:** the same PSNR (31.73 vs 31.74 dB) with better LPIPS (0.096 vs 0.109), 5.4× faster on their protocol, 2.3× faster in the best config, and 5× smaller.
* **On real footage and on generated video, at 480p, 720p and 768p,** the ranking is the same.
* **On our 20-clip protocol, Lite loses 2.0 dB; its README reports 1.25 dB.** Its paper’s real-dataset results, about −3 dB on UCF-101 and DAVIS, are consistent with our measurement.

## The whole stack in NVFP4[#](#the-whole-stack-in-nvfp4)

With the decoder done, every large component of FastH3 text-to-video now runs in NVFP4: the text encoder, the transformer and the VAE decoder. Here is what that buys against the same model kept in BF16.

![Stacked bars of the weights FastH3 loads for text-to-video: 118.3 GiB for the same model in BF16 and 30.0 GiB for the FastH3-QAD-v2 NVFP4 stack.](img/fig_stack_size.svg)

Figure 3. Weights loaded for text-to-video, by component.

| Component | Same model in BF16 | FastH3-QAD-v2 stack | Smaller by |
| --- | --- | --- | --- |
| Transformer linear layers (21.2B parameters) | 39.5 GiB | 11.1 GiB, NVFP4 | 3.6× |
| Timestep (AdaLN) projections (13.0B) | 24.2 GiB | 0.14 GiB, precomputed table | 170× |
| Other transformer weights (0.8B) | 1.6 GiB | 1.6 GiB, BF16 | — |
| Text encoder, Qwen3-VL, 50 layers (25.8B) | 48.0 GiB | 15.3 GiB, NVFP4 | 3.1× |
| VAE decoder (2.4B) | 4.5 GiB | 1.29 GiB (36 layers) / 0.31 GiB (8 layers) | 3.5× / 15× |
| Audio VAE | 0.6 GiB | 0.6 GiB | — |
| Total | 118.3 GiB | 30.0 GiB / 29.0 GiB | 3.9× / 4.1× |

* **NVFP4 stores a weight in about 4.5 bits** (4-bit values plus a shared FP8 scale for every 16), so 4-bit layers come out about 3.6× smaller than BF16.
* **The timestep projections are not quantized at all.** FastH3 samples on a fixed eight-step schedule, so their outputs are precomputed once into a 155 MB table and the 24 GiB of weights are never loaded.
* **What stays in BF16** is small and sensitive: norms, embeddings, the input and output projections, the text encoder’s vision tower and the audio VAE.
* **The BF16 column is the same layers FastH3 runs.** H3 reads layer 50 of its 64-layer Qwen3-VL text encoder, so we keep only those 50 layers. The BF16 H3 checkpoint as released is 137.7 GiB, because it also carries the last 14 encoder layers, the language-model head, and the FP32 VAE encoder and decoder.
* **Not all of it is on the GPU at once.** On a 32 GB RTX 5090, the transformer (12.7 GiB) and the decoder stay on the GPU, while the text encoder streams in one layer at a time from host memory and the timestep projections are never loaded. A DGX Spark keeps everything in its 128 GB of unified memory.

### End-to-end latency[#](#end-to-end-latency)

Same protocol as our last post: end to end on a warm server from prompt to finished MP4, the median of four runs, with model load excluded. The figure uses the FP4 VSA attention lane.

![Two-panel grouped bar chart. Top: 5 s 832×480 clips for V2, FastH3-QAD-v2 with the 36-layer decoder, and FastH3-QAD-v2 with the 8-layer decoder. Bottom: 10 s 1344×768 clips for the two FastH3-QAD-v2 decoders. Log scale.](img/fig_e2e.svg)

Figure 4. End-to-end time with audio. Top: a 5 s, 832×480 clip. Bottom: a 10 s, 1344×768 clip. Every row is one machine; all times use FP4 VSA.

## Community LoRAs[#](#community-loras)

The H3 community has published many LoRAs, from camera moves to film looks. Most use ComfyUI or trainer layouts. FastVideo loads them directly, including on NVFP4 models:

```
from fastvideo import VideoGenerator
from fastvideo.api import ComponentConfig, GeneratorConfig, PipelineSelection

generator = VideoGenerator.from_config(
    GeneratorConfig(
        model_path="FastVideo/FastH3-QAD-v2",
        pipeline=PipelineSelection(
            components=ComponentConfig(lora_path="pablodawson/MiniMax-H3-360-Orbit-LoRA", lora_strength=0.8),
        ),
    ))
```

* **Formats:** ComfyUI, fal, ai-toolkit and musubi-tuner layouts, with `lora_A/lora_B` or `lora_down/lora_up` factors and per-layer alpha.
* **On 4-bit models:** NVFP4 and FP8 weights stay packed and untouched; each LoRA runs as a small bf16 side branch next to its layer. Strength 0 reproduces the base model exactly, and strength can change at runtime.
* **Clear load errors:** a LoRA that matches no layers, or too few, fails with a list of what did not match instead of silently returning the base model.

Most community LoRAs target base H3’s 50-step schedule. FastH3 samples in eight steps, so style and motion LoRAs usually carry over, but the best strength can differ. Turbo LoRAs are unnecessary.

## Tomorrow: FastH3 Omni[#](#tomorrow-fasth3-omni)

Tomorrow we release **FastH3 Omni**: the general model and its training code in BF16, plus a consumer-hardware release. The consumer release uses the QAD recipe above, extended to 4-bit attention, and the NVFP4 decoders.

## Known limitations[#](#known-limitations)

* **The 8-layer decoder trades quality for speed.** Use the 36-layer decoder when detail matters.
* **The NVFP4 decoders need a Blackwell GPU:** RTX 50 series, RTX PRO 6000, DGX Spark, or B200/GB200.
* **LoRAs on FastH3 Trim are not supported yet.** Trim removes transformer blocks, so LoRAs trained on full H3 do not line up with its layers.

## Get the models[#](#get-the-models)

|  |  |
| --- | --- |
| FastH3-QAD-v2, NVFP4 (RTX 5090, RTX PRO 6000, DGX Spark) | [`FastH3-QAD-v2`](https://huggingface.co/FastVideo/FastH3-QAD-v2) |
| NVFP4 VAE decoders: `quality-36L/` and `fast-8L/` | [`FastH3-NVFP4-VAE-Decoder`](https://huggingface.co/FastVideo/FastH3-NVFP4-VAE-Decoder) |

## Acknowledgements[#](#acknowledgements)

FastH3 builds on [MiniMax H3](https://huggingface.co/MiniMaxAI/MiniMax-H3); we thank the MiniMax team for releasing its weights and code. We thank the [LightX2V](https://github.com/ModelTC/LightX2V) team for releasing LightVAE with its benchmark code, which made a fair comparison possible, and the H3 community for its LoRAs.

We thank the NVIDIA Enterprise Products team (Pengcheng Li and Cliff Woolley) for the Video Sparse Attention kernel, and the FlashInfer and NVIDIA Model Optimizer teams for the FP4 kernels and calibration tools. We also thank [Nuva Lab](https://nuvalab.ai/), [NVIDIA FastGen](https://github.com/NVlabs/FastGen), the [vLLM project](https://vllm.ai/), [NVIDIA](https://www.nvidia.com/en-us/) and [MBZUAI](https://mbzuai.ac.ae/) for their collaboration and support.

## FastVideo team[#](#fastvideo-team)

**Contributor:** [Aryan Kumar](https://github.com/aryan5v)

  
**Tech lead:** [Will Lin](https://github.com/SolitaryThinker)

  
**Advisor:** [Hao Zhang](https://github.com/zhisbug)
