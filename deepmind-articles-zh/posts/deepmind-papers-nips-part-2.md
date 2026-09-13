---
title: "DeepMind 论文精选 @ NIPS（第二部分）"
title_en: "DeepMind Papers @ NIPS (Part 2)"
source: https://deepmind.google/blog/deepmind-papers-nips-part-2/
site: deepmind
date: 2016-12-05
crawled: 2026-09-13
translated: 2026-09-13
---

# DeepMind 论文精选 @ NIPS（第二部分）

> 原文：[DeepMind Papers @ NIPS (Part 2)](https://deepmind.google/blog/deepmind-papers-nips-part-2/) · Google DeepMind

*本系列博客的第二篇，简要介绍我们将在巴塞罗那 NIPS 2016 大会上展示的论文。*

## Sequential Neural Models with Stochastic Layers

**作者：** Marco Fraccaro, Søren Kaae Sønderby, Ulrich Paquet, Ole Winther

我们对世界的许多推理都是顺序进行的：从聆听声音、人声和音乐，到想象自己走向目的地的每一步，再到随时间追踪一个网球。所有这些序列中都蕴含着某种潜在随机结构。循环神经网络（RNN）与随机状态空间模型（SSM）是两种强大且互补的模型，被广泛用于对这类序列数据建模。RNN 擅长捕捉数据中较长期的依赖关系，而 SSM 则对序列底层潜在随机结构中的不确定性建模，非常适合追踪与控制。

能否兼得两者之长？在本文中，我们展示了如何通过精心地把确定性（RNN）层与随机（SSM）层叠合起来做到这一点。我们展示了如何高效地对序列当前潜在的隐结构进行推理：既可以在只给定其过去的情况下（滤波，filtering），也可以在给定其过去与未来的情况下（平滑，smoothing）。

更多细节与相关工作，请参阅论文：<https://arxiv.org/abs/1605.07571>

**NIPS 现场信息：** 12 月 6 日（周二）17:20 - 17:40 @ Area 1+2（口头报告，Deep Learning 分会场）
12 月 6 日（周二）18:00 - 21:30 @ Area 5+6+7+8 #179

## Learning to learn by gradient descent gradient descent

**作者：** Marcin Andrychowicz, Misha Denil, Sergio Gomez, Matthew Hoffman, David Pfau, Tom Schaul, Nando De Freitas

如今的优化算法通常由人工设计；算法设计者针对每个问题深入思考，得以设计出利用他们能精确刻画的结构的算法。这一设计过程酷似 2000 年代初计算机视觉领域的努力：用手工设计的特征去刻画和定位图像中的边缘、角点等特征。现代计算机视觉最大的突破，正是转而直接从数据中学习这些特征，从而把人工工程从流程中移除。本文展示了如何把这些技术扩展到算法设计上——不仅学习特征，还学习学习过程本身。

我们展示了如何把优化算法的设计转化为一个学习问题，让算法以自动的方式学会利用所关注问题的结构。我们学到的算法在其训练所针对的任务上超越了标准的人工设计对手，并且能很好地泛化到结构相似的新任务上。我们在多个任务上证明了这一点，包括神经网络训练以及用神经艺术为图像造型。

更多细节与相关工作，请参阅论文：<https://arxiv.org/abs/1606.04474>

**NIPS 现场信息：** 12 月 6 日（周二）18:00 - 21:30 @ Area 5+6+7+8 #9
12 月 8 日（周四）14:00 - 21:30 @ Area 1+2（Deep Learning 研讨会 - 海报）
12 月 9 日（周五）08:00 - 18:30 @ Area 1（DeepRL 研讨会 - Nando De Freitas 报告）
12 月 9 日（周五）08:00 - 18:30 @ Area 5+6（Nonconvex Optimization for Machine Learning: Theory and Practice - Nando De Freitas 报告）
12 月 10 日（周六）08:00 - 18:30 @ Area 2（Optimizing the Optimizers - Matthew W. Hoffman 报告）

## An Online Sequence-to-Sequence Model Using Partial Conditioning

**作者：** Navdeep Jaitly, Quoc V. Le, Oriol Vinyals, Ilya Sutskever, David Sussillo, Samy Bengio

![使用部分条件化的在线序列到序列模型示意图，展示编码器层与转导器层之间的交互。](https://lh3.googleusercontent.com/DMg4X_XVZv27ROfuZgBMZmflL2zjsJl7Ip8O751YeBJR5V1_VUbp4c44JjQnCWIAYCosfLYQ0XLaZgLByMNucXzgHul7E5_R09swlzAS0fAEJNqpY1M=w1440)

把一个观测序列映射为另一个序列的模型（序列到序列）在过去两年极为流行，原因在于其通用性，在翻译、图像描述生成或句法分析等多种任务上都取得了最先进的结果。这些模型的主要缺点是：必须先读入完整的输入序列「x」，然后才开始生成输出序列「y」。在本文中，我们绕开了这些限制，允许模型在尚未读完全部输入序列时就发出输出符号。虽然这引入了一些独立性假设，但在语音识别或机器翻译等特定领域中，能够在线地做出决策会让这类模型更合乎需求。

更多细节与相关工作，请参阅论文<http://papers.nips.cc/paper/6594-an-online-sequence-to-sequence-model-using-partial-conditioning.pdf>

**NIPS 现场信息：** 12 月 6 日（周二）18:00 - 21:30 @ Area 5+6+7+8 #53

## Memory-Efficient Backpropagation through time

**作者：** Audrunas Gruslys, Remi Munos, Ivo Danihelka, Marc Lanctot, Alex Graves

许多最先进的成果都是通过在长输入序列上训练大型循环模型取得的。由于种种原因，训练循环网络并非易事。其中之一的复杂之处，在于标准的随时间反向传播（BPTT）算法内存消耗巨大，因为它需要记住全部或几乎全部过去时刻的神经元激活。在训练卷积循环网络时尤其容易耗尽宝贵的 GPU 显存，而内存约束常常导致在网络规模上做出不情愿的妥协。一个常用的缓解办法是只记住部分中间神经元激活，其余的按需重新计算。虽然已有许多在内存与计算之间权衡的启发式方法，但它们大多只适用于某些特定边界情形，并非最优。我们把这个问题看作一个动态规划问题，从而找到了在内存约束下可证明最优的一类策略。对于长度为 1000 的序列，我们的算法节省了 95% 的内存占用，而每个学习步骤只比标准 BPTT 多用三分之一的时间。

更多细节与相关工作，请参阅论文 [https://papers.nips.cc/paper/6220-memory-efficient-backpropagation-through-time.pdf](https://arxiv.org/abs/1606.03401)

**NIPS 现场信息：** 12 月 6 日（周二）18:00 - 21:30 @ Area 5+6+7+8 #64

## Towards Conceptual Compression

**作者：** Karol Gregor, Frederic Besse, Danilo Rezende, Ivo Danihelka, Daan Wierstra

发现高层次的抽象表示是无监督学习的首要目标之一。我们通过设计一个架构来切入这一问题：它把存储在像素中的信息变换为有序的、承载信息的表示序列。训练会产生一种涌现的次序：靠前的表示承载图像更全局、更概念性的信息，而靠后的表示则对应细节。该模型是一个受 DRAW 启发、全卷积的序列化变分自编码器。架构简单而同质，因此不需要做许多设计抉择。

所得到的信息变换可用于有损压缩：只传输靠前的那组表示（其数量由期望的压缩级别决定），再用生成模型生成其余表示以及图像。如果模型发现的信息次序与人类按重要性判定的信息次序高度相关，那么该算法传输的将是人类认为最重要的内容。如果其余变量的生成能产生高质量的图像，这种方法就应能带来高质量的有损压缩。由于人类和无监督算法都在尝试理解数据，且都使用深度网络来做到这一点，我们有充分的理由相信这一方法行得通。我们证明了情况确实如此，当前模型取得的性能已可与 JPEG 和 JPEG 2000 相媲美。随着生成模型不断进步，这些结果展示了该方法在构建未来压缩算法方面的潜力。

更多细节与相关工作，请参阅论文：<http://papers.nips.cc/paper/6542-towards-conceptual-compression.pdf>

**NIPS 现场信息：** 12 月 6 日（周二）18:00 - 21:30 @ Area 5+6+7+8 #77

## Unsupervised Learning of 3D Structure from Images

**作者：** Danilo Rezende, Ali Eslami, Shakir Mohamed, Peter Battaglia, Max Jaderberg, Nicolas Heess

![无监督 3D 结构学习模型的架构图，展示从训练输入出发，经过推断网络与 3D 结构模型，再到学习所得或指定的渲染器的流程。](https://lh3.googleusercontent.com/mtak3QbTGXQ04Bo94QuVIIBJsX1VmYak1k7QDw14g0J4nlmrswYukcuCyveOhD5lxDvapLojjhRcG5wdbhpcw4EHgrO1dBqDqpZCV7mQn3v3laOe1g=w1440)

想象你在看一张椅子的照片。你看到的图像是相机属性与位置、灯光、当然还有椅子形状的复杂函数。重要的是，由于自遮挡，你永远看不到整把椅子，因此存在无穷多个与你所见相符的椅子状物体。尽管如此，当被问及如何从另一个视角想象椅子的形状时，你多半能相当准确地做到。这种能力的关键不仅在于对透视、遮挡与成像过程的隐式理解，更关键的在于你对「一把合理的椅子应当长什么样」的先验知识，它让你得以「补全」缺失的部分。

在本文中，我们研究能够执行类似推理的模型。具体而言，我们构建了能够学习物体三维形状统计规律的生成模型。由此得到的形状先验可以生成高质量样本，并使我们能够把诸如「根据 2D 图像恢复合理的 3D 结构」这类病态的难题表述为概率推断，从而准确捕捉后验的多模态性。这种推断只需神经网络的一次前向传播即可快速完成；我们还展示了模型与推断网络都可以直接从 2D 图像端到端地训练，完全无需真实 3D 标签，从而首次证明了以纯无监督方式学习推断世界 3D 表示的可行性。

更多细节与相关工作，请参阅论文 <https://arxiv.org/abs/1607.00662> 及我们的视频：<https://www.youtube.com/watch?v=stvDAGQwL5c>

**NIPS 现场信息：** 12 月 7 日（周三）18:00 - 21:30 @ Area 5+6+7+8 #2
