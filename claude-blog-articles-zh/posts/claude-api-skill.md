---
title: "Claude API 技能现已登陆 CodeRabbit、JetBrains、Resolve AI 和 Warp"
title_en: "Claude API skill now in CodeRabbit, JetBrains, Resolve AI, and Warp"
source: https://claude.com/blog/claude-api-skill/
crawled: 2026-09-14
translated: 2026-09-14
---

# Claude API 技能现已登陆 CodeRabbit、JetBrains、Resolve AI 和 Warp

> 原文：[Claude API skill now in CodeRabbit, JetBrains, Resolve AI, and Warp](https://claude.com/blog/claude-api-skill/) · Claude 博客

今天，CodeRabbit、JetBrains、Resolve AI 和 Warp 正在打包集成 [claude-api 技能](https://github.com/anthropics/skills/tree/main/skills/claude-api)，让开发者无论在哪里构建，都能得到可用于生产环境的 Claude API 代码。该技能于 3 月首次随 Claude Code 推出，如今已进入更多开发者日常使用的工具之中。

## 使用 Claude API 技能进行构建

`claude-api` 技能收录了让 Claude API 代码良好运作的种种细节：哪种智能体模式适合特定任务、哪些参数在模型各代之间发生了变化、何时应用提示缓存（prompt caching）。其结果是更少的错误、更好的缓存、更整洁的智能体模式，以及更顺畅的模型迁移。

它会随我们的 SDK 变化而保持最新。当新模型发布或 API 新增功能时，Claude 早已知晓。

在任何提供该技能的地方，都可以让 Claude：

- **「提高我的缓存命中率。」** 该技能会应用许多开发者容易忽略的提示缓存规则。
- **「为我的智能体添加上下文压缩（compaction）。」** 它会带你了解我们文档中的压缩原语和智能体模式。
- **「把我升级到最新的 Claude 模型。」** Claude 会审查你的代码，并带你逐步更新模型名称、提示和努力等级（effort level）设置，以适配 [Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7) 这样的新模型。在 Claude Code 中，你也可以直接运行 `/claude-api migrate`。
- **「为我的行业构建一个深度研究智能体。」** Claude 会带你完成 [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) 的配置，让长时间运行的研究只需几条提示，而不必做成定制项目。在 Claude Code 中，你也可以直接运行 `/claude-api managed-agents-onboard`。

「在 CodeRabbit，我们每周评审数百万个 PR，深知过时的 API 知识多么频繁地引发生产问题。Claude API 技能让 Claude 随我们的 SDK 变化保持最新，构建智能体的开发者在评审时遇到的意外会少得多。」

「借助 Claude API 技能，JetBrains IDE 和 Junie 上的开发者可以把 Claude API 升级变成一条有引导的 IDE 工作流。一个典型例子是迁移到 Claude Opus 4.7：技能可以更新模型引用，把手动的思考设置改为自适应思考（adaptive thinking），清理过时的参数和 beta 请求头，并内联建议合适的努力等级。这让团队的首次产出更扎实，也有助于避免那些通常在清理轮次中才会暴露的版本特定错误。」

「Claude API 技能帮助 Resolve AI 的工程师更快采用新模型能力。我们的团队无需手动翻阅迁移指南、追逐每一个细小的 API 变更，就能在一次有引导的过程中从模型发布走到落地实现。」

「开发者不应该为了查 Claude API 参数或缓存规则而离开 Warp。内置 Claude API 技能之后，这些知识触手可及，工程师得以保持心流、更快交付。」

## 面向由 Claude 驱动的编程智能体

任何编程智能体都可以打包集成 `claude-api` 技能，为其用户提供围绕 Claude API 的专业知识。如果你正在构建一个开发者会在其中编写 Claude API 代码的工具，该技能已在 [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/claude-api) 开源。我们的集成指南会带你用大约 20 行 CI 完成配置，且技能会自动保持最新。

## 开始使用

该技能现已登陆 [Claude Code](https://claude.com/product/claude-code)、[CodeRabbit](https://www.coderabbit.ai/)、[JetBrains](https://www.jetbrains.com/)、[Junie](https://www.jetbrains.com/junie/)、[Resolve AI](https://resolve.ai/) 和 [Warp](https://www.warp.dev/)。了解更多，请参阅 [claude-api 技能文档](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/claude-api-skill)。

FAQ（常见问题）
