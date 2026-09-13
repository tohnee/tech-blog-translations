---
title: "共享内存 IPC 缓存：加速 LLM 推理系统中的数据传输"
title_en: "Shared Memory IPC Caching: Accelerating Data Transfer in LLM Inference Systems"
source: https://vllm.ai/blog/2025-11-13-shm-ipc-cache
crawled: 2026-09-12
translated: 2026-09-13
---

# 共享内存 IPC 缓存：加速 LLM 推理系统中的数据传输

> 原文：[Shared Memory IPC Caching: Accelerating Data Transfer in LLM Inference Systems](https://vllm.ai/blog/2025-11-13-shm-ipc-cache) · vLLM 博客

Donglu Wang（Cohere）

[#性能](https://vllm.ai/blog/tags/performance)[#多模态](https://vllm.ai/blog/tags/multimodal)

> **注意：** 本文最初发表于 [Cohere 博客](https://cohere.com/blog/making-data-transfer-in-llm-systems-faster-leaner-and-more-scalable)。

我们隆重介绍共享内存 IPC 缓存（Shared Memory IPC Caching）——一种由 [Cohere 贡献给 vLLM 项目](https://github.com/vllm-project/vllm/pull/20452)的高性能缓存机制。它通过绕过冗余的进程间通信（IPC）、将大型多模态输入保存在共享内存中，大幅降低了数据传输开销，为大规模 LLM 推理带来更快、更高效的性能。

现代 LLM 推理通常涉及多个进程协同工作，通过进程间通信进行交流。随着并行规模扩大、输入内容日益丰富（想想多模态数据），IPC 开销很快就会成为重要的性能瓶颈。

借助共享内存 IPC 缓存，我们可以显著减少单节点上进程之间冗余的数据传输。我们的基准测试显示：

- **首次请求**：预填充吞吐量提升 **11.5%**，TTFT 降低 **10.5%**
- **缓存命中的请求**（KV 与图像输入均被复用）：预填充吞吐量提升 **69.9%**，TTFT 降低 **40.5%**
  这些收益主要来自消除了进程之间冗余的 IPC 传输。

此外，收益随输入大小和张量并行（TP）规模而扩大：输入越大、TP 配置越宽，IPC 流量就越重，共享内存缓存对大型多模态负载的影响也就越显著。

## LLM 推理中的进程间通信

在一个典型的多进程 LLM 推理栈中，有三大主要组件：负责处理与预处理用户请求的**前端（front-end）**、负责调度与编排的**协调器（coordinator）**，以及执行模型计算的推理 **worker**。

下图展示了一个使用四块 GPU 的 LLM 推理系统中各进程如何协作。前端将输入数据发送给协调器，协调器再将其路由到四个 worker（每块 GPU 一个）去执行推理。

![](https://vllm.ai/blog-assets/figures/2025-shm-ipc-cache/processes1.png)
图 1. 使用四块 GPU 的 LLM 推理系统中进程协作概览

每个阶段通常运行在独立的进程中，以获得可扩展性和异步执行能力。因此，数据必须经由 IPC 在这些进程之间流动。对于小输入，这一开销可以忽略不计；但随着输入增大，IPC 时间可能成为主要瓶颈。

## 问题：重复的大数据传输

多模态输入，如图片、音频或长上下文序列，可能非常庞大。例如，在 [`CohereLabs/command-a-vision-07-2025`](https://huggingface.co/CohereLabs/command-a-vision-07-2025) 模型中，一张 1024×3072 像素的最大尺寸输入图像，以 int8 数组表示时约为 9 MB。该模型还接受多张图像作为输入，因此单个请求的总大小很容易达到数十 MB。

通过 IPC 在进程之间传输如此大的输入并非没有代价。在多轮对话或批处理场景中，同样的输入可能被多次传输，进一步放大了开销。

## 现有方案：镜像缓存

vLLM 已经使用镜像缓存（mirrored caching）来减少冗余的 IPC 传输。在这种方案中，发送方与接收方各自维护一份按相同插入顺序与相同淘汰策略更新的复制缓存。当发送方检测到某个输入发生缓存命中时，它假定接收方的缓存处于相同状态，于是跳过 IPC 传输。

然而，这一方案有一个关键限制：它依赖严格的输入顺序，即发送方与接收方必须以完全相同的顺序处理输入。例如，在一个典型的「前端—协调器—worker」设置中，如果镜像缓存放在 worker 上，协调器可能基于其调度策略对输入进行重排，导致缓存失步，进而可能引发错误行为。

因此，在 vLLM 中，镜像缓存只应用于前端与协调器之间的通信。至于协调器—worker 路径，当只有一个 worker 时，vLLM 会把它放进与协调器相同的进程里，从而免去额外的 IPC；而涉及多个 worker 时，vLLM 会退回到基于套接字的 IPC，这会带来序列化、传输与反序列化的额外开销。

## 新方案：共享内存 IPC 缓存

为了克服传统 IPC 缓存的局限，我们推出了共享内存 IPC 缓存。现在，一个单一的共享缓存可以被发送方与所有接收方直接访问，消除了对顺序的假设和冗余的数据拷贝。

### 共享内存对象存储（Shared Memory Object Store）

我们实现了一个共享内存对象存储数据结构来支撑这一缓存机制，让一个写者（writer）实例与多个读者（reader）实例能够高效共享同一块内存缓冲区。

**设计**

- **写者**：将输入对象插入共享环形缓冲区，更新地址索引，并把地址广播给所有相关读者
- **读者**：使用提供的地址直接从共享内存访问对象

下图展示了基于共享内存对象存储的 IPC 缓存。发送进程持有一个写者实例，而每个接收进程都有对应的读者实例。

![](https://vllm.ai/blog-assets/figures/2025-shm-ipc-cache/shared_memory_object_store.png)
图 2. 基于共享内存对象存储的 IPC 缓存示意图

发送「键—对象」对时，发送方先通过 `is_cached(key)` 检查该键是否已缓存。若已缓存，写者用 `get_cached(key)` 获取缓冲区地址；否则，它用 `put(key, object)` 把对象存入共享内存并获得缓冲区地址。随后，发送方通过默认 IPC 把该地址广播给所有接收方。

在接收侧，收到地址后，用 `get(address)` 从共享内存取出对象。为简洁起见，图中省略了序列化与反序列化步骤。

**淘汰与安全性**

当空间不足时，写者从环形缓冲区头部淘汰。
**读者计数器（共享）** 与 **写者计数器（本地）** 相互配合，防止数据仍在使用时被过早淘汰。只有当条件 `writer_counter × n_readers == reader_counter` 满足时，条目才会被淘汰。

**收益**

- **无顺序假设**：进程可以以任意顺序消费输入
- **单一共享缓存**：无论读者数量多少，共享内存占用保持恒定。
- **高效的并发访问**：多个读者可以同时读取同一输入，同步开销极小，且无需额外拷贝。

把共享内存对象存储应用到前述「前端—协调器—worker」设置中，我们把写者放在前端进程，并在每个 worker 进程中放置一个专属读者。这使我们能够绕过中间 IPC，尤其是对大型输入数据。

![](https://vllm.ai/blog-assets/figures/2025-shm-ipc-cache/processes2.png)
图 3. 由共享内存对象存储支撑的 LLM 推理系统中进程协作概览

### vLLM 基准测试结果

我们通过一个 PR 在 vLLM 中为多模态输入实现了共享内存 IPC 缓存。为评估其影响，我们使用以下配置运行了基准测试：

- 模型：[`CohereLabs/command-a-vision-07-2025`](https://huggingface.co/CohereLabs/command-a-vision-07-2025)
- 硬件：4× A100（80GB，TP=4）
- 数据集：[VisionArena-Chat](https://huggingface.co/datasets/lmarena-ai/VisionArena-Chat?ref=cohere-ai.ghost.io)

结果如下：

**首次请求**

| 指标 | 基线 | 共享内存 IPC 缓存 | 差异 |
| --- | --- | --- | --- |
| 预填充吞吐量 | 581.34 tok/s | 648.22 tok/s | **+11.5%** |
| 平均 TTFT | 3898.98 ms | 3491.15 ms | **−10.5%** |

加速来自在前端只写一次、让 worker 并发读取，同时消除了冗余传输和 IPC 排队延迟。

**缓存命中的请求**

| 指标 | 基线 | 共享内存 IPC 缓存 | 差异 |
| --- | --- | --- | --- |
| 预填充吞吐量 | 2894.03 tok/s | 4917.57 tok/s | **+69.9%** |
| 平均 TTFT | 790.18 ms | 470.60 ms | **−40.5%** |

在这一场景中，KV 与图像输入都被缓存，因此降低 IPC 开销的收益尤为明显。

## 立即上手

共享内存 IPC 缓存加速了 LLM 系统中的数据流动，使其更精简、更具可扩展性——对于具有大型多模态输入或多个并发 GPU worker 的负载尤其如此。在 LLM 推理之外，任何 IPC 缓存有助于减少冗余数据传输的场景都能从中受益，这使它成为适用范围极广的通用工具。

该特性现已在 vLLM main 分支可用。要为多模态缓存启用它，请设置 `mm_processor_cache_type = "shm"`。更多信息请参阅 [vLLM 用户指南](https://docs.vllm.ai/en/latest/configuration/optimization/#ipc-caching)。

## 致谢

特别感谢 Cohere 的 Bharat Venkitesh，以及 vLLM 社区的成员：[Cyrus Leung](https://github.com/DarkLight1337)，在代码评审与集成方面提供了宝贵反馈；[Nick Hill](https://github.com/njhill) 和 [Roger Wang](https://github.com/ywang96)，完成了早期概念验证；[Kero Liang](https://github.com/imkero)，报告并协助修复了一个 bug。
