# Claude Code 技术博客中文翻译（Anthropic Engineering Blog）

Anthropic 官方工程博客中 Claude Code 与智能体编码主题的 **29 篇技术文章**全文翻译。

- 英文存档：`../claudecode-articles/<slug>.md`（HTML→Markdown，含图片与链接）
- 中文译文：本目录 `<slug>.md`（与源文件同名镜像）
- 翻译规范：[../TRANSLATION_GUIDE_CLAUDECODE.md](../TRANSLATION_GUIDE_CLAUDECODE.md)（含全文统一术语表）
- 首批 25 篇完成于 2026-09-11；2026-09-14 增补 2 篇（Anthropic News 安全工程类），每日同步任务持续更新

## 目录（按发布时间排序）

| # | 日期 | 中文标题 | 英文标题 |
| --- | --- | --- | --- |
| 1 | 2024-09-19 | [上下文检索（Contextual Retrieval）介绍](contextual-retrieval.md) | Introducing Contextual Retrieval |
| 2 | 2024-12-19 | [构建高效智能体](building-effective-agents.md) | Building effective agents |
| 3 | 2025-01-06 | [用 Claude 3.5 Sonnet 刷新 SWE-bench Verified 纪录](swe-bench-sonnet.md) | Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet |
| 4 | 2025-03-20 | [「think」工具：让 Claude 在复杂工具使用场景中停下来思考](claude-think-tool.md) | The "think" tool: Enabling Claude to stop and think in complex tool use situations |
| 5 | 2025-04-18 | [Claude Code：智能体编码最佳实践](claude-code-best-practices.md) | Claude Code: Best practices for agentic coding |
| 6 | 2025-06-13 | [我们如何构建多智能体研究系统](multi-agent-research-system.md) | How we built our multi-agent research system |
| 7 | 2025-06-26 | [Desktop Extensions：为 Claude Desktop 带来一键安装 MCP 服务器](desktop-extensions.md) | Desktop Extensions: One-click MCP server installation for Claude Desktop |
| 8 | 2025-09-11 | [为智能体编写高效工具——用智能体来写](writing-tools-for-agents.md) | Writing effective tools for agents — with agents |
| 9 | 2025-09-17 | [三次近期事故的复盘](a-postmortem-of-three-recent-issues.md) | A postmortem of three recent issues |
| 10 | 2025-09-29 | [面向 AI 智能体的高效上下文工程](effective-context-engineering-for-ai-agents.md) | Effective context engineering for AI agents |
| 11 | 2025-10-16 | [用 Agent Skills 把智能体武装到现实世界](equipping-agents-for-the-real-world-with-agent-skills.md) | Equipping agents for the real world with Agent Skills |
| 12 | 2025-10-20 | [超越权限提示：让 Claude Code 更安全、更自主](claude-code-sandboxing.md) | Beyond permission prompts: making Claude Code more secure and autonomous |
| 13 | 2025-11-04 | [用 MCP 做代码执行：构建更高效的智能体](code-execution-with-mcp.md) | Code execution with MCP: Building more efficient agents |
| 14 | 2025-11-24 | [Claude 开发者平台高级工具使用功能发布](advanced-tool-use.md) | Introducing advanced tool use on the Claude Developer Platform |
| 15 | 2025-11-26 | [面向长时运行智能体的高效执行框架](effective-harnesses-for-long-running-agents.md) | Effective harnesses for long-running agents |
| 16 | 2026-01-09 | [解密 AI 智能体评估（evals）](demystifying-evals-for-ai-agents.md) | Demystifying evals for AI agents |
| 17 | 2026-01-21 | [设计抗 AI 的技术评估](AI-resistant-technical-evaluations.md) | Designing AI-resistant technical evaluations |
| 18 | 2026-02-05 | [用一支并行 Claude 团队构建 C 编译器](building-c-compiler.md) | Building a C compiler with a team of parallel Claudes |
| 19 | 2026-02-05 | [量化智能体编码评估中的基础设施噪声](infrastructure-noise.md) | Quantifying infrastructure noise in agentic coding evals |
| 20 | 2026-03-06 | [Claude Opus 4.6 在 BrowseComp 上的评估觉察现象](eval-awareness-browsecomp.md) | Eval awareness in Claude Opus 4.6's BrowseComp performance |
| 21 | 2026-03-24 | [面向长时运行应用开发的执行框架设计](harness-design-long-running-apps.md) | Harness design for long-running application development |
| 22 | 2026-03-25 | [我们如何构建 Claude Code 自动模式：一种更安全的免提示方式](claude-code-auto-mode.md) | How we built Claude Code auto mode: a safer way to skip permissions |
| 23 | 2026-04-08 | [Managed Agents 的规模化之道：把大脑与双手解耦](managed-agents.md) | Scaling Managed Agents: Decoupling the brain from the hands |
| 24 | 2026-04-23 | [关于近期 Claude Code 质量报告的更新](april-23-postmortem.md) | An update on recent Claude Code quality reports |
| 25 | 2026-05-25 | [我们如何在各产品中约束 Claude](how-we-contain-claude.md) | How we contain Claude across products |
| 26 | 2026-09-01 | [与我们的客户共同开发 Enterprise Frontier Safeguards](enterprise-frontier-safeguards.md) | Developing Enterprise Frontier Safeguards with our customers |
| 27 | 2026-09-10 | [改进我们的对齐与安全工作](improving-alignment-security-efforts.md) | Improving our alignment and security efforts |
| 28 | 2026-09-18 | [与 Accenture 合作开展嵌入式评估](accenture-embedded-evaluation.md) | Partnering with Accenture on embedded evaluation |
| 29 | 2026-09-23 | [Claude 发现具有类 CRISPR 重复序列的新型酶系统](claude-discovers-novel-enzyme-system.md) | Claude discovers a novel enzyme system with CRISPR-like repeats |

## 说明

- **范围**：Anthropic 工程博客自 2024-09 至 2026-05 的全部 25 篇文章（sitemap 全量），内容覆盖 Claude Code 最佳实践、沙箱与自动模式、权限体系、上下文工程、工具设计与 MCP、Agent Skills、长时运行智能体执行框架、多智能体系统、评估方法（evals）、事故复盘等。其中《上下文检索》《Desktop Extensions》等少数篇目并非 Claude Code 专属，为保持全量收录一并译出。2026-09-14 起，与安全工程同类的 Anthropic News 文章（对齐与安全实践、企业防护）也纳入收录。
- **claude-code-best-practices**：原博客 URL 现重定向至 code.claude.com/docs/en/best-practices（官方现行版本），本档按该页面存档；原 2025-04 博客版本因 Wayback Machine 在当前网络环境不可达而未采用，frontmatter 的 `note` 字段有记录。
- **翻译原则**：全文翻译不缩写；代码块、命令、图片 URL、链接 URL 原样保留；术语全文统一（见规范文件术语表）。
- **原文链接**：每篇译文开头的引用行均带原文 URL，可点击对照阅读。
