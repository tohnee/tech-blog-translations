---
title: "Tesla AI 产能扩张——H100、Dojo D1、D2、HW 4.0、X.AI、云服务提供商"
title_en: "Tesla AI Capacity Expansion – H100, Dojo D1, D2, HW 4.0, X.AI, Cloud Service Provider"
subtitle: "Tesla 立志成为产能排名前 5 的 AI 公司兼云服务提供商"
date: 2023-06-27
source: https://newsletter.semianalysis.com/p/tesla-ai-capacity-expansion-h100
crawled: 2026-09-15
authors: ["Dylan Patel", "Aleksandar Kostovic"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Tesla AI 产能扩张——H100、Dojo D1、D2、HW 4.0、X.AI、云服务提供商

> 原文：[Tesla AI Capacity Expansion – H100, Dojo D1, D2, HW 4.0, X.AI, Cloud Service Provider](https://newsletter.semianalysis.com/p/tesla-ai-capacity-expansion-h100) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Tesla 立志成为产能排名前 5 的 AI 公司兼云服务提供商**

Tesla 立志成为全球领先的 AI 公司之一。迄今为止，部署了最先进自动驾驶的并不是他们——[这一荣誉属于 Alphabet 旗下的 Waymo](https://thelastdriverlicenseholder.com/2023/02/17/2022-disengagement-report-from-california/)。此外，Tesla 在生成式 AI 领域也毫无踪影。话虽如此，凭借数据采集优势、专用计算、创新文化和顶尖 AI 研究人员，他们或许握有在自动驾驶和机器人领域实现跨越式领先的配方。

Tesla 目前自有的 AI 基础设施很少，只有约 4k 颗 V100 和约 16k 颗 A100。与世界其他大型科技公司相比，这个数字非常小——微软和 Meta 拥有 100k+ 颗 GPU，并计划在中短期内翻倍。Tesla AI 基础设施薄弱，部分原因是其自研 D1 训练芯片的多次延期。

现在，故事正在改变，而且很快。

Tesla 正在 1.5 年内将其 AI 产能扩大 10 倍以上。其中一部分是为了自身能力，但很大一部分也是为了 X.AI。今天我们想深入分析 Tesla 的 AI 产能、H100 与 Dojo 的逐季度爬坡及出货量估计，以及 Tesla 因其模型架构、训练基础设施和边缘推理（包括 HW 4.0）而产生的独特需求。最后，我们想聊聊 X.AI 在做什么——马斯克对标 OpenAI 的公司，已从 OpenAI 挖走了不少知名工程师。

D1 训练芯片的故事漫长而艰辛。从芯片设计到供电都曾出问题，但如今 Tesla 声称它已准备好登台亮相，并已开始量产。稍作回顾：Tesla 自 2016 年左右开始为其汽车设计自研 AI 芯片，2018 年左右开始为数据中心应用设计。我们[曾在该芯片发布前独家披露他们所采用的特殊封装技术](https://www.semianalysis.com/p/tesla-ai-day-supercomputer-chip-teaser)——InFO SoW。简单来说，可以把它想象成一个晶圆大小的扇出封装。原理上与 Cerebras 的做法类似，但优势在于[允许已知良好裸片（known good die）测试](https://www.semianalysis.com/p/advanced-packaging-part-1-pad-limited)。这是 Tesla 架构最独特、最有意思的一点：25 颗芯片被集成在这块 InFO-SoW 中，且没有直接挂载内存。

我们还在 2021 年更详细地讨论过其芯片架构的[优点](https://www.semianalysis.com/p/tesla-dojo-unique-packaging-and-chip)和[缺点](https://www.semianalysis.com/p/the-tesla-dojo-chip-is-impressive)。此后披露的最有趣的一点是：Tesla 不得不另造一颗放在 PCIe 卡上的芯片来提供内存连接，因为片上内存不够用。

Tesla 原定 2022 年多次爬坡，但由于芯片和系统问题始终未能实现。现在已是 2023 年年中，它终于开始量产。这一架构非常适合 Tesla 的独特用例，但值得注意的是，它对严重受内存带宽瓶颈制约的 LLM 并不适用。

Tesla 的用例很独特，因为它必须专注于图像网络。因此，其架构与其他公司大不相同。我们过去讨论过，深度学习推荐网络和基于 Transformer 的语言模型需要截然不同的架构。图像/视频识别网络对算力、片上通信、片上内存和片外内存的需求配比也与众不同。

这些卷积模型在训练时对 GPU 的利用率非常低。随着 Nvidia 下一代产品一头扎进[对 Transformer（尤其是稀疏 MoE）的进一步优化](https://www.semianalysis.com/p/the-ai-brick-wall-a-practical-limit)，Tesla 对自研差异化、面向卷积优化的架构的投资应该会有好回报。这些图像网络必须契合 Tesla 推理基础设施的约束。

[分享](https://newsletter.semianalysis.com/p/tesla-ai-capacity-expansion-h100?utm_source=substack&utm_medium=email&utm_content=share&action=share)

## **Tesla HW 4.0：第二代 FSD 芯片**

训练芯片由台积电制造，而在 Tesla 电动车内运行 AI 推理的芯片则叫做完全自动驾驶（Full Self-Driving，FSD）芯片。Tesla 车载模型受到极大限制，因为 Tesla 固执地认为，实现完全自动驾驶不需要车内有巨大的算力。此外，Tesla 的成本约束比 Waymo 和 Cruise 严格得多，因为他们的车是真金白银地大批量出货。而 Alphabet Waymo 和 GM Cruise 在开发和早期测试阶段用的是成本高 10 倍的全尺寸 GPU，并计划为自家车辆打造快得多（也贵得多）的自研 SoC。

第二代自 2023 年 2 月起随车出货，芯片设计与第一代非常相似。第一代基于三星 14nm 制程，围绕三个四核集群构建，共 12 颗 Arm Cortex-A72 核心，运行频率 2.2 GHz。而在第二代设计中，公司将 CPU 核心数提高到五个 4 核集群（20 核），共 20 颗 Cortex-A72 核心。

第二代 FSD 芯片最重要的部分是三个 NPU 核心。这三个核心各使用 32 MiB 的 SRAM 来存储模型权重和激活值。每个周期，256 字节激活数据和 128 字节权重数据从 SRAM 读入乘累加单元（MAC）。MAC 采用网格设计，每个 NPU 核心拥有 96x96 的网格，共 9,216 个 MAC、每时钟周期 18,432 次运算。每颗芯片三个 NPU、运行频率 2.2 GHz，总算力为 121.651 万亿次运算每秒（TOPS）。

![](https://substack-post-media.s3.amazonaws.com/public/images/66139cf6-86f3-4c62-b959-1a83f8f035fa_859x682.png)

第二代 FSD 配备 256GB 的 NVMe 存储和 16GB 美光 GDDR6（14Gbps），挂在 128-bit 内存总线上，提供 224GB/s 带宽。后者是最值得关注的变化，带宽较上代提升约 3.3 倍。算力增幅超过带宽增幅，说明 HW3 一直难以被充分利用。每套 HW 4.0 有两颗 FSD 芯片。

HW4 板卡性能提升的代价是功耗增加。HW4 板卡的待机功耗约为 HW3 的两倍，我们预计峰值功耗也会更高。HW4 外壳标注 16 伏 10 安，对应 160 瓦功耗。

尽管 HW4 性能提升，Tesla 仍希望让 HW3 也能实现 FSD，很可能是因为他们不想为已购买 FSD 的 HW3 老用户更换硬件。

信息娱乐系统采用 AMD GPU/APU。它与 FSD 芯片现在位于同一块板卡上，而上一代采用的是独立子板。

![](https://substack-post-media.s3.amazonaws.com/public/images/bb8cc3e1-dab6-40a3-a592-1d1a333bbd1f_1500x874.jpeg)

HW4 平台支持 12 个摄像头，其中一个用于冗余，因此实际启用 11 个。旧方案的前摄像头组使用三个较低的 120 万像素摄像头，新平台则使用两个更高的 500 万像素摄像头。

Tesla 目前不使用激光雷达（LIDAR）或其他非摄像头方案。过去他们确实用过雷达，但在产品世代中期被移除。这显著降低了整车制造成本——这正是 Tesla 死死盯住要优化的东西——而且公司认为纯视觉感知是通往自动驾驶的可行路线。不过他们也表示，如果有可用的好雷达，会将其与摄像头系统融合。

HW4 平台上还将有一颗自研雷达，名为 [Phoenix](https://www.youtube.com/watch?v=Nw2GdWrLrTM)。Phoenix 将雷达系统与摄像头系统结合，旨在利用更多数据打造更安全的车辆。Phoenix [雷达使用](https://apps.fcc.gov/oetcf/eas/reports/ViewExhibitReport.cfm?mode=Exhibits&RequestTimeout=500&calledFromFrame=Y&application_id=TAi5l5atHcj4G%2FIFPFuKbA%3D%3D&fcc_id=2AEIM-1541584) 76-77 GHz 频段，峰值等效全向辐射功率（EIPR）为 4.16 瓦，平均 EIRP 为 177.4 mW。它是一套非脉冲汽车雷达系统，具有三种感知模式。雷达 PCB 上有一颗 Xilinx Zynq XA7Z020 FPGA，用于传感器融合。

## **Tesla AI 模型的差异化**

Tesla 的目标是打造为其自主机器人和汽车提供动力的基础 AI 模型。两者都需要感知周围环境并在其中导航，因此同一类 AI 模型可以同时适用于两者。为未来自主平台创建高效模型需要大量研究，更具体地说，需要大量数据。此外，这些模型的推理必须在极低功耗、极低延迟下完成。由于硬件限制，这大大压缩了 Tesla 所能提供的最大模型规模。

在所有公司中，Tesla 拥有训练其深度神经网络的最大数据集。每辆上路的车都用传感器和图像采集数据，乘以路上行驶的 Tesla 电动车数量，就得到一个庞大的数据集。Tesla 把这部分数据采集工作称为「车队规模自动标注」（fleet scale auto labeling）。每辆 Tesla 电动车拍摄一段 clip——45-60 秒的密集传感器数据日志，包括视频、惯性测量单元（IMU）数据、GPS、里程计等——并发送到 Tesla 的训练服务器。

Tesla 的模型在分割、掩码、深度、点匹配等任务上训练。凭借路上数百万辆电动车，Tesla 拥有大量标注和记录都非常完善的数据源。这使其能够在公司设施内的 Dojo 超级计算机上持续训练。

Tesla 对数据的理念与其已建成的基础设施相矛盾。Tesla 只使用了其采集数据的一小部分。由于推理端限制严苛，Tesla 以「过度训练」模型著称——在给定模型尺寸内榨取最高精度。

过度训练小模型会导致完全自动驾驶性能进入平台期，且无法用上采集到的全部数据。许多公司同样选择尽可能大规模地训练，但它们使用的车载推理芯片也强大得多。例如，Nvidia 计划 2025 年向汽车客户交付算力超过 2,000 TeraFLOPS 的 DRIVE Thor，是 Tesla 新 HW4 的 15 倍以上。此外，Nvidia 架构对其他模型类型也更为灵活。

## **生成式 AI、基础设施产能与云服务提供商之梦**
