---
title: "谷歌新自研芯片取代 1000 万颗英特尔 CPU｜谷歌 Argos VPU"
title_en: "Google New Custom Silicon Replaces 10 Million Intel CPUs | Google Argos VPU"
date: 2021-06-02
source: https://newsletter.semianalysis.com/p/google-new-custom-silicon-replaces
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 谷歌新自研芯片取代 1000 万颗英特尔 CPU｜谷歌 Argos VPU

> 原文：[Google New Custom Silicon Replaces 10 Million Intel CPUs | Google Argos VPU](https://newsletter.semianalysis.com/p/google-new-custom-silicon-replaces) · SemiAnalysis

万亿美元级的科技公司都在竞相成为垂直整合的巨兽。谷歌（Google）在这方面毫不逊色，坐拥一大批定制与半定制芯片项目：从大名鼎鼎的 AI 芯片 TPU，到 Titan 安全芯片，再到即将问世的产品——Pixel/Chromebook SoC、Arm Neoverse 服务器 CPU，以及 Waymo 自动驾驶系统。

谷歌延续其自研芯片的雄心，打造了 Argos——一类被称为 VCU（Video Coding Unit，视频编码单元）的新型 ASIC。通过在数据中心大规模部署这款定制芯片，**谷歌取代了数以百万计的 x86 CPU**，并强化了自己的服务能力。这款定制芯片已经上线相当一段时间，谷歌的第二代 VCU 也已接近部署阶段，将带来 AV1 编码支持等增强特性。

VCU 专为加速视频工作负载而设计，覆盖 YouTube、Google Photos、Google Drive 和 Stadia 游戏串流等产品线。一方面，更高分辨率、更大体量的视频分享需求持续增长；另一方面，视频处理的改进却步履蹒跚。不采用领域专用硬件加速器，视频加速的未来增长便无从谈起。2019 年 5 月，谷歌每分钟收到超过 500 小时的 YouTube 视频素材。这相当于海量数据必须编码成标准格式、加以存储，再串流分发给用户。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/26ab7c23-f57e-4075-b9df-1139a0844416_717x1024.jpeg)

谷歌会把输入视频以 H264 编码到每一种可观看的分辨率。此外，观看量最高的视频还会用 VP9 再编码一份。VP9 是一种更复杂的视频编解码器，可以让视频文件更小而画质不变，也可以在文件大小不变的情况下呈现更高的画质。VP9 让谷歌节省下大量从数据中心经内容分发网络流向用户的出口带宽，进而大幅压低成本。如果能完全切换到 VP9，谷歌还能让整个视频存储库少占不少存储空间。

不过这种编解码器并非全是好处：CPU 编码这一格式非常吃力，速度慢了近 5 倍。谷歌在披露该产品时给出了编码性能数据。按其引用的数字，假设谷歌服务器 100% 稼动（实际并非如此）、所有 YouTube/Google Photos/Google Drive 视频素材均为 1080p 30FPS、目标格式为 H264，那么这项工作负载需要约 904,000 颗 Intel Skylake 服务器 CPU 来编码。在同样一组假设下切换到 VP9，则需要约 4,193,000 颗 Intel Skylake 服务器 CPU。若上传素材为 4k 60FPS，则 H264 所需 CPU 约为 7,205,000 颗，VP9 需要约 33,407,000 颗。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/73c94707-9bb1-43f9-a71d-513dab34d26b_1024x386.png)

CPU 根本不堪此任，专用加速器的必要性一目了然。许多人会转而追问 GPU。GPU 的 TCO 确实略好一些，但其稼动率更低，而且面对 VP9、AV1 这类新编码方案时工作负载灵活性更差。GPU 带来的提升幅度不足以值得采用，因此同样不适合手头这项任务。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c93da000-e3f9-4c27-bf06-2f2c26e1425d_1024x523.png)

于是就有了谷歌的 Argos VPU：每颗 Argos 芯片封装在一张 PCIe 卡上，每台服务器可用 10 张这样的 PCIe 卡。由于专为任务而生，它们提供了显著更高的性能与能效。你大概以为研发成本会高得吓人，但除编码器核心之外，其余 IP 全部从第三方授权而来，这大幅压低了成本和方案工程化的时间。它采用现代移动 SoC 的方法论和视角来构建，从而得以快速整合来自各方的 IP。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/387ad440-5f2a-4ef8-bee1-916c1c9bc2a2_1024x255.png)

整套方案的核心是软硬件协同设计。系统架构必须从每颗 Argos 芯片内部的硬件编码器核心和内存，一路贯通到整颗芯片、PCBA、服务器节点、集群乃至区域（region）。只有如此深度的整合，才能把稼动率拉满、平衡负载、大规模部署，并适应谷歌服务框架的持续调整。每个编码器/解码器核心以及 VCU 内存控制器都可以被切分，确保被完全利用。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/f22f49b8-3fc6-4159-84b0-85d24301f9cc_1024x594.png)

软硬件协同设计是双向的。除了使用 Mentor Graphics 名为 Catapult 的行业标准电子设计自动化（EDA）工具外，谷歌还自研了一款名为 Taffel 的集成工具。**谷歌的芯片自主雄心如此宏大，连 EDA 工具都在自己开发！** 他们仍依赖更广泛的 EDA 行业，但依赖程度已经下降。验证环节可占芯片设计成本的 50% 以上，因此 SemiAnalysis 认为，这款自研工具瞄准的很可能正是芯片设计流程中的这一环。

> 借助 HLS，相比传统 Verilog 方法，需要编写、评审和维护的代码量减少了 5-10 倍。

谷歌宣称其流程远比久经考验的传统 Verilog 方法高效，并宣称测试吞吐量加速了 7-8 个数量级。放眼这颗芯片之外，谷歌显然怀有借垂直整合的自研芯片成为半导体巨兽的长期雄心。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/73c94707-9bb1-43f9-a71d-513dab34d26b_1024x386.png)

把这一切加总：在 H.264 视频编码所需基础设施的总拥有成本（TCO）上，谷歌取得了 7 倍改善；在 VP9 上更是取得了 33.3 倍改善。这一 TCO 计算已计入芯片成本外加 3 年运营开支，VCU 的研发成本也包含在内。

沿用 100% 稼动率的假设（完全脱离现实），如果谷歌收到的每条视频都用 VP9 编码，按 1080p 30FPS 画质计算，所需 Intel Skylake 服务器 CPU 总数将达到约 4,192,000 颗。谷歌每张 PCIe 卡部署 2 颗 VCU，每台服务器使用 10 张卡，而这些服务器同时还要搭载 2 颗 Intel Skylake CPU。要以 1080p 30FPS 画质编码收到的全部视频，谷歌需要约 21,500 台这样的服务器——共计约 43,000 颗 Intel Skylake 服务器 CPU 和约 430,000 颗自研 Argos VPU。这就是谷歌少向英特尔（Intel）购买的 400 万颗服务器 CPU！

如果假设上传素材的画质为 4k 60FPS，那么从约 33,407,000 颗 Intel Skylake 服务器 CPU 的基数上削减下来就更令人咋舌：所需服务器降至约 170,000 台，CPU 总数约 340,000 颗，Argos VPU 约 3,400,000 颗。3300 万颗 CPU 的活儿就此消失。我们认为，上传到 Google Photos 和 YouTube 的平均视频多半达不到 4k 60FPS，但平均下来也很可能高于 1080P 30FPS。谷歌 VCU 省下的 CPU 采购量在 400 万到 3300 万颗之间，我们的估计约为 1000 万颗——这一估计已把稼动率并非 100%、平均上传画质略高于 1080p 30FPS 这两个事实考虑在内。

成本与速度上的这些巨大收益，让谷歌得以在所有平台全面启用 VP9，连少人问津的视频也不例外。存储和带宽出口成本显著下降。他们还能将 VP9 用于 Google Stadia 串流，实现 4k 60 FPS 游戏画面串流。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/69ef1058-1d3e-4bcf-b766-50ad5f71d517_800x444.png)

谷歌 VCU 的下一步是什么？据 SemiAnalysis 的消息源，下一代已在开发之中。它将支持 AV1 格式编码——这在 CPU 或 GPU 上是完全不可能实现的。存储和带宽还将进一步节省。此外，他们还计划在这颗新芯片上加入机器学习推理硬件。最后，他们还将在扩展卡本身上集成网络功能，以提高效率、减少与主机 CPU 的通信。这将让谷歌自动生成视频字幕、检查违反服务条款的内容，甚至在 YouTube 和 Google Photos 上实现视频搜索。

省下 1000 万颗 CPU 的收益当下即可兑现，但若没有谷歌的自研芯片，上述下一代功能绝对无从谈起。这将让谷歌在视频工作负载上对其他科技公司取得实实在在的领先——不仅是成本，还有能力。坐拥 Twitch.tv 的亚马逊（Amazon）和 Facebook/Instagram 必须为这类工作负载开发自己的芯片，否则在竞争中将被远远甩在身后。[TikTok 的母公司字节跳动（ByteDance）甚至也在开发针对其视频工作负载量身定制的自研芯片。](https://www.bloomberg.com/opinion/articles/2021-03-17/bytedance-move-into-chips-will-find-backing-in-china-s-tech-independence-drive) 而英特尔、Nvidia、AMD 等商用硅片供应商将发现，自己正被彻底踢出全球最大科技公司的视频工作负载。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

[分享](https://newsletter.semianalysis.com/p/google-new-custom-silicon-replaces?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[发表评论](https://newsletter.semianalysis.com/p/google-new-custom-silicon-replaces/comments)

*本文最初于 2021 年 6 月 2 日发布于 [SemiAnalysis](https://semianalysis.com/google-new-custom-silicon-replaces-10-million-intel-cpus-google-argos-vpu/)。*

*SemiAnalysis 的客户及员工可能持有本文所提及公司的仓位。*
