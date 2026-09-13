---
title: "Gemini 2.5：我们最智能的模型变得更强"
title_en: "Gemini 2.5: Our most intelligent models are getting even better"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/google-gemini-updates-io-2025/
site: google-blog
date: 2025-05-20
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini 2.5：我们最智能的模型变得更强

> 原文：[Gemini 2.5: Our most intelligent models are getting even better](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/google-gemini-updates-io-2025/) · Google

今年 3 月，我们发布了迄今最智能的模型 [Gemini 2.5 Pro](https://blog.google/technology/google-deepmind/gemini-model-thinking-updates-march-2025/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)；两周前，我们又提前带来了 [I/O 更新](https://blog.google/products/gemini/gemini-2-5-pro-updates/)，让开发者得以构建出色的 web 应用。今天，我们将分享 [Gemini 2.5](https://deepmind.google/technologies/gemini/?_gl=1*1hcx28i*_up*MQ..*_ga*OTE5NDY4NDk5LjE3NDc1NzI2Mzk.*_ga_LS8HVHCNQ0*czE3NDc1NzI2MzgkbzEkZzAkdDE3NDc1NzI2MzgkajAkbDAkaDA.) 模型系列的更多更新：

- 除了 2.5 Pro 在[学术基准测试](https://deepmind.google/technologies/gemini/pro/)上的惊艳表现之外，它如今在 [WebDev Arena](https://web.lmarena.ai/leaderboard) 和 [LMArena](https://lmarena.ai/?leaderboard) 排行榜上都是世界领先的模型，在[帮助人们学习](https://blog.google/outreach-initiatives/education/google-gemini-learnlm-update)方面同样领跑。
- 我们正在为 2.5 Pro 和 2.5 Flash 带来新能力：带来更自然对话体验的原生音频输出、更先进的安全防护措施，以及 [Project Mariner](https://deepmind.google/technologies/project-mariner/?_gl=1*1c8pzpn*_up*MQ..*_ga*MTg3MDY5NzA5LjE3NDc0MTgwOTc.*_ga_LS8HVHCNQ0*czE3NDc0MTgwOTckbzEkZzAkdDE3NDc0MTgxMDAkajAkbDAkaDA.) 的计算机操作能力。2.5 Pro 还将借助 [Deep Think](https://deepmind.google/models/gemini/pro) 变得更强——这是一种实验性的增强推理模式，面向高度复杂的数学与编码任务。
- 我们持续投资开发者体验：在 [Gemini API](https://www.googleadservices.com/pagead/aclk?sa=L&ai=DChcSEwisvpPlh62NAxVhkVAGHQQyExAYABABGgJkZw&co=1&ase=2&gclid=Cj0KCQjwiqbBBhCAARIsAJSfZkb2UNm71aDTiQj43uE6u_X4kdQjkW-zJE4ys1-WPCsHAjQPW0JsAfEaAnO5EALw_wcB&ohost=www.google.com&cid=CAESVuD2XZH0cGUhnUN_hgWfLPh0qxdkyaxfS7GgJW3CE1EWqyyuEGeFtJxpp-RPP_6lGT_tcrNml8Z0ycbys16CbucweCE9iTf9Fezie1FFOvssm7ZxarUX&category=acrcp_v1_5&sig=AOD64_3P3Z7aCoP-AB8jidfzdFepXVjQQg&q&nis=4&adurl&ved=2ahUKEwjz0Y7lh62NAxXXSEEAHTUKO98Q0Qx6BAgKEAE) 和 [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio) 中引入思考摘要（thought summaries）以获得更高透明度，将思考预算（thinking budgets）扩展到 2.5 Pro 以获得更多控制，并在 Gemini API 和 [SDK](https://ai.google.dev/gemini-api/docs/migrate) 中加入对 MCP 工具的支持，从而访问更多开源工具。
- 2.5 Flash 现已在 [Gemini 应用](http://gemini.google.com/)中对所有人开放；6 月初，更新版将在面向开发者的 [Google AI Studio](http://aistudio.google.com/) 和面向企业的 [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio) 中正式发布（GA），2.5 Pro 也将紧随其后。

这一显著进展，是 Google 各团队不懈努力的结果——他们不断改进我们的技术，并以安全、负责任的方式开发和发布。下面进入正题。

## 2.5 Pro 表现前所未有

我们最近[更新了 2.5 Pro](https://blog.google/products/gemini/gemini-2-5-pro-updates/)，帮助开发者构建更丰富、更具交互性的 web 应用。看到[用户和开发者的积极反响](https://www.youtube.com/watch?v=c6UkBTTOIAE%27)令人欣喜，我们会继续根据用户反馈做出改进。

除了在学术基准测试上的强劲表现，新版 2.5 Pro 目前以 1415 的 ELO 分数领跑广受欢迎的编程排行榜 [WebDev Arena](https://web.lmarena.ai/leaderboard)。它还在 [LMArena](https://lmarena.ai/?leaderboard) 的所有排行榜上居首，该榜单从多个维度评估人类偏好。此外，凭借 100 万 token 的上下文窗口，2.5 Pro 拥有最先进的[长上下文与视频理解性能](https://developers.googleblog.com/en/gemini-2-5-video-understanding/)。

自从融入 LearnLM——我们与教育专家共同构建的模型家族——2.5 Pro 现在也是[学习领域的领先模型](https://blog.google/outreach-initiatives/education/google-gemini-learnlm-update)。在评估其教学法与有效性的正面对比中，教育工作者和专家在多种不同场景下都更青睐 Gemini 2.5 Pro 而非其他模型。而且，它在用于构建学习型 AI 系统的[学习科学五大原则](http://goo.gle/learnlm)的每一项上都[胜过了顶尖模型](https://goo.gle/LearnLM-May25)。

更多信息请参阅我们更新的 [Gemini 2.5 Pro 模型卡](https://storage.googleapis.com/model-cards/documents/gemini-2.5-pro-preview.pdf)和 [Gemini 技术页面](https://deepmind.google/technologies/gemini/#introduction)。

### Deep Think

通过探索 Gemini 思考能力的前沿，我们开始测试一种名为 [Deep Think](https://deepmind.google/models/gemini/pro) 的增强推理模式，它采用新的研究技术，使模型在回应之前能够考虑多个假设。

2.5 Pro Deep Think 在 [2025 USAMO](https://maa.org/news/2025-usamo-and-usajmo-thresholds-now-available/)——目前最难的数学基准之一——上取得了令人瞩目的成绩。它还在 [LiveCodeBench](https://livecodebench.github.io/leaderboard.html)（高难度的竞赛级编程基准）上居首，并在测试多模态推理的 [MMMU](https://mmmu-benchmark.github.io/) 上取得 84.0% 的分数。

![展示 Gemini 2.5 Pro Deep Think 先进能力的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/deep-think-chart.width-1200.format-webp.webp)

由于 2.5 Pro DeepThink 正在定义前沿，我们将投入额外时间开展更多前沿安全评估，并征求安全专家的进一步意见。作为其中一环，我们将先通过 [Gemini API](https://ai.google.dev/) 向受信任的测试者开放，在广泛推出之前收集他们的反馈。

## 更进一步的 2.5 Flash

[2.5 Flash](https://deepmind.google/technologies/gemini/flash/) 是我们为速度和低成本而设计的高效主力模型——如今它在许多维度上都更出色。它在推理、多模态、代码和长上下文等关键基准测试上均有提升，同时效率更高——在我们的评估中 token 消耗减少了 20-30%。

![Gemini 2.5 Flash 与其他模型的对比图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_2-5_flashcomp_benchmarks_cropped_light2x.gif)

新版 2.5 Flash 现已开放预览：开发者在 [Google AI Studio](http://aistudio.google.com/) 中、企业在 [Vertex AI](https://console.cloud.google.com/vertex-ai/studio/multimodal?model=gemini-2.5-flash-preview-05-20) 中、所有人在 [Gemini 应用](http://gemini.google.com/)中均可使用。6 月初，它将正式发布（GA），可用于生产环境。

更多信息请参阅我们更新的 [Gemini 2.5 Flash 模型卡](https://storage.googleapis.com/model-cards/documents/gemini-2.5-flash-preview.pdf)和 [Gemini 技术页面](https://deepmind.google/technologies/gemini/#introduction)。

### 原生音频输出与 Live API 改进

今天，[Live API](https://ai.google.dev/gemini-api/docs/live) 推出了视听输入与原生音频输出对话的预览版，让你可以直接构建对话体验，拥有一个更自然、更具表现力的 Gemini。

它还允许用户调控其语气、口音和说话风格。例如，你可以让模型在讲故事时使用戏剧化的声音。它还支持工具使用，能够代你进行搜索。

你可以试用一组早期功能，包括：

- 情感化对话（Affective Dialogue）：模型能检测用户声音中的情绪并作出恰当回应。
- 主动音频（Proactive Audio）：模型会忽略背景对话，并知道何时该回应。
- Live API 中的思考（Thinking）：模型利用 Gemini 的思考能力来支持更复杂的任务。

我们还在 2.5 Pro 和 2.5 Flash 上发布新的文本转语音预览版。它们首次支持多说话人，可通过原生音频输出实现双声音的文本转语音。

与原生音频对话一样，文本转语音极具表现力，能够捕捉非常细微的差别，例如耳语。它支持超过 24 种语言，并可在语言之间无缝切换。

这项文本转语音能力将于今天晚些时候在 [Gemini API](https://ai.google.dev/) 中开放。

### 计算机操作

我们正在把 [Project Mariner](https://deepmind.google/technologies/project-mariner/) 的计算机操作能力引入 [Gemini API](https://ai.google.dev/) 和 [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio)。Automation Anywhere、UiPath、Browserbase、Autotab、The Interaction Company 和 Cartwheel 等公司正在探索其潜力，我们很高兴将于今年夏天更广泛地推出，供开发者试验。

### 更强的安全性

我们还大幅加强了对安全威胁的防护，例如间接提示词注入（indirect prompt injection）——即在 AI 模型检索到的数据中嵌入恶意指令。我们的[新安全方法](https://storage.googleapis.com/deepmind-media/Security%20and%20Privacy/Gemini_Security_Paper.pdf)显著提高了 Gemini 在工具使用过程中抵御间接提示词注入攻击的防护率，使 Gemini 2.5 成为迄今最安全的模型家族。

欲了解更多，请阅读我们[在安全、责任与保障方面的各项工作](https://deepmind.google/about/responsibility-safety/?_gl=1*10qw615*_up*MQ..*_ga*NDcyMjA1ODA3LjE3NDc0MDI5ODA.*_ga_LS8HVHCNQ0*czE3NDc0MDI5ODAkbzEkZzAkdDE3NDc0MDI5ODAkajAkbDAkaDA.)，以及 Google DeepMind 博客上[我们如何推进 Gemini 的安全防护措施](https://deepmind.google/discover/blog/advancing-geminis-security-safeguards/)。

### 思考摘要

2.5 Pro 和 Flash 现在将在 [Gemini API](https://ai.google.dev/) 和 [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio) 中提供思考摘要。思考摘要将模型的原始思考过程整理为清晰的格式，包含标题、关键细节以及模型动作的信息（例如何时使用了工具）。

我们希望，通过对模型思考过程采用更结构化、更精炼的呈现方式，开发者和用户会发现与 Gemini 模型的交互更易于理解和调试。

### 思考预算

我们在推出 2.5 Flash 时引入了思考预算（thinking budgets），通过平衡延迟与质量，让开发者更好地控制成本。现在我们将这一能力扩展到 2.5 Pro。这让你可以控制模型在响应之前用于思考的 token 数量，甚至可以完全关闭其思考能力。

未来几周，带思考预算的 Gemini 2.5 Pro 将与我们的正式版模型一同正式发布（GA），可用于稳定的生产环境。

### MCP 支持

我们在 Gemini API 中为 Model Context Protocol（MCP）定义添加了原生 SDK 支持，以便更轻松地集成开源工具。我们还在探索部署 MCP 服务器和其他托管工具的方式，让你更轻松地构建智能体化应用。

我们始终在探索新方法来改进模型与开发者体验，包括让它们更高效、性能更强，并持续回应开发者的反馈——请继续向我们提出！我们也在基础研究的广度和深度上加倍投入，不断推动 Gemini 能力的前沿。更多内容即将推出。

欲详细了解 Gemini 及其能力，请访问[我们的网站](https://deepmind.google/technologies/gemini/#introduction)。
