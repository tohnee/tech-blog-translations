---
title: "用认知心理学解读深度神经网络"
title_en: "Interpreting Deep Neural Networks using Cognitive Psychology"
source: https://deepmind.google/blog/interpreting-deep-neural-networks-using-cognitive-psychology/
site: deepmind
date: 2017-06-27
crawled: 2026-09-13
translated: 2026-09-13
---

# 用认知心理学解读深度神经网络

> 原文：[Interpreting Deep Neural Networks using Cognitive Psychology](https://deepmind.google/blog/interpreting-deep-neural-networks-using-cognitive-psychology/) · Google DeepMind

深度神经网络已经学会了完成一连串惊人的任务——从识别图像中的物体并对其进行推理，到以超人类水平玩雅达利游戏和围棋。随着这些任务和网络架构日益复杂，神经网络学到的解也变得越来越难以理解。

这就是所谓的「黑箱」问题，而且随着神经网络被用于越来越多的现实世界应用，它正变得愈发重要。

在 DeepMind，我们正努力扩展理解和解读这些系统的工具箱。在[最新论文](https://arxiv.org/abs/1706.08606)（最近被 ICML 接收）中，我们针对这一问题提出了一种新方法，运用认知心理学的手段来理解深度神经网络。认知心理学通过测量行为来推断认知机制，并且拥有大量详细记录这类机制及其验证实验的文献。随着我们的神经网络在特定任务上的表现日益接近人类水平，认知心理学的方法与黑箱问题的相关性也与日俱增。

![神经网络「黑箱」问题的抽象表现：一个深色金属质感的魔方状结构，内部露出一段发光的橙色和红色透明方块。](https://lh3.googleusercontent.com/AIqMoPoJo_lxnZrJD70ykBIMMH7ANHb1z13jvfEIFFtDiktfFlyjnU1Zc2hbobU0HgTd1QPB2mKmXs0IxhX0d9iFIyS98yrXFcFSVv57ymDQOhAm9Q=w1440)

「黑箱」图片来源：Shutterstock

为了证明这一点，我们的论文报告了一个案例研究：我们用一个本为阐明人类认知而设计的实验，来帮助我们理解深度网络是如何解决图像分类任务的。

我们的结果表明，认知心理学家在人类身上观察到的行为，这些深度网络同样会表现出来。此外，结果还揭示了这些网络如何解决分类任务的有用而出人意料的洞见。更广泛地说，这一案例研究的成功展示了利用认知心理学来理解深度学习系统的潜力。

## 测量单样本词语学习模型中的形状偏置

在我们的案例研究中，我们考察了儿童如何识别物体并为它们贴上标签——这是发展认知心理学中一个内容丰富的研究领域。儿童能够从单个例子中猜出词语的含义——即所谓「单样本词语学习」（one-shot word learning）——进行得如此轻松，以至于人们容易以为这是一个简单的过程。然而，哲学家 Willard Van Orman Quine 的一个经典思想实验说明了这实际上有多么复杂：

一位实地语言学家去走访一个语言与我们完全不同的文化。这位语言学家正试图从一位乐于助人的本地人那里学习一些词语，这时一只兔子窜过。本地人喊了一声「gavagai」，语言学家随后需要推断这个新词的含义。他面临着大量可能的推断，包括「gavagai」指兔子、动物、白色的东西、那只特定的兔子，或者「兔子的未分离部分」。可能的推断是无穷无尽的。人们是如何选出正确的那一个的？

![一只白兔坐在绿色草地上的特写照片。](https://lh3.googleusercontent.com/2rEOxUHbUpT5eQUbEozEdN33I93E-8wEhsutZYu5Hw03uI5y5TffbVr66N9DLtZBxl5eOPtaMe1qGpHXd18T5DayfT-IL_9vOBQ9asuOU6MXuE9fRg=w1440)

「Gavagai」图片来源：「Misha Shiyanov/Shutterstock」

五十年后，我们面对着关于能够进行单样本学习的深度神经网络的同一个问题。以[匹配网络（Matching Network）](https://deepmind.com/research/publications/matching-networks-one-shot-learning/)为例——这是我们在 DeepMind 的同事开发的一种神经网络。该模型利用注意力与记忆方面的最新进展，在仅使用某一类别单个样本的情况下对 ImageNet 图像进行分类，取得了最先进的性能。然而，我们并不知道该网络在分类这些图像时做出了哪些假设。

为了弄清这一点，我们求助于发展心理学家的研究（1-4），他们发现证据表明，儿童通过应用归纳偏置来排除大量错误推断，从而找到正确的推断。这类偏置包括：

- **整体对象偏置（whole object bias）**：儿童假定一个词指代整个物体，而不是物体的组成部分（从而消除了 Quine 关于兔子未分离部分的担忧）
- **分类学偏置（taxonomic bias）**：儿童假定一个词指代物体所属的基础类别（从而平息了 Quine 的恐惧，即所有动物都可能被选作「兔子」的含义）
- **形状偏置（shape bias）**：儿童假定名词的含义基于物体形状，而非颜色或质地（从而缓解了 Quine 的焦虑，即所有白色的东西都可能被当作「兔子」的含义）

我们选择测量神经网络的形状偏置，是因为针对这一偏置在人类身上的研究，已有特别丰富的文献。

![最左侧是一个近似 U 形、边缘呈直角的物体，作为我们的探针图像。AI 的任务是把这一物体与一个形状相同的蓝色物体，或一个颜色相同但形状不同的物体进行匹配。](https://lh3.googleusercontent.com/XbF3phYxzcPPkfwMAawz7HiEmi_CTHf9uXJ5q-RouK9JJUo_dJ2RqyyPo6U-a32RXjo7cw8mgeDXTdPIFaKkMFVo7SJE4iMKcY_7_EWU80LRip3L=w1440)

我们用来测量深度网络形状偏置的刺激物示例。这些图像由印第安纳大学认知发展实验室（Cognitive Development Lab）的 Linda Smith 慷慨提供。

我们采用的经典形状偏置实验流程如下：向深度网络展示三个物体的图像——一个探针物体、一个形状匹配物体（与探针形状相似但颜色不同）和一个颜色匹配物体（与探针颜色相似但形状不同）。然后，我们测量形状偏置：即探针图像被赋予与形状匹配图像相同标签（而非颜色匹配图像标签）的比例。

我们使用的物体图像与人类实验中所用的相同，来自印第安纳大学认知发展实验室。

![一幅形状偏置实验示意图：一个匹配网络把一个黄色 U 形「探针」物体归类为类别「A」（匹配蓝橙条纹的 U 形物体），而不是类别「B」（匹配黄色立方体形物体）。](https://lh3.googleusercontent.com/3QtYU-8m9hZSceHSEgLi2Ogpzo12oVUIGpLA6slqPPY1jWtMO513Iq-grnHTq00mFS8w9feM2HKcOsnxhLQWO4IX1oDSabUpsGvZMNykFNmAMk83ng=w1440)

我们用匹配网络进行的认知心理学实验示意图。匹配网络把探针图像（左）与图像「A」（上中）或图像「B」（右上）匹配。输出结果（右下）取决于匹配网络中形状偏置的强度。

我们用深度网络（匹配网络和一个 Inception 基线模型）尝试了这一实验，发现——与人类一样——我们的网络对物体形状有强烈的偏置，而不是对颜色或质地。换句话说，它们拥有「形状偏置」。

这表明匹配网络和 Inception 分类器使用针对形状的归纳偏置来排除错误假设，让我们清楚地看到这些网络是如何解决单样本词语学习问题的。

对形状偏置的观察并不是我们唯一有趣的发现：

- 我们观察到，形状偏置在我们的网络中是随着早期训练进程逐渐浮现的。这让人联想到人类身上形状偏置的浮现：幼儿的形状偏置比大龄儿童弱，而成年人的偏置最强（2）。
- 我们发现，取决于初始化与训练所用的随机种子，网络中的偏置水平有所不同。这教会我们：在对深度学习系统做实验时，必须使用大样本的训练模型才能得出有效结论，正如心理学家早已明白不能依据单个被试就下结论一样。
- 我们发现，即使形状偏置差异很大，网络也能取得相同的单样本学习性能，这表明不同的网络可以为同一个复杂问题找到多种同样有效的解。

在标准神经网络架构中发现这种此前未被注意的偏置，展示了利用人工认知心理学来解读神经网络解的潜力。在其他领域，情景记忆文献中的洞见可能有助于理解情景记忆架构，语义认知文献中的技术可能有助于理解近期的概念形成模型。心理学文献在这些领域及其他领域都非常丰富，为我们解决「黑箱」问题、更深入地理解神经网络的行为，提供了强大的新工具。

**附注**

本工作由 Sam Ritter\*、David G.T. Barrett\*、Adam Santoro 和 Matt M. Botvinick 完成。

阅读 [Cognitive Psychology for Deep Neural Networks: A Shape Bias Case Study](https://arxiv.org/abs/1706.08606)

参考文献

1. Landau, B., Smith, L. B., & Jones, S. S. (1988). The importance of shape in early lexical learning. *Cognitive Development*, *3*(3), 299–321.
2. Markman, E. M. (1990). Constraints children place on word meanings. *Cognitive Science*, *14*(1), 57–77.
3. Markman, E. M., & Hutchinson, J. E. (1984). Children's sensitivity to constraints on word meaning: Taxonomic versus thematic relations. *Cognitive Psychology*, *16*(1), 1–27.
4. Markman, E. M., & Wachtel, G. F. (1988). Children's use of mutual exclusivity to constrain the meanings of words. *Cognitive Psychology*, *20*(2), 121–157.
