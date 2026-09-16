---
title: "GPU 云经济学解析——隐藏的真相"
title_en: "GPU Cloud Economics Explained – The Hidden Truth"
subtitle: "CPU 云与 GPU 云的差异、TCO 模型、PUE、超大规模云厂商的劣势"
date: 2023-12-04
source: https://newsletter.semianalysis.com/p/gpu-cloud-economics-explained-the
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# GPU 云经济学解析——隐藏的真相

> 原文：[GPU Cloud Economics Explained – The Hidden Truth](https://newsletter.semianalysis.com/p/gpu-cloud-economics-explained-the) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**CPU 云与 GPU 云的差异、TCO 模型、PUE、超大规模云厂商的劣势**

过去一年，纯 GPU 云的数量出现了爆发式增长。我们没有开玩笑——先后有十几家不同公司的股权或债权融资方案为此目的送到我们桌上，市面上很可能还有更多我们根本没见过的。交易流终于放缓了，正好让我们公开地、更深入地审视一下这背后的经济学。

首先要快速澄清的一点是，新云厂商大规模涌入的总体动因。虽然确实存在一组独特的基础设施挑战，但从软件角度看，GPU 云比通用云的运营难度低得多。第三方纯 GPU 云不需要操心高级数据库服务、块存储、多租户安全保证、面向各类第三方服务商的 API，在很多场景下甚至连虚拟化都无关紧要。

关于「除了一流的模型之外，云上开发的软件对 AI 有多不重要」，AWS 提供了一个极其滑稽的例证。AWS 热衷于鼓吹其 SageMaker 平台是客户在云端创建、训练和部署模型的利器，但这明显是「照我说的做，别照我做的做」。[Amazon 自家最好的模型 Titan](https://blogs.nvidia.com/blog/nemo-amazon-titan/)，用的就是 [NVIDIA 的 NeMo 框架](https://blogs.nvidia.com/blog/nemo-amazon-titan/)而非 SageMaker。注意，Titan [明显逊于众多开源模型](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)！虽然 NeMo 和 SageMaker 并非完全同类事物，但它足以说明云厂商的「增值」软件有多不重要。

此外，标准云需要在算力、存储、内存和网络方面具备极致的灵活性与可替换性，而由于工作负载相对同质，GPU 云需要的选项要少得多。服务器通常以很长的周期锁定，而 H100 基本上是所有现代用例的最优 GPU，包括 LLM 训练和大批量 LLM/扩散模型推理。终端用户的基础设施选择主要就是需要多少张 GPU。当然，你需要确保网络性能过关，但在网络开支上花过头对多数用户并不是大问题，因为网络成本[相对于 GPU 而言微不足道](https://www.semianalysis.com/p/ai-server-cost-analysis-memory-is)。

对于除最大用户之外的所有人，训练和推理时现有数据的本地性甚至都不太重要，因为[出口带宽成本极低](https://www.semianalysis.com/i/108660819/amazon-scale-to-service)。数据可以做转换和传输，而高性能存储对云厂商来说从 Pure、Weka、Vast 等处采购也并非难事——同样，与其他项目一样，存储只占 AI 基础设施成本的很小一部分。

## **CPU 与 GPU 托管（Colo）总拥有成本（TCO）对比**

即便不考虑 GPU 云缺乏护城河这一问题（与 NVIDIA 的亲密关系除外），新厂商爆发的真正驱动因素，是托管（colo）环境下 CPU 服务器与 GPU 服务器总拥有成本（TCO）的公式差异。CPU 服务的 TCO 有更多需要权衡的重要因素，而 GPU 由于 NVIDIA 极高的利润率，几乎完全由资本成本主导。

换言之，既然真正的进入门槛只有资本而非物理基础设施，出现这么多新入局者也就不足为奇了。

![](https://substack-post-media.s3.amazonaws.com/public/images/27a54ff5-da5e-42ce-acb9-d4dddecb9ae3_1518x1323.png)
*OEM 定价，网络成本计入服务器层面，而非超大规模级别*

以 CPU 服务器为例，各项托管成本（每月 $220）与资本成本（每月 $301）处于同一量级。再对比 GPU 服务器：各项托管成本（每月 $1,871）在资本成本（每月 $7,025）面前完全不值一提。这就是第三方云能够存在的核心原因。

Google、Amazon、Microsoft 这样的超大规模云厂商可以通过更出色的数据中心设计与运营能力大幅优化托管成本。以电源使用效率（PUE）这一指标为例，它比较的是数据中心总耗能与输送给计算设备的电能之比。降低该指标的努力通常围绕散热与供电展开。Google、Amazon 和 Microsoft 很厉害，它们的 PUE 正尽可能接近 1。

多数托管（colo）设施通常明显更差，约在 1.4+，意味着约 40% 的电力损耗在散热与输电上。即便是 GPU 云最新的设施也只能做到 1.25 左右，仍显著高于大型云厂商——后者还因各种规模优势能以更低成本建设数据中心。这一差异对 CPU 服务器极其重要，因为 colo 更高的托管成本占 TCO 的很大比例。而对 GPU 服务器来说，尽管托管成本高昂，但在大局上真的无关紧要，因为托管成本占比很小，服务器资本成本才是 TCO 公式中的主导因素。

一个相对平庸的数据中心运营者，用 13% 利率的债务买入 NVIDIA HGX H100 服务器，算下来的全包时薪成本仍可低至 $1.525。更优秀的运营者在此之上还能做很多优化，但资本成本才是主要旋钮。反过来，即便最优惠的 GPU 云交易，每张 H100 也要约 $2 一小时，我们还见过走投无路的人被宰到每小时 $3 以上。云厂商的回报率惊人……

当然，这是一个简化框架。许多变量都可能变化，并彻底改变成本公式。我们甚至见过 CoreWeave 试图向人兜售 8 年生命周期，但那套数学完全是胡说八道。

事实上，上表中的许多假设并不代表当今 colo 的现实。我们在下面给出更符合实际的数字。

让我们深入剖析并解释这个简化模型。

[获取团体订阅 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
