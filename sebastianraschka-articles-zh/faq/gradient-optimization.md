---
title: "什么是梯度下降和随机梯度下降？"
title_en: "What are gradient descent and stochastic gradient descent?"
source: https://sebastianraschka.com/faq/docs/gradient-optimization.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 什么是梯度下降和随机梯度下降？

> 原文：[What are gradient descent and stochastic gradient descent?](https://sebastianraschka.com/faq/docs/gradient-optimization.html) · Sebastian Raschka's FAQ

## 梯度下降（GD）优化

使用梯度下降（Gradient Descent）优化算法时，权重在每个 epoch（= 遍历一遍训练数据集）之后增量更新。

权重更新的大小和方向通过沿着代价梯度的反方向迈出一步来计算：

\[\Delta w\_j = -\eta \frac{\partial J}{\partial w\_j},\]

其中 \(\eta\) 是学习率。然后，在每个 epoch 之后按如下更新规则更新权重：

\[\mathbf{w} := \mathbf{w} + \Delta\mathbf{w},\]

其中 \(\Delta\mathbf{w}\) 是一个包含各权重系数 \({w}\) 更新量的向量，其计算方式如下：

\[\Delta w\_j = -\eta \frac{\partial J}{\partial w\_j}\\
= -\eta \sum\_i (\text{target}^{(i)} - \text{output}^{(i)})(-x\_{j}^{(i)})\\
= \eta \sum\_i (\text{target}^{(i)} - \text{output}^{(i)})x\_{j}^{(i)}.\]

本质上，我们可以把梯度下降优化想象成一名登山者（权重系数）想要从山上（代价函数）走到山谷（代价最小值）中，每一步的幅度取决于坡度的陡峭程度（梯度）和登山者的腿长（学习率）。考虑一个只含单个权重系数的代价函数，我们可以把这个概念图示如下：

![](https://sebastianraschka.com/images/faq/gradient-optimization/ball.png)

## 随机梯度下降（SGD）

在梯度下降优化中，我们基于完整训练集计算代价梯度；因此，有时也称其为*批量梯度下降*（batch gradient descent）。对于非常大的数据集，使用梯度下降的代价可能相当高，因为遍历一遍训练集只前进一步——这样一来，训练集越大，算法更新权重就越慢，收敛到全局代价最小值所需的时间也就越长（注意 SSE 代价函数是凸函数）。

在随机梯度下降（Stochastic Gradient Descent；有时也称*迭代*或*在线*梯度下降）中，我们**不像**上面梯度下降那样累积权重更新：

- 迭代一个或多个 epoch：
  - 对每个权重 \(j\)
    - \(w\_j := w + \Delta w\_j\)，其中：\(\Delta w\_j= \eta \sum\_i (\text{target}^{(i)} - \text{output}^{(i)})x\_{j}^{(i)}\)

而是每处理完一个训练样本就更新一次权重：

- 迭代一个或多个 epoch，或直到近似达到代价最小值：
  - 对训练样本 \(i\)：
    - 对每个权重 \(j\)
      - \(w\_j := w + \Delta w\_j\)，其中：\(\Delta w\_j= \eta (\text{target}^{(i)} - \text{output}^{(i)})x\_{j}^{(i)}\)

这里「随机」（stochastic）一词源于这样一个事实：基于单个训练样本的梯度只是「真实」代价梯度的一个「随机近似」。由于这种随机性，在二维空间中可视化代价曲面时，SGD 通往全局代价最小值的路径不像梯度下降那样「直接」，而可能呈「之」字形。不过，已有研究表明，如果代价函数是凸函数（或伪凸函数），随机梯度下降几乎必然收敛到全局代价最小值 [1]。

### 随机梯度下降的洗牌（shuffling）

文献中可以见到好几种不同风格的随机梯度下降。下面来看三种最常见的变体：

### A)

- 在训练集中随机洗牌一次
  - 迭代一个或多个 epoch，或直到近似达到代价最小值
    - 对每个训练样本 *i*
      - 计算梯度并执行权重更新

### B)

- 迭代一个或多个 epoch，或直到近似达到代价最小值
  - 在训练集中随机洗牌
    - 对每个训练样本 *i*
      - 计算梯度并执行权重更新

### C)

- 迭代 *t* 次，或直到近似达到代价最小值：
  - 从训练集中随机抽取一个样本
    - 计算梯度并执行权重更新

在场景 A [3] 中，我们只在开始时对训练集洗牌一次；而在场景 B 中，我们在每个 epoch 之后都对训练集重新洗牌，以避免重复的更新循环。在场景 A 和场景 B 中，每个训练样本在每个 epoch 内只被用于更新模型权重一次。

在场景 C 中，我们从训练集中有放回地随机抽取训练样本 [2]。如果迭代次数 *t* 等于训练样本数，那么我们就是基于训练集的一个*自助样本*（bootstrap sample）来学习模型。

## 小批量梯度下降（MB-GD）

小批量梯度下降（Mini-Batch Gradient Descent，MB-GD）是批量 GD 与 SGD 之间的折中。在 MB-GD 中，我们基于较小的训练样本组来更新模型；我们既不是从 1 个样本（SGD）也不是从全部 *n* 个训练样本（GD）计算梯度，而是从 \(1 < k < n\) 个训练样本计算梯度（常见的小批量大小为 \(k=50\)）。

MB-GD 收敛所需的迭代次数比 GD 少，因为我们更新权重更频繁；同时，MB-GD 让我们能够利用向量化运算，这通常能带来比 SGD 更高的计算性能。

## 学习率

- 自适应学习率 \(\eta\)：选择一个随时间缩小学习率的衰减常数 *d*：\(\eta(t+1) := \eta(t) / (1 + t \times d)\)
- 动量学习：把前一次梯度的一个倍数加到权重更新中，以实现更快的更新：\(\Delta \mathbf{w}\_{t+1} := \eta \nabla J(\mathbf{w}\_{t+1}) + \alpha \Delta {w}\_{t}\)

## 参考文献

- [1] Bottou, Léon (1998). *"Online Algorithms and Stochastic Approximations"*. Online Learning and Neural Networks. Cambridge University Press. ISBN 978-0-521-65263-6
- [2] Bottou, Léon. *"Large-scale machine learning with stochastic gradient descent."* Proceedings of COMPSTAT'2010. Physica-Verlag HD, 2010. 177-186.
- [3] Bottou, Léon. *"Stochastic gradient descent tricks."* Neural Networks: Tricks of the Trade. Springer Berlin Heidelberg, 2012. 421-436.
