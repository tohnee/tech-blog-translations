---
title: "目标检测入门 Part 1：梯度向量、HOG 与选择性搜索"
title_en: "Object Detection for Dummies Part 1: Gradient Vector, HOG, and SS"
source: https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/
crawled: 2026-09-08
translated: 2026-09-08
---

# 目标检测入门 Part 1：梯度向量、HOG 与选择性搜索

> 原文：[Object Detection for Dummies Part 1: Gradient Vector, HOG, and SS](https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/) · Lilian Weng（翁荔）

> 在"目标检测入门"这一系列文章中，我们将梳理图像处理与目标检测的若干基本概念、算法和流行的深度学习模型。希望对没有相关经验但想深入学习的读者有所帮助。第 1 部分介绍梯度向量的概念、HOG（方向梯度直方图）算法以及用于图像分割的选择性搜索（Selective Search）。

我从未从事过计算机视觉领域的工作，也不明白当一辆自动驾驶汽车被配置为区分停车标志与戴红帽子的行人时，这种魔法是如何奏效的。为了激励自己研究目标识别与检测算法背后的数学，我正在写"目标检测入门"系列的几篇文章。本文是第 1 部分，从图像处理中最基础的概念和几种图像分割方法开始，暂不涉及深度神经网络。用于目标检测与识别的深度学习模型将在[第 2 部分](https://lilianweng.github.io/posts/2017-12-15-object-recognition-part-2/)和[第 3 部分](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/)中讨论。

> 免责声明：刚开始写作时，我混用了"目标识别（object recognition）"和"目标检测（object detection）"这两个词。我认为它们并不相同：前者更多是判断图像中是否存在某个物体，而后者还需要指出物体的位置。不过二者高度相关，许多目标识别算法为检测奠定了基础。

本系列所有文章的链接：
[[Part 1](https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/)]
[[Part 2](https://lilianweng.github.io/posts/2017-12-15-object-recognition-part-2/)]
[[Part 3](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/)]
[[Part 4](https://lilianweng.github.io/posts/2018-12-27-object-recognition-part-4/)].

## 图像梯度向量

首先，我要确保我们能区分以下术语。它们非常相似、密切相关，但并不完全相同。

|            | **导数（Derivative）** | **方向导数（Directional Derivative）** | **梯度（Gradient）** |
| 值类型 | 标量 | 标量 | 向量 |
| 定义 | 函数 $$f(x,y,z,...)$$ 在某点 $$(x_0,y_0,z_0,...)$$ 处的变化率，即该点处切线的斜率。 | $$f(x,y,z, ...)$$ 沿单位向量 $$\vec{u}$$ 方向的瞬时变化率。 | 指向函数增长率最大的方向，包含多变量函数所有偏导数的信息。 |

在图像处理中，我们想知道颜色从一个极端向另一个极端变化的方向（即灰度图上从黑到白）。因此，我们要在像素的颜色上度量"梯度"。图像上的梯度是离散的，因为每个像素相互独立且不可再分。

[图像梯度向量](https://en.wikipedia.org/wiki/Image_gradient)为每个单独的像素定义，包含该像素在 x 轴和 y 轴两个方向上的颜色变化。这一定义与连续多变量函数的梯度一致——后者是所有变量偏导数构成的向量。设 f(x, y) 记录位置 (x, y) 处像素的颜色，像素 (x, y) 的梯度向量定义如下：

$$
\begin{align*}
\nabla f(x, y)
= \begin{bmatrix}
  g_x \\
  g_y
\end{bmatrix}
= \begin{bmatrix}
  \frac{\partial f}{\partial x} \\[6pt]
  \frac{\partial f}{\partial y}
\end{bmatrix}
= \begin{bmatrix}
  f(x+1, y) - f(x-1, y)\\
  f(x, y+1) - f(x, y-1)
\end{bmatrix}
\end{align*}
$$

$$\frac{\partial f}{\partial x}$$ 项是 x 方向的偏导数，计算为目标像素左右相邻像素的颜色差 f(x+1, y) - f(x-1, y)。类似地，$$\frac{\partial f}{\partial y}$$ 项是 y 方向的偏导数，度量为目标像素上下相邻像素的颜色差 f(x, y+1) - f(x, y-1)。

图像梯度有两个重要属性：
- **幅值（magnitude）**是向量的 L2 范数，$$g = \sqrt{ g_x^2 + g_y^2 }$$。
- **方向（direction）**是两个方向偏导数之比的反正切，$$\theta = \arctan{(g_y / g_x)}$$。

![梯度向量的像素](https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/image-gradient-vector-pixel-location.png)

*图 1：要计算位于 (x, y) 的目标像素的梯度向量，我们需要知道其四个邻居的颜色（取决于所用的核，也可能是周围八个像素）。*

图 1 示例的梯度向量为：

$$
\begin{align*}
\nabla f 
= \begin{bmatrix}
  f(x+1, y) - f(x-1, y)\\
  f(x, y+1) - f(x, y-1)
\end{bmatrix}
= \begin{bmatrix}
  55-105\\
  90-40
\end{bmatrix}
= \begin{bmatrix}
  -50\\
  50
\end{bmatrix}
\end{align*}
$$

因此，
- 幅值为 $$\sqrt{50^2 + (-50)^2} = 70.7107$$，
- 方向为 $$\arctan{(-50/50)} = -45^{\circ}$$。

对每个像素迭代地重复梯度计算过程太慢了。相反，这可以很好地转化为用特别设计的卷积核之一对整个图像矩阵（记为 $$\mathbf{A}$$）施加卷积算子。

让我们从图 1 示例的 x 方向开始，用核 $$[-1,0,1]$$ 沿 x 轴滑动；$$\ast$$ 是卷积算子：

$$
\begin{align*}
\mathbf{G}_x &= 
[-1, 0, 1] \ast [105, 255, 55] = -105 + 0 + 55 = -50
\end{align*}
$$

类似地，在 y 方向上采用核 $$[+1, 0, -1]^\top$$：

$$
\begin{align*}
\mathbf{G}_y &= 
[+1, 0, -1]^\top \ast
\begin{bmatrix}
  90\\
  255\\
  40
\end{bmatrix} 
= 90 + 0 - 40 = 50
\end{align*}
$$

在 python 中试试：

```python
import numpy as np
import scipy.signal as sig
data = np.array([[0, 105, 0], [40, 255, 90], [0, 55, 0]])
G_x = sig.convolve2d(data, np.array([[-1, 0, 1]]), mode='valid') 
G_y = sig.convolve2d(data, np.array([[-1], [0], [1]]), mode='valid')
```

这两个函数分别返回 `array([[0], [-50], [0]])` 和 `array([[0, 50, 0]])`。（注意在 numpy 数组表示中，40 排在 90 前面，所以核中 -1 也相应地列在 1 之前。）

### 常见图像处理核

[Prewitt 算子](https://en.wikipedia.org/wiki/Prewitt_operator)：不只依赖四个直接相邻的邻居，Prewitt 算子利用周围八个像素以获得更平滑的结果。

$$
\mathbf{G}_x = \begin{bmatrix}
-1 & 0 & +1 \\
-1 & 0 & +1 \\
-1 & 0 & +1
\end{bmatrix} \ast \mathbf{A} \text{ and }
\mathbf{G}_y = \begin{bmatrix}
+1 & +1 & +1 \\
0 & 0 & 0 \\
-1 & -1 & -1
\end{bmatrix} \ast \mathbf{A}
$$

[Sobel 算子](https://en.wikipedia.org/wiki/Sobel_operator)：为了更强调直接相邻像素的影响，它们被赋予更高的权重。

$$
\mathbf{G}_x = \begin{bmatrix}
-1 & 0 & +1 \\
-2 & 0 & +2 \\
-1 & 0 & +1
\end{bmatrix} \ast \mathbf{A} \text{ and }
\mathbf{G}_y = \begin{bmatrix}
+1 & +2 & +1 \\
0 & 0 & 0 \\
-1 & -2 & -1
\end{bmatrix} \ast \mathbf{A}
$$

针对边缘检测、模糊、锐化等不同目标，人们设计了不同的核。更多示例和参考资料见[这个 wiki 页面](https://en.wikipedia.org/wiki/Kernel_(image_processing))。

### 示例：2004 年的马努

让我们用 Manu Ginobili 2004 年的照片[[下载图片](https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/manu-2004.png)]做一个简单的实验——那时他还有一头浓密的头发。为简单起见，照片先被转换为灰度图。对于彩色图像，只需在每个颜色通道上分别重复同样的过程。

![Manu 2004](https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/manu-2004.png)

*图 2：2004 年还有头发的 Manu Ginobili。（图片来源：[Manu Ginobili's bald spot through the years](http://ftw.usatoday.com/2013/05/manu-ginobilis-bald-spot-through-the-years)）*

```python
import numpy as np
import scipy
import scipy.signal as sig
# With mode="L", we force the image to be parsed in the grayscale, so it is
# actually unnecessary to convert the photo color beforehand.
img = scipy.misc.imread("manu-2004.jpg", mode="L")

# Define the Sobel operator kernels.
kernel_x = np.array([[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]])
kernel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

G_x = sig.convolve2d(img, kernel_x, mode='same') 
G_y = sig.convolve2d(img, kernel_y, mode='same') 

# Plot them!
fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

# Actually plt.imshow() can handle the value scale well even if I don't do 
# the transformation (G_x + 255) / 2.
ax1.imshow((G_x + 255) / 2, cmap='gray'); ax1.set_xlabel("Gx")
ax2.imshow((G_y + 255) / 2, cmap='gray'); ax2.set_xlabel("Gy")
plt.show()
```

![Sobel 算子](https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/manu-2004-sobel-operator.png)

*图 3：在示例图像上应用 Sobel 算子核。*

你可能注意到大部分区域是灰色的。因为两个像素之差介于 -255 到 255 之间，而为了显示我们需要把它们转回 [0, 255]。简单的线性变换 ($$\mathbf{G}$$ + 255)/2 会把所有的零（即纯色背景在梯度上没有变化）解释为 125（显示为灰色）。

## 方向梯度直方图（HOG）

方向梯度直方图（Histogram of Orientated Gradients，HOG）是一种从像素颜色中高效提取特征以构建目标识别分类器的方法。有了图像梯度向量的知识，理解 HOG 的工作原理并不难。开始吧！

### HOG 的工作原理

1) 预处理图像，包括缩放和颜色归一化。

2) 计算每个像素的梯度向量，以及它的幅值和方向。

3) 把图像划分成许多 8x8 像素的单元（cell）。在每个单元中，这 64 个像素的幅值被分箱并累加到 9 个无符号方向的桶中（无符号，所以是 0-180 度而非 0-360 度；这是基于经验实验的实用选择）。
<br/><br/>
为了更好的鲁棒性，如果某个像素梯度向量的方向落在两个桶之间，其幅值不会全部进入较近的那个桶，而是按比例在两者之间分摊。例如，若一个像素的梯度向量幅值为 8、角度为 15 度，它位于 0 度和 20 度两个桶之间，我们会把 2 分给 0 度桶、6 分给 20 度桶。
<br/><br/>
这个有趣的配置使得直方图在图像受到轻微形变时依然保持相当稳定。

![直方图构建](https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/HOG-histogram-creation.png)

*图 4：当一个梯度向量的角度位于两个角度箱之间时，如何拆分其幅值。（图片来源：https://www.learnopencv.com/histogram-of-oriented-gradients/）*

4) 然后我们把一个 2x2 单元（即 16x16 像素）的块（block）在图像上滑动。在每个块区域内，4 个单元的 4 个直方图被拼接成一个 36 维的一维向量，然后归一化为单位权重。
最终的 HOG 特征向量是所有块向量的拼接。它可以输入 SVM 等分类器来学习目标识别任务。

### 示例：2004 年的马努

让我们复用上一节的示例图像。记得我们已经为整幅图像计算了 $$\mathbf{G}_x$$ 和 $$\mathbf{G}_y$$。

```python
N_BUCKETS = 9
CELL_SIZE = 8  # Each cell is 8x8 pixels
BLOCK_SIZE = 2  # Each block is 2x2 cells

def assign_bucket_vals(m, d, bucket_vals):
    left_bin = int(d / 20.)
    # Handle the case when the direction is between [160, 180)
    right_bin = (int(d / 20.) + 1) % N_BUCKETS
    assert 0 <= left_bin < right_bin < N_BUCKETS

    left_val= m * (right_bin * 20 - d) / 20
    right_val = m * (d - left_bin * 20) / 20
    bucket_vals[left_bin] += left_val
    bucket_vals[right_bin] += right_val

def get_magnitude_hist_cell(loc_x, loc_y):
    # (loc_x, loc_y) defines the top left corner of the target cell.
    cell_x = G_x[loc_x:loc_x + CELL_SIZE, loc_y:loc_y + CELL_SIZE]
    cell_y = G_y[loc_x:loc_x + CELL_SIZE, loc_y:loc_y + CELL_SIZE]
    magnitudes = np.sqrt(cell_x * cell_x + cell_y * cell_y)
    directions = np.abs(np.arctan(cell_y / cell_x) * 180 / np.pi)

    buckets = np.linspace(0, 180, N_BUCKETS + 1)
    bucket_vals = np.zeros(N_BUCKETS)
    map(
        lambda (m, d): assign_bucket_vals(m, d, bucket_vals), 
        zip(magnitudes.flatten(), directions.flatten())
    )
    return bucket_vals

def get_magnitude_hist_block(loc_x, loc_y):
    # (loc_x, loc_y) defines the top left corner of the target block.
    return reduce(
        lambda arr1, arr2: np.concatenate((arr1, arr2)),
        [get_magnitude_hist_cell(x, y) for x, y in zip(
            [loc_x, loc_x + CELL_SIZE, loc_x, loc_x + CELL_SIZE],
            [loc_y, loc_y, loc_y + CELL_SIZE, loc_y + CELL_SIZE],
        )]
    )
```

下面的代码简单地调用这些函数构建直方图并绘制。

```python
# Random location [200, 200] as an example.
loc_x = loc_y = 200

ydata = get_magnitude_hist_block(loc_x, loc_y)
ydata = ydata / np.linalg.norm(ydata)

xdata = range(len(ydata))
bucket_names = np.tile(np.arange(N_BUCKETS), BLOCK_SIZE * BLOCK_SIZE)

assert len(ydata) == N_BUCKETS * (BLOCK_SIZE * BLOCK_SIZE)
assert len(bucket_names) == len(ydata)

plt.figure(figsize=(10, 3))
plt.bar(xdata, ydata, align='center', alpha=0.8, width=0.9)
plt.xticks(xdata, bucket_names * 20, rotation=90)
plt.xlabel('Direction buckets')
plt.ylabel('Magnitude')
plt.grid(ls='--', color='k', alpha=0.1)
plt.title("HOG of block at [%d, %d]" % (loc_x, loc_y))
plt.tight_layout()
```

在上面的代码中，我以左上角位于 [200, 200] 的块为例，这是该块最终归一化后的直方图。你可以修改代码，用滑动窗口来改变要识别的块位置。

![块直方图](https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/block_histogram.png)

*图 5：一个块的 HOG 直方图演示。*

这些代码主要用于演示计算过程。有许多现成实现了 HOG 算法的库，如 [OpenCV](https://github.com/opencv/opencv)、[SimpleCV](http://simplecv.org/) 和 [scikit-image](http://scikit-image.org/)。

## 图像分割（Felzenszwalb 算法）

当一张图像中存在多个物体时（几乎所有的真实照片都是如此），我们需要识别出一个可能包含目标物体的区域，这样分类可以更高效地执行。

Felzenszwalb 和 Huttenlocher（[2004](http://cvcl.mit.edu/SUNSeminar/Felzenszwalb_IJCV04.pdf)）提出了一种基于图的方法，把图像分割为相似的区域。它也是我们稍后要讨论的选择性搜索（一种流行的候选区域算法）的初始化方法。

设我们用无向图 $$G=(V, E)$$ 表示一张输入图像。一个顶点 $$v_i \in V$$ 表示一个像素。一条边 $$e = (v_i, v_j) \in E$$ 连接两个顶点 $$v_i$$ 和 $$v_j$$，其关联权重 $$w(v_i, v_j)$$ 度量 $$v_i$$ 与 $$v_j$$ 之间的不相似度。不相似度可以在颜色、位置、强度等维度上量化。权重越高，两个像素越不相似。一个分割方案 $$S$$ 是把 $$V$$ 划分成多个连通分量 $$\{C\}$$。直观上，相似的像素应属于同一个分量，而不相似的像素被分到不同的分量。

### 图的构建

有两种从图像构建图的方法。
- **网格图（Grid Graph）**：每个像素只与周围邻居相连（共 8 个其他单元格）。边的权重是像素强度值的绝对差。
- **最近邻图（Nearest Neighbor Graph）**：每个像素是特征空间 (x, y, r, g, b) 中的一个点，其中 (x, y) 是像素位置，(r, g, b) 是 RGB 颜色值。权重是两个像素特征向量之间的欧氏距离。

### 关键概念

在给出好的图划分（即图像分割）准则之前，先定义几个关键概念：
- **内部差异（Internal difference）**：$$Int(C) = \max_{e\in MST(C, E)} w(e)$$，其中 $$MST$$ 是分量的最小生成树。即使移除所有权重 < $$Int(C)$$ 的边，分量 $$C$$ 仍能保持连通。
- **两个分量之间的差异**：$$Dif(C_1, C_2) = \min_{v_i \in C_1, v_j \in C_2, (v_i, v_j) \in E} w(v_i, v_j)$$。若两者之间没有边，则 $$Dif(C_1, C_2) = \infty$$。
- **最小内部差异**：$$MInt(C_1, C_2) = min(Int(C_1) + \tau(C_1), Int(C_2) + \tau(C_2))$$，其中 $$\tau(C) = k / \vert C \vert$$ 有助于确保分量之间的差异有一个有意义的阈值。$$k$$ 越大，越可能产生更大的分量。

分割质量由针对给定两个区域 $$C_1$$ 和 $$C_2$$ 定义的成对区域比较谓词来评估：

$$
D(C_1, C_2) = 
\begin{cases}
  \text{True} & \text{ if } Dif(C_1, C_2) > MInt(C_1, C_2) \\
  \text{False} & \text{ otherwise}
\end{cases}
$$

只有当谓词为 True 时，我们才把它们视为两个独立的分量；否则分割过细，它们或许应该被合并。

### 图像分割的工作原理

该算法遵循自底向上的流程。给定 $$G=(V, E)$$ 且 $$|V|=n, |E|=m$$：
1. 边按权重升序排序，记为 $$e_1, e_2, \dots, e_m$$。
2. 初始时，每个像素自成一个分量，因此从 $$n$$ 个分量开始。
3. 对 $$k=1, \dots, m$$ 重复：
    * 第 $$k$$ 步的分割快照记为 $$S^k$$。
    * 取排序中的第 k 条边 $$e_k = (v_i, v_j)$$。
    * 若 $$v_i$$ 和 $$v_j$$ 属于同一分量，什么都不做，因此 $$S^k = S^{k-1}$$。
    * 若 $$v_i$$ 和 $$v_j$$ 属于分割 $$S^{k-1}$$ 中两个不同的分量 $$C_i^{k-1}$$ 和 $$C_j^{k-1}$$，当 $$w(v_i, v_j) \leq MInt(C_i^{k-1}, C_j^{k-1})$$ 时我们把它们合并为一个；否则什么都不做。

如果你对分割性质的证明以及它为何总是存在感兴趣，请参阅[论文](http://fcv2011.ulsan.ac.kr/files/announcement/413/IJCV(2004)%20Efficient%20Graph-Based%20Image%20Segmentation.pdf)。

![室内场景图像分割](https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/image-segmentation-indoor.png)

*图 6：用 Felzenszwalb 基于图的分割算法（k=300）中的网格图构建检测到的一个室内场景分割。*

### 示例：2013 年的马努

这次我用 2013 年年长的 Manu Ginobili 的照片[[图片](https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/manu-2013.png)]作为示例图像——他的秃斑那时已经长得很旺盛了。同样为简单起见，我们使用灰度化的图片。

![Manu 2013](https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/manu-2013.png)

*图 7：2013 年有秃斑的 Manu Ginobili。（图片来源：[Manu Ginobili's bald spot through the years](http://ftw.usatoday.com/2013/05/manu-ginobilis-bald-spot-through-the-years)）*

与其从零编写代码，不如直接对图像应用 [skimage.segmentation.felzenszwalb](http://scikit-image.org/docs/dev/api/skimage.segmentation.html#skimage.segmentation.felzenszwalb)。

```python
import skimage.segmentation
from matplotlib import pyplot as plt

img2 = scipy.misc.imread("manu-2013.jpg", mode="L")
segment_mask1 = skimage.segmentation.felzenszwalb(img2, scale=100)
segment_mask2 = skimage.segmentation.felzenszwalb(img2, scale=1000)

fig = plt.figure(figsize=(12, 5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.imshow(segment_mask1); ax1.set_xlabel("k=100")
ax2.imshow(segment_mask2); ax2.set_xlabel("k=1000")
fig.suptitle("Felsenszwalb's efficient graph based image segmentation")
plt.tight_layout()
plt.show()
```

代码运行了 Felzenszwalb 算法的两个版本，如图 8 所示。左边 k=100 生成了更细粒度的分割，出现了识别出马努秃斑的小区域。右边 k=1000 输出了更粗粒度的分割，区域往往更大。

![Manu 2013 图像分割](https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/manu-2013-segmentation.png)

*图 8：在马努 2013 年的照片上应用 Felzenszwalb 的高效基于图的图像分割。*

## 选择性搜索

选择性搜索（Selective Search）是提供可能包含物体的候选区域的常用算法。它构建在图像分割的输出之上，利用基于区域的特征（注意：不只是单个像素的属性）做自底向上的层次分组。

### 选择性搜索的工作原理

1. 在初始化阶段，应用 Felzenszwalb 和 Huttenlocher 的基于图的图像分割算法，创建起始区域。
2. 用贪心算法迭代地把区域分组到一起：
    * 首先计算所有相邻区域之间的相似度。
    * 把最相似的两个区域分为一组，然后计算所得区域与其邻居之间的新的相似度。
3. 重复分组最相似区域的过程（第 2 步），直到整张图像成为一个单一区域。

![选择性搜索算法](https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/selective-search-algorithm.png)

*图 9：选择性搜索的详细算法。*

### 配置变体

给定两个区域 $$(r_i, r_j)$$，选择性搜索提出了四种互补的相似度度量：
- **颜色**相似度
- **纹理**：使用对材质识别效果良好的算法，如 [SIFT](http://www.cs.ubc.ca/~lowe/papers/iccv99.pdf)。
- **大小**：鼓励小区域尽早合并。
- **形状**：理想情况下，一个区域可以填补另一个区域的空缺。

通过 (i) 调整 Felzenszwalb 和 Huttenlocher 算法中的阈值 $$k$$，(ii) 更换颜色空间，以及 (iii) 挑选相似度度量的不同组合，我们可以产出一组多样化的选择性搜索策略。产出候选区域质量最好的版本配置了 (i) 多种初始分割提议的混合，(ii) 多种颜色空间的融合，以及 (iii) 所有相似度度量的组合。不出意外，我们需要在质量（模型复杂度）和速度之间取得平衡。

---
引用格式：
```
@article{weng2017detection1,
  title   = "Object Detection for Dummies Part 1: Gradient Vector, HOG, and SS",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2017",
  url     = "http://lilianweng.github.io/lil-log/2017/10/29/object-recognition-for-dummies-part-1.html"
}
```

## 参考文献

[1] Dalal, Navneet, and Bill Triggs. ["Histograms of oriented gradients for human detection."](https://hal.inria.fr/file/index/docid/548512/filename/hog_cvpr2005.pdf) Computer Vision and Pattern Recognition (CVPR), 2005.

[2] Pedro F. Felzenszwalb, and Daniel P. Huttenlocher. ["Efficient graph-based image segmentation."](http://cvcl.mit.edu/SUNSeminar/Felzenszwalb_IJCV04.pdf) Intl. journal of computer vision 59.2 (2004): 167-181.

[3] [Histogram of Oriented Gradients by Satya Mallick](https://www.learnopencv.com/histogram-of-oriented-gradients/)

[4] [Gradient Vectors by Chris McCormick](http://mccormickml.com/2013/05/07/gradient-vectors/)

[5] [HOG Person Detector Tutorial by Chris McCormick](http://mccormickml.com/2013/05/09/hog-person-detector-tutorial/)
