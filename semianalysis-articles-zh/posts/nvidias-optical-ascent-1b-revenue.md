---
title: "英伟达的光学进击：营收超 $1B；缺席的 800G 爬坡；AI 假动作"
title_en: "Nvidia's Optical Ascent: >$1B Revenue; The Missing 800G Ramp; AI Head-Fakes"
subtitle: "一家供应商赢家通吃，同时揭示哪些是 AI 假动作"
date: 2023-08-23
source: https://newsletter.semianalysis.com/p/nvidias-optical-ascent-1b-revenue
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 英伟达的光学进击：营收超 $1B；缺席的 800G 爬坡；AI 假动作

> 原文：[Nvidia's Optical Ascent: >$1B Revenue; The Missing 800G Ramp; AI Head-Fakes](https://newsletter.semianalysis.com/p/nvidias-optical-ascent-1b-revenue) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**一家供应商赢家通吃，同时揭示哪些是 AI 假动作**

将 GPU 互连起来的网络性能，往往是整个系统性能的门控因素，正因如此，它是 AI 基础设施建设中[成本最高的环节之一](https://www.semianalysis.com/p/nvidias-infiniband-problem-qmx-ai)，仅次于加速器本身。英伟达正试图[将 GPU 产能配给当作武器挥舞，以塞进更多网络产品](https://www.semianalysis.com/p/amazons-cloud-crisis-how-aws-will)。在英伟达与博通争夺[高利润的交换芯片插槽](https://www.semianalysis.com/p/nvidias-infiniband-problem-qmx-ai)的同时，英伟达还在推销自家的光收发器，用于连接其 InfiniBand、以太网和 NVLink 网络。凭借捆绑销售，英伟达未来 12 个月的光模块销售额将超过 10 亿美元（$1B）。

今天我们想梳理外部 NVLink 网络的爬坡、面向交换机的 800G 光收发器，以及英伟达这轮爬坡的最大受益者。我们先从技术变迁的概览讲起，再谈生意。

![](https://substack-post-media.s3.amazonaws.com/public/images/20f40c6e-1a57-470b-9c6e-dba630d641ab_953x534.png)

AI 中存在巨大的瓶颈。去年我们报道过 Meta 对 AI 硬件与光学即将到来的问题的分析。我们还指出，与其他人相比，[英伟达在玩一场完全不同的游戏](https://www.semianalysis.com/p/meta-discusses-ai-hardware-and-co)。

这源于其 NVLink 纵向扩展（scale-up）网络。其他所有商用芯片加速器都无法在加速器之间扩展到如此高的带宽水平。高带宽对训练极其重要，而[根据 GPT-4 的架构，它对推理可能更为重要](https://www.semianalysis.com/p/gpt-4-architecture-infrastructure)。

多数 8x H100 部署总共有 400GB/s（3.2T）网络带宽，而英伟达开发了一个带纵向扩展 NVLink 网络的特殊版本。相比之下，NVLink 纵向扩展拥有 3.2TB/s 带宽。每个 H100 Superpod 最多可能配备 1,152 个 800G 光收发器，将 32 个 GPU 节点与 18 个交换节点全部互连（all to all）。虽然这很重要，但 800G 的更大出货量将在以太网和 InfiniBand 市场，而英伟达在那里同样在进行捆绑销售。

![](https://substack-post-media.s3.amazonaws.com/public/images/888a2891-039b-4cec-a975-5f6d0acbe3ef_866x307.png)

纵观整个网络行业，有多个细分领域都有公司宣称自己是 400G 与 800G 爬坡的赢家，但[其中许多其实是 AI 假动作（head-fake）](https://www.semianalysis.com/p/nvidias-ramp-volume-asp-cloud-pricing)。例如，[有几家公司宣称在有源电缆（AEC 与 ACC）领域获胜](https://www.semianalysis.com/p/thick-cables-thin-margins-microsoft)，但到明年初，那将是一场九家公司混战、利润率崩塌的绞杀战。而 AI 假动作最多的地方，莫过于光收发器市场。

这条供应链有多个组成部分：激光器、DSP、TIA、驱动器、发射/接收光学器件，以及光收发器的整体封装制造。其中成本最高的三大要素是 DSP、激光器和封装/模块制造。

[DSP 主要由 Marvell 主导](https://www.semianalysis.com/i/107160162/the-war-on-marvell)，尽管[博通正在夺回一些份额](https://www.semianalysis.com/i/107160162/the-war-on-marvell)；此外还有[去掉 DSP 的线性直驱（linear direct drive）光学方案](https://www.semianalysis.com/i/107160162/the-war-on-marvell)正在到来，明年开始渗透。这个环节总体非常强劲，但 Marvell 的其他业务（如存储与电信运营商基础设施）极度疲软，短期内可能掩盖其中部分利好。

*我们将于 9 月 3 日在台湾举办 [AI 与半导体研讨会](https://www.eventbrite.com/e/ai-and-semiconductor-symposium-tickets-692838296997)，众多代工厂、封装厂、ODM 供应商与买方将出席。议题涵盖 AI 基础设施的未来、谷歌 Gemini 与未来 OpenAI GPT 采用的下一代模型架构、中国模拟/功率半导体晶圆厂建设，以及英伟达当前的收购目标。演讲者包括 SemiAnalysis 的多位成员、[FabricatedKnowledge](https://www.fabricatedknowledge.com/)、[Asianometry](https://www.asianometry.com/)、[Alethia Capital](https://www.aletheia-capital.com/)，以及晶心科技（Andes）的 CEO 与董事长——Andes 是全球出货量最大的基于 RISC-V 的芯片公司，每年出货超过 10 亿颗核心。如果你能到场，[请在此注册](https://www.eventbrite.com/e/ai-and-semiconductor-symposium-tickets-692838296997)！*

激光器环节对领导者而言历来是高利润生意，但近年来持续走弱。激光器种类繁多，主要类型是电吸收调制激光器（EML）与垂直腔面发射激光器（VCSEL）。VCSEL 用于较短距离的光模块，主要优点是功耗更低、价格更便宜。另一面是 EML 激光器，传输距离远得多，但功耗更高。800G 初期主要是 EML 市场，但明年 VCSEL 应会拿下大部分出货量。

全球最大的激光器制造商 Lumentum 正是这样一个 AI 假动作。许多人追逐光模块零部件供应商，Lumentum 位居名单最前列。虽然公司本季度表现不错，但下季度指引远低于预期：3 亿至 3.25 亿美元，而卖方预期为 3.668 亿美元。公司确认电信（Telecom）与数通（Datacom）营收下季度将环比下滑，主要归因于电信业务。

不过，也有一线转机。公司表示：

> 2024 日历年的电信与数通营收将高于 2023 日历年。
>
> 我们预计将于 2024 日历年开始爬坡交付 200G EML 产品，客户对 800G 与 1.6T 收发器设计的认证正在顺利推进。

每通道 200G 尚需时日，预计要到 2024 年底尾段才会以可观的量出货，大概会与英伟达下一代 GPU 和 NVSwitch 同步登场。

![](https://substack-post-media.s3.amazonaws.com/public/images/4b247aab-d7d2-4df6-8790-84b2cf07dbf6_1138x636.png)

尽管按我们的渠道调研，Lumentum 在光模块中保持着良好份额，但 Lumentum 的数通业务是芯片业务——相对成品收发器而言 ASP 低得多，因此总营收也更少。此外，每通道 100G 的 EML 已相当大宗商品化，目前许多公司都在生产。这使得拐点很难显著拉动业绩。最后，随着基于 VCSEL 的 400G 与 800G 方案爬坡，每个光收发器的激光器用量将持续下降。

AI 爬坡此刻正在 GPU 与网络层面真实发生，但对 Lumentum 而言，2023 日历年似乎没有大的爬坡，因此，他们是一个 AI 假动作。

第三个高价值环节是收发器制造本身。Coherent 大概是这个市场里最大的 AI 假动作。它是该领域最大的玩家，一个垂直整合、债台高筑的巨兽，同时生产激光器和模块。他们一直宣称 AI 是业务的巨大驱动力，但细看其业绩，生意并不在那里。

![](https://substack-post-media.s3.amazonaws.com/public/images/66ca7f35-7ca7-400f-9d9b-13d5fa334106_1267x701.png)

其指引远低于预期，原因是电信市场疲软以及数通爬坡缺位。此外，其竞争地位也不如历史上那么稳固，并将随着 800G 时代的到来继续走弱。他们最近甚至抛出了这样一段奇怪的表述。

> 未计入全年 FY24 营收指引的，是与近期 AI 驱动的数据中心建设带来的 Datacom 收发器需求激增相关的数亿美元额外营收，因为供应链正在扩充增量产能以应对行业需求。

[FabricatedKnowledge 的 Doug](https://www.fabricatedknowledge.com/p/earnings-mchp-and-ifx-simo-rumors) 对这一怪象提出了[最好的问题](https://www.fabricatedknowledge.com/p/earnings-mchp-and-ifx-simo-rumors)。

> 如果这是真金白银的营收，为什么不放进指引？因为他们自己都不认为能兑现这个爬坡？

[点击阅读他就此以及许多其他财报的完整分析](https://www.fabricatedknowledge.com/p/earnings-mchp-and-ifx-simo-rumors)。

思科（Cisco）是全球最大的网络公司，出人意料地并非 AI 假动作。这主要是因为从来没人认为它是赢家，但它似乎确实正在拿到一些份额。

> 迄今为止，我们已为 AI 以太网 fabric 拿到超过 5 亿美元订单。我们也在为 AI 训练 fabric 试点 800G 能力。至于 800G，我想说的是：我们已经参与其中，我们的设备已经完成部署，我们赢得了这些客户的信任。

虽然我们不会称其为赢家，但其表现可谓得到公允反映，甚至赢走了相当大一块我们原以为会被博通和英伟达吞掉的业务。

中国的中际旭创（Zhongji Innolight，Innolight）是另一家被吹捧为 AI 建设大赢家的光收发器公司，因为据信其在 800G 收发器上拥有强势份额。这一点已深度体现在股价中——年初至今上涨 350%，预期被捧上了天。8 月 27 日发布财报时，我们将看到 Innolight 如何兑现这些预期。市场一致预期其截至 2023 年 12 月的财年营收增长 21%，截至 2024 年 12 月的财年营收增长 54%。

虽然我们的调研表明，他们确实是多家超大规模云厂商处的赢家，但中国一些人鼓吹的超过 1,000 万只的量级可能过高了。我们将其归因于[供应链亢奋（supply chain intoxication）](https://www.semianalysis.com/i/136248981/nvidia-supply-chain-intoxication)。

虽然他们是赢家，但其 800G 爬坡的到来没有我们下面讨论的那家公司快。明年，随着超大规模云厂商加大采购，Innolight 的业务将迎来爬坡。

今年下半年的 800G 爬坡由英伟达驱动。他们选择了一家不同的供应商。

[获取 8 折团购订阅](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
