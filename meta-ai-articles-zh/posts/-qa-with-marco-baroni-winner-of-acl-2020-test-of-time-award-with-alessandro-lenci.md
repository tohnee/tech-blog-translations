---
title: "对话 Marco Baroni：与 Alessandro Lenci 共获 ACL 2020 时间检验奖"
title_en: "Q&A with Marco Baroni, winner of ACL 2020 Test of Time award with Alessandro Lenci"
date: 2020-07-22
source: https://ai.meta.com/blog/-qa-with-marco-baroni-winner-of-acl-2020-test-of-time-award-with-alessandro-lenci/
crawled: 2026-09-22
translated: 2026-09-22
---

# 对话 Marco Baroni：与 Alessandro Lenci 共获 ACL 2020 时间检验奖

> 原文：[Q&A with Marco Baroni, winner of ACL 2020 Test of Time award with Alessandro Lenci](https://ai.meta.com/blog/-qa-with-marco-baroni-winner-of-acl-2020-test-of-time-award-with-alessandro-lenci/) · Meta AI（Wayback 存档）

我们很高兴地祝贺 Facebook AI 的 Marco Baroni 与比萨大学的 Alessandro Lenci 凭论文《Distributional Memory: A General Framework for Corpus-Based Semantics》获得 ACL 2020 时间检验奖，该论文 2010 年发表于《Computational Linguistics》期刊。Baroni 于 2016 年加入 Facebook AI，吸引他的是与 Tomas Mikolov、Armand Joulin、Jason Wetson、Antoine Bordes 等研究科学家共事和交流想法的机会——这些人都为语言的计算建模带来了新鲜视角。Baroni 在多模态与组合式分布式语义领域的工作获得了广泛认可，包括一项 ERC 启动资助和 ICAI-JAIR 最佳论文奖。在 Facebook AI，他专注于训练机器通过自然语言与人类以及与其他机器交互。目前，他正在深入研究人工神经网络彼此通信时演化出的语言的本质。Baroni 抽空分享了他对这篇 2010 年论文影响的看法。

**问：这项研究是关于什么的？**

答：与以往一次只针对一个任务调优的模型不同，我们的研究提出了一种替代方法：从文本语料库中一次性提取计算词表示，然后用这些表示来解决一系列任务，例如自动发现同义词或预测概念的典型属性。关于研究本身，你可以在此处阅读更多内容。

**问：论文最初发表时情况如何？当时社区对它的反响怎样？**

答：论文反响良好，尤其是在一个对连接计算语言学、理论语言学和认知科学感兴趣的小型研究者群体中。它（相对意义上）的成功部分归功于我们在论文发布时公开了所创建的表示。虽然现在看来这是理所当然的一步，但在当时并不常见。

**问：这项工作被如何延续？它对我们今天看到的产品有影响吗？**

答：这篇论文与当今至少两个非常显赫的话题产生共鸣。其一是通过所谓预训练阶段开发通用词句表示的想法。这是许多自然语言处理应用的核心，如机器翻译和自动问答。有趣的是，当时机器学习（ML）领域的研究者几乎同时独立发现了通用预训练。其二是创建一组标准测试来探查计算模型的语言能力。如今有一个非常活跃的社区专门从事这一方向，常与 BlackBox NLP 系列研讨会联系在一起。现在已有广泛共识：仅测量 NLP 系统在实际任务上的性能，不足以理解模型真正的语言能力。

**问：一路上有惊喜吗？**

答：2010 年底，在 EMNLP（自然语言处理实证方法会议）上，我第一次听到人们谈论「深度学习」和「表示学习」。我花了一段时间才理解这些术语的含义，但最终我发现许多 ML 研究者正在研究与我所属的小众计算语言学群体所开发的相似的想法。虽然我们来自不同的学科传统、目标不同，却得出了相同的结论。例如这样的想法：可以用连续而非离散的表示捕捉多种形式的知识，而且这些表示应当从数据中自动提取而非人工编码。我是理论语言学出身，非常惊讶地发现我正在做的事情与 ML 专家高度相关，反过来，我也能理解他们在做什么以及为什么。

**问：你目前的研究重点是什么？**

答：人类之所以能成就非凡之事，得益于我们通过语言彼此交流的能力。我们能否同样赋予当今的 AI 系统彼此「交谈」的能力？如果我们让它们演化出一种共享语言来共同解决问题，涌现出的语言会有什么样的特性？它像人类语言一样灵活吗？如果不是，我们如何让它变得灵活？这又能让我们对人类和机器各自有什么认识？
