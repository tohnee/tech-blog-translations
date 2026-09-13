---
title: "如何解释机器学习模型的预测？"
title_en: "How to Explain the Prediction of a Machine Learning Model?"
source: https://lilianweng.github.io/posts/2017-08-01-interpretation/
crawled: 2026-09-08
translated: 2026-09-08
---

# 如何解释机器学习模型的预测？

> 原文：[How to Explain the Prediction of a Machine Learning Model?](https://lilianweng.github.io/posts/2017-08-01-interpretation/) · Lilian Weng（翁荔）

> 本文回顾了模型可解释性方面的一些研究，涵盖两个方面：(i) 本身可解释的模型及其专属解释方法；(ii) 解释黑盒模型的各种途径。文末还附上了关于可解释人工智能（XAI）的开放讨论。

机器学习模型已开始渗透到医疗健康、司法系统和金融行业等关键领域。因此，弄清模型如何做出决策，并确保决策过程符合伦理要求或法律法规，已成为一种必需。

与此同时，深度学习模型的快速增长进一步推高了解释复杂模型的需求。人们渴望将 AI 的力量充分应用于日常生活的关键方面。然而，如果对模型没有足够的信任，或者缺乏解释意外行为的高效流程，这是很难做到的——尤其考虑到深度神经网络天生就是*黑盒*。

想想以下几种情形：

1. 金融行业受到高度监管，放贷机构依法必须做出公平的决策，并在拒绝贷款申请时解释其信贷模型、给出理由。
2. 医疗诊断模型关系到人的生命。我们如何能有足够的信心，按照一个黑盒模型的指示去治疗病人？
3. 当在法庭上使用犯罪决策模型预测再次犯罪的风险时，我们必须确保模型的行为是公平、诚实且无歧视的。
4. 如果一辆自动驾驶汽车突然行为异常而我们无法解释原因，我们还敢放心地让这项技术大规模上路吗？

在 [Affirm](https://www.affirm.com/)，我们每天发放数万笔分期贷款，当风控模型拒绝某人的贷款申请时，必须提供拒绝理由。这是我深入研究并写下这篇文章的众多动机之一。模型可解释性是机器学习中一个很大的领域。这篇综述无意穷尽所有研究，只希望作为一个起点。

---

## 可解释的模型

Lipton（2017）在一篇理论综述论文 ["The mythos of model interpretability"](https://arxiv.org/pdf/1606.03490.pdf) 中总结了一个可解释模型应具备的性质：人类可以复现（*"simulatability"，可仿真性）计算过程，对算法有完整理解（*"algorithmic transparency"，算法透明性），且模型的每个组成部分都有直观的解释（*"decomposability"，可分解性）。

许多经典模型结构相对简单，自然带有专属的解释方法。同时，新的工具也在不断被开发出来，帮助构建更好的可解释模型（[Been, Khanna, & Koyejo, 2016](http://papers.nips.cc/paper/6300-examples-are-not-enough-learn-to-criticize-criticism-for-interpretability.pdf)；[Lakkaraju, Bach & Leskovec, 2016](http://www.kdd.org/kdd2016/papers/files/rpp1067-lakkarajuA.pdf)）。

### 回归

线性回归模型的一般形式为：

$$y = w_0 + w_1 x_1 + w_2 x_2 + … + w_n x_n$$

系数描述了自变量每增加一个单位所引起的响应变化。除非特征已经过标准化（参见 sklearn.preprocessing.[StandardScalar](http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html#sklearn.preprocessing.StandardScaler) 和 [RobustScaler](http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.RobustScaler.html#sklearn.preprocessing.RobustScaler)），否则系数不能直接比较，因为不同特征的一个"单位"可能指代截然不同的东西。在未标准化的情况下，乘积 $$w_i \dot x_i$$ 可用于量化某一特征对响应的贡献。

### 朴素贝叶斯

朴素贝叶斯（Naive Bayes）之所以叫"朴素"，是因为它建立在一个非常简化的假设之上：特征相互独立，各自独立地贡献于输出。

给定特征向量 $$\mathbf{x} = [x_1, x_2, \dots, x_n]$$ 和类别标签 $$c \in \{1, 2, \dots, C\}$$，该数据点属于此类的概率为：

$$
\begin{aligned}
p(c | x_1, x_2, \dots, x_n) 
&\propto p(c, x_1, x_2, \dots, x_n)\\
&\propto p(c) p(x_1 | c) p(x_2 | c) \dots p(x_n | c)\\
&\propto p(c) \prod_{i=1}^n p(x_i | c).
\end{aligned}
$$

朴素贝叶斯分类器于是定义为：

$$\hat{y} = \arg\max_{c \in 1, \dots, C} p(c) \prod_{i=1}^n p(x_i | c)$$

因为模型在训练中已经学到了先验 $$p(x_i \vert c)$$，单个特征取值的贡献可以很容易地用后验 $$p(c \vert x_i) = p(c)p(x_i \vert c) / p(x_i)$$ 来度量。

### 决策树 / 决策列表

决策列表（decision list）是一组布尔函数，通常以 `if... then... else...` 这样的语法构建。if 条件包含一个涉及一个或多个特征的函数和一个布尔输出。决策列表天生具有良好的可解释性，并且可以以树结构可视化。许多关于决策列表的研究由医疗应用驱动，在那些场景中可解释性几乎与模型本身同等重要。

下面简要介绍几类决策列表：

- [Falling Rule Lists（FRL）](http://proceedings.mlr.press/v38/wang15a.pdf)（Wang and Rudin, 2015）对特征取值完全强制了单调性。以二分类为例，一个关键点是：与每条规则关联的预测 $$Y=1$$ 的概率随着沿决策列表向下移动而递减。
- [Bayesian Rule List（BRL）](https://arxiv.org/abs/1511.01644)（Letham et al., 2015）是一个生成式模型，能在所有可能的决策列表上产生后验分布。
- [Interpretable Decision Sets（IDS）](https://cs.stanford.edu/people/jure/pubs/interpretable-kdd16.pdf)（Lakkaraju, Bach & Leskovec, 2016）是一个创建分类规则集合的预测框架。其学习过程同时针对准确率和可解释性进行优化。IDS 与我稍后会描述的用于解释黑盒模型的 BETA 方法（[下文](https://lilianweng.github.io/posts/2017-08-01-interpretation/#beta-black-box-explanation-through-transparent-approximations)）密切相关。

### 随机森林

奇怪的是，很多人认为[随机森林](http://www.math.univ-toulouse.fr/~agarivie/Telecom/apprentissage/articles/randomforest2001.pdf)（Random Forests）模型是黑盒，其实并非如此。考虑到随机森林的输出是大量独立决策树的多数投票，而每棵树本身自然是可解释的。

如果我们一次只考察一棵树，衡量单个特征的影响并不难。随机森林的全局特征重要性可以通过集成中所有树的节点不纯度总减少量的平均值来量化（"平均不纯度减少"，mean decrease impurity）。

对单个实例而言，由于所有树中的决策路径都被良好记录，我们可以用父节点中数据点的均值与子节点均值之差来近似这次分裂的贡献。更多内容可阅读这一系列博客：[Interpreting Random Forests](http://blog.datadive.net/interpreting-random-forests/)。

## 解释黑盒模型

很多模型在设计上并不追求可解释。解释黑盒模型的方法旨在从训练好的模型中提取信息来论证其预测结果，而不必知道模型内部如何运作。让解释过程独立于模型实现，对现实应用很有好处：即使基础模型在不断升级和改进，构建在其上的解释引擎也无须担心这些变化。

无须顾虑模型的透明性与可解释性，我们可以通过增加更多参数和非线性计算赋予模型更强的表达能力。深度神经网络正是这样在涉及丰富输入的任务上取得成功的。

对于解释应该以何种形式呈现并没有硬性要求，但首要目标主要是回答：**我能信任这个模型吗？** 当我们依赖模型做出关键或生死攸关的决策时，必须事先确保模型值得信赖。

解释框架应在两个目标之间取得平衡：
- **保真度（fidelity）**：解释所给出的预测应尽可能与原始模型一致。
- **可解释性（interpretability）**：解释应足够简单，使人类能够理解。

> 旁注：接下来的三种方法都为局部解释（local interpretation）而设计。

### 预测分解

[Robnik-Sikonja and Kononenko (2008)](http://lkm.fri.uni-lj.si/rmarko/papers/RobnikSikonjaKononenko08-TKDE.pdf) 提出通过度量原始预测与省略一组特征后的预测之间的差异，来解释模型对单个实例的预测。

假设我们需要为一个分类模型 $$f: \mathbf{X} \rightarrow \mathbf{Y}$$ 生成解释。给定一个数据点 $$x \in X$$，它由属性 $$A_i$$（$$i = 1, \dots, a$$）的 $$a$$ 个独立取值组成，并被标记为类别 $$y \in Y$$。*预测差异（prediction difference）* 通过计算"知道"与"不知道" $$A_i$$ 时模型预测概率的差值来量化：

$$\text{probDiff}_i (y | x)  = p(y| x) - p(y | x \backslash A_i)$$

（论文还讨论了用几率比（odds ratio）或基于熵的信息度量来量化预测差异。）

**问题**：如果目标模型输出的是概率，那很好，得到 $$ p(y \vert x) $$ 很直接。否则，模型预测必须经过适当的建模后校准（post-modeling calibration）才能把预测分数转换为概率。这一校准层又增加了一层复杂性。

**另一个问题**：如果通过把 $$A_i$$ 替换为缺失值（如 `None`、`NaN` 等）来生成 $$x \backslash A_i$$，我们就得依赖模型内部的缺失值填补机制。一个用中位数填补缺失的模型，其输出会与用特殊占位符填补的模型大相径庭。论文中给出的一个解决方案是：用该特征的所有可能取值替换 $$A_i$$，然后按每个取值在数据中出现的可能性对预测加权求和：

$$
\begin{aligned}
p(y \vert x \backslash A_i)
&= \sum_{s=1}^{m_i} p(A_i=a_s \vert x \backslash A_i) p(y \vert x \leftarrow A_i=a_s) \\
&\approx \sum_{s=1}^{m_i} p(A_i=a_s) p(y \vert x \leftarrow A_i=a_s)
\end{aligned}
$$

其中 $$p(y \vert x \leftarrow A_i=a_s)$$ 是把 $$x$$ 的特征向量中的特征 $$A_i$$ 替换为值 $$a_s$$ 后得到标签 $$y$$ 的概率。训练集中 $$A_i$$ 共有 $$m_i$$ 个不同取值。

借助省略已知特征时的预测差异度量，我们就可以*分解*每个特征对预测的影响。

![预测分解示例](https://lilianweng.github.io/posts/2017-08-01-interpretation/interpretability_prediction_decomposition.png)

*图 1：对一个预测 [Titanic 数据集](https://www.kaggle.com/c/titanic/data)中一位男性成年头等舱乘客是否存活的 SVM 模型的解释。信息差异（information difference）与概率差异非常相似，但它度量的是在不知道 $$A_i$$ 的情况下确定 $$y$$ 为真所需的信息量：$$\text{infDiff}_i (y|x) = \log_2 p(y|x) - \log_2 p(y|x \backslash A_i)$$。针对特定实例的解释用深色条表示。浅色半高条是给定属性取值的平均正向与负向解释。在本例中，身为男性成年乘客使存活的可能性大大降低；舱位等级的影响则没那么大。*

### 局部梯度解释向量

该方法（[Baehrens, et al. 2010](http://www.jmlr.org/papers/volume11/baehrens10a/baehrens10a.pdf)）能够解释任意非线性分类算法所做的局部决策，它使用局部梯度来刻画一个数据点需要怎样移动才能改变其预测标签。

假设我们有一个在数据集 $$X$$ 上训练的[贝叶斯分类器](https://en.wikipedia.org/wiki/Bayes_classifier)，它输出类别标签 $$Y$$ 上的概率 $$p(Y=y \vert X=x)$$。类别标签 $$y$$ 取自标签池 $$\{1, 2, \dots, C\}$$。该贝叶斯分类器构造为：

$$ f^{*}(x)  = \arg \min_{c \in \{1, \dots, C\}} p(Y \neq c \vert X = x) $$

*局部解释向量（local explanation vector）* 定义为概率预测函数在测试点 $$x = x_0$$ 处的导数。该向量中数值很大的分量意味着一个对模型决策有重大影响的特征；正号表示增大该特征会降低 $$x_0$$ 被归入 $$f^{*}(x_0)$$ 的概率。

然而，这种方法要求模型输出是概率（与上面的["预测分解"](https://lilianweng.github.io/posts/2017-08-01-interpretation/#prediction-decomposition)方法类似）。如果原始模型（记为 $$f$$）没有校准为输出概率怎么办？论文建议，我们可以用另一个形式上类似贝叶斯分类器 $$f^{*}$$ 的分类器来近似 $$f$$：

(1) 对训练数据应用 [Parzen 窗](https://en.wikipedia.org/?title=Parzen_window&redirect=no)来估计加权类别密度：

$$\hat{p}_{\sigma}(x, y=c) = \frac{1}{n} \sum_{i \in I_c} k_{\sigma} (x - x_i) $$

其中 $$I_c$$ 是被模型 $$f$$ 判为类别 $$c$$ 的数据点索引集合，$$I_c = \{i \vert f(x_i) = c\}$$。$$k_{\sigma}$$ 是一个核函数。高斯核是[众多候选](https://en.wikipedia.org/wiki/Kernel_(statistics)#Kernel_functions_in_common_use)中流行的一种。

(2) 然后，应用贝叶斯规则近似所有类别的概率 $$p(Y=c \vert X=x)$$：

$$
\begin{aligned}
\hat{p}_{\sigma}(y=c | x)
&= \frac{\hat{p}_{\sigma}(x, y=c)}{\hat{p}_{\sigma}(x, y=c) + \hat{p}_{\sigma}(x, y \neq c)} \\
&\approx \frac{\sum_{i \in I_c} k_{\sigma} (x - x_i)}{\sum_i k_{\sigma} (x - x_i)}
\end{aligned}
$$

(3) 最终估计的贝叶斯分类器形如：

$$\hat{f}_{\sigma} = \arg\min_{c \in \{1, \dots, C\}} \hat{p}_{\sigma}(y \neq c \vert x)$$

注意，我们可以用原始模型 $$f$$ 生成任意多的带标签数据，不受训练数据规模的限制。超参数 $$\sigma$$ 的选取以最大化 $$\hat{f}_{\sigma}(x) = f(x)$$ 的机会为目标，以实现高保真度。

![GPC 的局部梯度解释向量](https://lilianweng.github.io/posts/2017-08-01-interpretation/interpretability_local_gradient.png)

*图 2：局部梯度解释向量应用于高斯过程分类器（GPC）简单物体分类的示例。GPC 模型天然输出概率。(a) 展示训练点及其标签，红色（正类 1）、蓝色（负类 -1）。(b) 展示正类的概率函数。(c-d) 展示局部梯度和局部解释向量的方向。*

> 旁注：可以看到，上面两种方法都要求模型预测是概率。模型输出的校准又增加了一层复杂性。

### LIME（局部可解释的模型无关解释）

[LIME](https://github.com/marcotcr/lime) 是 *local interpretable model-agnostic explanation*（局部可解释的模型无关解释）的缩写，它能在我们关心的预测点附近对黑盒模型进行局部近似（[Ribeiro, Singh, & Guestrin, 2016](https://arxiv.org/pdf/1602.04938.pdf)）。

同上，把黑盒模型记为 $$f$$。LIME 的步骤如下：

(1) 将数据集转换为可解释的数据表示：$$x \Rightarrow x_b$$。
- 文本分类器：指示一个词出现与否的二值向量
- 图像分类器：指示一片连续的相似像素块（超像素，super-pixel）出现与否的二值向量

![可解释数据表示](https://lilianweng.github.io/posts/2017-08-01-interpretation/LIME_interpretable_representation.png)

*图 3：将图像转换为可解释数据表示的示例。（图片来源：[www.oreilly.com/learning/introduction-to-local-interpretable-model-agnostic-explanations-lime](https://www.oreilly.com/learning/introduction-to-local-interpretable-model-agnostic-explanations-lime)）*

(2) 给定预测 $$f(x)$$ 及其对应的可解释数据表示 $$x_b$$，我们在 $$x_b$$ 附近采样：均匀随机地抽取 $$x_b$$ 的非零元素，抽取的数目也均匀采样。该过程生成扰动样本 $$z_b$$，其中只包含 $$x_b$$ 非零元素的一部分。

然后我们把 $$z_b$$ 还原为原始输入 $$z$$，由目标模型得到预测分数 $$f(z)$$。

利用许多这样的采样数据点 $$z_b \in \mathcal{Z}_b$$ 及其模型预测，我们可以学习一个具有局部保真度的解释模型（形式可以简单如一个回归）。采样数据点依据其与 $$x_b$$ 的接近程度被赋予不同权重。论文使用了带预处理的 lasso 回归，事先选出最重要的前 $$k$$ 个特征，称为 "K-LASSO"。

![LIME 示意图](https://lilianweng.github.io/posts/2017-08-01-interpretation/LIME_illustration.png)

*图 4：粉色和蓝色区域是黑盒模型 $$f$$ 预测出的两个类别。红色大叉是被解释的点，其他较小的叉（被 $$f$$ 预测为粉色）和点（被 $$f$$ 预测为蓝色）是采样数据点。即使模型可能非常复杂，我们仍能学习一个如灰色虚线般简单的局部解释模型。（图片来源：[homes.cs.washington.edu/~marcotcr/blog/lime](https://homes.cs.washington.edu/~marcotcr/blog/lime/)）*

检验解释是否合理可以直接判断模型是否可信，因为模型有时会捕捉到虚假的相关性或泛化。论文中一个有趣的例子是对一个区分"基督教"与"无神论"的 SVM 文本分类器应用 LIME。该模型准确率相当不错（留出测试集上 94%！），但 LIME 的解释表明，决策依据的理由非常武断，比如统计 "re"、"posting"、"host" 这些与"基督教"和"无神论"都无直接关系的词。经过这样的诊断，我们得知：即使模型给出漂亮的准确率，它也不可信。这也为改进模型指明了方向，比如对文本做更好的预处理。

![LIME](https://lilianweng.github.io/posts/2017-08-01-interpretation/LIME.png)
*图 5：如何在图像分类器上使用 LIME 的示意图。（图片来源：[www.oreilly.com/learning/introduction-to-local-interpretable-model-agnostic-explanations-lime](https://www.oreilly.com/learning/introduction-to-local-interpretable-model-agnostic-explanations-lime)）*

想要更详细的非论文式讲解，请阅读作者的[这篇博客](https://www.oreilly.com/learning/introduction-to-local-interpretable-model-agnostic-explanations-lime)，写得非常好。

> 旁注：局部解释模型应当比全局解释容易，但更难维护（想想[维度灾难](https://en.wikipedia.org/wiki/Curse_of_dimensionality)）。下面介绍的方法旨在解释模型的整体行为。然而，全局方法无法捕捉细粒度的解释——比如某个特征在这一区域很重要，在另一区域却完全不重要。

### 特征选择

本质上，所有经典的特征选择方法（[Yang and Pedersen, 1997](http://www.surdeanu.info/mihai/teaching/ista555-spring15/readings/yang97comparative.pdf)；[Guyon and Elisseeff, 2003](http://www.jmlr.org/papers/volume3/guyon03a/guyon03a.pdf)）都可以视为对模型的全局解释。特征选择方法分解多个特征的贡献，使我们能够按单个特征的影响来解释模型的整体输出。

关于特征选择的资料非常多，本文就跳过这个话题了。

### BETA（通过透明近似做黑盒解释）

[BETA](https://arxiv.org/abs/1707.01154) 是 *black box explanation through transparent approximations*（通过透明近似做黑盒解释）的缩写，与[可解释决策集](https://cs.stanford.edu/people/jure/pubs/interpretable-kdd16.pdf)（Interpretable Decision Sets，Lakkaraju, Bach & Leskovec, 2016）密切相关。BETA 学习一个紧凑的两层决策集，其中每条规则都无歧义地解释模型行为的一部分。

作者提出了一个新颖的目标函数，使学习过程针对**高保真度**（解释与模型高度一致）、**低歧义性**（解释中的决策规则很少重叠）和**高可解释性**（解释决策集轻量且小巧）进行优化。这些方面被合并进一个目标函数中共同优化。

![BETA](https://lilianweng.github.io/posts/2017-08-01-interpretation/BETA.png)

*图 6：优秀模型解释的各项要求指标：保真度、无歧义性、可解释性。给定目标模型 $$\mathcal{B}$$，其解释是一个两层的决策集 $$\Re$$，包含一组规则 $${(q_1, s_1, c_1), \dots, (q_M, s_M, c_M)}$$，其中 $$q_i$$ 和 $$s_i$$ 是形如（特征, 运算符, 取值）的谓词合取，$$c_i$$ 是类别标签。详见[论文](https://arxiv.org/abs/1707.01154)。（图片来源：[arxiv.org/abs/1707.01154](https://arxiv.org/abs/1707.01154)）*

## 可解释人工智能

这一节的名称借自 DARPA 项目 ["Explainable Artificial Intelligence"](https://www.darpa.mil/program/explainable-artificial-intelligence)。可解释 AI（XAI）计划旨在开发更可解释的模型，使人类能够理解、适当信任并有效管理新一代人工智能技术。

随着深度学习应用的进展，人们开始担心[即使模型变坏了我们可能也永远无从知晓](https://www.technologyreview.com/s/601860/if-a-driverless-car-goes-bad-we-may-never-know-why/)。复杂的结构、数量庞大的可学习参数、非线性的数学运算以及[一些奇特的性质](https://arxiv.org/abs/1312.6199)（Szegedy et al., 2014）导致了深度神经网络的不可解释性，造就了真正的黑盒。尽管深度学习的威力恰恰源于这种复杂性——它能更灵活地捕捉真实世界数据中丰富而复杂的模式。

关于[**对抗样本**]([OpenAI Blog: Robust Adversarial Examples](https://blog.openai.com/robust-adversarial-inputs/), [Attacking Machine Learning with Adversarial Examples](https://blog.openai.com/adversarial-example-research/), [Goodfellow, Shlens & Szegedy, 2015](https://arxiv.org/pdf/1412.6572.pdf)；[Nguyen, Yosinski, & Clune, 2015]http://www.cv-foundation.org/openaccess/content_cvpr_2015/papers/Nguyen_Deep_Neural_Networks_2015_CVPR_paper.pdf) 的研究为 AI 应用的鲁棒性与安全性敲响了警钟。有时模型会表现出非预期、意料之外且不可预测的行为，而我们没有快速或良好的策略来解释原因。

![BETA](https://lilianweng.github.io/posts/2017-08-01-interpretation/adversarial_examples.png)
*图 7：对抗样本示意图。(a-d) 是在原始图像上叠加人类难以察觉的噪声后生成的对抗图像（[Szegedy et al., 2013](https://arxiv.org/abs/1312.6199)）。训练良好的神经网络模型能正确分类原始图像，却在对抗图像上失败。(e-h) 是生成的图案（[Nguyen, Yosinski & Clune, 2015](http://www.cv-foundation.org/openaccess/content_cvpr_2015/papers/Nguyen_Deep_Neural_Networks_2015_CVPR_paper.pdf)）。训练良好的神经网络模型分别将它们标记为 (e) 校车、(f) 吉他、(g) 孔雀和 (h) 京巴犬。（图片来源：[Wang, Raj & Xing, 2017](https://arxiv.org/pdf/1702.07800.pdf)）*

Nvidia 最近开发了[一种可视化方法](https://blogs.nvidia.com/blog/2017/04/27/how-nvidias-neural-net-makes-decisions/)，用于展示其自动驾驶汽车决策过程中最重要的像素点。这种可视化让我们得以窥见 AI 如何思考、系统在驾驶时依赖什么。如果 AI 认为重要的东西与人类做类似决策的方式一致，我们自然会对这个黑盒模型更有信心。

这个不断演化的领域每天都在涌现激动人心的新闻和发现。希望我的文章能给你一些指引，鼓励你在这个方向上继续探索 :)

---

*如果你发现本文中的错误，请毫不犹豫地联系我 [lilian dot wengweng at gmail dot com]，我会非常乐意立即修正！*

未完待续 :)

## 参考文献

[1] Zachary C. Lipton. ["The mythos of model interpretability."](https://arxiv.org/pdf/1606.03490.pdf) arXiv preprint arXiv:1606.03490 (2016). 

[2] Been Kim, Rajiv Khanna, and Oluwasanmi O. Koyejo. "Examples are not enough, learn to criticize! criticism for interpretability." Advances in Neural Information Processing Systems. 2016.

[3] Himabindu Lakkaraju, Stephen H. Bach, and Jure Leskovec. ["Interpretable decision sets: A joint framework for description and prediction."](http://www.kdd.org/kdd2016/papers/files/rpp1067-lakkarajuA.pdf) Proc. 22nd ACM SIGKDD Intl. Conf. on Knowledge Discovery and Data Mining. ACM, 2016.

[4] Robnik-Šikonja, Marko, and Igor Kononenko. ["Explaining classifications for individual instances."](http://lkm.fri.uni-lj.si/rmarko/papers/RobnikSikonjaKononenko08-TKDE.pdf) IEEE Transactions on Knowledge and Data Engineering 20.5 (2008): 589-600.

[5] Baehrens, David, et al. ["How to explain individual classification decisions."](http://www.jmlr.org/papers/volume11/baehrens10a/baehrens10a.pdf) Journal of Machine Learning Research 11.Jun (2010): 1803-1831.

[6] Marco Tulio Ribeiro, Sameer Singh, and Carlos Guestrin. ["Why should I trust you?: Explaining the predictions of any classifier."](https://arxiv.org/pdf/1602.04938.pdf) Proc. 22nd ACM SIGKDD Intl. Conf. on Knowledge Discovery and Data Mining. ACM, 2016.

[7] Yiming Yang, and Jan O. Pedersen. ["A comparative study on feature selection in text categorization."](http://www.surdeanu.info/mihai/teaching/ista555-spring15/readings/yang97comparative.pdf) Intl. Conf. on Machine Learning. Vol. 97. 1997.

[8] Isabelle Guyon, and André Elisseeff. ["An introduction to variable and feature selection."](http://www.jmlr.org/papers/volume3/guyon03a/guyon03a.pdf) Journal of Machine Learning Research 3.Mar (2003): 1157-1182.

[9] Ian J. Goodfellow, Jonathon Shlens, and Christian Szegedy. ["Explaining and harnessing adversarial examples."](https://arxiv.org/pdf/1412.6572.pdf)  ICLR 2015.

[10] Christian Szegedy, Wojciech Zaremba, Ilya Sutskever, Joan Bruna, Dumitru Erhan, Ian Goodfellow, Rob Fergus. ["Intriguing properties of neural networks."](https://arxiv.org/abs/1312.6199) Intl. Conf. on Learning Representations (2014)

[11] Nguyen, Anh, Jason Yosinski, and Jeff Clune. ["Deep neural networks are easily fooled: High confidence predictions for unrecognizable images."](http://www.cv-foundation.org/openaccess/content_cvpr_2015/papers/Nguyen_Deep_Neural_Networks_2015_CVPR_paper.pdf) Proc. IEEE Conference on Computer Vision and Pattern Recognition. 2015.

[12] Benjamin Letham, Cynthia Rudin, Tyler H. McCormick, and David Madigan. ["Interpretable classifiers using rules and Bayesian analysis: Building a better stroke prediction model."](https://arxiv.org/abs/1511.01644) The Annals of Applied Statistics 9, No. 3 (2015): 1350-1371.

[13] Haohan Wang, Bhiksha Raj, and Eric P. Xing. ["On the Origin of Deep Learning."](https://arxiv.org/pdf/1702.07800.pdf) arXiv preprint arXiv:1702.07800 (2017).

[14] [OpenAI Blog: Robust Adversarial Examples](https://blog.openai.com/robust-adversarial-inputs/)

[15] [Attacking Machine Learning with Adversarial Examples](https://blog.openai.com/adversarial-example-research/)

[16] [Reading an AI Car's Mind: How NVIDIA's Neural Net Makes Decisions](https://blogs.nvidia.com/blog/2017/04/27/how-nvidias-neural-net-makes-decisions/)
