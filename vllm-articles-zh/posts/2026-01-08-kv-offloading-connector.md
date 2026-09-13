---
title: "深入 vLLM 全新的 KV 卸载连接器：更智能的内存传输，最大化推理吞吐量"
title_en: "Inside vLLM’s New KV Offloading Connector: Smarter Memory Transfer for Maximizing Inference Throughput"
source: https://vllm.ai/blog/2026-01-08-kv-offloading-connector
crawled: 2026-09-12
translated: 2026-09-13
---

# 深入 vLLM 全新的 KV 卸载连接器：更智能的内存传输，最大化推理吞吐量

> 原文：[Inside vLLM’s New KV Offloading Connector: Smarter Memory Transfer for Maximizing Inference Throughput](https://vllm.ai/blog/2026-01-08-kv-offloading-connector) · vLLM 博客

作者：Or Ozeri、Danny Harnik（IBM Research vLLM 团队）

[#性能](https://vllm.ai/blog/tags/performance)

在本文中，我们将介绍 vLLM 0.11.0 中引入的全新 KV 缓存卸载功能。我们将重点讨论卸载到 CPU 内存（DRAM）及其对提升整体推理吞吐量的益处。在博客的第二部分，我们将深入探讨为优化 KV 卸载的主机到设备（host-to-device）与设备到主机（device-to-host）吞吐量所做的努力。

# 动机

服务 LLM 模型是一项计算复杂的操作，其核心涉及计算被称为 KV 数据的数据块。为用户的提示（prompt）生成响应的第一步，是计算与该提示对应的 KV 值。这一阶段在请求处理生命周期中被称为预填充（prefill）阶段。预填充阶段针对每个提示计算 KV 值，计算开销高昂，需要专用的加速硬件（如 GPU）才能快速完成。

为一个提示计算得到的 KV 值，可以被共享相同前缀的其他提示复用，从而免去重新计算。对许多用例而言，缓存并复用 KV 值因此可以带来两大主要收益：

- **改善请求延迟**（前提是从缓存读取快于重新计算 KV 数据）
- **提高单节点吞吐量**（GPU 核心上的负载得以降低，从而可以处理更多并发请求）

此外，**即使对于请求之间不共享任何共同前缀的工作负载，KV 缓存卸载同样有用**。具体而言，在处理大量并发请求时，GPU 可能会耗尽用于存储当前所处理请求集合所需 KV 值的空间。此时，推理引擎可能会抢占（preempt）一个正在运行的请求，将其 KV 值从 GPU 内存中丢弃。之后该请求会被重新调度处理，其 KV 值就需要重新计算。只要在请求被抢占之前将 KV 缓存卸载到更大的存储层（例如 CPU DRAM），就可以避免重新计算 KV 值的开销。

## CPU 卸载

在本文中，我们重点讨论向 CPU 内存（DRAM）的 KV 卸载。出于以下几个原因的组合，这一做法尤其值得关注：

- CPU RAM 在各类部署环境中普遍可用。
- 其容量通常超过 GPU 内存，可以容纳更大的 KV 缓存。
- CPU RAM 与 GPU 内存之间的传输具有低延迟、高吞吐的特点。
  结合上一点，这使 CPU 卸载成为**高效处理请求抢占的理想方案**。
- CPU RAM 还是向外部存储进一步卸载的**便利中转区**。
  在存储延迟较高的场景中，这一点尤其有益。

# 全新的卸载连接器

## vLLM 连接器 API

vLLM 很久以来就支持一个与请求生命周期集成的、用于读写 KV 数据的 API。该 API 被称为连接器 API（Connector API）。从较高层面看，vLLM 在处理任何请求之前都会查询该 API，从而允许从外部来源导入 KV 数据。在 KV 数据计算完成之后，vLLM 也会调用该 API，把新生成的 KV 值存储到外部目标上。

最初，连接器 API 是同步的。也就是说，当 vLLM 在外部加载/存储 KV 值时，vLLM 引擎会被阻塞，无法并行处理新的请求批次。vLLM 0.9.0 扩展了连接器 API，以支持**异步加载与存储 KV 数据**。卸载连接器正是利用这一新的异步 API 来实现 KV 缓存卸载。

我们推出**卸载连接器（offloading connector）**，它支持异步地卸载与加载 KV 数据。它暴露了一个可插拔的后端 API，允许使用任意介质进行卸载。该 API 简化了新增卸载后端的工作：你基本上只需定义一个传输函数，实现介质之间的 KV 数据拷贝即可。

卸载连接器附带一个 CPU 后端，使 vLLM 原生支持将 KV 数据卸载到 CPU。在本文的其余部分，我们将只聚焦于 CPU 卸载。

## 使用卸载连接器

要使用卸载连接器进行 CPU 卸载，只需在 `vllm serve` 命令中添加以下 CLI 标志：

```
--kv_offloading_backend native --kv_offloading_size <size_in_GB>

```

这一 CLI 依赖于该 [PR #24498](https://github.com/vllm-project/vllm/pull/24498)，预计会包含在 0.14.0 版本中。

对于较旧的版本，可以使用以下 CLI 启用 CPU 卸载：

```
--kv-transfer-config '{"kv_connector":"OffloadingConnector","kv_role":"kv_both","kv_connector_extra_config":{"num_cpu_blocks": <num_cpu_blocks>}}'

```

其中 num\_cpu\_blocks 是为 CPU KV 缓存分配的 CPU 块数量。

# 通过卸载连接器进行 CPU 卸载的收益

我们给出两个不同的微基准测试。第一个测量单个请求的首 token 延迟（TTFT），强调单请求服务的加速效果；第二个测量服务多个并发请求的系统吞吐量，展示卸载如何帮助应对更繁重的工作负载。

在第一个基准测试中，我们测量处理单个预填充请求的延迟，将 CPU 缓存加载与 GPU 计算 KV 值进行比较。

![](https://vllm.ai/blog-assets/figures/2026-01-08-kv-offloading-connector/figure1.png)
**图 1**：单请求 TTFT（Llama-3.1-8B-Instruct，NVIDIA H100）。

结果表明，**从 CPU 加载 KV 值可将 TTFT 缩短 X2-X22 倍**，具体取决于提示大小。基准测试的确切设置与代码见本文末尾。

需要注意的是，KV 卸载（将 KV 数据从 GPU 拷贝到 CPU）的延迟并不直接面向用户，也就是说它不应影响响应时间。这是因为卸载同样是异步完成的，用户请求无需等待这次传输完成即可结束。这意味着**对于缓存未命中的情况，使用卸载连接器对 TTFT 的影响极小**。

接下来，我们测试使用 CPU 卸载对处理多个并发请求时整体吞吐量的影响。这一测试实质上是提交一批 10000 个互不相同的请求（每个 512 token），并测量 CPU 缓存在不同命中率下取得的吞吐量。

我们测量处理这些请求所花的时间（不计 CPU 缓存预热时间），并据此推算出以 token/s 为单位的吞吐量。为了聚焦 CPU 缓存的效果，测试未使用 GPU 缓存。

![](https://vllm.ai/blog-assets/figures/2026-01-08-kv-offloading-connector/figure2.png)
**图 2**：并发请求吞吐量（Llama-3.1-8B-Instruct，NVIDIA H100，10000 个 512 token 的预填充请求）。

结果显示，吞吐量随 CPU KV 缓存命中率上升而提高。我们观察到**吞吐量最高提升 X9**，尽管该提示大小下 TTFT 仅缩短了 X2。这表明 **KV 缓存卸载的主要收益在于吞吐量最大化**。

## 卸载连接器在 vLLM 各版本中的表现

请注意，**卸载连接器的性能在 0.12.0 中得到了大幅改进**。例如，使用 Llama-3.1-8B-Instruct 与 NVIDIA H100 GPU 测试时，我们观察到 TTFT 最高缩短 **X4 倍**，吞吐量最高提升 **X5 倍**。我们将在讨论 vLLM 物理块大小的章节中展开介绍这一改进的细节。

即将发布的 0.14.0 版本有望带来进一步的改进，特别是：

- 支持被抢占的请求从 CPU 重新加载回来（[PR #29870](https://github.com/vllm-project/vllm/pull/29870)）
- 修复卸载与模型计算之间的一个竞态条件（[PR #31341](https://github.com/vllm-project/vllm/pull/31341)）

本文中的评估已包含这些改进。

# 评估 GPU-CPU 传输技术

在本文余下的部分，我们将从技术层面深入探讨设计 CPU 卸载时的一些考量。具体来说，我们展示旨在优化推理吞吐量的研究：在最大限度降低 GPU 与 CPU 核心开销的同时，最大化 GPU-CPU 之间的传输吞吐量。

如前所述，为卸载连接器定义后端时，主要组件就是**一个传输函数**。就 CPU 后端而言，该传输函数在 GPU 内存与 CPU 内存之间拷贝数据（反之亦然）。它目前**支持 CUDA 兼容设备**（NVIDIA 与 AMD）。

CPU 后端实现的传输函数使用 *cudaMemcpyAsync* 函数，该函数利用 GPU 上一个名为 DMA（直接内存访问）的硬件组件。这一组件专为设备（GPU）与主机内存之间的高吞吐数据传输而设计。此外，用 DMA 执行传输意味着对 CPU 与 GPU 核心的开销极小。由于我们的传输是相对于模型计算异步运行的，这一特性尤为重要。

DMA 在处理较大的物理连续拷贝时能提供最佳吞吐量。这意味着我们预期测量到的卸载性能会随 KV 数据布局而变化。KV 数据块更大的 LLM 模型会表现更好。

但 DMA 到底有多快？与使用定制 CUDA 内核等替代方案相比又如何？

为了回答这些问题，我们创建了微基准测试 [gpu\_cpu\_benchmark](https://github.com/orozery/playground/tree/kv-offloading-blog-dec-2025/kvcache/gpu_cpu_benchmark)。
在该基准测试中，我们测试了在 GPU 与 CPU 之间拷贝数据的两种方案：

- 使用 **DMA** 拷贝——通过 cudaMemcpyAsync。
- 使用**定制 CUDA 内核**拷贝，它利用 **GPU 核心**通过原始指针拷贝 16 字节的字。这种方案很有效，因为它利用了 GPU 核心提供的大规模并行性；但另一方面，它对 GPU 核心的主要任务造成的干扰也更大。

我们的第一个测试测量单次传输 1000 个块的吞吐量，块大小从 4KB 到 16MB 不等：

![](https://vllm.ai/blog-assets/figures/2026-01-08-kv-offloading-connector/figure3.png)
**图 3**：单次 GPU -> CPU 传输吞吐量（NVIDIA H100，单次传输 1000 个块）。

![](https://vllm.ai/blog-assets/figures/2026-01-08-kv-offloading-connector/figure4.png)
**图 4**：单次 CPU -> GPU 传输吞吐量（NVIDIA H100，单次传输 1000 个块）。

结果证实，**DMA 表现良好，但仅限于较大的块大小**。对于较小的块大小，定制内核取得了明显更好的吞吐量。不过我们要指出，定制内核的结果噪声更大，方差更高。

接下来我们测试双向传输吞吐量：同时发起两个并发传输，一个读、一个写。在这个测试中，我们将块大小固定为 2MB，并改变两个方向传输量之间的比例。对两种拷贝机制而言，当两个方向传输量大致相当时达到峰值吞吐量。不过，尽管单向传输两者都能达到约 50GB/s，双向传输的结果却有所不同：

- DMA 达到 83.4 GB/s
- 定制内核达到 68.5 GB/s

因此，要在两种方案之间做出选择，剩下的问题就是：

- **vLLM 实际使用的有效块大小是多少？**
  这取决于所服务的模型以及 vLLM 配置。下一节中，我们将针对当今一些常用模型回答这个问题。
- **两种方案对 GPU 模型计算性能有何影响？**
  回顾一下，卸载连接器的设计目标是在 GPU 执行模型计算的同时并行地卸载/加载 KV 数据。在评估中我们将看到每种方案对整体吞吐量的影响。

# 改变 vLLM 的内存布局

在本节中，我们将介绍我们对 vLLM 中 GPU 内存布局所做的改动，使其成为更能支持 KV 传输的格式（同时不损害计算速度）。

我们首先描述 vLLM 为其 KV 缓存使用的默认内存布局，弄清在卸载 KV 数据时需要在 GPU 与 CPU 之间拷贝的碎片大小。这决定了在 vLLM 中传输 KV 数据的有效物理块大小。

vLLM 按 token 块分配 GPU 内存，默认每块 16 个 token。实际的物理布局取决于所使用的注意力后端（如 FlashAttention、FlashInfer 等）以及所服务的模型。当今最常见的模型是均匀模型（uniform model），由多个层组成，每层拥有自己的 KV 缓存但形状相同。vLLM 也支持混合模型（hybrid model），这类模型目前尚未针对卸载连接器做优化。对于均匀模型，vLLM 为每一层分配各自的 KV 缓存，因此单个逻辑块的 KV 缓存会被碎片化为 num\_layers 个块，每层一个。此外，取决于注意力后端，每层的块还可能进一步被拆分为 2 个子块，一个对应 K（键缓存），一个对应 V（值缓存）。

这种碎片化对模型计算性能没有影响，但对 KV 卸载却是致命的，因为它在 KV 缓存布局中造成了不必要的碎片，使有效块变小。为解决这个问题，我们最近向上游[提交](https://github.com/vllm-project/vllm/pull/27743)了一项对 vLLM KV 缓存布局的修改，创建出一个包含所有层 KV 数据的连续物理块。这一改动有效地把物理块大小提高了 2\*num\_layers 倍，进而**将卸载连接器的吞吐量提升了一个数量级**。

下表总结了当今一些常用模型，比较旧版（0.11.0）与新版（0.12.0）的物理块大小（假设 vLLM 使用 16 token 的块）。

| 模型 | 旧块大小 | 新块大小 |
| --- | --- | --- |
| deepseek-ai/DeepSeek-R1-Distill-Qwen-32B (tensor\_parallel\_size=2) | 16 KB | 2 MB |
| deepseek-ai/DeepSeek-V2-Lite-Chat (GPU block size=64) | 72 KB | 1.9 MB |
| meta-llama/Llama-3.1-8B-Instruct | 32 KB | 2 MB |
| meta-llama/Llama-3.2-1B-Instruct | 16 KB | 0.5 MB |
| meta-llama/Llama-3.1-70B-Instruct | 8 KB | 1.25 MB |
| mistralai/Mistral-7B-Instruct-v0.2 | 32 KB | 2 MB |
| mistralai/Mistral-Small-24B-Instruct-2501 | 32 KB | 2.5 MB |
| Qwen/Qwen2.5-3B-Instruct | 8 KB | 0.56 MB |
| Qwen/Qwen3-0.6B | 32 KB | 1.75 MB |
| Qwen/Qwen2.5-7B-Instruct | 16 KB | 0.87 MB |
| Qwen/Qwen3-4B-Instruct-2507 | 32 KB | 2.25 MB |
| Qwen/Qwen2.5-1.5B-Instruct | 8 KB | 0.44 MB |
| Qwen/Qwen3-8B | 28 KB | 1.97 MB |
| Qwen/Qwen3-1.7B | 32 KB | 1.75 MB |
| Qwen/Qwen3-32B (tensor\_parallel\_size=2) | 16 KB | 2 MB |

可以看到，新的 vLLM KV 缓存布局使物理块大小达到约 0.5-2 MB，而旧布局中只有几 KB。结合我们从 GPU-CPU 微基准测试中得到的数字，我们预期 **DMA 方案的性能与定制内核方案相当**，或略逊一筹（取决于模型）。

# 拷贝方法的端到端评估

在下一节中，我们使用这两个 vLLM 微基准测试来比较卸载连接器的两个变体：

- 上游版本，使用基于 DMA 的传输函数
- 补丁版本，使用我们 GPU-CPU 微基准测试中的定制内核

我们特意选择展示**卸载连接器最坏情形**下的结果，即使用物理块相对较小（0.5 MB）的模型。

![](https://vllm.ai/blog-assets/figures/2026-01-08-kv-offloading-connector/figure5.png)
**图 5**：单请求 TTFT（Llama-3.2-1B-Instruct，NVIDIA H100）。

在单请求基准测试中，我们看到**定制内核带来了稍好的 TTFT**：对 1K 提示的差异不足 1ms，对 90K 的大提示差异最高达 15ms。鉴于 GPU-CPU 微基准测试中 0.5 MB 块大小的结果，这些结果在预期之内。对于块大小更大的模型，两个变体的结果大致相同。

![](https://vllm.ai/blog-assets/figures/2026-01-08-kv-offloading-connector/figure6.png)
**图 6**：并发请求吞吐量（Llama-3.2-1B-Instruct，NVIDIA H100，10000 个 512 token 的预填充请求）。

然而，在并发请求测试中，我们看到 **DMA 取得了比定制内核更好的吞吐量**。增益从 0 命中率时的约 5.5% 开始，到 80% 命中率的测量点增加到约 15%。

这些结果的原因在于，定制内核方案会干扰模型计算，因为两者都要使用 GPU 核心。在 0% 命中率下，定制内核方案的吞吐量实际上比完全不使用 CPU 卸载还要差 6%。在 100% 命中率下，没有模型计算与 CPU 加载并行进行，因此两种方案之间的差距缩小。

我们要强调，我们展示的是对 DMA 方案而言最坏情形模型的结果。最常见的模型物理块更大，因而更加偏向 DMA。以 **Llama-3.1-8B-Instruct** 为例，DMA 在 TTFT 与定制内核持平的同时，吞吐量最高多出 **32%**。

总而言之，我们看到我们对 GPU 内存布局的改动使我们能够利用 DMA 进行 KV 传输，从而实现更好的整体吞吐量。

# 评估设置与基准测试代码

为评估 vLLM 的 CPU 卸载，我们使用了以下设置：

- 单个 Ubuntu 24.04.1 LTS 容器
- 内核 5.14.0-427.81.1.el9\_4.x86\_64
- Intel Xeon SapphireRapids 2.1Ghz（8 核上限）
- NVIDIA H100 80GB HBM3
- 500GB DRAM
- CUDA 版本：12.9
- vLLM commit 哈希 2a1776b7ac4fae7c50c694edeafc1b14270e4350
- Flash Attention 后端
- 禁用 GPU 前缀缓存（以便评估 CPU 命中）
- GPU 块大小 16 token
- CPU 块大小 16 token
- 禁用分词/反分词

我们的基准测试代码可在[这里](https://github.com/orozery/playground/blob/kv-offloading-blog-dec-2025/kvcache/kv_offload_benchmark.py)找到。

## 下一步是什么？

我们将继续增强 vLLM 的原生 KV 卸载功能。我们的下一个里程碑是让 CPU KV 缓存充当存储卸载的中间层。

与往常一样，我们的首要任务仍是正确性与性能。我们邀请你试用它、分享你的结果，并在遇到任何问题时告诉我们。

**参与讨论**：在 [vLLM Slack](https://vllm-dev.slack.com/archives/C09AYJFFLKD) 的 #feat-v1-cpu-offloading 频道分享你的用例与反馈。
