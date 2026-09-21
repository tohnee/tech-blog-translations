---
title: "Jev 与泛化"
title_en: "Jev and Generalization"
source: https://sebastianraschka.com/blog/2026/jev-classification-generalization.html
crawled: 2026-09-21
translated: 2026-09-21
---

# Jev 与泛化

> 原文：[Jev and Generalization](https://sebastianraschka.com/blog/2026/jev-classification-generalization.html) · Sebastian Raschka's Blog

吹捧 [Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) 和贬低它都很容易。过去几天我看到了很多有趣的演示，也读到了很多不屑一顾的评论。我认为真相介于这两个极端之间。

比如说，把 Jev 轻描淡写为「不过是个分类器」是很容易的。

它的具体模型与训练算法并未公开。但如果让我做一个有根据的猜测，它很可能是：

1. 一个类似 [(Modern)BERT](https://arxiv.org/abs/2412.13663) 的小型编码器风格模型；
2. 用类似「校准奖励强化学习」（Reinforcement Learning with Calibration Reward，出自 [Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty](https://arxiv.org/abs/2507.16806) 论文）的方法训练的。

很多人（包括我在内）多年来一直在训练编码器风格的分类模型。事实是，它们通常都是专用模型，在某些方面存在局限。

Jev 令人印象深刻的突破在于它的泛化能力如此之强（你可以用它分类邮件、玩电子游戏、交易股票……）。

而且我想说，秘诀可能更多在数据而非训练算法。（再加上一个设计精良的 API。）

是的，这并不是第一个有人把 RL 应用于（很可能）非自回归的编码器风格模型的项目。

但了不起之处在于它确实有效且泛化得如此之好——这能带来质的差别。也就是说，不久前我们在 Stable Diffusion（基于一篇[已有的研究论文](https://arxiv.org/abs/2112.10752)）上看到过同样的情形，甚至 2022 年 ChatGPT 本身的发布也是如此（它是 [InstructGPT](https://arxiv.org/abs/2203.02155) 的改进版，而数据才是决定性差异）。

[![Jev API 在 Choice 和 Noul 上的示例，请求输入与带标注的输出展示了所选选项、置信度、概率与 token 用量](https://sebastianraschka.com/images/blog/2026/jev-classification-generalization/jev.webp)](https://sebastianraschka.com/images/blog/2026/jev-classification-generalization/jev.png)

Jev API 在 Choice 和 Noul 上的示例。点击图片查看全分辨率版本。

来源：我的 [LinkedIn 帖子](https://www.linkedin.com/posts/sebastianraschka_its-easy-to-hype-and-dunk-on-jev-i-saw-activity-7507457962425110529-Z_KJ)的网站版。
