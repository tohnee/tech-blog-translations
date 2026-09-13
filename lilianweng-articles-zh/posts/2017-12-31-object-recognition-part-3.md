---
title: "目标检测入门 Part 3：R-CNN 家族"
title_en: "Object Detection for Dummies Part 3: R-CNN Family"
source: https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/
crawled: 2026-09-08
translated: 2026-09-08
---

# 目标检测入门 Part 3：R-CNN 家族

> 原文：[Object Detection for Dummies Part 3: R-CNN Family](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/) · Lilian Weng（翁荔）

> 在第 3 部分中，我们将考察四个目标检测模型：R-CNN、Fast R-CNN、Faster R-CNN 和 Mask R-CNN。这些模型高度相关，新版本相比旧版本有巨大的速度提升。

<span style="color: #286ee0;">[更新于 2018-12-20：移除了此处的 YOLO 内容。第 4 部分将涵盖多种快速目标检测算法，包括 YOLO。]</span>
<br/>
<span style="color: #286ee0;">[更新于 2018-12-27：为 R-CNN 增加了[边界框回归](#bounding-box-regression)和[技巧](#common-tricks)小节。]</span>

在"目标检测入门"系列中，[第 1 部分](https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/)从图像处理的基本概念（如梯度向量和 HOG）开始；[第 2 部分](https://lilianweng.github.io/posts/2017-12-15-object-recognition-part-2/)介绍了用于分类的经典卷积神经网络架构设计以及目标识别的先驱模型 Overfeat 和 DPM。在本系列的第三篇文章中，我们将回顾 R-CNN（"Region-based CNN"，基于区域的 CNN）家族的一系列模型。

本系列所有文章的链接：
[[Part 1](https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/)]
[[Part 2](https://lilianweng.github.io/posts/2017-12-15-object-recognition-part-2/)]
[[Part 3](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/)]
[[Part 4](https://lilianweng.github.io/posts/2018-12-27-object-recognition-part-4/)].

以下是本文涵盖的论文清单 ;)

| **模型**    | **目标**           | **资源**  |
| R-CNN        | 目标识别 | [[论文](https://arxiv.org/abs/1311.2524)][[代码](https://github.com/rbgirshick/rcnn)]   |
| Fast R-CNN   | 目标识别 | [[论文](https://arxiv.org/abs/1504.08083)][[代码](https://github.com/rbgirshick/fast-rcnn)]   |
| Faster R-CNN | 目标识别 | [[论文](https://arxiv.org/abs/1506.01497)][[代码](https://github.com/rbgirshick/py-faster-rcnn)]  |
| Mask R-CNN   | 图像分割 | [[论文](https://arxiv.org/abs/1703.06870)][[代码](https://github.com/CharlesShang/FastMaskRCNN)] |

## R-CNN

R-CNN（[Girshick et al., 2014](https://arxiv.org/abs/1311.2524)）是 "Region-based Convolutional Neural Networks"（基于区域的卷积神经网络）的缩写。其主要思想由两步组成。首先，使用[选择性搜索](https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/#selective-search)识别出数量可控的边界框物体候选区域（"感兴趣区域" region of interest，RoI）。然后从每个区域独立提取 CNN 特征用于分类。

![R-CNN 架构](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/RCNN.png)

*图 1：R-CNN 的架构。（图片来源：[Girshick et al., 2014](https://arxiv.org/abs/1311.2524)）*

### 模型工作流程

R-CNN 的工作方式可以总结如下：

1. 在图像分类任务上**预训练**一个 CNN 网络；例如在 [ImageNet](http://image-net.org/index) 数据集上训练的 VGG 或 ResNet。分类任务涉及 N 个类别。
<br />
> 注意：你可以在 Caffe 模型 [Zoo](https://github.com/caffe2/caffe2/wiki/Model-Zoo) 中找到预训练的 [AlexNet](https://github.com/BVLC/caffe/tree/master/models/bvlc_alexnet)。我认为 Tensorflow 里[找不到它](https://github.com/tensorflow/models/issues/1394)，但 Tensorflow-slim 模型[库](https://github.com/tensorflow/models/tree/master/research/slim)提供了预训练的 ResNet、VGG 等。
2. 通过选择性搜索提出与类别无关的候选区域（每张图像约 2k 个候选）。这些区域可能包含目标物体，且大小不一。
3. 将候选区域**扭曲（warp）**为 CNN 要求的固定尺寸。
4. 在扭曲后的候选区域上以 K + 1 个类别继续微调 CNN；额外的那一类指背景（没有感兴趣的物体）。在微调阶段，应使用小得多的学习率，并且 mini-batch 要对正样本过采样，因为大多数候选区域只是背景。
5. 给定每个图像区域，一次 CNN 前向传播生成一个特征向量。该特征向量随后由**为每个类别独立训练**的**二分类 SVM** 消费。
<br />
正样本是 IoU（交并比）重叠阈值 >= 0.3 的候选区域，负样本是无关的其他区域。
6. 为减少定位误差，训练一个回归模型，利用 CNN 特征修正预测检测窗口的边界框校正偏移。

### 边界框回归

给定预测边界框坐标 $$\mathbf{p} = (p_x, p_y, p_w, p_h)$$（中心坐标、宽、高）及其对应的真实标注框坐标 $$\mathbf{g} = (g_x, g_y, g_w, g_h)$$，回归器被配置为学习两个中心之间的尺度不变变换以及宽高之间的对数尺度变换。所有变换函数都以 $$\mathbf{p}$$ 为输入。

$$
\begin{aligned}
\hat{g}_x &= p_w d_x(\mathbf{p}) + p_x \\
\hat{g}_y &= p_h d_y(\mathbf{p}) + p_y \\
\hat{g}_w &= p_w \exp({d_w(\mathbf{p})}) \\
\hat{g}_h &= p_h \exp({d_h(\mathbf{p})})
\end{aligned}
$$

![bbox 回归](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/RCNN-bbox-regression.png)

*图 2：预测边界框与真实标注框之间的变换示意图。*

应用这种变换的一个明显好处是：所有边界框校正函数 $$d_i(\mathbf{p})$$（$$i \in \{ x, y, w, h \}$$）可以取 [-∞, +∞] 之间的任何值。它们要学习的目标是：

$$
\begin{aligned}
t_x &= (g_x - p_x) / p_w \\
t_y &= (g_y - p_y) / p_h \\
t_w &= \log(g_w/p_w) \\
t_h &= \log(g_h/p_h)
\end{aligned}
$$

标准的回归模型可以通过最小化带正则化的 SSE 损失来求解：

$$
\mathcal{L}_\text{reg} = \sum_{i \in \{x, y, w, h\}} (t_i - d_i(\mathbf{p}))^2 + \lambda \|\mathbf{w}\|^2
$$

正则化项在这里至关重要，R-CNN 论文通过交叉验证挑选了最佳的 λ。同样值得注意的是，并非所有预测边界框都有对应的真实标注框。例如，如果没有重叠，做边界框回归就没有意义。这里，只有那些附近存在 IoU 至少为 0.6 的真实标注框的预测框，才被保留用于训练边界框回归模型。

### 常用技巧

以下技巧在 RCNN 及其他检测模型中很常用。

**非极大值抑制（Non-Maximum Suppression）**

模型很可能为同一物体找到多个边界框。非极大值抑制有助于避免对同一实例的重复检测。当我们得到同一物体类别的一组匹配边界框后：
按置信度分数对所有边界框排序。
丢弃低置信度分数的框。
*当*还有剩余边界框时，重复以下操作：
贪心地选择分数最高的那个。
跳过与之前已选框有高 IoU（即 > 0.5）的剩余框。

![非极大值抑制](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/non-max-suppression.png)

*图 3：多个边界框检测到图中的汽车。经过非极大值抑制后，只保留最好的一个，其余因与被选中者重叠过大而被忽略。（图片来源：[DPM 论文](http://lear.inrialpes.fr/~oneata/reading_group/dpm.pdf)）*

**难负例挖掘（Hard Negative Mining）**

我们把不含物体的边界框视为负样本。并非所有负样本都同样难以识别。例如，若一个框内是纯空背景，它很可能是"*简单负例（easy negative）*"；但如果框内包含奇怪的噪声纹理或物体的一部分，它可能很难被识别，这些是"*困难负例（hard negative）*"。

困难负例很容易被误分类。我们可以在训练循环中显式地找出这些假正例样本，把它们纳入训练数据，从而改进分类器。

### 速度瓶颈

通读 R-CNN 的学习步骤，你很容易发现训练一个 R-CNN 模型昂贵而缓慢，因为以下步骤涉及大量工作：
- 运行选择性搜索为每张图像提出 2000 个候选区域；
- 为每个图像区域生成 CNN 特征向量（N 张图像 × 2000）。
- 整个过程涉及三个独立模型，几乎没有共享计算：用于图像分类和特征提取的卷积神经网络；用于识别目标物体的顶层 SVM 分类器；以及用于收紧区域边界框的回归模型。

## Fast R-CNN

为了让 R-CNN 更快，Girshick（[2015](https://arxiv.org/pdf/1504.08083.pdf)）改进了训练流程：把三个独立模型统一为一个联合训练的框架并增加共享计算，称为 **Fast R-CNN**。该模型不再为每个候选区域独立提取 CNN 特征向量，而是把它们聚合为对整张图像的一次 CNN 前向传播，候选区域共享该特征矩阵。然后同一特征矩阵被分支用于学习物体分类器和边界框回归器。总而言之，计算共享加速了 R-CNN。

![Fast R-CNN](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/fast-RCNN.png)

*图 4：Fast R-CNN 的架构。（图片来源：[Girshick, 2015](https://arxiv.org/pdf/1504.08083.pdf)）*

### RoI 池化

它是一种最大池化，把图像投影区域中任意尺寸 h × w 的特征转换为固定的小窗口 H × W。输入区域被划分为 H × W 个网格，每个子窗口的尺寸约为 h/H × w/W。然后在每个网格内做最大池化。

![RoI 池化](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/roi-pooling.png)

*图 5：RoI 池化（图片来源：[Stanford CS231n slides](http://cs231n.stanford.edu/slides/2016/winter1516_lecture8.pdf)。）*

### 模型工作流程

Fast R-CNN 的工作方式总结如下；许多步骤与 R-CNN 相同：
1. 首先，在图像分类任务上预训练一个卷积神经网络。
2. 通过选择性搜索提出区域（每张图像约 2k 个候选）。
3. 改造预训练的 CNN：
	- 把预训练 CNN 的最后一个最大池化层替换为 [RoI 池化](#roi-pooling)层。RoI 池化层输出候选区域的定长特征向量。共享 CNN 计算非常合理，因为同一图像的许多候选区域高度重叠。
	- 把最后一个全连接层和最后一个 softmax 层（K 类）替换为 K + 1 类的全连接层和 softmax。
4. 最后模型分支为两个输出层：
	- K + 1 类的 softmax 估计器（与 R-CNN 相同，+1 是"背景"类），为每个 RoI 输出一个离散概率分布。
	- 一个边界框回归模型，为 K 个类别中的每一个预测相对于原始 RoI 的偏移。

### 损失函数

该模型的优化目标是一个结合两个任务（分类 + 定位）的损失：

| **符号** | **解释** |
| $$u$$ | 真实类别标签，$$ u \in 0, 1, \dots, K$$；按惯例，兜底的背景类为 $$u = 0$$。 |
| $$p$$ | K + 1 类上的（每个 RoI 的）离散概率分布：$$p = (p_0, \dots, p_K)$$，由对全连接层 K + 1 个输出施加 softmax 计算。 |
| $$v$$ | 真实边界框 $$ v = (v_x, v_y, v_w, v_h) $$。 |
| $$t^u$$ | 预测的边界框校正，$$t^u = (t^u_x, t^u_y, t^u_w, t^u_h)$$。见[上文](#bounding-box-regression)。 |

损失函数将分类与边界框预测的代价相加：$$\mathcal{L} = \mathcal{L}_\text{cls} + \mathcal{L}_\text{box}$$。对"背景"RoI，$$\mathcal{L}_\text{box}$$ 被指示函数 $$\mathbb{1} [u \geq 1]$$ 忽略，定义为：

$$
\mathbb{1} [u >= 1] = \begin{cases}
    1  & \text{if } u \geq 1\\
    0  & \text{otherwise}
\end{cases}
$$

总体损失函数为：

$$
\begin{align*}
\mathcal{L}(p, u, t^u, v) &= \mathcal{L}_\text{cls} (p, u) + \mathbb{1} [u \geq 1] \mathcal{L}_\text{box}(t^u, v) \\
\mathcal{L}_\text{cls}(p, u) &= -\log p_u \\
\mathcal{L}_\text{box}(t^u, v) &= \sum_{i \in \{x, y, w, h\}} L_1^\text{smooth} (t^u_i - v_i)
\end{align*}
$$

边界框损失 $$\mathcal{L}_{box}$$ 应使用**鲁棒**损失函数度量 $$t^u_i$$ 与 $$v_i$$ 之间的差异。这里采用 [smooth L1 损失](https://github.com/rbgirshick/py-faster-rcnn/files/764206/SmoothL1Loss.1.pdf)，据称对异常值更不敏感。

$$
L_1^\text{smooth}(x) = \begin{cases}
    0.5 x^2             & \text{if } \vert x \vert < 1\\
    \vert x \vert - 0.5 & \text{otherwise}
\end{cases}
$$

![Smooth L1 损失](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/l1-smooth.png)

*图 6：smooth L1 损失的图像，$$y = L_1^\text{smooth}(x)$$。（图片来源：[链接](https://github.com/rbgirshick/py-faster-rcnn/files/764206/SmoothL1Loss.1.pdf)）*

### 速度瓶颈

Fast R-CNN 在训练和测试时间上都快得多。然而改进并不戏剧性，因为候选区域由另一个模型单独生成，那非常昂贵。

## Faster R-CNN

一个直观的提速方案是把候选区域生成算法整合进 CNN 模型。**Faster R-CNN**（[Ren et al., 2016](https://arxiv.org/pdf/1506.01497.pdf)）正是这样做的：构建一个由 RPN（区域提议网络）与 fast R-CNN 组成的单一统一模型，二者共享卷积特征层。

![Faster R-CNN](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/faster-RCNN.png)

*图 7：Faster R-CNN 模型示意图。（图片来源：[Ren et al., 2016](https://arxiv.org/pdf/1506.01497.pdf)）*

### 模型工作流程

1. 在图像分类任务上预训练一个 CNN 网络。
2. 端到端微调用于候选区域任务的 RPN（区域提议网络），它由预训练的图像分类器初始化。正样本的 IoU（交并比）> 0.7，负样本的 IoU < 0.3。
	- 在整幅图像的卷积特征图上滑动一个小的 n × n 空间窗口。
	- 在每个滑动窗口的中心，我们同时预测多个不同尺度和长宽比的区域。一个锚框（anchor）是（滑动窗口中心, 尺度, 长宽比）的组合。例如，3 种尺度 + 3 种长宽比 => 每个滑动位置 k=9 个锚框。
3. 使用当前 RPN 生成的提议训练一个 Fast R-CNN 目标检测模型。
4. 然后用 Fast R-CNN 网络初始化 RPN 训练。保持共享的卷积层，只微调 RPN 特有的层。至此，RPN 与检测网络已共享卷积层！
5. 最后微调 Fast R-CNN 的独有层。
6. 如有需要，可以重复第 4-5 步，交替训练 RPN 与 Fast R-CNN。

### 损失函数

Faster R-CNN 针对多任务损失函数优化，与 fast R-CNN 类似。

| **符号**  | **解释** |
| $$p_i$$     | 锚框 i 是物体的预测概率。 |
| $$p^*_i$$   | 锚框 i 是否为物体的真实标签（二值）。 |
| $$t_i$$     | 预测的四个参数化坐标。 |
| $$t^*_i$$   | 真实标注坐标。 |
| $$N_\text{cls}$$ | 归一化项，论文中设为 mini-batch 大小（~256）。 |
| $$N_\text{box}$$ | 归一化项，论文中设为锚框位置数（~2400）。 |
| $$\lambda$$ | 平衡参数，论文中设为 ~10（使 $$\mathcal{L}_\text{cls}$$ 与 $$\mathcal{L}_\text{box}$$ 两项的权重大致相等）。 |

多任务损失函数结合了分类与边界框回归的损失：

$$
\begin{align*}
\mathcal{L} &= \mathcal{L}_\text{cls} + \mathcal{L}_\text{box} \\
\mathcal{L}(\{p_i\}, \{t_i\}) &= \frac{1}{N_\text{cls}} \sum_i \mathcal{L}_\text{cls} (p_i, p^*_i) + \frac{\lambda}{N_\text{box}} \sum_i p^*_i \cdot L_1^\text{smooth}(t_i - t^*_i) \\
\end{align*}
$$

其中 $$\mathcal{L}_\text{cls}$$ 是两类上的对数损失，因为我们可以轻易地把多分类转化为"预测样本是否为目标物体"的二分类。$$L_1^\text{smooth}$$ 是 smooth L1 损失。

$$
\mathcal{L}_\text{cls} (p_i, p^*_i) = - p^*_i \log p_i - (1 - p^*_i) \log (1 - p_i)
$$

## Mask R-CNN

Mask R-CNN（[He et al., 2017](https://arxiv.org/pdf/1703.06870.pdf)）将 Faster R-CNN 扩展到像素级[图像分割](https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/#image-segmentation-felzenszwalbs-algorithm)。关键点在于将分类任务与像素级掩码预测任务解耦。在 [Faster R-CNN](#faster-r-cnn) 框架的基础上，它增加了第三个分支，与既有的分类和定位分支并行地预测物体掩码。掩码分支是一个作用于每个 RoI 的小型全连接网络，以像素到像素的方式预测分割掩码。

![Mask R-CNN](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/mask-rcnn.png)

*图 8：Mask R-CNN 是带图像分割的 Faster R-CNN 模型。（图片来源：[He et al., 2017](https://arxiv.org/pdf/1703.06870.pdf)）*

因为像素级分割比边界框需要精细得多的对齐，mask R-CNN 改进了 RoI 池化层（命名为 "RoIAlign 层"），使 RoI 能更好、更精确地映射到原图的区域。

![Mask R-CNN 示例](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/mask-rcnn-examples.png)

*图 9：Mask R-CNN 在 COCO 测试集上的预测。（图片来源：[He et al., 2017](https://arxiv.org/pdf/1703.06870.pdf)）*

### RoIAlign

RoIAlign 层旨在修复 RoI 池化中由量化导致的位置失配。RoIAlign 移除了粗糙的量化，例如使用 x/16 而非 [x/16]，使提取的特征能与输入像素正确对齐。计算输入中的浮点位置值时使用[双线性插值](https://en.wikipedia.org/wiki/Bilinear_interpolation)。

![RoI Align](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/roi-align.png)

*图 10：感兴趣区域从原图**精确**映射到特征图，不取整。（图片来源：[链接](https://blog.athelas.com/a-brief-history-of-cnns-in-image-segmentation-from-r-cnn-to-mask-r-cnn-34ea83205de4)）*

### 损失函数

Mask R-CNN 的多任务损失函数结合了分类、定位与分割掩码的损失：$$ \mathcal{L} = \mathcal{L}_\text{cls} + \mathcal{L}_\text{box} + \mathcal{L}_\text{mask}$$，其中 $$\mathcal{L}_\text{cls}$$ 和 $$\mathcal{L}_\text{box}$$ 与 Faster R-CNN 中相同。

掩码分支为每个 RoI 和每个类别生成一个 m × m 维的掩码；共 K 个类别。因此总输出大小为 $$K \cdot m^2$$。由于模型为每个类别学习一个掩码，类别之间在生成掩码时不存在竞争。

$$\mathcal{L}_\text{mask}$$ 定义为平均二元交叉熵损失，仅当区域与真实类别 k 关联时才纳入第 k 个掩码。

$$
\mathcal{L}_\text{mask} = - \frac{1}{m^2} \sum_{1 \leq i, j \leq m} \big[ y_{ij} \log \hat{y}^k_{ij} + (1-y_{ij}) \log (1- \hat{y}^k_{ij}) \big]
$$

其中 $$y_{ij}$$ 是大小为 m × m 的区域真实掩码中单元格 (i, j) 的标签；$$\hat{y}_{ij}^k$$ 是为真实类别 k 学习的掩码中同一单元格的预测值。

## R-CNN 家族模型总结

这里我图示了 R-CNN、Fast R-CNN、Faster R-CNN 和 Mask R-CNN 的模型设计。你可以通过对比细微差别来追踪一个模型如何演进到下一个版本。

![R-CNN 家族总结](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/rcnn-family-summary.png)

---
引用格式：
```
@article{weng2017detection3,
  title   = "Object Detection for Dummies Part 3: R-CNN Family",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2017",
  url     = "http://lilianweng.github.io/lil-log/2017/12/31/object-recognition-for-dummies-part-3.html"
}
```

## 参考文献

[1] Ross Girshick, Jeff Donahue, Trevor Darrell, and Jitendra Malik. ["Rich feature hierarchies for accurate object detection and semantic segmentation."](https://www.cv-foundation.org/openaccess/content_cvpr_2014/papers/Girshick_Rich_Feature_Hierarchies_2014_CVPR_paper.pdf) In Proc. IEEE Conf. on computer vision and pattern recognition (CVPR), pp. 580-587. 2014.

[2] Ross Girshick. ["Fast R-CNN."](https://arxiv.org/pdf/1504.08083.pdf) In Proc. IEEE Intl. Conf. on computer vision, pp. 1440-1448. 2015.

[3] Shaoqing Ren, Kaiming He, Ross Girshick, and Jian Sun. ["Faster R-CNN: Towards real-time object detection with region proposal networks."](http://papers.nips.cc/paper/5638-faster-r-cnn-towards-real-time-object-detection-with-region-proposal-networks.pdf) In Advances in neural information processing systems (NIPS), pp. 91-99. 2015.

[4] Kaiming He, Georgia Gkioxari, Piotr Dollár, and Ross Girshick. ["Mask R-CNN."](https://arxiv.org/pdf/1703.06870.pdf) arXiv preprint arXiv:1703.06870, 2017.

[5] Joseph Redmon, Santosh Divvala, Ross Girshick, and Ali Farhadi. ["You only look once: Unified, real-time object detection."](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Redmon_You_Only_Look_CVPR_2016_paper.pdf) In Proc. IEEE Conf. on computer vision and pattern recognition (CVPR), pp. 779-788. 2016.

[6] ["A Brief History of CNNs in Image Segmentation: From R-CNN to Mask R-CNN"](https://blog.athelas.com/a-brief-history-of-cnns-in-image-segmentation-from-r-cnn-to-mask-r-cnn-34ea83205de4) by Athelas.

[7] Smooth L1 Loss: [https://github.com/rbgirshick/py-faster-rcnn/files/764206/SmoothL1Loss.1.pdf](https://github.com/rbgirshick/py-faster-rcnn/files/764206/SmoothL1Loss.1.pdf)
