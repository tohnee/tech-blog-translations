---
title: "结合在线与离线测试改进 News Feed 排序"
title_en: "Combining online and offline tests to improve News Feed ranking"
date: 2019-04-03
source: https://ai.facebook.com/blog/online-and-offline-tests-to-improve-news-feed-ranking
crawled: 2026-09-22
translated: 2026-09-22
---

# 结合在线与离线测试改进 News Feed 排序

> 原文：[Combining online and offline tests to improve News Feed ranking](https://ai.facebook.com/blog/online-and-offline-tests-to-improve-news-feed-ranking) · Meta AI（Wayback 存档）

**研究内容：**A/B 测试是机器学习（ML）技术产品改进周期中的重要环节。但由于资源限制，将贝叶斯优化等先进技术应用于优化这些系统颇具挑战。我们提出了一种新的多任务贝叶斯优化方法，将在线 A/B 测试的观测结果与一个简单的离线模拟器结合起来。该模型最多可联合优化 20 个参数，而总共只需约 40 次在线 A/B 测试。我们利用该模型找出待在线测试的新系统配置，从而改进 News Feed 排序。我们还对其泛化行为进行了实证分析。

**工作原理：**与 Facebook 和 Instagram 使用的许多推荐系统一样，Facebook News Feed 使用多种信号（如机器学习模型的预测结果）对内容进行排序，这些信号通过一组规则组合起来，构成一套配置策略。由于系统动态特性复杂，改进系统的策略搜索只能通过 A/B 测试在线进行。我们的排序系统包含针对关注结果的预测模型，它们被用作信号。离线模拟是在线 A/B 测试的一种高吞吐量替代方案，可用于评估排序配置的变更。一种朴素的做法是把会话离线重放到一个采用新配置的模拟器中，再用现有模型预测排序后列表的在线结果。这种系统实现简单，因为它依赖现有的预测模型，但无法捕捉许多重要的行为动态，最终不能替代在线实验。

我们的做法是使用多任务高斯过程（MTGP），将少量在线测试与大量（未校准的）离线测试整合进单一模型。MTGP 能有效学会纠正模拟器误差，并借助离线测试的信息增强，做出准确的在线预测。然后我们结合 MTGP 与贝叶斯优化，找出更优、值得在线测试的策略。

**为什么重要：**减少所需的 A/B 测试数量，让工程师和研究人员能够在原本不可行的场景中使用贝叶斯优化。用简单、未校准的离线模拟来增强在线实验的能力，使我们能够加速系统改进，同时增加在线测试的正面配置数量。

阅读我们此前关于通过 A/B 测试使用贝叶斯优化调优在线系统的研究，以及我们如何将这一方法用于 Instagram 排序系统中的价值模型调优等场景。

**阅读完整论文：**Bayesian Optimization for Policy Search via Online-Offline Experimentation

**作者**

- Ben Letham，Facebook 数据科学家
- Eytan Bakshy，Facebook 研究经理
