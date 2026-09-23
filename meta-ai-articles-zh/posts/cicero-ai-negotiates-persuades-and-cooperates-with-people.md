---
title: "CICERO：能与人谈判、说服并合作的 AI 智能体"
title_en: "CICERO: An AI agent that negotiates, persuades, and cooperates with people"
date: 2022-11-22
source: http://ai.facebook.com/blog/cicero-ai-negotiates-persuades-and-cooperates-with-people
crawled: 2026-09-22
translated: 2026-09-22
---

# CICERO：能与人谈判、说服并合作的 AI 智能体

> 原文：[CICERO: An AI agent that negotiates, persuades, and cooperates with people](http://ai.facebook.com/blog/cicero-ai-negotiates-persuades-and-cooperates-with-people) · Meta AI（Wayback 存档）

游戏一直是 AI 新进展的试验场——从 Deep Blue 战胜国际象棋特级大师 Garry Kasparov，到 AlphaGo 精通围棋，再到 Pluribus 在扑克中唬住最优秀的人类选手。但真正有用、通用的智能体需要超越仅仅在棋盘上移动棋子。我们能否构建更有效、更灵活的智能体，能像人类那样使用语言去谈判、说服并与他人合作以实现战略目标？

今天，我们宣布在构建掌握了这些技能的 AI 方面取得突破。我们构建了一个名为 CICERO 的智能体——这是首个在流行策略游戏《外交》（Diplomacy*）中达到人类水平的 AI。CICERO 在该游戏的在线版本 webDiplomacy.net 上展示了这一点：它的得分是人类玩家平均分的两倍以上，在玩过多局的参与者中排名前 10%。

数十年来，《外交》一直被视为 AI 领域近乎不可能完成的大挑战，因为它要求玩家掌握理解他人动机与视角的艺术；制定复杂计划并调整策略；然后使用自然语言与他人达成协议、说服他们结成伙伴关系与联盟等等。CICERO 在《外交》中使用自然语言与人谈判的能力如此之强，以至于人们常常更愿意与 CICERO 合作，而不是与其他人类参与者合作。

与国际象棋和围棋不同，《外交》是一款关于人而非棋子的游戏。如果智能体无法识别某人可能正在虚张声势，或者另一个玩家会把某步棋视为挑衅，它很快就会输掉比赛。同样，如果它说话不像真人——展现共情、建立关系、有见地地谈论游戏——它就找不到愿意与它合作的其他玩家。

我们取得这一成就的关键，是在两个截然不同的 AI 研究领域的交叉点上开发了新技术：一是用于 AlphaGo 和 Pluribus 等智能体的战略推理，二是用于 GPT-3、BlenderBot 3、LaMDA 和 OPT-175B 等模型的自然语言处理。例如，CICERO 可以推断出自己在游戏后期需要某个特定玩家的支持，然后制定赢得该玩家好感的策略——甚至能从该玩家独特的视角识别其看到的风险与机会。

我们已经开源了代码并发表了论文，帮助更广泛的 AI 社区利用 CICERO 推动人机合作的进一步进展。你也可以访问 CICERO 网站了解该项目并观看智能体的实战。有兴趣的研究者可以向 CICERO RFP 提交申请以获取数据。

## 幕后：我们如何构建 CICERO

CICERO 的核心是一个面向《外交》的可控对话模型，与一个战略推理引擎相耦合。在游戏的每个节点，CICERO 会查看棋盘状态和对话历史，并建模其他玩家可能如何行动。然后它利用这个计划来控制一个能生成自由对话的语言模型：告知其他玩家自己的计划，并为其他玩家提出能与之良好协同的合理行动。

### 可控对话

为了构建可控对话模型，我们从一个 27 亿参数、类 BART 的语言模型开始，先在互联网文本上预训练，再在 webDiplomacy.net 上超过 40000 局人类对局上微调。我们开发了自动将训练数据中的消息与游戏中相应计划走法对应标注的技术，这样在推理时就可以控制对话生成，讨论智能体及其对话伙伴的具体期望行动。例如，如果我们的智能体扮演法国，基于「英国支持法国进入勃艮第」的计划来约束对话模型，可能会生成给英国的消息：「你好英国！这回合你愿意支持我进入勃艮第吗？」以这种方式控制生成，可以让 CICERO 把对话锚定在一组随时间推移不断制定和修正的计划上，以便更好地谈判。这有助于智能体更有效地与其他玩家协调并说服他们。

- 第 1 步：利用棋盘状态和当前对话，CICERO 对所有人的行动做出初步预测。
- 第 2 步：CICERO 通过规划迭代地细化该预测，然后利用这些预测为自己和伙伴形成意图。
- 第 3 步：它基于棋盘状态、对话和意图生成多条候选消息。
- 第 4 步：它过滤候选消息，以减少无意义内容、最大化价值并确保与意图一致。

我们进一步使用多种过滤机制来提升对话质量——例如训练用来区分人类文本与模型生成文本的分类器——以确保对话合理、与当前游戏状态和先前消息一致，且在战略上站得住脚。

### 对话感知的策略与规划

国际象棋、围棋和扑克等对抗游戏中此前的超人智能体，都是通过自博弈强化学习（RL）创造的——让智能体通过与自身副本进行数百万局对局来学习最优策略。然而，涉及合作的游戏需要建模人类在现实中实际会做什么，而不是建模当他们是完全理性副本时应该做什么。特别是，我们希望 CICERO 制定的计划与其同其他玩家的对话保持一致。

人类建模的经典方法是有监督学习，即用带标注的数据（例如人类玩家过往对局行动的数据库）训练智能体。然而，纯粹依靠有监督学习根据过往对话选择行动，会导致智能体相对较弱且极易被利用。例如，玩家可以对智能体说：「很高兴我们说好了你会把部队撤出巴黎！」由于训练数据中类似消息只在达成协议时出现，智能体可能真的会把部队撤出巴黎，哪怕这显然是战略失误。

为了解决这个问题，CICERO 运行一个迭代规划算法，在对话一致性与理性之间取得平衡。智能体首先根据它与其他玩家的对话预测所有人本回合的策略，并预测其他玩家认为智能体会采取什么策略。然后它运行我们开发的规划算法 piKL：该算法在尽量选择「给定其他玩家预测策略后期望值更高」的新策略的同时，尽量让新预测与原始策略预测保持接近，从而迭代改进这些预测。我们发现，与单纯的有监督学习相比，piKL 能更好地建模人类行为，也为智能体带来更好的策略。

## 生成自然而有目的的对话

在《外交》中，玩家如何与人交谈，可能比如何移动棋子更重要。CICERO 在与其他玩家商讨战略时能够清晰而有说服力地表达。例如，在一局演示对局中，CICERO 一边请求某位玩家立即在棋盘一处提供支援，一边敦促另一位玩家考虑在游戏后期结盟。在这些交流中，CICERO 试图通过向三位不同玩家提议走法来执行其策略。在第二段对话中，智能体能告诉对方为什么应该合作以及这对双方如何互利。在第三段中，CICERO 既在收集信息，也在为后续行动铺路。

## 仍有改进空间的地方

必须指出，CICERO 有时也会生成可能损害其目标的不一致对话。在下面 CICERO 扮演奥地利的例子中，智能体与第一条要求意大利移向威尼斯的消息自相矛盾。虽然我们的过滤器组合旨在检测这类错误，但它并不完美。

## 《外交》作为推进人机交互的沙盒

在一款既含合作又含竞争的游戏中出现目标导向的对话系统，在让 AI 与人类意图和目标对齐方面提出了重要的社会与技术挑战。《外交》为研究这一问题提供了特别有趣的环境，因为玩这款游戏需要应对相互冲突的目标，并将这些复杂目标转化为自然语言。举个简单的例子：玩家可能选择在短期利益上妥协以保住盟友，指望这位盟友在下一回合帮助自己取得更有利的局面。尽管我们在这项工作中取得了重大进展，但「让语言模型稳健地与特定意图对齐的能力」以及「决定这些意图的技术（和规范性）挑战」仍然是悬而未决的重要问题。

通过开源 CICERO 代码，我们希望 AI 研究者能够以负责任的方式在我们的工作之上继续构建。我们已经迈出早期步伐，利用我们的对话模型进行零样本分类，以检测并移除这个新领域中的有害消息。我们希望《外交》能作为一个安全的沙盒，推进人机交互研究。

## 未来方向

虽然 CICERO 只会玩《外交》，但这一成就背后的技术与许多现实世界应用相关。例如，通过规划和 RL 控制自然语言生成，可以缓解人类与 AI 驱动的智能体之间的沟通障碍。如今的 AI 助手擅长简单的问答任务，比如告诉你天气，但如果它们能以教会你一项新技能为目标进行长期对话呢？或者想象一款电子游戏，其中的非玩家角色（NPC）能像人一样规划与交谈——理解你的动机并相应调整对话——在你攻占城堡的征途中助你一臂之力。我们对这些领域的未来进展潜力感到兴奋，也期待看到他人在我们研究基础上的构建。

阅读论文 · 访问 CICERO 网站 · 了解 RFP

我们要感谢为这项工作做出贡献的庞大团队：Anton Bakhtin, Noam Brown, Emily Dinan, Gabriele Farina, Colin Flaherty, Daniel Fried, Andrew Goff, Jonathan Gray, Hengyuan Hu, Athul Paul Jacob, Mojtaba Komeili, Karthik Konath, Adam Lerer, Mike Lewis, Alexander H. Miller, Sasha Mitts, Adithya Renduchintala, Stephen Roller, Dirk Rowe, Weiyan Shi, Joe Spisak, Alexander Wei, David Wu, Hugh Zhang, Markus Zijlstra, Ana Paula Kirschner Mofarrej, Anne Davidson, Oliver Libaw, Amanda Felix, Karla Caraballo-Torres, Christopher Johnson, Lydia Baillergeau, Julia Vargas, Eric Kaplan, Raghu Nayani, Aiman Farooq, Andrea Cheung, Emily Astbury, Gopika Jhala, Jon Carvill, Jon Shepherd, Josh Terry, Marina Zannoli, Nathan Riley, Michelle Restrepo, Noah Rizk, Ritika Trikha, Steph Miles, Tamara Piksa, Zara Blum, Daniel Duncan, Antoine Bordes, Laurens van der Maaten, Alex Boesenberg, Korey Anvaripour, Somya Jain, Harrison Rudolph, Michael Friedrichs, Elisabeth Sperle, and Cesar Guiterrez。

*《外交》的所有权利归 Hasbro, Inc. 所有。
