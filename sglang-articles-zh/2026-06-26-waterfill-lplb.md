---
title: "在 SGLang 中使用 Waterfill 与 LPLB 改进 DeepEP MoE 负载均衡"
title_en: "Improving DeepEP MoE Load Balance in SGLang with Waterfill and LPLB"
author: "NVIDIA Team"
date: "June 26, 2026"
previewImg: /images/blog/waterfill_lplb/waterfill_timeline_nature_redraw.png
source: https://lmsys.org/blog/2026-06-26-waterfill-lplb/
translated: 2026-09-12
---

# 在 SGLang 中使用 Waterfill 与 LPLB 改进 DeepEP MoE 负载均衡

> 原文：[Improving DeepEP MoE Load Balance in SGLang with Waterfill and LPLB](https://lmsys.org/blog/2026-06-26-waterfill-lplb/) · LMSYS Blog · NVIDIA Team

## TL;DR

专家混合（MoE）模型依赖专家并行（EP）将推理扩展到多块 GPU 上。在 SGLang 中，DeepEP 和 EPLB 在 EP 模式下提供了高性能的推理服务，但由于 token 在各专家之间的路由并不均匀，每个 rank 所承担的负载仍可能不均衡。

本文介绍 SGLang 中的两个分发时负载均衡特性：

- **Waterfill**：一种面向 DeepEP 的轻量级共享专家负载均衡方法。它通过 DeepEP 分发共享专家，并将其分配给负载较低的 rank。在两个 Hopper GPU 节点上运行 DeepSeek-V3/R1 风格的服务负载时，Waterfill 在 MMLU、GPQA 和 GSM8K 上将总吞吐量提升了 **+1.48% 至 +4.66%**。在 DeepSeek V4 上，最佳实测点从 **49,253 tok/s** 提升到 **51,677 tok/s**（**+4.92%**）。
- **LPLB**：一种基于线性规划的负载均衡器，面向冗余专家副本。它对冗余专家求解逐层的分发优化问题。在同样的两个 Hopper GPU 节点上配合带冗余的 EPLB 布局，LPLB 在 MMLU、GPQA 和 GSM8K 上将总吞吐量提升了 **+0.84% 至 +7.34%**。

Waterfill 工作建立在两个 SGLang PR 之上：[EP 下的共享专家融合](https://github.com/sgl-project/sglang/pull/20089)和 [Waterfill 分发均衡](https://github.com/sgl-project/sglang/pull/19290)。DeepSeek V4 支持由 [#25391](https://github.com/sgl-project/sglang/pull/25391) 添加。LPLB 则在 [#24515](https://github.com/sgl-project/sglang/pull/24515) 中引入。

## 引言

DeepSeek-V3/R1、DeepSeek V4 等大型 MoE 模型通过稀疏专家激活来扩大模型容量，同时把每个 token 的计算量控制在可管理范围内。在推理时，EP 将专家分布到各块 GPU 上，并把 token 路由到拥有被选中专家的 rank。这降低了单 GPU 的内存压力，使大规模推理服务切实可行，但也引入了一个核心系统问题：**路由器产生的专家流量并不是完美均衡的**。

当某些专家收到的 token 远多于其他专家时，整个 EP 组都要等待最繁忙的 rank。这种不均衡同时影响计算和通信。EPLB 等静态放置方法可以改善专家和冗余副本的长期放置，但单个 batch 内仍可能存在残留的不均衡。分发时负载均衡通过在运行时决定由哪个物理副本处理每个 token 或每个共享专家请求，来弥合这一剩余差距。

在 SGLang 中，我们一直在为 DeepEP MoE 推理开发两种分发时方案：

- **Waterfill**：一种低开销算法，聚焦于共享专家路径。
- **LPLB**：一种基于线性规划（LP）的算法，聚焦于跨冗余专家副本的 token 路由。

这两种算法瞄准的是系统中同一个层面：分发时的 MoE 负载均衡。它们做出不同的权衡，作用于不同的分发选择。

## 背景：DeepEP MoE 推理中的负载不均衡

DeepEP 为专家并行提供了经过优化的 token 分发（dispatch）与合并（combine）算子，从而加速 MoE 推理。在一个典型的 DeepSeek 风格 MoE 层中，每个 token 会被路由到模型路由器选出的若干**路由专家**（routed experts）上。一些模型还包含**共享专家**（shared expert），它对每个 token 都生效。

从推理服务系统的视角看，路由专家和共享专家会造成不同的负载模式：

- 路由专家是稀疏的。不同 token 选择不同专家，因此其负载取决于路由器分布。
- 共享专家是稠密的。每个 token 都需要共享专家，因此共享专家负载贯穿整个 batch。
- 冗余专家由 EPLB 式的放置引入，为部分逻辑专家提供多个物理副本。它们为分发时均衡创造了机会，因为系统可以在不改变模型逻辑专家选择的前提下，选择由哪个物理副本来处理一个 token。

静态专家放置有帮助，但无法消除所有运行时不均衡。一个 batch 中的实际 token 仍可能集中在部分专家或 rank 上。在 DeepEP 中，这会导致一些 rank 一直等待过载的同伴。Waterfill 和 LPLB 都旨在减少这种分发时的不均衡，同时保持模型语义不变。

## Waterfill：面向共享专家分发的轻量级负载均衡

### Waterfill 分发策略

Waterfill 是一种面向 DeepEP 下共享专家路径的轻量级负载均衡算法。

如果共享专家总是由每个 rank 在本地计算，那么无论该 rank 是否已被路由专家压得过载，它都要支付共享专家的计算成本。过载的 rank 依旧过载，而负载较轻的 rank 也无法帮忙分担共享专家的工作。

Waterfill 改变了这一点：它把共享专家当作一个可分发的专家槽位。在路由专家选定之后，Waterfill 估计每个 EP rank 当前的路由负载，然后把共享专家工作分配给负载较低的 rank。从概念上讲，它填平了 rank 负载分布中的低谷，就像往高低不平的容器里注水一样。

对每个 token，Waterfill 为共享专家额外增加一个专家槽位。这个槽位并非总是分配给 token 所在的本地 rank，而是根据当前负载分布来选择一个 rank。路由专家的选择保持不变，因此模型仍会计算相同的逻辑路由专家和相同的共享专家。唯一改变的是**由哪个物理 rank 执行共享专家的工作**。

从高层来看，该算法如下：

1. 统计已经落在每个 EP rank 上的路由专家负载。
2. 将该统计值作为每个 rank 的负载分数。在动态模式下，SGLang 先执行一次 EP 组内的集合通信，使该分数能够使用全局路由负载向量加上每个 rank 当前的本地 batch 大小。
3. 为每个参与的 token 增加一个共享专家槽位，并计算目标水位线：

   $$
   H = \left\lceil\frac{\sum_r L_r + N}{R}\right\rceil\notag
   $$
   其中 $L_r$ 是 rank $r$ 的负载分数，$N$ 是待放置的共享专家槽位数量，$R$ 是 EP 组大小。
4. 低于该水位线的 rank 存在松弛量：

   $$
   S_r = \max(H - L_r, 0)\notag
   $$
   
5. 对每个 token，Waterfill 按照与松弛量成正比的概率从候选 rank 中采样共享专家的目标 rank，并带有一点本地 rank 偏好。如果所有候选的松弛量都为零，则回退到明显更轻的候选 rank，同样保留本地 rank 偏好。

详细推导以及 SGLang 中静态/动态模式的确切行为，见 [Waterfill 分发均衡 PR](https://github.com/sgl-project/sglang/pull/19290)。

这里有一个重要的通信权衡。如果每个 token 都可以把共享专家工作发给任意 EP rank，Waterfill 会拥有更大的均衡自由度，但也可能增加 all-to-all 流量。对 GPU MoE 推理服务而言，通信开销往往高于共享专家的额外计算开销。因此，通信保守的候选集合让共享专家留在该 token 为路由专家本来就要访问的那些 rank 上，并把源 rank 作为兜底。SGLang 还支持 all-rank 模式，它给 Waterfill 更大的均衡自由度，但可能为每个 token 新增一个分发目的地。这是一种有意的通信权衡，而不是模型语义的改变。

通过把共享专家工作从已经很重的 rank 转移到较轻的 rank，Waterfill 均衡了各 rank 的工作量，提升了端到端吞吐量。

![Waterfill timeline before and after shared-expert balancing](/images/blog/waterfill_lplb/waterfill_timeline_nature_redraw.png)

图 1. Waterfill 在保持路由专家选择不变的前提下，把共享专家工作从过载的 rank 转移到较轻的 rank，从而在不改变模型语义的情况下缩短 MoE 层最慢的那条路径。

### 共享专家融合作为使能机制

通过将共享专家与路由专家融合，Waterfill 还能进一步加速。

在 EP 下，共享专家原本与路由专家使用相互独立的执行路径。在 Waterfill 选出非本地的共享专家 rank 之后，原有设计需要从分发后的路由专家布局中抽取共享专家 token，并单独发起一次共享专家计算，带来额外的布局转换和启动开销。

共享专家融合避免了这条路径：它把共享专家表示为同一个 DeepEP MoE 布局中的另一个专家槽位。在 DeepSeek V3/R1 中，路由器仍按原样选出 top-k 路由专家，TopK 输出只为共享专家增加一列。在 DeepEP 的物理专家 ID 布局中，每个 rank 在其路由专家旁边预留一个额外的共享专家槽位。这样，路由专家和共享专家就能共用同一套 DeepEP 分发、grouped-GEMM 与合并流程。

这正是 Waterfill 特性被拆成两部分的原因：

- [#20089](https://github.com/sgl-project/sglang/pull/20089) 将共享专家以固定的本地分配方式融合进 DeepEP MoE 路径。
- [#19290](https://github.com/sgl-project/sglang/pull/19290) 添加了 Waterfill，用负载感知的共享专家分发取代固定分配。

融合本身并不是最终的负载均衡算法，它是必要的机制：正是它让共享专家的分发对 DeepEP 可见，从而能够被 Waterfill 控制。

## LPLB：面向冗余专家副本的基于线性规划的负载均衡

### LPLB 解决的问题

EPLB 为热门逻辑专家放置冗余副本，然后默认把每个热门专家的 token **均匀**拆分到其物理副本上。只有当构建放置方案所用的离线分布与实际线上流量一致时，均匀拆分才是最优的。实践中往往并非如此：单个 batch 集中在与校准集不同的专家上，服务中的数据集会偏离录制时的数据集，而再均衡周期又足够长，以至于放置方案在许多 batch 期间实际上是静态的。当这种情况发生时，即便把热门专家的负载均匀分给它的副本，持有这些副本的 rank 相对 EP 组的其余部分仍会负载不均，整个组都要等待最繁忙的 rank。

LPLB 在分发时弥补这一差距。对每个 MoE 层、每个 batch，它查看*实际的*每个专家 token 数量，并决定如何把每个被复制专家的 token 在其物理副本之间拆分，使**每个 rank 的最大负载最小化**。它不移动权重，也不改变路由器的逻辑 top-k 选择——它只是在某个逻辑专家的有效物理副本之间决定每个副本接收多少流量。结果是针对当前 batch 的 min–max 最优分配，而不是 EPLB 离线固化的静态均匀拆分。

### 线性规划建模

LPLB 把这个问题转化为一个逐层求解的小型线性规划。直觉可以直接映射到约束上：

- **目标——最小化峰值。** 引入一个标量 `M` 表示所有 rank 上的最大负载，并将其最小化。压低 `M` 会把最繁忙的 rank 拉向平均值，而这正是缩短 EP 不均衡造成的 grouped-GEMM 长尾的关键。
- **rank 负载约束。** 对每个 rank：*（来自其冗余专家副本的负载）+（来自其单副本专家的负载）+（到峰值的松弛量）= M*。每个 rank 上的单副本负载是固定的输入——那些专家没有分发选择。每个 rank 对应一条这样的等式；松弛量非负，因此 `M` 被迫至少等于每个 rank 的真实负载。
- **冗余专家守恒。** 对每个被复制的逻辑专家，分配给其各副本的负载之和必须等于该专家观测到的总负载：$x_1 + x_2 + ... + x_n = L$，其中 $x_i$ 是放在副本 $i$ 上的负载，$L$ 是该专家观测到的总负载。这保证 LPLB 只对现有流量做再分配，绝不会凭空产生或丢弃 token。

决策变量是被复制专家的逐副本负载，再加上各 rank 的松弛量和 `M`。单副本专家不是变量——它们只贡献固定项——这使线性规划保持很小：其规模只随*冗余*专家数量和 rank 数量增长，而与全部专家数量无关。

约束矩阵被拆分为离线部分和在线部分。结构性块——副本到逻辑专家的映射、被复制副本的逐 rank 归属，以及松弛/`−M` 列——只取决于专家到 GPU 的放置，因此**在启动时以及每次 EPLB 再均衡后预先计算一次**。逐 batch 变化的只有右端项：观测到的冗余专家负载和各 rank 的单副本负载。一个 Big-M 辅助列在求解过程中保持系统可行，并在目标函数中受到重罚，使求解器把它压到零。

### 从全局计数到求解完成的线性规划

DP 注意力的一个微妙之处在于：同一步中不同 EP rank 可能运行不同的前向模式——预填充（prefill）、解码（decode）或空闲——因此没有任何单个 rank 能看到全局的 token 分布。LPLB 用一个刻意简洁的集合通信设计来处理这一点：

1. 每个 rank 统计本地每个逻辑专家的 token 数。
2. **所有** EP rank 参与一次对这些计数的 all-reduce——空闲 rank 贡献零——于是每个 rank 最终都得到完全相同的全局逐专家分布。
3. 随后每个 rank 独立地用这些相同的输入求解*同一个*线性规划并得到相同的解，因此**无需广播结果**。

线性规划本身在 GPU 上由一个基于 `cuSOLVERDx`/`cuBLASDx` 构建的融合内点法（IPM）算子求解，启动时即针对该层的矩阵形状完成预编译，因此首个真实请求不必承担 JIT 编译开销。整个逐 batch 路径——构造右端项、求解、抽取逐副本拆分——被压缩成三次 CUDA kernel 启动，写入预分配的缓冲区，让启动开销和主机同步不占用关键路径。

### 从线性规划解到 token 分发

线性规划返回的是：对每个被复制的逻辑专家，其负载*应当*如何在其物理副本间划分。LPLB 将其归一化为该专家在有效物理副本上的概率分布（`log2phy_prob`）。分发时，每个被路由到被复制逻辑专家的 token 都从该分布中采样一个物理副本；单副本专家则像以前一样映射到其唯一的物理位置。这是对现有 `dynamic` 策略的即插即用替代——`dynamic` 策略均匀随机地挑选副本，而 LPLB 保留了同样的按 token 概率分发形态，只是把均匀抽样换成了为当前 batch 计算出的负载最优分布。

![LPLB load-aware split across redundant expert replicas](/images/blog/waterfill_lplb/lplb_redundant_traffic_diagram.png)

图 2. LPLB 在不改变逻辑专家路由的前提下，把被复制专家的流量转移到较轻的 rank，因此在存在冗余副本时，同一个被选中的专家可以在负载较轻的物理副本上完成计算。

### LPLB 与 Waterfill 的区别

Waterfill 和 LPLB 的最终目标一致——在 DeepEP 下抹平各 rank 的负载——但作用于不同的分发选择，采用不同的机制：

| | Waterfill | LPLB |
| --- | --- | --- |
| 目标 | 应用于每个 token 的**共享**（稠密）专家 | 被 EPLB **复制**的**路由**专家 |
| 决策 | 由哪个 rank 执行每个 token 的共享专家槽位 | 如何把每个被复制专家的 token 在其物理副本间拆分 |
| 方法 | 基于当前 rank 负载的轻量级填谷启发式 | 逐层在 GPU 上求解的 min–max 线性规划 |
| 前提条件 | 共享专家融合 | 存在 EPLB 冗余副本 |
| 开销 | 接近零的开销 | 每层一次 all-reduce 加一次线性规划求解 |

二者互补而非竞争：Waterfill 消除稠密共享专家带来的不均衡，LPLB 消除稀疏路由副本之间的不均衡。由于 LPLB 只在同一个逻辑专家的有效副本之间再分配流量、从不改动路由器的逻辑 top-k，它保持模型语义的理由与 Waterfill 相同。

### LPLB 何时收益最大

LPLB 的收益取决于线上 batch 偏离 EPLB 校准分布的程度。当流量非常均衡且 batch 极大（大规模、高度多样化的服务）时，留给线性规划消除的残留不均衡很少。当流量本质上固定且狭窄（少数几个几乎相同的问题）时，静态 EPLB 已经捕获了分布，均匀拆分已接近最优。LPLB 在两者之间发挥最大作用——**中等规模的服务**，聚焦于数量适中的相关主题，此时每个 batch 的不均衡方式是离线放置未曾预料的，但仍足够有结构，使得逐 batch 的最优拆分能切实降低峰值 rank 负载。

## 效果评估

### DeepSeek V3/R1 上的 Waterfill 与 LPLB

我们在同一套 DeepSeek-V3/R1 风格的服务配置上评估了 Waterfill 和 LPLB。下表对应直接集成进 SGLang 的运行 `dsv3_ep16_three_dataset_lplb_matrix_20260605_101821`，使用 SGLang commit `a462e0f864103785fd3e64327104103f1356f220`。

基准测试配置为：

- 模型：DeepSeek-V3 FP8，用作 DeepSeek-V3/R1 风格的服务负载。
- 硬件：两个 Hopper GPU 节点，共 16 块 GPU。
- 并行与后端：TP16、DP16、EP16、DP 注意力、DeepEP normal 模式。
- 数据集：MMLU、GPQA 和 GSM8K 提示池。
- 基准测试形态：`batch_size=1000`、`concurrency=256`、`request_rate=inf`、`max_tokens=1`。

表中每组比较都在相同的放置配置内进行。LPLB 只有在启用 EPLB 放置时才有意义，因为它是在同一个逻辑专家的有效物理副本之间进行路由的。

| 数据集 | 基线配置 | 基线 | Waterfill | Waterfill 提升 | LPLB | LPLB 提升 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| MMLU | 无 EPLB | 28,968 tok/s | 29,697 tok/s | +2.52% | - | - |
| MMLU | 静态 EPLB，red0 | 30,392 tok/s | 31,424 tok/s | +3.40% | 29,938 tok/s | -1.50% |
| MMLU | 静态 EPLB，red16 | 30,638 tok/s | 31,483 tok/s | +2.76% | 31,104 tok/s | +1.52% |
| MMLU | 静态 EPLB，red32 | 30,714 tok/s | 31,169 tok/s | +1.48% | 31,547 tok/s | +2.72% |
| GPQA | 无 EPLB | 23,201 tok/s | 24,283 tok/s | +4.66% | - | - |
| GPQA | 静态 EPLB，red0 | 26,322 tok/s | 26,970 tok/s | +2.46% | 25,899 tok/s | -1.61% |
| GPQA | 静态 EPLB，red16 | 26,124 tok/s | 26,683 tok/s | +2.14% | 26,350 tok/s | +0.86% |
| GPQA | 静态 EPLB，red32 | 25,975 tok/s | 26,655 tok/s | +2.62% | 26,193 tok/s | +0.84% |
| GSM8K | 无 EPLB | 29,649 tok/s | 30,892 tok/s | +4.19% | - | - |
| GSM8K | 静态 EPLB，red0 | 33,058 tok/s | 34,529 tok/s | +4.45% | 32,744 tok/s | -0.95% |
| GSM8K | 静态 EPLB，red16 | 34,026 tok/s | 35,226 tok/s | +3.53% | 35,474 tok/s | +4.26% |
| GSM8K | 静态 EPLB，red32 | 33,988 tok/s | 35,070 tok/s | +3.19% | 36,482 tok/s | +7.34% |

![Waterfill throughput on DeepSeek V3/R1-style workloads](/images/blog/waterfill_lplb/fig1_baseline_vs_waterfill.png)

图 3. 在 MMLU、GPQA 和 GSM8K 上，Waterfill 通过把共享专家工作转移到负载较轻的 EP rank，一致地使总吞吐量高于对应的基线。

![LPLB throughput on DeepSeek V3/R1-style workloads](/images/blog/waterfill_lplb/fig2_baseline_vs_lplb.png)

图 4. 当存在冗余专家副本（`red16`/`red32`）时，LPLB 能提升吞吐量，因为线性规划有物理副本可供选择。在 `red0` 下没有可供再均衡的冗余副本，算法无法改进分发，其 all-reduce/求解路径便只表现为开销。

这些结果表明，Waterfill 在保持模型质量的同时提升了吞吐量，因为它只改变共享专家的物理放置，不改变逻辑专家计算。当冗余专家副本提供了有用的分发选择时，LPLB 表现最佳，如 red16 和 red32 行所示。相反，在没有提供冗余专家时，LPLB 没有均衡负载的空间，因此只体现出算法开销。

### DeepSeek V4 上的 Waterfill

DeepSeek V4 可以使用 `HashTopK` 路由路径，此时 Waterfill 也需要在 `HashTopK` 输出路径中追加并重映射共享专家槽位。[#25391](https://github.com/sgl-project/sglang/pull/25391) 将 Waterfill 扩展到了该路径。共享专家均衡这一思路本身并不特定于 `HashTopK`，它同样适用于非 `HashTopK` 的路由路径。

在两个 Hopper GPU 节点上，DeepSeek V4 Flash FP8 在 MMLU 风格的服务负载上表现出一致的吞吐量提升。这次 V4 Flash 运行使用 14,042 条提示的 MMLU 池，batch=512、concurrency=128、`max_tokens=1`，2 轮预热，4 轮正式测量。表中报告的是截尾均值总吞吐量。由于这次 V4 Flash 运行使用了更小的 batch/并发形态，这些数字应被视为针对 V4 的验证，而不是与上文 DeepSeek-V3/R1 风格矩阵的直接吞吐量对比。

| 配置 | 基线 | Waterfill | 提升 |
| --- | ---: | ---: | ---: |
| 无 EPLB | 45,951 tok/s | 47,876 tok/s | +4.19% |
| 静态 EPLB，red0 | 49,253 tok/s | 51,677 tok/s | +4.92% |
| 静态 EPLB，red16 | 50,006 tok/s | 51,655 tok/s | +3.30% |
| 静态 EPLB，red32 | 50,167 tok/s | 51,813 tok/s | +3.28% |

![Waterfill throughput on DeepSeek V4 Flash](/images/blog/waterfill_lplb/fig3_v4_waterfill.png)

图 5. Waterfill 在 DeepSeek V4 Flash 上同样有效，在无 EPLB 和静态 EPLB 设置下都提升了吞吐量，增益为 +3.28% 至 +4.92%。

这些结果验证了，除上文 DeepSeek-V3/R1 风格负载外，Waterfill 在 DeepSeek V4 Flash 上依然保持正向收益。

### 精度验证

Waterfill 保持模型语义，因为它不改变路由器的逻辑 top-k 决策。模型选出的路由专家保持不变，共享专家也仍是同一个共享专家。Waterfill 只改变由哪个物理 EP rank 执行共享专家槽位。

出于同样的结构性原因，LPLB 也保持模型语义。它从不改动路由器的逻辑 top-k，只是选择由被选中逻辑专家的哪个物理副本来处理每个 token。由于同一逻辑专家的所有副本持有完全相同的权重，token 得到的结果与由哪个副本处理无关。这与 EPLB 和 `dynamic` 策略已经依赖的精度保证是同一个。

## 使用方法

### 启用 Waterfill

Waterfill 通过 DeepEP MoE 路径启用。一个有代表性的启动命令如下：

```bash
python3 -m sglang.launch_server \
    --model-path /path/to/DeepSeek-V3 \
    --tp 16 \
    --dp-size 16 \
    --nnodes 2 \
    --node-rank ${NODE_RANK} \
    --dist-init-addr ${HEAD_NODE_IP}:${PORT} \
    --host 0.0.0.0 \
    --port 30000 \
    --trust-remote-code \
    --moe-a2a-backend deepep \
    --deepep-mode normal \
    --enable-dp-attention \
    --enable-deepep-waterfill \
    --init-expert-location /path/to/expert_distribution.pt
```

关键的 flag 有：

- `--moe-a2a-backend deepep`：使用 DeepEP 进行 MoE all-to-all 分发。
- `--enable-deepep-waterfill`：启用共享专家融合与 Waterfill 路径。
- `--init-expert-location`：可选地根据采集到的专家分布统计信息初始化专家放置和 rank 负载元数据。

DeepSeek V4 支持使用 [#25391](https://github.com/sgl-project/sglang/pull/25391) 中添加的 `HashTopK` 路径。

### 启用 LPLB

LPLB 通过 DeepEP MoE 路径上的 EP 分发算法选择。由于 LPLB 是在冗余副本之间均衡 token 的，它要求 EPLB 放置中确实包含冗余专家。一个有代表性的两节点启动命令如下：

```bash
python3 -m sglang.launch_server \
    --model-path /path/to/DeepSeek-R1 \
    --tp 16 \
    --dp-size 16 \
    --ep-size 16 \
    --nnodes 2 \
    --node-rank ${NODE_RANK} \
    --dist-init-addr ${HEAD_NODE_IP}:${PORT} \
    --host 0.0.0.0 \
    --port 30000 \
    --trust-remote-code \
    --moe-a2a-backend deepep \
    --deepep-mode normal \
    --enable-dp-attention \
    --ep-num-redundant-experts 16 \
    --ep-dispatch-algorithm lp \
    --init-expert-location /path/to/expert_stats.pt
```

关键的 flag 有：

- `--ep-dispatch-algorithm lp`：选择 LPLB 线性规划分发器，取代默认的 `static` 或均匀随机的 `dynamic` 策略。
- `--ep-num-redundant-experts`：为热门逻辑专家创建冗余物理副本。没有它们，LPLB 就没有可均衡的对象——这正是上文 `red0` 行看不到 LPLB 增益的原因。
- `--init-expert-location`：加载从专家分布记录运行中收集的静态 EPLB 放置（物理到逻辑的映射，包括冗余槽位）。这里的副本数量必须与 `--ep-num-redundant-experts` 一致。

## 致谢

本工作构建于 SGLang 的 DeepEP 与 MoE 推理服务栈之上，并通过 SGLang 项目中的社区协作完成开发。

感谢 SGLang 的维护者和审阅者在相关 PR 中提供的讨论、评审和集成支持：

- [#20089：EP 下将共享专家融合进 MoE 分发](https://github.com/sgl-project/sglang/pull/20089)
- [#19290：为共享专家分发添加 Waterfill 负载均衡](https://github.com/sgl-project/sglang/pull/19290)
- [#25391：支持 DeepSeek V4 DeepEP Waterfill](https://github.com/sgl-project/sglang/pull/25391)
- [#24515：LPLB：面向 MoE 专家并行的线性规划负载均衡器](https://github.com/sgl-project/sglang/pull/24515)

我们衷心感谢为本工作做出贡献的人员：

- NVIDIA 团队：Xuting Zhou、Fei Liang 和 Aichen Feng
- SGLang 团队：Cheng Wan

同时感谢 DeepSeek 在 [deepseek-ai/LPLB](https://github.com/deepseek-ai/LPLB) 开源其 LPLB 工作，其用于在冗余专家副本间均衡 token 的线性规划建模启发了本文所述的 SGLang LPLB 集成。
