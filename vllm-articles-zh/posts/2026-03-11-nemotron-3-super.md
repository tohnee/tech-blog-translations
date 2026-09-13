---
title: "用 vLLM 运行 NVIDIA Nemotron 3 Super，实现高效精准的多智能体 AI"
title_en: "Run Highly Efficient and Accurate Multi-Agent AI with NVIDIA Nemotron 3 Super Using vLLM"
source: https://vllm.ai/blog/2026-03-11-nemotron-3-super
crawled: 2026-09-12
translated: 2026-09-13
---

# 用 vLLM 运行 NVIDIA Nemotron 3 Super，实现高效精准的多智能体 AI

> 原文：[Run Highly Efficient and Accurate Multi-Agent AI with NVIDIA Nemotron 3 Super Using vLLM](https://vllm.ai/blog/2026-03-11-nemotron-3-super) · vLLM 博客

作者：NVIDIA Nemotron 团队

[#模型支持](https://vllm.ai/blog/tags/model-support)

我们很高兴在 vLLM 上支持最新发布的 NVIDIA Nemotron 3 Super 模型。

Nemotron 3 Super 是 Nemotron 3 开放模型家族的一员，专为复杂的多智能体应用优化。如今的智能体 AI 系统依赖多个模型来规划、推理并执行复杂的多步骤任务。这些模型既要具备解决复杂技术难题所需的深度，又要具备大规模持续运行所需的效率。

Nemotron 3 Super 是一个开放的混合 Transformer-Mamba 架构混合专家（MoE）模型，总参数量达 1200 亿，推理时却只激活 120 亿。这一设计实现了高计算效率与领先的精度，尤其适合复杂的多智能体应用。它解决了大规模智能体系统的两大挑战：

- **"上下文爆炸"问题：** 多智能体系统常常因重复发送历史记录、工具输出和推理步骤而产生过多 token。Nemotron 3 Super 用 100 万 token 的超大上下文窗口解决这一问题，为智能体提供长期记忆，并显著减少目标漂移。
- **"思考税"：** 用传统超大模型运行推理密集的智能体可能又贵又慢。混合 MoE 架构提供高达 4x 的吞吐量提升，让复杂智能体在每个子任务上都不必承担高延迟与高成本，从而化解这项"税"。

![](https://vllm.ai/blog-assets/figures/2026-nemotron-3-super/figure1.png)
图 1：Artificial Analysis 图表，展示 Nemotron 3 Super 在热门开放模型的智能水平与开放程度对比中领先

如上图所示，Nemotron 3 Super 在 Artificial Analysis 开放程度指数上领先。与其他开放模型相比，Nemotron 完全开放：权重、数据集与配方（recipes）全部公开，开发者可以轻松地在自己的基础设施上定制、优化和部署，以获得最大的隐私与安全保障。

在这篇博文中，我们将分享如何用 vLLM 对 Nemotron 3 Super 进行推理，开启大规模、高效率、高精度的多智能体 AI。

## 关于 Nemotron 3 Super

- **架构：** 混合 Transformer-Mamba 架构的混合专家（MoE）
- 在同尺寸级别中拥有最高的吞吐效率，吞吐量比上一代 Nemotron Super 模型最高提升 5x
- **多 token 预测（MTP）：** 通过在单次前向传播中同时预测多个未来 token，MTP 大幅加速长文本生成
- 支持 **Thinking Budget**（思考预算），以最少的推理 token 生成获得最佳精度

**关键规格：**

- **精度：** 在同尺寸级别中于 Artificial Analysis 智能指数上精度领先；比上一代 Nemotron Super 模型精度最高提升 2x
- **潜在 MoE（Latent MoE）**能以仅调用 1 个专家的推理成本调用 4 个专家
- **模型规模：** 总参数 120B，激活参数 12B
- **上下文长度：** 最高 1M
- **模型输入/输出：** 文本进、文本出
- **支持的 GPU：** B200、H100、DGX Spark、RTX 6000

**开始使用：**

- 从 [Hugging Face](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16) 下载模型权重 —— BF16、FP8 与 NVFP4
- 用 vLLM 进行推理
- 阅读[技术报告](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Super-Technical-Report.pdf)了解更多细节

## 用 vLLM 运行优化后的推理

凭借 BF16、FP8 与 NVFP4 精度支持，Nemotron 3 Super 实现加速推理，并在同一块 GPU 上服务更多请求。Blackwell 上的 NVFP4 相比 H100 上的 FP8 可提供 4x 的更高吞吐量，同时保持精度。按照以下说明开始：

### 安装 vLLM

```
pip install vllm==0.17.1
```

### 服务模型

你可以通过 OpenAI 兼容 API 服务 Nemotron 3 Super。下面的命令按 4x H100 配置编写。如果你的硬件不同，请根据你的环境调整并行相关标志和设置。FP8 与 NVFP4 的详细说明请参考 cookbooks。

```
# BF16
vllm serve nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16 \
    --kv-cache-dtype fp8 \
    --tensor-parallel-size 4 \
    --trust-remote-code \
    --served-model-name nemotron \
    --enable-auto-tool-choice \
    --tool-call-parser qwen3_coder \
    --reasoning-parser nemotron_v3
```

服务器启动并运行后，你可以使用下面的代码片段向模型提问：

```
from openai import OpenAI
client = OpenAI(base_url="http://127.0.0.1:5000/v1", api_key="null")

# Simple chat completion
resp = client.chat.completions.create(
    model="nemotron",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Give me 3 bullet points about vLLM"}
    ],
    temperature=0.7,
    max_tokens=256,
)
print("Reasoning:", resp.choices[0].message.reasoning_content,
      "\nContent:", resp.choices[0].message.content)
```

想要更轻松的 vLLM 配置，请参阅我们的入门 cookbook（见[这里](https://github.com/anushapant/Nemotron/blob/main/usage-cookbook/Nemotron-3-Super/vllm_cookbook.ipynb)），或使用 [NVIDIA Brev launchable](https://brev.dev)。

## 面向多智能体应用的最高效率与领先精度

![](https://vllm.ai/blog-assets/figures/2026-nemotron-3-super/figure2.png)
图 2：Artificial Analysis 图表，展示 Nemotron 3 Super 与同规模热门开放模型相比在智能水平与效率上领先

如上图所示，该模型在 Artificial Analysis 基准测试中以更高效率取得领先精度，对于既需要效率又需要能力的多智能体系统来说是一个强有力的选择。

## 开始使用

Nemotron 3 Super 帮助你构建可扩展、高成本效益且高精度的多智能体 AI。借助开放的权重、数据集与配方，你可以获得完全的透明度，以及在工作站到云端的自有基础设施上微调和部署的灵活性。

准备好大规模运行多智能体 AI 了吗？

- 从 Hugging Face 下载 [Nemotron 3 Super 模型权重](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16) —— BF16、FP8 与 NVFP4
- 使用 [cookbook](https://github.com/anushapant/Nemotron/blob/main/usage-cookbook/Nemotron-3-Super/vllm_cookbook.ipynb) 并通过 [Brev launchable](https://brev.dev) 用 vLLM 进行推理
- 阅读 [Nemotron 3 Super 技术报告](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Super-Technical-Report.pdf)

订阅 [NVIDIA 新闻](https://www.nvidia.com/en-us/preferences/email-signup/)，在 [LinkedIn](https://www.linkedin.com/company/nvidia/)、[X](https://x.com/NVIDIAAI)、[YouTube](https://www.youtube.com/nvidia) 上关注 NVIDIA AI，并加入 [Discord](https://discord.gg/nvidia) 上的 Nemotron 频道，随时了解 NVIDIA Nemotron 的最新动态。

## 致谢

感谢所有为 Nemotron 3 Super 登陆 vLLM 做出贡献的人。

- **NVIDIA：** Nirmal Kumar Juluru、Anusha Pant
- **vLLM 团队与社区：** Roger Wang、Michael Goin、Thomas Parnell、Kevin Luu、Robert Shaw、Tyler Michael Smith
