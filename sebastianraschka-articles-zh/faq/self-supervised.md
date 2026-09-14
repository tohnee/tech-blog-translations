---
title: "什么是自监督学习？它什么时候有用？"
title_en: "What is self-supervised learning and when is it useful?"
source: https://sebastianraschka.com/faq/docs/self-supervised.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 什么是自监督学习？它什么时候有用？

自监督学习（self-supervised learning）是一种预训练流程，它让神经网络能够以监督学习的方式利用大规模无标签数据集。

自监督学习与迁移学习相关。假设我们想训练一个图像分类器来识别鸟类物种。在迁移学习中，我们会先在 ImageNet 上预训练一个卷积神经网络。在通用的 ImageNet 数据集上完成预训练之后，我们拿这个预训练模型在更小、更特定的目标数据集上训练，该数据集包含我们感兴趣的鸟类物种。

![](https://sebastianraschka.com/images/faq/self-supervised/self-supervised-transfer.png)

自监督学习是迁移学习的一种替代做法：我们不是在有标签数据上预训练模型，而是在*无标签*数据上预训练。我们考虑一个没有标签信息的数据集，然后设法从数据集自身的结构中获得标签，为神经网络构造一个预测任务。这些自监督训练任务也被称为*前置任务（pretext task）*。

![](https://sebastianraschka.com/images/faq/self-supervised/self-supervised-1.png)

这类自监督学习任务可以是自然语言处理场景中的「缺失词」预测。例如，给定句子 "It is beautiful and sunny outside"，我们可以遮住单词 "sunny"，把输入 "It is beautiful and [MASK] outside" 送入网络，让网络预测 "[MASK]" 位置上缺失的词。类似地，在计算机视觉场景中，我们可以移除图像块，让神经网络补全空缺。注意，这些只是自监督学习任务的两个例子，还有许多更多的自监督学习方法与范式。

总之，我们可以把前置任务上的自监督学习理解为表示学习。之后我们可以拿预训练好的模型，在目标任务（也称为*下游*任务）上进行微调。

**自监督学习什么时候有用？**

大型神经网络架构需要大量有标签数据才能表现良好并具备泛化能力。然而，在许多问题领域，我们并没有大规模的有标签数据集。借助自监督学习，我们可以利用无标签数据。因此，当我们使用大型神经网络、而有标签训练数据又有限时，自监督学习很可能有用。

作为大语言模型和视觉 transformer 基础的基于 transformer 的架构，众所周知需要自监督学习进行预训练才能有良好表现。

对于小型神经网络模型，例如只有两三层的多层感知机，自监督学习通常被认为既无用也不必要。不过，针对多层感知机和表格数据集的自监督学习例子确实存在。

自监督学习不适用的另一些场景是使用非参数模型的传统机器学习，例如基于树结构的随机森林或梯度提升。传统树方法没有固定的参数结构（与权重矩阵等形成对比）。因此，传统树方法不具备迁移学习能力，与自监督学习不兼容。

---

**这是我的书 [Machine Learning Q and AI](https://leanpub.com/machine-learning-q-and-ai/) 的缩略回答与摘录，书中包含更详尽的版本和更多插图。**
