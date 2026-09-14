---
title: "处理大量特征的机器学习"
title_en: "Machine Learning with a Large Number of Features"
source: https://sebastianraschka.com/faq/docs/large-num-features.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 处理大量特征的机器学习

如果有必要减少特征数量，以避免过拟合（源于维数灾难）和/或降低计算复杂度（即提高计算效率），主要有 3 种策略。

**1）正则化与稀疏化**

- 如果模型支持，我推荐使用 L1 或 ElasticNet 正则化，把一部分特征的权重归零。

**2）特征选择**

- 我们可以尝试各种不同的特征选择算法（例如按方差选择，或用贪心搜索：序列后向/前向选择、遗传算法等）。

**3）特征抽取**

- 我们可以通过向低维子空间的变换来压缩特征空间。一个流行的例子是主成分分析（PCA）。但必须记住，PCA 是一种线性变换技术，在非线性问题中可能会出问题。举例来说，考虑一个简单的「同心圆」数据集：

![](https://sebastianraschka.com/images/faq/large-num-features/concentric-circles.png)

假设蓝色样本属于一个类别，红色圆圈属于第二个类别。我们的目标是训练一个分类模型。进一步假设这个数据集的维度太多了（好吧，这里其实只有 2 个特征，但为了便于可视化，我们得保持「简单」）。现在，我们想把数据压缩到更低维的子空间上，这里是 1 维。
先从「标准」PCA 开始。你能看出问题所在吗？

![](https://sebastianraschka.com/images/faq/large-num-features/pca-pc1.png)

两个类别变得不可分了……
换核 PCA（kernel PCA）试试：

![](https://sebastianraschka.com/images/faq/large-num-features/kpca-pc1.png)

这好多了；现在我们可以训练一个线性分类器来分开这两个类别。但问题在于，我们引入了一个需要调节的额外超参数（gamma）。而且这种「核技巧」并非对任何数据集都奏效，还有许多比核 PCA「更强大」、更合适的流形学习技术。
例如，用局部线性嵌入（LLE）来展开著名的瑞士卷（Swiss Roll）：

![](https://sebastianraschka.com/images/faq/large-num-features/swiss-roll.png)

![](https://sebastianraschka.com/images/faq/large-num-features/lle1.png)

![](https://sebastianraschka.com/images/faq/large-num-features/lle2.png)
