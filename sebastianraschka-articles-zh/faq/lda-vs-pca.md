---
title: "降维时线性判别分析（LDA）与主成分分析（PCA）有什么区别？"
title_en: "What is the difference between LDA and PCA for dimensionality reduction?"
source: https://sebastianraschka.com/faq/docs/lda-vs-pca.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 降维时线性判别分析（LDA）与主成分分析（PCA）有什么区别？

线性判别分析（LDA）和主成分分析（PCA）都是线性变换技术：LDA 是监督方法，而 PCA 是无监督方法——PCA 会忽略类别标签。

可以把 PCA 想象成一种寻找最大方差方向的技术：

![](https://sebastianraschka.com/images/faq/lda-vs-pca/pca.png)

与 PCA 不同，LDA 试图找到一个能最大化类别可分性的特征子空间（注意，在上图中，LD 2 会是一个非常糟糕的线性判别方向）。

![](https://sebastianraschka.com/images/faq/lda-vs-pca/lda.png)

请记住，LDA 假设各类别服从正态分布且具有相等的类协方差。
如果你对实证比较感兴趣：A. M. Martinez and A. C. Kak. PCA versus LDA. Pattern Analysis and Machine Intelligence, IEEE Transactions on, 23(2):228–233, 2001.（在一个图像识别任务中，如果给定类别的样本数相对较少，PCA 往往能带来更好的分类结果。）
