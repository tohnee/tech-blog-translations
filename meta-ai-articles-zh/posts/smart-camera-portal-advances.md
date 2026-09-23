---
title: "我们如何为新款 Portal 视频通话设备升级 Smart Camera"
title_en: "How we’ve advanced Smart Camera for new Portal video-calling devices"
date: 2019-03-15
source: https://ai.facebook.com/blog/smart-camera-portal-advances
crawled: 2026-09-22
translated: 2026-09-22
---

# 我们如何为新款 Portal 视频通话设备升级 Smart Camera

> 原文：[How we’ve advanced Smart Camera for new Portal video-calling devices](https://ai.facebook.com/blog/smart-camera-portal-advances) · Meta AI（Wayback 存档）

随着今天三款新型号 Portal 的发布，我们在此分享我们如何升级 Smart Camera——这个在视频通话中智能取景的 AI 驱动系统。Smart Camera 构建在 Facebook AI 开创性的 Mask R-CNN 框架（用于物体实例分割和关键点检测）之上。我们在驱动 Smart Camera 的计算机视觉模型上做了额外的速度和精度改进。我们现在使用 Detectron2——Facebook AI 创建的新一代（第二代）物体检测平台——来训练 Smart Camera 的姿态估计模型。由于 Detectron2 是用我们的深度学习平台 PyTorch 开发的，它能实现更快的模型迭代。除了这些模型改进之外，我们还为物体检测构建了定制硬件集成，并加入了注视点处理（foveated processing）等增强功能——它把处理集中在相机传感器的特定区域。这些工作使我们能够把 Portal 体验带到更低功耗的物联网（IoT）芯片组上。点击上方视频了解更多。
