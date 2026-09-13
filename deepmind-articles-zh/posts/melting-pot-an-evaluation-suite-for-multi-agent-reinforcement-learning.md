---
title: "Melting Pot：多智能体强化学习评测套件"
title_en: "Melting Pot: an evaluation suite for multi-agent reinforcement learning"
source: https://deepmind.google/blog/melting-pot-an-evaluation-suite-for-multi-agent-reinforcement-learning/
site: deepmind
date: 2021-07-14
crawled: 2026-09-13
translated: 2026-09-13
---

# Melting Pot：多智能体强化学习评测套件

> 原文：[Melting Pot: an evaluation suite for multi-agent reinforcement learning](https://deepmind.google/blog/melting-pot-an-evaluation-suite-for-multi-agent-reinforcement-learning/) · Google DeepMind

部署到现实世界的技术不可避免地会面临未曾预料的挑战。这些挑战之所以出现，是因为技术开发时所处的环境与部署时的环境不同。当一项技术成功迁移时，我们说它泛化了。在多智能体系统（例如自动驾驶汽车技术）中，泛化困难有两种可能的来源：(1) 物理环境变化，例如天气或光照的变化；(2) 社会环境变化：其他交互个体行为的改变。应对社会环境变化与应对物理环境变化同等重要，但针对它的研究却少得多。

举一个社会环境的例子：想象自动驾驶汽车在道路上与其他汽车如何交互。每辆车都有尽快把自己乘客送达的动机。然而，这种竞争可能导致糟糕的协调（道路拥堵），进而对所有人产生负面影响。如果汽车协同合作，更多乘客或许能更快到达目的地。这种冲突被称为社会困境（social dilemma）。

不过，并非所有交互都是社会困境。例如，开源软件中存在协同增效的交互，体育运动中存在零和交互，而协调问题则是供应链的核心。应对这些不同情境需要截然不同的方法。

多智能体强化学习为我们提供了工具，可以探索人工智能体之间如何交互，以及它们如何与陌生个体（例如人类用户）交互。人们期望这类算法在社会泛化能力的测试中优于其他算法。然而，迄今为止还没有系统性的评估基准来衡量这一点。

![示意图：展示 Melting Pot 的评估流程——智能体先在一个由熟悉的蓝色圆形智能体组成的多智能体强化学习"基底"上训练，然后在全新的"测试场景"中评估（零样本迁移），它们必须以不同比例与陌生的红色菱形智能体交互。](https://lh3.googleusercontent.com/EG-5AeaSc16rfhRTx0PBuzB4K5vRj1_5wmdUTWdwJLTt90Kb1iw7EmQWudLCB3ZmZbHgmq3f4h12PGnSLpzTcmjpw3QC6XujYIqiF-bAKmoX3Tbp6dc=w1440)

蓝色：训练智能体的焦点种群；红色：预训练 bot 组成的背景种群。

在这里，我们介绍 Melting Pot——一个可扩展的多智能体强化学习评测套件。Melting Pot 评估智能体对涉及熟悉与陌生个体的新社会情境的泛化能力，其设计旨在测试广泛的社会交互类型，例如合作、竞争、欺骗、互惠、信任、固执等等。Melting Pot 为研究者提供 21 个多智能体强化学习「基底」（multi-agent games，多智能体游戏）用于训练智能体，以及超过 85 个独特的测试场景用于评估这些训练后的智能体。智能体在这些留存测试场景上的表现，量化了智能体是否能够：

- 在个体相互依存的一系列社会情境中表现良好；
- 与训练中未见过的陌生个体有效交互；
- 通过普遍化测试：对「如果每个人都这样做会怎样？」这一问题给出积极回答。

由此得到的分数可以用来按泛化到新社会情境的能力对不同多智能体强化学习算法进行排名。

![矩阵表格：将 21 个不同的多智能体强化学习"基底"（如 Capture the Flag 和 Clean Up）与多种"游戏属性"和"潜在解法属性"（如对称角色、时间协调、互惠和信任）对应起来，展示每个游戏的归类方式。](https://lh3.googleusercontent.com/AtZHNXW6fNLGXBFEKoUnvturb_ay6pmefHTsU3Em5difedVaQT1le8X9Ftgf31v7avCla9WrzdmQooZq0M2FcNf97yaiJE09NXQ_sLYCehrr-MH0=w1440)

我们希望 Melting Pot 能够成为多智能体强化学习的标准基准。我们计划持续维护它，并将在未来几年不断扩展，以覆盖更多的社会交互与泛化场景。

了解更多请访问我们的 [GitHub 页面](https://github.com/deepmind/meltingpot)。
