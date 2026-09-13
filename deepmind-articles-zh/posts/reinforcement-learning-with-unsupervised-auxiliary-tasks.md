---
title: "结合无监督辅助任务的强化学习"
title_en: "Reinforcement learning with unsupervised auxiliary tasks"
source: https://deepmind.google/blog/reinforcement-learning-with-unsupervised-auxiliary-tasks/
site: deepmind
date: 2016-11-17
crawled: 2026-09-13
translated: 2026-09-13
---

# 结合无监督辅助任务的强化学习

> 原文：[Reinforcement learning with unsupervised auxiliary tasks](https://deepmind.google/blog/reinforcement-learning-with-unsupervised-auxiliary-tasks/) · Google DeepMind

DeepMind 的首要使命是推动 AI 的边界，开发无需被专门教授就能学会解决任何复杂问题的程序。我们的强化学习智能体已经在 [Atari 2600 游戏](https://deepmind.com/research/publications/human-level-control-through-deep-reinforcement-learning/)和[围棋](https://deepmind.com/research/case-studies/alphago-the-story-so-far)上取得过突破。然而，这类系统可能需要大量数据和很长的时间才能学会，因此我们一直在寻找改进通用学习算法的方法。

我们最近的论文[《Reinforcement Learning with Unsupervised Auxiliary Tasks》](https://arxiv.org/pdf/1611.05397.pdf)介绍了一种大幅提升智能体学习速度和最终性能的方法。我们的做法是：在标准的[深度强化学习](https://deepmind.com/blog/article/deep-reinforcement-learning)方法之外，为智能体增加两项在训练期间执行的附加任务。

下方是我们的智能体在 Labyrinth 迷宫觅食任务中的可视化。

![示意图，展示 DeepMind 的 UNREAL 智能体可视化：左侧「Live Play」（实时对局）面板显示在 3D Labyrinth 迷宫中导航，右侧「Auxiliary Tasks」（辅助任务）面板展示像素控制（Pixel Control）、奖励预测（Reward Prediction）和价值函数回放（Value Function Replay）。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62228b56e2b4eb57fa1e7718_Reinforcement20Learning20with20Unsupervised20Auxi.gif)

第一项任务是让智能体学会控制屏幕上的像素，它强调学习「你的动作如何影响你将看到的内容」，而不只是预测。这类似于婴儿通过移动双手并观察这些移动来学会控制自己的手。通过学习改变屏幕的不同部分，我们的智能体学到了对玩游戏、获得更高分数有用的视觉输入特征。

在第二项任务中，智能体被训练从一段简短的历史情境预测即时奖励即将出现。为了更好地应对奖励稀少的情形，我们以相等的比例向智能体呈现过去的「有奖励」历史和「无奖励」历史。通过在学习中更频繁地接触有奖励的历史，智能体能够更早发现对奖励有预测力的视觉特征。

这些辅助任务与我们之前的 [A3C 论文](https://deepmind.com/blog/article/deep-reinforcement-learning)相结合，构成了我们新的 UNREAL 智能体（UNsupervised REinforcement and Auxiliary Learning，无监督强化与辅助学习）。我们在 57 个 Atari 游戏以及一个包含 13 个关卡的 3D 环境 Labyrinth 上测试了这个智能体。在所有游戏中，同一个 UNREAL 智能体都按照相同的方式、以游戏的原始图像输出为输入进行训练，产出使智能体在游戏中的得分或奖励最大化的动作。获得游戏奖励所需的行为差异极大——从在 3D 迷宫中捡苹果到玩《太空侵略者》——而同一个 UNREAL 算法就学会了玩这些游戏，且往往达到人类水平甚至更高。

在 Labyrinth 中，使用辅助任务——控制屏幕像素并预测奖励何时出现——的结果是，UNREAL 的学习速度比我们此前最好的 A3C 智能体快 10 倍以上，并达到了好得多的性能。在我们考察的 Labyrinth 关卡上，我们现在平均能达到专家人类表现的 87%，其中若干关卡上还超过了人类水平。在 Atari 上，该智能体现在平均达到人类表现的 9 倍。我们希望这项工作能让我们把智能体扩展到越来越复杂的环境中。

**说明**

请阅读论文：[Reinforcement Learning with Unsupervised Auxiliary Tasks](https://arxiv.org/pdf/1611.05397.pdf)
