---
title: "线性判别分析"
title_en: "Linear Discriminant Analysis"
source: https://sebastianraschka.com/Articles/2014_python_lda.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 线性判别分析

> 原文：[Linear Discriminant Analysis](https://sebastianraschka.com/Articles/2014_python_lda.html) · Sebastian Raschka's Articles

![Linear discriminant analysis lda 1](https://sebastianraschka.com/images/blog/2014/linear-discriminant-analysis/lda_1.webp)

### 章节

## 引言

线性判别分析（Linear Discriminant Analysis，LDA）最常用作降维技术，应用在模式分类和机器学习任务的预处理步骤中。其目标是将数据集投影到一个具有良好类别可分性的低维空间中，以避免过拟合（「维数灾难」），同时降低计算成本。

Ronald A. Fisher 在 1936 年提出了*线性判别*（Linear Discriminant）（[The Use of Multiple Measurements in Taxonomic Problems](http://onlinelibrary.wiley.com/doi/10.1111/j.1469-1809.1936.tb02137.x/abstract)），它作为分类器也有一些实际用途。最初的线性判别是针对 2 分类问题提出的，后来由 C. R. Rao 在 1948 年将其推广为「多类线性判别分析」（multi-class Linear Discriminant Analysis）或「多重判别分析」（Multiple Discriminant Analysis）（[The utilization of multiple measurements in problems of biological classification](http://www.jstor.org/stable/2983775)）。

**一般的 LDA 方法与主成分分析（Principal Component Analysis，PCA）非常相似（关于 PCA 的更多信息，请参阅前一篇文章[《Implementing a Principal Component Analysis (PCA) in Python step by step》（在 Python 中一步步实现主成分分析）](https://sebastianraschka.com/Articles/2014_pca_step_by_step.html)），但除了寻找使数据方差最大化的成分轴（PCA）之外，我们还对使多个类别之间分离程度最大化的坐标轴（LDA）感兴趣。**

简而言之，LDA 的目标通常是将特征空间（一个由 n 维样本组成的数据集）投影到一个更小的子空间 \(k\)（其中 \(k \leq n-1\)）上，同时保持类别的判别信息。一般来说，降维不仅可以降低特定分类任务的计算成本，还可以通过最小化参数估计中的误差来帮助避免过拟合（「维数灾难」）。

### 主成分分析与线性判别分析

线性判别分析（LDA）和主成分分析（PCA）都是常用的线性变换技术，常用于降维。PCA 可以被描述为一种「无监督」算法，因为它「忽略」类别标签，其目标是找到使数据集方差最大化的方向（即所谓的主成分）。与 PCA 相比，LDA 是「有监督」的，它计算出的方向（「线性判别式」）将构成使多个类别之间分离程度最大化的坐标轴。

尽管直觉上，对于已知类别标签的多分类任务，LDA 似乎应该优于 PCA，但实际情况未必如此。例如，对图像识别任务在使用 PCA 或 LDA 之后分类精度的比较表明，当每个类别的样本数量相对较少时，PCA 往往优于 LDA（[PCA vs. LDA](http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber=908974)，A.M. Martinez et al., 2001）。在实践中，把 LDA 和 PCA 结合起来使用也很常见：例如，先用 PCA 降维，然后再做 LDA。

### 什么是「好」的特征子空间？

假设我们的目标是通过将一个 \(d\) 维数据集投影到一个 \((k)\) 维子空间（其中 \(k\;<\;d\)）来降低维度。那么，我们如何知道应该为 \(k\)（\(k\) = 新特征子空间的维数）选择多大的值，又如何知道我们得到的特征空间是否「很好地」表示了我们的数据呢？

稍后，我们将从数据集中计算特征向量（即各个成分），并把它们收集在所谓的散度矩阵（scatter matrix）中（即类间散度矩阵和类内散度矩阵）。每个特征向量都对应一个特征值，特征值告诉我们特征向量的「长度」或「大小」。

如果我们观察到所有特征值的量级都相近，那么这可能是我们的数据已经投影在一个「好」的特征空间上的良好指标。

而在另一种情形下，如果某些特征值比其他特征值大得多，我们可能只想保留特征值最大的那些特征向量，因为它们包含了更多关于数据分布的信息。反之，接近 0 的特征值所含信息较少，在构建新的特征子空间时我们可以考虑丢弃它们。

### 用 5 个步骤概括 LDA 方法

下面列出了执行线性判别分析的 5 个一般步骤；我们将在后面的章节中更详细地探讨它们。

1. 从数据集中计算不同类别的 \(d\) 维均值向量。
2. 计算散度矩阵（类间散度矩阵和类内散度矩阵）。
3. 计算散度矩阵的特征向量（\(\pmb e\_1, \; \pmb e\_2, \; ..., \; \pmb e\_d\)）及对应的特征值（\(\pmb \lambda\_1, \; \pmb \lambda\_2, \; ..., \; \pmb \lambda\_d\)）。
4. 将特征向量按特征值递减排序，并选择特征值最大的 \(k\) 个特征向量，构成一个 \(d \times k\) 维矩阵 \(\pmb W\)（其中每一列代表一个特征向量）。
5. 使用这个 \(d \times k\) 维特征向量矩阵将样本变换到新的子空间上。这可以用矩阵乘法来概括：\(\pmb Y = \pmb X \times \pmb W\)（其中 \(\pmb X\) 是表示 \(n\) 个样本的 \(n \times d\) 维矩阵，\(\pmb y\) 是新子空间中变换后的 \(n \times k\) 维样本）。

## 准备示例数据集

### 关于 Iris 数据集

在下面的教程中，我们将使用著名的「Iris」（鸢尾花）数据集，它存放于 UCI 机器学习仓库  
（https://archive.ics.uci.edu/ml/datasets/Iris）。

\*\*参考文献：\*\*
Bache, K. & Lichman, M. (2013). UCI Machine Learning Repository. Irvine, CA: University of California, School of Information and Computer Science.

Iris 数据集包含对 150 朵鸢尾花的测量数据，这些花分属三个不同的物种。

Iris 数据集中的三个类别：

1. Iris-setosa (n=50)
2. Iris-versicolor (n=50)
3. Iris-virginica (n=50)

Iris 数据集的四个特征：

1. 花萼长度（单位：cm）
2. 花萼宽度（单位：cm）
3. 花瓣长度（单位：cm）
4. 花瓣宽度（单位：cm）

![Linear discriminant analysis iris petal sepal](https://sebastianraschka.com/images/blog/2014/linear-discriminant-analysis/iris_petal_sepal.webp)

```python
feature_dict = {i:label for i,label in zip(
                range(4),
                  ('sepal length in cm',
                  'sepal width in cm',
                  'petal length in cm',
                  'petal width in cm', ))}
```

### 读取数据集

```python
import pandas as pd

df = pd.io.parsers.read_csv(
    filepath_or_buffer='https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data',
    header=None,
    sep=',',
    )
df.columns = [l for i,l in sorted(feature_dict.items())] + ['class label']
df.dropna(how="all", inplace=True) # to drop the empty line at file-end

df.tail()
```

|  | 花萼长度（cm） | 花萼宽度（cm） | 花瓣长度（cm） | 花瓣宽度（cm） | 类别标签 |
| --- | --- | --- | --- | --- | --- |
| 145 | 6.7 | 3.0 | 5.2 | 2.3 | Iris-virginica |
| 146 | 6.3 | 2.5 | 5.0 | 1.9 | Iris-virginica |
| 147 | 6.5 | 3.0 | 5.2 | 2.0 | Iris-virginica |
| 148 | 6.2 | 3.4 | 5.4 | 2.3 | Iris-virginica |
| 149 | 5.9 | 3.0 | 5.1 | 1.8 | Iris-virginica |

\[\pmb X = \begin{bmatrix} x\_{1\_{\text{sepal length}}} & x\_{1\_{\text{sepal width}}} & x\_{1\_{\text{petal length}}} & x\_{1\_{\text{petal width}}}\\
x\_{2\_{\text{sepal length}}} & x\_{2\_{\text{sepal width}}} & x\_{2\_{\text{petal length}}} & x\_{2\_{\text{petal width}}}\\
... \\
x\_{150\_{\text{sepal length}}} & x\_{150\_{\text{sepal width}}} & x\_{150\_{\text{petal length}}} & x\_{150\_{\text{petal width}}}\\
\end{bmatrix}, \;\;
\pmb y = \begin{bmatrix} \omega\_{\text{setosa}}\\
\omega\_{\text{setosa}}\\
... \\
\omega\_{\text{virginica}}\end{bmatrix}\]

由于使用数值进行处理更为方便，我们将使用 `scikit-learn` 库中的 `LabelEncode` 将类别标签转换为数字：`1, 2, and 3`。

```python
from sklearn.preprocessing import LabelEncoder

X = df[[0,1,2,3]].values
y = df['class label'].values

enc = LabelEncoder()
label_encoder = enc.fit(y)
y = label_encoder.transform(y) + 1

label_dict = {1: 'Setosa', 2: 'Versicolor', 3:'Virginica'}
```

\[\pmb y = \begin{bmatrix}{\text{setosa}}\\
{\text{setosa}}\\
... \\
{\text{virginica}}\end{bmatrix} \quad \Rightarrow
\begin{bmatrix} {\text{1}}\\
{\text{1}}\\
... \\
{\text{3}}\end{bmatrix}\]

### 直方图与特征选择

为了粗略了解我们的三个类别 \(\omega\_1\)、\(\omega\_2\) 和 \(\omega\_3\) 的样本分布情况，让我们用一维直方图来可视化四个不同特征的分布。

```python
%matplotlib inline
```

```python
from matplotlib import pyplot as plt
import numpy as np
import math

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12,6))

for ax,cnt in zip(axes.ravel(), range(4)):  

    # set bin sizes
    min_b = math.floor(np.min(X[:,cnt]))
    max_b = math.ceil(np.max(X[:,cnt]))
    bins = np.linspace(min_b, max_b, 25)

    # plottling the histograms
    for lab,col in zip(range(1,4), ('blue', 'red', 'green')):
        ax.hist(X[y==lab, cnt],
                   color=col,
                   label='class %s' %label_dict[lab],
                   bins=bins,
                   alpha=0.5,)
    ylims = ax.get_ylim()

    # plot annotation
    leg = ax.legend(loc='upper right', fancybox=True, fontsize=8)
    leg.get_frame().set_alpha(0.5)
    ax.set_ylim([0, max(ylims)+2])
    ax.set_xlabel(feature_dict[cnt])
    ax.set_title('Iris histogram #%s' %str(cnt+1))

    # hide axis ticks
    ax.tick_params(axis="both", which="both", bottom="off", top="off",  
            labelbottom="on", left="off", right="off", labelleft="on")

    # remove axis spines
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)    

axes[0][0].set_ylabel('count')
axes[1][0].set_ylabel('count')

fig.tight_layout()       

plt.show()
```

![Linear discriminant analysis](https://sebastianraschka.com/images/blog/2014/linear-discriminant-analysis/2014-08-03-linear_discriminant_analysis_51_0.webp)

仅仅通过观察这些简单的特征分布图，我们已经可以看出，花瓣长度和花瓣宽度可能更适合作为区分三个花类的潜在特征。在实践中，除了通过投影（这里是 LDA）来降维之外，特征选择技术也是一个很好的替代方案。对于像 Iris 这样的低维数据集，看一眼这些直方图就能获得很多信息。另一种简单但非常实用的做法是使用特征选择算法；如果你感兴趣，我在[这里](http://rasbt.github.io/mlxtend/user_guide/feature_selection/SequentialFeatureSelector/)有一篇关于序列特征选择算法的更详细描述，scikit-learn 也实现了不少不错的替代[方法](http://scikit-learn.org/stable/modules/feature_selection.html)。关于这些不同方法的高层次总结，我写过一篇短文：[《特征选择中的过滤式、包裹式和嵌入式方法有什么区别？》](https://sebastianraschka.com/faq/docs/feature_sele_categories.html)。

### 正态性假设

需要说明的是，LDA 假设数据服从正态分布、各特征在统计上相互独立，并且每个类别具有相同的协方差矩阵。不过，这些要求只适用于把 LDA 用作分类器的情形；即使这些假设不成立，用于降维的 LDA 通常也能工作得相当好。而且即使在分类任务中，LDA 对数据的分布似乎也相当鲁棒：

> 「线性判别分析在人脸和物体识别任务中经常能取得良好的性能，
> 尽管各组具有相同协方差矩阵以及正态性这些假设往往并不成立
> （Duda, et al., 2001）」（Tao Li, et al., 2006）。

Tao Li, Shenghuo Zhu, and Mitsunori Ogihara. “[Using Discriminant Analysis for Multi-Class Classification: An Experimental Investigation](http://link.springer.com/article/10.1007%2Fs10115-006-0013-y).” Knowledge and Information Systems 10, no. 4 (2006): 453–72.)

Duda, Richard O, Peter E Hart, and David G Stork. 2001. Pattern Classification. New York: Wiley.

## 分 5 步执行 LDA

在完成了前面若干准备步骤之后，我们的数据终于可以用于真正的 LDA 了。在实践中，用于降维的 LDA 只是典型的机器学习或模式分类任务中又一个普通的预处理步骤。

### 第 1 步：计算 d 维均值向量

在第一步中，我们先来简单地计算 3 个不同花类的均值向量 \(\pmb m\_i\)，\((i = 1,2,3)\)：

\[\pmb m\_i = \begin{bmatrix}
\mu\_{\omega\_i (\text{sepal length)}}\\
\mu\_{\omega\_i (\text{sepal width})}\\
\mu\_{\omega\_i (\text{petal length)}}\\
\mu\_{\omega\_i (\text{petal width})}\\
\end{bmatrix} \; , \quad \text{with} \quad i = 1,2,3\]

```python
np.set_printoptions(precision=4)

mean_vectors = []
for cl in range(1,4):
    mean_vectors.append(np.mean(X[y==cl], axis=0))
    print('Mean Vector class %s: %s\n' %(cl, mean_vectors[cl-1]))
```

```python
Mean Vector class 1: [ 5.006  3.418  1.464  0.244]

Mean Vector class 2: [ 5.936  2.77   4.26   1.326]

Mean Vector class 3: [ 6.588  2.974  5.552  2.026]
```

### 第 2 步：计算散度矩阵

现在，我们将计算两个 *4x4* 维的矩阵：类内散度矩阵和类间散度矩阵。

#### 2.1 类内散度矩阵 \(S\_W\)

**类内散度**（within-class scatter）矩阵 \(S\_W\) 由以下公式计算：

\[S\_W = \sum\limits\_{i=1}^{c} S\_i\]

其中  
\(S\_i = \sum\limits\_{\pmb x \in D\_i}^n (\pmb x - \pmb m\_i)\;(\pmb x - \pmb m\_i)^T\)  
（每个类别的散度矩阵）

而 \(\pmb m\_i\) 是均值向量  
\(\pmb m\_i = \frac{1}{n\_i} \sum\limits\_{\pmb x \in D\_i}^n \; \pmb x\_k\)

```python
S_W = np.zeros((4,4))
for cl,mv in zip(range(1,4), mean_vectors):
    class_sc_mat = np.zeros((4,4))                  # scatter matrix for every class
    for row in X[y == cl]:
        row, mv = row.reshape(4,1), mv.reshape(4,1) # make column vectors
        class_sc_mat += (row-mv).dot((row-mv).T)
    S_W += class_sc_mat                             # sum class scatter matrices
print('within-class Scatter Matrix:\n', S_W)
```

```python
within-class Scatter Matrix:
 [[ 38.9562  13.683   24.614    5.6556]
 [ 13.683   17.035    8.12     4.9132]
 [ 24.614    8.12    27.22     6.2536]
 [  5.6556   4.9132   6.2536   6.1756]]
```

#### 2.1 b

作为替代方案，我们也可以通过在类内散度矩阵中加入缩放因子 \(\frac{1}{N-1}\) 来计算类协方差矩阵，这样我们的公式就变为

\(\Sigma\_i = \frac{1}{N\_{i}-1} \sum\limits\_{\pmb x \in D\_i}^n (\pmb x - \pmb m\_i)\;(\pmb x - \pmb m\_i)^T\)。

以及 \(S\_W = \sum\limits\_{i=1}^{c} (N\_{i}-1) \Sigma\_i\)

其中 \(N\_{i}\) 是相应类别的样本数量（这里为 50）。在这个特定案例中，由于所有类别的样本数量都相同，我们可以去掉 (\(N\_{i}-1)\) 这一项。

不过，最终得到的特征空间将是相同的（特征向量相同，只是特征值按一个常数因子有不同的缩放）。

#### 2.2 类间散度矩阵 \(S\_B\)

**类间散度**（between-class scatter）矩阵 \(S\_B\) 由以下公式计算：

\[S\_B = \sum\limits\_{i=1}^{c} N\_{i} (\pmb m\_i - \pmb m) (\pmb m\_i - \pmb m)^T\]

其中  
\(\pmb m\) 是总体均值，\(\pmb m\_{i}\) 和 \(N\_{i}\) 分别是相应类别的样本均值和样本数量。

```python
overall_mean = np.mean(X, axis=0)

S_B = np.zeros((4,4))
for i,mean_vec in enumerate(mean_vectors):  
    n = X[y==i+1,:].shape[0]
    mean_vec = mean_vec.reshape(4,1) # make column vector
    overall_mean = overall_mean.reshape(4,1) # make column vector
    S_B += n * (mean_vec - overall_mean).dot((mean_vec - overall_mean).T)

print('between-class Scatter Matrix:\n', S_B)
```

```python
between-class Scatter Matrix:
 [[  63.2121  -19.534   165.1647   71.3631]
 [ -19.534    10.9776  -56.0552  -22.4924]
 [ 165.1647  -56.0552  436.6437  186.9081]
 [  71.3631  -22.4924  186.9081   80.6041]]
```

### 第 3 步：求解矩阵 \(S\_{W}^{-1}S\_B\) 的广义特征值问题

接下来，我们将求解矩阵 \(S\_{W}^{-1}S\_B\) 的广义特征值问题，以得到线性判别式。

```python
eig_vals, eig_vecs = np.linalg.eig(np.linalg.inv(S_W).dot(S_B))

for i in range(len(eig_vals)):
    eigvec_sc = eig_vecs[:,i].reshape(4,1)   
    print('\nEigenvector {}: \n{}'.format(i+1, eigvec_sc.real))
    print('Eigenvalue {:}: {:.2e}'.format(i+1, eig_vals[i].real))
```

```python
Eigenvector 1:
[[-0.2049]
 [-0.3871]
 [ 0.5465]
 [ 0.7138]]
Eigenvalue 1: 3.23e+01

Eigenvector 2:
[[-0.009 ]
 [-0.589 ]
 [ 0.2543]
 [-0.767 ]]
Eigenvalue 2: 2.78e-01

Eigenvector 3:
[[ 0.179 ]
 [-0.3178]
 [-0.3658]
 [ 0.6011]]
Eigenvalue 3: -4.02e-17

Eigenvector 4:
[[ 0.179 ]
 [-0.3178]
 [-0.3658]
 [ 0.6011]]
Eigenvalue 4: -4.02e-17
```

**注意**

取决于我们所使用的 NumPy 和 LAPACK 的版本，我们得到的矩阵 \(\mathbf{W}\) 的符号可能会翻转。请注意，这并不是一个问题；如果 \(\mathbf{v}\) 是矩阵 \(\Sigma\) 的一个特征向量，我们有

\(\Sigma \mathbf{v} = \lambda \mathbf{v}\)。

这里，\(\lambda\) 是特征值，而 \(\mathbf{v}\) 也是一个具有相同特征值的特征向量，因为

\(\mathbf{Sigma} (-\mathbf{v}) = - \mathbf{-v} \Sigma= -\lambda \mathbf{v} = \lambda (-\mathbf{v})\)。

在把方阵分解为特征向量和特征值之后，让我们简要回顾一下如何解读这些结果。正如我们在高中或大学的第一堂线性代数课上所学到的，特征向量和特征值都为我们提供了关于线性变换扭曲的信息：特征向量基本上就是这种扭曲的方向，而特征值是特征向量的缩放因子，描述了扭曲的程度。

如果我们执行 LDA 的目的是降维，那么特征向量非常重要，因为它们将构成新特征子空间的新坐标轴；与之关联的特征值尤其值得关注，因为它们会告诉我们这些新「坐标轴」的「信息量」有多大。

让我们简要验证一下计算结果，并在下一节继续讨论特征值。

#### 检查特征向量-特征值的计算

快速检查特征向量-特征值的计算是否正确、是否满足以下方程：

\[\pmb A\pmb{v} = \lambda\pmb{v}\]

其中  
\(\pmb A = S\_{W}^{-1}S\_B\\
\pmb{v} = \; \text{Eigenvector}\\
\lambda = \; \text{Eigenvalue}\)

```python
for i in range(len(eig_vals)):
    eigv = eig_vecs[:,i].reshape(4,1)
    np.testing.assert_array_almost_equal(np.linalg.inv(S_W).dot(S_B).dot(eigv),
                                         eig_vals[i] * eigv,
                                         decimal=6, err_msg='', verbose=True)
print('ok')
```

```python
ok
```

### 第 4 步：为新的特征子空间选择线性判别式

#### 4.1. 将特征向量按特征值递减排序

回顾一下引言部分的内容：我们不只是想简单地把数据投影到一个能改善类别可分性的子空间中，还想降低特征空间的维度（特征向量将构成这个新特征子空间的坐标轴）。

然而，特征向量只定义了新坐标轴的方向，因为它们都具有相同的单位长度 1。

因此，为了决定在构建低维子空间时要丢弃哪些特征向量，我们必须查看这些特征向量所对应的特征值。粗略地说，特征值最低的特征向量所携带的关于数据分布的信息最少，这些正是我们想要丢弃的。常见的做法是将特征向量按对应的特征值从高到低排序，然后选择前 \(k\) 个特征向量。

```python
# Make a list of (eigenvalue, eigenvector) tuples
eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:,i]) for i in range(len(eig_vals))]

# Sort the (eigenvalue, eigenvector) tuples from high to low
eig_pairs = sorted(eig_pairs, key=lambda k: k[0], reverse=True)

# Visually confirm that the list is correctly sorted by decreasing eigenvalues

print('Eigenvalues in decreasing order:\n')
for i in eig_pairs:
    print(i[0])
```

```python
Eigenvalues in decreasing order:

32.2719577997
0.27756686384
5.71450476746e-15
5.71450476746e-15
```

**注意**

只要看一看这些特征值，我们就可以发现其中有两个特征值接近 0。它们接近 0 的原因并不是它们不含信息，而是浮点精度问题。事实上，最后这两个特征值本应恰好为零：在 LDA 中，线性判别式的数量最多为 \(c−1\)，其中 \(c\) 是类别标签的数量，这是因为类间散度矩阵 \(S\_B\) 是 \(c\) 个秩为 1 或更低的矩阵之和。注意，在罕见的完全共线情形下（所有对齐的样本点都落在一条直线上），协方差矩阵的秩将为 1，这将导致只有一个特征向量具有非零特征值。

现在，让我们把「解释方差」表示为百分比：

```python
print('Variance explained:\n')
eigv_sum = sum(eig_vals)
for i,j in enumerate(eig_pairs):
    print('eigenvalue {0:}: {1:.2%}'.format(i+1, (j[0]/eigv_sum).real))
```

```python
Variance explained:

eigenvalue 1: 99.15%
eigenvalue 2: 0.85%
eigenvalue 3: 0.00%
eigenvalue 4: 0.00%
```

第一个特征值-特征向量对（eigenpair）无疑是信息量最大的；如果基于这个特征对来构建 1 维特征空间，我们并不会损失多少信息。

#### 4.2. 选择特征值最大的 *k* 个特征向量

在按特征值递减顺序对特征对排序之后，现在可以构建我们的 \(d \times k\) 维特征向量矩阵 \(\pmb W\) 了（这里为 \(4 \times 2\)：基于信息量最大的 2 个特征对），从而把最初的 4 维特征空间降到 2 维特征子空间。

```python
W = np.hstack((eig_pairs[0][1].reshape(4,1), eig_pairs[1][1].reshape(4,1)))
print('Matrix W:\n', W.real)
```

```python
Matrix W:
 [[-0.2049 -0.009 ]
 [-0.3871 -0.589 ]
 [ 0.5465  0.2543]
 [ 0.7138 -0.767 ]]
```

## 第 5 步：将样本变换到新的子空间

在最后一步中，我们使用刚刚计算得到的 \(4 \times 2\) 维矩阵 \(\pmb W\)，通过方程

\(\pmb Y = \pmb X \times \pmb W\)。

将样本变换到新的子空间上。

（其中 \(\pmb X\) 是表示 \(n\) 个样本的 \(n \times d\) 维矩阵，\(\pmb Y\) 是新子空间中变换后的 \(n \times k\) 维样本。）

```python
X_lda = X.dot(W)
assert X_lda.shape == (150,2), "The matrix is not 150x2 dimensional."
```

```python
from matplotlib import pyplot as plt

def plot_step_lda():

    ax = plt.subplot(111)
    for label,marker,color in zip(
        range(1,4),('^', 's', 'o'),('blue', 'red', 'green')):

        plt.scatter(x=X_lda[:,0].real[y == label],
                y=X_lda[:,1].real[y == label],
                marker=marker,
                color=color,
                alpha=0.5,
                label=label_dict[label]
                )

    plt.xlabel('LD1')
    plt.ylabel('LD2')

    leg = plt.legend(loc='upper right', fancybox=True)
    leg.get_frame().set_alpha(0.5)
    plt.title('LDA: Iris projection onto the first 2 linear discriminants')

    # hide axis ticks
    plt.tick_params(axis="both", which="both", bottom="off", top="off",  
            labelbottom="on", left="off", right="off", labelleft="on")

    # remove axis spines
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)    

    plt.grid()
    plt.tight_layout
    plt.show()

plot_step_lda()
```

![Linear discriminant analysis](https://sebastianraschka.com/images/blog/2014/linear-discriminant-analysis/2014-08-03-linear_discriminant_analysis_120_0.webp)

上面的散点图表示的就是我们通过 LDA 构建的新特征子空间。可以看到，第一个线性判别式「LD1」相当漂亮地把各个类别分开了。而第二个判别式「LD2」并没有增加多少有价值的信息——这一点我们在第 4 步查看排序后的特征值时就已经得出结论了。

## PCA 与 LDA 的比较

为了与通过线性判别分析得到的特征子空间进行比较，我们将使用 `scikit-learn` 机器学习库中的 `PCA` 类。其文档见这里：  
<http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html>。

为了方便起见，我们可以通过 `n_components` 参数直接指定要在输入数据集中保留多少个成分。

```python
n_components : int, None or string

Number of components to keep. if n_components is not set all components are kept:
    n_components == min(n_samples, n_features)
    if n_components == ‘mle’, Minka’s MLE is used to guess the dimension if 0 < n_components < 1,
    select the number of components such that the amount of variance that needs to be explained
    is greater than the percentage specified by n_components
```

不过，在直接跳到各自线性变换的结果之前，让我们快速回顾一下 PCA 和 LDA 的目的：PCA 寻找使整个数据集方差最大的坐标轴，而 LDA 试图寻找能实现最佳类别可分性的坐标轴。在实践中，常常是先做一次 PCA，再跟着做一次 LDA 来降维。

![Linear discriminant analysis lda 1](https://sebastianraschka.com/images/blog/2014/linear-discriminant-analysis/lda_1.webp)

```python
from sklearn.decomposition import PCA as sklearnPCA

sklearn_pca = sklearnPCA(n_components=2)
X_pca = sklearn_pca.fit_transform(X)

def plot_pca():

    ax = plt.subplot(111)

    for label,marker,color in zip(
        range(1,4),('^', 's', 'o'),('blue', 'red', 'green')):

        plt.scatter(x=X_pca[:,0][y == label],
                y=X_pca[:,1][y == label],
                marker=marker,
                color=color,
                alpha=0.5,
                label=label_dict[label]
                )

    plt.xlabel('PC1')
    plt.ylabel('PC2')

    leg = plt.legend(loc='upper right', fancybox=True)
    leg.get_frame().set_alpha(0.5)
    plt.title('PCA: Iris projection onto the first 2 principal components')

    # hide axis ticks
    plt.tick_params(axis="both", which="both", bottom="off", top="off",  
            labelbottom="on", left="off", right="off", labelleft="on")

    # remove axis spines
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)    

    plt.tight_layout
    plt.grid()

    plt.show()
```

```python
plot_pca()
plot_step_lda()
```

![Linear discriminant analysis](https://sebastianraschka.com/images/blog/2014/linear-discriminant-analysis/2014-08-03-linear_discriminant_analysis_133_0.webp)

![Linear discriminant analysis](https://sebastianraschka.com/images/blog/2014/linear-discriminant-analysis/2014-08-03-linear_discriminant_analysis_133_1.webp)

上面两幅图很好地印证了我们之前讨论的内容：PCA 关注的是使整个数据集方差最大的坐标轴，而 LDA 给出的坐标轴关注的则是各个类别之间方差最大的方向。

## 通过 scikit-learn 执行 LDA

现在，我们已经看到了如何用逐步（step-by-step）的方式来实现线性判别分析；此外还有一种更便捷的方式可以达到同样的目的，即使用 [`scikit-learn`](http://scikit-learn.org/stable/) 机器学习库中实现的 `LDA` 类。

```python
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

# LDA
sklearn_lda = LDA(n_components=2)
X_lda_sklearn = sklearn_lda.fit_transform(X, y)
```

```python
def plot_scikit_lda(X, title):

    ax = plt.subplot(111)
    for label,marker,color in zip(
        range(1,4),('^', 's', 'o'),('blue', 'red', 'green')):

        plt.scatter(x=X[:,0][y == label],
                    y=X[:,1][y == label] * -1, # flip the figure
                    marker=marker,
                    color=color,
                    alpha=0.5,
                    label=label_dict[label])

    plt.xlabel('LD1')
    plt.ylabel('LD2')

    leg = plt.legend(loc='upper right', fancybox=True)
    leg.get_frame().set_alpha(0.5)
    plt.title(title)

    # hide axis ticks
    plt.tick_params(axis="both", which="both", bottom="off", top="off",  
            labelbottom="on", left="off", right="off", labelleft="on")

    # remove axis spines
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)    

    plt.grid()
    plt.tight_layout
    plt.show()
```

```python
plot_step_lda()
plot_scikit_lda(X_lda_sklearn, title='Default LDA via scikit-learn')
```

![Linear discriminant analysis](https://sebastianraschka.com/images/blog/2014/linear-discriminant-analysis/2014-08-03-linear_discriminant_analysis_142_0.webp)

![Linear discriminant analysis](https://sebastianraschka.com/images/blog/2014/linear-discriminant-analysis/2014-08-03-linear_discriminant_analysis_142_1.webp)

## 关于标准化的一点说明

为了回应我最近收到的一个问题，我想澄清一点：诸如标准化（standardization）这类的特征缩放**不会**改变 LDA 的总体结果，因此可以说是可选的。是的，散度矩阵会因特征是否经过缩放而不同；此外，特征向量也会有所不同。但关键在于，特征值以及最终的投影结果将是完全相同的——你会注意到的唯一区别就是成分轴的缩放。这一点可以从数学上加以证明（今后我会把公式补充进来），下面是一个用于演示的直观实例。

```python
%matplotlib inline
import pandas as pd
import matplotlib.pyplot as plt

import pandas as pd

df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data', header=None)
df[4] = df[4].map({'Iris-setosa':0, 'Iris-versicolor':1, 'Iris-virginica':2})
df.tail()
```

|  | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| 145 | 6.7 | 3.0 | 5.2 | 2.3 | 2 |
| 146 | 6.3 | 2.5 | 5.0 | 1.9 | 2 |
| 147 | 6.5 | 3.0 | 5.2 | 2.0 | 2 |
| 148 | 6.2 | 3.4 | 5.4 | 2.3 | 2 |
| 149 | 5.9 | 3.0 | 5.1 | 1.8 | 2 |

加载数据集之后，我们将对 `X` 中的各列进行标准化。标准化意味着均值中心化并缩放到单位方差：

\[x\_{std} = \frac{x - \mu\_x}{\sigma\_X}\]

标准化之后，各列将具有零均值（\(\mu\_{x\_{std}}=0\)）和等于 1 的标准差（\(\sigma\_{x\_{std}}=1\)）。

```python
y, X = df.iloc[:, 4].values, df.iloc[:, 0:4].values
X_cent = X - X.mean(axis=0)
X_std = X_cent / X.std(axis=0)
```

下面，为了方便起见，我简单地把我们前面讨论过的 LDA 的各个步骤封装成了 Python 函数。

```python
import numpy as np

def comp_mean_vectors(X, y):
    class_labels = np.unique(y)
    n_classes = class_labels.shape[0]
    mean_vectors = []
    for cl in class_labels:
        mean_vectors.append(np.mean(X[y==cl], axis=0))
    return mean_vectors

def scatter_within(X, y):
    class_labels = np.unique(y)
    n_classes = class_labels.shape[0]
    n_features = X.shape[1]
    mean_vectors = comp_mean_vectors(X, y)
    S_W = np.zeros((n_features, n_features))
    for cl, mv in zip(class_labels, mean_vectors):
        class_sc_mat = np.zeros((n_features, n_features))                 
        for row in X[y == cl]:
            row, mv = row.reshape(n_features, 1), mv.reshape(n_features, 1)
            class_sc_mat += (row-mv).dot((row-mv).T)
        S_W += class_sc_mat                           
    return S_W

def scatter_between(X, y):
    overall_mean = np.mean(X, axis=0)
    n_features = X.shape[1]
    mean_vectors = comp_mean_vectors(X, y)    
    S_B = np.zeros((n_features, n_features))
    for i, mean_vec in enumerate(mean_vectors):  
        n = X[y==i+1,:].shape[0]
        mean_vec = mean_vec.reshape(n_features, 1)
        overall_mean = overall_mean.reshape(n_features, 1)
        S_B += n * (mean_vec - overall_mean).dot((mean_vec - overall_mean).T)
    return S_B

def get_components(eig_vals, eig_vecs, n_comp=2):
    n_features = X.shape[1]
    eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:,i]) for i in range(len(eig_vals))]
    eig_pairs = sorted(eig_pairs, key=lambda k: k[0], reverse=True)
    W = np.hstack([eig_pairs[i][1].reshape(4, 1) for i in range(0, n_comp)])
    return W
```

首先，我们打印未缩放数据的特征值、特征向量和变换矩阵：

```python
S_W, S_B = scatter_within(X, y), scatter_between(X, y)
eig_vals, eig_vecs = np.linalg.eig(np.linalg.inv(S_W).dot(S_B))
W = get_components(eig_vals, eig_vecs, n_comp=2)
print('EigVals: %s\n\nEigVecs: %s' % (eig_vals, eig_vecs))
print('\nW: %s' % W)
```

```python
EigVals: [  2.0905e+01 +0.0000e+00j   1.4283e-01 +0.0000e+00j
  -2.8680e-16 +1.9364e-15j  -2.8680e-16 -1.9364e-15j]

EigVecs: [[ 0.2067+0.j      0.0018+0.j      0.4846-0.4436j  0.4846+0.4436j]
 [ 0.4159+0.j     -0.5626+0.j      0.0599+0.1958j  0.0599-0.1958j]
 [-0.5616+0.j      0.2232+0.j      0.1194+0.1929j  0.1194-0.1929j]
 [-0.6848+0.j     -0.7960+0.j     -0.6892+0.j     -0.6892-0.j    ]]

W: [[ 0.2067+0.j  0.0018+0.j]
 [ 0.4159+0.j -0.5626+0.j]
 [-0.5616+0.j  0.2232+0.j]
 [-0.6848+0.j -0.7960+0.j]]
```

```python
X_lda = X.dot(W)
for label,marker,color in zip(
        np.unique(y),('^', 's', 'o'),('blue', 'red', 'green')):
    plt.scatter(X_lda[y==label, 0], X_lda[y==label, 1],
                color=color, marker=marker)
```

```python
/Users/sebastian/miniconda3/lib/python3.5/site-packages/numpy/core/numeric.py:525: ComplexWarning: Casting complex values to real discards the imaginary part
  return array(a, dtype, copy=False, order=order, subok=True)
```

![Linear discriminant analysis](https://sebastianraschka.com/images/blog/2014/linear-discriminant-analysis/2014-08-03-linear_discriminant_analysis_154_1.webp)

接下来，我们对标准化后的花类数据集重复这一过程：

```python
S_W, S_B = scatter_within(X_std, y), scatter_between(X_std, y)
eig_vals, eig_vecs = np.linalg.eig(np.linalg.inv(S_W).dot(S_B))
W_std = get_components(eig_vals, eig_vecs, n_comp=2)
print('EigVals: %s\n\nEigVecs: %s' % (eig_vals, eig_vecs))
print('\nW: %s' % W_std)
```

```python
EigVals: [  2.0905e+01   1.4283e-01  -6.7207e-16   1.1082e-15]

EigVecs: [[ 0.1492 -0.0019  0.8194 -0.3704]
 [ 0.1572  0.3193 -0.1382 -0.0884]
 [-0.8635 -0.5155 -0.5078 -0.5106]
 [-0.4554  0.7952 -0.2271  0.7709]]

W: [[ 0.1492 -0.0019]
 [ 0.1572  0.3193]
 [-0.8635 -0.5155]
 [-0.4554  0.7952]]
```

```python
X_std_lda = X_std.dot(W_std)
X_std_lda[:, 1] = X_std_lda[:, 1]
for label,marker,color in zip(
        np.unique(y),('^', 's', 'o'),('blue', 'red', 'green')):
    plt.scatter(X_std_lda[y==label, 0], X_std_lda[y==label, 1],
                color=color, marker=marker)
```

![Linear discriminant analysis](https://sebastianraschka.com/images/blog/2014/linear-discriminant-analysis/2014-08-03-linear_discriminant_analysis_157_0.webp)

正如我们所看到的，无论数据是否经过缩放，特征值都是完全相同的（注意，由于 \(W\) 的秩为 2，在这个 4 维数据集中，两个最小的特征值实际上应该为 0）。此外，我们还可以看到，投影结果看起来是一样的，只是成分轴的缩放有所不同，而且在这个例子中还发生了镜像。
