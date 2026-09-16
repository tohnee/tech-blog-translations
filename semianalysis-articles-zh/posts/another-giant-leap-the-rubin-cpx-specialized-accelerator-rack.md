---
title: "又一次巨大飞跃：Rubin CPX 专用加速器与机柜"
title_en: "Another Giant Leap: The Rubin CPX Specialized Accelerator & Rack"
subtitle: "全新预填充专用 GPU、机柜架构、BOM、PD 分离、更高的单位 TCO 性能与更低的 TCO、GDDR7 与 HBM 市场趋势"
date: 2025-09-10
source: https://newsletter.semianalysis.com/p/another-giant-leap-the-rubin-cpx-specialized-accelerator-rack
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball", "Kimbo Chen", "Wega Chu", "Ivan Chiam", "Cheang Kang Wen"]
tags: ["Hardware Architecture", "Accelerators"]
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 又一次巨大飞跃：Rubin CPX 专用加速器与机柜

> 原文：[Another Giant Leap: The Rubin CPX Specialized Accelerator & Rack](https://newsletter.semianalysis.com/p/another-giant-leap-the-rubin-cpx-specialized-accelerator-rack) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**全新预填充专用 GPU、机柜架构、BOM、PD 分离、更高的单位 TCO 性能与更低的 TCO、GDDR7 与 HBM 市场趋势**

Nvidia 发布了 Rubin CPX——一款专为预填充（prefill）阶段优化设计的解决方案，单裸片（single-die）的 Rubin CPX 大幅强调计算 FLOPS 而非内存带宽。这对推理而言是一款改变游戏规则的产品，其意义仅次于 2024 年 3 月发布的 GB200 NVL72 Oberon 机柜级形态。只有针对推理中截然不同的两个阶段——预填充与解码（decode）——分别采用专用硬件，分离式服务（disaggregated serving）才能充分发挥其潜力。

其结果是，Nvidia 与竞争对手之间的机柜系统设计差距已经拉大到峡谷般宽。AMD 和定制芯片竞争对手或许在模仿 Nvidia 的 72-GPU 机柜级设计上迈出了一小步，但 Nvidia 刚刚又完成了一次巨大飞跃，再度把竞争对手甩成后视镜中遥不可及的影子。

AMD 和 ASIC 供应商早已在各自机柜级解决方案上投入巨资以图追赶。尤其是 AMD，一直在不遗余力地改进其软件栈，试图缩小与 Nvidia 的差距；但现在所有厂商都不得不再次加倍投入，因为它们必须开发自己的预填充芯片，这将进一步推迟它们缩小差距的时间表。随着此次发布，Nvidia 的所有竞争对手都将被推回绘图板前，重新调整各自的整条路线图——一如当年 Oberon 改写全行业路线图的重演。

## Rubin CPX

由于推理中的预填充阶段往往大量消耗计算（FLOPS），而仅轻度使用内存带宽，在配备大量昂贵 HBM、内存带宽极高的芯片上运行预填充是一种浪费。答案是一款内存带宽精简、计算相对富余的芯片。Rubin CPX GPU 应运而生。

![](https://substack-post-media.s3.amazonaws.com/public/images/cf35ef32-a85b-448d-97ff-673a3c719b1e_600x338.jpeg)
*来源：Nvidia*

Rubin CPX 提供 20 PFLOPS 的 FP4 密集（dense）算力，但内存带宽仅 2TB/s。它还配备 128GB GDDR7 内存——相比 VR200，这是容量更低、价格也更低的内存。作为对比，双裸片的 R200 芯片提供 33.3 PFLOPS 的 FP4 密集算力，以及 288GB HBM，内存带宽达 20.5 TB/s。

![](https://substack-post-media.s3.amazonaws.com/public/images/8a405e7b-c078-4ad5-9969-49ebdc0c5eaa_2560x1138.png)
*来源：SemiAnalysis、Nvidia*

Rubin CPX 的引入使 VR200 系列机柜级服务器扩展为三种形态：

1. VR200 NVL144：18 个计算托盘（compute tray）共 72 个 GPU 封装，每个计算托盘 4 个 R200 GPU 封装。
2. VR200 NVL144 CPX：18 个计算托盘中，除 72 个逻辑 GPU 封装外还有 144 个 Rubin CPX GPU 封装，每个计算托盘含 4 个 R200 GPU 封装和 8 个 Rubin CPX GPU 封装。
3. Vera Rubin CPX 双机柜（Dual Rack）：两个相互独立的机柜——一个 VR200 NVL144 机柜，加一个容纳 144 颗 Rubin CPX GPU 的 VR CPX 机柜，后者由 18 个计算托盘组成，每个计算托盘 8 颗 Rubin CPX GPU。

![](https://substack-post-media.s3.amazonaws.com/public/images/66962758-4765-4f78-89fc-0bf2ebd90229_1489x1091.png)
*来源：SemiAnalysis、Nvidia*

在本报告中，我们将首先梳理迄今为止的脉络，说明内存在推理的预填充与解码阶段所扮演的不同角色，以及由此催生 Rubin CPX 的动因。随后我们将深入剖析 Rubin CPX 芯片的架构及其所部署的机柜级解决方案。接着，我们将把焦点从过去与现在转向未来——分离式推理服务的前景，以及今日发布对其他商用加速器供应商和定制芯片项目未来路线图与竞争力的影响。在本文最后一部分，我们将简要给出两款机柜的关键物料清单（BoM）条目汇总，并按主要部件组别做功耗预算分析。

## 内存：迄今为止的故事

内存墙（memory wall）一直是 AI 最重要的约束。更大的内存容量是将更大的模型装载进加速器所必需的，而内存带宽则是推理和训练 token 吞吐的主要瓶颈因子。正因如此，单 GPU 的高带宽内存（HBM）容量与带宽快速增长——从 H100 的 80GB 和 3.4TB/s 到 GB300 的 288GB 和 8.0TB/s，不到三年时间内存容量增长逾三倍、带宽提升约 2.5 倍。

因此，从 Hopper 到 Blackwell，HBM 在加速器 BOM 中的占比持续攀升，如今 HBM 已成为 GB300 封装 BOM 中最大的单一组件。HBM 对训练和推理都极具价值，但当我们把推理拆解为预填充与解码两个组成步骤时，HBM 仅在解码步骤具有高价值。预填充是计算密集型的，由于预填充天然的并行性，KV 缓存（KVCache）的生成对带宽的占用要低得多，因此 HBM 在这一步骤中被低度利用。

HBM 因其额外的带宽而在价格上远高于其他形态的 DRAM，而当这部分带宽（B/W）被低度利用时，这些 HBM 就被“浪费”了。HBM 占 BOM 比例的不断攀升构成了又一面“墙”，正是 Rubin CPX GPU 研发背后的动因。

![](https://substack-post-media.s3.amazonaws.com/public/images/36207d0b-cff5-49f9-9c82-dff9bf0c06d1_2121x921.png)
*来源：SemiAnalysis*

在简要回顾内存迄今扮演的角色之后，让我们转向今日的发布，详细剖析 Rubin CPX 的架构及其所部署的机柜级服务器。

## 带宽与算力差异

每颗 Rubin CPX 芯片都将是采用传统倒装芯片 BGA 封装的单片式（monolithic）SoC。Rubin CPX 不用 HBM，而是配备 128GB GDDR7 DRAM。从 HBM 转向更便宜的 GDDR7 内存，可使每 GB 成本降低超过 50%。

内存速率大概率为 32Gbps，配合 512-bit 总线。这使得每颗 Rubin CPX 的内存带宽为 2TB/s，而每颗 R200 为 20.5TB/s。值得注意的是，借本次主题演讲，Nvidia 还确认了对常规版 Rubin 的一次重大带宽升级。正如我们此前在[加速器与 HBM 模型](https://semianalysis.com/accelerator-hbm-model/)中所讨论的，R200 的 HBM4 速率已大幅提升至 10Gbps，以实现每颗 R200 20.5TB/s 的内存带宽。相比之下，R200 首次发布时“仅”标称 13TB/s 内存带宽规格、对应 6.4Gbps 速率档。我们在该模型中也讨论并量化了[其对 HBM 供应商的影响](https://semianalysis.com/accelerator-hbm-model/)。144 颗各提供 2.0 TB/s 内存带宽的 CPX 芯片，加上 72 颗各提供 20.5TB/s 的 R200 芯片，合计可提供 1.7PB/s 的系统总内存带宽。

算力方面，每颗 CPX 提供 30 PFLOPS 的稀疏（sparse）FP4 计算吞吐（密集 20 PFLOPS），相比之下 R200 为稀疏 FP4 50 PFLOPS（密集 33.3 PFLOPS）。Rubin CPX 的密集 PFLOPS 与 R200 遵循同样的 3:2 稀疏/密集比率，因为它继承了与 Rubin R200 相似的张量核心架构。相对于采用两颗裸片的 R200，CPX 以单颗计算裸片提供了非常强劲的 FP4 计算吞吐。提升很可能来自削减更高精度的计算单元、换装更多 FP4 ALU。B300 就采用了这种做法，在沿用同一 4NP 制程节点的情况下获得了比 B200 更高的 FP4 吞吐。

然而，一如既往，理论峰值 FLOPS 在实践中极难企及。与 Nvidia 其他受功耗限制的 GPU 一样，Rubin CPX 很难持续运行在接近峰值 FLOPS 的水平——我们估计其额定功率仅在 800W 左右：我们认为突破 1W/mm2 的功率密度并不现实，尤其考虑到该板卡以“三明治”叠层形态集成（下文详述）。

另一个不同之处在于网络。Rubin CPX 没有用于纵向扩展（scale-up）的 NVLink SerDes，而是依靠 PCIe Gen 6，通过横向扩展（scale-out）网络上的 CX-9 NIC 与其他 GPU 通信。这种精简的网络能力完全够用，前提是采用下文讨论的流水线并行（pipeline parallelism）。

![](https://substack-post-media.s3.amazonaws.com/public/images/973a9e92-1304-4818-8390-1abcf7da7866_1984x1149.png)
*来源：SemiAnalysis 加速器与 HBM 模型、AI TCO 模型；以上图表仅为示意*

得益于更少的硅片总用量和更便宜的内存，Rubin CPX 的生产成本远低于 R200。降低内存总容量并改用成本更低的 GDDR7，意味着内存成本降至 1/5。芯片架构也简单得多：由于不用 HBM、只有单一光罩极限（reticle）尺寸的裸片且没有任何 I/O 小芯片（chiplet），因此无需 CoWoS 封装。作为参照，Rubin CPX 的设计类似于下一代的 RTX 5090 或 RTX PRO 6000 Blackwell，两者都采用大单片裸片配 512-bit 宽的 GDDR7 内存接口。由于这些芯片基于消费级 Blackwell GPU 裸片，它们的 FLOPS 仅为配备 HBM 的老大哥 B200 的 20%。而 Rubin CPX 将这一比例提升到 60%，因为它将是一次独立流片（tape-out），设计上更接近 R200 的计算裸片。作为追求单位成本最大 FLOPS 的一次实践——Rubin CPX 无出其右。

在本文后段，我们将拆解 Rubin CPX 的 BOM 优势，并估算把预填充从 R200 迁移到 Rubin CPX 上能节省多少成本。

## Nvidia Oberon 机柜架构升级：VR NVL144 CPX、VR NVL144、VR CPX

现在让我们把视线从 Rubin CPX 芯片移开，转向承载 CPX 的两款全新 Vera Rubin 机柜。

去年 3 月的 GTC 2024 上，Nvidia 发布了 Oberon 架构的第一代产品：GB200 NVL72。时间快进一年半，第二代 Oberon——GB300 NVL72——即将进入大批量出货。两代之间的设计与升级变化很少。第三代 Oberon 架构 Vera Rubin（VR）则是 Ian 今日在 AI Infra 峰会演讲的主角。VR 将于 2026 年上市，距 Oberon 机柜级形态首次亮相不到三年，将相较 GB200/GB300 迎来重大的设计变革与升级。

Vera Rubin Oberon 将 Oberon 架构的功率密度推至极限，因而需要大幅升级供电部分的用料，并改进散热方案的设计。采用无线缆（cableless）设计的考量，是为了克服 GB200/GB300 组装中飞线（flyover cable）布线的困难，以及托盘内线缆带来的可靠性挑战。连接 OSFP 笼形插座（cage）与 ConnectX NIC 的线缆已被移除。从 PCIe 连到前端 BlueField DPU 以及本地 NVMe 存储的线缆，连同其他边带线缆也一并移除。

Vera Rubin 的关键变化与升级集中于以下三种 Vera Rubin（VR）计算托盘 SKU 的全面翻新：

- VR NVL144（仅 Rubin）
- VR CPX（仅 Rubin CPX）
- VR NVL144 CPX（Rubin 与 Rubin CPX 同托盘）

这三种计算托盘形态是下文讨论的三种机柜解决方案的基本构件：

- VR NVL144
- VR NVL144 CPX
- VR NVL144 + VR CPX（双机柜）

![](https://substack-post-media.s3.amazonaws.com/public/images/6bcb4d23-fcb2-4487-a220-a328bbbdb351_1489x1091.png)
*来源：SemiAnalysis*

首先发布的是 VR NVL144 CPX 机柜。它与 VR NVL144 类似，区别在于 VR NVL144 CPX 的 18 个计算托盘中，除 4 颗 R200 GPU 和 2 颗 Vera CPU 外，每个计算托盘还增加了 8 颗 Rubin CPX GPU。

VR NVL144 CPX 机柜同样采用液冷——但其功耗预算高得多，约为 370kW，而 VR NVL144 约为 190kW。

另一种部署选项是 Vera Rubin CPX 双机柜。顾名思义，该方案允许已部署（或将部署）VR NVL144 机柜的客户，随后在其数据中心加配 VR CPX 机柜，为实现预填充/解码分离（PD 分离）推理提供专用硬件。VR CPX 不通过 NVLink 互连，因此 VR CPX 机柜不含 NVSwitch 托盘。VR CPX 机柜通过横向扩展的 InfiniBand 或以太网接入集群，可后续部署在方便的物理位置——不必与 VR NVL144 物理相邻。

与 VR NVL144 CPX 相比，双机柜方案的灵活性高得多，客户可以按自身需要设计预填充与解码的比例。此外，并非每家客户的数据中心基础设施都准备好迎接约 370kW 的 VR NVL144 CPX。同时，与单机柜方案相比，双机柜的故障影响范围（blast radius）也更小。

![](https://substack-post-media.s3.amazonaws.com/public/images/45ee596a-facd-437e-8a50-27f44e99ee7d_1526x1377.png)
*来源：SemiAnalysis、Nvidia*

从下表可以看到单个计算托盘里塞进了多少计算与网络器件——每个计算托盘共 22 颗 Nvidia 芯片（其中 14 颗为 XPU），即每个 VR NVL144 CPX 机柜 396 颗。为了把上述所有器件装进单个计算托盘，Nvidia 转向了无线缆的模块化设计，并重新设计了计算托盘内部的散热回路。

![](https://substack-post-media.s3.amazonaws.com/public/images/d4fb83ad-a41c-4974-b57f-5ed62e313dfd_1068x636.png)
*来源：Nvidia、SemiAnalysis 估算*

在计算托盘机箱后半部，NVL144 CPX 将沿用与 GB200/GB300 类似的计算板设计。显著区别是 CPU 侧内存改用可插拔（socketable）的 SOCAMM DRAM 模组，而非焊接的 LPDDR5X。VR NVL144 CPX 与 GB200/GB300 的大部分差异位于机箱前半部、主机处理器主板（Host Processor Motherboard，HPM）计算板的下方——这块板在 Blackwell 世代也被称为 Bianca 板。

在前部，VR NVL144 CPX 采用模块化设计，由 7 块子卡（daughter card）模组构成。

- 四块子卡模组位于机箱两侧，每侧两块上下堆叠。这四块子卡各含两颗 800G CX-9 NIC、一个 1.6T OSFP 笼形插座、一个 E1.S SSD NVMe 模组和两颗 Rubin CPX。
- 机箱中部一块子卡（下图中下方居中位置）承载 BlueField-4 模组，其中包含一颗 Grace CPU 和一颗 CX-9 NIC。
- 叠放在该 BlueField-4 模组上方的一块子卡承载供电板（PDB）。电力从机箱后部的母排连接器进入机箱时，PDB 负责将 48-54V 降压至 12-13.5V。
- 最后一块子卡小得多，位于 BlueField-4 模组右侧，非常纤薄，承载实用管理模组，内含 BMC、HMC、DC-SCM 及管理 I/O 等器件。

我们估计 Rubin CPX 芯片的 TDP 约为 800W，若计入含 GDDR7 内存在内的整个模组，则总计升至 880W。为了给计算托盘前部总计 7,040W 的 Rubin CPX 模组散热，机箱前部散热必须从风冷升级为液冷。

为此，NVIDIA 重拾了 2009 年 GTX 295 上的设计。Rubin CPX 与 CX9 子卡以“三明治”方式排布，中间夹着一块共享的液冷冷板。

在 PCB 外侧，热管与均热片将每个蚌壳式（clamshell）GDDR7 内存模组背面的热量传导至主冷板。通过充分利用 1U 托盘高度并使用冷板两侧，容纳这些 GPU 所需的计算托盘面积减半，实现最大密度。

![](https://substack-post-media.s3.amazonaws.com/public/images/58c43f61-e8e3-4003-a229-514015ed8787_675x396.png)
*来源：SemiAnalysis 估算、Nvidia*

VR NVL144 CPX 的另一项关键设计变化是采用无线缆设计。正如我们在 [PCB 超级周期核心研究报告](https://semianalysis.com/core-research/ai-server-pcb-super-cycle-copper-foil-content-upgrade/)以及近期关于[安费诺（Amphenol）AI 用量](https://semianalysis.com/core-research/amphenol-content-growth-vr-nvl144-backplane-board-to-board-connectors-dac-acc-aec-tam-kyber-midplane-backplane/)的核心研究报告中讨论的，这一设计有两方面原因。其一，飞线存在多个不同的故障点，在组装过程中极易受损。其二，VR NVL144 CPX 的高密度设计没有给线缆布线留出任何空间。

那么没有线缆，信号如何走线？答案很简单：来自 HPM（Bianca）板的信号经由安费诺的 Paladin 板对板连接器离开该板。这一点在我们[近期关于安费诺 AI 用量的文章](https://semianalysis.com/core-research/amphenol-content-growth-vr-nvl144-backplane-board-to-board-connectors-dac-acc-aec-tam-kyber-midplane-backplane/)中有更详细的讨论。随后信号穿过位于机箱中部的 PCB 中板（midplane）走线。在 PCB 中板的另一侧，各子卡通过另一组 Paladin 板对板连接器与中板相连。

为配合这一无线缆设计，HPM（Bianca）板上部的 CX-9 NIC 从机箱后半部移到了前半部，如下图所示。在 GB200/GB300 上，GPU/CPU 与 CX-7/8 之间的 PCIe 信号传输距离，短于 CX-7/8 与 OSFP 笼形插座之间的以太网/InfiniBand 信号传输距离。

过去——必须把 200G 以太网/InfiniBand 信号从计算托盘后半部的 NIC 传到计算托盘前部的 OSFP 笼形插座，这迫使设计者使用飞线，因为每通道 200Gbit/s（单向）速率下信号在 PCB 上的损耗过高。

而现在 NIC 离 OSFP 笼形插座更近，改为每通道速率更低的 PCIe Gen6 信号（单向 64Gbit/s/通道）走更长的距离，这部分连接便可改由 PCB 走线。尽管在 PCB 上驱动 PCIe Gen6 信号仍具挑战性，但通过升级 PCB 材料，仍可实现良好的信号完整性。

为了便于维护，子卡也设计成模组形式。每个子卡模组可在子卡模组舱中滑入滑出。计算托盘内设有专为此设计的内部导轨套件。

下面我们展示各款 Vera Rubin 计算托盘 SKU 内部的信号走线方式，以及 VR Rubin 各 SKU 的计算托盘拓扑。这些图中的一大亮点是：CX-9 在实现 Rubin CPX 与横向扩展连接方面扮演关键角色，因为它同时是一颗集成 PCIe 交换芯片。

## 巨大飞跃：分离式服务

今日发布的 Rubin CPX 对推理而言是改变游戏规则的产品，其意义仅次于 GB200 NVL72 Oberon 机柜级形态的首次发布。只有为推理中截然不同的预填充与解码两个阶段配备专用硬件，分离式服务才能真正实现。

在本节中，我们将讲解从传统服务到使用同质硬件的分离式服务的演进，最后以使用专用硬件的分离式服务作结进行分析。我们将展示使用同质硬件的分离式服务会造成多大的浪费。一旦专用推理硬件普及，继续使用同质硬件给人的感觉就像是买一把电锤来拍虫子。

正如本文前文所述，Rubin CPX 的发布将把 Nvidia 的竞争对手推回绘图板前重塑路线图。不推出自家预填充专用芯片，就意味着让自家客户背上低效系统，注定让这些客户在 token 经济（tokenomics）市场的竞争中落败。

服务一个 LLM 请求包含两个阶段：预填充阶段和解码阶段。预填充阶段中，LLM 根据用户提示词（prompt）生成第一个 token。该阶段决定首 token 延迟（TTFT），通常受计算瓶颈约束，内存带宽利用不足。另一方面，解码阶段在从 KV 缓存加载已有 token 的同时生成新 token。该阶段决定每输出 token 耗时（TPOT），始终受内存带宽约束，算力利用不足。

![](https://substack-post-media.s3.amazonaws.com/public/images/8222e4fe-0aba-4372-a31e-ae98ee65100d_1430x688.png)
*来源：NVIDIA*
![](https://substack-post-media.s3.amazonaws.com/public/images/94f8c60b-9302-487a-9ca5-8b6a57a96b50_2170x399.png)
*来源：SemiAnalysis 估算*

在下图中，我们看到一个示例，突出展示了在同一系统上同时进行预填充和解码时，内存带宽与 FLOPS 利用率之间的取舍。预填充单个 token 所需的 FLOPS 随输入序列长度线性增长。解码的 FLOPS 需求也随系统上的用户数（即批大小）和序列长度而增加。

较短的输入序列长度可能无法吃满推理系统的可用 FLOPS，此时系统的产出将受限于参数装载进芯片内存的速度——这是内存带宽的函数。而随着输入序列长度增加，工作负载最终会增长到用满推理系统的全部可用 FLOPS，转而受系统总 FLOPS 约束。在下图右半部分，我们展示了当序列长度超过 32k 时，FLOPS 利用率达到 100%，而内存带宽利用率下降。

![](https://substack-post-media.s3.amazonaws.com/public/images/bb6c7373-051d-4dc0-993e-b10d032eccdd_2462x1504.png)
*来源：SemiAnalysis*

由此可以看出，当一个节点执行非常重的预填充负载——序列长度很长或批大小很大时，内存带宽处于闲置状态。如前一节所述，随着芯片 BOM 中内存占比在过去几年持续上升，这最终成为一种代价高昂的资源闲置！

低效还源于另一个事实：预填充与解码阶段的工作负载特性差异极大，当二者并发处理时，预填充请求与解码请求总会相互干扰对方的性能。业界有许多试图平衡两者的优化手段——例如加入预填充计算来决策，以保证请求长度大致均匀从而提升利用率——但它们总是伴随取舍。另一种做法是将预填充与解码阶段完全分离，但若优先解码阶段，预填充就得等待——导致首 token 延迟很长。反过来，若优先预填充，解码阶段将被迫等待，且由于内存带宽利用不足，token 间延迟会很慢。

### **第一步：以相同硬件分离预填充与解码**

优先的解决方案是实现分离式服务，首先通过把预填充与解码请求路由到不同的计算单元来解决相互干扰问题，让性能分析变得更简单。其好处是能够更好地管理服务水平协议（SLA）——SLA 通常聚焦于一定的每用户 token/s 水平。但有几个问题。这种完全分离似乎只在特定的输入/输出序列长度比以及长解码长度下才有出色效果，其他场景收益平平。此外，这种分离仍遗留“配置失当”的问题：纯预填充操作几乎总是会严重低度利用内存带宽。

在下面的示例中，我们展示了 R200 仅用于预填充时几乎用不了多少内存带宽。随着序列长度增加、可用 FLOPS 的利用更充分，内存带宽利用率反而愈发微不足道——实际上就是在浪费极其昂贵的 HBM 内存。

![](https://substack-post-media.s3.amazonaws.com/public/images/ef4cd052-987d-4c3e-9c19-9cdeb76bde0f_1024x621.png)
*来源：SemiAnalysis*

### **下一步：在专用硬件上分离预填充与解码——Rubin CPX 登场**

既然预填充天生就难以充分利用内存带宽资源，减少浪费的一种办法就是降低内存的数量与成本。这正是 Rubin CPX 的做法：采用容量更低、价格更便宜的 GDDR7 内存。

在下面的示例中，我们展示了 R200 仅用于预填充时几乎用不了多少内存带宽。相比之下，Rubin CPX 在相当短的输入长度下反而能利用更高比例的内存带宽，随后在我们认为典型的输入长度下跌得更低。

![](https://substack-post-media.s3.amazonaws.com/public/images/0a53c441-5721-4e00-95af-6e0ff7f34107_2482x1526.png)
*来源：SemiAnalysis*

确实，我们要强调这并非为效率而效率——它对最终利润有巨大影响！在下表中，我们给出一个例子，比较 R200 GPU 与 Rubin CPX GPU 的内存带宽利用率。在该场景下，两者的内存带宽利用率都极低，但区别在于 Rubin CPX GPU 至少闲置的是容量更低、便宜得多的内存。而 R200——运行与 CPX 完全相同的预填充负载，会带来 $0.90/hr 的总拥有成本浪费！

![](https://substack-post-media.s3.amazonaws.com/public/images/efe2cede-c842-4260-a1c3-17cbdb3bf93c_2560x897.png)
*来源：SemiAnalysis*

Rubin CPX 带来了更大的内存容量，但这些比特位是“较低质量”的 GDDR7，按每 GB 计其成本不到 HBM 的一半。从内存厂商视角看，GDDR7 的利润率更低，因为它是技术门槛更低、竞争更激烈的产品（即三星（Samsung）也能供货）。

这意味着使用 CPX 系统会降低 HBM 在系统总器件价值中的占比。花在 VR200 NVL144 CPX 或 VR CPX 机柜上的每一美元，其中用于 HBM 的份额都低于把同一美元花在单独的 VR200 NVL144 机柜上的情况。在其他条件不变的前提下，假设 AI 系统支出总额固定，单位支出的 HBM 需求将下降。

### **为什么不进一步削减内存？**

毫无疑问，许多读者一想到能少花钱买 HBM 就垂涎欲滴，心里盘算着：为什么不把系统内存进一步削减？如果典型预填充序列长度对应的内存利用率只有百分之十几甚至个位数——为什么不把内存容量缩减到 1/10？这是否意味着 HBM 需求乃至内存整体需求的末日？

![](https://substack-post-media.s3.amazonaws.com/public/images/76ba89fb-500a-4ff3-96a4-8a7f4d8ad528_468x263.jpeg)
*来源：SoftRAM*

然而，技术领域的事情没这么简单。Rubin CPX 做的是降低预填充和 token 的成本。token 成本降低会刺激需求，意味着对解码的需求也随之增长。与许多其他压低成本的技术创新一样，需求的增长通常足以超过成本的下降，最终算下来按金额计的总市场规模反而更高。

这一 GDDR7 需求还有更多供应链层面的影响。RTX Pro 6000 同样使用 GDDR7，但速率较低，为 28Gbps。Nvidia 已为 RTX Pro SKU 下达巨额供应链订单，最初的计划是在 H20 出口许可恢复之前，将这些芯片作为 H20 的替代品卖给中国。这些订单主要下给三星，后者有产能满足这些突增的紧急订单。SK 海力士和美光（Micron）无法满足这一需求，因为它们的晶圆产能已被 HBM 订单等占用。既然三星能交付有竞争力的 GDDR7，三星同样可能从 Rubin CPX 中受益。

### **再谈预填充流水线并行：Rubin CPX 分离式预填充的一个有趣利好**

上一节我们概述了 Rubin CPX 如何减少内存浪费，而 Rubin CPX 放弃 NVLink 这类超高速纵向扩展网络能力方案，是另一项关键节省。Rubin CPX 的片外 I/O 仅有 16 条 PCIe Gen6 通道，单向带宽约 1Tbit/s，而 R200 的 NVLink 为 14.4Tbit/s。即便面对现代 MoE 前沿大模型，这点 I/O 也足以执行预填充。

例如，DeepSeek V3 以 NVFP4 数值格式运行时，需要 335GB 内存容量来装载全部模型权重——这超过了单颗 CPX 芯片 128GB 的内存容量。这一问题可以用流水线并行（pipeline parallelism，PP）解决，即把模型的多层拆分到不同 GPU 上。在 PP 中，每颗 GPU 顺序处理 token，并将激活值沿流水线向下传递。

PP 的缺点在于 token 需要在多颗 GPU 之间顺序传递，级间通信会带来延迟。重要的推论是：PP 的单 GPU token 吞吐往往高于专家并行（Expert Parallelism，EP），但代价是 PP 的首 token 延迟（TTFT）高于 EP。PP 的 tok/s/GPU 吞吐更高，因为 EP 涉及 all-to-all 集合通信，开销很大，而 PP 只需简单的发送与接收操作。

因此，对于流水线并行推理，更简单的通信需求意味着预填充几乎永远不会打满通信链路——也就是说，没有必要配置昂贵的高速纵向扩展网络。与 HBM 一样，这是又一个可以省钱的环节：把在纯预填充运行中闲置的另一层设备剥离出去——替系统所有者省下浪费掉的 TCO 开支。

在下表中，我们展示了 DeepSeek 采用 PP8 或 PP4 并行方案的预填充中，每 token 的消息大小为 7kB。如果用消息完全打满 PCIe Gen6 x16 的 I/O 通道，意味着我们最多可以每秒传输（因而也就是处理）18.3M 个 token。这就是通信约束界限。

再看计算约束情形：每 token 的预填充计算量为 0.074 TFLOP。因此，如果把 Rubin CPX 19,800 PFLOPS 的密集 FP4 吞吐除以 0.074 TFLOP，可得最大 token 吞吐为每秒 267.6k 个 token。

这远低于通信约束界限，甚至连相当普通的 PCIe Gen6 I/O 都远远用不满，更不用说带宽是 16 通道 PCIe Gen6 之 14 倍以上的 NVLink 了。

我们估计，对终端系统所有者而言，NVLink 纵向扩展的总成本（含 NVSwitch 与背板）约为每 GPU ~$8k——略高于每 GPU 全包集群成本的 10%。这是 Rubin CPX 为终端用户带来可观节省的另一个维度。

![](https://substack-post-media.s3.amazonaws.com/public/images/43b4f403-8fc3-446f-b4a6-c3b37a186c83_1786x1458.png)
*来源：SemiAnalysis*

然而，若试图在速率较低的网络连接上使用专家并行，将引发延迟问题与瓶颈。通信需求随 top_k 与层数的乘积而增长。DeepSeek V3 的 top_k 为 8、有 61 层，粗略估算即可看出，用 EP 取代 PP 会使通信需求增加约 488 倍。

### **关于扩展与黄氏定律的一点补充**

今日讨论的焦点是以 NVFP4 数值格式进行推理的各项指标。的确，推理服务商一直在通过采用越来越低精度的数值格式不断解锁更高吞吐。然而——一旦到了 FP4——能榨的油水就开始枯竭了。

稀疏性（sparsity）被宣传为可继续解锁更高吞吐的另一根杠杆，这也是多数营销规格和宣讲材料以稀疏 TFLOPS 口径表述的关键原因。然而稀疏性至今未能兑现其承诺的收益——远未达到其宣称的 2 倍提升。

今日发布还揭晓了 Rubin 的稀疏性方案。该方案不同于 Hopper 和 Ampere 采用的 2:4 结构化稀疏，也不像 Blackwell 的 4:8 成对结构化稀疏。我们希望 Rubin 稀疏能够带来实质性的吞吐收益，让黄氏定律（Huang's Law）继续稳步向前！

## 硬件专用化分离式服务的缺点

预填充专用芯片的到来固然令人兴奋，但我们尚未抵达极乐之境，硬件专用化的分离式服务也有其缺点。随着服务商的工作负载与模型发生变化，能否调整预填充与解码实例的比例（PD 比例）至关重要。

## 定制芯片接下来怎么办？

最优 PD 比例对诸多因素敏感，包括模型架构、SLA、网络带宽等。而 Vera Rubin NVL144 CPX 的一个关键劣势在于其 Rubin 与 Rubin CPX 芯片的数量和比例是固定的，若想改变 PD 比例，灵活性就打了折扣。

Nvidia 在芯片演进上的敏捷性，正在使其竞争对手所处的地形快速变动。每当竞争对手在性能或架构上接近追平，Nvidia 就会沿另一个维度再度进化其产品。下面来讨论 Rubin CPX GPU 的广泛采用可能如何冲击各竞争方案。

### Google TPU

TPU 的 3D Torus 纵向扩展网络提供了独特优势：最大 pod 规模可达 9,216 颗 TPU。这是业内最大的 world size，却提供了业界最低档的每加速器纵向扩展网络成本之一。这使其能够支持非常宽泛的并行方案组合，而其他较小的 world size 可能无法支持。

话虽如此，对 Google 而言，理想的做法仍是开发一款纯预填充芯片，以便在内部工作负载上持续保持其每美元性能优势。他们拥有内部工作负载，可以产生锚定需求，为纯预填充芯片的研发提供启动支撑与资金，该芯片日后还可面向外部市场销售。

Google 的独特拓扑意味着，在某些推理系统配置与模型上，其性能甚至可能超过某些 Nvidia 系统。

## AWS Trainium3 Max NVL72、AWS EFA NIC 与 Meta MTIAv4 SUE72

另一类厂商拥有内部工作负载，但采用的是模仿 NVL72 机柜形态的设计。这些供应商同样拥有可支撑纯预填充芯片研发启动的内部工作负载，而且它们理应这么做，以便与 Nvidia 的 VR200 NVL144 CPX 保持同等水准。

例如，一款与 Trainium3 Teton-3 Max NL72（具备与 VR200 NVL144 相同的 72 逻辑 GPU、全交换的纵向扩展规模）配套使用的纯预填充芯片，可以依托 Anthropic 的需求进行协同设计，并在其推理工作负载中获得采用。

AWS 的 VR 144 CPX 将面临重大的上市时间挑战，因为其 1U 计算托盘已经高度集成，塞满了 4 个大型 Rubin GPU 封装和 8 个 CPX GPU 封装，没有空间再把 AWS 自研的 EFA NIC 塞进计算托盘。亚马逊不想用 ConnectX-9。AWS 对 EFA 情有独钟！

我们相信他们会继续使用 EFA，并通过把 EFA NIC 分离到专用的 EFA NIC 边车（sidecar）机柜来克服这一挑战，再用外部 PCIe AEC 线缆连接 VR 144 CPX 机柜与 EFA NIC 边车机柜。此外，由于他们不会使用内置 PCIe 交换功能的 ConnectX-9 NIC，他们还需要使用 Astera Labs 的专用 PCIe 交换芯片，来连接 Vera CPU、本地 NVMe、Rubin CPX GPU，以及通往边车机柜内 EFA NIC 的外部 PCIe AEC 线缆。

MTIAv4 的 SUE72（同样具备与 VR200 NVL144 相同的 72 逻辑 GPU、全交换的纵向扩展规模）设计也可以依托 Meta 的内部推理工作负载。即便是 OpenAI 与 Broadcom 合作的新兴芯片设计也有竞争力，因为它们将以前沿模型（Frontier Models）为出发点进行协同设计，并有内部工作负载兜底。

尽管 MTIAv3 享有内部需求的好处，但由于其 16 GPU 的小 world size，它不属于这一类。如今它实际上也需要开发纯预填充芯片，才有一丝追平 Nvidia 即将推出的系统的机会。

### AMD MI400 系列 UALoE72 与 MI500 UAL256

然而，随着 Rubin CPX GPU 的发布，AMD 的翻盘策略如今看来既不够快也不够激进，AMD 将发现自己又要再度追赶 Nvidia。AMD 本已凭借机柜级的 MI400 逼近追平，但 Nvidia 又抬高了门槛。

AMD 与上述厂商的关键区别在于：AMD 缺乏足够的内部工作负载，无法为又一个仅为跟上节奏而立项的芯片研发项目提供营收与需求兜底。

今年早些时候，AMD 在其 Advancing AI 活动上掀起波澜，发布了 MI400 72 GPU 机柜级系统。[我们当时的分析](https://semianalysis.com/2025/06/13/amd-advancing-ai-mi350x-and-mi400-ualoe72-mi500-ual256/)指出，按单位 FP4 FLOPS 的总拥有成本计算，MI400 可以低于 VR200 NVL144 系统——同时提供 19.8TB/s 的内存带宽，而 VR200 NVL144 最初宣传的内存带宽为 13.0 TB/s。

通过向供应商要求快得多的速率档，Nvidia 的 VR200 NVL144 如今宣传的每逻辑 GPU 内存带宽达到约 20.5TB/s。VR200 的内存带宽现已追平 AMD MI400，且使用的 HBM 位点更少。

![](https://substack-post-media.s3.amazonaws.com/public/images/c123aa60-8277-467e-b1f0-52b869b2cd18_2442x1460.png)
*来源：SemiAnalysis AI TCO 模型*

如果 MI400 的 FP4 有效密集 FLOPS（即微基准测试实际能跑出的性能，而非营销口径的吞吐）与 VR200 NVL144 持平甚至更低，那么 AMD 实际上就是拿着一款 VR200 NVL144 的复制品、比 Nvidia 更晚上市。与此同时，Nvidia 将再度拉开身位，因为 VR200 CPX NVL144 在长上下文长度下能提供更优的单位 TCO 性能。届时 AMD 又得等到 2027 年才有机会追上。

不过，我们认为 AMD 仍处于战争状态，如今在开发机柜级系统和改进软件之外，还需要开辟另一条战线——纯预填充芯片之战——才有希望在 2027 年前追上 Nvidia。

## Nvidia

最后——Nvidia 为什么要止步于只有预填充专用芯片——为什么不也做一款解码专用芯片？迄今为止 Nvidia 只发布了预填充专用芯片，解码步骤仍由现有 R200 芯片承担，而非推出解码专用 SKU。

解码专用芯片将恰好是预填充芯片的反面：计算精简、内存带宽富余。这款芯片形似 R200，但不需要那么多算力。理想情况下，通过保留 I/O 小芯片的尺寸，内存与封装外 I/O 的能力都得以保全，但主计算裸片朝向 I/O 裸片的边缘可以收窄，同时保持相同的边长，以容纳每边 2 个 HBM 位点。其结果是一颗面积小得多的计算裸片。

通过大量屏蔽缺陷 SM（defeatured SM）带来的参数良率显著提升，以及大幅降低的 TDP 所带来的供电与散热管理成本下降，还可以实现额外节省。这与预填充芯片的情形恰好相反：在解码芯片上，HBM 数量得以保留，而系统的其他部分被削减，从而使 HBM 的 BOM 占比回升。
