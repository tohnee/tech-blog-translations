---
title: "朴素贝叶斯中混合使用二值与连续特征"
title_en: "Mixing Binary and Continuous Features in Naive Bayes"
source: https://sebastianraschka.com/faq/docs/naive-bayes-vartypes.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 朴素贝叶斯中混合使用二值与连续特征

> 原文：[Mixing Binary and Continuous Features in Naive Bayes](https://sebastianraschka.com/faq/docs/naive-bayes-vartypes.html) · Sebastian Raschka's FAQ

是的，这完全可行。

让我们先简要回顾朴素贝叶斯背后的概念：我们的目标函数是在给定训练数据的条件下最大化后验概率：

![](https://sebastianraschka.com/images/faq/naive-bayes-vartypes/bayes-theorem-in-words.png)

![](https://sebastianraschka.com/images/faq/naive-bayes-vartypes/bayes-theorem.png)

令

![](https://sebastianraschka.com/images/faq/naive-bayes-vartypes/bayes-theorem-notation.png)

基于该目标函数，我们可以把决策规则表述为：

![](https://sebastianraschka.com/images/faq/naive-bayes-vartypes/naive-bayes-decision.png)

在本文问题的语境下，我们先不讨论先验；它们通常通过极大似然估计（MLE）来计算，例如类频率 Nωj/N（ωj 类中的样本数除以训练集中全部样本数）。

关于证据项（evidence）简单说明一下：我写出它是为了完整性，但我们可以直接把它从决策函数中约去，因为它对所有类别而言都是一个常数项。接下来，类条件概率——我们称之为似然（likelihood）——是各个特征 *d* 各自似然的乘积：

![](https://sebastianraschka.com/images/faq/naive-bayes-vartypes/naive-bayes-likelihood.png)

这里我们做出的是「朴素」的条件独立假设，即各特征相互独立——朴素贝叶斯正是由此得名。我们基本上是在说：「观察到这组特征组合的概率，等于分别观察到每个特征的概率的乘积。」

我们做出的另一个假设是，*p(xi = b | ωj )* 服从某个特定的分布——这也是朴素贝叶斯被称为「生成式模型」的原因。回到最初的问题，让我们考虑用于二值特征的多变量伯努利模型（multi-variate Bernoulli model），以及用于连续特征的高斯朴素贝叶斯模型。

## （多变量）伯努利模型

我们用伯努利分布来计算二值变量的似然。例如，我们可以通过 MLE 把 P(xk=1 | ωj) 估计为它在训练集中出现的频率：

θ = P̂(xk=1 | ωj) = Nxk, ωj / N ωj  
它读作「ωj 类中满足 xk=1 的训练样本数（Nxk, ωj）除以 ωj 类的全部训练样本数（N ωj）」。在文本分类的语境下，这基本上就是 ωj 类中包含某个特定词的文档数，除以 ωj 类中的全部文档数。
现在，我们可以把给定类别 ωj 时二值特征向量 **x** 的似然计算为

![](https://sebastianraschka.com/images/faq/naive-bayes-vartypes/likelihood-bernoulli.png)

## 高斯模型

对于连续尺度上的变量，我们通常使用高斯朴素贝叶斯模型——即假设变量服从正态分布。

![](https://sebastianraschka.com/images/faq/naive-bayes-vartypes/gaussian-likelihood.png)

在上面的公式中，我们需要估计两个参数：与类别 ωj 相关联的样本均值 μ，以及与类别 ωj 相关联的方差 σ2。这一步很直接，细节在此略过。把估计出的参数代入公式之后，我们就可以（与上面的伯努利模型类似）计算连续特征向量的似然：

![](https://sebastianraschka.com/images/faq/naive-bayes-vartypes/naive-bayes-likelihood_shorter.png)

由于朴素贝叶斯带有条件独立假设，可以看到混合使用变量并不成问题。我们可以用伯努利贝叶斯计算二值变量的似然，用高斯模型计算连续变量的似然。要计算某个样本的类条件概率，只需把来自不同特征子集的似然相乘即可：

![](https://sebastianraschka.com/images/faq/naive-bayes-vartypes/combined.png)

（同样的概念也适用于多项式朴素贝叶斯等其他模型。）
