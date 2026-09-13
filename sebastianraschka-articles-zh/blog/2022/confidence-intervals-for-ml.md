---
title: "机器学习分类器的置信区间"
title_en: "ML Classifier Confidence Intervals"
source: https://sebastianraschka.com/blog/2022/confidence-intervals-for-ml.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 机器学习分类器的置信区间

> 原文：[ML Classifier Confidence Intervals](https://sebastianraschka.com/blog/2022/confidence-intervals-for-ml.html)

开发好的预测模型离不开准确的性能评估与比较。然而，在评估机器学习模型时，我们通常要应对许多限制，包括数据有限、独立性被违背以及采样偏差。置信区间并不是银弹，但至少可以为我们提供一扇额外的窗口，来审视模型所报告的准确率和性能的不确定性。

正如 [Steinbach 等人最近](https://arxiv.org/abs/2204.05173)所指出的，

> confidence intervals around accuracy measurements can greatly enhance the communication of research results as well as impact the reviewing process.

以我作为审稿人的经验来看，我见过许多通过加入不确定性估计来采纳这一最低标准的研究论文。不过，仍有许多文章完全省略任何形式的不确定性估计；展望未来，我希望这种做法能更加普及，因为加上它通常只是举手之劳。

![Confidence intervals for ml adding cis](https://sebastianraschka.com/images/blog/2022/confidence-intervals-for-ml/adding-cis.webp)

本文概述了为机器学习模型构造置信区间的几种不同方法。注意，这些方法同样适用于深度学习。本文有意写得比较短，聚焦于技术操作本身，不纠缠于细节；文中随处可见指向相关概念解释的链接。

最后值得强调的是，大方向是测量并报告不确定性。置信区间只是其中一种方式。此外，报告不同数据集划分或随机种子上的平均性能，同时附上方差或标准差，也很有帮助——[我有时会采用这种更简单的做法](https://arxiv.org/abs/1901.07884)，因为它更容易解释。不过既然本文的主题是置信区间，我们就先定义什么是置信区间，以及如何构造它们。

## 置信区间速览

简而言之，置信区间到底是什么？置信区间是一种在估计值周围计算上界和下界的方法。真实的参数值要么落在这些界之内，要么落在外面。

设想我们有一个统计量，比如从未知总体中抽取的样本计算出的样本均值。我们的目标是用这个统计量估计总体参数；例如，可以用样本均值来估计总体均值。然而在大多数时候，估计值与真实值并不完全相同。这时，我们就可以用置信区间来量化这一估计的不确定性。

实践中通常约定使用 95% 置信区间，但该怎么理解它呢？首先，假设我们能够接触到总体（当然，现实中从来不是这样；否则我们就不必估计参数，而是可以精确计算出它了）。然后，如果我们从这个分布中抽取非常多的样本，并对这些样本应用我们的置信区间方法，那么 95% 的置信区间会包含真实值。

![Confidence intervals for ml ci viz](https://sebastianraschka.com/images/blog/2022/confidence-intervals-for-ml/ci-viz.webp)

在机器学习语境中，我们通常关心的是模型的性能。因此，这里想要估计的总体参数可以是模型的泛化准确率，而测试集准确率就是我们估计的泛化准确率。最后，95% 置信区间给出了这个估计有多准确的不确定性度量。

### 关于统计显著性的说明

顺便一提：如果两个测量的置信区间*不*重叠，我们可以说两者的差异具有统计显著性；但如果置信区间重叠，我们却*不能*说结果*不*具有统计显著性。（《Points of Significance》系列中的 [Error bars](https://www.nature.com/articles/nmeth.2659) 一文很好地说明了这一点。）如果想检验差异是否不具有统计显著性，就必须考察待比较差异的分布，并检查其置信区间是否包含 0。

![Confidence intervals for ml ci overlap](https://sebastianraschka.com/images/blog/2022/confidence-intervals-for-ml/ci-overlap.webp)

## 为动手示例定义数据集与模型

接下来的小节将展示为机器学习分类器性能构造置信区间的一些常见方法。

为了简单起见，我们将使用 [Iris 数据集](https://archive.ics.uci.edu/ml/datasets/iris)和[决策树分类器](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html)。不过，这些方法可以推广到其他数据集和分类器，包括深度神经网络。

（包含代码示例的 Jupyter notebook 可以在[这里](https://github.com/rasbt/machine-learning-notes/tree/main/evaluation/ci-for-ml/confidence-intervals-for-ml.ipynb)找到。）

**输入：**

```python
from mlxtend.data import iris_data
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = iris_data()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.15, random_state=123, stratify=y
)

clf = DecisionTreeClassifier(random_state=123)
```

## 方法 1：基于测试集的正态近似区间

正态近似区间也许是构造置信区间最简单、最经典的方法。使用这种方法，我们从单一的「训练-测试」划分来计算置信区间。这在训练成本高昂的深度学习中特别有吸引力。当我们关注的是一个特定模型时（区别于像 k 折交叉验证中那样在不同训练折上拟合的模型），它同样有吸引力（通常也是在深度学习语境下）。

简而言之，在假设正态分布的前提下，为估计参数（比如样本均值 \(\bar{x}\)）计算置信区间的公式如下：
\(\bar{x} \pm z \times \text{SE},\)

其中

- \(z\) 是 \(z\) 值（某个值距离标准正态分布均值有多少个标准差）；
- \(\text{SE}\) 是被估计参数（这里是样本均值）的标准误（standard error）。

在我们的场景中，样本均值 \(\bar{x}\) 就是测试集准确率 \(\text{ACC}\_{\text{test}}\)，即一个成功比例（在[二项比例置信区间](https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval)的语境下）。

在正态近似下，标准误可计算为

\[\text{SE} = \sqrt{ \frac{1}{n} \text{ACC}\_{\text{test}}\left(1- \text{ACC}\_{\text{test}}\right)},\]

其中 \(n\) 是测试集大小。于是，把 SE 代回上面的公式，我们得到

\[\text{ACC}\_{\text{test}} \pm z \sqrt{\frac{1}{n} \text{ACC}\_{\text{test}}\left(1- \text{ACC}\_{\text{test}}\right)}.\]

（这一方法的描述可以在我的《[Model Evaluation, Model Selection, and Algorithm Selection in Machine Learning](https://arxiv.org/abs/1811.12808)》第 *1.7* 节「Confidence Intervals via Normal Approximation（通过正态近似构造置信区间）」中找到。）

现在，我们来看看如何在 Python 中实现它。先计算 z 值，可以通过 `scipy.stats.norm.ppf` 获得（而不必去翻旧统计学教科书里的 \(z\) 表）。

**输入：**

```python
import scipy.stats

confidence = 0.95  # Change to your desired confidence level
z_value = scipy.stats.norm.ppf((1 + confidence) / 2.0)
print(z_value)
```

**输出：**

```python
1.959963984540054
```

接下来，让我们计算分类器的测试准确率，并把数值代入上面的公式；对应的 Python 代码如下：

**输入：**

```python
import numpy as np

clf.fit(X_train, y_train)

acc_test = clf.score(X_test, y_test)
ci_length = z_value * np.sqrt((acc_test * (1 - acc_test)) / y_test.shape[0])

ci_lower = acc_test - ci_length
ci_upper = acc_test + ci_length

print(ci_lower, ci_upper)
```

**输出：**

```python
0.873179017733963 1.0398644605269067
```

所以上面的值就是测试集准确率周围的 95% 置信区间。让我们用下面的代码将置信区间可视化：

**输入：**

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 3))

ax.errorbar(acc_test, 0, xerr=ci_length, fmt="o")

ax.set_xlim([0.8, 1.0])

ax.set_yticks(np.arange(1))
ax.set_yticklabels(["Normal approximation interval"])
ax.set_xlabel("Prediction accuracy")

plt.tight_layout()
plt.grid(axis="x")
plt.show()
```

**输出：**

![Confidence intervals for ml normal approx](https://sebastianraschka.com/images/blog/2022/confidence-intervals-for-ml/normal-approx.webp)

我们把置信区间上界截断在 1.0（即 100% 准确率处），因为报告超过 100% 的准确率是没有意义的。

最后，让我们把置信区间存入一个 Python 字典，以便稍后与其他置信区间比较时取用：

**输入：**

```python
results = {
    "Method 1: Normal approximation": {
        "Test accuracy": acc_test,
        "Lower 95% CI": ci_lower,
        "Upper 95% CI": ci_upper,
    }
}
```

## 方法 2：对训练集做自助法——准备工作

置信区间用于估计未知参数。如果我们只有一个估计值，比如来自单一测试集的准确率，就需要对这个准确率值的分布做出假设。例如，我们可以假设（从不同样本计算出的）准确率值服从正态分布。

在理想世界中，我们能够接触到测试集样本的分布。如果是那样，我们就可以看看 95% 的准确率值落在哪个范围内。这固然理想，但并不现实，因为我们没有无穷多个测试集。
这时，一种变通方法是自助法（bootstrapping），它可以估计抽样分布，做法是从单个随机样本中*有放回地*抽取多个样本。公式如下：
\(\text{ACC}\_{\text{bootavg}}=\frac{1}{b} \sum\_{j=1}^{b} \text{ACC}\_{\text{boot}, j},\)

其中 \(b\) 是自助重采样的轮数，\(\text{ACC}\_{\text{boot}, j}\) 是第 \(j\) 轮计算出的模型准确率。注意，通常建议自助重采样至少进行 200 轮（参见《[Introduction to the Bootstrap](https://scholar.google.com/scholar_lookup?title=An%20introduction%20to%20the%20bootstrap&author=&publication_year=1993)》一书）。

我们用来评估机器学习模型的方法通常称为袋外自助（out-of-bag bootstrap）：我们在训练折上训练模型，并在每轮留出的数据点上评估它。更多细节请参见《[Model Evaluation, Model Selection, and Algorithm Selection in Machine Learning](https://arxiv.org/abs/1811.12808)》第 2 节「Bootstrapping and Uncertainties（自助法与不确定性）」。不过，自助法有多种变体。下面我们创建多个自助样本，供后续小节复用。

**输入：**

```python
import numpy as np

rng = np.random.RandomState(seed=12345)
idx = np.arange(y_train.shape[0])

bootstrap_train_accuracies = []
bootstrap_rounds = 200

for i in range(bootstrap_rounds):

    train_idx = rng.choice(idx, size=idx.shape[0], replace=True)
    valid_idx = np.setdiff1d(idx, train_idx, assume_unique=False)

    boot_train_X, boot_train_y = X_train[train_idx], y_train[train_idx]
    boot_valid_X, boot_valid_y = X_train[valid_idx], y_train[valid_idx]

    clf.fit(boot_train_X, boot_train_y)
    acc = clf.score(boot_valid_X, boot_valid_y)
    bootstrap_train_accuracies.append(acc)

bootstrap_train_mean = np.mean(bootstrap_train_accuracies)
```

我们可以通过下面的代码，用直方图将自助采样得到的准确率（\(\text{ACC}\_{\text{boot}, j}\)）及其样本均值（\(\text{ACC}\_{\text{bootavg}}\)）可视化：

**输入：**

```python
fig, ax = plt.subplots(figsize=(8, 4))

ax.vlines(bootstrap_train_mean, [0], 80, lw=2.5, linestyle="-", label="Mean")

ax.hist(
    bootstrap_train_accuracies, bins=7, color="#0080ff", edgecolor="none", alpha=0.3
)

plt.xlabel('Accuracy')
plt.ylabel('Count')
plt.xlim([0.8, 1.1])

plt.legend(loc="upper left")
plt.grid()
plt.show()
```

![Confidence intervals for ml bootstrap hist](https://sebastianraschka.com/images/blog/2022/confidence-intervals-for-ml/bootstrap-hist.webp)

### 关于用自助法替代独立测试集的说明

在上一节中，我们通过自助法从训练集构造了验证（或测试）集。不过，假设我们不在训练集上调优模型，那么就可以使用整个数据集，并报告平均自助准确率 \(\text{ACC}\_{\text{bootavg}}\) 作为模型性能估计，而不必使用独立测试集。这对小数据集尤其有吸引力。此外，正如 Bouthillier 等人在其《[Accounting for variance in machine learning benchmarks](https://arxiv.org/abs/2103.03098)》研究中发现的，使用袋外自助流程可以提高性能估计的可靠性。

### 方法 2.1：从自助样本构造 *t* 置信区间

介绍了袋外自助流程之后，现在进入有趣的部分：从自助样本计算置信区间。假设样本均值服从正态分布，我们可以像前面一样计算置信区间，公式如下：

\[\text{ACC}\_{\text{test}} \pm z \times \text{SE}.\]

一般来说，当我们处理有限样本量、并希望用样本标准差估计总体标准差时（标准差用于计算标准误），常见的做法是用 \(t\) 值替换 \(z\) 值：

\[\text{ACC}\_{\text{test}} \pm t \times \text{SE}.\]

不过，使用 \(z\) 分数也完全没有问题，因为当样本量大于 100 时，\(z\) 分数与 \(t\) 分数实际上几乎相同（这里我们假设至少有 200 个自助样本）。

然后我们可以把标准误（SE）计算为该分布的标准差：

\[\text{SE}=\sqrt{\frac{1}{b-1} \sum\_{j=1}^{b}\left(\text{ACC}\_{\text{boot},j}-{\text{ACC}\_\text{bootavg}}\right)^{2}}.\]

注意，我们通常会把标准差（SD）除以 \(\sqrt{n}\) 来得到标准误（SE），其中 \(n = b\)：

\[\text{SE} = \frac{\text{SD}}{\sqrt{n}}.\]

不过在这里没有必要这样做，因为自助分布是均值的分布（而不是单个数据点的分布），而 \(\text{ACC}\_{\text{bootavg}}\) 是这些均值的均值。

（作为可选练习，你可以尝试修改下面的代码，加入除以 \(\sqrt{n}\) 的操作（其中 \(\sqrt{n} = \sqrt{b}\)），你可能会发现这会把置信区间收缩到不现实的程度，也不再与稍后要介绍的百分位法的结果相符。）

做完这些准备之后，进入编码部分。同样，我们不必翻旧统计学教科书里的 \(t\) 表，而是用 SciPy 来获得 95% 置信区间、自由度为 \(b-1\) 的 \(t\) 值：

**输入：**

```python
confidence = 0.95  # Change to your desired confidence level
t_value = scipy.stats.t.ppf((1 + confidence) / 2.0, df=bootstrap_rounds - 1)
print(t_value)
```

**输出：**

```python
1.971956544249395
```

接下来，让我们计算 95% 置信区间：

**输入：**

```python
se = 0.0
for acc in bootstrap_train_accuracies:
    se += (acc - bootstrap_train_mean) ** 2
se = np.sqrt((1.0 / (bootstrap_rounds - 1)) * se)

ci_length = t_value * se

ci_lower = bootstrap_train_mean - ci_length
ci_upper = bootstrap_train_mean + ci_length

print(ci_lower, ci_upper)
```

**输出：**

```python
0.879470830164037 1.0132047668825668
```

为了让结果更直观，我们把置信区间加到直方图上：


**输入：**

```python
fig, ax = plt.subplots(figsize=(8, 4))
ax.vlines(bootstrap_train_mean, [0], 80, lw=2.5, linestyle="-", label="Mean")

ax.vlines(ci_lower, [0], 15, lw=2.5, linestyle="dotted", label="95% CI", color="C2")
ax.vlines(ci_upper, [0], 15, lw=2.5, linestyle="dotted", color="C2")

ax.hist(
    bootstrap_train_accuracies, bins=7, color="#0080ff", edgecolor="none", alpha=0.3
)

plt.xlabel('Accuracy')
plt.ylabel('Count')
plt.xlim([0.8, 1.1])

plt.legend(loc="upper left")

plt.grid()
plt.show()
```

**输出：**

![Confidence intervals for ml bootstrap hist oob t](https://sebastianraschka.com/images/blog/2022/confidence-intervals-for-ml/bootstrap-hist-oob-t.webp)

你可能会好奇它与前面构造的正态近似区间（方法 1）相比如何？别担心，我们会在后面的章节讨论。

同样，我们把 CI 值加入 Python 字典，以便稍后做比较研究。

**输入：**

```python
results["Method 2.1: Bootstrap, 1-sample CI"] = {
    "Test accuracy": bootstrap_train_mean,
    "Lower 95% CI": ci_lower,
    "Upper 95% CI": ci_upper,
}
```

### 方法 2.2：使用百分位法的自助置信区间

如果自助得到的准确率服从正态分布，上一节概述的方法看起来相当直接。然而，利用自助样本的一种更稳健、更通用的方法是百分位法（percentile method）（更多细节参见我的《[Model Evaluation, Model Selection, and Algorithm Selection in Machine Learning](https://arxiv.org/abs/1811.12808)》一文第 2 节「Bootstrapping and Uncertainties（自助法与不确定性）」）。

在这里，我们按如下方式选取置信下界与上界：

- \(\text{ACC}\_{lower}\) 为 \(\text{ACC}\_\text{boot}\) 分布的第 \(\alpha\_{1}th\) 百分位数；
- \(\text{ACC}\_{upper}\) 为 \(\text{ACC}\_{boot}\) 分布的第 \(\alpha\_{2}th\) 百分位数；

其中 \(\alpha\_1 = \alpha\)、\(\alpha\_2 = 1 - \alpha\)，而 \(\alpha\) 是我们的置信度，用于计算 \(100 \times (1 - 2 \times \alpha)\) 置信区间。例如，要计算 95% 置信区间，我们取 \(\alpha = 0.025\)，得到 *b* 个自助样本分布的第 2.5 和第 97.5 百分位数，作为置信下界与上界。

使用 NumPy 计算百分位数非常直接：

**输入：**

```python
ci_lower = np.percentile(bootstrap_train_accuracies, 2.5)
ci_upper = np.percentile(bootstrap_train_accuracies, 97.5)

print(ci_lower, ci_upper)
```

**输出：**

```python
0.8695652173913043 1.0
```

照例，让我们在直方图中将置信区间可视化，并更新 `results` 字典：

**输入：**

```python
fig, ax = plt.subplots(figsize=(8, 4))
ax.vlines(bootstrap_train_mean, [0], 80, lw=2.5, linestyle="-", label="Mean")

ax.vlines(ci_lower, [0], 15, lw=2.5, linestyle="dotted", label="95% CI", color="C2")
ax.vlines(ci_upper, [0], 15, lw=2.5, linestyle="dotted", color="C2")

ax.hist(
    bootstrap_train_accuracies, bins=7, color="#0080ff", edgecolor="none", alpha=0.3
)
plt.legend(loc="upper left")

plt.xlabel('Accuracy')
plt.ylabel('Count')
plt.xlim([0.8, 1.1])

plt.grid()
plt.show()
```

**输出：**

![In:](https://sebastianraschka.com/images/blog/2022/confidence-intervals-for-ml/bootstrap-hist-oob-percentile.webp)

**输入：**

```python
results["Method 2.2: Bootstrap, percentile"] = {
    "Test accuracy": bootstrap_train_mean,
    "Lower 95% CI": ci_lower,
    "Upper 95% CI": ci_upper,
}
```

### 方法 2.3：通过 .632 自助法对自助样本重新加权

本节我们来看 [.632 自助法](https://scholar.google.com/scholar?hl=en&as_sdt=0%2C50&q=Estimating+the+error+rate+of+a+prediction+rule%3A+improvement+on+cross-validation&btnG=)，它建立在前文介绍的百分位法之上。

略去技术细节，前面介绍的袋外自助方法带有轻微的悲观偏差，也就是说它报告的测试准确率会比模型真实的泛化准确率略差。.632 自助法旨在校正这种悲观偏差。（为了保持本文简洁，更详细的讨论请参见我的《[Model Evaluation, Model Selection, and Algorithm Selection in Machine Learning](https://arxiv.org/abs/1811.12808)》一文第 2 节「Bootstrapping and Uncertainties（自助法与不确定性）」。）

我们跳过公式，直接进入代码实现（实践中，我推荐使用我在 [mlxtend](http://rasbt.github.io/mlxtend/user_guide/evaluate/bootstrap_point632_score/) 中的实现）。简而言之，可以把它看作前面所用自助方法的一个重新加权版本：

**输入：**

```python
rng = np.random.RandomState(seed=12345)
idx = np.arange(y_train.shape[0])

bootstrap_train_accuracies = []
bootstrap_rounds = 200
weight = 0.632

for i in range(bootstrap_rounds):

    train_idx = rng.choice(idx, size=idx.shape[0], replace=True)
    valid_idx = np.setdiff1d(idx, train_idx, assume_unique=False)

    boot_train_X, boot_train_y = X_train[train_idx], y_train[train_idx]
    boot_valid_X, boot_valid_y = X_train[valid_idx], y_train[valid_idx]

    clf.fit(boot_train_X, boot_train_y)
    valid_acc = clf.score(boot_valid_X, boot_valid_y)
    # predict training accuracy on the whole training set
    # as ib the original .632 boostrap paper
    # in Eq (6.12) in
    #    "Estimating the Error Rate of a Prediction Rule: Improvement
    #     on Cross-Validation"
    #     by B. Efron, 1983, https://doi.org/10.2307/2288636
    train_acc = clf.score(X_train, y_train)

    acc = weight * train_acc + (1.0 - weight) * valid_acc

    bootstrap_train_accuracies.append(acc)

bootstrap_train_mean = np.mean(bootstrap_train_accuracies)
bootstrap_train_mean
```

**输出：**

```python
0.9677367193053941
```

**输入：**

```python
ci_lower = np.percentile(bootstrap_train_accuracies, 2.5)
ci_upper = np.percentile(bootstrap_train_accuracies, 97.5)

print(ci_lower, ci_upper)
```

**输出：**

```python
0.9221417322834646 1.0
```

**输入：**

```python
results["Method 2.3: Bootstrap, .632"] = {
    "Test accuracy": bootstrap_train_mean,
    "Lower 95% CI": ci_lower,
    "Upper 95% CI": ci_upper,
}
```

### 方法 2.4：更进一步的重加权：.632+ 自助法

[.632+ 自助法](https://scholar.google.com/scholar_lookup?&title=Improvements%20on%20Cross-Validation%3A%20The%20.632%2B%20Bootstrap%20Method&journal=J%20Am%20Stat%20Assoc&doi=10.1080%2F01621459.1997.10474007&volume=92&issue=438&pages=548-560&publication_year=1997&author=Efron%2CB&author=Tibshirani%2CR)是对上面实现的 .632 自助法的改进。简而言之，主要区别在于权重项不是固定的，而是通过所谓的无信息率（no-information rate）计算得到。

同样，我们跳过公式，直接进入代码实现。实践中，我推荐使用我在 [mlxtend](http://rasbt.github.io/mlxtend/user_guide/evaluate/bootstrap_point632_score/) 中的实现。更详细的讨论请参见我的《[Model Evaluation, Model Selection, and Algorithm Selection in Machine Learning](https://arxiv.org/abs/1811.12808)》一文第 2 节「Bootstrapping and Uncertainties（自助法与不确定性）」。

**输入：**

```python
from itertools import product

from sklearn.metrics import accuracy_score

def no_information_rate(targets, predictions, loss_fn):
    combinations = np.array(list(product(targets, predictions)))
    return loss_fn(combinations[:, 0], combinations[:, 1])

rng = np.random.RandomState(seed=12345)
idx = np.arange(y_train.shape[0])

bootstrap_train_accuracies = []
bootstrap_rounds = 200
weight = 0.632

for i in range(bootstrap_rounds):

    train_idx = rng.choice(idx, size=idx.shape[0], replace=True)
    valid_idx = np.setdiff1d(idx, train_idx, assume_unique=False)

    boot_train_X, boot_train_y = X_train[train_idx], y_train[train_idx]
    boot_valid_X, boot_valid_y = X_train[valid_idx], y_train[valid_idx]

    clf.fit(boot_train_X, boot_train_y)
    train_acc = clf.score(X_train, y_train)
    valid_acc = clf.score(boot_valid_X, boot_valid_y)

    gamma = no_information_rate(y, clf.predict(X), accuracy_score)
    R = (valid_acc - train_acc) / (gamma - train_acc)

    weight = 0.632 / (1 - 0.368 * R)

    acc = weight * train_acc + (1.0 - weight) * valid_acc

    bootstrap_train_accuracies.append(acc)

bootstrap_train_mean = np.mean(bootstrap_train_accuracies)
bootstrap_train_mean
```

**输出：**

```python
0.9683445668115584
```

**输入：**

```python
ci_lower = np.percentile(bootstrap_train_accuracies, 2.5)
ci_upper = np.percentile(bootstrap_train_accuracies, 97.5)

print(ci_lower, ci_upper)
```

**输出：**

```python
0.9248753660725227 1.0
```

**输入：**

```python
results["Method 2.4: Bootstrap, .632+"] = {
    "Test accuracy": bootstrap_train_mean,
    "Lower 95% CI": ci_lower,
    "Upper 95% CI": ci_upper,
}
```

## 方法 3：对测试集预测结果做自助法

前面几节介绍的自助法（2.1 至 2.3）彼此密切相关，因为它们都基于对训练集的重采样。本节来看另一种涉及自助法的置信区间构造方式，即对测试集做自助法。（我第一次见到这种方法被使用是在论文《[Machine Learning for Scent: Learning Generalizable Perceptual Representations of Small Molecules](https://arxiv.org/abs/1910.10685)》中。）

在这里，与我们之前介绍的其他自助法不同，我们保持模型固定，只对测试集（而不是训练集）重采样。这在深度学习场景中特别有吸引力，因为它避免了对模型重新训练。

**输入：**

```python
clf.fit(X_train, y_train)

predictions_test = clf.predict(X_test)
acc_test = np.mean(predictions_test == y_test)

rng = np.random.RandomState(seed=12345)
idx = np.arange(y_test.shape[0])

test_accuracies = []

for i in range(200):

    pred_idx = rng.choice(idx, size=idx.shape[0], replace=True)
    acc_test_boot = np.mean(predictions_test[pred_idx] == y_test[pred_idx])
    test_accuracies.append(acc_test_boot)

bootstrap_train_mean = np.mean(test_accuracies)
bootstrap_train_mean
```

**输出：**

```python
0.9597826086956522
```

通过自助采样得到各次测试准确率之后，我们可以用熟悉的百分位法计算 95% 置信区间：

**输入：**

```python
ci_lower = np.percentile(test_accuracies, 2.5)
ci_upper = np.percentile(test_accuracies, 97.5)

print(ci_lower, ci_upper)
```

**输出：**

```python
0.8260869565217391 1.0
```

**输入：**

```python
results["Method 3: Bootstrap test set"] = {
    "Test accuracy": bootstrap_train_mean,
    "Lower 95% CI": ci_lower,
    "Upper 95% CI": ci_upper,
}
```

同样，我们会在下一节介绍完最后一种计算置信区间的方法之后，再来回顾和讨论这些结果。

## 方法 4：用不同随机种子重新训练模型得到的置信区间

在深度学习中，用不同的随机种子重新训练模型是很常见的。如何从这些实验构造置信区间？假设样本均值服从正态分布，我们可以采用前面围绕样本均值 \(\bar{x}\) 计算置信区间的方法，公式如下：
\(\bar{x} \pm z \times \text{SE}.\)

由于在这种语境下我们通常处理的样本量相对较小（例如 10 个随机种子），\(t\) 分布更为合适。因此，与自助法方法 2.1 类似，我们把上面公式中的 \(z\) 值替换为 \(t\) 值，

另外，如果我们关心平均准确率 \(\overline{ACC}\_{\text{test}}\)，那么从技术上可以论证：对应不同随机种子（\(j\)）的每个 \(\text{ACC}\_{\text{test}, j}\) 都是一个样本，而我们所评估的随机种子数量就是样本量 \(n\)，于是我们计算
\(\overline{ACC}\_{\text{test}} \pm t \times \text{SE},\)

其中

\[\text{SE} = \frac{\text{SD}}{\sqrt{n}}.\]

这里，
\(\overline{ACC}\_{\text{test}} = \frac{1}{r} \sum\_{j=1}^{r} {ACC}\_{\text{test}, j},\)
且 \(r\) 是我们所评估的随机种子数量。\(\text{SD}\) 是样本标准差，

\[\text{SD}=\sqrt{\frac{\sum\_j\left({ACC}\_{\text{test}, j}-\overline{ACC}\_{\text{test}}\right)^{2}}{r-1}}.\]

请注意，对决策树分类器来说，随机种子在实践中通常没什么影响，所以下面的实验并不十分有趣。不过，出于完整性考虑我还是附上了代码，这样当你把它应用到深度神经网络时，就能了解它的工作方式：

**输入：**

```python
test_accuracies = []
rounds = 5

for i in range(rounds):

    clf = DecisionTreeClassifier(random_state=i)

    clf.fit(X_train, y_train)
    acc = clf.score(X_test, y_test)
    test_accuracies.append(acc)

test_mean = np.mean(test_accuracies)
test_mean
```

**输出：**

```python
0.9565217391304348
```

**输入：**

```python
confidence = 0.95  # Change to your desired confidence level
t_value = scipy.stats.t.ppf((1 + confidence) / 2.0, df=rounds - 1)

sd = np.std(test_accuracies, ddof=1)
se = sd / np.sqrt(rounds)

ci_length = t_value * se

ci_lower = test_mean - ci_length
ci_upper = test_mean + ci_length

print(ci_lower, ci_upper)
```

**输出：**

```python
0.9565217391304348 0.9565217391304348
```

和猜测的一样，各次测试准确率完全相同。不过，在训练深度神经网络的语境下，这是非常可行且值得推荐的方法。

## 比较不同的置信区间方法

既然有这么多置信区间方法，我们该用哪一个呢？要给出通用建议并不容易，因为这涉及两个方面：实用性和准确性。我们先看实用性。

**实用性**

- 如果想要一种计算开销小、又不像自助法那样需要重新训练模型的置信区间方法，正态近似方法（方法 1）非常合适。
- 与正态近似方法类似，对测试集做自助法（方法 3）也不需要重新训练模型。但它要求我们能够获得模型在测试集上的预测结果。相比之下，正态近似区间仅凭论文中列出的测试集得分（和样本量）就能计算，无需重跑额外的实验。
- 其他自助法（2.1 至 2.4）的开销大得多，因为它们需要在训练折上重新训练模型。由于建议至少进行 200 轮自助重采样，对于更大的数据集和深度神经网络来说，这可能非常昂贵。此外，最后我们得到的并不是一个可供评估的单一模型。当然，我们可以先在训练集上训练一个分类器 \(c\_t\)，然后通过在自助样本上拟合 200 个分类器（\(c\_1\) 到 \(c\_{200}\)）来评估其性能，再把 \(c\_t\) 的性能估计为 \(c\_1\) 到 \(c\_{200}\) 的平均值。这对大多数传统机器学习分类器都行之有效。但对于深度学习模型，我们必须格外小心，因为它们不一定总能收敛。未收敛的模型会产生误导性的准确率估计，而我们会把这些估计一并平均。
- .632+ 自助法（方法 2.4）可能是最准确的自助方法，但对大数据集而言计算开销非常大。在当前实现下，训练样本超过几百个时很可能就不可行了。因此，如果确定要用自助法，次优选择 .632 自助法（方法 2.3）可能是更好的替代。
- 用不同随机种子计算置信区间（方法 4）也是一个很好的选择。但它只在深度学习模型上真正有用。它比正态近似方法（方法 1）和对测试集做自助法（方法 3）更昂贵，因为它需要重新训练模型。另一方面，不同随机种子的结果能让我们很好地了解模型的稳定性。如果你关心统计显著性，还可以用它来做模型比较。此时，可以在假设方差不相等的前提下应用下面的公式：

\[\left(\overline{ACC}\_{\text{m1}} -\overline{ACC}\_{\text{m2}} \right) \pm t \sqrt{\frac{\text{SD}\_{\text{m1}}^{2}}{n\_{\text{m1}}}+\frac{\text{SD}\_{\text{m2}}^{2}}{n\_{\text{m2}}}},\]

其中 \(\text{m1}\) 和 \(\text{m2}\) 分别指模型 1 和模型 2。如果 95% 置信区间不包含 0，那么两个模型的性能差异就在 \(\alpha=0.05\) 水平上具有统计显著性。

因此，从实用性角度出发，我们可以把这些方法从最实用到最不实用排序如下：

1. 正态近似（方法 1）；
2. 对测试集做自助法（方法 3）；
3. 不同随机种子的置信区间（方法 4，仅适用于深度学习）；
4. 用百分位法或 t 区间对训练集做自助法（方法 2.1 和 2.2）；
5. .632 自助法（方法 2.3）；
6. .632+ 自助法（方法 2.4）。

接下来，我们利用本文中不断更新的 `results` 字典，把各种方法放在一起比较：

**输入：**

```python
labels = list(results.keys())

means = np.array([results[k]["Test accuracy"] for k in labels])
lower_error = np.array([results[k]["Lower 95% CI"] for k in labels])
upper_error = np.array([results[k]["Upper 95% CI"] for k in labels])

asymmetric_error = [means - lower_error, upper_error - means]

fig, ax = plt.subplots(figsize=(7, 3))
ax.errorbar(means, np.arange(len(means)), xerr=asymmetric_error, fmt="o")
ax.set_xlim([0.75, 1.0])
ax.set_yticks(np.arange(len(means)))
ax.set_yticklabels(labels)
ax.set_xlabel("Prediction accuracy")
ax.set_title("95% confidence intervals")

plt.grid()
plt.tight_layout()
plt.show()
```

**输出：**

![Confidence intervals for ml comparison](https://sebastianraschka.com/images/blog/2022/confidence-intervals-for-ml/comparison.webp)

可以看到，对测试集做自助法得到的置信区间最宽，而 .632 估计得到的置信区间最窄。如果 .632 置信区间是正确的（95% 的情况下包含真实参数），那么从准确性角度看它们是最理想的。

更窄的 95% 置信区间之所以理想，是因为它缩小了我们所估计的真实参数值的可能范围。然而，这只有在置信区间方法本身准确的前提下才有意义。我们怎么知道哪种方法真正正确或精确呢？用真实数据集很难验证，因为真实数据集的数据量有限——否则的话，我们一开始也就没有必要构造置信区间了。

不过，哪些置信区间方法是正确的、哪些最准确，这个问题很难回答。下一节将介绍一项进一步探究此问题的分析。

## 置信区间与真实模型性能

让我们通过一个小型模拟研究来考察不同置信区间方法的精确程度。这里我们关心的是：置信区间是否真的包含了模型的真实准确率（泛化准确率）。

我们创建一个用于分类的合成数据集，包含 1000 万加 2 千个数据点。前 1000 个数据点用于训练，第二个 1000 个数据点用于测试，剩下的 10,000,000 个数据点构成用于计算模型真实性能的数据集。

（本模拟研究的代码示例所在的 Jupyter notebook 可以在[这里](https://github.com/rasbt/machine-learning-notes/tree/main/evaluation/ci-for-ml/ci-simulation.ipynb)找到。）

![Confidence intervals for ml comparison simulation](https://sebastianraschka.com/images/blog/2022/confidence-intervals-for-ml/comparison-simulation.webp)

图中的红色竖线表示在 1000 万个测试数据点上评估得到的模型真实准确率。我们在这张图中省略了两种方法：方法 4（随机种子不影响决策树模型）和方法 2.4（.632+ 自助法对该数据集而言计算开销过大）。

可以看到，所有 95% 置信区间方法都包含真实参数，这很好。此外，「对测试集做自助法」（方法 3）和「正态近似」（方法 1）给出的平均准确率估计最接近真实准确率，这是一个不错的加分项。

不过，这项模拟研究应当谨慎看待：改变数据集中的标签噪声数量会导致明显不同的结果。另外，理想情况下，我们希望把这一模拟重复多次，看看置信区间是否有 95% 的时候包含真实参数。我本来想把这一点留作读者的练习，但后来还是忍不住跑了[这个实验](https://github.com/rasbt/machine-learning-notes/tree/main/evaluation/ci-for-ml/ci-simulation-repeated.ipynb)。

下面是用不同随机种子生成合成数据集、把上述模拟研究重复 1,000 次后的结果：

|  | 方法 | 95% 置信区间包含真实准确率的次数 |
| --- | --- | --- |
| 1 | 正态近似 | 95.6% |
| 2.1 | 自助法，单样本 CI | 98.5% |
| 2.2 | 自助法，百分位法 | 98.0% |
| 2.3 | 自助法，.632 | 83.2% |
| 3 | 对测试集做自助法 | 94.5% |

正态近似（方法 1）和测试集自助法（方法 3）是最精确的方法，它们的 95% 置信区间中约有 95% 包含真实准确率。相比之下，方法 2.1 和 2.2 显得过于保守（置信区间比必要的更宽），而 .632 自助法似乎会给出不正确的结果，原因可能是置信区间过窄或存在偏差（偏移过多）。

## 结语

正态近似（方法 1）和对测试集做自助法（方法 3）都是实用且准确的选择。具体到深度学习模型，考虑不同随机种子（方法 4）是另一种值得考虑的技术。注意，方法 1 和方法 2 都很方便，因为它们不像方法 4 那样需要训练多个模型。不过，方法 4 对算法比较可能很有吸引力，因为它还能告诉我们一个算法对随机种子的依赖程度。在深度学习中，这一点尤其重要：有时如果碰巧选到了一个不走运的随机种子，某个方法看起来会比实际更差（反之亦然）。

本文主要概述了各种置信区间方法及其优缺点。例如，有些方法通过改变测试集来估计不确定性，有些通过改变随机种子。在计算资源允许的情况下，组合多种方法（例如袋外自助法或测试集自助法，再加上改变学习算法的随机种子）也可能是值得考虑的途径。例如，在前文提到的《[Accounting for variance in machine learning benchmarks](https://arxiv.org/abs/2103.03098)》研究中，研究者发现尽可能多地随机化各种变异来源，有助于降低估计误差。

此外，正如文章开头提到的，置信区间只是传达不确定性的一种方式。机器学习[基准测试](https://sebastianraschka.com/glossary/#benchmark "Benchmark")研究不一定非要附上置信区间。一些更直白的统计量，比如多次重复实验的方差或标准差，就已经能对读者和审稿人有所帮助。

## 附加内容：用 TorchMetrics 构造置信区间

在深度学习和 PyTorch 的语境下，[我最近写过一篇关于 TorchMetrics 的文章](https://sebastianraschka.com/blog/2022/torchmetrics.html)，它是一个不错的工具，适用于数据集大到无法全部载入内存的模型评估场景。虽然前面给出的对测试集做自助法（方法 3）的代码相对简单，但你可能想用 TorchMetrics 来完成这项工作。

作为对照，我们前面用到的对测试集做自助法的代码如下：

**输入：**

```python
clf.fit(X_train, y_train)

predictions_test = clf.predict(X_test)
acc_test = np.mean(predictions_test == y_test)

rng = np.random.RandomState(seed=123)
idx = np.arange(y_test.shape[0])

test_accuracies = []

for i in range(200):

    pred_idx = rng.choice(idx, size=idx.shape[0], replace=True)
    acc_test_boot = np.mean(predictions_test[pred_idx] == y_test[pred_idx])
    test_accuracies.append(acc_test_boot)

bootstrap_train_mean = np.mean(test_accuracies)
bootstrap_train_mean
```

**输出：**

```python
0.956304347826087
```

**输入：**

```python
ci_lower = np.percentile(test_accuracies, 2.5)
ci_upper = np.percentile(test_accuracies, 97.5)

print(ci_lower, ci_upper)
```

**输出：**

```python
0.8695652173913043 1.0
```

使用 [TorchMetrics](https://torchmetrics.rtfd.io/en/latest/) 中的 [`Bootstrapper`](https://lightning.ai/docs/torchmetrics/stable/wrappers/bootstrapper.html)，我们可以复现上面的结果，如下所示：

**输入：**

```python
import torch
from torchmetrics import Accuracy, BootStrapper

torch.manual_seed(123)

quantiles = torch.tensor([0.05, 0.95])
base_metric = Accuracy()
bootstrap = BootStrapper(
    base_metric, num_bootstraps=200, sampling_strategy="multinomial", quantile=quantiles
)

bootstrap.update(torch.from_numpy(predictions_test), torch.from_numpy(y_test))
output = bootstrap.compute()

print(output)
```

**输出：**

```python
{'mean': tensor(0.9602), 'std': tensor(0.0408), 'quantile': tensor([0.8696, 1.0000])}
```

注意，如果我们想以增量方式计算（例如测试集大到内存放不下），这一功能在实践中会非常方便。假设预测结果分多个批次到来：

**输入：**

```python
idx = np.arange(predictions_test.shape[0])
groups = np.array_split(idx, 3)
```

**输入：**

```python
torch.manual_seed(123)

quantiles = torch.tensor([0.05, 0.95])
base_metric = Accuracy()
bootstrap = BootStrapper(
    base_metric, num_bootstraps=200, sampling_strategy="multinomial", quantile=quantiles
)

for group in groups:

    pred_chunk = torch.from_numpy(predictions_test[group])
    label_chunk = torch.from_numpy(y_test[group])

    bootstrap.update(pred_chunk, label_chunk)

output = bootstrap.compute()
print(output)
```

**输出：**

```python
{'mean': tensor(0.9550), 'std': tensor(0.0421), 'quantile': tensor([0.8696, 1.0000])}
```
