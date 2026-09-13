---
title: "vLLM × HPC-Ops：来自腾讯混元的高性能注意力与 MoE 后端"
title_en: "vLLM × HPC-Ops: High-Performance Attention and MoE Backends from Tencent Hunyuan"
source: https://vllm.ai/blog/2026-07-06-vllm-hpc-ops
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM × HPC-Ops：来自腾讯混元的高性能注意力与 MoE 后端

> 原文：[vLLM × HPC-Ops: High-Performance Attention and MoE Backends from Tencent Hunyuan](https://vllm.ai/blog/2026-07-06-vllm-hpc-ops) · vLLM 博客

作者：腾讯混元 AI Infra 团队与 vLLM 团队

[#性能](https://vllm.ai/blog/tags/performance)[#注意力](https://vllm.ai/blog/tags/attention)[#MoE](https://vllm.ai/blog/tags/moe)[#hpc-ops](https://vllm.ai/blog/tags/hpc-ops)

## **TL;DR**

来自 **HPC-Ops** 的注意力与 MoE 内核——HPC-Ops 是腾讯混元 AI Infra 团队打造的生产级算子库——现已作为一等后端进入 vLLM `main` 分支（[Attention PR #46020](https://github.com/vllm-project/vllm/pull/46020)、[MoE PR #45924](https://github.com/vllm-project/vllm/pull/45924)）。两者都针对 NVIDIA Hopper 架构优化，在 H20 上效果最佳：

- **注意力：** 一个逐步的、负载均衡的解码调度器，外加融合的 RoPE + QK-Norm + KV 写入前奏（prologue）。在混合长度解码上，最高比静态 split-KV 调度快 **2.95×**，平均比 FlashInfer 和 FlashAttention 快 **2.25×**。
- **MoE：** 一条完全融合的低延迟 FP8 MoE 流水线。TP8 / EP1 下平均比 Triton 和 CUTLASS 快 **1.59×**，TP1 / EP8 下快 **1.21×**，输出质量与基线相当。

在 8× H20 上对 Hy3 做端到端测试，两个后端合起来相比 vLLM 默认后端把 TTFT 削减约 **24%**、TPOT 削减约 **17%**。

两者都通过 vLLM 自带的后端接口接入原版 vLLM——无需改动源码，也没有长期分叉。

本文涵盖三件事：HPC-Ops 是什么、这两个上游化后端如何设计与集成，以及它们在 H20 上的表现。

## **为什么重要**

生产环境的 LLM 服务早已不是大多数内核最初调优时面对的那种均匀、单轮的批。真实流量是动态且混合长度的，模型越来越是带长上下文的 MoE，智能体负载则把两者都推得更紧。在这个规模上，延迟的很大一部分取决于内核能否在 GPU 上合理安排工作、并在阶段之间高效搬运数据，而不只是裸的 matmul 吞吐。在注意力解码中，固定的 split-KV 调度会被混合批里最长的请求卡住，同时让短请求的计算空转。在 MoE 中，每个专家的 GEMM 都很小，传统流水线要把 token gather 进按专家划分的缓冲区，每个阶段都付出发射开销，中间结果还要在 HBM 里来回搬运。

vLLM 已经为社区提供了快速、灵活的服务引擎；剩下的延迟与吞吐量就取决于注意力和 MoE 内核吸收这些杂乱真实流量的能力。这正是 HPC-Ops 的目标——一个在腾讯大规模生产服务中打磨过的算子库，服务 Hy3 的同一批内核现已作为一等注意力与 MoE 后端上游进 vLLM。

## **Hy3 系列模型简介**

Hy3 是腾讯混元面向智能体执行、编程和长程推理的混合专家模型。它只激活 295B 参数中的 21B，就达到同尺寸级别中最强的智能体能力之一——可与比它大 2–3× 的开源旗舰模型抗衡——同时大幅减少幻觉，多轮使用更可靠。其底层采用 192 个专家、top-8 路由、GQA 注意力（64 个查询头、8 个 KV 头、头维度 128）、256K 上下文窗口，以及用于投机解码的 3.8B MTP 层；提供 BF16 和 FP8（Hy3-FP8）两个版本。

本文有意不谈模型本身——谈的是服务它的内核，接下来就进入正题。

## **HPC-Ops：进入 vLLM 的生产级算子库**

[HPC-Ops](https://github.com/Tencent/hpc-ops) 是一个面向 LLM 推理的开源算子库，由腾讯混元 AI Infra 团队构建和维护。它聚焦主导真实服务延迟与吞吐的热路径——注意力、MoE、GEMM、采样、归一化以及通信-计算融合——原生支持 BF16 和 FP8，并提供可无缝嵌入推理框架的简洁 Python API。内核针对 NVIDIA Hopper 架构优化，在 H20 上表现尤为突出。

这些内核已在腾讯自身大规模混元生产服务中得到验证。本次发布中，其中两个已作为一等后端上游进 vLLM：

| vLLM 后端 | 优化内容 | 精度 | 合入 |
| --- | --- | --- | --- |
| 注意力 | 负载均衡解码 + 融合 RoPE/QK-Norm 前奏 | BF16 / FP8 | [PR #46020](https://github.com/vllm-project/vllm/pull/46020) |
| 融合 MoE | 完全融合的低延迟 MoE 流水线 | FP8 | [PR #45924](https://github.com/vllm-project/vllm/pull/45924) |

本文余下部分聚焦这两个后端。

## **注意力后端：动态负载均衡调度**

### **挑战：每个批里都有的混合长度解码**

解码时，每个 token 生成步都要对请求的完整 KV 缓存做注意力。积累了 16K token 上下文的请求，计算量大约是刚从 1K 起步的请求的 16 倍。生产服务中输出长度不可预测，连续批处理又让处于生成不同阶段的请求进入同一次内核发射——所以单个批里很常见地混着极短与极长的序列。

现有解码内核通过固定的发射网格把工作映射到 CTA，键为 KV 头、请求和 split-KV 块索引——而且 split-KV 度数必须在所有请求间统一，这迫使你在两个都不好的选项里选。固定切分数，最长序列就会主导一切：短请求的 CTA 用零头时间就跑完，然后闲置。改为固定块大小，切分数就必须设为任何请求所需的最大值，短请求被空块填充——这些空块照样发射、发现无活可干、然后退出——浪费调度槽位。无论哪种方式，内核总时长都由最重的 CTA 决定，其余 CTA 干等，SM 周期白白浪费。

### **解决方案：逐步的负载均衡解码调度器**

HPC-Ops 注意力后端用扁平的持久化（persistent）设计取代固定网格，适应批的实际长度分布而非发射时的切分策略，分三步构建。

- **分配。** 一个轻量的分配内核把每条 KV 序列切成统一的 64-token 瓦片。全部头和请求的瓦片总数除以可用 CTA 数，得到每个 CTA 的预算——即桶大小。瓦片按头优先、批次次之的顺序遍历，依次填入各 CTA 的桶：某个 CTA 的桶装满后，后续瓦片溢出到下一个 CTA。于是长序列按其长度比例分散到多个 CTA，短序列只贡献几个瓦片、不会独占一个 CTA。每个 CTA 有最小工作量下限，避免总工作量小时过度切分，保证块数可控、下游合并成本不会盖过调度收益。得到的任务映射每个解码步只计算一次，并被该步的每个 transformer 层复用，其开销摊薄到近乎为零。
- **计算与合并。** 一个持久化的内核网格随之运行：每个 CTA 循环处理自己分到的任务桶——取一个任务描述符、为该块计算注意力、把部分输出和 log-sum-exp 写入 split 缓冲区，再推进到下一个任务，直到遇到终止符。因为网格是持久化的，任务之间没有重新发射的开销，波次之间也没有空闲间隙——每个 SM 在整个内核期间保持饱和。最后一个轻量的合并内核读取每个（头，请求）对的块数，把每块的部分结果归约成最终的 BF16 输出。

净效果是：无论序列长度分布多么倾斜，所有 CTA 的负载都大致相等、几乎同时完成。静态调度固有的长尾停顿被消除，此前浪费在空等上的 GPU 周期转化为有效计算。

![动态分区：统一切片与均衡分桶](https://vllm.ai/blog-assets/figures/2026-07-06-vllm-hpc-ops/dynamic-partitioning.png)

动态分区：统一切片与均衡分桶

### **融合的注意力前奏**

注意力运行之前，每层通常要按独立的、访存受限的步骤依次执行 QK-Norm、RoPE 和 KV 缓存写入——FP8 下还要加一次查询量化。HPC-Ops 把它们融合成单个算子（`HpcRopeNorm`）：从融合 QKV 投影出发，按模型要求的顺序执行 QK-Norm 与 RoPE（Hy3 先归一化再 RoPE），把 K 和 V 直接写入分页缓存，FP8 下还输出带 scale 的逐 token、逐头 FP8 查询，使注意力内核无需再量化。一个内核取代了这些独立发射及其 HBM 往返——在预填充和解码中，每一层的注意力前奏都适用。

### **与 vLLM 集成**

HPC-Ops 注意力 API 作为原生注意力后端集成进 vLLM，与 FlashAttention、FlashInfer 等现有后端并列。具体来说，`HpcAttentionBackend` 继承自 vLLM 的 `AttentionBackend` 基类，并通过标准的后端注册机制注册。

## **MoE 后端：融合的低延迟 FP8 MoE 流水线**

### **挑战：小的专家 GEMM 与其周边开销**

MoE 推理有两种差异极大的工况。大批高吞吐下，专家 GEMM 很大且受计算约束，现有实现通常表现不错。低延迟解码则相反：每个专家只收到少量 token，专家 GEMM 小且受访存约束。为大型 matmul 调优的内核在这些形状上填不满 GPU，而且每个专家产生的瓦片数量不一、且随步数变化，这些小瓦片很难在 GPU 上均匀铺开。

GEMM 周边的工作让情况更糟。传统 MoE 路径是一串独立内核：路由 token、gather 进按专家划分的缓冲区、Gate-Up GEMM、激活与量化、Down GEMM，以及回到 token 位置的 top-k 加权归约。gather 在任何 matmul 开始前就把收集好的 token 张量物化到 HBM，每个阶段都要付出自己的内核发射和中间结果的 HBM 往返。在 GEMM 本身已经很小的解码中，这些全部堆在 GEMM 工作旁边。

### **解决方案：融合的 FP8 MoE 流水线**

HPC-Ops MoE 后端重构了整条 MoE 路径：路由与索引预处理、Gate-Up GEMM、激活与量化、Down GEMM、top-k 加权归约全部融合进一条紧凑的执行路径，去掉了多阶段设计的冗余开销。

- **路由与索引构建。** 一次共享内存计数把 token 分配给专家并保证每个专家的输出范围连续，削减大规模 token 路由的全局原子操作压力，并构建 GEMM 可直接消费的路由索引和逐瓦片任务映射。
- **Gate-Up GEMM。** Gate-Up GEMM 通过路由索引直接读取原始 token，跳过独立的 gather 步骤。激活与 FP8 量化随后作为单独的融合内核运行，其输出由 Down GEMM 直接读取。
- **占用优先，不用 warp specialization。** 单个 warp 组同时处理数据搬运与计算，把访存延迟隐藏从 CTA 内软件流水线转移到跨 CTA 的硬件调度上，提高每 SM 常驻 CTA 数。以保持每个 SM 占满为目标的持久化网格随后消费任务映射，把小而不均的逐专家瓦片均匀铺到各 CTA 上。
- **PDL 链式衔接的阶段。** Programmatic Dependent Launch（PDL）让每次内核发射与前一个内核的尾部重叠，抹掉阶段之间的气泡，一直延伸到最终的 top-k 加权归约——后者还可以把共享专家的输出合并进来。

这些加在一起，把中间结果和发射请出了关键路径。专家以 FP8 运行，同时支持逐张量与分块缩放，输出质量与基线相当。

### **与 vLLM 集成**

HPC-Ops 融合 MoE API 作为原生 MoE 后端集成进 vLLM，与 DeepGEMM、Triton 等现有后端并列。具体来说，`HPCExperts` 继承自 vLLM 的 `FusedMoEExpertsModular` 基类，并通过标准的后端注册机制注册。

## **在 vLLM 中使用 HPC-Ops 后端**

本指南介绍如何在 vLLM 中启用 [HPC-Ops](https://github.com/Tencent/hpc-ops) 后端（注意力与 MoE）。

### **安装**

开始之前，先从源码安装 **HPC-Ops**：

```
git clone https://github.com/Tencent/hpc-ops.git
cd hpc-ops

# Build and install the wheel package
make wheel
python3 -m pip install dist/*.whl
```

### **快速上手**

HPC-Ops 注意力后端目前只支持 **Hy3 系列**模型。

要用 HPC-Ops 注意力后端为标准 Hy3 模型启动 vLLM 服务器，运行：

```
vllm serve tencent/Hy3 \
    --tensor-parallel-size 8 \
    --attention-backend HPC_ATTN
```

对于 **Hy3-FP8** 模型，还需要几个额外选项：

```
vllm serve tencent/Hy3-FP8 \
    --tensor-parallel-size 8 \
    --attention-backend HPC_ATTN \
    --kv-cache-dtype fp8_e4m3 \
    --block-size 64
```

**提示：** 要为自定义模型启用 HPC-Ops 注意力后端，把模型 `forward` 方法中的 `rope_norm` 替换为 `HpcRopeNorm`。参考 PR [#46020](https://github.com/vllm-project/vllm/pull/46020)。

HPC-Ops MoE 后端**仅支持 FP8 模型**。

要用 HPC-Ops MoE 后端启动 vLLM 服务器，运行：

```
vllm serve tencent/Hy3-FP8 \
    --tensor-parallel-size 8 \
    --moe-backend hpc
```

### **硬件支持**

HPC-Ops 后端目前仅支持 NVIDIA Hopper 架构 GPU，在 H20 上性能最佳。

## **H20 上的性能**

### **融合 MoE：HPC-Ops 对比 Triton / CUTLASS**

我们在 Hy3 模型配置下、TP8 / EP1 和 TP1 / EP8 两种设置上，把 HPC-Ops MoE 后端与 Triton 和 CUTLASS MoE 后端做了对比。按批大小取平均，TP8 / EP1 下 HPC-Ops 比最佳基线快 1.59×，TP1 / EP8 下快 1.21×，收益最大的是主导低延迟解码的中小批大小。

表 1：TP8 / EP1（专家权重分片到 8 个 rank）下不同批大小的 FusedMoE 延迟（µs）

| 批大小 | HPC-Ops (µs) | Triton (µs) | CUTLASS (µs) |
| --- | --- | --- | --- |
| 4 | 42.0 | 56.4 | 74.5 |
| 16 | 85.7 | 124.2 | 209.2 |
| 32 | 124.0 | 184.3 | 275.6 |
| 64 | 147.2 | 374.9 | 330.3 |
| 128 | 161.5 | 302.9 | 345.3 |
| 256 | 170.1 | 310.9 | 351.6 |
| 512 | 194.5 | 331.6 | 369.2 |
| 1024 | 281.4 | 652.7 | 438.3 |
| 2048 | 491.8 | 731.5 | 794.4 |
| 4096 | 872.0 | 1366.0 | 1230.7 |
| 8192 | 1695.0 | 2216.8 | 2362.9 |
| 16384 | 3241.9 | 4329.1 | 4364.4 |

表 2：TP1 / EP8（专家分片到 8 个 rank）下不同批大小的 FusedMoE 延迟（µs）

| 批大小 | HPC-Ops (µs) | Triton (µs) | CUTLASS (µs) |
| --- | --- | --- | --- |
| 4 | 118.6 | 147.4 | 140.4 |
| 8 | 136.7 | 192.8 | 170.7 |
| 16 | 149.8 | 198.4 | 263.5 |
| 32 | 153.6 | 214.6 | 264.4 |
| 64 | 166.5 | 358.1 | 266.8 |
| 128 | 213.5 | 251.7 | 272.6 |
| 256 | 386.2 | 454.9 | 493.5 |
| 512 | 705.5 | 691.7 | 741.7 |
| 1024 | 1342.6 | 1369.1 | 1359.1 |
| 2048 | 2513.9 | 2668.7 | 2530.4 |

![HPC-Ops FusedMoE 在 H20 上 — Hy3](https://vllm.ai/blog-assets/figures/2026-07-06-vllm-hpc-ops/fused-moe-latency.png)

HPC-Ops FusedMoE 在 H20 上 — Hy3

### **混合长度批下的解码：动态对比静态调度**

注意力后端最大的亮点是混合长度批上的解码。为了单独考察调度器，我们把 FP8 解码从均匀分布扫到高度倾斜的 KV 长度分布（标记 A×B 表示 A 个请求、KV 长度为 B），并将 HPC-Ops 动态调度与静态 split-KV 调度、FlashInfer 和 FlashAttention 对比。相对静态调度的优势随倾斜度增大，从小型均匀批的持平到 1×128K + 31×4K 混合下的 2.95×。在这些用例中，动态调度平均比 FlashInfer 与 FlashAttention 中最好的那个快 2.25×。

表 3：不同 KV 长度分布下的解码延迟（ms）

| 解码场景 | HPC-Ops 动态 (ms) | HPC-Ops 静态 (ms) | FlashInfer (ms) | FlashAttention (ms) | 动态对比静态 |
| --- | --- | --- | --- | --- | --- |
| 64×0.5K | 0.013 | 0.013 | 0.050 | 0.025 | 1.00× |
| 64×4K | 0.033 | 0.043 | 0.221 | 0.095 | 1.32× |
| 32×0.125K + 32×4K | 0.020 | 0.033 | 0.119 | 0.053 | 1.59× |
| 2×32K + 30×4K | 0.032 | 0.056 | 0.169 | 0.094 | 1.76× |
| 1×64K + 15×4K | 0.042 | 0.097 | 0.118 | 0.065 | 2.32× |
| 1×128K + 31×4K | 0.063 | 0.186 | 0.220 | 0.097 | 2.95× |

![H20 上的解码注意力 — Hy3：动态对比静态调度](https://vllm.ai/blog-assets/figures/2026-07-06-vllm-hpc-ops/decode-dynamic-vs-static.png)

H20 上的解码注意力 — Hy3：动态对比静态调度

### **注意力：HPC-Ops 对比 FlashAttention / Triton / FlashInfer**

我们进一步用 vLLM 的注意力基准，在预填充、扩展（extend）和解码形状上把 HPC-Ops 注意力后端与 FlashAttention、Triton 和 FlashInfer 对比。在这些形状上，几乎每种情况下 HPC-Ops 都与三者中最快者持平或更快。

表 4：注意力延迟（ms），对比 FlashAttention、Triton 和 FlashInfer

| Batch Spec | 类型 | 批大小 | HPC-Ops (ms) | FlashAttention (ms) | Triton (ms) | FlashInfer (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| q512 | 预填充 | 1 | 0.047 | 0.069 | 0.123 | 0.070 |
| q1ks2k | 扩展 | 1 | 0.406 | 0.431 | 1.132 | 0.431 |
| q2k | 预填充 | 1 | 0.530 | 0.574 | 1.525 | 0.609 |
| q4k | 预填充 | 1 | 2.002 | 2.093 | 5.816 | 2.144 |
| q8k | 预填充 | 1 | 7.883 | 7.957 | 22.702 | 8.084 |
| 2q1ks4k | 扩展 | 2 | 1.835 | 1.830 | 5.046 | 1.829 |
| 8q1s1k | 解码 | 8 | 0.019 | 0.031 | 0.035 | 0.021 |
| 16q1s2k | 解码 | 16 | 0.054 | 0.098 | 0.106 | 0.052 |
| 32q1s1k | 解码 | 32 | 0.057 | 0.102 | 0.080 | 0.058 |
| 64q1s4k | 解码 | 64 | 0.299 | 0.620 | 0.510 | 0.340 |

### **端到端：8× H20 上的 Hy3**

最后，我们在 8× NVIDIA H20 GPU 上评估了 Hy3 模型搭配 HPC-Ops MoE 与注意力后端、对比 vLLM 默认后端的端到端（E2E）性能。在所有测试用例中，HPC-Ops 后端都稳定优于 vLLM 默认后端，TTFT 和 TPOT 都有大幅降低：TTFT 平均下降约 24%，TPOT 平均下降约 17%，最大批大小时 TPOT 改善达到约 30%。

表 5：不同批大小下的 TPOT（输出长度 = 4K）

| 批大小 | 基线 TPOT (ms) | HPC TPOT (ms) | 改善 |
| --- | --- | --- | --- |
| 1 | 8.00 | 7.76 | +3.0% |
| 4 | 11.14 | 10.67 | +4.2% |
| 8 | 13.49 | 11.31 | +16.2% |
| 16 | 17.98 | 13.56 | +24.6% |
| 32 | 24.13 | 18.32 | +24.1% |
| 64 | 31.10 | 21.90 | +29.6% |

表 6：不同批大小下的 TTFT（输入长度 = 8k，关闭 Chunked Prefill，关闭前缀缓存）

| 批大小 | 基线 TTFT (ms) | HPC TTFT (ms) | 改善 |
| --- | --- | --- | --- |
| 1 | 565.69 | 431.00 | +23.8% |
| 4 | 1920.15 | 1471.43 | +23.4% |
| 8 | 3948.22 | 3035.44 | +23.1% |
| 16 | 7807.18 | 5885.63 | +24.6% |

表 7：不同输入长度下的 TTFT（批大小 = 16，关闭 Chunked Prefill，关闭前缀缓存）

| 输入长度 | 基线 TTFT (ms) | HPC TTFT (ms) | 改善 |
| --- | --- | --- | --- |
| 2k | 1792.62 | 1363.13 | +24.0% |
| 4k | 3704.27 | 2886.40 | +22.1% |
| 8k | 7807.12 | 5893.93 | +24.5% |

## **下一步**

这只是与 vLLM 社区更长合作的开始。我们会继续与 vLLM 维护者和贡献者合作，改进和扩展这些能力，并在工作成熟后继续上游化。欢迎反馈、issue 和基准测试结果，期待与大家一起构建开放的高性能推理。

## **致谢**

我们感谢跨团队协作、把这些后端带进 vLLM 的众多同事：

- **腾讯混元 AI Infra** —— 构建并优化 HPC-Ops 注意力与 MoE 内核，并作为后端贡献给 vLLM。Sethran Liu、Chase Shao、Shengy Wei、Theo Cheng、Ryann Xue、Lando Jiang、Looper Zhao、Haank Lin、Aiden Ren、Lehua Ding、Chengv Jiang、Steven Kuang、Liqi He、Kipper Gong、Reedlau Liu、Raccoon Liu、Dick Zhu。
- **腾讯网络平台部** —— 在通信优化方面的紧密合作。Xuan Zhang、Haoran Zhao、Yuanyuan Gong、Yadong Liu、Jinzhu Wang、Yinben Xia、Xiang Li、Quan Wen、Zekun He。
- **vLLM/Inferact** —— 开放的后端接口、评审与设计讨论。Kaichao You、Yongye Zhu、Yifan Qiao。
- **NVIDIA** —— 内核与性能优化方面的紧密合作。Yuanhang Sun、Perkz Zheng、Yuxi Chi、Jiang Shao、Jun Gu、Meng Wang、River Liu、Gary Ji、Chandler Zhou。

我们还感谢更广泛的开源内核社区——这项工作建立在他们的成果之上，也以他们为衡量基准，包括 NVIDIA CUTLASS/CuTe、TensorRT-LLM、FlashInfer、FlashAttention 和 Triton。
