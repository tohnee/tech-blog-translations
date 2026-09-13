---
title: "规模化语言建模：Gopher、伦理考量与检索"
title_en: "Language modelling at scale: Gopher, ethical considerations, and retrieval"
source: https://deepmind.google/blog/language-modelling-at-scale-gopher-ethical-considerations-and-retrieval/
site: deepmind
date: 2021-12-08
crawled: 2026-09-13
translated: 2026-09-13
---

# 规模化语言建模：Gopher、伦理考量与检索

> 原文：[Language modelling at scale: Gopher, ethical considerations, and retrieval](https://deepmind.google/blog/language-modelling-at-scale-gopher-ethical-considerations-and-retrieval/) · Google DeepMind

语言，以及它在展示和促进理解——或者说智能——方面所扮演的角色，是人类之为人的根本部分。它让人们能够交流思想与概念、表达观点、创造记忆，并建立相互理解。这些是社会智能的基础。正因如此，DeepMind 的团队才会在人工智能体和人类两个层面研究语言处理与交流的各个方面。

作为更宏大的 AI 研究布局的一部分，我们相信，开发并研究更强大的语言模型——预测和生成文本的系统——对构建先进的 AI 系统有着巨大潜力，这些系统可以被安全高效地用于汇总信息、提供专家建议，以及通过自然语言遵循指令。开发有益的语言模型，需要研究它们潜在的影响，包括它们带来的风险。这需要来自不同背景的专家协作，审慎地预判并应对在现有数据集上训练算法可能带来的挑战。

今天，我们发布三篇关于语言模型的论文，体现了这一跨学科的方法。它们包括：对[一个名为 Gopher 的 2800 亿参数 transformer 语言模型](https://arxiv.org/abs/2112.11446)的详细研究、[一项关于大语言模型相关伦理与社会风险的研究](https://arxiv.org/abs/2112.04359)，以及[一篇探索具有更优训练效率的新架构的论文](https://arxiv.org/abs/2112.04426)。

## Gopher——一个 2800 亿参数的语言模型

在探索语言模型并开发新模型的征程中，我们训练了一系列不同规模的 transformer 语言模型，参数量从 4400 万到 2800 亿不等（其中最大的模型我们命名为 Gopher）。

我们的研究考察了这些不同规模模型的优势与劣势，重点指出模型规模增大仍能持续提升性能的领域——例如阅读理解、事实核查和毒性语言识别等方面。我们也揭示了模型规模并不能显著改善结果的地方——例如逻辑推理和常识任务。

![一张柱状图，比较 GPT-3、UnifiedQA、Gopher 和人类专家在人文、社会科学、医学、常识、科学/技术和数学等领域的准确率百分比，显示 Gopher 始终优于其他模型，但仍落后于人类专家水平。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6224d01f62cce9f8638e7d78_Fig201.svg)

Massive Multitask Language Understanding（MMLU）基准上的表现，按类别细分。Gopher 在多个类别上超越了此前的工作。

在我们的研究中，我们发现 Gopher 在许多关键任务上的能力超越了现有的语言模型。这包括 Massive Multitask Language Understanding（MMLU）基准，在该基准上，与此前的工作相比，Gopher 在迈向人类专家表现方面展现出了显著进步。

除了对 Gopher 进行定量评估之外，我们还通过与模型的直接交互来探索它。在我们的关键发现中，当 Gopher 被引导进行对话式交互（比如聊天）时，模型有时能展现出令人惊讶的连贯性。

![一张用户与 Gopher 对话的截图，双方讨论细胞生物学与原核生物，Gopher 成功地提供了关于大肠杆菌的准确事实、定义、示例以及一个 Wikipedia 链接。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6224d04aacea2444a5eeef02_Fig202.svg)

在这张图中，Gopher 能够讨论细胞生物学并提供正确的引用，尽管它没有经过任何专门的对话微调。然而，我们的研究也详细记录了在不同模型规模下持续存在的若干失效模式，其中包括重复的倾向、刻板偏见的映射，以及错误信息的自信传播。

![一张文字对话截图，展示了一种失效模式：Gopher 对关于 2021 年美国网球公开赛女单冠军、南美洲法语区以及欧拉恒等式的问题自信地给出错误答案，同时否认其回答存在任何不确定性。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6224d058786212486e2a4f1b_Fig203.svg)

这类分析很重要，因为理解并记录失效模式，能让我们洞察大语言模型可能如何造成下游危害，并告诉我们研究中的缓解工作应聚焦于何处来解决这些问题。

## 大语言模型的伦理与社会风险

在第二篇论文中，我们预判了语言模型可能带来的伦理与社会风险，并在该领域此前研究的基础上 [[Bommasani et al 2021](https://arxiv.org/abs/2108.07258)、[Bender et al 2021](https://dl.acm.org/doi/abs/10.1145/3442188.3445922)、[Patterson et al 2021](https://arxiv.org/abs/2104.10350)]，对这些风险和失效模式建立了全面的分类。这一系统性综述是理解这些风险并减轻潜在危害的关键一步。我们提出了一个与语言模型相关的风险分类体系，划分为六大主题领域，并深入阐述了 21 项风险。

以宽广的视野看待不同的风险领域至关重要：正如我们在论文中所展示的，过度狭隘地孤立关注某一单项风险，可能会让其他问题变得更糟。我们提出的这一分类体系，为专家和更广泛的公共讨论奠定了基础，有助于就语言模型的伦理与社会考量建立共同的总体认识、做出负责任的决策，并交流应对已识别风险的方法。

![一张信息图，展示大语言模型的六大主题风险领域，每个领域都配有一个蓝色图标、一个加粗标题和一段简要说明：**歧视、排斥与毒性**：来自歧视性和排斥性言论的危害。**信息危害**：因泄露或推断出真实敏感信息而造成的危害。**虚假信息危害**：因产生虚假或误导性信息而造成的危害。**恶意使用**：行为者蓄意利用模型造成危害。**人机交互危害**：用户过度信任模型或将模型拟人化对待而造成的危害。**自动化、获取与环境危害**：来自环境影响或下游经济影响的危害。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6224d06f425601d8baac2b6b_Fig204.svg)

我们的研究发现，有两个领域尤其需要进一步的工作。首先，当前的基准测试工具不足以评估某些重要风险，例如，当语言模型输出虚假信息而人们信以为真时。评估这类风险需要对语言模型的人机交互进行更细致的审视。在论文中，我们列出了若干同样需要新颖或更具跨学科性的分析工具的风险。其次，风险缓解方面还需要更多工作。例如，众所周知语言模型会复现有害的社会刻板印象，但对这一问题的研究仍处于早期阶段，正如 [DeepMind 最近的一篇论文](https://deepmind.com/research/publications/2021/Challenges-in-Detoxifying-Language-Models)所示。

## 借助互联网规模检索实现高效训练

我们的最后一篇论文以 Gopher 以及我们的伦理与社会风险分类体系为基础，提出了一种改进的语言模型架构，它降低了训练的能源成本，并使追溯模型输出到训练语料库中的来源变得更加容易。

Retrieval-Enhanced Transformer（RETRO）在预训练时配备了一种互联网规模的检索机制。受大脑学习时依赖专门记忆机制的启发，RETRO 能高效地查询文本段落以改进其预测。通过比较生成的文本与 RETRO 生成时所依赖的段落，我们可以解释模型为何做出某些预测，以及这些预测来自何处。我们还看到，该模型以少一个数量级的参数获得了与常规 Transformer 相当的性能，并在多个语言建模基准上取得了最先进的成绩。

![一张框图，展示 Retrieval-Enhanced Transformer（RETRO）架构：输入序列查询检索数据库以提取相邻段落，这些段落经编码后通过交叉注意力层被整合进来，最终产生输出序列。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6224d07ff43a03f5048d6d4e_Fig205.svg)

## 未来展望

这些论文为 DeepMind 未来的语言研究奠定了基础，尤其是在那些将影响这些模型如何被评估与部署的领域。应对这些领域，对于确保与 AI 智能体的安全交互至关重要——从人们告诉智能体他们想要什么，到智能体向人们解释自己的行为。更广泛的研究社区在利用交流保障安全方面的研究包括[自然语言解释](https://arxiv.org/abs/1812.01193)、[利用交流降低不确定性](https://en.wikipedia.org/wiki/Human_Compatible)，以及用语言把复杂决策拆解为若干部分，例如[放大（amplification）](https://arxiv.org/abs/1810.08575)、[辩论（debate）](https://arxiv.org/abs/1805.00899)和[递归奖励建模](https://arxiv.org/abs/1811.07871)——这些都是关键的探索领域。

在我们继续语言模型研究的过程中，DeepMind 将保持审慎与深思。这要求我们退后一步，评估我们所处的处境，梳理潜在风险，并研究缓解措施。我们将努力对我们的模型局限保持透明与开放，并致力于缓解已识别的风险。在每一步中，我们都汲取多学科团队的广博专业智慧，包括我们的语言、深度学习、伦理与安全团队。这一方法是打造服务社会的大语言模型的关键，也是推进我们「破解智能以促进科学、造福人类」这一使命的关键。
