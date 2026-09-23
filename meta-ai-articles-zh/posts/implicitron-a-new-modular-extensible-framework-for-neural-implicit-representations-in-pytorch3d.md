---
title: "Implicitron：PyTorch3D 中面向神经隐式表示的全新模块化可扩展框架"
title_en: "Implicitron: A new modular, extensible framework for neural implicit representations in PyTorch3D"
date: 2022-08-11
source: https://ai.meta.com/blog/implicitron-a-new-modular-extensible-framework-for-neural-implicit-representations-in-pytorch3d
crawled: 2026-09-22
translated: 2026-09-22
---

# Implicitron：PyTorch3D 中面向神经隐式表示的全新模块化可扩展框架

> 原文：[Implicitron: A new modular, extensible framework for neural implicit representations in PyTorch3D](https://ai.meta.com/blog/implicitron-a-new-modular-extensible-framework-for-neural-implicit-representations-in-pytorch3d) · Meta AI（Wayback 存档）

2022 年 8 月 11 日

**研究内容：**神经隐式表示的快速进展，正在为增强现实体验开启激动人心的新可能。这一计算机视觉技术可以在增强现实中无缝融合真实与虚拟物体——既不需要大量数据来学习，也不局限于少数几个视角。它的做法是：利用从任意视角拍摄的物体或场景的稀疏图像组合，学习该 3D 物体或场景的表示。与网格（mesh）或点云等传统 3D 表示不同，这种较新的方法把物体表示为一个连续函数，从而对复杂几何形状实现更精确的重建，并带来更高的颜色重建精度。

Meta AI 现发布 Implicitron——我们广受欢迎的开源库 PyTorch3D 中的一个模块化框架，为推进神经隐式表示研究而创建和发布。Implicitron 提供流行隐式表示和渲染组件的抽象与实现，便于轻松实验。这一研究领域仍处于萌芽阶段，新变体层出不穷，尚无公认的首选方法。自 NeRF 问世以来，仅过去一年就发表了 50 多种用于合成复杂场景新视角的 NeRF 变体方法。Implicitron 让人们可以用一个无需 3D 或图形学专业知识的公共代码库，轻松评估这些方法的变体、组合与修改。（这些 3D 重建由五个不同的模型生成，每个模型都可在 Implicitron 中使用。）

**工作原理：**当前大多数神经隐式重建方法通过光线步进（ray marching）创建实时照片级渲染。在光线步进中，从渲染相机发出光线，并沿这些光线采样 3D 点。一个隐式形状函数（表示场景的形状与外观）随后在这些光线采样点上评估密度或到表面的距离。渲染器再沿光线点行进，找到场景表面与光线的第一个交点，以渲染图像像素。最后计算损失函数（生成图像与真实图像之间的差异）及其他指标。

基于这一通用结构，Meta 为每个组件创建了模块化、可组合的实现。这包括负责采样光线和光线点的 RaySampler 与 PointSampler 类。光线点可以用 HarmonicEmbedding 类（实现 NeRF 的位置编码）编码，也可以用 ViewSampler 编码——它在 3D 点投影的 2D 位置上采样图像特征（PixelNeRF、NeRFormer）。给定逐点特征编码，Implicitron 可以利用若干隐式形状架构之一（NeRF 的 MLP、IDR 的 FeatureField、SRN 的隐式 raymarcher）生成隐式形状。然后由渲染器（MultipassEmissionAbsorptionRenderer、LSTMRenderer、RayTracing）把隐式形状转换为图像。训练过程由若干损失监督，包括可选掩码图像之间的 MSE、PSNR 和 Huber 损失，分割掩码、深度图，以及 Eikonal 损失、预测掩码上的 Beta 先验、体素网格的 TV 正则化项等方法特定的正则化项。

这种模块化架构让框架的使用者可以轻松组合不同论文的贡献，并替换特定组件来验证新想法。作为旗舰端到端示例，Implicitron 框架实现了一种最先进的、可泛化的基于类别的新视角合成方法，如我们近期的 Common Objects in 3D 工作所提出的。它在 NeRF 的基础上扩展了一个基于 Transformer 架构的可训练视图池化层。

Meta 还开发了额外组件，让实验和扩展更加容易。这包括一个插件与配置系统，支持用户自定义组件实现以及可在实现之间灵活切换的配置；还包括一个使用 PyTorch Lightning 启动新实验的 trainer 类。

**为什么重要：**正如 Detectron2 已成为在多种数据集上实现和基准测试目标检测方法的首选框架，Implicitron 力求成为神经隐式表示与渲染领域研究的基石。这降低了进入该领域的门槛，带来了广阔的新探索机会。拥有能把图像数据转化为精确 3D 重建的更好工具，对加速 AR/VR 研究至关重要。这将催生实用的现实应用，比如让人们在 AR 和 VR 购物时虚拟试穿服装，或从不同视角重温难忘时刻。这项工作与 Meta 在 Detectron2（另一个支持目标检测、分割及其他视觉识别任务的 Meta AI 开源平台）、Common Objects in 3D、最先进的 3D 内容理解、自监督学习与 Transformer 以及卷积神经网络方面的进展互为补充。通过把这个框架集成到 3D 深度学习领域研究者已广泛使用的流行 PyTorch3D 库中，Meta 希望让框架使用者可以轻松安装并把 Implicitron 的组件导入自己的项目，而无需重新实现或复制代码。

PyTorch3D 代码 / Common Objects in 3D

我们感谢 Meta AI 此处从事 PyTorch3D 工作的更广泛研究者群体对 Implicitron 的贡献。

作者：
- David Novotny，研究科学家
- Roman Shapovalov，软件工程师
- Jeremy Reizenstein，研究工程师
- Krzysztof Chalupka，计算机视觉工程师
- Nikhila Ravi，软件工程师
- Patrick Labatut，研究工程经理
