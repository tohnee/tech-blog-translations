---
title: "集中管理 MCP 连接器的授权"
title_en: "Centrally manage authorization for MCP connectors"
date: 2026-06-18
source: https://claude.com/resources/articles/enterprise-managed-auth
crawled: 2026-11-17
translated: 2026-11-17
---

# 集中管理 MCP 连接器的授权

> 原文：[Centrally manage authorization for MCP connectors](https://claude.com/resources/articles/enterprise-managed-auth) · Claude 博客

***更新：企业托管授权（Enterprise-managed authorization）现已正式发布，在原有支持 Asana、Atlassian、Canva、Figma、Granola、Linear 和 Supabase 的基础上，新增支持 Datadog、Notion 和 Slack，Exa、Miro 和 Zoom 即将支持。（2026 年 8 月 24 日）***

管理员现在可以通过身份提供方为整个组织配置 MCP 连接器，首发支持 Okta。用户在首次登录时即自动获得连接器访问权限，授权由组织集中配置。

连接器让 Claude 在工作中更有用——它们让 Claude 从团队已在使用的工具中获取所需的上下文。此前，启用连接器需要两步操作：管理员先为组织启用连接器，然后每个用户还要自行授权。

企业托管授权简化了第二步。管理员只需对连接器授权一次，用户通过已有的 IdP 组和角色继承访问权限，此后第一次打开 Claude 时连接器就已经就位。最终效果是：终端用户零操作完成连接器设置。

企业托管认证（enterprise-managed auth）是 Model Context Protocol 的 [Enterprise-Managed Authorization 扩展](https://modelcontextprotocol.io/extensions/auth/enterprise-managed-authorization)的首个实现。它构建在开放标准之上，因此任何连接器都可以支持它——包括你们自己团队构建的自定义连接器——并且对所有 Claude 客户而言工作方式完全一致。

### 工作原理

将身份提供方连接到 Claude，并选择为组织启用哪些 MCP 连接器。员工登录时，所需连接器已经在位。访问权限在 Claude 对话（Claude chat）、Claude Code 和 Cowork 中保持一致。

对管理员而言，这等于把 MCP 访问管理并入了治理其余技术栈的同一套工作流：一次配置、按组划定范围、通过 IdP 管理撤销。由于借助 IdP 校验访问权限几乎不产生额外摩擦，管理员可以缩短访问令牌的有效期而不影响生产力——因此当某人被取消配置后，其连接器访问权限会很快失效，而不是挂在一个旧令牌上继续存在。访问经由你已经信任的身份提供方，因此连接器与其他一切系统处于相同的安全与访问控制之下，而不是一个需要单独监控的暴露面。

管理员还可以要求某个连接器只能通过 IdP 建立连接，从而把工作用途与个人用途干净地隔离开，并防止有人意外把个人账号关联到工作工具上。

### 与生态共同构建

企业托管授权在三个群体之间协同运作：治理访问权限的身份提供方、支持该标准的 MCP 提供方，以及在各自团队中部署托管连接的 Claude 客户。

**身份提供方。** 发布时支持 Okta，更多身份提供方的支持即将到来。

**MCP 提供方。** Asana、Atlassian、Canva、Figma、Granola、Linear 和 Supabase 在发布时即支持企业托管认证，Slack 即将支持。

**Claude 客户。** HubSpot、Ramp 和 Webflow 等组织正在其团队中推广企业托管认证。

![Slack](https://assets.claude.com/d28a34b6acf04e16d9b8806ee16d3ca66f00b389.svg)

> 「Slack 是人与智能体并肩工作的地方——在同一个对话里、共享同一份上下文、朝同一个目标努力。通过 Slack MCP 服务器，这一切都可以为 Claude 所用，而且不只是读取，还能采取行动。企业托管认证意味着组织可以无摩擦地为所有用户开放访问。安全团队通过现有身份提供方配置一次，用户就能无缝获得访问。」

Rod García，工程副总裁

![Supabase](https://assets.claude.com/e42031c6a0e0c0cd1f5f598d9efb9e640b1fc6b3.svg)

> 「过去要通过 Claude 使用 Supabase，你要么是组织所有者，要么给团队里的每个人分发个人访问令牌（Personal Access Token）。企业托管认证解决了这个问题：由你的 IdP 控制访问和角色，构建者可以用 Claude 探索和查询他们的数据，而 IT 无需为此在安全上妥协。」

Bil Harmer，首席信息安全官

![Webflow](https://assets.claude.com/5ad498f237d04754725acb0af0c23e5d27611d33.svg)

> 「我们的团队打开 Claude，他们被授权的每个工具都就在那里，范围由 IT 已经在维护的身份组划定。企业托管认证让 AI 变成了人们直接使用、而不是需要申请的东西，我们正在把这一做法推广到整个 Webflow。」

Reed Shackelford，企业 AI 运营高级经理

![Asana](https://assets.claude.com/b8ffecd4a133f2860151d51156002816a54772e7.svg)

> 「企业托管认证是实现 Asana 作为『人机团队操作系统』愿景的一个奠基性里程碑。通过为企业提供一种安全、可控的方式把 Claude 连接到最关键的工作流，我们释放了在整个企业范围内扩展 AI 驱动价值的能力——并且具备大规模部署所要求的绝对治理、合规与信任。」

Arnab Bose，首席产品官

![Atlassian](https://assets.claude.com/4870b3d6c0253cea01b100c98ad2030b8e4f8ce1.svg)

> 「企业托管认证让 Atlassian Rovo MCP 更容易被 Claude Enterprise 客户大规模采用，为员工提供了一种简单方式，把 Claude 连接到他们已在依赖的 Jira、Confluence 和 Teamwork Graph 上的 Atlassian 工作。同样重要的是，它给管理员提供了一个集中位置来管理 MCP 客户端的访问权限，使组织能够更快推进 AI，同时维持他们所期望的治理。」

Brendan Haire，Rovo 与 AI 工程副总裁

![Canva](https://assets.claude.com/f047885ca3dadf9a16509752ef150ebb9bd424bb.svg)

> 「Canva 已获得 95% 的《财富》500 强企业信任，我们的 MCP 服务器让更多团队能在同一工作流中，用 Canva 的 AI 与设计工具创建、编辑并发布符合品牌规范的设计。与 Okta 配合的企业托管认证，让企业用一套已经信任的系统来管理 AI 访问变得清晰而简单，使团队能够安全、规模化地用 AI 创作。」

Anwar Haneef，总经理兼生态负责人

![Figma](https://assets.claude.com/30df15cbd261edbc52262a1fa2d1339f3a1a372b.svg)

> 「Figma MCP 把代码与画布的力量结合起来，让团队行动更快、探索更多，并交付脱颖而出的产品。随着 MCP 采用度提高，企业托管认证让企业能够安全地扩展其 MCP 部署，同时不拖慢团队。」

Devdatta Akhawe，工程副总裁

![Granola](https://assets.claude.com/3db5669fc35f363040dcf5ec573f2401d3f0e1a0.svg)

> 「很高兴看到 Anthropic 和 Okta 让企业能够安全、集中、规模化地连接到 MCP 服务器。Granola 帮助团队捕捉工作中最重要的一些上下文：决策、细节以及随之而来的跟进事项。MCP 让这些内容在各类团队工具中发挥作用，而企业托管认证让它能够无摩擦地在各团队间可用。」

Chris Pedregal，首席执行官兼联合创始人

![Hubspot](https://assets.claude.com/d6f4aa0286766975a05548621fb66283ec2bfe32.svg)

> 「企业托管认证正是我们在 MCP 连接上一直寻找的安全性和用户体验。人们只需用 Okta 完成一次标准登录，就能带着个人上下文连接到我们软件生态中的所有 MCP 主机。个人身份得以贯通，同时没有人会被一大堆 OAuth 授权搞得晕头转向。这对企业管理是巨大的胜利，尤其是再配合对那些 MCP 主机所暴露的各个工具进行选择性控制。」

Andrew Meinert，系统运营与 AI 总监

![Linear](https://assets.claude.com/02794cae131d86ae8d46e3238f14d1a7ad685181.svg)

> 「登录一次，所有 MCP 连接器就自动配置好，这感觉相当神奇。」

Tom Moor，工程负责人

![Okta](https://assets.claude.com/87c2bb73c73e8c1bfcd74b6f3535cb097f060b2b.svg)

> 「围绕 MCP 的势头令人难以置信，但当我们迈向互联的 AI 劳动力时，安全不能是事后才想到的事。通过把 Cross App Access 协议作为 Enterprise-Managed Authorization 扩展嵌入 MCP，并在 Claude 生态中实现它，我们把身份变成了一个集中的治理平面，为安全团队提供严格的合规控制，也为用户带来无缝、安全的体验。」

Aaron Parecki，身份标准总监

![Ramp](https://assets.claude.com/6db782273272dd89f11df7b54089328994fe718e.svg)

> 「在企业托管认证之前，让新员工用上完整的工具栈意味着要为每个连接器排队等待 OAuth 审批。现在他们在第一天登录 Claude 时就已经连接就绪——2,000 名员工，通过 Okta 配置，零额外步骤。」

Cameron Leavenworth，AI 方向资深 IT 工程师

### 开始使用

企业托管认证目前以 beta 形式向 Claude Team 和 [Enterprise](https://claude.com/solutions/enterprise) 方案的客户提供。[在我们的帮助中心了解更多](https://support.claude.com/en/articles/15537633)，并[申请访问权限](https://claude.com/form/ema-waitlist)以开始使用。

任何身份提供方或 MCP 提供方都可以通过实现 MCP 授权规范的[开放扩展](https://blog.modelcontextprotocol.io/posts/enterprise-managed-auth)来支持企业托管认证。有意加入 beta 者可[在此提交意向](https://docs.google.com/forms/d/e/1FAIpQLSf1goHGNDVFK7rncYuh6wnRpWSy7eGOcgL1i8uw3oyKFO9UUA/viewform?usp=sharing&ouid=101055591948883487705)。
