---
title: "晶体管的未来"
title_en: "The Future of the Transistor"
subtitle: "从平面晶体管到 FinFET、纳米片、互补型 FET，再到 2D 材料"
date: 2023-02-21
source: https://newsletter.semianalysis.com/p/the-future-of-the-transistor
crawled: 2026-09-15
authors: ["Dylan Patel", "Afzal Ahmad"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 晶体管的未来

> 原文：[The Future of the Transistor](https://newsletter.semianalysis.com/p/the-future-of-the-transistor) · SemiAnalysis

**从平面晶体管到 FinFET、纳米片、互补型 FET，再到 2D 材料**

任何芯片的最基本元件都是晶体管——它不久前刚度过 75 岁生日。今天我们要讨论的是接下来的 25 年。晶体管本质上是电流的开关：施加在其「栅极」上的电压，可以让电流在「源极」与「漏极」之间的沟道中流动。每个晶体管都可以导通或关断，分别对应「1」或「0」。在摩尔定律等比例缩放与 CMOS 工艺技术进步的驱动下，现代计算芯片可以以数十亿乃至数万亿的规模做到这一点。

理想的晶体管应做到以下几点：

1. 导通时流过尽可能大的电流
2. 关断时不允许任何电流通过
3. 开关速度尽可能快。

![](https://substack-post-media.s3.amazonaws.com/public/images/8ffde20c-c267-414e-80a7-9a993d7a4391_635x558.png)

晶体管的三个主要组成部分：「栅极」「源极」与「漏极」

## **晶体管简史**

晶体管于 1947 年诞生于 AT&T 的贝尔实验室，发明者为 John Bardeen、William Shockley 和 Walter Brattain。最早的晶体管被称为「平面」（planar）晶体管，因为包括栅极、源极和漏极在内的晶体管全部元件都位于同一个二维平面上。

![](https://substack-post-media.s3.amazonaws.com/public/images/cac067e6-c533-4e8e-ba68-7f0fc99f0795_524x429.jpeg)
*https://www.asml.com/en/news/stories/2022/what-is-a-gate-all-around-transistor*

在许多代技术里，平面晶体管的开关速度都可以通过缩小栅长来提升。对硅沟道进行「应变」（strain）处理同样能提高开关速度。要使沟道产生应变，需在硅锗（SiGe）层上放置一层硅。当硅层中的原子与 SiGe 层对齐时，硅原子之间的键会被拉伸，从而使沟道产生应变。在这种硅原子间距被拉大的构型中，干扰电子运动的原子间作用力得以减小。应变沟道中的电子迁移率（即电子在电场牵引下移动的快慢）可提升 70%，带来晶体管开关速度提高 35%。

![](https://substack-post-media.s3.amazonaws.com/public/images/7137f46a-87bd-4c2f-a218-0e0730982dd0_1000x725.png)

让等比例缩放得以延续的另一项进展，是「高介电常数/金属栅」（High-K/Metal gate）的开发。到了 45nm 节点，栅介质的绝缘（介电）特性开始失效，漏电流过大（即晶体管处于关断状态时仍会有显著电流流过）。

栅介质是一层极薄的绝缘层，传统上由二氧化硅制成，位于晶体管的金属栅电极与电流流经的沟道之间。英特尔在其 45nm 工艺（2007 年）上取得重大突破，采用铪基介质层，并以替代性金属材料构成栅电极。业界其他厂商在 3 年后跟进。这一组合带来了「高介电常数」（high dielectric constant，即「high-K」）栅极。

![](https://substack-post-media.s3.amazonaws.com/public/images/a96616d7-eab2-4a0e-ae14-752fc52634df_591x815.png)

随着晶体管尺寸持续缩小，源极与漏极之间的间距缩小到栅极已无法妥善控制沟道电流流动的地步。正因如此，平面晶体管出现了显著的「短沟道」效应，尤其是在 28nm 节点以下，漏电流过大。

![](https://substack-post-media.s3.amazonaws.com/public/images/607ed5b7-fa49-464d-9f93-5fc38819ae87_457x374.jpeg)
*https://www.asml.com/en/news/stories/2022/what-is-a-gate-all-around-transistor*

为应对这一挑战，业界转向了「3D」晶体管，即 FinFET。

[在 FinFET 中，栅极从硅鳍的三个侧面包裹沟道，而不再像平面晶体管那样只覆盖其顶部。](https://alwaysbecurious.substack.com/p/learn-about-the-tiniest-new-transistors)这带来了对晶体管电流更强的控制能力；FinFET 晶体管的开关时间显著快于平面晶体管。2010 年代初，英特尔在 22nm 节点将 FinFET 投入量产；台积电（TSMC）等代工厂则在 3 年后在 16nm 节点上大规模导入 FinFET。

![](https://substack-post-media.s3.amazonaws.com/public/images/f505729a-7ec0-49fc-8321-20424ada969c_575x470.jpeg)
*https://www.asml.com/en/news/stories/2022/what-is-a-gate-all-around-transistor*

由于鳍可以做到多薄/多高存在极限，能够并排放置的鳍数量也有限，业界目前正处于晶体管的新一轮演进之中。这类下一代晶体管被称为「环栅」（Gate-All-Around）晶体管，即 GAAFET。GAA 采用水平堆叠的「纳米片」，使栅极从四个侧面完全包裹沟道。这进一步提高了晶体管的驱动电流与整体性能。每个纳米片的宽度以及每个晶体管中纳米片的数量都可以调整，从而实现定制化设计。

2022 年，三星（Samsung）开始在 3nm 工艺上使用 GAA。由于良率问题，三星 3nm GAP 工艺的大批量芯片预计要到 2024 年才会面世。英特尔将 GAA 列入其 20A 制程节点路线图，2024 年达到可量产状态、2025 年产品大规模出货。台积电将在 2025 或 2026 年的 N2 节点上导入 GAA。这些量产年份都只是目标；在我们看来，这几家厂商中至少有两家进一步推迟的可能性很大。

![](https://substack-post-media.s3.amazonaws.com/public/images/cd38e658-4354-4065-bfe9-d375635409f7_1125x199.jpeg)

在初代 GAA 工艺之后，路线图还包括转向 forksheet 或 3D 互补型 FET（CFET）——即把 n 沟道与 p 沟道靠得更近，或垂直堆叠。

要让 2nm 之后的路线图继续走下去，向环栅（GAA）的过渡还需要为纳米片引入新的晶体管沟道材料。这是因为硅、锗这类体材料的电子迁移率在 < 5nm 时会显著下降。随着尺度深入纳米量级，原子层面的效应已不容忽视。解决这些挑战最有前景的材料家族，或许当属 *2D 材料*。

[分享](https://newsletter.semianalysis.com/p/the-future-of-the-transistor?utm_source=substack&utm_medium=email&utm_content=share&action=share)

## **2D 材料**

2D 材料是由单层原子构成的晶体固体。最著名的 2D 材料是石墨烯（Graphene）——碳的一种同素异形体，由排成六方晶格的单层原子组成。但值得注意的是，石墨烯没有带隙。

![](https://substack-post-media.s3.amazonaws.com/public/images/9a3e9e1a-9b7b-4013-8a73-2f9b674ea805_2000x1143.png)

半导体的定义在于其带隙：即把一个被束缚在价带（无法导电）中的电子激发到导带（可以导电）所需的能量。带隙必须足够大，才能让晶体管的导通态与关断态形成清晰的反差，也才能在处理信息时不产生错误。尽管电子迁移率很高，但没有带隙的石墨烯无法用作半导体材料。虽然掺杂后的石墨烯可以产生带隙，但掺杂石墨烯无法实现足够低的关态电流或足够高的开态电流。

用于下一代纳米片最有前景的 2D 材料，来自「过渡金属硫族化合物」（Transition Metal Dichalcogenide，TMD）子家族。该族材料包括二硫化钼（MoS2）、二硫化钨（WS2）和二硒化钨（WSe2）。TMD 兼具 < 5nm 沟道厚度所需的带隙与迁移率组合。

![](https://substack-post-media.s3.amazonaws.com/public/images/906e5e1d-38f3-45b9-8907-903fada20c42_1201x639.png)

H.-S. Philip Wong 在其 HotChips 2019 主题演讲《What will the next node offer us?》（下一个节点将带给我们什么？）中重点强调了这一点。

![](https://substack-post-media.s3.amazonaws.com/public/images/2bbc2787-7df9-4cfa-b76c-332274c3f84e_1201x632.png)

虽然碳纳米管（CNT，属于一维材料）也被重点提及，但经过 30 多年的研发，其制造难度之大依然出了名。要让晶体管应用达到预期的性能指标，必须生长出数百万根单管（即密度），且全部朝同一方向排列（即对准）。此外，CNT 只涉及碳这一种元素。2D 材料则灵活得多——它指的是一整个材料家族，而且理论上比 CNT 更容易制造：可以先生长出大面积单层薄膜，再进行转移。

## **2D 材料的生长**

2D 材料通常通过化学气相沉积（CVD）生长，近期的努力也包括原子层沉积（ALD）。根据衬底与工艺参数的选择，2D 薄膜可以单层或多层生长。

以最成熟的 2D 材料——单层石墨烯为例，如今主要通过 CVD 在铜箔或铜膜衬底上生长。然而，目前的 CVD 生长技术得到的是「多晶」石墨烯，晶格中存在多处晶界。生长过程也不稳定，意味着晶圆与晶圆之间难以保持一致性。由于晶界及其他缺陷，本征 CVD 石墨烯的电子迁移率往往仍远低于 10,000 cm2/(V⋅s)，与载流子浓度为 1012 cm−2 时纯净机械剥离石墨烯薄片所报道的 200,000 cm2/(V⋅s) 相去甚远。

剥离（exfoliated）石墨烯指从石墨上层离出来的纯净石墨烯薄片；2004 年石墨烯正是以这种方式首次被分离——曼彻斯特大学的两位研究者（Andre Geim 和 Kostya Novoselov）用透明胶带从石墨上层层撕下石墨烯。

可以想象，当一种材料/晶圆的性能波动如此剧烈时，量测/检测（metrology/inspection）会变得极其困难。

![](https://substack-post-media.s3.amazonaws.com/public/images/8624bf51-944e-40b3-b519-692425fddcbf_318x319.jpeg)
*CVD 生长石墨烯时出现「晶界」的示例。这种生长被称为「多晶」生长*

正因如此，如今的石墨烯电子市场微不足道，少数参与者主要专注于传感器（如霍尔效应传感器）或 MEMS 器件（光刻规则不那么严苛/线宽更大、可以容忍更高的性能波动等）。Cardea Bio 和 GrapheneDX 等公司正在专门研究石墨烯生物传感器，因为石墨烯具有生物相容性，且可以通过场效应传感（Field Effect Sensing）功能化，用以检测各种分子化合物。Graphenea 和 Applied Nanolayers 等其他公司（均位于欧洲）则在建设专用石墨烯代工线。

MoS2 和 WS2 等 TMD 材料则更为早期，目前通常在蓝宝石晶圆上生长。Aixtron 和牛津仪器（Oxford Instruments）是目前仅有的两家销售 2D 材料专用生长设备的前设备厂商（OEM）。要让 2D 材料被业界严肃对待，必须开发出晶圆间一致性更高的生长工艺，长期目标是获得「单晶」材料。

## **2D 材料的转移**

由于 2D 材料生长往往在较高温度（>600° C）下、在铜或蓝宝石等优化衬底上进行，因此需要一个转移步骤，把 2D 材料挪到最终的硅晶圆上。

目前把 2D 材料从生长衬底转移到目标硅器件晶圆的方法，对 CMOS 市场而言并不够用（需要湿法化学/蚀刻液、金属沉积、牺牲聚合物层、会留下残留物的热释放胶带（TRT）和/或激光解键合的某种组合）。最常规的 2D 转移技术是湿法蚀刻掉铜衬底，并用聚甲基丙烯酸甲酯（PMMA）聚合物把 2D 材料拾取并转移到目标衬底上。然而，转移后 PMMA 残留物会留在石墨烯表面，劣化石墨烯的电学性能。

今天的 2D 材料转移方法对于传感器或「卷对卷」/显示等某些应用/器件已经够用，但在质量、产能和污染方面仍未达到 CMOS 的门槛。

![](https://substack-post-media.s3.amazonaws.com/public/images/0824de86-b6ae-4fb2-ac58-601c51df38cc_1430x781.png)
*当今用于石墨烯的转移工艺示例。*
![](https://substack-post-media.s3.amazonaws.com/public/images/128081a8-9c5b-420b-9a1b-5d6f691f8f7a_1172x652.png)
*牛津仪器（Oxford Instruments）的石墨烯器件工艺流程示例*

## **直接生长 vs. 转移**

虽然在硅上直接生长 2D 材料是更理想的方式，但迄今为止，要实现低温、高质量的生长方案仍然困难。ALD 虽然允许比传统金属有机 CVD（MOCVD）更低的温度，但产能仍然很慢。

或许更好的做法，是把「在优化衬底上较慢的高质量生长步骤」与「高产能、优化过的转移步骤」解耦。这样可以更好地进行工艺优化与良率控制。对于先进节点上昂贵的 < 2nm、High-NA EUV + GAA 晶圆（尤其是每个晶体管需要多个纳米片时），这可能是最优方案。

解耦对晶圆厂（fab）也友好：生长与转移可以异步进行，从而最大限度提高晶圆厂产线的稼动率（实现更高的 WPH，即每小时晶圆产出数）。

最后，转移方式更灵活，比直接生长更容易实现异质结构、堆叠及扭转构型。这有潜力在更长远的未来开启[2D 转角电子学](https://www.quantamagazine.org/how-twisted-graphene-became-the-big-thing-in-physics-20190430/)（twistronics）领域。

## **IEDM 上的 2D 亮点**

在旧金山举行的第 68 届 IEDM 年会，为半导体与计算产业的未来提供了绝佳的视角。在与会业界领军者的演讲中，英特尔纪念晶体管诞生 75 周年的报告尤其引人注目，它既回顾了历史，也展望了未来可能的方向。

![](https://substack-post-media.s3.amazonaws.com/public/images/2565c33e-8003-404d-bbdc-a71add9b7345_624x309.png)
*Ann Kelleher 在 IEDM 的主题演讲：《庆祝晶体管 75 周年！展望下一代创新机遇》*

随着摩尔定律放缓，新技术开始驱动性能提升，无论是后硅沟道时代，还是封装技术。英特尔的报告提出了三个可能推动行业与缩放目标前进的方向：新型介质、定向自组装（用于纳米图案化）以及 2D 材料。

2D 材料在本次会议上表现得格外抢眼。业界对近期未来有清晰的路线图：FinFET 与 GAA 架构将延续硅沟道的统治地位。再往后会发生什么，则更具挑战性、也更加模糊。值得注意的是，[英特尔演示了一种 GAA 结构中的 2D 材料沟道](https://www.intel.com/content/www/us/en/newsroom/news/moores-law-paves-way-trillion-transistors-2030.html#gs.p17zba)，具有低漏电和接近理想的开关特性，这是朝着垂直堆叠晶体管迈出的重要一步。[IMEC 的路线图](https://www.imec-int.com/en/articles/smaller-better-faster-imec-presents-chip-scaling-roadmap)则提出互补型 FET（CFET）作为类似方案，其中基于 WS2 或 MoS2 等单层过渡金属硫族化合物（TMD）的 n 沟道与 p 沟道被堆叠起来。

本次 IEDM 还设有 2D 沟道技术专场，由斯坦福大学的 Eric Pop 博士与 IBM 先进 CMOS 逻辑项目的 Nicolas Loubet 共同主持。

各论文/报告聚焦 2D 晶体管的多个方面，包括沟道、栅介质、所需衬底/材料，以及降低接触电阻以提升器件性能。以下是对其中部分论文的技术评述：

![](https://substack-post-media.s3.amazonaws.com/public/images/d58b2290-fffe-44ce-ba26-cf329300a68e_1430x632.png)

在众多进展中，中国北京大学展示的研究包括顶栅 CVD 生长 WSe2 pFET，其漏极电流达 594 uA/um，以及基于 WSe2/MoS2 的 CFET¹。与传统平面 IC 相比，该 CFET 结构性能提升 8%，面积缩减 44%。但仍存在诸多挑战，主要在可制造性方面。本文演示的 CFET 几乎完全以兼容晶圆厂的方式制造，唯一例外是 nFET 中 MoS2 沟道采用了湿法转移。可扩展的干法转移技术，将是这类技术走向量产的关键。

![](https://substack-post-media.s3.amazonaws.com/public/images/44e4e3df-897f-45a3-955a-f7434ec401d3_936x368.png)

2D CFET 结构与集成面积缩减。垂直堆叠可以在不损失性能的情况下实现密度高得多的器件。¹

这种垂直堆叠路线在研发上的挑战，主要在于源漏接触的放置以及互连接触材料的选择。台积电在另一篇 IEDM 论文中，针对 SiN 上转移型 MoSe2 沟道器件²，为此类目的的理想材料提供了洞见。选择接触材料的难点在于找到理想功函数与较弱费米能级钉扎效应的组合；台积电选择利用薄层锑（Sb）和高功函数的铂（Pt），在 WSe2 沟道的 nFET 与 pFET 中实现这一目标。这项接触工程带来了已报道的最低接触电阻：pFET 为 0.75 kΩ-um，nFET 为 1.8 kΩ-um。其中 nFET 相比此前已报道的数值，接触电阻降低了 72%，是 2D 沟道在逻辑应用上迈出的一大步。

接触电阻只是器件总电阻的一个组成部分；侧墙（spacer）电阻是器件性能不佳的另一大因素，在 pFET 中尤甚。台积电在另一篇 IEDM 论文中，利用多层 WSe2 氧化形成的 WOx，与 WSe2 沟道配合，作为低阻侧墙掺杂³。WOx 作为高浓度 p 型掺杂，被发现可降低肖特基势垒高度，即便引入掺杂（1 kΩ-um），总电阻仍得以下降。

![](https://substack-post-media.s3.amazonaws.com/public/images/e7a58e95-6e5d-44d0-93f1-e5239138dfa0_777x585.png)

pFET，采用多层 WSe2 氧化形成的 WOx 掺杂。³

尽管基于 TMD 的器件前景可期，但 TMD 的生长方法存在一个根本性问题：转移法会留下聚合物残留，而用 MOCVD 在氧化物上直接生长则会带来多种缺陷，最明显的是有机污染和硫空位。IEDM 上有多篇论文同时涉及转移与直接生长两种方法。

英特尔展示了一种基于转移 MoS2 的 2D FET，源漏接触长度为 25 nm，可与当前硅制程节点媲美。测试器件在源漏间距低于 34 nm 时，亚阈值摆幅出现上升（SSsat= 75 mV/dec）。不过，英特尔的工艺采用了基于 ALD 生长牺牲介质层的层转移工艺，会留下大量残留物，并导致源极和漏极接触处的 MoS2 脱层。为了满足制造和未来的良率目标，转移方法必须做到无残留且全干法，否则就应采用直接生长方法。

直接生长的进展也有讨论，会上观察到采用 CVD、更兼容晶圆厂工艺的方案。北京大学的一篇论文介绍了一种低接触电阻（0.65 kΩ-μm）、纯欧姆接触⁵ 的 WSe2 pFET。该器件沟道长度 120 nm，在 6nm SiO2 上生长时创下了纪录级的性能（Ids= 425μA/μm，gm=80μS/μm，SSsat=200 mV/dec）。该工艺还兼容在 Si/HfLaO 介质膜上生长，只是性能略差（Ids=370μA/μm，gm=100μS/μm，SSsat=250 mV/dec）。然而，第一件器件制造中 890° C 的生长高温，对可制造性构成了晶圆厂兼容性风险。尽管如此，这项工作确实代表了 p 型 2D TMD 材料的重大进展——这正是 2D 材料领域中有待发展的方向之一。

2D 材料还出现在 MoS2 晶体管的介质界面工程中，采用 hBN 作为封装层⁶。这项工作实现了已报道的 CVD 生长单层 MoS2 器件的最低亚阈值摆幅。该封装层似乎还提升了器件可靠性：在 Al 种子层与顶栅沉积之后，关态劣化更少，说明介质层将后续工艺带来的损伤降到了最低。这代表了基于 2D 材料的器件可靠性与寿命方面的进步。当对 TaOx 掺杂层使用钽（Ta）种子层时，据报道可获得高达 Ids= 861μA/μm 的电流和低亚阈值摆幅（72 mV/dec）；而对低功耗应用，据报道可实现高 Ids=598 μA/μm 与 Vds=0.65 V，超越 IRDS 2028 HD 规格。

上述 2D 进展，只是 2D 材料革新这个行业潜力的冰山一角。然而，要在晶圆厂层面把 2D 材料转化为大批量制造，仍存在重大挑战。上述所有论文都采用湿法转移技术，把 2D 材料从生长衬底移到生产晶圆上。虽然如上所见，这些成果足以展示器件潜力，但由于可能引入聚合物残留且产能较低，这种方法无法扩展到大批量制造。尽管如此，随着一届届 IEDM 会议的召开，半导体产业的前进路径愈发清晰：2D 就是未来，在本文作者看来，这不可避免。就目前而言，先进制程阵营似乎更青睐 WS2 与 WSe2，因为它们既能做成 n 型也能做成 p 型。

2D 材料显然是行业的未来，推动该领域前进的动力十分强劲。随着 2D 材料进入半导体堆叠，也需要开发能在产线内有效表征它们的设备。为此，即将举行的 SPIE 光刻与图形化会议上的报告将讨论量测前景与生长进展，演讲方包括英特尔与 IMEC：

- [2D 过渡金属硫族化合物晶体管：是未来的硅替代者还是炒作？](https://spie.org/advanced-lithography/presentation/Are-2D-transition-metal-dichalcogenides-transistors-the-future-silicon-replacement/12498-502?enableBackToBrowse=true&SSO=1)
- [用于超薄 2D 材料层表征的 300mm 产线内量测技术](https://spie.org/advanced-lithography/presentation/300mm-in-line-metrologies-for-the-characterization-of-ultra-thin/12496-65?enableBackToBrowse=true&SSO=1)

此外，牵头欧盟石墨烯旗舰计划[「2D 实验中试线」（2D Experimental Pilot Line）](https://graphene-flagship.eu/innovation/pilot-line/)倡议的 IMEC，将在[下个月的一场研讨会](https://graphene-flagship.eu/events/enabling-technologies-for-graphene-and-tmdc-cmos-integration/)上介绍最新进展；参会者还包括英特尔与台积电。

## **产业下一步**

任何新材料/新工艺技术的第一步，都是进入行业路线图。过去几届 IEDM 以及即将召开的 SPIE 高级光刻会议都清楚地表明，2D 材料如今已稳稳站上路线图。但下一步，是从路线图走向具体行动。

说来容易做来难，但本文作者认为，2D 材料应当首先在较老节点的后道工序（Back-end-of-line）落地（主要在 MEMS、模拟+混合信号（analog+MS）、射频（RF）和光子学代工厂）。2D 材料在 MEMS 器件、5G/6G 射频开关和光子收发器等器件中能带来可观的性能提升。其中若干器件相比晶体管，并不要求最高品质的起始材料。

例如，原型射频开关器件（由 hBN 和 MoS2 等 2D 材料制成）已在 UT Austin 实验室[完成演示与表征](https://thedailytexan.com/2022/06/23/ut-austin-researchers-develop-faster-more-energy-efficient-components-for-6g-networks/)，合作伙伴还包括罗德与施瓦茨（Rohde & Schwarz）等。来自业界主要参与者的初步数据与反馈表明，2D 开关的经典品质因数（FoM）——「Ron x Coff 值」——达到甚至超出了新兴网络频段的预期。

在硅光子学中，目前调制器与光电探测器分开制造、再组装到芯片中；采用 2D 材料后，收发器的全部组件——包括调制器、开关与光电探测器——都可以在同一 2D 材料层内单片集成。当前的调制器材料（如 LiNBO3）体积庞大，需要 2-5 V 的驱动电压。石墨烯马赫-曾德尔（MZ）调制器的电压可以做到 <1 V。诺基亚意大利（Nokia Italia）、爱立信（Ericsson）以及位于亚琛的 Black Semiconductor 都在这一方向上布局。

2D 材料还有望实现更快的光交换。可重构光分插复用器（ROADM）的交换速度目前无法低于数十毫秒。而例如把石墨烯置于微环谐振器之上，可以实现皮秒量级的交换。

一旦工艺、量测与良率问题在后道得到解决，且 2D 材料生长与转移的品质持续改善，业界通往在先进制程/前道工序（front end of line）集成 2D 材料的道路就会清晰得多。在过渡期内，先进制程阵营还需要解决接触电阻、衬底/介质材料和架构（如纳米片数量）等问题，以达到所需的器件性能指标。

每当产业需要攻克一项重大材料/工艺技术来延续摩尔定律时，它都成功做到了。离子注入、High-K 栅极、EUV……例子不胜枚举，2D 也不会例外。然而，让 2D 变成现实所需的制造技术目前正处于「死亡之谷」阶段，因此需要整个行业（来自所有环节，尤其是设备商（OEM）、代工厂/无厂设计公司/IDM 以及量测厂商）拿出更多行动、协作与投资。

正如 IMEC CMOS 技术高级副总裁（SVP）Sri Samavedam [最近所言](https://spectrum.ieee.org/the-transistor-of-2047-expert-predictions)：「在这个行业，从（概念演示）到导入制造通常需要大约 20 年。可以放心地假设，2047 年（晶体管 100 周年）的晶体管或开关架构，已经在实验室尺度上被演示过了。」

![](https://substack-post-media.s3.amazonaws.com/public/images/e8a100a7-9c5e-43ae-bb8d-dad7ef85b320_1430x691.png)

感谢阅读 SemiAnalysis。如果你喜欢这篇文章，请分享出去。这对我们帮助很大！

[分享](https://newsletter.semianalysis.com/p/the-future-of-the-transistor?utm_source=substack&utm_medium=email&utm_content=share&action=share)

## **关于 Lab 91, Inc：**

Lab 91 Inc. 是一家位于得克萨斯州奥斯汀的半导体设备公司，致力于开发在半导体代工厂集成 2D 材料所需的工艺技术与设备。Lab 91 的工具可将 2D 材料从生长晶圆自动转移到目标晶圆，解决代工厂的一大瓶颈。

公司的使命是加速产业向 2D 半导体的转型。

想进一步了解 2D 材料或 Lab 91 的技术，请发送邮件至：[anand@lab91.co](mailto:anand@lab91.co)

[![](https://substackcdn.com/image/fetch/$s_!T7cG!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F5043efab-4e56-45f9-9f79-1dc0258bc629_993x993.png)Always Be Curious认识将为这十年提供动力的最小新型晶体管芯片行业火热的一周！🔥 三星本周将发布其 3 纳米工艺（似乎比台积电抢先几个月），而台积电则继续大力宣传其 2 纳米工艺的进展。这些基于最先进制造工艺的芯片将依赖……Read more4 年前 · Sander at ASML](https://alwaysbecurious.substack.com/p/learn-about-the-tiniest-new-transistors?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

1. X. Xiong et al. “Top-Gate CVD WSe2 pFETs with Record-High Id~594 μA/μm, Gm~244 μS/μm and WSe2/MoS2 CFET based Half-adder Circuit Using Monolithic 3D Integration” IEEE International Electron Device Meeting (IEDM) 2022.
2. A. Chou et al. “High-Performance Monolayer WSe2 p/n FETs via Antimony-Platinum Modulated Contact Technology towards 2D CMOS Electronics” IEEE International Electron Devices Meeting (IEDM) 2022.
3. Hung, Terry et al. “pMOSFET with CVD-grown 2D semiconductor channel enabled by ultra-thin and fab-compatible spacer doping” IEEE International Electron Devices Meeting (IEDM) 2022.
4. C. J. Dorow et al., “Gate length scaling beyond Si: Mono-layer 2D Channel FETs Robust to Short Channel Effects,” International Electron Devices Meeting (IEDM) 2022
5. Shi et al., “High-Performance Bilayer WSe2 pFET with Record Ids = 425 μA/μm and Gm = 100 at μS/μm Vds = -1 V By Direct Growth and Fabrication on SiO2 Substrate,” International Electron Devices Meeting (IEDM) 2022.
6. Lan et. Al., “Dielectric Interface Engineering for High-Performance Monolayer MoS₂ Transistors via hBN Interfacial Layer and Ta Seeding”. International Electron Devices Meeting (IEDM) 2022.
