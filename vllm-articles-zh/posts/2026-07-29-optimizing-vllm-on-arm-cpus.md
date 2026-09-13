---
title: "在 Arm CPU 上优化 vLLM"
title_en: "Optimizing vLLM on Arm CPUs"
source: https://vllm.ai/blog/2026-07-29-optimizing-vllm-on-arm-cpus
crawled: 2026-09-12
translated: 2026-09-13
---

# 在 Arm CPU 上优化 vLLM

> 原文：[Optimizing vLLM on Arm CPUs](https://vllm.ai/blog/2026-07-29-optimizing-vllm-on-arm-cpus) · vLLM 博客

作者：Arm 团队

[#硬件](https://vllm.ai/blog/tags/hardware)[#性能](https://vllm.ai/blog/tags/performance)

## 引言

在 CPU 上进行大语言模型服务是一种重要的部署选择：CPU 部署成本更低、基础设施更简单，而且在云端和企业数据中心广泛可得。随着基于 Arm® Neoverse™ 的服务器部署日益广泛，提升 vLLM 等开源服务框架在 Arm CPU 上的易用性、特性覆盖和性能变得越来越重要。

过去几个月，我们与 vLLM、PyTorch、oneDNN 和 KleidiAI 社区合作，对 Arm CPU 服务栈进行了上游改进。成果是更佳的易用性、更广的模型与特性支持，以及可观的性能提升——任何运行 vLLM 的 Arm Neoverse 服务器都能受益。

在本博客中，我们先介绍易用性与覆盖方面的改进，然后深入剖析主要性能优化和端到端服务结果。

## 使能与可用性

在性能优化之外，我们还改进了 vLLM 在 Arm® CPU 上的易用性与特性完备度，使在 Arm® 服务器上部署 vLLM 更加容易。

主要的使能改进包括：

- 预构建的 [wheel 包](https://docs.vllm.ai/en/latest/getting_started/installation/cpu/#arm-aarch64_2:~:text=venv/bin/activate-,Pre%2Dbuilt%20wheels,%C2%B6,-When%20specifying%20the)与 [Docker 镜像](https://docs.vllm.ai/en/latest/getting_started/installation/cpu/#arm-aarch64_4:~:text=%C2%B6-,Pre%2Dbuilt%20images,%C2%B6,-Intel/AMD%20x86)。
- 修复了崩溃、精度问题、线程以及 CPU 利用率方面的缺陷。
- 支持分块预填充（Chunked Prefill）与前缀缓存。
- 支持 INT8 W8A8 与 INT8 W4A8 推理。
- 使 GPT-OSS、Whisper 以及 Qwen 3.5 / 3.6 模型可用。
- 与 [PyTorch](https://github.com/pytorch/pytorch) 和 [UXL](https://github.com/uxlfoundation) 生态更紧密的集成。

在这些使能改进就位后，我们把注意力转向理解并消除性能瓶颈。

## 性能改进

2025 年 10 月我们首次在 Arm CPU 上对 vLLM 做基准测试时，性能远低于预期——尽管约 80% 的模型运行时间都花在派发给高度优化 BF16 GEMM 的稠密层上。这些层背后的独立 GEMM 内核已经接近预期的硬件效率，因此最大的收益不太可能仅来自 GEMM 内核。

性能剖析反而指向一个更广泛的优化问题：分配器行为、运行时同步、框架开销、注意力内核以及量化执行。

### 内存分配

LLM 服务给 CPU 内存分配器带来很大压力。在预填充和解码期间，vLLM 反复为调度、KV 缓存管理和中间算子输出分配与释放张量。在最初的基准测试中，内存分配成为瓶颈：大块分配的复用不佳导致大量缺页。

根源在于 PyTorch 使用 glibc 的 `malloc`。大块分配在反复的推理步骤之间得不到有效复用，且随着线程数增加，分配/释放路径成为争用来源。作为变通，我们起初建议预加载一个带缓存的分配器，但这增加了手动配置，并使性能依赖于运行时配置。

为了改善开箱即用的性能，我们在 PyTorch 中启用 [mimalloc](https://github.com/microsoft/mimalloc) 作为 Arm CPU 上的默认分配器。Mimalloc 是一个为多线程分配压力下的扩展性而设计的缓存分配器。我们选择它，是因为它在广泛的 TorchBench 工作负载上表现强劲，且此前已作为 PyTorch 依赖集成在非 Arm 的 Linux 构建中。

这使 Llama 3.1 8B 开箱即用的离线吞吐提升 2.3×，并在低并发服务场景中带来约 7× 的收益。

> **注意：** 本文所有性能图中都排除了分配器改进，因为其收益会主导坐标尺度、掩盖其他优化的影响。因此图中展示的是栈中其余部分的改进。

### 高核数下的同步

改善内存分配之后，下一个瓶颈出现在把推理扩展到更高核数时。超过某个点后，增加更多核并不能提升吞吐，甚至可能使性能回退。

为了弄清扩展性在哪里失效，我们在高线程数下对各个层做了剖析。一份剖析显示，分页注意力 74% 的时间花在 OpenMP 动态调度上：

```
97.94% gomp_thread_start
  90.08% paged_attention_v1_impl
    74.07% gomp_iter_dynamic_next
     7.00% reduceValueBlock::lambda(int)
```

`gomp_iter_dynamic_next` 属于 libgomp 的动态循环调度路径。在这条路径上，运行时用原子 fetch-add 把循环块分配给工作线程。PyTorch wheel 所用的 libgomp 运行时用一个 load-linked / store-conditional 重试循环实现该原子更新：

```
for (;;) {
    long old = LDXR(p);
    long newv = old + delta;
    int fail = STLXR(p, newv);
    if (fail == 0) {
        DMB_ISH();
        return old;
    }
}
```

在高核数下，大量工作线程在同一原子更新上争用，导致反复失败的写入尝试和重试流量。

追踪到汇编层面后发现了一个被错过的硬件优化机会。基准测试系统使用 Neoverse™ V2 核心，支持 [Arm 大系统扩展（LSE）](https://learn.arm.com/learning-paths/servers-and-cloud-computing/lse/example/)。LSE 提供硬件原子指令（如 `LDADDAL`），可以取代上面那条低效循环。然而 PyTorch 所用的 OpenMP 运行时并未利用 LSE 原子指令。

我们的解决方案是在 PyTorch 中构建一个 libgomp 运行时，在支持的 CPU 上使用 LSE 原子指令。

这使 Llama 3.1 8B 离线吞吐提升 9%，并在低并发服务场景中把每输出 token 时间（TPOT）延迟降低 15%。

### 稠密层布局开销

即使在分配器与运行时改进之后，稠密层仍有性能余量可挖。高性能 GEMM 内核对权重布局很敏感：要高效运行，权重需处于与内核的向量化及缓存访问模式匹配的分块格式。若不预先打包（prepacking），每次调用都可能付出把权重从框架张量布局转换为内核友好格式的代价。

这在低并发下代价尤其高，因为打包成本无法在大批量上摊销。我们的解决办法是为稠密层启用一条由 Compute Library for Arm Architecture 加速的快速 oneDNN 路径。该路径让 vLLM 在模型预热期间把 BF16 权重打包成内核期望的格式，然后在推理期间复用打包后的表示。

这使 Llama 3.1 8B 离线吞吐提升 16%，并在低并发服务场景中把 TPOT 延迟降低 60%。

### 分页注意力（Paged Attention）

CPU 分页注意力内核此前未针对 Arm CPU 优化。QK 与 PV 矩阵乘法以及 softmax 中的指数运算都在回退到参考实现。因此预填充依赖 PyTorch 的缩放点积注意力（SDPA）内核，这意味着 Arm CPU 路径不支持分块预填充与前缀缓存。

我们使用 Arm [BFMMLA](https://developer.arm.com/community/arm-community-blogs/b/ai-blog/posts/bfloat16-processing-for-neural-networks-on-armv8_2d00_a) 高级 SIMD 指令构建自定义 GEMM 内核，优化了 QK 与 PV 路径。我们还用快速向量化的三阶多项式近似优化了 softmax 指数运算。

这些改动让分页注意力最快提速 4×，并使 Llama 3.1 8B 离线吞吐提升 12%。
此外，这使我们得以在 Arm CPU 上为预填充启用分页注意力，解锁了对分块预填充与前缀缓存的支持。

### BF16 性能改进

同步、权重预打包与分页注意力优化叠加起来，构成了一个比 2025 年 10 月起点更强的 BF16 服务基线。

![Heatmap showing optimized BF16 serving relative to the October 2025 BF16 baseline](https://vllm.ai/blog-assets/figures/2026-07-29-arm-cpu/heatmap_bf16_optimized_vs_bf16_baseline.png)

热力图：优化后的 BF16 服务相对 2025 年 10 月 BF16 基线的表现

*优化后的 BF16 服务相对 2025 年 10 月 BF16 基线的表现。*

### INT8 W8A8（8 比特权重与激活值）

LLM 推理在预填充和解码期间反复读取大型权重矩阵。用 INT8 而非 BF16 存储权重可以降低内存带宽压力，并能让更大的模型装进相同的内存预算。

在具备 I8MM 的 Arm CPU 上，W8A8 还能映射到 [SMMLA](https://developer.arm.com/documentation/dui0379/e/arm-and-thumb-instructions/smmla)——Arm 的有符号 INT8 矩阵乘累加指令，理论矩阵乘吞吐是 BF16 的两倍。

为利用这一点，我们用 [oneDNN](https://github.com/uxlfoundation/oneDNN) JIT 内核加速 W8A8 量化路径，这些内核在 SVE128 与 SVE256 上使用 `SMMLA` 指令。

由此，多个 Hugging Face INT8 W8A8 检查点——包括 `RedHatAI/Meta-Llama-3.1-8B-quantized.w8a8` 和 `RedHatAI/whisper-large-v3-quantized.w8a8`——现在开箱即有良好表现。

与优化后的 BF16 基线相比，采用逐 token 激活量化与逐通道权重量化的 W8A8 视并发情况可带来最高 88% 的更高吞吐、45% 的更低 TPOT 和 54% 的更低 TTFT。

![Heatmap showing INT8 W8A8 serving relative to the optimized BF16 path](https://vllm.ai/blog-assets/figures/2026-07-29-arm-cpu/heatmap_int8_vs_bf16_optimized.png)

热力图：INT8 W8A8 服务相对优化 BF16 路径的表现

*INT8 W8A8 服务相对优化 BF16 路径的表现。*

> **注意：** 想进一步了解 Arm CPU 上的 INT8 W8A8，请尝试[这条](https://learn.arm.com/learning-paths/servers-and-cloud-computing/vllm-benchmark-quantisation/) Arm 学习路径。

### INT8 W4A8（4 比特权重、8 比特激活值）

W4A8 把同一思路推得更远：把权重量化为 INT4，以降低推理期间的内存带宽压力。这在低并发下尤其有用，因为此时批处理较少，难以摊销读取模型权重的成本。

该路径通过 [KleidiAI](https://github.com/ARM-software/kleidiai) 的 INT4 微内核加速。

与上述 W8A8 基线相比，采用逐 token 激活量化与逐通道权重量化的 W4A8 视并发情况可带来最高 29% 的更高吞吐、26% 的更低 TPOT 和 18% 的更低 TTFT。

与预期一致，W4A8 最大的加速出现在推理以内存受限为主的低并发场景。

![Heatmap showing INT8 W4A8 serving relative to the INT8 W8A8 path](https://vllm.ai/blog-assets/figures/2026-07-29-arm-cpu/heatmap_int4_vs_int8.png)

热力图：INT8 W4A8 服务相对 INT8 W8A8 路径的表现

*INT8 W4A8 服务相对 INT8 W8A8 路径的表现。*

> **注意：** 请参阅[这些文档](https://docs.vllm.ai/en/latest/features/quantization/llm_compressor/int8_w4a8/)了解如何用 llm-compressor 把模型量化为 INT8 W4A8。

## 总结

vLLM 在 Arm CPU 上的易用性、稳健性、模型与特性覆盖以及性能都得到了显著改进。

相对 2025 年 10 月的 BF16 基线，优化后的 BF16 路径可提供最高 **2.7× 的服务吞吐**。INT8 W8A8 达到最高 **4.8× 的基线吞吐**和 **5.7× 的 TPOT 加速**，而 INT8 W4A8 成绩最佳，最高达 **6.2× 的基线吞吐**、**7.8× 的 TPOT 加速**以及 **2.6× 的 TTFT 加速**。

这些收益来自对完整 CPU 推理栈的优化：内存分配、OpenMP 同步、稠密层预打包、分页注意力以及量化。

![Bar chart showing serving speedups for optimized BF16, INT8 W8A8, and INT8 W4A8 configurations relative to the October 2025 BF16 baseline](https://vllm.ai/blog-assets/figures/2026-07-29-arm-cpu/bars_all_vs_bf16_baseline.png)

条形图：优化 BF16、INT8 W8A8 与 INT8 W4A8 配置相对 2025 年 10 月 BF16 基线的服务加速比

*优化 BF16、INT8 W8A8 与 INT8 W4A8 配置相对 2025 年 10 月 BF16 基线的服务加速比。*

除了实测性能收益之外，这些改进还通过更广的特性覆盖、更好的开箱即用体验、上游集成和扩展的模型支持，让 vLLM 成为面向 Arm Neoverse 服务器更完整、更适合生产的推理栈。

## 致谢

我们感谢 vLLM 社区持续的支持与协作。

特别感谢 [Li Jiang](https://github.com/bigPYJ1151)（Intel®）维护 vLLM CPU 后端，并实现了本工作所依托的大部分基础设施。同时感谢 [Sanket Kale](https://github.com/sanketkaleoss)（Fujitsu）在 vLLM 中完成最初的 Arm CPU 使能工作，以及 [Shreyas](https://github.com/Shreyas-fuj)（Fujitsu）向 oneDNN 贡献 SVE256 INT8 内核。

---

Arm 是 Arm Limited（或其子公司或关联公司）的注册商标。
PyTorch 是 The Linux Foundation 的商标。
Intel 与 oneDNN 是 Intel Corporation 或其子公司的商标。

本博客文章版权归 2026 Arm Limited 和/或其附属公司所有 <open-source-office@arm.com>
