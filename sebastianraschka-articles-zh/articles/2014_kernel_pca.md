---
title: "RBF 核 PCA 与核技巧"
title_en: "RBF Kernel PCA and Kernel Tricks"
source: https://sebastianraschka.com/Articles/2014_kernel_pca.html
crawled: 2026-09-06
translated: 2026-09-14
---

# RBF 核 PCA 与核技巧

> 原文：[RBF Kernel PCA and Kernel Tricks](https://sebastianraschka.com/Articles/2014_kernel_pca.html) · Sebastian Raschka's Articles

## 章节

**大多数机器学习算法都是针对线性可分的数据开发并经过统计验证的。典型的例子包括支持向量机（SVM）这类线性分类器，以及用于降维的（标准）主成分分析（Principal Component Analysis，PCA）。然而，大多数现实世界中的数据需要借助非线性方法，才能成功地完成那些涉及分析与发现模式的任务。**

**本文的重点在于简要介绍核方法（kernel methods）的思想，并实现一个高斯径向基函数（Radial Basis Function，RBF）核，利用 RBF 核主成分分析（kernel PCA，kPCA）来执行非线性降维。**

## 主成分分析

主成分分析（PCA）的主要目的是对数据进行分析，以找出能够「很好地」表示数据的模式。主成分可以被理解为数据集的新坐标轴，它们使沿这些轴方向的方差最大化（即协方差矩阵的特征向量）。换句话说，PCA 的目标是找到方差最大的轴，数据在这些轴的方向上散布得最开。

![Kernel pca pca 1](https://sebastianraschka.com/images/blog/2014/kernel_pca/pca_1.webp)

## PCA 与线性降维

PCA 的一个常见应用是在尽量不损失信息的前提下降低数据集的维度。此时，整个数据集（*d* 维）会被投影到一个新的子空间（*k* 维，且 *k* < *d*）上。这种投影方法有助于降低计算成本以及参数估计的误差（「维数灾难」）。

标准 PCA 方法可以概括为六个简单的步骤：

![Kernel pca pca 2](https://sebastianraschka.com/images/blog/2014/kernel_pca/pca_2.webp)

更多细节可以在我之前写的文章[《Implementing a Principal Component Analysis (PCA) in Python step by step》（在 Python 中一步步实现主成分分析）](https://sebastianraschka.com/Articles/2014_pca_step_by_step.html)中找到。

## 非线性降维

上面描述的「经典」PCA 方法是一种线性投影技术，在数据线性可分时效果很好。然而，对于线性不可分的数据，如果任务是对数据集进行降维，就需要使用非线性技术。

![Kernel pca linear vs nonlinear](https://sebastianraschka.com/images/blog/2014/kernel_pca/linear_vs_nonlinear.webp)

## 核函数与核技巧

处理线性不可分数据的基本思路，是把它投影到一个更高维的空间中，使其在那个空间里变得线性可分。我们把这个非线性映射函数记作 \(\phi\)，于是样本 \(\mathbf{x}\) 的映射可以写成 \(\mathbf{x} \rightarrow \phi (\mathbf{x})\)，这被称为「核函数」。

而「核」（kernel）这个术语指的是这样一个函数：它计算样本 \(\mathbf{x}\) 在 \(\phi\) 之下的像之间的点积。

\[\begin{equation}\kappa(\mathbf{x\_i, x\_j}) = \phi (\mathbf{x\_i}) \phi (\mathbf{x\_j})^T \end{equation}\]

关于这个公式推导的更多细节，可以参见 Quan Wang 所写的一篇非常出色的综述文章：[Kernel Principal Component Analysis and its Applications in Face Recognition and Active Shape Models](http://arxiv.org/abs/1207.3538)。[[1](#References)]

换句话说，函数 \(\phi\) 通过构造原始特征的非线性组合，把原始的 d 维特征映射到一个更大的 k 维特征空间中。例如，假设 \(\mathbf{x}\) 由 2 个特征组成：

\[\mathbf{x} = \big[x\_1 \quad x\_2\big]^T \quad \quad \mathbf{x} \in I\!R^d\]
\[\Downarrow \phi\]
\[\mathbf{x}' = \big[x\_1 \quad x\_2 \quad x\_1 x\_2 \quad x\_{1}^2 \quad x\_1 x\_{2}^3 \quad \dots \big]^T \quad \quad \mathbf{x} \in I\!R^k (k >> d)\]

RBF 核的数学定义通常写成如下形式并按此实现：

\begin{equation} \kappa(\mathbf{x\_i, x\_j}) = exp\bigg(- \gamma \; \lVert\mathbf{x\_i - x\_j }\rVert^{2}\_{2} \bigg)\end{equation}

其中 \(\textstyle\gamma = \tfrac{1}{2\sigma^2}\) 是一个需要优化的自由参数。

## 高斯径向基函数（RBF）核 PCA

在线性 PCA 方法中，我们关心的是使数据集方差最大化的主成分。具体做法是基于协方差矩阵，提取与最大特征值相对应的特征向量（主成分）：

\begin{equation}\text{Cov} = \frac{1}{N} \sum\_{i=1}^{N} \mathbf{x\_i} \mathbf{x\_i}^T \end{equation}

Bernhard Scholkopf（[Kernel Principal Component Analysis](http://dl.acm.org/citation.cfm?id=299113) [[2](#References)]）将这一方法推广到了通过核函数映射到更高维空间的数据上：

\begin{equation}\text{Cov} = \frac{1}{N} \sum\_{i=1}^{N} \phi(\mathbf{x\_i}) \phi(\mathbf{x\_i})^T \end{equation}

然而在实践中，我们并不会显式地计算高维空间中的协方差矩阵（核技巧，kernel trick）。因此，RBF 核 PCA 的实现得到的并不是主成分坐标轴（这一点与标准 PCA 不同），不过所得到的特征向量可以理解为数据在各个主成分上的投影。

## 逐步实现 RBF 核 PCA

要实现 RBF 核 PCA，我们只需要考虑以下两个步骤。

### 1. 计算核（相似度）矩阵。

在第一步中，我们需要对每一对点计算

\begin{equation} \kappa(\mathbf{x\_i, x\_j}) = exp\bigg(- \gamma \; \lVert\mathbf{x\_i - x\_j }\rVert^{2}\_{2} \bigg)\end{equation}

例如，如果我们有一个包含 100 个样本的数据集，这一步将得到一个对称的 100×100 核矩阵。

### 2. 核矩阵的特征值分解。

由于无法保证核矩阵是中心化的，我们可以应用下面的公式来完成中心化：

\begin{equation} K’ = K - \mathbf{1\_N} K - K \mathbf{1\_N} + \mathbf{1\_N} K \mathbf{1\_N} \end{equation}

其中 \(\mathbf{1\_N}\) 是一个（与核矩阵同样大小的）\(N\times N\) 矩阵，所有元素都等于 \(\frac{1}{N}\)。[[3](#References)]

接下来，我们要获得中心化后的核矩阵中与最大特征值相对应的特征向量。这些特征向量就是已经投影到相应主成分上的数据点。

下面，我们用 Python 来实现这些步骤，看看这些计算是如何工作的。

```python
from scipy.spatial.distance import pdist, squareform
from scipy import exp
from scipy.linalg import eigh
import numpy as np

def stepwise_kpca(X, gamma, n_components):
    """
    Implementation of a RBF kernel PCA.

    Arguments:
        X: A MxN dataset as NumPy array where the samples are stored as rows (M),
           and the attributes defined as columns (N).
        gamma: A free parameter (coefficient) for the RBF kernel.
        n_components: The number of components to be returned.

    """
    # Calculating the squared Euclidean distances for every pair of points
    # in the MxN dimensional dataset.
    sq_dists = pdist(X, 'sqeuclidean')

    # Converting the pairwise distances into a symmetric MxM matrix.
    mat_sq_dists = squareform(sq_dists)

    # Computing the MxM kernel matrix.
    K = exp(-gamma * mat_sq_dists)

    # Centering the symmetric NxN kernel matrix.
    N = K.shape[0]
    one_n = np.ones((N,N)) / N
    K = K - one_n.dot(K) - K.dot(one_n) + one_n.dot(K).dot(one_n)

    # Obtaining eigenvalues in descending order with corresponding
    # eigenvectors from the symmetric matrix.
    eigvals, eigvecs = eigh(K)

    # Obtaining the i eigenvectors that corresponds to the i highest eigenvalues.
    X_pc = np.column_stack((eigvecs[:,-i] for i in range(1,n_components+1)))

    return X_pc
```

## RBF 核 PCA 实例

在本节中，我们将把 RBF 核 PCA 应用于几种不同的非线性样本数据，以执行降维。

### 半月形数据

我们先从一个简单的例子开始：使用 [scikit-learn](http://scikit-learn.org/stable/index.html) 的 [`make_moons`](http://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_moons.html) 函数生成两个半月形。

```python
%matplotlib inline
```

```python
import matplotlib.pyplot as plt

from sklearn.datasets import make_moons
X, y = make_moons(n_samples=100, random_state=123)

plt.figure(figsize=(8,6))

plt.scatter(X[y==0, 0], X[y==0, 1], color='red', alpha=0.5)
plt.scatter(X[y==1, 0], X[y==1, 1], color='blue', alpha=0.5)

plt.title('A nonlinear 2Ddataset')
plt.ylabel('y coordinate')
plt.xlabel('x coordinate')

plt.show()
```

```python
/Users/sebastian/miniconda3/envs/py34/lib/python3.4/site-packages/sklearn/datasets/samples_generator.py:612: DeprecationWarning: using a non-integer number instead of an integer will result in an error in the future
  y = np.hstack([np.zeros(n_samples_in, dtype=np.intp),
```

![Kernel pca 2014 09 14 kernel pca 47 1](https://sebastianraschka.com/images/blog/2014/kernel_pca/2014-09-14-kernel_pca_47_1.webp)

#### 线性 PCA

由于这两个半月形是线性不可分的，我们预计「经典」PCA 无法在 1 维空间中给出数据的「良好」表示。这里，我们将使用 scikit-learn 中实现的 [`PCA`](http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html) 类来执行降维。

```python
from sklearn.decomposition import PCA

scikit_pca = PCA(n_components=2)
X_spca = scikit_pca.fit_transform(X)

plt.figure(figsize=(8,6))
plt.scatter(X_spca[y==0, 0], X_spca[y==0, 1], color='red', alpha=0.5)
plt.scatter(X_spca[y==1, 0], X_spca[y==1, 1], color='blue', alpha=0.5)

plt.title('First 2 principal components after Linear PCA')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()
```

![Kernel pca 2014 09 14 kernel pca 52 0](https://sebastianraschka.com/images/blog/2014/kernel_pca/2014-09-14-kernel_pca_52_0.webp)

```python
import numpy as np
scikit_pca = PCA(n_components=1)
X_spca = scikit_pca.fit_transform(X)

plt.figure(figsize=(8,6))
plt.scatter(X_spca[y==0, 0], np.zeros((50,1)), color='red', alpha=0.5)
plt.scatter(X_spca[y==1, 0], np.zeros((50,1)), color='blue', alpha=0.5)

plt.title('First principal component after Linear PCA')
plt.xlabel('PC1')

plt.show()
```

![Kernel pca 2014 09 14 kernel pca 53 0](https://sebastianraschka.com/images/blog/2014/kernel_pca/2014-09-14-kernel_pca_53_0.webp)

正如我们所见，所得到的主成分并没有产生一个数据能被很好线性分开的子空间。请注意，PCA 是一种无监督方法，与[线性判别分析](https://sebastianraschka.com/Articles/2014_python_lda.html)不同，它不会为了最大化方差而「考虑」类别标签。这里的蓝色和红色只是为了可视化目的而添加的，用以指示分离的程度。

#### 高斯 RBF 核 PCA

接下来，我们对半月形数据执行 RBF 核 PCA 降维。\(\gamma\) 的选择取决于数据集，可以通过网格搜索（Grid Search）这类超参数调优技术来获得。超参数调优本身就是一个很宽泛的话题，这里我就直接使用一个我发现的能产生「良好」结果的 \(\gamma\) 值。

```python
X_pc = stepwise_kpca(X, gamma=15, n_components=2)

plt.figure(figsize=(8,6))
plt.scatter(X_pc[y==0, 0], X_pc[y==0, 1], color='red', alpha=0.5)
plt.scatter(X_pc[y==1, 0], X_pc[y==1, 1], color='blue', alpha=0.5)

plt.title('First 2 principal components after RBF Kernel PCA')
plt.text(-0.18, 0.18, 'gamma = 15', fontsize=12)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()
```

![Kernel pca 2014 09 14 kernel pca 59 0](https://sebastianraschka.com/images/blog/2014/kernel_pca/2014-09-14-kernel_pca_59_0.webp)

```python
plt.figure(figsize=(8,6))
plt.scatter(X_pc[y==0, 0], np.zeros((50)), color='red', alpha=0.5)
plt.scatter(X_pc[y==1, 0], np.zeros((50)), color='blue', alpha=0.5)

plt.title('First principal component after RBF Kernel PCA')
plt.text(-0.17, 0.007, 'gamma = 15', fontsize=12)
plt.xlabel('PC1')
plt.show()
```

![Kernel pca 2014 09 14 kernel pca 60 0](https://sebastianraschka.com/images/blog/2014/kernel_pca/2014-09-14-kernel_pca_60_0.webp)

我们可以清楚地看到，通过 RBF 核 PCA 进行的投影得到了一个类别分离良好的子空间。这样的子空间随后可以作为线性分类模型（例如支持向量机或朴素贝叶斯分类器）的输入，这些模型将在后续文章中介绍。

#### scikit 的 RBF 核 PCA

为了方便起见，scikit-learn 中已经有现成的 [`KernelPCA`](http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.KernelPCA.html) 实现。让我们来确认一下我们的实现结果与 scikit-learn 的方法是一致的。

```python
from sklearn.decomposition import KernelPCA

scikit_kpca = KernelPCA(n_components=2, kernel='rbf', gamma=15)
X_skernpca = scikit_kpca.fit_transform(X)

plt.figure(figsize=(8,6))
plt.scatter(X_skernpca[y==0, 0], X_skernpca[y==0, 1], color='red', alpha=0.5)
plt.scatter(X_skernpca[y==1, 0], X_skernpca[y==1, 1], color='blue', alpha=0.5)

plt.text(-0.48, 0.35, 'gamma = 15', fontsize=12)
plt.title('First 2 principal components after RBF Kernel PCA via scikit-learn')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()
```

![Kernel pca 2014 09 14 kernel pca 66 0](https://sebastianraschka.com/images/blog/2014/kernel_pca/2014-09-14-kernel_pca_66_0.webp)

```python
scikit_kpca = KernelPCA(n_components=1, kernel='rbf', gamma=15)
X_skernpca = scikit_kpca.fit_transform(X)

plt.figure(figsize=(8,6))
plt.scatter(X_skernpca[y==0, 0], np.zeros((50,1)), color='red', alpha=0.5)
plt.scatter(X_skernpca[y==1, 0], np.zeros((50,1)), color='blue', alpha=0.5)
plt.text(-0.48, 0.007, 'gamma = 15', fontsize=12)
plt.title('First principal component after RBF Kernel PCA')
plt.xlabel('PC1')
plt.show()
```

![Kernel pca 2014 09 14 kernel pca 67 0](https://sebastianraschka.com/images/blog/2014/kernel_pca/2014-09-14-kernel_pca_67_0.webp)

### 同心圆

在下一个例子中，我们来看一个经典案例：由 scikit-learn 的 [`make_circles`](http://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_circles.html) 生成的带随机噪声的两个同心圆。

```python
from sklearn.datasets import make_circles

X, y = make_circles(n_samples=1000, random_state=123, noise=0.1, factor=0.2)

plt.figure(figsize=(8,6))

plt.scatter(X[y==0, 0], X[y==0, 1], color='red', alpha=0.5)
plt.scatter(X[y==1, 0], X[y==1, 1], color='blue', alpha=0.5)
plt.title('Concentric circles')
plt.ylabel('y coordinate')
plt.xlabel('x coordinate')
plt.show()
```

![Kernel pca 2014 09 14 kernel pca 72 0](https://sebastianraschka.com/images/blog/2014/kernel_pca/2014-09-14-kernel_pca_72_0.webp)

#### 线性 PCA

```python
scikit_pca = PCA(n_components=2)
X_spca = scikit_pca.fit_transform(X)

plt.figure(figsize=(8,6))
plt.scatter(X[y==0, 0], np.zeros((500,1))+0.1, color='red', alpha=0.5)
plt.scatter(X[y==1, 0], np.zeros((500,1))-0.1, color='blue', alpha=0.5)
plt.ylim([-15,15])
plt.text(-0.125, 12.5, 'gamma = 15', fontsize=12)
plt.title('First principal component after Linear PCA')
plt.xlabel('PC1')
plt.show()
```

![Kernel pca 2014 09 14 kernel pca 76 0](https://sebastianraschka.com/images/blog/2014/kernel_pca/2014-09-14-kernel_pca_76_0.webp)

同样，线性 PCA 方法得到的结果并没有产生一个两个类别能被很好线性分开的子空间。

#### 高斯 RBF 核 PCA

```python
X_pc = stepwise_kpca(X, gamma=15, n_components=1)

plt.figure(figsize=(8,6))
plt.scatter(X_pc[y==0, 0], np.zeros((500,1)), color='red', alpha=0.5)
plt.scatter(X_pc[y==1, 0], np.zeros((500,1)), color='blue', alpha=0.5)
plt.text(-0.05, 0.007, 'gamma = 15', fontsize=12)
plt.title('First principal component after RBF Kernel PCA')
plt.xlabel('PC1')
plt.show()
```

![Kernel pca 2014 09 14 kernel pca 81 0](https://sebastianraschka.com/images/blog/2014/kernel_pca/2014-09-14-kernel_pca_81_0.webp)

而这一次，通过高斯 RBF 核 PCA 得到的这个 1 维子空间，就线性类别分离而言看起来要好得多。

### 瑞士卷

展开著名的「瑞士卷」（Swiss roll）比我们前面看到的例子更具挑战性。我们将使用 [`make_swiss_roll`](http://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_swiss_roll.html) 来创建三维瑞士卷，并先用线性 PCA 将数据集投影到 2 维和 1 维特征子空间上。

```python
from sklearn.datasets.samples_generator import make_swiss_roll
from mpl_toolkits.mplot3d import Axes3D

X, color = make_swiss_roll(n_samples=800, random_state=123)

fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=color, cmap=plt.cm.rainbow)
plt.title('Swiss Roll in 3D')
plt.show()
```

![Kernel pca 2014 09 14 kernel pca 87 0](https://sebastianraschka.com/images/blog/2014/kernel_pca/2014-09-14-kernel_pca_87_0.webp)

#### 线性 PCA

```python
from sklearn.decomposition import PCA

scikit_pca = PCA(n_components=2)
X_spca = scikit_pca.fit_transform(X)

plt.figure(figsize=(8,6))
plt.scatter(X_spca[:, 0], X_spca[:, 1], c=color, cmap=plt.cm.rainbow)

plt.title('First 2 principal components after Linear PCA')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()
```

![Kernel pca 2014 09 14 kernel pca 91 0](https://sebastianraschka.com/images/blog/2014/kernel_pca/2014-09-14-kernel_pca_91_0.webp)

```python
scikit_pca = PCA(n_components=1)
X_spca = scikit_pca.fit_transform(X)

plt.figure(figsize=(8,6))
plt.scatter(X_spca, np.zeros((800,1)), c=color, cmap=plt.cm.rainbow)
plt.title('First principal component after Linear PCA')
plt.xlabel('PC1')
plt.show()
```

![Kernel pca 2014 09 14 kernel pca 92 0](https://sebastianraschka.com/images/blog/2014/kernel_pca/2014-09-14-kernel_pca_92_0.webp)

#### 高斯 RBF 核 PCA

对于这个数据集，我还没有找到一个能让高斯 RBF 核实现良好线性分离的 \(\gamma\) 参数。我得到的最好结果如下图所示。

```python
X_pc = stepwise_kpca(X, gamma=0.1, n_components=2)

plt.figure(figsize=(8,6))
plt.scatter(X_pc[:, 0], X_pc[:, 1], c=color, cmap=plt.cm.rainbow)

plt.title('First 2 principal components after RBF Kernel PCA')
plt.text(-0.14, 0.14, 'gamma = 0.1', fontsize=12)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()
```

![Kernel pca 2014 09 14 kernel pca 97 0](https://sebastianraschka.com/images/blog/2014/kernel_pca/2014-09-14-kernel_pca_97_0.webp)

```python
plt.figure(figsize=(8,6))
plt.scatter(X_pc[:,0], np.zeros((800,1)), c=color, cmap=plt.cm.rainbow)

plt.text(-0.125, 0.007, 'gamma = 0.1', fontsize=12)
plt.title('First principal component after RBF Kernel PCA')
plt.xlabel('PC1')
plt.show()
```

![Kernel pca 2014 09 14 kernel pca 98 0](https://sebastianraschka.com/images/blog/2014/kernel_pca/2014-09-14-kernel_pca_98_0.webp)

#### 局部线性嵌入（LLE）

2000 年，Sam T. Roweis 和 Lawrence K. Saul（[Nonlinear dimensionality reduction by locally linear embedding](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.111.3313) [[4](#References)]）提出了一种称为局部线性嵌入（locally linear embedding，LLE）的无监督学习算法，它更适合识别高维特征空间中的模式，并且解决了我们对瑞士卷进行非线性降维的问题。这里，我们将使用 scikit-learn 的 [`locally_linear_embedding`](http://scikit-learn.org/stable/modules/generated/sklearn.manifold.locally_linear_embedding.html) 类来「展开」瑞士卷。

```python
from sklearn.manifold import locally_linear_embedding

X_lle, err = locally_linear_embedding(X, n_neighbors=12, n_components=2)

plt.figure(figsize=(8,6))
plt.scatter(X_lle[:, 0], X_lle[:, 1], c=color, cmap=plt.cm.rainbow)

plt.title('First 2 principal components after Locally Linear Embedding')
plt.show()
```

![Kernel pca 2014 09 14 kernel pca 103 0](https://sebastianraschka.com/images/blog/2014/kernel_pca/2014-09-14-kernel_pca_103_0.webp)

```python
from sklearn.manifold import locally_linear_embedding

X_lle, err = locally_linear_embedding(X, n_neighbors=12, n_components=1)

plt.figure(figsize=(8,6))
plt.scatter(X_lle, np.zeros((800,1)), c=color, cmap=plt.cm.rainbow)

plt.title('First principal component after Locally Linear Embedding')
plt.show()
```

![Kernel pca 2014 09 14 kernel pca 104 0](https://sebastianraschka.com/images/blog/2014/kernel_pca/2014-09-14-kernel_pca_104_0.webp)

## 附录 A：投影新数据

到目前为止一切顺利：在上面的章节中，我们一直在把一个数据集投影到新的特征子空间上。然而，在实际应用中，我们通常更关心的是把新的数据点映射到同一个新的特征子空间（例如，在模式分类任务中同时使用训练集和测试集时）。

还记得吗：当我们计算中心化核矩阵的特征向量 \( \mathbf{\alpha} \) 时，这些值实际上已经是数据点在主成分轴 \( \mathbf{g} \) 上的投影。

如果我们想把一个新的数据点 \( \mathbf{x} \) 投影到这条主成分轴上，就需要计算 \(\phi(\mathbf{x})^T \mathbf{g} \)。

幸运的是，在这里我们同样不必显式地计算 \(\phi(\mathbf{x})^T \mathbf{g} \)，而是可以使用核技巧来计算新数据点与训练集中每个数据点 \( j \) 之间的 RBF 核：

\[\phi(\mathbf{x})^T \mathbf{g} = \sum\_j \alpha\_{i} \; \phi(\mathbf{x}) \; \phi(\mathbf{x\_j})^T\]
\[= \sum\_j \alpha\_{i} \; \kappa(\mathbf{x}, \mathbf{x\_j})\]

而由于核矩阵 \(\mathbf{K}\) 的特征向量 \( \alpha \) 和特征值 \( \lambda \) 满足方程
\(\mathbf{K} \alpha = \lambda \alpha \)，我们只需要用相应的特征值对特征向量做归一化即可。

首先，让我们修改一下原先的实现，让它把核矩阵的特征值也一并返回。

```python
from scipy.spatial.distance import pdist, squareform
from scipy import exp
from scipy.linalg import eigh
import numpy as np

def stepwise_kpca(X, gamma, n_components):
    """
    Implementation of a RBF kernel PCA.

    Arguments:
        X: A MxN dataset as NumPy array where the samples are stored as rows (M),
           and the attributes defined as columns (N).
        gamma: A free parameter (coefficient) for the RBF kernel.
        n_components: The number of components to be returned.

    Returns the k eigenvectors (alphas) that correspond to the k largest
        eigenvalues (lambdas).

    """
    # Calculating the squared Euclidean distances for every pair of points
    # in the MxN dimensional dataset.
    sq_dists = pdist(X, 'sqeuclidean')

    # Converting the pairwise distances into a symmetric MxM matrix.
    mat_sq_dists = squareform(sq_dists)

    # Computing the MxM kernel matrix.
    K = exp(-gamma * mat_sq_dists)

    # Centering the symmetric NxN kernel matrix.
    N = K.shape[0]
    one_n = np.ones((N,N)) / N
    K_norm = K - one_n.dot(K) - K.dot(one_n) + one_n.dot(K).dot(one_n)

    # Obtaining eigenvalues in descending order with corresponding
    # eigenvectors from the symmetric matrix.
    eigvals, eigvecs = eigh(K_norm)

    # Obtaining the i eigenvectors (alphas) that corresponds to the i highest eigenvalues (lambdas).
    alphas = np.column_stack((eigvecs[:,-i] for i in range(1,n_components+1)))
    lambdas = [eigvals[-i] for i in range(1,n_components+1)]

    return alphas, lambdas
```

现在，让我们生成一个新的半月形数据集，并使用 RBF 核 PCA 将其投影到一个 1 维子空间上：

```python
from sklearn.datasets import make_moons
X, y = make_moons(n_samples=100, random_state=123)
alphas, lambdas = stepwise_kpca(X, gamma=15, n_components=1)
```

```python
/Users/sebastian/miniconda3/envs/py34/lib/python3.4/site-packages/sklearn/datasets/samples_generator.py:612: DeprecationWarning: using a non-integer number instead of an integer will result in an error in the future
  y = np.hstack([np.zeros(n_samples_in, dtype=np.intp),
```

为了确认我们的方法能产生正确的结果，让我们假设半月形数据集中的第 24 个点是一个新的数据点 \( \mathbf{x} \)，我们想把它投影到这个新的子空间上。

```python
x_new = X[25]
X_proj = alphas[25] # original projection
```

```python
x_new
```

```python
array([ 1.8713187 ,  0.00928245])
```

```python
X_proj
```

```python
array([ 0.07877284])
```

```python
def project_x(x_new, X, gamma, alphas, lambdas):
    pair_dist = np.array([np.sum((x_new-row)**2) for row in X])
    k = np.exp(-gamma * pair_dist)
    return k.dot(alphas / lambdas)

# projection of the "new" datapoint
x_reproj = project_x(x_new, X, gamma=15, alphas=alphas, lambdas=lambdas)
```

```python
x_reproj
```

```python
array([ 0.07877284])
```

```python
%matplotlib inline
```

```python
import matplotlib.pyplot as plt
plt.figure(figsize=(8,6))
plt.scatter(alphas[y==0, 0], np.zeros((50)), color='red', alpha=0.5)
plt.scatter(alphas[y==1, 0], np.zeros((50)), color='blue', alpha=0.5)
plt.scatter(X_proj, 0, color='black', label='original projection of point X[24]', marker='^', s=100)
plt.scatter(x_reproj, 0, color='green', label='remapped point X[24]', marker='x', s=500)
plt.legend(scatterpoints=1)
plt.show()
```

![Kernel pca 2014 09 14 kernel pca 121 0](https://sebastianraschka.com/images/blog/2014/kernel_pca/2014-09-14-kernel_pca_121_0.webp)

感谢阅读。如果你喜欢这些内容，也可以在 [Twitter 上找到我](https://twitter.com/rasbt)，我会在那里分享更多有用的内容。

## 参考文献

[1] Q. Wang. [Kernel principal component analysis and its applications in face recognition and active shape models](http://arxiv.org/abs/1207.3538). CoRR, abs/1207.3538, 2012.

[2] B. Scholkopf, A. Smola, and K.-R. Muller. [Kernel principal component analysis](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.128.7613). pages 583–588, 1997.

[3] B. Scholkopf, A. Smola, and K.-R. Muller. [Nonlinear component analysis as a kernel eigenvalue problem](http://www.mitpressjournals.org/doi/abs/10.1162/089976698300017467#.VBh9QkuCFHg). Neural computation, 10(5):1299–1319, 1998.

[4] S. T. Roweis and L. K. Saul. [Nonlinear dimensionality reduction by locally linear embedding](http://www.sciencemag.org/content/290/5500/2323.short). Science, 290(5500):2323–2326, 2000.
