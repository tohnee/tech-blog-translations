---
title: "D2Go 将 Detectron2 带到移动端"
title_en: "D2Go brings Detectron2 to mobile"
date: 2021-03-04
source: https://ai.facebook.com/blog/d2go-brings-detectron2-to-mobile
crawled: 2026-09-22
translated: 2026-09-22
---

# D2Go 将 Detectron2 带到移动端

> 原文：[D2Go brings Detectron2 to mobile](https://ai.facebook.com/blog/d2go-brings-detectron2-to-mobile) · Meta AI（Wayback 存档）

2021 年 3 月 4 日

Detectron2 由 Facebook AI Research（FAIR，Meta 基础人工智能研究院）于 2019 年发布，为开发者将自定义模块接入任意目标检测系统提供了便捷途径。今天，Facebook Reality Labs（FRL）的移动视觉团队在此基础上扩展，推出 Detectron2Go（D2Go）——一个新的、最先进的扩展，用于在移动设备与硬件上训练和部署高效的深度学习目标检测模型。D2Go 构建在 Detectron2、PyTorch Mobile 和 TorchVision 之上。它是同类工具中的第一个，让开发者能够把机器学习模型从训练一路带到移动端部署。

## 走向设备端

目标检测的用例取决于两个关键因素——延迟（速度）与准确率。设想自动驾驶车辆的安全措施、用目标识别来发现采矿作业中的隐患，甚至是为 Instagram 上的人们打造无缝的增强现实（AR）体验。在这类场景中，系统不仅要能准确检测和识别物体，还必须快速高效地完成。然而许多视觉系统面临的挑战正是延迟。使用服务端或云端模型的设备需要时间收集数据、发送到云端处理、再据此行动。但如果模型可以运行在边缘、就在设备本身之内，就能大幅降低这种延迟。设备端模型还为终端用户提供了额外的安全与隐私益处。与语音和自然语言处理（NLP）任务类似，目标识别也带有隐私顾虑——人们担心敏感数据（例如个人图像）被发送到云端。而使用 D2Go 开发的移动模型，所有处理都在设备上完成。

## 为什么选择 D2Go

Detectron2 是一个基于 PyTorch 的库，设计用于训练机器学习模型执行图像分类和目标检测任务。借助新的 D2Go 扩展，开发者可以将 Detectron2 开发再推进一步，创建已针对移动设备优化过的 FBNet 模型，其架构能高效执行检测与分割任务。这些模型经过量化，意味着它们能以更高效率和相当的准确率，完成与大型得多的服务端模型相同的任务。在 FAIR 自己的测试中，用 D2Go 开发的移动端模型表现出更低的延迟，且准确率与对应的服务端模型相当。

D2Go 在构建时就考虑了与开源软件的互操作性——开发者可以选择 PyTorch Lightning 作为训练框架，并利用社区已有的工具。与 FBNetV3 相结合，D2Go 提供高效的检测、实例分割和关键点估计模型，在资源充足的场景中节省算力，并让资源受限的场景得以在设备端运行。

D2Go 已被用于 Facebook 自己的计算机视觉模型开发，尤其是在 FRL 内部——在那里，硬件感知的实时模型对于提供出色的用户体验至关重要，Facebook 的 3D 照片功能就是一个例子。

（原文此处嵌入视频：D2Go 人体关键点估计的演示。）

## 开始使用 D2Go

作为 D2Go 开源发布的一部分，FRL 移动视觉团队发布了演示应用和一系列教程来帮助开发者入门。第一个教程面向 Detectron2 经验较少的用户，提供 Detectron2 与 D2Go 的高层概览，讲解基础知识以及如何使用自定义数据集创建目标检测器。第二个教程聚焦如何编写训练脚本来简化开发流程，以及如何针对你的特定需求定制 D2Go。

要开始使用 D2Go 并了解更多，请访问 D2Go GitHub 仓库。

感谢以下人员对本项目的贡献：Hang Zhang、Yanghan Wang、Xiaoliang Dai、Matthew Yu、Bichen Wu、Tao Xu、Sam Tsai、Peizhao Zhang、Francisco Massa、Jeff Tang、Yuxin Wu、Wan-Yen Lo、Ross Girshick、Kai Zhang、Luis Perez、Vasiliy Kuznetsov、Raghuraman Krishnamoorthi、Matt Uyttendaele、Christian Keller、Gaurav Aggarwal、Donny Greenberg、Vasilis Vryniotis 和 Peter Vajda。
