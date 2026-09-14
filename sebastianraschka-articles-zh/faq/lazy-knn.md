---
title: "为什么近邻算法是一种惰性算法？"
title_en: "Why is Nearest Neighbor a Lazy Algorithm?"
source: https://sebastianraschka.com/faq/docs/lazy-knn.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 为什么近邻算法是一种惰性算法？

尽管近邻算法（例如用于分类的 k 近邻，k-NN）是非常「简单」的算法，但这并不是它们被称为*惰性*（lazy）的原因 ;)。k 近邻（k-NN）之所以是惰性学习器，是因为它不从训练数据中学习判别函数，而只是把训练数据集「记住」。

举例来说，逻辑回归算法在训练阶段学习它的模型权重（参数）。相比之下，k 近邻没有训练阶段。这听起来也许非常省事，但这一特性并非没有代价：k 近邻的「预测」步骤开销相当大！每次想做一个预测，k 近邻都要在整个训练集中搜索最近邻！（注意，有一些技巧（例如 BallTree 和 KDTree）可以稍微加速这一过程。）

总结一下：急切学习器（eager learner）有模型拟合或训练步骤；惰性学习器（lazy learner）没有训练阶段。
