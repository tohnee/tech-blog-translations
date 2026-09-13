---
title: "目标检测 Part 4：快速检测模型"
title_en: "Object Detection Part 4: Fast Detection Models"
source: https://lilianweng.github.io/posts/2018-12-27-object-recognition-part-4/
crawled: 2026-09-08
translated: 2026-09-08
---

# 目标检测 Part 4：快速检测模型

> 原文：[Object Detection Part 4: Fast Detection Models](https://lilianweng.github.io/posts/2018-12-27-object-recognition-part-4/) · Lilian Weng（翁荔）

> "目标检测入门"系列第 4 部分聚焦于快速检测的单阶段（one-stage）模型，包括 SSD、RetinaNet 以及 YOLO 家族的模型。这些模型跳过显式的候选区域阶段，直接在密集采样的区域上执行检测。

在[第 3 部分](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/)中，我们回顾了 R-CNN 家族的模型。它们都是基于区域的目标检测算法，能达到高精度，但对某些应用（如自动驾驶）来说可能太慢。第 4 部分只关注快速目标检测模型，包括 SSD、RetinaNet 和 YOLO 家族的模型。

本系列所有文章的链接：
[[Part 1](https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/)]
[[Part 2](https://lilianweng.github.io/posts/2017-12-15-object-recognition-part-2/)]
[[Part 3](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/)]
[[Part 4](https://lilianweng.github.io/posts/2018-12-27-object-recognition-part-4/)].

## 两阶段与单阶段检测器

R-CNN 家族的模型都是基于区域的。检测分两个阶段发生：(1) 首先，模型通过选择性搜索或区域提议网络提出一组感兴趣区域。所提议的区域是稀疏的，因为潜在的边界框候选可以有无限多个。(2) 然后分类器只处理这些区域候选。

另一条不同的路线跳过候选区域阶段，直接在可能位置的密集采样上运行检测。单阶段目标检测算法就是这样工作的。它更快更简单，但可能略微拉低性能。

本文介绍的所有模型都是单阶段检测器。

## YOLO：You Only Look Once

**YOLO** 模型（**"You Only Look Once"**；[Redmon et al., 2016](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Redmon_You_Only_Look_CVPR_2016_paper.pdf)）是构建快速实时目标检测器的第一次尝试。由于 YOLO 不经历候选区域步骤，只在有限数量的边界框上预测，它的推理速度超快。

### 工作流程

1. 在图像分类任务上**预训练**一个 CNN 网络。

2. 把图像分成 $$S \times S$$ 个单元格。若一个物体的中心落入某个单元格，该单元格就"负责"检测该物体是否存在。每个单元格预测 (a) $$B$$ 个边界框的位置，(b) 一个置信度分数，(c) 以边界框中存在物体为条件的物体类别概率。
<br/>
<br/>
- **边界框坐标**由 4 元组定义（中心 x 坐标, 中心 y 坐标, 宽, 高）——$$(x, y, w, h)$$，其中 $$x$$ 和 $$y$$ 设为相对单元格位置的偏移。此外，$$x$$、$$y$$、$$w$$、$$h$$ 都按图像宽高归一化，因此都在 (0, 1] 之间。
- **置信度分数**表示该单元格包含物体的可能性：`Pr(containing an object) x IoU(pred, truth)`；其中 `Pr` 是概率，`IoU` 是交并比。
- 若单元格包含物体，它预测该物体属于每个类别 $$C_i, i=1, \dots, K$$ 的**概率**：`Pr(the object belongs to the class C_i | containing an object)`。在此阶段，模型每个单元格只预测一组类别概率，与边界框数量 $$B$$ 无关。
- 总计，一张图像包含 $$S \times S \times B$$ 个边界框，每个框对应 4 个位置预测、1 个置信度分数和 K 个用于物体分类的条件概率。一张图像的总预测值为 $$S \times S \times (5B + K)$$，即模型最终卷积层的张量形状。
<br/>
<br/>
3. 预训练 CNN 的最后一层被修改为输出大小 $$S \times S \times (5B + K)$$ 的预测张量。

![YOLO workflow](https://lilianweng.github.io/posts/2018-12-27-object-recognition-part-4/yolo.png)

*图 1：YOLO 模型的工作流程。（图片来源：[原论文](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Redmon_You_Only_Look_CVPR_2016_paper.pdf)）*

### 网络架构

基础模型类似 [GoogLeNet](https://www.cs.unc.edu/~wliu/papers/GoogLeNet.pdf)，inception 模块被替换为 1x1 和 3x3 卷积层。形状 $$S \times S \times (5B + K)$$ 的最终预测由整个卷积特征图之上的两个全连接层产生。

![YOLO architecture](https://lilianweng.github.io/posts/2018-12-27-object-recognition-part-4/yolo-network-architecture.png)

*图 2：YOLO 的网络架构。*

### 损失函数

损失由两部分组成：边界框偏移预测的*定位损失*和条件类别概率的*分类损失*。两部分都按误差平方和计算。用两个尺度参数控制：我们想增加多少边界框坐标预测的损失（$$\lambda_\text{coord}$$），以及想降低多少不含物体框的置信度预测损失（$$\lambda_\text{noobj}$$）。降低背景框贡献的损失很重要，因为大多数边界框不含实例。论文中模型设 $$\lambda_\text{coord} = 5$$、$$\lambda_\text{noobj} = 0.5$$。

$$
\begin{aligned}
\mathcal{L}_\text{loc} &= \lambda_\text{coord} \sum_{i=0}^{S^2} \sum_{j=0}^B \mathbb{1}_{ij}^\text{obj} [(x_i - \hat{x}_i)^2 + (y_i - \hat{y}_i)^2 + (\sqrt{w_i} - \sqrt{\hat{w}_i})^2 + (\sqrt{h_i} - \sqrt{\hat{h}_i})^2 ] \\
\mathcal{L}_\text{cls}  &= \sum_{i=0}^{S^2} \sum_{j=0}^B \big( \mathbb{1}_{ij}^\text{obj} + \lambda_\text{noobj} (1 - \mathbb{1}_{ij}^\text{obj})\big) (C_{ij} - \hat{C}_{ij})^2 + \sum_{i=0}^{S^2} \sum_{c \in \mathcal{C}} \mathbb{1}_i^\text{obj} (p_i(c) - \hat{p}_i(c))^2\\
\mathcal{L} &= \mathcal{L}_\text{loc} + \mathcal{L}_\text{cls}
\end{aligned}
$$

> 注意：原版 YOLO 论文的损失函数用 $$C_i$$ 而非 $$C_{ij}$$ 作为置信度分数。基于我自己的理解我做了修正，因为每个边界框都应有自己的置信度分数。如果你不认同，请告诉我。多谢。

其中，
- $$\mathbb{1}_i^\text{obj}$$：单元格 i 是否包含物体的指示函数。
- $$\mathbb{1}_{ij}^\text{obj}$$：指示单元格 i 的第 j 个边界框是否"负责"该物体预测（见图 3）。
- $$C_{ij}$$：单元格 i 的置信度分数，`Pr(containing an object) * IoU(pred, truth)`。
- $$\hat{C}_{ij}$$：预测的置信度分数。
- $$\mathcal{C}$$：所有类别的集合。
- $$p_i(c)$$：单元格 i 包含类别 $$c \in \mathcal{C}$$ 物体的条件概率。
- $$\hat{p}_i(c)$$：预测的条件类别概率。

![YOLO responsible predictor](https://lilianweng.github.io/posts/2018-12-27-object-recognition-part-4/yolo-responsible-predictor.png)

*图 3：在某一位置的单元格 i，模型提出 B 个边界框候选，与真实标注重叠最高的那个是"负责"的预测器。*

只有当该网格单元格中存在物体（$$\mathbb{1}_i^\text{obj} = 1$$）时，损失函数才惩罚分类误差。也只有当该预测器对真实标注框"负责"（$$\mathbb{1}_{ij}^\text{obj} = 1$$）时，才惩罚边界框坐标误差。

作为单阶段目标检测器，YOLO 超快，但由于边界框候选数量有限，它不擅长识别形状不规则的物体或一群小物体。

## SSD：Single Shot MultiBox Detector

**Single Shot Detector（SSD**；[Liu et al, 2016](https://arxiv.org/abs/1512.02325)）是最早尝试利用卷积神经网络金字塔特征层级来高效检测各种尺寸物体的工作之一。

### 图像金字塔

SSD 用在 ImageNet 上预训练的 [VGG-16](https://arxiv.org/abs/1409.1556) 模型作为提取有用图像特征的基础模型。
在 VGG16 之上，SSD 添加了若干尺寸递减的卷积特征层。它们可视为不同尺度图像的*金字塔表示*。直观上，较早层的大而细粒度的特征图擅长捕捉小物体，小而粗粒度的特征图能很好地检测大物体。在 SSD 中，检测发生在每个金字塔层，针对各种尺寸的物体。

![SSD architecture](https://lilianweng.github.io/posts/2018-12-27-object-recognition-part-4/SSD-architecture.png)

*图 4：SSD 的模型架构。*

### 工作流程

与 YOLO 不同，SSD 不把图像切成任意大小的网格，而是对特征图的每个位置预测预定义*锚框*（论文中称"default boxes"）的偏移。每个框相对于其对应单元格有固定的大小和位置。所有锚框以卷积的方式铺满整个特征图。

不同层的特征图有不同的感受野大小。不同层的锚框被重新缩放，使一张特征图只负责某一特定尺度的物体。例如图 5 中，狗只能在 4x4 特征图（较高层）中被检测到，而猫恰好被 8x8 特征图（较低层）捕获。

![SSD framework](https://lilianweng.github.io/posts/2018-12-27-object-recognition-part-4/SSD-framework.png)

*图 5：SSD 框架。(a) 训练数据包含图像和每个物体的真实标注框。(b) 在细粒度特征图（8 x 8）中，不同长宽比的锚框对应原始输入的较小区域。(c) 在粗粒度特征图（4 x 4）中，锚框覆盖原始输入的较大区域。（图片来源：[原论文](https://arxiv.org/abs/1512.02325)）*

锚框的宽、高和中心位置都归一化到 (0, 1)。在大小 $$m \times n$$ 的第 $$\ell$$ 个特征层的位置 $$(i, j)$$，$$i=1,\dots,n, j=1,\dots,m$$，我们有一个与层级成正比的独特线性尺度、5 种不同的框长宽比（宽高比），此外当长宽比为 1 时还有一个特殊尺度（为什么需要这个？论文没解释，也许只是一个启发式技巧）。这样每个特征单元格共有 6 个锚框。

$$
\begin{aligned}
\text{level index: } &\ell = 1, \dots, L \\
\text{scale of boxes: } &s_\ell = s_\text{min} + \frac{s_\text{max} - s_\text{min}}{L - 1} (\ell - 1) \\
\text{aspect ratio: } &r \in \{1, 2, 3, 1/2, 1/3\}\\
\text{additional scale: } & s'_\ell = \sqrt{s_\ell s_{\ell + 1}} \text{ when } r = 1 \text{thus, 6 boxes in total.}\\
\text{width: } &w_\ell^r = s_\ell \sqrt{r} \\
\text{height: } &h_\ell^r = s_\ell / \sqrt{r} \\
\text{center location: } & (x^i_\ell, y^j_\ell) = (\frac{i+0.5}{m}, \frac{j+0.5}{n})
\end{aligned}
$$

![Box scales](https://lilianweng.github.io/posts/2018-12-27-object-recognition-part-4/SSD-box-scales.png)

*图 6：锚框大小如何随层索引 $$\ell$$ 增大的示例，$$L=6, s_\text{min} = 0.2, s_\text{max} = 0.9$$。只画了长宽比 $$r=1$$ 的框。*

在每个位置，模型对 $$k$$ 个锚框中的每一个应用一个 $$3 \times 3 \times p$$ 卷积滤波器（$$p$$ 是特征图的通道数），输出 4 个偏移和 $$c$$ 个类别概率。因此，给定大小 $$m \times n$$ 的特征图，我们需要 $$kmn(c+4)$$ 个预测滤波器。

### 损失函数

与 YOLO 相同，损失函数是定位损失与分类损失之和。

$$\mathcal{L} = \frac{1}{N}(\mathcal{L}_\text{cls} + \alpha \mathcal{L}_\text{loc})$$

其中 $$N$$ 是匹配的边界框数量，$$\alpha$$ 平衡两个损失的权重，通过交叉验证选取。

*定位损失*是预测边界框校正与真值之间的 [smooth L1 损失](https://github.com/rbgirshick/py-faster-rcnn/files/764206/SmoothL1Loss.1.pdf)。坐标校正变换与 [R-CNN](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/#r-cnn) 在[边界框回归](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/#bounding-box-regression)中所做的相同。

$$
\begin{aligned}
\mathcal{L}_\text{loc} &= \sum_{i,j} \sum_{m\in\{x, y, w, h\}} \mathbb{1}_{ij}^\text{match}
 L_1^\text{smooth}(d_m^i - t_m^j)^2\\
L_1^\text{smooth}(x) &= \begin{cases}
    0.5 x^2             & \text{if } \vert x \vert < 1\\
    \vert x \vert - 0.5 & \text{otherwise}
\end{cases} \\
t^j_x &= (g^j_x - p^i_x) / p^i_w \\
t^j_y &= (g^j_y - p^i_y) / p^i_h \\
t^j_w &= \log(g^j_w / p^i_w) \\
t^j_h &= \log(g^j_h / p^i_h)
\end{aligned}
$$

其中 $$\mathbb{1}_{ij}^\text{match}$$ 指示坐标为 $$(p^i_x, p^i_y, p^i_w, p^i_h)$$ 的第 $$i$$ 个边界框是否与坐标为 $$(g^j_x, g^j_y, g^j_w, g^j_h)$$ 的第 $$j$$ 个真实标注框按某物体匹配。$$d^i_m, m\in\{x, y, w, h\}$$ 是预测的校正项。变换如何工作见[这里](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/#bounding-box-regression)。

*分类损失*是多类上的 softmax 损失（tensorflow 的 [softmax_cross_entropy_with_logits](https://www.tensorflow.org/api_docs/python/tf/nn/softmax_cross_entropy_with_logits)）：

$$
\mathcal{L}_\text{cls} = -\sum_{i \in \text{pos}} \mathbb{1}_{ij}^k \log(\hat{c}_i^k) - \sum_{i \in \text{neg}} \log(\hat{c}_i^0)\text{, where }\hat{c}_i^k = \text{softmax}(c_i^k)
$$

其中 $$\mathbb{1}_{ij}^k$$ 指示第 $$i$$ 个边界框与第 $$j$$ 个真实标注框是否按类别 $$k$$ 的物体匹配。$$\text{pos}$$ 是匹配的边界框集合（共 $$N$$ 个），$$\text{neg}$$ 是负样本集合。SSD 用[难负例挖掘](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/#common-tricks)选取易被误分类的负样本构建 $$\text{neg}$$ 集合：把所有锚框按物体性置信度分数排序后，模型挑选最高候选用于训练，使 neg:pos 至多为 3:1。

## YOLOv2 / YOLO9000

**YOLOv2**（[Redmon & Farhadi, 2017](https://arxiv.org/abs/1612.08242)）是 YOLO 的增强版。**YOLO9000** 构建在 YOLOv2 之上，但用结合 COCO 检测数据集与 ImageNet 前 9000 类的联合数据集训练。

### YOLOv2 的改进

为使 YOLO 预测更准更快，应用了多项修改，包括：

**1. BatchNorm 有帮助**：在所有卷积层上加*批归一化*，收敛显著改善。

**2. 图像分辨率重要**：用*高分辨率*图像微调基础模型能提升检测性能。

**3. 卷积锚框检测**：不再用整个特征图上的全连接层预测边界框位置，YOLOv2 用*卷积层*预测*锚框*位置，类似 faster R-CNN。空间位置预测与类别概率预测解耦。总体上，这一变化使 mAP 略降、召回率上升。

**4. 框尺寸的 K 均值聚类**：与 faster R-CNN 使用手工挑选的锚框尺寸不同，YOLOv2 对训练数据跑 K 均值聚类以找到锚框尺寸的良好先验。距离度量被设计为*依赖 IoU 分数*：

$$
\text{dist}(x, c_i) = 1 - \text{IoU}(x, c_i), i=1,\dots,k
$$

其中 $$x$$ 是真实标注框候选，$$c_i$$ 是某个质心。最佳质心（锚框）数 $$k$$ 可用[肘部法则](https://en.wikipedia.org/wiki/Elbow_method_(clustering))选取。

聚类生成的锚框在固定框数条件下提供了更好的平均 IoU。

**5. 直接位置预测**：YOLOv2 以一种不会偏离中心位置太多的方式表述边界框预测。若框位置预测可把框放在图像的任何地方（如区域提议网络那样），模型训练可能变得不稳定。

给定网格单元格（左上角在 $$(c_x, c_y)$$）处大小 $$(p_w, p_h)$$ 的锚框，模型预测偏移和尺度 $$(t_x, t_y, t_w, t_h)$$，相应预测边界框 $$b$$ 的中心为 $$(b_x, b_y)$$、大小为 $$(b_w, b_h)$$。置信度分数是另一个输出 $$t_o$$ 的 sigmoid（$$\sigma$$）。

$$
\begin{aligned}
b_x &= \sigma(t_x) + c_x\\
b_y &= \sigma(t_y) + c_y\\
b_w &= p_w e^{t_w}\\
b_h &= p_h e^{t_h}\\
\text{Pr}(\text{object}) &\cdot \text{IoU}(b, \text{object}) = \sigma(t_o)
\end{aligned}
$$

![YOLOv2 bbox location prediction](https://lilianweng.github.io/posts/2018-12-27-object-recognition-part-4/yolov2-loc-prediction.png)

*图 7：YOLOv2 边界框位置预测。（图片来源：[原论文](https://arxiv.org/abs/1612.08242)）*

**6. 增加细粒度特征**：YOLOv2 加了一个 passthrough 层，把较早层的*细粒度特征*引至最后的输出层。该 passthrough 层的机制类似 *ResNet 的恒等映射*，从先前的层提取更高维特征。这带来 1% 的性能提升。

**7. 多尺度训练**：为使模型对各种尺寸的输入图像鲁棒，每 10 个批次*随机采样*一个*新尺寸*的输入维度。由于 YOLOv2 的卷积层把输入维度下采样 32 倍，新采样的尺寸是 32 的倍数。

**8. 轻量级基础模型**：为了预测更快，YOLOv2 采用轻量级基础模型 DarkNet-19，含 19 个卷积层和 5 个最大池化层。要点是在 3x3 卷积层之间插入平均池化和 1x1 卷积滤波器。

### YOLO9000：丰富数据集训练

由于为目标检测在图像上标注边界框比为分类打标签昂贵得多，论文提出一种把小目标检测数据集与大型 ImageNet 结合的方法，使模型能接触到多得多的物体类别。YOLO9000 的名字来自 ImageNet 的前 9000 类。联合训练时，若输入图像来自分类数据集，则只反向传播分类损失。

检测数据集的标签少得多且更泛化，而且跨数据集的标签往往不互斥。例如 ImageNet 有标签 "Persian cat"，而 COCO 中同一图像会被标为 "cat"。不互斥时，对所有类别施加 softmax 就说不通了。

为高效合并 ImageNet 标签（1000 类，细粒度）与 COCO/PASCAL（< 100 类，粗粒度），YOLO9000 参照 [WordNet](https://wordnet.princeton.edu/) 构建了层次树结构，使泛化标签靠近根、细粒度类别标签是叶子。这样，"cat" 就是 "Persian cat" 的父节点。

![WordTree](https://lilianweng.github.io/posts/2018-12-27-object-recognition-part-4/word-tree.png)

*图 8：WordTree 层次结构合并 COCO 与 ImageNet 的标签。蓝色节点是 COCO 标签，红色节点是 ImageNet 标签。（图片来源：[原论文](https://arxiv.org/abs/1612.08242)）*

要预测一个类别节点的概率，我们可以沿着从该节点到根的路径：

```
Pr("persian cat" | contain a "physical object") 
= Pr("persian cat" | "cat") 
  Pr("cat" | "animal") 
  Pr("animal" | "physical object") 
  Pr(contain a "physical object")    # confidence score.
```

注意 `Pr(contain a "physical object")` 是置信度分数，在边界框检测管线中单独预测。条件概率预测的路径可以在任意一步停止，取决于哪些标签可用。

## RetinaNet

**RetinaNet**（[Lin et al., 2018](https://arxiv.org/abs/1708.02002)）是一个单阶段密集目标检测器。两个关键构件是*特征化图像金字塔*和*焦点损失（focal loss）*的使用。

### 焦点损失

目标检测模型训练的一个问题是：不含物体的背景与含感兴趣物体前景之间的极端不平衡。**焦点损失**旨在给困难、易误分类的样本（如有噪声纹理或部分物体的背景）分配更多权重，并降低简单样本（如明显空白的背景）的权重。

从二分类的普通交叉熵损失出发，

$$
\text{CE}(p, y) = -y\log p - (1-y)\log(1-p)
$$

其中 $$y \in \{0, 1\}$$ 是真实二值标签，指示边界框是否包含物体，$$p \in [0, 1]$$ 是预测的物体性概率（即置信度分数）。

为方便记号，

$$
\text{let } p_t = \begin{cases}
p    & \text{if } y = 1\\
1-p  & \text{otherwise}
\end{cases},
\text{then } \text{CE}(p, y)=\text{CE}(p_t) = -\log p_t
$$

容易分类的样本（$$p_t \gg 0.5$$，即 $$p$$ 非常接近 0（当 y=0）或 1（当 y=1）时）仍可能产生不小的损失。焦点损失显式地给交叉熵的每一项加一个权重因子 $$(1-p_t)^\gamma, \gamma \geq 0$$，使 $$p_t$$ 大（容易）时权重小，从而降低简单样本的权重。

$$
\text{FL}(p_t) = -(1-p_t)^\gamma \log p_t
$$

![Focal Loss](https://lilianweng.github.io/posts/2018-12-27-object-recognition-part-4/focal-loss.png)

*图 9：焦点损失以因子 $$(1-p_t)^\gamma$$ 降低对简单样本的关注。（图片来源：[原论文](https://arxiv.org/abs/1708.02002)）*

为了更好地控制权重函数的形状（见图 10），RetinaNet 使用 $$\alpha$$-平衡版焦点损失，$$\alpha=0.25, \gamma=2$$ 效果最佳。

$$
\text{FL}(p_t) = -\alpha (1-p_t)^\gamma \log p_t
$$

![WordTree](https://lilianweng.github.io/posts/2018-12-27-object-recognition-part-4/focal-loss-weights.png)

*图 10：不同 $$\alpha$$ 和 $$\gamma$$ 下，焦点损失权重 $$\alpha (1-p_t)^\gamma$$ 随 $$p_t$$ 变化的图像。*

### 特征化图像金字塔

**特征化图像金字塔（featurized image pyramid**，[Lin et al., 2017](https://arxiv.org/abs/1612.03144)）是 RetinaNet 的骨干网络。沿袭 SSD 中[图像金字塔](#image-pyramid)的同一思路，特征化图像金字塔为不同尺度的目标检测提供了基础的视觉组件。

特征金字塔网络的关键思想见图 11。基础结构包含一系列*金字塔层级*，每级对应网络的一个*阶段（stage）*。一个阶段包含多个相同尺寸的卷积层，各阶段尺寸逐级缩小 2 倍。把第 $$i$$ 个阶段的最后一层记为 $$C_i$$。

![Featurized image pyramid](https://lilianweng.github.io/posts/2018-12-27-object-recognition-part-4/featurized-image-pyramid.png)

*图 11：特征化图像金字塔模块示意图。（依据 [FPN 论文](https://arxiv.org/abs/1612.03144)图 3 重绘）*

两条通路连接卷积层：
- **自底向上通路**是普通的前馈计算。
- **自顶向下通路**沿相反方向，通过横向连接把粗但语义更强的特征图加回前一个更大尺寸的金字塔层级。
    - 首先，高层特征被空间上采样为 2 倍大。图像上采样论文用的是最近邻。虽然有许多[图像上采样算法](https://en.wikipedia.org/wiki/Image_scaling#Algorithms)（如用 [deconv](https://www.tensorflow.org/api_docs/python/tf/layers/conv2d_transpose)），采用另一种缩放方法未必能提升 RetinaNet 的性能。
    - 较大的特征图经一个 1x1 卷积层降通道维。
    - 最后，两个特征图经逐元素相加融合。
    <br/>
    <br/>
    横向连接只发生在各阶段的最后一层，记作 $$\{C_i\}$$，该过程持续直到生成最精细（最大）的融合特征图。每个融合图经一个 3x3 卷积层后做预测，得到 $$\{P_i\}$$。

根据消融实验，特征化图像金字塔设计中各组件的重要性排序为：**1x1 横向连接** > 跨多层检测物体 > 自顶向下增强 > 金字塔表示（相比只看最精细层）。

### 模型架构

特征金字塔构建在 ResNet 架构之上。回忆 [ResNet](TBA) 有 5 个卷积块（= 网络阶段 / 金字塔层级）。第 $$i$$ 个金字塔层级的最后一层 $$C_i$$ 的分辨率比原始输入低 $$2^i$$。

RetinaNet 使用特征金字塔层级 $$P_3$$ 到 $$P_7$$：
- $$P_3$$ 到 $$P_5$$ 由对应的 ResNet 残差阶段 $$C_3$$ 到 $$C_5$$ 计算，二者由自顶向下和自底向上两条通路连接。
- $$P_6$$ 由 $$C_5$$ 上的 3×3 步长 2 卷积得到。
- $$P_7$$ 在 $$P_6$$ 上应用 ReLU 和 3×3 步长 2 卷积。

在 ResNet 上添加更高金字塔层级提升了大物体检测的性能。

与 SSD 相同，检测在所有金字塔层级上发生，对每个融合特征图做预测。由于预测共享同一个分类器和框回归器，它们都被整形成相同的通道维 d=256。

每层有 A=9 个锚框：
- 基础尺寸对应 $$P_3$$ 到 $$P_7$$ 上 $$32^2$$ 到 $$512^2$$ 像素的面积。有三种尺寸比 $$\{2^0, 2^{1/3}, 2^{2/3}\}$$。
- 每种尺寸有三种长宽比 {1/2, 1, 2}。

照例，对每个锚框，模型在分类子网输出 $$K$$ 个类别各自的类别概率，在框回归子网回归从该锚框到最近真实物体的偏移。分类子网采用上文介绍的焦点损失。

![RetinaNet](https://lilianweng.github.io/posts/2018-12-27-object-recognition-part-4/retina-net.png)

*图 12：RetinaNet 模型架构，在 ResNet 上使用 [FPN](https://arxiv.org/abs/1612.03144) 骨干。（图片来源：[FPN](https://arxiv.org/abs/1612.03144) 论文）*

## YOLOv3

[YOLOv3](https://pjreddie.com/media/files/papers/YOLOv3.pdf) 通过在 YOLOv2 上应用一堆设计技巧创建。这些变化的灵感来自目标检测领域的最新进展。

变化清单如下：

**1. 置信度分数用逻辑回归**：YOLOv3 用*逻辑回归*为每个边界框预测置信度分数，而 YOLO 和 YOLOv2 用误差平方和做分类项（见上文[损失函数](#loss-function)）。偏移预测的线性回归导致 mAP 下降。

**2. 类别预测不再用 softmax**：预测类别置信度时，YOLOv3 为每个类别使用*多个独立的逻辑分类器*而非一个 softmax 层。这非常有用，尤其考虑到一张图像可能有多个标签，且并非所有标签都保证互斥。

**3. Darknet + ResNet 作为基础模型**：新的 Darknet-53 依然依赖连续的 3x3 和 1x1 卷积层（与原始 darknet 架构一样），但加入了残差块。

**4. 多尺度预测**：受图像金字塔启发，YOLOv3 在基础特征提取模型之后添加若干卷积层，并在这些卷积层中的三个不同尺度上做预测。这样，总体上它要处理多得多的各种尺寸的边界框候选。

**5. 跨层拼接**：YOLOv3 还在两个预测层（输出层除外）与较早的更细粒度特征图之间添加跨层连接。模型先上采样粗特征图，然后与先前的特征拼接融合。与细粒度信息的结合使其更擅长检测小物体。

有趣的是，焦点损失对 YOLOv3 没有帮助，可能是因为 $$\lambda_\text{noobj}$$ 和 $$\lambda_\text{coord}$$ 的使用——它们已增加边界框位置预测的损失、降低背景框置信度预测的损失。

总体而言，YOLOv3 比 SSD 更好更快；不如 RetinaNet 但快 3.8 倍。

![YOLOv3 performance](https://lilianweng.github.io/posts/2018-12-27-object-recognition-part-4/yolov3-perf.png)

*图 13：多种快速目标检测模型在速度与 mAP 性能上的对比。（图片来源：[焦点损失](https://arxiv.org/abs/1708.02002)论文，加上 [YOLOv3](https://pjreddie.com/media/files/papers/YOLOv3.pdf) 论文的额外标注。）*

---
引用格式：
```
@article{weng2018detection4,
  title   = "Object Detection Part 4: Fast Detection Models",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2018",
  url     = "http://lilianweng.github.io/lil-log/2018/12/27/object-detection-part-4.html"
}
```

## 参考文献

[1] Joseph Redmon, et al. ["You only look once: Unified, real-time object detection."](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Redmon_You_Only_Look_CVPR_2016_paper.pdf) CVPR 2016.

[2] Joseph Redmon and Ali Farhadi. ["YOLO9000: Better, Faster, Stronger."](http://openaccess.thecvf.com/content_cvpr_2017/papers/Redmon_YOLO9000_Better_Faster_CVPR_2017_paper.pdf) CVPR 2017.

[3] Joseph Redmon, Ali Farhadi. ["YOLOv3: An incremental improvement."](https://pjreddie.com/media/files/papers/YOLOv3.pdf).

[4] Wei Liu et al. ["SSD: Single Shot MultiBox Detector."](https://arxiv.org/abs/1512.02325) ECCV 2016.

[5] Tsung-Yi Lin, et al. ["Feature Pyramid Networks for Object Detection."](https://arxiv.org/abs/1612.03144) CVPR 2017.

[6] Tsung-Yi Lin, et al. ["Focal Loss for Dense Object Detection."](https://arxiv.org/abs/1708.02002) IEEE transactions on pattern analysis and machine intelligence, 2018.

[7] ["What's new in YOLO v3?"](https://towardsdatascience.com/yolo-v3-object-detection-53fb7d3bfe6b) by  Ayoosh Kathuria on "Towards Data Science", Apr 23, 2018.
