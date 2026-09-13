---
title: "主动式离线策略选择"
title_en: "Active offline policy selection"
source: https://deepmind.google/blog/active-offline-policy-selection/
site: deepmind
date: 2022-05-06
crawled: 2026-09-13
translated: 2026-09-13
---

# 主动式离线策略选择

> 原文：[Active offline policy selection](https://deepmind.google/blog/active-offline-policy-selection/) · Google DeepMind

近年来，强化学习（RL）在解决现实问题方面取得了巨大进展——而离线 RL 让它变得更加实用。如今我们不再需要与环境的直接交互，仅凭一份预先录制的数据集就能训练许多算法。然而，当我们评估手头的策略时，离线 RL 在数据效率上的实用优势就打了折扣。

例如，在训练机器人操作臂时，机器人资源通常有限，用离线 RL 在单一数据集上训练多个策略，相比在线 RL 能带来很大的数据效率优势。但评估每个策略是一个昂贵的过程，需要与机器人交互数千次。当我们还要挑选最优的算法、超参数和训练步数时，问题很快就会变得难以处理。

为了让 RL 更适用于机器人等现实应用，我们提出使用一种智能评估流程来选出用于部署的策略，称为主动式离线策略选择（A-OPS）。在 A-OPS 中，我们利用预先录制的数据集，并允许与真实环境进行有限的交互，以提升选择质量。

![主动式离线策略选择（A-OPS）示意图：以候选策略、离线数据和有限的环境交互为输入，选出最优策略。](https://lh3.googleusercontent.com/0s1yMdmoyHJb7GJW8wj25KlpuYLpc2Qtbfbx8RwNgo3EXfSWKzc7-dLXj4gTTCZtMhgQTIaeCORl7WyanIo4rrLkECyucrg-reZPiRQwA2D6QvKu=w1440)

主动式离线策略选择（A-OPS）在给定一份预先录制的数据集和有限环境交互的条件下，从一组策略中选出最佳策略。

为了将真实环境交互降到最少，我们实现了三项关键特性：

1. 离线策略评估（off-policy policy evaluation），例如拟合 Q 评估（FQE），使我们能够基于离线数据集对每个策略的性能做出初步猜测。它在许多环境中都与真实性能高度相关，包括首次将该方法应用于真实世界的机器人。

![散点图，展示 sim2real（深蓝色五边形）与离线 RL（浅蓝色五边形）策略的 FQE 得分（y 轴）与折扣回报（x 轴）之间的强相关性，各点紧密贴合对角线。](https://lh3.googleusercontent.com/Y_DMS4JuhFcptqRKl3Zq-Yic69LaMxPjRF0_iSz7h3_JCPysxjwOYwLhRC9-Ozzeq18kTptHwqJFVwgbT0a_3KGjwfmGZzGeL_w4dTvmGFdtogUX4g=w1440)

无论是 sim2real 还是离线 RL 设置下训练的策略，其 FQE 得分都与真实性能高度一致。

各策略的回报通过一个高斯过程联合建模，其中的观测包括 FQE 得分以及从机器人新采集的少量回合回报。在评估一个策略之后，我们对所有策略都获得了知识，因为它们的分布通过策略对之间的核函数相互关联。该核函数假设：如果两个策略采取相似的动作——例如让机器人夹爪朝相似的方向移动——它们往往会有相似的回报。

![](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/627bed70dc6376412174067c_3.gif)

我们使用 OPE 得分和回合回报，将潜在的策略性能建模为一个高斯过程。

![示意图，展示核函数如何通过比较两个机器人策略 pi_1 与 pi_2 在不同状态下输出的动作（由方向箭头表示）来度量二者之间的距离。](https://lh3.googleusercontent.com/npwokuqA8CGDIscGl3ZKdy4bdUreHL7gw5CyyyiQxKQ6GYuX2-1yQxiHrxXLkNBWIM1vvY-_X3kK7wP53pGaBBA_qlNABkLiiaJnDeGiwtNQEAM=w1440)

策略之间的相似性通过这些策略所产生的动作之间的距离来建模。

1. 为了提高数据效率，我们应用贝叶斯优化，优先安排更有希望的策略进入下一轮评估，即那些预测性能高且方差大的策略。

我们在多个领域的若干环境中演示了这一流程：dm-control、Atari、模拟机器人以及真实机器人。使用 A-OPS 可以快速降低遗憾值（regret），只需适度的策略评估次数，我们就能找出最佳策略。

![](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/627cf4fe45a4003f659b47c0_5.gif)

在一项真实世界的机器人实验中，A-OPS 比其他基线方法更快地识别出非常优秀的策略。用当前流程评估两个策略所需的时间，用 A-OPS 就足以在 20 个策略中找出一个遗憾值接近于零的策略。

我们的结果表明，通过利用离线数据、特殊的核函数和贝叶斯优化，仅用少量环境交互就可能完成有效的离线策略选择。A-OPS 的代码已开源并[发布在 GitHub 上](https://github.com/deepmind/active_ops)，附带一个可供尝试的示例数据集。
