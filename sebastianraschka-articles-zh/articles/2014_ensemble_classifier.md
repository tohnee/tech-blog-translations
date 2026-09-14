---
title: "加权多数投票分类器"
title_en: "Weighted Majority Vote Classifier"
source: https://sebastianraschka.com/Articles/2014_ensemble_classifier.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 加权多数投票分类器

> 原文：[Weighted Majority Vote Classifier](https://sebastianraschka.com/Articles/2014_ensemble_classifier.html) · Sebastian Raschka's Articles

如果你有兴趣使用 `EnsembleClassifier`，请注意它如今也可以通过 scikit-learn（>0.17）以 [`VotingClassifier`](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.VotingClassifier.html) 的形式使用。

在这篇文章中，我想介绍一种简单而保守的方法：在 [scikit-learn](http://scikit-learn.org/stable/) 中实现一个基于加权多数投票规则（weighted majority rule）的集成分类器（ensemble classifier）。当我在一次 [kaggle](https://www.kaggle.com) 竞赛中尝试它时，它取得了相当不错的效果。对我个人而言，kaggle 竞赛只是尝试和比较不同方法与思路的好途径——本质上是在一个可控的环境里、借助优质数据集来学习的机会。

当然，scikit-learn 中已经有更为复杂的[集成方法](http://scikit-learn.org/stable/modules/ensemble.html)（ensemble methods）的实现，例如[装袋分类器](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.BaggingClassifier.html)（bagging，即 bootstrap aggregating，自助聚合）、[随机森林](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)（random forest），以及著名的 [AdaBoost](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html) 算法。不过，就我看来，它们都要求使用一个共同的「基分类器」。

相比之下，我采用下面这种方法的动机是：把概念上不同的机器学习分类器组合起来，并使用多数投票规则。原因在于，我已经训练出了一组性能相当的模型，希望通过组合来平衡它们各自的弱点。

## 章节

## 用不同的分类模型对鸢尾花进行分类

举一个简单的例子，让我们使用三种不同的分类模型来对[鸢尾花（Iris）数据集](https://en.wikipedia.org/wiki/Iris_flower_data_set)中的样本进行分类：逻辑回归（logistic regression）、使用高斯核的朴素贝叶斯（naive Bayes）分类器，以及随机森林分类器——它本身就是一种集成方法。在这一步，我们暂时不必操心数据预处理以及训练集/测试集的划分问题。另外，我们只使用 2 个特征列（花萼宽度和花瓣高度），以增加分类问题的难度。

```python
from sklearn import datasets

iris = datasets.load_iris()
X, y = iris.data[:, 1:3], iris.target
```

```python
from sklearn import cross_validation
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
import numpy as np

np.random.seed(123)

clf1 = LogisticRegression()
clf2 = RandomForestClassifier()
clf3 = GaussianNB()

print('5-fold cross validation:\n')

for clf, label in zip([clf1, clf2, clf3], ['Logistic Regression', 'Random Forest', 'naive Bayes']):

    scores = cross_validation.cross_val_score(clf, X, y, cv=5, scoring='accuracy')
    print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))
```

```python
5-fold cross validation:

Accuracy: 0.90 (+/- 0.05) [Logistic Regression]
Accuracy: 0.92 (+/- 0.05) [Random Forest]
Accuracy: 0.91 (+/- 0.04) [naive Bayes]
```

从上面的交叉验证结果可以看出，这三个模型的性能几乎不相上下。

## 实现基于多数投票规则的集成分类器

现在，我们来实现一个简单的 `EnsembleClassifier` 类，它允许我们把这三个不同的分类器组合起来。我们定义一个 `predict` 方法，直接对各个分类器的预测结果应用多数规则（majority rule）。
例如，如果某个样本的预测结果为

- 分类器 1 -> 类别 1
- 分类器 2 -> 类别 1
- 分类器 3 -> 类别 2

那么我们就把这个样本归类为「类别 1」。

此外，我们还添加了一个 `weights` 参数，用于为每个分类器指定特定的权重。为了使用这些权重，我们会收集每个分类器预测的类别概率，将其乘以对应分类器的权重，然后取平均值。基于这些加权平均概率，我们就可以确定类别标签。

为了用一个简单的例子来说明，假设我们有 3 个分类器，面对的是一个 3 类分类问题，并且为所有分类器分配相同的权重（默认设置）：w1=1、w2=1、w3=1。

此时，某个样本的加权平均概率将按如下方式计算：

| 分类器 | 类别 1 | 类别 2 | 类别 3 |
| --- | --- | --- | --- |
| 分类器 1 | w1 \* 0.2 | w1 \* 0.5 | w1 \* 0.3 |
| 分类器 2 | w2 \* 0.6 | w2 \* 0.3 | w2 \* 0.1 |
| 分类器 3 | w3 \* 0.3 | w3 \* 0.4 | w3 \* 0.3 |
| 加权平均 | 0.37 | 0.40 | 0.23 |

从上表可以看出，类别 2 的加权平均概率最高，因此我们把该样本归类为类别 2。

现在，让我们把它落实成代码，并应用到我们的鸢尾花分类任务中。

```python
from sklearn.base import BaseEstimator
from sklearn.base import ClassifierMixin
import numpy as np
import operator

class EnsembleClassifier(BaseEstimator, ClassifierMixin):
    """
    Ensemble classifier for scikit-learn estimators.

    Parameters
    ----------

    clf : `iterable`
      A list of scikit-learn classifier objects.
    weights : `list` (default: `None`)
      If `None`, the majority rule voting will be applied to the predicted class labels.
        If a list of weights (`float` or `int`) is provided, the averaged raw probabilities (via `predict_proba`)
        will be used to determine the most confident class label.

    """
    def __init__(self, clfs, weights=None):
        self.clfs = clfs
        self.weights = weights

    def fit(self, X, y):
        """
        Fit the scikit-learn estimators.

        Parameters
        ----------

        X : numpy array, shape = [n_samples, n_features]
            Training data
        y : list or numpy array, shape = [n_samples]
            Class labels

        """
        for clf in self.clfs:
            clf.fit(X, y)

    def predict(self, X):
        """
        Parameters
        ----------

        X : numpy array, shape = [n_samples, n_features]

        Returns
        ----------

        maj : list or numpy array, shape = [n_samples]
            Predicted class labels by majority rule

        """

        self.classes_ = np.asarray([clf.predict(X) for clf in self.clfs])
        if self.weights:
            avg = self.predict_proba(X)

            maj = np.apply_along_axis(lambda x: max(enumerate(x), key=operator.itemgetter(1))[0], axis=1, arr=avg)

        else:
            maj = np.asarray([np.argmax(np.bincount(self.classes_[:,c])) for c in range(self.classes_.shape[1])])

        return maj

    def predict_proba(self, X):

        """
        Parameters
        ----------

        X : numpy array, shape = [n_samples, n_features]

        Returns
        ----------

        avg : list or numpy array, shape = [n_samples, n_probabilities]
            Weighted average probability for each class per sample.

        """
        self.probas_ = [clf.predict_proba(X) for clf in self.clfs]
        avg = np.average(self.probas_, axis=0, weights=self.weights)

        return avg
```

```python
np.random.seed(123)
eclf = EnsembleClassifier(clfs=[clf1, clf2, clf3], weights=[1,1,1])

for clf, label in zip([clf1, clf2, clf3, eclf], ['Logistic Regression', 'Random Forest', 'naive Bayes', 'Ensemble']):

    scores = cross_validation.cross_val_score(clf, X, y, cv=5, scoring='accuracy')
    print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))
```

```python
Accuracy: 0.90 (+/- 0.05) [Logistic Regression]
Accuracy: 0.92 (+/- 0.05) [Random Forest]
Accuracy: 0.91 (+/- 0.04) [naive Bayes]
Accuracy: 0.95 (+/- 0.03) [Ensemble]
```

## 关于 EnsembleClassifier 实现的补充说明：类别标签 vs. 概率

你可能会好奇，为什么我把 `EnsembleClassifier` 类实现成这样：在不提供权重时，它纯粹基于类别标签进行多数投票；否则则使用预测的概率值。

让我们考虑下面这个场景：

### 1) 基于多数类别标签的预测：

| 分类器 | 类别 1 | 类别 2 |
| --- | --- | --- |
| 分类器 1 | 1 | 0 |
| 分类器 2 | 0 | 1 |
| 分类器 3 | 0 | 1 |
| 预测结果 | - | 1 |

要实现这种行为，请像这样初始化 `EnsembleClassifier`：

```python
eclf = EnsembleClassifier(clfs=[clf1, clf2, clf3])
```

### 2) 基于预测概率的预测（等权重，`weights=[1,1,1]`）

| 分类器 | 类别 1 | 类别 2 |
| --- | --- | --- |
| 分类器 1 | 0.99 | 0.01 |
| 分类器 2 | 0.49 | 0.51 |
| 分类器 3 | 0.49 | 0.51 |
| 加权平均 | 0.66 | 0.18 |
| 预测结果 | 1 | - |

要实现这种行为，请像这样初始化 `EnsembleClassifier`：

```python
eclf = EnsembleClassifier(clfs=[clf1, clf2, clf3], weights=[1,1,1])
```

正如我们所见，基于类别标签应用多数投票，与取预测概率的平均值，所得的结果是不同的。总体而言，我认为使用预测概率（场景 2）更合理。在这个场景中，「非常自信」的分类器 1 压倒了非常不自信的分类器 2 和 3。

之所以提供两种不同的行为，是因为 scikit-learn 中并非所有分类器都支持 `predict_proba` 方法。在这种情况下，只要不提供 weights 参数，`EnsembleClassifier` 仍然可以仅基于类别标签来使用。

## EnsembleClassifier——权重调优

让我们回到 `weights` 参数上来。这里，我们将使用一种朴素的暴力搜索方法来为每个分类器寻找最优权重，以提高预测准确率。

```python
import pandas as pd

np.random.seed(123)

df = pd.DataFrame(columns=('w1', 'w2', 'w3', 'mean', 'std'))

i = 0
for w1 in range(1,4):
    for w2 in range(1,4):
        for w3 in range(1,4):

            if len(set((w1,w2,w3))) == 1: # skip if all weights are equal
                continue

            eclf = EnsembleClassifier(clfs=[clf1, clf2, clf3], weights=[w1,w2,w3])
            scores = cross_validation.cross_val_score(
                                            estimator=eclf,
                                            X=X,
                                            y=y,
                                            cv=5,
                                            scoring='accuracy',
                                            n_jobs=1)

            df.loc[i] = [w1, w2, w3, scores.mean(), scores.std()]
            i += 1

df.sort(columns=['mean', 'std'], ascending=False)
```

|  | w1 | w2 | w3 | 均值 | 标准差 |
| --- | --- | --- | --- | --- | --- |
| 2 | 1 | 2 | 1 | 0.953333 | 0.033993 |
| 17 | 3 | 1 | 2 | 0.953333 | 0.033993 |
| 16 | 3 | 1 | 1 | 0.946667 | 0.045216 |
| 20 | 3 | 2 | 2 | 0.946667 | 0.045216 |
| 1 | 1 | 1 | 3 | 0.946667 | 0.040000 |
| 6 | 1 | 3 | 2 | 0.946667 | 0.033993 |
| 7 | 1 | 3 | 3 | 0.946667 | 0.033993 |
| 11 | 2 | 2 | 1 | 0.946667 | 0.033993 |
| 13 | 2 | 3 | 1 | 0.946667 | 0.033993 |
| 14 | 2 | 3 | 2 | 0.946667 | 0.033993 |
| 18 | 3 | 1 | 3 | 0.946667 | 0.033993 |
| 22 | 3 | 3 | 1 | 0.946667 | 0.033993 |
| 23 | 3 | 3 | 2 | 0.946667 | 0.033993 |
| 19 | 3 | 2 | 1 | 0.940000 | 0.057349 |
| 5 | 1 | 3 | 1 | 0.940000 | 0.044222 |
| 8 | 2 | 1 | 1 | 0.940000 | 0.044222 |
| 9 | 2 | 1 | 2 | 0.940000 | 0.044222 |
| 12 | 2 | 2 | 3 | 0.940000 | 0.044222 |
| 21 | 3 | 2 | 3 | 0.940000 | 0.044222 |
| 4 | 1 | 2 | 3 | 0.940000 | 0.038873 |
| 3 | 1 | 2 | 2 | 0.940000 | 0.032660 |
| 10 | 2 | 1 | 3 | 0.940000 | 0.032660 |
| 0 | 1 | 1 | 2 | 0.933333 | 0.047140 |
| 15 | 2 | 3 | 3 | 0.933333 | 0.047140 |

## EnsembleClassifier——流水线（Pipeline）

当然，我们也可以在 `Pipeline`（流水线）中使用 `EnsembleClassifier`。当某个分类器在特定的特征子集上表现出色，或者需要不同的 `preprocessing`（预处理）步骤时，这种用法尤其有用。为了演示，我们来实现一个简单的 `ColumnSelector` 类。

```python
class ColumnSelector(object):
    """
    A feature selector for scikit-learn's Pipeline class that returns
    specified columns from a numpy array.

    """

    def __init__(self, cols):
        self.cols = cols

    def transform(self, X, y=None):
        return X[:, self.cols]

    def fit(self, X, y=None):
        return self
```

```python
from sklearn.pipeline import Pipeline
from sklearn.lda import LDA

pipe1 = Pipeline([
               ('sel', ColumnSelector([1])),    # use only the 1st feature
               ('clf', GaussianNB())])

pipe2 = Pipeline([
               ('sel', ColumnSelector([0, 1])), # use the 1st and 2nd feature
               ('dim', LDA(n_components=1)),    # Dimensionality reduction via LDA
               ('clf', LogisticRegression())])

eclf = EnsembleClassifier([pipe1, pipe2])
scores = cross_validation.cross_val_score(eclf, X, y, cv=5, scoring='accuracy')
print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))
```

```python
Accuracy: 0.95 (+/- 0.03) [Ensemble]
```

```python
pipe1 = Pipeline([
               ('sel', ColumnSelector([1])), # use only the 1st feature
               ('clf', RandomForestClassifier())])

pipe2 = Pipeline([
               ('sel', ColumnSelector([0, 1])), # use the 1st and 2nd feature
               ('dim', LDA(n_components=1)), # Dimensionality reduction via LDA
               ('clf', LogisticRegression())])

pipe3 = Pipeline([
               ('eclf', EnsembleClassifier([pipe1, pipe2])),
])
parameters = {
'eclf__clfs__dim__n_components':(1,1),
}
grid_search = GridSearchCV(pipe3, parameters, n_jobs=-1, cv=5, verbose=5, refit=True, scoring=None)
grid_search.fit(X, y)
```

## 结语

当我们把 `EnsembleClassifier` 应用到上面的鸢尾花示例时，结果看起来确实很不错。但我们必须记住，这只是一个玩具级的例子。多数投票方法在实践中未必总能取得这么好的效果，尤其是当集成中「弱」分类模型比「强」分类模型更多的时候。此外，尽管我们使用了交叉验证来应对过拟合问题，也请始终保留一份备用的验证数据集来评估结果。

无论如何，如果你对这些方法感兴趣，我已经把它们添加到了我的 Python 模块 [`mlxtend`](http://rasbt.github.io/mlxtend/) 中；在 mlxtend（「machine learning library extensions」的缩写）里，我收集了一些我个人觉得有用、但其他软件包尚未提供的功能。

你可以在 <http://rasbt.github.io/mlxtend/> 找到最新的文档。
