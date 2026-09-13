---
title: "FunSearch：利用大语言模型在数学科学中做出新发现"
title_en: "FunSearch: Making new discoveries in mathematical sciences using Large Language Models"
source: https://deepmind.google/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/
site: deepmind
date: 2023-12-14
crawled: 2026-09-13
translated: 2026-09-13
---

# FunSearch：利用大语言模型在数学科学中做出新发现

> 原文：[FunSearch: Making new discoveries in mathematical sciences using Large Language Models](https://deepmind.google/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/) · Google DeepMind

通过搜索以计算机代码编写的「函数」，FunSearch 利用 LLM 首次在数学科学的开放问题上做出了发现

更新：2024 年 12 月，我们在 [arXiv](https://arxiv.org/abs/2411.19744) 上发布了一份报告，展示我们的方法如何用于提升人类在组合竞赛编程中的表现。

大语言模型（LLM）是有用的助手——它们擅长组合概念，能够阅读、写作和编程，帮助人们解决问题。但它们能否发现全新的知识？

由于 LLM 已被证明会「幻觉」出事实错误的信息，用它们做出可验证为正确的发现是一项挑战。但如果我们可以只识别并采纳 LLM 最出色的想法、进而利用它们的创造力呢？

今天，在[发表于 Nature 的论文](https://www.nature.com/articles/s41586-023-06924-6)中，我们介绍 FunSearch，一种在数学和计算机科学中搜索新解的方法。FunSearch 的工作方式是将一个预训练 LLM（其目标是以计算机代码的形式提供创造性解法）与一个自动「评估器」配对，后者防范幻觉和错误想法。通过在这两个组件之间来回迭代，初始解会「演化」为新的知识。该系统搜索以计算机代码编写的「函数」——FunSearch（Fun=函数，Search=搜索）由此得名。

这项工作首次证明可以借助 LLM 为科学或数学中的具有挑战性的开放问题做出新发现。FunSearch 为 cap set 问题——一个长期悬而未决的数学难题——发现了新的解法。此外，为展示 FunSearch 的实际用处，我们用它为「装箱」（bin-packing）问题发现了更有效的算法，该问题应用无处不在，例如让数据中心更高效。

科学进步一直依赖于分享新认识的能力。FunSearch 之所以是一种特别强大的科学工具，在于它输出的程序会揭示其解是如何构造出来的，而不仅仅是解是什么。我们希望这能启发使用 FunSearch 的科学家获得更深入的洞见，推动改进与发现的良性循环。

## 用语言模型通过演化驱动发现

FunSearch 使用一种由 LLM 驱动的演化方法，来推举并发展得分最高的想法。这些想法以计算机程序的形式表达，从而可以被自动运行和评估。首先，用户以代码形式写出问题的描述。该描述包含一个评估程序的过程，以及一个用于初始化程序池的种子程序。

FunSearch 是一个迭代过程；在每次迭代中，系统从当前程序池中选出一些程序，将其输入 LLM。LLM 在此基础上进行创造性拓展，生成新的程序，这些程序会被自动评估。其中最好的程序被加回现有程序池，形成一个自我改进的循环。FunSearch 使用 [Google 的 PaLM 2](https://ai.google/discover/palm2/)，但它也兼容其他在代码上训练的 LLM。

![一幅示意图，说明 FunSearch 的迭代过程：问题规范被输入提示词，提示词被发送到预训练 LLM。LLM 生成若干候选程序，这些程序经过评估。不成功的程序被丢弃，而成功的程序被加入程序数据库，以更新下一轮迭代的提示词，最终输出一个新颖的程序。](https://lh3.googleusercontent.com/fy2yezSUH6zXaZy4Ya8fAvMVZJhlyQpRMkflDqJRzj5WxNUg0aGCghOwSc6OzsF5c6B06qHUTLytzkMMKJnXHiUjl8a-nGxDxXAVPeAOYA5JVlt1=w1440)

FunSearch 的过程。LLM 会看到它迄今生成的最佳程序的一个子集（从程序数据库中检索），并被要求生成更好的程序。LLM 提出的程序被自动执行和评估。最佳程序被加入数据库，供后续周期挑选。用户可以随时检索迄今发现的得分最高的程序。

在不同领域发现新的数学知识和算法是出了名的困难任务，在很大程度上超出了最先进 AI 系统的能力。为了用 FunSearch 应对这类极具挑战性的问题，我们引入了多个关键组件。我们不从零开始，而是用关于该问题的常识性知识启动演化过程，让 FunSearch 专注于找到实现新发现最关键的想法。此外，我们的演化过程采用一种提升想法多样性的策略，以避免停滞。最后，我们并行运行演化过程以提高系统效率。

## 在数学上开辟新天地

我们首先攻克了 [cap set 问题](https://en.wikipedia.org/wiki/Cap_set)——一个悬而未决的挑战，几十年来一直困扰着多个研究领域的数学家。著名数学家陶哲轩（Terence Tao）曾把它称为他[最喜欢的开放问题](https://terrytao.wordpress.com/2007/02/23/open-question-best-bounds-for-cap-sets/)。我们与威斯康星大学麦迪逊分校数学教授、[cap set 问题重要突破的作者](https://arxiv.org/abs/1605.09223) Jordan Ellenberg 开展了合作。

该问题是寻找高维网格中最大的点集（称为 cap set），要求任何三点不共线。这个问题很重要，因为它是极值组合学中其他问题的模型——极值组合学研究的是数字、图或其他对象构成的集合可以有多大或多小。暴力计算方法对这个问题描述无效——需要考虑的可能性数量很快就会超过宇宙中的原子数。

FunSearch 生成了以程序形式呈现的解，在某些设定下发现了有史以来最大的 cap set。这代表着过去 20 年中 cap set 规模的[最大增幅](https://link.springer.com/article/10.1023/A:1027365901231)。此外，FunSearch 的表现超过了最先进的计算求解器，因为这个问题的规模远远超出了它们当前的能力。

这些结果表明，FunSearch 技术能带我们超越在困难组合问题上已确立的结果——在这类问题上，直觉往往难以建立。我们预计这一方法将在组合学中类似的理论问题的新发现上发挥作用，未来还可能在通信理论等领域开辟新的可能。

## FunSearch 偏好简洁且人类可解读的程序

发现新的数学知识本身就意义重大，而 FunSearch 方法相对传统计算机搜索技术还有一项额外的好处。这是因为 FunSearch 并不是一个仅仅生成问题解的黑箱。相反，它生成描述这些解是如何得到的程序。这种「展示解题过程」的方式正是科学家通常的做法：通过产生新发现或新现象的过程来解释它们。

FunSearch 偏好寻找由高度紧凑的程序所表示的解——即低 Kolmogorov 复杂度†的解。短小的程序可以描述非常大的对象，使 FunSearch 能够扩展到大海捞针式的大规模问题。此外，这也让 FunSearch 的程序输出更容易被研究者理解。Ellenberg 表示：「FunSearch 提供了一种全新的机制来制定进攻策略。FunSearch 生成的解在概念上远比一串单纯的数字丰富。当我研究它们时，我能学到东西。」

更进一步，FunSearch 程序的这种可解释性还能为研究者提供可操作的洞见。例如，在使用 FunSearch 的过程中，我们注意到它的一些高分输出的代码中存在耐人寻味的对称性。这给了我们对该问题的新认识，我们利用这一洞见对输入 FunSearch 的问题进行精炼，从而得到更好的解。我们认为这是人类与 FunSearch 在数学众多问题上开展协作的一个范例。

![左侧显示一个 priority 函数的 Python 代码，右侧生成一个由数值数组组成的大型密集网格。](https://lh3.googleusercontent.com/UXVB4Tn8_MyS3ZujRgOnAiY84lDJlIrGdG2-adY15NaV9467onjhuBpjeo-AzLynMxxwrXS2MdkX4n0EDIpumnT11G_269Qb6NftZ6xuGJD1sqNY=w1440)

左：检查 FunSearch 生成的代码带来了进一步可操作的洞见（我们添加了高亮）。右：用左侧那个（短得多的）程序构造出的原始「可容许」集合。

> FunSearch 生成的解在概念上远比一串单纯的数字丰富。当我研究它们时，我能学到东西。

Jordan Ellenberg

合作者、威斯康星大学麦迪逊分校数学教授

## 应对计算领域一个出了名的难题

受 cap set 理论问题成功的鼓舞，我们决定通过将 FunSearch 应用于计算机科学中一个重要的实际挑战，来探索它的灵活性。「装箱」（bin packing）问题研究如何把不同尺寸的物品装入数量最少的箱子。它位于许多现实世界问题的核心，从装载集装箱，到在数据中心分配计算任务以最小化成本。

在线装箱问题通常使用基于人类经验的算法经验法则（启发式方法）来解决。但为每种具体情况——不同的尺寸、时机或容量——找到一套规则可能很有挑战性。尽管与 cap set 问题截然不同，为这个问题配置 FunSearch 却很容易。FunSearch 交付了一个自动定制的程序（能适应数据的具体特征），其表现超过了既有的启发式方法——用更少的箱子装下同样数量的物品。

![您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

使用现有启发式方法（最优适应启发式，左）与使用 FunSearch 发现的启发式方法（右）进行装箱的示例。

在线装箱这类困难组合问题也可以用其他 AI 方法解决，[例如神经网络](https://deepmind.google/impact/optimizing-computer-systems-with-more-generalized-ai-tools/)和强化学习。这类方法已被证明同样有效，但部署时可能也需要大量资源。而 FunSearch 输出的是易于检查和部署的代码，这意味着它的解有可能被直接嵌入各种现实世界的工业系统，迅速带来收益。

## 更新：提升人类在组合竞赛编程中的表现

2024 年 12 月，我们在 [arXiv](https://arxiv.org/abs/2411.19744) 上发布了 Veličković 等人的一份报告，展示我们的方法如何用于提升人类在组合竞赛编程中的表现。

在 [Codeforces](https://codeforces.com/) 这类被 [AlphaCode](https://deepmind.google/discover/blog/competitive-programming-with-alphacode/) 瞄准的传统编程竞赛中，参赛者需要在时间和内存受限的环境下为经典算法挑战提供完整解法。相比之下，组合类竞赛的特点是问题高度复杂，目标不是找到正确答案，而是找到尽可能好的近似解，类似寻找 cap set 这类问题。鉴于这些问题对人类的难度，我们的方法可以生成优于顶尖百分位参赛者所找到解法的方案。而且它采用的路径非常适合人类与 AI 协作：人类程序员编写解法代码的「主干」，然后让 LLM 创造性地演化驱动它的函数。

> 这是一种令人兴奋的方法，把人类竞赛程序员的工作与 LLM 结合起来，取得两者各自都无法单独取得的成果。

Petr Mitrichev

Google 软件工程师、世界级竞赛程序员

随着通用 LLM 的改进，我们不再需要代码专用模型，可以基于 [Gemini 1.5 Flash](https://developers.googleblog.com/en/updated-gemini-models-reduced-15-pro-pricing-increased-rate-limits-and-more/) 构建。

在竞赛编程之外，我们还用 FunSearch 在贝叶斯优化框架内[寻找优化函数的更好方法](https://arxiv.org/abs/2406.04824)。

## 用 LLM 驱动的发现服务科学与更远的地方

FunSearch 表明，如果我们防范 LLM 的幻觉，这些模型的力量不仅可以用来产生新的数学发现，还能为重要的现实世界问题揭示潜在有影响力的解。

我们展望，对于科学和工业中的许多问题——无论是长期存在的还是新出现的——用 LLM 驱动的方法生成有效且量身定制的算法将成为常规做法。

的确，这只是开始。随着 LLM 更广泛的进步，FunSearch 将自然而然地改进，我们也将努力拓展它的能力，以应对社会上各种紧迫的科学与工程挑战。

进一步了解 FunSearch

[阅读论文的开放获取版本\*](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/Mathematical-discoveries-from-program-search-with-large-language-models.pdf)[阅读我们发表在 Nature 上的论文](https://www.nature.com/articles/s41586-023-06924-6)[提升人类在组合竞赛编程中的表现](https://arxiv.org/abs/2411.19744)[FunBO: Discovering Acquisition Functions for Bayesian Optimization with FunSearch](https://arxiv.org/abs/2406.04824)

**致谢**

Petar Veličković、Alex Vitvitskyi、Larisa Markeeva、Borja Ibarz 和 Alexander Novikov 参与了 2024 年 12 月「提升人类在组合竞赛编程中的表现」的更新。感谢 Matej Balog、Emilien Dupont、Alexander Novikov、Pushmeet Kohli、Jordan Ellenberg 对本博客的宝贵反馈以及对图表的帮助。这项工作由一个团队完成，贡献者包括：Bernardino Romera Paredes、Amin Barekatain、Alexander Novikov、Matej Balog、Pawan Mudigonda、Emilien Dupont、Francisco Ruiz、Jordan S. Ellenberg、Pengming Wang、Omar Fawzi、George Holland、Pushmeet Kohli 和 Alhussein Fawzi。

\*这是作者版本的论文。经 Nature 许可在此发布，仅供个人使用，不得再分发。正式版本发表于 Nature：[DOI: 10.1038/s41586-023-06924-6](https://www.nature.com/articles/s41586-023-06924-6)。

†Kolmogorov 复杂度指输出该解的最短计算机程序的长度。
