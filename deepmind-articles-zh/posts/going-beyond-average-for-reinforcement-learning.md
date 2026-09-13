---
title: "超越平均值：强化学习的分布视角"
title_en: "Going beyond average for reinforcement learning"
source: https://deepmind.google/blog/going-beyond-average-for-reinforcement-learning/
site: deepmind
date: 2017-07-24
crawled: 2026-09-13
translated: 2026-09-13
---

# 超越平均值：强化学习的分布视角

> 原文：[Going beyond average for reinforcement learning](https://deepmind.google/blog/going-beyond-average-for-reinforcement-learning/) · Google DeepMind

想想那位每天乘火车上下班、来回奔波的通勤者。大多数清晨，她的列车准点运行，她能从容不迫地赶到第一场会议。但她知道，偶尔会有意外发生：机械故障、信号失灵，甚至只是一个特别多雨的日子。这些小插曲无一例外会打乱她的节奏，让她迟到而慌乱。

随机性是我们每天都会遇到的东西，它深刻地影响着我们体验世界的方式。在强化学习（RL）应用中同样如此——这类系统通过试错来学习，并以奖励为驱动。通常，RL 算法预测它在任务的多次尝试中获得的平均奖励，并利用这一预测来决定如何行动。但环境中的随机扰动可以通过改变系统实际获得的奖励数量来改变其行为。

在[一篇新论文](https://arxiv.org/abs/1707.06887)中，我们证明不仅可以对这一奖励的平均值建模，还可以对其完整的波动范围建模——我们称之为价值分布（value distribution）。这使得 RL 系统比以往模型更精确、训练更快，更重要的是，它开启了重新思考整个强化学习的可能性。

回到那位通勤者的例子，我们来看一段由三段各 5 分钟构成的路程，只是每周会有一次列车抛锚，为行程再增加 15 分钟。简单计算可知，平均通勤时间为 **(3 x 5) + 15 / 5 = 18** 分钟。

![一幅示意图，展示列车在四个站点之间行驶途中可能出现的延误。](https://lh3.googleusercontent.com/7opHvNS3gWnDiSqPD34eC3U4OnsKEudCt4Rplf5EAVw1QOyEM10xxNwkkM8P311Fhnf_6ZtAhijIqt81ofQ99NIJ0RL-j_zqmHe-OZ2iArlF-I7q=w1440)

在强化学习中，我们使用贝尔曼方程（Bellman's equation）来预测这一平均通勤时间。具体而言，贝尔曼方程把当前的预测值与我们对紧接着的未来的预测值联系起来。从第一站出发，我们预测全程 18 分钟（平均总时长）；从第二站出发，我们预测还有 13 分钟（平均时长减去第一段的长度）。最后，假设列车尚未抛锚，从第三站出发我们预测还剩 8 分钟（13 - 5），然后便到达目的地。贝尔曼方程依次做出每一个预测，并依据新信息更新这些预测。

贝尔曼方程有一点反直觉：我们实际上从未观察到这些预测出的平均值——列车要么要 15 分钟（五天中有四天），要么要 30 分钟，从来不会正好 18 分钟！从纯数学的角度看，这不是问题，因为决策理论告诉我们，做出最优选择只需要平均值。因此，这一问题在实践中大多被忽视了。然而，如今已有大量[经验](https://arxiv.org/abs/1512.04860)[证据](https://arxiv.org/abs/1509.06461)表明，预测平均值是一件棘手的事情。

> 我们的经验结果已经清楚表明，分布视角能带来更好、更稳定的强化学习

在[我们的新论文](https://arxiv.org/abs/1707.06887)中，我们证明实际上存在贝尔曼方程的一个变体，它可以预测所有可能的结果，而不对它们取平均。在我们的例子里，我们在每个车站维护两个预测——即一个分布：如果旅程顺利，那么各段时间分别是 15、10、然后 5 分钟；但如果列车抛锚，那么时间就是 30、25，最后是 20 分钟。

整个强化学习都可以在这一新视角下重新解读，而且它的应用已经带来了令人惊讶的新理论结果。预测结果的分布还开启了各种算法上的可能性，例如：

- **解耦随机性的成因**：一旦我们观察到通勤时间呈双峰分布，即取两个可能值，我们就可以据此采取行动，例如出门前先查一下列车动态；
- **区分安全与冒险的选择**：当两个选择的平均结果相同时（例如步行或乘火车），[我们可能更倾向于](http://www.mit.edu/~jnt/Papers/J145-13-mv-MDP.pdf)波动较小的那一个（步行）。
- **天然的辅助预测**：预测多种结果（例如通勤时间的分布）已被[证明](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.121.8707&rep=rep1&type=pdf)[有利于](https://deepmind.com/blog/reinforcement-learning-unsupervised-auxiliary-tasks/)更快地训练深度网络。

我们把新想法实现到 [Deep Q-Network 智能体](https://deepmind.com/research/dqn/)中，把它单一的平均奖励输出替换为具有 51 个可能取值的分布。除此之外唯一的变化是一条新的学习规则，用以体现从贝尔曼（平均）方程到其分布形式对应物的转变。令人难以置信的是，事实证明，从平均值到分布的这一转变，就足以让我们以较大优势超越所有其他同类方法的性能。下图显示了我们如何在 25% 的时间内达到训练后的 Deep Q-Network 75% 的性能，并取得显著更好的人类水平表现：

![一张折线图，纵轴为 Atari 游戏获胜数量，横轴为最多 2 亿帧的训练量。标注「C51 vs. DQN」的紫色曲线快速上升，在 50 多款游戏中超过 DQN；标注「C51 vs. HUMAN」的蓝色曲线稳步上升，在 30 多款游戏中超过人类表现；标注「DQN vs. HUMAN」的橙色曲线在约 18 款获胜游戏处趋于平缓。](https://lh3.googleusercontent.com/v2iMB2V1VBIb2dlKARw95QlwwwjZAGfgu_xY5snnQxJYkCADWdj3hV9nGVQwzdp8OnBJm2Qt8NDRj-26CI3rM1viq1ZNLwhFJPB33_B-c1NyVhT3lHQ=w1440)

一个令人惊讶的结果是，我们在 Atari 2600 游戏中观察到了某些随机性，尽管底层游戏模拟器 Stella 本身是完全可预测的。这种随机性部分源于所谓的部分可观测性（partial observability）：由于模拟器内部的程序设定，玩《乒乓》（Pong）的智能体无法预测自己得分的确切时刻。把智能体在连续各帧上的预测可视化（见下图），可以看到两个分离的结果（低与高），反映出可能出现的不同时机。虽然这种内在随机性并不直接影响性能，但我们的结果凸显了智能体理解能力的局限。

![《乒乓》（Pong）的游戏画面截图，旁边是 t=0 到 t=4 五个连续的概率分布图，展示了对高低两种回报随时间的双峰预测。](https://lh3.googleusercontent.com/JmLdX2dUqp4X6oYfQS0YK6BIcylUjFlGMI8yWODiEi_YZUahZHYXzvM9Jh30e65tyEAHYB1QDlcs3FCTGpEtMbM4NOT0Y8K8cU7Wny2I7-rCGY2O5tw=w1440)

随机性的另一个来源是智能体自身行为的不确定性。在《太空侵略者》（Space Invaders）中，我们的智能体学会了预测自己未来可能犯错并输掉游戏（零奖励）的概率。

![一段 AI 智能体玩《太空侵略者》的游戏录像。动画旁的图表记录了每个输入对应的成功概率。智能体从这一概率中学习，以预测未来更成功的行为。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62265c0345111906f5453238_Beyond20Average20for20RL204.gif)

正如火车通勤的例子一样，对这些截然不同的结果分别保持独立的预测是有意义的，而不是把它们合并成一个根本无法实现的平均值。事实上，我们认为性能提升在很大程度上要归功于智能体能够对自身的随机性建模。

我们的经验结果已经清楚表明，分布视角能带来更好、更稳定的强化学习。既然每一个强化学习概念现在都可能需要自己的分布形式对应物，这条路也许才刚刚开始。

**附注**

本工作由 Marc G. Bellemare\*、Will Dabney\* 与 Rémi Munos 完成。

阅读论文：[A Distributional Perspective on Reinforcement Learning](https://arxiv.org/abs/1707.06887)
