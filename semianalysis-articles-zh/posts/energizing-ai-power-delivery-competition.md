---
title: "为 AI 注入动力：电源供电竞争白热化——Vicor、MPS、Delta、ADI、Renesas、英飞凌"
title_en: "Energizing AI: Power Delivery Competition Heats Up Vicor, MPS, Delta, ADI, Renesas, Infineon "
subtitle: "NVIDIA H100、Google TPUv5、AMD MI300、Intel Gaudi3/PVC、Cerebras WSE2"
date: 2023-08-01
source: https://newsletter.semianalysis.com/p/energizing-ai-power-delivery-competition
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie", "Gerald Wong", "George Cozma"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 为 AI 注入动力：电源供电竞争白热化——Vicor、MPS、Delta、ADI、Renesas、英飞凌

> 原文：[Energizing AI: Power Delivery Competition Heats Up Vicor, MPS, Delta, ADI, Renesas, Infineon](https://newsletter.semianalysis.com/p/energizing-ai-power-delivery-competition) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**NVIDIA H100、Google TPUv5、AMD MI300、Intel Gaudi3/PVC、Cerebras WSE2**

AI 加速器的功耗正变得越来越高。NVIDIA H100 的热设计功耗（TDP）为 700 瓦（W），而全球装机量最大的数据中心 CPU——Intel Skylake/Cascade Lake——的 TDP 还不到 200W。下一代芯片将需要更多功率来支撑更高的计算密度。在机柜层面，这将要求 >200 kW 的供电能力，而目前传统 CPU 服务器机柜只能提供 15-20kW。

功耗越高，随之而来需要解决的挑战也越多。尤其是，更高的功率会带来不成比例地更大的传输和转换损耗：也就是被浪费掉的功率。电费是数据中心最大的开支之一，因此降低功率损耗对改善总拥有成本（TCO）至关重要。因此，我们正看到从机柜级一直到芯片级的供电网络被重新架构，以在 AI 训练和推理这类高功耗计算负载中解决这一问题。

先进供电架构的首要目标是提升效率。今天我们将深入探讨这个话题的技术与竞争格局。电源公司 Vicor 历来是这一趋势中受益最大的公司之一。过去十年间，Vicor 从一家通用电源器件供应商，成长为进入先进数据中心电源应用领域的玩家，在多家超大规模云厂商的数据中心机柜级电源方案以及 NVIDIA、Google、AMD、Cerebras、Tesla 和 Intel 的 AI 加速器上拿下了设计导入（design win）。

然而，鉴于电源市场的风云变幻，Vicor 的命运最近急转直下。正如[我们在一年多前独家发现并披露的](https://www.semianalysis.com/p/short-report-nvidia-supplier-cut)，Monolithic Power Systems 在 NVIDIA 的 H100 GPU 中取代了 Vicor。此外，Vicor 的第二大客户与它的关系也颇为波折。而且，超大规模数据中心机柜电源方案正在发生诸多变化，包括多个新竞争者入局（MPS、Delta、Renesas、英飞凌、ADI）。

围绕 Vicor 的叙事起伏剧烈，其未来角色已成为多空战场。最近的新闻流、Vicor 对竞争对手的诉讼、超大规模云厂商的部署情况，以及管理层的惊人言论，都为论战双方提供了弹药。

今天我们将梳理供电技术入门、Vicor 的技术领先性、我们对 Vicor 标志性的分解式电源架构（Factorized Power Architecture）与垂直供电（Vertical Power Delivery）技术的评估、关键设计导入（包括 Vicor 是否进入 H100 或 TPUv5 的细节）、Vicor 在汽车行业的潜力及其长期影响。我们还将分享对其 5 大竞争对手——MPS、Delta、Renesas、英飞凌和 ADI——以及当前正在爆发的法律战的观点。

## **芯片供电入门**

电网以高达数十万伏的交流（AC）电压生成和传输电力。而计算与存储芯片需要的是电压低得多、以直流（DC）形式存在的稳定而干净的电力。电压过高会过载并损坏芯片脆弱的电路；电压过低，芯片电路则无法正常开关。变压器、电源单元（PSU）以及最终的电压调节模块（VRM）的职责，就是向芯片输送正确类型的电力。随着功率需求不断增加，高效供电也变得更具挑战性。

![](https://substack-post-media.s3.amazonaws.com/public/images/34bda3cd-c0b0-4e1e-9777-fe1e98c0df15_3082x892.png)

在 GPU 或 CPU 这类电路中，有 4 个主要量：功率、电流、电压和电阻。功率（P）衡量的是单位时间内消耗的能量，通常以瓦特（W）为单位。电流衡量的是被移动的电子数量，换句话说，就是电子的流动速率。电流（I 或 A）通常以安培（A）为增量单位表示。电压（V）是两点之间的电势差。你可以把电压理解为推动电子穿过回路的压力。

电压通常以伏特（V）为单位。最后是电阻（R），通常以欧姆（Ω）为单位，表示电流流过该材料的难度。要运用这些量，我们需要欧姆定律，这里重点关注欧姆定律的两种形式。第一种是 P = I*V，即功率等于电流乘以电压。第二种是 P = R*I2，即功率也等于电阻乘以电流的平方。

硅芯片以约 1V 直流或更低的电压运行。为了追求能效，设计正在转向更低的时钟频率和更低的工作电压，以在性能/功率曲线上更高效的区段运行。

然而，以低电压、大电流传输电力会因供电线路电阻产生巨大的功率损耗（I^2R）。最小化功率损耗的关键是以更高的电压和更低的电流传输电力，然后在尽可能靠近有源硅电路的地方降压。

## **电压调节模块（VRM）由什么组成？**

VRM 是一组重要部件，它接收系统 PSU 的输入电压，然后将其转换为正确的电压为 SoC 供电。通常，VRM 位于承载芯片的 PCB 上，不过在少数情况下，这些器件可能放在封装本身上，甚至集成在硅片内。现代 VRM 有 3 个主要部分：电容、电感和功率级（power stage）。电容储存电能，然后以恒定速率释放，从而平滑输送到处理器的电力。电感则用于阻碍电流变化，防止巨大的电流尖峰毁掉处理器。

![](https://substack-post-media.s3.amazonaws.com/public/images/33694782-198d-46c6-8e45-22c05aa31978_2928x1431.png)
*简化版 VRM*

最后，也可以说是 VRM 最重要的部分是功率级，它接收来自 PSU 的输入电压（比如 12 伏），并将其转换为处理器所需的电压。在 CPU 上，所需电压传统上为 1.2 至 1.8 伏；而在 GPU 或大型 FPGA、ASIC、AI 加速器上，该电压在 0.8 至 1.0 伏之间。

## **功率更高，效率更低**

随着未来架构和制程技术的发展，SoC 的供电电压不断下降，要维持相同的功率，电流必须以与电压下降相同的倍数增加。举例来说，取一颗 240W、工作电压 1.2 伏的 AMD Genoa CPU。从 12 伏输入降到芯片的 1.2 伏（降压 10 倍），意味着电流需要从 12 伏下的 20 安培增加到 1.2 伏下的 200 安培（增加 10 倍），才能维持相同的功率水平。

再对比一颗工作在 0.8V 的 700 瓦 GPU。如果将 12 伏输入降到芯片的 0.8 伏（降压 15 倍），意味着电流需要从 12 伏下的 60 安培增加到 0.8 伏下的 875 安培（增加 15 倍）。**与功耗较低的 CPU 相比，GPU 的电流要高得多。电流更高意味着电阻损耗更大**，这从 P = R*I2 公式可知（损耗等于电阻乘以电流的平方）。

当电压降到 0.8V 时，电阻问题急剧恶化：电流增加 15 倍，**导致电阻损耗呈指数级放大至 225 倍**。这说明了效率损耗已成为最近几代数据中心芯片的一大问题。随着制程微缩使电压继续下降、[先进封装](https://www.semianalysis.com/p/advanced-packaging-part-1-pad-limited)使封装变得更大、更耗电，情况只会更糟。

[分享](https://newsletter.semianalysis.com/p/energizing-ai-power-delivery-competition?utm_source=substack&utm_medium=email&utm_content=share&action=share)

## **48 伏的崛起**

为了解决这一问题，业界开始采用更高的输入电压。长期以来，12V 直流（DC）一直是电子设备 PSU 输出的标准电压。12V 诞生之初绰绰有余，因为当时功率足够低，由此产生的效率损耗微不足道。而如今行业开始要求更高功率，同时 SoC 电压却更低，对效率构成双重打击。这些效率损耗已经超过了 12V 器件相对便宜且无处不在所带来的好处。

**从 12V 升到 48V，意味着所需电流降至 1/4，损耗将降低 16（4^2）倍。**这就是许多公司转向 48V 供电网络的原因。但如果最终反正要降到 1V，那意义何在？

你可以在离 SoC 近得多的地方把 48V 降到 SoC 电压，**因此走线长度更短。走线越长，电阻损耗越大。**所以，只在尽可能靠近负载点的地方对 48V 输入降压，带来的结果是更低的整体电阻损耗。

![](https://substack-post-media.s3.amazonaws.com/public/images/b291ece1-d130-48b0-bc5a-6f9143f7cd2b_3427x1905.png)

Google 是第一个在数据中心采用 48V 供电的超大规模云厂商（约 2016 年），并推动 48V 在 OpenCompute 联盟中标准化。

## **Vicor 的崛起**

作为回应，芯片公司和 OEM 厂商开始在板卡上布置 48V 输入的 VRM。主要受益者就是 Vicor。虽然电信设备已有一套成熟的 48V 生态，但那是负电压，而数据中心需要正电压。Vicor 是为计算用例提供 48V VRM 的主要玩家。

为实现这一转变，电源单元会将机柜接收的 380V 交流电转换为 48V 直流。数据中心在机柜层面提供 48V 电力，这给了服务器板卡也采用 48V 输入的理由，以便接收这个 48V 输入电压并进行降压。或者，为了让传统的 12V 板卡继续工作，需要一个中间器件把 48V 降到 12V。基本上，要么需要 48V 输出电压，要么需要 48V 输入电压，而 Vicor 正是最早把这些产品推向市场的厂商。

![](https://substack-post-media.s3.amazonaws.com/public/images/8f07ef00-694b-482d-8e44-a8126234a2f5_2677x1434.png)
*Vicor 的 48V 生态*

Vicor 第一个主流商用硅器件设计导入是 2018 年 NVIDIA 的 V100 SXM3 刷新版，其 48V VRM 采用了 Vicor 的器件。随后是 A100，整个产品线的 VRM 都使用了 Vicor 的器件。Google 也在与 V100 大致相同的时期为 TPU 采用了 Vicor。这巩固了 Vicor 在 48V 领域的主导地位，也确立了 Vicor 是高性能供电的未来之路。

此后，叙事被打破：[Vicor 在 H100 中被剔除，由 Monolithic Power Systems（MPS）取而代之](https://www.semianalysis.com/p/short-report-nvidia-supplier-cut)——这一消息由 SemiAnalysis 率先独家报道。这份独家报告发布后的次日早晨，Vicor 股价下跌超过 20%，并在接下来一年里又跌了 30%，原因正是 NVIDIA 对 Vicor 营收的巨大贡献。直到今天，Vicor 仍未在[正在大规模爬坡的 NVIDIA H100](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and) 中实现批量出货。

上周，Vicor 任职 30 多年的 CEO 声称将重新被设计导入某客户的基础平台，同时对其竞争对手提起诉讼，引发了一场剧烈的轧空。需要指出的是，这位 CEO 一年多以前也对卖方分析师说过会重新拿到设计导入，但订单至今没有落地。官方细节相当匮乏，让我们来拆解一下 NVIDIA 和其他客户身上究竟发生了什么。

今天我们将梳理 Vicor 的技术领先性、我们对 Vicor 标志性的分解式电源架构与垂直供电技术的评估、关键设计导入（包括 Vicor 是否进入 H100 或 TPUv5 的细节）、Vicor 在汽车领域的机会及其长期前景的影响。我们还将分享对其 5 大竞争对手——MPS、Delta、Renesas、英飞凌和 ADI——以及当前正在爆发的法律战的观点。

[团购订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
