---
title: "认识 NETINT：向字节跳动、百度、腾讯、阿里等出售数据中心 VPU 的初创公司"
title_en: "Meet NETINT: The Startup Selling Datacenter VPUs To ByteDance, Baidu, Tencent, Alibaba, And More"
subtitle: "视频编码 ASIC 对广告技术、云游戏、视频会议和 VDI 至关重要"
date: 2022-08-04
source: https://newsletter.semianalysis.com/p/meet-netint-the-startup-selling-to
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 认识 NETINT：向字节跳动、百度、腾讯、阿里等出售数据中心 VPU 的初创公司

> 原文：[Meet NETINT: The Startup Selling Datacenter VPUs To ByteDance, Baidu, Tencent, Alibaba, And More](https://newsletter.semianalysis.com/p/meet-netint-the-startup-selling-to) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**视频编码 ASIC 对广告技术、云游戏、视频会议和 VDI 至关重要**

NETINT 是你从未听说过的最成功的半导体初创公司之一，而且他们是在竞争惨烈的数据中心市场做到这一点的。2021 年，他们的芯片处理了超过 2,000 亿分钟的视频。NETINT 成立于 2015 年，目前已扩展到分布在温哥华、多伦多和上海的 160 名工程师。NETINT 是商用（merchant）视频编码 ASIC 领域的领导者。

如果这听起来有些耳熟——Google 也有一项类似的内部自研芯片项目，用于其内部工作负载，名为 [Argos](https://semianalysis.substack.com/p/google-new-custom-silicon-replaces)。我们[过去曾写过那款 ASIC](https://semianalysis.substack.com/p/google-new-custom-silicon-replaces)，以及 Google 如何在增强产品能力的同时[替换掉数百万颗 Intel CPU](https://semianalysis.substack.com/p/google-new-custom-silicon-replaces)。两家公司都已经在使用/出货其第二代视频编码 ASIC，即所谓 VPU（Video Processing Unit，视频处理单元）。

在进一步讨论 NETINT 的芯片方案之前，我们想先深入探讨一下视频内容、编码，以及正在以巨大力度推升这类半导体需求的格局变化。这不仅对半导体公司影响重大，对 Google、Amazon、Meta、字节跳动和 Netflix 这些公司的内容分发与广告网络同样影响巨大。

视频流媒体相关内容的人气正在爆发式增长，[占全部互联网流量的 80% 以上](https://www.fiercevideo.com/video/video-will-account-for-82-all-internet-traffic-by-2022-cisco-says)。在过去，制片厂创作内容，然后以少数几种格式处理、编码并分发内容。每份编码后视频的观众数量相对较多，因为观众可按需收看的电视频道数量有限。这些制片厂可以针对当时的交付方式——无论是有线电视还是 DVD——对内容的处理进行深度优化，以获得最高的视觉保真度。

网络在内容创作上一直在去中心化，消费者把更多时间花在用户生成内容（UGC）上。Google 凭 YouTube 引领了这股浪潮——YouTube 是用户生成内容的最大来源，用户每分钟上传超过 700 小时的 YouTube 视频。所有这些视频都必须由 Google 以多种格式处理和编码，才能分发给用户。其中涉及的处理和编码至关重要：要确保用户生成内容不违反服务条款、配上字幕，还要让视频可以基于其包含的内容被检索到，而不是仅依靠粗糙的标签和标题。

在优化视频质量与文件大小之间存在微妙的平衡。这种平衡之所以关键，是因为数据中心的[南北向带宽](https://www.fabricatedknowledge.com/p/r2-what-it-means-to-be-1-less-than)非常昂贵。如果编码方案在相同视频质量下能把文件再缩小哪怕 5%，一家大型内容分发网络就能省下数千万美元。

此外，许多消费者的网络连接条件差或有流量上限，因此视频必须以最适合其具体情况的尺寸和分辨率交付。如果没有提供分辨率、质量与带宽消耗的正确组合选项，用户可能会下意识地倾向于从另一家提供商获取娱乐内容。

Google 并非这个领域孤军奋战。Amazon 的 Twitch、Meta 的 Facebook Video 和 Instagram Reels、字节跳动的 TikTok 等公司的用户生成内容同样在爆发式增长。用户生成内容的单位内容观看时长明显更低。此外，每路视频流只有一个观众的内容形态也在快速发展。这些用例包括云游戏服务、虚拟桌面以及其他远程交互式计算环境。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/55b6d2d7-19d5-4170-a870-4ffb68590460_1558x791.png)

即使视频内容来自较为传统的制片厂、流媒体选项有限，内容分发网络仍可能需要对内容进行大批量的即时额外处理和编码。广告支持内容就是一个例子。包括 Netflix 在内的许多付费流媒体服务正在转向提供广告支持内容。

广告可能有各种不同的分辨率、尺寸和码率，未必与内容本身的格式匹配。投放广告的公司可能拥有自己的网络，如 Google 的 AdSense，但大多数公司必须依赖第三方广告交易清算机构。广告主会为更高的曝光率和转化率支付更多费用。广告要获得最大效果，就不能破坏用户的沉浸感。保持沉浸感包括匹配用户本来要观看的内容的分辨率和质量。每条广告都必须由内容网络进一步处理，否则其效果乃至最终收入都可能下滑。

广告与广告拦截手段也在进行持续的军备竞赛，YouTube、Twitch 等免费内容网络因广告拦截器蒙受了难以计数的收入损失。虽然这场军备竞赛一直此消彼长，但总体上广告拦截器占了上风，而击败广告拦截器唯一完全保险的方案，就是把广告直接编码进视频内容里。

按需广告市场高度动态化，包含基于时间和基于用户的定向投放。要实现广告收入和效果最大化，内容网络应当对内容流做拼接，并将针对该用户广告 ID 在需求竞价中售出的个性化广告编码进去。这是一个计算成本极高的处理步骤，用 CPU 和 GPU 无法经济地完成。

服务提供商的经济学是这些内容网络扩展能力的关键。Google 需要专用芯片才能在 YouTube 全面铺开 VP9，否则将需要[超过 1,000 万颗 CPU](https://semianalysis.substack.com/p/google-new-custom-silicon-replaces)。这正是 Google 自研方案与 NETINT 的 VPU 方案登场的地方。Google 只会服务自己的用例，而 NETINT 在其产品上的投入时间即使不比 Google 更长也至少相当，他们还服务于大得多的企业市场。因此，NETINT 收获了一大批重要客户，包括字节跳动、百度、腾讯、阿里、快手，以及一家规模相当的美国全球性平台。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/e34e9e55-6fd1-45b0-9107-0e4d8c5801e5_1521x750.png)

NETINT 的第一代 ASIC 名为 Logan，采用 TSMC 28nm 工艺。第二代名为 Quadra，采用 Samsung 14nm 工艺。他们保持 2 年一代的节奏，第三代 Mt. Augusta 将于 2024/2025 年出货。Quadra ASIC 拥有 4 条 PCIe 4.0 通道、外挂 DRAM，以及视频解码/编码、音频编码/解码、AI 推理、RISC CPU 和 2D 视频引擎的硬件 ASIC。最突出的能力是 AV1 和 H265/HEVC。NETINT 的对比测试一般使用 H265 和 AV1，因为在这两个编码格式下其 TCO 优势更大。

总体而言，ASIC 要想在目标工作负载上取得成功，需要提供一个数量级的更强能力。虽然他们的芯片在 H264 上也能带来有意义的优势，但只有在运用 HEVC 或 AV1 时才真正大放异彩。这些编码格式所需的计算量远高于 H.264。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/bbc1f504-d2b9-48fc-a545-4b91ab5b42e8_2888x1497.png)

性能对比非常亮眼。T432 是他们的首款 VPU 产品，搭载 4 颗 Logan 芯片。Quadra T4 是第二代 VPU，有 1、2、4 颗芯片的版本。使用 HEVC 编码格式时，NETINT 完胜 Nvidia 上一代 T4（已有更新的基于 Ampere 的 GPU）和 Intel 的 Skylake/Cascade Lake 服务器。视频 ASIC 所能实现的密度和功耗水平，是 CPU 和 GPU 无法比拟的。使用 AV1 的对比则更加夸张。

NETINT 甚至与 Google Argos 做了对比。这一对比稍有不公平，因为我们知道第二代已经在量产。话虽如此，功耗和吞吐量对比只是基于公开的规格参数，实际对比结果很可能有所不同。Google 并未披露那款芯片的细节，所以这已是 NETINT 能做到的最好对比。这个对比其实也没有意义，因为 Google 并不打算对外销售其 VPU。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d877ad99-3449-4e44-8fa2-9341ece0e604_3050x1488.png)

NETINT VPU 的形态规格非常有意思。他们以 U.2 形态的 NVMe 设备形式提供。这是数据中心用于一组基于 NAND 的 SSD 的形态规格。这使 NETINT 能轻松把产品插进每个数据中心都已在用的机箱类型和形态规格中。它也可以做成标准 PCIe 卡，但 U.2 形态密度更高。产品通过超微（Supermicro）和浪潮（Inspur）的系统销售。NETINT VPU 还支持可组合服务器架构。

VPU 的软件也高度可配置，因为输入流的尺寸和分辨率种类繁多，输出的分辨率和质量等级也很宽泛。这一点尤为关键，因为越来越多的视频来自智能手机。输入分辨率的范围以及竖屏到横屏的持续方向切换，如果编码器不是为此类用例而构建，就会引发性能问题。编码器并不生而平等，这在 GPU 领域可见一斑——[Nvidia 的编码器比 AMD 的好得多](https://chipsandcheese.com/2022/03/30/gpu-hardware-video-encoders-how-good-are-they/)。

可配置性的一个例子是：NETINT 的一位客户对 ASIC 编程，使其优先以更高质量编码画面中的某些部分、其余部分以较低质量编码，从而在最小化文件尺寸的同时最大化流的最终质量。内置的 AI 处理能力可以移除背景、做滤波、识别需要关注的关键区域或人物。这些技术帮助客户将编码成本最多降低了 5 倍。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8c4cd5f4-74ae-4039-964a-cf9f1d07b9e5_1427x722.png)

在某种意义上，VPU 比其他编码方式更灵活。CPU 可以瞄准较低的视频质量和码率效率，但其性能提升不足以值得这么做。此外，那颗 CPU 仍会消耗过多的功耗和空间，TCO 不划算。对 GPU 而言，运行驱动栈对某些应用来说是一团乱麻。各种版本的 Linux 或 Windows 无法正确工作。这类软件问题拖了 Intel GPU 的后腿，包括被取消的 Xe HP 拼接式（tiled）GPU 架构——该架构针对数据中心视频市场做了大量优化，甚至专门为此做过市场营销。

NETINT 拥有一批令人印象深刻的客户，包括但不限于字节跳动、阿里、百度、快手，以及一家规模相当的美国全球性平台。他们打造出了一款在商用芯片市场上独一无二的产品，让大型内容分发网络和云厂商有能力围绕视频内容扩展新体验，例如用户生成的短视频内容、云游戏和实时广告插入。

接下来我们将讨论：为什么我们认为许多美国公司（Google 除外）在采用 VPU 上已经落后，包括美国科技公司今后的采用情况。Nvidia 和 AMD 在这一领域的态度和计划也会讨论。我们还想谈谈 H265 与 AV1 之争。最后，关于这家公司的历史和融资，有一些重要的注记，我们认为应该被讨论并进一步调查。

以上讨论将全部放在下方仅面向付费订阅者的部分。

[分享](https://newsletter.semianalysis.com/p/meet-netint-the-startup-selling-to?utm_source=substack&utm_medium=email&utm_content=share&action=share)
