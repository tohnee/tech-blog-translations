---
title: "如何为交叉验证选择折数"
title_en: "Choosing the Number of Folds for Cross-Validation"
source: https://sebastianraschka.com/faq/docs/number-of-kfolds.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 如何为交叉验证选择折数

> 原文：[Choosing the Number of Folds for Cross-Validation](https://sebastianraschka.com/faq/docs/number-of-kfolds.html) · Sebastian Raschka's FAQ

假设我们讨论的是用于分类算法超参数调优的 k 折交叉验证，而所谓「更好」，指的是更善于估计泛化性能。在这种情况下，我的回答是否定的，否则我们就永远用 LOOCV（留一法交叉验证）而不是 k 折交叉验证了。（一个有用的参考文献：Shao, Jun. [Linear model selection by cross-validation.](http://www.sciencedirect.com/science/article/pii/S0378375803003719) Journal of the American statistical Association 88.422 (1993): 486-494.）

在实践中，我会说 k 折交叉验证中最常用（默认）的值是 k=10，这通常是一个合适的选择。但如果我们使用的是（较）小的训练集，我会增加折数，以便在每次迭代中用上更多训练数据；这会降低估计泛化误差的偏差。另一方面，它也会增加运行时间以及估计的方差。估计方差增大的原因在于，各训练集之间的重迭程度会随 *k* 的增大而增大——不过请注意，测试集是永远不会重迭的。

至于计算效率——例如，想象在（较）大的数据集上训练深度神经网络并做超参数调优——我会仔细考虑 *k* 的大小。如果我们的数据集很大，我会建议为 *k* 选择较小的值。但归根结底，这都是偏差、方差与计算效率之间的权衡；而且对于最终估计，我们反正还有独立的测试集。
