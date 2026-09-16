---
title: "AI 芯片大短缺"
title_en: "The Great AI Silicon Shortage"
subtitle: "台积电 N3 晶圆短缺、内存受限、数据中心瓶颈、供应链大战的赢家"
date: 2026-03-12
source: https://newsletter.semianalysis.com/p/the-great-ai-silicon-shortage
crawled: 2026-09-15
authors: ["Ivan Chiam", "Myron Xie", "Ray Wang", "Sravan Kundojjala", "Gerald Wong", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# AI 芯片大短缺

> 原文：[The Great AI Silicon Shortage](https://newsletter.semianalysis.com/p/the-great-ai-silicon-shortage) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**台积电 N3 晶圆短缺、内存受限、数据中心瓶颈、供应链大战的赢家**

![](https://substack-post-media.s3.amazonaws.com/public/images/bc74983e-edab-47a0-801c-fffe0839a20e_4000x4000.png)

---

## 算力短缺

token 需求正呈爆炸式增长，对 AI 算力的需求也在持续加速。模型能力的提升，叠加智能体（agentic）工作流的迅速兴起，推动了用户采用规模和总 token 需求的激增。仅 2 月单月，在智能体编程平台 Claude Code 被广泛采用的带动下，Anthropic 就新增了高达 $6B 的 ARR；而且如果 Anthropic 手里有更多算力，这个数字还会更大。尽管过去几年 AI 基础设施建设规模庞大，可用算力依然稀缺。按需 GPU 价格持续走高，连已经落后近两代的 Hopper 也未能幸免。

以我们自身的经历来说，我们联系了认识的每一家新兴 GPU 云（neocloud），询问是否有小型集群可用，但所有产能都已被牢牢锁定。这种供给紧张的环境，解释了超大规模云厂商资本开支（capex）计划的急剧上调。市场一致预期全面大幅上修，其中 Google 最为极端——2026 年资本开支预期较此前预期几乎翻了一倍，主要由数据中心和服务器支出驱动。

![](https://substack-post-media.s3.amazonaws.com/public/images/685652e0-3bff-448a-a33f-f1f16feb6b61_1844x1038.png)
*来源：公司财报、Bloomberg*

这是极其庞大的一笔支出，如果条件允许，超大规模云厂商还会投入更多资本，但一个关键因素制约着它们：芯片供给。先进逻辑与内存制造产能根本不足以支撑当前算力部署的速度。虽然「公元后」（AD，即 ChatGPT 发布之后）时代一直被 CoWoS 封装、数据中心电力等各种瓶颈所困扰，但如今我们已确确实实进入了芯片短缺阶段。

![](https://substack-post-media.s3.amazonaws.com/public/images/db3eb393-a811-44e0-b4f3-7c5ebf1b7f87_2030x1076.png)
*来源：SemiAnalysis 加速器模型（Accelerator Model）*

## 台积电 N3 短缺

最大的瓶颈即使不是台积电（TSMC）的 N3 逻辑晶圆产能，它也位居最前列。台积电 N3 家族于 2023 年开始量产出货，最初的需求主要来自智能手机和 PC。[N3 的开局并不顺利：首个变体 "N3B" 存在良率问题，而且相对于密度提升而言成本过高。](https://newsletter.semianalysis.com/i/175660907/tsmc-3nm-fab-costs)随着精修版 N3E 工艺的推出，采用率才显著提升——这是一个放宽规格的变体，EUV 层数少得多，成本也因此更低。关键的智能手机和 PC 客户包括：Apple（其 M3 至 M5 系列 Mac 芯片和 A17 至 A19 iPhone 处理器均采用 N3 变体）、Qualcomm（骁龙 8 Elite 系列）、MediaTek（Dimensity（天玑）智能手机 SoC 以及部分汽车和 PC 芯片），以及英特尔（Intel）（Lunar Lake 和 Arrow Lake 客户端处理器）。

![](https://substack-post-media.s3.amazonaws.com/public/images/be6a510f-f4ee-4ee8-9267-22ccd427f99c_1860x1038.png)
*来源：SemiAnalysis 代工模型（Foundry Model）*

直到今天，N3 需求一直主要由消费电子驱动。2026 年，所有主流 AI 加速器家族都在向 N3 迁移，AI 将占据 N3 需求的大头，随后再向 N2 及更先进的节点转移。

从下表可以看到，进入 2026 年，整个行业正在向台积电 N3 家族收敛，使其成为 AI 加速器的主流先进制程节点。NVIDIA 从 Blackwell 的 4NP 转向 Rubin 的 3NP。AMD 通常更早采用新节点，已在 MI350X 上采用 N3，MI400 的 AID 和 MID 小芯片（tile）也将停留在 N3（XCD 为 N2）。Google TPU 路线图自 TPU v7 起全面转向 N3E，且 TPU 项目规模今年大幅扩大。AWS 的 Trainium3 也转向 N3P。Meta 的 MTIA 走的是类似路径，只是规模要小得多。

![](https://substack-post-media.s3.amazonaws.com/public/images/0129d5ef-d8c3-46a8-a8f5-e69d5e4a84b5_1896x1180.png)
*来源：SemiAnalysis 加速器模型*

这一转移并不限于 XPU 芯片。VR 机柜中使用的 Vera CPU，其全部芯片均采用 N3P。还有网络芯片：NVLink 6 交换机，以及 Tomahawk 6、Spectrum 6 等横向扩展（scale-out）交换机。由于 Rubin 为每颗 GPU 提供 1.6T 的横向扩展网络带宽，Rubin 还开启了 3nm 200G 光 DSP 的采用。

N3 采用的突然汇聚，叠加 AI 算力需求的持续增长，给 N3 晶圆产能带来了巨大的需求冲击。台积电有些措手不及，晶圆产能扩张未能跟上激增的 AI 需求。这是怎么发生的？尽管史上最大规模的算力建设早在 2022 年底就已启动，台积电的资本开支直到 2025 年才超过此前峰值。今年，台积电将大幅突破去年的创纪录资本开支，因为它们已经意识到客户需求超出其产能的程度有多严重。

![](https://substack-post-media.s3.amazonaws.com/public/images/6fd015f7-6e9e-4a42-b5c9-2c359d65dd59_1424x742.png)
*来源：公司公告*

虽然台积电对其仅有的两个竞争对手——英特尔和三星（Samsung）——保持着明显的技术领先，但如果客户拿不到足够的晶圆供给来支撑自身业务，这种优势的意义就会大打折扣。产能受限因此可能促使客户探索更大的代工来源多元化。例如，英特尔有美国政府的撑腰，任何转向 Intel Foundry 的外包都会在美国政府那里挣得好感。与此同时，三星晶圆代工（Samsung Foundry）的势头也开始积聚，近期斩获了一些设计导入（design win）。首先，三星拿到了特斯拉的部分芯片项目，例如 AI5 和 AI6，不过这些项目与台积电采用双轨并行。此外，[三星晶圆代工也已进入 Nvidia 的数据中心供应链](https://semianalysis.com/institutional/samsung-foundry-finds-its-way-into-nvidias-ai-supply-chain/)，这一进展我们曾在代工模型中讨论过。

## 用数字看 N3

现在来看看到底有多紧张。N3 加速器晶圆需求今年全年都在激进爬坡。主要驱动力是 Nvidia 从基于 4NP 的 Blackwell 向基于 N3P 的 Rubin 世代切换所带来的 Rubin 量产爬坡。不过，鉴于平台和供应链更成熟，今年 Blackwell 的出货量仍将高于 Rubin。Google 与 Broadcom 的 TPU 抢在 Nvidia 和 Amazon 之前用上 N3，TPU v7 芯片 2025 年就已投产。这一势头今年仍在延续：由于 Google 内部以及 Anthropic 等外部需求的拉动，TPU 出货量将大幅增长。与此同时，向下一代 TPU v8 变体的过渡也将开启，后者同样停留在 N3 节点。另一个重大摇摆因素是基于 N3P 的 Trainium3：其晶圆投入从 2026 年初开始，为下半年产量大幅爬坡蓄力。

因此，AI 相关需求（加速器、主机 CPU 和网络芯片的 N3 需求）今年将占到 N3 产出的将近 60%。其余 40% 主要用于智能手机和 CPU。这些来源的需求已经吃掉了全部 N3 产能，台积电几乎没有余力再增加产能。即便台积电在增加 N3 产能，2027 年的紧张程度还会进一步加剧。我们的模型测算，AI 需求将占 2027 年 N3 晶圆产出的 86%，几乎完全挤占智能手机和 CPU 晶圆。这一转变的一部分源于智能手机路线图按计划向 N2 迁移，但 N3 产能紧张无疑也在加快这一过渡。对于仍停留在 N3 的产品线而言，需求不太可能得到完全满足。

![](https://substack-post-media.s3.amazonaws.com/public/images/5b707af9-3845-4437-9c68-561f36658df4_1868x1104.png)
*来源：SemiAnalysis 代工模型、SemiAnalysis 加速器模型*
![](https://substack-post-media.s3.amazonaws.com/public/images/0183a621-85de-4e9b-b829-6e6d90fddaa6_2092x1186.png)
*来源：SemiAnalysis 加速器模型*

在争夺有限 N3 产能配给（allocation）的客户之间，台积电最终扮演着「造王者」的角色。2026 年，AI 基础设施客户明显优先于消费电子。AI 加速器设计通常裸片面积更大、封装要求更复杂，对应更高的平均售价（ASP）。更重要的是，AI 驱动的需求迄今是台积电增长的首要驱动力。终端客户愿意不惜一切代价部署更多算力。这背后有主要 AI 实验室的算力承诺所带来的多年期需求可见性支撑。

与之形成对照的是，移动和客户端市场如今已相当饱和，无论出货量还是单机内容物增长的空间都不大。这使 AI 加速器客户在获取先进制程产能时拥有相对优势。其他细分市场中无法获得足够 N3 产能的客户，可能被迫延长现有产品周期，或直接迁移到 N2 平台。

## 台积电的供给状况

需求远远跑在供给前面，台积电一边扩充产能，一边把现有产线压到极限，从铭牌产能中榨出每一片可能的晶圆。其结果是，2026 年下半年 N3 的有效稼动率预计将超过 100%。公司还在把部分工艺层转移到其他晶圆厂，尽可能腾出增量的 N3 产能。

为什么台积电不能直接增加 N3 晶圆投片？与内存供应商一样，台积电受制于可用的洁净室空间。必须先建成可用的厂房面积，才能安装设备、让新产能上线。未来 2 年，台积电都无法增加足够的产能来完全满足需求。因此，在此期间若有公司想拿到更多晶圆配额，就必须有其他客户让出其现有的宝贵配额——而这种事确实有可能发生。

![](https://substack-post-media.s3.amazonaws.com/public/images/450c33c0-062f-486e-aff1-1db8c0dc68b4_2020x1088.png)
*来源：SemiAnalysis 代工模型*
![](https://substack-post-media.s3.amazonaws.com/public/images/12d5f30f-d1ba-4037-aa57-763d58a3bde1_2571x1505.png)
*来源：SemiAnalysis 代工模型*

## 智能手机：前道产能的泄压阀？

智能手机是今年 N3 晶圆需求的第二大来源。如果说什么细分市场最有可能出现需求走弱、从而为 XPU 晶圆腾出产能，那就是它。目前，Apple 及 MediaTek、Qualcomm 等其他智能手机客户已集体向供应链下单，其假设是今年智能手机出货量仅有个位数低段增长。

然而，不断上涨的内存价格正在传导到手机物料清单（BOM）成本，并最终传导到消费端售价。这很可能抑制消费需求。我们已经看到迹象：智能手机需求将被下修至同比低双位数下滑。随着智能手机需求走弱，相关晶圆需求将被削减，为 XPU 逻辑腾出更多产能。

从对出货量的影响来看，把 2026 年智能手机 N3 晶圆投片总量的 5%（437k 片晶圆的 5%）重新分配给 AI 加速器，就能多生产约 0.1 百万颗 Rubin GPU 或约 0.3 百万颗 TPU v7。在更极端的场景下——2026 年智能手机 N3 晶圆投片总量的 25% 被重新分配给 AI 加速器——台积电可以多制造约 0.7 百万颗 Rubin GPU 或约 1.5 百万颗 TPU v7。不过，逻辑晶圆只是 AI 加速器芯片等式的一部分，还需要内存供给和先进封装。

![](https://substack-post-media.s3.amazonaws.com/public/images/b40dd801-4946-431b-bcd4-b99550108971_1376x320.png)
*来源：SemiAnalysis 代工模型*
![](https://substack-post-media.s3.amazonaws.com/public/images/6f4f58ae-8668-4da8-8143-b528a369cd1a_2018x1084.png)
*来源：SemiAnalysis 估算*

## 内存：下一个最大瓶颈

[全球内存短缺](https://newsletter.semianalysis.com/p/memory-mania-how-a-once-in-four-decades)短期内不太可能缓解。内存已成为下一个主要战场，芯片厂商和超大规模云厂商正竞相锁定用于加速器生产的 DRAM 供给。虽然 DRAM 晶圆总产能仍在增长，但大部分增量产能正被 HBM 吸收，实际上挤出了常规 DRAM。

按每位元消耗的晶圆计算，HBM 的晶圆产能消耗约为常规 DRAM 的三倍；随着行业今年向 HBM4 过渡，这一差距可能扩大到近四倍，明年 HBM4E 时代还会更大。因此，HBM 的增量增长会把不成比例的 DRAM 晶圆产能从常规 DRAM 那里转移走，进一步强化内存供给的结构性紧张。

![](https://substack-post-media.s3.amazonaws.com/public/images/e3edd595-4b9d-4d67-8da2-ee97a6f6e053_2136x1126.png)
*来源：SemiAnalysis 内存模型（Memory Model）*
![](https://substack-post-media.s3.amazonaws.com/public/images/aab0bd24-a53a-4e2a-a0ea-7daa0057e0f8_2004x1094.png)
*来源：SemiAnalysis 内存模型*

每颗加速器的 HBM 容量快速增长，进一步放大了这一压力。HBM 位元出货量正在急剧上扬，主要驱动力是单设备内存容量的提升，而不只是出货量增长。对 NVIDIA 而言，从 Blackwell 到 Blackwell Ultra 再到 Rubin，HBM 容量提升 50%，Rubin Ultra 再带来约 4 倍的增长。超大规模云厂商的 ASIC 也出现类似跃升：TPU v8AX 和 Trainium3 都从上一代的 8 层（8-Hi）堆叠迁移到 12 层（12-Hi）堆叠，AMD 的内存容量也从 MI350 到 MI400 提升 50%。

![](https://substack-post-media.s3.amazonaws.com/public/images/17bae206-924e-4e87-a7f1-c91a3f257c9e_2098x1130.png)
*来源：SemiAnalysis 加速器模型*

另一个收紧动态是向更高 HBM 引脚速度的推进。NVIDIA 等客户为 HBM4 设定了约 11 Gb/s 的引脚速度目标，而内存厂商要在可接受的良率下实现这一要求仍有困难。SK hynix 和三星在满足这些规格方面进展较好，美光（Micron）在 HBM4 上则落在后面——这一动态我们最早在 1 月的 [Rubin 文章](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution)和[加速器与 HBM 模型](https://semianalysis.com/accelerator-hbm-model/)中就有讨论。客户要求更高的引脚速度、厂商又难以大规模交付，这种性能要求的不断升级进一步约束了有效 HBM 供给。

![](https://substack-post-media.s3.amazonaws.com/public/images/5c55d753-0c40-4c17-83f1-e3d2063f7cfc_2134x1226.png)
*来源：SemiAnalysis 内存模型*

在 HBM 之外，服务器 DRAM 需求也在走强。在 NVIDIA 的下一代平台中，AI 服务器系统内存将显著增加：VR NVL72 机柜的 DDR 容量提升 3 倍，每颗 Vera CPU 配 1,536 GB，而每颗 Grace 为 512 GB。我们还预计 2026 年整体 DRAM 位元需求将拐点向上，因为老化的云端和企业服务器装机量正进入多年期的更换周期。与此同时，AI 工作负载——尤其是数据预取（data staging）、编排和强化学习——正在[拉动 CPU 需求](https://newsletter.semianalysis.com/p/cpus-are-back-the-datacenter-cpu)，使 CPU 与 GPU 的配比逐步提高。

纵观整个 DRAM 市场，AI 及通用服务器部署的加速、单系统 DRAM 容量的提升，预计将推动服务器 DRAM 需求持续走高。随着内存价格上涨，这一需求应足以在未来两年抵消并超越智能手机、PC 和消费电子的疲软。

![](https://substack-post-media.s3.amazonaws.com/public/images/4f090096-02d5-4aaf-b7b2-d0233652675f_2002x1180.png)
*来源：SemiAnalysis 内存模型*

如果逻辑产能得以腾给加速器，客户很快就需要把注意力转向从内存供应商那里锁定更多 HBM。随着常规 DDR DRAM 价格飙升，DDR 的毛利率已飙升至接近甚至超过 HBM 已签约供货时的水平。过去，HBM 更优的利润率状况为内存供应商扩大 HBM 晶圆产能提供了明确理由。但如今情况已非如此——至少在 2026 年，利润率格局已经逆转。

要激励内存厂商把更多晶圆投片从常规产品转向 HBM，客户很可能需要支付高于当前签约水平的价格，才能锁定增量 HBM 供给。这一动态预计会在 2027 年变得更加明显，届时下一轮 HBM 定价谈判将尘埃落定。如果内存供应商松口并把产能转向 HBM，常规 DDR DRAM 的可用位元供给将进一步收紧。

另一个关键含义是位元从消费类应用向服务器和 HBM 的重新分配，这一动态我们自 2025 年下半年（2H25）起就一直在强调。在内存模型的最新分析中，我们重点评估了消费端冲击对潜在位元再分配的影响。在消费类出货量削减 50% 的极端场景下，将释放约 55,390 million Gb，相当于 2026 年 DRAM 总需求的约 14%。在削减 25% 的场景下，将腾出约 27,690 million Gb，约占 DRAM 总需求的 7%，接近今年 HBM 需求的 80%。

![](https://substack-post-media.s3.amazonaws.com/public/images/fd82a56a-592f-48d7-8269-232c73920309_2379x504.png)
*来源：SemiAnalysis 内存模型*

我们的基准情景仍是更为温和的消费类出货量下降 10-15%。在出货量削减 10% 的情景下，将释放约 11,076 million Gb，仅占 DRAM 总需求的约 3%。在我们看来，这一水平的增量供给不足以实质性改变我们预期今年将看到的整体供需格局。

关键问题在于，内存供应商对消费端疲软的准备程度如何，以及它们在多大程度上已经做出调整。我们认为，内存厂商对消费终端市场的疲软有清醒的认识。例如，三星管理层已多次强调消费端的疲弱，我们相信其产能配给计划已经纳入出货量下滑 10-15% 的下行情景。我们预计其他主要内存供应商也处于类似状态。

## CoWoS——仍然紧张，但正在缓解

如今前道产能才是主要瓶颈，CoWoS 的约束正在缓解。CoWoS 虽然也有限，但台积电的产能规划是把 N3 的约束考虑在内的。如果没有前道晶圆供给做支撑，台积电过度投资 CoWoS 产能毫无意义。2.5D 封装也还有其他选择。CoWoS 可以、而且此前也曾外包给 ASE/SPIL、Amkor 等 OSAT（封测代工）厂商。例如，在出口许可证将获批准的消息传出时，Nvidia 就找 Amkor 封装面向中国市场的 H200。英特尔的旗舰 2.5D 先进封装方案 EMIB 是另一个日益受到青睐的选项，Trainium 和 TPU 都在不同程度上采用了它。

在付费墙之后，我们将讨论另外两个主要瓶颈：数据中心和电力。它们的重要性随时间发生了变化。
