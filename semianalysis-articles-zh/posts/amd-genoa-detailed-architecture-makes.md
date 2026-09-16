---
title: "AMD Genoa 详解——架构让 Xeon 看起来像恐龙"
title_en: "AMD Genoa Detailed – Architecture Makes Xeon Look Like A Dinosaur"
subtitle: "两倍的 CPU 性能，无需两倍的功耗"
date: 2022-11-10
source: https://newsletter.semianalysis.com/p/amd-genoa-detailed-architecture-makes
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# AMD Genoa 详解——架构让 Xeon 看起来像恐龙

> 原文：[AMD Genoa Detailed – Architecture Makes Xeon Look Like A Dinosaur](https://newsletter.semianalysis.com/p/amd-genoa-detailed-architecture-makes) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**两倍的 CPU 性能，无需两倍的功耗**

本周我们有幸参加了 AMD 第 4 代 Genoa 服务器发布活动。更关心[出货量、ASP 与营收的读者，请参阅我们的深度报告](https://www.semianalysis.com/p/2023-datacenter-outlook-amd-and-intel)。

[![](https://substackcdn.com/image/fetch/$s_!HwSb!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F0150776c-9bf2-4bea-a9c2-41b24b7a0f15_1280x1280.png)SemiAnalysis2023 Datacenter Outlook – AMD and Intel Revenue, ASP, and Units – Genoa Ramp DetailsAMD has held pre-briefings for their next-generation 96-core Zen 4-based Genoa server platform. While we were unable to attend officially under NDA, the industry has been buzzing for months about the new product line. This includes this week at the OCP Summit which we are attending. Performance is absolutely incredible, with more than 2x the performance per socket in many general-purpose applications versus current platforms…Read more4 years ago · 20 likes · 3 comments · Dylan Patel](https://www.semianalysis.com/p/2023-datacenter-outlook-amd-and-intel?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

本报告将聚焦于技术、架构、性能与 SKU。长话短说：由于验证周期漫长，服务器行业一直迟迟不愿更换新供应商。稳妥的选择是继续留在现有供应商那里——几十年前是 IBM，如今是 Intel。

> 停留在 Xeon 的性能劣势里，才是不安全的。
>
> —— Ram Peddibhotla，Epyc 产品管理负责人

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/dc68ffc7-5271-4fa4-8241-cb19438f08a1_2654x1478.png)

第 4 代 Epyc Genoa 的发布，标志着 AMD 连续第 3 代在多数性能指标上击败 Intel。Rome 和 Milan 让云厂商开始大量采购 AMD，而 Genoa 则是[出货量在其余大多数市场和终端用户中全面跃升](https://www.semianalysis.com/p/2023-datacenter-outlook-amd-and-intel)的时刻。SemiAnalysis 认为，Genoa 与 Sapphire Rapids 之间的差距大于 Milan 与 Ice Lake 之间的差距。这一差距将持续扩大，直到 2024 年底，甚至可能延续到 2025 年的 Sierra Forrest 与 Granite Rapids。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/611140aa-d047-4b13-bfb8-0fff43a602ec_2654x1478.png)

AMD 正在推出越来越多的 CPU 变体。CPU 面向通用工作负载，但针对不同终端市场的定制化在不断加强。第 4 代有 4 个变体。Genoa 是今天的主角，面向通用与主流市场。

Bergamo 面向云原生工作负载。它的 IO die 与平台和 Genoa 共享，因此许多方面相似，但把 Zen 4 核心换成了 Zen 4C 核心——核心架构与 L2 缓存相同，每核 L3 缓存减半。Zen 4C 的核心排布以牺牲频率为代价最大化密度。

Genoa 还有一个面向「技术（technical）」领域的变体，叫 Genoa X。这个定义有点奇怪，但它面向计算流体力学、EDA 以及其他需要更多缓存的工作负载。Genoa X 就是带 3D V-Cache 的 Genoa，且可能有多个变体。

Siena 面向电信与边缘。由于功耗与资本开支需求更低，我们认为它也适用于某些企业级部署。可以把 Siena 理解为从内存到核心数都是 Genoa 或 Bergamo 的一半。不完全精确，但大意如此。

最后，AMD 的下一代叫 Turin，我们预计 2024 年上半年发布。它拥有更多产品家族与变体，但今天透露这些细节对 AMD 不太公平。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/665ad1d2-eda5-4ca3-8721-19b28d9fab79_2654x1478.png)

总结：AMD Genoa 的性能约为 Milan 的 2 倍，而功耗只有温和增长。得益于 AVX512 的加入以及内存带宽的大幅提升，浮点收益更大。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c3a7e532-debd-4f95-958e-35ce6a97bd91_5219x1458.png)

规格方面没有太大意外：96 核心、12 通道 DDR5、160 条 PCIe Gen 5 通道（其中 64 条支持 CXL）。CXL 挂载内存的加密对多租户云架构的安全至关重要。我们此前已[在此详述这些特性](https://www.semianalysis.com/p/cxl-deep-dive-future-of-composable)。支持加密不需要 CXL 内存 ASIC/设备提供任何支持，也不依赖任何特定 ASIC。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/042d541d-7448-4815-90fd-92eaf9e28b29_5219x1458.png)

Genoa 的心脏是 Zen 4 核心。性能大幅提升：IPC 提高 14%，频率显著提高，且得益于 2 倍大的 L2 缓存，平均延迟也有改善。我们对右边那张注明「仅作示意」的图做了像素统计：前端（Front End）贡献了 IPC 提升的 40%，加载/存储（Load/Store）改进贡献 24%，分支预测贡献 20%，L2 缓存与执行引擎各贡献 8%。

我们昨天见到了 Mike Clark，那是一次奇妙的会面。不熟悉的人可以了解一下：他基本上就是 Zen 的发明者。他掌管着整个 CPU 核心路线图，但为人非常谦逊。

> 我很荣幸能代表地球上最伟大的 CPU 团队
>
> —— Mike Clark，AMD Zen 首席架构师

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/78c594ab-5bf3-498a-9ea7-c1ced012dfa9_5304x2956.png)

架构细节我们不再展开，因为我们的朋友 [Chips And Cheese](https://chipsandcheese.com/) 已经讲得远比我们细致。

[AMD's Zen 4 Part 1: Frontend and Execution Engine](https://chipsandcheese.com/2022/11/05/amds-zen-4-part-1-frontend-and-execution-engine/)

[AMD's Zen 4, Part 2: Memory Subsystem and Conclusion](https://chipsandcheese.com/2022/11/08/amds-zen-4-part-2-memory-subsystem-and-conclusion/)

我们想专门谈的一点是 AVX512——一个浮点向量指令集。Intel 以 512 位宽度实现它，但这也意味着硅面积成本过高，因此 Intel 不在客户端芯片上包含该特性。此外，当 AVX512 启用时，芯片的时钟频率会下降，芯片上的其他工作负载跟着遭殃。AMD 走了一条聪明得多的路线：把它拆分到 256 位单元上分多个周期执行。这意味着[不存在「吵闹邻居」问题](https://www.semianalysis.com/p/is-ampere-computings-cloud-native)，硅面积影响也很小。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/f9a95cf1-75f4-4da0-92a0-6af7a97687d8_2654x1478.png)

安全永远值得一提。AMD 在多项核心级与 SOC 级安全特性上相对 Intel 占优。最值得注意的一项与 SMT（即超线程）有关。Ampere Computing 喜欢主张[每核多线程运行是不安全的](https://www.semianalysis.com/p/is-ampere-computings-cloud-native)。AMD 用 SEV-SNP 作出了回应：实现了该特性的安全客户机线程，可以选择在共享核心上存在活跃的兄弟线程时不运行。这能防范 Spectre、Meltdown 之类的侧信道攻击。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/83de7fad-00ef-4649-ba3b-1b7e9cc68427_5278x2891.png)

可以说，IO Die 才是第 4 代 Epyc 发布中更大、也更重要的变化。它采用 N6 工艺节点，而非 CPU 小芯片所用的 N5。IO die 如今得到强化，通过一个层数更多的更大封装与 12 个小芯片通信。当幻灯片上密密麻麻全是字，那说明它们很棒——几乎不需要额外解释，你自己读就行！

另一个值得注意的点是插槽（socket）彻底重新设计：安装机构更坚固，引脚间距更紧，为 0.94 × 0.81mm。尺寸从 58mm × 75mm 增大到 72mm × 75mm。层数更多的更大封装对 Unimicron 这样的公司是大事。

AMD 在 IO 可扩展性上非常值得称道。他们使用支持组合模式的 SerDes。本质上，这些 SerDes 可以有多种「人格」，让连接对象的选择高度可配置。平台可以配置 3 条或 4 条 Infinity Fabric 通道，从而在 2S 配置下实现可扩展的 PCIe 通道数。每台 2S 服务器可以选：3 条 Infinity Fabric 通道 + 160 条 PCIe 通道，外加 12 条平台用 PCIe 链接；或者 4 条 IFIS + 128 条 PCIe，外加 12 条平台用 PCIe。每个 16x PCIe 根复合体可以切分为 9 个 PCIe 设备：1 个 8x 设备 + 8 个 1x 设备。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/445e6200-8733-43e4-a09a-1a515237ec4b_2654x1478.png)

鉴于 Genoa 大幅提升了 IO 速度，充分利用这些带宽就至关重要。增强型 AVIC 降低了 IO 设备虚拟化的开销。这带来更高的带宽利用率和更低的 CPU 开销。Milan 上有一个更早期的版本，但更接近原型性质。如今在 Genoa 上，IO 设备已接近原生性能。测试用的是 Nvidia 旗下 Mellanox 的 Connect X7 跑 InfiniBand。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8aba2a1b-dc51-41c5-a618-3ad93dfcd169_5278x2891.png)

Genoa 在[内存成本——占服务器 BOM 的 50%](https://semianalysis.substack.com/p/cxl-enables-microsoft-azure-to-cut)——上有几项关键增强，其重要性怎么强调都不为过。

对 72-bit 和 80-bit DIMM 的支持值得注意。大多数服务器会用 80-bit ECC，但一些超大规模云厂商想降到 72-bit。相对于非 ECC 内存的 64-bit，这仍保有一定 ECC 能力，只是低于广泛使用的关键任务级 80-bit。好处是用于校验的 DRAM 裸片少了 1 颗。「Bounded Fault（限定故障）」能力对此也有帮助，因为一旦在内存器件中检测到错误，这些问题可以被映射出来。

另一个重要特性是双 rank 与单 rank 内存之分。在 Milan 和大多数 Intel 平台上，双 rank 内存对最大化性能至关重要。例如在 Milan 上有 25% 的性能差距。在 Genoa 上，这一差距被降到了 4.5%。这是又一笔可观的成本改进，因为可以使用更便宜的单 rank 内存。

Genoa 的内存延迟高于 Milan：Genoa 为 118ns，Milan 为 105ns。AMD 对此的解释是：其中只有 3ns 来自大得多的 IO die——Genoa 为 73ns，Milan 为 70ns。内存延迟的影响主要来自 DDR5 内存器件本身：DDR5 为 35ns，DDR4 为 25ns。这源于 DDR5 尚不成熟导致的时序放宽、更大的 bank 容量以及架构上的其他变化。内存延迟影响不小，但 SOC 层面微乎其微的增加令人赞叹。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ee7cf2b6-00ed-4f78-a8e2-138de658d5b1_5272x1462.png)

IO Die 与核心复合裸片（CCD）之间的连接得到了大幅改进。每比特传输功耗降至 ~2pj/bit 以下。作为参照，EMIB 号称约 ~0.5pj/bit。最值得注意的是新增了 GMI3-Wide 格式。在客户端 Zen 4 以及此前几代 Zen 小芯片上，IOD 与 CCD 之间只有 1 条 GMI 链接。而在 Genoa 上，对于核心数较少、CCD 数较少的 SKU，可以有多条 GMI 链接连到 CCD。这对低核心数 SKU 是巨大的带宽提升。具体而言，这将帮助关系型数据库和高频 SKU——在这些场景下，按核心授权的费用是一笔巨大开支。

功耗管理得到增强。Genoa 有两种基本功耗管理模式：性能确定性（performance determinism）与功耗确定性（power determinism）。由于热学与硅片的差异，不同芯片上的不同工作负载之间可能存在许多差别。硅片并非确定性的——毕竟制造涉及数千道工艺步骤。

性能确定性面向想要一致性能的企业。在允许时消耗更少功率，性能保持稳定。大多数客户会选择这个选项，因为稳定性至关重要。

功耗确定性则是保持功耗稳定，让性能上下浮动。鉴于硅片抽签（silicon lottery）、热预算与工作负载等因素，芯片会动态升降频。

除了功耗管理模式外，Genoa 芯片还有可配置的 TDP。峰值加速行为取决于所选选项。时钟加速基于可靠性与峰值供电能力。高活跃度工作负载将以更低频率运行。系统与硅片裕量都会被考虑。

与消费级平台相比，功耗预算不会被长时间突破。TDP 只能在数十毫秒内被超出。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/4d68c679-0b75-49a4-9e21-5c29fe2a754c_1400x758.png)

AMD 总体上支持 CXL 1.1，但对 Type 3 内存设备支持 CXL 2.0。我们已独家详解过[该特性的支持层级](https://www.semianalysis.com/p/cxl-deep-dive-future-of-composable)。

> Type 3 正是生态系统想要的。
>
> —— Kevin Lepak，Genoa 服务器 SOC 首席架构师

Genoa 为增加这一特性延期了 2 个季度，我们认为那是正确的决定。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/eaa52427-cc67-4b56-a3a2-f785a18669e2_2667x1500.png)

值得注意的一项是：64 条 CXL 通道可以 bifurcate（分化）为 16 个 4x 设备。正如我们[在此独家详述的](https://www.semianalysis.com/p/cxl-deep-dive-future-of-composable)，Sapphire Rapids 无法进行 CXL 通道分化。如果接一个 4x 或 8x 的 CXL 设备，会占满全部 16 条通道。Emerald Rapids 修复了这一特性，但那还是一年之后的事。

Hypervisor 无法更改客户机之下的内存分配，这对在云端使用 CXL 挂载内存的用户来说是大事。

AMD 的性能支柱是：每路（per-socket）性能领先、每核性能领先、在所有工作负载与细分市场全面领先、以及 TCO 与可持续性领先。而这一切都由能效领先来支撑。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/3356d579-c6f5-4a4f-9a24-0c7670581090_1300x735.png)

这张对比图最能说明问题：一颗中端 Genoa 对阵两颗顶配 Xeon。AMD 性能更高、功耗更低、CPU 成本更低，核心数还更少。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/55ffdb81-97b4-4dba-916b-17ac2b470dcb_5252x2992.png)

AMD 的领先是开创性的。特别要注意：当按核心数的软件授权成本计入时，这一领先在 TCO 上会进一步拉大。企业级基准测试最能体现这一点，它运行 VMMark。VMMark 每 tile 运行 19 个代表性 VM，然后衡量能跑多少个 tile 以及速度。Genoa 更快，且能承载更多 VM。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/82b08b51-d728-4233-99d3-9303740743f4_2654x1478.png)

SKU 命名非常直观清晰，每个数字都代表关键信息。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/eb6132c5-07b8-4ff6-9f9f-e09c956887bf_2686x764.png)

AMD 保持 SKU 阵列简洁。与 Intel 不同，没有一大堆锁定特性的 SKU。共有 3 个大类、18 个 SKU：核心性能（F）、核心密度、均衡/TCO 优化。他们也按单路（1 socket）与双路（2 socket）支持做区分。每核心价格也保持相对平稳。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ac86ecb4-14de-4709-a8d8-6f6cf5ce7295_5259x2935.png)

在 Genoa 上，AMD 的每核性能领先在整数工作负载上通常约 ~50%，浮点上高达 96%！后者很大程度上要归功于内存带宽与缓存。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/25eceeb1-4b02-4200-965c-1746790200c4_5259x2945.png)

SQL 基准测试值得注意，因为在某些数据库基准中，AMD 由于核间延迟较高而落后。在许多这类场景中他们仍会落后，但在一些常用项目上差距正在缩小。Sapphire Rapids 的单片式（monolithic）与 4 裸片先进封装方案的优势在于：那些大型关系型数据库的核间延迟会低得多。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a19ce190-3188-4649-b063-f260d8cbbd2c_5196x1478.png)

在 HPC 性能对比中，96C 的对比显示它仍受内存带宽限制，但 32C 对 32C 的对比表明 Genoa 的带宽优势巨大。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/003125aa-3ee3-4471-89ef-3fdeb4ae10c7_2667x1500.png)

服务器整合是这里的重头戏。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/f805dfcf-7373-4709-a251-304dbb1f0bf6_5229x1500.png)

具体数字取决于你用 2P 对 2P 还是 2P 对 1P 服务器，但结果类似：大致是 3 颗 CPU 整合为 1 颗。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/996a9691-5d79-4892-9140-1328ead833bd_1267x705.png)

Genoa 有趣的地方在于：它的核心实在太多，工作负载无法在整个芯片上扩展，有些应用甚至会崩。好在 AMD 的规模终于大到能接触大多数软件 ISV，因此 Genoa 发布时这些「长牙期的烦恼」大多已解决。回到 Naples 和 Rome 的年代，这还是痴人说梦。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/bf0b8ff9-18b6-476a-a98f-87205b5bbd61_2654x1478.png)

最后以机密计算（confidential computing）收尾。机密计算讲的是：你的软件无需信任硬件的拥有者，也能保障数据安全。静态与传输中的数据，加密是众所理解的标准答案；但「使用中」的数据，答案就复杂了。虽然 Genoa 尚未完全交付机密计算的完整愿景，但它在该领域带来了许多创新，让这一愿景近了一大步。毕竟机密计算是一个渐进的刻度。

感谢阅读 SemiAnalysis。本文为公开文章，欢迎分享。

[分享](https://newsletter.semianalysis.com/p/amd-genoa-detailed-architecture-makes?utm_source=substack&utm_medium=email&utm_content=share&action=share)

在仅限订阅者的部分，我们将简要分享我们对 2023 年底服务器市场份额与营收份额、AMD 股票的看法，并提供一个小型赠品活动。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
