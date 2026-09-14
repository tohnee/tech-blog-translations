---
title: "半监督学习的优势与局限"
title_en: "Advantages and Limits of Semi-Supervised Learning"
source: https://sebastianraschka.com/faq/docs/semi-vs-supervised.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 半监督学习的优势与局限

显然，当我们用监督学习构建（通常是预测性的）模型时，我们使用的是有标签数据集。而无监督学习的目标往往具有探索性质（聚类、压缩），并且使用的是无标签数据。

在半监督学习（semi-supervised learning）中，我们试图用「有标签数据加上无标签数据增广」的方式来解决一个监督学习问题；无标签或只有部分标签的样本数量通常多于有标签样本，因为前者成本更低、更容易获得。所以，我们的目标是克服监督学习的问题之一——有标签数据不够多。通过加入廉价而丰富的无标签数据，我们希望构建出比单用监督学习更好的模型。

虽然半监督学习听起来是一种强大的方法，但我们必须谨慎。半监督学习并不总是我们要找的「那把敲钉子的锤子」——有时效果很好，有时则不然。这里有一篇很不错的论文：

Singh, Aarti, Robert Nowak, and Xiaojin Zhu. "[Unlabeled data: Now it helps, now it doesn't.](http://www.cs.cmu.edu/~aarti/pubs/NIPS08_ASingh.pdf)" Advances in Neural Information Processing Systems. 2009.

此外，我们还要记住：使用半监督算法时需要做出某些假设（流形假设、聚类假设或平滑性假设；更多细节参见：[Semi-supervised learning](https://en.wikipedia.org/wiki/Semi-supervised_learning#Assumptions_used_in_semi-supervised_learning)），并且必须确保这些假设没有被违背。
