---
title: "Google I/O 2025：从研究走向现实"
title_en: "Google I/O 2025: From research to reality"
source: https://blog.google/innovation-and-ai/technology/ai/io-2025-keynote/
site: google-blog
date: 2025-05-20
crawled: 2026-09-13
translated: 2026-09-13
---

# Google I/O 2025：从研究走向现实

> 原文：[Google I/O 2025: From research to reality](https://blog.google/innovation-and-ai/technology/ai/io-2025-keynote/) · Google

*编者注：以下是 Google CEO Sundar Pichai（桑达尔·皮查伊）在 Google I/O 2025 上发言的整理稿，经过编辑以补充更多台上发布的内容。所有发布内容请见我们的*[合集](https://blog.google/technology/developers/google-io-2025-collection)*。*

通常情况下，在 I/O 召开前的几周里，你不会从我们这里听到太多消息，因为我们会把最好的模型攒到台上发布。但在 Gemini 时代，我们同样可能[在三月的某个星期二就发布我们最智能的模型](https://blog.google/technology/google-deepmind/gemini-model-thinking-updates-march-2025/)，或者[提前一周宣布像 AlphaEvolve 这样非常酷的突破](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)。

我们希望尽快把最好的模型交到你手中、融入我们的产品。因此，我们的发布速度比以往任何时候都快。

!["以不懈节奏持续发布"示意图，展示了 Google AI 发展的时间线](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/IO25_Shipping.width-1200.format-webp.webp)

## 不懈的模型进步

我对模型的快速进步尤其感到兴奋。作为衡量进步的一项指标，Elo 分数较我们的第一代 Gemini Pro 模型已提升 300 多分。如今，Gemini 2.5 Pro 在 LMArena 排行榜的所有类别中全面领先。

模型的进步得益于我们世界领先的基础设施。我们的第七代 TPU [Ironwood](https://blog.google/products/google-cloud/ironwood-tpu-age-of-inference/)，是首个专门为大规模思考与推理型 AI 工作负载而设计的 TPU。它的性能是上一代的 10 倍，每个 pod 可提供高达 42.5 exaflops 的算力——实在令人惊叹。

我们的基础设施实力——一直深入到 TPU 层面——让我们能够提供速度快得多的模型，即便模型价格正在大幅下降。一次又一次，我们都能够以最有效的价格点提供最好的模型。Google 不仅在帕累托前沿（Pareto Frontier）上领跑，更从根本上移动了这条前沿本身。

![展示低成本 AI 模型帕累托前沿的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/0520_ParetoFrontier.width-1200.format-webp.webp)

## 世界正在拥抱 AI

更强的智能正在惠及每个人、抵达每个地方。世界也在积极回应，以前所未有的速度拥抱 AI。以下是几个重要的进展标志：

- 去年这个时候，我们在所有产品和 API 上每月处理 9.7 万亿个 token。如今，我们每月处理超过 480 万亿个——增长了 50 倍。
- 超过 700 万开发者正在使用 Gemini 进行构建，是去年同期的 5 倍，Vertex AI 上 Gemini 的使用量增长了 40 倍。
- Gemini 应用的月活跃用户已超过 4 亿。尤其是 2.5 系列模型，我们看到了强劲的增长与使用度。在 Gemini 应用中使用 2.5 Pro 的用户，使用量上升了 45%。

## 从研究走向现实

这一切进步意味着，我们已经进入 AI 平台转移的新阶段：数十年的研究成果，如今正在成为全世界个人、企业和社区的现实。

### Project Starline → Google Beam + 语音翻译

几年前的 I/O 大会上，我们首次展示了突破性 3D 视频技术 [Project Starline](https://blog.google/technology/research/project-starline/)。它的目标是营造一种与对方共处一室的感觉，哪怕你们相隔遥远。

我们持续在技术上取得进展。今天，我们准备好开启下一个篇章：[Google Beam](http://blog.google/outreach-initiatives/research/project-starline-google-beam-update)，一个全新的 AI 优先视频通信平台。Beam 采用全新的最先进视频模型，将 2D 视频流转化为逼真的 3D 体验：它利用六摄像头阵列，借助 AI 将多路视频流融合在一起，并把你渲染到 3D 光场显示屏上。它拥有近乎完美、精确到毫米的头部追踪，帧率达到每秒 60 帧，而且全部实时完成。其结果是一种自然得多、沉浸感深得多的对话体验。与 HP 合作的首批 Google Beam 设备将于今年晚些时候向早期客户开放。

![Google Beam 设备](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/SP_MM_Beam_v91.width-1200.format-webp.webp)

这些年来，我们也在 Google Meet 中打造更具沉浸感的体验。其中包括借助语音翻译帮助人们打破语言壁垒的技术，[即将登陆 Google Meet](https://workspace.google.com/blog/product-announcements/new-ways-to-do-your-best-work)。它能以近乎实时的速度匹配说话者的声音与语气，甚至表情——让我们更接近跨语言的自然流畅对话。英语与西班牙语翻译即将以测试版形式推送给 Google AI Pro 和 Ultra 订阅用户，未来几周还将支持更多语言。今年之内，这项功能也将面向 Workspace 企业客户开放早期测试。

### Project Astra → Gemini Live

另一个在 I/O 上首次亮相的激动人心的研究项目是 [Project Astra](https://blog.google/technology/google-deepmind/google-gemini-ai-update-december-2024/#project-astra)，它探索的是能够理解你周围世界的通用 AI 助手（universal AI assistant）的未来能力。[Gemini Live](https://blog.google/technology/google-deepmind/gemini-universal-ai-assistant) 现已整合 Project Astra 的摄像头与屏幕共享能力。人们正以各种有趣的方式使用它，从面试准备到马拉松训练。该功能已面向所有 Android 用户开放，并从今天开始向 iOS 用户推送。

我们也在把这类能力带入 [Search](https://blog.google/products/search/google-search-ai-mode-update) 等产品。

### Project Mariner → Agent Mode

我们把智能体视为这样一类系统：它们将先进 AI 模型的智能与工具访问能力结合在一起，从而能够代表你、并在你的掌控下采取行动。

我们的早期研究原型 Project Mariner，是具备计算机操作（computer use）能力、能够与网页交互并替你把事情办妥的智能体向前迈出的早期一步。我们在 12 月将它作为早期研究原型发布，此后取得了大量进展：新增多任务处理能力，以及一种名为"教学与重复"（teach and repeat）的方法——你只需向它示范一次任务，它就能学会未来执行类似任务的计划。我们正通过 Gemini API 把 Project Mariner 的计算机操作能力带给开发者。Automation Anywhere 和 UiPath 等受信任的测试者已经开始基于它进行构建，它将在今年夏天更广泛地开放。

计算机操作只是我们要为智能体生态蓬勃发展而构建的更庞大工具集的一部分。

比如我们开放式的 Agent2Agent 协议，让智能体之间可以互相通信；又如 Anthropic 推出的 Model Context Protocol（MCP），让智能体能够访问其他服务。今天，我们高兴地宣布：我们的 Gemini API 和 SDK 现已兼容 MCP 工具。

我们也开始把智能体能力带入 Chrome、Search 和 Gemini 应用。例如，[Gemini 应用](https://blog.google/products/gemini/gemini-app-updates-io-2025)中全新的 Agent Mode 将帮你完成更多事情。如果你正在找公寓，它可以在 Zillow 等网站上帮你寻找符合要求的房源、调整筛选条件，并通过 MCP 访问房源信息，甚至为你预约看房。Gemini 应用中 Agent Mode 的实验版本即将向订阅用户推出。这对 Zillow 这样的公司也大有裨益——带来新客户并提升转化率。

这是一个新兴领域，我们期待探索如何最好地把智能体的益处带给更广泛的用户和生态系统。

## 个性化的力量

让研究走进现实的最好方式，是让它真正有用——在你的现实生活中有用。这正是个性化大显身手之处。我们正通过一个叫做个人上下文（personal context）的东西把这一点变为现实。在你许可的前提下，Gemini 模型可以以私密、透明且完全由你掌控的方式，在各个 Google 应用中使用相关的个人上下文。

我们在 Gmail 中推出的全新[个性化智能回复（Smart Replies）](https://workspace.google.com/blog/product-announcements/new-ways-to-do-your-best-work)就是一例。如果你的朋友发邮件向你咨询一次你曾经历过的公路旅行，Gemini 可以替你检索过去的邮件和 Google Drive 中的文件——比如你在 Google Docs 中创建的行程单——从而给出一条细节精准、切中要点的回复建议。它会匹配你惯用的问候语，捕捉你的语气、风格，甚至偏爱的用词，最终生成一条更贴切、听起来真切像你本人所写的回复。个性化智能回复将于今年晚些时候面向订阅用户推出。你可以想象，个人上下文在 Search、Gemini 等更多产品中会带来多么大的帮助。

## Search 中的 AI Mode

我们的 Gemini 模型正在帮助 Google Search 变得更加智能、智能体化和个性化。

自去年推出以来，AI Overviews 已扩展至超过 15 亿用户，覆盖 200 个国家和地区。随着人们使用 AI Overviews，我们看到他们对搜索结果更满意，搜索也更频繁。在美国和印度等最大的市场，AI Overviews 为展示它们的查询类型带来了超过 10% 的增长，而且这一增长还在随时间不断上升。

这是 Search 过去十年中最成功的发布之一。

对于想要端到端 AI 搜索体验的用户，[我们推出了全新的 AI Mode](https://blog.google/products/search/google-search-ai-mode-update)。这是对 Search 的彻底重新构想。借助更先进的推理能力，你可以向 AI Mode 提出更长、更复杂的查询。事实上，早期测试者提出的查询长度已是传统搜索的两到三倍，你还可以通过追问进一步深入。所有这些都可以通过 Search 中的一个新标签页直接使用。

我自己一直在大量使用它，它彻底改变了我使用 Search 的方式。我很高兴地宣布，AI Mode 从今天起面向美国所有人开放。借助我们最新的 Gemini 模型，我们的 AI 回答达到了你对 Search 一贯期待的质量与准确性，并且是业界最快的。而从本周开始，Gemini 2.5 也将登陆美国的 Search。

## 推进我们最智能的模型：Gemini 2.5

我们强大且最高效的主力模型 Gemini 2.5 Flash，深受喜爱其速度与低成本的开发商欢迎。而新版 2.5 Flash 在几乎所有维度上都更出色——在推理、多模态、代码和长上下文等关键基准测试上全面进步。它在 LMArena 排行榜上仅次于 2.5 Pro。

我们还在让 2.5 Pro 更进一步，推出了我们称之为 Deep Think 的增强推理模式。它运用了我们在思考与推理方面的最新前沿研究，包括并行思考（parallel thinking）技术。

## 更个性化、更主动、更强大的 Gemini 应用

我们正在让 [Deep Research](https://gemini.google/overview/deep-research/?hl=en) 更具个性化：你可以上传自己的文件，不久后还将能连接 Google Drive 和 Gmail，增强其生成定制研究报告的能力。我们还将它与 [Canvas](https://gemini.google/overview/canvas/?hl=en) 集成，只需点击一下，就能创建动态信息图、测验，乃至多种语言的播客。除此之外，我们看到基于 Canvas 的氛围编程（vibe coding）正被热情地采用，让更多人只需与 Gemini 聊天就能构建出功能完备的应用。

至于真正引起用户共鸣的 Gemini Live，我们正在向所有人（包括 iOS 用户）免费开放摄像头与屏幕共享功能，并即将把它与你喜爱的 Google 应用连接起来，提供[更无缝的帮助](https://www.youtube.com/watch?v=GaCKzEBT5mY)。

## 生成式媒体模型的进展

我们推出了最新、最先进的视频模型 Veo 3，它现在具备原生音频生成能力。我们还推出了 Imagen 4，这是我们最新、最强大的图像生成模型。两者都已在 Gemini 应用中可用——为创意打开了一个全新的世界。

我们还通过一款名为 [Flow](https://blog.google/technology/ai/google-flow-veo-ai-filmmaking-tool/) 的新工具，把这些可能性带给电影创作者。你可以创建电影级片段，也可以把一个短片段延展成更长的场景。

## 改善生活的机遇

AI 带来的机遇再大不过了。而让它的益处惠及尽可能多的人，将取决于这一代开发者、技术构建者和问题解决者。尤其令人振奋的是，想到我们今天正在做的研究——从机器人到量子，从 AlphaFold 到 Waymo——将成为明天现实的基础。

改善生活的机遇，我从不视为理所当然。最近的一段经历让我对此感触尤深。我和父母在旧金山，他们最想做的第一件事就是乘坐 Waymo——我这才知道，它正在成为这座城市最热门的观光项目之一。我以前坐过 Waymo，但我八十多岁的父亲完全被震撼了；我由此以一种全新的视角看到了这些进步。

这提醒了我：技术拥有激励人心、令人惊叹并推动我们前行的不可思议的力量。我迫不及待地想看到我们接下来共同创造的美好事物。
