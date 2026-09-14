---
title: "袋装和提升可以与逻辑回归一起使用吗？"
title_en: "Do bagging and boosting can be used with logistic regression?"
source: https://sebastianraschka.com/faq/docs/logistic-boosting.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 袋装和提升可以与逻辑回归一起使用吗？

我不确定袋装（bagging）用在逻辑回归上有多大意义——袋装的作用是降低过拟合训练数据的深层决策树模型的方差，而这并不太适用于逻辑回归。

不过提升（boosting）是可行的，但我觉得在这里「堆叠（stacking）」会是更好的方法。堆叠会更「强大」一些，因为我们不用预先指定的公式来调整权重，而是训练一个元分类器（meta-classifier）来学习组合这些模型的最优权重。

下面是众多有趣的相关论文之一，推荐你看看 :)

- "Is Combining Classifiers with Stacking Better than Selecting the Best One?"（用堆叠组合分类器是否优于只选最好的那一个？）
