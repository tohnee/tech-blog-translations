---
title: "Meta 的基础设施团队需要一场文化重置"
title_en: "Meta's Infrastructure Team Needs A Culture Reset"
subtitle: "Meta 基础设施部门已经变得臃肿，中层管理者把资源耗费在过度工程化的技术方案上，忽视了更广泛的组织需求。"
date: 2026-07-22
source: https://newsletter.semianalysis.com/p/metas-infrastructure-team-needs-a
crawled: 2026-09-15
authors: ["Wayne Ma", "Myron Xie", "Julien Martin-Prin", "Daniel Nishball", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Meta 的基础设施团队需要一场文化重置

> 原文：[Meta's Infrastructure Team Needs A Culture Reset](https://newsletter.semianalysis.com/p/metas-infrastructure-team-needs-a) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Meta 基础设施部门已经变得臃肿，中层管理者把资源耗费在过度工程化的技术方案上，忽视了更广泛的组织需求。**

在我们[近期关于 Meta Superintelligence 的通讯文章](https://newsletter.semianalysis.com/p/the-future-of-meta-superintelligence)中，我们表达了看好 Meta AI 的理由。MSL 如今已具备追赶 Anthropic 和 OpenAI、重返前沿所需的诸多正确要素。不过，我们也简要点到了困扰 Meta 基础设施团队的文化问题。本文将深入探讨这些文化问题如何演变成代价高昂的失误——无论是 Rivos 这样的收购，还是硬件架构上的奇怪选择。

我们认为，Meta 基础设施部门需要一场文化重置，以更好地服务 Meta AI 组织，尤其是 MSL 的那些世界级研究员。随着 [Meta 走上向外部客户出售算力的道路](https://newsletter.semianalysis.com/p/meta-compute-everyone-wants-to-be)，而不仅仅是服务无从选择的内部用户，这一点变得更加重要。

Meta 基础设施部门已经变得臃肿，中层管理者把资源耗费在过度工程化的技术方案上，忽视了更广泛的组织需求。这家公司似乎背负着太多彼此割裂的团体，它们为某些指标过度优化，而不是为整个公司交付可用的技术。中层管理者会不惜一切代价论证自己的提案以保住自己在 Meta 的位置——Meta 已经变成一个政治化极其严重的组织。

一个大问题是 Meta 的六个月绩效评估周期，每轮评估都会淘汰末位 10% 到 15%。其结果是一个由追求短期胜利而非长期战略的员工构成的组织。一些管理者力推那些能快速交付、高曝光度的项目——这种做法被称为「刷窗户」（window washing）——然后迅速转向或干脆弃之不顾。几乎没有人公开挑战领导层，导致糟糕的决策得不到纠正。整套体系抑制长期思考，助长规避风险的行为。

在 Meta 基础设施部门内部，供应链团队对工程团队几乎没有发言权。其结果是，技术决策由政治动机驱动，而不是为整个公司做深思熟虑的软硬件协同设计。

频繁掉头（pivot）也很常见。而且由于 Meta 有「用钱砸问题」、高速执行的名声，这些 U 形转弯最终比那些采取更自律或更保守路线的公司代价更高昂。供应商在被给予设计导入（design win）之后又被取消，也会失去信心。这导致新设计在供应链中的优先级下降。由于 Meta 频繁重组，一些供应商更倾向于把重心放在 Amazon 或 Google 的设计上。

Meta 的许多问题源于缺乏财务纪律：管理者不断创建新项目和新增 headcount，来填满并为 AI 等举措所获得的巨额预算寻找理由。这是 Meta Reality Labs 部门遭遇过的重演——数十亿美元被花在工程师和研发上，直到裁员（部分由公司转向 AI 引发）从 2022 年开始并持续到今年，砍掉了这些团队及其相关项目。

## Rivos 收购

首先，Meta 最近的一次失误是去年斥资超过 25 亿美元收购芯片初创公司 Rivos。

Meta 芯片部门内部几乎没人完全理解公司当初为什么要买 Rivos，而在内部力推这笔交易的人如今也已缄默。最流行的说法是：Meta 有钱，定制芯片领域正在升温，而且 Meta 本来就在为未来一颗芯片授权 Rivos 的 IP，所以领导层觉得不如干脆把 Rivos 的技术收入囊中，总好过让别人得到。

通过收购 Rivos，Meta 还获得了绕过 Broadcom 等合作伙伴、自行管理自家定制芯片制造与测试的能力——这种做法被称为客户自有工具（customer-owned tooling）。然而，为这项特权支付超过 25 亿美元同样说不过去，因为一个 COT 团队从零开始组建，每年也就 1 亿美元上下甚至更多。

尽管 Meta 只想要 Rivos 的加速器和 GPU 团队，但这家初创公司的创始人坚持「要么全盘收购、要么免谈」。Meta 买下了整个公司，然后在自己不想要的部分大举裁员。

![](https://substack-post-media.s3.amazonaws.com/public/images/f0536e95-d3f1-4bcf-82c7-c4763a34f9b8_1376x768.jpeg)
*来源：SemiAnalysis，Rivos*

一些前 Meta 芯片员工表示，这笔收购由 Meta 的芯片负责人 Yee Jiun Song 主导，他不顾部分下属的反对推动了交易，但此后已失去兴趣。结果是一个排斥移植的组织：Rivos 员工被困住、自谋出路。原有的 Meta 芯片管理者把这次收购当作免费的 headcount 池，抓走 Rivos 工程师来扩建自己的地盘，把这家初创公司原本的班底拉向不同方向，直到几乎没有什么完整的部分留下来。

这笔交易背后的技术理由同样迅速蒸发。Meta 当初的部分兴趣在于 Rivos 拥有 SIMT 核心 IP——在可编程性上更接近 NVIDIA 风格的 GPU 架构，而 Meta 自家的 MTIA 是 SIMD。然而交易完成后，Meta 取消了那颗名为 Olympus、原计划采用 Rivos GPU IP 的芯片，因为该设计在系统和封装架构上过于激进，软件也远未就绪。取而代之的是，Meta 将沿用其现有芯片架构直至 MTIA 600。

Meta 仍想开发一颗融合 Rivos 技术的芯片，并已启动名为 Phoebe 的新芯片项目，目前计划 2028 年流片。但 Meta 内部并非人人都对这个项目乐观，一些人认为它最终也可能被取消。我们一直在向[加速器模型](https://semianalysis.com/accelerator-hbm-model/)的订阅者更新各种定制芯片的不同架构、版图（floorplan）和出货量。

与此同时，加入 Meta 的 Rivos 员工领教了一堂 Meta 内部文化的速成课。与 Apple 那样更成熟的硬件组织不同，Meta 的硬件路线图变化速度与其软件路线图一样快，不断掉头，意味着你现在做的事情可能在六个月后变得毫无意义。Meta 芯片部门的许多人说，这里没有清晰的组织结构，没有清晰的决策机制，也没有哪个团队负责什么事的明确归属。

举一个不深入了解内情的人也能体会的失能例子：Meta 不给大多数员工分配固定工位；入职一年多的员工仍然每天四处找工位，有时桌上有显示器，有时显示器配错了线，有时根本没有显示器。员工正式申请过固定工位却被拒绝，哪怕空工位到处都是。

最后，Rivos 收购在原有的 Meta 芯片团队中制造了不满。许多 Rivos 工程师入职时带着更高的薪酬和头衔，却并没有与之相称的职责，而且他们被安置在原有 Meta 芯片员工之下。这导致原有团队士气下降，新加入的 Rivos 员工（缺乏决策权）同样士气低落。自今年年初以来，已有不少 Meta 芯片工程师离职，去向是初创公司或 Arm、NVIDIA 等根基深厚的老牌公司。

正如我们最先[向客户报告的](https://semianalysis.com/accelerator-hbm-model/)，随收购加入 Meta 的 Rivos 工程师中约有 30% 在最近的裁员中被裁掉。Rivos 联合创始人 Mark Hayter 已经离开。在第一批 RSU 于 5 月归属之后，一批前 Rivos 员工相继离开 Meta，加入了 Gerard Williams 的新芯片初创公司 Nuvacore。我们认为，Rivos 的 CEO 兼联合创始人 Puneet Kumar 也在盘算着一两年后等他在 Meta 的股份全部归属就退出。有传言称他可能加入 Rosaic Labs——一家由 Amarjit Gill 联合创立的新芯片初创公司；Amarjit Gill 是 Rivos 的投资人，也是 Puneet Kumar 在 SiByte、P.A. Semi、Apple 和 Agnilux 的长期合作者。

## Grand Teton

现在来谈谈 Meta 的 AI 服务器设计。Meta 的硬件决策主要由一项 TCO 分析驱动：将排序-推荐和 GenAI 等一系列工作负载，与 NVIDIA、AMD 以及自家定制芯片方案所能提供的能力进行对比。Meta CEO 马克·扎克伯格（Mark Zuckerberg）下了一道命令：所设计的系统必须服务整个业务，也就是说，不仅要支持 GenAI 工作负载，还要支持核心的排序和推荐系统。

然而，Meta 的 GPU 服务器仍选择了多项「优化」，这些选择都很奇怪，往往比其他超大规模云厂商购买的标准配置更差。部分问题源于该公司的服务器团队与网络团队处在完全割裂的组织里，目标和观点各不相同。Meta 工程师还有一种动机：拥有自己的网络操作系统和硬件，而不依赖其他公司。

回顾一下，Meta 的 H100 HGX 服务器名为「Teton Grand」，该设计已贡献给 OCP。与标准 HGX 服务器的主要区别在于，除了标准的 GPU 和 CPU 头节点配置之外，还增加了一个交换机托盘。这个交换机托盘容纳了 4 颗 Broadcom PCIe 交换芯片、16 块 SSD 和 8 块 NIC。其功能是提供额外的 PCIe 通道，让 Grand Teton 每台服务器能加装更多 SSD。

![](https://substack-post-media.s3.amazonaws.com/public/images/3b4a816f-4910-42af-b31e-b5c15cd97e33_2326x1314.jpeg)
*来源：Meta*

正是在 Hopper 世代，NVIDIA 通过在其 ConnectX-7 NIC 中实现 PCIe 交换功能，实际上用设计手段消除了对独立 PCIe 交换芯片的需求。

Intel Sapphire Rapids 主机 CPU 有 80 条 PCIe 通道可用，Meta 本可以设计一个这样的机箱：2 块 200G 前端 NIC 各用 8 条通道，4 条通道用于各种管理和控制，8 块 ConnectX-7 NIC 每块 16 条通道。这样还能剩下 32 条通道连接 8 块 E1.S SSD。所以最终，借助 Grand Teton，Meta 每台服务器多挤出了 8 块 SSD，代价是更高的服务器 BOM、更多功耗和更大的集成复杂度。

Meta 为什么想要这么多额外的直连存储？基础设施团队当初是抱着「训练运行做 checkpoint 需要更多存储」的信念做的配置。但在生产环境中，模型团队对这部分存储的利用远不及预期，这正是该设计最终被取消的原因。这是软硬件协同设计缺失、浪费资源的多个例子之一。

Meta 的其他理由是：该设计更易维护，并赋予其使用非 NVIDIA NIC 的灵活性。Meta 工程师想避免把更多业务拱手让给 NVIDIA，尤其是网络方面，因为公司在 GPU 上已经高度依赖 NVIDIA。

但那些 Broadcom 交换机根本没法维护，而且 Meta 的软件栈仍然依赖 NVIDIA 版本的 RoCE——GPU 流量所用的网络协议——所以 Meta 从来就不现实地可能更换 NIC 供应商。最终，Meta 花了更多钱、TCO 更差，既没有减少对 NVIDIA 网络设备的依赖，反而加重了对 Broadcom 的依赖。

## Ariel

Grand Teton 并非服务器设计上的一次性失误。这种失误延续到了 Blackwell 世代：Meta 定制的 GB200 Catalina 机柜，也称为「Ariel」。Ariel 是一颗 NVIDIA B200 GPU 搭配一颗 Grace CPU，而不是其他人购买的常规 GB200 SKU 中两颗 B200 GPU 搭配一颗 Grace CPU 的配置。实现方式很简单：Ariel 使用 GB200 所用的标准 Bianca 计算板，每块板上少焊一颗 GPU。

![](https://substack-post-media.s3.amazonaws.com/public/images/d9d214f0-6592-4441-80fc-0cc81094d3b6_2494x1405.jpeg)
*来源：Meta*

Meta 工程师担心单机柜 GB200 NVL72 的稳定性。NVL72 系统很复杂，涉及作为所有芯片连接中枢的铜背板、绵延数英里的密集铜缆，以及芯片与背板之间的数千个连接。Meta 基础设施部门最初押注 NVL36x2 配置会比完全通过背板连接的 NVL72 更稳定。

由于 Ariel 在一个机柜里放 36 颗 GPU，要达到 72 颗芯片的纵向扩展规模，就必须采用 36x2 形态。跨机柜 ACC 把各机柜的交换机托盘连接起来。这意味着交换机数量翻倍，同时还多增加了一跳的延迟。

![](https://substack-post-media.s3.amazonaws.com/public/images/304a5108-33ec-4134-a4f2-186e6442ea49_1176x793.png)
*来源：SemiAnalysis*

Meta 是这个 Ariel SKU 的唯一客户，原因在于 Meta 对其推荐系统（RecSys，负责推荐个性化广告和内容流）要更高 CPU-GPU 比例的执念。其逻辑是：RecSys 使用大量存储用户、广告和内容表示的嵌入表（embedding table），需要大量 CPU 密集型处理，而每颗 Grace 额外带来的 LPDDR 内存可以存放那些读取量小且分散的嵌入，因此带宽不像服务 LLM 时那么重要。

反面则是：提高 CPU 比例，再加上 36x2 配置带来的额外 NVLink 网络内容，每 GPU 的服务器资本开支随之上升。结果是 $/FLOP 以及每单位 HBM 容量和带宽的美元成本都远高于标准 GB200。而这些正是 LLM/GenAI 工作负载的关键指标，因此 Ariel 在 LLM 训练和推理上糟糕得多。总而言之，我们的计算显示，Ariel NVL36x2 服务器的 TCO 比标准 GB200 NVL72 高 14%。如前所述，这些额外开支换来的更多 CPU 和 DRAM 内容，LLM 团队根本用不上。这个决定让 Meta 损失了数十亿美元。

更不用说跨机柜 ACC 带来的两跳纵向扩展所附加的网络复杂性和可靠性挑战。正是这些挑战，导致只有少数超大规模厂商在 GB200 上出货过有限数量的 36x2，而 GB300 则完全放弃了 36x2 配置。讽刺的是，Meta 基础设施部门最初押注 NVL36x2 配置会比完全通过背板的 NVL72 更稳定。虽然背板最初确实是可靠性问题的来源，但如今背板已成熟得多，并战胜了跨机柜布线。公司低估了 36x2 设计的跨机柜布线问题，又高估了让 NVL72 背板正常运转的难度。一个机柜里放 36 颗 GPU 并没有带来任何背板可靠性上的好处。

因为我们了解到，Meta 的整个 GB200 机队都是这个 Ariel SKU，这项「优化」让 Meta 的 LLM 团队背负着一套劣于竞争对手所购标准 SKU 的系统。考虑到 GB200 当时是 GenAI 的旗舰系统，这一点尤其扎心。不出所料，Meta 的 GB300 类服务器不再有 Ariel，Meta 正在购买常规配置。

## 即将到来的 AMD MI450X：枪顶着脑袋的决定

*2026 年 8 月 3 日编辑：我们已根据新信息更新了 Meta 定制 MI450X SKU 的配置*

然而，我们看到这一幕如今在 AMD 的 MI450X 上重演。在 AMD 2026 年第一季度财报电话会上，苏姿丰（Lisa Su）确认 AMD 正在向 Meta 提供一款基于 MI450 的定制 GPU。我们已在[加速器模型](https://semianalysis.com/accelerator-hbm-model/)中对此报道了数月。[这款 Meta 定制 MI450X 是完整 MI450X 的削减版：I/O 减半，完整的 8 颗计算裸片/XCD 只保留 6 颗。](https://semianalysis.com/institutional/hbm-capacity-downgrades-amd-meta-version-and-increasing-2027-amd-estimates-trn4-tpu-whalefish-floorplan/)HBM4 也从标准 SKU 的 12 层堆叠（12-Hi）降级为 8 层堆叠（8-Hi）。

![](https://substack-post-media.s3.amazonaws.com/public/images/8a0433f0-d207-4f8f-b036-6ba8ff76e6b8_1710x1323.png)
*来源：AMD，SemiAnalysis*

只有 1 颗 I/O 裸片而不是 2 颗，可用的 I/O 通道就从 144 条减少到 72 条。通道预算缩减后，纵向扩展带宽必须降低。我们认为是 36 条通道用于纵向扩展，而非满血的 72 条；这意味着 Meta 版本每个机柜所需的 Tomahawk 6 交换芯片数量只需一半。剩下另外 36 条通道留给系统和横向扩展：16 条 UAL 128G 通道接往 NIC，实现每 GPU 1.6T 的横向扩展；另有 16 条 Infinity Fabric 通道用于连接主机 CPU。

这些选择的结果是，Meta 版 MI450X 的网络能力被显著削弱，每颗芯片的纵向扩展带宽只有一半，为 900GB/s，而 Rubin 是 1,800GB/s。相比常规版本还有 25% 的算力削减。算力削减幅度不算巨大，但减少 2 个计算 tile 省下的成本放在整个系统的语境里微不足道，因此人们不禁要问这个选择是否值得。

这一芯片配置是为 RecSys 工作负载设计的，是 RecSys 基础设施团队做的决定。然而，这个决定是在 TBD Lab 成立、或有机会发表意见之前做出的。鉴于如此严重的网络短板，TBD 会更倾向于 Vera Rubin。AMD 设计 MI450X Helios 是为了击败或打平 Vera Rubin 的规格，但 Meta Infra 决定钝化它，把算力和网络都变成短板。

这个决定将把 AMD 在 Meta 的出货量炸个精光，因为如果选定这款定制 MI450 设计，TBD 将极大地倾向 Rubin。AMD 需要介入，拿出成年人的担当，直接与 TBD 的团队合作，确保他们拿到正常的 MI450，而不是这个对 GenAI 十分糟糕的残血 Meta 定制版。正常的 MI450 其实有能力与 NVIDIA 的 Vera Rubin 一较高下。

这是我们向 Meta 和 AMD 发出的公开疾呼：不要浪费硅片，打造更好、更高效、更具成本效益的 AI 基础设施。如果做出这一改变，我们认为 TBD 实际上会考虑使用 MI450。

扎克伯格的命令也不过如此。接下来，我们将梳理 Meta 那套精心打造且耗资巨大的 DSF 网络架构，以及 Meta 为何迅速弃之而去。我们还将讨论这种文化可以如何修复。
