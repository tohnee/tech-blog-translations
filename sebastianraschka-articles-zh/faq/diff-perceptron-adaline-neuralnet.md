---
title: "感知机、ADALINE 与神经网络的比较"
title_en: "Perceptrons, Adaline, and Neural Networks Compared"
source: https://sebastianraschka.com/faq/docs/diff-perceptron-adaline-neuralnet.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 感知机、ADALINE 与神经网络的比较

> 原文：[Perceptrons, Adaline, and Neural Networks Compared](https://sebastianraschka.com/faq/docs/diff-perceptron-adaline-neuralnet.html) · Sebastian Raschka's FAQ

ADALINE 和感知机都是（单层）神经网络模型。
感知机是现存最古老、最简单的学习算法之一，而我认为 ADALINE 是对感知机的一种改进。

## ADALINE 与感知机的共同点

- 二者都是用于二分类的分类器
- 二者都有线性的决策边界
- 二者都可以迭代地、逐样本地学习（感知机天然如此，ADALINE 则通过随机梯度下降实现）
- 二者都使用阈值函数

在谈区别之前，先说说输入。这两个算法的第一步都是计算所谓的净输入 *z*，即特征变量 *x* 与模型权重 *w* 的线性组合。

![](https://sebastianraschka.com/images/faq/diff-perceptron-adaline-neuralnet/1.png)

然后，在感知机和 ADALINE 中，我们定义一个阈值函数来做预测。也就是说，如果 *z* 大于某个阈值 theta，我们就预测类别 1，否则预测 0：

![](https://sebastianraschka.com/images/faq/diff-perceptron-adaline-neuralnet/2.png)

![](https://sebastianraschka.com/images/faq/diff-perceptron-adaline-neuralnet/3.png)

## 感知机与 ADALINE 的区别

- 感知机使用类别标签来学习模型系数
- ADALINE 使用连续的预测值（来自净输入）来学习模型系数，这更「有威力」，因为它告诉我们对或错的程度「有多大」

因此，如下面所示，在感知机中我们直接用预测的类别标签来更新权重，而在 ADALINE 中我们使用连续的响应值：

![](https://sebastianraschka.com/images/faq/diff-perceptron-adaline-neuralnet/4.png)

（注意，我在 ADALINE 中插入「激活函数」只是为了便于说明；在这里，这个激活函数就是恒等函数）
只要我们对 ADALINE 使用随机梯度下降，这两种学习算法其实都可以概括为 4 个简单的步骤：

1. 将权重初始化为 0 或很小的随机数。
2. 对每个训练样本：
   1. 计算输出值。
   2. 更新权重。

我们把每次迭代中的权重更新写作：

![](https://sebastianraschka.com/images/faq/diff-perceptron-adaline-neuralnet/5.png)

其中

![](https://sebastianraschka.com/images/faq/diff-perceptron-adaline-neuralnet/6.png)

再强调一次，「输出」在 ADALINE 中是连续的净输入值，而在感知机中是预测的类别标签；eta 是学习率。
（如果你感兴趣：ADALINE 中的这个权重更新基本上就是沿着误差平方和代价梯度的方向迈出「反向的一步」。关于代价梯度的推导，我在[这里](https://web.archive.org/web/20170321045557/http://rasbt.github.io/mlxtend/user_guide/general_concepts/linear-gradient-derivative/)有一份更详细的讲解。

## 多层神经网络

虽然你没有具体问多层神经网络，但请允许我补充几句关于最古老、也最受欢迎的多层神经网络架构之一——多层感知机（Multi-Layer Perceptron，MLP）的话。在这个语境下，「感知机」这个说法有点不太恰当，因为它与 Rosenblatt 的感知机算法其实没有太大关系。

![](https://sebastianraschka.com/images/faq/diff-perceptron-adaline-neuralnet/7.png)

MLP 基本上可以被理解为分布在多层之中的多个人工神经元组成的网络。在这里，激活函数不再是线性的（如 ADALINE 中那样），我们使用非线性激活函数，比如 logistic sigmoid（即逻辑回归中用的那个）、双曲正切，或者分段线性的激活函数如修正线性单元（ReLU）。此外，我们常常在输出层使用 softmax 函数（logistic sigmoid 在多分类问题上的推广），并用一个阈值函数把（softmax 给出的）预测概率转换为类别标签。

那么，MLP 相对经典感知机和 ADALINE 的优势是什么？通过非线性激活函数把人工神经元连接成这样的网络，我们可以构造出复杂的非线性决策边界，从而解决各类别线性不可分的问题。

让我给你看一个例子 :)

![](https://sebastianraschka.com/images/faq/diff-perceptron-adaline-neuralnet/8.png)

如果你想复现这些图，下面是 Python 代码：

```python
from mlxtend.evaluate import plot_decision_regions
from mlxtend.classifier import Perceptron
from mlxtend.classifier import Adaline
from mlxtend.classifier import MultiLayerPerceptron
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
import matplotlib.gridspec as gridspec
import itertools

gs = gridspec.GridSpec(2, 2)xw
X, y = make_moons(n_samples=100, random_state=123)
fig = plt.figure(figsize=(10,8))

ppn = Perceptron(epochs=50, eta=0.05, random_seed=0)
ppn.fit(X, y)
ada = Adaline(epochs=50, eta=0.05, random_seed=0)
ada.fit(X, y)

mlp = MultiLayerPerceptron(n_output=len(np.unique(y)),
                           n_features=X.shape[1],
                           n_hidden=150,
                           l2=0.0,
                           l1=0.0,
                           epochs=500,
                           eta=0.01,
                           alpha=0.0,
                           decrease_const=0.0,
                           minibatches=1,
                           shuffle_init=False,
                           shuffle_epoch=False,
                           random_seed=0)

mlp = mlp.fit(X, y)

for clf, lab, grd in zip([ppn, ppn, mlp],
                         ['Perceptron', 'Adaline', 'MLP (logistic sigmoid)'],
                         itertools.product([0, 1], repeat=2)):

    clf.fit(X, y)
    ax = plt.subplot(gs[grd[0], grd[1]])
    fig = plot_decision_regions(X=X, y=y, clf=clf, legend=2)
    plt.title(lab)

plt.show()
```
