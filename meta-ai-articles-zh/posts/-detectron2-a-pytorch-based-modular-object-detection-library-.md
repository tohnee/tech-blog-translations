---
title: "Detectron2：基于 PyTorch 的模块化目标检测库"
title_en: "Detectron2: A PyTorch-based, modular object detection library"
date: 2019-10-10
source: https://ai.meta.com/blog/-detectron2-a-pytorch-based-modular-object-detection-library-/
crawled: 2026-09-22
translated: 2026-09-22
---

# Detectron2：基于 PyTorch 的模块化目标检测库

> 原文：[Detectron2: A PyTorch-based, modular object detection library](https://ai.meta.com/blog/-detectron2-a-pytorch-based-modular-object-detection-library-/) · Meta AI（Wayback 存档）

自 2018 年发布以来，Detectron 目标检测平台已成为 Facebook AI Research（FAIR，Meta 基础人工智能研究院）采用最广泛的开源项目之一。为了在这一项目的基础上继续前进，我们现在分享该库的第二代版本，它在研究和生产用途两方面都有重要增强。该库可在此处获取。

Detectron2 是对 Detectron 的彻底重写，起点是 maskrcnn-benchmark。平台现在用 PyTorch 实现。凭借全新的、更模块化的设计，Detectron2 灵活且可扩展，并能在单台或多台 GPU 服务器上提供快速训练。Detectron2 收录了多种最先进目标检测算法的高质量实现，包括 DensePose、全景特征金字塔网络（panoptic feature pyramid networks），以及同样由 FAIR 开发的开创性 Mask R-CNN 模型家族的众多变体。其可扩展的设计使得实现前沿研究项目无需 fork 整个代码库。

我们构建 Detectron2 的目的，一是满足 Facebook AI 的研究需求，二是为 Facebook 生产用例中的目标检测提供基础。我们正在使用 Detectron2 快速设计和训练下一代姿态检测模型，这些模型为 Smart Camera——Facebook Portal 视频通话设备中的 AI 相机系统——提供支持。通过将 Detectron2 作为研究和生产用例中统一的目标检测库，我们得以快速把研究想法转化为大规模部署的生产模型。

（原文此处嵌入视频，展示使用 Detectron2 完成的不同类型目标检测任务。）

我们之所以分享 Detectron2，是因为开源研究平台对整个社区（包括学术界和工业界的研究者与从业者）推动 AI 的快速进步至关重要。我们希望发布 Detectron2 能继续加速目标检测与分割领域的进展。

## Detectron2 的改进

**PyTorch：**最初的 Detectron 用 Caffe2 实现。PyTorch 提供了更直观的命令式编程模型，让研究者和从业者能够更快地迭代模型设计与实验。由于我们从零开始用 PyTorch 重写了 Detectron2，用户现在可以受益于 PyTorch 的深度学习方式，以及持续改进 PyTorch 的庞大而活跃的社区。

**模块化、可扩展的设计：**在 Detectron2 中，我们引入了模块化设计，允许用户将自定义模块实现插入目标检测系统的几乎任何部分。这意味着许多新研究项目只需数百行代码即可完成，并且核心 Detectron2 库与新颖的研究实现之间保持清晰的分离。我们会通过实现新模型、探索让 Detectron2 更灵活的新方式，持续打磨这一模块化、可扩展的设计。

（原文此处嵌入视频，展示 Detectron2 的模块化设计如何让用户以一张图像为输入，轻松切换自定义主干网络、插入不同预测头并执行全景分割。）

**新模型与新特性：**Detectron2 包含原版 Detectron 中的所有模型，如 Faster R-CNN、Mask R-CNN、RetinaNet 和 DensePose。它还收录了若干新模型，包括 Cascade R-CNN、Panoptic FPN 和 TensorMask，而且我们会继续增加更多算法。我们还添加了同步 Batch Norm 等特性，以及对 LVIS 等新数据集的支持。

**新任务：**Detectron2 支持一系列与目标检测相关的任务。与原版 Detectron 一样，它支持带边界框的目标检测和实例分割掩码，以及人体姿态预测。除此之外，Detectron2 还新增了对语义分割和全景分割（一个结合了语义分割与实例分割的任务）的支持。

**实现质量：**从零重写 Detectron2 让我们得以重新审视底层设计决策，并解决原版 Detectron 中的若干实现问题。

**速度与可扩展性：**通过将整个训练流水线迁移到 GPU，对于多种标准模型，我们使 Detectron2 比原版 Detectron 更快。此外，现在可以轻松地把训练分布到多台 GPU 服务器上，从而更简单地把训练扩展到超大数据集。

**Detectron2go：**Facebook AI 的计算机视觉工程师实现了一个附加的软件层 Detectron2go，让先进的新模型更容易部署到生产环境。这些功能包括使用内部数据集的标准训练工作流、网络量化，以及将模型转换为面向云端和移动端部署的优化格式。

## 为所有人加速 AI 研究与工程

AI 的进步是一项社区工程，参与者包括个人、大大小小的实验室、学术界和工业界。我们要解决的问题远超任何个人或团体独自所能企及的范围。正因如此，我们坚信应当分享能够支撑可复现研究、快速实验和新想法开发的代码。通过发布 Detectron2，我们希望进一步加速目标检测、分割和人体姿态理解领域的研究。

新的研究始于理解、复现和验证文献中的先前结果。借助 Detectron2，我们旨在为许多最先进的算法提供高质量参考实现，从而让研究过程的这一阶段走向平民化。该库的模块化设计也让研究者能够在与标准检测库功能清晰分离的前提下实现新项目。举个例子，Mesh R-CNN——FAIR 近期关于从 2D 图像预测逐目标实例 3D 网格的工作——就是在 Detectron2 中开发的。Detectron2 的模块化设计使研究者能够轻松扩展 Mask R-CNN 以处理表示 3D 网格的复杂数据结构、集成新数据集并设计新颖的评测指标。

Detectron2 可以在研究优先的用例与面向生产的用例之间轻松共享。由于该库基于 PyTorch 构建，新模型可以快速实现并随后转移到生产环境。

## 构建支撑下一代 CV 突破的技术

我们对 Detectron2 的目标是既支持当今广泛存在的最先进目标检测与分割模型，也服务于不断变化的前沿研究图景。新颖研究从定义上就意味着发明新模型，而这些模型很可能会打破现有模型的设计假设。这意味着要构建能支撑一组几乎无法预先穷举的需求的软件，同时让它尽可能易于使用。我们期望围绕这一目标持续开发和打磨 Detectron2。随着该库现已向更广泛的 ML 社区开放，我们期待在挑战计算机视觉系统可能性极限的路上与他人合作、向他人学习。

我们要感谢 Xinlei Chen、Jing Huang、Vasil Khalidov、Yanghao Li、Jon Morton、Sam Pepose、Ria Verma、Yanghan Wang、Peizhao Zhang 以及其他帮助构建 Detectron2 的贡献者。

**作者**

- Yuxin Wu，研究工程师
- Alexander Kirillov，研究科学家
- Francisco Massa，研究工程师
- Wan-Yen Lo，研究工程经理
- Ross Girshick，研究科学家
