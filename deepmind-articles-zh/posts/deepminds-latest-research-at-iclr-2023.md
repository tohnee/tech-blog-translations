---
title: "DeepMind 在 ICLR 2023 上的最新研究"
title_en: "DeepMind’s latest research at ICLR 2023"
source: https://deepmind.google/blog/deepminds-latest-research-at-iclr-2023/
site: deepmind
date: 2023-04-27
crawled: 2026-09-13
translated: 2026-09-13
---

# DeepMind 在 ICLR 2023 上的最新研究

> 原文：[DeepMind’s latest research at ICLR 2023](https://deepmind.google/blog/deepminds-latest-research-at-iclr-2023/) · Google DeepMind

面向能够泛化、扩展规模并加速科学研究的人工智能模型的研究

下周，第十一届[国际学习表征会议](https://iclr.cc/)（International Conference on Learning Representations，ICLR）即将开幕，会议将于 5 月 1 日至 5 日在卢旺达基加利举行。这将是首个在非洲举办的主要人工智能（AI）会议，也是疫情开始以来首场线下盛会。

来自世界各地的研究人员将齐聚一堂，分享他们在深度学习领域的前沿工作，涵盖人工智能、统计学与数据科学，以及机器视觉、游戏和机器人等应用方向。我们很荣幸能够以钻石赞助商和 DEI（多元、公平与包容）倡导者的身份支持本届会议。

今年，来自 DeepMind 各团队的学者将展示 23 篇论文。以下是一些亮点：

## 通往 AGI 道路上的开放性问题

近期的进展展现了人工智能在文本和图像方面的惊人表现，但要让系统能够跨领域、跨规模地泛化，还需要更多研究。这将是把通用人工智能（AGI）发展为日常生活中变革性工具道路上的关键一步。

我们提出了一种新的方法，让模型[通过同时求解两个问题来学习](https://openreview.net/pdf?id=hhvkdRdWt1F)。通过训练模型同时从两个视角审视同一个问题，它们能够学会对需要求解相似问题的任务进行推理，这有利于泛化。我们还通过将神经网络与乔姆斯基语言层级（Chomsky hierarchy）进行比较，探索了[神经网络的泛化能力](https://openreview.net/pdf?id=WbxHAzkeQcn)。通过对 2200 个模型在 16 个不同任务上进行严格测试，我们发现某些模型难以泛化，并且发现为它们配备外部记忆是提升性能的关键。

我们要解决的另一个挑战是，如何[在奖励稀少的长期任务上取得专家级进展](https://openreview.net/pdf?id=sKc6fgce1zs)。我们开发了一种新方法和一个开源训练数据集，帮助模型学会在长时间跨度上以类似人类的方式进行探索。

## 创新方法

随着我们开发出更先进的人工智能能力，必须确保现有方法能够按预期高效地服务于现实世界。例如，尽管语言模型可以给出令人印象深刻的答案，但许多模型无法解释自己的回答。我们介绍了一种[利用语言模型求解多步推理问题的方法](https://openreview.net/pdf?id=3Pf3Wg6o-A4)，它借助问题底层的逻辑结构，提供人类能够理解并加以核验的解释。另一方面，对抗攻击是一种探测人工智能模型极限的手段，它会迫使模型生成错误或有害的输出。在对抗样本上进行训练可以让模型对攻击更加鲁棒，但代价可能是在"常规"输入上的性能下降。我们证明，通过添加适配器（adapter），我们可以创建[能够即时控制这一权衡的模型](https://openreview.net/pdf?id=HPdxC1THU8T)。

强化学习（RL）已被证明可以成功应对一系列[现实世界挑战](https://www.deepmind.com/blog-categories/applied)，但强化学习算法通常只能把一个任务做好，难以泛化到新任务。我们提出了[算法蒸馏](https://openreview.net/pdf?id=hy0a5MMPUv)（algorithm distillation），这种方法通过训练一个 transformer 去模仿强化学习算法在多样任务上的学习历史，使单个模型能够高效地泛化到新任务。强化学习模型还通过试错来学习，这可能非常耗费数据和时间。我们的模型 [Agent 57](https://deepmind.google/blog/agent57-outperforming-the-human-atari-benchmark/) 花了近 800 亿帧数据才在 57 个 Atari 游戏上达到人类水平的表现。我们分享了一种[用少 200 倍的经验训练到该水平](https://openreview.net/pdf?id=JtC6yOHRoJJ)的新方法，大幅降低了算力与能源成本。

## 科学领域的 AI

对于研究人员来说，人工智能是分析海量复杂数据、理解身边世界的强大工具。多篇论文展示了人工智能如何加速科学进步——以及科学如何反过来推动人工智能的发展。

从分子的 3D 结构预测其性质对药物发现至关重要。我们提出了一种[去噪方法](https://openreview.net/pdf?id=tYIMtogyee)，在分子性质预测上取得了新的最优纪录（state-of-the-art），支持大规模预训练，并能跨不同生物数据集泛化。我们还介绍了一种新的 [transformer，它可以仅凭原子位置数据做出更精确的量子化学计算](https://openreview.net/pdf?id=xveTeHVlF7j%E2%80%9D)。

最后，借助 [FIGnet](https://openreview.net/pdf?id=J7Uh781A05p)，我们从物理学中汲取灵感，为茶壶、甜甜圈等复杂形状之间的碰撞建模。这一模拟器可望在机器人、图形学和机械设计等领域得到应用。

查看 [DeepMind 在 ICLR 2023 上的论文完整清单与活动日程](https://deepmind.events/events/iclr-2023/resources)。
