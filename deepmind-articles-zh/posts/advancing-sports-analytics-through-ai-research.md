---
title: "通过 AI 研究推进体育分析"
title_en: "Advancing sports analytics through AI research"
source: https://deepmind.google/blog/advancing-sports-analytics-through-ai-research/
site: deepmind
date: 2021-05-07
crawled: 2026-09-13
translated: 2026-09-13
---

# 通过 AI 研究推进体育分析

> 原文：[Advancing sports analytics through AI research](https://deepmind.google/blog/advancing-sports-analytics-through-ai-research/) · Google DeepMind

创建测试环境、帮助 AI 研究走出实验室进入现实世界是极具挑战性的事情。鉴于 AI 与游戏的深厚渊源，体育提供了令人兴奋的机会或许并不令人意外：它为研究者提供了一个试验场，AI 系统可以在其中协助人类，在一个由数十个动态、相互作用个体组成的多智能体环境中做出复杂的实时决策。

体育数据收集的快速增长意味着我们正处在一个对体育分析而言极其重要的时代。体育数据在数量和粒度上都在增长，正从汇总的高层统计与赛伯计量学（sabermetrics）时代，过渡到更精细的数据，例如事件流信息（如带标注的传球或射门）、高保真球员位置信息以及[穿戴式传感器](https://football-technology.fifa.com/en/media-tiles/epts-1/)。然而，体育分析领域直到最近才开始利用机器学习和 AI 来理解并辅助体育领域的人类决策者。在与利物浦足球俱乐部（Liverpool Football Club，LFC）合作发表于 JAIR 的[最新论文](https://www.jair.org/index.php/jair/article/view/12505)中，我们设想了结合统计学习、视频理解与博弈论的未来体育分析图景。我们特别阐明，足球是研究 AI 的一个有用缩影，从长远看，它能以自动视频助理教练（AVAC，automated video-assistant coach）系统（图 1(A)）的形式为体育决策者带来益处。

![两部分示意图（图 1）：A 部分展示一个自动视频助理教练（AVAC）系统在足球场上追踪带姿态与标签的进攻球员（绿色）和防守球员（蓝色）；B 部分为折线图，绘制信号值与目标事件检测值随时间的变化。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227a02399b20f5a694b481b_Fig201.svg)

图 1：(A) 设想中的自动视频助理教练界面示例，其中进攻与防守球员被检测、识别（对应球员姓名）、追踪，随后传入可用于分析潜在意图或规定轨迹的预测轨迹模型。(B) 事件检测的风格化示例，包含一个特定目标事件（例如射门/踢球）以及深度学习模型输出（「信号」）在全场比赛中的演化。

## 足球——AI 的一个有趣机会

与其他一些运动相比，足球在系统性收集大规模数据以进行旨在提升球队比赛水平的科学分析方面起步相当晚。原因有几方面，最突出的是与其他运动相比，比赛的可控设定要少得多（大型户外球场、动态的比赛等），此外职业足球界长期奉行主要依赖有实绩和经验的专家的信念。沿着这一话题，从未踢过职业足球的意大利成功足球教练兼经理人 Arrigo Sacchi，在 1987 年出任米兰教练时曾以一句[名言](https://www.fifa.com/news/they-said-arrigo-sacchi-1639785)回应对他缺乏经验的批评：「我从来不知道，要当骑师得先做一匹马。」

足球分析带来的挑战非常适合广泛的 AI 技术，它们来自三个领域的交汇：计算机视觉、统计学习和博弈论（见图 2 的可视化）。虽然这些领域各自对足球分析都有用，但它们结合时的益处尤其明显：球员需要在其他球员（合作与对抗）在场的情况下进行序贯决策，因此作为交互式决策理论的博弈论变得高度相关。此外，针对比赛中特定情境的战术解法可以基于比赛数据与特定球员表示来学习，这使统计学习成为高度相关的领域。最后，可以从广泛可得的视频输入中自动追踪球员并识别比赛场景。

![类维恩图：展示计算机视觉、统计学习与博弈论的交集，中心重叠区域代表一个包含"自动视频助理教练"的缩影。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227a11665e1f7f17789bd24_Fig202.svg)

图 2：三个关键领域（博弈论、统计学习和计算机视觉）的概览示意，它们在推进足球分析现状方面发挥了重要作用（每个相关领域列出了文献中的示例，并标出了相应的重叠前沿）。

我们设想的 AVAC 系统正位于这三个研究领域交集所形成的缩影之内（图 2）。在这一激动人心领域的研究中，我们不仅规划了一条可以持续多年攻克的科学与工程问题路线图，还在博弈论分析、统计学习和计算机视觉的交叉点上给出了新的原创结果，以说明这一激动人心的领域能为足球带来什么。

## AI 如何帮助足球

博弈论在体育研究中扮演重要角色，能为球员的行为策略提供理论基础。就足球而言，它的许多情境实际上可以建模为零和博弈，而零和博弈自博弈论诞生以来就被广泛研究。例如，我们把点球情境建模为一个双人非对称博弈，其中主罚者的策略可以整齐地归类为左、中、右三种射门。为研究这一问题，我们用[球员向量](https://ecmlpkdd2019.org/downloads/paper/701.pdf)（Player Vectors）增强点球情境的博弈论分析——球员向量概括了单个足球运动员的比赛风格。借助这种对单个球员的表示，我们能够把风格相近的主罚者分组，然后在组级别上进行博弈论分析（图 3）。我们的结果表明，不同组别被识别出的射门策略在统计上是有区别的。例如，我们发现其中一组偏好向球门左侧角射门，而另一组则更均匀地向左右两侧角射门。这类洞见或许能帮助守门员在面对不同类型的球员时多样化自己的防守策略。在这一博弈论视角的基础上，还可以通过把足球分析为时间延展的博弈来考虑它的持续性，据此为单个球员提供战术建议，甚至更进一步优化整支球队的战略。

![三部分示意图：展示球员向量与点球射门策略——(A) 3D 散点图将球员聚类为包括守门员和前锋在内的多个组；(B) 2D 散点图展示相同聚类并用具体球员标注，如 Ashley Westwood、Matthew Lowton、Callum Wilson 和 José Holebas；(C) 热图表示全部球员的总体平均射门分布，并分别为 Cluster-1、Cluster-2、Cluster-4 和 Cluster-5 单独展示。](https://lh3.googleusercontent.com/3Qy7u5JAEwXFehUsxSGoSsS7ksexx2Ed-xvKpLyAMs71cdXTwXVG1QqrquK8sJGCYCTwHmlc3FqO4LfaNISWqTf-__zxMmogkz8ol8BhkChYS0nzIg=w1440)

图 3：(A) 和 (B) 可视化了球员向量的聚类，球员数据来自一个包含超过 12,000 次点球的示例数据库。利用这种对球员行为的刻画，可以可视化各聚类中主罚者的进球热图，如 (C) 所示。

在统计学习方面，表示学习在体育分析中尚未被充分利用，而它能够对单个球员和球队的行为做出信息丰富的概括。此外，我们相信博弈论与统计学习之间的互动将进一步催化体育分析的进步。例如，在上述点球情境中，用球员特定统计量（球员向量）增强分析，为理解各类球员在点球情境中的行为或决策方式提供了更深入的洞见。另一个例子是研究「[幽灵化](https://authors.library.caltech.edu/75181/)」（ghosting），它指的是体育分析中一种特定的数据驱动分析，用事后视角研究球员本应如何行动（这与在线学习和博弈论中的后悔概念有关联）。幽灵化模型会为给定的一次进攻提出替代的球员轨迹，例如基于联赛平均水平或某支选定球队。预测轨迹通常以半透明层叠加在原始比赛之上显示，因此得名「幽灵化」（可视化示例见图 4）。生成式轨迹预测模型让我们能够通过分析比赛的关键情境以及它们本可能如何不同地展开来获得洞见。这些模型还有潜力用于预测战术调整、关键球员受伤或换人对本队表现的影响，以及对手对此类变化的反应。

![足球场俯视动画：展示幽灵化模型——随着真实足球（白色圆点）、进攻方（蓝色圆点）和防守方（红色圆点）移动，画面叠加了半透明黄色圆点，表示预测的防守球员轨迹。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227a14ad10a3334780dc13a_Fig204.gif)

图 4：使用足球追踪数据进行预测建模的示例。这里可视化了足球、进攻方和防守方的真实数据，以及一个序贯预测轨迹模型给出的防守球员预测。

最后，我们认为计算机视觉是推动最先进体育分析研究边界最有希望的途径之一。通过纯粹从视频检测事件——这是计算机视觉界已被充分研究的课题（例如参见这篇[综述](https://arxiv.org/pdf/1703.01170.pdf)以及我们论文中的更多参考文献）——其潜在应用范围极为广阔。将事件与特定帧关联后，视频变得可检索且更加有用（例如自动集锦生成成为可能）。反过来，足球视频也为计算机视觉提供了一个有趣的应用领域。数量庞大的足球视频满足了现代 AI 技术的一个前提条件。虽然每个足球视频都各不相同，但场景设置变化不大，这使该任务成为打磨 AI 算法的理想选择。还存在第三方供应商提供人工标注的事件数据，这类数据对训练视频模型有用但生成耗时，因此监督式与无监督算法都可以用于足球事件检测。例如，图 1(B) 提供了一个风格化的可视化：一个用监督方法训练、纯粹从视频识别目标事件（例如踢球/射门）的深度学习模型。

将先进 AI 技术应用于足球，有望在多个维度上革新这项运动，惠及球员、决策者、球迷和转播方。这类进步也很重要，因为它们有潜力进一步推动这项运动本身的民主化（例如，不必依赖现场球探/专家的主观判断，而可以使用计算机视觉等技术来量化来自代表性不足地区或低级别联赛球员的技术能力）。我们相信，足球这一缩影所促成的日益先进的 AI 技术的发展，可能适用于更广泛的领域。为此，我们（与多位外部组织者一起）正在共同组织今年晚些时候的 [IJCAI 2021 体育分析 AI 研讨会](https://sites.google.com/view/ijcai-aisa-2021/)，欢迎有兴趣的研究者参加。对该主题感兴趣的研究者，可以使用分析公司（如 StatsBomb）和更广泛的研究社区公开提供的数据集（[数据集链接](https://github.com/statsbomb/open-data)、[数据集链接](https://soccer-net.org/)）。此外，本文对该领域的研究提供了全面的综述。

论文及相关链接：

- [JAIR 论文](https://www.jair.org/index.php/jair/article/view/12505)
- [IJCAI 2021 体育分析 AI 线上研讨会](https://sites.google.com/view/ijcai-aisa-2021/)

**注释**

本工作由以下贡献者合作完成：Karl Tuyls、Shayegan Omidshafiei、Paul Muller、Zhe Wang、Jerome Connor、Daniel Hennes、Ian Graham、William Spearman、Tim Waskett、Dafydd Steele、Pauline Luc、Adria Recasens、Alexandre Galashov、Gregory Thornton、Romuald Elie、Pablo Sprechmann、Pol Moreno、Kris Cao、Marta Garnelo、Praneet Dutta、Michal Valko、Nicolas Heess、Alex Bridgland、Julien Perolat、Bart De Vylder、Ali Eslami、Mark Rowland、Andrew Jaegle、Yi Yang、Remi Munos、Trevor Back、Razia Ahamed、Simon Bouton、Nathalie Beauguerlange、Jackson Broshear、Thore Graepel 和 Demis Hassabis。
