---
title: "先进封装第三部 – Intel 对热压键合的奇特豪赌，以及 ASM Pacific、Kulicke and Soffa 与 Besi 的 TCB 设备格局"
title_en: "Advanced Packaging Part 3 – Intel’s Curious Bet on Thermocompression Bonding, ASM Pacific, Kulicke and Soffa, and Besi TCB Tool Landscape"
date: 2022-01-19
source: https://newsletter.semianalysis.com/p/advanced-packaging-part-3-intels
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 先进封装第三部 – Intel 对热压键合的奇特豪赌，以及 ASM Pacific、Kulicke and Soffa 与 Besi 的 TCB 设备格局

> 原文：[Advanced Packaging Part 3 – Intel’s Curious Bet on Thermocompression Bonding, ASM Pacific, Kulicke and Soffa, and Besi TCB Tool Landscape](https://newsletter.semianalysis.com/p/advanced-packaging-part-3-intels) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

在本系列的[第一部](https://semianalysis.substack.com/p/advanced-packaging-part-1-pad-limited)中，我们讨论了先进封装的必要性并做了基础概述。在[第二部](https://semianalysis.substack.com/p/advanced-packaging-part-2-review)中，我们讨论了市面上的主要封装类型，重点放在逻辑芯片方案上，同时也深入探讨了存储和图像传感器。在第三部中，我们将讨论热压键合（thermocompression bonding，TCB）以及这一领域的三大设备玩家：ASM Pacific、Kulicke and Soffa 和 Besi。热压键合是标准倒装芯片（flip chip）工艺的进化形态，但利弊兼备，我们将在本文中一一展开。

热压键合（TCB）用于当前所有形态的 HBM 存储上。Intel 的大多数封装技术也使用 TCB。Intel 对这项技术下了一记非常奇特的赌注，把它当作自身封装需求的驱动力，而 TSMC 则完全没有跟进。我们将讨论这项技术以及 Intel 在其发展中的独特角色——正是这一点让他们得以成为先进封装的领导者，但我们也会讨论它的一些缺点。Intel 看起来还将继续在 TCB 设备上砸钱，亚利桑那、新墨西哥的扩产以及马来西亚新建的 $7B 封装厂，都有数亿美元规模的订单纷至沓来。我们将先解释这项技术，再讲 Intel 在其发展中的核心角色，最后讲设备生态。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/93f0f183-e22d-4c85-94db-032f836df3fa_1024x409.png)

要理解 TCB 的优势，必须先谈倒装芯片封装的缺点。如第二部所述，标准倒装芯片工艺从沉积助焊剂（flux）或非导电膏（NCP）开始。随后由裸片贴装设备将芯片精确放置到封装基板、中介层或载板上。这一步是批量工艺，许多封装可以同时完成裸片贴装。贴装好的一整批裸片随后进入回流焊炉或连续回流链式炉，这同样是批量工艺。数十、数百乃至数千个封装被送入炉中，加热到熔化焊料以最终完成键合的温度，然后流入后续工序，比如助焊剂残留清洗和底部填充（underfill）。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/56120e50-6878-4030-8ca2-cc1fc2f05318_1023x817.png)

这个工艺速度极快，但也带来一些重大缺陷。最大的问题与热膨胀系数（CTE）有关。整个封装由许多不同材料构成，在回流焊炉中加热会使这些材料以不同速率膨胀。这个类比不算最贴切，但请容我们这么讲：如果你烤过派，就知道派皮和派的内馅膨胀速率不同。如果不小心控制好几个因素，内馅最终会顶破最上层的派皮沸溢出来，把派皮泡得软塌塌的。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

随着芯片和基板膨胀又冷却，CTE 的差异会导致翘曲（warpage）。此外，由于裸片先贴装、后焊接，焊球未必与每一个铜焊盘都完美接触，从而造成芯片间隙（chip gap）偏差。最后，裸片的贴装也未必完全水平。这些小问题会随时间累积，导致早期失效或更差的电气性能。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/fc0883c5-5ba7-45ae-b17b-083c01522deb_1024x805.png)

业界只需看看许多最早期的无源中介层技术。AMD 基于 Fiji 的 GPU 失效率相当高，因为当时的工艺做不出完美的键合，热循环累积之下最终产品罢工。随着 TSMC 和 ASE/SPIL 逐渐学会如何做基于中介层的封装，这些可靠性问题已随时间改善，但并未彻底解决。在温度不稳定、封装频繁在高低温之间循环的环境中，这些问题仍然相对常见。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/e02a8ef0-e2d7-4381-b678-ecfbaed14b7a_1024x759.png)

于是热压键合登场。它不再把裸片贴装好、再把整批组件送进回流焊炉，而是由单一设备逐颗放置裸片、施加压力，并加热使焊球回流。TCB 解决了标准倒装芯片的几大痛点。热量从芯片顶部施加，因此只有芯片和 C4 焊料连接处被加热。这就把基板翘曲问题压到了最低。施加的压力保证了键合均匀，没有间隙偏差或倾斜。最后，在施力的同时可以伴随高频振动，打碎铜焊盘和焊球表面金属的氧化层。所得的键合几乎没有任何空洞（void）和污染。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/cba2ad29-3390-474e-a9f8-ee0aa1b1ce27_1024x632.png)

在相同的 IO 间距（pitch）下，TCB 能实现更好的电气特性。TCB 允许 IO 间距向更小的尺寸微缩。TCB 还能封装更薄的裸片和封装体。最后这一点正是 HBM 采用 TCB 的原因，也是 Huawei 曾在手机芯片市场试验 TCB 的原因。看起来 TCB 相对标准倒装芯片工艺流程是一项全面占优的技术，但那忽略了一个重大因素。

成本。

一台先进的 TCB 设备每小时贴装约 500 到 1,000 颗裸片，售价约 $1.25M。而一台先进的倒装芯片裸片贴装设备每小时贴装 3,000 到 10,000 颗裸片，售价约 450k。这些数字因精度与产能的取舍以及设备附带的各种功能而差异很大，但显然标准倒装芯片的产能高得多。回流焊炉或链式炉非常便宜，而且能消化多台裸片贴装设备的产出，所以那部分成本不值得操心。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

这件事的奇特之处在于：Intel 拥有近 300 台 TCB 设备，而马来西亚封装厂将让这一数量再翻一倍。300 台设备远远超出了 Intel 先进封装的用量。Intel 在许多非先进封装的应用中也使用 TCB，尽管标准倒装芯片工艺完全够用。SemiAnalysis 与一位 Intel 封装工程师进行了不具名的交流，其中的逻辑相当有意思。鉴于 Intel 在高功率、高利润率应用中份额很重，良率损失和可靠性隐患，远远超过设备折摊到每颗封装上的那点微不足道的成本。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/cdda7718-da87-4cb4-8492-78be03844380_1024x761.png)

此外，这些设备在封装类型上带来了极大的灵活性。Intel 可以用同一台设备做标准封装、2.5D 封装和先进 3D 封装。上图来自 [der8auer](https://www.youtube.com/watch?v=BQYsR0Upr1E)，展示的是一颗带有多种间距尺寸的 Intel Sapphire Rapids 服务器 CPU。其中有一段是 EMIB 的 55 微米间距，其余裸片到封装的连接则为 100 微米间距。理论上不用 TCB 也能做到，但由于焊盘尺寸和焊料帽（solder cap）尺寸不同，现实中的实现要容易得多。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/dbbca5d3-f84c-41ee-bd88-ccfde5eda760_817x241.png)

当 Intel 转向 Foveros Omni 时，TCB 的能力才真正开始大放异彩。我们在[第二部](https://semianalysis.substack.com/p/advanced-packaging-part-2-review)中更详细地讨论过该技术，铜柱（copper pillar）和 ODI 裸片让 Foveros Omni 几乎不可能用标准倒装芯片工艺来封装。第一款 Foveros Omni 产品将是 Intel 的 Meteor Lake——一个面向大众市场的客户端架构，覆盖从 5W 的 SoC 一直到高功耗台式机。（编者注：后来这一角色被重新划定为 Arrow Lake。）尽管包含多颗裸片，Omni 却能在制造成本上实现大幅节约：为每块 IP 选择最优制程节点，并最小化裸片面积以提升良率。该封装具有多种凸点间距：130 微米、100 微米和 36 微米。先进 3D 逻辑封装并不只属于高性能应用。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/5cf0dce2-1ef4-43dd-9283-222fc86337a3_970x509.png)
*Meteor Lake 测试封装*

TSMC、Samsung 以及其他许多厂商，除非在 TCB 上重金投入，否则做不了这种封装。Intel 联合开发 TCB 设备已超过十年，竞争对手很难瞬间转向这项技术。TSMC 的 InFO 采用标准倒装芯片流程，但由于基板更贵，它反而可能是成本更高的封装技术。TSMC 至今只在标准化的大宗 ABF 基板上做先进封装，这制约了他们能把先进封装的成本打到多低。与此同时，InFO 也确有一些重大优势，我们在[第二部](https://semianalysis.substack.com/p/advanced-packaging-part-2-review)讨论过，主要是在不使用硅裸片的情况下于再布线层（RDL）内实现复杂布线。TSMC 确实在 HBM 上使用 TCB，但那与逻辑堆叠是完全不同的细分场景。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

混合键合（hybrid bonding）的能力超出倒装芯片和 TCB 所能提供的一切，但那项技术运行在成本与性能曲线上完全不同的位置点，这削弱了它在中期内上量的能力。这将在第四部中讨论。Intel 对 TCB 的拥抱，让他们能够围绕各种 IP 创造选择权，把许多不同的模块放到许多不同节点上流片，而在裸片间互连上不受大的惩罚。关于设计端这一策略的具体细节，请参阅这篇关于 [Intel 与 TSMC 晶圆供应协议的文章](https://semianalysis.substack.com/p/tsmc-wants-to-make-intel-dependent)。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a7080a7a-82fc-436b-acbd-b5eb34238048_846x1024.png)

TCB 也已被 HBM 应用所采纳。HBM 裸片必须极薄。上图只是 4 层堆叠的存储，但随着行业迈向 8 层及以上，Samsung、SK Hynix 和 Micron 使用 TCB 已成必然。在 SK Hynix 即将推出的 12 层堆叠 HBM3 中，裸片薄度的要求已变得如此极端，[每颗裸片要减薄到 30 微米](https://news.skhynix.com/sk-hynix-announces-development-of-hbm3-dram/)。凸点间距同样密得惊人。目前实现 HBM 堆叠的唯一途径就是 TCB 技术，但业界也期待未来采用更奇异的封装形态，比如混合键合。

由于是封装极薄裸片的最佳技术，TCB 也曾被手机应用试验过，旗舰机型上由 OSAT 和 IDM 封装的出货产品都用过。Samsung、Qualcomm/Amkor 以及 Huawei/ASE 都曾在与堆叠封装（PoP）DRAM 相关的一些应用中使用 TCB。OSAT 们正开始订购越来越多的 TCB 设备，但最大的订单仍来自 Intel 及其定制联合开发的 TCB 平台。关于这些其他用例，需要注意的重点是：它们用的设备与 Intel 的并不相同，而且并非为高功率或高性能应用设计。

ASM Pacific、Kulicke and Soffa 与 Besi 三家在 TCB 上的市场竞争相当有活力，各家在不同领域各有绝活，也因此各占一方细分市场。订单量在大幅攀升，但由于三家各自所处的细分市场不同，增幅并不一致。

这些内容我们将在订户专享章节中讨论。

[分享](https://newsletter.semianalysis.com/p/advanced-packaging-part-3-intels?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[立即订阅](https://newsletter.semianalysis.com/subscribe?)
