---
title: "SIMMC：用于开发下一代购物助手的数据集"
title_en: "SIMMC: A dataset for developing next-generation shopping assistants"
date: 2020-08-24
source: https://ai.facebook.com/blog/simmc-a-data-set-for-developing-next-generation-shopping-assistants
crawled: 2026-09-22
translated: 2026-09-22
---

# SIMMC：用于开发下一代购物助手的数据集

> 原文：[SIMMC: A dataset for developing next-generation shopping assistants](https://ai.facebook.com/blog/simmc-a-data-set-for-developing-next-generation-shopping-assistants) · Meta AI（Wayback 存档）

2020 年 8 月 24 日

**它是什么：** 情境化交互多模态对话（Situated and Interactive Multimodal Conversations，SIMMC）是一个首创性的数据集，已经开源，用于帮助研究者和工程师开发能够在共同观察（co-observed）的多模态情境中处理复杂、面向任务的对话的虚拟助手。想象一下你正在用 AR/VR 从网上商店购买商品。让这种交互顺畅进行的最简单方式之一，是使用一个能响应你语音指令和提示（例如「我想买一张棕色皮质沙发」）的数字助手——就像实体店里的售货员可能为你提供的帮助一样。然而，AR/VR 环境的复杂性意味着助手必须能够超越简单的呼叫-应答或问答式操作。要在虚拟环境中成功运行，就意味着能够处理并记住其中固有的各种多模态输入，例如物体的视觉方面，包括颜色、尺寸、形状和朝向。如果更广泛的研究和工程社区要开发能够紧密模仿人类 counterparts 的数字助手，就需要解决一系列新颖而不平凡的研究挑战。SIMMC 是一个专门面向训练此类智能体的数据集——这些智能体在对话历史之外，还能基于共同演化的多模态输入情境采取多模态行动。SIMMC 任务针对面向任务的对话，这些对话以共同观察的图像或 VR 环境的形式包含丰富的情境化多模态用户上下文，并根据对话流程和助手动作动态更新。它使 AI 助手能够以与用户几乎相同的方式理解不断演化的交互情境。（视频加载失败提示略）

**它能做什么：** SIMMC 包含约 13,000 段人与人对话（总计约 169,000 条话语）。我们选择购物体验——具体是家具和时尚——作为 SIMMC 数据集的领域，因为购物体验创造了动态的环境，围绕视觉落地的物品发生丰富的多模态交互。与以往的多模态对话数据集相比，SIMMC 有四大关键优势：

1. SIMMC 假设用户与助手之间存在共同观察的多模态情境，并记录每个出现物品的真实物品外观日志。SIMMC 任务强调对输入模态的语义处理，而该领域的工作传统上高度侧重于原始图像处理。
2. 与传统的面向任务的对话数据集相比，SIMMC 数据集中的智能体动作跨越多样的多模态动作空间（例如「旋转」「搜索」和「加入购物车」）。
3. 智能体动作既可以在物体层面执行（例如改变场景中特定物体的视图），也可以在场景层面执行（例如引入新场景或图像）。
4. SIMMC 强调语义处理。所提出的 SIMMC 标注模式让对话的视觉落地有了更系统、更结构化的方法，这对解决真实世界场景中的挑战性问题至关重要。

在 furniture 和 fashion 数据集上训练的机器学习模型，在 API 调用预测、响应生成和对话状态跟踪方面的表现均得到评估。

**为什么重要：** 我们在第九届对话系统技术挑战赛（DSTC9）上围绕 SIMMC 组织了一个挑战赛道。该赛道邀请对话研究社区致力于开发能处理多模态输入并执行多模态动作的真实世界助手智能体。SIMMC 框架是构建下一代虚拟助手的一步，这些助手能够进行创建动态体验（如基于 AR/VR 的购物）所需的多模态推理。这类数据集也为对话式 AI 的进一步研究打开了大门，包括多模态实体消歧。我们提供了两个数据集（furniture 和 fashion），以及这些数据集上的情境化自然语言理解和共指标注，供进一步研究。针对这些数据集支持的某些任务，已有若干强基线，展示了它们在真实世界应用中的多种用途。SIMMC 目前处于研究阶段，我们相信收集的标注应能促进对这项工作强调的任务以及其他若干任务的进一步研究。

在 GitHub 获取：Situated Interactive MultiModal Conversations (SIMMC) Challenge 2020

我们感谢我们的合作者：Seungwhan Moon、Paul A. Crook、Ankita De、Shivani Poddar、Theodore Levin、David Whitney、Daniel Difranco、Eunjoon Cho、Rajen Subba 和 Alborz Geramifard

**作者**
Satwik Kottur，研究科学家
Ahmad Beirami，研究科学家
