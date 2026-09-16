---
title: "ISSCC 2026：NVIDIA 与 Broadcom 的 CPO、HBM4 与 LPDDR6、TSMC Active LSI、逻辑工艺 SRAM、UCIe-S 等"
title_en: "ISSCC 2026: NVIDIA & Broadcom CPO, HBM4 & LPDDR6, TSMC Active LSI, Logic-Based SRAM, UCIe-S and More"
subtitle: "ISSCC 2026 综述"
date: 2026-04-15
source: https://newsletter.semianalysis.com/p/isscc-2026-nvidia-and-broadcom-cpo
crawled: 2026-09-15
authors: ["Afzal Ahmad", "Gerald Wong", "Daniel Nishball", "Clara Ee", "DC", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# ISSCC 2026：NVIDIA 与 Broadcom 的 CPO、HBM4 与 LPDDR6、TSMC Active LSI、逻辑工艺 SRAM、UCIe-S 等

> 原文：[ISSCC 2026: NVIDIA & Broadcom CPO, HBM4 & LPDDR6, TSMC Active LSI, Logic-Based SRAM, UCIe-S and More](https://newsletter.semianalysis.com/p/isscc-2026-nvidia-and-broadcom-cpo) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**ISSCC 2026 综述**

每年有三大半导体会议：[IEDM](https://newsletter.semianalysis.com/p/interconnects-beyond-copper-1000)、[VLSI](https://newsletter.semianalysis.com/p/vlsi2025)，以及压轴的 ISSCC。过去几年里，我们已经非常详尽地报道了前两者。今天，我们终于以 ISSCC 2026 综述补全这三部曲。

与 IEDM 和 VLSI 相比，ISSCC 对集成与电路的侧重要大得多。几乎每篇论文都配有某种形式的电路图，以及清晰的测量结果与数据。

在过去几年里，ISSCC 的成果对产业的影响时好时坏。今年不同以往：相当多的论文和报告与市场趋势直接相关。议题涵盖 HBM4、LPDDR6、GDDR7 和 NAND 的最新进展，直至共封装光学（CPO）、先进裸片间接口，以及 MediaTek、AMD、Nvidia、Microsoft 等公司的先进处理器。

在本篇综述中，我们将覆盖存储器、光网络、高速电互连、处理器等主要类别。

# 存储器

今年 ISSCC 上最吸引我们注意的关键主题之一是存储器，包括三星（Samsung）HBM4、三星与 SK Hynix 的 LPDDR6，以及 SK Hynix GDDR7。除了 DRAM 之外，基于逻辑工艺的 SRAM 和 MRAM 也引起了我们的兴趣。

## Samsung HBM4 —— 论文 15.6

在三大存储器厂商中，只有三星发表了 HBM4 技术论文。在 ISSCC 之前，我们曾在[加速器与 HBM 模型](https://semianalysis.com/institutional/hbm4-samsung-incremental-progress-micron-execution-risk-rising-hbm3e-pricing-revised-up/)中指出，三星的 HBM4 世代相较其 HBM3E 取得了长足进步。ISSCC 上公布的数据印证了我们的分析——三星交出了同类最佳的性能，这一进展我们数月前也已在[模型更新笔记](https://semianalysis.com/institutional/samsung-hbm4-performance-leadership-sk-hynix-hbm4-issues/)中详细阐述过。

ISSCC 上展示的技术细节，结合我们收集到的业界传闻，清楚地表明三星的 HBM4 已具备与同行竞争的实力。值得注意的是，它能在低于 1V 的电压下满足 Rubin 所需的引脚速率。尽管在可靠性与稳定性方面三星仍落后于 SK Hynix，但该公司在技术层面缩小差距上已取得实质性进展，有望挑战 SK Hynix 在 HBM 领域的主导地位。其基于 1c 的 HBM4 搭配 SF4 逻辑基础裸片，似乎能在引脚速率上带来更强的性能。

![](https://substack-post-media.s3.amazonaws.com/public/images/515a99f4-5397-4b1a-9f95-d9a3dff37521_2880x1620.jpeg)
*三星 HBM3E 与 HBM4 规格对比。来源：Samsung，ISSCC 2026*
![](https://substack-post-media.s3.amazonaws.com/public/images/773189fd-1dd5-434a-aa0c-694db785b9c9_2880x1620.jpeg)
*三星 HBM4 裸片图与剖面。来源：Samsung，ISSCC 2026*

三星展示了一个 36 GB、12 层堆叠的 HBM4 栈，拥有 2048 个 IO 引脚和 3.3 TB/s 的带宽，采用第六代 10nm 级（1c）DRAM 核心裸片搭配 SF4 逻辑基础裸片制造。

从 HBM3E 到 HBM4，最显著的架构变化是核心 DRAM 裸片与基础裸片在工艺上的分离。HBM4 只在核心裸片上使用 DRAM 制程节点，而基础裸片采用先进逻辑节点制造，不同于此前历代 HBM 两者使用同一工艺的做法。

随着 AI 工作负载对 HBM 提出更高带宽和更快数据速率的要求，关键的架构挑战随之而来。通过将基础裸片转移到 SF4 逻辑工艺，三星实现了更高的工作速率和更低的功耗。工作电压（VDDQ）下降了 32%，从 HBM3E 的 1.1V 降至 HBM4 的 0.75V。与在 DRAM 工艺上制造的基础裸片相比，逻辑工艺基础裸片凭借更小的晶体管和更丰富的金属层堆叠，提供更高的晶体管密度、更小的器件尺寸和更好的面积效率。这帮助三星的 HBM4 达到——并大幅超越——JEDEC 的 HBM4 标准，我们将在本节末尾详细解释该标准。

![](https://substack-post-media.s3.amazonaws.com/public/images/f3e96393-ade6-49e3-82fa-8127beff5ad4_2880x1620.jpeg)
*三星 HBM4 自适应体偏置控制与工艺偏差。来源：Samsung，ISSCC 2026*

结合可缓解堆叠核心裸片间工艺偏差的自适应体偏置（ABB）控制，翻倍的 TSV 数量进一步改善了时序裕量。综合来看，三星论文声称，ABB 加上 4 倍的 TSV 数量使其 HBM4 能够实现高达每引脚 13 Gb/s 的工作速率。

SF4 基础裸片与 1c DRAM 核心裸片带来的提升是有代价的。即便三星代工（Samsung Foundry）可以为内部基础裸片用量提供折扣，**三星为逻辑基础裸片选择 SF4 依然成本更高**。SK Hynix 的 HBM4 基础裸片采用 **TSMC 的 N12 逻辑工艺**，而美光（Micron）则依赖其**内部 CMOS 基础裸片技术**，即使考虑垂直整合的成本优势，这两者都是比接近先进制程的 SF4 节点成本更低的选项。

1c 前端制造工艺在整个 2025 年对三星而言都颇具挑战，尤其考虑到该公司跳过了 1b 节点，直接从基于 1a 的 HBM3E 跨入 1c 世代。去年 1c 节点的前端良率只有 50% 左右，尽管此后在逐步改善。较低的良率对其 HBM4 毛利率构成风险。

历史上，三星 HBM 的毛利率一直低于其最大竞争对手 SK Hynix，我们在[存储器模型](https://semianalysis.com/memory-model/)中对各厂商的这一动态进行了全面建模。我们详细覆盖了各厂商 HBM、DDR、LPDDR 在多个节点上的晶圆投片量、良率、密度、销售成本（COGS）等数据。

三星的策略似乎是激进地为基础裸片采用更先进的节点，以实现更优的性能并超越竞争对手，尤其是在 NVIDIA 等头部客户对 HBM 的要求持续提高之际。

HBM 需要解决的另一个关键问题是 tCCDR，即跨不同堆叠 ID（SID）发出的连续 READ 命令之间所需的最小间隔。对于严重依赖多通道并行内存访问的 AI 工作负载而言，tCCDR 直接影响可实现的内存吞吐量。

在堆叠式 DRAM 架构中，多颗核心裸片纵向集成在基础裸片之上。这天然会在整个堆叠中引入微小的延迟差异，其成因包括核心裸片与基础裸片之间的工艺偏差、TSV 传播差异以及局部通道偏差。

堆叠层数与通道数从 16 增加到 32，进一步加剧了这一挑战。随着通道数和堆叠高度增加，裸片之间的偏差不断累积，导致通道间和裸片间更大的时序失配，进而影响可实现的 tCCDR 和整体 HBM 性能。

![](https://substack-post-media.s3.amazonaws.com/public/images/e56f1735-adbc-4038-8473-b27f5ae002fb_1611x1352.jpeg)
*三星 HBM4 每通道 TSV RDQS 自动校准方案。来源：Samsung，ISSCC 2026*

为解决这一问题，三星引入了「每通道 TSV RDQS 时序自动校准方案」。上电后，系统利用一条镜像真实信号路径时序行为的复制 RDQS 路径来测量各通道间的延迟偏差。时间数字转换器（TDC）对这些时序差异进行量化，再由各通道的延迟补偿电路（DCDL）进行补偿。

这一校准同时考虑了堆叠核心裸片之间的全局延迟偏差和每通道的局部偏差，使整个堆叠的时序对齐。通过补偿这些失配，三星显著改善了有效时序裕量，并在满足所需 tCCDR 约束的同时提高了最大可实现数据速率。仅这一方案就将数据速率从 7.8 Gb/s 提升到 9.4 Gb/s。

一些精通存储器技术的读者可能会问：哪来足够的裸片面积容纳 TSV 数量的大幅增加？这正是 1c 节点的重要之处。与前一代 1a 节点相比，1c 进一步缩小了 DRAM 单元面积，释放出的裸片空间可用于集成 HBM4 所需的更多 TSV。

![](https://substack-post-media.s3.amazonaws.com/public/images/35b20c2b-2f00-4d4c-b05a-578d695a51c1_2880x1620.jpeg)
*三星 HBM4 PMBIST 测试图案操作。来源：Samsung，ISSCC 2026*
![](https://substack-post-media.s3.amazonaws.com/public/images/ec777954-f7fa-44fb-a8b3-f295d57f3e59_2880x1620.jpeg)
*三星 HBM4 PMBIST 与 HBM3E MBIST 对比。来源：Samsung，ISSCC 2026*

逻辑基础裸片带来的另一项关键创新是三星的可编程内存内建自测试（PMBIST）架构。PMBIST 允许基础裸片生成完全可编程的内存测试图案，同时支持完整的 JEDEC 行列命令集，这意味着测试引擎可以发出与真实系统相同的命令，并且可以在任意时钟沿、以全接口速率执行。实际上，这让工程师能够复制复杂的真实世界内存访问图案，并在真实工作条件下对 HBM 接口施加压力，而传统的固定图案测试引擎很难做到这一点。

这一方法与 HBM3E 相比是显著的转变。如前所述，HBM3E 基础裸片采用 DRAM 工艺制造，这给 MBIST（内存内建自测试）引擎带来了严格的功耗和面积约束，鉴于 DRAM 相对逻辑的天然功耗与面积劣势，测试被限制在少量预定义图案内。通过将基础裸片转移到三星代工的 SF4 逻辑工艺，三星实现了能够运行复杂测试算法和灵活访问序列的完全可编程测试框架。

这为 HBM 带来了强大得多的调试能力和更好的良率爬坡学习。工程师可以创建针对性的压力图案来验证 tCCDR 和 tCCDS 等关键时序参数，在制造早期识别角落案例失效，并加速晶圆上芯片（CoW）和系统级封装（SiP）测试期间的表征。简而言之，随着 HBM 堆叠变得更复杂、速率更高，PMBIST 改善了测试覆盖率、调试效率，并最终提高量产良率。

![](https://substack-post-media.s3.amazonaws.com/public/images/8a03c69a-dc9b-4dfb-a6d2-ad4315760852_2880x1620.jpeg)
*三星 HBM4 Shmoo 图。来源：Samsung，ISSCC 2026*

三星还展示了强劲的引脚速率结果——其 HBM4 能在低于 1V 的核心电压（VDDC）下达到 11 Gb/s，在更高电压下可达 13 Gb/s。我们尚未看到三星的同行展示出可比的性能，尽管后者确实拥有更好的可靠性与稳定性。

三星的实现大幅超出了 JEDEC 官方 HBM4 标准（JESD270-4）的基线规格，该标准规定的最大数据速率为每引脚 6.4 Gb/s、带宽约 2 TB/s。三星展示了超过 JEDEC 标准引脚速率 2 倍以上的成绩，达到每引脚 13 Gb/s、带宽 3.3 TB/s。即使在 VDDC/VDDQ 为 1.05V 和 0.75V 时，该器件也能维持 11.8 Gb/s 的数据速率。

## Samsung LPDDR6 —— 论文 15.8

三星和 SK Hynix 都展示了各自的 LPDDR6 芯片。我们先讨论三星的芯片，稍后再谈 SK Hynix 的。

![](https://substack-post-media.s3.amazonaws.com/public/images/b15266c9-bc1e-4365-9316-28d2a6e36fac_2880x1620.jpeg)
*LPDDR5X 与 LPDDR6 对比。来源：Samsung，ISSCC 2026*

三星介绍了他们的 LPDDR6 架构，并详细说明了所采用的节能技术。

![](https://substack-post-media.s3.amazonaws.com/public/images/0098a613-71de-4d6c-b446-2a203e66fef7_2880x1620.jpeg)
*LPDDR6 子通道与 Bank 结构。来源：Samsung，ISSCC 2026*

LPDDR6 采用每裸片 2 个子通道的架构，每个子通道 16 个 bank。它还有两种模式：正常模式和效率模式。在效率模式下，次级子通道断电，由主子通道控制全部 32 个 bank。但访问次级子通道中的数据会有延迟损失。

双子通道架构也意味着命令解码器、串行化和控制等外围电路数量翻倍。从三星和 SK Hynix 提供的裸片图来看，这一代价约占裸片总面积的 5%，导致每片晶圆的总位元数下降。

![](https://substack-post-media.s3.amazonaws.com/public/images/68f2f392-7912-4f69-9c53-ef6c4f6942b6_2880x1620.jpeg)
*LPDDR6 信令选项。来源：Samsung，ISSCC 2026*

与使用 PAM3 信令的 GDDR7 不同，LPDDR6 将继续使用 NRZ。但它并非标准 NRZ，否则眼图将没有足够的裕量。它使用宽 NRZ（wide NRZ），每个子通道 12 个数据（DQ）引脚，每次操作突发长度为 24。

![](https://substack-post-media.s3.amazonaws.com/public/images/1737c518-8a4f-4042-a536-513a9f769cb8_2880x1620.jpeg)
*LPDDR6 每突发的元数据与 DBI 位分配。来源：Samsung，ISSCC 2026*

有心算的读者会发现，12×24 是 288，并非 2 的幂。其余 32 位分为两种用途：16 位用于 ECC 等元数据，16 位用于数据总线反转（DBI）。

DBI 是一种节能与信号完整性机制。在发送一个突发之前，控制器检查与前一个突发相比是否有超过一半的位会翻转状态。如果是，控制器将所有位反转并置位 DBI 标志，接收端据此知道要再次反转以获得实际数据。这将同时翻转的输出数量限制为总线宽度的一半，降低了功耗和电源噪声。

计算有效带宽时必须计入这些元数据和 DBI 位，公式如下：带宽 = 数据速率 × 位宽（24 b）× 数据（32 b）/ 数据包（36 b）。
在 12.8 Gb/s 下为 34.1 GB/s，在 14.4 Gb/s 下为 38.4 GB/s。

![](https://substack-post-media.s3.amazonaws.com/public/images/986010c2-7d39-4d5f-b195-76d6c653c5ea_2880x1620.jpeg)
*三星 LPDDR6 高频电源域优化。来源：Samsung，ISSCC 2026*

LPDDR6 有两个常供电域：0.875V 的 VDD2C 和 1.0V 的 VDD2D。通过精心选择哪些外围逻辑使用哪个电源域，读取功耗降低了 27%，写入功耗降低了 22%。

![](https://substack-post-media.s3.amazonaws.com/public/images/8741b331-6528-4e4f-a064-722f271f43a0_2880x1620.jpeg)
*三星 LPDDR6 低数据速率下的 I/O 电源切换。来源：Samsung，ISSCC 2026*
![](https://substack-post-media.s3.amazonaws.com/public/images/06109578-4db8-490e-b963-1968a2ebacb0_2880x1620.jpeg)
*三星 LPDDR6 额外的低功耗 DQ/CA 路径。来源：Samsung，ISSCC 2026*

LPDDR 在空闲时主要以 3.2 Gb/s 及以下的低数据速率使用。三星着重于通过谨慎使用电压域在这些较低数据速率下省电，同时降低了待机和读写功耗。

![](https://substack-post-media.s3.amazonaws.com/public/images/931c917e-8cf5-4e59-9b07-45faa91aeee0_2880x1620.jpeg)
*LPDDR6 RDL 时序与版图优势。来源：Samsung，ISSCC 2026*

通过使用重布线层（RDL），三星可以把相关电路在物理上布置得更近。这缩短了关键延迟路径，并降低了对电压和温度变化的敏感度。在 LPDDR6 的高频率下，更紧的时序和更小的偏差至关重要。

![](https://substack-post-media.s3.amazonaws.com/public/images/295c4906-10e2-4877-909b-d7c76e61a6f4_2880x1620.jpeg)
*三星 LPDDR6 规格与裸片图。来源：Samsung，ISSCC 2026*
![](https://substack-post-media.s3.amazonaws.com/public/images/6c037b47-34b6-41db-b615-2e62e41bba05_2880x1620.jpeg)
*三星 LPDDR6 Shmoo 图。来源：Samsung，ISSCC 2026*

三星的 LPDDR6 可在 0.97V 下达到 12.8 Gb/s 的数据速率，在 1.025V 下最高可达 14.4 Gb/s。每颗 16 Gb 裸片面积为 44.5 mm²，在未知的 10nm 级工艺上密度为 0.360 Gb/mm²。这明显低于 1b 工艺 LPDDR5X 的 0.447 Gb/mm²，仅略高于 1a 工艺 LPDDR5X 的 0.341 Gb/mm²。虽然双子通道架构的面积代价是部分原因，但 LPDDR6 似乎还存在其他问题。所述的内存密度让我们认为这颗 LPDDR6 原型芯片是在其 1b 工艺上制造的。

## Samsung SF2 LPDDR6 PHY —— 论文 37.3

![](https://substack-post-media.s3.amazonaws.com/public/images/46165883-4137-4a8e-8fbd-76ee3b9dafd5_2880x1620.jpeg)
*三星 LPDDR6 PHY 测试芯片规格与裸片图。来源：Samsung，ISSCC 2026*

三星还公布了逻辑裸片上与 LPDDR6 接口的 PHY。这些 PHY 采用其新的 SF2 工艺制造，支持高达 14.4 Gb/s。PHY 占用 2.32 mm 的芯片边缘长度（shoreline）和 0.695 mm² 的面积，带宽密度分别为 16.6 Gb/s/mm 和 55.3 Gb/s/mm²。

![](https://substack-post-media.s3.amazonaws.com/public/images/fa36890f-e205-4a23-8281-71bf8c199448_2880x1620.jpeg)
*三星 LPDDR6 PHY 效率模式功耗降低。来源：Samsung，ISSCC 2026*

这些 PHY 同样支持 LPDDR6 芯片实现的效率模式，可将读取功耗降低 39%、写入功耗降低 29%。

PHY 还可以通过对未激活的次级子通道门控高速时钟路径来增强效率模式。加入时钟门控后，读写功耗降低接近 50%，空闲功耗降低 41%。

## SK Hynix 1c LPDDR6 —— 论文 15.7

![](https://substack-post-media.s3.amazonaws.com/public/images/4c8da198-d711-4b0a-8fcd-0d7fce1aa327_2880x1620.jpeg)
*SK Hynix LPDDR6 规格与裸片图。来源：SK Hynix，ISSCC 2026*

SK Hynix 公布了其首批 1c DRAM 产品，同时推出 LPDDR6 和 GDDR7 封装版本。其 LPDDR6 的数据速率最高可达 14.4 Gb/s，比最快的 LPDDR5X 快 35%，且功耗更低。

虽然 SK Hynix 未公布 LPDDR6 芯片的面积或密度，但基于其 GDDR7 密度的相对增幅，我们估计其位元密度将达到 0.59 Gb/mm²。

![](https://substack-post-media.s3.amazonaws.com/public/images/d451b064-d3c9-43a0-b92b-e26efd5df094_2880x1620.jpeg)
*SK Hynix LPDDR6 Shmoo 图。来源：SK Hynix，ISSCC 2026*

在 shmoo 图中，SK Hynix 展示了在 1.025V 下达到 14.4 Gb/s 的数据速率，与三星相同。但在 0.95V 下只能达到 10.9 Gb/s，而三星在 0.97V 下即可达到 12.8 Gb/s。这表明在较低引脚速率下，SK Hynix 的能效可能不如三星，需要以更高电压运行来维持可靠性。

![](https://substack-post-media.s3.amazonaws.com/public/images/9c3722fa-72c1-4ad3-9df8-2910380ab1d2_2880x1620.jpeg)
*SK Hynix LPDDR6 效率模式架构。来源：SK Hynix，ISSCC 2026*
![](https://substack-post-media.s3.amazonaws.com/public/images/001bcb01-81d3-42d2-b0a2-832688185377_2880x1620.jpeg)
*SK Hynix LPDDR6 效率模式节能。来源：SK Hynix，ISSCC 2026*

与三星的 LPDDR6 一样，SK Hynix 的 LPDDR6 也有正常模式和效率模式两种。效率模式在单个子通道上以 12.8 Gb/s 运行，待机电流和工作电流分别比正常模式低 12.7% 和 18.9%。

## SK Hynix 1c GDDR7 —— 论文 15.9

![](https://substack-post-media.s3.amazonaws.com/public/images/75df5c4b-d65e-4d6e-ad17-46db43d1c124_2880x1620.jpeg)
*SK Hynix 1c GDDR7 规格与裸片图。来源：SK Hynix，ISSCC 2026*

如果说 LPDDR6 是采用全新内存技术的世代跨越，那么 SK Hynix 1c 工艺上的 GDDR7 进步更为显著：在 1.2V/1.2V 下速率高达 48 Gb/s。即使仅在 1.05V/0.9V 下，它也能达到 30.3 Gb/s，高于 RTX 5080 中 30 Gb/s 的显存。

![](https://substack-post-media.s3.amazonaws.com/public/images/b54fd8fd-325c-495b-bd98-4187c051138b_2880x1620.jpeg)
*三星 1z GDDR7 Shmoo 图与裸片图。来源：Samsung，ISSCC 2024*
![](https://substack-post-media.s3.amazonaws.com/public/images/5fcf00cd-4001-4a32-8220-0846b9baa526_2880x1620.jpeg)
*三星 1b GDDR7 规格与裸片图。来源：Samsung，ISSCC 2025*

其实现的位元密度为 0.412 Gb/mm²，相比之下三星 1b 工艺为 0.309 Gb/mm²，更老的三星 1z 工艺为 0.192 Gb/mm²。

![](https://substack-post-media.s3.amazonaws.com/public/images/a8119950-b6d0-424a-af28-90305882aae1_1731x703.png)
*各厂商 LPDDR5X 与 GDDR7 密度对比。来源：SemiAnalysis*

GDDR7 的位元密度低于 LPDDR5X，通常约为后者的 70%。虽然其数据速率高得多，但这是有代价的，体现在功耗和面积两方面。

GDDR7 密度较低的原因在于，为实现高访问速度，外围电路面积显著增大，实际的存储阵列因此只占裸片面积中更小的比例。GDDR7 所用的 PAM3 和 QDR（每时钟周期 4 个符号）信令需要这更复杂的逻辑控制电路。

GDDR7 主要用于游戏 GPU 应用，这类应用相比 HBM 需要以更低的成本和容量获得高内存带宽。NVIDIA 曾于 2025 年发布搭载 128GB GDDR7 的 Rubin CPX 大上下文 AI 处理器，但随着 NVIDIA 转而专注于推出其 Groq LPX 解决方案，它已基本从 2026 年路线图中消失。

我们在[存储器模型中详细覆盖了各厂商 HBM、DDR、LPDDR 在多个节点的晶圆投片量、良率、密度、COGS 等数据](https://semianalysis.com/memory-model/)。

## Samsung 4F² COP DRAM —— 论文 15.10

我们已大量报道过 DRAM 持续微缩所面临的挑战。

在 [VLSI 2025 上，SK Hynix 详述了其自研的 4F² 外围电路置于单元下方（PUC）DRAM](https://newsletter.semianalysis.com/i/174558662/dram-4f2-and-3d)。而在 ISSCC 上，三星披露了其自研的 4F² 单元置于外围之上（COP）DRAM 实现。PUC 与 COP 是同一架构的不同名称。

![](https://substack-post-media.s3.amazonaws.com/public/images/1d73da51-6e13-4c3f-a013-11188a56fcaf_2880x1620.jpeg)
*4F² VCT DRAM 单元架构。来源：Samsung，ISSCC 2026*

其 4F² 单元架构与 SK Hynix 的相同，采用垂直沟道晶体管（VCT），电容器位于漏极之上。

![](https://substack-post-media.s3.amazonaws.com/public/images/b889dd90-99fa-42d6-acc7-c8198d858390_2880x1620.jpeg)
*单元置于外围之上（COP）DRAM 堆叠架构。来源：Samsung，ISSCC 2026*

三星展示的垂直架构与 SK Hynix 所用的基本相同：将单元晶圆混合键合在外围晶圆之上。采用这种架构，单元晶圆可以使用 DRAM 节点，而外围电路则可以使用更先进的逻辑节点。

![](https://substack-post-media.s3.amazonaws.com/public/images/f2c22653-7ddd-4eb8-87da-131a04a44314_2880x1620.jpeg)
*DRAM 与 NAND 的 COP 架构对比。来源：Samsung，ISSCC 2026*

三星指出，用于 COP 的混合键合已在 NAND 中得到使用。这对其他 NAND 厂商而言确实如此，但三星尚未将 NAND 混合键合投入大批量生产，距此仍有数年之遥。

此外，DRAM 所需的晶圆间互连数量比 NAND 高出一个数量级，且要求紧密得多的间距。为减少晶圆间互连数量，三星采用了两种新颖的方法。

![](https://substack-post-media.s3.amazonaws.com/public/images/058cc85d-e7c7-4d2c-bafe-43cdc55f9607_2880x1620.jpeg)
*COP NOR 型子字线驱动器优化。来源：Samsung，ISSCC 2026*
![](https://substack-post-media.s3.amazonaws.com/public/images/148125f3-7781-496c-9df5-f4ef6dd56b70_2880x1620.jpeg)
*COP 奇偶列选择 MUX 优化。来源：Samsung，ISSCC 2026*

第一，他们将子字线驱动器（SWD）从每个单元区块 128 个重组为 16 组、每组 8 个。这将 SWD 所需的信号数量减少了 75%。

第二，他们将列选择拆分为奇数和偶数两条路径。这需要两倍的复用器（MUX），但列选择线（CSL）数量减半，每个数据引脚 32 条。

![](https://substack-post-media.s3.amazonaws.com/public/images/76c17f7b-d3ae-4595-bee1-b49403715d62_2880x1620.jpeg)
*COP 单元阵列下方的核心电路版图。来源：Samsung，ISSCC 2026*

借助混合键合，核心电路，即位线灵敏放大器（BLSA）和 SWD，可以布置在单元阵列下方。目标是让核心电路占据与单元阵列相同的面积，以提高整体密度。

![](https://substack-post-media.s3.amazonaws.com/public/images/e3f4b60f-a3f5-4985-a5f6-d3a804ae9a69_2880x1620.jpeg)
*COP 核心电路版图选项。来源：Samsung，ISSCC 2026*

三星采用了「三明治」结构，使其能够最大化核心电路的面积效率，并缩减不处于任何单元下方的边缘区域面积。

![](https://substack-post-media.s3.amazonaws.com/public/images/b1824aa4-f1c3-4174-94c7-320067ca2401_2880x1620.jpeg)
*COP 三明治结构面积效率。来源：Samsung，ISSCC 2026*

核心电路所占面积从 17.0% 降至仅 2.7%，改善显著，直接转化为整体裸片面积的缩减。

在传统 DRAM 中，增加每条位线上的单元数量会导致芯片面积显著增加；而对 VCT DRAM 而言，由于核心电路全部位于单元下方，这一增加几乎可以忽略不计。

![](https://substack-post-media.s3.amazonaws.com/public/images/3bfef447-2020-4611-af35-496a0f7926c9_2880x1620.jpeg)
*三星 4F² COP DRAM 总结与裸片图。来源：Samsung，ISSCC 2026*

三星没有提供这颗芯片的密度数据，只说明这是一颗 10nm DRAM 工艺上的 16 Gb 芯片。

三星指出，VCT DRAM 存在浮体效应，会增大漏电并缩短数据保持时间。缓解这一效应仍是 4F² 落地的关键挑战。

尽管存在这些挑战，我们仍然预计 4F² 混合键合 DRAM 将在本十年后半段到来，最早在 1d 之后的世代。我们的[存储器模型详细跟踪了各节点的时间点与爬坡节奏](https://semianalysis.com/memory-model/)。当前的内存定价环境在很大程度上激励厂商加快更高位元密度新节点的导入与爬坡，以提高每座工厂的位元产出。另一方面，在许多应用场景中，内存的性能/美元比受到的追捧程度远超单纯容量。

## SanDisk/Kioxia BiCS10 NAND —— 论文 15.1

SanDisk 与 Kioxia（铠侠）展示了他们的 BiCS10 NAND，拥有 332 层、3 个 deck。这是已公开报道中最高的 NAND 位元密度，达 37.6 Gb/mm²，将此前的冠军——[SK Hynix 的 321 层 V9](https://newsletter.semianalysis.com/i/184077729/3d-nand-hynix-321-layer)——拉下王座。

![](https://substack-post-media.s3.amazonaws.com/public/images/9f240c14-4a4f-4fab-bc19-194185a47c6b_2880x1620.jpeg)
*BiCS10 裸片图及与 SK Hynix、三星 V9 的密度对比。来源：SanDisk/Kioxia，ISSCC 2026*

尽管采用了相近的架构——6 平面、3 个 deck、相近的层数——SK Hynix 却落后了，位元密度低 30%。在 QLC 配置下，BiCS10 的位元密度为 37.6 Gb/mm²，而 SK Hynix 的 V9 仅为 28.8 Gb/mm²。在 TLC 配置下，两者密度分别为 29 和 21 Gb/mm²，又一次体现了 SK Hynix 的落后地位。

![](https://substack-post-media.s3.amazonaws.com/public/images/6701cf01-e5c3-4aeb-87e6-ab7e99222f7d_2880x1620.jpeg)
*NAND 1×6 与 2×3 平面配置对比。来源：SanDisk/Kioxia，ISSCC 2026*

此外，BiCS10 采用 6 平面配置，将 IO 带宽提高了 50%。实现 6 平面配置有两种方式：1×6 和 2×3。SK Hynix 选择使用 2×3 配置，而 SanDisk 和 Kioxia 决定采用 1×6 配置。

1×6 配置的地焊盘更少，面积缩减 2.1%。但地焊盘和垂直供电轨道数量的减少会约束供电分布。

![](https://substack-post-media.s3.amazonaws.com/public/images/e1c58eb6-654f-4ec5-9d5b-14d27c7f3679_2880x1620.jpeg)
*BiCS10 CBA 用于供电分布的额外顶层金属。来源：SanDisk/Kioxia，ISSCC 2026*

借助 CBA（Cell Bonded Array）架构，SanDisk 和 Kioxia 可以定制 CMOS 晶圆工艺。通过在现有顶层金属之外并行再增加一层顶层金属，他们构建了更强的供电网络，克服了供电分布的约束。

![](https://substack-post-media.s3.amazonaws.com/public/images/3c965c54-2786-4298-bdfc-f916f5133490_2880x1620.jpeg)
*多裸片 NAND 空闲功耗代价与裸片门控方案。来源：SanDisk/Kioxia，ISSCC 2026*

堆叠更多裸片对提高存储密度至关重要。然而在多裸片架构中，未被选中裸片的空闲电流正在逼近被选中裸片的工作电流。SanDisk 实现了一套门控系统，可完全关断未选中裸片的数据路径，将空闲电流降低了两个数量级。

## MediaTek xBIT 逻辑工艺位单元 —— 论文 15.2

![](https://substack-post-media.s3.amazonaws.com/public/images/a42110ab-a204-4a5f-8977-830bd38e06ea_1283x461.jpeg)
*各节点 SRAM HC 位单元密度与逻辑工艺 MBFF 对比。来源：MediaTek，ISSCC 2026*
![](https://substack-post-media.s3.amazonaws.com/public/images/da693b39-6780-47ce-ac48-bf8a5b5a489f_2880x1620.jpeg)
*SRAM 位单元微缩的局限：面积与电压约束。来源：MediaTek，ISSCC 2026*

[SRAM 微缩已死。](https://newsletter.semianalysis.com/i/174558465/sram-scaling-beating-a-dead-horse)尽管从 N5 到 N2 逻辑面积缩减了 40%，8 晶体管高电流 SRAM 位单元的面积仅缩减了 18%。6 晶体管高电流（6T-HC）位单元更糟，只缩减了 2%。辅助电路缩减得更多，但这不是免费的午餐。

众所周知，[N3E 的高密度位单元相对 N3B 是一次倒退，密度回落到 N5 的水平](https://newsletter.semianalysis.com/i/175660907/n3-technology-nodes)。在这篇论文中，MediaTek 透露了一些高电流位单元的情况。N3E 的高电流位单元面积比 N5 增加了 1-2%，密度从约 39.0 Mib/mm² 降至约 38.5 Mib/mm²。请注意，这些数字未计入辅助电路的开销。

![](https://substack-post-media.s3.amazonaws.com/public/images/e8879827-c259-4dfd-a9ae-79a59dbfc37d_2880x1620.jpeg)
*逻辑规则下 8T 位单元 NMOS/PMOS 版图挑战。来源：MediaTek，ISSCC 2026*
![](https://substack-post-media.s3.amazonaws.com/public/images/d4abf3fe-77e4-4333-a1c8-da1eeedb5789_2520x1408.jpeg)
*MediaTek 10T xBIT 平衡位单元电路设计。来源：MediaTek，ISSCC 2026*

在现代逻辑节点中，6T 位单元有 4 个 NMOS 和 2 个 PMOS 晶体管，而 8T 位单元分别有 6 个和 2 个。NMOS 与 PMOS 晶体管数量不等需要专门的规则，并使版图效率降低。MediaTek 的新颖位单元是一个 10 晶体管单元，命名为 xBIT，包含 4 个 NMOS 和 6 个 PMOS 晶体管（或反之）。两种变体位单元可以拼合在一起组成一个包含 20 个晶体管的矩形区块，存储 2 位。

![](https://substack-post-media.s3.amazonaws.com/public/images/a550e975-e262-4350-8c6f-380c90b3ae01_2520x1408.jpeg)
*xBIT 与代工厂 8T 密度和功耗对比。来源：MediaTek，ISSCC 2026*

与 PDK 的标准 8T 位单元相比，xBIT 实现了 22% 到 63% 的更高密度，在字线宽度较小时收益最大。功耗也大幅改善，平均读写功耗降低超过 30%，0.5V 下漏电降低 29%。在 0.9V 下性能与 8T 位单元相当；在 0.5V 下虽然比 8T 位单元慢 16%，但足以快到不会成为处理器的瓶颈，且电压范围足够大，可用于电压-频率调节。

![](https://substack-post-media.s3.amazonaws.com/public/images/6f2a3a1a-a796-4979-8477-fab6bf41c58d_1699x1094.jpeg)
*xBIT Shmoo 图。来源：MediaTek，ISSCC 2026*

MediaTek 还展示了 xBIT 单元的 shmoo 图，从 0.35V 下的 100 MHz 到 0.95V 下的 4GHz。

我们将在即将发布的一篇新闻通讯文章中对 SRAM 及其微缩因子做深度解析。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

## TSMC N16 MRAM —— 论文 15.4

台积电（TSMC）展示了其 N16 节点上更新的 STT-MRAM，基于其 ISSCC 2023 的先前工作。台积电将 MRAM 定位为嵌入式非易失性存储器（eNVM），面向汽车、工业和边缘应用，这些应用不需要最先进的技术，而是需要可靠性。

![](https://substack-post-media.s3.amazonaws.com/public/images/b74d1b16-3ff4-4bca-8df1-6e8909f865d1_2880x1620.png)
*TSMC N16 MRAM 设计特性与裸片版图。来源：TSMC，ISSCC 2026*

该 MRAM 支持双端口访问，读写可以同时进行——这对汽车的空中升级（OTA）至关重要，因为在写入固件时系统不能停止读取。

![](https://substack-post-media.s3.amazonaws.com/public/images/2bb08e47-26dd-4357-b813-60ec053c33d4_2880x1620.png)
*TSMC N16 MRAM 在 -40 °C 和 150 °C 下的 Shmoo 图。来源：TSMC，ISSCC 2026*

它支持跨模块、使用独立时钟的交错读取，在 200 MHz 下将吞吐量提升至 51.2 Gb/s。在硅片上，84 Mb 宏在 0.8V、-40 °C 至 150 °C 范围内实现了 7.5ns 的读取访问时间。

![](https://substack-post-media.s3.amazonaws.com/public/images/9ac17a55-6e1f-415f-bebb-b5dd0c966ea9_2880x1620.png)
*TSMC N16 MRAM 模块化宏架构。来源：TSMC，ISSCC 2026*

该架构是模块化的——可配置为 16 Mb、8 Mb 和 2 Mb 模块，组合成从 8 Mb 到 128 Mb 的宏。通过将大的 16 Mb 模块与少量较小的 2 Mb 和 8 Mb 模块组合，容量可以精细调校到任何设计的需要。例如，5 个 16 Mb 模块加 2 个 2 Mb 模块构成一个 84 Mb 宏。

![](https://substack-post-media.s3.amazonaws.com/public/images/be9063a9-d2b4-4d04-9dfd-ebf11aac4259_2880x1620.png)
*TSMC N16 MRAM 耐久性与可靠性。来源：TSMC，ISSCC 2026*

如前所述，可靠性是嵌入式 MRAM 的生死线。在 -40 °C 下经过 100 万次耐久循环后，硬错误率保持在远低于 0.01 ppm 的水平——完全在 ECC 纠错范围之内。150 °C 下的读扰动在典型读取电压下低于 10⁻²² ppm，实际上可以忽略不计。168 Mb 测试芯片通过回流焊测试，并支持 150 °C 下 20 年数据保持，满足严苛的汽车级要求。

![](https://substack-post-media.s3.amazonaws.com/public/images/0ef20058-3a8c-4df0-85e1-5912e2da26ff_2880x1620.png)
*TSMC N16 MRAM 规格与先前工作对比。来源：TSMC，ISSCC 2026*

与同一 N16 节点上的旧 MRAM 相比，位单元缩小 25%，从 0.033 µm² 降至 0.0249 µm²，同容量下宏密度提升至 16.0 Mb/mm²。同容量下读取速度从 6 ns 降至 5.5 ns，而双端口访问和交错读取则是全新能力。

虽然三星代工今年也发表了 8LPP eMRAM 的工作，但台积电的方案前景要好得多：它瞄准了所需的特性，性能出色，且位于更便宜的 N16 节点上。

![](https://substack-post-media.s3.amazonaws.com/public/images/87ac2737-caab-46a2-8b88-417507719b1a_2880x1620.png)
*TSMC N16 MRAM「Flash-Plus」路线图。来源：TSMC，ISSCC 2026*

台积电已在规划下一代「Flash-Plus」变体，位单元再缩小 25%，耐久性提升 100 倍。

# 光网络

多家主要光学厂商的论文探讨了将在下一代 AI 加速器之间、数据中心内部及之间承载数据的光互连。

## Nvidia DWDM —— 论文 23.1

光信令格式的选择将影响纵向扩展共封装光学（CPO）的上市时间表。Nvidia 正在放量生产支持每通道 200G PAM4 的 COUPE 光引擎，用于近期的横向扩展交换。

![](https://substack-post-media.s3.amazonaws.com/public/images/a1a30ce9-0d17-45f9-9e83-026ba5f0a876_2880x1620.jpeg)
*Nvidia DWDM 架构总览。来源：Nvidia，ISSCC 2026*

不过在 ISSCC 上，Nvidia 提议采用每波长（lambda）32 Gb/s、用密集波分复用（DWDM）复合 8 个波长的方案。第 9 个波长以半速率用于时钟前传（clock forwarding）——即 16 Gb/s。

时钟前传意味着可以通过去掉时钟数据恢复（CDR）电路及其他电路让 SerDes 变得更简单一些，从而改善能效和芯片边缘长度效率。

今年 3 月初，就在 OFC 2026 之前，[光学计算互连联盟（Optical Compute Interconnect MSA，OCI MSA）的成立](https://www.businesswire.com/news/home/20260312254951/en/Optical-Scale-up-Consortium-Established-to-Create-an-Open-Specification-for-AI-Infrastructure-Led-by-Founding-Members-AMD-Broadcom-Meta-Microsoft-NVIDIA-and-OpenAI)对外公布，该联盟将聚焦 200 Gb/s 双向链路，发送和接收各由 4 个 50G NRZ 波长构成，并在同一根光纤上双向传输。我是不是听到有人提 OCS？

![](https://substack-post-media.s3.amazonaws.com/public/images/62c2c764-5aab-4981-aedc-1e6ba3864cf4_2869x1869.jpeg)
*OCI MSA 光链路规格。来源：OCI MSA*

有趣的是，OCI MSA 并未使用额外的波长做时钟前传，把所有波长都留给实际数据传输似乎是优先事项。

Nvidia 已发表的纵向扩展 CPO 研究大多围绕 DWDM 展开，而当今的 CPO 光引擎则围绕 200G PAM4 DR 光模块构建，后者对横向扩展网络更合理。OCI MSA 围绕 DWDM 构建纵向扩展光学，化解了这一表面上的矛盾——现在很清楚，Nvidia 等厂商将围绕「纵向扩展用 DWDM、横向扩展用 DR 光模块」的思路展开。

OCI MSA 还展示了不同的实现方式：板上光学（On-Board Optics，OBO）、通过 ASIC 封装基板集成的 CPO 版本，以及光引擎直接集成在中介层上的版本。中间图 (b) 所示的实现将是未来几年纵向扩展和横向扩展 CPO 最常用的方式，但它仍需要某种形式的、可穿越 ASIC 封装基板的串行化链路，并且两端仍需要某种形式的 SerDes。例如，UCIe-S 可以作为此类传输的协议。

![](https://substack-post-media.s3.amazonaws.com/public/images/02eb01f6-1c42-4388-b07d-744346a1d768_2262x1962.jpeg)
*光引擎集成层级（OBO、基板 CPO、中介层 CPO）。来源：OCI MSA*

实现 CPO 的「最终 Boss」是光引擎能够集成到中介层本身之上，如图 (c) 所示通过并行化的裸片到裸片（D2D）连接与 ASIC 相连。这可以显著提高边缘带宽密度，实现更高的端口数（radix）并改善能效。因此，这种实现能够以其他实现无法企及的方式释放 CPO 的优势，但其落地仍需数年，且需要先进封装技术的进一步进步。

## Marvell 相干精简（Coherent-Lite）收发器 —— 论文 23.2

![](https://substack-post-media.s3.amazonaws.com/public/images/c24a930f-d8f1-4622-96e6-9a39a7388ea5_2880x1620.jpeg)
*直接检测、相干精简与相干收发器对比。来源：Marvell，ISSCC 2026*

Marvell 展示了一款面向相干精简（coherent-lite）应用的 800G 收发器。传统收发器的传输距离有限，不到 10 千米。相干收发器支持远得多的距离，但复杂、功耗更高且更贵。Marvell 的相干精简收发器在功耗、成本和距离上瞄准中间地带，非常适合链路跨度最多几十千米的大型数据中心园区。

![](https://substack-post-media.s3.amazonaws.com/public/images/9995a322-bad8-4a3c-97e1-b84fde0aa424_2880x1620.jpeg)
*相干与相干精简光频段对比。来源：Marvell，ISSCC 2026*

相干收发器主要使用 C 波段波长以获得低衰减。然而，使用相干传输的长途链路通常色散非常高，需要繁重的 DSP 处理。对于建筑物之间仅相距几十千米的数据中心园区而言，传统相干光模块的长距离能力往往大材小用。

相干精简收发器转而使用 O 波段波长，在数据中心园区相对较短的距离上色散接近于零。这使得 DSP 处理降至最低，节省功耗并降低延迟。

![](https://substack-post-media.s3.amazonaws.com/public/images/0faa6bfc-c1c4-44bc-b8c8-c3b14f466c32_2880x1620.jpeg)
*Marvell 相干精简收发器架构。来源：Marvell，ISSCC 2026*

相干精简收发器是一个基于 DSP 的可插拔模块，由两个 400G 通道组成。每个 400G 通道运行双偏振 QAM，由 X 和 Y 两条并行调制流构成。

![](https://substack-post-media.s3.amazonaws.com/public/images/cc181023-63b7-4e6e-8769-eb69fdc1ca81_682x375.jpeg)
*Marvell 相干精简实测链路性能。来源：Marvell，ISSCC 2026*

此次演示的关键，在于突出为园区应用优化、用于扩展信道带宽的其他方法。

高阶调制结合使用 X、Y 轴的双偏振可提供 400G 信道带宽。如上所示，每通道 8 位，共计 32 个星座点。这 8 位乘以 62.5 GBd 的信号速率约等于 400G 的总带宽。

这种调制方案对业界而言并不全新，但如今被引入数据中心园区环境，用于那些较短的链路。

![](https://substack-post-media.s3.amazonaws.com/public/images/79b51c03-3812-498e-8f41-b9465e2c8164_2880x1620.jpeg)
*Marvell 相干精简与既有相干收发器性能对比。来源：Marvell，ISSCC 2026*

Marvell 的方案将功耗显著降至仅 3.72 pJ/b（不含硅光子学部分），是其他全功能相干收发器的一半。他们的测量在 40km 光纤上进行，延迟低于 300 ns。

## Broadcom 6.4T 光引擎 —— 论文 23.4

![](https://substack-post-media.s3.amazonaws.com/public/images/47fde40b-9947-4fac-b9db-2ac5e7592aec_2880x1620.jpeg)
*Broadcom Tomahawk 5 51.2T CPO 光引擎裸片图与封装。来源：Broadcom，ISSCC 2026*

Broadcom 展示了其 6.4T MZM 光引擎（OE）的进展，包含 64 条约 100G 的通道，采用 PAM4 调制。这些光引擎在 Tomahawk 5 51.2T CPO 系统中进行了测试。一个 CPO 封装由八个 6.4T OE 组成，每个 OE 含一颗 PIC 和一颗 EIC，采用台积电的 N7 工艺。

![](https://substack-post-media.s3.amazonaws.com/public/images/021fa5c2-1bfd-455b-84cc-730cabf6362c_2880x1620.jpeg)
*Broadcom Tomahawk 5 CPO 光引擎封装。来源：Broadcom，Hot Chips 2024*

Nvidia 使用 COUPE，而 Broadcom 为这款 OE 采用扇出型晶圆级封装（Fan-Out Wafer-Level Packaging）。[Broadcom 未来将转向 COUPE](https://newsletter.semianalysis.com/i/178153689/tsmc-coupe-is-emerging-as-the-integration-option-of-choice)，但此类老一代产品仍在使用其他供应链伙伴。以下是他们演示中亮眼的结果：

![](https://substack-post-media.s3.amazonaws.com/public/images/179ad311-5e3a-40c0-8fb6-f809fb2f8342_2880x1620.jpeg)
*Broadcom 6.4T OE 出口发射机性能。来源：Broadcom，ISSCC 2026*

# 高速电互连

随着多裸片设计成为常态，裸片间互连成为关键瓶颈。各大代工厂和芯片设计公司展示了在有机封装基板和先进封装上推高带宽密度与能效的多种方法。

## Intel UCIe-S —— 论文 8.1

![](https://substack-post-media.s3.amazonaws.com/public/images/c7669995-eecb-4441-843f-bfaa0348e31e_2494x1403.jpeg)
*Intel UCIe-S 裸片间链路裸片图与总览。来源：Intel，ISSCC 2026*

英特尔（Intel）展示了其兼容 UCIe-S 的裸片到裸片（D2D）接口。它在 UCIe-S 下经 16 条通道可达每通道 48 Gb/s，使用定制协议可达每通道 56 Gb/s。它可在标准有机封装上工作，距离最远 30mm。有趣的是，它采用英特尔的 22nm 工艺制造。

![](https://substack-post-media.s3.amazonaws.com/public/images/ccbdc885-60a6-4372-b840-6e6525a06002_2494x1403.jpeg)
*Intel UCIe-S 与其他裸片间链路对比。来源：Intel，ISSCC 2026*

在 VLSI 2025 上，Cadence 展示了其在 N3E 上的 UCIe-S 裸片间互连。尽管节点处于劣势，英特尔还是在数据速率、通道长度和边缘带宽上击败了 Cadence 的互连，仅在能效上落败。

![](https://substack-post-media.s3.amazonaws.com/public/images/ebe7307b-d87f-43d1-b7df-4b6cfbc8211a_2786x1606.jpeg)
*Intel Diamond Rapids 多裸片架构总览。来源：HEPiX via @InstLatX64*

英特尔展示的互连很可能是其 Diamond Rapids 至强 CPU 所用方案的原型。与这颗 22nm 测试芯片相比，在 Intel 3 工艺上设计的效率会好得多，并且可以取代 Granite Rapids 上 EMIB 之类的先进封装方案。正如我们在[数据中心 CPU 格局一文中所报道的](https://newsletter.semianalysis.com/i/187132686/intel-diamond-rapids-architecture-changes)，Diamond Rapids 由两颗 IMH 裸片和 4 颗 CBB 裸片组成。每颗 CBB 裸片到两颗 IMH 裸片之间的走线都很长，我们认为该链路是在标准封装基板上连接这些裸片的可行候选，从而免去 EMIB 的需要。

## TSMC Active LSI —— 论文 8.2

![](https://substack-post-media.s3.amazonaws.com/public/images/903517c9-6ff3-4ac5-9d4a-c0130cb9cbea_2880x1620.jpeg)
*TSMC 无源与有源 LSI 对比。来源：TSMC，ISSCC 2026*

台积电先进封装部门展示了其有源局部硅互连（Active Local Silicon Interconnect，aLSI）方案。与标准 CoWoS-L 或 EMIB 不同，aLSI 改善信号完整性，并降低上方裸片上 PHY 和 SerDes 的复杂度。

![](https://substack-post-media.s3.amazonaws.com/public/images/a8f473a9-3f0e-4b7a-b717-2bc9999adae6_2880x1620.jpeg)
*TSMC Active LSI 裸片间链路总览。来源：TSMC，ISSCC 2026*

台积电展示的器件使用了 32 Gb/s 的类 UCIe 收发器。由于 aLSI 改善了信号完整性，收发器的面积得以缩小，凸点间距也可以从 45 µm 减小到 38.8 µm。更紧的间距加上改用曼哈顿网格，使他们能够把 PHY 深度从 1043 µm 缩减到 850 µm，节省的空间设计师可以重新分配给计算、内存或 IO，或者用于缩小裸片。该收发器只是类 UCIe 而非真正的 UCIe，因为 UCIe 规定使用六边形凸点排布，而非此处使用的曼哈顿网格。

在设计师为下一代 AI 加速器抠出每一寸裸片空间之际，转向 aLSI 已不可避免。

aLSI 的「有源」之处在于，用构成边沿触发收发器（ETT）电路的有源晶体管，取代桥接裸片中的无源长距金属通道，以在更长距离上维持信号完整性。这也降低了上方裸片发送/接收端口的信号驱动要求。aLSI 内部的 ETT 电路仅增加 0.07pJ/b 的能耗，最大限度降低了在堆叠裸片中加入有源电路带来的散热顾虑。通过将信号调理电路移入桥接裸片，上方裸片 TX/RX 的 PHY 面积可以通过使用更小的预驱动器和时钟缓冲器来缩减，并免去接收端的信号放大。

ETT 集成了驱动器、交流耦合电容（Cac）、带负反馈和正反馈的放大器以及输出级。信号经过 Cac 会在信号跳变沿引入峰值，随后被双环路放大器拾取，「边沿触发」之名即由此而来。放大器同时利用正、负反馈环路来稳定电压电平。在该设计中，1.7 mm 通道长度下 Cac 设为 180 fF，裸片 A 上的电阻为 2kΩ，裸片 B 上为 3kΩ。

![](https://substack-post-media.s3.amazonaws.com/public/images/c151958f-7fdb-4903-b06a-38a0eace27d5_2667x1500.jpeg)
*TSMC CoWoS-L 集成 eDTC 的供电。来源：TSMC*

这些 aLSI 桥还可以沿前端集成嵌入式深沟槽电容（eDTC），改善 PHY 和 D2D 控制器的供电。集成 eDTC 的 aLSI 避免了桥接裸片挡在中间对供电网络的损害，同时改善了 D2D 接口沿线的供电和信号布线。

![](https://substack-post-media.s3.amazonaws.com/public/images/7d837ed3-5395-4e1a-b579-c95f1d9497cc_2880x1620.jpeg)
*TSMC Active LSI 布线能力与剖面。来源：TSMC，ISSCC 2026*

64 条 TX 和 64 条 RX 数据通道仅需 388 µm 的边缘长度，折合总面积 0.330 mm²。信号布线只需顶部 2 层金属，其余金属层可用于前端电路。

![](https://substack-post-media.s3.amazonaws.com/public/images/a2747466-8e4c-4447-ad94-6c2e8b71ea4a_2880x1620.jpeg)
*TSMC Active LSI 在 KGD 与 KGP 阶段的 Shmoo 图。来源：TSMC，ISSCC 2026*

台积电解释了 Active LSI 如何在多个阶段进行测试。首先是已知良好裸片（KGD），仅含 LSI，用于裸片验证。其次是已知良好堆叠（KGS），SoC 由 LSI 相连，验证堆叠功能。最后是已知良好封装（KGP），完整组装后全面验证功能、性能和可靠性。

他们展示了 KGD 和 KGP 阶段的 shmoo 图，两者都显示该互连在 0.75V 下达到 32 Gb/s、在 0.95V 下达到 38.4 Gb/s。

![](https://substack-post-media.s3.amazonaws.com/public/images/f44de7d8-9b9f-4086-a305-6c16677e9895_2880x1620.jpeg)
*TSMC Active LSI 裸片图与功耗分解。来源：TSMC，ISSCC 2026*

封装内可以看到两颗 SoC 裸片和两颗 IO 裸片。有趣的是，该测试载板似乎与 AMD MI450 GPU 的设计相符：2 颗基础裸片彼此相连、12 个 HBM4 栈和 2 颗带 Active LSI 的 IO 裸片。而且不是每个 HBM4 栈单独配一个 Active LSI，而是两个 HBM4 栈共享一个。

功耗方面，0.75V 下总计仅 0.36 pJ/b，其中 Active LSI 内的 ETT 仅消耗 0.07 pJ/b。以下是与其它 D2D 方案的对比。

![](https://substack-post-media.s3.amazonaws.com/public/images/d194a9ff-d0ee-4e74-98a9-1f426f98205c_2880x1620.jpeg)
*TSMC Active LSI 与其他裸片间互连对比。来源：TSMC，ISSCC 2026*

## Microsoft D2D 互连 —— 论文 8.3

![](https://substack-post-media.s3.amazonaws.com/public/images/7d6415fa-2e4a-4565-af88-6db7a3c95dbc_1309x1267.jpeg)
*Microsoft D2D 测试载板版图与布线。来源：Microsoft，ISSCC 2026*

Microsoft 也详述了其裸片到裸片（D2D）互连。他们的测试载板包含两颗裸片和两对用于互连的 D2D 节点。其中完整复刻了供电网络与布线，用以模拟时钟门控和串扰。

![](https://substack-post-media.s3.amazonaws.com/public/images/1bc8b78e-9738-4558-a155-efbddcf0dbbe_472x677.jpeg)
*Microsoft D2D 互连裸片图。来源：Microsoft，ISSCC 2026*

测试裸片上的互连占用 532 µm 的边缘长度，深度为 1350 µm。测试载板在台积电的 N3P 节点上制造，互连在两个数据速率下测试：0.65V 下 20 Gb/s 和 0.75V 下 24 Gb/s。

![](https://substack-post-media.s3.amazonaws.com/public/images/ffed7179-ed8f-414b-8aeb-2ff273f25784_2880x1620.jpeg)
*Microsoft D2D 功耗分解。来源：Microsoft，ISSCC 2026*

Microsoft 报告了两个功耗数字：一个包含模拟和数字系统功耗，一个仅含模拟功耗。后者是大多数裸片间互连报告的口径。在 24 Gb/s 下，系统功耗为 0.33 pJ/b，模拟功耗为 0.226 pJ/b；在 20 Gb/s 下，系统功耗为 0.25 pJ/b，模拟功耗为 0.17 pJ/b。空闲状态功耗为 0.05 pJ/b。

![](https://substack-post-media.s3.amazonaws.com/public/images/65fefab9-0819-4c73-8c7b-39b778230934_2880x1620.jpeg)
*Microsoft D2D 与其他裸片间互连对比。来源：Microsoft，ISSCC 2026*

Microsoft 还将其互连与台积电为 Active LSI 所用的同一批先前研究进行了对比。

正如我们[此前文章中所解释的](https://newsletter.semianalysis.com/i/187132686/microsoft-cobalt-200)，Microsoft 的 Cobalt 200 CPU 由两颗计算小芯片（chiplet）通过定制高带宽互连相连。我们认为此次报告详述的正是那款互连。

# 处理器

从小型移动 CPU 到大型 AI 加速器，ISSCC 上 MediaTek、Intel、AMD、Rebellions 和 Microsoft 首次公开了各自的架构拆解，不少还附带了裸片图。

## MediaTek Dimensity 9500 —— 论文 10.2

MediaTek 每年都会展示其旗舰移动 CPU 的一个不同侧面。今年也不例外，今年移动 CPU 报告的重点是加速（boost）与热管理。

![](https://substack-post-media.s3.amazonaws.com/public/images/29b40070-6df4-435c-9621-f7837da8602f_2880x1620.jpeg)
*MediaTek Dimensity 9500 C1 Ultra 大核工艺优化。来源：MediaTek，ISSCC 2026*

台积电为 N3E 和 N3P 提供两种不同的接触式栅极间距（Contacted Gate Pitch，CGP）选项：48nm 和 54nm。大多数芯片选择了更窄的 48nm CGP，因为它带来更小的单元尺寸和更大的裸片缩减。但由于关键尺寸更小，它在漏电、布线和制造上也面临问题。

MediaTek 在其 Dimensity 9500 的 C1 Ultra 高性能大核上使用了更大的 54nm CGP，以获得更好的能效。这使他们能够以更小的热代价达到更高性能：同漏电下性能提升 4.6%，或同性能下功耗降低 3%。

MediaTek 论文的其余部分聚焦于动态性能优化：利用未用满的老化预算并减少热过冲。总体上，他们将加速频率从 4.21 GHz 提升到了 4.4 GHz。如果你对这些优化感兴趣，我们推荐阅读论文 [10.2 A Dynamic Performance Augmentation in a 3nm-Plus Mobile CPU](https://ieeexplore.ieee.org/document/11409197)。

## Intel 18A 叠加 Intel 3 混合键合 —— 论文 10.6

![](https://substack-post-media.s3.amazonaws.com/public/images/fc1e02d7-2ca4-4129-9200-e99084fa4cfc_1792x1265.jpeg)
*Intel M3DProc 18A 与 Intel 3 裸片版图。来源：Intel，ISSCC 2026*

英特尔披露了其首款混合键合芯片 M3DProc。它由一颗 Intel 3 底部裸片和一颗 18A 顶部裸片组成，两颗裸片分别包含 56 个 mesh tile——核心 tile 和 DNN 加速器 tile。两颗裸片通过 Foveros Direct（9μm 间距的混合键合）连接在一起。

![](https://substack-post-media.s3.amazonaws.com/public/images/636479de-4917-48f9-b513-7c57fe81968e_2494x1403.jpeg)
*Intel M3DProc 3D Mesh 架构。来源：Intel，ISSCC 2026*

这些 mesh tile 排列为 14×4×2 的 3D mesh，SRAM 在两颗裸片间共享。

![](https://substack-post-media.s3.amazonaws.com/public/images/c2a08665-501d-4c3b-a54a-0bfae0dc5258_2412x910.jpeg)
*Intel M3DProc 2D 与 3D 吞吐量及能效。来源：Intel，ISSCC 2026*

英特尔发现，3D mesh 降低了延迟，吞吐量提升近 40%。他们还测试了数据传输的能效：2D 指仅在底部裸片的 56 个 mesh tile 之内，3D 指跨越两颗裸片的 28 个相邻 mesh tile。结果表明，混合键合互连（HBI）对能效的影响可以忽略不计。

![](https://substack-post-media.s3.amazonaws.com/public/images/4877bf3c-30c1-4278-b85e-65ddbc343f1b_1362x1400.jpeg)
*Intel M3DProc Tile 键合版图。来源：Intel，ISSCC 2026*

每个 tile 有 552 个焊盘，其中略少于一半用于数据，略少于四分之一用于供电。

在封装方面，M3DProc 与 Clearwater Forest（CWF）相似。CWF 采用 Intel 3 基础裸片，通过 9μm Foveros Direct 与 18A 计算裸片相连。

M3DProc 实现了 875 GB/s 的 3D 带宽，而每颗 CWF 计算裸片仅实现 210 GB/s。这颗芯片的 3D NoC 带宽密度显著更高。CWF 利用 Foveros Direct 将 CPU 核心集群的 L2 缓存与基础裸片的 L3 解耦，每颗顶部裸片 6 个集群、每个 35GB/s，即每颗顶部裸片 210GB/s。M3DProc 的 875GB/s 3D 带宽则由 56 个垂直 tile 连接聚合而成，每个 15.6GB/s，且面积远小于前者。

## AMD MI355X —— 论文 2.1

![](https://substack-post-media.s3.amazonaws.com/public/images/62444551-a7bc-4619-ae99-74199208f209_2880x1620.jpeg)
*AMD MI300X 与 MI355X XCD 对比。来源：AMD，ISSCC 2026*

AMD 展示了其 MI355X GPU。在会议报告中，AMD 通常是复述此前的发布内容，只引入一两件新信息。这篇论文在这方面好得多，解释了 MI355X 的 XCD 和 IOD 相较 MI300X 的改进。

![](https://substack-post-media.s3.amazonaws.com/public/images/b0f76dac-c592-4dd4-ab6d-0d1054fc2f8b_2880x1620.jpeg)
*AMD MI300X 与 MI355X XCD 面积效率。来源：AMD，ISSCC 2026*

AMD 详述了他们如何在总面积不变、CU 数量基本相近的情况下，将每 CU 的矩阵吞吐量翻倍。首先当然是从 N5 转向 N3P，这提供了晶体管密度提升的大头。N3P 提供的额外两层金属改善了布线，从而带来更高的单元利用率。AMD 设计了自己的标准单元——正如他们此前在 N5 上所做的那样——以为其 HPC 用例优化该节点。

他们还使用了更紧密的布局算法，类似于 EPYC Bergamo CPU 中使用的 Zen 4c 核心远小于 EPYC Genoa CPU 中使用的 Zen 4 核心的做法。

用同一套硬件处理 FP16、FP8、MXFP4 等许多不同数据格式的计算有两种做法。第一种是使用共享硬件，每种格式走同一套电路，但这有功耗代价，因为对每种格式几乎没有优化。第二种是每种数据格式使用完全不同的一套电路来计算，但这会占用大量额外空间。当然，最优解介于两者之间。这项优化是 AMD 的一个重点。

![](https://substack-post-media.s3.amazonaws.com/public/images/2c313972-5315-4d1e-aa02-be6f1ffad996_2880x1620.jpeg)
*AMD MI355X XCD 频率与能效提升。来源：AMD，ISSCC 2026*

作为拥有更优晶体管的下一代节点，N3P 本身就能带来性能提升。尽管如此，在计入工艺节点改进之前，AMD 还将同功耗下的频率提升了 5%。他们还设计了多种具有不同功耗与性能特性的触发器变体，根据用途和架构需求部署在芯片的不同区域。

![](https://substack-post-media.s3.amazonaws.com/public/images/8b8604cb-0c0d-404c-942a-7b8fe000edd8_2880x1620.jpeg)
*AMD MI355X IOD 合并带来的能效。来源：AMD，ISSCC 2026*

MI300X 有 4 颗 IO 裸片，MI355X 削减为 2 颗。由此，AMD 节省了裸片间互连的面积。更大的单片裸片改善了延迟，并减少了 SerDes 和转换。此外，通过增加互连宽度，HBM 的效率也得到了提升。省下的功耗可以重新分配给计算裸片以提高性能。

![](https://substack-post-media.s3.amazonaws.com/public/images/aee3a34c-c53c-4661-ac14-8907a7764064_2880x1620.jpeg)
*AMD MI355X IOD 互连功耗优化。来源：AMD，ISSCC 2026*

作为一颗在芯片上任意两个区域之间有众多布线选择的大裸片，AMD 必须做大量工作来优化连线和互连。通过对连线的定制化工程，AMD 将互连功耗降低了约 20%。

## Rebellions Rebel100 —— 论文 2.2

Rebellions 是一家研发 AI 加速器的韩国初创公司。在 ISSCC 上，他们发表了其新加速器 Rebel100 的首个架构拆解。与大多在台积电制造的其他加速器不同，Rebellions 选择了三星代工的 SF4X 节点。在 Nvidia、AMD、Broadcom 等占据台积电大部分产能的情况下，这给了他们更多灵活性。

![](https://substack-post-media.s3.amazonaws.com/public/images/f2ea04c2-71cf-4065-98b1-606182921d24_1068x801.jpeg)
*Rebellions Rebel-Quad（现名 Rebel100）Hot Chips 2025 摘要。来源：Rebellions via ServeTheHome*

在 Hot Chips 2025 上，Rebellions 演示了该芯片运行 Llama 3.3 70B。Hot Chips 与 ISSCC 之间规格保持不变。一个关键要点是采用了三星的 I-CubeS 中介层技术。虽然 Hot Chips 幻灯片提到使用台积电的 CoWoS-S，但我们已澄清那是幻灯片上的错误，实际一直使用 I-CubeS。

我们最近提到[CoWoS-S 产能约束正在缓解](https://newsletter.semianalysis.com/i/190110359/cowos-tight-but-easing)。话虽如此，三星可能提供了大幅折扣，将 I-CubeS 先进封装与其前端工艺捆绑——使这家初创公司免于寻找并认证单独的先进封装供应商。三星也可能以其 HBM 的供应为条件，要求使用 I-CubeS。

I-CubeS 尚未获得任何主流 AI 加速器的采用，这可能是三星打入市场的一次尝试。I-CubeS 仅确认有 5 个使用者：eSilicon、百度（Baidu）、Nvidia、Rebellions 和 Preferred Networks。

第一个是 eSilicon 在三星 14LPP 上搭载 HBM2 的网络 ASIC。Baidu 的 Kunlun1 加速器类似，采用三星 14LPP 工艺和 2 个 HBM2 栈。2023 年 CoWoS-S 产能非常紧张时，Nvidia 曾将少量 H200 生产外包给 I-CubeS。然后就是 Rebel100，最后是 Preferred Networks 计划在 SF2 工艺上打造的加速器。

![](https://substack-post-media.s3.amazonaws.com/public/images/91f29194-e088-40ef-b134-ac45449d21ae_2880x1620.jpeg)
*Rebellions Rebel100 多裸片架构。来源：Rebellions，ISSCC 2026*

Rebel100 使用 4 颗计算裸片和 4 个 HBM3E 栈。每颗裸片有 3 个 UCIe-A 接口，不过每颗裸片只使用其中两个，速率为 16 Gb/s。

![](https://substack-post-media.s3.amazonaws.com/public/images/f9b5a17f-feb0-4c70-b528-cae2a38c11f3_2880x1620.jpeg)
*Rebellions Rebel100 封装级模块化。来源：Rebellions，ISSCC 2026*

Rebellions 声称该设计在封装级可重构，可以添加额外的 IO 或内存小芯片，与以太网集成以实现纵向扩展。这就是剩余那个 UCIe-A 接口的用途。

Rebellions 表示 IO 小芯片将在 1Q2026 前流片。内存小芯片没有给出时间表。

![](https://substack-post-media.s3.amazonaws.com/public/images/cbab43a4-26b7-4011-bfeb-ea01c4902a56_2880x1620.png)
*Rebellions Rebel100 总结与路线图。来源：Rebellions，ISSCC 2026*
![](https://substack-post-media.s3.amazonaws.com/public/images/759c00f2-e242-404b-a841-5e4458a75e4c_2880x1620.png)
*Rebellions Rebel100 用于 HBM3E 供电质量的集成硅电容。来源：Rebellions，ISSCC 2026*

他们还在每个 HBM3E 栈旁集成了硅电容，以改善 HBM3E 和关键控制模块的供电质量。

## Microsoft Maia 200 —— 论文 17.4

Microsoft 详述了其 Maia 200 AI 加速器。这篇论文与其说是研究论文，不如说是白皮书，只有一张图片——一份与 Maia 100 对比的规格表。考虑到 Maia 200 的许多宣称存疑（例如 flops/mm^2 和 flops/w），这也说得通。

Maia 100 设计于前 GPT 时代，而 Maia 200 则是为当前这一代模型、尤其是推理而设计。今年早些时候，Maia 200 节点已在 Azure 上正式开放。

![](https://substack-post-media.s3.amazonaws.com/public/images/0c381cad-9332-483a-9fd7-8de08cd7d90a_2880x1620.jpeg)
*Microsoft Maia 200 规格总结。来源：Microsoft，ISSCC 2026*

Maia 200 是光罩级单片设计的最后坚守者。所有主流搭载 HBM 的训练与推理加速器都已转向多芯片设计，每个封装配 2、4 甚至 8 颗计算裸片。裸片的每一平方毫米都为单一目的进行了极限优化。与 Nvidia 或 AMD 的 GPU 不同，它没有用于媒体或向量运算的遗留硬件。Microsoft 在台积电的 N3P 工艺上将光罩级单片方案推向极限，塞入了超过 10 PFLOPs 的 FP4 算力、6 个 HBM3E 栈和 28 条 400 Gb/s 全双工 D2D 链路。

![](https://substack-post-media.s3.amazonaws.com/public/images/98820b64-6a10-4132-b24a-a2122f7417ad_2880x1620.jpeg)
*Microsoft Maia 200 封装剖面。来源：Microsoft，ISSCC 2026*

在封装层面，Maia 200 非常标准，模仿了 H100：CoWoS-S 中介层，1 颗主裸片加 6 个 HBM3E 栈。

![](https://substack-post-media.s3.amazonaws.com/public/images/4949a336-f267-4f4c-b813-1f6af0d7f629_506x541.jpeg)
*Microsoft Maia 200 裸片版图。来源：Microsoft，ISSCC 2026*

芯片的两条长边各覆盖 3 个 HBM3E PHY，两条短边各承载 28 条 400 Gb/s D2D 链路中的 14 条。中央是 272 MB 的 SRAM，其中 80 MB 为 TSRAM（L1）、192 MB 为 CSRAM（L2）。

![](https://substack-post-media.s3.amazonaws.com/public/images/62240549-cf4a-4472-8294-7b7b2bca21fa_2880x1620.jpeg)
*Microsoft Maia 200 纵向扩展网络与 IO。来源：Microsoft，ISSCC 2026*

Maia 200 有两类链路：同一节点内其他芯片之间的固定链路，以及芯片与交换机之间的交换链路。21 条链路配置为固定链路，到其他每颗芯片各 7 条；其余 7 条链路配置为交换链路，连接到四个机柜内交换机之一。

我们将为机构订阅用户发布一篇关于 Maia 200、其微架构和网络拓扑的深度解析。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

# 其他亮点

## Samsung SF2 温度传感器 —— 论文 21.5

![](https://substack-post-media.s3.amazonaws.com/public/images/5ae89ead-c1e7-409c-912f-bf86d659e2c0_2880x1620.png)
*传统温度传感器的取舍。来源：Samsung，ISSCC 2026*
![](https://substack-post-media.s3.amazonaws.com/public/images/66a71ead-cde8-4e94-9ea5-ddf5caebf775_2880x1620.png)
*Samsung SF2 基于金属电阻的温度传感器取舍。来源：Samsung，ISSCC 2026*

三星展示了 SF2 上的一款紧凑温度传感器，用后道金属（BEOL）电阻取代了传统的双极结晶体管（BJT）方案。这可能不如下一代内存或处理器那么抢眼，但对让芯片正常工作至关重要。

该金属电阻的方块电阻是同等布线金属的 518 倍，实现同样阻值大约只需 1% 的面积。由于位于上部金属层，它为其下方的电路留出了充足空间，并消除了 FEOL 面积开销。虽然分辨率较低，但其收益远超这一缺点。

![](https://substack-post-media.s3.amazonaws.com/public/images/22987230-7e2a-4317-b244-f4e76930494b_2880x1620.png)
*Samsung SF2 温度传感器堆叠式实现。来源：Samsung，ISSCC 2026*

该传感器采用全堆叠的电容-电阻-电路结构，总面积仅 625 μm²。作为经过表征的 PDK 元件，其行为由代工厂建模并验证。它更适合必须严格控制工艺偏差的大批量生产。即便在单颗芯片上，也可能在热点附近使用数千个这样的传感器。

如前所述，金属电阻的电阻温度系数（TCR）较低，仅为布线金属的 0.2 倍——这限制了感测分辨率。三星通过提高基础阻值来补偿，但随着 RC 时间常数增大，感测时间会变慢。为此，三星采用时间偏移压缩技术：低阻（0.1R）快充路径先快速给 RC 滤波器充电，然后电路切换到全阻值，完成波形中温度敏感部分的感测。

对于时间数字转换（TDC），他们用紧凑的环形振荡器（RO）TDC 取代了先前工作中使用的大型线性延迟发生器，将延迟发生器面积削减 99.1%。该 RO 还兼任系统时钟，相位交错计数可防止非单调性。

![](https://substack-post-media.s3.amazonaws.com/public/images/2cd264f4-0a79-4823-8ab5-1cbfd4627f9f_2880x1620.png)
*Samsung SF2 温度传感器与先前工作对比表。来源：Samsung，ISSCC 2026*
![](https://substack-post-media.s3.amazonaws.com/public/images/0d4c4094-3c4e-42fc-a4d5-6087d122c98a_2880x1620.png)
*Samsung SF2 温度传感器转换时间与精度对比。来源：Samsung，ISSCC 2026*

新款温度传感器的精度品质因数（FoM）为 0.017 nJ·%²，优于此前在三星 5LPE、台积电 N3E 和 Intel 4（JSSC 2025）上的工作。以往的温度传感器只能在这些指标中择一优化：面积或速度。N3E 上的传感器很小，仅 900 μm²，但需要 1 ms；而三星 5LPE 上的传感器很快，仅 12 μs，但面积巨大，达 6356 μm²。
