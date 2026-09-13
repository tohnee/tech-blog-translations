---
title: "用 AI 攻克早发性帕金森病"
title_en: "Targeting early-onset Parkinson’s with AI"
source: https://deepmind.google/blog/targeting-early-onset-parkinsons-with-ai/
site: deepmind
date: 2022-09-21
crawled: 2026-09-13
translated: 2026-09-13
---

# 用 AI 攻克早发性帕金森病

> 原文：[Targeting early-onset Parkinson’s with AI](https://deepmind.google/blog/targeting-early-onset-parkinsons-with-ai/) · Google DeepMind

AlphaFold 的预测正在为能够影响全球超过 1000 万人的新疗法铺平道路

这是一场仿佛常常逆坡而行的苦战之后来之不易的满足感。David Komander 和他的同事们终于发表了人们期待已久的 PINK1 结构。编码这种蛋白质的基因发生突变会导致早发性帕金森病——一种症状广泛且不断进展的神经退行性疾病，尤其表现为身体震颤和行动困难。但当其他科学团队发表了他们针对同一蛋白质的结构时，事情变得明显不对劲了。

「另外两个发表出来的结构与我们小组做出的结构看起来非常不同，」Zhong Yan Gan 说。他是 [Komander 实验室](https://www.wehi.edu.au/people/david-komander)的博士生，在澳大利亚墨尔本 WEHI（沃尔特与伊丽莎·霍尔医学研究所，Walter and Eliza Hall Institute of Medical Research）同时受副教授 Grant Dewson 的联合指导。他们的结构成了那个「异类」，带有其他结构中似乎并不存在的独特特征。这件事利害攸关：理解 PINK1 有助于解锁针对帕金森病根本病因的新疗法，而帕金森病[影响全球超过 1000 万人](https://www.parkinson.org/understanding-parkinsons/statistics)。

虽然 Komander 的团队对自己的研究结果有信心，但这些相互矛盾的结果引出了一些重大疑问。而且在这个竞争激烈的研究领域，他们知道追寻答案的绝非自己一家。「这些不仅是极难啃的硬骨头，而且一旦被啃下来，你突然就打开了整个领域，所有人都在做非常相似的事情，」Komander 说。

![实验室里的一位女性科学家和一位男性科学家。](https://lh3.googleusercontent.com/rt-Hf8fOFHDki2h0US5p00_wuAUXrJTq1KP-II-ZQvwjJOn2BEf7f4c3DJVySHLDgIToSaXsjeP3GdCUeqQV7S4JS3BCQR6c7u2OF1sqtDrn9M7QgDw=w1440)

图片来源：Jacinta Moore

团队最终解开了这个谜团，但这又花去了数年的研究、一次偶然的发现，以及 DeepMind 蛋白质结构预测系统 AlphaFold 的鼎力相助。

当一个人的大脑再也无法制造足够的多巴胺这种化学物质时，[帕金森病的症状](https://www.parkinsons.org.uk/information-and-support/what-parkinsons)就会出现。大多数帕金森病患者并不知道确切病因，但大约 10% 的患者可以追溯到[某个特定的基因突变](https://www.michaeljfox.org/news/parkinsons-genetics)。在这类病例中，帕金森病往往发病较早，在患者[年满 50 岁之前](https://www.michaeljfox.org/news/young-onset-parkinsons-disease)就已产生影响。

其中一个基因突变位于编码 [PINK1](https://en.wikipedia.org/wiki/PINK1) 蛋白质的基因中。PINK1 在线粒体（常被称为细胞内的「发电厂」）的分解与清除过程中发挥着关键作用。「随着年龄增长，线粒体会变得衰老和受损，」Gan 说。「PINK1 是身体回收旧线粒体、为新线粒体腾出位置的机制的一部分。」

当这一机制失灵时，受损的线粒体会不断累积，导致产生多巴胺的神经细胞死亡，最终引发帕金森病。因此，寻找更好疗法的一条途径，就是更好地[理解 PINK1 及其作用](https://molecularneurodegeneration.biomedcentral.com/articles/10.1186/s13024-020-00367-7)。

![两位科学家在实验室中进行一项看起来复杂的任务。他们被设备包围着。](https://lh3.googleusercontent.com/QkUaGq3uaj64nyePQgTltbvUgdbdwD6OOani-SD6TzjRggwEk2v3xc-U2htPJlpIk-MiQcg3XBzbGpeyCS19IZL2beNO9Jx7HFQs-C3Jm-3WAzW2Nzs=w1440)

图片来源：Jacinta Moore

2004 年，当研究人员发现 [PINK1 可能导致帕金森病](https://www.science.org/doi/10.1126/science.1096284)时，确定它的结构就成了一个关键目标——但这一目标迟迟未能实现，部分原因在于人类 PINK1 太不稳定，难以在实验室中生产。科学家们被迫把网撒得更宽，他们发现昆虫版本的 PINK1——例如来自人体虱的版本——足够稳定，可以在实验室中生产并研究。

这就把我们带回了故事的开头。Komander 的团队于 2017 年发表了他们的 [PINK1 结构](https://www.nature.com/articles/nature24645)。但当其他研究人员发表了来自另一种昆虫（面粉甲虫）的同一蛋白质的不同结构时，他们明白自己掌握的只是故事的一部分。这并不完全令人意外。毕竟，蛋白质是动态的分子。「它们就像机器，可以呈现不同的形状，」Gan 说。如果已发表的结构只是其中一种形状——只是 PINK1 在一个更长过程中的某个单一阶段的快照呢？

> 我们拿到了这些新结构，而在当时，我们是这个星球上唯一知道 PINK1 在激活过程中长什么样的人

David Komander

生物化学家

Gan 把弄清 PINK1 在激活过程的每一步中是什么样子作为自己博士课题中一项雄心勃勃的任务。正是在这项工作中，他发现了一个奇怪的东西：一个看起来远大于他的目标的分子。「通常你会把它当作一团凝聚在一起的东西而弃之不顾，就像一团炒鸡蛋似的东西，」Komander 说。

但 Gan 有一种直觉，认为这一团块值得深入研究，于是在 Alisa Glukhova 博士的帮助下，决定使用[冷冻电子显微镜](https://www.chemistryworld.com/news/explainer-what-is-cryo-electron-microscopy/3008091.article)（cryo-EM）在原子尺度上探测这个分子——即用电子束检查冷冻样品。「我记得对 Zhong 说：『行，你可以试试，但这绝不会成功』，」Komander 承认。

Gan 的坚持得到了丰厚的回报。他发现的正是研究人员要找的那个分子：PINK1。但它为什么这么大？原来 PINK1 喜欢结伴。它并非单个蛋白质，而是成对聚在一起，形成被称为二聚体（dimer）的分子对，这些二聚体又排列成更大的构造。「六个 PINK1 二聚体组装成了巨大的、百吉饼状的环状结构，」Gan 说。

![一张 David Komander 办公室内的照片。我们从走廊透过玻璃看进去。有两个人站在 Komander 身后，看着他正在电脑上做的工作。](https://lh3.googleusercontent.com/pG_bDFJQqMT0yr9sQPV4usbcyQJx5sCWaf3wInbDMgS8OyLYgyXtiMo2h2s3oYU1YfY0OQdvXmaHowDCpInLLq2KgxigfguOJ0ZZdoYxA_S1qrVndpk=w1440)

图片来源：Jacinta Moore

这次偶然的发现意味着他可以使用冷冻电子显微镜来解析这种蛋白质的物理结构——而这对单个 PINK1 那样小的分子是行不通的。团队得到了答案。

此前发表的 PINK1 结构并非错误——它们是该蛋白质在激活过程不同阶段呈现的不同形态。但有一个问题。所有这些实验工作都是使用来自昆虫的 PINK1 完成的。要理解他们的发现对人类帕金森病患者的意义，他们必须研究这些发现是否同样适用于人类版本的蛋白质。

Komander 和他的团队转向了 AlphaFold。「我们拿到了这些新结构，而在当时，我们是这个星球上唯一知道 PINK1 在激活过程中长什么样的人，」Komander 说。于是他们用 AlphaFold 调出它对[人类来源的 PINK1](https://alphafold.ebi.ac.uk/entry/Q9BXM7) 结构的预测，片刻之后结果就出现在屏幕上。他说，AlphaFold 预测的准确程度「完全令人震惊」。

后来，当 Gan 把两条蛋白质序列输入 AlphaFold 来预测人类 PINK1 二聚体的结构时，结果与他用昆虫蛋白质所做的实验工作几乎无法区分。「那个二聚体基本上精确展示了这两个蛋白质如何相互作用，从而使它们能够协同行动、共同形成我们所见过的某些复合物，」Komander 说。

> 我们可以开始思考：「我们需要开发什么样的药物来修复这个蛋白质，而不只是接受它坏掉了这个事实」

David Komander

多项实验结果与 AlphaFold 预测结构之间的高度吻合，让团队确信这个 AI 系统能够在他们的实证工作之外提供有意义的洞见。他们随后使用 AlphaFold 建模，探究某些突变会对二聚体的形成产生什么影响——以研究这些突变如何可能导致帕金森病——而他们的猜测得到了证实。

「我们能够立即为携带这些特定突变的患者生成一些真正的洞见，」Komander 说。这些洞见最终可能带来新的疗法。「我们可以开始思考：『我们需要开发什么样的药物来修复这个蛋白质，而不只是接受它坏掉了这个事实』，」Komander 说。

他们于 2021 年 8 月将关于 [PINK1 激活机制](https://www.nature.com/articles/s41586-021-04340-2)的研究结果提交给《自然》（Nature）杂志，论文于 2021 年 12 月上旬被接收。事实证明，加拿大蒙特利尔 Trempe 实验室的研究人员也得出了类似的结论，当那个团队的论文于 2021 年 12 月发表时，WEHI 的作者们不得不加速完成最后的修改。「我们被告知要在圣诞节前三天完成论文，以便它能在 2021 年内发表，」Komander 说。「那是一段残酷的时间表。」

![David Komander 在电脑屏幕上向同事们展示工作。他看起来对这项工作非常满意。](https://lh3.googleusercontent.com/d1ev982yS5u65xrJ2MZZ3dsIbr1NXk4dhYQH24Fuj_qw70P5J7vYz0C9YWeTDHI3ktNQ8DxfQBNpY66xWNMB5xvjpT_99L9Gey0MjGFyIUB_EeBk=w1440)

图片来源：Jacinta Moore

最终，这些[备受瞩目的论文](https://www.nature.com/articles/s41594-022-00733-7)在几周之内相继问世，都为理解帕金森病的分子基础做出了重要贡献。

当然，该领域的研究人员仍有很多问题待解，而 AlphaFold 是免费开放的，可以帮助他们找到部分答案。例如，Komander 实验室的高级博士后研究员 Sylvie Callegari 就使用 AlphaFold，通过拼接较小的蛋白质片段，找到了一种已知会导致帕金森病的大蛋白质 VPS13C 的结构。

「现在，我们可以开始提出不同的问题了，」她说。「我们可以不再问『它长什么样？』，而是开始问『它是如何工作的？』『这个蛋白质的突变如何导致疾病？』」

AlphaFold 的众多目标之一是加速医学研究，在 WEHI，它也被应用于早发性阿尔茨海默病患者的基因序列，让研究人员能够调查个别病例的病因。「AlphaFold 让我们能够基于出色而正确的人类模型来做这些，」Komander 说。「这非常强大。」
