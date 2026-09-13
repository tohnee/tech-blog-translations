---
title: "从博弈到生物学及更远：AlphaGo 十年影响力回顾"
title_en: "From games to biology and beyond: 10 years of AlphaGo's impact"
source: https://deepmind.google/blog/10-years-of-alphago/
site: deepmind
date: 2026-03-10
crawled: 2026-09-13
translated: 2026-09-13
---

# 从博弈到生物学及更远：AlphaGo 十年影响力回顾

> 原文：[From games to biology and beyond: 10 years of AlphaGo's impact](https://deepmind.google/blog/10-years-of-alphago/) · Google DeepMind

十年前，我们的 AI 系统 AlphaGo 成为第一个在围棋这一复杂博弈中击败世界冠军的程序——比许多专家认为可能的时点提前了十年，抵达了这一领域的里程碑。

这一成就宣告了如今被公认为人工智能（AI）现代纪元的开端。凭借一步充满创造力的落子——著名的「第 37 手（Move 37）」，[AlphaGo](https://deepmind.google/research/alphago/) 展示了 AI 的潜力，并传递出一个信号：我们如今已经掌握了开始攻克现实世界科学问题的技术。

今天，这一突破仍在滋养我们构建通往通用人工智能（AGI）系统的工作。我们相信，AGI 将是有史以来最深刻的技术，并有望成为推动科学、医学和生产力进步的终极工具。

## 一点创造的火花

2016 年，超过两亿人观看了 AlphaGo 在首尔对弈世界冠军棋手 Lee Sae Dol。这场比赛因第二局的「第 37 手」而被载入史册——那步棋如此超乎常规，职业解说最初以为是一步失误。但事实证明它是决定性的。约一百手之后，那颗棋子恰好落在让 AlphaGo 赢下这一局的位置上。这是惊人前瞻力的展现，也证明了这套 AI 系统有能力超越对人类专家的模仿，找到全新的策略。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

[在 YouTube 上观看 AlphaGo 纪录片](https://www.youtube.com/watch?v=WXuK6gekU1Y)

围棋因其极高的复杂度，长期以来一直是 AI 研究的试金石。棋盘上共有 10170 种可能的局面——远超可观测宇宙中原子的数量。

为了让这个博弈变得可解，AlphaGo 将深度神经网络与先进搜索及强化学习相结合——这是 DeepMind [开创](https://www.nature.com/articles/nature16961)的 AI 方法。

AlphaGo 首先从人类专家的对局中学习，随后通过与自己进行数十万盘对弈来学习一个合理的围棋落子模型，最强的获胜策略被不断强化，系统也随之进步。之后，系统只考虑最有希望带来收益的路径，并从这个更小的走法子集中，找出最有可能导向胜利的那一步。

在 AlphaGo 之后，我们构建了 [AlphaGo Zero](https://deepmind.google/blog/alphago-zero-starting-from-scratch/)，它完全从随机落子开始学习，并成为了可以说是史上最强的棋手。接着我们用 [AlphaZero](https://deepmind.google/blog/alphazero-shedding-new-light-on-chess-shogi-and-go/) 进一步泛化了该系统，它从零开始自学，掌握了任何双人完全信息博弈，包括围棋、国际象棋和将棋。除了游戏规则之外不带任何先验知识，AlphaZero 就能在几个小时内学会精通国际象棋，不仅击败顶尖人类棋手，还击败了当时最强的专用国际象棋程序，如 Stockfish。尽管国际象棋早已被这些程序反复研究，AlphaZero 依然像在围棋中一样，想出了有趣的[新策略](https://www.newinchess.com/game-changer)。

这进一步印证了我在首尔赢得比赛那一刻就知道的事情——这项技术已经成熟，可以应用于我们真正的目标：加速科学突破。

> 我相信 AlphaGo 带给世人最大的启示，是对 AI 时代一次确定无疑的预演——它证明 AI 并非遥远而模糊的未来，而是已经叩响门扉的现实。它像一份「来自未来的路线图」，向人类清晰地传递了世界即将如何改变的信号。

围棋大师 Lee Sae Dol

蔚山科学技术院（UNIST）兼职教授

## 催化科学突破

通过证明 AI 能够在围棋棋盘的巨大搜索空间中自如穿行，AlphaGo 展示了 AI 帮助我们更好地理解物理世界巨大复杂性的潜力。我们从尝试解决蛋白质折叠问题开始——这是一个有着 50 年历史的重大挑战，即预测蛋白质的三维结构，而这一信息对理解疾病和开发新药至关重要。

2020 年，我们用 [AlphaFold 2](https://deepmind.google/blog/alphafold-five-years-of-impact/) 系统最终攻克了这一悬而未决的科学难题。随后，我们折叠了科学界已知的全部 2 亿种蛋白质的结构，并将它们放入开源数据库，免费提供给科学家。今天，全球有超过 300 万研究人员使用 [AlphaFold 数据库](https://alphafold.ebi.ac.uk/)来加速他们的重要工作，研究对象涵盖从疟疾疫苗到「吃塑料」的酶。2024 年，John Jumper 和我有幸代表整个 AlphaFold 团队，因领导这一项目被授予诺贝尔化学奖——那是我一生的荣耀。

自 AlphaGo 获胜以来，我们已将其开创性的方法应用于科学和数学的许多其他领域，包括：

**数学推理：** AlphaGo 架构最直接的继承者 [AlphaProof](https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/) 结合语言模型与 AlphaZero 的强化学习和搜索算法，学会了证明形式化的数学命题。它与 AlphaGeometry 2 一起，成为首个在国际数学奥林匹克竞赛（IMO）中达到奖牌水准（银牌）的系统，证明了 AlphaGo 的方法能够解锁高级数学推理，并为我们最强能力的通用模型奠定了基础。

Gemini——我们最大、能力最强的模型——最近走得更远。其 Deep Think 模式的进阶版本[在 2025 年 IMO 上取得了金牌水准的成绩](https://deepmind.google/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/)，所用方法正是受 AlphaGo 启发。此后，Deep Think 已被[应用](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-deep-think/)于科学与工程中更复杂、更开放性的挑战。

**算法发现：** 正如 AlphaGo 在博弈中搜索最佳落子，我们的编码智能体 [AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) 在计算机代码的空间中探索，以发现更高效的算法。它也有属于自己的「第 37 手」时刻——找到了一种新颖的矩阵乘法方法，而矩阵乘法是驱动几乎所有现代神经网络的基础数学运算。如今，AlphaEvolve 正在被用于从数据中心优化到量子计算的各类问题。

**科学协作：** 我们正在把随 AlphaGo 开创的搜索与推理原则整合进一个 [AI co-scientist（AI 协同科学家）](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/)。通过让智能体「辩论」科学想法与假说，这个系统扮演着一位协作者的角色，能够完成在数据中识别模式、求解复杂问题所需的严谨思考。在[帝国理工学院](https://www.imperial.ac.uk/news/261293/googles-ai-co-scientist-could-enhance-research/)的验证研究中，它分析了数十年的文献，并独立得出了与研究人员花多年时间开发并通过实验验证的抗菌素耐药性假说相同的结论。

我们还利用 AI 来[更好地理解基因组](https://deepmind.google/blog/alphagenome-ai-for-better-understanding-the-genome/)、[推进聚变能源研究](https://deepmind.google/blog/bringing-ai-to-the-next-generation-of-fusion-energy/)、[改进天气预测](https://deepmind.google/science/weathernext/)等等。

尽管这些科学模型令人印象深刻，但它们高度专精。要实现像创造无限的清洁能源或攻克我们今天尚不理解的疾病这样的根本性突破，我们需要通用的 AI 系统：能够发现不同学科之间的底层结构与关联，并像最优秀的科学家那样帮助我们提出新假说。

## 智能的未来

一个 AI 若要真正做到「通用」，就需要理解物理世界。我们从一开始就把 Gemini 构建为多模态模型，使其不仅能理解语言，还能理解音频、视频、图像和代码，从而构建世界模型。

为了在这些模态之间进行思考与推理，最新的 Gemini 模型使用了我们随 AlphaGo 和 AlphaZero 开创的部分技术。

下一代 AI 系统还需要能够调用专门的工具。例如，如果一个模型需要知道某种蛋白质的结构，它就可以调用 AlphaFold 来完成。

我们认为，Gemini 的世界模型、AlphaGo 的搜索与规划技术，以及专门的 AI 工具使用三者的结合，对 AGI 而言将至关重要。

真正的创造力是这样一个 AGI 系统必须展现的关键能力。「第 37 手」让我们窥见了 AI 跳出思维定式的潜力，但真正原创性的发明还需要更多。它不仅要能像 AlphaGo 令人赞叹地做到的那样，提出一种新颖的围棋策略，还要能真正发明出一种和围棋一样深邃、优雅、值得研究的博弈。

在 AlphaGo 传奇性胜利十年之后，我们的终极目标已在地平线上显现。「第 37 手」最初迸发的创造火花催化了众多突破，它们如今正汇聚起来，铺就通往 AGI 的道路——并开启科学发现的崭新黄金时代。

整整十年过去，我们回望那场点燃现代 AI 革命的比赛。

[了解 AlphaGo](https://deepmind.google/research/alphago/)[在 YouTube 上观看 AlphaGo 纪录片](https://www.youtube.com/watch?v=WXuK6gekU1Y)
