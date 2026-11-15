---
title: "第 2 讲：从用户视角看智能体 I——Claude Code 如何工作"
title_en: "Agent From a User's Perspective I: How Claude Code Works"
source: https://cs2680.seas.harvard.edu/slides/2_agent_use_1.pdf
pages: 53
crawled: 2026-11-16
translated: 2026-11-16
---

# 第 2 讲：从用户视角看智能体 I——Claude Code 如何工作

> PDF 讲义文本抽取：[2_agent_use_1.pdf](https://cs2680.seas.harvard.edu/slides/2_agent_use_1.pdf) · Harvard CS2680

## 第 1 页

**现代 AI 系统：智能体与系统优化**

Juncheng Yang

从用户视角看智能体 I：Claude Code 如何工作

## 第 2 页

**日程更新**

LLM 基础后移

- 暂时把 LLM 当作一个魔法推理盒
- 学习智能体并不需要了解其内部

更多智能体，更少 GPU

- 你们大多数人对智能体更感兴趣
- 增加两节智能体设计课
- 减少 GPU 课程——与其他课程重叠更少

日程变化

- 不再有强制论文展示
- 分数计入参与和项目
- 作业 1 分享改为加分项
- 少量加分论文讨论——待定

## 第 3 页

**还有一些事务**

举手 = 得分

OPTIONAL——额外阅读，非必需

ADVANCED——略读，或自行深入阅读

新助教：Advaith Ravishankar

参与分：课堂提问 / 回答问题

每节课最多 1 分，课后找助教登记

额外阅读：可选

## 第 4 页

**今日安排**

- Claude Code 如何工作
- Claude Code：从无状态 LLM 到智能体
- 记忆
- 工具、skills、hooks、plugins

## 第 5 页

**当你在 Claude Code 中输入一条 prompt，会发生什么？**

举手 = 得分

## 第 6 页

**智能体循环**

1. 收集上下文
   - prompt、文件、工具结果
2. 生成动作
   - 运行工具：bash、read、edit
3. 运行工具
   - 测试、输出、重新读取状态

重复——每一步都以上一步返回的结果为条件。

一条用户 prompt = 多次模型调用和多次工具执行，而不是单个请求。

框架（harness）　模型　你的机器

## 第 7 页

**在你输入之前，上下文已经存在**

在你敲下第一个键之前，上下文大小已经达到 10k+ tokens。

- SYSTEM　Claude Code 指令
- PROJECT　环境
- MEMORY　持久化的项目 / 用户笔记 / CLAUDE.md
- TOOLS　Read、Edit、Bash、Glob、Grep、Web、Agent
- SKILLS / MCP　名称与描述
- USER　“修复失败的 auth 测试”

Skill 与 MCP 条目一开始只有名称——只有当 Claude 真正用到它们时，完整文本才会加载。

## 第 8 页

**它不会把你的代码库发出去**

代码库留在磁盘上。Claude 按需拉取其中的片段。

- 你的代码库：数千个文件，存放在磁盘上
- Claude：“我需要什么？”
- Grep("authentication")
- 返回少量几行
- 这个片段进入上下文

## 第 9 页

**模型提出，框架执行**

模型提出一个动作，框架执行它。

- Claude 模型：发出请求 `Bash("pytest")`
- Claude Code 框架：解析请求、检查权限、执行
- 你的机器：pytest 实际运行 → stdout / stderr
- `tool_result` 回到模型的上下文中

## 第 10 页

**一条用户 prompt 触发多次 LLM 推理**

一个用户轮次展开为推理与工具执行交替的链条。

U（prompt）→ M₁（推理）→ T₁（工具）→ M₂（推理）→ T₂（工具）→ Mₙ（推理）→ A（回答）

实践中看起来是这样：

pytest → 读取 session.py → grep create_session → 编辑 session.py → pytest 全部通过

每个请求都以上一次推理和上一次工具结果为条件。

## 第 11 页

**权限层位于意图与执行之间**

工具请求是一个提案，需要你或另一个模型批准。

Claude 请求：`Bash("rm -rf build/")`

权限层：

- Manual（手动）
- Accept Edits（接受编辑）
- Bypass permission（绕过权限）
- Auto（由一个小模型检查）

结果：

- allowed——命令运行
- ask——先由你确认
- denied——什么也不发生

## 第 12 页

**上下文增长——然后被压缩**

每一步都会增加 token：模型回复、文件内容、命令输出。

请求 1 → 请求 2 → 请求 3 → 请求 N → 请求 N+1

COMPACTION（压缩）：总结旧轨迹，重新注入 CLAUDE.md 与记忆

上下文管理是智能体框架设计的重要组成部分（下周讨论）。

典型上下文大小：1M tokens（Sonnet / Opus / Fable、GPT 5.6）；今年早些时候 256K 还很常见

上下文不是免费的：前缀缓存读取占成本的大部分。

## 第 13 页

**小结：智能体循环**

Prompt + 上下文 → 模型提出 → 框架执行 → 结果折入上下文

循环重复，直到任务完成。

## 第 14 页

**工具与记忆赋予智能体能力**

记忆　LLM　推理与规划　智能体　工具 / 动作　观察　环境

## 第 15 页

**智能体记忆**

LLM（无状态）　工具（行动）　状态（上下文 + 记忆）

## 第 16 页

**上下文是记忆的一种**

- 智能体在两次运行之间是无状态的——每个会话都从零开始
- 在实践中，“记忆”只是会话启动时加载的文件

每一次创建记忆，都是在决定什么内容会被永远重新读取。

**上下文：工作记忆**

模型现在能看到的内容——它会随会话结束而消失。

**持久记忆**

会话结束后仍保留、下次重新加载的内容。

## 第 17 页

**为什么智能体需要记忆**

记忆是指令变成惯例的方式。

- 重复指令
  - 每个会话都要重新解释同样的设置
- 丢失的决策 / 假设
  - 窗口压缩后，“为什么”消失了
- 重复发现
  - 智能体重新读取同样的文件来重新了解布局
- 行为不一致
  - 不同会话做出不同选择

## 第 18 页

**两套系统把知识传递下去**

两者都在每个会话开始时加载到上下文中。

| | CLAUDE.md 文件 | 自动记忆 |
| --- | --- | --- |
| 谁来写 | 你 | Claude |
| 内容 | 指令与规则 | 经验与模式 |
| 范围 | 项目、用户或组织 | 每个代码库，跨 worktree 共享 |
| 加载时机 | 每个会话 | 每个会话（前 200 行 / 25KB） |
| 用途 | 标准、工作流、架构 | 你的偏好、纠正、项目上下文 |

## 第 19 页

**两套系统把知识传递下去**

两者都在每个会话开始时加载到上下文中。

| | CLAUDE.md 文件 | 自动记忆 |
| --- | --- | --- |
| 谁来写 | 你 | Claude |
| 内容 | 指令与规则 | 经验与模式 |
| 范围 | 项目、用户或组织 | 每个代码库，跨 worktree 共享 |
| 加载时机 | 每个会话 | 每个会话（前 200 行 / 25KB） |
| 用途 | 标准、工作流、架构 | 你的偏好、纠正、项目上下文 |

## 第 20 页

**CLAUDE.md 放在哪里**

文件按作用域从宽到窄加载；最近的文件最后读取。

1. 管理策略
   - `…/ClaudeCode/CLAUDE.md` · 组织级，不能排除
2. 用户指令
   - `~/.claude/CLAUDE.md` · 你的偏好，适用于所有项目
3. 项目指令
   - `./CLAUDE.md` 或 `./.claude/CLAUDE.md` · 通过源码管理在团队间共享
4. 本地指令
   - `./CLAUDE.local.md` · 个人使用，被 gitignore

## 第 21 页

**CLAUDE.md 里该放什么**

上下文是租来的，记忆是拥有的——审慎选择你拥有什么。

- 大小：每个文件 200 行以内
- 结构：Markdown 标题与要点
- 具体性：具体规则，而非含糊规则
- 一致性：没有矛盾或过时的规则

**该放**

- 命令：如何运行测试、构建、linter
- 硬约束：绝不提交到 main，绝不编辑生成文件
- 智能体无法低成本推断的事实：布局、归属、坑

**不该放**

- 模型已经知道的关于语言或框架的任何内容
- linter 或 formatter 已经强制执行的风格偏好
- 长篇散文、变更日志，以及任何机密

## 第 22 页

**太长了？拆到 `.claude/rules/` 里**

一个文件一个主题——每条规则只在相关时加载。

- 一个文件一个主题
  - 每个规则文件只覆盖一个关注点，从而保持简短具体
- 添加 `paths:` frontmatter
  - 只有当 Claude 触碰到匹配文件时才加载（没有 `paths:` 则每个会话都加载）

示例：

```
.claude/rules/
├── testing.md
├── api-style.md
└── db-migrations.md
```

**经验**

- 作用域化的规则让上下文窗口保持小
- 只有与当前工作匹配的规则才会被加载
- CLAUDE.md 保持简短；细节放在 rules 里

## 第 23 页

**自动记忆：Claude 自己的笔记**

- user：你的角色、专业知识和协作偏好
- feedback：你给出的纠正、你确认的方法
- project：正在进行的工作、代码之外的决策
- reference：存在于项目之外的信息

```
~/.claude/projects/<project>/memory/
├── MEMORY.md
├── user_role.md
├── feedback_testing.md
└── other-topic-files.md
```

**行为方式**

- 每个文件都有一个 type 字段标记
- MEMORY.md 是索引——每个会话加载前 200 行（25KB）
- 机器本地；worktree 共享该目录
- 默认开启；用 `/memory` 关闭

## 第 24 页

**检索使用索引**

索引始终加载；主题文件只在相关时才读取。

1. 会话开始
2. 加载 MEMORY.md 索引
3. 识别相关主题
4. 按需读取主题文件
5. 将记忆应用于任务

Memory.md

索引让上下文窗口保持小——只读取任务需要的主题文件。

## 第 25 页

**检查与控制记忆**

四条命令，用来查看——并引导——Claude 记住什么。

- `/memory`——浏览、编辑、删除或禁用记忆
- `/context`——查看加载了哪些指令文件
- `/init`——生成一个 CLAUDE.md 起始文件
- `/doctor`——识别可能不该放进 CLAUDE.md 的内容

## 第 26 页

**记忆的代价**

- 每个永久 token 都是租金——在每个会话开始时支付
- 记忆与任务竞争同一个窗口
- 过时的记忆比没有更糟：它会主动误导
- 像对待代码一样对待记忆——审查、修剪、纳入版本控制

上下文大小有限 + 你发送给 Anthropic 的每个 token 都要付费。

## 第 27 页

**工具与记忆赋予智能体能力**

记忆　LLM　推理与规划　智能体　工具 / 动作　观察　环境

## 第 28 页

**成为可行动的智能体：核心工具**

- Read
  - 打开文件、检查状态——最常用的工具
- Search
  - grep 与 glob——无需读完所有内容就能找到
- Fetch
  - 拉取页面或文档——把不受信任的文本带进来
- Edit / Write
  - 修改文件——第一个会产生后果的工具
- Shell
  - 构建、测试、git——除非沙箱化，否则是整个机器
- Delegate
  - 派生一个子智能体——一个返回摘要的工具

模型会决定使用哪些工具，你不需要做太多。

你将在作业 2 中自己构建这些工具。

## 第 29 页

**扩展智能体：Skills、MCP、Hooks 与 Plugins**

## 第 30 页

**扩展智能体**

四种机制，解决四类不同问题——它们不可互换。

- **Skill**：智能体应该如何执行任务
- **MCP**：它可以访问哪些外部数据和动作
- **Hook**：在生命周期事件上自动发生什么
- **Plugin**：这些扩展如何打包和分发

四层：skill 决定怎么做，MCP 负责触达外部，hook 负责强制执行，plugin 负责分发。

## 第 31 页

**智能体循环中的扩展点**

每种机制挂载在循环中的不同位置。

- 用户请求
- 模型推理：Skill 提供知识与流程
- 工具选择：MCP 提供外部工具
- 工具执行
- Hook 可以在循环的任何阶段检查、阻断或响应
- Plugin 把 skills、MCP server 和 hooks 打包成一个可安装单元

## 第 32 页

**发布工作流示例**

准备一次发布，验证它，发布到 GitHub，通知团队。

- 遵循发布流程——Skill
- 创建 GitHub release——MCP
- 测试失败时阻止发布——Hook
- 共享完整配置——Plugin

## 第 33 页

**Skill 作为可复用流程**

当任务需要时，智能体加载的知识与流程。

一个 skill 承载：

- 领域知识
- 参考资料
- 可重复的工作流
- 模型与用户均可调用
- 运行时进行推理

把它理解为上下文工程。

示例：`/release 2.4.0`

## 第 34 页

**Skill 的结构**

一个文件夹、一段控制发现的描述，以及承载流程的正文。

```
.claude/skills/release/
├── SKILL.md
├── references/
└── scripts/
```

```
name: release
description: Prepare a release
```

**如何工作**

- description 控制发现
- 正文承载流程
- 辅助文件添加参考和脚本
- 用户也可以直接运行：`/release`

1. 阅读发布说明 · 2. 确认版本 · 3. 运行测试 · 4. 准备提交 · 5. 发布前询问

## 第 35 页

**Skill 的调用与上下文成本**

两种调用模式——以及两种不同的上下文成本。

- **模型调用**：当 description 与任务匹配时，Claude 加载该 skill
- **用户调用**：用户显式运行 `/<skill-name>`

**成本**

- description 在会话开始时加载；完整正文只在 skill 运行时加载
- 有副作用的工作流通常应要求显式调用
- 清晰、独特的描述可以减少错误的 skill 选择

## 第 36 页

**MCP 作为外部能力层**

Model Context Protocol 通过标准协议把智能体连接到外部服务。

- 读取和更新 GitHub issue
- 查询数据库
- 检索监控数据
- 访问 Figma 设计
- 向 Slack 发消息
- 控制浏览器

MCP 赋予 Claude 既不存在于模型、也不存在于本地文件中的能力。

## 第 37 页

**MCP 工具调用如何工作**

从意图到结构化结果的六个步骤。

1. Claude 识别需要执行的动作
2. MCP client 使用一个工具
3. MCP server 处理连接
4. 外部服务执行操作
5. 结构化结果返回给 Claude
6. Claude 评估结果

**几乎与本地工具相同**

- 相同的名称、描述和类型化 schema
- 相同的调用—返回契约
- 只是运行在另一个进程中

协议承载调用；是否发起调用仍由智能体决定。

## 第 38 页

**Hook 作为生命周期自动化**

一个会话从左到右运行；hook 可以在每个标记事件处触发。

- 会话开始
  - 加载上下文、记录日志
- 用户 prompt
  - 校验或补充
- 工具使用前
  - 检查或阻断
- 工具使用后
  - 格式化、测试、记录
- 停止前
  - 验证测试
- 无 hook
  - 推理本身不是事件

Hook 在事件上触发，可以运行命令、HTTP 请求、MCP 工具、prompt 或子智能体。

## 第 39 页

**Plugin 作为打包层**

一个可安装单元，携带 skills、hooks、agents 和 MCP 配置。

```
plugin/
├── skills/
├── hooks/
├── agents/
├── .mcp.json
├── .lsp.json
└── .claude-plugin/plugin.json
```

**打包带来什么**

- 安装——一条命令
- 版本管理——固定 release
- 命名空间——不会命名冲突
- 团队复用——所有人一套配置
- 分发——通过 marketplace 分享

Plugin 让一套可用的配置变成别人可以安装的东西。

## 第 40 页

**四种机制如何协同**

判断、能力、强制执行——以及把三者一起交付的包。

- Skill：知识与流程
- Claude：推理与工具使用
- MCP：GitHub · Slack · 数据库
- Hook 在生命周期事件触发——每次工具调用前后
- Plugin 把 skill、MCP 配置和 hooks 打包，以便在其他地方安装

## 第 41 页

**.claude/ 内部**

```
.claude/
  CLAUDE.md
  settings.json
  settings.local.json
  commands/
  skills/
  agents/
  hooks/
  plugins/
```

- 记忆：CLAUDE.md、rules/
- 配置：permissions、hooks、env
- 工作流：skills/、commands/
- 委派与护栏：agents/、hooks/

同样的布局也存在于 `~/.claude/`（用户作用域）。项目设置优先于用户设置。

## 第 42 页

**设计练习**

对每条需求进行分类——并说明为什么其他机制不合适。

- 应用公司 API 规范——Skill
- 从 Jira 读取 issue——MCP
- 每次编辑后运行格式化——Hook
- 指导多步部署——Skill
- 发送完成通知——Hook + MCP
- 阻止写入生产环境——Hook 或 policy
- 跨代码库共享所有内容——Plugin

Skill 知识与流程 · MCP 外部访问 · Hook 事件自动化 · Plugin 打包与分发

举手 = 得分

## 第 43 页

**下一节课**

- 从用户视角看智能体 II

## 第 44 页

**可选幻灯片**

## 第 45 页

**MCP：是什么、为什么**

为什么存在 MCP：访问外部工具与服务

- MCP 出现之前：N×M 种实现
- 它避免了为每个 AI 客户端构建独特的集成

一个开放协议（无状态），让 AI 应用发现并使用外部 server 暴露的能力。

https://modelcontextprotocol.io

如果我需要访问外部服务呢？Gmail、GitHub……

## 第 46 页

**MCP 架构**

- Host：Claude Code——你与之对话的应用。
- MCP protocol
- MCP client：每个 server 一个连接，由 host 运行。
- MCP server：把系统的能力暴露为工具。
- External system：GitHub、Slack、PostgreSQL、本地服务。

## 第 47 页

**MCP：三个核心原语**

- **Tools**：Claude 可以调用的动作——`create_issue(…)`
- **Resources**：可读数据——issue、schema——`github://issues/123`
- **Prompts**：server 暴露的可复用 prompt 模板——`triage_issue(…)`

一个 prompt 返回指令：

- 审查 issue #123。
- 判断它是否可复现。
- 将其严重性评估为高。
- 推荐负责人和下一步动作。

Prompts 由用户控制。

应用把它们呈现为命令或菜单项。在 Claude Code 中，呈现为带命名空间的斜杠命令：

`/mcp__github__triage_issue 123 high`

## 第 48 页

**它们如何协同工作**

假设你问：

“对 issue #123 做分诊，如果它是严重的认证 bug 就指派它。”

三个原语可能这样协作：

- Prompt `triage_issue`：提供组织的 triage 流程
- Resource `github://issues/123`：提供 issue 的内容
- Tool `get_related_errors`：检索当前诊断信息

## 第 49 页

**MCP 安全：关键部分**

一个已连接的 server 可以看到你发给它的内容，并用你的凭据行动。

- **最小权限**——把 token 限定到你真正需要的 repo、table 或 channel。
- **读 vs 写**——把读与写分开；让变更操作留在审批之后。
- **不信任工具输出**——绝不要把返回内容当作指令来信任。
- **安装前审查**——第三方 server 可能携带 prompt 注入；要审查它们。

连接前先问：这个 server 能读什么，又能改什么？

## 第 50 页

**什么是 MCP 网关**

AI 客户端与一个或多个 MCP server 之间的控制层。

像 API 网关——但它说 MCP：`tools/list`、`tools/call`、resources、prompts、schemas、协议版本。

一种架构模式，对客户端来说它只是另一个 MCP server。

Claude Code / agent → MCP 网关（auth · policy · logging · routing · rate limits）→ GitHub MCP / Jira MCP / Database MCP

## 第 51 页

**网关做什么**

1. **聚合**：一个连接、一个带命名空间的目录：`github.*`、`jira.*`、`postgres.*`
2. **路由**：把每个调用转发给所属 server；`Mcp-Method` header 让路由无需读取 body。
3. **执行策略**：谁可以连接，哪些工具可见、可调用或需要人工批准。
4. **代理身份**：客户端只认证一次；上游凭据留在网关之后。
5. **观测**：集中审计轨迹：身份、工具、决策、延迟、结果、成本。
6. **扩展**：负载均衡、重试、熔断、目录缓存、配额。

**值得使用当……** 许多用户、智能体、server、凭据或合规规则需要一致治理时。

**但它是一个信任边界**：宽泛凭据、丢失最终用户身份、命名冲突、日志中的密钥、单点故障。

OPTIONAL——额外阅读，非必需

## 第 52 页

**有什么新变化？**

Spec 2026-07-28——MCP 发布以来最大的一次修订

- **无状态核心**：不再持有会话。任何请求都可以落到任何实例，位于普通负载均衡器之后。
- **路由**：`Mcp-Method` header 让网关无需读取 body 即可路由；列表结果可带 TTL 缓存。
- **扩展**：用于长时运行工作的 Tasks 和用于 server 渲染 UI 的 MCP Apps 现在作为扩展发布。

OPTIONAL——额外阅读，非必需

## 第 53 页

（空白页）
