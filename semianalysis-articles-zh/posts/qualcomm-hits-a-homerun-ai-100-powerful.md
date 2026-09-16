---
title: "高通打出一记全垒打：AI 100——面向边缘的强大 AI 推理加速"
title_en: "Qualcomm Hits a Homerun AI 100 - Powerful AI Inference Acceleration For the Edge"
date: 2021-06-17
source: https://newsletter.semianalysis.com/p/qualcomm-hits-a-homerun-ai-100-powerful
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 高通打出一记全垒打：AI 100——面向边缘的强大 AI 推理加速

> 原文：[Qualcomm Hits a Homerun AI 100 - Powerful AI Inference Acceleration For the Edge](https://newsletter.semianalysis.com/p/qualcomm-hits-a-homerun-ai-100-powerful) · SemiAnalysis

高通（Qualcomm）的 AI 100 是一款面向边缘（edge）的 7nm AI 推理加速 ASIC。他们为这款产品造势已有一段时间，而最近在 Linley 大会上又披露了更多细节。其两大主打卖点是每瓦性能和延迟。在 AI 链条的这两个环节上，高通相信自己能以巨大优势击败 Nvidia 和基于 CPU 的方案。此外，他们还凭借真正过硬的软件支持，从 AI ASIC 阵营中脱颖而出。据 SemiAnalysis 了解，软硬件的这一组合已为高通赢得一家「Super 7」超大规模云厂商的订单，外加边缘市场的一连串胜利。

高通已多次申明，他们只瞄准推理市场，将完全放弃训练。他们希望无处不在地渗透边缘计算，并相信这是推理工作负载的头号目标市场。尽可能贴近数据产生的源头，是压低任何 AI 方案总拥有成本（TCO）的正道。高通设想 AI 100 同样可用于数据中心，与 5G 边缘盒子并肩作战，并遍布整个物联网（IoT）基础设施空间。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/e0c42253-de92-4287-a811-50819c686139_1023x491.png)

在数据中心侧，自然语言处理（NLP）和深度学习推荐网络（DLRN）是高通的主攻方向。许多初创公司喜欢吹嘘图像识别性能，但那些通常是参数极少的微小、简单模型。AI 推理的爆发式增长将主要来自 NLP 和推荐引擎中的巨型模型。[Facebook 最近预览了其新一代 DLRN，使用 12 万亿参数，比 DeepMind 的 GPT-3 多出 68.6 倍。](https://arxiv.org/abs/2104.05158) 这种量级的巨型模型将越来越常见，AI 领军者们也会继续推大模型规模。一颗只能跑小网络的推理芯片，在巨型 NLP 和 DLRN 推理面前毫无用处。

在智能边缘方向，高通瞄准智慧城市、零售、安防、制造和交通管理。这是一大类会产生海量数据并要求本地处理的用例。这些用例普遍对低延迟有要求，而这正是高通相对 GPU 的最大优势之一。

在 5G 基础设施方向，高通瞄准 RAN 基础设施设备和 5G 基站。一大批计算密集型算法都可以卸载到神经网络上：辅载波预测、天线倾角调整、小区切换、链路自适应、C-RAN 中的传输优化、干扰管理以及违规无人机检测，都是正在积极推进的用例。随着 2022 年高通的基站和天线产品组合日趋完整，高通将在 RAN 基础设施市场为 AI 100 发起强攻。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c15fd240-9906-411a-add6-72c98867ba98_1023x575.png)

就已公布的性能而言，高通只展示了 ResNet50 和 SSD-ResNet34——鉴于他们大谈在大型网络上的性能，这颇为令人失望。在小型网络上击败 Nvidia 的公司早已一抓一大把，高通本应展示更大网络上的性能。好在高通告诉我们，他们将在 8 月的 MLPerf 提交中展示 DLRN 和 NLP 模型。

尽管每瓦性能的营销话术与用例营销之间存在巨大落差，MLPerf 基准测试确实显示 AI 100 的能效比 Nvidia 的 GPU 高出 2 至 4 倍。蓝色阴影区域包含的是系统级功耗，而不只是图中灰色部分所示的 ASIC 功耗。高通采用的 batch size 仅为 8，而 Nvidia 在其数据中使用的是 32。要实现最高的性能/瓦，batch size 是个关键区别：GPU 需要更大的 batch size 才能得到有效利用。图中没有体现的另一点是，AI 100 的每次推理完成时间是在低得多的延迟下达成的。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/b9524859-2f54-417e-8709-1d7f17b2a8dd_2000x1145.png)

Cloud AI 100 提供 3 种外形规格，性能、功耗和目标用例差异极大。服务器级（server class）采用传统 PCIe 半高半长（HHHL）外形。不少其他推理加速器以及服务器领域的众多其他 PCIe 设备都采用这一规格，因此实施阻力极低——不需要任何外接供电，甚至不需要新的服务器设计。另外两种是符合开放计算项目（Open Compute Project）标准的双 m.2 卡，更适合本地部署的边缘应用。每种方案的内存容量和性能各不相同，以更好匹配其目标市场。Cloud AI 100 支持种类繁多的主机方案：从高通自家的 5G SoC，到 AMD 和 Intel 主机，后续还将支持其他 Arm 厂商的服务器与边缘芯片作为主机。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ab5b51b4-f6d3-4ee1-ac03-7fbcbc2636f0_1024x818.png)

Cloud AI 100 在裸片（die）上集成了大量 SRAM，每个 AI 硬件块 9MB。这是专用 AI 加速器中非常常规的设计，因为访问外存的功耗代价高得吓人。高通配备了 256 位总线、运行于 4266 MT/s 的 LPDDR4x，在内存带宽与能效之间取得了精妙平衡。这恰好与 Nvidia 基于 Xavier 的产品线所用的内存接口相同。尽管内存容量和带宽相近，高通却实现了高得多的性能。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/14ca2abe-d450-44c4-83a4-eceea7b24947_1024x576.png)

高通还支持一致性（coherent）多卡扩展。Cloud AI 100 可以通过 PCIe 交换机直接互通，无需绕道主机通信，从而节省功耗。许多面向推理的专用 AI SoC 无法以这种方式扩展，而这对体积急剧膨胀的 DLRN 尤其有利。技嘉（Gigabyte）演示了基于该平台可交付每秒 125 Peta-Operations 的算力。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/bc84ac78-4b9d-482d-8029-2209f6c845cd_1024x574.png)

强大的 AI 硬件并不稀罕，软件框架和架构好用、可互操作的硬件才难得得多。高通提供了开放的技术栈，支持所有主流框架和运行时。高通正在效仿 Nvidia 的策略：模型开箱即用、无需任何调整。他们提供自研的开放源代码工具，用于模型的优化与量化。这与 Nvidia 形成鲜明反差——后者同样拥有这类工具，却保持封闭，只限于自家硬件/软件方案使用。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/894b5904-8557-4526-9b30-eac578fdf35e_1024x575.png)

其开发流水线相当友好，在 AI 领域仅次于 Nvidia；而大规模部署与监控能力，在所有 AI 专用 ASIC（包括 Graphcore 在内）中堪称最佳。在 Cloud AI 100 上的开发流程，对该领域的大多数人来说都不会陌生。这与大多数其他 AI 专用 ASIC 相去甚远——后者需要定制的开发流水线，只支持现有框架和运行时的一小部分，而且往往对部署和负载监控几乎没有支持。Nvidia「极易开发」这一最大优势，正在受到挑战。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/47bebd15-294e-4467-91cb-36eb5f47dff8_1024x575.png)

高通的推理方案将高能效、高性能与低延迟结合在一起，构成一套极具说服力的硬件方案。干净、设计精良的软件工具帮助他们从一众竞争者中脱颖而出，并将在今年晚些时候开始赢得强劲的市场增长。高通似乎已做好准备，在蓬勃发展的 DLRN 和 NLP 推理市场中拿下大量份额。他们可以发挥自己在边缘和 5G 上的功底，为边缘 AI 推理提供最佳的整体方案。随着该产品逐步通过车规认证、高通的 ADAS 方案不断完善，Cloud AI 100 也将进军汽车领域。高通凭借 Cloud AI 100 打出了一记全垒打，因为他们真正吃透了软硬件协同设计的要义。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

[分享](https://newsletter.semianalysis.com/p/qualcomm-hits-a-homerun-ai-100-powerful?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[发表评论](https://newsletter.semianalysis.com/p/qualcomm-hits-a-homerun-ai-100-powerful/comments)

*本文最初于 2021 年 6 月 17 日发布于 [SemiAnalysis](https://semianalysis.com/qualcomm-hits-a-homerun-ai-100-powerful-ai-inference-acceleration-for-the-edge/)。*

*SemiAnalysis 的客户及员工可能持有本文所提及公司的仓位。*
