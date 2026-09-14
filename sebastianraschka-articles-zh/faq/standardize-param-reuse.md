---
title: "为什么测试数据必须使用训练集的缩放参数"
title_en: "Why Test Data Must Use Training-Set Scaling Parameters"
source: https://sebastianraschka.com/faq/docs/standardize-param-reuse.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 为什么测试数据必须使用训练集的缩放参数

针对这个非常常见的问题，我来举一个例子，说明为什么我们不希望对新的（或测试）数据「从头」做标准化。

假设我们有一个简单的训练集，由 3 个样本和 1 个特征组成（不妨把这个特征叫做「length/长度」）：

- train\_1: 10 cm -> class\_2
- train\_2: 20 cm -> class\_2
- train\_3: 30 cm -> class\_1

mean: 20, std.: 8.2

标准化之后，变换得到的特征值为

- train\_std\_1: -1.21 -> class\_2
- train\_std\_2: 0 -> class\_2
- train\_std\_3: 1.21 -> class\_1

接下来，假设我们的模型学到的是：把标准化后的长度值 < 0.6 的样本分类为 class\_2（否则分为 class\_1）。到目前为止一切正常。现在，假设我们有 3 个未标注的数据点想要分类：

- new\_4: 5 cm -> class ?
- new\_5: 6 cm -> class ?
- new\_6: 7 cm -> class ?

如果看训练集中「未经标准化的 length 值」，直觉上可以说这些样本都很可能属于 class\_2。然而，如果我们对它们重新计算标准差和均值来做标准化，得到的数值会与之前训练集中的数值相仿，于是分类器会（很可能是错误地）把样本 4 和 5 分为 class 2。

- new\_std\_4: -1.21 -> class 2
- new\_std\_5: 0 -> class 2
- new\_std\_6: 1.21 -> class 1

但如果我们使用训练集的均值 20 cm 和四舍五入后的标准差 8.2 cm，计算 `(length - 20) / 8.2`，就会得到：

- new\_4: -1.83 -> class 2
- new\_5: -1.71 -> class 2
- new\_6: -1.59 -> class 2

5 cm、6 cm、7 cm 这些值比我们之前在训练集中见过的任何值都要低得多。因此，「新样本」标准化后的特征远低于训练集中所有标准化特征，才是合理的结果。
