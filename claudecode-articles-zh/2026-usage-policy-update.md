---
title: "2026 Usage Policy 更新"
title_en: "2026 Usage Policy update"
source: https://www.anthropic.com/news/2026-usage-policy-update
published: 2026-10-08
crawled: 2026-10-26
translated: 2026-10-26
---

# 2026 Usage Policy 更新

> 原文：[2026 Usage Policy update](https://www.anthropic.com/news/2026-usage-policy-update) · Anthropic News

# 2026 Usage Policy 更新

* 发布时间

  2026 年 10 月 8 日
* 分类

  [政策](/news/policy)
* 主题

  + [滥用限制](/search?topic=limits-on-abuse)
  + [民主诚信](/search?topic=democratic-integrity)
  + [防护措施](/search?topic=safeguards)
  + [威胁情报](/search?topic=threat-intelligence)
  + [模型福利](/search?topic=model-welfare)
  + [机器人技术](/search?topic=robotics)查看更多...

相关文章

* 安全

  2026 年 9 月 10 日

  [检测与打击 AI 滥用：2026 年 9 月](/threat-intelligence-report-september-2026)

[查看更多](/search?topic=limits-on-abuse)

Anthropic 每年都会根据我们模型能力的演进，以及收到的客户反馈来更新其 Usage Policy（《使用政策》）。我们今天发布了该政策的新版本，本文将概述我们所做的修改。

最新版本中的大部分更新旨在澄清现有规则。自上次修订以来的这一年里，Claude 已经开始承担更长周期、更加独立的工作。本次更新补充了新的示例，说明我们的规则如何适用于 Claude 的新能力，并参考了过去一年我们观察到的有关影响力行动、武器开发和监控的新型滥用模式（相关内容已记录在我们的[最新威胁情报报告](https://www.anthropic.com/threat-intelligence-report-september-2026)中）。我们还对以下方面进行了更新：澄清健康和金融等领域高风险用例的要求；为 Claude 被用于自主采取物理行动的场景增加管控措施；以及处理针对我们模型的辱骂行为。

更新后的政策将于 11 月 12 日生效。完整的 [Usage Policy](https://www.anthropic.com/legal/aup)（《使用政策》）与 [Supported Regions Policy](https://www.anthropic.com/supported-countries)（《支持地区政策》）可在各自页面查阅。

### 新增欺骗性活动章节

正如我们[上个月所报道](https://www.anthropic.com/threat-intelligence-report-september-2026)的，我们已看到官方媒体机构、政府宣传部门以及商业公司利用 Claude 运营虚假账号网络和伪造新闻网站的实例。我们的政策此前已禁止此类活动，但相关限制散见于选举、欺诈、隐私和虚假信息等章节之中。

我们已将这些规则整合到一个新章节中，标题为「不得从事欺骗性行动或人为虚假活动」（Do Not Engage in Deceptive Campaigns or Artificial Activity），适用于任何类型的欺骗性活动（无论政治性还是商业性）。该章节涵盖隐藏信息背后真实发布者的行为、通过虚假账号或帖子放大内容的行为，以及构建用于开展影响力行动的工具和基础设施的行为。

### 重新聚焦选举章节

在 Usage Policy 的每个版本中，我们都不断打磨对政治内容的限制，以确保我们的模型能够在民主进程中被恰当使用。本版本进一步收紧了选举章节，将其明确聚焦于禁止利用 Claude 欺骗选民或干扰选举（例如，散布有关候选人或投票方式的虚假信息、冒充候选人或选举官员，或试图压低投票率）。为体现这一范围，我们将其更名为「不得破坏民主进程」（Do Not Undermine Democratic Processes）。

出于类似原因，我们还移除了对个性化投票宣传与竞选定向投放的一刀切禁令。该禁令原本覆盖了一些正当的公民工作，例如非营利组织利用 Claude 为选民撰写其他语言的信息，或选举官员发送选票补正通知。当初制定该规则所针对的行为（例如依赖欺骗手段或滥用选民个人数据的选民定向投放），在我们的欺骗性行动、监控和隐私章节下仍属禁止。

### 澄清武器禁令

我们的 Usage Policy 一直禁止利用 Claude 开发武器。近期，我们发现有人试图利用我们的模型为武器构建制导与控制软件。更新后的章节明确：我们的禁令涵盖使武器得以运作的软件和部件，以及为无人机和其他自主载具装配武器等行为。这些改动反映的正是我们对此前政策的实际执行方式。

### 以更精确的措辞规范监控与执法

我们 9 月的[威胁情报报告](https://www.anthropic.com/threat-intelligence-report-september-2026)记录了利用 AI 构建监控系统以识别和追踪政治异见人士的行为日益增多。我们重写了监控与刑事司法章节，以更精确地说明我们所禁止的内容。例如，未经本人同意追踪他人是被禁止的，无论是实时追踪，还是通过分析此前收集的数据进行追踪。在执法或刑事司法程序中，Claude 不得被用于决定或建议应调查、逮捕或起诉谁。我们也禁止利用 Claude 构建或改进专门为监控设计的工具。

与武器禁令的上次更新一样，本次更新并不代表我们在实际执行上的改变：其目的只是让政策表述更加明确。新章节还明确了哪些用途仍然被允许，包括经本人同意的追踪（例如欺诈监测）、内容审核、新闻报道和法律研究。

### 高风险用例的要求更加明确

当我们的产品被以可能影响他人健康、法律权利、财务状况、生计或基本服务获取方式使用时，我们要求必须有一名有资质的"人类在环"审核者（human in the loop，即有权审查并在必要时修改 Claude 建议的人员），且必须告知受影响的个人已使用了 AI。

随着新版 Usage Policy 的发布，这些要求本身并未改变。但由于用户经常询问某个用例是否适用这些要求，我们重写了《高风险用例要求》（High-risk Use Case Requirements）章节，以便更直接地回答这一问题。该章节现在明确列出了哪些类型的建议属于适用范围、哪些不属于。

在发布[模型硬件标准](https://www.anthropic.com/news/model-hardware-standard-research-preview)（Model Hardware Standard）之后，本章节还新增了我们的模型连接到会自主采取物理行动、且可能造成人身伤害的硬件时的使用要求：一名有资质的操作人员必须能够观察设备并在必要时使其停止；设备还必须能够在 Claude 断开连接时保持安全状态。

### 处理针对我们模型的辱骂行为

我们新增了一项禁令，针对对我们模型持续且无必要的辱骂或残忍行为。这一政策更新仅适用于极端情况，即用户在没有任何可辨识目的的情况下，反复对我们模型做出残忍行为。它不适用于常见的用户不满与反驳、黑暗题材的创意创作，也不适用于模型测试和研究。

这一新增内容与我们此前已采取的一项措施相一致：允许 Claude 模型在 Claude.ai 和 Claude Code 上[终结与持续辱骂用户的极少数对话](https://www.anthropic.com/research/end-subset-conversations)。此类滥用是本次更新的主要针对对象；Claude 终止这些交互的能力仍将是主要的执行机制。

### 澄清我们的 Supported Regions Policy

去年，我们[更新了 Supported Regions Policy](https://www.anthropic.com/news/updating-restrictions-of-sales-to-unsupported-regions)，以限制由总部位于非支持地区的实体控股过半的公司访问 Claude。我们已更新了[支持地区页面](https://www.anthropic.com/supported-countries)，以澄清我们如何执行这项政策。我们的政策禁止以下主体使用 Claude：实际身处非支持地区的人员；注册地或总部位于非支持地区的实体；以及由位于这些地区的人员或实体控股过半或控制的实体。

### 展望未来

随着 Claude 的能力和风险不断变化，我们将持续更新 Usage Policy。与本次更新及以往历次更新一样，我们将征求 Anthropic 内部各方，以及政策制定者、领域专家、民间社会和产品使用者的意见。
