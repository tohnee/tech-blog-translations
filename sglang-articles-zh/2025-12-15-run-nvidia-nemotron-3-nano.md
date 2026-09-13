---
title: "SGLang 为高效开放的 Nemotron 3 Nano 混合 MoE 模型提供 Day-0 支持"
title_en: "SGLang Adds Day-0 Support for the Highly Efficient, Open Nemotron 3 Nano Hybrid MoE Model"
author: "NVIDIA Nemotron Team"
date: "December 15, 2025"
previewImg: /images/blog/nemotron-3-nano/benchmark.png
source: https://lmsys.org/blog/2025-12-15-run-nvidia-nemotron-3-nano/
translated: 2026-09-12
---

# SGLang 为高效开放的 Nemotron 3 Nano 混合 MoE 模型提供 Day-0 支持

> 原文：[SGLang Adds Day-0 Support for the Highly Efficient, Open Nemotron 3 Nano Hybrid MoE Model](https://lmsys.org/blog/2025-12-15-run-nvidia-nemotron-3-nano/) · LMSYS Blog · NVIDIA Nemotron Team

**1 月 28 日更新**：NVIDIA 刚刚发布了 NVFP4 精度的 Nemotron 3 Nano 模型。SGLang 开箱即支持该模型；它采用一种名为量化感知蒸馏（Quantization-Aware Distillation，QAD）的新方法，在 NVFP4 精度下保持精度，同时在 B200 上相比 FP8-H100 提供 4 倍吞吐量。你可以从[这里](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4)下载 NVFP4 检查点，并通过这个 [NVIDIA Brev launchable](https://brev.nvidia.com/launchable/deploy?launchableID=env-386BHXsTBKROX8F2WBCbQP6S6qt) 运行。

我们很高兴地宣布，SGLang 已在首发日（Day 0）支持最新高效的 NVIDIA Nemotron 3 Nano 模型！

Nemotron 3 Nano 是新近发布的开放 [Nemotron 3 家族](https://developer.nvidia.com/blog/inside-nvidia-nemotron-3-techniques-tools-and-data-that-make-it-efficient-and-accurate/)的一员，是一个紧凑的 MoE 语言模型，提供业界领先的计算效率与精度，助力开发者构建专用的智能体 AI 系统。

Nemotron 3 Nano 完全开放，提供开放权重、数据集和训练配方（recipes），开发者可以轻松地在自己的基础设施上定制、优化和部署该模型，实现最大程度的隐私与安全。下图显示，Nemotron 3 Nano 在 Artificial Analysis 开放性-智能指数（Openness vs Intelligence Index）中处于最具吸引力的象限。


![figure1](/images/blog/nemotron-3-nano/artificial_analysis.png)<small><center>NVIDIA Nemotron 3 为开源 AI 树立新标准</center></small>

## TL;DR


- 架构：
    - 采用混合 Transformer-Mamba 架构的专家混合（MoE）模型
    - 支持思考预算（Thinking Budget），以最少的推理 token 生成提供最优精度
- 精度
    - 在编码、科学推理、数学和指令遵循上精度领先
- 模型规模：30B，激活参数 3.6B
- 上下文长度：1M
- 模型输入：文本
- 模型输出：文本
- 支持的 GPU：NVIDIA RTX Pro 6000、DGX Spark、H100、B200。
- 上手指南：
    - 从 Hugging Face 下载模型权重——[BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16)、[FP8](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-FP8)、[NVFP4](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4)
    - [使用 SGLang 运行推理](https://cookbook.sglang.io/docs/NVIDIA/Nemotron3-Nano)
    - [技术报告](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Nano-Technical-Report.pdf)，使用 Nemotron 技术构建自定义的优化模型。

## 安装与快速上手

如需更轻松地完成 SGLang 环境搭建，请参阅我们的入门 cookbook，可从[这里](https://cookbook.sglang.io/docs/NVIDIA/Nemotron3-Nano)获取，或通过 NVIDIA Brev [launchable](https://brev.nvidia.com/launchable/deploy?launchableID=env-36ikQZX0ZDTSCGE7YkqxiOKwKsj) 使用。

运行以下命令安装依赖：
```bash
uv pip install sglang==0.5.6.post3.dev1278+gad1b4e472 --extra-index-url https://sgl-project.github.io/whl/nightly/
```

然后即可启动该模型的服务：
```bash
# BF16
python3 -m sglang.launch_server --model-path nvidia/NVIDIA-Nemotron-Nano-3-30B-A3B-BF16 --trust-remote-code --reasoning-parser nano_v3 --tool-call-parser qwen3_coder

# FP8
python3 -m sglang.launch_server --model-path nvidia/NVIDIA-Nemotron-Nano-3-30B-A3B-FP8 --trust-remote-code --reasoning-parser nano_v3 --tool-call-parser qwen3_coder

# NVFP4
python3 -m sglang.launch_server --model-path nvidia/NVIDIA-Nemotron-Nano-3-30B-A3B-NVFP4 --trust-remote-code --reasoning-parser nano_v3 --tool-call-parser qwen3_coder
```

服务启动并运行后，即可使用以下代码片段向模型发起请求：

```python
from openai import OpenAI

# The model name we used when launching the server.
SERVED_MODEL_NAME = "nvidia/NVIDIA-Nemotron-Nano-3-30B-A3B-BF16"

BASE_URL = f"http://localhost:30000/v1"
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
print(resp.choices[0].message.reasoning_content, resp.choices[0].message.content)
```


## Nemotron 3 Nano：以领先精度为构建 AI 智能体提供最高效率

Nemotron 3 Nano 构建于混合 Mamba-Transformer 架构之上：用 MoE 层替换标准前馈网络（FFN）层，并用 Mamba-2 替换大部分注意力层。这使其仅用一小部分激活参数就实现了更高精度。借助 MoE，Nemotron 3 Nano 降低了计算需求，满足了真实世界部署所要求的严苛延迟约束。

Nemotron 3 Nano 的混合 Mamba-Transformer 架构将 token 吞吐量提升至最高 4 倍，让模型推理更快，同时精度更高。其「思考预算（thinking budget）」特性有助于避免不必要的计算，减少过度思考，确保更低且更可预测的推理成本。

![figure1](/images/blog/nemotron-3-nano/speed.png)<small><center>Nemotron 3 Nano 在开放推理模型中以领先精度实现更高吞吐量</center></small>


Nemotron 3 Nano 基于 NVIDIA 精选的高质量数据训练而成，在 SWE Bench Verified、GPQA Diamond、AIME 2025、Arena Hard v2 和 IFBench 等基准测试中领先，在编码、[推理](https://www.nvidia.com/en-us/glossary/ai-reasoning/)、数学和指令遵循方面达到顶级精度。这使其非常适合为金融、网络安全、软件开发和零售等各类企业用例构建 AI 智能体。

![figure1](/images/blog/nemotron-3-nano/benchmark.png)<small><center>Nemotron 3 Nano 在开放小型推理模型中于多个热门学术基准测试上精度领先</center></small>



## 上手指南

- 从 Hugging Face 下载 Nemotron 3 Nano 模型权重——[BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16)、[FP8](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-FP8)、[NVFP4](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4)
- 使用[这份](https://cookbook.sglang.io/docs/NVIDIA/Nemotron3-Nano) cookbook 或通过这个 NVIDIA Brev [launchable](https://brev.nvidia.com/launchable/deploy?launchableID=env-36ikQZX0ZDTSCGE7YkqxiOKwKsj) 运行 SGLang 推理。


## 延伸阅读
- [分享你的想法](http://nemotron.ideas.nvidia.com/?ncid=so-othe-692335)并为你关心的问题投票，帮助塑造 Nemotron 的未来。
- 订阅 NVIDIA 新闻，并在 [LinkedIn](https://www.linkedin.com/showcase/nvidia-ai/posts/?feedView=all)、[X](https://x.com/NVIDIAAIDev)、[YouTube](https://www.youtube.com/@NVIDIADeveloper) 以及 [Discord](https://discord.com/invite/nvidiadeveloper) 上的 [Nemotron 频道](https://discord.com/channels/1019361803752456192/1407781691698708682)关注 NVIDIA AI，随时了解 [NVIDIA Nemotron](https://developer.nvidia.com/nemotron) 的最新动态。


## 致谢

我们感谢所有贡献者为开发 Nemotron V3 Nano 并将其集成进 SGLang 所付出的努力。

**NVIDIA 团队**：Roi Koren, Max Xu, Netanel Haber, Tomer Bar Natan, Daniel Afrimi, Nirmal Kumar Juluru, Ann Guan 以及更多贡献者

**SGLang 团队与社区**：Baizhou Zhang, Jiajun Li, Ke Bao, Mingyi Lu, Richard Chen
