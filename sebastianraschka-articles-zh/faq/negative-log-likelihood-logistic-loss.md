---
title: "负对数似然与逻辑损失"
title_en: "Negative Log-Likelihood and Logistic Loss"
source: https://sebastianraschka.com/faq/docs/negative-log-likelihood-logistic-loss.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 负对数似然与逻辑损失

> 原文：[Negative Log-Likelihood and Logistic Loss](https://sebastianraschka.com/faq/docs/negative-log-likelihood-logistic-loss.html) · Sebastian Raschka's FAQ

## 负对数似然

FAQ 条目[似然与概率有什么区别？](https://sebastianraschka.com/faq/docs/probability-vs-likelihood.html)曾在分布的语境下解释过概率与似然。而在机器学习的语境下，我们通常关心的是对预测模型进行参数化（也就是训练或拟合）。更具体地说，当我们使用逻辑回归或神经网络之类的模型时，我们想找到能使似然最大化的权重参数值。

我们用记号 \(\mathbf{x}^{(i)}\) 表示数据集中的第 \(i\) 个训练样本，其中 \(i \in \{1, ..., n\}\)。然后我们把似然定义如下：\(\mathcal{L}(\mathbf{w}\vert x^{(1)}, ..., x^{(n)})\)。由于似然与概率密度之间的关系，我们有

\[\mathcal{L}(\mathbf{w}\vert x^{(1)}, ..., x^{(n)}) = \mathcal{p}(x^{(1)}, ..., x^{(n)}\vert \mathbf{w}) = \prod\_{i=1}^{n} \mathcal{p}(x^{(i)}\vert \mathbf{w}).\]

注意，我们假设各样本相互独立，因此上面用到了如下条件独立假设：\(\mathcal{p}(x^{(1)}, x^{(2)}\vert \mathbf{w}) = \mathcal{p}(x^{(1)}\vert \mathbf{w}) \cdot \mathcal{p}(x^{(2)}\vert \mathbf{w})\)。

所以，训练一个预测模型时，我们的任务就是找到使似然 \(\mathcal{L}(\mathbf{w}\vert x^{(1)}, ..., x^{(n)}) = \prod\_{i=1}^{n} \mathcal{p}(x^{(i)}\vert \mathbf{w})\) 最大化的权重值 \(\mathbf{w}\)。实现这一目标的一种方法是梯度下降。

由于连乘在数值上十分脆弱，我们通常会做一个对数变换，把乘积变成求和：\(\log ab = \log a + \log b\)，于是

\[\log \mathcal{L}(\mathbf{w}\vert x^{(1)}, ..., x^{(n)}) = \sum\_{i=1}^{n} \log \mathcal{p}(x^{(i)}\vert \mathbf{w}).\]

注意，由于 log 函数是单调递增函数，使似然最大化的权重同样会使对数似然最大化。

现在我们得到了一个优化问题：希望通过改变模型权重来最大化对数似然。实现它的一种简单技术是随机梯度上升。不过，由于大多数深度学习框架实现的是随机梯度*下降*（descent），我们把对数似然取负，从而把这个最大化问题变成最小化问题：

\[- \log \mathcal{L}(\mathbf{w}\vert x^{(1)}, ..., x^{(n)}) = - \sum\_{i=1}^{n} \log \mathcal{p}(x^{(i)}\vert \mathbf{w}).\]

## 逻辑回归损失

那么，这一切与监督学习和分类有什么关系？我们在逻辑回归或深度神经网络分类器中优化的函数本质上就是似然：
\(\mathcal{L}(\mathbf{w}, b \mid \mathbf{x})=\prod\_{i=1}^{n} p\left(y^{(i)} \mid \mathbf{x}^{(i)} ; \mathbf{w}, b\right),\)
其中

- \(\mathbf{w}\) 是模型权重，
- \(b\) 是偏置单元，
- \(\mathbf{x}\) 是输入特征，
- \(y\) 是类别标签。

对于一个二元逻辑回归分类器，我们有
\(p\left(y^{(i)} \mid \mathbf{x}^{(i)} ; \mathbf{w}, b\right)=\prod\_{i=1}^{n}\left(\sigma\left(z^{(i)}\right)\right)^{y^{(i)}}\left(1-\sigma\left(z^{(i)}\right)\right)^{1-y^{(i)}}\)
这样我们就可以按下面的方式计算似然：
\(\mathcal{L}(\mathbf{w}, b \mid \mathbf{x})=\prod\_{i=1}^{n}\left(\sigma\left(z^{(i)}\right)\right)^{y^{(i)}}\left(1-\sigma\left(z^{(i)}\right)\right)^{1-y^{(i)}}.\)
（这篇文章已经越写越长，所以我略去推导过程；更多细节可参见[我的书](https://www.amazon.com/Machine-Learning-PyTorch-Scikit-Learn-scikit-learn-ebook-dp-B09NW48MR1/dp/B09NW48MR1/) 😊。）

这里，

- \(\sigma\) 是 logistic sigmoid 函数，\(\sigma(z)=\frac{1}{1+e^{-z}}\)，
- \(z\) 是输入的加权和，\(z=\mathbf{w}^{T} \mathbf{x}+b\)。

同样地，为了在基于梯度下降的优化中计算导数时的数值稳定性，我们通过取对数把乘积变成求和（和的导数等于各项导数之和）：
\(l(\mathbf{w}, b \mid x)=\log \mathcal{L}(\mathbf{w}, b \mid x)=\sum\_{i=1}\left[y^{(i)} \log \left(\sigma\left(z^{(i)}\right)\right)+\left(1-y^{(i)}\right) \log \left(1-\sigma\left(z^{(i)}\right)\right)\right]\)
最后，我们把上面的对数似然乘以 \((-1)\)，把这个最大化问题转化为适用于随机梯度下降的最小化问题：
\(L(\mathbf{w}, b \mid z)=\frac{1}{n} \sum\_{i=1}^{n}\left[-y^{(i)} \log \left(\sigma\left(z^{(i)}\right)\right)-\left(1-y^{(i)}\right) \log \left(1-\sigma\left(z^{(i)}\right)\right)\right]\)

负对数似然 \(L(\mathbf{w}, b \mid z)\) 就是我们通常所说的*逻辑损失*（logistic loss）。注意，同样的概念也可以推广到深度神经网络分类器。唯一的区别在于：\(z\) 不再作为模型输入的加权和 \(z=\mathbf{w}^{T} \mathbf{x}+b\) 来计算，而是作为最后一层输入的加权和来计算，如下图所示：

![](https://sebastianraschka.com/images/faq/negative-log-likelihood-logistic-loss/likelihood-loss-nn.png)

（注意，上图中上标索引的是层，而不是训练样本。）
