---
title: "特斯拉 Dojo——独特的封装与芯片设计带来相对竞争 AI 硬件一个数量级的优势"
title_en: "Tesla Dojo - Unique Packaging and Chip Design Allow An Order Magnitude Advantage Over Competing AI Hardware"
date: 2021-08-20
source: https://newsletter.semianalysis.com/p/tesla-dojo-unique-packaging-and-chip
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 特斯拉 Dojo——独特的封装与芯片设计带来相对竞争 AI 硬件一个数量级的优势

> 原文：[Tesla Dojo - Unique Packaging and Chip Design Allow An Order Magnitude Advantage Over Competing AI Hardware](https://newsletter.semianalysis.com/p/tesla-dojo-unique-packaging-and-chip) · SemiAnalysis

特斯拉举办了 AI Day，披露了其软件与硬件基础设施的内幕。披露内容之一便是此前预告过的 Dojo AI 训练芯片。特斯拉宣称其 D1 Dojo 芯片具备 GPU 级算力、CPU 级灵活性，外加网络交换机级的 IO。[几周前，我们曾推测该系统的封装是台积电的集成扇出晶圆级系统（InFO_SoW）。](https://www.semianalysis.com/p/tesla-ai-day-supercomputer-chip-teaser)我们解释了这类封装的优势，也讨论了这颗巨型纵向扩展训练芯片所涉及的散热与功耗问题。此外，我们估计这种封装在性能上会胜过英伟达系统。从本次发布来看，这些推测似乎全部成立。今天我们将深入拆解本次发布的半导体细节。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/6b403d90-bfb7-4cc9-8e4c-f1479d0f54fc_1023x469.png)

在深入硬件硬菜之前，先聊聊评测基础设施。特斯拉在不断重训并改进其神经网络。他们对每一次代码改动做评测，看是否有提升。部署在车上的同款芯片，有数千颗部署在服务器中。他们每周运行数百万次评测。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/027b249a-c1e0-453e-b0e3-315b9f112959_1024x543.png)

多年来特斯拉一直在扩大其 GPU 集群规模。他们当前的训练集群，如果停掉所有真实工作负载、跑 Linpack 并提交给 Top500 榜单，将位列全球第 5 大超级计算机。但这样的性能扩展仍不能满足特斯拉的野心，于是数年前他们启动了自研芯片计划——Dojo 项目。特斯拉需要更高性能，以高能效、高性价比的方式支撑更大、更复杂的神经网络。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8dd67a30-f697-419d-a6da-7ca887f28fe5_1024x450.png)

特斯拉给出的架构方案是分布式计算架构。听他们讲细节时，这个架构与 Cerebras 非常相似。[我们在此分析过 Cerebras 晶圆级引擎及其架构。](https://semianalysis.substack.com/p/cerebras-wafer-scale-hardware-crushes)每种 AI 训练架构都是这种布局，但计算单元、网络与 fabric 的细节千差万别。这类网络最大的难题在于扩展带宽的同时保持低延迟。为了扩展到更大的网络，特斯拉尤其聚焦于后两点。这影响了他们设计的方方面面，从芯片 fabric 到封装。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1aa63a93-22f1-418c-ae45-575b2f98e454_1024x545.png)

功能单元的设计目标是 1 个时钟周期即可穿越，但又足够大，使同步开销和软件不至于主导整个问题。于是他们得到了一个几乎与 Cerebras 一模一样的设计：由高速 fabric 连接的单个单元组成的 mesh，功能单元间的通信 1 个时钟即可路由。每个单元拥有 1.25MB 的大容量 SRAM 暂存器（scratchpad），以及多个具备 SIMD 能力的超标量 CPU 核心和支持所有常见数据类型的矩阵乘单元。此外，他们还引入了一种名为 CFP8（可配置浮点 8 位）的新数据类型。每个单元可提供 1TFlop 的 BF16 或 CFP8 算力、64GFlops FP32，以及每方向 512GB/s 的带宽。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/baac7ac5-3e45-41ce-afc9-2ad41895f1e8_1024x530.png)

CPU 也绝非等闲之辈：4 发射宽度，向量流水线 2 发射。每个核心可承载 4 个线程以最大化利用率。遗憾的是，特斯拉选择了定制 ISA，而不是在 RISC-V 等开源 ISA 之上构建。这个定制 ISA 引入了转置（transpose）、收集（gather）、广播（broadcast）和链表遍历（link traversal）指令。

354 个功能单元组成一颗完整芯片，可达 362 TFlops 的 BF16 或 CFP8 算力、22.6 TFlops 的 FP32 算力。总面积 645mm^2，500 亿颗晶体管。每颗芯片的 TDP 高达惊人的 400W。这意味着其功率密度高于英伟达 A100 GPU 的大多数配置。有趣的是，特斯拉实现了 77.5M 晶体管/mm^2 的有效晶体管密度，高于其他所有高性能芯片，只有移动芯片和苹果 M1 能胜过它。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/00dd6cc5-e0b5-4a87-bec8-b3680dfd344c_1024x509.png)

基础功能单元另一个有意思的部分是 NOC 路由器。它在芯片内与芯片间的扩展方式与 Tenstorrent 非常相似。[链接是我们对该架构的分析。](https://semianalysis.substack.com/p/tenstorrent-wormhole-analysis-a-scale)特斯拉与其它口碑良好的 AI 初创公司殊途同归，并不令人意外。Tenstorrent 非常侧重横向扩展训练，而特斯拉也恰恰在此着力甚多。

片上，特斯拉拥有惊人的 10TBps 单向带宽，但这个数字在实际工作负载中意义有限。特斯拉相对 Tenstorrent 的一个巨大优势是芯片间带宽显著更高：576 条 112GTs 的 SerDes，合计 64Tb/s 即 8TB/s 的带宽。

我们不清楚特斯拉「每条边 4TB/s」的说法从何而来，更可能是 X 轴加 Y 轴各出这个数。先不管那张令人困惑的幻灯片，这颗芯片的带宽是疯了。目前已知外部带宽最高的芯片是最先进的 32Tb/s 网络交换芯片。特斯拉凭借海量 SerDes 和先进封装，把这个数字翻了一倍。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a1a6a1bb-069b-4577-bafe-fe10309cad1f_1024x458.png)

特斯拉将 Dojo 芯片的计算平面连接到接口处理器，接口处理器再通过 PCIe 4.0 连接主机系统。这些接口处理器还支持更高端口数（radix）的网络连接，作为既有计算平面 mesh 的补充。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/601ef750-e700-44f9-b23c-5533b135f2b9_1024x545.png)

25 颗 D1 芯片以「扇出晶圆工艺」封装为一个训练 tile。特斯拉没有确认这种封装就是我们在几周前推测的台积电集成扇出晶圆级系统（InFO_SoW），但考虑到疯狂的芯片间带宽，以及他们明确说了「扇出晶圆」，可能性极大。

特斯拉开发了一种专用高带宽连接器，在 tile 之间保住了片外带宽。每个 tile 拥有 9 PFlops 的 BF16/CFP8 算力和 36 TB/s 的 tile 间带宽。这远超 Cerebras 的晶圆外带宽，使特斯拉系统的横向扩展能力甚至胜过 Tenstorrent 这类专为横向扩展而生的设计。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ba113e8e-ed3d-4887-ab7a-337a61039820_1024x752.png)

供电方案同样独一无二、深度定制、令人惊叹。面对如此巨大的带宽和封装上超过 10KW 的功耗，特斯拉在供电上大胆创新，采用垂直供电。定制的电压调节器直接回流焊在扇出晶圆上。电、热与机械接口全部与 tile 直接对接。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9dd235b1-94ae-47e8-bc9b-78ea71ffd208_1024x550.png)

即便芯片本身合计只有 10KW，整个 tile 似乎要 15KW。供电、IO 和晶圆走线同样在吞噬大量功率。电从底部进，热从顶部出。对特斯拉而言，扩展的基本单位不是芯片，而是 25 芯片的 tile。在单位性能和纵向扩展能力上，这个 tile 远超英伟达、Graphcore、Cerebras、Groq、Tenstorrent、SambaNova 或其他任何面向 AI 训练的初创公司的任何产品。

这一切听起来像天方夜谭，但特斯拉声称实验室里已有 tile 在真实 AI 网络上以 2 GHz 运行。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/0f0a0d1c-e75b-43ed-93f1-2feaf6e57b4e_1024x689.png)

向数千颗芯片扩展的下一步是服务器级。Dojo 以 2 × 3 tile 配置纵向扩展，一个服务器机柜容纳两套这样的配置。在家自己数的读者：每机柜共 12 个 tile，合计 108 PFlops。每服务器机柜超过 100,000 个功能单元、400,000 个定制核心、132GB SRAM——这些数字令人窒息。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/03bde3cd-6613-4420-8885-c7abeed46a35_1023x439.png)

特斯拉的 mesh 在机柜之上还在继续扩展。芯片之间的带宽没有分界。这是一个拥有疯狂带宽的同构芯片 mesh。他们计划扩展到 10 个机柜、1.1 Exaflops。1,062,000 个功能单元、4,248,000 个核心、1.33TB SRAM。

我已经口水直流了。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/f4a731a4-88d2-475e-993c-15cfcec01da9_1024x806.png)

软件方面同样有意思，但今天我们不会挖得太深。他们声称可以对其进行虚拟切分，并称软件能无缝扩展到任意集群规模的 Dojo 处理单元（DPU）之上。Dojo 编译器可以处理细粒度并行，把网络映射到硬件计算平面上。它通过数据模型图并行（data model graph parallelism）实现这一点，同时还能做优化以减少内存占用。

模型并行可以轻松跨越芯片边界，解锁数万亿乃至更多参数的下一代 AI 模型。大批量（batch size）甚至都不再需要。他们无需依赖手写代码就能在这个巨型集群上跑模型。

总结一下：特斯拉宣称，在与英伟达 GPU 成本对等的情况下，他们可以实现 4x 性能、1.3x 的每瓦性能，以及占地面积仅为 1/5。特斯拉的 TCO 优势几乎比英伟达 AI 方案好一个数量级。如果他们的说法属实，特斯拉在 AI 硬件与软件领域技压了所有人。我持怀疑态度，但这同时也是硬件极客的美梦。SemiAnalysis 正努力让自己冷静下来，告诉自己：等它真正部署到生产环境再下结论。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

[分享](https://semianalysis.substack.com/p/tesla-ai-day-supercomputer-chip-teaser?utm_source=substack&utm_medium=email&utm_content=share&action=share&token=eyJ1c2VyX2lkIjoyMTc4MzMwMiwicG9zdF9pZCI6Mzk2MDc4NTgsImlhdCI6MTYyOTQ0NDMwOSwiaXNzIjoicHViLTMyOTI0MSIsInN1YiI6InBvc3QtcmVhY3Rpb24ifQ.ZGWDr02AG9si-HQAWkwHpmun8ugcaY7OR_nQ6wJtV4M)

[发表评论](https://semianalysis.substack.com/p/tesla-ai-day-supercomputer-chip-teaser/comments)

*本文最初于 2021 年 8 月 20 日发布于 [SemiAnalysis](https://semianalysis.com/tesla-dojo-ai-super-computer-unique-packaging-and-chip-design-allow-an-order-magnitude-advantage-over-competing-ai-hardware/)。*

*SemiAnalysis 的客户及员工可能持有本文所提及公司的仓位。*
