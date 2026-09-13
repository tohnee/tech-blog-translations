---
title: "Gemini 3.7 Flash 现已发布"
title_en: "Introducing Gemini 3.7 Flash"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/
site: gemini
date: 2026-08-13
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini 3.7 Flash 现已发布

> 原文：[Introducing Gemini 3.7 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/) · Google

今天，我们在广受欢迎的 Flash 系列基础上更进一步，推出 Gemini 3.7 Flash——迄今我们在编程与智能体方面最智能的主力模型。

本次发布距离 [Gemini 3.6 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/) 仅三周，它直接源自开发者的反馈和算法创新，我们期待把这些成果带到未来的模型中。3.7 Flash 在软件工程、知识工作和 Web 开发工作流上都带来大幅提升——而入门定价仅为原 3.6 Flash 每百万 token 价格的一半。

## 为复杂工作流带来更强的智能

![展示生产级代码质量的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__evals__frontier.width-100.format-webp.webp)

![展示长程软件工程的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__evals__deepswe-.width-100.format-webp.webp)

![展示 Web 开发的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__evals__codearen.width-100.format-webp.webp)

![展示专家级 PDF 文档理解的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__evals__gdp-pdf_.width-100.format-webp.webp)

![展示企业工作流自动化的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__evals__automati.width-100.format-webp.webp)

3.7 Flash 在调试和问题解决等编程任务上相较 3.6 Flash 展现出显著提升。它实现了更高的一次通过代码准确率，并在生成生产级代码方面表现更佳：在 [FrontierCode 1.1 Main](https://cognition.com/frontiercode) 上为 43.6% 对 34.4%，在 [DeepSWE v1.1](https://deepswe.datacurve.ai/) 上为 65.3% 对 49.0%。

在 Web 开发方面，3.7 Flash 用更少的提示词就能生成更实用的布局和功能完备的应用。对于 UI 生成，无论参考输入是截图、图像还是完整的设计系统，该模型都展现出高度的设计还原度与一致性。在 Arena.ai 的 [WebDev Arena](https://arena.ai/leaderboard/code/webdev) 上，它以 1588 对 1538 的 Elo 分数超越 3.6 Flash。

在金融、法律和生物科学等知识密集领域，3.7 Flash 带来了更强的推理能力和准确度。在用于测试模型处理复杂文档能力的 GDP.pdf 基准上，它大幅超越 3.6 Flash（34.0% 对 22.0%）。在 [AutomationBench](https://zapier.com/blog/introducing-automationbench/) 上它也超过了 3.6 Flash，证明它能更有效地完成真实世界的业务工作流（30.4% 对 17.0%）。

从一条简单的文本提示词到一款完全可玩的 3D 游戏。我们使用 Gemini 3.7 Flash 结合 Nano Banana，实时动态生成角色、道具和纹理。

一次生成、令人惊艳的交互式落地页。我们用 Gemini 3.7 Flash 编排子智能体，并借助 Gemini Omni 创建流畅的交互式视差组件。

一个机器人模型正在用 Gemini 3.7 Flash 训练，通过三智能体图循环利用多模态理解，帮助机器人更快地学习。

从静态 PDF 到交互式数据故事。看看复杂的年报如何被转化为配有实时图表和汇总洞察的引人入胜的网页体验。

## 更好的开发者体验与价格

相较 3.6 Flash，Gemini 3.7 Flash 带来了明显改善的开发者体验。它能更好地应对障碍、在需要时澄清意图，并以更高的保真度遵循指令。它思考得更勤勉，在多步规划和工具调用上投入更多努力。更严谨的执行意味着在工程工作流中需要更少的人工干预和更少的重试。

3.7 Flash 以入门价
[1](#footnote-1)
提供至今年年底：每百万输入 token 0.75 美元、每百万输出 token 3.75 美元。这一价格结合增强的模型性能，让开发者和客户能够以高性价比扩展生产级智能体。

![性能与成本对比图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__evals__perform.width-1200.format-webp.webp)

早期客户反馈重点强调了 3.7 Flash 的性能与精确度：在低成本下取得了显著优于 3.6 Flash 的结果。

![来自 Box 的引言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__bo.width-100.format-webp.webp)

![来自 Browser Use 的引言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__br.width-100.format-webp.webp)

![来自 Cartwheel 的引言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__ca.width-100.format-webp_dYz0MOf.webp)

![来自 databricks 的引言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__da.width-100.format-webp.webp)

![来自 emergent 的引言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__em.width-100.format-webp.webp)

![来自 Harvey 的引言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__ha.width-100.format-webp_NtGWF6a.webp)

![来自 Hebbia 的引言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__he.width-100.format-webp_H9baWpR.webp)

![来自 LangChain 的引言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__la.width-100.format-webp_7qAt1Kr.webp)

![来自 Nunu.ai 的引言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__nu.width-100.format-webp_DyOGCzR.webp)

![来自 Open Code 的引言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__op.width-100.format-webp_wy8PPtG.webp)

![来自 Pydantic 的引言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__py.width-100.format-webp.webp)

![来自 Stanford Department of Biology 的引言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__testimonial__st.width-100.format-webp_AzDrTOJ.webp)

## 用 3.7 Flash 改进 Gemini Spark

Gemini Spark 面向 [160 多个国家](https://support.google.com/gemini/answer/17094507?hl=en&co=GENIE.Platform%3DAndroid&sjid=2353166824601345951-NA#:~:text=Available%20wherever%20Gemini%20Apps%20are%20supported%2C%20except%20in%20the%20European%20Economic%20Area%2C%20Nigeria%2C%20Switzerland%2C%20and%20the%20United%20Kingdom)的 Google AI Pro 和 Ultra 订阅用户开放，从今天起将使用 Gemini 3.7 Flash。我们在 I/O 大会上发布了 Spark，它是全天候（24/7）运行的个人 AI 智能体，在你的指挥下代你采取行动。这次模型更新让 Spark 在知识工作上更高效，改进了对 Google Workspace 应用的工具使用，为复杂的多技能工作流带来更高的准确度和输出质量。

借助 3.7 Flash，Gemini Spark 可以更高效地把想法变成行动：整合文件、起草邮件、更新进度文档。

## 以安全为本的构建

我们持续提升[前沿安全防护措施](https://deepmind.google/frontier-safety/)的覆盖面与鲁棒性。Gemini 3.7 Flash 随附更新的防护措施，防范化学、生物、放射与核（CBRN）领域及网络攻击方面的滥用，同时支持有益的使用场景，符合[我们的生物韧性方针](https://deepmind.google/blog/our-approach-to-bioresilience/)和我们的[网络安全计划](https://deepmind.google/blog/introducing-gemini-3-5-flash-cyber/)。

更多信息请参阅 3.7 Flash 的[模型卡](https://deepmind.google/models/model-cards/gemini-3-7-flash)。

## 立即试用

- **开发者**：在 [Google Antigravity](https://antigravity.google/) 中探索智能体优先的工作流，或立即通过 [Google AI Studio](https://ai.dev/prompts/new_chat?model=gemini-3.7-flash) 和 [Android Studio](https://developer.android.com/studio) 在 Gemini API 中开始构建。请从我们的[开发者指南](https://ai.google.dev/gemini-api/docs/latest-model)入手。
- **企业**：在 [Gemini Enterprise Agent Platform](https://console.cloud.google.com/agent-platform/publishers/google/model-garden/gemini-3.7-flash) 和 [Gemini Enterprise](https://cloud.google.com/gemini-enterprise?e=48754805) 应用中使用 3.7 Flash。
- **个人用户**：通过 Spark 使用——它是 Gemini 应用中全天候的个人智能体，面向[受支持国家](https://support.google.com/gemini/answer/17094507?hl=en&co=GENIE.Platform%3DAndroid&sjid=2353166824601345951-NA#:~:text=Available%20wherever%20Gemini%20Apps%20are%20supported%2C%20except%20in%20the%20European%20Economic%20Area%2C%20Nigeria%2C%20Switzerland%2C%20and%20the%20United%20Kingdom)的 Google AI Pro 和 Ultra 订阅用户开放。

## 详细基准测试

![展示 AI 模型基准测试成绩的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-7-flash__evals__benchma.width-1200.format-webp.webp)
