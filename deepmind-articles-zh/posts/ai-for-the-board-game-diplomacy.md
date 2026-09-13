---
title: "用于棋盘游戏《外交》的 AI"
title_en: "AI for the board game Diplomacy"
source: https://deepmind.google/blog/ai-for-the-board-game-diplomacy/
site: deepmind
date: 2022-12-06
crawled: 2026-09-13
translated: 2026-09-13
---

# 用于棋盘游戏《外交》的 AI

> 原文：[AI for the board game Diplomacy](https://deepmind.google/blog/ai-for-the-board-game-diplomacy/) · Google DeepMind

智能体通过沟通与谈判实现更好的合作，而对违背承诺者施加惩罚则有助于让它们保持诚实

纵观历史，成功的沟通与合作一直是推动社会进步的关键。棋盘游戏的封闭环境可以作为一个沙盒，用来建模和研究交互与沟通——而我们能从对弈中学到很多东西。在我们[今天发表于《自然·通讯》（Nature Communications）](https://www.nature.com/articles/s41467-022-34473-5)的最新论文中，我们展示了人工智能体如何利用沟通在棋盘游戏《外交》（Diplomacy）中更好地合作。该游戏以注重结盟著称，是人工智能（AI）研究中一个充满活力的领域。

《外交》之所以具有挑战性，是因为它的规则简单，但由于玩家之间存在强烈的相互依赖，加之巨大的动作空间，游戏呈现出很高的涌现复杂性。为帮助应对这一挑战，我们设计了谈判算法，让智能体能够就联合行动方案进行沟通并达成一致，从而使它们能够战胜缺乏这种能力的智能体。

当我们无法指望同伴信守承诺时，合作就尤其困难。我们以《外交》作为沙盒，探究当智能体可能背弃过往协议时会发生什么。我们的研究揭示了当复杂智能体能够歪曲自己的意图或就未来计划误导他人时所产生的风险，这也引出了另一个重大问题：什么样的条件能够促成可信赖的沟通与团队协作？

我们证明，惩罚违约同伴的策略能大幅降低它们背弃承诺所能获得的收益，从而促成更诚实的沟通。

## 《外交》是什么，为什么它很重要？

[国际象棋](https://en.wikipedia.org/wiki/Deep_Blue_(chess_computer))、[扑克](https://en.wikipedia.org/wiki/Computer_poker_player)、[围棋](https://en.wikipedia.org/wiki/AlphaGo)以及许多[电子游戏](https://en.wikipedia.org/wiki/AlphaStar_(software))一直是 AI 研究的沃土。[《外交》](https://en.wikipedia.org/wiki/Diplomacy_(game))是一款七人谈判与结盟游戏，棋盘是一张被划分为多个省份的旧欧洲地图，每位玩家控制多个单位（[《外交》规则](https://media.wizards.com/2015/downloads/ah/diplomacy_rules.pdf)）。在名为"公开外交"（Press Diplomacy）的标准版本中，每个回合都包含一个谈判阶段，谈判结束后所有玩家同时亮出自己选择的行动。

《外交》的核心是谈判阶段，玩家在谈判中努力就下一步行动达成一致。例如，一个单位可以支援另一个单位，帮助它克服其他单位的抵抗，如下图所示：

![两幅并排的法国地图，展示两种移动情形。左边，两个单位——勃艮第的红方士兵图形与箭头，以及加斯科尼的蓝方士兵图形与箭头——都试图进入巴黎地区。由于双方兵力相当，谁都没有成功。右边，皮卡第的红方单位支援勃艮第的红方单位，压制了加斯科尼的蓝方单位，使红方单位得以进入勃艮第。](https://lh3.googleusercontent.com/SeB3fQbZy8hYrqEo5Zm2TSAT6_d6NsV0YXC6bbtpL802esmYrTGRmFjyVP9AeIbi1aguiS4ASoSxcHcYyIKhTiEBhiYz14eJWCctiAogYkPYW77cqw=w1440)

**两种移动情形。**
**左：**两个单位（勃艮第的红方单位与加斯科尼的蓝方单位）都试图进入巴黎。由于双方兵力相当，谁都没有成功。
**右：**皮卡第的红方单位支援勃艮第的红方单位，压制了蓝方单位，使红方单位得以进入勃艮第。

针对《外交》的计算方法研究可以追溯到 20 世纪 80 年代，其中许多研究是在一个名为"无谈判外交"（No-Press Diplomacy）的简化版本上开展的，该版本不允许玩家之间进行策略性沟通。研究者们还提出了[对计算机友好的谈判协议](http://www.daide.org.uk/)，有时被称为"受限谈判"（Restricted-Press）。

## 我们研究了什么？

我们用《外交》类比现实世界的谈判，为 AI 智能体提供协调行动的方法。我们取[不会沟通的《外交》智能体](https://www.deepmind.com/publications/learning-to-play-no-press-diplomacy-with-best-response-policy-iteration)，通过赋予它们一套协商联合行动方案契约的协议，将其增强为能够带沟通对弈《外交》的智能体。我们把这种增强后的智能体称为基线谈判者（Baseline Negotiator），它们会受自己协议的约束。

![两幅并排的法国地图，展示《外交》中的契约。左边，一条带叉的粉色箭头表示限制，阻止红方玩家从鲁尔移动到勃艮第；而一条从皮埃蒙特红方玩家指向马赛的粉色箭头则允许这一移动。右边的地图相同，只是在布雷斯特与加斯科尼之间多了一条粉色箭头。](https://lh3.googleusercontent.com/g-1iYXu5iFalP5lRCKkoNi7lsW7PT31a8vOTaV-iajiV-7veK0qK6rrbA-tzflULaVmzDxiOvoK1RfbtUGiCLlJOIHTGhUHhSxsaywKLnkdHyD4f=w1440)

**《外交》契约。**
**左：**一种只允许红方玩家采取特定行动的限制（他们不得从鲁尔移动到勃艮第，且必须从皮埃蒙特移动到马赛）。
**右：**红方玩家与绿方玩家之间的一份契约，对双方都施加了限制。

我们考察两种协议：互提议协议（Mutual Proposal Protocol）与提议-选择协议（Propose-Choose Protocol），[完整论文](https://www.nature.com/articles/s41467-022-34473-5)中有详细讨论。我们的智能体所应用的算法，会通过模拟游戏在各种契约下可能如何展开来识别互利的交易。我们以[博弈论](https://en.wikipedia.org/wiki/Game_theory)中的[纳什议价解](https://en.wikipedia.org/wiki/Cooperative_bargaining#:~:text=Nash%20bargaining%20game,-John%20Forbes%20Nash&text=His%20solution%20is%20called%20the,and%20independence%20of%20irrelevant%20alternatives.)（Nash Bargaining Solution）作为识别高质量协议的原则性基础。游戏可能随玩家行动以多种方式展开，因此我们的智能体使用蒙特卡洛模拟来观察下一回合可能发生什么。

![给定契约下下一状态模拟的地图图像。左边是当前状态的地图。右边是三幅较小的地图，展示多个可能的下一状态。](https://lh3.googleusercontent.com/aom4EV1Ay_Ibt4eYG_18K4AJhiq2kseick_zbz_SOch2F_cS1HG6FIZO_eC3MNblwUqn53GHuJyX08LHD4_wVToifsYmOqXMZmwJ3qiBpMT2due-=w1440)

在给定契约下模拟下一状态。左：棋盘某一区域的当前状态，包括红方与绿方玩家之间达成的一份契约。右：多个可能的下一状态。

我们的实验表明，我们的谈判机制让基线谈判者显著胜过基线的非沟通型智能体。

![两张图表，显示基线谈判者显著胜过非沟通型智能体。左图对应互提议协议，右图对应提议-选择协议。](https://lh3.googleusercontent.com/4DPDARaNRFGuI2QMVIqO58kqihMRdaqxvBAG5s7qwR55aQAbsZkt761dAXcTdQRQpNpMlU846EDhT0SpwQQIu_dhKGFHM9Orhd5AC__bRjqlfuALhg=w1440)

基线谈判者显著胜过非沟通型智能体。左：互提议协议。右：提议-选择协议。"谈判者优势"是指沟通型智能体与非沟通型智能体胜率之比。

## 违背协议的智能体

在《外交》中，谈判达成的协议并不具约束力（沟通属于"[廉价磋商](https://en.wikipedia.org/wiki/Cheap_talk#:~:text=In%20game%20theory%2C%20cheap%20talk,the%20state%20of%20the%20world.)"（cheap talk））。那么，当一个智能体在这一回合同意契约、下一回合却背离它时，会发生什么？在许多现实场景中，人们约定以某种方式行事，但随后却未能履行承诺。要让 AI 智能体之间、或智能体与人类之间实现合作，我们必须审视智能体策略性违背协议这一潜在陷阱，以及补救这一问题的办法。我们借助《外交》研究了背弃承诺的能力如何侵蚀信任与合作，并识别出促成诚实协作的条件。

于是我们考察了背叛者智能体（Deviator Agent），它们通过背离已达成的契约来战胜诚实的基线谈判者。简单背叛者（Simple Deviator）只是"忘记"自己同意过契约，随意行动。条件背叛者（Conditional Deviator）更为精明，它们在优化自己的行动时，会假定接受契约的其他玩家将依约行事。

![示意图，用绿色方框展示所有类型的沟通型智能体。其中一些引出蓝色方框，代表具体的智能体算法。](https://lh3.googleusercontent.com/gLIpehcVdrgG6HqkIV5Sk7jMC6Nd8yMlyISOmOUr492GKWGDFe_7D4ZuBsgQc6blRVH0LJtzm3c9Y9STUA3IrW5EkbFs91OTory5EomPMhLEvdwul50=w1440)

我们所有类型的沟通型智能体。在绿色分组标签之下，每个蓝色方块代表一种具体的智能体算法。

我们证明，简单背叛者与条件背叛者都显著胜过基线谈判者，其中条件背叛者的优势尤为压倒性。

![两张图表，对比背叛者智能体与基线谈判者智能体。左图展示互提议协议，右图展示提议-选择协议。](https://lh3.googleusercontent.com/Vg7_bhmDBR2G56_astmZZZY7SYFzKQelJvSxAb7-fotvGx7U4oGW6ExeuPOQSWfVEN7iNManFkMM4bEXRt-1H2jszoEcguL78ZvEAkzERGF4OT_NEg=w1440)

背叛者智能体对阵基线谈判者智能体。左：互提议协议。右：提议-选择协议。"背叛者优势"是指背叛者智能体相对基线谈判者的胜率之比。

## 鼓励智能体保持诚实

接下来，我们用防御型智能体（Defensive Agent）来应对背叛问题，它们会对背叛行为做出不利反应。我们研究了二元谈判者（Binary Negotiator），它们会简单地切断与违约智能体的沟通。但回避是一种温和的反应，因此我们还开发了惩罚型智能体（Sanctioning Agent），它们不会轻饶背叛行为，而是修改自己的目标，主动设法降低背叛者的价值——一个记仇的对手！我们证明，两类防御型智能体都能削弱背叛的优势，尤其是惩罚型智能体。

![两张图表，对比背叛者智能体与基线谈判者智能体。左图展示互提议协议，右图对应提议-选择协议。](https://lh3.googleusercontent.com/45v1YOhCJl4-VQ_aTRdDif-ZPc57voNR8RXROpcI41rbPAAFoVN1i7K1gTdWUD97OY7rbbwsE70fhgg57IrfeWmv5raCuZz4PUmjIq76Ddn3TNuw5w=w1440)

非背叛者智能体（基线谈判者、二元谈判者与惩罚型智能体）对阵条件背叛者。左：互提议协议。右：提议-选择协议。"背叛者优势"低于 1 的数值表示防御型智能体胜过背叛者智能体。与基线谈判者群体（灰色）相比，二元谈判者群体（蓝色）削弱了背叛者的优势。

最后，我们引入了习得型背叛者（Learned Deviator），它们会在多局对弈中针对惩罚型智能体调整并优化自己的行为，试图让上述防御手段失效。习得型背叛者只有在背叛的即时收益足够高、且对方的报复能力足够低时才会撕毁契约。在实践中，习得型背叛者偶尔会在游戏后期违约，并借此对惩罚型智能体取得轻微优势。尽管如此，这类惩罚仍驱使习得型背叛者履行了超过 99.7% 的契约。

我们还考察了惩罚与背叛可能的学习动态：当惩罚型智能体也可能违约时会发生什么，以及当惩罚行为本身有代价时停止惩罚的潜在激励。这类问题会逐渐侵蚀合作，因此可能需要额外的机制，例如跨多局重复互动，或使用信任与声誉系统。

我们的论文留下了许多供未来研究的问题：能否设计出更精巧的协议，促成更诚实的行为？如何将沟通技术与不完全信息结合起来处理？还有哪些其他机制可以威慑违约行为？构建公平、透明、可信赖的 AI 系统是一个极其重要的课题，也是 DeepMind 使命的关键部分。在《外交》这样的沙盒中研究这些问题，有助于我们更好地理解现实世界中可能存在的合作与竞争之间的张力。归根结底，我们相信，应对这些挑战能让我们更好地理解如何开发符合社会价值观与优先事项的 AI 系统。

请[在此](https://www.nature.com/articles/s41467-022-34473-5)阅读我们的完整论文。

**致谢**

我们感谢 Will Hawkins、Aliya Ahmad、Dawn Bloxwich、Lila Ibrahim、Julia Pawar、Sukhdeep Singh、Tom Anthony、Kate Larson、Julien Perolat、Marc Lanctot、Edward Hughes、Richard Ives、Karl Tuyls、Satinder Singh 与 Koray Kavukcuoglu 在整个研究过程中给予的支持与建议。

**完整论文作者**

János Kramár、Tom Eccles、Ian Gemp、Andrea Tacchetti、Kevin R. McKee、Mateusz Malinowski、Thore Graepel、Yoram Bachrach。
