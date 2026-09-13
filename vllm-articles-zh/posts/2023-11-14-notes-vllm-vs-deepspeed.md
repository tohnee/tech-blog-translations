---
title: "关于 vLLM 与 DeepSpeed-FastGen 的几点说明"
title_en: "Notes on vLLM v.s. DeepSpeed-FastGen"
source: https://vllm.ai/blog/2023-11-14-notes-vllm-vs-deepspeed
crawled: 2026-09-12
translated: 2026-09-12
---

# 关于 vLLM 与 DeepSpeed-FastGen 的几点说明

> 原文：[Notes on vLLM v.s. DeepSpeed-FastGen](https://vllm.ai/blog/2023-11-14-notes-vllm-vs-deepspeed) · vLLM 博客

vLLM 团队

[#性能](https://vllm.ai/blog/tags/performance)

---

**TL;DR：**

- 在常见场景中，vLLM 的速度与 DeepSpeed-FastGen 相当；在处理较长输出时，vLLM 更胜一筹。
- DeepSpeed-FastGen 仅在长提示、短输出的场景中优于 vLLM，这得益于其 Dynamic SplitFuse 优化。该优化已列入 vLLM 的路线图。
- vLLM 的使命是打造最快、最易用的开源 LLM 推理与服务引擎。它采用 Apache 2.0 许可证、由社区共同拥有，提供广泛的模型与优化支持。

---

DeepSpeed 团队最近发布了[一篇博客](https://github.com/microsoft/DeepSpeed/tree/master/blogs/deepspeed-fastgen)，声称借助 Dynamic SplitFuse 技术相比 vLLM 实现了 2x 的吞吐量提升。
我们很高兴看到开源社区的技术进步。
在本篇博客中，我们将展示 Dynamic SplitFuse 技术具有优势的具体场景，并指出这些场景相对有限。
对于大多数工作负载而言，vLLM 比 DeepSpeed-FastGen 更快（或性能相当）。

### 性能基准测试

我们在性能优化方面发现了 vLLM 与 DeepSpeed-FastGen 之间的两个关键差异：

1. **DeepSpeed-FastGen 采用了保守/次优的内存分配方案**，当输出长度较大时会浪费内存。
2. DeepSpeed-FastGen 的 Dynamic SplitFuse 调度**只有在提示长度远大于输出长度时才会带来加速**。

因此，当工作负载始终是长提示、短输出时，DeepSpeed-FastGen 表现更佳。
在其他场景中，vLLM 展现出更优越的性能。

我们在一块 NVIDIA A100-80GB GPU 上使用 LLaMA-7B 模型，在以下场景中对两个系统进行了基准测试：

#### 场景 1：长提示长度，短输出

在这里，DeepSpeed-FastGen 的 Dynamic SplitFuse 调度本应大放异彩。
然而，我们观察到的性能提升并不像 2x 那么显著。

![](https://vllm.ai/blog-assets/figures/notes-vllm-vs-deepspeed/s1.png)

#### 场景 2：其他情况

在这些情况下，vLLM 比 DeepSpeed-FastGen 快最高 **1.8x**。

![](https://vllm.ai/blog-assets/figures/notes-vllm-vs-deepspeed/s2.png)

### vLLM 的未来：一个真正的社区项目

我们致力于让 vLLM 成为吸纳社区最佳模型、最佳优化和最佳硬件的最佳开源项目。vLLM 诞生于 UC Berkeley Sky Computing Lab，我们正以 Apache 2.0 许可证真正开源地构建 vLLM。

vLLM 团队重视协作，努力保持代码库的高质量代码和易贡献性。我们正在积极改进系统性能，同时开发 LoRA、投机解码（Speculative Decoding）、更好的量化支持等新特性。此外，我们正与 AMD、AWS Inferentia、Intel Habana 等硬件厂商合作，把 LLM 带给最广泛的社区。

针对 Dynamic SplitFuse 优化，我们正在积极研究合适的集成方式。如果你有任何问题或建议，欢迎通过 [GitHub](https://github.com/vllm-project/vllm) 联系我们。我们也在[这里](https://github.com/vllm-project/vllm/blob/main/benchmarks/benchmark_throughput.py)发布了基准测试代码。

### 附录：功能对比

DeepSpeed-FastGen 目前只提供基础功能，仅支持三种模型类型，并且缺少停止字符串（stop strings）和并行采样（如束搜索）等热门特性。
我们预计 DeepSpeed-FastGen 会努力追赶，我们也欢迎市场上的创新！

|  | vLLM | DeepSpeed-FastGen |
| --- | --- | --- |
| 运行时 | Python/PyTorch | Python/PyTorch |
| 模型实现 | HuggingFace Transformers | 自定义实现 + HF 模型转换器 |
| 服务前端 | 用于演示的简单 FastAPI 服务器 | 自定义基于 gRPC 的服务器 |
| 调度 | 连续批处理（Continuous Batching） | Dynamic SplitFuse |
| 注意力内核 | PagedAttention 与 FlashAttention | PagedAttention 与 FlashAttention |
| 自定义内核（针对 LLaMA） | Attention、RoPE、RMS、SILU | Attention、RoPE、RMS、SILU、Embedding |
| KV 缓存分配 | 近乎最优 | 次优/保守 |
| 支持的模型 | 16 种不同架构 | LLaMA、Mistral、OPT |
| 采样方法 | 随机采样、并行采样、束搜索 | 随机采样 |
| 停止条件 | 停止字符串、停止 token、EOS | EOS |
