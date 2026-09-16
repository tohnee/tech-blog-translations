---
title: "Vera Rubin——极致协同设计：从 Grace Blackwell Oberon 的演进"
title_en: "Vera Rubin – Extreme Co-Design: An Evolution from Grace Blackwell Oberon"
subtitle: "Vera、Rubin、NVLink 6 Switch、ConnectX-9、BlueField-4、Spectrum-6、无缝无缆计算托盘设计、电源机柜、VR NVL72 TCO 与 BoM"
date: 2026-02-25
source: https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution
crawled: 2026-09-15
authors: ["Wega Chu", "Dylan Patel", "Daniel Nishball", "Clara Ee", "Gerald Wong", "Myron Xie", "Cheang Kang Wen", "Ray Wang", "Nicolas Bontigui", "Ivan Chiam", "Michael Chen"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Vera Rubin——极致协同设计：从 Grace Blackwell Oberon 的演进

> 原文：[Vera Rubin – Extreme Co-Design: An Evolution from Grace Blackwell Oberon](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Vera、Rubin、NVLink 6 Switch、ConnectX-9、BlueField-4、Spectrum-6、无缝无缆计算托盘设计、电源机柜、VR NVL72 TCO 与 BoM**

![](https://substack-post-media.s3.amazonaws.com/public/images/7257cc0c-a57b-4aa2-b03b-1ead3d930e8c_4800x2700.png)

在 CES 2026 上，Nvidia 正式详细发布了 Rubin 平台的全部 6 款产品：Rubin GPU、Vera CPU、NVLink 6 Switch、ConnectX-9、BlueField-4 和 Spectrum-6。VR NVL72 是登台的 Nvidia 机柜级 Oberon 架构第二代。面对竞争对手在机柜级竞赛中的追赶——Gen2 UltraServer 中的 Trainium 3、AMD MI450X Helios 机柜，以及[早在 GB200 之前就已实现机柜级形态的 Google TPU](https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the)——Nvidia 以「极致协同设计」（extreme co-design）的霸权作出回应。凭借极致协同设计，Nvidia 将机柜级集成推向新高度：机柜系统成为一个计算单元、一个单一的分布式加速器，而整个系统由 Nvidia 设计。

![](https://substack-post-media.s3.amazonaws.com/public/images/4d3419ee-609e-490d-999f-2454ec532c80_2683x1577.png)
*来源：Nvidia*

对于 Vera Rubin 平台，Nvidia 正在进一步收紧对系统级与机柜级设计的控制。机柜级集成与组装正变得更具挑战，因为每个组件都被推向极限，同时还要兼顾成本效率。与 Grace Blackwell 相比，VR NVL72 采用了更具整体性的模块化设计，目的在于提升集成效率与吞吐量。

凭借极致协同设计的霸权，Nvidia 的竞争力进一步增强。在 Nvidia 自己开创的 AI 服务器系统设计中，它是唯一一家在所有主要硅内容上都能提供一流或接近一流硅产品的玩家。Nvidia 拥有最强的加速器、SOTA 的纵向扩展交换机、最好的 NIC、最好的以太网交换机之一，以及[一款大幅改进的专用 CPU](https://newsletter.semianalysis.com/i/187132686/nvidia-vera)。没有其他竞争者拥有如此完整的集成化硅产品组合。

在下文各节中，我们将从芯片层面讨论 Vera Rubin 平台的 6 款硅产品。随后，我们将从设计角度讨论从 Grace Blackwell 到 Vera Rubin 的机柜与计算托盘演进，及其对各类组件的影响：线缆、连接器、PCB、散热、机械结构与电源。

接下来，我们将讨论 VR NVL72 系统的主要网络，即纵向扩展的 NVLink 6 网络与后端横向扩展网络。我们还将讨论超大规模云厂商定制空间大幅受限所带来的物流影响，以及组装供应商格局。

最后，本报告以 VR NVL72 系统的 TCO 讨论收尾，并给出支撑 TCO 分析的 BoM 与功率预算估算。在付费墙之后，我们还为读者提供 Nvidia 对其 Groq IP 规划的洞察，同时会涉及美光（Micron）、SK Hynix 与三星（Samsung）在 HBM 爬坡方面的一些挑战。

今天我们还同步发布 [VR NVL72 组件 BoM 与功率预算模型](https://semianalysis.com/vr-nvl72-model/)。该模型对本文涵盖的 VR NVL72 系统提供系统级物料清单与功率预算分析。这一点很重要，因为在 $500B 的 Rubin 建设周期中，各家供应商及其在子组件中的份额将决定它们是赢家还是输家。对市场的下游冲击与错配是巨大的。模型覆盖：

- **Nvidia 计算托盘内容：** 含 Rubin GPU、Vera CPU、SOCAMM 内存的 Strata 模块；BlueField-4；ConnectX-9
- **NVLink 系统：** NVSwitch、NVLink 背板与线缆、相关连接器、主机 CPU 管理模块
- **液冷内容：冷板、QD 快速接头、分液器**
- **PCB、载板与材料内容：** 关键系统板、ABF 载板、CCL 内容
- **连接器**：Paladin HD2 板对板连接器、Paladin HD2 NVLink 6.0 连接器
- **供电内容**：电源架、汇流排、VRM、供电模块
- **机械结构**：机箱、加载机构、导轨套件、机柜机箱
- **管理模块**：BMC
- **网络**：收发器、CX-9

![](https://substack-post-media.s3.amazonaws.com/public/images/7563ee69-3f02-47f8-944f-a7ac5b62cf0a_3362x844.png)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

请访问这个[自助服务门户](https://semianalysis.com/vr-nvl72-model/)购买模型。如有任何产品相关问题，请联系 sales@semianalysis.com。

# 极致协同设计：Rubin 平台下的 6 款硅产品——芯片平面布局与规格

![](https://substack-post-media.s3.amazonaws.com/public/images/7cdeb372-67f9-4140-889e-2f8f493cda0a_1984x1141.png)
*来源：SemiAnalysis、Nvidia*

Rubin 的密集（dense）FP4 与 FP8 FLOPS 相比 GB200 提升约 3.5 倍，而 FP16 FLOPS 增幅相对温和，约为 1.6 倍，凸显 NVIDIA 持续以 FP4/FP8 作为主要的扩展方向。内存方面，HBM 容量与 GB300 持平，而 HBM 带宽扩展更为激进，约 2.8 倍。总体而言，该架构将带宽与低精度计算置于优先地位。

![](https://substack-post-media.s3.amazonaws.com/public/images/6e9330b4-7407-4dcb-8a2b-fb323371ffba_2218x1210.png)
*来源：SemiAnalysis、Nvidia*

### Rubin

![](https://substack-post-media.s3.amazonaws.com/public/images/be50555c-6427-42ca-b58e-97716f2558c9_4800x2700.png)
*来源：Nvidia*

Rubin 的设计是 Blackwell 的合理演进：转向 3nm 制程，并将 I/O 拆分为小芯片（chiplet），同时保持 2 颗光罩极限大小裸片加 8 组 HBM 堆叠的基本结构。35 PFLOPS 密集 FP4 相比 Blackwell GB200 提升 3.5 倍，通过以下途径实现：

- SM 数量从 160 增加到 224
- SM 内张量核心位宽翻倍，达到每时钟 32768 次 FP4 MAC
- 时钟频率从 1.90GHz 提升 25% 至 2.38GHz

此外，Nvidia 声称借助升级后的第三代 Transformer Engine——它取代了前几代的 2:4 结构化稀疏——最高可实现等效 50 PFLOPS 的 FP4 性能。我们将在下文详述 Rubin 的这一架构特性。

值得注意的是，张量核心位宽翻倍仅适用于 FP4 和 FP8，BF16 与 TF32 与 Blackwell 持平，因此性能仅为 Blackwell 的 1.6 倍。这一架构决策反映出 NVIDIA 的判断：大多数训练与推理负载将告别 TF32 和 BF16，转向 FP8 和 FP4。

在内存方面，转向 HBM4 意味着每堆栈（stack）总线位宽翻倍，运行于 10.8 GT/s，总带宽 22TB/s，即在 288GB 容量与 GB300 相同的情况下为 Blackwell 的 2.75 倍。内存带宽相比 GTC 2025 最初公布的 13TB/s 大幅上调。为了追上 AMD MI450 的内存带宽，Nvidia 向 DRAM 供应商要求了高得多的 HBM4 引脚速率——远高于 JEDEC HBM4 规范中的速率。

虽然 Nvidia 的目标是 22TB/s，但我们了解到内存供应商在满足 Nvidia 的要求上遇到困难，我们认为首批出货很可能略低于此、更接近 20TB/s。[我们已面向加速器与 HBM 模型订阅者深入讨论了对 SK Hynix、三星和美光的影响。](https://semianalysis.com/accelerator-hbm-model/)美光大幅落后于三星和 Hynix，我们认为[其已实质上无缘 Rubin HBM4。](https://semianalysis.com/institutional/semianalysis-accelerator-model-micron-zero-hbm4-share-in-rubin/)有关认证与引脚速率的更多细节见[加速器与 HBM 模型](https://semianalysis.com/accelerator-hbm-model/)。

NVLink-C2C 小芯片承载连接 Vera CPU 的 SerDes，带宽翻倍至 1.8TB/s；芯片另一端更大的 NVLink 6 小芯片配备 36 条定制「400G」SerDes 链路，向全部 72 颗 Rubin GPU 提供 2 倍 NVLink 带宽。

晶体管数量增长 60%，达到 3360 亿。

Rubin 一处值得注意的缺失是对稀疏 FLOPs 的提及。在前几代中，2:4 结构化稀疏曾被用来把营销 FLOPs 数字翻倍。但由于刚性的稀疏结构强制一半数值为零而带来精度损失，实际采用极少，尤其在低精度下。程序员基本忽略了结构化稀疏，因为它并不实用，这也促使硬件设计随之改变：Blackwell Ultra GB300 在保持稀疏 FP4 FLOPs 不变的同时将密集 FP4 提升了 50%，而 AMD 的 MI355X 则不再支持 MXFP8、MXFP6 和 MXFP4 格式的结构化稀疏，以节省裸片面积。

Rubin 改进版 Transformer Engine 中的自适应压缩引擎是一项关键特性，可在运行中动态计算稀疏度、在不把非零值置零的前提下消除数据流中的零值，从而重新提升天然更稀疏的推理性能，在提升性能的同时保持模型精度。这对面向 Blackwell 构建的现有模型自动生效，无需新的编程模型或专门优化。虽然使用训练后量化（Post Training Quantization）或量化感知训练（Quantization Aware Training）的模型会经过调优以最大化自适应压缩加速比，但要利用动态压缩并非严格必需。

这意味着负载越稀疏，性能就越接近营销的 50 PFLOPS 峰值。因此 NVIDIA 把 50 PFLOPS 数字标称为 FP4 推理，而 35 PFLOPS 的 FP4 训练数字对应密集负载。由于精度得以保持，营销团队可以宣称 Rubin 相对 GB200 的 FLOPs 达到 5 倍——拿 50 PFLOPS 动态压缩 FP4 对比 10 PFLOPS 密集 FP4。实际 GEMM 性能能否达到 50 PFLOPS 取决于张量中零值的数量：零值越多，越接近该峰值；张量中零值越少，加速比越低。总体而言，得益于自动实现，我们预计 Rubin 的自适应稀疏压缩相比结构化稀疏将获得大得多的实际采用。

话虽如此，许多 ML 系统工程师仍然怀疑这种新的稀疏形式能否真正奏效，Nvidia 的 50 PFLOPS 很有可能与前几代一样纯属营销。

Rubin 芯片级 TDP 提升至最高 2,300W，而 Blackwell 为 1000-1400W。供应链传言显示存在两个功耗与性能档位不同的「SKU」：2,300W 的 Max-P 版本和 1,800W 的 Max-Q 版本。但它们并非不同的硬件 SKU，而是 Nvidia 根据用户负载需求提供的两种默认功耗档位。Max-Q 是 Nvidia 认为能提供最佳每瓦性能的档位；Max-P 提供最高绝对性能，但伴随能效损失。运行 Max-P 设置会使机柜功耗增加 20%，但性能提升远低于这 20% 的功耗增幅。

这些功耗档位由软件管理。用户也可以自选任何最大功耗（只要不超过每 GPU 2,300W），此前的 GPU 世代也是如此。多家超大规模云厂商与实验室已选择在更低功耗下运行 GPU，以优化每瓦性能，并兼顾电力供应约束。

![](https://substack-post-media.s3.amazonaws.com/public/images/61396626-3359-4a08-8dfa-58f7ed911443_2012x1118.png)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

在 Rubin 封装的机械结构方面也做了升级，新增了升级版均热盖（heat spreader）与加强框（stiffener）。相比之下，Blackwell B200 与 B300 封装只有均热盖。均热盖使热量更均匀地从封装导出，同时也为封装提供机械支撑、防止翘曲。

对 Rubin 而言，均热盖是由两块独立盖板组成的模块。除均热盖外，封装结构中还加入加强框，提供更多机械支撑以避免翘曲。均热盖表面还会有一层电镀金，目的是防止液态金属 TIM2 造成的腐蚀——TIM2 位于均热盖与冷板之间。

### Vera

![](https://substack-post-media.s3.amazonaws.com/public/images/b0795695-2bda-4134-a982-12e59acc76f9_3000x3040.jpeg)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

[NVIDIA 在 CPU 战线上动作激进](https://newsletter.semianalysis.com/i/187132686/nvidia-vera)。Vera 通过转向 3nm 光罩极限大小的计算裸片、并将内存控制器与 I/O 拆分为小芯片，实现相对 Grace 性能翻倍。核心数量从 72 增至 88，裸片上实际印制 91 个核心，以留出冗余改善良率。这些核心标志着 NVIDIA 自研 ARM CPU 设计的回归，「Olympus」核心现支持 SMT 多线程，合计 176 个处理线程。L3 缓存容量也提升 40% 至 162MB。内存总线位宽翻倍至 1024-bit，速率提升至 9600MT/s，带宽为 2.5 倍；借助 8 个 SOCAMM 模组，最大容量增至 3 倍的 1.5TB。通往 Rubin GPU 的 NVLink-C2C 带宽同样翻倍至 1.8TB/s。现在还支持 PCIe6 与 CXL3.1。这一切使晶体管数量增至 2.2 倍，达 2270 亿。

### NVLink 6 Switch

![](https://substack-post-media.s3.amazonaws.com/public/images/722c91c0-0b9e-43c6-9ca6-76714eb7fa70_3000x3048.jpeg)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

虽然机柜级交换带宽翻倍，每机柜 NVLink Switch 芯片数量也翻倍至 36 颗，每个交换托盘现容纳 4 颗 Switch 芯片。这意味着新的 NVLink 6 Switch 芯片与 NVLink5 Switch 一样拥有 28.8T 带宽，端口数减半但速率翻倍，采用「400G」双向 SerDes。这让高带宽交换芯片设计得以保持单颗单片（monolithic）裸片，节省设计复杂度。布局与 NVIDIA 以往交换芯片相同：两侧为 IO，中央为逻辑区块的交叉开关矩阵（crossbar），以及 3.6 TFlop 的 SHARP 网内计算加速。

### ConnectX-9

![](https://substack-post-media.s3.amazonaws.com/public/images/cb34a228-9fff-45eb-8851-68a1d54acf66_1781x1780.jpeg)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

ConnectX-9 相对 ConnectX-8 基本属于迭代升级，网络带宽同为 800G，并具备 48 lane PCIe6 交换能力。不过，CX-9 现在以 4x200G PAM4 SerDes 支持 800G 以太网，而 CX-8 只在 InfiniBand 上支持该速率。对 Rubin 平台，NVIDIA 将每 GPU 的 NIC 数量翻倍，以实现 2 倍横向扩展带宽。

### BlueField-4

![](https://substack-post-media.s3.amazonaws.com/public/images/60828488-61bb-416d-a9c8-df3e8fe3c284_2506x1673.jpeg)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

BlueField-4 的设计与 BlueField-3 大相径庭。NVIDIA 没有做一颗集成计算与网络的定制流片，而是直接复用其大型 Grace CPU 裸片，与 ConnectX-9 裸片协封装，打造出一颗具备强大算力的 800G DPU。128GB LPDDR5 为该 Grace CPU 供数，带宽为常规 Grace 的一半。这是 BlueField-3 内存容量的 4 倍。BlueField-4 还可充当存储控制器，每套上下文内存存储（Context Memory Storage）系统使用 4 颗 BF-4 芯片。

### Spectrum-6

![](https://substack-post-media.s3.amazonaws.com/public/images/2e1932aa-e7cf-438e-bc2a-984a03d9cd25_3000x2983.jpeg)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

虽然不属于 Rubin NVL72 机柜的一部分，Spectrum-6 CPO 凭借翻倍的端口数（radix）支持更大规模的横向扩展集群。设计延续 Spectrum-5 的特性：8 颗 IO 小芯片围绕主交换裸片。512 条 200G SerDes 实现 102.4T 交换带宽。封装上的 32 个 3.2T 光引擎（optical engine）将这些电信号转换为光链路，每个引擎配一个可拆卸光纤连接器。SN6810 采用其中一颗芯片，而 SN6800 容纳四颗，经多路复用组成一台 409.6T 交换机。此外还将有一个采用可插拔 OSFP 笼座的非 CPO 版本 SN6600。在我们看来，非 CPO 版本会更常见。

# Rubin Oberon 机柜：是 NVL72，不是 NVL144 也不是 NVL36

自 Nvidia 在 2024 年 GTC 上发布 GB200 以来，AI 服务器系统的概念已从机箱级转向机柜级系统。我们在 **[GB200 文章](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)** 中讨论了 Nvidia AI 服务器形态从 HGX（每节点 8 GPU）到 Oberon（NVL72 机柜级）的演进。HGX 形态依然存在，但 Nvidia 的大多数 Blackwell GPU 都以 Oberon 形态集成。Rubin 也将同时提供 HGX 与 Oberon 两种系统。

Blackwell 与 Rubin Oberon 架构的关键差异在于向客户提供的 SKU 数量。由于 Blackwell Oberon 是业界首次大规模部署的机柜级方案，且 GB200 NVL72 SKU 的机柜功率密度超过 100KW，许多数据中心当时尚未备好支持每机柜 100kw+ 的基础设施。Nvidia 为 Blackwell Oberon 提供了两款 SKU：GB200 NVL72 与 GB200 NVL36x2。后者是面向基础设施尚未就绪、无法应对单柜高密度散热的客户的低密度 SKU。我们在 **[GB200 文章](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)** 中讨论了两种形态的差异[。](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)

与 Blackwell 不同，Rubin 只提供 VR NVL72 一款 SKU。其配置与 GB200/GB300 NVL72 非常相似。每套 VR NVL72 系统包含：

- 72 个 Rubin GPU 封装
- 36 颗 Vera CPU
- 36 颗 NVLink 6 Switch ASIC

![](https://substack-post-media.s3.amazonaws.com/public/images/42660b70-c898-4e6b-a117-7490baf5ae4c_733x1702.png)
*来源：Nvidia VR NVL72 BoM 与功率预算模型*

顺带一提，VR NVL72 最初被称为 VR NVL144，因为 GTC 2025 的[「黄氏数学」](https://newsletter.semianalysis.com/i/174558496/jensen-math-changes-every-year)把 GPU 数量定义为系统中 GPU 计算裸片的数量（每封装 2 颗计算裸片、每 Oberon 机柜 72 个 Rubin 封装 = 144 颗计算裸片）。12 月下旬命名改回 VR NVL72，以代表系统中 72 个 Rubin GPU 封装。就在 CES 2026 之前，官方正式确认命名为 VR NVL72。

### **CPX 形态**

![](https://substack-post-media.s3.amazonaws.com/public/images/30fd28ad-beb1-46a4-844e-bab6c4d4b216_1507x1697.png)
*来源：Nvidia VR NVL72 BoM 与功率预算模型*

尽管 Nvidia 最初计划将 CPX 加速器集成进 VR NVL72 机柜，但目前的进展表明 CPX 将只以独立机柜形式提供，如我们在介绍 Nvidia [CPX](https://newsletter.semianalysis.com/p/another-giant-leap-the-rubin-cpx-specialized-accelerator-rack) 的[文章](https://newsletter.semianalysis.com/p/another-giant-leap-the-rubin-cpx-specialized-accelerator-rack)中详述的那样。回顾我们此前 CPX 文章对 Rubin 时代系统规划的梳理，Nvidia 最初考虑过三种 VR NVL72 配置：

- **VR NVL72（常规）：** 不含 CPX 的标准 Oberon VR NVL72
- **VR NVL72 CPX（集成式）：** Rubin GPU 与 Rubin CPX 位于同一计算托盘
- **VR NVL72 CPX（双机柜）：** Rubin CPX 部署在 VR NVL72 机柜旁的独立机柜中

独立/专用机柜的方向实质性改变了部署权衡。双机柜方案允许超大规模云厂商独立扩展预填充与解码容量、优化数据中心功耗包络，并相对紧耦合托盘降低系统级故障域。更重要的是，它在架构上正式实现了推理预填充（计算受限）与解码（带宽受限）的解耦。

Rubin CPX 最初被设计为面向预填充优化的 GDDR7 加速器，基于三点关键考量：

- 预填充主要受 FLOPs 限制而非带宽限制，HBM 并非不可或缺。
- HBM 更高的带宽在预填充中利用率结构性偏低。
- GDDR7 的每 GB 成本显著更低，且避免使用 2.5D 封装。

然而，Nvidia 开始为预填充探索搭载 HBM 的变体——要么通过修改 CPX 配置，要么通过以更低内存规格（如使用 HBM3E）、专用于预填充的 Rubin 部署。早在去年 12 月初，我们就在[加速器与 HBM 模型](https://semianalysis.com/accelerator-model/)中[指出](https://semianalysis.com/institutional/rubin-delay-and-gb300-revision-b30a-h200-rubin-cpx-hbm-update-new-specs-sheet/)了这一点（[报告链接](https://semianalysis.com/institutional/rubin-delay-and-gb300-revision-b30a-h200-rubin-cpx-hbm-update-new-specs-sheet/)）。

我们还认为，这一转变很大程度上由内存经济学的演变驱动。**传统 DRAM 价格已大幅上涨：** 随着 DDR 价格上涨，HBM 的相对溢价被压缩，因为其价格更多由长期合约锁定，这缩小了 GDDR 方案 CPX 与低规格 HBM 配置之间的成本差距，从而消除了 GDDR 相对性能而言的许多成本优势。虽然内存带宽对预填充不如对解码那样关键，但仍是必需的。

---

# 计算托盘重新设计

VR NVL72 的一大变化在计算托盘内部。这次计算托盘重设计的核心是简化组装，即从计算托盘中消除线缆——线缆一直是 GB200/300 组装的主要故障点。正如黄仁勋在 CES 2026 上所说，无缆设计将计算托盘组装时间从 2 小时缩短到 5 分钟。为此，VR NVL72 计算托盘采用模块化设计，各模块之间通过板对板连接器互连。

![](https://substack-post-media.s3.amazonaws.com/public/images/ff713757-9939-4bc5-a9b7-b21ea415c5bc_832x1398.png)
*来源：Nvidia VR NVL72 BoM 与功率预算模型*

要理解 VR NVL72 的计算托盘，必须先了解组成它的 6 类模块：

1. Strata 模块 x 2
2. Orchid 模块 x4
3. 计算托盘中板（Midplane）x 1
4. 供电模块 x 1
5. BlueField-4 模块 x 1
6. 系统管理模块 x 1

我们在 [Nvidia VR NVL72 BoM 与功率预算模型](https://semianalysis.com/vr-nvl72-model/)中拆解了这些组件及全部子组件的成本。

### Strata

![](https://substack-post-media.s3.amazonaws.com/public/images/3e60d518-4f27-49ac-b476-45433bca8a0a_911x1066.png)
*Strata 模块。来源：Nvidia VR NVL72 BoM 与功率预算模型*
![](https://substack-post-media.s3.amazonaws.com/public/images/4ccb2f3a-f952-4300-bc34-96c1470be6ba_1032x1080.png)
*Bianca 模块。来源：Nvidia VR NVL72 BoM 与功率预算模型*

位于机箱后部的 Strata 模块相当于 GB200/300 的 Bianca 板，容纳两颗 Rubin GPU 和一颗 Vera CPU。与 Bianca 不同，Vera 的 LPDDR5X 内存以 SOCAMM 模组插槽方式安装，8 个 SOCAMM 插槽分列 Vera 左右两侧。提供两种不同容量的 SOCAMM 模组：192GByte 与 128GByte，每颗 Vera 最大 1,534GByte、最小 1,024GByte。由于 CX-9 移至机箱前部，ConnectX NIC 夹层卡也不再放在 Strata 模块上。在无缆设计下，所有线缆连接器端口都被移除，取而代之的是模块底部的 Paladin HD2 板对板连接器。另一侧则沿用与 GB200、GB300 相同的一组 Paladin HD2 背板连接器，同样位于模块后部，经 NVLink 背板连接到 NVLink 6 Switch。

### Orchid

![](https://substack-post-media.s3.amazonaws.com/public/images/74182e8e-49ce-4a30-b7bd-c2b0a35b6419_584x1115.png)
*来源：Nvidia VR NVL72 BoM 与功率预算模型*

Orchid 模块容纳两块 ConnectX-9 NIC、两个 800G 收发器笼座（cage）和一个 E1.S 模组插槽。四个 Orchid 模块位于机箱前部：每两个 Orchid 模块上下堆叠，分别占据机箱前部左侧与右侧空间。模块末端有一个 Paladin HD2 板对板连接器，与中板上的连接器对接。Orchid 模块细而长，使 PCIe 6 信号得以从中板一直延伸到机箱前部的 CX-9 NIC。

### 中板（Midplane）

![](https://substack-post-media.s3.amazonaws.com/public/images/1b2c77d5-6f60-4022-9753-07ffa81846fe_1089x814.png)
*来源：Nvidia VR NVL72 BoM 与功率预算模型*

中板充当两个 Strata 模块与机箱前部各模块之间 PCIe 信号的桥梁。中板模块垂直横跨机箱中部，模块两侧均带 Paladin HD2 板对板连接器。Strata 模块连接中板一侧，而 Orchid 模块、BlueField-4 模块、PDB 模块与管理模块连接另一侧。

### BlueField-4

![](https://substack-post-media.s3.amazonaws.com/public/images/ea791cfc-972f-4952-b1fd-283e63357743_823x1648.png)
*来源：Nvidia VR NVL72 BoM 与功率预算模型*

BlueField-4 DPU 位于机箱前部中央，处于左侧 Orchid 模块与管理模块之间。如上节所述，BlueField-4 由 Grace CPU 与 CX-9 NIC 组成。该模块还板载 128GByte LPDDR5x、512Gbyte 板载可插拔 SSD，以及一颗来自 Aspeed 的集成 AST2600 BMC。在 VR NVL72 计算托盘的参考设计中，BlueField-4 作为 DPU 提供最高 800Gb/s 的前端网络能力。然而，与 BlueField-3 一样，BlueField-4 只会被少数客户采用，即 CoreWeave 和其他定制能力较弱的较小规模新兴 GPU 云（neocloud）客户。在大多数超大规模云厂商的部署中，BlueField-4 模块将被其自研前端网络模块取代，或干脆换成更便宜的 CX-9。

说到 BlueField-4，有必要讨论黄仁勋今年早些时候在 CES 上着重介绍的新产品：ICMS，即推理上下文内存存储（Inference Context Memory Storage）——我们听说该平台可能在 GTC 上更名为「CMX」。ICMS（或 CMX）引入了第三张完全独立的网络，专用于上下文内存。CMX 是一套专用的 KV 缓存 fabric。随着长上下文推理把上下文窗口推向百万 token 量级、智能体并发在用户与服务之间不断扩展，当前用于存储 KV 缓存的内存层级开始显得力不从心。

KV 缓存随序列长度线性增长、随负载并行度乘性增长，很快就会超出任何单一层级内存的设计容量。GPU HBM 带宽与延迟无可匹敌，但单靠它不足以存放 KV，尤其对在多轮对话或工具调用之间日益流行的长序列查询而言。主机 DRAM 扩展了容量，但受节点绑定限制，总容量规模有限，最终容量仍有上限。与此同时，传统共享存储——为持久性而非延迟设计——访问时间与功耗开销更大，不适合参与解码循环。

正如我们 1 月中旬在[内存模型报告](https://semianalysis.com/institutional/ssd-and-storage-anchoring-note-the-best-is-yet-come/)中指出的，Nvidia 的 ICMS 在本地 SSD（G3）与共享存储（G4）之间插入了一个新的 G3.5 层，专为易失、可重算的 KV 缓存优化。ICMS 需要一层专为 KV 流量设计的专用网络。该架构中凡用到网络之处，都按上下文内存网络来供给——与通用数据搬运隔离，并针对可预测的解码延迟优化。

问题在于，行业对流向 ICMS / CMX 的 SSD 数量炒作得相当过头。我们在[内存模型](https://semianalysis.com/memory-model/)和 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)中做过测算。

BlueField-4 将成为这第三张网络的硅锚点。部署在存储阵列侧时，它以线速终结 NVMe-oF 与 RDMA 流量，并独立于主机 CPU 与 GPU 管理 KV 搬运。凭借 2x400G SerDes 链路提供的 800Gb/s 带宽、集成 Grace CPU 与 LPDDR，BlueField-4 将充当分布式上下文内存 fabric 的控制器。在偏好的 DGX 风格配置中，每托盘一颗 BlueField-4 可服务四颗 Rubin 处理器，DPU 完全专用于 KV 缓存流量，不与通用存储 I/O 共享。

新的 CMX/ICMS 生态系统很可能纳入 Weka、DDN、Dell Technologies、NetApp、VAST Data 等领先存储厂商。

### 供电

供电模块位于 BlueField-4 模块上方。该模块通过内部汇流排线缆接收 50V 电力，随后由模块化电源砖（power brick）将电流降至 12V，再通过更小的内部汇流排把 12V 电流送往 Orchid 模块、BlueField-4 模块与管理模块。

在 [VR NVL72 组件 BoM 与功率预算模型](https://semianalysis.com/vr-nvl72-model/)中，我们给出了 BlueField、Strata 板及机柜其余组件供电内容的拆解。

### 系统管理

管理模块由归入此类的多个更小的管理模块组成，占据 BlueField-4 模块与右侧 Orchid 模块之间的一条狭长空间。管理模块包括：

- 系统管理模块（SMM）
- 可信平台模块（TPM）
- 数据中心安全控制模块（DC-SCM）

这些模块为计算托盘提供管理与安全功能。超大规模云厂商通常有自研的管理模块设计，因此每个最终客户的管理模块可能各不相同。除 BlueField-4 外，供电模块与管理模块是计算托盘内 Nvidia 仅允许定制的另外两类组件。一些最终客户正考虑把管理模块集成进供电模块。尽管如此，各模块仍必须遵循 Nvidia 提供的形态规格，才能插入计算托盘中板上的指定连接器。

### 计算托盘拓扑

VR NVL72 的计算托盘拓扑与 GB200 和 GB300 大体相似。相对 Grace Blackwell 的三大差异是：GPU 与 ConnectX NIC 的连接、到本地 NVMe 存储的连接，以及 BlueField-4 与 ConnectX-9 之间的连接。

![](https://substack-post-media.s3.amazonaws.com/public/images/571bad1d-efd0-4475-8d55-1563d0c00448_3772x1694.png)
*来源：Nvidia VR NVL72 BoM 与功率预算模型*
![](https://substack-post-media.s3.amazonaws.com/public/images/596ff1e3-1d12-4353-8d7f-c71ac273ae75_3105x2014.png)
*来源：Nvidia VR NVL72 BoM 与功率预算模型*

首先，GPU 与 ConnectX NIC 之间的连接经历了从 GB200 到 GB300 再到 Vera Rubin 的演变。在 GB200 中，GPU 无法直接访问 ConnectX-7：B200 经 C2C 连接接到 Grace CPU，再由 Grace CPU 通过 PCIe 5 与 ConnectX-7 通信。在 GB300 中，Nvidia 引入了 NIC 直连 ConnectX-8，使 B300 GPU 无需经由 Grace CPU 即可与 ConnectX-8 NIC 直接通信。

本质上，这意味着 ConnectX-8 拥有两个主机：Grace CPU 与 B300 GPU，从而改善了后端网络的时延。然而对 VR NVL72 而言，Rubin GPU 与 ConnectX-9 的直连又退回到与 GB200 相同的设计，因为 Rubin 没有足够的 PCIe 带宽供两颗 Connect-9 使用。Rubin 经 C2C 链路连接 Vera，再由 Vera 通过 PCIe6 lane 连接 ConnectX-9。

其次，Rubin 的本地 NVMe 存储位置与 Grace Blackwell 中的 NVMe 存储不同。此前，本地 NVMe 存储由 BlueField-3 管理；对 VR NVL72，本地 NVMe 存储物理上位于 Orchid 模块上，由 ConnectX-9 管理。

![](https://substack-post-media.s3.amazonaws.com/public/images/edcb2919-19ac-481a-851c-24e14c7eedee_3422x2419.png)
*来源：Nvidia、Nvidia VR NVL72 BoM 与功率预算模型*

最后，BlueField-4 DPU 能够控制 8 块 ConnectX-9 后端 NIC，实现前端南北向网络与后端高速东西向网络的统一管理。这套系统名为高级安全可信资源架构（Advanced Secure Trusted Resource Architecture，Astra），从而把供应与监控负担从主机 CPU 上卸下。唯一的问题是 BlueField-4 价格昂贵，因此我们预计大多数超大规模客户会转而部署自研 DPU 方案。定制化问题将在后文详细讨论。

### 相对 Blackwell 的演进

VR NVL72 计算托盘中的这些模块虽非完全相同，但都能在 GB200/300 的计算托盘中找到对应物。唯一的区别是中板模块——它是为消除计算托盘内部线缆而引入的新组件。此外，机箱前部的模块（子模块）比 Blackwell 中的对应物长得多，以便经 PCB 把信号从中板连到前部 I/O 端口。下面几节我们将讨论无缆设计、散热设计的变化，以及计算托盘机械设计的变化。

# 计算托盘无缆设计

如上所述，VR NVL72 计算托盘围绕无缆概念设计。正如我们在**[去年 8 月的 PCB 超级周期核心研究报告](https://semianalysis.com/institutional/ai-server-pcb-super-cycle-copper-foil-content-upgrade/)**以及近期**[关于 Amphenol AI 内容的核心研究报告](https://semianalysis.com/institutional/amphenol-content-growth-vr-nvl144-backplane-board-to-board-connectors-dac-acc-aec-tam-kyber-midplane-backplane/)**中所讨论的，这一设计有两个原因。第一，飞线（flyover cable）在组装过程中容易受损，呈现出多个不同的故障点。第二，VR NVL72 的高密度设计留给线缆布线的空间有限。

### **以板对板连接器取代内部线缆**

对 GB200/300 而言，最有价值且由安费诺（Amphenol）独家供应的线缆是计算托盘内的 DensiLink OverPass 线缆组，提供 CX-7/8 NIC 与 OSFP 笼座之间的以太网连接。但这类线缆在组装中极易被刮伤或端接受损，造成大量故障点。另有若干更低端的 PCIe 线缆（MCIO 与 SlimSAS）同样存在这些故障点。这些线缆还牵涉许多其他供应商，令采购与供应商管理复杂化。鉴于线缆的娇贵，工人把线缆装入极其密集紧凑的机箱时必须格外小心，从而拉长了组装时间。

无缆设计乍看对 Amphenol 不利，实则反而是利好。Strata 模块与各子模块之间的信号仍然需要物理互连。在这一架构中，信号经 Amphenol 的 PaladinHD2 板对板连接器离开 Strata 板，再经由位于机箱中央的 PCB 中板走线；在 PCB 中板另一侧，各子模块通过另一组 Paladin HD2 B2B 连接器与中板相连。在 [VR NVL72 组件 BoM 与功率预算模型](https://semianalysis.com/vr-nvl72-model/)中，我们对 Amphenol 在 Vera Rubin NVL72 计算托盘中的内容做了详细拆解。我们的**[Amphenol AI 内容](https://semianalysis.com/institutional/amphenol-content-growth-vr-nvl144-backplane-board-to-board-connectors-dac-acc-aec-tam-kyber-midplane-backplane/)**一文对此也有更详尽的讨论。

![](https://substack-post-media.s3.amazonaws.com/public/images/675f09bf-ba67-4a1c-9586-eee07284d81d_2256x418.png)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

### **ConnectX-9 的重新安置**

为配合无缆设计，原本会装在 Strata 模块上的 CX-9 NIC 被移至 Orchid 模块（从机箱后半部移到前半部），如下图所示。

![](https://substack-post-media.s3.amazonaws.com/public/images/9a44425c-aa7a-46e2-bc0a-9c5f1cdfce92_1354x2353.png)
*来源：Nvidia VR NVL72 BoM 与功率预算模型*
![](https://substack-post-media.s3.amazonaws.com/public/images/164f7aed-a3bb-4037-be5a-039fcebf216f_1422x2419.png)
*来源：Nvidia VR NVL72 BoM 与功率预算模型*

对 GB200/GB300 而言，GPU/CPU 与 CX-7/8 之间的 PCIe 信号距离，短于 CX-7/8 与 OSFP 笼座之间的以太网/InfiniBand 信号距离。过去，要把 200G 以太网/InfiniBand 信号从计算托盘后半部的 NIC 传到计算托盘前部的 OSFP 笼座，必须使用飞线，因为每 lane 200Gbit/s（单向）的信号在 PCB 上的损耗过高。

而现在 NIC 离 OSFP 笼座更近，换成速率较低的 PCIe Gen6 信号（每 lane 单向 64Gbit/s）走更长的距离。让 PCIe Gen6 信号走长距离是可行的，因为 PCIe Gen6 的信号完整性优于更高速的 200G 以太网/InfiniBand 信号，信号可以经 PCB 传输。

### **PCB 对比飞线**

尽管如此，驱动 PCIe Gen6 信号穿越从 Strata 模块到 Orchid 模块前部约 500mm 的 PCB 距离仍然很有挑战。除了高质量的 SerDes，还需升级 PCB 材料才能实现合格的信号完整性。

首先，我们必须理解为什么高速信号在 PCB 上的表现不如飞线。随着 SerDes 速率提高，高速通道日益受制于 PCB 走线、过孔、介质材料与导体粗糙度带来的插入损耗（insertion loss）。插入损耗定义为信号经过互连通道时损失掉的信号功率。

![](https://substack-post-media.s3.amazonaws.com/public/images/c4ac828d-47ff-4fa3-953a-cc21a29d201a_1020x648.png)
*来源：Doosan、SemiAnalysis*

PCB 通道中造成插入损耗的三大机制是：趋肤效应与铜面粗糙度引起的导体损耗、层压板吸收引起的介质损耗，以及过孔与换层等不连续结构引起的几何损耗。

![](https://substack-post-media.s3.amazonaws.com/public/images/a9047e9c-d055-47c2-b963-d09f338fb564_1199x675.png)
*来源：DesignCon、Circuit Foil Luxembourg*

导体损耗由铜面粗糙度驱动。信号沿 PCB 铜走线传播时，因铜的电阻而损耗能量。频率越高，信号越向走线表面集中，此即趋肤效应。在铜的固有电阻之上，若表面粗糙，电流无法沿均匀路径流动，带来更大的电阻与损耗。

介质损耗源于介质材料的吸能特性。树脂与玻纤布等介质材料为 PCB 走线提供绝缘与机械增强功能。高频下，高速信号并非简单地只在铜走线中传播，而是以电磁波形式传播，电场延伸进介质材料。信号向前传播时，介质吸收一部分能量并以热的形式耗散，构成插入损耗。介质损耗随频率上升，因此是长距 PCB 走线信号性能的主导限制因素。

几何损耗描述 PCB 走线突变结构带来的插入损耗。真实 PCB 通道包含许多突变结构，如过孔与换层。它们就像公路上的颠簸，信号可能被反射回去并受干扰，增大插入损耗。

另一个影响信号性能的因素是串扰。随着每 GPU 的 I/O 数量增加，PCB 中的 lane 密度也随之上升。串扰指铜走线彼此过近、一条 lane 的信号影响相邻 lane 信号的情形。部分铜走线用于供电，当电源走线与信号走线过近时，电源走线的噪声也会调制信号。

总之，插入损耗随信号频率上升，高速信号在 PCB 上遭受的插入损耗大于飞线。因此，随着传统 CPU 服务器升级到更高的信号频率（如升级到新一代 PCIe），CPU 服务器设计会增加飞线的采用，以补偿 PCB 带来的插入损耗。替代方案是升级 PCB 材料，但对传统服务器应用而言，飞线性价比更高、依然可行。

对 VR NVL72，鉴于 AI 服务器更高的密度与制造复杂度，设计转向了无缆。更高的制造良率与组装时间缩短所节省的成本，超过升级 PCB 材料的更高成本。必须缓解所有造成 PCB 插入损耗的因素，因此 PCB 材料升级对 VR NVL72 是必需的。[我们在此按组件拆解了成本](https://semianalysis.com/vr-nvl72-model/)。

### **PCB 材料升级与面积增长**

VR NVL72 的 PCB 内容价值相比 GB200/GB300 将显著增长。这一内容增长的两大驱动因素是材料的大幅升级与高端 PCB 面积及层数的显著增加。我们的 [VR NVL72 组件 BoM 与功率预算模型](https://semianalysis.com/vr-nvl72-model/)提供了 VR NVL72 对比 GB200/GB300 的高端 CCL 与 PCB 内容金额拆解。

![](https://substack-post-media.s3.amazonaws.com/public/images/48aa0d51-0ac3-472d-8674-aa48f5fbe1c1_2710x663.png)
*来源：VR NVL72 组件 BoM 与功率预算模型*

材料方面，CCL 从 M7 升级到 M8/M9 带动材料升级。主要计算与网络板的铜箔全面升级到 HVLP4。为降低介质损耗需要升级玻纤布，但是否必须采用石英布（Q 布）仍有争议。下面我们讨论材料升级及每种材料采用背后的关键考量。

下表展示 Blackwell 与 Rubin 中各主要板卡的 CCL 分级与 PCB 规格。

![](https://substack-post-media.s3.amazonaws.com/public/images/88c63783-7d94-4c4f-a2ad-b1ca150403f5_2845x1393.png)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

CCL 材料的分级由其在给定频率下的介电常数（Dk）与损耗因子（Df）决定。Dk 与 Df 越低，插入损耗越低。业界普遍以松下（Panasonic）的 Megtron 系列为分级锚点，因为该系列一直在设定行业标准。人们说 CCL 属于 M7 分级时，通常指其 Dk 与 Df 规格与松下 Megtron 7 相当。

![](https://substack-post-media.s3.amazonaws.com/public/images/6b72a49b-42c7-4197-8098-dee66c98dc54_976x415.jpeg)
*来源：Panasonic*

Rubin 的信号层铜箔从 HVLP2 升级到 HVLP4 级。如前所述，由于趋肤效应，铜箔越光滑，插入损耗越低。HVLP 是超低轮廓铜箔（Ultra-Low Profile Copper Foil）的分类，HVLP 等级越高，表面粗糙度越低。

电源层方面，Strata 相比 Blackwell 增加的层数大多是电源层，以满足进入 GPU 的更大功率。增加专用电源层后，电源层与信号层得以分离，串扰随之降低。电源层铜箔厚得多，以承载流经的电流。

玻纤布升级旨在降低 CCL 的介电常数。除玻纤布外，树脂也是影响介电常数的关键因素。为实现理想的介电常数，各 CCL 厂商对 CCL 中两种介质材料的配方各有独门配方。目前围绕 CCL 规格的争议在于石英布（Q 布）的采用。

石英布是替代玻纤布作为增强层的下一代材料，可将介电常数进一步压低。除更低的介电常数外，石英布还更坚固、更耐高温、CTE 更低。另一方面，其成本比最高等级玻纤布高出数倍，且在 PCB 制造环节加工难度大得多，导致良率更差。

在 VR NVL72 中，石英最初用于 Orchid 板与中板，让最长距离的 PCIe Gen 6 信号以尽可能小的插入损耗穿越这两块板。然而，考虑到石英布的成本与 Q 布加工难度，Nvidia 目前正在探索降回玻纤布的选项。最终决定取决于降级玻纤布下的信号表现。

![](https://substack-post-media.s3.amazonaws.com/public/images/90d73db2-1e48-4675-8fab-46e2d57d2671_2255x1609.png)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

除材料升级外，PCB 内容价值的另一驱动因素是高端 PCB 覆盖面积的增加。在 Grace Blackwell 中，仅 Bianca 板（M7 级 CCL）与 NVSwtich 板（M8 级 CCL）采用高端材料，计算托盘前半部没有高端 PCB 覆盖。对 VR NVL72，Orchid 板与中板扩大了计算托盘内高端 PCB 的面积，覆盖机箱前半部。加上 Strata 板大于 Bianca 板以及计算托盘内额外的外围板，我们估算从 GB300 到 VR NVL72 高端 PCB 面积增加约 2.3 倍。如表所示，Orchid 板是 GB300 与 VR NVL72 机柜之间高端 PCB 总面积增量的主要贡献者。

我们的 [VR NVL72 组件 BoM 与功率预算模型](https://semianalysis.com/vr-nvl72-model/)提供了 VR NVL72 对比 GB200/GB300 的高端 CCL 与 PCB 内容金额拆解。

# 计算托盘：散热

VR NVL72 将液冷推向新高度。VR NVL72 计算托盘为 100% 液冷，而 GB200 与 GB300 计算托盘采用 85% 液冷加 15% 风冷的混合方案。因此，计算托盘移除了风扇，冷板覆盖范围扩大，以带走机箱前半部的热量。机箱中央将放置一个内部分液器（manifold），向各模块分配进液冷却液并收集回液。计算托盘内每个模块都附带冷板模块，各冷板模块经 MQD（Nvidia 针对计算托盘内紧凑区域应用定义的更小规格快速接头标准）连接到内部分液器。

![](https://substack-post-media.s3.amazonaws.com/public/images/2397b285-cb78-4081-8813-51a223db97bb_1354x2343.png)
*来源：Nvidia VR NVL72 BoM 与功率预算模型*

冷却液从机箱左后侧经 UQD 进入计算托盘，随后经管路进入内部分液器，分配到所有模块。冷却液吸收各模块的热量后重新汇入内部分液器，最后从机箱右后侧经 UQD 流出计算托盘。

![](https://substack-post-media.s3.amazonaws.com/public/images/ce22913e-61af-49e3-9487-fad91f7a8af7_2012x722.png)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

VR NVL72 的冷板也有多项升级。每个 Strata 模块的冷板将作为单一模块提供，覆盖整块 Strata 板，包括两颗 Rubin GPU、一颗 Vera CPU、SOCAMM 模组及各 VRM 组件。Rubin GPU 的冷板升级为「微通道冷板」（MCCP）：冷板内通道间距从 150 微米缩小到 100 微米，从而增大表面积、提升冷板散热能力。此外，与 Rubin GPU 接触的表面将镀一层金，原因是防止液态金属铟 TIM2 对铜的腐蚀。

![](https://substack-post-media.s3.amazonaws.com/public/images/78fa8a53-ba67-4917-96be-3d5da6051095_1876x584.png)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

Strata 模块之外，机箱前部的模块同样附带冷板模块。每个 Orchid 模块将有一个覆盖 CX-9、E1.S SSD、收发器笼座及各 VRM 的冷板模块。冷板加板卡的高度不足 0.5U，因为两个 Orchid 模块堆叠在 1U 机箱内。每对 Orchid 模块仅共享一对来自分液器的 QD，另有一组分液器向这对 Orchid 模块的上下两块冷板分配冷却液。在 [VR NVL72 组件 BoM 与功率预算模型](https://semianalysis.com/vr-nvl72-model/)中，我们包含冷板模块、分液器与快速接头等全部各类散热组件的内容。

![](https://substack-post-media.s3.amazonaws.com/public/images/8e1b96be-6742-4679-8180-275aaad0521d_3164x999.png)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

此前，冷板在 L10 组装层级（各组件装入机箱）安装。采用模块化方案后，冷板需要与模块本身更紧密地集成，因此冷板将在 L6 组装层级、紧接 PCBA 工序之后安装。这提升了组装效率，因为 L10 组装被简化为把成品模块插入相应的连接器与快速接头。

# **计算托盘：供电**

在计算托盘层面，50VDC 电力经机箱后部的汇流排夹（busbar clip）进入计算托盘，再经内部汇流排线缆抵达机箱中部。由此，电力路径分为三个去向。第一路与第二路分别前往左侧和右侧的 Strata 板，内部汇流排线缆直接向 Strata 板馈入 50VDC。第三路前往机箱前部的配电模块：内部汇流排线缆将 50VDC 馈入一个从 PCB 中板下方穿过的汇流排装置，连接中板另一侧的配电板（PDB）。这与 Grace Blackwell 不同——后者的 50VDC 直接送往 PDB。随后，PDB 向计算托盘内所有板卡馈入 12VDC。

![](https://substack-post-media.s3.amazonaws.com/public/images/cc71c2bc-25a1-4ac8-93e1-e880143cdcee_1148x2332.png)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

50VDC 经 Strata 板两侧的其中一个 50V 电源连接器进入 Strata 板，由 Strata 板底部的 IBC 模块降至 12VDC，再由 VRM 降至 1VDC 后馈入 Rubin GPU 与 Vera CPU。Strata 直接接收 50VDC，而 Grace Blackwell 的 Bianca 板从 PDB 接收 12VDC。由于 Strata 板功耗约 4800W（相当于一般服务器机柜 TDP 的一半），而 Bianca 为 3000W，必须以更高电压向该板供电。把 50VDC-12VDC 转换移近负载的好处是降低电流、提高传输效率。由于功率损耗与电流呈平方关系，50V 下 96 安培的功率损耗比 12V 下 400A 低 17 倍。

[VR NVL72 组件 BoM 与功率预算模型](https://semianalysis.com/vr-nvl72-model/)中包含各类 VRM 全部功率半导体的用量与 ASP。

Vera 与 Rubin 之间的功率动态调配（power sloshing）依然存在，这是承自 GB300 的特性，我们在此前文章中已有讨论。通过在 GPU 与 CPU 之间共享 4800W 的功率供给，可以实现更高效的功率规划。在 GPU 重负载下，每颗 GPU 获得 2300W，留给 CPU 200W；当 GPU 需求下降时，Vera 可动态提升到更高功率，帮助尽量减少 GPU 空转时间，同时避免过度配置功率。

对机箱前部的模块——CX-9、BlueField-4 与管理模块——PDB 向各模块馈入 12VDC。50VDC 在 PDB 降至 12VDC，随后 PDB 经一个铜汇流排装置向相邻模块馈入 12VDC。CX-9 的电源连接器位于模块顶部 Paladin HD2 附近。

# 计算托盘：机械

VR NVL72 计算托盘的机械组件比 Grace Blackwell 略为复杂。在机箱前部，有一个把前部分为三段的机械结构：左右两段容纳 Orchid 模块，中段容纳 BlueField-4、供电与管理模块。每个模块还有自己的小金属底盘。该机械结构提供简单的导向机构，引导模块与中板及内部分液器完成盲插（blind mate）。

![](https://substack-post-media.s3.amazonaws.com/public/images/ac48da42-8603-43a2-a4b7-f852c1c09c5a_1460x922.png)
*来源：Nvidia、SemiAnalysis*

中板与内部分液器作为一个模块一起出货，其机械设计如上图所示。这些高亮的机械部件充当模块的加载机构：对模块施加一定作用力将其锁定到位，确保模块与 Paladin 连接器及 MQD 良好连接。

# 机柜级基础设施：散热

除了重新设计的无风扇前部机箱与 100% 液冷计算托盘，Vera Rubin 散热架构讨论中最引人注目的，是黄仁勋关于冷却液/水温度与冷水机组使用的评论。对许多人（更广泛地说，对「市场先生」！）而言，Vera Rubin 能以 45C 进液温度运行、从而可能避开机械压缩式冷水机组的说法，被散热供应商生态中的许多人视为重大意外。我们则将其视为既有趋势的延续。

Vera Rubin 能以 45C 进液温度运行，但 Blackwell 已能在 40C 以上的进水温度下运行（例如 Supermicro 的 DLC-2 系统）。联想（Lenovo）与 HPE 等主要系统厂商自 2025 年初以来也一直在讨论以 45C 运行的 100% 液冷架构。2024 年，HPE 发布了基于全液冷的工业级散热系统，类似做法在 HPC 领域早已长期使用。联想在 2025 年 OCP 峰会上介绍了其 Neptune 液冷方案的下一代产品，全液冷并同样使用 45C 水。

![](https://substack-post-media.s3.amazonaws.com/public/images/9fe04678-76b1-406b-bb5a-c7822727bab0_1863x1070.png)
*来源：HPE*

再看施耐德（Schneider）2025 年 9 月发布的 GB300 参考设计 111 作为另一个例子。该参考设计中，数据中心采用双环路架构：一个专用于风冷（向风扇墙供冷）的冷冻水环路，以及一个单独的、温度更高的液冷专用环路。液冷侧，TCS 以约 40C 向冷板循环输送冷却液并以更高温度回液，CDU 再把热量传入设施水环路——后者进入 CDU 的温度约为 37C。

![](https://substack-post-media.s3.amazonaws.com/public/images/345a084e-4701-4993-819c-892c840fbb4d_1717x960.png)
*来源：Schneider*

所以 45C 冷却并非全新事物。即便具备这一能力，部署 Blackwell 的大多数运营商仍按 20-30C 水温设计。粗略而言，当前 Blackwell 进液温度接近室温，回液温度在 40-50C 区间。只有少数运营商（如 Firmus）在气候允许的情况下从环路中去掉了冷水机组（即便使用 GB200 这类系统），转而采用高度优化的经济器设计。省去机械制冷中的压缩环节可带来可观的能效收益。

那么，在 Vera Rubin 的功耗与发热约为 Blackwell 两倍的情况下，Nvidia 如何为这头散热怪兽降温？回答之前，值得再加一层考量：更高的进液温度虽然提升能效，但当进液温度逼近最大回液温度（系统的上限温度）、温差（delta-T）收紧时，散热变得更困难。温差越小，带走同样热量就需要更高的水/冷却液流量。在 Blackwell 参考架构中，上限温度约 65C（例如参见 Vertiv 的 GB200 NVL72 参考设计）。

![](https://substack-post-media.s3.amazonaws.com/public/images/8dfbf6ca-5b7c-4296-b4e3-56f41888f963_2801x1132.png)
*来源：Vertiv*

尽管 NVIDIA 最初并未正式公布 Vera Rubin 液冷系统的完整规格，我们相信该平台将支持最高 65C 的冷却液回液温度。这与 Nvidia 的温水运行包络一致；对 delta-T 的确切影响取决于所选供水设定点与流量控制策略，我们预计 delta-T 会略微收紧。压力包络预计与 GB200 相比不变：最大工作压力 72 psig（5 bar），最小爆破压力 217 psig（15 bar），与 OCP 的 MGX 机柜级液冷规范对齐。

![](https://substack-post-media.s3.amazonaws.com/public/images/80029eec-d319-4b7a-8fa2-452e463f396e_1782x774.png)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

实践中，散热遵循直白的物理规律。要冷却一个系统，必须以适当的温度与压力在环路中输送足够的水/冷却液。若想提高 CDU 的制冷能力，就要在管控压力的同时提高流量——本例中意味着约 2.0-2.5 倍的流量提升，具体取决于运营商实际把回液温度推到多高。

Nvidia 已表示，Vera Rubin 提高了液冷流量，在 CDU 扬程不变、不引入额外散热复杂度或成本的前提下，实现接近 Blackwell 两倍的散热性能。Nvidia 通过优化整个液流路径达成这一点。我们预计快速接头会更大以支持更高流量，分液器与管路也会更新。如下图所示，供应商路线图表明，至少对下一代机柜而言，2 英寸 QD 应足以在压力与流速限制内容纳更高流量。

![](https://substack-post-media.s3.amazonaws.com/public/images/00716966-64d3-4d63-b50d-823b873e285c_2026x1132.png)
*来源：CoolIT*

## **采购与散热供应商影响**

更新的散热架构与翻倍功率密度对供应商的主要影响关乎 CDU 与机柜-CDU 配比。今天一台 CDU 约可支持 10 个 GB200 机柜。若单柜发热量约为 2 倍，除非 CDU 容量提升，该配比就得下降，意味着要么更多 CDU、要么更大容量的 CDU。我们认为多数主要运营商希望维持约每台 CDU 10 柜的比例。随着机柜功率密度上升，这指向更大的 CDU。如今列间（in-row）CDU 的制冷能力最高约 2 MW，但我们预计未来的设施级 CDU 将达到 3-6 MW。台达（Delta）目前在 CDU 专业厂商细分市场领先，施耐德电气、Vertiv 与 nVent 亦居前列。富士康（Foxconn）与广达（Quanta）主导系统集成商类别。

![](https://substack-post-media.s3.amazonaws.com/public/images/93c57f79-8dcb-46da-985f-f026e5181a64_2740x1537.png)
*来源：CoolIT*

从液冷+风冷转向 100% 液冷系统，叠加更高流量与更大制冷量，将要求整个散热栈做出改变。L2A CDU 中的风扇与散热器随时间推移重要性下降。话虽如此，在当前上行周期——部署速度比完全优化更重要——L2A 有望保持可观份额，尽管长期轨迹明显有利于 L2L。高密度 L2L 系统还将要求 TCS 的大部分重新设计，包括更新的分液器、更大的快速接头（Colder Products Company、Danfoss、Staubli、Parker Hannifin）、镀金冷板（AVC、Delta、Boyd、CoolIT、Auras），以及非常关键的、能够输送所需水量的大型泵。泵的选型与功率密度及必须带走的热量直接相关。甚至这些泵所用电机与驱动部件的制造商（如 Allegro MicroSystems），前景也可能随之改变，因为需要更大的电机、更多的电机，或两者兼有。总之，TCS 环路上更高的热量很可能提高白区散热供应商的内容/兆瓦。受益最大的是 QD，其次是分液器与冷板；CDU 也会受益，但程度较轻。

对 FWS 布局而言，头条影响是无冷水机组设计的可能性。虽然我们在面向核心研究与数据中心模型订阅者的单独说明中已讨论过这场争论，这里重申：这并非彻底颠覆。一些运营商已在更 AI 优化的设计中运行无冷水机组的 Blackwell 系统，另一些则出于负载灵活性、混布机房兼容性、冗余与可靠性而保留冷水机组。长期看，我们预计 AI 优化系统将使冷水机组愈发不必要，内容从风冷冷水机组转向干冷器或绝热冷却塔。我们目前估算风冷冷水机组内容约 $0.5M/MW，而干冷器或绝热冷却塔约 $0.2M/MW。SPX Technologies 与 BAC、Evapco 可能受益，而 Johnson Controls、Carrier 与 Trane 或受冲击。尽管如此，我们预计这种效率/灵活性的权衡中期内将持续，并不认为冷水机组会一夜之间进入下行。[详见我们的工业模型。](https://semianalysis.com/industrials-model/)

# 机柜级基础设施：供电

在 [2024 年的 GB200 文章](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component)中，我们讨论了供电从节点级 PSU（电源单元）到集中式机柜级电源架的上一轮演进。随着 VR NVL72 机柜 TDP 从 GB200 与 GB300 的 120kW-140kW 升至 180kW-220kW，供电基础设施再次演进。下面我们将讨论参考设计中机柜级的供电基础设施，以及 VR NVL72 计算托盘级的供电。

自 GB200 部署以来，供电基础设施演进的主线是传输效率与电力稳定。超大规模云厂商正围绕高密度 AI 服务器机柜带来的挑战开发供电基础设施，路线图指向未来几年每机柜 1MW。因此，HVDC（高压直流）电源机柜、BBU（电池备份单元）、CBU（电容备份单元）、液冷汇流排与 SST（固态变压器）正在被开发，以提升传输效率与电力稳定性。这些将由客户根据各自的专有基础设施设计部署。[关于 AI 训练对电网挑战的更多细节，我们在本报告中已有讨论。](https://newsletter.semianalysis.com/p/ai-training-load-fluctuations-at-gigawatt-scale-risk-of-power-grid-blackout)

![](https://substack-post-media.s3.amazonaws.com/public/images/06dbd2aa-7e3c-4f9a-ab81-60bcc8b26b5c_733x1702.png)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

在 VR NVL72 参考设计中，机柜级供电基础设施包括四个 110kW 电源架。对 2300W Rubin TDP SKU，VR NVL72 系统 TDP 最高 220kW。四个 110kW 电源架的设计属于 N+1 冗余方案。每个 110kW 电源架高 3U，内含六个 18.3kW PSU，PSU 内置电容。每个电源架从两条 100A whip 电源线接收三相 415VAC-480VAC 电力，将 415VAC-480VAC 降至 50VDC 后送入汇流排。有趣的是，VR NVL72 的汇流排额定电流为 5000A+，远高于 Grace Blackwell 的 2900A。鉴于极高的电流且机柜内无风扇，汇流排必须液冷。

![](https://substack-post-media.s3.amazonaws.com/public/images/ea4bba56-9812-4977-8f9e-201a0cab7ff1_1640x940.png)
*来源：TE Connectivity、OCP 2025*

对超大规模客户而言，他们可能选择部署独立电源机柜，采用 LVDC（低压直流）或 HVDC（高压直流）。下面我们给出 VR NVL72 电源机柜部署的两种可能情形。

![](https://substack-post-media.s3.amazonaws.com/public/images/882952fa-6781-496c-b90a-2bcb9eb0f1bc_3165x2172.png)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

第一，VR NVL72 机柜搭配运行于 800VDC（Nvidia 规格）或 +/-400VDC（OCP 规格）的 HVDC 电源机柜。由于 VR NVL72 机柜汇流排仍为 50V、计算托盘只能接收 50V，来自电源机柜的 800VDC 无法直接送入汇流排，VR NVL72 机柜内仍需 DC-DC 电源架。如下所示，DC-DC 电源架将电流从 800VDC 降至 50VDC。

第二，某些客户（如 Meta）可能考虑将网络交换机机柜与 BBU、CBU 电源架集成，以提升效率并削峰。这使 GPU 机柜内原本放不下的更多 CBU/BBU 容量得以安置。BBU/CBU 与交换机机柜将通过 50V 水平汇流排连接到 GPU 机柜。Meta 称之为高功率机柜（high power rack），已在 OCP 上讨论过。

更多电力与架构细节见我们的 [VR NVL72 组件 BoM 与功率预算模型](https://semianalysis.com/vr-nvl72-model/)。

# 网络：NVLink 6 与 Rubin 横向扩展

NVIDIA 的代际创新是演进式而非革命式。GPU 纵向扩展与横向扩展带宽约每 18 个月翻倍，NVIDIA 机柜中的铜基础设施正持续创新，以承载更高带宽的负载。纵向扩展网络基础设施最终会引入光器件以构建更大的互联规模（world size），但那是另一篇文章的主题。

下表展示纵向扩展与横向扩展网络速率的演进。Vera Rubin 采用的 NVLink 6 通过在同一数量的铜缆上实现双向信号传输将 NVLink 带宽翻倍——等效于每 NVLink 4 条 200G lane。后文将详述。

![](https://substack-post-media.s3.amazonaws.com/public/images/4e17ee04-dce9-4fde-b4fc-6b3f5dff2849_2233x1207.png)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

让我们逐一梳理 Rubin 网络的关键特性，以及围绕 Rubin 纵向扩展与横向扩展网络可能构建的架构。

### **面向纵向扩展的双向 SerDes**

从 GB300 NVL72 的 NVLink 5 到 Vera Rubin NVL72 的 NVLink 6，每逻辑 GPU 带宽翻倍，靠的是对铜背板使用同时双向（simultaneous bi-directional）SerDes，而非提高调制阶数或波特率。NVLink 5 每电气 lane 传输 224G，NVLink 6.0 每电气 lane 传输 448G。每条电气 lane 是一个差分对（DP），由两根承载等幅、反相信号的导体组成。

![](https://substack-post-media.s3.amazonaws.com/public/images/a92bb668-9e15-45d7-91a5-ed8bba8f3e2a_1946x1300.png)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

由此产生一个工程问题：如何确保导线两端都能接收到干净的信号，因为沿同一根铜线相向传输的两路信号会叠加（superpose），形成一个与预期发送信号不同的复合信号。

在光域，双向互连可通过在收发器中集成光环形器（circulator）实现，如我们去年底发布的 [TPUv7 文章](https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the)所述。环形器通过把[入向与出向信号路由到不同路径](https://newsletter.semianalysis.com/p/google-apollo-the-3-billion-game)，确保两者在光电二极管接收端互不重叠。而铜域的双向互连要棘手得多：铜缆是线性传输线，无法使用环形器，入向与出向信号会在接收端通过叠加求和。因此，铜线两端的接收器都需要一种机制，把本地 TX 与本地 RX 分离开来。

这个问题的解决方案是在导线两端各使用一个混合器（hybrid）。没有混合器，本地 RX 处会产生自干扰，因为本地 TX 与本地 RX 沿同一根线传输：

因此，必须在本地 RX 处生成本地 TX 的反相副本，以实现适当的回声消除：

下图展示了这一动态过程：

![](https://substack-post-media.s3.amazonaws.com/public/images/befba865-35dc-46a0-b593-48fa65baa8ae_4380x2667.png)
*来源：IEE Explore*

双向信号传输已被用于短距（小于 5mm）裸片间互连，而格外引人注目的是 NVIDIA 把该技术扩展到了至少 1m 距离的铜背板长距传输。

双向信号传输的挑战在于，回声消除必须精确校准，否则本地 TX 副本生成中的轻微延迟都可能导致链路失效。然而，若 NVIDIA 继续使用 200G SerDes，带宽翻倍就意味着背板铜缆数量翻倍，而这在若干方面都是难以企及的。

Blackwell 世代在背板上塞入约五千根铜缆，已在规模部署中引入不可忽视的可靠性失效模式。若继续沿用常规 200G SerDes 同时把纵向扩展带宽翻倍，需要背板翻倍到一万根铜缆：只会进一步增加制造复杂度与系统失效概率。

![](https://substack-post-media.s3.amazonaws.com/public/images/f79a0f25-17d9-4603-93ae-44a793db3705_4380x2490.png)
*Blackwell 铜背板。来源：Nvidia*

NVIDIA 也可以选择像 [AMD Helios 机柜](https://newsletter.semianalysis.com/p/amd-advancing-ai-mi350x-and-mi400-ualoe72-mi500-ual256)那样部署更宽的机柜，但这可能影响 PCB 上的信号完整性，因为电信号将不得不穿越更长的路径。

### **纵向扩展网络——NVLink 6**

铜背板上采用的双向 SerDes 技术用于 NVIDIA 的纵向扩展网络。对 Vera Rubin NVL72，纵向扩展网络继续保持轨道优化（rail-optimized），纵向扩展域内每颗 GPU 与每颗交换 ASIC 之间实现全互联。

去年，我们讨论过 NVIDIA 的 GB200 纵向扩展架构：NVL72 系统在单个机柜内包含 18 颗 NVLink 5 Switch 芯片。

尽管 VR NVL72 系统使用的 NVLink 6 Switch 提供与 NVLink 5 Switch 相同的每颗 28.8T 聚合带宽，但 NVLink 6 Switch 的 SerDes 速率是 NVLink 5 Switch 的两倍，而 DP 数量相同。因此，为了提供 NVLink 6 所需的两倍聚合纵向扩展带宽，Vera Rubin NVL72 机柜将包含两倍于 GB200 机柜的 NVLink Switch。折算下来即 9 个交换托盘、每托盘 4 颗 NVLink Switch 芯片，亦即每个机柜 36 颗 NVLink Switch 芯片。

每个 VR NVL72 交换托盘包含 4 颗 NVLink 6 Switch ASIC 和一个系统管理模块。与为 GB200 发布的第一代 Oberon NVLink 5 Switch 相比，Rubin NVLink 6 交换托盘的设计也更简单、相对更无缝，因为 Rubin NVLink 6 交换托盘不再使用飞线，所有 NVLink 信号都将在 PCB 上走线。

NVLink 6 Switch 板为液冷，由单一模块式冷板覆盖。连接到 NVSwitch 托盘的是系统管理模块（SMM），自带 CPU、充当交换托盘的主机。交换托盘与 SMM 的连接使用飞线，但这是整个 Vera Rubin NVL72 系统中唯一需要的飞线连接。鉴于 PCIe 连接速率较低且 NVLink Switch 托盘包含的模块相对较少，交换托盘的组装预计不会太难。

![](https://substack-post-media.s3.amazonaws.com/public/images/9a0db27b-2364-4f3e-8e5b-14a31327c898_919x1501.png)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

下图展示 NVLink 6 信号如何穿越托盘。每条绿线代表 9 个 NVLink 6 400G 逻辑端口，即 18 条 200G TX/RX lane。由于每 lane 仅 1 个 DP 采用双向 SerDes，任一连接器与任一交换芯片之间共 18 个 DP，每个连接器合计 72 个 DP，与前代 NVLink 5 Switch 托盘相同。

![](https://substack-post-media.s3.amazonaws.com/public/images/ccd14529-356f-493a-ad9a-4fe57d339d9d_883x1485.png)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

如前所述，高速信号需要更好的 PCB 材料，对 NVLink 6 尤其如此——由于采用双向信号传输，其对插入损耗的容忍度低得多。PaladinHD2 连接器与 NVLink Switch 之间的 lane 数量也给 PCB 设计带来复杂度。因此，NVLink 6 Switch 板 PCB 升级为 32 层、M8+ 级 CCL——至少为 LDK2 玻纤布，也可能采用石英纤布。

交换托盘及各组件的更多细节见 [VR NVL72 组件 BoM 与功率预算模型](https://semianalysis.com/vr-nvl72-model/)。

拉远视角：VR NVL72 系统用背板铜缆连接 NVLink Switch 托盘与 GPU 托盘。尽管带宽翻倍，但借助双向 SerDes，从 GB300 背板世代到 Vera Rubin NVL72 背板世代，所需线缆数量不变。连接器数量与每连接器 DP 数量从 Grace Blackwell NVL72 到 VR NVL72 也不变。

![](https://substack-post-media.s3.amazonaws.com/public/images/e18bd90a-d96f-4237-bb8a-bb5b0f0e0582_3193x1126.png)
*Grace Blackwell NVL72 纵向扩展拓扑。来源：SemiAnalysis AI 网络模型*![](https://substack-post-media.s3.amazonaws.com/public/images/a4533a61-ae9d-45a4-a80b-c5d76f70bd6d_3150x1090.png)
*Vera Rubin NVL72 纵向扩展拓扑。来源：SemiAnalysis AI 网络模型*

VR NVL72 系统的 GPU 与纵向扩展交换机由铜缆连接，而 VR HGX 系统的服务器由 8 颗 Rubin GPU 与 4 颗 NVLink Switch 芯片组成。NVL72 与 HGX 部署之间的第二个重要差异是：前者每 GPU 横向扩展带宽为 1.6T，而后者仅为每 GPU 800G。既然部分部署的每 GPU 横向扩展带宽只有一半，为什么所有 Rubin 200 部署都使用 CX-9 NIC？

HGX Rubin NVL8 服务器包含 8 个 800G CX-9 NIC 封装——每 GPU 一个——这意味着横向扩展带宽较其前身 HGX B300 服务器并无提升。而 Vera Rubin NVL72 部署把每 GPU 横向扩展带宽翻倍到 1.6T，但并非靠翻倍单 NIC 带宽：每颗 Rubin 芯片所对应的「1.6T NIC」由两个 800G CX-9 封装组成，经 PCIe Gen 6.0 lane 连接到 Vera CPU。

VR NVL72 每个计算托盘有 8 个 800G CX-9 NIC，但 OSFP 笼座数量有两种可能：要么每 GPU 一个 1.6T OSFP 笼座、每计算托盘共 4 个，要么每 GPU 两个 800G OSFP 笼座、每计算托盘共 8 个。我们认为后者会是更普遍的部署假设，并将作为本文后续横向扩展网络架构讨论的基础情形。

### **在横向扩展 InfiniBand 网络中连接 GPU**

大体上，Vera Rubin NVL72 的横向扩展部署有三类。其一是采用 NVIDIA Quantum 系列交换机的 InfiniBand 集群；其二是采用 Spectrum 系列交换机的 NVIDIA 以太网集群；最后是非 Nvidia 以太网，如基于 Tomahawk、Cisco Silicon One 或 Teralynx 的以太网交换机。超大规模云厂商部署的一些以太网集群会在 NIC 到 TOR 与交换机间连接中使用 AEC，而另一些仅使用光互连的以太网集群通常采用多平面、多轨道网络架构。不过，Vera Rubin NVL72 部署尤其值得注意的一点是：这是首个我们将在横向扩展后端网络中看到共封装光学（CPO）部署的 Nvidia GPU 世代。

虽然 InfiniBand 与 Spectrum-X 集群都存在，基于 InfiniBand 的 Quantum X800-34XX 系列交换机在新兴 GPU 云（Neocloud）中比在超大规模厂商中更受欢迎。InfiniBand 有两种部署类型：其一是采用可插拔光模块的 Quantum X800-Q3400，其二是采用协封装光引擎（OE）替代可插拔收发器的 Quantum X800-Q3450 CPO 交换机。

Quantum X800-Q3400 在逻辑上是一台多平面交换机，把 4 颗 Quantum-3 ASIC 组合进单个交换机箱，不过我们会在后文深入讨论这一等价性。这种多平面「拓扑」被抽象掉了，在网络工程师看来，Q3400 就是一台 144 端口的单交换机——或称「小男孩」（little boy）交换机。

![](https://substack-post-media.s3.amazonaws.com/public/images/c3908b30-94ca-4a19-a964-75806231894a_2695x1059.png)
*来源：SemiAnalysis AI 网络模型*

因此，HGX Rubin NVL8 服务器的 InfiniBand 架构实际上是一个单平面、8 轨道网络：每颗 HGX Rubin NVL8 GPU 有一条 800G 上行链路连到 leaf 交换机。

![](https://substack-post-media.s3.amazonaws.com/public/images/eacb373c-b4b3-4125-b335-d90e8d4caf2e_2538x1267.png)
*来源：SemiAnalysis AI 网络模型*

而对 Vera Rubin NVL72 部署，每 GPU 有两个 800G OSFP 笼座，合计每 GPU 1.6T 带宽。每 GPU 拥有两个 800G 逻辑端口是有利的，因为它允许在不复杂的纤缆管理下部署多平面网络——把一个逻辑 GPU 一分为二，连到两台不同的 leaf 交换机。因此，用两个 800G 逻辑端口能够构建比单个 1.6T 逻辑端口更大的网络集群。事实上，正如我们在此前多篇文章（如 [NVIDIA 的光魔（Optical Boogeyman）](https://newsletter.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband#the-clos-non-blocking-fat-tree-network)与[微软 AI 战略解构](https://newsletter.semianalysis.com/p/microsofts-ai-strategy-deconstructed)的网络章节）中所解释的，这一关系由一个简单公式决定——在 L 层网络中，使用 k 端口交换机可支持的最大主机数：

举例而言，设想两个分别使用 1.6T 与 800G 逻辑端口的假想 VR NVL 部署。采用单个 1.6T 逻辑端口的 1 平面、3 层网络只能达到最大 93,312 颗 GPU 的集群规模，即：

所谓单个 1.6T 逻辑端口，是指连接每颗 GPU 的两个 800G OSFP 笼座在 leaf 层连到单个双端口 1.6T 收发器，因为这两个 800G 端口实际执行的是一个 1.6T 端口的功能——故称「逻辑」。

![](https://substack-post-media.s3.amazonaws.com/public/images/ec57efde-b531-4f61-9d11-8703e99c5e20_3145x1357.png)
*来源：SemiAnalysis AI 网络模型*

要突破 93,312 GPU 的最大集群规模，可以部署 2 平面网络：把支持一颗 GPU 的两个 800G OSFP 笼座分别连到不同网络平面的不同 leaf 交换机。这样就能构建下图所示的 186,624 GPU 集群，甚至扩展到 746,496 GPU 的集群规模。

![](https://substack-post-media.s3.amazonaws.com/public/images/513cc763-5600-427d-a834-c1649efcc764_2626x1711.png)
*来源：SemiAnalysis AI 网络模型*

我们认为，带两个交换平面的第二种集群很可能是 Vera Rubin NVL72 InfiniBand 部署中更普遍的参考架构。

除风冷的 X800-Q3400 交换机外，NVIDIA 还将提供 CPO 版本 X800-Q3450，同样包含 144 个 800G 端口。如前所述，两款交换机的独特之处在于，每个交换机箱由 4 颗 28.8T Quantum-3 Switch ASIC 组成，单箱交换容量合计 115.2T。与 VR NVL72 服务器配合使用时，leaf 层 NIC 的信号在箱内被一分为四——每路 200G——分别送往箱内的每颗交换 ASIC。这种配置在逻辑上等价于 4 平面网络架构。

![](https://substack-post-media.s3.amazonaws.com/public/images/ab4648e8-1c21-41ba-92dc-457ddb09e3dc_2133x1368.png)
*来源：SemiAnalysis AI 网络模型*

### **基于以太网的集群部署**

尽管对 H100、GB200 等前几代 NVIDIA 芯片而言，InfiniBand 一直是更流行的网络架构，NVIDIA 正在激进地推广 Spectrum 以太网网络，并推出了多款交换机 SKU：

1. SN6600，102.4T 液冷交换机；
2. SN6800，4 ASIC、2048 端口数（radix）、409.6T 多平面 CPO 交换机，提供 512 个 800G 端口；
3. SN6810，高端口数 102.4T CPO 交换机，另有三种进一步的部署选项：512 个 200G 端口、256 个 400G 端口和 128 个 800G 端口。

对 SN6600 交换机，横向扩展参考架构是 8 平面网络，每颗 GPU 以 8 路扇出到 8 个不同平面。这与使用 SN6810 交换机的 8 平面横向扩展网络参考架构类似。

![](https://substack-post-media.s3.amazonaws.com/public/images/c31a2ad9-ef3a-4da2-83be-b8b39200d7e0_2605x1330.png)
*来源：SemiAnalysis AI 网络模型*

我们认为拥有 512 个 800G 端口的 SN6800 交换机对新兴 GPU 云会相当有吸引力，因为它简化了部署。与 X800-Q3400 横向扩展网络类似，SN6800 横向扩展网络可以由两个交换平面组成，不过 SN6800 能实现大得多的可行横向扩展互联规模。

下图展示了这种网络的可能形态——不过只画出了两个平面之一，读者可以从我们只描绘了每颗 GPU 1x800G 这一事实推断出来。另请注意，每个 SN6800 交换机箱由 4 颗 ASIC 组成，各有自己的交换平面，我们将在后文详述。

![](https://substack-post-media.s3.amazonaws.com/public/images/5e626b67-f940-4e47-a5d8-d3790f86d155_2611x1315.png)
*来源：SemiAnalysis AI 网络模型*

对一台 512 端口交换机，两层交换可连接最多 131,072 颗 GPU，3 层则可连接惊人的 33,554,432 颗 GPU。

对 CoreWeave 和 Lambda 这类新兴 GPU 云而言，在大规模集群部署中，SN6800 等 CPO 交换机能带来什么优势？

如我们近期[共封装光学深度解析文章](https://newsletter.semianalysis.com/p/co-packaged-optics-cpo-book-scaling)所述，第一个原因是消除大部分收发器内容可节省可观的电力。若把一个 800G DR4 光收发器（16-17W）的功耗，与光引擎（OE）及外置光源（ELS）模块在横向扩展网络中提供等效 800G 带宽所需的功率相比，光收发器的功耗平均降低约 70%。退一步看，在 3 层 HGX Rubin NVL8 集群中，这相当于网络设备总功耗节省 10%。不过，网络设备功耗的这一降幅相对而言并不显著，仅约占集群总功耗的 1%，因为服务器的功耗预算主导整个等式。

![](https://substack-post-media.s3.amazonaws.com/public/images/db19c505-aef9-494d-ab39-8e3caa913cf7_2902x936.png)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

第二个好处是几乎消除全部收发器所带来的成本下降。若考虑 NVIDIA LinkX 收发器，降价空间甚至更大——其定价往往显著高于同类通用产品。若比较有/无 CPO 交换机的 3 层网络横向扩展域总网络成本，收发器成本平均降低约 75%。然而，与上述省电一样，考虑到整个集群的成本，这类节省通常不足以扭转大局。

![](https://substack-post-media.s3.amazonaws.com/public/images/23326c48-f03b-409d-ad25-a64c79a62581_2902x953.png)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

我们在 [CPO 报告](https://newsletter.semianalysis.com/p/co-packaged-optics-cpo-book-scaling)中更详细地列出了这些计算，并更大篇幅地讨论了该话题。

整体网络可靠性的提升是另一个有力论点。收发器可能不可靠，大型集群必然存在持续的链路抖动。[Meta 在 ECOC 上发表的研究](https://newsletter.semianalysis.com/i/178153689/when-will-cpo-be-ready-for-primetime)在 1500 万 400G 端口-设备小时上给出了强劲的可靠性结果，约相当于 15 台 CPO 交换机在实验室测试 11 个月。这是个令人鼓舞的开端——但我们认为，随着更多实地测试部署，这一点会更有说服力。

我们想提及的最后一个有利于 CPO 采用的因素是，Nvidia 部分 CPO 交换机 SKU 集成了光纤重排（fiber shuffle），可简化多平面网络架构的安装与维护。回想一下：SN6800 在多平面配置中包含 4 颗 Switch ASIC，经集成光纤重排连接到端口，提供 409.6T 聚合带宽；而 SN6810 使用单颗 Switch ASIC、不带任何集成光纤重排，提供 102.4T 聚合带宽。

但首先，作为重要前言，我们要解释为什么我们认为多平面网络架构将长期存在。

集群规模超过 10 万 GPU 的大规模部署通常采用多平面网络架构，因为在当前交换机世代，单平面架构没有足够的逻辑端口来支撑更大的网络，除非动用 3 层或更多层交换。

回顾上文，用 Q3400-X800 交换机、每 GPU 1.6T 逻辑端口构建的 Vera Rubin NVL72 集群无法突破 93,312 GPU 的最大集群规模。即使未来交换机世代继续把单机箱最大交换容量翻倍，每 GPU 带宽预计也会翻倍，这意味着集群网络中的有效逻辑端口数不太可能改变。

这意味着，大规模 GPU 集群部署将继续需要多平面网络架构。但请注意，多平面网络架构并不受规模限制，我们也见过 NVIDIA 参考架构部署的多平面集群各自规模显著低于 10 万 GPU。

在使用 SN6600 交换机而非 CPO 交换机的多平面网络架构中，每颗 GPU 通过光纤重排扇出到多个交换机箱。这要求客户在交换机箱之外部署重排箱、配线架和笨重的「章鱼线」，给安装与维护带来复杂性。

Nvidia 部分 CPO SKU——如 SN6800 与 Q3450——在交换机箱内集成了这种光纤重排，每个光引擎扇出到不同的逻辑端口。因此，它们能提供比基于单颗 Switch ASIC 的机箱更高的聚合带宽——分别为 409.6T 与 115.2T。

![](https://substack-post-media.s3.amazonaws.com/public/images/41bf7a29-4917-41d8-957a-86cc9773b39c_2897x3821.png)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

对 SN6800 CPO 交换机，尽管负责电信号转光信号的带宽引擎从 1.6T 扩展到 3.2T、相比 SN6600 交换机翻倍，但 SN6800 机箱内的每个 3.2T OE 在箱内本身就被分成四个 800G 逻辑端口扇出，并经光纤连接器从前面板引出。这使单个 1.6T GPU 能够扇出到两个独立交换平面。事实上，SN6800 机箱由 4 颗 ASIC 组成，与 X800-Q3400 机箱类似。

![](https://substack-post-media.s3.amazonaws.com/public/images/21284057-cc2b-423a-836f-cce6283ef615_2916x1102.png)
*来源：SemiAnalysis AI 网络模型*

随着每 GPU 带宽继续向 3.2T 扩展，不难想象用 SN6800 交换机构建 4 平面网络：每颗 3.2T GPU 四路拆分，以每链路 800G 连到 4 个不同的交换机箱。

事实上，如果你还没注意到——前文讲解的 X800-Q3400 交换机（非 CPO）与 CPO 交换机之间存在高度相似性：两者都促成高端口数、多平面的网络架构，同时把复杂布线封装在机箱内，为客户省去线缆管理的麻烦。

在 NVIDIA 生态之外，主要的交换 ASIC 玩家是 Broadcom（将制造 Tomahawk 6 与 Tomahawk 6 CPO ASIC）以及 Cisco（最近发布了 G300 102.4T ASIC）。超大规模厂商后端网络部署有两类：

- 利用全部 512 交换端口数（radix）的 8 平面「扁平」网络；

![](https://substack-post-media.s3.amazonaws.com/public/images/2249c887-6af9-4933-9297-6b698aca46e3_2622x1323.png)
*来源：SemiAnalysis AI 网络模型*

- NIC 侧带 1.6T OSFP 笼座的单平面网络。

  ![](https://substack-post-media.s3.amazonaws.com/public/images/9cc07e85-ea9f-4089-a0a2-4d15b7c5ac8d_2782x1258.png)
  *来源：SemiAnalysis AI 网络模型*

对 Meta，我们认为其 VR NVL72 部署将只由非调度 fabric（NSF）集群组成，在每个数据中心使用基于 Tomahawk 6 的 Minipack-4 OCP Rack 102.4T 交换机构建。Meta 将使用光模块连接集群内的所有交换机，而一旦 1.6T AEC 在市场上广泛供货，NIC 到 TOR 的连接将使用 1.6T AEC。我们预计 1.6T AEC 的放量发生在 2026 日历年下半年。

![](https://substack-post-media.s3.amazonaws.com/public/images/c2c75af2-9d1e-41c6-86de-aede72445f14_1981x1623.png)
*来源：SemiAnalysis AI 网络模型*

问题在于，102.4T Minipack-4 交换机可能赶不上 Vera Rubin NVL72 机柜部署的出货时间，若真如此，部分 NSF 集群将改用 51.2T Minipack-3 交换机出货。这意味着 AEC 内的 gearbox 须把 NIC 侧每 lane 200G 的 SerDes 速率转换为交换机侧每 lane 100G。

不过，Meta 不会是唯一一家在 VR200 部署中使用 1.6T AEC 的超大规模厂商。我们认为 xAI 将在 leaf、spine 与 core 层的 NIC 到 TOR 及交换机间连接中都使用 1.6T AEC。那将是一个取代交换机箱中大部分 1.6T 收发器的单平面网络——这可能给 Credo 可观的定价权。

# 超大规模定制与组装物流

## **定制**

对 GB300，尽管参考设计为后端网络配置了 4 块 ConnectX-8 NIC、前端网络 1 块 Bluefield-3，大多数超大规模厂商有自己的设计与替代网络配置，尤其针对 Bluefield-3。除网络配置外，供电模块、本地 NVMe 存储与管理模块在各客户之间也高度定制、差异化。

例如，在某些机柜中，即使是亚马逊（Amazon），很多场合也在 GB300 中部署 ConnectX-8。而且，大多数超大规模厂商部署自研 DPU 而非 Bluefield-3 承担前端网络。GB300 的供电模块与管理模块同样高度定制，因为每个客户对这些模块的偏好各不相同。因此，GB300 的前半部高度可定制，各家超大规模厂商的设计彼此差异显著。

![](https://substack-post-media.s3.amazonaws.com/public/images/e84cedc7-fe5c-4781-99f8-1bf9cd135df9_2806x2341.png)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

对 VR NVL72，虽然仍有一定程度的定制空间，但形态规格上的限制多得多。鉴于 VR NVL72 的模块化与无缆设计，机箱前部的定制模块必须与 Nvidia 参考设计的形态规格和尺寸相匹配。可供定制的模块是供电、BlueField-4 与管理模块。我们预计大多数超大规模客户会采用自研 DPU 而非 BlueField-4。受形态与尺寸所限，超大规模厂商正在重新设计其自研 DPU 的板卡布局与模块形态，以匹配 BlueField-4。至于供电模块与管理模块，一些客户也在考虑将两者合并。亚马逊确实为 VR NVL72 准备了 JBOK / Nitro Box NIC 版本。

## **组装自动化与物流**

在 CES 2026 上，黄仁勋提到，凭借精简的无缆设计与自动化组装流程，计算托盘组装时间从 Blackwell 到 Rubin 显著缩短，从 2 小时降到 5 分钟。Rubin 平台具备自动化能力的 L10 级计算托盘组装伙伴只有三家——富士康（Foxconn）、广达（Quanta）与纬创（Wistron）。

![](https://substack-post-media.s3.amazonaws.com/public/images/ac6c92de-ef84-4ae2-917b-355a6c1a7930_5189x3373.png)
*来源：Nvidia VR NVL72 组件 BoM 与功率预算模型*

在 L6 板级 PCBA 层面，纬创与富士康是 Blackwell 与 Rubin 的主要供应商。在 L10 层面，Blackwell 曾有众多不同的计算托盘制造商，它们从 Nvidia 购入 Bianca 板再转售给客户。对 Rubin，具备计算托盘自动化能力的供应商只有三家。较小的 ODM 或 OEM，要么把计算托盘交给上述三家自动化供应商制造，要么在自家工厂以非自动化方式完成。尽管效率稍逊，得益于无缝的模块化设计，无自动化的计算托盘组装相比 Blackwell 也会容易得多。然后在 L11 层级，各家 ODM/OEM 把计算托盘组装进机柜。

# VR NVL72 TCO：BoM 与功率预算分析

[VR NVL72 组件 BoM 与功率预算模型](https://semianalysis.com/vr-nvl72-model/)对该机柜系统的 BoM 与功率预算提供了详细分析。

![](https://substack-post-media.s3.amazonaws.com/public/images/7a435ee7-a40f-4df2-a84a-9d37041115d5_3379x755.png)
*来源：VR NVL72 组件 BoM 与功率预算模型*

按每 GPU 资本成本计，VR NVL72 更贵：相比 GB300 高约 45%，相比 MI4XX 高约 14-15%，原因在于每 GPU 服务器成本更高。这导致更高的资本拥有成本（TCO）。例如，按 4 年使用寿命计，超大规模厂商 Arista 网络配置下 VR NVL72 的资本成本为每 GPU 每小时 $3.28，而 MI4XX 超大规模配置为 $2.86。我们的 TCO 模型以 4 年使用寿命计算每小时资本成本，以反映保守的商业情形，但大多数新兴 GPU 云与超大规模厂商会采用 5-6 年折旧期，我们认为最好以该折旧期来观察 EBIT 利润率。我们偏好的标尺是项目 IRR，它不受所选折旧期的影响。

不过，Nvidia 的 VR SOCAMM 选项有一项优势：NVIDIA 直接采购内存，使其能够与内存供应商谈判长期协议、批量优惠条款，以及最重要的 VVIP 定价。我们认为这将使最终客户免受内存成本冲击，详见我们的 [AI 服务器定价启示录报告](https://semianalysis.com/institutional/the-ai-server-pricing-apocalypse/?access_token=eyJhbGciOiJFUzI1NiIsImtpZCI6InNlbWlhbmFseXNpcy5wYXNzcG9ydC5vbmxpbmUiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJzZW1pYW5hbHlzaXMucGFzc3BvcnQub25saW5lIiwiYXpwIjoiS1NncVhBaGFmZmtwVjQzbmt0UU1INSIsImVudCI6eyJ1cmkiOlsiaHR0cHM6Ly9zZW1pYW5hbHlzaXMuY29tL2luc3RpdHV0aW9uYWwvdGhlLWFpLXNlcnZlci1wcmljaW5nLWFwb2NhbHlwc2UvIl19LCJleHAiOjE3NzIyMjcwMTcsImlhdCI6MTc2OTYzNTAxNywiaXNzIjoiaHR0cHM6Ly9zZW1pYW5hbHlzaXMucGFzc3BvcnQub25saW5lL29hdXRoIiwic2NvcGUiOiJmZWVkOnJlYWQgYXJ0aWNsZTpyZWFkIGFzc2V0OnJlYWQgY2F0ZWdvcnk6cmVhZCBlbnRpdGxlbWVudHMiLCJzdWIiOiIwMTk4OTQ2ZC0xNWUwLTc4MGItYWE2My1iNTc2YmQ3YWY2OTIiLCJ1c2UiOiJhY2Nlc3MifQ.2-BzgpJsNkRro7XCzTy3QDFtE-QyqEQxE7kykja0HIN5XHg3O1bvBzRuBc5x1Pz_HfCVhuRT3fA8f1s7GI_CvA)。这也是[作为「AI 央行」的 Nvidia](https://semianalysis.com/institutional/nvidia-as-the-central-bank-of-ai/) 实际上在为全体客户对冲 DRAM 价格的又一例证。

相比之下，AMD 对 DRAM 涨价的敞口大得多，因为其 DRAM 用量约为两倍：每机柜约 55 TB LPDDR5 加每机柜 55 TB DDR5。对 AMD 的 Helios 机柜级系统，AMD 出售 GPU/板卡并确实采购 LPDDR5 内存，但不为机柜计算托盘采购 DDR5 DRAM——机柜组装商/ODM 自行采购并集成 DDR5 内存。这使得 AMD 机柜的买家敞口更大，因为 AMD 只能通过长期合约潜在地「对冲」LPDDR5 部分，DDR5 部分则完全暴露。DRAM 内容翻倍也令整体敞口几乎翻倍。

Helios 的内存成本更可能被组装商转嫁或重新定价，因此在内存上行周期中涨幅更大。因此，下文中我们对 VR 与 GB 建模的内存涨价低于 MI4XX。我们的 MI400 机柜假设反映，AMD 的 LPDDR 定价为 $8.70/GB，而 Nvidia 为 $6.77/GB——相对 $10.63/GB 的市场合约价嵌入了批量折扣结构，但也体现了相对 NVIDIA 的规模经济差距。

我们的 [AI 内存模型](https://semianalysis.com/memory-model/)预计 LPDDR5 与 DDR5 合约价在 2Q26 及以后将大幅上涨，我们预计还将进一步上调服务器资本开支总量的预测。

NVIDIA 的 2300W 配置即 Max-P 配置，而能效优化的 Max-Q 配置运行于 1800W。Nvidia 声称，无论哪种配置都能达到相同的峰值频率，从而实现宣传的 50 PFLOPS FP4 性能。虽然底层硬件相同，但 TCO 上的差异来自不同功耗水平带来的运营成本。

以下（付费墙后）我们将分享服务器、存储、网络等成本的详细数字，以及 Nvidia 打算如何处置 Groq。
