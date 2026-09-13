---
title: "目标检测入门 Part 2：CNN、DPM 与 Overfeat"
title_en: "Object Detection for Dummies Part 2: CNN, DPM and Overfeat"
source: https://lilianweng.github.io/posts/2017-12-15-object-recognition-part-2/
crawled: 2026-09-08
translated: 2026-09-08
---

# 目标检测入门 Part 2：CNN、DPM 与 Overfeat

> 原文：[Object Detection for Dummies Part 2: CNN, DPM and Overfeat](https://lilianweng.github.io/posts/2017-12-15-object-recognition-part-2/) · Lilian Weng（翁荔）

> 第 2 部分介绍几种用于图像分类的经典卷积神经网络架构设计（AlexNet、VGG、ResNet），以及用于目标识别的 DPM（可变形部件模型）和 Overfeat 模型。

"目标检测入门"系列的[第 1 部分](https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/)介绍了：(1) 图像梯度向量的概念以及 HOG 算法如何汇总一张图像中所有梯度向量的信息；(2) 图像分割算法如何检测可能包含物体的区域；(3) 选择性搜索算法如何精炼图像分割的结果以获得更好的候选区域。

在第 2 部分中，我们将进一步了解用于图像分类的经典卷积神经网络架构。它们为后续目标检测深度学习模型的进步奠定了___基础___。想了解更多 R-CNN 及相关模型，请看[第 3 部分](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/)。

本系列所有文章的链接：
[[Part 1](https://lilianweng.github.io/posts/2017-10-29-object-recognition-part-1/)]
[[Part 2](https://lilianweng.github.io/posts/2017-12-15-object-recognition-part-2/)]
[[Part 3](https://lilianweng.github.io/posts/2017-12-31-object-recognition-part-3/)]
[[Part 4](https://lilianweng.github.io/posts/2018-12-27-object-recognition-part-4/)].

## 用于图像分类的 CNN

CNN 是 "**Convolutional Neural Network**"（卷积神经网络）的缩写，是深度学习世界中计算机视觉问题的首选方案。它在某种程度上[受启发](https://lilianweng.github.io/posts/2017-06-21-overview/#convolutional-neural-network)于人类视觉皮层系统的工作方式。

### 卷积运算

我强烈推荐这份卷积运算[指南](https://arxiv.org/pdf/1603.07285.pdf)，它以大量可视化和示例给出了干净而扎实的讲解。这里我们聚焦二维卷积，因为本文处理的是图像。

简而言之，卷积运算把预定义的[核](https://en.wikipedia.org/wiki/Kernel_(image_processing))（也称"滤波器"）在输入特征图（图像像素矩阵）上滑动，将核的值与部分输入特征相乘再相加，生成输出。这些值构成一个输出矩阵——通常核比输入图像小得多。

![卷积运算](https://lilianweng.github.io/posts/2017-12-15-object-recognition-part-2/convolution-operation.png)

*图 1：在输入特征图上应用核以生成输出的示意图。（图片来源：[River Trail documentation](http://intellabs.github.io/RiverTrail/tutorial/)）*

图 2 展示了两个真实示例：如何把一个 3x3 的核在 5x5 的二维数值矩阵上卷积，生成一个 3x3 的矩阵。通过控制填充（padding）大小和步长（stride），我们可以生成特定尺寸的输出矩阵。

![卷积运算](https://lilianweng.github.io/posts/2017-12-15-object-recognition-part-2/numerical_no_padding_no_strides.gif)
![卷积运算](https://lilianweng.github.io/posts/2017-12-15-object-recognition-part-2/numerical_padding_strides.gif)

*图 2：二维卷积运算的两个示例：（上）无填充且步长 1x1；（下）1x1 边界零填充且步长 2x2。（图片来源：[deeplearning.net](http://deeplearning.net/software/theano_versions/dev/tutorial/conv_arithmetic.html)）*

### AlexNet（Krizhevsky et al, 2012）
- 5 个卷积层 [+ 可选的最大池化] + 2 个 MLP 层 + 1 个 LR 层
- 使用数据增强技术扩充训练数据集，如图像平移、水平翻转和图块裁取。

![卷积运算示例](https://lilianweng.github.io/posts/2017-12-15-object-recognition-part-2/alex_net_illustration.png)

*图 3：AlexNet 的架构。（图片来源：[链接](http://vision03.csail.mit.edu/cnn_art/index.html)）*

### VGG（Simonyan and Zisserman, 2014）
- 该网络在当年被认为是"非常深"的；19 层。
- 架构极度简化，只使用 3x3 卷积层和 2x2 池化层。小滤波器的堆叠以更少的参数模拟了一个更大的滤波器。

### ResNet（He et al., 2015）
- 网络确实非常深；152 层的简单架构。
- **残差块（Residual Block）**：某一层的部分输入可以被传递给两层之后的组件。残差块对于保持深层网络可训练并最终能正常工作至关重要。若没有残差块，由于[梯度消失与梯度爆炸](http://www.wildml.com/2015/10/recurrent-neural-networks-tutorial-part-3-backpropagation-through-time-and-vanishing-gradients/)，普通网络的训练损失不会随层数增加而单调下降。

![残差块](https://lilianweng.github.io/posts/2017-12-15-object-recognition-part-2/residual-block.png)

*图 4：ResNet 残差块的示意图。在某种意义上，我们可以说残差块的设计受启发于人类视觉皮层系统中 V4 直接从 V1 获取输入的方式。（左图来源：[Wang et al., 2017](https://arxiv.org/pdf/1312.6229.pdf)）*

## 评估指标：mAP

许多目标识别与检测任务中常用的评估指标是 "**mAP**"，即 "**mean average precision**"（平均精度均值）的缩写。它是一个 0 到 100 之间的数，越高越好。
- 把所有测试图像的全部检测结果合并，为每个类别绘制一条精确率-召回率曲线（PR 曲线）；"平均精度"（AP）即 PR 曲线下的面积。
- 由于目标物体属于不同类别，我们先对每个类别分别计算 AP，再对类别取平均。
- 若一次检测与真实标注框的**交并比（intersection over union，IoU）**大于某个阈值（通常为 0.5；此时指标记作 "mAP@0.5"），则该检测为真正例（true positive）。

## 可变形部件模型

可变形部件模型（Deformable Parts Model，DPM）（[Felzenszwalb et al., 2010](http://people.cs.uchicago.edu/~pff/papers/lsvm-pami.pdf)）用可变形部件的混合图模型（马尔可夫随机场）来识别物体。该模型由三个主要组件构成：
1. 一个粗糙的___根滤波器（root filter）___定义一个大致覆盖整个物体的检测窗口。滤波器为一个区域特征向量指定权重。
2. 多个覆盖物体较小部件的___部件滤波器（part filter）___。部件滤波器以根滤波器两倍的分辨率学习。
3. 一个用于为部件滤波器相对于根的位置打分的___空间模型（spatial model）___。

![DPM](https://lilianweng.github.io/posts/2017-12-15-object-recognition-part-2/DPM.png)

*图 5：DPM 模型包含 (a) 一个根滤波器、(b) 多个两倍分辨率的部件滤波器，以及 (c) 一个为部件位置与形变打分的模型。*

检测物体的质量由滤波器的得分减去形变代价来度量。用外行话说，匹配得分 $$f$$ 为：

$$
f(\text{model}, x) = f(\beta_\text{root}, x) + \sum_{\beta_\text{part} \in \text{part filters}} \max_y [f(\beta_\text{part}, y) - \text{cost}(\beta_\text{part}, x, y)]
$$

其中，
- $$x$$ 是具有指定位置和尺度的图像；
- $$y$$ 是 $$x$$ 的一个子区域。
- $$\beta_\text{root}$$ 是根滤波器。
- $$\beta_\text{part}$$ 是一个部件滤波器。
- cost() 度量部件偏离其相对于根的理想位置的惩罚。

基本的打分模型是滤波器 $$\beta$$ 与区域特征向量 $$\Phi(x)$$ 的点积：$$f(\beta, x) = \beta \cdot \Phi(x)$$。特征集 $$\Phi(x)$$ 可以由 HOG 或其他类似算法定义。

根位置的高得分检测到一个很可能包含物体的区域，而各部件的高得分位置确认一个被识别的物体假设。论文采用隐 SVM（latent SVM）来建模分类器。

![DPM 匹配过程](https://lilianweng.github.io/posts/2017-12-15-object-recognition-part-2/DPM-matching.png)

*图 6：DPM 的匹配过程。（图片来源：[Felzenszwalb et al., 2010](http://people.cs.uchicago.edu/~pff/papers/lsvm-pami.pdf)）*

作者后来提出，DPM 与 CNN 并不是目标识别的两种截然不同的方法。恰恰相反，通过展开 DPM 的推断算法并把每一步映射到等价的 CNN 层，一个 DPM 模型可以被表述为 CNN。（细节见 [Girshick et al., 2015](https://www.cv-foundation.org/openaccess/content_cvpr_2015/papers/Girshick_Deformable_Part_Models_2015_CVPR_paper.pdf)！）

## Overfeat

Overfeat [[论文](https://pdfs.semanticscholar.org/f2c2/fbc35d0541571f54790851de9fcd1adde085.pdf)][[代码](https://github.com/sermanet/OverFeat)] 是将目标检测、定位与分类任务全部整合进一个卷积神经网络的先驱模型。其主要思想是：(i) 以滑动窗口的方式在图像多个尺度的区域上的不同位置做图像分类，(ii) 用在同一组卷积层之上训练的回归器预测边界框位置。

Overfeat 模型架构与 [AlexNet](#alexnet-krizhevsky-et-al-2012) 非常相似。它的训练方式如下：

![Overfeat 训练](https://lilianweng.github.io/posts/2017-12-15-object-recognition-part-2/overfeat-training.png)

*图 7：Overfeat 模型的训练阶段。（图片来源：[链接](http://vision.stanford.edu/teaching/cs231b_spring1415/slides/overfeat_eric.pdf)）*

1. 在图像分类任务上训练一个 CNN 模型（类似 AlexNet）。
2. 然后，把顶部的分类器层替换为一个回归网络，训练它在每个空间位置和尺度上预测物体边界框。该回归器是类别相关的，每个图像类别各生成一个。
	- 输入：带分类标签和边界框的图像。
	- 输出：$$(x_\text{left}, x_\text{right}, y_\text{top}, y_\text{bottom})$$，共 4 个值，表示边界框各边的坐标。
	- 损失：回归器的训练目标是最小化每个训练样本中生成的边界框与真实标注之间的 $$l2$$ 范数。

在检测时，
1. 用预训练的 CNN 模型在每个位置执行分类。
2. 在分类器生成的所有已分类区域上预测物体边界框。
3. 合并那些在定位上充分重叠、且分类器认为属于同一物体的置信度充分的边界框。

---
引用格式：
```
@article{weng2017detection2,
  title   = "Object Detection for Dummies Part 2: CNN, DPM and Overfeat",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2017",
  url     = "http://lilianweng.github.io/lil-log/2017/12/15/object-recognition-for-dummies-part-2.html"
}
```

## 参考文献

[1] Vincent Dumoulin and Francesco Visin. ["A guide to convolution arithmetic for deep learning."](https://arxiv.org/pdf/1603.07285.pdf) arXiv preprint arXiv:1603.07285 (2016).

[2] Haohan Wang, Bhiksha Raj, and Eric P. Xing. ["On the Origin of Deep Learning."](https://arxiv.org/pdf/1702.07800.pdf) arXiv preprint arXiv:1702.07800 (2017).

[3] Pedro F. Felzenszwalb, Ross B. Girshick, David McAllester, and Deva Ramanan. ["Object detection with discriminatively trained part-based models."](http://people.cs.uchicago.edu/~pff/papers/lsvm-pami.pdf) IEEE transactions on pattern analysis and machine intelligence 32, no. 9 (2010): 1627-1645.

[4] Ross B. Girshick, Forrest Iandola, Trevor Darrell, and Jitendra Malik. ["Deformable part models are convolutional neural networks."](https://www.cv-foundation.org/openaccess/content_cvpr_2015/papers/Girshick_Deformable_Part_Models_2015_CVPR_paper.pdf
) In Proc. IEEE Conf. on Computer Vision and Pattern Recognition (CVPR), pp. 437-446. 2015.

[5] Sermanet, Pierre, David Eigen, Xiang Zhang, Michaël Mathieu, Rob Fergus, and Yann LeCun. ["OverFeat: Integrated Recognition, Localization and Detection using Convolutional Networks"](https://pdfs.semanticscholar.org/f2c2/fbc35d0541571f54790851de9fcd1adde085.pdf) arXiv preprint arXiv:1312.6229 (2013).
