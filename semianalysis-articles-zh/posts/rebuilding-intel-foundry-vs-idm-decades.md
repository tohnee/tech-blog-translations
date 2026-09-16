---
title: "重建 Intel——代工与 IDM 之争：数十年低效逐一拆解"
title_en: "Rebuilding Intel – Foundry vs IDM Decades of Inefficiencies Unraveled"
subtitle: "代工成本、加急批（Hot Lots）、步进（Steppings）、设备稼动率、测试等：通往运营效率之路？"
date: 2023-06-22
source: https://newsletter.semianalysis.com/p/rebuilding-intel-foundry-vs-idm-decades
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 重建 Intel——代工与 IDM 之争：数十年低效逐一拆解

> 原文：[Rebuilding Intel – Foundry vs IDM Decades of Inefficiencies Unraveled](https://newsletter.semianalysis.com/p/rebuilding-intel-foundry-vs-idm-decades) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**代工成本、加急批（Hot Lots）、步进（Steppings）、设备稼动率、测试等：通往运营效率之路？**

Intel 在半导体行业中占据独特地位，是唯一一家大型 IDM（垂直整合制造商），即在一家公司内部同时设计和制造自己的先进芯片。三星（Samsung）虽然兼具两项职能，但其 LSI（设计）与代工之间实际上隔着一道防火墙。Intel 作为 IDM 的独特地位既是重大的结构性优势，也是劣势。今天我们想从技术和成本角度剖析 Intel 的低效之处。除了 Intel 自己的说法，我们还将分享对 Intel 技术、成本建模和毛利率的独立观点。

理论上，Intel 可以让制造与设计彼此更紧密地协同优化，比 AMD 与台积电（TSMC）这样的组合更甚，因为它是单一公司，数据共享限制更少。他们可以把最终芯片定价压得比 AMD 更低，因为不用向台积电这样的外部代工厂支付「代工税」。

![](https://substack-post-media.s3.amazonaws.com/public/images/0583331a-48ef-4dc0-ac08-96e80ca3cb90_1492x766.png)

几十年来，这一模式行之有效。Intel 的制程节点领先所有竞争对手巨大距离，因而得以称霸。它的毛利率长期高于台积电和 AMD 等公司。下图展示了假设一家代工厂 + 无厂设计公司合并为同一家公司时，与 Intel 相比的形态。

![](https://substack-post-media.s3.amazonaws.com/public/images/49bdbe62-bd7e-41b7-a38c-8aece2b24361_1363x730.png)

2010 年代初，其制程节点优势在 14nm 上开始出现裂缝，随后在原定 2016 年的 10nm 转型上彻底崩塌。代工厂们一路狂奔，先后拿下 16nm、10nm 和 7nm，把 Intel 的 3 年领先变成了 3 年落后。

其中一些裂缝正是拜其庞大的 IDM 体制所赐。职责与问责没有被恰当地落实到各个团队和业务部门。Intel 的部分部门日渐萎缩，在性能或成本上落后于行业，但没有人能看出来，因为 Intel 还沉浸在自己工程实力碾压一切的自嗨幻境里。

![](https://substack-post-media.s3.amazonaws.com/public/images/70575cf4-384f-4701-8f0a-b1a745c3b1c3_1480x742.png)

一旦失去领先，低效便暴露无遗。如今，Intel 制造晶圆的效率显著低于台积电。由于设备稼动率更低、良率更差，Intel 需要更多厂房面积才能达到同样的产出。

与此同时，Intel 的设计团队明显落后于 AMD，需要更大的核心、更多晶体管、更高功耗才能达到相近性能。此外，[由于设计方法学较差](https://www.semianalysis.com/p/the-dark-side-of-the-semiconductor)，Intel 的设计团队要让新架构量产需要多花好几年和更高的成本。

![](https://substack-post-media.s3.amazonaws.com/public/images/c55be01d-0218-4337-aff1-5bfc085ece37_1633x870.png)

Intel 解决这些问题的办法之一是在制程节点上追赶：接连两次快速微缩（Intel 4/3 和 Intel 20A/18A）。但仅凭这一点解决不了问题，他们仍然缺乏规模、客户基础和运营效率。

Intel 目前正着手解决其中许多问题，并向对外部各类客户开放的外部代工厂转型。表面上看，只有赢得外部客户才有意义，但其实还有别的好处。

通过转向内部代工厂模式，Intel 可以开始终结那种把成本分摊到整个业务部门、而不是核算到具体设计和团队头上的荒唐做法。这将把问责下沉到更底层，帮助在产品和晶圆厂层面管理成本，从而解决他们的一些重大低效问题。

# **当前的低效**

这些问题千头万绪，共同造就了我们今天看到的 Intel。总体而言，Intel 的产品团队过去可以躲藏在自家制造实力的背后，对分摊到整个业务部门的成本毫不在意。

## **加急批（Hot Lots）**

在半导体制造中，晶圆按批次（lot）生产。一个批次是一组晶圆，在某台设备上依次加工后，再转到下一台可用设备继续加工。由于一座晶圆厂耗资数百亿美元，厂内设备必须最大化利用。一般来说，由于晶圆按批次编组，一片先进制程晶圆的加工可能需要 10 周。

另一方面，如果完全不计成本，一片先进制程晶圆也可以在几周内加工完，但这会带来巨大的低效——设备要不断空等这批晶圆，好让它尽可能快地被加工。这就是所谓的「加急批」（hot lot），指被给予优先权、比标准批次更快加工的一批晶圆。

> 他们想开多少加急批就开多少，想做多少样品就做多少。
>
> David Zinsner，Intel CFO

原因可能多种多样，比如加快新工艺步骤或新设备的验证，或者为新设计、新技术制造测试芯片。这个说法源于这些晶圆被以最快速度推过制造流程，因而「发烫」。

> 我们确实用了大量加急批。而通常，作为总经理，我对加急批成本的思考并没有达到应有的程度——这不仅是成本问题，还关乎对工厂稼动率和效率的干扰。
>
> Sandra Rivera，Intel 数据中心与 AI 事业部执行副总裁兼总经理

然而，运行加急批确实会降低设备稼动率和整厂效率。因此，这是让特定晶圆尽快加工的紧迫性，与制造工厂整体效率和产出之间的权衡。

> 我们的基准测试表明，我们加急物料的频率大约是同行的 2 到 3 倍，估计使总产出损失 8% 到 10%。
>
> Jason Grebe，Intel 公司规划事业部副总裁兼总经理

Intel 正在通过转向内部代工厂模式来解决这一问题：像其他代工厂向客户收取加急批费用一样，向各业务部门收取加急批费用。

Intel 认为，仅这一项改变每年就能节省 $500M 到 $1B。

## **步进与样品（Steppings & Samples）**

设计一颗芯片的成本高得惊人。一旦设计完成，要将其投产，需要把设计发给晶圆厂，把设计转换成数十块实体光罩放入光刻设备，并让测试芯片经过数千道工艺步骤。拿到测试芯片后，可以检查缺陷/问题，然后微调设计。

我们曾[在此详细讨论过整个行业的设计成本问题](https://www.semianalysis.com/p/the-dark-side-of-the-semiconductor)，而 Intel 目前处于重大劣势的领域之一，就是他们要做更多次这样的迭代。步进（stepping）是指修改后的设计被送往晶圆厂、为新测试芯片制作新光罩的过程。

> 他们想做多少次步进就做多少次。
>
> David Zinsner，Intel CFO

Intel 花了 12 个步进才把 Sapphire Rapids 推向市场，而 AMD 的竞争芯片（如 [Bergamo](https://www.semianalysis.com/p/zen-4c-amds-response-to-hyperscale) 和 Genoa）通常只需 2 到 3 个步进。这使得 Intel 要制造所有这些额外的光罩，成本大幅增加，将新设计推向市场的时间也被大幅拉长。

我们甚至从前员工那里听到传闻：曾有一段时间，Intel 的一些设计团队宁愿把设计送到晶圆厂、拿回加急批样品来测 bug，也不愿完成更多的仿真和验证。

Intel 计划通过向设计和产品业务部门按公平价格收取这些操作的费用（而不是随心所欲地想步进多少次就多少次），来减少样品和步进的数量。设计团队几年前已开始转向更行业标准的设计方法学，尽管这项任务异常艰巨。

Intel 认为，这项改变每年可为其节省 $500M 到 $1B。

## **测试、分选、分档（Test, Sort, Bin）**

芯片制造完成后，要经过测试，按失效和不同档位（bin）分选，进入不同产品。Intel 多年来一直是测试、分选和分档的先驱。他们的设备高度定制，拥有许多独有的内部测试向量。虽然这给 Intel 带来了一些优于行业的优势，但并非全是好事。

> 与同行相比，我们的测试时间不断增长。目前我们估计，我们的测试时间是竞争对手的 2 到 3 倍。实际上，是我们成本更低的测试平台在补贴测试时间的增长。
>
> Jason Grebe，Intel 公司规划事业部副总裁兼总经理

Intel 过去这项强大的制造能力优势，再次变成了劣势。鉴于最终芯片的现场可靠性并没有真正的差别，测试时间没理由达到 AMD 等竞争对手的 2 到 3 倍。

Intel 认为，让各业务部门更直接地为测试、分选和分档付费，会促使他们在设计中更谨慎地选择测试策略，每年可节省约 $500M。

此外，Intel 先进的分档策略造就了一种我们喜欢称为「SKU 轰炸」（SKU Spam）的产品策略。在 PC 和数据中心领域，Intel 拥有几十上百个 SKU，因为他们能把芯片分选到如此多的档位，形成面向最终市场的芯片。相比之下，AMD、Broadcom 和 Nvidia 的产品线要精简得多。减少 SKU 数量显然有节省成本的潜力，但我们尚未听说 Intel 有任何改变这一做法的计划。

## **设计与爬坡**

产品经理和设计团队过去惯于借 Intel 的制造实力来掩盖其架构低效。在内部代工厂模式下，情况改变了：[裸片尺寸臃肿的产品](https://www.semianalysis.com/p/intel-emerald-rapids-backtracks-on)（如 Sapphire Rapids）的成本将立即冲击该团队的成本结构，而不是被制造部门吞掉。因此，这些变化将促使团队重新重视架构、裸片面积及由此带来的成本。

Intel 认为这每年可节省超过 $1B，因为团队能更容易地识别哪些功能值得花裸片面积、哪些不值得。目前，[Intel 的 Sapphire Rapids 把大量面积花在了大多数客户根本不用的功能上](https://www.semianalysis.com/p/intel-emerald-rapids-backtracks-on)。

Intel 设计团队还往往[忽视内部制造中的光罩难题和光刻设备产出问题](https://www.semianalysis.com/p/die-size-and-reticle-conundrum-cost)，而这些台积电都是要向客户收费的。更深入的解释请[看这里](https://www.semianalysis.com/p/die-size-and-reticle-conundrum-cost)。

Intel 没有说明是否会对内部代工厂客户就此收费。

Intel 还把爬坡速度作为成本扩张的核心抓手。台积电最大的强项在于其 7nm 和 5nm 的大规模爬坡曾在 6 个月内从每月 0 片晶圆拉到每月 50,000 片。这使良率爬坡学习更早兑现，并在节点余下的生命周期内持续受益，同时也提高了设备稼动率。应当指出，[由于种种磕绊](https://www.semianalysis.com/p/tsmcs-3nm-conundrum-does-it-even)和[成本问题、导致 Apple 转向拆分 SoC 的方法学](https://www.semianalysis.com/p/as-moores-law-slows-apple-is-forced)，[台积电 3nm 的爬坡要逊色得多](https://www.semianalysis.com/p/tsmcs-heroic-assumption-low-utilization)。

Intel 若想追赶，就必须大幅加快爬坡速度。Ice Lake 和 Sapphire Rapids 的爬坡慢得惊人，导致资本利用率低下、良率学习缓慢。Intel 现在将向内部团队收取跨节点生命周期的统一晶圆价格，以加速新产品的爬坡速度——据 Intel 称，这既可每年节省 $1B，也能加快有竞争力的新产品上市速度。

与台积电类似，Intel 也将开始按稼动率向团队收费，并要求更早锁定订单。他们对内部客户的晶圆订单也将变得不那么灵活。

> 他们只要愿意，几乎每周都能改预测。
>
> David Zinsner，Intel CFO

这一变化有助于更好地规划生产、提高设备稼动率，也将带来可观的节省。

![](https://substack-post-media.s3.amazonaws.com/public/images/8dbeaf6f-a5a6-41eb-a624-f1e74db9e62e_1473x751.png)

总体而言，Intel 声称内部代工厂模式的各种改变将带来大量成本节省。

现在让我们深入我们对 Intel 成本的分析，以及对其技术竞争力的展望。2024 年正注定成为艰难的一年，但他们转危为安了吗？
