---
title: "DeepMind 的 2016 年度工作回顾"
title_en: "DeepMind's work in 2016: a round-up"
source: https://deepmind.google/blog/deepminds-work-in-2016-a-round-up/
site: deepmind
date: 2017-01-03
crawled: 2026-09-13
translated: 2026-09-13
---

# DeepMind 的 2016 年度工作回顾

> 原文：[DeepMind's work in 2016: a round-up](https://deepmind.google/blog/deepminds-work-in-2016-a-round-up/) · Google DeepMind

在这个充斥着极端复杂、不断涌现、难以驾驭的系统的世界里——从我们的气候到我们奋力征服的疾病——我们相信，智能程序将帮助发掘新的科学知识，供我们用于社会福祉。要做到这一点，我们认为我们需要通用的学习系统，它们能够从零开始形成自己对问题的理解，并据此识别出那些我们或许会错过的模式与突破。这正是 DeepMind 长期研究使命的焦点。

虽然距离任何可以称为你我所理解的"智能"的东西还很遥远，但 2016 年是意义重大的一年：我们在多个核心底层挑战上取得了令人振奋的进展，并首次瞥见了积极的现实世界影响的可能。

我们的程序 [AlphaGo](https://deepmind.com/research/case-studies/alphago-the-story-so-far)——我们有幸因它收获了[第二张《自然》封面](https://www.nature.com/articles/nature16961)——在古老的围棋上迎战并击败了世界冠军李世石（Lee Sedol），许多专家称这一壮举提前了十年到来。对我们乃至全世界围棋界而言，最令人兴奋的是 AlphaGo 展现出的赢棋创造力，在某些对局中，它找到了挑战数千年围棋智慧的着法。AlphaGo 能够就这门有史以来被思索得最多的游戏之一识别并分享新的洞见，这预示着 AI 有朝一日可能提供的价值，我们期待着 2017 年下更多的棋。

我们在生成式模型领域也取得了有意义的进展，构建出能够自行想象新的构造与场景的程序。继关于图像生成的 [PixelCNN](https://arxiv.org/abs/1606.05328) 论文之后，我们关于 [WaveNet](https://deepmind.com/blog/article/wavenet-generative-model-raw-audio) 的论文展示了生成式音频的实用性，通过富有想象力地直接创建原始波形（而不是把录制语音的样本拼接起来），实现了世界上最逼真的语音合成。我们计划与 Google 一起把这项技术投入生产，我们对能够改进数百万人使用的相关产品感到兴奋。

另一个重要的研究领域是记忆，具体来说，是如何把神经网络的决策才能与存储并推理复杂结构化数据的能力结合起来。我们在[可微神经计算机（Differentiable Neural Computers）](https://deepmind.com/blog/article/differentiable-neural-computers)上的工作——我们因此在十八个月内收获了[第三篇《自然》论文](https://www.nature.com/articles/nature20101)——展示了一类模型，它们既能像神经网络一样学习，又能像计算机一样记忆数据。这些模型已经能够学会回答关于从家谱到地铁图等各类数据结构的问题，让我们离在复杂数据集中利用 AI 进行科学发现的目标更近了一步。

在拓展这些系统能力边界的同时，我们也投入了大量时间改进它们的学习方式。一篇题为《[Reinforcement Learning with Unsupervised Auxiliary Tasks](https://deepmind.com/blog/article/reinforcement-learning-unsupervised-auxiliary-tasks)》的论文描述了把某些任务的学习速度提高一个数量级的方法。考虑到高质量训练环境对智能体的重要性，我们把旗舰研究环境 [DeepMind Lab](https://deepmind.com/blog/article/open-sourcing-deepmind-lab) 开源给了社区，并且正在[与 Blizzard 合作](https://deepmind.com/blog/announcements/deepmind-and-blizzard-release-starcraft-ii-ai-research-environment)为 StarCraft II 开发面向 AI 的训练环境。

当然，这只是冰山一角。你可以在[我们今年发表的众多论文](https://deepmind.com/research?filters=%7B%22collection%22:%5B%22Publications%22%5D%7D)中读到关于我们工作的更多信息，它们发表在从 Neuron 到 PNAS 的顶级期刊上，并在从 ICLR 到 NIPS 的重要机器学习会议上宣读。看到社区中的其他人已经在积极地实现这些论文中的工作并在此基础上继续构建——只要看看 2016 年下半年围棋计算机程序显著的复兴！——并见证 AI 与机器学习这些更广阔的领域蒸蒸日上，实在令人惊叹。

同样令人惊叹的，是看到这项工作开始显现出早期现实世界影响的迹象。我们与 Google 数据中心团队的合作利用类似 AlphaGo 的技术[发现了创造性的冷却管理新方法](https://deepmind.com/blog/article/deepmind-ai-reduces-google-data-centre-cooling-bill-40)，使这些建筑的能效提升了可观的 15%。如果这类技术能够被证明可以扩展到其他大规模工业系统，那么在全球环境与成本效益方面就存在真正显著的潜力。这只是我们与 [Google 各个团队](https://deepmind.com/about/deepmind-for-google)合作、把我们的前沿研究应用于全球范围使用的产品与基础设施的一个例子。我们还在英国——我们的家乡——与两个 NHS 医院集团积极开展[机器学习研究合作](https://deepmind.com/about/health)，探索我们的技术如何帮助更高效地诊断和治疗影响全球数百万人的疾病；同时正与另外两个医院集团合作开发[移动应用与基础基础设施](https://deepmind.com/about/health)，以支持临床一线改善照护。

当然，技术的积极社会影响不仅关乎我们试图解决的现实问题，也关乎算法与模型总体上被设计、训练和部署的方式。我们很荣幸[参与创立](https://deepmind.com/blog/announcements/announcing-partnership-ai-benefit-people-society)了 [AI 伙伴关系（Partnership on AI）](https://www.partnershiponai.org/)，它将把一流的研究实验室与非营利组织、公民社会团体和学者聚在一起，在算法透明度与安全等领域发展最佳实践。通过培育经验与洞见的多样性，我们希望帮助应对其中的一些挑战，并找到把社会目标置于全球 AI 社区核心的方法。

在使命的征程上，我们仍是一家年轻的公司。但如果在 2017 年我们能够在这三条战线上同时取得进一步进展——算法突破、社会影响与伦理最佳实践——那么我们将有能力继续为科学界以及更广阔的世界做出有意义的贡献。
