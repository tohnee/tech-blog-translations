---
title: "GB200 硬件架构：组件供应链与 BOM"
title_en: "GB200 Hardware Architecture - Component Supply Chain & BOM"
subtitle: "超大规模定制、NVLink 背板、NVL36、NVL72、NVL576、PCIe 重定时器、交换机、光模块、DSP、PCB、InfiniBand/以太网、封装基板、CCL、CDU、边柜（Sidecar）、PDU、VRM、母排（Busbar）、导轨套件（Railkit）、BMC"
date: 2024-07-17
source: https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component
crawled: 2026-09-15
authors: ["Dylan Patel", "Wega Chu", "Chaolien Tseng", "Myron Xie", "Jeremie Eliahou Ontiveros", "Daniel Nishball"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# GB200 硬件架构：组件供应链与 BOM

> 原文：[GB200 Hardware Architecture - Component Supply Chain & BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**超大规模定制、NVLink 背板、NVL36、NVL72、NVL576、PCIe 重定时器、交换机、光模块、DSP、PCB、InfiniBand/以太网、封装基板、CCL、CDU、边柜（Sidecar）、PDU、VRM、母排（Busbar）、导轨套件（Railkit）、BMC**

英伟达的 GB200 凭借[更优的硬件架构](https://www.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband)带来了[显著的性能提升](https://www.semianalysis.com/p/nvidia-blackwell-perf-tco-analysis)，但部署复杂度也急剧上升。表面上，英伟达发布的是一个标准机柜，人们只需即插即用式地把它装进数据中心，不会有什么麻烦；但现实是，部署变体多达数十种，各有取舍，复杂度相比上一代显著增加。对数据中心最终部署方、云厂商、服务器 OEM/ODM 以及下游组件供应链来说，整条供应链都在被重塑。

今天，我们将从头到尾讲清 GB200 的各种形态（form factor）以及它们相比此前 8 GPU HGX 基板服务器的变化。**我们将拆解 GB200 机柜 50 多个不同子组件的出货量、供应商市场份额和成本。**此外，我们还会深入探讨大幅改变子组件供应链的超大规模定制。最后，我们还将深度解析各类液冷架构、部署复杂度及其供应链。

## 目录：

- GB200 各形态
- 功率预算
- 计算托盘架构
- 网络

  - NVLink 网络

    - NVL72
    - NVL36x2
    - NVL576
  - 后端网络（InfiniBand/以太网）
  - 前端网络
  - 网络美元用量汇总
  - 光模块
  - DSP
- 超大规模云厂商定制
- 封装基板、PCB 与 CCL
- 液冷

  - 机柜架构变化与用量
  - 传热路径
  - L2A（液到风）vs L2L（液到液）
  - 数据中心基础设施的重新设计
  - 供应链采购决策者与分析
  - 液冷组件竞争格局
- 供电网络、PDB、母排、VRM
- BMC
- 机械结构件
- OEM / ODM 对应关系

## **Blackwell 的 4 种机柜级形态**

GB200 机柜共有 4 种主要形态，每种形态内部还有定制空间。

- GB200 NVL72
- GB200 NVL36x2
- GB200 NVL36x2（Ariel）
- x86 B200 NVL72/NVL36x2

第一种是 **GB200 NVL72 形态**。该形态每柜需要约 120kW。为了让读者对这一密度有个概念：通用 CPU 机柜最高支持 12kW/柜，而密度更高的 H100 风冷机柜通常也只支持约 40kW/柜。远超 40kW/柜，正是 GB200 必须采用液冷的首要原因。

![](https://substack-post-media.s3.amazonaws.com/public/images/ab46e1af-916d-4fa1-874a-e31095be4bf8_810x780.png)
*来源：SemiAnalysis*

GB200 NVL72 机柜由 18 个 1U 计算托盘和 9 个 NVSwitch 托盘组成。每个计算托盘高 1U，包含 2 块 Bianca 板。每块 Bianca 板为 1 颗 Grace CPU 加 2 颗 Blackwell GPU。NVSwitch 托盘则各含两颗 28.8Tb/s 的 NVSwitch5 ASIC。

除了一家计划将其作为主力版本部署的超大规模云厂商外，我们认为在 Blackwell Ultra 之前这一版本将很少被部署，因为多数数据中心基础设施即便配上冷板式直冷（DLC）也无法支撑如此高的机柜功率密度。

下一种形态是 **GB200 NVL36 x2**，即两个并排机柜互联在一起。[大多数 GB200 机柜将采用这一形态。](https://www.semianalysis.com/p/accelerator-model)每个机柜包含 18 颗 Grace CPU 和 36 颗 Blackwell GPU。两柜之间仍保持着 NVL72 中 72 颗 GPU 全体无阻塞任意互联的特性。每个计算托盘高 2U，包含 2 块 Bianca 板。每个 NVSwitch 托盘有两颗 28.8Tb/s 的 NVSwitch5 ASIC 芯片，每颗芯片有 14.4Tb/s 朝向后方背板、14.4Tb/s 朝向前面板。每个 NVSwitch 托盘有 18 个 1.6T 双端口 OSFP 笼，横向连接到配对的 NVL36 机柜。

![](https://substack-post-media.s3.amazonaws.com/public/images/b49ca1d6-be75-436a-b4c7-35201a39f9fd_1161x799.png)
*来源：SemiAnalysis*

NVL36 x2 的单柜功率与散热密度为 66kW/柜，两柜合计 132kW。这是抢时间上市的方案，因为单柜只需 66kW/柜。遗憾的是，由于额外的 NVSwitch ASIC 以及跨机柜互连线缆的需求，NVL36x2 系统确实比 NVL72 多耗约 10kW。NVL36x2 总共需要 36 颗 NVSwitch5 ASIC，而 NVL72 只需 18 颗。[即便整体功率多出 10kW，明年大多数公司仍会部署这个版本而不是 NVL72，因为他们的数据中心支撑不了 120kW/柜的密度。](https://www.semianalysis.com/p/datacenter-model)原因我们将在后文液冷部分讨论。

最后一种形态是使用定制「Ariel」板（而非标准 Bianca 板）的特定机柜。我们认为这一变体将主要由 Meta 使用。由于 Meta 的推荐系统训练与推理负载，他们需要更高的 CPU 核数和更高的每 GPU 内存配比，以便存储海量嵌入表（embedding table）并在 CPU 上完成前/后处理。

其内容物与标准 GB200 NVL72 类似，只是把 Bianca 板换成了每块含 1 颗 Grace CPU 和 1 颗 Blackwell GPU 的 Ariel 板。由于每 GPU 对应的 Grace CPU 数量翻倍，这个 SKU 即便与 NVL36x2 相比也更贵。与 NVL36x2 类似，每个 NVSwitch 托盘有 18 个 1.6T 双端口 OSFP 笼，横向连接到配对的 NVL36 机柜。

![](https://substack-post-media.s3.amazonaws.com/public/images/25dbc81f-8d7c-4544-ad70-54608ad32cc3_1176x793.png)
*来源：SemiAnalysis*

[我们认为 Meta 拿到的配给大部分会是普通 NVL36x2，因为它更契合生成式 AI（GenAI）负载，而 Ariel 版本只会用于他们规模最大的推荐系统负载。](https://www.semianalysis.com/p/accelerator-model)虽然没有什么能阻止 Ariel 用于 GenAI 负载，但 CPU 的过度配置意味着它的 [TCO](https://www.semianalysis.com/p/ai-cloud-tco-model) 更差——资本开支和功率都更高。

最后，2025 年第二季度还会出现 **B200 NVL72 与 NVL36x2 形态**，采用 x86 CPU 而非英伟达自研的 Grace CPU。这一形态名为 Miranda。我们认为每个计算托盘的 CPU 与 GPU 之比将保持不变，仍为每托盘 2 颗 CPU 和 4 颗 GPU。

我们认为，相比 Grace CPU 版本，这一 NVL72/NVL36x2 变体的前期资本开支更低，流入英伟达的营收也更少。由于使用 x86 CPU，CPU 与 GPU 之间的带宽将远低于 Grace C2C——后者与 GPU 的通信带宽最高可达 900GB/s 双向（450GB/s 单向）。正因如此，其 TCO 存疑。此外，x86 CPU 无法在 CPU 与 GPU 之间针对负载共享功率，所需的总峰值功率要高得多。[在我们的加速器模型中，我们拆解了前 50 大买家各自将部署哪些 GB200 形态及其确切数量。](https://www.semianalysis.com/p/accelerator-model)

## **功率预算估算**

我们估计每个计算托盘的最大 TDP 为 6.3kW。计算托盘的功耗大头来自两块 Bianca 板和托盘内的 8 把风扇。NVL72 的 NVSwitch 托盘无需跨机柜连接，因此功耗比 NVL36 低 170W。NVL36 则需要 18 条 1.6T ACC 线缆横向连接相邻机柜。NVLink 拓扑我们会在后续章节解释。NVL72 每柜 123.6kW 是总功耗，包含了从输入线缆（whip）的交流电整流为计算托盘所用直流电的转换损耗。

![](https://substack-post-media.s3.amazonaws.com/public/images/f5ad0462-6e86-411e-9b23-a6bc3c9a9732_756x789.png)
*来源：SemiAnalysis GB200 组件与供应链模型*

而 NVL36x2 的每个机柜最大 TDP 约 67kW，两柜合计约 132kW，比 NVL72 多耗约 10kW。

## **计算托盘示意图与布线**

GB200 NVL72/NVL36x2 的核心是 Bianca 板。每块 Bianca 板包含两颗 Blackwell B200 GPU 和一颗 Grace CPU。相比 CPU 与 GPU 之比为 1:1 的 GH200，现在板上比例变为 1:2。大多数评估过 GH200 的客户都告诉英伟达它太贵了——1:1 的 CPU 配比对他们的负载而言过高。这是 GH200 出货量远低于 HGX H100（2 颗 x86 CPU、8 颗 H100 GPU）的主要原因之一。[到了 Blackwell 这代，GB200 的出货量相对大幅上升，其出货量将超过 HGX Blackwell B100/B200（出现交叉）。](https://www.semianalysis.com/p/accelerator-model)

![](https://substack-post-media.s3.amazonaws.com/public/images/7c2a43a7-20ec-4f25-a0dc-de125b9cb28b_1114x835.png)
*来源：SemiAnalysis*

在 Hopper 与 Blackwell 的 HGX 服务器中，CPU 与 GPU 之间通常有 Broadcom 的 PCIe 交换芯片。而在 GB200 上，CPU 和 GPU 位于同一块 PCB 上，插入损耗降低到在参考设计中 CPU 与 GPU 之间不再需要任何交换芯片或重定时器的程度。表面上看这对 Astera Labs 极为不利。该公司目前自由流通股的空头仓位约有 35%，但这主要来自那些没有深入跟踪供应链、只知道参考设计里没有重定时器的人。我们将在下文及 [GB200 组件与供应链模型](https://www.semianalysis.com/p/semianalysis-gb200-component-and)中分享更多细节。

参考设计还有一个有意思的地方：不再使用典型的 MCIO PCIe x16 连接器把主 PCB 连到 PCIe 形态的 ConnectX-7/8 网卡，而是让 ConnectX-7/8 芯片通过 Mirror Mezz 连接器、借助一块夹层板直接「坐」在 Bianca 板上方。

![](https://substack-post-media.s3.amazonaws.com/public/images/878d17ca-bec2-426d-aaa6-55d2ddcf1414_1018x830.png)
*来源：SemiAnalysis*

这样做的好处是可以用同一块冷板同时冷却 CPU、GPU 和 ConnectX-7/8 NIC。电气通道从夹层板通过 DensiLink 连接器走线到机箱前部的 OSFP 笼。这与英伟达在其镀金 DGX H100 机箱上用 DensiLink 从 ConnectX-7 布线到 OSFP 笼的做法类似。

与双路 GH200 类似，同一计算托盘内有一条高速一致性（coherent）NVLink 连接，可提供最高 600GB/s 的双向带宽（300GB/s 单向）。这是一条极快的连接，使两颗 CPU 可以共享资源与内存，类似于拥有 2 颗 CPU 和 NUMA（非统一内存访问）区域的 HGX H100/B100/B200 服务器。

![](https://substack-post-media.s3.amazonaws.com/public/images/932bad1a-1bc1-46c2-a8a7-8c6a569f8739_1200x658.png)
*来源：Nvidia*

由于这条连接两块 Bianca 板的一致性链路，两颗 CPU 之间可以共享内存、存储和 NIC 等资源。因此，你可以少装一块前端 NIC——每个计算托盘只需 1 块前端 NIC，而不是参考设计建议的 2 块。这与 x86 服务器的情况类似：即便一台服务器有 2 颗 CPU，也只需要 1 块前端 NIC，因为 CPU 之间可以共享资源。这一点我们会在前端网络部分再展开。

![](https://substack-post-media.s3.amazonaws.com/public/images/73d2e1aa-dd53-4536-a62b-b7f935c6319b_1870x1238.png)
*来源：SemiAnalysis*

至于 2,700 瓦功率如何送到板上：在 CPU 和 GPU 各自的电压调节模块（VRM）周围，分布着 4 个 RapidLock 12V 直流和 4 个 RapidLock 接地（GND）电源连接器。这些 12V 与 GND 电源连接器将连到计算托盘的配电板（PDB）。配电板从机柜级母排取 48V 直流电，降压为 Bianca 板所用的 12V 直流电。系统供电网络的变化，我们会在后文的供电部分讨论。

![](https://substack-post-media.s3.amazonaws.com/public/images/53f25091-a84e-422b-a265-d53e2a54bed7_839x944.png)
*来源：SemiAnalysis*

在计算托盘内部的线缆+连接器方面，成本大头是把 ConnectX-7/8 夹层板连到 Bianca 板的 Mirror Mezz 连接器，以及从 ConnectX-7/8 连到机箱前部 OSFP 笼的 DensiLink 线缆。

![](https://substack-post-media.s3.amazonaws.com/public/images/d8d3ba20-4a5a-4954-b8ba-40385c5be131_2238x1090.png)
*来源：SemiAnalysis GB200 组件与供应链模型*

英伟达参考设计中，每个计算托盘配两块 BlueField-3，但正如后文所解释的，我们认为大多数公司根本不会选用任何 BlueField-3。机箱前部可以看到所有常见的服务器管理端口，如 RJ45、USB 等。还有八个 NVMe 存储位用于本地节点级存储，以及横向扩展（scale-out）后端的 OSFP 笼。

![](https://substack-post-media.s3.amazonaws.com/public/images/389429cd-dbb4-4221-93be-4d312f1bc1ac_1833x802.png)
*来源：SemiAnalysis*

后端笼子引出 GB200 最关键的议题之一：网络。

## **网络**

与 HGX H100、AMD MI300X、Intel Gaudi、AWS Trainium 类似，GB200 系统中有 4 种不同的网络：

- 前端网络（普通以太网）
- 后端网络（InfiniBand/RoCE 以太网）
- 加速器互连（NVLink）
- 带外管理网络

快速回顾一下：**前端网络**就是你用来连接互联网、SLURM/Kubernetes、网络存储、数据加载和模型检查点（checkpoint）的普通以太网。这一网络通常为每 GPU 25-50Gb/s，因此在 HGX H100 服务器上是每台 200-400Gb/s，而在 GB200 计算托盘节点上，视配置不同为每台 200-800Gb/s。

你的**后端网络**用于在上百到上千个机柜之间横向扩展 GPU-GPU 通信。这张网络可以是英伟达的 InfiniBand，也可以是英伟达 Spectrum-X 以太网或 Broadcom 以太网。而[英伟达的方案要比 Broadcom 以太网方案贵得多](https://www.semianalysis.com/p/100000-h100-clusters-power-network)。

**纵向扩展的加速器互连**（[英伟达的 NVLink](https://www.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband)、AMD 的 Infinity Fabric/UALink、[Google TPU 的 ICI](https://www.semianalysis.com/p/google-ai-infrastructure-supremacy)、Amazon Trainium 2 的 NeuronLink）是在单个系统内把 GPU 连接起来的超高速网络。在 Hopper 上，这张网络以每颗 450GB/s 的速率连接 8 颗 GPU；而在 Blackwell NVL72 上，它将以每颗 900GB/s 的速率连接 72 颗 GPU。Blackwell 有一个叫 NVL576 的变体，可连接 576 颗 GPU，但基本不会有客户选择它。总体而言，加速器互连的速度是后端网络的 8-10 倍。

最后是你的**带外管理网络**，用于重装操作系统镜像、监控节点健康状况（如风扇转速、温度、功耗等）。服务器、PDU、交换机、CDU 上的基板管理控制器（BMC）通常都连到这张网络，对这些 IT 设备进行监控和控制。

## **NVLink 纵向扩展互连**

与 HGX H100 相比，GB200 的前端、后端和带外网络基本相同，唯一的例外是 NVLink 走出了机箱之外。各代之间不同的只有超大规模云厂商的定制部分。此前在 HGX H100 上，8 颗 GPU 和 4 颗 NVSwitch4 交换 ASIC 位于同一块 PCB（HGX 基板）上，因此用 PCB 走线相连。

![](https://substack-post-media.s3.amazonaws.com/public/images/14e66ac8-fe87-4487-9cca-9f65963b4ac5_1871x827.png)
*来源：SemiAnalysis*

而在 HGX Blackwell 上，NVSwitch ASIC 被放到中间位置，以便在升级到 224G SerDes 的情况下缩短 PCB 走线长度。

但在 GB200 上，NVSwitch 与 GPU 位于不同的托盘，因此二者之间必须使用光模块或 ACC（有源铜缆）来连接。

![](https://substack-post-media.s3.amazonaws.com/public/images/d805bbe1-628f-4252-a9d1-145c8fd0ae9e_1918x1058.jpeg)
*来源：Nvidia*

在 NVL72 中，英伟达沿用了与 HGX Hopper/Blackwell 相同的单层扁平 NVLink 拓扑，只需经过 1 跳 NVSwitch 就能和同机柜内的任意 GPU 通信。这与 AMD 和 Intel 当前一代不经交换机、GPU 点对点直连的互连不同——那种做法会导致加速器之间的带宽降低。

![](https://substack-post-media.s3.amazonaws.com/public/images/1c831628-5bc7-4582-9edf-8110eb1fa616_1365x834.png)
*来源：SemiAnalysis*

在 NVL36x2 中，到达同机柜内任意 36 颗 GPU 只需 1 跳，但要与隔壁机柜的另外 36 颗 GPU 通信，则需要跨机柜共 2 跳 NVSwitch。直觉上，多出的这一跳会增加时延，但对训练来说并不明显。它会轻微影响推理，但影响不大——[除非目标是 batch 1、不用投机解码（speculative decoding）的超高交互性（>500TPS）场景](https://www.semianalysis.com/p/nvidia-blackwell-perf-tco-analysis)。注意，这是相当不现实的场景，我们预计没有人会这么用。

![](https://substack-post-media.s3.amazonaws.com/public/images/a667c930-3e9d-4aba-be30-563e486bf437_767x973.png)
*来源：SemiAnalysis*

英伟达声称，如果使用带收发器的光模块方案，每个 NVL72 机柜就需要多加 20kW。我们自己算了一笔账：需要 648 个 1.6T 双端口收发器，每个收发器功耗约 30 瓦，算下来是 19.4kW/柜，与英伟达的说法基本一致。按每个 1.6T 收发器约 850 美元计算，仅收发器成本一项就是每柜 550,800 美元。再叠加英伟达 75% 的毛利率，最终客户要为每柜 NVLink 收发器支付 2,203,200 美元。[这正是 DGX H100 NVL256 最终未能出货的主要原因之一——收发器成本过于庞大。](https://pytorchtoatoms.substack.com/p/why-dgx-h100-nvl256-never-shipped)此外，1.6T NVLink 收发器这类最尖端的收发器，其可靠性远差于铜缆，甚至也差于上一代光模块。

正因如此，英伟达选择使用 5,184 根铜缆——一个便宜得多、功耗低得多、也更可靠的选项。每颗 GPU 拥有 900GB/s 的单向带宽。每对差分线（DP）能单向传输 200Gb/s，因此每颗 GPU 双向共需 72 对差分线。由于每个 NVL72 机柜有 72 颗 GPU，就意味着共需 5,184 对差分线。每根 NVLink 线缆包含 1 对差分线，因此共有 5,184 根线缆。

这使得铜的用量较上一代大幅增加。让人哭笑不得的是，我们看到一些投资者估算每颗 GPU 的 NVLink 互连用量价值约 3k 美元，总计每 NVL72 机柜 216k 美元——但这完全错误。

![](https://substack-post-media.s3.amazonaws.com/public/images/157775a3-bc51-4aef-8aa7-5b678a4a6a4f_1396x729.jpeg)
*来源：Coatue*

首先，人们是怎么得出每 GPU 3,000 美元这种离谱数字的？我们认为，他们拿了每颗 GPU 900GB/s（7,200Gb/s）的单向带宽，再对比零售价 162 美元的 400Gb/s 铜缆。由于每颗 GPU 需要 18 根 400Gb/s 全双工线缆，这样算出来每 GPU 就是 3k 美元。这个数字错得离谱。

![](https://substack-post-media.s3.amazonaws.com/public/images/8dc8b4d1-067f-4a63-857e-f83ed8f4877d_1359x784.png)
*来源：SemiAnalysis*

此外还有一个误解，以为线缆本身很贵。其实成本大头不在缆线本身，而在缆线的端接和连接器上。连接器之所以昂贵，是因为它们必须防止不同差分对之间的串扰。串扰非常有害：它会让其他信号变得模糊，导致解串器读出错误的比特位。英伟达选择采用 Amphenol 的 Ultrapass Paladin 背板产品作为其 NVLink 背板互连的首个主供货源。

**本文中各连接器与线缆均以主供应商名称指代，但实际上每类都有 3 家供应商、份额随时间变化，细节在我们的完整版 [GB200 组件与供应链模型](https://www.semianalysis.com/p/semianalysis-gb200-component-and)中分享**

![](https://substack-post-media.s3.amazonaws.com/public/images/e2220e1b-fe40-4a49-bb5a-e6fa7dfe78ef_1462x773.png)
*来源：SemiAnalysis*

每颗 Blackwell GPU 连接到一个 Amphenol Paladin HD 224G/s 连接器，每个连接器有 72 对差分线。然后，该连接器接到背板上的 Paladin 连接器。接下来，通过 SkewClear EXD Gen 2 线缆连到 NVSwitch 托盘的 Paladin HD 连接器（每个连接器 144 对差分线）。从 NVSwitch 的 Paladin 连接器到 NVSwitch ASIC 芯片，则需要 OverPass 飞越线缆，因为每个交换托盘有 4 个 144 对差分线连接器（共 576 对），在如此小的面积内走 PCB 走线会产生过多串扰。况且 PCB 上的损耗也比飞越线缆更大。

![](https://substack-post-media.s3.amazonaws.com/public/images/fa081534-6de4-4734-9f6d-395c7f06fe8f_2814x800.png)
*来源：SemiAnalysis GB200 组件与供应链模型*

在 NVL36x2 中，每套系统还需要额外的 162 条 1.6T 双端口横向 ACC 线缆（[价格极其昂贵](https://www.semianalysis.com/p/semianalysis-gb200-component-and)），用于连接 A 柜与 B 柜之间的 NVSwitch 托盘。[我们在此拆解了 ACC 线缆与芯片市场](https://www.semianalysis.com/p/semianalysis-gb200-component-and)：有多家份额可观的玩家。此外，OSFP 笼还需要额外 324 条 DensiLink 飞越线缆。仅这些 DensiLink 飞越线缆，每个 NVL36x2 就要增加超过 10,000 美元的成本。

![](https://substack-post-media.s3.amazonaws.com/public/images/b70f55ce-757d-4e8b-aa25-1db9392f2ce9_1262x833.png)
*来源：SemiAnalysis*

另外，实现 A 柜与 B 柜之间的连接还需要两倍数量的 NVSwitch5 ASIC。这将使 NVLink 铜缆总成本相比 NVL72 **增加超过一倍**。

尽管 NVL36x2 的 NVLink 背板用量成本是 NVL72 的两倍多，但由于功率和散热限制（下文详述），大多数客户仍会选择 NVL36x2 设计。需要说明的是，虽然价格不菲，但 NVL36x2 和 NVL72 的铜缆成本都比投资界以为的要低。

![](https://substack-post-media.s3.amazonaws.com/public/images/317da70f-8d52-4696-a48d-a8aac2d89968_2514x924.png)
*来源：SemiAnalysis GB200 组件与供应链模型*

真正的赢家是供应链中的线缆厂商和有源铜缆芯片厂商——随着 NVL36x2 的大行其道，他们在尖端 1.6T 产品上的出货量将大幅增长。

## **GB200 NVL576**

正如黄仁勋在台上所说，GB200 NVLink 可以将 576 颗 Blackwell GPU 连为一体。我们认为这是通过 18 个平面（plane）的两层胖树（fat tree）拓扑实现的。这类似于他们为 DGX H100 NVL256 规划的、连接 16 个 NVL36 机柜的方案。它将使用 288 颗 L1 NVSwitch5 ASIC（144 个 1U 交换托盘），像 NVL36x2 一样布置在计算机柜内；同时使用 144 颗 L2 NVSwitch ASIC（72 个 2U 交换托盘），布置在专用的 NVSwitch 托盘上。与 NVL36x2 一样，GPU 与 L1 NVSwitch 之间的连接由于距离短，将采用同样的铜背板。

![](https://substack-post-media.s3.amazonaws.com/public/images/0e566941-e7c5-4617-9c4d-12ce0c49f347_1909x762.png)
*来源：SemiAnalysis*

遗憾的是，L1 NVSwitch 与 L2 NVSwitch 之间的距离超出了铜缆的能力范围，因此必须使用光连接。此外，L2 NVSwitch 还要用飞越线缆连到机箱前部的 OSFP 笼。NVL576 的新增 BOM 成本是一个天文数字：英伟达需要向供应商支付超过 560 万美元（每颗 GPU 9.7k 美元）。

若再统一叠加 75% 的毛利率，客户要为 NVL576 的铜缆+光连接额外支付每颗 GPU 38.8k 美元。虽然英伟达可以压缩利润率，但即便这套纵向扩展 NVLink 方案按 0% 毛利卖，也基本上站不住脚。[这与 DGX H100 NVL256 因收发器成本庞大而从未出货的原因一模一样](https://pytorchtoatoms.substack.com/p/why-dgx-h100-nvl256-never-shipped)。光方案对加速器互连来说实在太贵，因为加速器互连必须具备极高的带宽。

![](https://substack-post-media.s3.amazonaws.com/public/images/7ab8deb2-bc40-4a04-b3cf-b26270f469ff_2730x482.png)
*来源：SemiAnalysis GB200 组件与供应链模型*

## **后端网络**

GB200 的后端网络是选项最集中的地方。英伟达通常会在发布 GPU 时同步准备好新一代 NIC 和交换机，但这一代由于英伟达的时间表过于激进（尤其是 224G SerDes），新网络要等到 Blackwell 这一代的中途才会就绪。因此，GB200 的所有首批出货都将沿用大多数 H100 服务器所配的 ConnectX-7。

在后端网络方面，客户会根据所用 NIC 选择以下几类交换机：

- Quantum-2 QM9700 InfiniBand NDR
- Quantum-X800 QM3400 InfiniBand XDR
- Quantum-X800 QM3200 InfiniBand NDR/XDR
- Spectrum-X SN5600
- Spectrum-X Ultra
- Broadcom Tomahawk 5
- Broadcom Tomahawk 6

就后端网络而言，抢首批的出货将全部使用 QM9700 Quantum-2 交换机或 Broadcom Tomahawk 5，与 H100 世代相同。尽管后端网络硬件相同，采用[轨道优化（rail optimized）设计](https://www.semianalysis.com/p/100000-h100-clusters-power-network)却有一大难题：交换机端口数与机柜端口数失配。NVL72 的每个计算托盘有 4 颗 GPU，这意味着在 4 轨优化设计下，每台 Quantum-2 交换机应有 18 个下行端口。

![](https://substack-post-media.s3.amazonaws.com/public/images/b31559f8-d744-4057-b7ef-e82e77d83e47_1099x767.png)
*来源：SemiAnalysis*

由于胖树中每台交换机的上行端口数相同，这意味着 64 个端口中只有 36 个会被使用。实际上，每台交换机都会有大量空闲端口。如果每台交换机接 2 条轨道，那就是 72 个端口，又超过了 QM9700 Quantum-2 交换机的容量。为了用满每台 Quantum-2 交换机的所有端口，每 4 个 NVL72 机柜需要配 9 台非轨道优化的 leaf 交换机。

![](https://substack-post-media.s3.amazonaws.com/public/images/20e9a6ad-0849-44da-870e-f370a399e030_1592x847.png)
*来源：Nvidia*

对于 ConnectX-7，还可以使用 Q3200 Quantum-3 交换托盘，其中包含 2 台独立交换机，各有 36 个 400Gb/s 端口。这不存在端口失配问题，每个 NVL72 可配 4 台 Q3200 Quantum-X800 交换机实现 4 轨优化。

![](https://substack-post-media.s3.amazonaws.com/public/images/02f8348b-4042-4d02-aa94-48fb226a047b_1586x855.png)
*来源：Nvidia*

至于升级到 800Gb/s 的 ConnectX-8（2025 年第二季度起出货），将搭配 Quantum-X800 Q3400——它有 144 个 800Gb/s 端口，分布在 72 个双端口 OSFP 笼上。由于没有端口失配，大多数客户会选择英伟达推荐的设计：4 轨优化，交换机机柜采用列尾（EoR）布置。

搭配 CX-8，还可以使用 Spectrum-X Ultra 800G，省掉上一代所必需的昂贵 BlueField 选项。[我们在此讨论了 Quantum-X800 交换机方案及其对光收发器市场的影响。](https://www.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband)基于 Broadcom Tomahawk 6 的部署变体也将于明年下半年到来。

![](https://substack-post-media.s3.amazonaws.com/public/images/067029ea-ebf0-4f20-93ff-64b79c85bf5c_1265x818.png)
*来源：SemiAnalysis*

从 CX-7 到 CX-8 的过渡，将是从 400G（4x100G）SR4 光收发器转向 800G（4x200G）DR4 光收发器的主要推手。在 GB200 NVL72 上使用 CX-7 时，每颗 GPU 有 400G 带宽，通过一个 OSFP 笼连接多模 [400G 单端口 SR4 收发器](https://docs.nvidia.com/networking/display/mma4z00ns400)——它有四条光通道，每条由一个多模 100G VCSEL 驱动。在基于 CX-7 的网络中，交换机一侧通常使用 800G 双端口 SR8 或 DR8 收发器。

到了 CX-8，所有速率翻倍：每颗 GPU 800G（4x200G）DR4，交换机端每个 OSFP 笼 1.6T（8x200G）DR8。由于 200G 多模 VCSEL 的开发工作还要 9 到 18 个月才能完成、赶不上 1.6T 爬坡，业界转而采用单模 200G EML。

[与 DGX H100 类似，还将提供 Cedar-8 方案：每块 Bianca 板上的两颗 CX-8 NIC 芯片进入同一个 OSFP224 笼](https://pytorchtoatoms.substack.com/p/nvidia-connectx-7-16tbits-cedar-fever)。其优势在于用两个 1.6T（8x200G 通道）双端口收发器取代四个 800G（4x200G 通道）单端口收发器。由于 4x200G 单端口收发器比 8x200G 双端口收发器便宜约 35%，用 Cedar-8 取代两个 4x200G 收发器可降低 30% 成本。不过，在计算托盘的单个 OSFP 笼里塞进 2 倍带宽会带来散热难题，因此我们预计大多数公司不会使用 Cedar-8。

发布之初，大多数公司将坚持使用 ConnectX-7/ConnectX-8。即便是 Google 这样历史上一直使用 Intel 等厂商定制后端 NIC 的公司，也将改回英伟达的 ConnectX-8 NIC。

唯一会集成自家后端 NIC 的例外是 Amazon。我们认为他们会使用定制的 400G（4x100G）后端 NIC。这张网卡与他们的标准 Nitro NIC 不同，将主要面向性能。

![](https://substack-post-media.s3.amazonaws.com/public/images/6780aeb7-04f2-4221-b4bf-b9d7564992c4_1025x816.png)
*来源：SemiAnalysis*

要在 Bianca 板上使用定制后端 NIC、而不是在夹层板上使用 ConnectX 芯片，就需要一块转接夹层板，从 Mirror Mezz 连接器分出 8 个 MCIO PCIe 连接器，一直走到机箱前部。

![](https://substack-post-media.s3.amazonaws.com/public/images/ac7b70d0-3203-4ef8-b096-d845aed55c16_2048x1536.jpeg)
*来源：HighYieldYT*

由于系统里没有 ConnectX-7/8，也没有 BlueField-3（两者均集成 PCIe 交换），要连接后端 NIC 与 CPU、GPU，就需要 Broadcom/Astera Labs 的独立 PCIe 交换芯片。在 [SemiAnalysis GB200 组件与供应链模型](https://www.semianalysis.com/p/semianalysis-gb200-component-and)中，我们拆解了 PCIe 交换芯片的供应商、出货量和 ASP。超大规模云厂商的定制设计中仍有在 CPU 与 NIC 之间放 PCIe 交换芯片的。英伟达的 Miranda 设计在 PCIe 通道处理上也与 GB200 有很大不同。此外 [Amazon Trainium 2 部署中含有大量 Astera Labs 的重定时器](https://www.semianalysis.com/p/accelerator-model)。

使用定制 NIC 会给公司带来额外的工程工作：他们无法使用默认的水冷块——那个水冷块是连 ConnectX 芯片一起冷却而设计的。他们还需要重新做热仿真，确保机箱前部的定制 NIC 有足够的散热能力、不会过热。此外，他们也无法使用 NVL72 所用的 1U 计算托盘版本。

他们只能选择 2U 的 NVL36 版本，因为其托盘前部有足够的风冷能力。所有这些额外工程工作都会拖慢 Amazon 以及任何其他想用定制后端 NIC 的厂商的上市时间。正是这些难题，让 Google 放弃继续使用 Intel 的 IPU，转而在其 GB200 服务器上使用 ConnectX-8。

## **前端网络**

参考设计中，每个计算托盘配两块 400Gb/s 的 BlueField-3。由于每个计算托盘有 4 颗 GPU，相当于每颗 GPU 分到 200Gb/s 的前端带宽。如今部署的最先进 HGX H100 服务器，前端流量只用一块 200-400Gb/s 的 ConnectX-7 NIC——那是给 8 颗 GPU 用的，即每颗 GPU 25-50Gb/s。每 GPU 200Gb/s 的前端带宽是一个极端数字，大多数客户不会为这项额外成本买单。总体而言，英伟达的参考设计是按绝对最坏情况过度配置的，为的是多卖你一些用料。

![](https://substack-post-media.s3.amazonaws.com/public/images/efa40b54-5fc5-43f2-b491-e616967e8d48_1739x760.png)
*来源：SemiAnalysis*

我们认为唯一会把 BlueField-3 用作前端 NIC 的大客户是 Oracle。他们运营的云服务需要前端网络虚拟化，但又不像其他超大规模云厂商那样已部署了定制 NIC 方案。Amazon、Google 和 Microsoft 都有自研前端 NIC，目前已用于其全部通用 CPU 服务器和加速计算服务器。他们打算继续使用这些方案，因为其 TCO 优势显著，而且已经与其网络/云软件栈垂直整合。

讽刺的是，唯一在 AI 集群中大规模使用 BlueField-3 的公司（xAI）甚至没有把它用于其本来的 DPU 用途。xAI 的 BlueField-3 工作在 NIC 模式而非 DPU 模式，因为第一代英伟达 Spectrum-X 以太网需要一个权宜之计——用 BlueField-3 充当后端 NIC。Spectrum-X800 Ultra 将可与 CX-8 后端 NIC 配合工作，不再需要 BlueField-3/4 才能正常运行。

![](https://substack-post-media.s3.amazonaws.com/public/images/81d84f83-e8bf-4244-a025-9d57c9645e82_1378x761.png)
*来源：SemiAnalysis、Michael Dell*

### **网络线缆+收发器物料清单**

下面我们计算了英伟达向合约制造商支付的物料清单成本。我们只计算计算托盘/NVSwitch 托盘一端的收发器成本，因为一旦把交换机算进来，计算会变得复杂——集群可能是 2 层或 3 层，超大集群甚至 4 层。

![](https://substack-post-media.s3.amazonaws.com/public/images/4f44375f-4d0a-46ed-bc11-040d2399267a_2542x1152.png)
*来源：SemiAnalysis GB200 组件与供应链模型*

可以看到，搭配 ConnectX-8 时，用 TOR（Top of Rack）设计加 DAC/ACC 铜缆取代 4 轨优化后端设计，仅后端网络一项就能省下约 32k 美元。遗憾的是，由于计算机柜的功率约束非常紧，我们认为大多数人将不得不把后端交换机放到另外的服务机柜中，并用光模块来连接。

带外管理则全部是便宜的铜质 RJ45 线缆（每条不到 1 美元），把计算/交换托盘连到机柜顶部的带外管理交换机。如前所述，参考设计在前端 NIC 数量和带宽上属于过度配置。**我们认为大多数公司只会配 200G 前端带宽，而不是 2 块 BF-3（每个计算托盘合计 800Gb/s 带宽）。**仅收发器成本一项，这就能为每套系统省下 3.5k 美元。

![](https://substack-post-media.s3.amazonaws.com/public/images/7e918707-4d7f-4016-99aa-33cf343c8550_2542x1208.png)
*来源：SemiAnalysis GB200 组件与供应链模型*

在光模块与 DSP 方面，英伟达正在大举扩充供应链：从原来占绝对主导的 Fabrinet 和 Innolight（中际旭创），扩展到 Eoptolink（新易盛）。Eoptolink 将专注于 800G LPO 和带 DSP 的 1.6T。

DSP 的格局也在剧变。上一代 H100 上，Marvell 在英伟达处是 100% 份额。这一代，Broadcom 大举进场。我们看到 Innolight 和 Eoptolink 都打算大量引入 Broadcom 的 DSP。

此外，英伟达招聘了一批 DSP 工程师，并流片了一款 1.6T DSP。我们认为它短期内不会量产，但若量产，将用于 Fabrinet 的收发器。自研 DSP 量产的最大挑战在于：英伟达在 DSP 两侧使用的基本上是同一种长距离、高功耗 SerDes。通常，DSP 面向光模块一侧和面向 NIC/交换机一侧的 SerDes 会做不同的优化。而英伟达这两套 SerDes 都更偏重功率优化而非单纯传输距离——这正是英伟达设计 224G SerDes 时的主要优化点。英伟达的自研 DSP 功耗大得惊人，因此在本就滚烫的 1.6T 收发器里，散热难题使其自研 DSP 很难上量。英伟达的这款 DSP 需要时也可以兼作重定时器，不过 ACC 已经够用了。

光模块供应商与 DSP 的市场份额及 ASP，见 [SemiAnalysis GB200 组件与供应链模型](https://www.semianalysis.com/p/semianalysis-gb200-component-and)。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

以上只是高层概览和基础知识。下文我们将深入 GB200 的所有子组件与 BOM，包括封装基板（substrate）、PCB、CCL、封装基板、液冷、边柜（Sidecar）、CDU、UQD、分液管（Manifold）、均热板（Vapor Chamber）、冷板、BMC 和供电。我们还会进一步讨论超大规模定制，以及液冷供应链选择的各种复杂细节和决策矩阵。
