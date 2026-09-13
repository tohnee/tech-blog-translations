---
title: "在 vLLM 上用 NVIDIA Nemotron 运行多模态推理智能体"
title_en: "Run Multimodal Reasoning Agents with NVIDIA Nemotron on vLLM"
source: https://vllm.ai/blog/2025-10-31-run-multimodal-reasoning-agents-nvidia-nemotron
crawled: 2026-09-12
translated: 2026-09-13
---

# 在 vLLM 上用 NVIDIA Nemotron 运行多模态推理智能体

> 原文：[Run Multimodal Reasoning Agents with NVIDIA Nemotron on vLLM](https://vllm.ai/blog/2025-10-31-run-multimodal-reasoning-agents-nvidia-nemotron) · vLLM 博客

作者：NVIDIA Nemotron 团队

[#模型支持](https://vllm.ai/blog/tags/model-support)[#多模态](https://vllm.ai/blog/tags/multimodal)

我们很高兴地发布 [NVIDIA Nemotron Nano 2 VL](https://huggingface.co/nvidia/Nemotron-Nano-12B-v2-VL-BF16)，vLLM 已提供支持。这个开放的视觉语言模型（[VLM](https://www.nvidia.com/en-us/glossary/vision-language-models/)）专为视频理解与文档智能而构建。

Nemotron Nano 2 VL 采用混合 Transformer–Mamba 设计，在保持最先进多模态推理准确率的同时提供更高的吞吐量。该模型还具备 [**高效视频采样（Efficient Video Sampling，EVS）**](https://arxiv.org/abs/2510.14624)——一项新技术，可减少视频工作负载中冗余 [token](https://blogs.nvidia.com/blog/ai-tokens-explained/) 的生成，从而以更高效率处理更多视频。

在这篇博文中，我们将探讨 Nemotron Nano 2 VL 如何推进视频理解与文档智能，展示实际用例与基准测试结果，并指导你使用 vLLM 开始推理，解锁大规模高效的多模态 AI。

## 面向高效视频理解与文档智能的领先多模态模型

NVIDIA Nemotron Nano 2 VL 将视频理解与文档智能两种能力集成在一个高效模型中。它构建于混合 Transformer–Mamba 架构之上，结合了 Transformer 模型的推理能力与 Mamba 的计算效率，实现高吞吐、低延迟，能够更快地处理多图像输入。

[Nemotron Nano 2 VL](https://huggingface.co/blog/nvidia/nemotron-vlm-dataset-v2) 在 NVIDIA 精选的高质量多模态数据上训练，在 MMMU、MathVista、AI2D、OCRBench、OCRBench-v2、OCR-Reasoning、ChartQA、DocVQA、Video-MME 等视频理解与文档智能基准测试中处于领先地位，在多模态[推理](https://www.nvidia.com/en-us/glossary/ai-reasoning/)、字符识别、图表推理和视觉问答方面提供顶级准确率。这使它成为构建多模态应用的理想选择——能够以企业级精度自动完成跨视频、文档、表单和图表的数据提取与理解。

![](https://vllm.ai/blog-assets/figures/2025-multimodal-nvidia-nemotron/figure1.png)
图 1：Nemotron Nano 2 VL 在多个视频理解与文档智能基准测试上提供领先的准确率

### 用 EVS 提升效率

借助 EVS，模型在不牺牲准确率的情况下实现了更高的吞吐量和更快的响应时间。EVS 技术会剪除冗余帧，在保留语义丰富性的同时高效处理更长视频。因此，企业可以在几分钟内分析数小时的视频素材——从会议、培训到客服通话——以更低成本更快获得可执行的洞察。

![](https://vllm.ai/blog-assets/figures/2025-multimodal-nvidia-nemotron/figure2.png)
图 2：使用高效视频采样时，Nemotron Nano 2 VL 模型在不同 token 剪除阈值下于 Video-MME 和 LongVideo 基准上的准确率趋势

## 关于 Nemotron Nano 2 VL

- 架构：
  - 基于 [CRADIOH-V2](https://huggingface.co/nvidia/C-RADIOv2-H) 的视觉编码器
  - 以高效视频采样作为 token 压缩模块
  - 混合 Transformer-Mamba 架构——支持推理的 [Nemotron Nano 2 LLM](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2) 主干。
- 准确率：
  - 在 OCRBench v2 上准确率领先
  - 在以下基准测试中平均得分 74（当前顶级 VL 模型为 64.2）：MMMU、MathVista、AI2D、OCRBench、OCRBench-v2、OCR-Reasoning、ChartQA、DocVQA 和 Video-MME
- 模型规模：12B
- 上下文长度：128k
- 模型输入：多图像文档、视频、文本
- 模型输出：文本
- 上手使用：
  - 从 Hugging Face 下载模型权重——[BF16](https://huggingface.co/nvidia/Nemotron-Nano-12B-v2-VL-BF16)、[FP8](https://huggingface.co/nvidia/Nemotron-Nano-12B-v2-VL-FP8)、[FP4-QAD](https://huggingface.co/nvidia/Nemotron-Nano-12B-v2-VL-FP4-QAD)
  - 用 vLLM 运行推理
  - [技术报告](https://research.nvidia.com/labs/adlr/files/NVIDIA-Nemotron-Nano-V2-VL-report.pdf)：使用 Nemotron 技术构建定制化的优化模型。

## 使用 vLLM 运行优化推理

本指南演示如何在 vLLM 上运行 Nemotron Nano 2 VL，借助 BF16、FP8 和 FP4 精度支持实现加速[推理](https://www.nvidia.com/en-us/glossary/ai-inference/)并高效服务并发请求。

### 安装 vLLM

对 Nemotron Nano 2 VL 的支持已在 vLLM 的 nightly 版本中可用。运行以下命令安装 vLLM：

```
uv venv
source .venv/bin/activate
uv pip install vllm --extra-index-url https://wheels.vllm.ai/nightly --prerelease=allow
```

### 部署并查询推理服务器

运行以下命令，用 vLLM 分别以 BF16、FP8 和 FP4 精度部署 OpenAI 兼容的推理服务器：

```
vllm serve nvidia/Nemotron-Nano-12B-v2-VL-BF16 --trust-remote-code --dtype bfloat16 --video-pruning-rate 0

# FP8
vllm serve nvidia/Nemotron-Nano-VL-12B-V2-FP8 --trust-remote-code --quantization modelopt --video-pruning-rate 0

# FP4
vllm serve nvidia/Nemotron-Nano-VL-12B-V2-FP4-QAD --trust-remote-code --quantization modelopt_fp4 --video-pruning-rate 0
```

服务器启动并运行后，你可以使用下面的代码片段向模型发送提示：

```
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8000/v1", api_key="null")
# Simple chat completion
resp = client.chat.completions.create(
    model="nvidia/Nemotron-Nano-12B-v2-VL-BF16",
    messages=[
        {"role": "system", "content": "/no_think"},
        {"role": "user", "content": [
            {"type": "text", "text": "Give me 3 interesting facts about this image."},
            {"type": "image_url", "image_url": {"url": "https://blogs.nvidia.com/wp-content/uploads/2025/08/gamescom-g-assist-nv-blog-1280x680-1.jpg"}
            }
            ]},
    ],
    temperature=0.0,
    max_tokens=1024,
)
print(resp.choices[0].message.content)
```

更多示例请查看我们的 [vLLM cookbook](https://github.com/NVIDIA-NeMo/Nemotron/blob/main/usage-cookbook/Nemotron-Nano2-VL/vllm_cookbook.ipynb) 和 [Nemotron Nano 2 VL 的 vLLM recipe](https://docs.vllm.ai/projects/recipes/en/latest/NVIDIA/Nemotron-Nano-12B-v2-VL.html)。

[*分享你的想法*](http://nemotron.ideas.nvidia.com/?ncid=so-othe-692335)，*为你关心的事项投票，帮助塑造 Nemotron 的未来。*

*订阅 NVIDIA 新闻，并在 [LinkedIn](https://www.linkedin.com/showcase/nvidia-ai/posts/?feedView=all)、[X](https://x.com/NVIDIAAIDev)、[YouTube](https://www.youtube.com/@NVIDIADeveloper)*、*以及 [Discord](https://discord.com/invite/nvidiadeveloper) 上的 [Nemotron 频道](https://discord.com/channels/1019361803752456192/1407781691698708682)关注 NVIDIA AI，随时了解 [NVIDIA Nemotron](https://developer.nvidia.com/nemotron) 的最新动态。*
