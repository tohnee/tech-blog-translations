---
title: "DGX Spark 上的 vLLM：架构、配置与本地评估"
title_en: "vLLM on the DGX Spark: Architecture, Configuration, and Local Evaluation"
source: https://vllm.ai/blog/2026-06-01-vllm-dgx-spark
crawled: 2026-09-12
translated: 2026-09-13
---

# DGX Spark 上的 vLLM：架构、配置与本地评估

> 原文：[vLLM on the DGX Spark: Architecture, Configuration, and Local Evaluation](https://vllm.ai/blog/2026-06-01-vllm-dgx-spark) · vLLM 博客

作者：Inferact

[#dgx-spark](https://vllm.ai/blog/tags/dgx-spark)[#nemotron](https://vllm.ai/blog/tags/nemotron)[#硬件](https://vllm.ai/blog/tags/hardware)[#部署](https://vllm.ai/blog/tags/deployment)[#computex](https://vllm.ai/blog/tags/computex)

NVIDIA DGX Spark 是一台桌边型 GB10 系统，用于在本地运行大模型推理，弥合笔记本级开发与数据中心 GPU 服务之间的鸿沟。[vLLM](https://docs.vllm.ai/) 在 DGX Spark 上提供快速、高效的本地推理端点：它将 OpenAI 兼容 API 与在本地运行大型 NVFP4 模型所需的内存、批处理、KV 缓存和遥测控制组合在一起。本文讲解 vLLM 如何映射到 DGX Spark 架构：模型选择、运行时标志、统一内存行为、OpenAI 兼容服务、Prometheus 遥测，以及一次 Nemotron-3-Super 部署的本地评估结果。

![vLLM running Nemotron-3-Super on the DGX Spark for a demo at the Inferact office.](https://vllm.ai/blog-assets/figures/2026-05-26-vllm-dgx-spark/office-dgx-spark.jpg)

在 Inferact 办公室，vLLM 在 DGX Spark 上运行 Nemotron-3-Super 进行演示。

![Figure 1. vLLM example serving architecture on DGX Spark: client apps use /v1 and /metrics against a local official vLLM image.](https://vllm.ai/blog-assets/figures/2026-05-26-vllm-dgx-spark/dgx-spark-vllm-serving-architecture.svg)

图 1. DGX Spark 上的 vLLM 示例服务架构：客户端应用对本地运行的官方 vLLM 镜像使用 /v1 与 /metrics。

## 技术摘要

- **vLLM 在 DGX Spark 上提供快速、高效的本地推理端点。** 它将 OpenAI 兼容 API 与在本地运行大型 NVFP4 模型所需的内存、批处理、KV 缓存和遥测控制组合在一起。当前的 Nemotron-3-Super DGX Spark 配方使用 vLLM 的[官方 OpenAI 兼容服务器镜像](https://docs.vllm.ai/en/latest/deployment/docker/)，配合 DGX Spark 专属的运行时标志，为开发者提供一条从模型下载到本地服务的经过测试的路径。
- **DGX Spark 架构决定了服务配置。** `sm_121` 消费级 Blackwell 芯片、统一的 CPU+GPU 内存池，以及 Spark 的内存带宽，使连续批处理、分页 KV 缓存、NVFP4 内核和 Prometheus 遥测格外值得关注。
- **vLLM 运行时标志应与 DGX Spark 的统一内存特性相匹配。** Spark 的 CPU、GPU、操作系统、容器运行时、模型权重和 KV 缓存共享同一个 128 GB 内存池，因此服务标志需要为系统的其余部分留出空间。`--gpu-memory-utilization` 应在统一内存池中为操作系统、容器运行时和 KV 缓存增长留出余量。`--max-num-seqs` 应保持较低，因为 DGX Spark 更适合小批量推理而非高并发服务。
- **vLLM 在 DGX Spark 上的性能很大程度上取决于开发者目标。** 当前的 vLLM 构建应默认使用 CUDA Graph，除非特定部署有理由禁用它。调优后的设置可以通过更新的 FP4 内核、异步调度和 MTP 投机解码提升吞吐量，但内核选择因模型和版本而异。

## DGX Spark 架构与内存模型

DGX Spark 围绕 GB10 Grace Blackwell SoC 构建，拥有统一的 CPU+GPU 内存池。Spark 的芯片与系统封装决定了哪些推理工作负载在它上面运行效率最高。有三个特性很重要，而这三点都影响到本文其余部分的引擎与配置选择。

**统一内存扩展了开发者可以在本地使用的模型规模。** DGX Spark 的 CPU/GPU 共享内存池让开发者能比固定专用显存池允许的更多地把系统内存用于推理，使得在单台 Spark 上加载参数量高达 2000 亿（200 billion）的更大 NVFP4 模型成为可能，具体取决于模型架构与运行时配置。vLLM 与这一架构契合良好，因为它提供了 `--gpu-memory-utilization`、`--max-model-len`、`--max-num-seqs` 和分页 KV 缓存等控制手段，帮助开发者在统一内存池内平衡模型规模、上下文长度和并发度。对于更大的部署，多 Spark 配置可以进一步扩展这一能力，利用 ConnectX 网络接口的低延迟与高带宽支持跨系统的高效分布式推理。

**面向 Spark 的 `sm_121` 验证。** 对于 DGX Spark 部署，开发者应使用专门针对 `sm_121` 验证过的 vLLM 构建、容器镜像标签和运行时设置。如果你是在从更大的 GPU 系统移植 vLLM 配置，请把这种对照当作内核支持与内存行为的工程核对清单，而不是对 Spark 的性能预期。

**DGX Spark 非常适合 NVFP4 MoE 服务。** NVFP4 通过降低内存压力、改善预填充/模型适配行为带来最大的实际优势，而解码速度仍受活跃参数量和当前 vLLM 构建所用内核路径的影响。活跃参数量约 100-150 亿（10-15 billion）的 NVFP4 混合专家模型是绝佳选择，因为其活跃参数集更小，而新的混合精度与 FP4 内核路径也在持续改善解码性能。

最好把 DGX Spark 视为大型 NVFP4 模型的本地单用户或小批量推理目标。稠密模型和高并发服务也能运行，但与系统的内存带宽和统一内存特性契合度较低。

![Figure 2. DGX Spark GB10 unified memory for vLLM: CPU, GPU, model weights, etc. share one 128 GB pool.](https://vllm.ai/blog-assets/figures/2026-05-26-vllm-dgx-spark/gb10-unified-memory-sm121-map.svg)

图 2. DGX Spark GB10 为 vLLM 提供的统一内存：CPU、GPU、模型权重等共享一个 128 GB 内存池。

## 与 DGX Spark 相关的 vLLM 能力

在 DGX Spark 上运行 vLLM 服务，重点在于单台 Spark 上的本地小批量推理，以及多台 Spark 互联时的多节点扩展。最相关的能力包括节省内存的 KV 缓存管理、动态请求调度、OpenAI 兼容服务、运行指标，以及感知架构的镜像/运行时支持。

### 面向 Spark 统一内存预算的分页 KV 缓存

经典的推理批处理模式按到达时间给请求分组并同步执行。这对定长补全有效，但对聊天类工作负载效率低下：一个请求可能五个 token 就结束，另一个却可能生成数百个 token。vLLM 的连续批处理在每个解码步骤都接纳和逐出请求，GPU 因此不必等待静态批次中最长的请求。配合分页 KV 缓存，Spark 的内存预算可以支撑一定数量的在途请求而不产生过度碎片。在 Spark 上服务一个 120B NVFP4 MoE 的实际运行中，KV 缓存利用率在单用户测试中通常保持在 5% 以下，在小批量演示流量下保持在 30% 以下。

### 本地 Spark 端点的 OpenAI 兼容流式输出

在 Spark 上，OpenAI 兼容 API 的意义不在于给框架打勾，而在于让本地应用保持简单。与托管 OpenAI 兼容端点通信的同一份客户端代码可以直接指向本地 vLLM 端点，例如 `http://localhost:8000/v1`。

流式输出是让 DGX Spark 在本地推理中感觉响应迅速的关键。虽然数据中心 GPU 可能提供更高的解码吞吐量，但 `stream=true` 让应用在 token 到达时立即渲染，给用户即时反馈，在桌面系统上营造自然的交互体验。这使得 Spark 成为聊天、编码和智能体工作流的实用本地端点——在这类场景中，感知延迟与总生成时长同样重要。

### 通过 Prometheus 观察 Spark 服务指标

在单台 Spark 上，可观测性意味着确认这台设备表现得像一个交互式本地家电：提示快速完成预填充、解码保持平稳、统一内存池有足够余量。vLLM 的 Prometheus 端点无需添加单独的服务即可暴露这些信号。在演示期间，侧边遥测视图可以在同一台机器上轮询 `/metrics`。

对 DGX Spark 最有用的信号是 KV 缓存利用率（`vllm:kv_cache_usage_perc`）、提示与生成 token 计数器，以及 TTFT / 逐 token 延迟直方图。在一次健康的交互式智能体运行中，开头阶段智能体读取系统提示时，提示处理会占用一些时间。在后续轮次中，KV 缓存持续增长，但当上一段对话前缀已被缓存时，提示处理时间不应出现尖峰。生成吞吐量与逐 token 延迟会稳定在预期解码速率附近。KV 缓存利用率会增长，但整体 KV 缓存保持在足够低的水平，系统不会耗尽内存。最终，智能体应用可以在 KV 缓存用量接近上下文上限之前压缩对话。

### 面向 DGX Spark 的官方 vLLM 镜像

DGX Spark 最好搭配为其 `sm_121` 目标构建并经过测试的软件栈。当前的 Nemotron-3-Super Spark 配方使用 vLLM 官方的 OpenAI 兼容服务器镜像。在我们运行时，使用的是 CUDA 13 nightly 轨道 [`vllm/vllm-openai:cu130-nightly`](https://hub.docker.com/r/vllm/vllm-openai/tags?name=cu130-nightly)，并配合 Spark 专属的解析器、FP4、调度与内存设置。

由于 nightly 标签会随时间变动，应把 `cu130-nightly` 视为兼容性轨道，而非可复现的固定版本。对于正式部署，请针对特定发布镜像、特定 commit 的 nightly 标签或镜像摘要验证模型配方，然后在你的运行手册中保留那个确切的镜像引用。

关键在于，Spark 不需要专门定制的服务接口：它通过 vLLM 标准的 OpenAI 兼容服务器运行。Spark 专属的工作在于模型配方、经过测试的镜像引用，以及匹配 GB10 `sm_121` 特性的运行时标志。

## 运行时配置与环境变量

本节介绍在 DGX Spark 上 `vllm serve` 的主要部署设置，并解释每个选项的作用。

### 应当先查阅的配方与文档

以 [vLLM Recipes](https://recipes.vllm.ai/) 索引作为模型专属命令的起点，然后交叉核对 [`vllm serve` CLI 参考](https://docs.vllm.ai/en/latest/cli/serve/)和 [vLLM Docker 文档](https://docs.vllm.ai/en/latest/deployment/docker/)，确认你所装版本中标志与镜像的确切行为。对于应用集成与生产可观测性，请把 [OpenAI 兼容服务器文档](https://docs.vllm.ai/en/latest/serving/openai_compatible_server/)和 [vLLM 生产指标文档](https://docs.vllm.ai/en/latest/usage/metrics/)放在手边。NVIDIA Spark 指南仍是 DGX Spark 专属模型配方、解析器插件和内核设置的权威来源。

### 模型选择

在调标志之前，模型选择是 Spark 上最大的性能杠杆。图 3 是方向性的模型选择指南，而非性能表：它概括了各类代表性模型通常如何映射到 Spark 的内存容量、活跃参数量和本地交互式服务特征。

![Figure 3. Directional DGX Spark model-fit guidance across current model classes, showing why 100-130B MoE NVFP4 models with roughly 10-15B active parameters are a strong fit for local vLLM serving on Spark.](https://vllm.ai/blog-assets/figures/2026-05-26-vllm-dgx-spark/dgx-spark-model-fit-decode-rate.svg)

图 3. 跨当前模型类别的 DGX Spark 模型适配方向性指南，说明为什么 100-130B、活跃参数约 10-15B 的 MoE NVFP4 模型非常适合在 Spark 上进行本地 vLLM 服务。

[Nemotron-3-Super-120B-A12B-NVFP4](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-NVFP4) 是下文的具体工作示例，因为它是与 Spark 非常匹配的 NVFP4 MoE 模型。对于其他 Spark 规模的 NVFP4 MoE 模型，请保持相同的服务原则，但从该模型自己的配方出发。

### 预先放置权重

避免让第一次 `vllm serve` 调用同时执行一次大规模模型下载。更可预期的模式是：先把权重一次性预置到宿主机挂载的 Hugging Face 缓存中，再把同一个缓存挂载进长期运行的容器。模型专属的下载与启动示例见 [vLLM Recipes](https://recipes.vllm.ai/)；对 Spark 而言，原则是“一次下载，处处挂载”。

### 对 `vllm serve` 重要的标志

示例命令使用 `vllm serve nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-NVFP4` 加上以下标志。

**`--gpu-memory-utilization`。** vLLM 允许占用的 GPU 可见内存的比例。在 Spark 上，这是统一内存池的一个比例，因此该设置应为操作系统、内核页缓存、容器运行时、KV 缓存增长以及任何其他会触碰同一块内存的进程留出空间。从模型配方出发，再根据观察到的内存余量和工作负载并发度进行调优。

**`--max-model-len 131072`。** 服务器接受的提示 + 补全最大长度。现代推理服务需要 131K，因为系统提示、工具 schema、文件和历史记录很容易超过 20K token。你可以把它上调至模型支持的最大值，或在受限演示中调低，但不应把它当作每个在途请求的固定最坏情况 KV 预留；vLLM 根据运行中请求实际使用的活跃上下文来调度。

**`--max-num-seqs 4`。** vLLM 允许接纳的在途序列最大数量。对于 Spark 上的 Nemotron NVFP4，当前配方保持较低的数值。超过四路并发解码流时，逐 token 的带宽代价可能超过连续批处理带来的收益，首 token 延迟（TTFT）会出现尖峰。

**自动前缀缓存。** vLLM 的[自动前缀缓存](https://docs.vllm.ai/en/latest/design/prefix_caching/)在共享开头提示的请求之间复用 KV 块。它在 vLLM V1 中默认启用，因此下面的示例没有传 `--enable-prefix-caching`。它对带有较长共享系统提示的聊天工作负载很有用，但即使在缓存命中为零时应用也应保持正确。

**工具与推理解析器标志。** vLLM 可以把模型专属的推理轨迹与工具调用格式解析成结构化的 OpenAI 兼容响应字段。在 Spark 上，这些标志应遵循模型配方而非硬件默认值：只对会输出受支持推理块的模型设置推理解析器，只在客户端需要工具调用时设置 `--enable-auto-tool-choice` 加上工具调用解析器。对于当前的 vLLM 构建，Nemotron-3 模型可以使用内置的 `--reasoning-parser nemotron_v3` 路径；较旧的 Spark 配方可能仍引用外部的 `super_v3` 解析器插件。

有几个标志值得评估，但未经验证不应直接照搬进演示运行手册。**[`--kv-cache-dtype fp8`](https://docs.vllm.ai/en/latest/features/quantization/quantized_kvcache/)** 可以降低 KV 缓存的内存压力，但可能影响模型行为的可预测性，并且在 Spark 上对某些工作负载带有明显的性能代价；除非内存压力确实需要且质量检查通过，否则应避免使用。**[`--speculative-config`](https://docs.vllm.ai/en/latest/features/speculative_decoding/)** 用于启用投机解码；对 Nemotron-3-Super 而言，相关路径是该模型的 MTP 支持。**`--tensor-parallel-size 2`** 只在两台 Spark 通过 ConnectX-7 端口互联时才有意义；请将其用于经过验证的多 Spark 配方，而不是当作单节点调优标志。

### 何时覆盖 vLLM 默认值

vLLM 的默认启发式会为所安装版本选择合适的量化线性层、MoE 和检查点加载路径。在单 GPU 的 DGX Spark 上，先从模型配方和 vLLM 默认值出发，只有当显式覆盖是针对你验证过的确切模型、镜像和硬件组合有意为之时，才添加它们。

**后端选择。** 除非你测试过的配方要求特定后端，否则请将量化线性层与 MoE 后端选择保持在 `auto`。正确的 FP4 路径可能随 vLLM 版本和模型架构而变化；最近的 FlashInfer CUTLASS 路径比旧版 Spark 指南所暗示的要强得多。如果你有意固定后端，优先使用 `--linear-backend` 和 `--moe-backend` 等 CLI 标志；这条路径上较旧的环境变量已被弃用。

**版本特定的变通方法。** 一些 Spark 配方包含针对特定镜像标签的兼容性环境变量。请把这些当作版本特定的变通方法，而不是 vLLM 的一般要求。例如，对不使用张量并行的单 Spark 命令而言，不需要 FlashInfer allreduce 后端覆盖。

**检查点量化。** vLLM 会从模型配置中检测检查点量化。对于预量化的 NVFP4 检查点，请不要设置 `--quantization`；只有当你有意让 vLLM 在加载时应用某种量化方法时才使用它。

### 预热 JIT

冷启动行为取决于模型、内核、镜像标签和请求路径。在我们的 Nemotron-3-Super Spark 环境中，`vllm serve` 启动后的第一个请求会触发 Inductor 和 FlashInfer 的 JIT 代码生成，耗时约 25 秒。不要把这条路径留给终端用户。让应用在启动时发送一个小的 `ping` 请求，走与真实工作负载相同的客户端路径（同样的模型、同样的 `chat_template_kwargs`，只是 `max_tokens=3`）。相关内核热身之后，在我们的环境中同样的短提示路径在半秒内即可返回。

初始权重加载是与请求热身不同的问题。如果 10-15 分钟的 safetensor 加载时间对你的部署有影响，请针对你确切的模型、镜像和存储栈评估 vLLM 的 [fastsafetensors](https://docs.vllm.ai/en/latest/models/extensions/fastsafetensor/) 或 [InstantTensor](https://docs.vllm.ai/en/latest/models/extensions/instanttensor/) 加载路径。

### 可预测性与吞吐量调优

Spark 的 vLLM 配置可以面向简单直接的演示运行调优，也可以面向最大吞吐量调优。

在本文的测量中，`--kv-cache-dtype` 未设置、投机解码被禁用、CUDA Graph 保持启用。请把这些当作针对该模型、镜像和工作负载实测得出的配方选择，而不是 Spark 的通用默认值。面向吞吐量的运行仍可以评估 FP8 KV 缓存、异步调度、投机解码和显式后端选择，但这些设置应针对确切的模型、提示形态、批模式与 vLLM 版本进行验证。

合适的平衡点取决于工作负载。在这里，我们为面向公众的演示路径做优化：可预测的本地服务、清晰的遥测和稳定的响应。

![Figure 4. DGX Spark vLLM configuration slider from straightforward demo settings to tuned throughput settings, comparing model-specific options such as FP4 backend selection, async scheduling, and speculative decoding.](https://vllm.ai/blog-assets/figures/2026-05-26-vllm-dgx-spark/spark-vllm-config-stability-performance-slider.svg)

图 4. DGX Spark 的 vLLM 配置滑块，从简单直接的演示设置到调优后的吞吐量设置，对比 FP4 后端选择、异步调度和投机解码等模型专属选项。

## 示例工作负载：vllm-spark-game

为了在简单的 `curl` 调用之外测试这套配置，我们构建了 [vllm-spark-game](https://github.com/zlxi02/vllm-spark-game)。这个游戏在本地 vLLM 端点上运行一场实时的“二十个问题”（20-Questions）交互，同时一个配套的统计视图从同一台 Spark 轮询 vLLM 和 GPU 遥测。这个工作负载的意义在于端到端地锻炼服务路径：OpenAI 兼容聊天请求、流式响应、提示预填充、解码、KV 缓存行为和实时指标。源码布局与运行命令见[项目 README](https://github.com/zlxi02/vllm-spark-game/blob/master/README.md)。

![vllm-spark-game demo at the Inferact booth during MLSys, May 2026.](https://vllm.ai/blog-assets/figures/2026-05-26-vllm-dgx-spark/spark-demo-crowd.jpg)

2026 年 5 月 MLSys 期间，vllm-spark-game 在 Inferact 展位的演示。

### Docker 启动命令

以下是这个示例工作负载的完整 Docker 命令，其中挂载了宿主机的 Hugging Face 缓存以在重启之间复用权重。代码片段中保留了 `cu130-nightly` 作为经过测试的兼容性轨道；对于可复现的部署，请将其替换为你验证过的确切发布标签、特定 commit 的 nightly 标签或镜像摘要。

```
docker run -d --name vllm --ipc=host --restart unless-stopped \
  --gpus all -p 8000:8000 \
  -e HF_TOKEN="$HF_TOKEN" \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  vllm/vllm-openai:cu130-nightly \
  nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-NVFP4 \
    --served-model-name nemotron-3-super \
    --trust-remote-code \
    --max-model-len 131072 \
    --gpu-memory-utilization 0.85 \
    --max-num-seqs 4 \
    --reasoning-parser nemotron_v3 \
    --enable-auto-tool-choice \
    --tool-call-parser qwen3_coder
```

在我们的环境中，使用默认 safetensor 加载路径时首次加载需要 10-15 分钟。对于启动时间重要的部署，请在敲定运行手册前评估 fastsafetensors 或 InstantTensor。用 `curl -sS http://localhost:8000/v1/models | jq -r '.data[0].id'` 验证就绪状态；该命令应返回 `nemotron-3-super`。

### 部署形态

![Figure 5. vllm-spark-game sends chat requests to /v1 while spark-stats polls /metrics and NVML from the same local vLLM endpoint.](https://vllm.ai/blog-assets/figures/2026-05-26-vllm-dgx-spark/vllm-spark-game-demo-flow.svg)

图 5. vllm-spark-game 向 /v1 发送聊天请求，同时 spark-stats 从同一个本地 vLLM 端点轮询 /metrics 和 NVML。

### 单 Spark 评估结果

我们针对一个本地 vLLM OpenAI 兼容端点（在单台 DGX Spark 上承载 Nemotron-3-Super-120B-A12B-NVFP4）运行了面向应用的五场景评估。这些数字旨在把部署方法讲具体，而不是作为排行榜提交。在我们更新的单 Spark 评估中，各场景实测解码吞吐量保持在 22.7-23.7 tok/s 区间。每行数据是单次预热调用之后三次运行的中位数。精确 token 数来自 `stream_options.include_usage`，而不是 chunk 计数。

| 场景 | 提示 token | 生成 token | TTFT | 总延迟 | 预填充 tok/s | 解码 tok/s |
| --- | --- | --- | --- | --- | --- | --- |
| 典型裁判调用（真实 20Q，含噪的 2-token 生成） | 58 | 2 | 0.42 s | ~0.53 s | 140 | ~23 |
| 中等提示，短生成 | 1,834 | 32 | 1.12 s | ~2.47 s | 1,636 | 23.7 |
| 长提示，短生成 | 7,234 | 32 | 3.85 s | ~5.26 s | 1,877 | 22.7 |
| 中等提示，长生成 | 1,834 | 108 | 1.12 s | ~5.74 s | 1,639 | 23.4 |
| 长提示，长生成 | 7,234 | 124 | 3.84 s | ~9.26 s | 1,884 | 22.9 |

*表 2. 在承载 Nemotron-3-Super-120B-A12B-NVFP4 的本地 vLLM 端点上的五场景单 Spark 评估。每行报告预热后三次运行的中位数。*

![Figure 6. vLLM single-Spark evaluation sweep on DGX Spark showing TTFT, total latency, prefill throughput, and measured decode throughput in the 22.7–23.7 tok/s range for Nemotron-3-Super-120B-A12B-NVFP4.](https://vllm.ai/blog-assets/figures/2026-05-26-vllm-dgx-spark/dgx-spark-vllm-benchmark-sweep.svg)

图 6. DGX Spark 上的 vLLM 单 Spark 评估扫描，显示 Nemotron-3-Super-120B-A12B-NVFP4 的 TTFT、总延迟、预填充吞吐量，以及处于 22.7–23.7 tok/s 区间的实测解码吞吐量。

### 评估解读

**预填充随提示长度近乎线性扩展。** 提示增长四倍时，TTFT 大约变为三倍。当提示大到足以摊薄每请求开销时，预填充速率从 140 攀升至接近 1,900 token/秒。预填充是计算受限的，并且可以在整个提示上并行，因此更直接地受益于可用的张量核吞吐量。

**在这些单 Spark 评估运行中，解码吞吐量保持在 22.7–23.7 tok/s 的窄带内。** 裁判调用的用户侧延迟比其解码速率更重要，因为它只生成两个 token。解码仍取决于活跃参数量、FP4 内核路径、CUDA Graph 行为以及确切的 vLLM 镜像。请把这当作 Nemotron-3-Super 在单台 DGX Spark 上的配方特定结果，而不是 DGX Spark 或 vLLM 的通用上限。

**配置说明。** 这些测量结果特定于本次运行所用的镜像标签、上下文长度、CUDA Graph 状态、后端路径和调度设置。复现评估时请一并报告这些值。

**游戏过程中的实时表现。** 一个典型的“二十个问题”回合发送约 1,000 token 的提示（系统提示 + 事实块 + 秘密词 + 问题）。端到端感知延迟仍主要由 TTFT 和短暂的解码突发决定；对于 5–15 个输出 token，在实测的 22.7–23.7 tok/s 区间内解码约需 0.2–0.7s。游戏过程中 KV 缓存利用率很少超过 2%。遥测视图显示，每个回合开始后 `prompt_tps` 会短暂冲高，随后在答案流式输出的稳定生成阶段，`gen_tps` 保持在实测的 22.7–23.7 tok/s 区间内。

## 运维要点

选择正确的模型类别是第一个调优决策：100-130B 的 MoE NVFP4 模型与 Spark 的内存容量和活跃参数特征匹配良好，而稠密模型通常与交互式本地解码契合度较低。除非需要自定义内核，官方 vLLM 镜像加上经 Spark 测试的配方可以规避源码构建风险。`--gpu-memory-utilization` 应针对统一内存池以及共享它的其他进程进行调优。预热 JIT 可以避免把冷启动延迟丢给第一个用户请求。`/metrics` 暴露了理解负载行为所需的 KV 缓存利用率和 TTFT 直方图。

## 结语

DGX Spark 是一个面向开发、演示和小批量服务的本地推理系统，其服务特征与数据中心 GPU 服务器不同。它的统一内存架构、`sm_121` 目标、模型专属 FP4 路径和本地解码特性，使工作负载调优格外重要。有了正确的模型、镜像标签和运行时设置，Spark 为开发者提供了一种在本地服务大型模型的实用方式，同时保留了熟悉的生产风格工作流。

vLLM 是 DGX Spark 的默认之选，因为它把这些选择保留在服务层，同时保有标准的应用接口。一旦模型、镜像标签和标志经过验证，应用依然能获得 OpenAI 兼容 API、流式输出、连续批处理、分页 KV 缓存管理和 Prometheus 指标。

---

*本文由 [Inferact](https://inferact.ai) 团队撰写，写作时使用的正是我们在办公室里持续运行的一台 Spark。*
