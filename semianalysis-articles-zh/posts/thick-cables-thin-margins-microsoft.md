---
title: "粗线缆、薄利润——微软、亚马逊与谷歌的需求被 $CRDO Credo 夸大了"
title_en: "Thick Cables, Thin Margins – Microsoft, Amazon, and Google Demand Overstated By $CRDO Credo"
subtitle: "未来需求蓬勃，但有源电缆（AEC）并非救世主"
date: 2023-02-15
source: https://newsletter.semianalysis.com/p/thick-cables-thin-margins-microsoft
crawled: 2026-09-15
authors: ["Dylan Patel", "Afzal Ahmad"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 粗线缆、薄利润——微软、亚马逊与谷歌的需求被 $CRDO Credo 夸大了

> 原文：[Thick Cables, Thin Margins – Microsoft, Amazon, and Google Demand Overstated By $CRDO Credo](https://newsletter.semianalysis.com/p/thick-cables-thin-margins-microsoft) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**未来需求蓬勃，但有源电缆（AEC）并非救世主**

数据中心网络速度大约每 3 年就如期提升一档，但这种等比例缩放开始遇到一些困难，尤其是 AI 与大语言模型对网络如饥似渴的需求。网络成本的上升速度远快于 CPU 或内存成本，导致数据中心成本急剧膨胀。这是一个需要立即关注的基本性问题。NVIDIA、英特尔（Intel）、AMD 和 Broadcom 等厂商正从 NIC 与交换机的角度着手解决，但这些并非唯一的解决方案空间。

数据中心架构师面临的最大问题之一在于线缆。从 8x25G 到 4x50G 再到 4x100G，每一代网络技术都在给无源直连铜缆（DAC）制造难题。随着数据传输速率的提高，线缆变得更粗、更大、含铜量更多。此外，这些线缆的可靠性在下降，错误率不断攀升。铜缆开始后劲不足，用起来越来越吃力。

要解决这个问题，必须转向另一种线缆形态。显而易见的选择是光纤。最大的挑战在于光收发器太贵。光纤将继续大量用于连接各个服务器机柜，但把服务器连接到机柜内交换机的成本会高得离谱。如果有读者有兴趣与我们的团队见面，几周后我们将在圣地亚哥的 OFC 大会上讨论光 DSP、成本与带宽缩放。

今天我们将讨论解决方案——有源电缆（AEC，active electrical cable），以及亚马逊、微软和谷歌对它的未来使用。此外，我们还将覆盖 AEC 与 ACC 产品的竞争格局以及该领域的公司，包括 Credo（ ）、Astera Labs、Marvell（）、Broadcom（）、Maxlinear（）、Point2、Spectra7、Macom（）、Semtech（）和 Alphawave Semi（£AWE.L）。最后，我们还将讨论这些玩家所使用的 SerDes IP。

![](https://substack-post-media.s3.amazonaws.com/public/images/410efec6-d4d8-4474-b9a8-a7bf6d8a474f_1024x523.jpeg)

为了进一步说明无源铜缆面临的问题，设想一台[微软部署给 OpenAI 用于训练大语言模型的 NVIDIA HGX A100 服务器](https://www.semianalysis.com/p/the-ai-brick-wall-a-practical-limit)。它在 4U 服务器机箱内包含 8 块 200G 或 400G 网络接口卡。视机柜功率/散热架构而定，单个机柜内最多可放置 8 台这样的服务器，并连接到 1 台或多台网络交换机。机柜内部的布线密度之高，仅凭线缆粗细就足以让无源铜缆难以使用。这就迫使布线更长、更杂乱，导致信号衰减、散热恶化、错误传输增多——除非在设计上格外用心。

![](https://substack-post-media.s3.amazonaws.com/public/images/4b1b60cb-97da-41f0-904b-9dea4882e593_800x501.jpeg)

此外，即使是标准 CPU 计算服务器也可能面临类似问题。展望谷歌、微软和亚马逊安装的[搭载 400G NIC 的 AMD Genoa 服务器](https://www.semianalysis.com/p/amd-genoa-detailed-architecture-makes)，如果服务器密度很高，同样的问题也可能出现。就目前而言，在极高密度部署之外的场景，无源直连铜缆（DAC）仍然可用，即使对 4x100G 也是如此。一些缓解策略包括把机柜顶（TOR）交换机移到机柜中部，大幅缩短平均线缆长度，从而得以改回线径更合理的 DAC。

Sun 与 Arista Networks 创始人 Andy Bechtolsheim 总是说，无源铜缆总能再撑一代，而事实也一再如此。这在 200G 和 400G 这一代基本成立。

即便有这种缓解手段，选择 AEC 而非 DAC 还有其他理由。可靠性是关键指标。在当前的服务器机柜架构中，单台 TOR 交换机把机柜内的每台服务器连接到更广的网络。这是一个单点故障。根据微软与 Credo 的这份联合演示，2% 的这类 TOR 交换机会在头三个月内发生故障。

![](https://substack-post-media.s3.amazonaws.com/public/images/da953e10-e276-4594-bc66-5f6b27280de7_2330x1304.png)

如果 TOR 交换机发生故障，该机柜内的每台服务器都会随之下线。SemiAnalysis 认为[亚马逊在单个机柜中使用 32 台 1U Graviton 3 服务器](https://www.semianalysis.com/p/amazon-graviton-3-uses-chiplets-and)。这 32 台服务器中的每一台都包含 3 颗 CPU，每颗 64 核。每台服务器共享一块 NIC，接到 TOR 交换机上。TOR 上的这一单点故障意味着，任何一次故障都可能让多达 6,144 个使用 m7g.medium 或 c7g.medium 实例的客户同时掉线。

业界正在出现一些解决该问题的创新。双 TOR（Dual ToR）、Y 型线缆和 X 型线缆都在开发之中，以便为 NIC、TOR 或两者提供冗余选项。

![](https://substack-post-media.s3.amazonaws.com/public/images/4e9afdde-84fb-45c8-ac51-418a111b3510_3352x1186.png)

技术讲完了，现在让我们谈谈亚马逊、微软和谷歌在 8x25G、4x50G 和 4x100G 下，AEC 在成品 AI 硬件、定制 AI 硬件和通用计算中的具体用途。我们还可以讨论采购策略。此外，我们还将讨论这三家公司的 NIC/交换机选择。最后，我们也会讨论 AEC 产品的时间点，以及来自 Marvell、Astera Labs 和 Alphawave 的 SerDes IP 授权。我们还可以分享 4x25G、4x50G 和 4x100G 的 AEC 与光模块 ASP。

Credo 是 AEC 的先发者，其主要客户是微软，用于 4x50G 的 AI 应用，包括上述 NVIDIA HGX A100 的例子。这包括 [ND A100 v4 系列实例](https://learn.microsoft.com/en-us/azure/virtual-machines/nda100-v4-series)——大多数训练负载的主力机型。据称 InfiniBand 交换机当时的可靠性较低，这正是微软与 Credo 案例中指出的问题。这是 Credo 双 TOR 技术的主要驱动因素。

在这个案例中，微软选择 AEC 纯粹是为了 InfiniBand 部署中的这一可靠性优势。AEC 在线缆走线距离上的好处无关紧要，因为在 <3m 的布线长度下，微软用 DAC 替代 AEC 同样不会带来可察觉的错误率上升。同样，在 4x50G 的超大规模出货量下，AEC 相对光模块并无成本优势，两者 ASP 相近。双 TOR AEC 的 ASP 高于标准的 1:1 光模块。再加上第二台交换机，从基础设施角度看这就非常昂贵了。

编辑注： 今日股价从 $19.36 跌至 $10.30，跌幅近 50%，与我们在此处及报告其余部分所描述的事件相关。微软只是小规模地部署了 AEC。随着 InfiniBand 交换机可靠性的提升，他们逐步淘汰了这项技术。微软在这一 AI 应用中已经转回更便宜的 DAC 与多模光模块方案。

[分享](https://newsletter.semianalysis.com/p/thick-cables-thin-margins-microsoft?utm_source=substack&utm_medium=email&utm_content=share&action=share)

奇怪的是，直到现在 Credo 才提醒投资者，而卖方早已乐此不疲地对这门生意疯狂臆测。一些卖方甚至买方还说，Credo 今年仅向微软一家就会以 $200 的 ASP 卖出 50 万条 AEC。这并没有发生。相反——

[团体订阅立减 20%](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
