---
title: "Python 多进程入门"
title_en: "Python Multiprocessing Introduction"
source: https://sebastianraschka.com/Articles/2014_multiprocessing.html
crawled: 2026-09-06
translated: 2026-09-14
---

# Python 多进程入门

> 原文：[Python Multiprocessing Introduction](https://sebastianraschka.com/Articles/2014_multiprocessing.html) · Sebastian Raschka's Articles

多核 CPU 已经成为现代计算机架构近期发展中的标准配置，我们不仅能在超级计算设施中见到它们，也能在家里的台式机和笔记本电脑中见到；就连 Apple 的 iPhone 5S 在 2013 年也用上了 1.3 GHz 的双核处理器。

然而，默认的 Python 解释器在设计上以简单为宗旨，带有一个线程安全机制，即所谓的「GIL」（全局解释器锁，Global Interpreter Lock）。为了防止线程之间发生冲突，它一次只执行一条语句（即所谓的串行处理，或称单线程）。

在这篇 Python `multiprocessing` 模块的入门文章中，我们将看到如何启动多个子进程，以规避 GIL 的一些缺点。

### 章节

### 多线程 vs. 多进程

视具体应用而定，并行编程中有两种常见的做法：分别通过线程或多个进程来运行代码。如果我们向不同的线程提交「作业」（job），这些作业可以被看作单个进程的「子任务」，而这些线程通常可以访问相同的内存区域（即共享内存）。一旦同步不当，这种方式很容易引发冲突，例如当多个进程同时写入同一内存位置时。

一种更安全的做法（尽管由于独立进程之间的通信开销会带来额外负担）是让多个进程运行在完全分离的内存位置上（即分布式内存）：每个进程都将完全独立地运行。

在本文中，我们将了解 Python 的 [`multiprocessing`](https://docs.python.org/dev/library/multiprocessing.html) 模块，看看如何利用它提交多个可以彼此独立运行的进程，从而充分利用我们的 CPU 核心。

![Multiprocessing intro multiprocessing scheme](https://sebastianraschka.com/images/blog/2014/multiprocessing_intro/multiprocessing_scheme.webp)

## `multiprocessing` 模块简介

Python 标准库中的 [multiprocessing](https://docs.python.org/dev/library/multiprocessing.html) 模块拥有许多强大的功能。如果你想了解所有细枝末节的技巧、窍门和细节，我建议以[官方文档](https://docs.python.org/dev/library/multiprocessing.html)作为入口。

在接下来的几节中，我想简要概述几种不同的方法，展示如何将 `multiprocessing` 模块用于并行编程。

### `Process` 类

最基本的方法大概是使用 `multiprocessing` 模块中的 `Process` 类。  
这里，我们将使用一个简单的队列函数来并行地生成四个随机字符串。

```python
import multiprocessing as mp
import random
import string

random.seed(123)

# Define an output queue
output = mp.Queue()

# define a example function
def rand_string(length, output):
    """ Generates a random string of numbers, lower- and uppercase chars. """
    rand_str = ''.join(random.choice(
                        string.ascii_lowercase
                        + string.ascii_uppercase
                        + string.digits)
                   for i in range(length))
    output.put(rand_str)

# Setup a list of processes that we want to run
processes = [mp.Process(target=rand_string, args=(5, output)) for x in range(4)]

# Run processes
for p in processes:
    p.start()

# Exit the completed processes
for p in processes:
    p.join()

# Get process results from the output queue
results = [output.get() for p in processes]

print(results)
```

```python
['BJWNs', 'GOK0H', '7CTRJ', 'THDF3']
```

### 如何按特定顺序获取结果

所获结果的顺序不一定与进程的顺序（`processes` 列表中的顺序）一致。由于我们最终是使用 `.get()` 方法按顺序从 `Queue` 中取出结果，因此进程完成的先后顺序决定了结果的顺序。  
例如，如果第二个进程恰好在第一个进程之前完成，那么 `results` 列表中字符串的顺序也可能是
`['PQpqM', 'yzQfA', 'SHZYV', 'PSNkD']`，而不是 `['yzQfA', 'PQpqM', 'SHZYV', 'PSNkD']`。

如果我们的应用要求按特定顺序获取结果，一种可行的办法是借助进程的 `._identity` 属性。就这个例子而言，我们也可以直接把 `range` 对象的值作为位置参数传入。修改后的代码如下：

```python
# Define an output queue
output = mp.Queue()

# define a example function
def rand_string(length, pos, output):
    """ Generates a random string of numbers, lower- and uppercase chars. """
    rand_str = ''.join(random.choice(
                        string.ascii_lowercase
                        + string.ascii_uppercase
                        + string.digits)
                   for i in range(length))
    output.put((pos, rand_str))

# Setup a list of processes that we want to run
processes = [mp.Process(target=rand_string, args=(5, x, output)) for x in range(4)]

# Run processes
for p in processes:
    p.start()

# Exit the completed processes
for p in processes:
    p.join()

# Get process results from the output queue
results = [output.get() for p in processes]

print(results)
```

```python
[(0, 'h5hoV'), (1, 'fvdmN'), (2, 'rxGX4'), (3, '8hDJj')]
```

取回的结果将是元组，例如 `[(0, 'KAQo6'), (1, '5lUya'), (2, 'nj6Q0'), (3, 'QQvLr')]`   
或者 `[(1, '5lUya'), (3, 'QQvLr'), (0, 'KAQo6'), (2, 'nj6Q0')]`。

为了确保按顺序取回结果，我们只需对结果排序，并可以选择去掉位置参数：

```python
results.sort()
results = [r[1] for r in results]
print(results)
```

```python
['h5hoV', 'fvdmN', 'rxGX4', '8hDJj']
```

**维护一个有序结果列表的更简单方法是使用 `Pool.apply` 和 `Pool.map` 函数，我们将在下一节中讨论它们。**

### `Pool` 类

对于简单的并行处理任务，`Pool` 类提供了另一种更便捷的方法。

有四个方法特别值得关注：

- `Pool.apply`
- `Pool.map`
- `Pool.apply_async`
- `Pool.map_async`

`Pool.apply` 和 `Pool.map` 方法基本上等价于 Python 内置的 [`apply`](https://docs.python.org/2/library/functions.html#apply) 和 [`map`](https://docs.python.org/2/library/functions.html#map) 函数。

在讨论 `Pool` 方法的 `async` 变体之前，先来看一个使用 `Pool.apply` 和 `Pool.map` 的简单例子。这里我们会把进程数设为 4，这意味着 `Pool` 类最多只允许 4 个进程同时运行。

```python
def cube(x):
    return x**3
```

```python
pool = mp.Pool(processes=4)
results = [pool.apply(cube, args=(x,)) for x in range(1,7)]
print(results)
```

```python
[1, 8, 27, 64, 125, 216]
```

```python
pool = mp.Pool(processes=4)
results = pool.map(cube, range(1,7))
print(results)
```

```python
[1, 8, 27, 64, 125, 216]
```

`Pool.map` 和 `Pool.apply` 会阻塞主程序，直到所有进程结束为止；如果我们希望在特定应用中按特定顺序获得结果，这一特性相当有用。   
相比之下，`async` 变体会一次性提交所有进程，并在各进程一结束后就取回结果。
另一个区别是，在调用 `apply_async()` 之后，我们还需要使用 `get` 方法才能获得已完成进程的 `return` 值。

```python
pool = mp.Pool(processes=4)
results = [pool.apply_async(cube, args=(x,)) for x in range(1,7)]
output = [p.get() for p in results]
print(output)
```

```python
[1, 8, 27, 64, 125, 216]
```

## 用核密度估计作为基准测试函数

接下来，我想对串行方式与多进程方式做一个简单的对比，其中会使用一个比前面用过的 `cube` 例子稍微复杂一点的函数。

在这里，我定义了一个函数，使用 Parzen 窗（Parzen-window）技术对概率密度函数执行核密度估计。  
我不想深入讨论这种技术的理论，因为我们主要关心的是如何利用 `multiprocessing` 来提升性能；不过欢迎阅读我写的关于 [Parzen 窗方法的更详细的文章](https://sebastianraschka.com/Articles/2014_kernel_density_est.html)。

```python
import numpy as np

def parzen_estimation(x_samples, point_x, h):
    """
    Implementation of a hypercube kernel for Parzen-window estimation.

    Keyword arguments:
        x_sample:training sample, 'd x 1'-dimensional numpy array
        x: point x for density estimation, 'd x 1'-dimensional numpy array
        h: window width

    Returns the predicted pdf as float.

    """
    k_n = 0
    for row in x_samples:
        x_i = (point_x - row[:,np.newaxis]) / (h)
        for row in x_i:
            if np.abs(row) > (1/2):
                break
        else: # "completion-else"*
            k_n += 1
    return (k_n / len(x_samples)) / (h**point_x.shape[1])
```

---

**关于「completion else」的简要说明**

有时我会收到评论，问我这个 for-else 组合是有意为之还是无心之失。这是个合理的问题，因为这种「completion-else」（完结 else）很少被使用（这是我对它的称呼，我不知道它是否有「官方」名称，如果有的话，请告诉我）。  
我在一篇博文中给出了[更详细的解释](https://sebastianraschka.com/Articles/2014_deep_python.html#else-clauses-conditional-else-and-completion-else)，简单来说：与条件 else（与 if 语句搭配使用）不同，「completion else」只在前面的代码块（这里是 `for` 循环）完整执行完毕之后才会执行。

---

### Parzen 窗方法简介

简单来说，这个函数做的是：统计某个定义区域（即所谓的「窗」）内的点数，再用窗内的点数除以总点数，从而估计单个点落在某一区域内的概率。

下面是一个简单的例子：我们的窗用一个中心位于原点的超立方体（hypercube）表示，我们要基于这个超立方体来估计一个点位于图形中心的概率。

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

![Multiprocessing intro 2014 06 20 multiprocessing intro 49 0](https://sebastianraschka.com/images/blog/2014/multiprocessing_intro/2014-06-20-multiprocessing_intro_49_0.webp)

```python
point_x = np.array([[0],[0],[0]])
X_all = np.vstack((X_inside,X_outside))

print('p(x) =', parzen_estimation(X_all, point_x, h=1))
```

```python
p(x) = 0.3
```

### 样本数据与 `timeit` 基准测试

在下面这一节中，我们将从一个二元高斯分布中创建一个随机数据集，该分布的均值向量以原点为中心，协方差矩阵为单位矩阵。

```python
import numpy as np

np.random.seed(123)

# Generate random 2D-patterns
mu_vec = np.array([0,0])
cov_mat = np.array([[1,0],[0,1]])
x_2Dgauss = np.random.multivariate_normal(mu_vec, cov_mat, 10000)
```

正如下面将看到的，位于分布中心的点的期望概率约为 0.15915。  
我们的目标是使用 Parzen 窗方法，基于上面创建的样本数据集来预测这个密度。

要想通过 Parzen 窗技术做出「好」的预测，选择合适的窗宽至关重要（除此之外还有其他要点）。这里，我们将使用多个进程、以不同的窗宽来预测二元高斯分布中心的密度。

```python
from scipy.stats import multivariate_normal
var = multivariate_normal(mean=[0,0], cov=[[1,0],[0,1]])
print('actual probability density:', var.pdf([0,0]))
```

```python
actual probability density: 0.159154943092
```

### 基准测试函数

下面，我们将为串行方式和多进程方式分别编写基准测试函数，以便传给我们的 `timeit` [基准测试](https://sebastianraschka.com/glossary/#benchmark "Benchmark")函数。  
我们将使用 `Pool.apply_async` 函数来发挥同时启动多个进程的优势：这里我们并不关心不同窗宽的结果以什么顺序计算出来，只需要把每个结果与输入的窗宽关联起来即可。  
因此，我们对 Parzen 密度估计函数做了一点小改动：让它返回一个包含两个值的元组——窗宽和估计出的密度——这样之后我们就能对结果列表排序。

```python
def parzen_estimation(x_samples, point_x, h):
    k_n = 0
    for row in x_samples:
        x_i = (point_x - row[:,np.newaxis]) / (h)
        for row in x_i:
            if np.abs(row) > (1/2):
                break
        else: # "completion-else"*
            k_n += 1
    return (h, (k_n / len(x_samples)) / (h**point_x.shape[1]))
```

```python
def serial(samples, x, widths):
    return [parzen_estimation(samples, x, w) for w in widths]

def multiprocess(processes, samples, x, widths):
    pool = mp.Pool(processes=processes)
    results = [pool.apply_async(parzen_estimation, args=(samples, x, w)) for w in widths]
    results = [p.get() for p in results]
    results.sort() # to sort the results by input window width
    return results
```

先来看看结果大概是什么样子（即不同窗宽下预测出的密度）：

```python
widths = np.arange(0.1, 1.3, 0.1)
point_x = np.array([[0],[0]])
results = []

results = multiprocess(4, x_2Dgauss, point_x, widths)

for r in results:
    print('h = %s, p(x) = %s' %(r[0], r[1]))
```

```python
h = 0.1, p(x) = 0.016
h = 0.2, p(x) = 0.0305
h = 0.3, p(x) = 0.045
h = 0.4, p(x) = 0.06175
h = 0.5, p(x) = 0.078
h = 0.6, p(x) = 0.0911666666667
h = 0.7, p(x) = 0.106
h = 0.8, p(x) = 0.117375
h = 0.9, p(x) = 0.132666666667
h = 1.0, p(x) = 0.1445
h = 1.1, p(x) = 0.157090909091
h = 1.2, p(x) = 0.1685
```

根据这些结果，我们可以说最佳窗宽是 h=1.1，因为估计结果与真实值 ~0.15915 很接近。  
因此，在进行基准测试时，让我们在 1.0 到 1.2 的范围内创建 100 个均匀间隔的窗宽。

```python
widths = np.linspace(1.0, 1.2, 100)
```

```python
import timeit

mu_vec = np.array([0,0])
cov_mat = np.array([[1,0],[0,1]])
n = 10000

x_2Dgauss = np.random.multivariate_normal(mu_vec, cov_mat, n)

benchmarks = []

benchmarks.append(timeit.Timer('serial(x_2Dgauss, point_x, widths)',
            'from __main__ import serial, x_2Dgauss, point_x, widths').timeit(number=1))

benchmarks.append(timeit.Timer('multiprocess(2, x_2Dgauss, point_x, widths)',
            'from __main__ import multiprocess, x_2Dgauss, point_x, widths').timeit(number=1))

benchmarks.append(timeit.Timer('multiprocess(3, x_2Dgauss, point_x, widths)',
            'from __main__ import multiprocess, x_2Dgauss, point_x, widths').timeit(number=1))

benchmarks.append(timeit.Timer('multiprocess(4, x_2Dgauss, point_x, widths)',
            'from __main__ import multiprocess, x_2Dgauss, point_x, widths').timeit(number=1))

benchmarks.append(timeit.Timer('multiprocess(6, x_2Dgauss, point_x, widths)',
            'from __main__ import multiprocess, x_2Dgauss, point_x, widths').timeit(number=1))
```

### 准备绘制结果

```python
import platform

def print_sysinfo():

    print('\nPython version  :', platform.python_version())
    print('compiler        :', platform.python_compiler())

    print('\nsystem     :', platform.system())
    print('release    :', platform.release())
    print('machine    :', platform.machine())
    print('processor  :', platform.processor())
    print('CPU count  :', mp.cpu_count())
    print('interpreter:', platform.architecture()[0])
    print('\n\n')
```

```python
from matplotlib import pyplot as plt
import numpy as np

def plot_results():
    bar_labels = ['serial', '2', '3', '4', '6']

    fig = plt.figure(figsize=(10,8))

    # plot bars
    y_pos = np.arange(len(benchmarks))
    plt.yticks(y_pos, bar_labels, fontsize=16)
    bars = plt.barh(y_pos, benchmarks,
             align='center', alpha=0.4, color='g')

    # annotation and labels

    for ba,be in zip(bars, benchmarks):
        plt.text(ba.get_width() + 2, ba.get_y() + ba.get_height()/2,
                '{0:.2%}'.format(benchmarks[0]/be),
                ha='center', va='bottom', fontsize=12)

    plt.xlabel('time in seconds for n=%s' %n, fontsize=14)
    plt.ylabel('number of processes', fontsize=14)
    t = plt.title('Serial vs. Multiprocessing via Parzen-window estimation', fontsize=18)
    plt.ylim([-1,len(benchmarks)+0.5])
    plt.xlim([0,max(benchmarks)*1.1])
    plt.vlines(benchmarks[0], -1, len(benchmarks)+0.5, linestyles='dashed')
    plt.grid()

    plt.show()
```

## 结果

```python
plot_results()
print_sysinfo()
```

![Multiprocessing intro 2014 06 20 multiprocessing intro 78 0](https://sebastianraschka.com/images/blog/2014/multiprocessing_intro/2014-06-20-multiprocessing_intro_78_0.webp)

```python
Python version  : 3.4.1
compiler        : GCC 4.2.1 (Apple Inc. build 5577)

system     : Darwin
release    : 13.2.0
machine    : x86_64
processor  : i386
CPU count  : 4
interpreter: 64bit
```

## 结论

可以看到，如果把 Parzen 窗函数的密度估计任务并行提交，我们就能为其提速。然而，在我这台特定的机器上，同时提交 6 个并行进程并不能带来进一步的性能提升——对于一颗 4 核 CPU 来说这是合理的。  
我们还注意到，从只用 2 个并行进程增加到 3 个时，性能有明显提升；而再增加到 4 个并行进程时，性能提升就没那么显著了。  
这可以归因于：在这台机器上，CPU 只有 4 个核心，而操作系统等系统进程也在后台运行。因此，第四个核心剩余的算力已不足以大幅提升第四个进程的性能。此外我们还要记住，每增加一个进程，都会带来额外的进程间通信开销。

另外，只有当任务是「CPU 密集型」（CPU-bound）的——即任务的主要时间都耗费在 CPU 上——并行处理带来的提升才有意义；与之相对的是「I/O 密集型」任务，即那些主要在处理磁盘数据的任务。
