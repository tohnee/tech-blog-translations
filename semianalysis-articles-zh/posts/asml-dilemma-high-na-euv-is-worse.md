---
title: "ASML 的两难：High-NA EUV 不敌低 NA EUV 多重曝光"
title_en: "ASML Dilemma: High-NA EUV is Worse vs Low-NA EUV Multi-Patterning"
subtitle: "低 NA 与 High-NA EUV 的成本模型、图形保真度、技术挑战"
date: 2023-12-11
source: https://newsletter.semianalysis.com/p/asml-dilemma-high-na-euv-is-worse
crawled: 2026-09-15
authors: ["Dylan Patel", "Jeff Koch", "Lithos Graphein"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# ASML 的两难：High-NA EUV 不敌低 NA EUV 多重曝光

> 原文：[ASML Dilemma: High-NA EUV is Worse vs Low-NA EUV Multi-Patterning](https://newsletter.semianalysis.com/p/asml-dilemma-high-na-euv-is-worse) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**低 NA 与 High-NA EUV 的成本模型、图形保真度、技术挑战**

*本文主要由 Jeff Koch 执笔。他上个月从 ASML 加入 SemiAnalysis，将负责我们的半导体资本设备与制造分析。匿名撰稿人「[Lithos Graphein](https://twitter.com/lithos_graphein)」（在芯片与光刻行业拥有数十年经验）也提供了重要帮助，欢迎[关注](https://twitter.com/lithos_graphein)他！*

近年来，光刻领域的「下一件大事」是高数值孔径极紫外光刻，即 High-NA EUV——ASML 光刻机技术演进的下一步。High-NA 的宣传卖点是降低工艺复杂度，并使 2nm 以下的微缩成为可能。ASML 的言下之意是：复杂度降低，成本随之下降。

我们的光刻模型显示：尽管复杂度有所降低，但对于包括 1.4nm/14A 在内的即将到来的技术节点，**High-NA EUV 单次曝光的成本显著高于用现有低 NA 机台做双重曝光**。此外，**低 NA EUV 多重曝光能实现比 High-NA 更细间距的图形**。

ASML 有许多雄心勃勃的目标，比如到 2025 年实现[年出货 600 台 DUV 和 90 台 EUV 机台](https://www.semianalysis.com/p/asml-and-the-semiconductor-market)，但其中最宏大、在我们看来**不可能实现的目标，是到 2028 年 High-NA EUV 机台年出货 20 台的计划**。High-NA 光刻带来了许多需要解决并产业化的新技术挑战，但最艰巨的挑战在于经济性。在下面详述成本及其他关键问题之前，先简单提一下 EUV 与 DRAM 之间发生过的一幕类似剧情。

过去二十年的大部分时间里，三星（Samsung）在 DRAM 技术上一直领先，在与美光（Micron）、SK 海力士（SK Hynix）等对手的竞争中，密度、性能和成本缩放优势明显。这一切在 D1Z 代 DRAM 上风云突变：三星（除其他问题外）过快导入 EUV 而吃了苦头。由于三星的跌撞，美光得以在密度和成本结构上冲到前面。时至今日，尽管三星现已全面采用 EUV，在[密度](https://www.techinsights.com/blog/micron-lpddr5-16-gb-non-euvl-chip-found-apple-iphone-15-pro)和[性能](https://www.semianalysis.com/i/133273576/the-hbm-market-sk-hynix-dominance-samsung-and-micron-investing-to-catch-up)竞赛中仍落后。[美光尽管用的是 DUV，却以相当明显的优势握有全世界最密的 DRAM](https://www.techinsights.com/blog/micron-lpddr5-16-gb-non-euvl-chip-found-apple-iphone-15-pro)。关于三星问题的更多细节，[参见此处](https://www.semianalysis.com/i/52361209/samsung-dram-catastrophe)。

不过必须说清楚：**虽然 High-NA 的技术挑战可以说更小，其经济性挑战却远比当年低 NA 面对的经济性挑战严重得多。**

## High-NA 研发中的妥协

在不复述 EUV 光刻细节的前提下（[EUV 背景](https://www.semianalysis.com/p/lam-research-tokyo-electron-jsr-battle)、[EUV 面临的挑战](https://www.semianalysis.com/p/embracing-chaos-the-imperfect-art)、[小芯片与大裸片之争](https://www.semianalysis.com/p/die-size-and-reticle-conundrum-cost?utm_source=%2Fsearch%2Fasml&utm_medium=reader2)、[半导体供应链](https://www.semianalysis.com/p/i-semiconductor-the-regionalization?utm_source=%2Fsearch%2Fasml&utm_medium=reader2)、[长期晶圆需求](https://www.semianalysis.com/p/lithography-intensity-and-long-term?utm_source=%2Fsearch%2Fasml&utm_medium=reader2)、[ASML 长期展望](https://www.semianalysis.com/p/asml-and-the-semiconductor-market?utm_source=%2Fsearch%2Fasml&utm_medium=reader2)、[光刻出口管制](https://www.semianalysis.com/p/the-gaps-in-the-new-china-lithography?utm_source=%2Fsearch%2Fasml&utm_medium=reader2)以及[奥地利的光罩写入机垄断](https://www.semianalysis.com/p/austrias-silent-monopolies-on-advanced)请参见我们此前的笔记），请允许我们简短回顾一下把 High-NA 塑造成今天这副模样的那些决策。

要让逻辑和存储节点继续微缩，光刻机（scanner）必须能印出越来越小的特征。在 High-NA 研发之初，芯片厂商与 ASML 面临一个艰难的架构决策：如何实现这一点。从根本上说，光刻机设计里印出更小特征只有两个主要旋钮：1) 缩短光源波长；2) 增大镜头（更准确地说是增大镜头的数值孔径 NA）。这一取舍可以用瑞利第一判据来表达——它如此家喻户晓，以至于 ASML 甚至把它印在了 T 恤上。

![](https://substack-post-media.s3.amazonaws.com/public/images/978fa77e-a172-44df-a8fc-685ede7596f8_563x539.webp)

出于诸多正当的技术理由，行业选择了追求更大的投影镜头。遗憾的是，镜头尺寸的增大无法不引发其他问题，主要原因在于 EUV 光掩模技术在主光线角（chief-ray-angle）方面的限制。这迫使 High-NA 架构做出进一步的妥协。

ASML 及其合作伙伴面对的是一堆糟糕的选项：

1. 增大光掩模（photomask）的尺寸——光罩上承载着要印到晶圆上的图形。
2. 缩小成像视场（imaging field）的尺寸

第一个选项不仅是巨大的技术挑战，还会带来大量连锁反应，因为现有光掩模基础设施都是围绕标准的 6 英寸方形光罩生态设计的。即便在现有尺寸下，生产无缺陷的光掩模基板在低 NA 研发时代就已是一大障碍，把面积放大 2 倍或 4 倍更绝非易事。用于检查 EUV 光掩模、使用低功率 EUV 光源的同源光罩检测（actinic mask inspection）设备也是最近才问世，且同样围绕 6 英寸标准设计。EUV 光掩模及其基础设施本来就比 DUV 对应物贵数倍，而面积增大带来的成本增长是急速攀升的。

选项 2 看上去是两害相权取其轻。它虽然也带来严峻的技术挑战，但不需要对光刻机之外的整个光刻生态做大改动。芯片厂商把宝押在了第二个选项上，ASML 随之启动的研发工作很快就将结出硕果——首台 High-NA 光刻机 EXE:5000 的出货。

![](https://substack-post-media.s3.amazonaws.com/public/images/02fd61ec-b157-4c9e-9fcb-1c464c921ea7_1444x766.png)

这些架构决策带来几个关键影响：半场拼接（half-field stitching）、焦深（depth of focus）和光刻胶方面的技术挑战，以及与现有低 NA 机台相比的成本挑战。我们将逐一展开。

## 半场难题

光刻机通过一条曝光狭缝对晶圆曝光。晶圆在狭缝下方移动（即扫描），把光掩模上的图形曝光到晶圆上。整张光掩模图形曝光完成后，光刻机步进到晶圆上一块新区域，重复扫描。曝光场（exposure field）就是光掩模一次完整曝光所覆盖的区域。

你可以在下面 ASML 的 gif 中看到这种步进-扫描运动。请记住，这套运动的速度足以每小时处理数百片晶圆，且图形位置精度达到纳米级、接近原子级——它居然能正常工作，本身就是一个奇迹。

![](https://substack-post-media.s3.amazonaws.com/public/images/6a2bf9f2-5c3e-4f08-bb8e-175482dc4aab_800x447.gif)

High-NA 光刻机的曝光场尺寸只有低 NA EUV 和传统 DUV 机台的一半。这就是那个「两害相权取其轻」的取舍：既保住了行业标准的光掩模尺寸，又实现了镜头的增大。

![](https://substack-post-media.s3.amazonaws.com/public/images/223ff4e6-132f-446a-9eb2-8bbf80deaff3_313x139.png)

这一取舍的「害」之一，是必须在同一片晶圆上混用半场和全场曝光。High-NA 只会用在少数最关键的层上，也就是要印最小图形的那些层。其他层则交给成像能力放宽、更便宜的机台。这意味着光掩模版图和芯片尺寸的规划必须同时兼顾半场与全场成像。要知道，即使没有半场这个额外复杂度，糟糕的光掩模版图也已经在[让小裸片付出高昂代价](https://www.semianalysis.com/p/die-size-and-reticle-conundrum-cost?utm_source=%2Fsearch%2Fchiplet&utm_medium=reader2)，因此这必然会成为未来芯片设计的一个问题。

这里牵扯的问题还有很多，芯片设计师应当高度警觉，我们会在本报告末尾深入展开。现在进入主题：成本与图形保真度。

## 剂量与产能

要理解 High-NA 架构对成本的影响，得先建立基线概念：光刻机的曝光剂量及其对产能的影响。光刻成本主要由光刻机（scanner）的购置成本主导。最新的低 NA NXE:3800E 机台如今单价已超过 2 亿美元（>$200M），因此在每片晶圆的分摊成本中，光刻机产能就成了主导因素。

剂量衡量的是到达晶圆的能量。这些能量在光刻胶中引发化学反应，使其从不可溶变为可溶（或相反）。图形尺寸越小，通常就需要越高剂量以[避免各类误差](https://www.semianalysis.com/p/embracing-chaos-the-imperfect-art)。关键在于：剂量需求随关键尺寸（CD）减小呈指数级上升。

![](https://substack-post-media.s3.amazonaws.com/public/images/2731068e-09ce-44e1-b66b-7eb68756cf6d_1009x460.png)
*IRDS 光刻路线图更新 2021*

这为什么重要？因为剂量影响产能，进而影响成本。更高的剂量意味着要么

1. 使用更强的光源
2. 让光刻机慢下来

ASML 每一代新 EUV 机型的光源功率都在稳步提升，但仍不足以跟上指数级上涨的剂量需求。这意味着光刻机必须放慢速度，以确保每个曝光场至少接收到最低剂量。

简单说：由于剂量需求陡增，光刻成本随关键尺寸减小而急剧上升。剂量越高，产出同样数量的晶圆就需要购置越多机台——也就是说，烧钱。

![产能取决于光刻机光源功率与曝光剂量。更高的光源功率和/或更低的需求剂量带来更高产能，从而降低光刻成本。](https://substack-post-media.s3.amazonaws.com/public/images/2f069c11-d188-40c1-bd74-fbc6c376fad8_886x522.png)
*Levinson，《日本应用物理学报》（Jpn. J. Applied Physics）《High-NA 光刻：现状与未来展望》*

## 低 NA 双重曝光

事实证明，High-NA 有一个现成的替代方案：低 NA 双重曝光。一些芯片厂商已在领先节点上使用，即用一台低 NA EUV 机台做两次曝光来印出单层图形。每次曝光的 CD 要求大约是最终特征尺寸的两倍。这带来一个极其理想的效果：所需剂量大幅降低，因为你在剂量-CD 指数曲线上移到了更靠下的位置。

![](https://substack-post-media.s3.amazonaws.com/public/images/bc07bdf0-b0f2-40fa-a7b8-39c1da67502d_480x264.png)

在这些更低的剂量下，光刻机可以物尽其用；产能将受限于晶圆台与光罩台的运动速度，而非剂量。

## 成本对比

低 NA 双重曝光的产能优势如此之强，以至于尽管晶圆需要通过光刻机的次数翻倍，其光刻成本仍低于 High-NA 单次曝光。我们的模型显示，从当前最先进的 3nm 制程节点直到大约 2030 年前后导入的 1nm 等效节点，这一结论始终成立。

![](https://substack-post-media.s3.amazonaws.com/public/images/99420447-33e5-4a42-8eb1-9bcc54026fa3_1488x925.png)
*成本以低 NA 3nm 归一化，采用 ASML 当年最先进的低 NA 与 High-NA 光刻机，并计入光源、工件台与套刻改进路线图*

成本以低 NA 3nm 归一化，采用 ASML 当年最先进的低 NA 与 High-NA 光刻机，并计入光源与工件台改进路线图

在所有这些节点上，High-NA 的产能都受剂量限制，即便 ASML 如期在 1nm 节点前实现其宣称的 1 kW 光源功率目标也是如此。原因很简单，就是上一节详述的剂量需求快速攀升。在剂量-CD 指数曲线上越靠上，对产能的杀伤越大，以至于尽管 CD 在缩，低 NA 双重曝光的成本优势反而在 2nm 到 1.4nm 节点之间进一步扩大。

而颇具讽刺意味的是，为 High-NA 开发的更快工件台将回移植到未来的低 NA 机型上，提升其产能，进一步拉大对 High-NA 的成本优势——因为低 NA 机台在低剂量下更多受限于工件台速度。

还值得考虑一下光源功率提不到 1kW 的情形。更高的光源功率会加速投影光学系统和光掩模的磨损，因为反射涂层要承受热负载增加等有害影响。有这种可能：高于当今 600W 的功率会让光学元件的磨损达到不可接受的水平——这些是光刻机里最昂贵的部件之一，若寿命过短就更换，成本高昂。

如果我们假设未来光源功率无法继续提升，High-NA 变得更划算的拐点并不会改变，但这确实意味着光刻成本整体将显著上升——未来节点上最多比当前 3nm 基线高 20%。

![](https://substack-post-media.s3.amazonaws.com/public/images/03878c0c-159d-4a42-b175-a1f586bda81c_1484x923.png)
*成本以低 NA 3nm 归一化，采用 ASML 当年最先进的低 NA 与 High-NA 光刻机，并计入工件台与套刻改进路线图*

目前这只是假设——迄今为止，每一代新 EUV 光刻机的光源功率都在持续提升，只是速度不如各大晶圆厂期望的那么快。

事实证明，ASML 的公开材料支持我们的成本结论。传统上，新一代光刻机售价更高，但每片晶圆成本低于现有机型。这对芯片厂商是合理的：只要光刻机满足成像性能要求，他们主要优化的就是每片晶圆的成本。ASML 也很开心，因为卖的是更贵的光刻机。

就在 2020 年，这还是 High-NA 的默认叙事：据说它相对低 NA 双重曝光拥有成本优势。

![](https://substack-post-media.s3.amazonaws.com/public/images/200dd4b3-2436-4841-9bb0-1403fb5f2e72_1438x810.png)
*2020 年：ASML 称 High-NA 成本更低*

但自 2021 年起，首选指标从每片晶圆成本变成了工艺复杂度。降低复杂度固然好，但它并非晶圆厂设备决策的主导因素。运行着 1000 多道工序的芯片厂商早就习惯了复杂度。他们规划晶圆厂、采购设备，依据的是成本和预期良率——而这两项低 NA 看起来都更优。

![](https://substack-post-media.s3.amazonaws.com/public/images/4b2f7f57-f12a-4316-9e35-89bae333ff80_1435x811.png)
*2021 年：ASML 只说 High-NA 复杂度更低*

到了 1nm 和 7A 节点——如今已排到 2030 年以后——成本差距终于弥合。推动这一变化的是从几何微缩到堆叠的范式转变：芯片的性能、功耗与面积改进不再靠水平缩小图形，而是靠垂直堆叠实现。这意味着 CD 要求保持不变，于是光刻胶与光源功率的持续进步使 High-NA 越来越接近持平。

![](https://substack-post-media.s3.amazonaws.com/public/images/e584d522-d113-485f-876d-a08d2d733021_1437x810.png)

我们认为，从 2D 微缩转向 3D、CD 缩小随之放缓，正是 High-NA 导入的天然窗口。这将大幅[改变先进逻辑制造的光刻强度](https://www.semianalysis.com/p/lithography-intensity-and-long-term)。

当然，这个故事远不止剂量与产能。

[领取团体订阅 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
