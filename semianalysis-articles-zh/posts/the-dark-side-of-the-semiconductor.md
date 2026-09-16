---
title: "半导体设计复兴的阴暗面——光罩组、验证与确认导致固定成本飙升"
title_en: "The Dark Side Of The Semiconductor Design Renaissance – Fixed Costs Soaring Due To Photomask Sets, Verification, and Validation"
date: 2022-07-24
source: https://newsletter.semianalysis.com/p/the-dark-side-of-the-semiconductor
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 半导体设计复兴的阴暗面——光罩组、验证与确认导致固定成本飙升

> 原文：[The Dark Side Of The Semiconductor Design Renaissance – Fixed Costs Soaring Due To Photomask Sets, Verification, and Validation](https://newsletter.semianalysis.com/p/the-dark-side-of-the-semiconductor) · SemiAnalysis

我们正处于一场半导体设计复兴之中。世界上几乎每家大公司都有自己的芯片战略，试图实现垂直整合。芯片初创公司也比以往任何时候都多。行业正在迅速摆脱「一切皆用英特尔 CPU」的模式。随着摩尔定律放缓，设计正涌向针对特定任务更加专业化的异构架构。在软件难题被解决的前提下，专用芯片的性能大幅超越 CPU，但这种专业化策略也有其阴暗面：固定成本在爆炸式增长，而这些设计的出货量被大幅压缩。半导体是一个规模经济行业，而且随着每一代新技术演进，这一点正变得愈发明显。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ddefd035-f1c1-4e62-b752-8217a4d8a48a_1024x1024.jpeg)
*SONY DSC*

晶圆制造是一个循环：用光刻定义图形，再用沉积、刻蚀等工艺步骤把它们构建出来。半导体的先进制程需要用到 60 多个不同的光刻层及相应工序。其中每一层都需要一张独一无二的光罩（photomask）。全部光罩的集合称为光罩组（mask set）。这些光罩组把芯片架构师的设计转换为物理图形。用最通俗的话说，光罩组可以被看作一组模板，上面承载着芯片的设计。每一个独特的芯片设计都需要自己的光罩组。

业界有许多降低芯片设计成本的巧妙手段，但把设计推向市场的最大障碍是光罩组的成本。在代工厂制程节点上，90nm 到 45nm 时代，光罩组的成本大约在数十万美元量级；到 28nm，成本突破 $1M；到 7nm，成本超过 $10M；而如今，随着我们跨过 3nm 门槛，光罩组成本将开始向 $40M 区间迈进。

*特别感谢 SPIE Advanced Lithography + Patterning 会议提供了许多聚焦光罩、光刻、图形化与量测的精彩演讲，指出了这一成本问题以及后续如何扩展。*

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/cfddb567-1f1f-4128-aaf5-43f700c8b7ec_898x702.png)

晶圆价格在上涨，但光罩组成本的上涨速度快得多。上面这张来自 IC Knowledge 的图表展示了这一困境：要享受晶体管微缩带来的经济性改善，不同制程技术时代的出货量必须显著提高。

有些人认为晶体管成本在 28nm、7nm、5nm 等各个制程节点停止了下降。宣称晶体管成本已经停止下降、开始上升的人，其数量似乎正以快于摩尔定律的速度翻倍。需要明确的是：即便在 5nm 乃至 3nm 代工制程上，每晶体管成本仍在持续下降，但这只属于那些拥有大批量晶圆投片的玩家。芯片设计很昂贵，但远没有 IDC 和麦肯锡装出来的那么夸张。请看他们那张错误的图表。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/b93fa74f-3623-4842-b790-bee03d0ec070_1024x525.png)

我们曾与多家芯片初创公司合作，他们在台积电（TSMC）7nm 上打造先进芯片的总花费为 $50M 到 $75M。这一成本涵盖其全部软件、设计和流片（tape-out）费用。这些成本会因芯片类型不同而差异巨大。

随着行业向更先进制程演进、成本持续攀升，将有更多公司的出货量不足以摊销与光罩组相关的固定成本，从而无法享受每晶体管成本下降带来的好处。

刚刚踏上芯片设计之路的初创公司和非半导体公司，不仅要面对更高的盈亏平衡出货量门槛，还必须应对巨大的风险。最大单项成本是设计确认（validation）与验证（verification）。如果确认与验证流程不够过硬，公司就要面临产品的大幅延期。这些问题甚至同样困扰着行业内最大的玩家。

英特尔的制程技术落后了，但鉴于台积电在 3nm 上最新的磕绊，如果英特尔能快速爬坡，Intel 4 和 Intel 3 制程节点有可能与台积电最好的制程一较高下。但即便英特尔在制程技术上追平台积电，它还有其他可能无法逾越的障碍。在我们看来，英特尔面临的最大问题与其设计确认与验证流程有关。为便于说明，我们来看英特尔的数据中心芯片。

Ice Lake 是英特尔当前的服务器芯片，首次上电（powered on）是在 2018 年 12 月。产品发布是 2021 年 4 月，而放量爬坡直到 2021 年第三、第四季度才开始。英特尔大概率在 2018 年初就完成了 Ice Lake 的首次 tape-in（汇聚 IP 开始制作光罩组）。Tape-in 之后，tape-out 是指首批晶圆使用新制成的光罩组流过晶圆厂。英特尔完成这些晶圆并封装芯片以启动测试是在 2018 年底。这是芯片的第一轮流片（spin），但 Ice Lake 需要多轮流片才能完全可用。每一轮新流片至少需要部分新光罩，通常在关键层上，意味着非常高的成本。

英特尔的下一代服务器芯片 Sapphire Rapids 在确认与验证上也面临类似问题。Sapphire Rapids 设计的第一版在 2020 年 6 月上电。而到 2022 年年中的现在，英特尔仍在因设计早期未能发现的问题修改设计和光罩组。这主要是确认与验证问题。Sapphire Rapids 看起来会在 2022 年晚些时候发布，但放量爬坡目前预计要拖到 2023 年初。

英特尔的确认与验证问题大幅推高了成本、拉长了时间线。被迫修改光罩对英特尔的成本影响不算大，因为它的出货量巨大，但延期对竞争力的影响非常大。每一轮修订至少需要部分新光罩、把晶圆流过产线、再封装芯片，整个过程需要数月。Ice Lake 用了 6 轮修订才得以出货，而 Sapphire Rapids 看起来糟糕得多：他们已经做了 12 个步进（stepping）仍未完全验证到可以批量出货的程度。A0、A1、B0、C0、C1、C2、D0、E0、E2、E3、E4，以及现在的 E5。

相比之下，被认为行业顶尖的设计公司如 AMD 和 Nvidia 所需的时间只是其中一小部分。以拥有非常完善的自研仿真、确认与验证流程著称的 Nvidia，在很多情况下甚至用时不到一年。英特尔这种巨头某种程度上还能承受这些问题，尽管这正是它衰落的原因。目前有大量力量在推动彻底改革和修复这一流程，我们希望英特尔能做到，但对此要打一个大大的问号。

现在想象一下，一家初创公司或非半导体公司里全新组建的芯片设计团队如果栽了跟头会怎样。这种延期足以杀死一个具体的芯片项目，Meta 和微软就曾如此；甚至可能拖垮整家公司或整个战略。随着半导体设计复兴的蓬勃发展，前景并不会全是玫瑰色。

失败设计的尸骸将一路铺陈。较成熟的公司可能会有一些完全垂直的设计，但它们也会转向与 Broadcom、Marvell、英特尔、AMD 等的半定制（semi-custom）交易。初创公司的日子要艰难得多，因为预算紧得多。我们认为，AI 芯片初创公司的洗牌很可能是最先显现的地方。多家高知名度 AI 初创公司已经出现裁员，而这只是开始。尽管如此，仍会有许多初创公司成长起来并赚到大钱。这是一个赌注极高的游戏。

[分享](https://newsletter.semianalysis.com/p/the-dark-side-of-the-semiconductor?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[发表评论](https://newsletter.semianalysis.com/p/the-dark-side-of-the-semiconductor/comments)
