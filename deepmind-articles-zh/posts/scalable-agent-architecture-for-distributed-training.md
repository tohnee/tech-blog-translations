---
title: "面向分布式训练的可扩展智能体架构"
title_en: "Scalable agent architecture for distributed training"
source: https://deepmind.google/blog/scalable-agent-architecture-for-distributed-training/
site: deepmind
date: 2018-02-05
crawled: 2026-09-13
translated: 2026-09-13
---

# 面向分布式训练的可扩展智能体架构

> 原文：[Scalable agent architecture for distributed training](https://deepmind.google/blog/scalable-agent-architecture-for-distributed-training/) · Google DeepMind

深度强化学习（DeepRL）已在一系列任务中取得显著成功，从机器人学中的连续控制问题到围棋和 Atari 等游戏。但迄今为止，这些领域的进步仍局限于单个任务——每个任务都需要单独调优和训练一个智能体。

在我们最新的工作中，我们探讨了用单个智能体学习多个任务的挑战。

今天我们发布 DMLab-30——一组新任务，它们在视觉统一、动作空间相同的环境中覆盖了多种多样的挑战。训练一个智能体在众多任务上都有良好表现，需要海量吞吐并高效利用每一个数据点。为此，我们开发了一种全新的、高度可扩展的分布式训练智能体架构——重要性加权行动者-学习者架构（Importance Weighted Actor-Learner Architecture），它使用一种称为 V-trace 的新离策略修正算法。

## DMLab-30

DMLab-30 是使用我们的开源强化学习环境 [DeepMind Lab](https://github.com/deepmind/lab) 设计的一组新关卡。这些环境让任何 DeepRL 研究者都能在大量有趣任务上测试自己的系统，既可以逐个任务单独测试，也可以在多任务设定下测试。

![DMLab-30 中部分环境的选集，包含墙壁、柱子和其他障碍物。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622679ec36bc1bb2eb6b021a_Tasks.gif)

这些任务的设计尽可能多样化。它们的目标各不相同，涵盖学习、记忆到导航。它们的视觉风格各异，从色彩鲜艳的现代风格纹理，到沙漠在黎明、正午或夜晚那微妙的棕绿色调。它们的物理设定也不相同，从开阔的山地地形，到直角迷宫，再到开阔的圆形房间。

此外，部分环境中还包含具有自身内在目标导向行为的「机器人（bots）」。同样重要的是，不同关卡之间的目标和奖励各不相同：从遵循语言指令、使用钥匙开门、采集蘑菇，到规划并沿一条复杂的不可逆路径前进。

不过，在最基础的层面上，这些环境在动作空间和观察空间上完全一致，因此可以训练单个智能体在这组高度多样的环境中行动。关于这些环境的更多细节，请见 [DeepMind Lab 的 GitHub 页面](https://github.com/deepmind/lab)。

## 重要性加权行动者-学习者架构（Importance-Weighted Actor-Learner Architectures）

为了攻克颇具挑战性的 DMLab-30 任务集，我们开发了一个名为重要性加权行动者-学习者架构的新分布式智能体，它借助 [TensorFlow](https://www.tensorflow.org/) 的高效分布式架构最大化数据吞吐。

重要性加权行动者-学习者架构的灵感来自流行的 [A3C](https://arxiv.org/abs/1602.01783) 架构——后者使用多个分布式行动者来学习智能体参数。在这类模型中，每个行动者都使用策略参数的一个副本在环境中行动。行动者会周期性地暂停探索，把它们计算出的梯度共享给一个应用更新的中央参数服务器（见下图）。

![对比三种分布式强化学习架构的示意图：A3C、IMPALA（单学习者）和 IMPALA（多学习者）。A3C 中紫色行动者向中央参数服务器发送梯度并接收参数；IMPALA 架构中蓝色行动者向一个或多个中央灰色学习者发送观察并接收参数。](https://lh3.googleusercontent.com/ND8sOkEin1P1vO7AbQHnVQwuyO2h41pQUjs_QihrdjslCL_mG6TIi69hTf0TIAHVkNq-F9CEDlUn7djOFC0L1dID3rIxZQo2iC2Eem32rvW34_XKfg=w1440)

相比之下，重要性加权行动者-学习者架构中的行动者并不用于计算梯度。它们只负责收集经验，并将其传递给计算梯度的中央学习者，从而形成行动者与学习者完全独立的模型。为了利用现代计算系统的规模，重要性加权行动者-学习者架构既可以部署在单一学习者机器上，也可以由多个学习者在彼此之间执行同步更新。以这种方式分离学习与行动还有另一个好处：提升整个系统的吞吐量，因为行动者不再需要像批处理 A2C 这类架构那样等待学习步骤。这使我们能够在有趣的环境中训练重要性加权行动者-学习者架构，而不受帧渲染时间波动或耗时任务重启的影响。

![时间线对比图：批处理 A2C 的行动者步调一致地等待单次反向传播，而 IMPALA 的行动者异步生成数据并持续发送给学习者，后者连续不断地执行前向和反向传播。](https://lh3.googleusercontent.com/oL04Fo2mjeqzKRuaWb7wuPJ8rrVXL_blD59Fz8B0Hj3_XQ2a1UCp8ZSKFtGEDMzWcgONUW3ZCCr_NhwxflhsAIyusQfoV6LNYA8xBN04WEhW6Ebw=w1440)

重要性加权行动者-学习者架构中的学习是连续进行的，而其他架构则需要在每个学习步骤暂停

然而，行动与学习的解耦会导致行动者中的策略落后于学习者。为了弥补这一差距，我们引入了一种有原则的离策略优势 actor-critic 形式——V-trace，它对行动者产生的偏离当前策略的轨迹进行修正。算法细节及其分析见我们的[论文](https://arxiv.org/abs/1802.01561)。

![折线图，比较 IMPALA（蓝色线）与 A3C（紫色线）的训练性能。y 轴为平均截断归一化得分（0 到 60），x 轴为环境帧数（至 1e10）。IMPALA 曲线始终上升更快，最终得分约 50，高于 A3C 的约 30。](https://lh3.googleusercontent.com/xiCotpILN14KXtEAfv9IcGH0VZu6ghMkB0EAGw8l8mY_qUxI2HN9b9FdbQGrn25F_z32RnRG7RG75WnxreUwRcW5DnxKeQQuaTbkgeiLR75YKVB_6lE=w1440)

得益于重要性加权行动者-学习者架构的优化模型，与同类智能体相比，它能处理一到两个数量级更多的经验，使得在具有挑战性的环境中学习成为可能。我们将重要性加权行动者-学习者架构与若干流行的 actor-critic 方法进行了比较，观察到了显著的加速。此外，重要性加权行动者-学习者架构的吞吐量随行动者和学习者数量的增加几乎线性扩展，这表明无论分布式智能体模型还是 V-trace 算法都能支撑超大规模实验，甚至达到数千台机器的量级。

在 DMLab-30 关卡上测试时，重要性加权行动者-学习者架构的数据效率是分布式 A3C 的 10 倍，最终得分是它的两倍。此外，与单任务训练相比，重要性加权行动者-学习者架构在多任务设定下训练时表现出正向迁移。

**注**

完整的重要性加权行动者-学习者架构论文可在[此处](https://arxiv.org/abs/1802.01561)阅读。

请在[此处](https://github.com/deepmind/lab/tree/master/game_scripts/levels/contributed/dmlab30)探索 DMLab-30。

本工作由 Lasse Espeholt、Hubert Soyer、Remi Munos、Karen Simonyan、Volodymir Mnih、Tom Ward、Yotam Doron、Vlad Firoiu、Tim Harley、Iain Dunning、Shane Legg 和 Koray Kavukcuoglu 完成
