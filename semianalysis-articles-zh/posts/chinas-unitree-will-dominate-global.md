---
title: "宇树科技不可思议的成长轨迹仍被忽视"
title_en: "Unitree's Impossible Trajectory Is Still Overlooked"
subtitle: "下一代机器人中最快的迭代周期理应迎来前所未有的加速"
date: 2026-06-08
source: https://newsletter.semianalysis.com/p/chinas-unitree-will-dominate-global
crawled: 2026-09-15
authors: ["Reyk Knuhtsen", "Niko Ciminelli", "Jacob Rintamaki", "Robert Ghilduta", "Joe Ryu", "Jeremie Eliahou Ontiveros", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 宇树科技不可思议的成长轨迹仍被忽视

> 原文：[Unitree's Impossible Trajectory Is Still Overlooked](https://newsletter.semianalysis.com/p/chinas-unitree-will-dominate-global) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**下一代机器人中最快的迭代周期理应迎来前所未有的加速**

我们正在见证又一家中国硬件巨头的诞生。三年前，宇树（Unitree）还是一家四足机器人公司。到去年，他们已将四足领域的主导地位转化为创建并领跑人形机器人市场。今年，他们的 G1 人形机器人终于开始进入可行的部署，还有三款新设计在路上，包括他们最直接的[西方人形机器人竞品](https://www.unitree.com/H2)。

特斯拉（Tesla）于 **2022** 年首次展示了人形机器人。虽然它和其他西方玩家如今量产的早期人形机器人仍是半成品，**但我们听说宇树可能在接下来几周内出货第 10,000 台。**

如今，宇树的营收同比增至三倍，产品线毛利率达 60%，计划投入近 $300M 的 AI 研发开支，并将越来越多的制造环节收归自产，同时把人形机器人定价在迄今市场上最便宜的水平。随着备受期待的 [IPO](https://static.sse.com.cn/stock/disclosure/announcement/c/202603/002178_20260320_QY8F.pdf) 临近，宇树成为人形机器人话题的焦点实至名归。但一直以来，宇树的人形机器人背着[可靠性欠佳](https://www.youtube.com/shorts/ZKHiooTF0Eg)的名声，被认为除了[娱乐](https://www.youtube.com/watch?v=Ykiuz1ZdGBc)和[研发](https://www.prnewswire.com/news-releases/nvidia-gtc-conferenceunitree-h1-humanoid-robot-embraces-ai-with-the-world-302096830.html)之外别无用处，还有“廉价”的口碑。

尽管如此，我们认为宇树的**成本结构**是其相对于竞争对手的最大优势之一。过去 12-18 个月里，宇树把税前定价从 **$50K 以上砍到了 $27.3K**。即便在这个价位，我们估计其旗舰产品 G1 仍有 **67% 的毛利率**。随着制造规模扩大、BoM 注定大幅下降，**我们已听说某些订单的价格远低于 $20K**。

![](https://substack-post-media.s3.amazonaws.com/public/images/5819a3cc-2fa8-4b48-b000-9855987f126f_4099x3240.jpeg)
*来源：SemiAnalysis 估算*

我们通过全面审查宇树机器人的设计、与每个组件的制造商交谈，并通过多位供应链买卖方逐项核实，得出了这些 BoM。

最后，尽管外界对这家公司有无数不屑一顾的评论，我们认为其 G1 人形机器人正在跨越现实世界部署的可行性门槛。

![](https://substack-post-media.s3.amazonaws.com/public/images/3c88403b-7d23-4f03-9494-663eecc7f7af_4183x2354.heic)
*来源：SemiAnalysis 估算*

然而，还没有人真正理解宇树的策略、成本与制造，也没有人认真对待“这些机器人到底有没有用”的质疑。今天我们就是要在此澄清事实。在我们的研究中，我们呈现了宇树模仿比亚迪（BYD）和大疆（DJI）策略的历史——培育自己的生态、催生新市场、然后吃掉这些市场。就在我们写下这些文字时，这一策略仍在推进之中。新市场已在视野之中，这意味着宇树的爆炸式增长应当会持续。

![](https://substack-post-media.s3.amazonaws.com/public/images/b0210f02-27b9-4976-8b2d-5e645096d08b_1343x889.heic)
*来源：Zoomax*

接下来，我们审视他们具体的硬件策略：他们的 QDD 执行器设计选择如何带来一种潜在的结构性优势，以及他们的执行器如何改进到接近可部署的水准。

最后，我们论证宇树的进步与成本优势正在叩开经济可行性、取代人类劳动力的大门。如今很可能已有超过 250 台宇树机器人部署在劳动场景中，我们会详细拆解这笔部署账是怎么算得过来的。值得注意的是，宇树是靠着小小的爱好者/研究者市场走到今天的。一旦宇树解锁可行部署并达到临界规模，它们可能会以不真实的速度加速。

所有这些都建立在碾压西方成本与交期的规模和制造能力之上，而宇树本身在竞争激烈的中国生态中也是出类拔萃的。在付费墙之后，我们会具体讨论旨在解锁更多任务和市场的新兴机器人灵巧手厂商，以及谁将被吃掉、谁将从宇树供应链中获益。

宇树的 IPO 标志着机器人时刻的诞生。他们正在解锁市场与生态，并推行一种规模战略，可能走上其他中国硬件巨头走过的路。让我们先回溯历史，理解宇树这件事可能如何成就。

# 一家中国硬件巨头的炼成

一家完全成熟的中国硬件巨头在实践中是什么样子？如今的汽车制造商比亚迪（BYD，Build Your Dream）就是宇树策略成熟形态的绝佳范例：掌控 BoM 中最昂贵、最具挑战性的组件，利用这种掌控力复利出无人能及的成本优势，同时在把供应链收归内部的过程中创造新市场、叠加更多价值。

![](https://substack-post-media.s3.amazonaws.com/public/images/17dc6910-2eba-4d77-9c11-926c4f648e4b_742x453.heic)
*来源：BYD*

比亚迪最初专注于电池电芯。电池可占一辆电动汽车 BoM 的约 30-40%（如今占比更低，多亏了比亚迪）。比亚迪成立于 1994 年，生产因毒性而被日本在位厂商放弃的电池电芯。比亚迪花了近十年打磨产品，才于 2011 年进入电动车领域，起初只是个小众玩家。当比亚迪于 2011 年 10 月向[中国市场](https://web.archive.org/web/20111101200501/http://www.bydenergy.com/bydenergy/energy/News%20Center/News/78.html)推出其首款纯电动车 e6 时，全中国一年的电动车销量只有 8,159 辆，仅占[新车销量的 0.04%](https://en.wikipedia.org/wiki/Plug-in_electric_vehicles_in_China)。当时根本没有电动车市场——是比亚迪帮忙造出来的。

**比亚迪的策略是关键。**

**以不断增长的汽车产量掌控电芯，需求向下传导，催生出更成熟的供应与生态**——[湖南裕能（Hunan Yuneng）](https://christopherchico.substack.com/p/why-korean-battery-makers-are-converting)和[深圳德方纳米（Shenzhen Dynanonic）](https://christopherchico.substack.com/p/why-korean-battery-makers-are-converting)（LFP 正极）、[汇川（Inovance）](https://www.marklines.com/en/top500/inovance-technology)（电机和逆变器）、[三花（Sanhua）](https://www.sanhuaautomotive.com/en)（热管理）等玩家涌现出来，以更低的成本为比亚迪供应下一代改良部件。2010 年，这些公司都还不成气候。

**比亚迪可以自由地把对其有复利效应的制造环节收归内部。**他们把电池电芯、电驱、电机、IGBT 和 SiC 功率模块（全球为数不多运行 IDM 模式的公司之一）、变速箱、底盘和车身外壳，甚至发动机本身都纳入自制。到 2010 年代末，一辆电动车的几乎所有部件都在比亚迪自家的屋檐下制造。

这形成了一个正反馈循环：掌控并改进正确的硬件，让比亚迪能创造出打开新市场的新产品，比如 2020 年的[刀片电池](https://electrek.co/2026/03/05/byds-new-ev-battery-unlocks-1000-km-range-10-min-charging/)。在刀片电池之前，LFP（磷酸铁锂）这种电池化学体系便宜、安全，但能量密度低，适合那些从不远离充电器的车辆，比如[叉车](https://www.emobility-engineering.com/lithium-iron-phosphate-lfp-batteries-ev/)（操作员休息时充电）或每晚回场的公交车。然而，必须应对长途出行和不可预测家庭充电的乘用电动车，曾把 LFP 视为不可行。

![](https://substack-post-media.s3.amazonaws.com/public/images/341cd7fc-c0a2-411d-a2c6-a30d2fb7ea4a_996x552.heic)
*来源：BYD*

2021 年，他们的刀片电池采用了新的封装结构，把电池包每 kg 的空间利用率提升了 [50%](https://volta.foundation/the-next-generation-battery-pack-design-from-the-byd-blade-cell-to-module-free-battery-pack/)。这样一来，LFP 电池在体积不变的同时，续航提升到了可行门槛之上。特斯拉把 Model 3 和 Y 换成了 LFP 电池，福特授权了宁德时代（CATL）的 LFP 技术——通过细致入微的硬件迭代，比亚迪一夜之间创造出了由自己主导的现代平价电动车市场。

刀片电池之前的 2020 年，比亚迪出货了 189K 辆新电动车。刀片电池之后的 2021 年，比亚迪出货 600K 辆，到 2025 年，比亚迪不仅成为全球第一大电动车生产商，还超越特斯拉成为[全球第一大 BEV 生产商](https://www.bbc.com/news/articles/cj9rjwpvmpzo)（纯电），而那是特斯拉的主力产品。比亚迪如今已把流程中如此大比例的环节收归内部（[海豹为 75%](https://www.ubs.com/global/en/investment-bank/insights-and-data/2023/byd-teardown.html)），其成本结构几乎无人能撼动——比如 2023 年约 $11,000 的[海鸥](https://insideevs.com/news/710364/byd-detroit-import-seagull-caresoft/)车型（更新的车型在中国[不到 $8k](https://electrek.co/2025/04/08/byds-low-cost-seagull-ev-now-starts-under-8000-china/)！）。比亚迪甚至掌控着更上游的供应链，例如 [2023 年与华友钴业的冶炼合资](https://evboosters.com/ev-charging-news/the-blueprint-of-an-ev-empire-how-byd-built-global-dominance-through-vertical-integration/)，以及在巴西“锂谷”[直接收购锂矿开采权](https://www.automotivemanufacturingsolutions.com/electrification/how-chinas-byd-surpassed-tesla-with-production-and-battery-tech-reshaping-the-global-ev-market/304649)。

![](https://substack-post-media.s3.amazonaws.com/public/images/5a625853-0a1f-460c-82ad-800655c4c376_3200x2160.heic)
*来源：SemiAnalysis*

这种规模优势让欧洲电动车节节败退，以至于大众（VW）宣布[史上首次](https://www.cbsnews.com/news/volkswagen-could-close-plants-in-germany-first-time-china-ev/)关闭德国工厂，Stellantis 下调[业绩指引](https://www.cnbc.com/2024/09/30/dodge-maker-stellantis-drops-profit-warning.html)，都把原因归咎于中国电动车的压力。连美国也不得不把[中国电动车的关税](https://www.npr.org/2024/05/14/1251096758/biden-china-tariffs-ev-electric-vehicles-5-things)提高到 100%，以保护本国产业。如今，比亚迪的规模已大到甚至拥有自己的[货运船队](https://carnewschina.com/2025/10/02/byd-completed-its-massive-fleet-now-able-to-export-1-million-cars-a-year-but-not-just-from-china/)，把自己最便宜、也最好的电动车运往全世界。

# 大疆打法——小众研究者/爱好者市场是可行的冷启动

大疆开创了一套与比亚迪不同的打法，而宇树今天正在运行这套打法：从研究者/爱好者这块滩头阵地起步，产品起初质量并不高。

2013 年，“有用的消费级无人机”还不是一个品类。当时的领先产品 [Parrot AR.Drone](https://arstechnica.com/gadgets/2013/03/esa-launches-drone-app-to-crowdsource-flight-data/)，拿的是 2010 年 CES *[电子游戏硬件](https://web.archive.org/web/20110416073134/http://www.gamerlive.tv/article/ces-2010-hottest-iphone-game-world)* 类别的奖项，与增强现实空战游戏捆绑销售。这款无人机没有相机增稳、没有 GPS，只能拍 640x480p 的照片/视频。真正想要一台有用的飞行相机的人只有两个选择：要么花 [$19,995 买一台 Draganflyer X6](https://hpisavagex46.wordpress.com/2011/01/24/ubercool-inventions-draganflyer-x6-uav-helicopter-aerial-video-platform/)，要么从各家供应商那里东拼西凑机架、电机、飞控和云台（增稳器），零件[最多花费 $1,200](https://hackaday.com/2011/07/27/how-to-build-your-own-quadcopter-step-by-step/)，再加上几十小时的组装和 PID（控制器）调参，而且往往以昂贵的坠机告终。

![](https://substack-post-media.s3.amazonaws.com/public/images/2316f417-e766-4143-84bf-12f26a3b4185_2500x1666.heic)
*来源：AR Drone 2.0*

研究者、爱好者和早期专业摄影工作者是一个愿意为新事物买单的市场。大疆的 [Phantom 1 于 2013 年 1 月以 $679 上市](https://www.dji.com/newsroom/news/dji-releases-all-in-one-solution-read-to-fly-phantom-quadcopter)，当时并不是一款成熟产品。它没有内置相机、没有云台（增稳器）、只有十分钟续航、没有实时图传，但价格大约是自己组装无人机的一半，而且完全不用承担组装负担。与大疆今天的无人机相去甚远，但 **Phantom 1 发布之后，大疆的营收从 2011 年的 $4M 增长到 2013 年的 [$130M](https://www.wsj.com/articles/who-builds-the-worlds-most-popular-drones-1415645659)**。这足以启动大疆的飞轮。

**接着，大疆收获了深圳消费电子生态的果实——这一生态已因智能手机的繁荣而庞大**。GPS 价格从 2003-2013 年[从 $800 降到 $14 以下](https://www.davidpublisher.com/Public/uploads/Contribute/65446bc585155.pdf)，控制器 2006-2011 年[从](https://www.davidpublisher.com/Public/uploads/Contribute/65446bc585155.pdf) $2,000 降到 $400，等等。在大疆带动的繁荣之下，如今已有[超过 3,000 家](https://electronics.alibaba.com/question/top-chinese-drone-manufacturers-dji,-autel,-ehang-more)无人机零部件供应商，你想要的大多数东西都能找到。

![](https://substack-post-media.s3.amazonaws.com/public/images/39b409ca-b7a1-495a-a48c-c5b5c8eb4a6a_1534x1144.heic)
*来源：GlobalSources*

**大疆选择首先把最昂贵、技术难度最高的组件收归自制：飞控。**2014 年，第三方供应商即使在数千件的批量下仍要卖 $200-400。后来，大疆又把云台、电机和电调（ESC）纳入自制。

和比亚迪一样，大疆的每一代新产品都解锁了上一代无法触及的新市场。2013 年的 Phantom 1（$679、无相机、10 分钟续航、无图传）是冷启动，吸引的是爱好者/研究者。2014 年的 [Phantom 2 Vision+](https://store.dji.com/product/phantom) 则把三轴云台（增稳器）整合进了机身——在此之前，要获得广播级稳定的航拍画面，需要一个 $2,000 以上的后装云台装在手工搭建的机架上，还得由技术娴熟的飞手操作。

在 Vision+ 之前，专业航拍是直升机和好莱坞第二摄制组的天下，而现在，小企业也能自己完成航拍。由此，一个个全新的市场向大疆敞开：房产展示、婚礼录像、本地新闻、农业勘察。到 2016 年的 [Phantom 4](https://store.dji.com/product/phantom-4)（$1,399、4K 相机、28 分钟续航、前向避障、44 mph 运动模式），企业级市场也被解锁：测绘、巡检、应急响应等等，我们在[这里](https://newsletter.semianalysis.com/p/robotics-levels-of-autonomy)有详细展开。

![](https://substack-post-media.s3.amazonaws.com/public/images/b266ee03-ba86-4f6a-a416-06a1e1cffc52_838x472.heic)
*来源：DJI*

2016-17 年，大疆握有全球约 70% 的消费级无人机份额，[全球无人机出货量达到 640 万台、营收 19 亿美元](https://www.businesswire.com/news/home/20160706005481/en/Consumer-Drone-Sales-Increase-Tenfold-67.7-Million)——这个市场在几年前几乎不存在。多家有实力的无人机厂商被碾压。3DR、GoPro 的 Karma 和 Parrot 的消费级产品线都已退出或正在退出这一品类。3DR CEO Chris Anderson [估计](https://www.recode.net/2017/1/9/14182200/parrot-drone-layoffs-dji-3dr-commerical)，Phantom 时代大疆曾在不到一年内把价格砍掉多达 70%。

为简洁起见，本文余下部分将把这套打法称为**“大疆策略”**：掌控一个关键组件，冷启动一个愿意买单的受众，驾驭生态，并让每一代硬件解锁下一个市场。（这一框架的早期版本曾出现在[我们的第一篇机器人报告](https://newsletter.semianalysis.com/p/america-is-missing-the-new-labor-economy-robotics-part-1)中。）

# 宇树：早期的大疆

宇树是“大疆策略”的活案例：掌控瓶颈组件，冷启动愿意买单的受众，驾驭并播种生态，一代一代解锁新市场。到目前为止，宇树已经：

- **把执行器的规模化顺势转化为四足机器人**，打造出市场上性价比最高的足式平台。
- **把四足项目扩展为面向研究者的人形机器人**，G1 成为一个规模大得出奇的市场中的主导研究平台。
- **为硬件改进提供了足够资金，得以开启现实世界部署**，而这道门槛眼下正在被跨越。
- **释放出下一代产品在性能上与西方人形机器人竞争的积极改进信号。**

让我们梳理一遍其历史、设计、策略，以及他们眼下正在跨越的关键门槛——人形机器人部署。

2016 年，曾在大疆[工作过](https://www.thewirechina.com/whos_who/wang-xingxing-%E7%8E%8B%E5%85%B4%E5%85%B4/)的[王兴兴](https://baike.baidu.com/item/%E7%8E%8B%E5%85%B4%E5%85%B4/8766961)为自己的硕士论文开发了一款名为 XDog 的低成本四足机器人。他随后在自己的新公司“宇树”里继续迭代同一款四足机器人。对宇树而言，他们选择的核心组件是执行器——驱动机器人四肢的一体化关节。正如比亚迪之于电芯、大疆之于飞控，宇树选择了昂贵的执行器（占人形机器人 BoM 的 50%-70%）作为改进和规模化的起点。

宇树起步于学术机器人社区，当时只是一家[四足机器人公司](https://newsletter.semianalysis.com/p/quadruped-state-of-the-market-unitree)。正如大疆的爱好者们为半成品无人机付出高价一样，宇树看到大学实验室在寻找一款价格不到 $70-100K+ 的足式平台。[Laikago](https://spectrum.ieee.org/this-robotics-startup-wants-to-be-the-boston-dynamics-of-china) 于 2018 年上市，售价 [$45,000](https://newatlas.com/laikago-quadruped-robot/59867/)。[A1](https://www.unitree.com/a1) 于 2020 年跟进，售价 [$15,000](https://tribotix.com/product/a1-quadruped-robot/)；Go1 于 2021 年上市，Air 版[起价 $2,700](https://spectrum.ieee.org/unitrees-go1-robot-dog-looks-pretty-great-costs-just-usd-2700)，Edu 版最高 $8,500；如今的 Go2 [起价在 $1,600 到 $2,800 之间](https://shop.unitree.com/)，视版本和地区而定。

入门级四足机器人价格在六年间下降了 94-96%，把宇树从学术界推向消费者，如今甚至进入[工业部署](https://newsletter.semianalysis.com/p/quadruped-state-of-the-market-unitree)——更广泛的 AI 浪潮也在提升其硬件能力。更重要的是，这给了宇树多年在同一套系统上的真实量产经验，而这套系统可直接用于人形机器人：执行器、控制、供应商和生产工艺。当宇树于 2024 年以约 $90K 的价格发布 H1 时，这款人形机器人与其说是全新产品，不如说是其四足规模化曲线的直接产物。我们从接近宇树的人士处得知，H1 本质上就是**一台用两条腿站立的四足机器人**——注意它弯曲的膝盖和[笨拙的步态](https://www.youtube.com/watch?v=GN2SNjctwCE)。H1 展示了四足时代的 IP 能被推进到人形机器人多远，而随后的 G1 则彻底改变了宇树的世界。

![](https://substack-post-media.s3.amazonaws.com/public/images/b0210f02-27b9-4976-8b2d-5e645096d08b_1343x889.heic)
*来源：Zoomax*

## $30-50K 的 G1——2024 年的新可能

2024 年年中，在宇树出现之前，买得起的、现货供应的人形机器人寥寥无几。[Agility 的 Digit](https://www.agilityrobotics.com/) 刚刚开始向工厂部署少量机器人。2023 年 8 月发布的 [Apptronik Apollo](https://apptronik.com/) 尚未商用。[Figure 与宝马的首次商业协议](https://www.prnewswire.com/news-releases/figure-announces-commercial-agreement-with-bmw-manufacturing-to-bring-general-purpose-robots-into-automotive-production-302036263.html)签署于 2024 年 1 月，出货量只有个位数。特斯拉则根本没有（截至 V3 版本仍然没有）对外出货 Optimus。中国方面，[UBTech 的 Walker](https://www.ubtrobot.com/)、Fourier 和 AGIBot 的早期迹象已经存在，但既不便宜也没有量。那时没有人能直接“买”到一台人形机器人。

G1 开启了一个规模可观的学术级市场。随便问一位研究者，他们都会告诉你，一台 $30-50K、可直接购买的人形机器人带来了多么剧烈的可及性跃迁。这部分研究社区的人其后通过招聘流向顶级 AI 研究公司——例如 [Nvidia、苹果（Apple）和 Meta 都购买了数百台 G1](https://semianalysis.com/core-research/)。宇树已成为人形机器人 AI 研究的主导平台。

![](https://substack-post-media.s3.amazonaws.com/public/images/933ee9fb-19e9-4601-987e-d6a5ef71f74a_519x393.heic)
*来源：Core Research，宇树在 Robotics Summit 2025 上的演示*

## 生态优势

宇树继承了大疆和比亚迪过去积累的供应商基础。中国 2024 年组装了 [3,130 万辆汽车](https://carnewschina.com/2025/01/14/china-produced-and-sold-31-282-million-and-31-436-million-vehicles-in-2024/)，其中 [40.9% 为新能源](https://carnewschina.com/2025/01/14/china-produced-and-sold-31-282-million-and-31-436-million-vehicles-in-2024/)（BEV 或 PHEV），前面提到的 3,000 家无人机零部件供应商早已把许多 BLDC 电机、驱动器、编码器、电池和制造工艺做到规模化，通用机器人可以直接复用。而宇树的引力效应体现在人形+四足机器人新供应链的崛起上：如今每个省都有若干家尺寸规格合适的减速器、高扭矩 BLDC 电机等部件的制造商。中国境内如今有[约 200 家](https://cnmra.com/china-now-has-over-200-humanoid-robot-manufacturers/)人形机器人公司，都在受益于并反哺这一生态。

![](https://substack-post-media.s3.amazonaws.com/public/images/bfe35430-f3ca-4200-9c10-6bb63086ea75_538x140.heic)
*来源：Leaderdrive*

这一切都源于宇树把执行器做到极致的决定。然而，他们最初几代执行器的表现并不好。

## 2024 年，他们的人形机器人并不好用

*为简洁起见，本文中的 QDD 指无刷直流电机与低减速比行星减速器的组合，减速比通常在个位数、最高 20:1，仍能提供足够的[反向可驱动性（backdrivability）](https://irisdynamics.com/articles/forcefeedback-in-robotics)；但请注意，这一命名存在[术语争议](https://robot-daycare.com/posts/actuation_series_1/)。*

先说清楚：大疆和比亚迪都是在产品真正**好用**时才解锁市场的，而 H1 和初版 G1 在出货时能力**并不**强。一旦用户让它们干真活，电机常常过热。G1 双臂完全伸直时只能负载 2kg——比如一瓶 2 升装可乐——持续几秒就必须强制冷却。手臂弯曲或收缩时，同样的 2-3kg 大概能坚持 2-3 分钟，如下图所示。

![](https://substack-post-media.s3.amazonaws.com/public/images/18ec0090-dfe1-4a78-9e8e-257554b3d9ac_1382x500.heic)
*来源：OmniRetarget*

此后，机器人通常需要约 30 分钟才能恢复功能，很可能要整整一小时才能重新干真正的活。干五分钟、凉一小时，这可不是一台有生产力的机器人。

这个问题主要源于宇树对核心执行器的选择：**QDD（准直驱，quasi-direct-drive），比典型的机器人执行器更简单、更便宜**。历史上，企业偏爱既能驱动机器人又能支撑其自重的高精度、高功率执行器。工业机械臂常用 [HarmonicDrive 谐波减速器](https://www.harmonicdrive.net/technology)。波士顿动力（Boston Dynamics）早期的人形机器人和四足机器人使用[笨重的液压执行器](https://bostondynamics.com/blog/electric-new-era-for-atlas/)。即便在今天，许多人形机器人公司仍默认采用高减速比执行器，比如 HarmonicDrive 的应变波（strainwave）减速器。

这些架构行得通，但昂贵、难制造，而且常常难以维护。2018 年，[MIT Mini Cheetah](https://dspace.mit.edu/handle/1721.1/118671) 让 QDD（准直驱）流行开来：一种更便宜、更简单的替代方案。悬而未决的问题是，QDD 能否规模化、能否证明自己在真实世界机器人中足够可靠。宇树相信答案是肯定的。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

# QDD 为什么会有这些问题？

![](https://substack-post-media.s3.amazonaws.com/public/images/35e5eab0-c226-45b9-9f64-75d6fb6e466b_1050x404.heic)
*来源：宇树（电机）与 Power Electric（减速器）*

QDD 颠覆了历史上常见的机器人关节配置：不用“小电机+大减速器”，而是用更强的电机搭配小得多的减速器。如果机器人想举起 5kg，有两条路。

- **大减速器，小电机。**减速器就像自行车的低速挡，用速度换力量，把电机的扭转力（扭矩）放大 30 倍、100 倍，某些情况下甚至 200 倍。这就是“减速比”，比如 30:1、100:1、200:1 等（多数情况下并非直接的 1:1 对应）。工业机械臂之所以能用不大的电机抡动整块车身，靠的就是这种配置：重活大多是减速器干的。
- **小减速器，大电机。**QDD 走的是这条路，用基础的现货行星减速器，减速比通常低于 20:1。由于减速器几乎不放大任何力，电机就必须强得多。要从上方抬起汽车底盘，就需要一台巨大的电机（我们的[四足机器人报告](https://newsletter.semianalysis.com/p/quadruped-state-of-the-market-unitree)对 QDD 有进一步探讨）。

宇树的 QDD 有其好处，比如能轻松适应外力（如碰撞），或实现快速、动态的动作范围，但代价也随之而来。由于电机直接承担了更多的扭矩负担，而不是依靠减速器放大，早期批评者认为宇树的电机会拉出极高的电流、发热严重，并被证明在实际工作中过于不可靠。

## 两年之后，QDD 正在打破预期

早期批评是公允的：QDD 给了宇树更便宜、更简单的执行器，却把过多的热负担推给了电机，于是有了前述过热问题。**但是**，**当大多数同行坚守应变波（HarmonicDrive）路线时，宇树抓住了机会并不断迭代。**

过去几年，宇树似乎在多个方面改进了执行器，如今展现出可规模化的可喜迹象，许多其他（中国）人形机器人公司正在**转投** QDD 浪潮，并因此**壮大了生态**。我们将尽量在此涵盖宇树已展现的改进之处，但需要说明：我们并未获得循环测试数据，这只是我们对评估其硬件改进的最佳近似。

让我们从经典的 P=I²R 说起——在本例中，热量*大致*随 I²R 缩放。因此你可以做两件事：降低电机需要汲取的电流（I），或降低电流所流经绕组的电阻（R）。大多数人关注电流，因为它是平方项，但两者都有贡献。

减少浪费电流的一个重要杠杆，是让电机的扭矩在每次旋转中更平滑。**通俗地说：骑一辆轮圈略歪的自行车比骑一辆正的更费劲。每转一圈，你都要对抗一小股阻力涌动，平均而言你必须更用力才能维持同样的速度。**

![](https://substack-post-media.s3.amazonaws.com/public/images/5a87cf10-eb9c-4315-80b5-b92303610816_1116x738.heic)
*来源：MQITechnology*

磁拉力不平滑的电机也有同样的问题：转子每转一圈都会轻微顿挫，而你为克服这种顿挫所额外汲取的电流会直接变成热量。这些顿挫来自齿槽转矩（cogging torque）等效应——转子磁钢与定子齿相互作用——也来自产生扭矩纹波（torque ripple）的非理想磁场形状。纹波越少，振动越少，浪费的电流越少，过热之前可用的扭矩也越多。

要解决这个问题，**我们可以对磁钢和槽进行整形或弧形处理，让磁拉力在旋转之间保持平滑**。此外，还可以把磁钢斜置（skew），让定子齿轮流咬合磁场，而不是同时全部卡住。

另一个有用的方案是**往电机里塞更多铜线**。更粗、更密实的线以更低的电阻承载同样的电流，宇树称之为[“低铜耗线圈”（Low Copper Consumption Coil）](https://www.unitree.com/go1/motor)。现已更名为 1X 的 Halodi 也以使用[粗壮的方形铜线](https://x.com/boxcardavid/status/1935133276974498233?s=20)调整其铜填充率而闻名。

对于一台能干活的机器人，散热仍然重要，但宇树的架构在这方面相当保守。我们发现其**大部分机身采用被动散热**，仅主控制板和髋关节有主动风冷，膝盖处有一片均热板（vapor chamber）。宇树在这里也**做了迭代**：在 2025 年 10 月的更新中为骨盆周围增加了主动散热，改善了后续 G1 批次的热余量。

![](https://substack-post-media.s3.amazonaws.com/public/images/b398c0af-1ef5-487f-8e71-7563f231f051_1032x847.png)
*来源：JONVER Electronics*

我们猜测，宇树之所以在散热上着墨不多，是因为它想降低成本和制造复杂度，同时聚焦我们前面提到的核心问题：降低电机所需的电流量。

## 那当初为什么选 QDD？一段关于速度+成本的题外话

宇树押注 QDD，在机器人最昂贵的组件上采用了（在部署层面）未经证明的架构。虽然难对付，但 QDD 的效率更高（95%-98%，而应变波为 85%-90%），而且便宜多达 80%。重要的是，低减速比行星减速器还是常见的工业部件，用广泛普及的设备进行标准滚齿加工（可理解为磨削），因此可以存在众多供应商。

相比之下，选择应变波减速器（例如 HarmonicDrive 或 LeaderDrive 的产品）的竞争对手则要面对更复杂的约 13 道工序。对金属晶粒进行数小时热处理以使其能够“柔性变形”（见下图）、微米级公差的精密滚齿等等，这一切构成了一个 HarmonicDrive 花了几十年才完善的工艺流程，而 LeaderDrive 成立 20 多年后仍被许多人认为在可靠性上落后于 HarmonicDrive。

![](https://substack-post-media.s3.amazonaws.com/public/images/620ef23c-344e-437b-8a16-92ef5a28a6c8_614x239.heic)
*来源：Nature*

与其纵向整合一条长达数十年的学习曲线，宇树选择了 QDD。如今，**一次新的 QDD 改版设计，宇树几周内就能拿到执行器样件**。作为对照，一个定制电机+减速器子系统可能要让一家西方人形机器人公司花 3 个月以上，原因在于供应链环节的层层交接：数周的规格迭代，6-8 周等待电机+减速器样件，然后是验证和返单。其结果是生产更便宜（如我们的 BoM 所示），迭代也更快——骨盆主动散热的悄然上线就是一例，几乎没有引起注意。

## 从烧毁到轻量任务

如今，宇树已对其 G1 和执行器做了足够的迭代与改进，使一些虽小但正经的任务触手可及。手臂弯曲时，G1 能带着 5 kg 负载持续作业 10-15 分钟以上，相比我们最初的数据，负载约提升 2 倍、持续时间提升 5 倍！双臂完全伸直时，能坚持托举 5kg（大约一个保龄球）约 1 分钟才触及热极限。这即便对人类来说也算一场锻炼。那么，宇树距离成为一台“可行”的人形机器人还有多远？

![](https://substack-post-media.s3.amazonaws.com/public/images/c488823a-e542-4715-806a-c0522455554e_998x520.heic)
*来源：NVIDIA*

# 迈向有用的工作

宇树显然非常便宜，我们也清楚它的策略和硬件进步轨迹，但这重要吗？也许有人会指着上一节说，托着 5kg 干 15 分钟不算什么：“灵巧性不够”、“它没有灵巧手”、“时间不够长”等等。然而，我们估计，除研究/爱好者销售之外，宇树 2025 年可能已有多达 **250 台人形机器人**出货进入生产性行业试点或部署。我们甚至发现一家公司**如今部署了 30 台 G1，还有多家公司部署了 5-6 台 G1**。当然，这些部署很可能受软件限制（例如 AI 模型能力），经济性会因所用方案不同而不同，比如 100% 远程操作（teleoperation）——这也是我们计算中采用的假设。

宇树机器人不需要完美运行，也不需要长时间运行，我们也不指望它们如此。真正的问题是：要做到“有用的工作”，什么程度就足够了。G1 的手臂依然动力不足，“自由度”也不足以完成完全拟人的动作，在过于繁重的岗位上仍会过热。但这只是给 G1 能做的任务类型设了一个**上限**，而不是判定它到底能不能做事的**下限**。

![](https://substack-post-media.s3.amazonaws.com/public/images/026abe1b-5aef-4c17-9aa8-19efdff04a45_350x482.heic)
*来源：ExtremControl*

抛开表演性的后空翻不谈，宇树机器人已经能够承担“有用的工作”，本文将其非穷尽地定义为以下二者之一。

*在企业中执行的、产出某种经济价值的任务，比如分拣箱子；或者为减轻人类身体负担而执行的任务，比如叠衣服。*

那么这些宇树机器人实际在干什么？本质上就是把箱子/物品从 A 搬到 B。目前多为轻量物料搬运，比如电商周转箱（料箱）搬运，负载 <3-5 kg，甚至只是搬运空箱/空料箱。

这些都不是 24 小时全自动产线，大多数仍靠远程操作。尽管如此，让我们来论证：搬箱子这件事正在变得经济可行。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

# 宇树机器人正在跨越部署可行性门槛

*“感谢 [Adamo](https://adamohq.com) 帮助我们进一步理解远程操作部署！”*

我们在 [Levels of Autonomy 报告](https://newsletter.semianalysis.com/p/robotics-levels-of-autonomy)中深入讨论过人形机器人的经济学，但在这里我们为宇树做一次完整计算。以 Agility Robotics（出色）的任务为基线，代入宇树的输入参数，我们发现宇树机器人**目前正跌破**人类每小时 $30 的劳动力成本线。

![](https://substack-post-media.s3.amazonaws.com/public/images/c65732ee-db1a-4891-b407-122c68480c71_4183x2354.heic)
*来源：SemiAnalysis 估算*

目前还没有任何人形机器人进入大规模量产/部署，所有玩家仍在迭代技术，而且这些数字会因部署具体情况（夹爪/灵巧手、负载、吞吐量等）而变化。我们将展示的是对它们当下能力的最佳估计，以及在一项具体任务上的表现，但想强调：这些都是早期阶段的数字，**而且如果宇树的硬件延续其改进轨迹、自主能力继续提升，经济性从现在起大概率只会更好。**

![](https://substack-post-media.s3.amazonaws.com/public/images/97e26440-c3fb-4c98-a58e-d29dc7d77eab_441x377.heic)
*来源：Agility Robotics*

## 一项可爱的任务：料箱交接

在这项具体工作中，Agility 充当自动化系统之间的“桥梁”，例如把料箱从 AMR（自主移动机器人）上取下、放到传送带上。这是一种标准但又特殊的物流工作负载：人类通常要等待自动化系统排队就位才能交接，中间留有大量空转时间。这也解释了为什么 Agility 每小时 [66 个料箱](https://www.automationworld.com/factory/robotics/article/55303585/agility-robotics-agility-robotics-digit-shows-promise-in-line-side-operations-with-new-iso-safety-standard-on-the-horizon)的吞吐（来自会议演示，实际部署中可能更高）完全够用。

![](https://substack-post-media.s3.amazonaws.com/public/images/6fdb642f-6b71-4e4a-a230-513c2fbbf281_992x490.heic)
*来源：The Robot Report*

此外，在 Agility 的 GXO 部署中，料箱重量为 [2-4kg](https://www.therobotreport.com/gxo-logistics-putting-digit-humanoid-to-test/)（正适合前述的宇树机器人）。负载轻、吞吐低、失败后可从容重试、几乎不需要灵巧操作——对当前的[自主能力等级](https://newsletter.semianalysis.com/p/robotics-levels-of-autonomy)来说，这是一项完美任务。

![](https://substack-post-media.s3.amazonaws.com/public/images/e636c2c0-f448-4bb5-9b76-a467d827bb7f_392x506.heic)
*来源：OmniRetarget*

## 计算宇树的经济可行性

Agility [目前采用](https://x.com/agilityrobotics/status/1909763546671726776?s=20) [2:1 的利用率模型](https://www.therobotreport.com/heres-what-it-could-cost-to-hire-a-digit-humanoid/)运行——每充电一个单位时间即运行两个单位时间——这使 Digit 相对人类拥有**三分之二的利用率**。

![](https://substack-post-media.s3.amazonaws.com/public/images/f56c6c37-3697-4b85-80c9-c1167c673095_780x440.heic)
*来源：Agility Robotics*

在类似的 2-4 kg 料箱转运工作中部署宇树机器人的运营方告诉我们，其吞吐量与 Digit 在该任务上相当。不过，宇树机器人并不是最皮实的机器人。一台宇树 G1 通常连续执行类似任务 10-15 分钟，然后需要 5-10 分钟冷却，但仍能保持 50%-67% 的利用率。在我们的假设中，我们**非常**保守：假设 100% 远程操作、15% 的服务合同费用（工业场景通常为 5-10%）、两年使用寿命、零残值，而且只算两班倒。即便如此，这台机器人**今天**就被证明是可行的。

![](https://substack-post-media.s3.amazonaws.com/public/images/f6340598-8962-405a-83b4-1cd909022265_4183x2354.heic)
*来源：SemiAnalysis 估算*

先把免责话说在前面：我们并不是说宇树已经是完整方案。还有很多层需要补齐。例如，Agility 拥有出色的操作系统来与仓库管理系统协同、更深入的功能安全方案、自有的自主能力层等等。但对宇树而言，即便 100% 远程操作，**如今**在合适的业务场景下似乎也已经可行。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

## 事情将走向何方

据我们所知，这是宇树人形机器人在部署中展现有用工作的第一阶段。这并不是说这项任务多么特别、或是一个 $100T 的 TAM，而是它表明宇树可能正在跨越一道门槛，而其轨迹相当了不起。回想大疆曾向小众爱好者出货半成品无人机，把营收做到 32 倍，迅速一跃成为无人机霸主。最初，G1 托一个箱子 2-3 分钟也会过热。迄今为止的性能改进，都是爱好者/研究者出钱资助的。一旦宇树解锁仓储 TAM 哪怕一小块，进步就可能以惊人的速度加速。

随着机器人 AI 模型[不断获得新能力](https://www.pi.website/blog/pi07)、BoM 下降、硬件质量持续改进，宇树有可能成为市场上最便宜且能力过硬的人形机器人平台。下面就来谈谈他们是如何做到世界领先的 $8,976 BoM 的。

# 中国的制造实力

到目前为止，本文一直在暗示宇树的制造能力及其周边生态。对机器人以及许多其他行业来说，要在全球尺度上竞争，与中国生态合作是必要的：供应商坐火车几小时就到，样品当天/次日即到，纵向迭代周期以周计而非以季度计，零部件比西方同类便宜 20-40%。值得注意的是，以 LeaderDrive 的应变波减速器为例，其价格有时只有 HarmonicDrive 的**三分之一**——当然，HarmonicDrive **目前**仍是可靠性方面的领导者。

大多数美国机器人初创公司已经在与中国供应链合作，例如 Sunday Robotics、Dyna 和 XDOF，它们的硬件团队都常驻中国。连特斯拉 Optimus 也从中国供应链采购，而且很可能[继续](https://www.scmp.com/tech/tech-trends/article/3341953/optimus-chain-chinese-suppliers-form-backbone-teslas-humanoid-robot-initiative)如此。

## 宇树的纵向整合程度惊人——即便在中国

中国生态固然了不起，但我们已反复强调纵向整合的好处，这里展开说说。宇树自研 BLDC 电机、行星减速器、LiDAR 和深度相机——这些通常（甚至对早年的宇树来说也是）由其他中国人形机器人 OEM 外购。而宇树自产电机的价格最低可做到西方同级电机的 30-40%，**他们如今还生产着世界上最便宜的一批人形机器人减速器。**

![](https://substack-post-media.s3.amazonaws.com/public/images/12b16c91-48e1-44da-aabf-c85fdcee2239_1266x713.heic)
*来源：IQSDirectory*

这些优势在 IPO 申报文件中体现得非常明显。在宇树向上海证券交易所（SSE）提交的[首轮问询回复](https://static.sse.com.cn/stock/disclosure/announcement/c/202603/002178_20260320_OE27.pdf)中，他们明确表示，规模化生产赋予了他们**上游议价权**，从而形成了持久的成本优势。

![](https://substack-post-media.s3.amazonaws.com/public/images/fbba04cf-cbd2-4781-bc32-ba5f822a5b5d_1255x535.heic)
*来源：宇树首轮问询回复，8-1-1-14*

这体现为其四足机器人的毛利率从 **42.36%** 提升到 **55.49%**，而成本几乎**腰斩**。不过，SemiAnalysis 订阅者[早在去年 9 月](https://newsletter.semianalysis.com/p/quadruped-state-of-the-market-unitree)就知道这些四足机器人的毛利率了。

![](https://substack-post-media.s3.amazonaws.com/public/images/c2cbfeee-3cba-47c1-8bff-256156183d32_1982x809.png)
*来源：SemiAnalysis*

这种纵向整合在西方市场堪称奇观，但即便在中国——那里硬件利润薄如刀刃、不纵向整合就难以求生——也是如此。前文的比亚迪和大疆已经展示了通过纵向整合走向主导地位的路径。UBTECH（优必选）和 AGIBot（智元）（两家主要的中国人形机器人竞争对手）正在[积极行动](https://biz.chosun.com/en/en-industry/2026/03/20/CNMGR4IU6ZAAHKJFX7WEXCYSXY/)，把减速器、电机等更多硬件纳入掌控——而这些组件宇树早已自研。

UBTECH 和 AGIBot 在制造乃至部分最终组装环节仍依赖 ODM/OEM 合作伙伴，比如 AGIBot 把欧洲生产外包给了塞尔维亚的敏实集团（Minth Group）。即便如此，AGIBot 还在以 $4M 的价格授权全套技术转移，靠合作伙伴扩张，而不是自己掌握制造学习曲线。相比之下，宇树在其 S-1 中表示计划把更多开发环节收归内部，包括“齿形设计、仿真优化、材料验证和高精度加工”。

然而，无论是宇树还是其他人形机器人公司，都还没有进入大批量生产。这意味着，即便各家开始放量，宇树从先发者角度看也很可能维持**结构性成本优势**。未来的文章将详述中国工业生态的全貌，但眼下请先假设：大多数人形机器人都会从中国采购，而即便在中国，宇树也是出类拔萃的。

# 结论

当西方厂商还在（且仍在）做人形机器人原型时，宇树已经盈利地出货了数万台四足机器人、建起了整个人形机器人市场、进入了有用的人形机器人工作。但每个人都应该思考：宇树的边界在哪里？比亚迪起步时只有电池电芯，大疆只有飞控，如今都已是行业巨人。

纵观宇树如何通过多种机器人形态加速成功，并不断夯实制造优势，它们或许会以同样的速度继续扩张，解锁此前难以想象的市场。

现在，让我们来谈谈机器人灵巧手，以及宇树的哪些供应商可能受益——这些内容都在付费墙之后。
