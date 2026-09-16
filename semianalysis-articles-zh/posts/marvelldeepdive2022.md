---
title: "Marvell 的愿景——定制芯片、CXL、DPU、以太网、光通信、电信、存储、汽车、SerDes、2025 年营收与 EPS"
title_en: "Marvell's Vision – Custom Silicon, CXL, DPUs, Ethernet, Optical, Telecom, Storage, Automotive, SerDes, 2025 Revenue & EPS"
subtitle: "转型为基础设施硅片领导者 & EPS 预估"
date: 2022-12-11
source: https://newsletter.semianalysis.com/p/marvelldeepdive2022
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Marvell 的愿景——定制芯片、CXL、DPU、以太网、光通信、电信、存储、汽车、SerDes、2025 年营收与 EPS

> 原文：[Marvell's Vision – Custom Silicon, CXL, DPUs, Ethernet, Optical, Telecom, Storage, Automotive, SerDes, 2025 Revenue & EPS](https://newsletter.semianalysis.com/p/marvelldeepdive2022) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**转型为基础设施硅片领导者 & EPS 预估**

Marvell 最近在其圣克拉拉总部接待了我们。他们讲述了自身的愿景以及未来的诸多产品细节。核心在于：Marvell 正努力成为基础设施硅片（infrastructure silicon）领域的领导者。在大多数情况下，Marvell 做的不是那些性感吸睛的 AI 加速器、堆料的数据中心 CPU，也不是 I/O 最多的交换机。相反，Marvell 力求打造处于数据流动、存储、处理与安全核心位置的 IP 与合作伙伴关系。

这些芯片里很可能都会有 Marvell 的一席之地，但 Marvell 并非唯一参与的公司。要成为基础设施领域的领导者，就需要与终端市场开展深度且定制化的协作——许多其他半导体公司无论在技术还是文化上都不具备这样的基因。

Marvell 的企业文化将来会是一个精彩的案例研究。自 2018 年以来，其员工数量翻了一番。如今的文化既不像被收购的那些公司，也不像老 Marvell。过去一年里与我们交谈过的该公司许多员工来看，如今的文化似乎是近几年多次收购进来的各路人马的融合体。尽管每个人加入 Marvell 的路径和背景各不相同，各个 IP 团队之间的协作依然紧密无间。

Marvell 与我们分享了他们的愿景和路线图；作为回报，我们将以批判性的眼光加以分析，指出我们认为他们会成功的地方，以及我们对其中哪些持怀疑态度。Marvell 以他们心目中的 4 大垂直市场开场：数据中心、电信基础设施、汽车和企业网络。

本报告将对这些市场做整体讨论，并更具体地分析以下领域的机会与竞争定位：云交换机、企业交换机、汽车交换机、超大规模云定制芯片的多个重大设计导入、HDD 控制器、SSD 控制器、DSP、TIA、可插拔光模块、共封装光学（CPO）、有源电缆（AEC）、基础设施 DPU、网络 DPU、5G 基带与射频单元 DPU、5G 分布式单元 DPU、[安全](https://www.semianalysis.com/p/marvells-next-1b-business-is-security)、AI 训练、AI 推理、CXL（正在开发的产品类别多达 9 种），以及[视频 ASIC](https://www.semianalysis.com/p/meet-netint-the-startup-selling-to)。

本报告还将分享我们对 FY2023、FY2024 和 FY2025 的营收和 EPS 预估。这些预估建立在我们自下而上的分析之上，来源于按产品线/类别拆分的营收预测。

Marvell 着重强调了业务在这一框架下的转型。2019 年，Marvell 在云领域的渗透率还很低，运营商基础设施 OEM 合作伙伴只有 1 家，在汽车市场刚刚入场，在企业网络上是远落后于 Broadcom 的第二名。这与今天的 Marvell 已截然不同。

2022 年的 Marvell 在存储的诸多方面依然像以往一样是领导者——保持着 SSD 和 HDD 控制器的第一地位，同时在企业网络市场上仍是远落后于 Broadcom 的第二名。网络才是 Marvell 重塑自身的战场。对 Innovium 的收购帮助 Marvell 进入了拥挤的超大规模数据中心交换机市场——Broadcom 在那里占据绝对领导地位，Nvidia、Cisco 和 Intel 也都杀得难解难分。Marvell 的老业务加上收购来的 Aquantia 业务，在企业交换机市场占有更高份额。Aquantia 业务还在帮助 Marvell 切入汽车以太网。

精彩的 Inphi 收购案正帮助 Marvell 领跑 PAM4 DSP/TIA 和相干 DSP/TIA 市场，并收获一个二线光子学业务。Cavium 的加入使 Marvell 成为 DPU 和云 [HSM](https://www.semianalysis.com/p/marvells-next-1b-business-is-security) 领域的领导者。Cavium 业务与 Avera ASIC 及定制设计业务的结合，还让 Marvell 登上了基础设施 5G 基带处理器的头把交椅。所有这些收购得来的 IP 加上 Marvell 的老本行家底，也可能推动他们领跑云端超大规模定制芯片业务。

这座 IP 军火库，加上协作进取的文化，使 Marvell 成为最顶尖的半导体公司之一。

通过整合业界顶尖的 SerDes、设计方法学、验证手段和先进制程技术，Marvell 得以覆盖数据中心、运营商基础设施、汽车和企业网络。5nm 制程技术对 Marvell 意味着一次重大转变。在此之前，在 7nm 和 16nm 时代，Marvell 要等制程节点进入大批量制造（HVM）一年多之后才运行首批测试芯片。而到了 5nm 和 3nm，只要 TSMC 一放行，Marvell 就第一时间上车跑初批 shuttle 流片。

2020 年 4 月，Marvell 就在 TSMC 的 N5P 制程节点上拥有了一款 112G SerDes。我们推测这是 Inphi 的成果，而非 Marvell 自己的。2022 年，Marvell 流片了两颗测试芯片，一颗在 TSMC N3 上，另一颗在 TSMC N3E 上。前者帮助他们决定跳过 N3（很可能是由于其性能和功耗提升有限），后者则让 Marvell 得以测试下一代 SerDes、DSP 和计算 IP，从而加快上市时间、提升竞争力。测试芯片中同时包含了 Marvell 自身和 Inphi 收购得来的 IP。

值得注意的是，仅在过去 6 个月里，Marvell 就完成了 2 次面积超过 700mm^2 的流片。关于这项定制芯片工程的更多细节稍后再谈。

在砸下整套光罩所需的巨资之前，Marvell 高度重视系统建模、仿真、形式验证和混合仿真。Marvell 正让自己避开那股困扰着 Intel 和许多其他设计团队的「半导体复兴的阴暗面」。

[![](https://substackcdn.com/image/fetch/$s_!HwSb!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F0150776c-9bf2-4bea-a9c2-41b24b7a0f15_1280x1280.png)SemiAnalysisThe Dark Side Of The Semiconductor Design Renaissance – Fixed Costs Soaring Due To Photomask Sets, Verification, and ValidationWe are in the midst of a semiconductor design renaissance. Nearly every major company in the world has their own silicon strategy as they try to become vertically integrated. There are also more chip startups than ever. The industry is rapidly shifting away from using Intel CPUs for everything. As Moore’s law slows, design is flocking towards heterogene…Read more4 years ago · 32 likes · 19 comments · Dylan Patel](https://www.semianalysis.com/p/the-dark-side-of-the-semiconductor?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

Marvell 还力争成为电光连接（electro-optical）领域的领导者。Inphi 已经在以太网世界握有这种领导地位，只要投资和工程到位，这种领导力有望扩展到封装之间和封装之内的一切电与光的连接。

在长距光模块市场，Marvell 主导着 112G PAM4 DSP 和 TIA，并正着手在下一代 224G 上复制同样的地位。在超长距相干模块市场，Marvell 专注于保持在 400G QAM 16 及下一代 800G DSP、TIA 和可插拔收发器上的领先。我们对其能否在竞争如此激烈的共封装光学（CPO）时代继续得逞则更为怀疑：Broadcom、Intel、Nvidia 和 Ayar Labs 等多家公司的产品化进度都领先于 Marvell。

[先进封装](https://www.semianalysis.com/p/advanced-packaging-part-1-pad-limited)对于成为半导体新时代的领导者同样至关重要。Marvell 目前在产品中对先进封装的运用还不多，而 AMD、Intel、Broadcom、Nvidia 等竞争对手不仅用得多、经验也更丰富。Marvell 想要追上并反超这一差距，因此他们专注于把整个产品线转向小芯片（chiplet）化。3nm 小芯片普遍规划为只带很少的 I/O，更聚焦于计算 ASIC 和低面积的裸片间互连；5nm 小芯片将用于 SerDes 和连接性。Marvell 对先进封装带来的独特散热挑战给予了特别的关注。

[![](https://substackcdn.com/image/fetch/$s_!HwSb!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F0150776c-9bf2-4bea-a9c2-41b24b7a0f15_1280x1280.png)SemiAnalysisAdvanced Packaging Part 1 – Pad Limited Designs, Breakdown Of Economic Semiconductor Scaling, Heterogeneous Compute, and ChipletsAdvanced packaging has been an increasingly common theme with semiconductors over the last handful of years. In this multi-part series, SemiAnalysis will break down the mega-trend. We will do a deep dive into the technologies that enable advanced packaging such as high accuracy flip chip, thermocompression bonding (TCB), and various types of hybrid bonding (HB). In part 1 of the deep dive, we focus on the need for the technology and why the industry is moving towards advanced packaging in a major way…Read more5 years ago · 6 likes · Dylan Patel](https://www.semianalysis.com/p/advanced-packaging-part-1-pad-limited?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

# DPU

对 Marvell 而言最重要的业务单元之一就是 DPU。它是基础设施处理的心脏，形态多元——从 5G 处理到网卡以及介于两者之间的一切。

DPU 是一个统称，指在单一封装内集成了特定任务所需的计算、加速器和网络接口的产品。相比之下，标准 CPU 在同一颗芯片上没有加速器也没有网络——依赖外部芯片来实现加速和网络，会导致方案功耗过高，限制其在基础设施平台上的使用。

DPU 的历史颇有趣味。Nvidia 借 Bluefield 2 DPU 的营销让这个词流行起来，但 Marvell 认为通过 Cavium 的老班底，他们做 DPU 已有约 17 年历史。安全业务和能力同样源自 Cavium 这笔遗产。

[![](https://substackcdn.com/image/fetch/$s_!HwSb!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F0150776c-9bf2-4bea-a9c2-41b24b7a0f15_1280x1280.png)SemiAnalysisMarvell's Next $1B Business Is Security – Hardware Security Modules HSMsMarvell has multiple significant markets that are often discussed, storage controllers, electro-optical devices, network switching, network processors, and custom silicon for hyperscalers. One market for Marvell that isn’t discussed much is hardware security modules, yet it is likely to be a $1B business for Marvell…Read more4 years ago · 13 likes · Dylan Patel](https://www.semianalysis.com/p/marvells-next-1b-business-is-security?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

这一代 DPU 相当全能。Marvell 采用 Arm 的 N2 核心，加上自研的 5G、机器学习、密码学、虚拟化、包处理加速器以及强大的以太网能力，使其拥有合适的 IP，能把面向基础设施优化的 DPU 送进众多市场。

此外，他们在这个领域叠了多款产品：已为该市场流片了 4 款不同的裸片，而其他每家厂商都只流片了 1 款。这让 Marvell 能覆盖广泛得多的用例。CN102 根据配置不同有 16 到 24 个核心，另有 6 通道 DDR5、48MB 缓存和 200G 以太网，TDP 仅约 40W。这颗芯片还可以与交换芯片共封装，从而获得近 1Tb 的以太网交换容量。

定位更低的 CN103 和 CN102 芯片瞄准的功耗与性能档位显著更低。此外还有面向 5G 的第 4 条产品线。产品表上还列有一款不同的 DPU400，但它距离产品化还很远——DPU400 的流片时间线更接近明年年中到年底。

这些 DPU 的目标市场包括云数据中心、核心网、边缘数据中心、企业与小型办公室，以及电信网络。具体用例涵盖虚拟防火墙、负载均衡器、网络安全、边缘 vRAN、内容分发网络、通道管理、路由、波束赋形（beamforming）以及 SmartNIC。

Marvell 大谈其支持的开放软件栈，但许多用户对 Marvell DPU 的软件质量感到失望。他们要如何改进软件，值得观察。幻灯片里没有提到 IPDK，但 Marvell 是 OPI 的创始成员，长期会支持 IPDK。

还需要指出的是，在云超大规模 DPU 用例上，AMD 的 Pensando、Intel 的 Mount Evans 和 Amazon 的 Nitro 似乎都已各自找到可以服务的大型公有云（Microsoft、Google、AWS）。Marvell 能否在这里有所斩获，将是一大看点。

关于这个话题的更多内容将在定制芯片部分展开。Marvell 下一代 DPU 的战略要有说服力得多。

他们展示的性能指标大多是 CPU 核心部分与 Intel、Nvidia 竞品 DPU 的对比。Marvell 还将其加密加速器与 Intel Icelake Xeon D 系列的加密加速器作了比较。

# 5G DPU

5G 是 Marvell 正在快速夺取份额的市场。尽管 5G 的炒作周期已跌入谷底，但网络建设远未完成，即便在发达市场也是如此。目前 5G 用户占比约 10%，到 2025 年这一数字将达到 25%，而这 25% 用户产生的流量估计将占到总流量的 45%。

每年部署的宏基站射频单元达 600 万个，专注电信的硅片潜在出货量和销售额可能非常庞大。随着信道带宽从 20MHz 提升到 100MHz、MIMO 从 4x4 提升到 32x32，波束赋形和 L1、L2、L3 处理的计算需求是巨大的。虽然 5G 的炒作周期曾经甚嚣尘上，但未来十年网络的持续升级，终将兑现人们从第一天起就鼓吹 5G 会带来的全部价值。

无线接入网主导着移动通信网络的功耗，因此面向它的加速器至关重要。

目前除 Intel 之外，Marvell 是唯一一家既提供 L1 加速处理、又为 L2/L3 提供强健 CPU 核心和强大网络能力的公司。区别在于 Marvell 的加速是 inline（在线/串联）式的，而非 lookaside（旁路）式。

Inline 加速器集成在主处理路径中，可以随数据流经系统时直接处理。这对某些类型的操作能带来显著加速，但也会增加系统复杂度、限制灵活性。归根结底，这种方式对功耗更友好。

与之对照的是 Intel 当前的方案，采用 lookaside 方式：加速器不集成在主处理路径中，而是由主处理器把数据发给加速器处理，再取回存放在另一块独立内存位置的结果。相比 inline 加速，这种方式的加速幅度和功耗收益没那么大，但更灵活、也更容易实现。值得注意的是，Intel 将在 [Sapphire Rapids EE 中加入 inline 加速，同时借助自定义 CPU 指令保留灵活性](https://www.semianalysis.com/p/how-nvidias-empire-could-be-eroded)。

虽然射频单元的部署数量将会下降，但每个射频单元的硅片用量将急剧上升。随着复杂度提高，射频单元内部承担的处理量相对于分布式单元也会越来越多。

Marvell 还恰好在其定制芯片部门拿下了诺基亚（Nokia）这个客户。如果你五年前留意过新闻，就会记得 Intel 用其不靠谱的 10nm「定制代工」坑死了诺基亚的 Reefshark SoC。诺基亚至今仍未缓过来，但与 Marvell 的合作或许能帮上忙。更多内容见定制芯片部分。

# PHY

PHY 是一类旨在处理网络物理层的集成电路，负责将数字数据转换为可通过通信信道传输的物理形态。以以太网为例，PHY 芯片会把数字数据转换成可在铜线上传输的电信号。

PHY 的形态跨度很大：从驱动直连无源铜缆的片上 PHY，到有源电缆、重定时器（retimer）、PAM4 DSP，再到相干 DSP。

Marvell 的 PHY 业务是其所有业务单元的核心，覆盖定制 ASIC、CXL 芯片组、相干模块、数据中心以太网、汽车以太网、SSD 和 HDD 控制器、PAM4 模块以及 DPU。

Marvell 正在进攻的一个有趣领域是有源电缆（AEC）。直连铜缆是最常见的线缆形态，光互连传统上用于长距离传输，而有源电气电缆在数据中心通信领域仍相对较新。

有源电气电缆内含电子元件，可执行额外功能，例如放大或调理通过线缆传输的电信号。总体而言，有源电气电缆比不含任何内置电子元件的无源电缆更贵，但性能更优、功能更多，同时又比光互连便宜。

Marvell 用其 Alaska AEC 进攻这一市场，对 Credo（$CRDO）来说是非常糟糕的消息。

# 电光连接

PHY 业务和电光连接均来自 Inphi 收购案。Inphi 的成名之作正是 PAM4 信令。

PAM4 是用于以太网等高速通信系统的一种信令技术。PAM 代表脉冲幅度调制（pulse amplitude modulation），PAM4 中的「4」指编码数据所用的电平数。在 PAM4 信令中，数字数据的每一比特由四个不同的幅度电平之一表示，而非传统二进制信令（0 和 1）的两个电平，因此相比传统 NRZ 信令，在给定信道上能传输更多数据。

PAM4 可让每比特数据传输的功耗和成本降低 30%。Marvell 现已出货 800G，其主要市场是 AI 集群。带宽需求总体上每 3 年翻一番，而 AI 正处于其 S 曲线的起点，正在加速推高这些需求。Broadcom 正在该市场发起强有力的竞争，尽管其目前在 400G PAM4 上的份额仍低得多。

Marvell 用一张漂亮的矩阵展示了数据中心内可插拔模块市场的演进。100G 世代基于 4 通道、25G 数据率、每个时钟 2 bit 的 NRZ。200G 转向 PAM4，使每通道的驱动速率翻倍。正是在这个节点，Inphi 的业务腾飞了。由于出众的成本和功耗，Microsoft 成为 Inphi 200G PAM4 的大客户，其他超大规模云厂商很快纷纷跟进。

400G 把数据率翻倍；800G 把通道数翻倍到 8。1.6T 世代尚存争议：一些公司想转向 16 通道，而 Marvell 则力主把 PHY 数据率从 112G PAM4 翻倍到 224G PAM4。Marvell 目前已在向客户送样这款产品。

一个有趣的观察是：Marvell 对外销售 DSP 和 TIA，供他人集成到可插拔收发器中；但在相干光市场，他们卖的主要是自家的可插拔收发器。

# 数据中心交换机

Marvell 最近的一次收购是 Innovium 及其 Teralynx 交换机产品线。Marvell 尽管已有两条交换机产品线，还是收购了第三条。Marvell 的理由是，数据中心交换所需的功能特性与其他市场差异巨大。在数据中心市场，带宽需求正以指数级速度飙升。

超大规模数据中心交换机需要低得多的时延以及用于拥塞管理的高级遥测。Teralynx 自夸拥有数一数二的时延，但我们听到、看到的信息相互矛盾——有资料显示 Broadcom 以及 Nvidia 的 InfiniBand 时延要低得多。

数据中心交换机市场竞争异常激烈：Broadcom 一家独大，Nvidia 凭借 Spectrum-4 以太网和 InfiniBand 强势崛起，Cisco 拼命防守止损，Intel 则对 Tofino 抱有宏大期许。我们对 Marvell Teralynx 能否拿下可观份额持怀疑态度。

雪上加霜的是，Marvell 当前一代交换机仍只支持 12.8T，而 Nvidia 和 Broadcom 已在小批量出货 51.2T。Marvell 打算跳过两代、直奔 51.2T，但其进入 25.6T 和 51.2T 世代的时点显然太晚——甚至比已在出货 25.6T 世代交换机的 Intel 和 Cisco 还要晚。我们的一些信源称，Marvell 在 25.6T 上遭遇了芯片级问题，迫使他们废弃了那版设计。

我们就进军路由芯片业务的可行性询问了 Marvell 的 Nariman Yousefi。Marvell 手握从优秀 PHY 到控制平面、数据平面处理的众多 IP，但他的论点是路由市场规模有限、没有他们的位置。在 Juniper Networks 和 Cisco 自研自用（captive）以及 Broadcom 极具竞争力的芯片之间，Marvell 追逐这个市场确实没什么道理。

[分享](https://newsletter.semianalysis.com/p/marvelldeepdive2022?utm_source=substack&utm_medium=email&utm_content=share&action=share)

**本文的后半部分仅面向订阅者，内容涵盖汽车、存储、与超大规模云厂商的定制芯片合作（包括存储、安全、一颗大型 AI 训练芯片、AI 推理、定制 DPU、定制视频 ASIC）以及 9 条不同的 CXL 产品线。**

**我们还将在仅限订阅者的部分分享我们对 FY2023、FY2024 和 FY2025 的营收和 EPS 预估。**

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

# 汽车

在汽车半导体市场，大多数目光集中在几个主要驱动因素上。其一是功率半导体，碳化硅（SiC）、氮化镓（GaN）乃至 IGBT 占据了话题的中心。其二是 ADAS 和自动驾驶，Mobileye、Nvidia 和 Intel 的芯片主导着讨论。再往深一层，关于传感器的讨论也很热闹，从 CMOS 图像传感器到雷达到激光雷达。但在谈论汽车半导体这一巨型趋势时，供应链中有一个关键环节被许多人忽视了，而 Marvell 或许握有答案。

值得注意的是，大多数汽车 OEM 都希望掌控自己的命运，不愿被锁死在单一平台上。此外，他们还希望能够基于软件实现差异化。虽然并非所有 OEM 都注定成功，但同样重要的是思考他们会把力气花在哪里。正因如此，他们必须依托通用平台，同时还能按自己的意愿加以调整和定制。
