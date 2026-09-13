---
title: "可解释机器学习"
title_en: "Interpretable Machine Learning"
source: https://sebastianraschka.com/blog/2020/interpretable-ml-1.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 可解释机器学习

> 原文：[Interpretable Machine Learning](https://sebastianraschka.com/blog/2020/interpretable-ml-1.html)

在这篇博文中，我将介绍 Christoph Molnar 的《Interpretable Machine Learning》（《可解释机器学习》）一书。在阅读过程中，我做了大量笔记，其中一部分是这本书的要点，用于充实我的个人 Wiki 和关于该主题的个人笔记。以这些笔记为模板，这篇博文最终演变成了一种颇为奇怪的混合体——介于书评、评注和教程之间。它绝谈不上详尽，如果你想学习机器学习与可解释性（interpretability），我推荐直接阅读这本书本身。

（在一篇较早的文章中，我提到过把"多读些书"作为 2020 年的新年承诺。目前进展还算顺利——2020 年至今我已经读了 20 本书。不过这些书大多是非虚构类，只有一小部分是教科书。等有时间的时候，我觉得写一些短篇博文来评论它们会格外有趣。）

这篇博文分为两部分。第一部分是我对《Interpretable Machine Learning》这本书的一些想法。第二部分则讨论作为可解释模型的线性回归和逻辑回归，并附上 Python 代码示例。

## 第一部分：关于《Interpretable Machine Learning》一书的想法

*声明：我想说明的是，我与本书作者没有任何关联。我写这篇文章并非出于私交。我没有收到这本书的赠阅本，我所写的一切都是我诚实、公正的看法。*

据我所知，《Interpretable Machine Learning》一书最早于 2018 年出现在网上。它由慕尼黑路德维希-马克西米利安大学（Ludwig Maximilian University of Munich）的统计学博士生 Christoph Molnar 撰写并自出版（[https://christophm.github.io](https://christophm.github.io/)）。正如作者所言，这本书"将随着时间的推移不断改进，并会加入更多章节。"这是如何实现的呢？这本书可以在线免费阅读，这一点非常棒：<https://christophm.github.io/interpretable-ml-book/>。就我个人而言，我从 Lulu 订购了一本按需印刷的纸质版（链接在书的网站上提供），一方面是为了支持作者，另一方面也是因为手捧一本老式纸质书时，我能更专注地阅读较长的文本。

这本书涵盖的主要内容是：关于可解释性的术语与不同的思考方式（第 1-3 章）、本身相对较易解释的具体模型（第 4 章），以及用于解释模型和预测的模型无关方法（第 5、6 章）。对每个有意阅读本书的人来说，一个重要前提是：本书聚焦于表格数据集和监督机器学习。如果你感兴趣的是深度学习或无监督学习（例如聚类分析等），那么这本书可能不适合你。我认为这种"聚焦"是件好事，因为它有助于让内容更易上手，例如书中大多使用相同或相似的数据集来对比各种方法。另外，纸质版已经有约 300 页，"可解释深度学习"（Interpretable Deep Learning）实在是一个适合另立项目的好主题——谁知道呢，说不定作者已经在写了！

把我手中 2020 年初拿到的纸质版目录与在线版目录对比，可以发现好几个部分已经更新。例如，在线版如今新增了关于 SHAP（Shapley additive explanations）和神经网络解释（Neural Network Interpretation）的章节。关于这本书的一点小批评是，书中存在不少不一致之处。

![Interpretable ml 1 book](https://sebastianraschka.com/images/blog/2020/interpretable-ml-1/book.webp)

书中零星有一些拼写错误和不一致之处（美式英语与英式英语混用、自然对数时而写作 *ln* 时而写作 *log*，等等），但都不是什么大问题，而且我相当确信作者已经在线上版本中修正了这些问题。总体而言，阅读这本书的过程非常愉快，我也很喜欢它平易近人的写作风格。

不过有一点需要指出：这本书没有包含代码示例。书中的图表和示例似乎是用 R 制作的——作者可能在网上分享了这些代码文件，但书中并未涉及或讨论它们（更新：我后来发现，一些代码示例可以在 GitHub 上获取：https://github.com/christophM/interpretable-ml-book/tree/master/scripts）。同样，这未必是缺点，我喜欢它让这本书不受编程语言限制。我认为这本书的重点在于总结、解释并比较可解释机器学习的各种技术与选项，而不是提供一份动手编程的教程。我相信，等你读完这本书、决定了想在当前项目中采用哪些技术之后，在网上找到代码示例不会遇到任何困难。

总体来说，这是一本对初学者友好的好书——如果你已经是这方面的专家，或者希望看到更形式化的论述，这本书可能不适合你。就我个人而言，尽管我熟悉其中许多主题并在实践中使用过，我仍然学到了很多有用的东西，也很喜欢书中把各种技术放在一起、在相互对照的语境中加以讨论的方式。这是一本读起来相当快的书，但很有价值。其中的一些表述和对比，在我下次开展合作型应用机器学习项目、需要选择具体模型或方法时，很可能派上用场。

无论如何，如果你不确定这本书是否对你有用，不妨直接在网上翻阅一些章节看看：<https://christophm.github.io/interpretable-ml-book/>。

## 第二部分：广义线性模型作为可解释机器学习模型的思考（附 Python 代码示例）

### 关于本文

介绍完这本书本身之后，在这一部分，我想就若干精选主题展开讨论，分享我的一些想法，并提供一些可供参考的代码示例。（这些主题基于书中讨论的内容，我只聚焦于线性回归和逻辑回归这两种*可解释模型*。也许在未来的文章中，我会讨论基于树的模型、模型无关方法以及基于示例的解释。）

这篇博文不是对整本书的复述。相反，我挑选了我觉得特别有趣、或者想结合自己的想法和 Python 代码示例加以扩展的具体主题。请注意，我假设读者已经听说过、最好还实际使用过这里讨论的机器学习算法，即线性回归和逻辑回归。这样本文就不会变成一篇冗长的机器学习入门教程，而可以专注于这些模型的可解释性方面。

### 关于模型可解释性的几点思考

在介绍一小部分技术之前，先让我谈谈对可解释性的一些想法和评论。在大多数场景下，我们都希望模型具有相当高的可解释性，因为我们想理解模型的行为。然而在实践中，我们通常要在模型的预测性能和可解释程度之间做出权衡。根据我的经验，那些可以归为"较简单"的模型（例如较短的决策树）更容易解释和理解，但可能不如"更复杂"的模型（例如随机森林——决策树的集成）效果好。

在我的研究合作中，我通常遇到两大类任务或问题：我们想理解（1）模型为什么以及如何做出预测，或者（2）变量之间的关系是什么（这通常指特征与目标变量之间的关系）。在这两种情况下，我们都希望模型相对准确。举例来说，如果模型本身就表现不佳，我们通常不会在实践中使用它，因此也就不关心如何理解它的预测。类似地，如果模型无法可靠地从观测特征预测目标变量，我们也不会相信它能就特征与目标之间的关系给出有用的洞见。（不过，一个在大数据集上训练但拟合效果很差的线性回归模型，至少能告诉我们：特征与目标之间的关系不是线性的。）

遗憾的是，在选择性能-可解释性权衡最优的模型或方法时，并没有什么万能灵药，这也是为什么建立对各种技术的储备和理解如此重要。

### 线性回归

线性回归是一个经典模型——它可能是跨领域、跨学科中被研究得最透彻、应用最广泛的模型。线性回归在可解释性上的一个优势在于特征与连续目标变量之间的线性关系，以及模型的单调性。只要线性回归的各项假设都得到满足——特征经过归一化（处于同一尺度）、彼此之间没有强相关、并呈现同方差性（在整个特征取值范围内方差恒定）——我们就可以通过查看模型权重来判断对应特征的重要程度。如果目标结果关于特征服从正态分布，我们还可以附加置信区间。（注意，即使特征本身不服从正态分布，根据中心极限定理，只要样本数量足够大，你同样可以构造这些置信区间。）

置信区间为我们提供了关于"真实"权重参数的信息（即如果我们能获得整个总体的数据时会得到的权重参数）。在实践中，我们可以把权重参数看作一种估计，因为它基于训练数据集中的数据。置信区间因容易被误读而"声名狼藉"，但它们能提供非常有用的信息。例如，一个 95% 置信区间意味着：对无穷多个训练数据集分别构造置信区间，其中 95% 的区间会包含真实参数（这里指回归模型的权重）。

为什么置信区间在线性回归的语境中特别有意思？它们为我们提供了关于确定性（或不确定性）的信息，以及某个结果是否*具有统计显著性*（statistically significant）——也就是说，它是否可能只是偶然造成的。如果你还记得统计学导论课程中的学生 t 检验（student t-test）：如果一个置信区间不包含原假设，那么该测量结果就是统计显著的。对于 95% 置信区间（或在 \(\alpha=0.05\) 水平上的 t 检验），这意味着我们错误地拒绝原假设（假阳性）的概率为 5%。在线性回归和模型权重的语境中，假设我们得到某个模型权重的 95% 置信区间与 0 重叠，这意味着我们没有充分的证据去否定"该特征不包含任何关于目标变量的信息"这一看法。简单转述一下：一个与 0 重叠的 95% 置信区间意味着该权重对应的特征变量对预测没有用处。

那么，如何围绕线性回归的权重系数构造置信区间呢？大多数统计学入门教材都会概述这一过程，为方便起见，维基百科上也有一个有用的页面总结了这一方法（<https://en.wikipedia.org/wiki/Simple_linear_regression#Confidence_intervals>），可以概括如下：

\[\text{CI}\_{1-\alpha}^{w\_j} = \big[w\_j - t\_{\alpha / 2, n-2} \times SE(w\_j), w\_j + t\_{\alpha / 2, n-2} \times SE(w\_j) \big],\]

其中 \(w\_j\) 是回归权重系数。注意 \(\alpha\) 是我们选定的显著性水平；例如，要构造 95% 置信区间，我们令 \(\alpha=0.05\)，使得 \(1-0.05 = 0.95\)。\(t\) 值服从自由度为 \(n-2\) 的学生 t 分布。\(SE\) 是标准误，计算方式如下：

\[S E\left(w\_{i}\right)=\left(\frac{\sqrt{M S E}}{\sqrt{\sum\_{i}\left(x\_{j}^{(i)}-\bar{x}\_{i}\right)^{2}}}\right)=\left(\frac{\sqrt{\frac{1}{n-2} \sum\_{i}\left(y^{(i)}-y^{(i)}\right)^{2}}}{\sqrt{\sum\_{i}\left(x\_{j}^{(i)}-\bar{x}\_{j}\right)^{2}}}\right).\]

#### 代码示例

为了让这些概念更加具体，让我们用 Python 看一个实际例子。这里我们使用上文维基百科置信区间链接中引用的数据，即"30-39 岁美国女性样本中，女性平均体重（质量）作为其身高的函数"。在下面的例子和文字中，我们在指体重时使用（身体）"质量（mass）"一词而不是"重量（weight）"，以避免与"权重（weight）"一词发生混淆——后者在线性回归语境中指模型系数。

```python
from sklearn.preprocessing import StandardScaler
import numpy as np

# https://en.wikipedia.org/wiki/Simple_linear_regression#Confidence_intervals
# This data set gives average masses for women as a function of their height in a sample of American women of age 30–39. 

height_in_m = [1.47, 1.50, 1.52, 1.55, 1.57, 1.60, 1.63, 1.65, 1.68, 1.70, 1.73, 1.75, 1.78, 1.80, 1.83]
mass_in_kg = [52.21, 53.12, 54.48, 55.84, 57.20, 58.57, 59.93, 61.29, 63.11, 64.47, 66.28, 68.10, 69.92, 72.19, 74.46]

np.random.seed(0)
rand1 = np.random.normal(size=len(height_in_m), scale=10, loc=5)
rand2 = np.random.normal(size=len(height_in_m))

X_train = np.array([(i, j, k) for i, j, k in zip(height_in_m, rand1, rand2)])
y_train = np.array(mass_in_kg)

sc_features = StandardScaler()
sc_target = StandardScaler()

X_std = sc_features.fit_transform(X_train)
y_std = sc_target.fit_transform(y_train.reshape(-1, 1)).flatten()
```

上面的代码为接下来的线性回归示例准备了训练数据集。注意，我们向数据集中加入了来自两个不同正态分布的随机样本，从而得到一个三特征的数据集。我们还对数据做了标准化，以便更直观地比较和解读线性回归模型权重。

就我个人而言，我喜欢先用散点图查看数据集，确保它的格式和缩放都没有问题，也不会有什么意外的"惊喜"。这也是一种直观检查各项假设是否满足的好办法——只有满足了这些假设（即特征之间（相对）不相关），模型权重之间才能相互比较。

```python
import matplotlib.pyplot as plt
from mlxtend.plotting import scatterplotmatrix

scatterplotmatrix(X_std, names=['Height','Rand 1', 'Rand 2'], 
                  figsize=(6, 5))
plt.tight_layout()
plt.show()
```

![Interpretable ml 1 linear scatter](https://sebastianraschka.com/images/blog/2020/interpretable-ml-1/linear-scatter.webp)

归一化（或标准化）数据集的一个优点是所有特征都处于同一尺度，这意味着我们可以直接比较不同权重，从而识别出重要的特征（权重越大，对预测的影响越大）。对目标变量做标准化是可选的，但有一个不错的副作用：我们不必再操心截距项，因为它恒为 0。

下面的代码片段拟合一个线性回归模型，并绘制权重系数：

```python
from sklearn.linear_model import LinearRegression

lr = LinearRegression()
lr.fit(X_std, y_std)

fig, ax = plt.subplots()
ax.bar([0, 1, 2], lr.coef_)

ax.set_xticks([0, 1, 2])
ax.set_xticklabels([f'Height\n({lr.coef_[0]:.3f})',
                    f'Random 1\n({lr.coef_[1]:.3f})',
                    f'Random 2\n({lr.coef_[2]:.3f})'])
plt.ylabel('Magnitude')
plt.show()
```

![Interpretable ml 1 linear regression weights](https://sebastianraschka.com/images/blog/2020/interpretable-ml-1/linear-regression-weights.webp)

从上面可视化的权重系数可以看到，"Height（身高）"是对预测影响最大的特征，两个随机特征（Random 1 和 Random 2）对模型预测几乎没有影响。由于基于权重 \(w\_i\) 和特征 \(x\_i\) 的预测定义为

\[\hat{y} = b + \sum\_{i=1} w\_ix\_i\]

我们知道，标准化身高每增加 1 个单位，预测值（标准化体重）就增加 0.999 个单位（因为 \(w\_{\text{height}}=0.999\)），即

\[\hat{y}\_{x\_\text{height} + 1} = \hat{y} +x\_\text{height}w\_{\text{height}} = \hat{y} +w\_{\text{height}}.\]

不过，标准化后的特征使得解读原始特征与目标变量之间的关系变得稍微麻烦一些。要想知道目标增加 0.999 个单位在未标准化的预测（以厘米计的身高）上意味着多少，我们必须把 z 分数标准化后的目标变回原始尺度。换言之，我们需要抵消标准化公式

\[z'\_{j} = \frac{z\_j - \mu\_j}{\sigma\_j},\]

也就是

\[z\_{j} = z'\_j \times \sigma\_j + \mu\_j.\]

在上面两个等式中，\(z\_j\) 可以表示目标变量（\(y\)）、预测值（\(\hat{y}\)）或第 \(j\) 个特征（\(x\_j\)），因为适用的概念相同。

回到上面的例子：对于某个给定输入，模型预测 \(\hat{y}=0.5\)（65.477 公斤）。我们把标准化身高增加 1，预测值随之增加到约 \(\hat{y}=1.5\)（72.276 公斤）。这一"增加 1"在目标变量原始尺度 \(y\) 上意味着多少？可以这样计算：

\[(1.5\sigma\_{\text{mass}}+\mu\_{\text{mass}}) - (0.5\sigma\_{\text{mass}}+\mu\_{\text{mass}}) = \sigma\_{\text{mass}}.\]

利用之前定义的 `StandardScaler` 实例中保存的均值和方差，我们可以用代码来实现：

```python
# y = 0.5 in kg
print(0.5 * np.sqrt(sc_target.var_) + sc_target.mean_)
# [65.4774427]

# y = 1.5 in kg
print(1.5 * np.sqrt(sc_target.var_) + sc_target.mean_)
# [72.2763281]

# sigma_mass:
print(np.sqrt(sc_target.var_))
# [6.7988854]
```

接下来，在可视化模型权重、并探索标准化特征与目标值之间的关系之后，我们来计算模型权重的置信区间。使用前面定义的公式

\[\text{CI}\_{1-\alpha}^{w\_j} = \big[w\_j - t\_{\alpha / 2, n-2} \times SE(w\_j), w\_j + t\_{\alpha / 2, n-2} \times SE(w\_j) \big]\]

以及

\[S E\left(w\_{i}\right)=\left(\frac{\sqrt{M S E}}{\sqrt{\sum\_{i}\left(x\_{j}^{(i)}-\bar{x}\_{i}\right)^{2}}}\right)=\left(\frac{\sqrt{\frac{1}{n-2} \sum\_{i}\left(y^{(i)}-y^{(i)}\right)^{2}}}{\sqrt{\sum\_{i}\left(x\_{j}^{(i)}-\bar{x}\_{j}\right)^{2}}}\right),\]

具体计算如下：

```python
def std_err_linearregression(y_true, y_pred, x):
    n = len(y_true)
    mse = np.sum((y_true - y_pred)**2) / (n-2)
    std_err = (np.sqrt(mse) / np.sqrt(np.sum((x - np.mean(x, axis=0))**2, axis=0)))
    return std_err

def weight_intervals(n, weight, std_err, alpha=0.05):
    t_value = stats.t.ppf(1 - alpha/2, df=n - 2)
    temp = t_value * std_err
    lower = weight - temp
    upper = weight + temp

    return lower, upper

y_pred = lr.predict(X_std)
std_err = std_err_linearregression(y_std, y_pred, X_std)
lower, upper = weight_intervals(len(y_std), lr.coef_, std_err)
```

然后我们可以在误差条图（errorbar plot）中可视化权重系数和置信区间：

```python
fig, ax = plt.subplots()

ax.hlines(0, xmin=-0.1, xmax=2.2, linestyle='dashed', color='skyblue')
ax.errorbar([0, 1, 2], lr.coef_, yerr=upper - lr.coef_, fmt='.k')

ax.set_xticks([0, 1, 2])
ax.set_xticklabels([f'Height\n({lr.coef_[0]:.3f})',
                    f'Random 1\n({lr.coef_[1]:.3f})',
                    f'Random 2\n({lr.coef_[2]:.3f})'])
plt.ylabel('Magnitude');
```

![Interpretable ml 1 linear errbar1](https://sebastianraschka.com/images/blog/2020/interpretable-ml-1/linear-errbar1.webp)

从上图可以看出，只有身高特征在 \(\alpha=0.05\) 水平上具有统计显著性。

如果你使用 Statsmodels，获得置信区间有一个更简单的方法：

```python
import statsmodels.api as sm

mod = sm.OLS(y_std, X_std)
res = mod.fit()
lower, upper = res.conf_int(0.05)[:, 0], res.conf_int(0.05)[:, 1]

########################
fig, ax = plt.subplots()

ax.hlines(0, xmin=-0.1, xmax=2.2, linestyle='dashed', color='skyblue')
ax.errorbar([0, 1, 2], res.params, yerr=upper - res.params, fmt='.k')

ax.set_xticks([0, 1, 2])
ax.set_xticklabels([f'Height\n({lr.coef_[0]:.3f})',
                    f'Random 1\n({lr.coef_[1]:.3f})',
                    f'Random 2\n({lr.coef_[2]:.3f})'])
plt.ylabel('Magnitude');
```

![Interpretable ml 1 linear errbar1](https://sebastianraschka.com/images/blog/2020/interpretable-ml-1/linear-errbar1.webp)

### 逻辑回归

逻辑回归（logistic regression）作为一种广义线性模型（generalized linear model，GLM），在解读模型权重方面享有与线性回归几乎相同的好处。（当然，两者的用途不同：逻辑回归用于预测类别标签，线性回归用于在线性尺度上预测连续目标。）

与线性回归类似，如果我们把逻辑回归模型拟合到标准化特征上，就可以通过权重的大小来了解各对应特征之间的相对重要性。一般来说，权重越大，对应特征对预测的影响越大。

线性回归和逻辑回归都是广义线性模型，这意味着两者都使用特征的加权和

\[z = b + w\_1x\_1 + w\_2x\_2 + ...+ w\_mx\_m = b + \sum\_j w\_jx\_j,\]

来做出预测。用更技术性的话说，广义线性模型是通过一个联系函数（link function）把加权和 \(z\) 与目标分布的均值联系起来的模型。在线性回归中，联系函数就是一个恒等函数；在逻辑回归中，联系函数是一个非线性函数（即 logistic sigmoid 函数）。logistic sigmoid 函数给出在给定特征 \(\mathbf{x}\) 时目标类（\(y=1\)）的类别隶属概率：

\[P\left(y=1 | \mathbf{x}^{(i)}\right) = \frac{1}{1+ e ^{- z^{(i)} }}.\]

遗憾的是，联系函数使得权重大小的解读比线性回归稍微复杂一些。在线性回归中，把特征 \(x\_j\) 增加 1 会给预测加上 \(w\_j\)（\(y\) 变成 \(y+w\_j\)）；而在逻辑回归中，改变 \(x\_j\) 对预测的影响是乘性的而非加性的。

为了弄清输入特征的变化如何影响预测，我们来考察预测值与几率（odds）之间的关系。一个事件（例如某个特定训练样本被分类为 \(y=1\)）的几率，写作事件发生的概率与事件不发生的概率之比（注意不要把这个比值与所谓的*几率比*（odds ratio）混淆）：

\[\text{Odds}\left(\mathbf{x}^{(i)}\right) = \frac{P\left(y=1 | \mathbf{x}^{(i)}\right) }{1 - P\left(y=1| \mathbf{x}^{(i)}\right)}.\]

几率与特征加权和的关系如下：
\(\text{Odds}\left(\mathbf{x}^{(i)}\right) = \frac{P\left(y=1 | \mathbf{x}^{(i)}\right) }{1 - P\left(y=1| \mathbf{x}^{(i)}\right)} = e^{z^{(i)}},\)

由于

\[\begin{align}\frac{P\left(y=1 | \mathbf{x}^{(i)}\right) }{1 - P\left(y=1| \mathbf{x}^{(i)}\right)} &= \frac{\frac{1}{1+e^{-z}}}{1-\frac{1}{1+e^{-z}}}\\
&= \frac{\frac{e^z}{1+e^z}}{1-\frac{e^z}{1+e^z}}\\
&= \frac{e^z}{1+e^z - e^z}\\
&=e^z
.
\end{align}\]

现在，把某个特征 \(x\_j\) 改变 1，会得到如下几率比：

\[\frac{\text{Odds}\left(x\_j^{(i)} + 1\right)}{\text{Odds}\left(x\_j^{(i)}\right)} = e^{w\_j}.\]

这是因为

\[e^z = e^{b + w\_1x\_1 + w\_2 x\_2 + ... + w\_m x\_m} = e^{w\_1x\_1} \cdot e^{b+ w\_2 x\_2 + ... + w\_m x\_m},\]

于是当 \(x\_{j+1} = x\_j + 1\) 时，有 \(x\_{j+1} w\_j = x\_jw\_j + w\_j\)，从而得到

\[\frac{\text{Odds}\left(x\_j^{(i)} + 1\right)}{\text{Odds}\left(x\_j^{(i)}\right)} = \frac{e^{w\_j + (b + w\_1x\_1 + w\_2 x\_2 + ... + w\_m x\_m)}}{e^{b + w\_1x\_1 + w\_2 x\_2 + ... + w\_m x\_m}}= e^{w\_j}.\]

总结一下：把特征 \(x\_j\) 增加 1，会使几率放大 \(e^{w\_j}\) 倍。

#### 数值示例

为了说明增加特征值对逻辑回归几率的乘性影响，我们来看一个数值例子。假设对某个特定样本 \(x^{(i)}\)，我们从几率 2 出发：

\[\text{Odds}\left(\mathbf{x}^{(i)}\right) = \frac{P\left(y=1 | \mathbf{x}^{(i)}\right) }{1 - P\left(y=1| \mathbf{x}^{(i)}\right)} = 2.\]

现在我们把第 \(j\) 个特征增加 1，也就是说，加权和增加了 \(w\_j\)。假设 \(w\_j=1.1\)，那么几率比为

\[\frac{\text{Odds}\left(x\_j^{(i)} + 1\right)}{\text{Odds}\left(x\_j^{(i)}\right)} = e^{w\_j} = e^{1.1} = 3.\]

这将使支持类别归属 \(y=1\) 的几率增大 3 倍（从 \(2\) 增至 \(2 \cdot 3=6\)）。换言之，支持事件 \(y=1\) 的几率变为原来的 3 倍。

我们也可以从预测类别隶属概率的角度来看这个变化：

\[P\left(y=1 | \mathbf{x}^{(i)}\right).\]

在逻辑回归中，预测类别隶属概率与几率的关系如下：

\[P\left(y=1 | \mathbf{x}^{(i)}\right) = \frac{1}{1 + e^{-z^{(i)}}} = \frac{e^{z^{(i)}}}{1 + e^{z^{(i)}}} = \frac{e^{\log\left(\text{Odds}\left(\mathbf{x}^{(i)}\right)\right)}}{1 + e^{\log(\text{Odds}\left(\left(\mathbf{x}^{(i)}\right)\right)}} = \frac{\text{Odds}\left(\mathbf{x}^{(i)}\right)}{1+\text{Odds}\left(\mathbf{x}^{(i)}\right)}.\]

从 \(\text{Odds}\left(\mathbf{x}^{(i)}\right)=2\) 出发，\(\mathbf{x}^{(i)}\) 被分类为 \(y=1\) 的概率是 \(2/(1+2) = 0.6667\)。

现在，把 \(x\_j\) 改变 1 个单位，也就是把几率比乘以 \(e^{w\_j}\)（设 \(w\_j=1.1\)），几率就从 2 更新为 \(2\cdot 3=6\)。因此，把几率代入上面的等式，预测类别隶属概率

\[P\left(y=1|\mathbf{x}^{(i)}\right),\]

从 \(2/3 = 0.6667\) 增加到 \(6/(1+6)=0.857\)。

我们也可以从加权输入 \(z = b + \sum\_j w\_j x\_j\) 的角度来观察特征增加的影响。例如，假设加权输入 \(z = \log(2)=0.693\)，那么

\[\frac{1}{1 + e^{-\log(2)}}=2/3=0.6667.\]

而把输入增加 1.1，得到
\(\frac{1}{1 + e^{- (\log(2)+1.1)}} = 0.857.\)

总结：把特征 \(x\_j\) 增加 1 会把几率比乘以 \(e^{w\_j}\)，也就是说，预测类别隶属概率会从

\[\frac{\text{Odds}\left(\mathbf{x}^{(i)}\right)}{1+\text{Odds}\left(\mathbf{x}^{(i)}\right)}\]

变为

\[\frac{\text{Odds}\left(\mathbf{x}^{(i)}\right) \cdot e^{w\_j}}{1+\text{Odds}\left(\mathbf{x}^{(i)}\right) \cdot e^{w\_j}}.\]

#### 逻辑回归权重的置信区间

在用上面那些详细的例子说明了与逻辑回归权重相关的特征值变化如何影响预测之后，我们简要过一遍为模型权重附加置信区间的一般流程。由于本文已经很长，我会尽量简短，更详尽的解释可以在大多数统计学教科书中找到。

简而言之，假设模型权重渐近正态，我们可以从参数协方差（或方差-协方差矩阵）计算标准误——标准误就是协方差矩阵对角线元素的平方根。然后，我们可以像前面的线性回归例子那样，用这些标准误构造置信区间。

协方差矩阵可以写作

\[\Sigma = \mathbf{(X}^{T}\mathbf{V}\mathbf{X)}^{-1},\]

其中 \(\mathbf{X}\) 是设计矩阵（\(m\) 是特征数，\(n\) 是训练样本数）：

\[\mathbf{X = }\begin{bmatrix} 1 & x^{(1)}\_{1} & \ldots & x^{(1)}\_{p} \\ 1 & x^{(2)}\_{1} & \ldots & x^{(2)}\_{m} \\ \vdots & \vdots & \ddots & \vdots \\ 1 & x^{(n)}\_{1} & \ldots & x^{(n)}\_{m} \end{bmatrix};\]

全为 1 的那一列是为模型的偏置单元而加的。\(\mathbf{V}\) 是一个对角矩阵，其对角线元素为各个预测类别隶属概率的方差，

\[p^{(i)} = P\left(y=1|\mathbf{x}^{(i)}\right):\]
\[\mathbf{V = } \begin{bmatrix} \hat{p}^{(1)}(1 - \hat{p}^{(1)}) & 0 & \ldots & 0 \\ 0 & \hat{p}^{(2)}(1 - \hat{(p}^{(2)}) & \ldots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \ldots & \hat{p}^{(n)}(1 - \hat{p}^{(n)}) \end{bmatrix}.\]

标准误（SE）就是 \(\Sigma\) 对角线元素的平方根，置信区间可以按照前面讲过的线性回归的相同方式计算：

\[\text{CI}\_{1-\alpha}^{w\_j} = \big[w\_j - t\_{\alpha / 2, n-2} \times SE(w\_j), w\_j + t\_{\alpha / 2, n-2} \times SE(w\_j) \big].\]

#### 代码示例

为了让逻辑回归背后的这些概念更加具体，我们来看 Python 代码示例。为了把注意力放在方法而非数据集上，我们将使用 Iris 数据集的一个简化版本：50 朵变色鸢尾（Versicolor）和 50 朵弗吉尼亚鸢尾（Virginia）。我们考虑的特征是花萼长度、花萼宽度和花瓣宽度。

按照惯例，加载数据集后我们先做一个简单的视觉检查，使用散点图矩阵：

```python
import matplotlib.pyplot as plt

from mlxtend.plotting import scatterplotmatrix
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
from scipy import stats
import numpy as np

# Load and standardize dataset
iris = load_iris()

X_train, y_train = iris.data[50:150, :3], iris.target[50:150]
y_train = np.array(50*[0] + 50*[1])

sc_features = StandardScaler()
sc_target = StandardScaler()

X_std = sc_features.fit_transform(X_train)

# Plot dataset
fig, axes = scatterplotmatrix(X_std[y_train==0], figsize=(6, 5), alpha=0.5)
fig, axes = scatterplotmatrix(X_std[y_train==1], fig_axes=(fig, axes), alpha=0.5,
                              names=['Sepal Length (std.)','Sepal Width (std.)', 'Petal Length (std.)'])

plt.tight_layout()
plt.show()
```

![Interpretable ml 1 iris scatterplot](https://sebastianraschka.com/images/blog/2020/interpretable-ml-1/iris-scatterplot.webp)

接下来，我们在标准化后的 Iris 特征上拟合一个 scikit-learn 的逻辑回归模型，并绘制模型权重：

```python
lor = LogisticRegression(random_state=0, solver='newton-cg', C=1e8)

# set C=1e8 to negate regularization to allow comparison with
# statsmodel coefficients later

lor.fit(X_std, y_train)

fig, ax = plt.subplots()
ax.bar([0, 1, 2], lor.coef_.flatten())

ax.set_xticks([0, 1, 2])
ax.set_xticklabels([f'Sepal Length\n({lor.coef_.flatten()[0]:.3f})',
                    f'Sepal Width\n({lor.coef_.flatten()[1]:.3f})',
                    f'Petal Length\n({lor.coef_.flatten()[2]:.3f})'])
plt.ylabel('Magnitude')
plt.show()
```

![Interpretable ml 1 logreg weights](https://sebastianraschka.com/images/blog/2020/interpretable-ml-1/logreg-weights.webp)

从上面的条形图可以看出，花瓣长度（petal length）似乎是区分变色鸢尾和弗吉尼亚鸢尾的主导特征。这与我们在散点图矩阵中的观察一致：看右下角的花瓣长度直方图，可以直观地看出一个线性分类器能够较好地分开两个物种。花萼宽度则似乎是线性分类器中最没用的特征，这一点在散点图矩阵和逻辑回归模型权重的大小上都有体现。

标准误可以从协方差矩阵计算得到，如上一节所述。模型权重的置信区间随后可以用与线性回归相同的方法计算（下面的 `weight_interval` 代码实际上与前文的 `weight_interval` 代码完全相同，放在这里只是为了便于参考）：

```python
def std_err_logisticregression(y_true, y_pred_proba, X):
    # based on code from 
    # https://stats.stackexchange.com/questions/89484/how-to-compute-the-standard-errors of a logistic regressions coefficients

    # Design matrix -- add column of 1's at the beginning of your X_train matrix
    X_design = np.hstack([np.ones((X.shape[0], 1)), X])
    
    # Initiate matrix of 0's, fill diagonal with each predicted observation's variance
    V = np.diagflat(np.product(y_pred_proba, axis=1))

    # Covariance matrix
    cov = np.linalg.inv(X_design.T @ V @ X_design)

    # Standard errors:
    std_errs = np.sqrt(np.diag(cov))
    
    return std_errs

def weight_intervals(n, weight, std_err, alpha=0.05):
    t_value = stats.t.ppf(1 - alpha/2, df=n - 2)
    temp = t_value * std_err
    lower = weight - temp
    upper = weight + temp

    return lower, upper
```

```python
y_pred_proba = lor.predict_proba(X_std)
std_err = std_err_logisticregression(y_train, y_pred_proba, X_std)

lower, upper = weight_intervals(len(y_train), lor.coef_.flatten(), std_err[1:])
```

计算出置信区间的上下界之后（这里我们使用 95% 置信区间），我们可以在误差条图中将其可视化：

```python
fig, ax = plt.subplots()

ax.hlines(0, xmin=-0.1, xmax=2.2, linestyle='dashed', color='skyblue')
ax.errorbar([0, 1, 2], lor.coef_.flatten(), yerr=upper - lor.coef_.flatten(), fmt='.k')

ax.set_xticks([0, 1, 2])
ax.set_xticklabels([f'Sepal Length\n({lor.coef_.flatten()[0]:.3f})',
                    f'Sepal Width\n({lor.coef_.flatten()[1]:.3f})',
                    f'Petal Length\n({lor.coef_.flatten()[2]:.3f})'])
plt.ylabel('Magnitude');
```

![Interpretable ml 1 log errbar1](https://sebastianraschka.com/images/blog/2020/interpretable-ml-1/log-errbar1.webp)

从上图可以看出，花萼长度和花瓣长度两个特征都具有统计显著性。

除了像上面那样手动计算置信区间，我们也可以使用 Statsmodels，它已经内置了这一功能：

```python
import statsmodels.api as sm

model = sm.Logit(y_train, X_std)
res = model.fit(method='ncg')
lower, upper = res.conf_int(0.05)[:, 0], res.conf_int(0.05)[:, 1]

fig, ax = plt.subplots()

ax.hlines(0, xmin=-0.1, xmax=2.2, linestyle='dashed', color='skyblue')
ax.errorbar([0, 1, 2], res.params, yerr=upper - res.params, fmt='.k')

ax.set_xticks([0, 1, 2])
ax.set_xticklabels([f'Sepal Length\n({res.params[0]:.3f})',
                    f'Sepal Width\n({res.params[1]:.3f})',
                    f'Petal Length\n({res.params[2]:.3f})'])
plt.ylabel('Magnitude');
```

![Interpretable ml 1 log errbar1 sm](https://sebastianraschka.com/images/blog/2020/interpretable-ml-1/log-errbar1-sm.webp)

## 结语

广义线性模型还有许多方面没有在本文中涉及。不过，鉴于线性回归和逻辑回归是应用数据科学和机器学习中常用的"工具"，我希望这段关于模型权重解读的简要介绍对你有所帮助。作为后续阅读，我推荐阅读《Interpretable Machine Learning》一书中关于广义线性模型和广义可加模型的章节：<https://christophm.github.io/interpretable-ml-book/extend-lm.html>。

未来的博文可能会探讨基于树的模型作为可解释机器学习模型的话题。

PS：本文代码示例对应的 Jupyter Notebook 已发布在 GitHub 上：<https://github.com/rasbt/interpretable-ml-article>。
