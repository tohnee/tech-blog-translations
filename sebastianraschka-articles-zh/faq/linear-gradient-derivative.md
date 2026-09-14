---
title: "推导线性回归与 Adaline 的梯度下降"
title_en: "Deriving Gradient Descent for Linear Regression and Adaline"
source: https://sebastianraschka.com/faq/docs/linear-gradient-derivative.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 推导线性回归与 Adaline 的梯度下降

线性回归（Linear Regression）和自适应线性神经元（Adaline）彼此密切相关。事实上，Adaline 算法与线性回归完全相同，只是多了一个阈值函数 ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/1.png)，用于把连续输出转换成离散的类别标签

![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/2.png)

其中 $z$ 是净输入，由输入特征 **x** 与模型权重 **w** 的乘积求和计算得到：

![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/3.png)

（注意，![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/4.png) 指的是偏置单元，因此有 ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/5.png)。）

在线性回归和 Adaline 的情形中，激活函数 ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/6.png) 就是恒等函数，于是 ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/7.png)。

![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/regression-vs-adaline.png)

现在，为了学习最优的模型权重 **w**，我们需要定义一个可供优化的代价函数。这里，我们的代价函数 ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/8.png) 是误差平方和（SSE），并乘上 ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/9.png) 以便推导更简单：

![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/10.png)

其中 ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/11.png) 是第 *i* 个训练点 ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/12.png) 的标签或目标标签。

（注意，SSE 代价函数是凸函数，因此是可微的。）

简单来说，梯度下降学习可以概括如下：

1. 将权重初始化为 0 或很小的随机数。
2. 重复 *k* 个轮次（遍历训练集）
   1. 对每个训练样本 ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/12.png)
      - 计算预测输出值 ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/13.png)
      - 将 ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/13.png) 与实际输出 ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/14.png) 比较，并计算「权重更新」值
      - 累加「权重更新」值
   2. 用累积的「权重更新」值更新权重系数

把它翻译成更数学化的记号：

1. 将权重初始化为 0 或很小的随机数。
2. 重复 *k* 个轮次
   1. 对每个训练样本 ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/12.png)
      - ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/15.png)
      - ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/16.png) （其中 *η* 是学习率）；
      - ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/17.png)
   2. ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/18.png)

执行这一全局权重更新

![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/18.png),

可以理解为「沿代价梯度的相反方向、按学习率 *η* 缩放的一步来更新模型权重」

![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/19.png)

其中对每个 ![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/21.png) 的偏导数可以写成

![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/20.png)

总结：要用梯度下降学习模型系数，我们只需在每次遍历训练集时，沿梯度的相反方向走一步来更新权重 **w**——基本就是这些。但这个方程

![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/22.png)

是怎么得来的？让我们一步步走完整个推导。

![](https://sebastianraschka.com/images/faq/linear-gradient-derivative/23.png)
