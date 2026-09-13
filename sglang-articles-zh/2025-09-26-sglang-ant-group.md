---
title: "携手 SGLang：在 H20-96G 上服务 DeepSeek-R1 的最佳实践"
title_en: "Together with SGLang: Best Practices for Serving DeepSeek-R1 on H20-96G"
author: "Tianyu Zhang*, Peng Zhang*, Yusong Gao, Yun Zhang"
date: "September 26, 2025"
previewImg: /images/blog/ant-group-prac/logo.svg
source: https://lmsys.org/blog/2025-09-26-sglang-ant-group/
translated: 2026-09-12
---

# 携手 SGLang：在 H20-96G 上服务 DeepSeek-R1 的最佳实践

> 原文：[Together with SGLang: Best Practices for Serving DeepSeek-R1 on H20-96G](https://lmsys.org/blog/2025-09-26-sglang-ant-group/) · LMSYS Blog · Tianyu Zhang*, Peng Zhang*, Yusong Gao, Yun Zhang

## 引言

将 DeepSeek-R1 这类大规模专家混合（MoE）模型投入生产运营，需要仔细权衡延迟、吞吐量与成本。这一挑战在性能特征不均衡的硬件上尤为突出——例如 H20 GPU：它拥有很高的显存带宽，计算吞吐却相对较低。我们的目标是设计一套推理服务栈，既能达到高端 GPU 通常才能满足的严格 SLA，又能充分发挥 H20 的成本优势。

本报告概述了我们为实现这一目标所采用的实践。我们介绍了一套有别于常见做法的硬件感知部署策略，以及一系列系统级与内核（kernel）级优化：

- 硬件感知的并行策略：预填充（prefill）采用单节点 TP-8，解码（decode）采用小规模 EP-16，在满足延迟目标的同时缩小故障域。
- 内核级优化：FlashMLA-FP8 与 DeepGEMM swapAB，最大化 H20 上的计算吞吐。
- 调度与负载均衡：采用单批重叠（Single-Batch Overlap, SBO）提升小批量吞吐，并引入异步的专家亲和负载均衡器（Expert Affinity Load Balancer），最大限度减少跨节点通信。
- 轻量级可观测性：一套专门构建的诊断工具栈，用于快速定位并解决分布式 MoE 推理服务中的瓶颈。

我们的实验表明，采用本文的部署策略，**每个节点**在 4096 token 输入序列上可达到 **16.5k tokens/秒的输入吞吐与 5.7k tokens/秒的输出吞吐**。

据我们所知，这是 H20 上的**当前最优（SOTA）**性能。此外，本工作也是针对 H20 的**首个全面研究**，涵盖部署、优化与大规模工业实践。

## H20 的挑战

### H20 为何重要

H20 GPU 供应广泛，使蚂蚁集团能够以非常大的规模运营集群。在这种规模下，哪怕吞吐量只有小幅提升，也能转化为可观的每日成本节约。

### 对比：H20 与 H800

| 规格                | H20-96G     | H800-80G   |
|---------------------|-------------|------------|
| FP8 算力            | 296 TFLOPS  | 1979 TFLOPS|
| FP16/BF16 算力      | 148 TFLOPS  | 989 TFLOPS |
| 显存容量            | 96 GB       | 80 GB      |
| 显存带宽            | 4000 GB/s   | 3352 GB/s  |
| NVLink 带宽         | 900 GB/s    | 400 GB/s   |
| RDMA 网卡带宽       | 4 × 400 Gb/s| 8 × 400 Gb/s|

与 H800 相比，H20 拥有**更大的显存（96 GB）**、**更高的显存带宽（4000 GB/s）**，以及**超过 2 倍的 NVLink 带宽（900 GB/s）**。但代价是**计算性能弱得多**，且 **RDMA 网卡带宽更低**。

关键在于，推理——尤其是**解码阶段**——通常属于**访存受限（memory-bound）**型负载，这让 H20 的**高显存带宽与大容量显存**优势格外突出。基于这些优势，我们设计了一系列优化来**最大化推理吞吐量**。

## 解决方案：H20 上的优化与策略

### 部署策略

<img src="/images/blog/ant-group-prac/deploy.svg" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 90%; image-orientation: none;"></img>


#### 预填充

- **SLA：**预填充是计算密集型的，多节点 DP+EP 会拉高首 token 延迟（TTFT），常常违反 SLA。单节点 TP 部署可将 TTFT 控制在目标之内。
- **弹性伸缩：**预填充需要随 KV 缓存的增减进行扩缩容。单节点 TP 让扩缩容简单直接，而多节点 DP+EP 会让资源与缓存管理变得复杂。

#### 解码

- **硬件特性：**（与 H800 相比）H20 用算力换来了更大的显存和更高的 NVLink 带宽，既能高效利用 KV 缓存，又能让 MoE 通信留在高带宽的 NVLink 上。
- **故障半径：**更小的 EP 配置可以限制解码故障或 GPU 故障的影响范围。在 EP 高可用（HA）机制尚不成熟的当下，小规模 EP 在生产环境中更安全、更可靠。

### 优化

#### 预填充

<img src="/images/blog/ant-group-prac/prefill_overview.svg" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 90%; image-orientation: none;"></img>

##### 观察

- 对长序列而言，MLA 的开销高于 MHA。
- 尽管计算量更低，MoE 的延迟却出乎意料地高
- `embed/mlp all reduce + RMSNorm + fused_qkv_a_proj_with_mqa` 在 TP 中引入了冗余的通信与计算

##### 解决方案

- [MHA/MLA](https://github.com/sgl-project/sglang/pull/9551)：引入可调参数 `se = extend × (extend + prefix)`，根据批大小与序列长度在 MHA 与 MLA 之间切换。
- [MoE](https://github.com/sgl-project/sglang/pull/10567)：优化了 `b_scale` 的计算，用 TMA 重构了 `down proj` 的输入访问方式，并基于真实的专家分布调优配置。
- [TP 优化](https://github.com/sgl-project/sglang/pull/10568)：优化了 `embed/mlp reduce scatter + RMSNorm + fused_qkv_a_proj_with_mqa + all gather`，以减少计算与通信开销。

#### 解码

##### 负载均衡

###### [专家亲和 EPLB](https://github.com/antgroup-infra/sglang/pull/2)

<img src="/images/blog/ant-group-prac/eplb.svg" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 90%; image-orientation: none;"></img>

标准 EPLB 只均衡 GPU 内部的负载，却忽略了专家之间的相关性：频繁共同激活的专家常被分散到不同节点上，增加了跨节点通信开销。

我们扩展了 EPLB，通过追踪 **top-k 专家共激活**信息构建**专家亲和矩阵**。在完成 GPU 内负载均衡之后，我们进一步调整专家放置，让**高度共激活的专家**留在同一节点内，从而减少跨节点通信，相比原版 EPLB 额外带来约 **5% 的性能提升**。

###### [异步动态负载调整](https://github.com/sgl-project/sglang/pull/8529)

<img src="/images/blog/ant-group-prac/async_eplb.svg" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 60%; image-orientation: none;"></img>

静态 EPLB 把负载均衡与推理紧密耦合在一起。这种耦合意味着迁移决策会阻塞正在进行的推理，一旦需要变更专家放置，就会带来明显的延迟。

我们将**负载均衡**与**推理**解耦，让两者并行运行、互不阻塞。为了尽量降低专家迁移的影响，我们采用了**分层传输策略**，确保传输期间推理无缝进行。该方法达到了与静态 EPLB 持平甚至更优的性能，同时始终保持 **70% 以上的负载均衡率**。

##### 计算

###### [FP8 MLA](https://github.com/deepseek-ai/FlashMLA/pull/82)

BF16 版 FlashMLA 性能已经不错，但仍有优化空间：访存传输与计算未能完全重叠，共享内存占用也居高不下。此前的 FP8 实现（#54）提升了吞吐量，但仍受制于流水线效率低下、数据布局不匹配和粗粒度分块，性能与精度都因此受限。

我们在 Hopper（`SM90`）上实现了**端到端的 FP8 注意力**，用 `TMA` 做访存传输、用 `WGMMA` 做计算。两个 warp 组对 `QK^T` 与 `PV` 做流水线处理，最小化共享内存压力，并让计算与访存相互重叠。相比 BF16 FlashMLA，通过引入 FP8 `Q/KV`、`WGMMA FP8`、共享内存重新分配并移除冗余操作，获得了约 **70% 的加速**。

相较此前的 FP8 实现（#54），凭借更精细的 `TMA–WGMMA` 流水线、乒乓缓冲区（`sP0/sP1`、`sVt0/sVt1`）、用于修正数据布局的 128 位 `STSM/LDSM`、配合 BF16 ROPE 的细粒度 `Q@K` 分块，并完全贴合 Hopper 编程模型，又带来了额外约 **5% 的提升**。

###### [SwapAB GEMM](https://github.com/deepseek-ai/DeepGEMM/pull/192)


<img src="/images/blog/ant-group-prac/swapAB.svg" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 90%; image-orientation: none;"></img>

在 Hopper 上，WGMMA PTX 有硬性约束：`N` 必须是 8 的倍数，`M` 固定为 64。这迫使分块粒度变粗，当 `M` 较小、不规则或未按 64 对齐时会浪费算力。结果是边界低效、负载不均与共享内存压力过高限制了整体吞吐量，在 `M` 尺寸多变的 MoE 负载中尤其如此。

我们引入 **swapAB**，把问题的 `M` 维度重新映射到 WGMMA 的 `N` 维度上。这使更小的 `BLOCK_M (32)` 分块成为可能，带来更细的粒度和更好的资源利用率。

##### SBO（单批重叠，Single-batch-overlap）

###### 为什么不用 TBO

在 H20 上，TBO（双批重叠，Two-batch-overlap）在解码阶段的性能收益有限：

- **Hopper 架构限制**：WGMMA 的 `block_m` 固定为 64。在小批量解码场景下，TBO 会引入冗余的 MLP GEMM 计算。只有在较大批量（如 64 或 128）时才出现正向吞吐收益。
- **H20 的 SLA 限制**：在这种大批量下，低算力硬件无法满足 TPOT 的 SLA 目标，TBO 因此不适用于在线服务。


###### SBO 的工作原理

<img src="/images/blog/ant-group-prac/sbo.svg" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 90%; image-orientation: none;"></img>

为了在不违反 SLA 的前提下提升解码吞吐，DeepSeek v3/R1 采用了[**单批重叠（Single Batch Overlap, SBO）**](https://github.com/sgl-project/sglang/pull/9660)，为此我们修改了 [DeepEP](https://github.com/deepseek-ai/DeepEP/pull/390) 与 [DeepGEMM](https://github.com/deepseek-ai/DeepGEMM/pull/183)。这些重叠设计的关键在于通信与计算的对齐粒度。

我们观察到，在"通信-计算"重叠中，受网卡多 QP 调度、网络拥塞和多路径路由等因素影响，token 数据包常常乱序到达接收端。这种乱序破坏了与 GEMM 计算按 wave 粒度对齐的机制，降低了重叠效率。因此，我们把 **Dispatch Recv** 与数据无关的 **Shared Expert** 计算重叠起来，以最大化资源利用率。

相比之下，"计算-通信"重叠则更为直接。**Down GEMM** 会按顺序为 **Combine Send** 生成可预测的、有序的数据流。利用这一点，我们把两者的交互设计成信号同步的生产者-消费者模型：

- 对每个本地专家，按每 `block_m` 个 token 分配一个信号单元。
- Down GEMM 每完成部分计算，就以原子方式递增信号值。
- Combine Send 轮询该信号单元，一旦信号值达到阈值，就发送对应的 `block_m` 个 token。

### 可观测性

<img src="/images/blog/ant-group-prac/deepX.svg" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 90%; image-orientation: none;"></img>

为了在专家并行（EP）部署下识别并诊断 MoE 模型中的通信变慢问题，我们开发了一套名为 [**DeepXTrace**](https://github.com/antgroup/DeepXTrace) 的轻量级工作流：

- **指标采集**：每个节点周期性记录通信与计算指标，每 10 秒聚合到 Rank 0 进行集中记录。
- **异常检测**：Rank 0 构建 `N×N` 延迟矩阵，并用 z-score 分析从行、列和单个数据点多个层面检测异常。
- **根因分析**：异常被归类为计算延迟、专家分布不均衡或通信瓶颈。
- **可视化（Web UI）**：结果以热力图形式呈现，便于快速发现慢的 rank 或链路，指导针对性优化。

## 性能：让 H20 在真实世界推理中大放异彩

**SGLang 版本**：`v0.5.2`

### 预填充

#### 测试环境

**部署策略**：预填充实例部署在单节点（8× H20 GPU）上。以下配置作为基线（Base，BF16 + fa3）：
```shell
--tp-size 8
--Attention-backend fa3
```
**基准测试**：使用 `sglang.bench_serving` 并配合以下基础配置进行性能测试：
```shell
--backend sglang
--dataset-path /path/to/ShareGPT.json
--num-prompt 512
--random-input 4096
--random-output 1
--dataset-name random
--random-range-ratio 1
```
**指标**：我们直接从 `sglang.bench_serving` 的返回结果中获取 `Input token throughput`，并将结果归一化到单 GPU 口径。

#### 性能提升

<img src="/images/blog/ant-group-prac/prefill_perf.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 60%; image-orientation: none;"></img>

**序列长度**  
吞吐量从 1K 到 2K 总体上升，因为开销被逐渐摊薄；到 4K 时，显存压力成为主导因素，吞吐量转而下降。

**优化项**  
- **MHA**：在较长序列（2K、4K）下带来适度收益，但在 1K 下没有可测量的提升。  
- **MoE**：在所有序列长度下都带来稳定提升。  
- **QKV**：带来额外的吞吐提升，在较长序列下尤为明显，并有助于缩小短序列与长序列之间的性能差距。  
- **Fa3-FP8**：在注意力模块中引入 FP8 量化后，吞吐量进一步提升，在 2K 和 4K 序列长度下最为显著。  

### 解码
#### 测试环境
**部署策略**：解码实例部署在双节点（16× H20 GPU）上。以下配置作为基线（Base，BF16 + MTP）：
```shell
--tp-size 16
--dp-size 16
--enable-dp-attention
--enable-deepep-moe
--deepep-mode low_latency
--speculative-algorithm NEXTN 
--speculative-num-steps 1
--speculative-eagle-topk 1
--speculative-num-draft-tokens 2
```
**基准测试**：使用 `sglang.bench_serving` 并配合以下基础配置进行性能测试：
```shell
--backend sglang
--dataset-path /path/to/ShareGPT.json
--random-input 4096
--random-output 1536
--dataset-name random
--random-range-ratio 1
```
**指标**：压测时批大小是逐步增大的，因此 `sglang.bench_serving` 的原始结果并不能准确反映给定批大小下的吞吐量。为此，我们解析日志中的 `Decode batch` 条目，取同一批大小下 100 个样本的吞吐量中位数作为代表值。

#### 性能提升 

<img src="/images/blog/ant-group-prac/decode_perf.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 80%; image-orientation: none;"></img>

**批大小**  
随着批大小增大，单 GPU 吞吐量稳步上升。但在更大批量下，计算与通信开始趋于饱和，收益随之放缓。

**优化项**  
- **FP8 MLA**：降低注意力计算成本。小批量下收益有限；在注意力占主导的更大批量下，BS=56 时吞吐量较基线提升 16.9%。
- **SwapAB Gemm**：支持更细粒度的分块，改善边界效率与并发度。中小批量下收益明显——BS=2 时 +8.1%，BS=4 时 +7.7%——更大批量下仍有约 2% 的增量收益。
- **SBO**：通过计算与通信重叠提升资源利用率。批量越大，重叠的效果越显著，在 BS=20–56 范围内带来 **+8%–10%** 的提升。

#### EP 规模探究

<img src="/images/blog/ant-group-prac/ep_size.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 80%; image-orientation: none;"></img>

- **批大小 < 16**：**EP32 优于 EP16**。更大的 EP 规模减少了每张 GPU 承载的专家数量，显著降低了访存开销。尽管更稀疏的专家放置会略微增加通信成本，但显存节省占据主导，因此吞吐量更高（例如 BS=8 时，EP32 达到 293 tokens/s，而 EP16 为 278 tokens/s）。
- **批大小 ≥ 16**：**EP16 反超 EP32**。更大的 EP 规模下，跨 GPU 通信成为主导。使用 DeepEP 时，EP16 下约 50% 的 MoE 流量留在 NVLink 上，而 EP32 下仅约 25%，迫使更多数据走节点间传输、抬高了延迟。结果就是吞吐量下降（例如 BS=32 时，EP16 达到 675 tokens/s，而 EP32 为 585 tokens/s）。

#### MTP 配置

<img src="/images/blog/ant-group-prac/mtp_perf.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 80%; image-orientation: none;"></img>

**草稿 token 数与接受长度（Accept Length）**  
- **(steps=1, topK=1, draft-tokens=2)** → 接受长度 ≈ 1.8–1.9  
- **(steps=2, topK=1, draft-tokens=3)** → 接受长度 ≈ 2.4–2.7  
- **(steps=3, topK=1, draft-tokens=4)** → 接受长度 ≈ 2.9–3.3  

**不同批大小下的性能**  
- **小批量**：在 H20 这类低算力 GPU 上，资源并未被充分利用。即使更大的草稿 token 数会降低接受长度，仍能提升吞吐量。例如 BS=1 时，吞吐量从 **43 tokens/s（steps=1, topK=1, draft-tokens=2）** 提升到 **52 tokens/s（steps=3, topK=1, draft-tokens=4）**，提升约 **21%**。
- **大批量**：批量更大时，GPU 变为算力受限。更大的草稿 token 设置带来更短的接受长度，导致计算浪费、性能下降。BS=32 时，吞吐量从 **675 tokens/s（steps=1, topK=1, draft-tokens=2）** 降到 **554 tokens/s（steps=1, topK=1, draft-tokens=2）**，损失约 **18%**。【译者注：原文中 554 tokens/s 处的配置同样写作 (steps=1, topK=1, draft-tokens=2)，结合上下文疑为笔误（应为 steps=3、draft-tokens=4 的配置），数据按原文保留。】

## 分层在线推理服务

我们团队支撑着蚂蚁集团的全部推理负载。  
为了在**用户体验**与**成本效率**之间取得平衡，我们提供**基于 SLA 的分层服务**：

- **InferX Base：**TTFT < 2s，TPOT < 70 ms  
- **InferX Pro：**TTFT < 1.5s，TPOT < 50 ms  
- **InferX Max：**TTFT < 1s，TPOT < 30 ms  

### 解码部署

<img src="/images/blog/ant-group-prac/mtp_latency.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 80%; image-orientation: none;"></img>

所有解码实例均以**双节点**方式部署：**Attention-DP16 + MoE-EP16**。  

为了满足不同的 SLA 目标，我们沿着**延迟–吞吐量曲线**调整配置，主要调节**单 GPU 批大小**与 **MTP 设置**。

| 服务层级        | 批大小/GPU      | Steps | Eagle-topk | Draft-tokens | 单 GPU 吞吐量（tokens/s） |
|-----------------|----------------|-------|------------|--------------|---------------------------|
| **InferX Base** | 48             | 1     | 1          | 2            | 714                       |
| **InferX Pro**  | 32             | 1     | 1          | 2            | 675                       |
| **InferX Max**  | 12             | 2     | 1          | 3            | 423                       |

### 预填充部署

如前文所述，我们的预填充实例采用单节点 TP8 部署。 
为防止排队延迟导致 TTFT 超标，我们为每个模型实例运行两个预填充实例。 
展望未来，我们计划支持预填充实例的动态伸缩，以更好地适应负载波动。

## 可复现性
我们的实验依赖多个仓库（SGLang、DeepEP、DeepGEMM、FlashMLA），其中若干 PR 仍在审核中。
为了便于复现，我们将把这些改动整合到一个专门的测试分支，并提供预构建镜像。 
两者都将在 [**antgroup/sglang**](https://github.com/antgroup/sglang.git) 仓库中提供。

## 结语
借助 SGLang，我们在 H20 GPU 上实现了 DeepSeek-R1 服务性能的当前最优（SOTA）水平。通过在吞吐量与延迟之间取得平衡，我们提供了针对多样化 SLA 需求优化的部署策略。未来，我们将继续紧跟社区进展，并把实践中的优化成果回馈给生态。

## 致谢

我们谨向以下团队与合作者致以诚挚的感谢，感谢他们宝贵的支持与贡献：

- **SGLang 团队与社区**——感谢他们在 SGLang 框架上的杰出工作。  
- **蚂蚁集团 SCT 与推理团队**——Yongfei Xu、Zhe Wang、Qianyu Zhang、Chun Huang、Xi Chen、Peipeng Cheng、Fakang Wang、Jianhao Fu 以及许多其他同事。
