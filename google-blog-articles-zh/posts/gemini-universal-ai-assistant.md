---
title: "我们构建通用 AI 助手的愿景"
title_en: "Our vision for building a universal AI assistant"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-universal-ai-assistant/
site: google-blog
date: 2025-05-20
crawled: 2026-09-13
translated: 2026-09-13
---

# 我们构建通用 AI 助手的愿景

> 原文：[Our vision for building a universal AI assistant](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-universal-ai-assistant/) · Google

过去十年里，我们为现代 AI 时代奠定了诸多基础：从开创所有大语言模型（LLM）赖以建立的 [Transformer](https://research.google/blog/transformer-a-novel-neural-network-architecture-for-language-understanding/) 架构，到开发出能够像 [AlphaGo](https://deepmind.google/research/breakthroughs/alphago/) 和 [AlphaZero](https://deepmind.google/research/breakthroughs/alphazero-and-muzero/?_gl=1*1pz0hjt*_up*MQ..*_ga*MTU3NjU3MjE3OC4xNzQ3MzA4NjIy*_ga_LS8HVHCNQ0*czE3NDczMDg2MjEkbzEkZzAkdDE3NDczMDkwMTIkajAkbDAkaDA.) 一样学习与规划的智能体系统。

我们运用这些技术在[量子计算](https://blog.google/technology/google-deepmind/alphaqubit-quantum-error-correction/)、[数学](https://deepmind.google/discover/blog/ai-solves-imo-problems-at-silver-medal-level/?_gl=1*1bl3hx2*_up*MQ..*_ga*MTU3NjU3MjE3OC4xNzQ3MzA4NjIy*_ga_LS8HVHCNQ0*czE3NDczMDg2MjEkbzEkZzAkdDE3NDczMDkzMzYkajAkbDAkaDA.)、[生命科学](https://deepmind.google/discover/blog/alphaproteo-generates-novel-proteins-for-biology-and-health-research/?_gl=1*1dmnab3*_up*MQ..*_ga*MTU3NjU3MjE3OC4xNzQ3MzA4NjIy*_ga_LS8HVHCNQ0*czE3NDczMDg2MjEkbzEkZzAkdDE3NDczMDk0NjEkajAkbDAkaDA.)和[算法发现](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/?_gl=1*16es8jk*_up*MQ..*_ga*MTU3NjU3MjE3OC4xNzQ3MzA4NjIy*_ga_LS8HVHCNQ0*czE3NDczMDg2MjEkbzEkZzAkdDE3NDczMDkzMzQkajAkbDAkaDA.)方面取得了突破。我们将继续在基础研究的广度和深度上加倍投入，努力发明通往通用人工智能（AGI）所必需的下一个重大突破。

正因如此，我们正致力于把最优秀的多模态基础模型 Gemini 2.5 Pro 扩展为一个"世界模型"（world model）——像大脑那样，通过理解和模拟世界的方方面面来制定计划并构想新的体验。

在这个方向上，我们早已迈出坚实步伐：从训练智能体掌握围棋（Go）和《星际争霸》（StarCraft）等复杂游戏的开拓性工作，到构建 [Genie 2](https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/)——它仅凭一张图像提示，就能生成可交互的 3D 模拟环境。

如今，我们已经能看到这些能力涌现的证据：Gemini 能够运用世界知识与推理来表征和[模拟自然环境](https://www.youtube.com/watch?v=zvouDoWL6fk)；[Veo](https://deepmind.google/technologies/veo/veo-2/?_gl=1*69oxzg*_up*MQ..*_ga*MTU3NjU3MjE3OC4xNzQ3MzA4NjIy*_ga_LS8HVHCNQ0*czE3NDczMTg1MzMkbzMkZzAkdDE3NDczMTg1MzMkajAkbDAkaDA.) 对直觉物理的深刻理解；以及 [Gemini Robotics](https://deepmind.google/technologies/gemini-robotics/?_gl=1*6jv8a4*_up*MQ..*_ga*MTU3NjU3MjE3OC4xNzQ3MzA4NjIy*_ga_LS8HVHCNQ0*czE3NDczMTg1MzMkbzMkZzAkdDE3NDczMTg3ODAkajAkbDAkaDA.) 教会机器人抓取物体、遵循指令并即时调整的方式。

让 Gemini 成为世界模型，是开发一种更新、更通用、更有用的 AI——通用 AI 助手（universal AI assistant）——的关键一步。这样的 AI 是智能的，理解你所处的上下文，并能在任何设备上代表你进行规划并采取行动。

## 把 Project Astra 的实时能力带入我们的产品

我们的终极愿景是把 [Gemini 应用](https://blog.google/products/gemini/gemini%E2%80%93app-updates-io-2025)转变为一个通用 AI 助手：它将替我们完成日常事务，打理繁琐的杂务，并带来令人惊喜的新推荐——让我们更高效，也让生活更丰富多彩。

这一切始于我们去年在研究原型 [Project Astra](https://deepmind.google/technologies/project-astra/?_gl=1*1ueecac*_up*MQ..*_ga*MjU3NzU4MzA2LjE3NDU4NTM0ODU.*_ga_LS8HVHCNQ0*MTc0NTg1MzQ4Mi4xLjAuMTc0NTg1MzQ4OS4wLjAuMA..) 中率先探索的能力，例如视频理解、屏幕共享和记忆。

过去一年，我们一直在把这类能力整合进 [Gemini Live](https://gemini.google/overview/gemini-live/?hl=en)，让更多人今天就能体验到。我们继续不懈地改进，并在前沿探索新的创新。例如，我们借助原生音频（native audio）将语音输出升级得更加自然，改进了记忆功能，并增加了计算机控制。

目前，我们正从受信任的测试者那里收集关于这些能力的反馈，并致力于将它们带入 [Gemini Live](https://gemini.google/overview/gemini-live/?hl=en)、[Search](https://blog.google/products/search/google-search-ai-mode-update/) 中的新体验、面向开发者的 [Live API](https://ai.google.dev/gemini-api/docs/live)，以及眼镜等新形态设备。

在这个过程的每一步中，安全与责任都是我们工作的核心。我们最近开展了一项大型研究项目，探讨[先进 AI 助手所涉及的伦理问题](https://deepmind.google/discover/blog/the-ethics-of-advanced-ai-assistants/)，这项工作将继续为我们的研究、开发和部署提供指导。

## 构建能为你同时处理多项任务的 AI

我们还通过 [Project Mariner](https://deepmind.google/project-mariner) 探索智能体能力如何帮助人们并行处理多项任务。这是一个研究原型，从浏览器入手，探索人与智能体交互的未来。

自[去年 12 月](https://blog.google/technology/google-deepmind/google-gemini-ai-update-december-2024/#project-mariner)发布 Project Mariner 以来，我们一直与一组受信任的测试者紧密合作，收集反馈并改进其实验性能力。

更新后的 Project Mariner 现在包含一个智能体系统，一次最多可以完成十项不同的任务。这些智能体可以帮你查找信息、进行预订、购物、做调研等等——全部同时进行。

更新版 Project Mariner 已面向美国的 [Google AI Ultra](https://blog.google/products-and-platforms/products/google-one/google-ai-ultra/) 订阅用户开放。我们正把它的计算机操作能力引入 [Gemini API](https://ai.google.dev/)，并计划在今年之内把它的更多能力带给 Google 产品。欲详细了解我们在 [Search](https://blog.google/products/search/google-search-ai-mode-update) 和 [Gemini 应用](https://blog.google/products/gemini/gemini%E2%80%93app-updates-io-2025)中的智能体能力，请阅读更多内容。

依托这项工作以及我们所有的开创性成果，我们正在构建更个性化、更主动、更强大的 AI——丰富我们的生活，加快科学进步的步伐，并开启一个充满发现与奇迹的新黄金时代。
