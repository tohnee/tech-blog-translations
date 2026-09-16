---
title: "LEGO 积木式数据中心的「狂野西部」"
title_en: "The Wild Wild West Of LEGO Datacenters"
subtitle: "人人都说自己模块化，厂商的说法站得住脚吗？扎克伯格的帐篷建筑、AWS 的 Houdini、追踪中的 60GW+ 模块化产能、完整厂商版图绘制、Vertiv 每 MW 价值量翻倍"
date: 2026-07-29
source: https://newsletter.semianalysis.com/p/the-wild-wild-west-of-lego-datacenters
crawled: 2026-09-15
authors: ["Nicolas Bontigui", "Eric (Junqi) Wen", "Jeremie Eliahou Ontiveros", "Nigel Chiang", "Reyk Knuhtsen", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# LEGO 积木式数据中心的「狂野西部」

> 原文：[The Wild Wild West Of LEGO Datacenters](https://newsletter.semianalysis.com/p/the-wild-wild-west-of-lego-datacenters) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**人人都说自己模块化，厂商的说法站得住脚吗？扎克伯格的帐篷建筑、AWS 的 Houdini、追踪中的 60GW+ 模块化产能、完整厂商版图绘制、Vertiv 每 MW 价值量翻倍**

# 劳动力难题，模块化来救场

今天我们来深入数据中心建造的世界，因为如今数据中心的建法，与这个行业历史上的做法已经几乎没有相似之处。混凝土墙以成品墙板的形式运抵现场，机电设备房间出厂时就已布好线，有时甚至整个数据大厅都是用卡车整车运来的。世界上一些最大的数据中心，如今越来越多地用你拼装新版蜘蛛侠 LEGO 积木的方式来组装——只不过这些「积木」重达 50,000 磅，而且要复杂那么一点点。这就是模块化建造的世界。

从超大规模云厂商（Hyperscaler）到托管数据中心（Colo）厂商，再到现在甚至包括 AI 实验室，模块化建造已经成为快速建设的默认打法。我们的模块化追踪器（Modular Tracker）收录在 SemiAnalysis [工业模型（Industrials Model）](https://semianalysis.com/industrials-model/)中，追踪到超过 61GW 的模块化产能，以及 1,000 多个采用某种形式模块化或预制化策略的站点。按模块化类别和设备类型的完整拆解同样收录在[工业模型](https://semianalysis.com/industrials-model/)中。我们估计，到 2028 年底，模块化渗透率将达到总在运产能的 30% 以上。

![](https://substack-post-media.s3.amazonaws.com/public/images/33c16231-6f3d-4c90-b750-cdee249d56f4_3354x2153.png)
*来源：SemiAnalysis Industrials Model*

超快速的模块化设计正日益成为常态。[一年多前，我们率先指出 Meta 转向「帐篷」建筑的激进转变](https://newsletter.semianalysis.com/p/meta-superintelligence-leadership-compute-talent-and-data)。如下图所示，AWS 如今也正在以非常大的规模铺开自己的模块化设计，代号「SAMDC」。

![](https://substack-post-media.s3.amazonaws.com/public/images/72654e35-b473-44d9-83d5-93bfd3ffda27_3114x2171.png)
*来源：SemiAnalysis Industrials Model*

要理解背后的原因，我们需要先来看一个单靠资本主义激励无法突破的结构性瓶颈：劳动力。

我们最近的一系列文章，正是朝着这个瓶颈一步步逼近。在[《太空数据中心的可行性论证》](https://newsletter.semianalysis.com/p/to-boldly-go-the-case-for-space-datacenters)中，我们展示了地面产能的天花板。上个月，在[《别再说 2026 年美国数据中心产能有一半被砍了》](https://newsletter.semianalysis.com/p/stop-saying-half-of-2026-us-datacenter)中，我们论证了大多数瓶颈其实被误读了，而且是可以解决的。技工劳动力是个例外，因为电工和管道工的短缺没法快速解决。对这类人才的争夺早已成为真正的约束——当 Crusoe 这样的运营商把工资上调 30% 来为 Abilene 项目吸引人才时，这一点显露无遗，该项目在高峰期需要超过 9,000 名工人。

![](https://substack-post-media.s3.amazonaws.com/public/images/c13c3a8e-bc45-4188-8596-978dd543a131_3450x1920.png)
*来源：SemiAnalysis Industrials Model，美国人口普查局（US Census Bureau）*

为了按工种量化劳动力短缺，我们现在把劳动力模型（Labor Model）也纳入了[工业模型](https://semianalysis.com/industrials-model/)。它把[我们的数据中心模型](https://semianalysis.com/datacenter-industry-model/)中按州拆分的建设规模，转换为每个工种的需求小时数，并与可触达的劳动力供给进行对照。为了在模块化登场之前先把问题框定清楚，下图剔除了模块化建造的影响：劳动需求曲线假设每 GW 所需劳动力在预测期内大致持平，尚未反映我们将在本文后文介绍的那些收益。而各州可触达的劳动力供给，则受其他州在建产能规模和劳动力被虹吸程度的影响。

![](https://substack-post-media.s3.amazonaws.com/public/images/d044c040-2aab-4ab9-aa65-be81bd574ece_2200x1240.png)
*来源：SemiAnalysis Industrials Model*

电工是最典型的例子，他们占到一个数据中心项目总施工工时的 30-40%。下图显示，在关键任务型（mission-critical）需求的巨大拉动下，预计电工短缺将于 2027 年显现。分州来看，短缺在建设最集中的地方最为严峻，比如得克萨斯州和俄亥俄州。

![](https://substack-post-media.s3.amazonaws.com/public/images/936d8787-b1b0-42eb-a95c-7dee8af1e844_2400x1380.png)
*来源：SemiAnalysis Industrials Model*

各方的应对是：如今每一家运营商和厂商都在全力冲向模块化——其本质是把可重复的工作从现场搬进工厂，从墙板到电力房间、再到冷却橇装设备，一切都在工厂里与现场施工并行制造，并以成品单元的形式交付。而且，它不仅能缓解劳动力紧张，还承诺大幅提升速度、缩短建设周期。而在今天，速度就是收入。

这一转变已经在发生：Compass 和 Switch 是最早把部分数据中心建设环节搬到场外的运营商。如今对每家运营商来说，电气设备采用某种形式的橇装方案已经相当标准化。AWS 的 Project Houdini 把白空间的建设环节预制化，把服务器进场前的准备时间从数月压缩到数周。Meta 正在搭建覆膜式的「帐篷」大厅。而在 OEM 和系统集成商两个阵营，都有一波新玩家专门围绕模块化来打造业务。

在这篇深度解析中，我们针对 Vertiv、Schneider 等厂商宣称的一些速度与成本数据，自下而上重建了模块化的商业案例，发现模块化建造可以把建设周期压缩约 36%（即 7-9 个月），按资本开支/MW 计算便宜约 8%。我们还分析了 Vertiv 这类厂商如何通过提供全栈解决方案扩大单个项目的价值捕获：从历史上约 $3.5M/MW 的价值量（content），借助模块化解决方案提升到约 $7M/MW。

![](https://substack-post-media.s3.amazonaws.com/public/images/a6a4ecdf-f99a-41bc-a676-b72206c25bdc_2912x1464.png)
*来源：SemiAnalysis Industrials Model*

但问题在于，如今似乎什么都叫模块化，而厂商、EPC 和托管数据中心商在很多情况下说的完全是不同的东西。为了给这片「狂野西部」带来一点秩序，本文拆解了模块化到底意味着什么。我们绘制了厂商版图，构建了一个包含 80 多家玩家的模块化宇宙，并检验厂商的宣传是否站得住脚。

面向订阅读者，我们聚焦主要受益者，逐一拆解每家玩家的卡位——从上市公司（FIX、STRL、PWR、VRT、SU、FLEX……）到 Infra Partners、Bladeroom、Faith Technologies 等私有挑战者，并提炼我们近期[核心研究](https://semianalysis.com/core-research/)订阅报告中关于 [Comfort Systems](https://semianalysis.com/institutional/comfort-systems-modular-capex-is-the-moat/)：*《模块化产能就是护城河》（Modular Capex Is The Moat）*，以及 [Sterling Infrastructure](https://semianalysis.com/institutional/sterling-infrastructure-winning-where-it-counts-quadrupled-tam-via-texas-pacific-northwest-and-the-midwest-2x-content-per-mw-from-cec-attach-6b-order-run-rate-in-view/)：*《赢在关键处：凭借得州、太平洋西北与中西部把 TAM 扩大四倍；借 CEC 并入实现每 MW 价值量翻倍；约 $6B 年化订单在望》*的关键洞察。

*首先，我们要感谢 [QTS](https://q.com/)、[EdgeConneX](https://www.edgeconnex.com/)、[Aligned Data Centers](https://aligneddc.com/)、[Schneider Electric](https://www.se.com/ww/en/)、[Applied Digital](https://www.applieddigital.com/)、[DG Matrix](https://www.dgmatrix.com/)、[Aran Industries](https://aranind.com/)、[Karman Industries](https://www.karmanindustries.com/)、[Radiant](https://radiant.co/) 以及 Rajat Bhagat 在这篇深度解析撰写过程中提供的贡献与洞察。*

# **模块化的分类学**

![](https://substack-post-media.s3.amazonaws.com/public/images/83a11e81-c993-45dd-b237-a716280c1f75_4704x3228.png)
*来源：SemiAnalysis Industrials Model*

在进入详细分类之前，先从基本定义说起，因为有两个概念经常被混为一谈：预制化（prefabrication）与模块化（modularization）。

- **预制化（Prefabrication）**是更宽泛的概念：任何在工厂制造、到场即可安装的建造部分都算。它描述的是工作发生的地点，而不是物品的形态。
- **模块化（Modular）**的口径更窄，指那些真正自成体系的单元（房间、箱体、区块），它们以完整形态出厂，在现场栓接拼装。每个模块化单元都是预制的，但预制的东西未必是模块。

![](https://substack-post-media.s3.amazonaws.com/public/images/48bf0f7a-3e0d-432a-acb1-3d23459c76ec_2240x944.png)
*来源：SemiAnalysis Industrials Model*

请记住这个区分，它是下文一切内容的主线。接下来，我们将按照数据中心实际的建造顺序走一遍整个版图，然后自下而上地详细拆解构成模块化市场的分类体系。

## **理解数据中心的构造分层**

宏观来看，一个数据中心可以简单地看成三层堆叠：场地（Site）、外壳（Shell）和系统（Systems）。

最底层是场地，即数据中心建设所依托的物理土地。场平、布线和地基施工都发生在这里。这一层无法模块化，因为你必须真实地在一片土地上破土动工，并在现场浇筑地基。

其上是外壳，即作为整个数据中心骨架、并为其遮风挡雨的结构、外皮与屋面。外壳之内安放的是所有设备与子系统，包括全部暖通与电气系统。

![](https://substack-post-media.s3.amazonaws.com/public/images/9c94a890-e7ae-45f6-9524-7e4b459b869b_2080x960.png)
*来源：SemiAnalysis Industrials Model*

鉴于场地本身无法物理移动，预制化策略都集中在另外两层上。我们就按这个顺序来讲，由外向内。

## **数据中心外壳的模块化**

外壳是撑起数据中心、隔绝天气的结构、墙体与屋面。它大体有两种做法：一种是框架加外皮（frame-and-skin）设计，结构与外挂墙板相互独立；另一种是承重墙板设计，把两者合二为一。

传统建造中，外皮和框架都需要在现场成型：施工队破土、浇筑地基，然后在大楼所在之处支模、养护混凝土，一段一段地完成。模块化外壳的起点相同——也是一个现场浇筑的地基——但从那之后，结构件和墙板都是从工厂运来的成品，到场后吊装、栓接到位。

![](https://substack-post-media.s3.amazonaws.com/public/images/48f56864-6591-4d77-9e20-396ff5c542f8_1280x500.png)
*来源：SemiAnalysis Industrials Model*

从上图可以直观看出时间上的节省。在传统的现浇施工中，每一段混凝土必须达到约 75% 的设计强度，下一段才能继续施工。预制结构件则完全绕开了这段等待。

不过，演进并没有止步于把同一栋传统建筑搬去预制。如今更大的收益来自对建筑本身的简化：从复杂的多层设施转向可重复的单层大厅，再转向更窄的、专门定制的结构。

#### **第一阶段：预制混凝土让传统外壳工业化**

第一阶段就是上文描述的预制混凝土（precast）。墙板不再在现场支模养护，而是在受控条件下制造，运到现场，再吊装到预备好的地基上。

这并不是什么新鲜事。北弗吉尼亚州多年来大量使用预制混凝土，因为当地施工劳动力早已紧张。CloudHQ 位于 Ashburn 的两层 LC-2 设施是一个代表性案例：它的承重外壳支撑着长长的无柱跨度，结构承载也足以把暖通设备放到屋顶上。

![](https://substack-post-media.s3.amazonaws.com/public/images/0c557b56-64e2-4056-8e48-5756a323ac9e_1600x611.png)
*来源：CloudHQ Datacenter Crogan*

尽管如此，这栋建筑的交付仍然花了大约 18 到 20 个月。预制减少了现场的支模与养护，但其底层的设施仍然是一个大型多层结构。

Tilt-up 混凝土（墙板倾立施工）逻辑类似，只是把墙板浇筑在建筑底板上，而不是在异地工厂。

![](https://substack-post-media.s3.amazonaws.com/public/images/a0d53c91-d115-4f7f-a562-6918d230ba17_1023x627.png)
*来源：DPR Construction 弗吉尼亚州 Ashburn 项目现场的 tilt-up 墙板*

这种方法避免了长途运输，对于大型单层「盒子」来说可能是成本最低的路线，不过质量和工期仍然更容易受现场条件与天气的影响。

#### **第二阶段：给建筑做减法**

第二阶段才是设计变革发生的地方。为了进一步压缩时间，行业开始转向用简化设计来换速度。这类建筑采用规则的结构柱网、更少的建筑造型元素和标准化的外墙板。钢结构往往更受青睐，因为框架可以在厂外加工、高效运输，并在一片平坦的大型园区里快速栓接成型。

轻量端的方案是预制金属建筑（pre-engineered metal building，PEMB），它由三部分构成：

1. 主框架，作为结构骨架；
2. 次框架，把主框架连成整体——这些是更轻的钢构件，比如跨接在主框架之间的屋面檩条；
3. 外皮，注意它和框架是两回事——它们是轻薄的金属墙板，职责是保护室内免受极端天气影响。

![](https://substack-post-media.s3.amazonaws.com/public/images/ca0c2e79-f004-4be7-b272-9750e2d4e799_1920x2560.png)
*来源：Diamond Steel 预制金属建筑安装现场*

这是最快的选项，因为所有构件出厂时已完成切割、开孔和贴标，施工队只需在现场把它们栓接起来。此外，轻钢结构所需的材料也远少于混凝土。

要求更高的大厅则采用结构钢——更重的热轧型钢梁柱在厂外加工，再栓接成刚性框架。它比轻量 PEMB 贵，但能支撑更大的跨度、更重的载荷和更复杂的布局。

QTS 的 Cedar Rapids 园区展示了这条路子能够释放的速度与规模。当前的 420 MW 阶段占地约 280 万平方英尺，用了大约 28,000 吨结构钢。QTS 从破土动工到结构封顶只用了约五个月，整体建筑大约 11 个月交付。

![](https://substack-post-media.s3.amazonaws.com/public/images/3d4ab1fb-268f-4b91-a4b4-b8d35729f005_1710x824.png)
*来源：SemiAnalysis Industrials Model*

外立面再用预制墙板封闭，最常见的是保温金属墙板。类似地，Crusoe 位于 Abilene 的 Stargate 园区也采用了这一做法，每栋建筑用了大约 672 块工厂制造的墙板。这些墙板在 40 天内完成制造，以每天约 15 到 20 块的速度安装，帮助每栋建筑在不到八周内实现外壳封闭（dried-in）。

![](https://substack-post-media.s3.amazonaws.com/public/images/dbb6bdb2-d30d-4dcd-a85e-d59991230758_1200x900.png)
*来源：Crusoe Stargate 园区*

因此，速度优势与其说来自钢材本身，不如说来自钢材所促成的种种可能：简单的单层大厅、可重复的结构柱网、更少的现场接口，以及可以跨市场复制的供应链。与高密度的多层设计相比，它还能降低每 MW 的劳动力与结构材料用量。

主要的代价是土地。单层园区需要更大的占地，但在新兴的 AI 市场中这往往可以接受——那里土地更便宜，部署速度比把每英亩 MW 数最大化更重要。

#### **第三阶段：专用快速部署外壳**

第三阶段更进一步，围绕更具体的部署模式来设计围护结构。更窄、更轻的结构可以减少常规外壳工程量，并支撑更快的重复建造，不过这种更紧的优化也可能给未来的设备或布局调整留下更少的灵活性。

Meta 在 New Albany 的 Prometheus 园区的快速部署结构（rapid-deployment structures）是最显眼的极端案例。这种铝框架、覆膜的大厅无需建造常规的永久外壳，就能提供围护和防风挡雨的能力。每个结构约 125,000 平方英尺，卫星追踪显示，在 2025 年 7 月宣布建设之后，到 2026 年 4 月已有八座矗立起来。

![](https://substack-post-media.s3.amazonaws.com/public/images/3728a388-fef1-4c9b-a890-451ec148878b_624x315.png)
*来源：SemiAnalysis Datacenter Model，Meta Prometheus New Albany 园区的帐篷建筑*

这并不意味着 Meta 在九个月内建成了一座完整的数据中心。帐篷加速的是围护结构，而不是市政并网、供电、冷却或调试。它们还牺牲了永久性混凝土或钢结构建筑的部分耐久性与长期灵活性。

AWS 最新的模块化建设也在朝类似方向走。它不再把外壳当成一座通用的巨型仓库，而是采用围绕内部所装系统来组织的、更窄、更可重复的结构。其结果是每 MW 所需的建筑量更少、结构跨度更短、现场施工队需要组装的接口也更少。

![](https://substack-post-media.s3.amazonaws.com/public/images/90b9184f-8001-4766-9168-690cf77e2593_2419x1137.png)
*来源：AWS 多层设计*

共同的主线是：外壳模块化越来越多地关乎设计简化，而不只是预制化。预制混凝土把混凝土生产搬到了场外，但基本保留了传统建筑形态。标准化钢结构让单层大厅更容易跨市场复制。专用结构则更进一步，直接缩减了外壳本身的尺寸与复杂度。

因此，成本节省来自减少楼层、降低结构复杂度、压缩现场人工，以及在同一园区内重复使用同一套围护方案/供应链。一旦外壳封闭完成，更大的模块化机会就转移到了建筑内部——电力、冷却和白空间系统，正是它们把一个围护结构变成一座投运的数据中心。

## **设备与子系统的模块化**

设备与子系统才是真正模块化的主力所在，产品形态跨度极大：小到单台设备，大到整栋开机即可投用的建筑。此前的深度解析已经非常深入地拆解过[暖通/机械系统](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-2-cooling-systems)和[电气系统](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-1-electrical)的构造。另外，在开始给各类形态命名之前，先统一几个术语：

![](https://substack-post-media.s3.amazonaws.com/public/images/db1a1f19-60c9-4c4a-8ac0-7cc51365b99d_2500x937.png)
*来源：SemiAnalysis Industrials Model*

1. **元件（Component）：** 形态层级的最底层，即工厂制造的单台设备。
2. **橇装（Skid）：** 第一种常见的模块形态。一组元件安装在一个开放式底架上。设备不再分开运输，而是预先排布、配置好，作为一个整体包装出厂。
3. **模块（Module）：** 加了封闭空间的橇装。它可以是一个简单的电力房间，也可以是类似橇装的预制机电房间，但只有当你给它加上墙体和屋顶，它才成为模块。
4. **集装箱（Container）：** 模块的一种特定形式，采用 ISO 集装箱封装。ISO 集装箱专为标准运输尺寸而造，意味着可以用普通卡车不受限制地运往任何地方。
5. **预制数据中心区块（Prefab Datacenter block）：** 设施级的建设方式，把多个工厂建造的模块拼合成一个大得多的设施区块。这些区块的目标是充当端到端的数据中心建设单元。

这就像一架梯子，从 1 到 5，工厂集成度和交付范围逐级递增。仔细看你会发现，前四级通常被称为子系统模块化（subsystem modularization）：供应商把数据中心的一部分作为工厂建造的单元交付。该单元到场时已完成组装和测试，但仍需接入整个设施才能发挥作用。

最后一级（有时也包括第四级）则更接近整设施模块化（whole facility modularization）。此时，供应商交付的是数据中心大得多的部分，而且是一个集成产品。

![](https://substack-post-media.s3.amazonaws.com/public/images/26cb7a1e-a34d-4c56-97c1-0ae098215b76_1431x560.png)
*来源：SemiAnalysis Industrials Model*

## **子系统模块化**

术语在手，我们现在可以开始沿着梯子向上爬了。自然的起点是最底层的子系统模块化——它是两大家族中更大的一个，也是今天市场的主要聚集地。我们先从灰空间讲起，而模块化电力区块正是大多数人讨论模块化设计时最先想到的东西。

### **模块化电力区块**

![](https://substack-post-media.s3.amazonaws.com/public/images/b23b7a03-7d2c-4cd0-b614-42a3ebcfd7ea_1430x842.png)
*来源：SemiAnalysis Industrials Model*

电力模块是工厂建造的电气房间或电力区块，把主要电气设备打包进一个箱体之中。在所有子系统模块里，电力是最适合模块化的领域之一，因为设备阵容定义清晰，而且组装成套需要很多不同的部件。在一个 50MW 电力大厅里，电气安装与调试平均需要 5.5 - 16.7 个月。

举一个例子，下面看看 Flex 通过 Anord Mardix 单元打造的模块化电力解决方案：

![](https://substack-post-media.s3.amazonaws.com/public/images/a172dde8-c1a8-45e3-9f02-4d9738d06016_947x503.png)
*来源：Flex*

Flex 销售两个版本：电力橇装（power skid）和电力模块舱（power module pod）——后者是同一套设备阵容外加一个安全围护结构。房间内，主要电气组件像一套传动链（power train）一样依次排开。

你可能已经注意到，模块里还包含母线槽系统，比如建筑上方连接电力舱与数据大厅的 IBAR 馈线。机房空气处理机（CRAH）和消防系统也一应俱全，用于管理封闭外壳内的空气温度，并防范意外情况。

据我们自己的测算，工期收益主要集中体现在电力区块上。仅把电力部分（按价值量计约占整个建造的 ~26%）搬进工厂，就能让大厅快约 ~22% 达到 IT 就绪——大约 ~13 个月，而传统现场建造（stick-build）为 ~16.7 个月——并且每 MW 便宜约 ~5%，主要途径是把机电安装从约 ~5.5 个月压缩到 ~2.5 个月。

最后，在模块化电力区块内部，一个新的子类正在兴起，我们可以将其定义为「软件定义」的电力路由区块。这类产品不再把传统的「变压器+开关柜+UPS+电池」链条打包进箱子，而是由 DG Matrix 这类公司用基于电力电子的多端口路由替换链条中的部分环节。这些系统能够通过一个统一的可控电力平台连接电网、发电、储能和直流负载。

### **模块化冷却区块与预制冷却基础设施**

![](https://substack-post-media.s3.amazonaws.com/public/images/5bba9e35-78a3-4d66-94c8-de79f4b2acd8_1430x840.png)
*来源：SemiAnalysis Industrials Model*

与电力模块类似，冷却区块把数据中心的冷却回路打包成一个集成子系统。乍一看，冷却的模块化理由不如电力充分，因为需要预装的部件本来就更少。但随着一次侧和二次侧回路日益复杂，以可重复的模块化增量添加冷却能力，对运营商的吸引力就大得多了。

聚焦到 TCS 回路，大多数模块化努力都集中在 CDU（冷量分配单元）橇装上。Airedale by Modine 的橇装式 CDU 就属于这一类（关于冷却系统的更多内容，[请阅读我们的冷却系统深度解析](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-2-cooling-systems)）。

![](https://substack-post-media.s3.amazonaws.com/public/images/18d71a00-7f47-4b7b-8fe1-2d2c4a080714_893x504.jpeg)
*来源：Modine*

Airedale by Modine 的橇装式 CDU 是一个 2 MW 级的单元，出厂时装在一个预制底橇上，该有的全都有：从红银相间的冷却回路，到右上角的缓冲水箱，乃至集成在橇体末端的泄漏检测系统。到了现场，施工队只需接上两个回路接口和一路电源即可。

另一方面，就预制冷却系统而言，价值主张在二次侧回路和室外机械场院上体现得更为充分：管道和其他室外冷却基础设施在工厂预制，能显著减少现场完成的土建、管道和控制工程量。

![](https://substack-post-media.s3.amazonaws.com/public/images/b512bc68-64e0-4b33-9da7-eb25bb700acb_1422x1143.png)
*来源：SemiAnalysis Industrials Model*

谈到冷却设备时要记住，其中很多最初是为医院、校园园区和工业过程冷却设计的，而不是为 GW 级数据中心设计的。在那个尺度上，巨大的占地面积和数百台集中布置的机组可能引发热空气回流和热岛效应等问题。

![](https://substack-post-media.s3.amazonaws.com/public/images/298ec60f-d43c-4a44-8901-693927971231_2400x1600.png)
*来源：Vertiv 的架空式冷水机组/冷却设备，安装在与预制大厅相邻的钢结构平台上，采用机械场院基础设施*

上图的 Vertiv 项目展示了一个常规机械场院。冷却设备作为独立的基础设施位于数据大厅之外，冷水机组、水泵、管道和支撑钢结构围绕建筑组装。

一些数据中心开发商（如 QTS）如今把大部分管道基础设施都做了预制，既加快了安装速度，又保持了高质量。在当下高密度液冷部署对管道需求与日俱增的背景下，这一点显得尤其有价值。

少数新玩家甚至开始对整个场院下手。Karman Industries 基于 CO2 的热处理单元（Heat Processing Unit，HPU）是一个专门定制的单元，从电动汽车借来碳化硅（SiC）电力电子和永磁电机，从航空航天借来紧凑型涡轮机械和先进热交换器。HPU 可按站点配置，以户外级 NEMA 橇装形式出厂，功率密度达到常规方案的 4 到 5 倍，可把场院占地削减 60% 到 80%。

![](https://substack-post-media.s3.amazonaws.com/public/images/07f5c81d-9a0f-4e02-9fb0-6a079bcbde49_1126x703.png)
*来源：Karman Industries*

## **其他可选的模块化部分**

电力和冷却并不是数据中心里仅有的可以搬进工厂的部分。同样的概念可以推广到整个灰空间，比如电池储能系统（BESS）、水处理橇装、消防系统等等。

其中很多并不在建设工期的关键路径上，或者体量小到足以在现场建造。而且，即使这些系统做了模块化，它们往往也是搭在更大的单元里一起交付，而不是单独运输。例如，Schneider 的 EcoStruxure 就内置了消防系统。

### **工厂建造的白空间**

![](https://substack-post-media.s3.amazonaws.com/public/images/24feeb10-afcc-43d3-ad01-baae3bfb3260_1431x816.png)
*来源：SemiAnalysis Industrials Model*

工厂建造白空间模块的意图，是用工厂化的产品替代手工建造的数据大厅和现场人工布线。这意味着运营商可以直接把算力就位，而不需要操心接线与连接问题。

整套产品出厂时已备好机架框架，以及机架运行所需的全部「最后一公里」连接点。可以把它想象成一个为算力准备好的信封：机架位置已经排好，供电与散热的线缆和连接方式已经就绪，机架上方还预装了电力母线槽和技术水回路。

![](https://substack-post-media.s3.amazonaws.com/public/images/1cbdc558-83be-405e-ac77-5440964920ea_2165x543.png)
*来源：Schneider Electric*

以 Schneider 的 EcoStruxure Pod 为例。上图中的黑色机柜构成 IT 机架列，用于安装 Nvidia GPU 服务器等产品，这一套系统最多可放置 40 个机架。机架上方灰色的架空基础设施是分配层，承载着向每个机架供电的母线槽、捕集热空气的气流封闭通道（因为部分方案仍将采用风冷）、分配液冷以带走热量的技术水回路，以及连接每台服务器的线缆。

这里真正有意思的是背后的产品设计。工厂白空间必须能够满足不同的定制需求，因此 Schneider 等供应商与 Nvidia 合作，支持超过 30 种（30+）参考设计。买家基本上只需挑选与自己想要的芯片相匹配的规格，就能得到一个与所需电力和冷却模块预先协调好的大厅。在下一节中，我们将更详细地研究这个设计过程是如何进行的。

## **整设施模块化**

整设施模块化就是字面意义上的「箱中式数据中心」模式。供应商交付的不再是零散部件，而是一个完整或接近完整的数据中心区块。

![](https://substack-post-media.s3.amazonaws.com/public/images/53c5b11d-1a27-4a02-b827-8a8ca6b69b5d_2500x937.png)
*来源：SemiAnalysis Industrials Model*

### **集装箱式数据中心**

![](https://substack-post-media.s3.amazonaws.com/public/images/b58d524c-fb6c-4fe5-9f7e-579425b515bc_1430x842.png)
*来源：SemiAnalysis Industrials Model*

先看集装箱式数据中心，这是形态设计梯子的第 4 级：数据中心本身被打包进 ISO 风格的集装箱或专门定制的防风雨围护结构中。如前所述，这种形态存在的理由就是运输便利。

![](https://substack-post-media.s3.amazonaws.com/public/images/e530d9bf-5ac8-4c91-9e56-07f232123c01_374x248.gif)
*来源：台达（Delta）All-in-One 边缘解决方案*

如上图所示，你几乎可以在箱子里看到一切：IT 机架、电力设备、电池，甚至冷却系统。

这类设计常用于边缘计算、工业环境、偏远或闲置空间，在买家需要快速获得一座较小数据中心时最有用。对于 AI 工作负载，买家通常不是追求规模的算力初创公司，而是需要在固定物理位置获得低延迟推理的资产所有者。

![](https://substack-post-media.s3.amazonaws.com/public/images/e3d57cbd-3cb8-405c-a590-efd9c56a31cd_1200x675.png)
*来源：Flex 的 CrownPod 正被吊装进场*

这种形态的主要局限是密度。让单元便于运输、快速部署的外形，同时也固化了布局。正因如此，供应商正在超越集装箱模式，向一体化预制数据中心区块演进。

### **一体化预制数据中心区块**

![](https://substack-post-media.s3.amazonaws.com/public/images/a300c885-7b79-4999-a283-c7bc7c824b00_1430x842.png)
*来源：SemiAnalysis Industrials Model*

一体化预制数据中心区块是整设施模块化中更进一步的版本。供应商交付的是一个更大的设施区块，数据中心的大部分在交付之前就已集成完毕。

![](https://substack-post-media.s3.amazonaws.com/public/images/de56d565-b8e6-40f4-bc02-ea222bd3062e_1000x1000.png)
*来源：Vertiv*

Vertiv 的 MegaMod 展示了这种模式在实践中的样子。这个结构实际上就是一座模块化数据中心，主要系统全部封装在同一个围护体里。区块中央是安装服务器的 IT 机架；机架上方和四周铺设着光纤和线缆管理通道；沿周边布置的则是冷却和电力单元等全部配套基础设施系统。

该系统的 1 MW 参考设计尺寸可达约 26.5 米长、24 米宽、4 米高，而 MegaMod plus 版本宽度甚至可以扩展到 31 米。你可能会问：这么大怎么运到现场？实际上，这种结构需要拆分成可运输的预制分段，通过标准的重载物流卡车运输，然后在现场连接成一个整体并完成调试。

## **平台化模块化与参考设计**

整设施模块化的最后一步，超越了任何单一厂商的区块，走向设施本身的标准参考设计。就像行业有机架系统和 CDU 的参考设计一样，Nvidia 现在为整座 AI 工厂发布了参考设计：Nvidia DSX。它最初于 2025 年 10 月在华盛顿 GTC 大会上作为 Omniverse 数字孪生蓝图亮相，2026 年 3 月正式定形为 Vera Rubin DSX 参考设计，最近又扩展成了完整的 DSX 平台。

DSX 参考设计是经过验证的 AI 工厂架构，覆盖算力、网络、存储、硬件集群设计，也覆盖设施侧，包括电力、冷却和控制，甚至土建、结构和建筑设计。其背后的价值主张是：Nvidia 的 DSX Max-Q 在固定电力预算内最大化每瓦特 token 产出，而 DSX Flex 则帮助设施接入电网服务，动态调节用电，并通过混合自备发电来编排需求。

![](https://substack-post-media.s3.amazonaws.com/public/images/5e1de1e0-f8b5-468d-9c6b-ca21d1ae6e56_597x335.jpeg)
*来源：Nvidia Vera Rubin DSX AI 工厂*

部署 DSX 设施时，运营商先通过 Omniverse DSX Blueprint 构建设施的数字孪生，实时仿真布局、电力拓扑、热行为和运营策略，在开工之前完成设计优化，然后把同一套经过验证的架构复用到各个站点。例如，CoreWeave 已经在用 DSX Air 构建和测试其 AI 工厂的数字孪生。

此外，整个 DSX 生态几乎涵盖了全部供应链：Cadence、Dassault Systemes、Eaton、Jacobs、Nscale、Phaidra、Procore、PTC、Schneider Electric、Siemens、Switch、Trane、Vertiv 等。例如 Vertiv 的 OneCore 就把电力和冷却打包成标准化的 12.5 MW 舱（pod），可组合成更大规模的 AI 工厂部署。

EdgeConneX 估计，在完成针对具体场地的本地化之前，一套通用设计就能把项目推进到大约 30% 到 60% 的报批文件完成度，从而让大量场外工作得以提前启动。

# 厂商版图

读到这里，你应该对各个品类有了基本的感觉。同时，可能也被一大堆名字搞得有点晕。我们已经把 Flex 的电力模块、Airedale 的 CDU、Schneider 的数据大厅舱和 Vertiv 的一体化数据中心全都摆在了你面前。所以在继续深入之前，不妨退后一步，把整个市场铺在一张地图上。

![](https://substack-post-media.s3.amazonaws.com/public/images/88ea5eee-1d24-497d-a2be-54b6bb9a5c55_2500x2041.png)
*来源：SemiAnalysis Industrials Model*

我们的版图涵盖 80 多家玩家。这样铺开的好处是，有两个模式立刻跳了出来。

1. **深度集中在子系统**：电力房间和冷却模块是竞争最拥挤的领域；
2. **同样的名字在各列反复出现**：因为 Vertiv、Schneider 或 Eaton 这样的厂商同时销售电力模块、CDU、白空间舱和整栋区块。

## **掌控集成：到底是谁在做模块化？**

上面的厂商版图画出了谁在造哪一块，但没有回答这些块如何变成模块、以及出问题时谁来负责。从解决方案的归属来看，答案有三种：

1. 一端是运营商大权独揽：自己定设备规格、直接采购，然后交给集成商纯粹做组装；
2. 中间是 EPC 或集成商主导的建设：运营商仍然定性能要求，但雇 EPC 或集成商来采购、协调和建造；
3. 另一端是 OEM 主导模式：Vertiv 这样的厂商把自家的整套技术栈设计成一个成品来销售，其 OneCore 产品组合就是如此。

![](https://substack-post-media.s3.amazonaws.com/public/images/0115ef28-b275-414a-a678-3115e0f62aff_2500x937.png)
*来源：SemiAnalysis Industrials Model*

### **运营商主导的模块化**

这种模式下，运营商自己编写技术规格，以业主供货设备的形式直接采购，然后交给集成商纯粹做组装。

这种模式要求运营商拥有深厚的内部工程与采购团队来定规格、寻源每一个部件，并愿意承担全部成本、库存和交期风险。

![](https://substack-post-media.s3.amazonaws.com/public/images/62884260-b354-4fff-a504-fdc00e29f23c_2304x892.png)
*来源：SemiAnalysis Industrials Model*

在供给紧张的市场里，这种风险相当尖锐：运营商在争夺稀缺的变压器和开关柜时，没有厂商那种产能配给的议价筹码——除非它的采购规模大到足以自带这种筹码。

这就是为什么运营商主导的模块化实际上只属于最大的那几家超大规模云厂商。例如 AWS 在 Project Houdini 下自行设计预制数据大厅橇装并直接采购设备，同时让 Cupertino Electric 担任设计伙伴。

Aligned 是运营商主导模块化的另一个例子，不过它依赖外部集成伙伴提供制造产能。Aligned 定义架构、业主供货主要部件、掌控调试与质量体系；其集成伙伴则在多个工厂负责收货、仓储、组装和测试。伙伴出厂房和产线，但模块化系统始终是 Aligned 的设计。

### **系统集成商或 EPC 主导的模块化**

EPC 主导的模块化包括系统集成商或建筑公司，它们把大部分第三方设备转换成橇装/模块。集成商负责组装、安装、工厂测试和围护封装，并对向终端客户交付成品橇装负全责。

扮演集成商角色的公司既包括具备集成场地与能力的建筑公司，如 Comfort Systems、Sterling Infrastructure 或 Quanta 旗下的 Cupertino Electric，也包括专业化模块集成商，如 PCX、Nautilus、DXN、Infra Partners、Bladeroom 等。

这类模块化不绑定任何设备厂商，意味着客户对数据中心设计保持更强的控制权，同时承包商把部分施工工序搬进了预制车间。EPC 负责买设备、组装、接线、配管、测试，然后以已完成的施工范围交付发运。

![](https://substack-post-media.s3.amazonaws.com/public/images/af02689f-123a-4dd5-b425-325162c8710d_2304x892.png)
*来源：SemiAnalysis Industrials Model*

以 Comfort Systems 为例。它是一家机电（MEP）承包商，不是设备制造商，因此扮演的是替运营商采购和组装设备的角色。运营商决定要什么设备，剩下的一切由 Comfort Systems 完成。它通过 Environmental Air Systems 和 TAS Energy，在得克萨斯州和北卡罗来纳州超过 350 万平方英尺的车间里运转这些工作。

这个概念对超大规模云厂商尤其有吸引力。大运营商通常早已明确知道自己要什么设备和设计，因此对购买别人的固定系统毫无兴趣。与 Comfort Systems 这类 EPC 集成商合作，运营商保留自己的设计和设备，只是把建造工作从工地搬进工厂。

### **OEM 主导的模块化**

在这种模式下，设备厂商把自家的数据中心基础设施栈变成可复制的模块或平台。虽然产品仍可针对特定站点做配置，但起点通常是采用 OEM 自家架构的标准化模块。

![](https://substack-post-media.s3.amazonaws.com/public/images/5e0f30ec-073c-4bf6-a1c1-eacaf53cf27b_2304x892.png)
*来源：SemiAnalysis Industrials Model*

Vertiv OneCore 是一个典型例子。Vertiv 不再单卖设备，而是把所有层级组合成一个模块化平台。该平台把 Vertiv 的电力、热管理、冷却和 IT 基础设施技术，集成在一个由 Vertiv 供货的钢结构外壳之内。

![](https://substack-post-media.s3.amazonaws.com/public/images/04db66d8-dcf4-43da-a099-03a359a69238_447x447.jpeg)
*来源：Vertiv*

这正是 OEM 主导的本质：客户买的是 Vertiv 的整套集成栈，而不是请 EPC 集成商去拼装设备阵容。这也让 Vertiv 通过端到端出售整套栈来捕获更高的价值量，某些全栈解决方案的 TAM 可扩大至约 $7M/MW。

代价在于产能与执行风险。除了这些公司正沿着价值链进入自己此前并未涉足的市场细分之外，OEM 主导的模块化的扩张速度，也只能跟得上 OEM 工厂产能、供应商体系和集成团队所能支撑的节奏。Vertiv 的模块化方案目前交期超过 12 个月。这也促使大型 OEM——不只是 Vertiv，还包括 Schneider、Siemens 等公司——对产能档期分配越来越挑剔，要求一定的起订规模，并优先大项目。结果是，寻求较小规模产能的运营商或开发商，越来越多地转向系统集成商。

# **模块化周期**

读到这里，读者应该已经熟悉了模块化解决方案的不同形态，以及引领这场变革的玩家们。大家也应该注意到，与传统数据中心建设相比，这一切看起来有多么不同，并且会对运营层面的影响产生许多疑问。这些正是本节要讨论的话题。

![](https://substack-post-media.s3.amazonaws.com/public/images/85b1dd62-b41a-48fe-a5b6-49cba38aa8c5_2400x800.png)
*来源：SemiAnalysis Industrials Model*

## **阶段一：方案设计与仿真**

方案工程化设计是第一步。现场建造时，有些决定可以在施工进行中再调整；而模块化建造则必须提前确定、尽早冻结、并可复制，因为箱体本身必须以最终成品形态出厂。

这一阶段最重要的工程工作发生在设施层面。在模块定型之前，设计团队必须确定负载、选定设备、绘制单线图（SLD）和布局，并用 ETAP、PSSE 等工具完成短路、保护配合和电弧闪光研究。这些分析决定了系统如何选型以及能用哪些部件。由于它们依赖于从市电接入到下游设备的完整电气路径，因此无法在一个孤立的橇体上完成。设施设计必须先行，模块则作为这个更大系统的一部分来设计。

来源：Aran Industries

对于 415/480VAC，这项工作已有成熟模板、可复制度高。但考虑[800VDC 转型的全部影响](https://newsletter.semianalysis.com/p/inside-the-800vdc-revolution-part)时，模板化程度就没那么高了。参考设计虽已有若干，但都还不成熟，设施级架构仍在逐个项目摸索中打磨。这也正是该周期中正在被自动化的环节。Aran Industries 等公司正在开发能接入 ETAP、PSCAD、PSSE、Revit 等设计工具的定制软件，把原本需要多名工程师、耗时数月（>2 个月）的电气设计流程，压缩成几个小时的计算加上一名工程师审阅输出。

### **建设的归属权**

设计确定后，归属问题归结为两个：

1. 谁来选定设备；
2. 谁来承担建设的成本、库存和交期风险。

这些决定并不总在同一个主体手里。运营商可能直接指定某个部件，也可能由集成商选定后报批。

![](https://substack-post-media.s3.amazonaws.com/public/images/74cebb3e-3b9f-4e0a-ae70-5fd1960a1f06_1200x630.png)
*来源：Schneider 的工厂，展示不同模块*

托管数据中心运营商是个干脆的例外。批发型托管商不受任何单一终端用户规格的约束，往往甚至不知道租户会是谁，因此可以自由选择自己想要的设备并尽早下单，无需等待任何人的批准。

即便如此，本地供应可得性仍然重要：开关柜和变压器的交期可能长达 12 到 18 个月，发电机还可能需要满足市场特定的排放法规。定制化也会重新打开工程设计的闸门，增加大约八周时间。

## **阶段二：交付包与文档**

设计在阶段一冻结后，流出设计环节的不是一张图纸，而是一整套文档交付包，由不同主体用不同工具产出：

- **加工制造发包（issued-for-fabrication，IFF）文件包**：包含车间图纸，告诉工厂如何建造橇体；
- **施工发包（issued-for-construction，IFC）文件包**：告诉现场如何接收、就位和连接；
- 单独的**报批与调试文档**：证明设计能够通过规范和测试。

![](https://substack-post-media.s3.amazonaws.com/public/images/303e91b9-6fe8-4cb7-b1a4-4f95deb64445_2400x904.png)
*来源：SemiAnalysis Industrials Model*

这个阶段很大程度上是一场文档与案头的功课。把阶段一的设计模型自动化后，这些交付包可以从同一个数据源生成，而不必手工重画，从而消除各方之间的手工翻图（IFF 与 IFC 面向不同受众——工厂和现场——分开发布；它们不是同一份文件，也不会彼此脱节）。

## **阶段三：模块组装与工厂测试**

一切前置工作完成后，模块还是要实打实地造出来。可以把这一步想象成一条生产线，只是规模是数据中心级别的。组装过程从一个底座、底橇或框架开始，它是模块的基础。然后设备逐层装入，每个部件放进自己的指定区域，就像你拼装一栋 LEGO 积木建筑一样。

![](https://substack-post-media.s3.amazonaws.com/public/images/5450c310-0b3e-4ba8-a843-2f08d95053e7_1000x486.png)
*来源：Flex 的白空间工厂产线*

与组装同步进行的是工厂验收测试（factory acceptance test，即大家更熟悉的「FAT」）。测试分两个层级：第一级在模块组装的每个工位上进行，相当于一道检查关卡，模块过关后才进入下一工位；第二级在模块完工后进行：整台单元上电，按未来在现场的运行方式实际运行，确认额定负载达标、一切安装到位。等到下线时，模块已经完成布线、贴标、密封，并验证过能够独立工作。

![](https://substack-post-media.s3.amazonaws.com/public/images/5609f744-8cd1-456b-8538-1b8be45a95a3_800x600.png)
*来源：Vertiv 工厂验收测试*

工厂测试至关重要。业内常用 1-10-100 法则来描述：在设计或组装阶段花 $1 就能修好的缺陷，进入量产阶段可能要花 $10，而产品发运之后则要花 $100。此外，标准化也让测试可复制，同一套 FAT 程序可以在生产中反复执行。

## **阶段四：模块的交付与安装**

现在，模块要离开工厂的受控环境，闯进现场物流这个不可控的世界。在当今 AI 园区的规模下，让第一个区块上线已经不够，运营商还必须考虑「最后一兆瓦」的投运时间。关键问题变成：有多少成品模块能够运抵现场、有多少能够并行卸货和就位、以及有限的吊装与安装队伍能否高效地从一个区块转场到下一个。

### **深入看：运输与物流**

在我们与数据中心开发商的交流中，物流是设备模块化带来的主要挑战之一。这些橇装和模块个个又大又重，把它们从工厂运到现场绝非小事。正因如此，产能布局和地理位置才如此重要——集成商们正在扩张布局，以贴近客户的站点。

联邦法律规定，免许可运输的界限是宽度 102 英寸、总重 80,000 磅，在标准板车上留给模块本身的重量大约只有 24 吨。微软的 Azure Modular Datacenter 和 Schneider 的 Easy Modular 装在宽 96 英寸的 40 英尺 ISO 集装箱内，因此可以免许可跨越任何州界，或用 C-17 运输机空运。

超过这个界限就需要许可证，但事实上许可费本身影响甚微，真正的代价在工期。一张标准的超限运输许可证每州只要 $15-100；即便是干线运输，按每满载英里 $12-14 计，一车 500 英里的运费也不过每台拖车六到七千美元。

![](https://substack-post-media.s3.amazonaws.com/public/images/3f165e61-54ec-4b94-9534-82ab4641fc5a_1200x675.png)
*来源：Flex 预制模块化解决方案待发运*

在时间上，超过大约 16 英尺的货物就变成「超限大件」（superload），触发桥梁工程审查——每个州 7 到 21 天，一条路线累积下来可达数月，押运还会强制限定通行时段。况且各州门槛并不统一：一个为通过弗吉尼亚州（18 英尺或 250,000 磅才算超限大件）而设计的模块，仍可能踩中俄亥俄州低得多的 14 英尺、120,000 磅红线。

运输本身也成了可靠性体系的一部分。一个模块在路上承受的机械应力可能比正常运行时更大，尤其是振动、制动和装卸过程。在一次验证演练中，Aligned DC 将一个 3 MW 模块从犹他州运到奥马哈再运回来，随车装上力记录仪，测量它在运输途中经历的各种工况。

除此之外，运输还会受保险制约。高价值的 AI 机架可能一次只运一两个，因为把太多设备集中在一辆拖车上造成的承保损失，是任何保险公司都不愿下注的不可接受风险。这种风险并非纸上谈兵——我们听说过这样的案例：一辆载有大型 UPS 模块的卡车在开往北弗吉尼亚的途中，于西弗吉尼亚州的公路上翻车，导致巨额赔付。

把这些因素都考虑进来，运营商们开始围绕运输来反向设计：比如 AWS 把 Houdini 的橇装设计成适配低平板（double-drop）拖车，以便从桥下通过；Nautilus 用驳船把它的数据中心水上漂了 50 英里送到斯托克顿港；Compass 则把一座 Schneider 模块工厂建在了自家 Red Oak 园区旁边。话虽如此，像 DXN 这样的运营商确实也能把集装箱从其位于西澳大利亚珀斯的工厂一路运到美国——不过那大多是较小的集装箱。

![](https://substack-post-media.s3.amazonaws.com/public/images/0bd6be86-de2d-4034-8e8f-a10bef3f39a7_2820x1740.png)
*来源：SemiAnalysis Industrials Model*

模块运抵现场后，必须吊装到预备好的基础上、锚固，并与上游电源和下游负载连接。就连吊车选型都成了设计流程的一部分。履带吊的起重能力随载荷远离吊臂而急剧下降：一台 Manitowoc 18000 在 7.3 米幅度能吊约 600 吨，但在 104 米幅度只能吊约 10 吨。因此模块的重量、吊点和最终落位决定了需要哪种吊车以及吊装成本——通常每天约 $5,000 到 $25,000。举例来说，单个 Schneider 500 kW 电力模块重 50,000 磅，需要六个吊点，而其载荷分布要到造出来才知道。

### **阶段五：现场调试**

模块就位后，就轮到调试了。工厂测试证明的是单个单元，而调试证明的是真实条件下的整个系统。运营商们一致认为，这是模块化周期中最大的单一缺口：一次完整的现场调试端到端要跑 3 到 8 个月。虽然有些厂商声称可以把它搬到场外，但实际上关键部分搬不走，因为主要的能量来源（市电进线、发电机组、BESS）只有在现场才会齐集。

#### **调试的层级**

业内普遍采用六级阶梯，有些框架还会在最前面加一个 Level 0 设计审查。

![](https://substack-post-media.s3.amazonaws.com/public/images/d10e9828-816b-44d2-b224-e5a62c1866d0_1800x1696.png)
*来源：SemiAnalysis Industrials Model*

- **L1 - 工厂见证测试（「红标」）：** 每个橇体或模块在制造商处被证明可以独立运行。这是工厂测试覆盖的层级，也是模块化预先完成的层级。
- **L2 - 到货与安装验证：** 单元在现场被接收、就位、锚固和检查。
- **L3 - 预功能测试/启动（「绿标」）：** 每个系统单独上电并启动。
- **L4 - 功能性能测试（「蓝标」）：** 每个系统对开关柜、冷却回路进行带载运行。
- **L5 - 综合系统测试/IST（「白标」）：** 所有系统在现场同时上电、协同运行，并在模拟故障下考验——A 路侧停电、UPS/STS 切换、水泵故障切换、全楼黑启动。

![](https://substack-post-media.s3.amazonaws.com/public/images/02d31ee5-c418-4fa6-b822-06082f1287b6_937x668.png)
*来源：Hioki 调试步骤*

从 L2 开始，工作就必须在物理现场进行，因为被测试所依赖的能量来源——市电进线、发电机、BESS——只存在于现场。

要想弄清时间到底能从哪里省回来，我们识别出两个抓手。第一，并行化：模块和子系统到场即调试，而不是等全站齐备，这样早期模块的 L2–L4 就能与后续模块的到货重叠，只有 L5 需要等全部到位。第二，让电站自带「负载柜」：电力设备及其电池储能可以在调试期间充当负载柜（load bank），于是不必再卡车运进租来的发电机组和电阻负载柜（测试一结束就得撤走），用来验证电站的那套设备本身留下来成为电站的一部分。

![](https://substack-post-media.s3.amazonaws.com/public/images/f57d19e3-88ed-4ede-beec-5a244ab78361_1000x668.png)
*来源：Electrical Engineering Portal，变电站与中压开关柜调试*

#### **并行工厂调试**

上规模之后，真正的约束通常是 Level 3 的逐点核对（point-to-point）工作，因为每台 PDU、每块控制盘、每个现场设备都必须完成接线、编址、命名，并逐一向楼宇管理系统（BMS）回验。数百台 PDU、每台又有几十到上百个点位，这才是调试的真正瓶颈。为了提速，一些大型数据中心运营商在标准现场流程之外并行开设工厂调试线，在发运前完成设备验证和控制检查（运输之后再重复部分测试），现场团队则保留到货检查、实际并网和综合系统测试。

在研究激进的项目工期宣传时，这一点也必须纳入考量。有些 6-9 个月的工期表，部分就是靠压缩或最小化调试流程实现的。这或许能加快初期通电，但会把风险显著转移到运营阶段。

# **把模块化解决方案的价值主张拿去检验**

所有模块化的推销话术基本都建立在三个主张上：(1) 上市速度；(2) 建造质量与安全性；(3) 总拥有成本（TCO）。宣传数字都很吓人：Vertiv 宣称 MegaMod 模块部署最快提速 50%，SmartRun 最快提速 85%；Schneider 则宣称电力与冷却环节快 60%、初始造价低 13%。

这些数字很大（非常大！），因此我们对照 [SemiAnalysis Industrials Model](https://semianalysis.com/industrials-model/) 中的基准参考数据中心——一座位于美国的 50 MW 液冷 AI 大厅——自下而上重建了整套测算。先给结论：考虑完整建设周期，我们估计模块化建造的施工窗口缩短约 ~36%，全口径成本低约 ~8%。下面拆解这些数字。

![](https://substack-post-media.s3.amazonaws.com/public/images/4ad1bd1f-3c81-4f65-833a-18e7320af078_2912x1344.png)
*来源：SemiAnalysis Industrials Model*

## **速度优势**

速度无疑是厂商的核心卖点。按照前文的分类体系，实际节省的幅度很大程度上取决于你在建设中采用了哪些模块化方案。要理解速度收益从何而来，需要先把建设周期拆成常见的四块：

- **场地工程（Groundworks）：** 4-6 个月，平均约 5 个月。模块化在这一环节除了简化部分垫层和基础工程外，改观不大。
- **结构与外壳：** 2.5-4.5 个月，中位约 3.5 个月。
- **机电安装：** 7-11 个月。今天的基准情形已经包含部分预组装电气设备，比如低压开关柜和 UPS 机列。
- **调试至 IT 就绪：** 3-8 个月，单一大厅中位约 4.5 个月。更长的工期通常反映分阶段、多大厅的移交。

加总起来，一座传统的 50MW 建筑从破土到 IT 就绪大约需要 18 到 24 个月，且这一计时不含报批。除了前述调试方面的考量，一些更快的工期宣传有时也和计时口径有关——往往从机电安装或竖向工程开始计时，而不是从场地工程开始。此外，报批还要增加 12 到 13 个月，且无法与施工重叠，使得全口径工期达到：传统现场建造约 ~30-35+ 个月，模块化约 ~24-30 个月。

下表考虑了运营商全面转向模块化的情形：模块化可以把施工窗口压缩到大约 12-18 个月，比纯现场建造快约 ~36%，比已包含部分模块化的当前基准快约 ~30%。

![](https://substack-post-media.s3.amazonaws.com/public/images/8d2c4802-46e6-40ff-a7bc-60798e936757_1430x393.png)
*来源：SemiAnalysis Industrials Model*

节省幅度与搬进工厂的范围成正比。只采用机电（MEP）橇装的运营商（介于当前基准与全面模块化之间）大约落在 17 个月。部署一体化预制区块或集装箱式数据中心还能把建设窗口进一步压缩到约 12 个月。如今我们甚至能听到 12 个月以内交付的宣传。

![](https://substack-post-media.s3.amazonaws.com/public/images/fd5db78c-8c8e-41ab-8f7f-bd5ab328facf_2912x1464.png)
*来源：SemiAnalysis Industrials Model*

再往深挖：在机电安装阶段，一座 AI 数据大厅每 MW 大约消耗 12,000 个现场工时，其中电气是最大工种。一个标准的 50 MW 大厅把 600,000 个现场工时集中在同一栋建筑里，高峰期堆叠约 300 名技术工人。把这部分机电范围搬进工厂后，现场工时下降约 ~63% 至每 MW 4,500 小时，持证电工工时下降约 85%。工期本身的压缩幅度小于工时降幅，因为搬走的工作现在在工厂里与现场施工并行推进。此外，把工作搬进工厂也降低了对天气和地域条件的依赖。

![](https://substack-post-media.s3.amazonaws.com/public/images/421792de-47ec-456d-9d49-d5899315b7c1_2912x1344.png)
*来源：SemiAnalysis Industrials Model*

**速度就是金钱**

速度就是算力，算力就是收入，所以提前投运的真正价值就是延迟的机会成本。在我们的测算中，经验法则是：如今对云服务商（CSP）而言，每 MW IT 负载一年产生大约 $12M 到 $15M 的收入，即每 IT MW 每月约 $1-1.25M。话虽如此，在如此供不应求的市场里，我们正看到新交易以高得多的公开价格达成——参见 SpaceX 与 Anthropic 的交易，或[我们近期在 Meta 通讯文章中报道过的](https://newsletter.semianalysis.com/p/meta-compute-everyone-wants-to-be)每 IT MW $50M 的收入。Anthropic 或 OpenAI 这样的公司在 API 上每 MW 赚的超过 $50M。

在销售成本（COGS）一侧，相关成本是 GPU 折旧：一个按五年折旧的 Nvidia 集群平均 $30M/MW，约合每月 $500,000/MW。闲置一个月至少损失这部分折旧——GPU 的折旧时钟不管大厅是否就绪都在走——因此我们把提前一个月对业主运营商的价值计为约 $500k/MW，这还是个保守数字，因为投运算力的边际贡献更高。对于从不持有 GPU 的批发托管运营商，提前一个月的价值只是它从此可以开单的租金，约每月 $190,000/MW，大约 $190/kW/月。

![](https://substack-post-media.s3.amazonaws.com/public/images/18483053-f344-4a19-9553-94575ef42deb_2500x1188.png)
*来源：SemiAnalysis Industrials Model*

把这些单位经济模型套用到相对纯现场建造大约 8 个月的领先上，业主运营商在这座 50 MW 大厅上未贴现可捕获约 $200M，即约 ~$4M/MW。

当然，这一切都以「建筑是约束瓶颈」为前提。投运日是三个日期中最晚的那个——建筑就绪、电力到位、GPU 到货——如果卡住进度的不是建筑，加快建筑速度就一分钱也赚不到。

## **TCO 优势**

与实实在在的速度收益相比，资本开支的节省并不算大。我们估计，同一座全面模块化的 50 MW 液冷大厅全口径成本低约 ~$1.1M/MW——约 ~$13.5M/MW 对约 ~$14.6M/MW——差距刚好不到 ~8%。

看数据中心设备的全口径价值量/MW，可以把它拆成硬件成本与服务或安装成本。硬件本身变化不大：无论装在现场砌筑的房间里还是集成到工厂橇体里，开关柜、UPS、变压器等核心硬件的价格是一样的。总节省主要来自两个地方：人工部分和更短的建造周期。

![](https://substack-post-media.s3.amazonaws.com/public/images/6ade310f-6211-4cfb-8f98-e15b5b7c3ae3_2912x1464.png)
*来源：SemiAnalysis Industrials Model*

我们估计，把机电工程搬进工厂可在施工服务上节省约 $0.6M/MW，在安装上节省约 $0.5M/MW。工资差距其实很小：美国劳工统计局（BLS）数据显示现场施工为 $34/小时，工厂为 $33/小时，不过加班和现场补贴把现场电工的实际时薪推高到约 $63/小时。真正的杠杆是更高的工厂产出效率，直接省掉一整块的现场工时。

第二是工期缩短的效应。更早锁定工厂成本、压缩现场周期，可以削减涨价、应急准备金、变更签证和现场开办费。

![](https://substack-post-media.s3.amazonaws.com/public/images/ef46db90-85cb-4744-9167-ac9ea243a3ea_1430x734.png)
*来源：SemiAnalysis Industrials Model*

与这些节省相对，模块化也有一些惩罚项，其中最大的是双重利润。现场建造只对安装内容加价一次，经由总包及其分包。模块化建造则在现场集成商的利润之上，又叠加了一层独立模块厂商的利润。当 OEM 同时也在现场做集成时，这一层会被压缩——Vertiv 和 Schneider 的交钥匙项目就是如此。Schneider 的 WP163 文档展示了这种动态：模块硬件比传统方式高约 40%，但计入设计与安装人工节省后，初始造价净低 13%。

![](https://substack-post-media.s3.amazonaws.com/public/images/6bb77f0f-01f9-4a9d-80ed-5486e4254f8d_1051x652.png)
*来源：Schneider*

另外还有两项较小的惩罚：一是模块溢价（底盘、加强撑、额外互联件、运输和吊装），二是从厂商视角看的额外工厂负担。

![](https://substack-post-media.s3.amazonaws.com/public/images/f5199a1d-0473-4b32-afd3-7e2e71d08888_1430x393.png)
*来源：SemiAnalysis Industrials Model*

## **质量与可预期性优势**

工厂一次通过质量——即无需返工即通过的测试与检验点位占比——在模块化方案中应能超过 95%，而现场基准只有 60-70%，这要归功于工厂里固定的工作指导书。收益是系统可预期性。Flex 把这一点定义为设计选择，并通过设计失效模式与影响分析（DFMEA）来工程化产品化配置，对项目定制配置则执行面向制造（DFM）和面向装配（DFA）评审。

但话说回来，近期的交流也指出了另一面：一些运营商和机电承包商声称，模块化方案已暴露出可靠性问题，没能兑现当初的宣传。这最终意味着不仅把最初抢下来的时间全部赔回去（还得派现场团队进驻），更严重的是让宝贵的硬件处于风险之中。

## **重新审视厂商的宣传**

我们得出的约 ~36% 时间节省（约 8 个月）恰好略高于 Flex 公布的整项目 30%+ 的下限。要做公平比较，必须考虑厂商的数字通常来自更窄的范围或复合口径，而非端到端的建设用时。Vertiv 85% 的 SmartRun 宣传针对的是架空母线槽与气流封闭系统；MegaMod 的 50% 针对的是模块部署与现场建造的对比；Schneider 的 60% 则针对电力与冷却模块。

![](https://substack-post-media.s3.amazonaws.com/public/images/6666639d-e2a7-43a2-b99c-0d031ac2a764_2912x1344.png)
*来源：SemiAnalysis Industrials Model*

# **如今运营商和开发商都在模块化什么**

纵观整个市场，运营商和开发商并没有收敛到同一种模块化策略上。

## **超大规模云厂商**

超大规模云厂商最常建造自有机群、垂直整合建设过程，并围绕自身实际工作负载来设计数据中心。正因如此，超大规模云厂商往往展现出创新者特质，拥有领先的试验性布局。

**AWS**

AWS 展示了当前最快的规模化建设，到 2025 年底新增了近 3.9 GW 产能。Project Houdini 是其对模块化模式最大的一次内部尝试。AWS 没有从零设计一栋模块化建筑，而是把标准的数据大厅图纸重新切分成约 45 英尺长、重约 2,000 磅的工厂预制橇装，可用低平板拖车运输。这让 Houdini 明确归入「工厂建造白空间」这一类。

![](https://substack-post-media.s3.amazonaws.com/public/images/1ea8619f-2321-4e42-bc73-a2e419c631d7_1170x633.png)
*来源：AWS Project Rainier 印第安纳项目*

这一方法把部署时间从最多 15 周削减到大约 2-3 周，每模块可减少超过 50,000 个现场电工工时。橇装在休斯敦、盐湖城和托皮卡制造，早期部署位于得克萨斯州和南本德（South Bend），目标是从开工到首个服务器机房约 ~25 周。

Houdini 的审批模式也值得注意。它不只依赖站点层面的工程签认，工厂流程要求对设计和实体建造分别验证。Cupertino Electric 是主要合作伙伴，负责后者。

![](https://substack-post-media.s3.amazonaws.com/public/images/57a7f6ee-678c-46c8-9d2e-2d9394a0b80f_1998x1366.png)
*来源：SemiAnalysis Industrials Model*

**Meta**

Meta 近期专注于如何更快实现建筑封闭。它的「帐篷」数据中心（即快速部署结构）是上文分类中外壳级模块化最清晰的例子。轻量结构框架张紧覆膜，比常规钢混建筑快得多地形成一个防风雨围护体。

在 New Albany 的 Prometheus 园区，Meta 正在用这一策略把外壳施工提前。

![](https://substack-post-media.s3.amazonaws.com/public/images/26f3426e-2d7c-469a-acba-ea104d023b84_916x482.png)
*来源：Meta New Albany Prometheus 园区的帐篷建筑*

Meta 已在该园区建成六座快速部署结构，每座约 125,000 平方英尺。为了直观感受速度收益：该园区首批五栋永久建筑花了 Meta 两到三年才建成，而帐篷只用了其中一小部分时间——自 2025 年 7 月宣布帐篷建设计划以来，据我们的卫星追踪，到 2026 年 4 月已有八座矗立。

这并不意味着 Meta 在九个月内建成了完整的数据中心，因为帐篷加速的只是外壳而非完整设施。另一方面，代价是韧性。正如前文所述，覆膜结构无法提供与永久性钢或混凝土外壳同等的长期耐久性和防风雨能力，它也并非本着提供数十年防护服务的设计意图建造。

## **GPU 云与新兴 GPU 云（Neocloud）**

**Crusoe**

Crusoe 同时参与了外壳模块化和整设施模块化两个类别。在 Abilene 的 Stargate 园区，Crusoe 用结构钢和工厂制造的保温金属墙板加速了外壳施工。在与 Digital Building Components 的合作中，每栋建筑用了大约 672 块预制墙板。墙板在 40 天内完成制造，以每天约 15 到 20 块的速度安装，使建筑在不到八周内达到外壳封闭状态。

![](https://substack-post-media.s3.amazonaws.com/public/images/509f6080-e982-4f6e-b0fb-dce2c6e2ecc7_1432x671.jpeg)
*来源：Crusoe Stargate Abilene 园区*

此外，Crusoe 决定垂直整合制造环节。2022 年对 Easter-Owens 的收购把模块化数据中心和电气系统制造收归内部，让 Crusoe 对设计、供应链和生产拥有更强的掌控。公司目前正通过位于科罗拉多州布莱顿（Brighton）的专用 Spark 工厂扩张这一能力。

每个 Spark 单元约一兆瓦规模，到场时已基本完工，这让 Spark 归入整设施模块化类别。

![](https://substack-post-media.s3.amazonaws.com/public/images/87869878-a751-4e71-8ee4-1ab52b74a00d_738x411.jpeg)
*来源：Crusoe Energy Systems – Spark 集装箱*

在内华达州的 Redwood Materials 部署展示了这一模式的扩展能力。Crusoe 最初安装了四个 Spark 单元和一套 12 MW 微电网，随后宣布扩建至 24 个单元。

**Hut 8**

Hut 8 买的是整套基础设施栈。这家坐拥电力和土地资源的前比特币矿商，正在竞速把这些资源转化为可出租的 AI 产能，而最快的路径就是购买成品化的模块化整栈。

![](https://substack-post-media.s3.amazonaws.com/public/images/88acc7be-4dbd-4153-93c4-e044f5f9d95e_1008x509.jpeg)
*来源：Hut 8 Corpus Christi Beacon Point 平台*

在位于 Corpus Christi 的 Beacon Point 园区，它运行 Vertiv 的 OneCore 来将 704MW 的 IT 租约商业化。

该项目围绕 Nvidia 的 DSX 参考架构设计，由一批老牌交易对手交付：American Electric Power 提供电网关系，Jacobs Solutions 承担 EPCM 范围，Vertiv 供应关键电力与冷却基础设施。

**Nebius**

Nebius 对模块化采取了更轻的方式：围绕自家算力架构定义设施，只对电力和冷却等选定基础设施环节做模块化。

在新泽西园区，设施由 Nebius 与 DataOne 的合作按其自有设计建造，规划为分期开发、可扩展至 300 MW。公司使用预制结构件加速外壳施工，同时为站点配套 Bloom Energy 的表后（behind-the-meter）燃料电池作为电力方案。

![Sherrill 公布新泽西州在能源成本上涨之际监管 AI 数据中心的计划 - nj.com](https://substack-post-media.s3.amazonaws.com/public/images/3a140a1a-442b-4e65-b2e5-d9159acf6656_800x476.jpeg)
*来源：NJ.com，Nebius/DataOne 新泽西项目*

在法国贝蒂讷（Béthune），公司以不同的建造方法遵循同样的运营逻辑。该项目复用了昔日的普利司通（Bridgestone）轮胎厂，省去了部分全新建设外壳和报批流程。Azur Datacenter 负责土地、市政接入、施工和物理厂房，Nebius 则专注 GPU、机架、网络和软件。

## **托管数据中心提供商**

**Compass**

Compass 是把模块化打法用得最久的托管商。它把整座设施工业化为一套可复制的「零件包」，而不只是单一子系统。我们估计每栋建筑约 70-85% 在场外制造、现场栓接成型，18 到 21 天就能立起一栋建筑的框架和屋顶。这套零件包覆盖全栈：

- 外壳：无钢筋、纤维增强的预制外壳，Compass 用现场搅拌站自行浇筑；
- 白空间：标准化预制机架与气流封闭系统，例如采用 Schneider 的 EcoStruxure Pod；
- 电力区块：可复制的约 ~1.25 MW Schneider 电力中心（Galaxy VX UPS、锂离子电池、QED-2 开关柜）；
- 中压开关柜：与 Siemens 签约的模块化中压开关柜橇装，五年内最多 1,500 套。

![](https://substack-post-media.s3.amazonaws.com/public/images/858e4c0e-9373-499f-93c5-4209a4698865_970x464.jpeg)
*来源：Compass 位于 Red Oak 的数据中心*

它在各园区复用同一套零件包：在得克萨斯州 Red Oak 高达 360 MW，在亚利桑那州 Goodyear 则是八栋建筑、共 180 万平方英尺。

**QTS**

QTS 的模块化策略围绕三件事：尽早锁定设计、标准化各厂商之间的接口、在具体建筑需要之前就采购关键设备。公司在堪萨斯州保有约 700 万平方英尺的仓库用于长交期设备，UPS 系统、开关柜、冷却设备等业主供货部件可以放在库存里，而不必等每个客户签约后再下单。

这套打法始于 Freedom Design：建筑外壳保持灵活，但电力架构重复使用。每个工厂预制舱把 1.5 MW 的 UPS 与开关柜包同 2.25 MW 的发电机组合在一起，系统按 1.5 MW 步进扩展。Freedom LC+ 把同一概念延伸到冷却，其架构既能支持全风冷、也能支持全液冷部署。QTS 更新的快速部署设计则把模块化进一步推进到建筑本体，围绕可复制的 60 MW 数据大厅区块来组织产能。

因此 QTS 持续把更多环节搬到场外：先是电力系统，然后是冷却系统的部分，如今连外壳和数据大厅的一部分也在内。外壳方面，QTS 部分设施（包括 Manassas）采用 tilt-up 混凝土，而 Cedar Rapids 等更大的园区则使用结构钢。

![项目档案：QTS MAN1 DC-3 | Tilt-up Concrete Association](https://substack-post-media.s3.amazonaws.com/public/images/9b685916-1e0f-401b-a00a-dd37556a4ffa_645x680.png)
*来源：QTS Man1 项目 tilt-up 施工*

价值在于人工、安全和工期确定性。QTS 估计，劳动力压力已使数据中心建设成本每 MW 上涨约 20-30%。转向模块化是公司的趋势，而提前储备长交期设备又消除了一个延迟来源，让 QTS 对最终几兆瓦何时能够投运拥有更强的掌控。

QTS 随后开发了「Rapids」设计，显著加快了建设进度。已有两家大型 AI 公司大规模采用了这一设计。

![](https://substack-post-media.s3.amazonaws.com/public/images/7671330c-35c5-43de-b0bb-59627d84a988_1414x1180.png)
*来源：SemiAnalysis Industrials Model*

**Aligned Data Centers**

Aligned 的模块化策略以适应性为核心：保持电力与冷却核心架构标准化，同时允许大厅配置随客户需求和机架密度的演进而改变。这一打法始于核心机电基础设施，包括集成了配电开关柜和电力的 2 MW UPS 集装箱。如今又延伸到厂区输送环节，例如预制冷冻水组件。对于能够早期协调的客户，范围还可以进一步深入白空间，比如二次侧流体管路。

![](https://substack-post-media.s3.amazonaws.com/public/images/8f482d50-f566-4f90-9fdc-8f95fb2d5463_1024x531.png)
*来源：Aligned Adaptive Modular Infrastructure*

另一个核心要素是 Aligned 的 Adaptive Modular Infrastructure 平台，它保持底层电力与冷却系统不变，同时允许大厅随着机架密度演进在风冷、混合与液冷之间切换。该平台组合了：

- Delta³：Aligned 的风冷系统，支持每机架最高约 50 kW 的密度；
- DeltaFlow：其液冷平台，支持每机架 350 kW 以上的密度。

由于底层冷冻水回路和设施接口保持一致，冷却组合可以改变而无需重新设计整个大厅。模块内部的组件保持标准化、不发生变化。一个例子是得克萨斯州的 Project Caprock：六栋建筑、共 540 MW、165 万平方英尺。
