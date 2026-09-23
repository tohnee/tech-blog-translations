---
title: "训练 AI 智能体解决陌生任务"
title_en: "Training AI agents to solve unfamiliar tasks"
date: 2018-10-01
source: https://ai.facebook.com/blog/training-ai-agents-to-solve-unfamiliar-tasks
crawled: 2026-09-22
translated: 2026-09-22
---

# 训练 AI 智能体解决陌生任务

> 原文：[Training AI agents to solve unfamiliar tasks](https://ai.facebook.com/blog/training-ai-agents-to-solve-unfamiliar-tasks) · Meta AI（Wayback 存档）

2018 年 10 月 1 日

**研究内容：**可组合规划（composable planning）是一种构建更擅长解决陌生任务的 AI 智能体的新方法。传统训练是让智能体一次反复练习某一个特定任务。为了铺就更通用的 AI，这种新方法聚焦于在给定环境中用一组简单、相关的任务训练智能体，使其随后能够执行更长、更复杂的任务。

**工作原理：**智能体基于研究者赋予的属性学习其环境模型，然后学会在这个带标注的环境中执行一系列基本任务。之后，它用这一模型来规划所面对的新任务。举例来说，如果用这种方法教 AI 智能体烹饪，它可能会学习厨房的总体布局以及若干适用于各种菜肴的简单子任务（如打蛋）。

**为什么重要：**为每个可想见的任务训练一个单独的智能体并不现实。可能任务的数量已经大到无法穷尽，而随着 AI 日益普及，系统必然会遇到训练时未知的任务。这种新方法产出的智能体能够组合简单的单步任务，去执行更长、更复杂的任务组合。这是一项基础研究，有助于把自主智能体的最先进水平从今天的单一用途系统，推向适应性更强的 AI。

**阅读完整论文：**Composable Planning with Attributes
