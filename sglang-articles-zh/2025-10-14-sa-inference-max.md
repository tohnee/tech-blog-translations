---
title: "SGLang 与 NVIDIA 携手加速 SemiAnalysis InferenceMAX 与 GB200"
title_en: "SGLang and NVIDIA Accelerating SemiAnalysis InferenceMAX and GB200 Together"
author: "NVIDIA and community SGLang developers"
date: "Oct 14, 2025"
previewImg: /images/blog/sa_inference_max/nvidia_gb200_nvl72.jpeg
source: https://lmsys.org/blog/2025-10-14-sa-inference-max/
translated: 2026-09-12
---

# SGLang 与 NVIDIA 携手加速 SemiAnalysis InferenceMAX 与 GB200

> 原文：[SGLang and NVIDIA Accelerating SemiAnalysis InferenceMAX and GB200 Together](https://lmsys.org/blog/2025-10-14-sa-inference-max/) · LMSYS Blog · NVIDIA and community SGLang developers

SGLang 与 NVIDIA 团队有着出色的合作记录，持续交付推理优化与系统级改进，确保 SGLang 框架始终具备卓越性能。最近，这一合作的重心放在了 **NVIDIA Blackwell 架构**——NVIDIA 最新的数据中心 GPU 上。借助 **FP8 注意力**、**NVFP4 MoE** 和 **PD 分离式专家并行**架构等 Blackwell 关键特性，SGLang 在高吞吐量下取得了[突破性性能](https://lmsys.org/blog/2025-09-25-gb200-part-2/)。在一台 NVIDIA GB200 NVL72 系统上，SGLang 服务 DeepSeek R1 模型时，预填充与解码阶段的每 GPU 吞吐分别达到惊人的 **26k 输入与 13k 输出 token/秒**。这一里程碑代表了大规模部署下成本与能效的新高度。

这项联合工作的成果，进一步体现在 SGLang 在最新发布的 SemiAnalysis InferenceMAX v1 基准测试中的表现上。[InferenceMAX](https://newsletter.semianalysis.com/p/inferencemax-open-source-inference) 是一个持续性基准测试框架，它在不同的输入/输出配置下运行推理测试，并每日发布更新的结果。

在 Blackwell GPU（GB200/B200）上用 SGLang 运行 DeepSeek R1 模型，相比上一代 Hopper GPU（H100/H200）最高可获得 **4 倍性能提升**。在评估延迟与吞吐量之间关键权衡的整条 Pareto 前沿上，都能一致地观察到这一提升。

## SemiAnalysis InferenceMAX 基准测试

LLM 推理性能由两大支柱驱动：**硬件与软件**。硬件创新带来阶跃式的提升，而软件则每天都在演进，持续带来性能收益。SemiAnalysis InferenceMAX™ 基准测试正是为捕捉这一动态而设计的。它每晚在数百块芯片上运行一整套基准测试，持续重新评估全球最流行的开源推理框架与模型，以实时追踪真实性能。实时看板已在 [inferencemax.ai](https://inferencemax.ai/) 向公众开放。

InferenceMAX™ 的一个核心目标，是提供能够覆盖不同 GPU、推理引擎与工作负载全部可能组合的基准测试。为确保服务器配置反映真实世界的部署情况，基准测试的组织方要求硬件厂商提交与其文档化最佳实践一致的配置。

**值得注意的是，该基准测试选定 SGLang 作为在 NVIDIA 与 AMD 硬件上运行 DeepSeek 模型的默认推理引擎**，这证明了 SGLang 对这些最先进模型所做的高度专业化优化。

下图展示了 1k 输入 token、8k 输出 token 配置下的结果，重点呈现 Blackwell 上的性能。

<img src="/images/blog/sa_inference_max/deepseek_fp8_results.jpg" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 85%"></img>
<p style="color:gray; text-align: center;">图 1：SGLang 在不同硬件平台上的性能。（来源：https://inferencemax.ai/）</p>

## SGLang 对大规模专家混合（MoE）模型的优化

上述性能提升，源自针对大规模专家混合（MoE）模型所做的深度系统级优化。

### 预填充-解码分离（PD 分离）与大规模专家并行

LLM 推理是一个两阶段过程：处理输入提示的计算密集型**预填充（prefill）**阶段，以及生成输出 token 的内存密集型**解码（decode）**阶段。在统一引擎中同时处理这两个阶段会产生低效问题，例如预填充批次打断解码流。

为解决这一问题，SGLang 实现了**预填充-解码分离（PD 分离，PD Disaggregation）**，将两个阶段拆分到不同的引擎中，从而可以对各自进行量身定制的调度与优化。这一架构对高效实现**大规模专家并行（EP）**至关重要，尤其是在使用 DeepEP 这类通信库时。DeepEP 对预填充（高吞吐）和解码（低延迟）使用不同的分发模式，统一引擎无法与之兼容。通过分离部署，SGLang 可以在每个阶段使用最优的 DeepEP 模式，最大化整体系统效率。

### Blackwell 专属 kernel 优化

通过与 NVIDIA 的合作，我们开发并集成了高度优化的 kernel，充分挖掘 Blackwell 架构的新能力：

* **FP8 注意力：** 对 KV 缓存使用 FP8 精度，可将解码期间的内存访问压力减半，并允许使用更快的 Tensor Core 指令。这不仅加速了注意力 kernel，还支持更大的批大小和更长的序列。
* **NVFP4 GEMM：** 对 MoE 专家和其他 GEMM 采用新的 NVFP4 精度，可降低内存带宽占用、发挥强大的 FP4 Tensor Core 能力，并将 token 分发的通信流量减半。这减少了权重内存占用，为更大的 KV 缓存腾出空间。
* **计算-通信重叠：** Blackwell 系统上大幅提升的通信带宽，使得可以采用更细粒度的方式将通信与计算重叠，更有效地隐藏通信延迟。
* **优化 kernel：** 我们集成了一套新的优化 kernel，包括 **NVIDIA Blackwell DeepGEMM**、用于 NVFP4 GEMM 和 FP8 注意力的 **FlashInfer** kernel、**Flash Attention CuTe** 以及 **CUTLASS MLA**，全部经过重写以利用 TMA 和集群启动控制（cluster launch control）等 Blackwell 新架构特性。

欲了解更多细节，请参阅我们的详细技术博客：

* [在 96 块 H100 GPU 上以 PD 分离与大规模专家并行部署 DeepSeek](https://lmsys.org/blog/2025-05-05-large-scale-ep/)
* [在 GB200 NVL72 上以 PD 分离与大规模专家并行部署 DeepSeek（第一篇）：解码吞吐提升 2.7 倍](https://lmsys.org/blog/2025-06-16-gb200-part-1/)
* [在 GB200 NVL72 上以 PD 分离与大规模专家并行部署 DeepSeek（第二篇）：预填充吞吐提升 3.8 倍、解码吞吐提升 4.8 倍](https://lmsys.org/blog/2025-09-25-gb200-part-2/)

<img src="/images/blog/gb200_part_2/primary.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 85%"></img>
<p style="color:gray; text-align: center;">图 2：SGLang 在预填充-解码分离与专家并行下的性能。（来源：https://lmsys.org/blog/2025-09-25-gb200-part-2/）</p>

## 未来的合作

接下来，我们将在运行时和 kernel 两个层面加强与 NVIDIA 团队的合作。我们将继续为 **DeepSeek v3.2、GPT-OSS 和 QWen 系列模型**优化性能，覆盖从紧凑的 [DGX Spark](https://lmsys.org/blog/2025-10-13-nvidia-dgx-spark/) 到 GB200、GB300 等整机架超级计算机的所有最新 NVIDIA GPU。

我们还计划与 SemiAnalysis 团队更紧密地合作，让 InferenceMAX 基准测试更加系统化、可复现、可靠。我们期待协助他们搭建并验证我们所有的整机架解决方案。

## 致谢

我们感谢社区中每一位帮助这项工作得以实现的人。

**NVIDIA 团队：** Trevor Morris, Kaixi Hou, Elfie Guo, Nicolas Castet, Faraz Khoubsirat, Ishan Dhanan, Shu Wang, Pavani Majety, Zihao Ye, Yingyi Huang, Alex Zhurkevich, Kushan Ahmadian, Pen Li, Juan Yu, Kedar Potar, Grace Ho, Lingjie Wu, Yiheng Zhang, Kyle Liang 以及更多贡献者

**SGLang 团队：** Jingyi Chen, Baizhou Zhang, Jiexin Liang, Qiaolin Yu, Yineng Zhang, Ke Bao, Liangsheng Yin, Jianan Ji, Ying Sheng

**SemiAnalysis 团队：** Dylan Patel, Kimbo Chen, Cam 等
