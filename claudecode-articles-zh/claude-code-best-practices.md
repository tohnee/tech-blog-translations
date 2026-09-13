---
title: "Claude Code：智能体编码最佳实践"
title_en: "Claude Code: Best practices for agentic coding"
source: https://www.anthropic.com/engineering/claude-code-best-practices
published: 2025-04-18
subjects: ["Developer Tools"]
note: 原博客 URL 现重定向至 code.claude.com/docs/en/best-practices，本档按该官方现行页面存档；原 2025-04 博客版本因 Wayback 不可达未采用
crawled: 2026-09-11
translated: 2026-09-11
---

# Claude Code：智能体编码最佳实践

> 原文：[Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices) · Anthropic Engineering Blog

从配置环境到跨并行会话扩展，充分发挥 Claude Code 效能的技巧与模式。

Claude Code 是一个智能体编码环境。与只会回答问题然后等待的聊天机器人不同，Claude Code 能读取你的文件、运行命令、做出修改，并在你旁观、纠偏或干脆走开时自主地解决问题。
这改变了你的工作方式。你不再自己写代码然后让 Claude 审查，而是描述你想要什么，由 Claude 想清楚如何实现。探索、规划、实现，都由 Claude 完成。
但这种自主性仍带有学习曲线。Claude 在一些特定约束下工作，你需要理解它们。
本指南汇集了在 Anthropic 内部团队以及各类代码库、语言和环境中使用 Claude Code 的工程师们验证有效的模式。关于智能体循环的底层原理，参见 [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)。

---

大多数最佳实践都基于同一个约束：Claude 的上下文窗口很快被填满，而性能会随着填充而下降。
Claude 的上下文窗口容纳你的整个对话，包括每条消息、Claude 读过的每个文件、每条命令输出。然而它会很快被填满——一次调试会话或代码库探索就可能生成并消耗数以万计的 token。
这一点很重要，因为 LLM 的性能会随着上下文填充而退化。当上下文窗口接近满载时，Claude 可能开始「忘记」较早的指令或犯更多错误。上下文窗口是最需要管理的资源。想直观了解会话如何被填满，可以[观看交互式演示](https://code.claude.com/docs/en/context-window)，看看启动时加载了什么、读每个文件代价多大。用[自定义状态行](https://code.claude.com/docs/en/statusline)持续跟踪上下文用量，并参考[减少 token 用量](https://code.claude.com/docs/en/costs#reduce-token-usage)了解节省 token 的策略。

---

## 给 Claude 一种验证自身工作的手段

给 Claude 一个它能自己运行的检查：测试、构建、可对比的截图。这决定了这场会话是你盯着的，还是你可以走开的。

当工作「看起来完成了」，Claude 就会停下。如果没有它能运行的检查，「看起来完成」就是唯一可用的信号，而你就成了验证循环本身：每一个错误都在等你去发现。给 Claude 一个能产出通过/失败信号的东西，循环就会自己闭合：Claude 干活、跑检查、读结果、迭代，直到检查通过。

这个检查可以是任何能在对话中返回 Claude 可读信号的东西：测试套件、构建退出码、linter、把输出与 fixture 做 diff 的脚本，或者与设计稿对比的[浏览器截图](https://code.claude.com/docs/en/chrome)。在 Claude 的检查通过之后，你自己再跑一次 [`/verify`](https://code.claude.com/docs/en/skills#run-and-verify-your-app)，对照运行中的应用确认改动。

| 策略 | 改进前 | 改进后 |
| --- | --- | --- |
| **提供验证标准** | *「实现一个校验邮箱地址的函数」* | *「写一个 validateEmail 函数。示例测试用例：[user@example.com](mailto:user@example.com) 为 true，无效输入为 false，[user@.com](mailto:user@.com) 为 false。实现后运行测试」* |
| **对 UI 改动做视觉验证** | *「把仪表盘弄好看点」* | *「[粘贴截图] 按这个设计实现。对结果截图并与原图对比。列出差异并修复」* |
| **解决根因而非症状** | *「构建挂了」* | *「构建报了这个错：[粘贴错误]。修好并验证构建成功。解决根因，不要压制错误」* |

检查就位后，再决定它以多强的力度把守「停止」：

- **在同一条提示里**：像上表那样，要求 Claude 在同一消息中运行检查并迭代。
- **贯穿整个会话**：把检查设为 [`/goal` 条件](https://code.claude.com/docs/en/goal)。一个独立的评估器在每轮之后重新检查，Claude 会持续工作直到目标达成。如果 Claude 停滞不前，Claude Code 最终会带着未达成的目标停止运行——参见 [/goal 评估的工作方式](https://code.claude.com/docs/en/goal#how-evaluation-works)。
- **作为确定性关卡**：一个 [Stop hook](https://code.claude.com/docs/en/hooks#stop) 以脚本形式运行你的检查，并在检查通过前阻止回合结束。连续阻止 8 次后，Claude Code 会越过该钩子并结束回合。
- **借助第二意见**：用一个[验证子智能体](https://code.claude.com/docs/en/sub-agents)或一个会复核自身发现的[动态工作流](https://code.claude.com/docs/en/workflows)，让一个全新的模型尝试反驳结果——干活的智能体就不给自己打分了。

每一步都是用配置换取你的注意力。提示版本今天就能用于任何任务；`/goal` 和 Stop hook 版本则能让无人值守的运行在没有你的情况下正确收尾。

让 Claude 出示证据而不是宣称成功：测试输出、它运行的命令及其返回、或结果截图。审查证据比你亲自重跑验证更快，而且适用于你没盯着的会话。

---

## 先探索，再规划，然后编码

把调研和规划与实现分开，避免解错问题。

放任 Claude 直接开写，可能产出一个解错了问题的方案。用[计划模式（plan mode）](https://code.claude.com/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode)把探索与执行分开。

推荐的工作流分四个阶段：

**1. 探索**

按 `Shift+Tab` 直到状态栏显示 `⏸ plan mode on` 进入计划模式，或用 `claude --permission-mode plan` 启动会话。Claude 只读文件、回答问题，不做修改。

```
read /src/auth and understand how we handle sessions and login.
also look at how we manage environment variables for secrets.
```

**2. 规划**

让 Claude 制定详细的实现计划。

```
I want to add Google OAuth. What files need to change?
What's the session flow? Create a plan.
```

按 `Ctrl+G` 在文本编辑器中打开该计划，在 Claude 继续之前直接编辑。

**3. 实现**

批准计划或按 `Shift+Tab` 退出计划模式，然后让 Claude 编码，并对照计划自行验证。

```
implement the OAuth flow from your plan. write tests for the
callback handler, run the test suite and fix any failures.
```

**4. 提交**

让 Claude 带着描述性提交信息提交并创建 PR。

```
commit with a descriptive message and open a PR
```

计划模式有用，但也会增加开销。对于范围清晰、改动很小的任务（修个错别字、加一行日志、重命名变量），直接让 Claude 干就行。规划在你对方案不确定、改动涉及多个文件、或你对被修改的代码不熟悉时最有价值。如果你能用一句话描述出 diff，就跳过计划。

---

## 在提示中提供具体的上下文

指令越精确，你需要纠正的次数就越少。

Claude 能推断意图，但不能读心。引用具体文件、说明约束、指出示例模式。

| 策略 | 改进前 | 改进后 |
| --- | --- | --- |
| **限定任务范围。** 指明哪个文件、什么场景、测试偏好。 | *「给 foo.py 加测试」* | *「为 foo.py 写一个测试，覆盖用户已登出的边界情况。不要用 mock」* |
| **指向信息源。** 把 Claude 引向能回答问题的源头。 | *「为什么 ExecutionFactory 的 API 这么奇怪？」* | *「翻一翻 ExecutionFactory 的 git 历史，总结它的 API 是如何演化成现在这样的」* |
| **参照现有模式。** 把 Claude 指向你代码库中的既有模式。 | *「加一个日历组件」* | *「看看首页现有组件是怎么实现的，理解其中的模式。HotDogWidget.php 是个好例子。照这个模式实现一个新的日历组件，让用户选择月份并前后翻页选择年份。只用代码库中已有的库，从零构建」* |
| **描述症状。** 给出症状、可能位置，以及「修好了」长什么样。 | *「修一下登录 bug」* | *「用户反馈会话超时后登录失败。检查 src/auth/ 的认证流程，尤其是 token 刷新。先写一个能复现问题的失败测试，再修复」* |

模糊的提示在你探索、且付得起纠偏成本时也有用。像 *「你觉得这个文件有什么可以改进的？」* 这样的提示，可能挖出你本来想不到要问的东西。

### 提供丰富的内容

用 `@` 引用文件、粘贴截图/图片，或直接管道传数据。

你可以用几种方式给 Claude 提供丰富的数据：

- **用 `@` 引用文件**，而不是描述代码在哪里。Claude 会在回答前读取该文件。
- **直接粘贴图片**。复制粘贴或拖放图片到提示中。
- **给 URL** 指向文档和 API 参考。用 `/permissions` 把常用域名加入允许列表。
- **管道传入数据**，运行 `cat error.log | claude` 直接发送文件内容。
- **让 Claude 自取所需**。告诉 Claude 用 Bash 命令、MCP 工具或读文件的方式自己拉取上下文。

---

## 配置你的环境

几个设置步骤能让 Claude Code 在你的所有会话中显著更有效。扩展功能的全貌及各自适用时机，参见 [Extend Claude Code](https://code.claude.com/docs/en/features-overview)。

### 写一份有效的 CLAUDE.md

运行 `/init` 基于当前项目结构生成一份初始 CLAUDE.md，之后持续打磨。

CLAUDE.md 是一个特殊文件，Claude 在每次对话开始时都会读取它。把 Bash 命令、代码风格、工作流规则写进去。这给了 Claude 无法仅凭代码推断的持久上下文。

CLAUDE.md 没有固定格式，但要保持简短、人类可读。例如：

```
# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible (eg. import { foo } from 'bar')

# Workflow
- Be sure to typecheck when you're done making a series of code changes
- Prefer running single tests, and not the whole test suite, for performance
```

运行 `/context` 确认 Claude 已加载该文件。CLAUDE.md 每个会话都会加载，所以只写普遍适用的内容。只在某些时候才相关的领域知识或工作流，改用 [skills（技能）](https://code.claude.com/docs/en/skills)：Claude 按需加载它们，不会撑大每场对话。

保持精炼。对每一行都问一句：*「删掉这行会让 Claude 犯错吗？」* 不会就删。臃肿的 CLAUDE.md 会让 Claude 忽视你真正的指令！

| ✅ 应当包含 | ❌ 不应包含 |
| --- | --- |
| Claude 猜不到的 Bash 命令 | Claude 读代码就能搞清楚的任何东西 |
| 与默认习惯不同的代码风格规则 | Claude 已然掌握的语言标准惯例 |
| 测试指令和偏好的测试运行器 | 详细的 API 文档（改为链接文档） |
| 仓库礼仪（分支命名、PR 约定） | 频繁变动的信息 |
| 项目特有的架构决策 | 长篇解释或教程 |
| 开发环境的怪癖（必需的环境变量） | 逐文件的代码库说明 |
| 常见坑或非显而易见的行为 | 「写整洁的代码」这类不言自明的口号 |

如果尽管有规则 Claude 还是反复做你不想要的事，多半是文件太长、规则被淹没了。如果 Claude 问的问题在 CLAUDE.md 里已有答案，可能是措辞有歧义。把 CLAUDE.md 当代码对待：出问题时复审、定期修剪、通过观察 Claude 行为是否实际改变来测试改动。对于纳入版本控制的 CLAUDE.md，可以运行 [`/doctor`](https://code.claude.com/docs/en/commands#all-commands)，Claude 会就它能从代码库中推导出来的内容提出删减建议。

如果 Claude 总是跳过某一条指令，只给那一行加强调，比如「IMPORTANT」。强调太多行，等于没有强调。把 CLAUDE.md 提交进 git，让团队共同维护——这个文件的价值会随时间复利增长。

CLAUDE.md 可以用 `@path/to/import` 语法导入其他文件。导入规则及 CLAUDE.md 可放置的位置，参见 [CLAUDE.md files](https://code.claude.com/docs/en/memory#claude-md-files)。

### 配置权限

想少被打断又不放弃控制：用 `/permissions` 预批准你信任的工具，用 `/sandbox` 让沙箱化的命令免询问运行。想亲自审批编辑和命令时切回手动（Manual）模式。

在 Pro、Max 和 Team 套餐上，自动模式（auto mode）是交互式终端与 VS Code 会话的[内置默认权限模式](https://code.claude.com/docs/en/permission-modes#eliminate-prompts-with-auto-mode)：由一个独立的分类器模型代替你审查大多数操作，只拦截看起来有风险的动作，例如权限范围升级、未知基础设施、或受敌意内容驱动的操作。

在手动模式（其他套餐的内置默认权限模式）下，Claude Code 会在可能修改系统的动作前询问：文件写入、Bash 命令、MCP 工具。这很安全但很烦：第十次点「批准」时你已经不是在审查而是在点鼠标了。两个工具能削减手动模式下的这些打扰，并且在自动模式下同样适用：

- **权限允许列表**：放行你确知安全的特定工具，如 `npm run lint` 或 `git commit`
- **沙箱机制**：启用操作系统级隔离，限制文件系统和网络访问，让 Claude 在划定边界内更自由地工作

更多内容参见[权限模式](https://code.claude.com/docs/en/permission-modes)、[权限规则](https://code.claude.com/docs/en/permissions)与[沙箱机制](https://code.claude.com/docs/en/sandboxing)。

### 使用 CLI 工具

让 Claude Code 在与外部服务交互时使用 `gh`、`aws`、`gcloud`、`sentry-cli` 等 CLI 工具。

CLI 工具是与外部服务交互时上下文效率最高的方式。如果你用 GitHub，装上 `gh` CLI——Claude 知道怎么用它创建 issue、开 pull request、读评论。没有 `gh`，Claude 仍可走 GitHub API，但未认证的请求常常撞上速率限制。

Claude 也很擅长学习它不认识的 CLI 工具。试试这样的提示：`Use 'foo-cli-tool --help' to learn about foo tool, then use it to solve A, B, C.`

### 连接 MCP 服务器

运行 `claude mcp add` 加上服务器名称和 URL 或命令，即可连接 Notion、Figma 或你的数据库等外部工具。例如：`claude mcp add --transport http notion https://mcp.notion.com/mcp`。

借助 [MCP 服务器](https://code.claude.com/docs/en/mcp)，你可以让 Claude 从 issue 跟踪器实现功能、查询数据库、分析监控数据、集成 Figma 设计稿、自动化工作流。

### 设置钩子（hooks）

必须每次发生、零例外的事情，交给钩子。

[钩子](https://code.claude.com/docs/en/hooks-guide)在 Claude 工作流的特定节点自动运行脚本。与 CLAUDE.md 的建议性指令不同，钩子是确定性的，保证动作一定发生。

Claude 可以替你写钩子。试试这样的提示：*「Write a hook that runs eslint after every file edit」*或*「Write a hook that blocks writes to the migrations folder.」*也可以直接编辑 `.claude/settings.json` 手工配置钩子，运行 `/hooks` 浏览已配置的钩子。

### 创建技能（skills）

在 `.claude/skills/` 创建 `SKILL.md` 文件，赋予 Claude 领域知识和可复用的工作流。

[技能](https://code.claude.com/docs/en/skills)用特定于你的项目、团队或领域的知识扩展 Claude。相关时 Claude 会自动应用，你也可以用 `/skill-name` 直接调用。

在 `.claude/skills/` 下添加一个带 `SKILL.md` 的目录即可创建技能：

.claude/skills/api-conventions/SKILL.md

```
---
name: api-conventions
description: REST API design conventions for our services
---
# API Conventions
- Use kebab-case for URL paths
- Use camelCase for JSON properties
- Always include pagination for list endpoints
- Version APIs in the URL path (/v1/, /v2/)
```

技能也可以定义你直接调用的可重复工作流：

.claude/skills/fix-issue/SKILL.md

```
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---
Analyze and fix the GitHub issue: $ARGUMENTS.

1. Use `gh issue view` to get the issue details
2. Understand the problem described in the issue
3. Search the codebase for relevant files
4. Implement the necessary changes to fix the issue
5. Write and run tests to verify the fix
6. Ensure code passes linting and type checking
7. Create a descriptive commit message
8. Push and create a PR
```

运行 `/fix-issue 1234` 调用它。对有副作用、希望手动触发的工作流，使用 `disable-model-invocation: true`。

### 创建自定义子智能体

在 `.claude/agents/` 定义专门的助手，Claude 可将隔离的任务委派给它们。

[子智能体](https://code.claude.com/docs/en/sub-agents)在自己的上下文中、以自己的一组允许工具运行。它们适合要读很多文件、或需要专门聚焦的任务，而不会弄乱你的主对话。

.claude/agents/security-reviewer.md

```
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
- Insecure data handling

Provide specific line references and suggested fixes.
```

明确地让 Claude 使用子智能体：*「Use a subagent to review this code for security issues.」*

### 安装插件

运行 `/plugin` 浏览插件市场。插件无需配置即可添加技能、工具和集成。

[插件](https://code.claude.com/docs/en/plugins)把来自社区和 Anthropic 的技能、钩子、子智能体和 MCP 服务器打包成单个可安装单元。如果你使用强类型语言，装一个[代码智能插件](https://code.claude.com/docs/en/discover-plugins#code-intelligence)，让 Claude 获得精确的符号导航和编辑后的自动错误检测。

关于在技能、子智能体、钩子和 MCP 之间如何取舍，参见 [Extend Claude Code](https://code.claude.com/docs/en/features-overview#match-features-to-your-goal)。

---

## 高效沟通

把你问其他工程师的问题拿来问 Claude；对较大的功能，先让 Claude 采访你、写出规格说明（spec）再开始实现。

### 向代码库提问

把你会问资深工程师的问题问给 Claude。

刚接触一个新代码库时，用 Claude Code 来学习和探索。你可以问 Claude 你会问其他工程师的那类问题：

- 日志是怎么工作的？
- 我怎么新增一个 API 端点？
- `foo.rs` 第 134 行的 `async move { ... }` 是干什么的？
- `CustomerOnboardingFlowImpl` 处理了哪些边界情况？
- 为什么第 333 行的代码调用的是 `foo()` 而不是 `bar()`？

这样使用 Claude Code 是高效的新人上手方式：缩短爬坡时间，减轻其他工程师的负担。不需要特殊提示技巧，直接提问即可。

### 让 Claude 采访你

对较大的功能，先让 Claude 采访你。用一个最小化的提示开场，让 Claude 用 `AskUserQuestion` 工具来采访你。

Claude 会问及你可能还没考虑过的事情：技术实现、UI/UX、边界情况、权衡取舍。发送前把 `[brief description]` 替换成你的功能描述。

```
I want to build [brief description]. Interview me in detail using the AskUserQuestion tool.

Ask about technical implementation, UI/UX, edge cases, concerns, and tradeoffs. Don't ask obvious questions, dig into the hard parts I might not have considered.

Keep interviewing until we've covered everything, then write a complete spec to SPEC.md.
```

规格说明完成后，开一个全新会话来执行它。新会话上下文干净、完全聚焦于实现，而你手里有一份书面规格可以参照。

最有用的规格是自包含的：它点名涉及的文件和接口、声明什么不在范围内，并以一个端到端验证步骤收尾来证明功能可用。把规格写精确所花的时间，比你盯着实现所花的时间回报更高。

---

## 管理你的会话

对话是持久的、可回退的。好好利用这一点！

### 尽早且频繁地纠偏

一旦发现 Claude 跑偏，立即纠正。

最好的结果来自紧密的反馈循环。虽然 Claude 偶尔能一次做对，但快速纠偏通常更快得到更好的方案。

- **`Esc`**：用 `Esc` 键中途叫停 Claude。上下文保留，你可以转向。
- **`Esc + Esc` 或 `/rewind`**：连按两次 `Esc` 或运行 `/rewind` 打开回退菜单，恢复到之前的对话和代码状态，或从选定消息做摘要。
- **「Undo that」**：让 Claude 撤销它的改动。
- **`/clear`**：在不相关的任务之间重置上下文。带着无关上下文的长会话会降低表现。

如果你在一个会话中就同一问题纠正 Claude 超过两次，说明上下文已塞满失败的尝试。运行 `/clear`，带着你学到的教训、用一个更具体的提示重新开始。带更好提示的干净会话，几乎总是胜过塞满累积纠偏的长会话。

### 积极管理上下文

在不相关的任务之间运行 `/clear` 重置上下文。

接近上下文上限时，Claude Code 会自动压缩（compact）对话历史，保留重要的代码与决策，同时腾出空间。

长会话中，Claude 的上下文窗口可能塞满无关的对话、文件内容和命令，这会降低表现，有时还会让 Claude 分心。

- 任务之间频繁使用 `/clear` 彻底重置上下文窗口
- 自动压缩触发时，Claude 会总结最重要的内容，包括代码模式、文件状态和关键决策
- 想要更多控制，运行 `/compact <instructions>`，如 `/compact Focus on the API changes`
- 只压缩部分对话：用 `Esc + Esc` 或 `/rewind`，选择一个消息检查点，然后选 **Summarize from here**（从此处开始摘要）或 **Summarize up to here**（摘要到此为止）。前者压缩该点之后的消息并保留更早的上下文；后者压缩更早的消息并完整保留近期消息。参见[回退菜单的摘要选项](https://code.claude.com/docs/en/checkpointing#rewind-and-summarize)。
- 在 CLAUDE.md 中定制压缩行为，例如写上 `"When compacting, always preserve the full list of modified files and any test commands"`，确保关键上下文在摘要后幸存
- 对不需要留在上下文里的问题，使用 [`/btw`](https://code.claude.com/docs/en/interactive-mode#side-questions-with-%2Fbtw)。答案不会进入对话历史，你可以查个细节而不撑大上下文。

### 用子智能体做调查

用 *「use subagents to investigate X」* 把调研委派出去。它们在单独的上下文里探索，让你的主对话保持干净、专注实现。

既然上下文是你的根本约束，就用子智能体把调研挡在主上下文之外。Claude 调研代码库时要读大量文件，全部消耗你的上下文。子智能体运行在独立的上下文窗口中，只汇报摘要回来：

```
Use subagents to investigate how our authentication system handles token
refresh, and whether we have any existing OAuth utilities I should reuse.
```

Claude 实现完之后，你也可以用子智能体验证。参见[加入对抗式审查环节](#加入对抗式审查环节)。

### 用检查点回退

你发送的每条提示都会创建一个检查点。可以把对话、代码或两者恢复到任何先前的检查点。

Claude 在每次改动前自动给文件做快照，因此检查点可以恢复它们。双击 `Escape` 或运行 `/rewind` 打开回退菜单。你可以只恢复对话、只恢复代码、两者都恢复，或从选定消息做摘要。详见 [Checkpointing](https://code.claude.com/docs/en/checkpointing)。

你不必步步谨慎规划，可以让 Claude 去试有风险的方案。不行就回退，换个思路再来。检查点随对话保存，所以你可以关掉终端、稍后恢复会话、继续回退。

检查点只跟踪通过 Claude 文件编辑工具所做的改动。通过 Bash 命令或外部进程做的改动不会被捕捉。它不能替代 git。

### 恢复对话

用 `/rename` 给会话命名，把它们当作分支对待：每个工作流都有自己持久的上下文。

Claude Code 在本地保存对话，所以当一个任务跨越多次坐班时，你不必重新解释上下文。运行 [`claude --continue`](https://code.claude.com/docs/en/sessions#resume-a-session) 从上次中断处继续，或 `claude --resume` 从列表中选择。给会话起描述性名字，如 `oauth-migration`，方便日后查找。恢复、分支和命名的完整控制见 [Manage sessions](https://code.claude.com/docs/en/sessions)。

---

## 自动化与扩展

当你用好了一个 Claude，就用并行会话、非交互模式和扇出（fan-out）模式把产出翻倍。

### 运行非交互模式

在 CI、pre-commit 钩子或脚本中使用 `claude -p "prompt"`。加 `--output-format stream-json --verbose` 获得流式 JSON 输出。

用 `claude -p "your prompt"` 可以非交互地运行 Claude，不进入交互提示。除非传入 `--no-session-persistence`，运行仍会创建可恢复的会话。[非交互模式](https://code.claude.com/docs/en/headless)是把 Claude 接入 CI 流水线、pre-commit 钩子或任何自动化工作流的方式。输出格式让你能以程序方式解析结果：纯文本、JSON 或流式 JSON。

```
# One-off queries
claude -p "Explain what this project does"

# Structured output for scripts
claude -p "List all API endpoints" --output-format json

# Streaming for real-time processing
claude -p "Analyze this log file" --output-format stream-json --verbose
```

第一条命令输出纯文本。`json` 格式返回带 `result` 字段的单个 JSON 对象。`stream-json` 格式每行打印一个 JSON 对象，以 init 事件开头。

### 运行多个 Claude 会话

并行运行多个 Claude 会话，加速开发、运行隔离实验或启动复杂工作流。

按你愿意亲自做多少协调来挑选并行方式，当会话之间需要传递发现时再加消息机制：

- [Worktrees](https://code.claude.com/docs/en/worktrees)：在隔离的 git checkout 中运行独立的 CLI 会话，编辑互不冲突
- [跨会话消息](https://code.claude.com/docs/en/cross-session-messaging)：让你自己运行的会话互相传递发现
- [桌面应用](https://code.claude.com/docs/en/desktop#work-in-parallel-with-sessions)：可视化管理多个本地会话，各自在自己的 worktree 中
- [网页版 Claude Code](https://code.claude.com/docs/en/claude-code-on-the-web)：在云端运行会话，默认跑在 Anthropic 托管的基础设施上
- [Agent view](https://code.claude.com/docs/en/agent-view)：研究预览。运行 `claude agents` 派发持续在后台运行的会话，并在一块屏幕上监视它们
- [Agent teams](https://code.claude.com/docs/en/agent-teams)：实验性功能，默认关闭。多会话的自动化协作，带共享任务、消息机制和团队负责人

除了把工作并行化，多会话还支持以质量为中心的工作流。新鲜的上下文能改进代码审查——Claude 不会偏袒自己刚写的代码。

例如，使用写作者/审查者（Writer/Reviewer）模式：

| 会话 A（写作者） | 会话 B（审查者） |
| --- | --- |
| `Implement a rate limiter for our API endpoints` |  |
|  | `Review the rate limiter implementation in @src/middleware/rateLimiter.ts. Look for edge cases, race conditions, and consistency with our existing middleware patterns.` |
| `Here's the review feedback: [Session B output]. Address these issues.` |  |

测试也可以如法炮制：让一个 Claude 写测试，另一个写代码让测试通过。

### 跨文件扇出

循环遍历任务，对每个任务调用 `claude -p`。批处理时用 `--allowedTools` 收紧权限范围。

对于大型迁移或分析，你可以把工作分给许多并行的 Claude 调用。在 git 仓库中，运行 [`/batch <instruction>`](https://code.claude.com/docs/en/commands#all-commands) 让 Claude 把改动拆给 5 到 30 个子智能体。每个子智能体在自己的 worktree 中工作并开一个 pull request。想用自己的脚本驱动扇出，就循环调用 `claude -p`：

**1. 生成任务列表**

让 Claude 把需要迁移的文件清单写到一个文件里，供下一步的循环读取，提示类似 `list all 2,000 Python files that need migrating and save the list to files.txt`。

**2. 写一个遍历清单的脚本**

```
for file in $(cat files.txt); do
  claude -p "Migrate $file from Python 2 to Python 3. Return OK or FAIL." \
    --allowedTools "Edit,Bash(git commit *)"
done
```

**3. 先在几个文件上测试，再全量运行**

根据前 2-3 个文件上出的问题打磨提示，然后跑全量。`--allowedTools` 标志限制 Claude 能做什么——无人值守运行时这一点很重要。

你还可以把 Claude 接入现有的数据/处理流水线：

```
claude -p "<your prompt>" --output-format json | your_command
```

开发期用 `--verbose` 调试，生产环境关掉。

### 用自动模式自主运行

要无人打断地执行、又有后台安全检查兜底，用[自动模式](https://code.claude.com/docs/en/permission-modes#eliminate-prompts-with-auto-mode)。分类器模型在命令运行前审查，拦截权限范围升级、未知基础设施和受敌意内容驱动的操作，同时让例行工作无需提示直接进行。

```
claude --permission-mode auto -p "fix all lint errors"
```

在带 `-p` 标志的非交互运行中，当分类器反复拦截动作时，Claude Code 不会停止运行。会发生什么、阈值是多少，参见[自动模式何时回退](https://code.claude.com/docs/en/permission-modes#when-auto-mode-falls-back)。

### 加入对抗式审查环节

在把任务标记为完成之前，让一个子智能体在全新上下文中审查 diff 并报告缺口。

Claude 无人值守工作得越久，在你把工作算作完成之前，一次独立检查就越重要。在全新[子智能体](https://code.claude.com/docs/en/sub-agents)上下文中运行的审查者只能看到 diff 和你给它的标准，看不到产生改动的推理过程，因此它会按自己的判断评估结果。

要做正确性检查，运行内置的 [`/code-review` 技能](https://code.claude.com/docs/en/commands)：它在全新子智能体中审查当前 diff 的 bug，并把发现返回给会话。要对照你的计划检查 diff，就自己写审查提示。写清三件事：要检查的工作、用于对照的计划、什么算一个发现：

```
Use a subagent to review the rate limiter diff against PLAN.md. Check that
every requirement is implemented, the listed edge cases have tests, and
nothing outside the task's scope changed. Report gaps, not style preferences.
```

由于审查者以子智能体身份运行，实现会话直接收到缺口清单，可以修复并重新审查，无需你在窗口之间复制发现。

被要求「找缺口」的审查者通常总会报出一些——即使工作本身没问题，因为这就是它被要求做的。追逐每一条发现会导致过度工程：多余的抽象层、防御性代码、为不可能发生的情况写的测试。告诉审查者只标记影响正确性或既定需求的缺口，其余视为可选。

---

## 避免常见的失败模式

这些都是常见错误，及早识别能省时间：

- **大杂烩会话。** 你从一个任务开始，中途问了 Claude 一个不相干的问题，又回到第一个任务。上下文塞满无关信息。
  > **对策**：不相关的任务之间 `/clear`。
- **反复纠正。** Claude 做错了，你纠正，它还是错，你再纠正。上下文被失败的尝试污染。
  > **对策**：两次纠正失败后，`/clear`，把你学到的写进一份更好的初始提示。
- **过度指定的 CLAUDE.md。** CLAUDE.md 太长，Claude 忽略其中一半，因为重要规则淹没在噪声里。
  > **对策**：无情修剪。Claude 不用这条指令也做得对的，删掉，或改成钩子。
- **先信任后验证的落差。** Claude 产出一个看起来靠谱、却不处理边界情况的实现。
  > **对策**：始终提供验证手段（测试、脚本、截图）。无法验证的东西，不要上线。
- **无限探索。** 你让 Claude 不加范围地去「调查」某事。它读了几百个文件，把上下文填满。
  > **对策**：把调查范围收窄，或改用子智能体，别让探索吃掉你的主上下文。

---

## 培养你的直觉

本指南中的模式并非金科玉律。它们是普遍有效的起点，但未必在每种情况下都最优。

有时你*应该*让上下文累积——因为你正深陷一个复杂问题，历史记录很宝贵。有时你应该跳过规划让 Claude 自己琢磨——因为任务是探索性的。有时模糊的提示恰恰是对的——因为你想在施加约束之前，先看看 Claude 如何理解这个问题。

留意什么有效。当 Claude 产出很棒的输出时，注意你做了什么：提示结构、你提供的上下文、你所在的模式。当 Claude 表现挣扎时，问个为什么：上下文太嘈杂？提示太模糊？任务太大一轮做不完？

假以时日，你会养成任何指南都无法传授的直觉：何时该具体、何时该开放，何时该规划、何时该探索，何时该清空上下文、何时该任其累积。

## 相关资源

- [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)：智能体循环、工具与上下文管理
- [Extend Claude Code](https://code.claude.com/docs/en/features-overview)：技能、钩子、MCP、子智能体与插件
- [Common workflows](https://code.claude.com/docs/en/common-workflows)：调试、测试、PR 等的分步配方
- [CLAUDE.md](https://code.claude.com/docs/en/memory)：存放项目约定与持久上下文
