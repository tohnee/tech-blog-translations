---
title: "推出面向法律工作的 artifacts"
title_en: "Introducing artifacts for legal work"
date: 2026-10-28
source: https://claude.com/resources/articles/introducing-artifacts-for-legal-work
crawled: 2026-11-17
translated: 2026-11-17
---

# 推出面向法律工作的 artifacts

> 原文：[Introducing artifacts for legal work](https://claude.com/resources/articles/introducing-artifacts-for-legal-work) · Claude 博客

*Claude for Legal 现在包含了面向法律工作的开箱即用 artifacts，团队可以用自己的数据和连接器加以调整，并在整个业务中共享。*

今天，我们推出开箱即用的 artifacts，法律专业人士可以按自己团队的工作方式加以调整，并与业务各处的同事共享。自我们[在 5 月推出 Claude for Legal](/resources/articles/claude-for-the-legal-industry) 以来，法律团队最常见的请求就是更简单的配置方式，以及更便捷的同事协作方式。

artifacts 是交互式工具，比如跟踪器和仪表盘，团队可以在 Claude 中使用并共享。我们新的法律模板库（gallery）包含了面向具体任务的 artifacts，例如审阅一叠合同、跟踪监管变化，以及接收来自业务方的法律请求。每个 artifact 打开时都带有一个示例，让法律专业人士在加入自己的数据和连接器之前，先看到这项工作如何成形。每个答案或输出都带有一个指向其来源的链接。

我们还在资助两类工作：为司法可及（access to justice）工作构建 artifacts 的公益团体，以及教未来律师用 Claude 构建的法律教育项目。同时，我们启动了法律大使计划（Legal Ambassadors Program），让法律专业人士可以相互学习。

## 模板库里有什么

使用这些 artifacts 时，法律专业人士带来自己的文档和来源，Claude 完成第一遍处理，律师再把判断力应用到结果上。它们覆盖了法律团队最常向我们提出的工作：

* **引证核查**：把一份法律文件与其来源比对，标出不一致的引文、错误的页码，以及无法支持该主张的来源。
* **法域调研矩阵**：在一张表里跨州或跨国比较某个法律议题（比如数据泄露通知规则），并附上底层法律的链接。
* **事项看板**：把委托书、邮件或电子表格变成一张在办事项看板，显示负责人、下一步和下一个截止日期。
* **Playbook 偏差看板**：把合同与公司的标准条款比对，标出每一处不同的条款，并发送给负责批准例外的人。
* **监管前瞻扫描**：根据公司的业务和运营地区，把即将出台的法规映射到时间线上，并按影响排序，附上来源链接。
* **表格化审阅**：从一组合同中构建一张表格，显示你询问的条款（比如遣散、竞业限制），并附上确切条文的链接。

## 贴合团队的工作方式，并在护栏下共享

每个法律团队的工作方式都不一样，而 artifacts 在与法律团队已经在用的系统连接时效果最好。法律专业人士可以让 Claude 把 artifacts 调整成适合自己团队的样子，并用连接器引入团队的 playbook 或研究来源，这样谁都不必手动上传文档。

自 Claude for Legal 推出以来，我们已经新增了 60 多个法律连接器，包括 Bloomberg Law、Filevine、Ivo、Legora 和 Patlytics。完整清单见我们的[法律目录（在新标签页中打开）](https://claude.ai/directory/legal)。

artifacts 支持组织内外的协作。法律团队可以与业务各处的同事，或与客户和合作伙伴一起处理同一个 artifact，共享设置既能确保隐私，也支持团队之间的道德隔离墙（ethical walls）。

## 向法律科技公司和律所开放模板库

我们与法律科技公司和律所合作，为法律专业人士构建 artifacts。每个 artifact 都在模板库中，供法律专业人士发现、试用并调整到自己的工作中：

* **AI Governance Benchmark，由 [Goodwin 构建（在新标签页中打开）](https://www.goodwinlaw.com/en/resource/ai-governance?utm_medium=referral&utm_source=external&utm_campaign=aiprac26&utm_content=anthropic_announcement)**：对一家公司的 AI 治理方法做基准评估，以发现潜在缺口。
* **Harvey Intake，由 [Harvey 构建（在新标签页中打开）](https://www.harvey.ai/)**：让业务用户在 Claude 中拥有一个提交法律问题与请求的统一入口，根据 Harvey 中法务部门自己的指引回答例行问题，其余路由给律师，律师的回复会回到 Claude 中。
* **Obligations Checker，由 [Foley & Lardner 构建（在新标签页中打开）](https://www.foley.com/)**：审阅协议中双方的义务，帮助在交割前验证预期、在交割后跟踪预期。
* **Subpoena Response Tool，由 [普华永道构建（在新标签页中打开）](https://www.pwc.com/)**：把团队的既有先例、标准异议和模板转化为自动化的、可供审计的初稿，让律师能专注于复杂问题，同时更快响应。

我们很高兴看到法律科技公司、律所和法律援助组织创建并分享自己的 artifacts，Legora 和 Orrick 还有更多 artifacts 即将推出。

![Spellbook](https://assets.claude.com/6d8c2b327807c9a9dc5b911946df64b7a0cbda3c.svg)

> “Claude 持续支撑我们成为世界上使用最广泛的合同审阅工具——Spellbook 每月处理的合同正接近 50 万份，没有 Claude 就没有我们的今天。”

Scott Stevenson，联合创始人兼 CEO，Spellbook

![The Access Project](https://assets.claude.com/d6661126feb224777780199d17eac5e9d054a66e.png)

> “在 The Access Project，我们构建工具，帮助法律团队和自行应诉的当事人完成记录清除。这个 artifact 让任何人都能启动案底清零流程：筛查资格、获取记录、理解州法律如何适用于每个案件，并找到当地的申报指引。”

Nora Cregan，执行董事，The Access Project

![Zealous](https://assets.claude.com/b89e39e3f6bd810907270b9866cd54e06c8dea2c.png)

> “时间永远不够。花在算数上的每一分钟，都是没能花在了解指控之外那个人身上的时间。Criminal Charge Reality Check 工具始于一个问题：我们怎么让那部分更快，好把时间还给这个人？”

Scott Hechinger，创始人兼执行董事，Zealous

![Accenture](https://assets.claude.com/eef8a51d4b99d31d65fa28d41f247f85bc363b45.svg)

> “在埃森哲，Claude 正在帮助我们转变法律团队的工作方式。我们很高兴有机会重新构想法律工作流，为我们的法律专业人员开辟支持业务的新方式。”

Mindy Lok，法务首席技术官、首席知识产权官，埃森哲

![Crosby](https://assets.claude.com/9815d36508ab5cbef0ba2782bc26371f19356894.svg)

> “Anthropic 在构建最适合法律工作的模型上投入巨大。我们在 Claude 上构建智能体，因为它在我们的内部基准中处于同类最佳水平；我们也很期待继续与 Anthropic 一起推动法律领域的前沿。”

John Sarihan，联合创始人，Crosby

![Docusign](https://assets.claude.com/e71b8b2ebc326b5b33e6e6fd155465e960464b5c.svg)

> “法律位于每一份协议的中心，但这项工作常常与业务的其余部分脱节。通过与 Anthropic 合作，我们把 Docusign 平台的能力直接带入 Claude，让法律团队和跨职能利益相关方能够创建、审阅并推进协议。”

Allan Thygesen，CEO，Docusign

![Eve](https://assets.claude.com/4b6969fb9c8ab337aeaeb462c3f61b08b9e9a09e.svg)

> “在 Eve，我们构建了 PlaintiffBench，用客户标记过的真实草稿、修正和边缘案例，衡量 AI 在原告律师实际工作中的表现。每个新模型在交付给律所之前都必须在那里证明自己，而 Claude Opus 5.5 实现了真正的跃升。对于同时应对数百个案件的原告律所来说，这些小时累积得很快。”

Jay Madheswaran，CEO 兼联合创始人，Eve

![EvenUp](https://assets.claude.com/466446f5f59635a264efe3e688a42b51c0e88976.svg)

> “人身伤害案件不是一步就能完成的。它们要用数月时间，通过在记录、笔记和邮件之间数百个相互关联的判断与任务逐步构建。Claude 是我们信任来编排这项长期工作的前沿模型，让 EvenUp 能按律所及其客户所依赖的标准交付。”

Saam Mashhad，联合创始人兼 CPO，EvenUp

![Filevine](https://assets.claude.com/1309546df049dbb8196876155f61757c6a75ea00.svg)

> “诉讼要求绝对的精确：从海量证据材料中检索出决定案情的事实，并部署专门构建的智能体执行后续动作，无论是为证人做准备还是起草动议。通过把 Filevine 和 LOIS 连接到 Claude，我们的客户可以把这套工具带到任何工作场所，直接在案卷上行动。”

Mike Anderson，CPO，Filevine

![Goodwin](https://assets.claude.com/bd102bc69fc9aeb934061d64f6f03f5f263a41e8.png)

> “我们用 Claude 构建了 AI Governance Benchmark，让任何公司都能走一遍我们的 AI 业务团队与客户使用的同一套问题，看到自己在 AI 治理上的缺口，并知道哪些领域应当优先处理。”

Kaitlin Betancourt，合伙人、AI 业务联席主席，Goodwin

![Harvey](https://assets.claude.com/9447073367b83132335cb2c191c36bef275f48e6.svg)

> “业务团队已经在把问题带到 Claude 那里。Harvey 在他们工作的地方与他们相遇，让法务部门能够设定规则、看到被问到的问题，并介入管理风险。我们很自豪能与 Anthropic 一起构建，让这一切成为可能。”

Matt Zerweck，In-House 产品负责人，Harvey

![Ironclad](https://assets.claude.com/9acaa73e1a36bbf59e1303b4ff18c25ed27c00c7.png)

> “胜出的企业，能以做出决策一样的速度对协议采取行动。Claude for Legal 把 Ironclad 的合同智能直接带入业务团队已经在用的平台。Ironclad 的集成帮助每一位 Claude for Legal 用户行动更快、降低风险、保持合规，让可信 AI 建立在每一份协议、审批和义务之上。”

Sunita Verma，首席技术官，Ironclad

![Ivo](https://assets.claude.com/ba4a38f1d5d4324786c81d44baba0b4e9014388f.png)

> “借助 Ivo 和 Claude，法律团队可以把已经存放在 Ivo 中的合同变成可在团队内共享的 artifacts——比如一份跟踪整个合同组合中每个通知日期的续约日历——无需任何手动上传。每个答案都有其来源合同条款作为依据，而 Ivo 仍然是记录系统。”

Min-Kyu Jung，CEO 兼联合创始人，Ivo

![Legora](https://assets.claude.com/666fbd8fbde356286a5ac8370b994f246c08fb10.svg)

> “随着法律团队在业务的更多环节采用 AI，他们需要在那些环境中获得可信的法律智能。通过把 Legora 连接到 Claude，我们让共同客户更容易在其更广泛的企业 AI 工作流中获得法律问题的答案，并带有回到 Legora 的链接，以便做来源审阅、引证和更深入的法律工作。”

Bryan Tsao，首席产品官，Legora

![Mobile Pathways](https://assets.claude.com/ebea04f981742354f8ac456eec1feb18437fa5ac.png)

> “对我们这些保护移民权利的人来说，变化的速度令人眩晕。而且，落后的后果可能是毁灭性的。Immigration Papers Reader 给资源捉襟见肘的团队提供了跟上节奏、在动荡时期帮助家庭的工具。”

Jeffrey O'Brien，律师，执行董事，Mobile Pathways

![PWC](https://assets.claude.com/99f71ec3e626032e4da0ddfce4dc448b0ba18737.svg)

> “当 AI 融入律师实际工作方式时，它才能在法律领域创造价值。通过与 Anthropic 的联盟，普华永道的工程师和我们的 Legal Business Solutions 团队正在构建由 Claude 驱动的 skills 和集成，直接连接法律团队每天依赖的系统，并具备这个行业所要求的安全与治理。这不是实验，它正在成为法律服务交付方式的一部分。”

Jane Allen，美洲区全球法律业务解决方案负责人、合伙人，普华永道美国

![Rising for Justice](https://assets.claude.com/84b430a68519bd781eae9e6e283e580eb2f7b493.png)

> “对于面临驱逐或背负旧刑事记录负担的华盛顿特区居民来说，法律援助可以改变人生。Rising for Justice 用 Claude 开发工具，帮助律师发现租金账本错误、评估记录封存资格，简化案件准备，让团队能专注于客户的需求与目标。”

Chijioke Akamigbo，律师，执行董事，Rising for Justice

![Solve Intelligence](https://assets.claude.com/2819327500f71d308c553acac2e114468c0e86fa.svg)

> “在我们的化学结构基准上，Claude Opus 5.5 比 Opus 5 多正确识别超过 10% 的结构，同时使用的输出 token 不到一半。在 Solve 中，它驱动从撰写到诉讼级权利要求图表（claim charting）的专利工作。”

Sanj Ahilan，首席研究官，Solve Intelligence

## 司法可及与法律大使计划

模板库包含九个司法可及类 artifacts，其中五个由我们用 Claude credits 支持的公益与公共利益组织构建：

* **Criminal Charge Reality Check，由 [Zealous 构建（在新标签页中打开）](https://zealo.us/)**：输入一项刑事指控，向辩护团队展示量刑范围、这类案件通常如何了结的公开数据，以及标准的释放操作手册。仅限纽约。
* **Immigration Papers Reader，由 [Mobile Pathways 构建（在新标签页中打开）](https://www.mobilepathways.org/)**：把客户的移民文书转化为一份用平实语言写成的初读材料，列出关键日期和缺失的文件。
* **Rent Ledger Reviewer，由 [Rising for Justice 构建（在新标签页中打开）](https://www.risingforjustice.org/)**：在准备驱逐案件时，帮助律师发现房东租金账本中的错误。基于华盛顿特区法律。
* **Record-Sealing Screener，由 [Rising for Justice 构建（在新标签页中打开）](https://www.risingforjustice.org/)**：帮助律师评估客户的刑事记录是否有资格封存。基于华盛顿特区法律。
* **Record Clearance，由 [The Access Project 构建（在新标签页中打开）](https://accessprojectca.org/)**：帮助法律援助团队判断客户的记录能否按其所在州的规则清除。

这是对牛津司法创新者计划（Oxford Justice Innovators Programme）的延续——我们与牛津科技与司法研究所（Oxford Institute of Technology and Justice）和 Microsoft 合作开展的为期 12 个月的项目，支持最多 10 位致力于扩大司法可及性的创新者。

我们同时启动了法律大使计划，这是一个面向用 Claude 构建的法律专业人士的社区，供大家分享工作、相互学习。[加入等候名单（在新标签页中打开）](https://form.typeform.com/to/GyMebQvL)。

## 上手

法律团队可以在 Claude 中[浏览模板库（在新标签页中打开）](https://claude.ai/artifacts?templates=legal)，或从我们的 [Claude for Legal 页面（在新标签页中打开）](https://claude.com/solutions/legal)开始。

要为你的组织规划部署，请联系我们的销售团队，或与我们的一位实施合作伙伴合作，包括埃森哲、AnswerRocket、Caylent、德勤、毕马威、Lazer、Perficient、phData、Protiviti、Provectus、普华永道、Sia Partners 和 Tenex。关于这些合作伙伴的更多信息，请[查看我们的合作伙伴目录（在新标签页中打开）](https://partnerhub.claude.com/directory?filters=1792457729232x209054638212244450)。
