---
title: "Lynceus：可降低检测与量测资本开支的在线实时 AI 过程控制监控"
title_en: "Lynceus: Inline, Real-time, AI Based Process Control Monitoring That Can Reduce Inspection & Metrology Capex"
subtitle: "在大产量晶圆厂中得到验证：以更高良率降低检测与量测开支"
date: 2022-07-28
source: https://newsletter.semianalysis.com/p/lynceus-inline-real-time-ai-based
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# Lynceus：可降低检测与量测资本开支的在线实时 AI 过程控制监控

> 原文：[Lynceus: Inline, Real-time, AI Based Process Control Monitoring That Can Reduce Inspection & Metrology Capex](https://newsletter.semianalysis.com/p/lynceus-inline-real-time-ai-based) · SemiAnalysis

**在大产量晶圆厂中得到验证：以更高良率降低检测与量测开支**

Lynceus 是半导体行业中最有意思的初创公司之一。他们不专注于制造或设计芯片，而是专注于运行在晶圆厂里的软件。在深入探讨他们的解决方案之前，我们先提供一些背景。大多数晶圆厂在其各个厂区使用各类自研和外部软件。像 PDF Solutions 这样的厂商可能提供把一切串联起来的数据库与工艺解决方案，各家设备厂商会为自己的设备提供软件，而来自 KLA、Onto、Nova Measuring Instruments 等领先检测与量测厂商的软件则帮助识别缺陷。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/db84ebf0-2443-4d9a-a43a-1f066ba1408c_1346x711.png)

说到底，大多数软件的使用很大程度上要靠晶圆厂自己摸索。大多数晶圆厂都有非常定制化的流程，用来决定哪些数据重要、如何根据这些数据采取行动，以及如何持续微调工艺。英特尔曾表示，他们每生产一片晶圆就会产生 TB 级的数据，但用传统方法存储或分析全部数据几乎是不可能的。尽管数据量巨大，晶圆厂仍必须能够快速判断缺陷出现在哪里、原因是什么、以及如何缓解。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/7ed1685c-071a-4754-85fb-90300c6e9674_1441x825.png)

数据必须被持续监控和分析，以判断某台设备是否超出规格（out of spec）。任何问题都必须被迅速捕捉，否则几十片、几百片甚至几千片晶圆就会报废。例如 2019 年，[台积电（TSMC）因一个未查明的问题损失了超过 5.5 亿美元的在制品晶圆](https://www.anandtech.com/show/13975/tsmcs-fab-14b-photoresist-material-incident-550-million-in-lost-revenue)——该问题仅在 1 座晶圆厂内持续了不到 1 个季度。与此同时，对晶圆所做的每一次检测或测试，都意味着占用了洁净室面积、生产周期和成本，却并没有推进芯片的实际制造。「量两次、裁一次」这句老话固然好，但若在半导体制造中照此执行，在经济上完全不可行。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/725c19fa-1132-4d59-82a6-57f8d4bd3ff9_780x434.png)

随着行业不断提升复杂度，市场期望良率仍能保持在优秀水平。这是一个极其困难的问题，因为每一代制程节点都会增加约 35% 以上的工艺复杂度。当先进制程的工序数以千计时，误差会迅速累积。工业企业喜欢大谈「六西格玛」（Six Sigma），但对半导体制造而言这还不够。假设一个有 2,000 道工序的工艺流程，即使每道工序在每平方厘米缺陷数维度上都达到 6 个西格玛，最终 D0（行业术语，指每平方厘米缺陷率）仍会达到 0.678。对于不熟悉的人来说：即便裸片面积只有智能手机芯片那样的小尺寸，你的产品也会有一半以上是缺陷品。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/5353212e-0032-46fa-95d9-f1427fb79f2c_1537x827.png)

任何大型晶圆厂都至少会有 1 台设备处于停机维护状态。某台刻蚀或沉积腔体的一个阀门或其他参数只是略微偏离规格：它可能运行得过热或过冷，可能工作在错误的压强下，某种前驱体化学品的流速也可能超出规格。更常见的情况是，这些问题比读取一个简单传感器所显示的更隐蔽、更难诊断。工厂产出的数据量如此之大，以至于也不可能对所有数据都进行分析。成本、产能、良率、制造周期和产品质量之间始终存在取舍。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a9cc5645-39cf-4029-a561-e60ad4207486_1536x826.png)

这正是 Lynceus 的切入点。他们利用晶圆制造设备产生的数据、晶圆厂在大产量产线上已有的数据，构建实时过程控制。所有数据会被馈送到多个 AI 模型中，帮助工艺工程师和良率工程师发现问题。更快速的根因分析能够把晶圆厂工程师的精力引导到关键问题上，而不是在无关紧要的问题上浪费时间，从而提升工程师效率。另一大优势在于，他们可以开始减少检测与量测的频次，优化分配给这类不直接推进晶圆制造的设备的资本开支和洁净室面积。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/cba27da6-ec46-4e10-980d-bca3352fd6c9_1532x826.png)

Lynceus 完全与工艺无关（process-agnostic），而且他们已经进入了产生收入的晶圆厂。设备维护数据、测试结果数据和 FDC（设备故障检测与分类）数据都可用于训练模型。模型还可以针对特定工艺甚至特定芯片设计做进一步调优。当数据从刻蚀、沉积或其他工艺腔体中产出时，系统会发出预测和诊断。模型在不断被验证和改进。

他们的软件和模型既可以运行在云端，也可以部署在本地，取决于晶圆厂的安全要求。它能够直接接入晶圆厂现有的定制化流程，并把数据所有权留在该晶圆厂手中。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a741aabd-cea1-4f49-a234-72ae76810622_780x435.png)

这些模型通常按单个工艺步骤或工艺模块划分。目前它们已在 2 座大产量晶圆厂中的部分工序上投入生产运行。结果令人震惊：缺陷检测时间从 4 天缩短到 3 小时，减少了 90%。此外，他们还将量测与检测的抽样频率降低了 4 倍。这对良率、成本和周期时间都是巨大的提升。

Lynceus 的制造质量预测软件旨在预测产线上每件产品质量测试的结果。该公司的软件利用 AI 技术实时计算产品通过质量测试的概率，为制造商提供实时质量预测，使客户能够在缺陷真正发生之前调整工艺。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/0ab8b7d0-f27e-4e7b-bc63-24c3d9666f8e_1537x827.png)

Lynceus 可以帮助晶圆厂从每片晶圆上获得更多合格裸片，降低销售成本（CoGS），实现更高的毛利率。虽然英特尔和台积电等一些规模更大的先进晶圆厂正在做类似的工作，但仅限内部使用，大多数晶圆厂尚未部署像 Lynceus 这样精密的模型。他们最初主要瞄准涉足汽车行业的晶圆厂作为切入市场，因为其中有大量的法规、测试和质量验证指标要求。一旦在此领域得到验证，他们就能进一步拓展到更多市场。

*顺便一提，我们很享受与 Lynceus 的 CEO 兼联合创始人 David Meyer 以及 Lynceus 团队其他成员的合作，看他们展翅高飞、进入越来越多的晶圆厂。*

[分享](https://newsletter.semianalysis.com/p/lynceus-inline-real-time-ai-based?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[发表评论](https://newsletter.semianalysis.com/p/lynceus-inline-real-time-ai-based/comments)
