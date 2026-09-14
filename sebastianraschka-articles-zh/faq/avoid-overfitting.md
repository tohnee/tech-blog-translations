---
title: "如何避免过拟合？"
title_en: "How can I avoid overfitting?"
source: https://sebastianraschka.com/faq/docs/avoid-overfitting.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 如何避免过拟合？

> 原文：[How can I avoid overfitting?](https://sebastianraschka.com/faq/docs/avoid-overfitting.html) · Sebastian Raschka's FAQ

简而言之，通用策略是：

1. 收集更多数据
2. 使用对多个模型做「平均」的集成方法
3. 选择更简单的模型 / 对复杂度施加惩罚

关于第一点，绘制学习曲线会有帮助，也就是把训练性能与验证（或交叉验证）性能画在一起。如果你观察到「更多数据有助于缩小二者差距」的趋势，而且你也有能力收集更多数据，那么这很可能是最好的选择。

以我的经验来看，在规模偏小的数据集上构建稳健的预测模型，集成（ensembling）大概是最省事的办法。就像现实生活中一样，在做决定之前咨询一群「专家」通常不是坏事 ;)

至于第三点，我在开始一个预测建模任务时，通常会用最简单的模型作为基准：一般是逻辑回归。如果我们的模型容量过大——需要拟合的模型参数太多、需要调优的超参数太多——过拟合就会成为一个实实在在的问题。如果数据集很小，简单模型永远是防止过拟合的好选择，同时它也是与更「复杂」的候选模型进行比较时的良好基准。
