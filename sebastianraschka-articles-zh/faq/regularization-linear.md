---
title: "我们如何对广义线性模型进行正则化？"
title_en: "How do we regularize generalized linear models?"
source: https://sebastianraschka.com/faq/docs/regularization-linear.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 我们如何对广义线性模型进行正则化？

> 原文：[How do we regularize generalized linear models?](https://sebastianraschka.com/faq/docs/regularization-linear.html) · Sebastian Raschka's FAQ

## 概述

我们可以把正则化理解为一种向模型引入额外偏置的方法，用于降低高方差模型的过拟合程度。通过在代价函数中加入正则化项，我们对较大的模型系数（权重）施加惩罚；其效果就是降低模型的复杂度。

## L2 正则化

在 L2 正则化中，我们通过计算权重系数（权重向量 \(\mathbf{w}\)）的欧几里得范数来收缩权重；\(\lambda\) 是待优化的正则化参数。

\[L2: \lambda\; \lVert \mathbf{w} \lVert\_2 = \lambda \sum\_{j=1}^{m} w\_j^2\]

例如，我们可以按如下方式对误差平方和代价函数（SSE）进行正则化：
\(SSE = \sum^{n}\_{i=1} \big(\text{target}^{(i)} - \text{output}^{(i)}\big)^2 + L2\)

直观上，我们可以把回归看作是添加了一个额外的惩罚项或约束，如下图所示。在没有正则化的情况下，我们的目标是找到全局代价最小值。而加入正则化惩罚之后，我们的目标变成在「必须停留在预算之内」（灰色阴影球体）这一约束条件下最小化代价函数。

![](https://sebastianraschka.com/images/faq/reqularization-linear/l2.png)

此外，我们可以通过正则化参数 \(\lambda\) 来控制正则化强度。\(\lambda\) 的值越大，模型的正则化越强。当 \(\lambda\) 趋于无穷大时，权重系数会趋近于 0。

## L1 正则化

在 L1 正则化中，我们使用权重系数（权重向量 \(\mathbf{w}\)）的绝对值来收缩权重；\(\lambda\) 是待优化的正则化参数。

\[L1: \lambda \; \lVert\mathbf{w}\rVert\_1 = \lambda \sum\_{j=1}^{m} |w\_j|\]

例如，我们可以按如下方式对误差平方和代价函数（SSE）进行正则化：
\(SSE = \sum^{n}\_{i=1} \big(\text{target}^{(i)} - \text{output}^{(i)}\big)^2 + L1\)

从本质上讲，L1 正则化与 L2 正则化非常相似。不过，L2 使用的是二次惩罚项，而这里我们是按权重系数的绝对值来惩罚模型。正如下图所示，我们的「预算」带有「尖锐的边角」，这正是 L1 模型之所以能产生稀疏性的几何解释。

![](https://sebastianraschka.com/images/faq/reqularization-linear/l1.png)

### 参考文献

- [1] M. Y. Park and T. Hastie. [*"L1-regularization path algorithm for generalized linear models"*](https://web.stanford.edu/~hastie/Papers/glmpath.pdf). Journal of the Royal Statistical Society: Series B (Statistical Methodology), 69(4):659–677, 2007.
- [2] A. Y. Ng. [*"Feature selection, L1 vs. L2 regularization, and rotational invariance"*](http://dl.acm.org/citation.cfm?id=1015435). In Proceedings of the twenty-first international conference on Machine learning, page 78. ACM, 2004.
