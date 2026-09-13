---
title: "RL Unplugged：离线强化学习基准"
title_en: "RL Unplugged: Benchmarks for Offline Reinforcement Learning"
source: https://deepmind.google/blog/rl-unplugged-benchmarks-for-offline-reinforcement-learning/
site: deepmind
date: 2020-06-24
crawled: 2026-09-13
translated: 2026-09-13
---

# RL Unplugged：离线强化学习基准

> 原文：[RL Unplugged: Benchmarks for Offline Reinforcement Learning](https://deepmind.google/blog/rl-unplugged-benchmarks-for-offline-reinforcement-learning/) · Google DeepMind

![一幅动态图，标题为「在线强化学习」。左侧是一个机器人头部表情符号，下方写着「智能体」。一条标为「动作」的红色箭头从左向右指向一个标注为「环境」的地球表情符号；一条标为「状态、奖励」的红色箭头从右向左指回机器人。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6231efbede9e9af7f611ff68_fig201.gif)

![一幅动态图，标题为「离线强化学习」。左侧是一个机器人头部表情符号，下方写着「智能体」。右侧是一个标注为「记录数据」的圆柱体。一条标为「状态、动作、奖励」的红色箭头从圆柱体由右向左指向机器人。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6231efcc337d93e52e2e23b2_fig202.gif)

强化学习（RL）的许多成功都严重依赖于智能体与环境的反复在线交互，我们称之为在线 RL。尽管强化学习在仿真中取得了成功，它在现实应用中的采用仍然有限。发电厂、机器人、医疗系统或自动驾驶汽车的运行成本高昂，不当的控制可能带来危险的后果。它们与 RL 中至关重要的探索思想以及在线 RL 算法的数据需求并不容易兼容。尽管如此，大多数现实系统在正常运行过程中都会产生大量数据，而离线 RL 的目标正是直接从这些记录数据中学习策略，而无需与环境交互。

离线 RL 方法（例如 Agarwal et al., 2020；Fujimoto et al., 2018）已在一些著名的基准领域展示了有希望的结果。然而，评估协议不标准化、数据集各不相同以及缺乏基线，使算法之间的比较变得困难。与此同时，一些潜在现实应用领域的重要特性——如部分可观测性、高维感官流（即图像）、多样的动作空间、探索问题、非平稳性和随机性——在当前的离线 RL 文献中体现不足。

我们引入了一套新的任务域集合及配套数据集，并附带清晰的评估协议。其中既包括广泛使用的领域，如 DM Control Suite（Tassa et al., 2018）和 Atari 2600 游戏（Bellemare et al., 2013），也包括对强大的在线 RL 算法仍具挑战性的领域，如现实世界 RL（RWRL）套件任务（Dulac-Arnold et al., 2020）和 DM Locomotion 任务（Heess et al., 2017；Merel et al., 2019a,b, 2020）。通过对环境、数据集和评估协议进行标准化，我们希望让离线 RL 的研究更具可复现性和可及性。我们把这组基准命名为「RL Unplugged」，因为离线 RL 方法使用它时不需要任何智能体与环境交互。我们的论文提供了四项主要贡献：（i）统一的数据集 API；（ii）多样的环境集合；（iii）面向离线 RL 研究的清晰评估协议；（iv）参考性能基线。
