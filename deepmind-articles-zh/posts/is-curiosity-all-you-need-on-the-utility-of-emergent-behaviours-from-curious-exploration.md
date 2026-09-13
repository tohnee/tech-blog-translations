---
title: "好奇心就是全部所需吗？论好奇心探索所涌现行为的价值"
title_en: "Is Curiosity All You Need? On the Utility of Emergent Behaviours from Curious Exploration"
source: https://deepmind.google/blog/is-curiosity-all-you-need-on-the-utility-of-emergent-behaviours-from-curious-exploration/
site: deepmind
date: 2021-09-17
crawled: 2026-09-13
translated: 2026-09-13
---

# 好奇心就是全部所需吗？论好奇心探索所涌现行为的价值

> 原文：[Is Curiosity All You Need? On the Utility of Emergent Behaviours from Curious Exploration](https://deepmind.google/blog/is-curiosity-all-you-need-on-the-utility-of-emergent-behaviours-from-curious-exploration/) · Google DeepMind

在纯粹的好奇心探索过程中，JACO 机械臂学会了抓取立方体、在工作空间中移动它们，甚至探索它们能否被立在其棱边上保持平衡。

好奇心探索使 OP3 能够直立行走、单脚平衡、坐下，甚至在向后跳跃时安全地自我保护——而这一切都不需要任何特定的目标任务作为优化对象。

内在动机（intrinsic motivation）[1, 2] 是一个强大的概念，它能在缺乏任务信息的情况下，赋予智能体一种持续探索环境的机制。实现内在动机的一种常见方式是通过好奇心学习（curiosity learning）[3, 4]。在这种方法中，一个关于环境如何响应智能体动作的预测模型会与智能体的策略一同被训练。这个模型也可以被称为世界模型（world model）。当智能体采取一个动作时，世界模型会对其下一个观测做出预测，然后将该预测与智能体实际观测到的结果进行比较。关键在于，智能体因采取该动作而获得的奖励会根据其预测下一观测时的误差进行缩放。这样一来，智能体会因采取那些结果尚难以预测的动作而获得奖励。与此同时，世界模型也会被更新，以更好地预测上述动作的结果。

这一机制已在同策略（on-policy）场景中得到成功应用，例如以无监督方式通关 2D 电脑游戏 [4]，或训练出易于适配具体下游任务的通用策略 [5]。然而，我们认为好奇心学习的真正优势在于好奇心探索过程中涌现出的多样化行为：随着好奇心目标的变化，智能体随之产生的行为也在变化，从而发现许多复杂的策略——如果这些策略能够被保留而不被覆盖，日后便可以加以利用。

在[这篇论文](https://arxiv.org/abs/2109.08603)中，我们对研究好奇心学习并利用其涌现行为做出了两项贡献：第一，我们提出了 SelMo，一种自我驱动、基于好奇心的探索方法的离策略（off-policy）实现。我们展示了在仿真操作与运动控制领域中，仅凭对好奇心目标的优化，SelMo 就能涌现出有意义且多样的行为。第二，我们建议将好奇心学习的应用重心扩展到对涌现出的中间行为的识别与保留上。我们通过一项实验支持了这一猜想：在分层强化学习（hierarchical reinforcement learning）设置中，将自我发现的行为重新加载为预训练的辅助技能。

![示意图：SelMo 离策略好奇心学习循环。执行器与环境交互产生的原始轨迹被存入经验回放缓冲区以训练动力学世界模型；这些轨迹随后依据预测误差被标注好奇心奖励，并发送到第二个回放缓冲区，用于执行离策略强化学习，改进执行器策略。](https://lh3.googleusercontent.com/AQyewboCUZANdrGw8av-m8_t383c5UnlE-qxKJ7vtDmEI_ay4ecapvG-kH_-u9pbzNz5Srw7suXoL-fJ1FI-qcOYNLDj-iZsyjUSvDjJapahvJcRFw=w1440)

SelMo 方法的控制流程：智能体（执行器，actor）使用当前策略在环境中收集轨迹，并存入左侧的模型回放缓冲区。与之相连的世界模型从该缓冲区中均匀采样，并使用随机梯度下降（SGD）更新其前向预测的参数。采样到的轨迹会依据其在当前世界模型下的预测误差被赋予相应缩放的好奇心奖励，随后这些已标注的轨迹被传递到右侧的策略回放缓冲区。系统使用最大后验策略优化（MPO）[6]，基于策略回放的样本拟合 Q 函数与策略。更新后的策略随后同步回执行器。

我们在两个仿真连续控制机器人领域中运行 SelMo：一个是带三指夹爪的 6 自由度 JACO 机械臂，另一个是 20 自由度的人形机器人 OP3。这两个平台分别为物体操作和运动控制提供了具有挑战性的学习环境。在仅优化好奇心目标的情况下，我们观察到训练过程中涌现出复杂且人类可解读的行为。例如，JACO 在没有任何监督的情况下学会抓起并移动立方体；OP3 学会单脚平衡或安全坐下而不摔倒。

![时间线：展示机械臂在 10 万个回合的好奇心探索中发现的行为演进——沿斜墙推物体、抬起立方体、将立方体移动更远距离、将立方体立在棱边上平衡、以及同时抓起两个立方体。](https://lh3.googleusercontent.com/vwaSmf-bz-LN6MtrUVeGFGaXZvNou8z9mhcfZ_T22CcRu4slQ3T1eCVBnI0nZJlu51hOHIrrm7y53KscLBAlZpD5rpUAkHQAYupjYSzv1jSo3yfzp8Q=w1440)

![时间线：展示人形机器人 OP3 在 10 万个回合的好奇心探索中发现的行为演进——举起手臂、单脚平衡、坐下、向后跳跃后自我保护、以及屈膝伸展。](https://lh3.googleusercontent.com/_f_eFZZmrG4nPN-ep2_6yVrEylKQXvQe0sNtlaif8b6FvokP8X1XCkSD2zwsUB6JCCx0EkO2VmgBZBCl64Epvg3_kKmoMJjrpOEN8iCIu9tlPrkLIGY=w1440)

JACO 与 OP3 的训练时间线示例。在优化好奇心目标的过程中，操作与运动控制两类场景中都涌现出复杂而有意义的行为。完整视频可在本页顶部观看。

然而，好奇心探索中观察到的这些令人印象深刻的行为有一个关键缺陷：它们并不持久，会随好奇心奖励函数不断变化。当智能体不断重复某种行为（例如 JACO 抬起红色立方体）时，该策略累积的好奇心奖励会逐渐减少。这导致智能体学习出一个修改后的策略，以重新获得更高的好奇心奖励，例如把立方体移出工作空间，甚至转而摆弄另一个立方体。但这一新行为会覆盖旧行为。我们认为，保留好奇心探索中涌现的行为，能为智能体配备一套有价值的技能，从而更快地学习新任务。为验证这一猜想，我们设计了一项实验来探究这些自我发现技能的效用。

![折线图，标题为"lift_red 累积奖励随时间变化"，比较四种强化学习设置（RHPO - early、RHPO - mid、RHPO - late 和 SAC-X）在 6 万个训练回合中的表现，表明使用探索中期的中间辅助技能（RHPO - mid）能带来最快的学习进度。](https://lh3.googleusercontent.com/5SNjJb2rU-f9Ut9YPCgMkqx-_nWUbqOrXGa1jwYQjj9oXUK8YxT8Uo4GUPQMLDbY7u7yrty3YkzFKGE-4ANbBwfVEJV9cd9fwRoa1mPvdRhoEf-yCA=w1440)

我们将好奇心探索不同阶段随机采样的快照视为模块化学习框架 [7] 中的辅助技能，并衡量借助这些辅助技能学习一个新目标技能的速度。以 JACO 机械臂为例，我们将目标任务设定为「抬起红色立方体」，并使用五个随机采样的自我发现行为作为辅助技能。我们将该下游任务的学习与 SAC-X 基线 [8] 进行比较，后者使用一套奖励函数课程来奖励接近和移动红色立方体，并最终促进学会抬起动作。我们发现，即便是这种简单的技能复用设置，其 downstream 任务的学习进度提升也已与人工设计的奖励课程相当。结果表明，自动识别并保留好奇心探索中有用的涌现行为，是无监督强化学习未来研究中一条富有成效的路径。

**参考文献**

[1] Oudeyer, Pierre-Yves, Frdric Kaplan, and Verena V. Hafner. "Intrinsic motivation systems for autonomous mental development." IEEE transactions on evolutionary computation 11.2 (2007): 265-286.

[2] Schmidhuber, Jürgen. "Formal theory of creativity, fun, and intrinsic motivation (1990–2010)." IEEE Transactions on Autonomous Mental Development 2.3 (2010): 230-247.

[3] Schmidhuber, Jürgen. "A possibility for implementing curiosity and boredom in model-building neural controllers." Proc. of the international conference on simulation of adaptive behavior: From animals to animats. 1991.

[4] Pathak, Deepak, et al. "Curiosity-driven exploration by self-supervised prediction." International conference on machine learning. PMLR, 2017.

[5] Sekar, Ramanan, et al. "Planning to explore via self-supervised world models." International Conference on Machine Learning. PMLR, 2020.

[6] Abdolmaleki, Abbas, et al. "Maximum a posteriori policy optimisation." arXiv preprint arXiv:1806.06920 (2018).

[7] Wulfmeier, Markus, et al. "Compositional transfer in hierarchical reinforcement learning." arXiv preprint arXiv:1906.11228 (2019).

[8] Riedmiller, Martin, et al. "Learning by playing solving sparse reward tasks from scratch." International Conference on Machine Learning. PMLR, 2018.

[9] Riedmiller, Martin, et al. "Collect & Infer" arXiv preprint arXiv:2108.10273 (2021).
