---
title: "宣布 vLLM 对 NVIDIA Nemotron 3 Ultra 的 Day-0 支持"
title_en: "Announcing Day-0 Support for NVIDIA Nemotron 3 Ultra on vLLM"
source: https://vllm.ai/blog/2026-06-04-nemotron-3-ultra-vllm
crawled: 2026-09-12
translated: 2026-09-13
---

# 宣布 vLLM 对 NVIDIA Nemotron 3 Ultra 的 Day-0 支持

> 原文：[Announcing Day-0 Support for NVIDIA Nemotron 3 Ultra on vLLM](https://vllm.ai/blog/2026-06-04-nemotron-3-ultra-vllm) · vLLM 博客

作者：NVIDIA Nemotron 团队

[#模型支持](https://vllm.ai/blog/tags/model-support)

![](https://vllm.ai/blog-assets/figures/2026-nemotron-3-ultra/hero.png)

我们很高兴地宣布：vLLM 现已对全新发布的 NVIDIA Nemotron 3 Ultra 提供 Day-0 支持。

[Nemotron 3 Ultra](https://blogs.nvidia.com/blog/nvidia-gtc-taipei-computex-2026-news/#nemotron-3-ultra) 是 Nemotron 开放模型家族的一员，为长期运行的自主智能体工作流中的前沿级推理而构建。它面向复杂编排、编码、深度研究、企业自动化，以及智能体必须规划、调用工具、从错误中恢复并在扩展上下文上进行推理的其他任务。

现代智能体系统越来越持久。它们不只是回答单个提示，而是搜索、写代码、跑测试、检查失败、协调工具、评估证据，并在漫长的任务视野中持续工作。这些工作流要求的模型既要能维持推理深度，又要让推理快到足以实际部署。

Nemotron 3 Ultra 满足高级智能体 AI 的两大主要需求：

**快速完成任务：**

长期运行的智能体需要的不仅是模型的原始智能。它们需要能在同样的时间预算内完成更多推理步骤的吞吐量。Nemotron 3 Ultra 结合混合 Transformer-Mamba MoE 架构、多 token 预测和 NVIDIA 优化的推理精度，为严苛的智能体工作负载提供高吞吐量。

**高级智能体推理：**

智能体工作流通常需要架构规划、多步调试、信源评估、合规审查或设计验证。Nemotron 3 Ultra 经过面向推理、工具使用和指令遵循的训练后优化，覆盖各类智能体环境，帮助智能体在不牺牲精度的情况下推进复杂任务。

借助这个模型，智能体系统可以更快地完成困难的推理工作流，同时在编码、工具调用、研究综合和企业自动化方面保持强劲表现。

vLLM 是 Nemotron 3 Ultra 训练工作流的关键组成部分，在整个训练过程中为 rollout 和模型评估提供高吞吐量多节点推理。在 NeMo RL 中，vLLM 作为强化学习 rollout 的生成后端，支持高效采样、可扩展推理，以及与 NeMo Gym 集成以构建多步与多轮训练环境。

Nemotron 团队还把 vLLM 用作评估循环的一部分，帮助我们跟踪进展、验证改进，并理解训练的每个阶段是否在把模型推向正确的方向。

# TL;DR：关于 Nemotron 3 Ultra

- **架构：** 混合 Transformer-Mamba 架构的混合专家（MoE）
  - 模型规模：总参数 550B，活跃参数 55B
  - 上下文长度：最高 1M token
  - 模态：文本输入、文本输出
- **效率：** 支持 NVFP4 与 BF16 的高吞吐量推理。NVFP4 检查点可在 Blackwell GPU 上运行。
- **推理：** 为长期运行的自主智能体、工具调用、编码、深度研究和编排而优化
- **训练：** 通过多环境强化学习进行训练后优化，获得稳健的推理与智能体行为
- **部署：** 开放权重、开放数据和开放配方，便于跨基础设施进行定制与部署
- **支持的 GPU：**
  - BF16：8x GB200/B200/GB300/B300、16x H100、8x H200
  - NVFP4：4x GB200/B200/GB300/B300、8x H100
- **开始使用**
  - 从 Hugging Face 下载模型权重 - [BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16)、[NVFP4](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-NVFP4)
  - 使用入门 [cookbook](https://github.com/NVIDIA-NeMo/Nemotron/blob/main/usage-cookbook/Nemotron-3-Ultra/vllm_cookbook.ipynb) 以 vLLM 运行推理
  - 阅读 [Nemotron 3 Ultra 技术报告](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Ultra-Technical-Report.pdf)了解架构、训练与基准测试细节

# 用 vLLM 运行优化的智能体推理

Nemotron 3 Ultra 面向跨 BF16 与 NVFP4 精度模式的高吞吐量智能体推理而设计。借助 vLLM，开发者可以通过 OpenAI 兼容 API 服务该模型，并将其集成到现有智能体框架、编码系统、研究管线和企业自动化工作流中。

要想更轻松地完成 vLLM 环境搭建，请参考 Nemotron 3 Ultra 入门 [cookbook](https://github.com/NVIDIA-NeMo/Nemotron/blob/main/usage-cookbook/Nemotron-3-Ultra/vllm_cookbook.ipynb)，或使用面向 NVFP4 的 NVIDIA Brev [launchable](https://brev.nvidia.com/launchable/deploy?launchableID=env-3EPQRUP8Sl27sxp1fMvXt3Lor8T)。

## 安装 vLLM

```
docker pull vllm/vllm-openai:v0.22.0

docker run --rm -it --gpus all --ipc=host --network=host \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  --entrypoint /bin/bash \
  vllm/vllm-openai:v0.22.0
```

## 服务模型

以下命令按 8x B200 配置。如果你的硬件不同，请根据你的环境调整并行标志和相关设置。

```
export VLLM_USE_FLASHINFER_MOE_FP4=1
export VLLM_MEMORY_PROFILER_ESTIMATE_CUDAGRAPHS=1

vllm serve nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-NVFP4 \
  --served-model-name nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B \
  --host 0.0.0.0 \
  --port 8000 \
  --trust-remote-code \
  --tensor-parallel-size 8 \
  --kv-cache-dtype fp8 \
  --max-num-seqs 16 \
  --max-model-len 262144 \
  --gpu-memory-utilization 0.90 \
  --max-num-batched-tokens 32768 \
  --enable-flashinfer-autotune \
  --async-scheduling \
  --speculative_config.method mtp \
  --speculative_config.num_speculative_tokens 5 \
  --mamba-backend triton \
  --mamba-ssm-cache-dtype float32 \
  --reasoning-parser nemotron_v3 \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_coder

```

服务器运行起来之后，使用 OpenAI 兼容客户端发送提示：

```
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8000/v1",
    api_key="EMPTY",
)

resp = client.chat.completions.create(
    model="nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Give me 3 bullet points about vLLM"},
    ],
    temperature=1.0,
    top_p=0.95,
    max_tokens=1024,
)

msg = resp.choices[0].message
print("Reasoning:", getattr(msg, "reasoning", None))
print("Content:", msg.content)
```

NVFP4 部署指南请参考 [Nemotron 3 Ultra vLLM cookbook](https://github.com/NVIDIA-NeMo/Nemotron/blob/main/usage-cookbook/Nemotron-3-Ultra/vllm_cookbook.ipynb)。

# 面向长期运行智能体的高吞吐量推理

Nemotron 3 Ultra 为需要跨越许多步骤持续推理的智能体系统而优化。

如图 1、图 2 和图 3 所示，Nemotron 3 Ultra 在智能体生产力、指令遵循和长上下文任务上精度领先，并提供领先的吞吐量，相比其他领先的开源模型节省 30% 成本。

![](https://vllm.ai/blog-assets/figures/2026-nemotron-3-ultra/figure1.svg)
图 1：在智能体生产力、编码和指令遵循的智能体基准测试上，Nemotron 3 Ultra 在开源模型中处于领先。

![](https://vllm.ai/blog-assets/figures/2026-nemotron-3-ultra/figure2.svg)
图 2：Nemotron 3 Ultra 位于最具吸引力的象限，在开源模型中精度与吞吐量双双领先。配置 - vLLM，10k/2k ISL/OSL，BS 1。

![](https://vllm.ai/blog-assets/figures/2026-nemotron-3-ultra/figure3.svg)
图 3：Nemotron 3 Ultra 成本节省最高达 30%，在成本效益前沿上处于领先位置。

为了缓解大容量推理模型典型的效率-精度权衡，Nemotron 模型引入了深刻的架构创新：

- **面向智能体框架（Agent Harness）的训练后优化：** Nemotron 模型使用 NVIDIA [NeMo RL](https://github.com/nvidia-nemo/rl) 和 [Gym](https://github.com/NVIDIA-NeMo/gym) 在众多智能体框架上进行训练后优化。它们面向领先的开放智能体框架进行优化，而不仅是单轮聊天，并专门针对智能体在多轮中规划、调用工具、读取观察结果、委派子智能体、验证输出和从错误中恢复的工作流进行了优化。
- **混合 Mamba-Transformer：** Mamba 层提升长上下文工作负载的序列效率，而 Transformer 层在智能体需要从大上下文窗口中检索具体事实时保持精确回忆。
- **潜在 MoE（Latent MoE）：** 潜在 MoE 支持更高效的专家路由，帮助模型处理跨越推理、代码生成、工具调用和领域专属逻辑的工作流。
- **多 token 预测（MTP）：** MTP 通过单次前向传播预测多个未来 token 来缩短生成时间，提升长输出与多轮工作负载的吞吐量。
- **NVFP4 精度：** 同一个 NVFP4 检查点可以在 NVIDIA Hopper 和 Blackwell GPU 上运行，借助专门的 NVFP4 量化内核，开发者可以在两种架构上无缝使用同一个检查点。

# 总结

NVIDIA Nemotron 3 Ultra 是一个面向长期运行自主智能体的开放前沿推理模型。它把高吞吐量推理、长上下文推理、工具使用能力和开放的部署灵活性结合在一起，服务于构建高级智能体 AI 系统的开发者与企业。

准备好构建更快、更强的智能体工作流了吗？

- 从 Hugging Face 下载模型权重 - [BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16)、[NVFP4](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-NVFP4)
- 使用 [cookbook](https://github.com/NVIDIA-NeMo/Nemotron/blob/main/usage-cookbook/Nemotron-3-Ultra/vllm_cookbook.ipynb) 以 vLLM 运行 Nemotron 3 Ultra
- 阅读 [Nemotron 3 Ultra 技术报告](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Ultra-Technical-Report.pdf)

*订阅 NVIDIA 新闻，并在 [LinkedIn](https://www.linkedin.com/showcase/nvidia-ai/posts/?feedView=all)、[X](https://x.com/NVIDIAAIDev)、[YouTube](https://www.youtube.com/@NVIDIADeveloper)*、*以及 [Discord](https://discord.com/invite/nvidiadeveloper) 上的 [Nemotron 频道](https://discord.com/channels/1019361803752456192/1407781691698708682)关注 [NVIDIA Nemotron](https://developer.nvidia.com/nemotron) 的最新动态。*

# 致谢

感谢所有为把 NVIDIA Nemotron 3 Ultra 带到 vLLM 做出贡献的人。

NVIDIA：Nirmal Kumar Juluru、Anusha Pant、Alex Steiner、Tomer Asida、Daniel Afrimi、Shaun Kotek、Roi Koren、Daniel Serebrenik、Amir Klein、Omer Ullman Argov、Netanel Haber、Amit Zuker、Shahar Mor、Tomer Bar Natan
vLLM 团队与社区：Michael Goin、Kaichao You、Yongye Zhu、Roger Wang、Simon Mo、Woosuk Kwon、Yasong Wang、Nick Hill、Zachary Xi
