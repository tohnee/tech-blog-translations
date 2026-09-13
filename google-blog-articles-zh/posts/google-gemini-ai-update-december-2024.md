---
title: "Gemini 2.0 发布：面向智能体时代的新一代 AI 模型"
title_en: "Introducing Gemini 2.0: our new AI model for the agentic era"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/google-gemini-ai-update-december-2024/
site: google-blog
date: 2024-12-11
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini 2.0 发布：面向智能体时代的新一代 AI 模型

> 原文：[Introducing Gemini 2.0: our new AI model for the agentic era](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/google-gemini-ai-update-december-2024/) · Google

**Google 与 Alphabet CEO Sundar Pichai（桑达尔·皮查伊）的一封信：**

信息是人类进步的核心。正因如此，26 年多来，我们始终专注于"整合全球信息，使人人皆可访问并从中受益"这一使命。也正因如此，我们持续推动 AI 的边界，跨越每一种输入形态去组织信息，并让它可以通过任何输出形态触达用户，从而真正对你有用。

这正是[去年 12 月我们发布 Gemini 1.0](https://blog.google/innovation-and-ai/technology/ai/google-gemini-ai/) 时的愿景。作为首个原生多模态模型，Gemini 1.0 和 1.5 凭借多模态与长上下文能力取得了重大进展，能够理解文本、视频、图像、音频和代码等不同形式的信息，并能处理更多的信息量。

如今，数百万开发者正在基于 Gemini 进行构建。它也在帮助我们重新构想旗下所有产品——包括全部 7 个用户数达 20 亿的产品——并创造新的产品。[NotebookLM](https://notebooklm.google/) 就是一个绝佳的例子，展示了多模态与长上下文能为人们带来什么，以及它为何深受如此多人的喜爱。

过去一年，我们持续投入开发更具智能体化（agentic）能力的模型，也就是说，这些模型能更深入地理解你周围的世界，进行多步思考，并在你的监督下代你采取行动。

今天，我们很高兴推出为这一全新智能体时代打造的下一代模型：Gemini 2.0，我们迄今最强大的模型。凭借多模态方面的新进展——如原生的图像与音频输出——以及原生工具使用能力，它将助力我们构建新的 AI 智能体，让我们离通用助手（universal assistant）的愿景更近一步。

今天，我们将 2.0 交到开发者和受信任测试者手中。我们也正在加紧把它集成到我们的产品中，率先落地的是 Gemini 和搜索。从今天起，我们的 Gemini 2.0 Flash 实验版模型将向所有 Gemini 用户开放。我们同时还在推出一项名为 [Deep Research](https://blog.google/products/gemini/google-gemini-deep-research/) 的新功能，它利用高级推理和长上下文能力充当研究助手，替你探索复杂主题并撰写报告。该功能现已在 Gemini Advanced 中可用，你可以[在我们的网站上了解更多](https://gemini.google/overview/deep-research?utm_source=keywordblog&utm_medium=referral)。

没有任何一款产品比搜索更多地被 AI 改变。我们的 AI Overviews 目前已覆盖 10 亿用户，让他们能够提出全新类型的问题——迅速成为有史以来最受欢迎的搜索功能之一。作为下一步，我们将把 Gemini 2.0 的高级推理能力引入 AI Overviews，以应对更复杂的主题和多步骤问题，包括高难度数学方程、多模态查询和编程。我们本周已开始小范围测试，并将在明年初更广泛地推送。未来一年，我们还将把 AI Overviews 带到更多国家和地区语言。

2.0 的进步离不开十年来我们对差异化全栈 AI 创新路径的持续投入。它构建在 Trillium 等定制硬件之上——这是我们第六代 TPU。TPU 支撑了 Gemini 2.0 训练与推理的 100% 算力，今天 Trillium 已[正式发布（GA）](https://cloud.google.com/blog/products/compute/trillium-tpu-is-ga)面向客户开放，他们也可以用它来进行构建。

如果说 Gemini 1.0 的主题是组织和理解信息，那么 Gemini 2.0 的主题就是让信息变得更有用。我迫不及待想看到下一个时代会带来什么。

——Sundar

---

## Gemini 2.0 发布：面向智能体时代的新一代 AI 模型

*由 Google DeepMind CEO Demis Hassabis（德米斯·哈萨比斯）与 Google DeepMind CTO Koray Kavukcuoglu 代表 Gemini 团队撰写*

过去一年，我们在人工智能领域继续取得令人惊叹的进展。今天，我们发布 Gemini 2.0 系列模型中的首个模型：Gemini 2.0 Flash 实验版。它是我们的主力模型，兼具低延迟与增强性能，代表着我们技术的最前沿，并可大规模部署。

我们还将展示智能体研究的前沿成果，呈现由 Gemini 2.0 原生多模态能力驱动的一系列原型。

## Gemini 2.0 Flash

Gemini 2.0 Flash 建立在 1.5 Flash 的成功之上——1.5 Flash 是迄今为止最受开发者欢迎的模型——2.0 Flash 在保持同样快速的响应时间的同时提升了性能。值得注意的是，2.0 Flash 在关键基准测试上甚至以两倍的速度超越了 1.5 Pro。2.0 Flash 还带来了新能力：除了支持图像、视频和音频等多模态输入之外，2.0 Flash 现在还支持多模态输出，包括与文本混合的原生生成图像，以及可控的多语言文本转语音（TTS）音频。它还能原生调用 Google 搜索、代码执行等工具，以及第三方用户自定义函数。

![比较各 Gemini 模型及其能力的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_benchmarks_narrow_light2x.gif)

我们的目标是安全、快速地把模型交到人们手中。过去一个月，我们一直在分享 Gemini 2.0 的早期实验版本，从开发者那里获得了极佳的反馈。

Gemini 2.0 Flash 现已作为实验模型通过 Gemini API 在 [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-2.0-flash-exp) 和 [Vertex AI](https://console.cloud.google.com/vertex-ai/studio/freeform?model=gemini-2.0-flash-exp) 上向开发者开放：多模态输入和文本输出对所有开发者可用，文本转语音和原生图像生成对早期访问合作伙伴开放。正式发布（GA）将在 1 月跟进，届时还会提供更多模型尺寸。

为帮助开发者构建动态交互式应用，我们同时发布了新的 Multimodal Live API，支持实时音频、视频流输入，并可以使用多个组合工具。关于 2.0 Flash 和 Multimodal Live API 的更多信息，请参阅我们的[开发者博客](https://developers.googleblog.com/en/the-next-chapter-of-the-gemini-era-for-developers/)。

### Gemini 2.0 登陆 Gemini 应用——我们的 AI 助手

同样从今天开始，全球的 [Gemini](https://gemini.google.com/) 用户都可以在桌面端和移动网页端的模型下拉菜单中选择经过聊天优化的 2.0 Flash 实验版，Gemini 移动应用也将很快支持。借助这一新模型，用户将体验到更加有帮助的 Gemini 助手。

明年初，我们将把 Gemini 2.0 扩展到更多 Google 产品。

## 用 Gemini 2.0 解锁智能体体验

Gemini 2.0 Flash 原生的用户界面操作能力，再加上多模态推理、长上下文理解、复杂指令遵循与规划、组合式函数调用、原生工具使用以及更低的延迟等改进，协同支撑起一整类全新的智能体体验。

AI 智能体的实际应用是一个充满激动人心可能性的研究领域。我们正通过一系列原型探索这一新前沿，帮助人们完成任务、把事情做成。这些原型包括：Project Astra 的更新版——我们探索通用 AI 助手未来能力的研究原型；全新的 Project Mariner——从你的浏览器开始探索人机智能体交互的未来；以及 Jules——一款可以帮助开发者的 AI 代码智能体。

我们仍处于开发的早期阶段，但我们很期待看到受信任测试者如何使用这些新能力，以及我们能从中学到什么，以便未来在产品中更广泛地提供这些能力。

## Project Astra：在真实世界中运用多模态理解的智能体

自我们在 I/O 大会上发布 [Project Astra](https://deepmind.google/technologies/gemini/project-astra/) 以来，我们一直在向在 Android 手机上使用它的受信任测试者学习。他们宝贵的反馈帮助我们更好地理解通用 AI 助手在实践中如何运作，包括对安全与伦理的影响。基于 Gemini 2.0 构建的最新版本包含以下改进：

- **更好的对话能力：** Project Astra 现在能够用多种语言以及混合语言进行对话，对口音和生僻词的理解也更好。
- **新的工具使用：** 借助 Gemini 2.0，Project Astra 可以使用 Google 搜索、Lens 和地图，在日常生活中作为助手更加有用。
- **更好的记忆：** 我们提升了 Project Astra 的记忆能力，同时让你保持掌控。它现在拥有长达 10 分钟的会话内记忆，并能记住更多你与它过去的对话内容，从而实现更贴合你个人的定制化。
- **更低的延迟：** 凭借新的流式处理能力和原生音频理解，该智能体能以接近人类对话的延迟理解语言。

我们正努力把这类能力引入 [Gemini](http://gemini.google.com/) 应用等 Google 产品——我们的 AI 助手——以及眼镜等其他硬件形态。我们也开始把受信任测试者计划扩展到更多人，其中一个小群体即将开始在原型眼镜上测试 Project Astra。

## Project Mariner：帮你完成复杂任务的智能体

Project Mariner 是一个基于 Gemini 2.0 构建的早期研究原型，从你的浏览器开始探索人机智能体交互的未来。作为研究原型，它能够理解并推理你浏览器屏幕上的信息，包括像素以及文本、代码、图像和表单等网页元素，然后通过一个实验性的 Chrome 扩展利用这些信息为你完成任务。

在测试智能体端到端真实网页任务表现的 [WebVoyager 基准测试](https://arxiv.org/abs/2401.13919)中，Project Mariner 以单智能体设置[取得了 83.5% 的最先进（state-of-the-art）成绩](http://deepmind.google/technologies/project-mariner)。

目前仍处于早期阶段，但 Project Mariner 表明，在浏览器内进行导航在技术上正变得可行——尽管它现在并不总是准确、完成任务的速度也较慢，这些都会随着时间迅速改善。

为了安全且负责任地构建这一能力，我们正针对新型风险与缓解措施开展积极研究，同时让人类始终在回路中。例如，Project Mariner 只能在你浏览器的活动标签页中输入、滚动或点击，并且在执行某些敏感操作（如购买商品）之前，会请求用户最终确认。

受信任测试者已开始通过实验性 Chrome 扩展测试 Project Mariner，与此同时，我们也在与网络生态展开对话。

## Jules：面向开发者的智能体

接下来，我们通过 Jules 探索 AI 智能体如何为开发者提供帮助——Jules 是一款实验性的 AI 代码智能体，可直接集成到 GitHub 工作流中。它可以在开发者的指导和监督下处理一个 issue、制定计划并执行计划。这一努力是我们长期目标的一部分：构建在包括编程在内的所有领域都有帮助的 AI 智能体。

关于这项持续进行的实验的更多信息，请参阅我们的[开发者博客文章](https://developers.googleblog.com/en/the-next-chapter-of-the-gemini-era-for-developers/)。

## 游戏及其他领域中的智能体

Google DeepMind 在利用游戏帮助 AI 模型更好地遵循规则、进行规划和逻辑推理方面有着[悠久](https://deepmind.google/discover/blog/agent57-outperforming-the-human-atari-benchmark/)[的历史](https://deepmind.google/research/breakthroughs/alphago/)。举例来说，就在上周，我们发布了 [Genie 2](https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/)——我们的 AI 模型，能够仅凭一张图像创造出无穷多样的可玩 3D 世界。延续这一传统，我们用 Gemini 2.0 构建了可以帮助你在电子游戏虚拟世界中导航的智能体。它能够仅凭屏幕上的动作对游戏进行推理，并在实时对话中给出下一步行动建议。

我们正在与 Supercell 等领先游戏开发商合作，探索这些智能体的工作方式，测试它们在从《部落冲突》（Clash of Clans）这样的策略游戏到《卡通农场》（Hay Day）这样的农场模拟器等各种游戏中解读规则和挑战的能力。

除了充当虚拟游戏伙伴之外，这些智能体甚至可以调用 Google 搜索，帮你连接网络上丰富的游戏知识。

除了在虚拟世界中探索智能体能力之外，我们还在试验能在物理世界中提供帮助的智能体，方法是将 Gemini 2.0 的空间推理能力应用于机器人技术。虽然仍处于早期，但我们对能在物理环境中提供协助的智能体的潜力感到兴奋。

你可以在 [labs.google](http://labs.google/) 上进一步了解这些研究原型和实验。

## 在智能体时代负责任地构建

Gemini 2.0 Flash 和我们的研究原型让我们得以在 AI 研究的最前沿测试并迭代新能力，这些能力最终将让 Google 产品更有帮助。

在开发这些新技术的过程中，我们认识到这带来的责任，以及 AI 智能体为安全与安保带来的诸多新问题。正因如此，我们采取探索性、渐进式的开发方式：对多个原型开展研究、迭代式地实施安全训练、与受信任测试者和外部专家合作，并进行广泛的风险评估以及安全与保障评测。

例如：

- 作为安全流程的一部分，我们与长期存在的内部审查机构——责任与安全委员会（Responsibility and Safety Committee，RSC）合作，识别并理解潜在风险。
- Gemini 2.0 的推理能力为我们 AI 辅助红队测试（red teaming）方法带来了重大进展，包括超越单纯的风险检测，能够自动生成评测数据和训练数据来缓解风险。这意味着我们可以更高效地大规模优化模型的安全性。
- 随着 Gemini 2.0 的多模态增加了潜在输出的复杂性，我们将继续针对图像和音频的输入与输出对模型进行评测和训练，以帮助提升安全性。
- 在 Project Astra 方面，我们正在探索针对用户无意间与智能体共享敏感信息的潜在缓解措施，并且已经内置了隐私控制，让用户可以轻松删除会话。我们还在继续研究如何确保 AI 智能体成为可靠的信息来源，不会代你采取意外的行动。
- 在 Project Mariner 方面，我们正努力确保模型学会优先考虑用户指令而非第三方的提示词注入（prompt injection）企图，从而识别来自外部来源的潜在恶意指令并防止滥用。这可以防止用户通过隐藏在电子邮件、文档或网站中的恶意指令遭受欺诈和钓鱼攻击。

我们坚信，构建 AI 的唯一方式就是从一开始就负责任。在推进模型与智能体的过程中，我们将继续把安全与责任作为模型开发流程的关键要素优先对待。

## Gemini 2.0、AI 智能体与更远的未来

今天的发布标志着 Gemini 模型的新篇章。随着 Gemini 2.0 Flash 的发布以及探索智能体可能性的一系列研究原型，我们已抵达 Gemini 时代一个激动人心的里程碑。在迈向通用人工智能（AGI）的构建过程中，我们期待继续安全地探索触手可及的一切新可能。
