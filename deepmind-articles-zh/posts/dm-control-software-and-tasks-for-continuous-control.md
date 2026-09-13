---
title: "dm_control：面向连续控制的软件与任务"
title_en: "dm_control: Software and Tasks for Continuous Control"
source: https://deepmind.google/blog/dm-control-software-and-tasks-for-continuous-control/
site: deepmind
date: 2020-06-15
crawled: 2026-09-13
translated: 2026-09-13
---

# dm_control：面向连续控制的软件与任务

> 原文：[dm_control: Software and Tasks for Continuous Control](https://deepmind.google/blog/dm-control-software-and-tasks-for-continuous-control/) · Google DeepMind

## 概览

包含 dm\_control 软件教程的公开 Colab 笔记本可在[这里](https://colab.sandbox.google.com/github/deepmind/dm_control/blob/master/tutorial.ipynb)获取。

## 基础设施

- 一个自动生成的 MuJoCo Python 封装层，提供对底层引擎的完整访问。
- PyMJCF 是一个文档对象模型（DOM），其中 Python Entity 对象的层级结构与 MuJoCo 模型元素一一对应。
- Composer 是高层「游戏引擎」，它简化了把 Entity 组合成场景的过程，以及定义观测、奖励、终止条件和通用游戏逻辑的过程。
- Locomotion（运动）框架引入了若干抽象的 Composer 实体，例如 Arena 和 Walker，为运动类任务提供了便利。

## 环境

- [Control Suite](https://www.youtube.com/watch?v=rAai4QzcYbs)，其中包括全新的[四足机器人](https://www.youtube.com/watch?v=RhRLjbb7pBE&t=5s)与[狗](https://www.youtube.com/watch?v=i0_OjDil0Fg)环境。
- 多种运动任务，包括足球。
- 使用可拼搭积木的单臂机器人操作任务。

## 按名称索引

利用 MuJoCo 对所有模型元素名称的支持，我们允许用字符串对数组进行索引和切片。因此，不必再写：

"fingertip\_height = physics.data.geom\_xpos[7, 2]"

……这种晦涩、脆弱的数值索引，你可以写成：

"fingertip\_height = physics.named.data.geom\_xpos['fingertip', 'z']"

从而得到一个健壮得多、可读性也强得多的代码库。

## PyMJCF

PyMJCF 库创建了一个与 MuJoCo 模型一一对应的 Python 对象层级。它引入了 attach() 方法，允许模型相互附着。例如，在我们的教程中，我们通过把腿附着到身体、把生物附着到场景来创建程序化生成的多足生物。

## Composer

Composer 是「游戏引擎」框架，它定义了运行时函数调用的特定顺序，并抽象出奖励、终止与观测的能力。这些抽象让我们得以创建一些实用的子模块：

composer.Observable：一个抽象的观测包装器，可以为任意传感器添加噪声、延迟、缓冲和滤波。

composer.Variation：一组用于随机化仿真量的工具，通过模型变化实现智能体稳健化和 sim-to-real（仿真到现实）迁移。

![流程图，展示 dm_control 中 Composer 环境的运行时执行流程，包括 Environment.reset 和 Environment.step。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6231ee766a323a1793376c3b_diagram3.svg)

示意图展示 Composer 回调的生命周期。圆角矩形代表 Task 和 Entity 可以实现的回调。蓝色矩形代表 Composer 内置的操作。

## Locomotion

Locomotion 框架引入了以下抽象：

Walker：一个可控实体，带有常见的与运动相关的方法，例如把向量投影到以自身为中心的坐标系。

Arena：一个可自动调整规模的随机化场景，可以把 walker 放置其中并交给它一个要执行的任务。

例如，只需 4 次函数调用，我们就可以实例化一个人形 walker、一个 WallsCorridor 场景，并把它们组合成一个 RunThroughCorridor 任务。

## 四足机器人（Quadruped）

- 一个具有被动稳定身体的通用四足领域。
- 若干纯运动任务（例如行走、奔跑）。
- 一个需要崎岖地形导航的逃生任务。
- 一个需要带球盘带的取物任务。

## 狗（Dog）

- 一个精细的模型，其骨架由 [leo3Dmodels](https://www.turbosquid.com/Search/Artists/leo3Dmodels) 受托制作。
- 一个具有挑战性的捡球任务，需要用嘴进行精确抓取。

## 展示

一段由 DeepMind 基于 dm\_control 任务制作的快节奏集锦：
