---
title: "分布式逐层卸载：在 vLLM-Omni 中高效扩展 200B+ DiT 模型"
title_en: "Distributed Layerwise Offload: Scaling Toward 200B+ DiT Models Efficiently in vLLM-Omni"
source: https://vllm.ai/blog/2026-08-17-distributed-layerwise-offload
crawled: 2026-09-12
translated: 2026-09-13
---

# 分布式逐层卸载：在 vLLM-Omni 中高效扩展 200B+ DiT 模型

> 原文：[Distributed Layerwise Offload: Scaling Toward 200B+ DiT Models Efficiently in vLLM-Omni](https://vllm.ai/blog/2026-08-17-distributed-layerwise-offload) · vLLM 博客

作者：vLLM-Omni 扩散模型团队

[#性能](https://vllm.ai/blog/tags/performance)[#分布式](https://vllm.ai/blog/tags/distributed)[#vllm-omni](https://vllm.ai/blog/tags/vllm-omni)[#cosmos3](https://vllm.ai/blog/tags/cosmos3)

## TL;DR

**开箱即用版本：** 对于下文 DLO + AllGather 快速上手，请使用 vLLM `0.27.0` 搭配 vLLM-Omni `v0.27.0rc1`。

vLLM-Omni 的分布式逐层卸载（Distributed Layerwise Offload）使超过单卡 HBM 容量的视频生成模型（例如 Cosmos3-Super 64B / 124 GB）能够以极小的主机内存开销运行在多张 NPU 或 GPU 上。该技术栈包括：

- **Meta 设备初始化 + mmap 权重加载**：权重以 mmap 视图加载，指向共享的操作系统页缓存，消除了模型创建过程中的 O(dp\_size × model\_size) RSS。冷启动 cgroup 可见峰值下降 73%（Cosmos3-Nano DP4 由 178 GB 降至 47 GB）。
- **权重分片 + AllGather**：每个 rank 只存储模型的 1/dp\_size。完整层权重在运行时通过 AllGather 重建，并与计算在专用流上重叠进行。
- **固定双缓冲方案**：任意时刻每台设备上恰好驻留 2 层权重，与总层数无关。缓冲容量仍随模型的最大块增长，且总 HBM 还包含依赖工作负载的激活与通信缓冲。在实测的 720p 10s 工作负载中，峰值 HBM 从 17B 模型到 64B 模型增长约 22%（23.1 → 28.1 GB）；空闲 HBM 增长约 27%（11.5 → 14.6 GB）。
- **DP 多并发**：每个 DP rank 并行处理不同的请求，相对单请求 HSDP 达到 3.3× 吞吐量——约为理想 4× 扩展的 83%。
- **平台无关**：通过 vLLM-Omni 的平台抽象层，可同时运行于 NVIDIA GPU（CUDA/NCCL）与昇腾 NPU（CANN/HCCL）。
- **8× B300 上的拓扑感知**：在评估的三条 MiniMax-H3 路线中，AllGather 最适合 DP1×SP8 的延迟与 DP4×SP2 的平衡点，而 rank-local DLO 在 DP8×SP1 上胜出，达到 183.78 视频/小时和 43.97 Wh/视频。

在实测的昇腾 910B3 DLO+AllGather 运行（Cosmos3-Nano 33 GB 与 Cosmos3-Super 124 GB）中，所有配置都产生了正确的视频输出，且 cgroup 可见的主机内存按 O(model\_size + dp\_size × constant) 扩展，而非 O(dp\_size × model\_size)。在纯 DP 配置下，无 AllGather 模式每个 rank 仍保留一份完整主机副本，而既有的 TP 分片本身已是 rank-local，按原样复用；CUDA 进程内存统计包含锁页分片，在下文单独报告。

## 快速上手

> **版本要求。** 下面两条 AllGather 命令要求 vLLM-Omni `v0.27.0rc1` 或更高版本，搭配 vLLM `0.27.0`。在 `v0.26.0` 发行版上，Cosmos3 DLO+DP 路径会拒绝所有请求，因为引擎在多请求准入时要求 `supports_request_batch=True`，而 `Cosmos3OmniDiffusersPipeline` 并未声明该属性（[#5953](https://github.com/vllm-project/vllm-omni/issues/5953)）。[#5864](https://github.com/vllm-project/vllm-omni/pull/5864) 通过对 DLO+AllGather+DP 配置绕过 `supports_request_batch` 要求来修复此问题：每个 DP rank 通过流水线的单请求前向路径独立运行自己的请求，引擎从各 rank 的队列收集结果。无 AllGather 的 DP 命令不在 #5864 的覆盖范围内；`--dlo-no-use-allgather` 的独立请求分发在 [#5911](https://github.com/vllm-project/vllm-omni/pull/5911) 中跟踪（仍处于打开状态）。#5864 中的正确性修复不改变 DLO 的权重分片或卸载内存机制；下文每个测量章节都会报告各自的环境。

```
# 4× NPU or GPU — Cosmos3-Nano with DP=4
vllm serve /path/to/Cosmos3-Nano --omni \
    --enable-distributed-layerwise-offload \
    --data-parallel-size 4

# 2× devices — Cosmos3-Super (124 GB) with DP=2
vllm serve /path/to/Cosmos3-Super --omni \
    --enable-distributed-layerwise-offload \
    --data-parallel-size 2

# Disable AllGather (each rank loads full weights, no sharding)
vllm serve /path/to/Cosmos3-Nano --omni \
    --enable-distributed-layerwise-offload \
    --data-parallel-size 4 \
    --dlo-no-use-allgather
```

`--dlo-use-allgather` / `--dlo-no-use-allgather` 标志控制权重是否分片（默认：分片）。禁用时，每个 rank 加载标准加载器的 rank-local 张量——在纯 DP 配置下这是一份完整模型副本，而既有 TP 分片已是 rank-local，按原样复用。当 AllGather 同步开销超过内存节省时，该模式很有用。

## 问题：大型扩散模型与 HBM 及主机内存的矛盾

Cosmos3-Super（64B 参数，BF16 下 124 GB）无法装进单张 64 GB HBM 设备。现有方案分为两大类——**卸载器**（从主机内存流式读取权重）与**并行**（把驻留工作分片到多台设备）——但各有局限：

![Why Distributed Layerwise Offload is needed](https://vllm.ai/blog-assets/figures/2026-07-30-distributed-layerwise-offload/dlo-problem-overview.svg)

为什么需要分布式逐层卸载

*图 1：Cosmos3-Super 的卸载器与并行替代方案。HSDP 每卡使用约 31 GB 权重，外加约 25 GB 激活与通信缓冲（合计约 56 GB），只留下 8 GB 余量；DLO 在 HBM 中只保留两层，同时对主机权重分片。*

| 方案 | 设备 HBM | 每 rank 主机内存 | 局限 |
| --- | --- | --- | --- |
| HSDP (FSDP2) | model / N | 0 | HBM 装满：64B → 56 GB/卡（8 GB 余量） |
| 逐层卸载（纯 DP） | 仅 2 层 | 完整模型 | N × model\_size 主机内存（4 × 124 GB = 496 GB） |
| 张量并行 | model / N | 0 | 激活值缩放有帮助，但有通信开销 |
| 分布式逐层卸载（本文） | 仅 2 层 | model / N | 需要 AllGather 同步 |

对于纯 DP 部署，主机内存瓶颈是致命的：传统逐层卸载会在每个 rank 的主机内存中存放一份完整模型副本。4 台设备就是 4 × 124 GB = 496 GB——超过大多数服务器的内存容量。TP 部署可能已经在使用 rank-local 分片，从而按比例降低每 rank 的主机内存。

更糟的是，模型加载期间每个 rank 会独立调用 `param.data.copy_(loaded_weight)`，在 RSS 中创建 dp\_size 份完整的私有副本。RSS 峰值按 O(dp\_size × model\_size) 扩展，对 200B 模型且 dp\_size=4 时可达 2 TB。

## 方案概览

分布式逐层卸载通过四项相互配合的技术，同时解决 HBM 与主机内存瓶颈：

| 技术 | 解决的问题 | 主要收益 |
| --- | --- | --- |
| Meta 设备 + mmap | 加载期间 O(dp\_size × model) 的 RSS | 冷启动 cgroup 可见峰值 -73% |
| 权重分片 + AllGather | N × model\_size 主机内存 | 总计 1× model\_size（共享页缓存） |
| 双缓冲预取 | 全部权重驻留设备 | 任意时刻 HBM 上仅 2 层 |
| DP 多并发 | 串行请求处理 | 通过 N 个并行请求获得 3.3× 吞吐量 |

前三项技术使大模型服务在内存上可行；DP 多并发是一项吞吐量优化，建立在技术 2 已经需要的 AllGather 同步之上。下文按我们实现它们的顺序逐一展开，并回答三个问题：为什么存在这个问题、为什么有效、你能得到什么。

## 1. Meta 设备 + mmap 权重加载

**为什么。** 原来的加载路径让每个 rank 在 `offload_backend.enable()` 之前独立调用 `load_model(load_device="cpu")`。这导致 `param.data.copy_(loaded_weight)` 在 RSS 中创建 dp\_size 份完整的模型私有副本。对于 Cosmos3-Nano DP4，cgroup 可见峰值为 178 GB——尽管模型本身只有 33 GB。

**为什么有效。** 卸载器用 `to_empty(device="meta")` 把已创建的 DiT 模块转换到 meta 设备，在保留张量元数据的同时释放其参数存储。然后用来自 `safe_open().get_tensor()` 的 mmap 视图替换这些 meta 参数，这些视图指向操作系统页缓存而非私有副本。

```
# distributed_layerwise_backend.py — release existing DiT parameter storage
dit_module.to_empty(device="meta")

# Resolve an HF repo ID, then replace meta parameters with mmap views
model_path = download_weights_from_hf(...)
tensor = safe_open(file_path, framework="pt", device="cpu").get_tensor(ckpt_key)
parent._parameters[name] = Parameter(tensor)  # points to shared page cache
```

由于所有 rank mmap 的是同一批 safetensors 文件，操作系统会在页缓存中为每个文件页只维护一份拷贝——在所有进程间共享。没有任何 rank 会创建私有副本。

对于 Hugging Face 仓库 ID（而非本地路径），我们先用 `download_weights_from_hf()` 解析出快照路径，与 vLLM 现有 DiffusersPipelineLoader 使用的模式一致。

**你能得到什么。** 对于 Cosmos3-Nano DP4，冷启动 cgroup 可见峰值从 178 GB 降至 47 GB——降幅 73%。178 GB 基线由 132 GB 私有模型副本、33 GB 共享页缓存以及约 13 GB 框架/瞬时开销组成。mmap 页缓存（1× model\_size）是共享且只读的，在内存压力下操作系统可以部分回收。

![Meta-device and mmap loading memory comparison](https://vllm.ai/blog-assets/figures/2026-07-30-distributed-layerwise-offload/mmap-loading-memory.svg)

Meta 设备与 mmap 加载的内存对比

*图 2：实测 Cosmos3-Nano DP4 冷启动峰值从 178 GB 降至 47 GB，方法是用一份共享 mmap 页缓存支撑的 meta 参数替换四份私有权重副本。*

## 2. 权重分片与 AllGather 重建

**为什么。** 即使采用 mmap 加载，逐层卸载机制仍会把完整模型复制进每个 rank 的锁页 CPU 内存以供 H2D 传输。在本文实测的纯 DP 基线中，4 台设备意味着 4 × 33 GB = 132 GB 锁页内存——而且随设备数线性增长。

**为什么有效。** 每个 rank 不再存储完整模型，只存储权重的 1/dp\_size。运行时，完整层权重通过 `all_gather_into_tensor` 在专用通信流上重建。

```
# _shard_and_pin: each rank stores only its 1/dp_size shard
shard_size = (total_numel + dp_size - 1) // dp_size  # ceil division
shard = torch.zeros(shard_size, dtype=dtype, device="cpu")
# Copy only the portion within [rank * shard_size, (rank+1) * shard_size)
shard[dst_slice].copy_(mmap_view.flatten()[src_slice])
shard = shard.pin_memory()  # DMA buffer for fast H2D
```

分片采用向上取整除法并做零填充，因此所有分片大小相等——这是 `all_gather_into_tensor` 的要求。分片完成后，原始 mmap 视图被替换为零元素占位符，释放页缓存引用。

**你能得到什么。** 锁页内存总量从 dp\_size × model\_size 降至 model\_size（所有 rank 之和）。对于 Cosmos3-Super DP4：4 × 124 GB → 总计 124 GB，每 rank 31 GB。

![Weight sharding and AllGather reconstruction](https://vllm.ai/blog-assets/figures/2026-07-30-distributed-layerwise-offload/weight-sharding-allgather.svg)

权重分片与 AllGather 重建

*图 3：驻留主机的权重从每个 rank 一份完整模型缩减为每个 rank 一个分片；AllGather 只在每台设备上重建当前的完整层。*

## 3. H2D 与 AllGather 重叠的双缓冲预取

**为什么。** 分片解决了内存问题，但每个层在计算期间仍需要其完整权重驻留设备。如果一次性加载所有层，HBM 会装满——最初的问题又回来了。同步加载（H2D → 等待 → AllGather → 等待 → 计算）还会浪费时间：数据搬运期间 GPU 闲置。

**为什么有效。** 我们恰好维护两个设备缓冲（槽位），每个按模型中最大块的尺寸分配。当计算流执行第 N 层（使用槽位 0）时，后台流把第 N+1 层准备进槽位 1：

![DLO Double-Buffer Prefetch Pipeline](https://vllm.ai/blog-assets/figures/2026-07-30-distributed-layerwise-offload/dlo_pipeline_last_frame.png)

DLO 双缓冲预取流水线

*图：完整的三流时间线，Compute（蓝）、H2D（橙）与 AllGather（绿）通过双缓冲槽位重叠。红色虚线箭头表示事件同步——计算流在切换槽位前等待 AllGather 完成。*

点击播放动画
![DLO Double-Buffer Prefetch Pipeline Animation](https://vllm.ai/blog-assets/figures/2026-07-30-distributed-layerwise-offload/dlo_pipeline.gif)

DLO 双缓冲预取流水线动画

两阶段准备在独立的流上运行：

1. **H2D**（`copy_stream`）：把 1/dp\_size 分片从锁页 CPU 加载到设备
2. **AllGather**（`comm_stream`）：把所有 rank 的分片汇聚到完整权重缓冲

两条流都通过基于事件的同步与计算流重叠。AllGather 完成后，使用缓存的元数据把参数重新指向输出缓冲的切片。

缓冲在所有块之间共享——按最大块尺寸一次性分配，每层复用。这确保 HBM 用量以 2 × max\_block\_size 为界，与总层数无关。

在昇腾 NPU 上，`pin_memory()` 通过 `/dev/davinci_manager`（NPU 设备驱动）分配支持 DMA 的内存。该内存驻留在 CPU 内核空间，cgroup 不跟踪它——这是解释 cgroup 峰值远低于预期的关键发现。

**你能得到什么。** HBM 只承载 2 层权重（Nano 约 2 GB，Super 约 3 GB），与总层数无关。所需缓冲容量仍随最大块增长，而总 HBM 还包含依赖工作负载的激活与通信缓冲。在实测的 `dist_offload+SP` 720p 10s 工作负载中，峰值 HBM 从 Nano 到 Super 增长约 22%（23.1 → 28.1 GB）；空闲 HBM 增长约 27%（11.5 → 14.6 GB）。模型大了 3.8 倍，但两项 HBM 测量值仍远低于 64 GB。

![HBM usage for Cosmos3-Nano and Cosmos3-Super](https://vllm.ai/blog-assets/figures/2026-07-30-distributed-layerwise-offload/hbm-nano-vs-super.svg)

Cosmos3-Nano 与 Cosmos3-Super 的 HBM 用量

*图 4：720p 10s 下实测 `dist_offload+SP` 的 HBM。峰值 HBM 从 23.1 GB 升至 28.1 GB，约增长 22%，而模型大 3.8 倍；HSDP+SP 在 Super 上达到 56.3 GB。*

## 4. DP 多并发：N 个请求并行

**为什么。** AllGather 只汇聚权重分片——它完全不依赖于请求。这意味着所有 DP rank 在每次 AllGather 调用处同步，但可以并行计算不同的激活值（不同请求）。若不利用这一点，DP rank 会在 AllGather 调用之间闲置，吞吐量被限制为一次 1 个请求。

**为什么有效。** 启用 `dp_concurrent` 后，调度器把最多 dp\_size 个请求打包在一起。执行器通过单次广播 RPC 发送所有请求：

![DP multi-concurrency request flow](https://vllm.ai/blog-assets/figures/2026-07-30-distributed-layerwise-offload/dp-multi-concurrency.svg)

DP 多并发请求流程

*图 5：单次广播携带一个请求列表；每个 DP rank 计算不同的请求，同时同步的 AllGather 调用交换与请求无关的权重分片。*

```
# Executor: send all requests at once
reqs_list = [nr.req for nr in new_reqs]
results = collective_rpc("execute_model", args=(reqs_list, ...),
                         unique_reply_rank=None, exec_all_ranks=True)
```

每个 worker 根据自己的 DP rank（而非全局 rank，以便正确处理 SP/TP）选择一个请求：

```
dp_rank = get_data_parallel_rank()
req = reqs_list[dp_rank % len(reqs_list)]
```

每个 DP 副本内只有主 rank（SP=0、TP=0、CFG=0、PP=0）回复，并带上 `dp_rank` 标签用于结果匹配。执行器通过轮询收集响应，并按 `dp_rank` 排序以把结果匹配到请求。

一个校验步骤会拒绝批兼容键不同的并发请求。该键涵盖空间/时间形状（`height`、`width`、`num_frames`、`fps`）、CFG/引导设置（`guidance_scale`、`true_cfg_scale`、`cfg_normalize`）、`num_inference_steps`、LoRA 身份（`lora_int_id`、`lora_scale`）、输出数量、质量模式以及流水线特有的 `extra_args`——因为 AllGather 是集合操作，这些共享字段中的任何不一致都会导致一个 rank 分岔而其他 rank 挂起。`extra_args` 尤其可能改变前向调度，因此引擎要求它在一个 wave 内 JSON 完全一致。种子与生成器等请求本地字段可以因 rank 而异。自 [#5864](https://github.com/vllm-project/vllm-omni/pull/5864) 起，流水线无需声明 `supports_request_batch=True`；引擎通过流水线的单请求前向路径独立运行每个 DP rank 的请求，并从各 rank 的结果队列收集结果。不兼容或空提示的 wave 会在 worker 分发之前被拒绝，部分 wave 超时会快速失败（fail closed），而不是让集合操作死锁。

**你能得到什么。** 4 个并发请求达到 3.22 生成视频帧/秒——是 HSDP 单请求基线的 3.3 倍，约为理想 4× 扩展的 83%。固定的 AllGather 开销（约 150 ms/步）被摊销到 4 个并发计算上。

## 昇腾内存核算：cgroup 可见内存与物理内存

天真的分析会预期主机内存占用 2× model\_size：页缓存（1× 模型）+ 分片缓冲（总计 1× 模型）。但在昇腾 NPU 上，`pin_memory()` 通过 `/dev/davinci_manager` 分配，把分片放进 cgroup 内存控制器看不到的 CPU 内核 DMA 内存。物理内存 ≈ 页缓存 + 锁页分片 + 框架开销；cgroup 看不到锁页 DMA 部分，但服务器仍然需要相应数量的物理内存。

![Ascend host and HBM memory accounting](https://vllm.ai/blog-assets/figures/2026-07-30-distributed-layerwise-offload/ascend-memory-accounting.svg)

昇腾主机与 HBM 内存核算

*图 6：Cosmos3-Nano DP2 的昇腾内存核算。cgroup 看到共享页缓存与框架 RSS，而通过 `/dev/davinci_manager` 分配的锁页分片驻留在驱动管理的 CPU DMA 内存中，而非 NPU HBM。*

通过干净测量验证（Cosmos3-Nano DP2，全新 cgroup）：

```
cgroup usage_in_bytes = 49 GB = cache(31) + rss(18)  ← exact match, no extra
cgroup kmem           = 0 GB
davinci_manager RSS   = 0 kB  (in /proc/<pid>/smaps)
NPU HBM per card      = 10 GB  (< 14.5 GB shard → shard NOT in HBM)
Slab                  = 3.3 GB  (too small for 29 GB shard)

```

| 组件 | 位置 | 大小 | cgroup 是否跟踪？ |
| --- | --- | --- | --- |
| Safetensors 页缓存 | 系统内存（用户空间，共享） | 1× model\_size | ✓（cache） |
| 框架（Python/torch/HCCL） | 系统内存（用户空间，每 rank） | ~3.5 GB × dp\_size | ✓（rss） |
| 分片（锁页） | CPU 内核 DMA（/dev/davinci\_manager） | 每 rank model\_size / dp\_size | ✗ |
| 预取缓冲 | NPU HBM | 每 rank 2 × block\_size | ✗ |

这意味着 cgroup 可见内存按 O(model\_size + dp\_size × constant) 扩展，而非 O(dp\_size × model\_size)——但总物理内存等于 cgroup 可见内存加上 cgroup 看不到的锁页 DMA 分片。对于 200B 模型且 dp\_size=4：约 423 GB cgroup + 约 400 GB 内核 DMA = 约 823 GB 总物理内存（可装进 2 TB），而不使用 mmap 时为 2000 GB。

## 验证结果

所有测试均在昇腾 910B3（每卡 64 GB HBM，2 TB 系统内存）上进行，模型为 Cosmos3-Nano（33 GB）与 Cosmos3-Super（124 GB）。

### 正确性

| 模型 | 配置 | 请求数 | HTTP | 帧数 | 视频 |
| --- | --- | --- | --- | --- | --- |
| Nano (33 GB) | DP2 | 2 并发，35 步 | 2/2 × 200 | 29/29 | OK |
| Nano (33 GB) | DP4 | 4 并发，35 步 | 4/4 × 200 | 29/29 | OK |
| Super (124 GB) | DP2 | 1 请求，5 步 | 200 | 29 | OK |
| Super (124 GB) | DP4 | 1 请求，5 步 | 200 | 29 | OK |

### 主机内存（cgroup 峰值）

| 模型 | 配置 | cgroup 峰值 | 页缓存 | RSS | 每 worker HWM | 相对基线 |
| --- | --- | --- | --- | --- | --- | --- |
| Nano (33 GB) | DP4（mmap） | 47 GB | 31 GB | 14 GB | 12.1 GB | — |
| Nano (33 GB) | DP4（无 mmap） | 178 GB | — | — | 36 GB | -73% |
| Super (124 GB) | DP2 | 157 GB | 149 GB | 7 GB | 65.2 GB | — |
| Super (124 GB) | DP4 | 172 GB | 149 GB | 14 GB | 35.5 GB | — |

### NPU HBM

| 模型 | 配置 | HBM/卡（空闲） | HBM/卡（推理中） | 64 GB 余量 |
| --- | --- | --- | --- | --- |
| Nano (33 GB) | DP2 | 9.9 GB | 10.4 GB | 55 GB |
| Nano (33 GB) | DP4 | 9.4 GB | 10.2 GB | 55 GB |
| Super (124 GB) | DP2 | ~15 GB | — | ~49 GB |
| Super (124 GB) | DP4 | ~10 GB | — | ~54 GB |

对于实测的 `dist_offload+SP` 720p 10s 工作负载，峰值 HBM 从 Nano 到 Super 增长约 22%（23.1 → 28.1 GB），空闲 HBM 增长约 27%（11.5 → 14.6 GB）。设备上只驻留 2 层权重，因此大 3.8 倍的模型仍远低于 64 GB 限制。

### 性能

这些昇腾测量使用 Cosmos3-Nano，832×480、29 帧、35 个去噪步。**生成帧/秒**指每墙上时钟秒产生的输出视频帧总数（`29 frames × outputs per wave / wave latency`），而非视频的播放帧率。

| 策略 | 每步（ms） | 生成帧/秒 | CPU/rank | HBM/卡 | 相对 HSDP |
| --- | --- | --- | --- | --- | --- |
| HSDP+SP（基线） | 870 | 0.967 | 0 GB | 20.3 GB | — |
| dist\_offload+AG（DP4，1 请求） | 1,020 | 0.806 | 3.5 GB | 12.4 GB | -17% |
| dist\_offload+AG（DP4，4 请求） | 1,020 | 3.22 | 3.5 GB | 12.4 GB | 3.3× |
| dist\_offload no-AG | 1,877 | 0.439 | 28.3 GB | 14.1 GB | -55% |

AllGather 开销 = 150 ms/步（72 ms 流切换 + 10 ms HCCL + 68 ms Python 分发），在 Cosmos3-Nano DP4 上测得。通信量随层维度、参与方数量和拓扑而变化。有 4 个并发请求时，这笔固定成本被摊销 4 倍。

### NVIDIA B300 GPU 结果

为验证平台无关性，我们在 NVIDIA B300 SXM6 GPU 上运行了同一套 DLO 技术栈。下面的 Cosmos3 测试使用 Cosmos3-Super BF16（124 GB）、4× NVIDIA B300（物理 GPU 1,5,6,7）、Python 3.12.3、PyTorch 2.11.0+cu130、CUDA 13.0、vLLM `0.23.0`，以及 vLLM-Omni commit [`9772bb32`](https://github.com/vllm-project/vllm-omni/commit/9772bb321f558a28c0dca1cb53b44aaf10e4ab69)（PR [#5397](https://github.com/vllm-project/vllm-omni/pull/5397) 合并前的快照；最终合并后的 HEAD 包含本基准测试中不存在的后续 loader 门控与 TP/mmap 校验改动）。接下来的 MiniMax-H3 小节记录了它自己的 vLLM/vLLM-Omni 版本、`enforce_eager=True` 标志以及一个本地流水线补丁；这些细节仅适用于 MiniMax-H3 研究，不适用于 Cosmos3 运行。

正确性通过所有策略间逐字节一致的输出哈希验证。例如，T2I seed 42 在 DLO+AG、no-AG、DLO+USP4、legacy layerwise+USP4 与 HSDP+USP4 下产生了相同的 SHA256 `6e7d2a8c63b88391...`。T2V 832×480×29f seed 17 在所有策略下产生了相同的 666,029 字节输出（SHA256 `c5d38f5d21ca619e...`）。

CUDA 进程树 PSS 包含共享页缓存、锁页 CPU 分片与框架内存。昇腾 cgroup 测量不含 `/dev/davinci_manager` 支撑的锁页分片，因此 GPU PSS 与昇腾 cgroup 数字不能直接比较。

#### 1024×1024 T2I，50 步

| 策略 | 并发 | Wave 延迟 | 吞吐量 | 进程树 PSS | 峰值 HBM/卡 |
| --- | --- | --- | --- | --- | --- |
| DLO+AG DP4 | 4 | 43.69s（中位数） | 0.0915 outputs/s | 198–202 GiB | 12.62 GiB |
| DLO no-AG DP4 | 4 | 112.96s | 0.0354 outputs/s | 532 GiB | 11.43 GiB |
| HSDP+USP4 | 1 | 15.19s | 0.0658 outputs/s | 483 GiB | 42.00 GiB |
| legacy layerwise+USP4 | 1 | 105.22s | 0.0095 outputs/s | 533 GiB | 13.99 GiB |

4 个并发请求的 DLO+AG DP4 达到 HSDP+USP4 吞吐量的 **1.39×**，同时只使用 **30%** 的 HBM（12.6 GiB 对 42.0 GiB）。

#### 832×480 T2V，29 帧，35 步

| 策略 | 每 wave 输出数 | Wave 延迟 | 吞吐量 | 输出 SHA |
| --- | --- | --- | --- | --- |
| DLO+AG DP4 | 4 | 38.79s | 0.1033 outputs/s | c5d38f5d... |
| HSDP+USP4 | 1 | 15.38s | 0.0653 outputs/s | c5d38f5d... |
| DLO+AG+USP4 | 1 | 30.79s | 0.0326 outputs/s | c5d38f5d... |
| legacy layerwise+USP4 | 1 | 81.46s | 0.0123 outputs/s | c5d38f5d... |

#### 工作负载延迟与 HBM（35 步，DLO+AG DP4 对比 HSDP+USP4）

| 工作负载 | DLO 策略 | DLO 每 wave 输出数 | DLO wave 延迟 | DLO 峰值 HBM/卡 | HSDP 每 wave 输出数 | HSDP wave 延迟 | HSDP 峰值 HBM/卡 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 480p, 29f | DLO+AG DP4 | 4 | 38.79s | 14.55 GiB | 1 | 15.38s | 43.77 GiB |
| 480p, ~5s (121f) | DLO+AG DP4 | 4 | 102.58s | 15.88 GiB | 1 | 41.36s (125f) | 53.73–62.65 GiB |
| 480p, ~10s (241f) | DLO+AG DP4 | 4 | 226.70s | 17.33 GiB | 1 | 82.47s (245f) | 53.74 GiB |
| 720p, 5s (121f) | DLO+AG DP4 | 4 | 288.29s | 24.95 GiB | 1 | 87.47s | 52.19 GiB |
| 720p, 10s (241f) | DLO+AG+USP4 | 1 | 214.53s | 24.99 GiB | 1 | 210.05s | 53.73 GiB |

在 720p 10s（241f）上，DLO+AG+USP4 以 214.53s 完成——与 HSDP 的 210.05s 相差 **2.13%** 以内——输出逐字节一致（SHA256 `08cb679322996ea6...`），同时只使用 HSDP **47%** 的 HBM（24.99 GiB 对 53.73 GiB）。

#### 8× B300 上的 MiniMax-H3：DLO 模式依赖拓扑

由 Shunyang Li 完成的一项独立 [MiniMax-H3 B300 研究](https://github.com/lishunyang12/vllm-omni-rankings/tree/main/scripts/minimax_h3_b300_dlo_industrial_report)测试了 DP、SP 与 DLO 执行模式在一台 8× NVIDIA B300 SXM6 AC 节点上如何相互作用。与上面的 Cosmos3 测量不同，该工作负载同时生成视频**和**音频：768×1344、124 视频帧、立体声音频、BF16、每副本批大小 1、请求 50 步（49 次调度器去噪更新）。该研究的 `environment.json.txt` 报告 vLLM `0.24.0` 与 vLLM-Omni `0.26.0rc2.dev11+g6607f4a7f`（源码 commit [`9e73ee1`](https://github.com/vllm-project/vllm-omni/commit/9e73ee1a50ce247c638052011914d8027d717f28)）；运行器设置 `enforce_eager=True`（禁用图编译），并对 `pipeline_minimax_h3.py` 应用了一个[本地子组广播补丁](https://github.com/lishunyang12/vllm-omni-rankings/tree/main/scripts/minimax_h3_b300_dlo_industrial_report)。这些结果不代表未修改的发行版或默认的编译图路径。下面每条选定的 T2VA 路线都包含跨两个引擎生命周期、每个生命周期一次完整预热后的 20 个实测 wave。吞吐量为输出数量除以 wave 时间；能耗按每输出的八卡板卡功率之积累积计算，未扣除空闲基线；一个外部 `nvidia-smi` 采样器以 0.758s 中位间隔记录内存与功率。

![Topology-aware DLO policy for MiniMax-H3 on eight B300 GPUs](https://vllm.ai/blog-assets/figures/2026-07-30-distributed-layerwise-offload/minimax-h3-topology-policy.svg)

八卡 B300 GPU 上 MiniMax-H3 的拓扑感知 DLO 策略

*图 7：三条受评估路线内实测的服务前沿。提高 DP 会用每 wave 延迟换取并发输出能力；首选 DLO 模式在 DP8×SP1 处从 AllGather 变为 rank-local。*

| 服务目标 | 拓扑 / DLO 模式 | Wave P50 | Wave P95 | 持续吞吐量 | 实测峰值/GPU | 每视频板卡能耗 |
| --- | --- | --- | --- | --- | --- | --- |
| 最低延迟 | DP1×SP8 / AllGather | 34.55s | 35.25s | 103.84 视频/小时 | 26.37 GiB | 68.08 Wh |
| 平衡拐点 | DP4×SP2 / AllGather | 94.73s | 95.31s | 151.89 视频/小时 | 25.11 GiB | 51.76 Wh |
| 最高吞吐 / 最低能耗 | DP8×SP1 / rank-local | 156.74s | 157.03s | 183.78 视频/小时 | 20.05 GiB | 43.97 Wh |

成对的五 wave 模式对比解释了为什么不存在单一的全局 DLO 策略。在 DP1×SP8，AllGather 利用 SP 组，将吞吐量提高 129.4%，同时把 P50 延迟降低 56.6%。在 DP4×SP2，其吞吐量收益收窄到 2.2%。在 DP8×SP1，AllGather 使吞吐量下降 4.1%、P50 延迟增加 3.8%，并把实测的每 GPU 峰值从 20.03 推高到 94.03 GiB，因此 rank-local DLO 更受青睐。FL2VA 首帧与 Ref2VA 图像+音频测试保持相同的延迟-吞吐排序。

![FL2VA and Ref2VA latency-throughput Pareto frontiers on MiniMax-H3](https://vllm.ai/blog-assets/figures/2026-07-30-distributed-layerwise-offload/minimax-h3-multimodal-frontiers.png)

MiniMax-H3 上 FL2VA 与 Ref2VA 的延迟-吞吐帕累托前沿

*图 8：在三条受评估路线中（每条路线 n=5 个实测 wave），FL2VA 首帧 I2VA 与 Ref2VA 图像+音频改变了绝对延迟和吞吐量，但保持了 DP1×SP8 → DP4×SP2 → DP8×SP1 的前沿排序。来源：[MiniMax-H3 B300 研究产物](https://github.com/lishunyang12/vllm-omni-rankings/tree/main/scripts/minimax_h3_b300_dlo_industrial_report)。*

这些结果是一项拓扑研究，并非普适的生产声明。DP2×SP4 未测量；实验覆盖单节点、单输入集、单分辨率与帧数，且是形状验证而非感知质量验证。它使用源码 commit [`9e73ee1`](https://github.com/vllm-project/vllm-omni/commit/9e73ee1a50ce247c638052011914d8027d717f28) 外加一个有记录的本地子组广播修复，且运行时警告所测试的 vLLM-Omni 与 vLLM 版本未与发行版对齐。该档案提供了 [PDF、CSV、105 个 wave 样本、环境哈希、本地 diff 与基准测试运行器](https://github.com/lishunyang12/vllm-omni-rankings/tree/main/scripts/minimax_h3_b300_dlo_industrial_report)供独立审查。

### 外推到 400 GB

下表基于上文实测内存模型的主机容量外推；并未实际运行任何 200B 级模型，该规模下的最大块大小、HBM 余量、带宽、延迟与输出质量均未验证。

| 模型 | dp\_size | cgroup 峰值（估计） | 总内存（估计） | 能装进 2 TB？ |
| --- | --- | --- | --- | --- |
| 33 GB | 4 | 47 GB | ~80 GB | ✓ |
| 124 GB | 4 | 172 GB | ~296 GB | ✓ |
| 185 GB | 4 | ~220 GB | ~405 GB | ✓ |
| 400 GB | 4 | ~423 GB | ~823 GB | ✓ |
| 400 GB | 8 | ~443 GB | ~843 GB | ✓ |

## 致谢

我们感谢 vLLM-Omni 的贡献者，包括提供细致代码评审反馈的 @hsliuustc0106 与 @yuanheng-zhao，为 MiniMax-H3 B300 拓扑研究与可复现产物做出贡献的 Shunyang Li（[@lishunyang12](https://github.com/lishunyang12)），以及提供硬件支持的昇腾 NPU 团队。

## 参考文献

**源代码：**

- 分布式逐层卸载后端、meta 转换与 mmap 加载：`distributed_layerwise_backend.py`
- OffloadConfig 与策略选择：`base.py`
- 多队列执行器：`multiproc_executor.py`
- DP 多并发 worker：`diffusion_worker.py`
- 单元测试：`test_distributed_layerwise_backend.py`

**RFC 与 PR：**

- RFC：GitHub Issue #5396
- 实现 PR：vllm-omni#5397
- DLO DP 并发请求修复：[vllm-omni#5864](https://github.com/vllm-project/vllm-omni/pull/5864)
- rank-local DLO DP 的独立请求：[vllm-omni#5911](https://github.com/vllm-project/vllm-omni/pull/5911)

**模型与基准测试产物：**

- Cosmos3-Nano：33 GB safetensors（17B 参数，72 个块）
- Cosmos3-Super：124 GB safetensors（64B 参数，128 个块）
- MiniMax-H3：[B300 DLO 研究笔记与可复现产物](https://github.com/lishunyang12/vllm-omni-rankings/tree/main/scripts/minimax_h3_b300_dlo_industrial_report)
