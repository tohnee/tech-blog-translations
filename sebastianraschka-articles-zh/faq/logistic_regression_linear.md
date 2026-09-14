---
title: "为什么逻辑回归被视为线性模型？"
title_en: "Why is logistic regression considered a linear model?"
source: https://sebastianraschka.com/faq/docs/logistic_regression_linear.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 为什么逻辑回归被视为线性模型？

简短的回答是：逻辑回归被视为广义线性模型，因为其输出**永远**依赖于输入与参数的**加和**。换句话说，输出不可能依赖于参数之间的乘积（或商等）！

那么，这是为什么呢？我们不妨先回顾一下逻辑回归的基础，这样 hopefully 能让事情更清楚。逻辑回归是一种学习二分类模型的算法。它的一个很好的副作用是，它能给出一个样本属于类别 1（反之亦然：类别 0）的*概率*。我们的目标函数是最小化所谓的逻辑函数 Φ（某一种 sigmoid 函数）；它长这样：

![](https://sebastianraschka.com/images/faq/logistic_regression_linear/2.png)

现在，如果 *φ(z)* 大于 *0.5*（等价地：如果 *z* 大于 *0*），我们就把输入分类为类别 1（否则为类别 0）。尽管逻辑回归产生的是线性决策面（见下图中的分类示例），但这个逻辑（激活）函数看上去可一点都不线性，对吧！？

![](https://sebastianraschka.com/images/faq/logistic_regression_linear/4.png)

那么，让我们再深挖一点，看看计算 *z* 所用的等式——净输入函数（net input function）！

![](https://sebastianraschka.com/images/faq/logistic_regression_linear/1.png)

净输入函数其实就是输入特征与相应模型系数 **w** 的点积：

![](https://sebastianraschka.com/images/faq/logistic_regression_linear/3.png)

这里，x0 指的是偏置单元的权重，它恒等于 1（这个细节我们在这里不必操心）。我知道数学等式有时候会显得有点「抽象」，所以我们来看一个具体的例子。

假设我们有一个由 4 个特征组成的训练样本点 **x**（例如 [*Iris 数据集*](https://archive.ics.uci.edu/ml/datasets/Iris) 中的 *sepal length*（萼片长度）、*sepal width*（萼片宽度）、*petal length*（花瓣长度）和 *petal width*（花瓣宽度））：

```python
x = [1, 2, 3, 4]
```

再假设我们的权重向量长这样：

```python
w = [0.5, 0.5, 0.5, 0.5]
```

现在来计算 *z* 吧！

z = wTx = 1*0.5 + 2*0.5 + 3*0.5 + 4*0.5 = 5

---

虽然不是重点，但这个样本属于类别 1 的概率是 99.3%：

*Φ(z=148.41) = 1 / (1 + e-5) = 0.993*

---

关键在于我们的模型是***可加的（additive）***
我们的输出 *z* 依赖于权重参数值的可加性，例如：

*z = w1x1 + w2x2*

特征取值之间不存在交互，没有 w1x1 \* w2x2

之类的东西——那样的模型才是非线性的！
