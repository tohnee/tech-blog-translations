---
title: "FastVideo FastH3 落地本地：在 NVIDIA DGX Spark 与 Apple Silicon 上实现 7 倍加速"
title_en: "FastVideo FastH3 Goes Local: 7x Speedup on NVIDIA DGX Spark and Apple Silicon"
date: 2026-09-02
source: https://haoailab.com/blogs/fasth3-local/
crawled: 2026-11-16
translated: 2026-11-16
---

# FastVideo FastH3 落地本地：在 NVIDIA DGX Spark 与 Apple Silicon 上实现 7 倍加速

> 原文：[FastVideo FastH3 Goes Local: 7x Speedup on NVIDIA DGX Spark and Apple Silicon](https://haoailab.com/blogs/fasth3-local/) · Hao AI Lab @ UCSD

2026 年 9 月 2 日 · 9 分钟 · FastVideo Team

![FastH3 在 Apple Silicon 与 DGX Spark 上](img/cover.png)

[![](https://img.shields.io/github/stars/hao-ai-lab/FastVideo?style=social)](https://github.com/hao-ai-lab/FastVideo)[![](https://img.shields.io/badge/🤗%20huggingface--green.svg?style=social)](https://huggingface.co/collections/FastVideo/fastvideo-fasth3)[![Slack](https://img.shields.io/badge/Slack--4A154B?style=social&logo=slack&logoColor=blue)](https://join.slack.com/t/fastvideo/shared_invite/zt-3f4lao1uq-u~Ipx6Lt4J27AlD2y~IdLQ)

## **TL;DR:**[#](#tldr)

FastVideo FastH3 现在最多可以跑在两台 NVIDIA DGX Spark 上，也能跑在 Apple Silicon 上。最高 8 倍加速！我们还会分享一些 FastH3 后续版本的消息。

FastVideo FastH3 构建于 [Minimax H3](https://huggingface.co/MiniMaxAI/MiniMax-H3) 之上。感谢 Minimax 团队发布其权重与代码。

FastVideo 团队与 [Nuva Lab](https://nuvalab.ai/)、[NVIDIA FastGen](https://github.com/NVlabs/FastGen)（Julius Berner、Chao Liu、Arash Vahdat）以及 NVIDIA Enterprise Products（Pengcheng Li、Cliff Woolley）团队紧密合作，共同完成了 [FastH3 Preview](/blogs/fasth3-preview/)。

H3 同时生成视频与音频。过去，这意味着必须用数据中心 GPU。我们的 [FastH3 Preview](/blogs/fasth3-preview/) 把它蒸馏成 NVIDIA Blackwell 上的几步采样。本次发布把该模型带到了 NVIDIA DGX Spark（最多两台）以及通过 MLX 的 Apple Silicon 上。Mac 路径需要 36 GB 或更多统一内存。一对 Spark 可以通过 QSFP 共享同一个片段。

本文还首次发布了 [FastVideo Cookbook](/FastVideo/cookbook/)。MiniMax H3 已收录其中，配有 CUDA、原生 MLX、Spark 双机配方，以及一个本地 OpenAI 兼容服务器。

## 本地生成[#](#generated-locally)

相同的提示词，分别在 Apple M4 Max、NVIDIA DGX Spark 和四台 GB200 上生成。请打开声音。

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--platforms--mac-space-gate.mp4)

**M4 Max**504 秒 · 冷启动

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--platforms--spark-astronaut-gateway.mp4)

**DGX Spark**264 秒 · 冷启动

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--platforms--gb200-space-gate.mp4)

**4 台 GB200**10.2 秒 · 首个请求

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--platforms--mac-desert-fashion.mp4)

**M4 Max**465 秒 · 冷启动

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--platforms--spark-fashion-highway.mp4)

**DGX Spark**243 秒 · 冷启动

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--platforms--gb200-desert-fashion.mp4)

**4 台 GB200**5.1 秒 · 热启动

这六个片段用的是同一套配方：832×480、124 帧、四步 FastH3、完整 VAE。图表把首次生成与重复生成区分开。Spark 的重复生成是在同一进程内的第二次生成，而不是已加载的服务器；Qwen 与 DiT 仍会重新加载，那 20 到 31 秒里大部分是此前已经付出的 VAE 编译开销。GB200 是已加载的服务器，350 秒的模型启动时间不计入两根柱子。

在 Mac 上，等待主要花在去噪上；在搭配完整 VAE 的 Spark 上，主要花在解码上。

![M4 Max、Spark 和四台 GB200 上，首次生成与重复生成时各阶段占端到端时间的比例](img/fig_platform_stages.svg)

图 1. 相同的 832×480、124 帧、完整 VAE 配方。Mac 的重复生成使用缓存后的提示词，Spark 的重复生成在同一进程内，GB200 是已加载的服务器。

## DGX Spark 上的 FastH3[#](#fasth3-on-dgx-spark)

[DGX Spark](https://www.nvidia.com/en-us/products/workstations/dgx-spark/) 是 NVIDIA 的桌面级 Blackwell 机器：GB10 GPU、128 GB 统一 LPDDR5X、CUDA 13、ARM64。Preview 版本中的 FastH3 CUDA 路径现在可以在这里运行，单台或两台均可。

模型虽然装得下，但没法按常规方式加载。

它没有独立的显存。CPU 与 GPU 共享同一个内存池，带宽约 270 GB/s，大约只有数据中心 HBM 的十分之一。FastH3 的编码器、transformer 与解码器加起来，超过了工作负载实际可用的 121 GB。若让它们全部常驻，进程在第一帧之前就会挂掉。

因此流水线从不把它们同时持有：编码提示词后卸载文本编码器，加载 transformer，去噪，卸载 transformer，然后加载 VAE。patch 大小与压缩比从检查点配置中读取，所以解码不必为了读一个 patch 大小而常驻 65 GB 的 DiT。

在独立显卡上，把权重复制到主机内存可以释放显存；在 Spark 上，这次复制落在同一个内存池里。我们取消了它，DiT 权重直接加载到 GPU 上。在单块 GB10 上，这让 transformer 的加载时间从 445 秒降到 39 秒，让一次 768×1344、124 帧的运行从 772 秒降到 336 秒。

H3 从不使用文本编码器的最后几层，Spark 路径会跳过它们。Video Sparse Attention 仍运行在 CUDA 上，FastVideo 的 kernel 针对 `sm_121` 从源码构建。

一对 Spark 可以共享同一次生成。序列并行把去噪与解码分摊到两块 NVIDIA GB10 上，通过 QSFP 链路通信。每台机器仍然分阶段加载组件。transformer 需要复制到两台机器上，所以任何一台都无法跳过这种分阶段加载。

在同样的 768×1344、124 帧配方下，两台 Spark 用 292 秒完成，单台需要 374 秒。那一对机器上使用 TAEH3 时为 195 秒。一个 345 帧的片段（约 14 秒视频），在搭配完整 H3 VAE 的双机上用 581 秒完成。

![单台与两台 DGX Spark 在 832×480 与 768×1344 下、使用完整 VAE 与 TAEH3 的端到端生成时间](img/fig_spark_setups.svg)

图 2. 一台 NVIDIA DGX Spark，或一对。GB10 上的冷启动进程。在 768×1344 下，TAEH3 解码为 12.5 秒，而不是 480p 下看到的 1 秒。

公开的 [vLLM-Omni MiniMax H3 DGX Spark 配方](https://recipes.vllm.ai/MiniMaxAI/MiniMax-H3?hardware=dgx_spark_gb10) 从 1024×576、五秒、50 步开始。在单台 Spark 上，该请求耗时 1881 秒。相同形状的 FastH3 用四步在 268 秒内完成，约 7 倍。832×480 是 8.4 倍，1344×768 是 7.9 倍。同一台机器，同样 124 帧的片段。

安装请参考 [CUDA 13 Spark 指南](/FastVideo/getting_started/installation/spark/)。双机请遵循 [双机指南](/FastVideo/getting_started/installation/spark_pair/)，然后在 [Cookbook](/FastVideo/cookbook/minimax-h3/) 里选一个 CUDA 配方。

## H3 如何在 Mac 上运行[#](#how-h3-runs-on-a-mac)

权重只是问题的一部分。H3 还需要一个大型文本编码器、去噪所需的工作内存，以及视频和音频解码器。在 36 GB 的 Mac 上把这些一次性全加载进来，就没什么内存留给生成了。

所以运行时压根不这么干，它分阶段执行：编码提示词、去噪、解码、导出。每个阶段只加载所需部分，用完即释放。

**编码**流式加载文本编码器

**→**

**去噪**视频与音频一起处理

**→**

**解码**画面与音轨

**→**

**导出**一个同步的 MP4

H3 读取的是 Qwen3-VL 的中间层，因此编码器会跳过最后 14 层。它逐层流式加载其余部分，只保留提示词用到的那些嵌入行。未缓存的提示词过去要在这里花约 80 秒。对每个张量做一次有界读取，把这一时间降到约 17 秒，且隐藏特征完全相同。缓存这些嵌入后，下一条提示词就能跳过这个阶段。

去噪之后，分块视频解码与原生音频解码器完成片段，无需一次性重建整个帧缓冲。

![M4 Max 上一次 FastH3 生成过程中的时间与内存](img/fig_mac_phases.svg)

图 3. 缓存提示词后，17 秒的编码阶段就消失了。TAEH3 把解码从 102 秒降到 1 秒，并把峰值解码内存从 11.0 GiB 降到 3.6 GiB。

更小的权重并不总是更快。H3 要做大尺寸的视频与音频矩阵乘法。在这些形状下，把量化权重解包成 BF16、再用 MLX 的稠密矩阵乘法，反而胜过量化 kernel。解包出来的副本在乘法后即被丢弃。

在一次四步 INT6 运行中，去噪从 386.47 秒降到 348.75 秒，视频与音频隐变量逐比特一致，MLX 峰值内存从 19.31 GiB 升到 19.46 GiB。那次运行使用 832×480、124 帧和稠密注意力，所以这是 matmul 路径，而不是 Video Sparse Attention。

Mac 路径仍然实现了 Video Sparse Attention：被选中的视频瓦片参与注意力，其余不参与。

## INT8、INT6 与 INT4[#](#int8-int6-and-int4)

本文所有 Mac 数字都来自一台 36 GB 统一内存的 M4 Max。

INT8 保留了更多原始权重，INT4 给激活留出的空间最大，INT6 是我们计时的默认选项。三者的实际耗时差别很小，峰值内存差别明显。相同提示词，相同随机种子。

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--quant--int8.mp4)

**INT8**481 秒 · 峰值 24.2 GiB

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--quant--int6.mp4)

**INT6**456 秒 · 峰值 19.5 GiB

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--quant--int4.mp4)

**INT4**467 秒 · 峰值 14.8 GiB

INT8、INT6 与 INT4 的 MLX 权重都在 [Hugging Face](https://huggingface.co/FastVideo/models) 上。

## 完整 VAE 与 TAEH3[#](#full-vae-versus-taeh3)

完整的 H3 VAE 是质量路线，[TAEH3](https://github.com/madebyollin/taehv) 是预览路线。它重建同样的隐变量要快得多，但细节会变柔：头发、织物和远景会失去锐度。

在 M4 Max 上，分块 H3 VAE 解码耗时 104 秒，TAEH3 只需 1 秒。在单台 Spark 上，VAE 解码为 114 秒，TAEH3 为 1.3 秒；该机上使用 TAEH3 的端到端时间为 134 秒，双机为 119 秒。在双 Spark 的 768×1344 下，TAEH3 解码为 12.5 秒，片段在 195 秒内完成。用 TAEH3 来检验提示词，满意后再用完整 VAE 出片。

相同提示词与随机种子。第一行是完整 VAE，第二行是 TAEH3。列为 M4 Max、单台 Spark、两台 Spark。

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--taeh3--mac-full-vae.mp4)

**M4 Max**完整 VAE · 451 秒

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--taeh3--1spark-full-vae.mp4)

**1 台 Spark**完整 VAE · 243 秒

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--taeh3--2spark-full-vae.mp4)

**2 台 Spark**完整 VAE · 209 秒

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--taeh3--mac-taeh3.mp4)

**M4 Max**TAEH3 · 350 秒

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--taeh3--1spark-taeh3.mp4)

**1 台 Spark**TAEH3 · 134 秒

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--taeh3--2spark-taeh3.mp4)

**2 台 Spark**TAEH3 · 119 秒

## 更快的草稿[#](#faster-drafts)

原生分辨率的片段要等一会儿。作为最终渲染，这没问题；但为了发现提示词写错而付这个代价，就太贵了。

`--fast` 会去噪更少的视频帧，再插值回 124 帧。这次运行生成了 73 帧，RIFE 补齐其余部分，音频保持完整时长。

`--fast-spatial` 在更小的画布上去噪，再上采样。下面这个片段用的是保守设置，672×384 上采样到 832×480。构图与细节会变柔，请把它当作预览开关，而不是最终渲染。

M4 Max 上相同的提示词与随机种子，INT6、缓存提示词、完整 VAE。

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--drafts--baseline.mp4)

**Baseline**457 秒 · 19.5 GiB

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--drafts--temporal-fast.mp4)

**Temporal fast**248 秒 · 1.84×

[
](https://github.com/hao-ai-lab/hao-ai-lab.github.io/releases/download/website-demo-media-v2/fasth3-local--img--videos--drafts--spatial-fast.mp4)

**Spatial fast**272 秒 · 1.68×

## FastVideo Cookbook[#](#fastvideo-cookbook)

打开 [Cookbook](/FastVideo/cookbook/)，选一个模型、选一个配方，复制一条我们真正跑过的命令。

H3 已在其中，带 CUDA、四步 preview、LoRA、原生 MLX 和双 Spark 配方。

你也可以把 FastH3 作为服务来跑。在 CUDA 或 MLX 上启动一次服务器，然后就可以从 playground、cURL，或你应用里的 OpenAI 兼容 SDK 更换提示词。后续提示词复用该进程，不必每次都重新加载模型。可打开 [H3 配方](/FastVideo/cookbook/minimax-h3/) 或 [服务器指南](/FastVideo/cookbook/openai-api/)。Spark 用户请先按 [CUDA 13 Spark 指南](/FastVideo/getting_started/installation/spark/) 安装，双机请遵循 [双机指南](/FastVideo/getting_started/installation/spark_pair/)。

**[FastVideo Cookbook](/FastVideo/cookbook/)**
持续维护的推理配方，从 MiniMax H3 开始。蒸馏、训练与评测一旦发布，也会进入同一目录。

我们仍在压缩延迟、加入更多蒸馏模型，并研究少于四步的采样调度。RTX 系列（包括 5090 与 4090）是下一个 CUDA 重点。

Apple 刚发布了 [Mac mini 的 M6 与 Mac Studio 的 M5 Ultra](https://www.apple.com/newsroom/2026/08/apple-introduces-m6-and-m5-ultra-for-a-big-leap-in-performance-and-ai-compute/)。我们还没有在这些芯片上运行 FastH3，也没有在 M5 Max 或 M5 Pro Mac mini 上跑过。本文所有 Mac 数字都来自 M4 Max。MLX 路径在这些芯片上是一样的，它们应该更快，尤其是拥有大容量统一内存与更强 GPU 的 M5 Ultra。我们很想实测它们。

如果你测了新机器、改进了 kernel，或碰到 bug，请从 [贡献指南](/FastVideo/contributing/overview/) 或 [代码仓库](https://github.com/hao-ai-lab/FastVideo) 开始，并附上硬件、设置、耗时和输出。

## 致谢[#](#acknowledgements)

FastVideo FastH3 构建于 [Minimax H3](https://huggingface.co/MiniMaxAI/MiniMax-H3) 之上。感谢 Minimax 团队发布其权重与代码。

感谢 NVIDIA Enterprise Products 团队（Pengcheng Li、Cliff Woolley）在 FastH3 所用 Video Sparse Attention（VSA）kernel 上的出色工作！

FastVideo 团队与 [Nuva Lab](https://nuvalab.ai/)、[NVIDIA FastGen](https://github.com/NVlabs/FastGen)（Julius Berner、Chao Liu、Arash Vahdat）以及 NVIDIA Enterprise Products 团队在 [FastH3](/blogs/fasth3-preview/) 上紧密合作。

感谢 Ollin Boer Bohan 的 [TAEH3](https://github.com/madebyollin/taehv)，这是本次发布所用的可选预览解码器。Mac 路径建立在 [MLX](https://github.com/ml-explore/mlx) 及其社区之上。

我们还要感谢 [vLLM 项目](https://vllm.ai/)、[NVIDIA](https://www.nvidia.com/en-us/) 和 [MBZUAI](https://mbzuai.ac.ae/) 对 FastVideo 的持续赞助与支持。

## FastVideo 团队[#](#fastvideo-team)

**贡献者：** Aryan Kumar\*
,
Kyle Hu\*
,
Satyam Srivastava\*
,
Ishan Vaish
  
（\*同等贡献）  
**技术负责人：** Will Lin
  
**指导：** Hao Zhang
