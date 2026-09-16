---
title: "苹果 A15 裸片图与标注——IP 模块面积分析"
title_en: "Apple A15 Die Shot and Annotation - IP Block Area Analysis"
date: 2021-10-01
source: https://newsletter.semianalysis.com/p/apple-a15-die-shot-and-annotation
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 苹果 A15 裸片图与标注——IP 模块面积分析

> 原文：[Apple A15 Die Shot and Annotation - IP Block Area Analysis](https://newsletter.semianalysis.com/p/apple-a15-die-shot-and-annotation) · SemiAnalysis

TechInsights 发布了 A15 的裸片图（die shot），在 SkyJuice 的协助下，我们今天对其进行分析。裸片总面积显著增大，从 87.76mm^2 增至 107.7mm^2，晶体管数量从 11.8B 增至 15B。苹果最初的官宣数据[并不那么亮眼，最令人失望的是 CPU 性能提升的缺位。](https://semianalysis.com/apple-cpu-gains-grind-to-a-halt-and-the-future-looks-dim-as-the-cpu-engineer-exodus-to-nuvia-and-rivos-impact-starts-to-bleed-in/)尽管如此，这一代仍有许多变化。[AnandTech](https://www.anandtech.com/show/16983/the-apple-a15-soc-performance-review-faster-more-efficient) 已完成对 A15 SoC 的初步评测，结合裸片分析可以挖掘出许多有意思的细节。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/f8a400a0-d2c1-4525-bd87-84754b56be71_1023x749.jpeg)

首先可以确认的细节是制程密度没有变化。单个 SRAM 单元保持不变，LPDDR4x PHY 的尺寸也完全相同。这基本可以确认苹果使用的是 N5P，而非某些人猜测的 N4 制程。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/7351f125-2d7d-4b3b-8267-2351a2a445c0_1024x517.png)

裸片总面积增长 22.8%，但各 IP 模块的增幅各不相同。共享级缓存是面积增长的最大单一贡献者。ISP 看起来也经过了大幅修订，但我们没有这里的测量数据。NPU 仍为 16 核心，但核心和共享逻辑在架构上有所改动，带来了可观的性能提升。尽管大核心的 IPC 增益缺失，大核心本身仍有一些变化。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/daae90a9-1030-40b3-b200-6f57dd8c31f7_1024x564.png)

尽管这是苹果有史以来最小的 IPC 增幅，这个核心显然经过了重新架构。两处最大的变化与 MMU 和缓存有关。布局明显不同，核心+L1 面积增加了 15.26%。[AnandTech](https://www.anandtech.com/show/16983/the-apple-a15-soc-performance-review-faster-more-efficient) 发现了 L1 缓存的一个有趣变化。

> 在性能核上，我还观察到 L1 速度的一些变化：只要缓存行位于同一页面内，它似乎能够以 1 个周期的延迟访问缓存行；而在 A14 上，同类访问需要 3 个周期。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ad4f9108-786c-4dea-8eef-3ba5de195938_1024x910.png)

共享 L2 缓存从 8MB 增至 12MB。尽管核心数量只有一半，这与 M1 的容量相同。[AnandTech](https://www.anandtech.com/show/16983/the-apple-a15-soc-performance-review-faster-more-efficient) 发现其访问延迟从 16 个周期增加到 18 个周期。容量与延迟之间的这一取舍看起来非常值得。共享 L2 缓存块的面积相较 A14 增长了 52%。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/3a8d237f-621e-4709-8439-9ac208a763dd_996x458.jpeg)

小核心 Blizzard 的面积增长了 18.6%，而性能提升为 23%。L2 缓存维持 4MB，但微增了 2.5%。苹果的 Blizzard 核心如今的性能已可与两年前安卓 SoC 中的大核心 A76 比肩。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/dfba3b85-f20c-4bbe-8b71-8f92080b47a6_1024x339.jpeg)

苹果在 A15 上真正下功夫的是 GPU。苹果发布了[这支视频](https://developer.apple.com/videos/play/tech-talks/10876)，详述了部分架构变化，其中包括将 M1 GPU 核心中 FP32 ALU 数量翻倍。苹果还引入了可节省显存与带宽的有损可渲染纹理（lossy renderable textures）、对稀疏深度与模板纹理的支持，以及新的 SIMD shuffle 和 fill 指令。尽管有这么多变化，GPU 核心的面积只增加了 4.4%。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c7d17b1a-0011-4ca0-ad15-5dba8e0fe543_1024x760.jpeg)

整个 GPU 的面积增长了 30%，主要来自第 5 个 GPU 核心以及共享逻辑的变化。即便第 5 个核心被禁用，仍有可观的性能提升。在内存带宽毫无增加的情况下，新的更大规模 GPU 实现了巨大的性能提升。苹果看来正在采取与 AMD Infinity Cache 类似的策略。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d78add60-c77f-4694-8a4e-5bd6dac3b02d_1024x568.jpeg)

面积增长最大的单一贡献者是系统缓存，从 16MB 翻倍至 32MB。这有助于持续喂饱 A15 的各个 IP 模块。本文只是 SkyJuice 裸片分析的一个简短摘要。关于这张裸片图，各位还注意到了什么？

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

[分享](https://newsletter.semianalysis.com/p/apple-a15-die-shot-and-annotation?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[发表评论](https://newsletter.semianalysis.com/p/apple-a15-die-shot-and-annotation/comments)

*本文最初于 2021 年 9 月 30 日发布于 [SemiAnalysis](https://semianalysis.com/china-has-built-the-worlds-most-expensive-silicon-carbide-fab-but-numbers-dont-add-up/)。*

*SemiAnalysis 的客户及员工可能持有本文所提及公司的仓位。*
