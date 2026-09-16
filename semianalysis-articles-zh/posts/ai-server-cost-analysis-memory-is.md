---
title: "AI 服务器成本分析——内存是最大的输家"
title_en: "AI Server Cost Analysis – Memory Is The Biggest Loser"
subtitle: "美光（Micron，$MU）在 AI 中显得非常弱势"
date: 2023-05-29
source: https://newsletter.semianalysis.com/p/ai-server-cost-analysis-memory-is
crawled: 2026-09-15
authors: ["Dylan Patel", "Gerald Wong"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# AI 服务器成本分析——内存是最大的输家

> 原文：[AI Server Cost Analysis – Memory Is The Biggest Loser](https://newsletter.semianalysis.com/p/ai-server-cost-analysis-memory-is) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**美光（Micron，$MU）在 AI 中显得非常弱势**

为 AI 训练和推理抢建数据中心的狂潮让市场陷入疯狂。例如，Credo（）过去一周上涨了 27%，但他们的受益其实很有限。过去我们曾独家解释过他们如何[失去了唯一的 AI 插槽](https://www.semianalysis.com/p/thick-cables-thin-margins-microsoft)。他们在 AEC 和 ACC 领域还[有 7 家竞争对手](https://www.semianalysis.com/p/thick-cables-thin-margins-microsoft)。Vicor（）上涨了 30%。一年多前，[我们曾独家详述 Vicor 失去了 Nvidia H100 供应商的地位](https://www.semianalysis.com/p/short-report-nvidia-supplier-cut)。虽然 Vicor 曾试图重新拿回设计导入，但在 Monolithic Power Systems（）之后，他们只是一个非常次要的第二选择。

还有许多公司跟着 Nvidia 一飞冲天，但名不副实；反过来，也有许多公司没有得到应有的认可。

IT 预算是有限的。它可以有一定增长，但考虑到宏观经济的不确定性，对大多数企业而言，资本开支（capex）和运营开支（opex）最多只能保持持平。因此，Nvidia 销售额的大爆发直接来自非 GPU 服务器采购的减少。市场已经认识到，由于 AI 支出的转移，传统 CPU 销售将会走弱。这一点清楚地体现在 Nvidia 数据中心营收今年余下时间里将超过 Intel 数据中心业务上。

![](https://substack-post-media.s3.amazonaws.com/public/images/9eacd0f7-a9d5-4555-9f58-6957b6ceac55_718x709.png)

上面是一台标准纯 CPU 服务器的演示性成本拆解。典型的 CPU 服务器配置差异很大，请注意这只是我们认为既高性能又高出货量的配置。对于大批量采购客户，其总成本约 $10,424，其中包含原始设备制造商约 $700 的利润。每插槽 512GB、合计 1TB 的内存占服务器成本的近 40%。服务器上还有其他零散的内存，比如 NIC、BMC、管理 NIC 上的内存，但它们对 DRAM 部分的总成本影响微不足道。我们确实把这些组件计入了上面和下面分享的 BOM 成本中。

NAND 占总 BOM 的 14.7%。诚然，许多用户已转向网络化存储，所以对更现代的架构而言这个数字偏高，但这更多是因为存在另外一些配了大量 NAND、其他配置极简的服务器。[内存整体占经典服务器部署成本的一半以上](https://www.semianalysis.com/p/cxl-enables-microsoft-azure-to-cut)。这些[成本未包含网络部分，我们在早前的报告中已覆盖](https://www.semianalysis.com/p/nvidias-infiniband-problem-qmx-ai)。

总体而言，虽然普通服务器仍会大量存在，但在 AI 时代其占比会下降。按服务器数量计，这一占比会低得多，而按金额计，差距更是巨大。随着数据中心转向加速计算，分配给各种组件的成本占比发生剧变。Nvidia 的 DGX H100 售价约 $270,000。下面的成本拆解包含了 Nvidia 在 GPU + 交换机基板以及整台 DGX 服务器上的加价。

另外，我们还有一份 8 GPU + 4 NVSwitch 基板的 BOM 成本拆解，涵盖供电、内存、组装、散热、GPU 成本、CoWoS 成本、裸片成本、良率成本、HBM 成本等。我们稍后会分享。

![](https://substack-post-media.s3.amazonaws.com/public/images/ffe15f59-3cea-4ac2-a76f-c41771f442cf_754x790.png)

Nvidia 每台 DGX H100 的毛利接近 $190,000。当然，研发及其他运营费用会把这一数字拉低不少。即便如此，这一庞大毛利率伴随着服务器成本中内存占比的大幅下降，尽管每台服务器的 DDR5 内存增长到了 2TB。前端网络中还会有其他基于 CPU 的服务器和存储服务器，但 AI 服务器本身扣除 HBM 后，分配给内存的成本不到总成本的 5%。

HBM 成本显然非常关键，尤其是考虑到 Nvidia 目前所有 HBM3 都是单一供货来源。我们将在下文与订阅用户分享这些成本。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
