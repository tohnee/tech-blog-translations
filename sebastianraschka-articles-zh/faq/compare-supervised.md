---
title: "如何在效率和准确率上比较监督学习算法？"
title_en: "How do you compare supervised algorithms efficiency and accuracy-wise?"
source: https://sebastianraschka.com/faq/docs/compare-supervised.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 如何在效率和准确率上比较监督学习算法？

> 原文：[How do you compare supervised algorithms efficiency and accuracy-wise?](https://sebastianraschka.com/faq/docs/compare-supervised.html) · Sebastian Raschka's FAQ

对监督学习算法做泛泛的比较并非易事；在比较预测性能时有很多事情需要考虑：

- 进行公平的超参数调优（例如，对所有算法使用相同的预算——即考虑的超参数取值数量相同）
- 考察不同的、多样的数据集
- 使用不同的性能指标

一个相对系统的监督学习算法比较研究的很好例子，是 UPenn Epistasis Lab 的 PMLB 基准测试研究：

> Olson, R. S., La Cava, W., Orzechowski, P., Urbanowicz, R. J., & Moore, J. H. (2017). [PMLB: a large benchmark suite for machine learning evaluation and comparison.](https://biodatamining.biomedcentral.com/articles/10.1186/s13040-017-0154-4) BioData mining, 10(1), 1-13.

![](https://sebastianraschka.com/images/faq/compare-supervised/pmlb1.png)

比较计算效率可以从理论上进行，也可以从实验上进行。我所说的理论比较指的是 Big-O 分析：

![](https://sebastianraschka.com/images/faq/compare-supervised/big-o-1.png)

例如，k 近邻算法在其朴素实现下

![](https://sebastianraschka.com/images/faq/compare-supervised/big-o-knn-1.png)

在预测阶段的运行时复杂度为 O(k × n)（其中 N 为训练集大小）。使用优先队列数据结构可以将其改进到 O(k log(n))。另一方面，（多项）逻辑回归的运行时间为 O((w+1) × c)，其中 w 是权重数量（常数），c 是类别数（如果是常规的二分类逻辑回归，则 c=1）。基于这一分析可以看到，作为训练样本数的函数，在预测标签这件事上逻辑回归应当比 KNN 更高效（假设训练集很大——这在机器学习中很常见）。如果数据集很小，KNN 可能也够用。

当然，你也可以在不同的数据集上以计算/实验的方式做这些比较（此时要确保选择的数据集在特征数、训练样本数、测试样本数和类别数上各不相同）。
