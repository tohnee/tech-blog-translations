---
title: "快速引擎恢复：基于权重缓存守护进程的 SGLang 亚秒级引擎重启"
title_en: "Fast Engine Recovery: Sub-Second Engine Restart for SGLang via Weight Cache Daemon"
author: "Ant Ling Infra Team (Ant Group), Alibaba, SGLang Team"
date: "August 21, 2026"
previewImg: /images/blog/sglang-fast-recovery/preview.png
source: https://lmsys.org/blog/2026-08-21-sglang-fast-recovery/
translated: 2026-09-12
---

# 快速引擎恢复：基于权重缓存守护进程的 SGLang 亚秒级引擎重启

> 原文：[Fast Engine Recovery: Sub-Second Engine Restart for SGLang via Weight Cache Daemon](https://lmsys.org/blog/2026-08-21-sglang-fast-recovery/) · LMSYS Blog · Ant Ling Infra Team (Ant Group), Alibaba, SGLang Team

## TL;DR

如今，最先进（SOTA）模型的规模越来越大，服务崩溃后重新加载模型的开销也变得非常昂贵。为此，我们推出**权重缓存守护进程（Weight Cache Daemon）**——一个常驻 GPU 的进程，它将量化后的模型权重保存在 GPU 显存中，并通过 CUDA IPC 零拷贝映射提供给新的 SGLang 引擎实例。这将权重加载时间从分钟级缩短到秒级。

权重缓存守护进程是我们**快速引擎恢复框架（Fast Engine Recovery Framework）**的第一阶段，该框架面向生产级 LLM 推理服务，目标是 **< 10 秒的冷启动重启**与 **< 1 秒的热备切换**。

关键成果：

1. **权重加载：~495s → ~0.63s**——**约 785 倍加速**，基于 Ling-2.6-1T FP8 模型。
2. **总启动时间：8.8min → 0.528min**——端到端引擎启动时间缩短 **93.9%**。
3. **多实例权重共享**——同一 GPU 上的多个引擎实例映射到相同的 IPC 句柄，消除冗余的磁盘 I/O 与量化后变换。
4. **< 1 秒完成主备故障切换**——备用引擎通过零拷贝共享权重，在不把整组 GPU 专门留给空闲副本的前提下，实现近乎零停机的故障切换。
5. **多节点实例权重共享**——支持面向大模型的多节点模式

## 背景

随着 LLM 模型不断变大——Qwen3-235B、Ling-2.6-1T，以及新发布的 2.8T Kimi K3——推理服务引擎的冷启动时间已成为生产效率的关键瓶颈。一个部署在 8×H20-3e GPU 上的 Ling-2.6-1T FP8 实例，权重存放在 3.5TB NVMe SSD 中，仅达到可服务状态就需要 **约 8.52 分钟**。在生产环境中，这意味着：

- 重启期间的 **P99 尾延迟尖峰**——所有进行中的请求要么失败，要么无限期排队。
- **可用性下降**——长达数分钟的恢复窗口会违反 SLA 目标。
- **运维摩擦**——滚动更新、配置变更和故障恢复全部被重启周期拖慢。
- **GPU 资源浪费**——传统主备部署会把一整组 GPU 专门留给空闲副本，使故障切换的硬件成本翻倍。

时间都花在哪里了？我们对 Ling-2.6-1T FP8 的一次完整 SGLang 引擎启动做了性能剖析：

| 阶段 | 耗时（s） | 占比 | 备注 |
|-------|----------|------------|-------|
| 预初始化与 ServerArgs | ~1 | 0.2% | 预初始化与 ServerArgs 解析 |
| Tokenizer 初始化 | ~13 | 2.4% | 加载并初始化分词器 |
| 初始化 torch distributed | ~5 | 0.9% | NCCL 2.28.9,8*H20,NVLink mesh 370.8 GB/s,P2P/IPC；最慢 rank TP1=5.19s |
| 加载权重（磁盘） | ~495 | 93.9% | 161 个分片，W8A8 FP8（CompressedTensorsW8A8Fp8MoE），最慢 rank=495.3s，每卡 120GB；受磁盘 I/O 限制 |
| 缓存分配（KV+Mamba） | ~1 | 0.2% | KV:553,599 tokens/5.94GB bf16；Mamba SSM state:5.33GB，max_mamba_cache_size=155 |
| 捕获 CUDA 图 | ~7.7 | 1.5% | 仅 3 个 decode 批大小 [1,2,4] |
| 服务器就绪 | ~4 | 0.8% | Unified RadixTree 初始化、HTTP/uvicorn 启动、预热请求 |
| **总计** | **~527** | | **约 8.8 分钟** 

瓶颈一目了然：**从磁盘加载权重占了启动时间的 93.2%**。对 Ling-2.6-1T FP8 模型而言，每个 TP rank 都要从磁盘读取约 120GB 的 safetensors，反序列化、执行 TP 分片，并进行量化后变换（FP8 量化、权重重排）。这些工作**在每次重启时都一模一样地重复一遍**，尽管最终得到的 GPU 张量是确定的，而且往往本来就还在 GPU 显存中。

能不能避免每次都从磁盘重新加载？答案是**可以**——让权重在引擎重启之间一直保留在 GPU 显存中。

## 设计

### 核心思路：基于 CUDA IPC 的持久权重缓存

权重缓存守护进程是一个常驻 GPU 的进程，它在 GPU 显存中保存量化后、已按 TP 分片的权重。引擎重启时，新的引擎进程通过 **CUDA IPC 零拷贝**直接从守护进程映射权重——没有磁盘 I/O，没有反序列化，也没有量化。

<img src="/images/blog/sglang-fast-recovery/architecture.svg" style="display:block; margin-left: auto; margin-right: auto; width: 92%;">

每个 GPU 为其 TP rank 运行**一个守护进程**。守护进程会：

1. 从磁盘加载模型权重（完整流水线：磁盘 → TP 分片 → 量化 → 重排）。
2. 将 `model.state_dict()` 中的每个参数和缓冲区导出为 CUDA IPC 句柄。
3. 记录一份 `CacheConfig` 指纹（模型路径、TP/DP 大小、量化配置哈希、dtype）。
4. 通过 Unix socket 向发起请求的引擎进程提供 IPC 句柄。

引擎连接守护进程、校验配置兼容性，然后将权重直接映射进自己的地址空间——引擎与守护进程通过 CUDA IPC **共享同一块物理 GPU 显存**。

### 基于 Meta Device 的零拷贝加载

亚秒级加载的关键在于**零拷贝**：引擎的 `param.data` 指针被直接设置为 IPC 映射的 GPU 张量，不发生任何数据拷贝。

为此，引擎先在 **meta 设备（meta device）** 上初始化模型（不分配 GPU/CPU 内存），再把每个参数的数据指针替换为 IPC 映射的张量。

由 `process_weights_after_loading()` 创建的量化后参数（例如 FP8 量化产生的 `weight_scale`）同样由守护进程缓存并直接映射——无需重新量化。

### 配置校验：安全第一

引擎配置与守护进程缓存配置之间的任何不匹配都会触发**完整的磁盘重载**，以确保正确性：

| 字段 | 不匹配示例 | 后果 |
|-------|-----------------|-------------|
| `model_path` + `model_arch` + `revision` | 模型或版本（revision）不同 | 权重完全错误 |
| `tp_size` + `tp_rank` | TP 分片方式不同 | 该 rank 拿到错误的分片 |
| `pp_size` + `pp_rank` | PP 划分方式不同 | 该流水线阶段拿到错误的层 |
| `dp_size` + `ep_size` | DP/EP 策略不同 | 权重分布不正确 |
| `quant_method` + `quant_config_hash` | 量化方式不同 | 未量化与 FP8 之间的错配 |
| `dtype` | float16 与 bfloat16 | 类型不匹配 |
| `device_capability` + `torch_version` | GPU 架构或 torch 版本不同 | 权重可以正常映射，但推理数值错误 |

最后两个字段构成一个**环境戳（environment stamp）**：如果守护进程与客户端运行了不同的后处理分支（不同的 compute capability 或 torch/内核版本），它们产出的权重可能通过 IPC 干净地映射过来，推理时却给出错误结果——把环境信息记入 `CacheConfig`，就能把这种情况变成一次明确的不匹配。

这对生产安全至关重要：如果运维人员更换了模型或量化配置，引擎会检测到不匹配并回退到磁盘加载，而不是映射不兼容的权重。

在配置校验之上，量化方法还受到 **IPC 白名单**的约束。CUDA IPC 零拷贝只导出原始张量数据，因此只有当 `process_weights_after_loading()` 的全部效果都被这些数据捕获时才是正确的。那些会写入 Python 侧元数据、或对权重做重排/转置的方法（逐张量 FP8、Marlin、AWQ/GPTQ）会在不经意间输出错误数值——因此它们会直接抛出硬错误。目前已验证的方法：**未量化**与**分块 FP8**（设置了 `weight_block_size`）；更多方法将在完成端到端验证后加入。

### 三种模式：daemon、client 与 off

| 模式 | 流程 | 权重加载耗时 | GPU 显存 | 适用场景 |
|------|------|-----------------|------------|----------|
| **daemon** | 引擎拉起守护进程 → 守护进程从磁盘加载 → 引擎映射 IPC | < 1s（守护进程就绪后） | 1×（共享） | 首次启动；由引擎管理守护进程生命周期 |
| **client** | 连接到预先运行的守护进程 → 映射 IPC | < 1s | 1×（共享） | 引擎重启；守护进程已在运行 |
| **off** | 常规磁盘加载 | 405–411s（Ling-2.6-1T FP8） | 1× | 默认；不使用缓存 |

**daemon** 模式下，引擎在启动过程中拉起守护进程，并等待它们从磁盘加载权重。首次启动仍然较慢（守护进程必须从磁盘加载），但之后的重启可以瞬时完成。

**client** 模式下，引擎连接到已在运行的守护进程。这就是快速重启路径——守护进程更早启动，权重已经保存在 GPU 显存中。

### 安全性与健壮性

权重缓存守护进程的设计原则是**低侵入且安全**：

- **侵入性最小**：该特性完全自包含在 `python/sglang/srt/weight_cache/` 中，对核心引擎的改动极少（仅涉及 `load_model()` 分发逻辑和一个命令行 flag）。
- **崩溃安全**：守护进程崩溃时，已运行的引擎实例可以继续工作——它们已通过 CUDA 引用计数持有 IPC 映射张量的引用。只有当守护进程和引擎**都**退出后，GPU 显存才会被释放。
- **守护进程恢复**：守护进程重启后会重新从磁盘加载权重并重新导出 IPC 句柄，新的引擎实例随后即可连接重启后的守护进程。
- **不匹配时回退**：配置不匹配时，client 模式会自动回退到磁盘加载；daemon 模式则直接抛出错误（因为两个进程共享同一块 GPU，回退会导致 OOM）。

## 超越重启：生产场景

权重缓存守护进程解锁了过去在传统磁盘加载方式下不切实际的生产模式：

### 多实例权重共享

每个 GPU 上由单个守护进程在显存中保存权重；多个引擎实例（例如相互独立的服务）通过零拷贝映射到相同的 IPC 句柄。无论有多少个实例在消费权重，磁盘加载与量化**在每个 GPU 上都只发生一次**。

<img src="/images/blog/sglang-fast-recovery/multi-instance.svg" style="display:block; margin-left: auto; margin-right: auto; width: 82%;">

### 优先级混部（Priority Co-Serving）

在同一块 GPU 上运行高优先级在线服务和低优先级批处理任务，二者由同一个权重缓存守护进程支撑。低优先级实例可以**在亚秒级时间内被逐出并重新拉起**，无需从磁盘重新加载权重——在不付出常规启动代价的情况下实现灵活的 GPU 分时复用。

### 主备故障切换

在主引擎旁边部署一个备用引擎，两者都由同一个权重缓存守护进程支撑。备用引擎通过零拷贝映射权重并保持热备状态。主引擎故障时，备用引擎在 **< 1 秒**内接管——无需加载权重，没有磁盘 I/O。

这实现了近乎零停机的故障切换，同时**无需把一整组 GPU 专门留给空闲副本**，避免了传统热备部署高昂的 GPU 资源浪费。

<img src="/images/blog/sglang-fast-recovery/active-standby.svg" style="display:block; margin-left: auto; margin-right: auto; width: 82%;">

## 性能

### 权重加载：磁盘 vs IPC 零拷贝

#### 单节点

| 模型 | 权重大小 | 磁盘加载（s） | IPC 零拷贝（s） | 加速比 |
|-------|-------------|---------------|-------------------|---------|
| **Qwen3-235B FP8** | **~235 GB** | **~306–327** | **<1** | **~500×** |
| **Ling-2.6-1T** | **~1 TB** | **~405–411** | **<1** | **~780×** |


#### 性能图表

<img src="/images/blog/sglang-fast-recovery/results.svg" style="display:block; margin-left: auto; margin-right: auto; width: 88%;">

## 使用方法

### 启动权重缓存守护进程 - 单节点

一条命令即可启动所有 TP rank 的守护进程：

```bash
# Standalone daemon launch (one command for all TP ranks):
python -m sglang.srt.weight_cache.daemon \
    --model-path /path/to/model --tp-size 4 \
    --load-format auto --dtype auto --quantization fp8
```

等待守护进程就绪（每个 rank 会写入一个 `.ready` 文件）：

```bash
# Check readiness:
ls /tmp/sglang_weight_cache_rank*.ready
```

### 以权重缓存启动引擎

```bash
# Engine Client — connect to pre-running daemons (restart)
python -m sglang.launch_server \
    --model-path /path/to/model --tp-size 4 \
    --weight-cache-mode client
```

### 启动权重缓存守护进程 - 多节点

在多节点部署中，每个节点为本地的 TP rank 运行自己的守护进程。所有守护进程加入同一个分布式组，因此 `--nnodes`、`--node-rank` 和 `--dist-init-method` 必须在各节点间保持一致，且 `$MASTER_ADDR` 指向节点 0：

```bash
# Daemon on node 0:
python -m sglang.srt.weight_cache.daemon \
    --model-path /path/to/model --tp-size 2 \
    --load-format auto --dtype auto --quantization fp8 \
    --nnodes 2 --node-rank 0 \
    --dist-init-method tcp://$MASTER_ADDR:29500

# Daemon on node 1:
python -m sglang.srt.weight_cache.daemon \
    --model-path /path/to/model --tp-size 2 \
    --load-format auto --dtype auto --quantization fp8 \
    --nnodes 2 --node-rank 1 \
    --dist-init-method tcp://$MASTER_ADDR:29500
```

待所有节点的守护进程都报告就绪后，启动引擎客户端。引擎客户端使用的会合端口（`29600`）与守护进程的端口（`29500`）相互独立：

```bash
# Engine client on node 0:
python -m sglang.launch_server \
    --model-path /path/to/model --tp-size 2 \
    --weight-cache-mode client \
    --nnodes 2 --node-rank 0 \
    --dist-init-addr $MASTER_ADDR:29600 --port 34000

# Engine client on node 1:
python -m sglang.launch_server \
    --model-path /path/to/model --tp-size 2 \
    --weight-cache-mode client \
    --nnodes 2 --node-rank 1 \
    --dist-init-addr $MASTER_ADDR:29600
```

## 快速引擎恢复框架：路线图

权重缓存守护进程是范围更大的**快速恢复框架（Fast Recovery Framework）**的第一阶段，该框架的目标是 **< 10s 冷启动重启**与 **< 1s 热备切换**：

| 阶段 | 当前（s） | 目标（s） | 方法 | 状态 |
|-------|-------------|------------|----------|--------|
| **权重加载** | **~306–327** | **< 1** | **权重缓存守护进程（CUDA IPC）** | **已完成（本 PR）** |
| 捕获 CUDA 图 | ~34.9 | < 3 | CUDA 图序列化 + 重放 | 计划中 |
| DeepGEMM JIT 预热 | ~23.1 | < 2 | 内核缓存持久化、并行预热 | 计划中 |
| 服务器初始化与 Tokenizer | ~17.3 | < 3 | 分词器延迟初始化、配置缓存 | 计划中 |
| 初始化 torch distributed | ~4.7 | < 2 | NCCL 会话复用、持久化进程组 | 计划中 |
| KV 缓存分配 | ~0.5 | < 0.5 | KV 缓存复用 | 计划中 |
| 服务器就绪 | ~3.4 | < 1 | 重启时跳过预热请求 | 计划中 |
| **总计（单节点）** | **~390** | **< 10** | | |

对更多模型的支持也在推进中。

## 公开路线图

权重缓存守护进程只是**第一步**——还有很多工作要做，我们对前方的路线充满期待。目前的 Phase 1 覆盖 TP + PP、单节点与多节点启动、每 GPU 零拷贝 CUDA IPC，以及未量化与分块 FP8。除此之外，还有许多高价值方向尚待开拓：

- **更多模型与量化方式**：将 IPC 白名单扩展到分块 FP8 之外（逐张量 FP8、INT8、MXFP8、NVFP4、AWQ/GPTQ 等），并覆盖更多架构，包括多模态模型与 LoRA 基座权重。
- **DP/EP 与多节点**：DP/EP 分片键（shard keying）、跨节点守护进程的协调、生命周期管理与故障切换。
- **免重载的权重更新**：面向强化学习（RL）/ 在线更新的原地权重刷新，由守护进程充当权重投递代理。
- **跨 GPU 与集群级共享**：通过 peer-copy 与集群填充（fleet-fill），让整个集群的冷启动只需为每个分片组支付约一次磁盘读取。
- **KV 缓存恢复**：在重启/故障切换过程中保留并重新映射 KV 缓存（KV 复用、移交热备），让进行中的上下文在恢复后得以延续，而不必从头重算。
- **启动路径的其余环节**：CUDA 图序列化、内核预热持久化，以及更快的服务器/分布式初始化，以达成 **< 10s** 的冷重启目标。
- **其他硬件后端**：将这一特性扩展到提供类似功能的其他加速器（AMD 与 Intel 均有可类比的 IPC 机制）。
- **运维与可靠性**：指标监控、状态工具、安全加固与 CI 覆盖。

这非常依赖社区的力量。完整计划已在 [sgl-project/sglang#33522](https://github.com/sgl-project/sglang/issues/33522) 公开跟踪——**非常欢迎贡献与反馈**，有不少高价值的工作等待认领。

## 致谢

**Ant Ling Infra Team, Ant Group**：[Michael Qiu](https://github.com/QiuMike) qiudayu.qdy@antgroup.com

**Alibaba**：[Siyu Liu](https://github.com/liusy58) liusy58@smail.nju.edu.cn

**SGLang Team**：[Alex Nails](https://github.com/alexnails)
