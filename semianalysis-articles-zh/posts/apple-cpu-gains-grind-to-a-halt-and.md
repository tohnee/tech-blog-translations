---
title: "苹果 CPU 性能提升陷入停滞、前景黯淡——CPU 工程师外流至 Nuvia 与 Rivos 的影响开始显现"
title_en: "Apple CPU Gains Grind To A Halt And The Future Looks Dim As The Impact From The CPU Engineer Exodus To Nuvia And Rivos Starts To Bleed In"
date: 2021-09-14
source: https://newsletter.semianalysis.com/p/apple-cpu-gains-grind-to-a-halt-and
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 苹果 CPU 性能提升陷入停滞、前景黯淡——CPU 工程师外流至 Nuvia 与 Rivos 的影响开始显现

> 原文：[Apple CPU Gains Grind To A Halt And The Future Looks Dim As The Impact From The CPU Engineer Exodus To Nuvia And Rivos Starts To Bleed In](https://newsletter.semianalysis.com/p/apple-cpu-gains-grind-to-a-halt-and) · SemiAnalysis

多年来，苹果一直因其面向消费级工作负载的最佳 CPU 核心而备受赞誉。它拥有迄今最高的每时钟周期性能，而其能效则建立在可与 AMD 和英特尔当前最强 CPU 比肩的性能之上。这背后是长达十年、每年一次架构更迭带来的狂飙式提升。

如今到了 A15，这些提升明显放缓。在新款 iPhone 发布会上，苹果对 A15 的对比说法总体上相当含糊。他们没有像往常那样与上一代对比，而是选择与语焉不详的「竞争对手」比较。这固然好看，但距离高通、三星（Samsung）和联发科的新芯片组发布只剩几个月了。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/426565e0-52bf-484e-b8d8-a0c943e31f18_1024x576.jpeg)

快速过一遍规格：CPU 采用 2+4 核大小核设计；GPU 则视普通版 iPhone 还是 iPhone Pro/iPad Mini 的删减策略，配 4 核或 5 核。官方宣称 CPU 比竞争对手快 50%，GPU 则视 4 核或 5 核版本宣称快 30% 或 50%。NPU 仍是 16 核，算力从 A14 的 11 TOPs 提升到 15.8 TOPs。视频编码器和解码器是新的，我们希望它加入了 AV1 支持。新 ISP 支持更好的照片与视频算法。Pro 机型支持可变刷新率，因此很可能需要新的显示引擎。最后，系统缓存翻倍至 32MB——这大概率是为了喂饱 GPU 并节省功耗。SemiAnalysis 还判断苹果并未从 LPDDR4X 迁移到 LPDDR5。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/3cc6ccca-2fdc-47e8-83f1-191d491a6e74_1024x576.jpeg)

与上一代 A14 直接对比有不少困难，但 iPad mini 帮了我们一些忙。苹果宣称新款 iPad mini 的 CPU 比搭载 A12 的上一代 iPad mini 快 40%，GPU 快 80%。去年我们也不得不做类似的推算，因为搭载 A14 的 iPad Air 率先发布时，也只与同样搭载 A12 的上一代 iPad Air 对比。那次发布给我们留下了下面这段话。

> 这颗最新一代 A 系列芯片采用全新 6 核设计，CPU 性能提升 40%；并采用全新 4 核图形架构，图形性能提升 30%。

最值得注意的一点是：从 A12 到 A14 的 CPU 提升幅度，与从 A12 到 A15 的提升幅度完全相同。GPU 的提升倒相当可观，按计算为 38.5%，比 A13 和 A14 两代的提升加起来还要大。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/f2ab32e4-1fc2-4988-a78c-3df57ca173f7_1023x343.png)

尽管晶体管数量从 11.8B 暴增至 15B，这些性能提升总体上仍相当寒酸。再者，明年的 [A16 将采用 N4 制程而非 N3](https://semianalysis.substack.com/p/qualcommmediatek-will-beat-apple)，提升预计会继续放缓。[制程技术尤其 SRAM 的放缓](https://semianalysis.com/apple-a14-die-annotation-and-analysis-terrifying-implications-for-the-industry/)，将成为砸向整个行业的一记重锤。苹果显然把晶体管预算投到了 SoC 中非 CPU 的部分。固定功能模块与异构计算为王。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9d32b3d4-1c3f-44df-89e9-e6306d368629_1024x676.png)

看起来苹果这一代并没有对 CPU 做太大改动。SemiAnalysis 认为，下一代核心因 CPU 工程师资源问题，已从 2021 年推迟到 2022 年。2019 年，Nuvia 成立，随后以 $1.4B 被高通收购。苹果首席 CPU 架构师 Gerard Williams 以及数十位其他苹果工程师离职加入该公司。更近一些时候，SemiAnalysis 独家报道了 [Rivos Inc——一家由众多苹果资深工程师参与创办的高性能 RISC-V 初创公司](https://semianalysis.substack.com/p/rivos-inc-a-chip-off-the-old-block)。人才流失仍在继续，其影响将随时间推移愈发明显。当年苹果曾从英特尔等全行业公司虹吸资源，如今反噬似乎正在发生。

我们认为，苹果正是因为持续的人事变动而不得不推迟下一代 CPU 核心。他们没有采用全新 CPU 核心，而是使用去年核心的修改版。其中一项修改与 CPU 核心的 MMU 有关——这项工作原是为即将发布的、坊间俗称「M1X」的 Mac 芯片世代所做的。这一变化的部分原因与更大的内存容量以及虚拟化特性/支持有关。此外可能还有其他小改动，但我们需要拿到真机硬件才能分析。我们也不确定 Avalanche 和 Blizzard 究竟是下一代核心，还是当前经过修改的 Firestorm 与 Icestorm 核心。

无论 CPU 提升多么寒酸、核心架构是否推迟，苹果仍是每瓦特性能的领导者。但随着英特尔设计团队重新走上正轨、AMD 的执行近乎完美无缺、搭载 Nuvia 核心的高通即将携重锤入场，我们不确定这一领先能否保持。A11 到 A12 那一代（仅提升 15%）曾被视作苹果性能提升开始逼近渐近线，A13 到 A14（提升 8.3%）看起来更加疲弱，而如今 CPU 提升几乎归零——让我们祈祷 A16 能带来一次大规模架构革新吧。

编辑注：补充首发基准测试的统计数据，进一步印证本文观点。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/134fcad2-4be1-45bd-9239-470c60711261_1292x544.png)

续航提升大体与电池容量增幅相称。最亮眼的当然是 Pro 版 iPhone 的全新 LTPO 面板与 VRR。WiFi 流媒体续航也有提升，这表明 RF 技术栈的优化以及上文提到的媒体模块编解码器改进。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/350ec3b7-8755-4a2f-9406-775cef7246f3_1507x1200.png)

CPU 单线程整体提升 7.7%，大体与频率从 3GHz 提升至 3.23GHz 的增幅相当。部分项目的弱缩放向我表明 LPDDR5 可能确实缺席。其中部分动机可能是：翻倍的 LLC 已经够用，没必要为 LPDDR5 相比 LPDDR4x 多花约 30% 的成本。有些测试可能受益于 LLC 翻倍至 32MB，另一些则无法随频率完美扩展。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9d36f0f7-af3a-4938-a37d-55d593aabeba_739x498.png)

GPU 对比是 iPhone Pro Max 与上代 Pro Max 之比，对应 A15 完整的 5 核 GPU。性能提升约 50%，其中 SFFT 子项得分尤其有意思：150% 意味着每 GPU 核心的 ALU 数量翻倍；130% 已经相当接近，而多出的那 1 个 GPU 核心本身不足以解释这一成绩。他们很可能在 GPU 上采用了 2xFP32。

[关于 iPhone 13 卫星上网那条垃圾谣言，我们也想小小地扬眉吐气一下——我们当时就戳穿了它。](https://semianalysis.substack.com/p/no-the-iphone-13-does-not-have-satellite)

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

[分享](https://newsletter.semianalysis.com/p/apple-cpu-gains-grind-to-a-halt-and?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[发表评论](https://newsletter.semianalysis.com/p/apple-cpu-gains-grind-to-a-halt-and/comments)

*本文最初于 2021 年 9 月 14 日发布于 [SemiAnalysis](https://semianalysis.com/apple-cpu-gains-grind-to-a-halt-and-the-future-looks-dim-as-the-cpu-engineer-exodus-to-nuvia-and-rivos-impact-starts-to-bleed-in/)。*

*SemiAnalysis 的客户及员工可能持有本文所提及公司的仓位。*
