---
title: "CXL 深度解析——可组合服务器架构与异构计算的未来、20 家公司的产品、3.0 标准全览"
title_en: "CXL Deep Dive – Future of Composable Server Architecture and Heterogeneous Compute, Products From 20 Firms, Overview of 3.0 Standard"
subtitle: "20 家公司的未来 CXL 产品盘点"
date: 2022-08-17
source: https://newsletter.semianalysis.com/p/cxl-deep-dive-future-of-composable
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# CXL 深度解析——可组合服务器架构与异构计算的未来、20 家公司的产品、3.0 标准全览

> 原文：[CXL Deep Dive – Future of Composable Server Architecture and Heterogeneous Compute, Products From 20 Firms, Overview of 3.0 Standard](https://newsletter.semianalysis.com/p/cxl-deep-dive-future-of-composable) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**20 家公司的未来 CXL 产品盘点**

Compute Express Link（CXL）的发展势头正达到临界规模——[每一家主要的半导体和数据中心公司都已加入该标准](https://www.computeexpresslink.org/members)，同时第一波第一代设备也即将发布。第三代 Compute Express Link（CXL）规范刚刚发布，它带来了此前版本中所缺失的一些重大变化。本文将讨论可组合服务器架构、异构计算，以及 CXL 标准的 1、2、3 版本。

在本报告的后半部分，我们将做一次状态更新，讨论来自 20 家不同半导体公司、将采用 CXL 的即将推出的产品，涵盖市场机会、时间点和能力。我们认识的最优秀的半导体投资者之一曾说过：准确理解并框定 CXL 对数据中心的影响，将是半导体行业最重要的超额收益（alpha）来源——我们对此深表赞同。这 20 家公司的产品将涵盖 CPU、GPU、加速器、交换机、NIC、DPU、IPU、共封装光学（CPO）、内存扩展器（memory expander）、内存池化器（memory pooler）和内存共享器（memory sharer）。

我们将讨论的公司包括 Intel、AMD、Nvidia、Ayar Labs、HPE、Microsoft、Meta、Google、Alibaba、Ampere Computing、Samsung、SK Hynix、Micron、Rambus、Marvell、Astera Labs、Microchip、Montage Technology、Broadcom 和 Xconn。CXL 联盟成员超过 200 家，但我们认为这些公司拥有最具影响力的产品和 IP。

过去，数据中心芯片的主题主要是打造更强的 CPU 核心和更快的内存。十年前的服务器与今天的服务器看起来大同小异。过去十年间，随着横向扩展（scale-out）和云计算的到来，竞争格局已经改变。[最快的核心不再是首要目标](https://semianalysis.substack.com/p/is-ampere-computings-cloud-native)。焦点在于如何以最具成本效益的方式交付总体计算性能，并把它们全部连接起来。在我们的[先进封装系列](https://semianalysis.substack.com/p/is-ampere-computings-cloud-native)中，我们深入探讨了摩尔定律的放缓以及半导体成本缩微终结带来的影响。

这些趋势都指向计算资源专业化的大潮。收益递减规律的终极例子之一：在通用 CPU 性能上每多投入一个晶体管，所带来的性能增量都在递减。[异构计算称王](https://semianalysis.substack.com/p/advanced-packaging-part-1-pad-limited)——专用 ASIC 在特定任务上可以[以更少的晶体管提供超过 10 倍的性能](https://semianalysis.substack.com/p/meet-netint-the-startup-selling-to)。

为每种工作负载设计具备精确匹配计算资源的专用芯片，成本高得离谱。我们在《[半导体设计复兴的阴暗面](https://semianalysis.substack.com/p/the-dark-side-of-the-semiconductor)》一文中探讨过这个观点。简言之，由于光罩套数成本、验证与确认成本，芯片设计的固定成本正在飙升。

与其为整套工作负载设计芯片，不如为各类计算设计芯片，再按特定工作负载的需要以任意配置把它们连接起来，这样成本效益会高得多。

> 用单独封装、相互互连的更小功能模块来构建大型系统，可能被证明更为经济。大功能模块的可用性，结合功能化设计与构建，应当能让大型系统的制造商快速且经济地设计和制造出种类相当繁多的设备。
>
> Dr. Gordon Moore 在预言「摩尔定律」的原始论文中——《Cramming more components onto integrated circuits》——1965 年

系统构建方式的这种转变，将计算单元从单颗芯片或单台服务器提升到了整个数据中心。

> 数据中心就是新的计算单元。
>
> Jensen Huang

服务器内部的芯片互连通常采用 PCI Express。其最大的缺陷是该标准缺少[缓存一致性](https://en.wikipedia.org/wiki/Cache_coherence)和[内存一致性](https://en.wikipedia.org/wiki/Memory_coherence)。这两个概念的非技术类比是：把服务器想象成一个邮局。信件异步到达，而新信息的到来往往比含有原始信息的信件晚好几天，使后者过时。一致性机制帮助管理和拉平这种状况。

采用 PCI Express 时，从性能和软件角度看，不同设备之间通信的开销都相对较高。此外，连接多台服务器通常意味着使用以太网或 InfiniBand。这些通信方式存在同样的所有问题，而且延迟更糟、带宽更低。

2018 年，IBM 和 Nvidia 凭借 NVLink 为 PCI Express 的这些缺陷带来了解决方案，将其注入了当时全球最快的超级计算机 [Summit](https://www.olcf.ornl.gov/wp-content/uploads/2018/05/Intro_Summit_System_Overview.pdf)。AMD 在 [Frontier 超级计算机](https://smc.ornl.gov/wp-content/uploads/2019/09/Geist-presentation-2019.pdf)中有一个类似的专有方案，称为 Infinity Fabric。这些专有协议周围无法形成产业生态。2010 年代中期，CCIX 曾作为一个潜在的行业标准出现，但尽管有 AMD、Xilinx、华为、Arm 和 Ampere Computing 的支持，它因缺乏产业支持的临界规模而始终未能起飞。

Intel 拥有超过 90% 的 CPU 市场份额，没有他们的加入，任何方案都行不通。Intel 当时正在开发自己的标准，并于 2019 年将他们的专有规范作为 Compute Express Link（CXL）1.0 捐赠给了新成立的 CXL 联盟。该标准获得了半导体行业大多数最大买家的同时认可。CXL 沿用了 PCIe 5.0 的现有生态，使用其物理层和电气层，但协议层得到改进，为 load-store 内存事务增加了一致性和低延迟模式。

CXL 让向异构计算的转型成为可能，因为它建立了一个获得行业内大多数主要玩家支持的行业标准协议。现在，业界拥有了一个把这些各式芯片连接起来的标准互连。

AMD 的 Genoa 和 Intel 的 Sapphire Rapids 将于 2022 年底/2023 年初支持 CXL 1.1。CXL 1.1 带来三类支持：CXL.io、CXL.cache 和 CXL.mem。CXL.io 可以理解为标准 PCIe 的类似但改进的版本。CXL.cache 允许 CXL 设备一致地访问并缓存主机 CPU 的内存。CXL.mem 允许主机 CPU 一致地访问设备的内存。更详细的解释见下方要点。大多数 CXL 设备将组合使用 CXL.io、CXL.cache 和 CXL.mem。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/b956a77c-ba15-4e39-a8d1-a510beaf54b4_1536x814.jpeg)

###### ·         CXL.io 是用于初始化、链路建立、设备发现与枚举以及寄存器访问的协议。它为 I/O 设备提供接口，类似于 PCIe Gen5。同时，CXL 设备必须支持 CXL.io。

###### ·         CXL.cache 是定义主机（通常是 CPU）与设备（如 CXL 内存模块或加速器）之间交互的协议。它使挂载的 CXL 设备能够因其本地副本的安全使用而以低延迟缓存主机内存。可以把它想象成 GPU 直接从 CPU 的内存中缓存数据。

###### ·         CXL.memory / CXL.mem 是为宿主处理器（通常是 CPU）提供使用 load/store 命令直接访问设备挂载内存的能力的协议。可以把它想象成 CPU 使用一个专用存储级内存设备，或使用 GPU/加速器设备上的内存。

到目前为止，我们谈论的主要是异构计算，但 CXL 真正的杀手锏在于内存。过去我们曾在解释 [Marvell 收购 Tanzanite Silicon 以及 Astera Labs 和 Rambus 在内存加速器领域的竞争](https://semianalysis.substack.com/p/marvell-acquires-tanzanite-silicon?s=w)的文章中讨论过这一点。我们在[对 Microsoft 内存池化方案的深入分析](https://semianalysis.substack.com/p/cxl-enables-microsoft-azure-to-cut)中进一步展开了这个想法。我们将在本文中做更详细的综述。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/cc8ca0ad-b4d7-4df2-9501-f1507120a75f_1510x800.png)

数据中心存在巨大的内存问题。自 2012 年以来，CPU 核心数快速增长，但每核内存带宽和容量并未相应增长。每核内存带宽自 2012 年以来甚至有所下降，且这一趋势未来还将持续。此外，直挂（direct-attached）DRAM 与 SSD 之间存在巨大的延迟和成本鸿沟。最后，昂贵的内存资源往往利用率很差——这是致命的。低利用率对任何资本密集型行业都是重大拖累，而数据中心业务是全世界资本密集度最高的行业之一。

[Microsoft 表示，服务器总成本的 50% 仅来自 DRAM](https://semianalysis.substack.com/p/cxl-enables-microsoft-azure-to-cut)。尽管 DRAM 成本巨大，但其 DRAM 内存中[高达 25% 处于闲置搁浅状态](https://semianalysis.substack.com/p/cxl-enables-microsoft-azure-to-cut)！简单来说，Microsoft Azure 服务器总成本中的 12.5% 什么也没干。

设想一下，如果这些内存不是守在每个 CPU 身边，而是放在一张互联的网络上，可以跨多颗 CPU、多台服务器动态分配给虚拟机，会怎么样？内存带宽可以根据工作负载的需求伸缩。这将大幅提升利用率。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/7307a123-3511-4766-a420-7623e5e09075_3171x1011.png)

这一概念不仅限于内存，也适用于一切形式的计算和网络资源。可组合服务器架构，就是把服务器拆解成各种组件，再分组放置，使这些资源可以被动态地、即时地分配给工作负载。

数据中心机柜成为计算单元。客户可以为其特定任务选择任意数量的核心、内存和 AI 处理性能。或者更好的是，Google、Microsoft、Amazon 等云服务商可以根据客户运行的工作负载类型任意分配资源，并只按实际使用量向客户收费。

这一愿景是服务器设计和云计算的圣杯。与之相关的工程难题众多，其中许多围绕[构建连接一切的网络](https://semianalysis.substack.com/p/ayar-labs-co-packaged-optics-revolution)的延迟和成本。这些必须审慎检验，但协议必须先行——这正是 CXL 2.0 和 3.0 带来的东西。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/963b9999-15fe-48ba-a329-e74187feb6bb_3001x664.png)

CXL 2.0 的主打特性是支持内存池化和交换。CXL 交换机可以连接多个主机和设备，使 CXL 网络上可连接的设备数量大幅增长。新的多逻辑设备（multiple logical devices）特性允许多个主机和设备全部互连并相互通信，而无需历史上强制要求的主从关系。这张资源网络将由 fabric manager（结构管理器）编排——这是一个用于控制和管理该系统的标准 API。细粒度资源分配、热插拔和动态容量扩展，使硬件可以在无需任何重启的情况下被动态分配并在不同主机之间迁移。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/e4915cd2-cec6-400d-b3f4-5f68811763a0_1067x805.png)

一图胜千言，我们来讨论一下上图。多个主机可以连接到交换机。交换机再连接到各种设备——SLD（single logical device，单逻辑设备）或 MLD（multiple logical devices，多逻辑设备）。MLD 的设计就是为连接多个主机以实现内存池化。

MLD 会以多个 SLD 的形式呈现。这使它们能在主机之间池化内存，甚至池化加速器计算资源。FM（fabric manager）位于控制平面。它是编排者，负责分配内存和设备。fabric manager 可以放在一颗单独的芯片上或放在交换机里；它不需要高性能，因为它从不触碰数据平面。如果 CXL 设备本身是多头的（multi-headed）并连接到多个主机的根端口，不使用交换机也能实现同样的效果。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/29f7f564-758e-4433-8cca-bd956f304a18_841x756.png)

综合来看，Microsoft 演示过[通过 DRAM 池化减少 10% 的 DRAM 部署量、节省 5% 的服务器总成本](https://semianalysis.substack.com/p/cxl-enables-microsoft-azure-to-cut)的潜力。这还是在第一代 CXL 方案上、未使用 CXL 交换机的情况下实现的。

CXL 3.0 带来了更多改进，有助于进一步扩展构建异构可组合服务器架构的能力。其主要焦点是把 CXL 从服务器尺度扩展到机柜尺度。这是通过从主机-设备模型转向让 CPU 只是网络上的另一种设备来实现的。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8dce0af4-3537-4b5c-86dd-1c5d4eada152_3013x1549.png)

CXL 交换机如今可以支持多种拓扑。此前在 CXL 2.0 中，只有面向 CXL.mem 设备的扇出（fan-out）一种。现在，一个机柜乃至多个机柜的服务器可以用 leaf-spine 或全互联（all-to-all）拓扑组网。CXL 3.0 下设备/主机/交换机/交换机端口的理论上限是 4,096。这些变化把 CXL 网络的潜在规模从几台服务器急剧扩展到许多机柜的服务器。

此外，各种类型的多个设备可以挂在主机的单个 CXL 根端口下。这在以前是一个重大限制，因为单个根端口只能寻址单一设备类型。如果一台主机用单个 CXL 根端口连接到交换机，那台主机就只能访问挂在该交换机下的一种设备类型。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ea431bf6-0610-4574-a47a-ce2052936146_3024x1531.png)

CXL 3.0 中最重要的变化是内存共享和设备间通信。主机 CPU 和设备如今可以在同一数据集上协同工作，无需无谓地搬运和复制数据。一个例子是 Google 和 Meta 等巨头采用的数十亿参数深度学习推荐系统这类常见 AI 工作负载。相同的模型数据被复制到许多服务器上。用户请求到来，推理运算随之运行。如果存在 CXL 3.0 内存共享，一个大型 AI 模型可以驻留在少数几个中央内存设备上，由许多其他设备来访问。这个模型可以用实时用户数据持续训练，更新可以通过 CXL 交换网络推送出去。这最多可以把 DRAM 成本降低一个数量级，并同时提升性能。

内存共享能够改善性能和经济性的领域几乎无穷无尽。第一代内存池化可以减少 10% 的总 DRAM 需求。更低延迟的内存池化可以在多租户云中带来约 23% 的节省。内存共享则可以把 DRAM 需求减少超过 35%。这些节省折合到数据中心 DRAM 年支出上，是每年数十亿美元的量级。

如果你喜欢我们的内容，请分享！帮忙传播！

[分享](https://newsletter.semianalysis.com/p/cxl-deep-dive-future-of-composable?utm_source=substack&utm_medium=email&utm_content=share&action=share)

# **CXL 的用途**

在本报告的后半部分，我们来谈谈 20 家公司在 CXL 上的产品、时间点和战略，涵盖交换机、NIC、DPU、IPU、共封装光学（CPO）、内存扩展器、内存池化器、内存共享器、CPU、GPU 和加速器。

仅在订阅者部分讨论的公司包括 Intel、AMD、Nvidia、Ayar Labs、HPE、Microsoft、Meta、Google、Alibaba、Ampere Computing、Samsung、SK Hynix、Micron、Rambus、Marvell、Astera Labs、Microchip、Montage Technology、Broadcom 和 Xconn。在这一部分，我们主要讨论封装外（off-package）能力，封装内（on-package）互连将在此后一篇关于 UCIe 的文章中单独讨论。

[分享](https://newsletter.semianalysis.com/p/cxl-deep-dive-future-of-composable?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
