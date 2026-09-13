---
title: "驾驭《军棋》：不完全信息的经典游戏"
title_en: "Mastering Stratego, the classic game of imperfect information"
source: https://deepmind.google/blog/mastering-stratego-the-classic-game-of-imperfect-information/
site: deepmind
date: 2022-12-01
crawled: 2026-09-13
translated: 2026-09-13
---

# 驾驭《军棋》：不完全信息的经典游戏

> 原文：[Mastering Stratego, the classic game of imperfect information](https://deepmind.google/blog/mastering-stratego-the-classic-game-of-imperfect-information/) · Google DeepMind

DeepNash 结合博弈论与免模型深度强化学习，从零学会下《军棋》

下棋类人工智能（AI）系统已经迈向一个新的前沿。《军棋》（Stratego）这款经典棋盘游戏比国际象棋和围棋更复杂，比扑克更诡谲，如今也已被驾驭。[论文发表于《科学》（Science）](https://www.science.org/stoken/author-tokens/ST-887/full)，我们展示了 DeepNash——一个通过与自己对弈、从零开始学到人类专家水平《军棋》的 AI 智能体。

DeepNash 采用了一种基于博弈论与免模型深度强化学习相结合的新颖方法。它的下法收敛到纳什均衡，这意味着对手极难加以利用。实际上难到什么程度呢——DeepNash 在全球最大的在线《军棋》平台 Gravon 的人类专家中取得了有史以来前三的排名。

棋盘游戏历来是衡量 AI 领域进步的标尺，让我们得以在受控环境中研究人类与机器如何制定并执行策略。与国际象棋和围棋不同，《军棋》是一款不完全信息游戏：玩家无法直接观察对手棋子的身份。

正是这种复杂性，使得其他基于 AI 的《军棋》系统一直难以超越业余水平。这也意味着，此前被用于驾驭许多完美信息游戏的非常成功的 AI 技术——"博弈树搜索"——对《军棋》而言扩展性不足。正因如此，DeepNash 彻底超越了博弈树搜索。

驾驭《军棋》的价值不止于游戏本身。在践行"求解智能、推动科学、造福人类"这一使命的过程中，我们需要构建能够在复杂真实情境中运转的先进 AI 系统——在这些情境中，关于其他智能体和人的信息是有限的。我们的论文展示了 DeepNash 如何被应用于不确定性情境，并成功地在各种结果之间取得平衡，帮助解决复杂问题。

## 认识《军棋》

《军棋》是一款回合制的夺旗游戏。它是一场虚张声势与战术的较量，是情报收集与微妙调兵的艺术。它还是一场零和游戏：任何一方所得，都意味着对手损失同等的价值。

《军棋》对 AI 具有挑战性，部分原因在于它是一款不完全信息游戏。双方玩家开局时可以随意布置自己的 40 枚棋子，并且在游戏开始时彼此隐藏。由于双方掌握的信息不同，他们在决策时必须权衡所有可能的结果——这为研究策略互动提供了一个富有挑战性的基准测试。棋子的类型与等级如下图所示。

![一张信息示意图，展示《军棋》的棋子与棋盘布局。左侧是一个纵向的等级结构，显示从最高战力（10：元帅）到最低（S：间谍）的棋子等级，以及炸弹（B）和军旗（F）等特殊棋子。箭头指示战力递增方向，并标明间谍可以俘获元帅。右侧是两幅并排的《军棋》棋盘图：一幅是完整的开局布置，红方棋子背对隐藏；另一幅是中盘状态，棋盘上若干蓝方和红方棋子已被翻开。](https://lh3.googleusercontent.com/2EDBMJ-WtTEw6GluHj-T23uUmQzYl7G2YIkiI5L-n1LyZGudfJ8Dn7txGUJQe6Pe5-47ee65E62yaGpOslmMhiJ8LqdL1v8f3XDUX35V1Kln5IONhA=w1440)

**左：**棋子等级。在交战中，等级高的棋子获胜，但例外是 10（元帅）在被间谍攻击时落败，而炸弹总是获胜，除非被工兵拆除。
**中：**一种可能的开局布置。注意军旗被安全地藏在了后排，两侧是用于护卫的炸弹。两块淡蓝色区域是"湖泊"，任何棋子都不得进入。
**右：**一局进行中的对弈，显示蓝方的间谍俘获了红方的 10。

在《军棋》中，情报得来不易。对手棋子的身份通常只有当它与另一方在战场上遭遇时才会揭晓。这与国际象棋或围棋等完美信息游戏形成鲜明对比——在后者的棋盘上，每枚棋子的位置和身份对双方都是公开的。

在完美信息游戏上表现出色的机器学习方法，例如 DeepMind 的 [AlphaZero](https://deepmind.google/blog/alphazero-shedding-new-light-on-chess-shogi-and-go/)，并不能轻易迁移到《军棋》。需要在信息不完备的情况下做决策、以及虚张声势的可能性，让《军棋》更接近德州扑克，并需要一种类似人类的能力——美国作家杰克·伦敦（Jack London）曾这样形容："人生并不总是握有一手好牌，有时是要把一手烂牌打好。"

然而，在德州扑克等游戏中行之有效的 AI 技术同样无法照搬到《军棋》，原因在于游戏长度惊人——通常要经过数百步棋才能分出胜负。《军棋》中的推理必须在大量连续动作上进行，而每个动作对最终结果的贡献并无直观线索可循。

最后，《军棋》的可能棋局状态数量（以"博弈树复杂度"衡量）远超国际象棋、围棋和扑克，求解难度极高。这正是《军棋》令我们兴奋之处，也是它数十年来一直是对 AI 社区的挑战的原因。

![一张对比表格，展示国际象棋、扑克、19 路围棋和《军棋》的游戏复杂度。与国象、扑克和围棋相比，《军棋》的单局回合数（约 1000）、开局布置数（$10^{66}$）和博弈树复杂度（$10^{535}$）均为最高（围棋的博弈树复杂度 $10^{360}$ 除外）。](https://lh3.googleusercontent.com/Q0y8T7O2QH6WGo37LlTxOAGxnTe-VTe5BGJEliTjR534qNFMngVp6m7RSVBIXUYWy1U6Zgq6YhA5eqNxeY2EBWVCv-NFJtjR5iBUu7iLzz_meXtN=w1440)

国际象棋、扑克、围棋与《军棋》之间差异的量级。

## 寻求均衡

DeepNash 采用了一种基于博弈论与免模型深度强化学习相结合的新颖方法。"免模型"意味着 DeepNash 在对局中并不试图显式建模对手的私有棋局状态。尤其是在游戏的早期阶段，当 DeepNash 对对手棋子知之甚少时，这种建模即便可行也难有效果。

而且由于《军棋》的博弈树复杂度太过庞大，DeepNash 无法采用 AI 博弈中的一大支柱方法——蒙特卡洛树搜索。树搜索一直是 AI 在复杂度较低的棋盘游戏和扑克上众多里程碑成就的关键要素。

相反，DeepNash 由一个新颖的博弈论算法思想驱动，我们称之为正则化纳什动力学（Regularised Nash Dynamics，R-NaD）。R-NaD 在空前的规模上工作，引导 DeepNash 的学习行为趋向所谓的纳什均衡（技术细节请深入阅读[我们的论文](https://www.science.org/stoken/author-tokens/ST-887/full)）。

收敛到纳什均衡的下法随时间推移是无法被利用的。如果一个人或机器下出完美无法被利用的《军棋》，它能达到的最差胜率将是 50%，而且只有面对同样完美的对手时才会如此。

在与最强《军棋》机器人的对局中——包括多位计算机《军棋》世界锦标赛冠军——DeepNash 的胜率超过 97%，并经常达到 100%。在 Gravon 游戏平台上对阵顶尖人类专家时，DeepNash 取得了 84% 的胜率，赢得了有史以来前三的排名。

## 预料之外

为取得这些成果，DeepNash 在初始布子阶段和对局阶段都展现出一些非凡的行为。为了变得难以被利用，DeepNash 发展出一种不可预测的策略。这意味着初始布子要足够多变，以免对手在一系列对局中发现规律。而在对局阶段，DeepNash 会在看似等价的动作之间随机选择，以避免形成可被利用的倾向。

《军棋》玩家都力求难以捉摸，因此隐藏信息自有其价值。DeepNash 以相当惊人的方式展示了它对信息的珍视。在下图的例子中，对阵一位人类玩家时，DeepNash（蓝方）在开局不久便牺牲了 7（少将）和 8（上校）等棋子，结果得以定位对手的 10（元帅）、9（中将）、一个 8 和两个 7。

![一幅《军棋》棋盘图，展示一个中盘状态：DeepNash（蓝方，下方）已牺牲数枚棋子来翻开关键的红方棋子（上方），包括对手的 10（元帅）、9（中将）、8（上校）和若干 7（少将），使蓝方处于子力劣势，但获得了战略信息优势。](https://lh3.googleusercontent.com/q8fmY1CTMaVWZz-tjRb55twuAVxGKGQ5McVcxmoSgG0nZhpYunnkUgsn-ilfO_SeFmNZL9IqrckLOrUQ98PIp69JtplrmINn1Siqa_2G8LT8uNFVCw=w1440)

在这一开局局面中，DeepNash（蓝方）已经摸清了对手许多最强棋子的位置，同时自己的关键棋子仍秘而不宣。

这些努力让 DeepNash 付出了显著的子力代价：它损失了一个 7 和一个 8，而它的人类对手保住了所有 7 级及以上的棋子。尽管如此，由于已确切掌握对手高层棋子的情报，DeepNash 评估自己的胜算为 70%——并最终获胜。

## 诈唬的艺术

和扑克一样，优秀的《军棋》玩家有时必须示强，即便自己虚弱。DeepNash 学会了多种此类诈唬战术。在下图的例子中，DeepNash 用一枚 2（弱小的侦察兵，对手并不知情）来追逐对手已暴露的 8，俨然一枚高等级棋子。人类对手判断追兵很可能是 10，于是试图用间谍（S）设伏诱杀。DeepNash 这一战术只冒着一枚小棋子的风险，却成功地把对手的关键棋子间谍引出并消灭。

![一幅《军棋》棋盘图，展示一种诈唬战术：DeepNash（蓝方）用弱小的 2（侦察兵）追逐对手的 8（上校），诱使对手（红方）试图用间谍（S）设伏围歼它。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6388cd77afcbf805472dd426_6384d343d2251b2c90fdbb17_Fig-4-crop.gif)

人类玩家（红方）确信，追赶自己那枚 8 的未知棋子一定是 DeepNash 的 10（注：DeepNash 已损失了它唯一的 9）。

观看 DeepNash 对阵（匿名化处理的）人类专家的四局完整对局视频，了解更多：[第 1 局](https://youtu.be/HaUdWoSMjSY)、[第 2 局](https://youtu.be/L-9ZXmyNKgs)、[第 3 局](https://youtu.be/EOalLpAfDSs)、[第 4 局](https://youtu.be/MhNoYl_g8mo)。

> DeepNash 的棋艺水平让我吃惊。我从未听说过哪个人工《军棋》玩家能接近战胜经验丰富的人类棋手所需的水平。但在亲自与 DeepNash 对弈之后，我对它后来在 Gravon 平台上取得前三的排名丝毫不感意外。我预计，如果允许它参加人类世界锦标赛，它会有非常出色的表现。

Vincent de Boer

论文共同作者、前《军棋》世界冠军

## 未来方向

虽然我们是为《军棋》这个高度明确的世界开发 DeepNash 的，但我们新颖的 R-NaD 方法可以直接应用于其他双人零和游戏，无论其信息是完美还是不完美。R-NaD 有潜力泛化到双人博弈场景之外，去解决大规模的现实世界问题——这些问题往往以信息不完备和天文数字般的状态空间为特征。

我们还希望 R-NaD 能帮助解锁 AI 在其他领域的新应用：这些领域有大量目标各异的人类或 AI 参与者，他们可能不了解彼此的意图或环境中正在发生的事情，例如大规模优化交通管理以缩短司机的出行时间并减少相关车辆排放。

通过创建一个在不确定性面前依然稳健的、可泛化的 AI 系统，我们希望把 AI 的问题求解能力进一步带入我们这个本质上难以预测的世界。

阅读[我们在《科学》上的论文](https://www.science.org/stoken/author-tokens/ST-887/full)，进一步了解 DeepNash。

对于有兴趣尝试 R-NaD 或与我们新提出的方法开展合作的研究者，我们已将[代码开源](https://github.com/deepmind/open_spiel/tree/master/open_spiel/python/algorithms/rnad)。

**论文作者**

Julien Perolat、Bart De Vylder、Daniel Hennes、Eugene Tarassov、Florian Strub、Vincent de Boer、Paul Muller、Jerome T Connor、Neil Burch、Thomas Anthony、Stephen McAleer、Romuald Elie、Sarah H Cen、Zhe Wang、Audrunas Gruslys、Aleksandra Malysheva、Mina Khan、Sherjil Ozair、Finbarr Timbers、Toby Pohlen、Tom Eccles、Mark Rowland、Marc Lanctot、Jean-Baptiste Lespiau、Bilal Piot、Shayegan Omidshafiei、Edward Lockhart、Laurent Sifre、Nathalie Beauguerlange、Remi Munos、David Silver、Satinder Singh、Demis Hassabis、Karl Tuyls。
