---
title: "开源 Psychlab"
title_en: "Open-sourcing Psychlab"
source: https://deepmind.google/blog/open-sourcing-psychlab/
site: deepmind
date: 2018-01-26
crawled: 2026-09-13
translated: 2026-09-13
---

# 开源 Psychlab

> 原文：[Open-sourcing Psychlab](https://deepmind.google/blog/open-sourcing-psychlab/) · Google DeepMind

想一想去超市采购食品这样一件简单的事。如果你没能买下购物清单上的一件商品，这能告诉我们关于你大脑运作的什么信息呢？这可能说明你在搜寻清单上的商品时，难以把注意力从一个物体转移到另一个物体上；也可能说明你在记住购物清单方面存在困难；又或者，问题可能出在同时执行这两项技能上。

![漫画插图：摆满五颜六色食品和价格标签的超市货架。](https://lh3.googleusercontent.com/OUNT_RkjJtzrsGCubJebiNItSX1f2_84kmW_ld9xWGAPVCbmbmpziQ72mIm2N9kOpHYoocnuGAntJzY-JHdigwSwRKkQDuhDb9EW2PkDgpqI17Pfcg=w1440)

看似单一的任务，实际上依赖于多种认知能力。我们在 AI 研究中也面临类似的问题：任务的复杂性往往让人难以把一个智能体（agent）取得成功所需的各项技能逐一拆分开来。但理解智能体所具备的具体认知技能组合，或许有助于提升它的整体表现。

为了解决人类身上的这一问题，心理学家在过去 150 年里设计了大量严格受控的实验，旨在每一次只隔离出一种特定的认知官能。例如，他们可以用两个彼此独立的测试来分析超市场景——一项「视觉搜索」测试要求被试在一组图案中找出特定形状，可以用来探测注意力；而让一个人回忆此前学习过的清单中的条目，则可以测试其记忆。

我们相信，可以运用类似的实验方法来更好地理解人工智能体的行为。这正是我们开发 Psychlab 的原因。Psychlab 是构建在 [DeepMind Lab](https://deepmind.com/blog/article/open-sourcing-deepmind-lab) 之上的一个平台，使我们能够直接应用认知心理学等领域的方法，在受控环境中研究人工智能体的行为。今天，我们也将开放这个平台的源代码，供他人使用。

Psychlab 在虚拟的 DeepMind Lab 环境中再现了人类心理学实验通常采用的设置。后者的典型形式是：一名被试坐在电脑显示器前，用鼠标对屏幕上的任务作出反应。类似地，我们的环境允许一个虚拟被试在虚拟的电脑显示器上执行任务，并用其注视方向来作出反应。这样一来，人类和人工智能体就可以参加完全相同的测试，最大限度地减少实验差异。这也让研究者更容易与认知心理学领域的既有文献建立联系并从中汲取洞见。

伴随着 Psychlab 的开源发布，我们还构建了一系列可在虚拟电脑显示器上运行的经典实验任务，并提供了灵活易学的 API，让其他人能够构建自己的任务。

- [视觉搜索（Visual search）](https://youtu.be/54AS3a6niPo)——测试在一系列条目中搜寻目标的能力。
- [持续识别（Continuous recognition）](https://youtu.be/rPlARM2KCuM)——测试对不断增长的条目清单的记忆。
- [任意视觉运动映射（Arbitrary visuomotor mapping）](https://youtu.be/385WgV-7fbw)——测试对刺激-反应配对的回忆。
- [变化检测（Change detection）](https://youtu.be/p10hRvFquqU)——测试检测在一组经过延迟后重新出现的对象中的变化的能力。
- [视觉敏锐度与对比敏感度（Visual acuity and contrast sensitivity）](https://youtu.be/m194hJJWwZE)——测试识别小尺寸、低对比度刺激的能力。
- [Glass 图案检测（Glass pattern detection）](https://youtu.be/KG0pO3U_EH8)——测试整体形状知觉。
- [随机点运动辨别（Random dot motion discrimination）](https://youtu.be/HuNMXq-AjjE)——测试感知连贯运动的能力。
- [多目标追踪（Multiple object tracking）](https://youtu.be/G4X5yeGCcyM)——测试随时间推移追踪运动对象的能力。

这些任务中的每一项都经过了验证，结果表明我们的人类实验结果与认知心理学文献中的标准结果相吻合。

以「视觉搜索」任务为例。在一组复杂刺激中定位某个物体——比如超市货架上的某件商品——的能力，一直被当作理解人类选择性注意的一种研究途径。

当人类执行「在一堆水平方向的条形中找出一条垂直方向的条形」和「在其他颜色的条形中找出一条粉色条形」的搜索任务时，他们的反应时间不会随屏幕上条目数量的变化而变化。换句话说，他们的反应时间与「集合大小（set size）」无关。然而，当任务是在形状不同、颜色也各异的条形中找出一条粉色条形时，每增加一条条形，人类的反应时间就会增加约 50 毫秒。当人类在 Psychlab 上执行这一任务时，我们复现了这一结果。

![三幅图表和折线图，对比人类（红色）与人工智能体（蓝色）在三项视觉搜索任务——「方向搜索」「颜色搜索」和「联合搜索」——中的反应时间。人工智能体在所有集合大小下反应时间保持平稳；人类在方向搜索和颜色搜索中反应时间保持平稳，但在联合搜索中随集合大小增加而上升。](https://lh3.googleusercontent.com/1AN2JnR2iRFdcICpdi1HUf6BLZp62cgkymf5zncus9KEdVjwuC2nKwpGHenAxt3rxRmhrivsIJQnPTzWOcr4LM40zpgdbrobfDHwGM-SOusagAyidg=w1440)

当我们用一个最先进的人工智能体执行同样的测试时，我们发现它虽然能够完成该任务，却没有表现出人类那种反应时间结果的模式。它在全部三种情形下都用了同样的时间来作出反应。在人类身上，这类数据曾揭示了[平行注意与串行注意](http://search.bwh.harvard.edu/new/pubs/FiveFactors_Wolfe-Horowitz_2017.pdf)之间的差别。而智能体似乎只拥有平行的机制。找出人类与我们当前人工智能体之间的这一差异，为改进未来的智能体设计指明了一条路径。

Psychlab 的设计初衷是作为连接认知心理学、神经科学与 AI 的桥梁工具。通过开源，我们希望更广泛的研究界能在自己的研究中使用它，并与我们一道塑造它的未来。

**说明**

[阅读论文](https://arxiv.org/abs/1801.08116)。

[在 GitHub 上下载代码](https://github.com/deepmind/lab/tree/master/game_scripts/levels/contributed/psychlab)。
