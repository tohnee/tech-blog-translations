---
title: "似然与概率有什么区别？"
title_en: "What is the difference between likelihood and probability?"
source: https://sebastianraschka.com/faq/docs/probability-vs-likelihood.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 似然与概率有什么区别？

## 似然（Likelihood）

我们先来定义*似然*这个术语。在日常对话中，*概率*和*似然*意思相同。但在统计学或机器学习语境中，它们是两个不同的概念。

使用*概率*这个词时，我们计算的是：从具有特定参数的给定分布中抽取到某个样本的可能性有多大。例如，考虑像正态分布这样的连续分布，我们把概率计算为数据 \(x\) 在给定取值范围内曲线下方的面积。具体做法是对概率密度函数在固定参数下积分：对正态分布而言，这些参数是均值和标准差。下图通过计算标准正态分布（均值 0、标准差 1）中抽取值介于 0 到 0.5 之间的样本 \(x\) 的概率来说明这一概念，即 \(Pr(0 < x < 0.5 \vert \mathbf{w}) =\int\_{0}^{0.5} p(x \vert \mathbf{w}) dx\)：

![](https://sebastianraschka.com/images/faq/probability-vs-likelihood/probability.png)

一般地，我们可以把概率密度定义为 \(p(\mathbf{x} \vert \mathbf{w})\)，其中 \(\mathbf{x}\) 是数据，\(\mathbf{w}\) 是分布或模型的参数。

---

**旁注**

正态分布的参数是 \(\mu\)（均值）和 \(\sigma\)（标准差）；不过在 \(\mathcal{L}(\mathbf{w} \vert \mathbf{x})\) 中，我用 \(\mathbf{w}\) 而不是 \(\mathcal{L}(\mu, \sigma \vert \mathbf{x})\)，以保持一般性。这也会让后文在机器学习语境中的记号更自然一些。就目前而言，在正态分布的语境下你可以这样理解：\(\mathbf{w} = (\mu, \sigma)\)。

---

如前图所示，概率量化的是：在分布参数（\(\mathbf{w}\)）给定的情况下，从该分布中抽样得到具有特定取值的数据（\(\mathbf{x}\)）的可能性。另一方面，似然 \(\mathcal{L}(\mathbf{w} \vert \mathbf{x})\) 计算的是：在观测数据给定的情况下，这些参数的"可信度"有多高——在实践中，我们会改变分布的参数，观察它如何影响似然。下图说明了如何获得固定数据点 \(x=0.5\) 的似然：

![](https://sebastianraschka.com/images/faq/probability-vs-likelihood/likelihood-1.png)

注意似然与概率密度之间的关系：  
\(\mathcal{L}(\mathbf{w} \vert \mathbf{x}) = p(\mathbf{x} \vert \mathbf{w})\)。
虽然数值相同，但概念不同。谈概率（或概率密度）时，我们假设参数给定，并在"从分布中抽样"的语境下计算概率。而谈似然时，我们把数据视为固定，去改变分布的参数。在许多场景中，我们感兴趣的是找到使似然最大化的参数。

下图比较了固定数据点 \(x=0.5\) 在两个不同正态分布下的似然：

![](https://sebastianraschka.com/images/faq/probability-vs-likelihood/likelihood-2.png)
