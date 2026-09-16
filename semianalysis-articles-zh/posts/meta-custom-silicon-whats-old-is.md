---
title: "Meta 定制芯片：旧的就是新的"
title_en: "Meta Custom Silicon: What's Old Is New"
subtitle: "面向 AI 与视频的半定制芯片、路线图、协同设计伙伴"
date: 2023-05-19
source: https://newsletter.semianalysis.com/p/meta-custom-silicon-whats-old-is
crawled: 2026-09-15
authors: ["Dylan Patel", "Gerald Wong"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Meta 定制芯片：旧的就是新的

> 原文：[Meta Custom Silicon: What's Old Is New](https://newsletter.semianalysis.com/p/meta-custom-silicon-whats-old-is) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**面向 AI 与视频的半定制芯片、路线图、协同设计伙伴**

Meta 刚刚发布了一大批与其内部 AI 基础设施和芯片相关的公告。话题包括转向更多液冷、更高功率的数据中心，以及园区层面的变革。至于芯片方面，有趣的是，Meta 正在采取[与 Google 一模一样的策略](https://www.semianalysis.com/p/google-ai-infrastructure-supremacy)。

Meta 只谈他们已经有的旧芯片，而恰好此时新芯片已接近就绪。例如，[他们为一座去年建成的、拥有 16,000 块 Nvidia A100 的研究集群发布了整篇博客](https://ai.facebook.com/blog/supercomputer-meta-research-super-cluster-2023/)，而这发生在他们已经开始用 H100 建设大得多的集群之后。正如我们此前报道的，[那座 H100 集群的基础设施配置非常诡异](https://www.semianalysis.com/p/metas-bizarre-ai-infrastructure-choice)。

本报告将覆盖 Meta 自 2021 年以来就拥有的旧芯片，以及 Meta 目前正在开发的新芯片。我们将讨论架构、路线图、各家设计伙伴以及未来野心。

## **Meta 可扩展视频处理器（MSVP）**

Meta 正在展示其自 2021 年起就在部署的视频编码 ASIC。对公司而言，视频编码 ASIC 是极其重要的一块基础设施。例如，这正是 [Amazon 的 Twitch 直播服务明显逊于 Google YouTube 的首要原因](https://www.semianalysis.com/p/amazon-web-services-infrastructure)。

![](https://substack-post-media.s3.amazonaws.com/public/images/3bb9aa4a-047a-4193-8c05-2ea09926fc46_1015x646.png)

[Google 是第一家设计视频编码芯片的公司，代号 Argos，我们多年前就报道过](https://www.semianalysis.com/p/google-new-custom-silicon-replaces)。大规模部署的 Google Argos VPU 完成了[超过 1,000 万颗 Intel CPU 的 VP9 编码工作，为 Google 节省了数十亿美元成本](https://www.semianalysis.com/p/google-new-custom-silicon-replaces)。我们还[报道过 NetInt 的 VCU](https://www.semianalysis.com/p/meet-netint-the-startup-selling-to)——一家拥有类似视频编码 ASIC 的初创公司，其芯片卖给 [ByteDance、百度、腾讯和阿里巴巴等公司](https://www.semianalysis.com/p/meet-netint-the-startup-selling-to)。

Meta 的 Instagram 和 Facebook 上有海量的视频上传，所以这款产品对降低成本至关重要。此外，正是 Meta 第二代可扩展视频处理器让他们能够在 Reels 中如此普遍地部署 AV1。注意，Meta 今天只披露了第一代。

![](https://substack-post-media.s3.amazonaws.com/public/images/0521aa4d-11a8-4728-aa7c-c93fa35da1e9_1670x876.png)

Meta 声称这颗芯片是自研的，但事实并非如此。已发布的 MSVP 和即将推出的下一代版本都是与 Broadcom 协同设计的。Google 前两代视频编码 ASIC 也是与 Broadcom 协同设计的。

每颗 MSVP ASIC 芯片拥有最高 4K 的转码能力：在最高质量设置、1 路输入流转 5 路输出流的配置下以 15fps 运行。在标准质量配置下，它可以扩展到 4K@60fps。Meta 声称性能随分辨率的提升而均匀扩展。这一切都在 PCIe 模块约 10W 的功耗下实现。H.264 有 9 倍的性能提升，VP9 有 50 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/20520b74-84c7-4585-8b04-60d0ca52ccd7_1100x220.png)

该芯片采用 M.2 22110 规格，支持 4 通道 PCIe Gen 4，即 8GB/s。展示板上还配有 2 颗 4GB 美光（Micron）LPDDR5，合计 8GB，内存带宽 88GB/s。封装尺寸约 ~24mm x 19mm，裸片面积约 ~112mm²。

![](https://substack-post-media.s3.amazonaws.com/public/images/ea228b57-e627-4f95-9460-d6f33d32777a_816x578.png)

Meta 视频中展示的芯片生产于 6 月 21 日至 6 月 27 日期间。

## **Meta 训练与推理加速器（MTIA）**

[AI 是 Meta 数据中心中最重要、成本最高的工作负载](https://www.semianalysis.com/p/google-ai-infrastructure-supremacy)。Meta 至少从 2019 年起就在开发自己的 AI 芯片。第一代刚刚发布，虽然这类处理器的名称是 Meta 训练与推理加速器（MTIA），但需要说明，第一代只能用于推理。

Meta 当前的主力工作负载是 [DLRM 推理](https://www.semianalysis.com/i/114314781/the-largest-at-scale-ai-model-architecture-dlrm)，因此他们试图让芯片架构特别贴合这一工作负载。提醒一下，[DLRM 模型至今仍是最大规模的 AI 工作负载](https://www.semianalysis.com/i/114314781/the-largest-at-scale-ai-model-architecture-dlrm)。这些 DLRM 是百度、Meta、ByteDance、Netflix 和 Google 这类公司的支柱。它是广告、搜索排序、社交媒体信息流排序等领域每年超过一万亿美元营收的引擎。

虽然生成式 AI 很快将在硬件需求上超过它，但这个反转尚未发生。[我们此前对 DLRM 的深度解析见这里](https://www.semianalysis.com/i/114314781/the-largest-at-scale-ai-model-architecture-dlrm)。

![](https://substack-post-media.s3.amazonaws.com/public/images/6e5e6d83-96ad-4de8-ad22-f1eca1665e79_1852x933.png)

DLRM 模型还在持续增长，这正给 Meta 带来重大的基础设施变革。有一段时间，他们大量使用 [Intel 的 NNP-I 推理加速器](https://en.wikichip.org/wiki/nervana/nnp/nnp-i_1100)，但很快就被 GPU 取代。在某些方面，第一代 MTIA 可以看作第二代 NNP-I，因为两者的系统架构（而非微架构）非常相似。

![](https://substack-post-media.s3.amazonaws.com/public/images/7172c4fb-9776-496f-bcd9-52f0799c6709_1876x930.png)

Meta 很多年前就启动了半定制 AI 加速器项目，目标非常明确：为更好的 DLRM 模型实现更低成本的推理，以及易用性。他们的第一代可以看作一个软件载具，用于培育借助 LLVM 编译器使用 PyTorch 2.0 eager 模式和完整图模式的能力。他们正在实现 Dynamo、Inductor 和 Triton。

![](https://substack-post-media.s3.amazonaws.com/public/images/14439890-f74c-4178-96b4-8d1abef7ef71_1891x991.png)

[我们的数据显示，Meta 是今年 Nvidia H100 GPU 最大的单一买家。](https://www.semianalysis.com/p/metas-bizarre-ai-infrastructure-choice)这绝非巧合。Meta 在训练和推理两端都需要 GPU，而 H100 是他们在多数场景下满足这一需求最具性价比的方式。

![](https://substack-post-media.s3.amazonaws.com/public/images/90ef9f49-9671-49d9-a3c6-6b098db107ba_1854x933.png)

Meta 分享了其各类生产推荐模型的画像。这些模型的大小和复杂度各不相同。Meta 还分享了各种硬件在这些工作负载上的性能。

![](https://substack-post-media.s3.amazonaws.com/public/images/e5958378-ad43-40b1-8709-d54547d280ee_1656x904.png)

Meta 没有说明对比的是哪款 GPU，我们多方打听后得知，那似乎是旧的 Ampere GPU，而不是新的 Hopper 和 Lovelace GPU。这看起来不公平，但请记住，Meta 第一代 MTIA 也是一颗较旧的芯片。一旦叠加新 Nvidia 芯片的额外性能，第一代 MTIA 在多数工作负载的每瓦性能上都会落败。

话虽如此，第一代 MTIA 只是个开始。让我们先深入剖析这颗芯片，再讨论下一代、路线图和设计伙伴。

Meta 在视频中展示的芯片早在 2021 年就拿到了。MTIA 在 TSMC 的 7nm 工厂制造，由 Amkor 封装。芯片上的标记显示生产时间为 2021 年 8 月 23 日至 8 月 29 日。

该芯片拥有 102.4 TOPS 的 INT8 算力和 51.2 TFLOPS 的 FP16 算力，TDP 为 25W。芯片上共有 128MB SRAM，运行速率 800GB/s。这些 SRAM 位于内存控制器旁边，既可以作为内存侧缓存，也可以被直接寻址为可寻址内存。此外还有最高 128GB 的 LPDDR5-5500，挂在 256-bit 总线上，带宽 176GB/s。值得注意的是，Meta 使用的 LPDDR5 额定速率可达 6400 MT/s，却被降频运行。芯片还有 8 条 PCIe 4.0 通道。

内存与 IO 环绕在处理元件周围。这些处理元件组成一个 8 x 8 的阵列，包含一个命令处理器、本地内存，以及两颗来自 Andes 的不同 RISC-V CPU。其中一颗只有标量能力，另一颗既能做标量也能做向量。这些核心从第三方 IP 公司授权而来。该第三方不协助后端设计。

![](https://substack-post-media.s3.amazonaws.com/public/images/2af2c46b-f8f9-4c2a-a66c-b1d5c6b3f9d6_1909x960.png)

芯片上还有多种固定功能加速器，用于加速矩阵乘法、非线性函数和数据搬运。

物理上，该芯片以 PCIe Gen 4x8 双 M.2 卡的形式插在 Delta Lake 服务器中，连接 Intel Copper Lake CPU、96GB DDR4，并通过 PCIe 3.0 x24 连接到嵌套交换机（80 通道 Broadcom PCIe4 交换机）。

每台主机 12 颗 MTIA，整个系统功耗 780W。

[分享](https://newsletter.semianalysis.com/p/meta-custom-silicon-whats-old-is?utm_source=substack&utm_medium=email&utm_content=share&action=share)

## **芯片协同设计伙伴与路线图**

接下来，我们将讨论路线图、芯片代号、MTIA 的未来，以及它在哪些场景有用、哪些场景没用。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
