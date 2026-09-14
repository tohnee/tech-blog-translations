---
title: "闭式解对比梯度下降与 SGD"
title_en: "Closed-Form Solutions vs. Gradient Descent and SGD"
source: https://sebastianraschka.com/faq/docs/closed-form-vs-gd.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 闭式解对比梯度下降与 SGD

> 原文：[Closed-Form Solutions vs. Gradient Descent and SGD](https://sebastianraschka.com/faq/docs/closed-form-vs-gd.html) · Sebastian Raschka's FAQ

为了解释估计模型参数的几种替代方法之间的差异，我们来看一个具体的例子：普通最小二乘（Ordinary Least Squares，OLS）线性回归。
下图可以作为一个快速提示，帮助我们回忆简单线性回归模型的各个组成部分：

![](https://sebastianraschka.com/images/faq/closed-form-vs-gd/simple_regression.png)

在普通最小二乘（OLS）线性回归中，我们的目标是找到使垂直偏移最小化的那条直线（或超平面）。换句话说，我们把拟合得最好的直线定义为：在大小为 *n* 的数据集中，使目标变量（y）与预测输出在所有样本 *i* 上的误差平方和（SSE）或均方误差（MSE）最小的那条直线。

![](https://sebastianraschka.com/images/faq/closed-form-vs-gd/sse_mse.png)

现在，我们可以通过以下方法之一来实现一个执行普通最小二乘回归的线性回归模型：

- 用解析方式（闭式方程）求解模型参数
- 使用优化算法（梯度下降、随机梯度下降、牛顿法、单纯形法等）

## 1) 正规方程（闭式解）

对于"较小"的数据集，闭式解可能（也应该）是首选——前提是计算（"代价高昂"的）矩阵逆不成问题。对于非常大的数据集，或者 **X**T**X** 的逆可能不存在（矩阵不可逆或奇异，例如存在完全多重共线性的情况）的数据集，则应优先选择 GD 或 SGD 方法。
线性函数（线性回归模型）定义为：

![](https://sebastianraschka.com/images/faq/closed-form-vs-gd/linear_model.png)

其中 *y* 是响应变量，***x*** 是 *m* 维样本向量，***w*** 是权重向量（系数向量）。注意 *w0* 表示模型的 y 轴截距，因此 *x0=1*。
使用闭式解（正规方程），我们按下式计算模型的权重：

![](https://sebastianraschka.com/images/faq/closed-form-vs-gd/closed-form.png)

## 2) 梯度下降（GD）

使用梯度下降（GD）优化算法时，权重在每个 epoch（= 遍历一遍训练数据集）之后增量更新。

代价函数 *J(⋅)*，即误差平方和（SSE），可以写成：

![](https://sebastianraschka.com/images/faq/closed-form-vs-gd/j.png)

权重更新的大小和方向通过沿着代价梯度的反方向迈出一步来计算：

![](https://sebastianraschka.com/images/faq/closed-form-vs-gd/dw.png)

其中 *η* 是学习率。然后，在每个 epoch 之后按如下更新规则更新权重：

![](https://sebastianraschka.com/images/faq/closed-form-vs-gd/w_upd.png)

其中 **Δw** 是一个包含各权重系数 *w* 更新量的向量，其计算方式如下：

![](https://sebastianraschka.com/images/faq/closed-form-vs-gd/w_upd_expl.png)

本质上，我们可以把 GD 优化想象成一名登山者（权重系数）想要从山上（代价函数）走到山谷（代价最小值）中，每一步的幅度取决于坡度的陡峭程度（梯度）和登山者的腿长（学习率）。考虑一个只含单个权重系数的代价函数，我们可以把这个概念图示如下：

![](https://sebastianraschka.com/images/faq/closed-form-vs-gd/ball.png)

## 3) 随机梯度下降（SGD）

在 GD 优化中，我们基于完整训练集计算代价梯度；因此，有时也称其为 *批量 GD*（batch GD）。对于非常大的数据集，使用 GD 的代价可能相当高，因为遍历一遍训练集只前进一步——这样一来，训练集越大，算法更新权重就越慢，收敛到全局代价最小值所需的时间也就越长（注意 SSE 代价函数是凸函数）。

在随机梯度下降（SGD；有时也称 *迭代* 或 *在线* GD）中，我们**不像**上面 GD 那样累积权重更新：

![](https://sebastianraschka.com/images/faq/closed-form-vs-gd/iter_gd.png)

而是每处理完一个训练样本就更新一次权重：

![](https://sebastianraschka.com/images/faq/closed-form-vs-gd/iter_sgd.png)

这里"随机"（stochastic）一词源于这样一个事实：基于单个训练样本的梯度只是"真实"代价梯度的一个"随机近似"。由于这种随机性，在二维空间中可视化代价曲面时，SGD 通往全局代价最小值的路径不像 GD 那样"直接"，而可能呈"之"字形。不过，已有研究表明，如果代价函数是凸函数（或伪凸函数），SGD 几乎必然收敛到全局代价最小值 [1]。
此外，还有一些改进基于 GD 的学习的技巧，例如：

- 自适应学习率 η：选择一个随时间缩小学习率的衰减常数 *d*：
  ![](https://sebastianraschka.com/images/faq/closed-form-vs-gd/adaptive_learning.png)
- 动量学习：把前一次梯度的一个倍数加到权重更新中，以实现更快的更新：
  ![](https://sebastianraschka.com/images/faq/closed-form-vs-gd/decrease_const.png)

### 关于洗牌（shuffling）的说明

文献中可以见到好几种不同风格的 SGD。下面来看三种最常见的变体：

#### A)

- 在训练集中随机洗牌一次
  - 迭代一个或多个 epoch，或直到近似达到代价最小值
    - 对每个训练样本 *i*
      - 计算梯度并执行权重更新

#### B)

- 迭代一个或多个 epoch，或直到近似达到代价最小值
  - 在训练集中随机洗牌
    - 对每个训练样本 *i*
      - 计算梯度并执行权重更新

#### C)

- 迭代 *t* 次，或直到近似达到代价最小值：
  - 从训练集中随机抽取一个样本
    - 计算梯度并执行权重更新

在场景 A [3] 中，我们只在开始时对训练集洗牌一次；而在场景 B 中，我们在每个 epoch 之后都对训练集重新洗牌，以避免重复的更新循环。在场景 A 和场景 B 中，每个训练样本在每个 epoch 内只被用于更新模型权重一次。

在场景 C 中，我们从训练集中有放回地随机抽取训练样本 [2]。如果迭代次数 *t* 等于训练样本数，那么我们就是基于训练集的一个 *自助样本*（bootstrap sample）来学习模型。

## 4) 小批量梯度下降（MB-GD）

小批量梯度下降（Mini-Batch Gradient Descent，MB-GD）是批量 GD 与 SGD 之间的折中。在 MB-GD 中，我们基于较小的训练样本组来更新模型；我们既不是从 1 个样本（SGD）也不是从全部 *n* 个训练样本（GD）计算梯度，而是从 *1 < k < n* 个训练样本计算梯度（常见的小批量大小为 *k=50*）。

MB-GD 收敛所需的迭代次数比 GD 少，因为我们更新权重更频繁；同时，MB-GD 让我们能够利用向量化运算，这通常能带来比 SGD 更高的计算性能。

## 参考文献

- [1] Bottou, Léon (1998). “Online Algorithms and Stochastic Approximations”. Online Learning and Neural Networks. Cambridge University Press. ISBN 978-0-521-65263-6
- [2] Bottou, Léon. “Large-scale machine learning with SGD.” Proceedings of COMPSTAT’2010. Physica-Verlag HD, 2010. 177-186.
- [3] Bottou, Léon. “SGD tricks.” Neural Networks: Tricks of the Trade. Springer Berlin Heidelberg, 2012. 421-436.
