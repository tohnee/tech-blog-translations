---
title: "正则化总能改进逻辑回归吗？"
title_en: "Does Regularization Always Improve Logistic Regression?"
source: https://sebastianraschka.com/faq/docs/regularized-logistic-regression-performance.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 正则化总能改进逻辑回归吗？

正则化并不会提升模型在算法用来学习模型参数（特征权重）的那份数据集上的表现。然而，它**可以提升泛化性能**，也就是在新的、未见过的数据上的表现——而这正是我们想要的。

直观地说，我们可以把正则化看作一种针对复杂度的惩罚。增大正则化强度会惩罚「过大」的权重系数——我们的目标是防止模型学到那些「特异之处」「噪声」，或者「在并不存在规律的地方臆想出规律」。

**再强调一次，我们不希望模型去死记硬背训练数据集，我们要的是一个能很好地泛化到新的、未见过的数据上的模型。**

更具体地说，如果我们的模型存在（高）方差（即它在训练数据上过拟合），我们可以把正则化看作是添加（或增大）偏置。另一方面，偏置过大会导致欠拟合（高偏置的一个典型标志是模型在训练集和测试集上的表现都「很差」）。我们知道，对于未正则化的模型，我们的目标是最小化代价函数，也就是说，我们要找到对应于全局代价最小值的特征权重（请记住，逻辑回归的代价函数是凸函数）。

![](https://sebastianraschka.com/images/faq/regularized-logistic-regression-performance/unregularized.png)

现在，如果我们对代价函数进行正则化（例如通过 L2 正则化），我们就会在代价函数（J）中添加一个额外的项，这一项会随参数权重（w）值的增大而增大；请记住，在正则化中我们引入了一个新的超参数 lambda，用来控制正则化强度。

![](https://sebastianraschka.com/images/faq/regularized-logistic-regression-performance/l2-term.png)

因此，我们的新问题就是在这一新增约束条件下最小化代价函数。

![](https://sebastianraschka.com/images/faq/regularized-logistic-regression-performance/regularized.png)

直观上，我们可以把上图中位于坐标中心的那个「球体」看作我们的「预算」。现在，我们的目标仍然不变：最小化代价函数。但我们受到了正则化项的约束；我们要在「预算」（即球体）范围内尽可能接近全局最小值。
