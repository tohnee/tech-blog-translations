---
title: "Grok 4 Fast"
title_en: "Grok 4 Fast"
date: 2025-09-19
source: https://x.ai/news/grok-4-fast
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok 4 Fast

> 原文：[Grok 4 Fast](https://x.ai/news/grok-4-fast) · xAI

2025 年 9 月 19 日

推进高性价比智能的前沿

![抽象数字蜂鸟](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fgrok-4-fast.aa4f6ad4.webp&w=3840&q=75)

我们很高兴地发布 Grok 4 Fast——我们在高性价比推理模型上的最新进展。Grok 4 Fast 建立在 xAI 从 Grok 4 中获得的经验之上，在企业与消费领域都提供前沿水平的性能，并拥有出色的 token 效率。这个模型推动了更小、更快 AI 的边界，让高质量推理惠及更多用户和开发者。Grok 4 Fast 具备最先进（SOTA）的成本效率、尖端的网页和 X 搜索能力、2M token 上下文窗口，以及将 `reasoning` 和 `non-reasoning` 模式融于同一模型的统一架构。

## [推进高性价比智能](#advancing-cost-efficient-intelligence)

Grok 4 Fast 树立了高性价比智能的新前沿：在推理基准上超越 Grok 3 Mini，同时大幅削减 token 成本。

| 基准 pass@1 | Grok 4 Fast | Grok 4 | Grok 3 Mini (High) | GPT-5 (High) | GPT-5 Mini (High) |
| --- | --- | --- | --- | --- | --- |
| GPQA Diamond | 85.7% | 87.5% | 79.0% | 85.7% | 82.3% |
| AIME 2025（无工具） | 92.0% | 91.7% | 83.0% | 94.6% | 91.1% |
| HMMT 2025（无工具） | 93.3% | 90.0% | 74.0% | 93.3% | 87.8% |
| HLE（无工具） | 20.0% | 25.4% | 11.0% | 24.8% | 16.7% |
| LiveCodeBench（1-5 月） | 80.0% | 79.0% | 70.0% | 86.8% | 77.4% |

我们用大规模强化学习来最大化 Grok 4 Fast 的智能密度。在我们的评测中，Grok 4 Fast 在基准上取得与 Grok 4 相当的表现，同时平均少用 40% 的思考 token。

### 智能密度

以最低成本实现最大性能

### AIME 2024（无工具）

分数(%)

100%

思考 token

28000

### AIME 2025（无工具）

分数(%)

100%

思考 token

28000

### HMMT 2025（无工具）

分数(%)

100%

思考 token

28000

### GPQA Diamond

分数(%)

100%

思考 token

28000

Grok 4 Fast 的 token 效率提升 40%，叠加显著更低的单 token 价格，使其在前沿基准上达到与 Grok 4 相同性能的价格降低 98%。经 Artificial Analysis 的独立评测验证，在 Artificial Analysis Intelligence Index 上，Grok 4 Fast 与其他公开可用模型相比展现出最先进（SOTA）的价格智能比。

### 智能与价格

Artificial Analysis Intelligence Index

Artificial Analysis Intelligence Index

75

运行智能指数的成本（美元，对数刻度）

*所有 Claude 模型均在 Extended Thinking 下进行基准测试。

## [原生工具使用与 SOTA 搜索](#native-tool-use-with-sota-search)

Grok 4 Fast 经过端到端的工具使用强化学习（RL）训练。它擅长决定何时调用代码执行或网页浏览等工具。

例如，Grok 4 Fast 展现出前沿的智能体搜索能力，可以无缝浏览网页和 X，用实时数据增强查询。它在链接间跳转、摄取媒体（包括 X 上的图片和视频），并以光速综合出结论。

| 基准 pass@1 | Grok 4 Fast | Grok 4 | Grok 3（非推理） |
| --- | --- | --- | --- |
| BrowseComp | 44.9% | 43.0% | — |
| SimpleQA | 95.0% | 94.0% | 82.0% |
| Reka Research Eval | 66.0% | 58.0% | 37.0% |
| BrowseComp (zh) | 51.2% | 45.0% | 10.8% |
| X Bench Deepsearch (zh) | 74.0% | 66.0% | 27.0% |
| X Browse* | 58.0% | 53.2% | 20.8% |

*X Browse 是一个内部基准，评测智能体在 X 上进行多跳搜索与浏览的能力。

## [通用后训练的前沿](#frontier-of-general-post-training)

Grok 4 Fast 在通用领域同样确立了新的高性价比前沿。我们很高兴分享 Grok 4 Fast 在 LMArena 上的成绩——它此前一直在 Search 和 Text 竞技场进行私密对战测试。

在 LMArena 的 [Search Arena](https://lmarena.ai/leaderboard/search) 上，`grok-4-fast-search`（代号：`menlo`）以 **1163** Elo 荣登**第一**——领先 `o3-search` 整整 **17** 分。其卓越的推理效率和智能密度，使它能在真实世界的搜索相关任务上超越大得多的模型。

![Artificial Intelligence Search Arena](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fsearch_arena.3ef5c2bf.webp&w=3840&q=75)

在 LMArena 的 [Text Arena](https://lmarena.ai/leaderboard/text) 上，`grok-4-fast`（代号：`tahoe`）排名**第八**，与 `grok-4-0709` 表现相当，凸显了其出色的智能密度。值得注意的是，它显著超越同量级的对手——所有同等规模的模型都排在**第 18**名或更低。

![Artificial Intelligence Text Arena](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Ftext_arena.7699983e.webp&w=3840&q=75)

以下是 Grok 4 Fast 的一些实战示例：

流放之路X 搜索研究

《流放之路 2》中可能获得的经验点数上限是多少？

显示完整轨迹

思考了 24 秒

调查游戏细节

这个请求是要找出《流放之路 2》中经验点数的最大值。

《流放之路 2》是一款动作 RPG，截至 2025 年 9 月 10 日可能仍处于抢先体验阶段。

搜索 maximum experience points Path of Exile 2

reddit.com

polygon.com

turtlebeach.com

+2 个其他来源

根据搜索结果，《流放之路 2》的最高等级为 100 级。

这个问题很可能指的是升到 100 级所需的总经验值。

浏览 https://www.poewiki.net/wiki/Experience

根据 PoE Wiki，最近的一次搜索发现《流放之路》升到 100 级所需的总经验值约为 230 亿。

搜索 total experience points to reach level 100 Path of Exile

reddit.com

pathofexile.fandom.com

pathofexile.com

+1 个其他来源

改进搜索策略

根据 91 级和 97 级的数据，最近的结果显示升到 100 级所需的总经验值可能超过 40 亿。

浏览 https://www.poewiki.net/wiki/Experience

让我们搜索确认 PoE2 是否使用与 PoE1 相同的经验表。

搜索 Path of Exile 2 experience requirements same as PoE1

reddit.com

pathofexile.com

pathofexile.fandom.com

+1 个其他来源

此前的搜索显示 PoE1 和 PoE2 的最高等级都是 100 级，且没有提到经验值有变化。

搜索 Path of Exile 2 total XP to level 100

reddit.com

pathofexile.com

pathofexile.fandom.com

+1 个其他来源

由于 PoE2 与 PoE1 使用相同的游戏引擎，其经验系统很可能与 PoE1 完全一致。

搜索 Path of Exile 2 experience table level XP

pathofexile.fandom.com

reddit.com

poe2db.tw

+1 个其他来源

找到了一个站点 PoE2DB，列出了最高到 100 级的经验等级。

浏览 https://poe2db.tw/us/Experience

**4,250,334,444**

在《流放之路 2》中，角色最高等级为 100 级，从 1 级升到 100 级总共需要 4,250,334,444 点经验值（XP）。这个数值是根据游戏固定的经验表（与初代《流放之路》完全相同）逐级累加所需经验的总和。达到 100 级之后，仍可继续获得经验值，但不再提升等级或带来实质性的进度。

为得出这一总数，游戏的经验系统采用一张预定义的表，每升一级所需的经验值逐步递增。100 级的「总经验」就是从 1 级到 100 级所有经验阈值的总和。计算步骤如下：

1. **理解经验结构**：每升到下一级都有对应的需求经验值（例如从 1 级升到 2 级需要 525 XP）。某一等级的总经验是此前所有需求的累计和。1 级从 0 XP 起步。
2. **查阅经验表**：《流放之路 2》的官方数据源提供了完整表格。例如：
   - 2 级：总经验 525（从 1 级起需获得 525）。
   - 3 级：总经验 1,760（从 2 级起需获得 1,235）。
   - ……以此类推，直到 100 级。
3. **求和**：把全部 99 次升级（从 1 级到 100 级）所需经验相加。可以通过程序计算或查表中的累计值，得到 4,250,334,444。

## [统一模型：推理与非推理](#unified-model-reasoning-and-non-reasoning)

此前，不同的推理模式需要不同的模型。Grok 4 Fast 引入了统一架构：`reasoning`（长思维链）和 `non-reasoning`（快速响应）由同一份模型权重处理，通过系统提示词进行切换。这种统一降低了端到端延迟和 token 成本，使 Grok 4 Fast 非常适合实时应用。

在 [grok.com](http://grok.com/?q=What%20is%20the%20answer%20to%20life,%20the%20universe,%20and%20everything?&m=7) 上，这带来了平滑的切换：简单查询即时响应，复杂查询则展开长时间的推理。在 xAI API 中，开发者可以微调这一行为，在速度与深度之间做优化。

## [Grok 4 Fast 登陆 grok.com、iOS 和 Android App](#grok-4-fast-in-grokcom-ios-and-android-apps)

[![Web Globe Icon](/_next/static/media/grok.8df090bc.svg)

打开

Grok.com](http://grok.com/?q=What%20is%20the%20answer%20to%20life,%20the%20universe,%20and%20everything?&m=7)[![iOS Play Store Icon](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fapp-store.c32726fa.png&w=48&q=75)

打开

Grok on iOS](https://apps.apple.com/us/app/grok/id6670324846)[![Android Play Store Icon](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fplay-store.57869c2b.png&w=48&q=75)

打开

Grok on Android](https://play.google.com/store/apps/details?id=ai.x.grok)

Grok 4 Fast 现已向所有用户开放。在 `Fast` 和 `Auto` 模式下，你会看到搜索和信息查询类问题的显著改进。此外，`Auto` 模式下的困难查询将使用 Grok 4 Fast，在不损失质量的前提下带来快得多的体验。所有用户（包括免费用户）都将首次不受限制地使用我们的最新模型，标志着先进 AI 普惠化的一步。

## [Grok 4 Fast 登陆 OpenRouter、Vercel AI Gateway 与 xAI API](#grok-4-fast-on-openrouter-vercel-ai-gateway-and-the-xai-api)

限时期间，Grok 4 Fast 将在 [OpenRouter](https://openrouter.ai/x-ai/grok-4-fast) 和 [Vercel AI Gateway](https://vercel.ai/ai-gateway) 上免费提供。

我们还将以两个模型的形式推出 Grok 4 Fast：`grok-4-fast-reasoning` 和 `grok-4-fast-non-reasoning`，均配备 2M token 上下文窗口。这让开发者可以针对自己的用例调节测试时算力的用量。

`grok-4-fast-reasoning` 和 `grok-4-fast-non-reasoning` 已通过 [xAI API](https://x.ai/api) 正式可用，定价如下：

| Token 类型 | <128k tokens | ≥128k tokens |
| --- | --- | --- |
| 输入 token | $0.20 / 1M | $0.40 / 1M |
| 输出 token | $0.50 / 1M | $1.00 / 1M |
| 缓存输入 token | $0.05 / 1M | |

## [接下来](#whats-next)

我们将根据你在 [x.com](http://x.com) 上的反馈，持续向 Grok 4 Fast 推送模型改进。请期待更多集成，包括增强的多模态能力和智能体功能。

在[这里](https://data.x.ai/2025-09-19-grok-4-fast-model-card.pdf)阅读 Grok 4 Fast 模型卡。

以上就是全部内容——再见，谢谢所有的鱼！

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

[安全性](/safety)

[法律](/legal)

[状态](https://status.x.ai)
