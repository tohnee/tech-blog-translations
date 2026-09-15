---
title: "Claude Developer Platform 上的结构化输出"
title_en: "Structured outputs on the Claude Developer Platform"
source: https://claude.com/blog/structured-outputs-on-the-claude-developer-platform/
crawled: 2026-09-14
translated: 2026-09-14
---

# Claude Developer Platform 上的结构化输出

> 原文：[Structured outputs on the Claude Developer Platform](https://claude.com/blog/structured-outputs-on-the-claude-developer-platform/) · Claude 博客

***更新：****现已面向 Claude Sonnet 4.5、Opus 4.5 与 Haiku 4.5，在 Claude Developer Platform 上原生正式发布（GA），并登陆 Amazon Bedrock。GA 版本新增了对更复杂 schema 的支持。（2026 年 2 月 4 日）*

***更新：****现已在 Claude Haiku 4.5 上可用——在 Claude Developer Platform 上原生支持，并登陆 Microsoft Foundry。（2025 年 12 月 4 日）*

Claude Developer Platform 现已为 Claude Sonnet 4.5 与 Opus 4.1 支持结构化输出（structured outputs）。该功能目前处于公测（public beta）阶段，可确保 API 响应始终符合你指定的 JSON schema 或工具定义。

借助结构化输出，开发者可以消除与 schema 相关的解析错误和失败的工具调用——通过确保 Claude 的响应遵循预定义的 schema，无论你是在从图像中提取数据、编排智能体，还是与外部 API 集成。

### 构建可靠的应用

对于在生产环境中构建应用与智能体的开发者来说，数据格式上的一个错误就可能引发连锁故障。结构化输出通过保证响应与你定义的结构完全一致来解决这一问题，且对模型性能没有任何影响。这让 Claude 成为那些对准确性要求严苛的应用与智能体的可靠之选，包括：

- **数据提取**：当下游系统依赖无错误、格式一致的数据时。
- **多智能体架构**：当智能体之间的一致通信对高性能、稳定的体验至关重要时。
- **复杂搜索工具**：当多个搜索字段必须准确填写并符合特定模式时。

结构化输出有两种使用方式：JSON 或工具（tools）。与 JSON 配合使用时，你在 API 请求中提供 schema 定义。对于工具，你定义工具规格（tool specifications），Claude 的输出会自动遵循这些工具定义。

最终效果是可靠的输出、更少的重试，以及一个不再需要故障转移逻辑或复杂错误处理的简化代码库。

### 客户聚焦：OpenRouter

OpenRouter 通过统一界面为 400 多万开发者提供对所有主流 AI 模型的访问。

"结构化输出已经成为智能体 AI 技术栈中非常有价值的一部分。智能体不断地摄取和产出结构化数据，因此 Anthropic 的结构化输出为开发者填补了一个真实的空白。智能体工作流每次都能可靠运行，团队可以专注于服务客户，而不是调试工具调用。"OpenRouter 首席运营官 Chris Clark 如是说。

### 开始使用

结构化输出现已在 Claude Developer Platform 上针对 Sonnet 4.5 与 Opus 4.1 开启公测，对 Haiku 4.5 的支持也即将推出。欢迎查阅我们的[文档](https://docs.claude.com/en/docs/build-with-claude/structured-outputs)，了解支持的 JSON schema 类型、实现示例与最佳实践。

FAQ（常见问题）
