---
title: "DeepMind 在 ICLR 2022 上的最新研究"
title_en: "DeepMind's latest research at ICLR 2022"
source: https://deepmind.google/blog/deepminds-latest-research-at-iclr-2022/
site: deepmind
date: 2022-04-25
crawled: 2026-09-13
translated: 2026-09-13
---

# DeepMind 在 ICLR 2022 上的最新研究

> 原文：[DeepMind's latest research at ICLR 2022](https://deepmind.google/blog/deepminds-latest-research-at-iclr-2022/) · Google DeepMind

朝着人工智能更强的泛化能力迈进

今天，会议季随着第十届国际学习表征会议（[ICLR 2022](https://iclr.cc/)）的开幕正式开启，会议于 2022 年 4 月 25 日至 29 日以线上形式举行。来自世界各地的与会者齐聚一堂，分享他们在表征学习领域的前沿工作——从推进人工智能的最新水平，到数据科学、机器视觉、机器人学等等。

在会议首日，我们 AI for Science 与 Robust and Verified AI 团队的负责人 Pushmeet Kohli 将发表演讲，讲述 AI 如何显著改进从基因组学、结构生物学到量子化学乃至纯数学等一系列科学问题的求解方案。

除了以赞助方和常任研讨会组织者的身份支持本次大会之外，我们的研究团队还将展示 29 篇论文，其中包括今年的 10 项合作成果。以下是我们即将进行的口头报告、spotlight 报告和海报展示的简要预览：

## 优化学习

多篇重点论文聚焦于让 AI 系统的学习过程更高效的关键途径：从提升性能、推进小样本学习，到创建降低计算成本的数据高效系统。

在[《Bootstrapped meta-learning》](https://openreview.net/forum?id=b-ny3x071E5)——[ICLR 2022 杰出论文奖](https://blog.iclr.cc/2022/04/20/announcing-the-iclr-2022-outstanding-paper-award-recipients/)获奖论文——中，我们提出了一种算法，让智能体通过自我教学学会如何学习。我们还提出了一种[策略改进算法](https://openreview.net/forum?id=bERaNdoegnO)，它重新设计了 [AlphaZero](https://deepmind.google/blog/alphazero-shedding-new-light-on-chess-shogi-and-go/)——我们那个从零自我学习并掌握国际象棋、将棋和围棋的系统——使其即便在少量模拟下训练也能持续进步；此外还有一个在广泛 RL 智能体和环境中[缓解容量损失风险的正则化器](https://openreview.net/forum?id=ZkC8wKoLbQ7)，以及一种可高效训练注意力模型的改进[架构](https://openreview.net/forum?id=sRZ3GhmegS)。

## 探索

好奇心是人类学习的关键部分，帮助知识和技能不断精进。类似地，探索机制让 AI 智能体能够超越既有知识，发现未知或尝试新事物。

沿着"智能体何时应当探索？"这一问题展开，我们研究了智能体应在何时切换到探索模式、在什么时间尺度上切换才有意义，以及哪些信号最能决定探索周期应当持续多久、出现多频繁。在另一篇论文中，我们提出了一种"信息增益探索奖励"（information gain exploration bonus），让智能体突破 RL 中内在奖励的局限，从而学习更多技能。

## 鲁棒 AI

要在现实世界部署 ML 模型，它们必须在训练与测试之间、以及跨越新数据集时保持有效。理解因果机制至关重要——它让一些系统能够适应变化，而另一些系统则难以应对新挑战。

在这些机制研究的延伸中，我们提出了一个实验框架，可以对分布偏移的鲁棒性进行细粒度[分析](https://openreview.net/forum?id=Dl4LetuLdyK)。鲁棒性还有助于防范对抗性伤害，无论其是有意还是无意。针对图像损坏的情形，我们提出了一种从理论上[优化图像到图像模型参数](https://openreview.net/forum?id=jJOjjiZHy3h)的技术，以减轻模糊、雾气等常见问题的影响。

## 涌现通信

除了帮助 ML 研究者理解智能体如何演化出自己的通信方式来完成任务之外，AI 智能体还有望揭示群体内语言行为的洞见，从而催生更具交互性、更有用的 AI。

我们与 Inria、Google Research 和 Meta AI 的研究人员合作，将人类群体多样性在塑造语言中的作用与神经智能体计算机模拟中的一个表面矛盾相联系，[部分解决了这一矛盾](https://openreview.net/forum?id=5Qkd7-bZfI)。此外，由于在 AI 中构建更好的语言表征对理解涌现通信至关重要，我们还研究了将数据集规模、任务复杂度和群体规模作为独立因素[进行扩展的重要性](https://openreview.net/forum?id=AUGBfDIV9rL)。而且，我们还研究了在多个智能体为同一个目标而通信的游戏中，[表达力、复杂度与不可预测性之间的权衡](https://openreview.net/forum?id=WxuE_JWxjkW)。

请在[这里](https://deepmind.events/events/iclr-2022)查看我们在 ICLR 2022 上工作的完整清单。
