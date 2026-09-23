---
title: "AI Habitat：最先进的仿真平台新增物体交互能力"
title_en: "AI Habitat: A state-of-the-art simulation platform adds object interactivity"
date: 2020-01-21
source: https://ai.meta.com/blog/ai-habitat-state-of-the-art-simulation-platform-adds-object-interactivity/
crawled: 2026-09-22
translated: 2026-09-22
---

# AI Habitat：最先进的仿真平台新增物体交互能力

> 原文：[AI Habitat: A state-of-the-art simulation platform adds object interactivity](https://ai.meta.com/blog/ai-habitat-state-of-the-art-simulation-platform-adds-object-interactivity/) · Meta AI（Wayback 存档）

**它是什么：**Facebook AI（FAIR，Meta 基础人工智能研究院）开源 AI Habitat 平台的一次重大更新，可在多种照片级真实的 3D 虚拟环境中显著加速具身 AI 智能体的训练。AI Habitat 现已支持可交互物体、逼真的物理建模、改进的渲染、从虚拟环境到物理环境的无缝迁移，以及更灵活的用户界面（支持在浏览器中运行仿真）。借助这些增强，研究者可以用 AI Habitat 训练和测试智能体——不仅是在照片级真实的虚拟环境中移动，还包括与这些环境及其中的物体进行交互。

**它做什么：**当我们去年发布 AI Habitat 时，它已兼容 Facebook Reality Labs 的 Replica 仿真（现有最照片级真实的环境 3D 重建之一）、具备灵活的模块化设计，并拥有在单个 GPU 上每秒渲染 10,000 帧的高效训练能力。除大量工具新增和性能改进外，今天的版本在既有特性基础上实现了多项重大提升：

- 研究者现在可以从库中导入物体（例如 YCB 数据集的家居物品或家具模型），并用「在这里加一把椅子」之类的指令执行程序化场景构建。
- Habitat 现通过 Bullet 物理引擎支持刚体物理，例如施加力/扭矩或检测碰撞。
- 研究者现在可以使用 Habitat-PyRobot-Bridge，在 AI Habitat 和实体机器人（如 LoCoBot）上运行同一套代码，其中包括 LoCoBot 执行器和深度传感器的逼真噪声模型。（更多细节见这篇论文。）
- Habitat 现在可以在浏览器中运行。通过以 WebGL 和 JavaScript API 在浏览器中运行 AI Habitat，研究者可以轻松比较智能体与真人的表现。
- Habitat 现提供 TensorBoard 支持，并为 Habitat 基线改进了 API 接口。
- AI Habitat 现在支持 Replica 环境中的 HDR 纹理，并对 Oculus Quest VR 提供初步支持。
- Habitat-API 新增了一项具身问答任务。

**为什么重要：**通过在虚拟世界中训练智能体，研究者可以在构建更好的 AI 助手和机器人（在物理世界的复杂情境中更智能地运作）所需的任务上取得快得多的进展。要让这种训练最有效，智能体不仅要在虚拟环境中穿行，还要能在这些空间中推、拉和操纵物体。AI Habitat 现在让高效做到这一点、进而对结果做基准测试并跨数据集比较性能变得容易。Habitat 的这些改进将加速并简化虚拟环境在开发更聪明、更强大智能体方面的使用。

在 GitHub 上获取：

- https://github.com/facebookresearch/habitat-sim
- https://github.com/facebookresearch/habitat-api

**作者**

- Alexander William Clegg，研究工程师
- Abhishek Kadian，软件工程师
- Erik Wijmans，AI 研究实习生
- Mandeep Baines，软件工程师
- Oleksandr Maksymets，研究工程师
- Yili Zhao，研究科学家
- Aaron Gokaslan，AI 驻留研究员
- Wojciech Galuba，研究工程经理
- Dhruv Batra，研究科学家
