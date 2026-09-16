---
title: "英伟达 Blackwell 重构：出货延迟与重构后的 GB200A 平台"
title_en: "Nvidia's Blackwell Reworked - Shipment Delays & GB200A Reworked Platforms"
subtitle: "MGX GB200A NVL36、B102、B20、CoWoS-L、CoWoS-S、GB200A NVL64、ConnectX-8、液冷 vs 风冷、NVLink 背板、PCB、CCL、封装基板、BMC、供电"
date: 2024-08-04
source: https://newsletter.semianalysis.com/p/nvidias-blackwell-reworked-shipment
crawled: 2026-09-15
authors: ["Dylan Patel", "Wega Chu", "Daniel Nishball", "Myron Xie", "Chaolien Tseng"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 英伟达 Blackwell 重构：出货延迟与重构后的 GB200A 平台

> 原文：[Nvidia's Blackwell Reworked - Shipment Delays & GB200A Reworked Platforms](https://newsletter.semianalysis.com/p/nvidias-blackwell-reworked-shipment) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**MGX GB200A NVL36、B102、B20、CoWoS-L、CoWoS-S、GB200A NVL64、ConnectX-8、液冷 vs 风冷、NVLink 背板、PCB、CCL、封装基板、BMC、供电**

英伟达（Nvidia）的 Blackwell 系列在迈向大批量生产的过程中正遭遇重大问题。这一挫折已影响到其 2024 年第三、第四季度以及明年上半年的生产目标。这将影响英伟达的出货量与营收，正如我们 7 月 22 日在 [Accelerator Model](https://www.semianalysis.com/p/accelerator-model) 中[详细分析](https://x.com/dylan522p/status/1819693289689198800)的那样。简而言之，英伟达延长了 Hopper 的生命周期与出货，以弥补一部分延迟造成的缺口。Blackwell 的产品时间表有所推后，但出货量所受的影响比首批出货时间点更大。

这些技术挑战还迫使英伟达仓促打造此前并未规划的全新系统，这对上下游数十家供应商都有重大影响。今天，我们将梳理英伟达面临的技术挑战、其修订后的时间表，并详细拆解英伟达新系统（包括全新的 MGX GB200A Ultra NVL36）的系统与组件架构。我们还会深入分析这将对整条供应链——从客户到 OEM/ODM 再到英伟达的组件供应商——产生的影响。

![](https://substack-post-media.s3.amazonaws.com/public/images/c6be5954-7924-4000-984a-bc1cca1e203c_2584x808.png)
*来源：SemiAnalysis 估算、Nvidia*

英伟达 Blackwell 系列中技术最先进的芯片是 GB200，英伟达在系统层面的多个方面都做出了激进的技术选择。这个 72 GPU 机柜的功率密度约为每柜 125 kW，而多数数据中心部署的标准仅为每柜约 12 kW 至 20 kW。

这是前所未有的计算与功率密度，考虑到所需的系统级复杂度，其爬坡已被证明充满挑战。层出不穷的问题涉及供电、过热、水冷供应链爬坡、快接头漏水，以及各种电路板复杂度难题。虽然这些问题已让供应链上的一些供应商和设计方手忙脚乱，但大多数问题都属于次要问题，并非英伟达削减出货量或大幅修改路线图的原因。

影响出货的核心问题与英伟达对 Blackwell 架构的设计直接相关。最初版 Blackwell 封装的供应受限，原因出在台积电（TSMC）的封装环节以及英伟达自身的设计上。Blackwell 封装是第一个采用台积电 CoWoS-L 技术进行大批量生产的封装设计。

![](https://substack-post-media.s3.amazonaws.com/public/images/e92064aa-964b-4f15-852a-cc75a550abc6_1600x466.png)
*来源：台积电（TSMC）*

回顾一下：CoWoS-L 采用 RDL 中介层，将局部硅互连（LSI）和桥接裸片（bridge die）嵌入中介层中，以桥接封装内各个计算芯片与内存之间的通信。相比之下，CoWoS-S 从表面上看要简单得多——就是一整块大面积的硅片。

![](https://substack-post-media.s3.amazonaws.com/public/images/704928a8-97a2-4f1b-bcfd-ba03150875bc_1293x488.png)
*来源：台积电（TSMC）*

随着未来 AI 加速器集成更多逻辑、内存和 IO，CoWoS-S 在封装尺寸扩展和性能方面都遇到了瓶颈，因此 CoWoS-L 成为它的继任者。台积电已借助 AMD 的 MI300 将 CoWoS-S 扩展到约 3.5 倍光罩尺寸的中介层，但这已是实际极限。制约因素有很多，但最关键的一点是硅本身很脆，中介层越大，超薄硅中介层的操作处理就越困难。而且随着光刻光罩拼接次数越来越多，这种大面积硅中介层的成本也会越来越高。

有机中介层可以解决这个问题，因为它不像硅那样脆，但它的电性能不如硅，无法为更强大的加速器提供足够的 I/O。此时可以再用硅桥（无源或有源）来补充信号密度加以补偿。此外，这些桥接的性能/复杂度还可以做到比大面积硅中介层更高。

CoWoS-L 是一项复杂得多的技术，但它代表着未来。英伟达和台积电曾定下[非常激进的产能爬坡计划](https://www.semianalysis.com/p/accelerator-model)，目标是每季度超过 100 万颗芯片。结果便是，[各种问题接连出现](https://www.semianalysis.com/p/accelerator-model)。

其中一个问题与中介层有关：在有机中介层中嵌入多个细间距凸点（fine bump pitch）桥接，会在硅裸片、桥接、有机中介层和封装基板之间造成热膨胀系数（CTE）失配，引发翘曲。

![](https://substack-post-media.s3.amazonaws.com/public/images/b5f7ce7a-f2d7-4d9d-bfff-17dfeb2a935a_1100x500.png)
*来源：Resonac*

桥接裸片的放置需要极高的精度，尤其是两个主计算裸片之间的桥接，因为它们对支撑 10 TB/s 的裸片间互连至关重要。传闻中的一个重大设计问题正与桥接裸片有关：这些桥接需要重新设计。另有传闻称，Blackwell 裸片顶部的几层全局布线金属层和凸点也需要重新设计。[这是造成数月延迟的一个主要原因。](https://www.semianalysis.com/p/accelerator-model)

另一个问题是台积电的 CoWoS-L 总体产能不足。过去几年，台积电[建设了大量 CoWoS-S 产能](https://www.semianalysis.com/p/ai-expansion-supply-chain-analysis)，其中英伟达拿走了最大份额。如今随着英伟达迅速把需求转向 CoWoS-L，台积电一方面在新建专门用于 CoWoS-L 的厂房 AP6，另一方面也在将 AP3 现有的 CoWoS-S 产能进行改造。台积电必须改造旧的 CoWoS-S 产能，否则这些产线将面临稼动率不足，而 CoWoS-L 的爬坡也会更慢。[这种改造过程本身也让爬坡呈现出非常参差不齐的形态。](https://www.semianalysis.com/p/accelerator-model)

把这两个问题叠加起来看，台积电显然无法按英伟达期望的规模供应足够的 Blackwell 芯片。因此，英伟达正把现有产能几乎全部集中到 GB200 NVL 36x2 和 NVL72 机柜级系统上。除最初的一小批较低出货量外，采用 B100 和 B200 的 HGX 形态产品实际上已被取消。

![](https://substack-post-media.s3.amazonaws.com/public/images/7cbd2167-547c-47bd-bd11-7d1bafc1f88f_2584x808.png)
*来源：SemiAnalysis 估算、Nvidia*

为了满足需求，英伟达现在将推出一款名为 B200A 的 Blackwell GPU，它基于 B102 裸片。有意思的是，这颗 B102 裸片也将用于中国版 Blackwell——即 B20。B102 是一颗单片式（monolithic）计算裸片，配 4 组 HBM 堆叠。关键在于，这使得该芯片可以用 CoWoS-S 封装而非 CoWoS-L，甚至可以交给[英伟达的其他 2.5D 封装供应商，如 Amkor、ASE SPIL 和三星（Samsung）](https://www.semianalysis.com/p/accelerator-model)。原版 Blackwell 裸片把大量边缘（shoreline）面积留给了 C2C I/O，而这在单颗单片式 SOC 上是多余的。

B200A 将用来满足低端和中端 AI 系统的需求，并将在 HGX 8-GPU 形态中取代 B100 和 B200 芯片。它将有 700W 和 1000W 两种 HGX 形态，配备最高 144GB 的 HBM3E 和最高 4 TB/s 的内存带宽。值得注意的是，这低于 H200 的内存带宽。

再来看 Blackwell Ultra——Blackwell 的中期增强版。标准的 CoWoS-L 版 Blackwell Ultra 将被称作 B210 或 B200 Ultra。Blackwell Ultra 包含两方面的升级：一是内存升级至最高 288GB 的 12 层堆叠（12-Hi）HBM3E，二是 FLOPS 性能提升，最高可达 50%。

B200A 也会有 Ultra 版本。值得注意的是，它不会有内存升级，不过裸片可能会经过重新设计以提升 FLOPS。B200A Ultra 还引入了一个全新的 MGX NVL 36 形态。与原版 B200A 一样，B200A Ultra 也会提供 HGX 配置。

![](https://substack-post-media.s3.amazonaws.com/public/images/823d51fe-36b6-4612-ba8e-4688f0660652_2524x913.png)
*来源：SemiAnalysis 估算、Nvidia*

对于超大规模云厂商市场，我们认为 GB200 NVL72 / 36x2 仍将是最有吸引力的选择，因为在推理超过 2 万亿参数的模型时，它拥有最高的性能/TCO。话虽如此，如果超大规模云厂商客户拿不到想要的那么多 GB200 NVL72 / 36x2 产能配给，他们可能仍需购买 MGX GB200A NVL36。此外，对于功率密度较低的数据中心，或者缺乏液冷改造所需许可/水源的数据中心来说，MGX NVL36 会更有吸引力。

超大规模云厂商仍会购买 HGX Blackwell 服务器，因为它是适合出租给外部客户的最小计算单元，但采购量将比以前低得多。对于小模型而言，HGX 依然是性能/TCO 最优的选择，因为这些模型不需要那么多内存，可以装进 NVL8 的单一内存一致性域内。

在投入训练负载的 GPU 少于 5,000 颗的训练场景中，HGX Blackwell 的性能/TCO 同样出色。话虽如此，MGX NVL36 对许多下一代模型而言是「甜蜜点」，而且作为基础设施总体上更灵活，因此在很多情况下是更优的选择。

至于新兴 GPU 云（neocloud）市场，我们认为大多数客户不会购买 GB200 NVL72 / 36x2，因为要找到支持液冷、或能借助边柜（sidecar）实现高功率密度部署的托管（colocation）服务商实在太复杂。此外，在有限的 GB200 NVL72 / 36x2 出货量面前，大多数新兴 GPU 云的排队位置总体上要落后于超大规模云厂商。

我们认为，像 CoreWeave 这样既自建/改造数据中心、又拥有大客户的大型新兴 GPU 云会选择 GB200 NVL72 / 36x2。而其余新兴 GPU 云市场中的大多数会选择 HGX Blackwell 服务器和 MGX NVL36，因为这两者只需风冷和较低功率密度的机柜即可部署。目前大多数新兴 GPU 云部署的是 Hopper，功率密度为 20kW/柜。我们认为新兴 GPU 云有可能部署 MGX GB200 NVL36，因为它只需要 40kW/柜的风冷能力。

通过冷通道封闭（cold aisle containment）并在数据中心里跳行（隔行）布置，每柜 40kW 的部署并不算太难。在新兴 GPU 云这个层面，运营商及其客户往往并不会针对自己的具体负载去认真计算性能/TCO，而只是想办法采购当下热度最高的产品。例如，绝大多数（甚至全部）新兴 GPU 云的客户并不使用 FP8 训练，而是选择 bfloat16 训练。对于用 bfloat16 训练小型 LLM 的场景，A100 80GB 的性能/TCO 要好得多。

由于 Meta 的 LLAMA 系列模型正在左右许多企业和新兴 GPU 云的基础设施选择，最相关的部署单元指标就是「能否装下 Meta 的模型」。LLAMA 3 405B 无法装进单个 H100 节点，但勉强能装进 H200（模型可以量化，但质量损失极大）。405B 对于 H200 HGX 服务器而言已经到了极限，下一代 MoE 架构的 LLAMA 4 肯定无法装进单个 Blackwell HGX 节点，这将显著影响性能/TCO。

因此，对于驱动初创公司和企业部署的最实用的那些开源模型的微调与推理来说，单台 HGX 服务器的性能/TCO 会更差。[我们对 MGX B200A Ultra NVL36 的估算定价](https://www.semianalysis.com/p/accelerator-model)表明，HGX B200A 不太可能卖得动。英伟达有多个强有力的动机去稍微削减利润率来主推 MGX，因为它可以凭借自家网络产品更高的搭售率（attach rate）把利润赚回来。

## MGX GB200A Ultra NVL36 的架构

MGX GB200A NVL36 这一 SKU 是一个完全风冷的 40kW/柜服务器，通过 NVLink 将 36 颗 GPU 全互联。每个机柜有九个计算托盘（compute tray）和九个 NVSwitch 托盘。每个计算托盘为 2U，包含一颗 Grace CPU 和四颗 700W 的 B200A Blackwell GPU；相比之下，GB200 NVL72 / 36x2 的每个计算托盘包含两颗 Grace CPU 和四颗 1200W 的 Blackwell GPU。如果不熟悉 GB200 的硬件架构和组件供应链，请参阅[这篇文章](https://www.semianalysis.com/p/gb200-hardware-architecture-and-component)。

MGX NVL36 设计的 CPU 与 GPU 之比只有 1:4，而 GB200 NVL72 / 36x2 为 2:4。此外，每个 1U NVSwitch 托盘只放一颗交换 ASIC，每颗交换 ASIC 的带宽为 28.8Tbit/s。

![](https://substack-post-media.s3.amazonaws.com/public/images/cba4fb41-f847-4258-ae55-e87d383faaf8_639x1433.png)
*来源：SemiAnalysis GB200 与 GB200A 组件及供应链模型*

由于每柜只有 40kW，MGX NVL36 可以采用风冷。虽然大多数数据中心和当前 H100 部署只有 20kW/柜，但 40kW/柜 的 H100 部署也并不罕见。其实现方式是在数据中心里跳行布置并使用冷/热通道封闭。部署 40kW 的 MGX NVL36 机柜时可以沿用同样的手法。这使得现有数据中心运营商无需改造基础设施就能轻松部署 MGX NVL36。

与 GB200 NVL72 / 36x2 不同，四颗 GPU 对一颗 CPU 的更高比例意味着它无法使用 C2C 互连，因为每颗 GPU 获得的 C2C 带宽只有 GB200 NVL72/36x2 的一半。取而代之的是，将利用集成 PCIe 交换功能的 ConnectX-8 来让 GPU 与 CPU 通信。此外，与现有所有其他 AI 服务器（HGX H100/B100/B200、GB200 NVL72 / 36x2、MI300）都不同，现在每块后端 NIC（backend NIC）要负责两颗 GPU。这意味着即便 ConnectX-8 NIC 设计可提供 800G 的后端网络，每颗 GPU 也只能用到 400G 的后端 InfiniBand/RoCE 带宽。

![](https://substack-post-media.s3.amazonaws.com/public/images/10810f6f-b1c5-4adc-9cb0-8ec0b1251289_1862x1404.png)
*来源：SemiAnalysis GB200 与 GB200A 组件及供应链模型*

在 GB200 NVL72 / 36x2 上，配备 ConnectX-8 后端 NIC 时，每颗 GPU 最高可享有 800G 带宽。

在参考设计中，GB200A NVL36 每个计算托盘将使用一块 BlueField-3 前端 NIC。相比 GB200 NVL72 / 36x2 每个计算托盘配两块 BlueField-3，这是一个更合理的设计。即便是对 MGX NVL36，我们依然认为很多客户不会选用任何 BlueField-3——超大规模云厂商会改用自家内部 NIC，其他客户则可能使用 ConnectX-6/7 这类通用前端 NIC。

GB200 NVL72/NVL36x2 计算托盘的核心是 Bianca 板。每块 Bianca 板包含两颗 Blackwell B200 GPU 和一颗 Grace CPU。每个计算托盘有两块 Bianca 板，也就是说每个计算托盘总共有两颗 Grace CPU 和四颗 1200W 的 Blackwell GPU。

![](https://substack-post-media.s3.amazonaws.com/public/images/e107c474-00de-4ca6-a987-ae95b579fd95_839x944.png)
*来源：SemiAnalysis GB200 与 GB200A 组件及供应链模型*

在 MGX GB200A NVL36 上，CPU 和 GPU 将位于不同的 PCB 上，这一点与 HGX 服务器的设计类似。但与 HGX 服务器不同的是，我们认为每个计算托盘的 4 颗 GPU 会被进一步拆分为两块 2-GPU 板。每块 2-GPU 板都会带有与 Bianca 板类似的 [Mirror Mezz 连接器](https://www.semianalysis.com/p/semianalysis-gb200-component-and)。这些 Mirror Mezz 连接器将用于连接 ConnectX-8 夹层板（mezzanine board），后者将带集成 PCIe 交换的 ConnectX-8 ASIC 与 GPU、本地 NVMe 存储以及 Grace CPU 连接起来。

让 ConnectX-8 ASIC 与 GPU 紧紧相邻，意味着 GPU 与 ConnectX-8 NIC 之间不再需要重定时器（retimer）。这与 HGX H100/B100/B200 不同——后者需要重定时器来实现从 HGX 基板到 PCIe 交换芯片的连接。

由于 Grace CPU 与 Blackwell GPU 之间没有 C2C 互连，Grace CPU 也被放在一块完全独立的 PCB 上，称为 CPU 主板。这块主板将包含 BMC 连接器、CMOS 电池、MCIO 连接器等。

![](https://substack-post-media.s3.amazonaws.com/public/images/9440584a-3168-44eb-bb3b-49a27bacead9_1590x1466.png)
*来源：SemiAnalysis GB200 与 GB200A 组件及供应链模型*

每颗 GPU 的 NVLink 带宽为每方向 900GByte/s，与 GB200 NVL72 / 36x2 相同。按每 FLOP 计算，GPU 间带宽大幅提升，这使 MGX NVL36 对某些负载非常有利。

由于只需 1 层交换机即可连接 36 颗 GPU，因此只需 9 颗 NVSwitch ASIC 就能提供无阻塞网络。而且，每个 1U 交换托盘只有一颗 28.8Tbit/s 的 ASIC，风冷相当容易。Quantum-2 QM9700 这类 25.6Tbit/s 的 1U 交换机早已可以轻松风冷。虽然英伟达本可以通过让交换托盘保留 2 颗 NVSwitch ASIC 来实现 NVL36x2 设计，但那会增加成本，而且由于前面板的 OSFP NVLink 笼会阻挡气流，可能导致无法风冷。

![](https://substack-post-media.s3.amazonaws.com/public/images/a1bc598c-3574-468d-a289-760a84b09d7a_1946x1308.png)
*来源：SemiAnalysis GB200 与 GB200A 组件及供应链模型*

在后端网络上，由于每个计算托盘只有两个 800G 端口，我们认为它将采用 2 轨优化（2-rail optimized）的列尾（end of row）组网。每 8 个 GB200A NVL36 机柜将配备两台 Quantum-X800 QM3400 交换机。

![](https://substack-post-media.s3.amazonaws.com/public/images/49dcafda-9e4b-4aa9-8de5-351c8c291209_2356x1425.png)
*来源：SemiAnalysis GB200 与 GB200A 组件及供应链模型*

我们估计，按每颗 GPU 700W 计算，GB200A NVL36 大概率在每柜 40kW 左右。2U 计算托盘约需 4kW 功率，但要在 2U 空间里风冷散掉 4kW 的热量，将需要特制散热器和高速风扇。

![](https://substack-post-media.s3.amazonaws.com/public/images/2421710f-f8cf-47c8-967d-87ff41fbd205_1518x1106.png)
*来源：SemiAnalysis GB200 与 GB200A 组件及供应链模型*

我们将在后文讨论其散热挑战，但这对英伟达的 MGX NVL36 设计而言是一个重大风险。

## MGX GB200A NVL36 爬坡的挑战

对于 GB200 NVL72 / NVL36x2，唯一不使用 ConnectX-7/8 后端 NIC 的客户是 Amazon。正如我们在 [GB200 架构分析](https://www.semianalysis.com/p/gb200-hardware-architecture-and-component)中所讨论的，这已经构成重大的工程挑战：系统里将没有 ConnectX-7/8 或 BlueField-3（两者都集成 PCIe 交换），因此需要 Broadcom 或 Astera Labs 的独立 PCIe 交换芯片来把后端 NIC 连接到 CPU、GPU 和本地 NVMe 存储。这会消耗额外功率并增加物料清单（BOM）成本。

[在 SemiAnalysis GB200 组件与供应链模型中，我们拆解了所有组件的供应商份额、出货量和平均售价（ASP），包括 PCIe 交换芯片。](https://www.semianalysis.com/p/semianalysis-gb200-component-and)由于 GB200A NVL36 完全风冷，若在 2U 机箱前部再放上独立 PCIe 交换芯片外加 PCIe 形态的 NIC，将大幅增加散热工程难度。

![](https://substack-post-media.s3.amazonaws.com/public/images/67d4a46b-a294-4025-af94-fa95034202a0_1862x1404.png)
*来源：SemiAnalysis GB200 与 GB200A 组件及供应链模型*

因此我们认为，在 GB200A NVL36 上做定制后端 NIC 对任何人来说都基本不可能。

既然 Grace CPU 和 Blackwell GPU 位于不同的 PCB 上，我们认为也可能出现 x86 + B200A NVL36 版本。由于很多 ML 依赖库都是针对 x86 CPU 编译和优化的，这对该 SKU 可能是一项额外优势。此外，x86 CPU 平台能提供峰值性能比 Grace 更高的 CPU。遗憾的是，愿意提供 x86 版本的 OEM 将面临散热挑战，因为 CPU 要多消耗约 100 瓦功率。我们认为，即便英伟达提供 x86 B200A NVL36 方案，它也会把大多数客户往 GB200A NVL36 方案上引导，因为后者能顺带卖掉 Grace CPU。

GB200A NVL36 的核心卖点是它是一套每柜 40kW 的风冷系统。对客户来说，主要的吸引力在于：许多人仍然无法支持每柜约 125 kW 的 GB200 NVL72（或双机柜合计超过 130kW 的 36x2）所需要的液冷和供电基础设施。

完全没有液冷，意味着与 GB200 NVL72 / 36x2 相比，整体散热方案将基本简化回归到一颗散热器（3D 均热板，3DVC）加几把风扇。不过，鉴于 GB200A NVL36 的计算托盘采用 2U 机箱，3DVC 的设计需要大幅调整。

TDP 为 700W 的 H100 目前使用 4U 高的 3DVC，而 1000W 的 H200 使用 6U 高的 3DVC。相比之下，700W TDP 塞进 2U 机箱的 MGX B200A NVL36 就相当局促了。我们认为需要一种向水平方向扩展、呈「阳台」状的散热器，以增大散热器表面积。

![](https://substack-post-media.s3.amazonaws.com/public/images/36cf68e1-1b08-4c75-920f-e42298e3f3af_1199x800.jpeg)
*来源：ServeTheHome*

除了需要更大的散热器之外，风扇还要提供比 GB200 NVL72 / 36x2 的 2U 计算托盘或 HGX 8 GPU 设计大得多的风量。我们估计，在这 40kW 机柜中，总系统功率的 15% 到 17% 将分配给机箱内部风扇。因此，GB200A NVL36 的 TUE 值（一个能[更好反映风冷与液冷能效差异](https://www.vertiv.com/en-emea/about/news-and-insights/articles/blog-posts/understanding-the-limitations-of-pue-in-evaluating-liquid-cooling-efficiency/)的指标）将远高于 GB200 NVL72 / NVL36。

即便是 HGX H100 这类风冷服务器，我们认为风扇也只占总系统功率的 6% 到 8%。由于让 MGX GB200A NVL36 跑起来需要巨量风扇功率，这一设计的效率要低得多。此外，甚至存在连这个设计也行不通的可能——届时英伟达将不得不推倒重来，尝试改做 3U 计算托盘，或缩小 NVLink world size（域内 GPU 规模）。

在进入 GB200A NVL36 的硬件子系统与组件变化（这些变化影响着供应链中的众多玩家）之前，先来谈谈 GB200A NVL64。

## **英伟达为何取消 GB200A NVL64**

在英伟达最终敲定 MGX GB200A NVL36 之前，它还试验过一种风冷 NVL64 机柜设计。这个完全风冷的 60kW 机柜本应通过 NVLink 将 64 颗 GPU 全互联。我们对这个拟议 SKU 做了大量工程分析，出于下文讨论的种种顾虑，我们认为该产品不可行，也不会出货。

在拟议的 NVL64 SKU 中，有 16 个计算托盘和 4 个 NVSwitch 托盘。每个计算托盘为 2U，包含一颗 Grace CPU 和四颗 700W 的 Blackwell GPU，与 MGX GB200A NVL36 一样。重大改动出现在 NVSwitch 托盘上：英伟达没有把 GB200 每托盘两颗 NVSwitch 减为一颗，而是尝试增加到四颗交换 ASIC。

![](https://substack-post-media.s3.amazonaws.com/public/images/9db8cfdb-a819-4ae5-a783-cb1b762884f9_808x1522.png)
*来源：SemiAnalysis GB200 与 GB200A 组件及供应链模型*

尽管英伟达的拟议设计称 NVL64 将是 60kW 机柜，但我们估算功率预算后认为下限更接近每柜 70kW。无论 60kW 还是 70kW，仅靠风冷给整柜散热都是疯狂的，往往需要后门热交换器——但这就摧毁了风冷机柜架构的意义，因为你仍然依赖液冷供应链，而且对大多数数据中心来说，要把设施水送到后门热交换器，仍然需要进行设施级改造。

![](https://substack-post-media.s3.amazonaws.com/public/images/9d26bbb1-65f6-4347-bf49-ecf36066aa8b_1354x1053.png)
*来源：SemiAnalysis GB200 与 GB200A 组件及供应链模型*

另一个非常棘手的散热问题是：NVSwitch 托盘要在单个 1U 机箱里塞进四颗 28.8Tbit/s 交换 ASIC，需要散掉近 1,500W 的热量。1U 机箱 1,500W 本身不算离谱，但一旦考虑到从交换 ASIC 到背板连接器的 [Ultrapass 飞越线缆（flyover cable）](https://www.semianalysis.com/p/semianalysis-gb200-component-and)会阻挡大量气流，散热就变得非常困难。

鉴于风冷 MGX NVL 机柜正以惊人速度冲向市场——英伟达试图从开始设计起仅 6 个月内就出货——对于一个工程资源早已捉襟见肘的行业来说，打造一款新的交换托盘及其供应链相当困难。

拟议 GB200A NVL64 的另一个大问题是端口失配：每个机柜有 64 个 800G 后端端口，而每台 XDR Quantum-X800 Q3400 交换机有 72 个 800G 下行端口。这意味着采用轨道优化（rail optimized）的后端拓扑会浪费端口——每台交换机会有 16 个 800G 端口空置。在昂贵的后端交换机上留空端口会显著损害网络性能/TCO，因为交换机很贵，尤其是 Quantum-X800 这种高端口数（high-radix）模块化交换机。

![](https://substack-post-media.s3.amazonaws.com/public/images/3c5f1438-a675-4ba6-ab08-4315e9447b45_1592x847.png)
*来源：Nvidia*

此外，在同一个 NVLink 域内放 64 颗 GPU 也并不理想。表面上看这似乎很棒——64 是 2 的漂亮偶数倍，适合各种并行配置，比如（张量并行 TP=8、专家并行 EP=8）或（TP=4、完全分片数据并行 FSDP=16）。遗憾的是，由于硬件的不可靠性，英伟达建议每个 NVL 机柜至少保留一个计算托盘作为储备，让 GPU 可以下线维护，同时用其充当热备（hot spare）。

如果每个机柜没有至少一个计算托盘处于热备状态，那么哪怕只坏一颗 GPU，其影响范围也会导致整个机柜被迫停机相当长时间。这与 8 GPU 的 HGX H100 服务器类似：服务器上只要有一颗 GPU 故障，全部 8 颗 H100 都得停止服务，无法继续为负载贡献力量。

![](https://substack-post-media.s3.amazonaws.com/public/images/95fcc21e-27ff-424d-aebd-fe3d9e1e0eb8_1871x827.png)
*来源：SemiAnalysis GB200 与 GB200A 组件及供应链模型*

为热备保留至少一个计算托盘后，每个机柜就只剩 60 颗 GPU 为负载工作。64 这个数字用起来更顺手——它有 2、4、8、16、32 这些公因数，可以组合出更漂亮的并行方案，而 60 则不然。

这正是 GB200 在 NVL36x2 或 NVL72 配置下选择总计 72 颗 GPU 的用意所在——它可以留两个计算托盘热备，让每个机柜仍有 64 颗 GPU 为负载工作。

GB200A NVL36 可以留一个计算托盘热备，同时保有 2、4、8、16 这些公因数用于并行方案，从而在实际负载中实现更高的可靠性。

## **硬件组件供应链与 OEM/ODM 影响**

在下面这一节，我们将讨论原版 Blackwell 延迟以及 MGX GB200A 推出对 OEM、ODM 和组件的影响。[我们预计 GB200 NVL72 / 36x2 的出货将减少/推后，B100 与 B200 HGX 的出货量将大幅下降。](https://www.semianalysis.com/p/accelerator-model)取而代之，我们预计 2024 年第四季度到 2025 年第一季度 Hopper 出货增加。此外，下半年出货的 GPU 订单将从 HGX Blackwell 和 GB200 NVL36x2 转向 MGX GB200A NVL36。

这将影响所有 ODM 和组件供应商，因为出货/营收时间表在 2024 年第三季度至 2025 年第二季度间将剧烈变动。每家供应商受影响的程度还取决于它是 GB200 NVL72 / 36 和 MGX NVL36 的赢家还是输家，以及它在 Hopper 系列中是否有可观份额（从而受益于 Hopper 生命周期延长）。

组件层面的影响涵盖散热、PCB、CCL、封装基板、NVLink 铜背板用量、ACC 线缆用量、光模块用量、BMC、供电用料等。我们会将 MGX GB200A NVL36 系统的 BOM 成本与 GB200 NVL72 / 36x2 进行对比，因为对于 Oberon 平台的机柜系统组件来说，这是更对等的比较。要做这个对比，需要先了解[前一篇关于硬件与组件架构的文章](https://www.semianalysis.com/p/gb200-hardware-architecture-and-component)，才能完全跟上增量变化。

此外，我们已更新 [GB200 组件与供应链模型](https://www.semianalysis.com/p/semianalysis-gb200-component-and)，加入了 MGX GB200A NVL36 的具体 ASP、BOM 及美元用量份额估算。
