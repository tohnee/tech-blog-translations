---
title: "用 vLLM 运行 NVIDIA Nemotron 3 Nano Omni，实现高效的多模态智能体 AI"
title_en: "Run Highly Efficient Multimodal Agentic AI with NVIDIA Nemotron 3 Nano Omni Using vLLM"
source: https://vllm.ai/blog/2026-04-28-nemotron-omni
crawled: 2026-09-12
translated: 2026-09-13
---

# 用 vLLM 运行 NVIDIA Nemotron 3 Nano Omni，实现高效的多模态智能体 AI

> 原文：[Run Highly Efficient Multimodal Agentic AI with NVIDIA Nemotron 3 Nano Omni Using vLLM](https://vllm.ai/blog/2026-04-28-nemotron-omni) · vLLM 博客

NVIDIA Nemotron 团队

[#模型支持](https://vllm.ai/blog/tags/model-support)

我们很高兴在 vLLM 上支持新发布的 NVIDIA Nemotron 3 Nano Omni 模型。

[Nemotron 3 Nano Omni](https://developer.nvidia.com/blog/nvidia-nemotron-3-nano-omni-powers-multimodal-agent-reasoning-in-a-single-efficient-open-model) 是 Nemotron 3 开源模型家族的一员，是效率最高、精度领先的开源多模态模型，专为驱动在单一循环中跨视觉、音频和语言进行感知与推理的子智能体（sub-agent）而构建。

企业智能体工作流天生就是多模态的。智能体必须解读屏幕、文档、音频、视频和文本，而且往往要在同一轮推理中完成。然而当今大多数智能体系统把视觉、语音和语言模型拼在一起使用，导致推理跳数成倍增加、编排复杂化，上下文也在流水线中被割裂。

Nemotron 3 Nano Omni 解决了这种割裂带来的两大挑战：

- **模型割裂：** 串联运行独立的视觉、音频和语言模型，会因反复推理而增加延迟，放大成本与失败模式，并让上下文在各模态间变得支离破碎。Nemotron 3 Nano Omni 把这一切收敛为一个单一的多模态推理循环——一个模型同时理解屏幕、文档、音频和视频，大幅简化智能体工作流设计并显著降低编排开销。
- **效率：** 持续的感知工作负载——屏幕监控、文档理解、视频分析——要求大规模持续运行。Nemotron 3 Nano 的混合 MoE 架构每次前向传播只激活 30B 参数中的 3B，可提供高吞吐量，并通过时间感知感知（temporal-aware perception）和高效视频采样降低视频推理的算力开销，让常驻智能体无需付出高昂成本即可运行。

使用该模型，AI 系统将在相同交互性下取得比其他开源 omni 模型高 9x 的吞吐量，从而在不牺牲响应速度的前提下获得更低的成本和更好的可扩展性。

## TL;DR：关于 Nemotron 3 Nano Omni

- **架构：** 混合专家（MoE）+ Transformer-Mamba 混合架构
- **模型规模：** 30B 总参数，3B 激活参数
- **上下文长度：** 256K
- **统一的视觉与音频编码器**免去单独的感知模型——一个模型取代割裂的多模态技术栈。3D 卷积层（Conv3D）可高效处理视频中的时空数据。
- **模态：**
  - 输入：文本、图像、视频、音频
  - 输出：文本
- **效率：** 在相同交互性下取得比其他开源 omni 模型高 9x 的吞吐量。高效视频采样（Efficient Video Sampling，EVS）可在相同算力预算下处理更长的视频，并通过时间感知感知降低视频推理的算力开销。支持 FP8 与 NVFP4 量化，部署方式灵活。
- **精度：** 多模态智能比最佳开源替代品高 20%。
- **后训练：** 通过 NVIDIA NeMo RL 与 NeMo Gym 在文本、图像、音频和视频环境中进行多环境强化学习，提升指令遵循能力并向正确的多模态答案收敛。
- **支持的 GPU：** NVIDIA B200、H100、H200、A100、L40S、DGX Spark 与 RTX 6000

**快速上手：**

- 从 Hugging Face 下载模型权重——[BF16](https://huggingface.co/nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16)、[FP8](https://huggingface.co/nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-FP8)、[NVFP4](https://huggingface.co/nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-NVFP4)
- 使用[cookbook](https://github.com/NVIDIA-NeMo/Nemotron/blob/main/usage-cookbook/Nemotron-3-Nano-Omni/vllm_cookbook.ipynb)或通过 [Brev launchable](https://brev.nvidia.com/launchable/deploy?launchableID=env-3Cm2gB9j5ROkCbiNKH5SQhERqBV) 用 vLLM 运行推理
- 阅读[技术报告](https://research.nvidia.com/labs/adlr/files/NVIDIA-Nemotron-3-Omni-report.pdf)了解更多细节

## 用 vLLM 运行优化的多模态推理

Nemotron 3 Nano Omni 支持 BF16、FP8 与 NVFP4 精度，可在同一块 GPU 上实现加速推理并服务更多请求。按照以下说明即可上手。

### 安装 vLLM

```
pip install vllm[audio]==0.20.0
```

### 服务模型

你可以通过 OpenAI 兼容 API 服务 Nemotron 3 Nano Omni。根据你的环境按需设置注意力后端和所需的环境变量。FP8 与 NVFP4 的详细说明请参阅 cookbook。

```
python3 -m vllm.entrypoints.openai.api_server \
    --model "nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16" \
    --served-model-name nemotron \
    --trust-remote-code \
    --dtype auto \
    --host 0.0.0.0 \
    --port 5000 \
    --tensor-parallel-size 1 \
    --max-model-len 131072 \
    --media-io-kwargs '{"video":{"num_frames":512,"fps":1}}' \
    --video-pruning-rate 0.5 \
    --enable-auto-tool-choice \
    --tool-call-parser qwen3_coder \
    --reasoning-parser nemotron_v3
```

服务器启动并运行后，你可以用下面的代码片段发送多模态提示。

```
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:5000/v1", api_key="null")
resp = client.chat.completions.create(
    model="nemotron",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about GPUs."}
    ],
    temperature=1,
    max_tokens=1024,
)
print("Reasoning:", resp.choices[0].message.reasoning,
      "\nContent:", resp.choices[0].message.content)
```

想要更轻松的 vLLM 搭建方式，请参阅我们的入门 cookbook，见[这里](https://github.com/NVIDIA-NeMo/Nemotron/blob/main/usage-cookbook/Nemotron-3-Nano-Omni/vllm_cookbook.ipynb)，或使用 [NVIDIA Brev Launchable](https://brev.nvidia.com/launchable/deploy?launchableID=env-3Cm2gB9j5ROkCbiNKH5SQhERqBV)。

## 面向多模态智能体应用的高效率与领先精度

Nemotron 3 Nano Omni 为硬件高效推理而优化，可与 vLLM 等现代推理栈直接集成。它支持 FP8 与 NVFP4 量化、NVIDIA 优化的内核以及高效视频采样，在各类部署环境中提供精确、低延迟且可预测的推理。

通过把这些优化与基于 3D 卷积的时空处理相结合，Nemotron 3 Nano Omni 能以更低的算力成本维持高质量的多模态感知，从工作站到云规模系统都保持一致的精度与响应速度。

图 1 的性能评估在固定的交互性阈值下进行：保持每用户 token 速率恒定，测量在不降低实时用户体验的前提下，多文档与视频两个用例分别能维持多大的系统总吞吐量。这种方法突出的是在真实部署约束下——而不仅仅是峰值并发——不牺牲响应速度或质量的效率。

### 多文档与视频效率

![Pareto curves showing more efficient system capacity for multi-document and video use cases, showcasing a 7.4x and 9.2x higher throughput, respectively, for Nemotron 3 Nano Omni compared to an alternative open omni model.](https://vllm.ai/blog-assets/figures/2026-04-28-nemotron-omni/figure1.png)

帕累托曲线展示了多文档与视频用例下更高的系统容量效率：相比另一个开源 omni 模型，Nemotron 3 Nano Omni 的吞吐量分别高出 7.4x 和 9.2x。

图 1：在固定的每用户交互性阈值（tokens/sec/user）下各模型维持的系统总吞吐量。相比另一个开源 omni 模型，Nemotron 3 Nano Omni 在多文档与视频用例下的吞吐量分别高出 7.4x 和 9.2x。

### 多模态精度

![A chart showing accuracy improvements across various industry-leading benchmarks for the previous model version, Nemotron Nano VL V2, compared to the new Nemotron 3 Nano Omni model, highlighting high performance for complex document intelligence, and video and audio reasoning.](https://vllm.ai/blog-assets/figures/2026-04-28-nemotron-omni/figure2.png)

图表展示了上一代模型 Nemotron Nano VL V2 与新一代 Nemotron 3 Nano Omni 在多个业界领先基准上的精度提升，凸显其在复杂文档智能以及视频与音频推理上的高性能。

图 2：相比上一代 NVIDIA Nemotron Nano VL V2 模型，在业界领先基准上的多模态推理精度提升，凸显其在复杂文档智能以及视频与音频推理上的强劲表现。

如图 2 所示，Nemotron 3 Nano Omni 经历了持续的模型改进，在视觉、视频、OCR 和音频基准上比上一代 NVIDIA Nemotron Nano VL V2 取得更高的多模态精度。这些精度提升与领先效率相结合，使其在六个多模态排行榜上均名列前茅。

![An image showing Nemotron 3 Nano Omni winning six industry-leading leaderboards for multimodal efficiency and accuracy, including MMlongbench‑Doc, OCRBenchV2, WorldSense, DailyOmni, VoiceBench, and MediaPerf.](https://vllm.ai/blog-assets/figures/2026-04-28-nemotron-omni/figure3.png)

图片展示了 Nemotron 3 Nano Omni 在多模态效率与精度的六个业界领先排行榜上夺魁，包括 MMlongbench‑Doc、OCRBenchV2、WorldSense、DailyOmni、VoiceBench 与 MediaPerf。

图 3：Nemotron 3 Nano 在多模态效率与精度的六个排行榜上登顶。

该模型在 MMlongbench‑Doc、OCRBenchV2 等文档智能基准上表现一流，同时在 WorldSense、DailyOmni、VoiceBench 等视频与音频理解基准上同样领先。在 MediaPerf 基准上，Nemotron 3 Nano Omni 在每项任务上都取得了最高吞吐量，并在视频级打标（video-level tagging）上拥有最低的推理成本。

在一个多智能体系统中，Nemotron 3 Nano Omni 扮演多模态感知与上下文子智能体的角色，为智能体提供横跨屏幕、文档、音频流和视频的"眼睛"和"耳朵"，并把结构化理解输送给下游的编排与执行智能体。其轻量架构使它能够与系统中的其他模型高效并肩运行，而无需在各自独立的感知流水线之间重复计算。智能体需要看到和听到的一切，它都能处理。

这使 Nemotron 3 Nano Omni 成为驱动计算机使用智能体（computer use agent）、文档智能工作流和音视频理解流水线的有力选择——而且完全无需承担维护割裂多模态技术栈的开销。

## 快速开始

NVIDIA Nemotron 3 Nano Omni 是一个效率最高的开源多模态模型，驱动子智能体在视觉、音频和语言上更快地完成任务。凭借开放的权重、数据集与配方，你将获得完全的透明度，以及在自己的基础设施上（从工作站到云）微调和部署的灵活性。

准备好大规模运行多模态 AI 智能体了吗？

- 从 Hugging Face 下载模型权重——[BF16](https://huggingface.co/nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16)、[FP8](https://huggingface.co/nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-FP8)、[NVFP4](https://huggingface.co/nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-NVFP4)
- 使用[cookbook](https://github.com/NVIDIA-NeMo/Nemotron/blob/main/usage-cookbook/Nemotron-3-Nano-Omni/vllm_cookbook.ipynb)或通过 [Brev launchable](https://brev.nvidia.com/launchable/deploy?launchableID=env-3Cm2gB9j5ROkCbiNKH5SQhERqBV) 用 vLLM 运行推理
- 阅读 [Nemotron 3 Nano Omni 技术报告](https://research.nvidia.com/labs/adlr/files/NVIDIA-Nemotron-3-Omni-report.pdf)

订阅 [NVIDIA news](https://www.nvidia.com/en-us/preferences/email-signup/)，并在 [LinkedIn](https://www.linkedin.com/company/nvidia/)、[X](https://x.com/NVIDIAAI)、[YouTube](https://www.youtube.com/nvidia) 以及 [Discord](https://discord.gg/nvidia) 上的 Nemotron 频道关注 NVIDIA AI，随时获取 NVIDIA Nemotron 的最新动态。

## 致谢

感谢每一位为把 Nemotron 3 Nano Omni 带到 vLLM 做出贡献的人。

- **NVIDIA：** Nirmal Kumar Juluru、Anusha Pant
- **vLLM 团队与社区：** Roger Wang、Michael Goin、Thomas Parnell、Kevin Luu、Robert Shaw、Tyler Michael Smith
