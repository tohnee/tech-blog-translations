---
title: "vLLM 携手 Mooncake：大规模智能体负载服务"
title_en: "Serving Agentic Workloads at Scale with vLLM x Mooncake"
source: https://vllm.ai/blog/2026-05-06-mooncake-store
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM 携手 Mooncake：大规模智能体负载服务

> 原文：[Serving Agentic Workloads at Scale with vLLM x Mooncake](https://vllm.ai/blog/2026-05-06-mooncake-store) · vLLM 博客

作者：Yifan Qiao、Trong Dao Le、Ao Shen、Zhewen Li、Bowen Wang

[#智能体](https://vllm.ai/blog/tags/agentic)[#KV缓存](https://vllm.ai/blog/tags/kv_cache)[#大规模服务](https://vllm.ai/blog/tags/large-scale-serving)[#分离部署](https://vllm.ai/blog/tags/disaggregation)

![](https://vllm.ai/blog-assets/figures/2026-05-06-mooncake-store/hero_vllm_mooncake.svg)

**TL;DR：** 智能体负载会产生大量共享前缀，而这些前缀常常在多轮之间被反复重算。通过将 Mooncake 的分布式 KV 缓存存储集成到 vLLM 中，我们在真实的智能体负载轨迹上实现了 **3.8 倍的吞吐量提升**、**46 倍的 TTFT 降低**和 **8.6 倍的端到端延迟降低**，并可近乎线性地扩展到 **60 个 GB200 GPU**。

## 智能体负载正在重塑 LLM 服务

随着 Claude Code 和 OpenClaw 等 LLM 智能体的兴起，推理负载正在经历一场根本性的转变。正如 Jensen 在 GTC 2026 [主题演讲](https://www.nvidia.com/gtc/keynote/)中所强调的，LLM 正在超越简单的聊天机器人，走向能够围绕复杂目标进行规划、推理和行动的自主长时运行系统。

智能体负载的独特之处在于其结构。它们通常由长程多轮循环构成，在*推理步骤*（模型处理上下文并产出中间思考）与*动作步骤*（模型发起工具调用并接收外部输出）之间交替进行。

为了量化这一行为，我们收集并分析了 Codex 与 GPT-5.4 在 SWE-bench Pro 数据集上的负载轨迹。我们还将该数据集开源在[这里](https://huggingface.co/datasets/Inferact/codex_swebenchpro_traces)，以鼓励社区对智能体服务负载开展更广泛的研究。

图 1 总结了 Codex/SWE-bench Pro 负载轨迹，并展示了一个具有代表性的智能体会话。

![Figure 1: Anatomy of an agentic trace from the Codex/SWE-bench Pro corpus. Each row is one LLM call; per-turn sizes use medians across 610 traces. The cached prefix (system prompt, skills/memory, prior turns' history) is reused turn after turn, while only the new tool output and the model's decode are active each turn.](https://vllm.ai/blog-assets/figures/2026-05-06-mooncake-store/agentic_trace.svg)

图 1：来自 Codex/SWE-bench Pro 语料的智能体负载轨迹剖析。每一行代表一次 LLM 调用；每轮的大小采用 610 条轨迹的中位数。被缓存的前缀（系统提示词、技能/记忆、先前各轮的历史）会在一轮又一轮中被复用，而每一轮真正活跃的只有新的工具输出和模型的解码。

这一模式十分惊人：到第 30 轮时，上下文长度增长到约 **80K token**，最长的上下文可以超过 **180K token**。然而每一轮通常只引入几百到几千个新 token，其余都是模型已经见过的前缀。在整个数据集上，平均输入输出 token 比约为 **131:1**。

如果我们能缓存这些前缀，被缓存部分的预填充就几乎免费。每轮的真实成本只剩新增的增量部分。

在整个 Codex/SWE-bench Pro 数据集（共 610 条轨迹，每条轨迹的中位轮数为 33 轮）上，我们观察到：

- 94.2% 缓存命中率
- 131:1 的输入输出比
- 平均每轮上下文增长约 2,242 个 token
- 每条轨迹的上下文中位数从 12K 增长到 80K token
- 轮间延迟中位数为 5.2 秒，P99 达 81.4 秒

然而，对于智能体负载，将 KV 缓存本地卸载到 CPU DRAM 或磁盘会遇到两大局限。

- **容量有限与驱逐。** 一个 100K token 的上下文可能占用数 GB 存储（例如 Kimi-2.5 的 FP8 KV 缓存约 3.8 GB）。在一个繁忙、服务众多长时会话的实例上，这些庞大的前缀缓存会迅速占满本地容量并触发驱逐。
- **跨实例未命中。** 为了负载均衡，路由器不一定总会把会话的下一轮调度到同一个 vLLM 实例上。如果会话被迁移到另一个实例，该实例从未见过这个前缀，必须从头重算。

**要点**：我们不能再把推理服务视为一组相互隔离的 vLLM 副本。对于智能体负载，各实例需要共享一个分布式 KV 缓存池，以同时提供更大的聚合容量和跨实例的缓存命中。

## 使用 Mooncake Store 构建分布式 KV 缓存池

[Mooncake](https://github.com/kvcache-ai/Mooncake) 是一个用于 KV 缓存传输和分布式存储的开源高性能库。vLLM 已经通过 [`MooncakeConnector`](https://docs.vllm.ai/en/stable/features/mooncake_connector_usage/) 将 Mooncake 用于预填充-解码（PD）分离部署，借助 Mooncake 的传输引擎在 GPU 之间搬运 KV 缓存。现在，我们把这一集成向前推进一步：用 Mooncake Store 构建分布式 KV 缓存池。

图 2 展示了总体设计。

![Figure 2: Overall design of the vLLM distributed KV cache pool. Multiple vLLM instances embed Mooncake clients and share a cluster-wide Mooncake Store. The Mooncake master manages KV-block metadata, service discovery, and client health, while workers transfer KV blocks between GPU HBM and the distributed DRAM or SSD pool over RDMA.](https://vllm.ai/blog-assets/figures/2026-05-06-mooncake-store/overall_design_option_C.svg)

图 2：vLLM 分布式 KV 缓存池的总体设计。多个 vLLM 实例内嵌 Mooncake 客户端，共享一个集群范围的 Mooncake Store。Mooncake master 管理 KV 块元数据、服务发现和客户端健康状态，而 worker 通过 RDMA 在 GPU HBM 与分布式 DRAM 或 SSD 池之间传输 KV 块。

从高层看，Mooncake Store 由一个 master 服务器和一组客户端组成。master 服务器在集群范围内运行，管理元数据，包括 KV 块哈希、大小等。它还监控客户端的健康与可用性，提供服务发现和失效节点清理。

Mooncake 客户端运行在 GPU 节点上，管理本地 CPU/DRAM/SSD 资源。客户端之间通过 RDMA 相连以进行 KV 缓存传输。它们共同构成了一个分布式 KV 缓存池。

vLLM 集成接入现有的 [`KVConnector`](https://github.com/vllm-project/vllm/blob/db9a84e0cd0e17ab693467ff4a71103abd4b77bf/vllm/distributed/kv_transfer/kv_connector/v1/base.py) 接口——与 PD 分离部署所用的抽象相同。该连接器承担两个角色：

在**调度器侧**，当新请求到达时，vLLM 对提示词的 token 块计算哈希，向 Mooncake master 查询匹配的 KV 缓存块，并利用查询结果指导调度决策。

在 **worker 侧**，vLLM 在每个 GPU worker 中内嵌一个 Mooncake 客户端，并启动后台线程负责数据搬运。GPU KV 缓存内存被注册为 RDMA 缓冲区，从而可以通过 Mooncake 客户端进行 GPUDirect RDMA 读写，既不占用 SM，也无需经 CPU 内存中转。

## 设计要点

### 基于 GPUDirect RDMA 的免 SM、零拷贝 KV 传输

传统上，GPU 到 CPU 的数据传输要么由 `cudaMemcpyAsync` 处理——它使用 GPU 拷贝引擎，但对于大量小传输可能吞吐量欠佳；要么启动专用 GPU 内核，用 SM 来拷贝数据。基于内核的拷贝在处理大量小传输时表现良好，但也会干扰 GPU 上正在运行的其他内核。

我们采用第三条路径：使用 RDMA 网卡和 GPUDirect RDMA 在 GPU HBM 与 CPU 内存之间直接搬运 KV 块。这条路径不需要中转缓冲区，也不消耗 SM，并且在大量小 KV 块传输时同样表现良好。

得益于 Mooncake 传输引擎，传输路径还可以通过多网卡池化和拓扑感知路径选择来利用节点上的多个 RNIC。这使得 KV 传输能够聚合带宽，更好地利用各网卡上的可用网络带宽。

### 全异步传输

尽管 RDMA 操作是异步的，但准备描述符和发起 RDMA 读写仍需要可观的 CPU 工作。这一开销随序列长度增长，因为更长的序列包含更多 KV 块。

为避免阻塞可能延迟 GPU 内核启动的主 CPU 路径，所有 RDMA 操作都在专用的后台 I/O 线程上运行。从 vLLM 的视角来看，这使得传输路径完全异步。

### 通过 MultiConnector 同时启用 PD 与分布式 KV 缓存池

这一集成还可以通过 [`MultiConnector`](https://github.com/vllm-project/vllm/blob/main/vllm/distributed/kv_transfer/kv_connector/v1/multi_connector.py) 接口自然地扩展到 PD 分离部署。如图 3 所示，`MultiConnector` 是一个把多个子连接器串联起来的包装器。每个连接器独立运作，不依赖其他连接器。

![Figure 3: PD disaggregation combined with the distributed KV cache pool via MultiConnector.](https://vllm.ai/blog-assets/figures/2026-05-06-mooncake-store/animation.gif)

图 3：通过 MultiConnector 将 PD 分离部署与分布式 KV 缓存池相结合。

**预填充：** 预填充实例为 PD 连接器准备 KV 块，同时通过 store 连接器把它们存入分布式 KV 缓存池。发生缓存命中时，vLLM 会查询所有连接器，并能从 Mooncake Store 连接器恢复匹配的前缀。

**解码：** 当解码实例把 KV 块写入分布式池时，它们对预填充实例立即可见。解码本身目前并不从池中读取：由于 vLLM 会把每个请求同时调度到预填充实例和解码实例，预填充实例会从池中加载前缀 KV 块，并通过 PD 连接器转发给解码端。

我们正在努力实现同时从预填充实例和分布式池进行多路径 KV 缓存加载，以最大化可用网络带宽。

## 性能

当前实现可在[这里](https://github.com/vllm-project/vllm/pull/40900)获取。我们还在构件仓库中提供了基准测试脚本，见[这里](https://github.com/ivanium/vllm/tree/feat/mooncake-store-int/scripts/mooncake/artifacts)。本文重点介绍两个结果。

我们在 GB200 节点上以 PD 分离方式运行 Kimi-2.5 NVFP4 模型。预填充实例使用 TP4，解码实例使用 DP8 + EP。我们发现这一配置提供了最佳的延迟-吞吐量折中。

### 加速真实的智能体负载轨迹

我们首先使用前文所述的 Codex 智能体负载轨迹，在真实场景下评估 vLLM。在该实验中，我们以 **1P1D** 部署模型，共使用 **12 个 GPU**。

![Figure 4: vLLM with Mooncake Store vs. baseline on realistic Codex agentic traces (1P1D, 12 GB200 GPUs). The distributed KV cache pool improves throughput by 3.8x, reduces P50 TTFT by 46x, and reduces E2E latency by 8.6x, driven by a cache hit rate increase from 1.7% to 92.2%.](https://vllm.ai/blog-assets/figures/2026-05-06-mooncake-store/pd_compare_mooncake_vs_nixl.png)

图 4：在真实 Codex 智能体负载轨迹上，vLLM + Mooncake Store 与基线的对比（1P1D，12 个 GB200 GPU）。分布式 KV 缓存池将吞吐量提升 3.8 倍，P50 TTFT 降低 46 倍，E2E 延迟降低 8.6 倍，这得益于缓存命中率从 1.7% 提升到 92.2%。

分布式 KV 缓存池将 vLLM 吞吐量提升 **3.8 倍**，并将 P50 TTFT 和 E2E 延迟分别降低 **46 倍**和 **8.6 倍**。这些收益来自缓存命中率的急剧提升：从 **1.7%**（只缓存系统提示词）提升到 **92.2%**（几乎整个前缀都被缓存）。

### 横向扩展到多节点

在可扩展性测试中，我们进一步增加了节点数量，并使用一个从 Codex 负载派生的合成数据集来进行受控的扩展实验。

实验设置：

- 20K 个公共 token（系统指令）
- 首次输入 10K token
- 每轮输入长度 2,048 token
- 900 个输出 token
- 共 30 轮
- 会话数量随 GPU 数量扩展：75 → 150 → 225 → 300 → 375
- 参数的选取大致对齐原始 Codex 负载，并将总输出/输入比保持在约 1.3%

![Figure 5: Scaling throughput with Mooncake Store from 12 to 60 GB200 GPUs under round-robin routing. The system achieves >95% cache hit rate at all scales and scales nearly linearly.](https://vllm.ai/blog-assets/figures/2026-05-06-mooncake-store/pd_scaling.png)

图 5：在轮询路由下使用 Mooncake Store 将吞吐量从 12 个 GB200 GPU 扩展到 60 个 GPU。系统在所有规模下均实现 >95% 的缓存命中率，并且近乎线性扩展。

为了在跨节点流量下对数据路径进行压力测试，我们使用了轮询路由。这样一来，请求在不同轮之间可能被调度到不同节点上，常常需要从先前的节点获取 KV 缓存。

如果没有分布式 KV 缓存池，这种路由模式会造成大量缓存未命中和严重的吞吐量下降。而使用 Mooncake Store，vLLM 始终保持 **95%** 以上的缓存命中率，并且系统近乎线性地扩展到 **60 个 GPU**。

这一结果表明，分布式 KV 缓存池在集群扩大的同时显著提升了缓存命中率，并保持了高效的数据路径。

## 下一步计划

我们正在积极开发以下特性与优化。

- **分布式磁盘卸载。** 将存储层级从 CPU DRAM 扩展到 NVMe SSD 和分布式文件系统，实现更大的缓存容量。
- **混合模型的 KV 缓存卸载。** 支持采用混合注意力机制的新兴模型架构，这类架构可能在不同层需要不同的缓存策略。
- **缓存感知路由。** 将请求路由器与 KV 缓存池协同设计，使各轮请求被导向已持有相关前缀的实例，在回退到分布式池之前最大化本地缓存命中。
- **进一步的数据路径优化。** 在 RDMA 之外利用 NVIDIA 多节点 NVLink 实现更快、多路径的 KV 缓存传输。我们还在探索类 [DualPath](https://arxiv.org/abs/2602.21548) 的方案，同时从预填充和解码实例加载 KV，以最大化聚合带宽。

## 致谢

vLLM 的 Mooncake Store 集成在很大程度上受到 [vLLM-Ascend](https://github.com/vllm-project/vllm-ascend) 中先前工作的启发。我们特别感谢蚂蚁集团的 Chao Lei 完成初始实现，以及 Inferact 的 Zijing Liu 提供智能体负载轨迹与分析。

我们还要感谢 Approaching.AI 的 Jiahao Lu、Zuoyuan Zhang、Zihan Tang 和 Ke Yang，华为的 Pengbo Zhao、Fuqiao Duan 和 Tianyu Xu，阿里云计算的 Tianchen Ding、Xuchun Shang、Xingrui Yi 和 Teng Ma，蚂蚁集团的 Yunxiao Ning、Dejiang Zhu 和 Shoujian Zheng，以及 9#AISoft 的 Feng Ren 提供的宝贵技术反馈。

我们感谢更广泛的 vLLM 与 Mooncake 社区的支持与建议。最后，特别感谢 Inferact 团队在本项工作全程中的紧密合作与讨论。
