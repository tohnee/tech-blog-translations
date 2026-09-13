---
title: "NVIDIA Nemotron 3.5 Lightning 在 vLLM 上的 Day-0 支持正式发布"
title_en: "Announcing Day-0 Support for NVIDIA Nemotron 3.5 Lightning on vLLM"
source: https://vllm.ai/blog/2026-08-10-nemotron-3-5-lightning-vllm
crawled: 2026-09-12
translated: 2026-09-13
---

# NVIDIA Nemotron 3.5 Lightning 在 vLLM 上的 Day-0 支持正式发布

> 原文：[Announcing Day-0 Support for NVIDIA Nemotron 3.5 Lightning on vLLM](https://vllm.ai/blog/2026-08-10-nemotron-3-5-lightning-vllm) · vLLM 博客

作者：NVIDIA Nemotron 团队与 vLLM 团队

[#模型支持](https://vllm.ai/blog/tags/model-support)

我们很高兴宣布 vLLM 对 NVIDIA Nemotron 3.5 Lightning 的 Day-0 支持。

Nemotron 3.5 Lightning 是一个可定制的开放模型，面向常驻（always-on）智能体：从本地运行的个人助手，到数据中心与云端的大规模智能体任务。它擅长编程、工具使用、指令遵循与多轮智能，并采用紧凑的混合专家（MoE）架构：总参数 300 亿，每次仅激活 30 亿参数。

该模型从 NVIDIA Nemotron 3 Ultra 蒸馏而来，并与 Nemotron Coalition 合作开发。现代智能体平台越来越多地把工作分配给多个模型：前沿模型负责困难的规划与编排，较小的模型处理频繁且边界清晰的操作步骤。Nemotron 3.5 Lightning 正是为第二种角色而生，同时不放弃真实智能体工作流所需的能力。

它满足常驻智能体的两项实际需求：

- **大规模下的快速执行：** 智能体系统的大部分时间往往花在完成大量小步骤上。Nemotron 3.5 Lightning 结合混合 MoE 设计（每个 token 激活 30B 参数中的 3B）与多 token 预测，以减少计算并加速生成。这些优化带来比同等规模开放模型最高 4x 的更高吞吐。
- **可定制的智能体智能：** 生产智能体需要理解组织专属术语、遵循政策、正确使用工具，并在多轮对话中维持上下文。Nemotron 3.5 Lightning 针对流行的智能体框架（agent harness）训练，且可继续后训练，适用于金融与风险自动化、网络安全调查、电信运营、零售体验以及本地个人助手等应用中的专门任务。

借助 vLLM，开发者可以通过 OpenAI 兼容 API 暴露该模型，并将其接入现有智能体框架、本地应用与企业自动化系统。

# TL;DR：关于 Nemotron 3.5 Lightning

- **架构：** 混合专家（MoE）架构
- **模型规模：** 总参数 30B，激活参数 3B
- **上下文长度：** 最高 100 万 token
- **模态：** 文本输入与文本输出
- **投机解码：** 多 token 预测、DFlash 与 DSpark
- **推理：** 可按请求启用或禁用推理，并支持可配置的推理 token 预算
- **训练：** 从 NVIDIA Nemotron 3 Ultra 蒸馏，并针对流行的智能体框架训练
- **定制：** 使用开放数据集训练的开放模型，支持在专门工作流上进行后训练
- **发布时可用格式：** BF16 与 NVFP4
- **部署目标：** NVIDIA DGX Spark、DGX Station、RTX PRO、RTX、NVIDIA Jetson、H100、H200、A100、L40S、B200/GB200 与 B300/GB300
- **开始使用：**
  - 从 Hugging Face 下载模型权重：[BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16) 与 [NVFP4](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4)。
  - 使用入门 [cookbook](https://github.com/NVIDIA-NeMo/Nemotron/blob/main/usage-cookbook/Nemotron-3.5-Lightning/vllm_cookbook.ipynb) 在 vLLM 上运行 Nemotron 3.5 Lightning。

# 用 vLLM 运行高吞吐推理

Nemotron 3.5 Lightning 旨在广泛的 NVIDIA 平台上运行。vLLM 提供把该模型引入生产工作流所需的服务层，包括连续批处理、前缀缓存、投机解码和 OpenAI 兼容 API。

BF16 检查点为部署提供了一个直接的基线。NVFP4 也在发布时提供，适用于能利用低精度推理的环境。

## 安装 vLLM

```
docker pull vllm/vllm-openai:v0.27.1

docker run --rm -it \
  --gpus all \
  --ipc=host \
  --network=host \
  --entrypoint /bin/bash \
  vllm/vllm-openai:v0.27.1
```

## 服务模型

此命令假设 1 x H100 配置。

```
vllm serve nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16 \
  --max-num-seqs 256 \
  --max-num-batched-tokens 32768 \
  --enable-prefix-caching \
  --async-scheduling \
  --mamba-backend flashinfer \
  --moe-backend humming \
  --linear-backend humming \
  --mamba-ssu-algorithm horizontal \
  --mamba-cache-mode align \
  --mamba-ssm-cache-dtype float16 \
  --enable-mamba-cache-stochastic-rounding \
  --mamba-cache-philox-rounds 5 \
  --reasoning-parser nemotron_v3 \
  --tool-call-parser qwen3_coder \
  --enable-auto-tool-choice \
  --host 0.0.0.0 \
  --port 8000
```

服务器运行后，应用可以通过 OpenAI 兼容客户端发送提示：

```
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="null",
)

response = client.chat.completions.create(
    model="nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Briefly explain: what is vLLM?"},
    ],
    temperature=1.0,
    top_p=0.95,
    max_tokens=1024,
)

choice = response.choices[0]
print("Reasoning:", choice.message.reasoning)
print("Content:", choice.message.content)
```

# 用投机解码加速长时间运行的智能体工作流

Nemotron 3.5 Lightning 支持三种投机解码技术：多 token 预测（MTP）、DFlash 与 DSpark。它们在加速 token 生成的同时保持目标模型的输出质量。

MTP 使用轻量的、集成在模型内的预测头来提出若干未来 token。DFlash 使用基于扩散的草稿模型并行生成整块候选 token。DSpark 增加了感知置信度的半自回归起草，在速度与 token 接受质量之间取得平衡。三者结合，让团队可以为自己的推理工作负载选择最佳的延迟、吞吐与部署权衡。

除权重与投机解码栈之外，Nemotron 3.5 Lightning 在架构上与 Nemotron 3 相同，因此大部分性能工作都落在了运行时本身。以下是我们向上游 vLLM 贡献的内容：

- **DSpark 集成：** 我们把 DSpark——一个融合自回归与扩散式起草的混合草稿模型——接入 vLLM 与 Nemotron 模型定义，让你在 MTP 与 DFlash 之外有了第三种草稿模型可选。
- **量化的 DSpark 草稿头：** 把草稿头量化到 W4A16，在不损害接受率的前提下降低其内存占用与每步延迟，这在 DGX Spark 这类内存受限的设备上尤为重要。
- **消除同步与异步调度：** 我们消除了起草-验证循环中的主机-设备同步，并启用异步调度，使当前批次仍在执行时就开始准备下一批次。
- **W4A16 的 MoE 与线性后端：** 我们把 vLLM 默认的 Marlin 后端替换为针对 Hopper 优化的 Humming 后端，对 Nemotron 的非门控 ReLU2 MoE 使用 W4A16 GEMM 内核——约值 20% 的吞吐——并把同一方案扩展到稠密线性层。
- **为 Mamba2 集成 ReplaySSM：** 我们为 Mamba2 状态空间层集成了 ReplaySSM，以降低混合架构循环路径中的每步开销。

对于低延迟服务，请在 H100、H200 与 DGX Spark 上使用 DSpark。就当前而言，若要最大吞吐，我们建议不启用投机解码运行。

## 多 token 预测（MTP）

Nemotron 3.5 Lightning 内置多 token 预测头。解码期间，这些头提出未来 token，由目标模型验证，从而减少较长响应所需的顺序生成步数。

vLLM 启动配置可以通过投机解码启用模型的 MTP 路径：

```
vllm serve --model nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 \
  --moe-backend marlin \
  --kv-cache-dtype fp8 \
  --max-num-batched-tokens 16384 \
  --enable-prefix-caching \
  --mamba-backend flashinfer \
  --mamba-cache-mode align \
  --reasoning-parser nemotron_v3 \
  --speculative_config.method mtp \
  --speculative_config.num_speculative_tokens 3 \
  --speculative_config.moe_backend flashinfer_cutlass \
  --tool-call-parser qwen3_coder \
  --enable-auto-tool-choice
```

## DFlash

DFlash 采取不同思路：它使用专用的扩散草稿模型提出一段线性 token 块，由目标模型并行验证。DFlash 需要兼容的草稿检查点，且与 MTP 分开配置。

```
vllm serve --model nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 \
  --moe-backend marlin \
  --kv-cache-dtype fp8 \
  --max-num-batched-tokens 16384 \
  --enable-prefix-caching \
  --speculative_config.num_speculative_tokens 3 \
  --mamba-backend flashinfer \
  --mamba-cache-mode align \
  --reasoning-parser nemotron_v3 \
  --speculative_config.model nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4-DFlash \
  --tool-call-parser qwen3_coder \
  --enable-auto-tool-choice
```

DFlash 草稿检查点：[nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4-DFlash](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4-DFlash)。

## DSpark

DSpark 是一个结合自回归与并行扩散式起草的混合草稿模型，介于 MTP 的完全自回归方法与 DFlash 的完全扩散方法之间，在 DGX Spark 上提供三者中最佳的性能。

```
vllm serve --model nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 \
  --moe-backend marlin \
  --kv-cache-dtype fp8 \
  --max-num-batched-tokens 16384 \
  --enable-prefix-caching \
  --speculative_config.num_speculative_tokens 3 \
  --mamba-backend flashinfer \
  --mamba-cache-mode align \
  --reasoning-parser nemotron_v3 \
  --speculative_config.model nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4-DSpark \
  --tool-call-parser qwen3_coder \
  --enable-auto-tool-choice
```

DSpark 草稿检查点：[nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4-DSpark](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4-DSpark)。

# 在 NVIDIA DGX Spark 上本地部署

如果你在 DGX Spark 上本地运行，以下配置可作为单用户本地开发的起点：

```
vllm serve --model nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 \
  --moe-backend marlin \
  --kv-cache-dtype fp8 \
  --trust-remote-code \
  --max-num-batched-tokens 16384 \
  --enable-prefix-caching \
  --compilation_config.cudagraph_capture_sizes '[1, 2, 4, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200, 208, 216, 224, 232, 240, 248, 256, 1024, 2048, 4096, 8192]' \
  --speculative_config.num_speculative_tokens 3 \
  --mamba-backend flashinfer \
  --mamba-ssm-cache-dtype float16 \
  --enable-mamba-cache-stochastic-rounding \
  --mamba-cache-philox-rounds 5 \
  --mamba-cache-mode align \
  --reasoning-parser nemotron_v3 \
  --speculative_config.method dspark \
  --speculative_config.model nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4-DSpark
```

![Pareto chart comparing inference performance of Nemotron 3.5 Lightning using various speculative decoding techniques on NVIDIA DGX Spark.](https://vllm.ai/blog-assets/figures/2026-nemotron-3-5-lightning/figure1-dgx-spark-pareto.png)

Pareto 图：在 NVIDIA DGX Spark 上比较 Nemotron 3.5 Lightning 使用不同投机解码技术的推理性能。

图 1：在 NVIDIA DGX Spark 上比较 Nemotron 3.5 Lightning 使用不同投机解码技术的推理性能的 Pareto 图。配置——前缀 32K，随后 10 轮 2k 输入与 1k 输出。

## 在 NVIDIA H100 上部署

如果你在 NVIDIA H100 上运行，以下配置可作为单用户本地开发的起点：

```
vllm serve --model nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 \
  --moe-backend humming \
  --linear-backend humming \
  --max-num-seqs 256 \
  --trust-remote-code \
  --max-num-batched-tokens 32768 \
  --enable-prefix-caching \
  --async-scheduling \
  --mamba-backend flashinfer \
  --mamba-ssm-cache-dtype float16 \
  --enable-mamba-cache-stochastic-rounding \
  --mamba-cache-philox-rounds 5 \
  --mamba-cache-mode align \
  --mamba-ssu-algorithm horizontal \
  --reasoning-parser nemotron_v3
```

![Pareto chart comparing inference performance of Nemotron 3.5 Lightning using various speculative decoding techniques on NVIDIA H100 GPUs.](https://vllm.ai/blog-assets/figures/2026-nemotron-3-5-lightning/figure2-h100-pareto.png)

Pareto 图：在 NVIDIA H100 GPU 上比较 Nemotron 3.5 Lightning 使用不同投机解码技术的推理性能。

图 2：在 NVIDIA H100 GPU 上比较 Nemotron 3.5 Lightning 使用不同投机解码技术的推理性能的 Pareto 图。配置——前缀 32K，随后 10 轮 2k 输入与 1k 输出。

# 在 NVIDIA Jetson 上本地部署

如果你在 NVIDIA Jetson 上本地运行，以下配置可作为单用户本地开发的起点：

```
vllm serve nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4 \
  --reasoning-parser nemotron_v3 \
  --kv-cache-dtype fp8 \
  --trust-remote-code \
  --max-num-batched-tokens 16384 \
  --enable-prefix-caching \
  --mamba-backend flashinfer \
  --mamba-ssm-cache-dtype float16 \
  --enable-mamba-cache-stochastic-rounding \
  --mamba-cache-philox-rounds 5 \
  --mamba-cache-mode align
```

# 专门智能体任务的领先精度与效率

Nemotron 3.5 Lightning 的设计目标是让专门化智能体既有能力又经济地运行。其混合 MoE 架构每个 token 仅激活 30B 参数中的 3B，多 token 预测则减少生成期间所需的顺序工作量。这些特性结合起来，带来比同等规模开放模型最高 4x 的更高吞吐。

Nemotron 3.5 Lightning 在智能体任务上提供领先的精度。通过从 Nemotron 3 Ultra 蒸馏能力，并在流行的智能体框架上训练，Nemotron 3.5 Lightning 在智能体生产力、编程、工具使用、指令遵循与长上下文推理等基准测试中表现强劲。

如图 3 所示，更高的推理吞吐与 token 效率把 Nemotron 3.5 Lightning 置于效率前沿之上，帮助常驻智能体更快完成大批量工作。

![Line chart comparing PinchBench accuracy with time to complete 10,000 tasks.](https://vllm.ai/blog-assets/figures/2026-nemotron-3-5-lightning/figure3-efficiency-frontier.png)

折线图：比较 PinchBench 精度与完成 10,000 个任务所需的时间。

图 3：Nemotron 3.5 Lightning 在精度相近的情况下完成智能体任务最多快 30%，领跑效率前沿。

# 总结

NVIDIA Nemotron 3.5 Lightning 把可定制的智能体智能带到本地系统、边缘、数据中心与云端。它结合了 30B 参数、激活 3B 参数的混合 MoE 架构、最高 100 万 token 的上下文窗口、可控推理，以及通过 MTP 或 DFlash 实现的投机生成。

借助 vLLM 的 Day-0 支持，开发者可以通过 OpenAI 兼容技术栈服务该模型，并将其集成到本地助手、智能体框架与专门的企业工作流中。

准备好用 Nemotron 3.5 Lightning 构建更快、更高效的智能体系统了吗？

- 从 Hugging Face 下载模型权重：[BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-BF16) 与 [NVFP4](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4)。
- 使用入门 [cookbook](https://github.com/NVIDIA-NeMo/Nemotron/blob/main/usage-cookbook/Nemotron-3.5-Lightning/vllm_cookbook.ipynb) 在 vLLM 上运行 Nemotron 3.5 Lightning。

*订阅 NVIDIA 新闻，并在 [LinkedIn](https://www.linkedin.com/showcase/nvidia-ai/posts/?feedView=all)、[X](https://x.com/NVIDIAAIDev)、[YouTube](https://www.youtube.com/@NVIDIADeveloper) 上关注 NVIDIA AI，以及在 [Discord](https://discord.com/invite/nvidiadeveloper) 上关注 [Nemotron 频道](https://discord.com/channels/1019361803752456192/1407781691698708682)，随时了解 [NVIDIA Nemotron](https://developer.nvidia.com/nemotron) 的最新动态。*

# 致谢

NVIDIA：Nirmal Kumar Juluru、Anusha Pant、Amir Klein、Faradawn Yang、Nave Assaf、Ryan Stewart、Alex Steiner、Bita Rouhani

# 常见问题

## 与 Nemotron 3 Nano 相比有什么新变化？

Nemotron 3 Nano 确立了一个高效的混合 Mamba-Transformer MoE 设计：总参数 30B、激活参数 3B、1M token 上下文窗口和可控推理。Nemotron 3.5 Lightning 在此基础上于四个重要方面更进一步：

- **前沿模型蒸馏：** Nemotron 3.5 Lightning 从 Nemotron 3 Ultra 蒸馏而来，把 NVIDIA 前沿智能体模型的能力迁移到小得多的部署占用中。
- **智能体框架优化：** Nemotron 3.5 Lightning 针对流行的智能体框架与多轮工作流训练，侧重编程、工具使用、指令遵循与专门任务完成。
- **投机解码：** Nemotron 3.5 Lightning 支持多 token 预测（MTP）、DFlash 与 DSpark，通过并行起草与验证多个 token 来加速生成。

最终成果是一个能在更短时间内更准确地完成更多智能体任务的模型。
