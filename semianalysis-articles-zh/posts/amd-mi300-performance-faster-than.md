---
title: "AMD MI300 性能——快过 H100，但快多少？"
title_en: "AMD MI300 Performance - Faster Than H100, But How Much?"
subtitle: "MI400：Broadcom + AMD 反 Nvidia 联盟将至，携 UEC 与开放 XGMI"
date: 2023-12-06
source: https://newsletter.semianalysis.com/p/amd-mi300-performance-faster-than
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# AMD MI300 性能——快过 H100，但快多少？

> 原文：[AMD MI300 Performance - Faster Than H100, But How Much?](https://newsletter.semianalysis.com/p/amd-mi300-performance-faster-than) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**MI400：Broadcom + AMD 反 Nvidia 联盟将至，携 UEC 与开放 XGMI**

MI300X 今天终于正式发布，而且来势汹汹。公布的客户名单很长——包括 Oracle、Meta、Microsoft 等，[其出货量与 ASP 我们此前已讨论过](https://www.semianalysis.com/p/amd-mi300-taming-the-hype-ai-performance)。今年 6 月我们已[发布过其配置与架构](https://www.semianalysis.com/p/amd-mi300-taming-the-hype-ai-performance)，因此虽然文末会有一些新的底层架构细节，今天的重点仍是性能、成本与软件。另外还有 AMD + Broadcom 反 Nvidia 联盟的重磅消息。

论纸面规格，MI300X 全面碾压 H100：FP8 FLOPS 多 30%，内存带宽多 60%，内存容量超 2 倍。当然，MI300X 更直接的对手是 H200——后者把内存带宽差距缩小到个位数百分比，容量差距缩小到 40% 以内。遗憾的是，MI300X 的内存带宽最终*只*做到了 5.3TB/s，而非最初目标的 5.6TB/s。

![](https://substack-post-media.s3.amazonaws.com/public/images/9553eb31-bf4c-4fa5-a6f9-5de1191af2f1_2018x1134.png)

当然，FLOPS、容量和带宽只是潜在能力。AMD 展示了几组不同的基准测试，主题很一致：相对理论峰值性能，实际表现仍有相当差距。

- FlashAttention2——这只是**前向传播**，即推理，不是训练**。**值得注意，AMD 分享的几乎每一项基准测试都只有前向传播。性能优势为 10% 到 20%，远低于纸面规格的差距。
- LLAMA2-70B——同样只是部分算子的前向传播，不是完整模型，性能领先同样是 10% 到 20%。这些更多是计算受限型负载，而非内存受限型。

![](https://substack-post-media.s3.amazonaws.com/public/images/f8863275-655f-428a-83b0-0113a27c1ce6_4690x2000.png)

至于推理，AMD 展示了两种不同的推理基准：一个面向高批规模与吞吐量，另一个追求尽可能低的时延。

- Bloom——这是所有基准里最亮眼的，但我们*认为*这是各家在拥有内存容量优势时玩过的经典戏法之一。选一个勉强塞进对方推理系统的模型——本例中 Bloom 略微超过 H100 HGX 640GB 内存中的 350GB——然后把输入序列长度拉得很大（此处为 2k），输出 token 数则很少（100）。内存较小的系统被迫以小得多的批规模运行，因为 KVCache 占光了内存容量；AMD 则可以用更大的批规模发挥算力优势。要说清楚：这是真实优势，面向吞吐的场景也是真实的，但它属于边缘用例。
- LLAMA 2-70B——这对大多数用例是更真实的推理基准。AMD 有 40% 的时延优势，考虑到其相对 H100 的 60% 带宽优势，这个数字非常合理。鉴于 H200 在带宽上接近得多，我们预计其表现会与 MI300X 相当。注意，AMD 在 Nvidia 上用的是 VLLM（吞吐最好的开源栈），但 Nvidia 闭源的 TensorRT LLM 同样好用，且在 H100 上时延还略优。

![](https://substack-post-media.s3.amazonaws.com/public/images/e22ed839-adcb-4791-88a2-88501cbfbc92_4666x2000.png)

最后一项基准是 LLAMA 2-13B。性能提升为 20%，这里没什么可挑剔的。MI300X 更便宜。H200 大概率能追平差距。

![](https://substack-post-media.s3.amazonaws.com/public/images/0cc1a792-b27d-4695-95ba-e54a464a6625_2707x1160.png)

再看训练。AMD 的软件栈在这里暴露了一些短板：MI300 只能达到理论 FLOPS 不到 30% 的水平，而 Nvidia 经常能做到 40%。因此性能不尽如人意。

他们（在训练上）的性能之所以只能与 Nvidia 打平，有几个原因。首要原因之一是 AMD 在纯 GEMM 负载上只能拿到约一半的理论 FLOPS。另一个是 FlashAttention2 在反向传播上仍表现不佳。支持正在路上，但架构差异让这件事很难。AMD 的 L1 缓存翻倍了，但 LDS 大小没变。相比 Nvidia 更大的 sharedmem，这让 FA2 的适配仍然更难。

![](https://substack-post-media.s3.amazonaws.com/public/images/3dc745f2-525a-4d47-95fe-bb6be21fb437_6300x2700.png)

假以时日，我们预计这些会显著改善。这些数字最大的亮点正在于此：我们看到 AMD 在快速进步。

总体而言，我们正关注 Triton 性能的持续改善，纯 GEMM 尤甚。

> OpenAI 正在与 AMD 合作，支持开放生态系统。我们计划从即将发布的 3.0 版本开始，在标准 Triton 发行版中支持包括 MI300 在内的 AMD GPU。
>
> Philippe Tillet，OpenAI

这是件大事，因为 OpenAI 和 Microsoft 将在推理上大量使用 AMD MI300。

另外要说明：对大多数现有模型，eager 模式和 torch.compile 在训练、微调和推理中开箱即用，缺的是性能优化。我们看到它正在发生。

我们敢打赌，未来几个月 AMD 相对 H100 的性能还会持续增长。虽然 H200 是一次重置，但随着更多软件优化，MI300 总体上仍应胜出。

更重要的还是 OEM 和云厂商。Microsoft 当然在支持之列。正如我们过去指出的，Oracle 也将提供支持，他们还公布了 Databricks（MosaicML）等客户。

但支持者不止这些。
