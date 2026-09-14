---
title: "机器学习中的降维方法"
title_en: "Dimensionality Reduction Methods in Machine Learning"
source: https://sebastianraschka.com/faq/docs/dimensionality-reduction.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 机器学习中的降维方法

> 原文：[Dimensionality Reduction Methods in Machine Learning](https://sebastianraschka.com/faq/docs/dimensionality-reduction.html) · Sebastian Raschka's FAQ

由于降维方法实在太多，我们把它拆成「特征选择」和「特征提取」两类来谈。

特征选择的一些例子：

- L1 正则化（例如逻辑回归）与稀疏性
- 方差阈值
- 基于线性模型权重的递归特征消除
- 随机森林/极端随机树与特征重要性（按平均信息增益计算）
- 序贯前向/后向选择
- 遗传算法
- 穷举搜索

特征提取的一些例子：

- 主成分分析（PCA）：无监督，在这些轴彼此正交的约束下返回方差最大的轴
- 线性判别分析（LDA；不要与 Latent Dirichlet Allocation 混淆）：监督，返回最大化类别可分性的轴（同样有轴彼此正交的约束）；另有一篇文章：Linear Discriminant Analysis bit by bit
- 核 PCA（kernel PCA）：使用核技巧把非线性数据变换到一个样本可能线性可分的特征空间（相比之下，LDA 和 PCA 都是线性变换技术
- 监督 PCA
- 以及更多非线性变换技术，可以在这里看到不错的汇总：[Nonlinear dimensionality reduction](https://en.wikipedia.org/wiki/Nonlinear_dimensionality_reduction)

\*\* 那么，我们该使用哪种技术？ \*\*

这在某种程度上也遵循「没有免费的午餐定理」原则：不存在永远占优的方法，一切取决于你的数据集。直觉上，如果面对的是一个线性分类任务，LDA 应该比 PCA 更合理，但实证研究表明情况并非总是如此。例如，核 PCA 能分开同心圆，却无法展开瑞士卷（Swiss Roll）；这时候，局部线性嵌入（LLE）会更合适。

![](https://sebastianraschka.com/images/faq/dimensionality-reduction/swiss-roll.png)

![](https://sebastianraschka.com/images/faq/dimensionality-reduction/rbf-kpca.png)

![](https://sebastianraschka.com/images/faq/dimensionality-reduction/lle.png)
