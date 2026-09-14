---
title: "监督机器学习基础"
title_en: "Supervised Machine Learning Basics"
source: https://sebastianraschka.com/Articles/2014_intro_supervised_learning.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 监督机器学习基础

> 原文：[Supervised Machine Learning Basics](https://sebastianraschka.com/Articles/2014_intro_supervised_learning.html) · Sebastian Raschka's Articles

在开发我的下一个模式分类应用时，我意识到不妨退后一步，纵观一下模式分类的整体图景，这样既能把我之前讨论过的主题串联起来，也能为后续将要展开的主题做一个引子。

模式分类与机器学习是非常热门的话题，几乎被用于所有现代应用之中：邮局里的光学字符识别（OCR）、邮件客户端里的垃圾邮件过滤、超市里的条形码扫描仪……这样的例子不胜枚举。
在本文中，我想快速梳理一下典型监督学习任务的主要概念，作为后续文章以及各种学习算法与应用实现的入门导引。

## 机器学习与模式分类

预测建模（predictive modeling）是构建能够做出预测的模型的一般性概念。通常，这样的模型包含一个机器学习算法，该算法从训练数据集中学习某些属性，以便据此做出预测。
预测建模可以进一步划分为两个子领域：回归（regression）与模式分类（pattern classification）。回归模型基于对变量之间关系和趋势的分析，来对连续变量做出预测，例如在天气预报中预测未来几天的最高[温度](https://sebastianraschka.com/glossary/#temperature "Temperature")。
与回归模型不同，模式分类的任务是将离散的类别标签分配给特定的观测，作为预测的结果。回到上面的例子：天气预报中的一个模式分类任务可以是预测某一天是晴天、雨天还是雪天。

为了不迷失于种种可能性之中，本文的主要焦点将放在"模式分类"上，即把预定义的类别标签分配给特定实例、从而将其归入离散类别的一般方法。"实例"（instance）与"观测"（observation）或"样本"（sample）是同义词，描述的是由一个或多个特征（feature，与"属性"attribute 同义）组成的"对象"。

## 监督学习、无监督学习与强化学习

模式分类任务可以归为两大子类：监督学习与无监督学习。在监督学习中，用于构建分类模型的数据集中的类别标签是已知的。例如，一个用于垃圾邮件过滤的数据集既包含垃圾邮件（spam），也包含"正常邮件"（ham，即非垃圾邮件）。在监督学习问题中，我们知道训练集中哪封邮件是垃圾邮件、哪封是正常邮件，我们会利用这一信息来训练模型，以便对新的、未见过的邮件进行分类。

![Intro supervised learning classify example](https://sebastianraschka.com/images/blog/2014/intro_supervised_learning/classify_example.webp)

上图展示了一个针对具有两个随机变量的样本的分类任务示例；训练数据（带类别标签）显示在散点图中。红色虚线表示线性（左）或二次（右）决策边界，用于定义决策区域 R1 和 R2。新的观测将被赋予类别标签"w1"或"w2"，具体取决于它们落入哪个决策区域。我们已经可以预料到，我们对未见实例的分类不会"完美"，会有一定比例的样本很可能被错误分类。

> 如果你想了解这些决策边界是如何计算出来的，相应的 IPython notebook 可以在我的模式分类代码库的[统计模式分类示例](https://github.com/rasbt/pattern_classification#statistical-pattern-classification-examples)部分找到。

与此相对，无监督学习处理的是无标签的实例，类别需要从非结构化的数据集中推断出来。通常，无监督学习会采用聚类技术，基于某种相似性（或距离）度量来对无标签样本进行分组。

第三类学习算法由"强化学习"（reinforcement learning）一词描述。在这类学习中，模型是通过一系列动作来学习的，其目标是最小化/最大化一个"奖励函数"。奖励函数可以通过惩罚"坏动作"和/或奖励"好动作"来实现最大化。强化学习的一个流行例子是利用环境反馈来训练自动驾驶汽车。最近，我还偶然看到另一个不错的强化学习例子：训练[游戏 Flappy Bird 自己玩自己](http://sarvagyavaish.github.io/FlappyBirdRL/)。

## 监督学习——一个典型的工作流程

时至今日，著名的"鸢尾花"（Iris）数据集可能是在"数据科学"领域介绍各种概念时最常用的示例之一。Iris 数据集由 R. A. Fisher 创建并用于他[1936 年的判别分析研究](http://onlinelibrary.wiley.com/doi/10.1111/j.1469-1809.1936.tb02137.x/abstract)，现在可以在 UCI 机器学习仓库中免费[获取](https://archive.ics.uci.edu/ml/datasets/Iris)。

![Intro supervised learning iris petal sepal 1](https://sebastianraschka.com/images/blog/2014/intro_supervised_learning/iris_petal_sepal_1.webp)

在这里，它是监督分类任务的一个完美示例，其类别标签是三种花的物种：Setosa、Virginica 和 Versicolor。150 个实例（单朵花）中的每一个都由四个特征组成：

- 萼片宽度
- 萼片长度
- 花瓣宽度
- 花瓣高度

（均以厘米为单位测量。）

### 可视化

在处理一个新数据集时，采用简单的可视化技术来做探索性数据分析往往很有用，因为人眼在发现模式方面非常强大。然而，有时我们面对的数据超过三个维度，无法在单张图中呈现：克服这种限制的一种方法是把属性集拆分成两两一对，然后绘制散点图矩阵。在实践中，"好用且有效"的可视化技术的选择在很大程度上取决于数据的类型、特征空间的维度，以及手头要解决的问题。

下面给出了 Iris 数据集的若干种或多或少有用的可视化示例。

![Intro supervised learning matplotlib ex](https://sebastianraschka.com/images/blog/2014/intro_supervised_learning/matplotlib_ex.webp)

创建这些图所用的代码可在 IPython notebook [Matplotlib 示例——用于探索性数据分析的可视化技术](https://github.com/rasbt/pattern\_classification/blob/master/data\_viz/matplotlib\_viz\_gallery.ipynb)中找到。

观察上面的那些图，尤其是散点图和（一维）直方图，我们已经可以看出：由于三个不同花类之间的重叠更小，花瓣尺寸比萼片宽度和长度包含更多的判别信息。例如，这一信息可以用于特征选择，以去除噪声并缩减数据集的规模。

### 工作流程图

在接下来的部分中，我们将了解典型监督学习任务的一些主要步骤，下图应该能让我们直观地理解这些步骤之间是如何衔接的。

![Intro supervised learning supervised learning flowchart](https://sebastianraschka.com/images/blog/2014/intro_supervised_learning/supervised_learning_flowchart.webp)

该流程图也提供 [PDF 版本](https://github.com/rasbt/pattern_classification/blob/master/PDFs/supervised_learning_flowchart.pdf)。

### 原始数据收集与特征提取

当我们下载 Iris 数据集时，会注意到它已经处于"良好状态"，而且 R. A. Fisher 似乎已经替我们做了一些初步的"预处理"：没有缺失数据，特征均为数值型，可以直接供学习算法使用。
不过，让我们假设 Iris 数据集的原始数据是由一系列图像组成的。在这种情况下，第一步预处理（特征提取）可能就需要对这些图像进行缩放、平移和旋转，以获得以厘米为单位的萼片和花瓣尺寸。

叶片遮挡可能是一个会导致数据缺失的问题：许多机器学习算法在数据集中存在缺失数据时将无法正确工作，因此"忽略"缺失数据可能并不可行。如果稀疏度（即数据集中空白单元格的数量）不太高，通常建议删除包含缺失值的样本行，或删除存在数据缺失的属性列。处理缺失数据的另一种策略是插补（imputation）：使用某些统计量来替换缺失值，而不是将其完全删除。对于类别型数据，可以用出现频率最高的类别来插补缺失值；对于数值型属性，则可以使用样本均值来插补缺失值。一般来说，通过 k 近邻（k-nearest neighbor）插补进行再代入，被认为优于用整体样本均值来替换缺失数据。

其他与特征提取相关的有趣方法还可以包括对花瓣和萼片测量值的聚合，例如花瓣或萼片的宽度与高度之比。

### 采样

假设我们已经从原始数据中提取了某些特征（这里是萼片宽度、萼片长度、花瓣宽度和花瓣长度），接下来我们会把数据集随机划分为训练数据集和测试数据集。训练数据集将用于训练模型，而测试数据集的用途则是在最终阶段评估最终模型的性能。

重要的是，我们在计算预测误差指标时只使用测试数据集一次，以避免过拟合（overfitting）。过拟合会产生在训练数据上表现良好但泛化能力差的分类器，以至于在新模式上的预测误差相对较高。因此，在模型的构建与调优阶段，会使用交叉验证（cross-validation）等技术来评估分类性能。除了重复使用测试数据集进行模型评估之外，另一种替代策略是创建第三个数据集，即所谓的验证数据集（validation dataset）。

### 交叉验证

交叉验证是评估特征选择、降维和学习算法不同组合的最有用技术之一。交叉验证有多种变体，其中最常见的可能就是 k 折交叉验证（k-fold cross-validation）。
在 k 折交叉验证中，原始训练数据集被拆分成 *k* 个不同的子集（即所谓的"折"，fold），其中 1 折保留作测试集，其余 k-1 折用于训练模型。例如，如果我们把 *k* 设为 4（即 4 折），就会用原始训练集的 3 个不同子集来训练模型，第 4 折用于评估。经过 4 次迭代之后，我们最终可以计算出模型的平均错误率（以及标准差），从而对模型的泛化能力有一个大致的了解。

![Intro supervised learning cross validation 001 small](https://sebastianraschka.com/images/blog/2014/intro_supervised_learning/cross-validation-001_small.webp)

### 归一化

归一化（normalization）以及其他特征缩放（feature scaling）技术往往是必需的，以便在不同属性之间进行比较（例如在聚类分析中计算距离或相似度），尤其是在属性使用不同量纲测量的情况下（例如开尔文与摄氏温度）；对大多数机器学习算法而言，对特征进行适当的缩放是一项必要前提。

"归一化"一词常被当作"Min-Max 缩放"（Min-Max scaling）的同义词使用：将属性缩放到某个特定范围内，例如 0 到 1。

![Intro supervised learning minmax scaling](https://sebastianraschka.com/images/blog/2014/intro_supervised_learning/minmax_scaling.webp)

另一种常见方法是（z-score）"标准化"（standardization）或"缩放到单位方差"：每个样本减去属性的均值再除以标准差，使该属性具有标准正态分布的性质（μ=0, σ=1）。

![Intro supervised learning zscore](https://sebastianraschka.com/images/blog/2014/intro_supervised_learning/zscore.webp)

我们必须牢记的一个重要要点是：如果在训练数据集上使用了任何归一化或变换技术，那么在测试数据集以及新的未见数据上也必须使用相同的参数。

更多细节可以在另一篇文章中找到：[关于特征缩放与归一化以及标准化对机器学习算法的影响](https://sebastianraschka.com/Articles/2014_about_feature_scaling.html)。

### 特征选择与降维

区分特征选择（feature selection）与降维（dimensionality reduction）乍看可能有点反直觉，因为特征选择最终也会（降低维度）得到一个更小的特征空间。
在实践中，"特征选择"与"降维"这两个术语的关键区别在于：特征选择保留的是"原始特征轴"，而降维通常涉及某种变换技术。

这两种方法的主要目的是去除噪声、通过只保留"有用的"（具判别性的）信息来提高计算效率，以及避免过拟合（即"维度灾难"，curse of dimensionality）。

在特征选择中，我们只想保留那些"有意义的"特征——即有助于构建一个"好"分类器的特征。例如，如果我们有一大堆描述鸢尾花的属性（颜色、高度等），特征选择可以包括把可用数据缩减为描述花瓣和萼片尺寸的那 4 项测量值。或者，如果我们从这 4 个属性（萼片和花瓣的长度与宽度）出发，还可以进一步把选择范围缩小到花瓣的长度和宽度，从而把特征空间从 4 维降到 2 维。特征选择通常基于领域知识（请注意，咨询领域专家总是有帮助的）或探索性分析，比如我们前面看到的直方图或散点图。要找到某一规模的、能使分类模型性能最优的特征子集，需要进行穷举搜索——即对所有可能的组合进行采样。在实践中，由于计算能力的限制，这种方法可能并不可行，因此人们会使用序列特征选择（sequential feature selection，[Python 特征选择算法](https://rasbt.github.io/mlxtend/user_guide/feature_selection/SequentialFeatureSelector/)）或遗传算法来选出一个次优的特征子集。

![Intro supervised learning pca lda](https://sebastianraschka.com/images/blog/2014/intro_supervised_learning/pca_lda.webp)

常用的降维技术是线性变换，例如主成分分析（Principal Component Analysis, PCA）和线性判别分析（Linear Discriminant Analysis, LDA）。PCA 可以被描述为一种"无监督"算法，因为它"忽略"类别标签，其目标是找到使数据集方差最大化的方向（即所谓的"主成分"）。与 PCA 相比，LDA 是"有监督"的，它计算出的方向（"线性判别器"，linear discriminant）将代表使多个类别之间分离程度最大化的坐标轴。

![Intro supervised learning iris pca lda](https://sebastianraschka.com/images/blog/2014/intro_supervised_learning/iris_pca_lda.webp)

关于 PCA 和 LDA 的更多细节可以在以下两篇文章中找到：

- [逐步讲解线性判别分析](https://sebastianraschka.com/Articles/2014_python_lda.html)
- [用 Python 逐步实现主成分分析（PCA）](https://sebastianraschka.com/Articles/2014_pca_step_by_step.html)

下图展示了经过线性判别分析（LDA）变换后，绘制在 2 维特征子空间上的鸢尾花数据。黑线表示示例性的线性决策边界，它们将特征空间划分为三个决策区域（R1、R2、R3）。基于这些决策区域，新的观测可以被归类到三种不同的花种之中：R1 → Virginica，R2 → Versicolor，R3 → Setosa。

![Intro supervised learning lda iris](https://sebastianraschka.com/images/blog/2014/intro_supervised_learning/lda_iris.webp)

### 学习算法与超参数调优

![Intro supervised learning learning algorithm 1](https://sebastianraschka.com/images/blog/2014/intro_supervised_learning/learning_algorithm_1.webp)

学习算法的种类多得不计其数，其中最流行的那些算法的细节非常适合用单独的文章和应用来展开。这里只对四种常用的监督学习算法做一个非常简略的概述：

- **支持向量机（Support Vector Machine, SVM）**是一种分类方法，它对能够分开两个或多个类别的超平面进行采样。最终，具有最大间隔（margin）的超平面会被保留下来，其中"间隔"定义为样本点到超平面的最小距离。构成间隔的样本点被称为支持向量（support vector），它们确立了最终的 SVM 模型。
- **贝叶斯分类器（Bayes classifier）**基于统计模型（即贝叶斯定理：基于先验概率和所谓的似然来计算后验概率）。朴素贝叶斯（Naive Bayes）分类器假设所有属性条件独立，因此似然的计算被简化为：在给定某个类别标签的条件下，观察到各个属性的条件概率的乘积。
- **人工神经网络（Artificial Neural Network, ANN）**是图状分类器，它模仿人类或动物"大脑"的结构，其中相互连接的节点代表神经元。
- **决策树分类器（decision tree classifier）**是树状图，图中的节点会对特定的一组特征测试某些条件，分支则将决策逐层延伸至叶节点。叶节点代表图中最底层的层级，并决定类别标签。最优的树通过最小化基尼不纯度（Gini impurity）或最大化信息增益（information gain）训练得到。

针对 Iris 数据集的一棵非常简单的决策树可以画成这样：![Intro supervised learning decision tree 1](https://sebastianraschka.com/images/blog/2014/intro_supervised_learning/decision_tree_1.webp)

超参数（hyperparameter）是分类器或估计器的这样一类参数：它们不是在机器学习步骤中直接从训练数据学得的，而是被单独优化的。超参数优化的目标是提升分类器的性能，并使学习算法获得良好的泛化能力。一种流行的超参数优化方法是网格搜索（Grid Search）。通常，网格搜索被实现为对候选参数值的穷举搜索（与随机参数优化相对）。在一个模型所有可能的参数组合都被评估完之后，最优的组合将被保留下来。

### 预测误差指标与模型选择

一个便于使用的性能评估工具是所谓的混淆矩阵（confusion matrix），它是一个方阵，其行与列以"实际类别"对"预测类别"的形式列出实例数量。

一个简单的"垃圾邮件 vs. 正常邮件"分类的混淆矩阵可能如下所示：

![Intro supervised learning confusion matrix 2](https://sebastianraschka.com/images/blog/2014/intro_supervised_learning/confusion_matrix_2.webp)

人们常用预测的"准确率"（accuracy）或"错误率"（error）来报告分类性能。
准确率定义为正确分类的数量占总样本数的比例；尽管计算方式不同，它常被当作特异性/精确率（specificity/precision）的同义词使用。准确率的计算公式为

![Intro supervised learning accuracy 1](https://sebastianraschka.com/images/blog/2014/intro_supervised_learning/accuracy_1.gif)

其中 TP=True Positives（真阳性）、TN=True Negatives（真阴性）、P=Positives（阳性）、N=Negatives（阴性）。

分类模型的经验误差可以用 1-Accuracy 来计算。

然而，选择合适的预测误差指标高度依赖具体任务。在"垃圾邮件"分类的语境下，我们会特别希望假阳性率较低。当然，把一封垃圾邮件误判为正常邮件固然令人恼火，但总好过因为把"正常邮件"误判为"垃圾邮件"而错过任何重要信息。

在诸如"垃圾邮件"分类这类二分类问题中，调整分类器的一种便捷方法是受试者工作特征（Receiver Operating Characteristic，ROC，或称 ROC 曲线）。

![Intro supervised learning roc curve 1](https://sebastianraschka.com/images/blog/2014/intro_supervised_learning/roc_curve_1.webp)

其他衡量分类性能的指标还有**灵敏度（Sensitivity）**、**特异度（Specificity）**、**召回率（Recall）**和**精确率（Precision）**。

- 灵敏度（与召回率同义）和精确率评估的是二分类问题的"真阳性率"（True Positive Rate）：即对"阳性/真"情形做出正确预测的概率（例如，在尝试预测某种疾病时，为确实患有该病的患者正确预测出疾病）。

![Intro supervised learning sensitivity](https://sebastianraschka.com/images/blog/2014/intro_supervised_learning/sensitivity.gif)

![Intro supervised learning precision](https://sebastianraschka.com/images/blog/2014/intro_supervised_learning/precision.gif)

- 特异度描述的是二分类问题的"真阴性率"（True Negative Rate）：即对"阴性/无"情形做出正确预测的概率（例如，在尝试预测某种疾病时，对健康人预测其没有患病）。

![Intro supervised learning specificity](https://sebastianraschka.com/images/blog/2014/intro_supervised_learning/specificity.gif)

在典型的监督学习工作流程中，我们会先评估特征子空间、学习算法和超参数的各种不同组合，然后再选出性能令人满意的模型。如前所述，交叉验证是进行此类评估的好方法，可以避免在我们的训练数据上过拟合。

感谢阅读。如果你喜欢这些内容，也可以[在 Twitter 上找到我](https://twitter.com/rasbt)，我会在那里分享更多有用的内容。

## 延伸阅读

我希望这篇关于监督学习与模式分类领域的简短介绍，多少能够激发你的兴趣。如果你想深入学习，下面是一些值得一读的资料！

我最喜欢的书之一、大概也是这个主题最常被推荐的入门书，当属 Richard O. Duda、Peter E. Hart 和 David G. Stork 合著的《Pattern Classification》。

> "我不认为任何想要教授模式识别或在其中从事严肃工作的人可以忽略这本书，因为它是那种人人都希望抽出时间从头到尾通读一遍的书！"（Pattern Analysis & Applications Journal, 2001）

> "对于模式识别领域任何认真的学生或从业者而言，本书都是独一无二的教科书与专业参考书。"（Mathematical Reviews, Issue 2001）

尽管这篇综述发表于将近 15 年前，但它仍然是一篇非常值得一读的出色文章：

*Jain, Anil K., Robert P. W. Duin, and Jianchang Mao. 2000. ["Statistical Pattern Recognition: A Review."](https://ieeexplore.ieee.org/document/824819) Pattern Analysis and Machine Intelligence, IEEE Transactions on 22 (1): 4–37.*

如果这些不适合你，也可以浏览我整理的涵盖机器学习、模式分类与人工智能领域的[免费电子书小合集](https://github.com/rasbt/pattern_classification/blob/master/resources/machine_learning_ebooks.md)。
