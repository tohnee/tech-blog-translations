---
title: "决策树在大型数据集上的局限"
title_en: "Decision Tree Limitations on Large Datasets"
source: https://sebastianraschka.com/faq/docs/decision-tree-disadvantages.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 决策树在大型数据集上的局限

> 原文：[Decision Tree Limitations on Large Datasets](https://sebastianraschka.com/faq/docs/decision-tree-disadvantages.html) · Sebastian Raschka's FAQ

## 计算效率视角

这是一个组合搜索问题：在每次分裂时，我们都要找到能给我们"最高性价比"（最大化信息增益）的特征。如果采用"暴力"搜索方式，计算复杂度为 O(m^2)，其中 m 是训练集中的特征数；对于 n 个训练样本则是 O(n^2)（我想如果运气好，可以达到 O(n log(n))）。

来看一个简单的数据集——Iris（150 朵花、3 个类别、4 个连续特征）。每次分裂时，我们都必须重新评估全部 4 个特征，而且对每个特征还要找到最优的分裂值，例如萼片长度 <3.4 cm（这是针对二叉分裂而言）。计算复杂度正是人们大多数时候实现*二叉*决策树的原因之一。

## 预测性能视角

未经剪枝的模型由于维数灾难（curse of dimensionality）而更容易过拟合。然而，与其对单棵决策树进行剪枝，使用集成方法往往是更好的主意。我们可以：

- 组合那些通过聚焦难分类样本而相互学习的决策树桩（decision tree stump）（AdaBoost）
- 构建一个由未剪枝决策树组成的集成；抽取自助样本，并进行随机特征选择（随机森林）
- 抛开 bagging，把全部训练样本作为未剪枝树的输入；随机选择分裂特征和分裂值（= 极端随机树，Extremely randomized trees）

（相关主题：[随机森林模型是如何工作的？它与集成模型中的 bagging 和 boosting 有什么不同？](https://sebastianraschka.com/faq/docs/bagging-boosting-rf.html)）
