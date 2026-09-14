---
title: "机器学习中的代价函数与损失函数"
title_en: "Cost Functions vs. Loss Functions in Machine Learning"
source: https://sebastianraschka.com/faq/docs/cost-vs-loss.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 机器学习中的代价函数与损失函数

> 原文：[Cost Functions vs. Loss Functions in Machine Learning](https://sebastianraschka.com/faq/docs/cost-vs-loss.html) · Sebastian Raschka's FAQ

*代价函数*（cost function）和*损失函数*（loss function）这两个术语是同义的（也有人称之为误差函数）。更一般的做法是先定义一个我们想要优化的目标函数。这个目标函数可以是：

- 最大化后验概率（例如朴素贝叶斯）
- 最大化适应度函数（遗传编程）
- 最大化总奖励/价值函数（强化学习）
- 最大化信息增益/最小化子节点不纯度（CART 决策树分类）
- 最小化均方误差代价（或损失）函数（CART、决策树回归、线性回归、自适应线性神经元……）
- 最大化对数似然或最小化交叉熵损失（或代价）函数
- 最小化铰链损失（支持向量机）
  ……
