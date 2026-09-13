---
title: "在 96 块 H100 GPU 上以 PD 分离与大规模专家并行部署 DeepSeek"
title_en: "Deploying DeepSeek with PD Disaggregation and Large-Scale Expert Parallelism on 96 H100 GPUs"
author: "The SGLang Team"
date: "May 5, 2025"
previewImg: /images/blog/large_scale_ep/cover.jpg
source: https://lmsys.org/blog/2025-05-05-large-scale-ep/
translated: 2026-09-12
---

# 在 96 块 H100 GPU 上以 PD 分离与大规模专家并行部署 DeepSeek

> 原文：[Deploying DeepSeek with PD Disaggregation and Large-Scale Expert Parallelism on 96 H100 GPUs](https://lmsys.org/blog/2025-05-05-large-scale-ep/) · LMSYS Blog · The SGLang Team

DeepSeek 是一款广受欢迎的开源大语言模型（LLM），以强劲的性能著称。然而，它庞大的模型规模和独特的架构——采用多头潜在注意力（MLA）与专家混合（MoE）——需要一个先进的系统才能实现大规模高效推理服务。在本博客中，我们将介绍如何用 SGLang 达到 DeepSeek 推理系统的性能水平。

<img src="/images/blog/large_scale_ep/overall-arch.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 90%; image-orientation: none;"></img>

我们的实现如图所示，运行在 Atlas Cloud 的 12 个节点上，每个节点配备 8 块 H100 GPU。它采用预填充-解码分离（PD 分离）与大规模专家并行（EP），在 2000 token 输入序列下达到**每节点 52.3k 输入 token/秒和 22.3k 输出 token/秒**的速度。据我们所知，这是首个在大规模场景下接近官方 DeepSeek 博客所报告吞吐量的开源实现。在本地部署该实现时，成本折合为 $0.20/百万输出 token，约为官方 DeepSeek Chat API 价格的五分之一。与使用相同资源的普通张量并行相比，这一优化策略可将输出吞吐量提升至多 5 倍。本博客将深入介绍我们的并行设计、优化方法与实验结果。我们工作的所有组件均已完全开源，欢迎大家在我们的成果之上继续探索与构建。复现实验的完整说明见[此处](https://github.com/sgl-project/sglang/issues/6017)。


## 亮点

✅ SGLang 现已支持预填充-解码（PD）分离与大规模专家并行（EP），包括 [DeepEP](https://github.com/deepseek-ai/DeepEP)、[DeepGEMM](https://github.com/deepseek-ai/DeepGEMM) 和 [EPLB](https://github.com/deepseek-ai/eplb) 的完整功能。

✅ 借助这些新特性，我们团队成功使用 12 个节点（每个节点 8 块 H100 GPU）复现了 DeepSeek 的推理系统。总体而言，在 2000 token 输入序列下，SGLang 达到每节点 52.3k 输入 token/秒和 22.3k 输出 token/秒的吞吐量。

✅ 本博客介绍了我们方法的技术细节，重点关注效率优化、峰值内存占用降低与负载均衡。性能剖析（profile）结果显示，我们的实现与官方 DeepSeek 报告的性能几乎持平。

✅ 所有实验和代码均已完全开源，供社区使用与进一步开发。


## 目录

- [并行设计](#parallelism-design)
- [预填充与解码分离](#prefill-and-decode-disaggregation)
- [大规模专家并行](#large-scale-expert-parallelism)
- [评估](#evaluation)
- [工具集](#toolkits)
- [局限与未来工作](#limitations-and-future-work)
- [结论](#conclusion)
- [致谢](#acknowledgment)


## 并行设计

高效的并行策略对于应对 DeepSeek 架构的计算复杂度和内存需求至关重要。本节概述我们优化关键组件的方法：注意力层、稠密前馈网络（FFN）、稀疏 FFN 以及语言模型（LM）头。每个组件都采用量身定制的并行策略，以提升可扩展性、内存效率和性能。

### 注意力层

DeepSeek 采用**多头潜在注意力（MLA）**来有效建模输入序列中的复杂依赖关系。为优化该机制，我们实现了 **DP 注意力（DP Attention）**——一种数据并行策略，消除了 KV 缓存在设备间的重复存储，显著降低内存开销。该方法在 [SGLang v0.4](https://lmsys.org/blog/2024-12-04-sglang-v0-4/#data-parallelism-attention-for-deepseek-models) 中首次引入，如今已扩展为支持**数据并行与张量并行的混合模式**，为高效处理小批量（batch size）提供了灵活性。

### 稠密 FFN

尽管 DeepSeek-V3 只有三个稠密 FFN 层，其计算仍会显著推高峰值内存占用，若不加妥善管理甚至可能导致系统崩溃。为此，我们选择**数据并行（DP）**而非张量并行（TP），利用了以下优势：

- **可扩展性更强**：在中间维度为 18,432 的情况下，高 TP 度（如 TP32）会导致低效的碎片化切分——切成小单元段（如 576 个单元），而 576 无法被 128 整除，128 是 H100 等现代 GPU 常见的对齐边界。这种不对齐会损害计算效率和内存利用率。DP 避免了碎片化，确保负载在设备间均衡分布，提供了更具可扩展性的方案。
- **内存效率更优**：传统上，TP 随 worker 数量增加而降低内存用量，但在 DP 注意力下这一优势被削弱。在纯 TP 配置下，单层 Transformer 模型的内存需求随 DP 大小变化如下：$$\text{Memory}=\frac{N_{\text{param}}}{\text{TP}}+(1+k)N_{\text{hidden\_state}}\cdot \text{DP}\notag$$ 其中，$N_{\text{hidden\_state}}=n_\text{token}\times n_\text{hidden\_size}$ 是每个设备（DP rank）上的隐藏状态大小，$N_{\text{param}}=n_\text{intermediate\_size}\times n_\text{hidden\_size}$ 是模型参数量，$k$ 是表示 CUDA 图复制带来的额外内存开销的系数。假设 $\text{DP}=\text{TP}$，该内存占用函数在 $\text{TP}=\sqrt{\frac{N_{\text{param}}}{(1+k)N_{\text{hidden\_state}}}}$ 时取最小值。DeepSeek-V3 的中间维度为 18,432。在预填充阶段，CUDA 图通常被禁用，因此 $k = 0$；此时每设备的 token 数很容易超过 2,048，最优 TP 大小为 3 或更小。在解码阶段，一个实际配置可能是每设备 128 个 token 并设 $k = 3$，此时内存最优的 TP 大小为 6。在两个阶段中，更低的 TP 度都能最小化每设备的内存占用。因此，与单纯依赖 TP 相比，DP 可能是扩展时更省内存的方案。
- **通信开销更小**：在纯 TP 下，每个 FFN 需要两次 all-reduce 操作，带来可观的通信开销。利用 DP，我们将这一过程优化为：在前一层注意力之后做一次 reduce-scatter、在下一层之前做一次 all-gather，通信成本降低 50%。此外，当注意力也在纯 DP 下计算时，设备间通信可完全消除，整体效率显著提升。

DP 稠密 FFN 与 DP 注意力的集成如下图左侧所示。用户可通过设置 `--moe-dense-tp-size=1` 启用该特性。



<img src="/images/blog/large_scale_ep/parallel-design.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 95%; image-orientation: none;"></img>



### 稀疏 FFN

在 DeepSeek-V3 的专家混合（MoE）架构中，稀疏 FFN 需要占用大量专家权重，构成显著的内存瓶颈。为此，我们实现了**专家并行（EP）**，将专家权重分布到多个设备上。这一方案在保持高性能的同时有效扩展了内存容量，但也带来了诸如不规则的 all-to-all 通信和负载不均等挑战。

上图右侧的图展示了我们基于 DeepEP 框架的 EP 实现，EP 设计与优化的更多细节见[后续章节](#large-scale-expert-parallelism)。



### LM 头

LM 头需要在大词表上计算输出概率，这一操作资源消耗大，传统上用词表并行从各个 TP 组聚合 token logit。为提升可扩展性与效率，我们采用**数据并行（DP）**，与稠密 FFN 的策略保持一致。这降低了内存开销、简化了设备间通信，提供了更精简的方案。


## 预填充与解码分离

LLM 推理包含两个截然不同的阶段：**预填充（prefill）**与**解码（decode）**。预填充阶段计算密集，需要处理整个输入序列；解码阶段则内存密集，需要管理用于 token 生成的键值（KV）缓存。传统做法是在统一引擎中处理这两个阶段，但预填充批与解码批混合调度会引入低效。为解决这些问题，我们在 SGLang 中引入了**预填充与解码分离（PD 分离，PD Disaggregation）**。

### 统一调度的问题

将预填充批与解码批放在一起处理的传统统一引擎存在三个显著问题：

1. **预填充打断解码**：新到来的预填充批频繁打断正在进行的解码批，导致 token 生成出现明显延迟。
2. **DP 注意力不均衡**：在 DP 注意力下，一个 DP worker 可能在处理预填充批，而另一个同时处理解码批，导致解码延迟增加。
3. **与 DeepEP 不兼容**：正如[后文](#expert-parallelism-with-deepep)将讨论的，DeepEP 对预填充和解码使用不同的分发（dispatch）模式，这使得统一调度与 DeepEP 不兼容。

PD 分离通过将两个阶段拆开来解决这些问题，从而可以对每个阶段进行针对性的优化。

### 实现细节

下图描绘了 SGLang 的 PD 分离设计：在预填充服务器（Prefill Server）与解码服务器（Decode Server）之间交错执行：



<img src="/images/blog/large_scale_ep/pd-disaggregation.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 60%"></img>



收到输入请求后，工作流程如下：

1. 预填充服务器与解码服务器通过握手配对，分别建立本地的发送端与接收端。
2. 解码服务器预先分配 KV 缓存，并通知预填充服务器开始模型前向计算，生成 KV 缓存。
3. 计算完成后，数据传输至解码服务器，由后者负责迭代式 token 生成。

这一分离确保每个阶段都在最优条件下运行，最大化 GPU 资源利用率。为进一步提升性能，我们的实现还包含：

- **非阻塞传输**：数据收发操作在后台线程中运行，保证调度器的事件循环不被打断。
- **基于 RDMA 的传输**：远程直接内存访问（RDMA）利用队列对（queue pair）建立连接，并借助散布-聚集元素（SGE）高效传输非连续内存块。
- **灵活的 API 集成**：SGLang 提供可灵活适配的 API，可集成 Mooncake、NIXL 等高性能 RDMA 库，简化数据传输。

更多细节见我们的[设计文档](https://docs.google.com/document/d/1rQXJwKd5b9b1aOzLh98mnyMhBMhlxXA5ATZTHoQrwvc/edit?tab=t.0)。


## 大规模专家并行

### 基于 DeepEP 的专家并行

[DeepEP](https://github.com/deepseek-ai/DeepEP) 由 DeepSeek 团队开发，是一个旨在简化 MoE 模型中 EP 的通信库。它解决的是如何跨多块 GPU 高效地将 token 路由到特定专家的难题。DeepEP 提供经过优化的通信内核（kernel），降低延迟、提升吞吐量，非常适合大规模推理任务。

DeepEP 提供两种专门化的分发模式以应对不同的负载需求：

- **普通分发（Normal Dispatch）**：针对长输入序列（如预填充阶段）优化，优先追求最大计算吞吐量。但它生成符号化形状（symbolic shapes），与 CUDA 图不兼容，因此在内核启动开销成为主要瓶颈的解码阶段效果较差。
- **低延迟分发（Low-Latency Dispatch）**：为解码阶段生成输出 token 而定制，优先保证最小延迟以实现实时性能。它支持 CUDA 图，但需要预分配固定大小的内存；若内存需求超出预分配量，将发生运行时错误。

在 SGLang 中，集成 DeepEP 后提供了 **auto 模式**，可根据负载在两种分发模式间动态选择。但在没有 PD 分离的情况下，auto 模式存在一个限制：无法在同一个通信组内同时支持普通分发（用于预填充）和低延迟分发（用于解码）。这一限制影响了它与 DP 注意力的兼容性，而 DP 注意力对内存高效的推理至关重要。各模式的兼容性如下表所示：

| **模式**    | **长输入** | **长输出** | **DP 注意力** | **CUDA 图** |
| ----------- | -------------- | --------------- | ---------------- | -------------- |
| Normal      | ✅              | ❌               | ✅                | ❌              |
| Low-Latency | ❌              | ✅               | ✅                | ✅              |
| Auto        | ✅              | ✅               | ❌                | ✅              |

PD 分离通过拆分预填充和解码阶段解决了这一问题：预填充阶段使用普通分发，解码阶段使用低延迟分发，二者都运行在 DP 注意力之下。这种集成使分发模式与各阶段的具体需求相匹配，优化了资源利用并提升了整体性能。



### DeepGEMM 集成

[DeepGEMM](https://github.com/deepseek-ai/DeepGEMM) 是 DeepSeek 团队开发的另一个高性能库，专门用于优化 MoE 模型中的计算。它提供两个专门函数来处理 MoE 相关的矩阵乘法（分组 GEMM，Grouped GEMM），分别针对推理过程的不同阶段。

- **分组 GEMM（连续布局，contiguous layout）：** 该内核面向动态输入形状设计，非常适合 MoE 推理的预填充阶段。它处理的是不同专家的数据连续拼接在一起的输入，可以灵活应对不同的输入大小。
- **分组 GEMM（掩码布局，masked layout）：** 该内核假设输入形状固定，使用掩码张量只计算输入的有效部分。它与 CUDA 图兼容，可优化内核启动，非常适合以降低开销为关键诉求的解码阶段。

DeepGEMM 与 DeepEP 的分发模式可以平滑集成：

- 对于与预填充阶段**普通分发**配合使用的**连续布局内核**，需要额外一步。由于普通分发的输出是符号化形状，需要一次重排（permutation）将输出转换为该内核所期望的连续格式。我们参考了 LightLLM 项目，实现了一个自定义 Triton 内核来高效完成重排。该内核确保普通分发的输出被正确重排，从而与连续 GEMM 内核平滑集成。
- **掩码布局内核**则与 DeepEP 的**低延迟分发**无缝配合，因为二者都为解码阶段优化且支持 CUDA 图。

SGLang 还将 DeepGEMM 集成用于张量并行下的 MoE 计算。此外，DeepGEMM 提供了一个非常高效的通用 GEMM 内核，在 SGLang 中将环境变量 `SGL_ENABLE_JIT_DEEPGEMM` 设为 1 即可启用，为非 MoE 操作带来更高的计算效率。



### 双批次重叠（Two-batch Overlap）

在多节点环境中，有限的通信带宽会显著增加整体延迟。为应对这一挑战，我们参照 [DeepSeek 的系统设计](https://github.com/deepseek-ai/profile-data)实现了**双批次重叠（Two-batch Overlap，TBO）**。TBO 将单个批次拆分为两个微批次（micro-batch），让计算与通信相互重叠，同时也通过将有效批大小减半来降低峰值内存占用。不过，将 TBO 落地实践会带来一些具体的实现难点。

##### 实现挑战

尽管 DeepSeek 公开了 TBO 的设计框架，落地时仍有两个实现层面的挑战。

- **代码复杂度**：直接编写 TBO 会导致管理多个微批次的逻辑重复。这增加了代码库的复杂度，使其更难维护且容易出错，尤其是当微批次数或重叠场景增多时。
- **预填充阶段的同步问题**：当 DeepEP 的普通分发阻塞 CPU 时，要实现计算与通信的有效重叠就必须考虑这一点。这种阻塞行为可能让流水线停顿、GPU 空转，从而削弱 TBO 的性能收益。

##### 面向简洁实现的抽象

为了构建更易维护、更可复用的代码库，我们使用了一个由操作（operation）和让出点（yield point）构成的抽象层。这种方法简化了开发：我们可以像处理单个微批次那样编写代码，同时通过插入让出点策略性地暂停执行，让其他微批次继续运行。它消除了代码重复，减少了为变量添加后缀的需求，并能高效处理"某些执行在层末完成而其他尚未完成"的情况。此外，它还能以极小的代码改动适配不同的重叠区域选择或未来增强（例如三批次重叠）。下面是这种方法的简要演示：

```python
operations = [
    self._forward_attn,
    YieldOperation(),  # Pause execution for other micro-batches
    self._forward_dispatch,
    self._forward_mlp,
    YieldOperation(),  # Another pause point
    self._forward_combine,
]

# Process a single micro-batch without duplicating code
def _forward_attn(self, state):
    state.hidden_states = self.self_attn(state.hidden_states, ...)
```

##### 预填充重叠的实现

我们在预填充阶段细化了启动顺序，以避免 DeepEP 的分发操作（即使使用的是其异步模式）阻塞 CPU。具体而言：

- 分发操作会阻塞 CPU，直到 GPU 从其他 rank 接收到元数据以分配大小正确的张量。
- 若实现不当，这一期间计算流将处于空闲状态，因为没有任何计算任务被提交给 GPU。

为进行优化，我们优先在启动阻塞 CPU 的通信之前向 GPU 提交计算任务，确保 GPU 在通信期间保持忙碌。如下图所示，采用合理启动顺序的 TBO（以加粗边框标示）避免了由阻塞 CPU 的操作（即普通分发）造成的气泡（bubble）。

<img src="/images/blog/large_scale_ep/tbo-prefill.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 90%"></img>



### 专家并行负载均衡器

在 MoE 模型中，EP 常常导致 GPU 间负载分布不均。这种不均衡迫使系统等待最慢的 GPU 完成计算或通信，浪费算力周期，并且专家激活也增加了内存占用。随着 GPU 数量（EP 大小）增加，不均衡问题会愈发严重。

为此，DeepSeek 开发了[专家并行负载均衡器（EPLB）](https://github.com/deepseek-ai/EPLB)。EPLB 以专家分布统计信息为输入，计算出最优的专家排布以最小化不均衡。用户可以分配冗余专家（例如额外 32 个），与原有 256 个专家合并后构成一个 288 个专家的池子。这个池子让 EPLB 可以策略性地放置或复制专家——例如将使用最频繁的专家复制多份，或将使用频率中等的专家与很少使用的专家放在同一块 GPU 上。

除均衡负载外，EPLB 还为并行设计带来更大灵活性。在原有 256 个专家的情况下，并行度只能取 2 的幂；而 EPLB 使用 288 个专家后，可以支持更多样的配置，例如并行度为 12 或 72。

下图中，我们通过仿真展示了规模与 EPLB 算法对不均衡问题的影响。我们将 GPU 均衡度定义为各 GPU 上 MoE 层平均计算时间与最大计算时间之比，并用每块 GPU 分到的 token 数来估算其计算时间。可以看到，随着系统按节点数扩展，利用率会下降；而启用 EPLB 能显著提升利用率。



<img src="/images/blog/large_scale_ep/eplb-balancedness.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 60%"></img>



##### 面向真实服务的 EPLB

要使 EPLB 有效发挥作用，其输入分布必须与实际推理服务的负载高度吻合。有两种策略可以增强这种匹配：

- **增大批大小**：更大的批次能降低专家使用上的随机波动，从而改善均衡；可以通过扩展集群规模或使用多 token 预测（MTP）等技术来实现。
- **周期性再均衡**：定期更新专家排布可以利用时间局部性，但需要高效地重新加载专家，这就要求将专家重载操作的成本降到最低。

即便有 EPLB，某些不均衡仍然不可避免，因此进一步优化是一个有价值的未来方向。

##### 再均衡的实现

SGLang 分三个阶段实现专家再均衡，以确保高效且尽量不产生干扰：

1. **系统加载阶段**：权重可选择性地从磁盘预加载到主内存以加快再均衡，或以内存映射（mmap）方式保留在磁盘上以减少内存占用。
2. **再均衡准备阶段**：所需权重在后台异步传输到设备内存，利用空闲的 DMA 硬件引擎，不打断正在进行的 GPU 操作。
3. **再均衡执行阶段**：通过设备间拷贝更新权重。这一步还可以通过物理内存重绑定技术进一步优化。

这种分阶段方法确保再均衡既高效又无干扰，在更新期间维持系统性能。

## 评估

### 端到端性能

##### 实验设置

我们在一个由 12 个节点组成、通过 InfiniBand 互连、每个节点配备 8 块 H100 GPU 的集群上，使用 DeepSeek-V3 评估了 SGLang 不同配置的端到端性能。此次评估凸显了我们的先进优化技术带来的吞吐量提升。我们比较了以下四种配置：

- **SGLang TP16 × 6**：每两个节点组成一个独立分组，以 TP 度 16 加 DP 注意力运行 DeepSeek-V3 推理。
- **SGLang + PD 分离**：该版本包含 PD 分离与完整的 EP 优化。对于 EPLB，由于实时服务统计数据不可用，我们采用了与输入/输出数据相匹配的分布。
- **SGLang + PD 分离 + 模拟 MTP**：为模拟 MTP 的效果，我们首先将批大小翻倍、将 KV 缓存长度减半，以保持 GroupedGeMM 计算与内存访问的负载不变。此外，我们在真实注意力计算之后插入哑内核（dummy kernel），确保注意力阶段耗时与 DeepSeek 的 profile 中一致，从而准确反映 MTP 注意力机制带来的减速。我们保守地假设 MTP 下接受率为 70%。
- **DeepSeek Profile 结果**：吞吐量估计值来自 [DeepSeek 的官方剖析数据](https://github.com/deepseek-ai/profile-data)。

##### 预填充与解码阶段的性能分析

为适应不同的负载需求，我们独立评估了预填充（P）和解码（D）阶段，并假设未测试阶段的资源不受限制，以隔离并最大化被测节点上的负载——与 DeepSeek 的设置方式一致。结果总结如下：

- **预填充阶段**：在 4 个节点（4×8×H100，EP32）上，系统在提示长度为 1K、2K、4K 时分别达到每节点 57,674、54,543 和 50,302 token/秒的吞吐量。如下方柱状图所示，相较 TP16 基线最高提升 3.3 倍，主要归功于优化后的 GroupedGeMM 内核（DeepGEMM）和双批次重叠。假设负载完全均衡，我们系统的吞吐量与 DeepSeek 官方 profile 相差在 5.6% 以内。
- **解码阶段**：在 9 个节点（9×8×H100，EP72；DeepSeek 规模的一半）上评估，系统在 2K 输入下达到每节点 22,282 token/秒——较 TP16 基线加速 5.2 倍。在模拟 MTP 条件下（注意力内核被有意放慢以反映真实延迟），系统在 4K 输入下仍保持每节点 17,373 token/秒的高吞吐量，仅比 DeepSeek 官方 profile 低 6.6%。如右图所示，这些性能提升主要归因于 EP 所支持的 4 倍更大批大小——它通过大幅降低每 GPU 的模型权重内存占用提升了可扩展性。

<img src="/images/blog/large_scale_ep/e2e-prefill-decode.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 80%"></img>

### 性能剖析结果

本节将 SGLang 的性能与 DeepSeek 的推理系统进行对比，实验设置尽可能贴近 DeepSeek 的生产环境。我们分析总体吞吐量和详细的内核耗时分解，以 DeepSeek 的博客和公开 profile 数据为基准。

##### 总体吞吐量

预填充测试的场景是每设备 16,384 个 token、输入长度 4,096。由于 DeepSeek 的专家分布存在不确定性，我们评估了两种情况：一种是默认专家分布，另一种是模拟完美 EPLB（遵循组受限路由语义的随机专家选择）作为性能上界。

结果如下表所示：

|                       | DeepSeek Blog（不含缓存命中） | DeepSeek Profile | SGLang（默认） | SGLang + 模拟完美 EPLB |
| --------------------- | ------------------------------- | ---------------- | ---------------- | ------------------------------- |
| 批大小（Batch Size）            | N/A                             | 16,384           | 16,384           | 16,384                          |
| 输入长度（Input Length）          | N/A                             | 4,096            | 4,096            | 4,096                           |
| 吞吐量（每节点，Throughput (per node)） | 32,206                          | 62,713           | 50,302           | 59,337                          |

DeepSeek 的 profile 数据显示的吞吐量约为其生产环境的两倍。在默认专家不均衡下，SGLang 比 DeepSeek 的 profile 慢 20%；而模拟完美 EPLB 的情况下差距缩小到 6%。

解码的结果如下表所示：

|                       | DeepSeek Blog | DeepSeek Profile | SGLang（默认） | SGLang + 模拟 MTP（慢注意力） |
| --------------------- | ------------- | ---------------- | ---------------- | --------------------------------------- |
| 批大小（Batch Size）            | N/A           | 128              | 256              | 128                                     |
| KV 缓存长度（KV Cache Length）       | 4,989         | 4,096            | 2,000            | 4,000                                   |
| 节点数（Number of Nodes）       | 18            | 16               | 9                | 9                                       |
| 吞吐量（每节点，Throughput (per node)） | 14,800        | 18,598           | 22,282           | 17,373                                  |

在使用 DeepSeek 一半节点数的情况下，带模拟 MTP 的 SGLang 仅比 DeepSeek 的 profile 略慢。在更高批大小设置（256 个序列、2,000 输入长度）下，SGLang 达到每节点 22,282 token/秒，展现出很强的可扩展性。

##### 细节分解

下图分解了预填充的内核执行时间，并将单元测试结果作为理论上界：

<img src="/images/blog/large_scale_ep/profile-prefill.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 80%"></img>

- **默认 EPLB**：与 DeepSeek 的 profile 相比，通信内核执行时间更长、方差更大，这可能是专家不均衡更严重所致。这导致计算流气泡（bubble）延长，拖慢整体性能。
- **模拟完美 EPLB**：这种设置与 DeepSeek 的 profile 更为接近，但仍存在差异，表明还有潜在的优化空间。
- **与单元测试对比**：DeepSeek 和 SGLang 的通信时间都慢于单元测试结果；而后者（单元测试水平）在禁用 TBO 时是可以达到的，这说明如果通信成为瓶颈，这里存在潜在的优化方向。

SGLang 的解码内核分解与 DeepSeek 高度接近，如下所示：

<img src="/images/blog/large_scale_ep/profile-decode.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 80%"></img>

关键观察包括：

- **Combine 时间差异**：SGLang 的 combine 操作看起来比 DeepSeek 慢 2 倍，原因是注意力计算更短，导致通信内核忙等（busy-wait）。在模拟慢注意力的实验中，combine 时间与 DeepSeek 持平，证实了这一假设。
- **MoE 性能**：SGLang 的 MoE 内核慢 25%，可能是因为 DeepSeek 的 18 个节点（相比我们的 9 个）能更高效地分布专家，降低了 GEMM 操作的内存访问开销。
- **Dispatch 优化潜力**：DeepSeek 和 SGLang 的每层 dispatch 时间都在约 0.17ms 左右，但 DeepEP 的单元测试显示占用 SM 的潜力为 0.06ms。目前，dispatch 花费大量时间忙等数据。在收发操作之间插入慢速哑内核可将 dispatch 时间降至 0.09ms，而利用单元测试数据进行的在途时长（in-flight duration）分析表明还有进一步提升的可能。

虽然还有一些小的改进空间——主要在"Other Kernels"（其他内核）项下的算子融合——SGLang 的解码性能已与 DeepSeek 大体持平，下一步的重点是预填充优化。



### 消融实验：双批次重叠

##### 批大小与注意力时间的影响

本节研究了 TBO 在不同批大小和模拟 MTP 场景下的性能。



<img src="/images/blog/large_scale_ep/tbo-overall.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 80%"></img>



吞吐量对比与内存占用优化都表明，TBO 在预填充阶段带来两大显著收益：

- **支持更大批大小**：在原始配置下，每设备最多处理 8,192 个 token，到 16,384 个 token 时会遇到显存不足（OOM）错误。TBO 通过优化输入 token 的内存占用缓解了这一问题，使每设备 16,384 个 token 的大批次推理成为可能。在其他配置均调至最优的前提下，仅打开 TBO 开关还能再带来 40.5% 的性能提升。
- **吞吐量提升**：通过将计算（如注意力与 MLP 阶段）与通信（如 DeepEP 的 Combine 与 Dispatch）重叠，即使每设备处理的 token 数相同，TBO 也比原始配置提升 27% 至 35% 的吞吐量。

TBO 在解码阶段的影响因场景而异，性能与批大小和注意力处理时间密切相关：

- **真实测试场景**：实际场景中的加速取决于批大小是否超过 64 到 128 之间的某个阈值。低于该阈值时，TBO 收益甚微甚至为负（如每设备 32 个 token 时为 -27%），因为过小的解码批次会妨碍内核效率。批大小为 256 时加速达到 25.5%，性能为每秒 22,310 个 token。
- **模拟 MTP 场景**：在模拟 MTP 场景中，当处理 128 个请求、每个解码步生成 256 个 token 时，TBO 的加速最为显著。这是由于注意力处理时间被拉长，使计算（如 DP 注意力层）能与 DeepEP 的通信开销（如 combine 与 dispatch 步骤）相互对齐。评估显示，每设备 128 个序列时加速 35%，吞吐量为每秒 17,552 个 token，而不启用 TBO 时为 12,929。

##### 细节分解

我们评估了三种预填充场景：每批 16k token 的 TBO、8k token 的 TBO，以及 8k token 的无 TBO。下图揭示了几个关键洞察：

- **TBO 效率**：对比两个 8k 场景，正如预期，TBO 通过计算与通信重叠提升了整体效率。
- **批大小影响**：在 TBO 下把批大小从 16k 降到 8k 会带来轻微减速，反映出小批次下内核效率的下降。
- **内核性能**：有趣的是，尽管两者的内核有效批大小都是 8k，无 TBO 的 8k 场景在单内核速度上反而优于 TBO 的 16k 场景。这可能是由于 TBO 下流式多处理器（SM）数量减少、重叠期间可能存在的噪声邻居（noisy neighbor）效应，或计算与通信之间的内核不兼容。这些发现为 SGLang 指出了未来的优化方向。

<img src="/images/blog/large_scale_ep/tbo-breakdown-prefill.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 80%"></img>



对于解码阶段，我们分析了三种配置：批大小为 256 的 TBO、批大小为 256 的无 TBO，以及批大小为 128 的无 TBO。耗时分解如下：

- **TBO 与无 TBO 对比（批大小 256）**：没有 TBO 时，由于缺少重叠，通信时间显著增加。但计算内核（尤其是 GEMM）受益于更大的有效批大小，执行反而更快。
- **TBO（256）与无 TBO（128）对比**：在内核批大小相同的情况下，无 TBO 设置中只有未重叠的通信变慢，计算保持一致。与预填充不同，解码的通信内核要么完全占用 SM（收发期间），要么完全不占用（在途等待期间），因此不会与计算内核发生资源争用。



<img src="/images/blog/large_scale_ep/tbo-breakdown-decode.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 80%"></img>



### 消融实验：EPLB

本节通过总体吞吐量分析和详细的案例研究来评估 EPLB 对系统性能的影响。考虑到 EPLB 对负载分布的敏感性以及生产环境中分布漂移的问题，我们聚焦于定性的、可推广的结论，而非依赖生产数据才能得出的真实世界性能。

##### 总体结果

下图展示了 EPLB 在大规模设置下对吞吐量的影响。正如预期，EPLB 带来了显著的加速：预填充 1.49 倍、解码 2.54 倍，这得益于其缓解 GPU 间负载不均衡的能力。随着 rank 数量扩展，不均衡会加剧，而 EPLB 在我们的大规模实验中有效解决了这一问题，带来可观的吞吐量提升。



<img src="/images/blog/large_scale_ep/eplb-throughput.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 60%"></img>



##### 案例研究：负载不均衡与总体吞吐量

为探究负载不均衡与吞吐量之间的关系，我们开展了一项案例研究：解码实验设置为 1800 输入 token、100 输出 token、批大小 256，并将吞吐量和均衡度（专家间平均 token 数除以最大 token 数）随解码步骤的变化绘制成图：

<img src="/images/blog/large_scale_ep/eplb-throughput-vs-imbalance.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 60%"></img>

结果显示均衡度与吞吐量之间存在强相关性，凸显了保持高均衡度对达到最优性能的重要性。

##### 案例研究：专家分布统计

下图展示了预填充和解码样本数据的专家分布统计：

<img src="/images/blog/large_scale_ep/eplb-stat.png" style="display:block; margin-top: auto; margin-left: auto; margin-right: auto; margin-bottom: auto; width: 80%"></img>

关键观察包括：

- **专家使用不均衡**：大多数专家很少被用到，而一小部分专家被重度使用，印证了 MoE 模型固有的不均衡性。
- **预填充与解码的差异**：尽管预填充和解码的分布有相似之处，但也存在明显差异。这支持了采用 PD 分离的做法——它允许为每个阶段设置不同的专家排布，从而优化性能。

这些发现凸显了 EPLB 在应对负载不均衡方面的作用，以及针对阶段特定需求定制专家排布的价值。


## 工具集

### 一次性张量（Disposable Tensor）

PyTorch 中的内存管理可能因持久的对象引用而颇具挑战，尤其是在 CUDA 内存十分稀缺的 GPU 密集型工作流中。请看下面的例子：

```python
def ffn(hidden_state: torch.Tensor, linear1: nn.Linear, linear2: nn.Linear):
    intermediate_state = linear1(hidden_state)
    del hidden_state  # Attempt to free memory, but no effect due to external reference
    return linear2(nn.ReLU(intermediate_state))

hidden_state = ffn(hidden_state, linear1, linear2)
```

在这段代码中，`del hidden_state` 的本意是在 `intermediate_state` 计算完成后释放 `hidden_state` 占用的内存。但由于 `hidden_state` 在函数外仍被引用，`del` 操作并不会生效。这会推高峰值内存占用，带来性能下降甚至内存耗尽错误的风险。

SGLang 通过 DisposableTensor 类解决这一问题。它是 `torch.Tensor` 的子类，引入了 dispose() 方法来显式且立即释放张量的内存，绕开了 Python 引用计数的限制。其工作方式如下：

```python
def ffn(hidden_state: torch.Tensor, linear1: nn.Linear, linear2: nn.Linear):
    intermediate_state = linear1(hidden_state)
    hidden_state.dispose()  # Immediately releases CUDA memory
    return linear2(nn.ReLU(intermediate_state))

# Wrap the tensor in DisposableTensor
hidden_state = DisposableTensor(hidden_state)
hidden_state = ffn(hidden_state, linear1, linear2)
```

将 `hidden_state` 包在 `DisposableTensor` 中，并在不再需要时调用 `dispose()`，CUDA 内存就会立刻释放。这确保张量在计算中的使命一完成就释放内存，从而降低峰值内存占用、提升整体效率。



### 专家负载提取与仿真

SGLang 还包含一套用于分析和仿真 MoE 模型中专家负载分布的工具集。该功能让用户可以：

- **导出专家负载统计**：既可以提取累计统计，也可以提取逐批（per-batch）负载数据。累计统计支持 EPLB 管理器进行实时优化，而逐批数据则为分析和仿真提供细粒度的洞察。
- **仿真专家利用率**：无需昂贵的硬件或反复试验，就能对各种配置下的专家均衡情况进行建模。例如，用户可以从中等规模配置（如 2x8xH100 或 8xH200）采集负载数据，然后仿真大规模 22 节点部署的性能。

这一仿真能力让用户能够评估再均衡频率、节点数量或批大小等因素对系统性能的影响，是在扩展规模之前调优配置的一种低成本方式。


## 局限与未来工作

尽管我们面向 DeepSeek-V3 推理的 SGLang 实现展示了显著的吞吐量提升，但仍存在以下几项局限和未来改进方向：

1. **延迟优化**：当前以吞吐量为重，导致首 token 延迟（TTFT）为 2–5 秒、每 token 生成时间（ITL）约 100ms，要满足实时场景还需进一步优化。
2. **序列长度限制**：由于只使用了 96 块 GPU，仅能支持较短的序列。扩充 GPU 资源即可支持更长的序列，这对某些应用至关重要。
3. **多 token 预测（MTP）集成**：SGLang 支持 MTP，但尚未与 DP 注意力完全集成，降低了混合并行配置下的效率。
4. **EPLB 分布**：本博客的实验为专家并行负载均衡器（EPLB）使用的是同分布（in-distribution）数据，可能无法反映现实世界的变化。后续工作应实验分布发生漂移时的性能表现。
5. **灵活的张量并行（TP）大小**：对 DeepSeek-V3 而言，稠密 FFN 的内存最优 TP 大小虽然较小但大于 1。目前 SGLang 只支持纯 TP 或纯 DP，导致内存利用并非最优，需要更灵活的 TP 选项。
6. **Blackwell 支持**：目前我们的实现仅支持 NVIDIA Hopper 架构。我们正在积极扩展对下一代 Blackwell 架构的兼容性。如果你有兴趣支持或赞助这项开发工作，欢迎联系 [lmsys.org@gmail.com](mailto:lmsys.org@gmail.com)。


## 结论

借助 PD 分离、专家并行（EP）以及精心打磨的并行设计，我们在 SGLang 中以卓越的性能复现了 DeepSeek 的推理框架。我们的开源成果——达到每秒 52.3k 输入 token 和 22.3k 输出 token——展示了 SGLang 在大规模 LLM 推理上的实力。我们邀请社区来探索、复现并扩展这项工作，共同突破高效 AI 部署的边界。


## 致谢

我们谨向以下团队与合作伙伴致以诚挚的谢意：

- **SGLang 核心团队与社区贡献者** — Jingyi Chen, Cheng Wan, Liangsheng Yin, Baizhou Zhang, Ke Bao, Jiexin Liang, Xiaoyu Zhang, Yanbo Yang, Fan Yin, Chao Wang, Laixin Xie, Runkai Tao, Yuhong Guo, Kaihong Zhang, Lei Yu, Yu-Hsuan Tseng, Qilin Tian, Peng Zhang, Yi Zhang, Yineng Zhang, Byron Hsu，以及许多其他人。
- **[Atlas Cloud](https://www.atlascloud.ai) 团队** — Jerry Tang, Wei Xu, Simon Xue, Harry He, Eva Ma 及同事们——提供了 96 卡 NVIDIA H100 集群，并给予快速响应的工程支持。
- **NVIDIA 方案架构团队** — Xuting Zhou, Jinyan Chen 及同事们——为专家并行的无缝集成所做的贡献。
- **NVIDIA 企业产品团队** — Trevor Morris, Elfie Guo, Kaixi Hou, Kushan Ahmadian 及同事们——对 DeepSeek R1 内核的优化。
- **LinkedIn 团队** — Biao He, Qingquan Song, Chunan Zeng, Yun Dai, Yubo Wang 及同事们——对 Flash-Attention 3 后端的优化。
- **Mooncake 团队** — Shangming Cai, Teng Ma, Mingxing Zhang 及同事们——在 SGLang PD 分离方面的合作。
- **FlashInfer 团队** — Zihao Ye, Yong Wu, Yaxing Cai——额外的 DeepSeek R1 内核优化。
- **Dynamo 团队** — Kyle Kranen, Vikram Sharma Mailthody 及同事们——对 SGLang PD 分离的额外支持。

感谢大家的宝贵支持与协作。


## 附录

**相关 PR**：[#1970](https://github.com/sgl-project/sglang/pull/1970) [#2925](https://github.com/sgl-project/sglang/pull/2925) [#4068](https://github.com/sgl-project/sglang/pull/4068) [#4165](https://github.com/sgl-project/sglang/pull/4165) [#4232](https://github.com/sgl-project/sglang/pull/4232) [#4390](https://github.com/sgl-project/sglang/pull/4390) [#4435](https://github.com/sgl-project/sglang/pull/4435) [#4521](https://github.com/sgl-project/sglang/pull/4521) [#4654](https://github.com/sgl-project/sglang/pull/4654) [#4767](https://github.com/sgl-project/sglang/pull/4767) [#4770](https://github.com/sgl-project/sglang/pull/4770) [#4836](https://github.com/sgl-project/sglang/pull/4836) [#4880](https://github.com/sgl-project/sglang/pull/4880) [#4957](https://github.com/sgl-project/sglang/pull/4957) [#5068](https://github.com/sgl-project/sglang/pull/5068) [#5085](https://github.com/sgl-project/sglang/pull/5085) [#5295](https://github.com/sgl-project/sglang/pull/5295) [#5415](https://github.com/sgl-project/sglang/pull/5415) [#5432](https://github.com/sgl-project/sglang/pull/5432) [#5435](https://github.com/sgl-project/sglang/pull/5435) [#5530](https://github.com/sgl-project/sglang/pull/5530) [#5558](https://github.com/sgl-project/sglang/pull/5558) [#5561](https://github.com/sgl-project/sglang/pull/5561) [#5626](https://github.com/sgl-project/sglang/pull/5626) [#5657](https://github.com/sgl-project/sglang/pull/5657) [#5805](https://github.com/sgl-project/sglang/pull/5805) [#5819](https://github.com/sgl-project/sglang/pull/5819) [#5890](https://github.com/sgl-project/sglang/pull/5890) [DeepEP#142](https://github.com/deepseek-ai/DeepEP/pull/142)
