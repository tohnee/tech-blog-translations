---
title: "vLLM 中的弹性专家并行（Elastic EP）"
title_en: "Elastic Expert Parallelism in vLLM"
source: https://vllm.ai/blog/2026-05-14-elastic-expert-parallelism
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM 中的弹性专家并行（Elastic EP）

> 原文：[Elastic Expert Parallelism in vLLM](https://vllm.ai/blog/2026-05-14-elastic-expert-parallelism) · vLLM 博客

作者：Itay Alroy（NVIDIA）、Yongji Wu（Sky Computing）、Rui Qiao（Anyscale）、Tyler Michael Smith（Red Hat）、Moein Khazraee（NVIDIA）、Omri Kahalon（NVIDIA）、Tzu-Ling Kan（NVIDIA）、Ron Tourgeman（NVIDIA）

[#大规模服务](https://vllm.ai/blog/tags/large-scale-serving)[#弹性EP](https://vllm.ai/blog/tags/elastic-ep)[#专家并行](https://vllm.ai/blog/tags/expert-parallelism)[#MoE](https://vllm.ai/blog/tags/moe)[#容错](https://vllm.ai/blog/tags/fault-tolerance)

专家并行（EP）是以高吞吐量服务混合专家（MoE）模型的关键技术。WideEP 部署（EP 跨越众多 worker）能够最大化 KV 缓存容量，从而支持极高的并发或极长的上下文。这对强化学习工作负载尤为重要——它们既需要长上下文也需要高吞吐量；对智能体工作负载也很重要——多轮对话会不断拉长上下文长度。

在 vLLM 中，与许多其他推理框架一样，EP 过去是**静态的**：部署一旦启动，其服务容量便固定下来。如果请求量超出该容量，vLLM 无法扩容以满足需求；如果需求下降，它也无法缩容以减少 GPU 使用和成本。唯一可行的办法是以新配置完全重启，这既缓慢，又可能丢弃大量流量。

**弹性专家并行**（Elastic EP）改变了这一点。它让 vLLM 能够在运行时重新配置 worker 数量，使 MoE 部署可以随需求变化扩容或缩容，同时将对服务的干扰降到最低。

Elastic EP 通过增删数据并行（DP）worker 来扩展。在 vLLM 中，这会改变共享专家并行（EP）组的大小以及专家在各 worker 上的分布方式，详见[背景](#background-expert-parallelism-and-dp-attention)一节。只需一次 API 调用：

```
curl -X POST http://localhost:8000/scale_elastic_ep \
  -H "Content-Type: application/json" \
  -d '{"new_data_parallel_size": 8}'
```

这条 API 调用会把一个运行中的部署从当前 DP 大小调整为 8 个 worker。

![](https://vllm.ai/blog-assets/figures/2026-05-14-elastic-expert-parallelism/elastic-ep.png)

本文介绍 vLLM 中的 Elastic EP（[RFC #20323](https://github.com/vllm-project/vllm/issues/20323)、[PR #34861](https://github.com/vllm-project/vllm/pull/34861)），包括扩容与缩容流程、vLLM 如何将重配置与正在执行的请求相协调、该特性如何与 EPLB 及 EP 通信后端交互，以及为什么这项工作与 vLLM 新兴的容错方向高度相关。本文还讨论了 NIXL EP（[PR #35627](https://github.com/vllm-project/vllm/pull/35627)）这一后端，其通信模型与弹性重配置和容错尤其相关。

> **面向运维人员的 TL;DR：**
>
> - Elastic EP 让 vLLM 能够在运行时通过改变 DP 大小来扩容或缩容 MoE 部署，而无需重启服务器。
> - 通过 `POST /scale_elastic_ep` 触发调整；vLLM 会重新配置在线拓扑，并按需重新分配专家。
> - 这条运行时重配置路径是 vLLM 容错服务的核心构件。
> - NIXL EP 能显著减少扩缩容事件期间的重初始化工作，并提供 EP 侧的故障检测、报告与恢复能力。

## 背景：专家并行与 DP 注意力

在 MoE 模型中，注意力层保持稠密，而大多数前馈层被替换为稀疏专家层，将每个 token 路由到一组被选中的专家。在深入弹性扩展之前，先了解 Elastic EP 所依赖的两种并行策略会有帮助。

**数据并行（DP）注意力**使用请求级并行：每个引擎核心处理不同的请求分片，并维护各自的 KV 缓存和调度器。这在 MLA 等架构中尤其有用，否则张量并行（TP）会在各 GPU 上复制 KV 缓存，浪费内存并限制批大小。

**专家并行（EP）**用于专家层。它不把每个专家切分到多个 GPU 上，而是将专家分布到不同的 GPU，token 只被派发给拥有被选中专家的 GPU。

在 vLLM 中，注意力在每个 DP worker 上独立运行，而专家层在这些 worker 之间共享同一个 EP 组（EP 组大小为 `DP x TP`）。Elastic EP 在运行时改变 DP worker 数量，从而相应调整 EP 组规模，并在其中重新分配专家。

## 挑战：哪些状态需要改变？

在运行时扩展 DP 不仅仅是启动或终止进程。EP 大小的变化会使若干运行时状态失效：

- **分布式通信组。** EP、DP 和 world 组都内嵌了一个固定的 rank 集合。
- **专家分配。** EP 大小变化时，专家到 rank 的映射随之改变。
- **模型权重。** 新 rank 需要模型权重，而重分配后现有 rank 可能需要更新后的专家权重。
- **CUDA Graph 与编译状态。** CUDA Graph 捕获和 `torch.compile` 都围绕特定假设做特化，而拓扑变化时这些假设随之改变。

因此，该实现把扩展视为一个协作式状态机。每个阶段都有显式的同步点，而这些同步点必须与模型前向执行安全共存。

## 扩容流程

从 `DP=N` 扩到 `DP=M`（其中 `M > N`）比缩容更复杂，因为需要把新 rank 引入一个正在运行的部署。

### 1. 触发与请求处理

操作从 `/scale_elastic_ep` 开始。如果设置了 `VLLM_ELASTIC_EP_DRAIN_REQUESTS=1`，vLLM 会先等待在途请求排空，最长等待 `drain_timeout` 秒（默认 120 秒）。否则，扩展会立即进行。

### 2. 新引擎核心初始化

启动新的引擎核心 worker 依赖 Ray DP 后端。扩容期间，Ray DP 后端在当前可用的 GPU 上拉起目标 DP 大小所需的额外 DP worker。新 rank 接收当前的专家映射，并以占位权重初始化模型，然后等待后续的传输与重配置阶段把它们纳入活跃拓扑。

就绪状态分两个阶段协调：一个信号允许现有 rank 创建备用组，稍后的另一个信号允许开始权重传输。

### 3. 备用通信组

一个关键设计选择是，vLLM 不会立即拆除活跃通信组。相反，现有 rank 会先创建跨越目标 rank 集合的**备用组**。这些组通过 `StatelessGroupCoordinator` 创建，它独立于 PyTorch 的全局 `WORLD` 状态。

这样就可以在切换之前准备好新配置，而旧配置在此期间仍可执行前向传播。

使用 `nixl_ep` 时，这一过渡可以是增量的：vLLM 无需拆除并重建所有 EP 侧连接，而是通过 NIXL EP 的 `connect_ranks()` / `disconnect_ranks()` API 增删 rank，同时保持现有连接不受影响。

### 4. 专家映射与权重传输

备用组就绪后，我们利用它们广播当前专家映射，并把非专家权重从现有 rank 传输给新 rank，传输工作尽可能均匀地分摊到各现有 rank 上。Elastic EP 复用了 EPLB 搬运专家权重所用的同一条 GPU 到 GPU 收发路径，并将其扩展到注意力层、归一化、嵌入及其他非专家权重，利用节点内 NVLink、跨节点 RDMA 等可用的高速互联。

专家权重不在这一阶段搬运。它们将在新拓扑激活后由 EPLB 传输。过渡期间，EPLB 的常规活动会被暂停，以免干扰重配置。

### 5. 切换

切换是所有 rank 停止使用旧拓扑并开始使用新拓扑的时刻。在这一阶段，vLLM：

1. 释放 CUDA Graph 并重置 `torch.compile` 状态。
2. 将备用组提升为活跃的 EP、DP 和 world 组。
3. 销毁旧组。
4. 针对新 EP 大小重新配置 MoE 模块。
5. 重新预热模型，使 CUDA Graph 与编译路径与新配置相匹配。

引擎协调状态（如 running 标志、wave 计数器和 step 计数器）会在新 DP 组间同步，确保每个 rank 从一致的点恢复。

此时，新 rank 已成为活跃 DP 组的一部分，可以参与前向传播并运行注意力，但尚未拥有专家。专家的归属权将在随后的 EPLB 重洗（reshuffle）中更新。

### 6. EPLB 重洗

新拓扑激活后，EPLB 会在全部 `M` 个 rank 间重新分配专家。这一步更新专家映射，并执行新布局所需的专家权重搬运。重洗完成后，EPLB 恢复正常运行。

## 缩容流程

从 `DP=M` 缩到 `DP=N` 遵循与扩容相同的大致流程，但有一个重要区别：EPLB 重洗必须先行。即将移除的 rank 可能仍持有专家权重，因此全部 `M` 个引擎核心会先参与一次重洗，把专家整合到 `N` 个存留 rank 上，并把所需专家权重从即将离场的 rank 上迁走。

## 在 DP rank 间协调重配置步骤

一个微妙的问题是，DP 引擎核心异步运行，因此它们收到重配置通知的时间可能略有不同。当某些 rank 到达下一个 Elastic EP 阶段时，其他 rank 可能已经开始多执行一步前向。如果先到的 rank 立即继续，整个组就会在重配置与前向执行之间分裂，导致部署死锁。

Elastic EP 通过**两阶段屏障**来处理这一问题。第一个屏障带超时：如果未能在时限内完成，先到的 rank 会推断某些同伴已多进入一个引擎步骤，因此它们也返回引擎循环再迭代一次，而不是独自继续。在下一次迭代中，一旦所有 rank 都到达同一边界，第二个不带超时路径的屏障便让它们一起进入下一阶段。

## 通往容错之路

Elastic EP 是容错的核心构件，因为它为 vLLM 提供了故障发生后所需的运行时重配置路径。如果某个 rank 宕机，Elastic EP 提供了先缩容、后扩容的路径，可以移除该 rank、重新分配其专家，并在替换容量可用后将其加回，而无需重启整个部署。这是 [RFC #30112](https://github.com/vllm-project/vllm/issues/30112) 中讨论的更广泛容错方向的一部分。

从高层看，恢复流程如下：

1. 通过健康检查或后端特定的故障信号**检测**故障。
2. **缩容**以移除故障 rank 并重新分配其专家。
3. 替换容量就绪后再次**扩容**。

NIXL EP 与此也相关，因为它能够在 EP 侧检测、报告故障并从中恢复，并在容量重新可用时重连替换 rank。

## 下一步

Elastic EP 已经提供了核心的运行时重配置路径，但当前实现仍有较为特定的适用范围和几个明显的后续方向：

- **支持更丰富的并行配置。** 包括 `tensor_parallel_size>1` 以及其他并行配置。
- **支持更多服务特性。** 当前实现将 `api_server_count` 限制为 1，尚不支持 DBO 或 MoE 草稿/起草模型。
- **缩短重配置窗口。** 在重叠执行、预热开销、CUDA Graph 重新捕获以及复用先前准备好的状态等方面仍有工作要做。
- **把 Elastic EP 与自动扩缩容策略连接起来。** 运行时控制平面已经就绪；策略与编排是另外的工作（Dynamo、llm-d）。
- **支持更多 DP 后端。** 目前扩缩容操作依赖 Ray DP 后端。

## 快速上手

### 以启用 Elastic EP 的方式启动

下面的示例以 `DeepSeek-V2-Lite-Chat` 作为小型 MoE 例子。当前实现面向 `tensor_parallel_size=1`、单个 API 服务器、无 DBO 的 Ray DP 部署。

```
vllm serve deepseek-ai/DeepSeek-V2-Lite-Chat \
    --trust-remote-code \
    --tensor-parallel-size 1 \
    --data-parallel-size 2 \
    --data-parallel-backend ray \
    --api-server-count 1 \
    --enable-expert-parallel \
    --enable-elastic-ep \
    --enable-eplb \
    --eplb-config.num_redundant_experts 0 \
    --all2all-backend allgather_reducescatter \
    --gpu-memory-utilization 0.8
```

### 运行时扩容

使用 Ray DP 后端时，增加容量可以简单到把另一个节点加入 Ray 集群；一旦 Ray 看到新 GPU，Elastic EP 就能在运行时把部署扩展到这些 GPU 上。

例如，在新的 worker 节点上：

```
ray start --address="${HEAD_NODE_IP}:6379"
```

```
curl -X POST http://localhost:8000/scale_elastic_ep \
  -H "Content-Type: application/json" \
  -d '{"new_data_parallel_size": 16}'
```

### 缩容

```
curl -X POST http://localhost:8000/scale_elastic_ep \
  -H "Content-Type: application/json" \
  -d '{"new_data_parallel_size": 8}'
```

### 使用 NIXL EP 作为通信后端

如果想在 Elastic EP 中使用 NIXL EP：

```
uv pip install nixl

vllm serve deepseek-ai/DeepSeek-V2-Lite-Chat \
    --trust-remote-code \
    --tensor-parallel-size 1 \
    --data-parallel-size 2 \
    --data-parallel-backend ray \
    --api-server-count 1 \
    --enable-expert-parallel \
    --enable-elastic-ep \
    --enable-eplb \
    --all2all-backend nixl_ep
```

安装细节与传输配置请参阅 [NIXL 仓库](https://github.com/ai-dynamo/nixl)。

## 参考文献

- [RFC #20323: Elastic Expert Parallelism](https://github.com/vllm-project/vllm/issues/20323)
- [PR #34861: [1/N] Elastic EP Milestone 2](https://github.com/vllm-project/vllm/pull/34861)
- [PR #35627: [2/N] Elastic EP Milestone 2: Integrating NIXL-EP](https://github.com/vllm-project/vllm/pull/35627)
- [RFC #30112: Fault-Tolerant Expert Parallelism](https://github.com/vllm-project/vllm/issues/30112)
- [RFC #16037: Data Parallel Attention and Expert Parallel MoEs](https://github.com/vllm-project/vllm/issues/16037)

## 致谢

感谢所有为 Elastic EP 落地 vLLM 做出贡献的人。

- Sky Computing：Yongji Wu
- NVIDIA：Itay Alroy、Moein Khazraee、Omri Kahalon、Tzu-Ling Kan、Ron Tourgeman
- Red Hat：Tyler Michael Smith
- Anyscale：Rui Qiao
- 更广泛的 vLLM 社区
