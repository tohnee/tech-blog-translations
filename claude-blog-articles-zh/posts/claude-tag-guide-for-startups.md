---
title: "初创公司 Claude Tag 指南"
title_en: "The Claude Tag guide for startups"
date: 2026-11-13
author: Michael Segner
source: https://claude.com/resources/articles/claude-tag-guide-for-startups
crawled: 2026-11-17
translated: 2026-11-17
---

# 初创公司 Claude Tag 指南

> 原文：[The Claude Tag guide for startups](https://claude.com/resources/articles/claude-tag-guide-for-startups) · Claude 博客

领先初创公司如何用 Claude Tag 更快交付、规模化运营

初创公司往往节奏极快，团队精简、人人身兼数职。从很多方面看，[Claude Tag](https://claude.com/product/tag)（beta）都很贴合初创公司的工作方式：你在上下文所在的 Slack 频道里 @Claude，添加连接器，让团队一起分派和引导任务。

对刚开始使用 Claude Tag 的初创团队来说，最常问的问题之一是："我应该先让 Claude 加入哪些频道？"为了回答这个问题，我们与八家高增长初创公司交流，看看 Claude Tag 在它们的团队里如何运作。

### 洞见来自

* [![Kikoff](https://assets.claude.com/58247642907b2621ae6d414ecb7dc6714bcf1e03.svg)](https://kikoff.com/)
* [![Campfire](https://assets.claude.com/547f3af27e33331c1409324c549d765f790ca68d.svg)](https://campfire.ai/)
* [![NavigateAI](https://assets.claude.com/5348eaceef888ace36b50da1a6c9f8126ad2f1bb.svg)](https://www.navigate.ai/)
* [![Moritz](https://assets.claude.com/6b65c9f5d995c188f6273248826bbe5fc494b4ff.svg)](https://www.moritzlegal.com/)
* [![Flagler Health](https://assets.claude.com/157cc2437bd370ee12b67e1ba178b5cded79cbfc.svg)](https://www.flaglerhealth.io/)
* [![Valence](https://assets.claude.com/5855d903e0e618842304aaf2e9b02e7d648a90e2.png)](https://www.valence.co/)
* [![Orderful](https://assets.claude.com/dcd269d39d743ba04bbf4a2e803b60367c0d6b88.svg)](https://www.orderful.com/?utm_source=anthropic&utm_medium=referral&utm_campaign=claude_tag_guide)
* [![Descript](https://assets.claude.com/05128b9e935b6625beecc1bc4c6fa08814473e3e.svg)](https://www.descript.com/)

与我们交流的领导者，其愿景从重塑律所到打造下一代资源规划软件，不一而足。有的公司几乎把 Claude 加进了每一个频道，有的则深入打磨一两个具体用例。

| 公司 | 值班响应 | 从讨论串到 PR | 公司大脑 | 自助数据 | 例行报表 |
| --- | --- | --- | --- | --- | --- |
| Kikoff | ● | ● |  | ● | ● |
| NavigateAI | ● | ● | ● |  | ● |
| Campfire | ● | ● | ● |  |  |
| Flagler Health | ● | ● | ● |  |  |
| Moritz |  |  | ● |  | ● |
| Orderful | ● | ● | ● | ● |  |
| Valence |  | ● | ● |  | ● |
| Descript |  | ● |  | ● | ● |

但每一位受访者都分享了一个"啊哈"时刻：他们意识到，一段几分钟的 Claude Tag 对话替代了数天的工作，或者挖出了本会一直隐藏的洞见。

最常见的那些都收录在本指南中，每一项都配有落地实施细节，帮助创始人找到并部署真正能为团队带来改变的用例。以下是受访初创公司"指标被推动"的一些例子：

![Campfire](https://assets.claude.com/547f3af27e33331c1409324c549d765f790ca68d.svg)

**21**

从在 Slack 被提及到开出 PR 的分钟数

![NavigateAI](https://assets.claude.com/5348eaceef888ace36b50da1a6c9f8126ad2f1bb.svg)

**134**

从 Slack 讨论串合并的 pull request 数

![Moritz](https://assets.claude.com/6b65c9f5d995c188f6273248826bbe5fc494b4ff.svg)

**5**

每日下班前更新所需分钟数，原先为 1 小时

![Valence](https://assets.claude.com/5855d903e0e618842304aaf2e9b02e7d648a90e2.png)

**<1**

从客户提出需求到无代码方案落地的小时数

![Orderful](https://assets.claude.com/dcd269d39d743ba04bbf4a2e803b60367c0d6b88.svg)

**2**

从在 Slack 提问到上线的天数

![Descript](https://assets.claude.com/05128b9e935b6625beecc1bc4c6fa08814473e3e.svg)

**从数天到数小时**

每周例行报表准备的耗时变化

在本指南中，我们分享领先初创公司使用 Claude Tag 最常见的用例、频道，以及集体洞见。

---

## 最值得 @Claude 的频道

我们交流的八家初创公司都在 Slack 里使用 Claude Tag，但有几个频道被反复提及，是最适合起步的地方。

## 01 Claude 值班

**示例配置**

**频道**

`#on-call` `#alerts-ci` `#deploy-watch` `#support-escalations`

**连接器**

GitHub、GitLab、Sentry、dbt、PagerDuty、Linear、Datadog、Jira、Grafana、incident.io

**讨论串与例行任务**

事故响应、每日事故摘要、周一值班交接、每日健康摘要、每小时事故复盘

**起步指令**

@Claude 请记住本频道规则：监控告警，并立即在各自的讨论串里对每条告警做初步分诊。先查是否已有工单。先查数据，再做推断，并把已验证的内容与推测的内容分开。如果问题属实，给出可能的根因并附链接，@相关负责人；只有当修复范围可控时才开草稿 PR。如果无需行动，就说明这一点。每次事故后，把你学到的东西补充到 [经验文件] 中。

分诊频道以噪音大著称。Sentry 报错、Datadog 告警、客户 bug 报告、支持请求不断打断，让人很难从噪音里分辨信号。这通常是团队交给 Claude 的第一项任务。

当 Claude 作为[第一响应者](https://claude.com/resources/articles/ai-ci-cd-on-call)待在频道里，第一轮排查往往在值班工程师打开笔记本之前就完成了。Claude 会在每条信息落地时阅读它，调查代码库和它能访问的工具，并分享发现。如果修复范围可控，它就开一个草稿 PR；否则，它把问题连同调查结果转给对的人。在这类配置中，每个修复合并前都有人审核，只有真正全新的问题才需要人亲自启动调查。

Campfire 为财务团队构建 AI 原生的 ERP。一位工程师 @Claude，报告其某个 AI 智能体已完成的回答有部分没有送达用户。21 分钟后 Claude 就开出了 PR，当天下午便合并了。

### Kikoff：每个分诊频道都有第一响应者

Kikoff 是一家金融科技初创公司，帮助消费者建立信用、解决流动性需求、实现财务安全。Claude Tag 是公司各个分诊频道的第一响应者，包括：

* `#deploys`：Claude 决定每次发布后要盯什么，并标记出它弄坏的任何东西。
* `#alerts-ci`：构建失败时，Claude 查明原因并以草稿 PR 提出修复。
* `#alerts-sentry-backend`：Claude 对 Sentry 异常和崩溃做第一轮排查。
* `#dog-fooding`：Claude 调查员工在内部试用（dogfooding）中标记的问题，并 @ 正确的负责人。
* `#support`：Claude 对支持工单做第一轮处理。

Kikoff 一开始只让 Claude 在被提及时参与对话，而最大的收益出现在团队允许它主动介入之后。当注册功能出故障时，Claude 追查到一次后端改动，评估了影响范围，指出了负责修复的团队，并开了一个草稿 PR，让应用在此期间能以软失败方式降级。

![Slack 消息：Claude 指出注册功能已损坏，并给出原因、影响范围、修复负责人和一个草稿 PR。](https://assets.claude.com/2b0f5523a07eac627cacb997fda4823706524505.png)

Claude 指出注册功能已损坏，追查到一次后端改动，评估影响范围，指出负责修复的团队，并开了一个草稿 PR，让应用以软失败方式降级。此对话由 Kikoff 复刻，姓名与图片已作修改，经 Kikoff 许可使用。

![](https://assets.claude.com/a6d8144b8cb41f297d29241e3e22bcb6898594d2.jpg?w=168&q=75&fm=webp&fit=max)
> "每当 Claude 比监控或人更早发现问题，我都很兴奋。一个人能亲手管理的上下文终归有限，Claude Tag 帮我们组织并承担一部分上下文，而我们负责管理结果。"

Alex Dejeu，Kikoff 工程经理

### NavigateAI：在碎片化上下文中修 bug

NavigateAI 为建筑现场团队构建 AI 副驾。他们在约 90 个频道里运行 Claude Tag，用于告警分诊、集中修 bug、快速构建功能和支持升级。自 6 月以来，Claude 直接从 Slack 讨论串开出了约 223 个 PR，其中 134 个已合并，从开出到合并的中位时间为两小时。

对 NavigateAI 来说，分诊是价值特别高的用例。因为 Claude 拥有大量上下文，它能找出第一眼容易遗漏、不那么直观的根因。

![](https://assets.claude.com/8146467a01dc8932c5071f62327bec5e7fa4b7bc.jpg?w=168&q=75&fm=webp&fit=max)
> "我们和 Claude Tag 最大的'哇！'时刻，是在排查一个负载问题时。表面上看像是某个客户造成的（因为他们的调用在失败）。按人的常规反应，会继续追着那个客户查。但 Claude 能访问那么多其他数据源，它发现真正的原因是同一时间段运行的、没有埋点的内部 cron job。"

Mike Chen，NavigateAI 工程负责人

用了 Claude 之后，平均问题解决时间（MTTR）下降了。有一个案例里，Sentry 告警触发 8 分钟后 Claude 就找到了根因，修复在告警后 93 分钟合并。

"快速前进的初创公司通常只能在速度与结构之间二选一。Claude Tag 让我们两者兼得。它是一个能把所有工具的线索连起来的大脑，于是我们获得了结构，却不必自己去搭建结构。"Mike 说。

**提示**

"投入建设一个技能仓库、并让 Claude 能访问这个仓库，帮助非常大。"Mike 说。在 Anthropic，我们的值班配置把 Claude 的指令保存在仓库的 `oncall.md` 文件里，每次事故后 Claude 会把学到的东西补充进 `lessons.md`。

## 02 从讨论串到 PR

**示例配置**

**频道**

`#quick-wins` `#bug-bash` `#product-feedback` `#feature-requests` `#ux-papercuts` `#tech-debt` `#design-polish`

**连接器**

GitHub、GitLab、Linear、Jira、Confluence、Notion、Figma、Sentry

**讨论串与例行任务**

每个讨论串一项请求、每周待办清理、每日 PR 汇总、每周已交付回顾

**起步指令**

@Claude 请记住本频道规则：当有人描述一个 bug 或小功能时，在它自己的讨论串里处理。先检查是否已有工单，并阅读相关代码。如果细节缺失，就去询问细节或索要真实示例，不要猜测。如果改动很小且范围可控，就开一个草稿 PR，附上简短说明：改了什么、如何测试。永远不要合并；由人审核并批准。如果改动太大或有风险，说明原因并建议开工单。

速度是初创公司最大的优势之一，但那些能让用户惊喜的小需求，常常在忙乱中被淹没。这些信息往往由面向客户的团队收集、在 Slack 里提交，如果没被忽略，最终会进入 Linear 或 Jira，与数百个工单一起排队排优先级。

有了 Claude Tag，任何人都能起草 PR，无论是否懂技术。在讨论串里抛出一个想法，让产品、工程和 GTM 在同一处实时反馈，Claude 会把讨论串变成一份反映所有人意见的草稿 PR。

与我们交流的许多初创公司用 Claude Tag 做那些"轻盈又讨喜"（light and delight）的功能，或者清理那些审核很快、但原本永远排不上优先级的小毛病（papercuts）。

### Orderful：从 Slack 对话到生产功能，只用了两天

Orderful 是一个 EDI 平台，通过 API 或直接在浏览器里把企业与它们的贸易伙伴连接起来。其客户通过该平台与伙伴交换标准单据。

其中一种单据类型——753——在 Orderful 的 Web 应用里并不受支持。这个需求一直躺在待办列表里，导致某大型零售商的货运被延误。

当一位客户经理在 Slack 里跟进时，PM 把 Claude 拉了进来："@Claude，你应该做一个。"Claude 先索要该单据的真实示例，以便按实际格式构建，随后开出一个增加 753 支持的草稿 PR。

![Slack 讨论串：Claude 确认打印视图修复在一笔真实的 753 交易上生效，同事作出回应。](https://assets.claude.com/1921c58bc091958f185f0fc960870d6dd18f7bd3.png)

Claude 确认修复在一笔真实的 753 交易上生效。姓名与图片已作修改，经 Orderful 许可使用。

第二天早上，Claude 为配套的 754（零售商的回复）开了工单，并开出第二个 PR。两次 Slack 交流后大约两天，两者都已上线。

"以前要花几周甚至几个月的事，现在一次 Slack 对话就够了。"Orderful CTO Piers MacDonald 说。"那些价值难以证明的轻量功能，过去总是卡在待办里。现在它们有出路了。"

**提示**

### 给 Claude 提供真实的构建依据。

在讨论串里丢一个样本文件、一条客户消息或一张截图，让它按你真正需要的东西来构建，而不是靠猜。

### Valence：从功能请求到上线

Valence 与全球最大的雇主合作，用 AI 教练 Nadia 把企业的人才与绩效体系连接起来。当一位 Valence 工程师在 Slack 里说明如何处理某重要客户提出的紧急产品变更时，Claude 不只是照做，它还发现同一份配置存在于两个地方，因此还有其他改动必须一并完成。如果没有 Claude，最初的改动会是不完整的。

![Slack 交流：Valence 工程师请 Claude 确认一处改动，Claude 回复说这其实是两处改动。](https://assets.claude.com/20696126082a923a5dc573f7571aadb71caf617e.png)

Claude 指出所请求的改动实际上是两处改动。经 Valence 许可使用。

![](https://assets.claude.com/3a62ff7d092a4f9d3cd4b74f49c1aa2e0a9a8340.jpg?w=168&q=75&fm=webp&fit=max)
> "它没有只是一味同意专家的判断。它抓到了重复的配置——那种人很容易跟丢的东西。"

Sameer Bansal，Valence 首席 AI 工程师

另一个案例里，一位客户紧急要求做一项定制。Claude 检查了代码，并与一位工程师协作确认：无需修改代码即可交付。不到一小时，一位同事就把方案准备好了交给客户。

## 03 公司大脑

**示例配置**

**频道**

`#ask-anything` `#company-wiki` `#product-questions`

**连接器**

GitHub、Notion、Google Drive、Linear、Jira、Confluence、Granola、Metabase

**讨论串与例行任务**

每个讨论串一个问题、决策日志更新、每周陈旧文档检查、重复问题汇总

**起步指令**

@Claude 请记住本频道规则：从我们的代码、文档和历史讨论串中寻找答案，并附上来源链接。如果来源之间相互矛盾，查代码，给出当前正确答案，并标出过时的文档。如果你不确定，就直说，并 @ 相关负责人。当讨论串形成决策时，把它记录到 [文档位置]。任何要发给客户的内容，都必须先经人核对。

在初创公司，机构知识常常活在人们的脑子里——从产品计费代码的细节，到入职文档托管在哪里。

对我们交流的许多初创公司来说，Claude Tag 已经成为公司大脑。Claude 回答时附上来源，不确定时 @ 负责人。它还让知识保持最新：当讨论串形成决策时，Claude 能当天就把它记录进你的文档，并标记出已经过时的文档。

![Slack 频道：同事问 Claude 最终决定了什么，Claude 对该频道做了总结。](https://assets.claude.com/a4edb94f8444bc21a1fc8aa3d489f15358328129.png)

示例交流。

### Moritz：从接收需求到排班，实时的可信来源

Moritz 是一家 AI 原生律所，承诺合同当天交付——按 Moritz 的说法，行业标准至少是三周。法律工作之外的一切，从接收需求、报价到人员安排和跟进，都发生在 Slack 里：每个事项一个讨论串，每个客户一个频道。

如今从 CEO 到律师助理，所有人都是先问 Claude。过去要在 Slack 里翻找最多 30 分钟的问题，现在两分钟内就能得到答案。下班前的更新如今由当天的讨论串自动草拟，从约一小时的整理变成五分钟的编辑。

省下的时间回到了法律工作上。Claude Tag 处理案件周边的行政事务，比如追问、提醒和状态更新。它无法访问客户文件，也无法访问与 Moritz 律师的保密对话。

![](https://assets.claude.com/39f487100b408fabef0773334afb8c15e050525f.jpg?w=168&q=75&fm=webp&fit=max)
> "一家业务横跨 44 个国家的律所，每月会产生数百个一次性问题，没有人会为这些问题专门开发功能。Claude Tag 从我们在 Slack 里的自有历史中给出答案。每个答案都是一个带链接的讨论串，机构记忆因此不断复利增长。"

Stefan Mandaric，Moritz 联合创始人兼 CTO

### Campfire：按需获取客户体验知识

有一个 Slack 频道的人气"爆炸式增长"：他们的 CX（客户体验）频道。销售用这个频道"在潜在客户对话中验证某些功能"，而不必"去 ping 十个人"。

这类频道特别有效，因为销售可以在客户正关注的那一刻当场回答，并在早期客户对话中更独立、更自信地行动。

![](https://assets.claude.com/921fd10de481a1094bdd4b483f52933e68791fb2.jpg?w=168&q=75&fm=webp&fit=max)
> "Claude Tag 基本上就是我们的中央知识库。"

Nancy Jin，Campfire AI 工程经理

## 04 自助数据

**示例配置**

**频道**

`#data-requests` `#ask-revops` `#metric-definitions`

**连接器**

dbt、GitHub、Metabase、BigQuery、Snowflake、Databricks、Notion

**讨论串与例行任务**

每个讨论串一个问题、每周站会前读报、发布与实验读数、管道故障分诊、新问题分诊

**起步指令**

@Claude 请记住本频道规则：基于我们受治理的模型和 [数据技能仓库] 中的定义来回答。如果数据未覆盖到，就说明它尚未经验证，不要猜测。先给答案，再给数字、驱动因素以及任何注意事项。在解释某处变化之前，先查看近期事故、发布和 Slack 讨论。如果某个指标的定义不清楚，就问清楚我们指的是哪一个。对于重要事项，先分享你的计划或 SQL，再执行。把你已验证的内容与你假设的内容分开，并在回答末尾列出任何未解决的数据质量警告。如果有人发现错误，起草一份修复方案，交由数据团队成员审核。如果同一个问题出现了两次，建议把它排进计划。

在高速成长的初创公司，每个职能都想要数字，数据团队必须决定谁的请求先做。把 Claude Tag 接入你的数据后，任何人都能用自然语言提问，不必再排数据团队的队。

这也是我们自己采用的用例。[在我们某个数据频道的一个月里，Claude Tag 回答了人们提出的 75% 以上的问题，通常在一两分钟内完成](https://claude.com/resources/articles/self-service-data-analytics-in-slack-how-anthropic-deploys-claude-tag-for-ad-hoc-questions)。它基于受治理的数据和与分析师相同的定义工作，这些定义存放在一个带版本管理的仓库里，Claude 在每次对话中都会重新读取。

![示意图：Claude Tag 把仓库中发生了什么与知识索引中的原因结合起来，形成关于注册量下滑的一个统一回答。](https://assets.claude.com/4cf8ac80c074a4f3b28e78bd605ec9a881a611a8.png)

出自《Slack 中的自助式数据分析：Anthropic 如何部署 Claude Tag 处理临时问题》。

### Descript：回答临时数据请求

Descript 是一个 AI 驱动的视频编辑平台。如今 Claude Tag 是数据请求和初步分析的第一道支持。产品、增长、RevOps 和财务在 Slack 里提问，得到基于 Descript dbt 模型的答案。

![](https://assets.claude.com/93f058c356e58c0f49205fd19e8f3585533542bf.jpg?w=168&q=75&fm=webp&fit=max)
> "过去我每周或每月都要手写复杂的 SQL、手动刷新数字。现在我用自己做的 Claude artifact 替换了好几个数据团队的仪表盘，也不用再手动刷新了。"

Daisy Zhang，Descript 增长营销负责人

Daisy 的每周例行报表准备时间从数天降到了数小时。

例如，增长团队会问：生命周期订阅为什么下降？付费搜索是否正在把最后触点归因让给其他渠道？一个自助账户变成企业机会需要多久？数据团队会跟踪 Claude 生成的 artifact，看哪些数据资产在各团队中最重要，同时把时间花在战略问题上，以及构建让自助服务得以运转的上下文。

![](https://assets.claude.com/04cc4542c1f0cb9d273d22b2597f8e856abe542a.jpg?w=168&q=75&fm=webp&fit=max)
> "商业智能一直许诺给业务用户自助服务。直到我们把 Claude Tag 配好、给它足够大的数据上下文，我才第一次看到它真的实现。"

Jen Huhn，Descript 变现 PM

**提示**

### 先把上下文投资好。

让你的数据团队把核心模型和指标定义记录下来，因为自助服务的效果，取决于 Claude 拥有多少上下文。参见[回答数据问题](https://claude.com/docs/claude-tag/users/use-cases/answer-data-questions)。

### Orderful：从提问到仪表盘

在 Orderful，自助分析既包括对话式分析，也包括完整的数据构建：任何人都可以从 Slack 里的一个问题，走到一个合并进生产环境的仪表盘。关键在于语义层（semantic layer），它编码了各方认可的指标和定义，因此每个答案、每次构建都用同一套定义。

![](https://assets.claude.com/ae41953c096037ea0d3a369b9af1e1f52378367a.jpg?w=168&q=75&fm=webp&fit=max)
> "我们信任输出，是因为语义层约束了 SQL，CI 把守着构建，而且有一套就定义达成共识的流程。没有这些，你就会得到看起来很自信的错误答案。这些护栏到位之后，接入 Claude Tag 用了不到 30 分钟。现在同事们在共享的 Slack 讨论串里一起构建，而不是各自单独作战。"

Piers MacDonald，Orderful CTO

## 05 报表与交接

**示例配置**

**频道**

`#sales-pipeline` `#customer-handoffs` `#standup-summary` `#qbr-prep`

**连接器**

Notion、Google Drive、Gong、Salesforce、Gainsight

**讨论串与例行任务**

每日下班前状态草稿、QBR 前简报、deal 交接

**起步指令**

@Claude 请记住本频道规则：根据我们的讨论串、文档和数据起草每份例行报告，并附上来源链接。先讲什么变了、什么需要决策。把你已验证的内容与你假设的内容分开，缺失的部分要明确标出，而不是自行填补。把草稿发在单独的讨论串里，由 [负责人] 编辑。在有人批准之前，任何内容都不外发。如果某份报告总是被同样地修改，建议更新这些指令。

我们讲过的许多例子都是反应式的：某件事发生了，Claude 作出响应。而例行报表是 Claude 按计划负责的工作，就像同事负责一项周期性交付物那样。

![Slack 交流：同事向 Claude 要周一的销售管道更新，Claude 发布了一份带图表的每周摘要。](https://assets.claude.com/8d3d8fd8252fc93f3bd80bb28ae0a728142a7ef2.png)

在 Claude Tag 中使用 Routines（例行任务）的示例。

你只需描述一次结果；之后 Claude 每次执行，并把结果发到团队本来就在工作的地方。

### Valence：deal 复盘与交接

Valence 正在让 Claude 在每次季度业务复盘（QBR）前为团队做简报，内容包括客户健康状况、进行中的 deal、阻塞项和下一步。他们也在努力让 deal 成单后从销售到客户成功的交接更顺畅。Claude 帮助汇总跨多个接触点的细节，为团队省下时间，还常常找出他们可能遗漏的关键事项。

"当一笔 deal 成单时，Tag 会依据 deal 历史、通话和合同构建交接材料：谁是谁、承诺了什么、哪些是定制的、哪些还悬而未决。然后客户成功团队在启动会前审核它。"Sameer 说。

**提示**

### 如果你已经问过两次，就把它排进计划。

"@Claude 每周一美东时间上午 9 点，为每个本月有 QBR 的客户发一份简报：健康状况、进行中的 deal、阻塞项和下一步。"参见[设置例行任务](https://claude.com/docs/claude-tag/users/proactivity)。

## 06 上手清单

下面的清单汇总了这些初创团队的最佳实践，供你应用到自己的工作流中。

**上线之前**

检查前置条件。

Claude Tag 在 Claude Team 和 Enterprise 套餐中处于公开测试（public beta），在 Free、Pro 或 Max 上不可用。你需要一位 Claude 组织 Owner 和一位 Slack 工作区管理员来连接两者。还必须由管理员开启 Routines（例行任务），Team 套餐还需要用量额度，Claude 才会响应。

用一个 bundle 配置 Claude 的访问权限。

在频道里，Claude 以自己的[智能体身份](https://claude.com/docs/claude-tag/concepts/agent-identity)工作，使用服务账号而非任何人的个人登录。把需要的连接器、仓库和指令归入一个 [bundle](https://claude.com/docs/claude-tag/admins/add-connections)，并按组织、工作区或频道挂载。这决定了 Claude 在每个地方能触达什么，且频道内所有人获得相同权限。从窄开始：只给第一个频道需要的东西。

先在一个私有频道里试验。

我们交流的近一半初创公司，都是先让一个小型跨职能团队在私有频道里试验，从而开始 Claude Tag 之旅的。"先以多种角色组成的小组私下开始，再转到群组频道。"Sameer 说。

确定边界。

默认情况下，Slack 工作区里的任何人都可以使用 Claude，即使没有 Claude 账号。你可以[限制访问](https://claude.com/docs/claude-tag/admins/restrict-access)到你的组织范围，并把搜索限制在 Claude 所在的频道内。在 Enterprise 上，你还可以限制到特定角色或选定频道。

为 Claude 能做和绝不能做的事设定清晰预期。我们交流的几个团队允许 Claude 开草稿 PR，但由人审核并合并。对 Orderful 来说，处理"基础设施变更、审计、敏感数据"的是 [Claude Code](https://claude.com/resources/articles/claude-code-guide-for-startups)，而不是 Tag。遇到"难题"，例如"一个触及多个服务的 PR"，Claude 会去征询第二意见。Moritz 不给予 Claude Tag 访问客户文件或与其律师保密对话的权限。

尽早启动安全审查。

常见问题是数据保留和 Claude 能触达什么，[安全](https://claude.com/docs/claude-tag/concepts/security-and-data)与[数据生命周期](https://claude.com/docs/claude-tag/concepts/data-lifecycle)页面分别回答了这两点。开启了零数据保留、使用客户管理加密（CMEK）策略或 HIPAA 配置的组织无法使用 Claude Tag，它也不在我们《商业伙伴协议》（BAA）的覆盖范围内，所以在规划推广前请先确认。

设定预算与告警。

Claude Tag 按用量计费，早点沟通可以避免采用规模扩大后出现意外。你可以整体以及按频道[设置支出上限](https://claude.com/docs/claude-tag/admins/set-spend-limit)，按频道选择模型，并通过 Enterprise Analytics API [按用户归集成本](https://claude.com/docs/claude-tag/admins/attribute-costs)。Orderful 设置了组织级上限，并在 75% 和 90% 处告警。"我们对频道成本有极强的所有权意识。负责人要论证'是的，这笔支出换来的产出/结果是合理的'。"Kikoff 工程经理 Alex Dejeu 说。用第一个频道的实际成本来估算下一个频道。

**部署**

在团队已经在用的频道里挑一个明确的任务，比如值班告警或 bug 分诊。

"我们在某些团队先做试验，看看什么有效；等确认把问题都磨平了，再把这个想法推广到其他团队，让它们也在自己类似的频道里加上。我们希望避免让对 AI 出错容忍度较低的人产生信任崩塌的体验。"Kikoff 工程经理 Alex Dejeu 说。

先让专家和文化引领者上手。

让你团队本来就信任的人先用 Claude，而且是公开地用。

"在公开场合与 Claude 来回切磋，既高效又有趣。销售和客户成功的好几个人看着专家[与 Claude Tag 互动]，然后开始自己去问 Claude，很快就获得了价值。"Valence 首席 AI 工程师 Sameer Bansal 说。

调节噪音。

多家初创公司告诉我们，需要调整 Claude 的话多程度。太话痨是一种风险。

"临时请求里的对话有时会变得很吵。我们一直在尝试降低这里的响应频率，也更讲原则地决定临时请求交给 Claude 做什么。"NavigateAI 工程负责人 Mike Chen 说。

但话太少同样是风险。在繁忙的频道里，"你要么每次都 @ 它，要么它基本不会做什么。"Flagler Health 联合创始人 Will Hu 说。而且"如果没人密切盯着某个频道、也没人跟它互动，它就会一直闲着。"

让同事连接自己的账号。

设置时配置的管理员 bundle 决定了 Claude 在频道里能替所有人触达什么。[个人连接器](https://claude.com/docs/claude-tag/concepts/personal-connectors)的工作方式不同：Claude 以提问者的权限行事，因此在他们批准后，可以从其文档、收件箱或 CRM 中取数（先由 Owner 为组织添加该连接器；在 Enterprise 上由管理员管理个人连接器）。答案仍会发到频道里，所以对敏感内容请选择"允许并审核"（Allow with review）。

像给新员工做入职那样撰写频道指令：

先检查什么、什么时候开 PR、什么时候该问，以及"无需行动"也是一个有效答案。

在频道里给 Claude 反馈，而不是在私信里。

在讨论串里纠正它。它会[按频道记忆](https://claude.com/docs/claude-tag/users/memory)，同事也能通过旁观学会如何与它协作。若要形成长期修正，请 Claude 更新它对本频道的记忆。

![两条来自 Valence 员工的 Slack 消息，感谢一位同事在公开场合与 Claude 一起把一个问题的思路走通。](https://assets.claude.com/7e4a82b6f73aabecf6a5a5fe148c38a53659ba7a.png)

两位 Valence 员工在旁观一位同事与 Claude 公开梳理一个问题后，向他表示感谢。经 Valence 许可使用。

不确定下一步该做什么？@Claude，问它对你的组织学到了什么、会扩展到哪些用例。

Moritz 的联合创始人兼 CTO Stefan Mandaric 让 Claude 为每个团队推荐用例。十五分钟后，它已经读完该律所的 Slack 频道、Linear 议题、Notion SOP、Drive 和 Metabase 仪表盘，并发布了 25 个建议。"其中 18 个无需进一步配置就能用。这就成了我们的推广计划。"

---

## 结语：从"哇"时刻里我们学到了什么

那些"哇"时刻并不总是关于速度。Claude 常常找到没人要它去找的东西。有时惊喜来自克制。有时惊喜来自意料之外的交流。"最终你会习惯 Claude 参与到玩笑里，而且很快会欣赏它是个容易逗笑的观众，总是第一个笑。"Orderful CTO Piers MacDonald 说。

![一张带图片回复和表情反应的 Slack 讨论串。](https://assets.claude.com/8884ca89d9b6e0bf91eb7b426d8546c971d8079d.png)

Orderful 在 Slack 中复刻的对话。经 Orderful 许可使用。

希望这份指南对你有用。特别感谢 Campfire、Descript、Flagler Health、Kikoff、Moritz、NavigateAI、Orderful 和 Valence 分享他们的经验与洞见。

---

## 更多资源

### 入门

* [Claude Tag 概览](https://claude.com/product/tag)
* [Claude Tag 文档](https://claude.com/docs/claude-tag)
* [设置 Claude Tag](https://claude.com/docs/claude-tag/admins/setup-overview)
* [值班引导式配置](https://claude.com/docs/claude-tag/admins/setup-oncall)
* [排查配置问题](https://claude.com/docs/claude-tag/admins/troubleshooting)

### 连接你的工具

* [添加连接与 bundle](https://claude.com/docs/claude-tag/admins/add-connections)
* [配置 GitHub 访问](https://claude.com/docs/claude-tag/admins/configure-github)
* [个人连接器](https://claude.com/docs/claude-tag/concepts/personal-connectors)
* [网络要求](https://claude.com/docs/claude-tag/admins/network-requirements)

### 访问、安全与支出

* [限制访问](https://claude.com/docs/claude-tag/admins/restrict-access)
* [智能体身份如何运作](https://claude.com/docs/claude-tag/concepts/agent-identity)
* [安全与数据](https://claude.com/docs/claude-tag/concepts/security-and-data)
* [数据生命周期与删除](https://claude.com/docs/claude-tag/concepts/data-lifecycle)
* [Claude Slack 应用可以访问什么](https://claude.com/docs/claude-tag/admins/for-slack-admins)
* [设置支出上限](https://claude.com/docs/claude-tag/admins/set-spend-limit)
* [把成本归集到用户](https://claude.com/docs/claude-tag/admins/attribute-costs)

### 在 Slack 中与 Claude 协作

* [控制 Claude 何时响应](https://claude.com/docs/claude-tag/users/when-claude-responds)
* [Claude Tag 能理解的命令](https://claude.com/docs/claude-tag/users/commands)
* [频道记忆](https://claude.com/docs/claude-tag/users/memory)
* [设置例行任务](https://claude.com/docs/claude-tag/users/proactivity)

### 用例

* [用例库](https://claude.com/docs/claude-tag/users/use-cases)
* [修复 bug](https://claude.com/docs/claude-tag/users/use-cases/fix-bugs)
* [回答数据问题](https://claude.com/docs/claude-tag/users/use-cases/answer-data-questions)

### Anthropic 如何使用 Claude Tag

* [Claude Tag 如何担任 Anthropic 应对 CI/CD 故障的第一响应者](https://claude.com/resources/articles/ai-ci-cd-on-call)
* [Anthropic 如何用 Claude 实现自助式数据分析](https://claude.com/resources/articles/how-anthropic-enables-self-service-data-analytics-with-claude)
