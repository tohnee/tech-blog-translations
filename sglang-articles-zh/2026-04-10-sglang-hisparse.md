---
title: "HiSparse：用分层内存为稀疏注意力全面提速"
title_en: "HiSparse: Turbocharging Sparse Attention with Hierarchical Memory"
author: "Zhiqiang Xie, Zhangheng Huang, Tingwei Huang"
date: "April 10, 2026"
previewImg: /images/blog/hisparse/hisparse_overview.png
source: https://lmsys.org/blog/2026-04-10-sglang-hisparse/
translated: 2026-09-12
---

# HiSparse：用分层内存为稀疏注意力全面提速

> 原文：[HiSparse: Turbocharging Sparse Attention with Hierarchical Memory](https://lmsys.org/blog/2026-04-10-sglang-hisparse/) · LMSYS Blog · Zhiqiang Xie, Zhangheng Huang, Tingwei Huang

## 为什么稀疏注意力的性能潜力尚未被充分挖掘
自注意力因其二次方的计算量与内存/IO 开销，已成为将大语言模型扩展到长上下文的主要瓶颈之一。这推动了人们对高效注意力机制日益浓厚的兴趣。其中，**稀疏注意力**尤其有前景：它只对选定的 KV 缓存子集进行注意力计算，在保留强大建模能力的同时，避免了普通注意力随上下文增长而面临的计算与 I/O 开销的急剧攀升。

然而，稀疏注意力（通常指 top-k 选择）并未消除**内存容量瓶颈**。在实践中，完整上下文的 KV 缓存必须常驻 GPU HBM 以便快速访问，尽管在每个解码步骤中实际只有一小部分条目处于活跃状态。因此，稀疏注意力往往是受容量限制（capacity-bound）而非受算力限制（compute-bound），这限制了可达到的批大小和整体吞吐量。如下图所示，基线（未启用 HiSparse 的稀疏注意力）的 token 生成吞吐量很早就进入平台期，因为 KV 缓存占用很快触及 GPU 显存容量上限。
相比之下，HiSparse 的吞吐量随并发增长接近线性扩展，在 256 并发请求时达到基线吞吐量的 3 倍以上。需要注意的是，在低并发下 HiSparse 会引入一定的额外开销，因为稀疏 KV 加载产生的额外 I/O 超过了内存节省带来的收益。当并发继续增加、内存压力占据主导时，收益就会变得十分显著。

<img src="/images/blog/hisparse/throughput_concurrency.png" style="width: 50vw; min-width: 300px;" />
<p style="text-align: center; color: #666; font-style: italic;"> <a href="https://huggingface.co/zai-org/GLM-5.1-FP8">GLM-5.1-FP8</a> 模型在 PD 共置的 8×H200 部署上，使用 32k 输入、8k 输出查询的基准测试结果。 </p>



## HiSparse 的设计
延续我们此前的工作 [HiCache](https://www.lmsys.org/blog/2025-09-10-sglang-hicache/)，我们提出 HiSparse：一个旨在克服上述限制的分层内存系统。HiSparse 主动将非活跃的 KV 缓存条目卸载到主机内存，显著降低 GPU 显存压力，同时在 GPU HBM 上保留一个热点设备缓冲区，存放频繁访问的 KV 区域，以尽量减少关键路径上的数据搬运。这使得解码批大小可以大幅提升，在提高吞吐量的同时扩展到更长的上下文。下图展示了 HiSparse 的工作流程。虽然图中以预填充-解码分离（PD 分离）部署为例，该设计同样适用于共置部署。
<img src="/images/blog/hisparse/hisparse_overview.png" style="width: 50vw; min-width: 300px;" />


### 高效的换入（swap-in）内核
这套系统的核心是一个专用 CUDA 内核，它能够高效地完成以下工作：\
(1) 在设备缓冲区中识别 top-k 缓存未命中；(2) 通过 LRU 策略选择逐出候选；(3) 更新页表并从主机内存取回所需条目到设备内存。\
下图展示了热点缓冲区大小与逐出策略对未命中率的影响。使用更大的热点设备缓冲区（4096 对比 2048 个槽位）以及 LRU 逐出策略时，未命中次数大幅下降，直接转化为关键路径上更低的换入延迟。

<img src="/images/blog/hisparse/miss_count_trend.png" style="width: 50vw; min-width: 300px;" />
<p style="text-align: center; color: #666; font-style: italic;"> <a href="https://huggingface.co/deepseek-ai/DeepSeek-V3.2">DeepSeek-V3.2</a>（top-k=2048）在 LongBenchV2 上的缓存未命中次数基准测试结果，未命中次数经 100 步滑动窗口平滑处理。</p>


## 基准测试
下面我们重点展示对最先进的开放模型 GLM-5.1-FP8 扫描多种序列配置得到的结果——在长上下文场景中最高取得 5 倍吞吐量提升，更详细的使用说明可在[这里](https://github.com/sgl-project/sglang/blob/main/docs/advanced_features/hisparse_guide.md)找到。


<img src="/images/blog/hisparse/hisparse_sweep.png" style="width: 50vw; min-width: 300px;" />
<p style="text-align: center; color: #666; font-style: italic;"> GLM-5.1-FP8 模型在双 H20 PD 分离部署上，各种输入与输出序列长度配置下的基准测试结果。</p>


```bash
# PD-disaggregation deployment (recommended) on two H20 nodes
# prefill instance:
python3 -m sglang.launch_server \
      --model-path "zai-org/GLM-5.1-FP8" --trust-remote-code --watchdog-timeout 100000 \
      --chunked-prefill-size 65536 --max-running-requests 480 --mem-fraction-static 0.8 \
      --tp-size 8 --dp-size 8 --enable-dp-attention --schedule-conservativeness 0.5 \
      --disaggregation-mode prefill \
      --disaggregation-ib-device mlx5_0,mlx5_1,mlx5_2,mlx5_3 \
      --dist-init-addr 127.0.0.1:5757 --nnodes 1 --node-rank 0

# decode instance:
python3 -m sglang.launch_server \
      --model-path "zai-org/GLM-5.1-FP8" --trust-remote-code --watchdog-timeout 100000 \
      --chunked-prefill-size 65536 --max-running-requests 480 --mem-fraction-static 0.85 \
      --tp-size 8 --dp-size 8 --enable-dp-attention \
      --load-balance-method round_robin --prefill-round-robin-balance \
      --kv-cache-dtype bfloat16 --nsa-decode-backend flashmla_sparse  \
      --disaggregation-mode decode --dist-init-addr 127.0.0.1:5757 \
      --disaggregation-ib-device mlx5_0,mlx5_1,mlx5_2,mlx5_3 --nnodes 1 --node-rank 0 \
      --enable-hisparse \
      --hisparse-config '{"top_k": 2048, "device_buffer_size": 6144, "host_to_device_ratio": 10}'


# PD-colocation deployment on a single 8xH200 instance
python3 -m sglang.launch_server \
      --model-path "zai-org/GLM-5.1-FP8" --trust-remote-code --watchdog-timeout 100000 \
      --chunked-prefill-size 65536 --max-running-requests 480 --mem-fraction-static 0.85 \
      --tp-size 8 --dp-size 8 --enable-dp-attention --disable-radix-cache \
      --enable-hisparse \
      --hisparse-config '{"top_k": 2048, "device_buffer_size": 4096, "host_to_device_ratio": 8}' 
```

## 未来工作
HiSparse 目前支持采用 [DeepSeek 稀疏注意力（DSA）](https://huggingface.co/deepseek-ai/DeepSeek-V3-0324)的模型系列，包括 DeepSeek-V3.2 和 GLM-5.1。作为一个实验性特性，我们期望持续改进其性能与模型覆盖范围。HiSparse 面向高并发场景设计，旨在最大化吞吐量；但由于 top-k 缓存未命中带来的额外 I/O，它也会引入一定开销。
我们期望通过更好的重叠机制来降低这一开销，并相信随着 Grace Blackwell（GB）系统等新兴平台提供更高的 CPU–GPU 带宽，该开销还将进一步得到缓解。

展望未来，我们将沿着此前 HiCache 工作的方向，计划扩展这一分层内存管理方法，以支持更广泛的新兴架构，包括[混合架构模型](https://github.com/sgl-project/sglang/pull/21206)。


## 致谢
我们衷心感谢阿里云 TairKVCache 团队与蚂蚁集团 SCT 推理团队的宝贵贡献。同时感谢来自阿里云的 Shangming Cai、Teng Ma 和 Xingyu Ling，以及来自 SGLang 社区的 Ziyi Xu 给予的大力支持。我们还要感谢斯坦福大学的 Christos Kozyrakis 和 Kristopher Geda，以及百度百舸 AI 团队提出的富有洞见的反馈。
