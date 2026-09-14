---
title: "什么时候应该用中位数而不是均值（平均数）？"
title_en: "When should one use median, as opposed to the mean or average?"
source: https://sebastianraschka.com/faq/docs/median-vs-mean.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 什么时候应该用中位数而不是均值（平均数）？

这实际上取决于数据的分布以及你想回答的问题。

考虑一个对称分布（这里我从标准正态分布中抽取了 10,000 个随机样本）：

![](https://sebastianraschka.com/images/faq/median-vs-mean/std-normal.png)

在这种情况下，中位数和均值会非常接近（mean≈0.00337，median≈0.01690）。事实上，如果你的数据样本是完全对称分布的，中位数和均值就会相同，例如 [1, 3, 5] 或 [1, 3, 3, 5]。

而如果数据是偏斜的，你往往更值得去计算中位数，因为它对离群点和极端值不那么敏感。我们来看一个经典例子——「薪水」。这里我绘制的是 [OpenData 的 FGCU 薪水数据集](https://web.archive.org/web/20150910074300/https://opendata.socrata.com/dataset/FGCU-salary-dataset/fjqw-ymup)：

![](https://sebastianraschka.com/images/faq/median-vs-mean/salary.png)

可以看到，均值和中位数之间存在显著差异。在这里，均值被那些相对较高但不常见的、超过 15,000 的薪水拉高了。

再说一次，这取决于你对数据提出的问题。不过，如果你问的「平均薪水是多少」其实是想问「一名员工的典型薪水是多少」，那么中位数会是比均值好得多的度量。
