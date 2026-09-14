---
title: "数据预处理与特征工程"
title_en: "Data Preprocessing vs. Feature Engineering"
source: https://sebastianraschka.com/faq/docs/dataprep-vs-dataengin.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 数据预处理与特征工程

> 原文：[Data Preprocessing vs. Feature Engineering](https://sebastianraschka.com/faq/docs/dataprep-vs-dataengin.html) · Sebastian Raschka's FAQ

我认为这两个任务领域之间的边界是比较模糊的。我把数据准备（data preparation）更多地看作一项技术性/计算性任务。例如，把数据转换成"正确"的格式、选择合适的数据结构/数据库等等。
然后是数据清洗（data cleaning），它也可以归入"准备/预处理"这一类。在这里，你可能需要考虑检测重复数据、如何处理异常值以及如何处理缺失数据。

在我看来，特征工程（feature engineering）则有些不同。我更把它看作一个"数据/特征创造"步骤，而不是数据"清洁消毒"步骤。特征工程可以包括各种方向的特征变换：变换到更高维的特征空间（例如多项式），变换到更低维的特征空间（如 PCA、LDA 等降维、哈希、聚类），或者保持维度不变而改变数据的分布（例如对数变换、标准化、最小-最大缩放等）。
