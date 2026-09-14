---
title: "朴素贝叶斯与逻辑回归"
title_en: "Naive Bayes vs. Logistic Regression"
source: https://sebastianraschka.com/faq/docs/naive-bayes-vs-logistic-regression.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 朴素贝叶斯与逻辑回归

> 原文：[Naive Bayes vs. Logistic Regression](https://sebastianraschka.com/faq/docs/naive-bayes-vs-logistic-regression.html) · Sebastian Raschka's FAQ

从宏观层面看，我会把它概括为「生成式模型与判别式模型」之别。

- |  |  |
  | --- | --- |
  | 生成式分类器学习联合概率 p(x, y) 的模型，并利用贝叶斯规则计算出 p(x | y) 来做出预测 |
- |  |  |
  | --- | --- |
  | 判别式模型「直接」学习后验概率 p(x | y) |

你可以把判别式模型想象成「能够区分说不同语言的人，但并不真正去学这些语言」。

在判别式模型里，你做出的「假设更少」。例如，在朴素贝叶斯分类中，你假设 p(x|y) 服从（通常为）高斯分布、伯努利分布或多项式分布，甚至还会违背特征条件独立的假设。站在判别式模型一边，Vapnik 曾写道：「应当直接解决分类问题本身，而绝不要把解决一个更一般的问题当作中间步骤。」
（Vapnik, Vladimir Naumovich, and Vlamimir Vapnik. Statistical learning theory. Vol. 1. New York: Wiley, 1998.）

不过，更偏好哪种方法确实取决于你的具体问题。我现在一时找不到参考出处，但例如在分类任务中，朴素贝叶斯收敛更快，但误差通常高于逻辑回归。在小数据集上，你或许想试试朴素贝叶斯；而随着训练集规模增大，逻辑回归很可能会带来更好的结果。
