---
title: "通过新数据集与研究让对话式 AI 系统平民化"
title_en: "Democratizing conversational AI systems through new data sets and research"
date: 2021-07-01
source: http://ai.facebook.com/blog/democratizing-conversational-ai-systems-through-new-data-sets-and-research
crawled: 2026-09-22
translated: 2026-09-22
---

# 通过新数据集与研究让对话式 AI 系统平民化

> 原文：[Democratizing conversational AI systems through new data sets and research](http://ai.facebook.com/blog/democratizing-conversational-ai-systems-through-new-data-sets-and-research) · Meta AI（Wayback 存档）

2021 年 7 月 1 日

## 这项研究是什么

Facebook 正在分享新的研究和两个新数据集，旨在帮助研究社区为全球数亿人构建更精巧、更有效的对话式 AI 系统。对话式 AI 和数字助手正在快速进步，支持复杂得多的实用用途，但这些改进往往只惠及说英语等广泛使用语言的人群。此外，将现有模型扩展到新用例通常非常困难。一个重要原因是标注训练数据的约束。这些系统使用最先进的深度神经模型来解析和理解复杂的请求与命令。这些自然语言理解（NLU）模型依赖每个任务、每种语言的大量标注训练数据。而大规模标注数据集在许多较少使用的语言中并不可得，对新用例来说也往往难以获得或根本无法获得。

我们的方法克服了这一局限。它仅用十分之一的训练数据即可创建能执行陌生复杂任务的最先进对话式 AI 系统。通过改进的训练技术和更好的表示学习，我们可以构建能更高效理解诸如「给我看去老鹰队比赛的驾车路线」这类指令的模型——这要求 AI 理解多个意图。将对话式 AI 模型扩展到新语言同样困难。因此我们还提供了一个多语言 NLU 模型的细节，其表现优于单语言模型。我们的方法能有效地将模型扩展到缺乏大规模标注数据集的语言。通过将 NLU 模型扩展到支持更多语言中更多样的用例——尤其是缺乏大量标注训练数据的语言——我们可以让对话式 AI 走向平民化，把这项技术带给更多人。

## 它是如何工作的

传统 NLU 模型解析「旧金山的天气怎么样？」这类问题的方式很直接：先把意图（此处是 GET_WEATHER）匹配到一组预定义的意图标签，再识别该意图所需的全部槽位（此处是将旧金山标注为 LOCATION 槽位）。但更复杂的任务需要更精巧的技术，而且模型通常必须为每个任务准备大量领域特定的标注训练样本。

（原文此处附图：在该示例中，请求包含多个槽位和嵌套意图。）

我们增强了 NLU 模型，使其支持更多样的领域，而无需重度依赖人工标注的训练数据。我们的方法可以为新领域创建面向任务的语义解析器，每个意图或槽位标签只需少至 25 个训练样本。我们首先证明，BART 等预训练 Transformer 模型对于学习更丰富、更鲁棒、可泛化到新低资源领域的表示至关重要。另一方面，这些大型预训练模型在新领域仅有极少训练样本做微调时有时会带来挑战。因此，我们进一步采用元学习来改进在高资源领域上训练的 BART 模型的泛化能力，使其更容易在目标领域用极少训练数据微调。我们还提出了一种称为低秩自适应标签平滑（low-rank adaptive label smoothing，LORAS）的技术，以利用 NLU 任务标签空间中的潜在结构——在可用于学习新用户意图表示的样本极少的低资源设置下，它能提升模型准确率。

我们正在发布 TOPv2——一个包含 8 个领域、超过 18 万个标注样本的多领域 NLU 数据集。在 TOPv2 上使用我们的元学习和 LORAS 技术，我们仅用十分之一的训练数据就取得了与标准监督方法相当的性能。

将 NLU 模型扩展到新语言同样充满挑战，因为这通常需要构建大规模标注数据集——既困难又耗时。我们试图通过构建多语言 NLU 模型来简化这一点，这类模型能将拥有大量训练数据的语言所学到的知识迁移到数据较少的其他语言。我们使用预训练的多语言 Transformer 模型（如 XLM-R、mBART、CRISS 和 MARGE）作为 NLU 模型的构建模块。实验表明，多语言共享的 NLU 模型相比逐语言模型，在所有语言上都显著提升性能，从而实现更快的语言扩展。通过使用机器翻译，我们进一步探索了「翻译—对齐」数据增强，并提出了一种远程监督技术，以构建无需目标语言任何训练数据即可良好泛化的模型。我们的零样本模型平均错误率接近最好的语言内 NLU 模型，这意味着我们可以在没有任何泰语训练数据的情况下开发泰语模型。

我们正在发布 MTOP 数据集——一个多语言面向任务解析数据集，涵盖六种语言、11 个领域和 117 种意图类型，共约 10 万条话语。关于该数据集、其创建过程和我们实验的更多细节见这篇论文。

## 为什么它重要

正如 Facebook AI 首席科学家 Yann LeCun 近来指出的，AI 研究的未来在于构建更智能的通用型模型，能够跨不同任务、领域和语言习得新技能而无需海量标注数据。这在对话式 AI 领域尤为如此——系统需要能够理解所有类型的用户、满足各种各样的需求。Facebook 对构建这类系统有长期承诺，因为世界太过丰富多样，仅靠人工精选并标注的样本训练的机器无法理解它。

我们知道，新的模型架构之类的技术创新只是确保 AI 系统公平性的一部分。Facebook AI 已就负责任地开发 AI 做出长期承诺，这项工作需要开发衡量公平性的新方法、新的技术工具包，以及与外部专家、政策制定者等的持续开放对话。我们在本博文中分享的新工作，将帮助我们更接近这样的愿景：通用模型能够为许多不同的人群把很多事情做好。

**阅读完整论文：**

- Low-resource domain adaptation for compositional task-oriented semantic parsing（EMNLP 2020）
- Learning better structured representations using low-rank adaptive label smoothing（ICLR 2021）
- MTOP: A comprehensive multilingual task-oriented semantic parsing benchmark（EACL 2021）

**获取数据集：** TOPv2、MTOP

我们要感谢 Brian Moran、Keith Diedrick 和 T.J. Trimble 在 TOPv2 数据集准备中的帮助。

**作者**

- Abhinav Arora，软件工程师
- Xilun Chen，研究科学家
- Asish Ghoshal，研究科学家
- Anchit Gupta，软件工程师
- Sonal Gupta，研究科学家经理
- Haoran Li，软件工程师
- Shuohui Chen，数据科学家
- Yashar Mehdad，应用研究科学家经理
- Luke Zettlemoyer，研究总监
