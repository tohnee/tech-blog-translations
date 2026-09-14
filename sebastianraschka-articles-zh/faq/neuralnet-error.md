---
title: "我的神经网络误差上升，是哪里出了问题？"
title_en: "What is wrong when my neural network's error increases?"
source: https://sebastianraschka.com/faq/docs/neuralnet-error.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 我的神经网络误差上升，是哪里出了问题？

> 原文：[What is wrong when my neural network's error increases?](https://sebastianraschka.com/faq/docs/neuralnet-error.html) · Sebastian Raschka's FAQ

有很多可能的原因可以解释这个问题。可能是技术性原因——我们把反向传播实现错了；也可能是我们选择的学习率太高，进而导致越过（overshoot）了代价函数的局部极小值。

## 梯度检查

我总是会做的第一件事，是实现「梯度检查」（gradient checking）来确保实现是正确的。梯度检查非常容易实现，而且是一个很好的初步诊断手段；这里，我们只是把解析解与数值近似的梯度做比较

![](https://sebastianraschka.com/images/faq/neuralnet-error/approx-grad-1.png)

（注意，ε 只是一个 1e-5 左右的小数。）

![](https://sebastianraschka.com/images/faq/neuralnet-error/approx-grad-2.png)

更好的做法是使用带 +/- ε 的两点公式

![](https://sebastianraschka.com/images/faq/neuralnet-error/approx-grad-3.png)

然后，我们把这个数值近似的梯度与解析梯度进行比较：

![](https://sebastianraschka.com/images/faq/neuralnet-error/approx-grad-4.png)

根据网络架构的复杂程度，我们可以定出类似下面这样的判据：

- 相对误差 <= 1e-7：一切正常！
- 相对误差 <= 1e-4：情况有问题，应当深入排查。
- 相对误差 > 1e-4：我们的代码很可能有错误

## 缩放与打乱

接下来，我们要检查数据是否做了适当的缩放。例如，如果我们使用随机梯度下降、并把权重初始化为 0 附近的小随机数，那就要确保特征做了相应的标准化（均值 = 0、标准差 = 1，即标准正态分布的性质）。

![](https://sebastianraschka.com/images/faq/neuralnet-error/standardizing.png)

另外，还要确保每一轮遍历训练集之前都对训练集做打乱（shuffle），以避免随机梯度下降中出现循环。

## 学习率

最后，我们来看学习率本身。如果计算出的代价随时间推移不断上升，这可能只是说明我们在反复越过局部极小值。除了降低学习率之外，还有几个我经常加到自己实现里的技巧：

1. 用于自适应学习率的衰减常数 d；在自适应学习中，我们随时间缩小学习率 η：η / [1 + t \* d]，其中 t 是时间步
2. 一个基于先前梯度的动量因子，用于更快的初期学习

![](https://sebastianraschka.com/images/faq/neuralnet-error/momentum.png)
