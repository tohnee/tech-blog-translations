---
title: "适用于任意损失与激活函数的反向传播"
title_en: "Backpropagation for Arbitrary Loss and Activation Functions"
source: https://sebastianraschka.com/faq/docs/backprop-arbitrary.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 适用于任意损失与激活函数的反向传播

> 原文：[Backpropagation for Arbitrary Loss and Activation Functions](https://sebastianraschka.com/faq/docs/backprop-arbitrary.html) · Sebastian Raschka's FAQ

反向传播基本上「只是」一种在多层神经网络中高效计算梯度的巧妙技巧。或者换句话说，反向传播就是利用链式法则，为以计算图表示的嵌套函数计算梯度。反向传播包含一些让梯度计算更高效的计算技巧，即「从后往前」执行矩阵-向量乘法，并存储中间值（或中间梯度）。因此，反向传播是按特定顺序应用链式法则以加速计算的一种特定方式。

换言之，反向传播是「倒着」计算链式法则，也就是说，对于形如下式的情形，

\[\frac{\partial A}{ \partial D} =\frac{\partial A}{ \partial B} \frac{\partial B}{ \partial C} \frac{\partial C}{ \partial D},\]

先计算

\[\frac{\partial B}{ \partial C} \frac{\partial C}{ \partial D}\]

而不是先计算

\[\frac{\partial A}{ \partial B} \frac{\partial B}{ \partial C}.\]

这会带来效率上的差异，因为神经网络的输出是一个向量，而输入和隐藏层激活值存储在矩阵中。矩阵乘矩阵比矩阵乘向量（这里的向量指 \(\mathbb{R}^{n \times 1}\) 矩阵）代价更高。

在多层神经网络中，常见的惯例是比如把 logistic sigmoid 单元与交叉熵（或负对数似然）损失函数搭配使用；不过这种选择本质上是任意的。损失函数和激活函数可以随意搭配组合，因为我们真正关心的只是计算损失对各层权重参数的梯度，以便对权重执行基于梯度的更新。

## 单层神经网络 / 逻辑回归示例

例如，假设我们想使用梯度下降，针对由损失函数 \(\mathcal{L}\) 计算出的误差 E，来更新单层神经网络中的权重，如下图所示。

这里，作为热身并为了简单起见，设 \(w\_i\) 为单层神经网络中的第 \(i\) 个权重参数。进一步，令

- \(w\_i\) 为我们要针对误差 E 进行更新的权重参数，
- \(x\_i\) 为网络输入，
- \(\sigma(\cdot)\) 为计算激活值 \(a\) 所用的激活函数，
- \(x\) 为输入值，
- \(b\) 为偏置单元，
- \(z\) 为由「net」函数计算的变量，即输入的加权和 \(\sum\_i w\_i x\_i\)，
- $o$ 为输出值，
- $t$ 为我们想要预测的目标值（例如类别标签）。

![backprop-1](https://sebastianraschka.com/images/faq/backprop-arbitrary/backprop-1.png)

简而言之，我们的目标是计算梯度

\[\frac{\partial E}{\partial w\_i},\]

以更新权重参数 \(w\_i\)：

\[\frac{\partial E}{\partial w\_i} = \frac{\partial E}{\partial o} \frac{\partial o}{\partial z} \frac{\partial z}{\partial w}\]

如果误差通过均方误差计算，

\[\mathcal{L(o, t)} =E = \frac{1}{2m} \sum\_j(t\_j-o\_j)^ 2,\]

我们会得到如下结果：

\[\begin{align}
\frac{\partial E}{w\_i} = -\frac{1}{m} \sum\_j (t\_j - o\_j) \frac{\partial o\_i}{\partial \text{net}\_i} \frac{\partial \text{net}\_i}{\partial w\_i}.
\end{align}\]

- 关于如何推导均方误差损失对网络输出的导数 \(\frac{\partial E}{\partial o}\)，请参阅相关 FAQ 条目 [What is the derivative of the Mean Squared Error?](https://sebastianraschka.com/faq/docs/mse-derivative.html)

用于计算输出（$o$）的导数 $\frac{\partial o\_i}{\partial \text{net}\_i}$ 取决于我们使用哪种激活函数。如果使用的是 logistic sigmoid 函数 \(\sigma\)，那么它是 \((1 - \sigma(z)) \sigma(z)\)，详见相关 FAQ 条目 [What is the derivative of the logistic sigmoid function?](https://sebastianraschka.com/faq/docs/logistic-sigmoid-derivative.html)

再加上简单的导数

\[\frac{\partial \text{net}\_i}{\partial w\_i} = x\_i,\]

我们可以把所有内容组合起来，得到

\[\begin{align}
\frac{\partial E}{w\_i} &= -\frac{1}{m} \sum\_j (t\_j - o\_j) \frac{\partial o\_i}{\partial \text{net}\_i} \frac{\partial \text{net}\_i}{\partial w\_i} \\
& = -\frac{1}{m} \sum\_j (t\_j - o\_j) o\_j(1-o\_j)x\_j.
\end{align}\]

上面虽然是在单层神经网络上演示反向传播的概念，但我们可以把这个概念扩展到多层。例如，考虑带一个隐藏层的多层神经网络的情形。与单层变体相比的变化部分已用红色标出。基本上，如果你把下面的多层变体与单层变体做比较，就会发现我只是复制粘贴了中间部分，并给权重、激活单元等加上了上标 (1) 和 (2)：

![backprop-2](https://sebastianraschka.com/images/faq/backprop-arbitrary/backprop-2.png)

所以在这种情形下，我们要计算「第一」层（$w^{(1)}$）和第二层（$w^{(2)}$）权重的梯度。例如，

我们前面定义的方程，

\[\frac{\partial E}{\partial w\_i} = \frac{\partial E}{\partial o} \frac{\partial o}{\partial z} \frac{\partial z}{\partial w},\]

​

可以用来计算隐藏层的权重：

\(\frac{\partial E}{\partial w\_i^{(2)}} = \frac{\partial E}{\partial o} \frac{\partial o}{\partial z^{(2)}} \frac{\partial z^{(2)}}{\partial w^{(2)}}.\)
输入层的梯度也可以类似地计算，

\[\frac{\partial E}{\partial w\_i^{(1)}} = \frac{\partial E}{\partial o} \frac{\partial o}{\partial z^{(2)}} \frac{\partial z^{(2)}}{\partial a^{(2)}}\frac{\partial a^{(2)}}{\partial z^{(1)}}\frac{\partial z^{(1)}}{\partial w\_j^{(1)}}.\]

请注意，反向传播算法区别于标准链式法则概念的一部分在于：我们保存来自较前层的中间值，用于计算较后层的梯度（这里是 \(\frac{\partial E}{\partial o} \frac{\partial o}{\partial z^{(2)}}\)）。

无论如何，关键结论是：你只需要计算上面的各个组成部分即可，而它们取决于你选择的损失函数和激活函数。
