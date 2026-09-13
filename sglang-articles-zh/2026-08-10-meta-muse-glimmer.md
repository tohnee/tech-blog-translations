---
title: "SGLang 为 Muse Glimmer 提供 Day-0 支持：一款面向本地智能体工作流的多模态模型"
title_en: "SGLang Adds Day-0 Support for Muse Glimmer, a Multimodal Model Built for Local Agentic Workflows"
author: "Meta Superintelligence Labs and the SGLang Team"
date: "August 10, 2026"
previewImg: /images/blog/2026-08-10-meta-muse-glimmer/cover-muse-glimmer.png
type: blog
source: https://lmsys.org/blog/2026-08-10-meta-muse-glimmer/
translated: 2026-09-12
---

# SGLang 为 Muse Glimmer 提供 Day-0 支持：一款面向本地智能体工作流的多模态模型

> 原文：[SGLang Adds Day-0 Support for Muse Glimmer, a Multimodal Model Built for Local Agentic Workflows](https://lmsys.org/blog/2026-08-10-meta-muse-glimmer/) · LMSYS Blog · Meta Superintelligence Labs and the SGLang Team

我们很高兴与 Meta Superintelligence Labs 合作，为 SGLang 带来 [Muse Glimmer](https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model) 的 Day-0 支持（首发日支持），并针对本地硬件上智能体工作流的高性能推理做了专门优化。

## 亮点

- **模型：** Muse Glimmer 是一个 30B 参数的多模态稠密模型，拥有 128k+ token 的上下文窗口，可在本地硬件上对端到端智能体工作流提供有竞争力的性能。
- **性能：** 得益于针对 SGLang SM120 后端的专门优化，SGLang 在 NVIDIA GeForce RTX 5090 上可实现最高 **1,452 tok/s** 的总输出吞吐量和 **236 tok/s** 的单用户解码速度（NVFP4 配合 DFlash）。
- **特性：** SGLang 为 Muse Glimmer 提供广泛的原生特性支持，包括 DFlash 投机解码、RadixAttention 前缀缓存以及可中断 CUDA 图（breakable CUDA graphs）。
- **硬件：** 开发者可以在多种消费级和工作站硬件上部署 Muse Glimmer——通过 SM120 后端支持 NVIDIA GeForce RTX 5090、RTX PRO 6000 和 DGX Spark，通过 MLX 后端支持 Apple Silicon。

## Muse Glimmer 模型架构

Muse Glimmer 是一个 30B 模型，由一个 27.9B 的稠密文本解码器、一个 1.9B 的 ViT 以及一个基于 GELU 的多模态投影层组成。文本解码器共有 52 层 transformer 层。每层包含分组查询注意力（GQA），使用 32 个查询头和 2 个键值头，后接 SwiGLU 前馈网络。

### 滑窗注意力

为提升效率，解码器采用一种混合注意力模式：连续三层为 2,048 token 的滑窗注意力层，每第四层则为全序列注意力层。局部窗口使用 RoPE、全注意力层使用 NoPE 的组合，使模型能够将上下文长度扩展到超出其训练极限。

## 特性支持

### 对本地 AI 硬件的广泛后端支持

Muse Glimmer 可以通过 SGLang 部署在开发者本地构建和运行 AI 智能体时常用的各类硬件上，包括 Apple Silicon 设备（Mac mini 和 M 系列 MacBook Pro）、NVIDIA GeForce RTX 5090 GPU 以及 NVIDIA DGX Spark。在 NVIDIA SM120 平台上，SGLang 利用其优化过的 GEMM 后端和 FlashInfer 后端实现高吞吐推理；而 Apple Silicon 设备则使用原生 MLX 后端，提供高性能的本地推理服务。

### 使用 DFlash 的投机解码

要实现低延迟推理，请使用 SGLang 的 DFlash 实现：

```shell
--speculative-algorithm DFLASH
```

### SGLang 原生优化

Muse Glimmer 兼容 SGLang 的众多原生优化，包括低开销调度器、RadixAttention 前缀缓存以及可中断 CUDA 图。我们还将其中若干优化（包括前缀缓存）引入了 SGLang 的 MLX 后端，使 Apple Silicon 上的智能体工作负载也能获得有竞争力的性能。

### BF16、NVFP4、GGUF 与 MLX 4-bit 检查点

我们提供多种格式的 Muse Glimmer 检查点，以满足用户在硬件、模型保真度和系统性能方面的不同需求。

对模型保真度要求最高的开发者可以在单张 H100 GPU 上运行原生 BF16 检查点。SM120 路径包含约 19.5 GB 的 NVFP4+MXFP8 混合量化方案。18 GB 的 NVFP4 检查点搭配 5 GB 的 BF16 DFlash 草稿模型，可以轻松装进单张 RTX 5090，从而在 NVIDIA GeForce RTX 5090 加速卡和 DGX Spark 上实现高性能部署。

我们还提供两个 GGUF 检查点。其中较小的一个采用 Q4KM 格式，分组大小（group size）为 128。该检查点可实现更快的推理速度，并能部署在内存约束更严格的硬件上。Q4K-Dynamic 则能带来更好的模型质量。对于在 Apple Silicon 设备上开发的开发者，我们以 MLX 格式提供前述 GGUF 检查点。

## 性能结果

我们在七个平台上测量了 Muse Glimmer 配合 SGLang 的表现，扫描了 batch size 1 到 8。下表报告的是 batch 1 下的交互性（tok/s/user）和 batch 8 下的总输出吞吐量（tok/s）。

| 平台 | 精度 | 解码 | tok/s/user（batch 1） | 输出 tok/s（batch 8） |
| ----- | ----- | ----- | ----- | ----- |
| NVIDIA B300 | bf16 | Standard | 91.77 | 721 |
| NVIDIA B300 | bf16 | DFlash | 308.51 | 1261 |
| NVIDIA B300 | nvfp4 | Standard | 83.98 | 841 |
| NVIDIA B300 | nvfp4 | DFlash | 290.01 | 1295 |
| NVIDIA RTX PRO 6000 | bf16 | Standard | 25.7 | 200 |
| NVIDIA RTX PRO 6000 | bf16 | DFlash | 108.08 | 833 |
| NVIDIA RTX PRO 6000 | nvfp4 | Standard | 58.04 | 451 |
| NVIDIA RTX PRO 6000 | nvfp4 | DFlash | 214.11 | 1403 |
| NVIDIA DGX Spark | bf16 | Standard | 4.4 | 35 |
| NVIDIA DGX Spark | bf16 | DFlash | 19.1 | 134 |
| NVIDIA DGX Spark | nvfp4 | Standard | 12.1 | 92 |
| NVIDIA DGX Spark | nvfp4 | DFlash | 36.4 | 301 |
| NVIDIA RTX 5090 | nvfp4 | Standard | 63.9 | 501 |
| NVIDIA RTX 5090 | nvfp4 | DFlash | 236.4 | 1452 |
| NVIDIA RTX 5090 | q4_k_m | Standard | 72.6 | 230 |
| NVIDIA RTX 5090 | q4_k_m | DFlash | 140.7 | 332 |
| Apple M5 Pro | q4_k_m | Standard | 15.3 | 52.6 |
| Apple M5 Pro | q4 | Standard | 17.6 | 56.9 |
| Apple M5 Pro | q4k-dynamic | Standard | 12.6 | 49.1 |

DFlash 可将 batch 1 交互性提升 1.9–4.3 倍，具体取决于平台和精度：除 RTX 5090 上的 GGUF 路径（提升 1.9 倍）外，其余所有配置的提升都在 3.0 倍及以上。batch 8 下的提升幅度较小且波动更大，介于 1.4 倍到 4.2 倍之间。MLX 后端暂不支持投机解码。

## 致谢

我们感谢 Meta Superintelligence Labs 团队与 SGLang 社区的通力协作，使 SGLang 得以在 Muse Glimmer 发布首日即提供支持。
