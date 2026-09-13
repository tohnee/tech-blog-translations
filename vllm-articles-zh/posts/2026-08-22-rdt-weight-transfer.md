---
title: "vLLM 中基于 Ray Direct Transport（RDT）的大规模分片权重传输"
title_en: "Large-Scale Sharded Weight Transfer with Ray Direct Transport (RDT) in vLLM"
source: https://vllm.ai/blog/2026-08-22-rdt-weight-transfer
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM 中基于 Ray Direct Transport（RDT）的大规模分片权重传输

> 原文：[Large-Scale Sharded Weight Transfer with Ray Direct Transport (RDT) in vLLM](https://vllm.ai/blog/2026-08-22-rdt-weight-transfer) · vLLM 博客

作者：Aaron Hao、Sumanth Hegde、Gal Meirom、Istvan Haller、Kourosh Hakhamaneshi、Gavin Parnaby、Moein Khazraee、Omri Kahalon

[#强化学习](https://vllm.ai/blog/tags/reinforcement-learning)[#性能](https://vllm.ai/blog/tags/performance)

## 引言

在在线 RL 设置中，必须周期性地同步模型权重，以确保 rollout 基于较新的权重版本生成。随着开源模型持续扩展到万亿级以上参数量，高效的权重传输对于限制内存消耗与传输时间变得十分重要。

在这篇博客中，我们详细介绍 vLLM 中一个利用 Ray Direct Transport（RDT）的分片权重传输实现。我们的贡献如下：

- **vLLM 内的原生分片权重传输引擎**，适用于一系列模型——稠密、MoE（融合检查点或按专家检查点）以及量化模型——基于 [vLLM 的原生 RL API](https://vllm.ai/blog/2026-05-28-native-rl-apis)。
- **一个便于 RL 框架采用的简单 API**，框架只需描述其权重的布局方式，传输的全部工作由引擎负责。
- **一个把预处理与传输重叠的优化实现**，使汇聚（gather）、传输与后处理彼此重叠。
- **一个容错 rollout 演示**，展示 RDT 结合 NIXL 的容错特性。

我们能够在 48 个 8xH100 节点（32 个节点跑训练器，16 个跑推理）上，用 7.53 秒完成 Kimi K2 模型 BF16 格式的分片权重传输。实现已在 [vLLM](https://docs.vllm.ai/en/latest/training/weight_transfer/sharded_rdt/) 中可用，并在 [SkyRL 中提供了端到端示例](https://github.com/NovaSky-AI/SkyRL/tree/main/examples/train/megatron/sharded_rdt)。

![Overview: Broadcast-based weight transfer vs sharded weight transfer with RDT(NIXL backend). With NCCL, trainer rank 0 forms a collective communication group with all the inference ranks and transfers full weights via broadcast. With the sharded weight transfer engine, we utilize all trainer ranks in the transfer and further only send the shard that is needed. The transfer is further optimized to avoid gathering weights across PP ranks, and skips gathering expert layers.](https://vllm.ai/blog-assets/figures/2026-08-22-rdt-weight-transfer/rdt_blog_overview.png)

概览：基于广播的权重传输与使用 RDT（NIXL 后端）的分片权重传输对比。使用 NCCL 时，训练器 rank 0 与所有推理 rank 组成集合通信组，并通过广播传输完整权重。使用分片权重传输引擎时，我们让所有训练器 rank 参与传输，并且只发送所需的那份分片。传输还经过进一步优化，避免跨 PP rank 汇聚权重，并跳过专家层的汇聚。

## 背景

标准的权重同步是一次 NCCL 广播。训练器把每个参数 all-gather 成 HuggingFace 格式，再广播给每个推理 worker。对中等规模的模型这没问题，但随着模型增长，它有以下缺点：

1. 每个 worker 都收到完整模型：在 TP8 下，一个 worker 只保留每个权重的 ⅛，丢弃其余部分。对 Kimi K2 这样的大型 MoE 模型（常以宽专家并行部署）情况更糟，因为每层的完整参数仍可能相当大（数十 GB），损害峰值内存与传输速度。
2. 广播是集合操作：NCCL 要求所有 rank 同步参与，这在动态场景下可能有问题。大规模下可能出现拖后腿的 rank 使集合操作停滞，甚至出现副本故障。

虽然此前已有大规模分片权重传输的工作（[1](https://www.lmsys.org/blog/2026-04-29-p2p-update/)、[2](https://research.perplexity.ai/articles/weight-transfer-for-rl-post-training-in-under-2-seconds)），我们的主要关注点是两个维度上的*通用性*：

- 跨模型与布局，兼容 vLLM 支持的几乎所有模型。
- 跨 RL 框架，让其他 RL 框架也能采用这一优化的权重传输实现。

## vLLM 中的权重加载

### 一个权重的旅程

当一个新的 HuggingFace 格式权重张量到达 vLLM worker 时，它必须经历以下操作：

1. 融合（Fuse）：权重分区被融合，例如注意力层中的 Q、K、V 张量
2. 重排布局（Relayout）：根据原始权重的格式，权重可能被转置或重塑
3. 切分/选择（Split/select）：融合后的张量可以被分块，或选择参数的一个子集（例如专家并行）
4. 分片（Shard）：权重可以为张量并行而被切片
5. 拷入缓冲（Copy Into Buffer）：权重被拷回按层分配的缓冲（"layerwise buffer"）。这些逐层缓冲是 vLLM 在权重加载期间分配的暂存缓冲。
6. 处理（Process）：权重可选地被量化，并执行一些内核特定操作，如填充（padding）、跨步（striding）等。
7. 拷贝（Copy）：最终处理好的权重被拷贝进已分配的 GPU 显存

操作 1-5 在 vLLM 的权重加载器中通过[逐层重载（layerwise reloading）](https://docs.vllm.ai/en/latest/training/layerwise/)完成。逐层重载有助于确保权重更新保留 CUDA Graph，同时把内存用量控制在有界范围。

![Overview of operations in layerwise reloading (Source)](https://vllm.ai/blog-assets/figures/2026-08-22-rdt-weight-transfer/layerwise_reloading.webp)

逐层重载中的操作概览（来源）

理想情况下，权重传输时我们从训练器传输最终处理好的权重（第 6 步之后），并直接写入现役权重的存储。然而，为了支持第 6 步中各种各样的后处理操作，我们专注于传输 BF16 格式的、已分片但未处理的权重（即第 4 步之后），其余交给引擎处理。这也让我们能够通过 vLLM 支持不同的量化方案。

### 自定义权重加载行为

把步骤 1-4 移到训练器上，意味着训练器必须知道：对每个 worker 的每个权重，该 worker 最终会保留哪些字节。

显而易见的办法是计算出来：读取并行配置，推算哪个张量的哪一段属于哪个 rank，然后按此发送。然而，具体要执行的操作会因层和模型而异。两个例子是：

1. **分组查询注意力下的 QKV 融合：** 三个张量（`q_proj`、`k_proj`、`v_proj`）融合为一个张量。在 GQA 下，KV 头数可能少于 TP rank 数——因此两个 worker 可能拉取不同的 Q 张量，但相同的 K 与 V 张量。这与标准 MHA 模型不同，后者中 Q、K、V 张量的 TP 分片是一致的。
2. **Llama-4 的融合专家：** 在 Llama-4 中，HuggingFace 格式的专家张量会被转置，拆分成 `gate_proj` 与 `up_proj`，vLLM worker 的专家从中选择。

这两个例子说明了权重加载器可能具有的多样化操作集合。面对 vLLM 支持的众多架构，在训练器上实现步骤 1-4 将涉及每个模型、每层的定制操作。避免这一点的唯一办法，是在运行时为给定配置记录步骤 1-4 的确切操作集合。

### 解决方案："记录张量"试运行

为支持如上自定义权重加载行为，我们的解决方案是：在引擎初始化时，向 vLLM 的加载器递一个"记录张量"（recording tensor）——一个报告正确形状与 dtype 但不持有数据的张量子类。每一个变换——view、narrow、transpose、reshape 等——都会被追加到一条操作链上。当加载器向参数拷贝时，我们记录它从哪里拷贝（*from*）以及落在了哪里。权重同步期间，我们利用这一操作序列（"分片计划"）把训练器上的完整张量变换为 vLLM worker 所需的分片张量。

由于该计划来自 vLLM 自己的加载器，因此无论这些加载器在不同层与模型上做什么，它都在构造上是正确的。

于是，我们在训练器上执行步骤 1-4，并把 BF16 格式的分片权重传输给每个 vLLM rank。收到分片权重后，我们执行剩余的步骤 5-7，更新每个 rank 上的现役权重。

## 基于 RDT 的分片权重传输引擎

verl、SkyRL、Slime、NemoRL 等大多数流行 RL 框架都使用 [Ray](https://www.ray.io/) 编排训练，训练与推理 rank 通常作为独立的 Ray actor 管理。为开发我们的分片权重传输引擎，我们使用了 [Ray Direct Transport](https://docs.ray.io/en/latest/ray-core/api/direct-transport.html)（RDT）——一个允许 Ray actor 之间直接进行 GPU-GPU 通信的 Ray API。RDT 允许 Ray actor 方法返回 GPU 张量而不把它们从 GPU 拷出。调用方收到一个 [ObjectRef](https://docs.ray.io/en/latest/ray-core/objects.html)，当调用方读取它时，字节通过可插拔传输（NIXL、NCCL、Gloo）移动。在我们的场景中，我们选择 NIXL 后端以获得灵活的 P2P 通信，从而可以把定制的权重传输给每个消费者/推理 rank。NIXL 还提供了长时训练运行所需的容错特性。由于 RDT 基于 NIXL 实现了拉取式传输，我们实现了一个拉取式权重传输引擎：推理 rank 从一个或多个映射的训练器 rank 拉取它们所需的分片张量。完整流程如下：

### 初始化时

1. **训练器收集所有权元数据：** 训练器报告每个参数的元数据——名称、dtype 与完整形状——以及训练器布局：每个 rank 持有哪些层（流水线并行）与哪些权重名称（例如专家并行下专家参数的子集）。训练器各 rank 对这些所有权元数据做 all-gather。
2. **Rank 0 把传输元数据发送给推理 worker：** Rank 0 发送参数与所有权元数据，以及 RDT 传输所需的训练器 Ray actor 名称。
3. **每个 vLLM worker 记录自己的分片计划**：每个 vLLM rank 执行上述记录张量试运行，生成由每个参数的操作链组成的分片计划。
4. **每个 vLLM worker 构建源训练器 rank 映射：** 利用传输元数据，每个 vLLM worker 构建源训练器 rank（持有它所需参数者）与待运行分片计划的映射。当多个训练器 rank 持有某个给定参数时，vLLM worker 会以负载均衡的方式选择一个训练器 rank。针对给定参数，vLLM worker 会分散到各可用生产者之上，而不同副本中的同一 worker rank 从同一生产者拉取，以降低内存开销并提升传输速度。
5. **双方分配并注册各自的 RDT 缓冲。** 消费者的目标缓冲与生产者的源缓冲各分配一次，并预先向 NIXL 注册。

![Initialization: Trainer ranks all-gather ownership metadata. Rank-0 transmits ownership + transfer metadata to the inference ranks. Inference ranks run through the recording-tensor dry run to build a sharding plan. All ranks allocate and register their RDT buffers for weight transfer.](https://vllm.ai/blog-assets/figures/2026-08-22-rdt-weight-transfer/rdt_blog_init_flow.png)

初始化：训练器各 rank all-gather 所有权元数据。Rank 0 向推理 rank 传输所有权 + 传输元数据。推理 rank 执行记录张量试运行以构建分片计划。所有 rank 为权重传输分配并注册各自的 RDT 缓冲。

### 权重同步期间

1. **每个训练器 rank 一次只汇聚一个权重组。** 一个权重组对应一个 transformer 块（注意力 + MoE 层）。我们一次 all-gather 一层，以最小化内存开销。可选地，我们可以利用权重局部性，只汇聚特定张量。在我们的集成中，我们只在 TP 上汇聚。我们不在 PP 阶段之间汇聚，在 EP 下也避免在训练器 rank 上汇聚专家。对于 EP 下的分布式专家，我们在初始化阶段直接把每个推理 rank 映射到持有所需专家的相关训练 rank。
2. **Worker 拉取分片权重。** 每个推理 worker 遍历其记录的计划，向对应的训练器 actor 请求下一批切片。训练器 actor 对汇聚好的权重重放记录的操作，并把结果连续打包进其注册的 RDT 缓冲。worker 随后通过 RDMA 从该存储读入自己的缓冲。
3. **Worker 在后台执行处理 + 拷贝。** 一个后台线程把每个切片从 worker 侧 RDT 缓冲拷贝到逐层缓冲，随后 vLLM 引擎运行 process + copy，得到内核就绪格式的最终权重。
4. **Worker 释放该权重组。** 在某权重组的最后一个切片之后，每个 vLLM worker 向持有它的训练器 rank 发信号。一旦所有 vLLM worker 都已发信号，训练器就丢弃该组的汇聚张量，可以开始汇聚下一个。
5. **训练器结束同步**——在没有在途数据后，worker 完成逐层重载。

![Weight sync for an attention layer: Overview of operations during weight sync on one trainer and one inference rank. Weight transfer is shown for Q, K and V tensors of an attention layer.](https://vllm.ai/blog-assets/figures/2026-08-22-rdt-weight-transfer/AllScenes.gif)

注意力层的权重同步：一个训练器 rank 与一个推理 rank 上权重同步期间的操作概览。展示注意力层 Q、K、V 张量的权重传输。

![Weight sync for an MoE layer: Overview of operations during weight sync on one trainer and one inference rank. Weight transfer is shown for experts.](https://vllm.ai/blog-assets/figures/2026-08-22-rdt-weight-transfer/ExpertScenes.gif)

MoE 层的权重同步：一个训练器 rank 与一个推理 rank 上权重同步期间的操作概览。展示专家的权重传输。

## 性能优化

我们记录构建该引擎的历程，并着重介绍训练器侧的几项重要性能优化。

为此，我们使用 SkyRL 中结合 Megatron 与 vLLM、针对 Qwen3-235B-A22B 的小规模权重同步设置。训练在 4 个 8×H100 节点上进行——两个训练器节点、两个推理节点，Megatron 并行为 TP4/PP2/EP8/ETP1，vLLM 以 DP16/EP16 服务，以匹配宽 EP 服务设置。报告的权重同步数字是包括 all-gather 权重提取在内的端到端延迟，为多次权重同步的平均值（不含第一次冷启动迭代）。

作为基线，SkyRL 中的 NCCL 广播实现在相同设置下耗时 64.72s。下面我们重点展示分片权重传输引擎不同版本的性能，聚焦训练器上如何汇聚、迭代与传输模型参数。其余一切与上文描述保持一致——训练器到推理 rank 的映射、记录张量试运行等。

### V1 —— 简单迭代器（跨所有维度汇聚）

这里我们使用一个简单的迭代器，逐参数遍历模型，并把每个参数跨所有维度（TP、PP 与 EP）汇聚，产出 HuggingFace 格式的完整张量。该方法有两个缺点：

1. **汇聚包含成千上万个微小的集合操作。** MoE 检查点为每个专家单独命名。Qwen3-235B 有 94 层 × 128 专家 × 若干投影——约 37,000 个张量，其中大多数很小。逐个汇聚会带来相当可观的开销。
2. **每个 rank 都汇聚全部内容。** 在每个训练器 rank 上重建完整张量导致大量冗余内存占用。

对于上述 Qwen3-235B-A22B 设置，这种方法的端到端权重同步时间为 25.02s。

### V2 —— 优化迭代器：PP 本地、EP 本地

这里我们解决 V1 的两大缺点，将迭代器修改如下：

- **PP 本地汇聚。** 一层的 all-gather 只在同一流水线阶段内的 rank 之间进行。
- **EP 本地传输。** 专家*完全不*汇聚。训练器 rank 不再重组 MoE 层中的所有专家，而是声明哪个 rank 持有哪个专家，推理 rank 从相应的 rank 拉取。

这些优化对 Kimi K2 这样更大的模型尤其重要，不仅节省传输时间，也节省内存：Kimi K2 的一个完整 MoE 层 BF16 格式约 30GB。权重同步期间在每块 GPU 上分配如此大的缓冲很容易导致 OOM。

通过上述优化，端到端权重传输时间从 25.02s 降至 5.61s。注意还有一些额外的优化（如元数据缓存）对传输时间影响较小。更多细节见[这里](https://github.com/NovaSky-AI/SkyRL/tree/main/examples/train/megatron/sharded_rdt)。

### V3 —— 流水线化执行

在 V2 中，同步仍按顺序运行多个操作：all-gather、重放操作与传输。这三个阶段使用不同的资源，可以流水线化。

- **训练器：按权重组汇聚。** 权重作为一个 decoder 块来汇聚。这使块成为汇聚、传输与释放的单元。
- **训练器：汇聚与拉取重叠。** 训练器汇聚第 N+1 组的同时，推理 rank 仍在拉取第 N 组。
- **训练器：重放与传输重叠。** 当一个数据块的 RDMA 正在落地时，生产者对下一个块进行打包并运行重放操作。推理侧同理，可以在把张量从当前 RDT 块拷贝进逐层缓冲的同时，并行接收下一个块。
- **推理：后台处理：** 把权重从 RDT 缓冲拷贝进 vLLM 引擎分配的逐层缓冲后，我们调度 Process + Copy 操作（第 6、7 步）在后台运行。RDT 缓冲随即可以用来接收下一层的权重。

![By allowing multiple all gather layers to be present on the trainer simultaneously, we can pipeline weight extraction, NIXL transfers, and inference side post processing. This is made possible by EP/PP local extraction, which reduces the additional memory on each trainer rank](https://vllm.ai/blog-assets/figures/2026-08-22-rdt-weight-transfer/rdt_pipelined_execution@2x.png)

通过允许多个 all-gather 层同时存在于训练器上，我们可以把权重提取、NIXL 传输与推理侧后处理流水线化。这得益于 EP/PP 本地提取，它减少了每个训练器 rank 上的额外内存。

加上额外的流水线化，权重同步延迟从 5.61s 降至 3.49s。

![End-to-end weight sync latencies for Qwen3-235B-A22B, using 4 nodes of 8xH100 (Megatron trainer TP4/PP2/EP8 to vLLM DP16EP16)](https://vllm.ai/blog-assets/figures/2026-08-22-rdt-weight-transfer/rdt_qwen_weight_sync_latencies.png)

Qwen3-235B-A22B 的端到端权重同步延迟，使用 4 个 8xH100 节点（Megatron 训练器 TP4/PP2/EP8 到 vLLM DP16EP16）

### 最终结果：48 节点上的 Kimi K2

NIXL 团队在 **48 个 8×H100 节点上用 Kimi K2 验证了权重同步**。

训练器设置：Megatron，TP8/PP8/EP32/ETP1
推理设置：vLLM，TP32/EP32

| 指标 | 数值 |
| --- | --- |
| 训练器拓扑 | 32 × 8×H100 |
| 推理拓扑 | 16 × 8×H100 |
| 每次同步传输字节 | 7.9 TB |
| 权重同步时间 | **7.53s** |
| 实现的聚合带宽 | 1,049 GB/s |

我们进一步估计了理论最佳权重传输时间。该设置的绝对光速（SoL）应是把权重经网络发送所需的传输时间。训练器占用 32 个节点，每个推理副本占用 4 个节点。PP 大小为 8 时，每个 4 节点的 PP 组需要向 4 个副本发送约 2TB/8 = 0.25TB 权重，因此每组需要从 4 个节点发送约 1 TB 权重。同样，每个 4 节点的推理副本需要接收 2TB 权重。因此我们可以聚焦一个推理副本来估计光速。

需传输的字节数 = 2TB 权重
聚合带宽：400\*4 GB/s = 1600 GB/s（InfiniBand）

因此，绝对 SoL 约为 1.25s。然而，由于 vLLM 的逐层重载逻辑，目前我们不得不在训练器 PP 组之间串行传输。每层都会在 GPU 显存上分配单独的缓冲，来自 PP 组的并行传输很容易引发 OOM。因此，对于一个合理的预期传输 SoL，我们应转而看发送侧。聚焦一个 PP 组的传输时间，每个 PP 组约 0.625s。训练器 PP 大小为 8，此设置下的预期 SoL 为 0.625\*8 = 5s。实测权重同步时间为 7.53s，在该设置的预期 SoL 传输时间的约 1.5 倍以内。

## rollout 的容错性

使用 NIXL 的主要好处之一是能够处理故障。使用广播集合操作时，如果组内某个特定 rank 发生故障，整个集合操作都可能失败，集合通信组将需要重新初始化。

为了突出 RDT 的好处，我们展示一个 SkyRL 中推理引擎故障的场景。当某个推理引擎发生故障时，运行继续但处于降级状态：路由器把流量导向其余推理引擎。训练器 rank 在下一次权重同步时只与存活的引擎通信。副本恢复后，它在下一个权重同步边界重新加入，接收更新后的权重，并继续服务请求。

![Qwen3-32B model training on a Text2SQL task on 4 8xH100 nodes with 4 inference replicas. We simulate failures by killing an inference engine at step 20 and step 40. The inference engines are brought back online after a few steps. Training with RDT+NIXL continues as usual and convergence remains unaffected.](https://vllm.ai/blog-assets/figures/2026-08-22-rdt-weight-transfer/rdt_fault_tolerance.png)

在 4 个 8xH100 节点上用 4 个推理副本对 Qwen3-32B 模型进行 Text2SQL 任务训练。我们通过在第 20 步与第 40 步杀掉一个推理引擎来模拟故障。推理引擎在几步之后重新上线。RDT+NIXL 训练照常进行，收敛不受影响。

## 与 SkyRL 集成

我们基于 RDT 的权重传输引擎已集成到 [SkyRL](https://github.com/NovaSky-AI/SkyRL) 中。要使用它，只需使用以下覆盖项：

```
generator.inference_engine.weight_sync_backend=sharded_rdt \
trainer.placement.colocate_all=false
```

其他 RL 框架要采用该引擎，训练器侧需要实现的主要接口是一个 `WeightSource` 迭代器。

```
class WeightSource(ABC):
    def metadata(self) -> list[ParamMeta]: ...        # names, dtypes, full shapes — no transfer
    def __iter__(self): ...                           # yield (name, materialized tensor)

    # Optional, for sharded trainers — declare what THIS rank holds:
    def held_names(self) -> "Collection[str] | None": ... # which params are yielded?
```

可选方法 `held_names` 让训练器精确声明某个特定 rank 持有哪些参数，从而启用 V2 中的优化。

## 局限与下一步

基于 RDT 的分片权重传输引擎仍处于早期。一些局限包括：

- 加载器必须局限于可记录的操作。例如，在加载期间检查真实值的加载器会在初始化时失败
- RDT 目标缓冲位于 vLLM 的 `gpu_memory_utilization` 预算之外，必须先确定其大小再选择该比例。
- 当前实现与 vLLM 中的 EPLB 不兼容。
- 为避免逐层重载引发 OOM，权重传输目前在训练器 PP 组之间是串行的。可以对指向不同副本的 PP 组间传输并行化来避免这一点。
- 我们目前使用 RDT 的 GPU -> GPU 传输。RDT 的远程 GPU -> CPU 传输支持[最近已加入](https://github.com/ray-project/ray/pull/64815)。我们可以利用远程 GPU -> CPU 传输，避免在推理 rank 的 GPU 显存上分配额外的 RDT 缓冲。此外，为避免为每个副本在 GPU 上分配独立缓冲的额外开销，我们不得不在多个副本之间同步对同一 worker 的拉取。如果直接把模型副本存放在 CPU 内存中，这一点也可以避免。

## 致谢

这项工作是与 NIXL 团队合作的成果，他们推动了 Kimi K2 上的大规模验证，并提供了许多提升权重传输性能的实用建议。

感谢 Josh Lee 与 Stephanie Wang 在 RDT 上的指导，以及 vLLM 团队（尤其是 Ao Shen）提供的有益评审。
