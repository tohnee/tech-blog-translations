---
title: "边玩边学"
title_en: "Learning by playing"
source: https://deepmind.google/blog/learning-by-playing/
site: deepmind
date: 2018-02-28
crawled: 2026-09-13
translated: 2026-09-13
---

# 边玩边学

> 原文：[Learning by playing](https://deepmind.google/blog/learning-by-playing/) · Google DeepMind

让孩子（以及大人）收拾好自己的东西可能已经是件难事，而我们要让 AI 智能体做到同样的事，则面临更大的挑战。成功取决于对几项核心视觉-运动（visuo-motor）技能的掌握：接近一个物体，抓住并提起它，打开一个箱子并把东西放进去。更复杂的是，这些技能必须按正确的顺序运用。

像收拾桌面或堆叠物体这样的控制任务，要求智能体决定如何、何时以及在何处协调其模拟手臂和手指的九个关节，才能正确运动并达成目标。任一时刻可能的动作组合数量之巨，加上需要执行一长串正确的动作序列，构成了一个严峻的探索问题——这也使它成为强化学习研究中一个特别有趣的领域。

奖励塑形、学徒学习或示范学习等技术可以帮助解决探索问题。然而，这些方法依赖关于任务的大量知识——在先验知识极少的情况下从零开始学习复杂控制问题，仍然是一个悬而未决的挑战。

我们的[新论文](https://arxiv.org/abs/1802.10567)提出了一种名为「调度辅助控制（Scheduled Auxiliary Control，SAC-X）」的新学习范式，力求克服这一探索难题。SAC-X 的基本理念是：要从零开始学习复杂任务，智能体必须先学会探索并掌握一组基础技能。就像婴儿必须先发展协调与平衡能力才能爬行或走路一样——为智能体提供与简单技能相对应的内部（辅助）目标，能增加它理解并执行更复杂任务的机会。

![一段动画：模拟机械臂在桌面上与红色和绿色方块互动，练习操作任务。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62267c4938ec8f7177c7d560_Learning20by20playing.gif)

我们在多个模拟和真实机器人任务上演示了 SAC-X 方法，任务包括不同物体的堆叠问题和「收拾游戏场」（把物体移进箱子）。我们定义的辅助任务遵循一个通用原则：鼓励智能体探索其传感空间。例如，激活手指上的触觉传感器、感知手腕处的力、最大化本体感觉传感器中的关节角度，或在其视觉摄像头传感器中引发物体的运动。每个任务都对应一个简单的奖励：目标达成记 1，否则记 0。

![一段动画：模拟机械臂在桌面上与红色和绿色方块互动，练习操作任务。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62267d28f70ee120ddd63bbb_unnamed_1.gif)

智能体最先学会的是激活手指上的触觉传感器并移动两个物体。

![一段动画：模拟机械臂在桌面上与红色和绿色方块互动，练习操作任务。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62267d46801fc6e300b17d42_unnamed-2.gif)

模拟智能体最终掌握了「堆叠」物体这一复杂任务。

然后，我们的智能体可以自行决定当前的「意图」，即接下来追求哪个目标。这可能是一个辅助任务，也可能是外部定义的目标任务。关键在于，通过大量使用基于回放的离策略学习，智能体能够从所有其他任务的奖励信号中发现并学习，即便它当前并未在执行这些任务。例如，在拾起或移动物体时，智能体可能顺手把物体堆叠起来，从而观察到「堆叠」的奖励。因为一串简单任务的执行可能带来对稀有外部奖励的观察，调度意图的能力至关重要。它可以基于收集到的所有顺带知识创建一个个性化的学习课程。事实证明，这是在如此大的领域内利用知识的有效方式，在外部奖励信号稀缺时尤其有用。我们的智能体通过一个调度模块决定遵循哪个意图。调度器在训练过程中通过一个元学习算法不断改进，该算法尝试最大化主任务的进展，从而显著提升了数据效率。

![一段动画：模拟机械臂在桌面上与红色和绿色方块互动，练习操作任务。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62267d63b8f50b29f6390f4c_unnamed.gif)

在探索了若干内部辅助任务之后，智能体学会了堆叠并把物体收拾好。

我们的评估表明，SAC-X 能够从零开始解决我们布置给它的所有任务——而且使用的是同一套底层辅助任务。令人兴奋的是，SAC-X 还能在我们实验室的真实机械臂上从零开始直接学会拾起和放置任务。过去这一直特别困难，因为在真实环境中的机器人学习要求数据效率，因此一种流行的做法是先在模拟中预训练智能体，再将它迁移到真实机械臂上。

![一段动画：真实机械臂在桌面上与绿色方块练习拾起和放置任务。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62267da9ac18bf6f60653b58_unnamed-3.gif)

在真实机械臂上，SAC-X 从零开始学会如何抬起并移动绿色方块，此前从未见过该任务。

我们认为，在只给定总体目标的情况下从零开始学习控制任务，SAC-X 是重要的一步。SAC-X 允许你任意定义辅助任务：它们可以基于一般性洞见（例如此处建议的刻意激活传感器），但最终也可以纳入研究者认为重要的任何任务。从这个意义上说，SAC-X 是一种通用的 RL 方法，可广泛应用于控制和机器人之外的各类稀疏强化学习场景。

**注**

论文可在[此处](https://arxiv.org/abs/1802.10567)阅读。

本工作由 Martin Riedmiller、Roland Hafner、Thomas Lampe、Michael Neunert、Jonas Degrave、Tom Van de Wiele、Volodymyr Mnih、Nicolas Heess 和 Tobias Springenberg 完成。
