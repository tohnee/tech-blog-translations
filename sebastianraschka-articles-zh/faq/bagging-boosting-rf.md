---
title: "随机森林与装袋、提升的对比"
title_en: "Random Forests vs. Bagging and Boosting"
source: https://sebastianraschka.com/faq/docs/bagging-boosting-rf.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 随机森林与装袋、提升的对比

> 原文：[Random Forests vs. Bagging and Boosting](https://sebastianraschka.com/faq/docs/bagging-boosting-rf.html) · Sebastian Raschka's FAQ

假设我们在三种方法中都使用决策树算法作为基分类器：提升（boosting）、装袋（bagging），以及（显然的 ;)）随机森林。

我们为什么以及何时想要使用这些方法？给定数量固定的训练样本，如果增加特征数量，我们的模型就会越来越多地受到「维数灾难」的困扰。单棵未经剪枝的决策树面临的挑战在于，其假设往往对底层训练数据而言过于复杂——决策树很容易过拟合。

**tl;dr：装袋和随机森林属于「装袋」类算法，目标是降低那些对训练数据过拟合的模型的复杂度。相反，提升是一种提高那些受高偏差困扰（即对训练数据欠拟合）的模型复杂度的方法。**

## 装袋（Bagging）

现在，我们来看看可能「最简单」的情形——装袋。在这里，我们从训练集的自助（bootstrap）样本中训练若干棵决策树（一个集成）。自助采样是指从训练集中有放回地抽取随机样本。例如，如果训练集由 7 个训练样本组成，那么我们的自助样本（这里 n=7）可能如下所示，其中 C1、C2、……、Cm 象征各个决策树分类器：

![](https://sebastianraschka.com/images/faq/bagging-boosting-rf/bagging.png)

在训练完这 m 棵决策树之后，我们可以通过多数规则用它们对新数据进行分类。例如，让每棵决策树各给出一个决定，然后预测获得较多票数的类别标签。这样通常会得到一个复杂度更低的决策边界，而且装袋分类器的方差（过拟合程度）会比单棵决策树更低。下图比较了单棵决策树（左）与装袋分类器（右）在 Wine 数据集两个变量（Alcohol 和 Hue）上的表现。

![](https://sebastianraschka.com/images/faq/bagging-boosting-rf/bagging-regions.png)

## 提升（Boosting）

与装袋相反，提升使用非常简单的分类器作为基分类器，即所谓的「弱学习器」（weak learner）。可以把这些弱学习器想象成「决策树桩」（decision tree stump）——只有 1 条分裂规则的决策树。下面我们以最著名的提升算法 AdaBoost 为例。这里，我们从一棵决策树桩（1）开始，并「聚焦」于它分错的样本。下一轮，我们训练另一棵决策树桩来尝试把这些样本分对（2）；实现方式是给这些训练样本赋予更大的权重。同样，第 2 个分类器大概率又会分错另一些样本，于是我们再次重新调整权重……

![](https://sebastianraschka.com/images/faq/bagging-boosting-rf/boosting.png)

简而言之，我们可以把 AdaBoost 概括为从错误中进行的「自适应」或「增量式」学习。最终，我们得到的模型会比单棵决策树具有更低的偏差（因此不太可能欠拟合训练数据）。

![](https://sebastianraschka.com/images/faq/bagging-boosting-rf/boosting-regions.png)

## 随机森林

随机森林算法实际上是一种装袋算法：同样地，我们从训练集中抽取随机自助样本。但除了自助样本之外，我们还会为训练每棵树而随机抽取特征子集；而在装袋中，每棵树都会拿到完整的特征集合。由于这种随机特征选择，与常规装袋相比，各树之间更加相互独立，这通常会带来更好的预测性能（得益于更好的偏差-方差权衡）。而且我认为它也比装袋更快，因为每棵树只从特征的一个子集中学习。
