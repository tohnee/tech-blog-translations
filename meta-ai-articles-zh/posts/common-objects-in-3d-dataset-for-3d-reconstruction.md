---
title: "开源 Common Objects in 3D：面向 3D 重建的大规模数据集"
title_en: "Open-sourcing Common Objects in 3D, a large-scale data set for 3D reconstruction"
date: 2021-09-02
source: https://ai.facebook.com/blog/common-objects-in-3d-dataset-for-3d-reconstruction
crawled: 2026-09-22
translated: 2026-09-22
---

# 开源 Common Objects in 3D：面向 3D 重建的大规模数据集

> 原文：[Open-sourcing Common Objects in 3D, a large-scale data set for 3D reconstruction](https://ai.facebook.com/blog/common-objects-in-3d-dataset-for-3d-reconstruction) · Meta AI（Wayback 存档）

**这项研究是什么：**以 3D 方式重建物体是计算机视觉的一项开创性问题，其 AR/VR 应用涵盖从远程呈现到为游戏生成 3D 模型。有了逼真而通用的 3D 重建，就能在传统智能手机和笔记本电脑屏幕上，以及在驱动未来体验的 AR 眼镜上，无缝地融合真实与虚拟物体。然而，当前的 3D 重建方法依赖为各种物体类别（「汽车」「甜甜圈」「苹果」等）学习的模型，而进展受到数据集匮乏的阻碍——既包含真实世界物体视频、又包含这些物体精确 3D 复制品的数据集十分稀缺。由于模型依靠这些示例学习如何创建 3D 重建，研究者通常只能使用合成物体的数据集，而这些数据只能近似匹配真实世界问题的挑战性。

为帮助填补这一空白并推动该领域的进展，Facebook AI 发布了 Common Objects in 3D（CO3D）——一个大规模数据集，包含常见物体类别的真实视频及 3D 标注。CO3D 总计包含来自近 19000 段视频的 150 万帧，拍摄了广泛使用的 MS-COCO 数据集中 50 个类别的物体。无论类别数还是物体数，CO3D 都超越了现有替代方案。

（视频展示 CO3D 数据集中的真实世界物体及精细的 3D 复制品。彩虹色线条表示拍摄视频的智能手机相机的轨迹。）

我们还分享了关于 NeRFormer 的工作——一种新方法，通过观察 CO3D 数据集中的视频，学习从新视角合成物体图像。为此，NeRFormer 高效地结合了两项近期的机器学习成果——Transformer 与神经辐射场（Neural Radiance Fields）。因此，NeRFormer 在合成新物体视角上比最接近的竞争者准确率高出最多 17%。

**工作原理：**我们的主要目标是收集一个大规模的、带 3D 形状标注的自然场景常见物体重活数据集。虽然用专用硬件（例如转台式 3D 扫描仪）可以收集后者，但这种方法难以扩展到与合成数据集相当的规模——后者涵盖数千个物体、跨越多样类别。我们转而设计了一种摄影测量方法，只需要以物体为中心的多视角图像。这类数据可以通过众包用消费级智能手机拍摄的「转台」视频大规模有效收集。为此，我们在 Amazon Mechanical Turk（AMT）上众包以物体为中心的视频。每个 AMT 任务要求工作者选择给定类别的一个物体，把它放在稳固的表面上并录制一段视频：在绕物体转一整圈的同时保持物体完整处于视野内（示例见下方视频）。我们选择了 50 个 MS-COCO 类别，它们由静止物体组成，具有明确的形状概念，是成功进行 3D 重建的理想候选。

（这段儿童三轮车的视频是作为 CO3D 数据集的一部分收集的。）

成熟的摄影测量框架 COLMAP 提供 3D 标注并被视为真值（ground truth）：它跟踪智能手机相机在 3D 空间中的位置，并进一步重建捕捉物体表面的稠密 3D 点云。上例中可以看到重建示例和相机跟踪。最后，为确保高质量的 3D 标注，我们设计了一种半自动的主动学习算法，过滤掉 3D 重建精度不足的视频。

（这五个物体也是 CO3D 数据集的一部分。）

在发布 CO3D 数据集的同时，我们提出了 NeRFormer——一种新颖的深度架构，通过观察收集到的视频学习物体类别的几何结构。训练期间，NeRFormer 通过可微分地渲染一个表示物体几何与外观的神经辐射场（NeRF）来学习。重要的是，渲染由一个新颖的深度 Transformer 完成，它联合学习：通过分析物体视频帧的内容来预测辐射场属性，并沿渲染光线「行进」来渲染新视角。以这种方式，一旦 NeRFormer 学会了某个类别的共同结构，它就能仅凭少量已知视角，为前所未见的物体合成新视角。

**为什么重要：**作为首个此类数据集，CO3D 将恰如其分地支撑真实生活 3D 物体的重建。事实上，CO3D 已经提供了训练数据，使我们的 NeRFormer 能够应对新视角合成（NVS）任务。逼真的 NVS 是通往完全沉浸式 AR/VR 效果的重要一步——物体可以被虚拟地「搬运」到不同环境中，让用户通过分享或重温各自的体验彼此连接。除了在 AR/VR 中的实际应用，我们希望该数据集成为近期涌现的一批方法（包括 NeRFormer、Implicit Differentiable Renderer、NeRF 等）的标准测试平台，这些方法都通过隐式形状模型重建 3D 场景。

阅读完整论文：Common Objects in 3D

获取数据集：https://github.com/facebookresearch/co3d

了解更多：Common Objects in 3D 微网站

**作者**

- David Novotny，研究科学家
- Jeremy Reizenstein，研究工程师
- Roman Shapovalov，软件工程师
- Philipp Henzler，研究实习生
- Luca Sbordone，项目经理
- Patrick Labatut，软件工程经理
