---
title: "特征缩放与归一化"
title_en: "Feature Scaling and Normalization"
source: https://sebastianraschka.com/Articles/2014_about_feature_scaling.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 特征缩放与归一化

> 原文：[Feature Scaling and Normalization](https://sebastianraschka.com/Articles/2014_about_feature_scaling.html) · Sebastian Raschka's Articles

## 章节

## 关于标准化

**标准化**（standardization，或称 **z 分数归一化**，Z-score normalization）的结果是：特征会被重新缩放，使其具有标准正态分布的性质，即

\(\mu = 0\) 和 \(\sigma = 1\)

其中 \(\mu\) 是均值（平均数），\(\sigma\) 是相对于均值的标准差；样本的标准分数（也称为 ***z*** 分数）按如下方式计算：

\[z = \frac{x - \mu}{\sigma}\]

将特征标准化，使其以 0 为中心、标准差为 1，这不仅在我们比较具有不同单位的测量值时很重要，而且也是许多机器学习算法的普遍要求。直观上，我们可以把梯度下降当作一个典型例子
（一种常用于逻辑回归、支持向量机（SVM）、感知器、神经网络等的优化算法）；当特征处于不同尺度时，某些权重的更新可能会快于其他权重，因为特征值 \(x\_j\) 在权重更新中起到了作用：

\[\Delta w\_j = - \eta \frac{\partial J}{\partial w\_j} = \eta \sum\_i (t^{(i)} - o^{(i)})x^{(i)}\_{j},\]

从而有

\(w\_j := w\_j + \Delta w\_j,\)
其中 \(\eta\) 是学习率，\(t\) 是目标类别标签，\(o\) 是实际输出。
其他直观的例子还包括 K 最近邻（K-Nearest Neighbor）算法以及使用诸如欧氏距离这类距离度量的聚类算法——事实上，基于树的分类器可能是唯一一类特征缩放与否不会带来差别的分类器。

事实上，我能想到的唯一一族对尺度不变的算法就是基于树的方法。以通用的 CART 决策树算法为例。在不深入讨论信息增益和不纯度度量的前提下，我们可以把决策过程看成「特征 x_i 是否大于等于某个值？」直观上就能看出，这个特征处于什么尺度其实无关紧要（厘米、华氏度、标准化尺度——真的都无所谓）。

以下是一些特征缩放会对其产生影响的算法例子：

- 使用欧氏距离度量的 k 最近邻算法，如果我们希望所有特征都同等地做出贡献
- k 均值（k-means）聚类（参见 k 最近邻）
- 逻辑回归、SVM、感知器、神经网络等，如果你使用的是基于梯度下降/上升的优化方法，否则某些权重的更新会比其他权重快得多
- 线性判别分析、主成分分析、核主成分分析，因为你想找到使方差最大化的方向（约束条件是这些方向/特征向量/主成分相互正交）；你会希望特征处于同一尺度，因为否则你会更加强调那些「测量尺度更大」的变量。
  相关情形远不止我在这里能列出的这些……我总是建议你先想一想所用算法本身及其在做什么，这样通常就能明显看出我们是否需要对特征进行缩放。

此外，我们还需要考虑究竟想对数据进行「标准化」还是「归一化」（这里指缩放到 [0, 1] 区间）。有些算法假设我们的数据以 0 为中心。例如，如果我们将一个带 tanh 激活单元的小型多层感知器的权重初始化为 0，或者初始化为以零为中心的小随机值，我们就会希望「均等地」更新模型权重。作为一个经验法则，我会说：拿不准时，就直接对数据做标准化，这不会有坏处。

## 关于最小-最大缩放

z 分数归一化（即标准化）的一种替代方法是所谓的**最小-最大缩放**（Min-Max scaling，通常也被简单地称为「归一化」——这是造成术语歧义的一个常见原因）。
在这种方法中，数据被缩放到一个固定的范围——通常是 0 到 1。
与标准化相比，这种有界区间的代价是：我们最终会得到更小的标准差，而这可能会抑制离群点的影响。

最小-最大缩放通常通过以下方程实现：

\[X\_{norm} = \frac{X - X\_{min}}{X\_{max}-X\_{min}}\]

## z 分数标准化还是最小-最大缩放？

*「标准化还是最小-最大缩放？」*——这个问题没有显而易见的答案：它完全取决于具体应用。

例如，在聚类分析中，为了基于某些距离度量来比较特征之间的相似性，标准化可能尤为关键。另一个突出的例子是主成分分析（PCA），在这种情况下我们通常更倾向于标准化而非最小-最大缩放，因为我们感兴趣的是使方差最大化的那些成分（具体取决于所研究的问题，以及 PCA 是通过相关矩阵还是协方差矩阵来计算成分；[关于 PCA 的更多内容可参见我之前的文章](https://sebastianraschka.com/Articles/2014_pca_step_by_step.html)）。

不过，这并不意味着最小-最大缩放就毫无用处！一个流行的应用是图像处理，其中像素强度必须被归一化到某个特定范围之内（例如 RGB 颜色范围是 0 到 255）。此外，典型的神经网络算法要求数据处于 0-1 尺度上。

## 标准化与归一化——如何用 scikit-learn 实现

当然，我们可以利用 NumPy 的向量化能力，按照前面几节提到的公式计算用于标准化的 z 分数，并对数据进行归一化。不过，还有一种更为便捷的方法：使用 Python 开源机器学习库 [scikit-learn](http://scikit-learn.org) 中的 preprocessing 模块。

在下面的示例和讨论中，我们将使用托管在 UCI 机器学习仓库  
(http://archive.ics.uci.edu/ml/datasets/Wine) 上的免费「葡萄酒（Wine）」数据集。

> Forina, M. et al, PARVUS - An Extendible Package for Data
> Exploration, Classification and Correlation. Institute of Pharmaceutical
> and Food Analysis and Technologies, Via Brigata Salerno,
> 16147 Genoa, Italy.

> Bache, K. & Lichman, M. (2013). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.

葡萄酒数据集包含 3 个不同的类别，其中每一行对应一个特定的葡萄酒样本。

类别标签（1、2、3）列在第一列，第 2-14 列对应 13 个不同的属性（特征）：

1) 酒精（Alcohol）
2) 苹果酸（Malic acid）
……

### 加载葡萄酒数据集

```python
import pandas as pd
import numpy as np

df = pd.io.parsers.read_csv(
    'https://raw.githubusercontent.com/rasbt/pattern_classification/master/data/wine_data.csv',
     header=None,
     usecols=[0,1,2]
    )

df.columns=['Class label', 'Alcohol', 'Malic acid']

df.head()
```

|  | 类别标签 | 酒精 | 苹果酸 |
| --- | --- | --- | --- |
| 0 | 1 | 14.23 | 1.71 |
| 1 | 1 | 13.20 | 1.78 |
| 2 | 1 | 13.16 | 2.36 |
| 3 | 1 | 14.37 | 1.95 |
| 4 | 1 | 13.24 | 2.59 |

正如上表所示，特征**酒精**（Alcohol，体积百分比）和**苹果酸**（Malic acid，g/l）是在不同尺度上测量的，因此在对这些数据进行任何比较或组合之前，***特征缩放*** 都是必要且重要的。

### 标准化与最小-最大缩放

```python
from sklearn import preprocessing

std_scale = preprocessing.StandardScaler().fit(df[['Alcohol', 'Malic acid']])
df_std = std_scale.transform(df[['Alcohol', 'Malic acid']])

minmax_scale = preprocessing.MinMaxScaler().fit(df[['Alcohol', 'Malic acid']])
df_minmax = minmax_scale.transform(df[['Alcohol', 'Malic acid']])
```

```python
print('Mean after standardization:\nAlcohol={:.2f}, Malic acid={:.2f}'
      .format(df_std[:,0].mean(), df_std[:,1].mean()))
print('\nStandard deviation after standardization:\nAlcohol={:.2f}, Malic acid={:.2f}'
      .format(df_std[:,0].std(), df_std[:,1].std()))
```

```python
Mean after standardization:
Alcohol=0.00, Malic acid=0.00

Standard deviation after standardization:
Alcohol=1.00, Malic acid=1.00
```

```python
print('Min-value after min-max scaling:\nAlcohol={:.2f}, Malic acid={:.2f}'
      .format(df_minmax[:,0].min(), df_minmax[:,1].min()))
print('\nMax-value after min-max scaling:\nAlcohol={:.2f}, Malic acid={:.2f}'
      .format(df_minmax[:,0].max(), df_minmax[:,1].max()))
```

```python
Min-value after min-max scaling:
Alcohol=0.00, Malic acid=0.00

Max-value after min-max scaling:
Alcohol=1.00, Malic acid=1.00
```

### 绘图

```python
%matplotlib inline
```

```python
from matplotlib import pyplot as plt

def plot():
    plt.figure(figsize=(8,6))

    plt.scatter(df['Alcohol'], df['Malic acid'],
            color='green', label='input scale', alpha=0.5)

    plt.scatter(df_std[:,0], df_std[:,1], color='red',
            label='Standardized [$$N  (\mu=0, \; \sigma=1)$$]', alpha=0.3)

    plt.scatter(df_minmax[:,0], df_minmax[:,1],
            color='blue', label='min-max scaled [min=0, max=1]', alpha=0.3)

    plt.title('Alcohol and Malic Acid content of the wine dataset')
    plt.xlabel('Alcohol')
    plt.ylabel('Malic Acid')
    plt.legend(loc='upper left')
    plt.grid()

    plt.tight_layout()

plot()
plt.show()
```

![About standardization normalization about standardization normalization 44 0](https://sebastianraschka.com/images/blog/2014/about_standardization_normalization/about_standardization_normalization_44_0.webp)

上面的图中包含了三种不同尺度下的葡萄酒数据点：以体积百分比测量酒精含量的输入尺度（绿色）、标准化后的特征（红色），以及归一化后的特征（蓝色）。
在下面这张图中，我们将放大展示三种不同的坐标轴尺度。

```python
fig, ax = plt.subplots(3, figsize=(6,14))

for a,d,l in zip(range(len(ax)),
               (df[['Alcohol', 'Malic acid']].values, df_std, df_minmax),
               ('Input scale',
                'Standardized [$$N  (\mu=0, \; \sigma=1)$$]',
                'min-max scaled [min=0, max=1]')
                ):
    for i,c in zip(range(1,4), ('red', 'blue', 'green')):
        ax[a].scatter(d[df['Class label'].values == i, 0],
                  d[df['Class label'].values == i, 1],
                  alpha=0.5,
                  color=c,
                  label='Class %s' %i
                  )
    ax[a].set_title(l)
    ax[a].set_xlabel('Alcohol')
    ax[a].set_ylabel('Malic Acid')
    ax[a].legend(loc='upper left')
    ax[a].grid()

plt.tight_layout()

plt.show()
```

![About standardization normalization about standardization normalization 48 0](https://sebastianraschka.com/images/blog/2014/about_standardization_normalization/about_standardization_normalization_48_0.webp)

## 自底向上的实现方式

当然，我们也可以「手动地」编写标准化和 0-1 最小-最大缩放的公式代码。不过，如果你在处理测试集和训练集，并且希望对它们进行同等程度的缩放，那么 scikit-learn 的方法仍然很有用。

例如：

```python
std_scale = preprocessing.StandardScaler().fit(X_train)
X_train = std_scale.transform(X_train)
X_test = std_scale.transform(X_test)
```

下面，我们将使用「纯」Python 代码来执行这些计算，并给出一种更便捷的 NumPy 方案——当我们试图变换整个矩阵时，后者尤其有用。

先回顾一下我们所使用的公式：

标准化：

\[z = \frac{x - \mu}{\sigma}\]

其中均值为：

\[\mu = \frac{1}{N} \sum\_{i=1}^N (x\_i)\]

标准差为：

\[\sigma = \sqrt{\frac{1}{N} \sum\_{i=1}^N (x\_i - \mu)^2}\]

最小-最大缩放：

\[X\_{norm} = \frac{X - X\_{min}}{X\_{max}-X\_{min}}\]

### 纯 Python 实现

```python
# Standardization

x = [1,4,5,6,6,2,3]
mean = sum(x)/len(x)
std_dev = (1/len(x) * sum([ (x_i - mean)**2 for x_i in x]))**0.5

z_scores = [(x_i - mean)/std_dev for x_i in x]

# Min-Max scaling

minmax = [(x_i - min(x)) / (max(x) - min(x)) for x_i in x]
```

### NumPy 实现

```python
import numpy as np

# Standardization

x_np = np.asarray(x)
z_scores_np = (x_np - x_np.mean()) / x_np.std()

# Min-Max scaling

np_minmax = (x_np - x_np.min()) / (x_np.max() - x_np.min())
```

### 可视化

为了确保我们的代码运行正确，我们用 matplotlib 把结果绘制出来。

```python
from matplotlib import pyplot as plt

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(10,5))

y_pos = [0 for i in range(len(x))]

ax1.scatter(z_scores, y_pos, color='g')
ax1.set_title('Python standardization', color='g')

ax2.scatter(minmax, y_pos, color='g')
ax2.set_title('Python Min-Max scaling', color='g')

ax3.scatter(z_scores_np, y_pos, color='b')
ax3.set_title('Python NumPy standardization', color='b')

ax4.scatter(np_minmax, y_pos, color='b')
ax4.set_title('Python NumPy Min-Max scaling', color='b')

plt.tight_layout()

for ax in (ax1, ax2, ax3, ax4):
    ax.get_yaxis().set_visible(False)
    ax.grid()

plt.show()
```

![About standardization normalization about standardization normalization 64 0](https://sebastianraschka.com/images/blog/2014/about_standardization_normalization/about_standardization_normalization_64_0.webp)

## 标准化对模式分类任务中 PCA 的影响

前面我提到过主成分分析（PCA）是一个标准化至关重要的例子，因为它在「分析」不同特征的方差。
现在，让我们看看标准化会如何影响对整个葡萄酒数据集进行的 PCA，以及随后的监督分类。

在接下来的小节中，我们将依次完成以下步骤：

- 读取数据集
- 将数据集划分为独立的训练集和测试集
- 对特征进行标准化
- 通过主成分分析（PCA）降维
- 训练一个朴素贝叶斯分类器
- 评估有无标准化时的分类准确率

### 读取数据集

```python
import pandas as pd

df = pd.io.parsers.read_csv(
    'https://raw.githubusercontent.com/rasbt/pattern_classification/master/data/wine_data.csv',
    header=None,
    )
```

### 将数据集划分为独立的训练集和测试集

在这一步中，我们将随机地把葡萄酒数据集划分为一个训练集和一个测试集，其中训练集将包含 70% 的样本，测试集将包含 30% 的样本。

```python
from sklearn.cross_validation import train_test_split

X_wine = df.values[:,1:]
y_wine = df.values[:,0]

X_train, X_test, y_train, y_test = train_test_split(X_wine, y_wine,
    test_size=0.30, random_state=12345)
```

### 特征缩放——标准化

```python
from sklearn import preprocessing

std_scale = preprocessing.StandardScaler().fit(X_train)
X_train_std = std_scale.transform(X_train)
X_test_std = std_scale.transform(X_test)
```

### 通过主成分分析（PCA）进行降维

现在，我们对标准化和非标准化的数据集分别执行 PCA，将数据集变换到一个二维特征子空间上。
在实际应用中，人们会执行诸如交叉验证之类的流程，以找出什么样的特征选择能够在「保留信息」与「过拟合」之间为不同分类器取得最佳平衡。不过，我们将省略这一步，因为我们并不打算在这里训练一个完美的分类器，而只是想比较标准化的效果。

```python
from sklearn.decomposition import PCA

# on non-standardized data
pca = PCA(n_components=2).fit(X_train)
X_train = pca.transform(X_train)
X_test = pca.transform(X_test)

# om standardized data
pca_std = PCA(n_components=2).fit(X_train_std)
X_train_std = pca_std.transform(X_train_std)
X_test_std = pca_std.transform(X_test_std)
```

让我们快速可视化一下我们新的特征子空间是什么样子（注意，与线性判别分析不同，PCA 并不考虑类别标签——但为了清晰起见，我还是会在图中把它们标注出来）。

```python
from matplotlib import pyplot as plt

fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10,4))

for l,c,m in zip(range(1,4), ('blue', 'red', 'green'), ('^', 's', 'o')):
    ax1.scatter(X_train[y_train==l, 0], X_train[y_train==l, 1],
        color=c,
        label='class %s' %l,
        alpha=0.5,
        marker=m
        )

for l,c,m in zip(range(1,4), ('blue', 'red', 'green'), ('^', 's', 'o')):
    ax2.scatter(X_train_std[y_train==l, 0], X_train_std[y_train==l, 1],
        color=c,
        label='class %s' %l,
        alpha=0.5,
        marker=m
        )

ax1.set_title('Transformed NON-standardized training dataset after PCA')    
ax2.set_title('Transformed standardized training dataset after PCA')    

for ax in (ax1, ax2):

    ax.set_xlabel('1st principal component')
    ax.set_ylabel('2nd principal component')
    ax.legend(loc='upper right')
    ax.grid()
plt.tight_layout()

plt.show()
```

![About standardization normalization about standardization normalization 89 0](https://sebastianraschka.com/images/blog/2014/about_standardization_normalization/about_standardization_normalization_89_0.webp)

### 训练一个朴素贝叶斯分类器

我们将使用朴素贝叶斯分类器来完成这个分类任务。如果你对它不太熟悉，可以这么理解：「朴素」一词来自所有特征都相互「独立」这一假设。
总而言之，它是一个基于贝叶斯法则的简单而稳健的分类器：

贝叶斯法则：

\[P(\omega\_j|x) = \frac{p(x|\omega\_j) \* P(\omega\_j)}{p(x)}\]

其中

- ω：类别标签
- \[P(\omega | x): \text{posterior probability}\]
- \[p(x | \omega ): \text{prior probability (or likelihood)}\]

以及**决策规则：**

\[\text{Decide } \omega\_1 \text{ if } P(\omega\_1|x) > P(\omega\_2|x) \text{ else decide } \omega\_2.\]
\[\Rightarrow \frac{p(x|\omega\_1) \* P(\omega\_1)}{p(x)} > \frac{p(x|\omega\_2) \* P(\omega\_2)}{p(x)}\]

在这篇文章中，我不想更深入地讨论贝叶斯法则，但如果你对更详细的示例合集感兴趣，请看一看我的模式分类仓库中的[统计模式分类示例](https://github.com/rasbt/pattern_classification#statistical-pattern-recognition-examples)（Statistical Pattern Classification）。

```python
from sklearn.naive_bayes import GaussianNB

# on non-standardized data
gnb = GaussianNB()
fit = gnb.fit(X_train, y_train)

# on standardized data
gnb_std = GaussianNB()
fit_std = gnb_std.fit(X_train_std, y_train)
```

### 评估有无标准化时的分类准确率

```python
from sklearn import metrics

pred_train = gnb.predict(X_train)

print('\nPrediction accuracy for the training dataset')
print('{:.2%}'.format(metrics.accuracy_score(y_train, pred_train)))

pred_test = gnb.predict(X_test)

print('\nPrediction accuracy for the test dataset')
print('{:.2%}\n'.format(metrics.accuracy_score(y_test, pred_test)))
```

```python
Prediction accuracy for the training dataset
81.45%

Prediction accuracy for the test dataset
64.81%
```

```python
pred_train_std = gnb_std.predict(X_train_std)

print('\nPrediction accuracy for the training dataset')
print('{:.2%}'.format(metrics.accuracy_score(y_train, pred_train_std)))

pred_test_std = gnb_std.predict(X_test_std)

print('\nPrediction accuracy for the test dataset')
print('{:.2%}\n'.format(metrics.accuracy_score(y_test, pred_test_std)))
```

```python
Prediction accuracy for the training dataset
96.77%

Prediction accuracy for the test dataset
98.15%
```

正如我们所看到的，在 PCA 之前进行标准化，确实降低了在测试集样本分类上的经验错误率。

## 附录 A：PCA 之前变量缩放与均值中心化的影响

让我们思考一下：对于主成分分析（PCA）这类应用，如果 PCA 是从协方差矩阵计算得到的（即 \(k\) 个主成分是协方差矩阵中对应 \(k\) 个最大特征值的特征向量），那么变量是否做过中心化究竟有没有影响。

### 1. 均值中心化不影响协方差矩阵

这里的理由是：如果无论变量是否中心化，协方差都相同，那么 PCA 的结果也将相同。

假设我们有两个变量 \(\bf{x}\) 和 \(\bf{y}\)，那么属性之间的协方差按下式计算：

\[\sigma\_{xy} = \frac{1}{n-1} \sum\_{i}^{n} (x\_i - \bar{x})(y\_i - \bar{y})\]

我们把中心化后的变量写作：

\[x' = x - \bar{x} \text{ and } y' = y - \bar{y}\]

那么中心化后的协方差将按如下方式计算：

\[\sigma\_{xy}' = \frac{1}{n-1} \sum\_{i}^{n} (x\_i' - \bar{x}')(y\_i' - \bar{y}')\]

但由于中心化之后 \(\bar{x}' = 0\) 且 \(\bar{y}' = 0\)，我们有：

\(\sigma\_{xy}' = \frac{1}{n-1} \sum\_{i}^{n} x\_i' y\_i'\)，而如果把 \(x' = x - \bar{x} \text{ and } y' = y - \bar{y}\) 代回原项，这正是我们原来的协方差矩阵。

即使只中心化一个变量，例如 \(\bf{x}\)，也不会影响协方差：

\(\sigma\_{\text{xy}} = \frac{1}{n-1} \sum\_{i}^{n} (x\_i' - \bar{x}')(y\_i - \bar{y})\)
\(= \frac{1}{n-1} \sum\_{i}^{n} (x\_i' - 0)(y\_i - \bar{y})\)
\(= \frac{1}{n-1} \sum\_{i}^{n} (x\_i - \bar{x})(y\_i - \bar{y})\)

### 2. 变量缩放确实会影响协方差矩阵

如果对某个变量进行了缩放，例如从磅换算为千克（1 磅 = 0.453592 千克），这确实会影响协方差，进而影响 PCA 的结果。

设 \(c\) 为 \(\bf{x}\) 的缩放因子。

假定「原始」协方差按下式计算：

\[\sigma\_{xy} = \frac{1}{n-1} \sum\_{i}^{n} (x\_i - \bar{x})(y\_i - \bar{y})\]

那么缩放后的协方差将按如下方式计算：

\(\sigma\_{xy}' = \frac{1}{n-1} \sum\_{i}^{n} (c \cdot x\_i - c \cdot \bar{x})(y\_i - \bar{y})\)
\(= \frac{c}{n-1} \sum\_{i}^{n} (x\_i - \bar{x})(y\_i - \bar{y})\)

\(\Rightarrow \sigma\_{xy} = \frac{\sigma\_{xy}'}{c}\)
\(\Rightarrow \sigma\_{xy}' = c \cdot \sigma\_{xy}\)

因此，将一个属性按常数 \(c\) 缩放后，得到的将是重新缩放后的协方差 \(c \sigma\_{xy}\)。所以，如果我们把 \(\bf{x}\) 从磅缩放到千克，那么 \(\bf{x}\) 与 \(\bf{y}\) 之间的协方差将变为原来的 0.453592 倍。

### 3. 标准化会影响协方差

特征标准化会对 PCA 的结果产生影响（假设变量原本并未标准化）。这是因为我们用每一对变量标准差的乘积，缩放了每一对变量之间的协方差。

变量标准化的公式写作：

\[z = \frac{x\_i - \bar{x}}{\sigma}\]

「原始」协方差矩阵：

\[\sigma\_{xy} = \frac{1}{n-1} \sum\_{i}^{n} (x\_i - \bar{x})(y\_i - \bar{y})\]

在对两个变量都进行标准化之后：

\[x' = \frac{x - \bar{x}}{\sigma\_x} \text{ and } y' =\frac{y - \bar{y}}{\sigma\_y}\]
\[\sigma\_{xy}' = \frac{1}{n-1} \sum\_{i}^{n} (x\_i' - 0)(y\_i' - 0)\]
\[= \frac{1}{n-1} \sum\_{i}^{n} \bigg(\frac{x - \bar{x}}{\sigma\_x}\bigg)\bigg(\frac{y - \bar{y}}{\sigma\_y}\bigg)\]
\[= \frac{1}{(n-1) \cdot \sigma\_x \sigma\_y} \sum\_{i}^{n} (x\_i - \bar{x})(y\_i - \bar{y})\]
\[\Rightarrow \sigma\_{xy}' = \frac{\sigma\_{xy}}{\sigma\_x \sigma\_y}\]
