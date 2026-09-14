---
title: "逻辑回归 vs. 神经网络"
title_en: "Logistic Regression vs. Neural Networks"
source: https://sebastianraschka.com/faq/docs/logisticregr-neuralnet.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 逻辑回归 vs. 神经网络

逻辑回归模型的「经典」应用是二分类。不过，我们也可以用逻辑回归的各种「变体」来解决多分类问题，例如通过 One-vs-All（一对其余）或 One-vs-One（一对一）方法，以及相关的 softmax 回归 / 多项逻辑回归（multinomial logistic regression）。
尽管逻辑回归存在核化（kernelized）变体，但标准的「模型」是一个线性分类器。因此，当我们处理的数据集中各类别或多或少「线性可分」时，逻辑回归是很有用的。对于「相对」很小的数据集，我建议把判别式的逻辑回归模型与相关的朴素贝叶斯分类器（一种生成式模型）或 SVM 做性能比较，后两者可能对噪声和离群点不那么敏感。即便如此，逻辑回归仍然是简单分类任务中一个出色且稳健的模型；今年的「三月疯狂」（March Madness）预测大赛就曾被两位教授用一个逻辑回归模型拿下

> Lopez 和 Matthews 两位教授也没有使用数据科学圈里任何时髦的方法：没有深度学习，没有层次聚类，没有压缩感知；用的只是一个叫做逻辑回归的老好模型，它能把一个数字（比如分差）变成「A 队将击败 B 队」的估计概率。
> （[The Math of March Madness](http://www.nytimes.com/2015/03/22/opinion/sunday/making-march-madness-easy.html?_r=0)）

神经网络与逻辑回归有一定关联。基本上，我们可以把逻辑回归看作一个单层神经网络。

![](https://sebastianraschka.com/images/faq/logisticregr-neuralnet/schematic.png)

事实上，在神经网络的隐藏层中使用逻辑 sigmoid 函数作为激活函数是非常常见的做法——就像上面的示意图那样，只不过不带阈值函数。

![](https://sebastianraschka.com/images/faq/logisticregr-neuralnet/sigmoid.png)

如果是二分类任务，在输出层使用阈值函数是没有问题的（这种情况下，输出层只会有一个 sigmoid 单元）。而在多分类的情形下，我们可以使用 One-vs-All 方法的推广形式；也就是说，通过独热（one-hot）编码来编码目标类别标签。

![](https://sebastianraschka.com/images/faq/logisticregr-neuralnet/mlp.png)

例如，我们可以把熟悉的 Iris 数据集中的三个类别标签（0=Setosa（山鸢尾），1=Versicolor（变色鸢尾），2=Virginica（维吉尼亚鸢尾））编码如下：

![](https://sebastianraschka.com/images/faq/logisticregr-neuralnet/onehot.png)

然后，在学得模型之后的预测步骤中，我们只需返回「argmax」，即输出向量中数值最大的那个索引作为类别标签。如果我们只关心类别标签预测，这样做完全没问题。而如果我们想要「有意义的」类别概率，也就是加起来等于 1 的类别概率，我们可以使用 softmax 函数（又名「多项逻辑回归」）。在 softmax 中，某个净输入为 *z* 的样本属于第 i 个类别的概率，可以通过分母中的一个归一化项来计算，该归一化项是所有 *M* 个线性函数的和：

![](https://sebastianraschka.com/images/faq/logisticregr-neuralnet/softmax.png)

虽然我前面提到神经网络（具体来说是多层感知机）可以使用逻辑激活函数，但双曲正切（tanh）在实践中往往效果更好，因为它在隐藏层中的输出不局限于只有正值。

![](https://sebastianraschka.com/images/faq/logisticregr-neuralnet/log-tanh.png)

好了，回到逻辑 sigmoid 上来。逻辑回归的一个好性质是，逻辑代价函数（或最大熵函数）是凸的，因此我们保证能找到全局代价最小值。但是，一旦我们把逻辑激活函数堆叠成一个多层神经网络，就会失去这种凸性。只看单个权重/模型系数的话，我们可以把多层感知机中的代价函数想象成一片崎岖的地形，上面有多个可能困住优化算法的局部极小值：

![](https://sebastianraschka.com/images/faq/logisticregr-neuralnet/unconvex.png)

不过在实践中，反向传播在 1 到 2 层的神经网络上效果相当不错（还有一些深度学习算法，比如自编码器，可以帮助处理更深的架构）。即使你可能收敛到一个局部极小值，你也往往依然能得到一个强大的预测模型。
所以，总结一下：我建议先用简单的模型（例如逻辑回归）来处理分类问题。在某些情况下，这可能已经足够好地解决你的问题了。但如果你对它的性能不满意，而且你有足够的训练数据，我会尝试训练一个计算开销更高的神经网络，它的优势在于能够学习更复杂的非线性函数。
