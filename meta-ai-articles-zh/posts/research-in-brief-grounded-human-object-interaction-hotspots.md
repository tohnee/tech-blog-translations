---
title: "研究简报：接地的人-物体交互热点"
title_en: "Research in Brief: Grounded Human-Object Interaction Hotspots"
date: 2019-03-15
source: https://ai.facebook.com/blog/research-in-brief-grounded-human-object-interaction-hotspots
crawled: 2026-09-22
translated: 2026-09-22
---

# 研究简报：接地的人-物体交互热点

> 原文：[Research in Brief: Grounded Human-Object Interaction Hotspots](https://ai.facebook.com/blog/research-in-brief-grounded-human-object-interaction-hotspots) · Meta AI（Wayback 存档）

**研究内容：** 一种通过向 AI 展示日常人类行为视频来教它如何与物体交互的新方法。与依赖人工标注的各类动作示例（即监督数据）的类似交互研究不同，这项工作提出：人们与物体交互的视频可以作为弱监督数据。这些视频提供了系统理解如何成功与物体交互所需的许多线索。这使系统能够外推，既提升识别物体的能力，也提升对未曾训练过的新物体如何交互的理解。

**工作原理：** 这项研究的目标是教系统理解交互热点（interaction hotspots），即给定物体上最能解释人类如何与之交互的特定部位。这一过程始于一个视频动作分类器，它经训练可识别各类动作。接着训练所得模型去预测物体被使用时的样子，最后将其改造为生成交互热点图——既针对训练中见过的物体和动作，也针对新物体。在实验中，使用热点图要么追平、要么超越了训练监督程度显著更高的相关基线和最先进系统。这一方法还表明，交互热点可以提供关于物体功能的有用提示。例如，通过理解「能摆动打开的物体是门状的」，训练好的模型可以将以类似方式交互的新物体归类，并想象新的交互方式。

**为什么重要：** 要弥合当今图像识别系统的被动感知与明日虚拟及机器人助手的交互式、具身化能力之间的鸿沟，AI 必须学习的不仅是物理世界看起来怎样，还有它如何运转。除了展示交互热点如何编码物体功能相似性（尤其是在训练有限的情况下）之外，这项研究的弱监督性质表明，系统可以通过观察更好地理解物体与动作之间的关系。鉴于系统要与人充分交互所需的动作和物体数量之巨，这一通用策略为训练 AI 驱动智能体的更大目标带来了希望。

阅读完整论文：Grounded Human-Object Interaction Hotspots from Video（从视频中接地的 人-物体交互热点）
