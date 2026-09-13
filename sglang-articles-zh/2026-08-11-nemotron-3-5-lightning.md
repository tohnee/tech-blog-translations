---
title: "SGLang 为 NVIDIA Nemotron 3.5 Lightning 提供 Day-0 支持"
title_en: "SGLang Adds Day-0 Support for NVIDIA Nemotron 3.5 Lightning"
author: "NVIDIA Nemotron Team and SGLang Team"
date: "August 11, 2026"
previewImg: /images/blog/nemotron-3-5-lightning/pinchbench-accuracy-vs-time.png
type: blog
source: https://lmsys.org/blog/2026-08-11-nemotron-3-5-lightning/
translated: 2026-09-12
---

# SGLang 为 NVIDIA Nemotron 3.5 Lightning 提供 Day-0 支持

> 原文：[SGLang Adds Day-0 Support for NVIDIA Nemotron 3.5 Lightning](https://lmsys.org/blog/2026-08-11-nemotron-3-5-lightning/) · LMSYS Blog · NVIDIA Nemotron Team and SGLang Team

SGLang 很高兴宣布为 NVIDIA Nemotron 3.5 Lightning 提供 Day-0 支持。这是一个可定制的开放模型，旨在为运行在本地设备、边缘、数据中心和云端的全天候运行（always-on）智能体提供动力。

全天候智能体需要在多步骤工作流中收集上下文、进行推理、调用工具并灵活应变。前沿模型负责处理复杂的编排，而更小的模型则高效应对大批量、专门化的任务。

Nemotron 3.5 Lightning 正是为处理这类大批量任务而生。它由 NVIDIA Nemotron 3 Ultra 蒸馏而来，并与 Nemotron Coalition 联合开发，在一个 300 亿参数的混合专家（MoE）模型中融合了出色的编码、工具调用、指令遵循与多轮对话能力，而每个时刻仅激活 30 亿参数。

Nemotron 3.5 Lightning 可以驱动本地个人助手、自动化金融与风险工作流、支持网络安全调查、优化电信运营，并改善零售体验。各组织可以针对自己的术语、政策、工具和工作流对它进行后训练并部署。

借助 SGLang，开发者可以通过高性能、OpenAI 兼容的推理栈来服务该模型，并将其接入智能体执行框架、本地助手和专门化的企业工作流。

## TL;DR：NVIDIA Nemotron 3.5 Lightning

* **架构：** 混合专家（MoE）架构
* **模型规模：** 总参数 30B，激活参数 3B
* **上下文长度：** 最高 100 万 token
* **投机解码：** 多 token 预测（MTP）、DFlash 与 DSpark
* **模态：** 文本输入、文本输出
* **训练：** 从 NVIDIA Nemotron 3 Ultra 蒸馏而来，并针对主流智能体执行框架进行训练
* **定制：** 使用开放数据集训练的开放模型，支持针对专门化工作流进行后训练
* **部署目标：** NVIDIA DGX Spark、DGX Station、RTX PRO、RTX、NVIDIA Jetson、H100、H200、A100、L40S、B200/GB200 以及 B300/GB300
* **发布时可用格式：** BF16、NVFP4
* **快速开始：**
  * 从 Hugging Face 下载模型权重：[BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16) 和 [NVFP4](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4)
  * 按照[入门 cookbook](https://docs.sglang.io/cookbook/autoregressive/NVIDIA/Nemotron3.5-Lightning) 使用 SGLang 运行 Nemotron 3.5 Lightning

## 安装与 SGLang 快速上手

SGLang 提供高性能的服务运行时、连续批处理、前缀缓存、投机解码以及 OpenAI 兼容 API。以下基线命令使用 BF16 检查点：

```py
docker run --rm -it \
  --gpus all \
  --cap-add SYS_NICE \
  --ipc=host \
  --network=host \
  --entrypoint /bin/bash \
  lmsysorg/sglang:dev-nemotron3-5-lightning
```

```py
sglang serve \
    --model-path nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16 \
    --mamba-backend flashinfer \
    --mamba-radix-cache-strategy extra_buffer \
    --reasoning-parser nemotron_3 \
    --tool-call-parser qwen3_coder
```

服务器启动后，使用任何 OpenAI 兼容客户端发送请求：

```py
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:30000/v1",
    api_key="EMPTY",
)

response = client.chat.completions.create(
    model="nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Briefly explain: what is SGLang?"},
    ],
    temperature=1.0,
    top_p=0.95,
    max_tokens=1024,
)
choice = response.choices[0]
print("Reasoning:", choice.message.reasoning_content)
print("Content:", choice.message.content)
```

## 用投机解码优化推理

Nemotron 3.5 Lightning 支持三种投机解码技术——多 token 预测（MTP）、DFlash 与 DSpark——在保持目标模型输出质量的同时加速 token 生成。

MTP 使用轻量的、集成在模型内部的预测头来提出多个未来 token；DFlash 使用基于扩散的草稿器（drafter）并行生成整个候选 token 块；DSpark 则引入置信度感知的半自回归草稿生成，在速度与 token 接受质量之间取得平衡。三者结合，团队可以根据自己的推理负载选择延迟、吞吐量与部署之间的最佳折中方案。

低延迟服务场景下，可在 H100、H200 和 DGX Spark 上使用 DSpark；就当前而言，如需最大吞吐量，我们建议不开启投机解码运行。

### 用 MTP 运行 Nemotron 3.5 Lightning

Nemotron 3.5 Lightning 内置多 token 预测。SGLang 通过其投机解码路径提供 MTP：模型内置的预测头负责草拟未来 token，再由目标模型进行验证。

SGLang 标准的 MTP 接口使用 EAGLE 投机算法。各硬件对应的确切命令请参阅 [cookbook](https://docs.sglang.io/cookbook/autoregressive/NVIDIA/Nemotron3.5-Lightning)。

### 用 DFlash 运行 Nemotron 3.5 Lightning

DFlash 使用专用的扩散草稿模型提出一段线性的 token 块，由目标模型并行验证。在 SGLang 中，DFlash 需要兼容的草稿检查点，且与 MTP 分开启用。

SGLang 的 DFlash 实现不支持数据并行注意力（DP attention），并且要求流水线并行大小为 1。当前参数参考请参阅 [SGLang 投机解码指南](https://docs.sglang.io)。

### 用 DSpark 运行 Nemotron 3.5 Lightning

DSpark 是一种混合投机解码方案，结合了自回归与并行扩散式草稿生成，介于 MTP 的完全自回归方式与 DFlash 的完全扩散方式之间，并且在三者之中于 DGX Spark 上表现最佳。

## 控制每个智能体步骤的推理

Nemotron 3.5 Lightning 支持开启或关闭推理（reasoning），让路由器或智能体执行框架可以对困难步骤使用更深入的推理，而对常规任务直接给出答案。

推理默认开启。若希望直接得到答案而不带推理轨迹，可通过 `chat_template_kwargs` 传入 `enable_thinking: false`：

```py
response = client.chat.completions.create(
    model="nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16",
    messages=[{"role": "user", "content": "Classify this ticket: billing or technical?"}],
    extra_body={"chat_template_kwargs": {"enable_thinking": False}},
)
```

对于开启推理的请求，可以省略 `chat_template_kwargs`（推理默认开启），也可以显式设置：

```py
response = client.chat.completions.create(
    model="nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16",
    messages=[{"role": "user", "content": "Plan the steps to migrate this service."}],
    extra_body={"chat_template_kwargs": {"enable_thinking": True}},
)
```

该模型还支持推理 token 预算。将 `thinking_budget`（通过 `custom_params`）与 `enable_thinking` 配合使用，即可按请求调整推理深度和响应时间：

```py
response = client.chat.completions.create(
    model="nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16",
    messages=[{"role": "user", "content": "Debug why this build is failing."}],
    extra_body={
        "chat_template_kwargs": {"enable_thinking": True},
        "custom_params": {"thinking_budget": 512},
    },
)
```

推理控制在多模型系统中尤其有用：编排器可以为规划、编码和模糊决策分配更大的预算，而对信息抽取、分类和结构化转换采用关闭推理的模式或较小的预算。

## 针对 Nemotron 3.5 Lightning 的推理优化

Nemotron 3.5 Lightning 在架构上与 Nemotron 3 完全相同，差异只在权重与投机解码栈，因此大部分性能优化工作都落在了运行时本身。以下是我们向上游 SGLang 贡献的内容：

* **DSpark 集成。** 我们将 DSpark——一种融合自回归与扩散式草稿生成的混合投机解码方案——接入 SGLang 与 Nemotron 模型定义，让你在 MTP 和 DFlash 之外又多了一种投机解码方案可选。
* **量化的 DSpark 草稿头。** 将草稿头量化到 W4A16，可以在不损失接受率的前提下削减其内存占用和单步延迟——这一点在 DGX Spark 这类内存受限的设备上最为关键。
* **消除同步与异步调度。** 我们消除了草拟-验证循环中的主机-设备同步，并启用了异步调度，使下一批任务在当前批次仍在执行时就能提前准备就绪。

## Nemotron 3.5 Lightning 为专门化 AI 提供领先的精度与效率

Nemotron 3.5 Lightning 将混合 MoE 架构——30B 参数中每个 token 仅激活 3B——与多 token 预测相结合，以减少计算量并加速生成。这些优化带来了最高 4 倍于同等规模开放模型的吞吐量，帮助智能体更快完成专门化任务。

Nemotron 3.5 Lightning 由 NVIDIA Nemotron 3 Ultra 蒸馏而来，并在主流智能体执行框架上训练，将前沿模型级别的智能体能力注入一个紧凑高效的模型。它在智能体生产力、编码、工具使用、指令遵循和长上下文推理等基准测试中均表现出色。

如图 1 所示，更高的推理吞吐量和 token 效率让 Nemotron 3.5 Lightning 位于效率前沿之上，帮助全天候智能体更快完成大批量工作。

![折线图：对比 PinchBench 精度与完成 10,000 个任务所需的时间。Nemotron 3.5 Lightning 以约快 30% 的速度达到与 Qwen3.6-35B 相当的精度，并显著领先于 Gemma 4 26B。](/images/blog/nemotron-3-5-lightning/pinchbench-accuracy-vs-time.png)

图 1：Nemotron 3.5 Lightning 领跑效率前沿——在相近精度下，完成智能体任务的速度最高快 30%。

## 总结

NVIDIA Nemotron 3.5 Lightning 为本地设备、边缘、数据中心和云端带来快速、可定制的智能体智能。借助 SGLang 的 Day-0 支持，开发者可以通过高性能、OpenAI 兼容的推理栈服务该模型；按智能体步骤控制推理；管理 DGX Spark 等本地部署的内存；并利用多 token 预测、DFlash 或 DSpark 加速生成。

对于在多个模型之间分发任务的系统而言，在精度、速度、开放性与部署控制都至关重要的高吞吐专门化任务上，Nemotron 3.5 Lightning 为开发者提供了一个极具吸引力的选择。

## 快速开始

* 从 Hugging Face 下载模型权重：[BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16) 与 [NVFP4](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4)
* 按照 [cookbook](https://docs.sglang.io/cookbook/autoregressive/NVIDIA/Nemotron3.5-Lightning) 使用 SGLang 运行 Nemotron 3.5 Lightning

*订阅 NVIDIA 新闻，并在 [LinkedIn](https://www.linkedin.com/showcase/nvidia-ai/posts/?feedView=all)、[X](https://x.com/NVIDIAAIDev)、[YouTube](https://www.youtube.com/@NVIDIADeveloper) 上关注 NVIDIA AI，以及加入 [Discord](https://discord.com/invite/nvidiadeveloper) 上的 [Nemotron 频道](https://discord.com/channels/1019361803752456192/1407781691698708682)，随时了解 [NVIDIA Nemotron](https://developer.nvidia.com/nemotron) 的最新动态。*

## 致谢

感谢每一位为 NVIDIA Nemotron 3.5 Lightning 落地 SGLang 做出贡献的人。

NVIDIA：Nirmal Kumar Juluru、Anusha Pant、Amir Klein、Faradawn Yang、Nave Assaf、Ryan Stewart、Alex Steiner、Bita Rouhani、Seong Hee Lee

SGLang 团队

## 常见问题（FAQ）

**与 Nemotron 3 Nano 相比有什么新变化？**

Nemotron 3 Nano 确立了高效的混合 Mamba-Transformer MoE 设计：总参数 30B、激活参数 3B、100 万 token 上下文窗口，以及可控推理。Nemotron 3.5 Lightning 在此基础上做出三项重要升级：

* **前沿模型蒸馏：** Nemotron 3.5 Lightning 从 Nemotron 3 Ultra 蒸馏而来，将 NVIDIA 前沿智能体模型的能力迁移到一个部署占用小得多的模型中。
* **智能体执行框架优化：** Nemotron 3.5 Lightning 针对主流智能体执行框架和多轮工作流进行训练，重点关注编码、工具使用、指令遵循和专门化任务的完成。
* **投机解码：** Nemotron 3.5 Lightning 支持多 token 预测（MTP）、DFlash 与 DSpark，通过并行草拟和验证多个 token 来加速生成。

最终得到的模型，能够用更少的时间、更准确地完成更多智能体任务。
