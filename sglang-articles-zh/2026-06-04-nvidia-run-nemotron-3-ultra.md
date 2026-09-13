---
title: "SGLang 与 Miles 为 NVIDIA Nemotron 3 Ultra 提供 Day-0 支持，面向长时运行自主智能体"
title_en: "SGLang and Miles Add Day-0 Support for NVIDIA Nemotron 3 Ultra for Long-Running Autonomous Agents"
author: "NVIDIA Nemotron Team and SGLang & Miles Team"
date: "June 4, 2026"
previewImg: /images/blog/nemotron-3-ultra/image1.png
type: blog
source: https://lmsys.org/blog/2026-06-04-nvidia-run-nemotron-3-ultra/
translated: 2026-09-12
---

# SGLang 与 Miles 为 NVIDIA Nemotron 3 Ultra 提供 Day-0 支持，面向长时运行自主智能体

> 原文：[SGLang and Miles Add Day-0 Support for NVIDIA Nemotron 3 Ultra for Long-Running Autonomous Agents](https://lmsys.org/blog/2026-06-04-nvidia-run-nemotron-3-ultra/) · LMSYS Blog · NVIDIA Nemotron Team and SGLang & Miles Team

![](/images/blog/nemotron-3-ultra/image1.png)

我们很高兴地宣布：SGLang 与 Miles 已在发布首日（Day 0）支持 NVIDIA Nemotron 3 Ultra。

智能体 AI 系统正在从短促的"提示词-响应"式交互，转向持久的工作流：它们能够规划、调用工具、检查结果、从故障中恢复，并在漫长任务周期中持续工作。这类智能体需要在同一套部署栈中同时具备强大的推理能力、高速推理、长上下文理解与可靠的工具调用。

[Nemotron 3 Ultra](https://blogs.nvidia.com/blog/nvidia-gtc-taipei-computex-2026-news/#nemotron-3-ultra) 正是为这类工作负载而生。

Nemotron 3 Ultra 属于 Nemotron 开源模型家族，是一个面向长时运行自主智能体的开放前沿推理模型。它针对编码、深度研究、企业工作流以及 EDA 等场景中的复杂编排进行了优化——在这些场景中，智能体必须在大量步骤和超大上下文窗口中保持持续推理。

借助 SGLang，开发者可以通过高性能推理栈部署 Nemotron 3 Ultra，并将其集成到智能体框架、编程系统、研究流水线和企业自动化工作流中。

## TL;DR：Nemotron 3 Ultra 简介

* **架构：** 采用混合 Transformer-Mamba 架构的专家混合（MoE）模型
  * 模型规模：总参数量 550B，激活参数量 55B
  * 上下文长度：最高 1M token
  * 模态：文本输入、文本输出
* **效率：** 支持 NVFP4 与 BF16 的高吞吐量推理。NVFP4 检查点可在 Blackwell GPU 上运行。
* **推理：** 针对长时运行自主智能体、工具调用、编码、深度研究和编排进行优化
* **训练：** 通过多环境强化学习（RL）后训练，获得稳健的推理与智能体行为
* **部署：** 开放权重、开放数据、开放配方，支持跨基础设施的定制与部署
* **支持的 GPU：**
  * BF16：8x GB200/GB300/B200/B300，16x H100，16x H200
  * NVFP4：2x GB200/GB300/B200
* **快速开始**
  * 从 Hugging Face 下载模型权重：[BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16)、[NVFP4](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-NVFP4)
  * 使用 SGLang，按照入门 [cookbook](https://docs.sglang.io/cookbook/autoregressive/NVIDIA/Nemotron3-Ultra) 运行推理
  * 阅读 [Nemotron 3 Ultra 技术报告](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Ultra-Technical-Report.pdf)，了解架构、训练与基准测试细节

## 安装与快速上手

如需更便捷地完成 SGLang 环境搭建，请参考 Nemotron 3 Ultra 入门 [cookbook](https://docs.sglang.io/cookbook/autoregressive/NVIDIA/Nemotron3-Ultra)，或使用 NVIDIA Brev 为 NVFP4 提供的 [launchable](https://brev.nvidia.com/launchable/deploy?launchableID=env-3EPQszEEuDqceuEswhpqhZRrd1M)。

启动 SGLang Docker 容器：

```py
docker run --rm -it \
  --gpus all \
  --cap-add SYS_NICE \
  --ipc=host \
  --network=host \
  --shm-size=16g \
  --ulimit memlock=-1 \
  --ulimit stack=67108864 \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -e SAFETENSORS_FAST_GPU=1 \
  -e NVIDIA_TF32_OVERRIDE=1 \
  -e SGLANG_DISABLE_DEEP_GEMM=1 \
  --entrypoint /bin/bash \
lmsysorg/sglang:dev-nemotron3-ultra
```

### 部署模型：

以下命令针对 8x B200 配置编写。如果你的硬件不同，请根据你的环境调整并行相关的 flag 及相关设置。

```py

python3 -m sglang.launch_server \
  --model-path nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-NVFP4 \
  --host 0.0.0.0 \
  --port 8000 \
  --served-model-name nemotron-3-ultra \
  --trust-remote-code \
  --tensor-parallel-size 8 \
  --reasoning-parser nemotron_3 \
  --tool-call-parser qwen3_coder

```

服务器启动后，即可使用兼容 OpenAI 的客户端发送请求：

```py
from openai import OpenAI

# Set this to the model you launched the server with
client = OpenAI(base_url="http://localhost:8000/v1", api_key="EMPTY")

resp = client.chat.completions.create(
    model="nemotron-3-ultra",
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Give me 3 bullet points about SGLang."}
    ],
    temperature=1.0,
    top_p=0.95,
    max_tokens=512,
)
print("Reasoning:", resp.choices[0].message.reasoning_content)
print("Content:", resp.choices[0].message.content)
```

## Nemotron 3 Ultra 为长周期智能体工作负载而构建

Nemotron 3 Ultra 完全开放，并从设计上即可与主流智能体框架和编排平台集成。它专为需要在大量步骤中持续推理的智能体系统而优化。为缓解高容量推理模型常见的效率-精度权衡，Nemotron 模型引入了多项深层次的架构创新：

* **面向智能体执行框架（agent harness）的后训练：** Nemotron 模型使用 NVIDIA [NeMo RL](https://github.com/nvidia-nemo/rl) 和 [Gym](https://github.com/NVIDIA-NeMo/gym)，在多种智能体执行框架上进行后训练。它们针对主流开放智能体执行框架进行了优化，而不仅限于单轮对话，并特别针对以下场景调优：智能体在其中进行规划、调用工具、读取观察结果、委派子智能体、校验输出，并在多轮交互中从错误中恢复。
* **混合 Mamba-Transformer：** Mamba 层提升了长上下文工作负载的序列处理效率，而 Transformer 层则在智能体需要从超大上下文窗口中检索特定事实时保留精确的记忆召回能力。
* **潜在 MoE（Latent MoE）：** 潜在 MoE 支持更高效的专家路由，帮助模型处理横跨推理、代码生成、工具调用和领域专属逻辑的工作流。
* **多 token 预测（MTP）：** MTP 通过在单次前向传播中预测多个未来 token 来缩短生成时间，提升长输出和多轮工作流的吞吐量。
* **NVFP4 精度：** 同一个 NVFP4 检查点可同时运行在 NVIDIA Hopper 和 Blackwell GPU 上。得益于专门优化的 NVFP4 量化内核，开发者可以在两种架构上无缝使用同一份检查点。

### 高吞吐量与强推理精度兼得

当模型能够在更短时间内完成更多轮推理时，长时运行智能体将直接受益。Nemotron 3 Ultra 融合了混合 Transformer-Mamba MoE 架构、长上下文支持以及 NVIDIA 优化的精度格式，为高要求的智能体工作负载提供快速而强大的推理能力。

这使得 Nemotron 3 Ultra 非常适合生产级智能体系统——在这类系统中，速度、推理质量与部署灵活性都至关重要。如图 1 和图 2 所示，Nemotron 3 Ultra 在智能体生产力、指令遵循和长上下文任务上准确率领先，且相比其他领先模型最多可节省 30% 的成本。

![](/images/blog/nemotron-3-ultra/image2.png)

图 1：在智能体生产力、编程和指令遵循等智能体基准测试中，Nemotron 3 Ultra 在开放模型中处于领先。

替代文本：一张表格图片，显示 Nemotron 3 Ultra 在智能体生产力、编程和指令遵循等智能体基准测试中于开放模型中处于领先。

![](/images/blog/nemotron-3-ultra/image3.png)

图 2：Nemotron 3 Ultra 最多可节省 30% 的成本，并处于成本效率前沿的领先位置。

替代文本：图片显示 Nemotron 3 Ultra 最多可节省 30% 的成本，并处于成本效率前沿的领先位置。

## 强化学习——Miles 支持

借助 Miles 框架，我们在 128 块 H200 GPU 上以共置（colocate）模式（训练与 SGLang rollout 共享 GPU）实现了 Nemotron 3 Ultra 的 GRPO 强化学习训练，并在 dapo-math-17k 上完成验证，全程仅需一个可复现的 Docker 镜像和启动脚本。

### Miles 支持的能力

**并行策略。** Miles 使用 Megatron 的多组并行维度训练 Nemotron 3 Ultra：TP、PP、EP 和 DP。

**面向 Mamba 混合 MoE 的 DP 注意力。** Mamba 的约束将张量并行切分上限限制为 8（由 n\_groups=8 决定），因此纯 TP 推理引擎的最大引擎规模被限制在 8 块 GPU。DP 注意力解除了这一限制：让注意力（以及 Mamba）在数据并行而非张量并行下运行，每个 SGLang 引擎即可将专家并行与 DP 注意力相结合，扩展到任意 rollout 规模，从而实现大规模 EP。

**经过验证的 RL 流水线。** 完整的 GRPO 循环基于 *deepscaler* 规则奖励端到端运行；在 dapo-math-17k 上，rollout 与训练的 logprob 保持接近（约 0.01），我们将其视为流水线符合 on-policy 行为的早期信号。这些只是短时间的调通（bring-up）运行，因此我们将其作为健全性检查结果报告，而非收敛后的结果。

**训练结果。** 以下结果来自在 128 块 H200 GPU（16×8）上以共置模式进行的 dapo-math-17k 实验。训练使用 TP8 · PP4 · EP32，搭配 DP4，并将优化器卸载到 CPU；rollout 使用 4 个 32 GPU 的 SGLang 引擎（ep\_size=32、dp\_size=4、enable\_dp\_attention），n\_samples=8，最大响应长度为 8192。检查点先离线一次性从 HF 格式转换为 Megatron torch\_dist 格式，模型在 Megatron 中通过 \--load 原生加载，\--hf-checkpoint 仅用于分词器和 SGLang。GRPO 运行

* **On-policy 程度。** RL 流水线的一项关键健康检查，是生成 rollout 所用的策略是否与训练中被更新的策略相匹配。一旦两者逐渐偏离，梯度就不再反映模型实际采样的数据，训练也会变得 off-policy 且不稳定。我们通过 train\_rollout\_logprob\_abs\_diff 来跟踪这一点，即 SGLang 与 Megatron 对每个 token 给出的 log 概率之间的平均绝对差。整个运行过程中，该值始终保持在 0.01 左右——如此小的差距表明 rollout 与训练策略保持高度一致，流水线行为符合 on-policy。

<img src="/images/blog/nemotron-3-ultra/image4.png" style="display:block; margin-left: auto; margin-right: auto; width: 60%"></img>

*图：完整运行过程中的 train\_rollout\_logprob\_abs\_diff；数值带始终保持在 0.01 左右。*

* **奖励曲线。** 随着训练推进，模型应当学会产出在奖励函数下得分更高的答案。我们跟踪 rollout/raw\_reward，即模型采样响应的平均奖励。在 30 个 rollout 步内，奖励随运行稳步增长。

<img src="/images/blog/nemotron-3-ultra/image5.png" style="display:block; margin-left: auto; margin-right: auto; width: 60%"></img>

*图：dapo-math-17k 在 8k 最大上下文长度下的 rollout/raw\_reward，随运行从 ~0.55 上升至 ~0.58。*

### Nemotron 3 Ultra RL 示例：

```shell
## Miles docker image for nemotron-3-ultra

docker pull radixark/miles:nemotron-3-ultra
cd /root/miles

## convert hf to dist

## env (optional): MODELS_DIR=/your/models

HF=$MODELS_DIR/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16
bash scripts/convert-nemotron-3-ultra-550b-hf-to-dist.sh <NODE_RANK 0..15> <HEAD_IP>

## Launch RL (128 GPU, colocate)

## head pod:
bash scripts/run-nemotron-3-ultra-550b-a55b.sh head   <HEAD_IP>

## each worker pod:
bash scripts/run-nemotron-3-ultra-550b-a55b.sh worker <HEAD_IP>

```

## 总结

NVIDIA Nemotron 3 Ultra 为长时运行自主智能体带来了高吞吐量的前沿推理能力。借助 SGLang 与 Miles 的 Day-0 支持，开发者可以快速部署或后训练该模型，并将其接入编程智能体、研究系统、企业自动化工作流以及领域专属的智能体技术栈。

准备好构建更快、更强大的智能体了吗？

* 从 Hugging Face 下载模型权重：[BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16)、[NVFP4](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-NVFP4)
* 使用 [cookbook](https://docs.sglang.io/cookbook/autoregressive/NVIDIA/Nemotron3-Ultra) 通过 SGLang 运行 Nemotron 3 Ultra
* 阅读 [Nemotron 3 Ultra 技术报告](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Ultra-Technical-Report.pdf)

*订阅 NVIDIA 新闻，并在 [LinkedIn](https://www.linkedin.com/showcase/nvidia-ai/posts/?feedView=all)、[X](https://x.com/NVIDIAAIDev)、[YouTube](https://www.youtube.com/@NVIDIADeveloper) 上关注 NVIDIA AI，同时加入 [Discord](https://discord.com/invite/nvidiadeveloper) 上的 [Nemotron 频道](https://discord.com/channels/1019361803752456192/1407781691698708682)，随时了解 [NVIDIA Nemotron](https://developer.nvidia.com/nemotron) 的最新动态。*

## 致谢

感谢每一位为 NVIDIA Nemotron 3 Ultra 落地 SGLang 与 Miles 做出贡献的同事。

NVIDIA：Nirmal Kumar Juluru, Anusha Pant, Ryan Stewart, Tomer Asida, Daniel Afrimi, Shaun Kotek, Roi Koren, Daniel Serebrenik, Amir Klein, Omer Ullman Argov, Netanel Haber, Amit Zuker, Shahar Mor, Tomer Bar Natan, Max Xu

SGLang & Miles 团队：Zhichen Zeng, Jiajun Li, Baizhou Zhang, Brayden Zhong, Cheng Wan, Yueming Yuan, Yuwei An, Banghua Zhu
