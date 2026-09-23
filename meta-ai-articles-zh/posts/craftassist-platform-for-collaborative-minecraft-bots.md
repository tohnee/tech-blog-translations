---
title: "CraftAssist：在 Minecraft 中实现协作式 AI 机器人的平台"
title_en: "CraftAssist, a platform for collaborative AI bots in Minecraft"
date: 2019-07-18
source: http://ai.facebook.com/blog/craftassist-platform-for-collaborative-minecraft-bots
crawled: 2026-09-22
translated: 2026-09-22
---

# CraftAssist：在 Minecraft 中实现协作式 AI 机器人的平台

> 原文：[CraftAssist, a platform for collaborative AI bots in Minecraft](http://ai.facebook.com/blog/craftassist-platform-for-collaborative-minecraft-bots) · Meta AI（Wayback 存档）

2019 年 7 月 18 日

## 这项研究是什么

一个用于实现 AI 助手的平台，这些助手能够在沙盒建造游戏 Minecraft 中与人类玩家协作。助手可以移动、放置或破坏方块、生成生物，并可以通过基于文本的聊天与人类玩家交流。通过在游戏中结合语言、感知、记忆和物理动作，这些机器人能够执行复杂任务，例如建造一座房子。发展这些技能有助于让研究者更接近更广泛的人机协作。该平台旨在支持对这类智能体的研究——它们既有趣、可以交互，又能完成由人类参与者指定和评估的多种多样任务。

为了鼓励更广泛的 AI 研究社区将 CraftAssist 平台用于自己的实验，我们开源了该框架，以及一个基线助手和我们构建它时所用的工具与数据。本次发布包括人类玩家在 Minecraft 中逐步建造房屋的序列步骤数据、这些房屋的语义分割数据，以及一个大规模自然语言语义解析数据集。

## 它是如何工作的

玩家可以通过标准的 Minecraft 客户端与这些助手交互，多个人类玩家和机器人可以在同一局游戏中相互配合。CraftAssist 使用开源、可扩展的 Minecraft 兼容游戏服务器 Cuberite，使研究者能够记录游戏会话（包括所有游戏内语言和动作），以生成自己的训练数据。

我们在 CraftAssist 中附带的基线助手，是在与该助手此前版本交互的人类数据集、以及众包的人类参与者在 Minecraft 中建造超过 2500 座不同房屋的示例数据集上训练的。这两个训练集都已包含在本次开源发布中。

我们基线助手的设计是模块化的，研究者既可以使用完整的机器人做实验，也可以专注于与记忆、感知和语言理解相关的单个组件。这些模块协同完成任务。例如，如果人类要求机器人「在蓝色立方体旁边建一座房子」，语言理解模块——一个神经语义解析器——会使用该聊天输入生成一个基于高级动作原语的程序。它会确定所请求的高级动作，例如先「移动」到指定目的地、随后「建造」。然后记忆模块会在机器人的记忆中查询已存储的对象，例如被标记为「蓝色」和「立方体」的对象，并创建一个以蓝色立方体坐标为目标的移动任务。这让机器人得以根据我们数据集中的建房示例，使用一系列「移动」和「建造」任务开始建造房屋。

## 为什么它重要

从长远来看，这项工作旨在让 AI 助手具备更广泛的能力——尤其是更高的灵活性。尽管机器学习（ML）方法已经在困难但定义狭窄的任务上取得了令人印象深刻的性能，但构建能在大量不同任务（尤其是人类用语言指定的任务，有时表述还很模糊）上都表现出色的系统，仍然是一项重要挑战。我们的立场论文详述了我们通过 Minecraft 研究这些系统的动机（下面链接的白皮书聚焦于该框架的技术层面）。在 Minecraft 中探索所得的经验，有助于催生能够在各种真实场景中更好地与人类交互和协作的 AI 助手，并通过这些交互主动学习新的概念与技能。

**阅读完整论文：** CraftAssist: A framework for dialogue-enabled interactive bots

**作者**

- Kavya Srinet，Facebook AI 研究工程师
- Jonathan Gray，Facebook AI 研究工程师
- Larry Zitnick，Facebook AI 研究科学家
- Arthur Szlam，Facebook AI 研究科学家
