---
title: "vLLM 中的分层 KV 缓存卸载"
title_en: "Tiered KV Cache Offloading in vLLM"
source: https://vllm.ai/blog/2026-09-10-tiered-kv-offloading
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM 中的分层 KV 缓存卸载

> 原文：[Tiered KV Cache Offloading in vLLM](https://vllm.ai/blog/2026-09-10-tiered-kv-offloading) · vLLM 博客

作者：Or Ozeri、Danny Harnik、Ronen Schaffer、Itay Etelis、Varun Sundar Rabindranath

长上下文模型和多轮对话会产生海量 KV 缓存。当加速器内存（例如 GPU HBM）被填满时，先前已计算好的 KV 数据会被逐出。下一个需要这些数据的请求到来时，vLLM 必须从头重新计算。

**分层 KV 缓存卸载会把被逐出的 KV 数据保留下来**，存放于主机内存、存储和远端节点等多个层级。vLLM 不再重新计算，而是从较低层级重新加载数据——节省计算量、降低延迟，并提升集群的有效服务容量。

有了次级层级，KV 数据还可以**跨节点共享**——从而支持缓存的横向扩展、从共享存储热启动新实例，以及在节点之间传输 KV 数据以实现分离式服务或负载均衡。

该框架自 v0.22 起已随 vLLM 提供，详细的使用指南见[这里](https://docs.vllm.ai/en/latest/features/kv_offloading_usage/)。

---

## 以主机为中心的设计

核心设计原则：**所有 KV 数据都要流经主机内存（CPU DRAM）**。

卸载时，KV 数据先从加速器移到主机，再从主机传播到次级层级——文件系统、对象存储或远端节点。重新加载时，流向相反：某个次级层级把数据提升到主机内存，然后再加载到加速器。

![](https://vllm.ai/blog-assets/figures/tiered-kv-offloading/architecture.svg)

所有 KV 数据都流经作为主层的主机内存。次级层级把容量扩展到主机 DRAM 之外。卸载时，数据块级联写入所有层级；重新加载时，由第一个持有该块的层级提供服务。

这种设计带来几个关键优势：

### 快速释放加速器内存，按需即时分配

从加速器到主机的复制是一次快速的本地 PCIe 传输。**这次复制一完成，加速器内存就被释放**——在任何次级层级传输开始之前。存储写入、网络发送和远端 RDMA 都基于主机上的副本进行，不会再次触碰加速器内存。**重新加载时，只有当数据在主机侧就绪后才会分配加速器内存**——而不是在等待层级传输期间预先保留。这两点合起来形成了一种按需即时分配的模式：加速器内存只在实际需要时才被占用。

![](https://vllm.ai/blog-assets/figures/tiered-kv-offloading/offload-flow.svg)

加速器内存在 t2 时刻被释放——主机复制一完成就释放。次级层级的写入基于主机副本继续异步进行。

### 归并 I/O

在多加速器配置（例如 `tensor_parallel_size=8`）中，每个设备持有 KV 缓存的一个分片。该框架**会把所有分片归并到一个共享的主机内存区域**。

![](https://vllm.ai/blog-assets/figures/tiered-kv-offloading/consolidated-io.svg)

多个加速器分片汇入同一个共享主机区域。次级层级看到的是数量更少、尺寸更大的 I/O 操作——从而提升存储和网络吞吐量。

### 规范化内存布局

主机区域使用规范化的内存布局：每个页存储某一层的一个块，来自各 TP rank 的所有 KV 头被收拢到一个连续区域。定位任何一个数据块只需要一次简单的偏移计算。

固定不变的主机侧布局确保了即使各节点的 GPU 内存布局不同也能正确共享——不同的加速器类型、注意力后端（FlashAttention、FlashInfer、Triton）或并行配置都映射到同一个规范表示。

由于布局与配置无关，**不同配置的节点可以直接共享 KV 数据**——无需重映射或格式转换。一个 TP=2 节点和一个 TP=4 节点对同样的 KV 数据会产生完全相同的主机侧数据块。

### 简单的次级层级

让所有数据都经过主机内存，使得次级层级**易于构建和运维**。它们是每个 vLLM 实例下的单个进程，使用标准的 CPU 侧库（POSIX I/O、S3 SDK、RDMA verbs）传输数据，并且完全不触碰加速器内存或加速器 API。

无需跨多个进程协调，也无需理解加速器特有的内存布局。

---

## 卸载与重新加载的工作方式

操作的基本单位是**块（chunk）**——一段覆盖一组 token 的固定大小 KV 数据。默认情况下，一个 chunk 对应一个加速器块。可配置的 `blocks_per_chunk` 参数允许使用更大的 chunk，从而对主机和次级层级产生更大的 I/O。

### 卸载路径

新的 KV chunk 通过异步 DMA 从加速器移动到主机。**加速器内存立即被释放**——在任何次级层级传输开始之前。随后，分层管理器把 chunk 级联写入**所有**已配置的次级层级，读取来源是主机上的副本。

主机主层是一个**真正的 LRU/ARC 缓存**，而不是中转缓冲区。chunk 会留在主机内存中，直接服务于未来的命中。只有当主机容量耗尽时，最久未使用的 chunk 才会被逐出——即便如此，它们也仍然保存在接收过它们的某个次级层级中。

### 重新加载路径

调度器先检查主机缓存——如果 chunk 在那里，就是一次即时命中。主机未命中时，按配置的顺序查询各次级层级；第一个持有该 chunk 的层级提供服务。该层级会把 chunk 异步提升回主机内存；在此期间，调度器收到一个 `RETRY`，并在下一轮循环中重新检查。

同一个请求中的不同 chunk 可以由不同层级提供——例如，一个 chunk 来自文件系统，另一个来自远端节点。

---

## 次级层级

### 文件系统

把每个 KV chunk 作为一个文件存储在本地或网络存储上。采用内容寻址命名——相同的 token 序列映射到同一个键，因此匹配的输入会自动共享缓存数据。

当多个 vLLM 实例共享同一个存储挂载点（例如网络附加存储，或同一节点上的多个实例）时，它们**自动共享 KV 数据**，无需额外配置。

亮点：

- **非阻塞查找**
- **原子写入**
- **独立的读/写线程池**

```
vllm serve Qwen/Qwen3.6-35B-A3B \
    --kv-transfer-config '{
        "kv_connector_extra_config": {
            "spec_name": "TieringOffloadingSpec",
            "cpu_bytes_to_use": 107374182400,
            "secondary_tiers": [{"type": "fs", "root_dir": "/mnt/kv-cache"}]
        }
    }'
```

### 对象存储

通过 NIXL 把 KV chunk 存储到 S3 兼容的对象存储中。与文件系统层级使用相同的内容寻址方案。提供了一种高性价比的网络存储选项——每 GB 成本通常低于高性能文件存储，同时仍支持跨实例共享访问。

```
--kv-transfer-config '{
    "kv_connector_extra_config": {
        "spec_name": "TieringOffloadingSpec",
        "cpu_bytes_to_use": 107374182400,
        "secondary_tiers": [{
            "type": "obj",
            "bucket": "my-kv-cache",
            "endpoint_override": "http://minio:9000"
        }]
    }
}'
```

### 点对点（P2P）

支持通过网络进行**跨实例 KV 缓存共享**。使用 ZMQ 做协调，使用 RDMA（经由 NIXL）做批量数据传输。所有传输都是**主机到主机**的——任何一方都不涉及加速器内存。

P2P 层不决定从哪个对端拉取 KV 数据——那是编排层的职责（例如 [llm-d](https://github.com/llm-d/llm-d) 这样的路由器）。编排器通过请求的 `kv_transfer_params` 驱动跨节点传输。示例和更多细节见[使用指南](https://docs.vllm.ai/en/latest/features/kv_offloading_usage/#orchestration-layer-protocol)。

```
--kv-transfer-config '{
    "kv_connector_extra_config": {
        "spec_name": "TieringOffloadingSpec",
        "cpu_bytes_to_use": 107374182400,
        "secondary_tiers": [{"type": "p2p", "host": "10.0.0.1", "port": 5710}]
    }
}'
```

两个关键用例：

#### 预填充/解码分离部署

预填充实例计算 KV chunk，并把它们放入自己的主机层级。解码实例通过 RDMA 从预填充实例的主机内存中拉取这些数据。

相比基于 GPU 的 P/D 方案，一个关键优势是：**归并 I/O 把许多小的按 GPU 传输变成更少、更大的 RDMA 操作**——显著提升网络吞吐量。此外，配合*分块预填充*（chunked prefill），每个完成的预填充块都可以立即用于传输——计算与数据搬运相互重叠，从而降低首 token 延迟（TTFT）。

#### 负载均衡

把 KV chunk 从过载的 vLLM 实例转移到有可用容量的实例。任何节点都可以从任何对端拉取 chunk。

关于 llm-d 的 P2P KV 缓存共享的更多内容，请参阅[这篇博客文章](https://llm-d.ai/blog/p2p-kv-cache-sharing-llm-d)。

---

## 混合模型支持

该框架与 vLLM 的混合内存分配器集成。组合了不同层类型的模型——全注意力、滑动窗口、MLA、Mamba——都能被透明地处理。

规范化布局把所有 KV 格式归一化为统一的字节缓冲区表示。**每个 chunk 在主机上具有固定的字节大小**，无论它包含哪些层类型。不同层类型往同一个 chunk 中打包的 token 数量不同——例如，Mamba 状态层每个 chunk 覆盖的 token 远多于全注意力层，因此它们的卸载频率更低。

这意味着：

- **滑动窗口层**只重新加载窗口内的 token，而不是全部历史
- **状态空间层**（Mamba）将其状态与注意力 KV 一起卸载和重新加载

该框架支持最先进的混合架构，包括 DeepSeek V4、GLM 5.3、Nemotron 3 等。

---

## 可观测性

该框架通过 vLLM 标准的 `/metrics` 端点暴露 Prometheus 指标：

- **主机缓存利用率**——主层当前的填充比例
- **传输吞吐量**——加速器 ↔ 主机传输的字节数与耗时
- **各层级延迟**——每个层级的查找和数据传输耗时
- **各层级命中率**——哪些层级在实际服务你的工作负载

次级层级可以**定义自定义指标**（计数器、直方图、仪表），它们会被自动注册并暴露出来——无需修改框架。

---

## KV 事件

当 chunk 在层级之间移动时，框架会发出结构化的 **KV 事件**，报告哪些 chunk 被存储或逐出、来自哪个层级，以及其位置属性（本地还是远端）。次级层级也可以发出自己的事件。

这些事件让外部编排系统能够做出智能的路由决策。llm-d 和 [Dynamo](https://github.com/ai-dynamo/dynamo) 等项目消费 KV 事件，以**把请求路由到最有可能缓存命中的实例**——相比不感知缓存的调度，可获得显著更高的吞吐量和更低的延迟。此外，llm-d 还利用这些事件在节点之间编排 P2P KV 传输。

---

## 添加一个新的次级层级

次级层级接口非常精简——只有四个核心方法：

```
class SecondaryTierManager(ABC):

    def lookup(self, key, req_context) -> LookupResult:
        """Does this tier have a chunk? Returns HIT, MISS, or RETRY."""

    def submit_store(self, job_metadata: JobMetadata) -> None:
        """Start async store from host to this tier."""

    def submit_load(self, job_metadata: JobMetadata) -> None:
        """Start async load from this tier to host."""

    def get_finished_jobs(self) -> Iterable[JobResult]:
        """Poll completed transfers."""
```

每个层级在构造时会获得一个指向共享主机区域的**直接 memoryview**。调用 `submit_store()` 时，层级直接从这个区域读取 KV 数据；调用 `submit_load()` 时，层级直接写入该区域。**无需中间拷贝或序列化**——层级直接在主层的内存上操作。

每个次级层级也独立管理自己的逐出策略。

一个完整的内存版参考实现位于 [`vllm/v1/kv_offload/tiering/example/`](https://github.com/vllm-project/vllm/tree/main/vllm/v1/kv_offload/tiering/example)。也支持树外（out-of-tree）次级层级——在层级配置中指定 `module_path`，vLLM 就会加载你自定义的 `SecondaryTierManager` 实现，而无需对 vLLM 本身做任何代码改动。

---

## 性能——扩展到更多用户

KV 缓存卸载的主要收益：通过从更廉价的层级重新加载 KV 数据，避免代价高昂的重复预填充。

并发会话较少时，所有缓存方法都能达到高吞吐量——加速器内存装得下所有内容。随着会话池的增长，各层级会先后出现容量限制：

- **约 64 个会话以内**——HBM 装得下工作集；所有缓存方法都表现良好。
- **64–128 个会话**——HBM 被填满；不使用卸载时吞吐量急剧下降。CPU 卸载能维持性能。
- **128 个会话以上**——CPU 缓存也被填满。存储卸载仍能保持高缓存命中率，吞吐量是其他方案的两倍以上。

![](https://vllm.ai/blog-assets/figures/tiered-kv-offloading/performance.svg)

存储的延迟高于 CPU 内存，因此达不到峰值吞吐量。但在大规模场景下，选择是在"命中基于存储的缓存"和"完整重新计算"之间——存储方案完胜。

**基准测试配置：**

- 模型：Qwen/Qwen3.6-35B-A3B，运行在 2× NVIDIA H100 上（TP=2）
- 存储层级：本地 NVMe 上的文件系统后端
- 工作负载：多轮对话，12K token 初始提示 + 每轮 4K token，共 8 轮
- 最大请求并发：64
- 仅测量预填充实例的吞吐量（预填充-解码分离部署）

完整的性能结果和复现脚本见 [neuralmagic/fs-offload-experiments](https://github.com/neuralmagic/fs-offload-experiments)。

---

## 致谢

我们感谢 Liran Schour、Chang Guo、Srinivas Krovvidi、Rotem Shavitt、Effi Ofer、Omer Paz、Kfir Toledo 和 Michal Malka 对分层 KV 缓存卸载框架设计与实现的贡献，也感谢所有贡献代码、评审和反馈的其他社区成员。
