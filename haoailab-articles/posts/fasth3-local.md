---
title: "FastVideo FastH3 Goes Local: 7x Speedup on NVIDIA DGX Spark and Apple Silicon"
date: 2026-09-02
source: https://haoailab.com/blogs/fasth3-local/
crawled: 2026-11-16
---

# FastVideo FastH3 Goes Local: 7x Speedup on NVIDIA DGX Spark and Apple Silicon

> 原文：[FastVideo FastH3 Goes Local: 7x Speedup on NVIDIA DGX Spark and Apple Silicon](https://haoailab.com/blogs/fasth3-local/) · Hao AI Lab @ UCSD

# FastVideo FastH3 Goes Local: 7x Speedup on NVIDIA DGX Spark and Apple Silicon

September 2, 2026 · 9 min · FastVideo Team

![FastH3 on Apple Silicon and DGX Spark](img/cover.png)

[![](https://img.shields.io/github/stars/hao-ai-lab/FastVideo?style=social)](https://github.com/hao-ai-lab/FastVideo)[![](https://img.shields.io/badge/🤗%20huggingface--green.svg?style=social)](https://huggingface.co/collections/FastVideo/fastvideo-fasth3)[![Slack](https://img.shields.io/badge/Slack--4A154B?style=social&logo=slack&logoColor=blue)](https://join.slack.com/t/fastvideo/shared_invite/zt-3f4lao1uq-u~Ipx6Lt4J27AlD2y~IdLQ)

## **TL;DR:**[#](#tldr)

FastVideo FastH3 now runs on up to 2x NVIDIA DGX Sparks and on Apple Silicon. Up
to 8x speedup! We also share some updates on next versions of FastH3!

FastVideo FastH3 builds on [Minimax H3](https://huggingface.co/MiniMaxAI/MiniMax-H3).
We thank the Minimax team for releasing its weights and code.

The FastVideo Team collaborated closely [Nuva Lab](https://nuvalab.ai/),  
[NVIDIA FastGen](https://github.com/NVlabs/FastGen) (Julius Berner, Chao Liu, Arash Vahdat), and NVIDIA Enterprise Products (Pengcheng Li, Cliff Woolley) team collaborated [FastH3 Preview](/blogs/fasth3-preview/).

H3 generates video and audio together. That used to mean a data-center GPU.
Our [FastH3 Preview](/blogs/fasth3-preview/) distilled it into a few steps on
NVIDIA Blackwell. This release puts that model on NVIDIA DGX Sparks (up to 2x) and Apple Silicon through MLX. The Mac path needs 36 GB of unified memory
or more. A pair of Sparks can share one clip over QSFP.

This post also publishes the [FastVideo Cookbook](/FastVideo/cookbook/) for
the first time. MiniMax H3 is on it, with CUDA, native MLX, a Spark-pair
recipe, and a local OpenAI-compatible server.

## Generated locally[#](#generated-locally)

The same prompts on an Apple M4 Max, NVIDIA DGX Spark, and four GB200s.
Turn the audio on.

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--platforms--mac-space-gate.mp4)

**M4 Max**504 s · cold

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--platforms--spark-astronaut-gateway.mp4)

**DGX Spark**264 s · cold

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--platforms--gb200-space-gate.mp4)

**4 GB200s**10.2 s · first request

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--platforms--mac-desert-fashion.mp4)

**M4 Max**465 s · cold

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--platforms--spark-fashion-highway.mp4)

**DGX Spark**243 s · cold

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--platforms--gb200-desert-fashion.mp4)

**4 GB200s**5.1 s · warm

Those six clips are the same recipe: 832×480, 124 frames, four-step FastH3,
full VAE. The chart splits a first generation from a repeat. Spark repeat is
a second generate in the same process, not a loaded server. Qwen and DiT
still reload. Most of those 20 to 31 seconds are VAE compile already paid.
GB200 is a loaded server. 350 s of model start sits outside both bars.

On the Mac, denoising is most of the wait. On Spark with the full VAE,
decode is.

![Share of end-to-end time per stage, first generation versus repeat, on M4 Max, Spark, and four GB200s](img/fig_platform_stages.svg)

Figure 1. Same 832×480, 124-frame, full-VAE recipe. Mac repeat is a cached prompt. Spark repeat is the same process. GB200 is a loaded server.

## FastH3 on DGX Spark[#](#fasth3-on-dgx-spark)

[DGX Spark](https://www.nvidia.com/en-us/products/workstations/dgx-spark/)
is NVIDIA’s desktop Blackwell machine. GB10 GPU, 128 GB of unified LPDDR5X,
CUDA 13, ARM64. The FastH3 CUDA path from the Preview release now runs here,
on one Spark or on a pair.

Although the model fits, we cannot load it the usual way.

There is no separate VRAM. CPU and GPU share one pool, at roughly 270 GB/s,
about a tenth of datacenter HBM. FastH3’s encoder, transformer, and decoders
add up to more than the 121 GB a workload actually gets. Keep them all
resident and the process dies before the first frame.

So the pipeline never holds them together. It encodes the prompt, drops the
text encoder, loads the transformer, denoises, drops the transformer, then
loads the VAE. Patch size and compression ratios come from the checkpoint
config, so decode does not keep a 65 GB DiT loaded just to read a patch size.

On a discrete GPU, copying weights to the host frees device memory. On Spark
that copy lands in the same pool. We stopped it. DiT weights load straight
onto the GPU. On one GB10 that cut the transformer load from 445 seconds to
39 seconds, and a 768×1344, 124-frame run from 772 seconds to 336 seconds.

H3 never uses the last layers of its text encoder. The Spark path skips them.
Video Sparse Attention stays on CUDA. The FastVideo kernel builds from source
for `sm_121`.

A pair of Sparks can share a single generation. Sequence parallel splits
denoising and decode across both NVIDIA GB10s over the QSFP link. Each box
still loads components in phases. The transformer is copied onto both, so
neither can skip the phased load.

On the same 768×1344, 124-frame recipe, two Sparks finished in 292 seconds.
One Spark took 374. TAEH3 on that pair was 195 seconds. A 345-frame clip,
about 14 seconds of video, finished in 581 seconds on the pair with the
full H3 VAE.

![DGX Spark end-to-end generation time for one Spark and two Sparks, full VAE and TAEH3, at 832 by 480 and 768 by 1344](img/fig_spark_setups.svg)

Figure 2. One NVIDIA DGX Spark, or a pair. Cold process starts on GB10. At 768×1344, TAEH3 decode is 12.5 s, not the 1 s you see at 480p.

The public [vLLM-Omni MiniMax H3 recipe for DGX Spark](https://recipes.vllm.ai/MiniMaxAI/MiniMax-H3?hardware=dgx_spark_gb10)
starts at 1024×576, five seconds, 50 steps. On one Spark that request took
1881 seconds. FastH3 at the same shape, four steps, finished in 268 seconds,
about 7×. 832×480 was 8.4×. 1344×768 was 7.9×. Same box, same 124-frame clip.

Install from the
[CUDA 13 Spark guide](/FastVideo/getting_started/installation/spark/). For a
pair, follow the
[pair guide](/FastVideo/getting_started/installation/spark_pair/), then pick a
CUDA recipe in the [Cookbook](/FastVideo/cookbook/minimax-h3/).

## How H3 runs on a Mac[#](#how-h3-runs-on-a-mac)

The weights are only part of the problem. H3 also needs a large text encoder,
working memory for denoising, and decoders for video and audio. Load all of
that at once on a 36 GB Mac and there is nothing left to generate with.

So the runtime never tries. It runs in phases. Encode the prompt, denoise,
decode, export. Each phase loads what it needs and frees the rest.

**Encode**Stream the text encoder

**→**

**Denoise**Video and audio together

**→**

**Decode**Frames and soundtrack

**→**

**Export**One synchronized MP4

H3 reads an intermediate layer of Qwen3-VL, so the encoder skips the last 14
layers. It streams the rest one layer at a time and keeps only the embedding
rows the prompt uses. An uncached prompt used to spend about 80 seconds here.
A single bounded read per tensor brings that to about 17 seconds, with the
same hidden features. Cache those embeddings and the next prompt skips this
stage.

After denoising, tiled video decode and a native audio decoder finish the clip
without rebuilding the whole frame buffer at once.

![Time and memory through one FastH3 generation on an M4 Max](img/fig_mac_phases.svg)

Figure 3. Cache the prompt and the 17 s encode disappears. TAEH3 drops decode from 102 s to 1 s, and peak decode from 11.0 GiB to 3.6 GiB.

Smaller weights are not always faster. H3 multiplies large video and audio
matrices. At those shapes, unpacking a quantized weight into BF16 and using
MLX’s dense matrix multiply beat the quantized kernel. The unpacked copy is
discarded after the multiply.

On a four-step INT6 run, denoising dropped from 386.47 seconds to 348.75
seconds. The video and audio latents were bit-exact. Peak MLX memory rose from
19.31 GiB to 19.46 GiB. That run used 832×480, 124 frames, and dense attention,
so this is the matmul path, not Video Sparse Attention.

The Mac path still implements Video Sparse Attention. Selected video tiles
attend. The rest do not.

## INT8, INT6, and INT4[#](#int8-int6-and-int4)

Every Mac number in this post comes from an M4 Max with 36 GB of unified
memory.

INT8 keeps more of the original weights. INT4 leaves the most room for
activations. INT6 is the default we timed. Wall clock barely moves across
the three. Peak memory does. Same prompt, same seed.

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--quant--int8.mp4)

**INT8**481 s · 24.2 GiB peak

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--quant--int6.mp4)

**INT6**456 s · 19.5 GiB peak

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--quant--int4.mp4)

**INT4**467 s · 14.8 GiB peak

INT8, INT6, and INT4 MLX weights are on
[Hugging Face](https://huggingface.co/FastVideo/models).

## Full VAE versus TAEH3[#](#full-vae-versus-taeh3)

The full H3 VAE is the quality path. [TAEH3](https://github.com/madebyollin/taehv)
is the preview path. It reconstructs the same latents much faster, and fine
detail goes softer. Hair, fabric, and distant backgrounds lose bite.

On an M4 Max, tiled H3 VAE decode took 104 seconds. TAEH3 took one second.
On one Spark, VAE decode was 114 seconds and TAEH3 was 1.3 seconds.
End-to-end with TAEH3 was 134 seconds on that box, 119 seconds on two.
At 768×1344 on two Sparks, TAEH3 decode was 12.5 seconds and the clip
finished in 195 seconds. Use TAEH3 to check a prompt. Render with the full
VAE when you like what you see.

Same prompt and seed. First row is the full VAE. Second row is TAEH3.
Columns are an M4 Max, one Spark, and two Sparks.

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--taeh3--mac-full-vae.mp4)

**M4 Max**Full VAE · 451 s

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--taeh3--1spark-full-vae.mp4)

**1 Spark**Full VAE · 243 s

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--taeh3--2spark-full-vae.mp4)

**2 Sparks**Full VAE · 209 s

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--taeh3--mac-taeh3.mp4)

**M4 Max**TAEH3 · 350 s

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--taeh3--1spark-taeh3.mp4)

**1 Spark**TAEH3 · 134 s

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--taeh3--2spark-taeh3.mp4)

**2 Sparks**TAEH3 · 119 s

## Faster drafts[#](#faster-drafts)

A native-resolution clip takes a while. That is fine for a final render. It
is a lot to pay to find out the prompt is wrong.

`--fast` denoises fewer video frames, then interpolates back to 124.
This run generated 73 frames. RIFE filled the rest. Audio keeps its full
duration.

`--fast-spatial` denoises a smaller canvas, then resamples up. The clip
below is the conservative setting, 672×384 up to 832×480. Composition and
fine detail get softer. Treat it as a preview knob, not a final render.

Same prompt and seed on the M4 Max. INT6, cached prompt, full VAE.

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--drafts--baseline.mp4)

**Baseline**457 s · 19.5 GiB

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--drafts--temporal-fast.mp4)

**Temporal fast**248 s · 1.84×

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--drafts--spatial-fast.mp4)

**Spatial fast**272 s · 1.68×

## FastVideo Cookbook[#](#fastvideo-cookbook)

Open the [Cookbook](/FastVideo/cookbook/), pick a model, pick a recipe, and copy
a command we actually run.

H3 is there with CUDA, the four-step preview, LoRA, native MLX, and a
two-Spark recipe.

You can also serve FastH3. Start the server once on CUDA or on MLX. Then
change prompts from the playground, from cURL, or from an OpenAI-compatible
SDK in your app. Later prompts reuse that process. You do not reload the
model for every try. Open the [H3 recipes](/FastVideo/cookbook/minimax-h3/)
or the [server guide](/FastVideo/cookbook/openai-api/). Spark users should
install from the
[CUDA 13 Spark guide](/FastVideo/getting_started/installation/spark/) first.
Two boxes should follow the
[pair guide](/FastVideo/getting_started/installation/spark_pair/).

**[FastVideo Cookbook](/FastVideo/cookbook/)**
Maintained inference recipes, starting with MiniMax H3. Distillation,
training, and evaluation land in the same catalog as they ship.

We are still cutting latency, adding distilled models, and looking at
schedules with fewer than four steps. The RTX family, including the 5090 and
4090, is the next CUDA focus.

Apple just announced
[M6 in the Mac mini and M5 Ultra in the Mac Studio](https://www.apple.com/newsroom/2026/08/apple-introduces-m6-and-m5-ultra-for-a-big-leap-in-performance-and-ai-compute/).
We have not run FastH3 on those, or on M5 Max or M5 Pro Mac mini. Every Mac
number here is from an M4 Max. The MLX path is the same on those chips. They
should be faster, especially M5 Ultra with its unified memory and GPU. We
want to measure them.

If you measure a new machine, improve a kernel, or hit a bug, start from the
[contribution guide](/FastVideo/contributing/overview/) or the
[repository](https://github.com/hao-ai-lab/FastVideo). Include hardware,
settings, timings, and the output.

## Acknowledgements[#](#acknowledgements)

FastVideo FastH3 builds on [Minimax H3](https://huggingface.co/MiniMaxAI/MiniMax-H3).
We thank the Minimax team for releasing its weights and code.

We thank the NVIDIA Enterprise Products team (Pengcheng Li, Cliff Woolley) for the amazing work on the Video Sparse Attention (VSA) kernel used by FastH3!

The FastVideo Team collaborated closely with [Nuva Lab](https://nuvalab.ai/),  
[NVIDIA FastGen](https://github.com/NVlabs/FastGen) (Julius Berner, Chao Liu, Arash Vahdat), and NVIDIA Enterprise Products team on [FastH3](/blogs/fasth3-preview/).

We thank Ollin Boer Bohan for [TAEH3](https://github.com/madebyollin/taehv),
the optional preview decoder this release uses. The Mac path is built on
[MLX](https://github.com/ml-explore/mlx) and the community around it.

We also thank the [vLLM project](https://vllm.ai/),
[NVIDIA](https://www.nvidia.com/en-us/), and [MBZUAI](https://mbzuai.ac.ae/) for
their continued sponsorship and support of FastVideo.

## FastVideo team[#](#fastvideo-team)

**Contributors:** Aryan Kumar\*
,
Kyle Hu\*
,
Satyam Srivastava\*
,
Ishan Vaish
  
(\*Equal Contribution)  
**Tech lead:** Will Lin
  
**Advisor:** Hao Zhang
