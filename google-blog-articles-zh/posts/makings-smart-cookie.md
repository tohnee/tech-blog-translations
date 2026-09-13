---
title: "一块“聪明饼干”是怎样炼成的"
title_en: "The makings of a smart cookie"
source: https://blog.google/innovation-and-ai/technology/research/makings-smart-cookie/
site: google-blog
date: 2017-12-04
crawled: 2026-09-13
translated: 2026-09-13
---

# 一块“聪明饼干”是怎样炼成的

> 原文：[The makings of a smart cookie](https://blog.google/innovation-and-ai/technology/research/makings-smart-cookie/) · Google

假日季节正酣，你大概已经把手伸进饼干罐了。你或许有一份久经考验、心头最爱的节日饼干配方，但今年我们决定给季节性烘焙换换花样，加入两种新配料：匹兹堡的一家本地烘焙坊，以及我们的 [Google AI](https://ai.google/) 技术。

过去一年，Google 的一个小型研究团队一直在试验一种用于实验设计的新技术。为了展示这项技术能做什么，团队提出了一个现实世界的挑战：用给定的一组原料，设计出尽可能美味的巧克力奇普饼干。让这个项目更添趣味的是，我们团队就在 Google 匹兹堡办公室工作，那里曾是一座老的 Nabisco 饼干工厂。

借助一种名为“[贝叶斯优化](https://cloud.google.com/blog/big-data/2017/08/hyperparameter-tuning-in-cloud-machine-learning-engine-using-bayesian-optimization)（Bayesian Optimization）”的技术，团队暂时离开电脑，在厨房里撸起了袖子。首先，我们设定了一堆（比喻意义上的）旋钮——在这里就是饼干配方中的各种原料，比如巧克力的种类，糖、面粉、香草等的用量。这些原料提供了足够多可操控、可测量的独特变量，而且配方易于复制。我们的系统猜出了第一个要试做的配方。我们把它烤了出来，我们热切的试吃员——那些愿意为了科学而吃饼干的 Googlers——品尝之后参照市售饼干样品给它打出了数字评分。我们把评分反馈给系统，系统从评分中学习并调整那些“旋钮”，生成新配方。如此往复数十次——烘烤、评分、再把结果喂回去生成新配方——很快，系统在创造美味配方这件事上就进步了一大截。

在 Google 内部琢磨出一个相当不错的配方之后，我们想看看专家能拿我们的“聪明饼干”做出什么。于是，办公室教学厨房的主厨 John 把团队介绍给了 [Gluten Free Goat Bakery & Cafe](http://glutenfreegoat.com/) 的 Jeanette Harris。Jeanette 十多年前被诊断出[乳糜泻](https://g.co/kgs/RTaAzs)（Celiac），她把对烘焙的热爱变成了一个机会，为那些通常无法享用甜点的人提供美食。“当 John 带着制作 AI 生成饼干的点子来找我时，我不知道该期待什么，”Jeanette 说。“我经营着一家小型本地烘焙坊，非常注意确保为顾客提供安全、优质的原料。但当团队花时间解释了他们想做的是什么之后，我就完全投入了！”

在 Goat Bakery 的厨房里，John 主厨和 Jeanette 按照 Google 系统提供的用量，混搭了一些不寻常的原料，比如豆蔻和花椒。两个月、59 个试制批次之后，这对烘焙搭档推出了经典巧克力奇普饼干的新变体：巧克力奇普豆蔻饼干。

![“聪明饼干”配方](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Smart_Cooke_Recipe.width-1200.format-webp.webp)

“这是一次多么有趣的实验！在 AI 的帮助下创造出全新而独特的东西，令人兴奋不已，也让我不禁思考，还能为顾客开发出哪些别出心裁的配方创意，”Jeanette 说。

![SmartCookie_1.jpg](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/SmartCookie_1.width-100.format-webp.webp)

Jeanette Harris、John Karbowski、Daniel Golovin 和 Greg Kochanski 在 Gluten Free Goat Bakery 展示巧克力奇普豆蔻“聪明饼干”。

![SmartCookie_2.jpg](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/SmartCookie_2.width-100.format-webp.webp)

左图：Jeanette Harris 进行现场烹饪演示。

![SmartCookie_3.jpg](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/SmartCookie_3.width-100.format-webp.webp)

John Karbowski、Jeanette Harris 和 Daniel Golovin 品尝美味点心。

![SmartCookie_4.jpg](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/SmartCookie_4.width-100.format-webp.webp)

Gluten Free Goat Bakery 的演示台。

“聪明饼干”实验让我们浅尝了 AI 的种种可能。我们希望它能让你思考：用 AI，你还能“烤”出些什么。
