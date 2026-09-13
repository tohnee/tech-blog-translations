---
title: "机器学习模型评估：第 2 部分"
title_en: "ML Model Evaluation: Part 2"
source: https://sebastianraschka.com/blog/2016/model-evaluation-selection-part2.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 机器学习模型评估：第 2 部分

> 原文：[ML Model Evaluation: Part 2](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part2.html)

**模型评估第 1–4 部分的单 PDF 合订版已发布在 arXiv 上：<https://arxiv.org/abs/1811.12808>**

## 引言

在上一篇文章（[第 1 部分](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part1.html)）中，我们介绍了监督式机器学习中模型评估背后的一般思想。我们讨论了留出法（holdout method），它帮助我们应对现实世界的限制，例如难以获取新的、带*标签*的数据用于模型评估。使用留出法时，我们把数据集划分为两部分：训练集和测试集。首先，我们把训练数据提供给一个监督学习算法；学习算法基于这批带标签的观测样本构建出一个模型。然后，我们在一个独立的测试集上评估该模型的预测性能，这个测试集应当代表新的、模型未曾见过的数据。此外，我们还简要介绍了*正态近似*（normal approximation）：通过某些假设，我们可以基于单一测试集为性能估计的不确定性计算置信区间——当然，这样的估计要打几分折扣来看待。

在本文中，我们将讨论一些更高级的模型评估技术。我们会先讨论如何估计模型性能估计值的不确定性，以及模型本身的方差与稳定性。在掌握这些基础知识之后，我们将在本系列的下一篇文章中讨论用于模型选择的交叉验证技术。回顾第 1 部分的内容，我们关心模型评估的原因有三个，它们相互关联但又各不相同：

1. 我们想要估计模型的泛化准确率，即模型在未来的（未见过的）数据上的预测性能。
2. 我们想要通过调整学习算法、并从给定的假设空间中选出表现最好的模型，来提升预测性能。
3. 我们想要找出最适合当前问题的机器学习算法；也就是说，我们希望比较不同的算法，选出表现最好的那一个，并从该算法的假设空间中选出表现最好的模型。

（生成本文图表的代码可以在 [GitHub](https://github.com/rasbt/pattern_classification/blob/master/data_viz/model-evaluation-articles/model-eval-kfold.ipynb) 上的 Jupyter notebook 中找到。）

## 重采样

在本系列的[第一部分](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part1.html)中，我们讨论了分类模型的预测准确率或预测误差。要在数据集 *S* 上计算分类误差或准确率，我们定义了如下公式

\[\text{ERR}\_S = \frac{1}{n} \sum\_{i=1}^{n} L\big(\hat{y}\_i, y\_i \big) = 1 - \text{ACC}\_S.\]

其中，\(L(\cdot)\) 表示 0-1 损失，它由预测类别标签 \(\hat{y}\_i\) 和真实标签 \(y\_i\) 在数据集 *S* 的全部 *n* 个样本上计算得出：

\[L(\hat{y\_i}, y\_i) :=
\begin{cases}
0 &\text{if } \hat{y\_i} = y\_i \\\\
1 &\text{if } \hat{y\_i} \neq y\_i.
\end{cases}\]

从本质上说，分类误差就是预测错误的数量除以数据集中的样本数；反过来，预测准确率则是预测正确的数量除以样本数。

注意，本文介绍的概念同样适用于其他类型的监督学习，例如回归分析。要使用接下来几节介绍的重采样方法，我们只需把基于预测准确率或误差的准确率/误差计算换成均方误差（MSE）：

\[MSE\_S = \frac{1}{n} \sum\_{i=1}^{n} ( \hat{y}\_i - y\_i)^2.\]

正如我们在[第 1 部分](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part1.html)中学到的，我们的性能估计可能受到偏差和方差的影响，我们要寻找的是二者之间的良好折中。举例来说，再代入评估（resubstitution evaluation，即在训练集上拟合模型，再用同一个训练集评估模型）会带来严重的乐观偏差；反过来，把数据集中的很大一部分留作测试集，则可能导致悲观偏差的估计。虽然缩小测试集可以降低这种悲观偏差，但性能估计的方差很可能会随之增大。在本文中，我们将考察一些替代性的重采样方法，以便在模型评估与选择中找到偏差与方差之间的良好平衡。

![Model evaluation selection part2 visual bias variance](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part2/visual_bias_variance.webp)

测试集占比过大会增加悲观偏差，原因在于模型此时可能还没有达到其全部容量。换句话说，如果学习算法见到更多数据，它本可以归纳出一个更强大、更具泛化能力的分类假设。为了演示这一效应，我绘制了 [softmax 分类器](http://rasbt.github.io/mlxtend/user_guide/classifier/SoftmaxRegression/)的学习曲线，它们是在 [MNIST](http://yann.lecun.com/exdb/mnist/) 的小规模子集上拟合得到的：

![Model evaluation selection part2 model eval mnist 0](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part2/model-eval-mnist_0.webp)

为了生成上图，我从 MNIST 的十个类别中各随机抽取了 500 个样本——即手写数字 0 到 9 的实例。随后，这个 5000 样本的 MNIST 子集被随机划分为一个 3500 样本的训练子集和一个包含 1500 个样本的测试集，并通过分层（stratification）保持类别比例不变。最后，我又通过随机的分层切分，从 3500 样本的训练集中生成了更小的子集，用这些子集拟合 softmax 分类器，并用同一个 1500 样本的测试集评估它们的性能；这些训练子集之间的样本可能存在重叠。观察上图，我们可以看到两个明显的趋势：第一，再代入准确率（训练集）随训练样本数量的增加而下降；第二，泛化准确率（测试集）随训练集规模的增大而提升。这些趋势很可能要归因于过拟合的减少。当训练集很小时，算法更容易学到训练集中的噪声，导致模型无法很好地泛化到未曾见过的数据上。这一观察也解释了留出法的悲观偏差：训练算法本可以从更多的训练数据中获益，而这些数据却被我们留作测试之用了。因此，在完成模型评估之后，我们应当在使用它投入真实应用之前，再次在完整数据集上运行学习算法。

既然我们已经说明了"测试集占比过大导致悲观偏差"这一点，那么自然会问：缩小测试集是不是一个好主意？缩小测试集又会带来另一个问题：它可能使模型性能估计产生很大的方差。原因在于，估计结果取决于哪些实例落入训练集、哪些特定实例落入测试集。要记住，每次对数据重新采样，我们都会改变样本分布的统计特性。大多数用于分类和回归的监督学习算法，以及我们的性能估计，都建立在"数据集能够代表它所抽自的总体"这一假设之上。正如我们在[第 1 部分](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part1.html)中学到的，分层有助于在划分数据集时保持样本比例不变。然而，特征轴上底层样本统计特性的变化仍然是一个问题，而且当我们处理小数据集时会变得更加突出。下面的图示说明了这一点，其中我对一个二维高斯分布进行了反复子采样。

![Model evaluation selection part2 resampling gauss](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part2/resampling_gauss.webp)

## 重复留出验证

要获得更稳健、对"数据如何划分为训练集与测试集"不那么敏感的性能估计，一种办法是把留出法用不同的随机种子重复 *k* 次，然后计算这 *k* 次重复的平均性能

\[\text{ACC}\_{avg} = \frac{1}{k} \sum^{k}\_{j=1} {ACC\_j},\]

其中 \(\text{ACC}\_j\) 是第 *j* 个大小为 *m* 的测试集上的准确率估计值，

\[\text{ACC}\_j = 1 - \frac{1}{m} \sum\_{i=1}^{m} L\big(\hat{y}\_i, y\_i \big).\]

这种重复留出流程，有时也被称为*蒙特卡洛交叉验证*（Monte Carlo Cross-Validation），能更好地估计模型在随机测试集上的表现，同时也能让我们对模型的稳定性有所了解——即学习算法在不同训练集划分下产生的模型会如何变化。下图展示了使用 [Iris](https://archive.ics.uci.edu/ml/datasets/Iris) 数据集拟合 3 近邻分类器时，不同的训练/测试划分下重复留出验证可能呈现的样子。

![Model evaluation selection part2 model eval iris](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part2/model-eval-iris.webp)

为了生成左边的子图，我进行了 50 次分层训练/测试划分，每次测试集和训练集各含 75 个样本；在每次重复中，都在训练集上拟合一个 K 近邻模型，并在测试集上评估。这 50 次 50/50 划分的平均准确率为 95%。我按照同样的流程生成了右边的子图，不过这里重复进行的是 90/10 划分，因此测试集只包含 15 个样本。这一次，50 次划分的平均准确率为 96%。回到上图：它确实印证了我们此前讨论过的两个要点。第一，随着测试集规模减小，估计值的方差增大。第二，当我们缩小训练集时，悲观偏差出现了小幅上升——在 50/50 划分中我们扣留了更多训练数据，这也许可以解释为什么 50 次划分的平均性能略低于 90/10 划分。

下一节中，我们将考察另一种评估模型性能的方法；我们将讨论自助法（bootstrap）的几种常见变体，它们常用于推断性能估计的不确定性。

## 自助法与经验置信区间

前面蒙特卡洛交叉验证的例子也许已经让我们相信：与基于单一训练/测试划分的评估相比，重复留出验证能够为我们提供更稳健的模型性能估计。此外，重复留出还能让我们对模型的稳定性有所了解。在本节中，我们将探索另一种模型评估方法，并使用自助法（bootstrap）计算其不确定性。

假设我们想为性能估计计算一个置信区间，以判断它的确定性——或者说不确定性。如果我们的样本抽自一个未知分布，该如何做到这一点？也许我们可以用样本均值作为总体均值的点估计，但如果均值的分布未知，我们又该如何计算它的方差或置信区间？当然，我们可以采集多个独立的样本；但在现实应用中，我们往往没有这种奢侈的条件。自助法的思想是：通过从一个经验分布中抽样来生成"新样本"。顺带一提，"bootstrap"一词很可能源自短语"to pull oneself up by one's bootstraps"（拽着自己的靴带把自己提起来）：

> 大约在 1900 年，"to pull (oneself) up by (one's) bootstraps" 被用来比喻不可能完成的任务（在 Steele 的教科书《Popular Physics》（1888）第一章末尾的"实际问题"中，有这样一道题："30. 人为什么不能靠拽自己的靴带把自己提起来？"）。到 1916 年，它的含义扩展为"通过艰苦的、不依靠外力的努力来提升自己"。而"加载计算机操作系统的一串固定指令"这一含义（1953 年）则来自"最先加载的程序靠自己（以及后续程序）沿着靴带被拉起来"这一意象。

（来源：[Online Etymology Dictionary](http://www.etymonline.com/index.php?allowed_in_frame=0&search=bootstrap)）

自助法是一种用于估计抽样分布（sampling distribution）的重采样技术。就本文而言，我们特别关心的是估计性能估计值——预测准确率或误差——的不确定性。自助法由 Bradley Efron 于 1979 年提出（Efron, 1979）。大约 15 年后，Bradley Efron 和 Robert Tibshirani 甚至为自助法专门写了一整本书——《An Introduction to the Bootstrap》（Efron and Tibshirani, 1994），如果你对这个话题的更多细节感兴趣，我推荐你阅读。简而言之，自助法的思想是：通过对原始数据集进行*有放回*的重复抽样来从总体中生成*新*数据——相比之下，重复留出法可以理解为*无*放回抽样。逐步展开来看，自助法的工作方式如下：

1. 我们有一个大小为 *n* 的数据集。
2. 进行 *b* 轮自助抽样：
   1. 我们从这个数据集中抽取一个实例，放入第 *j* 个自助样本。重复这一步，直到自助样本的大小达到 *n*——与原始数据集相同。由于每次都是从同一个原始数据集中抽样，某些样本可能在自助样本中出现多次，而另一些则可能完全不出现在其中。
3. 我们在 *b* 个自助样本上分别拟合模型，并计算再代入准确率（resubstitution accuracy）。
4. 我们把模型准确率取为这 *b* 个准确率估计值的平均

\[\text{ACC}\_{boot} = \frac{1}{b} \sum\_{j=1}^b \frac{1}{n} \sum\_{i=1}^{n} \bigg( 1 - L\big(\hat{y}\_i, y\_i \big) \bigg).\]

正如前面讨论过的，再代入准确率通常会导致极度乐观的偏差，因为模型可能对数据集中的噪声过度敏感。自助法原本的目的，是在底层分布未知、且无法获得额外样本时确定某个估计量的统计性质。因此，为了把这一方法用于预测模型（例如分类和回归假设）的评估，我们可能更倾向于一种略有不同的自助法变体，即所谓的*留一自助法*（Leave-One-Out Bootstrap，LOOB）。在这里，我们使用*袋外*（out-of-bag）样本作为评估用的测试集，而不是在训练数据上评估模型。袋外样本是那些未被用于模型拟合的、各不相同的实例集合，如下图所示。

![Model evaluation selection part2 bootrap concept](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part2/bootrap_concept.webp)

上图展示了从一个含有 10 个样本的示例数据集（\(X\_1, X\_2, \dots X\_{10}\)）中抽取三个随机自助样本，以及它们用于测试的袋外样本可能的样子。在实践中，Bradley Efron 和 Robert Tibshirani 建议抽取 50 到 200 个自助样本即可获得可靠的估计（Efron and Tibshirani, 1993）。

让我们退一步，假设有一个样本抽自正态分布 \(N(\mu, \sigma^2)\)，其中均值 \(\mu\) 和方差 \(\sigma^2\) 未知。距离上统计学入门课可能已经有一段时间了，但如果有一件事我们肯定还记得，那就是可以用样本均值 \(\bar{x}\) 作为 \(\mu\) 的点估计，

\[\bar{x} = \frac{1}{n} \sum\_{i=1}^{n} x\_i,\]

并且可以把方差 \(\sigma^2\) 估计为

\[\text{VAR} = \frac{1}{n-1} \sum\_{i=1}^{n} (x\_i - \bar{x})^2.\]

于是，我们计算标准差为 \(\text{SD} = \sqrt{\text{VAR}},\)
并计算标准误为

\[\text{SE} = \frac{\text{SD}}{\sqrt{n}}.\]

利用标准误，我们可以按照下式计算均值的 95% 置信区间

\[\bar{x} \pm z \times \frac{\sigma}{\sqrt{n}},\]

即

\[\bar{x} \pm t \times \text{SE}\]

其中 95% 置信区间对应 z=1.96。由于我们是从样本中估计 SD 的，因此必须查 t 表来获得 *t* 的实际取值，它取决于样本的大小——更准确地说，取决于*自由度*。例如，给定一个 n=100 的样本，我们可以查得 \(t\_{95} = 1.984\)。

类似地，我们可以计算自助估计值的 95% 置信区间

\[\text{ACC}\_{boot} = \frac{1}{b} \sum\_{i=1}^{b} \text{ACC}\_i\]

并用它来计算标准误

\[\text{SE}\_{boot} = \sqrt{ \frac{1}{b-1} \sum\_{i=1}^{b} (\text{ACC}\_i - \text{ACC}\_{boot})^2 }.\]

其中，\(\text{ACC}\_i\) 是在第 *i* 个自助副本上计算得到的统计量（ACC 的估计值）的取值。而 \(\text{ACC}\_1, \text{ACC}\_1, ..., \text{ACC}\_b\) 这些取值的标准差（如上计算）就是 ACC 标准误的估计（Efron and Tibshirani, 1994, pp. 12-13）。

最后，我们可以围绕均值估计计算置信区间

\[\text{ACC}\_{boot} \pm t \times \text{SE}\_{boot}.\]

尽管上面概述的方法看起来很直观，但如果我们的样本*并不*服从正态分布，该怎么办呢？一种更稳健、同时在计算上也很直截了当的方法是 B. Efron 描述的百分位数法（Efron, 1981）。这里，我们按如下方式选取置信下界和上界：

- \(\text{ACC}\_{lower} = \text{ACC}\_\text{boot}\) 分布的 \(\alpha\_{1}\) 百分位数
- \(\text{ACC}\_{upper} = \text{ACC}\_{boot}\) 分布的 \(\alpha\_{2}\) 百分位数

其中 \(\alpha\_1 = \alpha\)，\(\alpha\_2 = 1 - \alpha\)，而 \(\alpha\) 是我们的置信度，用来计算 \(100 \times (1 - 2 \times \alpha)\) 置信区间。例如，要计算 95% 置信区间，我们取 \(\alpha = 0.025\)，从而获得 *b* 个自助样本分布的第 2.5 和第 97.5 百分位数作为置信下界和上界。

在实践中，如果我们的数据确实（大致）服从正态分布，那么"标准"置信区间与百分位数法的结果通常是一致的，如下图所示。

![Model evaluation selection part2 bootstrap histo](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part2/bootstrap-histo.webp)

在左边的子图中，我用*留一自助法*（Leave-One-Out Bootstrap）在 Iris 上评估了 3 近邻模型；右边的子图则展示了在 MNIST 上采用同样评估方法的结果，使用的是我们前文讨论过的同一个 softmax 算法。

1983 年，Bradley Efron 描述了 *.632 估计*（.632 Estimate），这是对上述自助交叉验证方法的悲观偏差的进一步改进（Efron, 1983）。“经典”自助法中的悲观偏差可以归因于这样一个事实：自助样本仅包含原始数据集中大约 63.2% 的不重复样本。例如，我们可以计算大小为 *n* 的数据集中某个给定样本*不*被抽入某个自助样本的概率

\[P (\text{not chosen}) = \bigg(1 - \frac{1}{n}\bigg)^n,\]

当 \(n \rightarrow \infty.\) 时，它渐近等价于 \(\frac{1}{e} \approx 0.368\)。

反过来，我们可以计算一个样本*被*选中的概率

\[P (\text{chosen}) = 1 - \bigg(1 - \frac{1}{n}\bigg)^n \approx 0.632\]

对于规模足够大的数据集成立，因此在每轮迭代中，我们大约会选出 \(0.632 \times n\) 个不重复样本作为自助训练集，并保留 \(0.368 \times n\) 个袋外样本用于测试。

![Model evaluation selection part2 bootstrap prob](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part2/bootstrap_prob.webp)

现在，为了解决这种有放回抽样带来的偏差，Bradley Efron 提出了我们前文提到的 *.632 估计*，它通过如下公式计算：

\[\text{ACC}\_{boot} = \frac{1}{b} \sum\_{i=1}^b \big(0.632 \cdot \text{ACC}\_{h, i} + 0.368 \cdot \text{ACC}\_{r, i}\big),\]

其中 \(\text{ACC}\_{r, i}\) 是再代入准确率，\(\text{ACC}\_{h, i}\) 是袋外样本上的准确率。

虽然 *.632 自助法*试图解决估计的悲观偏差，但对于容易过拟合的模型，可能出现乐观偏差，于是 Bradley Efron 和 Robert Tibshirani 提出了 *.632+ 自助法*（Efron and Tibshirani, 1997）。与在下式中使用固定的"权重" \(\omega = 0.632\) 不同，

\[ACC\_{\text{boot}} = \frac{1}{b} \sum\_{i=1}^b \big(\omega \cdot \text{ACC}\_{h, i} + (1-\omega) \cdot \text{ACC}\_{r, i} \big),\]

我们把权重 \(\gamma\) 计算为

\[\omega = \frac{0.632}{1 - 0.368 \times R},\]

其中 *R* 是*相对过拟合率*（relative overfitting rate）

\[R = \frac{(-1) \times (\text{ACC}\_{h, i} - \text{ACC}\_{r, i})}{\gamma - (1 -\text{ACC}\_{h, i})}.\]

（由于我们把 \(\omega\) 代入上文的 \(ACC\_{boot}\) 计算公式，\(\text{ACC}\_{h, i}\) 和 \(\text{ACC}\_{r, i}\) 仍分别指第 *i* 轮自助抽样中的再代入准确率与袋外准确率估计。）

此外，我们还需要确定*无信息率*（no-information rate）\(\gamma\) 才能计算 *R*。例如，我们可以通过在一个包含样本 \(x\_{i'}\) 与目标类别标签 \(y\_{i}\) 之间所有可能组合的数据集上拟合模型来计算 \(\gamma\)——即假装观测样本与类别标签是相互独立的：

\[\gamma = \frac{1}{n^2} \sum\_{i=1}^{n} \sum\_{i '=1}^{n} L(y\_{i}, f(x\_{i '})).\]

或者，我们可以按如下方式估计无信息率 \(\gamma\)：

\[\gamma = \sum\_{k=1}^K p\_k (1 - q\_k),\]

其中 \(p\_k\) 是数据集中观测到的第 *k* 类样本所占的比例，\(q\_k\) 是分类器在数据集中预测为第 *k* 类的样本所占的比例。

感谢阅读。如果你喜欢这些内容，也可以[在 Twitter 上关注我](https://twitter.com/rasbt)，我在那里分享更多有用的内容。

## 下一步

在本文中，我们更详细地继续讨论了机器学习模型评估中的偏差与方差问题。我们谈到了重复留出法，它可以让我们进一步洞察模型的稳定性。然后，我们考察了自助法——一种从统计学领域借鉴而来的技术。我们探索了自助法的几种变体，它们帮助我们估计性能估计值的不确定性。在[第 1 部分](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part1.html)和[第 2 部分](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part2.html)打好模型评估的基础之后，我们将在接下来的[第 3 部分](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part3.html)和[第 4 部分](https://sebastianraschka.com/blog/2018/model-evaluation-selection-part4.html)中处理更有意思的任务：超参数调优与模型选择。

## 参考文献

- Efron, Bradley. 1979. “Bootstrap Methods: Another Look at the Jackknife.” *The Annals of Statistics* 7 (1). Institute of Mathematical Statistics: 1–26. doi:10.1214/aos/1176344552.
- Efron, Bradley. 1981. “Nonparametric Standard Errors and Confidence Intervals.” *Canadian Journal of Statistics* 9 (2). Wiley‐Blackwell: 139–58. doi:10.2307/3314608.
- Efron, Bradley. 1983. “Estimating the Error Rate of a Prediction Rule: Improvement on Cross-Validation.” *Journal of the American Statistical Association* 78 (382): 316. doi:10.2307/2288636.
- Efron, Bradley, and Robert Tibshirani. 1994. *An Introduction to the Bootstrap*. Chapman & Hall.
- Efron, Bradley, and Robert Tibshirani. 1997. “Improvements on Cross-Validation: The .632+ Bootstrap Method.” *Journal of the American Statistical Association* 92 (438): 548. doi:10.2307/2965703.
