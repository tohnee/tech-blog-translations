---
title: "SMIC N+3 的金属间距比 Intel 18A 更小吗？"
title_en: "Is SMIC N+3's Metal Pitch Smaller than Intel 18A's?"
subtitle: "SMIC N+3 制程节点深度解析（对比 TSMC N6）、TechInsights 私募股权出售、SemiAnalysis 拆解工程与评估实验室（STEEL）、海思 Kirin 9030、工艺技术、图形化、单元架构"
date: 2026-06-14
source: https://newsletter.semianalysis.com/p/steel-smic-n3-teardown
crawled: 2026-09-15
authors: ["STEEL Team", "Afzal Ahmad", "Andrew Wagner", "Gerald Wong", "Wayne Ma", "Dylan Patel", "Daniel Sanchez", "Adith Shankar", "Allison Elliott", "Sarah Lawrence"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# SMIC N+3 的金属间距比 Intel 18A 更小吗？

> 原文：[Is SMIC N+3's Metal Pitch Smaller than Intel 18A's?](https://newsletter.semianalysis.com/p/steel-smic-n3-teardown) · SemiAnalysis
> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**SMIC N+3 制程节点深度解析（对比 TSMC N6）、TechInsights 私募股权出售、SemiAnalysis 拆解工程与评估实验室（STEEL）、海思 Kirin 9030、工艺技术、图形化、单元架构**

将近四年前，我们曾报道[中芯国际（SMIC）已开始出货 7 nm（N+1）芯片](https://newsletter.semianalysis.com/p/chinas-smic-is-shipping-7nm-foundry)。如今，SMIC 的第三代 7 nm 工艺（N+3）已在华为（Huawei）Kirin 9030 上出货，其**最小金属间距为 32.5 nm**，比英特尔（Intel）最新 Panther Lake CPU 所用 18A 工艺出货的 36 nm 最小金属间距紧了约 10%。

这个标题属实，但它是一个不完整的、刻意挑选的指标。N+3 通过激进的 DUV 多重图形化和设计-技术协同优化（DTCO）达到了台积电（TSMC）N6 的密度，但为此在复杂性、能效和工艺控制上付出了代价。

这一点以及更多发现来自我们的逆向工程与拆解，涵盖 SMIC 的 N+3 工艺技术、华为的封装、内存、架构以及其他令人兴奋的特性。过去一年半里，SemiAnalysis 一直在俄勒冈州建设一个业界领先的拆解实验室，具备分析全球最先进、最重要芯片的能力。我们在先进数据中心芯片拆解上已经产生营收，其中包括最近对某家 TSMC 大客户的 COUPE CPO 光引擎 + EIC 3D 堆叠的逆向工程。

这是 SemiAnalysis 拆解工程与评估实验室（SemiAnalysis Teardown Engineering & Evaluation Lab，简称 STEEL）的首份公开报告。该实验室正在大举扩张，我们很高兴将其公之于众。对 TechInsights 来说，这个时机有点尴尬：它由私募股权持有、目前正被挂牌出售，而数十年来它几乎没有遇到过任何可信的竞争对手。这导致 TechInsights 在资本开支（CAPEX）上投入不足。

尽管没有任何风投或私募股权入股、成立仅 6 年，SemiAnalysis 的营收已超过 TechInsights。由于我们没有外部投资人、由创始人主导，我们行动更快、建设更快，能够定期免费发布客户芯片拆解报告，同时为大客户聚焦数据中心领域。

以下是我们实验室的首张公开图像——海思（HiSilicon）Kirin 9030 Pro SoC：

![](https://substack-post-media.s3.amazonaws.com/public/images/47814a7b-f944-416a-bf5c-1e8167b782a8_6728x7872.webp)
*海思 Kirin 9030 裸片图标注。来源：SemiAnalysis*

本报告将详述我们对 Kirin 9030 的拆解，以及我们对 SMIC N+3——中国最先进制程——的研究发现。作为对比，我们还会展示对联发科（MediaTek）Helio G99 的拆解，该芯片采用 TSMC N6 工艺制造。通过这一对比，我们可以考察出口管制的影响——SMIC N+3 与 TSMC N6 是彼此可比的节点，但一个受到严格的出口管制，另一个则可以自由使用西方最先进的设备。

从中我们既能看到中国的进步，也能看到其制约。SMIC N+3 达到了 TSMC N6 级别的逻辑密度，但需要激进得多的 DUV 多重图形化，因此在工艺成熟度和成本上不及 N6。Kirin 9030 Pro 的性能与三年前的 Android 旗舰机相当，远远落后于苹果（Apple）、高通（Qualcomm）、联发科和三星（Samsung）当前的旗舰 SoC。能效差距则更大。

出口管制并没有阻止华为和 SMIC 出货先进芯片，但迫使其走上了一条不同的道路。没有 EUV，SMIC 只能更重地依赖 DUV 多重图形化、DTCO 以及日益复杂的集成。路线图仍会通过更紧的设计规则和背面供电继续向前推进，但每一步都会增加成本与工艺风险。华为的 τ 缩放定律与 LogicFolding（逻辑折叠）展示了另一条路径：堆叠有源逻辑，并通过先进封装和系统-技术协同优化（STCO）找回密度。

# 裸片图与版图布局

要理解 Kirin 9030，必须先了解华为的 SoC 历史。海思是华为的芯片设计部门，负责 Kirin 智能手机 SoC、鲲鹏（Kunpeng）服务器 CPU、昇腾（Ascend）AI 加速器以及交换机/路由器网络芯片。

在出口管制之前，华为是 TSMC 最大的客户之一——是 TSMC 首个 EUV 节点 N7+ 的唯一客户，也是与苹果并列的 N5 首批客户之一。这一切在 2020 年底结束。华为在其旗舰智能手机中改用高通 SoC，但出口管制使其只能使用仅支持 4G 的版本。

2023 年底，华为以 Kirin 9000s 重回自研芯片。它是 Kirin 9000 的后继产品，由 SMIC N+2 而非 TSMC N5 制造。随后几年，他们在同一 N+2 工艺上发布了 Kirin 9010 和 9020。这些芯片采用华为自研的 TaiShan CPU 核心和 Maleoon GPU。

我们没有亲自拆解过 Kirin 9020，因此前代裸片图来自 Kurnal。这些裸片图展示了华为如何分配其硅片预算：各功能模块位于何处，以及它们的面积与前代相比如何。

![](https://substack-post-media.s3.amazonaws.com/public/images/2e265e05-7e1c-477a-8e0b-26add4ec820d_6705x3936.webp)
*海思 Kirin 9020（左）与 Kirin 9030（右）裸片图标注。来源：Kurnal、SemiAnalysis*

首先，快速导读裸片上的主要模块。

![](https://substack-post-media.s3.amazonaws.com/public/images/da49aa7b-3f9b-4702-8ed8-1e78a0024622_2159x1210.png)
*Kirin 9030 Pro 与 Kirin 9020 模块参考图。来源：SemiAnalysis*

两代芯片的总裸片面积几乎相同，但 9030 对这块面积的使用更为激进。更密的工艺让华为得以在同样的占位里塞进一个额外的中核（middle core）、更多 GPU 和 NPU 核心，以及更大的缓存。

![](https://substack-post-media.s3.amazonaws.com/public/images/4088da8f-7d40-4f12-81ae-58e6e9d4ae68_1798x1194.png)
*Kirin 9030 Pro 与 Kirin 9020 版图布局对比分析。来源：Kurnal、SemiAnalysis*

相比之下，Helio G99 是一款小得多的低成本 SoC，面向入门智能手机而非旗舰设备。Kirin 9030 约 140 mm²，而 G99 仅约 29 mm²，大约为前者的五分之一。不过，其底层的 TSMC 工艺技术可直接作为分析 SMIC 工艺的基线。

![](https://substack-post-media.s3.amazonaws.com/public/images/ab0ac5e1-a5ee-4112-86b2-3b3174c46377_2620x1914.png)
*联发科 Helio G99 裸片图标注。来源：SemiAnalysis*

# 架构与 PPA

Kirin 9030 是一次渐进式升级，而非推倒重来的全新设计。其 CPU、GPU 和 NPU 核心延续了 9020 的家族，提升来自三个杠杆：SMIC N+2 到 N+3 的工艺跃迁、DTCO 与版图布局工作，以及渐进的微架构改进。面积是前两项最直观的体现，9030 在这方面扩展得不错。性能与能效才是更难的考验。华为的设计表现好于其节点本身的水平，但这颗芯片仍然落后——一方面 N+3 落后于先进制程节点，另一方面其核心虽然合格，但仍比最新设计落后几代。

![](https://substack-post-media.s3.amazonaws.com/public/images/bdea3412-f6d4-46db-92c6-898b36724988_2600x1284.png)
*Kirin 9020 TaiShan V123（左）与 Kirin 9030 TaiShan Prime（右）核心。来源：Kurnal、SemiAnalysis*

新的 Prime 核心是一次渐进升级。主要变化是频率从 2.5 GHz 提升 10% 至 2.75 GHz，以及 L2 缓存从 1 MiB 翻倍至 2 MiB。尽管缓存增加，核心面积仍缩小了 7.6%；若不计私有 L2 缓存，核心面积缩小了 21%。对于一个渐进式节点来说，这是很大的缩减幅度。

![](https://substack-post-media.s3.amazonaws.com/public/images/288dd999-69ba-4086-aaf2-91797ac88a0c_1751x930.png)
*Kirin 9020 TaiShan New V120（左）与 Kirin 9030 TaiShan Middle（右）核心。来源：Kurnal、SemiAnalysis*

与 Kirin 9020 中的 TaiShan New V120 核心相比，Kirin 9030 的中核在架构上几乎未变，但每个核心缩小了约 22%。这主要来自 N+2 到 N+3 的工艺迁移，其余应归功于版图布局。

视觉上最显著的变化是中核数量从 3 个增加到 4 个。大核簇（big cluster）的共享 L3 缓存也增加了 20%。这有助于在不牺牲太多面积的情况下提升多核性能。

![](https://substack-post-media.s3.amazonaws.com/public/images/5d01dad1-e862-4213-b19a-21d883630268_5867x3578.webp)
*Kirin 9020（左）与 Kirin 9030（右）大 CPU 簇。来源：Kurnal、SemiAnalysis*

尽管每个核心都在缩小，大 CPU 簇的总面积基本没有变化。单核节省出的面积被重新投入到一个额外的中核和更大的缓存上。

![](https://substack-post-media.s3.amazonaws.com/public/images/ea6038c8-022a-403c-9943-9ddccb48f9c1_1087x480.png)
*Kirin 9020（左）与 Kirin 9030（右）TaiShan Tiny 核心。来源：Kurnal、SemiAnalysis*

Tiny 核心的缩小幅度小于 Prime 核心（不计其 L2 缓存），也小于中核。这很可能是因为固定开销在小核心中占比更大。仅凭裸片图我们无法分辨出任何架构变化，但下文展示的每时钟性能与能效提升表明，这不仅仅是纯粹的工艺与版图缩放。面积缩减被共享 L2 缓存从 2 MiB 翻倍至 4 MiB 所抵消，使整个 Tiny CPU 簇的总面积略有增加。

面积是从裸片图上最容易看到的改进，但它只是 PPA（性能、功耗、面积）的一部分。对现代逻辑芯片而言，功耗和性能同样重要，甚至往往更重要。自 2000 年代中期 Dennard 缩放失效以来，电压和频率已无法与晶体管尺寸同步缩放，因此每个节点都必须更费力地争取性能和能效的提升。

![](https://substack-post-media.s3.amazonaws.com/public/images/e64ef1ef-b398-45b0-8b9b-8d3c0219e569_1817x1222.png)
*Kirin 9030 Pro CPU 核心性能对比。来源：Littertree66、SimpleTech、David Huang、SemiAnalysis*

最悬殊的对比并不是 Kirin 9020 对阵 Kirin 9030 Pro。苹果的能效核心对华为的 Prime 核心是碾压级的领先。苹果的低功耗核心在仅 1 W 功耗下提供高出 20% 的整数性能，而华为 Prime 核心的功耗为 4.5 W。N+3 追平了 TSMC N6，但 N6 已是数代之前的工艺。苹果和高通基于 N4 和 N3P 打造芯片，这两者更密、位于更好的电压-频率曲线上，赋予它们更大的晶体管预算和更高的每瓦性能。

9030 自身的核心确有进步。中核和 Tiny 核的每时钟整数性能较 9020 分别提升 17% 和 14%；浮点性能中核持平、Tiny 核提升 11%。Tiny 核是干净的改进：性能上升、功耗下降，整数能效提升 45%、浮点能效提升 24%。中核则喜忧参半：整数性能上升但功耗上升更快，整数能效下降 7%；较低的功耗则使浮点能效提升 16%。

在相同或更低频率下取得的每时钟性能提升属于微架构层面的进步，说明这些核心经过了调优，而不只是被缩小。两者的实测频率也都未能守住标称最高频率，指向热、功耗或稳定性方面的限制。按每时钟性能计，中核大约处于 Arm Cortex-A720 的水平，Tiny 核接近 Cortex-A520；绝对性能落后，是因为华为给它们定的频率低得多。

Prime 核心的每时钟性能大致相当于 Cortex-X2 的水平——那是一个 2021 年的设计。苹果 2020 年的 M1 Firestorm 核心在相近的 4.5 W 功耗下，每时钟性能仍高出 35%、绝对整数性能快 57%。当前的领先者领先得更多：苹果 M5 P-core 每时钟性能高出 60%、绝对性能快 2.7 倍，Arm C1 Ultra 每时钟性能高出 45%、绝对性能快 2 倍。

在每时钟性能上追平较早前的高端核心是一项货真价实的设计成就。华为无法追平的，是先进制程节点的电压-频率曲线和晶体管预算——它们让苹果、高通等公司能够在同样的面积里、以更低的电压运行，把更多的晶体管花在更宽的核心、更大的缓存和更深的缓冲上。

华为的 LogicFolding 路线图是一种应对之道：堆叠有源逻辑以找回密度并缩短信号路径。我们将在后文回到这个话题。

![](https://substack-post-media.s3.amazonaws.com/public/images/f40c0f31-3ea3-452f-9581-d274dddf3ba4_2330x1238.png)
*Kirin 9020（左）与 Kirin 9030（右）Maleoon GPU 计算单元。来源：Kurnal、SemiAnalysis*

GPU 计算单元（CU）的变化比 CPU 核心更显眼：算术逻辑单元（ALU）簇和整个 CU 的版图都变得更加偏长方形。即便加入了光线追踪支持，单个 CU 仍缩小了约 28%。

![](https://substack-post-media.s3.amazonaws.com/public/images/d5b49202-c085-4dd2-915a-7e59e7f27a85_7219x3104.webp)
*Kirin 9020 Maleoon 920（左）与 Kirin 9030 Maleoon 935（右）GPU 簇。来源：Kurnal、SemiAnalysis*

不过，这一缩小被 CU 数量从 4 个增至 6 个所抵消，而且 CU 之外的面积增长了 33%。总体而言，GPU 簇大了约 10%。

![](https://substack-post-media.s3.amazonaws.com/public/images/461fd7e6-4f84-4e66-a933-045d8e76b24b_2364x1222.png)
*Kirin 9030 Pro GPU 性能对比。来源：Notebookcheck、SemiAnalysis*

GPU 是华为进步最大的地方。Maleoon 935 无法与当前旗舰竞争，但相较 920 是一大步，达到了老旗舰的区间。在 3DMark 中，它的 Wild Life Extreme（WLE）成绩比 920 快 70%，Steel Nomad Light（SNL）快 79%；在频率高 11%、CU 多 50% 的配置下，理论提升约 67%，与 WLE 的实测大致吻合，而 SNL 的实测则超过了理论值。

它在 WLE 和 SNL 中略超 Snapdragon 8+ Gen 1，在 WLE 中略超 Dimensity 9200 和苹果 A16，但与更新的芯片差距仍然很大：Snapdragon 8 Elite Gen 5 和 Dimensity 9500 在 WLE 中快约 2.4–2.6 倍，在 SNL 中快约 3.2 倍。

Maleoon 935 是华为首款支持硬件加速光线追踪的 GPU；在光追项目中，它略超 Exynos 2200，与苹果 A16 相当，而当前旗舰最快领先 3.7 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/2e564ac6-1296-45ba-9dfb-d8c8a1fa7642_3337x2334.png)
*Kirin 9020（左）与 Kirin 9030（右）Ascend NPU。来源：Kurnal、SemiAnalysis*

神经网络处理单元（NPU）是所有模块中结构变化最大的：从 Kirin 9020 的一个 Lite 核心加一个 Tiny 核心，变为 Kirin 9030 的一个 Lite 核心加两个 Tiny 核心。两类核心的版图也都有显著变化。

这是华为 NPU 设计的一次回调。Kirin 9000 5G——其最后一颗采用 TSMC N5 的旗舰芯片——使用两个 Lite 核心加一个 Tiny 核心。SMIC N+2 上的一系列 SoC 改为一个 Lite 核心加一个 Tiny 核心，很可能是为了节省面积。到了 Kirin 9030，华为又转回更大的多核 NPU 簇，但增加的面积给了一个 Tiny 核心而非 Lite 核心。

*我们正在深入剖析市场上最先进的数据中心与 AI 硬件。想了解更多即将推出的内容，或委托定制拆解，请联系 [sales@semianalysis.com](mailto:sales@semianalysis.com)。有兴趣与我们一起同行、并认为自己能带来改变？请查看我们的[招聘页面](https://semianalysis.com/semianalysis-careers/)。*

在深入工艺栈之前，值得先把封装和内存从 SoC 本体中分离出来看。

# 内存

Kirin 9030 的 Pro 版本搭载 12 GB 三星 DRAM，由两个 4 层堆叠（每堆 4 颗裸片）构成。裸片被识别为 K4L2E165YD，这是一款 12 Gb LPDDR5X-9600 器件，采用三星 1a 节点制造——即继 1x、1y、1z 之后其第四代 10 nm 级 DRAM。1a 自 2022 年起已大规模出货，因此这是现役内存，而非旧节点库存。

我们拿到的 16 GB Pro Max 版本中，同时发现了长鑫存储（CXMT）与三星两种封装。CXMT 封装印字为 CXDD7JEDM，两个 4 层堆叠，封装于 2025 年第 45 周。由 X 射线计算机断层扫描（CT）推断的裸片尺寸与 CXMT G4 工艺已知的约 0.3 Gib/mm² 密度相符，大致相当于其他厂商的 1z 工艺。

![](https://substack-post-media.s3.amazonaws.com/public/images/6464fcf5-eadd-4258-903a-4097e70611d5_2410x1116.png)
*Kirin 9030 Pro 中的三星 K4L2E165YD DRAM。上：部分裸片（SEC 印字）与一个 4 层堆叠；下：两个 4 层堆叠的剖面。来源：SemiAnalysis*

# 封装

Kirin 9030 采用典型的集成叠层封装（iPoP）堆叠：内存封装中的多颗 DRAM 裸片位于有机材质重布线层（RDL）中介层之上，后者又位于 SoC 与封装基板之上。整个封装再通过球栅阵列（BGA）焊球安装到印刷电路板（PCB）上。

![](https://substack-post-media.s3.amazonaws.com/public/images/ea34731b-e4c9-4844-b51c-c93488f48e33_2100x1977.png)
*Kirin 9030 iPoP 封装堆叠。来源：SemiAnalysis*

内存封装基板是一片承载 LPDDR5X 堆叠的轻薄双马来酰亚胺三嗪（BT）积层板。SoC 上方的有机 RDL 中介层将 PoP 信号绕着裸片引出，并可能带有 dummy 散热铜柱。封装基板则是在 BT 核心上做较厚的味之素积层膜（ABF）积层，把倒装焊凸点扇出到 BGA 间距，并内嵌电源平面。

整个堆叠全部为有机材质。唯一的硅只有 SoC 和 LPDDR5X 裸片；没有硅中介层。全有机方案使封装的热膨胀系数（CTE）接近 PCB，减少了板级翘曲，也省掉了 SoC 带宽并不需要的硅中介层成本。

![](https://substack-post-media.s3.amazonaws.com/public/images/4e96a8bb-ddfc-4ada-b39f-151f610404e2_2400x1229.png)
*来自 Mate 80 Pro（左）与 Pro Max（右）的 Kirin 9030 Pro 封装。来源：SemiAnalysis*

在 iPoP 堆叠中，内存封装通过焊球阵列连接到有机 RDL 中介层。底部填充（underfill）填满焊球周围的间隙，增加刚性并保护焊点免受机械应力。Pro 与 Pro Max 版本在这方面有所不同，相关内容我们在付费墙后详述。

![](https://substack-post-media.s3.amazonaws.com/public/images/005fc7ab-0f3f-4628-922c-502ce738eeb4_625x295.jpeg)
*Mate 80 Pro 封装去除 DRAM 后的侧视剖面，可见 BGA 与底部填充。来源：SemiAnalysis*

# 工艺

裸片图与架构告诉我们华为如何分配硅片预算，工艺则告诉我们 SMIC 能制造什么。我们以 Helio G99 作为 TSMC N6 的工艺参照。SMIC N+3 与 TSMC N6 都是由上一代 7 nm 级节点演进而来。

我们对逻辑和存储区域做了定点 TEM 剖面，分别沿 fin-cut（fin 截面）与 gate-cut（栅极截面）两个方向成像。每张剖面的图注都标出了水平视场宽度（HFW），即成像区域的实际宽度。我们从晶体管 fin 开始，再逐层向上经过标准单元、局部互连和 SRAM。

SMIC 并没有超越英特尔或台积电。它用激进的 DUV 缩放和 DTCO 达到了 N6 级密度，但这一密度并未转化为相当的性能与能效，原因有二：与先进节点之间的代差，以及华为的核心设计。

## fin 形貌

FinFET 工艺中最重要的调控旋钮之一是 fin 形貌：单根 fin 的形状，以及电流从源极流向漏极所经过的沟道。理想的 fin 应高、窄且近乎垂直。更高的 fin 增大有效沟道宽度，更窄的 fin 通过减薄栅极所需控制的鳍体来改善静电控制。任何一项做过头，工艺都要付出代价：驱动电流变弱、fin 变脆、锥形（taper）、底部增宽（footing）以及线边缘变化，都会损害良率和器件一致性。

![](https://substack-post-media.s3.amazonaws.com/public/images/08df59cb-4fd8-4864-8f5b-d5afc78b6441_625x350.png)
*英特尔 FinFET 架构的演进。来源：Intel*

英特尔 22 nm、14 nm 和 10 nm 的 fin 剖面展示了 FinFET 节点随时间的改进。22 nm 的 fin 是第一代结构，相对短、宽且锥度明显。这种形状限制了电流密度，并降低了栅极控制沿 fin 高度方向的一致性。到了 14 nm 和 10 nm，英特尔把 fin 推得更高、更窄，同时让侧壁更垂直。这些改变并不是缩小器件，而是提高每根 fin 的有效沟道宽度并改善静电控制。代价是，更紧的间距下做更高的 fin，制造难度大得多。

![](https://substack-post-media.s3.amazonaws.com/public/images/b172748e-3067-41c5-84b0-a22cd771c424_2072x2004.png)
*Kirin 9030 TaiShan Prime（左）与 Helio G99 Cortex-A55（右），fin 形貌，fin-cut，HFW 321.4 nm。来源：SemiAnalysis*

现在，让我们把 TSMC N6 上的 Helio G99 与 SMIC N+3 上的 Kirin 9030 作个对比。两种工艺属于同一级别：N+3 的 fin 间距为 30-32 nm，我们 N6 剖面中为 34 nm。N6 的这个间距尤其有意思：N7 的 HD 库通常标注 33 nm fin 间距，而 N6 并没有直接缩小间距，其密度收益来自 DTCO 而非更紧的间距。34 nm 这一间距在我们采样区域内保持稳定，此处主要用作与 SMIC N+3 的对比，我们未做进一步深究。

要确定 N+3 的 fin 图形化方案，仅凭一个核心单元是不够的。CPU 核心显示出约 32 nm 的密集间距，而 N-P fin 对之间的间距在 78 nm 与 88 nm 之间交替。仅看逻辑区，这可能与 120 nm 和 110 nm 的双节距芯轴（mandrel）方案相符，但这是一条复杂且不寻常的路线。把具有更复杂重复单元的 8T SRAM 的间距与 CPU 核心的序列结合起来，我们就能更有把握地逆向推断出图形化步骤。

![](https://substack-post-media.s3.amazonaws.com/public/images/77ad36de-cdb1-4094-9c1f-9404dfeff899_4257x3193.png)
*基于 CPU 核心与 8T SRAM fin 图案推断的 SMIC N+3 fin 图形化集成方案。来源：SemiAnalysis*

由于逻辑与 SRAM 应共用同一基础网格，单一 CD（关键尺寸）芯轴光刻图形以 128 nm 间距经过 SAQP，即可产生覆盖整个裸片的约 32 nm 网格（128 nm/4），这与逻辑和 SRAM 单元中看到的间距序列相吻合。

在所采样的剖面中，N+3 的 fin 比 N6 更高、更窄、长宽比更大。实测 fin 长宽比 N+3 约为 9.5:1，N6 为 7.8:1。N+3 的顶部圆化也更少，估计半径约 2 nm，而 N6 为 2.8 nm。即使两种工艺的 fin 宽度不同，顶部圆化与 fin 宽度之比讲的也是同一个故事：N+3 为 0.37，N6 为 0.44。从几何角度看，这个比值越低越好；完美的矩形 fin 不会有任何顶部圆化损失。

这些是从少量切片中测得的个位数纳米级特征，因此绝对数值请视为近似值。重要的结论是相对差距：N+3 的 fin 始终比 N6 的更高、更窄、圆化更少。

*我们正在深入剖析市场上最先进的数据中心与 AI 硬件。想了解更多即将推出的内容，或委托定制拆解，请联系 [sales@semianalysis.com](mailto:sales@semianalysis.com)。有兴趣与我们一起同行、并认为自己能带来改变？请查看我们的[招聘页面](https://semianalysis.com/semianalysis-careers/)。*

## 标准单元

标准单元是芯片版图的基本构建模块：一行固定高度，配对一颗 NMOS 和一颗 PMOS 晶体管并共享栅极，按网格平铺即构成逻辑块。其关键尺寸是接触式栅极间距（CGP）、单元高度（CH）、fin 数量以及低层金属布线网格。

测量密度时，我们采用 Bohr 指标：NAND2 门面积（权重 60%）与扫描触发器面积（权重 40%）的加权平均。这代表了组合逻辑与时序逻辑的现实混合。该指标有其局限，尤其是对 TSMC FinFLEX 这类在不同 fin 数单元间交替的复杂单元版图。即便如此，它仍是纯粹工艺层面对比的最佳指标。

另一个重要测量是 fin 间距，指同一颗晶体管两根 fin 之间的距离。在 FinFET 工艺中，每颗晶体管使用多根 fin 来提高驱动电流，进而提升性能。

TSMC N6 同时提供每单元 2 PMOS + 2 NMOS fin 的高密度（HD）库和各 3 fin 的高性能（HP）库。共享栅极下更多的 fin 意味着更大的有效沟道宽度。HP 单元开关驱动更强，但以面积为代价。设计者会在裸片上混用两者，主要把 HP 单元用在时序关键路径上，以匹配其 PPA 目标。

![](https://substack-post-media.s3.amazonaws.com/public/images/572e2f16-8440-432f-b6c1-fcff9a78d3ff_1040x1070.png)
*Helio G99 Cortex-A55 标准单元，fin-cut（TSMC N6 HD），HFW 562.5 nm。来源：SemiAnalysis*

在 Helio G99 的 Cortex-A55 核心中，我们测得 HD 单元的单元高度为 240 nm。联发科在 G99 中使用 HD 单元，以最小化裸片面积从而降低成本。对于一颗面向约 100 美元入门智能手机的 SoC，这是必须的。

相比之下，我们在 Kirin 9030 中只找到一种库：2 NMOS + 2 PMOS fin。这说明其库策略比广泛使用 HD 和 HP 双库的 TSMC N6 更窄。这可能反映了其更小的客户群体，以及[受到更多制约的国内设计与电子设计自动化（EDA）生态系统](https://newsletter.semianalysis.com/p/eda-market-primer)。

![](https://substack-post-media.s3.amazonaws.com/public/images/086f7333-95c1-41d2-86b0-3989f1d9faaf_3104x1524.png)
*Kirin 9030 TaiShan Prime（左）、Middle（中）与 Tiny（右）标准单元，fin-cut（SMIC N+3），HFW 562.5 nm。来源：SemiAnalysis*

在 Kirin 9030 的全部三种 CPU 核心中，我们测得单元高度均为 228 nm，比 N6 小 5%，也比 SMIC N+2 的 252 nm 单元高度缩减 9.5%。

![](https://substack-post-media.s3.amazonaws.com/public/images/6e77c6d8-5136-45cc-a0bf-ade11970c445_2072x2072.png)
*Kirin 9030 TaiShan Prime（左）与 Helio G99 Cortex-A55（右）栅极形貌，gate-cut，HFW 321.4 nm。来源：SemiAnalysis*

SMIC N+3 与 TSMC N6 的 HD 库 CGP 均为 57 nm。对 SMIC 而言，这是在 N+2 基础上缩减 9.5%。

过去，仅凭 CGP 和单元高度或许足以比较晶体管密度。如今，我们还必须考虑缩放助推器（scaling booster）与 DTCO。SMIC 的密度收益不来自 EUV，而是来自对每一种可用 DTCO 助推器的激进使用。

第一项是 fin 减配（fin depopulation）：减少每个单元中 NMOS 和 PMOS 的 fin 数量。最早的 FinFET 节点以每颗晶体管 3 或 4 根 fin 起步。SMIC N+3 与 TSMC N6 HD 都只给每颗晶体管 2 根 fin，以驱动强度换取密度。

第二项是活性栅极上接触（COAG）。让栅极接触直接落在活性栅极正上方，而不是延伸到隔离区上方，单元高度随之下降。N+3 集成了 COAG，而 N6 没有。我们的 N+3 gate-cut 剖面显示栅极接触位于活性区上方，即采用了 COAG；N6 则显示接触落在栅极之外。

第三项是单扩散切断（SDB）。扩散切断（diffusion break）插在同一行的单元之间以提供电学隔离，但也会引入局部版图效应（LLE）——电学特性随版图发生的偏移。过去使用双扩散切断，占用两个 CGP 的空间。SMIC N+3 与 TSMC N6 改用 SDB，节省了面积，却提高了对 LLE 的敏感性。这必须在工艺层面加以控制，并在工艺设计套件（PDK）中精确建模，EDA 工具才能将其计入。

综合来看，SMIC N+3 的晶体管密度为 113.4 MTr/mm²，略高于 TSMC N6 的 107.7 MTr/mm²。即使没有 EUV，SMIC 也实现了超越台积电使用 EUV 的成熟节点 N6 的密度。

## 金属堆叠

本次拆解中最小的关键尺寸是 M0：SMIC N+3 的局部金属间距为 32.5 nm，比 Panther Lake 中 Intel 18A 的 36 nm M0 间距更小。但这并不意味着 SMIC 拥有比 Intel 18A 或 TSMC N3P 更好的工艺。M0 是单元内部的局部布线层，其实际价值取决于整个互连堆叠：M1 与 M2 间距、轨道数、通孔与导线电阻、设计规则、掩模数量、套刻控制以及布线灵活性。

32.5 nm 的 M0 与自对准四重图形化（SAQP）相符，其四组线宽分布我们粗略读出为 21.5 至 24 nm 交替的宽度；M1 与 M2 分别为 38 nm 和 40 nm，与自对准双重图形化（SADP）——单次 A/B 拆分——相符。在 TSMC N6 上，M0、M2 和 M3 处于宽松的约 40 nm，与 SADP 级双重图形化一致，无需四重图形化。话虽如此，例如我们实测 M2 约为 43 nm，可能因布线稀疏而偏大。我们不会根据剖面对任何特定层做出是否使用 EUV 的判定；我们能区分的是双重还是四重图形化，而不是光刻波长。

前道工序（FEOL）的晶体管级密度设定了上限，但设计最终受限于互连堆叠能布通什么。最低几层金属对标准单元密度最重要，而半全局与全局层则决定了这种密度在模块级和芯片级的可用程度。

![](https://substack-post-media.s3.amazonaws.com/public/images/c12e16af-23cb-4ea4-9f47-4fb2fb839c27_2072x1432.png)
*Kirin 9030 TaiShan Prime（左）与 Helio G99 Cortex-A55（右）低层金属，fin-cut，HFW 562.5 nm。来源：SemiAnalysis*

芯片剖面通常使用两个方向：fin-cut 与 gate-cut。上图是 fin-cut，展示了 M0 至 M3。这个方向能让我们看到偶数层金属，M0 紧贴 fin 之上。

M0 导线有两类。第一类是电源轨：在每个标准单元上下边缘水平走线的 VDD 与 VSS 宽导线。宽导线实测 55 nm，是其他 M0 导线的两倍多。其宽度将电阻降至最低并减小 IR 压降。第二类是单元内导线：单元内把端子连接到 M1 的短线段，宽度在 21.5 至 24 nm 之间交替。

M0 间距为 32.5 nm，较 N+2 和 N6 缩减 19%。在这样的间距下，DUV 图形化需要更激进的多重图形化，掩模数量、套刻敏感性、工艺复杂度和成本都会随之上升。

M0 已低于单次 DUV 定义的间隔件工艺（SADP）所能解析的极限，因此 SMIC 级联了第二个间隔件步骤（SAQP）。剖面反映了这一代价：与同一颗芯片上的 M1 或 M2 相比，M0 沟槽明显更内收（底部比顶部更窄），并在沟槽与刻蚀停止层交界处带有富阻挡层的亮脚。这种形状一部分是刻意的大马士革剖面——稍窄的底部有助于铜的无空洞填充——但它在 M0 上的幅度是由紧凑间距和更高的沟槽长宽比造成的。

![](https://substack-post-media.s3.amazonaws.com/public/images/9bdf9cbd-902e-4930-b353-059f27eae8e7_5461x1642.png)
*自对准双重（SADP）与四重（SAQP）图形化的简化对比。来源：SemiAnalysis*

Intel 18A 支持 32 nm 的 M0 间距，不过 Panther Lake 实际出货只用了更宽松的 36 nm 间距。这是因为英特尔大量使用 HP 库。在先进节点中，18A 的 M0 间距最宽松，原因在于 PowerVia：供电走线移到背面后，拥塞减少，整个正面金属堆叠都可用来走信号。

M2 是第一个真正的单元间布线层。它与 M0 一样水平走线，但跨越多个单元以承载模块级信号。M2 间距决定了单元的轨道高度——即 VDD 与 VSS 电源轨之间能容纳多少条 M2 轨道，也就是库中所说的 6 轨道或 7.5 轨道单元。这一层最重要，它限制着整个模块的布线。

SMIC N+3 采用 5.7 轨道单元。M2 间距为 40 nm，较 N+2 缩小 5%，与 N6 持平。这一缩减使间距仍停留在双重图形化可行的边缘。未来的节点将需要为 M2 增加掩模数量，因为受布线限制，进一步减少轨道数要困难得多。

![](https://substack-post-media.s3.amazonaws.com/public/images/3d9f47f5-7311-43ac-b66a-94545fcb3e72_2072x1668.png)
*Kirin 9030 TaiShan Prime（左）与 Helio G99 Cortex-A55（右）低层金属，gate-cut，HFW 562.5 nm。来源：SemiAnalysis*

上图是与之垂直的方向，即 gate-cut，展示了 M0 至 M4。这使我们能够观察并测量奇数层的垂直金属层。

M1 间距为 38 nm，比 N+2 小 9.5%，比 N6 小 33%。M1 与栅极的线数比很重要，因为它决定了局部布线灵活性。N+2 与 N+3 采用 3:2，N6 采用 1:1，这解释了 M1 间距的巨大差异。M1 走线相对栅极越多，单元内电源与信号交叉的灵活性就越高。布线灵活性带来更复杂、更优秀的单元。人们也偏好整洁的分数比，因为网格具有周期性，能改善版图。3:2 让 SMIC 获得比严格 1:1 网格更多的局部布线灵活性，但也使版图与图形化更复杂。这是一个 DTCO 选择：SMIC 在没有 EUV 的情况下，以增加工艺复杂度为代价找回密度与可布线性。

3:2 比例在先进节点中并不流行。台积电只在 N7+、N5 家族和短命的 N3(B) 上用过，N3E 已改回 1:1。英特尔只在 10 nm/Intel 7 家族上用过，Intel 4、3 和 18A 全部采用 1:1。三星是先进制程中唯一仍在用 3:2 的厂商，用于 SF4 和 SF3 家族。SMIC 未来节点是继续 3:2 还是转向 1:1，仍有待观察。

业界仍在积极探索这些局部布线比例。在 VLSI 2026 上，imec 将发表关于更高比例的研究，包括一种最多可减少 14% 面积的 2:1 方案。我们将在未来的新闻通讯文章中报道这次会议。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

*我们正在深入剖析市场上最先进的数据中心与 AI 硬件。想了解更多即将推出的内容，或委托定制拆解，请联系 [sales@semianalysis.com](mailto:sales@semianalysis.com)。有兴趣与我们一起同行、并认为自己能带来改变？请查看我们的[招聘页面](https://semianalysis.com/semianalysis-careers/)。*

N+3 的最后一层局部互连是 M3，间距 44 nm。M3 间距与 N+2 相同，比 N6 大 10%。

![](https://substack-post-media.s3.amazonaws.com/public/images/558118d6-dffb-402b-b9c1-7619f9ed69a0_1571x1870.png)
*Kirin 9030 Middle（左）与 Helio G99 Cortex-A55（右）金属堆叠，fin-cut，HFW 4.59 µm（Kirin 9030）与 3.91 µm（Helio G99）。来源：SemiAnalysis*

半全局层承载了模块级信号布线的大头。它们的间距比低层局部层更粗。在先进节点上，它们被设计在 DUV 单次图形化的极限上。

M4 至 M11 的间距测得分为三档：80–82 nm（M4–M6）、128 nm（M7–M10）和 148 nm（M11）。鉴于采样有限，在布线密集区域它们有可能进一步细分。最顶部是两层巨型金属 M12 和 M13，间距与 N+2 相同，分别为 1920 nm 和 4600 nm。

![](https://substack-post-media.s3.amazonaws.com/public/images/7afc719e-806d-400f-bcbb-e40df1ee6fa0_1142x1180.png)
*Kirin 9030 与 Helio G99 金属堆叠间距汇总。来源：SemiAnalysis*

低层金属的间距通常由工艺和库决定，而高层金属的间距与层数则因设计而差异很大。即使两颗同工艺的智能手机 SoC，金属堆叠也可能截然不同。Helio G99 的布线层数较少，到 M9 就达到 850 nm 的粗间距；而更大、性能更高的 Kirin 9030 直到 M11 仍保持精细间距。

## SRAM

在先进制程上，SRAM 的微缩远比逻辑困难。台积电最新节点的位单元几乎没有缩放，而逻辑仍有许多 DTCO 杠杆可用。

在 GPU 计算单元中寻找其他逻辑库时，我们偶然发现了这批 SRAM。最常见的 SRAM 由 6 颗晶体管（6T）构成，但这个单元却有 8 颗晶体管（8T）。

8T SRAM 增加两颗晶体管构成专用读端口。6T 单元在读取时会扰动存储内容，而解耦的读端口消除了读扰动，改善了读稳定性，也让单元可以在性能上压得更狠。

![](https://substack-post-media.s3.amazonaws.com/public/images/c096bd39-b76b-4111-87c8-aa5b512dff19_864x578.png)
*Kirin 9030 8T SRAM，fin-cut，HFW 1.55 µm。来源：SemiAnalysis*

乍看之下，这个切片像是一个不寻常的逻辑库：每个单元行有 3 根一种极性的 fin 和 5 根另一种极性的 fin，而且行的方向还交替变化。

能量色散 X 射线光谱（EDS）解开了我们的疑惑。切片并没有落在 GPU 逻辑上，而是落在了旁边的 SRAM 宏上。不寻常的 fin 图案正是 SRAM 库所致。我们会在付费墙后的工艺流程分析中再回到 EDS。

SRAM 库与传统逻辑库不同。由于 PMOS 与 NMOS 晶体管数量不等，它们需要专门的规则和版图库。它们不需要逻辑库那样的灵活性，因此朝着唯一的目标极度优化：高密度、高可靠的存储。

![](https://substack-post-media.s3.amazonaws.com/public/images/0d11d860-92f3-4300-901a-0141f1b4001a_2072x657.png)
*Kirin 9030 8T SRAM，fin-cut，HFW 562.5 nm。来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/42cbac4f-df67-4d92-84fb-3b5d00d66d1d_4188x1326.png)
*从左至右：6T HDC（1:1:1）、6T HCC（1:2:2）与 8T HCC（1:2:2-2:2）位单元电路图。来源：SemiAnalysis*

我们发现的 SRAM 单元是 1:2:2-2:2 单元。也就是说，每颗上拉（PU）PMOS 晶体管 1 根 fin，每颗下拉（PD）和传输门（PG）NMOS 晶体管各 2 根 fin。这 2 颗 PU、2 颗 PD 和 2 颗 PG 晶体管通常构成一个 6T 高电流单元（HCC）。8T HCC 再增加读下拉（RPD）和读传输门（RPG）两颗 NMOS 晶体管，各带两根 fin。

![](https://substack-post-media.s3.amazonaws.com/public/images/82ed6252-d184-46ec-893b-7e9715ecfb70_1689x594.png)
*SMIC N+3 SRAM 位单元对比。来源：SemiAnalysis*

我们测得单元高度为 406 nm，对应位单元面积 0.0463 µm²，理论峰值密度 21.6 Mib/mm²。我们估计 6T HCC 的单元高度为 292 nm、面积 0.0337 µm²，比 Intel 3 和 Intel 4 上的 6T HCC 大约 12%。

我们还估计 6T 高密度单元（HDC）的单元高度为 228 nm、面积 0.0260 µm²——恰好与前文测得的逻辑标准单元高度相同。这一估计将该单元置于三星 7LPP/5LPP 附近、略低于 TSMC N7/N6，对应理论峰值密度 38.5 Mib/mm²。6T HDC 可以说是最重要的单元，因为它用于芯片中最大的缓存——L3 缓存和系统级缓存（SLC）。

![](https://substack-post-media.s3.amazonaws.com/public/images/8569b0bf-eacb-4927-8737-7609ea9c4d73_995x1130.png)
*Kirin 9020（左）与 Kirin 9030（右）SLC 体（bank）。来源：Kurnal、SemiAnalysis*

Kirin 9020 与 9030 都把 SLC 分成 4 个体以提高总 SLC 带宽。在 Kirin 9030 中，SLC 从每体 2 MiB 增至 3 MiB；相应地，体内阵列数量也增加了 50%，从 16 个增至 24 个。每个阵列可存储 128 KiB，在裸片图上排列成规整的图案。

从 Kirin 9020 到 Kirin 9030，128 KiB SLC 阵列的面积从 0.0477 mm² 降至 0.0392 mm²，缩减 18%。实际达到的密度为 25.5 Mib/mm²，是理论最大值的 66%。

![](https://substack-post-media.s3.amazonaws.com/public/images/ab089b55-6e9f-46b1-9e4e-8abfc62c5ac3_1768x660.png)
*Kirin 9020（左）与 Kirin 9030（右）大 CPU 簇 L3 缓存体。来源：Kurnal、SemiAnalysis*

两颗芯片的 SLC 相当接近，L3 则发生了重大变化，尤其是在版图上。总容量也从 10 MiB 提升到 12 MiB。与 SLC 一样，L3 也分为 4 个体。

在 Kirin 9020 中，一个 L3 体由 16 个 128 KiB 阵列加 16 个 32 KiB 阵列组成；而 Kirin 9030 的一个 L3 体改为由 48 个 64 KiB 阵列组成。

在 Kirin 9020 的 L3 中，128 KiB 阵列为 0.0513 mm²，32 KiB 阵列为 0.0154 mm²。128 KiB 阵列在 L3 与 SLC 上的尺寸不同，因为两类阵列的辅助电路随用途而异。

在 Kirin 9030 的 L3 中，64 KiB 阵列为 0.0210 mm²。虽然不是同尺寸的直接对比，但按容量归一化后，它比 9020 的 128 KiB L3 阵列小 18%，比其 32 KiB L3 阵列小 31%。实际密度略低于 SLC，为 23.8 Mib/mm²，是理论最大值的 62%。

![](https://substack-post-media.s3.amazonaws.com/public/images/3f13742f-ff34-408e-a53c-624fe723617e_1318x1205.png)
*Kirin 9020（左）与 Kirin 9030（右）Prime 核心私有 L2 缓存。来源：Kurnal、SemiAnalysis*

与 L3 和 SLC 不同，Prime 核心的私有 L2 缓存采用 2 体的设计。由于 Prime 核心的 L2 对延迟敏感，它很可能使用 6T HCC 而非 6T HDC。9020 每体有 16 个阵列，9030 有 32 个。每个阵列容量为 32 KiB。

L2 中的 32 KiB 阵列从 0.0171 mm² 缩小到 0.0142 mm²，小了约 17%。密度为 17.6 Mib/mm²，约为 6T HCC 理论最大值的 59%。

从 N+2 到 N+3，SRAM 缩放得不错，缩减约 19%，接近逻辑的理论缩减幅度。但要注意，N+2 的位单元异常偏大，超过可比的 7 nm 级节点，因此这部分收益属于补课，而非真正的微缩。

借助 STEEL 拆解获得的洞见，我们将在未来的新闻通讯文章中对 SRAM 做深度解析。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

*以上所有内容都出自 STEEL 的一次拆解：裸片图标注、模块级面积分析，以及贯穿逻辑与 SRAM 的 TEM 剖面。我们正在深入剖析市场上最先进的数据中心与 AI 硬件。想了解更多即将推出的内容，或委托定制拆解，请联系 [sales@semianalysis.com](mailto:sales@semianalysis.com)。*

## 未来路线图

确定 N+3 特性的那些剖面，同样揭示了 SMIC 下一步可以走向哪里。尽管 N+3 在若干层上已接近 DUV 多重图形化的实际极限，SMIC 手中仍握有几个微缩杠杆。

理论上的 N+4 很可能从单元高度入手。N+3 在电源轨之间使用 5 条 M0 轨道。改为 4 条 M0 轨道（如 SMIC N+2 和 TSMC N6 那样），单元高度可缩减约 15%。布线网格只是缩减的一方面；前端也必须塞进更小的单元。

![](https://substack-post-media.s3.amazonaws.com/public/images/88dba4ae-a5d6-4c26-856a-168be8c33d42_2000x1125.png)
*Intel 4 单扩散网格（Single Diffusion Grid）与缩小的多晶硅端到端间距。来源：Intel、VLSI 2022*

一个可能的 FEOL 杠杆是把 p 型与 n 型之间的隔离间距从两个扩散网格单元缩减到一个。英特尔在 Intel 4 上用过这一缩放助推器，台积电则在 N3 家族上使用。这条路径以版图灵活性换密度。M0 轨道更少会削减局部布线资源，而更紧的 p-to-n 间距则加大集成与设计规则的难度。

M2 同样受单元高度缩减的约束。SMIC 若要维持约 5.7 轨道单元，M2 需向约 35 nm 推进，这将把又一层推入 SAQP 的领地。

SMIC 还可以把 CGP 从 57 nm 降到 54 nm。英特尔在 Intel 10 nm/Intel 7 上没有 EUV 也达到了相近的 CGP。局部互连则更棘手。如果 SMIC 保持 3:2 的 M1 与栅极线数比，M1 需要缩到 36 nm，并且很可能同样需要 SAQP。如果改用 1:1，M1 可以放宽到 54 nm，但会牺牲布线灵活性。

在这条理论路径下，我们估计 SMIC N+4 可以达到 198 nm 的单元高度和 54 nm 的 CGP，对应 137.8 MTr/mm² 的 Bohr 密度，与 TSMC N5 或三星 SF4 相当。但难度是累积的。每一步单独看都可行，但合在一起使 N+4 比 N+2 到 N+3 的过渡更难。它很可能耗时更久、成本更高、工艺余量更小。

![](https://substack-post-media.s3.amazonaws.com/public/images/3b7e071e-cea6-4fb7-aec4-caf601dc7b46_1293x729.png)
*实现背面供电的埋入式电源轨与背面接触方案。来源：UC San Diego、ISPD 2026*

理论上的 N+5 则需要更大的集成范式转变。一条可能的路径是[背面接触（BSCon）](https://newsletter.semianalysis.com/i/174558465/direct-backside-contacts)：把供电走线和源/漏接触移到芯片背面，从而减轻正面布线压力，并让单元高度再降一步。

正面金属间距可以放宽以降低工艺复杂度。M0 可能小幅放宽到约 34 nm，M2 与 M4 间距可以进一步放宽。CGP 则不太可能再缩多少——即使有 EUV，48 nm 也一直是良率与工艺控制的实际上限。

这一方案可使 N+5 的单元高度降至 170 nm、CGP 降至 53 nm，对应 163.6 MTr/mm² 的 Bohr 密度，与 Intel 18A 的 HP 库相当。但这并不会让 N+5 在成本上具备与先进制程竞争的资格——它是通过一条昂贵得多的路线达到相近密度的。集成难度急剧上升，需要为背面套刻对准、晶圆减薄、接触点露出（contact reveal）和背面金属化引入全新的工艺流程。

越过这一点之后，常规的密度与互连微缩越来越不划算。也正是在这里，华为的路线图开始不再像一份普通的代工厂路线图，而更像一份封装路线图。

# 华为的 τ 缩放定律

在 ISCAS 2026 上，华为发布了其 tau（τ）缩放定律，把工艺缩放重新放到时间域中表述。τ 是数据搬运与处理的时延成本：晶体管的开关延迟、电路中的 RC 信号传播延迟、计算、内存与网络时延。抛开华为的术语，这就是所谓的[系统-技术协同优化](https://newsletter.semianalysis.com/i/190867437/stco-co-optimizing-the-entire-system)。

这是华为对缺少 EUV 光刻的回应。没有 EUV，平面密度无法跟上台积电、英特尔或三星。既然晶体管密度无法继续缩小，华为的替代方案就是缩短导线、减少缓冲、垂直堆叠逻辑。

"LogicFolding"（逻辑折叠）是华为对这一新缩放理念的实现，实质上是一种激进的 3D 堆叠方法。AMD V-Cache 把 SRAM 放在 CPU 裸片的上方或下方；AMD 的 MI350X 把有源中介层裸片（AID）放在加速与计算裸片（XCD）之下，由 AID 承担缓存、IO 接口、片上网络（NoC）和嵌入式金属-绝缘体-金属（MIM）电容。而 LogicFolding 是把同一个逻辑块的一部分拆分到多颗以超细间距面对面键合的有源裸片上。这使华为得以缩短某些关键路径并减少缓冲开销，而不只是增加缓存容量或卸载 IO 与互连。

更高的时钟频率正来自导线的缩短。现代核心的延迟与能耗预算中，很大一部分花在驱动长互连及其沿线的中继缓冲器上。LogicFolding 把一个模块的关键路径门电路分布到以极细间距键合的多个堆叠层上，使键合界面表现得像额外的一层金属，最长的路径因此变短。华为正是指望借此找回单靠工艺无法获得的频率与能效。

![](https://substack-post-media.s3.amazonaws.com/public/images/6e5103b2-05ed-4159-a09e-0d755c9f045b_2042x1229.png)
*华为 Prime 核心频率路线图。来源：Huawei、SemiAnalysis*

华为的路线图表明了其意图。Prime 核心频率目标是从 Kirin 9030 的 2.75 GHz 提升到 2031 年的约 5 GHz，远超单纯平面缩放所能达到的水平。3.1 GHz 和 3.39 GHz 时钟的 Prime 核心已在其实验室中测试，尽管功耗未知。再往后，芯片尚处于设计、仿真或路径探索（pathfinding）阶段，这意味着那些频率只是目标。不过方向更重要：LogicFolding 帮助的不只是密度，还有性能。

问题在于，华为的密度口径与代工厂密度没有直接可比性。堆叠设计可以通过增加有源层，在每封装占位上报告更多的晶体管，哪怕每一颗光刻成型的裸片在前端密度上仍远落后于台积电或英特尔。华为之所以能宣称到 2031 年达到代工厂 14A 等效密度，靠的正是这一点。

![](https://substack-post-media.s3.amazonaws.com/public/images/4e471462-c383-4094-9225-7fd0302bbf29_2043x1228.png)
*SMIC、华为（3D）、TSMC、Intel 与 Samsung 的密度路线图。来源：Huawei、SemiAnalysis*

这不是同类项的代工对比：华为使用堆叠逻辑，并按封装占位计量密度。在归一化的 Bohr 密度口径下，SMIC N+3 约为 114 MTr/mm²，比 Intel 18A 的 HD 库低 38%。华为的 3D 路线图通过堆叠有源逻辑缩小差距，到 2030 年达到 215 MTr/mm²。2031 年，路线图密度跳升到 295 MTr/mm²，意味着要么有第三层有源层，要么部分引入 EUV，要么进行激进的平面 DUV 缩放。

![](https://substack-post-media.s3.amazonaws.com/public/images/97decfee-0a5a-46d5-a730-3a3e7c6eab72_2328x1230.png)
*华为 LogicFolding 密度路线图与 TSMC、Intel 堆叠逻辑的对比。来源：Huawei、SemiAnalysis*

华为的口径也会让其他代工厂显得密度更高。把它套用到 N2 顶层裸片加 N3P 基底裸片的 AMD MI450X 上，可得出 2026 年 460.2 MTr/mm² 的理论密度，相比之下华为 2031 年才是 295 MTr/mm²。

这颗 Kirin 9030 并未使用 LogicFolding，仍采用传统手机 SoC 封装。它构成的是华为与 SMIC 平面缩放所能推进程度的基线。未来对 Kirin 和昇腾（Ascend）芯片的拆解将同时展示平面逻辑密度与华为的混合键合方案。

# 出口管制与未来缩放

出口管制改变的是中国的优化问题，而非终结它。EUV 限制抬高了先进制造的复杂度与成本，但并没有将其冻结。SMIC 通过 DUV 浸没式光刻、SAQP 和 DTCO 达到 N6 级逻辑密度，华为则把更多负担转移到架构、封装和系统级集成上。

未来的节点会更艰难。N+3 还有收紧局部金属、降低单元高度和 CGP 的余地；没有 EUV 的进一步缩放，可用的杠杆更少。更激进的多重图形化会带来更多掩模和更大的套刻误差。SMIC 可以继续压榨 DUV，但每一步都会更昂贵、容错更低。

设计侧同样关键。在 Kirin 9030 之前，华为就拥有国产 EDA 工具与流程，Kirin 9000s、9010 和 9020 已经说明了这一点。在被切断西方 EDA 工具链的情况下，华为仍能在 SMIC N+2 和 N+3 上出货多款消费级 SoC。

美国出口管制于 2022 年限制了面向先进芯片的 EDA 工具，但并未针对更成熟芯片的工具。2025 年，美国政府曾对 Synopsys、Cadence 等厂商的 EDA 软件实施范围广得多的限制，但不到两个月后便在与稀土挂钩的贸易协议中予以解除。华为则始终无法使用这些工具，因为它仍在美国贸易黑名单上。

这迫使华为、SMIC 和中国学术机构自建工具与流程。北京大学的研究人员最近公布了一款面向华为 LogicFolding 架构的原型 EDA 工具——该架构需要新的流程来处理多层版图与布局规划。这还不等于替代完整的 Synopsys 或 Cadence 工具链，但它指明了国产 EDA 的方向：走向架构、工艺与封装之间更紧密的协同优化。

这些进展也在向中国生态系统扩散。SMIC 正按政府指令（而非自愿）向华虹（HLMC/华虹）授权其 N+2 和 N+3 工艺。如果同样的工艺经验反哺到用于 AI 训练与推理的昇腾加速器，卡脖子点就会从某一家具名代工厂转移到整个生态系统。阿里巴巴的平头哥（T-Head）芯片部门，以及预计将为字节跳动供货的中国 AI 芯片设计公司寒武纪（Cambricon），也可能成为重大受益者。一旦制造知识扩散到其他晶圆厂和设计公司，仅针对 SMIC 的制裁效果就会大打折扣。

中国并没有追平与英特尔、三星和台积电的差距。这次拆解在多处展示的恰恰相反：没有 EUV、没有背面供电、更高的工艺复杂度，以及清晰可见的取舍。

但中国仍在前进。如果国产芯片好到足以支撑手机、推理、网络和安全性敏感的负载，那么即便追不上先进制程的台积电，它们也具有战略意义。

在付费墙后，我们将展示 STEEL 的更多能力：SMIC N+3 的材料与工艺流程分析，以及 Kirin 9030 封装的分析。

*我们正在深入剖析市场上最先进的数据中心与 AI 硬件。想了解更多即将推出的内容、获取完整的 Kirin 9030 与 SMIC N+3 分析，或委托定制拆解，请联系 [sales@semianalysis.com](mailto:sales@semianalysis.com)。*

![](https://substack-post-media.s3.amazonaws.com/public/images/d4fe0e41-e05d-4f7d-8427-1dd16f5dd478_1133x723.png)
*我们拆解管线中其他芯片的一瞥。来源：SemiAnalysis*
