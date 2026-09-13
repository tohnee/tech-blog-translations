---
title: "SGLang HiCache：搭配你喜爱的存储后端，实现高速分层 KV 缓存"
title_en: "SGLang HiCache: Fast Hierarchical KV Caching with Your Favorite Storage Backends"
author: "Zhiqiang Xie"
date: "September 10, 2025"
previewImg: /images/blog/hicache/hicache_overview.png
source: https://lmsys.org/blog/2025-09-10-sglang-hicache/
translated: 2026-09-12
---

# SGLang HiCache：搭配你喜爱的存储后端，实现高速分层 KV 缓存

> 原文：[SGLang HiCache: Fast Hierarchical KV Caching with Your Favorite Storage Backends](https://lmsys.org/blog/2025-09-10-sglang-hicache/) · LMSYS Blog · Zhiqiang Xie

## 来自社区的反馈：

在使用 Qwen3-Coder-480B 的编程智能体场景中，观察到的对话在每轮会话约 8 轮时就往往超过 25K token。如果没有完整的 KV 缓存保留，几乎所有请求都需要代价高昂的重新计算。通过**将 SGLang HiCache 与 DeepSeek 3FS KVStore 集成**来实现大规模历史 KV 缓存，会话的**平均 TTFT 下降了 56%，推理吞吐量翻倍，缓存命中率从 40% 跃升至 80%**。
<p align="right">
– Novita AI
</p>

高效的 KV 缓存通过消除冗余且代价高昂的重新计算，能显著降低 TTFT。**将 SGLang HiCache 与 Mooncake 服务集成**，可实现可扩展的 KV 缓存保留与高性能访问。在评估中，我们在 PD 分离部署下，使用从**通用问答（QA）场景**采样的自研线上请求测试了 DeepSeek-R1-671B 模型。平均而言，**相比完整重新计算，缓存命中使 TTFT 降低了 84%**。
<p align="right">
– Ant Group
</p>


我们还在本文末尾提供了在长上下文基准和多轮对话基准上复现这些性能提升的说明。在我们的测量中，HiCache **实现了最高 6 倍的吞吐量提升和最高 80% 的 TTFT 降低**，与社区报告的结果高度一致。除上述 3FS 和 Mooncake 存储后端外，SGLang 还支持 [NIXL](https://github.com/ai-dynamo/nixl) 以及本地文件后端。


## 为什么分层 KV 缓存很重要

复用历史 KV 缓存已被证明对高性能 LLM 推理服务系统至关重要。我们此前推出的 [RadixAttention](https://arxiv.org/abs/2312.07104) 通过复用存储在 GPU 显存中的 KV 缓存，实现了最先进的性能。然而，**缓存收益不可避免地受到容量瓶颈的制约**：随着上下文变得更长、更多客户端进行更多轮对话，缓存命中率会不断下降，因为大多数历史 KV 缓存必须被逐出，以便为新数据腾出空间。

为应对这一挑战，我们推出 SGLang HiCache，它在 RadixAttention 的基础上扩展出 HiRadixTree，充当页表来引用驻留在 GPU 与 CPU 内存中的本地 KV 缓存。与此同时，缓存控制器会自动管理 KV 缓存数据在各层级之间的加载与备份，涵盖 GPU 和 CPU 内存池，以及磁盘、远程内存等外部层。下图展示了 SGLang HiCache 的总体架构。
<img src="/images/blog/hicache/hicache_overview.png" style="width: 40vw; min-width: 300px;" />


## SGLang HiCache 的设计：

### 优化的数据面

分层内存系统的关键瓶颈，是把数据从较慢的层级搬到较快层级的延迟。除了标准的 `cudaMemcpyAsync`，我们还开发了一组 [GPU 辅助 I/O 内核](https://github.com/sgl-project/sglang/blob/main/sgl-kernel/csrc/kvcacheio/transfer.cu)，可将 CPU–GPU 传输的吞吐量提升至最高 3 倍。

为进一步加速 CPU 内存与存储层之间的数据搬运，我们在所实现内核的基础上，将主机内存池的布局与 GPU 布局解耦，如图 1 所示。GPU 内存池保持不变的“层优先（layer-first）”布局以兼容计算内核，HiCache 则在其他层级采用“页优先（page-first）”布局以优先保证 IO 效率。这使得每次事务可以传输更大的数据量，再结合零拷贝机制，在典型部署中可实现最高 2 倍的吞吐量提升。更多细节可参考 PR（[Mooncake](https://github.com/sgl-project/sglang/pull/8651)、[3FS](https://github.com/sgl-project/sglang/pull/9109)）。
<img src="/images/blog/hicache/hicache_layout.png" style="width: 40vw; min-width: 300px;" />


### 灵活多样的控制面

当缓存未命中 GPU 但命中 CPU 内存时，由于这两层之间的带宽通常很高，我们采用[逐层重叠机制](https://arxiv.org/abs/2403.19708)来加载数据。这使得第 *N+* 层的 KV 缓存能够与第 *N* 层的执行并发加载，从而将数据传输延迟有效隐藏在计算之后。
当涉及**外部存储**时，一旦在存储层检测到缓存命中，缓存控制器便会伺机将数据从存储**预取（prefetch）**到主机内存。预取策略是可配置的：它可以以**尽力而为（best-effort）模式**运行，在某个请求即将被调度时终止在途预取以最小化 TTFT；也可以更激进地**暂存请求（stage requests）**，以提高缓存复用率并可能提升整体吞吐量。

存储层之所以采用这种不同的设计选择，是因为与主机–GPU 传输相比，存储的延迟通常明显更高且更难预测；当性能权衡合适时，我们也乐于采用 GPU Direct Storage 等技术。
SGLang HiCache 还支持多种缓存写策略，用于将数据从较快的层级移动到较慢的层级。**写穿透（write-through）**策略在带宽允许时提供最强的缓存收益；**选择性写穿透（write-through-selective）**模式利用命中次数追踪，只备份热点数据，从而降低 I/O 负载。当较慢的内存层也出现容量紧张时，**写回（write-back）**策略可以有效缓解压力。

### 选择你喜爱的存储后端，或者自带一个！

SGLang HiCache 最棒的一点，是**接入新存储后端**非常简单。得益于干净、通用的接口，集成只需在你的后端中实现三个功能：`get(key)`、`exist(key)`、`set(key, value)`。其余一切——包括调度与同步协调这类繁重工作——都由中央缓存控制器处理。

这一设计已经让我们集成了三个高性能后端——[Mooncake](https://github.com/kvcache-ai/Mooncake)、[3FS](https://github.com/deepseek-ai/3FS) 和 [NIXL](https://github.com/ai-dynamo/nixl)——还有更多在路上。出于演示目的，我们还提供了一个简单的 HiCacheFile 后端作为参考实现。我们也在推进 HiCache 与 PD 分离的协同设计与性能优化。我们热忱欢迎社区贡献与反馈，无论是新的调度策略、对现有设计的重构、可观测性特性、并行策略兼容性，还是对更多后端的支持。

## **基准测试**

快来亲自体验性能提升吧！你可以在[这里](https://github.com/sgl-project/sglang/tree/main/benchmark/hicache)找到关于 HiCache 的各类基准测试。下面我们重点展示使用所提供基准脚本得到的两个结果，各后端的配置说明见[这里](https://github.com/sgl-project/sglang/tree/main/python/sglang/srt/mem_cache/storage)。如果你对基准测试或部署有任何疑问，欢迎在 GitHub 上提 issue，或在我们的 [slack 频道](https://slack.sglang.io/)发帖讨论。

![3fs_benchmark.png](/images/blog/hicache/3fs_benchmark.png)

```bash
# DeepSeek R1 on 8 * H20-3e using 3FS
python3 -m sglang.launch_server  --model-path /DeepSeek-R1/ --tp 8 --page-size 64 \
--context-length 65536 --chunked-prefill-size 6144 --mem-fraction-static 0.85 \
--enable-hierarchical-cache --hicache-ratio 2 \
--hicache-io-backend kernel --hicache-mem-layout page_first \
--hicache-storage-backend hf3fs --hicache-storage-prefetch-policy wait_complete 

python3 bench_long_context.py --model-path /DeepSeek-R1/ --dataset-path loogle_wiki_qa.json 
```
![mooncake_benchmark.png](/images/blog/hicache/mooncake_benchmark.png)

```bash
# Qwen3-235B-A22B-Instruct-2507 on 8 × H800 GPUs with 8 × mlx5 RDMA NICs using Mooncake
MOONCAKE_TE_META_DATA_SERVER="http://127.0.0.1:8080/metadata" \
MOONCAKE_GLOBAL_SEGMENT_SIZE=816043786240, MOONCAKE_PROTOCOL="rdma" \
MOONCAKE_DEVICE="$DEVICE_LIST", MOONCAKE_MASTER=127.0.0.1:50051 \
python3 -m sglang.launch_server --model-path $MODEL_PATH --tp 8 --page-size 64 \
--enable-hierarchical-cache --hicache-ratio 2 \
--hicache-storage-prefetch-policy timeout --hicache-storage-backend mooncake

python3 benchmark/hicache/bench_multiturn.py --model-path $MODEL_PATH --disable-random-sample \
--output-length 1 --request-length 2048 \ # simulate P-D disaggregation
--num-clients 80 --num-rounds 10 --max-parallel 4 --request-rate 16 \
--ready-queue-policy random --disable-auto-run --enable-round-barrier
```
我们还想特别介绍 [NIXL](https://github.com/ai-dynamo/nixl) 这个特殊后端：它是一个传输库，旨在桥接 GPU-direct 存储和云对象存储等存储后端。更多详情见[这里](https://github.com/sgl-project/sglang/tree/main/python/sglang/srt/mem_cache/storage/nixl)，与 [Dynamo](https://github.com/ai-dynamo/dynamo) 生态的集成也即将到来，敬请期待。

## 致谢：
我们衷心感谢社区给予的巨大支持与反馈。
感谢来自阿里云 TairKVCache 团队的 Sicheng Pan、Zhangheng Huang、Yi Zhang、Jianxing Zhu 和 Yifei Kang 完成 3FS 后端集成； 
感谢来自蚂蚁集团的 Tingwei Huang 和 Yongke Zhao、来自阿里云的 Teng Ma、Shangming Cai 和 Xingyu Liu、来自 Approaching.AI 的 Jinyang Su 和 Ke Yang，以及来自 Mooncake 社区的 Zuoyuan Zhang 和 Mingxing Zhang 为 Mooncake 集成付出的努力； 
感谢 NVIDIA 的 Moein Khazraee、Vishwanath Venkatesan 和 Dynamo 团队促成 NIXL 集成。
特别感谢 SGLang 团队的 Ziyi Xu、LMCache 的 Yuwei An、NVIDIA 的 Vikram Sharma Mailthody、Scott Mahlke 和 Michael Garland，以及斯坦福大学的 Mark Zhao 和 Christos Kozyrakis 对 HiCache 设计与实现的贡献。
最后，感谢 LMCache、AIBrix、PrisDB 和字节跳动 EIC 团队的持续贡献，将他们的产品引入这一生态。
