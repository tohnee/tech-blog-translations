---
title: "Python 中的核密度估计（KDE）"
title_en: "Kernel Density Estimation (KDE) in Python"
source: https://sebastianraschka.com/Articles/2014_kernel_density_est.html
crawled: 2026-09-06
translated: 2026-09-14
---

# Python 中的核密度估计（KDE）

> 原文：[Kernel Density Estimation (KDE) in Python](https://sebastianraschka.com/Articles/2014_kernel_density_est.html) · Sebastian Raschka's Articles

Parzen 窗方法（Parzen-window method，也称为 Parzen-Rosenblatt 窗方法）是一种广泛使用的非参数方法，用于从样本 *p(**x**n)* 中估计特定点 *p(**x**)* 的概率密度函数 *p(**x**)*，而且不需要对底层分布有任何了解或假设。

![Parzen rosenblatt parzen goal](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_goal.webp)

=================

## 1 引言

Parzen 窗方法（Parzen-window method，也称为 Parzen-Rosenblatt 窗方法）是一种广泛使用的非参数方法，用于从样本 *p(**x**n)* 中估计特定点 *p(**x**)* 的概率密度函数 *p(**x**)*，而且不需要对底层分布有任何了解或假设。

**放入具体语境——这种方法在哪些场景下有用？**

Parzen 窗技术的一个流行应用，是在监督模式分类问题中从训练数据集估计类条件密度（class-conditional densities，也常被称为「似然」）*p(**x** | ωi)*（其中 *p(**x**)* 指的是属于特定类别 *ωi* 的多维样本）。

设想我们要使用贝叶斯规则设计一个贝叶斯分类器，来解决一个统计模式分类任务：

![Parzen rosenblatt parzen bayes rule](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_bayes_rule.webp)

如果*类条件密度*（class-conditional densities，也称为*似然*）的参数是已知的，那么设计分类器就相当容易了。我在 [Parametric Approaches](https://github.com/rasbt/pattern_classification#param) 章节下用 IPython notebook 解决了一些简单的例子。

---

**关于数学记号：**

在整篇文章中，我将采用大多数线性代数教科书使用的通用矩阵记号：

- 斜体粗体小写字母（例如 ***x***）表示向量
- 斜体粗体大写字母（例如 ***A***）表示矩阵
- 用下标按行和列来引用元素（例如 \(A\_{ij}\) 表示第 *i* 行第 *j* 列的单元格）

  ---

然而，如果我们对定义数据模型的底层参数没有任何先验知识，问题就会变得更具挑战性。

设想我们要为一个模式分类任务设计分类器，而底层样本分布的参数是未知的。此时，我们并不需要掌握整个分布的知识；只需知道我们想要分类的那个特定点的概率，就足以做出决策了。接下来我们就会看到，如何从训练样本中估计这个概率。

不过，这个方法唯一的问题在于：只要考察一下任意一个训练数据集的频数直方图，就会发现我们几乎不可能拿到精确值。因此，我们在特定值周围定义一个*区域*（即 **Parzen 窗**）来做估计。

**那么 *Parzen 窗*这个名字究竟是怎么来的呢？**

在早期这是相当普遍的做法：这项技术以它的发明者 Emanuel Parzen 的名字命名，他于 1962 年在 [the Annals of Mathematical Statistics](http://ssg.mit.edu/cal/abs/2000_spring/np_dens/density-estimation/parzen62.pdf) 上发表了对此方法的详细数学分析 [1]。大约在同一时间，另一位统计学家 Murray Rosenblatt [2] 独立于 Parzen 发现（或者说发展了）这一技术，因此该方法有时也被称为 Parzen-Rosenblatt 窗方法。

---

> [1] *Parzen, Emanuel*. On Estimation of a Probability Density Function
> and Mode. The Annals of Mathematical Statistics 33 (1962), no. 3,
> 1065–1076.
> [doi:10.1214/aoms/1177704472.](http://projecteuclid.org/euclid.aoms/1177704472)

> [2] *Rosenblatt, Murray*. Remarks on Some Nonparametric Estimates of a
> Density Function. The Annals of Mathematical Statistics 27 (1956), no.
> 3, 832–837.
> [doi:10.1214/aoms/1177728190.](http://projecteuclid.org/euclid.aoms/1177728190)

## 2 定义区域 Rn

这种方法的基础，是统计有多少样本落入某个指定区域 \(R\_{n}\)（或者你愿意的话，可以称之为「窗口」）。直觉告诉我们（基于观察），一个样本落入该区域的概率为

![Parzen rosenblatt parzen eq 01](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_01.webp)

为了从更数学的角度来处理这个问题——估计「在区域 ***R*** 中观察到 n 个点中的 *k* 个点的概率」——我们考虑一个二项分布

![Parzen rosenblatt parzen eq 02](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_02.webp)

并做出这样的假设：在二项分布中，概率在均值处急剧达到峰值，因此有：

![Parzen rosenblatt parzen eq 03](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_03.webp)

而如果我们把概率看作一个连续变量，我们知道它的定义为：

![Parzen rosenblatt parzen eq 04](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_04.webp)

其中 *V* 是区域 ***R*** 的体积。如果把这些项重新整理，就得到下面这个方程，我们后面会用到它：

![Parzen rosenblatt parzen eq 05](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_05.webp)

上面这个简单的方程（即「概率估计」）让我们能够通过统计有多少个点 *k* 落在某个定义好的区域（或体积）内，来计算点 ***x*** 的概率密度。

### 2.1 两种不同的方法——固定体积 vs. 固定样本数而体积可变

估计不同点 \(p(\mathbf{x})\) 处的密度，有两种可行的方法。

#### 情形 1——固定体积：

对于一个特定的数目 *n*（= 总点数），我们使用固定大小的体积 *V*，并观察有多少个点 *k* 落入该区域。换句话说，我们使用同一个体积在不同的区域做估计。

**Parzen 窗技术就属于这一类！**

![Parzen rosenblatt parzen case1](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_case1.webp)

#### 情形 2——固定 *k*：

对于一个特定的数目 *n*（= 总点数），我们使用固定的数目 *k*（落入区域或体积内的点数），并相应地调整体积。
（**k 最近邻（k-nearest neighbor）技术采用的就是这种方法，它将在另一篇文章中讨论。**）

![Parzen rosenblatt parzen case2](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_case2.webp)

### 2.2 3D 超立方体示例

为了用一个例子和一组方程来说明这一点，我们假设区域 *Rn* 是一个超立方体。
这个超立方体的体积由 *Vn = hnd* 定义，其中 hn 是超立方体的边长，*d* 是维度数。
例如，对于边长为 1 的 2D 超立方体，就是 *V1 = 12*；而对于 3D 超立方体，则相应地为 *V\_1 = 13*。

那么让我们来可视化这样一个简单的例子：一个典型的 3 维单位超立方体（*h1 = 1*）表示区域 *R1*，以及 10 个样本点，其中 3 个位于超立方体内（红色三角形），另外 7 个位于超立方体外（蓝色点）。

**请注意，在实际应用中使用超立方体并不是一个理想的选择，但它确实能让后续步骤的实现简短得多、也容易理解得多**。

```python
%matplotlib inline

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations
fig = plt.figure(figsize=(7,7))
ax = fig.gca(projection='3d')
ax.set_aspect("equal")

# Plot Points

# samples within the cube
X_inside = np.array([[0,0,0],[0.2,0.2,0.2],[0.1, -0.1, -0.3]])

X_outside = np.array([[-1.2,0.3,-0.3],[0.8,-0.82,-0.9],[1, 0.6, -0.7],
                  [0.8,0.7,0.2],[0.7,-0.8,-0.45],[-0.3, 0.6, 0.9],
                  [0.7,-0.6,-0.8]])

for row in X_inside:
    ax.scatter(row[0], row[1], row[2], color="r", s=50, marker='^')

for row in X_outside:
    ax.scatter(row[0], row[1], row[2], color="k", s=50)

# Plot Cube
h = [-0.5, 0.5]
for s, e in combinations(np.array(list(product(h,h,h))), 2):
    if np.sum(np.abs(s-e)) == h[1]-h[0]:
        ax.plot3D(*zip(s,e), color="g")

ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(-1.5, 1.5)

plt.show()
```

![Parzen rosenblatt parzen plot1](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_plot1.webp)

### 2.3 窗函数

像上面那样把区域 ***R1*** 可视化之后，统计有多少样本落在这个区域内、多少落在区域外，就变得简单而直观。为了从更数学的角度来处理这个问题，我们会使用下面的方程来统计超立方体内的样本数 *kn*，其中 *φ* 就是我们所谓的*窗函数*

![Parzen rosenblatt parzen eq 06](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_06.webp)

它针对的是边长为单位长度 1、以坐标系原点为中心的超立方体。

这个函数的基本作用是：如果样本点落在超立方体边长的 1/2 范围之内，就为它赋值 1；如果落在范围之外，则赋值 0（注意，这一判断要对样本点的所有维度进行）。

如果我们推广这个概念，就可以定义一个更一般的方程，它适用于以 **x** 为中心、边长为任意 *hn* 的超立方体：

![Parzen rosenblatt parzen eq 07](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_07.webp)

#### 2.3.1 实现窗函数

```python
def window_function(x_vec, unit_len=1):
"""
Implementation of the window function. Returns 1 if 3x1-sample vector
lies within a origin-centered hypercube, 0 otherwise.

"""
for row in x_vec:
    if np.abs(row) > (unit_len/2):
        return 0
return 1
```

#### 2.3.2 统计 3D 超立方体内的样本点

使用我们刚刚在上面实现的*窗函数*，现在让我们来统计一下到底有多少点位于超立方体内部、多少位于外部。

```python
X_all = np.vstack((X_inside,X_outside))
assert(X_all.shape == (10,3))

k_n = 0
for row in X_all:
    k_n += window_function(row.reshape(3,1))

print('Points inside the hypercube:', k_n)
print('Points outside the hybercube:', len(X_all) - k_n)
```

```python
Points inside the hypercube: 3
Points outside the hypercube: 7
```

### 2.4 Parzen 窗估计

基于上一节中定义的窗函数，我们现在可以按如下方式写出使用超立方体核的 Parzen 窗估计：

![Parzen rosenblatt parzen eq 08](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_08.webp)

把它应用到上面单位超立方体的例子中（10 个样本中有 3 个落在超立方体内，即区域 *R* 内），我们就可以按如下方式计算样本 ***x*** 落入区域 *R* 的概率 *p(**x**)*：

![Parzen rosenblatt parzen eq 09](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_09.webp)

### 2.5 关键假设：收敛性

Parzen 窗技术（以及 k 最近邻技术）之所以成立，最关键的假设之一是：当我们假设训练样本数量为无穷多时，*pn*（其中下标 *n* 表示「样本数量」）会收敛到真实密度 *p(**x**)*。Emanuel Parzen 在他的[论文](http://ssg.mit.edu/cal/abs/2000_spring/np_dens/density-estimation/parzen62.pdf)中对此给出了漂亮的证明。

### 2.6 Parzen 窗技术的关键参数：窗宽与核

Parzen 窗技术有两个关键参数：

- 1) 窗宽（window width）
- 2) 核（kernel）

**1) 窗宽：**  
这部分我们先跳过，稍后会通过一个动手实例来讨论和探索如何选择合适的窗宽。

**2) 核**：  
最常见的情况是，窗函数要么使用超立方体核，要么使用高斯核。但我们怎么知道哪个更好呢？这实际上取决于训练样本。在实践中，通常的做法是对得到的模式分类器进行测试，看哪种方法在测试数据集上带来更好的性能。
直觉上，对于一个服从高斯分布的数据集，使用高斯核是合理的。**但请记住，Parzen 窗估计的整个目的，就是要估计一个未知分布的密度！**所以实践中我们并不知道数据是否来自高斯分布（否则我们就不用做估计了，而可以直接使用 MLE 或贝叶斯估计这类参数化技术）。
如果我们决定用高斯核来代替超立方体，只需简单地把上面为超立方体定义的窗函数的表达式替换为：

![Parzen rosenblatt parzen eq 10](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_10.webp)

此时 Parzen 窗估计就会变成这样：

![mixing different kernels:](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_11.webp)

**混合使用不同的核：**  
在一些论文中你会看到，作者混合使用超立方体核和高斯核来估计不同区域的密度。在实践中，这样做可能效果很好，但要注意，在理论上这会违背一条基本原理：密度的积分等于 1。

![Parzen rosenblatt parzen eq 12](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_12.webp)

- 另外几条要求是：在极限情况下，我们为 Parzen 窗选择的体积要变得无穷小。

![Parzen rosenblatt parzen eq 13](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_13.webp)

- 该区域内的点数 *kn* 收敛于：

![Parzen rosenblatt parzen eq 14](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_14.webp)

- 由此我们可以得出：

![Parzen rosenblatt parzen eq 15](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_15.webp)

### 2.7 实现 Parzen 窗估计

接下来，让我们进入更有趣的部分，实现超立方体核的代码：

```python
def parzen_window_est(x_samples, h=1, center=[0,0,0]):
    '''
    Implementation of the Parzen-window estimation for hypercubes.

    Keyword arguments:
        x_samples: A 'n x d'-dimensional numpy array, where each sample
            is stored in a separate row.
        h: The length of the hypercube.
        center: The coordinate center of the hypercube

    Returns the probability density for observing k samples inside the hypercube.

    '''
    dimensions = x_samples.shape[1]

    assert (len(center) == dimensions),  
            'Number of center coordinates have to match sample dimensions'
    k = 0
    for x in x_samples:
        is_inside = 1
        for axis,center_point in zip(x, center):
            if np.abs(axis-center_point) > (h/2):
                is_inside = 0
        k += is_inside
    return (k / len(x_samples)) / (h**dimensions)

print('p(x) =', parzen_window_est(X_all, h=1))
```

```python
    p(x) = 0.3
```

**说到这里，如果你稍微有点跟不上整体脉络，我完全能够理解。我在后面的章节中[总结了三个关键部分](#51-summarizing-the-implementation-of-the-parzen-window-estimation-with-a-hypercube-kernel)（超立方体核、窗函数以及最终的 Parzen 窗估计），我认为在下面把它应用到数据集之前，值得先快速看一眼。**

## 3 将 Parzen 窗方法应用于一个随机的多元高斯数据集

让我们使用一个从多元高斯分布中抽取的 2 维数据集，来实际应用 Parzen 窗技术进行密度估计。

### 3.1 从高斯分布生成 10000 个随机 2D 样本

一般的多元高斯概率密度函数（pdf）定义为：

![Parzen rosenblatt parzen eq 16](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_16.webp)

我们将使用以下参数来抽取随机样本：

![Parzen rosenblatt parzen eq 17](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_17.webp)

```python
import numpy as np

# Generate 10,000 random 2D-patterns
mu_vec = np.array([0,0])
cov_mat = np.array([[1,0],[0,1]])
x_2Dgauss = np.random.multivariate_normal(mu_vec, cov_mat, 10000)

print(x_2Dgauss.shape)
```

```python
(10000, 2)
```

```python
#from matplotlib import pyplot as plt

f, ax = plt.subplots(figsize=(7, 7))
ax.scatter(x_2Dgauss[:,0], x_2Dgauss[:,1],
        marker='o', color='green', s=4, alpha=0.3)
plt.title('10000 samples randomly drawn from a 2D Gaussian distribution')
plt.ylabel('x2')
plt.xlabel('x1')
ftext = 'p(x) ~ N(mu=(0,0)^t, cov=I)'
plt.figtext(.15,.85, ftext, fontsize=11, ha='left')
plt.ylim([-4,4])
plt.xlim([-4,4])

plt.show()
```

![Parzen rosenblatt parzen plot2](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_plot2.webp)

### 3.2 实现并绘制多元高斯密度函数

#### 3.2.1 绘制二元高斯密度

首先，让我们用 3D 图来绘制多元高斯分布（这里是二元）的图形，以便对实际的密度分布有更好的认识。

```python
#import numpy as np
#from matplotlib import pyplot as plt

from matplotlib.mlab import bivariate_normal
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 7))
ax = fig.gca(projection='3d')
x = np.linspace(-5, 5, 200)
y = x
X,Y = np.meshgrid(x, y)
Z = bivariate_normal(X, Y)
surf = ax.plot_surface(X, Y, Z, rstride=1,
        cstride=1, cmap=plt.cm.coolwarm,
        linewidth=0, antialiased=False
    )

ax.set_zlim(0, 0.2)
ax.zaxis.set_major_locator(plt.LinearLocator(10))
ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.02f'))

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('p(x)')

plt.title('Bivariate Gaussian distribution')
fig.colorbar(surf, shrink=0.5, aspect=7, cmap=plt.cm.coolwarm)

plt.show()
```

![Parzen rosenblatt parzen plot3](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_plot3.webp)

#### 3.2.2 实现计算多元高斯密度的代码

为了根据多元高斯密度函数计算概率，并将结果与我们的估计进行比较，让我们按照下面的方程来实现它：

![Parzen rosenblatt parzen eq 18](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_18.webp)

遗憾的是，目前还没有 Python 库提供这一功能。好消息是，`scipy.stats.multivariate_normal.pdf()` 将在 `scipy` 的新候选版本（v. 0.14）中得到实现。

```python
#import numpy as np

def pdf_multivariate_gauss(x, mu, cov):
    '''
    Caculate the multivariate normal density (pdf)

    Keyword arguments:
        x = numpy array of a "d x 1" sample vector
        mu = numpy array of a "d x 1" mean vector
        cov = "numpy array of a d x d" covariance matrix
    '''
    assert(mu.shape[0] > mu.shape[1]),\
        'mu must be a row vector'
    assert(x.shape[0] > x.shape[1]),\
        'x must be a row vector'
    assert(cov.shape[0] == cov.shape[1]),\
        'covariance matrix must be square'
    assert(mu.shape[0] == cov.shape[0]),\
        'cov_mat and mu_vec must have the same dimensions'
    assert(mu.shape[0] == x.shape[0]),\
        'mu and x must have the same dimensions'

    part1 = 1 / ( ((2* np.pi)**(len(mu)/2)) * (np.linalg.det(cov)**(1/2)) )
    part2 = (-1/2) * ((x-mu).T.dot(np.linalg.inv(cov))).dot((x-mu))
    return float(part1 * np.exp(part2))
```

##### 3.2.2.1 测试多元高斯 PDF 的实现

让我们通过将它与 matplotlib.mlab 包中的二元高斯进行比较，快速确认我们刚刚实现的多元高斯符合预期。

```python
from matplotlib.mlab import bivariate_normal

x = np.array([[0],[0]])
mu = np.array([[0],[0]])
cov = np.eye(2)

mlab_gauss = bivariate_normal(x,x)
mlab_gauss = float(mlab_gauss[0]) # because mlab returns an np.array
impl_gauss = pdf_multivariate_gauss(x, mu, cov)

print('mlab_gauss:', mlab_gauss)
print('impl_gauss:', impl_gauss)
assert(mlab_gauss == impl_gauss),\
        'Implementations of the mult. Gaussian return different pdfs'
```

```python
mlab_gauss: 0.15915494309189535
impl_gauss: 0.15915494309189535
```

#### 3.2.3 将 Parzen 窗估计与真实密度进行比较

最后，让我们把用自己实现的 Parzen 窗估计得到的密度与真实的多元高斯密度做个比较。

但在比较之前，我们还必须先问自己一个问题：应该选择多大的窗口尺寸（即超立方体的边长 h 应该是多少）？窗宽是训练样本数量的函数，

![Parzen rosenblatt parzen eq 19](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_19.webp)

但为什么是 √n，而不直接用 *n* 呢？

这是因为窗口内点数 *kn* 的增长速度要远小于训练样本数量的增长速度，尽管

![Parzen rosenblatt parzen eq 20](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_20.webp)

我们仍有：*k < n*

这也是 Parzen 窗技术最大的缺点之一：在实践中，训练数据的数量通常（过于）小，这使得选择「最优」窗口尺寸变得困难。

**在实践中，人们会尝试不同的窗宽，并分析哪一个能让所得分类器获得最佳性能。**我们仅有的指导原则是：假设「最优」窗宽会随着训练样本数量的增加而缩小。

如果我们选择的窗宽「太小」，会导致密度出现局部尖峰；而窗宽「太大」则会对整个分布做平均。下面我用一个 1D 样本来尝试说明这一点。

![Parzen rosenblatt parzen window width](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_window_width.webp)

在[后面的章节](#26-critical-parameters-of-the-parzen-window-technique-window-width-and-kernel)中，我们会看看它在我们这个示例数据上是什么样子：

![Parzen rosenblatt parzen window effect](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_window_effect.webp)

##### 3.2.3.1 选择合适的窗口尺寸

在我们的例子中，我们幸运地知道数据的分布，因此让我们看看几种可能的窗宽，观察它们如何影响分布在中心点处的密度估计
（根据上一节的测试，我们期望得到接近 *p(***x***) = 0.1592* 的值）。

```python
print('Predict p(x) at the center [0,0]: ')

print('h = 0.1 ---> p(x) =', parzen_window_est(
        x_2Dgauss, h=0.1, center=[0, 0])
        )
print('h = 0.3 ---> p(x) =',parzen_window_est(
        x_2Dgauss, h=0.3, center=[0, 0])
        )
print('h = 0.6 ---> p(x) =',parzen_windo    w_est(
        x_2Dgauss, h=0.6, center=[0, 0])
        )
print('h = 1 ---> p(x) =',parzen_window_est(
        x_2Dgauss, h=1, center=[0, 0])
        )
```

```python
Predict p(x) at the center [0,0]:
h = 0.1 ---> p(x) = 0.17999999999999997
h = 0.3 ---> p(x) = 0.1766666666666667
h = 0.6 ---> p(x) = 0.15694444444444444
h = 1 ---> p(x) = 0.1475
```

上面这个粗略的估计，让我们对什么样的窗口尺寸能给出相当合理的估计有了一些概念：\(h\) 的合适取值应该在 0.6 附近。

但我们还可以做得更好（也许我在这里应该用一种最小化算法，不过我认为这个例子已经足以说明整个流程了）。让我们为 *h* 在 (0,1) 之间创建 400 个均匀间隔的取值，看看哪一个能给出分布中心处概率的最佳估计。

```python
import operator

# generate a range of 400 window widths between 0 < h < 1
h_range = np.linspace(0.001, 1, 400)

# calculate the actual density at the center [0, 0]
mu = np.array([[0],[0]])
cov = np.eye(2)
actual_pdf_val = pdf_multivariate_gauss(np.array([[0],[0]]), mu, cov)

# get a list of the differnces (|estimate-actual|) for different window widths
parzen_estimates = [np.abs(parzen_window_est(x_2Dgauss, h=i, center=[0, 0])
               - actual_pdf_val) for i in h_range]

# get the window width for which |estimate-actual| is closest to 0
min_index, min_value = min(enumerate(parzen_estimates), key=operator.itemgetter(1))

print('Optimal window width for this data set: ', h_range[min_index])
```

```python
Optimal window width for this data set:  0.554330827068
```

##### 3.2.3.2 估计密度 vs. 真实密度

现在我们有了「合适的」窗宽，让我们在一些示例点上比较估计值和真实密度。

```python
import prettytable

p1 = parzen_window_est(x_2Dgauss, h=h_range[min_index], center=[0, 0])
p2 = parzen_window_est(x_2Dgauss, h=h_range[min_index], center=[0.5, 0.5])
p3 = parzen_window_est(x_2Dgauss, h=h_range[min_index], center=[0.3, 0.2])

mu = np.array([[0],[0]])
cov = np.eye(2)

a1 = pdf_multivariate_gauss(np.array([[0],[0]]), mu, cov)
a2 = pdf_multivariate_gauss(np.array([[0.5],[0.5]]), mu, cov)
a3 = pdf_multivariate_gauss(np.array([[0.3],[0.2]]), mu, cov)

results = prettytable.PrettyTable(["", "predicted", "actual"])
results.add_row(["p([0,0]^t",p1, a1])
results.add_row(["p([0.5,0.5]^t",p2, a2])
results.add_row(["p([0.3,0.2]^t",p3, a3])

print(results)
```

```python
+---------------+----------------+---------------------+
|               |   predicted    |        actual       |
+---------------+----------------+---------------------+
|   p([0,0]^t   | 0.159151557695 | 0.15915494309189535 |
| p([0.5,0.5]^t | 0.122208992134 | 0.12394999430965298 |
| p([0.3,0.2]^t | 0.150755520068 | 0.14913891880709737 |
+---------------+----------------+---------------------+
```

正如我们在上表中看到的，我们的预测效果相当不错！

##### 3.2.3.3 绘制估计得到的二元高斯密度

最后同样重要的是，让我们绘制使用超立方体的 Parzen 窗技术所预测的密度。

```python
#import numpy as np
#from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

##############################################
### Predicted bivariate Gaussian densities ###
##############################################

fig = plt.figure(figsize=(10, 7))
ax = fig.gca(projection='3d')

X = np.linspace(-5, 5, 100)
Y = np.linspace(-5, 5, 100)
X,Y = np.meshgrid(X,Y)

Z = []
for i,j in zip(X.ravel(),Y.ravel()):
    Z.append(parzen_window_est(x_2Dgauss, h=h_range[min_index], center=[i, j]))

Z = np.asarray(Z).reshape(100,100)
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.cm.coolwarm,
        linewidth=0, antialiased=False)

ax.set_zlim(0, 0.2)

ax.zaxis.set_major_locator(plt.LinearLocator(10))
ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.02f'))

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('p(x)')

plt.title('Predicted bivariate Gaussian densities')

fig.colorbar(surf, shrink=0.5, aspect=7, cmap=plt.cm.coolwarm)

###########################################
### Actual bivariate Gaussian densities ###
###########################################

fig = plt.figure(figsize=(10, 7))
ax = fig.gca(projection='3d')
x = np.linspace(-5, 5, 100)
y = x
X,Y = np.meshgrid(x, y)
Z = bivariate_normal(X, Y)
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.cm.coolwarm,
       linewidth=0, antialiased=False)

ax.set_zlim(0, 0.2)

ax.zaxis.set_major_locator(plt.LinearLocator(10))
ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.02f'))

fig.colorbar(surf, shrink=0.5, aspect=7, cmap=plt.cm.coolwarm)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('p(x)')

plt.title('Actual bivariate Gaussian densities')

plt.show()
```

![Parzen rosenblatt parzen pred vs actual1](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_pred_vs_actual1.webp)

![Parzen rosenblatt parzen pred vs actual2](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_pred_vs_actual2.webp)

## 4 Parzen 窗技术的结论与缺点

正如我们在上面两幅图中看到的（估计的与真实的二元高斯概率分布），我们能够相当不错地估计高斯密度。

**计算与性能**

Parzen 窗技术最大的缺点之一是：我们必须**保留训练数据集**，才能估计（计算）概率密度。例如，如果我们设计一个贝叶斯分类器，并使用 Parzen 窗技术来估计类条件概率密度 *p(**x**i | ωj)*，那么对每一个点做估计时，计算任务都需要用到整个训练数据集

- 这是非参数方法普遍存在的一个缺点。
  相比之下，参数化方法（例如最大似然估计（MLE）或贝叶斯估计（BE））只需要训练数据来计算参数值。一旦从训练数据集得到了参数，训练数据集就可以丢弃，而且在分类测试数据集中的数据时无需重新计算。不过，在贝叶斯学习（BL）中，还可以纳入新样本来改进估计出的参数值。

**训练数据集的规模**

由于 Parzen 窗技术是基于训练数据集来估计概率密度的，它也依赖规模合理的训练样本才能做出「好」的估计。粗略地说，训练数据集中的训练样本越多，估计就越准确（中心极限定理），因为我们降低了在局部区域遭遇点稀疏的可能性——前提是我们的训练样本是 *i.i.d*（**独**立抽取且**同**分布，independently drawn and identically distributed）的。然而另一方面，正如上一节所讨论的，更多的训练样本也会导致计算性能的下降。

**选择合适的窗宽**

选择合适的窗宽是一项非常具有挑战性的任务，因为我们对训练数据的分布一无所知（否则非参数方法就没有存在的必要了）。因此，我们必须在模式分类任务中通过分析所得分类器的性能来评估不同的窗宽，并把假设

![Parzen rosenblatt parzen eq 21](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_21.webp)

作为指导原则。

**选择核**

最常见的是为 Parzen 窗函数 φ 选择超立方体核或高斯核。然而，事先无法判断哪种核能对概率密度给出更好的估计，因为我们在使用 Parzen 窗技术时假设对底层分布一无所知。与选择合适的窗宽类似，我们也必须通过评估所得分类器的性能，才能做出切合实际的选择。

## 5 用高斯核替换超立方体

完成上面的例子之后，我们使用超立方体核估计了二元高斯分布的概率密度，我们的 Parzen 窗估计是通过下面的方程实现的：

![Parzen rosenblatt parzen eq 22](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_22.webp)

现在，让我们在 Parzen 窗估计中改用高斯核，于是方程变为：

![Parzen rosenblatt parzen eq 23](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_23.webp)

其中

![Parzen rosenblatt parzen eq 24](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_24.webp)

把它应用到上面单位超立方体的例子中（10 个样本中有 3 个落在超立方体即区域 *R* 内），我们就可以按如下方式计算样本 ***x*** 落入区域 ***R*** 的概率 *p(***x***)*：

![Parzen rosenblatt parzen eq 25](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_25.webp)

### 5.1 总结使用超立方体核的 Parzen 窗估计的实现

让我们快速总结一下我们是如何为超立方体实现 Parzen 窗估计的。

```python
def hypercube_kernel(h, x, x_i):
    """
    Implementation of a hypercube kernel for Parzen-window estimation.

    Keyword arguments:
        h: window width
        x: point x for density estimation, 'd x 1'-dimensional numpy array
        x_i: point from training sample, 'd x 1'-dimensional numpy array

    Returns a 'd x 1'-dimensional numpy array as input for a window function.

    """
    assert (x.shape == x_i.shape), 'vectors x and x_i must have the same dimensions'
    return (x - x_i) / (h)

def parzen_window_func(x_vec, h=1):
    """
    Implementation of the window function. Returns 1 if 'd x 1'-sample vector
    lies within inside the window, 0 otherwise.

    """
    for row in x_vec:
        if np.abs(row) > (1/2):
            return 0
    return 1

def parzen_estimation(x_samples, point_x, h, d, window_func, kernel_func):
    """
    Implementation of a parzen-window estimation.

    Keyword arguments:
        x_samples: A 'n x d'-dimensional numpy array, where each sample
            is stored in a separate row. (= training sample)
        point_x: point x for density estimation, 'd x 1'-dimensional numpy array
        h: window width
        d: dimensions
        window_func: a Parzen window function (phi)
        kernel_function: A hypercube or Gaussian kernel functions

    Returns the density estimate p(x).

    """
    k_n = 0
    for row in x_samples:
        x_i = kernel_func(h=h, x=point_x, x_i=row[:,np.newaxis])
        k_n += window_func(x_i, h=h)
    return (k_n / len(x_samples)) / (h**d)
```

让我们回到那个超立方体的例子：3 个点位于超立方体内，7 个点位于超立方体外，我们为中心处边长为 1 的单位超立方体给出的密度估计是 *p(***x***) = 0.3*。

```python
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations
fig = plt.figure(figsize=(7,7))
ax = fig.gca(projection='3d')
ax.set_aspect("equal")

# Plot Points

# samples within the cube
X_inside = np.array([[0,0,0],[0.2,0.2,0.2],[0.1, -0.1, -0.3]])

X_outside = np.array([[-1.2,0.3,-0.3],[0.8,-0.82,-0.9],[1, 0.6, -0.7],
                  [0.8,0.7,0.2],[0.7,-0.8,-0.45],[-0.3, 0.6, 0.9],
                  [0.7,-0.6,-0.8]])

for row in X_inside:
    ax.scatter(row[0], row[1], row[2], color="r", s=50, marker='^')

for row in X_outside:
    ax.scatter(row[0], row[1], row[2], color="k", s=50)

# Plot Cube
h = [-0.5, 0.5]
for s, e in combinations(np.array(list(product(h,h,h))), 2):
    if np.sum(np.abs(s-e)) == h[1]-h[0]:
        ax.plot3D(*zip(s,e), color="g")

ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(-1.5, 1.5)

plt.show()
```

![Parzen rosenblatt parzen plot4](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_plot4.webp)

现在我们可以使用带超立方体核的 `parzen_estimation()` 函数来计算 *p(***x**)*。

```python
point_x = np.array([[0],[0],[0]])

print('p(x) =', parzen_estimation(X_all, point_x, h=1, d=3,
                                 window_func=parzen_window_func,
                                 kernel_func=hypercube_kernel
                                 )
     )
```

```python
p(x) = 0.3
```

**再让我们快速确认一下，它在一个更大的数据集上、对于不以原点为中心的非单位超立方体也能正常工作：**
（注意，我只是为 *h* 任选了一个长度，它很可能不是 *h* 的最佳选择。）

```python
import numpy as np

# Generate 10000 random 2D-patterns
mu_vec = np.array([0,0])
cov_mat = np.array([[1,0],[0,1]])
x_2Dgauss = np.random.multivariate_normal(mu_vec, cov_mat, 10000)
```

```python
import prettytable

p1 = parzen_estimation(x_2Dgauss, np.array([[0],[0]]), h=0.3, d=2,
                                 window_func=parzen_window_func,
                                 kernel_func=hypercube_kernel)
p2 = parzen_estimation(x_2Dgauss, np.array([[0.5],[0.5]]), h=0.3, d=2,
                                 window_func=parzen_window_func,
                                 kernel_func=hypercube_kernel)
p3 = parzen_estimation(x_2Dgauss, np.array([[0.3],[0.2]]), h=0.3, d=2,
                                 window_func=parzen_window_func,
                                 kernel_func=hypercube_kernel)

mu = np.array([[0],[0]])
cov = np.eye(2)

a1 = pdf_multivariate_gauss(np.array([[0],[0]]), mu, cov)
a2 = pdf_multivariate_gauss(np.array([[0.5],[0.5]]), mu, cov)
a3 = pdf_multivariate_gauss(np.array([[0.3],[0.2]]), mu, cov)

results = prettytable.PrettyTable(["", "p(x) predicted", "p(x) actual"])
results.add_row(["p([0,0]^t",p1, a1])
results.add_row(["p([0.5,0.5]^t",p2, a2])
results.add_row(["p([0.3,0.2]^t",p3, a3])

print(results)
```

```python
+---------------+---------------------+---------------------+
|               |    p(x) predicted   |     p(x) actual     |
+---------------+---------------------+---------------------+
|   p([0,0]^t   |  0.1488888888888889 | 0.15915494309189535 |
| p([0.5,0.5]^t | 0.11777777777777779 | 0.12394999430965298 |
| p([0.3,0.2]^t |  0.1511111111111111 | 0.14913891880709737 |
+---------------+---------------------+---------------------+
```

#### 5.2 使用 `scipy.stats` 的高斯核

既然我们已经针对超立方体核一步一步地走完了 Parzen 窗技术的整个流程，接下来让我们从 `scipy` 包导入 `gaussian_kde` 类，用一种更便捷的方式来完成同样的事情。

完整文档见 [docs.scipy.org](http://docs.scipy.org/doc/scipy-0.13.0/reference/generated/scipy.stats.gaussian_kde.html)。

**`gaussian_kde` 类接受 2 个参数作为输入**

- **dataset**：`array_like` 用于估计的数据点。对于一元数据，这是一个 1-D 数组；否则是一个形状为（维度数, 数据数）的 2-D 数组。
- **bw\_method**：`str, scalar or callable, optional` 用于计算估计器带宽的方法。它可以是 `'scott'`、`'silverman'`、标量常量或可调用对象。如果是标量，它将被直接用作 kde.factor。如果是可调用对象，它应当以一个 gaussian\_kde 实例作为唯一参数并返回一个标量。如果为 `'None'`（默认值），则使用 `'scott'`。更多细节参见 Notes。

注意，初始化一个 `gaussian_kde` 实例需要一个 numpy 数组，其中不同的样本按列排列，而各行反映数据集的维度——这就是为什么我们必须把之前生成的训练数据以转置的形式传入。

首先，像我们之前对超立方体核所做的那样，使用一个简单的标量作为窗宽，快速看一下 gaussian\_kde() 方法是如何工作的，并估计中心处的密度。

```python
# Example evaluating the density at the center

from scipy.stats import kde

density = kde.gaussian_kde(x_2Dgauss.T, bw_method=0.3)
print(density.evaluate(np.array([[0],[0]])))
```

```python
[ 0.14652936]
```

#### 5.3 在任意窗宽下比较高斯核与超立方体核

现在让我们在同样任意选择的窗宽下，将高斯核与超立方体核进行比较：

```python
import prettytable

gde = kde.gaussian_kde(x_2Dgauss.T, bw_method=0.3)

results = prettytable.PrettyTable(["", "p(x) hypercube kernel",
    "p(x) Gaussian kernel", "p(x) actual"])
results.add_row(["p([0,0]^t",p1, gde.evaluate(np.array([[0],[0]]))[0], a1])
results.add_row(["p([0.5,0.5]^t",p2, gde.evaluate(np.array([[0.5],[0.5]]))[0], a2])
results.add_row(["p([0.3,0.2]^t",p3, gde.evaluate(np.array([[0.3],[0.2]]))[0], a3])

print(results)
```

```python
+---------------+-----------------------+----------------------+---------------------+
|               | p(x) hypercube kernel | p(x) Gaussian kernel |     p(x) actual     |
+---------------+-----------------------+----------------------+---------------------+
|   p([0,0]^t   |   0.1488888888888889  |    0.146529357818    | 0.15915494309189535 |
| p([0.5,0.5]^t | 0.11777777777777779   |    0.11282184148     | 0.12394999430965298 |
| p([0.3,0.2]^t |   0.1511111111111111  |    0.137350626774    | 0.14913891880709737 |
+---------------+-----------------------+----------------------+---------------------+
```

#### 5.4 比较高斯核的不同带宽估计计算方法

`gaussian_kde()` 类自带两种不同的「带宽估计计算方法」，让我们来看看在我们的数据集上，选择其中一种而非另一种是否会带来差异：

```python
from scipy.stats import kde
import prettytable

mu = np.array([[0],[0]])
cov = np.eye(2)

scott = kde.gaussian_kde(x_2Dgauss.T, bw_method='scott')
silverman = kde.gaussian_kde(x_2Dgauss.T, bw_method='silverman')
scalar = kde.gaussian_kde(x_2Dgauss.T, bw_method=0.3)
actual = pdf_multivariate_gauss(np.array([[0],[0]]), mu, cov)

results = prettytable.PrettyTable(["", "p([0,0]^t gaussian kernel"])
results.add_row(["bw_method scalar 0.3:", scalar.evaluate(np.array([[0],[0]]))[0]])
results.add_row(["bw_method scott:", scott.evaluate(np.array([[0],[0]]))[0]])
results.add_row(["bw_method silverman:", silverman.evaluate(np.array([[0],[0]]))[0]])
results.add_row(["actual density:", actual])

print(results)
```

```python
+-----------------------+---------------------------+
|                       | p([0,0]^t gaussian kernel |
+-----------------------+---------------------------+
| bw_method scalar 0.3: |       0.146529357818      |
|    bw_method scott:   |       0.153502928635      |
|  bw_method silverman: |       0.153502928635      |
|    actual density:    |    0.15915494309189535    |
+-----------------------+---------------------------+
```

## 6 绘制不同核的估计结果

最后，让我们为估计出的分布绘制不同高斯核带宽估计方法的结果。

```python
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.mlab import bivariate_normal
from mpl_toolkits.mplot3d import Axes3D

X = np.linspace(-5, 5, 100)
Y = np.linspace(-5, 5, 100)
X,Y = np.meshgrid(X,Y)

##########################################
### Hypercube kernel density estimates ###
##########################################

fig = plt.figure(figsize=(10, 7))
ax = fig.gca(projection='3d')

Z = []
for i,j in zip(X.ravel(),Y.ravel()):
    Z.append(parzen_estimation(x_2Dgauss, np.array([[i],[j]]), h=0.3, d=2,
                                 window_func=parzen_window_func,
                                 kernel_func=hypercube_kernel))

Z = np.asarray(Z).reshape(100,100)
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.cm.coolwarm,
        linewidth=0, antialiased=False)

ax.set_zlim(0, 0.2)

ax.zaxis.set_major_locator(plt.LinearLocator(10))
ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.02f'))

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('p(x)')

plt.title('Hypercube kernel with window width h=0.3')

fig.colorbar(surf, shrink=0.5, aspect=7, cmap=plt.cm.coolwarm)

plt.show()

#########################################
### Gaussian kernel density estimates ###
#########################################

for bwmethod,t in zip([scalar, scott, silverman], ['scalar h=0.3', 'scott',
        'silverman']):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.gca(projection='3d')
    Z = bwmethod(np.array([X.ravel(),Y.ravel()]))
    Z = Z.reshape(100,100)
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.cm.coolwarm,
        linewidth=0, antialiased=False)

    ax.set_zlim(0, 0.2)
    ax.zaxis.set_major_locator(plt.LinearLocator(10))
    ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.02f'))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('p(x)')

    plt.title('Gaussian kernel, bw_method %s' %t)
    fig.colorbar(surf, shrink=0.5, aspect=7, cmap=plt.cm.coolwarm)
    plt.show()

###########################################
### Actual bivariate Gaussian densities ###
###########################################

fig = plt.figure(figsize=(10, 7))
ax = fig.gca(projection='3d')
Z = bivariate_normal(X, Y)
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.cm.coolwarm,
        linewidth=0, antialiased=False)

ax.set_zlim(0, 0.2)

ax.zaxis.set_major_locator(plt.LinearLocator(10))
ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.02f'))
fig.colorbar(surf, shrink=0.5, aspect=7, cmap=plt.cm.coolwarm)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('p(x)')
plt.title('Actual bivariate Gaussian densities')

plt.show()
```

![Parzen rosenblatt parzen plot5](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_plot5.webp)

![Parzen rosenblatt parzen plot6](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_plot6.webp)

![Parzen rosenblatt parzen plot7](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_plot7.webp)

![Parzen rosenblatt parzen plot8](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_plot8.webp)

![Parzen rosenblatt parzen plot9](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_plot9.webp)

### 6.1 窗宽的影响：局部尖峰与过度平均

正如我们在前面章节中讨论过的，选择合适的窗宽可能是一项颇具挑战的任务：如果选择的窗宽太小，密度中会出现局部尖峰；而如果选择的窗宽太大，我们就会对整个分布做平均：

```python
gde_01 = kde.gaussian_kde(x_2Dgauss.T, bw_method=0.01)
gde_5 = kde.gaussian_kde(x_2Dgauss.T, bw_method=0.5)
gde_20 = kde.gaussian_kde(x_2Dgauss.T, bw_method=2)

for bwmethod,t in zip([gde_01, gde_5, gde_20],
        ['scalar h=0.05', 'scalar h=0.5', 'scalar h=2']):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.gca(projection='3d')
    Z = bwmethod(np.array([X.ravel(),Y.ravel()]))
    Z = Z.reshape(100,100)
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.cm.coolwarm,
        linewidth=0, antialiased=False)

    ax.set_zlim(0, 0.2)
    ax.zaxis.set_major_locator(plt.LinearLocator(10))
    ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.02f'))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('p(x)')

    plt.title('Gaussian kernel, window width h=%s' %t)
    fig.colorbar(surf, shrink=0.5, aspect=7, cmap=plt.cm.coolwarm)
    plt.show()
```

![Parzen rosenblatt parzen plot10](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_plot10.webp)

![Parzen rosenblatt parzen plot11](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_plot11.webp)

![Parzen rosenblatt parzen plot12](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_plot12.webp)

```python
fig = plt.figure(figsize=(10, 7))
ax = fig.gca(projection='3d')

Z = gde_5(np.array([X.ravel(),Y.ravel()]))
Z = Z.reshape(100,100)
surf = ax.plot_wireframe(X, Y, Z, rstride=4, cstride=4,
    alpha=0.3, label='h = 0.5')

Z = gde_20(np.array([X.ravel(),Y.ravel()]))
Z = Z.reshape(100,100)
surf = ax.plot_wireframe(X, Y, Z, color='red',
    rstride=4, cstride=4, alpha=0.3, label='h = 2')

Z = gde_01(np.array([X.ravel(),Y.ravel()]))
Z = Z.reshape(100,100)
surf = ax.plot_wireframe(X, Y, Z, color='green',
    rstride=4, cstride=4, alpha=0.3, label='h = 0.01')
ax.set_zlim(0, 0.2)
ax.zaxis.set_major_locator(plt.LinearLocator(10))
ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.02f'))
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('p(x)')
ax.legend()

plt.title('Gaussian kernel, window width h=%s' %title)

plt.show()
```

![Parzen rosenblatt parzen plot13](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_plot13.webp)

## 7 将核密度估计用于模式分类任务

在引言中我提到过，Parzen 窗技术的一个流行应用，是在监督模式分类问题中从训练数据集估计类条件密度（也常被称为「似然」）*p(**x** | ωi)*（其中 ***x*** 是属于特定类别 *ωi* 的多维样本）。
现在，让我们使用核密度估计来设计一个简单的贝叶斯分类器。

**贝叶斯规则**

为了设计一个最小误差分类器，我们将使用贝叶斯规则：

![Decision Rule](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_26.webp)

**决策规则**

其中后验概率被用来定义我们的决策规则。例如，对于一个带有两个类别标签 *ω1* 和 *ω2* 的简单二类问题：

若 *P(ω1 | ***x***)* > *P(ω2 | ***x***)*，则判定为 *ω1*；否则判定为
*ω2*

**目标函数**

在这个例子中，让我们把问题稍微简化一下。我们将假设先验概率相等（遇到每个类别的概率相同）：
*P(ω1 | ***x***)* = *P(ω2 | ***x***)* = … = *P(ω1 | ***x***)* = *1/n*

而由于 *p(***x***)* 只是一个对所有后验概率都相同的缩放因子，我们可以把它从方程中去掉。

现在，我们可以简化决策规则，使其只依赖于先验概率。对于一个二类问题，就是

若 *P(ω1 | ***x***)* > *P(ω2 | ***x***)*，则判定为 *ω1*；否则判定为
*ω2*

### 贝叶斯分类器

更一般地（对于多类别），我们的分类器变为
*ωj* -> max[*P(ω1 | ***x***)*]，其中 *j = 1, 2, …, c*

### 7.1 生成一个训练和测试样本数据集

让我们按照以下参数，从多元高斯分布中为 3 个类别生成随机 2 维数据：

![Parzen rosenblatt parzen eq 27](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_27.webp)

现在，我们将为这 3 个类别各创建 120 个随机样本，并将其划分为大小相等的训练数据集和测试数据集，使每个集合都包含来自每个类别的 30 个样本。

```python
import numpy as np

# Covariance matrices
cov_mats = {}
for i in range(1,4):
    cov_mats[i] = i * np.eye(2)

# mean vectors    
mu_vecs = {}
for i,j in zip(range(1,4), [[0,0], [3,0], [4,5]]):
    mu_vecs[i] = np.array(j).reshape(2,1)
```

```python
# Example for accessing parameters, e.g., mu_vec and cov_mat for class2
print('mu_vec2\n', mu_vecs[2])
print('cov_mat2\n', cov_mats[2])
```

```python
mu_vec2
 [[3]
 [0]]
cov_mat2
 [[ 2.  0.]
 [ 0.  2.]]
```

```python
# Generating the random samples
all_samples = {}
for i in range(1,4):
    # generating 40x2 dimensional arrays with random Gaussian-distributed samples
    class_samples = np.random.multivariate_normal(mu_vecs[i].ravel(), cov_mats[i], 40)
    # adding class label to 3rd column
    class_samples = np.append(class_samples, np.zeros((40,1))+i, axis=1)
    all_samples[i] = class_samples
```

```python
# Dividing the samples into training and test datasets
train_set = np.append(all_samples[1][0:20], all_samples[2][0:20], axis=0)
train_set = np.append(train_set, all_samples[3][0:20], axis=0)

test_set = np.append(all_samples[1][20:40], all_samples[2][20:40], axis=0)
test_set = np.append(test_set, all_samples[3][20:40], axis=0)

assert(train_set.shape == (60, 3))
assert(test_set.shape == (60, 3))
```

```python
# Visualizing samples by plotting them in a scatter plot

import numpy as np
from matplotlib import pyplot as plt

for dset,title in zip((test_set, train_set), ['Test', 'Training']):
    f, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(dset[dset[:,2] == 1][:,0], dset[dset[:,2] == 1][:,1], \
           marker='o', color='green', s=40, alpha=0.5, label='$\omega_1$')
    ax.scatter(dset[dset[:,2] == 2][:,0], dset[dset[:,2] == 2][:,1], \
           marker='^', color='red', s=40, alpha=0.5, label='$\omega_2$')
    ax.scatter(dset[dset[:,2] == 3][:,0], dset[dset[:,2] == 3][:,1], \
           marker='s', color='blue', s=40, alpha=0.5, label='$\omega_3$')
    plt.legend(loc='upper right')
    plt.title('{} Dataset'.format(title), size=20)
    plt.ylabel('$x_2$', size=20)
    plt.xlabel('$x_1$', size=20)
plt.show()
```

![Parzen rosenblatt parzen plot14](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_plot14.webp)

![Parzen rosenblatt parzen plot15](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_plot15.webp)

### 7.2 使用贝叶斯决策规则实现分类器

现在，让我们来实现这个分类器。回顾一下：

![Parzen rosenblatt parzen eq 28](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_28.webp)

我们可以去掉先验概率（先验相等）和缩放因子：

|  |  |
| --- | --- |
| *ωj* -> max[*P(ω1 | ***x***)*]，其中 *j = 1, 2, …, c* |

```python
import operator

def bayes_classifier(x_vec, kdes):
    """
    Classifies an input sample into class w_j determined by
    maximizing the class conditional probability for p(x|w_j).

    Keyword arguments:
        x_vec: A dx1 dimensional numpy array representing the sample.
        kdes: List of the gausssian_kde (kernel density) estimates

    Returns a tuple ( p(x|w_j)_value, class label ).

    """
    p_vals = []
    for kde in kdes:
        p_vals.append(kde.evaluate(x_vec))
    max_index, max_value = max(enumerate(p_vals), key=operator.itemgetter(1))
    return (max_value, max_index + 1)
```

### 7.3 通过带高斯核的 Parzen 窗技术进行密度估计

为了方便起见，让我们使用 `scipy.stats` 库中的 kde 类来进行核密度估计：

```python
from scipy.stats import kde
class1_kde = kde.gaussian_kde(train_set[train_set[:,2] == 1].T[0:2],
        bw_method='scott')
class2_kde = kde.gaussian_kde(train_set[train_set[:,2] == 2].T[0:2],
        bw_method='scott')
class3_kde = kde.gaussian_kde(train_set[train_set[:,2] == 3].T[0:2],
        bw_method='scott')
```

### 7.4 对测试数据进行分类并计算错误率

现在，是时候对测试数据进行分类并计算经验误差了。

```python
def empirical_error(data_set, classes, classifier_func, classifier_func_args):
    """
    Keyword arguments:
        data_set: 'n x d'- dimensional numpy array, class label in the last column.
        classes: List of the class labels.
        classifier_func: Function that returns the max argument from the discriminant function.
            evaluation and the class label as a tuple.
        classifier_func_args: List of arguments for the 'classifier_func'.
    
    Returns a tuple, consisting of a dictionary withthe classif. counts and the error.
    
    e.g., ( {1: {1: 321, 2: 5}, 2: {1: 0, 2: 317}}, 0.05)
    where keys are class labels, and values are sub-dicts counting for which class (key)
    how many samples where classified as such.
    
    """
    class_dict = {i:{j:0 for j in classes} for i in classes}

    for cl in classes:
        for row in data_set[data_set[:,-1] == cl][:,:-1]:
            g = classifier_func(row, *classifier_func_args)
            class_dict[cl][g[1]] += 1
    
    correct = 0
    for i in classes:
        correct += class_dict[i][i]
    
    misclass = data_set.shape[0] - correct
    return (class_dict, misclass / data_set.shape[0])
```

```python
import prettytable

classification_dict, error = empirical_error(test_set, [1,2,3], bayes_classifier,
        [[class1_kde, class2_kde, class3_kde]])

labels_predicted = ['w{} (predicted)'.format(i) for i in [1,2,3]]
labels_predicted.insert(0,'test dataset')

train_conf_mat = prettytable.PrettyTable(labels_predicted)
for i in [1,2,3]:
    a, b, c = [classification_dict[i][j] for j in [1,2,3]]
    # workaround to unpack (since Python does not support just '*a')
    train_conf_mat.add_row(['w{} (actual)'.format(i), a, b, c])
print(train_conf_mat)
print('Empirical Error: {:.2f} ({:.2f}%)'.format(error, error * 100))
```

```python
+--------------+----------------+----------------+----------------+
| test dataset | w1 (predicted) | w2 (predicted) | w3 (predicted) |
+--------------+----------------+----------------+----------------+
| w1 (actual)  |       19       |       1        |       0        |
| w2 (actual)  |       5        |       14       |       1        |
| w3 (actual)  |       0        |       1        |       19       |
+--------------+----------------+----------------+----------------+
Empirical Error: 0.13 (13.33%)
```

### 结论

考虑到我们的训练样本规模相当小（每类 20 个样本），这个错误率在测试数据集上算是相当小的了。根据收敛原理

![Parzen rosenblatt parzen eq 29](https://sebastianraschka.com/images/blog/2014/parzen-rosenblatt/parzen_eq_29.webp)

如果我们能够增大训练数据集的规模，分类器的性能很可能会得到提升。顺便说一下，这里在训练数据集上的性能预计会好得多，因为训练数据集正是用于推导参数的数据集。

```python
classification_dict, error = empirical_error(train_set,
        [1,2,3], bayes_classifier, [[class1_kde, class2_kde, class3_kde]])

labels_predicted = ['w{} (predicted)'.format(i) for i in [1,2,3]]
labels_predicted.insert(0,'training dataset')

train_conf_mat = prettytable.PrettyTable(labels_predicted)
for i in [1,2,3]:
    a, b, c = [classification_dict[i][j] for j in [1,2,3]]
    # workaround to unpack (since Python does not support just '*a')
    train_conf_mat.add_row(['w{} (actual)'.format(i), a, b, c])
print(train_conf_mat)
print('Empirical Error: {:.2f} ({:.2f}%)'.format(error, error * 100))
```

```python
  +------------------+----------------+----------------+----------------+
  | training dataset | w1 (predicted) | w2 (predicted) | w3 (predicted) |
  +------------------+----------------+----------------+----------------+
  |   w1 (actual)    |       20       |       0        |       0        |
  |   w2 (actual)    |       0        |       20       |       0        |
  |   w3 (actual)    |       0        |       1        |       19       |
  +------------------+----------------+----------------+----------------+
  Empirical Error: 0.02 (1.67%)
```
