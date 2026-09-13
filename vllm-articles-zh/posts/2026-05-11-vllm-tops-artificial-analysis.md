---
title: "vLLM 登顶 Artificial Analysis 排行榜"
title_en: "vLLM Tops the Artificial Analysis Leaderboard"
source: https://vllm.ai/blog/2026-05-11-vllm-tops-artificial-analysis
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM 登顶 Artificial Analysis 排行榜

> 原文：[vLLM Tops the Artificial Analysis Leaderboard](https://vllm.ai/blog/2026-05-11-vllm-tops-artificial-analysis) · vLLM 博客

作者：vLLM 团队

[#性能](https://vllm.ai/blog/tags/performance)[#基准测试](https://vllm.ai/blog/tags/benchmarking)[#内核融合](https://vllm.ai/blog/tags/kernel-fusion)[#投机解码](https://vllm.ai/blog/tags/speculative-decoding)

![](https://vllm.ai/blog-assets/figures/2026-05-11-vllm-tops-artificial-analysis/hero_image.png)

*vLLM 如何打造出 DeepSeek V3.2、MiniMax-M2.5 和 Qwen 3.5 397B 的领先部署。*

上周，DigitalOcean [发布了](https://www.digitalocean.com/blog/how-we-built-fastest-deepseek-minimax-qwen-on-blackwell-ultra)针对三个前沿开放权重模型的推理基准测试。在 DeepSeek V3.2 上，该部署实现了 230 TPS 的最佳单用户输出吞吐量——是大多数推理提供商对同一模型所报告数值的 4 倍以上。在 Qwen 3.5 397B 发布时，它在 [Artificial Analysis](https://artificialanalysis.ai/) 测量的全部 12 家提供商中排名第一，在 10,000 token 提示上 TTFT 低于 1 秒。

值得注意的地方是：其底层引擎是开源的。它就是 vLLM。

生产环境 AI 中的一个常见假设是，最佳的推理性能需要专有技术栈。然而在这个案例中，一个社区构建的推理引擎，运行在同样的 NVIDIA Blackwell Ultra 芯片上，排名第一。

这些结果背后的优化并未被锁在私有 fork 里。针对 DeepSeek V3.2 的算子融合、为 MiniMax-M2.5 定制的 EAGLE3 草稿模型，以及针对 Qwen 3.5 线性注意力路径调优的一组融合——每一项改动都已在 vLLM main 分支中，或正在合入途中。

本文介绍这一部署是如何构建的。

## vLLM 如何做到如此快速

这项工作分布在三个模型上，每个模型都有自己的瓶颈和对应的修复。

1. DeepSeek V3.2：以激进的内核融合削减低批大小下的开销（同样适用于 [DeepSeek V4](https://vllm.ai/blog/deepseek-v4)）。
2. MiniMax-M2.5：定向内核融合配合自定义 EAGLE3 草稿模型——尽管该模型本身是定制的，草稿模型却基于开源的 [TorchSpec](https://github.com/torchspec-project/TorchSpec) 和 vLLM 训练而成。同一个草稿模型也适用于 M2.7；两者的架构完全相同。
3. Qwen 3.5 397B：针对该模型注意力与归一化路径的定向融合。

以下各节将依次介绍每个模型。

## DeepSeek V3.2：低批大小下的内核融合

在低批大小下，DeepSeek V3.2 受制于 GPU 内核启动开销，而非计算本身。每个 transformer 层都会发出数十个独立内核——归一化、旋转位置编码、量化等小操作，GPU 本身只需微秒级即可执行完毕，但每个内核都带有固定的启动成本，正是这些成本主导了总时间。

解决方案是跨注意力路径的算子融合。此前作为独立内核启动的操作——Q 与 KV 的归一化、Q 与 KV 的旋转位置编码、indexer 的层归一化与旋转位置编码、FP8 量化以及 KV 缓存写入——被合并为一对融合内核，覆盖注意力与 MoE 之外的所有环节。每层内核数量从约 33 个降至接近约 10 个的目标。

![Figure 1: DSv3.2 attention-path fusion collapses ~33 per-layer kernel launches into ~10, yielding a 1.28× speedup at batch size 1.](https://vllm.ai/blog-assets/figures/2026-05-11-vllm-tops-artificial-analysis/figure1.png)

图 1：DSv3.2 的注意力路径融合将每层约 33 次内核启动压缩到约 10 次，在批大小为 1 时带来 1.28× 的加速。

仅融合本身就在批大小为 1 时带来了 1.28× 的加速（在 4× GB200 上从 85.8 提升到 109.3 tok/s，无 MTP）。在单个 8× B300 节点、并发为 1 的条件下：

- 无 MTP（TP=8）：125 tok/s
- 使用 MTP=1（TP=8）：234 tok/s（约 90% 草稿接受率）
- 使用预填充/解码分离（TP=4 + TP=4 + MTP=3）：262 tok/s

除融合之外，两个 DSv3.2 专用内核补齐了剩余差距。一个新的路由器 GEMM 内核——专门针对 DSv3 在小解码批大小下的 MoE 路由维度——取代了通用 matmul，在批大小为 1 时额外带来 6% 的加速（[#34302](https://github.com/vllm-project/vllm/pull/34302)）。

对于稀疏注意力 indexer，一个新的 TopK 内核根据序列长度为每行选择合适的算法，将所有情况纳入单个 CUDA Graph。这在 128K 上下文解码中带来了高达 17% 的每 token 延迟改善（[#37421](https://github.com/vllm-project/vllm/pull/37421)）。

这项工作如今构成了 [vLLM 对 DeepSeek V4 支持](https://vllm.ai/blog/deepseek-v4)的基础，后者复用了此前的 Q RoPE + 量化与 QK 归一化融合。结果如下所示。

![Figure 2: DeepSeek V3.2 Non-Reasoning, output speed across providers.](https://vllm.ai/blog-assets/figures/2026-05-11-vllm-tops-artificial-analysis/figure2.png)

图 2：DeepSeek V3.2 Non-Reasoning，各提供商输出速度。

*来源：[Artificial Analysis](https://artificialanalysis.ai/models/deepseek-v3-2/providers#output-speed)，2026 年 5 月。*

![Figure 3: DeepSeek V3.2 Reasoning, output speed across providers.](https://vllm.ai/blog-assets/figures/2026-05-11-vllm-tops-artificial-analysis/figure3.png)

图 3：DeepSeek V3.2 Reasoning，各提供商输出速度。

*来源：[Artificial Analysis](https://artificialanalysis.ai/models/deepseek-v3-2-reasoning/providers#output-speed)，2026 年 5 月。*

## MiniMax-M2.5：EAGLE3 与更多内核融合

[Inferact](https://inferact.ai) 团队使用 [TorchSpec](https://github.com/torchspec-project/TorchSpec) 为 MiniMax-M2.5 训练了一个自定义 EAGLE3 草稿模型。TorchSpec 是一个 torch 原生的在线投机解码框架，可并发运行 FSDP 草稿训练与基于 vLLM 的目标推理。该草稿模型并非从通用的监督数据集学习，而是消费由 vLLM 实时生成的隐藏状态，其响应由 MiniMax-M2.5 重新生成，从而训练它去匹配基础模型的精确 token 分布。

vLLM MRV2 路径上的投机解码基础设施改进使之成为可能：一项修复草稿模型元数据的改动，提高了靠后草稿位置的接受率（[#38311](https://github.com/vllm-project/vllm/pull/38311)）；以及草稿预填充的 CUDA Graph 支持（[#37588](https://github.com/vllm-project/vllm/pull/37588)）。

与草稿模型同步，MiniMax M2.5 还获得了定向内核融合工作。我们新增了自定义 QK 归一化融合（`fuse_minimax_qk_norm`），以处理该模型非标准的注意力归一化——其中 Q 和 K 的方差会先在各张量并行 rank 间归约，然后再应用逐通道缩放（[#37045](https://github.com/vllm-project/vllm/pull/37045)）。

![Figure 4: Anatomy of fuse_minimax_qk_norm across four tensor-parallel ranks.](https://vllm.ai/blog-assets/figures/2026-05-11-vllm-tops-artificial-analysis/figure4.png)

图 4：fuse\_minimax\_qk\_norm 在四个张量并行 rank 间的结构剖析。

在启用这一融合以及标准 `fuse_norm_quant`、`fuse_act_quant` 和 `fuse_gemm_comms` pass 之后，上限实验达到了：

- 并发 1 时 326 tok/s（TP=4，EAGLE3 + 3 个投机 token，合成的 100% 接受率）。

这代表了在完美草稿模型下服务栈的上限，从而将融合工作的贡献与草稿模型质量隔离开来。

![Figure 5: MiniMax-M2.5, output speed across providers.](https://vllm.ai/blog-assets/figures/2026-05-11-vllm-tops-artificial-analysis/figure5.png)

图 5：MiniMax-M2.5，各提供商输出速度。

*来源：[Artificial Analysis](https://artificialanalysis.ai/models/minimax-m2-5/providers#output-speed)，2026 年 5 月。*

## Qwen 3.5 397B：线性注意力与融合缺口

Qwen 3.5 在其注意力块中使用带非标准归一化的线性注意力。这两个架构选择都与 vLLM 的标准融合基础设施不太合拍：投影后的卷积路径是线性注意力模型独有的，而其归一化变体又不符合 vLLM 现有 `allreduce_rms` 融合所寻找的模式。

这一代价在性能剖析器中显露无遗。由于错过了 `allreduce_rms` 融合，大约一半的解码时间被花在未融合的跨设备归约上——这正是融合本应消除的开销类型。模型在正常运行、数值也正确，但引擎只是做了比必要更多的内存往返。

四项工作补齐了这一差距：

- 对现有 `allreduce_rms` 融合 pass 的修复，使其能够识别 Qwen 的归一化变体——批大小 > 1 时 TPOT 改善约 5%。
- qk-norm + rope 路径的内核级优化。
- 针对 Qwen 线性注意力架构的 post-conv 路径内核融合（[#37813](https://github.com/vllm-project/vllm/pull/37813)）。
- 双流执行，重叠彼此独立的计算分支。

![Figure 6: Qwen 3.5 397B kernel fusion work in vLLM.](https://vllm.ai/blog-assets/figures/2026-05-11-vllm-tops-artificial-analysis/figure6.png)

图 6：vLLM 中 Qwen 3.5 397B 的内核融合工作。

结合 TP=8 + 专家并行，生产部署达到了：

- 并发 1 时 163 tok/s（TEP=8，post-conv 融合）
- 并发 256 时 7.33 req/s，高于 6.69 req/s 的基线（+10%）

这项工作已随 vLLM main 分支发布。

![Figure 7: Qwen 3.5 397B, output speed across providers.](https://vllm.ai/blog-assets/figures/2026-05-11-vllm-tops-artificial-analysis/figure7.png)

图 7：Qwen 3.5 397B，各提供商输出速度。

*来源：[Artificial Analysis](https://artificialanalysis.ai/models/qwen3-5-397b-a17b/providers#output-speed)，2026 年 5 月。*

## 这对 vLLM 意味着什么

这些结果背后的优化——DSv3.2 注意力路径融合、MiniMax EAGLE3 草稿模型训练配方，以及 Qwen 3.5 融合——要么已经进入 vLLM main 上游，要么正在合入上游的路上。在当前 vLLM 上运行这些模型的团队即可获得同样的加速。

## 开源成为默认选择

历来，最快的推理栈都是专有的——由超大规模云厂商、模型实验室和芯片厂商为自身基础设施构建和调优。开源替代方案虽可广泛使用，但在生产性能上往往落后。

在推理层，这一情况不再成立。vLLM 如今在其所支持的模型上登顶 Artificial Analysis 排行榜。在这些基准测试上，世界上最快的推理是开源的。现代 AI 之下的基础设施也正在跟上。

## 致谢

感谢 Inferact、DigitalOcean、NVIDIA、Red Hat 以及 vLLM 开源社区对本项工作的贡献。
