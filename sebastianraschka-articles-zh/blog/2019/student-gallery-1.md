---
title: "UW-Madison 学生项目展示"
title_en: "UW-Madison Student Projects Gallery"
source: https://sebastianraschka.com/blog/2019/student-gallery-1.html
crawled: 2026-09-06
translated: 2026-09-06
---

# UW-Madison 学生项目展示

> 原文：[UW-Madison Student Projects Gallery](https://sebastianraschka.com/blog/2019/student-gallery-1.html)

就在不久之前的 2018 年夏天，在度过了约 5 年漫长而富有成效的时光并取得博士学位之后，我怀着无比激动的心情加入了威斯康星大学麦迪逊分校的[统计系](https://stat.wisc.edu)。如今，两个学期过去、期末考试周也结束了，我终于找到几个安静的日子，回顾一下这期间发生的事情。

在 UW-Madison 的第一年里，除了推进我的[研究项目](http://pages.stat.wisc.edu/~sraschka/publications/)之外，我的生活重心就是我教授的两门课程（每门约 70 名学生！）。秋天，我从设计和教授一门新的[机器学习课程](http://pages.stat.wisc.edu/~sraschka/teaching/stat479-fs2018/)开始；而在一个相对短暂的 2 周寒假之后，今年春天我又以同样的方式开设了一门新的[深度学习课程](http://pages.stat.wisc.edu/~sraschka/teaching/stat479-ss2019/)。由于这些是我们系新开的课程/主题，讲义材料都得从零准备。说实话，我挺喜欢这样；不过这也意味着大量的工作！而最终，一切都非常值得！

两门课程都包含各种作业以及期末考试。然而，最精彩的部分是学生们各自完成的课程项目。在这些课程项目中，每门课约 70 名学生可以自选主题，项目由三个阶段组成：

1. 一份项目提案；一篇简短的 3 页文字（不像经费申请书那么复杂 ;)），用来论证并描述他们的项目。这对学生和我来说都是一个绝佳的机会，可以在学期中段、正式投入计划之前获得/提供一些指导。
2. 学期末一场约 10 分钟的展示，既练习沟通技巧，也与其他同学分享有趣的结果和宝贵的经验——秉承小型会议的精神。
3. 一篇约 8 页的最终报告，[仿照](https://github.com/rasbt/stat479-deep-learning-ss19/tree/master/report-template) CVPR 会议论文的格式（主要是因为它是个很好的模板），练习书面沟通技巧，并为今后的研究工作积累经验。

如果你感兴趣和/或觉得有用，我所有的讲义材料都在 GitHub 上：

- [2018 年秋季机器学习课程](https://github.com/rasbt/stat479-machine-learning-fs18)
- [2019 年春季深度学习课程](https://github.com/rasbt/stat479-deep-learning-ss19)

下面，我想分享一些学生们所做的项目（两个班合计共有 46 个项目）。请注意，下面的项目并非我刻意挑选的。我只选了学生自愿分享的项目——公开分享项目并不是这些课程的要求。

（也请记住，这些项目是由此前没有任何机器学习和深度学习经验的本科生完成的。）

## 使用卷积神经网络进行音频分类

- [GitHub 仓库](https://github.com/nhaselow/stat479)
- [报告 PDF](https://github.com/nhaselow/stat479/blob/master/Audio%20Classification%20Using%20Convolutional%20Neural%20Networks.pdf)

在这个项目中，Poet Larsen、Reng Chiz Der 和 Noah Haselow 探索了音频分类的现代方法。具体来说，Poet、Reng 和 Noah 使用了最初为计算机视觉开发的深度学习架构，即卷积神经网络（CNN）。学生们实现了 CNN 架构，从频谱图中捕捉音频片段里的时间关系。他们发现[门控 CNN 架构](https://arxiv.org/abs/1612.08083)对于缓解梯度消失效应特别有帮助。

毫无疑问，由于支持音频的设备和技术大量存在——例如 Apple 的 Siri 语音助手或 Amazon 的 Echo 设备——音频分类有许多重要应用。然而，更重要的是，音频分类的进步可以改善听障人士的无障碍体验。

作为本研究的[基准测试](https://sebastianraschka.com/glossary/#benchmark "Benchmark")数据集，学生们使用了 [Google 的 Voice Ontology AudioSet](https://research.google.com/audioset/ontology/index.html)。由于计算处理能力的限制，该数据集被裁剪为 5000 个音频片段和 10 个类别（学生们观察到，下载全部 200 万个视频并将其转换为音频片段大约需要 3-5 个月）。在获得这 5000 个片段之后，学生们通过离散短时傅里叶变换把音频样本转换成频谱图。下面是两个示例：

![Student gallery 1 spectogram](https://sebastianraschka.com/images/blog/2019/student-gallery-1/spectogram.webp)

学生们主要聚焦于门控 CNN 架构，其灵感来自 Dauphin *等人*（["Language modeling with gated convolutional networks"](https://arxiv.org/abs/1612.08083)）和 Xu *等人*（["Large-scale weakly supervised audio classification using gated convolutional neural network"](https://arxiv.org/abs/1710.00343)）：

![Student gallery 1 gated cnn](https://sebastianraschka.com/images/blog/2019/student-gallery-1/gated-cnn.webp)

在这种架构中，ReLU 激活被可学习的门控线性单元（GLU）所取代，它们与 LSTM 或注意力架构有些相似，以帮助解决梯度消失问题（在这一点上也与 ResNet 架构有些类似）。

此外，学生们将门控 CNN 方法与其他为图像分类开发的 CNN 架构进行了比较，例如 [VGG](https://arxiv.org/abs/1409.1556)、[AlexNet](http://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networ) 和 [ResNet](http://openaccess.thecvf.com/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html)。结果总结在下面两个表格中：

![Student gallery 1 results table gated cnn](https://sebastianraschka.com/images/blog/2019/student-gallery-1/results-table-gated-cnn.webp)

从训练准确率来看，对于这种从频谱图进行的音频分类，门控 CNN 模型优于"常规"图像分类架构。有趣的是，增大最大池化的尺寸还能进一步提高训练准确率。学生们推测，这可能是因为最大池化有助于解决相邻声音切片之间的自相关问题。不过遗憾的是，所有模型都存在相当严重的过拟合。

过拟合问题可能源于相对较小的样本量（更大的 dropout 概率或许也能帮上忙）。一个证据是，在表格最下面两行中，分类任务的复杂度被降低为二分类问题后，训练-测试差距大幅缩小。看看这些架构在拥有更多训练样本的 10 类数据集上表现如何，将会是一件有趣的事。

尽管存在过拟合问题，但总的来说，这是一个令人兴奋的项目，它表明计算机视觉架构同样可以用于音频分类。

## 3D 卷积网络

- [GitHub](https://github.com/sberglin/Projects-and-Papers/tree/master/3D%20CNN)
- [PDF 报告](https://github.com/sberglin/Projects-and-Papers/blob/master/3D%20CNN/Report.pdf)

在这个项目中，学生们借机进一步探索了 3D 卷积神经网络，因为我们在课堂上只是简要地讲到了它们。虽然传统照片无疑更为普及，但在许多领域，3D 数据分析特别有用（这里说的是与 3D 电影相对的数据）。例如，涉及空间感知自动驾驶汽车和先进医疗（即涉及 CT 或 MRI 的医学成像）的应用，都是能从利用数据 3D 结构的深度学习技术中受益的领域。

由于这项研究是出于教学目的，Sam Berglin、Jiahui Jian 和 Lian Zheming 使用了一个 [3D MNIST 数据集](https://www.kaggle.com/daavoo/3d-mnist)来比较"传统"CNN 架构、全卷积 CNN 架构，以及一种被学生们称为"Connectome"的架构——一种[为 fMRI 数据设计的](https://link.springer.com/chapter/10.1007%2F978-3-030-00889-5_16)架构（传统上，connectome 一词指生物神经系统的接线图）。3D MNIST 数据集由原始 MNIST 数字生成的 3D 点云组成。每个 3D 图像包含 4096 个像素（16x16x16 像素），并带有通过体素化获得的 3 个颜色通道（每幅图像总计 3x4096 = 12,288 个像素）：

![Student gallery 1 3dmnist 1](https://sebastianraschka.com/images/blog/2019/student-gallery-1/3dmnist-1.webp)

然后，数据集被划分为 10,000 个训练实例、1,000 个验证实例和 1,000 个测试实例。

学生们首先实现了一个相对简单的架构，包含 3D 卷积、3D dropout、3D BatchNorm 和 3D 最大池化层：

![Student gallery 1 3d conv 1 8670932](https://sebastianraschka.com/images/blog/2019/student-gallery-1/3d-conv-1-8670932.webp)

接着，受 Springenberg *等人*的"[All Convolutional Net](https://arxiv.org/abs/1412.6806)"启发，学生们把所有最大池化层和全连接层替换为卷积层；然而，预测性能基本没有变化：

![Student gallery 1 allconv 3d 8671353](https://sebastianraschka.com/images/blog/2019/student-gallery-1/allconv-3d-8671353.webp)

随后，学生们实现了如下所示的所谓"Connectome"架构：

![Student gallery 1 connectome](https://sebastianraschka.com/images/blog/2019/student-gallery-1/connectome.webp)

虽然"Connectome"架构的表现明显逊于传统 CNN 架构和全卷积 CNN 架构，但值得注意的是，它带来了模型体积小得多的额外好处，这可能使它对嵌入式设备特别有吸引力：

![Student gallery 1 3d conv tables](https://sebastianraschka.com/images/blog/2019/student-gallery-1/3d-conv-tables.webp)

不过，所有基于 CNN 的模型都比学生们在本研究中使用的基线表现好得多：

- 多项式逻辑回归：52.6% 测试准确率
- 随机森林：52.1% 测试准确率
- K 近邻：55.3% 测试准确率

你可能知道，[在传统的 2D MNIST 数据集上，用多项式逻辑回归这类广义线性模型取得 >90% 的测试准确率是相对容易的](https://github.com/rasbt/deep-learning-book/blob/master/code/model_zoo/pytorch_ipynb/softmax-regression.ipynb)。考虑到这一点，基于 CNN 的模型的表现其实相当不错。另外请注意，除了多出一个维度带来的挑战（特征多 16 倍）之外，3D MNIST 数据集中的训练样本数量也只有原始 2D MNIST 数据集的 1/5，这使得过拟合更容易发生。

## 以封面评判一本书：一种现代做法

- [GitHub 仓库](https://github.com/yienxu/judging-a-book-by-its-cover)
- [报告 PDF](https://github.com/yienxu/judging-a-book-by-its-cover/blob/master/Report.pdf)

受俗语"不要以封面评判一本书"的启发，学生们想弄清楚"设计精良"的书籍封面是否确实能吸引更多读者——如果真是这样，这显然可以有实用的现实应用。为了解决这个问题，Yien Xu、Boyang Wei 和 Jiongyi Cao 把项目设计为由三个子任务组成：

1. 训练一个分类/序数回归 CNN 模型，根据封面图像预测一本书的受欢迎程度；
2. 使用"模型解释"算法来解释预测——哪些封面特征对预测一本书被归为受欢迎或不受欢迎的贡献最大；
3. 使用生成对抗网络（GAN）模型来生成新的受欢迎的书封。

注意，第二个要点——解释模型——只有在分类/序数回归模型能做出相当不错的预测时才有意义。同理，如果 1) 和 2) 得到了令人满意的结果，这就构成了支持性证据，表明数据集包含足够的信息来根据封面建模图书的受欢迎程度，而且 CNN 能够提取这些知识。

这个项目是全班最有创意的项目（由学生投票公认）；与此同时，它也是最有雄心的一个。虽然生成的书封并不算好看，但这依然是一个令人兴奋的项目。

学生们使用的数据集是 [Kaggle 的 Goodreads' Best Books Ever](https://www.kaggle.com/meetnaren/goodreads-best-books)，其中包含 53,618 个大小不一的书籍封面（大多数是 RGB 格式）。标签是 Goodreads 基于多种因素（包括用户平均评分和评论分数）计算出的分数。分数是按排名量表给出的，为了简化建模问题，学生们把排名量表划分为五个类别（从最好到最差）。请注意，这些类别标签是有序量表上的（序数量表，而非名义量表）。因此，在第一个子任务——预测书封的受欢迎程度——中，学生们使用了我和 Wenzhi Cao、Vahid Mirjalili 最近合作开发的用于 CNN 序数回归的 [CORAL 框架](http://arxiv.org/abs/1901.07884)，而不是传统的 Softmax+交叉熵分类器做法。

得到的训练平均误差（MAE）为 0.14——考虑到在均衡数据集上随机预测的期望 MAE 为 2.5，这个结果相对合理。然而遗憾的是，模型出现了较为严重的过拟合，测试 MAE 相对较高，达到 1.38。学生们没有尝试 L2 范数或 dropout 等正则化技术，这些方法或许有助于缓解这一过拟合问题。

无论如何，学生们接着使用 Ribeiro *等人*的 [LIME 方法](https://arxiv.org/abs/1602.04938)进行模型解释部分。就我个人而言，我会建议利用 CORAL-CNN 完全可微这一事实，使用显著性图（saliency map）或导向反向传播（guided backpropagation），不过 LIME 仍然给出了一些有趣的洞察，如下图中的《哈利·波特》示例所示（图中显示的是对图书受欢迎程度贡献最大的图像区块）：

![Student gallery 1 harry potter](https://sebastianraschka.com/images/blog/2019/student-gallery-1/harry-potter.webp)

从上图的上面一行可以看到，LIME 把书名本身与其受欢迎程度关联了起来。在下面一行中，学生们手动裁剪图像以去掉书名，LIME 随即把副标题与图书的受欢迎程度关联了起来。换句话说，我们可以猜测，CNN 模型似乎学会了提取封面文字并以此为依据做出预测，而不是依据图像的一般属性。

第三个子任务——训练 GAN 来生成新书封——遗憾的是不太成功。不过，它确实生成了一些（几乎）有趣的书封，如下所示：

![Student gallery 1 book cover generated](https://sebastianraschka.com/images/blog/2019/student-gallery-1/book-cover-generated.webp)

GAN 是出了名的难训练，而且众所周知，在展示结果时进行一些精挑细选是很常见的。总而言之，这是一个非常有趣的项目，我尤其欣赏其对模型解释的重视！

## 人脸转绘画机

- [GitHub 仓库](https://github.com/LingfengZhu/Face-to-painting-machine)
- [报告 PDF](https://github.com/LingfengZhu/Face-to-painting-machine/blob/master/STAT479_Project_Report.pdf)
- [展示幻灯片](https://github.com/LingfengZhu/Face-to-painting-machine/blob/master/479_Presentation.pdf)

人脸图像分析是一个日益流行的研究领域，催生了大量新算法和深度神经网络架构。Lingfeng Zhu、Zhuoyan Xu 和 Cecily Liu 的"Face-to-Painting Machine"（人脸转绘画机）围绕深度卷积神经网络的探索、比较和应用展开。学生们的主要目标是专门针对人脸图像做实验，他们进一步把项目划分为三个子项目：

1. 比较 VGG 和 ResNet 架构在人脸识别上的表现；
2. 使用三元组损失（triplet loss）进行人脸匹配；
3. 使用深度学习方法做照片风格迁移，将各种艺术风格应用于人脸图像。

![Student gallery 1 architectures canziani](https://sebastianraschka.com/images/blog/2019/student-gallery-1/architectures-canziani.webp)

虽然人脸识别在若干重要应用领域（最突出的是生物特征识别与安防领域）的实用性显而易见，神经风格迁移背后的动机可能就不那么一目了然了，不过学生们对它如何融入我们的现代社会给出了出色的解释：

> 基于这一特点，并考虑到人们对照片编辑类应用的疯狂迷恋，神经风格迁移的应用可以扩展为炫酷的滤镜，让人们尝试不同的滤镜效果。[...] 此外，博物馆可以使用这种方法修复受损的名画或创作新的画作。

### 使用交叉熵损失与迁移学习的人脸匹配

在这一部分，学生们构建了一个自定义网络爬虫，从 Google 图片搜索收集了 7500 张图像——该数据集包含 15 位电影演员的图像。学生们随后使用预训练的 VGG 和 ResNet 架构做迁移学习，只训练各自网络的最后一个全连接层来进行人脸匹配。得到的准确率如下所示（注意这些照片非常多样，随机预测的期望准确率为 6.7%）：

![Student gallery 1 face matching 1](https://sebastianraschka.com/images/blog/2019/student-gallery-1/face-matching-1.webp)

请注意，由于计算资源有限，模型只训练了 10 个小时（尚未完全收敛）。性能相对较低的其他可能解释是图像相对多样（未经裁剪），以及预训练模型可能不够理想（如果能收集更多数据，从头训练神经网络或许会带来更好的结果）。无论如何，学生们随后探索了一条更有成效的路线，即使用 FaceNet 的三元组损失在欧几里得空间中学习人脸嵌入，其中距离直接对应于面部相似度——随后可以使用一个距离阈值来进行人脸匹配。

### 使用三元组损失的人脸匹配

如下所示，使用 FaceNet 三元组损失函数的人脸匹配性能得到了显著提升：

![Student gallery 1 Screen Shot 2019 05 23 at 9.41.40 PM](https://sebastianraschka.com/images/blog/2019/student-gallery-1/Screen%20Shot%202019-05-23%20at%209.41.40%20PM.png)

有趣的是，最小的架构（ResNet34）取得了最佳的泛化性能。一个可能的解释是数据集相对较小，尤其是 VGG 架构可能遭受了日益严重的过拟合（提高 dropout 率或许能改善这一情况）。

为了训练基于 FaceNet 三元组损失函数的人脸匹配卷积神经网络模型，学生们使用了 [Labeled Face in the Wild](http://vis-www.cs.umass.edu/lfw/)（LFW）数据集。该数据集包含从互联网收集的 13,000 多张人脸图像，由约 6000 个不同人的照片组成。

正如原始 FaceNet 论文（[Schroff 等人，2015](http://arxiv.org/abs/1503.03832)）所指出的，学生们发现用所有正样本-锚点和负样本-锚点样本对进行训练并不理想（收敛缓慢）。

![Student gallery 1 facenet fig](https://sebastianraschka.com/images/blog/2019/student-gallery-1/facenet-fig.webp)

因此，在每个 minibatch 中只选取难负样本和难正样本进行训练可能会加快模型拟合。然而，当使用所有锚点-正样本对时，可以获得更快的收敛（以及更稳定的训练）。现在，如果只选取难负样本，我们很容易陷入局部极小值，因为标准三元组损失的梯度是不对称的，负样本-锚点对在某个点之后就停止更新，如下图所示：

[![Student gallery 1 triplet loss issue 1](https://sebastianraschka.com/images/blog/2019/student-gallery-1/triplet-loss-issue-1.webp)](https://sebastianraschka.com/images/blog/2019/student-gallery-1/triplet-loss-issue-1.jpg)

因此，更好的解决方案是聚焦于所谓的"半难"（semi-hard）样本，即距离大于锚点-正样本对的锚点-负样本对，但它们仍然算"难"，因为其测得的距离与锚点-正样本的距离相对接近。

### 基于深度学习的照片风格迁移

在这一部分，学生们重新使用了他们的自定义数据集——从 Google 图片搜索收集的 7500 张图像，包含 15 位电影演员的图像。学生们在论文中更详细地概述了这种风格迁移方法，其结果出奇地好：

![Student gallery 1 style transfer](https://sebastianraschka.com/images/blog/2019/student-gallery-1/style-transfer.webp)

## 基于歌词的音乐流派分类

- [GitHub 仓库 v1](https://github.com/c-lynn/stat479-genre-classification)
- [报告 PDF v1](https://github.com/c-lynn/stat479-genre-classification/blob/master/Lyrics_Final_Report.pdf)
- [GitHub 仓库 v2](https://github.com/jwang862/Music-Genre-Classification-Based-on-Lyrics)
- [报告 PDF v2](https://github.com/jwang862/Music-Genre-Classification-Based-on-Lyrics/blob/master/Final%20Report.pdf)

音频分类无疑是一个值得研究的有趣课题，因为它的应用领域非常广泛：比如 Apple 的 Siri 语音助手、Amazon 的 Echo 设备，等等。此外，从隐私的角度出发，人们还能想到许多潜在的有意思的应用。例如，Spotify 这类音乐服务的推荐引擎严重依赖基于用户的信息。尤其是在这个个人信息被无意泄露或被有意出售的时代，探索推荐"相似"歌曲的替代手段可能格外有意义。

在这方面，Wengie Wang、Christina Gregis 和 Yezhou Li 探索了歌词是否包含足够的信息来预测歌曲流派。在这个项目中，学生们以 [Million Song Dataset](http://millionsongdataset.com) 为起点，实现了若干 RNN 架构（原始 RNN、带长短期记忆的 RNN，以及带门控循环单元的 RNN）。

![Student gallery 1 lyrics pipeline](https://sebastianraschka.com/images/blog/2019/student-gallery-1/lyrics-pipeline.webp)

遗憾的是，Million Song Dataset 本身并不包含歌词；因此必须从 [LyricWiki](http://lyrics.wikia.com/wiki/Special:Search) 抓取歌词。流派标签来自 [Last.fm](https://www.last.fm)——注意这些是基于用户的流派标签，可能不是最准确的。虽然以 100 万首歌作为起点，但遗憾的是只有 1/5 的歌曲同时具备歌词和流派标签（约 22 万首）。而这 22 万首歌中只有约三分之一关联着英文歌词（对于这个项目，不混用多种不同语言在某种程度上是合理的）。

![Student gallery 1 wordcloud](https://sebastianraschka.com/images/blog/2019/student-gallery-1/wordcloud.webp)

虽然约 7 万首歌对训练 RNN 来说似乎是个小数据集，但结果（约 70% 测试准确率）看起来相当不错。然而，事实证明该数据集非常不均衡（偏向摇滚歌曲），这导致准确率分数被虚高：

![Student gallery 1 lyrics imbalance](https://sebastianraschka.com/images/blog/2019/student-gallery-1/lyrics-imbalance.webp)

当学生们把数据集平衡之后（每个流派只有 9600 首歌），预测准确率大幅下降：

![Student gallery 1 lyrics balanced outcome](https://sebastianraschka.com/images/blog/2019/student-gallery-1/lyrics-balanced-outcome.webp)

看来歌词可能并不包含足够多的显著信息来可靠地预测歌曲流派。不过，较低的性能也可能源于相对较小的数据集规模。探索"传统"机器学习方法或许有用，即用逻辑回归或朴素贝叶斯分类器的词袋模型作为基线。此外，另一个问题在于用户标注的流派标签相对模糊，流派之间的界限通常也不太清晰。

无论如何，虽然就预测准确率而言结果并不理想，但这是一个漂亮且技术上扎实的项目，也是实现 RNN 的一次很好的教学练习——当你有一个自定义文本数据集时，在 PyTorch 中实现 RNN 并非易事。

## STAT479：机器学习课程的项目

最后，下面是学生们从我这学期——2018 年秋季——教授的"传统机器学习"课上分享的另外两个项目。

### 基于监督学习的股票收益预测

- 作者：Samuel Ilic、Meenmo Kang、Jonathan Santoso
- [GitHub 仓库](https://github.com/meenmo/Forecasting_Stock_Returns_via_Supervised_Learning)

摘要：

> 我们把机器学习领域的方法引入时间序列股票收益预测这一由来已久的难题。我们对各种集成决策树算法以及普通最小二乘回归进行了比较分析，以做样本外收益预测。所实现的集成方法包括随机森林（Random Forest）、Bagging 和 Boosting，并在我们的分析中加以运用，以确定最佳模型。为简单起见，我们只聚焦于预测单一股票的收益，具体为 IBM，使用 2002 年 1 月至 2018 年 10 月的 OHLCV（开盘价、最高价、最低价、收盘价、成交量）数据。我们的实现使用两种不同的性能指标来训练模型，即均方误差（MSE）和 R 方（R-squared），以生成更好的测试集结果。我们发现，使用 PCA 和 LASSO 等降维技术实际上会降低我们模型的性能。最后，我们发现提升回归树（boosted regression tree）对未见数据的泛化效果最好，样本外表现最佳，R 方为一个虽小但为正的 0.06%。因此，我们以实证证据表明股市并非完全有效，因为像 IBM 这样流动性极高的股票也能以一定的准确度被预测。

[![Student gallery 1 forecasting](https://sebastianraschka.com/images/blog/2019/student-gallery-1/forecasting.webp)](https://github.com/meenmo/Forecasting_Stock_Returns_via_Supervised_Learning/blob/master/Paper.pdf)

### 汉字笔画计数

- 作者：Yien Xu、Yuqi Lin、Scott Lai
- [GitHub 仓库](https://github.com/yienxu/counting-strokes-in-chinese-characters)

摘要：

> 我们使用机器学习算法对图像形式的汉字进行笔画数计数。作为以自己的语言为荣的中国留学生，我们希望找到一种好方法，帮助更多[人](https://sebastianraschka.com/glossary/#per-layer-embeddings "Per-Layer Embeddings (PLE)")学习中文。为此，我们构建了一个汉字笔画数识别系统：如果输入一幅 28 × 28 像素的汉字图像，我们就能够判断它有多少个笔画。为了统一笔画特征的定义，我们使用 Unicode 中的定义作为数据库之一，其中总共包含 36 种笔画特征。我们还将数据集划分为 90% 训练集和 10% 测试集。我们使用的模型包括 k 近邻算法（kNN）、逻辑回归和卷积神经网络（CNN），并结合 k 折交叉验证（k-Fold CV）。我们使用欧几里得距离进行距离计算，并在 kNN 算法的交叉验证中选择 k = 15，发现测试准确率约为 20%。我们还尝试了逻辑回归模型：先把图像反相为黑色背景，然后应用 L1 正则化并使用优化器 SAGA [4] 进行训练。我们得到的测试准确率低于 kNN。通过为逻辑回归添加 Bagging，我们让准确率略有提升。带最大池化的逻辑回归在我们使用的所有模型中测试准确率最低，而我们通过 CNN 获得的最高测试准确率约为 50%。

[![Student gallery 1 stroke counting](https://sebastianraschka.com/images/blog/2019/student-gallery-1/stroke-counting.webp)](https://github.com/yienxu/counting-strokes-in-chinese-characters/blob/master/Report.pdf)
