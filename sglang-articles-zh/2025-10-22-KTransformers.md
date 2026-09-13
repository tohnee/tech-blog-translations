---
title: "使用 KTransformers CPU 算子加速 SGLang 混合推理"
title_en: "Accelerating Hybrid Inference in SGLang with KTransformers CPU Kernels"
author: "KVCache.AI and Approaching AI"
date: "October 22, 2025"
previewImg: /images/blog/ktransformers/primary.png
source: https://lmsys.org/blog/2025-10-22-KTransformers/
translated: 2026-09-12
---

# 使用 KTransformers CPU 算子加速 SGLang 混合推理

> 原文：[Accelerating Hybrid Inference in SGLang with KTransformers CPU Kernels](https://lmsys.org/blog/2025-10-22-KTransformers/) · LMSYS Blog · KVCache.AI and Approaching AI

## 背景：稀疏 MoE 模型的混合推理

以 **DeepSeek-V3** 为代表的现代专家混合（MoE）语言模型拥有数千亿参数，但每个 token 仅激活其中一小部分专家。

这种**稀疏激活**模式使 MoE 模型天然适合 **CPU/GPU 混合推理**：稀疏激活的专家可以高效地运行在内存容量大的 CPU 上，而稠密且计算密集的组件——注意力与共享专家——则在带宽和吞吐量更高的 GPU 上执行。

<img src="/images/blog/ktransformers/heterogeneous_computing.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 70%"></img>

这种混合设计使万亿参数模型能够部署在 GPU 显存有限的单台机器上，为科研和私有化应用提供本地推理能力。

然而，由于协调开销与算力利用不足等问题，充分挖掘 CPU 和 GPU 的潜力仍然充满挑战，这些因素限制了有效吞吐量。

## KTransformers：释放 MoE 模型 CPU/GPU 混合推理的全部潜力

为解决上述问题，MadSys @ Tsinghua 与 Approaching.AI 打造了 **KTransformers** 项目（发表于 SOSP'25），提出了一系列优化，使 MoE 推理中的 CPU/GPU 协作效率大幅提升。

其改进主要分为三个方面：

### 1. AMX 专用 CPU 算子

KTransformers 采用针对 Intel AMX 优化的算子重新设计了 CPU 计算，并配合感知分块（tiling-aware）的内存布局，使权重存储与缓存层级对齐。它还支持在 AMX（面向高负载 prefill 工作负载）与 AVX-512（面向轻量解码）之间动态切换。在单个 Xeon 插槽上，AMX 优化算子的持续吞吐量可达 **21.3 TFLOPS**，较 PyTorch 原生实现快 **3.9×**。这直接转化为 prefill 阶段显著更高的 CPU 侧专家吞吐量，以及混合推理模式下更高的整体 token 吞吐量。

### 2. 高效的设备协同

为了降低 CPU 与 GPU 之间的协同成本，KTransformers 引入了 NUMA 感知的张量并行和基于 CUDA Graph 的调度。

NUMA 感知的张量并行将专家权重的分片放置在每个 NUMA 节点的本地内存中，使计算尽量在本地完成，避免昂贵的跨 NUMA 内存访问；这一设计在双路服务器上带来了最高 **63%** 的解码吞吐量提升。

CUDA Graph 集成将混合的 CPU/GPU 执行捕获为连续的图。为了保证捕获的稳健性，KTransformers 采用异步任务调度，使 CPU 任务和数据传输不会在捕获的图中制造「断点」。通过这种方式捕获工作负载，GPU 算子启动开销从 **20% 以上**降至**几乎为零**。

这些优化共同确保两种设备都能以极小的同步延迟运行。

### 3. 专家延迟执行（Expert Deferral）：重叠模型执行

KTransformers 还引入了专家延迟执行（Expert Deferral）机制，对跨层的专家执行顺序进行重排。部分专家的计算被推迟到后续阶段执行，从而使 CPU 上的专家计算能够与 GPU 上的注意力处理重叠进行。

<img src="/images/blog/ktransformers/expert_deferral.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 70%"></img>

由于现代 Transformer 采用残差连接，天生就能容忍中间计算的少量延迟。因此，推迟部分专家计算以增强调度灵活性，只会带来模型行为上的轻微变化。

该机制提升了两种设备的并发利用率，可带来最高 **1.45×** 的解码吞吐量提升，且精度波动低于 0.5%。

## 将 KTransformers 集成到 SGLang

SGLang 现已将 KTransformers 作为后端库集成，以实现高效的 CPU/GPU 混合推理，为 MoE 模型组合了 GPU 张量并行与 CPU/GPU 混合专家并行。该集成支持跨异构设备的推理：KTransformers 提供高度优化的基于 AMX 的 CPU 算子，与 GPU 执行无缝协同。

KTransformers 专注于单 GPU 配置与高效的 CPU 协作，而 SGLang 擅长跨多 GPU 扩展，这在**高并发场景**下尤为有利。在混合模式下，多个 GPU 可以处理更大的请求上下文并执行快速的注意力计算，同时专家在 CPU 和 GPU 之间被智能调度——将频繁使用的「热」专家存放在 GPU 上，以缓解 CPU 的计算和带宽压力。

借助这一联合设计，各种硬件配置的用户都能充分利用可用资源，获得更好的吞吐量、可扩展性和性价比。

我们已完成概念验证实现，与 SGLang 完整集成的[路线图](https://github.com/sgl-project/sglang/issues/11425)正在推进中。

## 安装

要在 SGLang 中使用 KTransformers 混合推理，你需要同时安装 SGLang 和 KTransformers CPU 算子库（`kt-kernel`）。

### 前置条件

在安装之前，请确保系统满足以下要求：

- **CUDA**：12.1 及以上版本，并正确配置 PATH
- **操作系统**：Linux x86_64
- **编译器**：gcc、g++ >= 11
- **构建工具**：CMake >= 3.25（注意：Ubuntu 22.04 LTS 自带的 CMake 版本可能过旧）
- **Python**：Python 3.11（通过 Miniconda3 或 Anaconda3）

### 第 1 步：安装 SGLang

按照官方 [SGLang 安装指南](https://docs.sglang.io/get_started/install.html)安装 SGLang：

```bash
pip install "sglang[all]"
```

### 第 2 步：安装 KTransformers CPU 算子

KTransformers CPU 算子（`kt-kernel`）为混合推理提供经过 AMX 优化的计算能力。详细的安装说明与故障排查请参考 [kt-kernel 官方安装指南](https://github.com/kvcache-ai/ktransformers/blob/main/kt-kernel/README.md)。

## 使用示例

### 下载模型

针对 KTransformers 混合推理优化的 DeepSeek-R1 模型（同时包含 GPU 权重和 CPU 权重）可从 [Approaching AI 的 ModelScope 主页](https://modelscope.cn/profile/ApproachingAI2024)下载。

### 启动服务器

要启动一个启用 KTransformers 混合推理的 SGLang 服务器，可以使用以下命令：

```bash
python -m sglang.launch_server \
  --host 0.0.0.0 \
  --port 30000 \
  --model /path/to/gpu-weight \
  --kt-amx-weight-path /path/to/cpu-weight \
  --kt-cpuinfer 80 \
  --kt-threadpool-count 2 \
  --kt-num-gpu-experts 200 \
  --kt-amx-method AMXINT4 \
  --attention-backend triton \
  --trust-remote-code \
  --mem-fraction-static 0.98 \
  --chunked-prefill-size 4096 \
  --max-running-requests 37 \
  --max-total-tokens 37000 \
  --served-model-name DeepSeek-R1-0528-FP8 \
  --enable-mixed-chunk \
  --tensor-parallel-size 8 \
  --enable-p2p-check \
  --disable-shared-experts-fusion
```

### 关键参数

- `--kt-amx-weight-path`：CPU 优化模型权重的路径。这些权重经过预量化，并已按高效 AMX 计算所需的格式组织。
- `--kt-cpuinfer`：专用于专家推理的 CPU 核心数（例如双路服务器使用 80 核）。
- `--kt-threadpool-count`：用于 CPU 并行执行的线程池数量。双路 NUMA 配置通常设为 2。
- `--kt-num-gpu-experts`：保留在 GPU 上的「热」专家数量。更多的 GPU 专家可以减轻 CPU 的计算压力，但需要额外的显存。请根据 GPU 容量和负载特征进行调整。
- `--kt-amx-method`：CPU 算子优化方法。对 int4 量化模型使用 `AMXINT4`，以借助 Intel AMX 指令获得最大吞吐量。

### 硬件要求

要获得 KTransformers 混合推理的最佳性能：

- **CPU**：支持 AMX 的新一代 Intel Xeon 处理器（如 Sapphire Rapids 或更新型号），以获得最大的 CPU 专家吞吐量。
- **内存**：足以容纳全部专家权重的 DDR5 内存（DeepSeek-V3 规模的模型通常需要 500GB 以上）。
- **GPU**：一块或多块显存充足、足以容纳注意力层、共享专家以及部分路由专家的 GPU。
- **NUMA**：双路配置可借助 NUMA 感知的线程池分配获益（`--kt-threadpool-count 2`）。

服务器启动后，你就可以通过 OpenAI 兼容 API 端点 `http://0.0.0.0:30000` 发送推理请求。

## 基准测试结果（预览）

### 单 GPU + CPU 性能

原生 KTransformers 在单 GPU + CPU 配置上进行了细致的性能评估。在相同配置下，集成 KTransformers 的 SGLang 取得了与原生 KTransformers 相当的性能。

评估环境为一台双路 Intel® Xeon® Platinum 8452Y 服务器（36 核 × 2，1 TB DDR5 × 2），全精度模型使用 NVIDIA A100（40 GB），量化模型使用 RTX 4080（16 GB）。

<img src="/images/blog/ktransformers/prefill_performance.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 70%"></img>

在 **prefill 阶段**，得益于 AMX 优化的 CPU 算子，KTransformers 在所有 prompt 长度下都稳定优于两个基线，加速比最高可达 **20×**。

<img src="/images/blog/ktransformers/decode_performance.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 70%"></img>

在 **decode 阶段**，KTransformers 同样优于两个基线，性能提升主要归功于 CPU/GPU 协调开销的降低，加速比最高可达 **4×**。

### 多 GPU + CPU 性能

我们进一步评估了将 KTransformers 集成到 SGLang 后所获得的多 GPU + CPU 混合推理能力。具体而言，我们在配备 8× L20 GPU 和双路 Intel Xeon Gold 6454S CPU 的系统上测试了 int4 量化的 DeepSeek-V3，使用的负载平均输入长度为 128 token、输出长度为 512 token。

<img src="/images/blog/ktransformers/multigpu_performance.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 70%"></img>

上表展示了不同并发水平和不同 GPU 数量下的总吞吐量（tokens/s）。可以看到，在单并发条件下，8 GPU 配置相比 1 GPU 配置的提升有限（仅增加 26%）。而在 8 路并发下，同样的 8 GPU 配置相比 1 GPU 取得了 **264%** 的吞吐量增益，展现出出色的实用性——每个请求平均可达到接近 20 tokens/s。这一提升主要来自将更多专家放置到 GPU 上，从而减少了处于带宽瓶颈下的 CPU 内存访问。

#### NVIDIA L20 × 8 配置下的 ShareGPT 基准测试

我们进一步在由 **8× NVIDIA L20 GPU** 和 **Intel(R) Xeon(R) Gold 6454S CPU** 组成的 GPU 配置上评估了 SGLang + KTransformers 集成方案。基准测试对象为 **DeepSeek-R1-0528**（DeepSeek-R1 系列中的大规模 MoE 模型），使用 ShareGPT 数据集的 1000 个对话请求（301K 输入 token，188K 输出 token）。

**系统配置：**
- GPU：8× NVIDIA L20
- CPU：Intel(R) Xeon(R) Gold 6454S
- 模型：DeepSeek-R1-0528（FP8 量化的 MoE 模型）
- 数据集：ShareGPT（1000 个请求）

**基准测试命令：**

首先，启动 SGLang 服务器：

```bash
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
python -m sglang.launch_server \
  --host 0.0.0.0 \
  --port 30000 \
  --model models/DeepSeek-R1-0528-GPU-weight \
  --kt-amx-weight-path models/DeepSeek-R1-0528-CPU-weight \
  --kt-cpuinfer 60 \
  --kt-threadpool-count 2 \
  --kt-num-gpu-experts 200 \
  --kt-amx-method AMXINT4 \
  --attention-backend triton \
  --trust-remote-code \
  --mem-fraction-static 0.98 \
  --chunked-prefill-size 4096 \
  --max-running-requests 40 \
  --max-total-tokens 40000 \
  --served-model-name DeepSeek-R1-0528-FP8 \
  --enable-mixed-chunk \
  --tensor-parallel-size 8 \
  --enable-p2p-check \
  --disable-shared-experts-fusion
```

然后，在另一个终端中运行基准测试：

```bash
python -m sglang.bench_serving \
  --backend sglang \
  --host 127.0.0.1 \
  --port 30000 \
  --num-prompts 1000 \
  --model models/DeepSeek-R1-0528-GPU-weight
```

**性能结果：**

| 指标 | 数值 |
|--------|-------|
| 总 token 吞吐量 | 227.85 tok/s |
| 输出 token 吞吐量 | 87.58 tok/s |
| 请求吞吐量 | 0.46 req/s |
| 平均每 token 生成时间（ITL） | 431.61 ms |
| 每 token 生成时间中位数 | 299.18 ms |
| P99 每 token 生成时间 | 1935.13 ms |

这一配置表明，SGLang + KTransformers 能够有效利用消费级 GPU 进行混合推理，在万亿参数 MoE 模型上实现 **超过 220 tokens/s 的总吞吐量**。相对较低的每 token 生成时间（中位数 299ms）确保了交互式应用流畅的流式生成体验。

## 致谢

我们感谢社区中每一位为这项工作提供帮助的成员。

**KVCache.AI 团队**：Boxin Zhang, Jianwei Dong, Hongtao Chen, Weiyu Xie, Shaoyuan Chen, Chen Lin, Chengyu Qiu, Yuening Zhu, Jingqi Tang, Qingliang Ou, Yongwei Wu 和 Mingxing Zhang（来自清华大学 MadSys 团队）。

**Approaching AI**：Jiahao Wang, Ziwei Yuan, Yaochen Han, Jiaqi Liao, Xianglin Chen, Zhiyuan Ai, Yongsen Hu, Zhuo Wang, Daocheng Ye, Yanlong Wu, Yufeng Tian, Heng Guo, Hao Wu, Zirui Li, Yingqi Tian, Yue Qin, Xin Qu, Baijin Hao, Donghui Liu。

**SGLang 团队与社区**：感谢 Jingyi Chen, Shangming Cai, Lianmin Zheng, Yineng Zhang 以及其他众多成员为该 PR 提供的深入评审意见，以及他们为 SGLang 框架所做的贡献。

## 相关资源

代码仓库：https://github.com/kvcache-ai/ktransformers

SOSP25 论文：https://madsys.cs.tsinghua.edu.cn/publication/ktransformers-unleashing-the-full-potential-of-cpu/gpu-hybrid-inference-for-moe-models/
