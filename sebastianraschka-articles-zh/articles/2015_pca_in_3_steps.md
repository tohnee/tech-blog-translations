---
title: "主成分分析（PCA）"
title_en: "Principal Component Analysis"
source: https://sebastianraschka.com/Articles/2015_pca_in_3_steps.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 主成分分析（PCA）

> 原文：[Principal Component Analysis](https://sebastianraschka.com/Articles/2015_pca_in_3_steps.html) · Sebastian Raschka's Articles

主成分分析（Principal Component Analysis，PCA）是一种简单而又流行、实用的线性变换技术，被应用于众多场景，例如股票市场预测、基因表达数据分析等等。在本教程中，我们将看到 PCA 并不是一个“黑盒”，并会通过 3 个基本步骤来揭开它的内部原理。

本文刚刚经过了一次全面翻新，旧版本仍可在 [principal\_component\_analysis\_old.ipynb](http://nbviewer.ipython.org/github/rasbt/pattern_classification/blob/master/dimensionality_reduction/projection/principal_component_analysis.ipynb) 查看。

---

## 小节

---

## 引言

现代社会数据的庞大规模不仅对计算机硬件构成挑战，也是许多机器学习算法性能的主要瓶颈。PCA 分析的主要目标是识别数据中的模式；PCA 旨在检测变量之间的相关性。只有当变量之间存在强相关性时，尝试降低维度才有意义。简而言之，这就是 PCA 的全部内涵：在高维数据中寻找方差最大的方向，并将数据投影到一个更小维度的子空间中，同时保留大部分信息。

### PCA 与 LDA 的对比

线性判别分析（Linear Discriminant Analysis，LDA）和 PCA 都是线性变换方法。PCA 给出的是使数据方差最大化的方向（主成分），而 LDA 则还致力于寻找使不同类别之间的分离（或判别）最大化的方向，这在模式分类问题中非常有用（PCA 会“忽略”类标签）。
***换句话说，PCA 将整个数据集投影到一个不同的特征（子）空间，而 LDA 则试图确定一个合适的特征（子）空间，以便区分属于不同类别的模式。***

### PCA 与降维

通常，我们期望的目标是通过将一个 \(d\) 维数据集投影到一个 \((k)\) 维子空间（其中 \(k\;<\;d\)）来降低它的维度，从而在保留大部分信息的同时提高计算效率。一个重要的问题是：“\(k\) 取多大才能‘很好地’表示数据？”

稍后，我们将计算数据集的特征向量（即主成分），并把它们收集到一个投影矩阵中。每个特征向量都关联着一个特征值，特征值可以被解释为相应特征向量的“长度”或“大小”。如果某些特征值的量级显著大于其他特征值，那么通过丢弃“信息量较少”的特征对（eigenpair），利用 PCA 将数据集降维到一个更小的子空间就是合理的。

### PCA 方法小结

- 对数据进行标准化。
- 从协方差矩阵或相关矩阵中求得特征向量与特征值，或者执行奇异值分解。
- 将特征值按降序排序，并选择与最大的 \(k\) 个特征值对应的 \(k\) 个特征向量，其中 \(k\) 是新特征子空间的维数（\(k \le d\)）。
- 用选出的 \(k\) 个特征向量构造投影矩阵 \(\mathbf{W}\)。
- 通过 \(\mathbf{W}\) 变换原始数据集 \(\mathbf{X}\)，得到 \(k\) 维特征子空间 \(\mathbf{Y}\)。

## 准备 Iris 数据集

### 关于 Iris 数据集

在接下来的教程中，我们将使用著名的“Iris”（鸢尾花）数据集，它被存放在 UCI 机器学习仓库
（<https://archive.ics.uci.edu/ml/datasets/Iris>）中。

Iris 数据集包含了来自三个不同物种的 150 朵鸢尾花的测量数据。

Iris 数据集中的三个类别是：

1. *Iris-setosa*（山鸢尾，n=50）
2. *Iris-versicolor*（变色鸢尾，n=50）
3. *Iris-virginica*（维吉尼亚鸢尾，n=50）

而 Iris 数据集的四个特征是：

1. *sepal length*（花萼长度），单位 cm
2. *sepal width*（花萼宽度），单位 cm
3. *petal length*（花瓣长度），单位 cm
4. *petal width*（花瓣宽度），单位 cm

![Principal component analysis iris](https://sebastianraschka.com/images/blog/2015/principal_component_analysis_files/iris.webp)

### 加载数据集

为了直接从 UCI 仓库加载 Iris 数据，我们将使用出色的 [pandas](http://pandas.pydata.org) 库。如果你还没有用过 pandas，我强烈建议你去看看 [pandas 教程](http://pandas.pydata.org/pandas-docs/stable/tutorials.html)。如果让我说出一个能让数据处理变得无比简单的 Python 库，那一定非 pandas 莫属！

```python
import pandas as pd

df = pd.read_csv(
    filepath_or_buffer='https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data',
    header=None,
    sep=',')

df.columns=['sepal_len', 'sepal_wid', 'petal_len', 'petal_wid', 'class']
df.dropna(how="all", inplace=True) # drops the empty line at file-end

df.tail()
```

|  | sepal\_len | sepal\_wid | petal\_len | petal\_wid | class |
| --- | --- | --- | --- | --- | --- |
| 145 | 6.7 | 3.0 | 5.2 | 2.3 | Iris-virginica |
| 146 | 6.3 | 2.5 | 5.0 | 1.9 | Iris-virginica |
| 147 | 6.5 | 3.0 | 5.2 | 2.0 | Iris-virginica |
| 148 | 6.2 | 3.4 | 5.4 | 2.3 | Iris-virginica |
| 149 | 5.9 | 3.0 | 5.1 | 1.8 | Iris-virginica |

```python
# split data table into data X and class labels y

X = df.ix[:,0:4].values
y = df.ix[:,4].values
```

现在，我们的 Iris 数据集以一个 \(150 \times 4\) 矩阵的形式存储，其中各列是不同的特征，每一行代表一个独立的花朵样本。
每个样本行 \(\mathbf{x}\) 都可以被视为一个 4 维向量

\[\mathbf{x^T} = \begin{pmatrix} x\_1 \\ x\_2 \\ x\_3 \\ x\_4 \end{pmatrix}
= \begin{pmatrix} \text{sepal length} \\ \text{sepal width} \\\text{petal length} \\ \text{petal width} \end{pmatrix}\]

### 探索性可视化

为了直观感受 3 个不同的花类别在 4 个不同特征上的分布情况，让我们通过直方图将它们可视化。

```python
from matplotlib import pyplot as plt
import numpy as np
import math

label_dict = {1: 'Iris-Setosa',
              2: 'Iris-Versicolor',
              3: 'Iris-Virgnica'}

feature_dict = {0: 'sepal length [cm]',
                1: 'sepal width [cm]',
                2: 'petal length [cm]',
                3: 'petal width [cm]'}

with plt.style.context('seaborn-whitegrid'):
    plt.figure(figsize=(8, 6))
    for cnt in range(4):
        plt.subplot(2, 2, cnt+1)
        for lab in ('Iris-setosa', 'Iris-versicolor', 'Iris-virginica'):
            plt.hist(X[y==lab, cnt],
                     label=lab,
                     bins=10,
                     alpha=0.3,)
        plt.xlabel(feature_dict[cnt])
    plt.legend(loc='upper right', fancybox=True, fontsize=8)

    plt.tight_layout()
    plt.show()
```

![Principal component analysis](https://sebastianraschka.com/images/blog/2015/principal_component_analysis_files/2015-01-17-principal_component_analysis_34_0.webp)

### 标准化

在对协方差矩阵执行 PCA 之前是否要对数据进行标准化，取决于原始特征的测量尺度。由于 PCA 得到的特征子空间会最大化各条轴上的方差，因此对数据进行标准化是有道理的，尤其是当数据是在不同尺度上测量的时候。尽管 Iris 数据集的所有特征都是以厘米为单位测得的，我们还是继续把数据变换到单位尺度（均值 = 0、方差 = 1）——这也是许多机器学习算法获得最佳性能的必要条件。

```python
from sklearn.preprocessing import StandardScaler
X_std = StandardScaler().fit_transform(X)
```

## 1 - 特征分解——计算特征向量与特征值

协方差（或相关）矩阵的特征向量与特征值构成了 PCA 的“核心”：特征向量（主成分）决定了新特征空间的方向，而特征值决定了它们的大小。换句话说，特征值解释了数据沿新特征轴的方差。

### 协方差矩阵

PCA 的经典做法是对协方差矩阵 \(\Sigma\) 执行特征分解。协方差矩阵是一个 \(d \times d\) 矩阵，其中每个元素表示两个特征之间的协方差。两个特征之间的协方差按如下方式计算：

\[\sigma\_{jk} = \frac{1}{n-1}\sum\_{i=1}^{n}\left( x\_{ij}-\bar{x}\_j \right) \left( x\_{ik}-\bar{x}\_k \right).\]

我们可以用下面的矩阵等式来概括协方差矩阵的计算：
\(\Sigma = \frac{1}{n-1} \left( (\mathbf{X} - \mathbf{\bar{x}})^T\;(\mathbf{X} - \mathbf{\bar{x}}) \right)\)
其中 \(\mathbf{\bar{x}}\) 是均值向量
\(\mathbf{\bar{x}} = \frac{1}{n} \sum\limits\_{i=1}^n x\_{i}.\)
均值向量是一个 \(d\) 维向量，向量中的每个值代表数据集中某一特征列的样本均值。

```python
import numpy as np
mean_vec = np.mean(X_std, axis=0)
cov_mat = (X_std - mean_vec).T.dot((X_std - mean_vec)) / (X_std.shape[0]-1)
print('Covariance matrix \n%s' %cov_mat)
```

```python
Covariance matrix
[[ 1.00671141 -0.11010327  0.87760486  0.82344326]
 [-0.11010327  1.00671141 -0.42333835 -0.358937  ]
 [ 0.87760486 -0.42333835  1.00671141  0.96921855]
 [ 0.82344326 -0.358937    0.96921855  1.00671141]]
```

上面这种较为繁琐的写法仅仅是为了演示；等价地，我们也可以直接使用 numpy 的 `cov` 函数：

```python
print('NumPy covariance matrix: \n%s' %np.cov(X_std.T))
```

```python
NumPy covariance matrix:
[[ 1.00671141 -0.11010327  0.87760486  0.82344326]
 [-0.11010327  1.00671141 -0.42333835 -0.358937  ]
 [ 0.87760486 -0.42333835  1.00671141  0.96921855]
 [ 0.82344326 -0.358937    0.96921855  1.00671141]]
```

接下来，我们对协方差矩阵执行特征分解：

```python
cov_mat = np.cov(X_std.T)

eig_vals, eig_vecs = np.linalg.eig(cov_mat)

print('Eigenvectors \n%s' %eig_vecs)
print('\nEigenvalues \n%s' %eig_vals)
```

```python
Eigenvectors
[[ 0.52237162 -0.37231836 -0.72101681  0.26199559]
 [-0.26335492 -0.92555649  0.24203288 -0.12413481]
 [ 0.58125401 -0.02109478  0.14089226 -0.80115427]
 [ 0.56561105 -0.06541577  0.6338014   0.52354627]]

Eigenvalues
[ 2.93035378  0.92740362  0.14834223  0.02074601]
```

### 相关矩阵

尤其是在“金融”领域，人们通常用相关矩阵来代替协方差矩阵。不过，对协方差矩阵（在输入数据已标准化的前提下）做特征分解，与对相关矩阵做特征分解会得到相同的结果，因为相关矩阵可以理解为归一化的协方差矩阵。

基于相关矩阵对标准化后的数据进行特征分解：

```python
cor_mat1 = np.corrcoef(X_std.T)

eig_vals, eig_vecs = np.linalg.eig(cor_mat1)

print('Eigenvectors \n%s' %eig_vecs)
print('\nEigenvalues \n%s' %eig_vals)
```

```python
Eigenvectors
[[ 0.52237162 -0.37231836 -0.72101681  0.26199559]
 [-0.26335492 -0.92555649  0.24203288 -0.12413481]
 [ 0.58125401 -0.02109478  0.14089226 -0.80115427]
 [ 0.56561105 -0.06541577  0.6338014   0.52354627]]

Eigenvalues
[ 2.91081808  0.92122093  0.14735328  0.02060771]
```

基于相关矩阵对原始数据进行特征分解：

```python
cor_mat2 = np.corrcoef(X.T)

eig_vals, eig_vecs = np.linalg.eig(cor_mat2)

print('Eigenvectors \n%s' %eig_vecs)
print('\nEigenvalues \n%s' %eig_vals)
```

```python
Eigenvectors
[[ 0.52237162 -0.37231836 -0.72101681  0.26199559]
 [-0.26335492 -0.92555649  0.24203288 -0.12413481]
 [ 0.58125401 -0.02109478  0.14089226 -0.80115427]
 [ 0.56561105 -0.06541577  0.6338014   0.52354627]]

Eigenvalues
[ 2.91081808  0.92122093  0.14735328  0.02060771]
```

我们可以清楚地看到，这三种做法得到了相同的特征向量与特征值对：

- 对数据标准化之后，再对协方差矩阵做特征分解。
- 对相关矩阵做特征分解。
- 对数据标准化之后，再对相关矩阵做特征分解。

### 奇异值分解

虽然对协方差矩阵或相关矩阵做特征分解可能更直观，但大多数 PCA 实现为了提高计算效率会执行奇异值分解（Singular Value Decomposition，SVD）。所以，让我们执行一次 SVD，来确认结果确实相同：

```python
u,s,v = np.linalg.svd(X_std.T)
u
```

```python
array([[-0.52237162, -0.37231836,  0.72101681,  0.26199559],
       [ 0.26335492, -0.92555649, -0.24203288, -0.12413481],
       [-0.58125401, -0.02109478, -0.14089226, -0.80115427],
       [-0.56561105, -0.06541577, -0.6338014 ,  0.52354627]])
```

## 2 - 选择主成分

### 对特征对排序

PCA 的典型目标是通过把原始特征空间投影到一个更小的子空间来降低其维度，特征向量将构成这个子空间的各条轴。不过，特征向量只定义了新轴的方向，因为它们的单位长度都是相同的 1，这一点可以通过下面两行代码加以确认：

```python
for ev in eig_vecs.T:
    np.testing.assert_array_almost_equal(1.0, np.linalg.norm(ev))
print('Everything ok!')
```

```python
Everything ok!
```

为了决定在构建低维子空间时可以丢弃哪些特征向量而不损失太多信息，我们需要考察相应的特征值：特征值最小的特征向量所承载的关于数据分布的信息最少，它们就是可以被丢弃的那部分。
为此，常见的做法是将特征值从高到低排序，从而选出前 \(k\) 个特征向量。

```python
# Make a list of (eigenvalue, eigenvector) tuples
eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:,i]) for i in range(len(eig_vals))]

# Sort the (eigenvalue, eigenvector) tuples from high to low
eig_pairs.sort(key=lambda x: x[0], reverse=True)

# Visually confirm that the list is correctly sorted by decreasing eigenvalues
print('Eigenvalues in descending order:')
for i in eig_pairs:
    print(i[0])
```

```python
Eigenvalues in descending order:
2.91081808375
0.921220930707
0.147353278305
0.0206077072356
```

### 解释方差

对特征对排序之后，下一个问题是：“我们要为新特征子空间选择多少个主成分？”一个有用的度量是所谓的“解释方差”（explained variance），它可以由特征值计算得到。解释方差告诉我们，每个主成分分别承载了多少信息（方差）。

```python
tot = sum(eig_vals)
var_exp = [(i / tot)*100 for i in sorted(eig_vals, reverse=True)]
cum_var_exp = np.cumsum(var_exp)
```

```python
with plt.style.context('seaborn-whitegrid'):
    plt.figure(figsize=(6, 4))

    plt.bar(range(4), var_exp, alpha=0.5, align='center',
            label='individual explained variance')
    plt.step(range(4), cum_var_exp, where='mid',
             label='cumulative explained variance')
    plt.ylabel('Explained variance ratio')
    plt.xlabel('Principal components')
    plt.legend(loc='best')
    plt.tight_layout()
```

![Principal component analysis](https://sebastianraschka.com/images/blog/2015/principal_component_analysis_files/2015-01-17-principal_component_analysis_79_0.webp)

上图清楚地表明，大部分方差（准确地说是 72.77% 的方差）仅凭第一个主成分就能解释。第二个主成分仍然承载了一些信息（23.03%），而第三个和第四个主成分则可以放心地丢弃，不会损失太多信息。前两个主成分合计包含了 95.8% 的信息。

### 投影矩阵

现在是时候进入真正有趣的部分了：构造用于将 Iris 数据变换到新特征子空间的投影矩阵。尽管“投影矩阵”这个名字听起来颇为高大上，它其实只是由我们拼接起来的前 *k* 个特征向量组成的矩阵。

在这里，我们通过选择特征值最高的“前 2 个”特征向量来构造 \(d \times k\) 维特征向量矩阵 \(\mathbf{W}\)，从而把 4 维特征空间降到 2 维特征子空间。

```python
matrix_w = np.hstack((eig_pairs[0][1].reshape(4,1),
                      eig_pairs[1][1].reshape(4,1)))

print('Matrix W:\n', matrix_w)
```

```python
Matrix W:
 [[ 0.52237162 -0.37231836]
 [-0.26335492 -0.92555649]
 [ 0.58125401 -0.02109478]
 [ 0.56561105 -0.06541577]]
```

## 3 - 投影到新特征空间

在最后这一步中，我们将使用 \(4 \times 2\) 维投影矩阵 \(\mathbf{W}\)，通过等式
\(\mathbf{Y} = \mathbf{X} \times \mathbf{W}\) 把样本变换到新子空间上，其中 \(\mathbf{Y}\) 是一个 \(150\times 2\) 矩阵，由变换后的样本组成。

```python
Y = X_std.dot(matrix_w)
```

```python
with plt.style.context('seaborn-whitegrid'):
    plt.figure(figsize=(6, 4))
    for lab, col in zip(('Iris-setosa', 'Iris-versicolor', 'Iris-virginica'),
                        ('blue', 'red', 'green')):
        plt.scatter(Y[y==lab, 0],
                    Y[y==lab, 1],
                    label=lab,
                    c=col)
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.legend(loc='lower center')
    plt.tight_layout()
    plt.show()
```

![Principal component analysis](https://sebastianraschka.com/images/blog/2015/principal_component_analysis_files/2015-01-17-principal_component_analysis_89_0.webp)

现在，经过线性 PCA 变换之后，我们得到的是一个更低维的子空间（本例中是从三维到二维），样本沿新的特征轴“分散得最开”。

## 捷径——用 scikit-learn 做 PCA

出于教学目的，我们绕了很远的路才对 Iris 数据集应用了 PCA。不过幸运的是，scikit-learn 中已经有现成的实现。

```python
from sklearn.decomposition import PCA as sklearnPCA
sklearn_pca = sklearnPCA(n_components=2)
Y_sklearn = sklearn_pca.fit_transform(X_std)
```

```python
with plt.style.context('seaborn-whitegrid'):
    plt.figure(figsize=(6, 4))
    for lab, col in zip(('Iris-setosa', 'Iris-versicolor', 'Iris-virginica'),
                        ('blue', 'red', 'green')):
        plt.scatter(Y_sklearn[y==lab, 0],
                    Y_sklearn[y==lab, 1],
                    label=lab,
                    c=col)
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.legend(loc='lower center')
    plt.tight_layout()
    plt.show()
```

![Principal component analysis](https://sebastianraschka.com/images/blog/2015/principal_component_analysis_files/2015-01-17-principal_component_analysis_95_0.webp)
