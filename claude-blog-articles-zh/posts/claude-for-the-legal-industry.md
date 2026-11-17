---
title: "面向法律行业的 Claude"
title_en: "Claude for the legal industry"
date: 2026-05-12
source: https://claude.com/resources/articles/claude-for-the-legal-industry
crawled: 2026-11-17
translated: 2026-11-17
---

# 面向法律行业的 Claude

***更新：** Claude for Legal 现已包含[可直接使用的法律工作 artifacts](/resources/articles/introducing-artifacts-for-legal-work)。*

今年早些时候，我们发布了首个法律插件；此后几个月里，法律专业人士已成为所有知识工作职能中 Claude Cowork 参与度最高的用户群体。现在，我们在此基础上推出规模大得多的工具集。

法律工作运行在一套特定的技术栈之上：合同生命周期系统、[研究平台](https://claude.com/resources/articles/working-at-the-frontier-how-thomson-reuters-builds-ai-for-high--stakes-professional-work)、文档管理、电子取证、数据室、律所专有先例，以及更多。Claude 现在通过几个关键构件与这一切相连。首先，[MCP 连接器](https://claude.ai/directory/connectors)把你的法律工作（与特定事项相关的文档、通信和记录）带入 Claude。其次，执业领域插件把律师最常执行的任务打包成即用能力。最后，由于两者都构建在开放协议之上，律所和法务团队可以定制 Claude，使其贴合自己实际的工作方式。[看看 Anthropic 自己的法务团队如何使用 Claude](/resources/articles/how-anthropic-uses-claude-legal)

今天，我们推出 20 多个新的 MCP 连接器，把 Claude 与法律行业已依赖的软件连接起来；以及 12 个针对特定法律工作与执业领域的新插件。最后，我们与 Free Law Project、Justice Technology Association 以及其他致力于让目前无法获得法律服务的人也能触达法律帮助的组织建立合作。

## Claude 在法律团队工作的地方工作

Claude 在法律团队所在之处与之会合：直接工作在 Microsoft Word、Outlook、Excel 和 PowerPoint 之内，并在四个应用之间携带上下文。在 Word 中完成的红线批注，变成 Outlook 中的附函、Excel 中的交割清单、PowerPoint 中的董事会摘要时，不需要重新解释一遍。

在 **Word** 中，Claude 技能（skill）——把团队作业手册与标准编码为可复用的指令——负责起草、红线批注，以及对照这些手册做逐条款比较，并跟踪每一处修改、解释其背后的理由。它们还承担每一轮之间的机械性工作：在草稿发给对方之前清理内部评论、对签署版做最终的格式检查、从已批准的作业手册中调取兜底措辞。

在 **Outlook** 中，Claude 对涌入的事项工作进行分诊：标记合同请求、起草回复与附函、安排后续跟进，让事情不再堆积。

在 **Claude Cowork** 中，同样的连接器与插件可用于跨多份文档的工作：对一批合同做分诊、为某个产品功能做上市放行、为董事会起草监管动态备忘。定时任务可以自动化周期性工作，例如每周的监管更新扫描或收件分诊。

而借助 **Projects**，事项团队拥有一个持久工作空间，先例与既往草稿会在每次对话之间保留。

## 覆盖法律技术栈的新连接器

新的 MCP 连接器让 Claude 能与法律团队已经依赖的系统交互。

**合同生命周期与起草**

* **Definely**：为合同评审提供实时、确定性的合同结构访问——解析定义、校验交叉引用、映射依赖关系，并运行结构化 diff，查看编辑如何在一份协议中传播；
* **Docusign**：把 Claude 连接到你的协议数据，让你快速找出续约日期、义务等关键条款，并在整个合同生命周期中编排协议工作流——从起草、签署到签署后管理；
* **Ironclad**：让 Claude 访问你的合同库与工作流，用平实语言就合同提问，结果自动按每位用户的权限限定范围。

**交易室与交易文档**：

* **Box**：把 Claude 连接到存储在 Box 中的内容，用于搜索和访问文件、查询文档、创建或更新内容、提取元数据字段，同时执行 Box 现有的安全与访问策略；
* **Datasite**：把 Claude 连接到你的 Datasite 虚拟数据室——每年承载数千笔并购交易的安全工作空间——用于建立文件夹结构、邀请用户、搜索文档、跟踪买方问答，并审计数据室的就绪状态。

**文档管理：**

* **iManage**：这个知识工作平台为 Claude 提供受权限约束、可审计的访问，触达受治理的 iManage 内容，包括事项历史、文档与机构知识，无需批量导出或定制集成；
* **NetDocuments**：让 Claude 从你的 NetDocuments 库中搜索和检索文档，并基于你的先例起草新文档，完全尊重组织的权限与治理策略。

**专家网络与技能：**

* **Lawve AI**：提供由执业律师、企业法务和法律技术专家撰写的精选法律 AI 技能库，可在 Claude 内搜索；
* **The L Suite**：从其领先的企业法务社区提供两个 MCP 连接器：（1）**Lloyd**，让 The L Suite 会员把 Claude 与 Braintrust 会员平台连接；（2）**TopCounsel**，基于 The L Suite 的专有数据集与排序算法，帮助任何企业法务为特定事项找到合适的外部律师。

**电子取证与审查：**

* **Consilio**：把客户自己正在进行的活跃事项与 Consilio 的 Aurora Legal AI 放到 Claude 指尖，每个响应都限定在用户本就有权查看的范围内；
* **Everlaw**：这一诉讼平台让 Claude 使用元数据、关键词和文档类型在 Everlaw 项目中搜索、组织和检索文档，并提供直达审查的链接；
* **Relativity**：让 Claude 在其法律数据智能 AI 平台 RelativityOne 中建立事项、设计工作空间 schema、治理访问权限并分析使用情况。

**达到受托责任标准的工作流：**

* **Thomson Reuters**：把 Claude 连接到 CoCounsel Legal——一个达到受托责任标准（fiduciary-grade）的系统，覆盖所有主要执业领域的端到端起草、研究、审查与校验，作为高利害法律工作的 AI 助手，以 Westlaw 一手法律资源、Practical Law 指引、KeyCite 以及你自己的文档为依据，输出透明且可验证。

**法律研究与判例法：**

* **Legal Data Hunter**：让 Claude 访问全球增长最快的法律语料库：来自 160 多个司法辖区的 3100 多万份文档，包括欧盟合并法、最高法院与宪法法院判例法，以及官方学说；
* **Midpage**：把 Claude 连接到判例法数据库，用于复杂法律研究、判决书审查与工作成果，所有内容都超链接到真实来源，便于核实；
* **Trellis**：让 Claude 直接访问全美最大的州初审法院数据集，包括案卷、裁定、裁决与诉讼文件，用于法官与对方律师分析及动议起草。

**法律 AI 助手：**

* **Harvey**：把 Harvey 的法律智能带入 Claude，支持通用法律问询、对 Vault 项目的分析，以及针对选定知识来源的研究问题；
* **Solve Intelligence**：把 Claude 连接到专利与非专利文献、法律文本、标准必要专利（SEP）技术标准以及开放网络，用于现有技术检索、权利要求映射与专利起草。

**公共服务**

* **BoardWise**：为面临州执业委员会事项的持证专业人士提供指引：帮助他们理解截止日期、应对自身处境，并起草针对其司法辖区定制的结构化回复函；
* **Courtroom5**：为约 80% 没有律师出庭的民事诉讼当事人提供法律指引，覆盖全部 50 个州，具备司法辖区感知的案件受理、截止日期计算与下一步指引；
* **Descrybe**：为 Claude 提供处理一次法律资源的法律研究工具：按概念或引证检索案件、检查处理状态、查找引用权威、核验引文措辞；
* **Free Law Project**：把 Claude 连接到 CourtListener 的数百万份美国法院判决、PACER 案卷、法官档案、口头辩论与引证数据。

## 执业领域插件

同一个法律问题，坐在不同位置上看是不同的。我们发布 12 个执业领域插件（可从 [Legal Marketplace 此处](https://github.com/anthropics/claude-for-legal) 下载），每一个都围绕特定法律角色构建。每个插件都以一段简短的设置访谈开始，了解你的执业方式：你的作业手册、你的升级链、你的风险校准、你的行文风格——这样 Claude 的答案就不是泛泛而谈，而是为你的团队量身定制。这些插件包括：

* **Commercial Legal** 对照你的作业手册审查供应商协议与 NDA，并以业务利益相关者能读懂的平实语言摘要路由升级。
* **Corporate Legal** 处理并购：数据室尽调、披露清单、董事会同意书与交割清单。可配置为董事会工作、上市公司治理或实体合规。
* **Employment Legal** 覆盖招聘、解雇、劳动者分类、休假截止日期与调查，并起草内置州别规则的政策。
* **Privacy Legal** 对照你的作业手册审查 DPA，对 PIA 与 DPIA 做分诊，在法定期限内准备 DSAR 回复，并标记书面政策与实际做法之间的差距。
* **Product Legal** 对照你的内部框架执行上市评审，核查营销主张是否有依据，并回答来自业务各部门的风险问题。
* **Regulatory Legal** 监测监管动态，按你的重要性阈值过滤，将新规与你的政策库比对，并跟踪缺口与意见反馈截止日期。
* **AI Governance Legal** 按你的治理分级对 AI 用例做分诊，执行影响评估，审查供应商 AI 条款，并可起草一份初始 AI 政策。
* **IP Legal** 执行商标清查与自由实施（FTO）分诊，起草并回复停止侵权函，处理 DMCA 下架与开源合规，并筛选发明披露。
* **Litigation Legal** 管理事项受理与案件组合跟踪、法律保全、索赔函、传票分诊、时间线、庭外证言准备、特权日志与书状起草。
* **Law Student** 提供苏格拉底式提问训练、判例摘要、IRAC 评分与律师资格考试备考，并包含按司法辖区区分的差异点。
* **Legal Clinic** 管理客户受理、截止日期跟踪、案件备忘与督导审查队列。
* **Legal Builder Hub** 从公共注册表查找并安装社区构建的法律技能，对每次安装与更新执行安全审查、许可证检查与新鲜度检查。

每个智能体模板都能一键安装到 Cowork 或 Claude Code 中，产出的成果符合机构起草标准。其中[一部分](https://github.com/anthropics/claude-for-legal)（Commercial Legal、Corporate Legal、Litigation Legal、Product Legal、Litigation Legal）还以 cookbook 形式提供，可部署为 Claude Platform 中的托管智能体（Managed Agents）用于程序化调用。团队可以叠加自己的先例与作业手册来定制这些技能。

每家法律组织的工作方式都不同，没有哪一套插件能覆盖所有执业场景。插件与技能生态基于开放协议，包括 **Box、Legal Quants、Lawve AI** 和 **Thomson Reuters** 在内的早期贡献者已经发布了自己的技能、插件与风格约定。任何合作伙伴都可以通过 [Directory](https://claude.ai/directory) 提交连接器与技能。

## 用 AI 让法律服务更可及

对许多人和小企业来说，法律服务遥不可及，而且这一差距还在扩大。我们正与 **Free Law Project**、**Justice Technology Association** 以及其他法律援助与公共服务组织合作，帮助让法律服务更可负担、更可获得。

符合条件的法律援助诊所、公共辩护人和非营利法律服务组织，可以通过 [Claude for Nonprofits 计划](https://claude.com/solutions/nonprofits)获得大幅折扣的定价。BoardWise、Courtroom5、Descrybe 和 Free Law Project 提供的免费或低成本工具，也可通过 MCP 连接器供 Claude 用户使用。

> "大多数人在还来得及行使权利之前，根本不知道自己拥有这些权利。Claude 现在可以在他们所在的地方与他们相遇——就在他们害怕、正在寻找答案的那一刻。"—— Sonja Ebron，Courtroom5 首席执行官兼联合创始人

## 在整个法律行业获得信任

律所与法务团队已经从"试用 Claude"走向"用 Claude 运营业务"；而他们所依赖的法律工具，也越来越多地构建在 Claude 之上。在二月的 [Briefing: Enterprise Agents](https://www.anthropic.com/events/the-briefing-enterprise-agents-virtual-event) 活动上，Thomson Reuters 展示了基于 Claude Agent SDK 重建的 CoCounsel；随着今天的发布，这一集成变为双向。Harvey、Solve Intelligence 以及下文提到的其他公司也在做同样的事。

这些更新构建在 Claude Opus 4.7 之上——这是我们面向法律推理与长文档工作公开提供的最强模型。

以下是法律团队与生态合作伙伴告诉我们的、与 Claude 合作的情况：

![EvenUp](https://assets.claude.com/466446f5f59635a264efe3e688a42b51c0e88976.svg)

> "人身伤害（PI）法律对 AI 提出了最严峻的一些挑战：在大量病历与账单数据中进行推理、识别关键事实，并以一致性和准确性执行复杂工作流。Claude Opus 4.8 带来了全新水平的推理、可靠性和长上下文表现。EvenUp 在此基础上叠加了专有的人身伤害数据、领域专业能力和专门构建的工作流。"

Rami Karabibar，首席执行官兼联合创始人

![Solve Intelligence](https://assets.claude.com/2819327500f71d308c553acac2e114468c0e86fa.svg)

> "我们看到 Claude Opus 4.7 的多模态理解有了重大提升，从读取化学结构到解读复杂技术图表。更高的分辨率支持正帮助 Solve Intelligence 为生命科学专利工作流打造一流工具，覆盖从起草、审查到侵权检测与无效权利要求图的各个环节。"

Sanj Ahilan，首席研究官

![Eve Legal](https://assets.claude.com/f1efc487a08ab700dd2f0a0d09e717745da3e2d0.svg)

> "我们用 24 个以上法律专用评分器评估每个模型——引证准确性、无依据的判例引用、记忆泄漏、拒答正确性——因为在诉讼中，一个听起来权威的幻觉比没有答案更糟。在法律工作真正重要的指标上，尤其是依据性和引证忠实度，Claude 每次都在我们的内部对比评测中胜出。这就是我们把流水线中风险最高的部分跑在 Anthropic 上的原因。"

Jay Madheswaran，首席执行官兼联合创始人

![Freshfields](https://assets.claude.com/631c9f975e09f01ae344ef9004351099cc0d918b.svg)

> "我们在 Freshfields Lab 的方法一直是构建在可用的最佳技术之上。Claude 的能力已成为我们自研 AI 驱动解决方案的重要组成部分。通过这次合作，我们走得更远：与 Anthropic 共同开发能够端到端处理多步骤法律任务的智能体工作流。对我们的客户来说，这意味着更快、更精准、更可扩展的法律服务。"

Gerrit Beckhaus，合伙人兼联席负责人

![Accenture](https://assets.claude.com/eef8a51d4b99d31d65fa28d41f247f85bc363b45.svg)

> "我在 Accenture 的法务团队把 Claude 用于日常法律事务，看到生产力提升能够真正实现，我们非常兴奋。"

Mindy Lok，全球知识产权法务负责人兼法务首席技术官

![Thomson Reuters](https://assets.claude.com/3c80d8dc7dbf6556d1137977873dee26eaffae1d.svg)

> "AI 的未来不会由工作发生在哪里来定义，而会由结果是否可信来定义。在专业场景中，这意味着 AI 要以权威内容为依据、经过准确性校验，并把安全性构建在核心之中。这是可信 AI 的下一个前沿，也是 Thomson Reuters 通过与 Anthropic 的合作所处的位置。"

Joel Hron，首席技术官

![Quinn Emanuel Urquhart & Sullivan](https://assets.claude.com/9a319a911bf5466e2baf48bd08ee6bb10df98427.png)

> "我几乎没有编程背景，却在 Claude 上搭起了我们的诉讼平台——我需要它应对一场真实的庭审。突破点在于把 Claude 当作案件团队的一员：像给中途加入的合伙人做入职一样，用时间线、关键摘录和案由主题给它做入职。产出的工作成果远远超出我一个人能做到的——大概是永远做不到的。"

Christopher D. Kercher，合伙人，AI 与数据分析创始人兼负责人

![Harvey](https://assets.claude.com/9447073367b83132335cb2c191c36bef275f48e6.svg)

> "法律是 AI 转型最引人注目的行业之一，这也是我们为深化与 Anthropic 的合作感到兴奋的原因。Claude Opus 4.7 在 Harvey 的 BigLaw Bench 上得分 90.9%，是所有 Claude 模型中最高的；Harvey for Claude 连接器则把我们的法律智能直接带入 Claude。"

Winston Weinberg，首席执行官兼联合创始人

![Crosby](https://assets.claude.com/9815d36508ab5cbef0ba2782bc26371f19356894.svg)

> "Claude for Word 把 Claude 智能体的能力带进了律师关键的日常工作流。这让我们的团队能专注于最重要的事：律师把专家判断用于复杂的边缘案例，工程师则利用丰富的上下文为客户构建可自我改进的系统。"

Ryan Daniels，联合创始人兼首席执行官

![Legora](https://assets.claude.com/666fbd8fbde356286a5ac8370b994f246c08fb10.svg)

> "Opus 4.7 在复杂法律工作的推理上又前进了一步——长文档中的一致性更强、对细微指令的处理更好，在高利害工作流中的可靠性也更高。Anthropic 构建底层智能；Legora 将其转化为可投入生产的系统，把 Claude 嵌入律师在实践中能够信任的工作流、防护措施与界面之中。正是这种组合为法律专业人士带来真正的影响。"

Jake Lauritzen，首席技术官

![Holland & Knight](https://assets.claude.com/b8faaa7f6a90ceca02b29e39d7376ccd7dedda75.svg)

> "在 Holland & Knight，我们很欣赏 Everlaw 与 Anthropic 的合作，并通过 MCP 提供对其工具的访问。我们正在许多诉讼工作流中应用 Claude 的能力，并看到了在正确上下文中实现它们的巨大潜力。Everlaw 让我们能把正确的证据带入等式，释放出额外的力量。"

Manfred Gabriel，合伙人

## 开始使用

[新连接器](https://claude.ai/directory/connectors)与[执业领域插件](https://github.com/anthropics/claude-for-legal)都是开源的，并可在 Claude Cowork 中使用。企业管理员可以在工作空间设置中启用它们。[在此了解更多](http://www.claude.com/solutions/legal)或[联系我们的销售团队](https://claude.com/contact-sales)。

注册我们的[发布网络研讨会](http://website.anthropic.com/webinars/how-legal-teams-put-claude-to-work)，现场观看新功能演示——我们会做产品实机走查，并讲解律所与法务团队如何最大化利用 Claude 及互联生态。构建者也可以通过 Legal Quants 和 Lawvable 探索社区维护的技能。

有意合作的法律援助与司法可及性组织，请通过我们的 [Nonprofits 计划](https://claude.com/solutions/nonprofits)联系我们。
