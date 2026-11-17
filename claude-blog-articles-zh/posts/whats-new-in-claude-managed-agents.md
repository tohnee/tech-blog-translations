---
title: "Claude Managed Agents 新功能：按计划运行智能体，并将环境变量存入 Vault"
title_en: "New in Claude Managed Agents: run agents on a schedule and store environment variables in vaults"
date: 2026-06-09
source: https://claude.com/resources/articles/whats-new-in-claude-managed-agents
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude Managed Agents 新功能：按计划运行智能体，并将环境变量存入 Vault

> 原文：[New in Claude Managed Agents: run agents on a schedule and store environment variables in vaults](https://claude.com/resources/articles/whats-new-in-claude-managed-agents) · Claude 博客

从今天起，[Claude Managed Agents](https://claude.com/resources/articles/claude-managed-agents) 可以按计划运行，并能安全地访问 CLI 工具和其他需要认证的服务。这两项功能现已在 Claude Platform 上以公开 beta 提供。

## 定时部署：按计划运行智能体

智能体现在可以按计划运行，自动完成日常性工作。[定时部署](https://platform.claude.com/docs/en/managed-agents/scheduled-deployments)（scheduled deployment）会按 cron 计划运行一个 Claude Managed Agent。每次计划触发时，智能体都会启动一个新会话并完成任务，你无需自己构建或托管调度器。

可以把它用于夜间数据同步、每周合规扫描或每日摘要这类周期性工作。部署上线后，你可以随时暂停、恢复或归档，也可以按需触发额外运行。

![](https://assets.claude.com/baff2128f2d026b8c6892798adfc4021170bce04.png)

已有团队在用定时部署自动化周期性工作：

* [Rakuten](https://claude.com/customers/rakuten-qa) 使用定时部署，按每周或每月的计划分析电子表格数据并产出报告和演示文稿。团队还用它监控生产日志和指标，让产品经理无需搭建仪表盘就能了解应用健康状况。
* [Actively AI](https://actively.ai/) 使用 Managed Agents 为销售团队提供跨账户的智能体式搜索。定时部署会定期刷新答案，并通过替换团队最初自行搭建的调度基础设施，简化了他们的技术栈。
* [Ando](https://ando.so) 使用定时部署让招聘和销售团队保持推进。智能体会自主监控频道中提出的下一步动作，在到期时跟进，并发送会议提醒。

## Vault：存储环境变量，为 CLI 和其他工具完成认证

[Vault](https://platform.claude.com/docs/en/managed-agents/vaults) 为 Claude Managed Agents 安全地存储环境变量和凭证。运行时，智能体以环境变量的形式访问 API 密钥等机密信息，从而能够为 CLI 工具和其他服务完成认证，而无需把凭证硬编码进提示词或代码中。

智能体通过直接 API 调用、CLI 和 MCP [连接外部系统](https://claude.com/resources/articles/building-agents-that-reach-production-systems-with-mcp)。CLI 让智能体可以通过 shell 直接驱动现有的命令行工具，是一条快速、轻量的集成路径。把 API 密钥与一个环境变量名以及它可访问的域名一起注册，智能体沙箱中安装的 CLI 就能用它发起已认证的 API 调用。

智能体永远看不到你的密钥，因为沙箱中只持有一个占位符。真实密钥在网络边界处注入，且仅在你允许的域名请求上注入，因此它只会去往你批准过的地方。要更换密钥，只需在 Vault 中更新，正在运行的会话会在下一次调用时取到新值。大多数通过 HTTP 请求发送密钥的 CLI 都可以这样工作，包括 Browserbase、KERNEL、Notion、Ramp 和 Sentry 的 CLI。[Browserbase](https://docs.browserbase.com/integrations/anthropic/managed-agents/quickstart) 和 [KERNEL](https://www.kernel.sh/docs/integrations/claude-managed-agents) 首次为 Managed Agents 带来了浏览器能力，因此智能体可以一边使用其他工具，一边浏览并与 Web 交互。

![](https://assets.claude.com/e17afdf706d61056b4686ea4649ab1f0ee2e706e.png)

团队正在使用 Vault 中的环境变量，让智能体安全访问需要认证的工具：

* [Notion](https://claude.com/customers/notion-qa) 使用 Vault 中的环境变量，在推出 CLI 的同时配合 MCP 工具，为智能体增加了文件上传能力，而 API token 从未被交给模型。
* [Browserbase](https://www.browserbase.com/) 使用通过 Vault 完成认证的 [browse CLI](https://www.npmjs.com/package/browse) 构建了公开的浏览器技能目录。一个定时部署会定期校验该目录，以保持其准确。
* [KERNEL](https://www.kernel.sh/docs/integrations/claude-managed-agents) 使用 Vault 中的环境变量，将智能体安全地连接到记录用量和客户对话的数据库。智能体会在用量激增发生时将其标记出来，团队据此可以向客户确认该活动是否为有意为之。
* [Milana](https://getmilana.ai/) 使用 Vault 中的环境变量，将其 AI 产品工程师安全地连接到客户的代码库。智能体会自动发现并修复 bug，大规模数据分析也比以往更快。

![Milana](https://assets.claude.com/df4ef0d4ea1d8d538cba548c2987c958ae613b87.svg)

> “借助 Claude Managed Agents，我们让智能体建立在客户真实的代码库之上。我们发现它很容易上手，几乎立刻就能得到高质量的结果。关键的突破是 Vault 中的环境变量，它让我们的智能体可以通过 CLI 调用私有 API，而不暴露凭证。大规模数据分析现在快得多了，而且凭借这些产出，我们能够确保每一个输出的质量。”

Raghav Sethi，联合创始人兼 CTO

![BrowserBase](https://assets.claude.com/489e95f32195178dcffe6284f2d9135182747045.svg)

> “Vault 中的环境变量让我们的工程团队得以把两个主要的计算原语结合起来：智能体与浏览器。在 Browserbase，我们用 Claude Managed Agents 配合 browse CLI 生成了公开的浏览器技能目录，帮助智能体在 Web 上导航，并用定时部署对公开目录做定期校验。”

Ziray Hao，产品负责人

![KERNEL](https://assets.claude.com/3380cafbe5974d507544a64329ae6eba4c3d9794.svg)

> “Kernel 浏览器基础设施上的用量可能迅速激增，往往发生在客户刚完成部署之后。有了 Vault 中的环境变量，我们的智能体现在可以直接连接记录用量和客户对话的数据库。它能在几秒内拉取 30 天的每日用量，在激增发生时即时标记，并帮助我们的团队与客户确认该活动是否为有意为之。”

Catherine Jue，联合创始人兼 CEO

![Notion](https://assets.claude.com/19e0cdfaef9d2980bddd19cd993076d62b46c0c7.svg)

> “Vault 中的环境变量让我们能够安全地推出 Notion CLI，既满足了我们安全团队的严格规范，又确保敏感的 API token 永远不会被交给智能体。CLI 与 MCP 工具互补，在 Claude Managed Agents 中实现了文件上传能力。”

Quan Nguyen，公共 API 负责人

![Rakuten](https://assets.claude.com/5463fa5a44d12868ceec5ae30bfc8c412cafdeae.svg)

> “Rakuten 各团队使用定时部署，按每周或每月的计划分析电子表格中的数据并产出报告或演示文稿。我们的高级用户把它用在生产日志和指标上，这样产品经理无需创建分析仪表盘，就能看到自己应用的健康状况。”

Yusuke Kaji，AI for Business 总经理

![Ando](https://assets.claude.com/9d0ae4950cad063b171ca1e5a983f38f34493562.svg)

> “我们的大多数用户更喜欢与更少的智能体合作，而不是很多个。借助定时部署，他们可以把更多能力打包进一个自主智能体。例如，一个智能体可以同时盯住多条销售和招聘流程，向合适的人确认进展，并推动下一步动作。”

Sara Du，创始人

![Actively](https://assets.claude.com/af1bb9358ee0e5aac7291ad82c0287503c9b7b63.svg)

> “我们在 Claude Managed Agents 上构建了一套跨账户的智能体式搜索系统，让销售团队可以问出‘今天该联系哪些客户’这样的问题。由于客户希望这些答案定期刷新，我们用定时部署替换了自己搭建的调度基础设施，这大大简化了我们的技术栈，也改善了产品迭代周期。”

Mihir Garimella，联合创始人

## 开始使用

浏览我们的[文档](https://platform.claude.com/docs/en/managed-agents/overview)了解更多，或访问 [Claude Console](https://platform.claude.com/) 部署你的第一个智能体。
