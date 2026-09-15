---
title: "用 Claude Code 自动化安全审查"
title_en: "Automate security reviews with Claude Code"
source: https://claude.com/blog/automate-security-reviews-with-claude-code/
crawled: 2026-09-14
translated: 2026-09-14
---

# 用 Claude Code 自动化安全审查

> 原文：[Automate security reviews with Claude Code](https://claude.com/blog/automate-security-reviews-with-claude-code/) · Claude 博客

今天，我们在 Claude Code 中推出自动化安全审查（automated security reviews）功能。借助我们的 GitHub Actions 集成和全新的 /security-review 命令，开发者可以轻松让 Claude 识别安全问题——然后让它把它们修好。

随着开发者越来越多地依靠 AI 来更快交付、构建更复杂的系统，确保代码安全变得愈发关键。这些新功能让你可以把安全审查集成到现有的工作流中，帮助你在漏洞进入生产环境之前就将其捕获。

### 在终端中审查代码中的漏洞

全新的 /security-review 命令让你可以在提交代码之前，直接从终端运行临时的（ad-hoc）安全分析。在 Claude Code 中运行该命令，Claude 会在你的代码库中搜索潜在漏洞，并对发现的任何问题提供详细说明。

该命令使用一个专注于安全的专用提示（prompt），检查常见漏洞模式，包括：

- SQL 注入风险
- 跨站脚本（XSS）漏洞
- 身份验证与授权缺陷
- 不安全的数据处理
- 依赖项漏洞

你还可以在问题被识别之后，让 Claude Code 针对每个问题实施修复。这让安全审查留在你的内部开发循环中，趁问题最容易修的时候尽早捕获它们。

### 为新的 pull request 自动化安全审查

全新的 Claude Code GitHub action 把安全审查向前推进了一步：在 pull request 被打开时自动对其进行分析。配置好之后，该 action 会：

- 在新的 pull request 出现时自动触发
- 审查代码变更中是否存在安全漏洞
- 应用可自定义的规则，过滤误报（false-positive）和已知问题
- 将发现的隐患以内联评论的形式发布在 PR 上，包括修复建议

这为你的整个团队建立了一致的安全审查流程，确保任何代码在通过基线安全审查之前都不会进入生产环境。该 action 可与你现有的 CI/CD 流水线集成，并且可以自定义以符合你团队的安全策略。

### 在 Anthropic 改进产品安全

我们自己也在使用这些功能，帮助保障团队交付到生产环境的代码的安全，Claude Code 本身也不例外。自配置该 GitHub action 以来，它已经在我们自己的代码中捕获了安全漏洞，并阻止它们被交付出去。

举个例子，上周我们的团队为某个内部工具构建了一个新功能，它依赖于启动一个用于接受本地连接的本地 HTTP 服务器。GitHub action 识别出一个可通过 DNS 重绑定（DNS rebinding）利用的远程代码执行漏洞，并在该 PR 被合并之前就修复了它。

在另一个案例中，一位工程师构建了一个代理系统，用于安全地管理内部凭据。GitHub action 自动标记出这个代理容易受到 SSRF（服务器端请求伪造）攻击，我们随即修复了该问题。

### 开始使用

这两项功能现已面向所有 Claude Code 用户开放。要开始使用自动化安全审查：

- **关于 /security-review 命令**：只需将 Claude Code 更新到最新版本，然后在你的项目目录中运行 /security-review。如需定制你自己的命令版本，请参阅[文档](https://github.com/anthropics/claude-code-security-review/tree/main?tab=readme-ov-file#security-review-slash-command)
- **关于 GitHub action**：分步安装与配置说明请参阅[文档](https://github.com/anthropics/claude-code-security-review)

FAQ（常见问题）
