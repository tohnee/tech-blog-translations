---
title: "用 Dixon Q 检验检测离群值"
title_en: "Dixon's Q Test for Outlier Detection"
source: https://sebastianraschka.com/Articles/2014_dixon_test.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 用 Dixon Q 检验检测离群值

> 原文：[Dixon's Q Test for Outlier Detection](https://sebastianraschka.com/Articles/2014_dixon_test.html) · Sebastian Raschka's Articles

最近，我遇到了一个近乎不可能完成的任务：在样本量非常、非常小的数据集中识别离群值，于是 Dixon Q 检验引起了我的注意。说实话，我并不是这种统计检验的拥趸，但由于 Dixon Q 检验在某些科学领域（例如化学）仍然相当流行，理解它的原理十分重要——这样，当你日后在研究论文或学术报告中看到所展示的研究数据时，才能做出自己的判断。

## 章节

Dixon Q 检验 [1] 被人「发明」出来，作为一种便捷的流程，用于在只包含少量观测值的数据集中快速识别离群值：通常 3 > n ≤ 10。

> [1] R. B. Dean and W. J. Dixon (1951) [Simplified Statistics for Small
> Numbers of
> Observations”](http://pubs.acs.org/doi/abs/10.1021/ac60052a025). Anal.
> Chem., 1951, 23 (4), 636–638

### 应用

尽管（至少在我看来）剔除离群值是一种非常有争议的做法，但这种检验在化学领域相当流行，用来「客观地」检测并剔除由实验者的系统误差导致的离群值。

### 批评

如果我们想用这种检验来名正言顺地从数据集中剔除（潜在的）离群值，那么应当牢记：

- 我们的数据必须服从正态分布；
- 而且对同一个数据集，我们不应使用这种检验一次以上。

依我之见，使用 Dixon Q 检验时必须非常谨慎，因为这个简单的统计量建立在数据服从正态分布的假设之上，而在小样本情形下（如果没有先验/额外信息），要判断数据是否正态分布是相当困难的。就我个人而言，我只会用 Dixon Q 检验来**检测**离群值，而不会用它来**剔除**离群值——这有助于识别数据集中的不确定性或实验流程中的问题。直观上讲，这与找出标准差较大的样本的做法颇为相似。

例如，如果我在某种活性实验中测试了约 1000 种化合物——每种化合物测 5 次，我会把含有 Q 检验离群值的化合物标记出来以备重测，因为可能是测量流程中的某个问题导致了这种不一致。

### 方法

#### 1) 将观测值按升序排列

首先，我们将样本数据按升序（从最低值到最高值）排列：

\[x\_1 \le x\_2 \le . . . \le x\_N\]

#### 2) 计算 Q

接下来，我们计算实验 Q 值（\(Q\_{exp}\)）。

请注意，在 1953 年的一篇后续论文中，Dixon 和 Dean [3] 重新审视了 Q 值的计算，并针对不同场景给出了不同的方程：

![Dixon test dixon q equations](https://sebastianraschka.com/images/blog/2014/dixon_test/dixon_q_equations.webp)

（引自：Rorabacher, David B., 1991 [2]）

![Dixon test dixon q equations2](https://sebastianraschka.com/images/blog/2014/dixon_test/dixon_q_equations2.webp)

不过，根据一篇更晚近的论文（Rorabacher, David B., 1991 [2]）中的陈述/观察：「\(r\_{l0}\) 比率通常被记作 'Q'，并且一般被认为是用于从服从高斯分布的小样本中剔除异常值的最便捷、最正当的统计检验。（如果只存在一个离群值，它同样适用于更大的数据集。）」

因此，在下面实现 Dixon Q 检验时，我将使用 \(r\_{l0}\)：

![Dixon test dixon q equations3](https://sebastianraschka.com/images/blog/2014/dixon_test/dixon_q_equations3.webp)

其中假设数据已按升序排列：

\[x\_1 \le x\_2 \le . . . \le x\_N\]

---

> [2] Rorabacher, David B. (1991) “[Statistical Treatment for Rejection of
> Deviant Values: Critical Values of Dixon’s‘ Q’ Parameter and Related
> Subrange Ratios at the 95% Confidence
> Level.](http://pubs.acs.org/doi/pdf/10.1021/ac00002a010)” Analytical
> Chemistry 63, no. 2 (1991): 139–46.

> [3] W.J. Dixon: [Processing data for outliers
> Reference”](http://webspace.ship.edu/pgmarr/Geo441/Readings/Dixon%201953%20-%20Processing%20Data%20for%20Outliers.pdf):
> J. Biometrics 9 (1953) 74-89

#### 3) 将计算得到的 Q 值与查表得到的临界 Q 值进行比较

下一步，我们将计算得到的 \(Q\_{exp}\) 值与选定置信区间下查表得到的临界 Q 值 \(Q\_{crit}\) 进行比较。
如果某个观测值的计算 Q 值大于临界 Q 值（\(Q\_{exp} \ge Q\_{crit}\)），那么按照 Q 检验，该观测值被视为离群值。

\(r\_{10}\) Dixon 双侧 Q 检验在 3 个不同置信度水平下的临界值\*\*

| N | Q90% | Q95% | Q99% |
| --- | --- | --- | --- |
| 3 | 0.941 | 0.97 | 0.994 |
| 4 | 0.765 | 0.829 | 0.926 |
| 5 | 0.642 | 0.71 | 0.821 |
| 6 | 0.56 | 0.625 | 0.74 |
| 7 | 0.507 | 0.568 | 0.68 |
| 8 | 0.468 | 0.526 | 0.634 |
| 9 | 0.437 | 0.493 | 0.598 |
| 10 | 0.412 | 0.466 | 0.568 |
| 11 | 0.392 | 0.444 | 0.542 |
| 12 | 0.376 | 0.426 | 0.522 |
| 13 | 0.361 | 0.41 | 0.503 |
| 14 | 0.349 | 0.396 | 0.488 |
| 15 | 0.338 | 0.384 | 0.475 |
| 16 | 0.329 | 0.374 | 0.463 |
| 17 | 0.32 | 0.365 | 0.452 |
| 18 | 0.313 | 0.356 | 0.442 |
| 19 | 0.306 | 0.349 | 0.433 |
| 20 | 0.3 | 0.342 | 0.425 |
| 21 | 0.295 | 0.337 | 0.418 |
| 22 | 0.29 | 0.331 | 0.411 |
| 23 | 0.285 | 0.326 | 0.404 |
| 24 | 0.281 | 0.321 | 0.399 |
| 25 | 0.277 | 0.317 | 0.393 |
| 26 | 0.273 | 0.312 | 0.388 |
| 27 | 0.269 | 0.308 | 0.384 |
| 28 | 0.266 | 0.305 | 0.38 |
| 29 | 0.263 | 0.301 | 0.376 |
| 30 | 0.26 | 0.29 | 0.372 |

#### 4) 示例

考虑下面这个由 5 个观测值组成的样本：

0.142, 0.153, 0.135, 0.002, 0.175

- 首先，我们将其按升序排序：0.002, 0.135, 0.142, 0.153, 0.175
- 接下来，我们计算 Q 值：

![Dixon test dixon q equations4](https://sebastianraschka.com/images/blog/2014/dixon_test/dixon_q_equations4.webp)

- 现在，我们在 Q 表中查 n=5、置信度水平 95% 对应的临界值（\(= \ge 0.71\)）

于是我们得出结论（因为 0.7687 > 0.71）：按照 Dixon Q 检验，在 95% 置信度水平下，观测值 0.002 是一个离群值。

### 实现

在接下来的几个小节中，我将用纯 Python 实现 Q 检验。这次我没有使用科学计算栈（sci-stack）中的包（`pandas`、`NumPy`、`scipy`……），因此代码看起来没那么优雅，为此我得先道个歉——这段代码是为一位不用 Python 的人写的，我承诺过让它能在标准的 Python 安装环境下直接运行。

#### 构建用于查询 Q 值的字典

我们将根据 David B. Rorabacher 论文中表格化的数据，为不同置信区间构建一组简单的字典：Rorabacher, David B. (1991) “[Statistical Treatment for Rejection of
Deviant Values: Critical Values of Dixon’s‘ Q’ Parameter and Related
Subrange Ratios at the 95% Confidence
Level.](http://pubs.acs.org/doi/pdf/10.1021/ac00002a010)” Analytical
Chemistry 63, no. 2 (1991): 139–46.

然后，我们就可以用这个字典来查询不同样本量（字典的键）所对应的临界 Q 值（字典的值）。

```python
q90 = [0.941, 0.765, 0.642, 0.56, 0.507, 0.468, 0.437,
       0.412, 0.392, 0.376, 0.361, 0.349, 0.338, 0.329,
       0.32, 0.313, 0.306, 0.3, 0.295, 0.29, 0.285, 0.281,
       0.277, 0.273, 0.269, 0.266, 0.263, 0.26
      ]

q95 = [0.97, 0.829, 0.71, 0.625, 0.568, 0.526, 0.493, 0.466,
       0.444, 0.426, 0.41, 0.396, 0.384, 0.374, 0.365, 0.356,
       0.349, 0.342, 0.337, 0.331, 0.326, 0.321, 0.317, 0.312,
       0.308, 0.305, 0.301, 0.29
      ]

q99 = [0.994, 0.926, 0.821, 0.74, 0.68, 0.634, 0.598, 0.568,
       0.542, 0.522, 0.503, 0.488, 0.475, 0.463, 0.452, 0.442,
       0.433, 0.425, 0.418, 0.411, 0.404, 0.399, 0.393, 0.388,
       0.384, 0.38, 0.376, 0.372
       ]

Q90 = {n:q for n,q in zip(range(3,len(q90)+1), q90)}
Q95 = {n:q for n,q in zip(range(3,len(q95)+1), q95)}
Q99 = {n:q for n,q in zip(range(3,len(q99)+1), q99)}
```

#### 实现 Dixon Q 检验函数

下面是我写的一段简单的 Python 代码，用于对一行数据进行 Dixon Q 检验离群值检测：

```python
def dixon_test(data, left=True, right=True, q_dict=Q95):
    """
    Keyword arguments:
        data = A ordered or unordered list of data points (int or float).
        left = Q-test of minimum value in the ordered list if True.
        right = Q-test of maximum value in the ordered list if True.
        q_dict = A dictionary of Q-values for a given confidence level,
            where the dict. keys are sample sizes N, and the associated values
            are the corresponding critical Q values. E.g.,
            {3: 0.97, 4: 0.829, 5: 0.71, 6: 0.625, ...}

    Returns a list of 2 values for the outliers, or None.
    E.g.,
       for [1,1,1] -> [None, None]
       for [5,1,1] -> [None, 5]
       for [5,1,5] -> [1, None]

    """
    assert(left or right), 'At least one of the variables, `left` or `right`, must be True.'
    assert(len(data) >= 3), 'At least 3 data points are required'
    assert(len(data) <= max(q_dict.keys())), 'Sample size too large'

    sdata = sorted(data)
    Q_mindiff, Q_maxdiff = (0,0), (0,0)

    if left:
        Q_min = (sdata[1] - sdata[0])
        try:
            Q_min /= (sdata[-1] - sdata[0])
        except ZeroDivisionError:
            pass
        Q_mindiff = (Q_min - q_dict[len(data)], sdata[0])

    if right:
        Q_max = abs((sdata[-2] - sdata[-1]))
        try:
            Q_max /= abs((sdata[0] - sdata[-1]))
        except ZeroDivisionError:
            pass
        Q_maxdiff = (Q_max - q_dict[len(data)], sdata[-1])

    if not Q_mindiff[0] > 0 and not Q_maxdiff[0] > 0:
        outliers = [None, None]

    elif Q_mindiff[0] == Q_maxdiff[0]:
        outliers = [Q_mindiff[1], Q_maxdiff[1]]

    elif Q_mindiff[0] > Q_maxdiff[0]:
        outliers = [Q_mindiff[1], None]

    else:
        outliers = [None, Q_maxdiff[1]]

    return outliers
```

#### 断言测试

一些简单的断言测试，用来确保 Dixon Q 检验函数的行为符合预期/期望。

```python
test_data1 = [0.142, 0.153, 0.135, 0.002, 0.175]
test_data2 = [0.542, 0.153, 0.135, 0.002, 0.175]

assert(dixon_test(test_data1) == [0.002, None]), 'expect [0.002, None]'
assert(dixon_test(test_data1, right=False) == [0.002, None]), 'expect [0.002, None]'
assert(dixon_test(test_data2) == [None, None]), 'expect [None, None]'
assert(dixon_test(test_data2, q_dict=Q90) == [None, 0.542]), 'expect [None, 0.542]'

print('ok')
```

```python
ok
```

#### 应用示例

下面，我想用一个示例 CSV 文件，为我们的 Dixon Q 检验函数走一遍最简单的示例流程。在「真实的」应用中，我会更倾向于使用 `NumPy` 和/或 `pandas`，不过对于这个简单的场景，Python 内置的 `csv` 库就够用了。

下面展示的是我们将要读入的示例 CSV 文件：

```python
%%writefile ../../data/dixon_test_in.csv
,x1,x2,x3,x4,x5
id1,0.95,-0.65,0.6,0.82,NaN
id2,2.08,NaN,-1.43,0.38,NaN
id3,-0.46,NaN,-1.25,-2.62,0.22
id4,0.24,1.88,-0.49,-0.73,-0.49
id5,-1.65,2.1,-0.09,NaN,0.8
id6,-0.44,0.93,0.19,-4.36,-0.88
id7,0.36,-0.47,NaN,0.4,2.12
id8,1.29,-0.48,-0.6,-0.38,0.27
id9,-1.25,-1.35,1.13,1.7,-0.81
id10,0.04,1.98,NaN,NaN,NaN
```

```python
import csv

def csv_to_list(csv_file, delimiter=','):
    """
    Reads in a CSV file and returns the contents as list,
    where every row is stored as a sublist, and each element
    in the sublist represents 1 cell in the table.

    """
    with open(csv_file, 'r') as csv_con:
        reader = csv.reader(csv_con, delimiter=delimiter)
        return list(reader)

def print_csv(csv_content):
    """ Prints CSV file to standard output."""
    print(50*'-')
    for row in csv_content:
        row = [str(e) for e in row]
        print('t'.join(row))
    print(50*'-')

def convert_cells_to_floats(csv_cont):
    """
    Converts cells to floats if possible
    (modifies input CSV content list).

    """
    for row in range(len(csv_cont)):
        for cell in range(len(csv_cont[row])):
            try:
                csv_cont[row][cell] = float(csv_cont[row][cell])
            except ValueError:
                pass
```

```python
csv_cont = csv_to_list('../../data/dixon_test_in.csv')
convert_cells_to_floats(csv_cont)
print_csv(csv_cont)
```

```python
--------------------------------------------------
    x1  x2  x3  x4  x5
id1 0.95    -0.65   0.6 0.82    nan
id2 2.08    nan -1.43   0.38    nan
id3 -0.46   nan -1.25   -2.62   0.22
id4 0.24    1.88    -0.49   -0.73   -0.49
id5 -1.65   2.1 -0.09   nan 0.8
id6 -0.44   0.93    0.19    -4.36   -0.88
id7 0.36    -0.47   nan 0.4 2.12
id8 1.29    -0.48   -0.6    -0.38   0.27
id9 -1.25   -1.35   1.13    1.7 -0.81
id10    0.04    1.98    nan nan nan
--------------------------------------------------
```

现在，让我们添加一个新的 `outlier` 列，并对我们的数据集应用 Dixon Q 检验函数。

```python
import math

csv_cont[0].append('outlier')

for row in csv_cont[1:]: # skips header
    nan_removed = [i for i in row[1:] if not math.isnan(i)]
    if len(nan_removed) >= 3:
        row.append(dixon_test(nan_removed, left=True, right=True, q_dict=Q90))
    else:
        row.append('NaN')
```

```python
print_csv(csv_cont)

```python
--------------------------------------------------
    x1  x2  x3  x4  x5  outlier
id1 0.95    -0.65   0.6 0.82    nan [-0.65, None]
id2 2.08    nan -1.43   0.38    nan [None, None]
id3 -0.46   nan -1.25   -2.62   0.22    [None, None]
id4 0.24    1.88    -0.49   -0.73   -0.49   [None, None]
id5 -1.65   2.1 -0.09   nan 0.8 [None, None]
id6 -0.44   0.93    0.19    -4.36   -0.88   [-4.36, None]
id7 0.36    -0.47   nan 0.4 2.12    [None, None]
id8 1.29    -0.48   -0.6    -0.38   0.27    [None, None]
id9 -1.25   -1.35   1.13    1.7 -0.81   [None, None]
id10    0.04    1.98    nan nan nan NaN
--------------------------------------------------
```

从上表可以看出，我们的数据集中有 2 个潜在的离群值。最后，让我们把结果写入一个新的 CSV 文件，以备日后参考：

```python
def write_csv(dest, csv_cont):
    """ Writes a comma-delimited CSV file. """

    with open(dest, 'w') as out_file:
        writer = csv.writer(out_file, delimiter=',')
        for row in csv_cont:
            writer.writerow(row)

write_csv('../../data/dixon_test_out.csv', csv_cont)
```

### 数据绘图

为了对数据的样子获得一个直观的印象，让我们画一些简单的图。

#### 带标准差的样本均值条形图

首先，让我们画一个带标准差的条形图，因为这种带标准差或标准误误差条的条形图大概是所有领域中最常见的图形了。虽然它并不总是合适，但由于阅读科研文章时经常见到，它无疑是我们最熟悉的那种数据可视化形式。

```python
import numpy as np
from matplotlib import pyplot as plt

all_means = [np.nanmean(row[1:6]) for row in csv_cont[1:]]
all_stddevs = [np.nanstd(row[1:6]) for row in csv_cont[1:]]

fig = plt.figure(figsize=(8,6))

y_pos = np.arange(len(csv_cont[1:]))
y_pos = [x for x in y_pos]
plt.yticks(y_pos, [row[0] for row in csv_cont[1:]], fontsize=10)
plt.xlabel('measurement x')
t = plt.title('Bar plot with standard deviation')

plt.grid()
plt.barh(y_pos, all_means, xerr=all_stddevs, align='center', alpha=0.4, color='g')

plt.show()
```

![Dixon test dixon q plot1](https://sebastianraschka.com/images/blog/2014/dixon_test/dixon_q_plot1.webp)

正如我们所料，基本上每个样本的（相对）标准差都非常大。然而，我们无法从中得知造成这种大偏差的可能原因的任何细节：它究竟只是由 1 个离群值造成的，还是数据整体上就散布得很开。

#### 箱线图

在我看来更有用的图是 Tukey 的箱线图 [4]。事实上，箱线图是我最喜欢的快速、直观地指出高斯数据集中离群值的方法之一。不过，箱线图同样必须非常谨慎地使用，而且对于小样本量而言，它可能也提供不了太多信息。

> [4] Robert McGill, John W. Tukey and Wayne A. Larsen: “[The American
> Statistician](http://www.jstor.org/discover/10.2307/2683468?uid=3739256&uid=2&uid=4&sid=21104147331297)”
> Vol. 32, No. 1 (Feb., 1978), pp. 12-16

![Dixon test dixon q plot2](https://sebastianraschka.com/images/blog/2014/dixon_test/dixon_q_plot2.webp)

```python
csv_nonan = [[x for x in row[1:6] if not math.isnan(x)] for row in csv_cont[1:]]
fig = plt.figure(figsize=(8,6))
plt.boxplot(csv_nonan,0,'rs',0)
plt.yticks([y+1 for y in y_pos], [row[0] for row in csv_cont[1:]])
plt.xlabel('measurement x')
t = plt.title('Box plot')
plt.show()
```

![Dixon test dixon q plot3](https://sebastianraschka.com/images/blog/2014/dixon_test/dixon_q_plot3.webp)

这里的红色方块表示离群值。相当有意思的是，样本「id6」和「id1」的这两个离群值在我们之前的 Dixon Q 检验中同样被检出了。然而，「id4」和「id7」中的离群值却没有被 Dixon 离群值检验标记为离群值。

### 结论

**我真的不想在这里对哪种方法对、哪种方法错下任何结论，因为在我看来，基于如此少量观测值的数据集得出任何结论，根本就没有意义！**

那么你可能会问：如果你已经把文章读到了这里，我为什么还要浪费你的时间？因为 Dixon Q 检验在某些科学领域（例如化学）仍然相当流行，理解它的原理十分重要——这样，当你日后在研究论文或学术报告中看到所展示的研究数据时，才能做出自己的判断。
