---
title: "NAND 闪存垄断被打破？东京电子 Moly 沉积 + 低温刻蚀挑战 Lam Research 争夺 NAND 的未来"
title_en: "NAND Flash Monopoly Broken? Tokyo Electron Moly Dep + Cryo Etch Takes On Lam Research For The Future Of NAND"
subtitle: ">$1B 营收影响：Lam Research 2025 年来自低温刻蚀 + Moly 沉积的营收几何？"
date: 2023-07-16
source: https://newsletter.semianalysis.com/p/nand-flash-monopoly-broken-tokyo
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie", "Gerald Wong"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# NAND 闪存垄断被打破？东京电子 Moly 沉积 + 低温刻蚀挑战 Lam Research 争夺 NAND 的未来

> 原文：[NAND Flash Monopoly Broken? Tokyo Electron Moly Dep + Cryo Etch Takes On Lam Research For The Future Of NAND](https://newsletter.semianalysis.com/p/nand-flash-monopoly-broken-tokyo) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**>$1B 营收影响：Lam Research 2025 年来自低温刻蚀 + Moly 沉积的营收几何？**

数字逻辑与 DRAM 的摩尔定律几乎已经消亡，密度与成本的改善进展缓慢如冰川。NAND 闪存却并非如此。与半导体行业其他领域不同，NAND 一直享受着可观的年度成本下降。

这是因为 NAND 彻底改变了公式，不再依靠光刻来图形化更小的存储单元。相反，NAND 依靠的是另一种架构——3D NAND，于 2013 年首次商业化。自那以后，NAND 厂商通过不断增加存储单元层数来改善 NAND 的密度和成本结构。重心几乎完全从光刻转移到了沉积和刻蚀工艺步骤。因此，自 3D NAND 推出以来，密度以每年 30% 的速度非常稳定地提升。

今天我们将覆盖 NAND 半导体市场、工艺技术缩微路径、制造流程、NAND 价格趋势、当前的供给过剩/未来的短缺、2023 至 2025 年 NAND 晶圆厂设备（WFE）支出展望、Western Digital 与铠侠（Kioxia）的未来、YMTC、一起潜在的违反制裁事件、NAND 高深宽比刻蚀市场深度解析、3D DRAM 的可能性、沉积领域即将到来的重大材料变更，以及由于两项制造工艺变化导致的 Lam Research 向东京电子（Tokyo Electron，TEL）的潜在市场份额大转移——这代表着超过 $1B 的营收可能易手。

一如既往，技术背景将向所有人详细展开。NAND 沉积与刻蚀的 2 项新进展、3D DRAM 可能性、业务影响、变化、高层结论以及 WDC/铠侠点评将向订阅者详细展开。我们纳入了在 VLSI Japan 和 Semicon West 现场从设备厂商和 NAND 制造商处收集的市场情报。

自 3D NAND 推出以来，密度的提升使 NAND 每比特成本每年下降约 21%，预计缩微仍将继续，尽管前方可能有一些挑战。美光（Micron）认为 NAND 每比特成本可以继续以每年低至中双位数（low to mid-teens）的百分比下降，而 DRAM 更难缩微，只能以每年高个位数百分比为目标降低成本。这一低至中双位数的水平，相比行业直到最近还享有的 21% 是一种倒退。

最终结果是，尽管 2018 到 2022 年 NAND 晶圆厂的设备采购总额每年约为 $15 billion，NAND 总产能却持续以每年超过 30% 的速度增长。这主要归功于制造效率的提升。然而，除非新的设备创新推向市场，否则未来继续扩大产能将需要成比例更大的资本开支（资本开支强度）。另一方面，由于当前的半导体下行周期，市场上 NAND 严重供过于求，大型资本开支项目正被推迟。这为 1.5 年后的短缺埋下了完美伏笔。

![](https://substack-post-media.s3.amazonaws.com/public/images/5c44db81-34aa-4cd2-b493-5cef8dd611bf_1924x1346.png)

NAND 成本大幅改善的主要原因在于，晶圆厂可以在工艺步骤数量没有相应大幅增加的情况下提升密度。3D NAND 最关键的步骤是薄膜沉积和高深宽比刻蚀。

NAND 的制造流程简化来说就是：先沉积交替叠层薄膜，然后进行几种不同的刻蚀，贯穿叠层并分割存储单元/将其连接到外界。Lam Research 是其中许多工艺步骤的领导者，包括最关键的高深宽比刻蚀。

![](https://substack-post-media.s3.amazonaws.com/public/images/2af03fa9-eef8-462d-971b-057e9b489b16_2919x1501.png)

## **NAND 缩微的 4 条路径**

每片晶圆 NAND 闪存存储容量的缩微主要有 4 条路径。

1. 逻辑缩微（Logical scaling）——每个存储单元存储的比特数。这要求每个单元存储 2^n 个电压级别。
2. 垂直缩微（Vertical scaling）——垂直堆叠的 NAND 单元数量
3. 横向缩微（Lateral scaling）——在 2D 平面上能容纳的单元尺寸/数量
4. 架构缩微（Architecture scaling）——各种提升密度、降低单元/外围电路开销的技术。

![](https://substack-post-media.s3.amazonaws.com/public/images/9999fdce-3bab-4851-a98e-ce47b44da5de_1345x893.png)

一种方法是**逻辑缩微（Logical Scaling）**，即在每个物理存储单元中存储更多比特。单元每增加一个比特，就要求单元必须保持的可分辨电压状态数量翻倍。即：每单元 1 比特（SLC）对应 2 个电压级别，每单元 2 比特（MLC）对应 4 个电压级别，每单元 3 比特（TLC）对应 8 个电压级别，每单元 4 比特（QLC）对应 16 个电压级别，每单元 5 比特（PLC）对应 32 个电压级别。

理想情况下，这提供了「免费」的缩微——在不增加物理存储单元数量的情况下增加存储比特数。每单元 4 比特的 QLC 于 2018 年问世，SK 海力士（SK Hynix）从 Intel 收购的 Solidigm 团队一直在宣传每单元 5 比特的 PLC 浮栅（Floating Gate）NAND。铠侠的研究人员甚至早在 2021 年就在低温条件下演示了每单元 7 比特。

然而，逻辑缩微的最大弊端是每个存储状态可用的电子数减少。增加每单元的电压状态数量，意味着分割每个存储单元的电子存储容量。每个状态的电子越少，变异性越大，可靠性被摧毁。2D NAND 在 TLC 技术上已经触及这一极限，3D NAND 也正迅速接近类似极限。展望未来，我们开始看到预示逻辑缩微终结的种种迹象。

![](https://substack-post-media.s3.amazonaws.com/public/images/a57819dc-5b4f-4610-b2b4-27c80c5234eb_959x737.png)

制造商发现，制造更小的单元（横向+纵向）且每个单元容纳更少的电子，使得每单元更高比特数难以为继。例如，Solidigm 的 192 层 PLC 已经失败，由于成本结构不佳，不会大规模量产。

三星 >236 层的 V9 代 3D NAND 同样显示 QLC 相比 TLC 的代际缩微效果更差。在 V7 代，QLC 比 TLC 密度高 40%；到了 V9 代，QLC 只比 TLC 密度高 20%。这是因为 QLC 存储单元无法像 TLC 单元那样大幅缩小。因此，美光和 SK 海力士认为 TLC（每单元 3 比特）NAND 将是长期最具成本效益的解决方案。

接下来是**垂直缩微（Vertical Scaling）**，这是过去十年密度提升的主要路径。目前高深宽比（HAR）刻蚀的深度极限是 6 到 7 微米，每个单元的最小厚度约为 40nm。到目前为止，制造商最多只能实现 128 层字线（Word Line）堆叠（每层约 50nm）。要突破这一点，就需要多台阶（deck）的 string stacking——分别刻蚀再上下组合。Solidigm 的 192 层设计使用 4 个 48 层的台阶，而海力士最新的 238 层一代使用 2 个台阶、每个有 119 条有源字线。

![](https://substack-post-media.s3.amazonaws.com/public/images/234af7bd-a9c2-4691-b994-a84ea971d091_1379x776.png)

理想情况下，台阶越少越好，因为需要重复的制造步骤更少，堆叠台阶时对准误差的风险也更低。除此之外，垂直缩微仅有的其他办法就是降低每个存储单元和字线的 Z 向厚度，或者提高 HAR 刻蚀深度（我们将在下文详述）。这就是东京电子（TEL）可能从 Lam Research 手中夺走大量业务的原因。我们后文将描述的沉积变革可能同样影响深远。

然后是传统的 X、Y 方向**横向缩微（Lateral Scaling）**。这可以通过提高存储沟道孔的密度，或减少 slit（开槽）与存储块细分的面积开销来实现。前者已经挖掘殆尽，因为要在孔侧壁上容纳所有叠层以形成电荷陷阱单元，孔无法再小多少。孔与孔的间距目前也已压缩到极致。

![](https://substack-post-media.s3.amazonaws.com/public/images/c10baa3e-91f2-4add-a580-5f80d83a5e3e_1852x702.png)

对于后者，美光和 WDC/铠侠正在增加 slit 之间的沟道孔数量，减少 slit 总数，从而用孔实现更好的面积利用率。这意味着他们的替换栅（replacement gate）工艺必须横向深入叠层更远，才能彻底去除所有 SiN 残留并干净地完成后续的钨（W）填充。

![](https://substack-post-media.s3.amazonaws.com/public/images/b970cdea-d6ba-4433-8c1b-4ced61dd73b3_916x631.png)

自 64 层一代以来，行业标准是 slit 之间 9 个 pillar（柱）。美光 232 层做到了 slit 之间 19 个柱，WDC/铠侠 BiCS6 162 层则做到 slit 之间 24 个柱，不过我们没有发现后者在市场上广泛量产。他们的 218 层 BiCS8 更进一步，不再需要一排 dummy 孔来分隔子块。

![](https://substack-post-media.s3.amazonaws.com/public/images/79f31ca3-aa52-4c89-9ef0-b84dc501a9d4_767x782.png)

虽然这些横向缩微技术带来的密度提升相比垂直缩微较小，但它能在不增加 WFE 强度的情况下实现线性成本下降。除此之外，横向缩微还可以通过采用交错式（staggered）阶梯设计，减少阵列两侧阶梯结构的面积开销。但代价是布线密度增加、字线连接区的复杂度上升。

![](https://substack-post-media.s3.amazonaws.com/public/images/6f1d9a03-8299-49d0-aa24-47bbab7fcefa_644x496.png)

最后是**架构缩微（Architectural Scaling）**，重点是 CMOS 逻辑外围电路的摆放位置。设计从简单的 CMOS 位于阵列旁边（CMOS Next to Array），发展到近年的 CMOS 位于阵列下方（CMOS Under Array），通过把电路建在 NAND 叠层下方来节省裸片面积。然而，由于 NAND 阵列工艺步骤的严苛特性，CMOS 逻辑制程技术存在限制。CMOS 键合阵列（CMOS Bonded Array，CBA）通过在单独晶圆上制造逻辑电路、再用混合键合将其与存储阵列晶圆键合来解决这一问题。

![](https://substack-post-media.s3.amazonaws.com/public/images/d7b3b2b0-510c-41d6-810c-a81393ccfadf_1157x899.png)

这使更先进的逻辑和更高的布线密度成为可能，从而实现阶梯和子块划分的进一步横向缩微。多晶圆键合带来的成本增加，可以通过逻辑与存储并行制造所带来的设计与工艺复杂度及周期时间的降低来抵消。长江存储（YMTC）凭借 64 层 Xtacking 1.0 及其惊人的 1.0 微米间距混合键合引领了这条路。WDC/铠侠的 BiCS8 218 层也将采用混合键合工艺，其他制造商纷纷跟进。

这些缩微路径大多已基本挖掘殆尽。垂直缩微一直是最主要的缩微方式，但即便是它，在当前制造设备下也开始触及天花板。

## **3D NAND 结构与制造流程**

首先在基础晶圆上沉积氧化物与氮化物薄膜交替叠层。每层厚度在 20 到 30nm 之间。单叠层的理论极限可超过 250 层、近乎 7 微米高。然后添加厚硬掩模，为高深宽比（HAR）沟道孔刻蚀做准备。这个反应离子刻蚀工艺挖出的孔阵，深度可达宽度的 70 倍。沟道孔的圆度均匀性以及整个孔深方向的均匀性，对降低存储单元性能变异性至关重要。对于采用多台阶设计的产品，这些步骤会重复执行，随后各台阶再相互堆叠。

![](https://substack-post-media.s3.amazonaws.com/public/images/ac54c91c-e8a5-4fc5-af00-e6c35306f41a_950x445.jpeg)

接着，向沟道孔中填充多层材料以形成电荷陷阱单元，每一层沉积在孔侧壁上，使孔逐渐变窄。接下来是金属替换栅工艺。刻蚀 slit 贯穿所有叠层形成沟槽，露出叠层侧面。这样可以进入并掏除氮化物层，随后通过 ALD 沉积阻挡层并进行钨字线填充。阵列侧面刻蚀出阶梯结构，使字线层暴露给垂直接触孔。

最后，在上方形成位线（Bit line）与金属互连，与已制造好的 CMOS 电路（包括字线驱动器及 NAND 接口的其他外围电路）相连。由此可见，3D NAND 的密度与性能缩微高度依赖 HAR 刻蚀和沉积能力。

![](https://substack-post-media.s3.amazonaws.com/public/images/877bd822-938c-446b-9d85-514a2cc86028_3600x1669.png)

如前所述，制造工艺中的主要限制是沟道孔的刻蚀。这就是为什么预计每 GB 的原始工艺时间（以及工艺成本）的缩微，将从我们观察到的历史趋势放缓。这也是本文的重点。

## **NAND 市场更新，投资者的海市蜃楼：绿洲比看起来更近吗？**

NAND 依然疲软，产能严重过剩。由于供过于求，行业晶圆投片的稼动率目前仅为 60% 左右。库存情况也十分庞大。这是自 1997 年以来我们见过的最严重的供需失衡。

现在，各大 NAND 厂商都在降低稼动率，试图削减库存、让市场恢复平衡。不过，技术转型所需的一些投资仍然必要。最大的 NAND 生产商三星（占市场 34%）在 NAND 工艺上落后了。其当前一代产品仍以 128 层为主，176 层 NAND 在产量中占比仍然很小。

这明显落后于已用上 >200 层制程节点的 SK 海力士和美光。三星正试图投入资金，在今年将其大部分产能过渡到 236 层。他们实际上是在很大一部分产能上跳过了一个节点。虽然他们对技术转型的投资会提振今年的 NAND WFE，但这只会推迟行业复苏，因为会有更多闲置产能来吸收走强的需求。一旦技术转型完成，他们又将向市场多投放 70% 的位元。三星想强制推动行业整合，这是一项从公司最高层贯彻下来的策略。

中国也救不了场。中国主要的 NAND 玩家长江存储（YMTC）已被切断设备采购。这项禁令有其道理，因为 NAND 是中国自主芯片努力中最成功的领域。[无可争辩的是，禁令之前 YMTC 曾是技术领导者](https://www.semianalysis.com/p/2022-nand-process-technology-comparison)。即便在下行周期，他们也持续向市场投入资本开支，不断扩大产能和能力。原本的预期是，这会在下行周期为供给提供缓冲。中国受到出口管制，意味着他们在下行周期再也无法支撑 WFE 支出。

我们认为，与 2023 年相比，2024 年 NAND 资本开支将更加紧缩。我们只预计到 2025 年才会出现强劲复苏，届时庞大的库存和低稼动率提供的缓冲将使 NAND 供需恢复平衡。长期看位元需求将继续增长，行业最终需要投资来满足这一需求。注意，这是非常可怜的市场增长。这一判断还假设了一定的 NAND 行业整合，我们将在下文讨论。

下面我们将分享我们对 2023 至 2025 年 NAND 晶圆厂设备支出的预测、Western Digital 与铠侠的未来、NAND 高深宽比刻蚀市场深度解析、3D DRAM 的可能性、沉积领域即将到来的重大材料变更，以及 Lam Research 向东京电子的潜在市场份额大转移——这可能代表着超过 $1B 的营收易手。

[团购订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
