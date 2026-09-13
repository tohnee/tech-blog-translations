---
title: "2017：DeepMind 年度回顾"
title_en: "2017: DeepMind's year in review"
source: https://deepmind.google/blog/2017-deepminds-year-in-review/
site: deepmind
date: 2017-12-21
crawled: 2026-09-13
translated: 2026-09-13
---

# 2017：DeepMind 年度回顾

> 原文：[2017: DeepMind's year in review](https://deepmind.google/blog/2017-deepminds-year-in-review/) · Google DeepMind

今年七月，世界排名第一的围棋棋手柯洁在取得 20 连胜之后接受了采访。彼时距离他在中国[乌镇围棋峰会](https://deepmind.com/blog/article/exploring-mysteries-alphago)上与 AlphaGo 对弈，已过去两个月。

「与 AlphaGo 的那场比赛之后，我从根本上重新审视了围棋，如今我可以看到，这种反思让我受益匪浅，」他[说](https://c.m.163.com/news/a/COTHSDS005119L7G.html?spss=newsapp&spsw=1)。「我希望所有棋手都能细细体会 AlphaGo 对围棋的理解和思维方式，这一切都意义深远。虽然我输了，但我发现围棋的可能性是无穷的，这项运动仍在不断进步。」

![围棋对局中，柯洁探身越过蓝色棋桌，把一枚棋子放在木质棋盘上。](https://lh3.googleusercontent.com/wq3Sd0MzSxgo6WyswQugyJQo5-PgbJ0wC1LJraLB5_mPOJVI_5AF6rw1O5oR19pdWPLs5mQFN_1LA37CFycvN9g8EsoguXNu4cRK08L0il8lUuVPWfY=w1440-h810-n-nu)

乌镇围棋峰会是一场为期五天的盛会，包含了多种对局形式——包括联棋、团体赛，以及与柯洁的一对一对局

柯洁是围棋大师，[他的这番话令我们深感荣幸](https://twitter.com/demishassabis/status/884915065715085312)。这些话也给了我们启发，因为它们预示着这样一种未来：社会可以把 AI 当作发现的工具，去发掘新知识、增进我们对世界的理解。尤其是在[机器辅助科学](https://www.ft.com/content/048f418c-2487-11e7-a34a-538b4cb30025)方面，我们希望 AI 系统能够帮助攻克从气候变化、药物发现，到寻找复杂新材料、缓解医疗体系压力等一系列挑战。

这种造福社会的潜力正是我们创立 DeepMind 的初衷，我们也为在一些基础科学挑战以及 AI 安全与伦理方面取得的持续进展感到兴奋。

DeepMind 的研究路径[受神经科学启发](https://deepmind.com/blog/article/ai-and-neuroscience-virtuous-circle)，这帮助我们在[想象力](https://deepmind.com/blog/article/agents-imagine-and-plan)、[推理](https://deepmind.com/blog/article/neural-approach-relational-reasoning)、[记忆](https://deepmind.com/blog/article/enabling-continual-learning-in-neural-networks)和[学习](https://deepmind.com/blog/article/imagine-creating-new-visual-concepts-recombining-familiar-ones)等关键领域取得进展。以想象力为例：这种人类特有的能力在我们的日常生活中扮演着关键角色，让我们能够对未来进行规划和推理，但对计算机而言却极具挑战性。我们今年继续在这一问题上努力攻关，推出了[想象力增强智能体（imagination-augmented agents）](https://deepmind.com/blog/article/agents-imagine-and-plan)，它们能够从环境中提取相关信息，以规划未来的行动。

这种受神经科学启发的路径也造就了我们工作[最受欢迎的演示之一](https://deepmind.com/blog/article/producing-flexible-behaviours-simulated-environments)：我们训练了一个神经网络，在模拟环境中控制多种简化的人体形态。这种精细的运动控制是「物理智能」的标志，也是我们研究计划中至关重要的一环。虽然产生的动作狂野、有时还颇为笨拙，但它们同样出奇地成功，并且[观赏性十足](https://www.youtube.com/watch?v=gn4nRCC9TwQ)。

> 我们深知技术并非价值中立。我们不能只在基础研究中取得进展，却不为自己的工作承担伦理与社会影响方面的责任。

另外，我们在生成模型领域也取得了进展。就在一年多以前，我们发布了 [WaveNet](https://deepmind.com/blog/article/wavenet-generative-model-raw-audio)，这是一种用于生成原始音频波形的深度神经网络，能够生成比既有技术更好、听感更逼真的语音。当时，该模型还只是研究原型，计算量太大，无法在消费级产品中使用。在过去 12 个月里，我们的团队成功打造了一个快 1000 倍的新模型。十月，我们公布了这一新的 [Parallel WaveNet](https://deepmind.com/blog/article/high-fidelity-speech-synthesis-wavenet) 已投入实际应用，为[Google Assistant](https://www.blog.google/products/assistant/google-assistant-powering-our-new-family-hardware/) 生成美式英语和日语语音。

这是我们在让 AI 系统更易构建、训练和优化方面所投入努力的一个例子。我们今年研究的其他技术，例如[分布式强化学习（distributional reinforcement learning）](https://deepmind.com/blog/article/going-beyond-average-reinforcement-learning)、[神经网络的基于种群的训练](https://deepmind.com/blog/article/population-based-training-neural-networks)和[新的神经架构搜索方法](https://deepmind.com/research/publications/hierarchical-representations-efficient-architecture-search/)，有望让系统更容易构建、更准确、优化更快。我们还投入了大量时间打造全新且富有挑战性的环境来测试我们的系统，其中包括与暴雪娱乐合作[将《星际争霸 II》开放给研究界](https://deepmind.com/blog/announcements/deepmind-and-blizzard-open-starcraft-ii-ai-research-environment)。

但我们深知技术并非价值中立。我们不能只在基础研究中取得进展，却不为自己的工作承担伦理与社会影响方面的责任。这推动着我们在可解释性等关键领域开展研究——我们一直在探索新颖的方法来[理解](https://deepmind.com/blog/article/cognitive-psychology)和[解释](https://deepmind.com/research/publications/learning-explanatory-rules-noisy-data/)我们的系统如何运作。这也是为什么我们拥有一支成熟的技术安全团队，持续开发[切实可行的方法](https://deepmind.com/blog/article/specifying-ai-safety-problems)，确保我们能够[信赖未来的系统](https://deepmind.com/blog/article/learning-through-human-feedback)，并让它们始终处于有意义的人类控制之下。

![一名临床医生手持显示 Streams 应用患者警报界面的智能手机，背景中一位患者模糊地躺在医院病床上。](https://lh3.googleusercontent.com/COWUwcL_jAPs4H1fso5xqS6KwKy-tKLx0drzwblWhVc5Gksz4muYYpm7zlQq0Pg5ymC9h4JhqN1CaKPvZueWboA_FHdX6XwEOY65Ing8OnFcKQoeHF0=w1440-h810-n-nu)

我们目前已与四个英国国家医疗服务体系（NHS）信托机构就 Streams 展开合作

十月，我们迈出了另一步，启动了 [DeepMind Ethics & Society](https://deepmind.com/blog/announcements/why-we-launched-deepmind-ethics-society)——一个研究部门，将帮助我们探索和理解 AI 在现实世界中的影响，以实现社会公益。我们的研究将由各领域赫赫有名的专家组成的[Fellows（研究员）](https://deepmind.com/about/ethics-and-society#fellows)提供指导，例如哲学家 Nick Bostrom、气候变化专家 Christiana Figueres、顶尖研究者 James Manyika，以及经济学家 Diane Coyle 和 Jeffrey Sachs。

AI 必须由社会的优先事项和关切来塑造，这也是为什么我们与[合作组织](https://deepmind.com/about/ethics-and-society#partners)一起举办活动，旨在敞开关于 AI 应当如何设计与部署的公共讨论。例如，领导算法正义联盟（Algorithmic Justice League）的 [Joy Buolamwini](https://www.poetofcode.com/)，以及来自 Article 36、人权观察（Human Rights Watch）和英国武装部队的专家，与我们一起在 Wired Live 上进行了一场讨论，话题涉及算法偏见和限制致命性自主武器的使用。正如我们今年[一再表示](https://www.youtube.com/watch?v=xqYqWFksBeQ)的，这些问题太重要、影响太广泛，不容忽视。

这也是为什么我们还需要在 AI 公司内部和外部开辟新的讨论空间，来探讨如何预判和引导这项技术的影响。一个例子是[人工智能伙伴关系（Partnership on AI）](https://www.partnershiponai.org/)，我们今年担任了它的联席主席之一，它的使命是把行业竞争者、学术界和公民社会聚在一起讨论关键伦理议题。过去一年，PAI 迎来了 43 个新的非营利和营利成员，以及一位新的执行总监 Terah Lyons。在未来几个月里，我们期待与这一组织共同研究一系列课题，包括算法中的偏见与歧视、机器学习对自动化和劳动力的影响等等。

> 我们为 2017 年取得的所有进展感到自豪，但也深知前面还有很长的路要走。

我们同样相信用技术创造切实社会效益的重要性，并持续看到健康与能源领域现实影响的巨大潜力。今年，我们与两家 NHS 医院信托机构达成了新的合作，部署我们的 Streams 应用，它用数字技术[为英国国家医疗服务体系（NHS）的临床医生提供支持](https://www.youtube.com/watch?v=2HIcloy_OYk)。我们还是一家顶尖研究机构联合体的成员，该联合体发起了一项开创性研究，以确定前沿机器学习技术能否帮助改进乳腺癌的检测。

与此同时，我们也在健康业务工作的[监督](https://deepmind.google/blog/independent-reviewers-release-first-annual-report-on-deepmind-health/)方面下了很大功夫。我们[撰文总结了教训](https://deepmind.com/blog/ico-royal-free/)——来自信息专员办公室（Information Commissioner's Office）对我们与皇家自由医院（Royal Free）最初合作的调查结论；DeepMind Health 的独立评审员也发布了关于我们工作的第一份公开[年度报告](https://deepmind.com/blog/announcements/independent-reviewers-annual-report-2017)。他们的审视让我们的工作变得更好。我们已在与患者和公众的[沟通接触](https://www.youtube.com/watch?v=Kjtec1017_A)方面作出重大改进，包括与患者和照护者举行的[工作坊](https://deepmind.com/applied/deepmind-health/patients/)；我们还在探索把信任构建到系统中的技术手段，例如[可验证数据审计（verifiable data audit）](https://deepmind.com/blog/article/trust-confidence-verifiable-data-audit)，我们计划将其作为开源工具发布。

我们为 2017 年取得的所有进展感到自豪，但也深知前面还有很长的路要走。

在乌镇与柯洁对弈、并让 AlphaGo 退役退出竞技对局的五个月后，我们发表了第四篇 [Nature 论文](https://www.nature.com/articles/nature24270.epdf?author_access_token=VJXbVjaSHxFoctQQ4p2k4tRgN0jAjWel9jnR3ZoTv0PVW4gB86EEpGqTRDtpIz-2rmo8-KG06gqVobU5NSCFeHILHcVFUeMsbvwS-lxjqQGg98faovwjxeTUgZAUMnRQ)，介绍这个系统的新版本——[AlphaGo Zero](https://deepmind.google/blog/alphago-zero-starting-from-scratch/)，它不使用任何人类知识。在数百万盘对局的过程中，该系统从零开始逐步学会围棋，仅在几天之内就积累了数千年的棋艺知识。在这个过程中，它还发现了非同寻常的策略，并[揭示了关于这项古老运动的新知识](https://alphagoteach.deepmind.com/)。

我们相信，AI 作为一种科学工具和人类智慧的放大器，将能够在其他复杂问题上做到同样的事。AlphaGo 团队已经在攻克下一批重大挑战，我们希望他们帮助创造的那些算法灵光乍现的时刻，仅仅是个开始。
