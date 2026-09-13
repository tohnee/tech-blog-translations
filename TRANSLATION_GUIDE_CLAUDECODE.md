# 翻译规范（Anthropic Engineering Blog / Claude Code 技术博客中文化）

本文件是 Claude Code 技术博客翻译项目的统一规范，所有翻译批次开始前先读完。通用原则与 [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md)（Raschka 项目）一致，本文件补充本项目特有的约定与术语表。

## 项目信息

- 英文存档：`claudecode-articles/<slug>.md`（25 篇）
- 输出目录：`claudecode-articles-zh/<slug>.md`（与源文件同名镜像）
- 进度索引：`claudecode-articles-zh/README.md`（每完成一篇更新）

## 输出文件头格式

```markdown
---
title: "中文标题"
title_en: "Original English Title"
source: <原文件 source URL，保持不变>
published: <原文件 published 日期，保持不变>
crawled: <原文件 crawled 日期，保持不变>
translated: <完成日期 YYYY-MM-DD>
---

# 中文标题

> 原文：[Original English Title](source URL) · Anthropic Engineering Blog

（正文译文……）
```

- 除新增 `translated` 字段外，frontmatter 其他字段原样保留。`claude-code-best-practices.md` 的 `note` 字段也原样保留并在需要时附中文说明。

## 翻译原则（在通用规范基础上补充）

1. **全文翻译，不得缩写或跳过**：包括开头的摘要/编者按（`*Note: ...*` 译为「注：……」）、各章节、结尾的致谢与延伸阅读。
2. **代码块原样保留**：fenced code block 内的代码、命令、JSON/YAML 配置、终端输出一律不翻译；代码内的英文注释保留原文（可译，但以不引入错误为前提，默认保留）。行内代码保留。
3. **图片链接 URL 原样保留**：`![](url)` 的 URL 不动；图片下方 `**Figure N. ...**` 图注翻译（粗体格式保留）。
4. **Markdown 结构保持**：标题层级、列表、表格、引用块、粗斜体、分隔线与原文一一对应。表格表头与单元格翻译。
5. **链接文本翻译，URL 不动**。指向 Anthropic/claude.com/code.claude.com 的链接 URL 原样保留。
6. **人名**：正文首次出现用「外文姓名」，不必加中文译名（如 Boris Cherny、Jeremy Howard、Erik Schluntz 等保留原文）。
7. **产品/模型/系统名不翻译**：Claude、Claude Code、Claude Desktop、Cowork、MCP（Model Context Protocol）、Claude Agent SDK、GitHub Actions、DevContainer、SWE-bench Verified、Terminal-Bench、Claude 3.5 Sonnet/Haiku/Opus、Claude Opus 4.6 等。
8. **文件名与路径不翻译**：CLAUDE.md、.claude/、settings.json、CLAUDE.local.md、Makefile、README.md 等。
9. **命令行选项**：如 `--dangerously-skip-permissions`、`--print`、`claude -p "..."` 一律保留原文，行内代码格式不动。
10. 语气：工程博客风格，面向中文开发者/工程师，流畅自然；避免翻译腔。语气词与幽默感可以适度传达，但不要过度意译。

## 术语表（全文统一）

### Claude Code 产品与运行模式

| English | 中文 |
|---|---|
| Claude Code | Claude Code（不译） |
| agentic coding | 智能体编码 |
| coding agent / agent | 编程智能体 / 智能体 |
| agentic loop / agent loop | 智能体循环 |
| agentic system / workflow | 智能体系统 / 工作流 |
| harness | 执行框架（harness，首次出现标注英文） |
| scaffold | 脚手架 |
| auto mode | 自动模式（auto mode） |
| plan mode | 计划模式（plan mode） |
| headless mode | 无头模式（headless mode） |
| permission prompt / approval prompt | 权限提示 / 批准提示 |
| approval fatigue | 批准疲劳 |
| `--dangerously-skip-permissions` | `--dangerously-skip-permissions`（不译） |
| sandboxing / sandbox | 沙箱机制 / 沙箱 |
| filesystem isolation / network isolation | 文件系统隔离 / 网络隔离 |
| allowlist / denylist | 允许列表 / 拒绝列表 |
| proxy / firewall | 代理 / 防火墙 |
| classifier | 分类器 |
| guardrail | 防护栏 |
| CLAUDE.md / memory file | CLAUDE.md / 记忆文件 |
| slash command | 斜杠命令（slash command） |
| hook (PreToolUse/PostToolUse 等) | 钩子（hook），具体钩子名不译 |
| subagent | 子智能体（subagent） |
| skill / Agent Skills | 技能 / Agent Skills（首次标注） |
| MCP (Model Context Protocol) | MCP（Model Context Protocol，不译） |
| MCP server | MCP 服务器 |
| tool / tool use / tool calling | 工具 / 工具使用 / 工具调用 |
| tool definition / tool schema | 工具定义 / 工具 schema |
| computer use | 计算机使用（computer use） |
| bash tool | bash 工具 |
| text editor tool | 文本编辑器工具 |
| token-efficient tool use | 省 token 工具使用（token-efficient tool use） |
| fine-grained tool streaming | 细粒度工具流式输出 |
| context editing | 上下文编辑 |
| memory tool | 记忆工具 |
| programmatic tool calling | 程序化工具调用 |
| Tool Search Tool | Tool Search Tool（不译） |
| Managed Agents | Managed Agents（不译） |
| Desktop Extensions | Desktop Extensions（不译） |
| Cowork | Cowork（不译） |
| claude.ai | claude.ai（不译） |

### 上下文与提示工程

| English | 中文 |
|---|---|
| context engineering | 上下文工程 |
| context window / context rot | 上下文窗口 / 上下文腐化（context rot） |
| system prompt | 系统提示 |
| prompt / prompt engineering | 提示 / 提示工程 |
| prompt injection | 提示注入 |
| needle-in-a-haystack | 大海捞针（needle-in-a-haystack） |
| compaction / compact | 压缩（compaction）/ compact（命令名不译） |
| just-in-time context | 按需加载的上下文（just-in-time context） |
| long-horizon task | 长周期任务 |
| scratchpad | 草稿区（scratchpad） |
| note-taking / memory | 记笔记 / 记忆 |
| sub-agent communication | 子智能体间通信 |
| few-shot example | 少样本示例 |
| chain-of-thought / extended thinking | 思维链 / 扩展思考（extended thinking） |

### 评测与基础设施

| English | 中文 |
|---|---|
| evaluation / eval | 评估 / eval（评估场景通译「评估」） |
| benchmark | 基准测试 |
| SWE-bench Verified / Terminal-Bench / BrowseComp / OSWorld | 不译 |
| pass@k | pass@k（不译） |
| eval awareness | 评估觉察（eval awareness） |
| infrastructure noise | 基础设施噪声 |
| flaky / nondeterminism | 不稳定 / 非确定性 |
| sampling temperature | 采样温度 |
| postmortem | 事故复盘 |
| incident | 事故 |
| root cause | 根本原因 |
| race condition | 竞态条件 |
| token bucket / rate limit | 令牌桶 / 速率限制 |
| overflow / throttling | 溢出 / 限流 |
| rollout / canary | 灰度发布 / 金丝雀发布 |
| shadow mode | 影子模式（shadow mode） |
| false positive / false negative | 误报 / 漏报 |
| precision / recall | 精确率 / 召回率 |

### 通用工程

| English | 中文 |
|---|---|
| LLM (large language model) | 大语言模型（LLM） |
| retrieval-augmented generation (RAG) | 检索增强生成（RAG） |
| embedding / chunk | 嵌入 / 分块 |
| contextual retrieval | 上下文检索（contextual retrieval） |
| contextual embeddings / contextual BM25 | 上下文化嵌入 / 上下文化 BM25 |
| rank / rerank | 排序 / 重排序 |
| orchestrator / orchestrator-worker | 编排器 / 编排者-执行者（orchestrator-worker） |
| chain / routing / parallelization | 链式 / 路由 / 并行化 |
| evaluator-optimizer | 评估者-优化者（evaluator-optimizer） |
| container / VM / devcontainer | 容器 / 虚拟机 / devcontainer（不译） |
| snapshot / rollback | 快照 / 回滚 |
| checkpoint | 检查点 |
| git worktree | git worktree（不译） |
| monorepo / codebase | 单体仓库 / 代码库 |
| lint / static analysis | lint（不译）/ 静态分析 |
| screenshot / accessibility tree | 截图 / 可访问性树 |
| RL (reinforcement learning) | 强化学习（RL） |
| distilled / distillation | 蒸馏 |

其余术语以 [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md) 总表为准；两表冲突时以本文件为准。首次出现的重要术语采用「中文（English）」标注。
