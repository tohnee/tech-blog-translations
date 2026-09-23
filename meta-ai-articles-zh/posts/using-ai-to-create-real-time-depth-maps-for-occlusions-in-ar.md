---
title: "用 AI 为 AR 中的遮挡效果创建实时深度图"
title_en: "Using AI to create real-time depth maps for occlusions in AR"
date: 2019-03-15
source: https://ai.facebook.com/blog/using-ai-to-create-real-time-depth-maps-for-occlusions-in-ar
crawled: 2026-09-22
translated: 2026-09-22
---

# 用 AI 为 AR 中的遮挡效果创建实时深度图

> 原文：[Using AI to create real-time depth maps for occlusions in AR](https://ai.facebook.com/blog/using-ai-to-create-real-time-depth-maps-for-occlusions-in-ar) · Meta AI（Wayback 存档）

为了让增强现实（AR）更加逼真，我们需要能够把 AR 特效同时应用在场景中物体的前方和后方。然而，大多数 AR 系统基于 SLAM（即时定位与地图构建），只能跟踪少数稀疏的点特征。这足以在物体前方叠加内容，却无法在物体后方进行。我们开发了一种方法，将稀疏点跟踪位置的深度扩展到所有其他像素，为每一帧创建稠密深度图。该方法帮助 AR 特效与场景几何完全交互，例如让场景中的真实物体实现对虚拟内容的遮挡。

观看视频。

阅读完整论文：《Fast Depth Densification for Occlusion-aware Augmented Reality》
