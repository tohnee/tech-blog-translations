---
title: "朴素贝叶斯与文本分类"
title_en: "Naive Bayes and Text Classification"
source: https://sebastianraschka.com/Articles/2014_naive_bayes_1.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 朴素贝叶斯与文本分类

> 原文：[Naive Bayes and Text Classification](https://sebastianraschka.com/Articles/2014_naive_bayes_1.html) · Sebastian Raschka's Articles

朴素贝叶斯分类器（naive Bayes classifiers）是一类基于著名的贝叶斯概率定理构建的分类器，以能构建简单而性能良好的模型著称，尤其适用于文档分类和疾病预测等领域。  
在本系列的第一部分中，我们将探讨朴素贝叶斯分类器的理论，并介绍文本分类的基本概念。在后续文章中，我们将把这些概念付诸实践：训练一个朴素贝叶斯垃圾信息过滤器，并基于歌词将朴素贝叶斯应用于歌曲分类。

***[PDF 版本](https://arxiv.org/abs/1410.5329)可通过 arXiv 获取。***

## 引言

早在半个多世纪以前，科学家们就开始非常认真地对待这样一个问题："我们能否构建一个从现有数据中学习、并自动做出正确决策和预测的模型？"如今回望，这几乎像是一个反问句，而它的答案已经体现在模式分类、机器学习和人工智能领域涌现出的无数应用之中。

来自各类传感设备的数据，结合强大的学习算法和领域知识，催生了许多伟大的发明，如今我们已对其习以为常：通过 Google 等搜索引擎进行的互联网检索、邮局的文字识别、超市的条形码扫描仪、疾病诊断，以及手机上 Siri 或 Google Now 的语音识别，不一而足。

*预测建模*（predictive modeling）的一个子领域是*有监督模式分类*（supervised pattern classification）；有监督模式分类的任务是：基于带标签的训练数据训练一个模型，然后用它为新的对象分配预先定义好的类别标签。本文将贯穿探讨的一个例子是：利用朴素贝叶斯分类器进行垃圾信息过滤，以预测一条新的文本消息应被归为垃圾信息（spam）还是非垃圾信息。  
朴素贝叶斯分类器是一类基于著名的贝叶斯概率定理构建的分类器，以能构建简单而性能良好的模型著称，尤其适用于文档分类和疾病预测等领域。

![Figure 1.](https://sebastianraschka.com/images/blog/2014/naive_bayes_1/learning_algorithm_1.png)
**图 1.**

## 朴素贝叶斯分类

*朴素贝叶斯分类器*是线性分类器，以简单而高效著称。朴素贝叶斯分类器的概率模型基于贝叶斯定理，而"朴素"（naive）这一形容词来自数据集中各特征相互独立的假设。在实践中，这一独立性假设往往并不成立，但即便是在这种不太现实的假设下，朴素贝叶斯分类器仍往往表现得非常出色[[1](#References)]。尤其是当样本量较小时，朴素贝叶斯分类器的表现甚至可以超越更强大的替代方法[[2](#References)]。

由于相对稳健、易于实现、速度快且准确率高，朴素贝叶斯分类器被应用于许多不同的领域。例如：疾病诊断与治疗方案决策[[3](#References)]、分类学研究中 RNA 序列的分类[[4](#References)]，以及电子邮件客户端中的垃圾邮件过滤[[5](#References)]。  
然而，当独立性假设被严重违反，或者遇到非线性分类问题时，朴素贝叶斯分类器的表现可能会非常糟糕。  
我们必须牢记：数据的类型和所要解决的问题类型决定了我们应选择哪种分类模型。在实践中，始终建议在特定数据集上比较不同的分类模型，并同时兼顾预测性能与计算效率。

在接下来的几节中，我们将深入剖析朴素贝叶斯分类器的概率模型，并把这一概念应用到一个简单的玩具问题上。随后，我们将使用一份公开的 SMS（短信）数据集，用 Python 训练一个朴素贝叶斯分类器，把未见过的消息分类为垃圾信息（spam）或正常信息（ham）。

![Naive bayes 1 linear vs nonlinear problems](https://sebastianraschka.com/images/blog/2014/naive_bayes_1/linear_vs_nonlinear_problems.png)

**图 2.** *线性问题（A）与非线性问题（B）。图中以彩色圆球表示两个不同类别的随机样本，虚线表示类别边界，分类器通过计算决策边界来逼近这些类别边界。
非线性问题（B）指的是类别不线性可分的情形，此时朴素贝叶斯这类线性分类器并不适用。在这种场景下，应优先选择非线性分类器（例如基于实例的最近邻分类器）。*

### 后验概率

要理解朴素贝叶斯分类器的工作原理，我们必须先简要回顾贝叶斯法则的概念。
由托马斯·贝叶斯（Thomas Bayes，1701-1761）提出的概率模型非常简单却十分强大；用浅显的文字可以把它写成：

\[\text{posterior probability} = \frac{\text{conditional probability} \cdot \text{prior probability}}{\text{evidence}}\]

贝叶斯定理构成了朴素贝叶斯分类整个概念的核心。在分类问题的语境下，*后验概率*（posterior probability）可以解读为："在观测到某个对象的特征取值之后，该对象属于类别 \(i\) 的概率是多少？"一个更具体的例子是："在已知某个人早餐前血糖测量值和早餐后血糖测量值的情况下，这个人患糖尿病的概率是多少？"

\[P(\text{diabetes} \mid \textbf x\_i) \;, \quad \textbf x\_i = [90 \text{mg/dl}, 145 \text{mg/dl}]\]

设

- \(\textbf x\_i\) 为样本 \(i, \; i \in \{1, 2, ..., n\}\) 的特征向量，
- \(\omega\_j\) 为类别 \(j, \; j \in \{1, 2, ..., m\}\) 的记号，
- \(P(\textbf x\_i \mid \omega\_j)\) 为在样本属于类别 \(\omega\_j\) 的条件下观测到样本 \(\textbf x\_i\) 的概率。

后验概率的一般形式可以写成

\[P(\omega\_j \mid \textbf x\_i) = \frac{P(\textbf x\_i \mid \omega\_j) \cdot P(\omega\_j)}{P(\textbf x\_i)}\]

朴素贝叶斯概率模型中的目标函数是：在给定训练数据的条件下最大化后验概率，从而制定出决策规则。

沿用上面的例子，我们可以基于后验概率将决策规则表述如下：

\[\begin{split}
& \text{person has diabetes if} \\
& P(\text{diabetes} \mid \textbf x\_i) \ge P(\text{not-diabetes} \mid \textbf x\_i), \\
& \text{else classify person as healthy}.
\end{split}\]

### 类条件概率

贝叶斯分类器的一个假设是：样本是*独立同分布*的（*i.i.d.*）。  
缩写 *i.i.d.* 的意思是"独立同分布"（independent and identically distributed），用来描述彼此独立且来自相似概率分布的随机变量。独立性意味着一次观测的概率不会影响另一次观测的概率（例如，时间序列和网络图就不是独立的）。*i.i.d.* 变量最经典的例子是抛硬币：第一次抛硬币的结果不会影响第二次抛硬币的结果，以此类推。对于一枚均匀的硬币，无论抛多少次，硬币正面朝上的概率始终是 0.5。

朴素贝叶斯分类器的另一个假设是特征之间的*条件独立性*。在这一"朴素"假设下，样本的*类条件概率*（class-conditional probabilities，即*似然*）可以直接从训练数据中估计，而无须穷举 \(\textbf{x}\) 的所有可能取值。于是，给定一个 \(d\) 维特征向量 \(\textbf{x}\)，类条件概率可以按如下方式计算：

\[P(\textbf x \mid \omega\_j) = P(x\_1 \mid \omega\_j) \cdot P(x\_2 \mid \omega\_j) \cdot \ldots \cdot P(x\_d \mid \omega\_j) = \prod\_{k=1}^{d} P( x\_k \mid \omega\_j)\]

这里的 \(P(\textbf x \mid \omega\_j)\) 的含义只是："在属于类别 \(\omega\_j\) 的前提下，观测到这个特定模式 \(\textbf x\) 的可能性有多大？"特征向量中每个特征的"单独"似然都可以通过极大似然估计来估计，对于类别型数据而言，它就是一个频率：

\[\hat{P}(x\_i \mid \omega\_j) = \frac{N\_{x\_i, \omega\_j}}{N\_{\omega\_j}} \quad (i = (1, ..., d))\]

- \(N\_{x\_i, \omega\_j}\)：特征 \(x\_i\) 在类别 \(\omega\_j\) 的样本中出现的次数。
- \(N\_{\omega\_j}\)：类别 \(\omega\_j\) 中所有特征的总数。

为了用一个例子说明这个概念，假设我们有一个包含 500 篇文档的集合，其中 100 篇是*垃圾*（spam）信息。现在，我们想计算新消息 "Hello World" 在其为垃圾信息这一条件下的类条件概率。
这里，该模式由两个特征组成："hello" 和 "world"，类条件概率就是"在消息为垃圾信息的前提下遇到 'hello' 的概率"与"在消息为垃圾信息的前提下遇到 'world' 的概率"的乘积。

\[P(\textbf x=[\text{hello, world}] \mid \omega=\text{spam}) = P(\text{hello} \mid \text{spam}) \cdot P(\text{world} \mid \text{spam})\]

利用这个包含 500 篇文档的训练集，我们可以用极大似然估计来估计这些概率：只需统计这些词在全部垃圾信息语料中出现的频率即可。例如，

\[\hat{P}(\textbf x=[\text{hello, world}] \mid \omega=\text{spam}) = \frac{20}{100} \cdot \frac{2}{100} = 0.004\]

然而，对照条件独立性这一"朴素"假设，我们在这里会注意到一个问题：该假设认为某个特定的词不会影响同一文档中其他词出现的概率。举个例子，考虑文本文档中的 "peanut"（花生）和 "butter"（黄油）这两个词，直觉告诉我们这一假设显然被违反了：如果一篇文档包含 "peanut"，那么它同时包含 "butter"（或 "allergy"，过敏）的可能性会更大。在实践中，条件独立假设确实经常被违反，但众所周知，朴素贝叶斯分类器在这些情况下依然表现良好[[6](#References)]。

### 先验概率

与频率派方法不同，这里引入了一个额外的*先验概率*（prior probability，或简称*先验*），它可以被解释为*先验信念*或*先验*（a priori）知识。

\[\text{posterior probability} = \frac{\text{conditional probability} \cdot \text{prior probability}}{\text{evidence}}\]

在模式分类的语境下，先验概率也被称为*类先验*（class priors），它描述的是"遇到某个特定类别的一般概率"。在垃圾信息分类的例子中，先验可以表述为

\(P(\text{spam})=\text{"the probability that any new message is a spam message"}\) 以及

\[P(\text{ham})= 1-P(\text{spam}).\]

如果先验服从均匀分布，那么后验概率将完全由类条件概率和证据项决定。而由于证据项是一个常数，决策规则将完全取决于类条件概率（这类似于频率派方法与极大似然估计的做法）。

最终，*先验*知识可以通过多种途径获得，例如咨询领域专家，或者从训练数据中估计（前提是训练数据*独立同分布*，且是总体的一个有代表性的样本）。极大似然估计方法可以表述为

\[\hat{P}(\omega\_j) = \frac{N\_{\omega\_j}}{N\_c}\]

- \(N\_{\omega\_j}\)：类别 \(\omega\_j\) 中的样本数量。
- \(N\_c\)：所有样本的数量。

而在*垃圾信息分类*的语境下：

\[\hat{P}(\text{spam}) = \frac{\text{# of spam messages in training data}}{\text{ # of all messages in training data}}\]

图 3 展示了先验概率对决策规则的影响。给定一个一维模式 \(\textbf{x}\)（连续属性，图中以 "x" 符号绘制），它服从正态分布，且属于两个类别（*蓝色*和*绿色*）之一。第一类（\(\omega\_1=\text{blue}\)）的模式采样自均值为 \(x=4\)、标准差 \(\sigma=1\) 的正态分布。第二类（\(\omega\_2=\text{green}\)）的概率分布以 x=10 为中心，标准差同样为 \(\sigma=1\)。钟形曲线表示采样自这两个不同正态分布的样本的概率密度。如果只考虑类条件概率，此情形下的极大似然估计为

\[\begin{split}
&P(x=4 \mid \omega\_1) \approx 0.4 \text{ and } P(x=10 \mid \omega\_1) < 0.001\\
&P(x=4 \mid \omega\_2) < 0.001 \text{ and } P(x=10 \mid \omega\_2) \approx 0.4.
\end{split}\]

现在，给定均匀先验，即 \(P(\omega\_1) = P(\omega\_2) = 0.5\)，决策规则将完全依赖于这些类条件概率，因此决策边界会恰好落在两个分布的正中间

\[P(x \mid \omega\_1) = P(x \mid \omega\_2).\]

然而，如果先验概率为 \(P(\omega\_1) > 0.5\)，那么类别 \(\omega\_1\) 的决策区域就会扩张，如图 3 所示。在垃圾信息分类的语境下，这可以理解为：遇到一条新消息，其中只包含既可能出现在*垃圾*信息、也同样可能出现在*正常*信息中的词。此时，决策将完全取决于*先验知识*，例如，我们可以假设一条随机消息在 10 次中有 9 次不是*垃圾*信息，从而把这条新消息归类为*正常*信息。

![Figure 3.** *The effect of prior probabilities on the decision regions. The figure shows an 1-dimensional random sample from two different classes (blue and green crosses). The data points of both the blue and the green class are normally distributed with standard deviation 1, and the bell curves denote the class-conditional probabilities. If the class priors are equal, the decision boundary of a naive Bayes classifier is placed at the center between both distributions (gray bar). An increase of the prior probability of the blue class ($$\omega_1$$) leads to an extension of the decision region R1 by moving the decision boundary (blue-dotted bar) towards the other class and vice versa.](https://sebastianraschka.com/images/blog/2014/naive_bayes_1/effect_priors_1.png)

**图 3.** *先验概率对决策区域的影响。图中展示了来自两个不同类别（蓝色和绿色十字）的一维随机样本。蓝色类和绿色类的数据点均服从标准差为 1 的正态分布，钟形曲线表示类条件概率。当两类先验相等时，朴素贝叶斯分类器的决策边界位于两个分布的正中央（灰色竖条）；蓝色类（\(\omega\_1\)）先验概率的增大会使决策边界（蓝色虚线条）向另一类移动，从而使决策区域 R1 扩张，反之亦然。*

### 证据

在定义了*类条件概率*和*先验概率*之后，要计算*后验概率*还缺一项，那就是*证据*（evidence）。

\[\text{posterior probability} = \frac{\text{conditional probability} \cdot \text{prior probability}}{\text{evidence}}\]

证据 \(P(\textbf x)\) 可以理解为：与类别标签无关地遇到某个特定模式 \(\textbf x\) 的概率。给定后验概率更正式的定义

\[P(\omega\_j \mid \textbf x\_i) = \frac{P(\textbf x\_i \mid \omega\_j) \cdot P(\omega\_j)}{P(\textbf x\_i)},\]

证据可按如下方式计算（\(\omega\_j^C\) 表示"补集"（complement），基本等同于"\(\textbf{not} \text{ class } \omega\_j\)"，即"非类别 \(\omega\_j\)"）：

\[P(\textbf x\_i) = P(\textbf x\_i \mid \omega\_j) \cdot P(\omega\_j) + P(\textbf x\_i \mid \omega\_j^C) \cdot P(\omega\_j^C)\]

尽管准确计算后验概率需要用到证据项，但在决策规则"若 \(P(\omega\_1 \mid \textbf x\_i) > P(\omega\_2 \mid \textbf x\_i)\) 则将样本 \(\textbf x\_i\) 归为 \(\omega\_1\)，否则将样本归为 \(\omega\_2\)"中，证据项可以去掉，因为它仅仅是一个缩放因子：

\[\frac{P(\textbf x\_i \mid \omega\_1) \cdot P(\omega\_1)}{P(\textbf x\_i)} > \frac{P(\textbf x\_i \mid \omega\_2) \cdot P(\omega\_2)}{P(\textbf x\_i)}\]
\[\propto P(\textbf x\_i \mid \omega\_1) \cdot P(\omega\_1) > P(\textbf x\_i \mid \omega\_2) \cdot P(\omega\_2)\]

### 多项式朴素贝叶斯——一个玩具示例

在介绍了朴素贝叶斯分类器的基本概念、*后验概率*和*决策规则*之后，让我们基于图 4 所示的训练集，走一遍一个简单的玩具例子。

![Figure 4.** *A simple toy dataset of 12 samples 2 different classes $$+, -$$ . Each sample consists of 2 features: color and geometrical shape.](https://sebastianraschka.com/images/blog/2014/naive_bayes_1/toy_dataset_1.png)

**图 4.** *一个简单的玩具数据集，包含 12 个样本、2 个不同类别 \(+, -\)。每个样本由 2 个特征组成：颜色和几何形状。*

设

- \(\omega\_j\) 为类别标签：\(\omega\_j \in \{+, -\}\)
- \(\textbf x\_i\) 为二维特征向量：\(\textbf x\_i = [x\_{i1} \; x\_{i2}], \quad x\_{i1} \in \{ \text{blue}, \text{green}, \text{red}, \text{yellow} \}, \quad x\_{i2} \in \{\text{circle}, \text{square} \}.\)

两个类别标签为 \(\omega\_j \in \{+, -\}\)，样本 \(i\) 的特征向量可以写成

\[\begin{split}
& \textbf{x}\_i = [x\_{i1} \; x\_{i2}] \\
& \text{for } i \in \{1, 2, ..., n\}, \; \text{ with } n=12 \\
& \text{and } x\_{i1} \in \{ \text{blue}, \text{green}, \text{red}, \text{yellow} \}, \quad x\_{i2} \in \{\text{circle}, \text{square} \}
\end{split}\]

现在的任务是对一个新样本进行分类——假装我们并不知道它的真实类别标签是 "+"：

![Figure 5**. *A new sample from class $$+$$ and the features $$\textbf{x} = \text{[blue, square]}$$ that is to be classified using the training data in Figure 4.](https://sebastianraschka.com/images/blog/2014/naive_bayes_1/toy_dataset_2.png)

**图 5**. *一个来自类别 \(+\) 的新样本，其特征为 \(\textbf{x} = \text{[blue, square]}\)，将使用图 4 中的训练数据对它进行分类。*

### 极大似然估计

*决策规则*可以定义为

\[\begin{split}
& \text{Classify sample as } + \text{ if} \\
& P(\omega=\text{+} \mid \textbf x = \text{[blue, square]}) \geq P(\omega=\text{-} \mid \textbf x = \text{[blue, square]})\\
& \text{else classify sample as} -.
\end{split}\]

在样本*独立同分布*的假设下，*先验概率*可以通过极大似然估计获得（即每个类别标签在训练集中出现的频率）：

\[\begin{split}
& P(\text{+}) = \frac{7}{12} = 0.58 \\
& P(\text{-}) = \frac{5}{12} = 0.42
\end{split}\]

在"颜色"和"形状"这两个特征相互独立的*朴素*假设下，*类条件概率*可以计算为各个单独条件概率的简单乘积。

通过极大似然估计，例如 \(P(\text{blue} \mid -)\) 就是训练集中所有属于类别 \(-\) 的样本里"蓝色"样本出现的频率。

\[\begin{split}
& P(\textbf{x} \mid +) = P(\text{blue} \mid +) \cdot P(\text{square} \mid +) = \frac{3}{7} \cdot \frac{5}{7} = 0.31 \\
& P(\textbf{x} \mid -) = P(\text{blue} \mid -) \cdot P(\text{square} \mid -) = \frac{3}{5} \cdot \frac{3}{5} = 0.36
\end{split}\]

现在，*后验概率*可以简单地计算为类条件概率与先验概率的乘积：

\[\begin{split}
& P(+ \mid \textbf{x}) = P(\textbf{x} \mid +) \cdot P(+) = 0.31 \cdot 0.58 = 0.18 \\
& P(- \mid \textbf{x}) = P(\textbf{x} \mid -) \cdot P(-) = 0.36 \cdot 0.42 = 0.15
\end{split}\]

### 分类

综合以上各步，把后验概率代入决策规则，就可以对新样本进行分类：

\[\begin{split}
&\text{If } P(+ \mid \textbf x) \geq P(\text{-} \mid \textbf{x}) \\
&\text{classify as }+, \\
& \text{else } \text{classify as } -
\end{split}\]

由于 \(0.18 > 0.15\)，该样本可被归类为 \(+\)。仔细回顾后验概率的计算过程，这个简单的例子展示了先验概率对决策规则的影响。如果两个类别的先验概率相等，那么这个新模式会被归类为 \(-\) 而不是 \(+\)。这一观察也凸显了*有代表性的*训练数据集的重要性；在实践中，通常还建议额外咨询领域专家来设定先验概率。

### 加性平滑

对于图 5 中的样本，分类过程十分直接。更棘手的情形是：样本的颜色属性取了一个训练集中从未出现过的"新"值，例如*黄色*，如图 6 所示。

![Figure 6.** *A new sample from class $$+$$ and the features $$\textbf{x} = \text{[yellow, square]}$$ that is to be classified using the training data in Figure 4](https://sebastianraschka.com/images/blog/2014/naive_bayes_1/toy_dataset_3.png)

**图 6.** *一个来自类别 \(+\) 的新样本，其特征为 \(\textbf{x} = \text{[yellow, square]}\)，将使用图 4 中的训练数据对它进行分类*

如果*黄色*在我们的训练集中从未出现，那么类条件概率将为 0，进而后验概率也将为 0，因为后验概率是先验概率与类条件概率的乘积。

\[\begin{split}
& P(\omega\_1 \mid \textbf x) = 0 \cdot 0.42 = 0 \\
& P(\omega\_2 \mid \textbf x) = 0 \cdot 0.58 = 0
\end{split}\]

为了避免*零*概率问题，可以向*多项式贝叶斯*模型中加入一个额外的平滑项。加性平滑最常见的变体是所谓的 *Lidstone 平滑*（\(\alpha<1\)）和*拉普拉斯平滑*（Laplace smoothing，\(\alpha=1\)）。

\[\hat{P}(x\_i \mid \omega\_j) = \frac{N\_{x\_i, \omega\_j}+\alpha}{N\_{\omega\_j} + \alpha \, d} \quad (i = (1, ..., d))\]

其中

- \(N\_{x\_i, \omega\_j}\)：特征 \(x\_i\) 在类别 \(\omega\_j\) 的样本中出现的次数。
- \(N\_{\omega\_j}\)：类别 \(\omega\_j\) 中所有特征的总数。
- \(\alpha\)：加性平滑参数。
- \(d\)：特征向量 \(\textbf x = [x\_1, ..., x\_d]\) 的维数。

## 朴素贝叶斯与文本分类

本节将介绍把朴素贝叶斯模型应用于文本分类任务所需的一些主要概念和流程。虽然这里的例子主要围绕一个二分类问题——把文本消息分为*垃圾*（spam）或*正常*（ham）信息——但同样的方法也适用于多分类问题，例如将文档划分到不同的主题领域（如"计算机科学"、"生物学"、"统计学"、"经济学"、"政治学"等）。

### 词袋模型

模式分类中最重要的子任务之一是*特征提取*与*特征选择*；好特征的三条主要标准如下：

- *显著性*。特征相对于问题领域而言是重要且有意义的。
- *不变性*。不变性通常在图像分类的语境下描述：特征对畸变、缩放、方向等不敏感。C. Yao 等人在 *Rotation-Invariant Features for Multi-Oriented Text Detection in Natural Images* 一文中给出了一个很好的例子[[7](#References)]。
- *判别性。*选出的特征在用于训练分类器时，应携带足以很好地区分不同模式的信息。

在拟合模型并使用机器学习算法进行训练之前，我们需要先思考如何把一个文本文档最好地表示为特征向量。*自然语言处理*中一个常用的模型是所谓的*词袋*（bag of words）模型。这个模型背后的想法确实和它的名字一样简单。首先是构建*词表*（vocabulary）——收集训练集中出现的所有不同的词，并为每个词关联其出现次数。这个词表可以理解为一个无冗余、顺序无关的元素集合。设 \(D\_1\) 和 \(D\_2\) 是训练集中的两个文档：

- \(D\_1\): "Each state has its own laws."
- \(D\_2\): "Every country has its own culture."

基于这两个文档，词表可以写成 \

\[\begin{split}
&V= \{each: 1, state: 1, has: 2, its: 2, own: 2, \\
& laws: 1, every: 1, country: 1, culture: 1\}
\end{split}\]

然后就可以用这个词表为各个文档构造 \(d\) 维特征向量，其维数等于词表中不同词的数量（\(d=\vert V \vert\)）。这个过程称为*向量化*（vectorization）。

**表 1.** *两个示例文档 \(D\_1\) 和 \(D\_2\) 的词袋表示。*

|  | each | state | has | its | own | laws | every | country | culture |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| \(\mathbf{x}\_{D1}\) | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |
| \(\mathbf{x}\_{D2}\) | 0 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 1 |
| \(\Sigma\) | 1 | 1 | 2 | 2 | 2 | 1 | 1 | 1 | 1 |

对于表 1 中的例子，有一个问题：特征向量中的 1 和 0 究竟是二值计数（某词在某文档中出现则为 1，否则为 0），还是绝对计数（该词在每个文档中出现的次数）？答案取决于朴素贝叶斯分类器采用哪种概率模型：*多项式*（Multinomial）模型还是*伯努利*（Bernoulli）模型——关于这两种概率模型的更多内容见*多元伯努利朴素贝叶斯*一节和*多项式朴素贝叶斯*一节。

#### 分词

*分词*（tokenization）描述的是把文本语料切分成单个元素的一般过程，这些元素可作为各种自然语言处理算法的输入。通常，分词还会伴随其他可选的处理步骤，例如去除停用词和标点符号、词干提取或词形还原，以及构建 *n-gram*。下面是一个简单但典型的分词步骤示例：把句子切分成单个词、去除标点符号，并把所有字母转换为小写。

**表 2.** *分词示例。*

![Naive bayes 1 tokenization 1](https://sebastianraschka.com/images/blog/2014/naive_bayes_1/tokenization-1.png)

#### 停用词

*停用词*（stop words）是指在文本语料中特别常见、因而被认为信息量相当低的词（例如 *so*、*and*、*or*、*the*……）。去除停用词的一种方法是对照特定语言的停用词词典进行检索。另一种方法是先把整个文本语料中的所有词按频率排序，从而生成一份*停用词表*（stop list）。停用词表在转换为无冗余的*集合*（set）之后，再用它从输入文档中删除那些排在该停用词表前 *n* 位的词。

**表 3.** *停用词去除示例。*

![Naive bayes 1 stop 1](https://sebastianraschka.com/images/blog/2014/naive_bayes_1/stop-1.png)

### 词干提取与词形还原

*词干提取*（stemming）描述的是把词转换为其词根形式的过程。最初的词干提取算法由 Martin F. Porter 于 1979 年提出，因而被称为 *Porter 词干提取器*（Porter stemmer）[[8](#References)]。

**表 4.** *Porter 词干提取示例。*

![Naive bayes 1 porter 1](https://sebastianraschka.com/images/blog/2014/naive_bayes_1/porter-1.png)

词干提取可能产生并不真实存在的词，例如上例中的 "thu"。与词干提取不同，*词形还原*（lemmatization）的目标是获得词的规范形式（语法上正确的形式），即所谓的*词元*（lemma）。词形还原在计算上比词干提取更困难、代价更高，而在实践中，词干提取和词形还原对文本分类性能的影响都很小[[9](#References)]。

**表 4.** *词形还原示例。*

![Naive bayes 1 lemma 1](https://sebastianraschka.com/images/blog/2014/naive_bayes_1/lemma-1.png)

（上述词干提取和词形还原示例是使用 Python 的 NLTK 库创建的，<http://www.nltk.org>。）

#### N-Gram

在 *n-gram* 模型中，一个 token 可以定义为 *n* 个元素的序列。最简单的情形是所谓的 *unigram*（1-gram），其中每个词恰好由一个单词、字母或符号组成。前面所有示例使用的都是 unigram。最优 *n* 值的选择取决于语言以及具体应用。例如，Andelka Zecevic 在他的研究中发现，\(3 \le n \le 7\) 的 *n*-gram 是判定塞尔维亚语文本文档作者身份的最佳选择[[10](#References)]。在另一项研究中，大小为 \(4 \le n \le 8\) 的 *n*-gram 在英文图书的作者身份判定中取得了最高准确率[11](#References)]，而 Kanaris 等人报告称，大小为 3 和 4 的 *n*-gram 在电子邮件反垃圾过滤中表现良好[[12](#References)]。

![Naive bayes 1 grams 1](https://sebastianraschka.com/images/blog/2014/naive_bayes_1/grams-1.png)

### 垃圾信息分类的决策规则

在垃圾信息分类的语境下，基于后验概率的朴素贝叶斯分类器决策规则可以表示为

\[\begin{split}
& \text{if } P( \omega = \text{spam} \mid \textbf{x}) \ge P(\omega = \text{ham} \mid \textbf{x}) \text{ classify as spam, }\\
& \text{else classify as ham. }
\end{split}\]

如*后验概率*一节所述，后验概率是类条件概率与先验概率的乘积；分母中的证据项由于对两个类别而言是常数，可以略去。

\[\begin{split}
& P(\omega = \text{spam} \mid \textbf{x}) = P(\textbf{x} \mid \omega = \text{spam}) \cdot P(\text{spam}) \\
& P(\omega = \text{ham} \mid \textbf{x}) = P(\textbf{x} \mid \omega = \text{ham}) \cdot P(\text{ham})
\end{split}\]

先验概率可以基于训练集中垃圾信息与正常信息的频率，通过极大似然估计获得：

\[\begin{split}
& \hat{P}(\omega = \text{spam}) = \frac {\text{# of spam msg.}}{\text{# of all msg.}} \\
& \hat{P}(\omega = \text{ham}) = \frac {\text{# of ham msg.}}{\text{# of all msg.}}
\end{split}\]

假设每篇文档中的词都是条件独立的（依据*朴素*假设），就可以用两种不同的模型来计算类条件概率：*多元伯努利*（Multi-variate Bernoulli）模型和*多项式*（Multinomial）模型。

### 多元伯努利朴素贝叶斯

*多元伯努利*模型基于二值数据：文档特征向量中的每个 token 都取值 1 或 0。特征向量有 \(m\) 个维度，其中 \(m\) 是整个词表中的词数（见*词袋模型*一节）；值 1 表示该词出现在该文档中，值 0 表示该词未出现在该文档中。伯努利试验可以写成

\[P(\textbf x \mid \omega\_j) = \prod\_{i=1}^{m} P(x\_i \mid \omega\_j)^b \cdot (1-P(x\_i \mid \omega\_j))^{(1-b)} \quad (b \in {0,1}).\]

设 \(\hat{P}(x\_i \mid \omega\_j)\) 为特定词（或 token）\(x\_i\) 出现在类别 \(\omega\_j\) 中的极大似然估计。

\begin{equation} \hat{P}(x\_i \mid \omega\_j) = \frac{df\_{xi, y} + 1}{df\_y + 2} \end{equation}

其中

- \(df\_{xi, y}\)：训练集中包含特征 \(x\_i\) 且属于类别 \(\omega\_j\) 的文档数量。
- \(df\_y\)：训练集中属于类别 \(\omega\_j\) 的文档数量。
- +1 和 +2 是*拉普拉斯平滑*的参数（见"加性平滑"一节）。

### 多项式朴素贝叶斯

#### 词频

除了二值之外，另一种刻画文本文档的方法是*词频*（term frequency，tf(t, d)）。词频通常定义为给定词项 *t*（即词或 token）在文档 *d* 中出现的次数（这种方法有时也称为*原始频率*，raw frequency）。在实践中，常用原始词频除以文档长度来对词频做归一化。

\[\text{normalized term frequency} = \frac{tf(t, d)}{n\_d}\]

其中

- \(tf(t, d)\)：原始词频（词项 \(t\) 在文档 \(d\) 中的计数）。
- \(n\_d\)：文档 \(d\) 中词项的总数。

然后可以基于训练数据，利用词频计算极大似然估计，从而估计多项式模型中的类条件概率：

\[\hat{P}(x\_i \mid \omega\_j) = \frac{\sum tf(x\_i, d \in \omega\_j) + \alpha}{\sum N\_{d \in \omega j} + \alpha \cdot V}\]

其中

- \(x\_i\)：某个样本的特征向量 \(\textbf x\) 中的一个词。
- \(\sum tf(x\_i, d \in \omega\_j)\)：训练样本中属于类别 \(\omega\_j\) 的所有文档里词 \(x\_i\) 的原始词频之和。
- \(\sum N\_{d \in \omega j}\)：训练集中类别 \(\omega\_j\) 的所有词频之和。
- \(\alpha\)：加性平滑参数（拉普拉斯平滑时 \(\alpha = 1\)）。
- \(V\)：词表大小（训练集中不同词的数量）。

在条件独立的*朴素*假设下，遇到文本 \(\textbf x\) 的类条件概率可以计算为各个词的似然的乘积。

\[P(\textbf x \mid \omega\_j) = P(x\_1 \mid \omega\_j) \cdot P(x\_2 \mid \omega\_j) \cdot \dotsc \cdot P(x\_n \mid \omega\_j) = \prod\_{i= 1}^{m} P(x\_i \mid \omega\_j)\]

#### 词频-逆文档频率

*词频-逆文档频率*（term frequency - inverse document frequency，Tf-idf）是刻画文本文档的另一种替代方法。它可以理解为一种加权的*词频*，在语料尚未去除停用词时尤其有用。Tf-idf 方法假设：一个词的重要性与它在所有文档中出现的频繁程度成反比。尽管 Tf-idf 最常用于各类文本挖掘任务（例如搜索引擎的网页排序）中按相关性对文档进行排序，它同样可以应用于基于朴素贝叶斯的文本分类。

\[\text{Tf-idf} = tf\_n(t,d) \cdot idf(t)\]

设 \(tf\_n(d,f)\) 为归一化词频，\(idf\) 为逆文档频率，其计算方式如下

\[idf(t) = \log\Bigg(\frac{n\_d}{n\_d(t)}\Bigg),\]

其中

- \(n\_d\)：文档总数。
- \(n\_d(t)\)：包含词项 \(t\) 的文档数量。

#### 多元伯努利模型与多项式模型的性能

实证比较提供的证据表明：当[词表大小](https://sebastianraschka.com/glossary/#vocabulary-size "Vocabulary Size")相对较大时，多项式模型往往优于多元伯努利模型[[13](#References)]。然而，机器学习算法的性能高度依赖于对特征的恰当选择。就朴素贝叶斯分类器与文本分类而言，性能上的巨大差异可能源于停用词去除、词干提取以及 token 长度等方面的不同选择[[14](#References)]。实践中建议：在为文本分类选择多元伯努利模型还是多项式模型之前，应先开展包含不同特征提取与特征选择步骤组合的对比研究。

## 朴素贝叶斯模型的变体

到目前为止，我们已经了解了两种面向类别数据的不同模型，即多元伯努利模型（见*伯努利贝叶斯*一节）和多项式模型（见*多项式贝叶斯*一节）——以及两种估计类条件概率的不同方法。在*连续变量*一节中，我们将简要介绍第三种模型：*高斯朴素贝叶斯*（Gaussian naive Bayes）。

### 连续变量

文本分类是类别数据的典型场景，但朴素贝叶斯同样可以用于连续数据。*鸢尾花*（Iris）数据集就是带连续特征的有监督分类任务的一个简单例子：Iris 数据集包含以厘米为单位测量的花瓣和萼片的宽度与长度。在朴素贝叶斯分类中处理连续数据的一种策略是对特征离散化、形成互不相同的类别，或者使用高斯核来计算类条件概率。假设各特征的概率分布服从正态（高斯）分布，高斯朴素贝叶斯模型可以写成如下形式

\[P(x\_{ik} \mid \omega) = \frac{1}{\sqrt{2\pi\sigma^2\_{\omega}}} \exp\left(-\frac{(x\_{ik} - \mu\_{\omega})^2}{2\sigma^2\_{\omega}}\right),\]

其中 \(\mu\)（样本均值）和 \(\sigma\)（标准差）是需要从训练数据中估计的参数。在朴素贝叶斯的条件独立假设下，类条件概率可以进一步计算为各单个概率的乘积：

\[P(\textbf x\_i \mid \omega) = \prod\_{k=1}^{d} P(\textbf x\_{ik} \mid \omega)\]

### 急切学习与懒惰学习算法

朴素贝叶斯分类器是一种*急切学习器*（eager learner），以分类新实例相对迅速而著称。急切学习器是指一旦数据可用就从训练数据集学出一个模型的学习算法。模型学得之后，做新预测时无须重新评估训练数据。对急切学习器来说，计算上最昂贵的步骤是建模步骤，而对新实例的分类则相对较快。

而*懒惰学习器*（lazy learner）则会记住训练数据集，并在预测新实例的类别标签时重新评估它。*懒惰学习*的优点是建模（训练）阶段相对较快。另一方面，由于需要重新评估训练数据，实际预测通常比急切学习器慢。懒惰学习器的另一个缺点是必须保留训练数据，这在存储空间上也可能代价不菲。*k 近邻*（k-nearest neighbor）算法是懒惰学习器的一个典型例子：每当遇到一个新实例，算法都会评估其 *k* 个最近邻来决定新实例的类别标签，例如通过*多数规则*（即把 *k* 个最近邻中出现最频繁的类别标签赋给新实例）。

感谢阅读。如果你喜欢这些内容，也可以[在 Twitter 上找到我](https://twitter.com/rasbt)，我会分享更多有用的内容。

## 参考文献

[1] I. Rish, “An empirical study of the naive bayes classifier,” in IJCAI 2001 workshop on empirical methods in artificial intelligence, pp. 41–46, 2001.

[2] P. Domingos and M. Pazzani, “On the optimality of the simple bayesian classifier under zero-one loss,” Machine learning, vol. 29, no. 2-3, pp. 103–130, 1997.

[3] J. Kazmierska and J. Malicki, “Application of the na ̈ıve bayesian classifier to optimize treatment deci- sions,” Radiotherapy and Oncology, vol. 86, no. 2, pp. 211–216, 2008.

[4] Q. Wang, G. M. Garrity, J. M. Tiedje, and J. R. Cole, “Naive bayesian classifier for rapid assignment of rrna sequences into the new bacterial taxonomy,” Applied and environmental microbiology, vol. 73, no. 16, pp. 5261–5267, 2007.
e}

[5] M. Sahami, S. Dumais, D. Heckerman, and E. Horvitz, “A bayesian approach to filtering junk e-mail,” in Learning for Text Categorization: Papers from the 1998 workshop, vol. 62, pp. 98–105, 1998.

[6] H. Zhang, “The optimality of naive bayes,” AA, vol. 1, no. 2, p. 3, 2004.

[7] C. Yao, X. Zhang, X. Bai, W. Liu, Y. Ma, and Z. Tu, “Rotation-invariant features for multi-oriented text detection in natural images,” PloS one, vol. 8, no. 8, p. e70173, 2013.

[8] M. F. Porter, “An algorithm for suffix stripping,” Program: electronic library and information systems, vol. 14, no. 3, pp. 130–137, 1980.
orithm}

[9] M. Toman, R. Tesar, and K. Jezek, “Influence of word normalization on text classification,” Proceedings of InSciT, pp. 354–358, 2006.

[10] A. Zevcevic, “N-gram based text classification according to authorship,” in Student Research Workshop, pp. 145–149, 2011.

[11] V. Keˇselj, F. Peng, N. Cercone, and C. Thomas, “N-gram-based author profiles for authorship attribution,” in Proceedings of the conference pacific association for computational linguistics, PACLING, vol. 3, pp. 255–264, 2003.

[12] I. Kanaris, K. Kanaris, I. Houvardas, and E. Stamatatos, “Words versus character n-grams for anti-spam filtering,” International Journal on Artificial Intelligence Tools, vol. 16, no. 06, pp. 1047–1067, 2007.

[13] A. McCallum, K. Nigam, et al., “A comparison of event models for naive bayes text classification,” in AAAI-98 workshop on learning for text categorization, vol. 752, pp. 41–48, Citeseer, 1998.

[14] L. M. Rudner and T. Liang, “Automated essay scoring using bayes’ theorem,” The Journal of Technology, Learning and Assessment, vol. 1, no. 2, 2002.
