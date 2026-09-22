---
title: "Grok 4"
title_en: "Grok 4"
date: 2025-07-11
source: https://x.ai/news/grok-4
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok 4

> 原文：[Grok 4](https://x.ai/news/grok-4) · xAI

2025 年 7 月 9 日

Grok 4 是世界上最智能的模型。它包含原生工具使用和实时搜索集成，现已在 SuperGrok 和 Premium+ 订阅用户中可用，并可通过 xAI API 使用。我们同时推出新的 SuperGrok Heavy 档位，提供 Grok 4 Heavy——Grok 4 最强大的版本。

[试用 SuperGrok](https://grok.com/plans)[访问 API](https://docs.x.ai/)

## [扩展强化学习](#scaling-up-reinforcement-learning)

在 Grok 3 上，我们把下一 token 预测预训练扩展到前所未有的水平，得到了一个世界知识和性能无出其右的模型。我们还推出了 Grok 3 Reasoning，它通过强化学习训练，能对问题思考更久并以更高的准确率求解。在 Grok 3 Reasoning 的工作中，我们注意到的扩展规律表明，把强化学习训练大幅扩展是可行的。

对于 Grok 4，我们利用 Colossus 超算集群——我们的 200k GPU 集群——以预训练规模运行强化学习，打磨 Grok 的推理能力。这得益于整个技术栈的创新：从把训练计算效率提升 6 倍的新基础设施和算法工作，到大规模的数据采集工作——我们把可验证训练数据从主要是数学和编码数据显著扩展到更多领域。最终的训练运行在比此前高出一个数量级以上的算力上平稳地取得了性能增益。

### Humanity's Last Exam

处于人类知识前沿的深度专家级基准

### 最先进水平

完整题集（2025 年 4 月 3 日），配备 python 和搜索工具

### 训练过程中的性能

纯文本子集，配备 python 和搜索工具

Pass@1 准确率(%)

60

算力

无工具

有工具

测试时算力

## [原生工具使用](#native-tool-use)

Grok 4 经过强化学习训练来使用工具。这让 Grok 能够在大语言模型通常棘手的场景中，用代码解释器和网页浏览等工具增强自己的思考。在搜索实时信息或提出困难的研究问题时，Grok 4 会自行选择搜索查询，从整个网络中寻找知识，并按需要深入挖掘，以打磨出高质量的回答。

我们还训练 Grok 使用强大的工具从 X 深处寻找信息。Grok 可以使用高级关键词和语义搜索工具，甚至查看媒体来提升回答质量。

X 搜索网页搜索研究

我记得前几天有个很火的帖子，讲的是一个疯狂的文字谜题，好像跟「腿」有关。能帮我找到它吗？

显示完整轨迹

思考了 1 分钟

调查谜题帖子

- 这个请求要找的是 2025 年 7 月上旬一个关于与腿有关的疯狂文字谜题的热门帖子。
- 让我们试着搜索 2025 年 7 月 1 日至 9 日的相关 X 帖子。
- 也许搜索「viral word puzzle about legs」能帮助找到最近的帖子。

搜索 viral word puzzle about legs

iquantified

skeletonNaughty

AZ_NYsles

LegsEmporium

+2 个其他来源

搜索 (word puzzle) legs min_faves:100 since:2025-07-01 until:2025-07-09 filter:has_engagement

- 搜索到的帖子显示有一个谜题，关于以腿部部位的同音词结尾的单词，比如 toe、calf、knee、shin。
- 许多帖子提到「toe, calf, knee, shin」是 Connections 第 756 期谜题中的紫色类别。

探索谜题细节

- 2025 年 7 月 7-8 日前后的帖子表明，那个病毒式传播的帖子是关于 NYT Connections 谜题中荒诞的类别。
- 让我们搜索「NYT Connections puzzle #756 answers」。

搜索 NYT Connections puzzle #756 answers

nytimes.com

mashable.com

cnet.com

gamersant.com

+1 个其他来源

- 2025 年 7 月 6 日的第 756 期谜题中，紫色类别是以腿部部位同音词结尾的单词。
- 「疯狂」之处在于那种牵强的联想，比如在某些口音里「shun」听起来像「shin」。

搜索 connections (toe calf knee shin) since:2025-07-06 until:2025-07-09 min_faves:100

zaqtff

搜索 nyt connections crazy leg puzzle homophones

DreamWeaver5166

iquantified

VKlker

Silvanarsj

+2 个其他来源

- 一个有 660 个赞的帖子提到「toe calf knee shin they're homophones」，可能就是那个热门帖子。
- 现在，让我们在 X 上搜索 2025 年 7 月 6 日至 9 日包含「homophones」和「parts of the leg」、且至少 100 个赞的帖子。

搜索 homophones "parts of the leg" since:2025-07-06 until:2025-07-09 min_faves:100

ThaTurnerIV

搜索 connections legs OR leg since:2025-07-06 until:2025-07-09 min_faves:500

IsOutOf0

分析搜索结果

- 新的搜索发现了一条有 5052 个赞的回复帖，引用了一个关于该谜题荒谬之处的梗图。
- 另一次搜索发现一个有 89123 个赞的帖子，很可能就是那个病毒式帖子，引用了对该谜题的抱怨。

根据你的描述，你说的应该是 2025 年 7 月 7 日一条病毒式传播的 X 帖子，它抱怨《纽约时报》每日 Connections 文字谜题（第 756 期）中一个特别令人抓狂的类别。这个谜题要把 16 个词分组到四个主题类别，其中紫色（最难）一组的主题是「以腿部部位的同音词结尾」。这些词是 crypto（听上去以 "toe" 结尾）、decaf（以 "calf" 结尾）、Disney（以 "knee" 结尾）和 Prussian（以 "shin" 结尾）。这种牵强的关联因为过于冷僻、且依赖口音，在网上引发了大量声讨和梗图。

你想到的那条热门帖子很可能是这样：它展示了谜题网格的截图，配文「This game is a psyop to give me schizophrenia.」（这个游戏是给我植入精神分裂的心理战）。它由 @LinkofSunshine 发布并迅速走红，几天内收获超过 21,000 个赞和数百条回复、引用与转发。回复中许多人表达了同样的沮丧，称这个与腿相关的类别「荒唐」或「不靠瞎猜根本做不出来」。

如果这不是你想找的那条，告诉我更多细节（比如用户名或确切措辞），我可以继续深挖！

## [Grok 4 Heavy](#grok-4-heavy)

我们在并行测试时算力上取得了进一步进展，让 Grok 可以同时考虑多个假设。我们把这个模型称为 Grok 4 Heavy，它为性能和可靠性树立了新标准。Grok 4 Heavy 在大多数学术基准上达到饱和，并且是第一个在 Humanity's Last Exam 上得分达到 50% 的模型——该基准「旨在成为此类最后一个封闭式学术基准」。

Grok 4 Heavy

处理中

约剩 10 分钟

智能体 1

约剩 10 分钟

智能体 2

约剩 10 分钟

智能体 3

约剩 10 分钟

思考了 10 分钟

## [前沿智能](#frontier-intelligence)

Grok 4 代表了前沿智能的一次跃升：在 ARC-AGI V2 上以 15.9% 创下封闭模型的新纪录（几乎是 Opus 约 8.6% 的两倍，比此前最高高出 8 个百分点）。在智能体基准 Vending-Bench 上，它以 4694.15 美元净资产和售出 4569 件商品（5 次运行的平均值）占据绝对优势，远远甩开 Claude Opus 4（2077.41 美元、1412 件）、人类（844.05 美元、344 件）等。Grok 4 Heavy 以 61.9% 领跑 USAMO'25，并是第一个在 Humanity's Last Exam（纯文本子集）上得分 50.7% 的模型，展现了通过规模化强化学习和原生工具使用获得的复杂推理能力。

### GPQA

科学

### LiveCodeBench（1-5 月）

竞技编程

### USAMO 2025

奥数证明

### HMMT 2025

竞赛数学

### AIME'25

竞赛数学

### ARC-AGI v2 Semi Private

模式识别

## [Grok 4 API](#grok-4-api)

Grok 4 API 为开发者提供前沿的多模态理解、256k 上下文窗口和高级推理能力，以应对文本和视觉上的复杂任务。它通过我们新推出的实时搜索 API 集成 X、网络和各种新闻来源的实时数据搜索，借助原生工具使用给出最新、准确的回答。API 具备企业级安全与合规——包括 SOC 2 Type 2、GDPR 和 CCPA 认证——为敏感应用提供可靠保护。Grok 4 很快将登陆我们的超大规模云合作伙伴，让企业更容易大规模部署创新 AI 解决方案。

## [Grok 4 语音模式](#grok-4-voice-mode)

在我们升级后的语音模式中与 Grok 对话，拥有更强的真实感、响应速度和智能。我们引入了一个沉静的全新声音，并重新设计了对话，使其更加自然。

而现在，Grok 能看到你所看到的！把摄像头对准目标，直接开口说话，Grok 就会在语音聊天体验中实时拉取动态信息、分析你的场景并实时回应你。我们自豪地呈现这个完全内部训练的模型，它基于我们最先进的强化学习框架和语音压缩技术。

![Grok App 中的语音模式正在解释摄像头中看到的画面](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fvoice-vision.270067a9.webp&w=3840&q=75)

在语音聊天中开启视频，Grok 说话时就会看着它所看到的画面。

## [接下来](#whats-next)

xAI 将继续把强化学习扩展到前所未有的水平，在 Grok 4 进展的基础上推进 AI 智能的边界。我们计划把范围从受控领域的可验证奖励，扩展到处理复杂的真实世界问题，让模型可以在动态环境中学习和适应。多模态能力将持续改进，整合视觉、音频等更多模态，实现更直观的交互。总体而言，我们的重点仍是让模型更聪明、更快、更高效，朝着真正深刻理解并协助人类的系统迈进。

在以下平台试用 Grok

[网页](https://grok.com)

[iOS](https://apps.apple.com/app/apple-store/id6670324846?pt=126952307&ct=x.ai%20Direct%20Link&mt=8)

[Android](https://play.google.com/store/apps/details?id=ai.x.grok&hl=en)

[Grok on X](https://x.com/i/grok)

产品

[Grok](/grok)

[API](/api)

公司

[公司简介](/company)

[招聘](/careers)

[联系我们](/contact)

[新闻](/news)

资源

[文档](https://docs.x.ai)

[隐私政策](/privacy-policy)

[安全](/security)

[法律](/legal)

[状态](https://status.x.ai)
