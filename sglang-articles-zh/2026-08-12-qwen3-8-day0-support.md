---
title: "SGLang 与 Miles 为 Qwen3.8 提供 Day-0 支持"
title_en: "SGLang and Miles Add Day-0 Support for Qwen3.8"
author: "SGLang Team"
date: "Aug 12, 2026"
source: https://lmsys.org/blog/2026-08-12-qwen3-8-day0-support/
translated: 2026-09-12
previewImg: /images/blog/qwen3-8-day0-support/cover-qwen3-8.png
type: blog
---

# SGLang 与 Miles 为 Qwen3.8 提供 Day-0 支持

> 原文：[SGLang and Miles Add Day-0 Support for Qwen3.8](https://lmsys.org/blog/2026-08-12-qwen3-8-day0-support/) · LMSYS Blog · SGLang Team

我们很高兴地宣布，SGLang 与 Miles 为 **[Qwen3.8-2.4T-A95B](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B)** 提供 Day-0 支持（首发日支持）。这是 Qwen 最大的开源模型，总参数量达 2.4T、每 token 激活 95B 参数，其混合注意力架构对推理服务栈关于状态的绝大多数假设都构成了压力。在与 Qwen、阿里云百炼（Alibaba Bailian）、NVIDIA 和 AMD 团队的合作下，SGLang 在发布首日即完整覆盖了该模型。本文介绍这背后的工作。

**亮点**

- **混合架构。**共 92 层，69 层 GDN 线性注意力层与 23 层 GQA 全注意力层按 3:1 模式交错排列，MoE 层包含 512 个专家、top-10 路由。
- **由我们量化的 NVFP4 检查点** [RadixArk/Qwen3.8-2.4T-A95B-NVFP4](https://huggingface.co/RadixArk/Qwen3.8-2.4T-A95B-NVFP4)，于发布首日同步放出。
- **与 NVIDIA 共同打造、通过 FlashInfer 交付的内核栈**：MoE finalize 与 all-reduce、RMSNorm 融合（端到端提升 10% 以上）、上下文并行 GDN 预填充内核，以及低延迟单 GEMM 路径（端到端约 4%）。
- **投机解码**：在 B300 上以 TP8 运行时，NVFP4 检查点在 batch size 1 下配合 MTP（接受长度 3.3）解码速度达 **346** tok/s，配合 DSpark（接受长度 4）达 **378** tok/s。两个数值均包含 bonus token。
- **按阶段划分的并行方式**：分块流水线并行预填充，以及数据并行与专家并行结合的解码 worker，在 PD 分离下组合后在 8k/1k 负载上达到每 GPU **5,126** tok/s，并借助暂存缓冲区（staging buffer）让两侧独立设定规模与并行方式。
- **基于 Miles 的 Day-0 强化学习（RL）**：在原生 NVFP4 基座上共置（colocated）LoRA 训练，BF16 Megatron 训练器与 NVFP4 SGLang rollout 引擎共享同一批 64 台 GB300，并在 GSM8K 上运行 GRPO，验证了奖励稳定、训练/rollout KL 保持平稳。

启动命令与按负载类型的配置指引见 [Qwen3.8 cookbook](https://docs.sglang.io/cookbook/autoregressive/Qwen/Qwen3.8)。

## 模型架构

Qwen3.8-2.4T-A95B 延续了 Qwen3.5/3.6 系列的混合注意力设计。这一代将总参数量扩展到 2.4T，每 token 激活 95B 参数，分布在 92 层中。

### 架构亮点

Qwen3.8-2.4T-A95B 架构包括：

<img src="https://qianwen-res.oss-accelerate.aliyuncs.com/Qwen3-Next/model_architecture.png" alt="Qwen3.8-2.4T-A95B model architecture" width="400">

- **混合注意力。**将 69 层线性注意力（GDN）层与 23 层全注意力（GQA）层按 3:1 交错组合。该设计在线性计算复杂度与长上下文建模性能之间取得了平衡。


- **GDN（Gated Delta Network，门控增量网络）。**线性注意力层将状态空间模型（SSM）与因果卷积（CausalConv1d）相结合。用固定大小的循环状态取代不断增长的 KV 缓存，因此每个 GDN 层的内存占用为 `O(1)`，而计算量按 `O(N)` 扩展。

- **稀疏专家混合（MoE）。**每个 MoE 层提供 512 个路由专家外加 1 个共享专家，采用 top-k=10 路由。

## 功能支持

每个 Qwen3.8 请求需要维护三种形式的服务状态：全注意力层的 KV 缓存、GDN 层的循环状态，以及 GDN 卷积窗口。下述功能必须在前缀缓存、投机解码和 PD 分离之间一致地管理这三种状态。


### 面向 GDN 状态的 ReplaySSM

MTP 验证给 GDN 层带来了状态恢复问题。验证多个草稿 token 时，每一层都会原地更新其循环状态，但只有对应于已接受前缀的状态才应被提交。Qwen3.8 采用 [ReplaySSM](https://tridao.me/blog/2026/replayssm/) 解决这一问题。我们在[上一篇博客](https://www.lmsys.org/blog/2026-07-27-kimi-k3-day0-support#replayssm-raw-input-replay-for-the-kda-state)中详细描述过这一原始输入重放机制。验证期间，它记录循环输入，而不是在每个草稿位置对完整 GDN 状态做快照。一旦采样器确定了接受长度，一个 fold 内核便从已提交的检查点重放被接受的前缀，并原地推进状态。

我们将记录路径集成进了 FlashInfer 面向 BF16 状态的 CuTe DSL GDN MTP 内核。验证 prologue 已在寄存器中持有所需的数值，因此 ReplaySSM 只是增加了相应的环形缓冲区写入。它使验证结果逐比特不变，且未带来可测量的验证吞吐回退。借助同一条可变状态缓存路径，MTP 可以与前缀缓存、重叠调度和 PD 分离组合使用。

### 预填充-解码分离（PD 分离）

PD 分离通过一个带类型的注册表将全部三种状态从预填充 worker 传输到解码 worker。每个注册的处理器负责搬运其对应的状态，包括 KV 缓存、GDN 循环状态和 GDN 卷积窗口。每个卷积窗口的 `q`、`k`、`v` 子块在张量并行各 rank 间独立分片，因此传输层需要按目标布局对它们进行切片与重组。

同一负载还携带 MTP 草稿模型的 KV 缓存、隐藏状态和 top-k 元数据，使投机解码得以在解码 worker 上继续。当预填充与解码使用不同的注意力分片布局时，GPU 暂存缓冲区会将逐层切片合并为每个 chunk 一次的大块 RDMA 传输，而不是为每个切片单独发起传输。

### 基数树缓存与 HiCache

Qwen3.8 使用 SGLang 的[统一基数树缓存（Unified Radix Cache）](https://www.lmsys.org/blog/2026-08-11-unified-radix-cache)，为全注意力 KV 和 GDN 状态同时启用前缀缓存。`FULL` 组件管理全注意力 KV 缓存，`MAMBA` 组件管理 GDN 检查点。每个 GDN 检查点将循环状态与卷积窗口打包在一起。

在前向计算修改共享 GDN 检查点之前，写时复制（copy-on-write）会将其恢复到该请求的私有槽位。SGLang 在预填充 chunk 边界和固定解码间隔处创建新检查点。一个共享缓存控制器在设备层与主机层之间协调 KV 与 GDN 两个组件，使前缀缓存与 HiCache 能够与 MTP 和 PD 分离组合使用。

## 分块流水线并行预填充

在本文测量的配置中，解码与预填充各自偏好不同的并行布局。对于解码，我们使用宽专家并行（wide-EP）将全部 512 个专家分片到各 rank。下文两种 wide-EP 配置均启用了 EPLB。在测得的 8K 预填充工作点上，包含 dispatch 与 combine 集合通信的 wide-EP 配置吞吐低于纯 PP。PD 分离让两个阶段可以运行在不同的 worker 上并采用不同布局。

采用纯流水线并行预填充时，每个阶段拥有 92 层中一段连续的层切片，并在一个 rank 上执行该切片，使用全宽 GEMM，无需 MoE dispatch、combine 或 EPLB。阶段间的主要通信是每个阶段边界处的激活值传输。将请求切分为多个 chunk，可以让 chunk *i* 的交接与 chunk *i+1* 的计算重叠，chunk 就这样首尾相接地流过各阶段。

<img src="/images/blog/qwen3-8-day0-support/fig-chunked-pp-prefill.svg" alt="分块流水线并行预填充：chunk 首尾相接地流过各阶段，每次交接与下一个 chunk 的计算重叠" width="100%">

在所示工作点上测得的 8K 预填充性能，单位为每 GPU 每秒输入 token 数：

| 检查点 | 分块 PP 预填充 | Wide EP + EPLB | 加速比 |
|---|---:|---:|---:|
| FP8，16 GPU | **5231** (PP16) | 3421 | **1.53×** |
| NVFP4，8 GPU | **8363** (PP8) | 5151 | **1.62×** |

### 流水线并行预填充与 MTP

流水线化预填充与投机解码过去是互斥的，这意味着只能在上述吞吐量与下文的单用户速度之间二选一。障碍是结构性的：在流水线并行下，嵌入层（embedding）位于第一个阶段，LM 头位于最后一个阶段，没有任何单一阶段同时持有两者，而草稿头（draft head）却两者都需要。我们把草稿头放在最后一个阶段，并自备一份它接收不到的那一半的副本，将草稿 KV 与目标 KV 一道经 PD 边界暂存传递，且让不承载草稿的 rank 不持有草稿 KV 池。这样，预填充拓扑就成了一个自由变量：无论预填充 worker 如何切分，解码 worker 都能保留其投机解码。

### 暂存缓冲区：解耦预填充与解码布局

PP16 预填充 worker 与 wide-EP 解码 worker 在 KV 的划分方式上并不一致，若强行要求共享 TP 布局，就会把预填充拖回解码的拓扑，牺牲上述全部收益。

暂存缓冲区改变了双方需要达成一致的约定。预填充将完成的 chunk 写入暂存缓冲区，并发布逐对端（per-peer）的 watermark；解码从缓冲区中分散读取到它所使用的任意布局，逐 chunk 预取。约定的是一个 chunk 索引和一个 watermark，而非某种划分方式，这使得传输能与剩余预填充重叠进行。因此，预填充:解码比例、流水线深度与解码 EP 宽度可以分别独立调节。同一路径也承载草稿 KV。

## 性能

### 8K/1K 下的帕累托曲线

以下所有数据均为 GB300 上 8,192 输入 / 1,024 输出负载的结果。图中包含 NVFP4 与 FP8 的 PD 分离结果，以及 FP8 的聚合 TP 结果。吞吐量按每张活跃模型服务 GPU 每秒处理的总（输入 + 输出）token 数计算；单用户速度按每请求每秒输出 token 数计算。

<img src="/images/blog/qwen3-8-day0-support/fig-pareto-8k1k.svg" alt="FP8 与 NVFP4 检查点在 8,192 输入 / 1,024 输出 token 下的聚合与 PD 分离服务结果：每 GPU 总 tok/s 对每用户输出速度" width="100%">

代表性端点的标签标注活跃/已分配 GPU 数；`P` 与 `D` 表示活跃的预填充/解码划分。PP6 最大吞吐点使用了 24 张已分配 GPU 中的 20 张活跃 GPU（`12P + 8D`），TPS/GPU 按活跃模型服务 GPU 数计算。

此处展示的 PD 分离数据点使用 3.3 的强制接受长度。FP8 聚合数据点报告的是各自运行中实测的 TPOT（每 token 生成时间）。各端点数据如下：

| 检查点 | 最大吞吐量（PD 分离） | 低延迟端点 |
|---|---|---|
| NVFP4（2×PP6 预填充，DP2-attn / TP4 / EP8 解码） | **5,126** tok/s/GPU @ 36 tok/s/user | PD: **108** tok/s/GPU @ **334** tok/s/user |
| FP8（2×PP16 预填充，DP4-attn / TP4 / EP16 解码） | **3,532** tok/s/GPU @ 30 tok/s/user | 聚合 CC1: **220** tok/s/GPU @ **362** tok/s/user |

NVFP4 的峰值配置由两个 PP6 预填充 worker 向一个 DP2-attn / TP4 / EP8 解码 worker 供数。在低延迟端，NVFP4 使用 PD 分离的 PP2×TP4 预填充 worker 搭配 TP16 解码 worker（334 tok/s/user），而 FP8 使用并发为 1 的 TP16 聚合 worker（362 tok/s/user）。

在同条件的双 PP6 NVFP4 基线上，加入 MTP 使吞吐提升 +10.0%，单用户速度提升至 2.33 倍。更新后的 5,126 数据点不用于该同条件对比。这种不对称正是预期的形态：在饱和的解码 worker 中，每步生成的 token 数大致为 `running_requests × draft_tokens`，由显存预算固定，因此投机解码主要是把固定的步数预算转化为每请求更少但更长的步。

### 内核优化

- **MoE finalize、AllReduce 与 RMSNorm 融合。**在隐藏维度为 8,192、top-10 路由的条件下，finalize 输入缓冲区在预填充期间会变得很大。输入序列长度为 8K 时，`8192 × 10 × 8192 × sizeof(bfloat16)` 需要 1.25 GiB，使 finalize 最多占预填充时间的 10%。我们利用程序化依赖启动（Programmatic Dependent Launch，PDL）链接与持久化执行开发了计算与通信融合内核。在测试配置中，它们将端到端延迟与吞吐改善了 10% 以上。实现见 [FlashInfer PR #4358](https://github.com/flashinfer-ai/flashinfer/pull/4358)。

- **上下文并行 GDN 预填充。**该内核将序列切分为多个 chunk 并行处理，提升长序列、小 batch 场景下的 GPU 利用率，使预填充性能提升 2% 到 3%。实现细节见 [FlashInfer issue #3491](https://github.com/flashinfer-ai/flashinfer/issues/3491)。

- **低延迟单 GEMM 路径。**小 GEMM 是延迟的重要来源，尤其当它们需要单独的 Split-K 归约内核时。优化后的单 GEMM 路径带来最高 1.5 倍的内核级加速和约 4% 的端到端改进。见 [FlashInfer PR #4266](https://github.com/flashinfer-ai/flashinfer/pull/4266)。

- **GDN 解码算子融合。**我们为低延迟张量并行配置融合了 SplitKV 重排与 Conv1D 操作，使端到端解码性能提升 2% 到 3%。见 [SGLang PR #32919](https://github.com/sgl-project/sglang/pull/32919)。

## 强化学习：在原生 NVFP4 基座上进行 LoRA 训练

Qwen3.8 的 Day-0 强化学习（RL）是基于 [Miles](https://github.com/radixark/miles) 的共置 LoRA 训练：BF16 Megatron 训练器与原生 NVFP4 SGLang rollout 引擎共享同一批 64 台 GB300，在注意力投影上挂载 rank 为 32 的适配器并用 GRPO 训练。我们通过一轮简短的 GSM8K 训练验证了这一配置：奖励与评测分数稳步上升，同时训练/rollout KL 保持平稳。

<img src="/images/blog/qwen3-8-day0-support/fig-rl-gsm8k.png" alt="Qwen3.8 在 GSM8K 上的 LoRA RL：评测分数、rollout 奖励与训练/rollout KL" width="100%">

## 致谢

这项工作是 RadixArk 的 SGLang 与 Miles 团队、Qwen、Alibaba Bailian（阿里云百炼）、NVIDIA 和 AMD 的合作成果。

**SGLang 社区**：Qiaolin Yu, Yuhao Yang, Xinyuan Tong, Ke Bao, Zijie Xia, Yi Sun, Mao Cheng, Yueming Yuan, Mingyi Lu, Haoguang Cai, Banghua Zhu, Ying Sheng

**Qwen**：Yi Zhang, Zheng Li

**Alibaba Bailian**：Tao Lan 及其同事

**AMD**：Jacky Cheng, Zijie Chen, Hai Xiao

**NVIDIA**：NVIDIA 与 SGLang 在 GDN、GEMM、GQA 和 MoE 通信的内核上展开合作，包括上述通信融合。双方团队还共同完成了 Qwen3.8 性能结果中使用的并行配置。
