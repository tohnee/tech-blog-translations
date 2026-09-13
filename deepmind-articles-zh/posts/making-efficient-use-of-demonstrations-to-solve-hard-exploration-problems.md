---
title: "高效利用示范解决高难度探索问题"
title_en: "Making Efficient Use of Demonstrations to Solve Hard Exploration Problems"
source: https://deepmind.google/blog/making-efficient-use-of-demonstrations-to-solve-hard-exploration-problems/
site: deepmind
date: 2019-09-05
crawled: 2026-09-13
translated: 2026-09-13
---

# 高效利用示范解决高难度探索问题

> 原文：[Making Efficient Use of Demonstrations to Solve Hard Exploration Problems](https://deepmind.google/blog/making-efficient-use-of-demonstrations-to-solve-hard-exploration-problems/) · Google DeepMind

![六张游戏截图组成的网格，展示 Hard Eight 任务套件中各种 3D 房间环境。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6228bc30b71ebc05d2d0b6cb_Fig201.gif)

我们提出了一种新的智能体，称为 Recurrent Replay Distributed DQN from Demonstrations（R2D3）。R2D3 的设计目标是高效利用示范（demonstrations），来解决初始条件高度可变的部分可观测环境中的稀疏奖励任务。R2D3 智能体的架构如下所示。系统包含多个 actor 进程，每个进程都运行一份独立的行为副本，与一个环境实例交互。每个 actor 把它的经验流式传输到一个共享的智能体重放缓冲区，在那里，来自所有 actor 的经验被聚合起来并进行全局优先级排序。各 actor 会定期从 learner 进程请求最新的网络权重，以更新自身行为。

![R2D3 智能体的系统架构图：多个 actor 把轨迹流式传输到智能体重放缓冲区；一个 learner 进程同时从智能体重放缓冲区和示范重放缓冲区采样训练批次，通过双重 Q 学习进行优化并更新优先级。](https://lh3.googleusercontent.com/-u3hLQ-5nxjWDF8UoQ5nA7T9Em6wQjSv8-0IAXobJYXSkKBCVWe8JD_ETyaIrDGF1qXoNnaz0WzVtT43SO8YlPazA1brxciuFz9pqWGF-96o8pmHYQ=w1440)

如图所示，R2D3 有两个重放缓冲区：一个智能体重放缓冲区和一个示范重放缓冲区，后者填充了待解决任务的专家示范。为智能体经验和专家示范维护各自独立的重放缓冲区，使我们能够分别对智能体数据和专家数据的采样设置优先级。learner 进程同时从智能体重放缓冲区和示范重放缓冲区采样数据批次。示范比例（ρ）控制着数据来自专家示范与来自智能体自身经验的比例。示范比例是在批次层面实现的：以概率 ρ 独立地随机决定是否从专家重放缓冲区采样。当 ρ=0 时，R2D3 执行标准 RL；当 ρ=1 时，R2D3 在示范缓冲区的数据上执行批量 RL。损失由 learner 通过 n 步双重 Q 学习（n=5）和决斗（dueling）架构进行优化。

在每个重放缓冲区中，我们存储固定长度的 (s, a, r) 元组序列，相邻序列之间重叠 40 个时间步。这些序列从不跨越回合（episode）边界。给定单个轨迹批次后，我们将在线网络和目标网络在同一状态序列上展开，以生成价值估计，并将循环状态初始化为零。

## Hard Eight 任务套件

Hard Eight 任务套件中的任务要求智能体执行一系列高层技能，以获得一个大苹果——获得该苹果即可得到奖励并结束本回合。在下图中，我们给出了 Baseball 任务的一个示例。智能体必须学会把这些高层技能作为环境中一系列低层动作来执行。低层动作的序列可能相当长，因此该任务不太可能通过随机探索解决。需要说明的是，这个任务中的每一步都涉及与环境中的物理对象交互，这些对象以粗体显示。

![八幅面板，展示插画的流程：找到球棒、把它捡起、把球从基座上击飞、捡起球、激活传感器、打开门、穿门而过、收集苹果。](https://lh3.googleusercontent.com/TGqG8Mg5GHgMWJvNSh-UtAlk95K86aojS1CWB5oJOY5a-DtMcuWbeGVJ-zM_V5Ryg8Rk-BJds7zCUIGhK3XDquQXRvPk2xJS3IGXmBe3YDtI1uOONg=w1440)

在下图中，对于每个任务，智能体（蓝色三角形）必须与其环境中的对象交互，才能获得提供奖励的大苹果（红色三角形）。我们的 3D 环境是程序化生成的，因此在每个回合中，世界的状态——如对象的形状、颜色和位置——都各不相同。环境是部分可观测的，这意味着智能体在每个时间步只能看到环境的一部分。由于智能体只有在回合结束时才收到奖励，且需要执行一长串动作，探索可能相当困难。此外，高度可变的初始条件以及智能体可以交互的对象，会让探索更加困难。

![八个不同的 3D 模型，分别标注为棒球（baseball）、吊桥（drawbridge）、导航立方体（navigate cubes）、推方块（push blocks）、记忆传感器（remember sensor）、投掷穿越（throw across）、墙壁传感器（wall sensor）和墙壁传感器堆叠（wall sensor stack）。所有环境中都可见一个红色三角形和一个蓝色三角形。](https://lh3.googleusercontent.com/fSSdk1-SRlxfgbrdkEqM92h1wsXDy5hbEIfy26Wz0V8LENz0cEcJYWC1o7bt-lJxXo8bU9hDx1Oe1EIKZJWZIn8xon3wjGvbLRO9nv7RweuD82RCBQ=w1440)

## 人类示范任务

下面是一个视频播放列表，共八段视频，展示了人类执行每项任务以演示其中步骤的过程。

## R2D3 在 Hard Eight 任务上的表现

下面是一个视频播放列表，收录了 R2D3 智能体在这些任务上分别训练后的八段代表性视频。

## R2D3 的补充结果

我们运行了一些补充实验——见下方播放列表——以获取关于 R2D3 未能解决或解决得不正确的任务的更多信息。

### Remember Sensor（记忆传感器）

这个任务需要很长的记忆，其回合长度是该套件所有任务中最长的。为了缓解这些问题，我们以更高的动作重复次数 4 来训练智能体，从而缩短回合长度，并使用非零的过期 LSTM 状态（而非零初始化的 LSTM 状态），以提供回合早期阶段的信息。这使得 R2D3 能够学到表现出合理行为的策略。

### Throw Across（投掷穿越）

为该任务收集的示范成功率非常低，仅为 54%。我们尝试通过额外收集 30 条示范来弥补。当我们用全部 130 条示范训练 R2D3 时，所有随机种子都解决了该任务。

### Wall Sensor Stack（墙壁传感器堆叠）

最初的 Wall Sensor Stack 环境存在一个 bug，R2D3 智能体曾利用了这个漏洞。我们修复了该 bug，并验证了智能体能够学会正确的堆叠行为。

**注释**

我们感谢 DeepMind Worlds 团队的以下成员为本文开发任务：Charlie Beattie、Gavin Buttimore、Adrian Collister、Alex Cullum、Charlie Deck、Simon Green、Tom Handley、Cédric Hauteville、Drew Purves、Richie Steigerwald 和 Marcus Wainwright。
