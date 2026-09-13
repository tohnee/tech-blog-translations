---
title: "Netpreme X-Mem™ MPU 加速 SGLang HiCache"
title_en: "Accelerating SGLang HiCache with Netpreme X-Mem™ MPU"
author: "Netpreme Team"
date: "July 8, 2026"
previewImg: /images/blog/netpreme-xmem/figure1.png
source: https://lmsys.org/blog/2026-06-27-netpreme-xmem/
translated: 2026-09-12
---

# Netpreme X-Mem™ MPU 加速 SGLang HiCache

> 原文：[Accelerating SGLang HiCache with Netpreme X-Mem™ MPU](https://lmsys.org/blog/2026-06-27-netpreme-xmem/) · LMSYS Blog · Netpreme Team

> Netpreme X-Mem™ 内存处理单元（MPU，Memory Processing Unit）通过在较慢的主机 DRAM 卸载层之外增加一个专门构建的高带宽 KV 内存层，使 SGLang HiCache 更快、更具扩展性。

![Figure 1](/images/blog/netpreme-xmem/figure1.png)

## TL;DR

- 对长上下文、智能体式（agentic）和推荐类 LLM 负载而言，前缀缓存正变得至关重要。
- SGLang HiCache 将 RadixAttention 扩展为覆盖 HBM、主机 DRAM 和外部存储的分层 KV 缓存，为可扩展的前缀复用提供了软件基础。
- Netpreme X-Mem™ 以专用 TB/s 级 KV 内存层的身份与 SGLang HiCache 集成。
- 在前缀密集型负载上，相比基于主机 DRAM 的 SGLang HiCache，Netpreme X-Mem™ 将首 token 延迟（TTFT，Time-to-First-Token）改善了 **6.7×**。

## 为什么前缀缓存需要一个快速内存层

前缀缓存旨在为这样一类负载减少代价高昂的预填充（prefill）计算：请求反复共享长且 token 完全相同的提示词，只在末尾很短的部分有所不同。SGLang 已经凭借 **RadixAttention** 和 **HiCache** 为前缀复用打下了坚实的软件基础。RadixAttention 实现了 GPU 内存中高效的前缀缓存，而 HiCache 则将其扩展为超越 GPU HBM 的层次化体系。

然而，随着 GPU 变得越来越快，将 KV 缓存加载进 HBM 的速度也变得重要起来。为了估算 KV 缓存卸载所需的带宽，我们对一个长上下文编程智能体负载进行建模：提示词长 64K token，预填充并发度为 8。随着前缀命中率上升，剩余计算量迅速下降，但从次级内存取回的 KV 数据量却在增长。当命中率超过 95% 时，扩展 KV 缓存分层的带宽能显著降低 TTFT！

![Figure 2](/images/blog/netpreme-xmem/figure2.png)

但 95% 的前缀缓存命中率真的现实吗？让我们看看编程智能体中的 KV 缓存复用——编程智能体是当前 AI 应用最大的市场。

为了量化这一点，我们[测量](https://github.com/netpreme/coding_agents)了在 [SWE-bench](https://github.com/SWE-bench/SWE-bench) 上运行多轮编程工作流时、从 [Claude Code 智能体](https://code.claude.com/docs/en/overview)收集的 trace 中的前缀缓存命中率。我们观察到，同一会话在后续轮次中的缓存命中率持续超过 95%，平均命中率约为 98%。在这种情形下，将 KV 缓存带宽扩展到超出主机 CPU 卸载所能达到的水平，可带来 3× 的性能提升！

![Figure 3](/images/blog/netpreme-xmem/figure3.png)

这正是 Netpreme X-Mem™ 的用武之地！

## Netpreme X-Mem™：SGLang HiCache 的专用 KV 层

Netpreme X-Mem™ MPU 是一个专门构建的解决方案，可通过高速网络互连将 GPU 内存扩展数十 TB。从概念上讲，X-Mem™ 是 AI 机架中的一个专用内存节点，与机架内所有其他 GPU 点对点直连。单个内存节点最多可提供 24 TB 内存，同一机架内的所有 GPU 都能以 4 TB/s 的带宽访问它。机架内可部署的内存节点数量没有上限，使用多个 MPU 节点时聚合带宽还会成倍增加。在软件层面，X-Mem™ 的地址空间作为统一虚拟内存的一部分对外暴露，在语义上与访问本地 HBM 或远端 GPU 的内存没有任何区别。

在与 SGLang HiCache 集成时，Netpreme X-Mem™ 充当 KV 缓存卸载的专用内存层。MPU 不再使用主机 DRAM 或 RDMA 作为主要的 L2 KV 缓存层，而是提供了一个专门构建、面向加速器、针对 KV 数据搬运优化的内存层。

这使得 X-Mem™ 对以下负载尤其有用：

- 对 TTFT 有严格 SLO 要求；
- 长共享前缀 / 高并发会话；
- 反复出现的预填充密集型请求。

Netpreme X-Mem™ 通过兼容 CUDA 和 PyTorch 的 API 与 SGLang 集成。这些 API 让任何机器学习应用都能以透明的方式接入高带宽内存层，且几乎无需修改应用代码。

## SGLang + Netpreme X-Mem™ 基准测试

我们进行了两组实验：一组是测量单个请求 TTFT 的微基准测试，另一组是使用智能体负载的端到端 LLM 推理实验。在整个基准测试过程中，我们比较了三种配置：

| 配置 | 说明 |
| --- | --- |
| 仅 GPU 的 RadixAttention | 禁用前缀缓存，因此需要重新计算  |
| SGLang HiCache + 主机 DRAM | 使用主机 DRAM 作为卸载层的分层缓存 |
| SGLang HiCache + Netpreme X-Mem™ | 使用 Netpreme MPU（受 H100 GPU 限制的 350 GB/s 配置）作为卸载层的分层缓存 |

### X-Mem™ 让单请求 TTFT 趋于平缓

![Figure 4](/images/blog/netpreme-xmem/figure4.png)

结果显示，与主机 DRAM 相比，Netpreme 的 MPU 将单个请求的 TTFT 最多降低约 ~6.7×，即使在非常长的上下文下，TTFT 曲线也几乎保持平缓。

### X-Mem™ 提升 LLM 推理服务引擎的交互性与系统容量

上述 TTFT 的降低如何转化为端到端 LLM 推理的改进？为了回答这个问题，我们运行了端到端 LLM 推理服务基准测试 NVIDIA AIPerf。我们使用代表智能体式 AI 推理的负载：1K token 的系统提示词，外加每用户 20K token 的上下文。每个用户单轮输入 26 个 token，平均轮数为 20。实心点表示帕累托最优点；阴影点表示非帕累托最优点。

![Figure 5](/images/blog/netpreme-xmem/figure5.png)

结果表明，在中负载场景下，Netpreme 的 X-Mem™ 带来了高出 33% 的 TPS/user（交互性）；在高负载场景下，交互性高出 50%，TPS（系统容量）高出 30%。这是因为 GPU 的利用更加高效，在前缀缓存命中时花费在等待数据拷贝上的时间更少。

## 展望未来

随着编程智能体、长上下文助手和推荐系统不断壮大，推理服务系统将需要保存和搬运规模大得多的 KV 工作集。为此，Netpreme 将推进：

- 基于 MPU 与 SSD 的更大规模持久化 KV 存储
- 多实例 KV 共享
- 近内存 KV 压缩
- 近内存计算

Netpreme 的长期愿景是为智能体式负载提供全栈内存解决方案：不仅涵盖 KV 缓存，还包括模型权重、激活值、嵌入以及其他数据结构。通过提供针对机器学习负载优化的高性能内存层，Netpreme 让传统主机 DRAM 和 GPU HBM 无法实现的新软件架构与优化成为可能。

## 结论

SGLang 已经为前缀缓存提供了坚实的软件基础。RadixAttention 和 HiCache 让 KV 缓存可以在长上下文、多轮对话和前缀密集型负载中复用。但随着前缀缓存变得越来越有效，瓶颈也在转移。

挑战不再仅仅是找到可复用的前缀，而是要把缓存的 KV 足够快地搬回 GPU 内存，让复用真正带来延迟和吞吐量上的实际收益。

基于主机 DRAM 的卸载提升了容量，但其 PCIe 级别的带宽可能成为 KV 密集型推理的限制因素，尤其是当 TTFT SLO 非常紧张时。Netpreme X-Mem™ 通过为 SGLang HiCache 提供一个高带宽、专门构建的 KV 内存层，解决了这一瓶颈。

SGLang HiCache 与 Netpreme X-Mem™ 携手，让前缀缓存为下一代 LLM 负载（包括编程智能体、长上下文助手和推荐系统）变得更快、更具扩展性。

## 致谢

我们感谢 SGLang 团队在此次集成全程中给予的建设性技术讨论与指导。

## 参考文献

- SGLang 文档：HiCache Design
- SGLang 博客：HiCache：为 LLM 推理服务提供分层缓存的高性能 KV 缓存存储
- Netpreme SGLang X-Mem™ 集成：https://github.com/netpreme/sglang_xmem
- LinkedIn 工程博客：用 SGLang 为 LinkedIn 推荐系统全面提速
- Qwen3-235B-A22B-Thinking-2507：https://huggingface.co/Qwen/Qwen3-235B-A22B-Thinking-2507
- SWE-bench：https://github.com/SWE-bench/SWE-bench
- Netpreme 编程智能体实验：https://github.com/netpreme/coding_agents

---

## 附录

### 评测配置

- GPU：单张 H100 级 GPU
- KV 内存层容量：64 GB（主机 DRAM 或 Netpreme X-Mem™）
- CUDA 版本：12.8
- 注意力后端：FlashAttention
- GPU 前缀缓存：禁用（用于评估在本地 KV 缓存未命中、但命中 X-Mem™ 的场景）
- 模型：[Qwen3-30B-A3B-Instruct-2507-FP8](https://huggingface.co/Qwen/Qwen3-30B-A3B-Instruct-2507-FP8)
- 负载：
  - 单请求 TTFT 基准测试：使用了一个基准[脚本](https://github.com/netpreme/sglang_xmem/blob/mtier-dev/kvcache_benchmark.py)，它是 vLLM KVConnector 基准测试脚本的修改版（[博客](https://vllm.ai/blog/2026-01-08-kv-offloading-connector)、[代码](https://github.com/orozery/playground/blob/kv-offloading-blog-dec-2025/kvcache/kv_offload_benchmark.py)）。
  - 端到端吞吐量基准测试：使用了 NVIDIA Dynamo 团队的 [AIPerf](https://github.com/ai-dynamo/aiperf)。具体而言，我们使用了以下代表智能体式 AI 用例的负载配置：
    - 用户数：15
    - 所有用户的 QPS：[3.0,3.0,3.5,4.0,4.5,5.5]
    - 共享系统提示词：1000 token
    - 每用户上下文：20000 token
    - 每轮查询：26 token
    - 每轮输出长度：100 token
