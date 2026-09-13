# Claude Code 技术博客翻译进度

规范：TRANSLATION_GUIDE.md + TRANSLATION_GUIDE_CLAUDECODE.md
源：claudecode-articles/<slug>.md → 译文：claudecode-articles-zh/<slug>.md
frontmatter：title 换中文，新增 title_en + translated: 2026-09-11，其余照抄；正文 `# 中文标题` + `> 原文：[EN](url) · Anthropic Engineering Blog`。

子代理不可用（两种类型均 600s 无活动），由主会话直接翻译。

## 状态：✅ 全部完成（2026-09-11，25/25）

1. [x] contextual-retrieval (2024-09-19)
2. [x] building-effective-agents (2024-12-19)
3. [x] swe-bench-sonnet (2025-01-06)
4. [x] claude-think-tool (2025-03-20)
5. [x] claude-code-best-practices (2025-04, docs 版)
6. [x] multi-agent-research-system (2025-06-13)
7. [x] desktop-extensions (2025-06-26)
8. [x] writing-tools-for-agents (2025-09-11)
9. [x] a-postmortem-of-three-recent-issues (2025-09-17)
10. [x] effective-context-engineering-for-ai-agents (2025-09-29)
11. [x] equipping-agents-for-the-real-world-with-agent-skills (2025-10-16)
12. [x] claude-code-sandboxing (2025-10-20)
13. [x] code-execution-with-mcp (2025-11-04)
14. [x] advanced-tool-use (2025-11-24)
15. [x] effective-harnesses-for-long-running-agents (2025-11-26)
16. [x] demystifying-evals-for-ai-agents (2026-01-09)
17. [x] AI-resistant-technical-evaluations (2026-01-21)
18. [x] building-c-compiler (2026-02-05)
19. [x] infrastructure-noise (2026-02-05)
20. [x] eval-awareness-browsecomp (2026-03-06)
21. [x] harness-design-long-running-apps (2026-03-24)
22. [x] claude-code-auto-mode (2026-03-25)
23. [x] managed-agents (2026-04-08)
24. [x] april-23-postmortem (2026-04-23)
25. [x] how-we-contain-claude (2026-05-25)

质量核查（脚本验证）：25/25 通过——代码块围栏数与原文一致、frontmatter 字段齐全、图片/链接保留（4 篇重构了原文损坏的「Explore courses」怪链接，effective-harnesses 补齐了 claude.ai 链接）、术语一致（「代理」仅用于 proxy 语境）。
索引：claudecode-articles-zh/README.md（按时间排序，含中英文标题）。
