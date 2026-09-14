---
title: "均值中心化与特征缩放如何影响 PCA"
title_en: "How Centering and Feature Scaling Affect PCA"
source: https://sebastianraschka.com/faq/docs/pca-scaling.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 均值中心化与特征缩放如何影响 PCA

让我们来思考一下：当主成分分析（PCA）是从协方差矩阵计算得到时（即 *k* 个主成分是协方差矩阵中对应 *k* 个最大特征值的特征向量），变量是否做中心化对结果有没有影响。

## 1. 均值中心化不影响协方差矩阵

这里的理由是：如果变量无论是否中心化，协方差都相同，那么 PCA 的结果也将相同。

假设我们有两个变量 **x** 和 **y**。那么属性之间的协方差计算为

![](https://sebastianraschka.com/images/faq/pca-scaling/1.png)

我们把中心化后的变量写作

![](https://sebastianraschka.com/images/faq/pca-scaling/2.png)

中心化后的协方差将按下式计算：

![](https://sebastianraschka.com/images/faq/pca-scaling/3.png)

但由于中心化之后，x̄' = 0 且 ȳ' = 0，我们有

![](https://sebastianraschka.com/images/faq/pca-scaling/4.png)

把各项代回原变量，这就是我们原始的协方差矩阵

![](https://sebastianraschka.com/images/faq/pca-scaling/5.png)

即使只中心化一个变量，比如 **x**，也不会影响协方差：

![](https://sebastianraschka.com/images/faq/pca-scaling/6.png)

## 2. 对变量做缩放确实会影响协方差矩阵

如果对某个变量做了缩放，比如从磅换算成千克（1 磅 = 0.453592 千克），协方差确实会受影响，进而影响 PCA 的结果。

设 *c* 为 *x* 的缩放因子。

鉴于"原始"协方差计算为

![](https://sebastianraschka.com/images/faq/pca-scaling/7.png)

缩放后的协方差将计算为：

![](https://sebastianraschka.com/images/faq/pca-scaling/8.png)

因此，将一个属性按常数 *c* 缩放后，协方差会变成重新缩放过的协方差 *cσxy*。所以，如果我们将 x 从磅缩放为千克，x 与 y 之间的协方差将变为原来的 0.453592 倍（即缩小为 0.453592 分之一）。

## 3. 标准化会影响协方差

对特征做标准化会影响 PCA 的结果（假设变量原本不是标准化的）。这是因为我们用每一对变量的标准差之积，对每对变量之间的协方差都进行了缩放。

变量标准化的公式写作

![](https://sebastianraschka.com/images/faq/pca-scaling/9.png)

"原始"协方差矩阵：

![](https://sebastianraschka.com/images/faq/pca-scaling/10.png)

将两个变量都标准化之后：

![](https://sebastianraschka.com/images/faq/pca-scaling/11.png)
