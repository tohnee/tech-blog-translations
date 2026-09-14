---
title: "用数据减少过拟合"
title_en: "Reducing Overfitting with Data"
source: https://sebastianraschka.com/faq/docs/overfitting-data.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 用数据减少过拟合

> 原文：[Reducing Overfitting with Data](https://sebastianraschka.com/faq/docs/overfitting-data.html) · Sebastian Raschka's FAQ

**收集更多数据**

减少过拟合最好的方法之一就是收集更多（高质量的）数据。我们怎么知道更多的数据有利于把过拟合降到最低？我们可以绘制学习曲线来弄清楚。构造学习曲线时，我们在不同大小的训练集（10%、20% 等）上训练模型，并在同一个固定大小的验证集或测试集上评估训练好的模型。

**数据增强**

数据增强（data augmentation）指的是基于现有数据生成新的数据记录或特征。它使我们无需额外收集数据就能扩充数据集。

数据增强让我们能够创建原始输入数据的不同版本，从而提升模型的泛化性能。为什么？增强过的数据可以帮助模型更好地泛化，因为它让模型更难通过训练样本或特征（对图像数据而言，即特定像素位置上的精确像素值）记住虚假信息。

数据增强对图像数据和文本数据来说通常是标准做法，但也存在针对表格数据的数据增强方法 [ref1, ref2]。

- [ref1] GReaT 方法使用一个自回归生成式大语言模型来生成合成表格数据。参考文献：Borisov, Seßler, Leemann, Pawelczyk, Kasneci, (2022). *Language Models Are Realistic Tabular Data Generators.* <https://arxiv.org/abs/2210.06280>.
- [ref2] TabDDPM 是一种使用扩散模型生成合成表格数据的方法。Kotelnikov, Baranchuk, Rubachev, Babenko (2022). *TabDDPM: Modelling Tabular Data with Diffusion Models.* <https://arxiv.org/abs/2209.15421>.

**预训练**

自监督学习让我们能够利用大型无标注数据集来预训练神经网络。这有助于在较小的目标数据集上减少过拟合。

作为自监督学习的替代方案，在大型有标注数据集上做传统迁移学习也是一种选择。如果有标注数据集与目标领域密切相关，迁移学习的效果最好。例如，如果我们要训练一个分类鸟类物种的模型，可以先在一个大型通用动物分类数据集上预训练网络。不过，如果没有这样的大型动物分类数据集，我们也可以在相对宽泛的 ImageNet 数据集上预训练模型。

数据集可能极小而不适合监督学习，例如每个类别只有寥寥几个带标注的样本。如果我们的分类器需要在无法收集更多标注数据的场景中运行，还可以考虑少样本学习（few-shot learning）。

**其他方法**

上面列出了通过使用和修改数据集来减少过拟合的主要方法。不过这份清单并非穷尽，其他常用技术还包括

- 特征工程与归一化；
- 引入对抗样本以及标签或特征噪声；
- 标签平滑；
- 更小的批量大小；
- Mix-Up、Cut-Out、Cut-Mix 等数据增强技术。

---

**这是我的书 [Machine Learning Q and AI](https://leanpub.com/machine-learning-q-and-ai/) 中一个压缩后的答案与节选，书中有更详尽的版本并配有更多插图。**
