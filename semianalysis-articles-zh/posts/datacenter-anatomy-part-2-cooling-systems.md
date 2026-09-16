---
title: "数据中心解构 第二部分——冷却系统"
title_en: "Datacenter Anatomy Part 2 – Cooling Systems"
subtitle: "L2A、L2L、浸没式、相变冷却，Google vs Meta vs Microsoft vs Amazon 水冷设计，WUE、PUE、Nvidia Rubin 供电与冷却架构"
date: 2025-02-13
source: https://newsletter.semianalysis.com/p/datacenter-anatomy-part-2-cooling-systems
crawled: 2026-09-15
authors: ["Jeremie Eliahou Ontiveros", "Dylan Patel", "Daniel Nishball", "Reyk Knuhtsen"]
tags: ["Datacenter", "Hardware Architecture"]
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 数据中心解构 第二部分——冷却系统

> 原文：[Datacenter Anatomy Part 2 – Cooling Systems](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-2-cooling-systems) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**L2A、L2L、浸没式、相变冷却，Google vs Meta vs Microsoft vs Amazon 水冷设计，WUE、PUE、Nvidia Rubin 供电与冷却架构**

集群部署的规模已提升了一个数量级，[吉瓦级数据中心以远超大多数人想象的速度满负荷上线](https://semianalysis.com/datacenter-industry-model/)。因此，规划未来站点的数据中心开发者必须考虑相当大的设计变化。我们此前已经讨论过[数据中心的电气系统](https://semianalysis.com/2024/10/14/datacenter-anatomy-part-1-electrical/)，以及生成式 AI 的崛起如何影响数据中心设计与设备供应商。在本系列探讨数据中心基础设施与技术的第二部分中，我们将聚焦冷却系统。

Nvidia 在 3 月宣布其[最先进的 AI 计算平台](https://www.semianalysis.com/p/nvidia-b100-b200-gb200-cogs-pricing)将是一个 120kW、72 GPU 的机柜，且完全采用冷板式直冷（DLC）冷却，震动了整个数据中心行业。[Nvidia GB200 NVL72 系统将为大语言模型（LLM）推理和训练提供最佳的总拥有成本（TCO）](https://semianalysis.com/2024/04/10/nvidia-blackwell-perf-tco-analysis/)，并将在[按 scaling law 推进能力进步](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/)以及[降低 o3 等推理模型成本](https://semianalysis.com/2024/12/25/nvidias-christmas-present-gb300-b300-reasoning-inference-amazon-memory-supply-chain/)方面发挥关键作用。因此，GB200 NVL36/72 将成为 [Blackwell 产品家族中出货量最高的 SKU](https://semianalysis.com/accelerator-industry-model/)——而这仅仅是 Nvidia 极其激进的路线图的开始。

![](https://substack-post-media.s3.amazonaws.com/public/images/f7108144-2a57-4f8a-b820-db5381afce35_1024x414.png)
*来源：SemiAnalysis 数据中心模型*

DLC 并不是一项新技术，但它长期被局限于对成本不敏感、机柜功率密度 >100kW 的政府研发超算领域——以及 [Google 的定制 AI 基础设施](https://www.semianalysis.com/p/google-ai-infrastructure-supremacy)。在更广阔的市场中，机柜功率密度一直在缓慢上升：从 2010 年代每柜至多 5-10kW，提高到现代云计算数据中心普遍的 15-20kW。超大规模时代带来的是运营规模的扩大，但数据中心底层设计并未发生根本变化。

## 即将爆发的数据中心冷却市场

在数据中心的关键系统中，冷却可以说是演进最快、学习曲线最陡、并给数据中心运营方带来执行风险的领域。大型项目通常需要数十亿美元的资本开支（capex），因此利害关系极大。数据中心需求的快速演进也放大了在建资产迅速过时的风险。

液冷需求被低估了，这将导致低效的「桥式」过渡方案增多，因为具备液冷能力的数据中心会供不应求。为了量化这一点，我们构建了[逐芯片的液冷市场模型与预测](https://semianalysis.com/accelerator-industry-model/)，以及[逐站点的未来数据中心产能追踪器](https://semianalysis.com/datacenter-industry-model/)。

![](https://substack-post-media.s3.amazonaws.com/public/images/26e83220-36dc-45f8-bef3-91ba8ca912ff_1642x867.png)
*来源：SemiAnalysis 数据中心模型*

本报告是数据中心冷却系统的全面入门读物。第一部分解释数据中心冷却的基础概念并介绍关键设备。报告第二部分聚焦当前超大规模云厂商的自建设计，并解释其实现一流冷却效率的方法论——[依据是其旗舰 AI 数据中心的实时卫星影像](https://semianalysis.com/datacenter-industry-model/)。

![](https://substack-post-media.s3.amazonaws.com/public/images/32cb508a-3638-4bb4-aa1f-f032ec4478c1_1024x587.png)
*来源：SemiAnalysis 数据中心模型*

我们还将结合 Nvidia 及其关键客户的路线图讨论数据中心冷却的未来。我们将解释各家超大规模云厂商如何适应市场条件，以及为使基础设施适应生成式 AI（GenAI）时代而做出的重大设计转变。每家超大规模云厂商采取的路径各不相同，审视这些做法会引出有趣的供应链影响。我们还会讨论 Oracle 和字节跳动（Bytedance）在马来西亚的情况。

最后，我们将讨论关键供应商及其业务受到的影响。Nvidia 的大规模爬坡正在导致一些乍看很简单的组件出现短缺，例如快接头（Quick Disconnect）！虽然所有厂商都会从被低估的数据中心资本开支 boom 中受益，但底层设计变化会带来相对的赢家和输家。

## 数据中心冷却基础

三十年前，数据中心的 HVAC（供暖、通风与空调）与办公楼类似，直接沿用办公或商用设备，只是配备了更强化的空调（AC）和/或空气处理机组（AHU）。但现代数据中心单位面积产生的热量是办公楼的 >50 倍，且向 IT 设备供电普遍超过 30MW（全部转化为热量），行业因此转向了更加专业化的解决方案。这些复杂系统的目标是让 IT 设备维持在最优温度区间——例如 DGX H100 为 5°C 至 30°C 之间。超出该区间运行会缩短设备寿命——这在经济上并不划算，因为服务器及相关硬件占数据中心总拥有成本（TCO）的最大份额。

![](https://substack-post-media.s3.amazonaws.com/public/images/3cdf6c0b-b8b6-4769-aa0d-63ef8df5db44_2202x708.png)
*来源：Nvidia*

在当今的数据中心中，冷却系统是仅次于电气系统（不计 IT 设备）的第二大资本开支项。由于其架构多样、且对运营开支（opex）——尤其是能源，云服务提供商（CSP）最大的可变成本——影响重大，它也许已成为最关键的设计考量。与非 IT 设备相关的电力消耗（其中大部分是冷却）纯属非生产性支出，应当尽量压缩——但这存在取舍。

![](https://substack-post-media.s3.amazonaws.com/public/images/638df528-29b5-41f1-aa7e-76efdec81e66_2427x1804.png)
*来源：SemiAnalysis 数据中心模型*

## **冷却系统与能效**

比较设施能效的行业标准是电源使用效率（PUE）比率，即设施总功率除以 IT 总功率。PUE 为 1.5 意味着每 1 瓦 IT 负载，数据中心就要为冷却、电力转换损耗和照明等其他小项额外消耗 0.5 瓦。

Uptime Institute 测算的行业平均 PUE 约为 1.6。虽然许多分析师和营销图表直接采信该数字，但它并不能代表整个行业——其依据的调查基本未涵盖超大规模云厂商，且只是规模大于 4MW 的受访数据中心的简单平均。Google 和 Meta 的运行 PUE 都在 1.1 左右，Microsoft 和 AWS 约为 1.15——我们将在报告后文探讨它们是如何做到的。

![](https://substack-post-media.s3.amazonaws.com/public/images/3ece32c3-b004-47d3-994a-a1c3071a1821_1564x1312.png)
*来源：Uptime Institute*

值得注意的是，PUE 可以被人为操纵，并不总能实现公平比较。例如，服务器风扇功耗通常计入 IT 负载。这意味着当比较其他方面完全相同的风冷与液冷服务器时，后者尽管总功耗更低，却可能因服务器风扇功耗更低而显示更高的 PUE。业界虽已提出替代指标，但 PUE 仍是行业标准。

经验法则上，非 IT 电力消耗的典型构成如下：

- 60-80%：冷却系统，主要是冷水机组，其次是风机和水泵。
- 15-30%：[电气系统](https://semianalysis.com/2024/10/14/datacenter-anatomy-part-1-electrical/)——主要是 UPS 电力转换、配电损耗和变压器效率损失。
- 5-20%：照明及其他——数据中心通常包含一小块办公区。

## **风冷数据中心架构**

现在来看托管（Colocation）数据中心的常见设计。主要冷却组件包括数据大厅内的室内冷却单元、冷水机组和冷却塔。某些情况下冷水机组与冷却塔可能集成一体。这些组件通过相互隔离的液体回路协同工作，高效传递热量。

![](https://substack-post-media.s3.amazonaws.com/public/images/b0eba30b-cf7e-431b-a82b-aac10c2900f8_1200x668.jpeg)
*来源：Accuspeclnc*
![](https://substack-post-media.s3.amazonaws.com/public/images/6e3ac764-1315-451c-88b0-b7482aad5932_1712x1140.png)
*来源：三菱重工业（Mitsubishi Heavy Industries）*

在数据中心里，热量以下列方式从 IT 设备流向外部环境：

- 机柜层面，IT 设备产生热量，由 IT 服务器内部的风机排出。热空气被吹入数据大厅。
- 室内冷却单元——通常是 CRAC（Computer Room Air Conditioner，机房空调）或 CRAH（Computer Room Air Handler，机房空气处理机）——带走数据大厅的热量。冷水（或其他流体）在这些机组的盘管内循环。热回风吹过盘管，把热量传递给设施水，再由泵送回冷水机组。

![](https://substack-post-media.s3.amazonaws.com/public/images/6c1f7eb2-5b83-4c34-8293-27baca7e0c6b_660x340.png)
*来源：MEPacademy*

- 冷水机组执行制冷循环——一个耗能的降温过程。它把水中的热量转移给另一种叫做「制冷剂」的流体。升温后的制冷剂被压缩以进一步提高温度，随后流经名为冷凝器的热交换器——冷凝器要么是风冷式（风机把热量排到外部空气中），要么是水冷式（由连接冷却塔的独立冷却回路构成）。制冷剂在冷凝器中降温，以低得多的温度返回。冷却塔最终把冷凝器水中的热量交换到外部环境。
- 数据大厅的热量被带走后，循环重新开始，冷水再次供给室内冷却单元。这一持续过程所需能耗和水耗因系统设计而异。

![](https://substack-post-media.s3.amazonaws.com/public/images/cd8444e2-c6e6-412a-b1fb-17f49ba843a1_1423x1100.png)
*来源：Alpine Intel*

下面我们逐一放大观察各回路中冷却系统的组成部件。

## **服务器热管理与气流**

热流从数据大厅开始：IT 设备耗电会直接产生热量作为副产物——每 1 千瓦供给 IT 设备的电力大约产生 1 千瓦热量。芯片厂商通过热设计功耗（TDP）标定芯片或系统可承受的最大热量，为热设计工程师设计合适的冷却方案提供依据。过去 5-10 年，芯片 TDP 持续上行。AI 加速器让这一轨迹继续变陡，[明年将有 1500W 的芯片出货](https://semianalysis.com/datacenter-industry-model/)。

![](https://substack-post-media.s3.amazonaws.com/public/images/f0a88ffc-36a9-4535-984e-ade19beac708_1614x1110.png)
*来源：SemiAnalysis*

从芯片说起：在风冷服务器中，裸片（die）上方覆有热界面材料（TIM），把芯片封装本身的热量传导到均热片或散热器。

![](https://substack-post-media.s3.amazonaws.com/public/images/47eb8352-e3f6-4c10-9c6c-97c73df1bbbc_1296x389.webp)
*来源：TSMC*

在风冷服务器中，裸片（die）上方覆有热界面材料（TIM），将热量传导至均热片或散热器。散热器通过增大表面积来降低热流密度（单位面积热量），从而提升冷却性能。芯片发热越高，就需要越大的散热器，NVIDIA H100（700W TDP）上的超大散热器便是一例。这些超大散热器正是 Nvidia H100 服务器通常占用 8 个机柜单位（RU）的原因之一，而功耗低得多的 CPU 服务器可以装进 1U 或 2U 的机箱。

![](https://substack-post-media.s3.amazonaws.com/public/images/bfaeba0a-4f6e-45cb-b4dc-9dc108a45185_1170x663.jpeg)
*来源：SVA.de*

服务器风机排出内部各组件产生的总热量，在典型 H100 服务器中，GPU 和 CPU 占了最大头。散热器必须有足够的气流来带走热量——每千瓦热量需要 165 至 170 立方英尺每分钟（CFM）的气流，是常用的经验法则。

![](https://substack-post-media.s3.amazonaws.com/public/images/92c7f31f-cc67-4e8a-9787-f89c59f2e513_880x880.png)
*来源：Gigabyte*

服务器风机的功耗可能相当可观，这促使超大规模云厂商自行设计定制服务器，而不是向 Dell、Supermicro 等厂商采购现成产品。Nebius——一家拥有超大规模级别资源的新兴 GPU 云（[neocloud](https://semianalysis.com/2024/10/03/ai-neocloud-playbook-and-anatomy/)）——最近的数据展示了定制服务器设计如何降低能耗。

![](https://substack-post-media.s3.amazonaws.com/public/images/a18fb645-442f-48fe-950c-1d04edb1978f_1454x548.png)
*来源：Nebius，OCP Global Summit 2024*

温度与能耗的关系由 **Delta T**（服务器进风口与出风口的温差）决定。Delta T 通过以下方式影响能耗：

- 在冷却系统中，温差越高，散热所需的气流或泵送功率越少——这一关系是线性的。
- 尽管所需气流随 Delta T 线性变化，实现不同气流所需的能耗却不是线性缩放。根据风机定律（Fan Law）物理，风机能耗与风机转速的三次方成正比：转速（即气流）降低 10%，能耗降低 27%。
- 更高的芯片利用率更节能，因为发热增加会拉大出风相对进风的温差，形成更大的 Delta T。

## **能效低下的冷却系统解剖**

下面深入看典型运行温度及其在冷却系统设计与效率中的关键作用。下图展示了一个传统「低效」风冷数据中心的运行方式：

- 服务器进风 22°C——即空气进入服务器的温度。
- 室内冷却单元盘管中冷冻水温度 7°C，吸热后升至 13°C——空气处理机组处 Delta T 为 6°C。
- 在全球大多数地区，把水冷却到 7°C 需要大量电力，主要消耗于冷水机组的制冷循环。如此低的冷冻水温度承袭自办公或商用 HVAC 系统。把水冷冻到如此低温的能耗成本，远超过服务器风机降速带来的节省。

![](https://substack-post-media.s3.amazonaws.com/public/images/ca3bc359-eb1d-46e0-9a62-42a3d56c1f62_1289x741.png)
*来源：Supermicro，Hot Chips 2024*

过去十年，数据中心运营商越来越多地采用更高的进风温度——远高于 22°C——并发现这实际上并不会损害 IT 设备寿命。下表来自美国 HVAC 标准机构 ASHRAE，建议服务器干球（即空气）温度在 18°C 至 27°C 之间。但超过 30°C 也是允许的，某些情况下气温甚至可以高达 45°C——尽管「A4」服务器等级更偏军工类应用。

![](https://substack-post-media.s3.amazonaws.com/public/images/f1f904e1-3789-43c2-af51-d9cca0c881a5_919x1201.png)
*来源：ASHRAE*

审视 Supermicro 的示意图会引出一个重要问题：为什么进入数据大厅空气处理机组的 7°C 进水，最终只产生 22°C 的服务器进风温度？这一显著温差往往源于糟糕的气流管理。Upsite Technologies 提出了「四个 Delta T」概念，把这一温差拆解为数据大厅不同区域的若干离散 Delta T：

![](https://substack-post-media.s3.amazonaws.com/public/images/d43baf68-278f-4b86-a56e-69aea5d6cd05_504x360.png)
*来源：Upsite*

1. 服务器进风与回风之间的温差。
2. 数据大厅气流湍流/混合 Delta T：由大厅内热回风与冷送风混合造成的负温差。
3. 数据大厅空气处理机组 Delta T：盘管进水温度与吸热后回风温度之间的温差。
4. 二次空气混合 Delta T：冷回风与热排风混合造成的正温差。通过高效气流管理尽量减小该温差，可确保进风冷气保持温度。注意图中所示为架空地板（Raised Floor），但由于冷却能力（风量）受限且成本较高，现代数据中心已不流行。

为减少「空气混合」，需要使用通道封闭（Containment）系统来隔离空气。下图展示的是热通道封闭（Hot Aisle Containment），冷通道封闭同样存在且理论上效率相当。热通道封闭需要特定的吊顶设计，不适合改造项目；冷通道封闭则让维护更困难（因为室内非常热），导致部分运营商部署效率不高。现代化新建数据中心普遍采用热通道封闭。

![](https://substack-post-media.s3.amazonaws.com/public/images/e926ca9a-1f67-4a5a-8742-e362fb741511_945x518.png)
*来源：Smart Data Center Insights*

值得注意的是，气流管理非常复杂，可以通过计算流体力学（CFD）——一种对速度、压力、黏度、密度、温度等物理量的分析——进行高度优化。像超大规模云厂商这样成熟的运营方大量依赖 CFD 来降低所需风量。这些优化的成效可能非常显著——回想风机定律物理：风量的下降会带来能耗的立方级下降。

## **室内冷却单元**

路线图的下一项是数据大厅内使用的冷却单元。最常见的选项是 CRAC（机房空调）、CRAH（机房空气处理机）和风机墙（Fan Wall）。直接膨胀（DX）机组也是一种选项，但使用远没有那么普遍。它们的关键区别如下：

- CRAC 是采用制冷剂循环的完整空调系统（很像家用空调）。它是简单的两件套系统：室内每台 CRAC 机组与数据大厅外的一台冷凝机组配对。制冷能力（最高 100kW）和能效都较低。常见于老旧或极小型数据中心。

![](https://substack-post-media.s3.amazonaws.com/public/images/94700fd7-2bde-4afd-a7aa-ec99ef5a7921_2166x706.png)
*来源：Schneider Electric*

- 主要的替代方案是「集中式」系统：多台 CRAH 机组连接到中央设施水系统。CRAC 机组用制冷剂把热量从机组交换到室外冷却装置，而 CRAH 用设施水把热量从机组带走，送至冷水机组或冷却塔。使用 CRAH 机组需要覆盖整个数据中心的更大管道与水泵系统，但总的运动部件更少，对大型数据中心而言经济性更好。

![](https://substack-post-media.s3.amazonaws.com/public/images/d5a84a77-8fb3-49bc-b9aa-327ba1c67850_1578x1050.png)
*来源：Schneider Electric*

- 现代数据中心用风机墙取代 CRAH，因为风机墙单机容量更高，通常为 500-600kW。风机墙的外形更契合数据大厅设计：机组可以上下堆叠，为整个 5-10MW 的数据大厅提供足够风量。风机墙还免除了通过架空地板和多孔地板砖向机柜送冷风的需要。CRAH 机组从顶部吸入热回风，而风机墙从机组背部——通常是设备（机械）走廊——吸入热风。数据大厅的热空气经吊顶进入该走廊。

![](https://substack-post-media.s3.amazonaws.com/public/images/4fc6be82-8f2f-4d3b-a12f-2a124fc8f7da_1200x668.jpeg)
*来源：Accuspeclnc*

在相当于 Tier 3 级别的数据中心中，CRAH/CRAC/风机墙通常按 [N+1 或 N+2 冗余配置](https://semianalysis.com/2024/10/14/datacenter-anatomy-part-1-electrical/#datacenter-basics)，但连接空气处理机组与设施水的管道通常采用 2N 配置，以便在故障或维护时隔离。

另一种日益流行的室内冷却单元是后门热交换器（RDHx）——概念上可以理解为「机柜内的 CRAH」，尽管很多营销宣传把它包装成「液冷」。RDHx 是安装在每个机柜背面、带散热器的一扇门，冷水在其中流动，吸收风冷服务器排出的热量。它部分或完全免除了房间级气流管理与冷却的需求。

使用 RDHx 的机柜冷却能力通常为 30-40kW——通过在后门加装风机（即所谓主动式 RDHx，Active RDHx）可提升至 >50kW。

![](https://substack-post-media.s3.amazonaws.com/public/images/28add5e1-32df-4647-ad2f-5caf77f3b281_1210x815.png)
*来源：nVent*

随着机柜功率密度提高，RDHx 日益流行。我们已知多个采用该系统的 Nvidia H100/H200 部署，例如 xAI 位于田纳西州孟菲斯的超大集群——RDHx 与 DLC 结合使用。

![](https://substack-post-media.s3.amazonaws.com/public/images/3b39c801-f3b4-4b4e-90f7-e7c53cd95838_2287x1323.png)
*来源：ServeTheHome*

RDHx 的优势之一是紧邻热源，提高了热交换器效能——即实际换热量与最大换热量之比。RDHx 的该比值可达 0.8 左右，而 CRAH、风机墙等房间级方案为 0.6-0.7。在其他条件相同时，这允许冷水机组进水温度略高一些，即冷水机组能耗更低。

两大主要缺点是成本和风机功耗。物理上，一台大风机比多台小风机更高效，因为风量与风机直径的三次方成正比。相比房间集中方案，运动部件数量增加，资本开支（capex）也更高。某些情况下——尤其是只有部分房间通过 RDHx 冷却时——会引入冷量分配单元（CDU）以更好地控制液体流量、温度、压降等。这会进一步拉大 capex 差距。

![](https://substack-post-media.s3.amazonaws.com/public/images/95a2adf9-9122-4c54-8d88-68773a362853_2416x1280.png)
*来源：Meta*

CDU 是一个简单系统，核心部件包括液-液热交换器、泵和控制电子。它在连接 IT 设备的内冷却回路与连接中央设施水系统的外冷却回路之间交换热量，并服务多个机柜。CDU 容量通常大于 1MW——但其变体众多，我们将在后文讨论 DLC 时展开。

![](https://substack-post-media.s3.amazonaws.com/public/images/ad0bd677-01f7-4e94-8056-b752a3e74a14_2297x1210.png)
*来源：Dafnia*

## **风冷与水冷冷水机组**

接下来讨论冷水机组（chiller），它通常是数据中心（不含 IT 设备）单一能耗最高的部件。冷水机组本质上是大型冷柜，执行完整的制冷循环。任何制冷循环的核心都是压缩机。这里涉及两个物理现象：

1. 蒸气比液体能吸收更多热量。
2. 在封闭系统中，温度与压力呈线性关系，即压力越高，温度越高。冷水机组的制冷循环工作原理如下：

   - 冷水机组内流动着「制冷剂」：一种特定流体（如 R134a 或 R123ze），其沸点远低于水，以利用第 1 条特性（蒸气比液体吸收更多热量）。
   - 冷水机组有两个热交换器：「蒸发器」和「冷凝器」。在蒸发器中，液态制冷剂吸收室内冷却机组的热量并蒸发，变成气体/蒸气。
   - 气态制冷剂随后经过压缩机，压力和温度显著升高。制冷剂温度越高，其传递热量的能力越强。
   - 在冷凝器中，高温高压的制冷剂把热量传给另一种介质——通常是空气（即风冷冷水机组）或水；后者需要一个连接冷却塔的独立冷却回路。
   - 膨胀阀降低压力从而降低温度——制冷剂在极低温度下回到液态。

![](https://substack-post-media.s3.amazonaws.com/public/images/72292567-8c3e-4ef5-a0dd-55e7ab0977ab_2110x1234.png)
*来源：District Heating and Cooling Systems*

压缩机是关键部件，其性能直接影响制冷能力——在制冷剂进入冷凝器前把它的温度升得越高，所需压缩机能量（更高压力）就越多。

现在来看数据中心使用的两种主要冷水机组类型：风冷式和水冷式，先讲后者。两者的根本区别在于冷凝器及热量从系统中排出的方式。

水冷冷水机组是大型机组，通常安装在建筑物内部的专用房间——机械室（Mechanical Room）内，与大型水泵为伴。其冷凝器是液-液管式热交换器，把制冷剂的热量转移到独立的冷却回路。后者连接位于建筑外的冷却塔——在屋顶上或紧邻建筑。

![](https://substack-post-media.s3.amazonaws.com/public/images/512c95c4-a86d-4354-9627-6f5f247f0027_1712x1140.png)
*来源：三菱重工业（Mitsubishi Heavy Industries）*

水冷冷水机组（尤其是离心式）的一大便利特性是制冷能力大：冷水机组容量通常以冷吨（RT，1 RT = 12,000 英热单位/小时，即 3.517 kW）计。在大型数据中心中，常见单机制冷能力 15MW（约 4250 RT），甚至高达 20MW！因此冷却一座大型设施只需少数几台冷水机组，它们一般布置在同一个机械室里。反过来，把冷却集中到少数几台大冷水机组，需要覆盖整个数据中心的更大管路。

这类机组通常能效相当高，性能系数（COP = 冷水机组能耗除以制冷能力）约 7x，具体取决于室外条件和 Delta T（波动可能很大）。

鉴于其体量，这类机组缺乏运行灵活性——频繁启停的效率极低，即便外部条件允许无机械制冷运行时也是如此。这正是变频驱动器（VFD）日益普及的原因。变频驱动器是一套电力电子系统，通过可编程逆变器实现交流到直流、再由直流回交流的变换，可精确控制供给冷水机组电机的电压，并能精确调节泵回数据大厅的水流量。

![](https://substack-post-media.s3.amazonaws.com/public/images/42f23dbf-1bf9-43a1-be6e-b228864af6af_1210x854.png)
*来源：YORK*

水冷冷水机组与冷却塔协同工作，冷却塔分两大类型：干式和湿式。后者又称蒸发塔（Evaporation Tower），是开式回路系统，把冷凝回路的水喷淋到特定材料（「填料」）上。蒸发可提高制冷能力，但水耗巨大，且通常需要专门的水处理设施。

![](https://substack-post-media.s3.amazonaws.com/public/images/c4fa1f99-9fd6-46b8-b4ca-89478c7c618d_2637x1403.png)
*来源：The Engineering Mindset*

水的蒸发使温度从干球降到湿球，因为热量被吸收用于实现水到蒸气的相变。这降低了冷水机组压缩机的负荷。如下表所示，温降幅度与湿度呈反比关系。冷却塔在亚利桑那等干旱地区表现最好，而新加坡这类湿热地区则更具挑战。

![](https://substack-post-media.s3.amazonaws.com/public/images/640a12c2-3de5-42a4-b858-f77d512a46b8_605x485.jpeg)
*来源：Ariel's Checklist*

单个数据中心的蒸发塔通常可冷却约 7-8MW（大型塔）——常见流量约 5,000 GPM（加仑/分钟）。

![](https://semianalysis.com/datacenter-industry-model/)
*来源：SemiAnalysis 数据中心模型*

Tesla 在其 [Giga Austin 数据中心](https://semianalysis.com/datacenter-industry-model/)建造了更大的冷却塔，每座塔与一台冷水机组一一对应，冷却能力超过 10MW！

![](https://substack-post-media.s3.amazonaws.com/public/images/7cbaa4a9-d1aa-438f-b6d5-ee08f264b518_2063x1270.png)
*来源：Brad Sloan*

蒸发塔的替代方案是干式冷却塔（或「干冷器」，dry cooler）。它是闭环系统（即无水耗），水流经盘管、由风机冷却。它无法利用更低的湿球温度，但不耗水——水虽便宜，却可能稀缺，还可能涉及许可证，并面临当地抗议和政治问题。最大机组冷却能力可达 2MW，但需要 20 台以上风机。

![](https://substack-post-media.s3.amazonaws.com/public/images/a8810d31-a56e-4d3a-89d9-4e2e2d22d8cd_2680x1403.png)
*来源：The Engineering Mindset*

## **用水量、风冷冷水机组与干冷器**

湿式冷却塔的主要问题是用水量大，这会拖累缺水地区或数据中心密集区（如弗吉尼亚州北部 Ashburn 的「数据中心走廊」）的项目进度。常用指标是 WUE 比率（Water Usage Effectiveness，用水效率），单位为每 kWh 升数——简单说，就是每 kWh 能耗需要多少升水。美国能源部的下述报告提供了不错的估算——采用水冷冷水机组系统的大型数据中心，WUE 可能超过 2L/kWh。

- 对一座 50MW、利用率 60%、PUE 1.25 的数据中心而言，WUE 为 2.0 意味着每年耗水 6.57 亿升（每年 1.74 亿加仑）。
- 注意：我们将在下文解释什么是风侧和水侧节能器（economizer）。

![](https://substack-post-media.s3.amazonaws.com/public/images/bab8d08a-b5e3-4f79-8eaa-5ed11c2284c5_1210x898.png)
*来源：美国能源部*

得益于更好的能效以及日益紧张的水资源约束，风冷冷水机组近几年大受欢迎。基于风冷冷水机组的系统比水冷方案更简单：冷水机组位于室外，同时充当冷水机组和冷却塔——风机向冷凝器吹风排出热量。现代系统集成了多种传感器与控制器以及 VFD，在室外空气足够冷时自动调低压缩机功率或直接关停。

这座 QTS 数据中心（IT 容量 48MW）的屋顶布置了多台风冷冷水机组——这是 NTT、Digital Realty 等大型第三方运营商的常见设计。

![](https://substack-post-media.s3.amazonaws.com/public/images/f81415c0-e306-411e-b326-726f6702138b_1210x428.png)
*来源：Google Earth*

风冷冷水机组也可以布置在地面、紧邻数据中心。在孟菲斯，xAI 实际上同时部署了开式回路冷却塔（室内很可能配有水冷冷水机组）和室外风冷冷水机组！

![](https://substack-post-media.s3.amazonaws.com/public/images/4e7e7e2e-43ec-4252-9012-0d490a649a8b_1024x502.png)
*来源：SemiAnalysis 数据中心模型*

这类机组容量更低、效率不如水冷冷水机组：下面施耐德产品目录中的例子展示了一款现代风冷冷水机组的规格。最大 SKU 有 18 台风机、冷却能力最高 2MW——在室外气温 35°C、进水 20°C、回水 30°C 条件下，该机组需要 500kW 功率，即 4x 的能效比。

![](https://substack-post-media.s3.amazonaws.com/public/images/8ee98986-7508-446f-89b0-f4195094bba1_1210x298.png)
*来源：Schneider*

为提升风冷冷水机组和干冷器的能效，绝热冷却（adiabatic cooling）这一选项迅速走红。其做法是增加一层「预冷垫」：水喷淋到冷却垫上随后蒸发，从周围空气吸热，从而降低环境温度（湿球与干球之差）并提升系统效率。这可以降低风冷冷水机组的压缩机功耗。若环境温度足够低，或湿度大到使其效率下降，绝热喷淋也可以关闭。

![](https://substack-post-media.s3.amazonaws.com/public/images/1acb39c2-bfed-406a-a647-61f05878c049_1210x598.png)
*来源：SPX Cooling*

最后简单讨论一下热量再利用（Heat Reuse）概念。纸面上该方案很有吸引力——把热量转移给第三方（比如附近的城市），从而大幅降低冷却需求，并可能将热量变现。超大规模数据中心理论上可以服务数万户家庭！按照 Microsoft 的说法，能源再利用因子（Energy Reuse Factor，再利用能源/数据中心电力消耗）在冬季最高可达 69%，夏季可达 86%。

![](https://substack-post-media.s3.amazonaws.com/public/images/5f7024d2-26b4-4c12-af09-f5fc7f334e7b_1210x611.png)
*来源：Microsoft*

这一概念在欧洲很流行，已有少数数据中心在运营此类系统——Equinix 曾用附近的数据中心为 2024 年巴黎奥运会游泳池供能，颇为出名。德国等一些国家正从监管层面推动此事，以实现其可持续发展目标。

下图展示了 Nebius 在芬兰 Manstala 附近的系统：

- 数据中心内服务器产生的热量经过热交换器进入集中供暖站——通常由市政方面运营。
- 如需更多热量，供暖站会启用自身的 HVAC 设备（如热泵）进一步提高温度。
- 随后热量被输送到各家各户。

![](https://substack-post-media.s3.amazonaws.com/public/images/4838d6fa-4ced-4893-9c8c-9d1e565efd3b_1280x540.jpeg)
*来源：Nebius*

虽然纸面上很吸引人，但实际存在诸多限制，比如与居民区的距离以及所需基础设施是否具备。

## **超大规模云厂商设计与其超低 PUE 系统一览**

超大规模云厂商普遍采用标准化数据中心设计，以缩短上市时间、便利物流并降低成本。与必须满足多样化客户当下及未来广泛需求的托管服务商不同，超大规模云厂商作为唯一租户，可以打造贴合自身特定工作负载的高效设计。这类数据中心的 PUE 一般可做到 1.1 至 1.2 之间——主要依靠「自然冷却」（Free Cooling）技术、更高的 IT 设备运行温度以及深度 CFD 分析的组合。

在展示实际部署之前，先厘清一些基本概念。「自然冷却」或「节能器」（Economizer）是利用外部环境为数据中心降温的技术。主要有两大类，每类又有多种变体：

- 风侧节能器（Airside economizer）：用室外空气冷却数据中心——特别适合寒冷气候地区——无需冷水机组。该技术可通过在冷却塔喷水进一步增强。
- 水侧节能器（Waterside Economizer）：面向使用冷水机组的数据中心，增设一条绕过冷水机组制冷回路的次级液体回路，水直接送往冷却塔或干冷器——但这要求水温高于室外湿球温度。

![](https://substack-post-media.s3.amazonaws.com/public/images/3d6dc5a1-a91f-49e6-887b-6d53002f38fc_1210x898.png)
*来源：美国能源部*

这两种技术只有在数据中心所在地外部环境相对进风温度足够冷时才有效。环境越冷、进风温度越高，效果越好。超大规模云厂商在等式两端同时做文章：为最大化利用自然冷却，它们通常让服务器在 30°C 以上的进风温度运行，有时甚至超过 40°C。其定制服务器设计能在如此高温下不损害性能和寿命。

地理区位当然也是关键变量。下面展示了 Microsoft 按数据中心地理区位划分的 PUE 与 WUE 分解。使用自然冷却的最差情景是新加坡或印度这类湿热气候。

![](https://substack-post-media.s3.amazonaws.com/public/images/fe68dea0-a18f-43da-81f3-bba36a115889_1210x823.png)
*来源：Microsoft*

## **Microsoft 数据中心与冷却系统**

现在来看各家的实际设计，先从 Microsoft 开始——下图是其参考设计的演进，其中 [48MW 的「Ballard」仍在全球各地部署](https://semianalysis.com/datacenter-industry-model/)。

![](https://substack-post-media.s3.amazonaws.com/public/images/8c41ef5c-75c1-40be-b38e-dad56edc182a_1210x913.png)
*来源：Microsoft*

Ballard 为风冷设计，绕开了冷水机组。Microsoft 使用一套其称之为「直接蒸发冷却」（Direct Evaporative Cooling）的系统，如下图所示。它对应风侧节能器系统：

- 室外空气经过滤后由风机抽入设施。
- 如有需要，对空气加湿以降温。
- 空气进入服务器房间，升温后被导入热通道，再由排风机排出设施。

![](https://substack-post-media.s3.amazonaws.com/public/images/85a5f4ea-a0c3-4f10-8325-2665761abe9c_1210x1167.png)
*来源：Microsoft*

当不需要水蒸发时，Microsoft 把这套系统称作「自由空气冷却」（Free Air Cooling）。

![](https://substack-post-media.s3.amazonaws.com/public/images/e657b518-cc9c-4438-be03-8ec8fafd83c8_1210x1154.png)
*来源：Microsoft*

下面是热空气排风系统以及让外部空气进入的过滤装置的航拍视图。

![](https://substack-post-media.s3.amazonaws.com/public/images/cb4e3e23-3148-418e-a0da-1f01f324109e_2246x1514.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/e800325e-e569-41bb-aadb-2d63828c49e0_2050x804.png)
*来源：Google Earth、SemiAnalysis*

该系统设计避免了使用冷水机组和 CRAH 等空气-水热交换器。结果就是：无需设计风冷冷水机组/干冷器或冷却塔，数据中心的单位 MW 资本开支可以显著更低。该系统完全无水耗——而这座数据中心位于亚利桑那州凤凰城附近。当地气温超过 30°C 是常态，但凤凰城气候非常干燥——湿球温度可以显著低于干球温度。缺点是一年中大部分时间需要水蒸发，导致 Microsoft 在凤凰城的 WUE 超过 2，尽管其公司平均 WUE 为 0.3。

![](https://substack-post-media.s3.amazonaws.com/public/images/9e4199ab-a5cc-404c-8ba0-51d38523291d_1210x637.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/b882e49c-504b-4ef0-8d0a-d88591225dcd_1210x679.png)
*来源：Bing Maps 与 Google Earth*

注意上图中的设施内完全没有任何冷却塔，因为这座数据中心采用的是自然冷却。

![](https://substack-post-media.s3.amazonaws.com/public/images/6fbaf7e2-a488-4a9a-9e7e-6cf5667fa453_1210x880.png)

在某些地区，气候条件不适合这类冷却，Microsoft 会使用另一套称为「间接蒸发冷却」（Indirect Evaporative Cooling）的系统——仍然无需任何机械制冷，但会在室外放置一台干冷器。

![](https://substack-post-media.s3.amazonaws.com/public/images/2a0a6882-c72c-4232-9f4c-042a3b608eb6_929x858.png)
*来源：Microsoft*

下图为该系统在一座爱荷华州数据中心的卫星视图。注意紧邻设施布置的流体冷却器（fluid cooler）和 AHU。

![](https://substack-post-media.s3.amazonaws.com/public/images/a56c854c-18fd-43bb-8733-e188fd8470a8_1210x856.png)
*来源：Google Earth*

## **Meta 的「H」：效率优先于上市时间**

Meta 著名的「H」设计是另一个有趣案例。凭借自然冷却与高服务器进风温度的组合，加上相对较低的功率密度，Meta 十多年来一直以业内最佳的能效水平运营数据中心。下图描绘了其冷却系统：与 Microsoft 的「直接蒸发冷却」和「直接自然冷却」非常相似。

![](https://substack-post-media.s3.amazonaws.com/public/images/1c6171d3-d600-4752-8feb-305b64a06841_2548x1152.png)
*来源：Electronics Cooling*

在某些气候下，Meta 会在最热的夏季启用 CRAC 为室外空气降温——此时 PUE 很可能显著高于其 1.08 的公司平均值。

![](https://substack-post-media.s3.amazonaws.com/public/images/90d749f0-96c1-4021-b3d1-cc12ea8866bb_2162x958.png)
*来源：Google Earth*

2018 年，Meta 推出一个变体，使自然冷却也能适用于新加坡这类湿度较高的气候。它依托空气-水热交换器，由室外空气冷却设施水系统，并可通过绝热选项进一步降温。

![](https://substack-post-media.s3.amazonaws.com/public/images/6f21ff8d-365d-41e8-abe9-85442be08ac5_2564x1048.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/7bd750c3-8382-4f36-af76-2fb34338a013_2310x1468.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/24ccc387-757e-42ac-8158-a8149fc53a31_2232x1002.png)
*来源：Meta*

Meta 的能效水平令人印象深刻（PUE 1.08、WUE 0.20），但这是靠复杂的三层结构实现的。Meta 的「H」在相同或更低电力容量下比竞争对手的设计大得多——使风机可以更低转速运行。[我们的实时与历史卫星影像显示，其完成建筑外壳的时间通常约 2 年，是其他超大规模云厂商的 2-3 倍](https://semianalysis.com/datacenter-industry-model/)。低密度与长建设周期在 AI 时代并不理想，这促使 [Meta 采取激烈手段，拆除多座在建的「H」，换成其新的 AI-ready 设计](https://semianalysis.com/2024/10/14/datacenter-anatomy-part-1-electrical/#meta-datacenter-scrapped-vertiv-schneider-electric-eaton-legrand-delta-datacenter-bill-of-materials-by-component-transformers-switchgear-redundancy-ups-ocp-busbar-generators-substation)（付费墙后详述）。

![](https://substack-post-media.s3.amazonaws.com/public/images/bed9b66f-c9a6-46a5-9141-fbe7886744a2_1122x1286.png)
*来源：Google Earth*

## **Google 数据中心——用电换水的取舍**

Google 的参考设计截然不同——其 PUE 以 1.10 领先业界，但用水量大得多，WUE 超过 1.0。Google 采用水侧节能器，通常意味着两条相互独立的设施冷却回路——执行制冷循环的「冷水机组」回路，以及无机械制冷的「热交换器」回路。当室外条件允许时，数据中心只使用次级回路，水直接送往冷却塔或干冷器，绕过冷水机组。

![](https://substack-post-media.s3.amazonaws.com/public/images/78c87d09-fbba-4e3a-bd15-f1ab4ddc36eb_2550x796.png)
*来源：Schneider Electric*

板式热交换器是两条流体回路循环并交换热量的系统。这类机组换热效率通常相当高——经验法则，2-3°C 的损失是常态，即从冷却塔回来的 30°C 水会损失 2°C，以 28°C 进入室内冷却机组。

![](https://substack-post-media.s3.amazonaws.com/public/images/2a8167b4-c6be-4acf-b42f-991e374cc726_1210x880.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/34cd3cb4-152e-49e7-9fed-c6cf2f434bd2_605x341.jpeg)
*来源：Alfa Laval*

Google 部署过多种类型的冷却系统——其中最令人印象深刻的是[利用海水自由冷却的芬兰数据中心](https://www.youtube.com/watch?v=3f0V6_ZFHMk)——但其最常见的设计大量依赖蒸发冷却塔。在下面这个例子中，三座 IT 负载合计约 200MW 的大型数据中心共享同一套集中式冷却基础设施（可以看到管路），冷却塔顶部装有巨型风机。这些塔规模很大，每台水冷冷水机组配两个冷却单元（cell），也就是说 28 个 cell 冷却 200MW，平均每个 cell 约 7MW。有些设计包含水冷冷水机组，但另一些数据中心完全「无冷水机组」（chillerless）——Google 已公开表示其大型比利时园区为 chillerless。

![](https://substack-post-media.s3.amazonaws.com/public/images/921f26c3-9884-4a8d-adf2-cee4d1d726fd_964x1127.png)
*来源：SemiAnalysis 数据中心模型*

最后简单看一下 AWS 的数据中心。该公司透明度较低，我们掌握的信息也较少。下图展示了 Manassas 的一处园区，其中最大单体建筑的关键 IT 电力为 50MW。

![](https://substack-post-media.s3.amazonaws.com/public/images/3ad980bd-b6fc-4585-92e2-12435ecb1bbf_1210x668.png)
*来源：SemiAnalysis 数据中心模型*

我们注意到图中没有明显的室外冷却设备（风冷冷水机组、干冷器或冷却塔）。我们认为 AWS 采用的系统与 Microsoft 和 Meta 非常相似——屋顶的排风机加上让室外空气进入的百叶窗。

![](https://substack-post-media.s3.amazonaws.com/public/images/fae40254-b70e-47e7-8caa-1fbf7cd2fe75_1386x779.jpeg)
![](https://substack-post-media.s3.amazonaws.com/public/images/8a7020d9-8415-477e-914b-35df5d5cb970_2577x1326.png)
*来源：Amazon*

至此我们讲完了数据中心冷却系统的基础。超大规模云厂商已在很大程度上证明了「风冷不是节能技术」这一流行论调的错误。生成式 AI 的崛起颠覆了这一框架的一切，并对现有设计提出挑战。

接下来讨论 Nvidia 的路线图、数据中心设计近期与长期的未来，以及对设备供应商的影响。我们认为液冷普及背后的真正驱动因素仍被误解，推理与训练数据中心的冷却系统未来同样如此。我们常听到液冷的普及源于其卓越能效，或是因为 >1000W 的芯片无法用空气冷却。我们也常听到推理将需要低功耗服务器和风冷。
