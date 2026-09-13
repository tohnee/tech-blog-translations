---
title: "vLLM x AgentX：为真实世界智能体服务而优化"
title_en: "vLLM x AgentX: Optimizing for Real-World Agentic Serving"
source: https://vllm.ai/blog/2026-09-08-vllm-agentx
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM x AgentX：为真实世界智能体服务而优化

> 原文：[vLLM x AgentX: Optimizing for Real-World Agentic Serving](https://vllm.ai/blog/2026-09-08-vllm-agentx) · vLLM 博客

作者：vLLM 团队与 Inferact

[#智能体](https://vllm.ai/blog/tags/agentic)[#KV 缓存](https://vllm.ai/blog/tags/kv_cache)[#并行](https://vllm.ai/blog/tags/parallelism)[#大规模服务](https://vllm.ai/blog/tags/large-scale-serving)[#分离部署](https://vllm.ai/blog/tags/disaggregation)[#性能](https://vllm.ai/blog/tags/performance)

![](https://vllm.ai/blog-assets/figures/2026-09-08-vllm-agentx/hero-vllm-agentx.png)

**TL;DR：** 智能体工作负载正在成为 vLLM 流量的主要来源。其多轮会话、长上下文与广泛的前缀复用要求对整个服务栈进行优化。本文将梳理 vLLM 的协同方案：KV 缓存管理、并行与引擎优化，以及预填充/解码分离的方法论。

在 SemiAnalysis 的公开智能体基准 [AgentX](https://newsletter.semianalysis.com/p/agentx-inferencexv3-does-cuda-moat) 上实测，vLLM 在 DeepSeek V4 Pro 上达到最高 130K 总 token/GPU 秒，在 MiniMax M3 上达到最高 376 token/秒的交互性。在 DeepSeek V4 Pro、MiniMax M3 与 Kimi K3 上，vLLM 相对 Opus 5 API 定价拥有 14.6×–106× 的服务成本优势（见[性能](#performance-agentic-first-and-openly-verifiable)）。

![图 1：vLLM 在 SemiAnalysis AgentX 上的表现。DeepSeek V4 Pro、MiniMax M3 与 Kimi K3 的最佳 vLLM 配置的每 1 美元 TCO 总 token 对 P90 交互性曲线，并以 GB300 NVL72 上的 DeepSeek V4 Pro 作为案例研究。数据来源：SemiAnalysis AgentX。](https://vllm.ai/blog-assets/figures/2026-09-08-vllm-agentx/agentx-pareto-summary.png)

图 1：vLLM 在 SemiAnalysis AgentX 上的表现。DeepSeek V4 Pro、MiniMax M3 与 Kimi K3 的最佳 vLLM 配置的每 1 美元 TCO 总 token 对 P90 交互性曲线，并以 GB300 NVL72 上的 DeepSeek V4 Pro 作为案例研究。数据来源：SemiAnalysis AgentX。

[交互式图表](https://vllm.ai/blog-assets/interactive\_pages/vllm-agentx-pareto.html)

## 智能体工作负载画像：再看一眼

自 5 月我们发布第一篇关于[服务智能体工作负载](https://vllm.ai/blog/2026-05-06-mooncake-store)的文章以来，智能体流量的占比持续增长。截至 2026 年 6 月，[OpenAI 报告](https://openai.com/signals/enterprise-data/)称，在企业客户中，Codex 产生的输出 token 占 Codex 与 ChatGPT 合计输出的 64%。

不断增长的 token 消耗沿两个轴对服务基础设施施压：成本与延迟。成本效率决定固定的硬件预算能容纳多少并发智能体；延迟决定每个智能体推进其推理与工具使用周期的速度。因此，优化智能体服务意味着整体改善延迟-成本前沿。

为了在具有代表性的流量下评估这条前沿，SemiAnalysis 近期发布了 [AgentX](https://newsletter.semianalysis.com/p/agentx-inferencexv3-does-cuda-moat)，一个基于真实世界智能体编程轨迹构建的公开基准。这些轨迹具体呈现了服务系统必须应对的工作负载特征：

- **长时间运行的多轮会话。** 每个会话中位数为 43 轮。
- **长上下文、短输出。** 输入中位数 142K token，输出中位数 444 token。
- **广泛的前缀复用。** 前缀缓存命中率超过 96%。
- **子智能体密集的流量。** 44% 的会话包含至少一个子智能体，这些会话中子智能体 rollout 的中位数为四个。

这些统计源于智能体会话的构建方式。每一轮都把最新的工具结果追加到累积的上下文中，并把整体发回模型，因此输入不断增长，而每轮只新增一小段预填充，请求中几乎全部都是引擎已经见过的前缀。子智能体要么从该上下文分叉，要么从头开始，其结果会在最终答案之前合并回父会话。图 2 演示了这样一个会话：拖动滑块从第一轮走到最终答案，看看每个请求中有多少是复用的前缀、多少是新增预填充。

[交互式图表](https://vllm.ai/blog-assets/interactive\_pages/agentic-workload-explorer.html)

## 服务智能体工作负载的挑战

这些工作负载特征给高效服务带来三个挑战。

1. **前缀缓存压力**。多轮会话的每一轮都要重放目前为止的完整对话。为了让大量会话同时运行，引擎必须在轮与轮之间卸载 KV 缓存。在规模化场景下这变得更难：KV 缓存管理、前缀缓存与卸载必须跨 GPU、预填充/解码分离实例和副本高效协作。
2. **执行效率**。智能体工作负载具有长上下文与严格的延迟要求，引擎必须在更短时间内处理更多 token，并在每个 token 上做更多工作。这要求针对新的请求形态调整并行、内核、调度、投机解码以及其他引擎优化。
3. **找到合适的 P/D 比**。上下文长度与缓存命中率在不同会话与子智能体之间差异巨大，路由必须高效平衡跨 rank 的缓存亲和性与负载。这些因素使得寻找吞吐最优的 P/D 比变得困难，而且该比例还会随并发变化。

## vLLM 的方法：跨栈优化

![图 3：面向智能体服务的全栈优化。数据平面管理分布式共享 KV 缓存，执行平面把每个模型映射到合适的并行与内核，控制平面协调合理的 P/D 比与请求调度。](https://vllm.ai/blog-assets/figures/2026-09-08-vllm-agentx/full-stack-overview.png)

图 3：面向智能体服务的全栈优化。数据平面管理分布式共享 KV 缓存，执行平面把每个模型映射到合适的并行与内核，控制平面协调合理的 P/D 比与请求调度。

图 3 概括了这三个平面。本节其余部分将逐一展开，从数据平面开始。

### 数据平面：让 KV 缓存保持热态并贴近计算

#### 混合 KV 缓存管理：不断演进的基础

自 PagedAttention 以来，KV 缓存管理一直是 vLLM 的核心，而带长上下文的智能体工作负载给 KV 缓存容量带来更大压力。现代混合模型又把滑动窗口注意力与线性注意力同全注意力组合在一起，其缓存块的大小与生命周期各不相同，使分配进一步复杂化。

vLLM 的混合 KV 缓存管理器用一个简单的核心思想应对这种复杂性：以统一的内存页作为基本分配单元，通过一个共享块池进行管理（图 4）。

共享池让 vLLM 可以按需动态重新分配内存，而不是按注意力类型静态切分容量。这一点很重要，因为全注意力 KV 随序列长度增长，而滑动窗口与循环状态遵循不同的生命周期和扩展规律。因此最优划分会随并发、上下文长度与前缀复用模式而变化。

![图 4：vLLM 的混合 KV 缓存管理器。一种页大小服务所有注意力类型，单一块池在其间共享。](https://vllm.ai/blog-assets/figures/2026-09-08-vllm-agentx/hybrid-kv-cache-manager.png)

图 4：vLLM 的混合 KV 缓存管理器。一种页大小服务所有注意力类型，单一块池在其间共享。

随着新架构暴露出碎片化与传输低效，这一抽象也在持续演进。例如，[DeepSeek V4](https://vllm.ai/blog/2026-04-24-deepseek-v4) 最初的 KV 缓存布局把不同缓存类型碎片化成三个尺寸桶，分配了 92 个独立张量。如图 5 所示，这种碎片化在填充上浪费内存，对 P/D 传输与 KV 缓存卸载也不高效。

新的[打包 KV 缓存布局](https://github.com/vllm-project/vllm/pull/44577)改为把所有缓存组与层存放在每块一份连续的底层分配中，而不是 92 份碎片化的分配。这降低了描述符与 P/D 传输开销，并且在启用 FP4 indexer 时允许更小的分配单元，节省[约 10% 的 KV 缓存内存](https://github.com/vllm-project/vllm/pull/48993)。

[交互式图表](https://vllm.ai/blog-assets/interactive\_pages/dsv4-kv-cache-layout.html)

#### 分层 KV 缓存卸载：带智能保留策略的分布式 KV 缓存池

为了把前缀缓存保留到超出 GPU 显存容量、并跨越每个引擎，vLLM 已集成 [Mooncake Store](https://github.com/kvcache-ai/Mooncake) 作为分布式 KV 缓存池，设计细节见[我们之前的博客](https://vllm.ai/blog/2026-05-06-mooncake-store)。此后采用量稳步增长，我们持续为容量、效率以及智能体工作负载上的保留策略发布新功能与性能改进。

**模型架构对等。** KV 缓存卸载在 vLLM 中仍是一等公民，完整支持包括稀疏注意力、压缩注意力与线性注意力在内的新模型架构。与此同时，其他引擎功能保持完全可用且高性能，包括异步调度、P/D 分离、投机解码与并行。

**分层 KV 缓存卸载。** vLLM 支持为分布式 KV 缓存池设置分层层级，用磁盘和额外的纯 CPU 节点进一步扩展容量。这通过 vLLM 的 [Mooncake Store](https://docs.vllm.ai/en/latest/features/mooncake_store_connector_usage/#configure-mooncake) `standalone-store` 模式实现：由一个外部 Mooncake 客户端持有 CPU 池与磁盘层，vLLM worker 变成纯粹的请求方。通过在每个节点上启动独立 Mooncake 客户端，我们可以用 CPU 内存与磁盘自由扩展 KV 缓存池。我们还将分布式共享 KV 缓存池与 [Dynamo](https://github.com/ai-dynamo/dynamo)、[llm-d](https://github.com/llm-d/llm-d) 等路由器集成，这简化了路由策略，因为请求可以在任意实例上获得缓存命中。

**性能优化。** 混合模型必须为每种注意力类型分别构造键并执行查找，这会成倍放大 CPU 开销。我们通过更高效的数据结构、异步查找、把工作移出调度器关键路径以及并行的发送与接收操作降低了这一成本。实现细节见 [PR#46188](https://github.com/vllm-project/vllm/pull/46188/changes)、[PR#45444](https://github.com/vllm-project/vllm/pull/45444/changes)、[PR#45659](https://github.com/vllm-project/vllm/pull/45659/changes) 与 [PR#47317](https://github.com/vllm-project/vllm/pull/47317/changes)。

**会话感知的前缀缓存保留。** 对在线性或滑动窗口层之外还有全注意力的混合模型，前缀复用要求在复用边界处保存线性状态或滑动窗口缓存。在每个 token 处保存这些快照代价高昂，因此我们组合两种互补策略：

1. [**基于间隔的保留**](https://github.com/vllm-project/vllm/pull/43447)在每一轮自动保存提示词结尾处的缓存/线性状态。后续轮次与分叉出的子智能体通常会重放并扩展较早轮次的上下文，因此可以复用缓存的上下文。

   然而，共享前缀通常在轮内就结束了，基于间隔的保留可能保存不到检查点。为了捕捉这种复用，我们引入第二种策略：
2. [**Marconi 式选择性保留**](https://github.com/vllm-project/vllm/pull/47782)在前缀被第二次观察到时保存检查点。当请求遇到一个先前观察到但没有保留检查点的前缀时，vLLM 会重算缺失的状态并在该边界保存检查点。之后共享该前缀的请求即可复用它。

两种策略结合，在大规模智能体工作负载上保持高缓存命中率，同时避免过高的存储开销。我们的 [vLLM Kimi K3 博客](https://vllm.ai/blog/2026-07-27-k3)深入解释了技术细节。

### 执行平面：快速生成 token

#### 面向模型的并行策略

现代推理系统暴露出多个并行轴，例如张量并行（TP）、数据并行（DP）、专家并行（EP）、流水线并行（PP）与上下文并行（CP）。

然而，最优并行取决于模型架构、硬件拓扑、工作负载模式与延迟 SLO。本节我们在 NVIDIA GB 系列与 B 系列 GPU 及其 AMD 对应产品上考察两个代表性模型，并讨论我们的优化与发现。

**Kimi K3**

Kimi K3 采用多头潜在注意力（MLA）与 Kimi Delta Attention（KDA）。由于 MLA 把 KV 压缩到带一个头的单一潜在空间，普通张量并行（TP）会把该潜在缓存跨 rank 复制，效率不高。

作为 TP 的替代，我们发现[解码上下文并行（DCP）](https://vllm.ai/blog/2026-08-07-decode-context-parallelism)带来强劲的性能提升，它沿序列维度分片缓存，让每个 rank 只持有 1/N 的 KV 状态。具体而言，DCP 为智能体工作负载提供两个好处（图 6）：

- **更低的解码延迟**。MLA 注意力受内存带宽限制，其开销随上下文长度增长。随着智能体前缀变大，注意力在每个解码步骤中的占比上升，跨 rank 分片可以缩短该步骤。
- **更高的吞吐量与 KV 容量**。避免 KV 缓存复制让引擎可以在 KV 准入上不卡顿地保住更多进行中的序列，从而获得更高吞吐量。

![图 6：对 Kimi K3 而言，DCP8 相比 TP8 实现更低的解码延迟，并能扩展到更高并发。](https://vllm.ai/blog-assets/figures/2026-09-08-vllm-agentx/k3-tp8-vs-dcp8.png)

图 6：对 Kimi K3 而言，DCP8 相比 TP8 实现更低的解码延迟，并能扩展到更高并发。

DCP 的代价是额外通信：KV 缓存按序列分片，因此每个 MLA 解码层都需要注意力前的一次 query 聚合和注意力后的一次部分输出归约。

我们仔细优化了 DCP 计算路径以绕开 NCCL 操作、避免这些开销。我们使用对称内存缓冲区，对等 GPU 可以直接从中读取或写入。query 被直接多播进注意力内核消费的缓冲区。随后每块 GPU 把自己的部分注意力输出与 log-sum-exp（LSE）统计直接写入对等方的接收槽位，各 rank 在本地用 online softmax 合并结果。这些 GPU 到 GPU 的写入与计算融合进同一批内核（图 7），相比默认 DCP8 实现每层延迟降低约 13%。

![图 7：使用对称内存在 DCP4 下的 MLA 解码路径。每一步都融合为单个内核，取代 NCCL all-gather、暂存拷贝、all-to-all 与解包步骤。](https://vllm.ai/blog-assets/figures/2026-09-08-vllm-agentx/k3-dcp-symmem.gif)

图 7：使用对称内存在 DCP4 下的 MLA 解码路径。每一步都融合为单个内核，取代 NCCL all-gather、暂存拷贝、all-to-all 与解包步骤。

更大的纵向扩展域会改变最优策略。例如在 NVL72 级系统上，带数据并行的宽 EP（DEP）可以比 DCP 扩展得更好，并在相同解码延迟 SLO 下提供更高吞吐量（图 8）。在更大规模的多节点 DCP 尺寸下，分片注意力的通信开销超过了它节省的计算。DEP 把请求及其 KV 缓存分配给不同的数据并行 rank，在把 MoE 专家跨 rank 分片的同时，避免了 DCP 的注意力集合通信。

![图 8：对 Kimi K3 而言，一旦每 rank 批大小超过 3，宽 EP（DEP16）就比 DCP8 扩展得更好。](https://vllm.ai/blog-assets/figures/2026-09-08-vllm-agentx/k3-dcp8-vs-dep16.png)

图 8：对 Kimi K3 而言，一旦每 rank 批大小超过 3，宽 EP（DEP16）就比 DCP8 扩展得更好。

**DeepSeek V4**

DeepSeek V4 也有 MLA 风格的 KV 缓存，在 TP 下会被复制，导致内存使用低效。此外，其压缩稀疏注意力使 TP 的按头分片在计算上低效，原因有三：

- 压缩器路径对每个压缩位置只产生一份共享 KV 表示，而不是独立的每头状态。因此 TP 无法沿 KV 头维度切分计算，每个 rank 都要重复压缩器的工作。
- indexer 虽有 64 个头，但每个 token 只产生一次全局 top-k 选择。因此当前 TP 路径在每个 rank 上复制完整 indexer，避免了 top-k 之前的稠密分数归约，却重复了工作。
- sparse MLA 的主导开销是扫描与收集 top-k KV 缓存条目，而不是注意力算术。TP 让每个 rank 重复大量这种受内存限制的工作，却只切分了更便宜的按头计算。

实践中，prefill context parallelism（PCP）在长预填充上表现最好，而数据与专家并行（DEP）在更广的服务条件下都表现良好。

PCP 对提示词序列（query 张量）分片，把压缩器与 indexer 工作分布到各 rank，同时给 sparse MLA 一个更宽、更高效的 head 本地形状。对 32K 提示词，PCP8 相比 TP8 取得 2.65× 的预填充加速，大幅降低 TTFT。但它仍会在各 rank 间复制解码侧状态，因此最适合专用的预填充 worker。

由于 V4 的模型架构更复杂，DCP 在 DeepSeek V4 上不如在 Kimi K3 上有效（见[那些惨痛的教训](#decode-context-parallelism-dcp-does-not-transfer-cleanly-to-deepseek-v4)）。

DEP 则把请求与已解码 token 分布到数据并行 rank 上，保持注意力路径完全本地。这使 DEP 成为大多数 DeepSeek V4 配置的默认选择。

#### 在两个层级上调度混合智能体流量

智能体服务把频繁的仅追加请求（复用长前缀、只需短预填充）与偶发的横跨数万 token 的长全新预填充混在一起。这带来两个调度问题：在实例内部，长预填充可能阻塞短的交互轮次；在 DEP rank 之间，不均衡的预填充布置造成负载不均。我们用两个互补的调度控制来解决它们。

##### 打破队头阻塞

默认情况下，vLLM 的分块预填空调度器按先进先出顺序运行。一个长预填充可以一步一步占满整个 token 预算，排在同一 rank 上的短轮次在长预填充完成前完全无法被调度。这就是所谓的队头阻塞（head-of-line blocking）；图 9 在一个 rank 队列的会话视图中展示了它。

![图 9：预填充队列中的队头阻塞，单个 rank 的会话视图。左：没有块上限时，长预填充占满整个预算，短的已缓存轮次只能等待。右：设 512 token 上限后，短轮次得以加入每一步并更早开始解码。](https://vllm.ai/blog-assets/figures/2026-09-08-vllm-agentx/hol-blocking.gif)

图 9：预填充队列中的队头阻塞，单个 rank 的会话视图。左：没有块上限时，长预填充占满整个预算，短的已缓存轮次只能等待。右：设 512 token 上限后，短轮次得以加入每一步并更早开始解码。

我们用一个简单的调度策略解决这个问题：用 `--long-prefill-token-threshold` 限制一个请求每步可调度的 token 数。设 512 token 阈值后，长预填充会为短轮次腾出加入同一批次的空间，使其更早开始解码。在 B300 上运行 DeepSeek V4 Pro 时，这将每 GPU 秒总 token 数（TPGS）提高最多 93%，并把 P90 交互性改善约 2.3×。代价是长请求自身的 TTFT 变高，因此对 TTFT 敏感的部署应使用更大的阈值。

##### 对齐 DEP 预填充调度节奏

DEP 引入第二个低效点：MoE all-to-all 通信迫使各 rank 步调一致前进，因此某个正在处理预填充工作的 rank 会拖慢整组。当预填充在不同 rank 的不同步骤上到来时，这一惩罚会被反复支付。

为缓解这种不均衡，我们设置 `--prefill-schedule-interval`，只在每第 N 个引擎步骤接纳预填充工作，并使用跨数据并行 rank 对齐的计数器。这把预填充工作集中到各 rank 相同的步骤上，并提高其余步骤完全用于解码的比例。图 10 展示了 DEP8 组上的这种节奏。

![图 10：DEP8 组上的预填充调度节奏。左：预填充在不同步骤到来，反复卡住步调一致的组。右：间隔设为 4 时，预填充合并到节奏步骤上，中间的步骤为纯解码。](https://vllm.ai/blog-assets/figures/2026-09-08-vllm-agentx/prefill-schedule-interval.gif)

图 10：DEP8 组上的预填充调度节奏。左：预填充在不同步骤到来，反复卡住步调一致的组。右：间隔设为 4 时，预填充合并到节奏步骤上，中间的步骤为纯解码。

### 以最优 P/D 分离配置扩展

只优化单个引擎不足以找到分布式部署的最佳延迟-成本点，而更多的 GPU 或分离部署也不会自动改善这条前沿。预填充与解码阶段必须速率匹配。

我们使用一套标准化的两阶段速率匹配方法论，可以通过智能体工作流自动化：

**阶段 1：饱和画像。** 分别对纯预填充与纯解码部署做基准测试，扫描并行策略（如 TP 对比宽 EP）与部署规模（8、16 或 32 GPU），并发递增直到吞吐饱和。输出是一张饱和表：每个（并行，规模）配置的最大预填充/解码 req/s。

**阶段 2：P/D 扫描。** 从每个配置的阶段 1 饱和点推导 P/D 比，然后在组合的分离部署上扫描并发，采集整个工作范围内的指标。

### 闭环：面向模型的内核与社区贡献

智能体工作负载也把内核瓶颈推向长上下文注意力、投机解码与通信。这里我们重点介绍几项经过端到端实测影响的改动。我们的所有内核都完全开源，部分已被其他开源引擎采用。

对 MiniMax M3，[CuteDSL 长上下文 indexer](https://github.com/vllm-project/vllm/pull/48582) 依形状不同，将报告的 GB300 indexer 延迟改善约 3% 到 31%。上游化的 MSA top-k 路径把最坏情况内核性能提升最高 4×，并把 AgentX 端到端吞吐量提升约 7%；在报告的测试中，投机验证路径把中等批大小的解码性能提高约 20%。

对 Kimi K3，[GEMM 与 reduce-scatter 融合](https://github.com/vllm-project/vllm/pull/52079)改进了序列并行通信，而[潜在尾部 MoE 融合](https://github.com/vllm-project/vllm/pull/53152)把端到端延迟降低约 5%。

对 DeepSeek V4，社区贡献改进了 MXFP4 MoE 与 HCA 压缩（[#43584](https://github.com/vllm-project/vllm/pull/43584) 与 [#44230](https://github.com/vllm-project/vllm/pull/44230)），添加了[多流 C4A](https://github.com/vllm-project/vllm/pull/42925)，并改进了[基于聚类的 top-k](https://github.com/vllm-project/vllm/pull/43008)。

## 性能：智能体优先，且公开可验证

我们通过在 [SemiAnalysis AgentX](https://newsletter.semianalysis.com/p/agentx-inferencexv3-does-cuda-moat) 上的独立验证证明 vLLM 是智能体优先的。AgentX 是一个开放数据集，由价值 300 万美元、上下文达 1M 的真实世界智能体编程轨迹构建，运行在由超过 1,000 颗芯片、约 2 MW 算力组成的公开基准基础设施上。

![图 11：Kimi K3 运行于各种硬件时，在不同 P90 交互性下的每 1 美元总 token。来源：Kimi K3 SemiAnalysis AgentX 仪表盘。](https://vllm.ai/blog-assets/figures/2026-09-08-vllm-agentx/k3-agentx-dashboard.png)

图 11：Kimi K3 运行于各种硬件时，在不同 P90 交互性下的每 1 美元总 token。来源：Kimi K3 SemiAnalysis AgentX 仪表盘。

图 11 以 Kimi K3 仪表盘为例；该基准及其全部结果都可在 [AgentX 仪表盘](https://inferencex.semianalysis.com/inference?i_seq=agentic-traces&i_xmode=interactivity&g_runid=33418433573&i_best=0&i_active=b200_vllm%2Cb300_vllm%2Cgb200_dynamo-vllm%2Cgb300_dynamo-vllm&i_hc=1&i_advlabel=0&i_label=0)上公开访问。我们强烈建议探索其他模型与配置的帕累托结果。

本文聚焦三个开放前沿模型的结果：DeepSeek V4 Pro、MiniMax M3 与 Kimi K3。对每个模型，我们报告在保持每用户 P90 交互性高于 50 token/秒（一个常见且严苛的延迟 SLO）的前提下吞吐量最高的 vLLM 配置。下表概括关键结果。

| 模型 | GPU / 并发 | 每 GPU 秒总 token（TPGS）[1](#note-tpgs) @ P90 > 50 tok/s | P90 交互性 |
| --- | --- | --- | --- |
| [DeepSeek V4 Pro 1.6T](https://inferencex.semianalysis.com/inference/agentic/439873) | 12 个 GB300 / 256 | **83K TPGS** | 58.3 tok/s |
| [MiniMax M3 428B](https://inferencex.semianalysis.com/inference/agentic/439907) | 2 块 B300 / 24 | 70K TPGS | **74.2 tok/s** |
| [Kimi K3 2.8T](https://inferencex.semianalysis.com/inference/agentic/441066) | 16 个 GB300 / 48 | 11.8K TPGS | 62.7 tok/s |

1 每 GPU 秒总 token（TPGS）计入输入、输出与缓存 token。详细分解可通过各模型链接查看。

DeepSeek V4 Pro 代表高吞吐、高成本效益的案例。一个 12 芯片 GB300 P/D 部署服务 256 个并发智能体会话，同时在 P90 下保持 58.3 token/秒/用户。在这一工作点上，它每 GPU 秒处理 83K 总 token。

MiniMax M3 把交互性推得更远。仅用 2 块 B300，它在 P90 下保持 74.2 token/秒/用户，并提供 70K 总 TPGS。

Kimi K3 是最大的开放前沿模型之一，为前沿智能提供了例证。它拥有 2.8 万亿参数，规模大到常规单服务器部署无法容纳，而 16 个 GB300 在 P90 下保持 62.7 token/秒/用户，同时处理 11.8K 总 TPGS。

除性能外，成本是与用户日常使用和 token 经济学最相关的指标。下表将三个开放模型的服务成本与 Opus 5 对比。

| 模型 | GPU TCO/小时 | 等效 Opus 5 成本/小时[2](#note-opus) | 成本优势 |
| --- | --- | --- | --- |
| [DeepSeek V4 Pro 1.6T](https://inferencex.semianalysis.com/inference/agentic/439873) | $27.72 | $2,926 | **106×** |
| [MiniMax M3 428B](https://inferencex.semianalysis.com/inference/agentic/439907) | $4.52 | $384 | **85×** |
| [Kimi K3 2.8T](https://inferencex.semianalysis.com/inference/agentic/441066) | $36.96 | $538 | **14.6×** |

2 Opus 5 计算采用 缓存输入 × $0.50/M + 未缓存输入 × $5/M + 输出 × $25/M。它假设完美的理论缓存命中率，并排除缓存写入费用与长上下文定价溢价，这是保守且有利于 Opus 的。该比较关乎服务成本，而非模型质量。

成本优势来自智能体流量的本质特征：在超过 96% 的理论缓存命中率下，vLLM 有效复用前缀，并在与上表相同的设置下，把这种复用转化为三个模型上的服务效率。

对 DeepSeek V4 Pro，服务该实测工作负载在 GB300 基础设施 TCO 上每小时约 28 美元。用 Opus 5 处理同样的 token 量约需 2,926 美元，即使已把缓存读取价应用到每个理论上可复用的 token。B300 上的 MiniMax M3 显示出 85× 的成本优势，而 GB300 上的 Kimi K3 尽管模型规模大得多，仍便宜 14.6×。

这些是截至今天的数字；仪表盘实时开放，人人可访问。AgentX 测试工具公开于 [SemiAnalysisAI/agentx-harness](https://github.com/SemiAnalysisAI/agentx-harness)，上述每个结果都链接到其在 InferenceX 仪表盘上的运行，便于复现。

## 惨痛的教训：我们失败在哪里，学到了什么

每一个失败的想法都收窄了搜索空间。我们观察到若干貌似合理的直觉未能通过端到端测量的案例。这些功能仍在改进，但我们想分享目前为止的所学。

#### 流水线并行（PP）不适合热的智能体轮次

PP，包括[分块流水线并行（CPP）](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/dynamic_chunk_pipeline_parallel.html)，在长且全新的提示词上表现良好。大型预填充提供了足够的工作让流水线各阶段保持繁忙，吞吐量可以在很小的通信开销下近乎线性扩展。

然而，大多数智能体轮次的系统提示词与先前轮次已经被缓存，每个新请求可能只新增几百到几千 token。没有足够的新计算高效填满流水线，流水线气泡吞掉了大部分潜在收益。

教训不是 PP 无效。它对冷的、计算密集的预填充很有效，但不应成为主导智能体会话的、热的、前缀密集轮次的默认选择。

#### 解码上下文并行（DCP）无法顺利迁移到 DeepSeek V4

如前所示，DCP 对纯 MLA 模型（如 DeepSeek R1、Kimi K2.5 与 K2.7）和混合 MLA 模型（如 Kimi K3）都工作良好。然而，要在 DeepSeek V4 上实现类似收益则困难得多，因为它的注意力栈更复杂。压缩稀疏注意力与高度压缩注意力包含一个 indexer、一个额外的压缩器以及主注意力操作。上下文并行必须对所有这些子层进行划分与协调，引入了大量通信与实现复杂性。

我们在通信与计算重叠以及优化相应内核上投入巨大。即便经过这些改进，DCP 也只是追平 DEP 而非超越它。这一结果强化了执行平面小节的一个更普遍的观点：并行必须跟随模型架构。对一个潜在注意力模型奏效的策略，未必能推广到另一个。

#### 负载均衡并不保证更好的性能

在聚合式 DEP 部署中，我们观察到各 rank 之间 KV 缓存使用存在显著不均衡。直觉的应对是按队列深度、运行中 token 数或当前 KV 利用率来平衡请求。

然而，在 AgentX 的实验中，所有这些策略都不如简单的会话感知粘性路由。原因在于缓存局部性：许多智能体会话的轮间延迟很短，下一轮常常在前缀仍驻留于上一块 GPU 时就到来。把会话移到负载更轻的 rank 迫使系统取回 KV 缓存，即使前缀已保存在分布式 KV 缓存池中。传输是异步的、可与计算重叠，但并非没有代价。预取的块会临时占用 GPU KV 缓存容量，减少目标 rank 可接纳的序列数。因此系统可能得到一个更均衡的队列，总体处理的并发请求却更少。

对轮间延迟短的工作负载，保持会话局部性比完美平衡瞬时负载更有价值。路由决策必须考虑每个 worker 上已驻留的状态，而不仅仅是排队工作量。

## 前方之路：计划中的优化与未来工作

下一步是让智能体结构在整个服务栈中显式化。以下是各层的几个例子。

在控制平面，我们可以让路由对首轮请求（往往需要长的全新预填充来填满前缀缓存）与第 2 轮及以后的请求（获得高缓存复用、追加预填充相对较短）更加显式区分。这种区分避免队头阻塞，并让我们对两侧采用不同的引擎设置与并行（例如 PCP 与 CPP），使两者都效率最大化。

在执行平面与数据平面，我们正与社区合作支持：

- **智能体提示（Agent hints）。** 智能体框架或测试工具可以随请求携带提示，例如会话结构、潜在分支点与缓存位置、工具调用延迟或会话生命周期。我们的第一步是通过标准化 API 消费这些提示，然后用它们指导引擎的调度、缓存驱逐策略及其他优化。
- **可编程 KV 缓存。** 不同工作负载需要不同的放置、保留、复制与驱逐策略。可编程接口让用户能够控制 KV 缓存的预取、驱逐或软固定，以匹配自己的工作负载模式。
- **基于会话的 KV 缓存管理。** 轮间空隙提供了把保留的 KV 状态向可能服务下一轮的 worker 迁移的机会。在这个空闲间隔内预取可以隐藏传输延迟并减少冷恢复。

## 致谢

这项工作由 [Inferact](https://inferact.ai/) 牵头，并得到 vLLM 社区的大量支持。我们感谢 SemiAnalysis 开发并运营公开的 AgentX 基准，并使其方法与结果可复现。我们也感谢 NVIDIA 与 AMD 在整个工作中的紧密协作与支持。
