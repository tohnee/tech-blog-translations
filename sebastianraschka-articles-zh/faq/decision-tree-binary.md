---
title: "二叉决策树与不纯度指标"
title_en: "Binary Decision Trees and Impurity Metrics"
source: https://sebastianraschka.com/faq/docs/decision-tree-binary.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 二叉决策树与不纯度指标

> 原文：[Binary Decision Trees and Impurity Metrics](https://sebastianraschka.com/faq/docs/decision-tree-binary.html) · Sebastian Raschka's FAQ

出于实际原因（组合爆炸），大多数库实现的决策树都采用二叉分裂。有意思的是，构造最优二叉决策树是 NP 完全问题（Hyafil, Laurent, and Ronald L. Rivest. “Constructing optimal binary decision trees is NP-complete.” Information Processing Letters 5.1 (1976): 15-17.）。

我们的目标函数（例如在 CART 中）是在每次分裂时最大化信息增益（information gain，IG）：

![](https://sebastianraschka.com/images/faq/decision-tree-binary/information-gain.png)

其中 *f* 是用于执行分裂的特征，*D\_p* 和 *D\_j* 分别是父节点和第 *j* 个子节点的数据集。*I* 是不纯度度量。*N* 是样本总数，*N\_j* 是第 *j* 个子节点上的样本数。
现在来看分类中最常用的分裂准则（如 CART 中所述）。为简单起见，我将针对二叉分裂写出各公式，当然它们也可以推广到多路分裂。于是，对于二叉分裂，我们可以这样计算 *IG*：

![](https://sebastianraschka.com/images/faq/decision-tree-binary/information-gain-2.png)

二叉决策树中常用的两种不纯度度量（分裂准则）是基尼不纯度（Gini Impurity，*I\_G*）和熵（Entropy，*I\_H*），此外还有分类错误率（Classification Error，*I\_E*）。让我们先从熵的定义开始，其定义为：

![](https://sebastianraschka.com/images/faq/decision-tree-binary/entropy.png)

对所有"非空"类：

![](https://sebastianraschka.com/images/faq/decision-tree-binary/empty-classes.png)

其中 *p(i|t)* 是节点 *t* 上属于类别 *c* 的样本比例。因此，若某节点上的所有样本都属于同一类别，则熵为 0；若类别分布均匀，则熵最大。
直观上，基尼不纯度可以理解为最小化误分类概率的准则：

![](https://sebastianraschka.com/images/faq/decision-tree-binary/gini-impurity.png)

与熵类似，当各类别完全混杂时，基尼不纯度最大。
然而在实践中，基尼不纯度和熵通常给出非常相似的结果，与其花大量时间用不同的不纯度准则评估树，不如多尝试不同的剪枝阈值，后者往往更值得。
另一个不纯度度量是分类错误率：

![](https://sebastianraschka.com/images/faq/decision-tree-binary/error.png)

它是剪枝的有用准则，但不推荐用于生长决策树，因为它对节点类别概率的变化不那么敏感。

![](https://sebastianraschka.com/images/faq/decision-tree-binary/overview-plot.png)

下面让我借助下图中所示的两种可能的分裂场景，来解释"分类错误率对类别概率的变化不那么敏感"是什么意思。

![](https://sebastianraschka.com/images/faq/decision-tree-binary/split.png)

我们从一个由 40 个类别 1 样本和 40 个类别 2 样本组成的父节点数据集 *D\_p* 出发，将其分裂为两个数据集 D\_left 和 D\_right。若以分类错误率作为分裂准则，则场景 *A* 和场景 *B* 的信息增益相同（*IG\_E* = 0.25）：

![](https://sebastianraschka.com/images/faq/decision-tree-binary/calc_1.png)

![](https://sebastianraschka.com/images/faq/decision-tree-binary/calc_2.png)

然而，基尼不纯度会更青睐场景 B（0.1666）而非场景 A（0.125），而场景 B 确实更"纯"：

![](https://sebastianraschka.com/images/faq/decision-tree-binary/calc_3.png)

类似地，熵准则也会更青睐场景 B（IGH = 0.31）而非场景 A（IGH = 0.19）：

![](https://sebastianraschka.com/images/faq/decision-tree-binary/calc_5.png)

![](https://sebastianraschka.com/images/faq/decision-tree-binary/calc_6.png)

关于基尼对比熵，也许还可以再多说几句。如前所述，实践中得到的树通常非常相似。基尼的一个可能优点是你无需计算对数，这可以让你的实现稍快一些。
