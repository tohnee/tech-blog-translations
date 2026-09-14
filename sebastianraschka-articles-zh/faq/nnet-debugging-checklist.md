---
title: "如何调试一个人工神经网络算法？"
title_en: "How do I debug an artificial neural network algorithm?"
source: https://sebastianraschka.com/faq/docs/nnet-debugging-checklist.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 如何调试一个人工神经网络算法？

> 原文：[How do I debug an artificial neural network algorithm?](https://sebastianraschka.com/faq/docs/nnet-debugging-checklist.html) · Sebastian Raschka's FAQ

导致神经网络出现意外「糟糕」性能的原因有很多很多。让我们整理一份可以按大致顺序逐项排查的快速检查清单，以便找到问题的根源

- 数据集是否没问题？更具体地说：噪声是不是很多？特征是否足够「有力」，能够区分类别？（先尝试一批现成的分类器来获得一个初始基准是个好主意；例如随机森林、softmax 回归或核 SVM 这样的分类器）
- 我们是不是忘了对特征做标准化？
- 我们是否实现并使用了梯度检查，以确保实现是正确的？
- 我们使用的是随机权重初始化方案（例如，从一个随机正态分布乘以一个小的系数 < 0），而不是把模型参数全部初始化为零权重吗？
- 我们是否尝试过增大或减小学习率？
- 我们是否检查过代价随时间在下降？如果在下降，是否尝试过增加 epoch 的数量？
- 我们是否尝试过用动量学习和/或衰减常数（例如 AdaGrad）来调整学习率？
- 我们是否尝试过与当前使用的激活函数不同的其他非线性激活函数（例如 logistic sigmoid、tanh 或 ReLU）？
  1. 当我们通过交叉验证（例如留出法或 k 折）估计网络性能时，是否注意到训练性能与验证性能之间存在很大差异？在训练集与验证集上性能的显著差异可能表明我们对训练数据过拟合得太厉害了。作为对策，我们可以尝试
  1. 尽可能收集更多训练样本
  2. 降低网络的复杂度（例如更少的节点、更少的隐藏层）
  3. 实现 dropout
  4. 在代价函数中加入针对复杂度的惩罚（例如 L2 正则化）
