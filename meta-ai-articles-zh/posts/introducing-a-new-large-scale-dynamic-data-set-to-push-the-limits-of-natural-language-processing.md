---
title: "推出全新大规模动态数据集，突破自然语言处理的极限"
title_en: "Introducing a new, large-scale dynamic dataset to push the limits of natural language processing"
date: 2020-07-03
source: https://ai.facebook.com/blog/introducing-a-new-large-scale-dynamic-data-set-to-push-the-limits-of-natural-language-processing
crawled: 2026-09-22
translated: 2026-09-22
---

# 推出全新大规模动态数据集，突破自然语言处理的极限

> 原文：[Introducing a new, large-scale dynamic dataset to push the limits of natural language processing](https://ai.facebook.com/blog/introducing-a-new-large-scale-dynamic-data-set-to-push-the-limits-of-natural-language-processing) · Meta AI（Wayback 存档）

**这项研究是什么：**基准测试在推动 AI 研究进步方面扮演着关键角色。它们为研究社区确立了共同目标，并让不同架构、思想和方法之间可以直接比较。但随着研究不断推进，静态基准变得局限且很快被「刷爆」，在自然语言处理（NLP）领域尤为如此。例如，GLUE 基准于 2018 年初发布后，NLP 研究者不到一年就在其上达到了人类水平。SuperGLUE 增添了一组更难的任务，但研究者们构建出能在该基准上取得「超人类」表现的模型之后，它也很快饱和。这类静态基准可能导致模型不仅在这些基准上过拟合，还会捕捉到其中可能无意存在的偏见，而非真正理解语言。一个著名的例子是：在某些问答数据集中，面对「How much?（多少？）」这类数量问题，只要一律回答数字「2」，就能得到出人意料的高准确率。尽管 NLP 进展迅速，AI 系统距离真正理解自然语言仍然很远。这就引出了一个问题：我们的基准到底在测量正确的东西吗？我们能否让基准更鲁棒、更持久？为了提供一个更强大的 NLP 基准，我们推出了一个新的大规模数据集——对抗自然语言推理（Adversarial Natural Language Inference，ANLI）。NLI 是 NLP 的一项核心任务，也是判断 AI 系统对语言理解程度的一个良好代理指标。其目标在于判定一个陈述能否从给定上下文中推断出来（正向蕴含）。例如，「苏格拉底是人，而人皆有一死」蕴含「苏格拉底终有一死」；「苏格拉底不死」则是矛盾；「苏格拉底是哲学家」则为中性。我们采用了一种新颖的动态方法来构建 ANLI 数据集：由人类标注员蓄意「愚弄」在此类 NLI 任务上最先进的模型，从而为训练更强的模型创造出有价值的新样本。经过数轮迭代，我们不断推动最先进模型改进其薄弱之处，并构造出越来越难的测试集。一旦模型过拟合或学到了某种偏见，我们就可以增加新一轮样本来挑战它。因此，这种动态、迭代式的方法使该任务不可能被饱和，并为 NLP 社区带来了一项全新而鲁棒的挑战。

**工作原理：**我们这种新颖的数据收集方法名为 HAMLET（Human-and-Model-in-the-Loop-Entailment Training，人与模型在环的蕴含训练）。我们雇请人类标注员撰写陈述，刻意让最先进的模型对给定上下文（或前提）预测出错误标签。上下文从公开可用的第三方数据集中随机采样。如果标注员成功骗过了模型，我们会给予更丰厚的奖励，以此激励标注员想出那些对训练更鲁棒模型很有价值的困难样本。对每一条被模型错分的人类生成样本，我们还会请标注员给出他们认为模型失败的原因，再由另一个人进行核验。

（图中四个步骤构成一轮数据收集。在第 3 步中，模型答对的样本会进入训练集；开发集和测试集则完全由「模型答错且经核验正确」的样本构成。）

我们将该流程重复了三轮，针对的模型各不相同，且随着新采集数据的训练而越来越强。我们证明，这一过程促使标注员创造出更困难的样本，而这些样本对训练也更有价值。所收集的样本对当前最先进的系统构成了动态挑战——它们在新数据集上表现不佳。

**为什么重要：**当前的静态基准已难以跟上 NLP 的进步步伐。借助我们全新的 HAMLET 方法与 ANLI 数据集——模型与人类均在环中交互——我们可以推动最先进模型在语言理解上取得有意义的进步。动态对抗式数据收集帮助我们更好地度量模型的强弱。一个自然语言理解（NLU）系统越难被愚弄，它真正理解人类水平语言的能力就越强。展望未来，我们相信基准不应是静止的靶子；相反，研究社区应当转向动态的基准测试方式，让当前最先进的模型始终参与其中。

阅读完整论文：Adversarial NLI: A New Benchmark for Natural Language Understanding

试用演示：Adversarial NLI

获取数据集：Adversarial NLI GitHub
