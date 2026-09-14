---
title: "数据处理入门"
title_en: "Entry Point Data"
source: https://sebastianraschka.com/Articles/2014_scikit_dataprocessing.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 数据处理入门

> 原文：[Entry Point Data](https://sebastianraschka.com/Articles/2014_scikit_dataprocessing.html) · Sebastian Raschka's Articles

在这篇简短的教程中，我想简要概述一些我最喜欢的 Python 工具，它们涵盖了通用模式分类、机器学习任务以及各种其他数据分析中常见流程的入口步骤。

## 章节

## 安装 Python 包

**在本节中，我想推荐一种安装所需 Python 包的方法——如果你还没有安装的话。否则你可以直接跳过这一部分。**

本教程将使用以下包：

- [NumPy](http://www.numpy.org)
- [SciPy](http://www.scipy.org)
- [matplotlib](http://matplotlib.org)
- [scikit-learn](http://scikit-learn.org/stable/)

虽然这些包可以「手动」逐步安装，但我强烈建议你了解一下面向科学计算的 [Anaconda](https://store.continuum.io/cshop/anaconda/) Python 发行版。

Anaconda 由 Continuum Analytics 发行，但它完全免费，截至目前已包含 195 多个用于科学与数据分析的包。
安装步骤在这里有很好的总结：http://docs.continuum.io/anaconda/install.html

如果这对你来说太重了，那么 [Miniconda](http://conda.pydata.org/miniconda.html) 可能更适合你。Miniconda 基本上只是一个自带 Conda 包管理器的 Python 发行版，它让我们可以在 Shell 终端中把一系列 Python 包安装到指定的 `conda` 环境里，例如：

```python
$$[bash]> conda create -n myenv python=3
$$[bash]> source activate myenv
$$[bash]> conda install -n myenv numpy scipy matplotlib scikit-learn</pre>
```

现在，当我们在当前的 shell 会话中启动 "python" 时，它将使用我们刚刚创建的虚拟环境 "myenv" 中的 Python 发行版。要脱离（停用）该虚拟环境，只需使用

```python
<pre>$$[bash]> source deactivate myenv
```

**注意：** 默认情况下，环境会被创建在 ROOT\_DIR/envs 目录下；你可以在上面的 conda 命令中使用 `-p` 标志代替 `-n` 标志，以便指定自定义路径。

**我觉得这个流程非常方便，尤其是当你需要在安装了不同模块和包的不同 Python 发行版及版本之间切换时；而且它对于测试你自己的模块也极其有用。**

## 关于数据集

在下面的教程中，我们将使用存放在 UCI 机器学习仓库（http://archive.ics.uci.edu/ml/datasets/Wine）中的免费「Wine（葡萄酒）」数据集。

\*\*参考文献：\*\*
Forina, M. et al, PARVUS - An Extendible Package for Data
Exploration, Classification and Correlation. Institute of Pharmaceutical
and Food Analysis and Technologies, Via Brigata Salerno,
16147 Genoa, Italy.
Bache, K. & Lichman, M. (2013). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.

Wine 数据集由 3 个不同的类别组成，其中每一行对应一个特定的葡萄酒样本。

类别标签（1、2、3）列在第一列，第 2–14 列对应以下 13 个属性（特征）：

1. 酒精含量（Alcohol）
2. 苹果酸（Malic acid）
3. 灰分（Ash）
4. 灰分的碱度（Alcalinity of ash）
5. 镁（Magnesium）
6. 总酚（Total phenols）
7. 黄酮类物质（Flavanoids）
8. 非黄酮类酚（Nonflavanoid phenols）
9. 原花青素（Proanthocyanins）
10. 颜色强度（Color intensity）
11. 色调（Hue）
12. 稀释酒的 OD280/OD315
13. 脯氨酸（Proline）

`wine_data.csv` 数据集的一个节选：

```python
1,14.23,1.71,2.43,15.6,127,2.8,3.06,.28,2.29,5.64,1.04,3.92,1065
1,13.2,1.78,2.14,11.2,100,2.65,2.76,.26,1.28,4.38,1.05,3.4,1050
[...]
2,12.37,.94,1.36,10.6,88,1.98,.57,.28,.42,1.95,1.05,1.82,520
2,12.33,1.1,2.28,16,101,2.05,1.09,.63,.41,3.27,1.25,1.67,680
[...]
3,12.86,1.35,2.32,18,122,1.51,1.25,.21,.94,4.1,.76,1.29,630
3,12.88,2.99,2.4,20,104,1.3,1.22,.24,.83,5.4,.74,1.42,530
```

## 从网络下载并保存 CSV 数据文件

通常，我们的数据以常见的文本（或 CSV）文件形式存储在本地磁盘上，各行之间以逗号、制表符或空格分隔。下面只是一个示例，演示如何把 HTML 网站上的 CSV 数据文件直接加载到 Python 中，并可选择将其保存到本地。

```python
import csv
import urllib

url = 'https://raw.githubusercontent.com/rasbt/pattern_classification/master/data/wine_data.csv'
csv_cont = urllib.request.urlopen(url)
csv_cont = csv_cont.read() #.decode('utf-8')

# Optional: saving the data to your local drive
with open('./wine_data.csv', 'wb') as out:
    out.write(csv_cont)
```

**注意：** 如果你更希望直接以 `str`（字符串）格式处理数据，只需对默认以字节格式读入的数据调用 `.decode('utf-8')` 方法即可。

## 从 CSV 文件读入数据集

正如上文提到的，输入数据通常都存储在本地，因此我们将使用 [`numpy.loadtxt`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html) 函数从 CSV 文件中读入数据。
（也可以类似地使用 [`np.genfromtxt()`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.genfromtxt.html)，它提供了一些额外的选项。）

```python
import numpy as np

# reading in all data into a NumPy array
all_data = np.loadtxt(open("./wine_data.csv","r"),
        delimiter=",",
        skiprows=0,
        dtype=np.float64
        )

# load class labels from column 1
y_wine = all_data[:,0]

# conversion of the class labels to integer-type array
y_wine = y_wine.astype(np.int64, copy=False)

# load the 14 features
X_wine = all_data[:,1:]

# printing some general information about the data
print('\ntotal number of samples (rows):', X_wine.shape[0])
print('total number of features (columns):', X_wine.shape[1])

# printing the 1st wine sample
float_formatter = lambda x: '{:.2f}'.format(x)
np.set_printoptions(formatter={'float_kind':float_formatter})
print('\n1st sample (i.e., 1st row):\nClass label: {:d}\n{:}\n'
          .format(int(y_wine[0]), X_wine[0]))

# printing the rel.frequency of the class labels
print('Class label frequencies')
print('Class 1 samples: {:.2%}'.format(list(y_wine).count(1)/y_wine.shape[0]))
print('Class 2 samples: {:.2%}'.format(list(y_wine).count(2)/y_wine.shape[0]))
print('Class 3 samples: {:.2%}'.format(list(y_wine).count(3)/y_wine.shape[0]))
```

```python
total number of samples (rows): 178
total number of features (columns): 13

1st sample (i.e., 1st row):
Class label: 1
[14.23 1.71 2.43 15.60 127.00 2.80 3.06 0.28 2.29 5.64 1.04 3.92 1065.00]

Class label frequencies
Class 1 samples: 33.15%
Class 2 samples: 39.89%
Class 3 samples: 26.97%
```

## 数据集可视化

可视化数据集的方式无穷无尽，目的是对数据的样子先有一个初步的了解。其中最常见的可能就是直方图和散点图。

### 直方图

直方图是探索每个特征在各个类别上分布情况的有用工具。它可以为我们提供直观的洞察，让我们了解哪些特征的类间分离效果较好、哪些不太理想。下面，我们将为三个葡萄酒类别的「酒精含量」特征绘制一个示例直方图。

```python
from matplotlib import pyplot as plt
from math import floor, ceil # for rounding up and down

plt.figure(figsize=(10,8))

# bin width of the histogram in steps of 0.15
bins = np.arange(floor(min(X_wine[:,0])), ceil(max(X_wine[:,0])), 0.15)

# get the max count for a particular bin for all classes combined
max_bin = max(np.histogram(X_wine[:,0], bins=bins)[0])

# the order of the colors for each histogram
colors = ('blue', 'red', 'green')

for label,color in zip(
        range(1,4), colors):

    mean = np.mean(X_wine[:,0][y_wine == label]) # class sample mean
    stdev = np.std(X_wine[:,0][y_wine == label]) # class standard deviation
    plt.hist(X_wine[:,0][y_wine == label],
             bins=bins,
             alpha=0.3, # opacity level
             label='class {} ($$\mu={:.2f}$$, $$\sigma={:.2f}$$)'.format(label, mean, stdev),
             color=color)

plt.ylim([0, max_bin*1.3])
plt.title('Wine data set - Distribution of alocohol contents')
plt.xlabel('alcohol by volume', fontsize=14)
plt.ylabel('count', fontsize=14)
plt.legend(loc='upper right')

plt.show()
```

![Python data entry point python data entry point 40 0](https://sebastianraschka.com/images/blog/2014/python_data_entry_point/python_data_entry_point_40_0.webp)

### 散点图

散点图适用于在不止一个维度上可视化特征，例如用来感受特定特征之间的相关性。
遗憾的是，我们无法在这里一次性绘制全部 13 个特征，因为人类视觉皮层最多只能感知三个维度。

下面，我们将用「酒精含量」和「苹果酸含量」这两个特征绘制一个二维散点图示例。
此外，我们还将使用 [`scipy.stats.pearsonr`](http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html) 函数计算这两个特征之间的皮尔逊相关系数（Pearson correlation coefficient）。

```python
from scipy.stats import pearsonr

plt.figure(figsize=(10,8))

for label,marker,color in zip(
        range(1,4),('x', 'o', '^'),('blue', 'red', 'green')):

    # Calculate Pearson correlation coefficient
    R = pearsonr(X_wine[:,0][y_wine == label], X_wine[:,1][y_wine == label])
    plt.scatter(x=X_wine[:,0][y_wine == label], # x-axis: feat. from col. 1
                y=X_wine[:,1][y_wine == label], # y-axis: feat. from col. 2
                marker=marker, # data point symbol for the scatter plot
                color=color,
                alpha=0.7,
                label='class {:}, R={:.2f}'.format(label, R[0]) # label for the legend
                )

plt.title('Wine Dataset')
plt.xlabel('alcohol by volume in percent')
plt.ylabel('malic acid in g/l')
plt.legend(loc='upper right')

plt.show()
```

![Python data entry point python data entry point 46 0](https://sebastianraschka.com/images/blog/2014/python_data_entry_point/python_data_entry_point_46_0.webp)

如果我们想把 3 个不同的特征同时放进一张散点图里，也可以用三维（3D）的方式来做同样的事情：

```python
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, projection='3d')

for label,marker,color in zip(
        range(1,4),('x', 'o', '^'),('blue','red','green')):

    ax.scatter(X_wine[:,0][y_wine == label],
               X_wine[:,1][y_wine == label],
               X_wine[:,2][y_wine == label],  
               marker=marker,
               color=color,
               s=40,
               alpha=0.7,
               label='class {}'.format(label))

ax.set_xlabel('alcohol by volume in percent')
ax.set_ylabel('malic acid in g/l')
ax.set_zlabel('ash content in g/l')

plt.title('Wine dataset')

plt.show()
```

![Python data entry point python data entry point 49 0](https://sebastianraschka.com/images/blog/2014/python_data_entry_point/python_data_entry_point_49_0.webp)

## 划分训练集与测试集

对机器学习和模式分类任务而言，一个典型的流程是把一个数据集一分为二：训练数据集和测试数据集。
此后，训练数据集用于训练我们的算法或分类器，而测试数据集则提供了一种相当客观的方式来验证结果，然后我们再将其应用于「新的真实世界数据」。

这里，我们将对数据集进行随机划分，使整个数据集的 70% 成为我们的训练数据集，30% 成为测试数据集。

```python
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing

X_train, X_test, y_train, y_test = train_test_split(X_wine, y_wine,
     test_size=0.30, random_state=123)
```

请注意，由于这是随机分配，每个类别标签的原始相对频率并没有得到保持。

```python
print('Class label frequencies')

print('\nTraining Dataset:')    
for l in range(1,4):
    print('Class {:} samples: {:.2%}'.format(l, list(y_train).count(l)/y_train.shape[0]))

print('\nTest Dataset:')     
for l in range(1,4):
    print('Class {:} samples: {:.2%}'.format(l, list(y_test).count(l)/y_test.shape[0]))
```

```python
Class label frequencies

Training Dataset:
Class 1 samples: 36.29%
Class 2 samples: 42.74%
Class 3 samples: 20.97%

Test Dataset:
Class 1 samples: 25.93%
Class 2 samples: 33.33%
Class 3 samples: 40.74%
```

## 特征缩放

### 标准化

另一个重要流程是在拟合模型和进行其他分析之前先对数据做标准化，使特征具有标准正态分布的性质，即

\(\mu = 0\) 和 \(\sigma = 1\)

其中 \(\mu\) 是均值（平均数），\(\sigma\) 是相对均值的标准差；样本的标准分数（也称为 ***z*** 分数）按如下方式计算：

\begin{equation} z = \frac{x - \mu}{\sigma}\end{equation}

对特征进行标准化，使其以 0 为中心、标准差为 1，这在我们比较具有不同单位的测量值时尤为重要。例如，在我们的「葡萄酒数据」示例中，酒精含量以体积百分比为单位，而苹果酸含量以 g/l 为单位。

```python
std_scale = preprocessing.StandardScaler().fit(X_train)
X_train = std_scale.transform(X_train)
X_test = std_scale.transform(X_test)
```

```python
f, ax = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(10,5))

for a,x_dat, y_lab in zip(ax, (X_train, X_test), (y_train, y_test)):

    for label,marker,color in zip(
        range(1,4),('x', 'o', '^'),('blue','red','green')):

        a.scatter(x=x_dat[:,0][y_lab == label],
                y=x_dat[:,1][y_lab == label],
                marker=marker,
                color=color,   
                alpha=0.7,   
                label='class {}'.format(label)
                )

    a.legend(loc='upper left')

ax[0].set_title('Training Dataset')
ax[1].set_title('Test Dataset')
f.text(0.5, 0.04, 'malic acid (standardized)', ha='center', va='center')
f.text(0.08, 0.5, 'alcohol (standardized)', ha='center', va='center', rotation='vertical')

plt.show()
```

![Python data entry point python data entry point 63 0](https://sebastianraschka.com/images/blog/2014/python_data_entry_point/python_data_entry_point_63_0.webp)

### Min-Max 缩放（归一化）

标准化之外的一种替代方法是所谓的 Min-Max 缩放（有时也被称为「归一化」）。
在这种方法中，数据被缩放到一个固定的范围——通常是 0 到 1。
与标准化相比，这种有界范围的代价是我们最终会得到较小的标准差，例如在存在离群点的情况下。

计算「归一化」分数的公式为：

\begin{equation} X’ = \frac{X - X\_{min}}{X\_{max}-X\_{min}} \end{equation}

```python
minmax_scale = preprocessing.MinMaxScaler(feature_range=(0, 1)).fit(X_train)
X_train_minmax = minmax_scale.transform(X_train)
X_test_minmax = minmax_scale.transform(X_test)
```

```python
f, ax = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(10,5))

for a,x_dat, y_lab in zip(ax, (X_train_minmax, X_test_minmax), (y_train, y_test)):

    for label,marker,color in zip(
        range(1,4),('x', 'o', '^'),('blue','red','green')):

        a.scatter(x=x_dat[:,0][y_lab == label],
                y=x_dat[:,1][y_lab == label],
                marker=marker,
                color=color,   
                alpha=0.7,   
                label='class {}'.format(label)
                )

    a.legend(loc='upper left')

ax[0].set_title('Training Dataset')
ax[1].set_title('Test Dataset')
f.text(0.5, 0.04, 'malic acid (normalized)', ha='center', va='center')
f.text(0.08, 0.5, 'alcohol (normalized)', ha='center', va='center', rotation='vertical')

plt.show()
```

![Python data entry point python data entry point 70 0](https://sebastianraschka.com/images/blog/2014/python_data_entry_point/python_data_entry_point_70_0.webp)

## 线性变换：主成分分析（PCA）

主成分分析的主要目的是分析数据以识别模式，并利用所发现的模式在尽量少损失信息的前提下降低数据集的维度。

在这里，我们期望的主成分分析结果是：把特征空间（即由 n × d 维样本组成的数据集）投影到一个能「很好地」表示数据的更小子空间上。一个可能的应用是模式分类任务：通过提取一个能「最好地」描述数据的子空间来减少特征空间的维度，从而降低计算成本和参数估计的误差。

如果你想更详细地了解主成分分析，我在另一篇文章[《Implementing a Principal Component Analysis (PCA) in Python step by step》（在 Python 中一步步实现主成分分析）](https://sebastianraschka.com/Articles/2014_pca_step_by_step.html)中概述了具体步骤。

这里，我们将使用 [`sklearn.decomposition.PCA`](http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html) 把训练数据变换到二维子空间上：

```python
from sklearn.decomposition import PCA
sklearn_pca = PCA(n_components=2) # number of components to keep
sklearn_transf = sklearn_pca.fit_transform(X_train)

plt.figure(figsize=(10,8))

for label,marker,color in zip(
        range(1,4),('x', 'o', '^'),('blue', 'red', 'green')):

    plt.scatter(x=sklearn_transf[:,0][y_train == label],
                y=sklearn_transf[:,1][y_train == label],
                marker=marker,
                color=color,
                alpha=0.7,
                label='class {}'.format(label)
                )

plt.xlabel('vector 1')
plt.ylabel('vector 2')

plt.legend()
plt.title('Most significant singular vectors after linear transformation via PCA')

plt.show()
```

![Python data entry point python data entry point 77 0](https://sebastianraschka.com/images/blog/2014/python_data_entry_point/python_data_entry_point_77_0.webp)

### 用于特征提取的 PCA

正如上面简短的介绍所提到的（在我的另一篇 [PCA 文章](https://sebastianraschka.com/Articles/2014_pca_step_by_step.html)中有更详细的说明），PCA 在模式分类领域常被用于特征选择（或降维）。
默认情况下，变换后的数据会按方差最大的成分排序（降序）。

在上面的例子中，我只保留了前 2 个成分（沿各轴方差最大的 2 个成分）：样本空间被投影到一个二维子空间上，这对于把数据绘制成二维散点图来说基本已经足够了。

不过，如果我们想把 PCA 用于特征选择，我们可能并不希望如此大幅度地降低维度。默认情况下，`PCA` 函数（`PCA(n_components=None)`）会按排名顺序保留所有成分。因此，我们基本上既可以把 `n_components` 设置为小于输入数据集维数的值，也可以之后从返回的 NumPy 数组中提取前 **n** 个成分。

要了解每个成分（相对地）「解释」方差的程度，我们可以使用 `explained_variance_ratio_` 实例方法；它同时也证实了这些成分是按解释力从强到弱排序的（这些比率之和为 1.0）。

```python
sklearn_pca = PCA(n_components=None)
sklearn_transf = sklearn_pca.fit_transform(X_train)
sklearn_pca.explained_variance_ratio_
```

```python
array([0.36, 0.21, 0.10, 0.08, 0.06, 0.05, 0.04, 0.03, 0.02, 0.02, 0.01,
       0.01, 0.01])
```

## 线性变换：线性判别分析（MDA）

线性判别分析（LDA）的主要目的是分析数据、识别模式，以便把数据投影到一个能实现更好类别分离的子空间上。同时，数据集的维度也应尽量少损失信息地被降低。

**这种方法与主成分分析（PCA）非常相似，但除了寻找使数据方差最大化的成分轴之外，我们还额外关心能使各类别分离最大化的轴（例如，在有监督的模式分类问题中）。**

在这里，我们期望的线性判别分析结果是：把特征空间（即由 n 个 d 维样本组成的数据集）投影到一个既能「很好地」表示数据、又具有良好类别分离性的更小子空间上。一个可能的应用是模式分类任务：通过提取一个能「最好地」描述数据的子空间来减少特征空间的维度，从而降低计算成本和参数估计的误差。

### 主成分分析（PCA）与线性判别分析（LDA）对比

线性判别分析和主成分分析都是线性变换方法，且彼此密切相关。在 PCA 中，我们感兴趣的是找到使数据集方差最大化的方向（成分）；而在 LDA 中，我们还额外关心找到使不同类别之间分离（或判别）程度最大化的方向（例如，在数据集包含多个类别的模式分类问题中。相比之下，PCA 会忽略类别标签）。

**换句话说，在 PCA 中，我们把整个数据集（不带类别标签）投影到一个不同的子空间上；而在 LDA 中，我们试图确定一个合适的子空间来区分属于不同类别的模式。或者粗略地说，PCA 试图找到方差最大、数据散布最开的轴（这里的散布是就单一类别内部而言的，因为 PCA 把整个数据集当作一个类别来处理），而 LDA 在此基础上还要最大化类别之间的散布程度。**

![Python data entry point lda 1](https://sebastianraschka.com/images/blog/2014/python_data_entry_point/lda_1.webp)

如果你有兴趣，可以在我的 IPython notebook[《Stepping through a Linear Discriminant Analysis - using Python's NumPy and matplotlib》（逐步讲解线性判别分析——使用 Python 的 NumPy 和 matplotlib）](https://github.com/rasbt/pattern_classification/blob/master/dimensionality_reduction/projection/linear_discriminant_analysis.ipynb)中找到关于 LDA 的更多信息。

就像上面 PCA 一节中所做的那样，我们将使用 `scikit-learn` 的函数 [`sklearn.lda.LDA`](https://scikit-learn.org/stable/modules/generated/sklearn.discriminant_analysis.LinearDiscriminantAnalysis.html) 把训练数据变换到二维子空间上：

```python
from sklearn.lda import LDA
sklearn_lda = LDA(n_components=2)
transf_lda = sklearn_lda.fit_transform(X_train, y_train)

plt.figure(figsize=(10,8))

for label,marker,color in zip(
        range(1,4),('x', 'o', '^'),('blue', 'red', 'green')):

    plt.scatter(x=transf_lda[:,0][y_train == label],
                y=transf_lda[:,1][y_train == label],
                marker=marker,
                color=color,
                alpha=0.7,
                label='class {}'.format(label)
                )

plt.xlabel('vector 1')
plt.ylabel('vector 2')

plt.legend()
plt.title('Most significant singular vectors after linear transformation via LDA')

plt.show()
```

![Python data entry point python data entry point 92 0](https://sebastianraschka.com/images/blog/2014/python_data_entry_point/python_data_entry_point_92_0.webp)

### 用于特征提取的 LDA

如果我们想用 LDA 把数据投影到一个更小的子空间上（即进行降维），可以直接通过 `LDA(n_components=...)` 设置要保留的成分数量；这与我们前面见过的 [PCA 函数](#PCA-for-feature-extraction)类似。

## 简单的有监督分类

### 将线性判别分析用作简单线性分类器

我们在上一节中使用的 LDA 也可以用作一个简单的线性分类器。

```python
# fit model
lda_clf = LDA()
lda_clf.fit(X_train, y_train)
LDA(n_components=None, priors=None)

# prediction
print('1st sample from test dataset classified as:', lda_clf.predict(X_test[0,:]))
print('actual class label:', y_test[0])
```

```python
1st sample from test dataset classified as: [3]
actual class label: 3
```

sklearn 中另一个好用的子包是 `metrics`。例如，[`metrics.accuracy_score`](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html) 对于评估有多少样本能被正确分类非常有用：

```python
from sklearn import metrics
pred_train_lda = lda_clf.predict(X_train)

print('Prediction accuracy for the training dataset')
print('{:.2%}'.format(metrics.accuracy_score(y_train, pred_train_lda)))
```

```python
Prediction accuracy for the training dataset
100.00%
```

为了验证我们的模型没有过拟合训练数据集，让我们在测试数据集上评估一下该分类器的准确率：

```python
pred_test_lda = lda_clf.predict(X_test)

print('Prediction accuracy for the test dataset')
print('{:.2%}'.format(metrics.accuracy_score(y_test, pred_test_lda)))
```

```python
Prediction accuracy for the test dataset
98.15%
```

**混淆矩阵**
正如上面所看到的，把分类器应用到测试数据集上时，误分类率非常低。混淆矩阵可以更详细地告诉我们具体是哪些类别没能被正确分类。

![Python data entry point confusion matrix](https://sebastianraschka.com/images/blog/2014/python_data_entry_point/confusion_matrix.webp)

```python
print('Confusion Matrix of the LDA-classifier')
print(metrics.confusion_matrix(y_test, lda_clf.predict(X_test)))
```

```python
Confusion Matrix of the LDA-classifier
[[14  0  0]
 [ 1 17  0]
 [ 0  0 22]]
```

正如我们所见，有一个来自类别 2 的样本被错误地标记为类别 1：从类别 1 的角度看，这是 1 个「假负例（False Negative）」；而相应地从类别 2 的角度看，这就是一个「假正例（False Positive）」。

### 基于随机梯度下降（SGD）的分类

现在，让我们把 LDA 分类器的分类准确率与一个通过随机梯度下降（stochastic gradient descent，一种最小化线性目标函数的算法）实现的简单分类器比较一下（这里我们同样使用了可能并不理想的默认设置）。
关于 `sklearn.linear_model.SGDClassifier` 的更多信息可以在[这里](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html)找到。

```python
from sklearn.linear_model import SGDClassifier

sgd_clf = SGDClassifier()
sgd_clf.fit(X_train, y_train)

pred_train_sgd = sgd_clf.predict(X_train)
pred_test_sgd = sgd_clf.predict(X_test)

print('\nPrediction accuracy for the training dataset')
print('{:.2%}\n'.format(metrics.accuracy_score(y_train, pred_train_sgd)))

print('Prediction accuracy for the test dataset')
print('{:.2%}\n'.format(metrics.accuracy_score(y_test, pred_test_sgd)))

print('Confusion Matrix of the SGD-classifier')
print(metrics.confusion_matrix(y_test, sgd_clf.predict(X_test)))
```

```python
Prediction accuracy for the training dataset
99.19%

Prediction accuracy for the test dataset
100.00%

Confusion Matrix of the SGD-classifier
[[14  0  0]
 [ 0 18  0]
 [ 0  0 22]]
```

相当令人印象深刻的是，我们在没有额外花力气调整任何参数和设置的情况下，就在测试数据集上取得了 100% 的预测准确率。

### 决策区域

```python
sgd_clf2 = SGDClassifier()
sgd_clf2.fit(X_train[:, :2], y_train)

x_min = X_test[:, 0].min()  
x_max = X_test[:, 0].max()
y_min = X_test[:, 1].min()
y_max = X_test[:, 1].max()

step = 0.01
X, Y = np.meshgrid(np.arange(x_min, x_max, step), np.arange(y_min, y_max, step))

Z = sgd_clf2.predict(np.c_[X.ravel(), Y.ravel()])
Z = Z.reshape(X.shape)

# Plots decision regions
plt.contourf(X, Y, Z)

# Plots samples from training data set
plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train)
plt.show()
```

## 保存处理后的数据集

### Pickle

Python 标准库中内置的 [`pickle`](https://docs.python.org/3.4/library/pickle.html) 模块是一个便捷的工具，可以把 Python 对象以字节格式保存。例如，这让我们能够保存 NumPy 数组和分类器，以便之后在另一次或另一个 Python 会话中加载它们，继续处理我们的数据，比如训练一个分类器。

```python
# export objects via pickle

import pickle

pickle_out = open('standardized_data.pkl', 'wb')
pickle.dump([X_train, X_test, y_train, y_test], pickle_out)
pickle_out.close()

pickle_out = open('classifiers.pkl', 'wb')
pickle.dump([lda_clf, sgd_clf], pickle_out)
pickle_out.close()
```

```python
# import objects via pickle

my_object_file = open('standardized_data.pkl', 'rb')
X_train, X_test, y_train, y_test = pickle.load(my_object_file)
my_object_file.close()

my_object_file = open('classifiers.pkl', 'rb')
lda_clf, sgd_clf = pickle.load(my_object_file)
my_object_file.close()

print('Confusion Matrix of the SGD-classifier')
print(metrics.confusion_matrix(y_test, sgd_clf.predict(X_test)))
```

```python
Confusion Matrix of the SGD-classifier
[[14  0  0]
 [ 0 18  0]
 [ 0  0 22]]
```

### 逗号分隔值（CSV）格式

此外，把数据保存为常见的文本格式（比如我们最开始使用的 CSV 格式）也永远是个好主意。不过首先，让我们把类别标签加回到训练数据集和测试数据集的最前面一列。

```python
training_data = np.hstack((y_train.reshape(y_train.shape[0], 1), X_train))
test_data = np.hstack((y_test.reshape(y_test.shape[0], 1), X_test))
```

现在，我们可以使用 [`numpy.savetxt`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.savetxt.html) 函数把测试数据集和训练数据集保存为 2 个独立的 CSV 文件。

```python
np.savetxt('./training_set.csv', training_data, delimiter=',')
np.savetxt('./test_set.csv', test_data, delimiter=',')
```
