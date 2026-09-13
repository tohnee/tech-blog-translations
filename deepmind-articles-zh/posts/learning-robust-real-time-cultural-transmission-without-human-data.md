---
title: "在无人类数据的情况下学习鲁棒的实时文化传承"
title_en: "Learning Robust Real-Time Cultural Transmission without Human Data"
source: https://deepmind.google/blog/learning-robust-real-time-cultural-transmission-without-human-data/
site: deepmind
date: 2022-03-03
crawled: 2026-09-13
translated: 2026-09-13
---

# 在无人类数据的情况下学习鲁棒的实时文化传承

> 原文：[Learning Robust Real-Time Cultural Transmission without Human Data](https://deepmind.google/blog/learning-robust-real-time-cultural-transmission-without-human-data/) · Google DeepMind

千百年来，人类发现、演化并积累了丰富的文化知识，从航海路线到数学，从社会规范到艺术作品。文化传承——定义为在个体之间高效传递信息——正是人类能力指数级增长背后的继承过程。

我们的智能体（蓝色）模仿并记住两个演示者的动作——机器人（左）和人类（右）为红色。

更多智能体实际运作的视频，请访问我们的[网站](https://sites.google.com/view/dm-cgi)。

在这项工作中，我们使用深度强化学习生成了具备测试时文化传承能力的人工智能体。训练完成后，我们的智能体能够推断并回忆专家演示的导航知识。这种知识传递实时发生，并能泛化到广阔的此前未见过的任务空间。例如，我们的智能体可以通过观察单次人类演示快速学会新行为，而从未在人类数据上训练过。

![强化学习环境示意图，包含程序化生成的 3D 世界、红色的"专家"（Expert）与蓝色的"MEDAL-ADR"智能体玩家、可用的动作与传感器，以及复杂导航游戏的示例。](https://lh3.googleusercontent.com/kMuCeakChRUqxlFuWtuXEwMZ4oqLxxjf9qK43ZPZme0MStAVHgebEptMvy4s36jN-wKdyzBIKuwKZjjb_1iaK0M7F-p14eOa1VQn_1XnwbjUaq1elw=w1440)

我们强化学习环境的概览。这些任务代表了一大类人类技能中的导航性任务，它们需要特定的战略性决策序列，例如烹饪、寻路和问题解决。

我们在程序化生成的 3D 世界中训练和测试智能体，世界内嵌着彩色的球形目标，地形嘈杂且充满障碍。玩家必须按正确顺序经过这些目标，而顺序在每个回合中随机变化。由于顺序无法猜测，朴素的探索策略会招致大量惩罚。作为文化传递信息的来源，我们提供了一个拥有特权的"机器人"（bot），它总是按正确顺序进入目标。

![折线图，横轴为以小时计的训练时间，纵轴为文化传承性能，比较 MEDAL 智能体（蓝色实线）与 ME-AL（橙色虚线）及最佳种子（Best seed，灰色实线）。MEDAL 随时间展现的文化传承性能高于 ME-AL。](https://lh3.googleusercontent.com/Bw02zYeKnwjZRkUXOJlX8rCwxlGXzJVHZbgST72X56JKBIYFIYkGRtZ89dTsMlzELELGV1u9OnqZaBtPvzaq_Cz8dzEGp3DxTi7_tcXzyOPTGZaohA=w1440)

![折线图，比较不同智能体架构在 250 多小时训练中的文化传承性能。MEDAL-ADR 智能体（深蓝色实线）优于其消融变体 MEDAL--DR（紫色虚线）和 MEDAL----（粉色点划线），仅略低于"最佳种子"基线（细灰色实线）。](https://lh3.googleusercontent.com/2JzDYGMIPOHUwH62XG9awAs5rkRBAtb8iC2hBarwS0OZ7FcnKT5n1JyiyJ4xBnAtqpdOaIPwABArXMfdh5UqWhscwoOresrR8_dAOiVfdBgIm1Ioqg=w1440)

我们的 MEDAL(-ADR) 智能体在留出任务上优于各消融版本，涵盖无障碍世界（上）和有障碍世界（下）。

通过消融实验，我们确定了一组使文化传承得以涌现的最小充分"入门套件"，称为 MEDAL-ADR。这些组件包括记忆（M）、专家dropout（ED）、对专家的注意力偏置（AL）以及自动域随机化（ADR）。我们的智能体在一系列具有挑战性的留出任务上优于各消融版本，包括最先进的方法（ME-AL）。文化传承在分布之外泛化得惊人地好，而且即使专家早已离开，智能体仍能长久记住演示。深入观察智能体的"大脑"，我们发现了一些显著可解释的神经元，它们负责编码社会信息和目标状态。

![柱状图，评估文化传承的泛化能力，绘制 4 目标、5 目标和 6 目标游戏配置在不同路径经过次数下的归一化得分。实心蓝色柱代表分布内任务（5 目标），带纹理的蓝色柱代表分布外任务（4 目标和 6 目标），并与完美跟随（1.0 处的红色虚线）和完美记忆（2.0 处的蓝色点线）基线进行比较。](https://lh3.googleusercontent.com/6A8VBVW2-U3zlscxjOzlVBM8mrwCHvL1IYCbrEFaDWM_L5vUU-FJkBHJGnlyuISPpgmi_OKQ5Y9P5zW8Md5DeH2TR4egnqUGUMXq47PRfJnGa-typvI=w1440)

![折线图，展示智能体神经激活随回合步数的变化。在前半段，专家在场时（深蓝色点），激活平均约为 0.00。在后半段，专家离场时（橙色点），激活跳升并稳定在 0.15 左右。](https://lh3.googleusercontent.com/ose4b2I2r9QyANTNZmxTPicVrWtFKDMHg93ceb2KsBjUvacPyzUQH9Mb2D25yfXaaIyhKtXzVc0tz1WAQ0kDPKSLZRbVBxDqNqh5Iuh7YlbabS1UD2E=w1440)

我们的智能体在训练分布之外泛化（上），并拥有编码社会信息的单个神经元（下）。

总之，我们提供了一套训练流程，可以训练出具备灵活、高召回、实时文化传承能力的智能体，而训练管线中不使用任何人类数据。这为将文化演化作为发展更通用智能的人工智能体的算法铺平了道路。

这篇作者手记基于文化通用智能团队（Cultural General Intelligence Team）的联合工作，成员包括：Avishkar Bhoopchand、Bethanie Brownfield、Adrian Collister、Agustin Dal Lago、Ashley Edwards、Richard Everett、Alexandre Fréchette、Edward Hughes、Kory W. Mathewson、Piermaria Mendolicchio、Yanko Oliveira、Julia Pawar、Miruna Pîslar、Alex Platonov、Evan Senter、Sukhdeep Singh、Alexander Zacherl 和 Lei M. Zhang。

全文请见[这里](https://arxiv.org/abs/2203.00715)。
