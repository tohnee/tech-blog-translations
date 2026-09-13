---
title: "机器学习模型评估：第 4 部分"
title_en: "ML Model Evaluation: Part 4"
source: https://sebastianraschka.com/blog/2018/model-evaluation-selection-part4.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 机器学习模型评估：第 4 部分

> 原文：[ML Model Evaluation: Part 4](https://sebastianraschka.com/blog/2018/model-evaluation-selection-part4.html)

**《模型评估》第 1–4 部分的单份 PDF 版本已发布在 arXiv：<https://arxiv.org/abs/1811.12808>**

## 引言

本文是系列文章*机器学习中的模型评估、模型选择与算法选择*的最后一篇，将概述几种统计假设检验方法，及其在机器学习模型与算法比较中的应用。这包括基于独立测试集预测结果的统计检验（前几篇文章已经讨论过使用单一测试集进行模型比较的弊端），也包括通过交叉验证拟合并评估模型来进行算法比较的方法。最后，本文将介绍*嵌套交叉验证*（nested cross-validation），对于小到中等规模的数据集，它已成为一种常见且被推荐的算法比较首选方法。

在本文末尾，我会给出一份个人建议清单，涵盖模型评估、模型选择与算法选择，以此总结本系列文章中介绍的多种技术。

## 比例差异检验

实践中有若干不同的统计假设检验框架被用于比较分类模型的性能，其中包括一些传统方法，例如两个比例的差异检验（这里的比例指从测试集估计得到的泛化准确率）；我们可以基于「二项分布的正态近似」（Normal Approximation to the Binomial）概念为其构造 95% 置信区间，这一概念在[第一部分](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part1.html)中介绍过。

对两个总体比例做 z 分数检验（z-score test），无疑是比较两个模型最直接的方式（但绝不是最好的！）：简而言之，如果两个模型的准确率各自的 95% 置信区间不重叠，我们就可以在 \(\alpha=0.05\)（即 5% 概率）的置信水平上拒绝「两个分类器性能相等」这一零假设。撇开对假设的违背不谈（例如测试集样本并不独立），正如 Thomas Dietterich 基于一项模拟研究的经验结果所指出的（Dietterich 1998），这种检验往往有较高的假阳性率（这里指：在不存在差异时错误地检测出差异），这也是它不被推荐在实践中使用的原因之一。

尽管如此，出于完整性考虑，也由于它确实是实践中常用的方法，下面概述其一般流程（这一流程同样大体适用于后文介绍的各种假设检验）：

1. 陈述待检验的假设（例如，零假设为两个比例相同；相应地，如果我们采用双尾检验，则备择假设为两个比例不同）；
2. 确定显著性阈值（例如，如果观察到比当前差异更极端的差异的概率超过 5%，我们就计划拒绝零假设）；
3. 分析数据，计算检验统计量（这里是 z 分数），并将其对应的 p 值（概率）与先前确定的显著性阈值进行比较；
4. 根据 p 值和显著性阈值，在给定置信水平上接受或拒绝零假设，并对结果做出解释。

z 分数的计算方式是：观察到的差异除以两者合并方差的平方根

\[z = \frac{ACC\_1 - ACC\_2}{\sqrt{\sigma\_{1}^2 + \sigma\_{2}^2}},\]

其中 \(ACC\_1\) 是一个模型的准确率，\(ACC\_2\) 是从测试集估计出的另一个模型的准确率。回想一下，我们在[第一部分](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part1.html)中把估计准确率的方差计算为

\[\sigma^2 = \frac{ACC(1-ACC)}{n}\]

然后把置信区间（正态近似区间，Normal Approximation Interval）计算为

\[ACC \pm z \times \sigma,\]

其中 95% 置信区间对应 \(z=1.96\)。比较两个准确率估计的置信区间并检查它们是否重叠，就相当于计算两个比例差异的 \(z\) 值，并把概率（p 值）与选定的显著性阈值进行比较。因此，要直接为两个比例 \(ACC\_1\) 和 \(ACC\_2\) 的差异计算 z 分数，我们先合并（pool）这两个比例（假设 \(ACC\_1\) 和 \(ACC\_2\) 分别是在两个大小为 \(n\_1\) 和 \(n\_2\) 的独立测试集上估计出的两个模型的性能），

\[ACC\_{1, 2} = \frac{ACC\_1 \times n\_1 + ACC\_2 \times n\_2}{n\_1 + n\_2},\]

然后计算标准差

\[\sigma\_{1,2} = \sqrt{ ACC\_{1,2} (1-ACC\_{1,2}) \times \left(\frac{1}{n\_1} + \frac{1}{n\_2}\right) },\]

这样我们就可以计算 z 分数

\[z = \frac{ACC\_1 - ACC\_2}{\sigma\_{1,2}}.\]

由于使用的是同一个测试集（违背了独立性假设），我们有 \(n\_1 = n\_2 = n\)，于是可以把 z 分数的计算简化为

\[z = \frac{ACC\_1 - ACC\_2}{\sqrt{2\sigma^2}} = \frac{ACC\_1 - ACC\_2}{\sqrt{2\cdot ACC\_{1,2}(1-ACC\_{1,2}))/n}},\]

其中 \(ACC\_{1, 2}\) 就是 \((ACC\_1 + ACC\_2)/2\)。

第二步，基于计算出的 \(z\) 值（这里假设测试误差相互独立，而由于我们使用的是同一个测试集，这一假设在实践中通常不成立），如果 \(\lvert z \rvert\) 大于 1.96，我们就可以在 \(\alpha=0.05\) 的显著性水平上拒绝「这一对模型性能相等」（这里的性能以「分类准确率」衡量）的零假设。另一种做法是，如果我们愿意多花点功夫，可以计算标准正态累积分布在 z 分数阈值处的面积。如果发现这个 p 值小于我们在做检验之前设定的显著性水平，那么就可以在该显著性水平上拒绝零假设。

不过这种检验的问题在于，我们用同一个测试集来计算两个分类器的准确率；因此，使用配对检验（例如配对样本 t 检验）可能会更好，而更稳健的选择是下一节将介绍的 McNemar 检验。

## 用 McNemar 检验比较两个模型

因此，Dietterich（Dietterich, 1998）发现，相比「比例差异」检验，McNemar 检验更值得采用。McNemar 检验由 Quinn McNemar 于 1947 年提出（McNemar 1947），是一种用于配对比较的非参数统计检验，可用于比较两个机器学习分类器的性能。

McNemar 检验也常被称为「被试内卡方检验」（within-subjects chi-squared test），它应用于配对的定类数据，基于一种 2x2 混淆矩阵（有时也称为 *2x2 列联表*）将两个模型的预测结果相互比较（不要与机器学习中常见的混淆矩阵混淆——后者列出的是单个模型的假阳性、真阳性、假阴性和真阴性计数）。适合 McNemar 检验的 2x2 混淆矩阵布局如下图所示：

![Model evaluation selection part4 mcnemar table layout](https://sebastianraschka.com/images/blog/2018/model-evaluation-selection-part4/mcnemar-table-layout.webp)

对于上图所示的 2x2 混淆矩阵，我们可以通过 \((A+B) / (A+B+C+D)\) 计算 *模型 1* 的准确率，其中 \(A+B+C+D\) 是测试样本总数 \(n\)。类似地，模型 2 的准确率可计算为 \((A+C) / n\)。不过，这张表中最有意思的数字在 B 和 C 两格，因为 A 和 D 只是分别统计了 *模型 1* 和 *模型 2* 同时预测正确或同时预测错误的样本数。而对角线之外的 B 和 C 两格（非对角项）则告诉我们两个模型的差异所在。为了说明这一点，让我们看看下面的例子：

![Model evaluation selection part4 mcnemar table example1](https://sebastianraschka.com/images/blog/2018/model-evaluation-selection-part4/mcnemar-table-example1.webp)

在 A、B 两个子图中，*模型 1* 和 *模型 2* 的准确率分别为 99.6% 和 99.7%。

- 模型 1 准确率，子图 A：\((9959+11) / 10000 \times 100\% = 99.7\%\)
- 模型 1 准确率，子图 B：\((9945+25) / 10000 \times 100\% = 99.7\%\)
- 模型 2 准确率，子图 A：\((9959+1) / 10000 \times 100\% = 99.6\%\)
- 模型 2 准确率，子图 B：\((9945+15) / 10000 \times 100\% = 99.6\%\)

在子图 A 中，我们可以看到 *模型 1* 有 11 个预测对了，而 *模型 2* 预测错了；反过来，*模型 2* 只有 1 个预测对了而 *模型 1* 预测错了。因此，基于这个 11:1 的比例，凭直觉我们可能得出结论：*模型 1* 的性能明显优于 *模型 2*。然而在子图 B 中，*模型 1*:*模型 2* 的比例是 25:15，这对于该选哪个模型就不那么有说服力了。这正是 McNemar 检验能派上用场的好例子。

在 McNemar 检验中，我们设定零假设为概率 \(p(B)\) 和 \(p(C)\) 相同——其中 \(B\) 和 \(C\) 指前面图中介绍的混淆矩阵单元格；用简化的说法就是：两个模型都不比另一个表现更好。相应地，备择假设是两个模型的性能不相等。

McNemar 检验统计量（「卡方」）可按如下方式计算：

\[\chi^2 = \frac{(B-C)^2}{B+C}.\]

设定显著性阈值（例如 \(\alpha=0.05\)）之后，我们可以计算 p 值——假设零假设为真，p 值就是观察到当前经验（或更大）\(\chi^2\) 值的概率。如果 p 值低于我们选择的显著性水平，就可以拒绝「两个模型性能相等」的零假设。

由于 McNemar 检验统计量 \(\chi^2\) 服从自由度为 1 的 \(\chi^2\) 分布（在零假设成立、且 B 与 C 格中的数字相对较大（比如 > 25）的前提下），我们现在可以用自己喜欢的软件包，通过自由度为 1 的 \(\chi^2\) 概率分布来「查表」得到（单尾）概率。

如果对上图中场景 B（\(\chi^2=2.5\)）这样做，我们会得到 0.1138 的 p 值，它大于显著性阈值，因此无法拒绝零假设。而如果计算场景 A（\(\chi^2=8.3\)）的 p 值，我们会得到 0.0039，低于设定的显著性阈值（\(\alpha=0.05\)），从而拒绝零假设；我们可以得出结论：两个模型的性能不同（例如，*模型 1* 优于 *模型 2*）。

在 Quinn McNemar 发表 McNemar 检验（McNemar 1947）大约一年之后，Allen L. Edwards（Edwards 1948）提出了一个连续性校正版本，也就是今天更常用的变体：

\[\chi^2 = \frac{\big(| B - C| -1 \big)^2}{B+C}.\]

Edwards 特别写道：

> This correction will have the apparent result of reducing the absolute value of the difference, [B - C], by unity.

按照 Edwards 的说法，当我们处理的是离散频数、且数据要对照卡方分布进行评估时，这种连续性校正能提高 McNemar 检验的实用性和准确性。

MLxtend（Raschka, 2018）中实现了用于 McNemar 检验的函数：<http://rasbt.github.io/mlxtend/user_guide/evaluate/mcnemar/>。

## 通过二项检验计算精确 p 值

当 B、C 两格中的数值大于 50（指前面展示的 2x2 混淆矩阵）时，McNemar 检验对 p 值的近似相当不错；而当 B 和 C 的值相对较小时，由于 McNemar 检验得到的卡方值可能无法被卡方分布很好地近似，此时就有理由使用计算上更昂贵的二项检验来计算精确 p 值。

精确 p 值可按如下方式计算（依据是：在零假设下，McNemar 检验本质上是一个比例为 0.5 的二项检验）：

\[p = 2 \sum^{n}\_{i=max(B, C)} \binom{n}{i} 0.5^i (1 - 0.5)^{n-i},\]

其中 \(n=B+C\)，因子 2 用于计算双侧 p 值（这里的 \(n\) 不要与测试集大小 \(n\) 混淆）。

下面的热图展示了 McNemar 卡方值近似（含与不含 Edwards 连续性校正）与通过二项检验计算的精确 p 值之间的差异：

![Model evaluation selection part4 pvalue diff](https://sebastianraschka.com/images/blog/2018/model-evaluation-selection-part4/pvalue-diff.webp)

从上面的热图可以看到，当 B 和 C 都大于 50 时，经过连续性校正的 McNemar 检验得到的 p 值与二项检验的 p 值几乎完全一致。（MLxtend 的 `mcnemar,` 函数提供了在常规版与校正版 McNemar 检验之间切换的不同选项，并包含计算精确 p 值的选项，<http://rasbt.github.io/mlxtend/user_guide/evaluate/mcnemar/>）

## 多重假设检验

上一节我们讨论了如何用 McNemar 检验比较两个机器学习分类器。然而在实践中，我们往往有两个以上的模型需要基于其估计的泛化性能进行比较——例如基于在独立测试集上的预测结果。这时，如果多次应用前面描述的检验流程，就会遇到一个典型问题，称为「多重假设检验」（multiple hypotheses testing）。应对这类场景的一种常见做法如下：

1. 在「分类准确率之间没有差异」的零假设下进行综合检验（omnibus test）。
2. 如果综合检验拒绝了零假设，再进行成对的事后检验（post hoc test），并对多重比较做校正，以确定模型性能之间的差异出现在哪里。（例如，这里可以使用 McNemar 检验。）

综合检验（omnibus test）是一类用于检查随机样本是否偏离零假设的统计检验。综合检验的一个常见例子是所谓的方差分析（ANOVA），它是一种分析组间均值差异的方法；换句话说，ANOVA 常用于检验「若干组的均值相等」这一零假设的显著性。要比较多个机器学习模型，Cochran's Q 检验是一个可选方案，它本质上是 McNemar 检验面向三个或更多模型的推广版本。不过，综合检验是整体层面的显著性检验，不会提供各模型之间如何不同的信息——像 Cochran's Q 这样的综合检验只能告诉我们一组模型之间是否存在差异。

由于综合检验只能告诉我们模型*是否*存在差异，而无法告诉我们*如何*不同，因此当综合检验拒绝了零假设时，我们可以进行事后检验。换句话说，如果我们成功地在预先设定的显著性阈值上拒绝了「三个或更多模型性能相同」的零假设，就可以断定不同模型之间至少存在一处显著差异。

顾名思义，*事后*（post hoc）检验程序不需要任何「事先」的检验计划。因此，事后检验程序名声可能不太好，会被视为「碰运气的捕捞」或「大海捞针」，因为事先并不明确该比较哪些模型，于是不得不把所有可能的模型两两配对进行比较，这就引出了我们在[第三部分](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part3.html)简要讨论过的多重假设问题。**不过请记住，这些全都是近似方法，凡涉及统计检验以及重复使用测试集（违背独立性）的做法，都应当（至少）持保留态度。**

在事后检验中，我们可以使用众多校正项之一，例如针对多重假设检验的 Bonferroni 校正（Bonferroni, 1936; Dunn 1961）。简而言之，某个显著性阈值（或 \(\alpha\) 水平）对于两个模型之间的单次比较也许是合适的，但对于多次成对比较并不适用。举例来说，使用 Bonferroni 校正就是把显著性阈值调整得更保守，从而降低多重比较检验中的假阳性率。

接下来的两节将讨论两种综合检验：Cochran's Q 检验，以及由 Looney 提出的、用于在同一个测试集上比较多个分类器的 F 检验（Looney, 1988）。

## 用 Cochran's Q 检验比较多个分类器的性能

Cochran's Q 检验可以看作 McNemar 检验的推广版本，可用于比较三个或更多分类器。从某种意义上说，Cochran's Q 检验类似于 ANOVA，但面向配对的定类数据。与 ANOVA 一样，它不会告诉我们哪些组（或模型）之间存在差异——只告诉我们模型之间存在差异。

检验统计量 \(Q\) 近似服从自由度为 \(M-1\) 的卡方分布（与 McNemar 检验类似），其中 \(M\) 是我们要评估的模型数量（由于 McNemar 检验中 \(M=2\)，McNemar 检验统计量近似服从自由度为 1 的卡方分布）。

更正式地说，Cochran's Q 检验检验的零假设（\(H\_0\)）是分类准确率之间没有差异（Fleiss, 2013）：

\[H\_0: ACC\_1 = ACC\_2 = \ldots = ACC\_M.\]

设 \(\{C\_1, \dots , C\_M\}\) 为一组都在同一个数据集上测试过的分类器。如果这 \(M\) 个分类器在性能上没有差异，那么下面的 \(Q\) 统计量近似服从自由度为 \(M-1\) 的「卡方」分布：

\[Q = (M-1) \frac{M \sum^{M}\_{i=1}G\_{i}^{2} - T^2}{MT - \sum^{n}\_{j=1}M\_j^2} .\]

这里，\(G\_i\) 是 \(n\) 个测试样本中被 \(C\_i= 1, \dots M\) 正确分类的对象数量；\(M\_j\) 是 \(M\) 个分类器中正确分类了测试数据集中第 \(j\) 个样本的分类器数量；\(T\) 是 \(M\) 个分类器正确投票的总数（Kuncheva, 2004）：

\[T = \sum\_{i=1}^{M}; \quad G\_i = \sum^{N}\_{j=1} M\_j.\]

执行 Cochran's Q 检验时，我们通常把分类器的预测结果组织成一个二值的 \(n \times M\) 矩阵（测试样本数 × 分类器数）。若分类器 \(C\_j\) 误分类了数据样本（向量）\(\mathbf{x}\_i\)，则该矩阵的第 \(ij\text{th}\) 个元素为 0，否则（即分类器正确预测了类别标签 \(f(\mathbf{x}\_i)\)）为 1。

下面以取自（Kuncheva, 2004）的示例数据集为例，说明分类结果可以如何组织。例如，假设我们有测试数据集的真实标签 \(\mathbf{y}\_{true}\)

以及 3 个分类器在测试集上的如下预测（\(\mathbf{y}\_{C\_1}\)、\(\mathbf{y}\_{C\_2}\) 和 \(\mathbf{y}\_{C\_3}\)）：

\[\mathbf{y}\_{true} = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\\
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \\
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \\
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\\
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];\]
\[\mathbf{y}\_{C\_1} = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,\\
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\\
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\\
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\\
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];\]
\[\mathbf{y}\_{C\_2} = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\\
1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\\
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\\
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\\
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];\]
\[\mathbf{y}\_{C\_3} = [1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\\
1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\\
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\\
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\\
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1].\]

然后我们可以把正确（1）与错误（0）的分类结果制成如下表格：

|  | \(C\_1\)（模型 1） | \(C\_2\)（模型 2） | \(C\_3\)（模型 3） | 出现次数 |
| --- | --- | --- | --- | --- |
|  | 1 | 1 | 1 | 80 |
|  | 1 | 1 | 0 | 2 |
|  | 1 | 0 | 1 | 0 |
|  | 1 | 0 | 0 | 2 |
|  | 0 | 1 | 1 | 9 |
|  | 0 | 1 | 0 | 1 |
|  | 0 | 0 | 1 | 3 |
|  | 0 | 0 | 0 | 3 |
| 准确率 | \(84/100 \times 100\% = 84\%\) | \(92/100 \times 100\% = 92\%\) | \(92/100 \times 100\% = 92\%\) |  |

把相应的数值代入前面的公式，我们得到如下 \(Q\) 值：

\[Q = 2 \times \frac{3 \times (84^2 + 92^2 + 92^2) - 268^2}{3\times 268-(80 \times 9 + 11 \times 4 + 6 \times 1)} \approx 7.5294.\]

现在，这个 Q 值（近似于 \(\chi^2\)）在自由度为 \(M-1 = 2\) 的 \(\chi^2\) 分布下对应的 p 值约为 0.023。假设我们选择的显著性水平为 \(\alpha=0.05\)，由于 \(0.023 < \alpha\)，我们会拒绝「所有分类器性能一样好」的零假设。（MLxtend 中提供了 Cochran's Q 检验的实现，<http://rasbt.github.io/mlxtend/user_guide/evaluate/cochrans_q/>。）

在实践中，如果我们成功拒绝了零假设，就可以进行多次事后成对检验——例如带 Bonferroni 校正的 McNemar 检验——来确定哪些模型对之间总体比例不同。遗憾的是，大量比较在实践中通常非常棘手。Peter H. Westfall、James F. Troendl 和 Gene Pennello 曾写过一篇很好的文章，讨论当我们想把多个模型相互比较时该如何处理这类情况（Westfall *等人* 2010）。

正如 Perneger, Thomas V（Perneger, 1998）所写：

> Type I errors [False Positives] cannot decrease (the whole point of Bonferroni adjustments) without inflating type II errors (the probability of accepting the null hypothesis when the alternative is true) (Rothman, 1990). And type II errors [False Negatives] are no less false than type I errors.

说到底，这又一次归结为「没有免费的午餐」——在这个语境下，我们不妨称之为「统计检验的没有免费午餐定理」。不过，统计检验框架在决策中可以成为有价值的辅助工具。因此，在实践中，如果我们诚实而严谨，带有适当校正的多重假设检验流程可以成为决策的重要助力。但是，在评估数据中的证据时，我们必须小心，不要对这类流程寄予过多期望。

## 用 F 检验比较多个分类器

颇具讽刺意味的是，Cochran 在其关于 Q 检验的工作中（Cochran, 1950）指出：

> If the data had been measured variables that appeared normally distributed, instead of a collection of 1's and 0's, the F-test would be almost automatically applied as the appropriate method. Without having looked into that matter, I had once or twice suggested to research workers that the F-test might serve as an approximation even when the table consists of 1's and 0's

本节使用 F 检验比较两个分类器的方法大致依据 Looney, 1988（需要说明的是，Looney 推荐的是一个称为 \(F^+\) 检验的调整版本）。

在 F 检验的语境下，我们的零假设同样是分类准确率之间没有差异：

\[p\_i: H\_0 = p\_1 = p\_2 = \cdots = p\_L.\]

设 \(\{C\_1, \dots , C\_M\}\) 为一组都在同一个数据集上测试过的分类器。如果这 \(M\) 个分类器性能没有差异，那么 F 统计量服从自由度为 \((M-1)\) 和 \((M-1)\times n\) 的 F 分布，其中 \(n\) 是测试集中的样本数量。F 统计量的计算包含若干组成部分，列举如下（改编自 \cite{looney1988statistical}）。

我们先定义 \(ACC\_{avg}\) 为不同模型准确率的平均值

\[ACC\_{avg} = \frac{1}{M}\sum\_{j=1}^M ACC\_j.\]

然后，分类器的平方和计算为

\[SSA = n \sum\_{j=1}^{M} (G\_j)^2 -n \cdot M \cdot ACC\_{avg},\]

其中 $G\_j$ 是分类器 \(j\) 正确分类的样本占 \(n\) 个样本的比例。

对象（样本）的平方和计算如下：

\[SSB= \frac{1}{M} \sum\_{j=1}^n (M\_j)^2 - M\cdot n \cdot ACC\_{avg}^2.\]

这里，\(M\_j\) 是 $M$ 个分类器中正确分类了对象 \(\mathbf{x}\_j \in \mathbf{X}\_{n}\) 的分类器数量，其中 \(\mathbf{X}\_{n} = \{\mathbf{x}\_1, ... \mathbf{x}\_{n}\}\) 是分类器受测的测试数据集。

最后，我们计算总平方和

\[SST = M\cdot n \cdot ACC\_{avg} (1 - ACC\_{avg}),\]

进而可以计算「分类–对象」交互作用的平方和：

\[SSAB = SST - SSA - SSB.\]

为了计算 F 统计量，接下来计算 SSA 与 SSAB 的均值：

\[MSA = \frac{SSA}{M-1},\]

以及

\[MSAB = \frac{SSAB}{(M-1) (n-1)}.\]

由 MSA 和 MSAB，我们可以如下计算 F 值：

\[F = \frac{MSA}{MSAB}.\]

计算出 F 值之后，我们可以从 F 分布表中查到相应自由度对应的 p 值，或者通过累积 F 分布函数计算得到。在实践中，如果我们成功地在先前选定的显著性阈值上拒绝了零假设，就可以进行多次*事后*成对检验——例如带 Bonferroni 校正的 McNemar 检验——来确定哪些模型对之间总体比例不同。

这个 F 检验的实现可在 mlxtend 中找到：<http://rasbt.github.io/mlxtend/user_guide/evaluate/ftest>。

## 算法比较

前面介绍的统计检验聚焦于模型比较，因而没有考虑训练集的方差；当训练集很小、而学习算法对训练集扰动敏感时，这可能会成为问题。

然而，如果考虑的是「多组模型」之间的比较——其中每组模型拟合自不同的训练集——那么在概念上我们就从模型比较转移到了算法比较的任务。而这往往是人们想要的。例如，假设我们开发了一种新的学习算法，或者想决定新软件应搭载哪种学习算法（一个简单的例子是带学习算法的邮件程序，它根据用户的操作学习如何过滤垃圾邮件）。在这种情况下，我们想了解的是不同算法在来自相似问题域的数据集上的表现。

算法比较的常用技术之一是 Thomas Dietterich 的 5 \(\times\) 2 折交叉验证方法（简称 5x2cv），由其在论文《Approximate statistical tests for comparing supervised classification learning algorithms》（Dietterich, 1998）中提出。这是一篇很好的论文，在统计检验的语境下讨论了所有不同的检验场景（模型评估、模型选择和算法选择的不同情形与应用）。在模拟数据集上通过经验比较得出的结论总结如下：

1. McNemar 检验：
   - 假阳性率低
   - 速度快，只需执行一次
2. 比例差异检验：
   - 假阳性率高（这里指在不存在差异时错误地检测出差异）
   - 不过计算成本低
3. 重采样配对 t 检验：
   - 假阳性率高
   - 计算成本非常高
4. k 折交叉验证 t 检验：
   - 假阳性率有所偏高
   - 需要在训练集上重新拟合；计算量是 McNemar 检验的 *k* 倍
5. 5x2cv 配对 t 检验
   - 假阳性率低（与 McNemar 类似）
   - 比 McNemar 检验的统计功效略高；如果计算效率（运行时间）不是问题则值得推荐（计算量是 McNemar 检验的 10 倍）

结论是：如果数据集相对较大，和/或模型拟合只能进行一次，McNemar 检验是不错的选择。如果模型可以反复拟合，5x2cv 检验则是好选择，因为它还考虑了训练集变化或重采样对模型拟合的影响。

出于完整性考虑，下一节将总结我们尚未介绍过的那些检验的具体机制。

## 重采样配对 t 检验

重采样配对 *t* 检验（resampled paired *t*-test，也称为 k 次留出配对 *t* 检验）是一种流行的两模型（分类器或回归器）性能比较方法；然而正如 Dietterich（Dietterich, 1998）所指出的，这一方法有许多缺陷，不建议在实践中使用。

为了解释这一方法的工作原理，考虑两个分类器 \(C\_1\) 和 \(C\_2\)，以及一个带标签的数据集 \(\mathcal{D}\)。在常见的留出法（hold-out method）中，我们通常把数据集分成两部分：训练集和测试集。在重采样配对 *t* 检验流程中，我们把这一划分过程重复 *k* 次（通常 2/3 作为训练数据、1/3 作为测试数据；*k* 通常取 30 或更多）。在每次迭代中，我们在同一个训练集上拟合 \(C\_1\) 和 \(C\_2\)，并在同一个测试集上评估它们。然后，我们在每次迭代中计算 \(C\_1\) 与 \(C\_2\) 的性能差异，从而得到 *k* 个差异度量。现在，假设这 *k* 个差异是独立抽取的、且近似服从正态分布，那么在「模型 \(C\_1\) 和 \(C\_2\) 性能相等」的零假设下，我们就可以按照 Student *t* 检验，计算自由度为 *k-1* 的如下 *t* 统计量：

\[t = \frac{ACC\_{avg} \sqrt{k}}{\sqrt{\sum\_{i=1}^{k}(ACC\_{i} - ACC\_{avg})^2 / (k-1)}}.\]

这里，\(ACC\_i\) 是第 \(i\) 次迭代中模型准确率之差，即 \(ACC\_i = ACC\_{i, C\_1} - ACC\_{i, C\_2}\)；\(ACC\_{avg}\) 表示分类器性能差异的平均值，即 \(ACC\_{avg} = \frac{1}{k} \sum\_{i=1}^k ACC\_i\)。

一旦计算出 *t* 统计量，我们就可以算出 p 值，并将其与选定的显著性水平（例如 \(\alpha=0.05\)）比较。如果 p 值小于 \(\alpha\)，我们就拒绝零假设，并接受两个模型之间存在显著差异。

这一方法的问题——也是不建议在实践中使用它的原因——在于它违背了 Student *t* 检验的假设：模型性能的差异并不服从正态分布，因为准确率不是独立的（我们在同一个测试集上计算它们）。此外，准确率之间的差异本身也不独立，因为重采样时各测试集相互重叠。因此，实践中不建议使用这一检验。不过，用于比较研究时，MLxtend 中实现了这一检验：[http://rasbt.github.io/mlxtend/user\_guide/evaluate/paired\_ttest\_resampled/](http://rasbt.github.io/mlxtend/user_guide/evaluate/ftest)。

## k 折交叉验证配对 t 检验

与重采样配对 t 检验类似，k 折交叉验证配对 t 检验是一种在（较早的）文献中非常常见的统计检验技术。虽然它解决了重采样配对 t 检验流程的部分缺陷，但这一方法仍然存在训练集相互重叠的问题，因此同样不建议在实践中使用（Diettrich, 1998）。

同样出于完整性考虑，该方法概述如下。其流程与重采样配对 t 检验基本等价，区别在于我们使用 k 折交叉验证而非简单重采样，这样在计算 \(t\) 值时，

\[t = \frac{ACC\_{avg} \sqrt{k}}{\sqrt{\sum\_{i=1}^{k}(ACC\_{i} - ACC\_{avg})^2 / (k-1)}},\]

\(k\) 等于交叉验证的轮数。同样，用于比较研究时，我通过 MLxtend 提供了这一检验流程的实现：<http://rasbt.github.io/mlxtend/user_guide/evaluate/paired_ttest_kfold_cv/>。

## Dietterich 的 5 \(\times\) 2 折交叉验证配对 t 检验

5x2cv 配对 *t* 检验是 Dietterich（Dietterich, 1998）提出的一种两模型（分类器或回归器）性能比较方法，用以弥补前两节概述的重采样配对 *t* 检验和 k 折交叉验证配对 *t* 检验等其他方法的不足。

虽然总体思路与前面介绍的 t 检验变体相似，但在 5x2cv 配对 *t* 检验中，我们把划分（50% 训练数据、50% 测试数据）精确重复五次。

在这 5 次迭代中的每一次里，我们把两个分类器 \(C\_1\) 和 \(C\_2\) 拟合到训练划分上，并在测试划分上评估其性能。然后，我们对调训练集与测试集（原训练集变成测试集，反之亦然），再次计算性能，得到两个性能差异度量：

\[ACC\_A = ACC\_{A, C\_1} - ACC\_{A, C\_2},\]

以及

\[ACC\_B = ACC\_{B, C\_1} - ACC\_{B, C\_2}.\]

然后，我们估计这些差异的均值与方差：

\[ACC\_{avg} = (ACC\_A + ACC\_B) / 2,\]

以及

\[s^2 = (ACC\_A - ACC\_{avg})^2 + (ACC\_B - ACC\_{avg}^2)^2.\]

差异的方差针对 5 次迭代分别计算，然后用于计算 *t* 统计量，如下所示：

\[t = \frac{ACC\_{A, 1}}{\sqrt{(1/5) \sum\_{i=1}^{5}s\_i^2}},\]

其中 \(ACC\_{A, 1}\) 是第一次迭代得到的 \(ACC\_{A}\)。

在「模型 \(C\_1\) 和 \(C\_2\) 性能相等」的零假设下，该 *t* 统计量近似服从自由度为 5 的 *t* 分布。利用 *t* 统计量可以计算 p 值，并与先前选定的显著性水平（例如 \(\alpha=0.05\)）比较。如果 p 值小于 \(\alpha\)，我们就拒绝零假设，接受两个模型之间存在显著差异。5x2cv 配对 *t* 检验在 MLxtend 中可用：<http://rasbt.github.io/mlxtend/user_guide/evaluate/paired_ttest_5x2cv/>。

## 组合 5x2cv F 检验

5x2cv 组合 *F* 检验是 Alpaydin（Alpaydin, 1999）提出的一种模型（分类器或回归器）性能比较方法，作为上一节介绍的 Dietterich 5x2cv 配对 *t* 检验的更稳健替代方案。

为了解释这一方法的机制，考虑分类器 1 和 2，并沿用上一节的记号。F 统计量计算如下：

\[\mathcal{f} = \frac{\sum\_{i=1}^{5} \sum\_{j=1}^2 (ACC\_{i,j})^2}{2 \sum\_{i=1}^5 s\_i^2},\]

它近似服从自由度为 10 和 5 的 F 分布。组合 5x2cv F 检验在 mlxtend 中可用：<http://rasbt.github.io/mlxtend/user_guide/evaluate/combined_ftest_5x2cv/>。

## 效应量

我们或许还应考虑效应量（effect size）——尽管遗憾的是实践中很少这么做——因为大样本会推高 p 值，可能让*一切*都显得具有统计显著性。换句话说，「理论显著性」并不等于「实际显著性」。由于效应量是一个相当依赖当前问题/任务/具体提问的议题，详细讨论显然超出了本文的范围。

## 嵌套交叉验证

在实际应用中，我们几乎从来没有条件拥有一个大型的（理想情况下是无限大的）测试集来为我们提供模型真实泛化误差的无偏估计。因此，我们总是在寻找处理规模受限数据集的「更好」变通办法：留给训练的数据太多，会导致泛化性能估计不可靠；留给测试的数据太多，训练数据又太少，从而损害模型性能。

此外，对于给定的问题或问题域，我们几乎总是不知道学习算法的理想设置。因此，我们需要用现有的训练集来做超参数调优和模型选择。前面我们已经确定，可以用 k 折交叉验证来完成这些任务。然而，如果我们基于平均 k 折性能或*同一个*测试集来选择「最佳超参数设置」，就会给流程引入偏差，模型性能估计也就不再无偏了。关键在于，我们可以把模型选择看作另一种*训练*过程，因此要得到模型性能的无偏估计，就需要一个规模可观、且此前未见过的独立测试集。而这往往是负担不起的。

近年来，一种称为「嵌套交叉验证」（nested cross-validation）的技术已成为比较机器学习算法的流行且多少被推荐的方法之一；它很可能最早由 Iizuka（Iizuka et al., 2003）以及 Varma 和 Simon（Varma and Simon, 2006）在处理小数据集时提出。嵌套交叉验证为小数据集场景提供了一种变通方案，在无法预留数据构建独立测试集的情况下，实践中表现出的偏差较低。

Varma 和 Simon 发现，与常规 k 折交叉验证（同时用于超参数调优和评估时）相比，嵌套交叉验证方法可以显著降低偏差。正如研究者所言：「嵌套交叉验证流程提供了对真实误差几乎无偏的估计」（Varma and Simon, 2006）。

嵌套交叉验证的方法相对直观，它只是两个 k 折交叉验证循环的嵌套：内循环负责模型选择，外循环负责估计泛化准确率，如下图所示。

![Model evaluation selection part4 nested cv](https://sebastianraschka.com/images/blog/2018/model-evaluation-selection-part4/nested-cv.webp)

注意，在这个具体例子里，这是一个 5x2 的设置（外循环 5 折交叉验证，内循环 2 折交叉验证）。然而这与 Dietterich 的 5x2cv 方法并不是一回事，这是一个经常被混淆的情形，所以我想在这里特别强调。

在 scikit-learn（Pedegrosa et al., 2011）中使用嵌套交叉验证的代码可在此找到：<https://github.com/rasbt/model-eval-article-supplementary/blob/master/code/nested_cv_code.ipynb>。

## 结语

由于「一图胜千言」，我想用下面这幅图来结束这一关于模型评估、模型选择与算法选择的系列文章，它基于所回顾的概念和文献总结了我的个人建议。

![Model evaluation selection part4 model eval conclusions](https://sebastianraschka.com/images/blog/2018/model-evaluation-selection-part4/model-eval-conclusions.webp)

在上图中，缩写「MC」代表「模型比较」（Model Comparison），「AC」代表「算法比较」（Algorithm Comparison），用以区分这两类任务。需要强调的是，用于比较模型性能的参数检验通常会违背一个或多个独立性假设（模型之间不独立，因为使用了同一个训练集；估计的泛化性能之间也不独立，因为使用了同一个测试集）。在理想世界里，我们可以获得数据生成分布，或至少是几乎无限的新数据池。然而在大多数实际应用中，数据集的规模是有限的；因此，我们可以把本文讨论的某种统计检验当作启发式方法来辅助决策。

需要注意，我在上图中列出的建议仅供参考，并取决于当前的问题。例如，大型测试数据集（「大」是相对的，可能指数千或数百万条数据记录）能够提供可靠的泛化性能估计；而当只有少量数据记录可用时，使用单一的训练集和测试集则可能因[第二部分](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part2.html)和[第三部分](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part3.html)中讨论的若干原因而产生问题。如果数据集非常小，可能无法预留数据用于测试；在这种情况下，我们可以使用较大 *k* 的 k 折交叉验证或留一交叉验证（Leave-one-out cross-validation）作为评估泛化性能的变通办法。但使用这些流程时必须牢记：此时我们比较的不是模型，而是在训练折上产出不同模型的不同算法。尽管如此，各测试折上的平均性能仍可作为泛化性能的估计（[第三部分](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part3.html)讨论了这一估计的偏差与方差随折数变化的种种影响）。

对于模型比较，我们通常没有多个独立测试集来评估模型，因此可以再次求助于交叉验证流程，例如 k 折交叉验证、5x2cv 方法或嵌套交叉验证。正如 Gael Varoquaux 所写：

> "Cross-validation is not a silver bullet. However, it is the best tool available, because it is the only non-parametric method to test for model generalization." (Varoquaux, 2017)

最后，希望这个系列文章对你有所帮助。如果你有任何问题或疑虑，请随时联系我——毕竟这只是一篇博客文章，并不意味着我们不能做出调整 :)。

感谢阅读。如果你喜欢这些内容，也可以在 [Twitter 上找到我](https://twitter.com/rasbt)，我在那里分享更多有用的内容。

## 参考文献

- Alpaydin, Ethem. “Combined 5x2 cv F test for comparing supervised classification learning algorithms.” *Neural computation* 11, no. 8 (1999): 1885-1892.
- Bonferroni, Carlo E. “Teoria statistica delle classi e calcolo delle probabilita.” *Libreria internazionale Seeber*, 1936.
- Cochran, William G. “The comparison of percentages in matched samples.” *Biometrika* 37, no. 3/4 (1950): 256-266.
- Dietterich, Thomas G. “Approximate statistical tests for comparing supervised classification learning algorithms.” *Neural computation* 10, no. 7 (1998): 1895-1923.
- Dunn, Olive Jean. “Multiple comparisons among means.” *Journal of the American Statistical Association* 56.293 (1961): 52-64.
- Edwards, Allen L. “Note on the “correction for continuity” in testing the significance of the difference between correlated proportions.” *Psychometrika* 13.3 (1948): 185-187.
- Fleiss, Joseph L., Bruce Levin, and Myunghee Cho Paik. Statistical methods for rates and proportions. John Wiley & Sons, 2013.
- Iizuka, Norio, Masaaki Oka, Hisafumi Yamada-Okabe, Minekatsu Nishida, Yoshitaka Maeda, Naohide Mori, Takashi Takao et al. “Oligonucleotide microarray for prediction of early intrahepatic recurrence of hepatocellular carcinoma after curative resection.” *The Lancet* 361, no. 9361 (2003): 923-929.
- Kuncheva, Ludmila I. Combining pattern classifiers: methods and algorithms. John Wiley & Sons, 2004.
- Looney, Stephen W. “A statistical technique for comparing the accuracies of several classifiers.” *Pattern Recognition Letters*8, no. 1 (1988): 5-9.
- McNemar, Quinn. “Note on the sampling error of the difference between correlated proportions or percentages.” *Psychometrika* 12.2 (1947): 153-157.
- Neyman, Jerzy, and Egon S. Pearson. “On the use and interpretation of certain test criteria for purposes of statistical inference: Part I.” *Biometrika* (1928): 175-240.
- Pedregosa, Fabian, Gaël Varoquaux, Alexandre Gramfort, Vincent Michel, Bertrand Thirion, Olivier Grisel, Mathieu Blondel, et al. “Scikit-learn: Machine learning in Python.” *Journal of Machine Learning Research* 12, no. Oct (2011): 2825-2830.
- Perneger, Thomas V. “What's wrong with Bonferroni adjustments.” *BMJ: British Medical Journal* 316.7139 (1998): 1236.
- Raschka, Sebastian. “MLxtend: Providing machine learning and data science utilities and extensions to Python's scientific computing stack.” *The Journal of Open Source Software* 3, no. 24 (2018).
- Rothman, Kenneth J. “No adjustments are needed for multiple comparisons.” *Epidemiology* 1.1 (1990): 43-46.
- Varma, Sudhir, and Richard Simon. “Bias in error estimation when using cross-validation for model selection.” *BMC bioinformatics* 7, no. 1 (2006): 91.
- Varoquaux, Gael. “Cross-validation failure: small sample sizes lead to large error bars.” Neuroimage (2017).
- Westfall, Peter H., James F. Troendle, and Gene Pennello. “Multiple McNemar tests.” *Biometrics* 66.4 (2010): 1185-1191.
