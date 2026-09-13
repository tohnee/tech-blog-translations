---
title: "机器学习模型评估：第三部分"
title_en: "ML Model Evaluation: Part 3"
source: https://sebastianraschka.com/blog/2016/model-evaluation-selection-part3.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 机器学习模型评估：第三部分

> 原文：[ML Model Evaluation: Part 3](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part3.html)

**模型评估第 1-4 部分的单 PDF 合订版可在 arXiv 获取：<https://arxiv.org/abs/1811.12808>**

## 引言

几乎每一种机器学习算法都带有大量需要我们——机器学习研究者和从业者——手动指定的配置项。这些调节旋钮，也就是所谓的超参数，让我们能够在优化性能、寻找偏差与方差之间恰当平衡时控制机器学习算法的行为。面向性能优化的超参数调优本身就是一门艺术，没有任何硬性规则能够保证在给定数据集上取得最佳性能。在[第一部分](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part1.html)和[第二部分](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part2.html)中，我们了解了用于估计模型泛化性能的各种留出法（holdout）与自助法（bootstrap）技术，学习了偏差-方差权衡，并计算了估计值的不确定性。在这第三部分中，我们将聚焦用于模型评估和模型选择的各类交叉验证方法，并利用这些交叉验证技术对来自多组超参数配置的模型进行排序，估计它们在独立数据集上的泛化能力。

## 关于超参数与模型选择

在前面的部分中，我们使用*留出法*（holdout method）或*自助法*（bootstrapping）的各种变体来估计预测模型的泛化性能。我们把数据集划分为两部分：训练集和测试集。在机器学习算法对训练集拟合出模型之后，我们在模型拟合阶段对算法屏蔽、未参与建模的独立测试集上评估模型。在讨论*偏差-方差权衡*等挑战的过程中，我们在学习算法中使用了固定的*超参数设置*，例如*K 近邻*（K-nearest neighbors）算法中的 *k* 值。我们把*超参数*定义为学习算法本身的参数，必须在模型拟合*之前先验地*（a priori）指定；与之相对，我们把最终所得模型的参数称为*模型参数*。

那么，超参数究竟是什么？以*k 近邻*算法为例，超参数的一个例子就是整数 *k*。如果设 *k=3*，k 近邻算法会根据训练集中 3 个最近邻的多数投票来预测类别标签。而寻找这些最近邻所用的距离度量则是该算法的另一个超参数。

![模型评估与选择第三部分 kNN](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part3/knn.webp)

不过，用 k 近邻算法来说明超参数与模型参数的区别可能并非理想之选，因为它是一种*惰性*（lazy）学习器，也是一种非参数方法。在这里，*惰性学习*（lazy learning，或称*基于实例的学习*，instance-based learning）意味着不存在训练或模型拟合阶段：k 近邻模型会原封不动地存储（记忆）训练数据，只在预测时才使用它。因此，在 k 近邻模型中，每个训练实例本身就是一个"参数"。简言之，非参数模型就是无法用一组固定数量、随训练集调整的参数来描述的模型；这类模型的结构由训练数据决定，而不是事先设定。与参数方法不同，非参数模型不假设数据服从特定的概率分布（做出此类假设的非参数方法属于例外，如*贝叶斯非参数*方法）。因此，可以说非参数方法对数据所做的假设比参数方法更少。

与 k 近邻相对，*参数*方法的一个简单例子是*逻辑回归*（logistic regression）——一种广义线性模型，其模型参数数量是*固定的*：数据集中每个特征变量对应一个权重系数，外加一个偏置（或截距）单元。逻辑回归中的这些权重系数即模型参数，通过最大化对数似然函数或最小化 logistic 损失来更新。在将模型拟合到训练数据时，逻辑回归算法的一个超参数可以是基于梯度的优化中的迭代次数，或遍历训练集的次数（epoch 数）。超参数的另一个例子是正则化参数的取值，例如 L2 正则化逻辑回归中的 *lambda* 项：

![模型评估与选择第三部分 逻辑回归](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part3/logistic-regression.webp)

在训练集上运行学习算法时，改变超参数的取值可能得到不同的模型。从由不同超参数设置产生的一组模型中找出表现最佳模型的过程，称为*模型选择*（model selection）。下一节我们将介绍留出法的一种扩展，它能帮助我们完成这一选择过程。

## 用于超参数调优的三路留出法

在[第一部分](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part1.html)中，我们了解到*代入验证*（resubstitution validation）是估计泛化性能的糟糕做法。由于我们想知道模型对新数据的泛化能力如何，我们用留出法把数据集划分为两部分：训练集和独立测试集。那么，能否用留出法来做超参数调优？答案是"可以！"，但必须对最初"二分"的做法稍作修改，把数据集划分为三部分：训练集、验证集和测试集。

我们可以把超参数调优和模型选择的过程视为一项元优化（meta-optimization）任务：学习算法在训练集上优化目标函数（*惰性*学习器除外），而超参数优化是叠加在其之上的另一层任务——此时我们通常要优化的是某个性能指标，例如分类准确率或 ROC 曲线（Receiver Operating Characteristic curve）下面积。调优阶段结束后，基于测试集性能来选择模型看似合理，但多次复用测试集会给最终的性能估计引入偏差，很可能导致对泛化性能的过度乐观估计——我们可以说"测试集泄露了信息"。为避免这个问题，我们可以采用三路划分，把数据集分为训练集、验证集和测试集。用"训练-验证"这一对数据集来做超参数调优和模型选择，就能让测试集在模型评估时保持"独立性"。现在，还记得我们讨论过的性能估计的"三大目标"吗？

1. 我们想估计泛化准确率，即模型在未来（未见过）数据上的预测性能。
2. 我们想通过调整学习算法、从给定假设空间中选出表现最佳的模型，来提高预测性能。
3. 我们想找出最适合当前问题的机器学习算法；也就是说，我们想比较不同的算法、选出表现最佳的那个，并从该算法的假设空间中选出表现最佳的模型。

"三路留出法"是应对目标 1 和目标 2 的一种方式（目标 3 将在下一篇文章，即第四部分中详述）。不过，如果我们只关心目标 2——选出最佳模型——而不那么在意泛化性能的"无偏"估计，那么用二分划分来做模型选择也未尝不可。回想[第二部分](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part2.html)中关于学习曲线和悲观偏差的讨论：机器学习算法通常能从更多带标签数据中受益；数据集越小，悲观偏差和方差——即模型对数据划分方式的敏感度——就越大。

"天下没有免费的午餐。"用于超参数调优和模型选择的三路留出法并不是完成这一任务的唯一方法——而且往往也不是最好的方法。在后面的章节中，我们会学习其他替代方法并讨论它们的优势与取舍。不过，在进入可能是最受欢迎的模型选择方法——*k 折交叉验证*（k-fold cross-validation，在较早的文献中有时也称"轮换估计"，rotation estimation）——之前，先来看一下三路划分留出法的图示：

![模型评估与选择第三部分 留出验证](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part3/holdout-validation.webp)

这张图信息量很大，我们一步步来看。

![模型评估与选择第三部分 留出验证 01](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part3/holdout-validation_01.webp)

第一步，我们把数据集划分为三部分：用于模型拟合的训练集、用于模型选择的验证集，以及用于对最终选中模型做评估的测试集。

![模型评估与选择第三部分 留出验证 02](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part3/holdout-validation_02.webp)

第二步展示了超参数调优阶段。我们用不同的超参数设置（*此处为*三种）运行学习算法，在训练数据上拟合模型。

![模型评估与选择第三部分 留出验证 03](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part3/holdout-validation_03.webp)

接下来，我们在验证集上评估各模型的性能。这一步对应模型选择阶段：比较各性能估计之后，我们选择与最佳性能相对应的超参数设置。注意，实践中我们常常把第二、三步合并：先拟合一个模型并计算其性能，再进入下一个模型，以免把所有拟合好的模型都保存在内存中。

![模型评估与选择第三部分 留出验证 04](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part3/holdout-validation_04.webp)

正如[第一部分](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part1.html)和[第二部分](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part2.html)所讨论的，如果训练集太小，我们的估计可能带有悲观偏差。因此，模型选择完成后，我们可以合并训练集与验证集，并用上一步得到的*最佳*超参数设置在这个更大的数据集上拟合模型。

![模型评估与选择第三部分 留出验证 05](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part3/holdout-validation_05.webp)

现在，我们可以用独立测试集来估计模型的泛化性能。请记住，测试集的目的是模拟模型从未见过的新数据；复用该测试集可能导致对模型泛化性能的估计出现过度乐观的偏差。

![模型评估与选择第三部分 留出验证 06](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part3/holdout-validation_06.webp)

最后，我们可以利用全部数据——合并训练集与测试集——在所有数据点上拟合模型，用于真实场景。

注意，在全部可用数据上拟合得到的模型，可能与第 5 步中评估的模型略有不同。不过从理论上讲，用全部数据（即训练数据加测试数据）来拟合模型只会提升其性能。基于这一假设，第 5 步得到的评估结果可能略微低估了第 6 步所拟合模型的性能。（如果把测试数据也用于拟合，我们就没有剩余数据来评估模型了，除非再收集新数据。）在真实应用中，我们通常希望得到"尽可能好"的模型——换句话说，即便略微低估了它的性能，我们也并不介意。无论如何，可以把第六步视为可选项。

## k 折交叉验证入门

现在是时候介绍机器学习实践中最常见的模型评估与模型选择技术了：*k 折交叉验证*（k-fold cross-validation）。文献中对*交叉验证*（cross-validation）一词的使用比较宽泛，从业者和研究者有时会把训练/测试留出法也称为一种交叉验证技术。不过，把*交叉验证*理解为"训练阶段与验证阶段在连续多轮之间交叉互换"可能更贴切。交叉验证背后的核心思想是：数据集中的每个样本都有机会被用于测试。k 折交叉验证是交叉验证的一个特例：我们对数据集迭代 *k* 次。在每一轮中，我们把数据集分成 *k* 份，其中一份用于验证，其余 *k-1* 份合并为训练子集，用于模型评估。下图展示了这一过程，即 5 折交叉验证的示意：

![模型评估与选择第三部分 k 折](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part3/kfold.webp)

与"二分"留出法一样，如果把 k 折交叉验证用于*模型评估*，我们在每次迭代中都用具有固定超参数设置的学习算法在训练折上拟合模型。在 5 折交叉验证中，这一过程会拟合出五个不同的模型；这些模型分别拟合于互不相同但部分重叠的训练集，并在互不重叠的验证集上评估。最终，我们把来自验证集的 *k* 个性能估计的算术平均值作为交叉验证性能。

由此我们看到"二分"留出法与 k 折交叉验证的主要区别：k 折交叉验证让所有数据都既用于训练也用于测试。这种做法的思路是：相比于把数据集中相对较大的一部分留作测试数据，使用更多训练数据可以降低悲观偏差。而与[第二部分](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part2.html)讨论过的*重复*留出法（repeated holdout）不同，k 折交叉验证中的测试折互不重叠。在重复留出法中，样本被反复用于测试，导致各轮之间的性能估计彼此相关；这种相关性会给统计比较带来问题，我们将在第四部分讨论这一点。此外，与重复留出法可能让某些样本从未进入测试集不同，k 折交叉验证保证每个样本都会被用于验证。

本节介绍了用于*模型评估*的 k 折交叉验证。但在实践中，k 折交叉验证更常用于模型选择或算法选择。本文稍后将讨论用于模型选择的 k 折交叉验证，而算法选择将在下一篇文章（第四部分）中详细展开。

## 特殊情形：2 折与留一法交叉验证

读到这里，你可能会好奇为什么上一节用 *k=5* 来演示 k 折交叉验证。一个原因是这样能更紧凑地画出示意。此外，*k=5* 也是实践中的常见选择，因为与更大的 *k* 值相比，它的计算开销更低。不过，如果 *k* 太小，可能会增大估计的悲观偏差（因为可用于模型拟合的训练数据变少），估计的方差也可能上升，因为模型对数据划分方式更加敏感（稍后我们会讨论一些实验，它们表明 *k=10* 是 *k* 的一个不错选择）。

事实上，k 折交叉验证有两个著名的特殊情形：*k=2* 和 *k=n*。大多数文献把 2 折交叉验证等同于留出法。但这种说法只有在以下情形才成立：我们以两轮轮换训练集与验证集的方式执行留出法（即每轮恰好用 50% 的数据做训练、50% 的样本做验证，然后交换这两个集合，重复训练和评估流程，最终把在两个验证集上的性能估计的算术平均值作为性能估计）。鉴于留出法最常见的用法，我更倾向于把留出法和 2 折交叉验证描述为两种不同的过程，如下图所示：

![模型评估与选择第三部分 留出法与 2 折对比](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part3/holdout-vs-2fold.webp)

而如果我们设 *k=n*，即把折数设为与训练样本数相等，那么这种 k 折交叉验证过程就称为***留一法交叉验证***（Leave-one-out cross-validation，LOOCV）。在 LOOCV 的每次迭代中，我们用数据集中的 *n-1* 个样本拟合模型，并在剩下的那一个数据点上评估。尽管这一过程计算开销很大（毕竟有 *n* 次迭代），但它对小数据集很有用——在这种情况下，从训练集中扣留数据就显得太过浪费。

![模型评估与选择第三部分 LOOCV](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part3/loocv.webp)

已有若干研究比较了 k 折交叉验证中不同的 *k* 值，分析 *k* 的选择如何影响估计的方差和偏差。遗憾的是，正如 Yoshua Bengio 和 Yves Grandvalet 在《No Unbiased Estimator of the Variance of K-Fold Cross-Validation》中所展示的，这里同样没有*免费午餐*。

> 该定理的主要结论是：不存在普适的（对所有分布都有效的）K 折交叉验证方差的无偏估计量。（[Bengio and Grandvalet, 2004](#references)）

不过，我们可能仍然想找到一个"甜蜜点"——一个在多数情况下都能在方差与偏差之间取得良好折中的取值。下一节我们将继续讨论偏差-方差权衡。现在，让我们以一个有趣的研究项目来结束本节：Hawkins *等人*比较了通过 LOOCV 与留出法得到的性能估计，并建议在计算可行的情况下优先使用 LOOCV。

> […] 在可用样本量不大的情况下，为模型测试而扣留一部分化合物并非明智之举。这种对样本的切分会损害校准质量，而且无论如何也无助于对拟合效果的可信评估。更好的做法是把全部数据都用于校准步骤，再用交叉验证来检验拟合，并确保交叉验证的执行方式正确。[…] 唯一应该依赖留出样本而非交叉验证的理由，是有理由认为交叉验证不可信——有偏或方差极大。但无论是理论结果还是这里概述的实证结果，都没有给出任何怀疑交叉验证结果的理由。（[Hawkins *and others*, 2003](#references)）

这些结论部分基于该研究在一个 469 样本数据集上开展的实验。下表总结了不同*岭回归*（Ridge Regression）模型比较的发现：

| 实验 | 均值 | 标准差 |
| --- | --- | --- |
| 真实 R2—q2 | 0.010 | 0.149 |
| 真实 R2—留出 50 | 0.028 | 0.184 |
| 真实 R2—留出 20 | 0.055 | 0.305 |
| 真实 R2—留出 10 | 0.123 | 0.504 |

在第 1-4 行中，Hawkins *等人*使用 100 样本的训练集来比较不同的模型评估方法。第一行对应的实验中，研究者使用 LOOCV，在 100 样本的训练子集上拟合回归模型；报告中的"均值"指的是：在不同 100 样本训练集上重复该过程之后，*真实*决定系数与通过 LOOCV 得到的决定系数（此处记为 *q2*）之间差值的平均。在第 2-4 行中，研究者使用留出法在 100 样本训练集上拟合模型，并分别在大小为 10、20、50 样本的留出集上评估性能。每个实验重复 75 次，*均值*一列显示的是估计的 *R2* 与*真实* *R2* 之间的平均差值。可以看到，通过 LOOCV 得到的估计（*q2*）最接近*真实* *R2*；不过，采用 50 样本测试集的留出法所得到的估计也尚可接受。基于这些特定实验，我认同研究者的结论：

> 就上述第三点而言，如果你手头有 150 个或更多的化合物，当然可以随机地分成 100 个用于校准、50 个或更多用于测试。然而，很难说清你为什么要这么做。

如果数据集足够大，我们可能更倾向于留出法，一个原因便是出于计算效率的考虑。根据经验，数据集越大，悲观偏差和大方差问题就越不构成困扰。此外，实践中也常用不同的随机种子重复 k 折交叉验证流程，以获得"更稳健"的估计。例如，如果把 5 折交叉验证重复运行 100 次，我们将为 500 个测试折计算性能估计，并把这 500 个折的算术平均值报告为交叉验证性能。（尽管实践中经常这样做，但要注意此时各测试折是相互重叠的。）不过，重复 LOOCV 没有任何意义，因为 LOOCV 每次产生的划分都是相同的。

## k 值与偏差-方差权衡

基于上一节看到的实验证据，对于小型和中等规模的数据集，我们可能更倾向于用 LOOCV，而不是留出法的单次训练/测试划分。此外，我们可以认为 LOOCV 的估计近似无偏：直观上看，LOOCV（*k=n*）的悲观偏差要低于 *k<n* 的 k 折交叉验证，因为几乎所有（例如 *n-1* 个）训练样本都可用于模型拟合。

虽然 LOOCV 几乎无偏，但相对于 *k<n* 的 k 折交叉验证，它的一个缺点是 LOOCV 估计的方差很大。首先要指出，当使用不连续的损失函数（如分类中的 0-1 损失）乃至连续损失函数（如均方误差）时，LOOCV 是*有缺陷的*。人们常说 LOOCV

> …… [LOOCV] 方差很高，因为测试集只包含一个样本。
> （[Tan *and others*, 2005](#references)）

> …… [LOOCV] 波动很大，因为它基于单个观测 (x1, y1)。
> （[Gareth *and others*, 2013](#references)）

如果我们指的是各折之间的方差，这些说法当然没错。要知道，如果使用 0-1 损失函数（预测要么*正确*要么不正确），我们可以把每次预测看作一次伯努利试验，正确预测的次数 \(X\) 服从二项分布 \(X \sim B(n, p)\)，其中 \(n \in \mathbb{N} \text{ and } p \in [0,1]\)；二项分布的方差定义为 \(\sigma^2 = np(1-p)\)。

我们可以从统计量（*此处指*模型性能）在子样本之间的波动来估计该统计量的变异性。但显然，各折之间的方差并不是 LOOCV 估计方差——即由训练数据的随机性带来的变异性——的好估计。当我们谈论 LOOCV 的方差时，通常指的是：如果从底层分布中抽取不同的数据样本、多次重复重采样过程，所得结果之间的差异。因此，Hastie、Tibshirani 和 Friedman 提出了一个更有意思的观点：

> 当 K = N 时，交叉验证估计量对真实（期望）预测误差近似无偏，但由于这 N 个"训练集"彼此非常相似，其方差可能很高。
> （[Hastie *and others*, 2009](#references)）

换句话说，我们可以把这种高方差归因于一个众所周知的事实：高度相关的变量，其均值的方差要高于不高度相关变量的均值的方差。直观的解释可以从协方差（\(\text{cov}\)）与方差（\(\sigma^2\)）的关系入手：

\[\text{cov}\_{X, X} = \sigma^2\_{X}\]

证明：\(\text{Let } \mu = E(X), { then } \quad \text{cov}\_{X, X} = E\left[(X - \mu)^2\right] = \sigma^{2}\_{X}\)

而协方差 \(\text{cov}\_{X, Y}\) 与相关系数 \(\rho\_{X, Y}\)（X 和 Y 为随机变量）之间的关系定义为

\[\text{cov}\_{X, Y} = \rho\_{X, Y} \; \sigma\_X \sigma\_Y,\]

其中

\[\text{cov}\_{X, Y} = E [(X - \mu\_X)(Y - \mu\_Y)]\]

且

\[\rho\_{X, Y} = E [(X - \mu\_X)(Y - \mu\_Y)] / (\sigma\_X \sigma\_Y).\]

人们常把巨大的*方差*与 LOOCV 联系在一起，这种高方差在实证研究中也已被观察到——例如，我强烈推荐阅读 Ron Kohavi 的那篇优秀论文 *A Study of Cross-Validation and Bootstrap for Accuracy Estimation and Model Selection*（[Kohavi, 1995](#references)）。

既然我们已经确认 LOOCV 估计通常方差大、偏差小，那么它与其他 *k* 取值的 k 折交叉验证以及自助法相比又如何呢？在[第二部分](https://sebastianraschka.com/blog/2016/model-evaluation-selection-part2.html)中，我们提到过标准自助法的悲观偏差——训练集渐近地（*仅*）包含原数据集 0.632 比例的样本；2 折或 3 折交叉验证也有差不多的问题。我们还讨论了为解决这一悲观偏差而设计的 *0.632 自助法*（0.632 Bootstrap）。然而，Kohavi 在他的实验中（[Kohavi, 1995](#references)）也观察到，在某些真实数据集上，自助法的偏差仍然极大（此时变为乐观偏差），相比之下 k 折交叉验证则好得多。最终，Kohavi 在多个真实数据集上的实验表明，10 折交叉验证在偏差与方差之间提供了最佳折中。此外，其他研究者发现，重复 k 折交叉验证可以提高估计的精度，同时仍保持较小的偏差（[Molinaro *and others*, 2005; Kim, 2009](#references)）。

在进入模型选择之前，让我们通过列出增大折数（即 *k*）时的一般趋势，来总结这段关于偏差-方差权衡的讨论：

- 性能估计量的偏差减小（更准确）
- 性能估计量的方差增大（波动更大）
- 计算成本上升（迭代次数更多，拟合时训练集更大）
- 例外：把 k 折交叉验证中的 *k* 减小到很小的值（如 2 或 3），在小数据集上也会因随机采样效应而使方差增大。

## 基于 k 折交叉验证的模型选择

之前我们将 k 折交叉验证用于*模型评估*。现在，我们要更进一步，把 k 折交叉验证用于*模型选择*。同样，关键思想是保留一个独立测试数据集，在训练和模型选择阶段不让它参与，以避免测试数据在训练阶段泄露：

![模型评估与选择第三部分 k 折选择](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part3/kfold-selection.webp)

虽然上图乍看之下有点复杂，但整个过程其实很简单，与本文开头讨论的"三路留出"流程类似。我们一步步来看。

![模型评估与选择第三部分 k 折选择 01](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part3/kfold-selection_01.webp)

与留出法类似，我们把数据集分成两部分：训练集和独立测试集；把测试集收好，留待最后一步做最终的模型评估。

![模型评估与选择第三部分 k 折选择 02](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part3/kfold-selection_02.webp)

第二步，我们可以尝试各种超参数设置：可以使用贝叶斯优化（Bayesian Optimization）、随机搜索（Randomized Search），或者老式的网格搜索（Grid Search）。对每一组超参数配置，我们在训练集上执行 k 折交叉验证，得到多个模型和相应的性能估计。

![模型评估与选择第三部分 k 折选择 03](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part3/kfold-selection_03.webp)

取与表现最佳模型相对应的超参数设置，然后用完整的训练集进行模型拟合。

![模型评估与选择第三部分 k 折选择 04](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part3/kfold-selection_04.webp)

现在到了启用我们扣留的独立测试集的时候；我们用这个测试集来评估第 3 步得到的模型。

![模型评估与选择第三部分 k 折选择 05](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part3/kfold-selection_05.webp)

最后，当评估阶段完成后，我们可以在全部数据上拟合模型，作为（所谓）*部署*用的模型。

翻阅深度学习文献时，我们常常发现三路留出法是模型评估的首选方法；它在较早期（非深度学习）文献中同样常见。如前所述，相较于 k 折交叉验证，三路留出法可能更受青睐，因为相比之下它的计算开销更低。除了计算效率的考虑之外，我们本来就只在样本量相对较大时才使用深度学习算法——在这种场景下，我们不必太担心高方差——即我们的估计对训练/验证/测试集划分方式的敏感性——所带来的问题。

注意，如果我们要做数据归一化或特征选择，通常应在 k 折交叉验证循环*内部*执行这些操作，而不是在把数据切分成各折之前就先对整个数据集施加这些步骤。在交叉验证循环内部做特征选择可以降低因过拟合带来的偏差，因为我们在训练阶段避免偷看测试数据的信息。不过，在交叉验证循环内部做特征选择也可能导致估计过于悲观，因为可用于训练的数据变少了。关于"特征选择应放在交叉验证循环之内还是之外"这一话题的更详细讨论，推荐阅读 Refaeilzadeh 的《On Comparison of Feature Selection Algorithms》。
（[Refaeilzadeh *and others*, 2007](#references)）

## 简约律

上一节讨论了模型选择，现在让我们花点时间看看简约律（Law of Parsimony），也就是奥卡姆剃刀（Occam's Razor）：

> 在相互竞争的假设中，应当选择假设最少的那一个。

换个说法，用我最喜欢的一句名言来说：

> "万事应力求简洁，但不要过于简洁。" —— 阿尔伯特·爱因斯坦

在模型选择实践中，我们可以按以下方式用*一标准误差法*（one-standard error method）来应用奥卡姆剃刀：

1. 考察数值上最优的估计值及其标准误差。
2. 选择性能落在第 1 步所得值的一个标准误差范围内的模型（[Breiman *and others*, 1984](#references)）。

尽管出于多种原因我们可能更偏好简单模型，但 Pedro Domingos 就"复杂"模型的性能提出了一个很好的观点。以下是他近期文章《[Ten Myths About Machine Learning](https://medium.com/@pedromdd/ten-myths-about-machine-learning-d888b48334a3)》的节选：

> 更简单的模型更准确。这一信条有时被等同于奥卡姆剃刀，但剃刀只说更简单的解释更可取，却没说为什么。它们更可取，是因为更易于理解、记忆和推理。有时，与数据一致的最简单假设在预测上反而不如更复杂的假设准确。一些最强大的学习算法输出的模型看似过于繁复——有时甚至在完美拟合数据之后仍在继续增添复杂度——但它们正是以此击败了那些较弱的算法。

再次强调，只要模型的性能落在某个可接受的范围内，我们就有好几条理由偏好更简单的模型——例如使用*一标准误差法*。更简单的模型或许不是最"准确"的那个，但与更复杂的备选方案相比，它可能计算效率更高、更易于实现、也更容易理解和推理。

为了看看*一标准误差法*在实践中如何运作，我们把它应用到一个简单的玩具数据集上：300 个数据点、同心圆形状、均匀的类别分布（类别 1 有 150 个样本，类别 2 有 150 个样本）。首先，我们使用分层抽样（stratification）保持类别比例一致，把数据集分成两部分：70% 的训练数据和 30% 的测试数据。训练数据集中的 210 个样本如下图所示：

![模型评估与选择第三部分 模型评估同心圆 1](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part3/model-eval-circles_1.webp)

假设我们要为一个采用非线性径向基函数核（RBF 核）的支持向量机（SVM）优化 *Gamma* 超参数，其中 \(\gamma\) 是高斯 RBF 的自由参数：

\[K(x\_i, x\_j) = exp(-\gamma || x\_i - x\_j ||^2), \gamma > 0\]

（直观地说，可以把 *Gamma* 理解为控制单个训练样本对决策边界影响程度的参数。）

我在训练集上用不同的 *Gamma* 值运行 RBF 核 SVM 算法，采用分层 10 折交叉验证，得到了以下性能估计，其中误差棒是交叉验证估计的标准误差：

![模型评估与选择第三部分 模型评估同心圆 2](https://sebastianraschka.com/images/blog/2016/model-evaluation-selection-part3/model-eval-circles_2.webp)

（生成本文所示图表的代码可在 GitHub 上的[这个 Jupyter Notebook](https://github.com/rasbt/pattern_classification/blob/master/data_viz/model-evaluation-articles/model-eval-kfold.ipynb) 中找到。）

可以看到，*Gamma* 取值在 0.1 到 100 之间时，预测准确率达到 80% 或更高。此外可以看到，\(\gamma=10.0\) 给出了相当复杂的决策边界，而 \(\gamma=0.001\) 给出的决策边界则过于简单，无法分开两个类别。实际上，\(\gamma=0.1\) 看起来是上述两种模型之间的一个良好折中——相应模型的性能落在最佳模型（\(\gamma=0\) 或 \(\gamma=10\)）的一个标准误差范围之内。

## 总结与结论

评估预测模型泛化性能的方法有很多。到目前为止，我们已经了解了留出法、自助法的各种变体以及 k 折交叉验证。在我看来，在样本量相对较大时，留出法用于模型评估完全没有问题。如果要做超参数调优，我们可能更倾向于 10 折交叉验证；而如果样本量很小，留一法交叉验证是一个不错的选择。至于模型选择，受计算资源所限，"三路"留出法可能仍是好选择；一个不错的替代方案是 k 折交叉验证加上独立测试集。而用于模型选择或算法选择的更佳方法是*嵌套交叉验证*（nested cross-validation），我们将在第四部分讨论这一方法。

感谢阅读。如果你喜欢这些内容，也可以[在 Twitter 上找到我](https://twitter.com/rasbt)，我在那里分享更多有用的内容。

## 下一部分预告

在本系列的下一部分中，我们将更详细地讨论假设检验和算法选择的方法。

假设我们想招聘一名股票市场分析师。为了找到一名*优秀*的分析师，不妨假定我们在面试之前，让各位候选人预测某些股票价格在未来 10 天内是涨还是跌。优秀的候选人至少应答对这 10 个预测中的 8 个。在对股市运作一无所知的情况下，我们每天正确预测趋势的概率是 50%——相当于每天抛一次硬币。那么，如果我们只面试了一位"抛硬币"式的候选人，她 10 次中答对 8 次的概率将是 0.0547：

\[\frac{ {10 \choose 8} + {10 \choose 9} + {10 \choose 10}}{2^{10} } = 0.0547.\]

换句话说，我们可以说这位候选人的预测表现不太可能是运气使然。然而，假设我们邀请的不只一位面试者，而是 100 位。如果我们请这 100 位面试者都做出预测，并假定没有一位候选人了解股市如何运作、所有人都在随机猜测，那么至少有一位候选人答对 10 个预测中的 8 个的概率是：

\[1 - (1 - 0.0547)^{100} = 0.9964.\]

那么，我们是否应该认定一位 10 个预测答对 8 个的候选人并非在随机瞎猜？我们将在[第四部分](https://sebastianraschka.com/blog/2018/model-evaluation-selection-part4.html)中继续讨论假设检验以及学习算法之间的比较。

## References

- Bengio, Yoshua, and Yves Grandvalet. 2004. "[No Unbiased Estimator of the Variance of K-Fold Cross-Validation](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.9.3582)." *J. Mach. Learn. Res. 5* (December). JMLR.org: 1089–1105.
- Breiman, Leo, Jerome Friedman, Charles J Stone, and Richard A Olshen. 1984. *Classification and Regression Trees*. CRC press.
  Breiman, Leo. 1996. "[Heuristics of Instability and Stabilization in Model Selection](http://projecteuclid.org/euclid.aos/1032181158)." *The Annals of Statistics* 24 (6). Institute of Mathematical Statistics: 2350–83.
- Hastie, Trevor, Robert Tibshirani, and J. H. Friedman. "7.10.1 K-Fold Cross-Validation." *In [The Elements of Statistical Learning: Data Mining, Inference, and Prediction](http://statweb.stanford.edu/~tibs/ElemStatLearn/)*. 2nd ed. New York: Springer, 2009.
- Hawkins, Douglas M., Subhash C. Basak, and Denise Mills. 2003. "[Assessing Model Fit by Cross-Validation.](https://www.ncbi.nlm.nih.gov/pubmed/12653524)" *Journal of Chemical Information and Computer Sciences* 43 (2). American Chemical Society: 579–86.
- Kohavi, Ron. 1995. "[A Study of Cross-Validation and Bootstrap for Accuracy Estimation and Model Selection](http://www.ijcai.org/Proceedings/95-2/Papers/016.pdf)." *International Joint Conference on Artificial Intelligence* 14 (12): 1137–43
- James, Gareth, Daniela Witten, Trevor Hastie, and Robert Tibshirani. "5.1 Cross-Validation" *In [An Introduction to Statistical Learning: With Applications in R](http://www-bcf.usc.edu/~gareth/ISL/).* Vol. 6. New York: Springer, 2013.
- Jiang, Wenyu, and Richard Simon. 2007. "[A Comparison of Bootstrap Methods and an Adjusted Bootstrap Approach for Estimating the Prediction Error in Microarray Classification](https://www.ncbi.nlm.nih.gov/pubmed/17624926)." *Statistics in Medicine* 26 (29): 5320–34.
- Kim, Ji-Hyun. 2009. "[Estimating Classification Error Rate: Repeated Cross-Validation, Repeated Hold-out and Bootstrap](http://www.sciencedirect.com/science/article/pii/S0167947309001601)." *Computational Statistics & Data Analysis* 53 (11): 3735–45.
- Molinaro, Annette M, Richard Simon, and Ruth M Pfeiffer. 2005. "[Prediction Error Estimation: A Comparison of Resampling Methods](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.573.5753)." *Bioinformatics (Oxford, England)* 21 (15). Oxford University Press: 3301–7.
- Refaeilzadeh, Payam, Lei Tang, and Huan Liu. 2007. "[On Comparison of Feature Selection Algorithms](https://www.aaai.org/Papers/Workshops/2007/WS-07-05/WS07-05-007.pdf)." *In Proceedings of AAAI Workshop on Evaluation Methods for Machine Learning II*, 34–39.
- Tan, Pang-Ning, Michael Steinbach, and Vipin Kumar. "4. Classification: Basic Concepts, Decision Trees, and Model Evaluation." *In [Introduction to Data Mining](http://www-users.cs.umn.edu/~kumar/dmbook/index.php)*. Boston: Pearson Addison Wesley, 2005.
