---
title: "D4RT：教 AI 从四个维度看世界"
title_en: "D4RT: Teaching AI to see the world in four dimensions"
source: https://deepmind.google/blog/d4rt-teaching-ai-to-see-the-world-in-four-dimensions/
site: deepmind
date: 2026-01-22
crawled: 2026-09-13
translated: 2026-09-13
---

# D4RT：教 AI 从四个维度看世界

> 原文：[D4RT: Teaching AI to see the world in four dimensions](https://deepmind.google/blog/d4rt-teaching-ai-to-see-the-world-in-four-dimensions/) · Google DeepMind

我们推出 D4RT，一个用于跨时空 4D 场景重建与跟踪的统一 AI 模型。

每当我们注视这个世界时，都在完成一项记忆与预测的非凡壮举。我们看到并理解事物在某一时刻的样子、它们刚才的样子，以及它们接下来一刻将会呈现的样子。我们对世界的心理模型保持着对现实的持久表征，并借助这个模型对过去、现在与未来之间的因果关系得出直观结论。

要让机器像我们一样看世界，我们可以为它们装上摄像头，但那只解决了输入问题。要理解这些输入，计算机必须求解一个复杂的逆问题：拿到一段视频——一组平面的 2D 投影序列——并恢复或理解那个丰富的、立体的、处于运动中的 3D 世界。

今天，我们推出 [D4RT（Dynamic 4D Reconstruction and Tracking，动态 4D 重建与跟踪）](https://d4rt-paper.github.io/)，一个把动态场景重建统一进单一高效框架的新 AI 模型，让我们更接近人工智能的下一个前沿：对我们动态现实的全面感知。

## 第四维度的挑战

要理解一段 2D 视频捕捉到的动态场景，AI 模型必须跟踪每个物体的每一个像素，跟随它穿过三维空间和作为第四维度的时间。此外，它还必须把这种运动与摄像机的运动解耦开，即便物体彼此遮挡或完全离开画面，也要保持连贯的表征。传统上，从 2D 视频中捕获这种水平的几何与运动信息，需要计算密集的处理流程，或者拼凑各种专用 AI 模型——有的负责深度，有的负责运动或摄像机角度——最终得到速度慢、碎片化的 AI 重建结果。

D4RT 的简化架构和新颖的查询机制，使其跻身 4D 重建的最前沿，同时效率比以往方法高出最多 300 倍——足以支撑机器人技术、增强现实等领域的实时应用。

## D4RT 的工作原理：基于查询的方法

D4RT 以统一的编码器-解码器 Transformer 架构运行。编码器首先把输入视频处理为场景几何与运动的压缩表征。与为不同任务使用独立模块的旧系统不同，D4RT 借助一个灵活的查询机制、围绕一个根本性的问题只计算它所需要的内容：

"视频中的**某个给定像素**，在任意**时刻**、从**选定的摄像机**视角看，位于**三维空间**中的什么位置？"

基于[我们此前的工作](https://srt-paper.github.io/)，一个轻量级解码器随后查询这一表征，来回答该问题的具体实例。由于各查询相互独立，它们可以在现代 AI 硬件上并行处理。这使得 D4RT 无论只跟踪几个点，还是重建整个场景，都极为快速且可扩展。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ 您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

D4RT 结合了一个强大的编码器——对视频建立丰富、全局的理解——和一个轻量级解码器——并行回答成千上万个查询。通过提出具体的问题——确定某个源像素在目标时刻和摄像机视角下的位置——该模型通过单一、灵活的接口高效地解决跟踪、深度估计、位姿估计等多种任务。

## 能力：快速而精准的 4D 理解

凭借这种灵活的表述方式，模型现在可以解决多种多样的 4D 任务，包括：

- **点跟踪**：通过查询一个像素在不同时间步的位置，D4RT 可以预测它的 3D 轨迹。重要的是，模型做出预测并不要求该物体在视频其他帧中可见。
- **点云重建**：通过冻结时间与摄像机视点，D4RT 可以直接生成场景的完整 3D 结构，省去了额外的步骤，例如单独的摄像机估计或针对每段视频的迭代优化。
- **摄像机位姿估计**：通过从不同视点生成并配准同一时刻的 3D 快照，D4RT 可以轻松恢复摄像机的运动轨迹。

正如[底层技术报告](https://arxiv.org/abs/2512.08924)中详述的，D4RT 在广泛的 4D 重建任务上超越了以往方法。定性对比显示，当其他方法在动态物体上遇到困难——常常把它们复制出来或完全无法重建——D4RT 始终保持对运动世界的扎实、连续的理解。

至关重要的是，D4RT 的精度并不以牺牲效率为代价。在测试中，它的速度比此前最先进的方法快 18 到 300 倍。例如，D4RT 在单个 TPU 芯片上用大约 5 秒处理了一段一分钟的视频。以往最先进的方法完成同样的任务最多需要 10 分钟——提升了 120 倍。

第 1 页，共 3 页

![一张标题为“MPI Sintel 上的点云重建”的柱状图，比较了六个模型的 3D 保真度（2 减去 L1 误差，越高越好）。性能从低到高依次为：MapAnything 0.282、VGGT 0.420、MegaSaM 0.469、SpatialTrackerV2 0.625、π3 0.861，D4RT 以最高分 1.091 领先，以亮蓝色柱形高亮显示。](https://lh3.googleusercontent.com/XpEVj8v4dIrVaUtViFeyGyY4fyRUMnvpIcP9jheHwWS17VhKk5eGNoHWQNoXzRKIOxHxNj3kU0AlD-8kDE-gxHOeM_dwSa2CZbxTMWoQAtMUy0Mxcwc=w1440-h810-n-nu)![一张标题为“MPI Sintel 上的点云重建”的柱状图，比较了六个模型的 3D 保真度（2 减去 L1 误差，越高越好）。性能从低到高依次为：MapAnything 0.282、VGGT 0.420、MegaSaM 0.469、SpatialTrackerV2 0.625、π3 0.861，D4RT 以最高分 1.091 领先，以亮蓝色柱形高亮显示。](https://lh3.googleusercontent.com/muuplDDRZOonBlJAm4pYP3QJhNlRXlGzFWoXsnpIAnpUgUoIl5_z4UacYi0f6NuejmFJ48m7PKHpHRn6-4ieX6-0KVsjNEJv6EhBuShwYE4HC5KrAAQ=w1440-h810-n-nu)

在以快速运动模糊和非刚性形变为特点的复杂合成场景构成的 MPI Sintel 基准上评估时，D4RT 相比近期强有力的基线展现出更高的保真度。这凸显了该模型即便在物体或摄像机快速穿过场景时也能准确重建几何结构的能力。

![一张标题为“Aria Digital Twin 上的点跟踪”的柱状图，比较了四个模型的 3D 保真度（2 减去 L1 误差，越高越好）。性能从低到高依次为：St4RTrack 1.161、CoTracker3 + VGGT 1.264、SpatialTrackerV2 1.762，D4RT 以最高分 1.904 领先，以亮蓝色柱形高亮显示。](https://lh3.googleusercontent.com/g6EamdthyxHW3RAZn0ln9LwWVTDdIAb9-LFcTyzdqzG0Ya20gMb6txonCrAivra7zqo256Bj03-4YquLVONufp2sXLkMWO1EkEjoi24BCHJx-NtIM6k=w1440-h810-n-nu)![一张标题为“Aria Digital Twin 上的点跟踪”的柱状图，比较了四个模型的 3D 保真度（2 减去 L1 误差，越高越好）。性能从低到高依次为：St4RTrack 1.161、CoTracker3 + VGGT 1.264、SpatialTrackerV2 1.762，D4RT 以最高分 1.904 领先，以亮蓝色柱形高亮显示。](https://lh3.googleusercontent.com/4-7pj8axU2Z9RTs7rcnVN4XJxcSS1x9QaM23ogfVlz0k3xwdms06i5ArIWC3FCANXRqfYy7fP-FbepGqTrwdXFw4rYdBGfuzVrcXs8P6mhcSUroPbg=w1440-h810-n-nu)

使用来自 Aria Digital Twin 数据集的智能眼镜画面，D4RT 在 3D 点跟踪上取得了顶尖的表现。这验证了该模型在真实家庭环境中对复杂自我运动和遮挡的稳健处理能力。

![一张标题为“RE10k 上的摄像机位姿估计”的柱状图，比较了五个模型的位姿 AUC。性能从低到高依次为：VGGT 0.702、MegaSaM 0.710、SpatialTrackerV2 0.757、π3 0.787，D4RT 以最高分 0.835 领先，以亮蓝色柱形高亮显示。](https://lh3.googleusercontent.com/UoGso_JmalQ1HFec6Vw4LPY8qShLWVmaSUEDR3nAWca0VA8PVJpMr5olAYC7kw1KMKqtFTbmY7fCjnagrEqF1o02CEvtQhRSqR1ezeBeHwobSrrH=w1440-h810-n-nu)![一张标题为“RE10k 上的摄像机位姿估计”的柱状图，比较了五个模型的位姿 AUC。性能从低到高依次为：VGGT 0.702、MegaSaM 0.710、SpatialTrackerV2 0.757、π3 0.787，D4RT 以最高分 0.835 领先，以亮蓝色柱形高亮显示。](https://lh3.googleusercontent.com/EtGSifMr1elbDT1MtcHCK1EDj6EMcFNqACQsrtWr5oisX4F0LcGqBxDmW1Ehtf-yfM6bhT63LGrIuNCVzR9dxt2vEHSECgXEiuTkUFjFdsFJdwxCHvY=w1440-h810-n-nu)

在 RE10k 数据集多样的室内外场景上评估摄像机位姿估计时，D4RT 取得了最高的 AUC 分数。这一指标衡量估计位姿落入严格精度阈值范围的频率，体现了模型无需昂贵的测试时优化即可锁定稳定几何结构的能力。

## 下游应用

D4RT 表明，在 4D 重建中我们不必在精度与效率之间做选择。它灵活的、基于查询的系统可以实时捕捉我们动态的世界，为下一代空间计算铺平道路。这包括：

- **机器人技术**：机器人需要在有移动的人和物体的动态环境中导航。D4RT 可以提供安全导航与灵巧操作所需的空间感知。
- **增强现实（AR）**：AR 眼镜要把数字物体叠加到真实世界之上，就需要对场景几何进行即时、低延迟的理解。D4RT 的效率有助于让设备端部署成为切实的现实。
- **世界模型**：通过有效解耦摄像机运动、物体运动与静态几何，D4RT 让我们向拥有物理现实真正"世界模型"的 AI 又迈进了一步——这是通往 AGI 道路上的必要一步。

我们将继续探索该模型的能力，以及它在机器人技术、增强现实等领域的应用潜力。

[阅读我们的技术报告](https://arxiv.org/abs/2512.08924)[访问我们的项目网站](https://d4rt-paper.github.io/)
