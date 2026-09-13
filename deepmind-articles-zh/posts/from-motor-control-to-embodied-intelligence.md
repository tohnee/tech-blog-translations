---
title: "从运动控制到具身智能"
title_en: "From motor control to embodied intelligence"
source: https://deepmind.google/blog/from-motor-control-to-embodied-intelligence/
site: deepmind
date: 2022-08-31
crawled: 2026-09-13
translated: 2026-09-13
---

# 从运动控制到具身智能

> 原文：[From motor control to embodied intelligence](https://deepmind.google/blog/from-motor-control-to-embodied-intelligence/) · Google DeepMind

利用人类和动物的动作教会机器人运球，并让模拟的人形角色搬箱子、踢足球

![](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f66e86725db418b6d33f0_Football20blog201.gif)

人形角色通过反复试错学习穿越障碍训练场，这可能产生标新立异的解决方案。Heess, et al. "Emergence of locomotion behaviours in rich environments" (2017)。

五年前，我们接下了一个挑战：教会一个全关节 articulated 的人形角色[穿越障碍训练场](https://youtu.be/hx_bgoTF7bs?t=88)。这展示了强化学习（RL）通过反复试错能够取得的成就，但也凸显了解决具身智能（embodied intelligence）问题的两大挑战：

1. **复用先前学习到的行为：** 智能体要「起步」需要大量数据。在对自己的每个关节该施加多大的力毫无初始认知的情况下，智能体一开始只会随机抽搐身体并迅速倒地。通过复用先前学习到的行为，可以缓解这一问题。
2. **标新立异的行为：** 当智能体最终学会穿越障碍训练场时，它采用的是不自然的（[虽然颇为滑稽](https://www.youtube.com/watch?v=EI3gcbDUNiM&t=258s)）运动模式，这对于机器人学等应用来说并不实用。

在这里，我们描述一种针对这两大挑战的解决方案，称为神经概率运动原语（neural probabilistic motor primitives，NPMP），它借助源自人类和动物的运动模式进行引导式学习，并讨论这一方法如何应用于今天发表在《科学·机器人学》（Science Robotics）上的我们的[人形足球论文](https://www.science.org/doi/10.1126/scirobotics.abo0235)。

我们还将讨论这同一方法如何实现基于视觉的人形全身操控（例如人形角色搬运物体），以及真实世界中的机器人控制（例如机器人运球）。

## 使用 NPMP 将数据蒸馏为可控的运动原语

NPMP 是一个通用的运动控制模块，它将短时程的运动意图转换为低层控制信号，它通过[离线训练](https://openreview.net/forum?id=BJl6TjRcY7)或[经由 RL 训练](https://proceedings.mlr.press/v119/hasenclever20a.html)来模仿动作捕捉（MoCap）数据——这些数据由佩戴追踪器的人或动物在执行感兴趣的动作时记录而来。

![一个橙色的 3D 人形角色在铺有瓷砖的蓝色表面上，模仿一个半透明灰色角色的行走和转身动作。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f68789b57e07b40fcd865_Football20blog202.gif)

一个智能体学习模仿 MoCap 轨迹（以灰色显示）。

**该模型包含两个部分：**

1. 一个编码器，接收未来轨迹并将其压缩为运动意图。
2. 一个低层控制器，在给定智能体当前状态和该运动意图的情况下产生下一步动作。

![一幅示意图，左侧为 NPMP 训练，右侧为其复用。在 NPMP 训练阶段，参考数据提供智能体状态与未来轨迹，经过编码器生成运动意图。这些意图在先验的正则化约束下，引导低层控制器执行动作。在复用阶段，RL 环境向粉色任务策略提供任务观测，任务策略直接输出运动意图给复用的低层控制器以执行任务动作。](https://lh3.googleusercontent.com/BVUVxX__mBb14uR12QhmavzmOnnw1bVtMCKaDU1SAB2ECVN7AXB743XMEPQaeVPlG1ZQ91bQbRoVL0gaDfnW5jvvE9evXNN4ta7citvyT2lXVnrzPw=w1440)

我们的 NPMP 模型首先将参考数据蒸馏为一个低层控制器（左）。随后，该低层控制器可以在新任务上作为即插即用的运动控制模块使用（右）。

训练完成后，低层控制器可以被复用来学习新任务，此时会优化一个高层控制器，使其直接输出运动意图。这带来了高效的探索——因为即便运动意图是随机采样的，也能产生连贯的行为——并约束了最终解。

## 人形足球中的涌现式团队协作

足球一直是具身智能研究的[一项长期挑战](https://link.springer.com/chapter/10.1007/3-540-64473-3_46)，它既需要个人技能，也需要协调的团队配合。在我们最新的工作中，我们使用 NPMP 作为先验来引导运动技能的学习。

其结果是一支从学习追球技能起步、最终学会协同配合的球员队伍。此前，在一项[采用简单身体的](https://openreview.net/forum?id=BkG8sjR5Km)研究中，我们已经证明协作行为可以在相互竞争的团队中涌现。NPMP 让我们得以在一个需要先进得多的运动控制的场景中观察到类似效应。

![一个橙色的 3D 人形智能体在铺有瓷砖的蓝色表面上，模仿一个半透明灰色的动作捕捉角色的行走和转身动作。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f6d699c09633d3acf48f2_football20blog203.gif)

![一幅三格图，显示一个蓝色人形智能体在模拟足球场上。第一格标注「跟随」（Follow），智能体站在一条由蓝到红的路径旁；第二格标注「运球」（Dribble），智能体在一颗足球旁移动；第三格标注「踢向目标」（Kick to target），智能体站在一条白线上。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f6d7c7e2a3064bd727f40_football20blog204.gif)

智能体首先模仿足球运动员的动作来学习 NPMP 模块（上）。然后利用 NPMP，智能体学习足球专项技能（下）。

我们的智能体掌握了包括敏捷移动、传球和劳动分工在内的技能，这一点由一系列统计数据所证实，其中包括[真实世界体育分析](https://www.researchgate.net/profile/William-Spearman/publication/327139841_Beyond_Expected_Goals/links/5b7c3023a6fdcc5f8b5932f7/Beyond-Expected-Goals.pdf)中使用的指标。球员既展现出敏捷的高频运动控制，也展现出涉及预判队友行为的长期决策，从而实现协调的团队配合。

![三个模拟的人形智能体——一个穿红色球衣正在运球，两个穿蓝色球衣在防守——在带有球门的绿色条纹数字足球场上比赛。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f6e29ba1f6d269aff7c2d_football20blog205.gif)

一个智能体使用多智能体 RL 学习竞技性踢足球。

## 基于视觉的全身操控与认知任务

学习用手臂与物体互动是另一个困难的控制挑战。NPMP 同样能够实现这种类型的全身操控。只需少量与箱子互动的 MoCap 数据，我们就能够[训练智能体把箱子](https://www.youtube.com/watch?v=2rQAW-8gQQk)从一个位置搬到另一个位置，使用第一人称自我中心视觉，且只需要稀疏的奖励信号：

![一个橙色的 3D 人形角色，周身环绕着发光的绿色追踪标记，走向蓝色瓷砖地板上的一个灰色箱子，将其拾起并搬走。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f6f62cacfa971dd2e681e_Football20blog206.gif)

![一个橙色的 3D 人形角色，左侧为第一人称自我中心摄像机视角，右侧为第三人称视角，在蓝色瓷砖地板上接住抛向它的球并将其抛回。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f6f73a8d8fad56ff930ae_Football20blog207.gif)

只需少量 MoCap 数据（上），我们的 NPMP 方法就能解决搬箱子任务（下）。

类似地，我们还可以教智能体接球和抛球：

![一个橙色的 3D 人形角色，左侧为第一人称自我中心摄像机视角，右侧为第三人称视角，在蓝色瓷砖地板上接住抛向它的球并将其抛回。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f6fac40b994092e8e6e81_Football20blog208.gif)

模拟人形角色接球和抛球。

使用 NPMP，我们还能攻克[涉及移动、感知与记忆的迷宫任务](https://openreview.net/forum?id=BJfYvo09Y7)：

![一幅三格演示图，展示一个人形角色完成迷宫任务。左格为第一人称自我中心摄像机视角，中格为红蓝迷宫（含若干房间）的俯视示意图，右格为橙色人形角色在蓝色走廊中奔跑的第三人称视角。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f70036725db20fe779940_Football20blog209.gif)

模拟人形角色在迷宫中收集蓝色球体。

## 真实世界机器人的安全高效控制

NPMP 还能帮助控制真实的机器人。行为得到良好正则化，对于在崎岖地形上行走或搬运易碎物体之类的活动至关重要。抖动的动作可能损坏机器人本身或其周围环境，至少也会耗尽它的电池。因此，人们通常投入大量精力来设计学习目标，让机器人在以安全高效的方式行事的同时完成我们期望的任务。

作为另一种选择，我们研究了使用[源自生物运动的先验](https://arxiv.org/abs/2203.17138)能否为腿式机器人带来正则化良好、外观自然且可复用的运动技能，例如适合部署在真实世界机器人上的行走、奔跑和转身。

从人类和狗的 MoCap 数据出发，我们改造了 NPMP 方法，在模拟中训练技能和控制器，随后分别部署到真实的人形机器人（OP3）和四足机器人（ANYmal B）上。这使得机器人能够被用户通过操纵杆操控，或以自然且稳健的方式把球运到目标位置。

![一个模拟的火柴人四足狗在深色铺砖蓝色表面上行走、小跑和转身，展示源自生物动作捕捉的自然外观运动技能。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f73af3cbb9ede40ae9f98_Football20blog2010.gif)

ANYmal 机器人的移动技能是通过模仿狗的 MoCap 学到的。

![一个小型深色人形机器人在一个有围墙的测试区域内的一块蓝色垫子上稳定且可控地行走。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f73ed0b5f123a00699490_Football20blog2011.gif)

![一台四足机器人在绿色草皮场地上运着一颗橙色的球，成功地将它引导进入指定的红色圆形目标区域。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/630f741e73d0d9437e370ec8_Football20blog2012.gif)

移动技能随后可被复用于可控行走和运球。

## 使用神经概率运动原语的益处

总而言之，我们使用 NPMP 技能模型让模拟中的人形角色和真实世界机器人学会了复杂任务。NPMP 以可复用的方式打包低层运动技能，使学习那些靠无结构试错难以发现的有用行为变得更加容易。以动作捕捉作为先验信息的来源，它使运动控制的学习偏向自然的动作。

NPMP 使具身智能体能够：更快地通过 RL 进行学习；学习更自然的行为；学习更适合真实世界机器人技术的更安全、更高效、更稳定的行为；以及将全身运动控制与更长时程的认知技能（如团队协作与协调）相结合。

进一步了解我们的工作**：**

- 查看精选的[研究参考文献](https://storage.googleapis.com/deepmind-media/From%20motor%20control%20to%20embodied%20intelligence/From%20motor%20control%20to%20embodied%20intelligence%20-%20selected%20references.pdf)。
- 阅读《科学·机器人学》上的[人形足球论文](https://www.science.org/doi/10.1126/scirobotics.abo0235)，或观看[摘要视频](https://www.youtube.com/watch?v=tWnGTtbOK7I)。
- 阅读我们关于人形全身控制的[论文](https://dl.acm.org/doi/abs/10.1145/3386569.3392474)，或观看[摘要视频](https://www.youtube.com/watch?v=2rQAW-8gQQk)。
- 阅读我们关于真实世界机器人控制的[论文](https://arxiv.org/abs/2203.17138)，或观看[摘要视频](https://youtu.be/K77HS6uO5F8)。
