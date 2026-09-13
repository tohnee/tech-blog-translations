---
title: "Deep Research Max：自主研究智能体的跨越式升级"
title_en: "Deep Research Max: a step change for autonomous research agents"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/next-generation-gemini-deep-research/
site: gemini
date: 2026-04-21
crawled: 2026-09-13
translated: 2026-09-13
---

# Deep Research Max：自主研究智能体的跨越式升级

> 原文：[Deep Research Max: a step change for autonomous research agents](https://blog.google/innovation-and-ai/models-and-research/gemini-models/next-generation-gemini-deep-research/) · Google

[去年 12 月](https://blog.google/innovation-and-ai/technology/developers-tools/deep-research-agent-gemini-api/)，我们通过 [Interactions API](https://blog.google/technology/developers/interactions-api) 向开发者开放了 Gemini Deep Research 智能体，让开发者得以使用 Google 最先进的自主研究能力。今天，我们通过自主研究智能体的两个新版本把这些能力推向新的高度：Deep Research 和 Deep Research Max。

随着我们最先进的模型 Gemini 3.1 Pro 的集成，Deep Research 已经从一个精密的摘要引擎，蜕变为横跨金融、生命科学、市场研究等领域的企业级工作流基础。Deep Research 的报告本身就有价值，同时也常常作为复杂智能体化管线的第一步——这类管线往往始于深入的背景信息收集。现在，开发者只需一次 API 调用，就能触发穷尽式的研究工作流，首次把开放网络与自有的专有数据流融合起来，交付专业级、带完整引用的分析。

## 选择契合你工作流的研究配置

在 Gemini Deep Research 初次发布的基础上，我们推出两个定位不同的智能体，覆盖从直接的用户辅助到大规模离线研究流程的各类需求：

- **Deep Research：**为速度和效率优化，这个新智能体取代了我们 12 月的预览版本，在更高质量水平上大幅降低了延迟和成本。对于直接集成到交互式用户界面、需要低延迟的研究体验而言，它是理想的智能体。
- **Deep Research Max：**为最大限度的全面性和最高质量的综合而设计，Max 利用扩展的测试时计算（test-time compute）来迭代式地推理、搜索并打磨最终报告。它是异步后台工作流的完美引擎——比如一个夜间定时任务，在早晨之前为分析师团队生成穷尽式的尽职调查报告。

Deep Research Max 在追踪检索与推理能力的行业标准基准测试上实现了性能跃升。

![Deep Research Max 在追踪检索与推理能力的行业标准基准测试上实现了性能跃升。](https://storage.googleapis.com/gweb-uniblog-publish-prod/documents/gemini-3.1-pro_deep-research-and-max_blog_evals.png)

## 解锁专有数据与丰富的原生可视化

Deep Research 现在可以搜索网络、任意远程 MCP、上传的文件和已连接的文件存储——或它们的任意组合，带来专为专业人士日常依赖的复杂、受权限管控的数据世界而设计的能力。

- **模型上下文协议（MCP）支持：**你现在可以通过 MCP 安全无缝地把 Deep Research 连接到你的自定义数据和专业化数据流（例如金融或市场数据提供商）。Deep Research 支持任意的工具定义，这把它从一台网络搜索器转变为能够驾驭任何专业数据仓库的自主智能体。
- **原生图表和信息图：**这是 Deep Research 在 Gemini API 中的首次：我们的智能体不再只是生成文本，而是原生地生成高质量图表和信息图，内嵌于 HTML 或借助 [Nano Banana](https://blog.google/innovation-and-ai/technology/ai/nano-banana-2/)，动态可视化复杂的数据集，丰富分析报告。

![法定货币的赢家与输家：兑美元的同比表现（2025 年 4 月 - 2026 年 4 月）](https://storage.googleapis.com/gweb-uniblog-publish-prod/documents/visual_1.png)

Deep Research 原生生成的丰富视觉元素，把复杂的定性与定量数据流转化为可直接用于演示的图表和信息图。

![FIG 格局无法暂停的四年时钟](https://storage.googleapis.com/gweb-uniblog-publish-prod/documents/visual_2.png)

Deep Research 原生生成的丰富视觉元素，把复杂的定性与定量数据流转化为可直接用于演示的图表和信息图。

![支付基础设施主导欧洲金融科技的资本配置](https://storage.googleapis.com/gweb-uniblog-publish-prod/documents/visual_3.png)

Deep Research 原生生成的丰富视觉元素，把复杂的定性与定量数据流转化为可直接用于演示的图表和信息图。

![全球能源贸易格局重塑：主要海上绕行航线（2024-2026）](https://storage.googleapis.com/gweb-uniblog-publish-prod/documents/visual_4.png)

Deep Research 原生生成的丰富视觉元素，把复杂的定性与定量数据流转化为可直接用于演示的图表和信息图。

我们还扩展了智能体的能力，让研究过程拥有更多控制力和透明度：

- **协作式规划：**在智能体开始执行之前，审查、引导并打磨它生成的研究计划，对调查范围实现精细化控制。
- **扩展工具集：**组合使用 Gemini API 的全套工具。让 Deep Research 同时使用 Google Search、远程 MCP 服务器、URL Context、代码执行和文件搜索——或者彻底关闭网络访问，只在你的自定义数据上进行搜索。
- **多模态研究锚定：**提供 PDF、CSV、图像、音频和视频的组合作为输入，把智能体的研究锚定在你的自定义上下文之中。
- **实时流式输出：**通过实时思考摘要追踪智能体的中间推理步骤，并在文本和图像输出生成的同时接收它们，这对交互式用户界面尤其有用。

## 用专家级分析驱动真实世界的成果

Deep Research Max 以比以往更低的价格、更高的效率，交付高度全面的报告、严谨的事实性和专家级分析。与我们 12 月的版本相比，Deep Research Max 咨询的来源显著更多，并能识别旧版本经常忽略的关键细微差别。我们还着力教 Deep Research 咨询多样化的来源，并仔细权衡相互冲突的证据。最终产出的是一份细致入微的报告：它引用 SEC 文件和开放获取的同行评审期刊等权威来源，条理清晰地呈现信息，并把密集的技术数据转化为可执行、可直接呈交利益相关方的格式。

![Deep Research 4/26 与 Deep Research 12/25 在内部 Deep Research 专家评测上的胜率对比](https://storage.googleapis.com/gweb-uniblog-publish-prod/documents/gemini-3.1-pro_deep-research-qualitative-advacements_blog_evals.png)

为了确保这项技术能带来真实世界的成果，我们正在与专业化和受监管领域的初创公司和企业紧密合作——这些领域几乎没有出错的余地，尤其是金融和生命科学。例如，我们正在积极与 [FactSet](https://www.factset.com/)、[S&P Global](https://www.spglobal.com/ratings/en) 和 [PitchBook](https://pitchbook.com/) 合作设计它们的 MCP 服务器，让共同的客户能把金融数据产品集成到由 Deep Research 驱动的工作流中，并让它们借助以闪电速度从其穷尽式数据世界中收集上下文的能力，实现生产力的跃升。

## 利用经过验证的 Google 规模化性能

当你使用 Deep Research 智能体进行构建时，你接入的是同一套自主研究基础设施——它支撑着 Google 一些最受欢迎产品中的研究能力，例如 [Gemini 应用](https://gemini.google/overview/deep-research/)、[NotebookLM](https://blog.google/technology/google-labs/notebooklm-deep-research-file-types/)、[Google Search](https://blog.google/products/search/google-search-ai-mode-update/#deep-search) 和 [Google Finance](https://blog.google/products/search/new-google-finance-ai-deep-search/)。

## 通过 Interactions API 开始使用 Deep Research

Deep Research 和 Deep Research Max 从今天起通过 Gemini API 的付费档以公开预览版提供。前往我们的[开发者文档](https://ai.google.dev/gemini-api/docs/deep-research)，开始使用 [Interactions API](https://blog.google/technology/developers/interactions-api) 构建 Deep Research 应用。Deep Research 和 Deep Research Max 不久后也将通过 Google Cloud 面向初创公司和企业开放。
