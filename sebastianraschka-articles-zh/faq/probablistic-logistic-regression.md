---
title: "正则化逻辑回归的概率视角"
title_en: "A Probabilistic View of Regularized Logistic Regression"
source: https://sebastianraschka.com/faq/docs/probablistic-logistic-regression.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 正则化逻辑回归的概率视角

我们直接从极大似然函数开始：

![](https://sebastianraschka.com/images/faq/probablistic-logistic-regression/1.png)

其中 phi 是条件概率，即 sigmoid（logistic）函数：

![](https://sebastianraschka.com/images/faq/probablistic-logistic-regression/2.png)

![](https://sebastianraschka.com/images/faq/probablistic-logistic-regression/3.png)

而 z 就是*净输入*（net input，一个标量）：

![](https://sebastianraschka.com/images/faq/probablistic-logistic-regression/4.png)

所以，最大化似然就是最大化概率。既然我们谈的是"代价"，那就把似然函数反过来，以便最小化一个代价函数 J。首先取对数，得到多数人都熟悉的那个等式（在求偏导时使用"加法技巧"特别方便，例如当你使用梯度下降或随机梯度下降时）：

![](https://sebastianraschka.com/images/faq/probablistic-logistic-regression/5.png)

![](https://sebastianraschka.com/images/faq/probablistic-logistic-regression/6.png)

现在，想象我们针对一个二维数据集，把代价绘制成两个权重的函数。对于未正则化的代价，我们会在某个特定的 w1、w2 组合处找到全局代价最小值（图中中心的圆点）。关键思想是：我们会把权重增大到到达全局代价最小值所需的程度。

![](https://sebastianraschka.com/images/faq/probablistic-logistic-regression/7.png)

接下来，加入一个正则化项，比如 L2：

![](https://sebastianraschka.com/images/faq/probablistic-logistic-regression/8.png)

这基本上意味着，我们会把权重向量欧氏范数的平方加到代价上。换句话说，我们现在受到了约束，由于这个不断增大的惩罚，再也达不到全局最小值了。基本上，我们现在必须找到那个"最佳平衡点"：在"w1、w2 轴上都不能走得太远"这一约束下使代价最小的点。（在下图中，球体的大小取决于一个额外的超参数 lambda。）

![](https://sebastianraschka.com/images/faq/probablistic-logistic-regression/9.png)

这就好比我们给权重加上了一个先验。我们不再是在给定训练数据下最大化似然（最小化代价函数），而是在给定这个额外信息偏置的条件下最大化似然。
