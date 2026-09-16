---
title: "混合键合工艺流程——先进封装第 5 部分"
title_en: "Hybrid Bonding Process Flow - Advanced Packaging Part 5"
subtitle: "BESI、EV Group、AMAT、TEL、ASMPT、SET、Shibaura、SUSS Microtec"
date: 2024-02-09
source: https://newsletter.semianalysis.com/p/hybrid-bonding-process-flow-advanced
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie", "Jeff Koch"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 混合键合工艺流程——先进封装第 5 部分

> 原文：[Hybrid Bonding Process Flow - Advanced Packaging Part 5](https://newsletter.semianalysis.com/p/hybrid-bonding-process-flow-advanced) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**BESI、EV Group、AMAT、TEL、ASMPT、SET、Shibaura、SUSS Microtec**

混合键合（hybrid bonding）将成为自 EUV 以来对半导体制造最具变革性的创新。事实上，它对设计流程的影响甚至会比 EUV 本身更大——从封装架构一路延伸到单元（cell）设计与版图。IP 生态将被大幅重塑，制造流程同样如此。晶体管在 2D 平面上继续微缩的时代还会延续，但步伐将放缓；而混合键合将开启一个新时代——芯片设计师开始以 3D 方式思考。

唱完这段激情澎湃的颂歌之后需要指出，要让混合键合大规模走向市场，还面临许多重大的工程与技术挑战——如今它仅用于少数 AMD 芯片、CMOS 图像传感器以及部分厂商的 3D NAND。这一转型将重塑供应链与设计流程。

我们将从**基础**一路讲到混合键合的进阶内容：工艺流程、设备、设计用例、挑战、chip-on-wafer 与 wafer-on-wafer 的成本对比。我们还将呈现自有的采用率建模——按市场（手机、客户端 PC、数据中心 CPU、AI 加速器、HBM 等）刻画用途、设备需求与用量，并覆盖到本十年末的公司层面采用情况。

混合键合是我们先进封装系列的延续。在本系列[第 1 部分](https://semianalysis.substack.com/p/advanced-packaging-part-1-pad-limited)，我们讨论了先进封装的必要性，概述了制程节点微缩的经济学，以及为什么先进封装如此不可或缺。

在[第 2 部分](https://semianalysis.substack.com/p/advanced-packaging-part-2-review)，我们梳理了各类封装技术及其用例。在[第 3 部分](https://semianalysis.substack.com/p/advanced-packaging-part-3-intels)，我们讨论了英特尔（Intel）对热压键合（TCB）的押注及设备格局。在[第 4 部分](https://www.semianalysis.com/p/the-future-of-packaging-gets-blurry)，我们探讨了扇出封装、有机中介层和硅桥，作为绕开昂贵无源中介层的路径。随着 AI 供应链升温，我们还覆盖了[CoWoS 供应链、产能配给与 HBM](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and)，以及[上游设备供应链与产能扩张](https://www.semianalysis.com/p/ai-expansion-supply-chain-analysis)。SemiAnalysis 提供[一个从产能到芯片 SKU、再到出货量、ASP 与营收的详细模型，按无厂设计公司、半定制伙伴和超大规模厂商划分，同时跟踪 30 多家公司的加速器装机量](https://www.semianalysis.com/p/accelerator-model)。我们的模型领先于 Nvidia、Broadcom、AMD 和 Marvell 的业绩超预期和/或指引上调，而市场仍在误读这轮资本开支（capex）爬坡。

在先进封装系列的第 5 和第 6 部分，我们将首先讨论混合键合的工艺流程、制造相关的难点、设备工具链中的主要玩家，以及使用和参与混合键合的主要厂商与设计，例如台积电（TSMC）、Intel、三星（Samsung）、SK hynix、美光（Micron）、CXMT、Sony、OmniVision、YMTC、Kioxia、西部数据（Western Digital）、Besi、Shibaura、东京电子（Tokyo Electron）、Applied Materials、ASM Pacific、EV Group、SUSS Microtec、SET、Bosch、Adeia（前身 Xperi）等。我们对 BESI 持有非常不同于市场共识的观点。

随后我们将讨论 chip-on-wafer（D2W，裸片对晶圆）与 wafer-on-wafer（W2W，晶圆对晶圆）混合键合之间正在进行的攻防战。在本系列中，我们将直接拆解 AMD、Apple、Nvidia、Marvell、Broadcom 等公司各产品线和终端市场的采用率，并结合设备吞吐量、稼动率、键合步骤数量、不断演进的用例等数据加以整合。我们还将深入设计流程、台积电 N2 制程的定制化客户专属修改、混合键合间距持续微缩下的未来用例，以及当前的成本壁垒将如何被攻克。

本文是第 5 部分，主要聚焦工艺流程，让我们开始吧。

![](https://substack-post-media.s3.amazonaws.com/public/images/b1adb147-cacc-48f2-87c1-ccb0571bcea8_1632x881.png)

在封装历史上，上一次重大范式转移是从引线键合（wire bonding）到倒装芯片（flip chip）。此后，晶圆级扇出、TCB 等更先进的封装形式都只是同一核心原理上的渐进改良。这些封装方法都以某种带焊料的凸点（bump）作为硅片与封装基板或电路板之间的互连。这些技术可以一直微缩到约 20 微米间距。

到目前为止，我们在多篇构成的先进封装系列中讨论过的主要封装类型和工艺流程都处于 220 微米到 100 微米量级，且大多以焊料作为各小芯片（chiplet）铜互连之间的介质。要继续微缩，就需要又一次范式转移：无凸点互连的混合键合。混合键合可将互连间距缩至 10 微米以下，路线图直指百纳米量级，而且不使用任何电阻更高的焊料之类的中间介质。

![](https://substack-post-media.s3.amazonaws.com/public/images/b68e3e41-68f5-4172-8f95-4e8facf1a8bb_3376x2038.png)
*Nvidia A100 截面图；C4 凸点（约 130 微米间距）和铜柱（约 50 微米间距）上的银色团块即为焊料。*

取而代之的是，不同芯片或晶圆之间的互连由铜过孔直接相连。直接铜连接意味着低得多的电阻，从而在向各芯片传输数据时功耗更低。再加上连接数量提升多个数量级，设计思路需要彻底重构。

[回顾第 1 部分](https://www.semianalysis.com/p/advanced-packaging-part-1-pad-limited)：先进封装的意义究竟何在？可以看到，封装技术的演进旨在实现更高的互连密度（单位面积内更多互连）、缩短走线长度以降低时延和每比特传输能耗。混合键合同时满足了这两点：走线长度大幅缩短，时延低到仅次于片上互连的极限，某些情况下甚至比片内全局布线更短；互连间距则可以缩至远低于 10 微米来提升密度。

## **混合键合究竟是什么？**

混合键合用于芯片的垂直（3D）堆叠。其标志性特征是无凸点（bumpless）。它摆脱了基于焊料的凸点技术，转向铜与铜的直接连接。这意味着上层裸片（die）与下层裸片紧贴在一起。两颗裸片上没有凸点，只有可以微缩到超精细间距的铜焊盘。没有焊料，与焊料相关的一系列问题也就无从谈起。

![](https://substack-post-media.s3.amazonaws.com/public/images/dde8c3bf-3b20-4bd5-b1a6-07981b3baeca_1920x1080.jpeg)

从上图可以看到 AMD 3D V-Cache 的截面，它采用台积电 SoIC-X 裸片对晶圆（die-to-wafer）混合键合。上下两层硅之间的键合界面是混合键合层，位于硅裸片金属层之上。混合键合层是一种介质材料（如今最常见的是 SiO 或 SiCN），其中通过图形化形成了铜焊盘和过孔，间距通常在 10 微米以下。

介质层的作用是隔离每个焊盘，避免焊盘之间的信号干扰。铜焊盘通过硅通孔（TSV）连接到芯片金属层。TSV 负责向堆叠中的另一颗裸片输送电力和信号。由于下层裸片是「正面朝下」放置的，需要这些过孔把上层裸片的金属层穿过晶体管层连接到下层裸片的金属层。

![](https://substack-post-media.s3.amazonaws.com/public/images/118962cf-0c57-4665-b02b-9ca0f360f9b9_552x525.png)

芯片间通信的信号正是经由这些铜焊盘通过的。之所以称为「混合」键合，是因为它是介质-介质键合与铜-铜直接键合的结合，键合界面之间不使用任何额外的粘合剂或材料。

## **关键工艺条件**

与以往的凸点式互连相比，混合键合带来了一整套全新的技术与工艺挑战。要获得高质量的键合，对表面平整度、洁净度和键合对准精度都有极为严苛的要求。我们先讲述其中一些挑战，因为工艺流程正是围绕缓解这些挑战而设计的。心中带着这些挑战，有助于你更好地理解流程为何如此设计，以及不同方法的优劣。

## **颗粒与洁净度**

任何关于混合键合的讨论都绕不开颗粒（particle）问题，因为颗粒是混合键合良率的天敌。混合键合要求两个极其光滑平整的表面紧贴键合，因此键合界面**极其**敏感于任何颗粒的存在。

一颗仅 [1 微米高的颗粒就会造成直径 10 毫米的键合空洞](https://ieeexplore.ieee.org/document/9058783)，导致键合缺陷。而凸点式互连中，器件与基板之间始终存在间隙，且使用了底部填充（underfill）或非导电膜，可以容忍一定颗粒。

![](https://substack-post-media.s3.amazonaws.com/public/images/23434868-490e-4f9d-b812-44ab51c29b4f_828x219.png)

保持洁净至关重要，而这极具挑战。颗粒来源于晶圆切割、研磨、抛光等众多步骤。任何摩擦都会产生颗粒，这是个问题——尤其混合键合涉及机械拾取裸片并放置到其他芯片之上。设备中裸片键合头（bond-head）和翻片器（flipper）带来大量机械运动。颗粒不可避免，但有多种技术可以缓解其对良率的影响。

![](https://substack-post-media.s3.amazonaws.com/public/images/9c8b2260-6fbb-4cb9-90a2-8e04002e89a9_1384x650.png)

当然，晶圆清洗会定期进行以去除污染物。但清洗并不完美，单次无法去除 100% 的污染物，因此最好从一开始就避免污染。混合键合所需洁净室的先进程度远超其他先进封装形式的要求。

![](https://substack-post-media.s3.amazonaws.com/public/images/a75c9d2e-61fd-494f-bf1b-b3288118cfbb_2340x753.png)

因此，混合键合通常要求 Class 1 / ISO 3 级或更好的洁净室与设备。例如台积电和 Intel 一路做到 ISO 2 甚至 ISO 1 级。这是混合键合被视为「前道」（front-end）工艺的一大原因——即它在与晶圆厂类似的环境中进行，而非传统封测厂（OSAT）的环境。鉴于洁净度要求的跃升，OSAT 要进军混合键合非常困难。大多数 OSAT 若想参与混合键合，都需要新建更先进的洁净室；而台积电、Intel 这样的公司则可以直接利用老晶圆厂，或按既有晶圆厂的同等标准新建。

混合键合的工艺流程还涉及许多历来为晶圆厂所专用的设备。日月光（ASE）、安靠（Amkor）等封测代工厂（OSAT）在化学气相沉积（CVD）、刻蚀、物理气相沉积（PVD）、电化学沉积（ECD）、化学机械抛光（CMP）以及表面制备/活化方面的经验相对薄弱。

洁净度要求与设备数量增加相叠加，带来了巨大的成本上升。相对其他封装形式，混合键合的工艺并不便宜。下面我们将走完整个工艺流程。

## **平整度**

混合键合层的表面平整度也极其关键。键合界面同样对任何形貌起伏敏感，起伏会造成空洞和失效键合。一般认为表面粗糙度阈值是介质 0.5nm、铜焊盘 1nm。要达到这种平整度，需要进行化学机械抛光（CMP），这是混合键合的一项关键工艺。

![](https://substack-post-media.s3.amazonaws.com/public/images/3eb0ed23-fe74-4401-ad37-27b062f7788a_1200x676.jpeg)

抛光之后，这种平整度必须在整个流程中得到保持。任何可能损伤表面的步骤（例如剧烈清洗）都要避免。甚至连晶圆测试（wafer sort）的探针作业都需要调整，以免破坏表面。

## **晶圆对晶圆（W2W）还是裸片对晶圆（D2W）？**

先讨论 W2W 与 D2W。混合键合可以通过晶圆对晶圆（W2W）或裸片对晶圆（D2W）工艺完成。W2W 是指两片已完成制造的晶圆直接键合在一起。W2W 具有更高的对准精度、吞吐量和键合良率。鉴于其相对容易，目前绝大多数混合键合都通过 W2W 完成。

![](https://substack-post-media.s3.amazonaws.com/public/images/895717e5-2251-4e19-9835-a219eb56f74a_1024x706.png)

W2W 键合良率更高的原因在于对准与键合是分开的两步。W2W 设备中有一个专门的对准腔室。上下晶圆对准后，被移入键合腔室（处于真空中），施加一定压力压合，约 20 分钟后形成初始预键合。

W2W 的关键在于步骤更少、工艺更洁净。在对准和键合之前，可以先对晶圆进行清洗以去除大部分颗粒。裸片切单（singulation）这一颗粒污染源只发生在键合之后。而且由于是晶圆级工艺，对准步骤可以分配更多时间——对准时间长对吞吐的影响远小于芯片级工艺。

腔室内也没有太多机械运动，因此腔室自身产生的污染物更少。目前 W2W 键合机可实现 50nm 以下的对准精度。W2W 键合已是成熟工艺，并不特别昂贵。证据就是它已广泛应用于三层堆叠图像传感器和 NAND 等大众市场产品。

W2W 键合固然好，但一大局限是无法通过晶圆测试挑选已知合格裸片（KGD）。这会带来不想要的后果：坏芯片与好芯片键合到一起，白白浪费好硅片。

鉴于此，W2W 用于良率较高的晶圆，通常意味着较小的芯片设计。下图展示了裸片面积与 W2W 和 D2W 成本的关系。裸片面积小时 W2W 更便宜，因为晶圆良率更高。但随着裸片面积增大，W2W 的成本曲线陡峭得多，主要驱动因素正是好裸片的损失成本。芯片尺寸越大，每片晶圆上合格裸片的占比越低，导致更多坏裸片与好裸片键合的情况。

![](https://substack-post-media.s3.amazonaws.com/public/images/ec88cc70-a729-49ee-bc51-7501d0fe91a2_902x623.png)

可以看到 W2W 用于良率较高的小芯片：CMOS 图像传感器、[3D NAND](https://www.semianalysis.com/p/the-impending-chinese-nand-apocalypse-e01)，以及在逻辑芯片领域迄今仅有的 [Graphcore Bow IPU](https://www.semianalysis.com/p/graphcore-announces-worlds-first)。

虽然 Graphcore Bow IPU 是一颗较大的 HPC 芯片，但其上层裸片并非先进制程逻辑，而是用于供电的无源电容裸片，因此良率应当相当高，硅成本也便宜得多。W2W 的另一个缺点是上下裸片尺寸必须一致，这限制了异构集成方案的灵活性。

成本有多个可调杠杆，主要是晶圆成本、D0（缺陷密度）和键合良率。每个杠杆都会带来成本的升降。注意，这些只是为了强调观点的示例数字。请勿直接引用下图，它显示的并非真实键合成本。如需当今产品的实际成本，请联系我们获取 AMD MI300X 成本报告，或 Zen 3、Zen 4、Zen 5 混合键合成本报告。

![](https://substack-post-media.s3.amazonaws.com/public/images/b1b4f1a9-4075-4e2d-aa82-e01cba8eaef0_2146x931.png)

如图所示，小裸片时 D2W 更贵，但裸片变大后形势逆转，W2W 反而更贵。关键在于能够只测试和键合已知合格裸片（KGD），而不是冒着缺陷堆叠、浪费好硅的风险——这也是裸片对晶圆（D2W）率先实现产品化的原因。它能在更差的良率下仍做出商业上可行的产品。

![](https://substack-post-media.s3.amazonaws.com/public/images/58fd782b-c172-4da5-b2cf-0e09657e693e_2818x737.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/b8fd9222-5ff7-453d-8a5b-58e935db45bc_2336x631.png)

要绕开这些限制，就得转向 D2W。D2W 键合的挑战大得多。在完成晶圆测试后，KGD 从上层晶圆切单，再通过拾放（pick-and-place）设备逐颗贴装到基础晶圆上。就键合而言这更困难，因为每片晶圆多出数次键合步骤。这些额外步骤引入更多颗粒污染，尤其是切单以及拾放过程中键合头的运动。

D2W 可以做成「集合式」（collective）工艺：先把 KGD 对准并临时键合到一片重构载片（carrier wafer）上，再把重构载片与基础晶圆键合完成真正的预键合。这样做是为了像 W2W 那样把对准与键合分离，并允许在最终预键合前插入一步清洗，清除累积的污染物。缺点是步骤更多，而且额外的 W2W 键合步骤也带来更多对准误差的机会。

![](https://substack-post-media.s3.amazonaws.com/public/images/90ec8164-ed4a-461b-8437-f525054822d8_2202x978.png)

这其实还是简化版流程，因为下层裸片同样可以重构到载片上。也就是说，上下两种芯片都从原始硅晶圆切下并挑选出 KGD，两组芯片分别键合到各自载片的精确位置上，然后两片载片再用 W2W 工艺键合。台积电 SOIC 就是这么做的。因此，每颗 AMD 3D V-Cache 芯片要用到 5 次键合（下层 CPU 裸片到载片、3D V-Cache 小芯片到载片、2 颗虚设硅片到载片、以及晶圆对晶圆键合）。

![](https://substack-post-media.s3.amazonaws.com/public/images/feabbdd0-b5ab-4c56-aacb-b9dbb3c1606e_1794x1821.png)

重构工艺还可用于更极端的异构集成方案。[Intel 在 IEDM 2022 上演示了「准单片芯片」（quasi-monolithic chips，QMC）](https://www.semianalysis.com/i/100427011/foveros-direct-reconstituted-wafer-on-wafer-bonded-paper)。他们展示的一个 QMC 应用示例是上下各 2 颗裸片异构集成的封装。上下两侧的每颗裸片都先贴装到载片上，然后用 SiO2 等厚无机氧化物对晶圆进行塑封，随后进行 W2W 键合，最后将塑封后的芯片切单并贴装到封装基板上完成流程。

![](https://substack-post-media.s3.amazonaws.com/public/images/e3d1916b-0924-43e5-bb98-6147f5334b2c_1212x291.png)

注意，重构区域内也可以有 TSV。

直接式 D2W 键合则是把单颗裸片直接放到目标晶圆上进行预键合。直接式 D2W 成熟度较低，但展望未来，出于工艺简化的考虑，直接式 D2W 的应用会更多。集合式 D2W 的一个好处是清洗后可以直接送入对准腔室以减少污染。如今新近推出的 D2W 集群设备（下文将讨论）已经能够复刻这一流程，削弱了集合式工艺的这一优势。此外，D2W 更适合更精细的焊盘间距——间距越细对准越难，省去会带来额外失准风险的 W2W 步骤就有了意义。

鉴于 D2W 混合键合的工艺挑战和相应成本，目前应用有限。AMD 是 2022 年的首个采用者，也是迄今唯一的采用者。未来应用、各家公司的采用速度、工艺步骤数量等内容，我们将在后文讨论。

需要注意的一点是，W2W 在对准上远领先于 D2W，所以如果你的设计并非异构集成、晶圆良率又足够高，W2W 实际上是精度更高、良率更高的工艺。这种更细的间距还将解锁许多 D2W 尚无法进入的新用例。

## **混合键合工艺流程**

接下来更详细地过一遍 D2W 与 W2W 的工艺流程。

![](https://substack-post-media.s3.amazonaws.com/public/images/26731116-cc24-493e-b86e-74c1e9577dcd_1966x292.jpeg)
![](https://substack-post-media.s3.amazonaws.com/public/images/a5cd76cf-c350-4e61-a8c0-db642ac47d8e_1718x229.jpeg)

## **TSV 形成**

如前所述，封装内的所有芯片都需要 TSV 来获得电力和信号。想象一个传统的倒装芯片封装：芯片只需在一面有互连，从封装基板接收电力、与之通信数据。这一互连层的凸点连接到无源布线层（也称「金属层」或「后道工序」BEOL），由它向负责开关和处理数据的晶体管层提供电力和信号。

对 3DIC 而言，下层裸片既要与其下方的封装基板通信，又要与其上方的裸片通信，因此裸片两面都需要互连。这正是 TSV 登场的地方。按在流程中制造时机的不同，TSV 有多种变体：「via-first」——在晶体管层之前先在硅中制造；「via-middle」——在晶体管层完成之后、金属层之前制造；或「via-last」——在 BEOL 之后制造。

3DIC 最常见的是「via-middle」方案：TSV 从金属层之间穿过晶体管层，在芯片背面露出，使芯片两面都有互连层，下文将详述。

![](https://substack-post-media.s3.amazonaws.com/public/images/17da1d7d-7381-4a0a-8939-71c837520584_2389x1216.png)

我们在[此处](https://www.semianalysis.com/i/135455698/silicon-interposer-key-process-steps)详细讲过 TSV 流程，本报告再作概述。

晶圆先涂覆光刻胶，再用光刻完成图形化。然后用深反应离子刻蚀（DRIE）在硅中刻出高深宽比的深沟槽，深入晶圆但不穿透整片。接着用化学气相沉积（CVD）沉积绝缘层（SiOx、SiNx）和阻挡层（Ti 或 Ta），防止铜扩散进硅中。然后用物理气相沉积（PVD）沉积铜种子层，种子层沉积于沟槽内，再用电化学沉积（ECD）填充，TSV 就此成形。但工艺尚未完成，因为过孔还没有在背面露出。为了露出 TSV，需对 TSV 的背面进行抛光，某些情况下还需刻蚀减薄背面，使 TSV 显露出来。完成后，晶圆即可进入 BEOL 的形成。

TSV 形成绝非小事，而且可能相当耗时，尤其是因为所需的深刻蚀。我们了解到，TSV 形成正是制约 HBM 与 CoWoS 产量的工序之一。部分客户从硅中介层[改用 CoWoS-R](https://www.semianalysis.com/i/133273576/cowos-variants) 的原因之一，就是避开硅中介层中昂贵的 TSV 工艺。

## **混合键合层形成**

在晶圆的键合界面处，混合键合层制作在晶圆 BEOL 之上。无论 W2W 还是 D2W，这一步都相同。这是一层以精细间距铜过孔图形化的介质薄膜。介质（通常为氮碳化硅 SiCN）通过 PECVD 沉积。然后制作焊盘：用光刻对铜焊盘的孔进行图形化并刻蚀，沉积阻挡层和种子层，再用标准的铜大马士革工艺电镀铜。

![](https://substack-post-media.s3.amazonaws.com/public/images/1ffa5c75-8128-479c-8c3f-e6322f0ef8af_1268x689.png)

接着是 CMP 步骤，研磨平滑介质表面并使铜获得正确的轮廓。[铜焊盘的一个显著特点是：直到约 1 微米间距，它们都是凹陷（recessed）的](https://www.semianalysis.com/i/58498676/sonys-leading-micron-pitch-hybrid-bonding)。如前所述，光滑的表面对形成良好键合至关重要。[介质粗糙度必须控制在 0.5nm 以内，铜焊盘在 1nm 以内](https://ieeexplore.ieee.org/document/9026700)。

混合键合界面的一个特征是：铜焊盘最初凹陷至低于介质层约 5 纳米。这是为了确保退火时铜不会妨碍初始的介质-介质键合。[如果铜凹陷过深，Cu-Cu 键可能无法正常形成](https://iopscience.iop.org/article/10.7567/1347-4065/ab17c4)。

在对铜及其他金属做 CMP 时，由于过度抛光以及金属与介质软硬程度不同，常会出现碟陷（dishing）。这虽不理想，但并非致命，可以设法处理。需要精确控制碟陷的轮廓，以防止键合时铜的过度生长/生长不足。

为获得正确的碟陷轮廓，需要组合使用低铜去除率与高铜去除率抛光液的多个 CMP 步骤。CMP 是混合键合实现超光滑表面和最优轮廓的关键工艺。

[在 ECTC 会议上，Sony 展示了当间距缩小到 1 微米时，让铜凸出（protrude）反而比凹陷更好。](https://www.semianalysis.com/i/58498676/sonys-leading-micron-pitch-hybrid-bonding)

## **晶圆测试 / 切单**

仅对 D2W 而言，需要先做晶圆测试，再把 KGD 切单并重构到载片或膜框（tape frame）上以便后续加工。如前所述，混合键合给传统晶圆测试流程带来了新的麻烦。晶圆测试需要用探针接触晶圆的凸点或焊盘进行电学测试。

探针会在铜焊盘表面造成轻微损伤，破坏 CMP 工序获得的表面平整度。虽然这种焊盘损伤通常很轻微、多数情况下可以接受，但混合键合对微小的形貌变化要敏感得多——这些变化会影响键合质量。一种解决办法是在初始 CMP 时预先补偿，再在探针测试后追加一轮 CMP，把探针造成的损伤抛掉。

![](https://substack-post-media.s3.amazonaws.com/public/images/9b7908c9-4136-4405-a77d-9c3a6fee0c1e_564x378.png)

至于切单/切割，问题在于工艺产生的颗粒。[刀轮切割](https://www.semianalysis.com/p/disco-corporation-the-world-leader)一般不被采用，因为它最脏：产生大量颗粒和大量良率损失。[激光切割和等离子切割](https://www.semianalysis.com/p/disco-corporation-the-world-leader)比刀轮切割干净得多，因而更受青睐，但仍会产生颗粒物。等离子切割是最极端的方法，机理类似于把分隔裸片的划道刻蚀掉，但刻穿整片晶圆耗时较长，吞吐量低得多。

![](https://substack-post-media.s3.amazonaws.com/public/images/c6db2bf0-c18b-4299-9c13-66db0f5902e0_992x652.png)

Disco 是这一领域的领导者。自我们撰文分析它以来，其股价已涨至原来的三倍以上。

一种缓解办法是先在晶圆上涂覆保护层。颗粒落在保护层上，剥离保护层时可一并去除。这有助于解决切单期间的颗粒问题，但保护层可能留下残留物，剥离过程也可能对混合键合层造成一些表面损伤，加大表面粗糙度。

## **等离子活化与清洗：**

现在对两片晶圆进行键合前处理：用 N2 等离子体活化表面。等离子处理改变表面特性，提高表面能并使其更加亲水。两面都更亲水后，表面之间才便于形成氢键。[这有助于实现下一步在室温下形成的初始弱介质-介质预键合](https://ieeexplore.ieee.org/document/9026700)。

处理之后，进行最终清洗以去除累积的颗粒。键合之前，来料晶圆务必尽可能干净。清洗既要彻底，又不能造成损伤，以保持混合键合界面的完好。最佳方案似乎是辅以[兆声波](https://www.semianalysis.com/p/acm-research-chinas-most-successful)的去离子水清洗。使用刷洗（scrubber）或基于等离子的清洗可能损伤过大和/或引入污染物。

![](https://substack-post-media.s3.amazonaws.com/public/images/3c68a15f-2722-40a7-9386-6b8ec6d1c50c_861x776.png)

## **键合**

现在到了键合步骤。更准确地说这是一步「预键合」，因为此步只形成初始的介质-介质键合，只是较弱的范德华键。W2W 与 D2W 的流程我们将分别讲述。

## **W2W 键合**

W2W 键合良率更高的原因在于对准与键合是分开的步骤。先看对准。W2W 对准有多种技术。过去使用红外（IR）扫描仪检查两片晶圆间的对准，局限在于其中一片晶圆必须对红外透明。这对 CMOS 晶圆行不通，因为红外无法穿透金属层。

在 W2W 键合领域占主导地位的 EVG 拥有专利的 SmartView 对准技术。两台相互标定的相机，一台置于晶圆上方，一台在下方。移动夹持上层晶圆的卡盘，让下方相机识别对准标记，系统记录该标记的位置；上层晶圆退回后，下层晶圆移动到两台相机之间，直到上方相机识别出对准标记。对准机通过计算两个对准标记的相对位置即可完成两片晶圆的对准。为帮助保持精度和可控性，两片晶圆彼此非常接近（50 微米以内），卡盘只在 X、Y 平面移动，预键合之前不做 Z 轴（垂直）运动。

对准完成后，晶圆被移入键合腔室，以较小压力压合约 20 分钟，形成初始键合。

键合后的检测可通过声学方式在线完成；若对准不达标，键合还可以返工。

![](https://substack-post-media.s3.amazonaws.com/public/images/5968a62d-3a58-4643-9a2f-494b3c5fbcf2_559x651.png)

在 W2W 设备中，有独立的腔室负责对准。上下晶圆对准后，被移入键合腔室（真空中），以一定压力压合，约 20 分钟后形成初始预键合。W2W 的关键在于步骤更少、工艺更洁净。对准和键合之前可以先清洗晶圆，去除大部分颗粒。颗粒污染源之一的裸片切单只发生在键合之后。

而且，由于这是晶圆级工艺，对准步骤可以有更充裕的时间——对准时间长对吞吐的损害远小于芯片级工艺。腔室内的机械运动也不多，腔室自身产生的污染物更少。目前 W2W 键合机可实现 **50nm 以下的对准精度**。W2W 键合已是成熟工艺，并不特别昂贵。证据是：它已广泛应用于 Sony、OmniVision、三星的图像传感器以及 YMTC、西部数据、Kioxia 的 NAND 等大众市场产品。

## **D2W 键合**

D2W 键合通过拾放设备完成。

下层目标晶圆置于晶圆卡盘上。待键合的裸片正面朝上放在膜框上。翻片臂拾取单颗裸片并翻转，使其背面朝上停在翻片臂上。上方键合臂用键合头的真空吸嘴吸起翻转后的裸片。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

下面我们将详细讨论 D2W 键合、退火、自组装（self assembly）以及所有相关设备公司。
