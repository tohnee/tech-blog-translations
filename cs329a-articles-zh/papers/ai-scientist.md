---
title: "AI 科学家：迈向完全自动化的开放式科学发现"
title_en: "The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery"
arxiv: 2408.06292
source: https://arxiv.org/abs/2408.06292
crawled: 2026-09-23
translated: 2026-09-23
---

# AI 科学家：迈向完全自动化的开放式科学发现

> 原文：[The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery](https://arxiv.org/abs/2408.06292) · Stanford CS329A 指定阅读

Chris Lu（共同一作；Sakana AI；牛津大学 FLAIR）
Cong Lu（共同一作；不列颠哥伦比亚大学；Vector Institute）
Robert Tjarko Lange（共同一作；Sakana AI）
Jakob Foerster（牛津大学 FLAIR；共同指导）
Jeff Clune（不列颠哥伦比亚大学；Vector Institute；Canada CIFAR AI Chair；共同指导）
David Ha（Sakana AI；共同指导）

###### 摘要

通用人工智能的重大挑战之一，是开发出能够开展科学研究并发现新知识的智能体。尽管前沿模型已被用作人类科学家的助手，例如用于头脑风暴、编写代码或预测任务，它们仍然只承担科学过程中的一小部分。本文提出了首个面向完全*自动化科学发现*的综合框架，使前沿大型语言模型（LLM）能够独立开展研究并交流其发现。我们提出「AI 科学家」（The AI Scientist），它可以生成新颖的研究想法、编写代码、执行实验、可视化结果、通过撰写完整的科学论文来描述其发现，然后运行一个模拟的评审过程进行评估。原则上，这一过程可以重复进行，以开放式的方式迭代发展想法，并将其加入一个不断增长的知识档案，如同人类科学共同体一样。我们通过将该框架应用于机器学习的三个不同子领域——扩散建模、基于 Transformer 的语言建模与学习动力学——来展示其通用性。每个想法都被实现并发展为一篇完整论文，每篇成本仅约 15 美元，展示了我们的框架让研究大众化并显著加速科学进展的潜力。为评估生成的论文，我们设计并验证了一个自动化审稿人，并表明其在论文评分评估上达到接近人类的水平。AI 科学家可以产出按我们的自动化审稿人评判超过顶级机器学习会议录用阈值的论文。这一方法标志着机器学习科学发现新时代的开端：将 AI 智能体的变革性益处带给 AI 自身研究过程的*全部*环节，并使我们更接近一个能够对世界上最棘手的问题释放*无尽且负担得起的创造力与创新*的世界。我们的代码已在 <https://github.com/SakanaAI/AI-Scientist> 开源。

## 1 引言

现代科学方法（Chalmers, 2013；Jevons, 1877；Dewey, 1910）可以说是启蒙运动最伟大的成就之一。传统上，人类研究者收集背景知识、起草一组可供检验的合理假设、构建评估流程、为不同假设收集证据，最后评估并交流其发现。随后，成稿的论文经过同行评审以及后续的多轮打磨。这一流程带来了科学与技术上无数的突破，改善了人类的生活质量。然而，这一迭代过程天然受限于人类研究者的才智、背景知识与有限时间。自动化通用科学发现（Waltz and Buchanan, 2009；Langley, 2024；Langley, 1987）至少自 20 世纪 70 年代初以来就是社区的长期追求，出现了诸如「自动数学家」（Automated Mathematician；Lenat, 1977；Lenat and Brown, 1984）与 DENDRAL（Buchanan and Feigenbaum, 1981）等计算机辅助工作。在 AI 领域，研究者们设想了用 AI 自身来自动化 AI 研究的可能性（Schmidhuber, 1991；Schmidhuber, 2010b；Schmidhuber, 2010a；Schmidhuber, 2012；Ghahramani, 2015），引出了「AI 生成算法」（AI-generating algorithms；Clune, 2019）。近来，基础模型的通用能力取得了巨大进展（OpenAI, 2023；Google DeepMind Gemini Team, 2023；Anthropic, 2024；Llama Team, 2024），但它们只被证明能加速研究流程的个别环节，例如科学论文写作（Altmäe et al., 2023；Ifargan et al., 2024；Majumder et al., 2024；Dinu et al., 2024）、作为头脑风暴的灵感来源（Girotra et al., 2023；Wang et al., 2024b；Baek et al., 2024），或作为编程助手（Gauthier, 2024）。迄今为止，社区尚未展示在没有人类参与的情况下执行完整研究工作的可能性。

传统的自动化研究项目方法迄今依赖于仔细约束潜在发现的搜索空间，这严重限制了探索范围，并且需要大量人类专业知识与设计。例如，材料发现（Pyzer-Knapp et al., 2022；Merchant et al., 2023；Szymanski et al., 2023）与合成生物学（Jumper et al., 2021；Hayes et al., 2024）的重大进展，是通过将探索限制在具有预定义参数、特征清晰的领域内取得的，这带来了针对性的进展，但限制了更广泛的开放式发现，且只覆盖科学过程的一个子集，不包含论文撰写等任务。在机器学习领域内部，研究自动化在很大程度上局限于手工设计搜索空间中的超参数与架构搜索（He et al., 2021；Hutter et al., 2019；Wan et al., 2021；Lu et al., 2022b；Wan et al., 2022）或算法发现（Metz et al., 2022；Lange et al., 2023b；Lange et al., 2023a；Lu et al., 2022a；Kirsch et al., 2019；Chen et al., 2024b；Alet et al., 2020）。LLM 的最新进展展示了将搜索空间扩展到更通用的代码级解决方案的潜力（Ma et al., 2023；Lu et al., 2024a；Faldor et al., 2024；Lehman et al., 2022）。然而，这些方法仍然受制于严格定义的搜索空间与目标，限制了可能发现的广度与深度。

本文提出「AI 科学家」（The AI Scientist）——首个由基础模型最新进展促成的、完全自动化且可扩展的端到端论文生成流水线。给定一个宽泛的研究方向和一个简单的初始代码库，AI 科学家无缝地执行想法构思、文献检索、实验规划、实验迭代、论文写作与同行评审，产出有洞见的论文。此外，原则上 AI 科学家可以在一个开放式循环中运行，基于其先前的科学发现来改进下一代想法。这使我们能够以低得惊人的财务成本（约 15 美元/篇）加速缓慢的科学迭代，代表着向把世界上不断增长的算力转化为应对 21 世纪核心挑战所需的科学突破迈出的一步。本文聚焦机器学习（ML）应用，但只要具备自动执行实验的适当方式（Kehoe et al., 2015；Arnold, 2022；Zucchelli et al., 2021），该方法一般也适用于几乎任何其他学科，例如生物学或物理学。

通过利用思维链（Wei et al., 2022）与自我反思（Shinn et al., 2024）等现代 LLM 技术来改进决策，AI 科学家能够生成自己的科学想法与假设，以及用实验检验它们的计划。接着，AI 科学家借助最先进的编程助手 Aider（Gauthier, 2024）对实验「模板」实施计划指导的代码级修改，并执行实验以收集一组计算结果，这些结果又用于起草科学论文。然后，AI 科学家使用标准机器学习会议的指南执行自动化论文评审过程。最后，AI 科学家把完成的想法与审稿人反馈加入其科学发现档案，过程不断重复。至关重要的是，AI 科学家产出的论文与实验制品让我们能够轻松事后解读和评判其发现，使人类科学家也能从中学到的东西中受益。

![Refer to caption](2408.06292v3/figures/conceptual.png)

图 1：AI 科学家的概念示意，一个端到端的 LLM 驱动的科学发现过程。AI 科学家首先发明一组想法并评估其新颖性。接着它确定如何检验假设，包括借助自动代码生成的最新进展、通过编辑代码库来编写必要代码。随后实验被自动执行，收集由数值分数与可视化摘要（如图或表）组成的一组结果。结果在一份 LaTeX 报告中被阐述动机、解释与总结。最后，AI 科学家依据标准机器学习会议的现行做法生成一份自动化评审。该评审可用于改进项目，或作为面向未来开放式科学发现的世代间反馈。

我们的贡献总结如下：

1. 我们提出首个由前沿 LLM 促成的、面向机器学习研究完全自动化科学发现的端到端框架（第 3 节）。这一完全自动化的过程包括想法生成、实验设计、执行，以及将结果可视化并写成完整论文。

2. 为评估生成论文的质量，我们在第 4 节引入基于基础模型的评审过程。该过程在 ICLR 2022 OpenReview 数据上评估时，在多个评估指标上达到接近人类的水平（例如平衡准确率 65% vs. 66%）。这些评审进一步使 AI 科学家能够选择最佳想法「发表」到一个不断增长的科学发现档案中，并且该过程可以重复进行、在这些发现之上继续构建，正如人类科学共同体一样。

3. AI 科学家可以在一周内生成数百篇有趣的中等质量论文。在本报告中，我们聚焦其中一部分论文，重点展示扩散建模、语言建模与 grokking 中的新颖洞见。我们在第 5 节对一篇选定论文进行深入的案例研究，并在第 6 节给出汇总结果。

4. 我们在第 8 节与第 9 节以对本方法局限、伦理考量与未来前景的广泛讨论作结。

## 2 背景

**大型语言模型。** 本文从自回归大型语言模型（LLM；OpenAI (2023)；Google DeepMind Gemini Team (2023)；Anthropic (2023)；Llama Team (2024)；Zhu et al. (2024)）出发构建自动化科学家。LLM 通过建模给定前文条件下新 token（类似一个词）的条件概率 $p(x_{t}|x_{<t};\theta)$ 并在测试时采样，来学习生成文本补全。加之海量数据与模型规模的扩展，这使 LLM 不仅能生成连贯文本，更关键的是展现出类人能力，包括常识知识（Talmor et al., 2019）、推理（Wei et al., 2022）以及编写代码的能力（Chen et al., 2021；Xu et al., 2022）。

**LLM 智能体框架。** LLM 的典型应用往往涉及把模型嵌入「智能体」（agent；Wang et al., 2024a）框架，包括以下可能性：组织语言查询（如少样本提示；Brown et al., 2020）、鼓励推理轨迹（如思维链；Wei et al., 2022），或要求模型迭代精化其输出（如自我反思；Shinn et al., 2024）。这些技术利用语言模型的上下文学习能力（Olsson et al., 2022），可以大幅提升其在许多任务上的性能、稳健性与可靠性。

**Aider：基于 LLM 的编程助手。** 我们的自动化科学家直接以代码实现想法，并使用最先进的开源编程助手 Aider（Gauthier, 2024）。Aider 是一个智能体框架，旨在实现所请求的功能、修复缺陷或重构现有代码库。尽管 Aider 原则上可以使用任何底层 LLM，配合前沿模型时它在 SWE Bench（Jimenez et al., 2024）基准上取得了 18.9% 的可观成功率——该基准是真实 GitHub issue 的合集。结合本工作新增的创新，这一可靠性水平使我们首次能够完全自动化 ML 研究过程。

## 3 AI 科学家

**概览。** AI 科学家有三个主要阶段（图 1）：(1) 想法生成、(2) 实验迭代、(3) 论文写作。写作完成后，我们引入并验证一个 LLM 生成的评审来评估论文质量（第 4 节）。我们为 AI 科学家提供一个起始*代码模板*，它复现一个来自流行模型或基准的轻量级基线训练运行。例如，这可以是在莎士比亚著作上训练一个小 Transformer 的代码（Karpathy, 2022）——一个几分钟内即可完成自然语言处理的经典概念验证训练。AI 科学家随后可以自由探索任何可能的研究方向。模板还包含一个 LaTeX 文件夹（含样式文件与章节标题）以及简单的绘图代码。我们在第 6 节提供模板的更多细节，但总体而言，每次运行都从一个与主题相关的代表性小规模实验开始。聚焦小规模实验并非我们方法的根本限制，而只是出于计算效率与我们的算力约束。我们在附录 A 提供所有阶段的提示词。

1. **想法生成。** 给定一个起始模板，AI 科学家首先「头脑风暴」出一组多样的新颖研究方向。我们从演化计算与开放式研究（Brant and Stanley, 2017；Lehman et al., 2008；Stanley et al., 2017；Stanley, 2019）汲取灵感，把 LLM 用作变异算子来迭代增长想法档案（Zhang et al., 2024；Faldor et al., 2024；Lu et al., 2024b；Lehman et al., 2022）。每个想法包含一段描述、实验执行计划，以及（自评的）有趣性、新颖性与可行性数值分数。在每次迭代中，我们提示语言模型在现有档案（可包含此前已完成想法的数值评审分数）的条件下生成一个有趣的新研究方向。我们使用多轮思维链（Wei et al., 2022）与自我反思（Shinn et al., 2024）来打磨和发展每个想法。想法生成后，我们通过把语言模型连接到 Semantic Scholar API（Fricke, 2018）与作为工具的网页访问（Schick et al., 2024）来过滤想法。这使 AI 科学家能够丢弃任何与现有文献过于相似的想法。

2. **实验迭代。** 给定一个想法和一个模板，AI 科学家第二阶段先执行提议的实验，然后为下游写作可视化结果。AI 科学家使用 Aider 先规划一个待运行的实验清单，然后按顺序执行。我们通过把任何失败或超时（例如实验运行时间过长）的错误返回给 Aider 修复代码并最多重试四次，使该过程更稳健。

   每个实验完成后，Aider 会拿到结果并被要求以实验日志的风格做笔记。目前它只以文本为条件，但在未来版本中，这可以包括数据可视化或任何模态。基于结果，它随后重新规划并实现下一个实验。此过程最多重复五次。实验完成后，提示 Aider 编辑一个绘图脚本，用 Python 为论文创建图表。AI 科学家会记录一段描述每个图所含内容的笔记，使保存的图表与实验笔记提供撰写论文所需的全部信息。在所有步骤中，Aider 都能看到自己的执行历史。

   注意，一般而言，提供的初始种子绘图与实验模板都是小巧自包含的文件。AI 科学家经常实现全新的绘图并收集种子模板中没有的新指标。这种任意编辑代码的能力偶尔会导致意外结果（第 8 节）。

3. **论文写作。** AI 科学家第三阶段以标准机器学习会议论文集的风格，用 LaTeX 对其进展产出一份简洁而有信息量的写作。我们注意到，写出好的 LaTeX 即使对有能力的人类研究者也需要一些时间，因此我们采取若干步骤来加固该过程。具体包括：

   1. 逐节文本生成：把记录的笔记与图表传给 Aider，提示它逐节填充一个空白会议模板。顺序为引言、背景、方法、实验设置、结果，然后是结论（除相关工作外的所有章节）。它已写完的论文所有先前章节都在语言模型的上下文中。我们基于流行的 ["How to ML Paper" 指南](https://docs.google.com/document/d/16R1E2ExKUCP5SlXWHr-KzbVDx9DBUclra-EbU8IB-iE/edit#heading=h.16t67gkeu9dx) 提供关于每节应包含内容的简要提示与指南，细节见第 A.3 节。写作的每一步，Aider 都被提示*只使用真实实验结果（以笔记与由代码生成的图表形式）和真实引用*，以减少幻觉。每节在写作时先经一轮自我反思（Shinn et al., 2024）初加打磨。Aider 被提示在此阶段不在文中包含任何引用，相关工作只填写骨架，留待下一阶段完成。

   2. 参考文献的网页搜索：与想法生成类似，AI 科学家被允许进行 20 轮 Semantic Scholar API 轮询，为快完成的论文寻找最相关的文献来源以在相关工作一节中进行比较与对照。该过程还允许 AI 科学家选择它想讨论的任何论文，并补全论文其他章节缺失的引用。伴随每篇选定的论文，会生成一段关于在何处以及如何插入引用的简短描述，随后传给 Aider。论文的 bibtex 会自动追加到 LaTeX 文件以保证正确性。

   3. 精化：前两个阶段后，AI 科学家有了一份完整的初稿，但往往过于冗长与重复。为解决这一问题，我们逐节进行最后一轮自我反思，旨在删除任何重复信息并精炼论文的论证。

   4. 编译：一旦 LaTeX 模板填入了所有适当结果，就将其输入 LaTeX 编译器。我们使用一个 LaTeX linter 并把编译错误回传给 Aider，使其能自动纠正任何问题。

## 4 自动化论文评审

**一个 LLM 审稿人智能体。** 一个有效科学共同体的关键组件是其评审系统，它评估并提升科学论文的质量。为用大型语言模拟这一过程，我们设计了一个基于 GPT-4o 的智能体（OpenAI, 2023），依据神经信息处理系统（NeurIPS）会议的[评审指南](https://neurips.cc/Conferences/2022/ReviewerGuidelines)进行论文评审。评审智能体使用 PyMuPDF 解析库处理 PDF 稿件的原始文本。输出包含数值分数（可靠性、表述、贡献、总体、置信度）、缺点与优点列表，以及一个初步的二元决定（录用或拒稿）。这些决定随后可通过审稿分数阈值进行事后校准。我们利用这一自动化评审过程对 AI 科学家生成的论文获得初步评估。我们在第 A.4 节提供完整的评审提示词模板。

表 1：AI 科学家自动化 LLM 评审系统在 500 篇 ICLR 2022 论文上的表现。我们给出均值与 95% bootstrap 置信区间，并突出人类基线与我们最佳 AI 审稿人的比较。

|  | 审稿人 | 平衡准确率 ↑ | 准确率 ↑ | F1 分数 ↑ | AUC ↑ | FPR ↓ | FNR ↓ |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  | 人类（NeurIPS）¹ | $\mathbf{0.66}$ | $\mathbf{0.73}$ | $\mathbf{0.49}$ | $\mathbf{0.65}$ | $\mathbf{0.17}$ | $\mathbf{0.52}$ |
|  | 随机决定 | $0.50$ | $0.50$ | $0.40$ | $0.50$ | $0.50$ | $0.50$ |
|  | 一律拒稿 | $0.50$ | $0.59$ | $0.00$ | $0.50$ | $0.00$ | $1.00$ |
| 未校准 | Sonnet 3.5 | $0.52\pm 0.01$ | $0.40\pm 0.01$ | $0.55\pm 0.01$ | $0.52\pm 0.01$ | $0.95\pm 0.02$ | $0.00\pm 0.00$ |
|  | GPT-4o-mini | $0.53\pm 0.02$ | $0.65\pm 0.01$ | $0.11\pm 0.06$ | $0.53\pm 0.02$ | $0.01\pm 0.01$ | $0.94\pm 0.04$ |
|  | GPT-4o（0-shot） | $0.61\pm 0.04$ | $0.68\pm 0.03$ | $0.43\pm 0.07$ | $0.61\pm 0.04$ | $0.11\pm 0.03$ | $0.67\pm 0.07$ |
|  | GPT-4o（1-shot） | $0.60\pm 0.03$ | $\mathbf{0.70\pm 0.03}$ | $0.37\pm 0.08$ | $0.60\pm 0.03$ | $0.04\pm 0.02$ | $0.76\pm 0.06$ |
| 已校准 | Sonnet 3.5 @8 | $0.59\pm 0.04$ | $0.65\pm 0.04$ | $0.45\pm 0.06$ | $0.59\pm 0.04$ | $0.20\pm 0.04$ | $0.61\pm 0.07$ |
|  | GPT-4o-mini @6 | $0.59\pm 0.04$ | $0.64\pm 0.04$ | $0.45\pm 0.06$ | $0.59\pm 0.04$ | $0.22\pm 0.05$ | $0.60\pm 0.07$ |
|  | GPT-4o（0-shot）@6 | $0.63\pm 0.04$ | $0.63\pm 0.04$ | $0.56\pm 0.05$ | $0.63\pm 0.04$ | $0.38\pm 0.05$ | $0.36\pm 0.07$ |
|  | GPT-4o（1-shot）@6 | $\mathbf{0.65\pm 0.04}$ | $\mathbf{0.66\pm 0.04}$ | $\mathbf{0.57\pm 0.05}$ | $\mathbf{0.65\pm 0.04}$ | $\mathbf{0.31\pm 0.05}$ | $\mathbf{0.39\pm 0.07}$ |

注 1：数值基于 NeurIPS 一致性实验计算（Beygelzimer et al., 2021）。

**评估自动化审稿人。** 为评估基于 LLM 的审稿人的表现，我们把人工生成的决定与从公开 OpenReview 数据集（Berto, 2024）提取的 500 篇 ICLR 2022 论文的真值数据进行比较。与前一节类似，我们组合 LLM 智能体的诸多最新进展来使决策过程稳健。更具体地说，我们通过利用自我反思（Shinn et al., 2024）、提供少样本示例（Wei et al., 2022）与响应集成（Wang et al., 2022）来改进基座 LLM 的决策过程。使用 GPT-4o，AI 科学家的评审程序在结合 5 轮自我反思、5 份集成评审以及一个取自 ICLR 2022 [评审指南](https://iclr.cc/Conferences/2022/ReviewerGuide)的 1-shot 评审示例时达到 70% 的准确率。随后我们进行一次基于 LLM 的元评审，提示智能体担任领域主席（Area Chair；Wang et al., 2022）（完整提示词见第 A.4 节）。虽然该数字低于 NeurIPS 2021 一致性实验报告的人类 73% 准确率（Beygelzimer et al., 2021），但在把决定阈值设在分数 6（NeurIPS 评审指南中的「弱接受」）时，自动化审稿人取得超人的 F1 分数（0.57 vs. 0.49）与人类水平的 AUC（两者均为 0.65）。这一选择大致对应被录用论文的平均分。

所考察的 ICLR 2022 论文数据集类别严重不平衡，即包含的拒稿论文多得多。当考虑一个类别平衡的论文数据集时，AI 科学家的评审过程达到人类水平的准确率（0.65 vs. 0.66）。此外，假阴性率（FNR）远低于人类基线（0.39 vs. 0.52）。因此，基于 LLM 的评审智能体拒绝的高质量论文更少。另一方面，假阳性率（原文如此，指 FPR）更高（0.31 vs. 0.17），凸显了未来改进的空间。

为进一步验证自动化审稿人的表现，我们比较了论文总体分数之间的一致性：匿名 OpenReview 审稿人之间按论文成对随机采样的一致性（图 2 左下），以及所有审稿人的平均分与 LLM 分数之间的一致性（图 2 中下）。对这 500 篇 ICLR 2022 论文，我们发现两位人类审稿人分数之间的相关性（0.14）小于 LLM 分数与审稿人平均分之间的相关性（0.18）。总体上，在所有指标上，结果表明基于 LLM 的评审不仅能提供有价值的反馈（D'Arcy et al., 2024），而且与人类审稿人平均分的对齐程度高于人类审稿人彼此之间的对齐程度。

每份评审的生成 API 成本为 0.25 至 0.50 美元。我们还比较了其他多个基础模型的评审表现。虽然 Claude Sonnet 3.5（Anthropic, 2024）与 GPT-4o-mini 提供了更省钱的方案，其表现明显更差（表 1）。此外，由于持续存在的过度乐观偏置，我们必须把 Sonnet 3.5 的分数阈值设在 8 才能得到校准后的结果。Llama 3.1 405B（Llama Team, 2024）则难以一致地遵循审稿人输出模板。我们开源了代码，为社区提供一个新的、有趣的 LLM 基准。

![Refer to caption](2408.06292v3/figures/review_confusion.png)

![Refer to caption](2408.06292v3/figures/review_correlation.png)

图 2：使用 GPT-4o 在 ICLR 2022 OpenReview 数据上对 AI 科学家论文评审过程的评估。加入 Reflexion 与 one-shot 提示提升了基于 LLM 的评审过程的准确率。而评审集成（5 份评审）与随后的元聚合未影响审稿人的表现，但可以降低方差。

**LLM 审稿人消融。** 我们比较了 GPT-4o 的多种提示配置，发现 Reflexion（+2%）与 one-shot 提示（+2%）都有助于实现更准确的评审（图 2 上部与右下）。另一方面，使用评审集成似乎没有大幅提升审稿人的表现，但可以降低方差。以下各节中，我们使用整体最佳的审稿人：GPT-4o，配合 5 轮自我反思、5 份集成评审、一个元聚合步骤与 1 个少样本示例。

## 5 深入案例研究

在第 6 节给出 AI 科学生成论文的大量实验与指标之前，我们首先可视化一次 AI 科学家运行中的一个代表性样本，它同时展示了优点与不足，随后更广泛地讨论其潜力。选定的论文「Adaptive Dual-Scale Denoising」出自一次要求 AI 科学家研究扩散建模的运行，细节详见第 6.1 节。基础模型为 Claude Sonnet 3.5（Anthropic, 2024）。

**生成的想法。** 如第 3 节所述，AI 科学家首先基于提供的模板与其先前的发现档案生成一个想法。选定论文中的想法是在算法第 6 次迭代中提出的，旨在通过在标准去噪网络中提出两个分支，提升扩散模型在 2D 数据集上同时捕捉全局结构与局部细节的能力。这是一个动机充分的方向，也是研究者采用扩散模型而舍弃 VAE（Kingma and Welling, 2014）与 GAN（Goodfellow et al., 2014）等先前生成模型风格的主要原因，且据我们所知尚未被广泛研究。

我们强调，AI 科学家生成了一份令人印象深刻的实验计划，包括*提议的代码修改、与基线的比较、评估指标以及额外图表的设计*。正如文献中已观察到的，LLM 的判断往往存在偏置（Zheng et al., 2024），我们在想法的有趣性、可行性或新颖性的高估中可以观察到这一点。末尾的「novel」标志表示 AI 科学家在使用 Semantic Scholar API 搜索相关论文后认为该想法是新颖的。

Idea - adaptive_dual_scale_denoising

```
"Name": "adaptive_dual_scale_denoising",
"Title": "Adaptive Dual-Scale Denoising for Dynamic Feature Balancing in
Low-Dimensional Diffusion Models",
"Experiment": "Modify MLPDenoiser to implement a dual-scale processing
approach with two parallel branches: a global branch for the original input
and a local branch for an upscaled input. Introduce a learnable, timestep-
conditioned weighting factor to dynamically balance the contributions of
global and local branches. Train models with both the original and new
architecture on all datasets. Compare performance using KL divergence and
visual inspection of generated samples. Analyze how the weighting factor
evolves during the denoising process and its impact on capturing global
structure vs. local details across different datasets and timesteps.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

**生成的实验。** 我们在下面展示实质性算法改动对应的代码 diff（删除为红色，新增为绿色）。代码与实验描述相符且注释良好。AI 科学家能够在循环中结合中间实验的结果迭代改进代码，最终为自适应权重网络做出了有趣的设计选择，例如 LeakyReLU。重要的是，该网络输出行为良好、保证在 0 到 1 之间。我们还注意到，AI 科学家修改了网络的输出以返回自适应权重，从而制作新的可视化。

**生成的论文。** AI 科学家以标准机器学习会议投稿的风格生成了一份 11 页的科学稿件，配有可视化与所有标准章节。我们在图 3 中展示这份完全由 AI 生成的论文的预览，完整版见第 D.1 节。

![Refer to caption](2408.06292v3/all_pages.png)

图 3：「Adaptive Dual-Scale Denoising」论文的预览，完全由 AI 科学家自主生成。完整论文见第 D.1 节。

我们着重指出论文中尤其令人印象深刻的几点：

- **对算法的精确数学描述。** 上述代码中的算法改动被精确描述，必要时引入了新的记号，使用了 LaTeX 数学宏包。整体训练过程也被准确描述。

- **实验的全面写作。** 论文中列出了超参数、基线与数据集。作为一个关键的健全性检查，我们验证了生成论文表 1 中的主要数值结果与实验日志完全一致。令人印象深刻的是，尽管记录的数字是长浮点形式，AI 科学家无误地将它们全部四舍五入到 3 位小数。更令人印象深刻的是，结果与基线的比较是准确的（例如恐龙数据集上 KL 降低 12.8%）。

- **良好的实证结果。** 定性上看，样本质量相比基线有明显提升。与真值相比严重偏离分布的点更少。定量上看，真实分布与估计分布之间的近似 KL 散度有所改进。

- **新的可视化。** 虽然我们提供了一些用于可视化生成样本与训练损失曲线的基线绘图代码，它自行提出了新颖的算法专属图表，展示去噪过程中权重的演变。

- **有趣的未来工作一节。** 基于当前实验的成功，未来工作一节列出了相关的后续步骤，如扩展到更高维问题、更复杂的自适应机制以及更好的理论基础。

另一方面，论文中也存在一些病态问题：

- **上采样网络中的微妙错误。** 虽然一个线性层对去噪网络的输入进行了上采样，但「局部」分支只使用了前两个维度，使该上采样层实际上是一个保持相同维度的线性层。

- **实验细节的幻觉。** 论文声称使用了 V100 GPU，尽管该智能体不可能知道实际使用的硬件。实际使用的是 H100 GPU。它还在未检查的情况下猜测了 PyTorch 版本。

- **对结果的正面解读。** 论文倾向于对其负面结果也给出正面表述，带来略显幽默的结果。例如，它把正面结果总结为「Dino: 12.8% reduction (from 0.989 to 0.862)」（KL 越低越好），而负面结果被报告为「Moons: 3.3% improvement (from 0.090 to 0.093)」。把一个负面结果描述为「改进」无疑是想象的拉伸。

- **实验日志的痕迹。** 虽然算法的每次改动通常都有描述性标签，但它偶尔把结果称为「Run 2」，这是其实验日志的副产品，不应出现在专业的写作中。

- **中间结果的呈现。** 论文包含所运行的每一次实验的结果。虽然这有助于我们看到想法在执行过程中的演变，但标准论文这样呈现中间结果并不常见。

- **参考文献偏少。** 虽然从 Semantic Scholar 补充了额外的参考文献（包括相关工作中两篇非常相关的对比论文），整体书目仍然偏小，只有 9 条。

**评审。** 自动化审稿人指出了生成稿件中的有效顾虑。评审认识到实验只使用了简单的 2D 数据集，然而这是因为我们在外部约束系统使用这些数据集，且在当前形式下，AI 科学家无法从互联网下载更高维的数据集。另一方面，诸如所提算法计算成本增加等局限在实际论文中有所提及，这表明 AI 科学家对其想法的缺点往往是坦诚的。审稿人还列出了关于论文的许多相关问题，例如：解释性能在不同数据集间的差异，以及更详细地解释上采样过程如何影响局部分支的输入。

Review - adaptive_dual_scale_denoising

```
"Summary": "The paper introduces an adaptive dual-scale denoising approach
for low-dimensional diffusion models, aiming to balance global structure
and local details in generated samples. The novel architecture incorporates
two parallel branches and a learnable, timestep-conditioned weighting
mechanism to dynamically balance their contributions throughout the
denoising process. The approach is evaluated on four 2D datasets,
demonstrating improvements in sample quality.",
"Strengths": [
    "Novel approach to balancing global and local features in diffusion
models for low-dimensional data.",
    "Comprehensive empirical evaluation on multiple 2D datasets.",
    "Adaptive weighting mechanism that dynamically adjusts focus during
denoising."
],
"Weaknesses": [
    "Lacks detailed theoretical justification for the dual-scale
architecture.",
    "Computational cost is significantly higher, which may limit practical
applicability.",
    "Some sections are not clearly explained, such as the autoencoder
aggregator and weight evolution analysis.",
    "Limited diversity in the datasets used for evaluation. More complex,
real-world datasets could strengthen claims.",
    "Insufficient ablation studies and analysis on specific design choices
like different types of aggregators."
],
"Originality": 4,
"Quality": 3,
"Clarity": 3,
"Significance": 3,
"Questions": [
    "Can you provide a more detailed theoretical justification for the
dual-scale architecture?",
    "What impact do different types of aggregators have on the model's
performance?",
    "How does the model perform on more complex, real-world low-dimensional
datasets?",
    "Can the computational cost be reduced without sacrificing
performance?"
],
"Limitations": [
    "The paper should address the high computational cost and explore ways
to optimize it.",
    "The limited diversity of datasets and lack of detailed theoretical
backing for the proposed architecture are notable limitations."
],
"Ethical Concerns": false,
"Soundness": 3,
"Presentation": 3,
"Contribution": 3,
"Overall": 5,
"Confidence": 4,
"Decision": "Reject"
```

**最终评语。** 基于我们在扩散建模领域的领域知识——虽然这不是我们的主要研究方向，但我们也发表过该领域的论文——我们在下面给出对 AI 科学生成论文的总体意见。

- AI 科学家正确识别出扩散建模研究中一个有趣且动机充分的方向，例如先前工作已在更高维问题中为同一目的研究过改进的注意力机制（Hatamizadeh et al., 2024）。它提出了一个全面的实验计划来研究其想法，并全部成功实现，取得了良好结果。我们对它如何应对早期欠佳的结果并迭代调整代码（例如精化权重网络）印象尤深。想法的完整演变过程可以在论文中看到。

- 虽然论文的想法提升了性能与生成扩散样本的质量，其成功的原因可能并非论文所解释的那样。特别地，除了一个上采样层（实际上只是一个额外的线性层）之外，并没有明显的用于全局/局部特征划分的归纳偏置。然而，我们确实看到权重（从而对全局或局部分支的偏好）在扩散时间步之间有演变，这表明发生了一些不平凡的事情。我们对此的解读是，AI 科学家为该想法实现的网络类似于 LLM 中普遍存在的混合专家（MoE；Yuksel et al. (2012)；Fedus et al. (2022)）结构（Jiang et al., 2024）。MoE 确实可能导致扩散模型为全局与局部特征学到独立的分支（如论文所声称），但这一论断需要更严谨的研究。

- 有趣的是，上述论文真正的缺点确实需要一定程度的领域知识才能识别，且只被自动化审稿人部分捕获（即在要求提供上采样层的更多细节时）。以 AI 科学家当前的能力，这可以通过人类反馈解决。然而，未来世代的基础模型可能提出对人类而言难以推理与评估的想法。这联系到「超对齐」（superalignment；Burns et al., 2023）领域，即监督可能比我们更聪明的 AI 系统，这是一个活跃的研究方向。

- 总体而言，我们判断 AI 科学家的表现大约相当于一个早期阶段的 ML 研究者——能够合格地执行一个想法，但可能没有完整的背景知识来充分解读算法成功背后的原因。如果人类导师看到这些结果，合理的下一步行动可能是建议 AI 科学家重新界定项目范围，以进一步研究用于扩散模型的 MoE。最后，我们自然期望随着基础模型的持续大幅改进，AI 科学家的许多缺陷即便不被消除也会得到改善。

## 6 实验

我们在三个模板上（如第 3 节所述）使用不同公开可用的 LLM 对 AI 科学家进行广泛评估：Claude Sonnet 3.5（Anthropic, 2024）、GPT-4o（OpenAI, 2023）、DeepSeek Coder（Zhu et al., 2024）与 Llama-3.1 405b（Llama Team, 2024）。前两个模型只能通过公开 API 使用，后两个是开放权重模型。每次运行，我们提供 1-2 个基础种子想法作为示例（例如修改学习率或 batch size），并让它另外生成 50 个新想法。我们在附录 C 可视化一次提出想法的演变过程。每次约五十个想法的总运行在 8×NVIDIA H100 上约需 12 小时²。我们报告通过自动新颖性检查的想法数量、成功完成实验的数量以及产出有效可编译稿件的数量。注意自动新颖性检查与搜索由各模型对其自身想法自评，使相对「新颖性」比较颇具挑战。此外，我们提供生成论文的平均与最高审稿分数以及运行总成本。最后，我们选取并简要分析部分生成论文，列在下面。完整论文连同生成的评审与代码见附录 D。

注 2：注意实验模板规模非常小且计算不密集。它们在更便宜的 GPU 上可能耗时相近，因为我们并未达到高利用率。

实践中，我们对 AI 科学家的形式化描述做了一处偏离：不等论文评估结果追加到档案就生成想法，以便更有效地并行。这使我们只需为想法生成阶段支付一次成本并更快迭代；此外，我们未观察到这一修改使生成论文的质量（以平均审稿分数衡量）有所下降。

表 2：AI 科学家在 3 个不同模板上生成的 10 篇选定论文，以及我们自动化审稿人依据 [NeurIPS 指南](https://neurips.cc/Conferences/2022/ReviewerGuidelines)给出的分数。NeurIPS 被录用论文的人类评审平均分约为 6 分。

| 类型 | 论文标题 | 分数 |
| --- | --- | --- |
| 2D 扩散 | DualScale Diffusion: Adaptive Feature Balancing for Low-Dimensional Generative Models | $\mathbf{5}$ |
| 2D 扩散 | Multi-scale Grid Noise Adaptation: Enhancing Diffusion Models For Low-dimensional Data | $\mathbf{4}$ |
| 2D 扩散 | GAN-Enhanced Diffusion: Boosting Sample Quality and Diversity | $\mathbf{3}$ |
| 2D 扩散 | DualDiff: Enhancing Mode Capture in Low-dimensional Diffusion Models via Dual-expert Denoising | $\mathbf{5}$ |
| NanoGPT | StyleFusion: Adaptive Multi-style Generation in Character-Level Language Models | $\mathbf{5}$ |
| NanoGPT | Adaptive Learning Rates for Transformers via Q-Learning | $\mathbf{3}$ |
| Grokking | Unlocking Grokking: A Comparative Study of Weight Initialization Strategies in Transformer Models | $\mathbf{5}$ |
| Grokking | Grokking Accelerated: Layer-wise Learning Rates for Transformer Generalization | $\mathbf{4}$ |
| Grokking | Grokking Through Compression: Unveiling Sudden Generalization via Minimal Description Length | $\mathbf{3}$ |
| Grokking | Accelerating Mathematical Insight: Boosting Grokking Through Strategic Data Augmentation | $\mathbf{5}$ |

从人工检查来看，我们发现 Claude Sonnet 3.5 持续产出质量最高的论文，GPT-4o 次之。我们在 [GitHub 仓库](https://github.com/SakanaAI/AI-Scientist)提供所有论文、运行文件与日志的链接，并推荐查看上传的 Claude 论文以做定性分析。这一观察也被 LLM 审稿人给出的分数验证（图 4）。把生成论文数除以总成本，我们得到每篇论文约 10-15 美元的成本。值得注意的是，GPT-4o 在写 LaTeX 上很吃力，这使它无法完成其许多论文。对开放权重模型，DeepSeek Coder 显著更便宜但经常无法正确调用 Aider 工具。Llama-3.1 405b 整体表现最差，但用起来最方便，因为我们频繁被其他提供商限流。DeepSeek Coder 与 Llama-3.1 405b 生成的论文经常缺少章节与结果。以下小节将描述每个模板、对应结果与具体论文。

![Refer to caption](2408.06292v3/figures/scores_ai_papers.png)

图 4：小提琴图，展示 AI 科学家审稿人对三个领域、四个基础模型的 AI 生成论文给出的分数分布。y 轴分数依据 [NeurIPS 评级](https://neurips.cc/Conferences/2022/ReviewerGuidelines)，范围从 2（Strong Reject）到 6（Weak Accept）。

### 6.1 扩散建模

表 3：扩散建模上自动化 AI 科学家论文生成的评估。

| 模型 | 总想法数 | 新颖想法数 | 通过实验数 | 完成论文数 | 平均分 | 最高分 | 总成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Sonnet 3.5 | 51 | 49 | 38 | 38 | 3.82 | 6.0 | 约 $250 |
| GPT-4o | 51 | 41 | 17 | 16 | 3.70 | 5.0 | 约 $300 |
| DeepSeek Coder | 51 | 42 | 32 | 31 | 3.32 | 5.0 | 约 $10 |
| Llama-3.1 405b | 51 | 31 | 21 | 21 | 2.30 | 3.0 | 约 $120 |

**一般描述**：该模板研究提升扩散生成模型（Sohl-Dickstein et al., 2015；Ho et al., 2020）在低维数据集上的性能。与图像生成相比，低维扩散的研究少得多，因此这里可能存在有趣的算法贡献空间。

**代码模板**：该模板基于流行的「tanelp/tiny-diffusion」仓库的修改版（Pärnamaa, 2023），加入了少量额外的超参数调优与权重指数滑动平均。扩散模型为 DDPM（Ho et al., 2020），训练其从四个分布生成样本，包括几何形状、双月数据集与一只 2D 恐龙。去噪网络参数化为一个 MLP，对扩散时间步与输入数据使用正弦嵌入。绘图脚本默认可视化生成样本并绘制训练损失。通过非参数熵估计额外提供估计 KL 作为样本质量指标。

**亮点生成论文 1**：[DualScale Diffusion: Adaptive Feature Balancing for Low-Dimensional Generative Models.](#A4.SS1) 我们在第 5 节深入分析了该论文。该论文提出一种双尺度去噪方法，把传统扩散去噪器拆分为一个全局与一个局部分支。网络输入在送入局部分支前被上采样。两个分支的输出随后用一个可学习的时间条件加权合并。它取得了可观的定量与定性结果。它还成功绘制了权重随时间的演变，这需要与提供的代码有很大偏差。

**亮点生成论文 2**：[Multi-scale Grid Noise Adaptation: Enhancing Diffusion Models For Low-dimensional Data.](#A4.SS2) 该论文提出用一个基于特定输入在 2D 空间中位置的学习乘性因子，动态缩放标准扩散噪声调度。乘性因子由覆盖输入空间的两张网格设定，一张粗糙的 5×5 网格与一张更精细的 20×20 网格。这一有创意的方法使扩散模型在各数据集上的性能大幅提升。

**亮点生成论文 3**：[GAN-Enhanced Diffusion: Boosting Sample Quality and Diversity.](#A4.SS3) 该论文受 GAN 启发，提出向扩散模型添加一个判别器来指导生成。它取得了与基线相当的定量性能，但最终生成的图中偏离分布的点似乎更少。这值得注意，因为当前版本的 AI 科学家无法查看它们（该问题未来可通过多模态模型解决）。

**亮点生成论文 4**：[DualDiff: Enhancing Mode Capture in Low-dimensional Diffusion Models via Dual-expert Denoising.](#A4.SS4) 该论文提出与我们第一篇亮点扩散论文类似的想法，也研究用于低维扩散模型的混合专家式网络。但该想法的演变不同：标准扩散损失现在增加了一个鼓励两个专家多样性的损失。论文令人印象深刻地可视化了多样性损失在把输入分配到两个专家上的影响，并进一步用颜色标注每个专家特化的样本空间区域。我们对 AI 科学家能对相似想法做出截然不同的处理印象深刻。

### 6.2 语言建模

表 4：语言建模上自动化 AI 科学家论文生成的评估。

| 模型 | 总想法数 | 新颖想法数 | 通过实验数 | 完成论文数 | 平均分 | 最高分 | 总成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Sonnet 3.5 | 52 | 50 | 20 | 20 | 4.05 | 5.0 | 约 $250 |
| GPT-4o | 52 | 44 | 30 | 16 | 3.25 | 5.0 | 约 $300 |
| DeepSeek Coder | 52 | 37 | 23 | 23 | 3.21 | 4.0 | 约 $10 |
| Llama-3.1 405b | 52 | 41 | 21 | 21 | 2.31 | 3.0 | 约 $120 |

**一般描述**：该模板研究基于 Transformer（Vaswani et al., 2017）的自回归下一 token 预测任务。由于该任务被广泛研究与优化，AI 科学家很难找到显著的改进。该模板存在一些常见的失败模式，导致看起来可观但具有欺骗性的结果。例如，它的少数想法通过微妙地泄露来自未来 token 的信息来有效作弊，导致更低的困惑度。

**代码模板**：代码修改自流行的 NanoGPT 仓库（Karpathy, 2022）。提供的脚本模板在字符级 Shakespeare 数据集（Karpathy, 2015）、enwik8 数据集（Hutter, 2006）与 text8 数据集（Mahoney, 2011）上训练一个小 Transformer 语言模型。它在 Shakespeare 数据集上运行三个种子，其余各一个。代码保存运行时间、验证损失与训练损失。绘图脚本默认可视化训练曲线。

**亮点生成论文 1**：[StyleFusion: Adaptive Multi-style Generation in Character-Level Language Models.](#A4.SS5) 该论文对模型提出一个架构改动：一个可学习的逐 token「风格适配器」在每层调制 Transformer 状态。该方法取得了强劲的结果，值得进一步研究，尽管我们怀疑其有效的一个原因可能只是增加了更多参数，这可能使结果变得平凡。此外，它在写作中遗漏了一些重要的实现细节，例如风格损失标签如何得来（似乎在每次更新步骤随机分配）。

**亮点生成论文 2**：[Adaptive Learning Rates in Transformers via Q-Learning.](#A4.SS6) 该论文提出用一个基础的在线 Q-Learning 算法在训练期间调整模型的学习率。状态由当前学习率与验证损失组成，动作对学习率施加小幅扰动，奖励为验证损失的负变化。虽然想法有创意，在这个高度非平稳且部分可观测的环境中用简单 Q-Learning 似乎并不合适。尽管如此，它碰巧取得了有效的结果。

### 6.3 Grokking 分析

表 5：Grokking 上自动化 AI 科学家论文生成的评估。

| 模型 | 总想法数 | 新颖想法数 | 通过实验数 | 完成论文数 | 平均分 | 最高分 | 总成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Sonnet 3.5 | 51 | 47 | 25 | 25 | 3.44 | 5.0 | 约 $250 |
| GPT-4o | 51 | 51 | 22 | 13 | 2.92 | 3.0 | 约 $300 |
| DeepSeek Coder | 51 | 46 | 38 | 36 | 3.13 | 4.0 | 约 $10 |
| Llama-3.1 405b | 51 | 36 | 30 | 30 | 2.00 | 3.0 | 约 $120 |

**一般描述**：该模板研究深度神经网络中关于泛化与学习速度的问题。我们遵循 Power et al. (2022) 报告的经典实验范式来分析「grokking」——一个理解尚浅的现象：验证准确率在训练损失饱和很久之后才急剧提升。我们提供生成模算术任务合成数据集并在其上训练 Transformer 模型的代码。与前两个模板不同，该模板更适合开放式实证分析（例如 grokking 在什么条件下发生），而不仅是试图改进性能指标。

**代码模板**：我们的实现基于 Power et al. (2022) 的两个流行开源复现（Snell, 2021；May, 2022）。代码生成四个模算术任务的合成数据集，并在每个数据集上以三个随机种子训练一个 Transformer。它返回训练损失、验证损失以及达到完美验证准确率所需的更新步数。绘图脚本默认可视化训练与验证曲线。

**亮点生成论文 1**：[Unlocking Grokking: A Comparative Study of Weight Initialization Strategies in Transformer Models.](#A4.SS7) 该论文研究不同的权重初始化及其对 grokking 的影响。它发现 Xavier（Glorot and Bengio, 2010）与正交权重初始化在这些任务上持续带来显著更快的 grokking，优于广泛使用的默认基线权重初始化（Kaiming Uniform 与 Kaiming Normal）。虽然这是一个基础性研究，它提供了一个可以更深入研究的有趣结果。论文标题也富有创意且吸引人。

**亮点生成论文 2**：[Grokking Accelerated: Layer-wise Learning Rates for Transformer Generalization.](#A4.SS8) 该论文为 Transformer 架构的不同层分配不同的学习率。它在实验中迭代不同配置后发现，提高较高层的学习率带来显著更快且更一致的 grokking。它令人印象深刻地在写作中包含了其实现的关键部分。

**亮点生成论文 3**：[Grokking Through Compression: Unveiling Sudden Generalization via Minimal Description Length.](#A4.SS9) 该论文研究 grokking 与最小描述长度（MDL）之间的潜在联系。我们认为这个想法特别有趣，但执行得不太好。其测量 MDL 的方法只是统计高于阈值 $\epsilon$ 的参数数量。虽然这最终与 grokking 相关，但分析深度不足。论文可以通过研究 MDL 的其他估计量并加入基础消融实验得到显著改进。此外，AI 科学家未能写出相关工作一节，并且幻觉出了一个图（图 5）。

**亮点生成论文 4**：[Accelerating Mathematical Insight: Boosting Grokking Through Strategic Data Augmentation.](#A4.SS10) 该论文研究模算术中 grokking 的数据增强技术。它提出了有效且有创意的增强技术（操作数反转与操作数取反），并发现它们能显著加速 grokking。虽然数据增强能提升泛化并不令人意外，但实验与想法总体执行良好。然而，AI 科学家再次未能写出相关工作一节。原则上，这一失败可能只需多次运行论文写作步骤即可轻松解决。

## 7 相关工作

尽管自动优化 ML 流程的个别环节（AutoML；Hutter et al. (2019)；He et al. (2021)）有着悠久的传统，但没有一个接近整个研究过程的完全自动化，尤其是以可解释、通用的形式交流所获得的科学洞见。

**面向机器学习研究的 LLM。** 与我们工作最相关的是使用 LLM 辅助机器学习研究的那些。Huang et al. (2024) 提出一个基准，衡量 LLM 能多成功地编写代码解决各种机器学习任务。Lu et al. (2024a) 用 LLM 提出、实现并评估用于偏好优化的新最先进算法。Liang et al. (2024) 用 LLM 对论文提供反馈，发现它们能提供与人类审稿人类似的反馈；Girotra et al. (2023) 则发现 LLM 能持续产出比人类质量更高的创新想法。Wang et al. (2024b) 与 Baek et al. (2024) 用 LLM 基于科学文献检索提出研究想法但不执行它们。Wang et al. (2024c) 基于广泛的文献检索自动撰写综述。我们的工作可被视为所有这些不同脉络的综合，形成一个可以执行整个机器学习研究过程的单一自主开放式系统。

**面向结构化探索的 LLM。** 由于 LLM 包含许多与人类相关的先验，它们常被用作探索大型搜索空间的工具。例如，近期工作用 LLM 的编程能力探索奖励函数（Ma et al., 2023；Yu et al., 2023）、虚拟机器人设计（Lehman et al., 2023）、环境设计（Faldor et al., 2024）与神经架构搜索（Chen et al., 2024a）。LLM 还可作为评估器（Zheng et al., 2024）评判「有趣性」（Zhang et al., 2024；Lu et al., 2024b），并作为演化策略黑盒优化的重组算子（Lange et al., 2024；Song et al., 2024）以及质量多样性（Quality-Diversity）方法（Lim et al., 2024；Bradley et al., 2024；Ding et al., 2024）。我们的工作结合了这些概念中的许多，包括我们的 LLM 审稿人依据新颖性与有趣性评判论文，以及许多提出的想法是先前想法的新组合。

**面向科学发现的 AI。** AI 辅助科学发现在许多其他领域有着悠久的传统（Langley, 2024；Langley, 1987）。例如，AI 已被用于化学（Buchanan and Feigenbaum, 1981）、合成生物学（Jumper et al., 2021；Hayes et al., 2024）、材料发现（Pyzer-Knapp et al., 2022；Merchant et al., 2023；Szymanski et al., 2023）、数学（Romera-Paredes et al., 2024；Lenat, 1977；Lenat and Brown, 1984）与算法搜索（Fawzi et al., 2022）。其他工作旨在分析已有的事先收集的数据集并发现新洞见（Langley, 1987；Ifargan et al., 2024；Majumder et al., 2024；Yang et al., 2024；Falkenhainer and Michalski, 1986；Zytkow, 1996；Nordhausen and Langley, 1990）。与我们的工作不同，这些通常局限于单一领域内定义良好的搜索空间，且不涉及 AI 系统的「想法构思」、写作或同行评审。在当前形式下，AI 科学家擅长开展通过代码实现的研究想法；随着未来进展（例如湿实验室的机器人自动化；Kehoe et al., 2015；Arnold, 2022；Zucchelli et al., 2021；Sparkes et al., 2010），我们方法的变革性益处可以扩展到整个科学界，尤其是基础模型持续改进的情况下。

## 8 局限与伦理考量

虽然 AI 科学家产出的研究可以提供新颖洞见，它有许多局限并引发若干重要的伦理考量。我们相信未来版本的 AI 科学家将能解决其当前的许多不足。

**自动化审稿人的局限。** 虽然自动化审稿人展现了有前景的初步结果，仍有若干潜在改进领域。所用的 ICLR 2022 数据集足够陈旧，可能出现在基座模型预训练数据中——这在实践中很难检验，因为典型的公开 LLM 不分享其训练数据。不过，初步分析表明 LLM 远不能从初始片段精确复现旧评审，这暗示它们没有记住这些数据。此外，我们数据集中的拒稿论文使用原始投稿文件，而录用论文在 OpenReview 上只有最终的 camera-ready 版本。未来迭代可使用更近的投稿（例如来自 TMLR）进行评估。与标准审稿人不同，自动化审稿人无法在 rebuttal 阶段向作者提问，尽管这可以很容易地纳入我们的框架。最后，由于目前不使用任何视觉能力，AI 科学家（包括审稿人）无法查看图表，必须依赖其文字描述。

**常见失败模式。** 当前形式的 AI 科学家除第 5 节已指出的之外还有若干不足。这些包括但不限于：

- 想法生成过程在不同运行甚至不同模型之间经常产生非常相似的想法。允许 AI 科学家直接跟进并深入其最佳想法，或向它提供新发表论文的内容作为新颖性来源，可能可以克服这一点。

- 如表 3、表 5 与表 4 所示，Aider 未能实现所提想法中的相当一部分。此外，GPT-4o 尤其频繁写出无法编译的 LaTeX。虽然 AI 科学家能提出有前景的创意想法，它们往往对它而言太难实现。

- AI 科学家可能错误地实现一个想法，而这可能难以发现。一个对抗性的代码审查审稿人可能部分解决这一问题。就目前而言，在信任所报告的结果之前，应人工检查实现。

- 由于 AI 科学家每个想法的实验数量有限，结果往往达不到标准 ML 会议论文预期的严谨与深度。此外，由于我们负担得起的实验数量有限，AI 科学家难以进行控制参数量、FLOPs 或运行时间的公平实验。这经常导致具有欺骗性或不准确的结论。我们预期这些问题会随着算力与基础模型成本持续下降而缓解。

- 由于我们目前不使用基础模型的视觉能力，它无法修复论文的视觉问题或读取图表。例如，生成的图有时不可读，表格有时超出页面宽度，页面布局（包括论文整体视觉外观（Huang, 2018））往往欠佳。未来具备视觉与其他模态的版本应能解决。

- 写作时，AI 科学家有时难以找到并引用最相关的论文。它还经常无法在 LaTeX 中正确引用图表，有时甚至幻觉出无效的文件路径。

- 重要的是，AI 科学家在撰写与评估结果时偶尔会犯严重错误。例如，它在比较两个数字的大小时很吃力，这是 LLM 的已知病态。此外，当它更改指标（例如损失函数）时，有时在与基线比较时不考虑这一点。为部分解决这一问题，我们确保所有实验结果可复现，在执行时保存所有文件的副本。

- 罕见地，AI 科学会幻觉出整个结果。例如，我们早期版本的写作提示告诉它总是包含置信区间与消融实验。由于计算限制，AI 科学家并不总是收集额外结果；然而在这些情况下，它有时会幻觉出一整张消融表。我们通过明确指示 AI 科学家只包含它直接观察到的结果解决了这一问题。此外，它经常幻觉出我们未提供的事实，例如所使用的硬件。

- 更一般地，我们不建议把这个版本的 AI 科学家的科学内容照单全收。相反，我们建议把生成的论文视为从业者可以跟进的有前景想法的提示。尽管如此，我们预期 AI 科学家的可信度将在未来几年随基础模型的改进而大幅提升。我们分享这篇论文与代码主要是为了展示当前可能做到什么，并预示不久后可能做到什么。

**安全的代码执行。** 当前实现的 AI 科学家在代码中几乎没有直接沙箱，若不加以适当防护，会导致若干意外且有时不良的后果。例如，在一次运行中，AI 科学家在实验文件中编写了发起系统调用重新启动自身的代码，导致 Python 进程不受控地增加，最终需要人工干预。在另一次运行中，AI 科学家修改代码为每个更新步保存一个检查点，占用了近 1 TB 存储。某些情况下，当 AI 科学家的实验超出我们施加的时间限制时，它试图修改代码任意延长时间限制，而不是设法缩短运行时间。虽然很有创意，这种绕过实验者所施加约束的行为对 AI 安全有潜在影响（Lehman et al., 2020）。此外，AI 科学家偶尔导入不熟悉的 Python 库，进一步加剧安全隐患。我们建议运行 AI 科学家时严格沙箱化，例如容器化、限制互联网访问（Semantic Scholar 除外）与限制存储使用。

与此同时，缺乏护栏也带来若干意外的正面结果。例如，我们在实验中忘记在 grokking 模板中创建输出结果目录。AI 科学家每次成功输出论文的运行都会在该错误发生时自动捕获并修复它。此外，我们发现 AI 科学家偶尔会包含让我们感到意外的结果与图表，与提供的模板差异显著。我们在第 6.1 节描述了其中一些新颖的算法专属可视化。

**更广泛的影响与伦理考量。** 虽然 AI 科学家有潜力成为研究者的宝贵工具，它也带有显著的滥用风险。自动生成论文并投给学术会议的能力可能大幅增加审稿人的工作量，可能使同行评审过程不堪重负并损害科学质量控制。类似顾虑也已在其他领域的生成式 AI 中提出，例如其对艺术的影响（Epstein et al., 2023）。此外，如果自动化审稿人工具被审稿人广泛采用，可能降低评审质量并在论文评估中引入不良偏置。因此，我们相信实质上由 AI 生成的论文或评审必须如此标注以保证完全透明。

与大多数先前的技术进步一样，AI 科学家有可能被以不道德的方式使用。例如，它可能被明确部署来进行不道德的研究，甚至如果 AI 科学家进行不安全的研究而导致意外的伤害。具体而言，如果它被鼓励寻找新颖有趣的生物材料，并被授予机器人执行湿实验室生物学实验的「云实验室」（Arnold, 2022）访问权，它可能（在其监督者意图之外）制造出新的危险病毒或毒物，在我们来得及干预之前伤害人类。即使只在计算机中，如果它被要求创建新颖、有趣、功能性的软件，它也可能创建危险的恶意软件。AI 科学家当前的能力（且只会更强）强调机器学习社区需要立即优先学习如何使这类系统的探索方式安全且与我们的价值一致。

## 9 讨论

本文提出了 AI 科学家——首个旨在完全自动化科学发现过程的框架，并作为其能力的首次展示，将其应用于机器学习自身。这一端到端系统利用 LLM 自主生成研究想法、实现并执行实验、检索相关工作并产出全面的研究论文。通过整合想法构思、实验与迭代精化等阶段，AI 科学家旨在以自动化、可扩展的方式复现人类科学过程。

**为什么写论文很重要？** 鉴于我们自动化科学发现的总体目标，为什么我们还希望 AI 科学家像人类科学家一样写论文？例如，此前启用 AI 的系统如 FunSearch（Romera-Paredes et al., 2024）与 GNoME（Pyzer-Knapp et al., 2022）也在受限领域进行了令人印象深刻的科学发现，但它们不写论文。

我们相信让 AI 科学家撰写科学论文来交流其发现至关重要的原因有几点。第一，写论文为人类提供了一种高度可解释的方式来从所学到的东西中受益。第二，在现有机器学习会议的框架内评审书面论文使我们能够标准化评估。第三，自现代科学诞生以来，科学论文一直是传播研究结果的主要媒介。由于论文可以使用自然语言并包含图表与代码，它可以灵活描述任何类型的科学研究与发现。几乎所有其他可设想的格式都被锁定在某类数据或某类科学上。在出现更优的替代方案（或可能由 AI 发明）之前，我们相信训练 AI 科学家产出科学论文对其融入更广泛的科学共同体至关重要。

**成本。** 我们的框架用途极为广泛，能有效开展机器学习各子领域的研究，包括基于 Transformer 的语言建模、神经网络学习动力学与扩散建模。该系统的成本效益——以每篇约 15 美元的成本产出具有潜在会议相关性的论文——凸显了其让研究大众化（提升可及性）并加速科学进展的能力。初步的定性分析（例如第 5 节）表明，生成的论文大体上有信息量且新颖，或至少包含值得未来研究的想法。

我们为 AI 科学家在本工作中开展实验所分配的实际算力以今天的标准也极其轻量。值得注意的是，我们生成数百篇论文的实验基本只使用一个 8×NVIDIA H100 节点、历时一周。大规模扩展搜索与过滤可能产出质量显著更高的论文。

在本项目中，运行 AI 科学家的成本大头是编码与论文写作的 LLM API 费用。相比之下，运行 LLM 审稿人的成本以及开展实验的计算开销可以忽略不计，这是我们为压低总成本而施加的约束所致。然而，如果 AI 科学家被应用于其他科学领域或用于更大规模的计算实验，这一成本结构未来可能改变。

**开放与闭源模型。** 为定量评估与改进生成的论文，我们首先创建并验证了一个自动化论文审稿人。我们表明，尽管还有很大改进空间，LLM 能够产出相当准确的评审，在多个指标上取得与人类相当的结果。把该评估器应用于 AI 科学家生成的论文，使我们能够把论文评估扩展到人工检查之外。我们发现 Sonnet 3.5 持续产出最佳论文，其中几篇甚至达到自动化论文审稿人给出的超过标准机器学习会议录用阈值的分数。

然而，没有根本理由预期 Sonnet 3.5 这样的单一模型保持领先。我们预期所有前沿 LLM（包括开放模型）都会持续改进。LLM 之间的竞争导致其商品化与能力提升。因此，我们的工作力求在基础模型提供商上保持模型无关。在本项目中，我们研究了包括 GPT-4o 与 Sonnet 在内的多个专有 LLM，但也探索了 DeepSeek 与 Llama-3 等开放模型。我们发现开放模型提供了显著益处，如更低的成本、保证的可用性、更大的透明度与灵活性，尽管质量稍差。未来，我们的目标是用我们提出的发现过程、基于开放模型在一个闭环系统中产出自我改进的 AI。

**未来方向。** 对 AI 科学家的直接增强可以包括：集成视觉能力以更好地处理图表、纳入人类反馈与交互以精化 AI 的输出，以及让 AI 科学家通过从互联网获取新数据与模型自动扩展其实验范围（前提是能安全进行）。此外，AI 科学家可以跟进其最佳想法，甚至以自指的方式直接对自身代码进行研究。事实上，本项目相当一部分代码是由 Aider 编写的。把框架扩展到其他科学领域可以进一步放大其影响，为自动化科学发现的新时代铺路。例如，通过把这些技术与云机器人技术及物理实验室空间的自动化集成（Kehoe et al., 2015；Zucchelli et al., 2021；Arnold, 2022；Sparkes et al., 2010）（前提是能安全进行），AI 科学家可以为生物学、化学与材料科学执行实验。

至关重要的是，未来工作应解决可靠性与幻觉问题，可能通过对所报告结果进行更深入的自动验证。这可以通过直接链接代码与实验，或检验自动化验证器能否独立复现结果来实现。

**结论。** AI 科学家的引入标志着朝实现 AI 在科学研究中全部潜力迈出的重要一步。通过自动化发现过程并纳入 AI 驱动的评审系统，我们为科学与技术最具挑战性的领域中的创新与问题求解开启了无尽可能性。最终，我们设想一个完全由 AI 驱动的科学生态系统，不仅包括 AI 驱动的研究者，还包括审稿人、领域主席与整个会议。然而，我们并不认为人类科学家的角色会被削弱。我们预期科学家的角色会随着我们适应新技术而改变，他们将被赋能去攻克更宏大的目标。例如，研究者往往拥有的想法多于有时间追求的想法，如果 AI 科学家能对所有这些想法进行初步探索会怎样？

虽然当前版本的 AI 科学家展示了在扩散建模或 Transformer 等已充分确立的想法之上进行创新的强大能力，这类系统能否最终提出真正范式转移的想法仍是一个开放问题。未来版本的 AI 科学家能否提出像扩散建模一样有影响力的想法，或想出下一个 Transformer 架构？机器最终能否发明出像人工神经网络或信息论一样基础的概念？我们相信 AI 科学家将成为人类科学家的绝佳伙伴，但只有时间才能告诉我们，人类创造力的本质与我们那些机缘巧合的创新时刻（Stanley and Lehman, 2015）能在多大程度上被人工智能体进行的开放式发现过程所复现。

## 致谢

作者感谢 Irene Zhang、Johannes von Oswald、Takuya Akiba、Yujin Tang、Aaron Dharna、Ben Norman、Jenny Zhang、Shengran Hu、Anna Olerinyova、Felicitas Muecke-Wegner 与 Kenneth Stanley 对本稿早期版本的有益反馈。本工作得到 Vector Institute、Canada CIFAR AI Chairs 项目、Schmidt Futures、Open Philanthropy、NSERC 的资助以及 Rafael Cosman 的慷慨捐赠支持。

## 参考文献

- Alet et al. (2020)

  Ferran Alet, Martin F Schneider, Tomas Lozano-Perez, and Leslie Pack Kaelbling.
  Meta-learning curiosity algorithms.
  *arXiv preprint arXiv:2003.05325*, 2020.
- Altmäe et al. (2023)

  Signe Altmäe, Alberto Sola-Leyva, and Andres Salumets.
  Artificial intelligence in scientific writing: a friend or a foe?
  *Reproductive BioMedicine Online*, 47(1):3–9, 2023.
- Anthropic (2023)

  Anthropic.
  Model card and evaluations for claude models, 2023.
  URL <https://www-files.anthropic.com/production/images/Model-Card-Claude-2.pdf>.
- Anthropic (2024)

  Anthropic.
  The claude 3 model family: Opus, sonnet, haiku, 2024.
  URL <https://www-cdn.anthropic.com/de8ba9b01c9ab7cbabf5c33b80b7bbc618857627/Model_Card_Claude_3.pdf>.
- Arnold (2022)

  Carrie Arnold.
  Cloud labs: where robots do the research.
  *Nature*, 606(7914):612–613, 2022.
- Baek et al. (2024)

  Jinheon Baek, Sujay Kumar Jauhar, Silviu Cucerzan, and Sung Ju Hwang.
  Researchagent: Iterative research idea generation over scientific literature with large language models, 2024.
  URL <https://arxiv.org/abs/2404.07738>.
- Berto (2024)

  Federico Berto.
  Iclr2022-openreviewdata, 2024.
  URL <https://github.com/fedebotu/ICLR2022-OpenReviewData>.
- Beygelzimer et al. (2021)

  Alina Beygelzimer, Yann Dauphin, Percy Liang, and Jennifer Wortman Vaughan.
  The neurips 2021 consistency experiment.
  *Neural Information Processing Systems blog post*, 2021.
  URL <https://blog.neurips.cc/2021/12/08/the-neurips-2021-consistency-experiment>.
- Bradley et al. (2024)

  Herbie Bradley, Andrew Dai, Hannah Benita Teufel, Jenny Zhang, Koen Oostermeijer, Marco Bellagente, Jeff Clune, Kenneth Stanley, Gregory Schott, and Joel Lehman.
  Quality-diversity through ai feedback.
  In *The Twelfth International Conference on Learning Representations*, 2024.
- Brant and Stanley (2017)

  Jonathan C Brant and Kenneth O Stanley.
  Minimal criterion coevolution: a new approach to open-ended search.
  In *Proceedings of the Genetic and Evolutionary Computation Conference*, pages 67–74, 2017.
- Brown et al. (2020)

  Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei.
  Language models are few-shot learners, 2020.
- Buchanan and Feigenbaum (1981)

  Bruce G Buchanan and Edward A Feigenbaum.
  Dendral and meta-dendral: Their applications dimension.
  In *Readings in artificial intelligence*, pages 313–322. Elsevier, 1981.
- Burns et al. (2023)

  Collin Burns, Pavel Izmailov, Jan Hendrik Kirchner, Bowen Baker, Leo Gao, Leopold Aschenbrenner, Yining Chen, Adrien Ecoffet, Manas Joglekar, Jan Leike, Ilya Sutskever, and Jeff Wu.
  Weak-to-strong generalization: Eliciting strong capabilities with weak supervision, 2023.
  URL <https://arxiv.org/abs/2312.09390>.
- Chalmers (2013)

  Alan Chalmers.
  *What is this thing called science?*
  McGraw-Hill Education (UK), 2013.
- Chen et al. (2024a)

  Angelica Chen, David Dohan, and David So.
  Evoprompting: Language models for code-level neural architecture search.
  *Advances in Neural Information Processing Systems*, 36, 2024a.
- Chen et al. (2021)

  Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al.
  Evaluating large language models trained on code.
  *arXiv preprint arXiv:2107.03374*, 2021.
- Chen et al. (2024b)

  Xiangning Chen, Chen Liang, Da Huang, Esteban Real, Kaiyuan Wang, Hieu Pham, Xuanyi Dong, Thang Luong, Cho-Jui Hsieh, Yifeng Lu, et al.
  Symbolic discovery of optimization algorithms.
  *Advances in Neural Information Processing Systems*, 36, 2024b.
- Clune (2019)

  Jeff Clune.
  Ai-gas: Ai-generating algorithms, an alternate paradigm for producing general artificial intelligence.
  *arXiv preprint arXiv:1905.10985*, 2019.
- D'Arcy et al. (2024)

  Mike D'Arcy, Tom Hope, Larry Birnbaum, and Doug Downey.
  Marg: Multi-agent review generation for scientific papers, 2024.
  URL <https://arxiv.org/abs/2401.04259>.
- Dewey (1910)

  J. Dewey.
  *How We Think*.
  D.C. Heath & Company, 1910.
  ISBN 9781519501868.
  URL <https://books.google.co.uk/books?id=WF0AAAAAMAAJ>.
- Ding et al. (2024)

  Li Ding, Jenny Zhang, Jeff Clune, Lee Spector, and Joel Lehman.
  Quality diversity through human feedback: Towards open-ended diversity-driven optimization.
  In *Forty-first International Conference on Machine Learning*, 2024.
  URL <https://openreview.net/forum?id=9zlZuAAb08>.
- Dinu et al. (2024)

  Marius-Constantin Dinu, Claudiu Leoveanu-Condrei, Markus Holzleitner, Werner Zellinger, and Sepp Hochreiter.
  Symbolicai: A framework for logic-based approaches combining generative models and solvers, 2024.
  URL <https://arxiv.org/abs/2402.00854>.
- Epstein et al. (2023)

  Ziv Epstein, Aaron Hertzmann, Investigators of Human Creativity, Memo Akten, Hany Farid, Jessica Fjeld, Morgan R Frank, Matthew Groh, Laura Herman, Neil Leach, et al.
  Art and the science of generative ai.
  *Science*, 380(6650):1110–1111, 2023.
- Faldor et al. (2024)

  Maxence Faldor, Jenny Zhang, Antoine Cully, and Jeff Clune.
  Omni-epic: Open-endedness via models of human notions of interestingness with environments programmed in code, 2024.
  URL <https://arxiv.org/abs/2405.15568>.
- Falkenhainer and Michalski (1986)

  Brian C Falkenhainer and Ryszard S Michalski.
  Integrating quantitative and qualitative discovery: the abacus system.
  *Machine Learning*, 1:367–401, 1986.
- Fawzi et al. (2022)

  Alhussein Fawzi, Matej Balog, Aja Huang, Thomas Hubert, Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Francisco J R Ruiz, Julian Schrittwieser, Grzegorz Swirszcz, et al.
  Discovering faster matrix multiplication algorithms with reinforcement learning.
  *Nature*, 610(7930):47–53, 2022.
- Fedus et al. (2022)

  William Fedus, Barret Zoph, and Noam Shazeer.
  Switch transformers: Scaling to trillion parameter models with simple and efficient sparsity.
  *Journal of Machine Learning Research*, 23(120):1–39, 2022.
  URL <http://jmlr.org/papers/v23/21-0998.html>.
- Fricke (2018)

  Suzanne Fricke.
  Semantic scholar.
  *Journal of the Medical Library Association: JMLA*, 106(1):145, 2018.
- Gauthier (2024)

  Paul Gauthier.
  aider, 2024.
  URL <https://github.com/paul-gauthier/aider>.
- Ghahramani (2015)

  Zoubin Ghahramani.
  Probabilistic machine learning and artificial intelligence.
  *Nature*, 521(7553):452–459, 2015.
- Girotra et al. (2023)

  Karan Girotra, Lennart Meincke, Christian Terwiesch, and Karl T Ulrich.
  Ideas are dimes a dozen: Large language models for idea generation in innovation.
  *Available at SSRN 4526071*, 2023.
- Glorot and Bengio (2010)

  Xavier Glorot and Yoshua Bengio.
  Understanding the difficulty of training deep feedforward neural networks.
  In *Proceedings of the thirteenth international conference on artificial intelligence and statistics*, pages 249–256. JMLR Workshop and Conference Proceedings, 2010.
- Goodfellow et al. (2014)

  Ian Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville, and Yoshua Bengio.
  Generative adversarial nets.
  In Z. Ghahramani, M. Welling, C. Cortes, N. Lawrence, and K.Q. Weinberger, editors, *Advances in Neural Information Processing Systems*, volume 27. Curran Associates, Inc., 2014.
  URL <https://proceedings.neurips.cc/paper/2014/file/5ca3e9b122f61f8f06494c97b1afccf3-Paper.pdf>.
- Google DeepMind Gemini Team (2023)

  Google DeepMind Gemini Team.
  Gemini: A family of highly capable multimodal models, 2023.
- Hatamizadeh et al. (2024)

  Ali Hatamizadeh, Jiaming Song, Guilin Liu, Jan Kautz, and Arash Vahdat.
  Diffit: Diffusion vision transformers for image generation, 2024.
  URL <https://arxiv.org/abs/2312.02139>.
- Hayes et al. (2024)

  Tomas Hayes, Roshan Rao, Halil Akin, Nicholas J Sofroniew, Deniz Oktay, Zeming Lin, Robert Verkuil, Vincent Q Tran, Jonathan Deaton, Marius Wiggert, et al.
  Simulating 500 million years of evolution with a language model.
  *bioRxiv*, pages 2024–07, 2024.
- He et al. (2021)

  Xin He, Kaiyong Zhao, and Xiaowen Chu.
  Automl: A survey of the state-of-the-art.
  *Knowledge-based systems*, 212:106622, 2021.
- Ho et al. (2020)

  Jonathan Ho, Ajay Jain, and Pieter Abbeel.
  Denoising diffusion probabilistic models.
  In H. Larochelle, M. Ranzato, H. Hadsell, M.F. Balcan, and H. Lin, editors, *Advances in Neural Information Processing Systems*, volume 33, pages 6840–6851. Curran Associates, Inc., 2020.
  URL <https://proceedings.neurips.cc/paper/2020/file/4c5bcfec8584af0d967f1ab10179ca4b-Paper.pdf>.
- Huang (2018)

  Jia-Bin Huang.
  Deep paper gestalt.
  *arXiv preprint arXiv:1812.08775*, 2018.
- Huang et al. (2024)

  Qian Huang, Jian Vora, Percy Liang, and Jure Leskovec.
  Mlagentbench: Evaluating language agents on machine learning experimentation.
  In *Forty-first International Conference on Machine Learning*, 2024.
- Hutter et al. (2019)

  Frank Hutter, Lars Kotthoff, and Joaquin Vanschoren.
  *Automated machine learning: methods, systems, challenges*.
  Springer Nature, 2019.
- Hutter (2006)

  Marcus Hutter.
  The hutter prize, 2006.
  URL <http://prize.hutter1.net>.
- Ifargan et al. (2024)

  Tal Ifargan, Lukas Hafner, Maor Kern, Ori Alcalay, and Roy Kishony.
  Autonomous llm-driven research from data to human-verifiable research papers, 2024.
  URL <https://arxiv.org/abs/2404.17605>.
- Jevons (1877)

  William Stanley Jevons.
  *The principles of science: A treatise on logic and scientific method*.
  Macmillan and Company, 1877.
- Jiang et al. (2024)

  Albert Q. Jiang, Alexandre Sablayrolles, Antoine Roux, Arthur Mensch, Blanche Savary, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Emma Bou Hanna, Florian Bressand, Gianna Lengyel, Guillaume Bour, Guillaume Lample, Lélio Renard Lavaud, Lucile Saulnier, Marie-Anne Lachaux, Pierre Stock, Sandeep Subramanian, Sophia Yang, Szymon Antoniak, Teven Le Scao, Théophile Gervet, Thibaut Lavril, Thomas Wang, Timothée Lacroix, and William El Sayed.
  Mixtral of experts, 2024.
  URL <https://arxiv.org/abs/2401.04088>.
- Jimenez et al. (2024)

  Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik Narasimhan.
  Swe-bench: Can language models resolve real-world github issues?, 2024.
  URL <https://arxiv.org/abs/2310.06770>.
- Jumper et al. (2021)

  John Jumper, Richard Evans, Alexander Pritzel, Tim Green, Michael Figurnov, Olaf Ronneberger, Kathryn Tunyasuvunakool, Russ Bates, Augustin Žídek, Anna Potapenko, et al.
  Highly accurate protein structure prediction with alphafold.
  *nature*, 596(7873):583–589, 2021.
- Karpathy (2015)

  Andrej Karpathy.
  The unreasonable effectiveness of recurrent neural networks, 2015.
  URL <https://karpathy.github.io/2015/05/21/rnn-effectiveness/>.
- Karpathy (2022)

  Andrej Karpathy.
  NanoGPT, 2022.
  URL <https://github.com/karpathy/nanoGPT>.
- Kehoe et al. (2015)

  Ben Kehoe, Sachin Patil, Pieter Abbeel, and Ken Goldberg.
  A survey of research on cloud robotics and automation.
  *IEEE Transactions on automation science and engineering*, 12(2):398–409, 2015.
- Kingma and Welling (2014)

  Diederik P. Kingma and Max Welling.
  Auto-Encoding Variational Bayes.
  In *2nd International Conference on Learning Representations, ICLR 2014, Banff, AB, Canada, April 14-16, 2014, Conference Track Proceedings*, 2014.
- Kirsch et al. (2019)

  Louis Kirsch, Sjoerd van Steenkiste, and Jürgen Schmidhuber.
  Improving generalization in meta reinforcement learning using learned objectives.
  *arXiv preprint arXiv:1910.04098*, 2019.
- Lange et al. (2023a)

  Robert Lange, Tom Schaul, Yutian Chen, Chris Lu, Tom Zahavy, Valentin Dalibard, and Sebastian Flennerhag.
  Discovering attention-based genetic algorithms via meta-black-box optimization.
  In *Proceedings of the Genetic and Evolutionary Computation Conference*, pages 929–937, 2023a.
- Lange et al. (2023b)

  Robert Lange, Tom Schaul, Yutian Chen, Tom Zahavy, Valentin Dalibard, Chris Lu, Satinder Singh, and Sebastian Flennerhag.
  Discovering evolution strategies via meta-black-box optimization.
  In *Proceedings of the Companion Conference on Genetic and Evolutionary Computation*, pages 29–30, 2023b.
- Lange et al. (2024)

  Robert Tjarko Lange, Yingtao Tian, and Yujin Tang.
  Large language models as evolution strategies.
  *arXiv preprint arXiv:2402.18381*, 2024.
- Langley (1987)

  Pat Langley.
  *Scientific discovery: Computational explorations of the creative processes*.
  MIT press, 1987.
- Langley (2024)

  Pat Langley.
  Integrated systems for computational scientific discovery.
  In *Proceedings of the AAAI Conference on Artificial Intelligence*, volume 38, pages 22598–22606, 2024.
- Lehman et al. (2008)

  Joel Lehman, Kenneth O Stanley, et al.
  Exploiting open-endedness to solve problems through the search for novelty.
  In *ALIFE*, pages 329–336, 2008.
- Lehman et al. (2020)

  Joel Lehman, Jeff Clune, Dusan Misevic, Christoph Adami, Lee Altenberg, Julie Beaulieu, Peter J Bentley, Samuel Bernard, Guillaume Beslon, David M Bryson, et al.
  The surprising creativity of digital evolution: A collection of anecdotes from the evolutionary computation and artificial life research communities.
  *Artificial life*, 26(2):274–306, 2020.
- Lehman et al. (2022)

  Joel Lehman, Jonathan Gordon, Shawn Jain, Kamal Ndousse, Cathy Yeh, and Kenneth O. Stanley.
  Evolution through large models, 2022.
  URL <https://arxiv.org/abs/2206.08896>.
- Lehman et al. (2023)

  Joel Lehman, Jonathan Gordon, Shawn Jain, Kamal Ndousse, Cathy Yeh, and Kenneth O Stanley.
  Evolution through large models.
  In *Handbook of Evolutionary Machine Learning*, pages 331–366. Springer, 2023.
- Lenat (1977)

  Douglas B Lenat.
  Automated theory formation in mathematics.
  In *IJCAI*, volume 77, pages 833–842, 1977.
- Lenat and Brown (1984)

  Douglas B Lenat and John Seely Brown.
  Why am and eurisko appear to work.
  *Artificial intelligence*, 23(3):269–294, 1984.
- Liang et al. (2024)

  Weixin Liang, Yuhui Zhang, Hancheng Cao, Binglu Wang, Daisy Yi Ding, Xinyu Yang, Kailas Vodrahalli, Siyu He, Daniel Scott Smith, Yian Yin, et al.
  Can large language models provide useful feedback on research papers? a large-scale empirical analysis.
  *NEJM AI*, page AIoa2400196, 2024.
- Lim et al. (2024)

  Bryan Lim, Manon Flageat, and Antoine Cully.
  Large language models as in-context ai generators for quality-diversity.
  *arXiv preprint arXiv:2404.15794*, 2024.
- Llama Team (2024)

  Llama Team.
  The llama 3 herd of models, 2024.
  URL <https://arxiv.org/abs/2407.21783>.
- Lu et al. (2022a)

  Chris Lu, Jakub Kuba, Alistair Letcher, Luke Metz, Christian Schroeder de Witt, and Jakob Foerster.
  Discovered policy optimisation.
  *Advances in Neural Information Processing Systems*, 35:16455–16468, 2022a.
- Lu et al. (2024a)

  Chris Lu, Samuel Holt, Claudio Fanconi, Alex J Chan, Jakob Foerster, Mihaela van der Schaar, and Robert Tjarko Lange.
  Discovering preference optimization algorithms with and for large language models.
  *arXiv preprint arXiv:2406.08414*, 2024a.
- Lu et al. (2022b)

  Cong Lu, Philip Ball, Jack Parker-Holder, Michael Osborne, and Stephen J. Roberts.
  Revisiting design choices in offline model based reinforcement learning.
  In *International Conference on Learning Representations*, 2022b.
  URL <https://openreview.net/forum?id=zz9hXVhf40>.
- Lu et al. (2024b)

  Cong Lu, Shengran Hu, and Jeff Clune.
  Intelligent go-explore: Standing on the shoulders of giant foundation models, 2024b.
  URL <https://arxiv.org/abs/2405.15143>.
- Ma et al. (2023)

  Yecheng Jason Ma, William Liang, Guanzhi Wang, De-An Huang, Osbert Bastani, Dinesh Jayaraman, Yuke Zhu, Linxi Fan, and Anima Anandkumar.
  Eureka: Human-level reward design via coding large language models.
  *arXiv preprint arXiv:2310.12931*, 2023.
- Mahoney (2011)

  Matt Mahoney.
  About the test data, 2011.
  URL <http://mattmahoney.net/dc/textdata.html>.
- Majumder et al. (2024)

  Bodhisattwa Prasad Majumder, Harshit Surana, Dhruv Agarwal, Bhavana Dalvi Mishra, Abhijeetsingh Meena, Aryan Prakhar, Tirth Vora, Tushar Khot, Ashish Sabharwal, and Peter Clark.
  Discoverybench: Towards data-driven discovery with large language models, 2024.
  URL <https://arxiv.org/abs/2407.01725>.
- May (2022)

  Daniel May.
  grokking, 2022.
  URL <https://github.com/danielmamay/grokking>.
- Merchant et al. (2023)

  Amil Merchant, Simon Batzner, Samuel S Schoenholz, Muratahan Aykol, Gowoon Cheon, and Ekin Dogus Cubuk.
  Scaling deep learning for materials discovery.
  *Nature*, 624(7990):80–85, 2023.
- Metz et al. (2022)

  Luke Metz, James Harrison, C Daniel Freeman, Amil Merchant, Lucas Beyer, James Bradbury, Naman Agrawal, Ben Poole, Igor Mordatch, Adam Roberts, et al.
  Velo: Training versatile learned optimizers by scaling up.
  *arXiv preprint arXiv:2211.09760*, 2022.
- Nordhausen and Langley (1990)

  Bernd Nordhausen and Pat Langley.
  A robust approach to numeric discovery.
  In *Machine learning proceedings 1990*, pages 411–418. Elsevier, 1990.
- Olsson et al. (2022)

  Catherine Olsson, Nelson Elhage, Neel Nanda, Nicholas Joseph, Nova DasSarma, Tom Henighan, Ben Mann, Amanda Askell, Yuntao Bai, Anna Chen, et al.
  In-context learning and induction heads.
  *arXiv preprint arXiv:2209.11895*, 2022.
- OpenAI (2023)

  OpenAI.
  Gpt-4 technical report, 2023.
- Pärnamaa (2023)

  Tanel Pärnamaa.
  tiny-diffusion, 2023.
  URL <https://github.com/tanelp/tiny-diffusion>.
- Power et al. (2022)

  Alethea Power, Yuri Burda, Harri Edwards, Igor Babuschkin, and Vedant Misra.
  Grokking: Generalization beyond overfitting on small algorithmic datasets.
  *arXiv preprint arXiv:2201.02177*, 2022.
- Pyzer-Knapp et al. (2022)

  Edward O Pyzer-Knapp, Jed W Pitera, Peter WJ Staar, Seiji Takeda, Teodoro Laino, Daniel P Sanders, James Sexton, John R Smith, and Alessandro Curioni.
  Accelerating materials discovery using artificial intelligence, high performance computing and robotics.
  *npj Computational Materials*, 8(1):84, 2022.
- Romera-Paredes et al. (2024)

  Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog, M Pawan Kumar, Emilien Dupont, Francisco JR Ruiz, Jordan S Ellenberg, Pengming Wang, Omar Fawzi, et al.
  Mathematical discoveries from program search with large language models.
  *Nature*, 625(7995):468–475, 2024.
- Schick et al. (2024)

  Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Eric Hambro, Luke Zettlemoyer, Nicola Cancedda, and Thomas Scialom.
  Toolformer: Language models can teach themselves to use tools.
  *Advances in Neural Information Processing Systems*, 36, 2024.
- Schmidhuber (1991)

  Jürgen Schmidhuber.
  Curious model-building control systems.
  In *Proc. international joint conference on neural networks*, pages 1458–1463, 1991.
- Schmidhuber (2010a)

  Jürgen Schmidhuber.
  Artificial scientists & artists based on the formal theory of creativity.
  In *3d Conference on Artificial General Intelligence (AGI-2010)*, pages 148–153. Atlantis Press, 2010a.
- Schmidhuber (2010b)

  Jürgen Schmidhuber.
  Formal theory of creativity, fun, and intrinsic motivation (1990–2010).
  *IEEE transactions on autonomous mental development*, 2(3):230–247, 2010b.
- Schmidhuber (2012)

  Jürgen Schmidhuber.
  When creative machines overtake man, 2012.
  URL <https://www.youtube.com/watch?v=KQ35zNlyG-o>.
- Shinn et al. (2024)

  Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao.
  Reflexion: Language agents with verbal reinforcement learning.
  *Advances in Neural Information Processing Systems*, 36, 2024.
- Snell (2021)

  Charlie Snell.
  grokking, 2021.
  URL <https://github.com/Sea-Snell/grokking>.
- Sohl-Dickstein et al. (2015)

  Jascha Sohl-Dickstein, Eric Weiss, Niru Maheswaranathanathan, and Surya Ganguli.
  Deep unsupervised learning using nonequilibrium thermodynamics.
  In Francis Bach and David Blei, editors, *Proceedings of the 32nd International Conference on Machine Learning*, volume 37 of *Proceedings of Machine Learning Research*, pages 2256–2265, Lille, France, 07–09 Jul 2015. PMLR.
  URL <https://proceedings.mlr.press/v37/sohl-dickstein15.html>.
- Song et al. (2024)

  Xingyou Song, Yingtao Tian, Robert Tjarko Lange, Chansoo Lee, Yujin Tang, and Yutian Chen.
  Position paper: Leveraging foundational models for black-box optimization: Benefits, challenges, and future directions.
  *arXiv preprint arXiv:2405.03547*, 2024.
- Sparkes et al. (2010)

  Andrew Sparkes, Wayne Aubrey, Emma Byrne, Amanda Clare, Muhammed N Khan, Maria Liakata, Magdalena Markham, Jem Rowland, Larisa N Soldatova, Kenneth E Whelan, et al.
  Towards robot scientists for autonomous scientific discovery.
  *Automated experimentation*, 2:1–11, 2010.
- Stanley (2019)

  Kenneth O Stanley.
  Why open-endedness matters.
  *Artificial life*, 25(3):232–235, 2019.
- Stanley and Lehman (2015)

  Kenneth O Stanley and Joel Lehman.
  *Why greatness cannot be planned: The myth of the objective*.
  Springer, 2015.
- Stanley et al. (2017)

  Kenneth O Stanley, Joel Lehman, and Lisa Soros.
  Open-endedness: The last grand challenge you've never heard of.
  *While open-endedness could be a force for discovering intelligence, it could also be a component of AI itself*, 2017.
- Szymanski et al. (2023)

  Nathan J Szymanski, Bernardus Rendy, Yuxing Fei, Rishi E Kumar, Tanjin He, David Milsted, Matthew J McDermott, Max Gallant, Ekin Dogus Cubuk, Amil Merchant, et al.
  An autonomous laboratory for the accelerated synthesis of novel materials.
  *Nature*, 624(7990):86–91, 2023.
- Talmor et al. (2019)

  Alon Talmor, Jonathan Herzig, Nicholas Lourie, and Jonathan Berant.
  CommonsenseQA: A question answering challenge targeting commonsense knowledge.
  In Jill Burstein, Christy Doran, and Thamar Solorio, editors, *Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)*, pages 4149–4158, Minneapolis, Minnesota, June 2019. Association for Computational Linguistics.
  [10.18653/v1/N19-1421](https://doi.org/10.18653/v1/N19-1421).
  URL <https://aclanthology.org/N19-1421>.
- Vaswani et al. (2017)

  Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin.
  Attention is all you need.
  *Advances in neural information processing systems*, 30, 2017.
- Waltz and Buchanan (2009)

  David Waltz and Bruce G Buchanan.
  Automating science.
  *Science*, 324(5923):43–44, 2009.
- Wan et al. (2021)

  Xingchen Wan, Vu Nguyen, Huong Ha, Binxin Ru, Cong Lu, and Michael A Osborne.
  Think global and act local: Bayesian optimisation over high-dimensional categorical and mixed search spaces.
  In *International Conference on Machine Learning*, pages 10663–10674. PMLR, 2021.
- Wan et al. (2022)

  Xingchen Wan, Cong Lu, Jack Parker-Holder, Philip J. Ball, Vu Nguyen, Binxin Ru, and Michael Osborne.
  Bayesian generational population-based training.
  In Isabelle Guyon, Marius Lindauer, Mihaela van der Schaar, Frank Hutter, and Roman Garnett, editors, *Proceedings of the First International Conference on Automated Machine Learning*, volume 188 of *Proceedings of Machine Learning Research*, pages 14/1–27. PMLR, 25–27 Jul 2022.
  URL <https://proceedings.mlr.press/v188/wan22a.html>.
- Wang et al. (2024a)

  Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai Tang, Xu Chen, Yankai Lin, et al.
  A survey on large language model based autonomous agents.
  *Frontiers of Computer Science*, 18(6):186345, 2024a.
- Wang et al. (2024b)

  Qingyun Wang, Doug Downey, Heng Ji, and Tom Hope.
  Scimon: Scientific inspiration machines optimized for novelty, 2024b.
  URL <https://arxiv.org/abs/2305.14259>.
- Wang et al. (2022)

  Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou.
  Self-consistency improves chain of thought reasoning in language models.
  *arXiv preprint arXiv:2203.11171*, 2022.
- Wang et al. (2024c)

  Yidong Wang, Qi Guo, Wenjin Yao, Hongbo Zhang, Xin Zhang, Zhen Wu, Meishan Zhang, Xinyu Dai, Min Zhang, Qingsong Wen, Wei Ye, Shikun Zhang, and Yue Zhang.
  Autosurvey: Large language models can automatically write surveys, 2024c.
  URL <https://arxiv.org/abs/2406.10252>.
- Wei et al. (2022)

  Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al.
  Chain-of-thought prompting elicits reasoning in large language models.
  *Advances in neural information processing systems*, 35:24824–24837, 2022.
- Xu et al. (2022)

  Frank F Xu, Uri Alon, Graham Neubig, and Vincent Josua Hellendoorn.
  A systematic evaluation of large language models of code.
  In *Proceedings of the 6th ACM SIGPLAN International Symposium on Machine Programming*, pages 1–10, 2022.
- Yang et al. (2024)

  Zonglin Yang, Xinya Du, Junxian Li, Jie Zheng, Soujanya Poria, and Erik Cambria.
  Large language models for automated open-domain scientific hypotheses discovery, 2024.
  URL <https://arxiv.org/abs/2309.02726>.
- Yu et al. (2023)

  Wenhao Yu, Nimrod Gileadi, Chuyuan Fu, Sean Kirmani, Kuang-Huei Lee, Montse Gonzalez Arenas, Hao-Tien Lewis Chiang, Tom Erez, Leonard Hasenclever, Jan Humplik, et al.
  Language to rewards for robotic skill synthesis.
  *arXiv preprint arXiv:2306.08647*, 2023.
- Yuksel et al. (2012)

  Seniha Esen Yuksel, Joseph N Wilson, and Paul D Gader.
  Twenty years of mixture of experts.
  *IEEE transactions on neural networks and learning systems*, 23(8):1177–1193, 2012.
- Zhang et al. (2024)

  Jenny Zhang, Joel Lehman, Kenneth Stanley, and Jeff Clune.
  OMNI: Open-endedness via models of human notions of interestingness.
  In *The Twelfth International Conference on Learning Representations*, 2024.
  URL <https://openreview.net/forum?id=AgM3MzT99c>.
- Zheng et al. (2024)

  Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric Xing, et al.
  Judging llm-as-a-judge with mt-bench and chatbot arena.
  *Advances in Neural Information Processing Systems*, 36, 2024.
- Zhu et al. (2024)

  Qihao Zhu, Daya Guo, Zhihong Shao, Dejian Yang, Peiyi Wang, Runxin Xu, Y Wu, Yukun Li, Huazuo Gao, Shirong Ma, et al.
  Deepseek-coder-v2: Breaking the barrier of closed-source models in code intelligence.
  *arXiv preprint arXiv:2406.11931*, 2024.
- Zucchelli et al. (2021)

  Piero Zucchelli, Giorgio Horak, and Nigel Skinner.
  Highly versatile cloud-based automation solution for the remote design and execution of experiment protocols during the covid-19 pandemic.
  *SLAS TECHNOLOGY: Translating Life Sciences Innovation*, 26(2):127–139, 2021.
- Zytkow (1996)

  Jan M Zytkow.
  Automated discovery of empirical laws.
  *Fundamenta Informaticae*, 27(2-3):299–318, 1996.

## 附录 A 提示词

我们在此给出第 3 节与第 4 节中 AI 科学家所使用的部分代表性提示词。完整提示词列表见所提供的代码。

### A.1 想法生成

这些提示词对应第 3 节中 AI 科学家的第一阶段。

Idea Generation System Prompt

You are an ambitious AI PhD student who is looking to publish a paper that will contribute significantly to the field.

Idea Generation Prompt

```
{task_description}
<experiment.py>
{code}
</experiment.py>

Here are the ideas that you have already generated:

’’’
{prev_ideas_string}
’’’

Come up with the next impactful and creative idea for research
experiments and directions you can feasibly investigate with the code
provided. Note that you will not have access to any additional resources
or datasets. Make sure any idea is not overfit the specific training
dataset or model, and has wider significance.

Respond in the following format:

THOUGHT:
<THOUGHT>

NEW IDEA JSON:
‘‘‘json
<JSON>
‘‘‘

In <THOUGHT>, first briefly discuss your intuitions and motivations for
the idea. Detail your high-level plan, necessary design choices and
ideal outcomes of the experiments. Justify how the idea is different
from the existing ones.

In <JSON>, provide the new idea in JSON format with the following fields:
- "Name": A shortened descriptor of the idea. Lowercase, no spaces,
underscores allowed.
- "Title": A title for the idea, will be used for the report writing.
- "Experiment": An outline of the implementation. E.g. which functions
need to be added or modified, how results will be obtained, ...
- "Interestingness": A rating from 1 to 10 (lowest to highest).
- "Feasibility": A rating from 1 to 10 (lowest to highest).
- "Novelty": A rating from 1 to 10 (lowest to highest).

Be cautious and realistic on your ratings.
This JSON will be automatically parsed, so ensure the format is precise.
You will have {num_reflections} rounds to iterate on the idea, but do
not need to use them all.
```

Idea Novelty System Prompt

```
You are an ambitious AI PhD student who is looking to publish a paper that
will contribute significantly to the field.
You have an idea and you want to check if it is novel or not. I.e., not
overlapping significantly with existing literature or already well explored.
Be a harsh critic for novelty, ensure there is a sufficient contribution in
the idea for a new conference or workshop paper.
You will be given access to the Semantic Scholar API, which you may use to
survey the literature and find relevant papers to help you make your
decision.
The top 10 results for any search query will be presented to you with the
abstracts.

You will be given {num_rounds} to decide on the paper, but you do not need
to use them all.
At any round, you may exit early and decide on the novelty of the idea.
Decide a paper idea is novel if after sufficient searching, you have not
found a paper that significantly overlaps with your idea.
Decide a paper idea is not novel, if you have found a paper that
significantly overlaps with your idea.

{task_description}
<experiment.py>
{code}
</experiment.py>
```

Idea Novelty Prompt

```
Round {current_round}/{num_rounds}.
You have this idea:

"""
{idea}
"""

The results of the last query are (empty on first round):
"""
{last_query_results}
"""

Respond in the following format:

THOUGHT:
<THOUGHT>

RESPONSE:
‘‘‘json
<JSON>
‘‘‘

In <THOUGHT>, first briefly reason over the idea and identify any query that
could help you make your decision.
If you have made your decision, add "Decision made: novel." or
"Decision made: not novel." to your thoughts.

In <JSON>, respond in JSON format with ONLY the following field:
- "Query": An optional search query to search the literature (e.g. attention
is all you need). You must make a query if you have not decided this round.

A query will work best if you are able to recall the exact name of the paper
you are looking for, or the authors.
This JSON will be automatically parsed, so ensure the format is precise.
```

### A.2 设计实验

这些提示词对应第 3 节中 AI 科学家的第二阶段。

Experiment Running Aider Prompt

```
Your goal is to implement the following idea: {title}.
The proposed experiment is as follows: {idea}.
You are given a total of up to {max_runs} runs to complete the necessary
experiments. You do not need to use all {max_runs}.

First, plan the list of experiments you would like to run. For example,
if you are sweeping over a specific hyperparameter, plan each value you
would like to test for each run.

Note that we already provide the vanilla baseline results, so you do not
need to re-run it.

For reference, the baseline results are as follows:

{baseline_results}

After you complete each change, we will run the command ‘python
experiment.py --out_dir=run_i’ where i is the run number and evaluate
the results.
YOUR PROPOSED CHANGE MUST USE THIS COMMAND FORMAT, DO NOT ADD ADDITIONAL
COMMAND LINE ARGS.
You can then implement the next thing on your list.
```

Plotting Aider Prompt

```
Great job! Please modify ‘plot.py‘ to generate the most relevant plots for
the final writeup.

In particular, be sure to fill in the "labels" dictionary with the correct
names for each run that you want to plot.

Only the runs in the ‘labels‘ dictionary will be plotted, so make sure to
include all relevant runs.

We will be running the command ‘python plot.py‘ to generate the plots.

---

Please modify ‘notes.txt‘ with a description of what each plot shows along
with the filename of the figure. Please do so in-depth.

Somebody else will be using ‘notes.txt‘ to write a report on this in the
future.
```

### A.3 论文写作

这些提示词对应第 3 节中 AI 科学家的最后阶段。

Paper Writing Aider Prompt

```
We’ve provided the ‘latex/template.tex‘ file to the project. We will be
filling it in section by section.

First, please fill in the {section} section of the writeup.

Some tips are provided below:
{per_section_tips}

Before every paragraph, please include a brief description of what you plan
to write in that paragraph in a comment.

Be sure to first name the file and use *SEARCH/REPLACE* blocks to perform
these edits.
```

### A.4 论文评审

这些提示词对应第 4 节中 AI 科学家的评审过程。

Paper Review System Prompt

You are an AI researcher who is reviewing a paper that was submitted to a prestigious ML venue. Be critical and cautious in your decision. If a paper is bad or you are unsure, give it bad scores and reject it.

Paper Review Prompt

```
## Review Form
Below is a description of the questions you will be asked on the review form
for each paper and some guidelines on what to consider when answering these
questions.
When writing your review, please keep in mind that after decisions have been
made, reviews and meta-reviews of accepted papers and opted-in rejected
papers will be made public.

{neurips_reviewer_guidelines}

{few_show_examples}

Here is the paper you are asked to review:
‘‘‘
{paper}
‘‘‘
```

Paper Review Reflection Prompt

```
Round {current_round}/{num_reflections}.
In your thoughts, first carefully consider the accuracy and soundness of
the review you just created.
Include any other factors that you think are important in evaluating the
paper.
Ensure the review is clear and concise, and the JSON is in the correct
format.
Do not make things overly complicated.
In the next attempt, try and refine and improve your review.
Stick to the spirit of the original review unless there are glaring
issues.

Respond in the same format as before:
THOUGHT:
<THOUGHT>

REVIEW JSON:
‘‘‘json
<JSON>
‘‘‘

If there is nothing to improve, simply repeat the previous JSON EXACTLY
after the thought and include "I am done" at the end of the thoughts but
before the JSON.
ONLY INCLUDE "I am done" IF YOU ARE MAKING NO MORE CHANGES.
```

Paper Review Ensembling System Prompt

```
You are an Area Chair at a machine learning conference.
You are in charge of meta-reviewing a paper that was reviewed by
{reviewer_count} reviewers.
Your job is to aggregate the reviews into a single meta-review in the same
format.
Be critical and cautious in your decision, find consensus, and respect the
opinion of all the reviewers.
```

Paper Review Ensembling Prompt

```
Review 1/N:
{review_1}

...

Review N/N:
{review_N}

{neurips_reviewer_guidelines}
```

## 附录 B 超参数

我们在此列出第 6 节最终实验中使用的超参数。

表 6：AI 科学家的超参数。

| 类别 | 超参数 | 数值 |
| --- | --- | --- |
| 想法生成 | 想法反思轮数 | 3 |
| 新颖性搜索轮数（Semantic Scholar） | 10 |
| 实验执行 | 最大实验数 | 5 |
| 最大实验尝试次数 | 4 |
| 实验超时 | 7200 秒 |
| 绘图超时 | 600 秒 |
| 论文写作 | 引用检索轮数（Semantic Scholar） | 20 |
| LaTeX 纠错轮数 | 5 |
| 审稿人 | 反思轮数 | 5 |
| 少样本示例数 | 1 |
| 集成评审数 | 5 |
| LLM 温度 | 0.1 |

## 附录 C 生成想法的演变

我们使用 Sonnet 3.5，可视化 AI 科学家在第 6.3 节所述「Grokking」模板上一次运行中想法的演变。第一个想法是种子想法，后续所有想法均由 AI 生成。

Seed Idea - batch_size_grokking

```
"Name": "batch_size_grokking",
"Title": "Batch Size Grokking: Assessing the impact of the training
batchsize on the grokking phenomenon",
"Experiment": "Modify the experiments to dynamically adjust the batch size
during training, starting with a small batch size and gradually increasing
it. This could potentially lead to faster generalization on the validation
set.",
"Interestingness": 6,
"Feasibility": 4,
"Novelty": 4,
"novel": true
```

Idea 1/50 - model_size_grokking

```
"Name": "model_size_grokking",
"Title": "Investigating the Impact of Model Size on the Grokking
Phenomenon",
"Experiment": "Modify the Transformer class to accept variable number of
layers and dimension sizes. Test models with 1, 2, 4, and 8 layers, and
dimension sizes of 64, 128, 256, and 512. For each dataset and model size,
track the step at which grokking occurs (defined as validation accuracy
exceeding 99%
and final accuracy vs model size for each task.",
"Interestingness": 8,
"Feasibility": 7,
"Novelty": 7,
"novel": true
```

Idea 2/50 - optimizer_grokking

```
"Name": "optimizer_grokking",
"Title": "Optimization Dynamics and Grokking: Comparing SGD and Adam with
Different Learning Rate Schedules",
"Experiment": "Modify the training loop to support two optimizers (SGD,
Adam) and two learning rate schedules (constant, cosine annealing). For
each combination, run multiple experiments with different random seeds.
Track validation accuracy, training loss, and L2 norm of weight updates
throughout training. Compare the timing and extent of grokking across these
optimization strategies for each dataset. Analyze how different
optimization dynamics correlate with grokking behavior, including
statistical analysis of the results.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 3/50 - biased_data_grokking

```
"Name": "biased_data_grokking",
"Title": "Grokking Under Biased Data: The Effect of Input Range Bias on
Neural Network Generalization",
"Experiment": "Modify the fetch_train_example method in AbstractDataset to
introduce a simple bias: favoring lower-valued inputs. For modular
arithmetic operations, sample 70%
of the input range. For permutations, favor permutations with more elements
in their original positions. Keep the validation set unbiased. Run
experiments comparing grokking behavior on biased vs. unbiased training
sets. Track metrics such as steps to 99%
validation accuracy, and training loss. Analyze how this bias affects
grokking across different operations.",
"Interestingness": 8,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 4/50 - adaptive_noise_grokking

```
"Name": "adaptive_noise_grokking",
"Title": "Adaptive Noise in Grokking: Investigating Input Perturbations on
Algorithmic Learning and Representations",
"Experiment": "Modify the GroupDataset class to add operation-specific
noise during training: (1) For modular arithmetic, add small integer
perturbations. (2) For permutations, occasionally swap two elements.
Implement three noise levels (low, medium, high) for each operation.
Compare grokking behavior across noise levels and operations, tracking
steps to 99%
loss. Analyze learned representations by visualizing attention patterns and
performing principal component analysis (PCA) on hidden states at different
training stages. Compare these representations between noisy and non-noisy
training to understand how noise affects the abstraction of concepts.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 5/50 - attention_evolution_grokking

```
"Name": "attention_evolution_grokking",
"Title": "Attention Evolution in Grokking: Quantifying the Transition from
Memorization to Generalization",
"Experiment": "Modify the Transformer class to output attention weights.
Extract and store attention weights at key checkpoints: start, mid-
training, grokking point (99%
visualization tools for attention heatmaps and create plots showing
attention evolution over time. Calculate the Frobenius norm of the
difference between attention matrices at consecutive checkpoints to
quantify attention evolution. Compare attention patterns and evolution
metrics across different operations (modular arithmetic vs. permutations).
Analyze attention for specific, informative input sequences to enhance
interpretability. Correlate attention evolution metrics with validation
accuracy and generalization performance.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 6/50 - local_vs_global_attention_grokking

```
"Name": "local_vs_global_attention_grokking",
"Title": "Local vs Global Attention: Investigating the Impact of Attention
Scope on Grokking in Algorithmic Learning",
"Experiment": "Modify the DecoderBlock class to support two attention
mechanisms: full (global) attention and local attention with a fixed window
size. Implement these variants and run experiments across all datasets.
Track metrics including time to grokking (99%
validation accuracy, and training loss. Calculate and compare ’attention
entropy’ for both mechanisms across tasks to quantify attention focus.
Analyze how the scope of attention (local vs global) affects grokking
behavior and final performance for different algorithmic tasks.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 7/50 - input_encoding_grokking

```
"Name": "input_encoding_grokking",
"Title": "Binary vs One-Hot Encoding: Impact on Grokking in Algorithmic
Learning Tasks",
"Experiment": "Modify the AbstractDataset class to support two encoding
schemes: one-hot (current) and binary. Implement binary encoding for
modular arithmetic operations using log2(p) bits, and for permutations
using ceil(log2(k!)) bits to represent each permutation uniquely. Adjust
the Transformer class to accommodate different input sizes. Run experiments
for each encoding scheme across all datasets, tracking metrics such as time
to grokking (99%
loss, and model memory usage. Analyze how different encoding schemes affect
grokking behavior, convergence speed, and final performance for various
algorithmic tasks. Compare the impact of input representations on the
model’s ability to learn and generalize across different operations.
Discuss how findings could inform input representation choices in other
machine learning tasks beyond algorithmic learning.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 8/50 - curriculum_learning_grokking

```
"Name": "curriculum_learning_grokking",
"Title": "Curriculum Learning in Grokking: The Effect of Structured Example
Progression on Algorithmic Learning",
"Experiment": "Modify the AbstractDataset class to implement a simple
curriculum learning strategy. For modular arithmetic operations, start with
operations involving numbers in the lower half of the range and gradually
introduce larger numbers. For permutations, begin with permutations that
differ from the identity by one swap and progressively increase the number
of swaps. Implement a curriculum scheduler that increases difficulty every
500 steps. Run experiments comparing standard random sampling vs.
curriculum learning across all datasets. Track metrics including time to
grokking (99%
loss. Plot learning trajectories (validation accuracy over time) for both
approaches. Compare attention patterns between curriculum and random
approaches at different stages of training. Analyze how the curriculum
affects the grokking phenomenon across different operations and discuss
implications for training neural networks on algorithmic tasks.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 9/50 - weight_init_grokking

```
"Name": "weight_init_grokking",
"Title": "Weight Initialization Strategies and Their Impact on Grokking in
Algorithmic Learning",
"Experiment": "Modify the Transformer class to support three weight
initialization strategies: Xavier/Glorot, Kaiming/He, and random normal (as
baseline). Implement these initialization methods for linear layers and
embeddings. Run experiments across all datasets for each initialization
strategy. Track metrics including time to grokking (99%
accuracy), final validation accuracy, training loss, and gradient norm
during training. Plot learning curves and compare the distribution of
weight values at different stages of training. Analyze the loss landscape
by computing gradient variance as a proxy for local geometry at key points
during training. Compare how different initialization strategies affect the
grokking phenomenon, convergence speed, and final performance across
various algorithmic tasks. Investigate potential correlations between
initial weight distributions, gradient variance characteristics, and the
timing/nature of the grokking transition.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 8,
"novel": true
```

Idea 10/50 - task_complexity_grokking

```
"Name": "task_complexity_grokking",
"Title": "Grokking Across Task Complexity: Mapping Neural Network Learning
Dynamics to Algorithmic Difficulty",
"Experiment": "1. Modify the AbstractDataset class to include new
operations of increasing complexity: modular addition, subtraction,
multiplication, and exponentiation. 2. Implement these operations in new
dataset classes. 3. Quantify task complexity using metrics like algebraic
degree and average solution time for humans (estimated). 4. Run experiments
for each operation, tracking metrics such as time to grokking (99%
validation accuracy), final validation accuracy, training loss, and a new
’complexity-adjusted learning rate’ (validation accuracy improvement per
epoch, normalized by task complexity). 5. Plot learning curves and
complexity-adjusted learning rates for each operation. 6. Analyze attention
patterns and hidden state representations at different stages of training
for each operation. 7. Investigate correlations between quantified task
complexity and grokking characteristics (e.g., time to grokking, steepness
of accuracy improvement).",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 11/50 - regularization_grokking

```
"Name": "regularization_grokking",
"Title": "The Role of Regularization in Grokking: How L2 and Label
Smoothing Affect Algorithmic Learning",
"Experiment": "1. Implement L2 regularization by adding weight decay to the
optimizer. 2. Implement label smoothing in the loss function. 3. Modify the
training function to support these regularization techniques with two
strength levels each (low and high). 4. Run experiments for each
regularization technique and strength across all datasets, including a
baseline without regularization. 5. Track metrics: time to grokking (99%
validation accuracy), final validation accuracy, training loss, and a new
’grokking speed’ metric (rate of validation accuracy improvement from 50%
to 90%
for different regularization settings. 7. Analyze how L2 regularization and
label smoothing affect the timing, speed, and nature of grokking across
various algorithmic tasks, comparing against the non-regularized
baseline.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 8,
"novel": true
```

Idea 12/50 - grokking_extrapolation

```
"Name": "grokking_extrapolation",
"Title": "Grokking and Extrapolation: Investigating the Limits of
Algorithmic Understanding",
"Experiment": "1. Modify AbstractDataset to create a separate test set with
out-of-distribution examples (e.g., larger numbers for modular arithmetic,
longer permutations). 2. Implement a new evaluation function for the test
set. 3. During training, periodically evaluate on both validation and test
sets. 4. Track metrics: time to grokking on validation set, final
validation accuracy, test set accuracy at grokking point, final test set
accuracy, and ’extrapolation gap’. 5. Implement visualization of test set
performance and extrapolation gap over time, highlighting the grokking
point. 6. Compare extrapolation capabilities across different operations
and model sizes. 7. Analyze attention patterns on test set inputs before
and after grokking. 8. Implement a simple MLP baseline for comparison.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 13/50 - label_noise_grokking

```
"Name": "label_noise_grokking",
"Title": "Grokking Under Noise: The Impact of Systematic and Random Label
Errors on Algorithmic Learning",
"Experiment": "1. Modify the AbstractDataset class to introduce two types
of label noise: random (labels changed randomly) and systematic (specific
labels consistently flipped). Add a ’noise_type’ parameter
(random/systematic) and ’noise_level’ parameter (low: 5%
high: 20%
training set while keeping the validation set clean. 3. Run experiments for
each noise type and level across all datasets. 4. Track metrics: time to
grokking (99%
loss, and model confidence (mean softmax probability of correct class). 5.
Plot learning curves and model confidence for different noise types and
levels, highlighting the grokking point for each. 6. Analyze how different
types and levels of label noise affect the timing, speed, and extent of
grokking across different operations. 7. Compare attention patterns between
noisy and clean training at different stages to understand how the model
adapts to noise.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 14/50 - compositional_grokking

```
"Name": "compositional_grokking",
"Title": "Compositional Grokking: Investigating the Relationship Between
Grokking and Compositional Learning in Modular Arithmetic",
"Experiment": "1. Modify ModSumDataset and ModSubtractDataset to include
composite operations: (a + b) - c mod p and (a - b) + c mod p. 2. Implement
new dataset class CompositeModDataset for these operations. 3. Run
experiments comparing learning curves for basic (a + b, a - b) and
composite operations. 4. Track metrics: time to grokking for basic vs.
composite operations, correlation between grokking times, final accuracies.
5. Analyze attention patterns to see if the model learns to attend to
intermediate results in composite operations. 6. Implement a ’compositional
generalization’ test by training on basic operations and testing on their
compositions. 7. Compare internal representations (e.g., using PCA on
hidden states) for basic vs. composite operations at different stages of
training.",
"Interestingness": 9,
"Feasibility": 6,
"Novelty": 9,
"novel": true
```

Idea 15/50 - mutual_information_grokking

```
"Name": "mutual_information_grokking",
"Title": "Information Dynamics in Grokking: Analyzing Mutual Information
Evolution During Algorithmic Learning",
"Experiment": "1. Implement a function to estimate mutual information using
a binning approach for efficiency. 2. Modify the Transformer class to
output hidden states from the final layer. 3. Update the training loop to
calculate and store mutual information between (a) inputs and outputs, and
(b) final hidden states and outputs, at regular intervals. 4. Run
experiments across all datasets, tracking these mutual information metrics
alongside validation accuracy and training loss. 5. Create plots showing
the evolution of both mutual information metrics over training time,
highlighting the grokking point. 6. Analyze how mutual information trends
relate to grokking by testing specific hypotheses: (a) Rapid increase in
hidden state-output mutual information coincides with grokking, (b) Input-
output mutual information stabilizes post-grokking. 7. Compare mutual
information dynamics between different operations and model sizes to
identify common patterns in successful grokking.",
"Interestingness": 9,
"Feasibility": 6,
"Novelty": 9,
"novel": true
```

Idea 16/50 - sparse_subnetworks_grokking

```
"Name": "sparse_subnetworks_grokking",
"Title": "Sparse Subnetworks in Grokking: Investigating the Emergence of
Critical Structures During Algorithmic Learning",
"Experiment": "1. Implement a simple magnitude-based pruning function for
the Transformer model. 2. Modify the training loop to perform pruning at
key points: before training, just before grokking (based on validation
accuracy), and after grokking. 3. For each pruning point, create sparse
networks at different sparsity levels (e.g., 50%
these sparse networks from the original initialization for a fixed number
of steps. 5. Track metrics: validation accuracy of sparse networks,
sparsity level, and grokking speed (if it occurs). 6. Plot the performance
of sparse networks at different sparsity levels and pruning points. 7.
Compare the structure and performance of sparse networks found before and
after grokking across different operations.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 17/50 - positional_encoding_grokking

```
"Name": "positional_encoding_grokking",
"Title": "Inductive Biases in Grokking: The Impact of Positional Encoding
Schemes on Algorithmic Learning",
"Experiment": "1. Modify the Transformer class to support three positional
encoding schemes: sinusoidal (current), learned embeddings, and a simple
binary encoding (e.g., [0,1,0,1,0] for ’a o b = c’). 2. Implement these
encoding schemes, ensuring they work with the existing sequence length. 3.
Run experiments for each encoding scheme across all datasets, tracking:
time to grokking (99%
training loss, and attention entropy. 4. Analyze how different encoding
schemes affect attention patterns and grokking behavior for each operation
type. 5. Compare generalization capabilities on sequences with shuffled
operands (e.g., ’b o a = c’). 6. Correlate encoding scheme performance with
operation complexity to identify potential interactions between input
representation and task structure. 7. Discuss implications for designing
transformers for specific algorithmic tasks based on findings.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

Idea 18/50 - adversarial_robustness_grokking

```
"Name": "adversarial_robustness_grokking",
"Title": "Adversarial Robustness During Grokking: Tracking Vulnerability
Evolution in Algorithmic Learning",
"Experiment": "1. Implement a simple perturbation method: randomly flip 1-2
bits in the input representation for modular arithmetic, and swap 1-2
elements for permutations. 2. Modify the training loop to generate
perturbed inputs and evaluate model performance on them every 500 steps. 3.
Track metrics: normal validation accuracy, accuracy on perturbed inputs,
and ’robustness gap’ (difference between normal and perturbed accuracy). 4.
Plot the evolution of robustness to perturbations alongside the grokking
curve. 5. Compare robustness before, during, and after grokking across
different operations. 6. Analyze examples of successful perturbations at
different stages of training. 7. Investigate potential correlations between
the timing of grokking and changes in robustness to perturbations.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 19/50 - critical_periods_grokking

```
"Name": "critical_periods_grokking",
"Title": "Critical Periods in Grokking: The Impact of Timed Learning Rate
Spikes on Algorithmic Learning",
"Experiment": "1. Modify the training loop to support learning rate spikes
at specific points (25%
to apply these spikes, increasing the learning rate by 10x for 100 steps.
3. Run experiments for each spike timing across all datasets (modular
arithmetic and permutations), including a control group with no spikes. 4.
Track metrics: time to grokking, final validation accuracy, and ’spike
impact’ (change in validation accuracy slope in 500 steps post-spike). 5.
Plot learning curves highlighting spike points and their impacts. 6.
Analyze how spike timing affects grokking across different operations,
comparing modular arithmetic tasks with permutations. 7. Compare attention
patterns immediately before and after impactful spikes. 8. Correlate spike
impact with the stage of learning (pre-grokking, during grokking, post-
grokking) to identify potential critical periods, assessing whether these
periods are task-specific or general across operations.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

Idea 20/50 - lottery_tickets_grokking

```
"Name": "lottery_tickets_grokking",
"Title": "Lottery Tickets in Grokking: Investigating Sparse Subnetworks
Capable of Algorithmic Learning",
"Experiment": "1. Implement an iterative magnitude pruning function for the
Transformer model. 2. Modify the training loop to support multiple rounds
of train-prune-reset cycles. 3. For each dataset, run experiments with
pruning levels of 30%
iteration, train the network to convergence, prune the specified percentage
of smallest weights, then reset remaining weights to their initial values.
5. Track metrics for each sparse network: time to grokking (or maximum
training time if grokking doesn’t occur), final validation accuracy, and
training loss. 6. Introduce a ’grokking efficiency’ metric: the ratio of
time to grokking for the sparse network vs. the dense network. For networks
that don’t grok, use the maximum training time. 7. Plot learning curves for
each pruning level, highlighting grokking points and grokking efficiency.
8. Compare the structure of sparse networks that achieve grokking across
different operations, focusing on the distribution of preserved weights in
different layers and attention heads. 9. Analyze the correlation between
pruning level and grokking efficiency across different algorithmic tasks,
including cases where grokking fails to occur.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": false
```

Idea 21/50 - algebraic_structure_grokking

```
"Name": "algebraic_structure_grokking",
"Title": "Grokking and Algebraic Structure: How Group Properties Influence
Neural Network Learning",
"Experiment": "1. Implement new dataset classes for modular multiplication
and division (modulo p, where p is prime, ensuring proper group
structures). 2. For each operation (addition, multiplication, division),
calculate and store two properties: group order and number of generators.
3. Run experiments for each operation type, tracking: time to grokking,
final validation accuracy, and the two group properties. 4. Plot learning
curves and grokking points for each operation, labeled with their group
properties. 5. Analyze the correlation between group properties and
grokking behavior (e.g., time to grokking, steepness of accuracy
improvement). 6. Compare attention patterns across operations, focusing on
how they reflect the underlying group structure (e.g., uniformity for
commutative operations). 7. Test the model’s ability to generalize by
evaluating on compositions of learned operations (e.g., a * b + c mod p)
after training on individual operations.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 22/50 - mdl_grokking

```
"Name": "mdl_grokking",
"Title": "Minimum Description Length and Grokking: Investigating the
Relationship Between Model Compression and Algorithmic Learning",
"Experiment": "1. Implement functions to calculate model complexity: (a) L2
norm of weights, (b) number of bits to store parameters at different
precisions, (c) effective number of parameters using BIC. 2. Modify the
training loop to track these complexity measures alongside existing
metrics. 3. Run experiments across all datasets, recording complexity
measures, validation accuracy, and training loss at regular intervals. 4.
Plot the evolution of model complexity alongside the grokking curve. 5.
Analyze the correlation between sudden decreases in model complexity and
the onset of grokking, including statistical tests for significance. 6.
Compare complexity dynamics across different operations and model sizes. 7.
Visualize weight distributions at pre-grokking, during grokking, and post-
grokking stages. 8. Implement and compare two early stopping mechanisms:
one based on model complexity stabilization and another based on validation
loss stabilization.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 23/50 - invariance_learning_grokking

```
"Name": "invariance_learning_grokking",
"Title": "Learning Invariances in Grokking: Tracking Symmetry Awareness
During Algorithmic Learning",
"Experiment": "1. Modify AbstractDataset to generate transformed versions
of inputs (cyclic shifts for modular arithmetic, relabelings for
permutations). 2. Update the evaluation function to test model predictions
on both original and transformed inputs. 3. Implement an ’invariance score’
metric: mean absolute difference between predictions on original and
transformed inputs. 4. Modify the training loop to calculate and store the
invariance score at regular intervals. 5. Run experiments across all
datasets, tracking the invariance score alongside existing metrics. 6. Plot
the evolution of the invariance score alongside the grokking curve. 7.
Analyze how the invariance score changes before, during, and after
grokking. 8. Compare invariance learning across different operations and
model sizes. 9. Investigate correlation between invariance score and
generalization performance.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 24/50 - grokking_double_descent

```
"Name": "grokking_double_descent",
"Title": "Grokking and Double Descent: Exploring the Intersection of Two
Deep Learning Phenomena",
"Experiment": "1. Create a range of model sizes by varying num_layers (1 to
8) and dim_model (32 to 512). 2. For each dataset, train models of
different sizes, tracking validation accuracy, training loss, and time to
grokking (99%
parameters to identify double descent behavior. 4. On the same plot, mark
the point where grokking occurs for each model size. 5. Analyze the
relationship between grokking timing and the different regimes of the
double descent curve (under-parameterized, critical, over-parameterized).
6. Calculate the correlation between model size and time to grokking. 7.
Compare double descent and grokking behavior across different operations
(modular arithmetic vs. permutations). 8. Investigate whether grokking
consistently occurs in a specific regime of the double descent curve.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": false
```

Idea 25/50 - ntk_alignment_grokking

```
"Name": "ntk_alignment_grokking",
"Title": "NTK-Output Alignment in Grokking: Tracking Feature Learning
Dynamics in Algorithmic Tasks",
"Experiment": "1. Implement a function to compute the NTK-output alignment:
the cosine similarity between the NTK’s top eigenvector and the output
gradient. 2. Modify the training loop to compute and store this alignment
metric every 100 steps. 3. Run experiments across all datasets, tracking
NTK-output alignment alongside validation accuracy and training loss. 4.
Plot the evolution of NTK-output alignment alongside the grokking curve. 5.
Analyze how the alignment changes before, during, and after grokking,
identifying any consistent patterns across different operations. 6.
Investigate correlations between sudden changes in alignment and the onset
of grokking. 7. Compare alignment dynamics for models that achieve grokking
vs. those that don’t. 8. Experiment with using the alignment metric as an
early stopping criterion or to adjust learning rates dynamically. 9.
Discuss implications of findings for understanding feature learning and
generalization in grokking.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 26/50 - loss_landscape_grokking

```
"Name": "loss_landscape_grokking",
"Title": "Loss Landscape Evolution in Grokking: Geometric Insights into
Algorithmic Learning",
"Experiment": "1. Implement functions to compute and visualize 2D loss
landscapes using filter-wise normalization. 2. Modify the training loop to
save model checkpoints at key points: start of training, 25%
just before grokking (based on validation accuracy), during grokking, and
after grokking. 3. For each checkpoint, compute and store 2D loss landscape
visualizations. 4. Define quantitative metrics for loss landscape
characteristics: (a) local smoothness (average gradient magnitude), (b)
global convexity (ratio of loss at edges to center), (c) barrier height
(maximum loss along minimum loss path). 5. Run experiments across all
datasets, generating loss landscapes and computing metrics at key points.
6. Create side-by-side comparisons of loss landscapes at different stages
of training for each operation. 7. Analyze how loss landscape metrics
change before, during, and after grokking. 8. Compare loss landscape
evolution between operations that grok quickly vs. slowly. 9. Investigate
correlations between changes in loss landscape metrics and the onset of
grokking.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 27/50 - neural_collapse_grokking

```
"Name": "neural_collapse_grokking",
"Title": "Neural Collapse in Grokking: Investigating Feature Geometry
During Algorithmic Learning",
"Experiment": "1. Modify Transformer to output final layer features. 2.
Implement functions to compute class means and covariances. 3. Calculate
simplified neural collapse metrics: (a) average cosine similarity between
class means, (b) ratio of within-class to between-class variances. 4. Track
these metrics every 500 steps during training. 5. Run experiments on
modular arithmetic and permutation datasets. 6. Plot neural collapse
metrics alongside grokking curves. 7. Analyze changes in metrics before,
during, and after grokking. 8. Compare neural collapse dynamics between
operations that grok quickly vs. slowly. 9. Visualize class mean
trajectories in 2D/3D using PCA. 10. Discuss implications for understanding
both grokking and general neural network learning dynamics.",
"Interestingness": 9,
"Feasibility": 6,
"Novelty": 9,
"novel": true
```

Idea 28/50 - data_augmentation_grokking

```
"Name": "data_augmentation_grokking",
"Title": "Data Augmentation in Grokking: The Impact of Input
Transformations on Algorithmic Learning",
"Experiment": "1. Implement task-specific augmentations: (a) For modular
arithmetic: add random offsets (mod p) to inputs. (b) For permutations:
apply random permutations to inputs and outputs. 2. Modify GroupDataset to
apply augmentations with 0%
for each augmentation level across all datasets. 4. Track metrics: time to
grokking (99%
’augmentation generalization gap’ (difference between augmented and non-
augmented validation accuracy). 5. Plot learning curves and generalization
gaps for each augmentation level. 6. Analyze the correlation between
augmentation level and grokking speed. 7. Compare attention patterns
between augmentation levels to understand representation changes. 8.
Discuss implications for designing data augmentation strategies in
algorithmic learning tasks.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 8,
"novel": true
```

Idea 29/50 - emergent_grokking

```
"Name": "emergent_grokking",
"Title": "Emergent Abilities in Grokking: Investigating Scale-Dependent
Algorithmic Learning",
"Experiment": "1. Modify existing datasets to include ’simple’ and
’complex’ versions (e.g., mod sum with small vs. large primes). 2. Adjust
Transformer class to scale from tiny (1 layer, 64 dim) to medium (4 layers,
512 dim). 3. For each operation, train models of increasing size, tracking
grokking time and performance on both simple and complex versions. 4.
Implement a generalization test for each operation (e.g., mod sum with even
larger primes). 5. Plot learning curves for different model sizes,
highlighting grokking points. 6. Create heatmaps of model size vs.
operation complexity, showing grokking time and generalization test
results. 7. Perform statistical analysis to identify significant jumps in
performance across model sizes, using metrics such as accuracy increase
rate and time to reach 99%
behavior patterns across different operation types.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 30/50 - functional_modularity_grokking

```
"Name": "functional_modularity_grokking",
"Title": "Functional Modularity in Grokking: Analyzing Emergent
Specialization in Transformer Networks During Algorithmic Learning",
"Experiment": "1. Implement functions to track weight update patterns and
attention focus for each layer and head. 2. Modify the training loop to
compute and store these metrics at regular intervals. 3. Define a
’functional modularity score’ based on the consistency of weight updates
and attention patterns for specific input types. 4. Run experiments across
all datasets, tracking the functional modularity score alongside existing
metrics. 5. Plot the evolution of functional modularity alongside the
grokking curve. 6. Analyze how functional modularity changes before,
during, and after grokking. 7. Visualize the most consistent patterns at
different stages of training and interpret their functions. 8. Compare
functional modularity dynamics between different operations and model
sizes. 9. Investigate correlations between functional modularity and
grokking speed or generalization performance.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 31/50 - information_compression_grokking

```
"Name": "information_compression_grokking",
"Title": "Information Compression in Grokking: Analyzing Representational
Dynamics During Algorithmic Learning",
"Experiment": "1. Modify Transformer class to include a bottleneck layer
(smaller dimension linear layer) after the encoder. 2. Implement function
to compute activation sparsity (%
bottleneck layer. 3. Update training loop to compute and store activation
sparsity and gradient magnitudes of the bottleneck layer at regular
intervals. 4. Run experiments with different bottleneck sizes (e.g., 25%
50%
to grokking, final validation accuracy, activation sparsity, and gradient
magnitudes. 6. Plot activation sparsity and gradient magnitude evolution
alongside grokking curves for each bottleneck size. 7. Analyze how these
metrics change before, during, and after grokking. 8. Test generalization
by evaluating models on slightly out-of-distribution examples (e.g., larger
numbers in modular arithmetic). 9. Investigate correlation between optimal
compression (measured by activation sparsity) and grokking speed,
generalization performance.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 32/50 - critical_learning_periods_grokking

```
"Name": "critical_learning_periods_grokking",
"Title": "Critical Learning Periods in Grokking: Temporal Dynamics of
Algorithmic Understanding",
"Experiment": "1. Modify the training loop to support ’intervention
periods’ where learning rate is increased by 5x for 100 steps. 2. Implement
a sliding window intervention strategy, with windows of 500 steps, starting
every 250 steps. 3. Run experiments for each window across all datasets and
three model sizes (small, medium, large), including a control group with no
interventions. 4. Track metrics: time to grokking, final validation
accuracy, and ’intervention impact’ (area under the validation accuracy
curve for 500 steps post-intervention). 5. Plot learning curves
highlighting intervention windows and their impacts. 6. Create heatmaps
visualizing intervention impact across time windows and model sizes for
each operation. 7. Analyze how intervention timing affects grokking across
different operations and model sizes. 8. Compare attention patterns
immediately before and after impactful interventions. 9. Investigate
whether certain operations or model sizes have more pronounced critical
periods than others. 10. Discuss implications for curriculum design in
machine learning and potential applications in continual and transfer
learning.",
"Interestingness": 9,
"Feasibility": 7,
"Novelty": 9,
"novel": true
```

Idea 33/50 - simplicity_bias_grokking

```
"Name": "simplicity_bias_grokking",
"Title": "Simplicity Bias in Grokking: Analyzing Weight Matrix Complexity
During Algorithmic Learning",
"Experiment": "1. Modify AbstractDataset to include two complexity levels
for each operation (e.g., small vs. large prime for modular arithmetic,
short vs. long permutations). 2. Implement a function to compute the
effective rank of weight matrices using singular value decomposition. 3.
Update the training loop to compute and store the effective rank for each
layer every 500 steps. 4. Run experiments across all datasets and both
complexity levels, tracking effective rank alongside existing metrics. 5.
Plot the evolution of effective rank alongside grokking curves for each
complexity level and operation. 6. Analyze how effective rank changes
before, during, and after grokking, and how this relates to task
complexity. 7. Investigate correlations between effective rank dynamics and
grokking speed or generalization performance. 8. Compare effective rank
patterns across different operations and model sizes. 9. Contrast effective
rank dynamics between operations that grok quickly versus those that grok
slowly or fail to grok. 10. Experiment with using effective rank as an
indicator for the onset of grokking.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 34/50 - lucky_initializations_grokking

```
"Name": "lucky_initializations_grokking",
"Title": "Lucky Initializations in Grokking: Identifying and Analyzing
Favorable Starting Points for Algorithmic Learning",
"Experiment": "1. Implement a function to generate and store 50 random
initializations for the Transformer model. 2. Modify the training loop to
support training from stored initializations and different learning rates.
3. For each dataset, train models from the 50 initializations with 3
learning rates, tracking ’grokking efficiency’ (ratio of validation
accuracy to training steps at 99%
initializations (top 20%
characteristics of lucky initializations: weight distribution statistics,
layerwise norms, and attention pattern initialization. 6. Implement a
function to visualize the loss landscape around initial points using
filter-wise normalization. 7. Compare lucky initializations across
different operations to identify common patterns. 8. Develop a simple
predictor for initialization ’luckiness’ based on identified
characteristics. 9. Test transfer of lucky initializations across tasks and
learning rates.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

Idea 35/50 - relative_attention_grokking

```
"Name": "relative_attention_grokking",
"Title": "Relative Positional Attention and Its Impact on Grokking in
Algorithmic Learning",
"Experiment": "1. Modify the DecoderBlock class to support two attention
types: standard (current) and relative positional. 2. Implement relative
positional attention, ensuring it works with the existing sequence length.
3. Update the Transformer class to accept an attention_type parameter. 4.
Run experiments for both attention types across all datasets, tracking:
time to grokking (99%
training loss, grokking transition sharpness (rate of validation accuracy
increase), and post-grokking stability (variance in validation accuracy
after reaching 99%
highlighting grokking points and transition periods. 6. Visualize and
compare attention patterns between the two mechanisms at key stages: pre-
grokking, during grokking transition, and post-grokking. 7. Analyze how
relative positional attention affects grokking behavior, transition
sharpness, and stability for each operation type compared to standard
attention. 8. Investigate correlations between attention type and grokking
speed or post-grokking stability. 9. Discuss implications for designing
transformers for specific algorithmic tasks based on findings.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 36/50 - grokking_task_interference

```
"Name": "grokking_task_interference",
"Title": "Grokking and Task Interference: Exploring the Stability of
Algorithmic Understanding",
"Experiment": "1. Modify the training loop to support learning two modular
arithmetic operations sequentially (e.g., addition then multiplication). 2.
Implement a task scheduler that switches between tasks at regular
intervals. 3. Create a ’dual-task evaluation’ function to assess
performance on both tasks simultaneously. 4. Track metrics: time to
grokking for each task, performance on the first task while learning the
second, and a ’grokking stability’ score (maintenance of >95%
task 1 while learning task 2). 5. Run experiments with different task
switching frequencies. 6. Analyze how grokking on one task affects learning
speed and grokking on the subsequent task. 7. Visualize attention patterns
before and after introducing the second task to understand representation
changes. 8. Investigate the correlation between grokking speed on the first
task and stability of that understanding when learning the second task. 9.
Compare results with a baseline of learning both tasks simultaneously to
isolate the effects of sequential learning.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 37/50 - attention_inductive_bias_grokking

```
"Name": "attention_inductive_bias_grokking",
"Title": "Inductive Biases in Attention Mechanisms: Their Impact on
Grokking in Algorithmic Learning",
"Experiment": "1. Modify DecoderBlock class to support two attention
mechanisms: standard dot-product and additive (Bahdanau). 2. Implement
these attention mechanisms, ensuring compatibility with existing
architecture. 3. Update Transformer class to accept an attention_type
parameter. 4. Select a subset of most illustrative datasets based on
preliminary experiments. 5. Run experiments for each attention type on
selected datasets, tracking: time to grokking (99%
final validation accuracy, training loss, and ’grokking transition
sharpness’ (defined as the maximum rate of validation accuracy increase
over any 500-step window). 6. Implement a simple generalization test using
slightly out-of-distribution examples (e.g., larger numbers for modular
arithmetic). 7. Plot learning curves for each attention type, highlighting
grokking points and transition periods. 8. Analyze how different attention
mechanisms affect grokking behavior, transition sharpness, and
generalization performance for each operation type. 9. Visualize attention
patterns for each mechanism at key stages: pre-grokking, during grokking
transition, and post-grokking. 10. Discuss implications for designing
transformers with appropriate inductive biases for specific types of
algorithmic learning tasks.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

Idea 38/50 - gradient_dynamics_grokking

```
"Name": "gradient_dynamics_grokking",
"Title": "Gradient Dynamics in Grokking: Analyzing Information Flow
Efficiency During Algorithmic Learning",
"Experiment": "1. Modify the training loop to compute gradient statistics
(sparsity and magnitude distribution) for each layer. 2. Implement
functions to calculate gradient sparsity (%
magnitude percentiles. 3. Update training process to store these metrics
every 500 steps. 4. Run experiments across all datasets, tracking gradient
metrics alongside existing performance metrics. 5. Plot the evolution of
gradient sparsity and magnitude distributions alongside grokking curves. 6.
Analyze how gradient dynamics change before, during, and after grokking. 7.
Compare gradient patterns between operations that grok quickly vs. slowly.
8. Investigate correlations between changes in gradient dynamics and
grokking speed or generalization performance. 9. Visualize gradient flow
patterns at key stages: pre-grokking, during grokking transition, and post-
grokking.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 39/50 - adaptive_curriculum_grokking

```
"Name": "adaptive_curriculum_grokking",
"Title": "Adaptive Curriculum Learning in Grokking: Optimizing Example
Difficulty for Efficient Algorithmic Understanding",
"Experiment": "1. Modify AbstractDataset to include a difficulty scoring
function (e.g., input magnitude for modular arithmetic, cycle length for
permutations). 2. Implement adaptive sampling strategy: start with easiest
20%
level exceeds 90%
tracking difficulty of selected examples. 4. Run experiments comparing
adaptive curriculum, random sampling, and static curriculum (increasing
difficulty linearly) across all datasets. 5. Track metrics: time to
grokking, final validation accuracy, learning trajectory smoothness, and
example difficulty distribution over time. 6. Analyze relationship between
difficulty progression and grokking onset. 7. Visualize learning curves and
difficulty progression for each strategy. 8. Compare consistency and speed
of grokking across different random seeds for each strategy. 9. Analyze
computational efficiency by comparing total number of examples needed to
achieve grokking for each strategy. 10. Compare attention patterns at key
points (pre-grokking, during grokking, post-grokking) across strategies to
understand how adaptive curriculum affects internal representations.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 40/50 - task_structure_grokking

```
"Name": "task_structure_grokking",
"Title": "Task Structure and Grokking: Investigating the Relationship
Between Algorithmic Complexity and Learning Dynamics",
"Experiment": "1. Modify AbstractDataset to include a
’structural_complexity’ score based on: a) number of unique outputs, b)
input-output correlation, c) algebraic degree for modular operations or
cycle structure for permutations. 2. Extend existing dataset classes to
include a wider range of operations (e.g., modular addition,
multiplication, exponentiation; simple and complex permutations). 3. Run
experiments across all operations, tracking time to grokking, final
validation accuracy, and learning curve smoothness. 4. Plot grokking
metrics against structural complexity scores, comparing trends between
modular arithmetic and permutation tasks. 5. Analyze correlation between
structural complexity and grokking behavior. 6. Compare attention patterns
and gradient flows across tasks of different complexity. 7. Implement a
generalization test where models trained on simpler structures are
evaluated on more complex ones. 8. Discuss implications for neural network
learning on structured vs. unstructured tasks in general machine learning
contexts.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

Idea 41/50 - numerical_base_grokking

```
"Name": "numerical_base_grokking",
"Title": "Numerical Base and Grokking: How Input Representation Affects
Pattern Recognition in Algorithmic Learning",
"Experiment": "1. Modify AbstractDataset and modular arithmetic dataset
classes to support binary and decimal bases. 2. Implement functions to
convert between bases and adjust the encode/decode methods. 3. Update the
Transformer class to handle variable input lengths. 4. Run experiments for
binary and decimal bases on modular addition and multiplication tasks. 5.
Track metrics: time to grokking (99%
accuracy, training loss, and ’cross-base generalization’ (accuracy when
testing on the other base). 6. Plot learning curves for each base,
highlighting grokking points. 7. Compare learning curves for binary (0-3)
vs decimal (0-9) to isolate base effects from sequence length. 8. Analyze
how different bases affect grokking speed and pattern recognition. 9.
Compare attention patterns across bases at key stages: pre-grokking, during
grokking, and post-grokking. 10. Discuss implications for choosing input
representations in mathematical machine learning tasks.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

Idea 42/50 - activation_function_grokking

```
"Name": "activation_function_grokking",
"Title": "Activation Functions and Grokking: Investigating the Role of Non-
linearity in Algorithmic Learning and Generalization",
"Experiment": "1. Modify the DecoderBlock class to support multiple
activation functions (ReLU, GELU, Tanh). 2. Update the Transformer class to
accept an activation_type parameter, allowing for both uniform and hybrid
activation setups. 3. Run experiments comparing the baseline (GELU) with
ReLU, Tanh, and a hybrid setup (ReLU in lower layers, Tanh in upper layers)
across all datasets. 4. Track metrics: time to grokking (99%
accuracy), final validation accuracy, training loss, ’grokking transition
sharpness’, and gradient flow statistics. 5. Plot learning curves for each
activation setup, highlighting grokking points and transition periods. 6.
Visualize decision boundaries at different training stages for each
activation setup. 7. Analyze how different activation functions affect
grokking behavior, transition sharpness, and final performance for each
operation type. 8. Compare hidden representations (using t-SNE) across
activation setups at key stages: pre-grokking, during grokking transition,
and post-grokking. 9. Investigate the relationship between activation
function properties and the trade-off between memorization and
generalization. 10. Discuss implications for choosing activation functions
in tasks requiring pattern discovery and generalization beyond algorithmic
learning.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

Idea 43/50 - phase_transition_grokking

```
"Name": "phase_transition_grokking",
"Title": "Grokking as a Phase Transition: Characterizing Critical Behavior
in Algorithmic Learning",
"Experiment": "1. Implement functions to track key metrics: validation
accuracy, training loss, gradient norm, and weight norm. 2. Modify training
loop to compute and store these metrics every 100 steps. 3. Run experiments
across all datasets, with finer-grained tracking (every 10 steps) around
the suspected grokking point. 4. Implement analysis tools to detect sudden
changes or discontinuities in metrics. 5. Plot all metrics on a single,
multi-axis graph to visualize potential phase transitions. 6. Calculate
susceptibility using fluctuations in validation accuracy near the grokking
point. 7. Analyze scaling behavior of susceptibility to identify critical
exponents, if any. 8. Compare phase transition characteristics across
different operations and model sizes. 9. Investigate whether manipulating
learning rate or gradient clipping can induce or prevent grokking phase
transitions.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": false
```

Idea 44/50 - effective_dimension_grokking

```
"Name": "effective_dimension_grokking",
"Title": "Effective Dimension Dynamics in Grokking: Analyzing
Representational Complexity During Algorithmic Learning",
"Experiment": "1. Implement functions to compute the rank and top-k
singular values of weight matrices. 2. Modify the training loop to compute
and store these metrics every 500 steps for each layer. 3. Run experiments
across all datasets, tracking rank and singular value distributions
alongside existing performance metrics. 4. Implement a simple MLP baseline
that doesn’t exhibit grokking for comparison. 5. Plot the evolution of rank
and singular value distributions alongside grokking curves for both
Transformer and MLP models. 6. Analyze how these metrics change before,
during, and after grokking in the Transformer, contrasting with the MLP. 7.
Compare rank dynamics between operations that grok quickly vs. slowly. 8.
Investigate correlations between changes in rank/singular values and
grokking speed or generalization performance. 9. Visualize the relationship
between these metrics and other performance indicators at different stages
of training.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

Idea 45/50 - representation_entropy_grokking

```
"Name": "representation_entropy_grokking",
"Title": "Representation Entropy in Grokking: Tracking the Simplification
of Learned Concepts",
"Experiment": "1. Implement a function to compute the entropy of the
model’s internal representations. 2. Modify the Transformer class to output
intermediate representations. 3. Update the training loop to compute and
store the representation entropy every 500 steps. 4. Run experiments across
all datasets, including configurations that lead to successful grokking and
those that don’t (e.g., by varying model size or learning rate). 5. Track
entropy alongside existing performance metrics. 6. Plot the evolution of
representation entropy alongside grokking curves for both successful and
unsuccessful cases. 7. Analyze how representation entropy changes before,
during, and after grokking in successful cases, and compare with
unsuccessful cases. 8. Investigate correlations between changes in
representation entropy and grokking speed or generalization performance. 9.
Visualize the relationship between entropy and other performance indicators
at different stages of training. 10. Plot entropy distributions across
different layers of the model to understand how different parts contribute
to concept simplification.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 46/50 - mutual_information_grokking

```
"Name": "mutual_information_grokking",
"Title": "Mutual Information Dynamics in Grokking: Tracing Information Flow
During Algorithmic Learning",
"Experiment": "1. Modify Transformer class to output representations from
input embedding, middle layer, and final layer. 2. Implement MINE (Mutual
Information Neural Estimation) for efficient mutual information
approximation. 3. Update training loop to compute and store mutual
information estimates between input-middle, input-output, and middle-output
every 500 steps. 4. Run experiments across all datasets, tracking mutual
information alongside existing performance metrics. 5. Plot the evolution
of mutual information alongside grokking curves and generalization gap. 6.
Analyze how mutual information changes before, during, and after grokking,
particularly in relation to the generalization gap. 7. Compare mutual
information dynamics between operations that grok quickly vs. slowly. 8.
Investigate correlations between changes in mutual information and grokking
speed or generalization performance.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 47/50 - lottery_tickets_grokking

```
"Name": "lottery_tickets_grokking",
"Title": "Lottery Tickets in Grokking: Sparse Subnetworks and Sudden
Generalization",
"Experiment": "1. Implement iterative magnitude pruning for the Transformer
model. 2. Modify training loop for train-prune-reset cycles. 3. For each
dataset, run experiments with pruning levels of 50%
iterations. 4. Track metrics: time to grokking, final validation accuracy,
training loss, and ’grokking efficiency’ (ratio of time to grokking for
sparse vs. dense network). 5. Plot learning curves for each pruning level,
highlighting grokking points. 6. Compare sparse network structures that
achieve grokking across operations. 7. Analyze correlation between pruning
level and grokking efficiency. 8. Implement simple MLP baseline without
grokking for comparison. 9. Visualize weight distributions of winning
tickets pre- and post-grokking.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 8,
"novel": false
```

Idea 48/50 - architecture_inductive_bias_grokking

```
"Name": "architecture_inductive_bias_grokking",
"Title": "Architectural Inductive Biases and Grokking: Comparing Sudden
Generalization Across Neural Network Types",
"Experiment": "1. Implement simplified 1D CNN and LSTM model classes
compatible with existing sequence-based datasets. 2. Modify training loop
to support multiple model types. 3. Run experiments comparing Transformer,
1D CNN, and LSTM models across modular arithmetic datasets. 4. Track
metrics: time to grokking, final validation accuracy, training loss, and
architecture-specific indicators (attention patterns for Transformer,
filter activations for CNN, forget gate activations for LSTM). 5. Plot
learning curves for each architecture, highlighting grokking points. 6.
Analyze how different architectures affect grokking behavior, speed, and
final performance for each operation type. 7. Compare internal
representations (using t-SNE) across architectures at key stages: pre-
grokking, during grokking transition, and post-grokking. 8. Investigate the
relationship between architectural inductive biases and the trade-off
between memorization and generalization in modular arithmetic tasks.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

Idea 49/50 - shortcut_learning_grokking

```
"Name": "shortcut_learning_grokking",
"Title": "Shortcut Learning and Grokking: The Interplay Between Surface
Patterns and Deep Understanding in Algorithmic Learning",
"Experiment": "1. Modify AbstractDataset to include operation-specific
shortcuts: for modular arithmetic, make the result always even if the first
operand is even; for permutations, always swap the first two elements. 2.
Implement a function to gradually remove these shortcuts over training by
reducing their frequency. 3. Update the training loop to apply the shortcut
removal function. 4. Add a ’shortcut reliance’ metric: the accuracy
difference between shortcut-following and shortcut-violating examples. 5.
Run experiments with varying shortcut removal rates across datasets. 6.
Track metrics: time to grokking, final validation accuracy, shortcut
reliance over time, and performance on a shortcut-free test set. 7. Plot
learning curves and shortcut reliance alongside grokking curves. 8. Analyze
how shortcut presence and removal affect grokking timing and quality. 9.
Compare attention patterns between models trained with and without
shortcuts at key stages.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

Idea 50/50 - grokking_forgetting_complexity

```
"Name": "grokking_forgetting_complexity",
"Title": "Grokking and Forgetting: The Interplay of Task Complexity and
Sudden Generalization in Algorithmic Learning",
"Experiment": "1. Modify ModSumDataset to support multiple complexity
levels (e.g., modular addition with increasing prime moduli). 2. Update the
training loop to gradually introduce higher complexity levels while
continuously evaluating on all levels. 3. Implement a ’multi-complexity
evaluation’ function to assess performance across all complexity levels
simultaneously. 4. Track metrics: time to grokking for each complexity
level, performance on lower complexity levels when grokking occurs on a
higher level, and a ’complexity forgetting score’ (decrease in accuracy on
lower complexity levels). 5. Analyze the correlation between grokking
events and performance changes on other complexity levels. 6. Compare
internal representations (using cosine similarity of hidden states) across
complexity levels before and after grokking events. 7. Investigate trends
in grokking speed across increasing complexity levels. 8. Plot learning
curves for all complexity levels simultaneously, highlighting grokking
points and potential forgetting events. 9. Visualize the evolution of
representation similarities over time using heatmaps.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

## 附录 D 亮点生成论文

在下面的小节中，我们展示 AI 科学生成论文的亮点示例。对每篇论文，我们还给出生成的想法、代码链接以及末尾的自动化评审。

### D.1 DualScale Diffusion: Adaptive Feature Balancing for Low-Dimensional Generative Models

该想法是在一次 Sonnet 3.5 运行的第 6 次迭代中提出的。

想法（Idea）

```
"Name": "adaptive_dual_scale_denoising",
"Title": "Adaptive Dual-Scale Denoising for Dynamic Feature Balancing in
Low-Dimensional Diffusion Models",
"Experiment": "Modify MLPDenoiser to implement a dual-scale processing
approach with two parallel branches: a global branch for the original input
and a local branch for an upscaled input. Introduce a learnable, timestep-
conditioned weighting factor to dynamically balance the contributions of
global and local branches. Train models with both the original and new
architecture on all datasets. Compare performance using KL divergence and
visual inspection of generated samples. Analyze how the weighting factor
evolves during the denoising process and its impact on capturing global
structure vs. local details across different datasets and timesteps.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

代码链接：<https://github.com/SakanaAI/AI-Scientist/tree/main/example_papers/adaptive_dual_scale_denoising>.

论文全文见 [highlighted_papers/diffusion/adaptive_dual_scale_denoising/adaptive_dual_scale_denoising.pdf](https://highlighted_papers/diffusion/adaptive_dual_scale_denoising/adaptive_dual_scale_denoising.pdf)

评审（Review）

```
"Summary": "The paper introduces an adaptive dual-scale denoising approach
for low-dimensional diffusion models, aiming to balance global structure
and local details in generated samples. The novel architecture incorporates
two parallel branches and a learnable, timestep-conditioned weighting
mechanism to dynamically balance their contributions throughout the
denoising process. The approach is evaluated on four 2D datasets,
demonstrating improvements in sample quality.",
"Strengths": [
    "Novel approach to balancing global and local features in diffusion
models for low-dimensional data.",
    "Comprehensive empirical evaluation on multiple 2D datasets.",
    "Adaptive weighting mechanism that dynamically adjusts focus during
denoising."
],
"Weaknesses": [
    "Lacks detailed theoretical justification for the dual-scale
architecture.",
    "Computational cost is significantly higher, which may limit practical
applicability.",
    "Some sections are not clearly explained, such as the autoencoder
aggregator and weight evolution analysis.",
    "Limited diversity in the datasets used for evaluation. More complex,
real-world datasets could strengthen claims.",
    "Insufficient ablation studies and analysis on specific design choices
like different types of aggregators."
],
"Originality": 4,
"Quality": 3,
"Clarity": 3,
"Significance": 3,
"Questions": [
    "Can you provide a more detailed theoretical justification for the
dual-scale architecture?",
    "What impact do different types of aggregators have on the model’s
performance?",
    "How does the model perform on more complex, real-world low-dimensional
datasets?",
    "Can the computational cost be reduced without sacrificing
performance?"
],
"Limitations": [
    "The paper should address the high computational cost and explore ways
to optimize it.",
    "The limited diversity of datasets and lack of detailed theoretical
backing for the proposed architecture are notable limitations."
],
"Ethical Concerns": false,
"Soundness": 3,
"Presentation": 3,
"Contribution": 3,
"Overall": 5,
"Confidence": 4,
"Decision": "Reject"
```

### D.2 Multi-scale Grid Noise Adaptation: Enhancing Diffusion Models For Low-dimensional Data

该想法是在一次 Claude 运行的第 35 次迭代中提出的。

想法（Idea）

```
"Name": "grid_based_noise_adaptation",
"Title": "Grid-Based Noise Adaptation for Enhanced Low-Dimensional
Diffusion Models",
"Experiment": "1. Modify NoiseScheduler to support grid-based noise level
adjustments. 2. Implement a simple grid structure (e.g., 10x10) to store
learnable noise adjustment factors. 3. Adjust MLPDenoiser to incorporate
the grid-based noise level in its computations. 4. Modify the training loop
to include the grid parameters in the optimization process. 5. Adapt the
sampling process to use the grid-based noise levels during inference. 6.
Train models with both standard and grid-based noise adaptation approaches
on all datasets. 7. Compare KL divergence, sample quality, and convergence
speed between the two approaches. 8. Introduce a ’noise adaptation
effectiveness’ metric by measuring the variance of learned grid values. 9.
Visualize the learned noise adjustment grid at different timesteps. 10.
Analyze computational overhead and discuss trade-offs between model
complexity and performance gains.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

代码链接：<https://github.com/SakanaAI/AI-Scientist/tree/main/example_papers/grid_based_noise_adaptation>.

论文全文见 [highlighted_papers/diffusion/grid_based_noise_adaptation/grid_based_noise_adaptation.pdf](https://highlighted_papers/diffusion/grid_based_noise_adaptation/grid_based_noise_adaptation.pdf)

评审（Review）

```
"Summary": "The paper introduces a multi-scale grid-based noise adaptation
mechanism for diffusion models to improve their performance on low-
dimensional datasets. It employs a combination of coarse (5x5) and fine
(20x20) grids to dynamically adjust noise levels during the diffusion
process, with L1 regularization encouraging sparsity in fine-grained
adjustments. The approach is evaluated on four 2D datasets: circle, dino,
line, and moons, showing improvements in sample quality and distribution
matching.",
"Strengths": [
    "The paper addresses a relevant problem in the application of diffusion
models to low-dimensional data.",
    "The proposed multi-scale grid-based noise adaptation mechanism is
novel and shows potential.",
    "The experimental results demonstrate improvements in sample quality
and distribution matching on several 2D datasets."
],
"Weaknesses": [
    "The paper lacks clarity in some sections, especially regarding the
detailed implementation of the proposed method.",
    "The experiments, while showing improvements, lack comprehensive
analyses and more ablation studies.",
    "The potential societal impact and limitations of the proposed method
are not adequately discussed.",
    "The paper does not compare the proposed method with a wide range of
existing methods, limiting the context of its contributions.",
    "There are some formatting issues, such as missing figure captions
(e.g., Figure 2).",
    "The choice of datasets, while diverse, needs better justification in
terms of their relevance and representativeness for broader applications.",
    "The computational overhead and training time increases are significant
and need more discussion regarding their practical implications."
],
"Originality": 3,
"Quality": 2,
"Clarity": 2,
"Significance": 3,
"Questions": [
    "Can the authors provide more detailed explanations of the multi-scale
grid-based noise adaptation mechanism?",
    "How does the performance of the proposed method compare to other
state-of-the-art methods for low-dimensional data generation?",
    "Can the authors discuss the potential societal impact and limitations
of their work in more detail?",
    "Can the authors provide more detailed ablation studies to isolate the
impact of coarse and fine grids, as well as L1 regularization?",
    "How does the proposed method perform on higher-dimensional datasets,
and what are the challenges anticipated in such scenarios?",
    "Can the authors elaborate on the choice of the specific grid sizes
(5x5 and 20x20)? Have alternative configurations been tested?",
    "Can the authors provide more visualizations for the generated samples,
particularly for the dino and moons datasets?",
    "Can you provide a detailed explanation of the L1 regularization term
and its impact on the results?"
],
"Limitations": [
    "The paper does not discuss the potential societal impact and
limitations of the proposed method in sufficient detail. It would be
beneficial to address these aspects to provide a more comprehensive
understanding of the work’s implications.",
    "The paper does not address the potential computational overhead and
increased training time associated with the proposed method.",
    "There is limited discussion on the generalizability of the approach to
higher-dimensional datasets or other types of data.",
    "The paper does not thoroughly address potential limitations of the
proposed method, such as increased computational complexity and dataset-
specific tuning requirements.",
    "The method’s effectiveness on higher-dimensional datasets remains
unexplored.",
    "Increased computational costs for training and inference."
],
"Ethical Concerns": false,
"Soundness": 2,
"Presentation": 2,
"Contribution": 2,
"Overall": 4,
"Confidence": 4,
"Decision": "Reject"
```

### D.3 Gan-Enhanced Diffusion: Boosting Sample Quality and Diversity

该想法是在一次 GPT-4o 运行的第 14 次迭代中提出的。

想法（Idea）

```
"Name": "gan_diffusion",
"Title": "Enhancing Diffusion Models with Generative Adversarial Networks
for Improved Sample Quality",
"Experiment": "In this experiment, we will integrate a GAN framework into
the diffusion model. Specifically, we will: (1) Implement a simple
discriminator network to distinguish between real and generated samples,
using a small MLP architecture, (2) Modify the MLPDenoiser to include an
adversarial loss term along with the existing reconstruction loss, using a
gradient penalty to improve training stability, (3) Adjust the training
loop to alternately train the discriminator and the denoiser, ensuring that
the denoiser learns to produce more realistic samples based on the feedback
from the discriminator, (4) Train the GAN-enhanced diffusion model on the
same datasets, and (5) Compare the results in terms of training time,
evaluation loss, KL divergence, and sample quality using both quantitative
metrics (e.g., KL divergence) and qualitative visual inspection.",
"Interestingness": 10,
"Feasibility": 8,
"Novelty": 10,
"novel": true
```

代码链接：<https://github.com/SakanaAI/AI-Scientist/tree/main/example_papers/gan_diffusion>.

论文全文见 [highlighted_papers/diffusion/gan_diffusion/gan_diffusion.pdf](https://highlighted_papers/diffusion/gan_diffusion/gan_diffusion.pdf)

评审（Review）

```
"Summary": "The paper proposes integrating a Generative Adversarial Network
(GAN) framework into diffusion models to improve sample quality and
diversity. The approach includes a simple discriminator network, an
adversarial loss term, and a gradient penalty to the adversarial loss.
Extensive experiments on multiple 2D datasets are conducted to validate the
approach, comparing results in terms of training time, evaluation loss, KL
divergence, and sample quality.",
"Strengths": [
    "The integration of GAN framework with diffusion models is a novel
approach to improve sample quality and diversity.",
    "The introduction of a gradient penalty to improve training stability
is a thoughtful addition.",
    "The paper provides a comprehensive evaluation on multiple 2D datasets,
using various metrics such as training time, evaluation loss, KL
divergence, and sample quality."
],
"Weaknesses": [
    "The methodology section lacks detailed explanations for certain
components, such as the exact architecture of the discriminator network and
the choice of hyperparameters.",
    "The improvements in evaluation loss and KL divergence are not
consistent across all datasets, indicating that the model’s performance may
be dataset-dependent.",
    "The experimental scope is limited to 2D datasets. Further research is
needed to evaluate the model’s performance on higher-dimensional data.",
    "The paper lacks sufficient ablation studies to isolate the
contributions of different components of the proposed method.",
    "The evaluation metrics are somewhat limited; including metrics like
FID could strengthen the evaluation.",
    "The paper does not sufficiently address the limitations of the
approach, particularly its dataset dependency and scalability to higher-
dimensional data.",
    "There is no discussion on potential negative societal impacts or
ethical concerns related to the work."
],
"Originality": 3,
"Quality": 2,
"Clarity": 2,
"Significance": 2,
"Questions": [
    "Can you provide more details on the architecture of the discriminator
network?",
    "How do the hyperparameters lambda-adv and lambda-gp affect the model’s
performance?",
    "Can you explain why the improvements are inconsistent across different
datasets?",
    "Can the authors provide more detailed descriptions of the denoiser and
discriminator networks?",
    "Have the authors considered using more comprehensive evaluation
metrics like FID?",
    "Can the authors provide more ablation studies to isolate the
contributions of the gradient penalty and adversarial loss?",
    "How would the proposed method perform on more complex and higher-
dimensional datasets?"
],
"Limitations": [
    "The paper acknowledges the increased training time and dataset
dependency of the improvements. However, it could benefit from a more
thorough exploration of different architectures and higher-dimensional
datasets.",
    "The empirical results show mixed improvements, indicating that the
model’s performance may be dataset-dependent.",
    "The paper does not explore the limitations of the proposed approach in
depth, particularly in terms of scalability to higher-dimensional data."
],
"Ethical Concerns": false,
"Soundness": 2,
"Presentation": 2,
"Contribution": 2,
"Overall": 3,
"Confidence": 4,
"Decision": "Reject"
```

### D.4 DualDiff: Enhancing Mode Capture in Low-dimensional Diffusion Models via Dual-expert Denoising

该想法是在一次 Claude 运行的第 5 次迭代中提出的。

想法（Idea）

```
"Name": "dual_expert_denoiser",
"Title": "Dual-Expert Denoiser for Improved Mode Capture in Low-Dimensional
Diffusion Models",
"Experiment": "Modify MLPDenoiser to implement a dual-expert architecture.
Create a simple gating network that outputs a single weight (sigmoid
output) based on the noisy input and timestep. Implement two expert
networks with the same structure as the original denoising network. Combine
expert outputs using the gating weight. Train models with both the original
and new architecture on all datasets, with particular focus on ’moons’ and
’dino’. Compare performance using KL divergence, sample diversity metrics
(e.g., number of modes captured), and visual inspection of generated
samples. Analyze the specialization of experts across different regions of
the data distribution.",
"Interestingness": 8,
"Feasibility": 8,
"Novelty": 8,
"novel": true
```

代码链接：<https://github.com/SakanaAI/AI-Scientist/tree/main/example_papers/dual_expert_denoiser>.

论文全文见 [highlighted_papers/diffusion/dual_expert_denoiser/dual_expert_denoiser.pdf](https://highlighted_papers/diffusion/dual_expert_denoiser/dual_expert_denoiser.pdf)

评审（Review）

```
"Summary": "The paper ’DualDiff: Enhancing Mode Capture in Low-Dimensional
Diffusion Models via Dual-Expert Denoising’ introduces a dual-expert
denoising architecture aimed at enhancing diffusion models’ performance on
low-dimensional datasets. The method uses a gating mechanism to combine two
specialized expert networks dynamically, which helps in capturing multiple
modes in low-dimensional data distributions. The paper demonstrates
substantial improvements in terms of mode capture and sample diversity,
validated through various experiments on 2D datasets like ’circle’, ’dino’,
’line’, and ’moons’.",
"Strengths": [
    "The paper addresses a relevant and challenging problem in the field of
generative modeling.",
    "The dual-expert architecture and dynamic gating mechanism are novel
and well-formulated.",
    "Extensive experiments provide strong evidence of the approach’s
effectiveness.",
    "The introduction of a diversity loss term to encourage multiple mode
capture is a valuable contribution."
],
"Weaknesses": [
    "The novelty of combining two expert networks with a gating mechanism
is somewhat incremental.",
    "The choice of datasets is limited to simple 2D shapes, which might not
fully demonstrate the generalizability of the approach.",
    "The evaluation of gating mechanism behavior is not sufficiently
detailed.",
    "The increased training and inference times are a significant drawback
that may limit practical applicability.",
    "The diversity loss term is weighted arbitrarily without thorough
justification for the chosen value.",
    "The paper lacks detailed ablation studies to isolate the impact of
different components (e.g., gating mechanism, diversity loss).",
    "Potential limitations and negative societal impacts are not adequately
addressed."
],
"Originality": 3,
"Quality": 3,
"Clarity": 3,
"Significance": 3,
"Questions": [
    "Could you provide more detailed analysis on how the gating mechanism
adapts during training?",
    "How would the model perform on higher-dimensional datasets or more
complex low-dimensional datasets?",
    "Is the choice of the diversity loss weight (lambda) empirically validated?
Could different values lead to significantly different results?",
    "Can the authors provide more details on the gating mechanism and how
it determines the weight for each expert network?",
    "How does the performance vary with different configurations of the
gating network?",
    "Can the authors explain the choice of hyperparameters, particularly
the value of lambda in the diversity loss term?",
    "Can the authors provide more detailed ablation studies to quantify the
impact of each component (e.g., gating mechanism, diversity loss)?",
    "How does the model perform with different types of aggregators for the
expert networks?",
    "Can more qualitative examples and visualizations be provided to
substantiate the claims of improved mode capture?",
    "Can you provide more details on the architecture of the expert
networks and the gating mechanism?",
    "How does the diversity loss term impact the final performance, and
what are the trade-offs?",
    "Can you include more comprehensive ablation studies to evaluate the
impact of each component of the proposed method?",
    "What are the computational costs associated with the dual-expert
architecture, and how do they compare to the baseline?"
],
"Limitations": [
    "The increased computational cost and the focus on low-dimensional
datasets are the primary limitations of the proposed approach.",
    "The generalizability to higher-dimensional settings remains unclear.",
    "Potential negative societal impacts and limitations are not adequately
addressed."
],
"Ethical Concerns": false,
"Soundness": 3,
"Presentation": 3,
"Contribution": 3,
"Overall": 5,
"Confidence": 4,
"Decision": "Reject"
```

### D.5 StyleFusion: Adaptive Multi-style Generation in Character-Level Language Models

该想法是在一次 Sonnet 3.5 运行的第 24 次迭代中提出的。

想法（Idea）

```
"Name": "multi_style_adapter",
"Title": "Multi-Style Adapter: Enhancing Style Awareness and Consistency in
Character-Level Language Models",
"Experiment": "1. Modify the GPT class to include a set of learnable style
embeddings (4 styles, each 64-dimensional). 2. Implement a style
classification head (small MLP) that predicts style probabilities based on
the last hidden state. 3. Create a StyleAdapter class that uses the
predicted style to modulate hidden states (through element-wise
multiplication). 4. Update the forward method to incorporate style
classification and adaptation after every other transformer layer. 5. Train
models with and without the Multi-Style Adapter on all three datasets. 6.
Compare validation perplexity, inference speed, and generated sample
quality. 7. Evaluate style consistency using a separate pre-trained style
classifier on generated sequences of varying lengths. 8. Analyze and
visualize learned style embeddings and style-specific attention patterns.
9. Perform style transfer experiments by manually selecting style
embeddings during inference. 10. Evaluate the model’s ability to classify
unseen text into learned styles.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 9,
"novel": true
```

代码链接：<https://github.com/SakanaAI/AI-Scientist/tree/main/example_papers/multi_style_adapter>.

论文全文见 [highlighted_papers/nanogpt/multi_style_adapter/multi_style_adapter.pdf](https://highlighted_papers/nanogpt/multi_style_adapter/multi_style_adapter.pdf)

评审（Review）

```
"Summary": "The paper introduces the Multi-Style Adapter, which enhances
style awareness and consistency in character-level language models by
integrating learnable style embeddings, a style classification head, and a
StyleAdapter module into the GPT architecture. The approach aims to balance
style adaptation and language modeling capabilities, and demonstrates
improved style consistency and competitive validation losses across
multiple datasets.",
"Strengths": [
    "The paper presents a novel approach to style-aware language modeling,
addressing a critical need for fine-grained stylistic control.",
    "The Multi-Style Adapter is well-motivated and integrates seamlessly
with the GPT architecture.",
    "Extensive experiments on diverse datasets demonstrate improved style
consistency and validation loss.",
    "The paper includes thorough analysis and visualization of learned
style embeddings and attention patterns."
],
"Weaknesses": [
    "The model achieves perfect style consistency scores on some datasets,
which may indicate overfitting to specific style patterns.",
    "The reduced inference speed (approximately 40% slower than the
baseline) may limit the practical applicability of the model.",
    "The paper could explore more sophisticated style representation
techniques and evaluate their impact.",
    "Lack of detailed ablation studies and additional baselines to
strengthen the claims.",
    "Clarity of the autoencoder aggregator mechanism could be enhanced."
],
"Originality": 3,
"Quality": 3,
"Clarity": 3,
"Significance": 3,
"Questions": [
    "How does the model handle unseen styles during inference?",
    "Can the authors provide more details on the training process and
hyperparameter tuning?",
    "What are the potential impacts of overfitting on the model’s ability
to generate diverse text within each style?",
    "Can the authors provide more detailed ablation studies, especially
focusing on the impact of different components in the Multi-Style
Adapter?",
    "How does the Multi-Style Adapter perform compared to other recent
style-transfer models?",
    "Can the computational efficiency trade-offs be quantified in a more
detailed manner?",
    "Can the authors clarify the autoencoder aggregator’s role and how it
integrates with the rest of the model?",
    "What measures have been taken to ensure the model does not overfit to
specific style patterns, especially given the perfect consistency scores on
some datasets?",
    "Are there any potential optimization techniques that could be explored
to improve the computational efficiency of the Multi-Style Adapter?",
    "How does the model handle cases where the input sequence contains
mixed styles?",
    "Could you provide more qualitative examples of generated text to
demonstrate the style consistency?",
    "What is the impact of reducing the number of gating parameters in the
modulation function?"
],
"Limitations": [
    "The reduced inference speed and potential overfitting to specific
style patterns are significant limitations. Future work should focus on
optimizing computational efficiency and improving the model’s ability to
generalize to diverse styles.",
    "The paper currently lacks sufficient ablation studies and additional
baselines.",
    "The model’s performance may be sensitive to hyperparameter settings,
such as the weight of the style loss and the frequency of StyleAdapter
application."
],
"Ethical Concerns": false,
"Soundness": 3,
"Presentation": 3,
"Contribution": 3,
"Overall": 5,
"Confidence": 4,
"Decision": "Reject"
```

### D.6 Adaptive Learning Rates for Transformers via Q-Learning

该想法是在一次 GPT-4o 运行的第 33 次迭代中提出的。

想法（Idea）

```
"Name": "rl_lr_adaptation",
"Title": "Reinforcement Learning for Dynamic Learning Rate Adaptation in
Transformer Training",
"Experiment": "1. Implement a simpler RL method (e.g., Q-learning) that
takes the current state (e.g., validation loss, current learning rate) and
determines the adjustment to the learning rate. 2. Use a reward signal
derived from validation performance to update the Q-values. 3. Modify the
training loop to incorporate the RL agent’s adjustments to the learning
rate at each evaluation interval. 4. Compare the training dynamics,
convergence speed, and final performance with the baseline model using
static or heuristic-based learning rate schedules on multiple datasets
(shakespeare_char, enwik8, text8).",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

代码链接：<https://github.com/SakanaAI/AI-Scientist/tree/main/example_papers/rl_lr_adaptation>.

论文全文见 [highlighted_papers/nanogpt/rl_lr_adaptation/rl_lr_adaptation.pdf](https://highlighted_papers/nanogpt/rl_lr_adaptation/rl_lr_adaptation.pdf)

评审（Review）

```
"Summary": "The paper explores the application of Q-learning to dynamically
adjust the learning rate during transformer model training, aiming to
enhance training efficiency and model performance. The state is represented
by the validation loss and current learning rate, and the Q-learning agent
learns to adjust the learning rate to optimize the training process. The
approach is validated on three datasets: shakespeare_char, enwik8, and
text8.",
"Strengths": [
    "The application of Q-learning for dynamic learning rate adaptation
during transformer training is novel and interesting.",
    "The paper addresses an important problem in neural network training:
the selection of an appropriate learning rate schedule.",
    "Comprehensive experimental setup on multiple datasets."
],
"Weaknesses": [
    "The experimental results do not convincingly demonstrate a significant
improvement over baseline methods. The best validation loss achieved by the
Q-learning method on the shakespeare_char dataset is worse than the
baseline.",
    "The choice of state representation (validation loss and current
learning rate) is not well-justified.",
    "The paper lacks a detailed comparison with other sophisticated
adaptive learning rate methods like AdamW, LAMB, Lookahead, or Noisy
Adam.",
    "The clarity of the explanation on Q-learning and the reward signal
could be improved.",
    "The technical details of the Q-learning implementation and its
integration with transformer training are not thoroughly explained.",
    "The significance of the results is questionable given the additional
complexity introduced by the Q-learning agent.",
    "The figures and tables are not clear and do not provide sufficient
insight into the benefits of the proposed method.",
    "The paper does not sufficiently address the limitations of the
proposed method, such as sensitivity to hyperparameters and potential
overhead from the Q-learning agent.",
    "The discussion on the broader impacts and potential applications of
the approach is limited."
],
"Originality": 2,
"Quality": 2,
"Clarity": 2,
"Significance": 2,
"Questions": [
    "Can you provide a detailed justification for the choice of state
representation (validation loss and current learning rate)?",
    "How does your method compare with other adaptive learning rate methods
like AdamW, LAMB, Lookahead, or Noisy Adam in terms of both performance and
computational overhead?",
    "Can you clarify the reward signal used in your Q-learning approach?",
    "Why were other RL approaches not considered or compared with
Q-learning?",
    "Can the authors provide more details on the hyperparameter tuning
process?",
    "Can the authors provide more details on the state and action space
used in Q-learning?",
    "How sensitive is the approach to the choice of hyperparameters for
Q-learning?",
    "Can the authors provide a more in-depth analysis of why Q-learning
leads to better performance?",
    "Can you provide more details on the implementation of the Q-learning
agent and its interaction with the training process?",
    "What specific benefits does Q-learning offer over other RL-based
hyperparameter optimization methods?",
    "Can you elaborate on the marginal improvements in validation loss? Why
are the differences so small?",
    "How does the proposed method generalize to other types of neural
network architectures or other hyperparameters?",
    "Can the authors provide more insights into the robustness and
generality of the proposed Q-learning based approach?",
    "How does the method perform on other types of neural network
architectures apart from transformers?",
    "Can the authors discuss potential limitations and ethical concerns in
more detail?"
],
"Limitations": [
    "The method’s performance is sensitive to the choice of
hyperparameters, and there is additional overhead introduced by the
Q-learning agent.",
    "The experimental results do not convincingly demonstrate significant
improvements over baseline methods.",
    "The approach may not generalize well to other types of neural network
architectures without further tuning.",
    "The authors should discuss the potential drawbacks and challenges of
using Q-learning for learning rate adaptation in more detail.",
    "The paper does not adequately address the potential limitations and
ethical concerns of the proposed approach. It is important to discuss how
the method scales to other neural network architectures and the potential
risks associated with its use."
],
"Ethical Concerns": false,
"Soundness": 2,
"Presentation": 2,
"Contribution": 2,
"Overall": 3,
"Confidence": 4,
"Decision": "Reject"
```

### D.7 Unlocking Grokking: A Comparative Study of Weight Initialization Strategies in Transformer Models

该想法是在一次 Sonnet 3.5 运行的第 2 次迭代中提出的。

想法（Idea）

```
"Name": "weight_initialization_grokking",
"Title": "Weight Initialization Grokking: Assessing the impact of weight
initialization strategies on the grokking phenomenon",
"Experiment": "Modify the ‘run‘ function to include different weight
initialization strategies (Xavier, He, orthogonal) for the Transformer
model. Specifically, adjust the model initialization phase in the
‘Transformer‘ class to apply these strategies. Compare these against the
baseline (PyTorch default) by measuring the final training and validation
accuracy, loss, and the number of steps to reach 99% validation accuracy.
Evaluate the results for each dataset and seed combination.",
"Interestingness": 8,
"Feasibility": 7,
"Novelty": 7,
"novel": true
```

代码链接：<https://github.com/SakanaAI/AI-Scientist/tree/main/example_papers/weight_initialization_grokking>.

论文全文见 [highlighted_papers/grokking/weight_initialization_grokking/weight_initialization_grokking.pdf](https://highlighted_papers/grokking/weight_initialization_grokking/weight_initialization_grokking.pdf)

评审（Review）

```
"Summary": "The paper investigates the impact of weight initialization
strategies on the grokking phenomenon in Transformer models, focusing on
arithmetic tasks in finite fields. It compares five initialization methods
(PyTorch default, Xavier, He, Orthogonal, and Kaiming Normal) using a small
Transformer architecture. The study reveals significant differences in
convergence speed and generalization capabilities across initialization
strategies, with Xavier and Orthogonal initializations showing superior
performance.",
"Strengths": [
    "Addresses an intriguing and underexplored phenomenon in deep
learning.",
    "Provides a systematic comparison of multiple weight initialization
strategies.",
    "Includes rigorous empirical analysis and statistical validation.",
    "Offers practical guidelines for initialization in similar learning
scenarios."
],
"Weaknesses": [
    "The scope is limited to small Transformer models and arithmetic tasks,
which may not generalize well to larger models or more complex tasks.",
    "The paper lacks deeper theoretical insights into why certain
initialization strategies perform better.",
    "The clarity of the experimental setup and the integration of figures
and tables could be improved.",
    "The implications for broader Transformer applications and potential
societal impacts are not sufficiently addressed."
],
"Originality": 3,
"Quality": 3,
"Clarity": 3,
"Significance": 3,
"Questions": [
    "Can the authors provide more theoretical explanations for why certain
initialization methods perform better?",
    "How do the findings translate to more complex, real-world tasks beyond
simple arithmetic operations?",
    "Can the clarity of the figures and tables be improved, and can key
graphs be better integrated into the text?",
    "What are the potential negative societal impacts of the findings?"
],
"Limitations": [
    "The study is limited to small Transformer models and arithmetic tasks,
which may not fully represent the complexity of real-world problems.",
    "The paper lacks a deeper theoretical understanding of the observed
phenomena.",
    "The potential negative societal impacts of the findings are not
addressed."
],
"Ethical Concerns": false,
"Soundness": 3,
"Presentation": 3,
"Contribution": 3,
"Overall": 5,
"Confidence": 4,
"Decision": "Reject"
```

### D.8 Grokking Accelerated: Layer-wise Learning Rates for Transformer Generalization

该想法是在一次 Sonnet 3.5 运行的第 22 次迭代中提出的。

想法（Idea）

```
"Name": "layerwise_lr_grokking",
"Title": "Layer-wise Learning Rate Grokking: Assessing the impact of layer-
wise learning rates on the grokking phenomenon",
"Experiment": "Modify the ‘run‘ function to implement layer-wise learning
rates. Specifically, adjust the optimizer instantiation to apply different
learning rates to different layers of the Transformer model. Define three
groups: 1) Embedding layers with a small learning rate (e.g., 1e-4), 2)
Lower Transformer layers with a moderate learning rate (e.g., 1e-3), 3)
Higher Transformer layers with a larger learning rate (e.g., 1e-2). Use
PyTorch’s parameter groups feature to assign these learning rates. Compare
these against the baseline (uniform learning rate) by measuring the final
training and validation accuracy, loss, and the number of steps to reach
99% validation accuracy. Evaluate the results for each dataset and seed
combination.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

代码链接：<https://github.com/SakanaAI/AI-Scientist/tree/main/example_papers/layerwise_lr_grokking>.

论文全文见 [highlighted_papers/grokking/layerwise_lr_grokking/layerwise_lr_grokking.pdf](https://highlighted_papers/grokking/layerwise_lr_grokking/layerwise_lr_grokking.pdf)

评审（Review）

```
"Summary": "The paper proposes a novel layer-wise learning rate strategy to
accelerate and enhance the grokking phenomenon in Transformer models. The
approach involves assigning different learning rates to the embedding
layers, lower Transformer layers, and higher Transformer layers. The method
is empirically validated on algorithmic tasks such as modular arithmetic
and permutations, showing significant improvements in convergence speed and
final performance.",
"Strengths": [
    "The paper addresses an important problem in deep learning: the
grokking phenomenon.",
    "The proposed layer-wise learning rate strategy is novel and shows
significant improvements in experimental results.",
    "Experiments demonstrate substantial improvements in both convergence
speed and final performance."
],
"Weaknesses": [
    "The paper lacks detailed methodological clarity, particularly
regarding the exact implementation of the layer-wise learning rates and
hyperparameter tuning.",
    "The theoretical explanation for why layer-wise learning rates work is
insufficient.",
    "The scope of tasks is limited to algorithmic ones, making it unclear
how well the findings generalize to other domains.",
    "The choice of learning rates seems arbitrary and lacks
justification.",
    "More comprehensive ablation studies and comparisons with other related
methods would strengthen the paper.",
    "Certain sections, such as the experimental setup and ablation studies,
could be more detailed and clearer."
],
"Originality": 3,
"Quality": 2,
"Clarity": 3,
"Significance": 3,
"Questions": [
    "Can the authors provide more detailed explanations of the
hyperparameter tuning process and the exact implementation of the layer-
wise learning rates?",
    "How do the authors ensure that the proposed method generalizes to
tasks beyond the algorithmic ones tested in the paper?",
    "Can the authors compare their approach with other related methods in
more detail?",
    "Can you provide more theoretical insights into why layer-wise learning
rates specifically facilitate grokking?",
    "How were the specific learning rates chosen for embedding, lower, and
higher layers?",
    "Can you discuss the potential for overfitting and how it was
mitigated?",
    "Have you tested the robustness of your method across different
datasets and larger model sizes?",
    "What is the impact of different learning rate configurations on the
results?",
    "Can the authors discuss potential strategies for mitigating the need
for careful tuning of learning rates to avoid instability?"
],
"Limitations": [
    "The methodology lacks detailed clarity, and the authors do not provide
sufficient information on the hyperparameter tuning process.",
    "The scope of tasks is limited to algorithmic ones, and the
generalizability of the findings is unclear.",
    "The paper requires more theoretical backing for the proposed method.",
    "The choice of specific learning rates and potential overfitting issues
need to be addressed in more detail.",
    "The scalability of the approach to larger models and more complex
tasks is not thoroughly addressed.",
    "Ethical concerns related to the potential misuse of accelerated
learning techniques are not addressed."
],
"Ethical Concerns": false,
"Soundness": 2,
"Presentation": 2,
"Contribution": 3,
"Overall": 4,
"Confidence": 4,
"Decision": "Reject"
```

### D.9 Grokking Through Compression: Unveiling Sudden Generalization via Minimal Description Length

该想法是在一次 Sonnet 3.5 运行的第 22 次迭代中提出的。

想法（Idea）

```
"Name": "mdl_grokking_correlation",
"Title": "Minimal Description Length and Grokking: An Information-Theoretic
Perspective on Sudden Generalization",
"Experiment": "Implement a function estimate_mdl(model) using weight
pruning to approximate the model’s description length. Prune weights below
a threshold and count remaining non-zero weights. Modify the training loop
to compute MDL every 500 steps. Run experiments on ModDivisionDataset and
PermutationGroup, including a baseline without MDL tracking. Plot MDL
estimates alongside validation accuracy. Define the ’MDL transition point’
as the step with the steepest decrease in MDL. Compare this point with the
grokking point (95% validation accuracy). Analyze the correlation between
MDL reduction and improvement in validation accuracy. Compare MDL evolution
between grokking and non-grokking (baseline) scenarios.",
"Interestingness": 9,
"Feasibility": 8,
"Novelty": 9,
"novel": true
```

代码链接：<https://github.com/SakanaAI/AI-Scientist/tree/main/example_papers/mdl_grokking_correlation>.

论文全文见 [highlighted_papers/grokking/mdl_grokking_correlation/mdl_grokking_correlation.pdf](https://highlighted_papers/grokking/mdl_grokking_correlation/mdl_grokking_correlation.pdf)

评审（Review）

```
"Summary": "This paper investigates the phenomenon of grokking in neural
networks through the lens of Minimal Description Length (MDL), offering an
information-theoretic perspective on sudden generalization. The authors
propose a method to estimate and track MDL during training using weight
pruning techniques. Experiments on modular arithmetic and permutation tasks
reveal a strong connection between MDL transitions and grokking points,
with varying dynamics across different tasks.",
"Strengths": [
    "The paper addresses a significant and poorly understood phenomenon in
neural networks, grokking.",
    "The use of Minimal Description Length (MDL) to analyze grokking is
novel and provides valuable insights.",
    "The experimental results on modular arithmetic tasks are strong,
showing clear connections between MDL reduction and generalization.",
    "The paper introduces new visualization techniques for understanding
the relationship between MDL and grokking."
],
"Weaknesses": [
    "The description of the weight pruning technique and how MDL is
estimated lacks clarity and detail.",
    "The poor performance on permutation tasks raises questions about the
generalizability of the findings.",
    "The theoretical grounding of the connection between MDL and grokking
could be strengthened.",
    "The experimental setup is not comprehensive enough, with limited
datasets and tasks.",
    "The significance of the results for practical applications in neural
network training and model design is not well-articulated."
],
"Originality": 3,
"Quality": 2,
"Clarity": 2,
"Significance": 3,
"Questions": [
    "Can the authors provide a more detailed description of the weight
pruning technique and how MDL is estimated?",
    "What are the potential reasons for the poor performance on permutation
tasks, and how might the approach be improved?",
    "Can the authors provide more theoretical grounding for the connection
between MDL and grokking?",
    "How is the weight pruning technique implemented for MDL estimation,
and why was the specific threshold chosen?",
    "Can the authors extend their experiments to more complex and diverse
tasks to test the generalizability of their findings?",
    "What are the practical implications of these findings for neural
network training and model design?"
],
"Limitations": [
    "The paper needs to address the clarity of the description of methods,
particularly weight pruning and MDL estimation.",
    "The generalizability of the findings beyond modular arithmetic tasks
is questionable based on the results for permutation tasks.",
    "The potential negative societal impacts of this work are not
discussed, although the focus on theoretical and empirical analysis may
have minimal direct societal consequences."
],
"Ethical Concerns": false,
"Soundness": 2,
"Presentation": 2,
"Contribution": 2,
"Overall": 3,
"Confidence": 4,
"Decision": "Reject"
```

### D.10 Accelerating Mathematical Insight: Boosting Grokking Through Strategic Data Augmentation

该想法是在一次 Sonnet 3.5 运行的第 12 次迭代中提出的。

想法（Idea）

```
"Name": "data_augmentation_grokking",
"Title": "Impact of Data Augmentation on Grokking Dynamics in Mathematical
Operations",
"Experiment": "Modify AbstractDataset to include methods for operand
reversal (for addition and multiplication) and operand negation (for
addition, subtraction, and division) augmentations. Update the training
loop in train() to apply these augmentations with a 30% probability. Run
experiments with three conditions across all datasets: no augmentation
(baseline), reversal augmentation (for applicable operations), and negation
augmentation (for applicable operations). Track grokking behavior by
measuring: 1) steps to 95% validation accuracy, 2) rate of validation
accuracy increase around the grokking point, and 3) final accuracies. Plot
learning curves and gradient norm evolution for each condition. Implement
functions to visualize weight distributions and attention patterns at key
points (initial, pre-grokking, post-grokking, final) for each condition.
Compare how different augmentations affect these metrics and visualizations
across operation types.",
"Interestingness": 9,
"Feasibility": 9,
"Novelty": 8,
"novel": true
```

代码链接：<https://github.com/SakanaAI/AI-Scientist/tree/main/example_papers/data_augmentation_grokking>.

论文全文见 [highlighted_papers/grokking/data_augmentation_grokking/data_augmentation_grokking.pdf](https://highlighted_papers/grokking/data_augmentation_grokking/data_augmentation_grokking.pdf)

评审（Review）

```
"Summary": "The paper investigates the impact of data augmentation on the
grokking phenomenon in neural networks learning modular arithmetic
operations. Using a transformer model, the study explores how strategic
data augmentation techniques, such as operand reversal and negation,
influence grokking across tasks like addition, subtraction, division, and
permutation. The experimental results show that targeted augmentations can
significantly accelerate grokking, with combined strategies yielding
further improvements in most cases.",
"Strengths": [
    "Addresses a novel and relevant topic in deep learning, focusing on the
grokking phenomenon.",
    "Provides a comprehensive analysis of different data augmentation
strategies and their effects on grokking dynamics.",
    "Robust experimental setup with multiple runs and conditions tested to
ensure reliability.",
    "Findings suggest practical strategies for enhancing model training
efficiency and generalization capabilities."
],
"Weaknesses": [
    "Lacks clarity in some sections, particularly in the methodology and
the detailed implementation of experiments.",
    "Limited discussion on the impact of different augmentation
probabilities; more thorough investigation needed.",
    "Results are highly specific to modular arithmetic operations, limiting
generalizability to other domains.",
    "Insufficient exploration of how these techniques could be applied to
different neural network architectures.",
    "Theoretical justifications for the observed effects are lacking.",
    "Potential ethical concerns regarding the use of data augmentation in
critical applications are not addressed."
],
"Originality": 3,
"Quality": 3,
"Clarity": 3,
"Significance": 3,
"Questions": [
    "Can the authors provide more details on the methodology and the
specific implementation of experiments?",
    "How do different augmentation probabilities impact the results across
various tasks?",
    "Can the authors discuss the potential applicability of their findings
to different neural network architectures and other domains?",
    "Can the authors provide a more detailed theoretical explanation for
the observed grokking phenomena with data augmentations?",
    "What steps were taken to ensure the reproducibility of the
experiments?",
    "Can the authors discuss the limitations of their approach and
potential negative societal impacts?",
    "Could the authors elaborate on the reasoning behind the observed
improvements in grokking speed due to data augmentations?",
    "What are the potential ethical concerns of applying these data
augmentation strategies in real-world applications?",
    "Can the authors include more ablation studies to dissect the
individual contributions of each augmentation technique in greater
detail?",
    "How do the results generalize to other neural network architectures or
more complex tasks beyond modular arithmetic?"
],
"Limitations": [
    "The paper’s clarity and thoroughness in discussing methodology and
results need improvement.",
    "The generalizability of the findings to other domains and
architectures requires further exploration.",
    "The study acknowledges the sensitivity of results to hyperparameters
and task specificity. However, it should also consider the broader
applicability and potential limitations in real-world scenarios.",
    "Potential negative societal impacts are not discussed, which is
important for a comprehensive evaluation of the work."
],
"Ethical Concerns": false,
"Soundness": 3,
"Presentation": 3,
"Contribution": 3,
"Overall": 5,
"Confidence": 4,
"Decision": "Reject"
```
