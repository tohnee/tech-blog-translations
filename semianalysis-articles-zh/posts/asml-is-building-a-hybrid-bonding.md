---
title: "ASML 正在打造混合键合设备！"
title_en: "ASML Is Building a Hybrid Bonding Tool!"
date: 2026-10-15
source: https://newsletter.semianalysis.com/p/asml-is-building-a-hybrid-bonding
crawled: 2026-09-15
authors: ["Sherry Zhang", "Gerald Wong", "Steven Lee", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-10-16
---

# ASML 正在打造混合键合设备！

> 原文：[ASML Is Building a Hybrid Bonding Tool!](https://newsletter.semianalysis.com/p/asml-is-building-a-hybrid-bonding) · SemiAnalysis
> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

ASML 尚未官宣任何消息，但它的专利申请、一篇[新闻报道](https://www.thelec.net/news/articleView.html?idxno=5864)以及它自己的路线图都指向了这一结论。我们认为，它会从裸片到晶圆（die-to-wafer，D2W）混合键合（hybrid bonding，HB）设备入手。这种设备比晶圆到晶圆（W2W）更难造，但也正是 ASML 有机会建立优势的地方。我们把这一动作视为 ASML 垂直整合的自然延伸，而且它还应能强化 ASML 与客户的纽带。

本文将从专利文件出发，对这台设备的设计做端到端的拆解。它最独特的地方在于**在轨道上运行**。这改变了设备与裸片的移动方式：每颗裸片都坐在自己的承载座（holder）上依次经过各个工艺工位，各工位的加工机构则主动靠近裸片来完成加工。轨道上的独立梭车（shuttle）还能提高工位稼动率、节省重复配置的硬件，并支持异构集成。

我们认为，ASML 有望在混合键合的对准精度（alignment accuracy）与颗粒控制上**建立优势**。这两项因素正是决定键合良率的关键，而 ASML 在光刻领域恰好有解决同类问题的深厚积累。

尽管有这些优势，ASML **仍需解决一系列挑战**：前馈量测（feed-forward metrology）、裸片与晶圆的接触、对非键合类工位的改造（使其能加工轨道上的裸片），以及整个回路的洁净度保持。

我们预计，先进逻辑——D2W 已在此领域大规模量产——会最先采用 ASML 的 D2W HB 设备。这对 **Besi 是个坏消息**。Besi 如今的 HB 业务大多来自逻辑，且集中在台积电（TSMC）和英特尔（Intel）。ASML 与这两家的合作都已超过二十年，并在 9 月刚刚宣布了一项光掩模联合计划。如果后道工艺再出现类似动作，我们不会感到意外。Besi 在 HBM 方面的前景也在走弱：除了我们[预计](https://semianalysis.com/institutional/de-specced-out-of-a-job-d2w-hbm-hybrid-bonding-goes-from-when-to-if/) HBM 采用该技术的时间点将推迟到 2029 年或更晚之外，韩国挑战者们也正在追赶。

## **ASML 正在打造混合键合机**

我们在 2024 年对[混合键合](https://newsletter.semianalysis.com/p/hybrid-bonding-process-flow-advanced)做过深度解析，至今我们仍视其为 EUV 以来半导体制造领域最具变革性的创新。晶圆到晶圆（wafer-to-wafer，W2W）混合键合（HB）已在图像传感器和 3D NAND 中量产，下一家将是 DRAM 厂商。**裸片到晶圆（D2W）HB 的推进要慢得多**，因为业界仍缺乏能同时兼顾令人满意的对准精度和吞吐量的成熟设备（我们了解到，当前应用的吞吐量上限仅为每小时一片晶圆），这使得单颗裸片的成本居高不下。如今 D2W 只在逻辑领域大规模量产：AMD 自 2022 年起出货混合键合的 V-Cache；台积电的 SoIC 目前以约 6um 间距键合，目标在 2029 年前后达到 4.5um。市场原本预期 HBM 会从 2028 年起成为 D2W 上量的最大驱动力。但我们的看法不同：我们认为 [HBM 在 2029 年之前不会采用 D2W HB](https://semianalysis.com/institutional/de-specced-out-of-a-job-d2w-hbm-hybrid-bonding-goes-from-when-to-if/)，甚至可能永远都不会。

Besi 一直领跑 D2W，是唯一一家设备已进入大规模量产的供应商。其他所有厂商还在努力让第一台设备通过验证。但我们认为，**局面很快就会改变，因为 ASML 正在打造 D2W 混合键合设备。**管理层尚未宣布任何消息，但该公司在 2022 年 12 月到 2024 年 11 月之间提交了 27 个键合专利族，其中大多数与 D2W 相关；真实数量很可能更高，因为 2024 年 11 月之后的申请尚未公开。[The Elec](https://www.thelec.net/news/articleView.html?idxno=5864) 还在 3 月报道过，ASML 已与 Prodrive Technologies 和 VDL ETG 一起启动了混合键合机的架构设计。

在核心专利申请（[WO2025201788A1](https://patents.google.com/patent/WO2025201788A1/en)）中，ASML 绘制了它的键合流程如何运作。有意思的是，这套系统与传统 D2W 键合机毫无相似之处（传统机台的工作原理可参见[先进封装系列第 5 篇](https://newsletter.semianalysis.com/p/hybrid-bonding-process-flow-advanced)）。ASML 不是用键合头从已切割的晶圆上逐颗拾取再放置裸片，而是**让单颗裸片坐在独立承载座上沿轨道移动**（图 1）。每颗裸片依次经过检测、清洗、等离子体活化以及量测（形貌、调平与对准）工位，最后到达键合工位——在那里，卡盘把下方晶圆抬起去迎接裸片。下面几节我们会逐一拆解这套设计。

**图 1：ASML 基于轨道的 D2W 键合机，SemiAnalysis 标注并简化**

![](https://substack-post-media.s3.amazonaws.com/public/images/d065d224-aa2f-4e22-be62-f11210f775a7_2046x1308.png)
*来源：ASML；SemiAnalysis 晶圆制造设备模型*

**ASML 可能也在打造 W2W 混合键合设备。**根据仁荷大学（Inha University）的一项[专利分析](https://www.thelec.net/news/articleView.html?idxno=10055)，ASML 很可能在其 TWINSCAN 平台上构建 W2W HB 设备，依托的是其晶圆套刻精度。本文聚焦 D2W 机台，因为它更难造，也是 ASML 有望建立真正优势的地方。

## **……其垂直整合布局的一部分**

**我们认为，这是 ASML 垂直整合、拉近客户关系努力的延续。**ASML 在 2013 年为光源收购了 Cymer，2016 年为电子束检测收购了 HMI，2020 年为光学模块收购了 Berliner Glas。它还在 2025 年第三季度[交付](https://www.sec.gov/Archives/edgar/data/937966/000162828025045043/pressreleasequarterlyresul.htm)了第一款后道产品——XT:260 i 线封装光刻机。而最近，ASML 又宣布与[台积电](https://www.asml.com/en/news/press-releases/2026/tsmc-and-asml-announce-industry-transition-to-large-format-photomasks-for-high-na-euv)、[Intel Foundry](https://www.asml.com/en/news/press-releases/2026/intel-foundry-and-asml-collaborate-to-accelerate-industry-readiness-for-high-na-euv)和[三星（Samsung）](https://www.asml.com/en/news/press-releases/2026/samsung-electronics-and-asml-expand-collaboration-on-next-generation-semiconductor-manufacturing)开展联合计划，推动行业为 High NA EUV 从 6 英寸转向 12 英寸光掩模。

**打造键合机是顺理成章的下一步。**事实上，ASML 自己的路线图已经把键合放进了前道流程。它 2024 年投资者日列出了面向 NAND、DRAM 和逻辑的 W2W 与 D2W 混合键合（图 2）。而一份 [2024 年 7 月的专利申请](https://patents.google.com/patent/TW202607495A/en)展示了键合机与光刻机如何通过共享裸片位置数据协同工作。今天，光刻机在已键合晶圆上曝光之前，必须对每颗裸片做预对准和粗对准。在 ASML 的设计中，键合机本来就知道自己把每颗裸片放在了哪里，并把这个图（专利中的「坐标系」）交给光刻机，后者只需检查少数标记便可曝光。客户在键合晶圆上获得更快的曝光速度，ASML 则得以把键合机和光刻机成对销售。

**图 2：ASML 的前道 3D 集成版图**

![](https://substack-post-media.s3.amazonaws.com/public/images/d9161a19-850b-4e34-abab-d4de4d766fd5_1536x864.png)
*来源：ASML 投资者日，2024 年 11 月 14 日*

**我们预计先进逻辑会最先采用。**逻辑是 D2W HB 已大规模量产的领域，也是对准要求不断收紧的领域。台积电称套刻精度是 SoIC「始终最大的挑战」。随着其 HB 间距在 2029 年前从 6um 推进到 4.5um，放置精度的要求还会进一步收紧。ASML 在对准方面实力强劲（下文详述），因此这一优势应能帮助它先赢得逻辑客户。先进逻辑裸片也是最昂贵的芯片之列，逻辑客户买得起高端设备。我们预计 ASML 的定价会高于同行。

接下来三节，我们将讨论：（1）设备的轨道系统——这是它与市面上现有产品相比最不寻常之处；（2）ASML 在对准、颗粒控制与运动控制上的积累如何可能让它的 HB 设备更胜一筹；（3）ASML 或其供应链伙伴仍需解决哪些挑战才能造出可用的设备。让我们开始。

## **这台设备的独特之处**

这台设备最有意思的一点是它**在轨道上运行**。ASML 在[专利申请](https://patents.google.com/patent/WO2025201788A1/en)中把 SuperTrak CONVEYANCE（图 3）列为示例，因此我们假设它采用的就是这种轨道，我们的分析也基于该轨道公开发表的设计。

与传统键合机的根本区别在于裸片「住」在哪里。在 Besi 类设备中，裸片在别处完成预处理，键合头只在最终贴装时才把它拾起。**而在 ASML 的设计中，每颗裸片从离开载具那一刻起就坐在自己的承载座上，一直待到键合工位**。各工艺工位沿轨道布置：裸片停在一个工位前，该工位就地完成清洗、活化或量测，然后裸片继续前行。

**图 3：SuperTrak CONVEYANCE 轨道（HORIZON10 平台）**

![](https://substack-post-media.s3.amazonaws.com/public/images/f3cfbe97-fa51-4614-bfd6-e603d64f8bf8_1342x523.png)
*来源：公司官网*

**下面我们逐步过一遍流程**。为了便于说明，我们取专利附图并在图 4 中标注了每个工位。一只夹爪把裸片从载具上取下，放到一个空置的基板承载座 (206) 上，由后者载着它沿轨道 (202) 前行。裸片依次停靠检测、清洗、等离子体活化、形貌检测、调平、粗对准、位置调整与精对准工位（210 至 226）。每次停靠时裸片都留在自己的承载座上，由工位完成作业。请注意这里的一个反转：在专利中，是工位的传感器或加工头主动移动去够裸片，而不是像今天的流程那样把裸片送进设备里。完成这些步骤后，裸片抵达键合工位 (228)。

**这个键合工位值得细看**。首先要注意，最终贴装由承载座 (206) 和卡盘 (234) 完成，而非轨道：SuperTrak 的规格表显示梭车的重复精度约为 10um，与键合所需的 50nm 放置精度相去甚远。其次，放大图 4 右侧可以看到键合动作：卡盘把下方晶圆抬升到距裸片几十微米之内，承载座的执行器调整裸片位置，裸片被压到晶圆上完成键合，承载座随之释放。空出来的承载座接着开始下一轮循环。

**图 4：专利 WO2025201788A1 图 2（左）与图 6 侧视图（右），SemiAnalysis 标注**

![](https://substack-post-media.s3.amazonaws.com/public/images/494b8fba-1313-4368-99e8-6543930f76e0_2045x755.png)
*来源：ASML；SemiAnalysis 晶圆制造设备模型*

这套设计有三大好处：

第一，**独立梭车提高了每个工位的稼动率**。每道工序的工位数量可以按该工序的节拍时间（cycle time）设定：3 秒的清洗工序配三个工位，1.2 秒的键合工序配一个工位，这样每个工位都保持满负荷。专利对此有明确要求，即「让所有工艺工位同时工作」。

第二，只要设备腔体还有空间，增加产能的方式是加装一个工位，而不是添购第二台设备。这**节省了重复的硬件投入和预算**。

最后同样重要的是，这套设计适合**异构集成**：新的裸片类型只是一套新的软件配方，因此不同种类的小芯片（chiplet）可以共用一条产线。

话虽如此，轨道本身也带来了关于非键合工位以及整个回路洁净度的挑战。我们会在后文再回到这些话题。

## **ASML 如何可能建立优势**

在此之前，先看 ASML 能把哪些既有优势带进 HB 设备。

首先回顾一下，为什么**对准精度和洁净度在混合键合中如此重要**。正如我们此前[详述](https://newsletter.semianalysis.com/p/hybrid-bonding-process-flow-advanced)的，两片全厚度晶圆之间的[一颗 1um 颗粒](https://iopscience.iop.org/article/10.1149/2162-8777/ac7662)就能让直径约 10mm 的区域无法键合，形成缺陷键合（图 5）。因此颗粒控制对 HB 极其重要。对准之所以重要，原因有二：**放置精度**直接决定键合良率；**对准耗时**对 D2W 吞吐量的拖累远大于 W2W，因为它会随裸片数量成倍放大。正是这两道门槛，使混合键合几乎成了一道前道工序。

**图 5：混合键合中，一颗小颗粒造成空洞与接触开路**

![](https://substackcdn.com/image/fetch/$s_!_TqG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd3511d6d-3406-48a5-b818-80aca90d0a7c_902x232.png)
*来源：SemiAnalysis*

我们认为，凭借数十年在光刻中解决同样两个问题的经验，ASML 有能力双管齐下。

**在对准方面，我们认为 ASML 可以复用其晶圆对准传感器技术。**根据其[专利申请](https://patents.google.com/patent/TW202616420A/en)，键合系统在每颗裸片上放置一个微小的衍射光栅，并通过光栅散射的光来读取裸片位置。其原理与 [ORION](https://www.asml.com/en/company/stories/2021/fellow-simon-mathijssen-aligning-lithography-nanometer) 相同——ORION 是 2017 年以来每台新 TWINSCAN 都配备的晶圆对准传感器。ORION 的设计初衷就是读取被 CMP 和刻蚀倾侧或变形的标记（图 6），而键合裸片上的标记会经历与旁边铜焊盘相同的 CMP 与等离子体活化，因此也带有同样的不对称性。我们认为同一传感器家族可以直接服务于 D2W 键合机。

**图 6：一个对称与一个倾侧的对准标记。工艺步骤会让表观中心发生偏移；ORION 的多色读出正是为看穿这一点而设计**

![](https://substackcdn.com/image/fetch/$s_!NR0y!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff401c807-b2b1-4291-82e2-ba55679929dd_564x159.png)
*来源：ASML，《Aligning lithography to the nanometer》，2021 年 12 月*

**它的传感与运动控制能力，也为总对准误差预算留出了更大余量。**其 [NXT:2100i](https://www.asml.com/en/products/duv-lithography-systems/twinscan-nxt2100i) 单机套刻精度可保持在 0.9nm。ASML 还已能量测 W2W 键合晶圆的畸变，并据此修正下一层光刻，把键合后套刻精度从 40-60nm 降到 4nm 以下（图 7）。这些是光刻指标，不是键合结果，但它们意味着 ASML 的传感器与工件台误差比键合机所需的 50nm 低一个数量级以上。更高的工件台精度，为键合机误差预算中的其他因素——裸片在承载座上的偏移、热漂移以及接触过程中的移动——留出了更多空间。

**图 7：ASML 量测加光刻机修正，将键合后套刻精度做到 2.5-3.9nm**

![](https://substack-post-media.s3.amazonaws.com/public/images/fb6bca63-32fe-4237-9030-273f28a2d894_1536x825.png)
*来源：ASML 投资者日，2024 年 11 月 14 日*

Prodrive Technologies 和 VDL ETG [很可能](https://www.thelec.net/news/articleView.html?idxno=5864)会成为助力 ASML 键合机实现高速运动的零部件供应商。Prodrive 为 ASML 的 EUV 磁悬浮工件台制造直线电机与驱动器，还打造过 Hanwha Semitech 的 SHB2 Nano 键合机。VDL ETG 则为 ASML 制造机架与模块（图 8）。

**图 8：Prodrive 的直线电机（左）与 VDL ETG 的晶圆传送模块（右）**

![](https://substack-post-media.s3.amazonaws.com/public/images/e914a2f5-f1c4-4aa3-ac7e-af959781a38b_1212x495.png)
*来源：公司官网*

**在洁净度方面，ASML EUV 系统的要求比键合机更严苛。**很少有设备厂商像 ASML 这样长期在纳米尺度上与颗粒作战。EUV 光刻机在真空中移动光罩与晶圆，并把光罩颗粒增量控制在「[与 sub-10nm 节点光刻的量产要求兼容](https://doi.org/10.1117/12.2514874)」的水平。我们认为 ASML 也考虑到了键合表面：其[键合装置](https://patents.google.com/patent/WO2026098870A1/en)申请加入了一个清洗基板支撑件的工具，以及一个监测其平整度、颗粒负载与畸变的传感器。

话虽如此，键合机中的污染物与光刻机不同。大部分是裸片边缘的切割碎屑，以及落在新活化、亲水表面上的颗粒。我们期待在后续专利中看到 ASML 如何处理这些键合机特有污染物的更多细节。

付费墙后，我们将讨论 ASML 要造出可用设备仍需解决的挑战，以及它的设备将如何冲击 Besi 的业务前景。

## ASML 尚待解决的开放问题
