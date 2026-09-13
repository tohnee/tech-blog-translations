---
title: "用新技术和旧书籍对抗疾病"
title_en: "Using new technology and old books to combat disease"
source: https://blog.google/innovation-and-ai/technology/research/using-new-technology-and-old-books-to-combat-disease/
site: google-blog
date: 2022-12-12
crawled: 2026-09-13
translated: 2026-09-13
---

# 用新技术和旧书籍对抗疾病

> 原文：[Using new technology and old books to combat disease](https://blog.google/innovation-and-ai/technology/research/using-new-technology-and-old-books-to-combat-disease/) · Google

每年有数亿人受到虫媒疾病的影响，而气候变化只会让问题变得更糟。气温和降雨的增加扩大了包括蜱虫和蚊子在内的昆虫的活动范围，助长了登革热、莱姆病和疟疾等疾病的暴发。

人类可以在哪里找到应对这些最新挑战的答案？一个想法：旧书籍。

Google Brain 的一个团队正在使用 Google Books 挖掘出的几十年前的数据集，加上一张新开发的气味感官图谱，来对抗这一重大全球健康问题。这之所以成为可能，是因为该团队最近发现，蚊子的嗅觉与人类的并没有太大不同。

前 Google Brain 研究员、现任 Google Ventures 驻企创业家（Entrepreneur in Residence）的 Alex Wiltschko 解释说："我的团队专注于赋予计算机嗅觉。在我们审查为预测分子对人而言闻起来是什么味道而训练的神经网络的预测结果时，我们发现这些网络也可以用来预测昆虫大脑中的'嗅觉部分'如何对相同的分子作出反应。"

蚊子之类的昆虫利用嗅觉来定位食物——植物中含糖的花蜜，而对于许多物种的产卵雌虫来说，还有血液中的一种蛋白质。化学驱避剂的作用是干扰这些昆虫的嗅觉信号，使它们无法专注于叮咬可能的受害者，从而防止致病病原体的传播。Google Brain 团队意识到，如果他们能训练计算机识别驱蚊的气味，这些计算机就能帮助预测安全、廉价且有效的驱避剂，从源头上遏制虫媒疾病。

当然，要训练模型，他们需要数据。

团队找到了美国农业部（USDA）在二战期间完成的相关研究。"我们了解到一个数据集，他们在其中测试了数千种驱避剂——比我们手头的 20 种多得多，"Alex 说。但这些 USDA 数据记录在笔记本和文件柜中，有些没有编入索引，而且全都太难找到、也难以与 Google Brain 团队共享。幸运的是，USDA 的研究已被 Google 的另一个团队——Google Books——扫描并编入索引。USDA 提供了搜索关键词，帮助 Google Brain 团队在 Google Books 语料库的 4000 多万卷图书中找到了这批缺失的数据集。

在 Google Books 中发现的一个庞大却被遗忘的驱虫剂数据集，其中记录了 20 世纪 40 年代末对 DEET（避蚊胺）的首次测试。

![20 世纪 40 年代一项研究的一页](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/oldbook.width-1200.format-webp.webp)

这是一个好的开始。但当 Google Books 技术馆藏专家 Kurt Groetsch 听说这第一个数据集时，他知道还能找到更多。一次全面检索找出了 100 多个大小不一的数据集——这些数据集早已被 USDA 和其他所有人遗忘。"科学家们为这些研究项目做过严格的测试。这些科学信息记录得非常完善，以印刷形式静静存放在那里几十年——它的存在却在时间中湮没，"Google Books 图书馆合作高级经理 Ben Bunnell 说。"现在我们可以使用 40 年代还不存在的工具，利用他们的研究推演出今天可能挽救生命的信息。"

将涂抹了驱避剂的手臂伸入装有埃及伊蚊的笼子中。

![一名男子把手臂伸进一个装满虫子的封闭箱子里。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/oldimage.width-1200.format-webp.webp)

在比尔及梅琳达·盖茨基金会的支持下，手握所需全部数据的 Google Brain 团队联系了 TropIQ——一家测试对抗虫媒传染病分子的机构——以验证这些数据是否可用。"我们想看到的是，1942 年的好驱避剂如今依然是好驱避剂——而结果恰恰如此，"Alex 说。

在确认了 USDA 数据的质量后，[团队得以训练一个神经网络](https://www.biorxiv.org/content/10.1101/2022.09.01.504601v2)来预测哪些分子可以作为有效的驱虫剂。他们把目前已在用作化学驱避剂的分子从名单上划掉，然后让 TropIQ 测试其余的分子：那些已被确认为有效但目前尚未投入使用的分子。在其中，TropIQ 的测试发现了 10 种驱避效果高于 DEET 的分子。Google Brain 团队目前正在就成本、安全性和可得性对这些分子进行研究，为一批有助于对抗疾病的新型驱虫剂铺平道路。。

此外，Google Brain 与 Google Books 的合作还揭示了一个尚未被发掘、等待进一步研究的庞大数据集来源。"这个项目开启了提取更多此类数据进行机器学习分析的机会——不仅是化学领域的，还有环境、天文、地质……名单还在继续，"Ben 说。"Google Books 中有太多信息等待被发现，还有太多书籍尚未被扫描——这个项目只是一个很长故事的第一页。"团队的希望是，通过使用 Google Books 发掘其中蕴藏的一切，我们能找到应对人们日常所面临的一些挑战的答案。
