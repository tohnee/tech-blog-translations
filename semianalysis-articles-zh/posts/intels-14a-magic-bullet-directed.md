---
title: "Intel 14A 的魔法子弹：定向自组装（DSA）"
title_en: "Intel’s 14A Magic Bullet: Directed Self-Assembly (DSA)"
subtitle: "High-NA EUV 如何在 1.4nm 制程节点上实现经济可行"
date: 2024-04-18
source: https://newsletter.semianalysis.com/p/intels-14a-magic-bullet-directed
crawled: 2026-09-15
authors: ["Dylan Patel", "Jeff Koch"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Intel 14A 的魔法子弹：定向自组装（DSA）

> 原文：[Intel’s 14A Magic Bullet: Directed Self-Assembly (DSA)](https://newsletter.semianalysis.com/p/intels-14a-magic-bullet-directed) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**High-NA EUV 如何在 1.4nm 制程节点上实现经济可行**

Intel 的 18A 节点近来占据了大部分聚光灯——台积电（TSMC）与 Intel 管理层之间围绕 TSMC N2 与 Intel 18A 孰优孰劣的论战仍在继续。然而，对 Intel Foundry 而言，14A 才是生死攸关的节点。赢得客户要从工艺技术开始，而 Intel 正在此处重注押下，但他们需要一代让所有人都安心的时间窗口。客户会用 18A「试水」，把一些非核心业务的次要芯片交给 Intel；如果一切顺利，他们会把 14A 作为其命脉设计的主力工艺——想想 2027 年最大、最贵的裸片，如 AI 加速器、CPU，甚至可能包括移动芯片。

![](https://substack-post-media.s3.amazonaws.com/public/images/6df00e0e-57ec-441d-9038-ef0b7e90b67e_1730x837.png)
*来源：Intel*

Intel 需要赢得这些客户的业务，其 IDM 2.0 代工战略才能成立，否则他们不会有足够的规模和体量参与竞争——毕竟其内部产品业务未来几年还会继续丢失市场份额。没有多个大型先进制程客户，根本不可能运营一家先进制程代工厂。

Intel 将以数年的领先差距，成为第一家在大量量产（HVM）中采用 ASML High-NA EUV 光刻机的厂商。TSMC 和三星（Samsung）都只订购了用于研发的设备。Intel 也许是为了弥补当年在低 NA（low-NA）竞赛中的迟到，一直是 High-NA 最响亮、最坚定的拥趸。随着首台客户所有的 High-NA 光刻机正在其 Hillsboro 晶圆厂装机，Intel 将在 High-NA 光刻机的研发和实战经验上占得先机。

但经济性问题依然存在。我们的模型显示，High-NA 单次曝光[比低 NA 双重成像（double patterning）更贵](https://www.semianalysis.com/p/asml-dilemma-high-na-euv-is-worse)。

其他芯片制造商也已通过寥寥无几的订单和公开表态，明确示意 High-NA 太贵了：

> 技术本身没有价值，只有能服务客户的技术才有价值。所以我们始终与客户一起，给他们最好的晶体管技术、最好的能效技术，而且成本要合理，对吧？更重要的是技术成熟度——在大规模量产中的成熟度，这才是最重要的。一切都要算在一起。所以，每当有新结构、新工具出现，比如 High-NA EUV，我们都会仔细审视：看工具的成熟度、看工具的成本、看达成目标的日程。我们总是在正确的时刻做出正确的决策来服务客户。
>
> C.C. Wei，TSMC 副董事长兼 CEO

那么，既然 High-NA 更贵，Intel Foundry 为什么还要把未来押在它上面？在 SPIE 光刻与先进图形工艺会议上，以及现在 Intel 的新发布中，我们终于听到了答案：**定向自组装（directed self-assembly，DSA）**——Intel 的魔法子弹，能大幅降低光刻成本。

![](https://substack-post-media.s3.amazonaws.com/public/images/13afb197-ea06-4d8e-a130-73af00001086_2537x1160.png)
*来源：Intel*

下文我们将讨论 DSA 是什么、它如何可能让 High-NA 变得经济可行，逐项拆解 DSA 工作原理的技术细节，以及采用这项新技术的风险。我们还将展示一个纳入 High-NA + DSA 的更新成本模型，讨论其在先进逻辑关键层之外的潜在应用，最后分析对相关公司的影响——Intel、TSMC、有望受益的独家 DSA 材料供应商、结合设备订单来看的 ASML 未来前景（与昨日财报风波中的市场共识相当不同），以及更多关于 14A 挑战的内容。

## **为什么需要定向自组装：打破剂量与 CD 的取舍**

推高 High-NA 成本的主要挑战，是关键尺寸（critical dimension，CD）与剂量（dose）曲线及其对吞吐量和每片晶圆成本的传导效应。关键尺寸是光刻机能成像的最小线宽或间距。要在更小的 CD 下获得良好的成像质量，所需的剂量呈指数级上升。由于光源功率有限，交付更高的剂量意味着光刻机必须跑得更慢，等待足够的光子到达每个曝光区域。跑得慢意味着光刻机产出的晶圆更少——对于一台每天折旧超过 150,000 美元的设备来说，这就转化为巨大的成本增加。更详细的讨论见[我们关于 High-NA 成本的文章](https://www.semianalysis.com/p/asml-dilemma-high-na-euv-is-worse)。

更低的曝光剂量让光刻机能够以其最大、受平台限制的吞吐量或接近该水平运行。虽然正常情况下成像质量会差到无法接受，但借助定向自组装可以将其修复。定向自组装（DSA）是一种纳米图形技术，利用嵌段共聚物（block copolymer）的自组织特性，并由预制图形的模板引导。简单来说，它可以修复图形，大幅降低所需剂量，并实际提升最终图形质量。

## **定向自组装（DSA）如何工作**

DSA 的机理就写在名字里：一种会「自组装」的化学物质，并且是在被「定向」的位置上自组装。

![](https://substack-post-media.s3.amazonaws.com/public/images/7483d154-5278-4527-80f3-db0deaeb5836_2021x753.png)
*DSA 集成流程，来源：(Han, E. et al. "DSA materials and processes development for ≤ P24 EUV resist L/S pattern rectification," Proc. SPIE 12956 (2024))*

「自组装」尽管背后的化学很复杂，概念却很直观——初始随机排列的组分，在系统被加入能量后自行组织成有用的结构。想象一下（略有夸张）：一套乐高积木放进烤箱烤一烤就自己拼好了。

![](https://substack-post-media.s3.amazonaws.com/public/images/a8bff5de-53a4-4813-a77e-850160406268_625x643.png)
*嵌段共聚物的自组装：受热后嵌段自行排列，来源：(Gornev, E et al. "Cellular automata method for directed self-assembly modeling," Proc. SPIE 11022 (2019))*

在化学上，这一行为通过嵌段共聚物（BCP）实现。两种聚合物，长度仅几纳米到十几纳米，通过共价键连接形成 BCP。目前使用的最先进聚合物是聚苯乙烯-聚甲基丙烯酸甲酯嵌段共聚物，缩写为 PS-*b*-PMMA。

PS 和 PMMA 这两种聚合物互不相溶。就像油和水一样：PS 是非极性分子，而 PMMA 是极性的——它们会自然分离成层，因为那是能量最低的排布。PS-*b*-PMMA 天然*想要*排列成规则的层状图案。以热量的形式加入能量，能让分子更快找到这一平衡排布。

在实践中，这意味着在晶圆上涂覆 PS-*b*-PMMA 并烘烤不到一小时，就会形成 PS 与 PMMA 交替的规则线条图案，每条线宽约 ~20nm。如果这听起来像是生产超细金属导线、把数十亿晶体管连起来的好起点（先进逻辑的 M0 层）……那你可想对了。

但光靠这种自组装方法本身基本没用，因为线条的位置和取向或多或少是随机的。它需要被引导，这就是光刻登场的地方。

![](https://substack-post-media.s3.amazonaws.com/public/images/3e6a6a10-a7ea-4d4a-ae55-8163dae95a10_1554x1117.png)
*单次 EUV 曝光 vs. EUV + DSA 光刻胶图形修复。下方中间的图展示无引导图形的自组装：看起来整齐，但对集成电路没用，来源：(Han, E. et al. "DSA materials and processes development for ≤ P24 EUV resist L/S pattern rectification," Proc. SPIE 12956 (2024))*

用一次 EUV 曝光来制作引导图形（guide pattern）：由它定义自组装的取向和位置。该流程与普通 EUV 光刻流程非常相似，只是图形要从光刻胶转移到一层专为 DSA 定制的特殊底层（underlayer）上。这层底层只对嵌段共聚物中的一种具有化学亲和性。有了这层带图形的底层，烘烤期间共聚物不仅会彼此对齐，还会相对底层对齐——这样线条就落在恰好想要的位置。

![](https://substack-post-media.s3.amazonaws.com/public/images/ef5c07b2-5963-48d0-88a9-cbf224d2c4be_778x950.png)
*DSA 的化学「魔法」：嵌段共聚物自组装成线，并与下方引导图形对齐，来源：(Han, E. et al. "DSA materials and processes development for ≤ P24 EUV resist L/S pattern rectification," Proc. SPIE 12956 (2024)) 及 SemiAnalysis*

这些线条的关键尺寸由每条聚合物链的长度决定。这意味着 BCP 可以定制，去打印聚合物链能做得多小（或多大）的特征。该应用领域领先的 DSA 化学品制造商已展示 9nm 的 CD，且还有更小的可能。这已足以与 High-NA EUV 互补。

而这里是 EUV 引导图形的关键细节：它可以用低得多的剂量来制作。DSA 分子会自组装成线边缘粗糙度（LER）极低的线条，无论引导图形本身的 LER 如何。它们会与引导图形的*平均*位置对齐。只要引导图形放置得足够准（这一点可以做到，EUV overlay 精度非常好），EUV 曝光的 LER 就可以很差——DSA 能把它修复。放宽对 EUV 曝光成像质量的要求，意味着剂量可以降低 50% 或更多。

我们采用 50% 这一剂量削减数字，是基于现有可复现研究的合理假设。Intel 早期的研发工作使用一种可直接用 EUV 曝光形成图形的「新型底层」（而非从光刻胶转移图形），表明 25 mJ/cm2 的剂量是可行的——相当于减少 3-4 倍。如果这能投入量产，那么成本节省将远高于我们下文保守建模的结果。

![](https://substack-post-media.s3.amazonaws.com/public/images/5ded2f28-04bf-4733-81ce-8e72d8dc88b1_2289x1023.png)
*采用可图形化底层 + DSA，可实现仅 25 mJ/cm2 的 EUV 剂量，来源：(Han, E. et al. "DSA materials and processes development for ≤ P24 EUV resist L/S pattern rectification," Proc. SPIE 12956 (2024))*

图形化拼图的最后一块是干法刻蚀：PS-*b*-PMMA 可以被选择性刻蚀，只把极性分子（PMMA）去掉。PS 成为线条，PMMA 留出间隙——其最终作用与显影后的光刻胶基本相同，因此可以使用典型的显影后集成流程（图形转移到硬掩膜、SOC、衬底等）。

归根结底，实验结果不言自明。Intel 展示了在使用 DSA 修复图形时，自对准 EUV 光刻-刻蚀-光刻-刻蚀（litho-etch-litho-etch）方案出色的良率结果：

## **有什么坑？（风险）**

到目前为止，这对 DSA 来说是一个近乎完美的故事。鉴于上文描述的产品特性，每家芯片制造商都应该在每个 EUV 层使用它。但目前他们并没有。这项技术在实验室里已经卡了十几年。为什么？

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

下面我们将讨论 Intel 采用这项新技术的风险。我们还会展示一个纳入 High-NA + DSA 的更新成本模型，讨论其在先进逻辑关键层之外的潜在应用，最后分析对相关公司的影响——Intel、TSMC、有望受益的独家 DSA 材料供应商、结合设备订单来看的 ASML 未来前景（与昨日财报风波的市场共识相当不同），以及更多关于 14A 挑战的内容。
