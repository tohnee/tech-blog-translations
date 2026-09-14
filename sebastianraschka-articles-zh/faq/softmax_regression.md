---
title: "什么是 Softmax 回归，它与 Logistic 回归有什么关系？"
title_en: "What is Softmax regression and how is it related to Logistic regression?"
source: https://sebastianraschka.com/faq/docs/softmax_regression.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 什么是 Softmax 回归，它与 Logistic 回归有什么关系？

Softmax 回归（同义词：多项 Logistic 回归、最大熵分类器，或简称多分类 Logistic 回归）是 logistic 回归的一种推广，可用于多分类任务（前提是假设各类别互斥）。相比之下，（标准的）Logistic 回归模型用于二分类任务。

下面我简要说明它的工作原理，以及 softmax 回归与 logistic 回归的区别。关于 logistic 回归我有更详细的讲解：[LogisticRegression - mlxtend](http://rasbt.github.io/mlxtend/user_guide/classifier/LogisticRegression/)，这里我复用其中一张图来说明问题：

![](https://sebastianraschka.com/images/faq/softmax_regression/logistic_regression_schematic.png)

顾名思义，在 softmax 回归（SMR）中，我们把 sigmoid logistic 函数替换成所谓的 *softmax 函数* φ：

![](https://sebastianraschka.com/images/faq/softmax_regression/1.png)

其中我们将净输入 z 定义为

![](https://sebastianraschka.com/images/faq/softmax_regression/2.png)

（*w* 是权重向量，*x* 是单个训练样本的特征向量，*w0* 是偏置单元。）
这个 softmax 函数计算的是：在给定权重和净输入 z(i) 的条件下，训练样本 x(i) 属于类别 *j* 的概率。也就是说，我们对 *j = 1, …, k* 中的每个类别标签都计算概率 *p(y = j | x(i); wj)*。注意分母中的归一化项，它使这些类别概率之和为 1。

为了直观说明 softmax 的概念，我们来看一个具体例子。假设我们有一个训练集，由来自 3 个不同类别（0、1、2）的 4 个样本组成。

![](https://sebastianraschka.com/images/faq/softmax_regression/3.png)

首先，我们要把类别标签编码成一种更便于处理的格式；这里采用 one-hot 编码：

![](https://sebastianraschka.com/images/faq/softmax_regression/4.png)

属于类别 0 的样本（第一行）在第一个单元格中为 1，属于类别 2 的样本在其所在行的第二个单元格中为 1，依此类推。
接下来，我们定义这 4 个训练样本的特征矩阵。这里假设数据集由 2 个特征组成；因此我们创建一个 4×(2+1) 维的矩阵（+1 对应偏置项）。

![](https://sebastianraschka.com/images/faq/softmax_regression/5.png)

类似地，我们创建一个 (2+1)×3 维的权重矩阵（每个特征一行，每个类别一列）。

为了计算净输入，我们把 4×(2+1) 的特征矩阵 **X** 与 (2+1)×3（n\_features × n\_classes）的权重矩阵 **W** 相乘。

**Z = WX**

得到一个 4×3 的输出矩阵（n\_samples × n\_classes）。

![](https://sebastianraschka.com/images/faq/softmax_regression/6.png)

现在可以计算前面讨论过的 softmax 激活了：

![](https://sebastianraschka.com/images/faq/softmax_regression/7.png)

![](https://sebastianraschka.com/images/faq/softmax_regression/8.png)

可以看到，现在每个样本（每行）的值都恰好加和为 1。例如，我们可以说第一个样本
`[ 0.29450637 0.34216758 0.36332605]` 有 29.45% 的概率属于类别 0。
现在，为了把这些概率转换回类别标签，我们只需取每一行 argmax 索引所在的位置：

![](https://sebastianraschka.com/images/faq/softmax_regression/9.png)

可以看到，我们的预测错得离谱，因为正确的类别标签是 `[0, 1, 2, 2]`。现在，为了训练我们的 logistic 模型（例如通过梯度下降等优化算法），我们需要定义一个想要最小化的代价函数 *J*：

![](https://sebastianraschka.com/images/faq/softmax_regression/10.png)

它是 n 个训练样本上所有交叉熵的平均值。交叉熵函数定义为

![](https://sebastianraschka.com/images/faq/softmax_regression/11.png)

这里 T 代表「target」（真实类别标签），O 代表输出（经 softmax 计算得到的概率；***而不是***预测的类别标签）。

![](https://sebastianraschka.com/images/faq/softmax_regression/12.png)

为了通过梯度下降学习 softmax 模型，我们需要计算导数

![](https://sebastianraschka.com/images/faq/softmax_regression/13.png)

然后用它沿梯度的反方向更新权重：

![](https://sebastianraschka.com/images/faq/softmax_regression/14.png) 对每个类别 j。

（注意 w\_j 是类别 *y=j* 对应的权重向量。）
我不打算在这里展开更多冗长的细节，但这个代价函数的导数最终可以化简为：

![](https://sebastianraschka.com/images/faq/softmax_regression/15.png)

使用这个代价梯度，我们迭代地更新权重矩阵，直到达到指定的轮数（epoch，即对训练集的完整遍历）或达到期望的代价阈值。
