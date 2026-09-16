---
title: "Zen 4c：AMD 对超大规模云厂商 ARM 与 Intel Atom 的回应"
title_en: "Zen 4c: AMD's Response to Hyperscale ARM & Intel Atom"
subtitle: "Bergamo 出货量、ASP、性能、超大规模厂商订单转向、裸片图、平面布局、物理设计与高密度核心变体的未来用途"
date: 2023-06-05
source: https://newsletter.semianalysis.com/p/zen-4c-amds-response-to-hyperscale
crawled: 2026-09-15
authors: ["Dylan Patel", "Gerald Wong"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Zen 4c：AMD 对超大规模云厂商 ARM 与 Intel Atom 的回应

> 原文：[Zen 4c: AMD's Response to Hyperscale ARM & Intel Atom](https://newsletter.semianalysis.com/p/zen-4c-amds-response-to-hyperscale) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Bergamo 出货量、ASP、性能、超大规模厂商订单转向、裸片图、平面布局、物理设计与高密度核心变体的未来用途**

Bergamo 是 AMD 即将推出的 128 核服务器产品，将 x86 CPU 性能推向新高度。Bergamo 从架构上就是为[云原生（cloud native）](https://www.semianalysis.com/p/sound-the-siryn-ampereone-192-core)而生，在摩尔定律趋于停滞之际，它代表着数据中心 CPU 设计的一个重要拐点。Bergamo 的核心是 Zen 4c——其大获成功的 5nm Zen 4 微架构的全新高密度核心变体，正是它支撑了每插槽核心数的持续攀升。虽然 Zen 4c 的官方细节至今相当匮乏，但 AMD 首席技术官在 [Ryzen 7000 发布会主题演讲](https://youtu.be/WcH_7xsYtUk?t=1224)上这样说道：

> 我们的 Zen 4c 是我们的紧凑高密度版本，是一个新增项，是我们核心路线图上的一条新泳道，它以大约一半的核心面积提供与 Zen 4 完全相同的功能。
>
> Mark Papermaster，AMD CTO

在这篇深度解析中，我们将分享我们对 Zen 4c 架构、市场影响、ASP、出货量、超大规模厂商订单切换的分析，以及 AMD 如何在保持相同核心功能与性能的同时将核心面积减半。我们将审视 AMD 为何在 CPU 设计上开辟这条新路径，以回应市场需求以及来自 [Amazon](https://www.semianalysis.com/p/amazons-cloud-crisis-how-aws-will)、[Google](https://www.semianalysis.com/p/google-ai-infrastructure-supremacy)、[Microsoft](https://semianalysis.sharepoint.com/:w:/s/Confidential/EeVJIcFY-7dFsfjT6D0coHQBkvpnm7ym5dsItRd7EtKNLw)、[Alibaba](https://www.semianalysis.com/i/122267137/ipo-hyperscale-in-house-chips-and-amdintel-competition)、[Ampere Computing](https://www.semianalysis.com/p/sound-the-siryn-ampereone-192-core) 的 ARM 架构芯片以及 Intel 的 x86 Atom E 核的竞争。

![](https://substack-post-media.s3.amazonaws.com/public/images/6308e8a6-3049-481b-a73b-8c406889761e_1885x1800.png)

最后，我们将分析 Bergamo 更低的生产成本和预期销量，以及高密度核心变体未来在 AMD 客户端、嵌入式和数据中心产品线中的普及。在深入这些市场与架构细节之前，先分享一些更高层次的背景。

## **摩尔定律尽头的云 CPU 时代**

Zen 4c 与 Bergamo 设计理念的核心，是在摩尔定律放缓、与硅的物理极限搏斗的同时，交付尽可能多的计算资源。这种放缓是全行业现象，尽管对核心数持续增加的呼声不断，它仍给设计者带来挑战。当 AMD 将其 128 核 Bergamo 推向市场时，对手 Intel 正在筹备其 144 核的「Sierra Forest」。两者都在应对数据中心中 ARM CPU 核心的崛起——从 [Amazon](https://www.semianalysis.com/p/amazons-cloud-crisis-how-aws-will)、[Google](https://www.semianalysis.com/p/google-ai-infrastructure-supremacy)、[Microsoft](https://semianalysis.sharepoint.com/:w:/s/Confidential/EeVJIcFY-7dFsfjT6D0coHQBkvpnm7ym5dsItRd7EtKNLw) 和 [Alibaba](https://www.semianalysis.com/i/122267137/ipo-hyperscale-in-house-chips-and-amdintel-competition) 等超大规模厂商的自研努力，到商用芯片厂商的 [192 核 AmpereOne 云原生 CPU](https://www.semianalysis.com/p/sound-the-siryn-ampereone-192-core)。

[虽然随着生成式 AI 的崛起，GPU、加速器和 ASIC 风头正劲，吞下越来越多的资本开支](https://www.semianalysis.com/p/ai-server-cost-analysis-memory-is)，但不起眼的通用 CPU 依然是全球绝大多数数据中心部署的基础骨干。在云计算范式中，游戏规则就是最大化计算资源、最小化总拥有成本（TCO）。

增加核心数是省电省钱的主要手段之一。插槽整合（socket consolidation）——用一颗新 CPU 替换四颗或更多旧 CPU——正大行其道。市面上有大量 22 至 28 核、14nm 工艺、耗电惊人的 Intel CPU 等待替换。自 2010 年代中期以来我们还没有经历过一轮基础设施更替周期，云厂商已把服务器寿命从 3 年延长到 6 年。随着新一代云原生 CPU 的性能/TCO 改善刺激开发投入，这种局面很快就会改变。

通过整合，可以减少对又慢又耗电的跨插槽通信和网络通信的依赖，所需的物理资源（风扇、电源、电路板等）也更少。即便在同代产品中，两台 32 核服务器的功耗本质上也会高于一台提供相同性能的 64 核服务器。在云端，计算节点更少、单节点更强时，客户端在计算网络上的创建、缩减和迁移都更简单。

然而，更多核心意味着更多功耗。过去 7 年里，CPU 插槽热设计功耗（TDP）从 140W 飙升至 400W。2024 年平台将突破 500W！尽管如此，热密度上升带来的功率与散热限制，意味着 TDP 的增长与核心数的增长并不相称，结果是分摊到每个核心的功耗预算不断下降。以高时钟频率和高功率运行可以最大化每核心性能和每 mm² 硅面积的性能——这是成本的基本单位。

行业趋势是：任一给定工作负载下的每瓦性能才是最重要的因素，因而可以获得可观的溢价。看看 AMD 从 Milan 到 Genoa 的换代就知道：仅仅凭借更高的部署密度和每瓦性能，AMD 就能够[提价 80%](https://www.semianalysis.com/p/2023-datacenter-outlook-amd-and-intel)。

因此，CPU 架构师必须在核心设计上精心权衡，以优化每瓦性能。与此同时，随着摩尔定律放缓，新制程节点的每晶体管成本趋于平线，控制晶体管预算和核心尺寸的任务变得更加艰难。

![](https://substack-post-media.s3.amazonaws.com/public/images/8390270a-072e-4335-b486-dd8f5af1f4e3_1379x776.png)

工程师在性能、功耗、面积等多个变量之间，凭不完整的信息做出设计权衡。性能、功耗、面积（PPA）曲线的一端是 IBM 的 Telum，专注于为传统大型机式应用提供极致的单核性能。为了服务银行、航空和政府客户，IBM 必须打造巨型核心、5GHz+ 时钟频率和极致可靠性，而这些对于新兴的容器化分布式工作负载来说代价过高。

曲线的另一端是微控制器和低功耗移动芯片中的 CPU，它们优先考虑能效和最小面积（成本）。Intel 在智能手机革命中的失利，意味着他们缺少 ARM 十年的能效优化设计经验。这种设计取向的差异，在 Apple 用 M1 Mac 把自家架构放大并彻底击溃 Intel 时显露无遗。Intel 的高性能 P 核多年来为了追逐单核性能和 6GHz 时钟频率，牺牲了功耗和面积，变得愈发臃肿。把同一颗核心跑在服务器芯片 3GHz 以下的频率上，在面积效率上绝非最优。

Intel 明年的 Sierra Forest 将通过把 E 核设计带入数据中心来解决这一问题。E 核源自其 Atom 低功耗核心产品线，Intel 可以在给定裸片面积下塞入 3-4 倍的核心数。不过，E 核的局限在于指令集架构（ISA）特性等级降低、每时钟指令数（IPC）更低，导致单核性能和能效更差。在许多工作负载中，后一短板完全可以通过核心数的大幅增加来弥补。

Intel 开始在客户端产品线中组合 E 核与 P 核，以提升每 mm² 的多线程性能，而 ISA 不匹配也带来了一些怪相，比如 P 核上的 AVX-512 被禁用，还需要一个硬件线程调度器来把工作负载分配给特性迥异的核心。至于纯 E 核的 Sierra Forest，其目标是以少得多的硅面积提供接近 P 核 Granite Rapids 的插槽性能。其后继者 Clearwater Forest 则将在性能和每插槽核心数上全面发力。

回到 AMD——他们既没有智能手机经验，也没有低功耗核心血统的独立设计团队。他们的 Zen 核心必须覆盖从 5.7GHz 桌面到高能效笔记本和服务器。作为对 ARM 和 Atom 的回应，他们创造了 Zen 4c。Zen 4c 是 AMD 各设计团队通力协作的成果：打造一颗位于性能、功耗、面积（PPA）曲线上另一个点位的核心，以更好地契合数据中心 CPU 工作负载的新趋势。相当取巧的是，AMD 拿同样的 Zen 4 架构，通过物理设计上的多项技巧省下了大量面积。

这意味着完全相同的 IPC 和 ISA 特性等级，简化了客户端的集成。事实上，AMD 还在其低端 4nm Ryzen 7000U「Phoenix」移动处理器中悄然将部分 Zen 4 核心换成了 Zen 4c 核心。在 Bergamo 上，Zen 4c 让 AMD 在节省面积和成本的同时，把核心数从 96 提升到 128。这种设计理念的分叉在未来几代硬件中还会加剧。

接下来我们先讲透技术细节，最后再拉远视角，覆盖成本、ASP、超大规模厂商订单切换、出货量，以及在非数据中心环境中的采用。

## **AMD EPYC 9004「Bergamo」规格**

![](https://substack-post-media.s3.amazonaws.com/public/images/9ef557e3-9436-407c-a915-6f6872be9f44_683x868.png)

上表是 Bergamo 的规格表及其与 Genoa 的差异。6 月将发布两款型号：全核启用的 128 核 EPYC 9754 和屏蔽了 1/8 Zen 4c 核心的 112 核 EPYC 9734。与 Genoa 最好的 96 核 EPYC 9654 相比，Zen 4c 让 Bergamo 在同样的 SP5 插槽和 360W TDP 下装下 1.33 倍的核心数。Zen 4c 的私有缓存容量与 Zen 4 相同，L1 完全一致，L2 同为 1MB。在云和虚拟化环境中，保留足够大的私有缓存非常重要。这有助于减少对共享资源的依赖、降低「吵闹邻居」的影响，从而维持性能一致性。

Bergamo 的时钟频率也有所下降，基础频率低 150MHz，加速频率低 600MHz。很自然，同样的 360W 插槽 TDP 下塞进更多核心，就意味着更低的运行频率。Bergamo 在原始 CPU 吞吐量（核心数 x 基础频率）上仍有 1.25 倍优势，而 Genoa 虽然能加速到更高频率，但那只在低利用率场景下有帮助。Bergamo 面向的是以可预测性能为关键指标的云环境，工作频率区间也更低。

Bergamo 另一大差异在裸片与 L3 缓存配置上。CCD 数量从 Genoa 的 12 颗降到 Bergamo 的 8 颗，这意味着 Bergamo 每颗 CCD 上有 16 个 Zen 4c 核心，而 Genoa 每颗 CCD 是 8 个 Zen 4 核心。Bergamo 还恢复了每颗 CCD 多个 CCX 的设计，上一次见到它还是在 EPYC 7002「Rome」一代。这将裸片一分为二，一半上的核心要想到另一半，必须经 IO Die 绕一大圈。

这对性能的影响下文详述。虽然 Bergamo 每个 CCX 仍有 8 个可本地通信的核心，但它们的共享 L3 缓存减半至 16MB。这种减半的 L3 也出现在 AMD 的移动设计中，目的是省面积。虽然这会损害部分工作负载的 IPC，但对更强调每 mm² 性能、弱化共享资源的 Bergamo 来说是合理的。需要大 L3 的用户可以期待 Genoa-X，其 L3 高达 1152MB。

Bergamo 使用与 Genoa 相同的 IO Die，因此 SP5 插槽 IO 完全一致：12 通道 DDR5-4800、128 条 PCIe 5.0 通道、支持双路。不过，Bergamo 的 IO Die 只连接 8 颗 CCD（Genoa 是 12 颗），这就带来一个问题：AMD 能否做出 12 CCD、192 核的 Bergamo？撇开每核心功耗预算和内存带宽会大幅降低不谈，硅片本身理论上支持。但封装做不到。

![](https://substack-post-media.s3.amazonaws.com/public/images/551f3f7b-e607-450c-9469-54f9c57e9fd8_1885x1800.png)

IO Die 有 12 条全局内存互连 3（GMI3）小芯片链路，经封装基板走线。在 Genoa 上，距离 IO Die 较远的 CCD 的 GMI3 走线从较近 CCD 的 L3 缓存区域下方通过。事实证明，这在 Bergamo 上更困难，因为 Zen 4c CCD 密度更高，走线必须从较近 CCD 更小的 L3 下方经过，需要更多布线层。从 CCD 裸片摆放上可以直观看到结果：Genoa 上每 3 颗 CCD 紧挨着放置，而 Bergamo 的 CCD 之间留有空隙用于走线。封装还要在中间走 PCIe、上下走 DDR5，可用空间不足以容纳 12 颗 Zen 4c CCD。

## **裸片图、平面布局与核心分析**

这是 Bergamo 的 Zen 4c CCD 裸片图，代号「Vindhya」。制作素材来自 AMD 在 ISSCC 2023 提供的、代号为「Durango」的 Zen 4 CCD 资料。可以看到并排的两个 8 核 CCX 计算复合体，各带 16MB 共享 L3。这个 L3 还去掉了用于 3D V-Cache 的硅通孔（TSV）阵列，省下了一小块面积。这是合理的，因为云工作负载并不能从大量共享缓存中获得同等收益。

![](https://substack-post-media.s3.amazonaws.com/public/images/d3ae5eac-9709-443c-80d2-978f24ee65f8_1059x1751.png)
*来源：B. Munger 等，《"Zen 4"：AMD 5nm 5.7GHz x86-64 微处理器核心》，2023 IEEE 国际固态电路会议（ISSCC），美国旧金山，2023 年，第 38-39 页，doi: 10.1109/ISSCC42615.2023.10067540。*

然而，真正令人震惊的是裸片面积。16 个 Zen 4c 核心只比 8 个 Zen 4 核心略大。在 ISSCC 2023 上，AMD 公布 Zen 4 的 CCD 为 66.3mm²。这是不含边缘裸片密封和切割道的设计面积。Zen 4c 的 CCD 设计面积只有 72.7mm²，大了不到 10%！要知道，每颗裸片上的核心数翻倍、L2 缓存翻倍、L3 缓存总量不变。核心本身必定大幅缩小，才能在面积仅小幅增加的情况下塞进更多缓存。

关于小芯片互连，两颗裸片上的封装内 Infinity Fabric（IFOP）相同，均由两条 GMI3-Narrow 链路组成。不过，虽然裸片支持双链路，目前似乎没有任何 Zen 4c 型号同时使用两条 GMI3 链路。两个独立 CCX 的信号是通过单条链路复用（mux）送往 IO Die 的。

![](https://substack-post-media.s3.amazonaws.com/public/images/f7e48eab-af56-435b-9680-1ecfd901835b_1200x1502.png)

放大看核心，会发现设计与布局上的巨大差异。下表是 Zen 4c（代号「Dionysus」）与 Zen 4（代号「Persephone」）的面积拆解对比。

![](https://substack-post-media.s3.amazonaws.com/public/images/741b5e8f-787f-430d-813f-77882cc48724_673x382.png)

Zen 4c 相对 Zen 4 的核心面积下降了 35.4%，这很了不起，因为该数字还包含各自 1MB 的 L2 缓存。虽然这意味着 L2 的 SRAM 单元占用相同面积，但 AMD 通过让 L2 控制逻辑更紧凑，缩小了 L2 区域的面积。若剔除 L2 和核心全局逻辑（CPL）区域，核心缩小了惊人的 44.1%，引擎部分（前端 + 执行）面积几乎减半。

这正是 Papermaster 所说的：Zen 4c 与 Zen 4 本质上是同一个设计、同样的 IPC，只是实现和布局方式不同，堪称工程壮举。浮点单元（FPU）缩小的幅度没有其他部分那么大，可能是出于热点的考虑——高负载下 FPU 通常是核心中最热的部位。我们还注意到，核心内部的 SRAM 单元似乎也紧凑得多，面积减少 32.6%。从右下角的页表遍历器（Page Table Walker）上可以清楚看到这一点。

## **物理设计技巧**

AMD 打造 Zen 4c 的方式，是拿完全相同的 Zen 4 寄存器传输级（RTL）描述——它定义了 Zen 4 核心 IP 的逻辑设计——然后以紧凑得多的物理设计去实现它。两者都在 TSMC N5 上制造，设计规则相同，面积差异却极其巨大。我们详细拆解实现这一点的三大器件物理设计关键技术。

![](https://substack-post-media.s3.amazonaws.com/public/images/9fdde53d-3f5a-4884-aadb-cb48bab1934b_1419x853.png)
*来源：S.-Y. Wu 等，《面向移动 SoC 与高性能计算应用、能效与性能增强的 3nm CMOS FinFlex™ 平台技术》，2022 年国际电子器件会议（IEDM），美国旧金山，2022 年，第 27.5.1-27.5.4 页，doi: 10.1109/IEDM45625.2022.10019498。*

第一，降低设计的时钟目标可以在核心综合时减少面积。这是一颗 ARM Cortex-A72 CPU 核心在 TSMC N5 和 N3E 节点上综合出的速度-面积曲线。即便同一节点上的同一核心设计，在核心面积和可达时钟频率之间也有选择余地。时钟目标更低时，设计者在关键路径的设计上有更多回旋空间，时序收敛更简单，也减少了为满足放宽后的时序约束所需的额外缓冲器单元数量。如今大多数设计受布线密度和拥塞限制，更低的运行时钟让设计者能把信号路径压得更密，提高标准单元密度。

![](https://substack-post-media.s3.amazonaws.com/public/images/3b95171e-fe67-4b9b-822e-7ccc66504e27_762x800.png)
*来源：T. Singh 等，《2.1 Zen 2：AMD 7nm 高能效高性能 x86-64 微处理器核心》，2020 IEEE 国际固态电路会议（ISSCC），美国旧金山，2020 年，第 42-44 页，doi: 10.1109/ISSCC19947.2020.9063113。*

标准单元密度指设计中可布单元区域被标准单元占据的比例。标准单元是触发器、反相器等功能电路，在整个设计中重复出现，组合成复杂的数字逻辑。它们有各种不同尺寸，正如这张布局软件特写所示。蓝色矩形是标准单元，黑色区域是未填充的。我们突出标出了一个低单元密度区域（约 50% 面积利用率）和一个高单元密度区域（90% 以上）。输入输出信号引脚数量多的标准单元会挤占附近的布线资源，实际上会阻碍相邻空间的标准单元放置。

![](https://substack-post-media.s3.amazonaws.com/public/images/801b27ef-a97e-4ad2-b49c-6421d932c139_1591x1162.png)
*来源：《采用 PowerVia（背面供电）技术的 Intel 4 工艺 E 核实现》——Intel 公司，VLSI 2023 论文 T1-1*

把视野拉远看整个核心，可以生成一张单元密度图，总览标准单元排布紧密的区域（橙色、黄色）和面积利用率较低的区域（绿色、蓝色）。黑色矩形是先于标准单元摆放大规模 SRAM 宏。这一切意味着：AMD 本可以拿他们的 Zen 4 核心，沿速度-面积曲线下移直接缩小，核心外观会大体相似、只是单元密度更高。但 Zen 4c 看起来截然不同，原因在于下一种物理设计手法。

![](https://substack-post-media.s3.amazonaws.com/public/images/a7a32d84-9799-462b-90ab-7e9eb9ced469_2150x900.png)
*来源：I. Kang，《扩展的艺术：分布式与互联以延续计算的黄金时代》，2022 IEEE 国际固态电路会议（ISSCC），美国旧金山，2022 年，第 25-31 页，doi: 10.1109/ISSCC42614.2022.9731536。*

Zen 4c 之所以看起来如此不同，是因为采用了分区更少的更扁平设计层级。对于这种数亿晶体管的复杂核心设计，在平面布局上把核心拆成多个独立区域是合理的，设计者和仿真工具可以并行工作，加快上市时间（TTM）。对某个电路的工程改动也可以隔离在一个子区域内，而不必重做整个核心的布局布线。

刻意分离时序关键区域还有助于缓解布线拥塞、减少相互干扰以实现更高时钟频率。我们看到 ARM 的 Neoverse V1 和 Cortex-X2 核心在逻辑区域之间没有硬分区，布局尽可能塞紧。从物理裸片上看，各区域显得浑然一体。另一方面，Intel 的 Crestmont E 核则有许多清晰可见的分区，边界以紫色标出。

从我们的 Zen 4 核心标注中可以看到，核心内每个逻辑块都有众多分区，而 Zen 4c 将其大幅削减到仅 4 个分区（L2、前端、执行、FPU）。通过合并 Zen 4 的这些分区，各区域可以挤得更近，进一步提升标准单元密度，开辟了又一条省面积的路。可以说 AMD 的 Zen 4c「长得像一颗 ARM 核心」。

![](https://substack-post-media.s3.amazonaws.com/public/images/bdde045e-ee01-4da0-a79d-39596eefcf1a_602x362.png)

最后一种缩小面积的方法是使用密度更高的存储。Zen 4c 缩小了核心内部的 SRAM 面积，因为 AMD 换用了新型 SRAM 位单元。图中是一个 8 晶体管（8T）SRAM 电路的示意图。中间的 4 个晶体管用于存储 1 比特信息，2 对存取晶体管连接 2 对字线和位线。高性能乱序执行核心有多种功能要对同一块存储进行读写，因此要用到这些 8T 双端口位单元。与密度更高的 6T 单端口位单元相比，它们占用更多面积，并需要双倍的信号布线资源。

为了省面积，AMD 用 TSMC 开发的新型 6T 伪双端口位单元替换了这些 8T 双端口位单元。

> 《5nm 工艺下同周期双泵读写的 4.24GHz 128X256 SRAM》，Z. N. Zhang 等，TSMC，中国台湾
>
> 本文提出了一种采用单端口 6T 位单元宏的高速 1R1W 双端口 32Kbit（128X256）SRAM。为增强读取性能，提出了一种带 TRKBL 旁路的先读后写（Read-Then-Write，RTW）双泵 CLK 生成电路。采用双层金属方案以改善信号完整性和整体工作时钟周期。在灵敏放大器（Sense-Amp）中引入局部互锁电路（Local Interlock Circuit，LIC）以降低动态功耗并进一步推高 Fmax。硅片结果表明，在 5nm FinFET 工艺下，慢角晶圆在 1.0V、100 摄氏度条件下可实现 4.24GHz。

TSMC 将在 6 月的 VLSI 2023 上公布这种新位单元的更多细节，SemiAnalysis 将到场。从描述来看，TSMC 通过在同一时钟周期内顺序执行读和写操作，模拟出了双端口位单元的行为。虽然这不如两个独立访问端口灵活，但面积缩减足够显著，促使 AMD 在 Zen 4c 上采用了该技术。随着 [SRAM 面积微缩陷入停滞](https://fuse.wikichip.org/news/7343/iedm-2022-did-we-just-witness-the-death-of-sram/)，此类省面积技术今后会越来越多。

[分享](https://newsletter.semianalysis.com/p/zen-4c-amds-response-to-hyperscale?utm_source=substack&utm_medium=email&utm_content=share&action=share)

接下来，让我们把视角拉远，覆盖性能、成本、ASP、超大规模厂商订单切换、出货量，以及在非数据中心环境中的采用。

## **性能**

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
