---
title: "HPC-Ops × SGLang：来自腾讯混元的高性能注意力、Router GEMM 与 MoE 算子"
title_en: "HPC-Ops × SGLang: High-Performance Attention, Router GEMM, and MoE Kernels from Tencent Hunyuan"
author: "Tencent Hunyuan AI Infra and the SGLang Team"
date: "August 7, 2026"
previewImg: /images/blog/hpc-ops-sglang/hpc-ops-sglang-cover.webp
type: blog
source: https://lmsys.org/blog/2026-08-07-hpc-ops-sglang/
translated: 2026-09-12
---

# HPC-Ops × SGLang：来自腾讯混元的高性能注意力、Router GEMM 与 MoE 算子

> 原文：[HPC-Ops × SGLang: High-Performance Attention, Router GEMM, and MoE Kernels from Tencent Hunyuan](https://lmsys.org/blog/2026-08-07-hpc-ops-sglang/) · LMSYS Blog · Tencent Hunyuan AI Infra and the SGLang Team

[HPC-Ops](https://github.com/Tencent/hpc-ops) 是一个面向大语言模型推理的开源算子库，已部署于腾讯的大规模生产推理服务。其核心算子（包括 Dynamic Attention 与 Fused MoE）在混元线上推理中发挥着关键作用，可将 Hy3 模型的每 token 生成时间（TPOT）最多降低 48.8%。目前，HPC-Ops 的 Attention、Router GEMM 和 MoE 算子已合入 SGLang 主分支，把这些经过生产环境验证的优化带给开源推理服务社区。

在本文中，我们将介绍 HPC-Ops 中三个重要算子的设计及其与 SGLang 的集成，随后给出 H20 上的算子基准测试与推理服务结果，以及 H200 上的验证结果。这些集成面向 NVIDIA Hopper 架构 GPU（SM90），并已在 Qwen3、Hy3 和 LongCat 负载上完成验证。

## 亮点

- **Attention：**在 H20 上，HPC-Ops 动态调度相比其静态 split-KV 调度最高可达 **2.95×**，在所有测量场景中平均比 FlashInfer 与 FlashAttention 中的最优者快 **2.25×**。在上游 H200 验证中，集成后的 Hy3-FP8 路径配合 FP8 KV 缓存，输出吞吐量相比 FlashAttention 提升 **3.7–5.9%**。
- **Router GEMM：**在 H20 上，HPC-Ops 比 FP32 cuBLAS 快 **1.30–3.22×**，且相对 FP32 cuBLAS 的最大绝对误差仅为 **0.00177**，而 TF32 cuBLAS 为 **0.06464**。在上游 H200 的 LongCat-Flash 内核验证中，相比现有 FP32 路径可带来 **4.31×** 加速。
- **MoE：**在 H20 上，针对 Hy3，相比 SGLang 与 vLLM 基线中的最优者，HPC-Ops 在 TP8 / EP1 下取得平均每批 **1.08×** 加速，在 TP1 / EP8 下取得 **1.21×** 加速。在上游 Qwen3/H200 内核基准测试中，在 8 个 token 时相比 Triton 最高可达 **4.21×**。
- **端到端推理服务：**在 8× H20 上运行 Hy3-FP8，同时启用 HPC-Ops Attention 与 MoE，批大小 4–64 时 TPOT 降低 **15.1–48.8%**，批大小 4–16 时首 token 延迟（TTFT）降低 **3.3–6.0%**。在 8× H20 上运行 LongCat-Flash-Lite-FP8，启用 HPC-Ops Router GEMM 后，批大小 4–64 时输入吞吐量提升 **5.5–6.1%**。

## Attention、路由与专家：MoE 模型推理服务中的三条热点路径

生产环境的 MoE 推理服务很少呈现出孤立内核基准测试中所测的那种均匀负载。它在同一条延迟敏感的路径上，同时混合了长度不一的 Attention 计算、对精度敏感的路由，以及稀疏的专家执行；长上下文、多轮对话与智能体类负载进一步拉大了实际 KV 长度的分布范围。因此，推理服务性能不仅取决于原始的矩阵乘吞吐量，还取决于负载均衡、数值保真度与开销控制。

这些约束集中体现在 MoE 模型推理服务的三个性能关键阶段。解码阶段，Attention 计算量随每个请求的实际 KV 长度伸缩，使混合长度批次成为一个负载均衡问题。Router GEMM 产出用于 top-k 选择的分数，而微小的数值变化就可能改变专家的选择结果。被选中的专家随后处理的是规模小且不均匀的 token 组，这使得元数据构建、token 搬运、中间结果存储和内核启动开销的代价足以与专家 GEMM 本身相当。

HPC-Ops 为每个阶段都提供了专门的算子：面向 Attention 的负载感知调度、面向 Router GEMM 的精度感知设计，以及面向 MoE 的融合流水线——它消除了独立的 gather 操作，并减少启动开销与中间数据搬运。上游集成通过 SGLang 的原生后端与分发接口，把这些算子接入其推理服务运行时。下面各节将逐一说明每个算子的设计。

## Attention：混合长度解码的负载均衡

解码阶段，每个新 token 都要对请求的完整 KV 缓存做注意力计算，因此 Attention 计算量随实际序列长度伸缩。缓存了 16K token 的请求，其 KV 计算量大约是 1K token 请求的 16 倍。在生产环境中，提示与输出长度差异很大，而连续批处理会把处于不同生成阶段的请求放进同一次内核启动；于是一个批次里经常同时出现短 KV 缓存和长达数万 token 的序列。

静态 split-KV 调度把计算映射到一个由 KV 头、请求和 KV 分块构成的固定启动网格上，整个批次共享同一种切分策略。静态 split-KV 调度器通常采用以下两种策略之一，而两者对混合长度批次都表现不佳：(1) 固定切分数量，长请求会产出繁重得多的分块——短请求的 CTA 早早完成，而少数长时间运行的 CTA 决定了内核的尾部耗时；(2) 固定分块大小，网格必须为最长的请求预留足够的切分数量，导致较短的请求留下空或接近空的分块，却仍占用调度槽位。一种策略制造了不均匀的计算量，另一种策略则调度了并不存在的计算。

### 围绕实际 KV 计算量进行调度

HPC-Ops 用一个常驻内核（persistent kernel）取代静态的按请求切分，该内核根据批次的实际长度分布在各 CTA 之间动态均衡 KV tile。对每个解码批次，一个分配内核（assign kernel）会根据实际 KV 长度构建一张全局任务映射表：它把每条序列切成统一的 64-token tile，统计所有头和请求的 tile 总数，再除以常驻 CTA 的数量，得出每个 CTA 的 tile 预算。分配内核会先把每个 CTA 的任务桶（bin）填满至该预算，再溢出到下一个 CTA，因此长序列按其长度比例跨越多个 CTA，短序列则只贡献自己实际拥有的 tile。一个最小计算量下限避免了总计算量较小时过度切分，使下游的合并操作保持廉价。这张任务映射表在每个解码步根据设备侧序列长度生成一次，并在所有 Transformer 层间复用，从而摊薄其开销。

执行时，每个 CTA 处理完自己被分配的 bin。对每个描述符，它在一个或多个连续 KV tile 上计算 Attention，并写出带 log-sum-exp 统计量的部分输出；同一个常驻 CTA 会继续处理下一个描述符，直到自己的 bin 清空。由于每个 CTA 只为给定请求产出部分结果，最后的合并内核（combine kernel）会读取每个请求和头的实际分块数量，并在正确的全局 softmax 归一化下合并这些部分结果。接近相等的 bin 大小保证了各 CTA 大致同时完成，消除了少数超长请求原本会造成的内核尾部。

### 融合的 Attention prologue（前置处理）

针对 Hy3 FP8，HPC-Ops 将 QKV 投影之后的 Attention prologue 融合为一体：先施加 QK-Norm 再做 RoPE，以逐 token、逐头的缩放因子输出 FP8 格式的 Q，并把 K 和 V 直接写入分页的 FP8 缓存。量化后的 Q 及其缩放因子被直接传递给主 Attention 内核，避免重复量化。这条融合路径在预填充和解码两个阶段都消除了中间张量及相应的 HBM 往返和单独的内核启动。

## Router GEMM：在路由精度与吞吐量之间取得平衡

路由精度直接影响 MoE 模型的质量。在每个 MoE 层，路由器把隐藏状态投影为专家分数，对这些分数做 top-k 选择决定了哪些专家参与执行。第 k 名与第 k+1 名专家之间的分数差距可能非常小，因此这一投影的运算精度决定了能否选中正确的专家。

为了保住路由精度，一些生产模型即使在隐藏状态为 BF16 时也保留 FP32 的路由权重。把这些权重转换为 BF16 可以获得 BF16 Tensor Core 的吞吐量，但会丢弃可能翻转 top-k 决策的低位尾数位。完整的 FP32 GEMM 保留了全部权重精度，但 Tensor Core 吞吐量较低。

### 精度感知的 BF16 设计

HPC-Ops 的解法是把 FP32 权重分解为两个 BF16 分量。它通过直接截断提取出 BF16 高位部分 $W_{\mathrm{high}}$，再由缩放后的残差 $(W - W_{\mathrm{high}}) \times 256$ 构造第二个 BF16 分量。原始权重被近似为 $W \approx W_{\mathrm{high}} + W_{\mathrm{low}} / 256$，于是矩阵乘变成两个 BF16 GEMM，其结果通过一次缩放修正合并，从而恢复低位尾数的贡献。单个内核同时完成这两个 BF16 乘法：它只从共享内存加载一次激活 tile，在 FP32 寄存器中累加两份部分结果，在 epilogue 中施加 $1/256$ 缩放，并把最终的 FP32 路由分数写入全局内存。这种设计在把主要运算放在 BF16 Tensor Core 上执行的同时，恢复出接近完整 FP32 GEMM 的精度。

在框架侧，SGLang 在模型加载时缓存分解后的权重对，并在多个请求和 CUDA 图重放之间复用。形状感知分发（shape-aware dispatch）会在实测的交叉点处选择 HPC-Ops 内核或默认路径。低于这些交叉点时，单一 FP32 路径更快，因为两次乘积的开销超过了 Tensor Core 带来的收益。

## MoE：削减小规模专家 GEMM 周边的开销

解码阶段，MoE 层中的每个专家只会收到少量 token。由此产生的专家 GEMM 规模小且属于访存受限（memory-bound），GPU 的 SM 在这些形状下利用率不足。负载不均让问题雪上加霜：路由到每个专家的 token 数量既因专家而异，也随解码步不断变化，很难把这些小而不均匀的 tile 均匀铺到可用的 SM 上。

除了专家 GEMM 本身，环绕它们的操作也带来可观的开销。传统 MoE 路径把多个独立内核串在一起：路由、把 token 收集（gather）到按专家划分的缓冲区、Gate-Up GEMM、激活与量化、Down GEMM，以及按 top-k 加权归约回 token 位置。gather 步骤在任何矩阵乘开始之前，就要在 HBM 中物化一份完整的 token 张量；随后的每个阶段都要为中间结果付出各自的内核启动和 HBM 往返。当 GEMM 规模较小时，这些周边开销会消耗掉该阶段墙钟时间的相当一部分。

### 面向低延迟的融合 MoE 流水线

面向小批量的推理场景，HPC-Ops MoE 后端以任务映射表驱动的常驻专家 GEMM 为核心，把路由与索引预处理、Gate-Up、激活与重量化、Down，以及 top-k 加权归约组织进一条低延迟流水线。

- **路由与索引构建。**从选定的 top-k 专家 ID 出发，一次基于共享内存的计数过程把 token–专家的分配关系整理成连续的按专家划分的输出区间，降低全局原子操作压力，并构建出路由索引和逐 tile 任务映射表，供常驻专家 GEMM 直接消费。
- **Gate-Up 与激活。**Gate-Up GEMM 通过路由索引直接读取原始 token，跳过独立的 gather 及其额外的 HBM 流量。SiLU-and-mul 与 FP8 重量化随后作为一个融合内核运行，其输出由 Down GEMM 直接读取。
- **优先占用率，不用 warp 特化。**由单个 warp 组同时承担数据搬运和矩阵运算，而不是预留独立的生产者与消费者组。这提高了 CTA 驻留率，并把内存延迟的隐藏从 CTA 内的软件流水线转移到跨 CTA 的硬件调度上。常驻网格随后消费这些任务映射表，把小而不均匀的专家 tile 铺开到各 SM 上。
- **以 PDL 链式衔接各阶段。**程序化依赖启动（Programmatic Dependent Launch，PDL）让每个下游内核的启动与前一阶段的收尾重叠执行，缩短 Gate-Up、激活、Down 以及最终的 top-k 加权归约（它把专家输出恢复到 token 顺序）之间的空隙。

这些优化共同减少了关键路径上的中间数据搬运和内核启动开销。

## 从 HPC-Ops 内核到 SGLang

通过 SGLang 的原生后端与分发接口，HPC-Ops 直接作用于推理服务运行时的既有状态，同时仍是一个独立维护的算子库。Attention 直接消费分页 KV 存储和实时的设备侧序列元数据，无需额外的布局转换；Router GEMM 在多个请求和 CUDA 图重放之间复用预处理好的权重与工作区；MoE 则遵循 SGLang 的专家 ID 和划分方式，无需额外的重映射。这些集成既保留了各算子预期的数据通路，又契合 SGLang 现有的执行模型。

三个已集成的算子路径汇总如下：

| HPC-Ops 算子 | 优化内容 | 精度 | 上游 PR |
| --- | --- | --- | --- |
| Attention | 面向混合长度解码的负载均衡，以及融合了 QK-Norm、RoPE、量化与 KV 写入的 prologue | BF16 激活；BF16 或 FP8 E4M3 KV 缓存 | [#30540](https://github.com/sgl-project/sglang/pull/30540), [#32304](https://github.com/sgl-project/sglang/pull/32304) |
| Router GEMM | 精度感知的路由投影，使用 BF16 Tensor Core 同时保留 FP32 权重信息 | BF16 激活 × FP32 权重 → FP32 分数 | [#30247](https://github.com/sgl-project/sglang/pull/30247), [#31943](https://github.com/sgl-project/sglang/pull/31943) |
| MoE | 围绕小而不均匀专家 GEMM 的低开销执行 | BF16 隐藏状态；FP8 E4M3 专家权重 | [#30541](https://github.com/sgl-project/sglang/pull/30541) |

## 快速上手

本指南介绍如何在 SGLang 中使用 [HPC-Ops](https://github.com/Tencent/hpc-ops) 的 Attention、Router GEMM 和 MoE 算子。

### 安装

从源码安装 HPC-Ops：

```bash
git clone https://github.com/Tencent/hpc-ops.git
cd hpc-ops
make wheel
python3 -m pip install dist/*.whl
```

HPC-Ops 已包含在 SGLang 官方的 `x86_64` 开发镜像中（`lmsysorg/sglang:dev`，CUDA 12.9 使用 `lmsysorg/sglang:dev-cu12`），使用这些镜像时无需单独安装。

### Attention 与 MoE

在 SGLang 中，Attention 与 MoE 是两个独立的后端选项，对于 Qwen3、Hy3 等兼容模型，可以单独启用也可以一起启用。下面的示例同时选择两个 HPC-Ops 后端，并启用 FP8 KV 缓存的 Attention 路径：

```bash
python3 -m sglang.launch_server \
  --model tencent/Hy3-FP8 \
  --tp-size 8 \
  --attention-backend hpc_ops \
  --kv-cache-dtype fp8_e4m3 \
  --page-size 64 \
  --moe-runner-backend hpc_ops
```

若使用 BF16 KV 缓存，去掉 `--kv-cache-dtype fp8_e4m3`。若只想使用某一个 HPC-Ops 算子，只指定对应的后端选项即可。

### Router GEMM

在 SGLang 中，HPC-Ops Router GEMM 在 BF16 Tensor Core 上执行矩阵运算的同时，保留 FP32 路由权重的低位信息。这条集成路径已在 LongCat-Flash Chat 和 Lite 上完成验证，并在受支持的模型与路由器形状下被自动选中。安装 HPC-Ops 后，标准的 LongCat-Flash 启动命令即可使用它：

```bash
python3 -m sglang.launch_server \
  --model meituan-longcat/LongCat-Flash-Lite-FP8
```

## 性能评估

HPC-Ops 后端目前支持 NVIDIA Hopper 架构 GPU，并在 H20 上取得最佳性能。下面的评估涵盖 H20 上的算子基准测试、8× H20 上的 SGLang 端到端推理服务，以及上游 SGLang 拉取请求中报告的 H200 结果。

### H20 算子基准测试

**Attention。**

Attention 调度器最突出的收益体现在混合长度解码中，此时同一批次内各请求的 KV 缓存长度可能相差悬殊。我们评估了从均匀到高度偏斜分布下的 FP8 KV 缓存解码；表中 A×B 表示 KV 长度为 B 的 A 个请求。为了隔离调度本身的效果，我们将 HPC-Ops 动态调度与其静态 split-KV 版本对比，FlashInfer 和 FlashAttention 则提供额外基线。动态相对静态的收益随偏斜程度增大，从均匀 64×0.5K 批次上的持平，到 1×128K + 31×4K 混合批次上的 **2.95×**。在全部六个场景中，动态调度平均比每个场景中 FlashInfer 与 FlashAttention 中的最优者快 **2.25×**。

*表 1：H20 上不同 KV 长度分布下的解码延迟。数值越低越好。*

| 解码场景 | HPC-Ops 动态 | HPC-Ops 静态 | FlashInfer | FlashAttention | 动态 vs. 静态 |
| --- | --- | --- | --- | --- | --- |
| 64×0.5K | 0.013 ms | 0.013 ms | 0.050 ms | 0.025 ms | 1.00× |
| 64×4K | 0.033 ms | 0.043 ms | 0.221 ms | 0.095 ms | **1.32×** |
| 32×0.125K + 32×4K | 0.020 ms | 0.033 ms | 0.119 ms | 0.053 ms | **1.59×** |
| 2×32K + 30×4K | 0.032 ms | 0.056 ms | 0.169 ms | 0.094 ms | **1.76×** |
| 1×64K + 15×4K | 0.042 ms | 0.097 ms | 0.118 ms | 0.065 ms | **2.32×** |
| 1×128K + 31×4K | 0.063 ms | 0.186 ms | 0.220 ms | 0.097 ms | **2.95×** |

![H20 mixed-length Attention decode latency](/images/blog/hpc-ops-sglang/h20-attention-dynamic-scheduling.png)

*图 1：实际 KV 计算量的偏斜程度越大，动态调度的效果越显著。数值越低越好。*

**Router GEMM。**

我们首先用一组通用的 $K = 4096, N = 192$ 参数扫描来评估 Router GEMM。在所有测量的 M 值上，HPC-Ops 比 FP32 cuBLAS 快 **1.30–3.22×**，比 TF32 cuBLAS 快 **1.25–1.78×**。以 FP32 cuBLAS 作为数值参考，最大绝对误差保持在 **0.00177** 及以下，而 TF32 为 **0.06464**。

*表 2：H20 上 K = 4096、N = 192 时 BF16 × FP32 Router GEMM 的延迟。数值越低越好。*

| M | HPC-Ops | FP32 cuBLAS | TF32 cuBLAS | 相对 FP32 加速 | 相对 TF32 加速 |
| --- | --- | --- | --- | --- | --- |
| 1 | 11.200 µs | 14.576 µs | 14.048 µs | **1.30×** | **1.25×** |
| 16 | 11.744 µs | 23.808 µs | 18.752 µs | **2.03×** | **1.60×** |
| 48 | 12.144 µs | 31.008 µs | 20.064 µs | **2.55×** | **1.65×** |
| 96 | 13.904 µs | 31.760 µs | 24.720 µs | **2.28×** | **1.78×** |
| 208 | 17.088 µs | 39.280 µs | 28.928 µs | **2.30×** | **1.69×** |
| 512 | 26.992 µs | 86.976 µs | 44.736 µs | **3.22×** | **1.66×** |
| 1024 | 50.640 µs | 110.480 µs | 68.544 µs | **2.18×** | **1.35×** |
| 2048 | 76.688 µs | 198.576 µs | 100.800 µs | **2.59×** | **1.31×** |
| 4096 | 141.120 µs | 403.728 µs | 205.760 µs | **2.86×** | **1.46×** |

![H20 Router GEMM numerical error and cuBLAS latency](/images/blog/hpc-ops-sglang/h20-router-gemm-cublas.png)

*图 2：Router GEMM 相对 FP32 cuBLAS 的数值误差（左），以及相对 FP32 与 TF32 cuBLAS 的延迟（右）。数值越低越好。*

随后我们复测了 LongCat-Flash 使用的两种路由器形状。在 SGLang 的模型感知分发区间内，相比 SGLang 默认实现，HPC-Ops 在 Chat 形状上取得 **1.06–2.83×** 加速，在 Lite 形状上取得 **1.09–2.46×** 加速。

*表 3：H20 上 SGLang 分发区间内 LongCat-Flash Router GEMM 的延迟。数值越低越好。*

| M | Chat 默认 | Chat HPC-Ops | 加速比 | Lite 默认 | Lite HPC-Ops | 加速比 |
| --- | --- | --- | --- | --- | --- | --- |
| 64 | 39.19 µs | 37.01 µs | **1.06×** | — | — | — |
| 128 | 74.18 µs | 59.36 µs | **1.25×** | 25.83 µs | 23.72 µs | **1.09×** |
| 256 | 100.03 µs | 82.47 µs | **1.21×** | 41.87 µs | 34.01 µs | **1.23×** |
| 512 | 190.37 µs | 141.73 µs | **1.34×** | 71.89 µs | 41.95 µs | **1.71×** |
| 1024 | 380.68 µs | 207.00 µs | **1.84×** | 108.64 µs | 74.09 µs | **1.47×** |
| 2048 | 961.15 µs | 339.04 µs | **2.83×** | 235.81 µs | 106.81 µs | **2.21×** |
| 4096 | 1469.70 µs | 670.14 µs | **2.19×** | 423.52 µs | 172.44 µs | **2.46×** |
| 8192 | 2881.00 µs | 1333.84 µs | **2.16×** | 835.22 µs | 339.66 µs | **2.46×** |

![H20 LongCat-Flash Router GEMM latency](/images/blog/hpc-ops-sglang/h20-router-gemm-longcat.png)

*图 3：SGLang 分发区间内 LongCat-Flash Chat（左）与 Lite（右）形状的 Router GEMM 延迟。数值越低越好。*

**MoE。**

对于 MoE，我们在 TP8 / EP1 与 TP1 / EP8 两种 Hy3 形状下，将完整的融合算子与 SGLang、vLLM Triton 以及 vLLM CUTLASS 进行基准对比。取每行三个基线中的最低延迟来计算，HPC-Ops 在 TP8 / EP1 下取得平均每批 **1.08×** 加速，在 TP1 / EP8 下取得 **1.21×** 加速，其中增益最大的正是低延迟解码中常见的小到中等批大小区间。

*表 4：H20 上 TP8 / EP1 时 Hy3 MoE 的延迟。数值越低越好。*

| 批大小 | HPC-Ops | SGLang | vLLM Triton | vLLM CUTLASS | 相对最优加速比 |
| --- | --- | --- | --- | --- | --- |
| 16 | 85.7 µs | 88.6 µs | 124.2 µs | 209.2 µs | **1.03×** |
| 32 | 124.0 µs | 137.2 µs | 184.3 µs | 275.6 µs | **1.11×** |
| 64 | 147.2 µs | 164.4 µs | 374.9 µs | 330.3 µs | **1.12×** |
| 128 | 161.5 µs | 179.9 µs | 302.9 µs | 345.3 µs | **1.11×** |
| 256 | 170.1 µs | 191.5 µs | 310.9 µs | 351.6 µs | **1.13×** |
| 512 | 194.5 µs | 230.1 µs | 331.6 µs | 369.2 µs | **1.18×** |
| 1024 | 281.4 µs | 300.5 µs | 652.7 µs | 438.3 µs | **1.07×** |
| 2048 | 491.8 µs | 522.5 µs | 731.5 µs | 794.4 µs | **1.06×** |
| 4096 | 872.0 µs | 899.2 µs | 1366.0 µs | 1230.7 µs | **1.03×** |
| 8192 | 1695.0 µs | 1712.7 µs | 2216.8 µs | 2362.9 µs | **1.01×** |
| 16384 | 3241.9 µs | 3257.1 µs | 4329.1 µs | 4364.4 µs | **1.00×** |

*表 5：H20 上 TP1 / EP8 时 Hy3 MoE 的延迟。数值越低越好。*

| 批大小 | HPC-Ops | SGLang | vLLM Triton | vLLM CUTLASS | 相对最优加速比 |
| --- | --- | --- | --- | --- | --- |
| 4 | 118.6 µs | 183.1 µs | 147.4 µs | 140.4 µs | **1.18×** |
| 8 | 136.7 µs | 231.5 µs | 192.8 µs | 170.7 µs | **1.25×** |
| 16 | 149.8 µs | 234.2 µs | 198.4 µs | 263.5 µs | **1.32×** |
| 32 | 153.6 µs | 475.3 µs | 214.6 µs | 264.4 µs | **1.40×** |
| 64 | 166.5 µs | 477.3 µs | 358.1 µs | 266.8 µs | **1.60×** |
| 128 | 213.5 µs | 482.3 µs | 251.7 µs | 272.6 µs | **1.18×** |
| 256 | 386.2 µs | 494.3 µs | 454.9 µs | 493.5 µs | **1.18×** |
| 512 | 705.5 µs | 970.7 µs | 691.7 µs | 741.7 µs | 0.98× |
| 1024 | 1342.6 µs | 1476.8 µs | 1369.1 µs | 1359.1 µs | **1.01×** |
| 2048 | 2513.9 µs | 2871.2 µs | 2668.7 µs | 2530.4 µs | **1.01×** |

![H20 Hy3 MoE latency](/images/blog/hpc-ops-sglang/h20-hy3-moe.png)

*图 4：TP8 / EP1 与 TP1 / EP8 两种配置下的 Hy3 MoE 延迟。数值越低越好。*

### H200 算子验证

上游 PR 中还包含 H200 上的推理服务结果，证实这些性能收益可以推广到整个 Hopper GPU 系列。

*表 6：上游 SGLang 拉取请求中报告的算子验证。*

| 算子 | 上游验证负载 | 对比对象 | 结果 |
| --- | --- | --- | --- |
| FP8 Attention | 使用 FP8 KV 缓存的 Hy3-FP8；混合长度解码 | HPC-Ops 动态调度 vs. HPC-Ops 静态 split-KV | 输出吞吐量 **+2.0%**；总吞吐量 **+2.0%**；TTFT 中位数 **−5.3%** |
| BF16 Attention | 使用 BF16 KV 缓存的 Qwen3；混合长度解码 | HPC-Ops 动态调度 vs. HPC-Ops 静态 split-KV | 输出吞吐量 **+3.0%**；平均端到端延迟 **−2.8%**；平均 TPOT **−2.8%** |
| Router GEMM | LongCat-Flash Chat 与 Lite 路由器形状 | HPC-Ops Router GEMM vs. SGLang 默认 | 内核加速：**1.56–4.31×** |
| MoE | 1 至 4,096 token 的 Qwen3 FP8 MoE 负载 | HPC-Ops MoE vs. SGLang Triton 融合专家 | 内核加速：**0.89–4.21×** |

### 端到端性能

端到端评估在 8× NVIDIA H20 GPU 上进行，对比对象为对应的 SGLang 默认实现。在 TP8、FP8 KV 缓存的 Hy3-FP8 上，我们通过同时启用 HPC-Ops Attention 与 MoE 来测量二者叠加的服务影响。在 LongCat-Flash-Lite-FP8 上，则只测量 Router GEMM。我们还汇总了上游 SGLang 拉取请求中报告的 H200 推理服务验证。

**Hy3-FP8：Attention 与 MoE。**

在 8K 输入、4K 输出的设置下，HPC-Ops 在批大小 1 时将 TPOT 降低 **3.3%**。批大小 4–64 时，降幅扩大到 **15.1–48.8%**。

*表 7：FP8 KV 缓存下同时启用 HPC-Ops Attention 与 MoE 时的 Hy3-FP8 TPOT。数值越低越好。*

| 批大小 | SGLang 默认 | HPC-Ops | 提升 |
| --- | --- | --- | --- |
| 1 | 7.56 ms | 7.31 ms | **3.3%** |
| 4 | 11.10 ms | 9.42 ms | **15.1%** |
| 8 | 14.29 ms | 10.76 ms | **24.7%** |
| 16 | 22.90 ms | 13.09 ms | **42.8%** |
| 32 | 35.33 ms | 18.09 ms | **48.8%** |
| 64 | 40.70 ms | 23.81 ms | **41.5%** |

在 8K 输入下，批大小 1–16 时 HPC-Ops 将 TTFT 改善 **3.3–9.0%**。

*表 8：8K 输入、FP8 KV 缓存下的 Hy3-FP8 TTFT。提升为正表示延迟更低。*

| 批大小 | SGLang 默认 | HPC-Ops | 提升 |
| --- | --- | --- | --- |
| 1 | 460.67 ms | 419.43 ms | **9.0%** |
| 4 | 1612.47 ms | 1533.66 ms | **4.9%** |
| 8 | 3210.93 ms | 3018.68 ms | **6.0%** |
| 16 | 5810.53 ms | 5619.48 ms | **3.3%** |

在批大小 16 下，我们还在关闭分块预填充和前缀缓存的情况下，把输入长度从 2K 扫描到 8K。在三个输入长度上，HPC-Ops 将 TTFT 改善 **2.3–8.9%**。

*表 9：批大小 16、FP8 KV 缓存下不同输入长度的 Hy3-FP8 TTFT。提升为正表示延迟更低。*

| 输入长度 | SGLang 默认 | HPC-Ops | 提升 |
| --- | --- | --- | --- |
| 2K | 1509.98 ms | 1375.95 ms | **8.9%** |
| 4K | 2779.46 ms | 2715.18 ms | **2.3%** |
| 8K | 5810.53 ms | 5619.48 ms | **3.3%** |

**LongCat-Flash-Lite-FP8：Router GEMM。**

Router GEMM 单独评估，采用 1,024 token 输入和 128 token 输出。批大小 1 时输入吞吐量基本持平，提升 **0.5%**；批大小 4–64 时提升 **5.5–6.1%**。

*表 10：启用 HPC-Ops Router GEMM 后的 LongCat-Flash-Lite-FP8 输入吞吐量。数值越高越好。*

| 批大小 | SGLang 默认 | HPC-Ops Router GEMM | 提升 |
| --- | --- | --- | --- |
| 1 | 16,612.11 tok/s | 16,695.77 tok/s | **0.5%** |
| 4 | 54,466.27 tok/s | 57,810.27 tok/s | **6.1%** |
| 8 | 60,425.93 tok/s | 63,833.96 tok/s | **5.6%** |
| 16 | 61,995.23 tok/s | 65,539.10 tok/s | **5.7%** |
| 32 | 62,833.85 tok/s | 66,306.52 tok/s | **5.5%** |
| 64 | 62,841.93 tok/s | 66,422.92 tok/s | **5.7%** |

![H20 SGLang end-to-end performance](/images/blog/hpc-ops-sglang/h20-sglang-end-to-end.png)

*图 5：SGLang 端到端结果。三幅 Hy3-FP8 面板均使用 FP8 KV 缓存并同时启用 HPC-Ops Attention 与 MoE；右下面板单独测量 Router GEMM。*

### H200 推理服务验证

上游拉取请求还在 H200 的 SGLang 推理服务主循环中评估了这些集成算子，在以 H20 为主要调优目标之外提供了模型层面的集成验证。

*表 11：上游 SGLang 拉取请求中报告的模型层面服务验证。*

| 算子 | 上游验证负载 | 对比对象 | 结果 |
| --- | --- | --- | --- |
| Attention | 使用 FP8 KV 缓存的 Hy3-FP8 推理服务负载 | HPC-Ops Attention vs. FlashAttention | 输出吞吐量：**+3.7–5.9%** |
| Router GEMM | LongCat-Flash Lite 预填充服务负载 | HPC-Ops Router GEMM vs. SGLang 默认 | 输入吞吐量：**+2.8–5.4%** |
| MoE | Qwen3 与 Hy3 的 FP8 MoE 服务负载 | HPC-Ops MoE vs. SGLang 默认 | 输出吞吐量：Qwen3 从持平到 **+2.7%**；Hy3 为 **−4.2% 到 +6.3%** |

上游集成还通过了数值与模型层面的保真度检查。Attention 测试在 BF16 和 FP8 下均通过，且所评估的 Hy3 FP8 贪心解码输出与 BF16 路径逐 token 一致。Router GEMM 通过了与 FP32 参考实现的对比，并保持贪心解码输出不变。对于 Qwen3，HPC-Ops MoE 路径相对 FP32 的误差与 Triton 相当，余弦相似度为 **0.99974**，最大相对误差为 **0.024**。完整配置和逐场景结果可在上游 PR 中查阅。

## 下一步计划

这项工作是 HPC-Ops 与 SGLang 社区更广泛合作的一部分。我们将继续与 SGLang 的维护者和贡献者合作，改进并扩展这些算子，并在其他 HPC-Ops 能力成熟后陆续贡献上游。我们非常欢迎反馈、Issue 和基准测试结果，期待与大家共同推进开放、高性能的大模型推理。

## 致谢

我们感谢各团队中共同把这些算子带入 SGLang 的众多同事：

- **Tencent Hunyuan AI Infra** —— 构建并优化 HPC-Ops 的 Attention、Router GEMM 和 MoE 算子，并将其贡献给 SGLang。Sethran Liu、Chase Shao、Shengy Wei、Theo Cheng、Ryann Xue、Lando Jiang、Looper Zhao、Haank Lin、Aiden Ren、Lehua Ding、Chengv Jiang、Steven Kuang、Liqi He、Kipper Gong、Reedlau Liu、Raccoon Liu、Dick Zhu。
- **Tencent Network Platform Department** —— 在通信优化方面的紧密协作。Xuan Zhang、Haoran Zhao、Yuanyuan Gong、Yadong Liu、Jinzhu Wang、Yinben Xia、Xiang Li、Quan Wen、Zekun He。
- **SGLang** —— 提供开放的后端接口、代码评审与设计讨论。Xiaoyu Zhang（BBuf）、Xinyuan Tong、Ke Bao 以及整个 SGLang 团队。
- **NVIDIA** —— 在内核与性能优化方面的紧密协作。Yuanhang Sun、Perkz Zheng、Yuxi Chi、Jiang Shao、Jun Gu、Meng Wang、River Liu、Gary Ji、Chandler Zhou。

我们还要感谢更广泛的开源内核社区——本文的工作建立在其成果之上，也以其为衡量基准，包括 NVIDIA CUTLASS/CuTe、TensorRT-LLM、FlashInfer、FlashAttention 和 Triton。
