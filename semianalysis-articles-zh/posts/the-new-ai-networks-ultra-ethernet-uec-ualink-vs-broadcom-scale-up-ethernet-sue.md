---
title: "新一代 AI 网络 | Ultra Ethernet（UEC）| UALink 对阵 Broadcom 纵向扩展以太网 SUE"
title_en: "The New AI Networks | Ultra Ethernet UEC | UALink vs Broadcom Scale Up Ethernet SUE"
subtitle: "LibFabric、包喷洒、rail 优化、拥塞控制、ECN、ACK、流控、PFC、UEC 面临的挑战"
date: 2025-06-11
source: https://newsletter.semianalysis.com/p/the-new-ai-networks-ultra-ethernet-uec-ualink-vs-broadcom-scale-up-ethernet-sue
crawled: 2026-09-15
authors: ["Tanj Bennett", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 新一代 AI 网络 | Ultra Ethernet（UEC）| UALink 对阵 Broadcom 纵向扩展以太网 SUE

> 原文：[The New AI Networks | Ultra Ethernet UEC | UALink vs Broadcom Scale Up Ethernet SUE](https://newsletter.semianalysis.com/p/the-new-ai-networks-ultra-ethernet-uec-ualink-vs-broadcom-scale-up-ethernet-sue) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**LibFabric、包喷洒、rail 优化、拥塞控制、ECN、ACK、流控、PFC、UEC 面临的挑战**

SemiAnalysis 订阅用户可获得本文的音频朗读版。

在生成式 AI 热潮初期，标准以太网最初输给了 Nvidia 的 InfiniBand，丢掉了可观的市场份额。此后，以太网开始逐步夺回份额，主要驱动力是成本、InfiniBand 的种种缺陷，以及在以太网之上叠加更多特性与定制化的能力。

Amazon 和 Google 的内部以太网实现已经填补了相当大一部分性能差距（尽管与基于 Nvidia 的网络相比仍然远远落后）。此外，Oracle 和 Meta 等公司已在以太网之上重金投入构建，与 Nvidia 的差距并不算大。

连 Nvidia 自己也认可以太网的统治地位：在 Blackwell 一代，Spectrum-X 以太网的出货量已大幅超过他们自己的 Quantum InfiniBand。总体而言，若不投入大量精力打造专有实现，标准以太网在性能上仍远远落后。

这正是 Ultra Ethernet Consortium（超以太网联盟）登场的意义所在：为大型 AI 网络标准化诸多改进，并把所有重量级玩家聚合成一个庞大的联盟。

## **Ultra Ethernet Consortium 候选发布版 1（Release Candidate 1）：深度评述**

Ultra Ethernet Consortium（UEC）的候选发布版 1（Release Candidate 1）是一份分量十足的文件，[共 565 页，今日公开发布](https://ultraethernet.org/wp-content/uploads/sites/20/2025/06/UE-Specification-6.11.25.pdf)。这与以简洁为优先的 Ultra Accelerator Link v1 规范形成鲜明对比。UEC 从本质上说就不简单；直接通读几乎如坠云雾。不过，采用结构化的方法可以揭示其内在逻辑。

![](https://substack-post-media.s3.amazonaws.com/public/images/552392af-1423-4473-a26f-e14b286a0bd6_361x825.png)
*来源：UEC Alliance——Ultra Ethernet Consortium*

UEC 项目旨在为以太网 NIC 和交换机提供传输层与流控层，从而改善其在大型、高速数据中心网络中的运行。传输层是确保用户内容从源头到达目的地的那一层，并承载现代 AI 或 HPC 用户所期望的全部命令。流控确保数据以尽可能快的速度流动，防止网络拥塞，并在故障或慢速链路周围重路由。要实现这一切，网卡（NIC）必须实现 UEC。交换机则是可选的，网络部分可以沿用现有的以太网交换机。UEC 规范编写得细致入微，以确保不同厂商的设备能够互操作。

## UEC **背景与核心模块**

UEC 在 Linux 联合开发基金会（JDF）之下运作，履行标准开发组织（SDO）的职能。以太网是 UEC 赖以立足的基础，但 UEC 还以若干其他规范或行业经验作为构建模块。它被设计为一种本地网络，目标是在集群内实现 1 到 20 微秒的往返时延，明确瞄准数据中心。其首要目标是为 AI 训练、AI 推理和高性能计算（HPC）优化横向扩展网络。该规范强制要求网络 PHY 使用以太网标准，并要求交换机具备现代以太网特性。

一个关键的构建模块是 Open Fabric Interfaces，又称 [LibFabric](https://ofiwg.github.io/libfabric/)。理解了 LibFabric，就等于解锁了 UEC 规范的前 120 页。LibFabric 是一套已被广泛采纳的 API，将 NIC 的使用方式标准化。现有的绑定或插件把 LibFabric 接到高性能网络库上，例如 NCCL（Nvidia 出品）、RCCL（AMD 出品）、MPI（超级计算并行通信的鼻祖）、SHMEM（共享内存）和 UD（不可靠数据报）——这些正是 AI 或 HPC 超级集群所需的网络风格。

![](https://substack-post-media.s3.amazonaws.com/public/images/c5b3593e-5ae4-4f73-aee3-294f814b06ec_891x426.png)
*来源：OFI——https://ofiwg.github.io/libfabric/——UEC 是 OFI 的 provider，即一块带加速的 NIC。*

UEC 并非全然的全新发明。它构建在一个成熟的开放标准之上，为其运行定义了可互操作的框架。互操作性显然是核心关切，因为 UEC 对 API 如何与 CPU 或 GPU 配合没有施加任何约束。LibFabric 围绕用于数据发送、接收和特殊值的命令队列，以及完成事件（completion）展开。这种基于队列的 NIC 交互方式已经标准化了 40 多年。UEC 并不规定这些队列如何用你的 GPU 或 CPU 来构建，但强制要求支持全部 LibFabric 命令：发送、接收、RDMA、原子操作和特殊命令。超过 100 页的篇幅详细规定了这些命令如何封装进消息头，以确保在不同厂商的 NIC 之间兼容执行。这实际上把 LibFabric 从 CPU/GPU 上的软件栈，转变为 NIC 上的一套硬件加速命令集。

![](https://substack-post-media.s3.amazonaws.com/public/images/60a18744-ad60-4300-be99-d19cba6f0dfa_450x301.png)
*来源：AMD——AMD 是有望在 UEC 网络上实现互操作的众多支持者之一*

从 LibFabric 借鉴并融入 UEC 的一个关键概念是"Job"（作业）。Job 表示分布在多个端点上的一组协作进程。它在功能上类似 VXLAN，但使用的是 UEC NIC 内部的 Fabric 端点（FEP），而非以太网的 VXLAN。一块 NIC 可以承载多个 FEP，但每个 FEP 只归属一个 Job，只能与共享同一 JobID 的其他 FEP 交互。一个受信任的 fabric 服务负责管理这些 Job 及其关联 FEP 的创建与终止。Job 还可以包含加密域，提供安全的流量隔离。规范还为成员资格灵活可变的 Job 预留了条款，以适应动态服务环境。这些 LibFabric 概念与命令都是强制组件。

接下来，UE 传输层（UE Transport Layer）负责把 LibFabric 命令和数据内容交付给 FEP，可以走纯以太网，但最好获得可选层的支持。

## **包层（Packet Layer）：第 3.2 节**

规范真正变得有趣的是第 3.2 节，它详细规定了包层。虽然没有明确致谢，但这一层显然大量借鉴了各厂商在模块化交换机上的丰富经验。它把 LibFabric 消息切分成更小的包并灵活路由，并显式考虑了可靠性与流控。UEC 的一个既定目标是把这些功能整合进传输层。数据中心的时延低到必须依靠硬件加速的差错恢复和流控，才能获得最佳、最平滑的流量。包引入了额外的头部，但便于 NIC 与交换机之间独立于消息流交换网络运行信息。在模块化交换机中，这由第二层内部交换机通过包来处理；而 UEC 依靠 NIC 生成带有增强流控的包，由增强型以太网承载。

UEC 明确为"胖"（fat）网络而设计，其特征是 FEP 之间存在多条等距、等速的路径。一种常见的现代实现是"rail"（轨道）配置。在 UEC 网络中，这可能意味着一块 NIC 拥有例如由 8 条 100Gbps lane 组成的 800GbE 接口。在交换机机柜侧，这 8 条 lane 分别连到不同的交换机，比如 8 台交换机、每台 512 个 100G 端口。这样最多可以有 512 个 FEP 连接到这 8 个端口。UEC NIC 的设计是把消息"喷洒"（spray）到全部 8 条 lane 上，做法是分配一个"entropy"（熵）编号，在路径上每个输出 lane 的选择点对 lane 分配做哈希。发送方选择 entropy 值来平衡各条路径的使用，以填满完整的 800 Gbps 吞吐。关键是，CPU 或 GPU 应用对这种复杂度毫无感知；它们只是通过 LibFabric 把消息入队，NIC 负责搞定"rail 的魔法"。

![](https://substack-post-media.s3.amazonaws.com/public/images/b5ef2118-f658-41ca-9545-cd6ab2c9dbed_2560x925.png)
*双 rail 示例：粉色列（Pink Rail）与黄色列（Yellow Rail）网络拓扑相同。来源：SemiAnalysis*

rail 的魔法让 512 端口交换机（当前的热门选择）能够以相同拓扑并行使用，从而获得数倍的吞吐收益。最大的进步在于：各端点由单块 NIC 内的 UEC 协调，因此主机看到的是大吞吐，而 NIC 把流量分发到所有路径上。交换机的大端口数（radix）对构建大型集群极其宝贵，而拓扑一致则简化了网络的构建与管理。UEC NIC 的设计能够处理路由，甚至穿越多层交换机。额外的好处是，多路径上的包让 UEC NIC 能够提供极快的丢包替换和超快流控，即使在欠优的应用调度或偶发的网络链路抖动下也能保证流量平滑。

第 3 节到 3.4 节用大量篇幅详细规定了包与包头的构造，与 LibFabric 语义有一定关联。包头可能相当可观，最大可达 44 字节，不过针对频繁短包优化的包头可以小到 20 字节。按 UEC lane 最慢的预期速率 100Gbps 计算，20 字节——160 比特——折合约 1.6ns。虽然 UEC 的最大吞吐会低于裸以太网的理论最大值——模块化交换机通常用稍快的背板来吸收包开销——UEC 的以太网本身就充当背板，因此用户数据速率会略慢。这种折换换来的是近乎完美的流量，通常反而能提升实际数据速率。

第 3.5 节（第 219 页！）深入包操作的具体细节。与命令和队列部分不同，这是 UEC 独有的内容。它看起来规定得很全面，明显借力了模块化交换机的经验，但没有给出任何外部参考，表明这是一种共识设计，而非从任何单一市场方案派生而来。这也说得通：UEC 依赖以太网充当背板，而现代模块化交换机使用的是专有背板。

连接即时建立，没有 ACK（确认收到的应答）开销，因为消息已被切分成包。虽然同一条消息的所有包走同一条选定的 lane（便于修复和重组），但消息本身可以而且将会被喷洒到不同的 lane 上。lane 的选择由包头中的一个"entropy"值（与真正的熵无关）引导，它代表路由选择，并带有相应的流控。

启用加密后，建立包连接会有一些开销（一次强制性的往返 ACK）。真实世界的性能将需要带加密进行基准测试。希望这一代价不会太大。

丢包通过序列号来推断，并通过特定请求补发——在预期丢包率极低的数据中心里（否则就存在更大的系统性问题），这是明智的做法。

## **拥塞控制：UEC-CC（第 3.6 节）**

第 3.6 节介绍 UEC-CC，即拥塞管理系统——它是可选的，但也是人们想要 UEC 的核心原因。这里的设计选择是明智的。UEC-CC 采用基于时间的机制，渡越时间精度优于 500ns。前向路径和反向路径独立测量，这暗示 NIC 之间在绝对时间上同步，尽管规范并未明说。双向测量可以把拥塞准确地归因到发送方和接收方。若启用 UEC-CC，交换机被要求使用 ECN（显式拥塞通知），并且预期使用现代的 ECN 变体：拥塞标志按流量类别（traffic class）置位，并在包发送前即时测量。这提供了最新的拥塞信息和按流量类别的差异化处理。在严重拥塞时，包可以被裁剪（trim），只留下一个"墓碑"包头，向接收 NIC 明确传达坏消息——单纯丢包反而会拖慢纠正动作。

这一机制至关重要，因为接收 FEP（每块 NIC 一个或多个）负责给发送方定步（pacing）。数据中心往返时间（RTT）只有几微秒，发送方在未收到 ACK 之前能够发送的数据窗口非常短。接收方决定授予多少新包，使发送方能在微秒级被暂停，从而大体上避免丢包。接收方从分布于多条 lane 和多个流量类别的 ECN 标志中收集丰富的流量状况信息，这使其既握有各自的信用（credit）计数，也掌握所有到达流量的全局视图。它通过 ACK 和一条特殊的 Credit CP 命令把自己的决策传达给发送方。

![](https://substack-post-media.s3.amazonaws.com/public/images/3b7e8e8a-f955-4ac8-9b7c-85b5d0b22f10_2560x754.png)
*多层网络下端点之间的流控。来源：SemiAnalysis*

这些决策还能够通过调整特定的"entropy 容量"来重新平衡路由，从而改变消息喷洒所用的均衡。UEC 对（前向）纠错率和丢包率标准化了某种程度的报告，能够检测出使用弱链路的特定 entropy，并重路由流量绕开它。Entropy 在每台交换机上对跳选择做哈希，预计 entropy 的数量会比 lane 多出一个数量级，因此可以把弱链路隔离出来，而对整体路由容量的影响极小。

至关重要的是，UEC-CC 废弃了一些流控方法。被广泛使用的老方法 RoCE 和 DCQCN 会劣化 UEC-CC 的性能，因为与 UEC-CC 不同，它们不会把流控直接更新到流问题实际发生的位置。PFC（优先级流控）是不必要的，在交换机之间必须禁用，因为它可能阻塞合法的流量。在 NIC 连接交换机之处 PFC 也被弃用，因为它缺乏 UEC-CC 的精度，可能过度削减流量。基于信用的流控（CBFC）由于会干扰 UEC-CC，同样被弃用。

## **传输安全子层（第 3.7 节）**

第 3.7 节"传输安全子层"技术性极强，而且看起来非常专业。它大量借鉴了经过验证的方法，同时融入了有用的更新。推荐的加密算法是一种后量子的 DES 密码。规范对防御性操作给予高度重视，规定了定期更换 nonce 的规则。加密按域（domain）分配——域是 Job 内 FEP 的一个子集——包括一种支持客户端动态加入和离开的自适应域变体。一套巧妙的密钥派生方案允许整个域使用单一密钥，同时每条流使用不同的密钥和 nonce，而占用的表项空间极小（一个 Job 可以有数万个端点）。

数据中心 fabric 必须包含可信组件：一个负责建立域的安全域管理实体（Secure Domain Management Entity），以及 NIC 中为其入域端口内建的可信硬件。虽然对这些组件版本的验证与证明（attestation）超出了 UEC 规范的范围，但已有开放标准，可以要求厂商予以支持。

第 3.8 节为第 3.7 节提供了一份有用的参考文献清单。

## **其他各层**

第 4 节 UE 网络层（UE Network Layer）主要讨论包裁剪，这是拥塞控制的一个可选特性。

第 5 节 UE 链路层（UE Link Layer）旨在通过链路级包替换和交换机间流控来提升整体性能。在我看来，这是没有正当理由的复杂度，尤其考虑到 CBFC（该层实现的正是它）已在 UEC-CC 一节中被弃用。在一个往返时间为微秒级、接收端 FEP 能凭全局流量信息做出高质量流控决策、丢包罕见且 UEC 已能在补发调度期间绕流而行的数据中心里（第 6 节对此也有帮助！），规范的这一部分似乎是徒增复杂度而没有相应的价值。好在这一层是可选的，我敢打赌它永远不会被广泛使用。它肯定会让测试和 plugfest（多厂商互操作测试大会）变得更复杂。

第 6 节 UE 物理层（UE Physical Layer）主要推荐多条 100Gb 以太网 lane，遵循 802.3/db/ck/df 规范。文中简短致歉称，由于 200Gb 尚未正式标准化而无法引用。UALink 规范引用 200Gb 毫无障碍，而风向已然如此。UEC 应当瞄准从 200Gb 起步，而不仅仅是最终抵达那里。

第 6.3 节探讨利用 FEC（前向纠错）遥测来监控和估计链路级可靠性。虽然这对任何网络爱好者都极具吸引力，但要点很简单：FEC 极其有效，使得在正确初始化的数据中心链路上，丢包成为极其罕见的事件。很高兴看到它被写进规范。

## **UEC：关键优势**

总而言之，采用 UEC 的令人信服的理由包括：

- 硬件加速的 LibFabric。
- 与现代加密集成良好、设计出色的 Job 结构。
- 实现正确的数据中心拥塞控制。
- 消除问题多多的 RoCE 和 DCQCN。
- 现成的 CCL、MPI、SHMEM 和 UD 开源插件。

## **UEC：注意事项**

值得注意的是，为使用 LibFabric 的 Amazon EFA 网络提供插件支持，历来并不轻松。虽然插件配置是现成的，但 Nvidia 的立场往往是不予支持——它尽管支持底层接口，却更偏爱自己的专有方案。虽然据报告该插件能从 EFA NIC 获得良好的性能，但它在较新的 UEC NIC 上的表现仍有待观察。

通用互操作性必须加以检验，不仅要看"能不能跑通"，还要看当端点来自不同厂商时性能是否依然坚挺。同样值得观察的是，当中间的网络不是 UEC 时，UEC NIC 的表现如何——只要你确保交换机确实支持 UEC 所使用和依赖的特性，比如最佳实践的 ECN 生成。

## **与 UALink 和 SUE 的对比**

Ultra-Accelerator Link 的规范篇幅不到 UEC 的一半，尽管编写得同样用心。Broadcom 的纵向扩展以太网（Scale-Up Ethernet）描述认真但非正式，只有区区 20 页，并且想当然地认为它所描述的东西简单明了。

![](https://substack-post-media.s3.amazonaws.com/public/images/804d9545-92ab-49ee-923f-136942e59a9a_885x604.png)
*来源：AMD/UALink——Ultra Accelerator Link 聚焦中间层*

UALink 和 SUE 都只聚焦纵向扩展（ScaleUp），类似于 Nvidia 的 NVLink。它们都只支持单一交换机层，端口数（radix）最多 1024（即 GPU 或 xPU 的数量）。这比 UEC 的目标——多层交换机、数万端点的横向扩展网络——要受限得多。三份规范都假设 AI 或 HPC 集群采用使交换机端口数最大化的 rail 网络。

![](https://substack-post-media.s3.amazonaws.com/public/images/cccf2891-d743-45e0-b3cc-5853fbbacb27_1092x460.png)
*来源：Broadcom——SUE（Broadcom 方案）瞄准单层 rail 交换网络*

SUE 和 UALink 都在各自的规范中放心地引用 200GbE 链路，这让 UEC 显得有些落后于形势。

UALink 与 UEC 一样，会把流量喷洒到各条 rail 上。UALink 明确详述了一种基于信用的流控。SUE 则相反，把这一点往后推，建议在客户端软件的辅助下在以太网内实现——规范更简单，实际效果大体相同。UALink 把 4 条 lane 绑定在一起（例如 4x200）以加快消息传输，而 SUE 和 UEC 似乎都认定 200G lane 已经足够快。这是 UALink 多出的一处复杂度，价值似乎有限。

SUE 建议由以太网通过 PFC、或者更好的是基于信用的流控（CBFC）来处理流控。鉴于在单一交换机层级上 PFC 大体有效，而 CBFC 能带来更平滑的运行，这种做法应该是可行的。

UALink 为连接实现了加密。SUE 则更简单，声明可靠性、数据完整性和加密应由以太网提供。

SUE 把跨 rail 的消息喷洒和负载均衡下放给端点内的软件层。对专精此类软件的公司来说，这是明确的利好。

SUE 和 UALink 都提供内存映射接口。两份规范都没有规定内存映射的实现方式，但都预期通过读写对应大型虚拟系统中另一个端点的内存地址来收发消息。它们的效率应当与 NVLink 相当，但将需要插件或新的底层代码，因为它们没有照搬 NVLink 的包格式。

## 内存映射与主机 fabric

内存映射（memory-mapped）常被冠以"内存语义"之名。映射——用一个巨大的虚拟地址空间为每台主机分配其独有的可识别地址区间——让主机处理器可以使用读写指令，即内存**操作**。但它并不包含内存**语义**，比如定序（ordering）与一致性（coherency）。这里没有发生内存窥探（snooping），也不会围绕集群巧妙地更新缓存。

对于包括 UEC 在内的所有这些系统而言，数据中心中的运行速度和低时延正把端点推向主机芯片 fabric 上的协处理器位置，而不是被一条日益落伍的"IO 总线"隔着老远。这更像是端点（NIC）只是多核系统里的又一个核心。这简化了从计算核心（流式 GPU 或传统 CPU）发出命令、以及端点与主机内存交互之间的高效协作。

我们可以预期 SUE 和 UALink 会以 IP 模块的形态集成进主机芯片，而不是以独立芯片的形态出现。NVLink 早已是这种形态，Intel Gaudi 3、Microsoft Maia 100 这类芯片也在用以太网链路做同样的事情。这简化了 IP 模块，但也**要求**它们保持简单，以缩小在主机芯片中的占位。UEC 的复杂度可能会以独立 NIC 的形态落地，但集成进主机 fabric 应该也为期不远。也许会以小芯片（chiplet）的形式？

## 结论与要点
