---
title: "EUV 需求减半？Applied Materials 的 Sculpta 重新定义光刻与图形化市场"
title_en: "EUV Requirements Halved? Applied Materials' Sculpta Redefines Lithography And Patterning Market"
subtitle: "每年减少 45 亿美元 EUV 开支、High-NA、接触孔、通孔、产能、ASP、使用场景、TSMC N2、Intel 18A、Samsung 2nm"
date: 2023-03-06
source: https://newsletter.semianalysis.com/p/euv-requirements-halved-applied-materials
crawled: 2026-09-15
authors: ["Dylan Patel", "George Cozma", "Afzal Ahmad"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# EUV 需求减半？Applied Materials 的 Sculpta 重新定义光刻与图形化市场

> 原文：[EUV Requirements Halved? Applied Materials' Sculpta Redefines Lithography And Patterning Market](https://newsletter.semianalysis.com/p/euv-requirements-halved-applied-materials) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**每年减少 45 亿美元 EUV 开支、High-NA、接触孔、通孔、产能、ASP、使用场景、TSMC N2、Intel 18A、Samsung 2nm**

ASML 的 EUV 光刻机很贵……真的非常贵。如今每一台 EUV 光刻机的价格已逼近 1.7 亿美元，而一座先进制程半导体晶圆厂需要用到很多台。未来，每一台 High-NA EUV 光刻机的价格将超过 3.5 亿美元。此外，这些晶圆厂还需要许多 DUV 光刻机。光刻一项就吃掉 3nm 制程节点约 35% 的成本，人人都想要一种更具性价比的芯片图形化方式。试想如果有一种办法能打破这一趋势……

上周，全球第二大半导体设备制造商 Applied Materials（应用材料公司）宣布他们可能有一个解决方案。这个方案就是 Centura Sculpta 设备——一种能够执行全新工艺步骤「图形整形」（pattern shaping）的新设备。据 Applied Materials 介绍，Sculpta 可在某些层次上将 EUV 光刻的使用减少多达一半。如果属实，这将重塑整个行业的成本结构。Applied Materials 的说法有很大的存疑空间，让我们细细道来。

本报告将深度解析全新的 Centura Sculpta。我们将讨论这项技术的工作原理、它对 EUV 多重图形化（multi-patterning）和 High-NA EUV 的影响、它可以应用的环节（前段、接触孔、通孔、各金属层、剂量削减），以及这些用例将如何随未来工艺技术微缩而演进。此外，本报告还包含针对一个真实工艺节点、分别采用纯 EUV 与 EUV+Sculpta 混合方案的成本对比。我们将分享这台设备的产能（throughput）、周期时间、成本、我们的出货量估算，以及来自首家客户的收入估算。

我们将分享如何得出 EUV 需求可能减少 45 亿美元的结论、这一影响在哪一年会达到该量级，以及哪些因素会令该数字上下浮动。我们将直接讨论 TSMC、Samsung 和 Intel 在 2nm 级节点上对 Centura Sculpta 的采用与导入节点，其中包括即将采用 Applied Materials Sculpta 的某先进工艺的具体节点细节——最小间距（pitch）与 Sculpta 层。这一决策的利弊也将一并讨论。

我们还将讨论引入全新图形整形步骤对其他工艺步骤的影响，包括光刻、光刻胶、涂胶显影机、CVD、PVD、刻蚀、CMP、外延生长、离子注入、量测和检测。图形整形对业内供应商的影响深远，包括但不限于 ASML、Lam Research、Tokyo Electron、JSR、TOK、Shin-Etsu、Lasertec、KLA、Onto、Nova、Hoya 和 Asahi Glass。

首先，尽管这台设备有非常明确的用例，半导体和金融行业却有很多人对它不以为然。有人说它没有任何新意，不过是一种花哨昂贵的电感耦合等离子体（ICP）反应离子刻蚀——这种设备在大规模量产中已存在数十年。照这种说法，也可以说光刻已存在 150 年，EUV 也毫无新意。图形整形的用例显然是独一无二的。

另一种主要的否定意见认为它不成熟、离量产还很遥远。这也是错的。虽然 Sculpta 上周才在 SPIE 光刻与先进图形化会议上正式发布，这台新设备其实酝酿已久。Applied Materials 至少从 2015 年起就持续发表关于此类设备的公开研究论文。第一家客户自 2017 年前后就与 Applied Materials 在这台设备上展开合作。Applied Materials 去年甚至在 SPIE 先进光刻与图形化会议上做过一场技术报告，展示了真实的客户测试数据。

关于那场报告有个有趣的故事。报告结束后，我们走出会场，与几位同场听众交流。大家的一致看法是：这东西超酷，但行不通。为什么？企业在 SPIE 上的报告不外乎三类：1，即将进入量产的东西；2，还差很多年、纯粹用来提前占位（plant a stake in the ground）的东西；3，根本行不通、但数据放着也是放着不如拿出来讲讲的东西。我们去年的假设是它属于第 2 类和/或第 3 类。这个假设错了。

[Share](https://newsletter.semianalysis.com/p/euv-requirements-halved-applied-materials?utm_source=substack&utm_medium=email&utm_content=share&action=share)

Applied Materials 的 Centura Sculpta 并非什么完全不成熟、距量产遥遥无及的疯狂技术。Sculpta 是真实存在的，它确实管用，并将在未来几年创造数亿美元的收入。鉴于它的第一个用例被宣传为直接去除 EUV 双重图形化，我们先快速回顾一下光刻多重图形化工艺。

## **光刻多重图形化工艺**

光刻是大批量半导体制造的核心工艺。基础原理我们不再赘述，可参阅我们此前关于该主题的报告。[1,](https://www.semianalysis.com/p/embracing-chaos-the-imperfect-art) [2,](https://www.semianalysis.com/p/lam-research-tokyo-electron-jsr-battle) [3,](https://www.semianalysis.com/p/die-size-and-reticle-conundrum-cost?utm_source=%2Fsearch%2Fasml&utm_medium=reader2) [4,](https://www.semianalysis.com/p/lithography-intensity-and-long-term?utm_source=%2Fsearch%2Fasml&utm_medium=reader2) [5,](https://www.semianalysis.com/p/asml-and-the-semiconductor-market?utm_source=%2Fsearch%2Fasml&utm_medium=reader2) [6,](https://www.semianalysis.com/p/the-gaps-in-the-new-china-lithography?utm_source=%2Fsearch%2Fasml&utm_medium=reader2) [7](https://www.semianalysis.com/p/i-semiconductor-the-regionalization?utm_source=%2Fsearch%2Fasml&utm_medium=reader2)

一旦越过光刻机的极限，你仍然可以通过各种多重图形化方案继续微缩单一特征尺寸。下图是「光刻-刻蚀-光刻-刻蚀（LELE）」的简化示意——最常见的多重图形化方案之一。为简单起见，我们在此把 SADP、LELB 等其他方案也归入 LELE 一类。

![](https://substack-post-media.s3.amazonaws.com/public/images/f78f0711-8fd2-4ae5-a993-cdae9f1c9180_1051x832.png)

LELE 工艺流程要完整走两轮光刻循环，以实现单次图形化所达不到的更小特征尺寸。完整的一轮循环可能包含数十个不同的工艺步骤，包括硬掩膜沉积、底层、中间层、BARC、CMP、清洗、去胶、旋涂、烘烤、显影、曝光、刻蚀，以及穿插其间的各类量测/检测步骤。

关键在于：从单次光刻循环改为 LELE 工艺，意味着光刻成本翻倍，工艺中涉及的许多其他设备也要翻倍。

Applied Materials 明确将削减 EUV 多重图形化作为 Sculpta 的第一个用例。他们声称，用单次光刻循环加 Sculpta，即可达到与 LELE 同等的图形保真度。

![](https://substack-post-media.s3.amazonaws.com/public/images/921592c0-0b90-453f-8f99-f469704859b9_2666x1377.png)
> 我们估算每个 LE（光刻-刻蚀）循环每片晶圆约消耗 25 千瓦时电力、排放约 0.5 千克二氧化碳当量、消耗约 15 升水。右侧方框展示的是成本。我们估算每 10 万片月投片产能约需 3.5 亿美元资本成本，每个 EUV 循环每片晶圆约 70 美元的制造成本即运营开支（OpEx）。至于成本节约，我们估算每 10 万片月投片产能可节省约 2.5 亿美元资本成本，每片晶圆可节省约 50 美元制造成本。

Applied Materials 给出的成本、电力、水和二氧化碳节约 claim 相当惊人。TSMC 的 7nm 和 5nm 节点已爬坡到（大约）每月 20 万片晶圆。按每层计算，这将为他们在资本开支上节省 5 亿美元，每年运营开支上节省超过 1 亿美元。我们的数字与他们不同，将在后文分享。

TSMC 5nm 有一个 EUV 多重图形化步骤。TSMC 3nm 包含多个 EUV 多重图形化步骤。这项技术瞄准的是在「2nm」级节点上的导入——若没有 Applied Materials Sculpta 图形整形，这些节点可能包含超过 10 个 EUV 多重图形化步骤。如果假设 Sculpta *处处*可用，它的使用每年可节省*数十亿美元*。

这种分析过于简化，图形整形不可能处处可用。我们将分享它可以在哪里、如何使用，但先来谈谈 Sculpta 和图形整形究竟是什么。

## **什么是 Centura Sculpta 和图形整形？**

Centura Sculpta 的核心是能够执行一种名为「图形整形」的新型步骤。图形整形是以一定角度向晶圆发射带状等离子体束。相对于晶圆，角度可以在 0 到 70 度之间调控。零角度即与晶圆呈 90 度角——垂直入射。

![](https://substack-post-media.s3.amazonaws.com/public/images/34f16ec9-5c53-48db-bbad-a59140bf9cc6_2012x1052.png)

等离子体束沿一维行进，以保证整片晶圆加工的均匀性。其目的是让特征图形沿单一方向单向拉伸。通过旋转晶圆并让束流再次扫过晶圆，图形整形可以在任意方向上执行。

![](https://substack-post-media.s3.amazonaws.com/public/images/d83f823e-676a-4247-a5f0-583c58186548_2008x1062.png)

图形整形的关键在于不能影响必须保持不变的硅特征尺寸（critical dimension）。这意味着只改变特征在一个轴上的尺寸是关键所在。Applied Materials 表示，他们可以在一个方向上改变 20 个长度单位，而另一个方向仅变化 1 个长度单位。

![](https://substack-post-media.s3.amazonaws.com/public/images/9fec0437-7d6d-4ecc-8bb7-683068202a06_1100x522.png)

这种定向加工具有高度选择性。晶圆厂还可以通过增加或减少带状束轰击的时间，来控制图形被拉伸的程度。刻蚀时间是晶圆厂可以灵活运用的重要杠杆。

保持形状均匀的另一个考量，是确保束流角度针对晶圆上各种不同结构做了优化。

![](https://substack-post-media.s3.amazonaws.com/public/images/a2429a8d-6190-43dc-80b6-d7297fb6e59b_2206x990.png)

如果束流角度对位不当，不同尺寸的结构上就可能出现阴影效应（shadowing）。

![](https://substack-post-media.s3.amazonaws.com/public/images/9777d4c1-13c5-40c1-a3b9-5f9f50e4292f_2013x1082.png)

如果平坦化层与硬掩膜的刻蚀选择比不同，等离子体束就会导致侧壁无法均匀笔直。

特征的侧壁形貌必须优化，否则会出现性能、功耗或良率问题。

![](https://substack-post-media.s3.amazonaws.com/public/images/6d1f9795-2fce-48cf-aeb9-117cb25e2810_2022x1063.png)

等离子体束的入射角度对晶圆厂的优化至关重要，以确保各种尺寸的特征获得均匀一致的拉伸量。采用较高角度还是较低角度，需要在刻蚀所需时间、顶层侵蚀速率与底层侵蚀速率之间权衡，以保住关键尺寸完好。每种应用的束流角度和时间各不相同。Applied Materials 已开发多种不同的化学配方，使束流可以配合各种硬掩膜、底层和中间层使用。

![](https://substack-post-media.s3.amazonaws.com/public/images/cc6fb089-3cf3-48c0-a32a-8e0356f3cf81_2028x1063.png)

图形整形发生在光刻胶和抗反射涂层层的显影、清洗和刻穿之后。

![](https://substack-post-media.s3.amazonaws.com/public/images/3f48c444-4f1e-478e-b342-df58bc389d2d_2016x1082.png)

图形整形完成后，即可进行图形转移刻蚀。因此，即使你有多重掩膜和多个图形化阶段，图形整形依然可用。图形整形可以与多重图形化结合。

图形整形也不必只沿既有特征的方向进行，它还可以以任意角度执行。在我们看来，这更多是 Applied 借 Sculpta 展示其对准与工艺控制能力的秀肌肉，而非存在非对称整形的真实用例。我们想不出非对称整形的用例，但如果你认为有，欢迎分享。

![](https://substack-post-media.s3.amazonaws.com/public/images/23902a6e-f798-4970-ab85-8904feafc8d4_2011x1078.png)

讲完图形整形是什么，接下来讲它的实际用例。

## **用例**

Sculpta 设备有 3 大用例：紧凑的孔与槽图形、更窄的端到端（tip-to-tip）间距，以及消除随机性桥连缺陷。

第一个应用是用传统光刻-刻蚀（LE）方法实现紧凑的孔间/槽间角对角（corner-to-corner）尺寸需要多重图形化，而有了图形整形，你只需一次 LE 步骤就能获得紧凑的角对角。紧凑的角对角之所以重要，是因为它让你能在同样面积内放入更多特征。以通孔（via）为例，这带来更大的通孔面积，从而改善性能与功耗特性。

![](https://substack-post-media.s3.amazonaws.com/public/images/ec29b50a-768a-4fcf-ad56-858ad0d0cdfb_2009x1073.png)

在上图中，左侧展示了用传统自对齐 LELE 技术如何实现紧凑的角对角。要让通孔达到紧凑的角对角，你需要 2 张不同的掩膜版；而有了图形整形，你可以用单一掩膜版先做出所有不带紧凑角对角的通孔，再把通孔整形成紧凑角对角。

第二个应用是生成端到端间距更紧凑的沟槽。它与第一个应用非常相似，只是特征类型不同。在这个应用中，图形整形用于让两组线条尽可能靠近，而无需使用第二张掩膜版。

![](https://substack-post-media.s3.amazonaws.com/public/images/e17af23d-d9aa-4b03-973e-3ee65a227a78_2018x1081.png)

左侧是传统 LELE 技术：第一张掩膜版做出线条，第二张掩膜版在两组线条之间切开一道分割，以获得尽可能紧凑的端到端间距。而用图形整形，你只需一张掩膜版做出两组中间留有宽松沟槽的线条，然后 Sculpta 尽可能多地去除材料，把沟槽缩到尽可能细。

![](https://substack-post-media.s3.amazonaws.com/public/images/915cace0-fdb3-485f-aa0b-14b23d6428e5_2020x1088.png)

第三个应用是减少随机性（stochastic）桥连缺陷。随机性桥连缺陷是线条上刻蚀未能全部去除本应去除材料的位置。通常这是因为光刻胶层未被光刻机充分曝光。关于随机误差更详尽的解释见此处。

[![](https://substackcdn.com/image/fetch/$s_!HwSb!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F0150776c-9bf2-4bea-a9c2-41b24b7a0f15_1280x1280.png)SemiAnalysisEmbracing Chaos: The Imperfect Art of Semiconductor Manufacturing And LithographyAll manufacturing in the world is built upon stacking multiple processes and systems with various tolerances and variation ranges to get a consistently useful product. Nowhere is this more evident than in semiconductor manufacturing due to being the single most complicated manufacturing process with the lowest tolerance for error in the world. Despite these challenges, the semiconductor industry has stacked hundreds of abstraction layers on top of each other for the software world to see a consistent device. As the layers are peeled back, an extreme amount of variation reveals itself…Read more4 years ago · 24 likes · 15 comments · Dylan Patel and Afzal Ahmad](https://www.semianalysis.com/p/embracing-chaos-the-imperfect-art?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

这些缺陷会因电子跑到不该去的地方而增加功耗。如果一处桥连最终把两个关键层短接在一起，造成短路或通信错误，还会导致良率下降。Applied Materials 表示，借助图形整形，Sculpta 可以将这些缺陷减少 90% 以上。

![](https://substack-post-media.s3.amazonaws.com/public/images/53eef56a-b07a-4214-b29a-114da28fada1_2017x1058.png)

在另一场报告中，ASML 谈到对于 EUV 单次图形化，当端到端间距缩小到 27nm 以下时，随机缺陷开始呈指数级增加。图形整形将有助于显著减少这类图形缺陷，因为光刻机可以打印更宽松的特征，再由 Sculpta 整形到更紧的端到端。图形整形同样有助于以相同方式减少沟槽间缺陷。

![](https://substack-post-media.s3.amazonaws.com/public/images/e54631b7-6373-4458-a527-0df765ffebdf_3485x1468.png)

需要指出的是，ASML 的数据基于简化流程；真实芯片中使用的复杂布线，在当前光刻胶体系下会把缺陷墙推到 30nm 或以上。

## **首个用例——金属互连叠层**

金属叠层（metal stack）是任何工艺节点最重要的部分之一，它负责在晶圆上实现信号布线。金属叠层由十余层组成，其中最重要的是 M0 到 M4 层。在现代工艺节点的版图上，M0、M2、M4 是与栅极垂直的关键金属层，M1 和 M3 则与栅极平行。

![](https://substack-post-media.s3.amazonaws.com/public/images/ed42483c-a503-4859-bea2-3d49b6f6db7d_950x449.jpeg)

芯片的金属叠层是一个充满复杂艰难权衡的领域。每一层金属做得越密、越细，能完成的信号布线就越多，最终能在给定面积里塞进更多有用晶体管。然而，这要付出巨大代价。

金属线越细，电阻越大。还记得高中物理的欧姆定律吧。欧姆定律指出 R = (V/I)，其中 R 是电阻，V 是电压，I 是电流。尽管欧姆定律在如此细小的导线上并不严格成立，工艺节点集成工程师必须应对金属层越密、电路电阻越高的问题。他们可以通过提高电压或降低电流来补偿。简化的权衡是：更密的金属叠层发送一个信号比更宽松的金属叠层耗费更多功耗。缩小金属间距并不总是好事。

![](https://substack-post-media.s3.amazonaws.com/public/images/7cfbec64-d814-495d-908b-c4299013f153_950x353.jpeg)

铜是 Intel、TSMC 和 Samsung 的 3nm 与 4nm 工艺节点的首选金属。在当前光刻胶体系和套刻精度下，单次图形化 EUV 的线条间距极限约为 32nm。对通孔而言，这个数字其实更高。为简单起见，我们假设所有特征的 EUV 单次图形化极限都是 30nm。

![](https://substack-post-media.s3.amazonaws.com/public/images/722080e9-54ce-47a4-b991-80a78a0d249f_2094x1474.png)
*示例用途，非真实数据*

这个例子**极其简化**，仅作**演示用途**。上图是芯片上的单一金属层。EUV 单次图形化工具能定义的每个 30nm x 30nm 单元，可以是铜，也可以是绝缘体（通常是 SiO2）。实际光刻并非如此运作，但这样解释起来更容易。

如果使用 EUV 单次图形化，金属层看起来就像上面那样。许多导线四处延伸，把信号从芯片一处送到另一处。这些导线还与我们视线所及这一层的上下各层相连。在很多情况下，该层中有一些通孔直接上下传递信号到其他层，而不做布线。在这个例子中，由于金属线只有 30nm 宽，电阻上的代价很大。

多重图形化由此登场。目标不是塞进更多导线，而是让铜面积最大化、SiO2 面积最小化。这样能降低电阻，从而在信号传遍全芯片时获得更高的性能与能效。

为简单起见，我们假设多重图形化的极限从 30nm 变为 15nm。现实中，当前 LELE EUV 的极限更接近约 21 到 23nm。上限是 [TSMC N3E 工艺节点 M0 金属层的间距](https://www.semianalysis.com/p/tsmcs-3nm-conundrum-does-it-even)，下限是我们后文将讨论的 2nm 级节点。需要说明，多重图形化并不能把间距直接减半，因为[套刻误差叠加与随机误差](https://www.semianalysis.com/p/embracing-chaos-the-imperfect-art)会吃掉一部分裕量。

![](https://substack-post-media.s3.amazonaws.com/public/images/67f7907e-5622-493a-b986-e6d3e66a3437_2226x1464.png)
*演示用途，LELE EUV 加图形整形实际做不到*

在这个**极度简化的演示性假想例子**中，如果像素尺寸变成 15nm，布线密度保持不变。相反，这提升的图形保真度会被用来按比例沉积更多的铜、更少的 SiO2。铜线宽从 30nm 提升到 45nm，端到端间距也得到改善。SiO2 绝缘层仍然存在，以防止铜信号互相混杂、造成芯片短路。

![](https://substack-post-media.s3.amazonaws.com/public/images/0b5a8a53-e0e4-40f0-a6f0-10e1dadd1e70_950x353.jpeg)

线宽和端到端间距的增加带来电阻大幅下降，以及功耗与性能的改善。注意，从单次图形化转向 SALELE 或图形整形，端到端与线间距并不会同时双双改善，这个例子是**夸张且不现实的**，只为在**概念上**展示潜在收益。

现实世界中，收益更小，但确有必要，而且这正是图形整形的主要用例之一。特征密度用单次图形化已能实现，但这些特征的形状却做不到。图形整形帮助把光刻能印出的特征，变成晶圆厂想要的形状。

![](https://substack-post-media.s3.amazonaws.com/public/images/87956ef3-86fd-42f0-9a7d-f8df67ca93d1_2666x1375.png)

金属层和通孔层之间还存在良率与功耗的权衡。通孔是各金属层之间的连接方式。每一层先制造出来，再完美地堆叠在一起。工艺裕量与套刻精度决定了能否完美堆叠。

![](https://substack-post-media.s3.amazonaws.com/public/images/002fc70a-b4c8-464d-a279-2323d736069c_1830x932.png)

任何对位偏差都可能导致一层错过其下一层，该连接的地方没有连接（开路，opens）。更糟的是，金属层可能与本不该相连的另一层相连，形成错误连接（短路，shorts）。由于图形整形是一个选择性工艺，晶圆厂可以按需要的方向和量，上下调节定向刻蚀，在最大化特征尺寸的同时把短路和开路降到最低。

电阻问题非常显著，尤其是在图形整形最适用的高层通孔上。在 TSMC 的 N3E 节点上，超过 90% 的通孔电阻来自 V0 到 V5。

![](https://substack-post-media.s3.amazonaws.com/public/images/667b24bd-6037-4f92-b3a2-4f6888307aff_1618x1410.png)
*TSMC*

就通孔电阻而言，接下来的 9 层通孔微不足道。如果 V0 到 V5 的通孔能做得更大、又仍装在同样面积之内，电阻就会下降，密度也不受影响。

![](https://substack-post-media.s3.amazonaws.com/public/images/a675ac32-498c-4120-8e2c-4a10d1646a31_2666x1363.png)

从功耗与性能视角看，多重图形化带来的更佳图形保真度对金属叠层极为有利，但从成本角度看则损失惨重：每个金属层的工艺步骤数量几乎翻倍。

图形整形无法增加给定面积内的金属层或通孔数量，但能增大它们的尺寸并缩小端到端间距。第一个用例将于 2024 年底/2025 年进入量产的某个节点的金属叠层上落地。

本报告的后半部分为订阅者专享。我们将讨论并量化对 EUV 多重图形化和 High-NA EUV 的影响，讨论 Sculpta 的用例将如何随未来工艺技术微缩而演进，并分享针对一个真实工艺节点、分别采用纯 EUV 与 EUV+Sculpta 混合方案的成本对比。我们还将披露这台设备的产能、周期时间、成本、我们的出货量估算，以及来自客户的收入估算。

我们将直接讨论 TSMC、Samsung 和 Intel 对 Centura Sculpta 的采用与导入节点，其中包括即将采用 Applied Materials Sculpta 的某先进工艺的具体节点细节——最小间距与层次。其中有利有弊。

我们还将分享引入全新图形整形步骤对其他工艺步骤的影响，包括光刻、光刻胶、涂胶显影机、CVD、PVD、刻蚀、CMP、外延生长、离子注入、量测和检测。图形整形对业内供应商的影响深远，包括但不限于 ASML、Lam Research、Tokyo Electron、JSR、TOK、Shin-Etsu、Lasertec、KLA、Onto、Nova、Hoya 和 Asahi Glass。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
