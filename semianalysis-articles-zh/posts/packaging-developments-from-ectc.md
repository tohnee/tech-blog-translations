---
title: "ECTC 2022 先进封装进展"
title_en: "Packaging Developments From ECTC 2022"
subtitle: "台积电 CoWoS-R+、台积电第四代 SoIC、英特尔集体式裸片-晶圆混合键合、AMD V-Cache、索尼领先的 1 微米间距混合键合、联发科网络 SoC 与共封装光学"
date: 2022-06-08
source: https://newsletter.semianalysis.com/p/packaging-developments-from-ectc
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# ECTC 2022 先进封装进展

> 原文：[Packaging Developments From ECTC 2022](https://newsletter.semianalysis.com/p/packaging-developments-from-ectc) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**台积电 CoWoS-R+、台积电第四代 SoIC、英特尔集体式裸片-晶圆混合键合、AMD V-Cache、索尼领先的 1 微米间距混合键合、联发科网络 SoC 与共封装光学**

ECTC 是先进封装领域最顶级的会议，混合键合、共封装光学（CPO）等我们在先进封装世界中最喜欢的一些议题都在会上得到讨论。围绕这些议题，还有一些交易和供应链细节可以由我们独家披露。今年我们有机会以线上方式参加了 2022 年 IEEE 第 72 届电子元件与技术大会（Electronic Components and Technology Conference）。这场会议是线下举行的，可惜我们错过了那些精彩的现场自由交流。不过明年我们一定会去现场！即便如此，这次会议仍有不少值得总结的有趣新闻、发布与技术进展。

我们将讨论的亮点包括：台积电（TSMC）的 CoWoS-R+、台积电第四代 SoIC（3 微米间距混合键合）、英特尔（Intel）与 CEA-LETI 的自对准集体式裸片-晶圆混合键合、三星（Samsung）关于单片式 vs MCM vs 2.5D vs 3D（含混合键合）的研究、即将在 DRAM 上商业化的 SK 海力士（SK Hynix）晶圆-晶圆混合键合、日月光（ASE）的共封装光学先进封装、思科（Cisco）的共封装光学、Xperi 的超薄裸片取放方案、东京电子（Tokyo Electron）晶圆-晶圆混合键合的晶圆搬运、索尼（Sony）1 微米混合键合、AMD Zen 3 上的 V-Cache 混合键合，以及联发科（MediaTek）InFO-oS 网络 SoC 的可靠性。

# **台积电的 CoWoS-R+**

正如我们在[先进封装入门系列](https://semianalysis.substack.com/p/advanced-packaging-part-2-review)中所讨论的，CoWoS 是一种后置芯片（chip-last）封装技术。CoWoS 通常是先把有源硅裸片放到无源硅中介层之上，但这种做法相当昂贵。为此，台积电开发了 CoWoS-R，改用带 RDL（再布线层）层的有机基板，成本更低。CoWoS-R 尚未出现在公开出货的产品中，但已有一些产品在路上。我们所知的首款此类产品来自 AMD，将在仅限订阅者的章节中讨论，包括其系统架构。坦白说，非常惊艳。

台积电没有止步于 CoWoS-R，CoWoS-R+ 是对该技术的进一步演进。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/3a0679a0-acfc-4788-af21-77b898671453_1023x392.png)

需要理解的关键概念之一是裸片间连接的距离。HBM 目前是唯一能把内存带宽提升到 AI 与高性能计算所需合理水平的手段。这一前沿的进步非常迅速：初代 HBM 每焊盘速率为 1Gbps，到 HBM2 已快速提升至 2.4Gbps，HBM2E 世代达到 3.2Gbps，HBM3 更是一路冲到 6.4Gbps。封装宽度也从 HBM2 时代的 7.8mm 增长到 HBM2E 的 10mm 再到 11mm，这意味着互连长度如今已增长到约 5.5mm。

简单来说，导线需要承载快得多的数据速率，同时还要走更长的距离。这极其困难，而且会产生大量噪声，降低信号完整性。另一个问题是，随着摩尔定律的放缓与日益增长的性能需求相互博弈，芯片功耗正在爆炸式增长。英伟达（Nvidia）的 Hopper 已经达到 700W，未来封装还将膨胀到千瓦级。HBM3 也比 HBM2E 更耗电。流经封装的功率更大，同样可能产生更多噪声，进而劣化信号完整性。为此台积电开发了新的高密度 IPD（集成无源器件）来应对。简而言之，台积电的客户可以在 CoWoS-R+ 上实现 6.4Gbps 的 HBM3，但在 CoWoS-R 上做不到。高密度 IPD 的重要性在于引入额外电容、让供电更平滑。例如 Graphcore 仅凭台积电的 SoIC 混合键合塞进一大堆电容，就在不增加功耗的情况下把频率提高了 40%，[我们在本文中有详细分析](https://semianalysis.substack.com/p/graphcore-announces-worlds-first?s=w)。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a4717ebd-1bab-41a4-838c-95e208f0ec6b_1024x718.png)

台积电还分享了嵌入式桥接裸片（embedded bridge die）能力的更多进展。桥接裸片与顶部有源裸片之间的互连可以低至 24 微米。台积电如今可以做到 3 倍光罩极限，与 CoWoS-S（完整无源硅中介层）持平。未来他们的路线图最高要做到 45 倍光罩尺寸，这意味着采用后置芯片工艺的复杂芯片可以用于晶圆级封装。与此同时，CoWoS-S 明年也只会扩展到 4 倍。

# **台积电第四代 SoIC：3 微米间距混合键合**

台积电发表了其第四代混合键合技术的研究，可实现每 mm² 100,000 个键合焊盘。考虑到目前只有 AMD 和台积电出货过一款 SoIC 器件，能在如此面向未来的技术上看到切实进展，令人欣慰。那款器件的间距显著放宽到了 17 微米，而第一代 SoIC 的能力是 9 微米。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1b5209a9-11f9-4c17-a7af-989f4280258f_1024x340.png)

台积电混合键合的工艺流程大体不变。从已完成的前道晶圆出发，生长一层新的键合焊盘层，刻蚀成形，沉积种子层，再电镀。接着对顶部裸片晶圆进行减薄和切割。要特别注意保持洁净。然后进行等离子体活化，完成裸片键合。

台积电的论文展示了 SoIC 的良率，非常有意思。测试采用 6mm × 6mm 测试裸片上的菊花链测试结构——恰好与 AMD V-Cache 的裸片尺寸相同。芯片-晶圆（chip-on-wafer）混合键合中最慢的步骤之一，就是 Besi 机台实际拾取裸片并将其放置到底部晶圆上。这一键合步骤深受精度制约，产能与精度的权衡是一场硬仗。台积电在 3 微米 TSV 间距下展示的结果是：失准小于 0.5 微米时良率没有差异、电阻没有实质变化，键合良率达 98%。失准在 0.5 到 1 微米之间时，结构仍能成活，但菊花链结构最后 10% 的电阻急剧上升。失准大于 1 微米时，良率只有 60%，且所有测量结构的电阻都超出规格。0.5 微米是一个非常关键的水位，因为 Besi 声称其 8800 Ultra 机台的精度是 <200nm，尽管我们听说实际更接近 0.5 微米且方差很大——这还是在产能只有机台额定规格一半的情况下。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/3a0b07eb-ad66-4fd6-a2b6-711122e2ca2e_1024x650.png)

台积电还展示称，由于阻挡层更薄，整个堆叠的接触电阻都有改善。此外，台积电认为 SoIC 更可靠，包括在更宽的工作温度范围内。当 AMD 在 5800X3D 桌面芯片上完全锁死超频和功耗修改时，许多人大失所望。这很可能只是第一代的一个小坎。随着台积电调整铜合金配方、SoIC 第四代间距缩小，其可靠性和良率似乎都在改善。

# **英特尔与 CEA-LETI 的集体式裸片-晶圆混合键合**

关于裸片-晶圆 vs 晶圆-晶圆 vs 集体式裸片-晶圆键合的深入对比（包括设备生态、订单归属和 TCO），我们会在先进封装系列中详述，这里先做个简短说明。裸片-晶圆键合的精度远低于晶圆-晶圆键合，速度也慢得多。例如，尽管 Besi 宣称每小时可放置 2,000 颗裸片，但要达到哪怕 1 微米的精度，产能就会跌到每小时 1,000 颗以下。另一方面，晶圆-晶圆键合也有许多问题：无法做异构集成，也无法在键合步骤之前对裸片进行测试和分级筛选（bin）。集体式裸片-晶圆键合在精度和产能上都优于裸片-晶圆键合，同时还保留了测试、分级以及实现异构集成的能力。

英特尔与 CEA-LETI 将集体式裸片-晶圆键合与一种自对准技术相结合，实现了 150nm 的平均失准（比裸片-晶圆键合精确得多），且产能更高。这种自对准技术非常巧妙。他们利用水滴的毛细力：改造过的拾放（pick and place）机台先快速、较不精确地把裸片放到目标位置，随后水滴的毛细力让对准变得更精确。水分蒸发时，直接键合随即形成，不需要任何其他中间材料。键合后的晶圆再进入标准退火步骤，使键合进一步强化。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c870bdc1-4aca-42a1-8d52-682fb32ec1b7_820x1024.png)

除了水滴沉积之外，唯一的独特步骤是在键合位点涂覆亲水与疏水材料，这可以用光刻定义，套刻精度达纳米级。这个过程并非毫无问题。水的分配、液滴特性、冷凝和键合工艺都存在不少问题。英特尔与 CEA-LETI 用 3 项指标呈现结果：收集良率（Collection Yield）指水滴成功挂在裸片上；键合良率（Bonding yield）指成功键合的裸片数量；对准良率（Alignment yield）指达到亚微米精度的裸片数量。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/118fd751-ba3c-466d-a1c9-2cfe3601d5a8_1024x1006.png)

他们尝试了多种工艺的组合矩阵，最优组合的键合良率达到 98%，其他步骤均达 100%。整体对准精度令人惊叹：所有裸片的对准精度都小于 1 微米，大多数低于 0.2 微米。英特尔与 CEA-LETI 还用多种不同裸片尺寸进行了尝试，而这一工艺在高纵横比裸片上表现尤为出色，非常有意思。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2b99cacc-fba8-40ea-a45d-bffe86677943_1024x620.png)

# **三星：单片式 vs MCM vs 2.5D vs 3D（含混合键合）**

三星发表了一项关于先进封装在面积与功耗层面成本的非常有意思的研究。他们对比了两类主要设计：受带宽约束的（HPC/AI）与受延迟约束的（CPU）。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d1900a01-abf5-4338-ae95-617f7927365b_1023x521.png)

用于 HPC 与 AI 对比的单片式 2D 芯片面积为 450mm²。它被切分开，再用先进封装拼回去。MCM 版本的功耗增加 2.1%、裸片面积增加 5.6%。2.5D 设计功耗增加 1.1%、面积增加 2.4%。3D 设计功耗仅增加 0.04%，但面积增加 2.4%。当然这些结果是理想化的，现实世界中还会有布局规划（floorplan）与版图相关的更多开销。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/79258b4a-d93c-4146-9916-a463c190856a_1024x541.png)

# **SK 海力士晶圆-晶圆混合键合 DRAM**

SK 海力士发表了其晶圆-晶圆混合键合工艺的研究。晶圆-晶圆键合在先进封装中已经非常普遍：索尼、三星和豪威（Omnivision）的 CMOS 图像传感器都在用；长江存储（YMTC）在其 NAND 闪存中使用自家的 [XStacking 技术](https://semianalysis.substack.com/p/the-impending-chinese-nand-apocalypse-e01)；[Graphcore 与台积电的 BOW 芯片](https://semianalysis.substack.com/p/graphcore-announces-worlds-first?s=w)也在用。我们曾独家告诉过大家，SK 海力士将在其 [16 层 HBM 堆叠](https://semianalysis.substack.com/p/advanced-packaging-part-2-review)中使用混合键合。SK 海力士没有直接给出良率数字，但他们似乎对这项技术的商业化非常有信心。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1709c09f-aa0c-4841-bda2-c8d97f2bc7a9_805x1024.png)

# **日月光（ASE）的共封装光学**

日月光发表的内容从技术角度看并不算多么开创性，但对投资者的意义却不小。因为过去大型 OSAT 封测厂一直远离光网络产品。在我们看来，这项研究对我们总体上喜欢的 Fabrinet 这类公司不是好消息。话虽如此，这毕竟只是研究，市场上的实际动作更重要。无论如何，如果日月光在研究这个，他们很可能也想来抢份额。下面看看日月光发表了什么。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/5e5f479c-481f-4b29-b6a2-69ba3b707b66_1024x917.png)

引线键合（wirebonding）是 100G 世代的主力技术，但向 400G 和 800G 世代过渡时开始成为瓶颈。其他公司转型已有一段时间，例如英特尔和 Fabrinet 在最近几代产品中已不再对 PIC（光子集成电路）与 EIC（电子集成电路）做引线键合。思科也已从引线键合转向倒装芯片（flip chip），今年他们甚至发表了带 TSV 的 3D 组装，远比日月光展示的先进。我们会在仅限订阅者的章节讨论思科及其制造伙伴。

日月光的论文总体上梳理了光制造的独特挑战，包括污染工艺的差异、所用的特殊切割与刻蚀技术。晶圆后道工艺也有所不同，例如凸点下金属化（UBM）和硅等。论文还讨论了独特的测试要求。日月光要进入光制造还有很长的路要走，但必须持续关注他们——他们可能成为电信与数据中心市场光组装与封装领域一个非常能打、令人生畏的新进入者。

# **Xperi 的超薄裸片取放**

在大多数混合键合中，裸片必须极薄。以即将到来的 16 层 HBM 为例，厚度甚至只有 30 微米量级，不到人发直径的一半。硅裸片极其脆弱，无法用常规方式拾取。因此，Xperi 发表了用伯努利吸附（Bernoulli grip）拾取裸片的研究——利用高速气流与低静压，在不发生物理接触的情况下吸附物体。随后夹持器把裸片以 1 微米以内的精度放到另一颗裸片上。论文对裸片翘曲和搬运有很多细节讨论。这里没有什么开创性的东西，我们只是觉得这种搬运超薄裸片的机制很酷。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8d3fcd58-827b-4cd5-aa0f-821e61cdb5d6_1024x583.png)

# **东京电子的晶圆-晶圆混合键合**

我们曾独家向订阅者披露，东京电子的晶圆-晶圆混合键合设备与工艺流程在[全球最大代工厂拿下重磅订单](https://semianalysis.substack.com/p/graphcore-announces-worlds-first?s=w)。虽然不知道这项研究是否会商业化，但我们认为这是又一种有意思的晶圆搬运技术。晶圆薄到发软，下压键合时可能封住空气，影响良率。东京电子展示了一种避免这一问题的方法。这是研究，并非他们现役键合设备所用的工艺。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/59847526-f9f2-4308-b7d0-1dc57b5f0f94_1024x592.png)

# **索尼领先的 1 微米间距混合键合**

索尼继续证明自己为何是混合键合的领导者。他们于 2017 年率先将该技术用于大批量产品。目前他们每年出货数百万颗采用 6.3 微米间距混合键合、3 裸片堆叠的 CMOS 图像传感器，而其他公司的间距密度远低于此、出货量也更小。索尼的出货量全部采用晶圆-晶圆混合键合。今年索尼发表了 1 微米间距面对面（face-to-face）混合键合与 1.4 微米面对背（face-to-back）混合键合。索尼目前同时使用面对面与面对背两种混合键合。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/7d23785d-e96c-48f0-a1db-d65c31f35552_842x1024.png)

简单解释一下索尼为何如此激进地押注混合键合：索尼希望继续拆分并堆叠图像传感器像素的各项功能，以捕获更多光线，并尽可能多地获取这些数据、将其转化为真正的照片和视频。

他们展示的技术相当有意思。所有混合键合工艺都要求极其平整的表面，但在 CMP（化学机械抛光）过程中，铜和 SiO2 的抛蚀速率不同。对大多数工艺而言，这意味着铜会被磨得比 SiO2 更低，这就是常说的凹陷（dishing）。这一过程必须精确控制，因为 SiO2 与铜的热膨胀系数也有所不同。台积电采用的一种技巧是使用铜合金代替纯铜，以控制凹陷程度、让 CMP 工艺更容易做。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2108d4a1-12d3-4879-b7ec-1bd179f2c683_771x1024.png)

随着索尼把间距缩小到远小于业内其他玩家的水平，他们拿出了相反的策略：在其先进方案中，SiO2 被抛得比铜更低。这需要一套完全不同的专有 CMP 工艺。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c793cb56-dbdc-48c2-93ec-35b5a3658cf8_1024x729.png)

索尼还通过调整 ECD（电化学沉积）工艺中的晶粒尺寸，实现了对铜的类似控制与凸出。通过我们的消息源，我们可以在仅限订阅者的章节独家披露他们在此工艺中使用了谁家的设备。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1ea398b2-5c82-4fdc-bad1-9e7f3cbd4b79_1024x717.png)

其结果令人难以置信。相比常规工艺，接触电阻改善了多个数量级。这是在 200,000 个菊花链 Cu-Cu 连接上测得的。以上是 1 微米面对面键合的结果，1.4 微米面对背键合同样给出了亮眼的数据。

# **AMD Zen 3 上的 V-Cache SoIC 混合键合**

AMD 重申了很多内容，但也有不少新东西。另外，这里要宣传一下我们的 Twitter：我们注意到[AMD 负责 V-Cache 混合键合与抬升扇出桥（elevated fan out bridge）的首席工程师已离开 AMD 跳槽微软](https://twitter.com/dylan522p/status/1534355166656331776?s=20&t=1GOKy6AESdJp7gUTNRSGcQ)。我们对微软自研芯片的前景感到兴奋，他们正从全行业大量招揽人才。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ee96e2b0-b6cd-443f-8f93-8abc7cda2686_1794x1821.png)

V-Cache 的物理结构相当有意思。并非只是 CPU CCD 小芯片上加 SRAM 小芯片和支撑小芯片，AMD 与台积电还在整个组件的最上面加了第五块支撑硅片。这一结构已由 IBM 的 [Tom Wassick](https://www.linkedin.com/in/tom-wassick-95992220/) 独立确认。乍看似乎浪费了额外的硅，但这样做是因为台积电的混合键合工艺要求减薄裸片。这最后一块支撑硅的作用是赋予最终裸片组件足够的刚性，并使其高度与不带混合键合 SRAM 的标准 CCD 相当。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8a6bca0c-1e79-4a81-8648-80649c5f3554_1024x468.png)

AMD 将 9 微米间距混合键合与 36 微米间距微凸点（micro bump）3D 架构作了对比。AMD 指的是将用于 Ponte Vecchio GPU 和 Meteor Lake CPU 的 Foveros。AMD 宣称互连能效高 3 倍、互连密度高 16 倍，并且由于 TSV 与接触电容/电感更低，信号/供电完整性更好。奇怪的是，他们用 9 微米间距作为对比基准。这个对比有点不老实，因为 [TechInsights](https://www.linkedin.com/posts/yuzo-fukuzaki-12408111_3dv-ryzen-amd-activity-6828725467298828288-X9U-/) 发现量产版 V-Cache 实际采用的是 17 微米间距。间距放宽会削弱其所展示的部分优势。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/81b19c6a-8ff7-4234-b585-44042d1c16df_1024x635.png)

这张图很有意思，尽管非常笼统。Zen 3 有 32MB L3 缓存，V-Cache 为每个小芯片再增加 64MB。目前只有 1 个小芯片被堆叠，因此 IPC 提升的范围很宽。我很好奇 AMD 用了什么仿真和基准测试得出这个 IPC 提升百分比。AMD 还展示了一些可靠性相关数据，表明在正常电压下没有任何顾虑。

# **联发科网络 SoC 的可靠性**

联发科发表了一篇题为《面向高性能计算应用的高密度扇出封装可靠性挑战》（Reliability Challenges of High-Density Fan-out Packaging for High-Performance Computing Applications）的论文。论文没说出口的是，这是一颗真实的芯片，联发科正通过其定制 ASIC 部门面向中国市场的网络应用销售。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/aa808104-6ef8-4e0f-9d7b-451e409ee81c_941x1024.png)

联发科同样没有直接说明，但我们知道他们用的是台积电的 InFO-oS 技术。论文讨论了温度、翘曲及其他可靠性问题，但有意思的是他们把这颗芯片公开了出来。

在仅限订阅者的章节中，我们将谈及思科在共封装光学上与谁合作、索尼混合键合工艺的部分环节用了谁家的设备，以及关于那颗将采用 CoWoS-R 的 AMD 芯片的讨论。

[分享](https://newsletter.semianalysis.com/p/packaging-developments-from-ectc?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[立即订阅](https://newsletter.semianalysis.com/subscribe?)
