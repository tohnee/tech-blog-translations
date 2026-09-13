---
title: "Mahima Pushkarna 让数据更易于理解"
title_en: "Mahima Pushkarna is making data easier to understand"
source: https://blog.google/innovation-and-ai/technology/research/mahima-pushkarna-interview/
site: google-blog
date: 2022-06-30
crawled: 2026-09-13
translated: 2026-09-13
---

# Mahima Pushkarna 让数据更易于理解

> 原文：[Mahima Pushkarna is making data easier to understand](https://blog.google/innovation-and-ai/technology/research/mahima-pushkarna-interview/) · Google

五年前，信息设计师 Mahima Pushkarna 加入 Google，致力于让数据更易于理解。作为 [People + AI Research](http://pair.withgoogle.com/)（PAIR）团队的高级交互设计师，她设计了 [Data Cards](https://pair-code.github.io/datacardsplaybook/)，帮助每个人更好地理解自己所用数据的背景。Data Cards Playbook 通过提供反馈机会、相关解释和申诉渠道，将 [Google 的 AI 原则](https://ai.google/principles/)付诸实践。

最近，Mahima 关于 Data Cards 的[论文](https://arxiv.org/abs/2204.01075)（与 Google 员工 Andrew Zaldivar 和 Oddur Kjartansson 合著）被 ACM 公平性、问责与透明度会议（[ACM FAccT](https://facctconference.org/)）接收。让我们与她聊聊，进一步了解是什么把她带到了 Google。

**你的背景是如何引导你走上如今这份工作的？**

我一直着迷于为各种事情想出解决方案。我发现自己觉得有意义的，是那些永远不会被真正解决、或者永远没有一个正确答案的问题。（就是那些让我们抓狂的问题！）这些一直是我被吸引的问题。

在职业生涯早期，我意识到数据可视化的力量，但电子表格令人望而生畏。我想知道设计如何能让复杂信息的传达变得更容易。于是我在波士顿的研究生院学习信息设计与数据可视化。我专注于研究人们如何体验数据，以及我们彼此之间的关系和所处情境是如何被媒介化的。

我以全职身份加入 Google Brain，成为第一位全职视觉设计师，尽管我并没有人工智能或机器学习背景——这就像一头扎进了泳池的深水区。这为我打开了探索人机交互的空间，让 AI 对更广泛的开发者群体更易使用。在 PAIR，我的工作重点是让信息体验对开发者、研究人员和其他构建 AI 技术的人来说更有意义。

**作为技术 AI 研究团队中一位背景独特的设计师，是什么感受？**

当你是一名工程师、沉浸在构建技术中的时候，很容易假设每个人都和你有着相似的经历——尤其是当你身边都是与你拥有相同专业能力的同行时。而实际的用户体验是非常个人化的，会在不同用户和不同情境之间发生巨大差异。设计师带来的正是这种独特的清晰视角。

我从一开始就能用简单的、以人为中心的问题引发工程和研究同事的思考。人们是如何使用某个 AI 工具的？他们从中学会了什么？还有谁可能参与这场对话？他们真的具备我们所假设的那种熟练程度吗？

**你是如何开始设计 Data Cards 的？**

这个项目始于我当时在开发另一个可视化工具包 [Facets](http://facets.dev/)，用于传达数据集中的偏斜与失衡，帮助机器学习从业者做出明智决策。当时，透明度还是一个不断移动的靶标。Andrew、Tulsee Doshi 和我开始主动思考数据中的公平性问题，并看到一个巨大的空白：贯穿数据集生命周期各个环节的人类决策缺乏文档记录。

这些"看不见的"信息塑造着我们使用数据的方式，以及基于数据训练的模型的结果。例如，用仅按两三个年龄段划分的数据集训练的模型，其结果会与用十个年龄段划分的数据集训练的模型大不相同。Data Cards 的目标是让关于数据集的可见与不可见信息都变得可获得、易于理解，让来自各种背景的人都能够有依据地做出决策。

正如我们在 [FAccT 论文](https://arxiv.org/abs/2204.01075)中所阐述的，我和 Andrew、Oddur 得出了两个洞见。第一个是，识别我们对数据不了解的东西，与阐明我们所知道的东西同样重要。通过捕捉这些细微之处，甚至可以在收集数据之前就缩小这些知识差距。第二个令我们惊讶的是，参与数据集生命周期的人数之多，以及知识何其脆弱。无论是团队之间还是团队内部，无论跨越文档、邮件、人员还是时间，背景信息都很容易在传递中丢失。

Data Cards 站在巨人的肩膀上，比如 [Data Sheets](https://arxiv.org/abs/1803.09010)（Gebru 等）和 [Model Cards](https://arxiv.org/abs/1810.03993)（Mitchell 等）。我们非常幸运地得到了这些开创性论文的许多原作者的支持，它们为我们铺就了通往 FAccT 的道路。

**你希望这篇论文在科技行业中被如何使用？**

想象这样一个世界：查找关于数据集创建者动机或模型性能的可验证信息，就像了解一位名人的道德信仰或一部电影的评分一样容易。我们对 Data Cards 的愿景是，它们成为一种文化支柱——隐形存在，但一旦缺失，机器学习从业者就会感到缺憾。

在这篇论文中，我们介绍了其他团队可以在自己的工作中使用的框架。除此之外，我们还开源了 [Data Cards Playbook](https://pair-code.github.io/datacardsplaybook/)，我们正在尽一切可能降低使用的门槛。
