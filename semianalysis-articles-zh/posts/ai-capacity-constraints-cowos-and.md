---
title: "AI 产能瓶颈——CoWoS 与 HBM 供应链"
title_en: "AI Capacity Constraints - CoWoS and HBM Supply Chain"
subtitle: "Nvidia、Broadcom、Google、AMD、AMD 嵌入式（Xilinx）、Amazon、Marvell、Microsoft、Alchip、阿里巴巴平头哥、中兴微电子、三星、美光与 SK 海力士的季度爬坡"
date: 2023-07-05
source: https://newsletter.semianalysis.com/p/ai-capacity-constraints-cowos-and
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie", "Gerald Wong"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# AI 产能瓶颈——CoWoS 与 HBM 供应链

> 原文：[AI Capacity Constraints - CoWoS and HBM Supply Chain](https://newsletter.semianalysis.com/p/ai-capacity-constraints-cowos-and) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Nvidia、Broadcom、Google、AMD、AMD 嵌入式（Xilinx）、Amazon、Marvell、Microsoft、Alchip、阿里巴巴平头哥、中兴微电子、三星、美光与 SK 海力士的季度爬坡**

生成式 AI 已经到来，并将改变世界。自从 ChatGPT 风靡全球、激发了我们对 AI 可能性的想象以来，我们看到各行各业的公司争先恐后地训练 AI 模型，并将生成式 AI 部署到内部工作流或面向客户的应用中。不仅仅是大科技公司和初创公司，许多非科技的财富 5,000 强企业也在摸索如何部署基于 LLM 的解决方案。

当然，这需要海量的 GPU 算力。GPU 销量火箭般蹿升，供应链难以跟上 GPU 需求。各公司正争抢 GPU 或云实例。

[连 OpenAI 都拿不到足够的 GPU，这严重制约了其近期路线图。](https://web.archive.org/web/20230601163710/https:/humanloop.com/blog/openai-plans) 由于 GPU 短缺，OpenAI 无法部署其多模态模型；由于 GPU 短缺，OpenAI 无法部署更长序列长度（8k 对 32k）的模型。

与此同时，中国公司不仅投资部署自己的 LLM，还在[美国出口管制进一步收紧之前](https://www.wsj.com/articles/u-s-considers-new-curbs-on-ai-chip-exports-to-china-56b17feb)囤货。例如，[TikTok 背后的中国公司字节跳动据称正向 Nvidia 订购价值超过 $1B 的 A800/H800。](https://www.latepost.com/news/dj_detail?id=1703)

虽然数十万张 GPU 投入 AI 有许多正当用例，但也有很多人一窝蜂抢购 GPU，试图构建一些他们自己都不确定是否有正当市场的东西。某些情况下，大科技公司是为了追赶 OpenAI 和 Google，以免被甩在身后。风投资金洪水般涌向尚无经验证商业用例的初创公司。我们知道有十几家企业在尝试用自己的数据训练自己的 LLM。最后，主权国家也是如此——沙特阿拉伯和阿联酋今年也试图采购价值数亿美元的 GPU。

NVIDIA 最高端的 GPU H100 将持续售罄到明年第一季度，尽管 Nvidia 在大力提升产量。Nvidia 将爬坡至每季度出货超过 400,000 颗 H100 GPU。

今天我们将详细介绍生产瓶颈，以及 Nvidia 及其竞争对手的下游产能在扩张多少。我们还将分享对 Nvidia、Broadcom、Google、AMD、AMD 嵌入式（Xilinx）、Amazon、Marvell、Microsoft、Alchip、阿里巴巴平头哥、中兴微电子、三星、美光和 SK 海力士逐季度供给增长的估计**。**

![](https://substack-post-media.s3.amazonaws.com/public/images/7200eed5-4750-42ef-9709-755af8ec5f0e_2387x2025.png)

Nvidia 的 H100 是封装在 CoWoS-S 上的 7 裸片方案。中央是裸片面积 814mm2 的 H100 GPU ASIC，周围是 6 个 HBM 存储堆叠。HBM 配置因 SKU 而异，H100 SXM 版本使用 HBM3，每堆 16GB、总计 80GB，只用了 5 颗 HBM 加一颗 dummy 裸片。H100 NVL 将有两个封装，每个封装上有 6 个有源 HBM 堆叠。

在只有 5 个有源 HBM 的情况下，非 HBM 裸片可以是 dummy 硅片，作用是为芯片提供结构支撑。这些裸片位于一块硅中介层上（图中不太看得清）。硅中介层则安放在封装基板上，这是一块 ABF 封装基板。

## GPU 裸片与台积电制造

Nvidia GPU 的主要运算部件是处理器裸片本身，采用台积电名为「4N」的定制制程节点制造，产自台积电位于台湾台南的 Fab 18，与台积电 N5、N4 制程节点共用产线设施。[这不是生产的限制因素](https://www.semianalysis.com/p/tsmcs-heroic-assumption-low-utilization)。

由于 PC、智能手机以及非 AI 数据中心芯片的极度疲软，台积电 N5 制程节点的稼动率曾跌破 70%。Nvidia 获得额外晶圆供应毫无问题。

事实上，Nvidia 已为 H100 GPU 和 NVSwitch 下了大量晶圆订单并立即投产，远早于出货芯片所需的时间。这些晶圆将存放在台积电的裸片库（die bank），直到下游供应链有足够产能把它们封装成成品芯片。

基本上，Nvidia 是在消化台积电的部分低稼动率，并因承诺后续购买成品而获得一点价格优惠。

晶圆库（wafer bank），也称裸片库（die bank），是半导体行业的一种做法：部分加工或已完成的晶圆被存储起来，直到客户需要为止。[与其他一些代工厂不同](https://www.semianalysis.com/p/globalfoundries-stuffing-customers)，台积电会把这些几乎完全加工好的晶圆记在自己的账上，帮客户分担。这种做法让台积电及其客户保持财务灵活性。由于只经过部分加工，存放在晶圆库中的晶圆不算产成品，而是归类为在制品（WIP）。只有当这些晶圆全部完工后，台积电才能确认收入并把所有权转移给客户。

这有助于客户粉饰资产负债表，使库存水平看起来处于受控状态。对台积电来说，好处是有助于维持较高的稼动率，从而支撑毛利率。等到客户需要更多库存时，这些晶圆只需最后几道工序即可全部完工，然后按正常售价、甚至略有折扣交付给客户。

## **HBM 在数据中心的兴起：AMD 的创新如何帮了 Nvidia**

GPU 周围的高带宽内存（HBM）是下一个主要部件。HBM 供给同样有限，但正在爬坡。HBM 是通过硅通孔（TSV）连接、[采用 TCB（热压键合）](https://www.semianalysis.com/p/advanced-packaging-part-3-intels)垂直堆叠的 DRAM 裸片（未来更高堆叠层数将需要混合键合）。DRAM 裸片下方是一颗充当控制器的基础逻辑裸片。通常，现代 HBM 有 8 层存储加 1 颗基础逻辑裸片，但我们很快会看到 12+1 层 HBM 的产品，例如 AMD 的 MI300X 和 Nvidia 即将推出的 H100 刷新版。

![](https://substack-post-media.s3.amazonaws.com/public/images/fbe12301-f937-4b2f-95f0-a9c7f8c2e1d9_3999x2250.png)

有趣的是，开创 HBM 的正是 AMD，尽管如今 Nvidia 和 Google 才是用量最大的用户。2008 年，AMD 预测：要让内存带宽持续扩展以匹配游戏 GPU 性能，将需要越来越多的功耗，而这些功耗必须从 GPU 逻辑电路中分走，从而损害 GPU 性能。AMD 与 SK 海力士及供应链上的其他公司（如 Amkor）合作，寻找一种能以更低功耗提供高带宽的内存方案。这促成了 SK 海力士于 2013 年开发出 HBM。

![](https://substack-post-media.s3.amazonaws.com/public/images/8e06f96d-a715-4d5b-a6d9-017eecdf00fe_500x387.jpeg)

2015 年，SK 海力士首次为 AMD 的 Fiji 系列游戏 GPU 出货 HBM，由 Amkor 进行 2.5D 封装。随后是 2017 年采用 HBM2 的 Vega 系列。然而，HBM 对游戏 GPU 性能并没有带来多大改变。由于没有明显的性能优势、成本又更高，AMD 在 Vega 之后重新在游戏显卡上使用 GDDR。今天，Nvidia 和 AMD 的顶级游戏 GPU 仍在使用更便宜的 GDDR6。

不过，AMD 最初的预测在某种程度上是对的：内存带宽扩展确实被证明是 GPU 的一大难题，只不过这主要是数据中心 GPU 的问题。在消费级游戏 GPU 上，Nvidia 和 AMD 已转向用大缓存充当帧缓冲，从而继续使用带宽低得多的 GDDR 内存。

正如我们过去详述的，推理和训练负载对内存需求极大。AI 模型参数数量呈指数级增长，仅权重就把模型体量推到了 TB 级。因此，AI 加速器的性能受限于从内存存取训练和推理数据的能力：这个问题常被称为[内存墙](https://www.semianalysis.com/p/nvidiaopenaitritonpytorch#%C2%A7the-memory-wall)（memory wall）。

为解决这一问题，先进制程数据中心 GPU 都与高带宽内存（HBM）共封装。Nvidia 于 2016 年发布了首款 HBM GPU——P100。HBM 通过在传统 DDR 内存与片上缓存之间找到中间地带来应对内存墙，以容量换带宽。HBM 通过大幅增加引脚数量，实现每个 HBM 堆叠 1024 bit 的内存总线宽度——是 DDR5 每 DIMM 64 bit 位宽的 16 倍——从而获得高得多的带宽。同时，凭借大幅降低的每比特传输能耗（pJ/bit），功耗得到控制。这得益于短得多的走线长度：HBM 的走线以毫米计，而 GDDR 和 DDR 以厘米计。

今天，许多面向 HPC 的芯片公司都在享受 AMD 努力的成果。讽刺的是，AMD 的对手 Nvidia 作为 HBM 用量最大的用户，或许是最大的受益者。

![](https://substack-post-media.s3.amazonaws.com/public/images/4feecb9f-7add-4af9-b4ce-650e13473c98_602x268.png)

## **HBM 市场：SK 海力士一家独大 | 三星与美光投资追赶**

作为 HBM 的开创者，SK 海力士是拥有最先进技术路线图的领导者。SK 海力士于 2022 年 6 月开始生产 HBM3，目前是唯一大批量出货 HBM3 的供应商，市场份额超过 95%，大多数 H100 SKU 用的正是它的 HBM3。当前 HBM 的最高配置是 8 层 16GB HBM3 模组。SK 海力士正在为 AMD MI300X 和 Nvidia H100 刷新版生产数据速率 5.6 GT/s 的 12 层 24GB HBM3。

![](https://substack-post-media.s3.amazonaws.com/public/images/b555e9d1-0d98-43a0-bc74-3e41edd02343_895x427.jpeg)

HBM 的主要挑战在于内存的封装与堆叠，而这正是 SK 海力士的强项，它积累了最强的工艺流程知识。[在另一篇文章中，我们还详述了 SK 海力士的 2 项关键封装创新如何开始放量，并将把当前 HBM 工艺中的一家关键设备供应商挤出去。](https://www.semianalysis.com/p/ai-expansion-supply-chain-analysis)

![](https://substack-post-media.s3.amazonaws.com/public/images/da9acc5f-2a97-40eb-88fc-7984c342831d_2170x1134.png)

三星紧随海力士之后，预计 2023 年下半年出货 HBM3。我们相信它们同时拿到了 Nvidia 和 AMD GPU 的设计导入。目前其出货量与 SK 海力士差距很大，但他们紧追不舍，正投入巨资追赶市场份额。三星正像在标准内存上那样投资追赶，目标是拿下 HBM 市场份额第一。我们听说他们正与一些加速器公司签下优惠协议，试图夺取更多份额。

他们展示了 12 层 HBM 以及未来的混合键合 HBM。三星 HBM-4 路线图一个有趣之处是，他们想在自家的 FinFET 节点上制造逻辑/外围电路。这显示出他们拥有逻辑与 DRAM 代工都在内部的优势。

![](https://substack-post-media.s3.amazonaws.com/public/images/7c1dc967-eb69-49be-b10a-364d22febebe_1742x3086.jpeg)

美光掉队最远。美光曾更重度地投入混合内存立方体（Hybrid Memory Cube，HMC）技术。这是与 HBM 几乎同期发展、概念非常相似的竞争技术。然而 HMC 的生态是封闭的，使其难以发展出周边 IP。此外，它还有一些技术缺陷。HBM 的采用率高得多，最终胜出，成为 3D 堆叠 DRAM 的行业标准。

直到 2018 年，美光才开始从 HMC 转向、投资 HBM 路线图。这就是美光掉队最远的原因。他们还停留在 HBM2E（SK 海力士 2020 年年中就开始量产），甚至连最高档（top bin）HBM2E 都无法成功制造。

在最近一次财报电话会上，美光对其 HBM 路线图发表了一些大胆声明：他们相信凭借 2024 年的 HBM3E，将从掉队者变为领导者。HBM3E 预计第三/第四季度开始为 Nvidia 下一代 GPU 出货。

> 我们的 HBM3——实际上是下一代 HBM3——其性能、带宽都远高于当今行业量产的 HBM3，功耗也更低。这款行业领先的产品将于 2024 年第一季度（CQ1）开始放量爬坡，在 2024 财年带来可观营收，并在 2025 年从 2024 年的水平再大幅增长。而且我们——**我们的目标是在 HBM 上取得非常强劲的份额，高于我们在行业 DRAM 中的自然供给份额**。
>
> Sumit Sadana，美光首席商务官

声称其 HBM 市场份额将高于其整体 DRAM 市场份额，这一表态非常大胆。鉴于他们仍难以大批量制造最高档 HBM2E，我们很难相信美光会在 2024 年初出货先进 HBM3、甚至率先推出 HBM3E 的说法。在我们看来，美光似乎在试图扭转「[AI 输家](https://www.semianalysis.com/p/ai-server-cost-analysis-memory-is)」的叙事——尽管每台 Nvidia GPU 服务器的内存用量远低于 Intel/AMD CPU 服务器。

![](https://substack-post-media.s3.amazonaws.com/public/images/9bd20377-fd7e-4d13-b531-4634da7465ce_2196x912.png)

我们所有的渠道调研都显示：SK 海力士在新一代技术上依然最强，而三星正通过大幅增加供给、大胆的路线图和签协议非常努力地追赶。

## **真正的瓶颈——CoWoS**

下一个瓶颈是 CoWoS 产能。CoWoS（Chip on Wafer on Substrate）是台积电的一种「2.5D」封装技术，将多颗有源硅裸片（通常配置为逻辑芯片与 HBM 堆叠）集成在一块无源硅中介层上。中介层充当其上有源裸片的通信层。随后中介层与有源硅被安装到一块包含 I/O 的封装基板上，以便放置到系统 PCB 上。

![](https://substack-post-media.s3.amazonaws.com/public/images/7f86cdd6-ed3b-4d1e-ac0b-368164184537_1293x488.png)

HBM 与 CoWoS 相辅相成。HBM 对高焊盘数量和短走线长度的要求，决定了必须使用 CoWoS 这类 2.5D 先进封装技术，才能实现如此致密、短距的连接——这在 PCB 甚至封装基板上都做不到。CoWoS 是以合理成本提供最高互连密度和最大封装尺寸的主流封装技术。由于几乎所有 HBM 系统目前都封装在 CoWoS 上，而所有先进 AI 加速器都用 HBM，推论就是：几乎所有先进制程数据中心 GPU 都由台积电以 CoWoS 封装。百度确实与三星合作在其版本上做了一些先进加速器。

虽然台积电 SoIC 等 3D 封装技术可以把裸片直接堆叠在逻辑芯片之上，但对 HBM 而言，由于散热和成本原因并不划算。SoIC 的互连密度高出好几个量级，更适合通过裸片堆叠扩展片上缓存，AMD 的 3D V-Cache 方案就是例证。AMD 旗下的 Xilinx 也是多年前 CoWoS 的第一批用户，用于将多颗 FPGA 小芯片（chiplet）组合在一起。

![](https://substack-post-media.s3.amazonaws.com/public/images/a0865601-28b7-4204-897c-513a955460fd_2048x1159.jpeg)

虽然还有其他一些应用使用 CoWoS，比如网络（其中一些被[用于 GPU 集群组网，如 Broadcom 的 Jericho3-AI](https://www.semianalysis.com/p/nvidias-infiniband-problem-qmx-ai)）、超算和 FPGA，但 CoWoS 绝大多数需求来自 AI。与半导体供应链其他环节不同——那些环节因其他主要终端市场疲软而有大量闲置产能可以吸收 GPU 需求的暴增——CoWoS 和 HBM 本来就是以 AI 为主的技术，所有闲置产能早在第一季度就被消化掉了。随着 GPU 需求爆炸式增长，供应链中跟不上的正是这些环节，它们卡住了 GPU 的供给。

> 就在最近这两三天，我接到一位客户的电话，要求大幅增加后段产能，尤其是 CoWoS。我们仍在评估。
>
> 魏哲家（C.C Wei），台积电 CEO

台积电一直在为更多封装需求做准备，但恐怕没有料到这波生成式 AI 需求来得如此之快。[今年 6 月，台积电宣布其位于竹南的先进后段 Fab 6 开幕。](https://pr.tsmc.com/english/news/3033)这座厂占地 14.3 公顷，其洁净室空间足以支撑每年潜在 100 万片晶圆的 3D Fabric 产能，不仅包括 CoWoS，还包括 SoIC 和 InFO 技术。有趣的是，这座厂比台积电其他封装厂加起来还要大。虽然这只是洁净室空间，距离装备齐全、真正提供那么大的产能还很远，但显然台积电已在为先进封装方案的更多需求做筹备。

![](https://substack-post-media.s3.amazonaws.com/public/images/2ec5b650-d503-451b-b038-db2bf0fd3c82_752x431.png)

稍有帮助的是，晶圆级扇出（Wafer Level Fan-Out）封装产能（主要用于智能手机 SoC）存在闲置，其中一部分可以转用于某些 CoWoS 工艺步骤。特别是两者有一些重叠工序，如沉积、电镀、背面减薄、塑封、贴装和 RDL 形成。我们将在后续文章中梳理 CoWoS 工艺流程以及因此看到需求向好的所有公司。设备供应链正在发生有意义的转移。编者按：后续文章在此。

Intel、三星和 OSAT 厂商也有其他 2.5D 封装技术（如 ASE 的 FOEB），但 CoWoS 是唯一被大批量使用的，因为台积电遥遥领先、是 AI 加速器最主要的代工厂。连 Intel Habana 的加速器也是由台积电制造和封装的。不过，一些客户正在寻找台积电之外的替代方案，我们将在下文讨论。[更多信息请参阅我们的先进封装系列。](https://www.semianalysis.com/p/advanced-packaging-part-1-pad-limited)

## **CoWoS 变体**

CoWoS 有几个变体，但最原始的 CoWoS-S 仍是唯一大批量生产的配置。这就是上文描述的经典配置：逻辑裸片 + HBM 裸片通过带 TSV 的硅中介层连接，中介层再安放在有机封装基板上。

![](https://substack-post-media.s3.amazonaws.com/public/images/8a814f2d-41f1-49a8-9e62-feba55acd065_720x540.jpeg)

硅中介层的一项使能技术叫做「光罩拼接」（reticle stitching）。由于[光刻设备的狭缝/扫描最大只能到这个尺寸](https://www.semianalysis.com/p/die-size-and-reticle-conundrum-cost)，芯片一般最大为 26mm x 33mm。仅 GPU 裸片就已接近这一极限，周围还要放下 HBM，因此中介层必须做得很大，远超光罩极限。台积电用光罩拼接解决这一问题，使其能对数倍于光罩极限的中介层进行图形化（目前最高 3.5 倍，即 AMD MI300）。

![](https://substack-post-media.s3.amazonaws.com/public/images/3c535cc0-8513-4937-9c1a-2e4ae285b47f_2880x3016.png)

CoWoS-R 使用带再布线层（RDL）的有机基板来替代硅中介层。这是一种成本更低的变体，由于用有机 RDL 取代硅基中介层，牺牲了 I/O 密度。正如我们详细分析过的，[AMD 的 MI300 最初设计在 CoWoS-R 上，但我们认为由于翘曲和热稳定性顾虑，AMD 只能改用 CoWoS-S。](https://www.semianalysis.com/p/amd-mi300-taming-the-hype-ai-performance)

![](https://substack-post-media.s3.amazonaws.com/public/images/9f4314f4-d94a-434e-9cb8-3ee42320b9a0_712x334.png)

CoWoS-L 预计今年晚些时候爬坡，它采用 RDL 中介层，但内嵌用于裸片间互连的有源和/或无源硅桥（silicon bridge）。这是台积电对标 Intel EMIB 的封装技术。由于硅中介层越来越难做大，CoWoS-L 将支持更大的封装尺寸。MI300 的 CoWoS-S 可能已接近单块硅中介层的极限。

![](https://substack-post-media.s3.amazonaws.com/public/images/b028f9fd-94b3-4765-b5a3-96b0dec4e7a3_453x286.png)

对更大的设计而言，改用 CoWoS-L 会经济得多。台积电正在开发 6 倍光罩尺寸的 CoWoS-L 超级承载中介层。至于 CoWoS-S，他们没有提及 4 倍光罩以上的任何东西。这是因为硅中介层十分脆弱：它只有 100 微米厚，随着中介层在工艺流程中越做越大，面临分层或开裂的风险。

## **CoWoS 客户**

![](https://substack-post-media.s3.amazonaws.com/public/images/4aba0593-eec3-4e48-85a4-7a22f4049b08_905x656.png)

注意，该图并非按比例或百分比绘制，我们的模型提供实际单位数据。

对订阅者，我们将逐一分析各家 CoWoS 公司的需求：Nvidia、Broadcom、Google、AMD、AMD 嵌入式（Xilinx）、Amazon、Marvell、Microsoft、Alchip、阿里巴巴平头哥和中兴微电子。

[团购订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
