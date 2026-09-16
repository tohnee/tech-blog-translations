---
title: "数据中心解构 第一部分——电气系统"
title_en: "Datacenter Anatomy Part 1: Electrical Systems"
subtitle: "Meta 拆除在建数据中心，Vertiv、Schneider Electric、Eaton、Legrand、Delta，按组件划分的数据中心物料清单，变压器、开关设备、冗余、UPS、OCP 母线、发电机、变电站"
date: 2024-10-14
source: https://newsletter.semianalysis.com/p/datacenter-anatomy-part-1-electrical
crawled: 2026-09-15
authors: ["Jeremie Eliahou Ontiveros", "Dylan Patel", "Daniel Nishball"]
tags: ["Datacenter", "Hardware Architecture", "AI Infrastructure"]
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 数据中心解构 第一部分——电气系统

> 原文：[Datacenter Anatomy Part 1: Electrical Systems](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-1-electrical) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Meta 拆除在建数据中心，Vertiv、Schneider Electric、Eaton、Legrand、Delta，按组件划分的数据中心物料清单，变压器、开关设备、冗余、UPS、OCP 母线、发电机、变电站**

## Meta 拆除在建数据中心，Vertiv、Schneider Electric、Eaton、Legrand、Delta，按组件划分的数据中心物料清单，变压器、开关设备、冗余、UPS、OCP 母线、发电机、变电站

多年来，数据中心行业一直都是一个关键行业，但如今，由于其在国家安全和未来经济增长中扮演的重要角色，该行业正经历前所未有的加速——这一切都由 AI 训练和推理的海量需求所驱动。AI 引发的电力需求激增带来了巨大的宏观与微观影响，而供给十分紧张。

过去几年，行业一直在零散地、逐步采用能够实现更高功率密度的关键系统，而高功率密度对 AI 应用至关重要。这一推动主要由较小的玩家引领，它们推出自己的全新设计来承载 AI，却并没有得到 Nvidia 的背书——与 Google 相比，Nvidia 在采用液冷方面动作迟缓。这些年里，行业始终没有形成统一标准。

随着即将到来的 Blackwell 爬坡，这一切都在改变。Nvidia 的 [GB200 家族](https://semianalysis.com/gb200-hardware-architecture-and-component)要求冷板式直冷，机柜功率密度高达 130kW，相较 H100 带来约 9 倍的推理性能和约 3 倍的训练性能提升。任何不愿或无法提供更高密度液冷的数据中心，都将错失为客户带来的巨大性能与 TCO 改善，并在这场生成式 AI 军备竞赛中掉队。

Blackwell 把需求标准化了，如今供应商和系统设计者有了清晰的 AI 数据中心发展路线图，这将导致数据中心系统与组件格局中赢家与输家的大洗牌。

这些设计转变已经造成了相当大的影响。例如，Meta 拆除了一栋在建建筑，因为那是他们沿用多年的旧数据中心设计，功率密度偏低。取而代之的是他们全新的 AI-Ready 设计！大多数数据中心设计都尚未为 GB200 准备就绪，而 Meta 尤其突出——与其他超大规模云厂商相比，其数据中心的功率密度是最低的。

![](https://substack-post-media.s3.amazonaws.com/public/images/3ae5f53c-509f-4232-8a47-fc71cb47d261_2542x822.jpeg)
*来源：SemiAnalysis 数据中心模型*

在本篇报告《数据中心解构 第一部分——电气系统》中，我们将深入剖析 AI 数据中心的电气系统，并探讨[吉瓦级集群](https://semianalysis.com/multi-datacenter-training-openais)将如何冲击传统供应链。我们将讨论 Vertiv、施耐德电气（Schneider Electric）、伊顿（Eaton）等关键设备供应商，以及 AI 对其业务的影响。我们将展示我们的数据中心物料清单（BOM）估算，并推导出按组件划分的行业资本开支（capex）预测。

后续报告将探讨设施冷却系统、浸没式（Immersion）等即将到来的服务器冷却技术，并深入解析超大规模云厂商的设计。本报告基于我们对 200 多家数据中心相关供应商的追踪工作、按产品划分的市场份额建模，以及对液冷等新关键技术的自下而上 TAM 测算。此外，我们还通过[基于半导体的逐 SKU 需求预测和逐建筑的数据中心产能预测（至 2030 年）](https://semianalysis.com/datacenter-model)，拥有市场上最详细的自上而下估算。

## 数据中心基础

数据中心是一种专门建造的设施，旨在以高效、安全的方式向 IT 设备供电，并在 IT 硬件的整个生命周期内实现尽可能低的总拥有成本（TCO）。IT 设备通常布置在装满服务器、网络交换机和存储设备的机柜中。运行这些设备可能需要大量电力，并产生大量热量。

三十年前，这些设施看起来就像配备了强化空调的办公楼，但自那以后规模已大幅增长——如今的消费者每天观看数十亿小时的 YouTube 视频、Netflix 剧集和 Instagram 动态。这引发了数据中心建设方式的深刻变革：现代设施单位面积的用电量可达典型办公楼的 >50 倍，而为这些服务器散热需要截然不同的冷却基础设施。

![](https://substack-post-media.s3.amazonaws.com/public/images/9efdb98a-a46e-4b41-9a8a-f56bfa90e7bf_1021x677.jpeg)
*来源：Data Center Dynamics*

在这样的规模下，任何由数据中心问题导致的中断都可能造成重大营收损失并损害运营商的声誉——无论是 Azure、AWS 这样的云服务提供商（CSP），还是托管运营商（数据中心地产）。确保高正常运行时间意味着更多收入，而这在很大程度上取决于内部可靠的电气与冷却系统。电气故障虽然更常见，但其「爆炸半径」往往更小，通常不如冷却故障破坏性大。

评估数据中心预期停机时间与冗余的一个有用框架，是 Uptime Institute 的[「Tier」等级分类](https://uptimeinstitute.com/tiers)或 ANSI/TIA-942 标准（基于 Uptime 的 Tier 体系），下图展示了其四个评级级别。

![](https://substack-post-media.s3.amazonaws.com/public/images/b1e1a445-f050-413e-97ae-f778bced2444_2395x1800.jpeg)
*来源：PRASA*

「Rated 3」数据中心（及同等标准）是全球大型设施中最常见的，并且始终要求为 IT 设备配备备份电力冗余。谈到冗余时，我们使用「N」「N+1」或「2N」等术语。例如，如果一座数据中心需要 10 台变压器，N+1 意味着总共购买 11 台，其中 10 台运行、1 台冗余；而 2N 则需要购买 20 台变压器。

Rated 3 设施必须做到「可同步维护」（concurrently maintainable），通常要求变压器和发电机等组件采用 N+1 冗余，配电组件——不间断电源（UPS）和配电单元（PDU）——采用 2N 冗余。Rated 4 数据中心较为少见，必须做到「容错」（fault tolerant）——常见于关键任务或政府数据中心设施。

顺带一提，CSP 常谈到「三个 9」（99.9%）或「五个 9」（99.999%）的预期可用性——这是其与客户服务水平协议的一部分，覆盖的是服务的正常运行时间，比单一数据中心的预期可用性范围更广。其中涵盖多座数据中心（「可用区」），也包括服务器和网络等组件的正常运行时间。

## 从零售型数据中心到超大规模园区

数据中心有各种形状和规模，我们通常依据其关键 IT 功率容量（即 IT 设备的最大功率）以千瓦为单位进行分类。这是因为在托管业务中，运营商出租空机柜并按「IT kW/月」计价。数据中心的空间成本远低于为客户服务器供电所涉及的电气与冷却设备。

关键 IT 功率（Critical IT Power）指 IT 设备的最大功率，而从电网实际抽取的功率还包括冷却和照明等非 IT 负载，以及稼动率系数。平均而言，云计算工作负载的功率利用率通常为 50-60%，AI 训练则超过 80%。企业自用往往甚至低于 50%。

我们将设施分为三大类：

**零售型数据中心（Retail Datacenters）**：功率容量较低的小型设施——至多几兆瓦，但通常位于城市内部。它们通常拥有许多只租用几个机柜（即几 kW）的小租户。其价值主张在于将众多不同客户汇聚在同一设施内，提供强大的网络生态系统。通过提供与其他客户和网络的低延迟便捷互联，零售型数据中心运营商可以降低客户的网络成本。因此，零售型数据中心运营商的商业模式更接近传统地产玩法，讲究「位置、位置、位置」的价值主张。

![](https://substack-post-media.s3.amazonaws.com/public/images/9f37681d-58aa-4e7b-be59-e098e222dedd_1712x986.jpeg)
*来源：Google Earth（此处）*

**批发型数据中心（Wholesale Datacenters）**：功率在 10-30MW 区间的较大型设施。这类设施中的客户往往租赁更大面积，即整列或多列机柜，并可选择进一步扩张。与零售型数据中心相反，其价值主张在于部署更大容量并具备随时间扩展的弹性。许多批发型数据中心分期建设以达至最终容量，这意味着随着客户所需求容量的增长，它们可以相应扩张。下面是一个由 Digital Reality 持有的例子。

![](https://substack-post-media.s3.amazonaws.com/public/images/77ee092f-357c-4cb9-8077-1a3858835b76_1482x1140.jpeg)
*来源：Google Earth（此处）*

**超大规模数据中心（Hyperscale Datacenters）**：这类设施通常由超大规模云厂商自建并专用，单体建筑通常为 40-100MW，是拥有多栋互联建筑的更大园区的一部分。此类园区的规模在数百 MW 量级，例如下图这个功率接近 300MW 的 Google 站点。大型科技公司也可以委托托管运营商建造「定制代建」（build-to-suit）数据中心——按超大规模云厂商的规格建造，然后出租给该超大规模云厂商。规模超过 100MW 的定制代建租约正日益普遍。

![](https://substack-post-media.s3.amazonaws.com/public/images/fada17a6-9427-4f9a-81b9-e89b72d9eddf_2178x1260.jpeg)
*来源：SemiAnalysis 数据中心模型*

我们还可以按运营商将数据中心分为两类：**托管（Colocation）**或**自建（Self-Build）**。

托管就是以功率为单位（$/kW/月）向第三方数据中心运营商租赁数据中心容量。典型的小型租约为 100-500kW 关键 IT 功率，而批发级租约通常在 1-5MW 之间。超大规模客户通常租赁 5MW 以上的规模，租赁整个园区时甚至可达数百 MW！

这可以帮助超大规模云厂商提高资本效率——无需预先支付 Capex，也无需处理诸多物流事务。超大规模云厂商还会采用介于定制代建租赁与自建之间的混合安排——例如租赁「暖壳」（warm shell）建筑，它已确保接通市政电力，但由超大规模云厂商在租赁的壳体内自行建设机电基础设施。

另一方面，自建数据中心由企业为自身专用而私人建设。历史上这类建设由金融、支付、医疗、政府、能源等敏感数据行业的大型企业承担——例如摩根大通（JPMorgan）或 Verizon。这些数据中心的设计千差万别，但单设施功率容量通常介于零售型与批发型数据中心之间。

但过去 10 年数据中心市场影响最深远的趋势，当属自建超大规模数据中心的崛起，其主要驱动因素是云计算的兴起，以及运行[日益强大的推荐模型](https://semianalysis.com?p=114314781/the-largest-at-scale-ai-model-architecture-dlrm)和内容分发等工作的社交媒体平台。如上所述，超大规模云厂商也可以租用托管容量。常见原因包括：在没有规模或本地市场知识支持自建的市场、缺乏能够执行复杂项目的本地团队，或作为更快扩充总产能的手段。超大规模云厂商还有更靠近终端用户的小规模部署需求，例如网络边缘、内容分发网络（CDN），这类场景用托管更为合适。

为了让读者对超大规模园区的电力需求有直观感受：美国家庭某一时刻的用电功率最高可达 10kW，但实际平均负荷约为其 1/9，即 1.214kW。因此，考虑到更高的功率利用率，一座 300MW 数据中心园区的年耗电量轻松相当于 ~200,000 户家庭。

我们此前[数据中心深度报告](https://semianalysis.com/ai-datacenter-energy-dilemma-race)中的表格也应能帮助读者把这些容量数字与 AI 部署联系起来：一个 20,840 块 Nvidia H100 组成的集群需要一座关键 IT 功率容量约 25.9MW 的数据中心。这一数字还将大幅上升，因为人们现在正在建设 [100,000 块 H100 集群](https://semianalysis.com/100000-h200-clusters-power-network)和[吉瓦级集群](https://semianalysis.com/multi-datacenter-training-openais)。

![](https://substack-post-media.s3.amazonaws.com/public/images/553c9add-cb81-4c1c-be5c-89eb95749d98_1424x1068.png)
*来源：SemiAnalysis 数据中心模型*

介绍完基本分类，我们来看看电力是如何送入这些设施的。

## 数据中心的电气系统

我们从一个高度简化的布局入手，来理解这些设施的设计。目标是向装满 IT 设备的机柜输送大量电力，这些机柜布置在称为数据大厅（Data Hall）的房间里。要做到既高效又安全、同时保障硬件寿命，需要大量设备。

为了尽量减少配电损耗，我们希望在物理上尽可能靠近终端设备之前，始终保持尽可能高的电压——电压越高意味着电流越小，而功率损耗与电流的平方成正比（Ploss = I2R）。

但高电压可能很危险且需要更多绝缘，不适合用在建筑物附近——因此中压（如 11kV、25kV 或 33kV）是将电力送入建筑的首选方案。进入数据大厅后，需要再次将电压降至低压（美国为 415V 三相电）。

从外到内，电力沿以下路径流动：

![](https://substack-post-media.s3.amazonaws.com/public/images/0d29156c-5276-40ec-ad7b-6466a998eeba_1327x1137.jpeg)
*来源：DEAC*

- 电力公司输送高压（>100kV）或中压电力。若是前者，则需要一座配备电力变压器的现场变电站，将其降至中压（MV）。
- 随后中压电力经由中压开关柜安全地分配到另一台变压器——它物理上靠近数据大厅——将电压降至低压（415V）。
- 与变压器配套的是一台柴油发电机，同样输出 415V 交流电。如果电力公司供电中断，自动切换开关（ATS）将自动切换至发电机供电。

从这里开始有两条供电路径：一条通向 IT 设备，另一条通向冷却设备：

- IT 设备路径首先经过 UPS 系统，后者连接一组电池：通常配置 5-10 分钟的电池储能，足以让发电机在一分钟内启动，从而避免瞬时断电。
- 「UPS 电力」随后直接供给 IT 设备，一般通过配电单元（PDU）分配。
- 最后一步是通过电源供应单元（PSU）和电压调节模块（VRM）将电力送达芯片，这部分我们曾在[此处](https://semianalysis.com/energizing-ai-power-delivery-competition)详细讨论。

当然，这张示意图会因数据中心容量的不同而差异巨大，但总体思路和电力流向是一致的。

## 高压变压器

现代超大规模数据中心当然比上面这张示意图复杂得多。此类园区通常拥有一座现场高压变电站，例如下图所示的 Microsoft 站点，或前文的 Google 园区。

![](https://substack-post-media.s3.amazonaws.com/public/images/55087283-41d0-4b73-8839-480eea7fdb59_2172x1458.jpeg)
*来源：Google Earth、SemiAnalysis*

由于需要在密集地点获得 >100MW 的电力，这些设施通常会选址在高压（HV）输电线（138kV、230kV 或 345kV）附近。这些线路的输电能力远高于中压（MV）配电线路——在某些地区，监管机构会根据电力线路的电压等级设定最大用电功率。因此，超大规模云厂商需要一座现场变电站，将电压从 HV 降至 MV。如果没有配备高压变压器的现成变电站，数据中心运营商要么自建，要么出资让电力公司建设一座。

这些变压器以 MVA 为额定单位：1 MVA 大致相当于 1 MW，但 MVA 是「视在功率」（即电压 × 电流），而 MW 是「有功」功率；由于[功率因数](https://en.wikipedia.org/wiki/Power_factor)的存在，MW 数值更低——功率因数反映了交流配电系统中的低效环节。5% 的差异很典型，但为了留出余量，数据中心运营商通常按 10% 的功率因数进行配置。

典型高压变压器的额定容量在 50 MVA 到 100 MVA 之间：例如，一个需要 150MW 峰值功率的数据中心园区可以使用两台 80 MVA 变压器，或者为实现 N+1 冗余而使用三台，以覆盖可能的故障——每台将电压从 230kV 降至 33kV，电流从约 350 安培升至约 2500 安培。在这种 N+1 配置中，三台变压器共同分担负载，但只以额定容量的 2/3 运行，以便发现任何早期失效（即初次启用时的故障），并避免完全闲置的变压器可能出现的性能劣化。值得注意的是，高压变压器通常是定制的，因为每条输电线路都有自己的特性，因此交期往往很长（>12 个月）。为了缓解这一瓶颈，数据中心运营商可以在规划阶段提前下单。

尽管变压器是我们电力传输系统的核心部件，但它是非常简单的设备：它将交流（AC）电力的电压和电流从一个等级变换到另一个等级。这项拥有百年历史的技术之所以有效，是因为电流会产生磁场——而交流电会产生持续变化的磁场。

![](https://substack-post-media.s3.amazonaws.com/public/images/97a9f6a9-af3a-4ac9-88ba-eceaacc6a6f2_1806x1034.jpeg)
*来源：The Engineering Mindset*

两个铜线圈相邻放置——当一段导线紧密缠绕在一起时，会产生强磁场。将两个这样的线圈靠近放置并通以交流电，就可通过[磁感应](https://en.wikipedia.org/wiki/Electromagnetic_induction)把功率从其中一个传递到另一个。在此过程中，总功率保持不变，但我们可以通过改变导线的特性来改变电压和电流。

如果次级线圈的「匝数」少于初级线圈，功率将以更低的电压和更高的电流传递——这就是降压变压器的一个例子。

![](https://substack-post-media.s3.amazonaws.com/public/images/2be968dd-b160-4711-9955-6bced6a07a16_2014x1332.jpeg)
*来源：GeeksforGeeks*

变压器的两大主要部件是用于线圈的铜，以及用于「变压器铁芯」（transformer core）的钢——铁芯的作用是促进能量传递。剖析变压器短缺问题时，症结通常在后者：需要一种特殊钢材，称为取向硅钢（GOES，Grain Oriented Electrical Steel），其制造商数量有限。

## 数据大厅与 Pod

回到数据中心和我们的电力流向：现在我们拥有了 11kV、25kV 或 33kV 之一的中压电力（取决于集群配置和位置），要把它输送到 IT 机柜。现代数据中心以模块化方式建造，下面这座 Microsoft 数据中心就是一个完美的例子。

![](https://substack-post-media.s3.amazonaws.com/public/images/a070a333-e879-497d-a899-f4f699b06c99_2134x1508.jpeg)
*来源：Google Earth、SemiAnalysis*

一栋建筑通常被划分为多个数据大厅（蓝色矩形）——数据大厅就是我们摆放服务器的房间。在上面的例子中，我们认为每栋建筑（约 25 万平方英尺）的关键 IT 容量为 48MW，每栋建筑分为五个数据大厅，即每个数据大厅 9.6MW。

数据大厅内布置着多个「Pod」，每个 Pod 由自己专属的一套电气设备供电：发电机（橙色矩形）、变压器（绿色矩形）、UPS 和开关柜。在上图中，我们可以看到每个数据大厅配有四台发电机和四台变压器。每个大厅还有四个 Pod，这也意味着四个低压配电柜（switchboard），以及按 2N 配电冗余假定的八套 UPS 系统。

![](https://substack-post-media.s3.amazonaws.com/public/images/6b06a8bb-6996-4001-abca-130b8ef52dd1_2024x1032.jpeg)
*来源：Legrand*

数据大厅通常被划分为 Pod，原因有二。

- 模块化：设施可以渐进、快速地扩容以承载更高负载。
- 标准化：Pod 的尺寸设计为与最标准化（即便宜且现成可得）的电气设备相匹配。在 Microsoft 这个例子中，我们看到多台 3MW 发电机和 3MVA 变压器——这些规格在众多行业中被广泛使用，采购起来远比那些更大、更小众、更定制化的设备容易。最常见的 Pod 尺寸是 1600kW、2MW 和 2.5MW，尽管理论上任何 Pod 尺寸都是可行的。

## 发电机、中压变压器与配电

在高压变压器（HV Transformer）的帮助下，电压从高压（如 115kV、230kV 等）降至中压（MV）（如 33kV、22kV 或 11kV 等）之后，我们使用中压开关柜将这些中压电力分配到各个 Pod 附近。服务器和网络交换机等典型 IT 设备无法在 11kV 下运行，因此在电力进入数据大厅之前，还需要另一组中压（MV）变压器——通常为 2.5 MVA 或 3 MVA——将电压从中压（11kV/25kV/33kV）降至低压（LV，415V，美国的常见电压）。

下面的示意图有助于说明典型的高压与中压配电：电力如何从 HV 降至 MV，再由通常布置在设施外或设施内的中压开关柜进行分配，其配置方式确保每个数据大厅都可由两个不同电源供电，不留任何单点故障。

![](https://substack-post-media.s3.amazonaws.com/public/images/478574eb-fef6-4f20-8228-24af193d4ddd_1994x1092.png)
*来源：Schneider Electric*

中压开关柜是一个工厂组装的金属柜体，内含用于分配、保护和计量电力的设备。

![](https://substack-post-media.s3.amazonaws.com/public/images/cbea7e05-312a-4a05-a3c3-237a675231f2_1280x960.jpeg)
*来源：Eaton*

在这些柜体内部，你会发现以下设备：

- [断路器](https://en.wikipedia.org/wiki/Circuit_breaker)：一种电气安全装置，设计用于在电流过高时切断电流、防止火灾。
- 计量组件与继电器。
- 一台电流互感器和一台电压互感器：它们与断路器和计量设备协同工作。
- 一个用于接通或切断电源的开关。
- 中压电缆。

![](https://substack-post-media.s3.amazonaws.com/public/images/9dcee20b-1071-4738-8c18-2c9e0eac64bd_1080x883.png)
*来源：Schneider Electric*

如上所述，中压（MV）开关柜会将 33kV、22kV 或 11kV 的中压电力输送到中压变压器。此时，我们在物理上已经非常接近实际的 IT 机柜：虽然电流要高得多（4000-5000A），但低压（LV）电缆带来的功率损耗不会很高。随后电力由低压（LV）配电柜分配——这是一种与上述中压装置非常相似的工厂组装柜体，同样装满了保护（断路器）、计量和分配电力的设备。

每台低压变压器旁都配有一台功率等级与之匹配的发电机，在变压器或变压器上游电源发生故障时顶上。自动切换开关（ATS）——通常是低压配电柜的一个组件——用于在这种情况下自动切换到发电机（超大规模园区中每台 2-3MW）作为主电源。

作为参照，一台 3 MW 发电机的功率超过 4,000 马力，与一台机车引擎相当，而在一座超大规模数据中心中配备 20 台以上这样的机组是常有的事！这些机组通常烧柴油，天然气是主要的替代燃料。数据中心通常储备满负荷运行 24 至 48 小时的燃油，柴油在运输和储存上的便利性使其常常成为首选。柴油的能源效率也更高，但污染更大：受监管约束影响，柴油发电机往往更贵，因为需要专门设备来减少环境污染。

![](https://substack-post-media.s3.amazonaws.com/public/images/07006bcf-2569-43b7-a8e5-1a1b1f5f3de8_2022x1062.jpeg)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/99300db6-1413-4188-83e3-a1db62958415_2456x1294.jpeg)
*来源：Data Center Frontier*

自动切换开关（ATS）的正下游是不间断电源（UPS）系统，用于确保供电永不中断。这些设备包含电力电子器件，并连接一组电池以保证持续的电力供应：发电机一般需要约 60 秒才能启动并达到满容量，而且和你的汽车引擎一样，它们偶尔也会一次打不着火。UPS 系统的职责就是填补这一空档，其响应时间通常低于 10ms，采用以下组件：

- 逆变器：通常基于 IGBT 功率半导体，将电池的直流电转换为数据中心使用的交流电。
- 整流器：将交流电转换为直流电，使 UPS 得以为电池组充电——电池必须保持充满电，以确保电力持续供应。
- 电池组，铅酸或锂电。铅酸电池正被锂电池取代，不过后者必须遵守严格的消防规范。
- 静态旁路开关：如果 UPS 发生故障，负载将自动切换到主电源。如果 UPS 需要停机维护，也可以手动切换负载。

![](https://substack-post-media.s3.amazonaws.com/public/images/cb167556-06e3-49ca-89a5-c7920dcea7ae_1844x1362.png)
*来源：Vertiv*

UPS 可能是低效的一大来源，典型损耗为 3-5%，且在低负载时进一步加剧。现代设备可以通过待机模式运行（下图中的「VFD」）并绕过 AC-DC-AC 转换，将效率提升到 >99%，但这会使切换时间增加几毫秒（ms），并带来短暂断电的风险。

![](https://substack-post-media.s3.amazonaws.com/public/images/9826c37c-197a-4525-9110-23e1bd369a7a_2292x1150.png)
*来源：Vertiv*

现代系统是模块化的：它们不再是一台固定尺寸的大单元，而是拆分为更小的「核心」（core），可以堆叠在一起并作为一台设备协同工作。在 Vertiv 最新的产品中，每个核心为 200kVA 或 400kVA——作为对比，一辆 Tesla Model 3 的逆变器可输出 200kW 交流电。在模块化 UPS 中，单台设备最多可堆叠十个核心——并且最多八台设备可以并联运行以进一步提升容量，最大可达 27MW。

![](https://substack-post-media.s3.amazonaws.com/public/images/65d7d2b6-03b2-4b4d-ae3b-05af5c418300_2310x1266.jpeg)
*来源：Vertiv*

对于 Rated 3 数据中心，UPS 系统采用 2N 冗余（即「2N 配电」）是典型做法。PDU 等下游组件同样为 2N，从而实现「可同步维护」的设施。

![](https://substack-post-media.s3.amazonaws.com/public/images/daafa512-1afc-41b4-8f70-582b752acd80_1644x1070.png)
*来源：Schneider Electric*

但超大规模云厂商通常使用 4N3R（四套设备可用、正常运行只需三套）或 N+2C（又称「Catcher」）等方案，来提高 UPS 负载利用率（更高的效率）并降低每 MW 的资本开支。

在 Catcher 方案中，我们不再配置两台各自能够承担全部负载的 UPS 系统（下例中为 2*3MW），而是采用 N+1 设计，配备多台较小的 UPS（3*1MW）外加一台冗余单元。我们使用静态切换开关（STS）在某台 UPS 发生故障时瞬间将负载切换到另一台——STS 依靠电力电子器件而非机械部件，比 ATS 快得多。在 4N3R 中，我们从配电一直到背板（即从供电甩线一直到发电机和变压器）使用四套独立的电力系统，其中正常运行只需要三套。

不过 2N 配电最容易理解，运营 Rated 3 数据中心的零售型和批发型托管运营商普遍采用。在 2N 配电中，两套独立的配电系统（从 UPS 一直到甩线）分别被称为 A 侧和 B 侧，一旦某一侧因任何组件故障而供电中断，IT 机柜可以使用另一侧供电。

![](https://substack-post-media.s3.amazonaws.com/public/images/83edbda0-b64c-4c67-8932-cca8dc685d4f_2452x1328.jpeg)
*来源：SOCOMEC*

现在 UPS 电力已进入数据大厅内部，在把电力送到我们的 CPU、GPU 和其他 IT 组件之前，还有几件设备。接下来我们将探讨 IT 机柜的典型布局，以更好地理解这一切如何运转。

机柜通常彼此相邻排成一行。在下图中，每个房间有六排机柜、每排 26 个，当然这一数字会有很大差异。

![](https://substack-post-media.s3.amazonaws.com/public/images/3e3903d2-6a2b-471c-a38e-47404b226572_1334x1206.png)
*来源：Schneider Electric*

电力通过架空母线槽——一根通常为铜的固态导电金属排——或软性电力电缆进行分配。在上面的例子中，一条主「房间」母线槽向更小的「列」母线槽配电，每排机柜配有三条。

使用母线槽时，需配合配电单元（PDU）和远程配电盘（RPP），利用母线槽对单列和单个机柜进行管理、监控和配电。挂接在每个机柜上方母线槽上的插接单元（tap-off unit）通过甩线（whip）向机柜供电——甩线是从插接箱敷设到机柜内电源或机柜内电源架的软电缆。

![](https://substack-post-media.s3.amazonaws.com/public/images/aa204910-d943-4c4c-9052-c3271c032846_2560x818.jpeg)
*来源：Vertiv*

使用软性电力电缆时，则使用机柜外部的配电单元（PDU），它同样负责配电，并包含各个机柜的断路器。这些软性电力电缆随后直接敷设进每个机柜。

![](https://substack-post-media.s3.amazonaws.com/public/images/7b7b247e-e8f0-491e-a89e-2519fd27dc9c_2560x758.jpeg)
*来源：Vertiv*

这是实现同一目标的两种不同方案：安全地向服务器分配低压电力。PDU 和母线槽都集成另一套断路器和计量设备。

传统数据中心倾向于使用软电缆和 PDU，但当涉及大功率和高密度时，母线槽往往是首选方案，多年来已被超大规模云厂商广泛采用。为实现冗余，母线槽成对使用，由独立的 UPS 系统供电，并且每个机柜通常配有两个母线插接单元——A 侧一个、B 侧一个，代表 2N 配电冗余方案中的两套独立配电侧。

![](https://substack-post-media.s3.amazonaws.com/public/images/d7962c94-e3f3-4b00-b456-3e6439c52c24_2560x1440.jpeg)
*来源：Datacenterknowledge*

在机柜内部，我们常使用下图所示的垂直 PDU。我们在机柜两侧各装一个，A 侧一个、B 侧一个，以实现 2N 配电冗余，从而不存在单点故障。

![](https://substack-post-media.s3.amazonaws.com/public/images/f38bb5ab-d88b-48ee-ac34-56cf08943495_1678x940.jpeg)
*来源：Vertiv*

## OCP 机柜与 BBU

以上描述的是数据中心典型的电力流向，但超大规模云厂商在追求效率的过程中，常常偏离典型部署。一个绝佳的例子是 Meta 十年前推出的开放计算项目（OCP）机柜。

在 OCP 架构中，不再由机柜内垂直 PDU 向每台服务器输送交流电（每台服务器各自带整流器将交流转换为直流），而是由集中的电源架（Power Shelf）负责这一步，为整个机柜完成交流到直流的转换，并通过母线向服务器供应直流电。电源架通常是模块化的——在下面的例子中，我们可以看到每台设备有六个 3kW 模块。OCP 设计要求定制服务器设计：包含一个用于连接直流母线的卡夹（bar clip），并且服务器内部没有整流器。

![](https://substack-post-media.s3.amazonaws.com/public/images/32392932-e625-4042-8a19-19c18464def7_707x1024.jpeg)
*来源：StorageReview*

电源架还可以集成电池备份单元（BBU），锂电池可支撑几分钟的负载，充当「机柜内 UPS」，从而省去任何中央 UPS。绕过中央 UPS 之后，效率得到提升，因为电池的直流电可以直接供给 IT 设备。

这还有一个好处：将数据中心所需的总电池容量削减一半，因为不再需要 A 侧和 B 侧两套 UPS，只用单个机柜内电池作为备份。这种做法的缺点是，在机柜内放置锂电池需要先进的消防灭火方案以满足消防规范，而在中央 UPS 系统中，所有电池都可以隔离在一个防火房间里。

![](https://substack-post-media.s3.amazonaws.com/public/images/91294240-913b-45b9-b53b-c552e7bf9939_1528x1128.jpeg)
*来源：Schneider Electric*

为进一步提升效率，Google 引入了 48V 母线，详见我们关于 AI 加速器 VRM 的[报告](https://semianalysis.com/energizing-ai-power-delivery-competition)中的详细解释。

![](https://substack-post-media.s3.amazonaws.com/public/images/1d45b8fa-f8c5-440f-9986-0e7ee999713a_3427x1905.png)
*来源：Google*

现在让我们探讨 AI 数据中心的崛起将如何影响设备供应商格局和数据中心设计。我们也将解释为什么 Meta 如此仓促，甚至决定拆除在建设施。

## 逼近传统数据中心的极限

生成式 AI 以前所未有的规模带来新的计算需求，显著改变了数据中心的设计与规划。第一个大变化是功率：正如我们的[数据中心能源](https://semianalysis.com/ai-datacenter-energy-dilemma-race)、[100k H100](https://semianalysis.com/100000-h200-clusters-power-network)和[吉瓦级多数据中心训练](https://semianalysis.com/multi-datacenter-training-openais)报告所解释的，AI 的电力需求正以极快的速度增长，明年每设施 50MW+ 将不再够用。

第二个重大变化是计算密度。正如我们多年来深入讨论的那样，网络是扩大集群规模的关键一环。这在资本开支（CapEx）上是一项重大成本项，但更重要的是，设计不当的网络会显著降低你那些昂贵 GPU 的利用率。

通常而言，在一个大型集群中，[我们希望在纵向扩展网络和横向扩展网络中都尽可能多地使用铜](https://semianalysis.com/nvidias-optical-boogeyman-nvl72-infiniband)。用铜质电缆进行通信可以避免使用光纤收发器——后者成本高昂、消耗电力并引入延迟。但在极高速传输时，铜的传输距离通常至多只有几米——因此，GPU 之间必须尽可能靠近，以便通过铜介质进行通信。

AI 影响计算密度的最佳例证是下图所示的 Nvidia 最新机柜级 GPU 服务器：GB200 家族。我们曾[在此处](https://semianalysis.com/gb200-hardware-architecture-and-component)发布对其架构的全面分析。NVL72 版本是一个由 72 块 GPU 组成、总功率达 130kW+ 的机柜。所有 GPU 通过超高速纵向扩展网络 NVLink 互连，[与 H100 相比，最大的语言模型推理性能吞吐量提升 9 倍](https://semianalysis.com/ai-cloud-tco-model)。

回到数据中心功率：这里的关键数字是每机柜 130 kW+。这与过去有多大不同？只需看看下面的图表：平均机柜密度过去通常低于 10kW，而 Omdia 预计到 2030 年将升至 14.8kW。Omdia 的数字即便从历史角度看也是错的，而且未来这个数字会高得多。

![](https://substack-post-media.s3.amazonaws.com/public/images/2822f5dd-8841-4e33-98c7-8c2ef3027979_1868x926.jpeg)
*来源：Vertiv & OMDIA*

超大规模云厂商的机柜密度差异很大，且因建筑类型而异。总体而言，Meta 的密度最低，在 10kW 量级；而 Google 的机柜密度最高，通常超过 40 kW。

## 为什么 Meta 不得不废弃一座数据中心

回到开篇：Meta 拆除了一栋在建建筑，因为那是他们沿用多年的旧数据中心设计，功率密度偏低，取而代之的是他们全新的 AI-Ready 设计。

![](https://substack-post-media.s3.amazonaws.com/public/images/b40f9fa0-199c-4938-b4aa-1ef41d94b18a_2542x822.jpeg)

功率密度，连同我们将在第二部分探讨的冷却，是促使 Meta 做出如此急转弯的关键原因。Meta 的参考设计即「H」楼，与竞争对手相比功率密度低得多。虽然超大规模云厂商不公布其建筑的精确 MW 容量，但我们可以利用许可数据、公用事业申报文件和其他数据来源进行估算。

![](https://substack-post-media.s3.amazonaws.com/public/images/5907c766-6a48-4ecc-b5e7-b0ddf5703e7d_2082x958.jpeg)
*来源：SemiAnalysis 数据中心模型*

我们的[数据中心模型订阅用户](https://semianalysis.com/datacenter-model)可以获得完整细节，但作为一个极简化的经验法则，我们可以直接数发电机。一座 Meta「H」楼最多有 36 台发电机，相比之下 Google 为 34 台。但 Google 使用更大的发电机，且其每栋建筑的面积不到「H」楼的 1/2。就功率密度而言，按每平方英尺 kW 计算，Google 是 Meta 的 3 倍以上。此外，由于体量庞大、结构复杂，一栋「H」楼的建造周期很长——从开工到完工约两年，而 Google 的建筑只需 6-7 个月。

「H」楼自有其优点，其中最显著的是能效（第二部分讲冷却时详述），但在生成式 AI 军备竞赛中，它与其他超大规模云厂商相比是一个关键的竞争劣势。

接下来，让我们讨论数据中心规模上的赢家和输家，并展示我们按组件划分的数据中心资本开支拆解。

## 如何建设下一代 Blackwell 数据中心——赢家与输家
