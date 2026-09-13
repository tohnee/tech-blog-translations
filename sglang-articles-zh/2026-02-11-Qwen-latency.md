---
title: "释放算力：Qwen3 与 Qwen3-VL 在 AMD MI300X 系列上的极致延迟优化"
title_en: "Unleashing Computational Power: Ultimate Latency Optimization of Qwen3 and Qwen3-VL on AMD MI300X Series"
author: "The Qwen C-end Infrastructure Engineering Team & The AMD AI Framework Team"
date: "February 11, 2026"
previewImg: /images/blog/qwen_amd_latency/preview.png
source: https://lmsys.org/blog/2026-02-11-Qwen-latency/
translated: 2026-09-12
---

# 释放算力：Qwen3 与 Qwen3-VL 在 AMD MI300X 系列上的极致延迟优化

> 原文：[Unleashing Computational Power: Ultimate Latency Optimization of Qwen3 and Qwen3-VL on AMD MI300X Series](https://lmsys.org/blog/2026-02-11-Qwen-latency/) · LMSYS Blog · The Qwen C-end Infrastructure Engineering Team & The AMD AI Framework Team

## 1. 引言


Qwen 是阿里云 Qwen 团队开发的一系列大规模、高性能大语言模型（LLM）。从第一代到最新的第三代旗舰模型，各代 Qwen 模型都经过了专门的训练与精细调优，具备强大的指令遵循能力、面向交互式 AI 应用的高效可部署性，以及解决复杂任务的稳健表现。作为 Qwen3 家族的旗舰模型，Qwen3-235B 和 Qwen3-VL-235B 实现了全方位的多维度提升，并已在 Qwen APP 中大规模部署。


近几个月来，Qwen C 端基础设施工程团队与 AMD AI 框架团队展开合作，在基于 SGLang 框架的 AMD Instinct<sup>TM</sup> MI300X 系列 GPU 平台上，为 Qwen3-235B 和 Qwen3-VL-235B 实现了极致的延迟优化方案，在性能、精度和稳定性方面均取得了显著突破。
* **对于 Qwen3-235B**：与基线相比，首 token 延迟（TTFT）优化了 1.67 倍，每 token 生成时间（TPOT）优化了 2.12 倍。
* **对于 Qwen3-VL-235B**：与基线相比，首 token 延迟（TTFT）优化了 1.62 倍，每 token 生成时间（TPOT）优化了 1.90 倍。


AMD Instinct<sup>TM</sup> MI300X 系列 GPU 基于 CDNA<sup>TM</sup> 3 架构，单卡配备 192 GB HBM3 内存——足以支持超过 700 亿参数模型的推理。结合 5.3 TB/s 的内存带宽、256 MB Infinity Cache，以及 Matrix Core 对 FP8 和 PTPC 量化的原生支持，该平台具备卓越的性能与性价比，是大规模 LLM 集群部署的理想选择。


本文详细阐述了两个团队共同探索并落地的性能优化技术，核心聚焦于实现超低延迟推理。所有优化工作均已开源：[[Tracking][Performance][AMD] Qwen3 & Qwen3-VL Latency Optimization on AMD Instinct<sup>TM</sup> MI300X Series GPUs](https://github.com/sgl-project/sglang/issues/18466)。

<p align="center">
  <img src="/images/blog/qwen_amd_latency/QwenVL.jpg" width="80%">
</p>
<p align="center" style="color:gray; text-align: center;"><em>图 1. Qwen3-VL 模型结构（来自 Qwen3-VL 论文）</em></p>


## 2. 延迟优化技术


### 2.1 Qwen3-235B 的延迟优化


Qwen3-235B 的推理计算流程如图 2 所示。下面几节将详细阐述针对这些关键组件的优化。

<p align="center">
  <img src="/images/blog/qwen_amd_latency/qwen_optimization_flowchart.png" width="100%">
</p>
<p align="center" style="color:gray; text-align: center;"><em>图 2. Qwen3-235B 模型推理计算流程图</em></p>



#### 2.1.1 GEMM 量化策略

<p align="center">
  <img src="/images/blog/qwen_amd_latency/PTPC.png" style="display: block; margin: 20px auto 0; width: 40%; max-width: 100%; height: auto;">
</p>
<p align="center" style="color:gray; text-align: center;"><em>图 3. PTPC-FP8：逐 token 激活、逐通道权重量化（Per-Token-Activation, Per-Channel-Weight Quantization）</em></p>


量化对于加速 LLM 推理至关重要。本工作采用 **PTPC**（Per Token Activation, Per Channel Weight，逐 token 激活、逐通道权重）量化方案——一种同时对模型权重和激活施加的 FP8 量化方法，其核心原理如图 3 所示。该方案对激活采用逐 token 量化、对权重采用逐通道量化，与传统的逐张量（per-tensor）FP8 量化相比，能够获得更高的量化精度并减少信息损失。


与标准 BlockScale FP8 量化相比，PTPC 量化在保持相当精度的同时具备更优的计算效率。BlockScale 的固定块大小常常与硬件 GEMM 单元的最佳 tile 尺寸不对齐，从而引入数据切分与重排的额外开销。相比之下，PTPC 的细粒度设计摆脱了固定块约束，天然契合硬件 GEMM 单元的原生计算粒度；其逐通道权重量化也能更好地匹配现代加速器的通道并行计算架构。再叠加低精度计算带来的吞吐收益，基于 PTPC 的 GEMM 显著提升了硬件利用率。


在 AMD ROCm<sup>TM</sup> 平台上的实验结果表明，PTPC FP8 GEMM 量化的性能比 BlockScale FP8 高出 15%–30%，在小矩阵和不对齐矩阵的部署场景下，延迟降低尤为明显。


#### 2.1.2 并行策略


在对 Qwen3-235B 实施专家并行（EP）的实验过程中，我们观察到某些数据集上存在专家热点问题（如图 4 所示，例如第 57 层的 EP rank 10/120/216 是被频繁访问的热点专家）。这种负载不均衡会在推理过程中造成延迟瓶颈。

<p align="center">
  <img src="/images/blog/qwen_amd_latency/hot_expert.png" width="80%">
</p>
<p align="center" style="color:gray; text-align: center;"><em>图 4. 专家热点分布</em></p>



在 Qwen 的生产场景中，TTFT 和 TPOT 是关键性能指标。实测证实，MoE 模型推理通常是内存带宽受限（memory-bound）的。AMD Instinct<sup>TM</sup> MI300X 系列的高带宽 HBM 有效缓解了张量并行（TP）中的 I/O 瓶颈，从而大幅降低推理延迟。


对于完整的 Qwen3-235B 模型（包括其 MoE 结构），我们采用 TP8 张量并行配置，并结合 PTPC FP8 量化来实现极致低延迟。具体而言，PTPC 的逐通道权重量化配备 192 个独立缩放因子，使 MoE 模块与 TP8 无缝兼容，保证了大规模并行部署的稳定与高效。


在低并发、极致延迟敏感的场景中，TP8 将模型权重分布到 8 张 GPU 上，降低了单卡的权重加载与内存延迟。在架构层面，它还缓解了 MoE 专家负载不均衡的问题，为进一步实现超低延迟推理夯实了基础。


#### 2.1.3 注意力模块优化

**（1）优化的 KV 缓存布局**

对于注意力模块，我们集成了 AMD AITER 库中针对专用 KV 缓存布局定制的高性能 MHA 与分页注意力（PagedAttention）算子。该布局定义如下：


* k_cache: [num_blocks, num_kv_heads, head_dim // x, block_size, x]
* v_cache: [num_blocks, num_kv_heads, block_size // X, head_dim, X]


这种布局使内存访问模式与 AMD CDNA<sup>TM</sup> 3 架构对齐，大幅提升了 PagedAttention 的内存效率。在解码阶段，无需为布局转换进行额外的设备间（D2D）拷贝，从而消除了冗余开销（图 5）。与标准 KV 缓存布局 [num_blocks, num_kv_heads, head_dim, block_size] 相比，该优化在降低推理延迟的同时，将解码吞吐量提高了 15%–20%。

<p align="center">
  <img src="/images/blog/qwen_amd_latency/K_Cache_Layout.png" style="display: block; margin: 20px auto 0; width: 40%; max-width: 100%; height: auto;">
</p>
<p align="center" style="color:gray; text-align: center;"><em>图 5. K Cache 布局分布</em></p>


**（2）数据类型优化**
* 在**预填充（prefill）**阶段：对 MHA 的 query、key、value 激活应用逐张量 FP8 量化。
* 在**解码**阶段：query 使用 BF16，而 KV 缓存仍以逐张量 FP8 存储（与预填充一致）。


这种混合精度配置在保持精度和性能的同时，降低了 HBM 占用。


#### 2.1.4 MoE 优化


针对低并发负载，我们在 AITER 中对 MoE 算子从四个关键维度进行了深度优化：
* **负载均衡**：在低并发推理时对计算单元（CU）进行细粒度任务调度，使各 CU 几乎同步执行，消除空闲周期，最大化硬件利用率。
* **计算效率**：针对 K 维度进行硬件感知的循环调优，消除冗余操作，显著提升吞吐量。
* **内存效率**：优化原子内存访问模式，提高 L2 缓存命中率，缓解内存带宽瓶颈。
* **自动调优**：在手工优化之后，使用自动化调优工具搜索最优算子配置，进一步榨取性能。


值得注意的是，负载均衡与细粒度调度在 LLM 解码期间带来了尤为显著的性能收益，最终**将 MoE 模块性能提升了 2 倍**。


#### 2.1.5 算子融合优化

我们还融合了多个关键算子，包括：
* 模块 2：QKNorm + RoPE
* 模块 6 和 9：AllReduce + AddRMSNorm + per-token quant

算子融合减少了频繁的 HBM 访问，进一步降低了端到端推理延迟。


| 融合模式 | 融合前 (us) | 融合后 (us) | 加速比 |
| --- | --- | --- | --- | 
| QKNorm + RoPE | 11.6 | 5.1 | 127% |
| AllReduce + AddRMSNorm + Quant | 35 | 21 | 67% |

### 2.2 Qwen3-VL-235B 的优化

<p align="center">
  <img src="/images/blog/qwen_amd_latency/qwenvl_deployment.png" style="display: block; margin: 20px auto 0; width: 60%; max-width: 100%; height: auto;">
</p>
<p align="center" style="color:gray; text-align: center;"><em>图 6. SGLang 中的 Qwen3-VL-235B 部署</em></p>


与 Qwen3-235B 相比，Qwen3-VL-235B 引入了若干新的关键推理阶段：
* 多模态数据格式适配、预处理与跨模态对齐
* ViT 编码器执行、视觉 patch 嵌入与跨模态特征融合

这些扩展拉长了推理流水线，并涉及复杂的跨模态数据协同与特征适配，显著增加了单请求延迟。完整数据流如图 6 所示。相对于纯语言 LLM，Qwen3-VL 的主要开销来自三个方面：
* 主机侧多模态预处理
* 多模态数据传输
* GPU 侧 ViT 编码器计算


我们针对每个瓶颈设计了相应的延迟优化方案。


#### 2.2.1 基于 rocJPEG 的图像解码优化


在传统流水线中，主机侧的 JPEG 解码与张量转换非常缓慢：单张 720p 图像约需 27 ms。当输入多张图像或视频帧时，延迟会迅速增长，严重制约推理效率。


为了加速解码、降低端到端延迟，我们将 rocJPEG——AMD 高性能 GPU 加速 JPEG 解码 SDK——集成为 torchvision 的后端。当收到 JPEG 输入时，SGLang Tokenizer 的图像解码器调用 torchvision API，通过 rocJPEG 将解码卸载到 GPU（图 7）。实测表明，单张 720p 图像的解码延迟降至约 4 ms，带来了 **约 7 倍的加速**。

<p align="center">
  <img src="/images/blog/qwen_amd_latency/rocjpeg_flowchart.png" width="100%">
</p>
<p align="center" style="color:gray; text-align: center;"><em>图 7. rocJPEG 解码流程图</em></p>

#### 2.2.2 多模态数据传输优化


在 SGLang 中，Tokenizer 与 Scheduler 通常运行在独立进程中。预处理后的多模态数据必须通过 IPC 传输给 Scheduler。传统的基于 CPU 的 gloo:broadcast 对大型多模态数据而言效率低下（图 8）。

<p align="center">
  <img src="/images/blog/qwen_amd_latency/VLM_host_overhead.png" width="100%">
</p>
<p align="center" style="color:gray; text-align: center;"><em>图 8. 多模态传输与图像哈希编码的主机开销</em></p>


ROCm<sup>TM</sup> 后端支持 **CUDA IPC**，可实现无需 CPU 中转的 GPU 到 GPU 直接数据传输。这消除了冗余的 CPU-GPU 拷贝，大幅降低了多模态传输延迟，如图 9 所示。此外，我们还将图像哈希（图 6）卸载到 GPU 上执行，进一步压缩了开销。

<p align="center">
  <img src="/images/blog/qwen_amd_latency/cuda_ipc.png" style="display: block; margin: 20px auto 0; width: 50%; max-width: 100%; height: auto;">
</p>
<p align="center" style="color:gray; text-align: center;"><em>图 9. ROCm 后端上的 CUDA IPC
</em></p>


#### 2.2.3 ViT 的数据并行


视觉 Transformer（ViT）模块负责对图像和视频进行视觉特征编码。然而对于高分辨率输入，由于基于 patch 的分词方式，它会成为严重的计算受限（compute-bound）瓶颈：
* 输入被切分为固定大小的 patch（例如 16×16）
* 序列长度随分辨率呈平方级增长
* 完整自注意力的复杂度为 O(N<sup>2</sup>)

一张 1280×1280 的图像会生成约 4,800 个 token（与原文修正一致：960×1280 → 4,800 tokens），产生超过 2,300 万次注意力交互。在涉及大批量高分辨率图像或长视频的极端场景下，token 数量可超过 1M，使注意力复杂度达到 O(10<sup>12</sup>)。这会导致内存消耗爆炸、延迟极高，且硬件利用率低下。

为了缓解这些问题，我们对 ViT 模块应用数据并行（DP）：多图输入被切分后，在多张独立 GPU 上并行处理（图 6）。这一策略分散了计算负载，降低了单 GPU 压力。在每请求 5 张图像（960×1280）的实验中，我们观察到 3%–4% 的性能提升。性能收益随输入图像和视频数量的增加而扩大。


## 3. 实验与基准测试


### 3.1 实验设置


#### 3.1.1 硬件


我们基于 SGLang 推理引擎，将系统部署在配备 8 张 GPU 卡的单个 AMD MI308 节点上。本文介绍的优化技术具有**通用性和可移植性**，可直接应用于其他基于 **CDNA<sup>TM</sup> 3 架构**的 AMD 平台。


#### 3.1.2 模型权重


我们使用 PTPC-FP8 量化方案，相应的模型权重可在 [Qwen3-235B](https://huggingface.co/RedHatAI/Qwen3-235B-A22B-FP8-dynamic) 和 [Qwen3-VL-235B](https://huggingface.co/RedHatAI/Qwen3-VL-235B-A22B-Instruct-FP8-dynamic) 获取。


#### 3.1.3 测试场景


这些优化面向**低延迟推理场景**，评测设置如下：
* **Qwen3-235B**：单请求，输入序列长度（ISL）= 8000，输出序列长度（OSL）= 500。
* **Qwen3-VL-235B**：单请求，文本 ISL = 8000，每请求 5 张图像（960×1280），OSL = 500。


### 3.2 CUDA IPC 配置 


为了启用 **GPU 直接 IPC** 以实现高效的多模态数据传输，用户可以设置以下环境变量。变量取值可根据不同场景调整。
* export SGLANG_USE_CUDA_IPC_TRANSPORT=1
* export SGLANG_VLM_CACHE_SIZE_MB=8192

实验结果表明，对于 5 张 960×1280 分辨率的图像，启用 CUDA IPC 可**显著降低数据传输延迟**，与 gloo:broadcast 相比峰值降低可达 2 秒。

### 3.3 性能回顾


对于 Qwen3-235B，性能优化里程碑如图 10 所示。首 token 延迟（TTFT）优化了 1.67 倍，从 756.54ms 降至 450.59ms。每 token 生成时间（TPOT）优化了 2.12 倍，从 26.44ms 降至 12.44ms。

<p align="center">
  <img src="/images/blog/qwen_amd_latency/qwen_latency.png" width="70%">
</p>
<p align="center" style="color:gray; text-align: center;"><em>图 10. Qwen3-235B TTFT 与 TPOT 优化里程碑
</em></p>



对于 Qwen3-VL-235B，性能优化结果如图 11 所示。首 token 延迟（TTFT）优化了 1.62 倍，从 1764ms 降至 1084.59ms。每 token 生成时间（TPOT）优化了 1.90 倍，从 23.7ms 降至 12.48ms。

<p align="center">
  <img src="/images/blog/qwen_amd_latency/qwenvl_latency.png" width="70%">
</p>
<p align="center" style="color:gray; text-align: center;"><em>图 11. Qwen3-VL-235B TTFT 与 TPOT 优化里程碑
</em></p>

## 4. 参考资料
* [Qwen3：Thinker Deeper, Act Faster](https://qwen.ai/blog?id=qwen3)
* [AITER](https://github.com/ROCm/aiter)
* [SGLang 文档](https://docs.sglang.io/)
* [rocJPEG](https://github.com/ROCm/rocJPEG)
