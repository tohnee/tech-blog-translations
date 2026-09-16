---
title: "Astera Labs IPO：下一个连接芯片超级英雄，还是会被竞争碾压？"
title_en: "Astera Labs IPO - The Next Connectivity Superhero or Steamrolled By Competition?"
subtitle: "自下而上模型、出货量、ASP、营收、分超大规模云厂商分析、EPS 与现金流、竞争分析"
date: 2024-03-17
source: https://newsletter.semianalysis.com/p/astera-labs-ipo-the-next-connectivity
crawled: 2026-09-15
authors: ["Dylan Patel", "Jeremie Eliahou Ontiveros"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Astera Labs IPO：下一个连接芯片超级英雄，还是会被竞争碾压？

> 原文：[Astera Labs IPO - The Next Connectivity Superhero or Steamrolled By Competition?](https://newsletter.semianalysis.com/p/astera-labs-ipo-the-next-connectivity) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**自下而上模型、出货量、ASP、营收、分超大规模云厂商分析、EPS 与现金流、竞争分析**

AI 基础设施的淘金热正为供应关键使能技术的公司创造巨大机遇。在这场基础设施建设的盛宴中，并非人人都是 NVIDIA，也有许多小型关键玩家。今天我们深入聊聊 Astera Labs——它的芯片已悄然出货到超过 80% 的 AI 服务器中。

Astera Labs 是一家数据中心连接芯片纯玩家（pure-play），主要面向三类客户：超大规模云厂商、AI 加速器厂商和系统 OEM。Astera Labs 的产品组合目前包括三大系列：Aries 重定时器（retimer）、Taurus 有源电缆（AEC）小板（paddle board）模块，以及 Leo CXL 内存控制器。我们此前覆盖过它所处的一些市场，最引人注目的是 [CXL](https://www.semianalysis.com/p/cxl-is-dead-in-the-ai-era) 和 [AEC](https://www.semianalysis.com/p/thick-cables-thin-margins-microsoft)。

![](https://substack-post-media.s3.amazonaws.com/public/images/138b1bdd-6d05-4187-bca4-e020bb10ba11_2384x1044.png)
*Astera Labs*

连接（芯片）历来是数据中心市场中竞争极其激烈、但粘性很高的高利润率板块。尽管在交换芯片和 DSP 领域出现过无数次竞争尝试，Broadcom 和 Marvell 依然以超过 80% 的营收份额和 >65% 的毛利率稳居统治地位。

所有人都在问的头号问题是：Astera Labs 是靠入场早而一举撞大运（把闪电装进了瓶子），还是先发优势根本无关紧要、竞争对手终将进场把它碾平。我们将讨论其所有主要市场中的主要竞争对手，包括 Marvell Technologies、Broadcom、Montage Technology（澜起科技）、Parade Technologies（谱瑞）、Rambus、Microchip、XConn 和 Credo。Astera Labs 可能逐渐消逝，也可能成为下一个连接芯片超级英雄——前提是它保持高 retimer 市场份额，并扩张到 AEC 和各类 CXL 产品。

在本报告中，我们将分享对营收、EPS、市场规模等的预测。我们的方法自下而上，基于各公司/各类型的 [AI 加速器](https://www.semianalysis.com/p/accelerator-model)与 CPU 出货量为这些市场建模 ASP 与出货量。我们还考虑了连接产品在各超大规模云厂商处的长期订单/份额情况。

在此之前，先回顾一下 Astera Labs 的历史。

## **Astera Labs 如何解决连接瓶颈**

Astera Labs 于 2017 年在一间车库里成立，颇具硅谷经典风格。三位联合创始人 Jitendra Mohan、Sanjay Gajendra 和 Casey Morrison 此前都在德州仪器的高速接口业务。他们看到，由于算力的指数级增长，以及 AI 工作负载与超大规模云计算所驱动的异构计算需求，世界上的连接瓶颈与日俱增。

> Astera Labs 做的就是消除瓶颈的生意——无论瓶颈出现在系统的哪个角落。
>
> Jitendra Mohan

下图展示了 Astera Labs 着力解决的三大瓶颈。

![](https://substack-post-media.s3.amazonaws.com/public/images/fb4929d4-f743-4d80-88ef-0befc10979d0_1200x611.png)
*Astera Labs*

公司最初的焦点是 PCIe 及相关协议，例如 CXL。PCIe 4.0 规范于 2017 年发布，首次正式定义了「redriver（重驱动器）」和「retimer（重定时器）」这两个术语。redriver 本质上是一种模拟信号放大器件，用来抵消 PCB 造成的随频率变化的衰减。简单说，它就是把信号放大，可以想象成一个「扩音喇叭」。redriver 最大的缺点是它会把信号路径上的噪声也一并放大。在 PCIe Gen 1 到 Gen 3 时代这还算够用，但到 Gen 4 就开始带来挑战，Gen 5 更快的数据速率进一步加剧了问题。下图展示了各代 PCIe 与各种 PCB 材料的每英寸损耗。

![](https://substack-post-media.s3.amazonaws.com/public/images/1e1a140c-e0d3-4705-a0d0-9098101084ff_1722x654.png)
*Planet Analog*

为了补偿信号损耗，首选方案是使用更高质量的 PCB 材料，但这成本高昂。例如，PCB 材料「Megtron 6」的价格大约是最流行、最具性价比的材料「FR4」的七倍。请记住，PCIe 规范有精确的插入损耗预算；以 PCIe 5.0 为例，在 32 GT/s 下端到端（bump-to-bump）为 36 dB，误码率低于 10^-12。

![](https://substack-post-media.s3.amazonaws.com/public/images/f204e8d2-0f0b-4a0c-ae48-19beffe19f74_2059x1137.png)
*Astera Labs*

Astera Labs 的立业之本就是解决 PCIe 4 和 PCIe 5（规范于 2019 年发布）的连接挑战。他们围绕解决这些信号完整性挑战、设计基于 retimer 的方案建立了这家公司。retimer 是一种具备协议感知能力的数模混合信号器件，能够完整恢复数据、提取嵌入式时钟，并用干净的时钟重新发送一份「全新」的数据。简单说，如果说 redriver 是「扩音喇叭」，那 retimer 就是高品质麦克风 + 专业音频设备，把校正后的信号送进音箱。retimer 是一颗小芯片，执行 PCIe SerDes 功能，同时监测并采集信号完整性数据。下图展示了一个典型架构。

![](https://substack-post-media.s3.amazonaws.com/public/images/6379a3ea-55fa-431f-8d58-28b7b8533c6f_787x440.png)
*PCI-SIG*

retimer 可以把信号链路一分为二，显著降低信道损耗。下图展示了这些芯片如何集成到 PCB 上。它也说明，低损耗 PCB、甚至超低损耗 PCB，也未必能把信道损耗压到要求的范围之内。

![](https://substack-post-media.s3.amazonaws.com/public/images/c0c6ff9c-8b36-41be-a596-41241404ac28_2400x1134.png)
*PCI-SIG*

Astera Labs 凭借面向 PCIe 4.0 以及 PCIe 5.0 的 Aries 智能重定时器率先进入市场，并在 2019 年拿下首批设计导入（design win）。量产于 2020 年启动，采用台积电（TSMC）工艺；2021 年，公司实现营收 $34.8M。他们拥有一批优质投资者，如 Fidelity、Atreides Management、Intel Capital 和 Sutter Hill Ventures。IPO 前的最后一轮融资发生在拒绝 Marvell 的收购邀约之后。

Astera 公布了打造全球连接平台的愿景，又推出了两条产品线：CXL 内存控制器和智能线缆模块（Smart Cable Module）。下图描绘了 Astera Labs 的愿景。

![](https://substack-post-media.s3.amazonaws.com/public/images/209beb23-35a4-4df3-a2d0-398e409444ca_2496x754.png)
*Astera Labs*

2023 年开局不顺：受通用数据中心与网络市场库存调整的拖累（其背后又是[其最大超大规模云客户的云危机](https://www.semianalysis.com/p/amazons-cloud-crisis-how-aws-will)），第一季度和第二季度疲软且持续下滑。但故事并未就此结束：2023 年第三季度和 2024 年第四季度出现了爆发式增长。那么，这中间发生了什么？这可持续吗？

![](https://substack-post-media.s3.amazonaws.com/public/images/6cfec880-2d61-43a0-84d2-82a78aae3059_938x541.png)
*Astera Labs 招股书（Form S-1）*

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

要回答这个问题，让我们更深入地了解 Aries 产品系列及其主要应用。

## **面向 AI 与云应用的 Aries 重定时器**

简短的回答是肯定的：随着 AI 加速器需求持续火爆，PCIe retimer 市场也将随之增长。事实上，每块加速卡内部都包含一颗 retimer。如下图所示，服务器头节点（head node）中还有额外的 retimer。这里的主要客户是 AI 加速器厂商和服务器 ODM。

![](https://substack-post-media.s3.amazonaws.com/public/images/136f3a6d-f265-44e6-951c-e9c40aebd240_1630x1240.png)
*Astera Labs*

retimer 在加速计算系统中如此流行的原因是[信号反射（Signal Reflection）](https://resources.pcb.cadence.com/blog/2022-signal-reflection-and-distortion-in-pcbs)。除了距离之外，这是 PCB 走线或线缆中信号损耗的第二大原因。简单来说，GPU 系统密度极高：上图展示了基板（例如 NVIDIA HGX）如何容纳 8 张 GPU。这样的密度会诱发信号问题，因而需要 PCIe retimer。AI 服务器可以在加速器基板和所连接的服务器头节点两侧都配备 retimer。每 GPU 的确切用量随 PCB 与设计布局等多种因素而异，我们将在报告后文的订阅部分分享我们的估算。不同超大规模云厂商的设计所含 retimer 数量各不相同。

Astera Labs 的第一个大客户其实是亚马逊，用于「常规」（非 AI）云工作负载。在某些场景下，对于较高的数据速率，Aries retimer 能帮助云服务商实现比替代方案更低的 TCO。下图展示了 retimer 在 IT 设备中的位置。

![](https://substack-post-media.s3.amazonaws.com/public/images/c2580389-7924-4cdb-9f91-f6c8021cc719_1006x763.jpeg)
*ServeTheHome*

Aries 的另一个新兴驱动力是 CXL——一种构建在 PCIe 之上的协议。正如我们在[深度解析](https://www.semianalysis.com/p/cxl-deep-dive-future-of-composable)中所解释的，CXL 在内存池化（Memory Pooling）上的普及将带来越来越多的 CXL 交换机需求，进而需要 retimer。当然，我们对这个话题并不那么乐观。

讲完基础之后，本报告的主体将探讨 Astera Labs 护城河的牢固程度，并深入其他主要产品线。我们将覆盖增长、ASP、竞争、毛利率等。我们还将分享到 2027 年的预测，从营收一直到自由现金流。我们考虑了 Astera 在各平台、各超大规模云厂商处不同的渗透率，为每个超大规模云厂商的每条产品线建模出货量。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
