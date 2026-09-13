---
title: "机器学习与深度学习导论"
title_en: "Intro to ML and Deep Learning"
source: https://sebastianraschka.com/blog/2020/intro-to-dl-ch01.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 机器学习与深度学习导论

> 原文：[Intro to ML and Deep Learning](https://sebastianraschka.com/blog/2020/intro-to-dl-ch01.html)

*说明：本文由我在威斯康星大学麦迪逊分校（UW-Madison）教授深度学习课程时所制作的讲义幻灯片整理而成。幻灯片的较新版本可在此处获取：<https://github.com/rasbt/stat453-deep-learning-ss20>。今年初夏，我养成了一个写作习惯：每天早上 7 点左右醒来后写大约 25 分钟。本文就是到目前为止的成果。也许有一天，它会成为一本书。如果你正在读这篇文章，我非常期待你的反馈。但请不要太过苛刻，因为这只是一份未经任何编辑的初稿。（另：抱歉，我也不知道下一章什么时候能写好，可能要等很久。另外，我知道机器学习和深度学习的入门介绍早已汗牛充栋；不过，无论开课还是写书，不写导论我总觉得开不了头。）*

*希望这些内容对你有用 :)。*

## 第 1 章：机器学习与深度学习导论

> *"开始容易——坚持却难。"*
> ——日本谚语

第一章介绍机器学习的核心思想与概念，为后续章节更深入地探讨深度学习做好铺垫。首先，我们定义什么是机器学习，以及它与传统的自动化形式——即编程——之间的关系。接着，我们介绍机器学习的三大类别：监督学习、无监督学习和强化学习。最后，基于典型的预测建模流程，本章介绍深度学习领域乃至全书所使用的核心术语与记号。

### 1.1 什么是机器学习？

在深入聚焦深度学习领域之前，先介绍更宏观的机器学习概念会很有帮助——深度学习是机器学习的一个子领域，本章（1.1.2 节）将进一步说明这一点。不过，先别急着往前赶，让我们来探讨开发和使用机器学习的动机之一。

#### 1.1.1 传统编程范式的自动化

想象一下，我们刚刚完成了一款非常好用的邮件客户端。我们通过新增"稍后提醒"（snooze）邮件的功能，让我们自己（以及每位用户）的生活轻松了不少。然而，收件箱里仍然塞满了大量垃圾邮件。我们该如何实现一个垃圾邮件过滤器来改善这种状况呢？

不巧的是，定义识别垃圾邮件的规则对我们人类来说是件相当有挑战性的事[1](#fn:1)。如果我们无法给*垃圾邮件*下一个精确定义，又怎么能在邮件程序中设计并编写出一套规则呢？也许我们可以实现一些简单规则，例如，过滤主题栏全大写（"ALL CAPS"）的邮件。但把这种过滤器应用到真实收件箱之后，我们很可能会发现大量的漏报（false negative，即未被归为垃圾邮件的垃圾邮件）。于是，也许我们只能推倒重来，再补充一些新规则。

上一段勾勒了开发邮件客户端场景下的传统编程范式。它是开发某些功能的绝佳方式，但对另一些功能并不理想。例如，在实现垃圾邮件过滤器时，也许存在比凭直觉定义规则更高效的方法。除了单纯依赖直觉，我们还可以读取并分析数据集中成千上万甚至数百万封邮件，记录这些垃圾邮件有哪些共同点、又有哪些特征把它们与正常邮件区分开。尽管这在技术上可行，但听起来实在枯燥、艰巨且容易出错。一定有更好的办法，那就是使用机器学习。

![Intro to dl ch01 ml vs traditional](https://sebastianraschka.com/images/blog/2020/dl-intro-ch01/ml-vs-traditional.webp)
*图 1. 传统编程（A）与机器学习（B）的比较。*

图 1A 描述了传统编程范式：程序员开发出一套规则或程序，交给计算机执行，然后观察其输出。如果输出不尽如人意，程序员就回到程序中调整规则，希望改进结果（此处指被正确分类的邮件数量）。

与传统编程范式相反，机器学习是让计算机自己弄清这类复杂的输入-输出关系。如图 1B 所总结的，传统编程范式与机器学习的区别在于：后者是这样一种范式——我们向计算机算法提供要解决任务的示例，由它得出决策"程序"（*此处指*机器学习模型），并依据用户定义的目标来优化决策。

#### 1.1.2 机器学习、深度学习与人工智能之间的联系

人工智能（AI）作为计算机科学的一个子领域而兴起，其目标是编程让计算机解决人类擅长的问题（自然语言、语音、图像识别等）。据普遍说法，"AI"一词由 John McCarthy 在 1956 年举办的夏季研讨会——*达特茅斯人工智能夏季研究计划*（Dartmouth Summer Research Project on Artificial Intelligence）——上首次提出 [@emmertstreib2020clarification]。机器学习这个领域，最终正是源于设计 AI 的愿望而诞生的。

最早的机器学习算法（Rosenblatt 感知机，见第 3 章《感知机》）诞生于 20 世纪 50 年代 [@rosenblatt1958perceptron]，其灵感来自人脑神经元的早期数学模型 [@mcculloch1943logical]。在随后的几十年里，人们开发了具有多个神经元、多个层的神经网络，以及有效训练它们的算法 [@rumelhart1986learning]。至于多层神经网络为何在 2012 年前后以*深度学习*这一统称迎来复兴，其缘由将在第 2 章《神经网络与深度学习简史》中更详细地展开。

由于过去十年对深度学习方法的关注与日俱增，加上技术栈和算法技术的不断演进，不涉及深度神经网络[2](#fn:2)的机器学习分支如今常被称为*传统*机器学习或*常规*机器学习 [@raschka2020machine]。

正如上文所述，机器学习、AI 与深度学习三个领域之间联系紧密且相互重叠，如图 2 所示。AI 可以理解为开发能表现出类人智能形式的非生物系统的探索。早期颇有前景的途径包括符号模型与推理、早期版本的神经网络以及专家系统 [@emmertstreib2020clarification]。几经起伏之后，到了 20 世纪后期，机器学习（无论是否使用神经网络）脱颖而出，成为开发此类人工智能系统最有前景的方向之一。简而言之，机器学习就是教会机器或计算机如何从数据中学习，而无需人类手工编写特定规则。

![Intro to dl ch01 connection between fields](https://sebastianraschka.com/images/blog/2020/dl-intro-ch01/connection-between-fields.webp)
*图 2. 机器学习、深度学习与人工智能三个领域之间紧密的联系与重叠。*

机器学习固然可以用来开发 AI，但并非所有机器学习应用都称得上 AI。例如，如果有人实现了一棵决策树，依据年龄、收入和信用评分来决定某人是否应获得贷款，我们通常不会把它视为做出该决策的人工智能体（而只当作某种"简单规则"）。

不基于机器学习的 AI 途径包括符号表示或逻辑规则，它们可以通过观察人类专家执行特定任务来编写或编程实现。基于观察人类专家而开发的系统称为专家系统。这种符号主义 AI 路线如今有时被称为"好旧式人工智能"（Good Old-Fashioned Artificial Intelligence）[@haugeland1989artificial]。从编程的角度看，可以把这类专家系统想象成带有大量（深度嵌套的）条件语句（if/else 语句）的复杂计算机程序。

AI 还可以进一步分为通用人工智能（artificial general intelligence，AGI）和狭义人工智能（narrow AI）。AGI 致力于开发能在多种任务上模仿人类智能的多用途 AI；狭义 AI 则专注于解决单一、特定的任务（玩游戏、驾驶汽车等等）。2018 年，Martin Ford 出版了一本书，围绕"AGI 终将在何时出现"这一主题，收录了对多位顶尖人工智能研究者的访谈 [@ford2018architects]。供有兴趣的读者参考：这 18 位受访者的猜测介于 2018 年之后的 11 年（2029 年）到 182 年（2200 年）之间，平均预测是 2018 年之后的 81 年，即 2099 年。

总而言之，经典 AI 可以描述为在一个或多个任务上表现出类人智能形式的非生物系统；机器学习则是一个关注开发能自动从数据中学习模型、表示与规则的算法的领域。

### 1.2 机器学习的类别

本节介绍并总结机器学习的三个经典类别：监督学习、无监督学习和强化学习。除了这三大类别之外，本节还将介绍监督学习的两个主要子类别：半监督学习——可以视为监督学习与无监督学习的混合——以及自监督学习。

如 1.1.2 节所述，深度学习是机器学习的一个子类别，专注于参数化多层神经网络，使其能够通过多层抽象学习数据的表示。在本书中，我们将用*机器学习*一词同时指代传统机器学习和深度学习。

监督学习专注于预测建模任务，即对从数据中提取的特征与一个或多个目标变量（或标签）之间的关系建模。监督学习基于带标签的数据，而无监督学习旨在在没有标签信息的情况下对数据中的隐藏结构建模。最后，强化学习关注的是开发奖励系统，以对复杂决策过程建模并学习一系列动作。

#### 1.2.1 监督学习

监督学习关注的是在给定输入观测的情况下预测目标值。在机器学习中，我们把模型输入称为"特征"[3](#fn:3)。监督模型被训练来预测的目标值也常被称为*标签*[4](#fn:4)。监督学习可以分为两大子类别：回归分析和分类。在回归分析中，目标值或标签是连续变量（图 3A）；在分类中，标签是所谓的*类别标签*（class labels），可以理解为离散的类别或群体归属指示（图 3B）。

![Intro to dl ch01 regression and classification](https://sebastianraschka.com/images/blog/2020/dl-intro-ch01/regression-and-classification.webp)
*图 3. 监督学习两大主要类别的示意：回归（A）与分类（B）。*

在机器学习中，我们经常处理高维数据集，即由大量输入特征组成的数据集。然而，受人类想象力和书面载体的限制，常规插图只能描绘两个（至多三个）空间维度。图 3 中的二维散点图展示了两个简单的数据集。其中子图 A 描绘了一个只含单一特征的数据集上的简单回归示例；目标变量，也就是我们想预测的值，被绘制在 y 轴上。子图 B 描绘了一个二维分类数据集，其目标变量——离散的类别标签信息——被编码为符号（三角形与圆形）。在这两种情况下，都存在一个模型要学习预测的目标变量。在线性回归示例中，目标变量是图 3A 中绘制在 y 轴上的连续变量；而在图 3B 的分类示例中，目标变量由以符号（三角形和圆形）表示的类别标签构成。

监督学习的第三个类别是*序数回归*（ordinal regression），有时也称为*序数分类*（ordinal classification）。序数回归可以理解为前面提到的（度量）回归分析与分类这两者的混合体。在序数回归中，和分类一样存在若干类别，但类别之间带有顺序信息。与度量回归不同，其标签是离散的，且标签之间的距离是任意的。例如，预测一个人的身高属于度量回归：目标变量（身高）可以在连续尺度上度量，150 cm 与 160 cm 之间的距离等于 180 cm 与 190 cm 之间的距离。而预测 1-5 分制的电影评分则更适合用序数回归模型。假设电影评分尺度定义如下：1=差、2=一般、3=好、4=很好、5=极佳。此时，1（差）与 2（一般）之间的距离是任意的；换句话说，我们无法直接把 1（差）到 2（一般）的差距与 3（好）到 4（很好）的差距进行比较。与序数回归相关的一个任务是排序（ranking）。但请注意，在排序任务中，我们只关心项目的*相对*顺序，例如把一组电影从最差排到最好；而在序数回归中，我们关心的是给定尺度上的绝对取值。对序数回归的详细讨论超出了本书的范围，对该主题感兴趣的读者可以参考论文《Rank-consistent Ordinal Regression for Neural Networks》[@cao2019rank]，其中引用了与深度学习相关的序数回归文献。

#### 1.2.2 无监督学习

上一节介绍了监督学习——机器学习中最突出的子类别。本节讨论机器学习的第二大类别：无监督学习。与监督学习不同，无监督学习没有给定标签信息，其目标是发现或对数据中的隐藏结构建模，而不是预测连续或离散的目标标签。

无监督学习的一个主要子类别是表示学习与降维。这方面一种流行且经典的技术是主成分分析（principal component analysis，PCA；图 4）。

![Intro to dl ch01 pca](https://sebastianraschka.com/images/blog/2020/dl-intro-ch01/pca.webp)
*图 4. PCA 示意。(A) 一个具有两条特征轴 \(x\_1\) 和 \(x\_2\) 的数据集（蓝色圆点）被投影到主成分 \(PC1\) 和 \(PC2\) 上 (B) 数据投影到第一主成分（PC1）后的视图。*

简而言之，PCA 识别数据集中方差最大的方向。这些方向（协方差矩阵的特征向量）构成新坐标系的主成分轴。实践中，PCA 通常用于在保留数据大部分信息（方差）的同时降低数据集的维度。PCA 是一种线性变换技术，因此无法捕捉数据中复杂的非线性模式；不过，还有核 PCA（kernel PCA）以及其他非线性降维技术。第 15 章将介绍自编码器（autoencoder），它是一种可用于非线性降维的深度神经网络架构。如图 5 所示，自编码器由两个子网络组成：编码器（encoder）和解码器（decoder）。输入（例如一张图像）被送入编码器，编码器把输入压缩成一个低维表示，也称为"嵌入向量"（embedding vector）或"潜在表示"（latent representation）。编码器把特征嵌入到这个低维空间之后，解码器再从这个潜在表示重建原始图像。编码器与解码器这两个子网络端到端相连，通常被画成一个沙漏的形状，沙漏的宽度表示多层神经网络所产生的特征图的大小。

![Intro to dl ch01 autoencoder](https://sebastianraschka.com/images/blog/2020/dl-intro-ch01/autoencoder.webp)
*图 5. 自编码器示意。*

在典型的自编码器架构中，编码器的输出是网络中最小的特征图，随后被送入解码器——编码器与解码器之间的这一连接也常被称为"瓶颈"（bottleneck）。自编码器思想的内在逻辑是：要让解码器对原始输入图像做出忠实的重建，编码器必须学会构造一个保留大部分信息的潜在表示。通常，自编码器架构被设计成潜在表示的维度低于输入（及其重建结果），这样自编码器就无法只是把原始输入原样记住并传递过整个架构——这一点有时也被称为信息瓶颈（information bottleneck）。

无监督学习的另一个主要子类别是聚类（clustering），即为数据点赋予群体归属信息。可以把它想象成一个与分类相似、但训练数据集中没有标签信息的任务。因此，在缺少类别标签信息的情况下，聚类的做法是依据相似性对数据记录分组，并基于相似性阈值定义不同的群组。

聚类可以分为三大类：基于原型的聚类、基于密度的聚类和层次聚类。在基于原型的聚类算法（如 K-Means [@macqueen1967some; @lloyd1982least]）中，会定义固定数量的聚类中心（聚类中心会被迭代地重新定位），并根据成对距离度量（例如欧氏距离）把数据点分配给最近的原型。在基于密度的聚类中，与基于原型的聚类不同，聚类中心的数量并不固定，而是通过识别高密度区域（即按用户定义的距离度量彼此接近的众多数据记录所在的位置）来确定。在层次聚类中，使用距离度量以树状结构对样本进行分组，越靠近树根的样本彼此关联越紧密，树的深度决定了聚类的数量。

![Intro to dl ch01 clustering](https://sebastianraschka.com/images/blog/2020/dl-intro-ch01/clustering.webp)
*图 5. 聚类示意。(A) 一个二维无标签数据集。(B) 由聚类算法推断出的簇，该算法把相似的点归入同一个簇。*

#### 1.2.3 强化学习

机器学习的第三个、也可能是最具挑战性的子类别是强化学习（图 6）。监督学习专注于预测特定的结果，而强化学习关注的是学习能带来特定结果的*一系列动作*。结合图 6 来说明强化学习：(1) 在第 \(t\) 轮迭代中，给定棋盘状态 \(S\_t\) 和某个奖励值 \(R\_t\)，(2) 强化学习智能体选择一个动作 \(A\_t\)，把一枚棋子移动两格。(3) 接下来，环境根据 \(A\_t\) 产生下一个状态 \(S\_{t+1}\) 以及执行该动作所对应的奖励 \(R\_{t+1}\)。这一循环不断重复，直到本局（episode）结束。

![Intro to dl ch01 rl diagram](https://sebastianraschka.com/images/blog/2020/dl-intro-ch01/rl-diagram.webp)
*图 6. 以国际象棋棋盘为例说明强化学习。*

#### 1.2.4 半监督学习

半监督[5](#fn:5)学习是介于监督学习与无监督学习之间的一个类别混合。半监督学习指的是一部分训练样本有标签、另一部分没有标签的场景。半监督学习背后的主要思想是：利用数据集中有标签的部分（通过监督学习）来为无标签的部分打标签，然后再将后者用于监督学习。在这里，使用无标签样本可以提升泛化性能，因为训练时可用的数据更多了。

![Intro to dl ch01 semi supervised](https://sebastianraschka.com/images/blog/2020/dl-intro-ch01/semi-supervised.webp)
*图 7. 利用无标签样本的半监督学习示意。(A) 仅由有标签训练样本得到的决策边界。(B) 基于有标签与无标签样本得到的决策边界。*

#### 1.2.5 自监督学习

为大型数据集收集标签可能贵得令人望而却步。自监督学习旨在利用大量无标签数据来做监督学习。由于它能够把自然可得的信息用作监督学习的标签，自监督学习有时也被称为*自主*（autonomous）监督学习。监督学习与自监督学习密切相关，因为二者都是从带标签的输入-输出对中学习从输入（例如图像）到输出（例如类别标签）的映射。自监督学习与常规监督学习的区别在于：前者的标签是自动生成的，或者天然蕴含在数据之中。

借助自监督学习，我们可以先在与目标任务相关的任务上（预）训练模型（用于目标任务的监督学习），然后再在目标任务上训练，从而利用更多的数据。这个相关任务也常被称为"代理任务"（pretext task）。对图像分类而言，常见的代理任务包括：预测图像被旋转了多少度 [@gidaris2018unsupervised]、给图像的灰度版本上色 [@zhang2016colorful]、把被切分成子区域的图像重新拼合（有点像拼图游戏）[@noroozi2016unsupervised]，以及预测随机图像块（patch）的上下文位置 [@doersch2015unsupervised]（图 8）。

实践中，当目标任务对应的有标签数据集相对较小，或者模型能从更多数据中受益时，常常会使用自监督学习。在这种场景下，可以利用一个与目标任务数据类型相似（例如分辨率相同的图像）的规模更大的无标签数据集，按照上一段所述为代理任务构造标签。在代理任务标签上对模型（通常是神经网络）进行预训练之后，再在目标任务数据集上训练。实践中，先在代理任务上预训练模型，往往能比仅在目标任务数据集上训练获得更好的模型性能。

![Intro to dl ch01 cat self supervised](https://sebastianraschka.com/images/blog/2020/dl-intro-ch01/cat-self-supervised.webp)
*图 8. 通过上下文预测进行自监督学习。(A) 随机采样一个图像块（红色方块），并取其 9 个相邻图像块。(B) 给定随机图像块和一个随机相邻块，任务是预测相邻块相对于中心块（红色方块）的位置。*

### 1.3 机器学习术语与记号

机器学习与深度学习研究具有很强的跨学科性。研究者所属的院系或主要专业领域不同（统计学、计算机科学、电气工程，以及许多其他领域），所用术语也主要取决于其教育背景。不过，多年来，机器学习会议与出版渠道已经收敛出一套领域专属的术语、行话和记号，它们在各个子领域中被采纳得越来越广。

#### 1.3.1 预测建模流程

监督学习在很大程度上专注于开发预测模型，即训练分类器或回归模型来预测新观测的目标信息（例如类别标签）。图 9 中的流程图总结了一个典型的预测建模工作流，该流程图某些环节的细节将在后面几小节中进一步展开。

![Intro to dl ch01 pipeline1](https://sebastianraschka.com/images/blog/2020/dl-intro-ch01/pipeline1.webp)
*图 9. 监督学习与预测建模流程示意。*

简要地说，图 9 所描绘的监督学习工作流可以分为两个主要步骤：(1) 模型训练和 (2) 推断。训练阶段涉及一个带标签的训练数据集和一个机器学习或深度学习算法。学习算法学习如何把训练数据集中的观测（也称为特征）——例如花卉图像——与标签信息（例如花卉物种的名称）关联起来。具体而言，学习算法会利用训练数据集来构建或参数化一个预测模型，随后就可以用这个模型对新观测做出预测。

注意，某些学习算法直接在所谓"原始特征"上工作，而另一些类别的学习算法则在预处理或提取后的特征上运行，下一小节（1.3.2 节）将更详细地讨论这一点。

如今，在深度学习研究者和从业者中，用模型预测新观测的目标信息也被称为"推断"（inference）[6](#fn:6)。实践中，在把模型投入真实世界应用之前，我们通常还会加入一个模型评估步骤。这与图 9 中展示的"推断"阶段类似，但新观测来自一个独立测试数据集，并且我们知道其中待预测目标的真实标签。这一基本的模型评估过程如图 10 所示：我们把模型应用于新观测（来自测试数据集的数据记录），然后把预测标签与测试数据集中的实际标签进行比较，并计算评估指标，例如预测误差或准确率。注意，模型评估本身就是一个内涵很广的主题，超出了本书的范围。不过，如果你有兴趣深入了解，我推荐免费可得的论文《Model Evaluation, Model Selection, and Algorithm Selection in Machine Learning》[@raschka2018model]。

![Intro to dl ch01 pipeline2](https://sebastianraschka.com/images/blog/2020/dl-intro-ch01/pipeline2.webp)
*图 10. 使用测试数据集评估预测模型的性能。*

#### 1.3.2 数据表示

在比较传统机器学习与深度学习所用的特征表示时，理解*结构化*（structured）与*非结构化*（unstructured）数据的概念会很有帮助（图 11）。

简单来说，结构化数据可以理解为表格数据。结构化数据的一个特点是，它通常已经过预处理，包括特征提取。例如，结构化数据一般以数据库条目、电子表格或 CSV 文件的形式存储。在机器学习中，常见的做法是把结构化数据格式化为：表格数据集的每一行代表一个数据实例或记录（例如一个训练样本），每一列代表一个观测到的或提取出的特征。在统计学中，这种数据表示形式也常被称为*设计矩阵*（design matrix）。图 11 展示了一个结构化数据集的例子，其中包含鸢尾花叶片的测量值（花萼长度、花萼宽度、花瓣长度和花瓣宽度）。这里，第一列只是数据集索引；第 2-5 列是花的测量值（特征），构成数据集的设计矩阵部分；最后一列包含与每朵花（训练样本）相关联的类别标签（此处为花的物种：Iris-setosa、Iris-versicolor 和 Iris-virginica）。在监督学习场景下，我们可以训练一个分类器，从特征（第 2-5 列）预测类别标签（最后一列）。

非结构化数据则指更接近其*原始*形态的数据——即数据被采集时的形态。例如，就上一段的鸢尾花例子而言，非结构化数据格式就是与图 11A 结构化数据表中所列花朵相对应的一组图像。由此很容易看出，如何从一条非结构化数据记录（图 11B）中提取特征，来构造一条结构化数据记录（图 11A 中的一行）。

传统机器学习是为处理结构化数据而设计的，而深度学习从设计之初就面向非结构化数据。本书稍后介绍的卷积神经网络和循环神经网络等大多数深度学习架构，都是为处理图像和文本数据而设计的。作为学习过程的一部分，深度神经网络会学习对原始（非结构化）数据进行提取和变换，使其有利于预测建模（在监督学习场景中）。因此，深度学习也常被描述为*表示学习*（representation learning）。

![Intro to dl ch01 iris](https://sebastianraschka.com/images/blog/2020/dl-intro-ch01/iris.webp)
*图 11. 结构化数据与非结构化数据。(A) 一个用于监督学习的结构化表格数据集，其中每一行代表一个训练样本（此处为鸢尾花），带有四个测量值和一个类别标签（鸢尾花的物种）。(B) 一张鸢尾花照片（非结构化数据）。这类照片可以处理成 (A) 所示的结构化数据集。*

#### 1.3.3 监督学习的数学表述

回顾 1.2.1 节，我们介绍了机器学习中最大的子类别——监督学习。更正式地，我们把监督学习描述为学习一个函数[7](#fn:7)，它把输入空间 \(X\) 映射到某个输出空间 \(Y\)：

\[h: X \rightarrow Y.\]

给定 \(n\) 个带标签的训练样本 \(\mathcal{D} = \left\{\left(\mathbf{x}^{[1]}, y^{[1]}\right), \ldots,\left(\mathbf{x}^{[n]}, y^{[n]}\right)\right\}\)，每个训练样本 \(\left(\mathbf{x}^{[i]}, y^{[i]}\right)\) 都是输入 \(\mathbf{x}^{[i]}\) 与标签 \(y^{[i]}\)（例如分类中的类别标签）组成的一对。输入 \(\mathbf{x}\_{j}^{[i]\) 常被称为*特征*；由于 \(\mathbf{x}^{[i]}\) 表示一个向量（在大多数传统机器学习概念中），我们通常把给定训练样本的输入称为特征*向量*：

\[\mathbf{x}=\left[\begin{array}{c}
x\_{1} \\
x\_{2} \\
\vdots \\
x\_{m}
\end{array}\right].\]

有了 \(n\) 个训练样本各自的特征向量，我们就可以把数据集（由 \(m\) 个特征和 \(n\) 个训练样本组成）表示为一个设计矩阵，

\[\mathbf{X}=\left[\begin{array}{c}
\mathbf{x}\_{1}^{\top} \\
\mathbf{x}\_{2}^{\top} \\
\vdots \\
\mathbf{x}\_{n}^{\top}
\end{array}\right] = \left[\begin{array}{cccc}
x\_{1}^{[1]} & x\_{2}^{[1]} & \cdots & x\_{m}^{[1]} \\
x\_{1}^{[2]} & x\_{2}^{[2]} & \cdots & x\_{m}^{[2]} \\
\vdots & \vdots & \ddots & \vdots \\
x\_{1}^{[n]} & x\_{2}^{[n]} & \cdots & x\_{m}^{[n]}
\end{array}\right].\]

而在深度学习场景中，我们经常处理图像数据，此时的特征（图像）是更高阶的张量。这一点将在第 4 章《深度学习的线性代数》和第 12 章《卷积神经网络导论》中更详细地讨论。

#### 1.3.4 损失函数

假设存在某个未知的标签生成函数 \(f\)，它在第 \(i\) 个训练样本中把标签 \(y\) 与特征 \(\mathbf{x}\) 关联起来，那么监督学习的目标就是学习一个函数 \(h\)，它能为无标签数据点 \(\mathbf{x}\) 产生输出或预测 \(\hat{y}\)，

\[h(\mathbf{x}) = \hat{y}\]

并使预测性能达到最优。在统计学习理论中，我们把它表述为最小化风险 \(R\)，风险定义为损失 \(L\) 的期望，

\[R(h)=E[L(h(x), y)]=\int L(h(x), y) d P(x, y).\]

在监督学习中，目标是对模型进行参数化（即找到 \(h\)）以最小化风险。由于实践中我们并不知道联合概率分布 \(P(x, y)\)，我们转而对给定数据集中的全部 \(n\) 个样本做经验风险最小化：

\[R\_{\mathrm{emp}}(h)=\frac{1}{n} \sum\_{i=1}^{n} L\left(h\left(x\_{i}\right), y\_{i}\right).\]

在机器学习文献中，更常见的做法是把经验风险 \(R\_{\mathrm{emp}}\)——即损失在训练数据集上的总和（越低越好）——称为*代价函数*（cost function）。传统上，*损失*（loss）是针对单条数据记录比较预测标签与真实标签的函数。例如，在分类中，我们可以把 0-1 损失定义如下：

\[L(\hat{y}, y)\_{\text{0-1}}=\delta(\hat{y} \neq y),\]

其中 \(\delta\) 是克罗内克 δ 函数（Kronecker delta function）

\[\delta({i \neq j}) \equiv\left\{\begin{array}{ll}
0 & \text{ for } i \neq j, \\
1 & \text{ for } i=j.
\end{array}\right.\]

在回归中，常见的做法是定义平方误差损失，

\[L\_{\text{SE}}(\hat{y}, y)=(\hat{y} - y)^2.\]

相应地，在整个数据集上测得的均方误差（MSE）在此情况下就是*代价*函数：

\[\text{MSE}(h)=\frac{1}{n} \sum\_{i=1}^{n} L\_{\text{SE}}\left(h\left(x\_{i}\right), y\_{i}\right).\]

注意，机器学习文献中曾有区分损失函数（针对单条数据记录）与代价函数（应用于整个数据集的损失函数）的惯例。深度学习文献在很大程度上放弃了这一区分，或者把 loss 和 cost 这两个词混用。不过，在本书中，我们将区分代价函数与损失函数，因为这样做能增强表述的清晰度，避免不必要的歧义。

最后要指出，在深度学习实践中，通常无法直接优化 0-1 损失，因此我们需要借助替代函数（surrogate function）来进行优化。例如，类别交叉熵（categorical cross entropy）就可以作为最小化预测误差（训练集上的 0-1 损失）的替代指标。这一点将在第 5 章《用梯度下降拟合神经元》中更详细地讨论。概括地说，需要记住的重点是：存在 (1) 优化性能度量和 (2) 评估度量——(1) 和 (2) 可以相同，但往往不同（尽管彼此相关）。最终目标是让评估度量或指标上的表现良好（例如分类错误率低或分类准确率高），而这与优化优化度量（例如类别交叉熵）高度相关。

#### 1.3.5 机器学习行话小词典

机器学习已经成为一个高度跨学科的领域。来自计算机科学、统计学、神经科学、数学以及其他诸多学科的研究者和从业者都在开发、塑造并为这个领域做出贡献。因此，由于研究者和从业者的背景不同，相似的概念可能用不同的术语来指代。本小节简要概述最常见的机器学习与深度学习术语，以及它们在其他领域中的同义说法：

- **训练样本**（training example）。与 observation（观测）、training record（训练记录）、training instance（训练实例）、training sample（训练样本）同义（在某些语境中，sample 指一组训练样本的集合）。
- **特征**（feature）。与 predictor（预测变量）、variable（变量）、independent variable（自变量）、input（输入）、attribute（属性）、covariate（协变量）同义。
- **目标**（target）。与 outcome（结果）、ground truth（真值）、desired output（期望输出）、response variable（响应变量）、dependent variable（因变量）、label（标签）、class label（类别标签，分类语境下）同义。
- **输出**（output）。与模型输出或预测同义；这里的输出指模型的返回值，将与目标进行比对。

### 1.4 本章小结

本章介绍了机器学习的核心思想（或者说愿景），并厘清了机器学习、深度学习与人工智能之间的关系。总而言之，要点是：深度学习是机器学习的一个子领域，而人工智能与机器学习并非同义词。此外，本章介绍了机器学习的三大类别，即处理带标签数据（监督学习）、处理无标签数据（无监督学习）以及学习复杂过程（强化学习）。最后，围绕深度学习存在大量领域专属的行话；许多技术术语来自其他领域，但请注意，那些看起来熟悉的术语在深度学习的语境下可能另有所指。

下一章将深入探讨深度学习的历史，介绍开发人工神经元与神经网络背后更宏观的思想脉络。下一章旨在自顶向下地给出深度学习的概貌，随后我们再自底向上地对它进行剖析。

感谢阅读。如果你喜欢这些内容，也可以[在 Twitter 上找到我](https://twitter.com/rasbt)，我在那里分享更多有用的内容。

### 1.5 References

@cao2019rank: Cao, W., Mirjalili, V., & Raschka, S. (2019). [Rank-consistent ordinal regression for neural networks](https://arxiv.org/abs/1901.07884). arXiv:1901.07884.

@doersch2015unsupervised: Doersch, C., Gupta, A., & Efros, A. A. (2015). [Unsupervised visual representation learning by context prediction](https://www.cv-foundation.org/openaccess/content_iccv_2015/papers/Doersch_Unsupervised_Visual_Representation_ICCV_2015_paper.pdf). In Proceedings of the IEEE International Conference on Computer Vision (pp. 1422-1430).

@emmertstreib2020clarification: Emmert-Streib, F., Yli-Harja, O., & Dehmer, M. (2020). [A clarification of misconceptions, myths and desired status of artificial intelligence](https://arxiv.org/abs/2008.05607). arXiv:2008.05607.

@ford2018architects: Ford, M. (2018). [Architects of Intelligence: The truth about AI from the people building it](https://www.packtpub.com/product/architects-of-intelligence/9781789954531). Packt Publishing Ltd.

@gidaris2018unsupervised: Gidaris, S., Singh, P., & Komodakis, N. (2018, April). [Unsupervised representation learning by predicting image rotations](https://arxiv.org/pdf/1803.07728.pdf). In ICLR 2018.

@haugeland1989artificial: Haugeland, J. (1989). [Artificial intelligence: The very idea](https://mitpress.mit.edu/books/artificial-intelligence-1). MIT Press.

@lloyd1982least: Lloyd, S. (1982). [Least squares quantization in PCM](https://ieeexplore.ieee.org/document/1056489). IEEE Transactions on Information Theory, 28(2), 129-137.

@macqueen1967some: MacQueen, J. (1967, June). [Some methods for classification and analysis of multivariate observations](https://projecteuclid.org/euclid.bsmsp/1200512992). In Proceedings of the fifth Berkeley symposium on mathematical statistics and probability (Vol. 1, No. 14, pp. 281-297).

@mcculloch1943logical: McCulloch, W. S., & Pitts, W. (1943). [A logical calculus of the ideas immanent in nervous activity](https://link.springer.com/article/10.1007/BF02478259). The Bulletin of Mathematical Biophysics, 5(4), 115-133.

@noroozi2016unsupervised: Noroozi, M., & Favaro, P. (2016, October). [Unsupervised learning of visual representations by solving jigsaw puzzles](https://link.springer.com/chapter/10.1007/978-3-319-46466-4_5). In European Conference on Computer Vision (pp. 69-84). Springer, Cham.

@raschka2018model: Sebastian Raschka (2018). [Model Evaluation, model selection, and algorithm selection in machine learning](https://arxiv.org/abs/1811.12808). arXiv:1811.12808

@raschka2020machine: Raschka, S., Patterson, J., & Nolet, C. (2020). [Machine Learning in Python: Main developments and technology trends in data science, machine learning, and artificial intelligence](https://www.mdpi.com/2078-2489/11/4/193). Information, 11(4), 193.

@rosenblatt1958perceptron: Rosenblatt, F. (1958). [The perceptron: a probabilistic model for information storage and organization in the brain](https://pubmed.ncbi.nlm.nih.gov/13602029/). Psychological Review, 65(6), 386.

@rumelhart1986learning: Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986). [Learning representations by back-propagating errors](https://www.nature.com/articles/323533a0). Nature, 323(6088), 533-536.

@zhang2016colorful: Zhang, R., Isola, P., & Efros, A. A. (2016, October). [Colorful image colorization](https://arxiv.org/abs/1603.08511). In European Conference on Computer Vision (pp. 649-666). Springer, Cham.

### 1.6 致谢

感谢 Andrea Panizza 对手稿提出的有益反馈。

### 1.7 脚注

*本博文是从 LaTeX 文档导出的，格式和脚注处理较为笨拙，敬请见谅。*

1. 如果你不同意，可以试着回答"什么才算垃圾邮件？"这个问题，并把你的标准应用到自己的收件箱和垃圾邮件文件夹上。[↩](#fnref:1)
2. 这包括最近邻算法、广义线性模型、支持向量机、决策树、随机森林等等。[↩](#fnref:2)
3. 特征相当于统计学中的 predictor variables（预测变量）、independent variables（自变量）或 covariates（协变量）。[↩](#fnref:3)
4. 在统计学中，这对应自变量（independent variable）或结果（outcome）。[↩](#fnref:4)
5. 前缀 *semi-* 源自拉丁语，意为"一半"。[↩](#fnref:5)
6. 深度学习中"inference"一词的用法不要与它在统计学中的含义相混淆——在统计学中，它指基于样本统计量推断总体信息的过程。[↩](#fnref:6)
7. 具体用什么符号并不重要，但在机器学习中，字母 \(h\) 常用来指代模型或分类器。在这种语境下，\(h\) 是 *hypothesis*（假设）的缩写。就分类模型而言，假设是一个预测类别标签的函数，它近似地刻画了决定一组观测（特征）所对应类别标签的那个真实的底层函数或现象。[↩](#fnref:7)
