---
title: "Apple M2 裸片图与架构解析——成本大增与基于 A15 的 IP"
title_en: "Apple M2 Die Shot and Architecture Analysis – Big Cost Increase And A15 Based IP"
date: 2022-06-10
source: https://newsletter.semianalysis.com/p/apple-m2-die-shot-and-architecture
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# Apple M2 裸片图与架构解析——成本大增与基于 A15 的 IP

> 原文：[Apple M2 Die Shot and Architecture Analysis – Big Cost Increase And A15 Based IP](https://newsletter.semianalysis.com/p/apple-m2-die-shot-and-architecture) · SemiAnalysis

苹果在 WWDC 上发布了其集成 200 亿颗晶体管的新款 M2 SoC。遗憾的是，它在 CPU 等部分领域的性能提升相当有限。苹果的性能增益主要来自 GPU 和视频编辑方面。如果考虑到这款新 M2 随之而来的纯粹成本上升，以及距离 M1 发布已近 2 年的事实，其整体性能提升可谓[相当令人失望](https://semianalysis.com/apple-cpu-gains-grind-to-a-halt-and-the-future-looks-dim-as-the-cpu-engineer-exodus-to-nuvia-and-rivos-impact-starts-to-bleed-in/)。成本上升的情况与我们在 A16 上所写的类似——[由于物料清单（BOM）方面的顾虑，苹果被迫在产品线上分化 SoC 选择：Pro 版 iPhone 机型采用 A16，普通 iPhone 机型继续采用 A15](https://semianalysis.substack.com/p/as-moores-law-slows-apple-is-forced?s=w)。

今天，我们将讨论 M2 的架构以及苹果未来设计（包括 M2 Pro/Max 和 M3）的相关细节，这些内容并未在 WWDC 上提及。我们还将在 Locuza 的帮助下，对苹果发布的 M2 图像做一次裸片面积分析。如果你更愿意听而不是读，[我们制作了一期 YouTube 视频](https://www.youtube.com/watch?v=r1OBUIwS_Dc)。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8ba3c972-8372-453a-9a89-0dc8e7c2ad8b_1024x572.jpeg)

我们看到一些评论人士把 M2 称作 M1.5 或 M1+，这非常奇怪。这纯属无稽之谈。M1 除少数偏差外，大体上基于与苹果 A14 相同的 IP 模块。而代号为 Staten 的 M2，大体上基于代号为 Ellis 的 A15 的相同 IP 模块。这些代号都取自纽约一些最著名的岛屿，这也暗示了这些架构之间的紧密亲缘关系。性能提升方面的大量失望情绪，源于在距 M1 已近 2 年的间隔下，代际提升依然疲弱。许多人对 M2 抱有更高的期待。

我们[过去曾讨论过](https://semianalysis.com/apple-cpu-gains-grind-to-a-halt-and-the-future-looks-dim-as-the-cpu-engineer-exodus-to-nuvia-and-rivos-impact-starts-to-bleed-in/)，性能放缓很大程度上源于苹果向 [Nuvia 和 Rivos](https://semianalysis.com/apple-cpu-gains-grind-to-a-halt-and-the-future-looks-dim-as-the-cpu-engineer-exodus-to-nuvia-and-rivos-impact-starts-to-bleed-in/) 等公司流失了大批杰出工程师。近年来这种失血仍未停止，因为苹果的工作文化实在算不上最好，而其他公司——主要是 Google、Microsoft、Amazon 和 Meta 等超大规模云厂商——为了挖角人才开出的薪酬比苹果更高。最后，还有一批并非为钱所动的工程师也离开了。他们认为自己已经成功推动苹果摆脱英特尔（Intel）芯片、转向自研芯片。这些工程师同样转投行业其他地方他们眼中更有意思的项目，无论是超大规模云厂商还是传统公司。

这些人才流失最终导致 A15、M2 以及可能即将推出的 A16 的 CPU 增益都较为平淡。我们听说 A16 将不会采用下一代基于 Armv9 的核心，如果属实，这相当令人遗憾，因为苹果当年是第一个落地 Armv8 的厂商。我们听说这个下一代 Armv9 核心将只会出现在 M3 中——那将是苹果在台积电 N3 节点上的首款产品。苹果已经设计并流片了 M2 Pro 和 M2 Max，它们仍基于 N5 和 A15 基础 IP。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/69502024-a55e-4ceb-bbd4-0cf1193153d8_1024x421.jpeg)

让我们深入看看裸片图。苹果发布了 M1 和 M2 两款未标注的图像。图中显示 M2 为 141.7mm2，但我们认为苹果对裸片图像做了修改。这不会是第一次。苹果对 [M1 Max 也做过同样的事，隐藏了 M1 Ultra 所用的裸片间连接](https://twitter.com/dylan522p/status/1450286632729518089?s=20&t=rK10G4Q9PcTSeERJYRIRww)。他们还挪动了尺寸标注。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/21795c5c-b04c-43ab-87e4-1f26da858693_1024x331.png)

苹果的图像在 M2 上似乎同样比例失真。你可以辨认出本应在各芯片之间完全一致的 SRAM 单元和 PHY，并发现 M2 显得比它应有的尺寸更小。苹果公布的 M2 的晶体管密度看起来甚至高于 A15，这同样不合常理。由于分配给高密度 SRAM 单元的总面积更小、分配给 IO 及其他逻辑的总面积更大，M2 的密度本应更低。正因如此，Locuza 对 M2 裸片进行了缩放。缩放之后，SRAM 单元和相同的 PHY 与苹果在 M1 和 A15 上的情况对齐一致。苹果营销图像的这种古怪之处意味着，裸片按尺寸缩放后仍存在约 3% 的误差窗口。尽管存在误差范围，文中数字仍按实测值呈现。

接下来看看苹果把增加的裸片面积花在了哪里。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/5c08fac1-c4bf-4d5e-aebb-b598b87afdc9_1024x479.jpeg)

首先从苹果的 P 核（性能核）说起。它基于出现在 A15 中的苹果 Avalanche 核心，不过存在一些细微差异。这与 M1 Pro 和 M1 Max 的做法一脉相承——它们采用了经过修改的 Firestorm，通过实现更大的物理地址（PA）来支持更大的内存容量。基于 M 系列的核心还有一些其他修改，用于支持 macOS 中必须支持的多种页大小。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1b16a058-cf31-4482-995c-089932dd9d42_1024x123.png)

该核心本身比 M1 中的大 21%，比 A15 的大 7%。代际面积增长的大头在共享 L2 缓存：与 M1 和 A15 相比，它从 12MB 增加到了 16MB。AMX 单元在 A15 和 M1 上看起来也完全相同。共享逻辑平面也明显更大，这表明核心与 L2 缓存及系统级缓存（SLC）之间的带宽更高。总体而言，苹果在大 P 核上花费了 5.2mm2，但其性能提升主要来自时钟频率。IPC 的提升相当小，[各类评测已有记录](https://www.anandtech.com/show/16983/the-apple-a15-soc-performance-review-faster-more-efficient/2)。

一个非常有意思的变化是：与 M1 和 A14 中的 Firestorm 核心相比，A15 和 M2 所用 Avalanche 核心中的重排序缓冲区（ROB）看起来反而更小了。这一点尤其耐人寻味，因为苹果为了实现业界最宽、IPC 最高的核心，历来拥有业界最大的 ROB。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8a4f288b-769a-4098-9e3a-ec09f7acbfcf_838x404.jpeg)

从 CPU 角度看，E 核（能效核）是从 A14 到 A15 变化最大的部分，这一点在 M2 上同样成立。对苹果提供的裸片图缩放之后，A15 和 M2 的 E 核看起来几乎完全一致，这也是缩放准确的一个好迹象。苹果在 Mac 芯片上对 E 核很少修改或完全不修改，而针对那些改动，P 核则会做一些调校和不同的物理设计。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/45b9996e-e0fb-42a2-97c0-b72ce6dcf59f_1024x165.png)

关于 E 核这里没有太多可说的，它显然与 A15 的相同，而后者已经过[大量测试](https://www.anandtech.com/show/16983/the-apple-a15-soc-performance-review-faster-more-efficient/2)。E 核集群整体代际只增大了 1mm2，而整个 CPU 集群增大了 6.2mm2。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/4c373ad0-2ac1-4219-832a-75e037481764_1024x301.jpeg)

缩放后，GPU 单核心面积与 M1（128 ALU）相比也几乎相同。这一点非常有意思，因为 M1 正是在此处与 A14 分道扬镳的领域之一——尽管两者属于同一代，M1 的 GPU 却发生了架构变化。苹果此前就有 X 系列 SoC 相对 A 系列 SoC 做出变化的先例。例如多年前的 A6 和 A6X 就采用了不同的 GPU 架构。鉴于 M 系列 SoC 本质上只是 X 系列的更名，这一规律得到延续。这一代 GPU 核心本身似乎没有变化，但共享逻辑和杂项部分更大了，因此某些固定功能部分可能有所改动。主要变化在核心数量：苹果将其提升到了 10 核心 GPU。我们可以独家披露 GPU 的时钟频率，它从 1.27 GHz 提升到了 1.406 GHz。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ca212b72-2bc4-4b66-bf15-4c6670ff69dd_1022x164.png)

新 GPU 总共代际增加了近 7mm2。这是一次值得的性能提升，不过苹果表示在最大性能档位下功耗略有上升。而在相同功耗水平下，得益于更好的内存以及整体更宽/更慢的设计，苹果仍获得了可观的性能提升。我们这里也列出了 NPU 和 SLC 的数字。NPU 的数字看起来有点古怪，所以我们略过不谈。SLC 才是有意思的地方。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/3358b9e8-3339-45fc-874c-a12c2e650cb9_1022x272.jpeg)

每个 2MB 数据阵列（Data Array）在 M1、A15 和缩放后的 M2 裸片上大小基本一致，这合乎逻辑，也印证了我们基于相同 PHY 尺寸进行缩放的做法。从第一代到第二代 N5 制程节点，SRAM 并没有任何微缩。尽管如此，M2 上的 SLC 面积还是有所增长，很可能是为了给更大的 GPU 等各个 IP 模块提供更多带宽。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/b6272bad-2379-4e5e-b728-e3558b77affd_1024x208.jpeg)

最后一个要对比的 IP 模块是内存控制器 + PHY。为了支持 LPDDR5 6400，苹果显著增加了这里的面积。上图所示为 1 个单元，当然内存控制器包含多个通道。128 位 LP5 总线所占的总面积约为 14mm2，相比之下，采用 128 位 LP4X 的 M1 为 8.1mm2，采用 64 位 LP4X 的 A15 为 4.3mm2。从成本角度看，真正的要害在于 LPDDR5 6400 比 LPDDR4X 4266 贵得多。

这也是苹果在今年即将推出的 iPhone 上采取 A15/A16 产品线分化策略的重要一环。我们[在此](https://semianalysis.substack.com/p/as-moores-law-slows-apple-is-forced?s=w)写过这个决策。总体而言，苹果在 M2 上不得不应对类似的问题，这也正是他们继续保留基于 M1 的机型主打低端的原因。晶圆价格小幅上涨、裸片面积从 118.91mm2 增大到 155.25mm2，再加上更昂贵的内存，这套组合伤害不小。

最后一个我们没有显式测量的 IP 模块是大幅变大的媒体引擎，用于实现增强的媒体能力。苹果 M 系列是迄今为止最适合创意专业人士的芯片，这一点毫无疑问。如果你使用 Adobe 套件工作，M 系列芯片就是最佳之选。

如果你喜欢这项工作，请考虑订阅免费或付费新闻通讯。也请前往 [Locuza 的 Twitter](https://twitter.com/Locuza_)、[Patreon](https://www.patreon.com/locuza) 和 [YouTube](https://www.youtube.com/channel/UCaFk_ygFCffeQhYouGCcAkQ) 支持他的工作。

[分享](https://newsletter.semianalysis.com/p/apple-m2-die-shot-and-architecture?utm_source=substack&utm_medium=email&utm_content=share&action=share)
