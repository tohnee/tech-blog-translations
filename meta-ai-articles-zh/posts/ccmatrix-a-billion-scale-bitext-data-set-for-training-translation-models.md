---
title: "CCMatrix：用于训练翻译模型的十亿级双语文本数据集"
title_en: "CCMatrix: A billion-scale bitext dataset for training translation models"
date: 2020-02-06
source: http://ai.facebook.com/blog/ccmatrix-a-billion-scale-bitext-data-set-for-training-translation-models
crawled: 2026-09-22
translated: 2026-09-22
---

# CCMatrix：用于训练翻译模型的十亿级双语文本数据集

> 原文：[CCMatrix: A billion-scale bitext dataset for training translation models](http://ai.facebook.com/blog/ccmatrix-a-billion-scale-bitext-data-set-for-training-translation-models) · Meta AI（Wayback 存档）

**它是什么：**CCMatrix 是迄今最大的基于网络的高质量双语文本（bitext）数据集，用于训练翻译模型。它从 CommonCrawl 公开数据集的快照中提取了 576 个语言对、超过 45 亿个平行句子，比我们去年发布的 WikiMatrix 语料库大 50 多倍。

收集如此规模的数据集需要修改我们此前用于 WikiMatrix 的双语文本挖掘方法，其假设是：一个句子的翻译可能出现在 CommonCrawl（一个开放的互联网档案）的任何地方。为了应对比较数十亿句子以确定哪些互为翻译所带来的巨大计算挑战，我们使用了大规模并行处理，以及我们高效的 FAISS 库进行快速相似度搜索。

我们分享了创建 CCMatrix 的细节，以及其他研究者复现结果并在其工作中使用该语料库所需的工具。为了展示自动生成如此大量平行文本的价值，我们在 CCMatrix 上训练了神经机器翻译（NMT）系统，并与既有基线比较了性能。尽管只使用挖掘出的翻译（而非人工提供的翻译），我们得到的模型在四个语言方向（包括俄译英）上超越了机器翻译大会（WMT'19）上评估的最先进单一 NMT 系统。在 TED 语料库上测试时，与其他方法相比，CCMatrix 也让我们在许多语言对上显著提升了 NMT 性能。

**它做什么：**平行文本——一种语言的句子及其在另一种语言中的对应翻译——是大多数 NMT 训练方法的支柱。虽然更多的双语文本样本通常会带来更好的翻译性能，但收集覆盖众多语言的大型平行语料库是一项资源密集型任务。我们的方法将这一双语文本挖掘过程自动化、并行化，在配备 8 个 GPU 的服务器上一次处理多批 5000 万个样本。借助 FAISS 库，我们能够计算每批中所有句子嵌入之间的距离，且每次计算都是并行执行的。这样可以快速抽取句对，其来源比同类数据集（包括我们基于维基百科的 WikiMatrix）更为多样的公开文本。CCMatrix 的并行化双语文本挖掘方法可以一次性映射多种语言中数百万个句子之间的相似度，寻找可以用作翻译模型训练样本的句对。

**为什么重要：**CCMatrix 让 NMT 研究社区能够在数十个语言对上利用比以往大得多的双语文本数据集。这可以加速创建适用于更多语言、更有效的 NMT 模型，尤其是语料相对有限的低资源语言。凭借其巨大的规模和对广泛公开文本的使用，我们相信 CCMatrix 将成为整个 NMT 领域构建和评估系统时最常用的资源之一。我们也希望用于创建 CCMatrix 的技术能帮助研究社区开发出创建大规模数据集的新方法，从而改进全球人们使用的翻译工具。

在 GitHub 上获取：

- 论文：https://arxiv.org/abs/1911.04944
- GitHub：https://github.com/facebookresearch/LASER/tree/master/tasks/CCMatrix

**作者**

- Armand Joulin，研究科学家
- Holger Schwenk，研究科学家
