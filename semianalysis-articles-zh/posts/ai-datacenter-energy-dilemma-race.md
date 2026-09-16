---
title: "AI 数据中心的能源困境——数据中心空间争夺战"
title_en: "AI Datacenter Energy Dilemma - Race for AI Datacenter Space"
subtitle: "吉瓦之梦与套娃大脑：受制于数据中心而非芯片"
date: 2024-03-13
source: https://newsletter.semianalysis.com/p/ai-datacenter-energy-dilemma-race
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball", "Jeremie Eliahou Ontiveros"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# AI 数据中心的能源困境——数据中心空间争夺战

> 原文：[AI Datacenter Energy Dilemma - Race for AI Datacenter Space](https://newsletter.semianalysis.com/p/ai-datacenter-energy-dilemma-race) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**吉瓦之梦与套娃大脑：受制于数据中心而非芯片**

AI 集群需求的爆发式增长，使数据中心容量成为焦点，电网、发电容量与环境也因此承受极端压力。AI 基础设施建设受到数据中心容量不足的严重制约——训练环节尤其如此，因为 GPU 通常需要同址部署以实现高速芯片间互连。推理的部署则深受各区域总容量以及更好模型不断上市的影响。

关于瓶颈究竟会出现在哪里，讨论已经很多——新增电力需求有多大？GPU 部署在哪里？北美、日本、台湾、新加坡、马来西亚、韩国、中国、印度尼西亚、卡塔尔、沙特阿拉伯、科威特等各区域的数据中心建设进展如何？加速器产能爬坡何时会被物理基础设施卡住？会先是变压器、发电机、电网容量，还是我们所跟踪的其他 15 类数据中心部件中的某一类？需要多少资本开支（capex）？哪些超大规模云厂商和大公司在竞相锁定足够容量，哪些又因为对 AI 猝不及防、手中没有数据中心容量而将受到严重掣肘？未来几年，吉瓦（GW）级乃至更大的训练集群将建在哪里？天然气、太阳能、风电等各发电类型的占比如何？这一切到底可不可持续，AI 建设浪潮会不会毁掉环境？

今天我们就来回答这些问题：报告前半部分免费公开，后半部分订阅读者可在下方阅读。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

许多人正基于荒谬的假设对数据中心建设速度大发议论。连 Elon Musk 也凑热闹发表了看法，但他的评估并不完全准确。

> 上线的人工智能算力似乎每六个月就增长 10 倍……这样的话，很容易预测下一个短缺的就是降压变压器。你得给这些东西喂电。如果电力公司输出 100-300 千伏，而它要一路降到六伏，这个降压幅度可不小。我那个不太冷的笑话是：要驱动 Transformer（Transformer 模型），你需要 transformer（变压器）……再下一个短缺的将是电力。他们将找不到足够的电力来驱动所有芯片。我认为明年你们就会看到，他们根本找不到足够的电来驱动所有芯片。
>
> 博世互联世界大会（Bosch Connected World Conference）

需要说明的是，他对这些物理基础设施限制的判断大体是对的，但算力并非每六个月增长 10 倍——我们持续跟踪[所有主要超大规模和商用芯片公司的 CoWoS、HBM 及服务器供应链](https://www.semianalysis.com/p/accelerator-model)，看到以峰值理论 FP8 FLOPS 计的总 AI 算力容量自 2023 年一季度以来一直以仍然很快的环比 50-60% 的速度增长。也就是说，离六个月 10 倍相去甚远。CoWoS 和 HBM 的增长速度根本跟不上。

![](https://substack-post-media.s3.amazonaws.com/public/images/361a28af-afe2-4df8-b47a-7eed2f07a7d4_1591x1030.png)
*SemiAnalysis 估算*

由 Transformer 模型驱动的生成式 AI 热潮，确实将需要大量的变压器、发电机以及数不清的其他电气与散热部件。

许多信封背面的粗略估算、乃至彻头彻尾的危言耸听，都基于过时的研究。国际能源署（IEA）近期的[《Electricity 2024》报告](https://www.iea.org/reports/electricity-2024)预计，到 2026 年 AI 数据中心的电力需求将达到 90 太瓦时（TWh），约相当于 10 吉瓦（GW）的数据中心关键 IT 电力容量，折合约 730 万颗 H100。而我们估计，仅 Nvidia 一家从 2021 年到 2024 年底就将出货功耗需求相当于 500 万颗以上 H100 的加速器（实际上大部分就是 H100 的出货量），并且我们看到 AI 数据中心容量需求将在 2025 年初突破 10 GW。

![](https://substack-post-media.s3.amazonaws.com/public/images/88b7b56f-ae27-41cd-a9bd-3ff2ce18b727_1162x837.png)
*IEA《Electricity 2024》报告*

上述报告低估了数据中心电力需求，但高估的也大有人在——危言耸听一派中有人翻出写在加速计算普及之前、发表于国际期刊上的[旧论文](https://www.mdpi.com/2078-1547/6/1/117)，宣称最坏情景下到 2030 年数据中心将消耗高达 7,933 TWh，占全球发电量的 24%！

瞧，数据中心蝗虫、戴森球、套娃大脑（Matrioshka Brain）来了！

![](https://substack-post-media.s3.amazonaws.com/public/images/80bb03fa-0fe7-4d92-8b6b-02d5f8d4abef_1355x912.png)
*《On Global Electricity Usage of Communications Technology: Trends to 2030》*

这类信封背面的估算，很多是基于全球互联网协议流量的增长预测，再乘以按效率改进打折后的单位流量功耗——全都是极难估算的数字；另一些则采用 AI 时代之前自上而下做出的数据中心功耗估算。麦肯锡（McKinsey）的估算同样差得可笑，基本等于随手点一个 CAGR，再用精美的图表反复复读。

**让我们在这里把叙事扳正，用实证数据量化数据中心电力危机。**

我们的方法是通过[我们对北美 3,500 多座既有托管（colocation）和超大规模数据中心的分析](https://www.semianalysis.com/p/datacenter-model)来预测 AI 数据中心的供需，包括在建数据中心的施工进度预测；而且在这类研究中，我们首次将该数据库与[我们的 AI 加速器模型](https://www.semianalysis.com/p/accelerator-model)推导出的 AI 加速器电力需求相结合，估算 AI 与非 AI 数据中心的关键 IT 电力供需。我们还结合 [Structure Research](https://www.structureresearch.net/) 整理的北美以外地区（亚太、中国、欧洲中东非洲、拉美）区域汇总估算，以呈现全球数据中心趋势的完整图景。我们以卫星影像和施工进度跟踪单个有代表性的集群和建设项目，作为对区域估算的补充，例如马来西亚新山（Johor Bahru）高达 1,000 MW 的开发管线（主要由中国公司建设）——那里就在新加坡以北几英里处。

这项跟踪按超大规模云厂商逐一进行，而结论很清楚：一些最大的 AI 玩家在中期的可部署 AI 算力上将落后于同行。

AI 热潮确实会快速加速数据中心用电增长，但短期内全球数据中心用电量将远低于「占总发电量 24%」的世界末日情景。我们认为，到 2030 年，AI 将推动数据中心用电占到全球发电量的 4.5%。

![](https://substack-post-media.s3.amazonaws.com/public/images/6463db46-a5e5-497a-8b7f-0b468fbe911d_1411x911.png)
*SemiAnalysis 估算*

## **真正的 AI 超级强权**

未来几年，数据中心电力容量增速将从 12-15% 的 CAGR 加速到 25% 的 CAGR。全球数据中心关键 IT 电力需求将从 2023 年的 49 吉瓦（GW）跃升至 2026 年的 96 GW，其中 AI 将消耗约 40 GW。而现实中的建设不会这么平滑，一场真正的电力紧缺即将到来。

![](https://substack-post-media.s3.amazonaws.com/public/images/1bad42d2-36a2-4c27-b85e-ab8aa4e5d92b_1553x987.png)
*SemiAnalysis 估算*

对充足、廉价电力的需求，对在快速扩充电网容量的同时仍要满足超大规模云厂商碳排放承诺的要求，叠加芯片出口管制，共同决定了哪些国家和地区能够承接 AI 数据中心带来的需求激增。

美国等国家和地区能够以较低的电网碳强度、成本低廉且供应稳定的燃料灵活应对；欧洲等则会被地缘政治现实和电力领域结构性的监管约束死死铐住；还有一些则根本不管环境影响，单纯扩张容量。

## **训练与推理的关键需求**

AI 训练负载有其独特要求，与现有数据中心里部署的典型硬件截然不同。

首先，模型训练要持续数周乃至数月，对网络连接的要求相对局限于训练数据的注入。训练对时延不敏感，不需要靠近任何主要人口中心。在满足数据驻留与合规法规的前提下，AI 训练集群原则上可以部署在全球任何经济上划算的地方。

第二点主要差异也相当直观——AI 训练负载极其耗电，AI 硬件的运行功率比传统非加速的超大规模或企业级负载更接近其热设计功耗（TDP）。此外，CPU 和存储服务器功耗约为 1kW 量级，而如今每台 AI 服务器已突破 10kW。再加上对时延不敏感、是否靠近人口中心的重要性下降，这意味着相对于传统负载，能否获得大量廉价电力（未来甚至只是「能否接入任何电网供电」）对 AI 训练负载的相对重要性要高得多。顺带一提，这些要求中有不少与毫无用处的加密货币挖矿相同，只是后者享受不到单一站点超过 100 兆瓦的规模化效益。

推理则相反，它最终会是比训练更大的负载，但也可以相当分散。芯片不必集中部署，但其绝对规模将十分惊人。

## **数据中心的数学**

AI 加速器能达到较高的利用率（以功耗计，而非 MFU）。每台 DGX H100 服务器在正常运行下的预期平均功率（EAP）约为 10,200 W，折合每台服务器 8 颗 GPU、每颗 1,275W。其中包含 H100 本身 700W 的热设计功耗（TDP），加上分摊到每颗 GPU 约 575W 的部分，用于双路 Intel Xeon Platinum 8480C 处理器、2TB DDR5 内存、NVSwitch、NVLink、网卡（NIC）、重定时器（retimer）、网络收发器等。再加上整个 SuperPOD 的存储与管理服务器以及各类网络交换机的功耗需求，每台 DGX 服务器的有效功耗需求达到 11,112W，即每颗 H100 GPU 1,389W。与 HGX H100 相比，DGX H100 配置在存储等方面略有超配，我们对此做了修正。Meta 等公司已公开了足够多的整机配置信息，足以估算系统级功耗。

![](https://substack-post-media.s3.amazonaws.com/public/images/3d35bdb0-8f62-42a2-a936-182d3f23a9d8_1506x1216.png)
*NVIDIA DGX SuperPOD 数据中心设计*

关键 IT 电力（Critical IT Power）定义为数据中心楼层上可供机柜内计算、服务器和网络设备使用的电力容量，不含数据中心运行制冷、配电及其他设施相关系统所需的电力。要计算本例中需要建设或购买的关键 IT 电力容量，只需把所部署 IT 设备的预期总功率负载加总。在下面的例子中，20,480 颗 GPU、每颗 1,389W，对应 28.4 MW 的关键 IT 电力需求。

要得到 IT 设备预期实际消耗的总功率（关键 IT 电力消耗），需要在关键 IT 电力需求之上乘以一个合理的利用率。这一系数反映了 IT 设备通常不会以 100% 设计能力运行、且 24 小时内的利用强度并不一致的事实。本例中该比值设为 80%。

在关键 IT 电力消耗之上，运营商还必须为制冷供电，并覆盖配电损耗、照明及其他非 IT 设施设备的用电。业界用电源使用效率（PUE）来衡量数据中心的能效，其计算方法是用进入数据中心的总功率除以其中 IT 设备运行所用的功率。这个指标当然有严重缺陷，因为服务器内部的散热也被算作「IT 设备」。我们的处理办法是将关键 IT 电力消耗乘以 PUE。PUE 越低代表数据中心能效越高，PUE 为 1.0 代表完全不耗电于制冷或任何非 IT 设备的完美数据中心。典型企业托管数据中心的 PUE 约为 1.5-1.6，多数超大规模数据中心低于 1.4，一些专门设计的设施（如 Google 的）号称能做到 PUE 低于 1.10。多数 AI 数据中心的设计指标瞄准 PUE 低于 1.3。过去 10 年，全行业平均 PUE 从 2010 年的 2.20 降到 2022 年估计的 1.55，这一直是电力节约的最大来源之一，使数据中心用电避免了失控增长。

举例来说，在 80% 利用率和 1.25 的 PUE 下，这个拥有 20,480 颗 GPU 集群的假想数据中心平均将从电网汲取 28-29 MW 的电力，全年累计 249,185 兆瓦时；按美国平均电价每千瓦时 0.083 美元计算，每年电费为 2,070 万美元。

![](https://substack-post-media.s3.amazonaws.com/public/images/92ae3573-7fc5-4ed1-a1f4-359e0f41187b_1126x943.png)

## **数据中心布局与约束**

虽然 DGX H100 服务器需要 10.2 千瓦（kW）的 IT 功率，但多数托管数据中心目前单机柜仍只能支持约 12 kW 的电力容量，而典型的超大规模数据中心可以提供更高的电力容量。

![](https://substack-post-media.s3.amazonaws.com/public/images/4d2a0109-8514-45f5-addf-6fc5b8c68f7a_1806x1006.png)
*NVIDIA DGX SuperPOD 数据中心设计*

因此，服务器部署方案将随可用供电与制冷能力而变化：在电力/散热受限的地方每机柜只能部署 2-3 台 DGX H100 服务器；而在托管数据中心，整排机柜空间被刻意留空，以把供电密度从 12 kW 提高一倍到 24 kW。这种间隔同样是为了解决制冷超订的问题。

![](https://substack-post-media.s3.amazonaws.com/public/images/538d01af-834d-483b-9b4b-5fb494a95add_2410x840.png)
*NVIDIA DGX SuperPOD 数据中心设计*

随着越来越多数据中心在设计时就以 AI 负载为出发点，通过使用增强气流的专用设备，风冷机柜将能达到 30-40kW 以上的功率密度。未来采用冷板式直冷（direct-to-chip 液冷）则为进一步提高功率密度打开大门：去掉风扇可以[将每机柜功耗降低约 10%](https://www.supermicro.com/white_paper/white_paper_Liquid-Cooling-Solutions.pdf)，减少或取消环境空气冷却可使 PUE 降低 0.2-0.3。不过，在 PUE 已降至 1.25 左右的背景下，这将是最后一波有意义的 PUE 改善。

![](https://substack-post-media.s3.amazonaws.com/public/images/e1a7a62e-6e67-461d-8c69-e122921f02df_1357x954.png)
*Supermicro 液冷白皮书*

许多运营商强调的另一个重要考量是：各 GPU 服务器节点之间应尽量靠近部署，以获得可接受的成本和时延。一条经验法则是，同一集群的机柜距离网络核心不得超过 30 米。短距离使部署可以采用较便宜的多模光收发器，而非昂贵得多、动辄传输数公里的单模光收发器。Nvidia 连接 GPU 与 leaf 交换机的典型多模光收发器的传输距离短至最多 50 米。若要用更长的光纤和更远距离的收发器来迁就更远的 GPU 机柜，就会推高成本，因为需要贵得多的收发器。未来采用其他纵向扩展（scale-up）网络技术的 GPU 集群同样要求极短的线缆距离才能正常工作。例如，在 [Nvidia 面向 H100 集群、尚未部署的 NVLink 纵向扩展网络](https://www.semianalysis.com/p/nvidias-optical-ascent-1b-revenue)中——该网络支持跨 32 个节点、最多 256 颗 GPU 的集群，可提供 57.6 TB/s 的全互联带宽——交换机之间的最大线缆长度将是 20 米。

![](https://substack-post-media.s3.amazonaws.com/public/images/7238a422-8aa2-47cd-946a-7e3093af69e3_2535x1390.png)
*NVIDIA H100 架构白皮书*

机柜功率密度持续走高的趋势，更多是网络、计算效率和单位算力成本驱动的——在数据中心规划中，占地面积成本和数据大厅空间利用率往往只是次要考量。托管数据中心的成本大约 90% 来自电力，只有 10% 来自物理空间。

安装 IT 设备的数据大厅通常只占数据中心总建筑面积的 30-40% 左右，因此把数据大厅设计得大 30%，整个数据中心的总建筑面积只需增加约 10%。考虑到 [GPU 总拥有成本的 80% 来自资本开支](https://www.semianalysis.com/p/gpu-cloud-economics-explained-the)，[另外 20% 与托管相关（其中已包含托管数据中心成本），额外空间的成本仅占 AI 集群总拥有成本的区区 2-3%](https://www.semianalysis.com/p/gpu-cloud-economics-explained-the)。

多数既有托管数据中心还撑不起单机柜 20kW 以上的机柜密度。2024 年芯片产能约束将显著缓解，但某些超大规模云厂商和托管商会一头撞上数据中心容量瓶颈，因为它们对 AI 措手不及——托管数据中心内尤其明显——同时还存在功率密度错配的问题：传统托管的 12-15kW 供电上限，将成为实现 AI 超级集群理想物理密度的障碍。

新建数据中心可以部署后门热交换器和冷板式直冷液冷方案来解决功率密度问题。但是，从零开始把这些方案设计进一座新设施，远比改造既有设施容易——Meta 意识到这一点后，[暂停了原定数据中心项目的开发](https://www.datacenterdynamics.com/en/news/exclusive-after-meta-cancels-odense-data-center-expansion-other-projects-are-being-rescoped/)，将其重新定位为[专门服务 AI 负载](https://www.datacenterdynamics.com/en/analysis/how-meta-redesigned-its-data-centers-for-the-ai-era/)的数据中心。

在所有超大规模厂商中，Meta 的数据中心设计在功率密度上曾是最差的，但他们醒悟并转向得非常快。改造既有数据中心成本高、耗时长，某些情况下甚至根本不可行——可能没有物理空间加装额外的 2-3 MW 柴油发电机、不间断电源（UPS）、开关设备或更多变压器；而为冷板式直冷所需的冷量分配单元（CDU）重新布设管路，也绝非理想做法。

![](https://substack-post-media.s3.amazonaws.com/public/images/f988c129-702b-4f1b-bea9-02d7fc302fd4_2472x1306.png)
*NVIDIA DGX SuperPOD 数据中心设计*

## **AI 需求 vs. 当前数据中心容量**

基于我们的 [AI 加速器模型](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and)，我们按加速器芯片逐项做出出货量预测，结合我们估算的芯片规格和建模的配套设备功率需求，计算未来几年 AI 数据中心关键 IT 电力总需求。

![](https://substack-post-media.s3.amazonaws.com/public/images/dd411a4d-2b02-4f43-a20b-888a04a64de2_1553x987.png)
*SemiAnalysis 估算*

如前所述，数据中心关键 IT 电力总需求将从 2023 年的约 49 GW 翻倍至 2026 年的 96 GW，其中 90% 的增长来自 AI 相关需求。这只是从芯片需求出发的推算，而[实体数据中心](https://www.semianalysis.com/p/datacenter-model)讲述的是另一个故事。

没有哪里比美国更能感受到这种冲击。我们的卫星数据显示，大多数 AI 集群正在美国部署和规划，这意味着美国的数据中心关键 IT 容量从 2023 年到 2027 年需要增长两倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/2f8168e8-e7ca-4006-bab6-e93b55151e83_1698x514.png)
*SemiAnalysis 估算*

主要 AI 云厂商激进的加速器上量计划印证了这一点。OpenAI 计划在其最大的多站点训练集群中[部署数十万颗 GPU](https://www.semianalysis.com/p/microsoft-swallows-openais-core-team)，这需要数百兆瓦的关键 IT 电力。[通过观察实体基础设施、发电机和蒸发冷却塔的建设进展，我们可以相当精确地跟踪其集群规模](https://www.semianalysis.com/p/datacenter-model)。Meta 提到其到年底的装机量相当于 650,000 颗 H100。GPU 云厂商 CoreWeave [计划向得克萨斯州 Plano 的一处设施投资 16 亿美元](https://www.datacenterdynamics.com/en/news/coreweave-plans-16bn-ai-cloud-data-center-in-plano-texas/)，意味着其计划投入建设高达 50 MW 关键 IT 电力、仅在该设施就安装 30,000-40,000 颗 GPU，并有一条通往全公司 250 MW 数据中心版图（相当于 180k 颗 H100）的清晰路径，而且他们还在规划单一站点数百 MW 的项目。

微软在 AI 时代之前就已拥有最大的数据中心建设管线（见下方 2023 年 1 月数据），而[我们的数据显示此后更是直线飙升](https://www.semianalysis.com/p/datacenter-model)。他们一直在狼吞虎咽地吃进一切能拿到的托管空间，同时激进扩张自建数据中心。[亚马逊这样的 AI 落后者](https://www.semianalysis.com/p/amazons-cloud-crisis-how-aws-will)发布了合计 1,000 MW 核电数据中心的新闻稿，但要说清楚的是，由于是[最后一家对 AI 幡然醒悟的超大规模厂商](https://www.semianalysis.com/p/amazons-cloud-crisis-how-aws-will)，他们在真正意义上的近期建设上是实质性滞后的。Google 与 Microsoft/OpenAI 双方都有超过吉瓦级训练集群的计划在酝酿中。

![](https://substack-post-media.s3.amazonaws.com/public/images/280f1cf9-216f-472b-86d6-0b817c5255b5_2953x1654.png)
*Structure Research*

从供给侧看，卖方一致预期 Nvidia 在 2024 自然年出货 3M+ 颗 GPU，这对应超过 4,200 MW 的数据中心需求——接近当前全球数据中心容量的 10%，而这还只是一年的 GPU 出货量。当然，市场对 Nvidia 出货量的一致预期本身也错得离谱。退一步讲，AI 在之后几年只会更大，而 Nvidia 的 GPU 还[将变得更加耗电](https://www.semianalysis.com/p/nvidias-plans-to-crush-competition)，路线图上有 1,000W、1,200W 和 1,500W 的 GPU。Nvidia 也不是唯一生产加速器的公司——[Google 正在快速提升自研加速器的产量](https://www.semianalysis.com/p/broadcoms-google-tpu-revenue-explosion)。往后，Meta 和亚马逊也将提升各自自研加速器的产量。

全球顶级超大规模厂商显然没有忽视这一现实——他们正在快速加码数据中心建设和托管租赁。AWS 豪掷 6.5 亿美元买下了一座 1,000 MW 的[核能供电数据中心园区](https://www.datacenterdynamics.com/en/news/aws-acquires-talens-nuclear-data-center-campus-in-pennsylvania/)。虽然近期上线的很可能只是第一栋 48 MW 容量的建筑，但这为 AWS 提供了一条宝贵的数据中心容量管线，不必苦等发电或电网输电容量。我们认为，如此庞然大物级别的园区需要很多年才能完全爬坡到承诺的 1,000 MW 关键 IT 电力。

![](https://substack-post-media.s3.amazonaws.com/public/images/e94eed35-8a5b-44c1-a02e-6aeae001a145_1886x1078.png)
*Datacenter Dynamics*

## **AI 训练与推理的碳成本与电力成本**

了解主流模型的训练功耗，有助于评估电力需求、理解 AI 行业产生的碳排放。[《Estimating the Carbon Footprint of BLOOM, a 175B Parameter Language Model》](https://arxiv.org/abs/2211.02001)考察了在法国国家科学研究中心（CNRS）旗下 IDRIS 的 Jean Zay 计算集群上训练 BLOOM 模型的用电情况。该论文提供了关于 AI 芯片 TDP 与集群总用电量（包括存储、网络及其他 IT 设备）直至电网实际取电量的关系的实证观察。

另一篇论文[《Carbon Emissions and Large Neural Network Training》](https://arxiv.org/abs/2104.10350)报告了另外几个模型的训练时长、配置和功耗。训练的电力需求会因模型与训练算法的效率（对模型 FLOPS 利用率 MFU 的优化）以及整体网络与服务器能效和利用率而异，但下面转载的结果仍是有用的标尺。

![](https://substack-post-media.s3.amazonaws.com/public/images/37d56f20-7ac9-419c-b1cf-a1ada44c0838_1518x632.png)
*《Estimating the Carbon Footprint of BLOOM, a 176B Parameter Language Model》《Carbon Emissions and Large Neural Network Training》*

这些论文估算训练碳排放的方法，是把以千瓦时计的总功耗乘以数据中心所在[电网的碳强度](https://www.epa.gov/egrid/data-explorer)。眼尖的读者会注意到，在法国训练 BLOOM 模型的碳强度低至 0.057 kg CO2e/kWh——法国 60% 的电力来自核电，远低于[美国 0.387 kg CO2e/kWh 的平均水平](https://www.epa.gov/egrid/data-explorer)。我们还额外提供了一组计算，假设这些训练任务在接入亚利桑那州电网的数据中心上运行——该州是当前数据中心建设最活跃的州之一。

排放拼图的最后一块是内含排放（embodied emissions），定义为制造和运输某一设备所产生的总碳排放，此处指加速器芯片及相关 IT 设备。AI 加速芯片内含排放的扎实数据很稀缺，但有人粗略估算为每颗 A100 GPU 150 kg CO2e、每台搭载 8 颗 GPU 的服务器 2,500 kg CO2e。内含排放约占一次训练总排放的 8-10%。

![](https://substack-post-media.s3.amazonaws.com/public/images/5dbf1092-7f5c-4a15-8b4c-ce80d891c6ef_1458x991.png)
*《Estimating the Carbon Footprint of BLOOM, a 176B Parameter Language Model》《Carbon Emissions and Large Neural Network Training》、EPA eGrid、SemiAnalysis 估算*

这些训练运行的碳排放并非小数：一次 GPT-3 训练产生 588.9 公吨 CO2e，相当于[128 辆乘用车一年的排放](https://www.epa.gov/greenvehicles/greenhouse-gas-emissions-typical-passenger-vehicle)。但对 GPT-3 训练排放大加指责，就像回收塑料水瓶然后每隔几个月坐一次飞机——纯属无关痛痒的道德表演。

反过来说，几乎可以肯定，在最终模型定稿之前经历了多轮训练迭代。2022 年，Google 包括数据中心在内的各类设施[共排放 8,045,800 公吨 CO2e](https://sustainability.google/reports/google-2023-environmental-report/)，这还未计入可再生能源项目的任何抵消。这一切说明，GPT-3 并没有影响全球碳输出；但 GPT-4 的 FLOPS 高出多个数量级，而 OpenAI 正在进行的训练又比之再高出一个数量级以上——几年之内，训练的碳排放将开始变得可观。

推理方面，我们在[GPU 云经济学](https://www.semianalysis.com/p/gpu-cloud-economics-explained-the)和[Groq 推理代币经济学](https://www.semianalysis.com/p/groq-inference-tokenomics-speed-but)两篇文章中详细分析了 AI 云托管的经济学。一台典型的 8 GPU H100 服务器每月将排放约 2,450 kg CO2e，需要 10,200 W 的 IT 功率——按每千瓦时 0.087 美元计算，每月电费 648 美元。

![](https://substack-post-media.s3.amazonaws.com/public/images/cb6ee4a0-5d69-466b-965f-fc42ebd93924_1912x1365.png)
*SemiAnalysis 估算*

## **大规模建设 AI 基础设施——什么才算真正的 AI 超级强权？**

AI 数据中心产业将需要以下条件：

- 极低的电力成本，因为需要持续消耗海量电力，尤其是推理需求只会随时间复利式增长。
- 能源供应链在地缘政治和天气扰动下的稳定与强韧，以降低能源价格剧烈波动的可能性，同时具备快速提升燃料产量、从而大规模快速部署发电的能力。
- 整体低碳强度的发电组合，并具备大规模上马可在合理经济性下发电的可再生能源的条件。

能够挺身而出、把这些条件全部打钩的国家，才是「真正的 AI 超级强权」的竞争者。

## **电价、发电结构与碳强度**

![](https://substack-post-media.s3.amazonaws.com/public/images/6fec2a9c-7a44-4eaa-83c3-55049d3174c6_2446x1464.png)
*美国 EIA、各国及区域电力配送机构*

比较全球电价，美国属于世界上电价最低的国家之列，平均为每千瓦时 0.083 美元。美国天然气产量充足，自[2000 年代初的页岩气革命](https://www.strausscenter.org/energy-and-security-project/the-u-s-shale-revolution/)以来激增，使美国成为全球最大的天然气生产国。美国近 40% 的发电以天然气为燃料，低发电成本主要源于页岩层干气产量充足。由于页岩油压裂和油井伴生气占比不断上升，美国天然气价格将持续低迷——那些每隔几周就来向我们念叨数据中心用电的天然气多头，可以消停了。

美国在天然气上的能源自给为价格增添了地缘政治稳定性，气田遍布全美则增强了供应链韧性，而[相当于 20 年消费量的已探明储量](https://www.eia.gov/energyexplained/natural-gas/how-much-gas-is-left.php)保证了能源供应的长期性——何况这些储量估算多年来还在不断上调，自 2015 年翻了一番，仅 2021 年就增长了 32%。

![](https://substack-post-media.s3.amazonaws.com/public/images/bf313653-f6bd-4ea6-894c-e5ebd258ff9a_1891x1273.png)
*美国能源信息署（EIA）*

此外，美国的能源结构比大多数其他竞争者绿色得多：煤电占比已从 2012 年的 37% 降至 2022 年的 20%，随着天然气和可再生能源补位，预计到 2030 年将降至 8%。相比之下，印度煤电占比为 75%，中国为 61%，就连日本 2022 年仍有 34%。这一差异影响巨大：燃煤电厂的[碳强度为 1.025 kg/kWh CO2e，是天然气电厂 0.443 kg/kWh CO2e 的两倍多](https://www.eia.gov/todayinenergy/detail.php?id=48296)。因此，建在美国的数据中心，其必需的基础负荷与夜间发电所依赖的燃料组合，要比许多国家清洁得多。

![](https://substack-post-media.s3.amazonaws.com/public/images/6e1d9b5b-6ebd-47d6-9643-d5355df394b8_2055x1377.png)
*美国能源信息署（EIA）*

美国的能源供应状况，与分别承载全球约 15% 和 18% 数据中心容量的东亚和西欧形成鲜明反差。美国天然气自给自足，而日本、台湾、新加坡、韩国等国家和地区的天然气和煤炭需求九成以上依赖进口。

日本的发电结构偏向这些进口燃料：天然气占 35%、煤占 34%、水电占 7%、核电占 5%，导致 2022 年平均工业电价为每千瓦时 0.152 美元，比美国的 0.083 美元高出 82%。台湾和韩国的发电结构类似，以进口天然气为主，电价约为每千瓦时 0.10 到 0.12 美元——但这是在每千瓦时 0.03 到 0.04 美元的实际补贴之后，因为两地国有电力公司巨额亏损：韩国 [KEPCO 2022 年亏损 240 亿美元](https://www.ft.com/content/3533347c-cd50-4e42-bd15-e48173b003d7)，台湾的台电[每卖出一度电亏损 0.04 美元](https://www.taiwannews.com.tw/en/news/4839443)。

在东盟，新加坡是另一个数据中心枢纽，其发电结构的 90% 严重依赖进口天然气，2022 年电价高达每千瓦时 0.23 美元。新加坡承载的 900 MW 关键 IT 电力相对其发电能力而言规模很大，消耗了新加坡全国发电量的 10% 以上。为此，新加坡曾对新数据中心建设实施为期四年的暂停令，直到 2023 年 7 月才解除，且仅批准了区区 80 MW 新容量。这一限制催生了隔壁马来西亚新山——就在新加坡以北几英里——高达 1,000 MW 的庞大开发管线，其中很大一部分由试图「国际化」、日益与中国母公司保持距离的中国公司推动。印度尼西亚也有可观的管线。

中国每千瓦时 0.092 美元的工业电价处于全球电价区间的低端，但与许多其他新兴市场一样，中国的发电结构非常「脏」，61% 的发电来自煤炭。这在排放角度是重大劣势，而且尽管中国在可再生能源装机上大幅领先全球，新的燃煤电厂仍在获批。任何做出净零排放承诺的超大规模或 AI 公司，在实现该目标的路上都将是一场苦战——煤炭的[碳强度为 1.025 kg/kWh CO2e，天然气为 0.443 kg/kWh CO2e](https://www.eia.gov/todayinenergy/detail.php?id=48296)。

![](https://substack-post-media.s3.amazonaws.com/public/images/e6e8efac-1e93-41c4-8364-7db3182dafad_2275x1521.png)
*Ember Electricity*

中国在发电用煤上基本自给，但其他能源需求绝大部分依赖进口，其七成以上的石油和 LNG 经马六甲海峡运输，因此受制于所谓的「[马六甲困局](https://gjia.georgetown.edu/2023/03/22/chinas-economic-security-challenge-difficulties-overcoming-the-malacca-dilemma/)」。这意味着出于战略原因，中国无法转向天然气，只能依靠增加煤电和核电来保障基础负荷发电。中国确实在新增可再生能源装机上领先全球，但其庞大的既有火电基数和继续依靠新增煤电扩大总容量的做法，意味着 2022 年可再生能源仅占总发电量的 13.5%。

需要说明，中国是全世界最擅长新建发电能力的国家；如果被允许，他们很可能在吉瓦级数据中心建设上领先全球——但他们不被允许，所以美国在这里占主导地位。

![](https://substack-post-media.s3.amazonaws.com/public/images/c1b41678-81d7-4f60-8245-7d25d97b0346_787x602.png)
*美国能源信息署（EIA）*

而以上还未正面直视屋里的大象——即美国工业与安全局（BIS）推出的[持续进行中的 AI 半导体出口管制](https://www.semianalysis.com/p/wafer-wars-deciphering-latest-restrictions)，其意图几乎是完全禁止中国获得任何形式的 AI 芯片。在这方面，出口管制的「打地鼠」游戏仍在继续，Nvidia 不断调整芯片以[符合管制的最新变化](https://www.semianalysis.com/p/nvidias-new-china-ai-chips-circumvent)。H20 从二季度起将在中国市场大幅上量，但这仍远达不到被允许情况下中国本会进口的、占 AI 芯片 35% 到 40% 的份额。

在西欧，发电量一直在缓慢下降，过去五年累计下降 5%。原因之一是核电在政治上成为禁区，导致核电发电量大幅下滑——例如德国核电从 2007 年到 2021 年下降了 75%。对「环境」的高度关注也使煤炭等高污染燃料在同一时期急剧减少，尽管在某些情况下，世界上最清洁的电源核电被煤炭和天然气所取代。可再生能源在欧洲发电结构中的占比在上升，但速度不够快，迫使许多欧洲国家慌忙转向更多天然气——目前天然气占西欧主要国家发电结构的 35-45%。

![](https://substack-post-media.s3.amazonaws.com/public/images/a619727c-e1d8-4d83-acb1-f67ad8d6a4c2_2059x1378.png)
*Ember Electricity*

鉴于欧洲的能源形势，2022 年欧盟平均工业电价达到每千瓦时 0.18 美元，英国为 0.235 美元，数据中心重镇爱尔兰为 0.211 美元——接近美国电力成本的三倍。与亚洲一样，欧洲九成以上的天然气以 LNG 形式进口，主要来自中东（尽管战事仍在继续，也依然[来自俄罗斯](https://www.reuters.com/business/energy/lng-imports-russia-rise-despite-cuts-pipeline-gas-2023-08-30/)）。因此，欧洲整个工业基础——不只是数据中心——都暴露在地缘政治风险之下，多数读者对乌克兰战争爆发时的情景应该还记忆犹新。鉴于政治与地缘政治现实，要在欧洲新增海量发电能力来承接 AI 数据中心热潮，将非常艰难。

而且，欧洲对「搞建设」过敏——针对数据中心和制造业的诸多现行法规与限制就是证明。虽然一些小型数据中心项目和管线正在推进——尤其是在至少多少意识到了地缘政治必要性的法国——但没有人打算在欧洲建吉瓦级集群。据我们估算，欧洲已部署的 AI 加速器 FLOPS 不到全球的 4%。

如前所述，考虑到待部署 AI 集群的规模，电价将产生重大影响，集群选址不同可带来数亿美元的成本差异。把 AI 数据中心放在欧洲或亚洲，电力成本轻而易举就会是在美国建设的两到三倍。此外，由于技能人才短缺，建设成本也更高。

中东是另一个正在竞相启动数据中心建设的地区，按「真正的 AI 超级强权」的部分标准衡量，它得分很高：电价位居全球最低之列，太阳能利用的可行性非常高。事实上，中东拥有非常强劲的管线，预计阿联酋的数据中心关键 IT 电力将从 2022 年的 115 MW 增至 2026 年的 330 MW，接近三倍。

沙特阿拉伯也已经入局，其研究机构迄今[仅购买了区区 3,000 颗 H100](https://www.ft.com/content/c93d2a76-16f3-4585-af61-86667c5090ba)，并计划自建 LLM。继 2022 年[启用的卡塔尔数据中心](https://news.microsoft.com/en-xm/2022/08/31/microsoft-opens-first-global-datacenter-region-in-qatar-bringing-new-opportunities-for-a-cloud-first-economy/)之后，微软也宣布了在沙特建立数据中心的计划。不过领跑者仍是沙特：当前关键 IT 电力为 67 MW，但计划在未来几年一举超越阿联酋，达到 530 MW。

与此同时，刚刚走出隐身模式的 AI 初创公司 Omniva，据称计划在中东建设低成本 AI 数据中心设施，并得到一位科威特王室成员的重金支持。其核心团队中有来自 AWS、Meta 和微软的干将。他们是唯一真正在实地推进并取得实际进展的玩家，人才背景也最亮眼——但他们与 Meta 之间还有一场官司：Meta 起诉了一名员工，指控其窃取文件并挖走 8 名前员工加入。

**接下来我们将量化电价差异、变压器基础设施、发电能力，并按 UPS、发电机、开关设备、配电、CRAH/CRAC、冷水机组、冷却塔、阀门/管道/水泵、项目管理与设施工程、照明、管理、安防、IT 机柜与封闭、架空地板/吊顶、消防等类目，拆解全球数据中心资本开支需求。**

**我们还将专门深入探讨 Meta 的建设情况，讨论可再生能源侧太阳能与风电的优劣，以及部署此类电力的区域差异，并涉及储能能力与碳排放。**

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

![](https://substack-post-media.s3.amazonaws.com/public/images/9d2bade3-4a05-402f-9ee6-c45e4a3403cb_970x1060.png)
*美国 EIA、各国及区域电力配送机构*
