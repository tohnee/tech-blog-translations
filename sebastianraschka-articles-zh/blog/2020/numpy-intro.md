---
title: "NumPy 与 Matplotlib 入门"
title_en: "NumPy and Matplotlib Introduction"
source: https://sebastianraschka.com/blog/2020/numpy-intro.html
crawled: 2026-09-06
translated: 2026-09-06
---

# NumPy 与 Matplotlib 入门

> 原文：[NumPy and Matplotlib Introduction](https://sebastianraschka.com/blog/2020/numpy-intro.html)

由于我的「Stat 451：机器学习与统计模式分类导论」课上许多学生对 Python 和 NumPy 还比较陌生，我最近专门安排了一节课来讲后者。课程讲义基于一个交互式 Jupyter notebook 文件，我也以它为基础录制了课程视频，因此我觉得值得把它重新整理成一篇博客文章，并附上「讲解内容」——也就是视频录像。

**补充材料：**

- [这个链接](https://deepnote.com/launch?url=https%3A%2F%2Fgithub.com%2Frasbt%2Fnumpy-intro-blogarticle-2020%2Fblob%2Fmaster%2Fscipython__blog.ipynb)指向本文的 Deepnote 版本，你可以在浏览器中与之交互。
- 本文的 Jupyter notebook 版本可在 GitHub 上找到：<https://github.com/rasbt/numpy-intro-blogarticle-2020>。

本文的代码基于以下软件版本生成：

- CPython 3.8.3
- numpy 1.19.1
- matplotlib 3.3.1

## 4.1：NumPy 基础

### NumPy——处理数值数组

#### NumPy 简介

本节将对 NumPy 库做一个快速导览，介绍如何在 Python 中处理多维数组。NumPy（Numerical Python 的缩写）诞生于 2005 年，由 Numarray 合并进 Numeric 而成。从那时起，开源的 NumPy 库逐渐发展成为 Python 科学计算的核心库，并成为 SciPy、Scikit-learn、Pandas 等许多其他科学库的基础构件。
NumPy 对科学界如此有吸引力的地方在于：它提供了便捷的 Python 接口，可以高效地处理多维数组数据结构；这种 NumPy 数组数据结构也称为 `ndarray`，是 *n*-dimensional array（n 维数组）的缩写。

除了大部分用 C 实现、以 Python 作为「胶水语言」之外，NumPy 数值计算如此高效的主要原因还在于：NumPy 数组使用连续的内存块，CPU 可以高效地缓存它们。相比之下，Python 列表是指向内存中随机位置对象的指针数组，难以缓存，且内存查找的开销更大。不过，计算效率和低内存占用是有代价的：NumPy 数组大小固定且是同质的（homogeneous），即所有元素必须是同一类型。同质的 `ndarray` 对象的好处是，NumPy 可以用高效的 C 代码执行操作，避免昂贵的类型检查以及 Python API 的其他开销。虽然从 Python 列表末尾添加或删除元素非常高效，但改变 NumPy 数组的大小非常昂贵，因为这需要创建一个新数组，并把旧数组中我们想保留的内容搬运过去（无论是扩大还是缩小）。

除了在数值计算上比原生 Python 代码更高效之外，得益于向量化操作和广播（broadcasting），NumPy 代码还可以更优雅、更易读——这些特性正是本文将要探索的内容。

如今，NumPy 构成了 Python 科学计算生态的基础。

#### 动机：NumPy 很快！

在讨论更多细节之前，先给出一些动机，说明为什么学习和使用 NumPy 是值得的。我们来看一下与普通 Python 代码的速度对比。具体来说，我们用 Python（使用列表）计算向量点积，并与 NumPy 的点积函数进行比较。从数学上讲，两个向量 \(\mathbf{x}\) 和 \(\mathbf{w}\) 的点积可以写为：

\[z = \sum\_i x\_i w\_i = x\_1 \times w\_1 + x\_2 \times w\_2 + ... + x\_n \times w\_n = \mathbf{x}^\top \mathbf{w}\]

首先是使用 for 循环的 Python 实现：

**输入：**

```python
def python_forloop_list_approach(x, w):
    z = 0.
    for i in range(len(x)):
        z += x[i] * w[i]
    return z

a = [1., 2., 3.]
b = [4., 5., 6.]

print(python_forloop_list_approach(a, b))
```

**输出：**

```python
32.0
```

让我们用 IPython 的 `%timeit` 魔法函数来计算两个更大（1000 个元素）的向量的运行时间：

**输入：**

```python
large_a = list(range(1000))
large_b = list(range(1000))

%timeit python_forloop_list_approach(large_a, large_b)
```

**输出：**

```python
100 µs ± 9.48 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)
```

接下来，我们使用 NumPy 实现的 `dot` 函数/方法来计算两个向量之间的点积，然后运行 `%timeit`：

**输入：**

```python
import numpy as np

def numpy_dotproduct_approach(x, w):
    # same as np.dot(x, w)
    # and same as x @ w
    return x.dot(w)
    

a = np.array([1., 2., 3.])
b = np.array([4., 5., 6.])

print(numpy_dotproduct_approach(a, b))
```

**输出：**

```python
32.0
```

**输入：**

```python
large_a = np.arange(1000)
large_b = np.arange(1000)

%timeit numpy_dotproduct_approach(large_a, large_b)
```

**输出：**

```python
1.13 µs ± 31.5 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
```

可以看到，用 NumPy 的 dot 函数替换 for 循环后，向量点积的计算速度大约快了 100 倍。

#### n 维数组

NumPy 围绕 [`ndarrays`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html) 对象构建，这是一种高性能的多维数组数据结构。直观上，我们可以把一维 NumPy 数组看作表示元素向量的数据结构——你可以把它当作一个固定大小、所有元素类型相同的 Python 列表。类似地，二维数组可以看作表示矩阵的数据结构，或者「列表的列表」。虽然在不修改源代码编译的情况下，NumPy 数组最多可以有 32 个维度，但为了便于说明，本入门只关注较低维度的数组。

现在，让我们通过调用 `array` 函数开始使用 NumPy——从一个「列表的列表」创建一个两行三列的二维 NumPy 数组：

**输入：**

```python
a = [1., 2., 3.]
np.array(a)
```

**输出：**

```python
array([1., 2., 3.])
```

**输入：**

```python
lst = [[1, 2, 3], 
       [4, 5, 6]]
ary2d = np.array(lst)
ary2d

# rows x columns
```

**输出：**

```python
array([[1, 2, 3],
       [4, 5, 6]])
```

![Drawing](https://sebastianraschka.com/images/blog/2020/numpy-intro/array_1.webp)

默认情况下，NumPy 在构造数组时会推断其类型。由于我们传入的是 Python 整数，在 64 位机器上，`ndarray` 对象 `ary2d` 的类型应当是 `int64`，可以通过访问 `dtype` 属性来确认：

**输入：**

```python
ary2d.dtype
```

**输出：**

```python
dtype('int64')
```

如果想构造不同类型的 NumPy 数组，可以向 `array` 函数的 `dtype` 参数传入实参，例如 `np.int32`，以创建 32 位数组。受支持数据类型的完整列表请参阅官方 [NumPy 文档](https://docs.scipy.org/doc/numpy/user/basics.types.html)。数组构造完成后，可以通过 `astype` 方法向下转型或重新指定类型，如下例所示：

**输入：**

```python
int32_ary = ary2d.astype(np.int32)
int32_ary
```

**输出：**

```python
array([[1, 2, 3],
       [4, 5, 6]], dtype=int32)
```

**输入：**

```python
float32_ary = ary2d.astype(np.float32)
float32_ary
```

**输出：**

```python
array([[1., 2., 3.],
       [4., 5., 6.]], dtype=float32)
```

**输入：**

```python
float32_ary.dtype
```

**输出：**

```python
dtype('float32')
```

上面的代码片段返回了 `8`，这意味着数组中的每个元素（记住，`ndarray` 是同质的）在内存中占用 8 字节。这个结果是合理的，因为数组 `ary2d` 的类型是 `int64`（64 位整数，前面已确认），而 8 位等于 1 字节。（注意，`'int64'` 只是 `np.int64` 的简写。）

要返回数组中元素的数量，可以使用 `size` 属性，如下所示：

而数组的维数（直观上，你可以把*维度*理解为张量的*秩*）可以通过 `ndim` 属性获得：

**输入：**

```python
ary2d
```

**输出：**

```python
array([[1, 2, 3],
       [4, 5, 6]])
```

**输入：**

```python
ary2d.ndim
```

**输出：**

```python
2
```

如果我们关心每个数组维度上元素的数量（在 NumPy 数组的语境中，也可以把它们称为*轴*，axis），可以访问 `shape` 属性，如下所示：

**输入：**

```python
len(ary2d.shape)
```

**输出：**

```python
2
```

`shape` 总是一个元组；在上面的代码示例中，如果把这个二维 `ary` 对象看作矩阵表示，它有*两*行和*三*列，即 `(2, 3)`。

反过来，一维数组的 `shape`（一个 `tuple` 类型的对象）只包含单个值：

**输入：**

```python
np.array([1., 2., 3.]).shape
```

**输出：**

```python
(3,)
```

## 4.2：NumPy 数组构造与索引

### 数组构造例程

本节提供一份并不完整的数组构造函数清单。有一些简单而实用的函数可以构造全 1 或全 0 的数组：

**输入：**

```python
np.ones((3, 4), dtype=np.int)
```

**输出：**

```python
array([[1, 1, 1, 1],
       [1, 1, 1, 1],
       [1, 1, 1, 1]])
```

**输入：**

```python
np.zeros((3, 3))
```

**输出：**

```python
array([[0., 0., 0.],
       [0., 0., 0.],
       [0., 0., 0.]])
```

我们可以用这些函数创建具有任意值的数组，例如，可以像下面这样创建一个包含值 99 的数组：

**输入：**

```python
np.zeros((3, 3)) + 99
```

**输出：**

```python
array([[99., 99., 99.],
       [99., 99., 99.],
       [99., 99., 99.]])
```

创建全 1 或全 0 的数组也可以用作占位数组，适用于我们不想把初始值用于计算、而是想立刻填入其他值的情况。如果不需要初始值（例如 `'0.'` 或 `'1.'`），还有 `numpy.empty` 可用，其语法与 `numpy.ones` 和 `np.zeros` 相同。不过，`empty` 函数并不会用某个特定值填充数组，而是用内存中的无意义值创建数组。我们可以把 `zeros` 看作先用 `empty` 创建数组、再把所有值设为 `0.` 的函数——不过在实践中，速度上的差异并不明显。

NumPy 还提供了以 `ndarray` 形式创建单位矩阵和对角矩阵的函数，这在线性代数场景中很有用——线性代数是我们将在本文后面探讨的主题。

**输入：**

```python
np.eye(3)
```

**输出：**

```python
array([[1., 0., 0.],
       [0., 1., 0.],
       [0., 0., 1.]])
```

**输入：**

```python
np.diag((1, 2, 3))
```

**输出：**

```python
array([[1, 0, 0],
       [0, 2, 0],
       [0, 0, 3]])
```

最后，我想提两个非常有用的、用于在指定范围内创建数列的函数：`arange` 和 `linspace`。NumPy 的 `arange` 函数与 Python 的 `range` 对象遵循相同的语法：如果提供两个参数，第一个参数表示起始值，第二个参数定义半开区间的终止值：

**输入：**

```python
np.arange(4, 10)
```

**输出：**

```python
array([4, 5, 6, 7, 8, 9])
```

注意，`arange` 也会像 `array` 函数一样进行类型推断。如果只提供一个函数参数，该 range 对象会把此数字当作区间的端点，并从 0 开始：

**输入：**

```python
np.arange(5)
```

**输出：**

```python
array([0, 1, 2, 3, 4])
```

与 Python 的 `range` 类似，还可以提供第三个参数来定义*步长*（默认步长为 1）。例如，我们可以这样获得 1 到 10 之间所有非整数的值：

**输入：**

```python
np.arange(1., 11., 0.1)
```

**输出：**

```python
array([ 1. ,  1.1,  1.2,  1.3,  1.4,  1.5,  1.6,  1.7,  1.8,  1.9,  2. ,
        2.1,  2.2,  2.3,  2.4,  2.5,  2.6,  2.7,  2.8,  2.9,  3. ,  3.1,
        3.2,  3.3,  3.4,  3.5,  3.6,  3.7,  3.8,  3.9,  4. ,  4.1,  4.2,
        4.3,  4.4,  4.5,  4.6,  4.7,  4.8,  4.9,  5. ,  5.1,  5.2,  5.3,
        5.4,  5.5,  5.6,  5.7,  5.8,  5.9,  6. ,  6.1,  6.2,  6.3,  6.4,
        6.5,  6.6,  6.7,  6.8,  6.9,  7. ,  7.1,  7.2,  7.3,  7.4,  7.5,
        7.6,  7.7,  7.8,  7.9,  8. ,  8.1,  8.2,  8.3,  8.4,  8.5,  8.6,
        8.7,  8.8,  8.9,  9. ,  9.1,  9.2,  9.3,  9.4,  9.5,  9.6,  9.7,
        9.8,  9.9, 10. , 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8,
       10.9])
```

如果我们想在指定的半开区间内创建特定数量的等间距值，`linspace` 函数尤其有用：

**输入：**

```python
np.linspace(6., 15., num=10)
```

**输出：**

```python
array([ 6.,  7.,  8.,  9., 10., 11., 12., 13., 14., 15.])
```

### 数组索引

本节我们将介绍通过不同索引方法获取 NumPy 数组元素的基础知识。简单的 NumPy 索引和切片的工作方式与 Python 列表类似，我们将在下面的代码片段中演示——获取一维数组的第一个元素：

**输入：**

```python
ary = np.array([1, 2, 3])
ary[0]
```

**输出：**

```python
1
```

同样，切片操作也遵循相同的 Python 语义。下面的例子展示如何获取 `ary` 中的前两个元素：

**输入：**

```python
ary[0:3] # equivalent to ary[0:2]
```

**输出：**

```python
array([1, 2, 3])
```

如果处理的是具有多个维度或轴的数组，我们就用逗号分隔索引或切片操作，如下面的一系列示例所示：

**输入：**

```python
ary = np.array([[1, 2, 3],
                [4, 5, 6]])

ary[0, -2] # first row, second from last element
```

**输出：**

```python
2
```

**输入：**

```python
ary[-1, -1] # lower right
```

**输出：**

```python
6
```

**输入：**

```python
ary[1, 1] # first row, second column
```

**输出：**

```python
5
```

![Drawing](https://sebastianraschka.com/images/blog/2020/numpy-intro/array_2.webp)

**输入：**

```python
ary[:, 0] # entire first column
```

**输出：**

```python
array([1, 4])
```

**输入：**

```python
ary[:, :2] # first two columns
```

**输出：**

```python
array([[1, 2],
       [4, 5]])
```

## 4.3：NumPy 数组数学与通用函数

### 数组数学与通用函数

在前面的章节中，你学习了如何创建 NumPy 数组以及如何访问数组中的不同元素。现在该介绍让 `ndarray` 用起来如此高效便捷的核心特性之一了：向量化。通常，如果想对序列类对象执行算术运算，我们会使用 for 循环；而 NumPy 提供了向量化封装，可以通过所谓的 *ufunc* 隐式地执行逐元素运算——「*ufunc*」是 universal function（通用函数）的缩写。

截至撰写本文时，NumPy 中已有 60 多个 ufunc；ufunc 以编译后的 C 代码实现，与原生 Python 相比非常快速高效。本节我们将了解最常用的 ufunc，完整的列表建议查阅[官方文档](https://docs.scipy.org/doc/numpy/reference/ufuncs.html#available-ufuncs)。

为了给出一个简单的逐元素加法 ufunc 示例，请看下面的例子：我们把一个标量（这里是 1）加到嵌套 Python 列表的每个元素上：

**输入：**

```python
lst = [[1, 2, 3], 
       [4, 5, 6]] # 2d array

for row_idx, row_val in enumerate(lst):
    for col_idx, col_val in enumerate(row_val):
        lst[row_idx][col_idx] += 1
lst
```

**输出：**

```python
[[2, 3, 4], [5, 6, 7]]
```

这种 for 循环的写法非常冗长，我们可以用列表推导式更优雅地实现同样的目标：

**输入：**

```python
lst = [[1, 2, 3], [4, 5, 6]]
[[cell + 1 for cell in row] for row in lst]
```

**输出：**

```python
[[2, 3, 4], [5, 6, 7]]
```

使用 NumPy 的逐元素标量加法 ufunc 也能完成同样的事情，如下所示：

**输入：**

```python
ary = np.array([[1, 2, 3], [4, 5, 6]])
ary = np.add(ary, 1) # binary ufunc
ary
```

**输出：**

```python
array([[2, 3, 4],
       [5, 6, 7]])
```

基本算术运算的 ufunc 包括 `add`、`subtract`、`divide`、`multiply`、`power` 和 `exp`（指数）。不过，NumPy 使用了运算符重载，因此我们可以直接使用数学运算符（`+`、`-`、`/`、`*` 和 `**`）：

**输入：**

```python
np.add(ary, 1)
```

**输出：**

```python
array([[3, 4, 5],
       [6, 7, 8]])
```

**输入：**

```python
ary + 1
```

**输出：**

```python
array([[3, 4, 5],
       [6, 7, 8]])
```

**输入：**

```python
np.power(ary, 2)
```

**输出：**

```python
array([[ 4,  9, 16],
       [25, 36, 49]])
```

**输入：**

```python
ary**2
```

**输出：**

```python
array([[ 4,  9, 16],
       [25, 36, 49]])
```

上面我们看到的都是*二元*（binary）ufunc 的例子，即接受两个输入参数的 ufunc。此外，NumPy 还实现了几个有用的*一元*（unary）ufunc，例如 `log`（自然对数）、`log10`（以 10 为底的对数）和 `sqrt`（平方根）：

**输入：**

```python
np.sqrt(ary)
```

**输出：**

```python
array([[1.41421356, 1.73205081, 2.        ],
       [2.23606798, 2.44948974, 2.64575131]])
```

我们常常想沿给定轴计算数组元素的和或积。为此可以使用 ufunc 的 `reduce` 操作。默认情况下，`reduce` 沿第一个轴（`axis=0`）应用运算。对于二维数组，可以把第一个轴理解为矩阵的行。因此，沿行方向把元素相加就得到该矩阵的列和，如下所示：

**输入：**

```python
ary = np.array([[1, 2, 3], 
                [4, 5, 6]]) # rolling over the 1st axis, axis 0

np.add.reduce(ary, axis=0)
```

**输出：**

```python
array([5, 7, 9])
```

要计算上面数组的行和，可以指定 `axis=1`：

**输入：**

```python
np.add.reduce(ary, axis=1) # row sums
```

**输出：**

```python
array([ 6, 15])
```

虽然 `reduce` 作为更通用的操作可能更直观，但 NumPy 也为特定操作提供了简写形式，例如 `product` 和 `sum`。例如，`sum(axis=0)` 等价于 `add.reduce`：

**输入：**

```python
ary.sum(axis=0) # column sums
```

**输出：**

```python
array([5, 7, 9])
```

**输入：**

```python
ary.sum(axis=1) # row sums
```

**输出：**

```python
array([ 6, 15])
```

![Drawing](https://sebastianraschka.com/images/blog/2020/numpy-intro/ufunc.webp)

需要提醒的是，如果我们不指定轴，`product` 和 `sum` 会计算整个数组的积或和：

**输入：**

```python
ary.sum()
```

**输出：**

```python
21
```

其他有用的一元 ufunc 还有：

- `np.mean`（计算算术平均值）
- `np.std`（计算标准差）
- `np.var`（计算方差）
- `np.sort`（对数组排序）
- `np.argsort`（返回能对数组排序的索引）
- `np.min`（返回数组的最小值）
- `np.max`（返回数组的最大值）
- `np.argmin`（返回最小值的索引）
- `np.argmax`（返回最大值的索引）
- `np.array_equal`（检查两个数组的形状和元素是否相同）

## 4.4：NumPy 广播

### 广播

上一节我们略过了一个话题：广播（broadcasting）。广播允许我们在两个维度不匹配的数组之间执行向量化操作，方式是创建隐式的多维网格。你在上一节已经接触过 ufunc——我们在标量与多维数组之间做逐元素加法，这只是广播的一个例子。

![Drawing](https://sebastianraschka.com/images/blog/2020/numpy-intro/broadcasting-1.webp)

自然地，我们也可以在维度相同的数组之间执行逐元素运算：

与线性代数中的惯例不同，我们还可以对形状不同的数组做加法。在上面的例子中，我们将一个一维数组与一个二维数组相加，NumPy 从一维数组 `ary1` 创建了一个隐式的多维网格：

**输入：**

```python
ary = np.array([1, 2, 3])
ary + 1
```

**输出：**

```python
array([2, 3, 4])
```

**输入：**

```python
ary + np.array([1, 1, 1])
```

**输出：**

```python
array([2, 3, 4])
```

![Drawing](https://sebastianraschka.com/images/blog/2020/numpy-intro/broadcasting-2.webp)

**输入：**

```python
ary2 = np.array([[4, 5, 6], 
                 [7, 8, 9]])

ary2 + ary
```

**输出：**

```python
array([[ 5,  7,  9],
       [ 8, 10, 12]])
```

## 4.5：NumPy 高级索引——内存视图与副本

### 高级索引——内存视图与副本

在前面的章节中，我们使用的是基本的索引和切片例程。需要特别注意的是，基于整数的基本索引和切片会在内存中创建 NumPy 数组的所谓*视图*（view）。使用视图可能非常有价值，因为它避免了创建不必要的数组副本，从而节省内存资源。为了说明内存视图的概念，让我们走过一个简单的例子：访问数组的第一行，把它赋给一个变量，然后修改该变量：

**输入：**

```python
ary = np.array([[1, 2, 3],
                [4, 5, 6]])

first_row = ary[0]
```

**输出：**
**输入：**

```python
first_row
```

**输出：**

```python
array([1, 2, 3])
```

**输入：**

```python
first_row += 99
```

**输出：**
正如预期，`first_row` 被修改了，现在包含第一行的原始值加 99：

**输入：**

```python
first_row
```

**输出：**

```python
array([100, 101, 102])
```

但请注意，原数组也被修改了：

**输入：**

```python
ary
```

**输出：**

```python
array([[100, 101, 102],
       [  4,   5,   6]])
```

正如上面的例子所示，修改 `first_row` 的值也影响了原数组。原因在于 `ary[0]` 创建的是 `ary` 第一行的视图，随后其元素被加了 99。同样的概念也适用于切片操作：

**输入：**

```python
ary = np.array([[1, 2, 3],
                [4, 5, 6]])

first_row = ary[1:3]
first_row += 99
ary
```

**输出：**

```python
array([[  1,   2,   3],
       [103, 104, 105]])
```

**输入：**

```python
ary = np.array([[1, 2, 3],
                [4, 5, 6]])

center_col = ary[:, 2]
center_col += 99
ary
```

**输出：**

```python
array([[  1,   2, 102],
       [  4,   5, 105]])
```

使用 NumPy 数组时，始终要记住**切片创建的是视图**——这有时是我们想要的，因为它避免了在内存中创建不必要的副本，从而加快代码速度。但在某些场景下，我们想强制创建数组的副本；可以通过 `copy` 方法实现，如下所示：

**输入：**

```python
ary = np.array([[1, 2, 3],
                [4, 5, 6]])

first_row = ary[0].copy()
first_row += 99
```

**输入：**

```python
first_row
```

**输出：**

```python
array([100, 101, 102])
```

**输入：**

```python
ary
```

**输出：**

```python
array([[1, 2, 3],
       [4, 5, 6]])
```

### 花式索引

除了基本的单整数索引和切片操作之外，NumPy 还支持称为*花式*索引（fancy indexing）的高级索引例程。通过花式索引，我们可以使用由非连续整数索引组成的元组或列表对象来返回所需的数组元素。由于花式索引可以用非连续的序列执行，它无法返回视图——即内存中的一段连续切片。因此，花式索引总是返回数组的副本——这一点要牢记于心。下面的代码片段展示了一些花式索引的例子：

**输入：**

```python
ary = np.array([[1, 2, 3],
                [4, 5, 6]])

ary[:, [0, 2]] # first and and last column
```

**输出：**

```python
array([[1, 3],
       [4, 6]])
```

**输入：**

```python
this_is_a_copy = ary[:, [0, 2]]
this_is_a_copy += 99
```

注意，`this_is_a_copy` 中的值如预期那样被增加了：

**输入：**

```python
this_is_a_copy
```

**输出：**

```python
array([[100, 102],
       [103, 105]])
```

不过，原数组的内容不受影响：

**输入：**

```python
ary
```

**输出：**

```python
array([[1, 2, 3],
       [4, 5, 6]])
```

### 用于索引的布尔掩码

最后，我们还可以使用布尔掩码（Boolean mask）来索引——也就是由 `True` 和 `False` 值组成的数组。请看下面的例子，我们返回数组中所有大于 3 的值：

**输入：**

```python
ary = np.array([[1, 2, 3],
                [4, 5, 6]])

greater3_mask = ary > 3
greater3_mask
```

**输出：**

```python
array([[False, False, False],
       [ True,  True,  True]])
```

利用这些掩码，我们可以按照期望的条件选取元素：

**输入：**

```python
ary[greater3_mask]
```

**输出：**

```python
array([4, 5, 6])
```

我们还可以用逻辑与运算符 `&` 或逻辑或运算符 `|` 把不同的选择条件串联起来。下面的例子演示如何选取既大于 3 又能被 2 整除的数组元素：

**输入：**

```python
(ary > 3) & (ary % 2 == 0)
```

**输出：**

```python
array([[False, False, False],
       [ True, False,  True]])
```

与前面的例子类似，我们可以把这个布尔数组当作掩码，从数组中选取相应的元素：

**输入：**

```python
ary[(ary > 3) & (ary % 2 == 0)]
```

**输出：**

```python
array([4, 6])
```

注意，使用布尔数组进行索引同样被视为「花式索引」，因此返回的是数组的副本。

## 4.6：随机数生成器

### 随机数生成器

在机器学习和深度学习中，我们经常需要生成随机数数组——例如优化前模型参数的初始值。NumPy 提供了一个 `random` 子包，可以方便地生成随机数以及来自各种分布的样本。同样，建议你浏览更全面的 [numpy.random 文档](https://docs.scipy.org/doc/numpy-1.14.0/reference/routines.random.html)，了解随机采样函数的完整列表。

为了简要概述我们最常用的伪随机数生成器，先从均匀分布中抽取随机样本开始：

**输入：**

```python
np.random.seed(123)

np.random.rand(3)
```

**输出：**

```python
array([0.69646919, 0.28613933, 0.22685145])
```

在上面的代码片段中，我们首先为 NumPy 的随机数生成器设置了种子（seed），然后通过 `random.rand` 从半开区间 [0, 1) 的均匀分布中抽取了三个随机样本。无论在应用实践还是研究项目中，我都强烈建议进行设定种子这一步，因为它能保证我们的结果可复现。如果我们按顺序运行代码——例如执行一个 Python 脚本——那么通常只需在开头设置一次种子，就足以保证不同次运行之间结果可复现。不过，为代码的不同部分创建独立的 `RandomState` 对象往往也很有用，这样我们就可以在单元测试中可靠地测试函数的方法。当我们以非顺序方式运行代码时——例如在交互式会话或 Jupyter Notebook 环境中试验代码——使用多个独立的 `RandomState` 对象同样有帮助。

下面的例子展示了如何使用 `RandomState` 对象来复现前一个代码片段中通过 `np.random.rand` 得到的结果：

**输入：**

```python
rng2 = np.random.RandomState(seed=531)
rng2.rand(3)
```

**输出：**

```python
array([0.68980796, 0.35494577, 0.94994208])
```

此外，NumPy 开发者社区在近期的 NumPy 版本中开发了新的随机数生成方法。更多细节请参阅[新的随机 `Generator` 文档](https://numpy.org/doc/stable/reference/random/generator.html#numpy.random.default_rng)：

**输入：**

```python
rng2 = np.random.default_rng(seed=123)
rng2.random(3)
```

**输出：**

```python
array([0.68235186, 0.05382102, 0.22035987])
```

## 4.7：重塑 NumPy 数组

### 数组重塑

在实践中，我们经常会遇到现有数组不具备执行某些计算所需的*正确*形状的情况。你可能还记得本文开头讲过，NumPy 数组的大小是固定的。幸运的是，这并不意味着当我们想要不同形状的数组时，就必须创建新数组并把旧数组的值复制过去——大小是固定的，但形状不是。NumPy 提供了 `reshape` 方法，让我们可以获得具有不同形状的数组视图。

例如，我们可以用 `reshape` 把一维数组重塑为二维数组，如下所示：

**输入：**

```python
ary1d = np.array([1, 2, 3, 4, 5, 6])
ary2d_view = ary1d.reshape(2, 3)
ary2d_view
```

**输出：**

```python
array([[1, 2, 3],
       [4, 5, 6]])
```

`np.may_share_memory` 返回的 `True` 值表明 reshape 操作返回的是内存视图，而不是副本：

**输入：**

```python
np.may_share_memory(ary2d_view, ary1d)
```

**输出：**

```python
True
```

虽然我们需要为每个轴指定期望的元素数，但必须确保重塑后的数组与原数组具有相同的元素总数。不过，我们并不需要指定每个轴上的元素数量；只要有一个轴未指定（使用占位符 `-1`），NumPy 就足够聪明，能算出该轴上应放置多少元素：

**输入：**

```python
ary1d.reshape(-1, 2)
```

**输出：**

```python
array([[1, 2],
       [3, 4],
       [5, 6]])
```

当然，我们也可以用 `reshape` 把数组展平：

**输入：**

```python
ary = np.array([[[1, 2, 3],
                 [4, 5, 6]]])

ary.reshape(-1)
```

**输出：**

```python
array([1, 2, 3, 4, 5, 6])
```

还有其他展平数组的方法，即 `flatten`（创建数组的副本）和 `ravel`（像 reshape 一样创建内存视图）：

**输入：**

```python
ary.flatten()
```

**输出：**

```python
array([1, 2, 3, 4, 5, 6])
```

**输入：**

```python
ary.ravel()
```

**输出：**

```python
array([1, 2, 3, 4, 5, 6])
```

有时我们想把不同的数组合并起来。遗憾的是，由于 NumPy 数组大小固定，若不创建新数组，就没有高效的办法完成这件事。虽然出于计算效率的考虑应尽量避免合并数组，但有时这是必要的。要合并两个或多个数组对象，可以使用 NumPy 的 `concatenate` 函数，如下例所示：

**输入：**

```python
ary = np.array([1, 2, 3])

# stack along the first axis
np.concatenate((ary, ary))
```

**输出：**

```python
array([1, 2, 3, 1, 2, 3])
```

**输入：**

```python
ary = np.array([[1, 2, 3]])

# stack along the first axis (here: rows)
np.concatenate((ary, ary), axis=0)
```

**输出：**

```python
array([[1, 2, 3],
       [1, 2, 3]])
```

**输入：**

```python
# stack along the second axis (here: column)
np.concatenate((ary, ary), axis=1)
```

**输出：**

```python
array([[1, 2, 3, 1, 2, 3]])
```

## 4.8：NumPy 比较运算符与掩码

### 比较运算符与掩码

*4.5 节*已经简要介绍了 NumPy 中布尔掩码的概念。布尔掩码是 `bool` 类型的数组（存储 `True` 和 `False` 值），其形状与某个目标数组相同。例如，考虑下面这个包含 4 个元素的数组。使用比较运算符（如 `<`、`>`、`<=` 和 `>=`），我们可以为该数组创建布尔掩码，其中元素为 `True` 还是 `False` 取决于目标数组（这里是 `ary`）中相应位置是否满足条件：

**输入：**

```python
ary = np.array([1, 2, 3, 4, 5])
mask = ary > 2
mask
```

**输出：**

```python
array([False, False,  True,  True,  True])
```

创建好这样的布尔掩码后，我们就可以用它从目标数组中选取特定的条目——即满足创建掩码时所用条件的那些条目：

**输入：**

```python
ary[mask]
```

**输出：**

```python
array([3, 4, 5])
```

除了从数组中选取元素之外，当我们想统计数组中有多少元素满足某个条件时，布尔掩码也很有用：

**输入：**

```python
mask.sum()
```

**输出：**

```python
3
```

一个相关的、用于给数组中特定元素赋值的有用函数是 `np.where`。在下面的例子中，我们把数组中所有大于 2 的值赋为 1，其余赋为 0：

**输入：**

```python
ary = np.array([1, 2, 3, 4, 5])

np.where(ary > 2, 1, 0)
```

**输出：**

```python
array([0, 0, 1, 1, 1])
```

还有所谓的按位运算符（bit-wise operators），可以用来表达更复杂的选择条件：

**输入：**

```python
ary = np.array([1, 2, 3, 4, 5])
mask = ary > 2
ary[mask] = 1
ary[~mask] = 0
ary
```

**输出：**

```python
array([0, 0, 1, 1, 1])
```

上面例子中的 `~` 运算符是 NumPy 逻辑运算符之一：

- 与（A）：`&` 或 `np.bitwise_and`
- 或（Or）：`|` 或 `np.bitwise_or`
- 异或（Xor）：`^` 或 `np.bitwise_xor`
- 非（Not）：`~` 或 `np.bitwise_not`

这些逻辑运算符让我们可以把任意数量的条件串联起来，创建更「复杂」的布尔掩码。例如，使用「或」运算符，我们可以如下选取所有大于 3 或小于 2 的元素：

**输入：**

```python
ary = np.array([1, 2, 3, 4, 5])

ary[(ary > 3) | (ary < 2)]
```

**输出：**

```python
array([1, 4, 5])
```

又如，要对条件取反，可以使用 `~` 运算符：

**输入：**

```python
ary[~((ary > 3) | (ary < 2))]
```

**输出：**

```python
array([2, 3])
```

## 4.9：用 NumPy 做线性代数

### 用 NumPy 数组做线性代数

直观上，我们可以把一维 NumPy 数组看作表示行向量的数据结构：

**输入：**

```python
row_vector = np.array([1, 2, 3])
row_vector
```

**输出：**

```python
array([1, 2, 3])
```

类似地，我们可以用二维数组创建列向量：

**输入：**

```python
column_vector = np.array([1, 2, 3]).reshape(-1, 1)
column_vector
```

**输出：**

```python
array([[1],
       [2],
       [3]])
```

除了把一维数组重塑为二维数组，我们也可以简单地添加一个新轴，如下所示：

**输入：**

```python
row_vector[:, np.newaxis]
```

**输出：**

```python
array([[1],
       [2],
       [3]])
```

注意，在这个语境下，`np.newaxis` 的行为就像 `None`：

**输入：**

```python
row_vector[:, None]
```

**输出：**

```python
array([[1],
       [2],
       [3]])
```

上面列出的三种方法——使用 `reshape(-1, 1)`、`np.newaxis` 或 `None`——都会得到相同的结果：三者创建的都是 `row_vector` 数组的视图，而不是副本。

我们可以把列向量看作只有一列的矩阵。做矩阵与矩阵的乘法时，我们学过：左矩阵的列数必须与右矩阵的行数相匹配。在 NumPy 中，可以通过 `matmul` 函数执行矩阵乘法：

**输入：**

```python
matrix = np.array([[1, 2, 3], 
                   [4, 5, 6]])
```

**输入：**

```python
np.matmul(matrix, column_vector)
```

**输出：**

```python
array([[14],
       [32]])
```

![Drawing](https://sebastianraschka.com/images/blog/2020/numpy-intro/matmul.webp)

不过，当处理矩阵和向量时，得益于广播，即使矩阵与一维数组的维度并非严格匹配，NumPy 也相当宽容。下面的例子与矩阵乘列向量的结果相同，只是返回的是一维数组而不是二维数组：

**输入：**

```python
np.matmul(matrix, row_vector)
```

**输出：**

```python
array([14, 32])
```

类似地，我们可以计算两个向量的点积（这里是向量的范数）

**输入：**

```python
np.matmul(row_vector, row_vector)
```

**输出：**

```python
14
```

NumPy 还有一个特殊的 `dot` 函数，在处理一维或二维数组对时行为与 `matmul` 类似——不过其底层实现不同，在特定的机器和 [BLAS](https://en.wikipedia.org/wiki/Basic_Linear_Algebra_Subprograms) 版本上，两者中某一个可能会略快：

**输入：**

```python
np.dot(matrix, row_vector)
```

**输出：**

```python
array([14, 32])
```

注意，执行 `np.dot` 还有一个更方便的方式：在 NumPy 数组上使用 `@` 符号：

**输入：**

```python
matrix @ row_vector
```

**输出：**

```python
array([14, 32])
```

与上面的例子类似，我们可以用 `matmul` 或 `dot` 来做两个矩阵（这里是二维数组）的乘法。在这个语境下，NumPy 数组有一个便捷的 `transpose` 方法，可以在需要时转置矩阵：

**输入：**

```python
matrix = np.array([[1, 2, 3], 
                   [4, 5, 6]])

matrix.transpose()
```

**输出：**

```python
array([[1, 4],
       [2, 5],
       [3, 6]])
```

![Drawing](https://sebastianraschka.com/images/blog/2020/numpy-intro/transpose.webp)

**输入：**

```python
np.dot(matrix, matrix.transpose())
```

**输出：**

```python
array([[14, 32],
       [32, 77]])
```

![Drawing](https://sebastianraschka.com/images/blog/2020/numpy-intro/matmatmul.webp)

在实现线性代数运算时，`transpose` 的写法可能冗长得让人恼火——想想 [PEP8](https://www.python.org/dev/peps/pep-0008/) 的*每行 80 字符*建议——NumPy 为此提供了一个简写：`T`：

**输入：**

```python
matrix.T
```

**输出：**

```python
array([[1, 4],
       [2, 5],
       [3, 6]])
```

本节演示了我们在实践中用到的一些基于 NumPy 数组的基本线性代数运算，更多的函数可以在 NumPy 线性代数子模块的文档中找到：[`numpy.linalg`](https://docs.scipy.org/doc/numpy/reference/routines.linalg.html)。如果你想执行某个 NumPy 中未实现的线性代数例程，也值得查阅 [`scipy.linalg` 文档](https://docs.scipy.org/doc/scipy/reference/linalg.html)——SciPy 是构建在 NumPy 之上的科学计算库。

---

我想提一下，NumPy 中还有一种特殊的 [`matrix`](https://docs.scipy.org/doc/numpy/reference/generated/numpy.matrix.html) 类型。NumPy 的 `matrix` 对象与 NumPy 数组类似，但被限制为二维。此外，矩阵对某些运算的定义与数组不同；例如，`*` 运算符执行的是矩阵乘法而不是逐元素乘法。不过，与更通用的数组数据结构相比，NumPy 的 `matrix` 在科学界的受欢迎程度较低。

---

### SciPy

SciPy 是 Python 科学计算技术栈中的另一个开源库。SciPy 包含用于积分、优化以及许多其他计算的子模块，这些超出了 NumPy 本身的范围。本文不会把 SciPy 作为一个库来介绍，因为它更像是构建在 NumPy 之上的一个「附加」库。

建议你浏览 SciPy 文档，简要了解该库中存在的各种函数：<https://docs.scipy.org/doc/scipy/reference/>

## 4.10：Matplotlib

### Matplotlib 是什么？

最后，本文将简要介绍 Matplotlib。Matplotlib 是由 John D. Hunter 于 2003 年创建的 Python 绘图库。遗憾的是，John D. Hunter 于 2012 年因病去世。不过，Matplotlib 仍是最成熟的绘图库，并且至今仍在维护之中。

总体而言，Matplotlib 是一个相当「低层」的绘图库，这意味着它有很大的定制空间。Matplotlib 的优点在于高度可定制；缺点也在于高度可定制——由于选项繁多，有些人觉得它有点过于繁琐。

无论如何，Matplotlib 都是使用最广泛的绘图库之一，是许多数据科学家以及机器学习研究者和从业者的首选。

在我看来，使用 Matplotlib 的最佳方式是经常参考官方网站 <https://matplotlib.org/gallery/index.html> 上的 Matplotlib 图例库（gallery）。其中包含创建各种不同图表的代码示例，可以作为创建自己图表的模板。另外，如果你对 Matplotlib 完全陌生，我推荐 <https://matplotlib.org/tutorials/index.html> 上的教程。

本节我们来看几个非常简单的例子，它们应该非常直观，不需要太多解释。

**输入：**

```python
%matplotlib inline
import matplotlib.pyplot as plt
```

Matplotlib 的主要绘图函数都包含在 pyplot 模块中，我们已经在上面导入了它。注意，`%matplotlib inline` 命令是一个「IPython magic」命令。这个特定的 `%matplotlib inline` 命令是 Jupyter notebook（在我们的例子中使用 IPython 内核）特有的，用于「内联」显示图表，也就是直接显示在 notebook 本身中。

#### 绘制函数与直线

**输入：**

```python
x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x))

plt.show()
```

**输出：**

![Numpy intro plot 1](https://sebastianraschka.com/images/blog/2020/numpy-intro/plot-1.webp)

添加坐标轴范围和标签：

**输入：**

```python
x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x))

plt.xlim([2, 8])
plt.ylim([0, 0.75])

plt.xlabel('x-axis')
plt.ylabel('y-axis')

plt.show()
```

**输出：**

![In:](https://sebastianraschka.com/images/blog/2020/numpy-intro/plot-2.webp)

**输入：**

```python
x = np.linspace(0, 10, 10)

plt.plot(x, np.sin(x), label=('sin(x)'), linestyle='', marker='o')

plt.ylabel('f(x)')
plt.xlabel('x')

plt.legend(loc='lower left')
plt.show()
```

**输出：**

![Numpy intro plot 3](https://sebastianraschka.com/images/blog/2020/numpy-intro/plot-3.webp)

### 散点图

**输入：**

```python
rng = np.random.RandomState(123)
x = rng.normal(size=500)
y = rng.normal(size=500)

plt.scatter(x, y)
plt.show()
```

**输出：**

![Numpy intro plot 4](https://sebastianraschka.com/images/blog/2020/numpy-intro/plot-4.webp)

#### 条形图

**输入：**

```python
# input data
means = [5, 8, 10]
stddevs = [0.2, 0.4, 0.5]
bar_labels = ['bar 1', 'bar 2', 'bar 3']

# plot bars
x_pos = list(range(len(bar_labels)))
plt.bar(x_pos, means, yerr=stddevs)

plt.show()
```

**输出：**

![Numpy intro plot 5](https://sebastianraschka.com/images/blog/2020/numpy-intro/plot-5.webp)

#### 直方图

**输入：**

```python
rng = np.random.RandomState(123)
x = rng.normal(0, 20, 1000) 

# fixed bin size
bins = np.arange(-100, 100, 5) # fixed bin size

plt.hist(x, bins=bins)
plt.show()
```

**输出：**

![In:](https://sebastianraschka.com/images/blog/2020/numpy-intro/plot-6.webp)

**输入：**

```python
rng = np.random.RandomState(123)
x1 = rng.normal(0, 20, 1000) 
x2 = rng.normal(15, 10, 1000)

# fixed bin size
bins = np.arange(-100, 100, 5) # fixed bin size

plt.hist(x1, bins=bins, alpha=0.5)
plt.hist(x2, bins=bins, alpha=0.5)
plt.show()
```

**输出：**

![Numpy intro plot 7](https://sebastianraschka.com/images/blog/2020/numpy-intro/plot-7.webp)

#### 子图

**输入：**

```python
x = range(11)
y = range(11)

fig, ax = plt.subplots(nrows=2, ncols=3,
                       sharex=True, sharey=True)

for row in ax:
    for col in row:
        col.plot(x, y)
        
plt.show()
```

**输出：**

![Numpy intro plot 8](https://sebastianraschka.com/images/blog/2020/numpy-intro/plot-8.webp)

#### 颜色与标记

**输入：**

```python
x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x),
         color='blue',
         marker='^',
         linestyle='')
plt.show()
```

**输出：**

![Numpy intro plot 9](https://sebastianraschka.com/images/blog/2020/numpy-intro/plot-9.webp)

#### 保存图表

保存图表的文件格式可以通过文件后缀（.eps、.svg、.jpg、.png、.pdf、.tiff 等）方便地指定。就个人而言，我建议在可能的情况下使用矢量图形格式（.eps、.svg、.pdf），它通常比位图图形（.jpg、.png、.bmp、tiff）文件更小，而且分辨率不受限制。

**输入：**

```python
x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x))

plt.savefig('myplot.png', dpi=300)
plt.savefig('myplot.pdf')

plt.show()
```

**输出：**

![Numpy intro plot 10](https://sebastianraschka.com/images/blog/2020/numpy-intro/plot-10.webp)

感谢阅读/观看。如果你喜欢这些内容，也可以在 [Twitter 上找到我](https://twitter.com/rasbt)，我在那里分享更多有用的内容。

## 参考资料

NumPy 与 Matplotlib 参考资料：

- [NumPy 官方文档](https://docs.scipy.org/doc/numpy/reference/index.html)
- [Matplotlib 官方图例库](https://matplotlib.org/gallery/index.html)
- [Matplotlib 官方教程](https://matplotlib.org/tutorials/index.html)

NumPy 相关书籍、教程与论文：

- Rougier, N.P., 2016. [From Python to NumPy](http://www.labri.fr/perso/nrougier/from-python-to-numpy/).
- Oliphant, T.E., 2015. [A Guide to NumPy: 2nd Edition](https://www.amazon.com/Guide-NumPy-Travis-Oliphant-PhD/dp/151730007X). USA: Travis Oliphant, independent publishing.
- Varoquaux, G., Gouillart, E., Vahtras, O., Haenel, V., Rougier, N.P., Gommers, R., Pedregosa, F., Jędrzejewski-Szmek, Z., Virtanen, P., Combelles, C. and Pinte, D., 2015. [SciPy Lecture Notes](https://scipy-lectures.org/intro/numpy/index.html).
- Harris, C.R., Millman, K.J., van der Walt, S.J. et al. [Array Programming with NumPy](https://www.nature.com/articles/s41586-020-2649-2). Nature 585, 357–362 (2020).
