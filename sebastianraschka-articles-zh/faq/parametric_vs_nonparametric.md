---
title: "参数化与非参数化学习算法"
title_en: "Parametric vs. Nonparametric Learning Algorithms"
source: https://sebastianraschka.com/faq/docs/parametric_vs_nonparametric.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 参数化与非参数化学习算法

> 原文：[Parametric vs. Nonparametric Learning Algorithms](https://sebastianraschka.com/faq/docs/parametric_vs_nonparametric.html) · Sebastian Raschka's FAQ

「非参数化」（non-parametric）这个词乍一听可能有点让人困惑：非参数化并不意味着它们没有参数！恰恰相反，非参数化模型（可以）随着数据量的增加而变得越来越复杂。

所以，在参数化模型中，我们拥有有限个参数；而在非参数化模型中，参数的数量（潜在）是无限的。换句话说，非参数化模型的复杂度随训练数据数量的增长而增长；而参数化模型拥有的参数个数是固定的（或者你愿意的话，说结构是固定的）。

线性模型，例如线性回归、逻辑回归和线性支持向量机，是典型的参数化「学习器」；这里参数的规模是固定的（即权重系数）。相比之下，K 近邻、决策树或 RBF 核 SVM 被视为非参数化学习算法，因为它们的参数数量随训练集规模而增长。——K 近邻和决策树好理解，但为什么 RBF 核 SVM 是非参数化的，而线性 SVM 是参数化的？因为在 RBF 核 SVM 中，我们通过计算训练点之间的两两距离来构造核矩阵，这使它成为非参数化的。

在统计学领域，「参数化」这个词还与一个指定的概率分布相关联，即你「假设」数据服从的分布，而这个分布带有有限个参数（例如正态分布的均值和标准差）；在非参数化模型中，你不做/没有这些假设。所以，直观地讲，我们可以把非参数化模型看作一种「无分布」或（准）无假设的模型。

不过请记住，「参数化」与「非参数化」的定义充其量也「有点含糊」；根据《The Handbook of Nonparametric Statistics 1》（1962）第 2 页：
「目前尚无一个精确且被普遍接受的『非参数』定义。本手册采用的观点是：如果一个统计程序的性质，在某些至少具有中等普遍性的假设成立时，能够以合理的近似得到满足，那么该程序就属于非参数类型。」
