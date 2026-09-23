---
title: "以全新 Detectron2 Mask R-CNN 基线推进计算机视觉研究"
title_en: "Advancing computer vision research with new Detectron2 Mask R-CNN baselines"
date: 2021-06-21
source: http://ai.facebook.com/blog/advancing-computer-vision-research-with-new-detectron2-mask-r-cnn-baselines
crawled: 2026-09-22
translated: 2026-09-22
---

# 以全新 Detectron2 Mask R-CNN 基线推进计算机视觉研究

> 原文：[Advancing computer vision research with new Detectron2 Mask R-CNN baselines](http://ai.facebook.com/blog/advancing-computer-vision-research-with-new-detectron2-mask-r-cnn-baselines) · Meta AI（Wayback 存档）

**研究内容：**自 Facebook AI 于 2018 年发布我们最先进的实例分割模型 Mask R-CNN 以来，它已成为计算机视觉研究和应用中被广泛使用的核心工具。我们现在分享新的、显著改进的基线，它们基于该领域其他专家最近发表的最先进结果。我们还就这些改进如何实现提供了新分析，并在我们的开源检测库 Detectron2 中加入了新的基线配方（recipe），让其他研究者可以轻松复现并在此基础上继续发展。

如果没有度量结果并与他人工作比较的手段，就很难取得快速的科学进展。AI 研究者用基线来做这件事，因为它们可以作为易于复现的标尺。但由于该领域演进迅速，我们必须经常更新基线以反映领域的进步。该领域近期的工作（如 Simple Copy-Paste 数据增强）在两项核心任务——为物体创建边界框以及在不同物体上绘制精细掩码——上带来了（以平均精度 AP 度量的）显著准确率提升。该论文报告的最高 Mask R-CNN ResNet-50-FPN 基线为 47.2 Box AP 和 41.8 Mask AP，超过了 Detectron2 报告的最高基线 41.0 Box AP 和 37.2 Mask AP。这一差距很重要，因为多数研究论文发表的改进幅度在 1% 到 3% 的量级。若不能透彻理解基线间的这一差距并复现这些结果，研究界就难以推进自己的工作，也难以理解他人性能提升的来源。在本例中，AP 的这些非常显著的改进似乎可归因于两个简单因素：更长的训练和更强的随机图像缩放增强。

（图：使用新 Mask R-CNN 基线得到的边界框预测。）

**工作原理：**复现研究是推进科学知识的核心机制，但实践中往往很难。特定实验的细节可能不清晰或不可得，不同实验室可能使用不同的硬件（如用 Tensor Processing Unit 而非 GPU）和软件平台（如 TensorFlow 与 PyTorch），这可能引入输出的细微差异。负责任一直是 Facebook AI 的特别关注点，例如可复现性清单和挑战，以及我们与 Papers with Code 的合作。

为复现上述 Copy-Paste 论文实现的 ResNet-50-FPN 基线，我们从 Mask R-CNN 的 TensorFlow 实现入手，用 COCO 数据集训练该论文的配方。（我们利用 Bottleneck Transformer 论文的信息，近似了某些不可得的实现细节。）下一步，我们在 Detectron2 中实现了尺度抖动（Scale Jitter）算法（Copy-Paste 论文基线使用的主要数据增强方法）。尽管 TensorFlow 实现与基于 PyTorch 的 Detectron2 实现之间存在许多底层差异，我们想检验「更长训练 + 更强数据增强」这些基本原理是否对这些底层细节稳健。新配方把 Mask R-CNN ResNet-50-FPN 的 Box AP 指标从 41（使用 ImageNet 初始化）提升到 46.7（使用 ImageNet 初始化）和 47.4（使用随机初始化）。

我们做了一系列消融实验，以理解是哪些超参数变化驱动了这些改进。为了看能否把准确率推得更高，我们还尝试了更大的图像配合更深的模型。我们的实验表明：

- 更长的训练日程、更大的输入图像尺寸和更大的尺度抖动范围对 AP 有正向影响。
- Box AP 和 Mask AP 随训练日程的增加持续提升（如上图所示）。
- 在 144 epoch 日程下训练时，Box AP 和 Mask AP 在尺度抖动 0.5–1.6 处趋于饱和（如下图所示）。
- 如下表所示，Sync Batch Norm、Weight Decay 以及更深的区域建议网络（RPN）和感兴趣区域（ROI）头对 Box AP 和 Mask AP 也有正向影响。
- 启用 PyTorch 的自动混合精度（AMP）和 FP16 使训练速度提升 30%，且不降低 Box AP 和 Mask AP。这些性能提升是在一个八节点集群上测得的，每个节点配备八块 Nvidia V100 32GB GPU。
- 更深的头有望进一步提升 AP，需要在广泛的训练日程上进一步研究。

（图：在 144 epoch 日程下训练时，Box AP 和 Mask AP 在尺度抖动 0.5–1.6 处趋于饱和。）

消融实验：

| 配置 | Box AP | Mask AP | 备注 |
|---|---|---|---|
| LSj，144 Epochs，RandomInit | 45.2 | 41.0 | 我们使用 144 epoch 日程（而非 396 epoch 日程）做消融实验，以缩短训练时间。 |
| - SyncBN，+ Group Norm | 43.5 (-1.7) | 39.8 (-1.2) | |
| + AMP，FP16 梯度 | 44.9 (-0.3) | 40.5 (-0.5) | 使用 AMP 和 FP16 使吞吐提升 30%。 |
| D2 默认权重衰减 | 43.7 (-1.6) | 39.7 (-1.3) | 权重衰减从 4E-5 增加到 1E-4。 |
| D2 默认边界框头 | 44.0 (-1.2) | 40.1 (-0.9) | 用 2 个全连接层替换 4 卷积 + 1 全连接。 |

（图：该图总结了我们的消融实验结果。）

**为什么重要：**对于从 AR 特效到检测有害内容等各类计算机视觉任务，性能在很大程度上取决于所用图像检测模型的准确性。提升 AP 可以直接改善 Portal 等产品的用户体验——Portal 的智能摄像系统由我们的 Mask R-CNN2Go 算法驱动，能在视频通话中像经验丰富的摄像师那样智能取景。通过在此分享我们的工作并用 Detectron2 加以实现，我们希望不仅帮助他人构建更好的计算机视觉工具，也让研究界可以轻松把它们作为新检测研究的基础。最终，我们希望这有助于在构建能攻克挑战性计算机视觉任务的机器方面带来新突破。

在 GitHub 获取：新基线、训练配方、Detectron2

**作者**

- Vaibhav Aggarwal，研究工程师
- Wan-Yen Lo，研究工程经理
- Yuxin Wu，研究工程师
- Ross Girshick，研究科学家
