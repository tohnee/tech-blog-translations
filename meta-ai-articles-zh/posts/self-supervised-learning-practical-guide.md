---
title: "自监督学习实战指南（SSL 食谱）"
title_en: "The self-supervised learning cookbook"
date: 2023-04-25
source: https://ai.facebook.com/blog/self-supervised-learning-practical-guide
crawled: 2026-09-22
translated: 2026-09-22
---

# 自监督学习实战指南（SSL 食谱）

> 原文：[The self-supervised learning cookbook](https://ai.facebook.com/blog/self-supervised-learning-practical-guide) · Meta AI（Wayback 存档）

2023 年 4 月 25 日

自监督学习（SSL）——被称为「智能的暗物质」——是近期 AI 突破的关键要素。它使从海量未标注数据中学习成为可能，而非依赖精心标注的数据集，从而在多个领域拓展了深度学习的边界。如今它支撑着跨模态的前沿模型：自然语言（如翻译和大语言模型）、音频（如 data2vec），并解锁了灵活的新型计算机视觉模型（如在十亿张图像上训练的 SEER 模型和 DINOv2）。但训练 SSL 就像烹制一顿精致大餐——这是一门复杂的手艺，入门门槛很高。虽然许多食材可能为人熟知，但一份成功的 SSL 食谱涉及令人眼花缭乱的一系列选择，从选择合适的代理任务（pretext task）到用精心整理和调试的超参数进行训练。我们发布了全新的《自监督学习食谱》（Cookbook of Self-Supervised Learning）——一份面向 AI 研究者和从业者的实用指南，讲解如何驾驭 SSL 食谱、理解它的各种旋钮和杠杆，并获得探索 SSL 尚未被开发的风味所需的专长。这是我们降低门槛、帮助普及 SSL 研究的努力之一。你还会找到来自多所大学十余位作者的技巧与诀窍，包括纽约大学、马里兰大学、加州大学戴维斯分校、蒙特利尔大学，以及 Meta AI 的顶尖研究者（如 Yann LeCun）。

## SSL 的特色

与监督学习（目标是让输入匹配标签）不同，SSL 可以在没有标签的情况下学习，办法是基于数据的底层结构定义学习目标，这也被称为代理任务。例如在自然语言中，一个常见的 SSL 目标是遮住文本中的一个词并预测周围的词。这一目标鼓励模型捕捉文本中词与词之间的关系，而无需标签。同样的 SSL 模型表示随后可用于一系列下游任务，例如跨语言翻译文本、摘要，甚至生成文本等等。在计算机视觉中，类似的目标包括预测图像中被遮住的块（MAE：masked autoencoders）或表示（BYOL：bootstrap your own latent）。其他 SSL 目标鼓励将同一图像的两个视图（例如通过加色或裁剪形成）映射到相似的表示。

## SSL 食谱的难以捉摸之处

虽然原理简单，但多种因素的交汇导致了 SSL 的高入门门槛。第一，处理海量未标注数据的计算成本在训练和评估两方面都非常高。第二，没有多少详细论文展示实现 SSL 潜力所需的复杂实现选择。第三，由于 SSL 建立了一个显著不同的范式，它缺乏统一的词汇表和理论视角。没有刻画不同组件的共同基础，研究者就难以理解、比较和开发 SSL 方法。此外，从实现角度看，SSL 是一个快速发展的新兴领域，每种方法都有自己精确调校的训练食谱。标准代码库难觅踪影，而且它们往往使用前沿且难以理解的优化。

## SSL 的厨师指南

我们的新论文以任何研究者都易于使用的风格奠定了 SSL 及其食谱的基础。就像厨师先学习 chopping（切）和 sautéing（煎）等基本技法一样，研究者可以用这本食谱学习 SSL 的基本技法和词汇。具体而言，我们描述了各类方法家族，并用理论线索把它们的目标统一到一个视角中。你会看到关键概念（如损失项或训练对象）以易于理解的概念框呈现。研究者可以查看常见的训练食谱，包括超参数选择、如何组装架构和优化器等组件，以及如何评估 SSL 方法。你将在一处找到成功实现 SSL 方法所需的关键实践考量。

## 未开发的潜力

SSL 仍有许多悬而未决的研究问题，包括泛化保证、公平性属性，以及对对抗攻击乃至自然发生的变异的鲁棒性。研究界需要更好地理解那些看似不同却相互重叠的方法如何能产生最先进的结果，并更广泛地推进对 SSL 的理论理解以及真实世界部署的最佳实践。我们需要新的研究者来帮助解决这些开放问题并继续推动该领域前进。我们希望我们的 SSL 食谱能助一臂之力。

获取 SSL 食谱

我们感谢以下贡献者：Vlad Sobal、Ari Morcos、Shashank Shekhar、Tom Goldstein、Florian Bordes、Adrien Bardes、Gregoire Mialon、Yuandong Tian、Avi Schwarzschild、Andrew Gordon Wilson、Jonas Geiping、Quentin Garrido、Pierre Fernandez、Amir Bar、Hamed Pirsiavash、Yann LeCun 和 Micah Goldblum

**作者**
Mark Ibrahim，研究工程师
Randall Balestriero，博士后研究员
