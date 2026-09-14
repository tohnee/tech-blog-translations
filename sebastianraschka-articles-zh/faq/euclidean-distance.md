---
title: "在机器学习中，欧氏距离是什么？"
title_en: "What is Euclidean distance in terms of machine learning?"
source: https://sebastianraschka.com/faq/docs/euclidean-distance.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 在机器学习中，欧氏距离是什么？

> 原文：[What is Euclidean distance in terms of machine learning?](https://sebastianraschka.com/faq/docs/euclidean-distance.html) · Sebastian Raschka's FAQ

它只是 *n* 维特征空间中一对样本 *p* 和 *q* 之间的一种距离度量：

![](https://sebastianraschka.com/images/faq/euclidean-distance/eucl-1.png)

例如，可以把它想象成二维特征空间中一条「笔直的连接」线段：

![](https://sebastianraschka.com/images/faq/euclidean-distance/eucl-2.png)

欧氏距离常常是「默认」使用的距离，例如在 K 近邻（分类）或 K 均值（聚类）中，用来寻找某个样本点的「k 个最近点」。另一个突出的例子是层次聚类、凝聚聚类（complete linkage 和 single linkage），此时你需要计算簇与簇之间的距离。
