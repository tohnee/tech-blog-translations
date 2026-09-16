---
title: "裸片面积与光罩难题——结合光刻机产能的成本模型"
title_en: "Die Size And Reticle Conundrum – Cost Model With Lithography Scanner Throughput"
subtitle: "更小的芯片未必更好"
date: 2022-06-19
source: https://newsletter.semianalysis.com/p/die-size-and-reticle-conundrum-cost
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 裸片面积与光罩难题——结合光刻机产能的成本模型

> 原文：[Die Size And Reticle Conundrum – Cost Model With Lithography Scanner Throughput](https://newsletter.semianalysis.com/p/die-size-and-reticle-conundrum-cost) · SemiAnalysis

**更小的芯片未必更好**

在我们的私人咨询业务中，我们花了大量时间，试图为各种逻辑和存储制程节点构建一个按设备类型划分的半导体晶圆厂资本开支模型。我们密切追踪的一个问题是：随着各代节点微缩，光刻支出如何演变。我们的起点是 28nm，一路经过第一代 FinFET 节点、第一批 EUV 节点，直到第一代环栅纳米片节点（3nm 和 2nm）。所考察节点的不同，光刻支出占比差异相当大。为了留档，下面是一张关于这个话题的 ASML 旧幻灯片。它似乎遗漏了很多各类晶圆厂资本开支项目，但仍有参考价值。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ebfb4f25-8874-4d64-8652-88b99d8050c3_1023x570.png)

光刻、沉积与刻蚀支出的相对演变，对 ASML、Lam Research、Applied Materials、Tokyo Electron 等公司的相对表现有很大影响。在研究过程中，最重要的单一因素是每个 DUV 或 EUV 层每次曝光的成本，以及曝光的层数。顺带一提，一些卖方分析师曾试图把每个节点的 EUV 曝光次数纳入他们的 ASML 模型，结果全都错得离谱。

读到这里你可能在想：好家伙 Dylan，很棒，但这跟裸片面积有什么关系？

传统观点认为，裸片越大，成本呈指数级上升。我们相信所有读者都知道这一点。更大的裸片面积会增加成本，因为缺陷更容易击中更大的裸片。这是小芯片（chiplet）革命背后的主要驱动力之一。我们在[先进封装系列](https://semianalysis.substack.com/p/advanced-packaging-part-1-pad-limited)文章中，用 AMD 小芯片数据中心 CPU 对比 Intel 单片式（monolithic）数据中心 CPU，对此做了量化。

这一传统思路可能完全错误。让我们用一个带图的假设例子来解释更小的裸片为什么可能制造成本更高。假设一个无厂设计（fabless）芯片设计团队正在纠结：做一颗大单片裸片，还是做 2 颗小芯片的 MCM 设计。左边是布满 25mm × 32mm、800mm2 裸片的晶圆；右边是布满 13.5mm × 32mm、432mm2 裸片的晶圆。两芯片方案每颗小芯片只多花 8% 的硅面积，与 AMD 当前小芯片 CPU 的额外开销相当。尽管两种设计所用的晶圆被模拟为具有相同的每平方厘米缺陷数（0.1），无缺陷裸片的数量在两者之间差异巨大。

单片式设计每片晶圆有 30 颗良品裸片，而小芯片 MCM 设计每片晶圆有 79 颗良品裸片。假设所有缺陷裸片都必须报废。在没有裸片良率分级回收（die yield harvesting）的情况下，单片式设计每片晶圆只能卖出 30 个产品，而小芯片 MCM 设计可以卖出 39.5 个。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2e9503ba-419a-47d9-b8bf-694475fb3ff5_1024x511.png)

采用小芯片加 MCM 后，每片晶圆多产出约 30% 的产品。假设每片晶圆价格为 $17,000，则单片式设计的无缺陷硅裸片成本为 $567，而小芯片 MCM 每颗无缺陷硅裸片成本为 $215、两颗共 $430。显然，如果我们忽略功耗、裸片分级回收和封装成本的差异，设计团队应该选择小芯片 MCM 方案，因为每个产品能省下 $136！

如果我们告诉你这个小芯片 MCM 设计其实更贵呢？

你大概不会相信，但让我们一步步拆解。在这个假设场景中，假设产品采用某代工厂的 5nm 级节点。假设这家代工厂以约 50% 的毛利率、约 $17,000 的价格出售这些晶圆。下面是按耗材或工序划分的成本拆解，包括设备折旧、维护成本、电力使用、分摊下来的人工成本等。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/663648af-c0b8-417d-b918-0ab00cc96b48_1024x875.png)

这些数字相对我们的实际估算做了大幅模糊处理，但有一点是一致的：最大的成本中心是光刻。它几乎占加工晶圆成本的 1/3。这个光刻成本只是一个平均假设值，它会因你选择的裸片尺寸不同而大不相同。

光刻机对晶圆是不加区分地曝光的。它需要知道哪里该曝光、哪里不该曝光。光罩（photomask）承载着芯片设计，遮挡光线或让光线透过以曝光晶圆。一个先进 5nm 代工设计大约需要十几张 EUV 光罩和另外几十张 DUV 光罩。每张光罩对应晶圆上的某个特征或特征的一部分，且对每个芯片设计都是独一无二的。通过光刻与其他所有工序的循环往复，代工厂大约能在 10 周内在晶圆上造出特定的 5nm 芯片。下面是一张 DUV 光罩的照片。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2253f19f-accf-4e60-97fc-61d8f4c9b688_600x600.jpeg)

标准光罩尺寸为 104mm × 132mm。光刻机透过光罩曝光，以 4 倍缩小比例将特征印到晶圆上。这个曝光场（field）为 26mm × 33mm。大多数设计并不能与 26mm × 33mm 完美对齐。

于是就有了光罩利用率（reticle utilization rate）的概念。

通常芯片设计比较小，所以一张光罩可以包含多个相同的设计，如上图所示。即便如此，大多数设计仍无法完美填满 26mm × 33mm 的曝光场，因此光罩上一般总有一部分不会被曝光。

如果裸片为 12mm × 16mm，每张光罩可以放 4 颗裸片。这时光罩利用率相当高，因为只有极窄的一条光罩未被曝光。对于 25mm × 32mm 的单片式裸片，狭缝（slit）方向和扫描（scan）方向各有 1mm 未被利用，光罩利用率同样相当高。而我们的 13.5mm × 32mm 小芯片则不同：这颗裸片太大，无法在光罩上并排放下 2 颗，因此每张光罩只能放 1 颗裸片。上述示例的可视化见下图。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/75d8c7fa-2567-46d4-89cb-b541b92d5a16_1024x392.png)

你可能会问，光罩利用率低有什么问题？

当我们把视角拉远到晶圆级加工过程时，这就成了一个大成本问题。晶圆放入光刻机后，设备一次一个光罩曝光场地对曝光晶圆的一部分。如果整个 26mm × 33mm 光罩都被利用，光刻机以最少的步数扫过 300mm 晶圆——宽 12 个光罩场、高 10 个光罩场。如果光罩利用率较低，设备就必须在每个方向上更多次地在晶圆上步进。

对比每片晶圆上的 25mm × 32mm 单片式裸片与 13.5mm × 32mm 小芯片 MCM 设计，后者需要在晶圆上步进的次数是前者的 1.875 倍！

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/422fde6a-41fb-4529-85bb-2362b1687a94_720x540.jpeg)

现代 DUV 和 EUV 光刻机采用狭缝加扫描的方式。被曝光的是狭缝（26mm），它沿扫描方向（33mm）扫过光罩区域。下面这个由 [Andreas Schilling](https://twitter.com/aschilling/status/1537804140474253312?s=20&t=BXrxL05jt-ZI5rgaLvPvRw) 分享的动图来自 ASML，讲的是 High-NA EUV，很好地展示了这个概念。在 High-NA EUV 下，狭缝最大仍是 26mm，但扫描长度减半。产能损失主要来自晶圆载台必须以多快的速度移动。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a141234b-66d7-45fb-8f6f-bde8c1691220_800x447.gif)

设想一下，如果被减半的是狭缝，对产能的影响会大得多。

对比单片式设计与小芯片 MCM 设计，我们的光刻机占用时间显著上升，因为晶圆必须被扫描的次数增加到 1.875 倍。原因在于狭缝的很大一部分没有被充分利用。虽然晶圆装卸时间方面仍有一些效率可循，但光刻机成本的大头在扫描时间。因此，每片晶圆的内部成本显著上升。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/e70ca358-e3b4-43e4-9bdb-4308d92d9bb9_1024x543.png)

在这个假设场景中，代工厂现在每片晶圆的光刻成本要多花 $2,174。这是一笔巨大的成本增加，对于那些本来利润率就被压得很紧的大客户，代工厂是不会自己消化的。假设代工厂按利润率定价，因此无论设计如何都维持 50% 的毛利率。

光罩狭缝利用不足带来的成本增加，意味着代工厂不会以 $17,000 出售这些晶圆来维持 50.2% 的毛利率，而是会卖到 $21,364。单片式产品的无缺陷硅裸片成本仍为 $567。小芯片每颗无缺陷裸片的成本不再是 $215，而是 $270；每个产品不再是 $430，而是 $541。

现在，小芯片与单片式之间的抉择变得困难多了。一旦把封装成本算进去，单片式裸片的制造成本很可能会更低。此外，小芯片设计还伴随一些功耗成本。在这个案例中，做一颗大单片裸片绝对优于走小芯片/MCM 路线。

这个例子是为了说明光罩利用率问题而选取的最坏情况。这个简化且假设性的分析还有大量附加条件。此外，5nm 之前的多数其他制程节点，以及进入环栅（GAA）时代之后，光刻成本相对其他工序的占比都会更低。多数小芯片架构很可能会提高而非降低光罩利用率。

[留下评论](https://newsletter.semianalysis.com/p/die-size-and-reticle-conundrum-cost/comments)

这是我们钻了几天牛角尖的一个问题，最后对我们的工作或任务没有任何影响，但我们还是想把学到的东西分享出来。特别感谢 Cyrus Tabery 帮助我们理清了本文所讲的光罩利用率相关公开概念。

[分享](https://newsletter.semianalysis.com/p/die-size-and-reticle-conundrum-cost?utm_source=substack&utm_medium=email&utm_content=share&action=share)
