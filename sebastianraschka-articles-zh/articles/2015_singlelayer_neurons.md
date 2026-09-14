---
title: "神经网络与梯度下降"
title_en: "Neural Networks & Gradient Descent"
source: https://sebastianraschka.com/Articles/2015_singlelayer_neurons.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 神经网络与梯度下降

> 原文：[Neural Networks & Gradient Descent](https://sebastianraschka.com/Articles/2015_singlelayer_neurons.html) · Sebastian Raschka's Articles

**本文将简要回顾机器学习的历史与基本概念。我们将一同了解第一个以算法形式描述的神经网络，以及自适应线性神经元（adaptive linear neuron）语境下的梯度下降算法；这不仅可以引出机器学习的基本原理，也为后续文章中讲解现代多层神经网络打下基础。**

## 章节

*请注意，本文中的代码示例需要按顺序执行。本文的 Jupyter Notebook 版本可在 [GitHub](https://github.com/rasbt/pattern_classification/blob/master/machine_learning/singlelayer_neural_networks/singlelayer_neural_networks.ipynb) 上获取。*

## 引言

机器学习是当今技术时代最热门、最令人兴奋的领域之一。得益于机器学习，我们拥有了强健的电子邮件垃圾过滤器、便捷的文本与语音识别、可靠的网络搜索引擎、颇具挑战性的国际象棋程序，以及——希望不久之后——安全高效的自动驾驶汽车。

毫无疑问，机器学习已经成为一个庞大而热门的领域，有时难免让人「只见（决策）树、不见（随机）森林」。因此，我想有必要更细致地深入探讨各种机器学习算法：不仅讨论理论，还要一步一步地动手实现。

简要概括一下机器学习的本质：「机器学习是这样一个研究领域，它让计算机无需被显式编程就能具备学习能力」（Arthur Samuel，1959）。机器学习关注算法的开发与使用，这些算法能够识别数据中的模式，并基于统计学、概率论、组合学和最优化理论做出决策。

本系列的第一篇文章将介绍感知机（perceptron）与 ADALINE（ADAptive LINear NEuron，自适应线性神经元），它们都属于单层神经网络。感知机不仅是第一个以算法形式描述的学习算法 [[1](#references)]，而且非常直观、易于实现，是通向（被重新发现的）现代最先进机器学习算法——人工神经网络（或者你喜欢的话，也可称之为「深度学习」）——的良好入口。稍后我们将看到，ADALINE 是感知机算法顺理成章的改进，也为我们提供了学习机器学习中一种流行优化算法——梯度下降——的好机会。

## 人工神经元与 McCulloch-Pitts 模型

感知机最初的思想可以追溯到 Warren McCulloch 和 Walter Pitts 在 1943 年的工作 [[2](#references)]，他们将生物神经元与具有二进制输出的简单逻辑门做了类比。更直观地说，神经元可以理解为生物大脑中神经网络的子单元。在生物大脑中，强弱不一的信号到达树突，这些输入信号随后在神经元的细胞体中累积起来，一旦累积信号超过某个阈值，就会产生一个输出信号，并由轴突传递出去。

![](https://sebastianraschka.com/images/blog/2015/singlelayer_neural_networks_files/perceptron_neuron.webp)

## Frank Rosenblatt 的感知机

继续这段历史：在 McCulloch 和 Walter Pitts 之后几年，Frank Rosenblatt 发表了感知机学习规则的最初概念 [[1](#references)]。其核心思想是定义一个算法来学习权重 \(w\) 的取值，然后将这些权重与输入特征相乘，从而决定一个神经元是否「放电」。在模式分类的语境下，这样的算法可以用来判断一个样本属于这个还是那个类别。

![](https://sebastianraschka.com/images/blog/2015/singlelayer_neural_networks_files/perceptron_binary.webp)

把感知机算法放到更宏大的机器学习背景中来看：感知机属于监督学习算法，更确切地说，是单层二分类线性分类器。简而言之，任务是依据一组输入变量，预测某个数据点属于两个可能类别中的哪一个。在本文中，我不想过于深入地讨论预测建模与分类的概念，如果你想了解更多的背景知识，请参阅我之前的文章[《Introduction to supervised learning》（监督学习入门）](https://sebastianraschka.com/Articles/2014_intro_supervised_learning.html)。

### 单位阶跃函数

在深入探讨学习人工神经元权重的算法之前，先简单看一下基本记号。在后续章节中，我们将把二分类设置中的*正*类（positive）和*负*类（negative）分别记为「1」和「-1」。接下来，我们定义一个激活函数 \(g(\mathbf{z})\)，它以输入值 \(\mathbf{x}\) 与权重 \(\mathbf{w}\) 的线性组合作为输入（\(\mathbf{z} = w\_1x\_{1} + \dots + w\_mx\_{m}\)）；若 \(g(\mathbf{z})\) 大于某个给定的阈值 \(\theta\)，我们就预测为 1，否则预测为 -1。此时，这个激活函数 \(g\) 就是简单「单位阶跃函数」（unit step function）的一种变体，有时也被称为「Heaviside 阶跃函数」。

（请注意，*单位阶跃*的经典定义是：当 \(z < 0\) 时取 0，当 \(z \ge 0\) 时取 1；不过为简单起见，我们把下面这个当 \(z < \theta\) 时取 -1、当 \(z \ge \theta\) 时取 1 的分段线性函数也称作*单位阶跃函数*。）

\[g(\mathbf{z}) =\begin{cases}
1 & \text{if }\mathbf{z} \ge \theta\\
-1 & \text{otherwise}.
\end{cases}\]

其中

\[\mathbf{z} = w\_1x\_{1} + \dots + w\_mx\_{m} = \sum\_{j=1}^{m} x\_{j}w\_{j} \\ = \mathbf{w}^T\mathbf{x}\]

\(\mathbf{w}\) 是特征（权重）向量，\(\mathbf{x}\) 是来自训练集的一个 \(m\) 维样本：

\[\mathbf{w} = \begin{bmatrix}
w\_{1} \\
\vdots \\
w\_{m}
\end{bmatrix}
\quad \mathbf{x} = \begin{bmatrix}
x\_{1} \\
\vdots \\
x\_{m}
\end{bmatrix}\]

![](https://sebastianraschka.com/images/blog/2015/singlelayer_neural_networks_files/perceptron_unit_step.webp)

为了简化记号，我们把 \(\theta\) 移到等式左边，并定义 \(w\_0 = -\theta \text{ and } x\_0=1\)

于是

\[\begin{equation}
g({\mathbf{z}}) =\begin{cases}
1 & \text{if } \mathbf{z} \ge 0\\
-1 & \text{otherwise}.
\end{cases}
\end{equation}\]

且

\[\mathbf{z} = w\_0x\_{0} + w\_1x\_{1} + \dots + w\_mx\_{m} = \sum\_{j=0}^{m} x\_{j}w\_{j} \\ = \mathbf{w}^T\mathbf{x}.\]

### 感知机学习规则

这听起来也许像是还原论思路的极端案例，但这个「带阈值」的感知机背后的想法，正是模拟大脑中单个神经元的工作方式：它要么「放电」，要么不放电。总结上一节的重点：感知机接收多个输入信号，如果输入信号之和超过某个阈值，它就输出一个信号，否则保持「沉默」。而让这一切成为「机器学习」算法的，正是 Frank Rosenblatt 提出的感知机学习规则：感知机算法要学习的是输入信号的权重，以便画出一条线性决策边界，把 +1 和 -1 这两个线性可分的类别区分开来。

![](https://sebastianraschka.com/images/blog/2015/singlelayer_neural_networks_files/perceptron_schematic.webp)

Rosenblatt 最初的感知机规则相当简单，可以概括为以下几个步骤：

1. 将权重初始化为 0 或很小的随机数。
2. 对每个训练样本 \(\mathbf{x^{(i)}}\)：
   1. 计算*输出*值。
   2. 更新权重。

输出值就是由我们先前定义的单位阶跃函数预测出的类别标签（output \(=g(\mathbf{z})\)），而权重的更新可以更正式地写成 \(w\_j := w\_j + \Delta w\_j\)。

每次增量更新所用的权重更新量由如下学习规则计算：

\[\Delta w\_j = \eta \; (\text{target}^{(i)} - \text{output}^{(i)})\;x^{(i)}\_{j}\]

其中 \(\eta\) 是学习率（一个介于 0.0 和 1.0 之间的常数），「target」是真实类别标签，「output」是预测类别标签。

需要注意的是，权重向量中的所有权重都是同时更新的。具体来说，对于二维数据集，我们可以把更新写成：

\(\Delta w\_0 = \eta(\text{target}^{(i)} - \text{output}^{(i)})\)  
\(\Delta w\_1 = \eta(\text{target}^{(i)} - \text{output}^{(i)})\;x^{(i)}\_{1}\)  
\(\Delta w\_2 = \eta(\text{target}^{(i)} - \text{output}^{(i)})\;x^{(i)}\_{2}\)

在用 Python 实现感知机规则之前，先做一个简单的思想实验，来说明这条学习规则是多么简洁优美。在感知机正确预测类别标签的两种情形下，权重保持不变：

\(\Delta w\_j = \eta(-1^{(i)} - -1^{(i)})\;x^{(i)}\_{j} = 0\)  
\(\Delta w\_j = \eta(1^{(i)} - 1^{(i)})\;x^{(i)}\_{j} = 0\)

而在预测错误的情形下，权重会被分别「推向」正目标类或负目标类的方向：

\(\Delta w\_j = \eta(1^{(i)} - -1^{(i)})\;x^{(i)}\_{j} = \eta(2)\;x^{(i)}\_{j}\)  
\(\Delta w\_j = \eta(-1^{(i)} - 1^{(i)})\;x^{(i)}\_{j} = \eta(-2)\;x^{(i)}\_{j}\)

值得注意的是，只有当两个类别线性可分时，感知机的收敛才有保证。如果两个类别无法被线性决策边界分开，我们可以设置遍历训练数据集的最大次数上限（「轮次（epoch）」），以及/或设置可容忍误分类数的阈值。

### 用 Python 实现感知机规则

在本节中，我们将用 Python 实现简单的感知机学习规则，对 Iris 数据集中的花进行分类。
请注意，为了清晰起见我省略了一些「安全检查」，更「健壮」的版本请参见 [GitHub 上的代码](https://github.com/rasbt/mlxtend/blob/master/mlxtend/classifier/perceptron.py)。

```python
import numpy as np

class Perceptron(object):

    def __init__(self, eta=0.01, epochs=50):
        self.eta = eta
        self.epochs = epochs

    def train(self, X, y):

        self.w_ = np.zeros(1 + X.shape[1])
        self.errors_ = []

        for _ in range(self.epochs):
            errors = 0
            for xi, target in zip(X, y):
                update = self.eta * (target - self.predict(xi))
                self.w_[1:] +=  update * xi
                self.w_[0] +=  update
                errors += int(update != 0.0)
            self.errors_.append(errors)
        return self

    def net_input(self, X):
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def predict(self, X):
        return np.where(self.net_input(X) >= 0.0, 1, -1)
```

在下面的例子中，我们将从 [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/) 加载 Iris 数据集，并且只关注 *Setosa* 和 *Versicolor* 这两个物种。此外，出于可视化目的，我们只使用*萼片长度*（sepal length）和*花瓣长度*（petal length）这两个特征。

```python
import pandas as pd
df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data', header=None)

# setosa and versicolor
y = df.iloc[0:100, 4].values
y = np.where(y == 'Iris-setosa', -1, 1)

# sepal length and petal length
X = df.iloc[0:100, [0,2]].values
```

```python
%matplotlib inline
import matplotlib.pyplot as plt
from mlxtend.plotting import plot_decision_regions

ppn = Perceptron(epochs=10, eta=0.1)

ppn.train(X, y)
print('Weights: %s' % ppn.w_)
plot_decision_regions(X, y, clf=ppn)
plt.title('Perceptron')
plt.xlabel('sepal length [cm]')
plt.ylabel('petal length [cm]')
plt.show()

plt.plot(range(1, len(ppn.errors_)+1), ppn.errors_, marker='o')
plt.xlabel('Iterations')
plt.ylabel('Misclassifications')
plt.show()
```

```python
Weights: [-0.4  -0.68  1.82]
```

![Singlelayer neural networks](https://sebastianraschka.com/images/blog/2015/singlelayer_neural_networks_files/2015-03-14-singlelayer_neural_networks_46_1.webp)

![Singlelayer neural networks](https://sebastianraschka.com/images/blog/2015/singlelayer_neural_networks_files/2015-03-14-singlelayer_neural_networks_46_2.webp)

可以看到，感知机在第 6 次迭代后收敛，并完美地分开了两个鸢尾花类别。

### 感知机的问题

尽管感知机完美地分开了两个 Iris 花类别，收敛却是感知机最大的问题之一。Frank Rosenblatt 在数学上证明了：只要两个类别能够被线性超平面分开，感知机学习规则就会收敛；但当类别无法被线性分类器完美分开时，问题就来了。为了演示这个问题，我们改用 Iris 数据集中另外两个不同的类别和特征。

```python
# versicolor and virginica
y2 = df.iloc[50:150, 4].values
y2 = np.where(y2 == 'Iris-virginica', -1, 1)

# sepal width and petal width
X2 = df.iloc[50:150, [1,3]].values

ppn = Perceptron(epochs=25, eta=0.01)
ppn.train(X2, y2)

plot_decision_regions(X2, y2, clf=ppn)
plt.show()

plt.plot(range(1, len(ppn.errors_)+1), ppn.errors_, marker='o')
plt.xlabel('Iterations')
plt.ylabel('Misclassifications')
plt.show()
```

![Singlelayer neural networks](https://sebastianraschka.com/images/blog/2015/singlelayer_neural_networks_files/2015-03-14-singlelayer_neural_networks_52_0.webp)

![Singlelayer neural networks](https://sebastianraschka.com/images/blog/2015/singlelayer_neural_networks_files/2015-03-14-singlelayer_neural_networks_52_1.webp)

```python
print('Total number of misclassifications: %d of 100' % (y2 != ppn.predict(X2)).sum())
```

```python
Total number of misclassifications: 43 of 100
```

即使学习率更低，感知机也没能找到好的决策边界，因为每一轮次（epoch）总会有一个或多个样本被误分类，于是学习规则永远停不下对权重的更新。

在这种背景下可能显得有些矛盾的是，感知机算法的另一个缺点是：一旦所有样本都被正确分类，它就立刻停止更新权重。直觉告诉我们，类别之间具有更大间隔（如下图中虚线所示）的决策边界，其泛化误差很可能优于感知机得到的决策边界。不过，支持向量机（SVM）这类大间隔分类器是另外一次的话题了。

![](https://sebastianraschka.com/images/blog/2015/singlelayer_neural_networks_files/perceptron_margin.webp)

## 自适应线性神经元与 delta 规则

感知机在被提出之时确实非常流行，然而仅仅几年之后，Bernard Widrow 和他的博士生 Tedd Hoff 就提出了自适应线性神经元（ADALINE）的思想 [[3](#references)]。

与感知机规则不同，ADALINE 的 delta 规则（也被称为「Widrow-Hoff 规则」或 Adaline 规则）基于线性激活函数而非单位阶跃函数来更新权重；在这里，这个线性激活函数 \(g(\mathbf{z})\) 就是净输入的恒等函数 \(g(\mathbf{w}^T\mathbf{x}) = \mathbf{w}^T\mathbf{x}\)。下一节我们将看到，为什么这一线性激活是对感知机更新方式的改进，以及「delta 规则」这个名字的由来。

![](https://sebastianraschka.com/images/blog/2015/singlelayer_neural_networks_files/perceptron_vs_adaline.webp)

### 梯度下降

线性激活函数作为连续函数，相比单位阶跃函数的一大优势在于它是可微的。这一性质让我们可以定义一个代价函数 \(J(\mathbf{w})\)，通过最小化它来更新权重。对于线性激活函数，我们可以把代价函数 \(J(\mathbf{w})\) 定义为*误差平方和*（SSE），它与普通最小二乘（OLS）线性回归中最小化的代价函数类似。

\[J(\mathbf{w}) = \frac{1}{2} \sum\_{i} (\text{target}^{(i)} - \text{output}^{(i)})^2 \quad \quad \text{output}^{(i)} \in \mathbb{R}\]

（分数 \(\frac{1}{2}\) 只是为了便于推导梯度而引入的，我们将在下面几段看到。）

为了最小化 SSE 代价函数，我们将使用梯度下降——一种简单而实用的优化算法，在机器学习中常被用来寻找线性系统的局部最小值。

在进入有趣的部分（微积分）之前，先来考虑针对单个权重的凸代价函数。如下图所示，梯度下降背后的原理可以描述为「沿山坡往下爬」，直到抵达局部或全局最小值。每一步都朝着梯度的反方向迈出，而步长由学习率的数值以及梯度的坡度共同决定。

![](https://sebastianraschka.com/images/blog/2015/singlelayer_neural_networks_files/perceptron_gradient_descent_1.webp)

现在，如约进入有趣的部分——推导 Adaline 学习规则。
如上所述，每次更新都是朝着梯度的反方向迈出一步，即 \(\Delta \mathbf{w} = - \eta \nabla J(\mathbf{w})\)，因此我们必须对权重向量中的每个权重计算代价函数的偏导数：\(\Delta w\_j = - \eta \frac{\partial J}{\partial w\_j}\)。

SSE 代价函数对某个特定权重的偏导数可以按如下方式计算：

\[\begin{equation}
\frac{\partial J}{\partial w\_j} = \frac{\partial }{\partial w\_j} \frac{1}{2} \sum\_i (t^{(i)} - o^{(i)})^2 \\
= \frac{1}{2} \sum\_i \frac{\partial}{\partial w\_j} (t^{(i)} - o^{(i)})^2 \\
= \frac{1}{2} \sum\_i 2 (t^{(i)} - o^{(i)}) \frac{\partial}{\partial w\_j} (t^{(i)} - o^{(i)}) \\
= \sum\_i (t^{(i)} - o^{(i)}) \frac{\partial}{\partial w\_j} \bigg(t^{(i)} - \sum\_j w\_j x^{(i)}\_{j}\bigg) \\
= \sum\_i (t^{(i)} - o^{(i)})(-x^{(i)}\_{j})
\end{equation}\]

（t = target（目标值），o = output（输出值））

把结果代回学习规则，就得到

\(\Delta w\_j = - \eta \frac{\partial J}{\partial w\_j} = - \eta \sum\_i (t^{(i)} - o^{(i)})(- x^{(i)}\_{j}) = \eta \sum\_i (t^{(i)} - o^{(i)})x^{(i)}\_{j}\)，

最后，我们可以采用与感知机规则类似的同步权重更新：

\(\mathbf{w} := \mathbf{w} + \Delta \mathbf{w}\)。

**虽然上面的学习规则看起来与感知机规则一模一样，但我们要注意两个主要区别：**

1. 这里的输出「o」是一个实数，而不是感知机学习规则中的类别标签。
2. 权重更新是基于训练集中的全部样本计算的（而不是每处理完一个样本就增量更新一次），因此这种方法也被称为「批量」（batch）梯度下降。

### 梯度下降规则实战

现在，是时候用 Python 实现梯度下降规则了。

```python
import numpy as np

class AdalineGD(object):

    def __init__(self, eta=0.01, epochs=50):
        self.eta = eta
        self.epochs = epochs

    def train(self, X, y):

        self.w_ = np.zeros(1 + X.shape[1])
        self.cost_ = []

        for i in range(self.epochs):
            output = self.net_input(X)
            errors = (y - output)
            self.w_[1:] += self.eta * X.T.dot(errors)
            self.w_[0] += self.eta * errors.sum()
            cost = (errors**2).sum() / 2.0
            self.cost_.append(cost)
        return self

    def net_input(self, X):
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def activation(self, X):
        return self.net_input(X)

    def predict(self, X):
        return np.where(self.activation(X) >= 0.0, 1, -1)
```

在实践中，往往需要通过一些试验才能找到适合最优收敛的学习率，因此我们先把两种不同学习率下的代价绘制出来。

```python
ada = AdalineGD(epochs=10, eta=0.01).train(X, y)
plt.plot(range(1, len(ada.cost_)+1), np.log10(ada.cost_), marker='o')
plt.xlabel('Iterations')
plt.ylabel('log(Sum-squared-error)')
plt.title('Adaline - Learning rate 0.01')
plt.show()

ada = AdalineGD(epochs=10, eta=0.0001).train(X, y)
plt.plot(range(1, len(ada.cost_)+1), ada.cost_, marker='o')
plt.xlabel('Iterations')
plt.ylabel('Sum-squared-error')
plt.title('Adaline - Learning rate 0.0001')
plt.show()
```

![Singlelayer neural networks](https://sebastianraschka.com/images/blog/2015/singlelayer_neural_networks_files/2015-03-14-singlelayer_neural_networks_77_0.webp)

![Singlelayer neural networks](https://sebastianraschka.com/images/blog/2015/singlelayer_neural_networks_files/2015-03-14-singlelayer_neural_networks_77_1.webp)

上面两张图很好地说明了绘制学习曲线的重要性，它们展示了梯度下降最常见的两个问题：

1. 如果学习率太大，梯度下降会冲过最小值点而发散。
2. 如果学习率太小，算法需要非常多轮次（epoch）才能收敛，而且更容易被困在局部极小值中。

![](https://sebastianraschka.com/images/blog/2015/singlelayer_neural_networks_files/perceptron_learning_rate.webp)

梯度下降也是一个很好的例子，可以说明特征缩放对许多机器学习算法为何重要。
当特征处于同一尺度时，不仅更容易找到合适的学习率，还往往收敛更快，并能防止权重变得过小（数值稳定性）。

一种常用的特征缩放方法是标准化（standardization）：

\[\mathbf{x}\_{j, std} = \frac{\mathbf{x}\_j - \mathbf{\mu}\_j}{\mathbf{\sigma}\_j}\]

其中 \(\mathbf{\mu}\_j\) 是特征 \(\mathbf{x}\_{j}\) 的样本均值，\(\mathbf{\sigma}\_j\) 是相应的标准差。标准化之后，各特征的方差为 1，并且以零均值为中心。

```python
# standardize features
X_std = np.copy(X)
X_std[:,0] = (X[:,0] - X[:,0].mean()) / X[:,0].std()
X_std[:,1] = (X[:,1] - X[:,1].mean()) / X[:,1].std()
```

```python
%matplotlib inline
import matplotlib.pyplot as plt
from mlxtend.plotting import plot_decision_regions

ada = AdalineGD(epochs=15, eta=0.01)

ada.train(X_std, y)
plot_decision_regions(X_std, y, clf=ada)
plt.title('Adaline - Gradient Descent')
plt.xlabel('sepal length [standardized]')
plt.ylabel('petal length [standardized]')
plt.show()

plt.plot(range(1, len( ada.cost_)+1), ada.cost_, marker='o')
plt.xlabel('Iterations')
plt.ylabel('Sum-squared-error')
plt.show()
```

![Singlelayer neural networks](https://sebastianraschka.com/images/blog/2015/singlelayer_neural_networks_files/2015-03-14-singlelayer_neural_networks_82_0.webp)

![Singlelayer neural networks](https://sebastianraschka.com/images/blog/2015/singlelayer_neural_networks_files/2015-03-14-singlelayer_neural_networks_82_1.webp)

![](https://sebastianraschka.com/images/blog/2015/singlelayer_neural_networks_files/perceptron_animation.gif)

### 通过随机梯度下降实现在线学习

上一节讲的都是「批量」梯度下降学习。所谓「批量」更新，指的是代价函数基于完整的训练数据集来最小化。回想一下感知机规则，我们记得它是在每处理完一个单独的训练样本后就增量地更新权重。这种方法也被称为「在线」（online）学习，事实上，Bernard Widrow 等人 [[3](#references)] 最初对 Adaline 的描述正是如此。

这种增量更新权重的过程也被称为「随机」梯度下降，因为它只是对代价函数最小化的近似。尽管随机梯度下降因其「随机」性质和「近似的」方向（梯度）听起来不如梯度下降，但它在实践中却有一些优势。由于每处理完一个训练样本就立即应用更新，随机梯度下降往往比（批量）梯度下降收敛快得多；随机梯度下降的计算效率也更高，对于超大数据集尤其如此。在线学习的另一个优点是，当新训练数据到来时（例如在 Web 应用中），分类器可以立即得到更新，而在存储成问题的场景下，旧的训练数据也可以被丢弃。在大规模机器学习系统中，人们还普遍使用所谓的「小批量」（mini-batch），这是收敛比随机梯度下降更平滑的一种折中方案。

为了内容完整，我们再来实现随机梯度下降版的 Adaline，并确认它能在线性可分的 Iris 数据集上收敛。

```python
import numpy as np

class AdalineSGD(object):

    def __init__(self, eta=0.01, epochs=50):
        self.eta = eta
        self.epochs = epochs

    def train(self, X, y, reinitialize_weights=True):

        if reinitialize_weights:
            self.w_ = np.zeros(1 + X.shape[1])
        self.cost_ = []

        for i in range(self.epochs):
            for xi, target in zip(X, y):
                output = self.net_input(xi)
                error = (target - output)
                self.w_[1:] += self.eta * xi.dot(error)
                self.w_[0] += self.eta * error

            cost = ((y - self.activation(X))**2).sum() / 2.0
            self.cost_.append(cost)
        return self

    def net_input(self, X):
        return np.dot(X, self.w_[1:]) + self.w_[0]

    def activation(self, X):
        return self.net_input(X)

    def predict(self, X):
        return np.where(self.activation(X) >= 0.0, 1, -1)
```

在让 Adaline 通过随机梯度下降学习之前，还有一条建议：先打乱训练数据集，以便以随机顺序遍历训练样本。

我们应当指出，「标准」的随机梯度下降算法采用的是「有放回」（with replacement）采样，也就是说，每次迭代都从整个训练集中随机选取一个训练样本。相比之下，「无放回」（without replacement）采样意味着每个训练样本在每轮次（epoch）中恰好被使用一次，它不仅更容易实现，在实验对比中也表现出更好的性能。关于这一主题更详细的讨论，可以参阅 Benjamin Recht 和 Christopher Re 的论文 *Beneath the valley of the noncommutative arithmetic-geometric mean inequality: conjectures, case-studies, and consequences* [[4](#references)]。

```python
ada = AdalineSGD(epochs=15, eta=0.01)

# shuffle data
np.random.seed(123)
idx = np.random.permutation(len(y))
X_shuffled, y_shuffled =  X_std[idx], y[idx]

# train and adaline and plot decision regions
ada.train(X_shuffled, y_shuffled)
plot_decision_regions(X_shuffled, y_shuffled, clf=ada)
plt.title('Adaline - Gradient Descent')
plt.xlabel('sepal length [standardized]')
plt.ylabel('petal length [standardized]')
plt.show()

plt.plot(range(1, len(ada.cost_)+1), ada.cost_, marker='o')
plt.xlabel('Iterations')
plt.ylabel('Sum-squared-error')
plt.show()
```

![Singlelayer neural networks](https://sebastianraschka.com/images/blog/2015/singlelayer_neural_networks_files/2015-03-14-singlelayer_neural_networks_91_0.webp)

![Singlelayer neural networks](https://sebastianraschka.com/images/blog/2015/singlelayer_neural_networks_files/2015-03-14-singlelayer_neural_networks_91_1.webp)

## 接下来是什么？

尽管本文涵盖了许多不同的主题，我们对人工神经网络的探索也不过是浅尝辄止。

在后续文章中，我们将探讨动态调整学习率的不同方法、用于多分类的「One-vs-All」与「One-vs-One」概念、通过引入额外信息来克服过拟合的正则化方法、非线性问题与多层神经网络的应对、人工神经元的各种激活函数，以及逻辑回归和支持向量机等相关概念。

![](https://sebastianraschka.com/images/blog/2015/singlelayer_neural_networks_files/perceptron_activation.webp)

感谢阅读。如果你喜欢这些内容，也可以在 [Twitter 上找到我](https://twitter.com/rasbt)，我会在那里分享更多有用的内容。

### 参考文献

[1] F. Rosenblatt. The perceptron, a perceiving and recognizing automaton Project Para. Cornell Aeronautical Laboratory, 1957.

[2] W. S. McCulloch and W. Pitts. A logical calculus of the ideas immanent in nervous activity. The bulletin of mathematical biophysics, 5(4):115–133, 1943.

[3] B. Widrow et al. Adaptive "Adaline" neuron using chemical "memistors". Number Technical Report 1553-2. Stanford Electron. Labs., Stanford, CA, October 1960.

[4] B. Recht and C. R ́e. Beneath the valley of the noncommutative arithmetic-geometric mean inequality: conjectures, case-studies, and consequences. arXiv preprint arXiv:1202.4184, 2012.
