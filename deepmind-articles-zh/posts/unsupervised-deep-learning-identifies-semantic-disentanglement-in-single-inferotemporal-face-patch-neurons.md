---
title: "无监督深度学习在单个下颞叶面部区块神经元中发现语义解耦"
title_en: "Unsupervised deep learning identifies semantic disentanglement in single inferotemporal face patch neurons"
source: https://deepmind.google/blog/unsupervised-deep-learning-identifies-semantic-disentanglement-in-single-inferotemporal-face-patch-neurons/
site: deepmind
date: 2021-11-09
crawled: 2026-09-13
translated: 2026-09-13
---

# 无监督深度学习在单个下颞叶面部区块神经元中发现语义解耦

> 原文：[Unsupervised deep learning identifies semantic disentanglement in single inferotemporal face patch neurons](https://deepmind.google/blog/unsupervised-deep-learning-identifies-semantic-disentanglement-in-single-inferotemporal-face-patch-neurons/) · Google DeepMind

我们的大脑具有处理视觉信息的惊人能力。我们只需瞥一眼复杂场景，就能在几毫秒内把它解析成物体及其属性（如颜色或大小），并利用这些信息用简单的语言描述这一场景。这种看似毫不费力的能力背后，是我们的视觉皮层执行的复杂计算：它把从视网膜传来的数以百万计的神经脉冲，转换成一种更有意义、可以映射到简单语言描述的形式。为了充分理解这一过程在大脑中如何运作，我们既需要弄清语义上有意义的信息在视觉处理层级末端神经元放电中是如何表示的，也需要弄清这样一种表示如何能够从大量未经传授的经验中学习得到。

![图 1：示意图展示了解耦神经网络的过程：将三维输入场景通过推理映射为结构化的槽位与潜在表示，再通过生成重建出输出场景。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/623358932faa37a01b17d6b6_unnamed.gif)

图 1. 解耦指的是神经网络在未被明确告知这些属性是什么的情况下，发现图像中语义有意义属性的能力。这类模型通过推理神经网络把图像映射到低维表示，并尝试用生成神经网络重建图像，以此学习。解耦表示中的每个潜在单元学会编码单一可解释的属性，比如物体的颜色或大小。每次只操纵一个这样的潜在变量，会使生成的图像重建发生可解释的变化。动画制作：Chris Burgess。

为了在面部感知的语境下回答这些问题，我们与加州理工学院（Caltech）的合作伙伴（[Doris Tsao](https://www.tsaolab.caltech.edu/)）以及中国科学院的合作伙伴（[Le Chang](http://english.cebsit.cas.cn/)）联手。我们之所以选择面孔，是因为它们在神经科学界已被充分研究，并常被视为「[物体识别的缩影](https://pubmed.ncbi.nlm.nih.gov/18558862/)」。具体而言，我们希望把合作伙伴记录的、视觉处理层级末端面部区块中单个皮层神经元的反应，与最近兴起的一类所谓「解耦」深度神经网络进行比较——与通常的「黑箱」系统不同，这类网络明确地以对人类可解释为目标。「解耦」神经网络学习把复杂图像映射到少量内部神经元（称为潜在单元），每个单元表示场景的一个语义上有意义的属性，如物体的颜色或大小（见图 1）。与那些通过生物学上不现实的大量外部监督训练出来、用于识别视觉物体的「黑箱」深度分类器不同，这类解耦模型在没有外部教学信号的情况下训练，使用的是从学习到的潜在表示（通过图 1 中的推理获得）重建输入图像（图 1 中的生成）这一自监督目标。

近十年前，机器学习界就曾[假设](https://arxiv.org/pdf/1305.0445v2.pdf)解耦是构建更[数据高效](https://arxiv.org/abs/1911.10866)、更[可迁移](https://arxiv.org/abs/1707.08475)、更[公平](https://arxiv.org/pdf/2002.02886.pdf)、更具[想象力](https://deepmind.com/blog/article/imagine-creating-new-visual-concepts-recombining-familiar-ones)的人工智能系统的必要组成部分。然而，多年来，构建一个在实践中能够真正解耦的模型一直困扰着这个领域。第一个能够成功且稳健地做到这一点的模型叫做 [β-VAE](https://openreview.net/references/pdf?id=Sy2fzU9gl)，它的开发[从神经科学中汲取了灵感](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3306444/#:~:text=Mounting%20evidence%20suggests%20that%20%E2%80%9Ccore,in%20the%20inferior%20temporal%20cortex.)：β-VAE 通过[预测自身输入](https://www.nature.com/articles/s41593-018-0200-7)来学习；它要成功学习所需要的视觉经验与[婴儿所经历的](https://www.cell.com/trends/cognitive-sciences/fulltext/S1364-6613(18)30027-5)类似；而且它学到的潜在表示呼应了[已知的视觉大脑特性](https://www.nature.com/articles/s41593-019-0377-4)。

在我们的[新论文](https://www.nature.com/articles/s41467-021-26751-5)中，我们测量了一个在面部图像数据集上训练的 β-VAE 所发现的解耦单元，与灵长类动物在观看相同面孔时记录的视觉处理末端单个神经元的反应之间的相似程度。神经数据由我们的合作伙伴在 [Caltech 机构动物管理与使用委员会](https://researchcompliance.caltech.edu/committees/institutional-animal-care-and-use-committee-iacuc)的严格监督下采集。当我们进行比较时，我们发现了一些令人惊讶的东西——β-VAE 发现的少数几个解耦单元的表现，似乎等价于同等规模的真实神经元子集。仔细观察后，我们发现了真实神经元与人工神经元之间强大的一一对应关系（见图 2）。这种对应关系远强于替代模型的对应关系，包括此前被视为视觉处理最先进计算模型的深度分类器，以及被神经科学界视为「黄金标准」的手工设计面部感知模型。不仅如此，β-VAE 的单元编码了诸如年龄、性别、眼睛大小或是否有笑容这类语义上有意义的信息，使我们能够理解大脑中的单个神经元是用哪些属性来表示面孔的。

![表示图 2 的插图，展示了解耦的人工单元与真实生物神经元之间强大的一一对应关系。左侧，一张风格化的面孔被水平切分为可调节的面部特征槽位（眼睛、鼻子、嘴巴）；右侧，这些特征直接连接到带有相应放电活动尖峰的各个生物神经元。](https://lh3.googleusercontent.com/ixm0cc1TmsdjTcabieUNsjSsnm38UScJHH7dH-pKVA09XM9ShLEt4-Dbho2ty2UjrQfKTtywcpih6v2oPR4A3EO5jO_DnGm-EmxPjM_tNMy6dBqb3Q=w1440)

图 2. 视觉处理层级末端的灵长类面部区块中的单个神经元，表示可解释的面部属性，如眼睛形状或是否有笑容，并且与通过解耦表示学习发现的 β-VAE 中的单个人工神经元等价。图片来源：Marta Garnelo。

如果 β-VAE 确实能够自动发现就其对面部图像的反应而言与真实神经元等价的人工潜在单元，那么就有可能把真实神经元的活动翻译成与之匹配的人工对应物，并使用训练好的 β-VAE 的生成器（见图 1）来可视化真实神经元正在表示的面孔。为验证这一点，我们向灵长类动物展示了模型从未见过的新面孔图像，并检验我们能否用 β-VAE 生成器把它们渲染出来（见图 3）。我们发现这确实是可能的。仅使用 12 个神经元的活动，我们就生成了比替代深度生成模型所产生的重建更准确、视觉质量更好的面孔图像。尽管事实上，人们普遍知道替代模型在一般情况下是比 β-VAE 更好的图像生成器。

![图 3 的插图，展示把真实生物神经元翻译为人工潜在变量以重建新面孔。左侧，一个灵长类剪影正在观看「新面孔」图像。记录电极通过线性映射把单个神经元（在脑图标下表示）映射到单个 β-VAE 人工潜在变量（在神经网络图标下）。这些潜在变量经过训练好的 β-VAE 生成器，在最右侧生成「重建」的面孔。](https://lh3.googleusercontent.com/8Nn55WMWK9v4bF6TStxZ0MOazJ9UTWrUw0hCDwEZnLxxluJos9J4BQICijcwkXA2GKI7ZGU-_Di81CQuGghjqWe53Ckywvvkp9O8uYtTI1xnVRC45A=w1440)

图 3. 在灵长类观看新面孔时，训练好的 β-VAE 生成器根据灵长类视觉皮层中 12 个一一匹配神经元的活动，准确重建了面孔图像。新面孔图像经 Ma et al. 和 Phillips et al. 授权转载。

我们在[新论文](https://www.nature.com/articles/s41467-021-26751-5)中总结的发现表明，视觉大脑可以在单个神经元的层面上被理解，甚至在其处理层级的末端也是如此。这与一种普遍看法相悖，即语义上有意义的信息[在大量此类神经元之间复用](https://www.sciencedirect.com/science/article/abs/pii/S0959438818300990)，每个神经元单独来看基本不可解释，这很像深度分类器中信息在整个人工神经元层上的编码方式。不仅如此，我们的发现还提示，大脑可能是通过优化解耦目标来学会支持我们不费吹灰之力进行视觉感知的能力的。虽然 β-VAE 最初是受[高层神经科学原理](https://www.cell.com/trends/cognitive-sciences/fulltext/S1364-6613(18)30027-5)启发而开发的，但解耦表示对智能行为的效用迄今主要是在[机器学习界](https://arxiv.org/pdf/2002.02886.pdf)得到论证的。延续神经科学与机器学习之间互利[互动的悠久历史](https://www.cell.com/neuron/pdf/S0896-6273(17)30509-3.pdf)，我们希望机器学习最新的洞见能够反哺神经科学界，去研究解耦表示对于支持生物系统智能的价值，尤其是作为[抽象推理](https://www.science.org/doi/10.1126/science.aat6766)或可泛化、高效[任务学习](https://www.nature.com/articles/s41593-019-0470-8)的基础。
