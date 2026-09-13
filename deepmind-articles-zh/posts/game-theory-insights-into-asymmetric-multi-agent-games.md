---
title: "博弈论对非对称多智能体博弈的洞见"
title_en: "Game-theory insights into asymmetric multi-agent games"
source: https://deepmind.google/blog/game-theory-insights-into-asymmetric-multi-agent-games/
site: deepmind
date: 2018-01-17
crawled: 2026-09-13
translated: 2026-09-13
---

# 博弈论对非对称多智能体博弈的洞见

> 原文：[Game-theory insights into asymmetric multi-agent games](https://deepmind.google/blog/game-theory-insights-into-asymmetric-multi-agent-games/) · Google DeepMind

随着 AI 系统开始在现实世界中扮演越来越重要的角色，理解不同系统之间将如何相互作用就变得至关重要。

在发表于 [Scientific Reports](https://www.nature.com/srep/) 期刊的[最新论文](https://www.nature.com/articles/s41598-018-19194-4)中，我们借助[博弈论](https://en.wikipedia.org/wiki/Game_theory)的一个分支来阐明这一问题。具体而言，我们考察了两个智能系统在一类被称为[非对称博弈](https://en.wikipedia.org/wiki/Game_theory#Symmetric_/_Asymmetric)的特殊情形中如何行动和回应，这类博弈包括 Leduc 扑克以及[苏格兰场（Scotland Yard）](https://en.wikipedia.org/wiki/Scotland_Yard_(board_game))等多种桌面游戏。非对称博弈也天然地刻画了某些现实场景，例如买卖双方动机各异的自动化拍卖。我们的结果为这类情形提供了新的洞见，并揭示出一种出奇简单的分析方法。虽然我们关注的是这一理论如何应用于多个 AI 系统之间的交互，但我们相信这些结果同样可用于经济学、演化生物学和经验博弈论等领域。

> 该方法在数学上非常简洁，能够快速而直接地分析非对称博弈

博弈论是数学的一个分支，用于分析决策者在竞争情形中所采用的策略。它适用于各种情境下的人类、动物和计算机，但在 AI 研究中通常用于研究存在多个系统的「多智能体」环境，例如多台家用机器人协作打扫房屋。传统上，多智能体系统的演化动态是用简单的[对称博弈](https://en.wikipedia.org/wiki/Symmetric_game)来分析的，例如经典的[囚徒困境](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma)——在这类博弈中，每个参与者可以使用的动作集合是相同的。尽管这些博弈能为多智能体系统的运作方式提供有益洞见，并告诉我们如何达成对所有参与者都理想的结果——即纳什均衡（Nash equilibrium）——但它们无法建模所有情形。

我们的新技术使我们能够快速、便捷地识别出在更复杂的非对称博弈中用于寻找纳什均衡的策略——非对称博弈的特点是每个参与者拥有不同的策略、目标和奖励。这些博弈，以及我们用来理解它们的新技术，可以用博弈论研究中常用的一个协调博弈「性别之战（Battle of the Sexes）」的例子来说明。

在这个例子中，两名参与者需要协调一次夜间外出，去歌剧院或者看电影。其中一位略微偏好歌剧院，另一位略微偏好电影。这个博弈是非对称的，因为尽管两名参与者面对的选项相同，但基于各自的偏好，每个选项对应的奖励却不相同。为了维持他们的友谊——也就是均衡——参与者应当选择相同的活动（因此分开活动时收益为零）。

![非对称的「性别之战」协调博弈的收益矩阵：同选歌剧收益为 (3,2)，同选电影收益为 (2,3)，选择不一致时收益为 (0,0)。](https://lh3.googleusercontent.com/jwWLgsEQbbwBGt8lEf-LMFAMblkrcQJxmFwXWsqj0lFzMK9NzD01bNaRAc4XMz6A7MIDfaZ06hRtrnGq_DHu0nHi7hx6-ayDpX7KGqSU3O2G6Ffu=w1440)

这个博弈有三个均衡：(i) 两名参与者都决定去歌剧院；(ii) 都决定去看电影；(iii) 最后一个混合选项，即每位参与者有五分之三的时间选择自己偏好的选项。最后这个选项被称为「不稳定」均衡，可以通过把非对称博弈简化——或者说分解——为它的对称对应博弈，用我们的方法迅速找到。这些对应博弈本质上是把每个参与者的收益表各自视为一个独立的对称两人博弈，其均衡点与原非对称博弈的均衡点相重合。

在下图中，我们为两个简单的对应博弈绘出了纳什均衡，使我们能够快速找出非对称博弈 (a) 中的最优策略。反过来也可以做到，即用非对称博弈来确定其对称对应博弈中的均衡。

![三幅方向场图，展示非对称「性别之战」博弈 (a) 分解为两个对称对应博弈——博弈 1 (b) 与博弈 2 (c)——以确定均衡点。](https://lh3.googleusercontent.com/anzpnloh49usEKec3qmq5mYd1VUSLvR9_ERNXkvvee7XRzjJF7IDtgnhL8DU3itLD8y998c0hyFMYkMMmgI3uRZSe7BWzCq32ElmeVEbzT2pphf_rQ8=w1440)

红点代表纳什均衡。对于非对称博弈 (a)，它可以轻松地从两个对称对应博弈 (b) 和 (c) 的图中导出。在所有图中，x 轴对应参与者 1 选择歌剧院的概率，y 轴对应参与者 2 选择歌剧院的概率。

这一方法还可以应用于其他博弈，包括论文中详细描述的 Leduc 扑克。在所有这些情形中，该方法在数学上都十分简洁，能够对非对称博弈进行快速而直接的分析。我们希望这也能帮助大家加深对各种动态系统——包括多智能体环境——的理解。

在[这里](https://www.nature.com/articles/s41598-018-19194-4)阅读 Scientific Reports 原始论文。

在[这里](https://arxiv.org/abs/1803.06376)阅读后续的 AAMAS 论文。

Scientific Reports 论文由 Karl Tuyls、Julien Perolat、Marc Lanctot、Georg Ostrovski、Rahul Savani、Joel Leibo、Toby Ord、Thore Graepel 和 Shane Legg 撰写。AAMAS 论文由 Karl Tuyls、Julien Perolat、Marc Lanctot、Joel Leibo 和 Thore Graepel 撰写。

更新（2018 年 3 月 20 日）

我们的[最新论文](https://arxiv.org/abs/1803.06376)将在自治智能体与多智能体系统会议（AAMAS）上发表，它建立在上述 Scientific Reports 论文的基础上。[《经验博弈论分析的一种广义方法》（A Generalised Method for Empirical Game Theoretic Analysis）](https://arxiv.org/abs/1803.06376)提出了一种对多智能体交互进行经验分析的一般方法，既适用于对称博弈，也适用于非对称博弈。该方法可以理解多智能体策略之间如何相互作用、吸引子是什么、吸引域是什么样子，从而对所涉策略的强弱形成直观理解。此外，它还解释了需要考虑多少数据样本，才能保证近似博弈的均衡足够可靠。我们将该方法应用于多个领域，包括 AlphaGo、Colonel Blotto 和 Leduc 扑克。
