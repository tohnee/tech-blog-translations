---
title: "保障 AI 智能体的未来安全"
title_en: "Securing the future of AI agents"
source: https://deepmind.google/blog/securing-the-future-of-ai-agents/
site: deepmind
date: 2026-06-18
crawled: 2026-09-13
translated: 2026-09-13
---

# 保障 AI 智能体的未来安全

> 原文：[Securing the future of AI agents](https://deepmind.google/blog/securing-the-future-of-ai-agents/) · Google DeepMind

我们如何保护内部系统免受能力日益增强、对齐尚不完善的 AI 的威胁

AI 智能体正在改变我们与技术的关系。通过自主执行复杂任务——从网络防御到科学发现再到产品开发——这些系统正在开启一个全新的生产力时代。仅在美国，到 2030 年 AI 智能体就可能创造 2.9 万亿美元的[经济价值](https://www.mckinsey.com/mgi/our-research/agents-robots-and-us-skill-partnerships-in-the-age-of-ai#/)。

随着这些智能体能力的增强，它们也需要更精密的防护措施。正因如此，我们制定了[AI Control Roadmap](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/securing-the-future-of-ai-agents/gdm-ai-control-roadmap.pdf)：一个用于构建和管理我们在 Google 内部部署的先进 AI 的框架。这种「纵深防御」方法可以作为整个行业的范本，它超越了传统的模型对齐，增加了一层关键的系统级安全保障，即使对齐并不完善也能提供保证。

## 理解 AI Control

我们的安全方法始于坚实的基础，融合了沙箱、终端安全、抗提示词注入等传统防护措施。在此基础上，AI Control Roadmap 将模型对齐（即训练 AI 使其本质上安全且有用）作为第一道防线。它提供了额外的安全层：把内部智能体视为潜在未对齐的对象来对待，从而即使对齐不完善也能提供保证。

可以把它想象成配有双重控制装置的驾驶教练。教练信任学员，但随时准备在出现失误时接管方向盘或踩下刹车。类似地，我们的 AI 控制系统根据智能体经过验证的行为授予其权限，让我们能够通过受控的、渐进式的访问来建立信任。

我们的路线图建立在一个简单而审慎的假设之上：如果一个能力很强的 AI 智能体与我们的目标不一致、并做出意想不到的行为怎么办？为应对这一点，我们的计划聚焦于三个关键领域。

首先，遵循网络安全的最佳实践，我们为 AI 开发了一个新颖的威胁建模框架。该路线图将不受信任的 AI 智能体视为潜在的「内部威胁」——就像公司对待一个已经拥有办公室门禁权限的潜在不良员工那样。通过构建在行业标准 [MITRE ATT&CK](https://attack.mitre.org/) 框架（一个基于真实世界观察、全球可访问的对手战术与技术知识库）之上，我们将潜在攻击拆解为更小的战术与技术。这使我们能够有条理地跟踪风险，在不良行为造成损害之前发现它，并安全地开展演练以检验我们的防御是否真正有效。

其次，我们制定了一个部署 AI 控制缓解措施来应对这些风险的计划。

- 识别问题（检测）：监控是 AI 控制的支柱。我们使用其他可信的 AI 系统作为「监督者」，持续审查工作智能体的推理、行动和计划，判断它是否偏离轨道。
- 管理问题（预防与响应）：如果监督者发现智能体试图做有害的事情，它可以在损害发生之前介入并阻止该行为。

最后，为确保我们的系统切实有效，我们持续衡量三项关键指标的表现：覆盖率（被监控流量的比例）、召回率（被捕获的未对齐行为比例）以及响应时间。

## 随 AI 变得更聪明而同步扩展安全

随着 AI 模型不断进步，我们的防御也必须同步加强。在 AI Control Roadmap 中，我们将安全协议映射到 AI 能力在两个关键前沿上的可衡量里程碑：

- **规避检测的能力：** 如今，我们监控模型可见的思维链（chain-of-thought）。然而，随着模型学会隐藏自己的推理——无论是通过*监督觉察*（oversight awareness，知道自己正被监控）还是*不透明推理*（opaque reasoning，不借助可见文本进行推理）——仅仅读取它们用语言表达出来的推理将不再足够。我们将需要分析它们的行为，并可能需要检查模型的内部运作。
- **造成潜在危害的能力：** 对于低风险且可逆的操作，我们可以依赖带延迟的记录审查并在问题发生后快速补救（异步响应）。对于特别高风险的操作，例如重大网络攻击，我们必须转向实时预防，在有害行为被执行之前将其阻止（同步响应）。换言之，我们的响应策略必须随威胁的严重程度而升级。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

AI Control Roadmap 根据部署模型的能力推荐安全措施。模型的检测规避能力决定检测等级（D1-D4），模型的攻击执行能力决定预防与响应等级（R1-R3）。

## 分析一百万条智能体轨迹以支撑实时监控

要构建这些系统，我们需要数据。我们的团队构建了一个异步监控系统的内部原型，用于审查编码智能体的轨迹，并将发现升级给人工审查。每一个被标记的事件都会按照我们路线图中的威胁分类法进行归类。

我们已经分析了一百万个编码智能体任务，这为我们完善安全协议提供了宝贵洞察，并使我们能够超越简单的关键词过滤，转向识别高信号的行为模式。例如，这项研究对为 Gemini Spark 智能体构建实时监控器起到了关键作用，使我们能够实时响应新出现的问题，例如意外删除数据。

需要指出的是，我们的数据显示，大多数被标记的事件并非源于对抗性意图；相反，它们往往源于[智能体对用户目标的误解或过度积极](https://arxiv.org/abs/2605.30322)。理解这些细微差别对于完善我们的安全与保障协议至关重要。

## 守护智能体生态是共同的责任

AI Control Roadmap 是我们智能体安全多层方法中的一个关键要素。通过将这些协议与我们更广泛的基础设施相集成，我们正在扩展内部安全体系，以安全地管理我们最先进的 AI 模型。

此外，这种多层智能体安全方法应成为行业、政策制定者和学术界协作推进的优先事项。通过围绕最佳实践和标准对齐整个生态，我们可以赋能网络防御者并构建社会韧性。正因如此，今天我们还为政策制定者发布了一份技术框架：[「Three Layers of Agent Security」](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/securing-the-future-of-ai-agents/three-layers-of-agent-security.pdf)。该论文详述了我们如何需要在单个智能体层面、多智能体系统中改进安全性，以及如何赋能网络防御者并在更广泛的生态中构建韧性。

我们打算在这些框架的基础上继续推进，以便在今天自信地部署能力强大的 AI，同时继续为未来构建安全的基础。

在此阅读完整技术报告：

[AI Control Roadmap](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/securing-the-future-of-ai-agents/gdm-ai-control-roadmap.pdf)

### 研究作者

Mary Phuong, Erik Jenner, Laurent Simon, Lewis Ho, Rohin Shah, Sebastian Farquhar, and Scott Coull.

### 致谢

Four Flynn, Anca Dragan, Alan Cooney, Bilal Chughtai, Buck Shlegeris, Cody Wild, David Lindner, Julian Stastny, Kevin Klyman, Li Ding, Myriam Khan, Raluca Ada Popa, Roland Zimmermann, Ryan Greenblatt, Senthooran Rajamanoharan, Victoria Krakovna and Xerxes Dotiwalla.
