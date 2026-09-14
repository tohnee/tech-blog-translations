---
title: "什么是过拟合？"
title_en: "What is overfitting?"
source: https://sebastianraschka.com/faq/docs/overfitting.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 什么是过拟合？

> 原文：[What is overfitting?](https://sebastianraschka.com/faq/docs/overfitting.html) · Sebastian Raschka's FAQ

假设我们有一个要在训练数据上拟合的假设（hypothesis）或模型 m。在机器学习中，训练性能——例如准确率——是我们在训练期间测量和优化的东西。我们把它称为训练准确率 ACCtrain(*m*)。

而机器学习中我们真正关心的是构建一个对未见数据泛化良好的模型，也就是说，我们想要构建一个在整个数据分布上都有高准确率的模型；我们称之为 ACCpopulation(*m*)。（通常，我们使用交叉验证技术和一个单独的独立测试集来估计泛化性能。）

现在，如果在算法的假设空间中存在另一个模型 *m'*，它的训练准确率比模型 *m* 更好，而泛化性能更差，我们就说发生了过拟合——即 m 对训练数据过拟合了。

## 学习曲线

作为一条经验法则，当训练样本数固定时，模型越复杂越容易过拟合。下图展示了某个 SVM 模型在某个数据集上的训练和验证准确率。这里，我把准确率绘制成关于逆正则化参数 C 的函数——C 值越大，针对复杂度的惩罚项就越大。

![](https://sebastianraschka.com/images/faq/overfitting/learning_curve_1.png)

我们观察到，随着 C 值增大（模型更复杂），训练与测试准确率之间的差异也更大。根据这张图，我们可以说 < 10^-1 处的模型对训练数据欠拟合，而 > 10^-1 处的模型对训练数据过拟合。

## 补救措施

对抗过拟合的补救措施包括

1. 通过增加偏差和/或减少参数数量来选择更简单的模型
   1. 加入正则化惩罚
   2. 降低特征空间的维度
2. 收集更多训练数据
