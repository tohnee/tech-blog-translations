---
title: "在 vLLM 上使用 NVIDIA Nemotron 3 Nano 运行高效且精准的 AI 智能体"
title_en: "Run Highly Efficient and Accurate AI Agents with NVIDIA Nemotron 3 Nano on vLLM"
source: https://vllm.ai/blog/2025-12-15-run-nvidia-nemotron-3-nano
crawled: 2026-09-12
translated: 2026-09-13
---

# 在 vLLM 上使用 NVIDIA Nemotron 3 Nano 运行高效且精准的 AI 智能体

> 原文：[Run Highly Efficient and Accurate AI Agents with NVIDIA Nemotron 3 Nano on vLLM](https://vllm.ai/blog/2025-12-15-run-nvidia-nemotron-3-nano) · vLLM 博客

NVIDIA Nemotron 团队

[#模型支持](https://vllm.ai/blog/tags/model-support)

**1 月 28 日更新**：NVIDIA 刚刚发布了 NVFP4 精度的 Nemotron 3 Nano 模型。vLLM 开箱即支持该模型，它采用一种名为量化感知蒸馏（Quantization-Aware Distillation, QAD）的新方法，在 NVFP4 下保持精度的同时，相比 FP8-H100 在 B200 上提供 4x 的吞吐量。你可以从[这里](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4)下载 NVFP4 检查点，并使用这个 [NVIDIA Brev launchable](https://brev.nvidia.com/launchable/deploy?launchableID=env-386KFyCvmg3y22JIf0q8BUh6jia) 运行。

我们很高兴地发布由 vLLM 支持的 NVIDIA Nemotron 3 Nano。

Nemotron 3 Nano 隶属于新近发布的 Nemotron 3 系列——这是以领先精度构建智能体 AI 应用的最高效开源模型家族。Nemotron 3 系列模型采用混合 Mamba-Transformer MoE 架构和 1M token 上下文长度。这使开发者能够在复杂、多文档、长时间运行的操作中构建可靠、高吞吐的智能体。

Nemotron 3 Nano 是完全开放的：开放权重、数据集和配方，开发者可以在自己的基础设施上轻松定制、优化和部署该模型，以获得最大的隐私与安全。下图显示，在 Artificial Analysis 的开放性与智能指数中，Nemotron 3 Nano 位于最具吸引力的象限。

![](https://vllm.ai/blog-assets/figures/2025-12-15-run-nvidia-nemotron-3/figure_1.png)
图 1：NVIDIA Nemotron 3 为开源 AI 树立了新标准

Nemotron 3 Nano 在编程、推理和智能体任务上表现出色，并在 SWE Bench Verified、GPQA Diamond、AIME 2025、Arena Hard v2 和 IFBench 等基准上居于领先。

在本文中，我们将分享如何使用 vLLM 对 Nemotron 3 Nano 进行推理，从而大规模解锁高效的 AI 智能体。

## 关于 Nemotron 3 Nano

- 架构：
  - 采用混合 Transformer-Mamba 架构的混合专家（MoE）
  - 支持思考预算（Thinking Budget），以最少的推理 token 生成提供最优精度
- 精度
  - 在编程、科学推理、问题求解、数学、指令遵循、对话上精度领先
- 模型规模：30B，激活参数 3B
- 上下文长度：1M
- 模型输入：文本
- 模型输出：文本
- 支持的 GPU：NVIDIA RTX Pro 6000、DGX Spark、H100、B200。
- 快速开始：
  - 从 Hugging Face 下载模型权重 - [BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16)、[FP8](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-FP8)
  - [使用 vLLM 运行](https://brev.nvidia.com/launchable/deploy?launchableID=env-36ikINrMffBCbrtTVLr6MFcllcs)进行推理
  - [技术报告](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Nano-Technical-Report.pdf)，使用 Nemotron 技术构建定制、优化的模型。

## 使用 vLLM 运行优化的推理

Nemotron 3 Nano 借助 [BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16)、[FP8](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-FP8) 精度支持，实现加速[推理](https://www.nvidia.com/en-us/glossary/ai-inference/)，并在同一 GPU 上服务更多请求。按照以下说明开始：

`运行以下命令安装 vLLM。`

```
VLLM_USE_PRECOMPILED=1 pip install git+https://github.com/vllm-project/vllm.git@main
```

`然后我们就可以通过 OpenAI 兼容 API 来服务这个模型`

```
export VLLM_ATTENTION_BACKEND=FLASHINFER

# BF16
```bash
vllm serve --model "nvidia/NVIDIA-Nemotron-Nano-3-30B-A3B-BF16" \
    --dtype auto \
    --trust-remote-code \
    --served-model-name nemotron \
    --host 0.0.0.0 \
    --port 5000 \
    --enable-auto-tool-choice \
    --tool-call-parser qwen3_coder \
    --reasoning-parser deepseek_r1
```
OR
```bash
python -m vllm.entrypoints.openai.api_server \
    --model "nvidia/NVIDIA-Nemotron-Nano-3-30B-A3B-BF16" \
    --dtype auto \
    --trust-remote-code \
    --served-model-name nemotron \
    --host 0.0.0.0 \
    --port 5000 \
    --enable-auto-tool-choice \
    --tool-call-parser qwen3_coder \
    --reasoning-parser deepseek_r1
```


# Swap out model name for FP8
```bash
vllm serve --model "nvidia/NVIDIA-Nemotron-Nano-3-30B-A3B-FP8" \
    --dtype auto \
    --trust-remote-code \
    --served-model-name nemotron \
    --host 0.0.0.0 \
    --port 5000 \
    --enable-auto-tool-choice \
    --tool-call-parser qwen3_coder \
    --reasoning_parser deepseek_r1
```

```

`服务器启动并运行后，你可以使用下面的代码片段提示模型`

```
from openai import OpenAI
client = OpenAI(base_url="http://127.0.0.1:5000/v1", api_key="null")

# Simple chat completion
resp = client.chat.completions.create(
    model="nemotron",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about GPUs."}
    ],
    temperature=0.7,
    max_tokens=256,
)
print(resp.choices[0].message.reasoning_content, resp.choices[0].message.content)
```

如需更轻松地完成 vLLM 环境搭建，请参阅我们的入门 cookbook，见[这里](https://brev.nvidia.com/launchable/deploy?launchableID=env-36ikINrMffBCbrtTVLr6MFcllcs)。

## 面向智能体任务的高效率与领先精度

Nemotron 3 Nano 在 Nemotron Nano 2 模型的混合 Mamba-Transformer 架构基础上，用稀疏 MoE 层替换标准前馈网络（FFN）层，并用 Mamba-2 替换大部分注意力层。MoE 层帮助我们在仅一小部分激活参数量的情况下取得更好的精度。借助 MoE 架构，Nemotron 3 Nano 降低了计算需求，并满足了真实应用严苛的延迟要求。

凭借混合 Mamba-Transformer 架构，Nemotron 3 Nano 提供高达 4x 的 token 吞吐量，使模型能够更快地思考并同时提供更高的精度。「思考预算」特性防止模型过度思考，优化出更低、可预测的推理成本。

![](https://vllm.ai/blog-assets/figures/2025-12-15-run-nvidia-nemotron-3/figure_2.png)
图 2：Nemotron 3 Nano 在开放推理模型中提供更高吞吐量与领先精度

Nemotron 3 Nano 由 NVIDIA 精选的高质量数据训练而成，在 SWE Bench Verified、GPQA Diamond、AIME 2025、Arena Hard v2 和 IFBench 等基准上居于领先，在编程、[推理](https://www.nvidia.com/en-us/glossary/ai-reasoning/)、数学和指令遵循方面提供顶级精度。这使它成为构建面向金融、网络安全、软件开发和零售等各类企业用例的 AI 智能体的理想之选。

![](https://vllm.ai/blog-assets/figures/2025-12-15-run-nvidia-nemotron-3/figure_3.png)
图 3：在开放小规模推理模型中，Nemotron 3 Nano 在多个热门学术基准上提供领先精度

## 开始使用

总而言之，Nemotron 3 Nano 帮助各行业构建可扩展、高成本效益的智能体 AI 系统。借助开放权重、训练数据集和配方，开发者获得充分的透明度与灵活性，可以在从本地部署到云端的任何环境中微调和部署该模型，实现最大的安全与隐私。

准备好构建企业级智能体了吗？

- 从 Hugging Face 下载 Nemotron 3 Nano 模型权重 - [BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16)、[FP8](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-FP8)
- 使用[这份](https://brev.nvidia.com/launchable/deploy?launchableID=env-36ikINrMffBCbrtTVLr6MFcllcs) cookbook 用 vLLM 进行推理

[*分享你的想法*](http://nemotron.ideas.nvidia.com/?ncid=so-othe-692335)*，并对重要的方向投票，帮助塑造 Nemotron 的未来。*

*订阅 NVIDIA 新闻并关注 [LinkedIn](https://www.linkedin.com/showcase/nvidia-ai/posts/?feedView=all)、[X](https://x.com/NVIDIAAIDev)、[YouTube](https://www.youtube.com/@NVIDIADeveloper) 上的 NVIDIA AI*，*以及 [Discord](https://discord.com/invite/nvidiadeveloper) 上的 [Nemotron 频道](https://discord.com/channels/1019361803752456192/1407781691698708682)，随时了解 [NVIDIA Nemotron](https://developer.nvidia.com/nemotron) 的最新动态。*
