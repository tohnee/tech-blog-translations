---
title: "如何选择预测建模技术"
title_en: "Choosing a Predictive Modeling Technique"
source: https://sebastianraschka.com/faq/docs/choosing-technique.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 如何选择预测建模技术

> 原文：[Choosing a Predictive Modeling Technique](https://sebastianraschka.com/faq/docs/choosing-technique.html) · Sebastian Raschka's FAQ

这是一个非常宽泛的问题，答案基本上能写满一整本书。简而言之，我会先考虑以下问题：

## 1. 你的目标变量是什么样的？

- 连续型目标变量？-> 回归
- 类别型（名义型）目标变量？-> 分类
- 有序型目标变量？-> 有序分类（ranked classification）
- 没有目标变量、想发现数据中的结构？-> 聚类分析、投影

## 2. 计算性能是否是考量因素？

- 使用更「廉价」的模型/算法
- 降维
- 特征选择
- 惰性学习器（lazy learner，例如 k 近邻）

## 3. 我的数据集能装进内存吗？如果不能：

- 核外学习（out-of-core learning）
- 分布式系统

## 4. 我的数据是线性可分的吗？

- 很难预先知道答案
- 比较不同的模型永远是个好主意

## 5. 找到合适的偏差-方差平衡点。我的模型过拟合了吗？

- 如果模型支持，就增大正则化强度
- 否则做降维或特征选择
- 可能的话收集更多训练数据（先用学习曲线确认）

## 6. 你打算让模型随新数据在线更新吗？

- 一种选择是惰性学习器（例如 K 近邻）；需要保留训练数据；无需学习过程，但预测开销更大
- 更新生成式模型一般相对廉价
- 另一种选择是用随机梯度下降做在线学习

……

这份清单还可以一直列下去 :)。我认为 Andreas Mueller 的 scikit-learn 算法「速查表」是一个绝佳的资源。（点击图片可在 scikit-learn 上查看原始的交互式版本）

[![Scikit-learn algorithm selection cheat sheet](https://sebastianraschka.com/images/faq/choosing-technique/scikit-cheatsheet.png)](http://scikit-learn.org/dev/tutorial/machine_learning_map/index.html)

[来源：http://scikit-learn.org/dev/tutorial/machine\_learning\_map/index.html]
