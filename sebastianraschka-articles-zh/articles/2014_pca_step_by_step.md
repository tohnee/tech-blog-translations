---
title: "从零实现主成分分析（PCA）"
title_en: "PCA From Scratch"
source: https://sebastianraschka.com/Articles/2014_pca_step_by_step.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 从零实现主成分分析（PCA）

> 原文：[PCA From Scratch](https://sebastianraschka.com/Articles/2014_pca_step_by_step.html) · Sebastian Raschka's Articles

## 章节

## 引言

主成分分析（principal component analysis）的主要目的，一是对数据进行分析以识别模式，二是通过发现模式来在信息损失尽可能小的前提下降低数据集的维度。

在这里，我们期望主成分分析得到的结果是：把一个特征空间（即由 \(n\) 个 \(d\) 维样本组成的数据集）投影到一个能「很好地」表示我们数据的较小子空间上。一个可能的应用场景是模式分类任务：我们希望通过提取一个能「最好地」描述数据的子空间来减少特征空间的维度，从而降低计算成本以及参数估计的误差。

### 主成分分析（PCA）与多元判别分析（MDA）

多元判别分析（Multiple Discriminant Analysis，MDA）和主成分分析（PCA）都是线性变换方法，而且彼此密切相关。在 PCA 中，我们感兴趣的是找到能使数据集方差最大化的方向（成分）；而在 MDA 中，我们还想进一步找到能最大化不同类别之间分离（或判别）程度的方向（例如，在数据集包含多个类别的模式分类问题中。这与忽略类别标签的 PCA 形成了对比）。

***换句话说，通过 PCA，我们把整个数据集（不带类别标签）投影到另一个子空间上；而在 MDA 中，我们试图确定一个合适的子空间来区分属于不同类别的模式。或者粗略地说，在 PCA 中我们试图找到方差最大、数据散布最开的那些轴（由于 PCA 把整个数据集当作一个类别来看待，所以是在单个类别内部）；而在 MDA 中，我们还要额外最大化类别之间的散布程度。***

在典型的模式识别问题中，PCA 之后往往还会接着做一次 MDA。

#### 什么是「好」的子空间？

假设我们的目标是通过把一个 \(d\) 维数据集投影到一个 \(k\) 维子空间（其中 \(k\;<\;d\)）来降低它的维度。
那么，我们如何知道应该为 \(k\) 选择多大的值？又如何知道我们得到的特征空间是否能「很好地」表示数据呢？
后文我们会从数据集中计算出特征向量（即各个成分），并把它们收集到一个所谓的散布矩阵（scatter matrix）中（或者也可以改为从协方差矩阵计算）。每一个特征向量都对应一个特征值，特征值告诉我们该特征向量的「长度」或「大小」。如果我们观察到所有特征值的量级都非常接近，这就是一个很好的指标，说明我们的数据已经处在一个「好」的子空间中了。而如果其中一些特征值比其他的高出很多，我们可能就只想保留那些特征值大得多的特征向量，因为它们包含了更多关于数据分布的信息。反过来，接近 0 的特征值所包含的信息较少，在构建新的特征子空间时，我们可以考虑舍弃它们。

### PCA 方法步骤总结

下面列出了执行主成分分析的 6 个一般步骤，我们将在后续章节中逐一研究。

1. [取整个由 \(d\) 维样本组成的数据集，忽略类别标签](#drop_labels)
2. [计算 \(d\) 维均值向量](#mean_vec)（即整个数据集中每个维度各自的均值）
3. [计算整个数据集的散布矩阵（或者协方差矩阵）](#sc_matrix)
4. [计算特征向量（\(\pmb e\_1, \; \pmb e\_2, \; ..., \; \pmb e\_d\)）及相应的特征值（\(\pmb \lambda\_1, \; \pmb \lambda\_2, \; ..., \; \pmb \lambda\_d\)）](#eig_vec)
5. [将特征向量按特征值递减排序，并选择特征值最大的 \(k\) 个特征向量，构成一个 \(d \times k\) 维矩阵 \(\pmb W\;\)](#sort_eig)（其中每一列代表一个特征向量）
6. [用这个 \(d \times k\) 维特征向量矩阵把样本变换到新的子空间上。](#transform)这一步可以用下面的数学方程来概括：\(\pmb y = \pmb W^T \times \pmb x\)（其中 \(\pmb x\) 是表示单个样本的 \(d \times 1\) 维向量，\(\pmb y\) 是新子空间中变换后的 \(k \times 1\) 维样本。）

## 生成一些三维样本数据

在下面的例子中，我们将生成 40 个从多元高斯分布中随机抽取的三维样本。
这里我们假设这些样本来自两个不同的类别：数据集的一半（即 20 个）样本标记为 \(\omega\_1\)（类别 1），另一半标记为 \(\omega\_2\)（类别 2）。

\(\pmb{\mu\_1} =\)
\(\begin{bmatrix}0\\0\\0\end{bmatrix}\)
\(\quad\pmb{\mu\_2} =\)
\(\begin{bmatrix}1\\1\\1\end{bmatrix}\quad\)（样本均值）

\(\pmb{\Sigma\_1} =\)
\(\begin{bmatrix}1\quad 0\quad 0\\0\quad 1\quad0\\0\quad0\quad1\end{bmatrix}\)
\(\quad\pmb{\Sigma\_2} =\)
\(\begin{bmatrix}1\quad 0\quad 0\\0\quad 1\quad0\\0\quad0\quad1\end{bmatrix}\quad\)（协方差矩阵）

### 为什么我们要选择三维样本？

多维数据的问题在于难以可视化，这会让我们很难（至少在视觉上）跟上这个主成分分析的例子。当然，我们也可以为下面的例子选择一个二维样本数据集，但由于 PCA 在「降维」应用中的目标是至少舍弃一个维度，我觉得从一个三维数据集出发、通过舍弃 1 个维度把它降为二维数据集，这样更直观、视觉效果也更好。

```python
import numpy as np

np.random.seed(234234782384239784) # random seed for consistency

# A reader pointed out that Python 2.7 would raise a
# "ValueError: object of too small depth for desired array".
# This can be avoided by choosing a smaller random seed, e.g. 1
# or by completely omitting this line, since I just used the random seed for
# consistency.

mu_vec1 = np.array([0,0,0])
cov_mat1 = np.array([[1,0,0],[0,1,0],[0,0,1]])
class1_sample = np.random.multivariate_normal(mu_vec1, cov_mat1, 20).T
assert class1_sample.shape == (3,20), "The matrix has not the dimensions 3x20"

mu_vec2 = np.array([1,1,1])
cov_mat2 = np.array([[1,0,0],[0,1,0],[0,0,1]])
class2_sample = np.random.multivariate_normal(mu_vec2, cov_mat2, 20).T
assert class2_sample.shape == (3,20), "The matrix has not the dimensions 3x20"
```

利用上面的代码，我们创建了两个 \(3\times20\) 的数据集——类别 \(\omega\_1\) 和 \(\omega\_2\) 各一个——
其中每一列都可以看作一个三维向量 \(\pmb x = \begin{pmatrix} x\_1 \\ x\_2 \\ x\_3 \end{pmatrix}\)，于是我们的数据集具有如下形式  
\(\pmb X = \begin{pmatrix} x\_{1\_1}\; x\_{1\_2} \; ... \; x\_{1\_{20}}\\ x\_{2\_1} \; x\_{2\_2} \; ... \; x\_{2\_{20}}\\ x\_{3\_1} \; x\_{3\_2} \; ... \; x\_{3\_{20}}\end{pmatrix}\)

为了对两个类别 \(\omega\_1\) 和 \(\omega\_2\) 的样本分布有一个大致的了解，我们把它们画成一幅三维散点图。

```python
%pylab inline
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, projection='3d')
plt.rcParams['legend.fontsize'] = 10   
ax.plot(class1_sample[0,:], class1_sample[1,:], class1_sample[2,:], 'o', markersize=8, color='blue', alpha=0.5, label='class1')
ax.plot(class2_sample[0,:], class2_sample[1,:], class2_sample[2,:], '^', markersize=8, alpha=0.5, color='red', label='class2')

plt.title('Samples for class 1 and class 2')
ax.legend(loc='upper right')

plt.show()
```

![Principal component analysis old principal component analysis old 14 1](https://sebastianraschka.com/images/blog/2014/principal_component_analysis_old/principal_component_analysis_old_14_1.webp)

## 1. 忽略类别标签，取整个数据集

由于 PCA 分析不需要类别标签，我们把两个类别的样本合并为一个 \(3\times40\) 维数组。

```python
all_samples = np.concatenate((class1_sample, class2_sample), axis=1)
assert all_samples.shape == (3,40), "The matrix has not the dimensions 3x40"
```

## 2. 计算 d 维均值向量

```python
mean_x = np.mean(all_samples[0,:])
mean_y = np.mean(all_samples[1,:])
mean_z = np.mean(all_samples[2,:])

mean_vector = np.array([[mean_x],[mean_y],[mean_z]])

print('Mean Vector:\n', mean_vector)
```

```python
    Mean Vector:
     [[ 0.50576644]
     [ 0.30186591]
     [ 0.76459177]]
```

## 3. a) 计算散布矩阵

散布矩阵由以下方程计算：  
\(S = \sum\limits\_{k=1}^n (\pmb x\_k - \pmb m)\;(\pmb x\_k - \pmb m)^T\)  
其中 \(\pmb m\) 是均值向量  
\(\pmb m = \frac{1}{n} \sum\limits\_{k=1}^n \; \pmb x\_k\)

```python
scatter_matrix = np.zeros((3,3))
for i in range(all_samples.shape[1]):
    scatter_matrix += (all_samples[:,i].reshape(3,1) - mean_vector).dot((all_samples[:,i].reshape(3,1) - mean_vector).T)
print('Scatter Matrix:\n', scatter_matrix)
```

```python
    Scatter Matrix:
     [[ 48.91593255   7.11744916   7.20810281]
     [  7.11744916  37.92902984   2.7370493 ]
     [  7.20810281   2.7370493   35.6363759 ]]
```

## 3. b) 计算协方差矩阵（可代替散布矩阵）

作为替代方案，我们可以不计算散布矩阵，而是使用内置的 `numpy.cov()` 函数来计算协方差矩阵。协方差矩阵和散布矩阵的方程非常相似，唯一的区别在于：协方差矩阵使用了缩放因子 \(\frac{1}{N-1}\)（这里是 \(\frac{1}{40-1} = \frac{1}{39}\)）。因此，它们的***特征空间（eigenspace）***将是完全相同的（特征向量完全一致，只是特征值相差一个常数倍）。

\[\Sigma\_i = \Bigg[
\begin{array}{cc}
\sigma\_{11}^2 & \sigma\_{12}^2 & \sigma\_{13}^2\\
\sigma\_{21}^2 & \sigma\_{22}^2 & \sigma\_{23}^2\\
\sigma\_{31}^2 & \sigma\_{32}^2 & \sigma\_{33}^2\\
\end{array} \Bigg]\]

```python
cov_mat = np.cov([all_samples[0,:],all_samples[1,:],all_samples[2,:]])
print('Covariance Matrix:\n', cov_mat)
```

```python
    Covariance Matrix:
     [[ 1.25425468  0.1824987   0.18482315]
     [ 0.1824987   0.97253923  0.07018075]
     [ 0.18482315  0.07018075  0.91375323]]
```

## 4. 计算特征向量及相应的特征值

为了证明无论特征向量是从散布矩阵还是从协方差矩阵推导出来的，它们都完全相同，我们在代码中加入一条 `assert` 语句。此外，我们还会看到，从散布矩阵推导时，特征值确实被放大了 39 倍。

```python
# eigenvectors and eigenvalues for the from the scatter matrix
eig_val_sc, eig_vec_sc = np.linalg.eig(scatter_matrix)

# eigenvectors and eigenvalues for the from the covariance matrix
eig_val_cov, eig_vec_cov = np.linalg.eig(cov_mat)

for i in range(len(eig_val_sc)):
    eigvec_sc = eig_vec_sc[:,i].reshape(1,3).T
    eigvec_cov = eig_vec_cov[:,i].reshape(1,3).T
    assert eigvec_sc.all() == eigvec_cov.all(), 'Eigenvectors are not identical'

    print('Eigenvector {}: \n{}'.format(i+1, eigvec_sc))
    print('Eigenvalue {} from scatter matrix: {}'.format(i+1, eig_val_sc[i]))
    print('Eigenvalue {} from covariance matrix: {}'.format(i+1, eig_val_cov[i]))
    print('Scaling factor: ', eig_val_sc[i]/eig_val_cov[i])
    print(40 * '-')
```

```python
    Eigenvector 1:
    [[-0.84190486]
     [-0.39978877]
     [-0.36244329]]
    Eigenvalue 1 from scatter matrix: 55.398855957302445
    Eigenvalue 1 from covariance matrix: 1.4204834860846791
    Scaling factor:  39.0
    ----------------------------------------
    Eigenvector 2:
    [[-0.44565232]
     [ 0.13637858]
     [ 0.88475697]]
    Eigenvalue 2 from scatter matrix: 32.42754801292286
    Eigenvalue 2 from covariance matrix: 0.8314755900749456
    Scaling factor:  39.0
    ----------------------------------------
    Eigenvector 3:
    [[ 0.30428639]
     [-0.90640489]
     [ 0.29298458]]
    Eigenvalue 3 from scatter matrix: 34.65493432806495
    Eigenvalue 3 from covariance matrix: 0.8885880596939733
    Scaling factor:  39.0
    ----------------------------------------
```

### 检验特征向量-特征值的计算

让我们快速检验一下特征向量-特征值的计算是否正确、是否满足方程

\[\pmb\Sigma\pmb{v} = \lambda\pmb{v}\]

其中

\[\pmb\Sigma = Covariance \; matrix\\
\pmb{v} = \; Eigenvector\\
\lambda = \; Eigenvalue\]

```python
for i in range(len(eig_val_sc)):
    eigv = eig_vec_sc[:,i].reshape(1,3).T
    np.testing.assert_array_almost_equal(scatter_matrix.dot(eigv), eig_val_sc[i] * eigv,
                                         decimal=6, err_msg='', verbose=True)
```

### 可视化特征向量

在进入下一步之前，为了满足我们自己的好奇心，我们画出以样本均值为中心的特征向量。

```python
%pylab inline

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from matplotlib.patches import FancyArrowPatch

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot(111, projection='3d')

ax.plot(all_samples[0,:], all_samples[1,:], all_samples[2,:], 'o', markersize=8, color='green', alpha=0.2)
ax.plot([mean_x], [mean_y], [mean_z], 'o', markersize=10, color='red', alpha=0.5)
for v in eig_vec_sc.T:
    a = Arrow3D([mean_x, v[0]], [mean_y, v[1]], [mean_z, v[2]], mutation_scale=20, lw=3, arrowstyle="-|>", color="r")
    ax.add_artist(a)
ax.set_xlabel('x_values')
ax.set_ylabel('y_values')
ax.set_zlabel('z_values')

plt.title('Eigenvectors')

plt.show()
```

![Principal component analysis old principal component analysis old 36 1](https://sebastianraschka.com/images/blog/2014/principal_component_analysis_old/principal_component_analysis_old_36_1.webp)

## 5.1. 将特征向量按特征值递减排序

我们的出发点是降低特征空间的维度，也就是通过 PCA 把特征空间投影到一个更小的子空间上，而特征向量将构成这个新特征子空间的坐标轴。不过，特征向量只定义了新坐标轴的方向，因为它们的单位长度都是 1，我们可以用下面的代码来确认这一点：

```python
for ev in eig_vec_sc:
    numpy.testing.assert_array_almost_equal(1.0, np.linalg.norm(ev))
    # instead of 'assert' because of rounding errors
```

因此，为了决定在构建低维子空间时要舍弃哪些特征向量，我们必须查看这些特征向量所对应的特征值。粗略地说，特征值最低的特征向量所承载的关于数据分布的信息最少，正是我们要舍弃的对象。  
常见的做法是把特征向量按对应特征值从高到低排序，然后选择前 \(k\) 个特征向量。

```python
# Make a list of (eigenvalue, eigenvector) tuples
eig_pairs = [(np.abs(eig_val_sc[i]), eig_vec_sc[:,i]) for i in range(len(eig_val_sc))]

# Sort the (eigenvalue, eigenvector) tuples from high to low
eig_pairs.sort(key=lambda x: x[0], reverse=True)

# Visually confirm that the list is correctly sorted by decreasing eigenvalues
for i in eig_pairs:
    print(i[0])
```

```python
    55.3988559573
    34.6549343281
    32.4275480129
```

## 5.2. 选择特征值最大的 *k* 个特征向量

在我们这个把三维特征空间降到二维特征子空间的简单例子中，我们把特征值最大的两个特征向量组合起来，构造我们的 \(d \times k\) 维特征向量矩阵 \(\pmb W\)。

```python
matrix_w = np.hstack((eig_pairs[0][1].reshape(3,1), eig_pairs[1][1].reshape(3,1)))
print('Matrix W:\n', matrix_w)
```

```python
    Matrix W:
     [[-0.84190486  0.30428639]
     [-0.39978877 -0.90640489]
     [-0.36244329  0.29298458]]
```

## 6. 把样本变换到新子空间

在最后一步，我们使用刚刚计算得到的 \(2 \times 3\) 维矩阵 \(\pmb W\)，通过方程 \(\pmb y = \pmb W^T \times \pmb x\) 把样本变换到新的子空间上。

```python
transformed = matrix_w.T.dot(all_samples)
assert transformed.shape == (2,40), "The matrix is not 2x40 dimensional."
```

```python
plt.plot(transformed[0,0:20], transformed[1,0:20], 'o', markersize=7, color='blue', alpha=0.5, label='class1')
plt.plot(transformed[0,20:40], transformed[1,20:40], '^', markersize=7, color='red', alpha=0.5, label='class2')
plt.xlim([-4,4])
plt.ylim([-4,4])
plt.xlabel('x_values')
plt.ylabel('y_values')
plt.legend()
plt.title('Transformed samples with class labels')

plt.show()
```

![Principal component analysis old principal component analysis old 49 0](https://sebastianraschka.com/images/blog/2014/principal_component_analysis_old/principal_component_analysis_old_49_0.webp)

## 使用 matplotlib.mlab 库中的 PCA() 类

现在，我们已经了解了主成分分析是如何工作的，为了在今后的应用中省事，我们可以使用 `matplotlib` 库内置的 `PCA()` 类。
遗憾的是，[官方文档](https://matplotlib.org/1.3.1/api/mlab_api.html#matplotlib.mlab.PCA)写得非常简略。

`PCA()` 类的原始代码实现可以在这里查看：  
<https://github.com/matplotlib/matplotlib/blob/v1.3.1/lib/matplotlib/mlab.py>

### `PCA()` 的类属性

```python
    Attrs:

    a : a centered unit sigma version of input a

    numrows, numcols: the dimensions of a

    mu : a numdims array of means of a

    sigma : a numdims array of atandard deviation of a

    fracs : the proportion of variance of each of the principal components

    Wt : the weight vector for projecting a numdims point or array into PCA space

    Y : a projected into PCA space
```

另外还需要说明的是，`PCA()` 类期望输入是一个 `np.array()`，并且满足 `'we assume data in a is organized with numrows>numcols')`，也就是说我们必须先对数据集做转置。

`matplotlib.mlab.PCA()` 在变换后保留了输入数据集的全部 \(d\) 个维度（保存在类属性 `PCA.Y` 中），而且在假定它们已经排好序的前提下（「由于 PCA 分析会按照描述聚类的重要性递减的顺序来排列各个 PC 轴，我们可以看到 fracs 是一个单调递减的列表。」，<https://matplotlib.org/1.3.1/api/mlab_api.html#matplotlib.mlab.PCA>），如果我们想把三维输入数据集投影到二维子空间上，只需要绘制前 2 列即可。

```python
from matplotlib.mlab import PCA as mlabPCA

mlab_pca = mlabPCA(all_samples.T)

print('PC axes in terms of the measurement axes scaled by the standard deviations:\n', mlab_pca.Wt)

plt.plot(mlab_pca.Y[0:20,0],mlab_pca.Y[0:20,1], 'o', markersize=7, color='blue', alpha=0.5, label='class1')
plt.plot(mlab_pca.Y[20:40,0], mlab_pca.Y[20:40,1], '^', markersize=7, color='red', alpha=0.5, label='class2')

plt.xlabel('x_values')
plt.ylabel('y_values')
plt.xlim([-4,4])
plt.ylim([-4,4])
plt.legend()
plt.title('Transformed samples with class labels from matplotlib.mlab.PCA()')

plt.show()
```

```python
    PC axes in terms of the measurement axes scaled by the standard deviations:
     [[ 0.65043619  0.53023618  0.54385876]
     [-0.01692055  0.72595458 -0.68753447]
     [ 0.75937241 -0.43799491 -0.48115902]]
```

![Principal component analysis old principal component analysis old 54 1](https://sebastianraschka.com/images/blog/2014/principal_component_analysis_old/principal_component_analysis_old_54_1.webp)

## 逐步实现方法与 matplotlib.mlab.PCA() 之间的差异

当我们把变换后的数据集绘制到新的二维子空间上时，会发现逐步实现方法和 `matplotlib.mlab.PCA()` 类得到的散点图看起来并不相同。原因在于 `matplotlib.mlab.PCA()` 类在计算协方差矩阵之前会***把各个变量缩放到单位方差***。这最终会/可能导致沿各坐标轴的方差有所不同，并影响各个变量对主成分的贡献。

一个适合做缩放的场景是：一个变量的单位是**英寸（inches）**，而另一个变量的单位是**厘米（cm）**。
不过，在我们这个假设性的例子中，我们假定两个变量使用相同的（任意）单位，因此我们跳过了对输入数据进行缩放这一步。

## 使用 sklearn.decomposition 库中的 PCA() 类来确认我们的结果

为了确保我们的逐步实现方法没有出错，我们将使用另一个默认不会对输入数据做重新缩放的库。
这里我们使用 `scikit-learn` 机器学习库中的 PCA 类。其文档在这里：  
<http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html>。

为了方便，我们可以直接通过 `n_components` 参数指定要把输入数据集降到多少个成分。

```python
    n_components : int, None or string

    Number of components to keep. if n_components is not set all components are kept:
        n_components == min(n_samples, n_features)
        if n_components == ‘mle’, Minka’s MLE is used to guess the dimension if 0 < n_components < 1,
        select the number of components such that the amount of variance that needs to be explained
        is greater than the percentage specified by n_components
```

接下来，我们只需要使用 `.fit_transform()` 即可完成降维。

```python
from sklearn.decomposition import PCA as sklearnPCA

sklearn_pca = sklearnPCA(n_components=2)
sklearn_transf = sklearn_pca.fit_transform(all_samples.T)

plt.plot(sklearn_transf[0:20,0],sklearn_transf[0:20,1], 'o', markersize=7, color='blue', alpha=0.5, label='class1')
plt.plot(sklearn_transf[20:40,0], sklearn_transf[20:40,1], '^', markersize=7, color='red', alpha=0.5, label='class2')

plt.xlabel('x_values')
plt.ylabel('y_values')
plt.xlim([-4,4])
plt.ylim([-4,4])
plt.legend()
plt.title('Transformed samples with class labels from matplotlib.mlab.PCA()')

plt.show()
```

![Principal component analysis old principal component analysis old 62 0](https://sebastianraschka.com/images/blog/2014/principal_component_analysis_old/principal_component_analysis_old_62_0.webp)

上图看起来恰好是我们逐步实现方法所绘图形的镜像。这是因为特征向量的符号可正可负——由于特征向量被缩放成了单位长度 1——我们只需把变换后的数据乘以 \(\times(-1)\) 即可翻转镜像图像。

```python
sklearn_transf = sklearn_transf * (-1)

# sklearn.decomposition.PCA
plt.plot(sklearn_transf[0:20,0],sklearn_transf[0:20,1], 'o', markersize=7, color='blue', alpha=0.5, label='class1')
plt.plot(sklearn_transf[20:40,0], sklearn_transf[20:40,1], '^', markersize=7, color='red', alpha=0.5, label='class2')
plt.xlabel('x_values')
plt.ylabel('y_values')
plt.xlim([-4,4])
plt.ylim([-4,4])
plt.legend()
plt.title('Transformed samples via sklearn.decomposition.PCA')
plt.show()

# step by step PCA
plt.plot(transformed[0,0:20], transformed[1,0:20], 'o', markersize=7, color='blue', alpha=0.5, label='class1')
plt.plot(transformed[0,20:40], transformed[1,20:40], '^', markersize=7, color='red', alpha=0.5, label='class2')
plt.xlim([-4,4])
plt.ylim([-4,4])
plt.xlabel('x_values')
plt.ylabel('y_values')
plt.legend()
plt.title('Transformed samples step by step approach')
plt.show()
```

![Principal component analysis old principal component analysis old 64 0](https://sebastianraschka.com/images/blog/2014/principal_component_analysis_old/principal_component_analysis_old_64_0.webp)

![Principal component analysis old principal component analysis old 64 1](https://sebastianraschka.com/images/blog/2014/principal_component_analysis_old/principal_component_analysis_old_64_1.webp)

观察上面两幅图，沿各成分轴的分布看起来是一样的，只是数据的中心略有不同。如果我们想模仿 scikit-learn 的 `PCA` 类所产生的结果，可以从样本 `X` 中减去均值向量，把数据的中心移到坐标系的原点上（感谢 Alexander Guth 的建议）——也就是把变换 `transformed = matrix_w.T.dot(all_samples)` 替换为 `transformed = matrix_w.T.dot(all_samples - mean_vector)`。
