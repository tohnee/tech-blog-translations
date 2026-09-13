---
title: "推出 Gemini 3.5 Flash 中的计算机操作能力"
title_en: "Introducing computer use in Gemini 3.5 Flash"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-computer-use-gemini-3-5-flash/
site: gemini
date: 2026-06-24
crawled: 2026-09-13
translated: 2026-09-13
---

# 推出 Gemini 3.5 Flash 中的计算机操作能力

> 原文：[Introducing computer use in Gemini 3.5 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-computer-use-gemini-3-5-flash/) · Google

计算机操作（computer use）现在是 Gemini 3.5 Flash 支持的内置工具，为我们迄今为止的智能体计算机操作任务带来最佳性能。此前它只能作为独立的 [Gemini 2.5 computer use 模型](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-computer-use-model/)使用，如今计算机操作已原生集成到主 Gemini Flash 模型中。Gemini 本就擅长函数调用以及使用 Search 和 Maps 锚定（grounding）等内置工具。有了内置的计算机操作能力，开发者现在可以使用 3.5 Flash 可靠地构建自定义智能体，让它们能在浏览器、移动和桌面环境中观察、推理并采取行动。这为长时程和企业自动化任务——如持续软件测试和专业应用中的知识工作——解锁了更出色的性能。

![Gemini 3.5 基准测试](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-5__benchmark-OSWorld-Ve.width-1200.format-webp.webp)

开发者和企业可以通过 [Gemini API](https://ai.google.dev/gemini-api/docs/computer-use) 和 [Gemini Enterprise Agent Platform](https://console.cloud.google.com/projectselector2/agent-platform/overview?pli=1&supportedpurview=project) 开始在 3.5 Flash 中使用计算机操作。

3.5 Flash 使用计算机操作来分析 Gemini 应用，并返回一份分类的功能清单。

启用计算机操作的 3.5 Flash 对自己的文档进行无障碍问题审查。

## 让计算机操作在 3.5 Flash 中安全运行

为了缓解智能体在真实环境中运行所面临的部分提示词注入风险，我们对 Gemini 3.5 Flash 的计算机操作能力使用了有针对性的对抗训练。我们还在发布两个可选的企业级防护系统，让企业能够：

- 要求对敏感或不可逆的操作进行明确的用户确认。
- 在识别到间接提示词注入时自动停止任务。

秉持「纵深防御」的思路，我们鼓励开发者将这些功能与安全的沙箱、人在回路的验证以及严格的访问控制结合使用。关于安全措施的更多信息，请参阅我们的[最佳实践](https://ai.google.dev/gemini-api/docs/computer-use#safety-best-practices)文档。

我们已经看到客户借助计算机操作创造了价值。以下是其中一些客户的评价：

![来自 Browserbase 的 Migual Gonzalez Fernandez 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Gemini_3.5_Flash_BrowserBase_v2.width-100.format-webp.webp)

![来自 Browser Use CEO Magnus Muller 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Gemini_3.5_Flash_Browser_Use_1.width-100.format-webp.webp)

![来自 UIPath 高级总监 Alvin Stanescu 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Gemini_3.5_Flash_UiPath_v3.width-100.format-webp.webp)

立即开始用计算机操作进行构建：

- **立即试用**：在 [Browserbase 托管的演示环境](http://gemini.browserbase.com/)中测试各项能力。
- **开始构建**：深入研究我们的[参考实现](https://github.com/google-gemini/computer-use-preview)与文档，包括 [Gemini API](https://ai.google.dev/gemini-api/docs/interactions/computer-use) 和 [Gemini Enterprise Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/computer-use)。
