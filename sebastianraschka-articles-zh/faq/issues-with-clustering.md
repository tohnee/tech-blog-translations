---
title: "聚类有哪些问题？"
title_en: "What are some of the issues with Clustering?"
source: https://sebastianraschka.com/faq/docs/issues-with-clustering.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 聚类有哪些问题？

我不一定把其中大多数称为「问题」，更愿意称之为「挑战」。以 *k*-均值（*k*-means）为例：

- 不同的随机初始化会让 *k*-均值产生不同的结果，这确实是个问题。不过我们可以用 *k*-means++ 作为替代方案；而且如果计算上可行，我们希望用不同的随机种子把算法运行多次，然后选择比如簇内误差平方和（SSE）最低的那一次结果
- 聚类的数量（通常）无法先验地得知（这基本上是无监督学习问题的固有特点），但有一些「性能」或评估指标可以帮助我们针对不同的 K 值推断出一个「令人满意」的分组；这也叫肘部法（elbow method）：
  ![](https://sebastianraschka.com/images/faq/issues-with-clustering/elbow.png)

这里看起来 k=3 是个不错的选择。来看看我用于训练 *k*-均值算法的那个配套二维数据集，看看我们的直觉是否同意：

![](https://sebastianraschka.com/images/faq/issues-with-clustering/clusters_unlabeled.png)

![](https://sebastianraschka.com/images/faq/issues-with-clustering/clusters_kmeans.png)

我得说 k=3 绝对是一个合理的选择。不过请注意，实际中的「肘部」通常不会像上图那样清晰。另外还要注意，实践中我们面对的通常是高维数据集，无法简单地画出来用肉眼复核。（不过我们可以使用无监督降维技术，比如主成分分析（PCA）。）事实上，如果我们本来就知道这 3 个簇分属三个不同的组，那这就成了一个分类任务。

除此之外，还有其他有用的评估指标，比如轮廓系数（silhouette coefficient），它能让我们大致了解簇的大小和形状。还是用同一个数据集，我给你看一张「好」的轮廓图（k=3）和一张不太好的（k=2）：

![](https://sebastianraschka.com/images/faq/issues-with-clustering/silhouette_good.png)

![](https://sebastianraschka.com/images/faq/issues-with-clustering/silhouette_bad.png)

我认为 *k*-均值最大的「短板」可能在于：我们假设各组数据呈球形或团状，而「真实世界」的数据很少如此。相比之下，我倒可以把选择「最优」*k* 看作只是又一次超参数优化过程——几乎每个监督学习算法也都需要做这件事。
