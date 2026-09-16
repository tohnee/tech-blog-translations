---
title: "台积电 3nm 困局：它究竟还划不划算？——N3 与 N3E 工艺技术与成本详析"
title_en: "TSMC’s 3nm Conundrum, Does It Even Make Sense? – N3 & N3E Process Technology & Cost Detailed"
subtitle: "微缩终于变贵了，摩尔定律在经济意义上已经死了"
date: 2022-12-21
source: https://newsletter.semianalysis.com/p/tsmcs-3nm-conundrum-does-it-even
crawled: 2026-09-15
authors: ["Dylan Patel", "Afzal Ahmad"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 台积电 3nm 困局：它究竟还划不划算？——N3 与 N3E 工艺技术与成本详析

> 原文：[TSMC’s 3nm Conundrum, Does It Even Make Sense? – N3 & N3E Process Technology & Cost Detailed](https://newsletter.semianalysis.com/p/tsmcs-3nm-conundrum-does-it-even) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**微缩终于变贵了，摩尔定律在经济意义上已经死了**

几周前，我们得以参加 IEDM 大会，台积电在会上公布了许多关于其 N3B 与 N3E（3nm 级制程节点）的细节。此外，台积电宣布将增加其在亚利桑那州凤凰城的资本开支，Fab 21 一期与二期总投资达 400 亿美元。该厂将分别生产 N5 与 N3 家族芯片。本报告将覆盖这次制程节点迁移、台积电最先进技术的高昂成本，以及它将如何显著加速行业向[先进封装与小芯片（chiplet）](https://www.semianalysis.com/p/advanced-packaging-part-1-pad-limited)的转向。此外，我们将详列 N5、N4、N3B、N3E 的各种间距、特征尺寸与 SRAM 单元尺寸。

## **台积电 5nm 晶圆厂成本**

2018 年初，[台积电宣布投资一个新厂区](https://pr.tsmc.com/english/news/1951)。这个新厂区将承载其最先进的 N5 技术。随着苹果与华为为 2020 年锁定 N5 晶圆，这正是一次超大规模建设的机会。台积电表示，Fab 18 一期至三期的投资将超过 5,000 亿新台币（约 170 亿美元）。该厂区计划每月产出超过 8 万片晶圆。在 2020 年一季度财报电话会上，台积电确认 N5 已进入大批量生产（大概率在一期）。

尽管位于台南科学园区的 Fab 18 仍将是 N5 生产的主基地，台积电也宣布了在美国亚利桑那州凤凰城的扩张。2018 年年中，[台积电宣布该厂区](https://pr.tsmc.com/english/news/2033)总投资 120 亿美元、月产 2 万片晶圆。建成后，这将是台积电在台湾之外制造的最先进制程节点。以 2022 年台积电 N5 月产能远超 12 万片计，该厂约占其 N5 产能的 15%。

乍一看，台湾台南 N5 设施的一至三期规模是 4 倍，却只贵 40%，这给「没有巨额补贴在美国建厂就不经济」的论点提供了弹药。实际上，这些数字不可直接比较。台积电美国厂口径包含 2021 到 2029 年的全部支出——远不止初期 CapEx；而台湾厂的口径只是初期建设，不含其他成本。

要注意，晶圆厂初期建设中约 80% 的总成本来自设备；而运营成本中超过 60% 来自材料、化学品、设备维保与能源投入。无论晶圆厂坐落在哪个地区，这些成本大体相同（能源确有差异）。

## **台积电 3nm 晶圆厂成本**

台南科学园区的 Fab 18 也是 N3 家族节点的主生产基地，四期至六期专用于该家族。位于新竹科学园区的 Fab 12 八期与九期也将生产该节点。最近，[台积电宣布对 Fab 21 二期追加投资](https://pr.tsmc.com/english/news/2977)，扩建其亚利桑那现有晶圆厂以生产 N3 晶圆。亚利桑那的新计划将使台积电总支出增至 400 亿美元，产能提升至每月 5 万片——其中 2 万片仍是 N5、3 万片是 N3。建成后，N3 产能将约占台积电全球 N3 产能的 25%。

这将是台积电首次在同一厂区公开不同世代晶圆厂之间的完整成本对比。有成本超支传闻称，台积电 N5 厂成本可能已从最初约 120 亿美元增至约 130 亿美元；最有可能处于该区间中段。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/b670a3bd-5f5f-4fd8-9f19-47c633f7c8ab_1697x362.png)

每月每片晶圆投片的总支出增幅从 38% 升至 55%。这与我们听到的另一传闻吻合：N3E 定价比 N5 贵约 35%。与 [DigiTimes 传闻](https://www.digitimes.com/news/a20221121PD217/tsmc.html)相反，晶圆价格并非 2 万美元；且 N3B 比 N3E 还要贵上一截。

N3 的故事很复杂。最初，N3 良率难产且昂贵，而性能、功耗与密度的改善平淡，超出多数客户愿意支付的水平。它有约 25 层 EUV，几乎是 N5 的两倍。N3 暴露出许多问题，[最终导致台积电错过了其重大制程节点发布惯常的两年节奏](https://www.semianalysis.com/p/tsmc-3nm-wafer-shipments-pushed-into)。N3B——最初的 N3——于 2022 年四季度投产；N3E 于 2023 年年中至下半年投产。对公众而言最值得注意的变化是：[随着摩尔定律放缓，苹果被迫彻底改变其产品芯片规划](https://www.semianalysis.com/p/as-moores-law-slows-apple-is-forced)。

除了 N3 从 2022 年 iPhone 推迟到 2023 年 Pro iPhone 之外，许多其他客户也从原本的 N3 计划上撤退。围绕 Zen 5、Intel GPU 以及一些博通定制 ASIC 的传闻众多。据传这些公司选择坚守 N5 级节点，或转向放宽的 N3E 工艺。最初的 N3 多数人称之为 N3B，除苹果之外不会有大規模爬坡。我们将在本报告后文深入技术差异，但先说一点：N3E 的 SRAM 位单元尺寸与 N5 级节点相同，并减少了 EUV 曝光次数。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/233344b5-d8e5-4dbe-84a0-8e8e1b5deaa0_1725x487.png)

密度改善最多也只是略好于晶圆成本涨幅。采用 FinFlex 2-1 实现时，密度改善约 56%、成本增加约 35%——折合每晶体管成本改善约 15%，是 50 多年来主要制程技术最弱的一次微缩。

其他实现方式的每晶体管成本持平甚至更差，但换来更高的单晶体管速度提升。注意上述代际改善以 Arm Cortex A72 测量；密度改善会因所实现 IP 不同而变化。

多数芯片设计达不到 56% 的密度改善，而只有低得多的约 30%。这意味着每晶体管成本上升，但各公司正在调整设计以确保不会如此。这将在工艺技术一节解释。

## **3nm 实现成本**

当在最先进制程上实现一颗芯片的成本变得更高时，转向 3nm 还是留在 N5 家族的决策变得更加棘手。

[![](https://substackcdn.com/image/fetch/$s_!HwSb!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F0150776c-9bf2-4bea-a9c2-41b24b7a0f15_1280x1280.png)SemiAnalysisThe Dark Side Of The Semiconductor Design Renaissance – Fixed Costs Soaring Due To Photomask Sets, Verification, and ValidationWe are in the midst of a semiconductor design renaissance. Nearly every major company in the world has their own silicon strategy as they try to become vertically integrated. There are also more chip startups than ever. The industry is rapidly shifting away from using Intel CPUs for everything. As Moore’s law slows, design is flocking towards heterogene…Read more4 years ago · 33 likes · 19 comments · Dylan Patel](https://www.semianalysis.com/p/the-dark-side-of-the-semiconductor?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

我们在此前的文章中详细解释过：在最新制程上实现产品的固定成本正变得如此庞大，以至于对企业构成巨大风险。延迟更难承受，重新流片更昂贵，而最糟的是，实现每晶体管成本改善所需的出货量门槛越来越高。

因此，许多公司将在很长时间内坚守 N5 级节点。另有许多公司只会把计算小芯片转移到 N3 级，而把 SRAM、模拟等其他 IP 留在更老的工艺上。台积电 N3 将带来小芯片与先进封装的爆发。

在进入 N3 工艺细节之前，我们想先详述 N5 家族——它真正印证了台积电的了不起。它不是单一节点的迭代，而是多个并行的版本与改动，各自最贴合不同类型客户的需要。

## **5nm 工艺家族技术详析**

台积电 N5 家族包括：N5、N5P、N5A、N4、N4P 与 N4X。除这些已宣布的版本外，我们预计台积电未来几年还会推出射频优化与漏电优化版本。凭借所有这些变体，台积电希望延长工艺生命周期，并把更多客户推向 N4 节点——部分原因在于其更低的生产成本与更低的客户固定成本。N4 是最新进入大批量生产的节点，已用于联发科天玑 9200、高通骁龙 8 Gen 2 与苹果 A16。

N5 是工程奇迹，发布时毫无争议是最先进的节点。台积电宣称其逻辑密度提升 1.84 倍、同功耗下性能提升 15%、同性能下功耗降低 30%。无数芯片确实享受了性能与功耗的改善，但宣称的密度增益似乎从未兑现。

[正如 Angstronomics 最近揭示的](https://www.angstronomics.com/p/the-truth-of-tsmc-5nm)，这是因为台积电的宣称不实：逻辑密度的增益更接近 52%。虽然密度宣传有水分，但台积电 N5 仍显然是大批量生产中最优秀的节点。

N5 的鳍间距为 28nm，仅略逊于三星 5LPE；接触式栅极间距（CGP）51nm，仅略逊于 Intel 4。通过连续扩散区（continuous diffusion）这一新颖方法，台积电压缩了单元宽度。我们将在未来关于 scaling booster 的文章中详述。

N5 的 M0 最小金属间距为 28nm，较 N7 缩小 30%，有助于缓解信号与电源布线可能造成的瓶颈。M2 金属间距 35nm，台积电拥有 6-track 标准单元——用 2 个 PMOS 鳍 + 2 个 NMOS 鳍的 FinFET 实现的最密可能。N5 还拥有最小的 6T 高密度 SRAM 位单元，尺寸 0.021 μm²，低于 Intel 4 的 0.0240 μm² 与三星 4LPE 的 0.0262 μm²。台积电的 6T 大电流 SRAM 位单元也小至 0.025 μm²，史上第三密。

N5P 是 N5 的工艺优化版。通过对 FEOL 与 MOL 的增强，台积电又榨出 7% 性能与 15% 功耗改善。看起来不多，但妙处在于该优化与 N5 IP 兼容——任何 N5 设计都可轻松移植到 N5P 获得这些增益。在[半导体设计固定成本飙升](https://www.semianalysis.com/p/the-dark-side-of-the-semiconductor)的当下，这一点的影响怎么强调都不为过。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/de785c50-edc9-4a92-8fda-396a9f6dd7a8_1379x776.png)

N4 是 N5 的又一次工艺优化，但伴随小幅设计微缩，也被称为「nodelet」。通过标准单元库优化、小幅光学微缩与设计规则调整，N4 实现了更好的面积效率，还减少了光罩数量与工艺复杂度，使台积电能以低于 N5 的每片晶圆成本生产 N4。

曾有[日经亚洲的传闻称苹果 A16 的代工成本翻倍](https://asia.nikkei.com/Business/Technology/iPhone-14-teardown-reveals-parts-20-costlier-than-previous-model)，但完全失实。与 N5P 一样，其功耗与特性改善来自 FEOL 与 MOL 的进步。

与台积电此前的 nodelet N6 一样，N4 为从既有 N5 设计迁移提供两条路径，各有取舍。其一是 RTO（重新流片），沿用与 N5 相同的设计规则——更便宜、工程量更小、享受的 N4 红利也更少。联发科正是借此在「N4」风险试产之后很快发布了天玑 9000。

其二是 NTO（全新流片），要求用 N4 提供的最新库重新实现逻辑模块并做更多优化——工程量更大但收益也更多，包括小幅面积缩减。

2021 年底，[台积电发布了 N4P](https://pr.tsmc.com/english/news/2874)——N4 的工艺优化版。通过 FEOL 与 MOL 的进一步改进，性能较 N4 再提升 6%，功耗较 N5 降低 22%。

再看特色工艺：[N5A 基于台积电 N5 工艺](https://www.tsmc.com/english/news-events/blog-article-20210602)。该节点技术上并无特别独到之处，但通过了汽车公司在制程节点上要求的全部标准认证，经过优化可在车辆中长期服役——10 年或 20 年——而不退化。

[N4X 是台积电首个面向 HPC 优化的工艺技术](https://pr.tsmc.com/english/news/2895)。N4X 针对 1.2V 以上高压器件优化，性能比 N4P 高 4%。其 FEOL 对鳍做了增强，以支持更高电流、电压与频率。金属叠层经过工程设计，通过降低电阻与寄生电容改善这些高性能器件的供电与信号完整性；叠层还改进了 Metal-in-Metal 电容，通过抑制电压跌落进一步增强供电稳健性、再获 2-3% 性能。

要达到如此高的频率，部分设计规则可能放宽了，但这大概率不是问题——高性能器件更受金属叠层限制，本就用不上那些密度。为提升性能，漏电方面也做了些让步。多数半导体公司不会用这个节点（他们偏好更低功耗/漏电），但 N4X 是某些最高性能应用的有力候选。

下面讨论 N5 家族的关键间距，并单独详列台积电 N4 节点的间距。N5 高密度（HD）库鳍间距 28nm，8 条扩散线对应 210nm 单元高度；接触式栅极间距（CGP）51nm。N5 高性能（HP）库间距相同，但增加 2 条扩散线，单元高度 280nm；HP 库的 CGP 略放宽至 57nm 以支持更高性能。如台积电所述，N4 通过光学微缩实现 6% 面积缩减：HD 与 HP 库的单元高度分别缩至 206nm 与 274nm，CGP 缩至 49nm 与 55nm。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1e4d0b50-b46b-4991-9968-b0e108c18c63_1593x478.png)

N5 最低金属层间距 28nm，是量产中最小的，也是该节点的最小金属间距；其 metal 2 间距 35nm，同样是量产最小。

如前所述，N5 拥有量产中最密的 6T HD 与 HP 位单元。计入 30% 辅助电路开销后，其 HD SRAM 密度为 31.8 Mib/mm²，HP SRAM 密度为 26.7 Mib/mm²。尽管 N4 未进一步缩小 SRAM 位单元，台积电依然领先。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/adcba5d3-9bb8-4597-b23f-af0c0c2ea53b_1338x416.png)

接下来是重头戏——逻辑密度。这可能是最抓眼球的数字，但它无法单独定义一个节点：从 SRAM 位单元到功耗与性能，其他所有特性都必须纳入考量。这些指标按 Bohr 公式计算——小而不密的 NAND2 单元权重 60%，大而密的扫描触发器（SFF）单元权重 40%。台积电在该指标上领先，尽管优势小于其他维度。

其 HD 库密度是量产最高，但 HP 库密度落后于 Intel 4 的 HP。需要说明，按英特尔口径 Intel 4 已「制造就绪」，但真正的大批量制造还有几个季度。无论如何，密度是选择台积电 N5 家族节点最具吸引力的理由之一。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/caa013b3-531d-42d0-9234-479e8569327c_1523x420.png)

台积电 N5 家族是一组出色的节点，单看这些指标并不足以体现其价值。其功耗、性能、面积、易用性、IP 生态与成本的组合无出其右。

## **N3 技术节点**

N3 家族节点包括 N3B、N3E、N3P、N3X 与 N3S。其中许多是为特定目的优化的 nodelet，但有个反转：N3B（最初的 N3）与 N3E 并无承继关系——与其说是 nodelet，不如把它看作一个完全不同的节点。

在 IEDM 2022 上，台积电揭示了 N3B 的部分面貌。N3B 的 CGP 为 45nm，相对 N5 缩放 0.88 倍。台积电还实现了[自对准接触](https://en.wikichip.org/wiki/self-aligned_contact)，使 CGP 得以进一步缩放。我们将在未来系列中详述这一点及其他 DTCO 缩放。台积电还展示了 0.0199 μm² 的 6 晶体管高密度 SRAM 位单元——仅缩了 5%，对 SRAM 未来微缩是个坏兆头。

近年来，芯片设计师高度依赖 SRAM 来提升性能。SRAM 微缩之死夺走了提升性能的一根大杠杆，并将抬高架构在改善功耗与性能特性上的重要性。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/5ab7ba7b-5da3-489a-ba1e-304a61f3f8ee_451x230.png)

相较 N5，台积电最初宣称 N3 将在同功耗下提升约 12% 性能、同性能下降低 27% 功耗，并带来 1.2× SRAM 密度与 1.1× 模拟密度。

IEDM 披露的高密度位单元**只把 SRAM 密度提升了约 5%，与最初宣称的 20% 相去甚远**。

[谁能解释一下台积电为什么又一次避重就轻………](https://twitter.com/david_schor/status/1540807695678291969?s=20&t=FrAXykWypS5vEAMb2toE7Q)

[分享](https://newsletter.semianalysis.com/p/tsmcs-3nm-conundrum-does-it-even?utm_source=substack&utm_medium=email&utm_content=share&action=share)

IEDM 期间，台积电揭示 N3B 的 CGP 为 45nm——迄今已披露的最密，领先 Intel 4 的 50nm、三星 4LPP 的 54nm 与台积电 N5 的 51nm。

虽然逻辑密度提升无疑可期，但 SRAM 密度增益之低意味着 SRAM 密集型设计很可能面临显著成本上涨。N3B 还有良率与金属叠层性能问题。因此，N3B 不会是台积电的主力节点。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/f91ee269-2e2f-48fc-9be5-fb9ba7a240ad_450x245.png)

由于 N3B 未能达到台积电在性能、功耗与良率上的目标，N3E 应运而生，目的就是修正 N3B 的短板。第一个重大变化是略微放宽金属间距：在接触孔、V1、V2、M0、M1 与 M2 金属层上，台积电放弃了 EUV 多重图形化，改用单次图形化。

> 此外，上一代需要 EUV 双重图形化的三个关键层改为单次 EUV 图形化，降低了工艺复杂度、固有成本与周期时间。
>
> ——台积电在 IEDM

EUV 层数从 N3B 的 25 层降到 N3E 的 19 层，同时保持功耗与性能数字相近，逻辑密度也略有缩水。而且，对一颗标准单片芯片（50% 逻辑 + 30% SRAM + 20% 模拟），密度只提升 1.3 倍——对典型单片芯片设计而言，每晶体管成本实际持平，开发成本却更高。

IEDM 期间，台积电揭示 N3E 的位单元尺寸为 0.021 μm²——与 N5 一模一样。这对 SRAM 是毁灭性打击。出于良率考虑，台积电相对 N3B 放弃了 SRAM 单元尺寸的缩微。

> 256Mb HC/HD SRAM 宏与产品级逻辑测试芯片持续展现出优于上一代的缺陷密度。
>
> ——台积电

N3E 的表现比 N3B 好得多，将于明年年中进入大批量生产。给正在计数的人：距 N5 导入已超过 3 年。AMD、Nvidia、博通、高通、联发科、[Marvell](https://www.semianalysis.com/p/marvelldeepdive2022) 以及其他许多公司最终都将用 N3E 作为其先进制程。

与台积电为 N7、N5 家族推出的此前那些 nodelet 不同，N3E 与 N3B 的 IP 不兼容——IP 模块必须重新实现。因此，GUC 等许多公司选择只在更长寿的 N3E 节点上实现其 IP。

N3P 将是 N3E 的后续节点，与 N5P 类似：通过优化带来小幅性能与功耗增益，同时保持 IP 兼容。N3X 类似 N4X，面向极高性能优化；其功耗、性能目标与时间表尚未公布。

N3S 是最后一个已披露的变体，称将是密度优化节点。目前所知不多，但有一些传闻：[Angstronomics 认为它可能是单鳍（single-fin）库](https://www.angstronomics.com/i/61101273/single-fin-library-ns)，使台积电能进一步压缩单元高度。受金属叠层限制，其用途可能有限，但能用上的设计会用。N3S 甚至可能实现背面供电网络（BSPDN）以缓解许多金属叠层问题——不过这尚未证实。

[分享](https://newsletter.semianalysis.com/p/tsmcs-3nm-conundrum-does-it-even?utm_source=substack&utm_medium=email&utm_content=share&action=share)

作为台积电最后一个 FinFET 节点，N3E 及其后续有机会赢得与 N28 比肩的地位——后者是台积电最成功的节点之一。鉴于其坎坷的历史，这不是易事，但台积电已多次证明自己的能力，尤其在其生态方面。

下面我们把 N3B、N3E 与 N5 做个对比。DTCO 与微缩的变化非常有意思。
