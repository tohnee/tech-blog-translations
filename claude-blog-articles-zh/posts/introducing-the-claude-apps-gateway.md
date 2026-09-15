---
title: "推出面向 Amazon Bedrock 和 Google Cloud 的 Claude 应用网关"
title_en: "Introducing the Claude apps gateway for Amazon Bedrock and Google Cloud"
source: https://claude.com/blog/introducing-the-claude-apps-gateway/
crawled: 2026-09-14
translated: 2026-09-14
---

# 推出面向 Amazon Bedrock 和 Google Cloud 的 Claude 应用网关

> 原文：[Introducing the Claude apps gateway for Amazon Bedrock and Google Cloud](https://claude.com/blog/introducing-the-claude-apps-gateway/) · Claude 博客

今天，我们推出面向 Amazon Bedrock 和 Google Cloud 的 Claude 应用网关（apps gateway）。此前，在这些平台上运行 Claude Code 意味着要为每位开发者配置一个云凭证、手动把设置推送到每一台笔记本，还要另起一套工具才能看到每位开发者的花费。这个网关是一个自托管（self-hosted）控制平面，为 Claude Code 提供企业 SSO 登录、集中执行的策略、基于角色的访问控制，以及按用户归集的成本核算。

## **部署网关**

网关以单个无状态容器的形式运行，部署在 Linux 上，由一个 PostgreSQL 数据库支撑。它保存你的上游凭证、向你的身份提供方验证开发者身份、分发并执行托管设置（managed settings），并把按用户统计的用量上报给你运维的采集器。让一位开发者接入，只需把他加入你的身份提供方（Identity Provider，IdP）；让他离开，就是把他移除。

网关由 Anthropic 构建并随开发者早已安装的同一个 `claude` 二进制一起分发，因此你可以在自己的基础设施上以单个无状态容器运行它。由于网关与客户端是一体构建的，`/login` 流程天然感知网关，客户端会在登录时自动应用托管设置，策略也会在每一次请求上一致地执行。

## **网关的工作方式**

网关负责处理：

- **身份。**它作为 OpenID Connect（OIDC）依赖方（relying party）对接 Google Workspace、Microsoft Entra ID、Okta 或任何符合标准的 OIDC 提供方，并签发短时会话。开发者的机器上不会存放长期有效的密钥。
- **策略。**你只需在服务器上定义一次托管设置，客户端在登录时接收策略，网关则在每一次请求上执行它。你可以集中调整允许使用的模型和默认设置。
- **遥测。**客户端为每个请求打上用量指标，网关通过 OTLP 把它转发到你配置的采集器——数据留在你的网络里，按你的保留周期管理。
- **路由。**网关保存你的上游凭证，把推理请求路由到 Claude API、Amazon Bedrock 或 Google Cloud，并可在不同提供方之间选择性地故障转移。
- **花费上限。**网关允许你设置每日、每周和每月的花费限额。限额可以按组织、组或用户分别应用。

除非你把网关配置为使用 Claude API，否则它不会向 Anthropic 发送推理流量或用量数据。我们还会公开发布网关所使用的协议，让其他网关开发者也能实现同样的功能。

## **开始使用**

网关现已可用。要开始上手：

- **部署网关**：下载 Claude Code CLI 二进制，把 `gateway.yaml` 指向你的 OIDC 签发方和上游凭证，并在你的 IdP 中注册一个 OIDC 应用。
- **推广上线**：在客户端机器的 `managed-settings.json` 中配置 `forceLoginMethod` 和 `forceLoginGatewayUrl` 参数。客户端在首次启动时即会连接到你的网关。

[参阅文档](https://code.claude.com/docs/en/claude-apps-gateway)了解更多。

FAQ（常见问题）
