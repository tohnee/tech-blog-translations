---
title: "vLLM AFD 插件正式发布：注意力与 FFN 分离，实现灵活的 MoE 服务"
title_en: "Announcing vLLM AFD Plugin: Disaggregating Attention and FFN for Flexible MoE Serving"
source: https://vllm.ai/blog/2026-07-23-vllm-afd-plugin
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM AFD 插件正式发布：注意力与 FFN 分离，实现灵活的 MoE 服务

> 原文：[Announcing vLLM AFD Plugin: Disaggregating Attention and FFN for Flexible MoE Serving](https://vllm.ai/blog/2026-07-23-vllm-afd-plugin) · vLLM 博客

作者：AFD Plugin 贡献者们

[#推理](https://vllm.ai/blog/tags/inference)[#MoE](https://vllm.ai/blog/tags/moe)[#生态](https://vllm.ai/blog/tags/ecosystem)

我们很高兴推出 [**vLLM AFD 插件**](https://github.com/vllm-project/afd-plugin)——一个实验性的外部插件，为 vLLM 带来**注意力-FFN 分离（Attention-FFN Disaggregation，AFD）**。

vLLM AFD 插件通过将 Attention 与 FFN 拆分为独立部署的服务，把 AFD 引入混合专家（MoE）模型。该插件保留了 vLLM 既有的请求生命周期和 OpenAI 兼容服务接口，同时允许 Attention 与 FFN 两条路径独立扩展。

该项目目前支持 NVIDIA GPU 与 Ascend NPU、同步与异步连接器、DeepSeek V2/V3 系列模型封装，以及在明确验证范围内的 eager、graph 和 dual-batch 执行路径。

> **注意：** 该项目仍处于实验阶段，需要在更多不同硬件后端上开展大规模测试。

## 为什么要做注意力-FFN 分离？

混合专家（MoE）推理在每一个 transformer 层内部都结合了两种截然不同的工作。Attention 是有状态的，与请求调度和 KV 缓存紧密耦合；而 FFN（专家路径）则由路由专家计算和 all-to-all 通信主导。当两条路径共享同一套 worker 拓扑时，服务系统必须用同一套扩展与执行策略，去应对需求差异极大的工作负载。

要让这种分离真正落地，需要解决若干系统设计挑战：

1. **Attention 与 FFN 的扩展需求不同。** Attention 的容量取决于请求状态、序列长度和 KV 缓存压力；专家容量则取决于 token 路由与专家负载。服务系统应当支持独立扩展，让两条路径使用不同的 rank 拓扑，而不是强制共享一套布局。
2. **Attention 与 FFN 的运行时职责不同。** Attention 需要调度、KV 缓存协调和采样；FFN 执行只需要激活值、路由元数据，以及一种把专家输出返回的方法。拆分服务后，FFN 一侧可以作为轻量的、由连接器驱动的守护进程运行。
3. **通信是后端相关的。** CUDA 与 Ascend 暴露的集合通信库、图运行时和优化的 MoE 算子各不相同。一个通用的连接器契约能让面向模型的流程保持稳定，同时允许各后端拥有自己的数据通路。
4. **通信与计算可以受益于重叠。** 异步派发与 MoE ubatching 可以让相互独立的阶段重叠执行，而不是把所有专家工作都串行排在 Attention 路径之后。

这些挑战共同定义了 AFD 的核心设计目标：保持 vLLM 面向请求的 Attention 路径原封不动，同时把 FFN 执行移到一个狭窄的连接器接口之后，使其能够独立扩展、通信和执行。

## 架构内部

![vLLM AFD Plugin runtime architecture](https://vllm.ai/blog-assets/figures/2026-07-23-vllm-afd-plugin/vllm-afd-plugin-architecture.svg)

vLLM AFD 插件运行时架构

该插件通过 vLLM 的 `vllm.general_plugins` 入口点和标准的 `--additional-config` 通道集成，不需要修改 vLLM 源码树。

运行时由三个主要部分组成：

- **Attention 服务。** Attention worker 保留 vLLM 的调度器、KV 缓存、批处理、模型生命周期与采样路径。由插件提供的 model runner 会把 AFD 元数据装入 forward context，并把数据并行、ubatch、层与图状态发布给 FFN 一侧。
- **FFN 服务。** FFN worker 没有请求流量、调度器或 KV 缓存。一个后台循环接收元数据与激活值，在插件提供的模型封装上调用 `compute_ffn_output()`，再把结果返回给 Attention。请求始终发给 Attention API 服务器。
- **连接器层。** 在每个切分层，连接器把 Attention 隐藏状态连同 FFN 服务所需的执行元数据一起传输，然后返回计算好的 FFN 输出。一个后端中立的连接器接口定义了这种交换，同时允许各后端实现自己的通信与运行时优化。

这一集成面被刻意设计得很小。在现有抽象适用之处，vLLM 继续拥有服务控制平面；插件则提供 AFD worker、model runner、连接器、元数据、模型切分点的实现，以及一小组限定版本的兼容性补丁。

### 连接器与后端支持

| 连接器 | 后端 | 执行方式 | 建议阶段 | 图支持 |
| --- | --- | --- | --- | --- |
| `P2pNcclAFDConnector` | GPU | 同步 P2P | 解码 | `FULL_DECODE_ONLY` CUDA Graph |
| `CAMP2pAFDConnector` | NPU | 同步 CAMP2P/HCCL | 解码 | `FULL_DECODE_ONLY` ACL 图 |
| `CAMAsyncAFDConnector` | NPU | 异步 CAM | 预填充 | 暂不支持 |

同一种高层交换——Attention 输出送 FFN、FFN 输出回 Attention——在各连接器之间共享。后端包保持相互独立，使 CUDA Graph 行为、ACL 图行为、NCCL 通信与 Ascend 自定义算子不会相互渗透。

### 支持的特性

- **原生 vLLM 服务面。** 现有 vLLM 用户仍然用 `vllm serve` 启动，把请求发给 OpenAI 兼容端点，并通过 `--additional-config` 配置运行时。
- **GPU 与 NPU 实现。** GPU worker 扩展 vLLM v1 类，而 NPU worker 直接扩展 vLLM-Ascend 类。共享行为放在配置、拓扑、元数据和连接器契约中，而不是跨设备继承。
- **面向解码吞吐的同步 AFD。** `P2pNcclAFDConnector` 与 `CAMP2pAFDConnector` 同步交换 Attention 激活值与 FFN 输出，让两种角色在以吞吐为导向的解码部署中独立扩展。它们当前的图路径分别使用 CUDA 与 ACL 上的 `FULL_DECODE_ONLY` 语义。
- **面向预填充的异步 AFD。** `CAMAsyncAFDConnector` 使用 CAM 异步派发与 combine 算子，把预填充 Attention rank 与专家 worker 解耦。配合 AFD 管理的 MoE ubatching，它让相互独立的 Attention 与 FFN 阶段重叠执行，以减少流水线停顿。该路径目前面向预填充/解码分离部署中的预填充阶段，尚不支持图执行。
- **MoE 模型集成。** 插件为 DeepSeek V2/V3 系列架构（包括 DeepSeek V3.2）以及 GLM MoE DSA 注册了封装。封装暴露独立的 Attention 与 FFN 计算，同时复用上游层实现。
- **图与 ubatching 路径。** 同步 GPU 与 NPU 连接器支持仅解码的图捕获。Dual Batch Overlap 支持恰好两个 ubatch 的场景，CAM async 则为其预填充路径提供 AFD 管理的 MoE ubatching。

## 性能快照

### 使用 `CAMP2pAFDConnector` 的同步 AFD 解码吞吐

[vllm-project/afd-plugin#67](https://github.com/vllm-project/afd-plugin/pull/67) 中的同步解码配方，在 Ascend 910C 上比较了传统 EP64 部署与基于 `CAMP2pAFDConnector` 的 AFD 部署在 DeepSeek-V3.2 W8A8 上的表现。该基准测量的是饱和解码吞吐，而非在线服务延迟。

| 部署 | 物理拓扑 | 总 die 数 |
| --- | --- | --- |
| EP64 | DP64, EP64, TP1 | 64 |
| 48A16F | 48 个 Attention rank，16 个 FFN rank | 64 |
| 64A16F | 64 个 Attention rank，16 个 FFN rank | 80 |

> **注意：** 这些是受控的性能结果，不是精度或生产服务结果。由于机器可用性有限，物理 48A16F 和 64A16F 部署模拟了逻辑 192A64F 和 256A64F 的规模。实验用确定性的强制均衡循环替代了自然路由的专家 ID，这会改变模型输出。`AFDDecodeBenchConnector` 提供仅解码的 KV 状态，AFD 启用了 DBO。

吞吐按部署 die 的总数归一化：

```
tokens/s/die = aggregate output token throughput / total deployed dies
```

两种工作负载都使用定长输入和从 512 到 1,536 token 均匀分布的输出。

#### 16K 固定输入

![DeepSeek-V3.2 16K decode throughput per die](https://vllm.ai/blog-assets/figures/2026-07-23-vllm-afd-plugin/throughput_dsv3-2_16k.png)

DeepSeek-V3.2 16K 每 die 解码吞吐

EP64 达到 **232.6 tokens/s/die**，48A16F 达到 **220.3 tokens/s/die**，64A16F 达到 **258.9 tokens/s/die**。相对 EP64，AFD 结果为 48A16F **-5.3%**、64A16F **+11.3%**。

#### 32K 固定输入

![DeepSeek-V3.2 32K decode throughput per die](https://vllm.ai/blog-assets/figures/2026-07-23-vllm-afd-plugin/throughput_dsv3-2_32k.png)

DeepSeek-V3.2 32K 每 die 解码吞吐

EP64 达到 **168.2 tokens/s/die**，48A16F 达到 **151.4 tokens/s/die**，64A16F 达到 **183.3 tokens/s/die**。相对 EP64，AFD 结果为 48A16F **-10.0%**、64A16F **+9.0%**。

在两种输入长度下，48A16F 都低于 EP64 基线，而 64A16F 提供了最高的归一化吞吐：**16K 时 +11.3%**，**32K 时 +9.0%**。这一结果表明 Attention 与 FFN 的配比很重要；分离本身并不保证吞吐提升。

由于机器可用性有限，我们没有评估 Attention 与 FFN 配比更高的部署。观察到的趋势表明，在所测配比下，FFN rank 仍有计算余量，而不是受计算限制。因此，提高 Attention rank 的占比可能带来进一步的吞吐增益。

### 使用 `CAMAsyncAFDConnector` 的异步 AFD 预填充性能

仓库中包含一项在两个 Ascend 910C 节点上进行的早期 CAM async 实验，使用裁剪到 10 层的 DeepSeek V3.2 W8A8 模型。对比采用强制专家均衡，将 `DP4PCP8 TP1` 基线与由 Attention `DP3PCP8 TP1` 加 FFN `EP8` 组成的 AFD 布局进行对照。

![Median TTFT comparison for the CAM async experiment](https://vllm.ai/blog-assets/figures/2026-07-23-vllm-afd-plugin/text_matched_dp_afd_median_ttft.png)

CAM async 实验的中位数 TTFT 对比

在所测的请求速率范围内，AFD 配置降低了中位数/P50 首 token 时间。在每秒 12 个请求时，中位 TTFT 从 **15.1 秒降至 8.0 秒**，降幅约 **47%**。在每秒 10 个和 12 个请求时，实测差距均约为 7.2 秒。

**注意**：这些数字是对 CAM async 执行路径的针对性验证，并不是对完整 DeepSeek V3.2 或所有 AFD 拓扑的普适性能结论。性能收益也可能因工作负载而异。

## 快速上手

当前实现要求 Python 3.10–3.13，面向 vLLM `0.19.1`。

### 安装

安装步骤详见我们的 [README](https://github.com/vllm-project/afd-plugin#install)。

### 部署配方

部署命令取决于后端、连接器、模型和 rank 拓扑。与其在这里重复罗列配置，不如使用我们持续维护的 [AFD Plugin 配方](https://github.com/vllm-project/afd-plugin/tree/main/recipe)：

- **GPU 同步 AFD：** [DeepSeek V2 Lite P2P NCCL 配方](https://github.com/vllm-project/afd-plugin/tree/main/recipe/gpu/p2p_nccl/deepseek_v2_lite)覆盖面向解码的共置部署与预填充/解码分离部署、eager 与 CUDA Graph 执行，以及多种 DP/TP 布局。
- **NPU 异步预填充 AFD：** [DeepSeek V3.2 CAM async 配方](https://github.com/vllm-project/afd-plugin/blob/main/recipe/npu/cam_async/DeepSeek-V3.2.md)记录了所需环境、拓扑、AFD 配置、基准测试设置与当前限制。

最新的连接器支持矩阵、配置字段和完整启动命令，请参阅仓库 README 与 recipe 目录。

## 当前范围与路线图

该项目刻意公开了当前的边界：精确的 vLLM 版本锁定、仅支持 model runner v1、两个角色都持有完整权重、仅解码的图模式、DBO 恰好两个 ubatch，以及受硬件条件限制的端到端测试。

下一阶段的开发将聚焦于：

- **更广泛的 vLLM 兼容性与上游对齐：** 跟踪更新的 vLLM 版本、评估 model runner v2、把兼容性补丁保持在最少，并在通用抽象成熟后向上游贡献。
- **更灵活的执行：** 扩展图模式、ubatch 数量、异步阶段以及经过验证的 rank 拓扑。
- **生产规模验证：** 在完整模型和真实工作负载上发布可复现的精度、延迟、吞吐、稳定性与多节点结果。
- **扩展模型与连接器覆盖：** 通过现有的模型封装与连接器接口增加 MoE 架构和后端传输，并为每个新支持的模型和连接器提供相应的部署配方。
- **多模态与 vLLM-Omni 集成：** 探索 AFD 如何与 [vLLM-Omni](https://github.com/vllm-project/vllm-omni) 以及异构多模态流水线集成，包括在自回归（AR）、Diffusion Transformer（DiT）等可以受益于独立扩展的 Attention 与 FFN 执行的阶段中的应用。
- **异构硬件与低延迟服务：** 探索在不同加速器类型与互连上部署 Attention 与 FFN 角色，以及通过连接器、调度、放置和计算-通信重叠等优化来降低首 token 延迟与逐 token 延迟。

## 加入社区

vLLM AFD 插件尚处于早期阶段，来自模型、服务和硬件社区的反馈将决定其方向。

- **代码与文档：** [github.com/vllm-project/afd-plugin](https://github.com/vllm-project/afd-plugin)
- **运行时设计文档：** [GPU Attention/FFN 与 Ascend Attention/FFN 设计](https://github.com/vllm-project/afd-plugin/tree/main/docs)
- **问题与功能请求：** [GitHub Issues](https://github.com/vllm-project/afd-plugin/issues)

让我们一起为 MoE 服务构建一个更可组合、更硬件感知的未来。
