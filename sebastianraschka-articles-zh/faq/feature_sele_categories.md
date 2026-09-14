---
title: "过滤式、包裹式与嵌入式特征选择"
title_en: "Filter, Wrapper, and Embedded Feature Selection"
source: https://sebastianraschka.com/faq/docs/feature_sele_categories.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 过滤式、包裹式与嵌入式特征选择

> 原文：[Filter, Wrapper, and Embedded Feature Selection](https://sebastianraschka.com/faq/docs/feature_sele_categories.html) · Sebastian Raschka's FAQ

包裹式（wrapper）方法依据分类器性能来衡量特征的「有用程度」。与之相对，过滤式（filter）方法借助单变量统计量来捕捉特征本身的内在属性（即特征的「相关性」），而不是交叉验证性能。因此，包裹式方法本质上是在求解「真正」的问题（优化分类器性能），但由于需要反复的训练步骤和交叉验证，其计算成本也比过滤式方法更高。
第三类，嵌入式（embedded）方法与包裹式方法颇为相似，因为它们同样用于优化学习算法或模型的目标函数或性能。与包裹式方法的区别在于，嵌入式方法在训练过程中使用了一种内在的模型构建度量指标。
让我凭记忆列举这三类方法的一些例子。

## 过滤式方法：

- 信息增益（information gain）
- 卡方检验（chi-square test）
- Fisher 分数（fisher score）
- 相关系数（correlation coefficient）
- 方差阈值（variance threshold）

## 包裹式方法：

- 递归特征消除（recursive feature elimination）
- 序贯特征选择算法（sequential feature selection algorithms）
- 遗传算法（genetic algorithms）

## 嵌入式方法：

- L1（LASSO）正则化
- 决策树

（注意，我会把主成分分析（Principal Component Analysis）这类变换与投影技术归为特征*提取*方法，因为我们是在把数据投影到一个新的特征空间中。）
为了给你更直观的说明，让我从每个类别中各挑一个算法来解释。

**1). 过滤式方法示例：方差阈值**

这里，我们只需计算每个特征的方差，然后根据用户指定的阈值来选择特征子集。例如，「保留所有方差大于等于 *x* 的特征」，或者「保留方差最大的前 *k* 个特征」。我们假设方差较大的特征可能包含更有用的信息，但请注意，我们并没有考虑特征变量之间以及特征与目标变量之间的关系，这是过滤式方法的缺点之一。

**2). 包裹式方法示例：序贯特征选择**

序贯前向选择（Sequential Forward Selection，SFS）是序贯特征选择的一个特例，它是一种贪心搜索算法，试图依据分类器性能迭代地选择特征，从而找到「最优」特征子集。我们从一个空的特征子集开始，每一轮每次加入一个特征；这个特征从所有尚未进入特征子集的特征池中选出，并且是加入后能使分类器性能最优的那个特征。由于我们必须对每一种特征子集组合都训练并交叉验证模型，这种方法比前面讨论的方差阈值之类的过滤式方法昂贵得多。

**3). 嵌入式方法示例：L1 正则化**

对于广义线性模型，L1（或 LASSO）回归可以理解为向代价函数中加入一个针对复杂度的惩罚项，通过引入更多偏差来降低模型的过拟合程度或方差。这里，我们直接在代价函数中加入一个惩罚项，

```python
regularized_cost = cost + regularization_penalty
```

在 L1 正则化中，惩罚项为

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| L1 : λ Σki | wi | = λ | **w** | 1, |

其中 **w** 是我们的 *k 维*特征向量。加入 L1 项之后，我们的目标函数就变成了对正则化代价的最小化；由于惩罚项会随权重参数取值的增大而增大（λ 只是一个用于微调正则化强度的自由参数），我们可以通过这个 L1 向量范数诱导稀疏性——这可以看作一种内在于模型训练步骤中的特征选择方式。
