---
title: "驾驭 Claude Code：何时使用 CLAUDE.md、skills、hooks 和子智能体"
title_en: "Steering Claude Code: when to use CLAUDE.md, skills, hooks, and subagents"
source: https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more/
crawled: 2026-09-14
translated: 2026-09-14
---

# 驾驭 Claude Code：何时使用 CLAUDE.md、skills、hooks 和子智能体

> 原文：[Steering Claude Code: when to use CLAUDE.md, skills, hooks, and subagents](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more/) · Claude 博客

Claude 的设计初衷就是以你的方式工作，而在 Claude Code 中你可以对它进行自定义。

指导 Claude 行为的方法有七种：CLAUDE.md 文件、rules（规则）、[**skills**](https://code.claude.com/docs/en/skills)、[**子智能体（subagents）**](https://code.claude.com/docs/en/sub-agents)、[**hooks**](https://code.claude.com/docs/en/hooks-guide)、output styles（输出样式），以及追加系统提示。

每种方法决定：

- 指令何时加载进上下文；
- 它能否在长会话中持续存在（压缩行为）；以及
- 它具有多大的约束力。

下表简要概括了各方法之间的关键差异，正文则提供更多细节和决策框架，帮助你判断每条 Claude 指令应该放在哪里。

| 方法 | 何时加载 | 压缩行为 | 上下文成本 | 何时使用 |
|---|---|---|---|---|
| CLAUDE.md（根目录） | 会话开始时；整个会话期间驻留上下文 | 已记忆化（memoized）：读取一次并在会话中缓存；压缩后缓存清空并重新读取 | 高。无论是否相关，每一行都消耗 token | 构建命令、目录布局、单体仓库结构、编码约定、团队规范 |
| CLAUDE.md（子目录） | 按需加载，当 Claude 读取该子目录下的文件时 | 在再次触及该子目录之前会丢失 | 低。只在处理相关子目录时占用上下文 | 特定子目录的约定 |
| Rules | 会话开始时（用户级 rules），或仅在触及匹配文件时（路径限定的） | 压缩时重新注入 | 中。除非路径限定，否则始终在线 | 具体约束或约定（如所有 API handler 必须用 Zod 验证输入） |
| Skills | 会话开始时加载名称和描述；调用 skill 时加载完整内容 | 已调用的 skills 在共享预算内重新注入；最旧的先被丢弃 | 低。仅在调用时加载完整内容；受所有已调用 skills 共享的 token 预算约束 | 流程性工作流（部署或发布清单） |
| 子智能体 | 会话开始时加载名称、描述和工具列表；仅当通过 Agent 工具调用时加载正文 | 只有最终消息（摘要加元数据）返回主会话 | 低。调用前在主上下文中零成本；在自己的隔离上下文窗口中运行 | 并行运行工作，或运行应当隔离执行、只返回摘要的支线任务（深度搜索、日志分析、依赖审计） |
| Hooks | 在生命周期事件上触发 | 完全绕过压缩 | 低。配置位于主上下文之外；部分输出可能返回（如阻断错误） | 确定性自动化：运行 linter、完成时发布到 Slack、阻断命令、在 PreCompact 时备份聊天历史 |
| Output styles | 会话开始时；注入系统提示 | 永不压缩 | 高。占用上下文窗口，但会覆盖默认系统提示 | 重大的角色改变（从代码助手变为通用助手） |
| 追加系统提示 | 会话开始时；作为 CLI 标志传入 | 永不压缩；仅对当次调用生效 | 中等。会话内首次请求后被缓存 | 语气、回复长度、格式偏好 |

## 七种传递指令的方法

自定义 Claude Code 行为的方式有七种：CLAUDE.md 文件提供始终在线的项目上下文，rules 提供硬性约束，skills 提供可复用的流程，子智能体承担委派的工作，hooks 提供确定性自动化，output styles 或系统提示追加则用于全局性改变。

每种方法都在上下文成本与约束力之间做权衡。这些方法影响 Claude 的行为，而另外两个独立的旋钮——[你选择哪个模型和努力等级（effort level）](https://claude.com/blog/claude-model-and-effort-level-in-claude-code)——则决定它能力多强、干活多卖力。

### CLAUDE.md 文件

CLAUDE.md 是位于项目根目录的 markdown 文件。它在会话开始时加载进上下文，并在整个会话期间驻留。

构建命令、目录布局、单体仓库结构、编码约定和团队规范，天然适合放在这里。

它有两种类型，加载方式不同：

- **始终加载**：第一种是根目录的 CLAUDE.md 文件，可以放在共享仓库中，和/或保存在本地，用于你针对某个项目的个人偏好。这些文件都在会话开始时加载，不会在长会话中丢失或衰减。当 Claude Code 压缩对话时，会重新读取这些文件。
- **按需加载：**位于初始化会话的文件夹之下各子目录中的 CLAUDE.md 文件。例如，`app/api/CLAUDE.md` 会在 Claude 读取 `app/api` 下的文件时加载，而不是在会话开始时。它与路径限定的 rules 共享相同的压缩行为：在再次触及该子目录之前会丢失。

当前工作目录（cwd）之下所有子目录的 CLAUDE.md 文件，都会在 Claude 读取该目录内的文件时加载。

在共享仓库中，CLAUDE.md 会像任何无人负责的配置文件一样增长：每个团队都往里追加自己的指令，什么也不会被删除。规模一大，成本便层层累积。

仓库里的每一位工程师，其每个会话都会加载文件中的每一行，无论是否与他们的任务相关。这既消耗 token，也稀释了对真正重要指令的遵从度。文件变大后，应把团队专属的约定移入路径限定的 rules，把流程移入 skills——它们只在相关时加载。

**提示：**让 CLAUDE.md 保持在 200 行以内，为它指定一位负责人，并像审查代码一样审查对它的更改。内容本身应遵循与任何提示相同的原则：[写出有效的提示](https://claude.com/blog/best-practices-for-prompt-engineering)意味着表达明确、解释约束背后的原因，并给出示例。

不妨把这个文件看作给 Claude 的一份代码库概览，或是一份索引，指向 Claude 可按需查阅更多信息的其他文件。

在单体仓库中，给每个团队的目录配置各自的子目录 CLAUDE.md，让团队只加载自己的约定；开发者还可以使用 claudeMdExcludes 设置，跳过那些他们从不接触的团队的文件。

对于必须适用于组织内每个仓库的标准——安全策略、合规要求——可以通过 MDM 或配置管理把集中管理的 CLAUDE.md 部署到开发者机器上，而且它无法被个人设置排除。

关于设置 CLAUDE.md 的更多内容，请参阅我们的博客文章：[CLAUDE.md 文件：为你的代码库定制 Claude Code](https://claude.com/blog/using-claude-md-files)。

### Rules（规则）

[**Rules**](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/) 是 `.claude/rules/` 中的 markdown 文件，为 Claude 提供具体的约束或约定。

未限定范围的 rules 行为与 CLAUDE.md 相同：在会话开始时始终加载，并在压缩时重新注入。这可能在上下文与当前任务无关时也加载它，浪费 token。

路径限定的 rules 允许你通过添加 `paths` 字段控制加载时机，只在相关时加载规则指令。

例如：一条限定于 `src/api/**` 的规则，在纯文档会话中不会进入上下文；只有当 Claude 读取 `src/api/` 目录内的文件时才会加载。

具体写法如下：

```
---
paths:
  - "src/api/**"
  - "**/*.handler.ts"
---
All API handlers must validate input with Zod before processing.
```

**提示：**针对特定文件的约束，比如"迁移文件只能追加"，最适合作为放在 `paths:` frontmatter 中的 **rule**。当指令涉及横切关注点，或涉及出现在代码库多个（但非全部）角落的文件时，优先选择路径限定的 rule，而不是嵌套的 CLAUDE.md 文件。

### Skills（技能）

[**Skills**](https://code.claude.com/docs/en/skills) 位于 `.claude/skills/`，是由指令、脚本和资源构成的文件夹，由 Claude 动态加载。每个 skill 都有一个 `SKILL.md` 文件，包含名称、描述和正文。

会话开始时只加载名称和描述；当 Claude 调用 skill 时——通过斜杠命令（/code-review）或自动匹配任务——才加载完整正文。

Skills 通过你的系统提示触发。

例如，`/code-review` 是一个内置 skill，它会审查你当前的 diff 并报告发现，不修改文件。该 skill 定义了行动手册，因此每次调用时 Claude 都遵循同样的结构化方法。

压缩时，Claude Code 会在所有已调用 skills 共享的总预算内重新注入它们。如果一次会话中调用了很多 skills，最旧的会先被丢弃。

**提示：**流程性的指令——比如部署工作流、发布清单或审查流程——应该放在 skill 里，而不是 CLAUDE.md 里。

Claude Code 自带一些 skills，你也可以编写自己的自定义 skills。我们的[Claude skills 构建完全指南](https://claude.com/blog/complete-guide-to-building-skills-for-claude)会教你如何做。

### 子智能体（Subagents）

[**子智能体（Subagents）**](https://code.claude.com/docs/en/sub-agents)是 `.claude/agents/` 中的 markdown 文件，为特定支线任务定义相互隔离的助手。每个文件使用 YAML frontmatter（name、description，以及 model 和工具访问权限的可选字段），后接的正文会成为该子智能体的系统提示。

子智能体与 skills 的相似之处在于名称、描述和工具列表在会话开始时加载，但正文中的较大上下文不会被自动调用。Claude 通过 Agent 工具调用它们，并传入一段提示字符串。

Claude Code 的上下文窗口保存着 Claude 关于你会话所知的一切。[这里的交互式时间线](https://code.claude.com/docs/en/context-window)逐步演示了什么在何时加载。

子智能体正文中的大量指令性上下文不仅不会被自动调用，而且根本不会进入父对话。

子智能体随后在自己全新的上下文窗口中运行，返回主会话的只有子智能体的最终消息（通常是许多子任务聚合后的结果）加上元数据。

这种模式可以扩展：子智能体最多可嵌套五层，[动态工作流](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code)可以编排数十到数百个后台智能体，而无需你指定子智能体架构的每个细节。编排计划和中间结果保存在脚本变量中，而不是 Claude 的上下文窗口里，从而在不损失指令保真度的情况下实现规模化。

**提示：**这种隔离正是选择子智能体而非 skill 的主要原因之一。当深度搜索、一轮日志分析或依赖审计这类支线任务，会用你不会再引用的中间结果弄乱主对话时，用子智能体；当你希望流程在主线程中展开、以便观察和引导每一步时，用 skill。

### Hooks

[**Hooks**](https://code.claude.com/docs/en/hooks-guide) 是用户定义的命令、HTTP 端点或 LLM 提示，通过在 [Claude 生命周期中的特定事件](https://code.claude.com/docs/en/hooks#hook-lifecycle)（如文件编辑、工具调用或会话开始）上触发，为 Claude 的行为提供更确定性的控制。

这是一张图，展示了 Claude Code 会话中 hook 可以触发的事件分布。

你在 `settings.json`、托管策略设置或 skill/agent 的 frontmatter 中注册 hooks。

hooks 有几种类型：command、HTTP、mcp_tool、prompt 和 agent。所有 hooks 都是被确定性触发的。前三种是确定性执行的；后两种（prompt 和 agent）则依靠 Claude 的判断而非一组规则来决定输出。

hooks 的上下文成本很低，因为配置或指令位于主上下文窗口之外。执行框架（harness）会根据 hook 类型运行处理器（command、http、mcp_tool），或使用独立窗口进行模型调用（prompt、agent）。

某些 hooks 的输出可能会保存到主上下文窗口。例如，阻断型 hook 的标准错误会保存在上下文中，让 Claude 知道调用为何被拒绝。

但除非配置显式返回输出，大多数 hooks 的输出不会保存到主窗口。如果你在压缩前使用 `PreCompact` 事件把聊天历史备份到另一个文件以备后查，Claude 并不知道聊天历史保存在哪个文件里。

这使得这些 hook 类型与 CLAUDE.md、rules 和 skills 有了本质区别。更多信息请参阅我们的文章[**如何配置 hooks**](https://claude.com/blog/how-to-configure-hooks)。

**提示：**任何应当确定性发生的事情都可以用 hooks：编辑后运行 linter、完成时发布到 Slack，或在特定命令执行前阻断它。`PreToolUse` hook 可以检查任何工具调用，并以退出码 2 拒绝它。

它们的上下文成本很低，因为它们是执行框架运行的代码，而不是会加载进上下文的给 Claude 的指令。Skills 和 hooks 也是[设计 agent loops](https://claude.com/blog/getting-started-with-loops) 的构建模块——那些反复运行、直到满足停止条件为止的工作流。

### Output styles（输出样式）

[**Output styles**](https://code.claude.com/docs/en/output-styles) 是 `.claude/output-styles/` 中的文件，会把指令注入系统提示。它们永不被压缩，每次会话开始时加载，并在会话内首次请求后缓存，这意味着它们有中等的上下文成本。

因为位于系统提示中，output styles 在我们目前介绍的所有方法中指令遵从权重最高，应当审慎使用。

**更改 output style 将替换默认的 output style**（除非你在该 style 的 frontmatter 中设置 keep-coding-instructions: true）。

在 Claude Code 中，这会移除那些告诉 Claude 自己正在协助用户完成软件工程任务的指令，其中还包含其他关键的默认指令，比如：

- 如何界定变更范围；
- 何时添加或省略代码注释；
- 如何处理安全问题；以及
- 验证习惯，比如在宣告工作完成之前先运行测试。

默认情况下，自定义 output style 会丢弃所有这些内容，Claude Code 也随之更像一个通用助手，而不是软件工程助手。

**提示：**编写自定义 output style 之前，先看看内置样式。**Proactive**、**Explanatory** 和 **Learning** 覆盖了最常见的需求（自主性、教学模式、协作编码），无需你维护样式文件。

### 追加系统提示

修改 output styles 的替代方案是 `append-system-prompt` 标志。修改 output style 文件可能给 Claude 的行为带来巨大的意外变化，而追加标志只对原始系统提示做加法。它不改变 Claude 的角色，只是在其默认角色上添加指令。

它也是在调用时传入的，只对当次调用生效，而不是作为文件在多个会话间持久保存。

与其他传递指令的方法相比，追加系统提示可能有更高的上下文成本。它会增加输入 token，不过提示缓存（prompt caching）可以在会话内首次请求之后降低这部分成本。指示 Claude 采用更啰嗦或更长的风格也会增加输出 token。

**提示：**追加系统提示最适合用来添加具体的编码标准、输出格式或领域知识。请记住，追加系统提示的遵从效果存在边际递减。通常，你用这种方式提供的指令越多，Claude 对它们的遵循就越宽松，尤其当指令之间存在矛盾时。

## 何时使用哪种方法

如果你发现自己正在做以下事情之一，也许应该考虑为指令换个位置：

**在 CLAUDE.md 里写"每当 X，就一定做 Y"。** 如果某个行为应当可靠地发生，比如每次编辑后运行 prettier、完成时发布到 Slack，请改用 `settings.json` 里的 hook。模型选择运行格式化工具，与格式化工具自动运行，是两回事。

**在 CLAUDE.md 里写"绝不这样做"。** 当有的事情绝对不能发生时，指令是错误的工具。Claude 大多数时候会遵循指令，但在压力之下、在长会话或模糊情境中，或者由于任务中访问的文件里存在提示注入（prompt injection），模型可能无法遵循提示中的规则。真正的防护栏必须是确定性的，而执行手段是 [hooks](https://code.claude.com/docs/en/hooks) 和[权限（permissions）](https://code.claude.com/docs/en/permissions)。`PreToolUse` hook 可以检查调用并以退出码 2 阻断它。[**托管设置（Managed settings）**](https://code.claude.com/docs/en/settings#managed-settings)更进一步：它们由管理员部署，不能被用户的本地配置覆盖，是实施确定性、全组织范围防护栏的唯一途径。

**在 CLAUDE.md 里写 30 行的流程。** 流程属于 skills。CLAUDE.md 用于 Claude 应当时刻掌握的事实：构建命令、单体仓库布局、团队约定。部署手册或安全审查清单应该放在 `.claude/skills/` 里，正文只在被调用时加载。

**不加 paths 的 API 专属规则。** 如果一条规则只适用于 `src/api/**`，用 `paths:` 限定范围就能让它在无关工作中不进入上下文。未限定范围的规则在机制上等同于把内容放进 CLAUDE.md：始终加载，始终消耗 token。

**把个人偏好写进项目级 CLAUDE.md 文件。** 所有基于文件的方法都有对应的用户级版本，无论你在哪个仓库，每个 Claude Code 会话都会加载它。个人偏好请使用本地文件（比如始终使用语义化提交信息）。项目级文件留给那些全团队适用、但特定于某个代码库的偏好。

## 开始自定义 Claude Code

关于充分发挥 Claude Code 效能的更多技巧和模式——从配置环境到跨并行会话扩展——请参阅我们的 [Claude Code 最佳实践](https://code.claude.com/docs/en/best-practices#write-an-effective-claude-md)文档。

当其中几项配置运转起来后，你可以把它们中的许多（skills、子智能体、hooks、output styles）打包成一个[插件（plugin）](https://code.claude.com/docs/en/plugins)，在队友或项目之间共享一套连贯的配置。

*本文由 Anthropic 员工 Michael Segner 撰写。*

FAQ（常见问题）
