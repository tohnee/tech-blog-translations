---
title: "MiniHack：面向开放式强化学习的新沙盒"
title_en: "MiniHack: A new sandbox for open-ended reinforcement learning"
date: 2021-09-29
source: https://ai.facebook.com/blog/minihack-a-new-sandbox-for-open-ended-reinforcement-learning
crawled: 2026-09-22
translated: 2026-09-22
---

# MiniHack：面向开放式强化学习的新沙盒

> 原文：[MiniHack: A new sandbox for open-ended reinforcement learning](https://ai.facebook.com/blog/minihack-a-new-sandbox-for-open-ended-reinforcement-learning) · Meta AI（Wayback 存档）

强化学习（RL）已成为解决序贯决策问题的宝贵工具，相关研究涵盖机器人、内容个性化到改进 MRI 扫描等方向。RL 的进步通常由模拟基准驱动，但既有基准（如 Arcade Learning Environment 和 MuJoCo）正趋于饱和——研究者开发的算法在这些任务上已接近最优。ProcGen、Minecraft、NetHack 等新基准将帮助 RL 研究社区构建强大的新算法，但在这些复杂丰富的环境中，很难厘清究竟在测试哪类问题。这些由完整游戏构成的测试平台，并非为评估 RL 智能体的特定能力（如探索、记忆和信用分配）而显式设计。理想情况下，从业者应当能够针对特定研究问题定义一个由高度受控任务组成的广阔宇宙，并轻松通过提升复杂度和丰富度来调整它们，而无需任何繁重的工程工作。

为填补这一空白，我们构建了 MiniHack——一个环境创建框架及配套任务套件，基于世界上最难的游戏之一 NetHack。借助这一工具，工程师可以轻松创建一个挑战现代 RL 方法、并针对 RL 内特定问题的任务宇宙。MiniHack 现已开源并在 GitHub 上提供。研究者可以使用我们的详细文档学习如何使用 MiniHack，并在这篇 NeurIPS 2021 论文中了解项目更多细节。

## 轻松创建复杂的问题求解任务

MiniHack 使用 NetHack 学习环境（NLE），为环境设计者提供了一种便捷手段，把这款游戏的丰富性用于复杂 RL 任务。这个新沙盒自带游戏中的大量既有素材，例如 500 多种怪物和 450 多种物品（包括武器、魔杖、工具和法术书），它们都具有独特的属性和复杂的环境动态。该框架让 RL 从业者得以超越动作空间有限的简单网格世界式导航任务，转而应对更复杂的技能习得与问题求解任务。

为此，MiniHack 利用了 NetHack 中用于描述地牢的所谓「描述文件」。描述文件使用一种人类可读、类似概率编程的领域特定语言（DSL）编写。只需几行代码，人们就能生成大量多样的环境，控制每一个细节——从怪物的位置和类型，到关卡的陷阱、物件和地形——同时引入随机性来挑战 RL 智能体的泛化能力。描述文件让人们在几行代码内构建多样的 MiniHack 环境。该 DSL 对环境局部的欠规范（underspecification）和随机生成函数提供一等支持。这意味着每当环境重置、智能体开启新的一轮（episode）时，其所在的关卡都可能显著不同。这种程序化内容生成让 MiniHack 能够评估 RL 在前所未见情境下的泛化能力，从而训练出更鲁棒、更通用的智能体。对于没有时间学习描述文件细节的研究者，我们还提供了一个用 Python 描述整个环境的便捷接口。

## MiniHack 环境

（图为各种 MiniHack 任务的截图。）采用流行 Gym 接口的 MiniHack 环境的一切都高度可定制。用户可以轻松选择智能体接收何种观测（例如基于像素的、符号的或文本的），以及它可以执行哪些动作。此外，我们提供便捷接口来指定引导智能体学习的自定义奖励函数。我们还用 MiniHack 构建了一套 RL 任务，用于测试 RL 智能体的核心能力，并将其作为 MiniHack 的一部分发布。这套任务可以像任何其他 RL 基准一样使用。此外，这些任务也可作为积木，供希望开发新任务的研究者使用。（图为 MiniHack 中的像素、符号和文本观测。）

MiniHack 还能把既有的基于网格的基准汇集到同一屋檐下。我们展示了 MiniGrid 和 Boxoban 等此前测试平台如何移植到 MiniHack。得益于 MiniHack 的灵活性与丰富性，可以通过添加额外实体、环境特征和随机性来提升它们的难度。

## 让 MiniHack 投入使用

为特定深度 RL 研究问题创建丰富复杂的环境，从未如此容易。MiniHack 的目标是分离式地测试 AI 智能体的特定能力，包括探索、记忆和语言辅助 RL。该框架可用于 NetHack Challenge 竞赛——FAIR 正在 NeurIPS 2021 上共同组织该赛事。

作为上手指南，我们提供了基于 TorchBeast 和 RLlib 等框架的多种基线。此外，我们还演示了如何以无监督方式用 MiniHack 设计环境，并以最近提出的 PAIRED 算法为例。我们还为我们的实验在 Weights & Biases 中提供了基线学习曲线。

总而言之，我们相信 MiniHack 将帮助研究者快速迭代想法，并系统地提升基准任务的难度。要开始使用，请查看 MiniHack 教程。MiniHack 已开源并在 GitHub 上提供。使用我们的详细文档学习如何使用 MiniHack。查看 MiniHack NeurIPS 2021 论文。

我们要感谢伦敦大学学院博士生 Robert Kirk 的贡献。

作者：Mikayel Samvelyan，研究助理；Tim Rocktäschel，研究科学家
