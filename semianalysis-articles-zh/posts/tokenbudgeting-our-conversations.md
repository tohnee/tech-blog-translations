---
title: "TokenBudgeting：我们与企业关于 token 支出的对话"
title_en: "TokenBudgeting: Our Conversations with Enterprises on Token Spend "
subtitle: "大规模 TokenMaxxing 究竟是否真的来过？"
date: 2026-06-30
source: https://newsletter.semianalysis.com/p/tokenbudgeting-our-conversations
crawled: 2026-09-15
authors: ["Crystal Huang", "Joey Brookhart", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# TokenBudgeting：我们与企业关于 token 支出的对话

> 原文：[TokenBudgeting: Our Conversations with Enterprises on Token Spend](https://newsletter.semianalysis.com/p/tokenbudgeting-our-conversations) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**大规模 TokenMaxxing 究竟是否真的来过？**

据报道，在今年早些时候企业内部毫无节制的消费之后，token 消耗正在撞上预算之墙。SemiAnalysis 团队通过 Slack、电话以及在 Databricks AI Summit 现场与 50 多家客户交流，以了解企业内部的趋势。

- 媒体广泛报道的 Meta、Uber 等公司针对 TokenMaxxing 预算的应对之举被夸大了，其根源在于糟糕的激励机制与员工额度设置，而我们在其他组织中并未发现这些问题

- 预算如今已成新常态，但并不存在一个公认的标准数字——预算从每月 $250 起步，最高可达数万美元。

- 企业正在下调默认模型档次、关闭高级版（premium tiers），与此同时，员工则在钻 Microsoft 365 Copilot 订阅的空子，以把自己的 token 额度榨到极限。

# TokenMaxxing 的兴衰

TokenMaxxing 兴起于今年早些时候，当时 Meta、Salesforce 等公司开始鼓励员工尽可能多地消耗 AI token 以提升生产力。在 Meta，甚至有员工搭了一个「Claudeconomics（Claude 经济学）」仪表盘，对公司排名前 250 位的重度用户进行排行。结果显示，Meta 员工在 30 天内消耗了超过 60T 个 token，其中消耗最高的个人约占 280B 个 token。员工们开始让智能体连做几个小时的研究、单纯为了烧 token，来争夺「Token 传奇」（Token Legend）、「缓存法师」（Cache Wizard）之类的头衔。

在 The Information 报道这笔支出两天后，该仪表盘即被关停。

这一幕只是 2026 年上半年（1H26）企业 TokenMaxxing 浪潮中的众多事件之一。如今，企业的关注点正从 TokenMaxxing 转向 token 预算管理。最新一例是 Uber 登上新闻头条：它在四个月内就烧光了 Claude Code 和 Codex 的年度预算。作为应对，公司设定了每名员工每月 $1,500 的上限，超限请求仍可提出，并按个案审批。为了验证媒体对 2026 年初 TokenMaxxing 以及当下 TokenBudgeting 的报道是否属实，SemiAnalysis 团队在 Databricks AI Summit 现场展开走访，并与大型企业交流以理解这些趋势。

# 我们对数据与叙事的看法

关于 TokenMaxxing 及由此导致的预算爆表，外界已有大量报道。但根据我们在 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)中的工作，我们估计第 90 百分位及以上的客户贡献了大部分收入，且在今年余下时间里几乎不存在 API 收入被砍的风险。即便是 Meta——2 月份每月烧掉 70T 个 token、按牌价计算每名员工年支出接近至少 $50,000——据我们估计也只占 Anthropic 收入的 3-5%。Ramp 的数据也显示出顶级客户的类似趋势：第 99 百分位客户每名员工年支出接近 $90,000，第 90 百分位客户约为 $7,300。这与 Ramp 客户中位数仅 $136 的支出形成鲜明对比。请注意，Ramp 客户总体上远更为技术前沿，因此这本身已是一个支出高度右偏的分布。而媒体笔下的财富 500 强，每员工支出仍远低于 $100。

![](https://substack-post-media.s3.amazonaws.com/public/images/e60590bd-4f37-4a0d-9194-b9eae8ca8349_2502x1310.png)
*来源：Ramp Economics Lab*

我们对企业客户（包括众多财富 500 强）的访谈也呈现同样的分化。许多技术前沿的财富 500 强企业在 AI 上的支出远低于每名员工每年 $2,000，且较大的支出主要集中在工程和数据科学部门。这表明企业级使用的 s 曲线仍有充足的爬升空间。今天的市场由编码（coding）垂直领域的爆发所驱动，其余则是基于 Anthropic 或 OpenAI 模型构建产品、由风投支持的 AI 公司（这些第 90-99 百分位客户的收入同样在加速）。

编码市场为 AI 实验室 ARR 带来的爆发，将在网络安全（Cyber，取决于 Mythos 的重新发布）领域以比 Claude Code 更快的速度重演，并随着 Cowork、CoPilot、Codex 以及 Computer 类产品渗透企业，在白领知识工作上再度重演。

[Tokenomics 模型](https://semianalysis.com/tokenomics-model/)以第一方与第三方两种口径估算各家 AI 实验室的编码相关支出，以及应用层公司（Cursor、Loveable、GitHub CoPilot 等）的 ARR 与利润率，帮助投资者和企业跟踪该垂直领域及其内部的增长。我们认为，如今 OpenAI 与 Anthropic 合计超过 70% 的 ARR 可归因于编码用例；考虑到 B2B 与 B2C 结构差异（Anthropic 90% 以上为 B2B，OpenAI 为 60%），Anthropic 的编码支出规模高于 OpenAI。

![](https://substack-post-media.s3.amazonaws.com/public/images/b752149f-ce67-4fcd-9303-5c17396e839d_1597x792.png)

尽管如此，廉价 token 的需求依然广泛。我们看到 Token 即服务（TaaS）/API 端点市场的支出在前沿模型与开源模型两端都在高速增长。我们对本季度 AWS Bedrock 的估算，使我们对 AWS 总增长率的判断远高于华尔街一致预期。[Tokenomics 模型](https://semianalysis.com/tokenomics-model/)还预测 Together、Fireworks、Baseten 等 TaaS 供应商将迎来旺盛需求，这些公司目前的合计 ARR 已超过 $4B。

![](https://substack-post-media.s3.amazonaws.com/public/images/15115dda-fbce-4ff6-80dc-99d155a99399_936x429.png)
*来源：SemiAnalysis Tokenomics 模型，TaaS 标签页*

因此可以说，我们的研究工作表明：头条新闻言过其实，企业仍在持续支出，而新的需求与 token 消费用例/垂直领域正推动 AI 列车高速前进。

# 预算管理：随便挑个数字

我们访谈的大多数公司（n>50）同样对 AI 使用设置了硬性上限——不过各公司似乎并没有向某个统一的 token 金额收敛。在低端一端，我们与美国一家排名前三的航空航天与国防制造商的 AI 负责人、以及全球最大制药公司之一交流过，它们分别将员工上限设为每月 $250 和 $500。在高端一端，我们与 Workday、Stripe 等公司的交流显示，其员工预算约为每月 $2,000。

还有一部分公司至今未设置任何限额，原因似乎有两种可能：

1. 员工对 AI 工具的访问受到极大限制，成本根本不构成顾虑；或

2. 公司从员工身上获得了足够的额外产出，足以证明这笔支出合理。

金融业是前者的典型例子。该行业大部分机构采用 AI 的速度缓慢，少数行动者也只是浅尝辄止。在与多家资产管理公司、地区性银行和汽车金融公司的数据科学家、分析师和 AI 负责人的交流中，同样的模式反复出现：员工被局限在微软平台所提供的工具之内。

而投资回报率（ROI）一旦存在，可能非常惊人：

- 亚马逊一名负责在公司内部物色和安置首席工程师（principal engineer）的招聘人员指出，从初筛电话到团队安置的流程过去需要 6-9 个月，而借助 AI 工具记录面试笔记并生成报告，这一周期已被压缩了一半。

- 一家服务 85% 财富 500 强企业的数据分析供应商的员工表示，过去需要一周完成的工作，如今几小时即可完成。

最成熟的公司则在实施软性限额，员工应将其视为指导原则而非硬性规则。在一家上市网络安全公司，统管所有开发者和数据科学家的分析总监表示，他们为初级员工设定每月 $800 的「限额」，资深员工则为每月 $1,600-$4,000 不等。数据科学家获得的预算最大，因为他们往往要处理更大的数据集、需要更多 token——这一模式在预算灵活的公司中反复出现。若员工超出额度，系统会提醒其经理进行沟通，而不是直接掐断使用、等到计数重置。

# token 节约的艺术

随着 token 支出上升以及高管对这笔支出关注度的提高，员工开始学着适应。当上述那家航空航天与国防制造商首次推出每月 $250 限额时，一些重度用户四天就将其烧光。员工现在可以申请更高预算，但过去并没有这个选项。如今员工必须发挥创造力来节约 token。该公司披露，尽管员工可以使用 Claude，但公司已「关闭」Opus 4.8 和 Fast-Mode，认为其并非必要。管理层认为，给员工更大的 token 预算会促使他们去自动化一些根本不该自动化的任务，比如写邮件。我们认为管理层的这种反自动化观点是天真的。电子邮件就像接入 AI 实验室连接器的 Slack 一样，将随着时间推移变得更自动化、更 AI 原生，从而在整个组织内带来更高的生产力、透明度和协作效率。

一家全球旅游科技公司采取了稍微温和的方式。该公司 1,500 名员工中有 800 名工程师，全员每年在 AI 上的总支出略低于 $10M。公司最近将全体员工的 Claude 默认模型从 Opus 切换为 Sonnet。Opus 仍可使用，但现在使用它需要有意识地主动选择。大多数员工默认预算为每月 $200，但根据资历和岗位可提高至数万美元，且预计不久后将上调预算。

随着越来越多公司设置限额，许多员工并不受困扰，因为他们的用量远够不到上限。我们在 Databricks AI Summit 上以及研究电话中与客户的交流显示，在许多组织中，大多数员工都远未触及限额。

这与我们在 SemiAnalysis 内部看到的用量分布如出一辙：少数员工每天支出四到五位数，另一些人则接近于 0。接近或超过限额的员工已经找到了拉长 token 用量的办法。我们没有设置限额，因为表现最出色的恰恰是那些大量消耗 token 的人。

订阅 Microsoft 365 Enterprise 的公司员工可以免费、无限量地使用标准版 Copilot 聊天机器人。由于这部分用量不计入月度预算，员工可以钻系统的空子：先用 Copilot 的 365 聊天起草和归纳想法，再动用按量计费的 token 去用 Claude 或 Codex。

# AI 作为人力杠杆

AI 工具的成本由公司承担，但收益也归公司所有。美国三大航空公司之一在预算方式上与我们交流过的其他公司截然不同。它的 token 配额与具体项目以及该项目预期带来的收入挂钩。项目立项时，财务团队会决定将收入的多少比例预留用于差旅、承包商费用等开支，而现在这笔预算也必须覆盖 token 使用。

这完全重构了 AI 支出的意义。慷慨发放额度的公司，前提预期是员工会工作得更快。产出预期随支出水涨船高，许多员工发现自己在职时间反而比以前更长。在与 50 多家中大型企业的交流中，有一点已经很清楚：Uber、Meta 等财富 500 强 token 消耗登上头条的故事，是激励机制失当和监督松弛的结果，而不是缺少高 ROI 的活动/项目可供投入 token。这种 ROI 动态最清晰的表达在亚马逊：尽管裁员被广泛报道，但受益于 AI 工具释放的效率，该公司正在以更快的速度招聘。

# 预算管理将长期存在

上限、软性限额和节约技巧，都是管理月底账单的手段。与新闻流中动辄高企的 token 支出数字形成对照的是，Anthropic 官方文档显示，每位开发者的 Claude Code 平均用量在每月 $150-$250 之间，且只有 10% 的用户每日支出超过 $30。经过这轮与客户的一线走访，有一点很明确：2026 年下半年（2H26）AI 预算不存在实质性风险，我们预计 Anthropic 与 OpenAI 的 API 业务在可预见的未来将继续保持当前的净新增月环比（m/m）增速。

如需进一步了解 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)，包括我们对各家 AI 实验室和超大规模云厂商财务状况的估算，请发送邮件至 [sales@semianalysis.com](mailto:sales@semianalysis.com)

# 精选访谈摘要

我们在下方附上与部分企业交流情况的摘要：
