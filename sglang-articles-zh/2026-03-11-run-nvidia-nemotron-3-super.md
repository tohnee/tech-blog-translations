---
title: "SGLang 为 NVIDIA Nemotron 3 Super 提供 Day-0 支持，助力构建高效多智能体系统"
title_en: "SGLang Adds Day-0 Support for NVIDIA Nemotron 3 Super for building High-Efficiency Multi-Agent Systems"
author: "NVIDIA Nemotron Team"
date: "March 11, 2026"
previewImg: /images/blog/nemotron-3-super/figure_1.svg
source: https://lmsys.org/blog/2026-03-11-run-nvidia-nemotron-3-super/
translated: 2026-09-12
---

# SGLang 为 NVIDIA Nemotron 3 Super 提供 Day-0 支持，助力构建高效多智能体系统

> 原文：[SGLang Adds Day-0 Support for NVIDIA Nemotron 3 Super for building High-Efficiency Multi-Agent Systems](https://lmsys.org/blog/2026-03-11-run-nvidia-nemotron-3-super/) · LMSYS Blog · NVIDIA Nemotron Team

我们很高兴地宣布，SGLang 已在 Day 0（首发日）支持 NVIDIA Nemotron 3 Super。

[Nemotron 3 Super](https://developer.nvidia.com/blog/introducing-nemotron-3-super-an-open-hybrid-mamba-transformer-moe-for-agentic-reasoning/) 是 Nemotron 3 家族中领先的开放模型，专为让众多协作智能体共同运行而构建。串联规划、推理与工具调用的智能体系统所产生的 token 远多于单轮对话；而且它们还需要在每一步都具备强大的推理能力。

Nemotron 3 Super 是一个 120B 参数的混合专家（MoE）模型，每次前向传播仅激活 12B 参数，以极低的成本提供编程、工具调用与指令遵循方面的领先精度——并配备 1M token 上下文，让智能体在长工作流中始终掌握对话与规划状态。

![figure1](/images/blog/nemotron-3-super/figure_1.svg)<small><center>[Artificial Analysis](https://artificialanalysis.ai/) 图表：与同等规模的流行开放模型相比，Nemotron 3 Super 在智能水平与开放性上处于领先</center></small>

正如上图所示，Nemotron 3 Super 在 Artificial Analysis 开放性指数上处于领先。与其他开放模型相比，Nemotron 是完全开放的——开放权重、数据集与训练配方，开发者可以轻松地在自己的基础设施上进行定制、优化与部署，从而获得最大的隐私与安全保障。

本文将带领大家安装 SGLang，并用它部署 Nemotron 3 Super 进行推理。


## 关于 Nemotron 3 Super


- **架构**：采用混合 Transformer-Mamba 架构的专家混合（MoE）  
  - 在其规模级别中拥有最高的吞吐效率，相比上一代 Nemotron Super 模型（Llama Nemotron Super 1.5）吞吐量最高提升 5 倍
  - 多 token 预测（MTP）：通过在单次前向传播中同时预测多个未来 token，MTP 大幅加速长文本生成
  - 支持 Thinking Budget（思考预算），以最少的推理 token 生成获得最优精度
- **精度**：在其规模级别中，在 Artificial Analysis Intelligence Index 上精度领先
  - 在 Artificial Analysis Intelligence Index 上相比上一代 Nemotron Super 模型精度最高提升 2 倍。
  - 潜在 MoE（Latent MoE）使得可以以单个专家的推理成本调用 4 个专家
- **模型规模**：总参数 120B，激活参数 12B
- **上下文长度**：最高 1M
- **模型输入/输出**：文本输入，文本输出
- **支持的 GPU**：B200、H100、H200、DGX Spark、RTX 6000
- **快速上手**： 
    - 从 Hugging Face 下载模型权重——[BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16)、[FP8](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-FP8) 与 [NVFP4](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-NVFP4)
    - [使用 SGLang 进行推理](https://cookbook.sglang.io/autoregressive/NVIDIA/Nemotron3-Super)
    - [技术报告](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Super-Technical-Report.pdf)——了解如何运用 Nemotron 技术构建定制化、经过优化的模型。

## 安装与快速上手

为了更轻松地完成 SGLang 环境搭建，请参考我们的入门 cookbook，可在[此处](https://cookbook.sglang.io/autoregressive/NVIDIA/Nemotron3-Super)获取，或通过 NVIDIA Brev [launchable](https://brev.nvidia.com/launchable/deploy?launchableID=env-39d03Y3mDAiGuIrnHKmZwv0tA4s) 一键启动。

运行以下命令安装依赖：
```bash
pip install 'git+https://github.com/sgl-project/sglang.git#subdirectory=python'
```

随后即可部署该模型。以下命令针对 4×H200 配置，详细说明请参考 cookbook。
```bash
# BF16
```bash
python3 -m sglang.launch_server \
  --model-path nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16 \
  --host 0.0.0.0 \
  --port 5000 \
  --trust-remote-code \
  --tp 4 \
  --tool-call-parser qwen3_coder \
  --reasoning-parser nemotron_3
```

服务器启动并运行后，你可以使用以下代码片段调用模型：

```python
from openai import OpenAI

# The model name we used when launching the server.
SERVED_MODEL_NAME = "nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16"

BASE_URL = f"http://localhost:5000/v1"
API_KEY = "EMPTY"  # SGLang server doesn't require an API key by default

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

resp = client.chat.completions.create(
    model=SERVED_MODEL_NAME,
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Give me 3 bullet points about SGLang."}
    ],
    temperature=0.6,
    max_tokens=512,
)
print("Reasoning:", resp.choices[0].message.reasoning_content, "\nContent:", resp.choices[0].message.content)
```


## Nemotron 3 Super 非常适合多智能体与推理负载

![figure2](/images/blog/nemotron-3-super/figure_2.svg)<small><center>[Artificial Analysis](https://artificialanalysis.ai/) 图表：与同等规模的流行开放模型相比，Nemotron 3 Super 在智能水平与效率上处于领先</center></small>

如上图所示，该模型在 Artificial Analysis 基准测试中以更高的效率取得了领先的精度，这使其成为兼顾效率与能力的多智能体系统的有力选择。

1M token 上下文专为长周期智能体工作而设计：智能体可以在上下文中保留完整的对话历史与规划状态，RAG 流水线也能一次性提供大规模文档集。这减少了多步工作流中的信息碎片化与目标漂移。

综上，Super 成为在单节点上编排与运行大量智能体的有力选择——从代码生成与调试，到研究摘要、告警分诊与文档分析。

## 开始使用

Nemotron 3 Super 帮助你以高精度构建可扩展、高性价比的多智能体 AI。凭借开放权重、数据集与训练配方，你将获得完全的透明度，以及在自己的基础设施上微调与部署的灵活性——从工作站到云端皆可。

准备好大规模运行多智能体 AI 了吗？
- 从 Hugging Face 下载 Nemotron 3 Super 模型权重——[BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16)、[FP8](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-FP8) 与 [NVFP4](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-NVFP4)
- 使用 [cookbook](https://cookbook.sglang.io/autoregressive/NVIDIA/Nemotron3-Super) 并通过 [Brev launchable](https://brev.nvidia.com/launchable/deploy?launchableID=env-39d03Y3mDAiGuIrnHKmZwv0tA4s) 以 SGLang 进行推理
- 阅读 Nemotron 3 Super [技术报告](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Super-Technical-Report.pdf)

## 致谢
感谢每一位为 Nemotron 3 Super 落地 SGLang 做出贡献的人。

**NVIDIA**：Nirmal Kumar Juluru、Anusha Pant、Max Xu、Daniel Afrimi、Shahar Mor、Roi Koren、Ann Guan 等众多成员
**SGLang 团队与社区**：Baizhou Zhang、Jiajun Li、Ke Bao、Lingyan Hao、Mingyi Lu
