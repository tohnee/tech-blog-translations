---
title: "平方误差损失是合格的度量吗？"
title_en: "Is the squared error loss a proper metric?"
source: https://sebastianraschka.com/faq/docs/proper-metric-squared-error.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 平方误差损失是合格的度量吗？

考虑两个向量或点 \(\mathbf{v}\) 和 \(\mathbf{w}\)，以及它们的距离 \(d(\mathbf{v}, \mathbf{w})\)。

一个合格的度量（proper metric）需要满足以下准则：

1. 两点之间的距离总是非负的 \(d(\mathbf{v}, \mathbf{w}) \geq 0.\) 而且，距离只在两点完全相同时才为零，即 $\mathbf{v} = \mathbf{w}.$$
2. 距离是对称的，即 \(d(\mathbf{v}, \mathbf{w}) = d(\mathbf{w}, \mathbf{v}).\)
3. 距离函数对任意三点 \(\mathbf{v}, \mathbf{w}, \mathbf{x}\) 满足*三角不等式*，即
   \(d(\mathbf{v}, \mathbf{w}) \leq d(\mathbf{v}, \mathbf{x}) + d(\mathbf{x}, \mathbf{w}).\)

均方误差损失（MSE）计算目标变量 \(y\) 与预测目标值 \(\hat{y}\) 之间欧氏距离的平方：

\[\mathrm{MSE}=\frac{1}{n} \sum\_{i=1}^n\left(y^{(i)} - \hat{y}^{(i)}\right)^2.\]

下标 \(i\) 表示数据集或样本中的第 \(i\text{ 个}\)数据点。为简单起见，我们考虑两个数据点之间的平方误差（SE）损失（不过，下文的结论同样适用于 MSE）：

\[\mathrm{SE}(y, \hat{y})=\left(y - \hat{y}\right)^2.\]

**准则 1。** SE 满足第一条准则的前半部分：*两点之间的距离总是非负的。*由于我们对差值取了 2 次方，它不可能是负数。

**准则 2。** 那么第二条准则呢——*距离只在两点完全相同时才为零*？由于 SE 中存在减法，很容易直观看出：只有当预测值与目标变量完全一致、即 \(y = \hat{y}\) 时，它才为 0。

我们已经看到 SE 满足合格度量的第一条准则；还可以再次利用*平方*来确认它也满足第二条准则：*距离是对称的*。由于平方的存在，我们有 \(\left(y - \hat{y}\right)^2 = \left(\hat{y} - y\right)^2.\)

**准则 3。** 乍看之下，平方误差损失似乎也满足三角不等式。直观地，你可以任选三个数（这里取 1、2、3）来验证：

1. \[(1-2)^{2} \leq (1-3)^{2} + (2-3)^{2}\]
2. \[(1-3)^{2} \leq (1-2)^{2} + (2-3)^{2},\]
3. \[(2-3)^{2} \leq (1-2)^{2} + (1-3)^{2}.\]

然而，存在使该式不成立的取值，[例如 \(d(a,c) = 4\)，\(d(a,b) = 2\)，\(d(b,c) = 3\)](https://gmd.copernicus.org/articles/7/1247/2014/)，此时 \(4^2 \lneq 2^2 + 3^2\)，三角不等式不成立。

相比之下，均方根误差（root-mean squared error）确实满足三角不等式，上面的例子也成立：\(4 \lneq 2 + 3.\)

平方根误差 \(\sqrt{\left(y - \hat{y}\right)^2}\) 本质上就是两点之间的 \(L\_2\) 或欧氏距离，[后者已知满足三角不等式](https://en.wikipedia.org/wiki/Euclidean_distance)。

由于通过上面的例子可以看出它不满足三角不等式，我们得出结论：（均）平方误差损失不是一个合格的度量。
