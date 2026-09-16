---
title: "Meta 诡异的 AI 基础设施选择让他们多花了数亿美元"
title_en: "Meta's Bizarre AI Infrastructure Choice Costs Them $100s of Millions"
subtitle: "Meta 正以更高功耗为同样的性能支付更高成本。"
date: 2023-05-06
source: https://newsletter.semianalysis.com/p/metas-bizarre-ai-infrastructure-choice
crawled: 2026-09-15
authors: ["Dylan Patel", "Gerald Wong"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Meta 诡异的 AI 基础设施选择让他们多花了数亿美元

> 原文：[Meta's Bizarre AI Infrastructure Choice Costs Them $100s of Millions](https://newsletter.semianalysis.com/p/metas-bizarre-ai-infrastructure-choice) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Meta 正以更高功耗为同样的性能支付更高成本。**

在 AI 能力上，Meta 稳居前三，仅次于 Microsoft/OpenAI 和 Google。他们创新并推向市场了大量软件，包括 [PyTorch](https://www.semianalysis.com/p/nvidiaopenaitritonpytorch)、[LLAMA](https://ai.facebook.com/blog/large-language-model-llama-meta-ai/)、[Cicero](https://ai.facebook.com/research/cicero/diplomacy/)、[最先进的深度学习推荐模型](https://arxiv.org/pdf/2104.05158.pdf)、[RecD](https://research.facebook.com/publications/recd-deduplication-for-end-to-end-deep-learning-recommendation-model-training-infrastructure/)、[Segment Anything](https://ai.facebook.com/blog/segment-anything-foundation-model-image-segmentation/) 等等。因此，Meta 也拥有最庞大的 AI 基础设施之一，这毫不意外。事实上，我们的数据显示，Meta 今年采购的 Nvidia H100 GPU 将超过包括 Microsoft 在内的任何其他公司。尽管如此，Meta 的一切并非阳光和彩虹。

Meta 历来在 AI 基础设施上做过非常奇怪的选择。首先，他们在较小的推荐模型上过度依赖 CPU，尽管 GPU 在总拥有成本（TCO）上要优越得多。随后，他们在 7nm 自研 AI 芯片上的尝试也搞砸了——无论以何种合理的标准衡量，那些项目都是失败。

尽管 Meta 终于在 Nvidia GPU 上全力以赴……

> 我们已经把模型从以 CPU 为主转向以 GPU 为主。当前的资本开支（CapEx）激增确实源于 AI 基础设施的建设，我们去年真正开始，并延续到今年。
>
> [Meta 2023 年 2 月财报电话会](https://s21.q4cdn.com/399680738/files/doc_financials/2022/q4/META-Q4-2022-Earnings-Call-Transcript.pdf)

但这并不意味着他们诡异的基础设施选择已经绝迹。Meta 目前正在部署价值数十亿美元的服务器，其所用芯片会推高成本、增加功耗，而最糟的是，还会因增加延迟而降低性能。这一基础设施选择的收益从非常有限到几乎为零，而实施它将花费他们数亿美元。

今天我们想深入剖析 Meta 这一诡异的选择，并解释他们为何这么做。我们也想解释替代方案是什么。最后，我们想深入讨论 Microsoft 等公司对那一替代方案的采用。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
