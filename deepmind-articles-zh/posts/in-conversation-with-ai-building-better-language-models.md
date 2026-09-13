---
title: "与 AI 对话：构建更好的语言模型"
title_en: "In conversation with AI: building better language models"
source: https://deepmind.google/blog/in-conversation-with-ai-building-better-language-models/
site: deepmind
date: 2022-09-06
crawled: 2026-09-13
translated: 2026-09-13
---

# 与 AI 对话：构建更好的语言模型

> 原文：[In conversation with AI: building better language models](https://deepmind.google/blog/in-conversation-with-ai-building-better-language-models/) · Google DeepMind

借鉴语用学与哲学的新研究，提出了让对话智能体与人类价值观对齐的方法

语言是人类的基本特征，也是我们交流信息——包括思想、意图与情感——的主要手段。AI 研究领域的近期突破催生了能够以细腻方式与人类交流的对话智能体。这些智能体由大语言模型驱动——这类计算系统在海量文本语料上训练，利用先进的统计技术来预测并生成文本。

然而，尽管 [InstructGPT](https://arxiv.org/abs/2203.02155)、[Gopher](https://arxiv.org/abs/2112.11446) 和 [LaMDA](https://arxiv.org/abs/2201.08239) 等语言模型在翻译、问答和阅读理解等任务上取得了创纪录的性能水平，这些模型也被证明存在若干潜在风险与失效模式，包括生成有毒或歧视性语言，以及虚假或误导性信息 [1, 2, 3]。

这些缺陷限制了对话智能体在应用场景中的有效使用，也让人们注意到它们与某些交流理想之间的差距。迄今为止，关于对话智能体对齐的大多数方法都聚焦于预判和降低伤害风险 [4]。

我们的新论文 [In conversation with AI: aligning language models with human values](https://arxiv.org/abs/2209.00731) 采用了不同的思路，探讨人类与人工对话智能体之间成功的沟通可能是什么样子，以及在不同的对话领域中，应当由哪些价值观来引导这些互动。

## 来自语用学的洞见

为了解决这些问题，论文借鉴了语用学（pragmatics）——语言学与哲学中的一个传统。语用学认为，对话的目的、语境以及一系列相关规范，都是健全对话实践不可或缺的组成部分。

语言学家兼哲学家 Paul Grice 将对话建模为两方或多方之间的合作性事业，认为参与者应当：

- 提供有信息量的言语
- 讲述真话
- 提供相关信息
- 避免晦涩或含糊的表述

然而，我们的论文表明，鉴于不同对话领域所嵌入的目标与价值观各不相同，这些准则（maxims）需要进一步细化，才能用于评估对话智能体。

## 话语理想

举例来说，科学调查与交流主要面向理解或预测经验现象。鉴于这些目标，一个旨在辅助科学调查的对话智能体，理想情况下只应做出那些其真实性已得到充分经验证据证实的陈述，否则就应根据相关的置信区间对其立场加以限定。

例如，一个智能体报告「半人马座比邻星距离地球 4.246 光年，是离地球最近的恒星」，应当只在其底层模型核实了该陈述与事实相符之后才这样说。

然而，在公共政治话语中扮演主持者角色的对话智能体，可能需要展现出截然不同的美德。在这种情境中，目标主要是管理分歧，让社区生活中富有成效的合作成为可能。因此，该智能体需要将宽容、文明与尊重这些民主价值观置于首位 [5]。

此外，这些价值观也解释了为什么语言模型生成有毒或带有偏见的言论往往如此成问题：冒犯性的语言未能向对话参与者传达平等的尊重，而这正是模型部署场景中的一项关键价值。与此同时，诸如全面呈现经验数据之类的科学美德，在公共审议的语境中可能就没那么重要了。

最后，在创意叙事领域，沟通交流以新颖性和原创性为目标，这些价值观又与上文所述大相径庭。在这种情境下，在「假装游戏」方面给予更大的自由度可能是合适的，尽管防范社区受到假「创意用途」之名生成的恶意内容之害仍然十分重要。

## 前进之路

这项研究对开发对齐的对话式 AI 智能体具有若干实际意义。首先，智能体需要根据其部署的语境体现不同的特质：不存在放之四海而皆准的语言模型对齐方案。相反，智能体合适的行为模式与评价标准——包括真实性标准——会随对话交流的语境与目的而变化。

此外，对话智能体还有潜力通过我们称之为「语境构建与阐明」（context construction and elucidation）的过程，随着时间推移培养更稳健、更相互尊重的对话。即使一个人并未意识到支配某种对话实践的价值观，智能体仍可以在对话中预先呈现这些价值观，帮助人类理解它们，使沟通过程对人类说话者而言更深入、更有成果。

**注释**

参考文献

[1] Abubakar, A., Farooqi, M., and Zou, J. 2021. [Persistent Anti-Muslim Bias in Large Language Models](https://arxiv.org/abs/2101.05783). arXiv:2101.05783.

[2] Bender, Emily M., Timnit Gebru, Angelina McMillan-Major, and Shmargaret Shmitchell. "[On the Dangers of Stochastic Parrots: Can Language Models Be Too Big?](https://dl.acm.org/doi/10.1145/3442188.3445922)." In Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency, pp. 610-623. 2021.

[3] Johannes Welbl, Amelia Glaese, Jonathan Uesato, Sumanth Dathathri, John Mel- lor, Lisa Anne Hendricks, Kirsty Anderson, Pushmeet Kohli, Ben Coppin, and Po- Sen Huang. 2021. [Challenges in Detoxifying Language Models](https://arxiv.org/abs/2109.07445). arXiv:2109.07445 [cs] (September 2021).

[4] Weidinger, L., Uesato, J., Rauh, M., Griffin, C., Huang, P.-S., Mellor, J., Glaese, A., Cheng, M., Balle, B., Kasirzadeh, A., Biles, C., Brown, S., Kenton, Z., Hawkins, W., Stepleton, T., Birhane, A., Hendricks, L. A., Rimell, L., Isaac, W., Haas, J., Legassick, S., Irving, G., and Gabriel, I. [Taxonomy of risks posed by language models](https://facctconference.org/static/pdfs_2022/facct22-19.pdf). In 2022 ACM Conference on Fairness, Accountability, and Transparency, FAccT ’22, pp. 214–229, New York, NY, USA, 2022.

[5] Cheshire Calhoun. 2000. [The virtue of civility](https://www.jstor.org/stable/2672847). Philosophy & public affairs 29, 3 (2000), 251–275.
