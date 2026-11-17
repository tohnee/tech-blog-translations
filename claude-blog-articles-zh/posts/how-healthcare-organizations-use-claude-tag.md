---
title: "医疗健康机构如何使用 Claude Tag"
title_en: "How healthcare organizations use Claude Tag"
date: 2026-09-14
author: Camy Pearson
source: https://claude.com/resources/articles/how-healthcare-organizations-use-claude-tag
crawled: 2026-11-17
translated: 2026-11-17
---

# 医疗健康机构如何使用 Claude Tag

> 原文：[How healthcare organizations use Claude Tag](https://claude.com/resources/articles/how-healthcare-organizations-use-claude-tag) · Claude 博客

*Insight Health、Tennr 和 Medallion 如何借助 Claude Tag 构建人类-智能体团队。*

医疗健康机构正在使用 [Claude Tag（beta）](https://support.claude.com/en/articles/15594475-what-is-claude-tag)。它把 Claude 作为[团队成员](https://academy.claude.com/courses/building-effective-human-agent-teams)引入 Slack，帮助机构分诊生产环境告警、维护内部工具、解答支付方规则相关问题。Claude Tag 目前尚未被纳入 Anthropic [《商业伙伴协议》（BAA）](https://support.claude.com/en/articles/8114513-business-associate-agreements-baa-for-commercial-customers)的保障范围，但已有数家医疗健康机构在使用它——所用频道与连接器都不会接触受保护健康信息（PHI）。

在频道里 @Claude，它就会读取整个话题串、调用你连接好的工具、完成工作并回报结果。它会记住每个频道里发生的事，因此长期运行的工作无需反复交代；只要你允许，它还能盯住某个频道，自行介入。

管理员决定 Claude Tag 在哪些地方工作、能访问什么，因此医疗团队可以让 Claude Tag 避开存放 PHI 的频道与系统：

* Claude Tag 可以默认关闭，**仅在获批频道中启用**，同时禁用私信，并**按频道限定连接器范围**。
* Claude Tag 并不会读取整个 Slack——它只能看到工作区成员能看到的内容。它可以读取工作区的公开频道并按关键词搜索，但对未被邀请加入的私有频道没有访问权限。
* **访问权限包（access bundles）**让团队可以在某个频道里连接代码库、问题跟踪器等数据源，同时无法访问 EHR、临床系统与患者沟通记录。关于 Claude Tag 的[智能体身份与访问模型](https://claude.com/resources/articles/agent-identity-access-model)及其完整架构，详见[安全与数据处理文档](https://claude.com/docs/claude-tag/concepts/security-and-data?open_in_browser=1)；医疗健康机构的最佳实践见[此处](https://claude.com/docs/claude-tag/admins/healthcare)。

已启用 Claude Tag 并关联 GitHub 的 Enterprise 组织可获得 25,000 美元的 Claude Tag 额度（10 个席位以上的 Team 组织为 2,500 美元）；请注意，这些额度将于 2026 年 10 月 1 日过期。额度详情见[此处](https://support.claude.com/en/articles/15575654-claude-tag-launch-promo-for-claude-team-and-enterprise)。

下面来看 Insight Health、Tennr 和 Medallion 目前如何借助 Claude Tag 构建[人类-智能体团队](https://claude.com/resources/articles/building-effective-human-agent-teams)。

#### **在 Insight Health 运行事件响应**

Insight Health 打造了 MagicDocs，一款面向专科医疗机构、充当转诊协调员的 AI 产品。MagicDocs 会读取接入的患者文档（传真、转诊单、预授权申请、化验单和病历），抽取临床细节，把每份文档匹配到正确的患者，并把结构化数据写入 EHR。该公司服务 56 个专科的 1,100 多家机构。

随着客户规模扩大，生产环境告警的分诊工作不断侵蚀这支精干工程团队本应用于更高价值工作的时间。因此过去三个月里，公司在其不含 PHI 的工程与支持频道中运行 Claude Tag，由它调查生产告警、提交并去重工单、评审 PR，并把上下文从一个话题串带到下一个。

在高流量的生产告警频道中，他们把 Claude Tag 与第二个智能体 Zeus（由 Insight Health 基于 Claude Agent SDK 构建）配对，让一次事件从首次通知一路走到经过测试的修复。两个智能体的访问权限被刻意区分：Claude Tag 能看到代码库和 Linear，因此了解代码模式与工单历史；Zeus 运行在公司受 BAA 覆盖的 Claude API 组织上，因此可以查询生产数据，并在数据进入 Slack 之前对 PHI 做脱敏。告警到达后，两个智能体会展开调查——查询生产数据、对照代码与近期部署、并与历史工单比对——同时把进展汇报在 Slack 话题串里。一旦定位根因，它们就开一个草稿 PR 并监控测试，最后由工程师审核并合并。Claude Tag 的频道记忆在这里很有价值：它能把一条新投诉识别为已知问题且修复在途，能回想起几周前的调查，还能无需提示就遵循常设指令。

“Slack 频道里的每个人都能看到两个智能体的推理过程以及它们如何分工，”Insight Health 联合创始人兼 CTO Saran Siva 说。“这种透明度建立了信任，也教会团队如何从智能体身上获得最大价值。”自 Claude Tag 上线以来，Insight Health 关键告警频道中 97% 的告警在无需工程师介入的情况下关闭，让团队得以专注于核心产品工作。

除事件处理之外，Insight Health 团队还把 Claude Tag 用于招聘、供应商谈判准备、合同评审（把条款与通话记录逐项核对）以及日常业务运营。

#### **在 Tennr 维护内部工具**

Tennr 是一个患者流程编排平台，通过自动化接诊、文书、授权与排期等原本会拖慢诊疗的工作，帮助医疗机构更快把患者送入合适的诊疗场景。Claude Tag 常驻其内部工具环境，帮助非技术团队搭建和维护定制的内部应用。

在 Tennr 这样高速增长的公司，内部工具建起来有多快，死得就有多快，因为没人有余力维护。2026 年 7 月，Tennr 在搭建内部工具时换了做法。它上线了 recruiting.tennr.com——一个用 Claude Code 构建的内部 offer 展示门户——并通过一个专门的 Slack 频道，让 Claude Tag 成为其主要维护者。如今，真正使用这个工具的人（招聘人员、People 团队成员、用人经理和 RevOps）用平实的英文 @Claude 提出需求，Claude 就完成代码改动、部署并回报结果。他们可以直接迭代这个工具，而无需把工程师从产品工作中抽走。

大约一个月内，团队以此方式完成了 15 个以上工单：根据上传的一页纸 PDF 搭建的福利详解板块、链接到 Dropbox Sign 的“在此签署 offer”横幅、目标奖金字段，以及自助管理控制项。当一个公开暴露的 copy API 被标记出来时，Claude 当天就把它锁定了访问。当一个 Ashby 导入 bug 不断把在途 offer 上的股权重置时，Claude 修复了 bug 并把更正后的数值同步到各处。当另一个 bug 曾短暂地把候选人的浮动薪酬显示错误时，Claude 未经要求便发布了全频道通知，说明受影响的时间窗口与补救措施。它还撰写了该工具的上手文档，并负责权限管理。

团队在频道里教会了 Claude 自己的运维惯例，包括 emoji 状态图例，以及一种工单格式：编号工单、提出人、commit 链接、截图和实时测试链接。Claude 此后便沿用了这些惯例。招聘人员用自然语言提交相当于工程工单的需求——有时只是一张截图——就能在一小时内拿到生产环境的改动。“Claude Tag 是让内部工具真正可行的关键，”Tennr 业务运营与战略副总裁 Abe Griffiths 说。“有了 Claude 通过 Slack 频道担任工具的管家，真正使用工具的人可以直接迭代它，而无需把工程师从产品工作中抽走。”

推广很快，因为基础已经打好。Tennr 只允许 PHI 出现在有限的几个私有频道中，因此大范围引入 Claude Tag 并未带来新的数据问题。让 Claude Tag 容易获批的关键，是按频道限定范围。

“在 offer 工具频道里，我们希望 Claude 主动出击：修复问题、修改代码、跳过 PR 评审、直接发布，”Griffiths 说。“这种姿态显然不适合比如产品频道或工程频道——在那些地方，Claude 的角色更接近信息收集或帮我们保持条理。能够逐个频道划清界限，意味着我们可以在低风险的地方给 Claude 真正的自主权，而不是到处都放权。”

#### **在 Medallion 积累支付方专业知识**

Medallion 为医疗健康机构自动化提供方资质认证、执照办理与支付方登记。这类工作很大程度上依赖晦涩、无文档记录的规则：哪些支付方要求一个团体在登记前必须拥有最低数量的已认证提供方、各州特有的法规，以及工程师在把某个流程固化为产品之前需要得到答案的几十个类似问题。过去，这些答案掌握在一小批内部医疗领域专家手中，为核心产品开发决策制造了持续的人为瓶颈。

如今 Claude Tag 进入了这一环，打破了知识孤岛。当工程师在 Slack 里提出支付方规则问题时，Claude Tag 会基于过往专家回复、历史数据和非结构化内部资料作答。专业知识沉淀在频道里，而不是只装在某个人的脑子里。

“当它没有把握时，它会拉入合适的专家，而专家的回复会成为未来相关主题答案的基础，”CTO Armaan Sarkar 说。

是什么让他们放心推广 Claude Tag？Sarkar 指出三点：选对不含 PHI 的工作流、专家复核、自动化校验。Claude Tag 在政策层面运作：问题关乎支付方规则与流程，而非个别患者或提供方。它并非独自作答：专家提供监督与更正，且每次交流都发生在公司任何人都可审计的 Slack 频道中。输出还会在下游被检查，因为 Medallion 的系统会用这些政策采取行动，而这些行动本身会被审计与校验。

#### **如何开始**

上述团队的起点都一样：从工程、产品、运营或招聘频道开始，只接一两个连接器，在公开话题串而非私信里工作，以便整个团队都能审阅并接上上下文。

先阅读医疗健康机构的 Claude Tag 最佳实践（见[此处](https://claude.com/docs/claude-tag/admins/healthcare)），然后从一个频道开始。为告警频道或支持工程频道开启 Claude Tag，连接 GitHub，让团队先用两周，再扩大允许列表。

***开始使用 [Claude Tag](https://support.claude.com/en/articles/15594475-what-is-claude-tag)。***
