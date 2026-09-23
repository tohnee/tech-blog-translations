---
title: "SlowFast：通过双帧率分析进行视频识别"
title_en: "SlowFast video recognition through dual frame-rate analysis"
date: 2019-03-15
source: https://ai.facebook.com/blog/slowfast-video-recognition-through-dual-frame-rate-analysis
crawled: 2026-09-22
translated: 2026-09-22
---

# SlowFast：通过双帧率分析进行视频识别

> 原文：[SlowFast video recognition through dual frame-rate analysis](https://ai.facebook.com/blog/slowfast-video-recognition-through-dual-frame-rate-analysis) · Meta AI（Wayback 存档）

**这项研究是什么：** 一种新的视频识别方法，通过同时以慢速和快速两种帧率从视频中提取信息，改进动作分类和动作检测。这个名为 SlowFast 的模型使用两条通路：一条专注于处理可以在低帧率下观察的空间外观语义（如颜色、纹理和物体），另一条通路则寻找快速变化的运动（如拍手或挥手），这些运动在以更高帧率播放的视频中更容易识别。我们的方法部分受到灵长类视觉双通路特性的启发，比以往的视频识别系统更轻量，并在四个主要公开基准数据集上刷新了最先进纪录。

**工作原理：** 通过以不同速度分析原始视频，我们的方法使 SlowFast 网络得以各个击破，每条通路都发挥其在视频建模中的特长。一条通路以低至每秒 2 帧（fps）的速率处理原始刷新率为 30 fps 的视频片段。即使在这样慢的速度下，物体或人的颜色、纹理或身份等特征也不会改变。与此同时，快速通路处理相同的原始视频片段，但帧率高得多——给定 30 fps 的素材，这条通路可能以 16 fps 处理。更快的刷新速度有助于更好地理解视频中正在发生何种运动。但这种方法的主要好处在于效率：既降低了快速通路的通道容量，又增强了其时间建模能力。其结果是一个总体计算复杂度更低、准确率却高于其他计算密集方法的系统。我们在 Kinetics-400、Kinetics-600 和 Charades 数据集上评估了该方法对视频中动作进行分类的能力，并在 AVA 数据集上评估了其动作检测能力。实验结果表明，SlowFast 网络始终比经过预训练的系统更准确，包括在 Kinetics 和 Charades 上以数个百分点优势击败最先进模型。我们基于 SlowFast 的系统还在 CVPR 2019 的 AVA 视频活动检测挑战赛中排名第一。

**为什么重要：** 我们尚未使用 SlowFast 或本帖提到的公开数据集来训练生产模型，但我们的研究在视频分析方面可以有广泛应用，包括改进系统自动识别和分类视频内容的方式。这一领域的进展可以推进查找和删除有害视频的工作，同时为视频推荐提供更好的个性化。除了在下面的论文中分享我们的结果外，我们还在开源该方法的代码库，可从 GitHub 下载。参加 ICCV 2019 的人可以在我们 10 月 28 日的教程和 10 月 31 日的口头报告中了解更多关于 SlowFast 及相应代码库的信息。

**阅读完整论文：** SlowFast networks for video recognition
