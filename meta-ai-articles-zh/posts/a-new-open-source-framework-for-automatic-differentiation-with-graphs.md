---
title: "一个基于图做自动微分的新开源框架"
title_en: "A new open source framework for automatic differentiation with graphs"
date: 2019-05-22
source: http://ai.facebook.com/blog/a-new-open-source-framework-for-automatic-differentiation-with-graphs
crawled: 2026-09-22
translated: 2026-09-22
---

# 一个基于图做自动微分的新开源框架

> 原文：[A new open source framework for automatic differentiation with graphs](http://ai.facebook.com/blog/a-new-open-source-framework-for-automatic-differentiation-with-graphs) · Meta AI（Wayback 存档）

**研究内容：**GTN 是一个开源框架，使用一种强大而富有表现力的图——加权有限状态转换器（WFST）——进行自动微分。正如 PyTorch 为张量上的自动微分提供了框架，GTN 为 WFST 提供了这样的框架。AI 研究者和工程师可以用 GTN 更有效地训练基于图的机器学习模型。WFST 数据结构常用于在语音识别、自然语言处理和手写识别等应用中组合不同的信息源。一个标准的语音识别器可能由声学模型（预测一段语音中出现的字母）和语言模型（预测某个词跟在另一个词后面的可能性）组成。这些模型可以表示为 WFST，通常分开训练，再组合给出最可能的转写。我们的新 GTN 库让不同类型的模型可以一起训练，从而提供更好的结果。图比张量更有结构，这让研究者能够把更多关于任务的有用先验知识编码进学习算法。例如在语音识别中，如果某个词有几种可能的发音，GTN 允许我们把这个词的发音编码到图中，并把该图纳入学习算法。此前，训练时对单个图的使用是隐式的，开发者不得不在软件中硬编码图结构。现在，借助这一框架，研究者可以在训练时动态使用 WFST，整个系统可以更高效地从数据中学习和改进。这张图展示了在 GTN 中构建的一个简单 WFST，它把「the」的词片分解转换（transduce）为该词本身。

**工作原理：**借助 GTN（graph transformer networks 的缩写），研究者可以轻松构建 WFST、将其可视化并对其执行运算。只需简单调用一次 gtn.backward，就可以对参与计算的任何图计算梯度。下面是一个示例：

```python
import gtn

g1 = gtn.Graph()
g2 = gtn.Graph()
# ... 向图中添加一些节点和弧 ...

# 计算图的一个函数：
intersection = gtn.intersect(g1, g2)
score = gtn.forward_score(intersection)

# 计算梯度：
gtn.backward(score)
```

GTN 的编程风格用起来像 PyTorch 等流行框架一样熟悉。其命令式风格、autograd API 和 autograd 实现都基于相似的设计原则，主要区别在于我们用 WFST 及其相应运算取代了张量。与任何框架一样，GTN 力求在不牺牲性能的前提下做到易用。在我们的研究论文中，我们展示了如何用 GTN 实现算法的示例。其中一个示例使用 GTN 为任意序列级损失函数增添对「短语到词片分解」求边缘化的能力。模型可以自由选择如何把「the」这样的词分解为词片，例如模型可以选择使用「th」和「e」，或者「t」「h」「e」。词片常用于机器翻译和语音识别，但分解方式是从与任务无关的模型中选出的。我们的新方法让模型能够为给定任务学习一个词或短语的最优分解。

**为什么重要：**由于缺乏易用的框架，用有用的基于图的数据结构构建机器学习模型一直很困难。通过把图（数据）与图上的运算分离，研究者拥有更多自由和机会，在结构化学习算法的更大设计空间中进行实验。如果基于张量的框架的经验可以借鉴，那么便于实验算法的工具在开发更新更好的算法中扮演着关键角色。借助 GTN，图结构非常适合以「有启发性但不过分死板」的方式编码有用的先验知识。通过在训练时使用这些图，整个系统仍能从数据中学习和改进。从长远来看，WFST 的结构与数据学习的结合，有望让机器学习模型更准确、更模块化、更轻量。我们希望发布该软件能鼓励该领域的其他研究者与我们一起探索这一新的设计空间，寻找更好的学习算法。

在 GitHub 上获取：https://github.com/facebookresearch/gtn（或用 `pip install gtn` 安装）。

论文：https://arxiv.org/abs/2010.01003

**作者**

- Awni Hannun，研究科学家
- Vineel Pratap，研究工程师
- Jacob Kahn，研究工程师
- Wei-Ning Hsu，研究科学家
