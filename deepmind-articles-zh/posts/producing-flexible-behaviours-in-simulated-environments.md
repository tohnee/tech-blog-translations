---
title: "在模拟环境中产生灵活的行为"
title_en: "Producing flexible behaviours in simulated environments"
source: https://deepmind.google/blog/producing-flexible-behaviours-in-simulated-environments/
site: deepmind
date: 2017-07-10
crawled: 2026-09-13
translated: 2026-09-13
---

# 在模拟环境中产生灵活的行为

> 原文：[Producing flexible behaviours in simulated environments](https://deepmind.google/blog/producing-flexible-behaviours-in-simulated-environments/) · Google DeepMind

猴子在树间荡跃的敏捷，或足球运动员躲开对手、破门得分的灵活，都可以令人叹为观止。掌握这类复杂的运动控制，是身体智能的标志，也是 AI 研究中的关键一环。

真正的运动智能，需要学会如何控制并协调一个灵活的身体，在多种复杂环境中解决任务。现有的对物理仿真人形身体的控制尝试来自多个领域，包括计算机动画和生物力学。一种趋势是使用手工设计的目标，有时辅以动作捕捉数据，来产生特定的行为。然而，这可能需要相当可观的工程投入，并且可能导致行为受限，或产生难以改用于新任务的行为。

在三篇新论文中，我们探索产生灵活而自然、可复用、可改造以解决任务的行为的途径。

## Emergence of locomotion behaviours in rich environments（丰富环境中运动行为的涌现）

对于某些 AI 问题，例如玩雅达利游戏或围棋，目标很容易定义——那就是赢。但你要如何描述做一个后空翻的过程？甚至只是描述一次跳跃？准确描述一个复杂行为的困难，是向人工系统教授运动技能时的常见问题。在这项工作中，我们探索复杂的行为如何能仅凭简单的高层目标（例如「前进而不摔倒」），从身体与环境的交互中从零涌现。具体而言，我们训练了拥有各种模拟身体的智能体，让它们在多样地形上前进，这些地形需要跳跃、转向和下蹲。结果表明，我们的智能体在没有任何具体指令的情况下发展出了这些复杂技能——这一方法可以应用于训练我们的系统驾驭多个不同的模拟身体。下面的 GIF 展示了这一技术如何带来高质量的动作与坚韧的毅力。完整视频可在[这里](https://youtu.be/hx_bgoTF7bs)观看。

![一个橙色简化人形角色在模拟 3D 环境中高高跃起，跳过一道宽阔的缝隙。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622655eb68abbee38e669eb2_A20simulated2027planar2720walker20makes20repeated.gif)

一个模拟的「平面」行走者反复尝试爬过一堵墙。

![一个橙色的四足模拟智能体在 3D 环境中穿越狭窄的高架平台。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622656200aa988d46d909b6f_A20simulated2027ant2720walker20learns20the20preci.gif)

一个模拟的「蚂蚁」行走者学习在木板之间跳跃所需的精确动作。

![一个橙色简化人形角色在模拟 3D 环境中高高跃起，跳过一道宽阔的缝隙。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62265611c0a057d54f0c6e31_unnamed-3.gif)

一个模拟的「人形」行走者学习在不熟悉的地形中前进。

## Learning human behaviours from motion capture by adversarial imitation（通过对抗性模仿从动作捕捉中学习人类行为）

上文所述的涌现行为可以非常稳健，但由于动作必须从零涌现，它们往往看起来不像人类。在我们的第二篇论文中，我们展示了如何训练一个策略网络，使其模仿人类行为的动作捕捉数据，从而预学习某些技能，例如走路、从地上起身、奔跑和转身。在产生了看起来像人类的行为之后，我们可以对这些行为进行调优和改造，去解决其他任务，例如爬楼梯和穿越有围墙的走廊。

![一个模拟人形角色在蓝白相间的方格地板上以自然的类人步态行走。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62265660284fd1853f765891_A20humanoid20walker20produces20human-like20walkin.gif)

一个人形行走者产生出类人的行走行为。

![一个模拟人形角色在蓝白相间的方格地板上用手臂撑地站起。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6226568168abbe472b66a4d5_A20simulated20humanoid20walker20falls20over20and2.gif)

一个模拟人形行走者摔倒后又爬了起来。

## Robust imitation of diverse behaviours（对多样行为的稳健模仿）

第三篇论文提出了一种神经网络架构，它建立在最先进的生成式模型之上，能够学习不同行为之间的关系，并模仿向它展示的特定动作。经过训练，我们的系统可以编码单一观察到的动作，并基于该演示创造一个新的动作。它还能在不同类型的行为之间切换，尽管从未见过它们之间的过渡，例如在不同行走风格之间切换。

![三个并排的模拟人形角色在方格地板上展示不同的行走风格与姿态。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622656f6284fd1d557765db0_Behaviours201.gif)

左图与中图展示两种被演示的行为。右图中，我们的智能体产生了这两种行为之间从未见过的过渡。

![两个并排的模拟简化人形角色在方格地板上展示不同的行走风格。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622657235460dd5f37e33ee2_Planar20Walking.gif)

左图中，平面行走者展示了一种特定的行走风格。右图中，我们的智能体使用单一策略网络模仿这一行走风格。

实现对模拟身体灵活而自适应的控制，是 AI 研究的关键要素。我们的工作旨在开发灵活的系统，让它们学习和调整技能以解决运动控制任务，同时减少达成这一目标所需的手工工程量。未来的工作可以把这些方法进一步扩展，以便在更复杂的情形下协调更大范围的行为。

**附注**

[Emergence of locomotion behaviours in rich environments](https://arxiv.org/abs/1707.02286)

[Learning human behaviours from motion capture by adversarial imitation](https://arxiv.org/abs/1707.02201)

[Robust imitation of diverse behaviours](https://arxiv.org/abs/1707.02747)
