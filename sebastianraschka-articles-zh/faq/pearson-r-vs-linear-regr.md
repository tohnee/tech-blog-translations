---
title: "Pearson R 与简单线性回归有什么区别？"
title_en: "What is the difference between Pearson R and Simple Linear Regression?"
source: https://sebastianraschka.com/faq/docs/pearson-r-vs-linear-regr.html
crawled: 2026-09-06
translated: 2026-09-14
---

# Pearson R 与简单线性回归有什么区别？

在"简单线性回归"（含一个变量的普通最小二乘回归）中，你拟合一条直线

ŷ = a + b \* x

以尝试用预测变量 *x* 来预测目标变量 *y*。

让我们通过一个简单的例子来说明它与线性相关系数（衡量两个变量线性相关或共同变化程度的指标）之间的关系。

x = [1.0, 1.8, 3.0, 3.7]  
y = [0.5, 2.0, 3.0, 3.9]

![](https://sebastianraschka.com/images/faq/pearson-r-vs-linear-regr/example-1.png)

## 变量之间的线性相关

Pearson 相关系数的计算公式为：

![](https://sebastianraschka.com/images/faq/pearson-r-vs-linear-regr/pearson.png)

可以看到，相关系数其实就是两个特征 *x* 和 *y* 之间的协方差（cov）被它们的标准差（σ）"标准化"后的结果，其中

标准差的计算公式为

![](https://sebastianraschka.com/images/faq/pearson-r-vs-linear-regr/sigma.png)

类似地，协方差的计算公式为

![](https://sebastianraschka.com/images/faq/pearson-r-vs-linear-regr/covariance.png)

在上面的简单例子中，我们得到

- cov(x, y) ≈ 1.3012
- σ\_x ≈ 1.0449
- σ\_y ≈ 1.2620
- r = 0.9868

## 简单线性回归

接下来，对于简单线性回归，我们按如下方式计算斜率：

![](https://sebastianraschka.com/images/faq/pearson-r-vs-linear-regr/slope.png)

为了看清相关系数 r 是如何参与其中的，我们把它改写为

![](https://sebastianraschka.com/images/faq/pearson-r-vs-linear-regr/slope_rewrite.png)

其中第一项就等于我们之前定义的 r；现在可以看到，我们可以用"线性相关系数"来计算回归直线的斜率：

![](https://sebastianraschka.com/images/faq/pearson-r-vs-linear-regr/slope_r.png)

延续上面的例子，我们得到 b ≈ 0.8171。

**所以，本质上，线性相关系数（Pearson r）就是简单线性回归直线（拟合结果）的标准化斜率。**
继续这个例子，我们现在可以计算 y 轴截距：

![](https://sebastianraschka.com/images/faq/pearson-r-vs-linear-regr/intercept.png)

a ≈ 0.4298

于是，我们的线性回归拟合结果为

ŷ = 0.4298 + 0.8171 \* x

![](https://sebastianraschka.com/images/faq/pearson-r-vs-linear-regr/example-1-fit.png)

## 标准化变量

实践中，我们常常会对输入变量做标准化：

![](https://sebastianraschka.com/images/faq/pearson-r-vs-linear-regr/standardize.png)

标准化之后，我们的变量具有标准正态分布的性质：均值为 0，
标准差为 1。

![](https://sebastianraschka.com/images/faq/pearson-r-vs-linear-regr/example-2.png)

换句话说，我们把变量的中心移到 0，这样就无需再计算 y 轴截距。

ŷ = a \* x = r \* x

如果我们使用优化算法来做多元线性回归（比如梯度下降），而不是闭式解（这在处理大型数据集时很方便），这一做法同样有用。此时我们希望对变量做标准化，好让梯度下降学习算法在多元线性回归中"均等地"学习各个模型系数。
这种方法的另一个优点是，此时的斜率恰好等于相关系数，从而省去了一步额外的计算。

ŷ = a \* x = r \* x = a \* 0.9868

![](https://sebastianraschka.com/images/faq/pearson-r-vs-linear-regr/example-2-fit.png)
