---
title: "「High Five」行动：菲律宾政治评论"
title_en: "Operation “High Five”: Philippines political comments"
date: 2026-10-13
source: https://openai.com/index/disrupting-malicious-uses-of-ai-high-five/
crawled: 2026-10-19
category: research
translated: 2026-10-19
---

# 「High Five」行动：菲律宾政治评论

> 原文：[Operation "High Five": Philippines political comments](https://openai.com/index/disrupting-malicious-uses-of-ai-high-five/) · OpenAI 博客

*本案例研究最初发表于 OpenAI 的* [*2025 年 6 月*](https://cdn.openai.com/threat-intelligence-reports/5f73af09-a3a3-4a55-992e-069237681620/disrupting-malicious-uses-of-ai-june-2025.pdf) *报告。*

## 行为者

我们封禁了一批 ChatGPT 账号，它们使用我们的模型批量生成英语和 Taglish（他加禄语与英语的混合语）短评论。这些评论由 TikTok 和 Facebook 上的账号发布，聚焦菲律宾的政治与时事。该活动与菲律宾的一家商业营销公司 Comm&Sense Inc 存在关联。

## 行为

该威胁行为者使用 ChatGPT 支持一场以菲律宾受众为目标的政治影响力活动的多个阶段，这些阶段包括内容分析、评论生成，以及生成与该活动相关的公关材料。

首先，该威胁行为者使用 ChatGPT 分析有关菲律宾政治事件的社交媒体帖子，尤其是涉及 Bongbong Marcos 总统的内容，并让它为回复建议合适的主题。其次，他们要求模型按照每个拟定主题批量生成短评论，通常不超过十个词。

第三，该威胁行为者使用 ChatGPT 为其隐蔽影响力行动生成公关推介文案和统计分析，很可能既服务于其推定的当前客户，也服务于未来的潜在客户。这些推介文案声称，该行动已创建了五个旨在推广 Marcos 总统议程的 TikTok 频道。基于这五个频道的使用、该行动在许多评论中使用表情符号的做法，以及整体上的正面基调，我们将其命名为「High Five」（意为「击掌」）。

我们的调查识别出了这五个 TikTok 频道，它们似乎从 2025 年 2 月中旬开始发布内容。每个频道发布相同的视频，但配以不同的说明文字。该行动生成的评论随后由数十个 TikTok 账号发布，作为对这些视频的回复。

![与该行动相关联频道上的 TikTok 视频，展示了其中三条用户评论。这三条评论均由该威胁行为者使用我们的模型生成。](https://images.ctfassets.net/kftzwdyauwt9/6oqOSVwS3A3XcSIfHuUatQ/f21d1c4b5f34b9477d7300cf4e1e62c3/june-2025-covert-io-operation-high-five-p15-fig1.png?w=3840&q=90&fm=webp)

*与该行动相关联频道上的 TikTok 视频，展示了其中三条用户评论。这三条评论均由该威胁行为者使用我们的模型生成。*

在 Facebook 上，该行动生成的评论被发布在主流媒体的新闻报道下作为回复。没有任何迹象表明这些主流媒体与该行动存在任何关联。

![由该行动生成的 Facebook 评论，作为对 ABS-CBN News 一篇新闻报道的回复发布。](https://images.ctfassets.net/kftzwdyauwt9/1cxRurSy9az09KoaQuCQWs/633c010a345a847adb341bed5fcbf6fa/june-2025-covert-io-operation-high-five-p16-fig2.png?w=3840&q=90&fm=webp)

*由该行动生成的 Facebook 评论，作为对* [*ABS-CBN News*](https://www.facebook.com/abscbnNEWS/posts/pfbid02aor2cQq2HYGx85npDbuAR4Po9Kk1vtmMnt8X2EZUEX2ykyW3oHefYbvSKMEafxqZl) *一篇新闻报道的回复发布。*

在我们封禁最初那批账号之后，我们根据现有的技术和行为指标判断，该威胁行为者曾多次试图重新使用我们的模型。

## 生成内容

该行动生成并发布到网上的评论简短但带有明显的党派倾向。它们通常称赞 Marcos 总统及其各项倡议，或批评副总统 Sara Duterte。一些评论给副总统 Duterte 起了「Princess Fiona」（菲欧娜公主）的绰号，可能是在影射《怪物史莱克》系列电影。

篇幅较长的推销文案则更为详细，其中包括一份为该行动本身所做的推介。少部分生成内容（completions）属于商业营销材料。这种隐蔽影响力行动与商业营销材料相结合的特征，与一家同时服务多个客户的公关公司的做法相符。

## 影响

该网络发布了大量内容，在 TikTok 和 Facebook 上发布的评论至少数以千计。然而，在我们调查期间于网上识别出的评论中，没有任何一条获得超过个位数的回复、点赞或分享，大多数甚至一无所获。

从该威胁行为者自己使用的 prompt 来看，其 Facebook 评论的目标是灌满评论区。这一目标充其量只取得了部分成功。在 TikTok 上，评论则聚集在该行动运营的五个频道周围。鉴于其中大量评论并非出自真实用户，对这些数字应谨慎解读。

使用影响力行动（IO）影响评估所用的 Breakout Scale（爆发量表），我们会将此次行动评为第二类：在多个平台上均有活动，但几乎没有证据表明有真实人群接收或广泛传播了其内容。

## 作者
