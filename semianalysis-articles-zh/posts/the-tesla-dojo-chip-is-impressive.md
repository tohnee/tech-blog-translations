---
title: "特斯拉 Dojo 芯片令人印象深刻，但存在一些重大技术问题"
title_en: "The Tesla Dojo Chip Is Impressive, But There Are Some Major Technical Issues"
date: 2021-08-25
source: https://newsletter.semianalysis.com/p/the-tesla-dojo-chip-is-impressive
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 特斯拉 Dojo 芯片令人印象深刻，但存在一些重大技术问题

> 原文：[The Tesla Dojo Chip Is Impressive, But There Are Some Major Technical Issues](https://newsletter.semianalysis.com/p/the-tesla-dojo-chip-is-impressive) · SemiAnalysis

上周特斯拉发布了 Tesla D1 Dojo 芯片。[其规格令人垂涎，我们在此做了分析](https://semianalysis.substack.com/p/tesla-dojo-unique-packaging-and-chip)，简而言之：其独特的晶圆级系统封装与芯片设计选择，有望在数万亿参数大规模网络的训练上，相对竞争 AI 硬件取得一个数量级的优势。与历次发布一样，特斯拉的规格表非常亮眼，但其中隐藏着限制条件和巨大的问号。SemiAnalysis 将深入剖析这些问题。我们还将独家详述特斯拉为设计这颗芯片与一家现有半导体公司达成的合作。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/dafada19-d11a-4340-9c94-0232a8a7da39_1024x545.png)

在功能单元级和系统级上，特斯拉的内存都不够用。单个功能单元拥有 1.25MB SRAM 和 1TFlop 的 FP16/CFP8 算力。相对于他们想达到的性能水平，这实在是捉襟见肘。对于数万亿参数的巨型模型来说，这个配比严重失衡。在芯片级，同样的比例问题依然存在，因为裸片上没有其他 SRAM 结构。每颗芯片的 mesh 网络中有 354 个单元，每单元仅 1.25MB。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a0392ed1-f53c-457d-804e-2f0929fd759b_1024x509.png)

虽然芯片与 tile 之间的带宽惊人，但即便资源零冗余的完整 ExaPod，在超过 1 EFLOP（FP16）的算力下总内存也只有 1.33TB。这解释了特斯拉为何创造 CFP8 数据类型：它与 FP16 速率相同，但占用面积更小，能让他们把片上那一点可怜的内存再撑一撑。Graphcore 也在片上 SRAM 上栽过同样的跟头——就是不够用。尽管其每颗裸片的 SRAM 是特斯拉的 2 倍多，[片上内存的不足已导致其相对英伟达的性能与 TCO 表现非常糟糕](https://semianalysis.com/graphcore-looks-like-a-complete-failure-in-machine-learning-training-performance/)。

特斯拉最吸引人的卖点之一是芯片间互连极为强大。其带宽比竞争 ASIC 和英伟达高出一个数量级。特斯拉的做法是在裸片的每一条边都塞满 112G SerDes。这些 IP 完全来自特斯拉与第三方供应商的合作授权。总计 576 条 SerDes，实现了令人瞠目的 8TB/s IO。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/22804a68-524d-4399-a1b9-8acb6035e87b_1024x545.png)

要把这么大的 IO 引出芯片，特斯拉只能依赖非常特殊的封装。他们的芯片封装贵得离谱，但这是从如此小的封装里引出 8TB/s IO 的唯一办法。桌面或服务器 CPU 常规的 LGA 式封装，引脚数量连零头都远远不够。

此外，若用这种粗糙的封装吞吐 8TB/s，功耗会直接爆炸。台积电的 CoWoS 有 3 倍光罩极限，InFO 有 2 倍光罩极限。这意味着特斯拉一次只能封装寥寥几颗芯片。他们唯一的选择是晶圆级封装。具体来说，他们采用的是台积电的集成扇出晶圆级系统（InFO_SoW）。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ea086032-65dd-4da3-bbb5-ecb0b475de25_1024x550.png)

这就是特斯拉目前的进度。他们实验室里有一颗运行在 2GHz 的、极其昂贵的单 tile。他们还没有完整系统。完整系统计划在 2022 年某个时间点就绪。想想特斯拉在 Model 3、Model Y、Cybertruck、Semi、Roadster 和完全自动驾驶（FSD）上的时间表，我们应该默认这里的时间也要再放宽。

两座最困难的技术大山甚至还没有翻越：tile 间互连和软件。每个 tile 的外部带宽都超过最高端的网络交换机。为实现这一点，特斯拉开发了定制互连。所谓「特斯拉开发」，其实是他们在互连领域拥有深厚积累的合作伙伴。这些是为 tile 间互连专门定制的互连。相比标准以太网，这种实现的成本极其高昂。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ae54c677-8c19-4132-9dbd-70d53d09bfc2_1024x806.png)

房间里另一头大象是软件。特斯拉甚至没有声称自己有办法把微型张量（mini-tensor）的运算自动布局布线到整个架构上。他们确实声称其编译器能处理细粒度并行和数据模型并行。但这一句含糊带过不足以让我们信服。太多公司手握 AI 硬件，成群的工程师在已存在数年的芯片上做软件，连这个问题的皮都没蹭破。就算他们声称做到了，「一个神奇的编译器」这种事也值得怀疑。[在问答环节被问到软件栈的问题时，他们明显准备不足，甚至亲口承认尚未解决软件问题。](https://youtu.be/j0z4FweCy4M?&t=2h14m07s)

最有可能的情况是，特斯拉的研究人员需要手工完成这一过程的部分环节。此外，研究人员必须显式地针对 SRAM 做优化，否则就有跑飞的风险。这些约束迫使他们的开发者为一个本应解除海量模型扩展枷锁的系统，反复调参、重度优化模型。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/995dba7f-c668-410c-9088-1c91c599ad56_1023x439.png)

半导体专业人士问得最多的一个问题是：「这东西在经济上到底怎么成立？」特斯拉描述的是一套非常特定、出货量并不大的硬件。目前承诺部署的 645mm^2 7nm 裸片总共只有 3,000 颗。与之相伴的是极其特殊的封装，以及专为 ExaPod 超级计算机开发的定制互连。这样的量远远不够摊薄研发这样一颗芯片的巨额成本。即便 tile 间互连和 112G SerDes 的研发并非特斯拉亲自完成，这个结论也依然成立。

对经济可行性的担忧其实不是问题。这台超算的用途非常明确：训练自动驾驶 AI。最终目标和目标市场价值以万亿美元计。特斯拉的全部估值都建立在「比特任何人更早实现 Robotaxi」的预期之上。如果他们能在全球数百万辆车上创建并部署自动驾驶 AI，那么万亿美元估值就名副其实。

为了这个目标，如果这套芯片和超算系统设计能让特斯拉哪怕提早 6 个月达成目标，那么每一分钱的花费都值回十倍票价。很多人会争论他们能否第一个到达。这个领域里几十亿美元正源源涌入，Mobileye、Google 旗下 Waymo、英伟达及其伙伴、GM Cruise、Motional 等强劲对手林立。在这些竞争者中，只有 Google 和英伟达拥有能与特斯拉比肩的超算。虽然这主要是个软件问题，但充裕的计算资源能帮助研究者用更复杂的神经网络更快迭代。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/bc9ec567-50d3-4bca-b99c-407762b8be13_1400x788.jpeg)

尽管没有巨型超算，Mobileye 的纽约项目仍被广泛视为最令人印象深刻的自动驾驶公开演示。Google 旗下 Waymo 依据监管数据显示的每英里接管次数最少。我们认为，特斯拉为赢得 Robotaxi 竞赛、追平这两家而尽可能砸钱是合理的。他们可以轻松通过廉价债务或进一步增发股票融到更多资金。在任何「他们不是第一个建成大规模 Robotaxi 网络」的世界里，特斯拉的估值都被严重高估。为此，他们必须执行这一战略乃至更多。

马斯克表示，最终他们可以用这颗芯片/计算机开展 SaaS 业务。虽然我们不知道这是否会成功，但把这些 E1 计算机扩展到相当规模、配上那种商业模式，将会是一记重锤。

成本、定制互连、内存限制、软件缺失，以及这颗芯片要到 2022 年甚至更晚这一事实，都是我们必须铭记于心的。这颗芯片并不是特斯拉仅凭一己之力设计出超越所有人的产物。我们无权披露其合作伙伴的名称，但眼光敏锐的读者在我们提到「外购 SerDes 与互连 IP」时，就会确切知道我们在说谁。特斯拉的芯片与系统设计确实令人印象深刻，但不应该被吹上天。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

[分享](https://semianalysis.substack.com/p/tesla-ai-day-supercomputer-chip-teaser?utm_source=substack&utm_medium=email&utm_content=share&action=share&token=eyJ1c2VyX2lkIjoyMTc4MzMwMiwicG9zdF9pZCI6Mzk2MDc4NTgsImlhdCI6MTYyOTQ0NDMwOSwiaXNzIjoicHViLTMyOTI0MSIsInN1YiI6InBvc3QtcmVhY3Rpb24ifQ.ZGWDr02AG9si-HQAWkwHpmun8ugcaY7OR_nQ6wJtV4M)

[发表评论](https://semianalysis.substack.com/p/tesla-ai-day-supercomputer-chip-teaser/comments)

*本文最初于 2021 年 8 月 25 日发布于 [SemiAnalysis](https://semianalysis.com/the-tesla-dojo-chip-is-impressive-but-there-are-some-major-technical-issues/)。*

*SemiAnalysis 的客户及员工可能持有本文所提及公司的仓位。*
