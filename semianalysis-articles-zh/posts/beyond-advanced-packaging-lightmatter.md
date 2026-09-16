---
title: "超越先进封装：Lightmatter Passage 小芯片共封装于光学中介层"
title_en: "Beyond Advanced Packaging: Lightmatter Passage Chiplets Co-Packaged On Optical Interposer"
subtitle: "但会有产品大规模采用它吗？"
date: 2022-08-22
source: https://newsletter.semianalysis.com/p/beyond-advanced-packaging-lightmatter
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 超越先进封装：Lightmatter Passage 小芯片共封装于光学中介层

> 原文：[Beyond Advanced Packaging: Lightmatter Passage Chiplets Co-Packaged On Optical Interposer](https://newsletter.semianalysis.com/p/beyond-advanced-packaging-lightmatter) · SemiAnalysis

**但会有产品大规模采用它吗？**

几年前，Lightmatter 凭一款重新思考电子计算与数据搬运范式的 AI 加速器 Mars 一鸣惊人。他们展示了一颗用光子学做计算的处理器，这颗芯片承诺在延迟、带宽和功耗上带来多个数量级的改善。但最终它没能成功，问题出在这颗芯片在软件与计算结构上的僵硬。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8f059703-dabd-4a9a-9824-431ba42d3197_5292x1464.png)

Lightmatter 已推出该 AI 计算产品的第二代 Envise，但那不是今天文章的重点。我们想分享的是 Lightmatter 关于其最新产品 Passage 的介绍。这几天我们人在 SPIE Optics and Photonics 现场并同时线上参加 HotChips——如果你也在 SPIE Optics and Photonics 或本周在圣地亚哥，请[联系我们](https://semianalysis.com/contact/)，很乐意见面聊聊。

概括地说，Lightmatter 想用 Passage 打破[先进封装与 IO 的约束](https://semianalysis.substack.com/p/advanced-packaging-part-1-pad-limited)。

AI 与 HPC 等领域的问题规模呈指数级增长，而摩尔定律跟不上。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/7b0dba07-021b-4537-b869-0d305eb9bbb9_1518x837.jpeg)

于是行业转向小芯片（chiplet），用更大的封装拼装出更强算力。把芯片拆成多颗小芯片、突破[光罩极限（光刻工具图形化能力的物理上限）](https://semianalysis.substack.com/p/die-size-and-reticle-conundrum-cost)可以继续微缩，但这一范式仍有问题：即便有[先进封装，把数据搬出芯片的功耗代价也会成为限制因素](https://semianalysis.substack.com/p/advanced-packaging-part-1-pad-limited)；而且即便采用最先进的封装形式，带宽依然受限。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ba2dc917-bb89-41bb-a58a-139a82cf0a84_1535x812.jpeg)

Lightmatter 不想在硅上再堆硅，而是要用 Passage 把先进封装的游戏彻底翻转。Passage 在一枚光学中介层（optical interposer）上连接 48 颗客户芯片。Passage 基于[格芯（GlobalFoundries）Fotonix 45CLO 工艺技术](https://semianalysis.substack.com/p/globalfoundries-fotonix-the-leading)打造，设计用于以极高的带宽和性能连接众多芯片。这枚光学中介层打破了带宽限制：每个瓦片（tile）之间可提供 768 Terabits per second，并支持以 128 Terabits per second 扩展到多个中介层。这是传统封装无法企及的能力与规模。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ff5139a6-ab92-4e22-adc6-352af3b9e499_1537x837.jpeg)

几十年来，光学历来被寄望于解决电 IO 的瓶颈，技术也在缓慢推进。Lightmatter 所说的 Gen 1——可插拔光模块——多年来一直用于连接数据中心内的交换机。把光学放到同一封装内或直接相连的 Gen 2 与 Gen 3 光学，正开始进入[网络交换机](https://semianalysis.substack.com/p/how-intel-was-designed-into-the-majority)和计算领域，推手是[英特尔（Intel）](https://semianalysis.substack.com/p/intels-trojan-horse-into-the-foundry)和 [Ayar Labs](https://semianalysis.substack.com/p/ayar-labs-co-packaged-optics-revolution?s=w) 等公司。Lightmatter 想凭借 Passage 直接跳到 Gen 4 和 Gen 5。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c91688a0-3fc0-4099-8579-6e179e3bcac8_3058x1628.jpeg)

英特尔和 Ayar Labs 所瞄准的标准共封装光学，其规模比 Lightmatter 采用的光学中介层方案低一个数量级。Lightmatter 的互连密度高出 40 倍，因为单颗芯片只能插入约 200 根光纤。此外，标准方案的互连完全静态，而 Passage 拥有动态可重构的 fabric。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/5eaa4a69-d215-49fc-a1d2-31be3d5fffc8_2904x658.jpeg)

这枚光学中介层可以在芯片之间执行交换与路由。整张互连网络可在 1ms 以内完成重构。Lightmatter 表示他们支持所有拓扑，比如 all-to-all、一维环、Torus、Spine-leaf 等。在 48 颗芯片的阵列上，Passage 的交换与路由在任意两颗芯片之间的最大延迟为 2ns。

交换的实现方式是用环形谐振器（ring resonator）调制不同颜色（波长）的光，再用马赫-曾德尔干涉仪（Mach-Zehnder interferometer）引导它们。

Lightmatter 的[光子晶圆级中介层](https://semianalysis.substack.com/p/cerebras-wafer-scale-hardware-crushes)已有 A0 版硅片，并声称每个站点（site）功耗低于 50 瓦。每个站点有 8 台混合激光器驱动 32 个通道，每个通道运行 32Gbps NRZ。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1eae21c0-54b4-4d16-b2bb-4057bef9eb3b_3019x1611.jpeg)

Lightmatter 的[晶圆级](https://semianalysis.substack.com/p/cerebras-wafer-scale-hardware-crushes)硅光子芯片主要采用基于硅的制造技术，因此也继承了诸多同样的约束，也就是[光刻工具的光罩极限](https://semianalysis.substack.com/p/die-size-and-reticle-conundrum-cost)。格芯和 Lightmatter 通过波导拼接（stitching）绕开了这一问题。纳米光子波导的光罩间连接每次跨光罩仅 0.004 dB 损耗。波导本身的损耗为 0.5 dB/cm，每个马赫-曾德尔干涉仪损耗 0.08 dB，每次交叉还有 0.028 dB 损耗。

Lightmatter 表示，借助 UCIe，小芯片到中介层的互连可以跑到 32Gbps 的最高规格。如果使用直接 SERDES，他们认为可以跑到 112G。客户 ASIC 以 3D 封装方式叠放在中介层之上，最终产品再由 OSAT 组装。它可以有众多变体：从 48 颗芯片到少至 8 颗芯片的更小中介层。Passage 封装还必须向叠放在上面的芯片供电，方式是通过 TSV 为每个瓦片输送最高 700W。在这一功耗水平下水冷必不可少，但如果客户 ASIC 功耗较低，风冷也能应付。

值得注意，标称的 768Tbps 看起来大部分被浪费了。其功能似乎只允许一个输入耦合到一个输出，这就让互连的很大一部分处于空闲。要利用起这些容量，需要由它们自己找出互不冲突的路径。这些路径是无源的，不用时几乎不耗电。MZI 元件要么向左、要么向右，没有混合，没有多播，一进一出。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/441a5861-a5d1-4158-a486-2b0612960149_1455x673.png)

Lightmatter 还给出了解耦内存设计与多租户架构的例子。他们表示该中介层[可以支持任何协议，包括 CXL](https://semianalysis.substack.com/p/cxl-deep-dive-future-of-composable)。通过重构网络，中介层上的客户 ASIC 之间可以实现「空气隔离」（air-gapped），使特定芯片之间无法传递数据。最大的问题在于产品会不会来、何时来。这可能只是 vaporware（空头产品），也可能成为高端先进制程解耦服务器设计的未来。Lightmatter 必须说服其他公司为这一平台构建芯片，而这些公司必须把[昂贵的开发投入](https://semianalysis.substack.com/p/the-dark-side-of-the-semiconductor)托付给一个未经证实的伙伴。

如果你喜欢我们的内容，请分享！帮忙传出去！

[分享](https://newsletter.semianalysis.com/p/beyond-advanced-packaging-lightmatter?utm_source=substack&utm_medium=email&utm_content=share&action=share)
