---
title: "统计建模 vs. 机器学习"
title_en: "Statistical Modeling vs. Machine Learning"
source: https://sebastianraschka.com/faq/docs/statistical-modeling-vs-machine-learning.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 统计建模 vs. 机器学习

作为一名讲授机器学习课程的统计学教授，这是学生们最常问我的问题之一。当然，这个问题可以从很多角度来切分。在我看来，如果必须归结为几个要点，我会强调以下几点：

- 在统计建模中，我们通常使用参数化方法（例如，线性回归或 logistic 回归是参数化模型最简单的例子——我们预先指定参数的数量），而在机器学习中，我们常常使用非参数化方法，即不预先指定模型的结构（例如 K 近邻、决策树、核 SVM 等）
- 在大多数统计模型中，我们假设特征（预测变量、协变量）是可加的（additive）
- 使用统计模型时，我们通常非常关心不确定性估计（置信区间、假设检验等）
- 使用机器学习模型时，我们通常不做诸如无共线性、残差正态分布之类实质性/特别的假设
- 机器学习模型的绝对预测性能通常优于统计模型（不过，它们往往不具备统计模型那样的可解释性）

我想推荐两篇与该主题相关的文章：

- Breiman, L. (2001). [Statistical modeling: The two cultures](https://projecteuclid.org/euclid.ss/1009213726)（含评论及作者答复）。Statistical science, 16(3), 199-231.
- Carmichael, I., & Marron, J. S. (2018). [Data science vs. statistics: two cultures?](https://link.springer.com/article/10.1007/s42081-018-0009-3). Japanese Journal of Statistics and Data Science, 1(1), 117-138.
