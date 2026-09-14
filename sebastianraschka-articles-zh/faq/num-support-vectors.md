---
title: "SVM 支持向量的数量说明了什么"
title_en: "What the Number of SVM Support Vectors Tells Us"
source: https://sebastianraschka.com/faq/docs/num-support-vectors.html
crawled: 2026-09-06
translated: 2026-09-14
---

# SVM 支持向量的数量说明了什么

> 原文：[What the Number of SVM Support Vectors Tells Us](https://sebastianraschka.com/faq/docs/num-support-vectors.html) · Sebastian Raschka's FAQ

遗憾的是，和机器学习应用中的许多问题一样，这真的取决于数据集。如果我们训练一个 RBF 核 SVM，最终得到的支持向量通常会比线性模型多。如果我们的数据线性可分，后者（线性模型）可能更好；如果不是线性可分，前者（RBF 核 SVM）可能更好。

此外，我们还必须把计算效率和泛化性能区分开来。如果支持向量的数量增加，我们的分类会变得更「昂贵」，尤其是在核 SVM 中，我们必须重新计算每个新样本与整个训练集之间的距离。

我想说，解决预测性能问题的最佳方式就是评估模型、绘制学习曲线、做 k 折和/或交叉验证，看看在我们的给定数据集上什么效果最好。
