---
title: "第 3 讲：从用户视角看智能体 II——多智能体与最佳实践"
title_en: "Agent From a User's Perspective II: Multi-agent and Best Practice"
source: https://cs2680.seas.harvard.edu/slides/3_agent_use_2.pdf
pages: 72
crawled: 2026-11-16
translated: 2026-11-16
---

# 第 3 讲：从用户视角看智能体 II——多智能体与最佳实践

> PDF 讲义文本抽取：[3_agent_use_2.pdf](https://cs2680.seas.harvard.edu/slides/3_agent_use_2.pdf) · Harvard CS2680

## 第 1 页

**现代 AI 系统：智能体与系统优化**

Juncheng Yang

从用户视角看智能体 II：多智能体与最佳实践

## 第 2 页

**更新与提醒**

- 作业 1 截止
- 作业 1 分享报名
- 把我和助教加入你的 repo

新助教：Charles Wang

## 第 3 页

**回顾**

- 智能体循环
- 状态管理
  - 上下文作为工作记忆：每条用户 prompt、LLM 响应、工具调用结果都会被追加
  - 智能体记忆：跨会话持久化
    - CLAUDE.md（AGENTS.md）
    - 自动记忆
- 工具
  - 内置工具
  - 扩展 Claude Code 能力：skill、MCP、hook、plugin

## 第 4 页

**今日安排**

- 案例研究：Superpowers 与 Caveman
- 借助多个智能体成为 100 倍研究员和工程师
- 编程 / Software 3.0：编程如何演进
- 人们如何使用 OpenAI Codex
- 2026 年 6 月和 2026 年 9 月的两份报告

## 第 5 页

**案例研究：Superpowers**

一个软件开发 plugin

https://github.com/obra/superpowers

```
/plugin install superpowers@claude-plugins-official
```

## 第 6 页

**同一个模型，不同的工作流**

1. 澄清问题
2. 批准设计
3. 编写详细计划
4. 测试驱动构建
5. 审查与验证
6. 完成或合入分支

PLAN　BUILD　SHIP

HUMAN 0——人类输入 prompt

DEFAULT：功能请求 → 直接开始写代码 → 靠迭代修复

两个智能体共享同一个模型和同一套工具——只有指令不同。

## 第 7 页

**Superpowers 的九个 skill**

| Skill | 职责 |
| --- | --- |
| using-superpowers | 发现与调用 skill 的规则 |
| brainstorming | 把请求变成获批的设计 |
| writing-plans | 把设计分解为具体任务 |
| using-git-worktrees | 创建隔离工作区 |
| test-driven-development | 强制执行红、绿、重构 |
| systematic-debugging | 在提出修复前找到根因 |
| requesting-code-review | 对照计划审查实现 |
| verification-before-completion | 报告成功前要求证据 |
| finishing-a-development-branch | 合并、pull request、保留或清理 |

OPTIONAL——额外阅读，非必需

## 第 8 页

**Superpowers 架构**

仓库布局 / 组件图

```
superpowers/
├── .claude-plugin/   plugin.json
├── hooks/            hooks.json
│                     session-start
├── skills/
│     using-superpowers/
│     brainstorming/
│     writing-plans/
│     test-driven-development/
└── tests/
```

Superpowers plugin → Plugin 元数据 / Session hook / Skill 库 → 智能体行为

Plugin 是分发容器——skills 与 hooks 提供行为。

## 第 9 页

**Skill 剖析**

目录：

```
skills/
└── brainstorming/
      SKILL.md
      visual-companion.md
      scripts
```

SKILL.md（简化）：

```
---
name: brainstorming
description: Use before creative work.
---
## Workflow
1. Inspect the project
2. Classify the scope
3. Clarify requirements
4. Compare approaches
5. Present a design
6. Wait for user approval
7. Invoke writing-plans
```

Front matter 是元数据。正文是智能体遵循的流程。

## 第 10 页

**SKILL.md 包含什么**

| 组件 | 功能 |
| --- | --- |
| name | 稳定标识符 |
| description | skill 何时适用 |
| Instructions | 要遵循的流程 |
| Checkpoints | 继续前需要批准 |
| References | 仅在需要时提供细节 |
| Scripts | 确定性操作 |

一个流程型 skill 可以定义：

- 进入条件
- 必需动作
- 禁止动作
- 人工批准关卡
- 验证要求
- 下一个适用的 skill

每个 skill 引导智能体行为，并可选地指定其后继者。

## 第 11 页

**为什么仅有 Skills 不够**

安装 skill 只是让它们可用——可用本身并不保证智能体会去检查它们。

`hooks/hooks.json`

```json
{
 "hooks": {
  "SessionStart": [{
   "matcher": "startup|clear|compact",
   "hooks": [{ "type": "command",
    "command": "run-hook.cmd",
    "async": false }]
  }] } }
```

**hook 保证什么**

- 每个会话中确定性的时机
- 在智能体行动之前运行
- 在 clear 和 compaction 之后重新运行

## 第 12 页

**会话启动脚本**

`hooks/session-start`（简化）

```bash
#!/usr/bin/env bash
set -euo pipefail
ROOT="$(plugin_root)"
skill="$ROOT/skills/using-
       superpowers/SKILL.md"
content="$(cat "$skill")"
printf '{"hookSpecificOutput": {
 "hookEventName": "SessionStart",
 "additionalContext": "%s" }}' \
 "$(escape_json "$content")"
```

执行步骤：

1. 定位已安装的 plugin
2. 读取 bootstrap SKILL.md
3. 为 JSON 转义 Markdown
4. 作为 `additionalContext` 返回
5. Claude Code 将其加入上下文

OPTIONAL——额外阅读，非必需

## 第 13 页

**端到端演示**

运行时序列：“添加认证”

- Claude Code → 启动会话
- Hook → 读取 bootstrap skill
- Agent → 接收选择策略
- User → “添加认证”
- Agent → 加载 brainstorming，澄清需求
- User → 批准设计
- Agent → 加载 writing-plans

后续阶段：

- 实现计划
- 隔离 worktree
- 测试驱动构建
- 代码审查
- 验证
- 分支集成

## 第 14 页

**Superpowers 的设计经验**

| 设计问题 | Superpowers 的答案 |
| --- | --- |
| 复杂行为应如何表示？ | 小而可组合的 skills |
| 智能体如何记得使用它们？ | 通过 session hook 注入 bootstrap skill |
| 如何保持上下文可控？ | 只在相关时加载任务 skill |
| 各阶段如何协调？ | 每个 skill 指定自己的关卡和后继者 |
| 用户如何安装系统？ | 把所有内容打包为 plugin |
| 每个 plugin 都需要 commands 或 MCP 吗？ | 不——只在需要时添加 |

OPTIONAL——额外阅读，非必需

## 第 15 页

**Caveman 案例研究**

五种扩展机制——外加一个本地代理

```
claude plugin marketplace add JuliusBrussee/caveman
claude plugin install caveman@caveman
```

## 第 16 页

**为什么要压缩智能体的 token？**

- 上下文会填满
  - 日志、diff 和工具输出挤占工作内容。
- 每一轮都有成本
  - token 双向付费，双向等待。
- Compaction 丢失细节
  - 太晚裁剪上下文会丢掉重要的东西。

BEFORE——786 行测试输出

```
$ npm test
FAIL  src/api/client.test.ts
  ● client › retries on 5xx
    connect ETIMEDOUT 10.0.3.8:443
      at client.ts:88
… 776 more lines …  3 failed, 214 passed
```

AFTER——模型读到的内容

```
3 tests fail: ETIMEDOUT at client.ts:88
```

双向压缩——并保留原始内容以供检索。

## 第 17 页

**Caveman 从两个方向压缩 token**

Model：

- AGENT INPUT（日志 · 工具结果 · diff · 文件）← Local proxy + engine
- AGENT OUTPUT（Response skill，较早注入上下文）→ What you read

skill 改变模型的写法。代理改变模型读到的内容。

报告：输出 token 减少 65%

skill 本身会增加输入 token，因此整个会话的节省会更低。

`/caveman ultra`，然后：“Run the tests and explain the failure.”

## 第 18 页

**走一遍示例**

`/caveman ultra`，然后：“Run the tests and explain the failure.”

按顺序发生：

1. Hook 存储 ultra 模式
2. Hook 注入简洁响应提醒
3. 智能体执行命令（来自 LLM）
4. Caveman（代理）压缩嘈杂的测试输出
5. 模型收到缩减后的上下文
6. 模型返回简洁诊断
7. MCP 按需检索原始内容

OPTIONAL——额外阅读，非必需

## 第 19 页

**Plugin 打包**

REPOSITORY STRUCTURE

```
caveman/
├─ .claude-plugin/plugin.json
├─ skills/
│   caveman, -commit, -review,
│   -compress, -stats
├─ commands/
├─ src/hooks/
├─ mcp/
├─ proxy/
├─ engine/
└── agents/
```

PLUGIN MANIFEST

```json
{
  "name": "caveman",
  "hooks": {
    "SessionStart":
      ["caveman-activate.js"],
    "UserPromptSubmit":
      ["caveman-mode-tracker.js"]
  }
}
```

## 第 20 页

**response skill 让输出更简洁**

`SKILLS/CAVEMAN/SKILL.md`

```
---
name: caveman
description: Compressed mode
---
# Caveman response mode
Preserve: technical terms, commands, paths, code, errors, 
numbers, units, negation
Remove: filler, repetition, pleasantries, hedging
Short sentences. Active voice.
```

它改变智能体的沟通方式。

## 第 21 页

**Commands 提供显式的用户控制**

COMMANDS

- `/caveman`：激活默认完整模式
- `/caveman ultra`：最大压缩
- `/caveman off`：停用该风格
- `/caveman-commit`：简洁提交信息
- `/caveman-review`：简洁审查发现
- `/caveman-compress`：压缩记忆文件
- `/caveman-stats`：会话 token 统计
- `/caveman-help`：可用操作

`COMMANDS/CAVEMAN.md`

```
---
description: Activate Caveman mode
argument-hint: [lite|full|ultra|off]
---
Activate Caveman mode: $ARGUMENTS
If no level is supplied, use full.
If off, deactivate.
```

## 第 22 页

**Hooks 让 prompt 时刻的选择持久化**

`SessionStart`：`caveman-activate.js`

- 决定本次会话的模式
- 安全地存储模式状态
- 将规则作为隐藏上下文注入
- 在 compaction 后恢复规则
- 清理旧状态；提供状态行

`UserPromptSubmit`：`caveman-mode-tracker.js`

- 检查每条用户 prompt
- 检测 `/caveman ultra`
- 检测“normal mode”之类的短语
- 更新会话模式
- 在聚焦操作后恢复模式

```json
"hooks": {
  "SessionStart":
    ["node caveman-activate.js"],
  "UserPromptSubmit":
    ["node caveman-mode-tracker.js"]
}
```

SessionStart 初始化行为。UserPromptSubmit 在对话中途检测变化。

## 第 23 页

**MCP 把压缩暴露为可调用工具**

五个 MCP 工具：

- `caveman_compress`：压缩 + 恢复句柄
- `caveman_retrieve`：字节级精确原文
- `caveman_stats`：压缩统计
- `caveman_toon_encode`：JSON 转 TOON
- `caveman_toon_decode`：TOON 转回 JSON

MCP CONFIGURATION

```json
{"mcpServers": {
  "caveman": {
    "command": "npx",
    "args": ["-y","caveman-mcp"]
```

EXAMPLE TOOL RESULT

```json
"compressed": "3 tests fail.
   Root error: timeout.",
"ratio": 0.72,
"recovery_handle": "ccr_abc123"
```

## 第 24 页

**代理压缩模型读到的内容**

编程智能体 → 本地 Caveman 代理 → 模型提供商

TYPE-AWARE COMPRESSION——保留什么

- 日志：错误、栈追踪、头 + 尾
- 代码：imports、签名、类型、函数体
- Diff：文件 + hunk 头、变更行
- JSON：键、结构、错误子树
- 搜索：高价值匹配、诊断
- HTML / 文本：标题、相关章节

PROXY vs MCP

- 拦截每个请求；MCP 只在被调用时运行
- 位于智能体与提供商之间；MCP 位于旁边
- 代理改变上下文；MCP 不能

Hooks 拦截请求——但它们无法透明地重写发给 LLM 的请求。需要代理。

如果你自己写 harness，那就可以。

## 第 25 页

**Caveman 中各项能力如何配合**

- Skills：简洁风格、聚焦工作流
- Hooks：激活、跟踪、强化模式
- Commands：选择模式、请求操作
- MCP：压缩、检索、统计、编码
- Plugin：打包 Claude Code 集成
- Local proxy：拦截提供商请求

PACKAGE：Caveman plugin——一个安装与更新单元

MECHANISMS：Skills、Commands、Hooks、MCP server

STATE + ENGINE：会话模式状态、压缩引擎

INTERCEPT：本地代理——位于智能体与模型提供商之间

## 第 26 页

**借助多个长时运行智能体成为 100 倍工程师**

- 手工并行智能体
- 子智能体
- 智能体团队
- 动态工作流

智能体并行铺开，账单也是。

1. 出现　2. 保持清醒　在这里完成　午饭前搞定

如何在两小时内完成作业？

## 第 27 页

**扩展的三个轴**

**并行智能体——广度**

- 运行多个独立任务，每个在隔离的工作树中
- 换取吞吐量：墙钟时间，而非答案质量

**子智能体——广度与深度**

- 把有界任务委派给全新上下文；返回摘要
- 换取吞吐量与专注：父级永远看不到中间的混乱

**长时运行智能体——持续时间**

- 让更大的工作跨越许多步骤
- 换取范围：更少干预、更多工作

智能体团队与动态工作流把它们组合起来。

## 第 28 页

**手工并行智能体**

每个会话一个任务，各自位于自己的 git worktree——一个独立的工作目录和分支，共享仓库历史。

```
claude -w feature-payments
```

终端 1 在自己的分支上构建功能。

```
claude -w bugfix-auth
```

终端 2 修复 bug，不受第一个影响。

一个会话中的编辑永远不会碰到另一个会话的文件。

无需 stash，无需第二个 clone。在桌面应用中，每个新会话自动获得一个 worktree。

## 第 29 页

**Git Worktree：一个仓库，多个工作目录**

一个仓库

```
.git
history · branches
objects · remotes
```

- `../repo-main`——分支：main（Agent 1：审查）
- `../feat-auth`——分支：feature/auth（Agent 2：构建）
- `../fix-flaky`——分支：fix/flaky-test（Agent 3：调试）

一份共享历史。三个检出。无需切换分支，无需 stash。

## 第 30 页

**手工并行的极限**

几个会话是生产力提升。二十个会话就需要克隆一个你自己。

- **计划在你脑中**——每次交接和下一步都只存在于你脑子里
- **会话彼此不可见**——发现只有在你亲自搬运时才会流动
- **由你协调分支**——合并顺序和冲突由你处理
- **它不会重复**——运行过程没有任何记录可供重跑

3 个会话：你能掌握计划。

20 个会话：你需要一个克隆。你 / 你 + 一个克隆。

## 第 31 页

**子智能体：为什么？**

一个拥有自己上下文窗口、工具和权限的专门助手。

- 保留上下文
  - 日志、搜索结果和文件转储留在主对话之外。
- 强制约束
  - 限制子智能体可以使用哪些工具，以及由哪个模型运行。
- 随处复用
  - 面向某个领域的聚焦 prompt，可跨项目和团队共享。
- 并行化
  - 独立子任务并发运行，因此最慢的那个决定总时间。
  - style-checker、security-scanner 和 test-coverage 同时运行。
- 控制成本
  - 把任务路由到更快、更便宜的模型，如 Haiku。
  - 在子智能体的 frontmatter 中写 `model: haiku`。

code.claude.com/docs/en/sub-agents

## 第 32 页

**内置子智能体**

Claude 会自动委派给这些子智能体。

- **Explore**
  - 只读搜索代码库。Write 和 Edit 被拒绝；彻底程度按调用设置。
- **Plan**
  - 在 plan 模式期间研究，使探索留在主窗口之外。
- **General-purpose**
  - 需要探索和行动的复杂多步工作。

Explore 和 Plan 跳过 CLAUDE.md 和 git status，以保持快速和低成本。

## 第 33 页

**定义子智能体**

一个带 YAML frontmatter 的 Markdown 文件；正文成为 system prompt。

`.claude/agents/code-reviewer.md`

```
---
name: code-reviewer
description: Reviews code for quality
tools: Read, Glob, Grep
model: sonnet
---
You are a code reviewer. Analyze the
code and give actionable feedback.
```

- `.claude/agents/`
  - 项目作用域——纳入版本控制，团队共享。
- `~/.claude/agents/`
  - 用户作用域——在你所有项目中可用。

## 第 34 页

**定义嵌套子智能体**

子智能体 frontmatter：

```
---
name: my-orchestrator
tools: Read, Grep, Agent
model: claude-sonnet-5-0
---
```

Agent 必须出现在 tools 中，子智能体才能派生子级。

调用本身：

父智能体 → Agent 工具调用 → 子智能体 1 / 子智能体 2

最多允许 5 层嵌套。2 到 3 层是甜点。

## 第 35 页

**多级子智能体：常见模式**

- Level 0：主智能体——拥有计划
- Level 1：实现子智能体、调试子智能体、代码审查子智能体
- Level 2：测试编写子智能体、验证子智能体

每一层都从全新上下文开始，只返回摘要。

## 第 36 页

**与子智能体协作**

自动委派会自行发生——当它没有发生时，显式升级。

1. **自然语言**
   - 在 prompt 中点名子智能体——Claude 决定是否委派。
   - “用 test-runner 子智能体修复测试”
   - 作用域：一次性
2. **@提及**
   - 选择子智能体，它保证运行。
   - `@agent-code-reviewer look at auth changes`
   - 作用域：一个任务
3. **`--agent` 标志**
   - 整个会话采用其 prompt、工具和模型。
   - `claude --agent code-reviewer`
   - 作用域：整个会话

对运行哪个子智能体的控制逐级增强。

## 第 37 页

**子智能体，还是主对话？**

子智能体从零开始：它看不到历史，并且要付出延迟成本来收集上下文。

想在主上下文中获得可复用工作流？用 Skill。

**留在主对话**

- 迭代式来回
- 共享上下文的阶段
- 快速、有针对性的修改
- 延迟重要

**委派给子智能体**

- 你不会复用的冗长输出
- 工具或权限限制
- 返回摘要的自包含工作
- 并行、独立的工作
- 简单工作可委派给小模型

## 第 38 页

**智能体团队**

多个 Claude Code 会话协同工作：一个负责人，若干队友。

- **审查**
  - 队友从不同角度探查，然后互相质疑发现。
- **独立模块**
  - 每个队友拥有独立部分，互不干扰。
- **调试**
  - 并行测试竞争假设，更快收敛。
- **跨层**
  - 前端、后端和测试，各由一名队友负责。

不是免费的：协调开销和 token 成本随团队规模增长。

顺序任务、同文件编辑或重依赖——使用单个会话或子智能体。

实验性——默认关闭。code.claude.com/docs/en/agent-teams

## 第 39 页

**团队如何连接**

四个部分，队友之间直接对话。

- **团队负责人**
  - 主会话：派生队友、协调工作、综合结果。
- **队友**
  - 独立的 Claude Code 实例，各自拥有上下文窗口。
- **任务列表**
  - 共享工作项，队友认领并标记完成。
- **邮箱**
  - 每个智能体一个 JSON 收件箱。

队友不继承你的对话。它们会自动加载 CLAUDE.md 和 skills，任务细节放在 prompt 中。

## 第 40 页

**智能体团队 vs 子智能体**

子智能体向负责人汇报。队友共享任务列表并互相交谈。

子智能体：主智能体 → 子智能体 ×3 → 结果返回主智能体

智能体团队：主智能体（团队负责人）→ 共享任务列表 → 队友 ×3，认领任务并互相发消息

## 第 41 页

**子智能体 vs 智能体团队**

| | 子智能体 | 智能体团队 |
| --- | --- | --- |
| 上下文 | 自己的窗口，结果返回调用者 | 自己的窗口，独立 |
| 通信 | 只返回调用者 | 队友之间 |
| 协调 | 负责人管理工作 | 共享任务列表 |
| 最适合 | 只需结果的任务 | 工作需要讨论 |
| Token 成本 | 较低 | 较高 |

团队成本更高——只在工作需要讨论时使用。

## 第 42 页

**子智能体 vs 智能体团队**

| | 子智能体 | 智能体团队 |
| --- | --- | --- |
| 上下文 | 自己的窗口，结果返回调用者 | 自己的窗口，独立 |
| 通信 | 只返回调用者 | 队友之间 |
| 协调 | 负责人管理工作 | 共享任务列表 |
| 最适合 | 只需结果的任务 | 工作需要讨论 |
| Token 成本 | 较低 | 较高 |

团队成本更高——只在工作需要讨论时使用。

## 第 43 页

**动态工作流**

一个 JavaScript 脚本，在后台编排许多子智能体。

当任务需要的智能体超过一个对话能协调的数量时使用它。

- 全代码库 bug 清扫
- 500 文件迁移
- 交叉核查研究
- 从多个角度制定计划

两种启动方式：

- `ultracode`：在 prompt 中输入
- `/effort ultracode`：让 Claude 替你决定

两种途径都会派生许多子智能体——计划、设计、实现、审查。

## 第 44 页

**长时运行智能体：`/goal`**

交出一个可验证的最终状态；Claude 持续工作直到它成立。

```
/goal "npm run lint exits with zero errors"
```

- **定义完成**
  - 一个 Claude 可以测试的条件：测试通过、lint 零错误。
- **自我检查**
  - 评估器在每次尝试后重新检查条件，然后把 Claude 送回。
- **自行停止**
  - 目标达成时结束，或 `--max-tries` 用尽时结束。

必须可验证！“all integration tests pass” 可以，“refactor the code” 不行。

## 第 45 页

**长时运行智能体：`/loop`**

按计划重新运行 prompt；它持续运行直到你停止。

```
/loop 5m "check CI, fix whatever broke"
```

- **触发器，不是测试**
  - 你交出间隔；同样的 prompt 每次重新运行。
- **由你结束**
  - 它反复迭代，直到你在两次运行之间的等待中按 Esc。
- **自己的默认值**
  - 把默认 prompt 放在 `.claude/loop.md`。

`/goal` 在条件成立时停止。`/loop` 在你要求时停止。

## 第 46 页

**小结**

用多智能体放大能力的四种方式——以及让一个智能体持续运行的两种方式。

一次更多智能体：

- 并行智能体（手工）——由你自己协调
- 子智能体——Claude 委派；结果返回给它
- 智能体团队——负责人在共享列表上监督同伴
- 工作流——由脚本而非聊天持有计划

一个智能体，运行更久：

- `/goal`：运行到可验证的最终状态成立
- `/loop`：按计划重跑，直到你停止

## 第 47 页

**智能体团队示例：十六个智能体构建了一个 C 编译器**

一个能构建 Linux 内核的 Rust C 编译器——16 个智能体、约 2,000 个会话、两周

**规模**

- 16 个智能体并行工作
- 两周内约 2,000 个会话
- 2B 输入 / 140M 输出 tokens
- API 成本略低于 20,000 美元

**结果**

- 约 100,000 行代码
- 在 x86、ARM 和 RISC-V 上运行 Linux 6.9
- QEMU、FFmpeg、Postgres、Redis、Doom
- 主要测试套件约 99% 通过率

OPTIONAL——额外阅读，非必需

https://www.anthropic.com/engineering/building-c-compiler

## 第 48 页

**十六个智能体如何协调**

普通基础设施——容器、Git 和文本文件——完成了编排。

- 每个智能体在隔离容器和 Git 检出中
- 任务通过简单的锁文件认领
- Git 作为协调与集成层
- 新会话读取进度文档以恢复上下文
- 文档、性能、质量、去重的专家智能体
- 自动化测试给智能体提供进度信号

OPTIONAL——额外阅读，非必需

## 第 49 页

**Git 作为协调层**

没有聊天，没有管理者智能体——智能体通过共享的 Git 状态协调。

- 读取仓库：clone，扫描 docs 和 logs
- 认领任务：`current_tasks/` 中的锁文件
- 实现并测试：在自己的容器中
- 合并、推送、解锁：先 pull 其他人的

循环重复——智能体自己挑选下一个显然的任务；Git 裁决重复认领。

**冲突自行解决**

- 同一任务被认领两次？一个智能体转向其他工作

**工件携带上下文**

- README、进度文档、CI 失败为新会话提供简要信息

OPTIONAL——额外阅读，非必需

## 第 50 页

**成功，但不完全**

智能体还不完美，你还有更多工作要做！

- 合并冲突频繁
- 一旦每个智能体都撞上同一个内核失败，并行就不再有帮助
- 16 位 x86 的部分仍依赖 GCC
- 生成代码效率低于 GCC 输出

OPTIONAL——额外阅读，非必需

## 第 51 页

**编程 / Software 3.0**

## 第 52 页

**编程 3.0**

**PROGRAMMING 1.0（对硬件编程）**

人类 → 显式机器指令或汇编 → 硬件

**PROGRAMMING 2.0（对编程语言编程）**

人类 → 编程语言 → 编译器 → 机器指令 → 硬件

**PROGRAMMING 3.0（表达目标）**

人类 → 自然语言 → 智能体 → 编程语言 → 机器指令 → 硬件

这是我创造的一个术语，与 Andrej 的定义不同（下一页）。

更高的生产力 / 更多的不确定性

## 第 53 页

**Software 3.0**

- Software 1.0：人类 → 代码 → 计算机
- Software 2.0：人类 → 数据 → 优化器 → 神经网络
- Software 3.0：人类 → 语言 / 上下文 → LLM → 动作

Software Is Changing (Again)——YouTube

知道在哪里划出 1.0、2.0 和 3.0 之间的边界，是一项重要的工程技能。

| 范式 | 程序是什么？ | 如何创建？ |
| --- | --- | --- |
| 1.0 | 源代码 | 编写 Python/C++ |
| 2.0 | 神经网络权重 | 收集数据 + 优化 |
| 3.0 | LLM prompts | 自然语言 |

Andrej Karpathy

## 第 54 页

**编程 3.0 中的不确定性**

不确定性成为核心主题，你应该学会与之共处！

## 第 55 页

**不确定性是新的吗？**

| 不确定性来源 | Programming 2.0 | Programming 3.0 新增 |
| --- | --- | --- |
| 硬件 | 架构：32 位 vs 64 位、字节序 | GPU 计算；非确定性 kernel、浮点方差 |
| 环境 | 并发、不可靠网络 | 在代码生成时交互——它边写边触碰环境 |
| 软件 | 编译器版本、依赖漂移 | 编译器、模型、不同 kernel、采样 |

**2.0 如何解决**

- 固定宽度类型、交叉编译、虚拟化
- 内存一致性模型、幂等 API
- 升级前全面测试

相同的源代码 != 相同的输出，这在很久以前就发生过。

## 第 56 页

**更多不确定性：从意图到结果**

1.0 / 2.0：人类（PM）→ 需求 → 程序员 → 环境、内存、程序 → 结果

3.0：人类 → 需求 → LLM 智能体 → 环境、内存、程序 → 结果

- 形式化验证：在上一页讨论过
- 被忽略（但存在）
- 由于单条 prompt 导致的歧义输入：需要更多研究

## 第 57 页

**与不确定性共处**

- 自然语言的语义不确定性
- 检索 / 上下文检索漂移
  - 索引更新、分块、上下文截断
- 模型生成的概率性变化
  - 1. 采样
  - 2. 软件与硬件非确定性
- 智能体 / 工具循环
  - 轨迹 / 环境非确定性
  - 工具失败
  - 环境变化

生成出的程序一旦生成通常是确定性的，除非它在运行时调用模型或工具。

## 第 58 页

**编程 / Software 3.0 最佳实践**

**1 · 定义**

- 一开始就陈述假设
  - 让模型在执行前确认任何含糊之处。

**2 · 控制**

- 把提案与执行分开
  - 智能体提出计划；在提交任何内容前验证。
- 显式管理上下文
  - 拥有记忆、来源和检索；让过时信息过期。
- 指定结果，而非 prompt
  - 给出需求、不变量、约束和验收测试。

**3 · 验证与治理**

- 收紧生成—验证循环
  - 廉价、频繁的检查胜过最后一次性昂贵审查。
- 更深一层地测量
  - 创建测试、测量多个指标、构造你能推理的合成工作负载。

## 第 59 页

**不要指望智能体是确定性的；让周围系统可靠。**

**让自主性与风险匹配：自主性越高，不确定性和风险越高。**

## 第 60 页

**来自一线的证据**

Codex 的证据（2026 年 6 月）

OpenAI 员工使用情况（2026 年 9 月）

## 第 61 页

**从对话到委派**

**Conversational AI**

- 人类提问
- 模型回答
- 人类留在循环中
- 人类执行工作
- 人类是执行者。

**Agentic AI（Codex）**

- 人类委派任务
- 智能体计划、调用工具、编辑文件、运行命令
- 交付工件或动作
- 人类审查并集成。

向智能体 AI 的转变：来自 Codex 的证据

2026 年上半年活跃用户增长超过 5 倍。

过去 28 天使用 Codex：

- 个人：< 1%
- 组织：17.3%
- OpenAI 员工：几乎全部

## 第 62 页

**被委派的任务正在变得大得多**

| | 2025 年 12 月 | 2026 年 5 月 |
| --- | --- | --- |
| 任务 ≥ 1 人时 | 35.4% | 70.2% |
| 任务 ≥ 8 人时 | 2.1% | 25.6% |

至少提交过一项此类任务的个人用户占比。

线程中的第一条 prompt 通常是最复杂的一条。

处理全天任务的用户增长了 12 倍。

## 第 63 页

**一个人，多个智能体**

人类 → Agent A 构建功能 / Agent B 运行分析 / Agent C 调试 + 测试 → 审查 · 集成 · 重新委派

- 28.6% 的 OpenAI 用户在一周内同时运行 5+ 个智能体
- 中位数 OpenAI 员工每天约 2.5 智能体小时
- 第 99 百分位每天约 71 智能体小时（自 4 月以来 +88%）

人类角色转变为计划者、委派者、监督者、审查者、集成者。

2026 年 6 月

## 第 64 页

**智能体工作日已远超人类研究者**

2026 年 6 月之前，智能体运行时间落后于人类劳动；现在智能体做的工作是人类 3.14 倍。

大多数研究者有 4+ 个并发工作流（未显示）。

2026 年 9 月

## 第 65 页

**工程师交付速度几乎快 8 倍**

## 第 66 页

**智能体解决越来越复杂的任务**

**但人类干预仍然必要**

## 第 67 页

**编程智能体正在重塑 OpenAI 研究人员的日常工作**

研究加速：OpenAI 内部视角

2026 年 9 月

## 第 68 页

**委派阶梯**

1. 聊天机器人——AI 回答；人类完成工作
2. 助手——人类与 AI 一起完成任务
3. 智能体——人类委派一个完整工作单元
4. 多智能体工作者——人类协调多个智能体
5. 系统化工作流——skills 与智能体运行流程

OpenAI 的劳动力位于接近底部的位置。

## 第 69 页

**下一节课**

- 智能体设计 I
- 找助教登记参与分

## 第 70 页

**可选幻灯片**

## 第 71 页

**超越 Claude Code**

- **模型实验室**——模型 + 框架一体
  - Claude Code、Codex CLI、Antigravity CLI、Grok Build、Mistral Vibe、Kimi Code、Qwen Code
- **平台 CLI**——位于开发栈内
  - Copilot CLI、Cursor CLI、Amp、Auggie、Droid、Junie CLI、Qoder、CodeBuddy
- **开源**——自带 key
  - OpenCode、Crush · Goose、Aider · Cline、Kilo · Continue、OpenHands、Reasonix、Codebuff
- **极简核心**——小而可审计
  - Deepseek Harness、Pi · oh-my-pi (Omp)、mini-SWE-agent、gptme、Open Interpreter

State of CLI Coding Agents, Mid-2026 (July 2026)

## 第 72 页

**它们有何不同：五个关键维度**

- **开放 vs 闭源**
  - 开放：Codex CLI、OpenCode、Goose、Cline、Pi
  - 闭源：Claude Code、Copilot CLI、Cursor、Droid、Junie
- **锁定 vs BYOK**
  - 单一供应商：Claude Code、Antigravity CLI、Grok Build
  - 任意端点：OpenCode 支持 75+ 提供商，Kilo 支持 500+ 模型
- **沙箱 vs prompt**
  - OS 沙箱：Codex CLI、Copilot CLI、OpenHands 容器
  - 权限 prompt：Claude Code 及大多数其他工具
- **本地 vs 云**
  - 本地优先、无遥测：Goose、Nanocoder、gptme
  - 云端交接：Copilot CLI、Codex、Mistral Vibe 远程智能体
- **最大 vs 最小**
  - 包含一切：Omp（功能最广）、Claude Code
  - 只有四个工具：Pi、mini-SWE-agent（约 100 行 Python）

State of CLI Coding Agents, Mid-2026 (July 2026)
