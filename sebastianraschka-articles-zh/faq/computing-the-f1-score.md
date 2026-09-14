---
title: "F1 分数如何帮助应对类别不平衡问题？"
title_en: "How can the F1-score help with dealing with class imbalance?"
source: https://sebastianraschka.com/faq/docs/computing-the-f1-score.html
crawled: 2026-09-06
translated: 2026-09-14
---

# F1 分数如何帮助应对类别不平衡问题？

> 原文：[How can the F1-score help with dealing with class imbalance?](https://sebastianraschka.com/faq/docs/computing-the-f1-score.html) · Sebastian Raschka's FAQ

这是我一篇即将发布的博客文章的节选。遗憾的是，那篇博客文章写得太长了，实在过长。在删减的过程中，必须做出艰难的取舍，于是这段离题的——呃——章节不得不删掉……
在我按下删除键之前……也许这一节对其他人有用！？

接着刚才的话头往下讲：我们"如何"选择模型、如何在不同的机器学习算法之间做选择，完全取决于我们如何评估这些不同的模型，而这又取决于我们选择的性能指标。总结来说，我们最关心的话题有：

- 泛化性能的估计
- 算法选择
- 超参数调优技术
- （交叉）验证与采样技术
- 性能指标
- 类别不平衡

不过现在进入我真正想分享的那一节……

## 插曲：在交叉验证中比较和计算性能指标——类别不平衡问题以及计算 F1 分数的三种不同方式

不久前，George Forman 和 Martin Scholz 写了一篇发人深省的论文，讨论如何跨文献比较和计算性能指标，尤其是在处理类别不平衡问题时：[Apples-to-apples in cross-validation studies: pitfalls in classifier performance measurement (2010)](http://www.hpl.hp.com/techreports/2009/HPL-2009-359.pdf)。这篇论文写得非常好、非常易懂（而且主题非常重要）！我强烈推荐一读。如果你对此还不算熟悉，它可能会改变你的视角——你阅读论文的方式、你评估和做机器学习模型基准测试的方式——而且如果你决定发表自己的结果，你的读者也一定会受益。

现在，假设我们想把自己闪亮的新算法与过往的工作进行比较。首先，我们要确保是在"同水果比同水果"（fruits to fruits）。假设我们在相同的数据集上评估，我们要确保使用相同的交叉验证技术和评估指标。我知道这听起来理所当然，但我们首先要立下这条基本规矩：不能拿 ROC 曲线下面积（AUC）指标去和 F1 分数比较……
顺便说一句，ROC AUC 指标的使用至今仍是热议话题，例如：

- JM. Lobo, A. Jiménez-Valverde, and R. Real 2008: [AUC: a misleading measure of the performance of predictive distribution models](http://onlinelibrary.wiley.com/doi/10.1111/j.1466-8238.2007.00358.x/abstract;jsessionid=40E65D14D4CEEC38F203699F5DCC18C7.f01t03?userIsAuthenticated=false&deniedAccessCustomisedMessage=)
- Jin Huang & C. X. Ling 2005: [Using AUC and accuracy in evaluating learning algorithms](https://ieeexplore.ieee.org/document/1388242)
- AP. Bradley 1997 [The use of the area under the ROC curve in the evaluation of machine learning algorithms](http://www.sciencedirect.com/science/article/pii/S0031320396001422)

无论如何，我们暂且聚焦于 F1 分数，在定义一些相关术语之后，概述 Forman 与 Scholz 论文中的一些想法。

我们大概都听说过或读到过，F1 分数就是精确率（precision，PRE）与召回率（recall，REC）的调和平均：

F1 = 2 \* (PRE \* REC) / (PRE + REC)

***F1 分数这一指标想达到的目的，是在精确率和召回率之间找到一个均衡，这在大多数处理不平衡数据集（即类别标签分布不均匀的数据集）的场景中极为有用。***

---

如果我们用真阳性（TP）、真阴性（TN）、假阳性（FP）和假阴性（FN）来表示 PRE 和 REC 这两个指标，就得到：

- PRE = TP / (TP + FP)
- REC = TP / (TP + FN)

于是，精确率告诉我们（以 1.0 到 0.0 的分数表示，从好到差）：在我们所有被判为垃圾邮件的邮件（TP + FP）之中，有多少真正的垃圾邮件（TP）被我们正确分类。
相比之下，召回率（同样取值 1.0 到 0.0）告诉我们：所有真正的垃圾邮件（TP）中，我们"检回"或"召回"了多少（TP + FN）。

---

好，假设我们选定 F1 分数作为性能指标，来为我们的新算法做基准测试；巧的是，某篇论文中的算法——它将作为我们的参考性能——也是用 F1 分数评估的。在相同的数据集上使用相同的交叉验证技术，这样比较应该是公平的，对吧？不不不，别急着下结论！除了选择合适的性能指标——即"同水果比同水果"——之外，我们还必须关心它是如何计算的，才能做到"苹果比苹果"（apples to apples）。在比较不平衡数据集上的性能指标时，这一点极其重要，我马上就会解释（基于 Forman 与 Martin Scholz 论文的结果）。***另外请记住，即使我们的数据集乍看起来并不不平衡——想想 Iris 数据集里 50 朵 Setosa、50 朵 Virginica 和 50 朵 Versicolor——如果我们采用一对其余（One-vs-Rest，OVR；或 One-vs-All，OVA）的分类方案，会怎样？***

无论如何，我们先聚焦于一个二分类问题（一个*正*类和一个*负*类），并选用 k 折交叉验证作为模型选择的交叉验证技术。

如前所述，我们按下式计算 F1 分数：

F1 = 2 \* (PRE \* REC) / (PRE + REC)

现在，如果我们有一个高度不平衡的数据集，并在训练集上执行 k 折交叉验证，会发生什么？很有可能某个特定的折里不包含*正*样本，于是 TP=FN=0。如果这听起来还不算太糟，再回头看一眼上面的召回率公式——没错，这是一个除零错误！又或者，如果我们的分类器几乎总是预测负类（即它的假阳性率很低）呢？同样，由于 TP = FP = 0，精确率公式会出现除零错误。

我们能做些什么？有两件事。第一，让我们对各折做分层（stratify）——分层意味着随机采样过程会尽量在不同折之间保持类别标签的比例。这样一来，只要 *k* 不大于训练集中*正*样本的数量，我们就不太会遇到"某一折没有正类样本"之类的问题。

***在实践中，不同的软件包对除零错误的处理方式各不相同：有的会毫不犹豫地抛出运行时异常；有的可能会悄悄地把精确率和/或召回率替换为 0——请务必弄清楚它到底做了什么！*** 除此之外，我们还可以用几种不同的方式计算 F1 分数（在多分类问题中，还可以在此之上使用 micro 和 macro 平均技术，但这超出了本节的范围）。正如 Forman 和 Scholz 所列出的，这三种不同的情形是：

### (1)

我们对每个折（每次迭代）分别计算 F1 分数；然后对这些各自的 F1 分数求平均，
得到平均 F1 分数。

F1avg = 1/k Σki=1 F1(i)

### (2)

我们先在 *k* 个折上计算平均的精确率和召回率；然后用这些平均值来计算最终的 F1 分数。

PRE = 1/k Σki=1 PRE(i)

REC = 1/k Σki=1 REC(i)

F1PRE, REC = 2 \* (PRE \* REC) / (PRE + REC)

### (3)

我们为每个折或每次迭代分别统计 TP、FP 和 FN 的数量，再基于这些"micro"指标计算最终的 F1 分数。

TP = Σki=1 TP(i)

FP = Σki=1 FP(i)

FN = Σki=1 FN(i)

F1TP, FP, FN = (2 \* TP) / (2 \* TP + FP + FN)

（注意这个公式不会出现除零问题。）

---

请注意，对于分类错误率或准确率（accuracy）的不同计算方式，我们不必担心——本节之外，博客文章正文里用到的就是它们。原因在于，无论我们把准确率计算为

ACCavg = 1/k Σki=1 ACC(i)

还是

TP = Σki=1 TP(i)

TN = Σki=1 TN(i)

ACC avg = (TP + TN) / N

两种方式的结果是完全相同的，举个更具体的例子：(30 + 40) / 100 = (30/50 + 40/50) / 2 = 0.7。

---

最后，Forman 和 Scholz 在一个具有高度类别不平衡的基准数据集上（为了演示目的略有夸张，但在处理文本数据时并不罕见）实际演练了用不同方式计算 F1 分数的把戏。结果是，同一个模型得到的分数相差悬殊：

- F1avg: 69%
- F1PRE, REC: 73%
- F1TP, FP, FN: 58%

***最终，基于进一步的模拟，Forman 和 Scholz 得出结论：计算 F1TP, FP, FN（相对于其他计算 F1 分数的替代方式）能给出使用 \*k*\-折交叉验证时对泛化性能"最无偏"的估计。**\*

总之，底线是：我们不仅要为任务选择合适的性能指标和交叉验证技术，而且当我们引用论文或依赖现成的机器学习库时，还应当***更仔细地考察各种性能指标究竟是如何计算的。***
