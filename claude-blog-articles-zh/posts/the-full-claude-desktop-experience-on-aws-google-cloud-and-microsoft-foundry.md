---
title: "在 AWS、Google Cloud 和 Microsoft Foundry 上获得完整的 Claude Desktop 体验"
title_en: "The full Claude Desktop experience on AWS, Google Cloud, and Microsoft Foundry"
date: 2026-06-22
source: https://claude.com/resources/articles/the-full-claude-desktop-experience-on-aws-google-cloud-and-microsoft-foundry
crawled: 2026-11-17
translated: 2026-11-17
---

# 在 AWS、Google Cloud 和 Microsoft Foundry 上获得完整的 Claude Desktop 体验

> 原文：[The full Claude Desktop experience on AWS, Google Cloud, and Microsoft Foundry](https://claude.com/resources/articles/the-full-claude-desktop-experience-on-aws-google-cloud-and-microsoft-foundry) · Claude 博客

通过 AWS、Google Cloud 和 Microsoft Foundry 使用 Claude Desktop 的组织，现在可以获得完整的 Desktop 体验——Chat、Claude Cowork 和 Claude Code，全部集成在一个应用中。

现在，IT 团队可以让推理在所有产品中都保留在自己的环境内，并借助按用户的 SSO、MDM 策略模板、离线安装程序选项，以及可完全在设备上运行的 M365 连接器，在整个组织范围内部署 Claude Desktop。

推理在你配置的区域、在你自己的云上运行，对话历史存储在本地。数据连接器可以访问哪些端点、Anthropic 能收到哪些聚合遥测数据，都由你掌控。

### 一个覆盖整个组织的界面

在此之前，通过 AWS、Google Cloud 和 Microsoft Foundry 使用 Claude Desktop 的客户只能使用 Claude Cowork 和 Claude Code。现在，一次部署即可覆盖所有角色，且每个界面都有自己的策略键，由你决定谁能使用什么、以及何时可用。

Chat 用于快速获取答案、梳理问题。Claude Cowork 用于人们更愿意交出去的工作：Claude 在已批准的来源中调研，处理设备上已有的文件并产出交付物，完成后呈现结果。Claude Code 则面向希望进行智能体式编程、又不想整天泡在终端里的工程师。

### 部署控制

在整个组织内部署 Claude Desktop，意味着要在你已有的系统之内完成工作。

**像任何办公应用一样登录。** 员工使用他们登录其他一切应用时所用的同一个工作账号：IAM Identity Center、Workforce Identity Federation、Microsoft Entra ID，或 Okta 等任何 OIDC 提供方。没有需要轮换的共享密钥，终端用户机器上也没有云凭据。

**像任何已有应用一样部署。** 从设置界面导出策略模板，然后通过 Intune、GPO 或 Jamf 推送。离线安装程序可覆盖隔离网络（air-gapped）环境。

**在任何人看到之前就确认它可用。** 在上线前测试每一个连接器、确认你的提供商提供哪些 Claude 模型，并验证连接。模型守卫会让路由始终停留在 Claude 上，包括在 GovCloud 中，即使某个设置配置错误也是如此。

**小规模起步，随采用扩大。** Chat、Claude Cowork 和 Claude Code 各有一个策略键，因此你可以先给非技术团队开放 Chat 和 Claude Cowork、给工程团队开放 Claude Code，再随着团队对各个界面的采用逐步扩大访问范围。你的硬性拒绝规则适用于所有标签页。

**把 Claude 带到工作所在之处。** Microsoft 365 连接器通过你自己的 Entra 应用让 Claude 访问邮件和文档，支持租户白名单，并 beta 支持 GCC High/DoD 端点。对于最严格的数据驻留要求，可使用我们的本地连接器，连接只保留在设备与 Microsoft 之间。

> “我们通过现有的云环境快速完成了 Claude Desktop 的推广——无需单独的供应商合同。我们自有的 LLM Gateway 让一个团队就能把它部署给全球数百名用户，而无需进行繁重的基础设施建设。”——Sarang Oh，韩华解决方案（Hanwha Solutions）分析/AI 团队负责人

### 开始使用

管理员可参阅[部署指南](http://claude.com/docs/third-party/claude-desktop/installation)，其中逐步介绍了 SSO、策略模板和上线前验证。你也可以联系客户团队，我们会协助你规划推广。
