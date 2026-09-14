---
title: "为什么说朴素贝叶斯分类器是“朴素”的？"
title_en: "Why is the Naive Bayes Classifier naive?"
source: https://sebastianraschka.com/faq/docs/naive-naive-bayes.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 为什么说朴素贝叶斯分类器是“朴素”的？

> 原文：[Why is the Naive Bayes Classifier naive?](https://sebastianraschka.com/faq/docs/naive-naive-bayes.html) · Sebastian Raschka's FAQ

先来快速看一下贝叶斯定理（Bayes' Theorem）：

![](https://sebastianraschka.com/images/faq/naive-naive-bayes/bayes-theorem-english.png)

在模式分类的语境下，我们可以把它写成

![](https://sebastianraschka.com/images/faq/naive-naive-bayes/bayes_theorem.png)

![](https://sebastianraschka.com/images/faq/naive-naive-bayes/let.png)

如果我们将贝叶斯定理用于分类，那么我们的目标（也就是目标函数）就是最大化后验概率

![](https://sebastianraschka.com/images/faq/naive-naive-bayes/decision_rule.png)

下面再具体谈谈其中各个组成部分。先验代表我们的专家知识（或其他任何先验知识）；实践中，先验通常通过 MLE 来估计（按类频率计算）。证据项则可以约去，因为它对所有类别都是常数。

再来看朴素贝叶斯分类器中「朴素」的部分：它之所以「朴素」，是因为我们把条件概率（有时也称为似然）计算成每个特征各自概率的乘积：

![](https://sebastianraschka.com/images/faq/naive-naive-bayes/likelihood.png)

由于这一假设（特征之间绝对独立）在实践中恐怕永远不会真正成立，这正是朴素贝叶斯真正「朴素」的地方。
