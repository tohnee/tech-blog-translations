---
title: "将 DeepSeek-V4-Pro 推理服务推向极限"
title_en: "Pushing the Limits of Serving DeepSeek-V4-Pro"
author: "Tianyu Zhang, Yusong Gao, Yun Zhang"
date: "August 19, 2026"
previewImg: /images/blog/deepseek_v4/00_cover.png
type: blog
source: https://lmsys.org/blog/2026-08-19-deepseek-v4-pro-engine-optimization-h20/
translated: 2026-09-12
---

# 将 DeepSeek-V4-Pro 推理服务推向极限

> 原文：[Pushing the Limits of Serving DeepSeek-V4-Pro](https://lmsys.org/blog/2026-08-19-deepseek-v4-pro-engine-optimization-h20/) · LMSYS Blog · Tianyu Zhang, Yusong Gao, Yun Zhang

## 1. 引言

DeepSeek-V4-Pro 是一个 1.6 万亿参数的专家混合（MoE）模型，发布时同时提供 FP8 与 FP4 两种权重。这一规模的模型天然受益于 NVIDIA Blackwell GPU 这类加速器——它们提供更大的 HBM、更高的计算吞吐以及原生 FP4 Tensor Core。然而，H20 GPU 仍被广泛部署，尽管它并不具备这些优势。

硬件受限并不意味着服务要求可以放宽。长上下文预填充（prefill）仍须控制首 token 延迟（TTFT）；交互式解码必须满足各服务档位的每输出 token 时间（TPOT）目标；持续流量则需要在总吞吐量与 KV 缓存容量之间取得平衡。短输入、长上下文、延迟敏感请求与高并发会以不同方式给系统施压，没有任何一种通用配置能把所有场景都服务好。

**一个模型需要多套服务配置（serving profile）。**负载特征、服务等级目标（SLO）与实测硬件行为共同决定部署拓扑与执行路径：

- **让服务配置匹配负载。**在本文评估的配置中，预填充根据实测的上下文长度范围在 PP2 与 PP4 之间选择，解码则使用针对不同延迟、吞吐量与 KV 容量目标做过优化的配置。
- **优化预填充路径。**我们优化 `Attention-CP8 → MoE-TP8` 执行路径与上下文并行通信，并针对长、短上下文负载产生的真实路由形状进行调优。
- **优化解码路径。**我们优化 DSpark 投机解码路径，并针对不同的解码 SLO 改进执行方式、专家路由与通信-计算重叠。

**推向延迟极限。**在 batch size 1 下，单节点 H20-141GB 参考配置达到 **271 输出 tokens/s**，而 [B300 上报告的数据](https://www.lmsys.org/blog/2026-07-06-dspark-sglang/)为 **383.7 tokens/s**。尽管硬件差距巨大，针对负载的系统优化把两者实测解码性能之比缩小到 **1.42×**。详细的基准测试设置与基于日志的吞吐量提取方法见[附录 B.3](#b3-benchmark-settings)。

**覆盖服务能力的全部边界。**延迟结果只是系统的一条边界。在整个配置家族中，优化后的预填充达到**每节点 8.45k 输入 tokens/s**，并能在 **43.7 秒内处理完 1M token 的提示词**。面向吞吐量的解码方面，DP16-EP16 效率参考配置达到**每节点 4.67k 输出 tokens/s**，对应平均 TPOT 为 **27.4 ms**。这些结果有意来自不同的配置，每个配置都针对上下文长度、延迟、吞吐量与容量约束的不同组合做了选择与优化。

**本文的贡献是一套方法论，而非单一基准。**场景化推理服务让每种负载都能在现有硬件上评估过的各配置之间，走向一个更好的实测工作点。我们希望本文呈现的部署选择、优化方法与测量结果，能为在算力、内存、带宽或互连受限条件下服务前沿模型的团队提供一份实用参考。

## 2. 从硬件约束到服务配置

### 2.1 硬件约束与服务角色

<img src="/images/blog/deepseek_v4/01_hardware_gap.svg" alt="Hardware specification comparison across H20-96GB, H20-141GB, and B300, covering FP4 and FP8 compute, HBM capacity, memory bandwidth, NVLink, and RDMA" style="display:block; margin:auto; width:100%; max-width:640px; height:auto;"></img>

*图 1. 硬件差距：H20 vs. B300。*

**Blackwell 提供原始性能，H20 提供可部署的规模。**B300 提供原生 FP4 Tensor Core、高得多的 FP8 吞吐以及大得多的 HBM。H20 无法匹敌其算力，但仍可大规模获取，并提供高内存带宽与 900 GB/s 的 NVLink。本研究中每个节点包含 8 块由 NVLink 互联的 GPU。预填充不保留长期存续的每请求状态，因此其硬件选择主要由 TTFT、算力与通信效率决定。解码则必须在生成全程保留每个活跃请求的 KV 缓存，这使得 HBM 容量成为上下文长度与并发的直接限制。对于本文研究的部署，这促使我们用 H20-141GB 做解码，用 H20-96GB（其容量对我们的预填充负载已经足够）做预填充。

<img src="/images/blog/deepseek_v4/02_h20_role_assignment.svg" alt="Hardware assignment by serving role: H20-96GB serves TTFT-sensitive prefill with short-lived state, while H20-141GB serves KV-capacity-bound decode with persistent state" style="display:block; margin:auto; width:80%; max-width:100%; height:auto;"></img>

*图 2. 按服务角色分配硬件。*

### 2.2 容量选择

服务容量最终来自一份共享的 HBM 预算：模型权重与每请求 KV 状态争夺同一块内存。我们将**全 token 容量（full-token capacity）**定义为：在模型权重与运行时缓冲区分配完毕后，每个 rank 所能容纳的全注意力 KV token 的最大数量。它是一个内存上限，并不直接保证可接纳的 batch size。

#### 用 Humming MXFP4AFP8 压缩权重占用

**先压缩权重占用。**[Humming MXFP4AFP8](https://github.com/inclusionAI/humming) 采用 MXFP4 专家权重加在线 FP8 激活值，在缺乏原生 FP4 Tensor Core 的 H20 GPU 上降低权重占用与内存流量。SGLang 集成见 [sglang#23754](https://github.com/sgl-project/sglang/pull/23754)。我们将在后续专门文章中介绍 Humming/SGLang 集成。模型级精度结果与公开参考测量见[附录 D.2](#d2-humming-accuracy-validation)。

#### 用 Online C128 扩展 KV 容量

**给 KV 缓存留出增长空间。**Offline C128 基线为每个压缩页保留逐索引状态；Online C128 则改为维护一个紧凑的聚合状态，把更多 HBM 释放给 KV 缓存池。它会引入额外的状态维护与投机验证工作，但在我们的测试中未观察到 TPOT 回退。

#### 容量收益叠加

<img src="/images/blog/deepseek_v4/03_capacity_scaling.svg" alt="Two horizontal bar-chart panels show full-token capacity scaling for DP32-EP32 and PP2-TP8 from Baseline FP8 through Humming MXFP4AFP8 to Online C128" style="display:block; margin:auto; width:96%; max-width:100%; height:auto;"></img>

*图 3. Humming MXFP4AFP8 与 Online C128 带来的容量扩展。*

**容量收益在权重与 KV 状态两个维度上叠加。**通过压缩权重占用，Humming MXFP4AFP8 将全 token 容量扩展到 Baseline FP8 + Offline C128 配置的 **1.71×**（DP32-EP32）与 **4.47×**（PP2-TP8）。Online C128 再缩减 C128 辅助状态的占用，在 Humming 之上再提供 **2.268×** 的提升。两项技术合起来，把容量提升到基线的 **3.88×**（DP32-EP32）与 **10.14×**（PP2-TP8）。完整数据见附录 D.1。

### 2.3 场景化服务配置

#### 预填充配置

<img src="/images/blog/deepseek_v4/04_prefill_profiles.svg" alt="Two independent prefill deployment strategies: PP2 and PP4 use different layer partitions while every stage follows the same Attention-CP8 and MoE-TP8 execution path" style="display:block; margin:auto; width:96%; max-width:100%; height:auto;"></img>

*图 4. 预填充配置：相同执行路径，不同流水线深度。*

**合适的流水线深度取决于有多少工作可供流水化。**PP2-CP8-TP8 与 PP4-CP8-TP8 共享相同的 `Attention-CP8 → MoE-TP8` 执行路径。在拓扑层面，两者的主要区别是流水线深度：PP2 把模型分布到两个阶段，PP4 则用四个。

**短上下文偏好更低的流水线开销；长上下文能暴露更多并行性。**短输入产生的分块更少，更深的流水线会填充不足，使填充、排空与跨阶段传输的成本更加突出。长上下文能提供足够多的分块让四个阶段保持忙碌；每个阶段分到的层更少，额外的节点就转化为更多的预填充并行度。在我们的部署中，这些特征促使我们**对较短上下文使用 PP2-CP8-TP8**，**对长上下文负载使用 PP4-CP8-TP8**。

#### 低延迟解码配置

<img src="/images/blog/deepseek_v4/05_low_latency_decode.svg" alt="Single-node TP8 is the dashed reference and PP2-TP8 is the two-node low-latency serving profile used in our deployment; both execute Attention-TP8 and MoE-TP8, each followed by its own AllReduce" style="display:block; margin:auto; width:96%; max-width:100%; height:auto;"></img>

*图 5. 低延迟解码：TP8 参考与 PP2-TP8 服务配置。*

**低延迟始于最短的执行路径。**单节点 TP8 与 PP2-TP8 共享相同的 `Attention-TP8 → MoE-TP8` 执行路径；区别在于模型是否跨节点切分。单节点 TP8 把所有层放在一个 H20-141GB 节点上，避免跨阶段通信与同步。PP2-TP8 则把模型切分到两个流水线阶段。

**最快的拓扑未必是最能承载服务的拓扑。**单节点 TP8 的执行路径更短，但模型权重与服务状态共享一个节点的 HBM，留给 KV 缓存的空间有限，无法同时支持长上下文与更大的 batch size。PP2-TP8 付出额外的流水线开销，但把模型权重分布到两个节点上，为 KV 状态释放更多 HBM。针对我们的延迟与容量目标，我们**以单节点 TP8 作为 batch size 1 的延迟参考**，**以 PP2-TP8 作为低延迟服务配置**。

#### 高吞吐解码配置

<img src="/images/blog/deepseek_v4/06_high_throughput_decode.svg" alt="High-throughput decode scales DP and EP ranks from the two-node DP16-EP16 reference to the four-node DP32-EP32 serving profile used in our deployment; every node participates in all layers while routed experts remain sharded across EP ranks" style="display:block; margin:auto; width:96%; max-width:100%; height:auto;"></img>

*图 6. 高吞吐解码：DP16-EP16 参考与 DP32-EP32 容量配置。*

**高吞吐解码同时扩展数据并行与专家并行。**两种配置都使用 `Attention-DP → MoE-EP` 执行路径。DP16-EP16 是最小部署单元；DP32-EP32 在同一拓扑内同时扩展 DP 与 EP。

**横向扩展优先考虑请求容量而非单 GPU 吞吐。**更大的 EP 组把专家权重分布到更多 GPU 上，为 KV 缓存释放 HBM，从而接纳更多并发请求。与此同时，留在每个节点内的 MoE 流量比例变小、跨节点的比例变大，这会降低单 GPU 效率。在本文评估的配置中，我们以 DP16-EP16 作为最小部署单元和效率参考，用 DP32-EP32 扩展请求容量。

## 3. 预填充：平衡计算与通信

**预填充性能是一个系统问题。**专家负载不均衡、上下文并行通信与生产环境路由形状共同决定 TTFT；只优化孤立的单个算子是不够的。

### 3.1 为什么用 MoE-TP 而非 MoE-EP

<img src="/images/blog/deepseek_v4/07_cp_fused_moe_mechanism.svg" alt="Replacing MoE-EP with MoE-TP in the prefill path" style="display:block; margin:auto; width:96%; max-width:100%; height:auto;"></img>

*图 7. 用 MoE-TP 替换 MoE-EP。*

**流量更少仍可能更慢。**MoE-EP 只交换被路由的 token，但真实的预填充流量呈现显著的专家偏斜（expert skew）。持有热点专家的 rank 计算量更大，成为掉队者；所有其他 rank 在 combine 步骤都要等待最慢的那条路径。通信量更低并不等于 TTFT 更低。

**先平衡计算，再压缩流量。**对于本文评估的 H20 预填充负载，PP2 与 PP4 都使用 MoE-TP。全序列 all-gather 与 reduce-scatter 带来更多通信量，但这些流量始终走高带宽 NVLink，成本稳定且可预测。所有 TP rank 对同一批被路由的 token 执行张量并行计算，避免专家偏斜演变成 rank 级长尾。对这一负载而言，**可预测的通信比不可预测的不均衡更便宜**。实现见 [sglang#24947](https://github.com/sgl-project/sglang/pull/24947)。

### 3.2 加速并融合预填充集合通信

<img src="/images/blog/deepseek_v4/08_collective_communication_optimization.svg" alt="Symmetric-memory collectives provide a reusable foundation for TP and CP, while fused Prefill kernels collapse the communication-heavy critical path" style="display:block; margin:auto; width:96%; max-width:100%; height:auto;"></img>

*图 8. 对称内存集合通信与预填充融合。*

**构建可复用的集合通信快速路径。**MoE-TP 用可预测的集合通信流量取代不可预测的专家不均衡，使通信效率成为下一个瓶颈。我们让对称内存在 TP 与 CP 之间可复用，使 AllReduce、AllGather 与 ReduceScatter 得以共享注册缓冲区快速路径以及适用的 Hopper 加速。支撑这一点的上游工作包括[内存池所有权](https://github.com/sgl-project/sglang/pull/21392)、[通信器注册](https://github.com/sgl-project/sglang/pull/19329)、[MoE-TP 集合通信缓冲区](https://github.com/sgl-project/sglang/pull/29007)，以及 [CP 注意力](https://github.com/sgl-project/sglang/pull/17756)与 [KV 缓存](https://github.com/sgl-project/sglang/pull/24040)缓冲区路径。

**再缩短预填充临界路径。**更快的集合通信本身并不能消除通信与计算之间的边界。针对 32K 单分块场景，我们构建了一条融合路径：用拷贝引擎驱动的 AllGather 与融合后的 FP8 量化及共享专家 GEMM 重叠执行，再用第二个 Triton 算子把 TopK 归约、共享专家加法与 ReduceScatter 合并在一起。这一改造把 7 个算子重组为 3 个执行组，在同等条件 PP4 A/B 对比中将 TTFT 降低约 **3.5%**。

### 3.3 针对真实路由形状调优 Humming

<img src="/images/blog/deepseek_v4/09_humming_exact_shape_workflow.svg" alt="Humming prefill workflow from routing capture through separate W13 and W2 tuning to staged validation" style="display:block; margin:auto; width:96%; max-width:100%; height:auto;"></img>

*图 9. 针对真实路由形状调优 Humming。*

**通用调优会错过真正重要的形状。**预填充路由把 token 不均匀地分布到 384 个专家上，因此有效的 `M` 维度会聚集成少数离散值。W13 与 W2 又作用于不同的形状，单一通用启发式无法同时优化两条路径。

**从生产路由出发调优。**我们从真实路由直方图中提取高频形状，为 W13 与 W2 分别构建精确形状配置，并在算子、流水线阶段与同等条件 A/B 三个层级上验证。优化目标不是合成的 `M` 取值范围，而是**我们实际服务的路由分布**。在 32K 输入长度下的同等条件 PP4 A/B 对比中，所选 MoE 算子延迟下降约 **21%**，折合端到端 TTFT 降低 **11.35%**。

## 4. 解码：优化投机与 MoE 执行

**在我们的实现中，解码优化因配置而异。**PP2-TP8 需要在投机流水线各阶段之间做协调，DP32-EP32 则聚焦于高并发下优化精化（refinement）步骤与专家路由。Humming 融合与重叠改进的是这些服务拓扑之下共享的 MoE 热点路径。

### 4.1 低延迟 PP2-TP8：将 DSpark 扩展到流水线各阶段

<img src="/images/blog/deepseek_v4/10_pp2_tp8_dspark_execution.svg" alt="PP2-TP8 DSpark execution coordinated across two pipeline stages, with target hidden states sent to Stage 1 and accepted tokens and next candidates returned under a shared stage-tick protocol" style="display:block; margin:auto; width:96%; max-width:100%; height:auto;"></img>

*图 10. 在 PP2 各阶段间协调 DSpark。*

**流水线并行切开了投机循环。**在 PP2-TP8 中，目标模型执行跨越两个流水线阶段，而 [DSpark](https://github.com/sgl-project/sglang/pull/30261) 草稿器（drafter）只驻留在最后一个阶段。Stage 0 把目标隐藏状态发送给 Stage 1，由后者执行验证、接受 token，并为下一轮生成候选。

**让两个阶段步调一致地推进。**每一轮投机都要跨越流水线边界。我们在一个执行协议下协调两个阶段与所需的中间数据传输，既防止各阶段进入不同的轮次，又避免冗余同步。针对 PP 的 DSpark 集成正在通过 [sglang#32281](https://github.com/sgl-project/sglang/pull/32281) 上游化。

### 4.2 高吞吐 DP32-EP32：消除高并发瓶颈

<img src="/images/blog/deepseek_v4/11_dp32_ep32_bottleneck_removal.svg" alt="DP32-EP32 bottleneck removal: single-chunk transposed GEMM replaces row-wise full-vocabulary dot-reduce, while a routing-affinity snapshot guides EPLB placement and redundant experts" style="display:block; margin:auto; width:96%; max-width:100%; height:auto;"></img>

*图 11. DP32-EP32 瓶颈消除。*

本小节的同等条件 A/B 结果使用 DP32-EP32、4K 输入长度、每个 DP rank 32 个并发请求。

**为精化选择合适的执行形状。**精化步骤对全词表做投影，为 DSpark 的候选集合重新打分。在高并发下，逐行 dot-reduce 会为每个活跃行反复读取词表权重，在每个解码步骤中形成持续的长尾。我们把活跃行合并成一次转置 GEMM，减少冗余内存流量、缩短精化路径。单 GPU 吞吐量提升 **22.8%**。

**依据实测路由放置专家。**DSpark 流量同样呈现显著的专家偏斜。我们从代表性请求中记录路由亲和性（routing affinity），并用它配置专家并行负载均衡（EPLB）与冗余专家，防止少数热点专家反复拉长临界路径。单 GPU 吞吐量提升 **13.5%**。

### 4.3 Humming 解码热点路径：融合与重叠

<img src="/images/blog/deepseek_v4/12_humming_decode_hot_path_optimizations.svg" alt="Two side-by-side Humming decode optimizations: quantized hot-path fusion removes intermediate buffering before W2, while Humming-Aware SBO overlaps per-tile W2 completion with DeepEP combine sends" style="display:block; margin:auto; width:96%; max-width:100%; height:auto;"></img>

*图 12. Humming 解码热点路径优化。*

这些优化位于服务拓扑之下，可以被基于 Humming 的解码配置复用。下文的同等条件结果使用 DP32-EP32、4K 输入长度、每个 DP rank 32 个并发请求。

**消除额外的量化步骤。**我们把 SwiGLU 激活与量化融合，使融合后的算子直接产出 W2 所需的数据与 scale。这消除了对中间缓冲的反复访问，也去掉了独立的量化步骤，让 W2 更早启动。在同等条件 DSpark A/B 对比中，单 GPU 吞吐量提升 **44.0%**。

**让通信与 W2 重叠。**我们把此前工作（[sglang#9660](https://github.com/sgl-project/sglang/pull/9660)）中的[单批次重叠（Single-Batch Overlap, SBO）](https://www.lmsys.org/blog/2025-09-26-sglang-ant-group/#sbo-single-batch-overlap)机制改造为 **Humming-Aware SBO**。逐 tile 的信号让 DeepEP 在某个 W2 输出 tile 完成时即开始相应的 combine 发送，而无需等待整个 GEMM 完成。在早前同一工作点的同等条件非投机 A/B 对比中，SBO 相对 FP8 传输档位挽回了 **4.12%** 的吞吐量。

## 5. 评估：系统收益与配置权衡

### 5.1 预填充：累计收益与上下文长度权衡

<img src="/images/blog/deepseek_v4/13_humming_prefill_throughput_uplift.svg" alt="Baseline and final prefill throughput for PP2-CP8-TP8 and PP4-CP8-TP8 across input lengths from 4K to 1M" style="display:block; margin:auto; width:96%; max-width:100%; height:auto;"></img>

*图 13. 预填充吞吐量的累计提升。*

**PP2 强化了短上下文配置。**PP2 在全部九个输入长度上都有提升，吞吐量几何平均增益为 **36.5%**，总输入吞吐量峰值达 **16,900 tokens/s**。更浅的流水线降低了短请求的填充-排空开销，使 PP2 能用更少的资源维持更低的 TTFT。

**PP4 把收益带入长上下文。**在同样九个测试点上，PP4 的吞吐量几何平均增益为 **31.8%**。随着上下文长度增长，更深的流水线有足够的工作来摊销其固定成本：总输入吞吐量在 512K 达到 **25,860 tokens/s**，在 1M 仍保持 **23,970 tokens/s**。

<img src="/images/blog/deepseek_v4/14_prefill_ttft_crossover.svg" alt="TTFT trade-off between the evaluated PP2-CP8-TP8 and PP4-CP8-TP8 profiles across context lengths" style="display:block; margin:auto; width:96%; max-width:100%; height:auto;"></img>

*图 14. PP2 与 PP4 之间的 TTFT 权衡。*

**上下文长度会移动 PP2/PP4 的权衡点。**相对 PP4，PP2 在 4K 把 TTFT 降低 **16.7%**，在 32K 降低 **19.5%**；两种配置在 8K、16K 与 64K 处的差距保持在 **2%** 以内。从 128K 起PP4 建立起决定性优势，相对 PP2 分别在 128K、256K、512K 与 1M 处把 TTFT 降低 **26.2%**、**33.3%**、**42.1%** 与 **44.8%**。因此，我们把路由边界视为由实测上下文长度范围推导出的运行策略，而不是一个普适的交叉点。

附录 A.1–A.2 提供完整的 TTFT 与总输入吞吐量结果。

### 5.2 低延迟解码：性能与容量权衡

<img src="/images/blog/deepseek_v4/15_decode_optimized_dspark_tpot.svg" alt="Four grouped bar charts compare No-Spec baseline and Optimized DSpark peak TPOT across batch sizes at 8K, 64K, 256K, and 1M input lengths" style="display:block; margin:auto; width:96%; max-width:100%; height:auto;"></img>

*图 15. Optimized DSpark 带来的峰值 TPOT 提升。*

**Optimized DSpark 重置了延迟基线。**在图 15 所示的四个输入长度上，Optimized DSpark 在 batch size 1 下把峰值 TPOT 降低 **74.8%–78.0%**；在每对测量共享的最大 batch size 下，降幅仍达 **52.2%–60.0%**。这一收益从 8K 一直保持到 1M，并不局限于短上下文或单请求执行。

<img src="/images/blog/deepseek_v4/16_decode_bs1_throughput.svg" alt="Batch-size-1 throughput across four input lengths for No-Spec PP2-TP8, Optimized DSpark PP2-TP8, and single-node TP8 on H20-141GB, with 383.7 tokens per second on B300 shown as a separate external reference" style="display:block; margin:auto; width:96%; max-width:100%; height:auto;"></img>

*图 16. Batch Size 1 解码吞吐量：H20-141GB 与 B300 参考。*

**实测服务性能远比峰值算力之比所暗示的更接近。**在图 16 所示的四个输入长度上，PP2-TP8 上的 Optimized DSpark 在 batch size 1 达到 **150–174 tokens/s**；单节点 TP8 参考达到 **183–271 tokens/s**。就实际执行路径所用的精度而言，B300 的峰值 Tensor Core 算力约为 H20-141GB 的 **45.6×**（B300 FP4 对 H20 FP8），内存带宽为其 **1.67×**。然而实测最高生成速率分别为 [B300 上的 **383.7 tokens/s**](https://www.lmsys.org/blog/2026-07-06-dspark-sglang/)与 H20-141GB 上的 **271 tokens/s**——比值仅为 **1.42×**。即便面对这块强得多的硬件参考，针对负载的优化也让 H20-141GB 参考配置在实测服务性能上大幅逼近对手。

**就我们的生产目标而言，容量因素更青睐 PP2-TP8。**单节点 TP8 更快，但在 1M 上下文时其 KV 缓存容量只够 batch size 1，无法接纳更大的 batch 或更多并发请求。PP2-TP8 通过把模型权重分布到两个流水线阶段，分别在 1M、512K 与 256K 上下文下支持 batch size 4、8 与 16。配合 Online C128，其全 token 容量达到 **11.04M tokens/rank**。对于与我们相近的上下文长度与并发目标，我们建议保留单节点 TP8 作为延迟参考，并使用 **PP2-TP8 作为低延迟服务配置**。完整性能与容量数据见附录 B 与附录 D.1。

### 5.3 高吞吐解码：前沿收益与配置权衡

<img src="/images/blog/deepseek_v4/17_decode_high_throughput_pareto.svg" alt="Throughput-interactivity Pareto frontiers at 4K, 32K, 128K, and 1M compare FP8 MTP, optimized MTP, FP8 DSpark, and Humming MXFP4AFP8 with Online C128 and DSpark" style="display:block; margin:auto; width:96%; max-width:100%; height:auto;"></img>

*图 17. 吞吐量-交互性帕累托前沿。*

图 17 展示了吞吐量-交互性前沿如何随系统演进而移动。横轴是交互性（tokens/s/user），纵轴是吞吐量（tokens/s/GPU）。在这些 DP/EP 配置中，每个 DP rank 对应一块 GPU；交互性等于单 GPU 吞吐量除以每个 DP rank 的并发请求数。越靠右上方的点，用户可见的生成速度与 GPU 效率的组合越好。四条曲线代表系统的累计演进，而不是第 4 节中任何单一优化的孤立收益。

MTP 指多 token 预测（multi-token prediction）；`(3, 1, 4)` 配置使用三步投机、top-k 1 与四个草稿 token。

**系统优化推动整条前沿外移。**在 4K、每个 DP rank 32 个并发请求时，单 GPU 吞吐量从 **319.92 tokens/s/GPU** 升至 **703.15 tokens/s/GPU**，提升 **2.20×**。在 1M、每个 DP rank 一个请求时，从 **27.05 tokens/s/GPU** 升至 **66.82 tokens/s/GPU**。前三个系统里程碑在 1M 时每个 DP rank 都只能处理一个请求；最终系统支持四个，并达到 **177.48 tokens/s/GPU**。运行边界的扩大既来自更快的执行，也来自更大的容量。

<img src="/images/blog/deepseek_v4/18_dp16_dp32_throughput.svg" alt="Two grouped bar charts compare DP16-EP16 and DP32-EP32 throughput per GPU across input lengths with 16 and 32 concurrent requests per DP rank" style="display:block; margin:auto; width:96%; max-width:100%; height:auto;"></img>

*图 18. 单 GPU 吞吐量：DP16-EP16 vs. DP32-EP32。*

**更小的部署单元在特定高并发工作点上保住效率。**在我们此前[在 H20 上服务 DeepSeek-V3/R1 的工作](https://www.lmsys.org/blog/2025-09-26-sglang-ant-group/#investigation-for-ep-size)中，我们发现更小的 EP 部署单元能让更大比例的 MoE 流量留在节点内。DeepSeek-V4-Pro 在图 18 所绘的工作点上表现出同样的优势：在每个 DP rank 16 与 32 个并发请求时，DP16-EP16 的单 GPU 吞吐量比 DP32-EP32 高约 **3.6%–20%**。但完整扫描在所有并发级别上并非单调，因此我们把 DP16-EP16 用作效率参考，而不是 DP32-EP32 的通用替代。

<img src="/images/blog/deepseek_v4/19_dp16_dp32_capacity.svg" alt="A compact table compares the maximum valid request capacity per DP rank for DP16-EP16 and DP32-EP32 at 256K, 512K, and 1M input lengths" style="display:block; margin:auto; width:100%; max-width:640px; height:auto;"></img>

*图 19. 每 DP rank 的长上下文请求容量。*

**容量因素改变了高吞吐配置的取舍。**DP16-EP16 单 GPU 效率更高，但 DP32-EP32 把专家权重分布到更多 rank 上，为 KV 缓存释放出额外的 HBM。在 256K、512K 与 1M 下，每 DP rank 的最大并发请求数分别从 **8、4、2** 提升到 **16、8、4**——一致的 **2×** 扩展。对于长上下文并发目标与我们相近的部署，这份额外容量使 **DP32-EP32 成为面向容量的高吞吐配置**，而 DP16-EP16 仍可作为效率参考。完整数据见附录 C 与附录 D.1。

## 6. 结语

**一个模型不必只配一套妥协的方案。**我们在 H20 上为 DeepSeek-V4-Pro 构建了场景化推理服务栈：预填充根据上下文长度在 PP2 与 PP4 之间切换；解码用 PP2-TP8 换低延迟、用 DP32-EP32 换高吞吐。通过容量、部署拓扑与执行路径的协同设计，H20 在算力受限且没有原生 FP4 Tensor Core 的情况下，依然能够支撑 1M token 上下文并满足多套推理服务 SLO。

**可迁移的成果是一套场景驱动的方法论。**服务配置不应仅凭硬件规格或孤立的基准测试来选择。我们建议从负载、SLO、上下文长度与并发出发，再用性能剖析找出起约束作用的资源，并将其转化为具体的拓扑与执行路径决策。我们希望这套方法论能帮助 AI 基础设施团队在多种资源约束下——无论瓶颈是算力、内存容量、内存带宽还是互连——构建实用的前沿模型服务系统，并与更广泛的开源生态分享这些经验。

## 致谢

我们感谢 **SGLang 团队与社区**为 SGLang 框架做出的杰出工作，同时感谢以下团队与协作者的支持与贡献：

- **Ant Group SCT Team:** Yongfei Xu, Qianyu Zhang, Zekai Gu, ZhiLin Huang, Fakang Wang, Jianhao Fu, Zhuoxuan Du, Xia Zhan, Chun Huang, Qi Liu, Xi Chen, Yuhan Mao, Peipeng Cheng, Hanlin Gao, Jinghua Yao
- **Ant Group Venus Team:** Jinzhen Lin
- **SGLang Community:** Peng Zhang

## 附录 A. 预填充结果

### A.1 Humming PP2 预填充：基线 vs. 最终配置

| 输入长度 | 基线 TTFT (ms) | 基线总输入吞吐量 (tokens/s) | 最终 TTFT (ms) | 最终总输入吞吐量 (tokens/s) |
|---|---:|---:|---:|---:|
| 4K | 775.8 | 5,280 | 573.3 | 7,140 |
| 8K | 1202.1 | 6,810 | 907.6 | 9,030 |
| 16K | 2059.8 | 7,950 | 1649.5 | 9,930 |
| 32K | 4137.5 | 7,920 | 2470.3 | 13,260 |
| 64K | 6195.7 | 10,580 | 4063.8 | 16,130 |
| 128K | 10744.4 | 12,200 | 7975.9 | 16,430 |
| 256K | 20542.2 | 12,760 | 15507.2 | 16,900 |
| 512K | 44544.6 | 11,770 | 34982.6 | 14,990 |
| 1M | 100304.2 | 10,450 | 79214.2 | 13,240 |

### A.2 Humming PP4 预填充：基线 vs. 最终配置

| 输入长度 | 基线 TTFT (ms) | 基线总输入吞吐量 (tokens/s) | 最终 TTFT (ms) | 最终总输入吞吐量 (tokens/s) |
|---|---:|---:|---:|---:|
| 4K | 924.6 | 4,430 | 687.9 | 5,950 |
| 8K | 1174.5 | 6,970 | 890.3 | 9,200 |
| 16K | 2202.0 | 7,440 | 1635.4 | 10,020 |
| 32K | 4185.6 | 7,830 | 3068.4 | 10,680 |
| 64K | 5252.4 | 12,480 | 3982.6 | 16,460 |
| 128K | 7793.4 | 16,820 | 5882.5 | 22,280 |
| 256K | 13210.7 | 19,840 | 10348.9 | 25,330 |
| 512K | 26350.1 | 19,900 | 20273.1 | 25,860 |
| 1M | 55532.3 | 18,880 | 43742.5 | 23,970 |

## 附录 B. 低延迟解码结果

### B.1 各输入长度与 batch size 下的峰值 TPOT

#### B.1.1 No-Spec PP2-TP8

| 输入长度 / Batch Size (峰值 TPOT, ms) | 1 | 2 | 4 | 8 | 16 |
|---|---:|---:|---:|---:|---:|
| 8K | 26.39 | 30.86 | 31.31 | 31.79 | 31.74 |
| 32K | 25.72 | 26.58 | 27.81 | 31.06 | 37.97 |
| 64K | 25.75 | 26.62 | 28.13 | 29.19 | 38.75 |
| 128K | 25.94 | 26.94 | 28.38 | 29.75 | 38.51 |
| 256K | 26.08 | 27.21 | 28.84 | 32.43 | 38.83 |
| 512K | 26.25 | 27.51 | 29.16 | 33.70 | - |
| 1M | 26.42 | 27.81 | 29.52 | - | - |

#### B.1.2 Optimized DSpark PP2-TP8

| 输入长度 / Batch Size (峰值 TPOT, ms) | 1 | 2 | 4 | 8 | 16 | 32 |
|---|---:|---:|---:|---:|---:|---:|
| 4K | 5.91 | 6.76 | 7.97 | 10.00 | 14.55 | 19.23 |
| 8K | 5.80 | 6.87 | 8.85 | 10.48 | 15.18 | 19.60 |
| 32K | 6.14 | 7.04 | 8.39 | 10.83 | 14.86 | 20.46 |
| 64K | 6.15 | 7.13 | 8.73 | 10.39 | 15.49 | 21.65 |
| 128K | 6.77 | 7.02 | 8.91 | 11.59 | 16.17 | 24.78 |
| 256K | 5.76 | 6.98 | 8.61 | 11.98 | 17.72 | - |
| 512K | 6.35 | 7.95 | 9.87 | 14.30 | - | - |
| 1M | 6.65 | 8.92 | 12.43 | - | - | - |

### B.2 Batch Size 1 输出吞吐量

| 输入长度 | No-Spec PP2-TP8 (tokens/s) | Optimized DSpark PP2-TP8 (tokens/s) | 单节点 TP8 (tokens/s) |
|---|---:|---:|---:|
| 4K | - | 169 | 213 |
| 8K | 38 | 172 | 260 |
| 16K | - | - | 244 |
| 32K | 39 | 163 | 269 |
| 64K | 39 | 163 | 246 |
| 128K | 39 | 148 | 267 |
| 256K | 38 | 174 | 271 |
| 512K | 38 | 157 | 254 |
| 1M | 38 | 150 | 183 |

### B.3 基准测试设置

硬件：一台 8× H20-141GB 解码节点。

**解码服务端**

```bash
--tp-size 8 \
--mem-fraction-static 0.91 \
--max-running-requests 1 \
--cuda-graph-max-bs 1 \
--cuda-graph-bs 1 \
--moe-runner-backend humming \
--moe-a2a-backend none \
--speculative-algorithm DSPARK \
--speculative-num-draft-tokens 7 \
--speculative-dspark-block-size 7 \
--speculative-moe-runner-backend triton \
--speculative-moe-a2a-backend none
```

**客户端基准测试**

```bash
python3 -m sglang.bench_serving \
  --backend sglang-oai-chat \
  --host 127.0.0.1 \
  --port 8000 \
  --model <MODEL_PATH> \
  --dataset-name random \
  --dataset-path <DATASET_PATH> \
  --random-input-len 262144 \
  --random-output-len 4096 \
  --random-range-ratio 1.0 \
  --num-prompts 10 \
  --max-concurrency 1 \
  --warmup-requests 0 \
  --seed 1
```

输出吞吐量从服务端 TP0 的 `Decode batch` 日志行中提取；我们丢弃最高与最低各 20% 的样本，对余下样本取平均。B300 的数字遵循所链接来源中报告的设置。

## 附录 C. 高吞吐解码结果

### C.1 DP32-EP32：FP8 + MTP (3, 1, 4)

| 输入长度 / 每 DP rank 并发请求数 (tokens/s/GPU) | 1 | 2 | 4 | 8 | 16 | 32 |
|---|---:|---:|---:|---:|---:|---:|
| 4K | 30.49 | 58.58 | 102.89 | 174.75 | 253.15 | 319.92 |
| 8K | 30.34 | 58.29 | 102.38 | 174.67 | 251.62 | 318.32 |
| 16K | 29.70 | 56.55 | 99.47 | 170.01 | 242.22 | 302.43 |
| 32K | 29.58 | 56.35 | 98.28 | 164.26 | 234.13 | - |
| 64K | 29.07 | 55.73 | 96.43 | 161.60 | - | - |
| 128K | 28.39 | 54.06 | 92.89 | 153.55 | - | - |
| 256K | 28.35 | 53.02 | 90.89 | - | - | - |
| 512K | 27.51 | 51.49 | - | - | - | - |
| 1M | 27.05 | - | - | - | - | - |

### C.2 DP32-EP32：FP8 + Optimized MTP (3, 1, 4)

| 输入长度 / 每 DP rank 并发请求数 (tokens/s/GPU) | 1 | 2 | 4 | 8 | 16 | 32 |
|---|---:|---:|---:|---:|---:|---:|
| 4K | 36.84 | 69.86 | 131.96 | 232.94 | 389.94 | 514.77 |
| 8K | 32.58 | 69.51 | 131.53 | 222.06 | 348.80 | 416.82 |
| 16K | 31.89 | 67.44 | 127.79 | 216.14 | 341.85 | 395.99 |
| 32K | 31.49 | 67.21 | 124.49 | 208.83 | 337.97 | - |
| 64K | 30.95 | 66.47 | 123.68 | 205.44 | - | - |
| 128K | 30.22 | 64.47 | 119.14 | - | - | - |
| 256K | 30.18 | 63.23 | - | - | - | - |
| 512K | 29.28 | 61.40 | - | - | - | - |
| 1M | 28.79 | - | - | - | - | - |

### C.3 DP32-EP32：FP8 + DSpark

| 输入长度 / 每 DP rank 并发请求数 (tokens/s/GPU) | 1 | 2 | 4 | 8 | 16 | 32 |
|---|---:|---:|---:|---:|---:|---:|
| 4K | 53.1 | 94.8 | 181.2 | 338.1 | 495.8 | 591.8 |
| 8K | 44.5 | 88.4 | 170.1 | 317.3 | 495.5 | - |
| 16K | 43.6 | 88.3 | 165.3 | 308.8 | 455.5 | - |
| 32K | 43.0 | 87.3 | 161.0 | 298.4 | - | - |
| 64K | 42.3 | 86.3 | 158.0 | - | - | - |
| 128K | 41.3 | 83.8 | - | - | - | - |
| 256K | 41.2 | - | - | - | - | - |
| 512K | 40.0 | - | - | - | - | - |
| 1M | 39.3 | - | - | - | - | - |

### C.4 DP32-EP32：Humming MXFP4AFP8 + Online C128 + DSpark

| 输入长度 / 每 DP rank 并发请求数 (tokens/s/GPU) | 1 | 2 | 4 | 8 | 16 | 32 |
|---|---:|---:|---:|---:|---:|---:|
| 4K | 75.32 | 127.10 | 235.85 | 417.53 | 564.08 | 703.15 |
| 8K | 75.60 | 128.29 | 238.01 | 417.34 | 560.68 | 709.64 |
| 16K | 74.00 | 124.47 | 231.25 | 406.21 | 539.72 | 674.19 |
| 32K | 73.07 | 122.27 | 225.28 | 392.47 | 521.70 | 601.67 |
| 64K | 71.81 | 120.92 | 221.05 | 386.11 | 516.54 | 599.63 |
| 128K | 70.12 | 117.29 | 212.93 | 366.88 | 487.69 | - |
| 256K | 70.03 | 115.03 | 208.35 | 345.21 | 457.62 | - |
| 512K | 67.95 | 111.71 | 191.99 | 302.80 | - | - |
| 1M | 66.82 | 105.82 | 177.48 | - | - | - |

### C.5 DP16-EP16：Humming MXFP4AFP8 + Online C128 + DSpark

| 输入长度 / 每 DP rank 并发请求数 (tokens/s/GPU) | 1 | 2 | 4 | 8 | 16 | 32 |
|---|---:|---:|---:|---:|---:|---:|
| 4K | 76.80 | 129.62 | 236.83 | 397.42 | 584.37 | 759.73 |
| 8K | 76.69 | 130.55 | 237.53 | 398.60 | 582.03 | 762.09 |
| 16K | 76.16 | 127.88 | 233.10 | 388.54 | 571.22 | 745.23 |
| 32K | 74.07 | 124.77 | 226.24 | 378.79 | 559.05 | 722.51 |
| 64K | 74.57 | 124.69 | 223.84 | 373.13 | 541.46 | 695.35 |
| 128K | 72.36 | 120.34 | 219.66 | 365.13 | 518.98 | - |
| 256K | 71.38 | 119.19 | 211.64 | 340.72 | - | - |
| 512K | 69.54 | 115.14 | 198.81 | - | - | - |
| 1M | 67.39 | 106.50 | - | - | - | - |

## 附录 D. 容量结果

### D.1 解码容量扩展

| 解码配置 | 配置 | 全 token 容量 (tokens/rank) | 相对上一阶段 | 相对 FP8 基线 |
|---|---|---:|---:|---:|
| DP32-EP32 | Baseline FP8 + Offline C128 | 1,475,328 | - | 1.00× |
|  | Humming MXFP4AFP8 + Offline C128 | 2,526,720 | 1.71× | 1.71× |
|  | Humming MXFP4AFP8 + Online C128 | 5,731,328 | 2.268× | 3.88× |
| PP2-TP8 | Baseline FP8 + Offline C128 | 1,089,024 | - | 1.00× |
|  | Humming MXFP4AFP8 + Offline C128 | 4,869,888 | 4.47× | 4.47× |
|  | Humming MXFP4AFP8 + Online C128 | 11,044,906 | 2.268× | 10.14× |

### D.2 Humming 精度验证

我们在 GSM8K1000 上评估了 DP16-EP16 Humming MXFP4AFP8 + Online C128 + DSpark 配置。该配置达到 **95.5% 精确匹配准确率**，有 1 个无效响应、0 次系统错误，通过了我们 **95.0% 的验收阈值**。

作为公开参考，上游 [SGLang Humming 集成](https://github.com/sgl-project/sglang/pull/23754)报告了在 DeepSeek-V4-Flash 的 200 例 GSM8K 评估上的如下结果：

| 后端 | GSM8K 准确率 |
|---|---:|
| Marlin MXFP4A16 | 96.5%–97.0% |
| FlashInfer MXFP4 | 96.5%–97.0% |
| Humming MXFP4A16 | 96.5%–97.5% |
| Humming MXFP4AFP8 | 97.0% |

在这一公开对比中，Humming MXFP4AFP8 没有可见的精度下降。由于该对比使用的是 DeepSeek-V4-Flash 而非 DeepSeek-V4-Pro，我们将其视为外部参考，而不是针对我们服务配置的同等条件精度损失测量。
