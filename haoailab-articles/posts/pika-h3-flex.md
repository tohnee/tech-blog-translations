---
title: "Pika H3 Flex in FastVideo: 7x Faster, and Near Real Time in 4-bit"
date: 2026-11-03
source: https://haoailab.com/blogs/pika-h3-flex/
crawled: 2026-11-16
---

# Pika H3 Flex in FastVideo: 7x Faster, and Near Real Time in 4-bit

> 原文：[Pika H3 Flex in FastVideo: 7x Faster, and Near Real Time in 4-bit](https://haoailab.com/blogs/pika-h3-flex/) · Hao AI Lab @ UCSD

# Pika H3 Flex in FastVideo: 7x Faster, and Near Real Time in 4-bit

November 3, 2026 · 9 min · Aryan Kumar, Will Lin, Hao Zhang

![FastVideo x Pika: Pika-H3-Flex in FastVideo + NVFP4 QAD](https://haoailab.com/blogs/pika-h3-flex/img/cover.jpg)

[![](https://img.shields.io/github/stars/hao-ai-lab/FastVideo?style=social)](https://github.com/hao-ai-lab/FastVideo)[![](https://img.shields.io/badge/🤗%20huggingface--green.svg?style=social)](https://huggingface.co/FastVideo/Pika-H3-Flex-NVFP4-QAD)[![Slack](https://img.shields.io/badge/Slack--4A154B?style=social&logo=slack&logoColor=blue)](https://join.slack.com/t/fastvideo/shared_invite/zt-3f4lao1uq-u~Ipx6Lt4J27AlD2y~IdLQ)

[**Pika H3 Flex**](https://huggingface.co/Pika-Labs/Pika-H3-Flex) turns a prompt, first and last frames, or image, video and audio references into video with synchronized sound. It now runs in **FastVideo**, up to **7x faster** than the official code. We are also releasing **NVFP4 versions** trained with quantization-aware distillation, [with BF16 attention](https://huggingface.co/FastVideo/Pika-H3-Flex-NVFP4-QAD) and [with FP4 attention](https://huggingface.co/FastVideo/Pika-H3-Flex-NVFP4-FP4Attn-QAD): a 5-second 480p clip takes **5.8 seconds** on one GB200.

Flex builds on MiniMax H3, the same model behind our [FastH3](/blogs/fasth3-local/) releases, so our kernels, NVFP4 decoder and quantization recipe carried straight over. We are grateful to Pika for open-sourcing it.

## TL;DR[#](#tldr)

* **Near real time.** A 5-second 480p clip in **5.8 s** on one GB200 with the NVFP4 model.
* **Faster at BF16.** **2.4x** faster than the official code on one GPU, and **7x** for 15-second clips on four GPUs.
* **NVFP4, trained to match.** QAD brings both adapters 14-17% closer to the BF16 model than plain quantization, and FP4 attention makes long clips **16%** faster.
* **Runs locally.** The NVFP4 models target Blackwell hardware down to DGX Spark and RTX 5090: a 5-second 480p FL2VA clip takes **59.5 s on one DGX Spark**.
* **2K.** Regenerate any H3-family video at 2560x1440.
* **Open source.** [NVFP4 QAD weights](https://huggingface.co/FastVideo/Pika-H3-Flex-NVFP4-QAD) ([FP4 attention](https://huggingface.co/FastVideo/Pika-H3-Flex-NVFP4-FP4Attn-QAD)), inference and the full training recipe.

## What Pika H3 Flex does[#](#what-pika-h3-flex-does)

Flex is MiniMax H3 post-trained by Pika, with two adapters: one for text and keyframe tasks, one for reference-conditioned generation. It samples in six steps with no CFG and uses dense attention.

| Task | Input | Adapter |
| --- | --- | --- |
| T2VA | a prompt | `fl2va` |
| I2VA / L2VA / FL2VA | a first frame, a last frame, or both | `fl2va` |
| Ref2VA | up to 9 images, 3 videos and 3 audio clips | `ref2va` |

## Same prompt, four ways[#](#same-prompt-four-ways)

Each scene is generated four ways from the same prompt and seed on one GB200: Pika’s official code, FastVideo at BF16, and the two NVFP4 QAD models. The four clips play in sync, and each tile shows its end-to-end time.

Faster!Text to video
Blue hourText to video
CannonballText to video
FireworksFirst frame to video
CampfireReferences to video

![](/blogs/pika-h3-flex/media/compare/official__v1_faster.jpg)

**Pika official** BF16*59.7 s*

![](/blogs/pika-h3-flex/media/compare/fv_bf16__v1_faster.jpg)

**FastVideo** BF16*26.6 s*

![](/blogs/pika-h3-flex/media/compare/nvfp4_bf16attn__v1_faster.jpg)

**NVFP4 QAD** BF16 attention*16.8 s*

![](/blogs/pika-h3-flex/media/compare/nvfp4_fp4attn__v1_faster.jpg)

**NVFP4 QAD** FP4 attention*15.2 s*

![](/blogs/pika-h3-flex/media/compare/official__v2_bluehour.jpg)

**Pika official** BF16*59.7 s*

![](/blogs/pika-h3-flex/media/compare/fv_bf16__v2_bluehour.jpg)

**FastVideo** BF16*26.9 s*

![](/blogs/pika-h3-flex/media/compare/nvfp4_bf16attn__v2_bluehour.jpg)

**NVFP4 QAD** BF16 attention*16.9 s*

![](/blogs/pika-h3-flex/media/compare/nvfp4_fp4attn__v2_bluehour.jpg)

**NVFP4 QAD** FP4 attention*15.1 s*

![](/blogs/pika-h3-flex/media/compare/official__v3_cannonball.jpg)

**Pika official** BF16*59.7 s*

![](/blogs/pika-h3-flex/media/compare/fv_bf16__v3_cannonball.jpg)

**FastVideo** BF16*27.1 s*

![](/blogs/pika-h3-flex/media/compare/nvfp4_bf16attn__v3_cannonball.jpg)

**NVFP4 QAD** BF16 attention*16.8 s*

![](/blogs/pika-h3-flex/media/compare/nvfp4_fp4attn__v3_cannonball.jpg)

**NVFP4 QAD** FP4 attention*15.2 s*

![](/blogs/pika-h3-flex/media/compare/official__v4_fireworks.jpg)

**Pika official** BF16

![](/blogs/pika-h3-flex/media/compare/fv_bf16__v4_fireworks.jpg)

**FastVideo** BF16*29.2 s*

![](/blogs/pika-h3-flex/media/compare/nvfp4_bf16attn__v4_fireworks.jpg)

**NVFP4 QAD** BF16 attention*18.2 s*

![](/blogs/pika-h3-flex/media/compare/nvfp4_fp4attn__v4_fireworks.jpg)

**NVFP4 QAD** FP4 attention*16.5 s*

![](/blogs/pika-h3-flex/media/compare/official__v5_campfire.jpg)

**Pika official** BF16

![](/blogs/pika-h3-flex/media/compare/fv_bf16__v5_campfire.jpg)

**FastVideo** BF16*75.4 s*

![](/blogs/pika-h3-flex/media/compare/nvfp4_bf16attn__v5_campfire.jpg)

**NVFP4 QAD** BF16 attention*61.7 s*

![](/blogs/pika-h3-flex/media/compare/nvfp4_fp4attn__v5_campfire.jpg)

**NVFP4 QAD** FP4 attention*51.4 s*

Same prompt, seed and resolution (768p, 5 s) on one GB200; times are end to end.

## Faster at BF16[#](#faster-at-bf16)

On one GB200, the official code spends 20 s on six DiT forwards for a 5-second 768p clip, then **38 s decoding** with an fp32 VAE. FastVideo cuts both, with the same weights:

* **FlashAttention-4** replaces cuDNN SDPA.
* **Fused H3 kernels** remove the `cat`/`mul` glue, about 19% of the official forward, and further fused kernels cover the QKV prologue, normalization, modulation and SwiGLU, all exact in BF16.
* **BF16 decoding**, then our NVFP4 decoder, takes the decode from 38 s to 1.5 s.

DiT denoise (6 forwards)
VAE decode
Other

**5 s · 768p · 1 GPU**T2VA, 1344×768, 124 frames (37,718 tokens), one GB200, warm median

Official pika-h3-prodiffusers, cuDNN SDPA, fp32 VAE

**59.7 s**

FastVideo BF16FA4 + fused H3 ops + bf16 VAE

**25.1 s***2.38×*

+ kernels + NVFP4 decoderfused kernels, NVFP4 VAE decoder

**17.6 s***3.38×*

**15 s · 768p · 1 GPU**T2VA, 1344×768, 362 frames (109,070 tokens), one GB200, warm median

Official pika-h3-profp32 VAE

**224 s**

FastVideo BF16FA4 + fused H3 ops + bf16 VAE

**104 s***2.15×*

+ kernels + NVFP4 decoderfused kernels, NVFP4 VAE decoder

**94.7 s***2.37×*

**15 s · 768p · 4 GPUs**T2VA, 1344×768, 362 frames, four GB200 (sequence parallel), warm median

Official, 1 GPUreference point

**225 s**

Official, 4 GPUsdiffusers Ulysses CP

**146 s**

FastVideo BF16, 4 GPUssequence parallel DiT + VAE

**53.3 s***2.73×* vs official 4 GPUs*4.22×* vs official 1 GPU

+ kernels + NVFP4 decoder4 GPUs

**31.8 s***4.58×* vs official 4 GPUs*7.07×* vs official 1 GPU

End-to-end seconds from prompt to MP4 with audio, one or four GB200 GPUs, models resident, warm medians. Speedups are against the official code on the same number of GPUs; the 4-GPU panel also shows the speedup over official on one GPU. Each panel has its own scale.

At 15 seconds the picture changes: a clip has 109k tokens, dense attention grows with their square, and attention becomes about 75% of each forward. That is the case FP4 attention targets below.

The NVFP4 models also run on local Blackwell hardware such as DGX Spark and RTX 5090. On one DGX Spark, the NVFP4 QAD model (BF16 attention) generates a 5-second 480p first-and-last-frame (FL2VA) clip in **59.5 seconds**.

## NVFP4 QAD[#](#nvfp4-qad)

Both adapters ship in NVFP4: 4-bit weights and activations, with one 8-bit scale per 16 values, for every attention and feed-forward linear in all 50 blocks. Three choices keep them close to BF16.

**Merge first.** Flex ships fp32 LoRA adapters. We merge each into its trunk in fp32 and round once, so quantization starts from the exact Flex weights:

```
W_merged = (W.float() + (alpha / rank) * B.float() @ A.float()).to(torch.bfloat16)
```

**Calibrate for video and audio.** Static activation scales are set on Flex’s own six-step trajectories. Scaling to the largest value wastes the 4-bit range on rare spikes, and minimizing overall error lets the many video tokens drown out the audio. Each layer instead keeps the clipping that best balances the two, which beat both alternatives.

**Distill under the deployed numerics.** The 4-bit student trains against the frozen BF16 model along its six-step path, with 4-bit math on from the first step. It matches both the final prediction and every block’s output, and a quarter of the time it starts from its own states to learn to correct its own drift.

| Distance to BF16 Flex (lower is better) | Quantized only | After QAD |
| --- | --- | --- |
| Ref2VA | 0.326 | **0.270** (−17%) |
| FL2VA | 0.272 | **0.234** (−14%) |

**A lower loss is not always a better model.** Every evaluation also samples full clips and checks first- and last-frame fidelity, audio and motion against limits set from seed noise. One run kept improving its score while its last frame drifted; the guard stopped it, and a lower learning rate fixed it.

## FP4 attention[#](#fp4-attention)

Long clips are attention-bound, so the second variant also quantizes queries and keys for FlashAttention-4’s NVFP4 kernel. Done naively, this costs 13-17% of the QAD score. Three choices recover most of it:

* **Smooth K.** Subtract each head’s mean key before quantizing. This is exact: `q·(k_j − k̄) = q·k_j − q·k̄`, and softmax ignores a shift shared by every key.
* **Rotate Q and K.** Apply the same orthonormal Hadamard matrix to both. This is also exact, since `(qH)·(kH) = q·k`, and it spreads outlier channels evenly across the 16-value scale blocks.
* **Keep two blocks in BF16.** Blocks 45 and 49 carry most of the remaining error, so their attention stays BF16.

Shared key bias 
Outlier channel strength

Smooth-Ksubtract the mean key
Hadamardrotate Q and K

One NVFP4 block of a key: 16 values, one shared scale

Attention weights of one query over 12 keys

exact BF16 Q/K in NVFP4

FP4 attention error, mean of 100 random heads

softmax(QKᵀ) before quantization, transformed vs original

Toy heads: 64 channels (four 16-value blocks), 32 keys, Gaussian values, keys share a per-channel bias and two channels are scaled up. Quantization follows FlashAttention-4's NVFP4 path: E2M1 values, one E4M3 scale per 16 channels, unit global scale; P and V stay in BF16. Everything is computed in your browser.

| Per-layer FP4 attention error, real Flex activations | FL2VA | Ref2VA |
| --- | --- | --- |
| Plain FP4 | 0.115 | 0.113 |
| + smooth K + Hadamard | 0.095 | 0.095 |
| + blocks 45 and 49 in BF16 | **0.083** | **0.080** |

Distillation then closes most of the remaining gap: FL2VA lands at 0.237 against 0.234 with BF16 attention, and Ref2VA at 0.276 against 0.270. A fused kernel applies both transforms while quantizing Q and K, so they cost under 1 ms per attention call:

| One GB200, end to end | BF16 attention | FP4 attention |
| --- | --- | --- |
| 480p, 5 s | 5.79 s | 5.74 s |
| 768p, 15 s | 101.8 s | **85.3 s (−16%)** |

* ✓ **Bit-exact export:** the released 4-bit weights are byte-identical to what training quantized.
* ✓ **Train what we ship:** the training-time FP4 attention matches FlashAttention-4's kernel to within 1% of its quantization error.
* ✓ **Exact transforms:** softmax(QKᵀ) is unchanged before quantization (checked live in the figure).

## 2K[#](#2k)

FastVideo now runs NVIDIA’s [Open-H3-Regenerate-2K](https://huggingface.co/Efficient-Large-Model/Open-H3-Regenerate-2K), which regenerates a 768p H3 video at 2560x1440. Any H3-family draft works, from FastH3 or Flex. With the NVFP4 QAD Flex model as the draft and our NVFP4 decoder, which takes the 2K decode from 23.3 s to 5.0 s, text to 2K drops from about 7 minutes to under 2:

| Text to 2K, one GB200 | Draft | Total |
| --- | --- | --- |
| Base H3 draft (50 steps), as released | 316 s | 412 s |
| Pika H3 Flex NVFP4 QAD draft + NVFP4 decoder | 16.8 s | **106 s** |

◀ ▶

768p draft2560×1440

Drag the handle to compare. Five 768p drafts from the NVFP4 QAD model, each regenerated at 2560×1440 with Open-H3-Regenerate-2K and the NVFP4 VAE decoder on one GB200. Times shown are end to end per clip.

## Try it[#](#try-it)

The easiest way to run Flex is the [FastVideo cookbook](https://haoailab.com/FastVideo/cookbook/minimax-h3/models/pika-h3-flex-t2va/): pick a task, resolution, duration and weights (BF16, NVFP4 QAD or NVFP4 QAD with FP4 attention), and copy a ready-to-run command. Or run it directly:

```
FASTVIDEO_ATTENTION_BACKEND=FLASH_ATTN FASTVIDEO_FA4=1 \
python examples/inference/basic/basic_pika_h3_flex.py --weights nvfp4-qad \
  --task t2va --prompt "..." --resolution 768p --duration 5
```

| Weights | Hugging Face |
| --- | --- |
| BF16 (Pika’s release) | [Pika-Labs/Pika-H3-Flex](https://huggingface.co/Pika-Labs/Pika-H3-Flex) |
| NVFP4 QAD, BF16 attention | [FastVideo/Pika-H3-Flex-NVFP4-QAD](https://huggingface.co/FastVideo/Pika-H3-Flex-NVFP4-QAD) |
| NVFP4 QAD, FP4 attention | [FastVideo/Pika-H3-Flex-NVFP4-FP4Attn-QAD](https://huggingface.co/FastVideo/Pika-H3-Flex-NVFP4-FP4Attn-QAD) |

The NVFP4 models need a Blackwell GPU. The full training recipe, from adapter merge and calibration through QAD and export, is in the [training guide](https://github.com/hao-ai-lab/FastVideo/blob/main/docs/training/pika_h3_flex_qad.md).

## Acknowledgements[#](#acknowledgements)

Pika H3 Flex is built by [Pika](https://pika.art/). We thank the Pika team for open-sourcing Flex, its adapters and its inference code. FastH3 and Flex both build on [MiniMax H3](https://huggingface.co/MiniMaxAI/MiniMax-H3), and we thank the MiniMax team for releasing its weights and code.

We thank NVIDIA’s [Efficient-Large-Model](https://huggingface.co/Efficient-Large-Model) team for releasing Open-H3-Regenerate-2K, and the NVIDIA Enterprise Products team (Pengcheng Li and Cliff Woolley) for the Video Sparse Attention kernel used by FastH3. We thank the FlashAttention, FlashInfer and NVIDIA Model Optimizer teams for the attention and FP4 kernels and calibration tools this work relies on, and the [NVIDIA FastGen](https://github.com/NVlabs/FastGen) team (Julius Berner, Chao Liu and Arash Vahdat) for the DMD2 framework and H3 reference work.

We thank the upstream serving, kernel and open-source communities whose implementations make these experiments possible, and the [vLLM project](https://vllm.ai/), [NVIDIA](https://www.nvidia.com/en-us/) and [MBZUAI](https://mbzuai.ac.ae/) for their support of FastVideo.

## FastVideo team[#](#fastvideo-team)

**Contributor:** [Aryan Kumar](https://github.com/aryan5v)

  
**Tech lead:** [Will Lin](https://github.com/SolitaryThinker)

  
**Advisor:** [Hao Zhang](https://github.com/zhisbug)
