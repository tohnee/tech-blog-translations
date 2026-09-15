---
title: "连接器可观测性与应用内目录提交"
title_en: "Connector Observability and In-App Directory Submission"
source: https://claude.com/blog/observability-for-developers-building-connectors/
crawled: 2026-09-14
translated: 2026-09-14
---

# 连接器可观测性与应用内目录提交

> 原文：[Connector Observability and In-App Directory Submission](https://claude.com/blog/observability-for-developers-building-connectors/) · Claude 博客

## 监控、调试并改进连接器

已发布到[目录](https://claude.ai/directory/connectors)中的连接器现在有了一个仪表盘，展示它们在 Claude 各产品界面上的表现。连接器所有者可以用它来：

- **追踪采用情况。** 随时间监控活跃用户数、工具调用总量和目录排名。
- **诊断错误与延迟。** 一目了然地查看健康分、错误率和延迟，并借助按工具拆分的错误明细定位问题出在哪里。
- **按产品拆分使用情况。** 对比 Claude、Claude Code、Cowork 等产品上的工具调用，了解用户在哪些场景下活跃使用。

*连接器可观测性示意视图。数据仅为示例。*

该功能即日起以公开测试版（public beta）提供。在 Claude 中依次进入[组织设置](https://claude.ai/admin-settings/organization)下的[目录](https://claude.ai/admin-settings/directory/submissions)即可找到。需要 Team 或 Enterprise 套餐的管理员（Admin）或所有者（Owner）权限。在 Enterprise 套餐中，所有者还可以通过带有「目录管理」（Directory management）或「资源库」（Libraries）权限的[自定义角色](https://support.claude.com/en/articles/13930452-manage-custom-roles-on-enterprise-plans)来委派访问权限。

## 加入目录

连接器构建于 [Model Context Protocol（MCP）](https://modelcontextprotocol.io/docs/getting-started/intro)之上。[目录](https://claude.ai/directory/connectors)中已有 300 多个第三方连接器，每天有数百万人使用。如果你想把自己的 MCP 服务器提交到目录，现在可以直接在 Claude 中完成。[了解更多](https://claude.com/docs/connectors/building/submission)。

FAQ（常见问题）
