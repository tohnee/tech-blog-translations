---
title: "走进 vLLM：高吞吐量 LLM 推理系统剖析"
title_en: "Inside vLLM: Anatomy of a High-Throughput LLM Inference System"
source: https://vllm.ai/blog/2025-09-05-anatomy-of-vllm
crawled: 2026-09-12
translated: 2026-09-13
---

# 走进 vLLM：高吞吐量 LLM 推理系统剖析

> 原文：[Inside vLLM: Anatomy of a High-Throughput LLM Inference System](https://vllm.ai/blog/2025-09-05-anatomy-of-vllm) · vLLM 博客

作者：Aleksa Gordic

[#大规模服务](https://vllm.ai/blog/tags/large-scale-serving)[#投机解码](https://vllm.ai/blog/tags/speculative-decoding)

> **注意：** 本文最初发布于 [Aleksa Gordic 的个人网站](https://www.aleksagordic.com/blog/vllm)。

### 从分页注意力、连续批处理、前缀缓存、投机解码（specdec）等，到多 GPU、多节点的大规模动态服务

在这篇文章中，我会逐步介绍构成一个现代高吞吐量 LLM 推理系统的所有核心系统组件与高级特性。具体而言，我将对 vLLM [[1]](#ref-1) 的工作原理进行拆解。

本文是一个系列的第一篇。它从宏观开始，然后逐层叠加细节（遵循倒金字塔式的结构），让你能够对完整系统建立准确的高层心智模型，而不会淹没在细枝末节中。

后续文章将深入探讨特定子系统。

本文分为五个部分：

1. [LLM 引擎与引擎核心](#llm-engine--engine-core)：vLLM 的基础（调度、分页注意力、连续批处理等）
2. [高级特性](#advanced-features--extending-the-core-engine-logic)：分块预填充、前缀缓存、引导解码与投机解码、PD 分离
3. [纵向扩展](#from-uniprocexecutor-to-multiprocexecutor)：从单 GPU 到多 GPU 执行
4. [服务层](#distributed-system-serving-vllm)：分布式 / 并发的 Web 脚手架
5. [基准测试与自动调优](#benchmarks-and-auto-tuning---latency-vs-throughput)：测量延迟与吞吐量

> **注意：** \* 分析基于 [commit 42172ad](https://github.com/vllm-project/vllm/tree/42172ad)（2025 年 8 月 9 日）。
>
> - 目标读者：所有对最先进 LLM 引擎工作原理感到好奇的人，以及有兴趣为 vLLM、SGLang 等项目做贡献的人。
> - 我将聚焦 [V1 引擎](https://docs.vllm.ai/en/latest/usage/v1_guide.html)。我也研究过 V0（现已[弃用](https://github.com/vllm-project/vllm/issues/18571)），这对理解项目演进很有价值，而且许多概念至今仍然适用。
> - 第一节关于 LLM Engine / Engine Core 的内容可能有些让人应接不暇/枯燥——但博客的其余部分有大量示例和图示。:)

## LLM 引擎与引擎核心

LLM 引擎是 vLLM 的基础构件。就其本身而言，它已经能够实现高吞吐量推理——但仅限于离线场景。你还不能通过 Web 把它服务给客户。

我们将以下面的离线推理代码片段作为贯穿全文的例子（改编自 [basic.py](https://github.com/vllm-project/vllm/blob/main/examples/offline_inference/basic/basic.py)）。

```
from vllm import LLM, SamplingParams

prompts = [
    "Hello, my name is",
    "The president of the United States is",
]

sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

def main():
    llm = LLM(model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

    outputs = llm.generate(prompts, sampling_params)

if __name__ == "__main__":
    main()
```

> **注意：** 环境变量：
>
> - VLLM\_USE\_V1="1" # 我们使用 V1 引擎
> - VLLM\_ENABLE\_V1\_MULTIPROCESSING="0" # 我们在单进程中运行

这一配置是：

- 离线的（没有 Web/分布式系统脚手架）
- 同步的（所有执行都发生在一个阻塞式的进程中）
- 单 GPU 的（没有数据/模型/流水线/专家并行；DP/TP/PP/EP = 1）
- 使用标准 transformer [[2]](#ref-2)（支持 Jamba 这类混合模型需要更复杂的混合 KV 缓存内存分配器）

从这里开始，我们将逐步构建出一个在线、异步、多 GPU、多节点的推理系统——但仍然服务标准 transformer。

在这个例子里我们做两件事：

1. 实例化一个引擎
2. 对它调用 `generate`，从给定提示中采样

让我们从分析构造函数开始。

### LLM 引擎构造函数

引擎的主要组件包括：

- vLLM 配置（包含配置模型、缓存、并行等所有旋钮）
- 处理器（processor）（通过校验、分词和处理，把原始输入 → `EngineCoreRequests`）
- 引擎核心客户端（在本运行示例中我们使用 `InprocClient`，它基本上等价于 `EngineCore`；我们将逐步构建到 `DPLBAsyncMPClient`，它支持大规模服务）
- 输出处理器（把原始 `EngineCoreOutputs` 转换为用户看到的 `RequestOutput`）

> **注意：** 随着 V0 引擎被弃用，类名和细节可能会变化。我会强调核心思想而非确切的函数签名。我会抽象掉其中一些、但并非全部的细节。

引擎核心本身由若干子组件构成：

- 模型执行器（Model Executor）（驱动模型的前向传播；我们目前面对的是 `UniProcExecutor`，它在单个 GPU 上有一个 `Worker` 进程）。我们将逐步构建到支持多 GPU 的 `MultiProcExecutor`
- 结构化输出管理器（Structured Output Manager）（用于引导解码——稍后介绍）
- 调度器（决定哪些请求进入下一个引擎步骤）——它进一步包含：
  1. 策略设置——可以是 **FCFS**（先来先服务）或**优先级**（高优先级请求先被服务）
  2. `waiting` 与 `running` 队列
  3. KV 缓存管理器——分页注意力 [[3]](#ref-3) 的心脏

KV 缓存管理器维护着一个 `free_block_queue`——可用 KV 缓存块的池（数量常常达到数十万的量级，取决于显存大小和块大小）。在分页注意力过程中，这些块充当把 token 映射到其已计算 KV 缓存块的索引结构。

![](https://vllm.ai/blog-assets/figures/2025-vllm-anatomy/engine_constructor.png)
**图 1**：本节描述的核心组件及其关系

> **注意：** 标准 transformer 层（非 MLA [[4]](#ref-4)）的块大小计算如下：
> 2（key/value）\* `block_size`（默认=16）\* `num_kv_heads` \* `head_size` \* `dtype_num_bytes`（例如 bf16 为 2）

在模型执行器构造期间，会创建一个 `Worker` 对象，并执行三个关键流程。（之后在 `MultiProcExecutor` 中，这些相同的流程会在不同 GPU 上的各个 worker 进程中独立运行。）

1. 初始化设备：

- 为 worker 分配一个 CUDA 设备（例如 "cuda:0"），并检查模型 dtype 是否受支持（例如 bf16）
- 验证在给定的 `gpu_memory_utilization` 下是否有足够的显存（例如 0.8 → 总显存的 80%）
- 设置分布式配置（DP / TP / PP / EP 等）
- 实例化 `model_runner`（持有采样器、KV 缓存以及 `input_ids`、`positions` 等前向传播缓冲区）
- 实例化 `InputBatch` 对象（持有 CPU 侧的前向传播缓冲区、用于 KV 缓存索引的块表、采样元数据等）

2. 加载模型：

- 实例化模型架构
- 加载模型权重
- 调用 model.eval()（PyTorch 的推理模式）
- 可选：对模型调用 torch.compile()

3. 初始化 KV 缓存

- 获取每层 KV 缓存规格。历史上这总是 `FullAttentionSpec`（同构 transformer），但随着混合模型（滑动窗口、Jamba 这类 Transformer/SSM）的出现，它变得更复杂（见 Jenga [[5]](#ref-5)）
- 运行一次虚拟/性能分析（profiling）前向传播并对 GPU 内存做快照，以计算可用显存中能容纳多少 KV 缓存块
- 分配、重塑并将 KV 缓存张量绑定到注意力层
- 准备注意力元数据（例如把后端设置为 FlashAttention），供内核在前向传播期间使用
- 除非提供 `--enforce-eager`，否则对每个预热批大小做一次虚拟运行并捕获 CUDA Graph。CUDA Graph 把整个 GPU 工作序列记录为一个 DAG。之后在前向传播中我们启动/重放预烘焙的图，从而削减内核启动开销、改善延迟。

这里我抽象掉了许多底层细节——但这些就是我现在要介绍的核心部分，因为后面的章节会反复引用它们。

现在引擎已经初始化完毕，接下来看 `generate` 函数。

### Generate 函数

第一步是校验请求并将其送入引擎。对每个提示我们：

1. 创建唯一的请求 ID 并记录其到达时间
2. 调用输入预处理器，对提示进行分词，返回一个包含 `prompt`、`prompt_token_ids` 和 `type`（text、tokens、embeds 等）的字典
3. 把这些信息打包进 `EngineCoreRequest`，再加上优先级、采样参数和其他元数据
4. 把请求传入引擎核心，后者将其包装为 `Request` 对象并把状态设为 `WAITING`。该请求随后被加入调度器的 `waiting` 队列（FCFS 用 append，优先级用 heap-push）

至此引擎已被喂入请求，可以开始执行。在同步引擎示例中，这些初始提示是我们唯一会处理的请求——没有在运行中途注入新请求的机制。相比之下，异步引擎支持这一点（即**连续批处理** [[6]](#ref-6)）：每一步之后，新旧请求都会被纳入考虑。

> **注意：** 由于前向传播会把批次摊平成单个序列、由自定义内核高效处理，即使在同步引擎中，连续批处理在根本上也是受支持的。

接下来，只要还有待处理的请求，引擎就会反复调用它的 `step()` 函数。每一步有三个阶段：

1. 调度：选择本步骤要运行哪些请求（解码，和/或（分块）预填充）
2. 前向传播：运行模型并采样 token
3. 后处理：把采样得到的 token ID 追加到每个 `Request`，进行 detokenize，并检查停止条件。如果某个请求已完成，就做清理（例如把它的 KV 缓存块归还给 `free_block_queue`）并提前返回输出

> **注意：** 停止条件包括：
>
> - 请求超出其长度限制（`max_model_length` 或其自身的 `max_tokens`）
> - 采样到的 token 是 EOS ID（除非启用 `ignore_eos` → 在我们想强制生成一定数量的输出 token 做基准测试时很有用）
> - 采样到的 token 与采样参数中指定的任何 `stop_token_ids` 匹配
> - 输出中出现停止字符串（stop strings）——我们会在第一个停止字符串出现处截断输出，并在引擎中中止该请求（注意 `stop_token_ids` 会出现在输出中，而停止字符串不会）。

![](https://vllm.ai/blog-assets/figures/2025-vllm-anatomy/engine_loop.png)
**图 2**：引擎循环

> **注意：** 在流式模式下，我们会在 token 生成的同时就把中间 token 发送出去，这里暂时忽略这一点。

接下来，我们更详细地看看调度。

### 调度器

推理引擎处理的工作负载主要有两类：

1. **预填充（Prefill）**请求——对所有提示 token 做一次前向传播。这类请求通常是**计算受限（compute-bound）**的（阈值取决于硬件和提示长度）。结束时，我们从最终 token 位置的概率分布中采样一个 token。
2. **解码（Decode）**请求——只对最近一个 token 做前向传播。所有更早的 KV 向量都已缓存。这类请求是**内存带宽受限（memory-bandwidth-bound）**的，因为即使只为计算一个 token，我们仍需要加载所有 LLM 权重（以及 KV 缓存）。

> **注意：** 在[基准测试部分](#benchmarks-and-auto-tuning---latency-vs-throughput)中我们会分析 GPU 性能的所谓屋顶线（roofline）模型。那里会进一步讲解预填充/解码的性能特征。

得益于更聪明的设计选择，V1 调度器可以在同一步骤中混合处理两类请求。相比之下，V0 引擎一次只能处理预填充或解码中的一种。

调度器优先处理解码请求——即已经在 `running` 队列中的那些。对每个这样的请求，它：

1. 计算要生成的新 token 数（由于投机解码和异步调度，并不总是 1——稍后详述）。
2. 调用 KV 缓存管理器的 `allocate_slots` 函数（细节见下）。
3. 用第 1 步中的 token 数扣减 token 预算。

之后，它处理 `waiting` 队列中的预填充请求，对每个请求：

1. 获取已计算块的数量（若禁用前缀缓存则返回 0——稍后介绍）。
2. 调用 KV 缓存管理器的 `allocate_slots` 函数。
3. 把请求从 waiting 弹出并移入 running，把其状态设为 `RUNNING`。
4. 更新 token 预算。

现在让我们看看 `allocate_slots` 做了什么：

1. **计算块数量**——确定需要分配多少个新的 KV 缓存块（`n`）。每个块默认存储 16 个 token。例如，如果一个预填充请求有 17 个新 token，我们需要 `ceil(17/16) = 2` 个块。
2. **检查可用性**——如果管理器池中的块不足，提前退出。根据是解码还是预填充请求，引擎可能尝试重计算抢占（recompute preemption，V0 还支持交换抢占 swap preemption），通过驱逐低优先级请求来实现（调用 `kv_cache_manager.free`，把 KV 块归还块池），也可能跳过调度并继续执行。
3. **分配块**——通过 KV 缓存管理器的协调器（coordinator），从块池（前面提到的 `free_block_queue` 双向链表）取出前 `n` 个块。存入 `req_to_blocks`，即把每个 `request_id` 映射到其 KV 缓存块列表的字典。

![](https://vllm.ai/blog-assets/figures/2025-vllm-anatomy/kv_cache_blocks.png)
**图 3**：KV 缓存块列表

我们终于准备好做前向传播了！

### 运行前向传播

我们调用模型执行器的 `execute_model`，它委托给 `Worker`，后者再委托给模型运行器（model runner）。

以下是主要步骤：

1. **更新状态**——从 `input_batch` 中剔除已完成的请求；更新其他与前向传播相关的元数据（例如每个请求将用于在分页 KV 缓存内存中索引的 KV 缓存块）。
2. **准备输入**——把缓冲区从 CPU 拷贝到 GPU；计算位置；构建 `slot_mapping`（在示例中详述）；构造注意力元数据。
3. **前向传播**——用自定义分页注意力内核运行模型。所有序列被摊平并拼接成一条长长的"超级序列"。位置索引和注意力掩码确保每个序列只关注自己的 token，这使得连续批处理无需右侧填充（right-padding）即可实现。
4. **收集末位 token 状态**——提取每个序列最后一个位置的隐藏状态并计算 logits。
5. **采样**——按采样配置（贪心、temperature、top-p、top-k 等）从计算得到的 logits 中采样 token。

前向传播步骤本身有两种执行模式：

1. **Eager 模式**——当启用了 eager 执行时，运行标准 PyTorch 前向传播。
2. **"已捕获"模式**——当未强制 eager 时，执行/重放预先捕获的 CUDA Graph（回忆一下，我们在引擎构造的初始化 KV 缓存流程中捕获了它们）。

下面这个具体例子应当能把连续批处理和分页注意力讲清楚：

![](https://vllm.ai/blog-assets/figures/2025-vllm-anatomy/fwd_pass.png)
**图 4**：前向传播：连续批处理与分页注意力

## 高级特性——扩展核心引擎逻辑

有了基本的引擎流程，我们现在可以看高级特性了。

我们已经讨论过抢占、分页注意力和连续批处理。

接下来，我们将深入：

1. 分块预填充
2. 前缀缓存
3. 引导解码（通过基于语法的有限状态机）
4. 投机解码
5. PD 分离（prefill/decode 分离）

### 分块预填充

分块预填充是一种处理长提示的技术：把它们的预填充步骤拆分成更小的块。没有它，一个非常长的请求可能独占一个引擎步骤，使其他预填充请求无法运行。这会推迟所有其他请求并增加它们的延迟。

举例来说，设每个块包含 `n`（=8）个 token，用小写字母表示并以 "-" 分隔。一个长提示 `P` 可能形如 `x-y-z`，其中 `z` 是一个不完整的块（例如 2 个 token）。对 `P` 执行完整预填充将需要 ≥ 3 个引擎步骤（如果它在某一步中未被调度执行，则会大于 3），而且只有在最后一个分块预填充步骤中才会采样出一个新 token。

下面是同一例子的可视化：

![](https://vllm.ai/blog-assets/figures/2025-vllm-anatomy/chunked_pt1.png)
**图 5**：分块预填充

实现很直接：限制每一步的新 token 数量。如果请求的数量超过 `long_prefill_token_threshold`，就把它重置为恰好该值。底层的索引逻辑（前面已描述）会处理其余部分。

在 vLLM V1 中，把 `long_prefill_token_threshold` 设为正整数即可启用分块预填充。（严格来说，即使不设置它也可能发生：如果提示长度超过 token 预算，我们会截断它并运行分块预填充。）

### 前缀缓存

为了解释前缀缓存的工作原理，我们对最初的代码示例稍作修改：

```
from vllm import LLM, SamplingParams

long_prefix = "<a piece of text that is encoded into more than block_size tokens>"

prompts = [
    "Hello, my name is",
    "The president of the United States is",
]

sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

def main():
    llm = LLM(model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

    outputs = llm.generate(long_prefix + prompts[0], sampling_params)
    outputs = llm.generate(long_prefix + prompts[1], sampling_params)

if __name__ == "__main__":
    main()
```

前缀缓存避免了对多个提示在开头共享的 token 的重复计算——故名**前缀**。

关键在于 `long_prefix`：它定义为任何长度超过一个 KV 缓存块（默认 16 个 token）的前缀。为简化例子，假设 `long_prefix` 的长度恰为 `n x block_size`（其中 `n ≥ 1`）。

> **注意：** 即它与块边界完美对齐——否则我们就得重新计算 `long_prefix_len % block_size` 个 token，因为不完整的块无法缓存。

没有前缀缓存时，每次处理带有相同 `long_prefix` 的新请求，我们都要重新计算全部 `n x block_size` 个 token。

有了前缀缓存，这些 token 只计算一次（其 KV 存入分页 KV 缓存内存）然后被复用，因此只需处理新的提示 token。这会加速预填充请求（对解码没有帮助）。

这在 vLLM 中是如何工作的？

在第一次 `generate` 调用时，在调度阶段，引擎在 `kv_cache_manager.get_computed_blocks` 内调用 `hash_request_tokens`：

1. 该函数把 `long_prefix + prompts[0]` 切分成 16 个 token 的块。
2. 对每个完整的块，计算一个哈希（使用内置 hash 或 SHA-256，后者更慢但冲突更少）。哈希组合了前一块的哈希、当前 token 以及可选元数据。

> **注意：** 可选元数据包括：MM 哈希、LoRA ID、缓存盐（cache salt）（注入第一个块的哈希中，确保只有带此缓存盐的请求能复用这些块）。

3. 每个结果存为一个 `BlockHash` 对象，同时包含哈希和它的 token ID。我们返回一个块哈希列表。

该列表存入 `self.req_to_block_hashes[request_id]`。

接着，引擎调用 `find_longest_cache_hit` 检查这些哈希是否已存在于 `cached_block_hash_to_block` 中。在第一个请求时，没有任何命中。

![](https://vllm.ai/blog-assets/figures/2025-vllm-anatomy/prefix_pt1.png)
**图 6**：前缀缓存——哈希函数

然后我们调用 `allocate_slots`，它调用 `coordinator.cache_blocks`，后者把新的 `BlockHash` 条目与已分配的 KV 块关联起来，并记录到 `cached_block_hash_to_block` 中。

之后，前向传播会填充与上面分配的 KV 缓存块相对应的分页 KV 缓存内存中的 KV。

> **注意：** 经过许多引擎步骤后，它会分配更多 KV 缓存块，但这对我们的例子无关紧要，因为前缀在 `long_prefix` 之后立即分叉了。

![](https://vllm.ai/blog-assets/figures/2025-vllm-anatomy/prefix_pt2.png)
**图 7**：前缀缓存——在分页内存中填充 KV

当带着相同前缀的第二次 `generate` 调用发生时，步骤 1-3 重复，但这次 `find_longest_cache_hit`（通过线性搜索）为全部 `n` 个块找到匹配。引擎可以直接复用这些 KV 块。

![](https://vllm.ai/blog-assets/figures/2025-vllm-anatomy/prefix_pt3.png)
**图 8**：前缀缓存——复用 KV

如果原始请求仍然存活，这些块的引用计数会递增（例如到 2）。在这个例子中，第一个请求已经完成，所以块已被释放回池中，引用计数重置为 0。由于我们能够从 `cached_block_hash_to_block` 中取回它们，我们知道它们是有效的（KV 缓存管理器的逻辑就是这样设计的），所以只需再次把它们从 `free_block_queue` 中移除。

> [!NOTE] 进阶说明：
> KV 缓存块只有在即将从 `free_block_queue`（从左侧弹出）重新分配、而我们发现该块仍关联着一个哈希且存在于 `cached_block_hash_to_block` 中的那一刻才会失效。此时，我们会清除该块的哈希并从 `cached_block_hash_to_block` 中删除其条目，确保它不能再通过前缀缓存被复用（至少不能再为那个旧前缀所用）。

这就是前缀缓存的要义：不要重新计算你已经见过的前缀——直接复用它们的 KV 缓存！

如果你理解了这个例子，你也就理解了分页注意力是如何工作的。

前缀缓存默认启用。要禁用它：`enable_prefix_caching = False`。

### 引导解码（FSM）

引导解码是这样一种技术：在每个解码步骤，logits 都被一个基于语法的有限状态机约束。这确保只有语法允许的 token 才能被采样。

这是一个强大的机制：你可以强制执行从正则语法（乔姆斯基 3 型，例如任意正则表达式模式）一直到上下文无关语法（2 型，涵盖大多数编程语言）的任何东西。

为了让它不那么抽象，让我们从最简单的例子开始，基于之前的代码：

```
from vllm import LLM, SamplingParams
from vllm.sampling_params import GuidedDecodingParams

prompts = [
    "This sucks",
    "The weather is beautiful",
]

guided_decoding_params = GuidedDecodingParams(choice=["Positive", "Negative"])
sampling_params = SamplingParams(guided_decoding=guided_decoding_params)

def main():
    llm = LLM(model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

    outputs = llm.generate(prompts, sampling_params)

if __name__ == "__main__":
    main()
```

在我给出的玩具示例中（假设字符级分词）：在预填充时，FSM 掩蔽 logits，使只有 "P" 或 "N" 可选。如果采样到 "P"，FSM 进入 "Positive" 分支；下一步只允许 "o"，依此类推。

![](https://vllm.ai/blog-assets/figures/2025-vllm-anatomy/fsm.png)
**图 9**：玩具示例 FSM

它在 vLLM 中是如何工作的：

1. 在 LLM 引擎构造时，创建一个 `StructuredOutputManager`；它可以访问分词器，并维护一个 `_grammar_bitmask` 张量。
2. 添加请求时，其状态被设为 `WAITING_FOR_FSM`，`grammar_init` 选择后端编译器（例如 `xgrammar` [[7]](#ref-7)；注意后端是第三方代码）。
3. 该请求的语法被异步编译。
4. 调度期间，如果异步编译已完成，状态切换为 `WAITING`，`request_id` 被加入 `structured_output_request_ids`；否则它被放入 `skipped_waiting_requests`，在下一个引擎步骤重试。
5. 调度循环之后（仍在调度内部），如果有 FSM 请求，`StructuredOutputManager` 让后端准备/更新 `_grammar_bitmask`。
6. 前向传播产生 logits 之后，xgr\_torch\_compile 的函数把位掩码扩展到词表大小（32 倍扩展率，因为我们使用 32 位整数），并把不允许的 logits 掩为 –∞。
7. 采样出下一个 token 后，通过 `accept_tokens` 推进该请求的 FSM。形象地说，我们在 FSM 图上移动到下一个状态。

第 6 步值得进一步澄清。

如果 `vocab_size = 32`，`_grammar_bitmask` 是一个整数；它的二进制表示编码了哪些 token 被允许（"1"）与不允许（"0"）。例如，"101…001" 扩展成长度 32 的数组 `[1, 0, 1, ..., 0, 0, 1]`；为 0 的位置的 logits 被设为 –∞。对更大的词表，则使用多个 32 位字并相应地扩展/拼接。后端（例如 `xgrammar`）负责用当前 FSM 状态产生这些比特模式。

> **注意：** 这里大部分复杂性都隐藏在 xgrammar 之类的第三方库里。

下面是一个更简单的例子，vocab\_size = 8，使用 8 位整数（送给喜欢我的图示的读者）：

![](https://vllm.ai/blog-assets/figures/2025-vllm-anatomy/fsm2.png)
**图 10**：玩具示例

在 vLLM 中传入所需的 `guided_decoding` 配置即可启用它。

### 投机解码

在自回归生成中，每个新 token 都需要对大模型做一次前向传播。这很昂贵——每一步都要重新加载并应用所有模型权重，只为计算一个 token！（假设批大小 == 1，一般情况下是 `B`）

投机解码 [[8]](#ref-8) 通过引入一个更小的草稿模型来加速。草稿模型廉价地提出 `k` 个 token。但我们最终并不想从更小的模型采样——它只是用来猜测候选续写的。大模型依然决定什么是有效的。

步骤如下：

1. **草稿（Draft）**：在当前上下文上运行小模型，提出 `k` 个 token
2. **验证（Verify）**：在上下文 + `k` 个草稿 token 上运行一次大模型。这会为那 `k` 个位置各产生一个概率，外加一个额外的（因此我们得到 `k+1` 个候选）
3. **接受/拒绝（Accept/reject）**：从左到右遍历 `k` 个草稿 token：

- 如果大模型对草稿 token 的概率 ≥ 草稿模型的概率，接受它
- 否则，以概率 `p_large(token)/p_draft(token)` 接受它
- 在第一个拒绝处停止，或接受全部 `k` 个草稿 token

- 如果全部 `k` 个草稿 token 都被接受，还从大模型"免费"采样出额外的第 `(k+1)` 个 token（那个分布我们已经算好了）
- 如果发生了拒绝，就在该位置构造一个新的重新配平的分布（`p_large - p_draft`，最小值截为 0，归一化为和为 1），并从中采样最后一个 token

**为什么这是对的**：虽然我们用小模型提出候选，但接受/拒绝规则保证了在期望意义上，序列的分布与逐 token 从大模型采样完全一致。这意味着投机解码在统计上等价于标准自回归解码——但可能快得多，因为一次大模型前向可以产出多达 `k+1` 个 token。

> **注意：** 我推荐看 [gpt-fast](https://github.com/meta-pytorch/gpt-fast) 的简单实现，以及[原始论文](https://arxiv.org/abs/2302.01318)的数学细节和与从完整模型采样等价的证明。

vLLM V1 不支持 LLM 草稿模型方法，而是实现了更快但较不精确的提议方案：n-gram、EAGLE [[9]](#ref-9) 与 Medusa [[10]](#ref-10)。

各自一句话简介：

- **n-gram**：取最后 `prompt_lookup_max` 个 token；在序列中寻找此前的匹配；若找到，提出该匹配之后的 `k` 个 token；否则缩小窗口并重试，下限为 `prompt_lookup_min`

> **注意：** 当前实现在第一次匹配后返回 `k` 个 token。引入"越近越好"的偏好、反转搜索方向（即取最后一次匹配）会不会更自然？

- **Eagle**：对大模型做"模型手术"——保留 embedding 和 LM head，把 transformer 栈替换为一个轻量 MLP；把它微调为廉价的草稿模型
- **Medusa**：在大模型之上（LM head 之前的 embeddings）训练辅助线性头，并行预测接下来的 `k` 个 token；用这些头比运行一个独立小模型更高效地提出 token

下面是如何在 vLLM 中以 `ngram` 作为草稿方法调用投机解码：

```
from vllm import LLM, SamplingParams

prompts = [
    "Hello, my name is",
    "The president of the United States is",
]

sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

speculative_config={
    "method": "ngram",
    "prompt_lookup_max": 5,
    "prompt_lookup_min": 3,
    "num_speculative_tokens": 3,
}

def main():
    llm = LLM(model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", speculative_config=speculative_config)

    outputs = llm.generate(prompts, sampling_params)

if __name__ == "__main__":
    main()
```

它在 vLLM 中如何工作？

**准备（引擎构造期间）：**

1. 初始化设备：创建一个 `drafter`（草稿模型，例如 `NgramProposer`）和一个 `rejection_sampler`（其部分代码用 Triton 编写）。
2. 加载模型：加载草稿模型权重（对 n-gram 而言是空操作）。

**此后在 `generate` 函数中**（假设我们收到一个全新的请求）：

1. 用大模型运行常规的预填充步骤。
2. 前向传播和标准采样之后，调用 `propose_draft_token_ids(k)` 从草稿模型采样 `k` 个草稿 token。
3. 把它们存入 `request.spec_token_ids`（更新请求元数据）。
4. 在下一个引擎步骤，当请求位于 running 队列时，把 `len(request.spec_token_ids)` 加入"新 token"计数，使 `allocate_slots` 为前向传播预留足够的 KV 块。
5. 把 `spec_token_ids` 拷贝进 `input_batch.token_ids_cpu`，构成（上下文 + 草稿）token。
6. 通过 `_calc_spec_decode_metadata` 计算元数据（它从 `input_batch.token_ids_cpu` 拷贝 token、准备 logits 等），然后对草稿 token 运行一次大模型前向传播。
7. 不做常规的 logits 采样，而是使用 `rejection_sampler` 从左到右接受/拒绝，产出 `output_token_ids`。
8. 重复步骤 2-7，直到满足停止条件。

内化这些内容的最佳方式是打开调试器单步调试代码库，但这一节希望能让你先尝尝味道。还有这个：

![](https://vllm.ai/blog-assets/figures/2025-vllm-anatomy/specdec_pt1.png)

![](https://vllm.ai/blog-assets/figures/2025-vllm-anatomy/specdec_pt2.png)
**图 11**：投机解码

### PD 分离（Disaggregated P/D）

我在前面已经暗示过 PD 分离（prefill/decode 分离）背后的动机。

预填充和解码的性能特征截然不同（计算受限 vs 内存带宽受限），因此把它们的执行分开是一个合理的设计。它提供了对延迟更精细的控制——包括 `TFTT`（time-to-first-token，首 token 时间）和 `ITL`（inter-token latency，逐 token 延迟）——详见[基准测试](#benchmarks-and-auto-tuning---latency-vs-throughput)部分。

在实践中，我们运行 `N` 个 vLLM 预填充实例和 `M` 个 vLLM 解码实例，并根据实时请求构成对它们自动伸缩。预填充 worker 把 KV 写入专用的 KV 缓存服务；解码 worker 从中读取。这把漫长而突发性的预填充与平稳、延迟敏感的解码隔离开来。

这在 vLLM 中如何工作？

为清楚起见，下面的例子使用 `SharedStorageConnector`，一个用于说明机制的调试用连接器实现。

> **注意：** Connector（连接器）是 vLLM 处理实例间 KV 交换的抽象。Connector 接口尚未稳定，近期有一些计划中的改进会带来变更，其中一些可能是破坏性的。

我们启动 2 个 vLLM 实例（GPU 0 用于预填充，GPU 1 用于解码），然后在它们之间传输 KV 缓存：

```
import os
import time
from multiprocessing import Event, Process
import multiprocessing as mp

from vllm import LLM, SamplingParams
from vllm.config import KVTransferConfig

prompts = [
    "Hello, my name is",
    "The president of the United States is",
]

def run_prefill(prefill_done):
  os.environ["CUDA_VISIBLE_DEVICES"] = "0"

  sampling_params = SamplingParams(temperature=0, top_p=0.95, max_tokens=1)

  ktc=KVTransferConfig(
      kv_connector="SharedStorageConnector",
      kv_role="kv_both",
      kv_connector_extra_config={"shared_storage_path": "local_storage"},
  )

  llm = LLM(model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", kv_transfer_config=ktc)
  llm.generate(prompts, sampling_params)

  prefill_done.set()  # notify decode instance that KV cache is ready

  # To keep the prefill node running in case the decode node is not done;
  # otherwise, the script might exit prematurely, causing incomplete decoding.
  try:
      while True:
          time.sleep(1)
  except KeyboardInterrupt:
      print("Script stopped by user.")

def run_decode(prefill_done):
  os.environ["CUDA_VISIBLE_DEVICES"] = "1"

  sampling_params = SamplingParams(temperature=0, top_p=0.95)

  ktc=KVTransferConfig(
      kv_connector="SharedStorageConnector",
      kv_role="kv_both",
      kv_connector_extra_config={"shared_storage_path": "local_storage"},
  )

  llm = LLM(model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", kv_transfer_config=ktc)

  prefill_done.wait()  # block waiting for KV cache from prefill instance

  # Internally it'll first fetch KV cache before starting the decoding loop
  outputs = llm.generate(prompts, sampling_params)

if __name__ == "__main__":
  prefill_done = Event()
  prefill_process = Process(target=run_prefill, args=(prefill_done,))
  decode_process = Process(target=run_decode, args=(prefill_done,))

  prefill_process.start()
  decode_process.start()

  decode_process.join()
  prefill_process.terminate()
```

> **注意：** 我也试验过 `LMCache` [[11]](#ref-11)，这是最快的生产级连接器（使用 NVIDIA 的 NIXL 作为后端），但它仍处于最前沿，我遇到了一些 bug。由于它的复杂性大部分位于外部仓库中，`SharedStorageConnector` 更适合用来讲解。

以下是 vLLM 中的步骤：

1. **实例化**——在引擎构造期间，连接器在两处被创建：

- 在 worker 的初始化设备流程中（init worker distributed environment 函数内），角色为 "worker"。
- 在调度器构造函数中，角色为 "scheduler"。

2. **缓存查找**——当调度器处理 `waiting` 队列中的预填充请求时（在本地前缀缓存检查之后），它会调用连接器的 `get_num_new_matched_tokens`。这会检查 KV 缓存服务器中是否存在外部缓存的 token。预填充在这里总是看到 0；解码可能有缓存命中。结果会在调用 `allocate_slots` 之前加到本地计数上。
3. **状态更新**——调度器随后调用 `connector.update_state_after_alloc`，记录发生缓存命中的请求（对预填充是空操作）。
4. **构建元数据对象**——调度结束时，调度器调用 `meta = connector.build_connector_meta`：

- 预填充把所有请求以 `is_store=True` 加入（用于上传 KV）。
- 解码把请求以 `is_store=False` 加入（用于获取 KV）。

5. **上下文管理器**——前向传播之前，引擎进入一个 KV 连接器上下文管理器：

- 进入时：调用 `kv_connector.start_load_kv`。对解码而言，这会从外部服务器加载 KV 并注入分页内存。对预填充，它是空操作。
- 退出时：调用 `kv_connector.wait_for_save`。对预填充而言，它会阻塞直到 KV 上传到外部服务器。对解码，它是空操作。

下面是一个可视化示例：

![](https://vllm.ai/blog-assets/figures/2025-vllm-anatomy/pd.png)
**图 12**：PD 分离

> [!NOTE] 补充说明：
>
> - 对 `SharedStorageConnector` 来说，"外部服务器"只是一个本地文件系统。
> - 根据配置，KV 传输也可以逐层进行（每个注意力层之前/之后）。
> - 解码只在其请求的第一步加载外部 KV；之后它在本地计算/存储。

## 从 UniprocExecutor 到 MultiProcExecutor

核心技术就位后，我们现在可以谈谈纵向扩展了。

假设你的模型权重已经塞不进单个 GPU 的显存。

第一种选择是用张量并行把模型分片到同一节点的多个 GPU 上（例如 `TP=8`）。如果模型还是放不下，下一步是跨节点的流水线并行。

> [!NOTE] 说明：
>
> - 节点内带宽显著高于节点间带宽，这就是张量并行（TP）通常优于流水线并行（PP）的原因。（PP 通信的数据量确实少于 TP。）
> - 我不涵盖专家并行（EP），因为我们聚焦标准 transformer 而非 MoE；也不涵盖序列并行，因为实践中 TP 和 PP 最常用。

到了这个阶段，我们需要多个 GPU 进程（worker）以及一个编排层来协调它们。这正是 `MultiProcExecutor` 所提供的。

![](https://vllm.ai/blog-assets/figures/2025-vllm-anatomy/multiprocexecutor.png)
**图 13**：TP=8 设置下的 MultiProcExecutor（driver worker 为 rank 0）

它在 vLLM 中如何工作：

1. `MultiProcExecutor` 初始化一个 `rpc_broadcast_mq` 消息队列（底层用共享内存实现）。
2. 构造函数遍历 `world_size`（例如 `TP=8 ⇒ world_size=8`），通过 `WorkerProc.make_worker_process` 为每个 rank 生成一个守护进程。
3. 对每个 worker，父进程先创建读管道和写管道。
4. 新进程运行 `WorkerProc.worker_main`，它实例化一个 worker（经历与 `UniprocExecutor` 相同的"初始化设备"、"加载模型"等流程）。
5. 每个 worker 判断自己是 driver（TP 组中的 rank 0）还是普通 worker。每个 worker 设置两个队列：

- `rpc_broadcast_mq`（与父进程共享）用于接收工作。
- `worker_response_mq` 用于回送响应。

6. 初始化期间，每个子进程通过管道把它的 `worker_response_mq` 句柄发给父进程。全部收到后，父进程解除阻塞——协调就此完成。
7. 然后 worker 进入忙碌循环，阻塞在 `rpc_broadcast_mq.dequeue` 上。当工作项到达时，它们执行它（就像 `UniprocExecutor` 一样，但现在带有 TP/PP 特定的分区工作）。结果通过 `worker_response_mq.enqueue` 送回。
8. 运行时，当请求到达时，`MultiProcExecutor` 把它（非阻塞地）放入 `rpc_broadcast_mq`，广播给所有子 worker。然后它在指定输出 rank 的 `worker_response_mq.dequeue` 上等待，收集最终结果。

从引擎的视角看，什么都没有变——所有这些多进程的复杂性都通过对模型执行器 `execute_model` 的一次调用被抽象掉了。

- 在 `UniProcExecutor` 的情况：execute\_model 直接导致在 worker 上调用 execute\_model
- 在 `MultiProcExecutor` 的情况：execute\_model 通过 `rpc_broadcast_mq` 间接导致在每个 worker 上调用 execute\_model

此时，我们可以用同一个引擎接口运行资源允许范围内任意大的模型。

下一步是横向扩展：启用数据并行（`DP > 1`）把模型复制到多个节点，添加一个轻量的 DP 协调层，引入跨副本的负载均衡，并在前面放置一个或多个 API 服务器来处理入站流量。

## 服务 vLLM 的分布式系统

搭建服务基础设施有很多方式，但为了具体起见，这里举一个例子：假设我们有两台 H100 节点，想在它们上面运行 4 个 vLLM 引擎。

如果模型需要 `TP=4`，我们可以像这样配置节点。

![](https://vllm.ai/blog-assets/figures/2025-vllm-anatomy/server_setup.png)
**图 14**：2 台 8xH100 节点的服务器配置（1 台 headless，1 台 API 服务器）

在第一台节点上，用以下参数以 headless 模式（无 API 服务器）运行引擎：

```
vllm serve <model-name>
  --tensor-parallel-size 4
  --data-parallel-size 4
  --data-parallel-size-local 2
  --data-parallel-start-rank 0
  --data-parallel-address <master-ip>
  --data-parallel-rpc-port 13345
  --headless
```

然后在另一台节点上运行同样的命令，稍作调整：

- 去掉 `--headless`
- 修改 DP 起始 rank

```
vllm serve <model-name>
  --tensor-parallel-size 4
  --data-parallel-size 4
  --data-parallel-size-local 2
  --data-parallel-start-rank 2
  --data-parallel-address <master-ip>
  --data-parallel-rpc-port 13345
```

> **注意：** 这里假设网络已配置好，所有节点都能访问指定的 IP 和端口。

这在 VLLM 中如何工作？

### 在 headless 服务器节点上

在 headless 节点上，`CoreEngineProcManager` 启动 2 个进程（按 `--data-parallel-size-local`），每个都运行 `EngineCoreProc.run_engine_core`。这些函数各自创建一个 `DPEngineCoreProc`（引擎核心），然后进入其忙碌循环。

`DPEngineCoreProc` 初始化其父类 `EngineCoreProc`（`EngineCore` 的子类），它会：

1. 创建 `input_queue` 和 `output_queue`（`queue.Queue`）。
2. 使用 `DEALER` ZMQ 套接字（异步消息库）与另一节点上的前端进行初始握手，并接收协调地址信息。
3. 初始化 DP 组（例如使用 NCCL 后端）。
4. 以 `MultiProcExecutor`（如前所述在 4 张 GPU 上 `TP=4`）初始化 `EngineCore`。
5. 创建 `ready_event`（`threading.Event`）。
6. 启动一个输入守护线程（`threading.Thread`）运行 `process_input_sockets(…, ready_event)`。类似地启动输出线程。
7. 仍在主线程中，等待 `ready_event`，直到跨 2 个节点的全部 4 个进程的所有输入线程完成协调握手，最终执行 `ready_event.set()`。
8. 解除阻塞后，向前端发送一条带元数据（例如分页 KV 缓存内存中可用的 `num_gpu_blocks`）的 "ready" 消息。
9. 主线程、输入线程和输出线程随后各自进入忙碌循环。

TL;DR：我们最终得到 4 个子进程（每个 DP 副本一个），每个运行主线程、输入线程和输出线程。它们与 DP 协调器和前端完成协调握手，然后每个进程的三个线程都进入稳态忙碌循环。

![](https://vllm.ai/blog-assets/figures/2025-vllm-anatomy/dpenginecoreproc.png)
**图 15**：运行 4 个 DPEngineCoreProc 的 4 个 DP 副本组成的分布式系统

**当前稳态**：

- **输入线程**——阻塞在输入套接字上，直到一个请求从 API 服务器路由过来；收到后，解码载荷，通过 `input_queue.put_nowait(...)` 入队一个工作项，然后回到套接字上阻塞。
- **主线程**——在 `input_queue.get(...)` 上醒来，把请求喂给引擎；`MultiProcExecutor` 运行前向传播并把结果入队到 `output_queue`。
- **输出线程**——在 `output_queue.get(...)` 上醒来，把结果送回 API 服务器，然后恢复阻塞。

**其他机制**：

- **DP 波次计数器**——系统追踪"波次"；当所有引擎空闲时它们静默（quiesce），新工作到达时计数器递增（对协调/指标有用）。
- **控制消息**——API 服务器可以发送的不只是推理请求（例如中止以及工具/控制 RPC）。
- **锁步 dummy 步骤**——如果任何一个 DP 副本有工作，所有副本都执行一个前向步骤；没有请求的副本执行 dummy 步骤以参与必需的同步点（避免阻塞活跃副本）。

> **注意：** 锁步澄清：这实际上只对 MoE 模型是必需的——MoE 模型的专家层构成 EP 或 TP 组而注意力层仍是 DP。目前 DP 时总是这样做——这只是因为"内置"的非 MoE DP 用处有限，因为你完全可以运行多个独立的 vLLM 并以常规方式在它们之间做负载均衡。

现在看第二部分：API 服务器节点上发生了什么？

### 在 API 服务器节点上

我们实例化一个 `AsyncLLM` 对象（LLM 引擎的 asyncio 包装器）。内部它会创建一个 `DPLBAsyncMPClient`（数据并行、负载均衡、异步、多进程客户端）。

在 `MPClient` 的父类中，`launch_core_engines` 函数运行并：

1. 创建用于启动握手的 ZMQ 地址（如 headless 节点上所见）。
2. 生成一个 `DPCoordinator` 进程。
3. 创建 `CoreEngineProcManager`（与 headless 节点上相同）。

在 `AsyncMPClient`（`MPClient` 的子类）中，我们：

1. 创建 `outputs_queue`（`asyncio.Queue`）。
2. 创建一个 asyncio 任务 `process_outputs_socket`，它（通过输出套接字）与全部 4 个 `DPEngineCoreProc` 的输出线程通信并写入 `outputs_queue`。
3. 随后，来自 `AsyncLLM` 的另一个 asyncio 任务 `output_handler` 从该队列读取，最终把信息发送给 `create_completion` 函数。

在 `DPAsyncMPClient` 中我们创建一个 asyncio 任务 `run_engine_stats_update_task`，它与 DP 协调器通信。

DP 协调器在前端（API 服务器）与后端（引擎核心）之间做中介。它：

- 周期性地把负载均衡信息（队列大小、waiting/running 请求）发送给前端的 `run_engine_stats_update_task`。
- 处理来自前端的 `SCALE_ELASTIC_EP` 命令，动态改变引擎数量（仅支持 Ray 后端）。
- 向后端发送 `START_DP_WAVE` 事件（由前端触发时），并把波次状态更新报告回来。

回顾一下，前端（`AsyncLLM`）运行着若干 asyncio 任务（记住：是并发，不是并行）：

- 一类任务通过 `generate` 路径处理输入请求（每个新的客户端请求会派生一个新的 asyncio 任务）。
- 两个任务（`process_outputs_socket`、`output_handler`）处理来自底层引擎的输出消息。
- 一个任务（`run_engine_stats_update_task`）维护与 DP 协调器的通信：发送波次触发、轮询 LB 状态、处理动态扩缩请求。

最后，主服务器进程创建一个 FastAPI 应用并挂载诸如 `OpenAIServingCompletion` 与 `OpenAIServingChat` 的端点，它们暴露 `/completion`、`/chat/completion` 等。整个技术栈随后通过 Uvicorn 提供服务。

把所有这些拼起来，就是完整的请求生命周期！

你在终端发送：

```
curl -X POST http://localhost:8000/v1/completions -H "Content-Type: application/json" -d '{
  "model": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
  "prompt": "The capital of France is",
  "max_tokens": 50,
  "temperature": 0.7
}'
```

接下来发生什么：

1. 请求命中 API 服务器上 `OpenAIServingCompletion` 的 `create_completion` 路由。
2. 该函数异步地对提示分词，并准备元数据（请求 ID、采样参数、时间戳等）。
3. 然后调用 `AsyncLLM.generate`，它遵循与同步引擎相同的流程，最终调用 `DPAsyncMPClient.add_request_async`。
4. 后者又调用 `get_core_engine_for_request`，它根据 DP 协调器的状态在引擎间做负载均衡（挑选分数最小 / 负载最低的那个：`score = len(waiting) * 4 + len(running)`）。
5. `ADD` 请求被发送到所选引擎的 `input_socket`。
6. 在该引擎上：

- 输入线程——解除阻塞，从输入套接字解码数据，把一个工作项放到 `input_queue` 上供主线程处理。
- 主线程——在 `input_queue` 上解除阻塞，把请求加入引擎，反复调用 `engine_core.step()`，把中间结果入队到 `output_queue`，直到满足停止条件。

> **注意：** 提醒：`step()` 会调用调度器、模型执行器（它又可以是 `MultiProcExecutor`！）等等。我们已经见过这些了！

- 输出线程——在 `output_queue` 上解除阻塞，通过输出套接字把结果送回。

7. 这些结果触发 `AsyncLLM` 的输出 asyncio 任务（`process_outputs_socket` 与 `output_handler`），它们把 token 传回 FastAPI 的 `create_completion` 路由。
8. FastAPI 附加元数据（finish reason、logprobs、用量信息等），通过 Uvicorn 返回 `JSONResponse` 到你的终端！

就这样，你的补全（completion）回来了——整个分布式机制都藏在一个简单的 `curl` 命令背后！:) 太有趣了！！！

> [!NOTE] 补充说明：
>
> - 当添加更多 API 服务器时，负载均衡在 OS/套接字层面处理。从应用的视角看，没有什么显著变化——复杂性被隐藏了。
> - 以 Ray 作为 DP 后端时，你可以暴露一个 URL 端点（`/scale_elastic_ep`），实现对引擎副本数量的自动扩缩。

## 基准测试与自动调优——延迟 vs 吞吐量

到目前为止，我们一直在分析"气体粒子"——请求在引擎/系统中流动的内部机制。现在是时候拉远视角，把系统当作整体来看，并追问：我们如何衡量一个推理系统的性能？

在最高层面，有两个相互竞争的指标：

1. **延迟**——从请求提交到返回 token 的时间
2. **吞吐量**——系统每秒能生成/处理的 token/请求数

**延迟**对交互式应用最重要，用户在那里等待响应。

**吞吐量**在离线工作负载中很重要，例如训练前/后的合成数据生成、数据清洗/处理，以及一般而言——任何类型的离线批量推理任务。

在解释延迟与吞吐量为何相互竞争之前，先定义几个常见的推理指标：

| 指标 | 定义 |
| --- | --- |
| `TTFT`（time to first token，首 token 时间） | 从请求提交到收到第一个输出 token 的时间 |
| `ITL`（inter-token latency，逐 token 延迟） | 两个连续 token 之间的时间（例如从 token i-1 到 token i） |
| `TPOT`（time per output token，每输出 token 时间） | 一个请求中所有输出 token 的平均 ITL |
| `Latency / E2E`（端到端延迟） | 处理一个请求的总时间，即 TTFT + 所有 ITL 之和，等价于提交请求与收到最后一个输出 token 之间的时间 |
| `Throughput`（吞吐量） | 每秒处理的 token 总数（输入、输出或两者），或每秒请求数 |
| `Goodput` | 满足服务级目标（SLO）的吞吐量，SLO 例如最大 TTFT、TPOT 或 e2e 延迟。例如，只有满足这些 SLO 的请求的 token 才被计入 |

![](https://vllm.ai/blog-assets/figures/2025-vllm-anatomy/latency_diagram.png)
**图 16**：ttft、itl、e2e 延迟

下面是一个解释这两个指标竞争本质的简化模型。

> [!NOTE] 假设：
> 权重 i/o（而非 KV 缓存 i/o）占主导；也就是说我们面对的是短序列。

观察批大小 `B` 如何影响单个解码步骤，这个权衡就清楚了。当 `B ↓` 趋向 1 时，ITL 下降：每一步的工作更少，token 不用与其他 token "竞争"。当 `B ↑` 趋向无穷时，ITL 上升，因为我们每步做更多 FLOPs——但吞吐量改善（直到达到峰值性能），因为权重 I/O 被摊销到更多 token 上。

屋顶线模型有助于理解这一点：在饱和批大小 `B_sat` 以下，步骤时间由 HBM 带宽主导（把权重逐层流入片上内存），因此步骤延迟几乎平坦——计算 1 个 token 和 10 个 token 耗时相近。超过 `B_sat` 后，内核变为计算受限，步骤时间大致随 `B` 增长；每多一个 token 都会增加 ITL。

![](https://vllm.ai/blog-assets/figures/2025-vllm-anatomy/roofline.png)
**图 17**：屋顶线性能模型

> [!NOTE] 注意：
> 要做更严谨的处理，我们必须考虑内核自动调优：随着 `B` 增长，运行时可能切换到对该形状更高效的内核，改变达到的性能 `P_kernel`。步骤延迟为 `t = FLOPs_step / P_kernel`，其中 `FLOPs_step` 是该步骤的工作量。可以看到，当 `P_kernel` 达到 `P_peak` 后，每步更多的计算将直接导致延迟上升。

### 如何在 vLLM 中做基准测试

vLLM 提供了 `vllm bench {serve,latency,throughput}` CLI，它包装了 vllm / benchmarks / {server,latency,throughput}.py。

这些脚本的功能：

- **latency**——使用短输入（默认 32 个 token），用小批次（默认 8）采样 128 个输出 token。它运行多轮迭代并报告该批次的 e2e 延迟。
- **throughput**——一次性提交固定的一组提示（默认：1000 条 ShareGPT 样本）（即 `QPS=Inf` 模式），并报告整个运行期间的输入/输出/总 token 数与每秒请求数。
- **serve**——启动一个 vLLM 服务器，并通过从泊松（或更一般地，伽马）分布采样请求到达间隔来模拟真实世界工作负载。它在一个时间窗口内发送请求，测量我们讨论过的所有指标，还可以选择性地强制服务端最大并发（通过信号量，例如把服务器限制在 64 个并发请求）。

下面是如何运行 latency 脚本的示例：

```
vllm bench latency
  --model <model-name>
  --input-tokens 32
  --output-tokens 128
  --batch-size 8
```

> **注意：** CI 中使用的基准测试配置位于 `.buildkite/nightly-benchmarks/tests`。

还有一个自动调优脚本，它驱动 serve 基准测试来找到满足目标 SLO 的参数设置（例如"在保持 p99 e2e < 500 ms 的同时最大化吞吐量"），并返回建议的配置。

## 结语

我们从基础的引擎核心（`UniprocExecutor`）开始，添加了投机解码和前缀缓存等高级特性，纵向扩展到 `MultiProcExecutor`（`TP/PP > 1`），最后横向扩展，把一切包裹进异步引擎与分布式服务技术栈——并以如何衡量系统性能作结。

vLLM 还包含一些我略过的专门处理。例如：

- **多样的硬件后端**：TPU、AWS Neuron（Trainium/Inferentia）等。
- **架构/技术**：`MLA`、`MoE`、编码器-解码器（例如 Whisper）、池化/嵌入模型、`EPLB`、`m-RoPE`、`LoRA`、`ALiBi`、无注意力变体、滑动窗口注意力、多模态 LM 以及状态空间模型（例如 Mamba/Mamba-2、Jamba）
- **TP/PP/SP**
- **混合 KV 缓存逻辑**（Jenga）、束采样等更复杂的采样方法，等等
- **实验性**：异步调度

好消息是，其中大部分与上述主流程正交——你几乎可以把它们当作"插件"来对待（实践中当然存在一些耦合）。

我热爱理解系统。话虽如此，在这个高度上分辨率确实受损了。在接下来的文章里，我会放大到特定子系统，深入细枝末节。

> [!NOTE] 联系方式：
> 如果你发现文中的任何错误，请私信我——欢迎通过 [X](https://x.com/gordic_aleksa)、[LinkedIn](https://www.linkedin.com/in/aleksagordic/) 或[匿名反馈](https://docs.google.com/forms/d/1z1fEirrN2xtGxAsJvptpM7yV4ByT5SF25S-XiMPrXNA)给我留言。

### 致谢

衷心感谢 [Hyperstack](https://www.hyperstack.cloud/) 在过去一年里为我的实验提供 H100！

感谢 [Nick Hill](https://www.linkedin.com/in/nickhillprofile/)（vLLM 核心贡献者，RedHat）、[Kaichao You](https://github.com/youkaichao)（vLLM 核心贡献者）、[Mark Saroufim](https://x.com/marksaroufim)（PyTorch）、[Kyle Krannen](https://www.linkedin.com/in/kyle-kranen/)（NVIDIA，Dynamo）以及 [Ashish Vaswani](https://www.linkedin.com/in/ashish-vaswani-99892181/) 阅读本文的预发布版本并提供反馈！

References

1. vLLM <https://github.com/vllm-project/vllm>
2. "Attention Is All You Need" <https://arxiv.org/abs/1706.03762>
3. "Efficient Memory Management for Large Language Model Serving with PagedAttention" <https://arxiv.org/abs/2309.06180>
4. "DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model" <https://arxiv.org/abs/2405.04434>
5. "Jenga: Effective Memory Management for Serving LLM with Heterogeneity" <https://arxiv.org/abs/2503.18292>
6. "Orca: A Distributed Serving System for Transformer-Based Generative Models" <https://www.usenix.org/conference/osdi22/presentation/yu>
7. "XGrammar: Flexible and Efficient Structured Generation Engine for Large Language Models" <https://arxiv.org/abs/2411.15100>
8. "Accelerating Large Language Model Decoding with Speculative Sampling" <https://arxiv.org/abs/2302.01318>
9. "EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty" <https://arxiv.org/abs/2401.15077>
10. "Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads" <https://arxiv.org/abs/2401.10774>
11. LMCache <https://github.com/LMCache/LMCache>
