---
title: "AI 扩张——CoWoS 与 HBM 供应链分析"
title_en: "AI Expansion - Supply Chain Analysis For CoWoS And HBM"
subtitle: "生成式 AI 扭矩下的 28 家上游供应商分析"
date: 2023-07-26
source: https://newsletter.semianalysis.com/p/ai-expansion-supply-chain-analysis
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie", "Gerald Wong"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# AI 扩张——CoWoS 与 HBM 供应链分析

> 原文：[AI Expansion - Supply Chain Analysis For CoWoS And HBM](https://newsletter.semianalysis.com/p/ai-expansion-supply-chain-analysis) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**生成式 AI 扭矩下的 28 家上游供应商分析**

AI 正在蓬勃发展。人人都想要更多 AI 加速器，而主要的限制因素是[将 5nm ASIC 与 HBM 封装在一起的 CoWoS 先进封装](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and)。这种产能不足正在[造成 GPU 缺货，且将持续到明年第二季度](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and)。在[上一篇报告](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and)中，我们讨论了[Nvidia、Broadcom、AMD、Marvell、Amazon/Alchip 等大客户要求台积电（TSMC）增加多少 CoWoS 产能](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and)。我们还解释了终端市场用例、CoWoS 产能的分配以及 CoWoS 的需求面。

今天我们讨论供给侧。台积电正向设备制造商紧急下单，以[充实其位于竹南的新先进封装厂](https://pr.tsmc.com/english/news/3033)。三星（Samsung）、Intel、Amkor、JCET 和 ASE 也在扩充[某些自有竞争技术](https://www.semianalysis.com/p/advanced-packaging-part-2-review)，以求分一杯生成式 AI 的羹。随着部分通用数据中心开支（如内存和 CPU）被生成式 AI 开支挤占，理解哪些环节仍在增长对理解供应链至关重要。在本文中，我们将详细介绍 CoWoS 的制造工艺流程，以及 CoWoS 与 HBM 生产所需的 28 家不同上游企业。

我们将分享这 28 家上游厂商中哪些从这一趋势中拿到了相对较大的订单。我们还将分享其中哪些供应商虽然其设备是工艺流程的一部分、却并未获得相对较大的订单。我们的部分报道与市场错误认知相悖。我们还将揭示 HBM3 和 HBM4 工艺流程中的一些创新，以及一家因此被完全挤出工艺流程的公司。最后，我们想分享 Nvidia 明年争取更多产能的最新进展。一如既往，**技术背景将免费分享，而与当前产能建设和供应商相关的结论与细节将只与订阅者分享。**

回顾一下，CoWoS 是台积电的一种「2.5D」封装技术，将多颗有源硅裸片（通常配置为逻辑芯片与 HBM 堆叠）集成在一块无源硅中介层上。中介层充当其上有源裸片的通信层。随后中介层与有源硅被安装到一块包含 I/O 的封装基板上，以便放置到系统 PCB 上。[CoWoS 是 GPU 和 AI 加速器中最流行的封装技术，因为它是将 HBM 与逻辑芯片共封装、为训练和推理负载获取最大性能的主要手段。](https://www.semianalysis.com/i/133273576/the-real-bottleneck-cowos)

![](https://substack-post-media.s3.amazonaws.com/public/images/7dae3ae3-f074-40e5-8241-2a8f42ade96c_1293x488.png)

下面我们将详细介绍 CoWoS-S（主要变体）的关键制造步骤。

## 硅中介层关键工艺步骤

第一部分是制造硅中介层，它包含连接芯片的「导线」。硅中介层的制造与传统前段晶圆制造类似。人们常说硅中介层是用 65nm 制程工艺制造的，但这并不准确。CoWoS 中介层中没有晶体管，只有金属层，硬要说的话其金属层间距有点类似，但其实并不相同。

这就是为什么 2.5D 封装通常由先进制程代工厂在内部完成——它们既能生产硅中介层，又能直接获得先进制程硅片。虽然 ASE 和 Amkor 等其他 OSAT 也做过类似 CoWoS 的先进封装或 FOEB 等替代方案，但它们必须从联电（UMC）这类代工厂采购硅中介层/桥接。

硅中介层的制造从空白硅晶圆开始，先制作硅通孔（TSV）。这些 TSV 贯穿晶圆，提供垂直电气连接，使中介层顶部的有源硅（逻辑与 HBM）裸片能与封装底部的 PCB 基板通信。芯片正是通过这些 TSV 向外界发送 I/O，也通过它们接收电力。

制作 TSV 时，先在晶圆上涂覆光刻胶，再用光刻技术进行图形化。然后使用深反应离子刻蚀（DRIE）在硅中刻蚀出 TSV，以实现高深宽比刻蚀。接着用化学气相沉积（CVD）沉积绝缘层（SiOX、SiNx）和阻挡层（Ti 或 TA）。再用物理气相沉积（PVD）沉积铜种子层。然后用电化学沉积（ECD）以铜填充沟槽，形成 TSV。这些通孔并不贯穿整片晶圆。

![](https://substack-post-media.s3.amazonaws.com/public/images/6ecb110f-3f9d-444d-8b98-233a6c499122_1935x1341.png)

TSV 制造完成后，在晶圆正面形成再布线层（RDL）。可以把 RDL 想象成多层导线，将各颗有源芯片连接在一起。每层 RDL 由更小的通孔和实际的 RDL 组成。

通过 PECVD 沉积二氧化硅（SiO2），然后涂覆光刻胶并用光刻对 RDL 进行图形化，再用反应离子刻蚀去除 RDL 通孔处的二氧化硅。该过程重复多次，在其上形成更大的 RDL 层。

在典型配方中，先溅射钛和铜，再用电化学沉积（ECD）沉积铜。不过我们认为，台积电使用极低 k 介质（可能是 SiCOH）来降低电容，而不是 SiO2。然后用 CMP 去除晶圆上多余的电镀金属。这基本上是标准的双大马士革工艺。每增加一层 RDL 都重复这些步骤。

![](https://substack-post-media.s3.amazonaws.com/public/images/09d568cd-a1c9-48e8-8ad9-6e894d8236f6_1906x1363.png)

在最顶层 RDL 上，通过溅射铜形成凸点下金属（UBM）焊盘。涂覆光刻胶，经光刻曝光形成铜柱图形。电镀铜柱后再以焊料覆盖封端。剥离光刻胶，并刻蚀掉多余的 UBM 层。芯片正是通过 UBM 及其上的铜柱与硅中介层连接。

![](https://substack-post-media.s3.amazonaws.com/public/images/c24f98b1-8204-4dbd-9086-f1acde98ee44_2961x1861.png)

## 晶圆上芯片（Chip on Wafer）关键工艺步骤

现在，已知良好（known good）的逻辑与 HBM 裸片通过传统的倒装芯片批量回熔工艺贴装到中介层晶圆上。先在中介层上涂助焊剂，然后倒装焊机将裸片放置到中介层晶圆的焊盘上。贴装好全部裸片的晶圆随后在回焊炉中烘烤，使凸点焊料与焊盘之间的连接固化。多余的助焊剂残留物被清洗掉。

随后用树脂填充有源裸片与中介层之间的间隙，以保护微凸点免受机械应力。晶圆再次烘烤以固化底部填充胶。

![](https://substack-post-media.s3.amazonaws.com/public/images/b017275a-d65e-4252-aa3a-218368a17f8e_3604x1798.png)

接下来，用树脂对顶部裸片进行塑封，并用 CMP 平滑表面、去除多余树脂。塑封后的中介层随后被翻转，通过研磨和抛光减薄到约 100um 厚，以露出中介层背面的 TSV。

贴装在中介层晶圆顶部的顶部裸片与封装体即便在减薄后，也可能为晶圆提供足够的结构支撑与稳定性，因此并不总是需要载片晶圆来支撑。

## 晶圆上基板（Wafer on Substrate）关键工艺步骤

中介层背面进行电镀并形成 C4 焊料凸点，然后切割成单个封装。接着每颗中介层裸片再次以倒装芯片方式贴装到积层式封装基板上，完成封装。

在下图 Nvidia A100 的横截面中，我们可以看到 CoWoS 封装的各种组成部分。

![](https://substack-post-media.s3.amazonaws.com/public/images/5ddd4fb4-c3ef-4f50-b626-1b5ec1f58847_3376x2038.png)

顶部是带有 RDL 和铜柱微凸点的芯片裸片，它们与硅中介层正面的微凸点键合。接着是顶部带有 RDL 的硅中介层。可以看到 TSV 贯穿中介层，下方每个 C4 凸点对应 2 个 TSV。底部是封装基板。

注意，A100 只在中介层正面有单面 RDL。A100 的架构较简单，只有内存和 GPU，因此布线要求也较简单。而 [MI300 由内存、CPU 和 GPU 组成，全部位于 AID 之上，因此需要复杂得多的 CoWoS 布线，影响成本和良率](https://www.semianalysis.com/p/amd-mi300-taming-the-hype-ai-performance)。

对订阅者，我们将讨论参与这一工艺流程的 28 家厂商、其工艺步骤的强度，以及我们认为其中将大幅受益的一些公司。大多数公司不会受到巨大影响，但也有一些公司我们认为不会像当前大众市场所认为的那样受益。我们还将揭示 HBM3 与 HBM4 键合流程中的创新，以及一家因此被挤出去的公司。

[团购订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

## 设备与供应链
