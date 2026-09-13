---
title: "让神经网络实现持续学习"
title_en: "Enabling Continual Learning in Neural Networks"
source: https://deepmind.google/blog/enabling-continual-learning-in-neural-networks/
site: deepmind
date: 2017-03-13
crawled: 2026-09-13
translated: 2026-09-13
---

# 让神经网络实现持续学习

> 原文：[Enabling Continual Learning in Neural Networks](https://deepmind.google/blog/enabling-continual-learning-in-neural-networks/) · Google DeepMind

学会执行任务的计算机程序，通常也会很快把这些任务忘掉。我们证明，可以通过修改学习规则，让程序在学习新任务时记住旧任务。这是朝着能够渐进式、自适应学习的更智能程序迈出的重要一步。

深度神经网络是目前解决包括语言翻译、图像分类和图像生成在内多种任务的最成功的机器学习技术。然而，它们通常只有在数据一次性全部给出时，才能被设计成学习多个任务。当网络针对某个特定任务进行训练时，它的参数会为解决该任务而调整。一旦引入新任务，新的调整就会覆写神经网络之前学到的知识。这种现象在认知科学中被称为"灾难性遗忘"（catastrophic forgetting），被视为神经网络的基本局限之一。

相比之下，我们大脑的工作方式截然不同。我们能够增量式地学习，一次掌握一项技能，并在学习新任务时运用先前的知识。在我们最近的 [PNAS 论文](http://www.pnas.org/content/early/2017/03/13/1611835114.abstract)中，我们提出了一种克服神经网络灾难性遗忘的方法；作为这项工作的起点，我们从神经科学关于哺乳动物和人类大脑如何固化先前习得的技能与记忆的理论中获得了启发。

神经科学家区分了大脑中发生的两种固化：系统固化（systems consolidation）与突触固化（synaptic consolidation）。系统固化是指由大脑中快速学习的部位所获取的记忆被铭刻进慢速学习部位的过程。已知这种铭刻由有意识与无意识的回忆来介导——例如，这可以发生在做梦的时候。在第二种机制——突触固化——中，如果神经元之间的连接曾在先前学习的任务中发挥重要作用，它们被覆写的可能性就会降低。我们的算法正是从这一机制中获得灵感，来解决灾难性遗忘问题。

神经网络由许多连接构成，这一点与大脑非常相似。在学完一个任务后，我们计算每一条连接对该任务的重要程度。当我们学习新任务时，每条连接都会受到保护、免于被修改，保护的强度与其对旧任务的重要性成正比。这样一来，就有可能在不覆写前一任务所学内容、且不产生显著计算开销的情况下学习新任务。用数学的语言来说，我们可以把在新任务中施加于每条连接的保护想象成通过一根弹簧与旧的保护值相连，弹簧的刚度与该连接的重要性成正比。正因如此，我们把算法称为弹性权重固化（Elastic Weight Consolidation，EWC）。

![一段动画示意图，展示了神经网络按顺序学习任务 A 和任务 B 时的弹性权重固化（EWC）。实线表示任务 A 的重要连接权重在学习任务 B 形成新连接的同时受到保护并得以维持。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62229423100cfeaf511d88da_Enabling20Continual20Learning20in20Neural20Networ.gif)

使用 EWC 对两个任务进行学习的过程示意图

为了检验我们的算法，我们让一个智能体依次接触多款 Atari 游戏。仅凭得分学习单个游戏已是具有挑战性的任务，而依次学习多个游戏则更具挑战性，因为每个游戏都需要单独的策略。如下图所示，在没有 EWC 的情况下，智能体在停止玩某个游戏后会很快把它忘掉（蓝色）。这意味着平均而言，智能体几乎学不会任何一个游戏。然而，如果使用 EWC（棕色和红色），智能体就不会那么容易遗忘，并且能够一个接一个地学会玩好几个游戏。

![折线图，显示依次训练的 Atari 游戏在训练时长（百万帧）内的总归一化得分。"无惩罚"方法（蓝线）在 0 附近保持平坦，显示出灾难性遗忘。"EWC + 任务先知"（棕色）与"EWC + FMN"（红色）的得分随更多游戏受到保护而稳步上升，直至 5 亿帧，下方的阶梯图展示了这一过程。](https://lh3.googleusercontent.com/z4f0nbMAdAzE2vIrftw2uq4_iJP-LCsg_Ks_xqWNnCvFssPjfDoKCBraMXsPxFcvR5WCcvXU4QTDYfGpZGGZ6AeQsMSQgIFgya2JPfxBc8zwgCsJP-c=w1440)

今天，计算机程序还无法自适应地、实时地从数据中学习。然而，我们已经证明，灾难性遗忘对神经网络而言并非不可逾越的挑战。我们希望这项研究代表着向能够以更灵活、更高效的方式学习的程序迈出的一步。

我们的研究也推进了我们对固化在人脑中如何发生的理解。我们的工作所基于的神经科学理论，实际上大多只在非常简单的例子中得到过验证。通过证明这些同样的理论可以应用于一个更真实、更复杂的机器学习情境，我们希望为"突触固化是保留记忆与技能诀窍的关键"这一观点提供进一步的支持。

![一幅抽象插画：一个人脑中包含复古电子游戏迷宫，象征着神经科学启发的记忆固化与神经网络持续机器学习的交汇。](https://lh3.googleusercontent.com/RHT3VlM6p9C29oMKNfblDgBC30fvGBNNjwvJY3LPcNHRHm1RYApbhFrbNXAf9Tg4lNzI3sVC16TAG1scmY4N05yZC3T2KoNVVmR9SGMhBl28zsOzmw=w1440)

**注**

阅读论文：[Overcoming catastrophic forgetting in neural networks](https://www.pnas.org/doi/abs/10.1073/pnas.1611835114)
