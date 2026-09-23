---
title: "基于李雅普诺夫的安全强化学习算法方法"
title_en: "A Lyapunov-based approach for safe reinforcement learning algorithms"
date: 2019-02-07
source: http://ai.facebook.com/blog/lyapunov-based-safe-reinforcement-learning
crawled: 2026-09-22
translated: 2026-09-22
---

# 基于李雅普诺夫的安全强化学习算法方法

> 原文：[A Lyapunov-based approach for safe reinforcement learning algorithms](http://ai.facebook.com/blog/lyapunov-based-safe-reinforcement-learning) · Meta AI（Wayback 存档）

**这项研究是什么：**一种在训练与部署期间都考虑智能体安全的强化学习（RL）方法。在许多序列决策问题中，智能体在优化长期表现的同时避免产生不安全策略非常重要——无论训练过程中还是收敛之后。在这类问题中，不安全的策略可能对智能体（例如机器人）或环境（工厂或附近工作的人）造成损害。在这项工作中，我们首先通过施加约束来形式化安全性，然后提出一类强化学习算法，它们：1) 学到最优的安全策略；2) 即使在训练期间也不产生违反约束的策略（不安全策略）。我们算法的主要特点是用李雅普诺夫（Lyapunov）函数——控制理论中广泛用于分析动力系统稳定性的概念——来保证安全。

**工作原理：**我们首先把安全序列决策问题形式化为受约束马尔可夫决策过程（CMDP）。目标是学习最优可行策略，同时确保训练期间只执行可行策略。我们提出一种基于线性规划的算法，针对 CMDP 约束构造李雅普诺夫函数，再利用这些函数的性质开发动态规划（DP）算法求解 CMDP。

**贡献 1：**假设 CMDP 已知且有限，我们提出两种安全 DP 算法：安全策略迭代（safe policy iteration）与安全值迭代（safe value iteration）。我们分析了这些算法并证明：1) 算法各次迭代生成的策略都是安全的且单调改进；2) 在某些技术假设下，算法可达到最优。我们在基准 2D 迷宫的规划任务上评估了算法，结果表明在平衡性能与约束满足方面优于常见基线。

**贡献 2：**为处理未知且大规模（或连续）的 CMDP，我们提出两种近似 DP 算法：safe DQN 与 safe DPI。为评估这些算法，我们重复了上述实验，但这次假设模型未知，且状态空间是迷宫的航拍像素图像而非智能体的 (x, y) 坐标。结果依然表明，我们的算法在平衡性能与约束满足方面优于基线。

本工作提出的安全 RL 算法均基于值函数，因此难以处理动作空间大或连续的问题。在后续工作中，我们把该方法扩展为更适合连续动作问题的算法，并在若干模拟机器人运动任务以及一个真实室内机器人导航问题中评估了其性能。

**为什么重要：**我们的工作是朝着用 RL 解决现实问题迈出的一步——在现实中，出于安全考虑，有时必须对智能体的行为施加约束。这项研究有助于消除阻碍 RL 算法广泛应用的一个重要障碍：缺乏既能在训练期间保证智能体安全、又能返回安全且表现良好策略的算法。我们相信这项工作有助于设计在安全与性能之间取得良好平衡的 RL 算法。

阅读完整论文：A Lyapunov-based approach to safe reinforcement learning

**作者**

- Mohammad Ghavamzadeh，研究科学家，Facebook AI
