---
title: "协方差和相关性有什么区别？"
title_en: "What is the difference between covariance and correlation?"
source: https://sebastianraschka.com/faq/docs/covariance-vs-correlation.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 协方差和相关性有什么区别？

> 原文：[What is the difference between covariance and correlation?](https://sebastianraschka.com/faq/docs/covariance-vs-correlation.html) · Sebastian Raschka's FAQ

协方差（covariance）度量的是两个变量彼此之间的关联，即两个变量如何共同变化。

设 \(n\) 为总体大小，\(x\) 和 \(y\) 为两个不同的特征（变量），\(\mu\) 为总体均值；协方差可形式化地定义为：

\[\sigma\_{x y}=\frac{1}{n} \sum\_{i}^{n}\left(x^{(i)}-\mu\_{x}\right)\left(y^{(i)}-\mu\_{y}\right).\]

协方差为 0 表示两个变量完全无关。协方差为正时，两个变量朝相同方向增大；协方差为负时，两个变量朝相反方向变化。从上式可以看出，协方差的量级取决于每个变量的尺度（总体或样本均值的大小）。

Pearson 的 \(\rho\) 或 "r"（通常就直接称为"相关系数"）度量两个特征之间的线性相关，与协方差密切相关。事实上，它是协方差的归一化版本，如下所示：

\[\rho=\frac{\sum\_{i=1}^{n}\left[\left(x^{(i)}-\mu\_{x}\right)\left(y^{(i)}-\mu\_{y}\right)\right]}{\sqrt{\sum\_{i=1}^{n}\left(x^{(i)}-\mu\_{x}\right)^{2}} \sqrt{\sum\_{i=1}^{n}\left(y^{(i)}-\mu\_{y}\right)^{2}}}=\frac{\sigma\_{x y}}{\sigma\_{x} \sigma\_{y}}\]

（注意我们省去了 \(1/n\) 项，因为它被约掉了。）

通过用特征的标准差去除协方差，我们确保两个特征之间的相关性落在 [-1, 1] 区间内，这使它比无界的协方差更易于解读。不过要注意，如果特征已被归一化为单位方差（例如通过标准化或 z 分数归一化），协方差与相关性就完全相同。
当 \(\rho=1\) 时两个特征完全正相关，\(\rho=-1\) 时完全负相关。\(\rho=0\) 时观察不到相关。

## 标准化特征下的协方差与相关性

我们可以证明，两个特征之间的相关性实际上等于两个标准化特征的协方差。为了证明这一点，先把两个特征 \(x\) 和 \(y\) 标准化，得到它们的 z 分数，分别记作 \(x'\) 和 \(y'\)：

\[x^{\prime}=\frac{x-\mu\_{x}}{\sigma\_{x}}, \quad y^{\prime}=\frac{y-\mu\_{y}}{\sigma\_{y}}.\]

如你所回忆的，两个特征之间的（总体）协方差计算如下：

\[\sigma\_{x y}=\frac{1}{n} \sum\_{i}^{n}\left(x^{(i)}-\mu\_{x}\right)\left(y^{(i)}-\mu\_{y}\right).\]

由于标准化会做均值中心化，我们可以把上式改写为

\[\sigma\_{x y}^{\prime}=\frac{1}{n} \sum\_{i}^{n}\left(x^{\prime (i)}-0\right)\left(y^{\prime (i)}-0\right).\]

现在，如果我们用标准化特征的定义把那些项代回去，就得到：

\[\begin{equation}
\begin{aligned} & \frac{1}{n} \sum\_{i}^{n}\left(\frac{x-\mu\_{x}}{\sigma\_{x}}\right)\left(\frac{y-\mu\_{y}}{\sigma\_{y}}\right) \\ &= \frac{1}{n \cdot \sigma\_{x} \sigma\_{y}} \sum\_{i}^{n}\left(x^{(i)}-\mu\_{x}\right)\left(y^{(i)}-\mu\_{y}\right), \end{aligned}
\end{equation}\]

化简得

\[\sigma\_{x y}^{\prime}=\frac{\sigma\_{x y}}{\sigma\_{x} \sigma\_{v}}\]

这就完成了证明：当特征被标准化后，协方差与相关性是相同的。
