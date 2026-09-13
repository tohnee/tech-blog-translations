---
title: "一种关系推理的神经方法"
title_en: "A neural approach to relational reasoning"
source: https://deepmind.google/blog/a-neural-approach-to-relational-reasoning/
site: deepmind
date: 2017-06-06
crawled: 2026-09-13
translated: 2026-09-13
---

# 一种关系推理的神经方法

> 原文：[A neural approach to relational reasoning](https://deepmind.google/blog/a-neural-approach-to-relational-reasoning/) · Google DeepMind

想象一位读者拼凑阿加莎·克里斯蒂小说中的种种线索来推断真凶，一个孩子跑到她的皮球前面、防止它滚进小溪，甚至一位购物者在市场里权衡买猕猴桃还是买芒果哪个更划算。

我们把世界切分为事物之间的关系。我们之所以理解世界如何运转，靠的正是对这些不同事物——比如物理对象、句子，甚至抽象概念——彼此之间如何关联做出逻辑推断的能力。这种能力被称为关系推理（relational reasoning），它是人类智能的核心。

我们从每天经历的、源源不断的非结构化感官输入中构建这些关系。例如，我们的眼睛接收密集的光子流，而大脑却把这种"纷繁嘈杂的混沌"组织成我们需要建立关联的特定实体。

> 这两篇论文都为理解关系推理这一挑战展示了富有前景的方法。

要开发具有人类认知那种灵活性与效率的人工智能系统，一个关键挑战就是赋予它们类似的能力——从非结构化数据中对实体及其关系进行推理。解决这一问题将使这些系统能够泛化到实体的新组合上，以有限的方式实现无限的运用。

现代深度学习方法在解决来自非结构化数据的问题方面取得了巨大进步，但它们这样做时往往没有显式地考虑对象之间的关系。

在两篇新论文中，我们探索了深度神经网络用非结构化数据执行复杂关系推理的能力。在第一篇论文——[A simple neural network module for relational reasoning](https://arxiv.org/abs/1706.01427)——中，我们描述了关系网络（Relation Network，RN），并展示它在一项富有挑战性的任务上可以达到超越人类的水平。而在第二篇论文——[Visual Interaction Networks](https://arxiv.org/abs/1706.01433)——中，我们描述了一个通用模型，它可以纯粹基于视觉观察来预测物理对象的未来状态。

## A simple neural network module for relational reasoning

为了更深入地探索关系推理这一思想，并检验它是否是一种可以轻松添加到现有系统中的能力，我们创建了一个简单易用、即插即用的 RN 模块，它可以加入到现有的神经网络架构中。一个增强了 RN 的网络能够接收非结构化输入——比如一张图像或一系列句子——并对其中的对象关系进行隐式推理。

例如，一个使用 RN 的网络可能会面对一个由摆放在桌上的各种形状（球体、立方体等）构成的场景。为了弄清它们之间的关系（例如球体比立方体大），网络必须从图像的非结构化像素流中找出场景中什么才算作一个对象。网络不会被显式告知什么算作对象，而必须自己弄清楚。随后，这些对象的表示被两两分组（例如球体和立方体），并送入 RN 模块，由它进行比较以确立一种"关系"（例如球体比立方体大）。这些关系不是硬编码的，而是必须由 RN 在比较每一对可能的组合时学习得到。最后，它把所有这些关系累加起来，为场景中所有成对的形状产生一个输出。

我们在多个任务上测试了这一模型，其中包括 [CLEVR](https://cs.stanford.edu/people/jcjohns/clevr/)——一个视觉问答任务，旨在显式地考察模型执行不同类型推理的能力，例如计数、比较和查询。CLEVR 由这样的图像组成：

![多种颜色的三维物体集合，包括若干球体和长方体形状。它们以无规律、无次序的方式摆放在一个平面上。](https://lh3.googleusercontent.com/JLHuhf3IgcWwfYQ6-ovwuRwEpEzt5SkV9RSeyJVUZwXdOf89qjRf0vh1oe00hoHr54b7kCxuchR6evdhr9e1uN87rSNG2jaIECxw7V8D0fZGFmdV=w1440)

每张图像都配有考察场景中对象之间关系的问题。例如，针对上图的一个问题可能是："有一个微小的橡胶物体，它的颜色与那个大圆柱体相同；它是什么形状？"

使用标准视觉问答架构在 CLEVR 上的最先进成绩是 68.5%，而人类为 92.5%。但利用我们增强 RN 的网络，我们实现了 95.5% 的超人表现。

为了检验 RN 的通用性，我们还在一个截然不同的语言任务上测试了 RN。具体来说，我们使用了 [bAbI 套件](https://research.fb.com/downloads/babi/)——一系列基于文本的问答任务。bAbI 由许多故事组成，每个故事包含数量不定的句子，并以一个问题结尾。例如，"Sandra 拿起了足球"和"Sandra 去了办公室"可能引出问题"足球在哪里？"（答案："办公室"）。

增强 RN 的网络在 20 个 bAbI 任务中的 18 个上得分超过 95%，与现有最先进的模型相当。值得注意的是，它在某些任务上——例如归纳（induction）——得分更高，而这些任务恰恰给那些更成熟的模型带来了麻烦。

所有这些测试及更多内容的完整结果可在[论文中](https://arxiv.org/abs/1706.01427)查阅。

## Visual Interaction Networks

关系推理的另一个关键部分涉及在物理场景中预测未来。只需一眼，人类不仅能推断出哪些对象在哪里，还能推断出在接下来的几秒、几分钟甚至某些情况下更长的时间里它们会发生什么。例如，如果你把一个足球踢向墙壁，你的大脑会预测球撞上墙时会发生什么，以及此后两者的运动会受到怎样的影响（球会以与踢球力度成正比的速度反弹回来，而——在大多数情况下——墙会留在原地）。

这些预测由一套复杂的认知系统引导，用于推理对象及其物理交互。

在这项相关工作里，我们开发了"Visual Interaction Network"（VIN）——一个模仿这种能力的模型。VIN 能够仅凭几帧视频推断出多个物理对象的状态，然后用它来预测未来许多步的对象位置。这与生成式模型不同，后者可能会在视觉上"想象"出视频的下几帧。VIN 则是预测对象底层的相对状态如何演化。

VIN 由两个机制组成：一个视觉模块和一个物理推理模块。二者合在一起能够把视觉场景处理成一组彼此区分的对象，并学习一个隐式的物理规则系统，用以预测这些对象未来会发生什么。

我们在多种系统中测试了 VIN 的这一能力，包括弹跳的台球、由弹簧连接的质量块，以及存在引力的行星系统。我们的结果表明，VIN 能够准确预测未来数百步内对象会发生什么。

在与此前发表的模型以及去除了其关系推理机制的 VIN 变体的实验对比中，完整的 VIN 表现明显更好。

结果的完整细节同样可以[在我们的论文中](https://arxiv.org/abs/1706.01433)找到。

这两篇论文都为理解关系推理这一挑战展示了富有前景的方法。它们展示了如何通过把世界分解为对象及其关系的系统，赋予神经网络强大的推理能力，使它们能够泛化到对象的新组合，并对那些表面上看起来截然不同、但底层具有共同关系的场景进行推理。

我们相信这些方法是可扩展的，可以应用于更多的任务，帮助构建更精密的推理模型，并让我们更好地理解人类强大而灵活的通用智能中这个我们每天习以为常的关键组成部分。

**注**

关系网络（Relation Network）由 Adam Santoro、David Raposo、David G.T. Barrett、Mateusz Malinowski、Razvan Pascanu、Peter Battaglia 和 Timothy Lillicrap 开发

Visual Interaction Network 由 Nicholas Watters、Daniel Zoran、Theophane Weber、Peter Battaglia、Razvan Pascanu 和 Andrea Tachetti 开发

阅读 [A simple neural network module for relational reasoning](https://arxiv.org/abs/1706.01427)

阅读 [Visual Interaction Networks](https://arxiv.org/abs/1706.01433)
