---
title: "Meteor Lake 裸片图与架构分析——为什么 Intel 4 相对 Intel 7 只有 40% 的面积缩减？"
title_en: "Meteor Lake Die Shot and Architecture Analysis – Why Is Intel 4 Only A 40% Area Reduction Versus Intel 7?"
date: 2022-05-26
source: https://newsletter.semianalysis.com/p/meteor-lake-die-shot-and-architecture
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Meteor Lake 裸片图与架构分析——为什么 Intel 4 相对 Intel 7 只有 40% 的面积缩减？

> 原文：[Meteor Lake Die Shot and Architecture Analysis – Why Is Intel 4 Only A 40% Area Reduction Versus Intel 7?](https://newsletter.semianalysis.com/p/meteor-lake-die-shot-and-architecture) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

在这篇报告中，[Locuza](https://twitter.com/locuza_) 与 SemiAnalysis 将分享并分析英特尔（Intel）Meteor Lake 计算模块（compute tile）在 Intel 4 制程节点上的裸片图。借助这张裸片图，我们可以分析核心、缓存与互连（fabric）中的各种结构，进而判定其相对 Intel 7 节点大约只有 40% 的面积缩减。这一实际达成的密度提升，与英特尔此前宣称 Intel 4 制程节点将带来的 2 倍理论密度增益大相径庭。Intel 4 是英特尔首个采用 EUV 的工艺技术，本应标志着英特尔在工艺上重返与台积电（TSMC）竞争的行列。我们还将讨论 Meteor Lake 与 Arrow Lake 的系统架构，以及重新设计的 Redwood Cove 和 Crestmont 核心内部的架构变化。最后，我们会讨论爬坡时间表、竞争定位以及一些对制造成本的担忧。如果你更想边看边听，我们还制作了 [YouTube 视频](https://youtu.be/2JBXnVyZRr4)。

在进入细枝末节之前，我们需要从几周前说起，带你了解我们是如何做这项分析的。英特尔举办了自己的 Vision 大会，议题涵盖当前与即将推出的产品等方方面面。SemiAnalysis 得以参会，并与英特尔的人进行了许多精彩的交流。其中最有意思的一幕，是 [Pat Gelsinger 在回答我们的提问时直截了当地表示会收购更多 SAAS 公司](https://semianalysis.substack.com/p/turning-the-titanic-how-intel-is)。其他亮点包括近距离接触英特尔的部分产品、当面请教工程师技术问题。对我们而言，最兴奋的莫过于有机会给各种英特尔产品拍照！照片里的我显然非常开心，手里拿着英特尔的部分网络产品：Tofino 2、Tofino 3 和 Mount Evans IPU（DPU）。虽然我们还不能深入谈论 Tofino 3 的能力，但它是世界上最大的 BGA 封装。换句话说，那可是好大一片硅。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/48747e24-344f-4f96-8acb-e4bd2a0f2b1f_768x1024.jpeg)

展会上最有意思的实物是硅晶圆，包括 Alder Lake 桌面 CPU、下一代 Sapphire Rapids 数据中心 CPU 和下一代 Meteor Lake 计算模块。他们还展示了一些来自 Intel 20A 和 Intel 18A 工艺技术的测试晶圆。虽然我们自己拍的 Meteor Lake 照片不怎么样，但我们的朋友 [Comptoir-Harware](https://www.comptoir-hardware.com/actus/processeurs/45991-intel-vision-exclusivite-comptoiresque-un-die-shot-de-meteor-lake-ca-vous-dit-.html) 拍到了更好的！他们把 Meteor Lake 晶圆放大到了单颗裸片。这张图片是我们下文大量分析的基础。[Carsten Spille](https://twitter.com/CarstenSpille/status/1524174362185719808) 对封装图片的处理也非常出色。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/0a1fb08c-b6d6-4cb5-ad1b-00a94743839a_860x1024.png)

利用 Meteor Lake 晶圆与封装的第一方及媒体图片，以及[封装过程的视频](https://www.cnet.com/pictures/a-look-inside-intels-mammoth-arizona-chipmaking-fab/)，我们可以确定英特尔在 Meteor Lake 上所用各小芯片的裸片面积。计算模块（compute tile）由多个 CPU 核心模块及部分相关互连组成，仅有区区 ~40mm²。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2821a99c-5859-49f3-b7f4-83361452f289_1024x847.jpeg)

其他裸片分别约 ~174mm²、~10mm²、~95mm² 和 ~23mm²。每颗裸片的确切用途尚未证实，但我们认为它们分别用于 IO、SOC 和 GPU。本文稍后会为每个模块单独开辟章节。先来谈计算模块。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/863ef392-1fa0-4832-b09e-097a4e260c04_1024x674.jpeg)

[Locuza](https://twitter.com/locuza_) 得以识别并标注裸片上的大多数结构，包括 2 个 P 核 Redwood Cove、8 个 E 核 Crestmont，以及挂在环形总线（ring bus）上的末级缓存。这里要说明，本分析并不完美，存在一些注意事项。Meteor Lake 的图片是用普通单反相机拍摄的。[Locuza](https://twitter.com/locuza_) 校正了离轴倾斜等因素，但条件仍然不是最优，限制了精度。这些图片摄于展会现场而非实验室，分辨率不算最高。切割道（scribe line）边缘以及其他一些因素也存在不确定性。因此我们认为裸片图中各结构的潜在误差在中等至高个位数百分比范围。并非所有结构和结构尺寸都保证 100% 正确，但我们认为自己准确呈现了物理版图设计。我们将如实呈现测量数据。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9feb47d9-f545-4e49-b331-affd89233a72_1024x349.png)

左边是当代 Alder Lake 的 Golden Cove，右边是 Meteor Lake 的 Redwood Cove。从高层视角看，Redwood Cove 并没有大幅洗牌，大多数子单元看起来与之前非常相似，位置和相对尺寸比例都没有变。在许多结构上，Redwood Cove 基本是一次工艺收缩，但仍有不少一眼可见、应有助于 IPC 和性能的架构变化。

例如，L1 缓存看起来相对更大（图像分析显示 40KB 到 45KB），因此我们认为它可能从现在的 32KB 增加到了 48KB。L2 缓存似乎从 1.25MB 增长到 2MB。这一 L2 缓存变化看来也会出现在今年晚些时候发布的英特尔 Raptor Lake 上。英特尔很可能改进了分支预测逻辑，尽管缓冲区大小看起来（基本）没变。这个结构基本上是每一代核心都要微调的地方。加载/存储缓冲区似乎也更大了，可以期待更好的内存子系统。乱序（OoO）区域与分支预测单元之间的区域有几个模块看起来比以前大。FPU 设计看起来几乎没变，根据该指令的各种软件指标，AVX512 似乎也相对未变。浮点和整数寄存器堆也不显得更大，所以我们不预期表项数大幅增加。最后，有几个模块的版图重新设计过，包括 SRAM 的摆放改为纵向占用更多空间而非横向。我们需要第一方的架构讲解，以及 [Chips and Cheese](https://chipsandcheese.com/) 这类网站的深入微基准测试，才能真正弄清变化所在。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/11715907-4521-4c3d-8e75-3ec5d8f82746_1024x602.png)

面积对比才是火药味渐浓的地方。整颗核心的总面积缩减约 ~25.17%（密度提升 1.34 倍）。各模块相对收缩幅度不同的原因有几个。一是两颗核心之间存在明确的架构变化，因此总面积对比并非同类项相比。另一个原因是 SRAM 和逻辑的收缩幅度不同，所以即使结构完全相同，基于各模块的构成也会得到不同的收缩系数。这一点我们在[根据英伟达大型泄密中的规格与仿真估算其下一代 Lovelace 架构裸片面积](https://semianalysis.substack.com/p/nvidia-ada-lovelace-leaked-specifications?s=w)时已详细讨论。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

最能剔除架构因素、纯粹对比工艺的，是 Intel 4 与 Intel 7 上 256KB L2 缓存的尺寸差异。我们的数据显示面积缩减 26.5%（密度提升 1.36 倍）。实际收缩与英特尔对其高密度 SRAM 单元的宣称相当接近，尽管要注意 L2 缓存可能采用性能更高的 SRAM 单元，并包含辅助电路等逻辑。单个子单元面积缩减最大的是整数寄存器堆，接近 40%（密度提升 1.65 倍），因此我们把它设定为实际工艺密度提升的上界。这与宣称的 2 倍收缩相去甚远。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/6c7d18d6-94c4-469b-ba9e-e4279840ffb6_1024x459.png)

计算模块上可用于密度对比的另一主要结构是 E 核。左边是 Alder Lake 的 Gracemont，右边是 Meteor Lake 的 Crestmont。从架构上看，除了 L2 缓存似乎从 2MB 变成 3MB 之外，这个对比能挖掘的信息不多。奇怪的是，一些爆料称 Raptor Lake 的 E 核 L2 会提升到 4MB，那将使 Meteor Lake 的 3MB 处在一个尴尬的中间地带。Raptor Lake 的这个细节尚未证实。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/6088a70e-2300-4741-ae91-37abb0ee2d8d_1022x185.png)

Crestmont 的核心在视觉上似乎没有重大架构变化，~34% 的面积缩减（密度提升 1.52 倍）也支持这一判断。共享 L2 缓存主要由 SRAM 构成，因此该模块的收缩更小。整个 E 核集群面积缩减约 ~29%（密度提升 1.4 倍）。带 L2 缓存的 Golden Cove 比不含共享 L2 的 Gracemont 大约 ~4.48 倍。到了 Meteor Lake，两颗核心的尺寸差距进一步拉大：Redwood Cove 比 Crestmont 大约 ~5.1 倍。英特尔的 E 核战略对于最大化单位硅面积的性能而言完全说得通。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/152edfa5-9b77-468f-9e21-52b74fc477d7_1024x847.jpeg)

CPU 计算模块只占 Meteor Lake 总硅面积的一小部分。只有 CPU 模块采用 Intel 4 制程节点。基础模块（base tile）被认为是一种有源中介层，采用成本更低、为 Foveros 优化的 Intel 7 变体节点。既然英特尔以 Foveros 之名宣传，这个基础模块理应是有源的，但看来英特尔把它的绝大部分做成了无源，因为有源元件似乎都在其他小芯片上。我们能为这个模块指认的唯一功能就是供电、电容以及连接各小芯片。这颗芯片上最大的裸片是「SOC」模块。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/549956c7-28a5-494c-af1a-09992df774e2_1024x440.jpeg)

我们认为 SOC 模块是现有 CPU 裸片上的 IP 与 PCH（芯片组）的组合。Meteor Lake 不再有 PCH/芯片组。目前 PCH 采用 14nm 级制程节点生产，以此降低附加 IP 的成本。Alder Lake 移动版的 PCH 为 54mm²，包含诸如更多 PCIe 通道、USB 端口、SATA 所需的 IO、英特尔管理引擎（Management Engine）以及 Wi-Fi 所需的数字逻辑等 IP。我们相信这些都会纳入 SOC 模块。此外，目前位于 CPU 上的各种其他逻辑也可以移过去。Alder Lake P 左侧整个非核心（uncore）区域（TB4、显示 PHY、PCIe PHY、数字控制逻辑、图像处理单元、GNA AI 加速器、系统代理与内存控制器）占 55.9mm²。这部分 IP 的大多数将移到 SOC 模块，少量 IP 移到 10mm² 的 IO 模块。

总体算下来，我们认为 54mm² 的 14nm 与 ~40mm² 的 uncore Intel 7 硅将合并到 SOC 裸片上。芯片组部分会有一些冗余面积，但英特尔很可能还会增强其中一些 IP 模块。即便采用稍旧的节点，所有这些 IP 也能妥妥装进实测 ~94.9mm² 的 SOC 模块。英特尔可以再次使用 14nm 或 16nm 级节点，但有传言称他们可能为这个模块采用台积电 N6 节点。如果 SOC 模块上如一些传言所说，包含用于联网待机（connected standby）的低功耗 Atom 岛、媒体复合单元和 VPU，后者就说得通了。若这些 IP 出现在 SOC 模块上，很可能意味着 Meteor Lake 拥有新的电源状态和睡眠状态，有望大幅省电。编者按 2022/6/3：我们可以确认它采用的是台积电 N6 制程节点。

至于 10mm² 的 IO 模块，关于哪些 uncore IP 位于此处，我们听到了相互矛盾的传言。一些业内人称 Thunderbolt 4 和显示引擎移到了那里，另一些人则说内存控制器在这里。两种可能都存在。4 个 Thunderbolt 接口加显示引擎在 Alder Lake P 上约 20mm²。Alder Lake P 支持 DDR4、DDR5、LPDDR4x 和 LPDDR5，占 16.7mm²，其中约 6.8mm² 为 IO PHY + 互连、9.9mm² 为内存控制器。

这两个 IP 模块无论哪个塞进 10mm² 的 IO 模块都很紧张，但先进封装大幅提升 IO 密度、加上对 IP 更优化的制程节点可以解决这一问题。此外，英特尔很可能砍掉 DDR4 和 LPDDR4x 支持，能省一些面积。Alder Lake M 有 2 个 Thunderbolt 接口，而 Alder Lake P（实测）有 4 个。英特尔可以在 Meteor Lake M 上保留 2 个，Meteor Lake P 也降到 2 个。有传言称 IO 模块采用台积电制程节点，但我们对此还不确定。台积电用量如此戏剧性的增长令人难以置信，但并非不可能。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9454a04f-cb25-4050-aa02-8c3f08d98440_891x1024.jpeg)

至于 GPU，英特尔表示 Meteor Lake 将拥有 96EU 到 192EU 的图形。我们认为已展示的 Meteor Lake 包含 64EU 或 96EU。GPU 驱动代码似乎表明有效配置为 64EU、128EU 和 192EU，而英特尔的幻灯片显示 96EU 和 192EU。英特尔如何做到 192EU，稍后详述。在 Alder Lake 上，96EU 加 2 个媒体引擎在 Intel 7 节点上共 42.5mm²。随着叠加英特尔 DG2 Alchemist GPU 上出现的各种架构变化——AV1 编码支持、指令缓存从 48KB 增加到 96KB、向量寄存器堆从 28KB 增加到 32KB、浮点与整数 ALU 的专用发射端口、RT 硬件以及 1024 位矩阵引擎——这个面积还会进一步增长。

乍看这是不可能完成的任务，但 SemiAnalysis 可以确认，英特尔 Meteor Lake 的 GPU 模块采用了台积电的 N3B 节点。虽然我们认为这适用于所有 GPU 模块，但可能仅限 192EU 模块。如果 64/96EU 模块实际上用的是 N5/N4 而非 N3B，那么媒体引擎很可能就得放在 SOC 模块上。经过收缩，64/96EU 有可能装进 ~23mm²。N3B 相对台积电 N5 是可观的收缩，而 N5 本就比 Intel 7 密得多。有人可能会问，台积电为什么要把最先进节点的晶圆配给给英特尔，但这说得通。去年我们就深挖过[这一决定，以及英特尔将在台积电代工哪些基础 IP](https://semianalysis.substack.com/p/tsmc-wants-to-make-intel-dependent?s=w)。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/6f711f68-2e10-405b-8d76-840253593b9d_1024x299.jpeg)

这是一张示意图，展示英特尔如何在 Foveros 中介层尺寸允许的范围之外大幅扩展 GPU。正如我们在[先进封装深度解析](https://semianalysis.substack.com/p/advanced-packaging-part-2-review)中所解释的，Foveros Omni 允许悬垂（overhang）以及其他封装增强，尤其是在供电和设计灵活性方面。这将是一种与标准 Foveros（芯片-晶圆流程）不同的封装流程，而 Foveros Omni 似乎无法走那条流程。英特尔此前表示 Foveros Omni 将于 2023 年投产，而且是一款客户端移动产品。

> 我们的首款 Foveros Omni 产品将是移动细分市场的客户端产品。
>
> Babak Sabi，英特尔封装/测试技术开发高级副总裁兼总经理

就 Meteor Lake 的上市节奏而言，这说得通。Meteor Lake 整体于 2022 年开始投产，但那不代表每个变体。OEM 的朋友告诉我们，他们会先拿到 GPU 性能较低的移动 CPU，年内晚些时候会有 GPU 性能更高的移动 CPU。Omni 很可能留给与它共享许多系统架构细节的 Arrow Lake SOC。我们将在仅限订阅者的章节进一步讨论 Meteor Lake 与 Arrow Lake 的发布与爬坡。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

借助 Foveros Omni，英特尔可以设计一颗执行单元更多的大 GPU，并装进同一个 Meteor Lake P 封装。这颗 GPU 将用铜柱直接从基板供电，并用塑封料辅助结构完整性。这种先进封装方法让英特尔可以在合理的地方销售更小、更便宜的 GPU，而在想升级到更高性能水平时，无需重新设计那么多硅。它需要重新设计封装工艺流程、GPU 模块和基板，但比全部推倒重来便宜得多。Foveros Omni 也可能成为扩展 CPU 核心数的手段，但我们没有听到英特尔打算如何超越 2P+8E 核心的任何消息。我们确实知道英特尔计划在移动和桌面都推出更高核心数的变体。

我们从英特尔 Vision 活动上捕捉到的最后一条信息与 Meteor Lake 的最终封装有关。我们拍了 Meteor Lake 背面的照片。照片相当无聊，就不折磨大家了，但从中能读出的细节很有意思。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/f9824e03-cb3f-46a7-864d-dee94ead30d0_1023x218.jpeg)

首先，Meteor Lake 的 M Type 4 封装小得多。这很可能是因为英特尔在设计上追求小得多的外形尺寸。英特尔过去曾表示 Meteor Lake 的功耗范围从 5W 一直到 125W。目前 Alder Lake 声称在 Type 4 封装中可低至 9W，但我们还没见过按此配置出货的设备。

除了压缩 X 和 Y 尺寸，我们认为英特尔也大力压缩了 Z 轴高度。凭借这种高密度封装设计，x86 架构上 5W 到 10W 级别、又薄又强的设备终于有望成真。Meteor Lake M 封装的焊盘数显著多于 Alder Lake M。这可能是因为 IO 更多以及预留/未用，但那不是唯一的解释。我们的朋友 [Angstronomics](https://www.angstronomics.com/) 向我们解释：更薄、更密的封装需要更多焊盘，因为没有那么多空间合并供电与地，于是需要更多专用焊盘分别给裸片各区域供电。更紧的凸点间距也意味着更小的焊料焊盘、更小的表面积和更低的单焊盘电力传输能力，因此需要更多焊盘。

总体而言，Meteor Lake 是一个有意思的架构与设计。它为英特尔创下多个第一：大规模量产的 Foveros（抱歉，Lakefield 和 Ponte Vecchio 不算数）、通过 Intel 4 工艺用上 EUV，以及采用台积电 N3B 制程节点。它标志着英特尔系统架构的彻底重新设计，并将在 Arrow Lake 等未来架构中延续。小芯片（tile）架构帮助英特尔完全独立地验证和开发各部分 IP，甚至可以按产品定位和时间表随时更换 IP，正如我们在 GPU 上的讨论。

这次 Meteor Lake 分析最具突破性、或者说最令人失望的一点是：Intel 4 相对 Intel 7 似乎只有不到 40% 的面积缩减（密度提升 1.67 倍）。虽然 SRAM、逻辑和模拟电路在不同制程节点间的收缩速率本就差异很大，但即便是我们能认定为完全相同的那些最小子单元，也远达不到传统完整节点的理论缩放。如前文所示，SRAM 占比高的 IP（如 256KB L2 SRAM 模块）的面积似乎只缩减了 26.5%（密度提升 1.36 倍）。

根据英特尔向 VLSI [提交](https://twitter.com/IanCutress/status/1521495841332203529?s=20&t=bRDGUNUYDgaSBEBo0EzJ3g)的论文，Intel 4 具有 50nm 栅极间距、30nm 鳍片间距、40nm 最小金属间距、16 层金属、低层金属采用增强铜以降低线路电阻，以及 8 种 VT 选项（4N+4P）。高密度 SRAM 单元面积在 Intel 4 上为 0.024μm²，相比之下台积电 N5 为 0.021μm²、Intel 7 为 0.0312μm²。即使按官方口径，英特尔的 SRAM 密度仍落后于台积电推出已两年半的 N5 工艺。英特尔的高密度 SRAM 单元只实现了 23.08% 的面积缩减（密度提升 1.3 倍）。

SRAM 微缩的难题也并非英特尔独有。SRAM 微缩不佳的一个具体例子是台积电 N5 工艺：台积电给出的 SRAM 缩放为 1.35 倍，而纯逻辑为 1.8 倍。SRAM 微缩的失灵对[整个行业有着可怕的隐含影响](https://semianalysis.com/apple-a14-die-annotation-and-analysis-terrifying-implications-for-the-industry/)。尽管 Intel 4 的实际密度看起来不是一次完整收缩，但它仍领先于[台积电与苹果从 N7 到 N5 实现的 1.49 倍](https://semianalysis.com/apples-a14-packs-134-million-transistors-mm2-but-falls-far-short-of-tsmcs-density-claims/)，以及台积电与英伟达从 N7 到 N5 实现的 1.5 倍。因此，在 [SRAM 微缩难题的大背景下](https://semianalysis.com/apple-a14-die-annotation-and-analysis-terrifying-implications-for-the-industry/)，英特尔的这次收缩确实算得上完整节点级缩放。不过 Intel 4 这个工艺命名有点尴尬，因为台积电 N5 的高密度 SRAM 相对 Intel 4 实际有 1.14 倍的密度优势。

我们想讨论的最后一件事是爬坡时间表与规模、相对 AMD Phoenix 和 Strix 的竞争定位，以及与 Meteor Lake 及其继任者 Arrow Lake 相关的制造成本。这些将在仅限订阅者的章节完成。[Locuza](https://twitter.com/locuza_) 与 SemiAnalysis 完全没有广告、独立运营，直接依靠我们的订阅者和咨询项目支持，所以欢迎订阅我们中的任何一位，或者两位都订。测量与面积方面的工作大部分由 [Locuza](https://twitter.com/locuza_) 完成，请在 [Twitter](https://twitter.com/locuza_) 上关注他、订阅他的 [YouTube](https://www.youtube.com/channel/UCaFk_ygFCffeQhYouGCcAkQ)，并在 [Patreon](https://www.patreon.com/locuza) 上给他打几块钱支持他。

[分享](https://newsletter.semianalysis.com/p/meteor-lake-die-shot-and-architecture?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[立即订阅](https://newsletter.semianalysis.com/subscribe?)
