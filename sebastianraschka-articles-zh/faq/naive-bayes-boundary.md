---
title: "朴素贝叶斯的决策边界是什么？"
title_en: "What is the decision boundary for Naive Bayes?"
source: https://sebastianraschka.com/faq/docs/naive-bayes-boundary.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 朴素贝叶斯的决策边界是什么？

决策边界取决于朴素贝叶斯（Naive Bayes）的具体变体。高斯朴素贝叶斯（Gaussian Naive Bayes）在两个类别之间通常产生一条二次（曲线）边界。多项式朴素贝叶斯（Multinomial Naive Bayes）在输入计数特征上产生的是线性边界。

## 高斯边界为什么会弯曲

高斯朴素贝叶斯为每个类别内的每个特征拟合一个均值和一个方差。它的对数概率包含与这些均值之间的平方距离。因此，比较两个类别的得分会得到一个关于特征的二次方程。如果每个特征在两个类别中的方差都相同，二次项就会相互抵消，边界随之变成线性。

当类别多于两个时，预测区域由这些两两比较共同构成。而多项式朴素贝叶斯则是把特征计数乘以类别专属的对数概率再求和，并加上一个对数先验。这些得分关于计数是线性的。[scikit-learn 朴素贝叶斯指南](https://scikit-learn.org/stable/modules/naive_bayes.html)给出了这两种变体背后的概率模型。

## Wine（葡萄酒）数据集示例

在这张 UCI Wine 数据集的双特征视图里，曲线划分出了分配给两个类别的区域。由于拟合出的分布相互重叠，有些点落在了边界的另一侧。

![用 alcohol 和 proline 两个特征对葡萄酒样本绘制的高斯朴素贝叶斯决策区域](https://sebastianraschka.com/images/faq/naive-bayes-boundary/gaussian_1.png)

## XOR 示例

XOR 这个例子展示了它的一个局限。类别取决于特征的组合，而朴素贝叶斯假设特征在给定类别时条件独立。仅有一条弯曲的边界并不足以表示这种关系。在这个样本中，高斯朴素贝叶斯拟合出了一个近似椭圆形的区域，因此错分了许多点。

![高斯朴素贝叶斯对 XOR 数据拟合出一个近似椭圆形的区域，错失了交替的类别模式](https://sebastianraschka.com/images/faq/naive-bayes-boundary/gaussian_2.png)
