---
title: "用 AI 预测基因表达"
title_en: "Predicting gene expression with AI"
source: https://deepmind.google/blog/predicting-gene-expression-with-ai/
site: deepmind
date: 2021-10-04
crawled: 2026-09-13
translated: 2026-09-13
---

# 用 AI 预测基因表达

> 原文：[Predicting gene expression with AI](https://deepmind.google/blog/predicting-gene-expression-with-ai/) · Google DeepMind

我们基于 Transformer 的新架构 Enformer 提升了预测 DNA 序列如何影响基因表达的能力，推动遗传学研究向前发展。

当[人类基因组计划](https://www.genome.gov/human-genome-project/What)成功绘制出人类基因组的 DNA 序列时，国际研究界对更好地理解影响人类健康与发育的遗传指令这一机会感到兴奋。DNA 携带决定一切——从眼睛颜色到对某些疾病和紊乱的易感性——的遗传信息。人体中被称为基因的大约 2 万个 DNA 区段，包含着蛋白质氨基酸序列的指令，而蛋白质在我们的细胞中执行着众多至关重要的功能。然而，这些基因只占基因组的不到 2%。其余的碱基对——占基因组 30 亿个「字母」的 98%——被称为「非编码」区域，它们包含着关于基因应在人体何时、何地被产生或表达的指令，但人们对这些指令的理解还比较有限。在 DeepMind，我们相信 AI 能够解锁对这类复杂领域的更深入理解，加速科学进步，并为人类健康带来潜在益处。

今天，《自然·方法学》（Nature Methods）发表了「[Effective gene expression prediction from sequence by integrating long-range interactions](https://www.nature.com/articles/s41592-021-01252-x)」（最早以预印本形式发布于 [bioRxiv](https://www.biorxiv.org/content/10.1101/2021.04.07.438649v1)）。在这项工作中，我们与 Alphabet 旗下 [Calico](https://www.calicolabs.com/) 的同事合作，提出了一种名为 Enformer 的神经网络架构，它在从 DNA 序列预测基因表达方面带来了大幅提升的准确性。为了推动对基因调控和疾病因果因素的进一步研究，我们还将我们的模型及其对常见遗传变异的初步预测[在此开放提供](https://github.com/deepmind/deepmind-research/tree/master/enformer)。

以往关于基因表达的工作通常使用卷积神经网络作为基本构件，但它们在建模远端增强子对基因表达影响方面的局限，阻碍了其准确性和应用。我们最初的探索依赖于 [Basenji2](https://github.com/calico/basenji)，它可以从 4 万碱基对这样相对较长的 DNA 序列预测调控活性。受这项工作以及「调控 DNA 元件可以在更远距离上影响表达」这一认识的启发，我们意识到需要对基础架构做出改变，以捕捉长序列。

我们开发了一个基于 [Transformer](https://ai.googleblog.com/2017/08/transformer-novel-neural-network.html) 的新模型——Transformer 在自然语言处理中很常见——以利用自注意力机制整合大得多的 DNA 上下文。由于 Transformer 非常适合处理长篇文本，我们把它改造为能够「阅读」大幅扩展的 DNA 序列。通过有效处理序列、考虑距离达以往方法 5 倍以上（即 20 万碱基对）的相互作用，我们的架构可以在 DNA 序列中从更远处建模被称为增强子的重要调控元件对基因表达的影响。

![一张展示 Enformer 神经网络架构的示意图：它使用卷积层与 Transformer 层处理 DNA 序列输入，捕捉宽广的感受野（100 kb，相比之下 Basenji2 为 20 kb），然后输出针对不同物种（人类与小鼠）的预测，涵盖基因表达、DNA 可及性和组蛋白修饰等多种基因组学轨道。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227e3d36e3ad3540e4966f8_Fig_01.svg)

Enformer 经过训练，可以从 20 万碱基对的输入 DNA 预测包括基因表达在内的功能基因组学数据。上例展示了超过 5,000 条可能基因组轨道中的三条。通过使用借助注意力在整个序列上收集信息的 Transformer 模块，与以前的模型相比，我们得以有效考虑长得多的输入序列。

为了更好地理解 Enformer 如何解读 DNA 序列以得出更准确的预测，我们使用贡献分数来突出输入序列中哪些部分对预测影响最大。与生物学直觉相符，我们观察到模型会关注增强子，即使它们距离该基因超过 5 万碱基对。预测哪些增强子调控哪些基因仍是基因组学中一个重要的未解难题，因此我们很高兴地看到，Enformer 的贡献分数与专门为这一任务开发的现有方法（使用实验数据作为输入）表现相当。Enformer 还学习了隔离子元件——它们把两个独立调控的 DNA 区域分隔开来。

![一张对比图，展示 Enformer 与 Basenji2 在从 -20 到 50 kb 以上的基因组位置上的贡献分数，显示 Enformer 捕捉到了远超 Basenji2 范围的远程增强子信号。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227e3eaa74731761213efe1_Fig_02.svg)

得益于更宽广的感受野，即使增强子（灰色方框）距离基因超过 2 万碱基对，Enformer 也能关注到相关的调控 DNA 区域（蓝色显示）。

尽管如今已经可以研究一个生物体的完整 DNA，但要理解基因组仍需要复杂的实验。尽管实验工作投入巨大，DNA 对基因表达控制的绝大部分仍是未解之谜。借助 AI，我们可以探索在基因组中寻找模式的新可能，并为序列变化提供机制性假设。就像一个拼写检查器，Enformer 部分理解 DNA 序列的「词汇」，因而能够标出那些可能导致基因表达改变的「编辑」。

这个新模型的主要应用是预测对 DNA 字母的哪些改变（也称为遗传变异）会改变基因的表达。与以前的模型相比，Enformer 在预测变异对基因表达的影响方面显著更准确，无论是针对自然遗传变异，还是针对改变重要调控序列的合成变异。这一特性对于解读全基因组关联研究获得的、数量不断增长的疾病相关变异非常有用。与复杂遗传疾病相关的变异绝大多数位于基因组的非编码区，很可能通过改变基因表达而致病。但由于变异之间固有的相关性，这些疾病相关变异中有许多只是虚假相关，而非因果关系。计算工具如今可以帮助区分真正的关联与假阳性。

![一张三面板基因组图，对比观测到的 NLRC5 表达与 Enformer 的预测，说明 r11644125 C>T 变异所导致的表达差异预测，并配以放大的序列标志图，显示该变异破坏了一个 SP1 结合位点。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227e3fd5038a523cf94bc53_Fig_03.svg)

变异 rs11644125 位于免疫应答基因 NLRC5 中，与较低水平的单核细胞和淋巴细胞（白细胞）相关。通过系统性地突变该变异周围的每个位置并预测其对 NLRC5 基因表达的相应影响（以字母高度显示），我们观察到该变异导致 NLRC5 的整体表达降低，并调节了名为 SP1 的转录因子的已知结合基序。因此，Enformer 的预测提示，该变异影响白细胞计数背后的生物学机制，是由 SP1 结合受到扰动导致 NLRC5 基因表达降低。

我们距离解开人类基因组中尚存的无数谜题还很远，但 Enformer 是理解基因组序列复杂性道路上向前迈出的一步。如果你有兴趣使用 AI 探索细胞的基本过程如何运作、它们如何被编码在 DNA 序列中，以及如何构建新系统来推进基因组学和我们对疾病的理解，[我们正在招聘](https://deepmind.com/careers/jobs/2079110)。我们也期待扩大与渴望探索计算模型、帮助解决基因组学核心开放问题的其他研究者和组织的合作。
