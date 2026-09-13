---
title: "更上一层楼的推理：为什么你的单节点 vLLM 部署需要 Prefill-Decode 分离"
title_en: "Next-Level Inference: Why Your Single-Node vLLM Setup Needs Prefill-Decode Disaggregation"
source: https://vllm.ai/blog/2026-04-07-moriio-kv-connector
crawled: 2026-09-12
translated: 2026-09-13
---

# 更上一层楼的推理：为什么你的单节点 vLLM 部署需要 Prefill-Decode 分离

> 原文：[Next-Level Inference: Why Your Single-Node vLLM Setup Needs Prefill-Decode Disaggregation](https://vllm.ai/blog/2026-04-07-moriio-kv-connector) · vLLM 博客

AMD 与 Embedded LLM

[#分离部署](https://vllm.ai/blog/tags/disaggregation)

**TL;DR：** 预填充（Prefill）和解码（Decode）会争夺同一批 GPU，导致负载下逐 token 延迟（ITL）出现尖峰。我们展示了如何在一台 8 GPU 的 MI300X 节点上，使用 AMD 的 MORI-IO 连接器将两者分离部署——与相同 8 张 GPU 上的标准同置服务相比，实现 **2.5x 的 goodput 提升**，且 token 生成保持稳定。基准测试使用 Qwen3-235B-A22B-FP8，请求速率 8 req/s，提示长度 2000 token、输出长度 1000 token——完整配置见表 3 与[实验细节](#experimental-details)。

---

## 引言

在我们此前对 MoE 优化的探索 [[1]](#ref-1) 中，我们详细介绍了如何借助张量并行、流水线并行、数据并行和专家并行，将一个超大规模模型分布到一台 8 GPU 的 AMD Instinct MI300X 节点上。在本文中，我们将展示由 AMD 的 MORI-IO 所实现的 Prefill-Decode 分离部署如何解决这一瓶颈：无需多节点集群，即可交付更高的 goodput 和更可预测的性能。

你的 HBM 已被充分利用，算力负载均衡良好，vLLM 部署运行顺畅——直到你提高并发度。问题开始显现：逐 token 延迟（ITL）出现不可预测的尖峰。根本原因很简单——预填充和解码是本质上不同的工作负载，却在争夺相同的 GPU 资源。

**预填充是计算受限的**：它使用大型 GEMM 并行处理整个提示，成本随输入长度线性增长。

**解码是内存带宽受限的**：它一次生成一个 token，反复从 HBM 加载模型权重，而每字节对应的计算量相对较低。

当两个阶段共享同一实例时，它们会互相干扰。预填充请求可能阻塞数十条正在进行的解码流，造成明显的卡顿；而解码工作负载又会延迟新预填充请求的调度。结果就是一个两个阶段都既无法高效运行、也无法可预测运行的系统。

---

## 核心亮点

- **相同硬件上 2.5× 的 goodput 提升**。通过分离预填充与解码，在单台 8 GPU MI300X 节点上实现显著更高的满足 SLO 的吞吐量。
- **消除负载下的 ITL 尖峰**。专用解码 GPU 消除了预填充的干扰，确保 token 生成稳定、可预测。
- **单节点分离部署——无需集群**。完全在一台节点内实现 Prefill-Decode（PD）分离，释放未被利用的性能。
- **MORI-IO 实现快速 KV 缓存传输**。基于 RDMA 的 KV 数据搬运使两个阶段之间的高效交接成为可能。
- **灵活模式与各自权衡**。写模式性能最佳（TTFT 更低），读模式编排更简单——两者都远胜标准服务方式。

---

## 误区："分离部署只适用于数据中心集群"

当推理工程师听到"Prefill-Decode（PD）分离部署"时，脑海里浮现的往往是多节点数据中心方案——专用预填充节点、专用解码节点，以及将它们连接起来的 RDMA 网络。很自然的假设是："我只有一台 8 GPU 的节点——这跟我没关系。"

这种假设会让你错失可观的性能。PD 分离部署完全可以在一台 8 GPU 的系统内实现，而且如果你在乎满足严格的延迟 SLO，它往往就是正确的做法。

思路很直接：把两个阶段拆到各自的专用实例中。例如，四张 GPU 负责预填充，另外四张负责解码。每个实例随后可以独立地确定规模、并行度和调度方式，从而消除限制单体部署的队头阻塞。

难点在于交接。预填充期间生成的 KV 缓存必须传输到解码实例——这可能涉及数 GB 的数据。如果处理不当，传输本身会成为新的瓶颈，抵消分离部署的收益。

AMD 通过 **MORI-IO** 解决了这个问题：这是一个向 vLLM 贡献的基于 RDMA 的 KV 缓存连接器 [[4]](#ref-4)，构建在开源的 MORI（Modular RDMA Interface）[[5]](#ref-5) 框架之上。

> **范围说明：** 本文聚焦于单节点 PD 分离部署——在一台 8 GPU 的机器上部署，以提升现有硬件上的 goodput。

---

## 架构：采用 PD 分离部署的服务

拆分你的节点，意味着从单体部署转向一个由三个组件构成的轻量级微服务架构，如下面的表 1 所示。

| 组件 | 角色 |
| --- | --- |
| 预填充实例 | 处理输入提示并生成 KV 缓存（GPU 0–3） |
| 解码实例 | 使用传输过来的 KV 缓存逐个生成输出 token（GPU 4–7） |
| 代理服务器 | 客户端请求的入口；先路由到预填充，再到解码 |

总体而言，两种模式都是把 KV 缓存（预填充的输出）从预填充实例传输到解码实例，区别在于*由谁发起传输*以及*何时发起*：

- **读模式：** 代理等待预填充完成，然后把 KV 块的位置转发给解码。解码在开始生成之前通过 RDMA 拉取 KV 数据。
- **写模式：** 代理同时向预填充和解码分发请求。预填充每计算完一层，就把该层的 KV 数据直接推入解码的内存——因此预填充一完成，解码就可以立刻开始生成。

### 请求流程详解

MORI-IO 支持两种传输模式，区别在于**由谁发起 RDMA 传输**以及**代理如何编排两个阶段**。模式由 `VLLM_MORIIO_CONNECTOR_READ_MODE` 环境变量设定。

#### 读模式——解码拉取 KV 缓存

启用方式：`export VLLM_MORIIO_CONNECTOR_READ_MODE=1`

在读模式下，代理**串行**地向预填充和解码分发请求：它先等待预填充完成，提取远程块 ID，再把它们转发给解码。解码实例使用这些 ID 通过 RDMA 从预填充拉取 KV 缓存。请求流程见图 1。

![](https://vllm.ai/blog-assets/figures/2026-04-07-moriio-kv-connector/read-mode-request-flow-diagram.svg)
*图 1：读模式请求流程。代理串行分发——第 3 步（预填充响应）必须完成后才会进行第 4 步（向解码分发）。*

单个请求按时间排序的流程：

1. **客户端 → 代理**：客户端发送推理请求。
2. **代理 → 预填充**：代理将提示路由到预填充实例（`max_tokens=1`）。
3. **预填充 → 代理（响应）**：预填充返回 `remote_block_ids` 和 `remote_engine_id`，指明 KV 缓存所在的位置。
4. **代理 → 解码**：代理将请求转发给解码，附带远程块 ID。
5. **解码拉取 KV 缓存**（`WAITING_FOR_REMOTE_KVS`）：解码对预填充的内存发起 RDMA 读。在传输完成之前，调度器每一步都会跳过该请求。
6. **解码 → 预填充（清理）**：所有 KV 块传输完毕后，解码通知预填充释放其块。
7. **解码 → 代理 → 客户端**：生成的 token 通过 SSE 流式返回。

#### 写模式——预填充推送 KV 缓存（默认）

启用方式：不设置 `VLLM_MORIIO_CONNECTOR_READ_MODE`（或设为 `=0`）

在写模式下，代理**并发**地向预填充和解码分发请求——无需先等待预填充完成。预填充实例在逐层计算的过程中，把 KV 缓存逐层直接推入解码实例预先分配好的内存。请求流程见图 2。

![](https://vllm.ai/blog-assets/figures/2026-04-07-moriio-kv-connector/write-mode-request-flow-diagram.svg)
*图 2：写模式请求流程。代理同时向预填充和解码发起请求（第 2 步）；预填充通过 RDMA WRITE 逐层推送 KV（第 3 步），解码端等待。*

单个请求按时间排序的流程：

1. **客户端 → 代理**：客户端发送推理请求。
2. **代理 → 预填充 与 代理 → 解码（并发）**：代理并行发起两个请求。预填充请求携带解码的连接信息；解码请求携带预填充的连接信息。代理不阻塞等待预填充的响应。
3. **预填充推送 KV 缓存**：每计算完一层，`save_kv_layer` 就通过 RDMA 写直接写入解码实例预先分配的 KV 块内存。对于分块预填充（Chunked Prefill），各块会累积到最后一个块之后才发起写入。
4. **解码等待写完成**（`WAITING_FOR_REMOTE_KVS`）：解码调度器每一步轮询 `pop_finished_write_req_ids`，直到收到所有块。
5. **解码开始生成**：所有 KV 块到位后，解码立即把请求移入就绪队列，开始自回归生成。
6. **解码 → 代理 → 客户端**：生成的 token 通过 SSE 流式返回。

代理端的关键代码差异只是一个条件分支：

```
# examples/online_serving/disaggregated_serving/moriio_toy_proxy_server.py

if TRANSFER_TYPE == "READ":
    # Serial: wait for prefill to finish, extract block IDs for decode to pull.
    prefill_response = await send_prefill_task
    req_data["kv_transfer_params"]["remote_engine_id"] = prefill_response[
        "kv_transfer_params"
    ]["remote_engine_id"]
    req_data["kv_transfer_params"]["remote_block_ids"] = prefill_response[
        "kv_transfer_params"
    ]["remote_block_ids"]

# In WRITE mode, execution falls through here immediately —
# no await on send_prefill_task. Both phases are already in flight.
decode_request_task = asyncio.create_task(
    start_decode_request(decode_instance_endpoint["request_address"], req_data, request_id)
)
```

在读模式下，`remote_block_ids` 必须经由代理中转，因为解码需要知道该拉取预填充侧的哪些具体块。在写模式下，写入由预填充主导，直接推送到解码的地址——无需中转任何块 ID。

### 读模式 vs. 写模式：一图速览

在底层，MORI-IO（在 vLLM 中以 `MoRIIOConnector` 的形式暴露）负责管理 KV 缓存的交接。无论哪种传输模式，在实例对之间进行第一次 RDMA 传输之前，MORI-IO 都会通过 ZMQ 完成一次性的元数据交换——共享 KV 缓存基地址、块大小以及每层的张量步长。这个握手过程在后台线程中异步运行，因此不会阻塞引擎循环，随后建立的 RDMA 会话会被缓存下来供后续所有请求使用。

两种模式共享同样的握手与 RDMA 传输通道——差异完全体现在代理分发层和传输方向上。表 2 汇总了关键区别：

| 属性 | 读模式 | 写模式 |
| --- | --- | --- |
| `VLLM_MORIIO_CONNECTOR_READ_MODE` | `=1` | 不设置（或 `=0`） |
| RDMA 方向 | 解码从预填充拉取 | 预填充推送给解码 |
| 代理分发 | 串行（等待预填充 → 分发解码） | 并发（预填充与解码并行） |
| `remote_block_ids` 经代理中转 | 需要 | 不需要 |
| KV 清理信号 | 解码拉取完成后通知预填充释放块 | 预填充按请求跟踪写完成状态 |

---

## 结果：2.5x 的 goodput 提升

在深入配置细节之前，先看看分离部署实际能带来什么。

### 为什么用 goodput 而不是吞吐量

单纯的原始吞吐量具有误导性——一个系统可以在大多数用户悄悄违反延迟目标的情况下维持很高的请求速率。我们遵循 DistServe 的方法论 [[3]](#ref-3)，以 **goodput** 作为首要指标：

**Goodput** = 满足 TTFT < *T\_ttft* 且 ITL < *T\_itl* 的请求所对应的最大请求速率（req/s）。

这个指标把成本（每秒请求数）和服务质量（延迟 SLO 达标情况）浓缩在同一个数字里。我们的 SLO 目标是：**TTFT < 1 秒**、**ITL < 50 毫秒/token**。只有两个条件同时满足，请求才计入 goodput。

### 核心结果

**图 3** 展示了请求速率 = 8 时的 goodput：

| 指标 | 标准（1× TP8） | 标准（2× TP4） | MORI-IO 读模式（1P+1D） | MORI-IO 写模式（1P+1D） |
| --- | --- | --- | --- | --- |
| 同时满足两个 SLO 的请求数 | 26/100 | 30/100 | 70/100 | 73/100 |
| 主要失败模式 | ITL 尖峰（P99 ITL 远超 50 毫秒） | ITL 尖峰（双峰分布：约 30ms 与约 150ms） | 部分请求 TTFT 超过 1s | 部分请求 TTFT 超过 1s |
| 相对 goodput | 0.9x | 1x | 2.4x | 2.5x |

标准服务失败的原因是 ITL 集中在两个簇上——约 150ms 的高延迟簇远超 50ms 阈值。两种分离部署模式都完全消除了 ITL 违规；其剩余失败是在请求速率攀升时出现的 TTFT 超限。写模式略胜读模式（73 对 70），因为并发的代理分发降低了 TTFT，让更多请求保持在 1s 阈值以下。

TTFT 阈值：

1.00 s

ITL 阈值：

50 ms

*图 3：goodput 测量。每根柱代表一个请求——灰色柱表示至少违反一个 SLO 阈值。拖动滑块可探索不同的 SLO 目标。默认：TTFT < 1 s，ITL < 50 ms。*

### 不同请求速率下的 SLO 达标率

**图 4** 展示了请求速率从 0.5 到 10 的 SLO 达标率：

- **标准服务（1× TP8）**：从较低请求速率开始就出现 ITL 违规，并在所有测试速率下占据主导。在速率 = 8 时达到 26/100。
- **标准服务（2× TP4）**：急剧劣化——从速率 0.5 时的 100% 降到速率 1 时的约 60%，到速率 2 时崩塌至约 25% 并就此徘徊。ITL 违规很早就达到饱和。
- **MORI-IO 读模式（1P+1D）**：在速率约 5 之前保持 100% 达标率，随后随着 TTFT 开始超过阈值，逐渐下降至速率 10 时的约 44%。
- **MORI-IO 写模式（1P+1D）**：在速率约 5.5 之前保持 100% 达标率，随后随着 TTFT 开始超过阈值，逐渐下降至速率 10 时的约 46%。

![](https://vllm.ai/blog-assets/figures/2026-04-07-moriio-kv-connector/SLO-attainment.png)
*图 4：不同请求速率下的 SLO 达标率（同时满足 TTFT 与 ITL 目标的请求百分比）。在所有测试请求速率下，两种分离部署模式的 SLO 达标率都高于所有标准服务配置。*

---

## 理解权衡

### 为什么 ITL 会改善

在标准部署中，预填充和解码共享同一个 vLLM 引擎，并在每个批次内争夺调度。一次预填充——在一个前向传播中处理所有输入 token——耗时远长于一个解码步。同一批次中的每个解码请求都必须等这次预填充结束才能生成下一个 token，直接推高 ITL。

采用分离部署后，解码引擎*只*运行解码批次。没有计算密集的预填充任务打断其步调节奏，因此无论有多少新请求进入系统，ITL 都保持稳定、可预测。这一收益在读模式和写模式中完全相同——两种模式下解码引擎都与预填充隔离。

### 为什么 TTFT 会变差

硬币的另一面：分离部署给首 token 路径增加了开销。在标准服务中：

```
TTFT = queue + prefill_forward_pass + sample_T1 + detokenize + SSE_encode + network

```

在读模式下，会插入两个额外步骤（图 5）：

```
TTFT = queue(prefill) + prefill_forward_pass
     + [proxy serialization: await prefill, dispatch to decode]  <- Overhead 1
     + RDMA transfer (WAITING_FOR_REMOTE_KVS)                   <- Overhead 2
     + queue(decode) + sample_T1 + detokenize + SSE_encode + network

```

![](https://vllm.ai/blog-assets/figures/2026-04-07-moriio-kv-connector/read-mode-kv-transfer-sequence-diagram.svg)
*图 5：读模式时序。开销 1（代理串行化）与开销 2（RDMA READ）是 TTFT 的叠加项。*

在写模式下（图 6）：

```
TTFT ≈ max(
           queue(prefill) + prefill_forward_pass + RDMA_write_time,
           queue(decode)
       ) + sample_T1 + detokenize + SSE_encode + network

```

![](https://vllm.ai/blog-assets/figures/2026-04-07-moriio-kv-connector/write-mode-kv-transfer-sequence-diagram.svg)
*图 6：写模式时序。RDMA WRITE 与预填充计算重叠，因此开销 2 不会累加到实际 TTFT 上。*

写模式消除了开销 1。由于代理并发地向两个实例分发请求，解码队列等待与预填充计算相互重叠。剩下的成本——RDMA 传输本身——在结构上等同于读模式中的 RDMA 读。

#### 开销 1：代理串行化（仅读模式）

在读模式下，代理要等待完整的预填充响应才能向解码分发。这会把整个预填充计算时间加上一次代理往返计入客户端可见的 TTFT。在写模式下，这一段被跳过——解码请求在预填充结束前就已经在途。

```
# examples/online_serving/disaggregated_serving/moriio_toy_proxy_server.py

if TRANSFER_TYPE == "READ":
    # In read mode, prefill and decode are executed serially.
    prefill_response = await send_prefill_task
    req_data["kv_transfer_params"]["remote_engine_id"] = prefill_response[
        "kv_transfer_params"
    ]["remote_engine_id"]
    req_data["kv_transfer_params"]["remote_block_ids"] = prefill_response[
        "kv_transfer_params"
    ]["remote_block_ids"]
```

#### 开销 2：RDMA 传输等待

解码实例收到请求后进入 `WAITING_FOR_REMOTE_KVS` 状态。调度器每一步都会跳过该请求，直到 RDMA 传输完成，然后立即把它移入就绪队列等待调度。

```
# vllm/v1/request.py

WAITING_FOR_REMOTE_KVS = enum.auto()

# vllm/v1/core/sched/scheduler.py
# KVTransfer: skip request if still waiting for remote kvs.

if request.status == RequestStatus.WAITING_FOR_REMOTE_KVS:
    is_ready = self._update_waiting_for_remote_kv(request)
    if is_ready:
        request.status = RequestStatus.WAITING
    else:
        logger.debug("%s is still in WAITING_FOR_REMOTE_KVS state.",
                     request.request_id)
        self.waiting.pop_request()
        skipped_waiting_requests.prepend_request(request)
        continue
```

在读模式下，这一等待在预填充已经完成之后才开始。在写模式下，这一等待在解码请求到达时立即开始——与另一实例上正在进行的预填充计算重叠。

**结论：** 分离部署用更长的首 token 等待时间换取稳定、可预测的 ITL。会长多少取决于模式。在读模式下，TTFT 至少增加一次完整的预填充前向传播（代理串行化）加上 RDMA 传输时间。在写模式下，代理串行化被消除——TTFT 只增加 RDMA 传输时间，而它又与预填充计算重叠，因此净代价更小。无论哪种模式，ITL 的收益完全一致。

### 什么时候应该用它？

表 4 总结了何时应选择哪种部署方式。

| 你的情况 | 建议 |
| --- | --- |
| 生产负载下 ITL p99 超出你的 SLO | 分离部署——这是首要使用场景 |
| TTFT 是你的硬性约束（如聊天机器人 UX） | 标准服务可能更合适 |
| 高并发且提示很长 | 分离部署——预填充干扰在这里最严重 |
| 低请求速率且提示较短 | 标准服务足够 |

---

## 如何搭建

看完结果，下面讲如何部署。你需要配置三个组件：一个预填充实例、一个解码实例和一个代理服务器。vLLM 分离式预填充的完整文档见 [[2]](#ref-2)。

### 预填充实例

预填充实例充当 KV 生产者（`kv_role: kv_producer`）。它处理输入提示、计算 KV 缓存，并使其可供解码实例通过 RDMA 读取。

```
vllm serve <model> \
  ...
  --gpu_memory_utilization 0.9 \
  --kv-transfer-config '{
    "kv_connector": "MoRIIOConnector",
    "kv_role": "kv_producer",
    "kv_connector_extra_config": {
      "proxy_ip": "127.0.0.1",
      "proxy_ping_port": "36367",
      "http_port": "20005",
      "handshake_port": "6301",
      "notify_port": "6105"
    }
  }'
```

启动时，实例会通过 ZMQ 向代理注册自身，发送自己的角色、HTTP 地址、握手与通知端口以及并行配置。它会持续周期性发送注册消息，以便代理能够检测其是否可用。

### 解码实例

解码实例充当 KV 消费者（`kv_role: kv_consumer`）。它在预填充完成后接收来自代理的请求，然后通过 RDMA 拉取 KV 缓存。

```
vllm serve <model> \
  ...
  --gpu_memory_utilization 0.9 \
  --kv-transfer-config '{
    "kv_connector": "MoRIIOConnector",
    "kv_role": "kv_consumer",
    "kv_connector_extra_config": {
      "proxy_ip": "127.0.0.1",
      "proxy_ping_port": "36367",
      "http_port": "40005",
      "handshake_port": "7301",
      "notify_port": "7501"
    }
  }'
```

### 代理服务器

代理是一个轻量级 HTTP 服务器，负责编排两阶段流程。它通过 ZMQ 在 `proxy_ping_port` 上监听实例注册，并使用轮询（round-robin）调度路由每个请求。

```
python examples/online_serving/disaggregated_serving/moriio_toy_proxy_server.py
```

在 READ 模式下，代理等待预填充实例完成，从响应中提取 `remote_block_ids`，并将其传递给解码实例，让它确切知道该拉取哪些 KV 块。

### 端口参考

每个实例使用若干端口进行不同的通信，汇总见表 5。各 rank 的端口偏移在 `MoRIIOConfig` 中应用（见 `moriio_common.py`）：

| 端口 | 用途 |
| --- | --- |
| `proxy_ping_port` | 各实例向代理注册的 ZMQ 端点 |
| `http_port` | vLLM HTTP 服务器端口；代理把推理请求转发到这里 |
| `handshake_port` | 一次性元数据交换：消费者获取生产者的 KV 缓存布局 |
| `notify_port` | 按请求同步：KV 块就绪时预填充向解码发信号 |

---

## 实验细节

### 环境配置

该环境可以通过提供的 Dockerfile 构建复现——`Dockerfile.rocm_base`（使用 [ROCm/mori](https://github.com/ROCm/mori) 的 MORI commit `2d02c6a9`）和 `Dockerfile.rocm`（使用 [vllm-project/vllm](https://github.com/vllm-project/vllm) 的 vLLM main 分支）。

**硬件：**

- GPU：8× AMD Instinct MI300X GPU（gfx942）
- CPU：2× AMD EPYC 9654 96 核处理器

**软件栈：**

- ROCm 驱动：6.10.5（AMDGPU）
- 容器：rocm/vllm-dev（ROCm 7.0.51831-a3e329ad8）
- vLLM：0.16.0rc1.dev1+gc46b0cd0a（git sha: c46b0cd0a）
- PyTorch：2.9.1+git8907517（ROCm 7.0.51831-a3e329ad8）
- MORI 库：commit [`c365eaed`](https://github.com/ROCm/mori/commit/c365eaed02b13e6b8f2e9c8215b21516d86856ce)

**基准测试配置：**

- 模型：Qwen/Qwen3-235B-A22B-FP8
- 输入序列长度：2000 token
- 输出序列长度：1000 token
- 数据集：random
- 工作负载：共 100 个请求
- 请求速率：0.5 到 10（步长 0.5）

### 基线配置

本文比较的四种配置见表 6。

| 配置 | 描述 |
| --- | --- |
| 标准（1× TP8） | 单个 vLLM 实例使用全部 8× MI300X GPU（TP=8）并启用专家并行。在同一引擎上处理混合的预填充与解码工作负载。 |
| 标准（2× TP4） | 两个相同的 vLLM 实例，各使用 4× MI300X GPU（TP=4）并启用专家并行。轮询代理均匀分发请求。两个实例都处理混合的预填充与解码工作负载。 |
| MORI-IO 读模式（1P+1D） | 一个预填充实例（GPU 0–3）和一个解码实例（GPU 4–7），各为 TP=4 并启用专家并行。两个实例均设置 `VLLM_MORIIO_CONNECTOR_READ_MODE=1`。代理串行分发：等待预填充返回 `remote_block_ids`，再转发给解码。解码通过 RDMA 拉取 KV 缓存。禁用前缀缓存。 |
| MORI-IO 写模式（1P+1D） | 一个预填充实例（GPU 0–3）和一个解码实例（GPU 4–7），各为 TP=4 并启用专家并行。KV 缓存通过 MORI-IO 以写模式传输。有状态代理编排两阶段路由。按 MORI-IO 连接器的要求禁用前缀缓存。 |

> **为什么选这个基线？** 标准（2× TP4）与分离部署配置使用相同的 GPU 总数（8× MI300X），都拆成两个 4 GPU 组，确保公平的同口径比较。唯一区别是每个组运行混合的预填充+解码工作负载（标准），还是专用的预填充或解码工作负载（分离）。标准（1× TP8）作为额外参考点纳入，即把全部 8 张 GPU 用于单个引擎。

**普适性说明：** 这些结果基于混合专家（MoE）模型（Qwen3-235B-A22B-FP8）。预填充/解码的干扰模式是 Transformer 推理的固有问题，同样适用于稠密模型。MoE 模型往往会放大这种效应，因为专家路由增加了每步计算量的波动，使 ITL 抖动更加明显。

---

## 结论与展望

本文证明了 PD 分离部署并非只是数据中心级别的技术——它在单台 8 GPU 节点上就能带来可衡量的收益。通过为每个阶段分配专用 GPU，并使用 MORI-IO 进行高效的基于 RDMA 的 KV 缓存传输，我们实现了 2.5× 的 goodput 提升，并消除了困扰同置部署的 ITL 违规。

### 下一步

- **多节点部署：** 在生产环境中，预填充和解码实例可以跨越多个节点——MORI-IO 本来就走网络 fabric 上的 RDMA，因此同一连接器无需改动代码即可跨主机工作。
- **按阶段调优：** 有了专用实例，预填充实例可以配置为高计算吞吐（更大的 token 预算、分块预填充），而解码实例则为低延迟调优（更小的批大小、更严格的调度）。这种各自独立旋钮式的调优在同置部署中是不可能实现的。

---

## 附录：可复现配置

要复现这些结果，可以使用 [rocm/vllm-dev](https://hub.docker.com/r/rocm/vllm-dev) 提供的预构建 nightly 镜像，或使用 vLLM 仓库中的 `Dockerfile.rocm_base` 与 `Dockerfile.rocm` 从源码构建（MORI commit [2d02c6a9](https://github.com/ROCm/mori/commit/2d02c6a9)，vLLM commit [c46b0cd0a](https://github.com/vllm-project/vllm/commit/c46b0cd0a)）。

下面给出所有基准测试完整的 vLLM 命令行配置。每条命令都包含在 AMD Instinct MI300X GPU 上运行 Qwen3-235B-A22B-FP8 所需的环境变量、并行标志与部署参数。

### 标准服务

```
# Instance 1 (GPU 0-3)
CUDA_VISIBLE_DEVICES=0,1,2,3 VLLM_ROCM_USE_AITER=1 vllm serve Qwen/Qwen3-235B-A22B-FP8 \
  -tp 4 \
  --enable-expert-parallel \
  --max-model-len 16384 \
  --max-num-batched-tokens 8192 \
  --distributed-executor-backend mp \
  --no-enable-prefix-caching \
  --port 8100

# Instance 2 (GPU 4-7)
CUDA_VISIBLE_DEVICES=4,5,6,7 VLLM_ROCM_USE_AITER=1 vllm serve Qwen/Qwen3-235B-A22B-FP8 \
  -tp 4 \
  --enable-expert-parallel \
  --max-model-len 16384 \
  --max-num-batched-tokens 8192 \
  --distributed-executor-backend mp \
  --no-enable-prefix-caching \
  --port 8200

# Proxy
cd <path_to>/vllm
python benchmarks/disagg_benchmarks/round_robin_proxy.py
```

### 分离式服务

```
# Prefill instance (GPU 0-3)
export VLLM_MORIIO_CONNECTOR_READ_MODE=1    # unset for write mode
export VLLM_ROCM_USE_AITER=1
export CUDA_VISIBLE_DEVICES=0,1,2,3
export HIP_VISIBLE_DEVICES=0,1,2,3
export MORI_DISABLE_AUTO_XGMI=1
export MORI_IO_ENABLE_NOTIFICATION=0

vllm serve Qwen/Qwen3-235B-A22B-FP8 \
  -tp 4 \
  --enable-expert-parallel \
  --port 20005 \
  --max-num-batched-tokens 4096 \
  --distributed-executor-backend mp \
  --gpu_memory_utilization 0.9 \
  --max-model-len 16384 \
  --max_num_seqs 64 \
  --no-enable-prefix-caching \
  --kv-transfer-config '{
    "kv_connector": "MoRIIOConnector",
    "kv_role": "kv_producer",
    "kv_connector_extra_config": {
      "proxy_ip": "127.0.0.1",
      "proxy_ping_port": "36367",
      "http_port": "20005",
      "handshake_port": "6301",
      "notify_port": "6105"
    }
  }'

# Decode instance (GPU 4-7)
export VLLM_MORIIO_CONNECTOR_READ_MODE=1    # unset for write mode
export VLLM_ROCM_USE_AITER=1
export CUDA_VISIBLE_DEVICES=4,5,6,7
export HIP_VISIBLE_DEVICES=4,5,6,7
export MORI_DISABLE_AUTO_XGMI=1
export MORI_IO_ENABLE_NOTIFICATION=0

vllm serve Qwen/Qwen3-235B-A22B-FP8 \
  -tp 4 \
  --enable-expert-parallel \
  --port 40005 \
  --no-enable-prefix-caching \
  --max-num-batched-tokens 4096 \
  --distributed-executor-backend mp \
  --gpu_memory_utilization 0.9 \
  --max-model-len 16384 \
  --max_num_seqs 64 \
  --kv-transfer-config '{
    "kv_connector": "MoRIIOConnector",
    "kv_role": "kv_consumer",
    "kv_connector_extra_config": {
      "proxy_ip": "127.0.0.1",
      "http_port": "40005",
      "proxy_ping_port": "36367",
      "handshake_port": "7301",
      "notify_port": "7501"
    }
  }'

# Proxy
cd <path_to>/vllm
python examples/online_serving/disaggregated_serving/moriio_toy_proxy_server.py
```

## 致谢

我们要感谢为这次合作做出贡献的众多优秀同事：

**AMD：** Hongxia Yang、Gilbert Lei、Mingzhi Liu、Niko Ma、Tian Di、Randall Smith、Feiyue Zhai、Peng Sun 以及 MORI 团队。

**Embedded LLM：** Pin Siang Tan、Jun Kang Chow、Ye Hur Cheong、Vensen Mu、Jeff Aw、Tun Jian Tan 以及 Embedded LLM 团队。

## 参考文献

1. AMD and Embedded LLM, "The vLLM MoE Playbook: A Practical Guide to TP, DP, PP and Expert Parallelism" <https://rocm.blogs.amd.com/software-tools-optimization/vllm-moe-guide/README.html>
2. vLLM Disaggregated Prefill Documentation <https://docs.vllm.ai/en/latest/features/disagg_prefill/>
3. DistServe: Maximizing Goodput in LLM Serving <https://haoailab.com/blogs/distserve/>
4. MORI-IO Connector PR #29304 <https://github.com/vllm-project/vllm/pull/29304>
5. MORI (Modular RDMA Interface) <https://github.com/ROCm/mori>

---

## 免责声明

测试时间为 2026 年 3 月 12 日，测量 AMD Instinct MI300X 平台上的推理 goodput。

**硬件配置**

- MI300X：AMD EPYC 9654 96 核处理器服务器，配备 8× AMD Instinct MI300X（192GB，750W）GPU，NPS1（每个 socket 1 个 NUMA），2.2TiB（24 根 DIMM，4800 MT/s 内存，96 GiB/DIMM）

**软件配置**

Ubuntu 22.04 LTS，Linux 内核 5.15.0-153-generic，ROCm 驱动 6.10.5（AMDGPU），ROCm 7.0.51831-a3e329ad8，PyTorch 2.9.1+git8907517，vLLM 0.16.0rc1.dev1+gc46b0cd0a，MORI 库 commit c365eaed

服务器厂商的配置可能有所不同，从而产生不同结果。性能可能因配置、软件、vLLM 版本以及是否使用最新驱动和优化而异。

---
