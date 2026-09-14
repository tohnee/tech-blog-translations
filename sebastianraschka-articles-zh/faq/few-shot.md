---
title: "少样本学习 vs. 传统监督学习"
title_en: "Few-Shot Learning vs. Conventional Supervised Learning"
source: https://sebastianraschka.com/faq/docs/few-shot.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 少样本学习 vs. 传统监督学习

> 原文：[Few-Shot Learning vs. Conventional Supervised Learning](https://sebastianraschka.com/faq/docs/few-shot.html) · Sebastian Raschka's FAQ

少样本学习（few-shot learning）是监督学习的一个分支，适用于样本数与类别数之比极小的训练集。在常规监督学习中，我们通过迭代遍历训练集来训练模型，模型始终看到的是一组固定的类别。而在少样本学习中，我们操作的是一个支撑集（support set），从中构造多个训练任务，组成一个个训练回合（episode），每个训练任务由不同的类别构成。

在监督学习中，我们在训练数据集上拟合模型，并在测试数据集上评估。通常，训练集中每个类别包含相对较多的样本。例如，在监督学习的语境下，Iris 数据集这样每类只有 50 个样本的数据集就已经算微型数据集了；对于深度学习模型而言，即便是 MNIST 这种每类有 5k 个训练样本的数据集，也被认为非常小。

在少样本学习中，每个类别的样本数量要少得多。我们通常使用 *N*-way *K*-shot（N 类 K 样本）这样的术语，其中 *N* 代表类别数，K 代表每类的样本数。最常见的取值是 *K=1* 或 *K=5*。例如，在一个 5-way 1-shot 问题中，我们有 5 个类别，每类只有 1 个样本。

![](https://sebastianraschka.com/images/faq/few-shot/few-shot-1.png)

与其说少样本学习是把模型拟合到训练数据集上，不如把它理解为「学习如何学习」（learning to learn）。与监督学习不同，我们没有训练数据集，而是有一个所谓的支撑集。我们从支撑集中采样出训练任务，这些任务模拟预测时的实际使用场景。例如，对于 3-way 1-shot 学习，一个训练任务由 3 个类别、每类 1 个样本组成。每个训练任务还附带一张待分类的查询图像（query image）。模型在支撑集中的若干训练任务上进行训练；这就称为一个回合（episode）。

然后在测试阶段，模型会接到一个新任务，其中的类别与训练时见过的类别不同。同样，任务的目标是对查询图像进行分类。测试任务与训练任务类似，唯一不同的是测试时的类别与训练时遇到的所有类别都不重叠。

![](https://sebastianraschka.com/images/faq/few-shot/few-shot-2.png)

---

**这是一个缩写版的回答，摘自我的书 [Machine Learning Q and AI](https://leanpub.com/machine-learning-q-and-ai/)，书中有更详尽的版本和更多插图。**
