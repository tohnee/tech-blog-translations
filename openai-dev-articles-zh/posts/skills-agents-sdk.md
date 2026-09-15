---
title: "用 skills 加速开源（OSS）维护"
title_en: "Using skills to accelerate OSS maintenance"
source: https://developers.openai.com/blog/skills-agents-sdk/
crawled: 2026-09-14
translated: 2026-09-14
---

# 用 skills 加速开源（OSS）维护

> 原文：[Using skills to accelerate OSS maintenance](https://developers.openai.com/blog/skills-agents-sdk/) · OpenAI 开发者博客

我们使用 Codex 改变了维护 [OpenAI Agents SDK](https://developers.openai.com/api/docs/guides/agents) 各仓库的方式。仓库级 skills、`AGENTS.md` 与 GitHub Actions 让我们把反复出现的工程工作——如验证、发布准备、示例集成测试与 PR 审查——变成可重复的工作流。即便配置相当简单，这也帮助我们在这些活跃仓库中提升了开发吞吐量。2025 年 12 月 1 日至 2026 年 2 月 28 日期间，两个仓库共合并了 457 个 PR，而此前三个月（2025 年 9 月 1 日至 2025 年 11 月 30 日）为 316 个（Python：182 -> 226，TypeScript：134 -> 231）。

简单介绍一下背景：该 SDK 提供 [Python](https://github.com/openai/openai-agents-python) 与 [TypeScript](https://github.com/openai/openai-agents-js) 两个版本。它提供构建智能体应用的核心组件，也是在 [Realtime API](https://developers.openai.com/api/docs/guides/realtime) 之上构建语音智能体的一条简洁路径，支持多智能体、工具与人在回路（human-in-the-loop）控制。它的使用规模相当可观：截至 2026 年 3 月 6 日的近 30 天窗口内，Python 包在 PyPI 上的下载量约为 1470 万次，TypeScript 包在 npm 上的下载量约为 150 万次。

这套配置很简单：

- [`AGENTS.md`](https://agents.md/) 中的仓库策略
- `.agents/skills/` 中的仓库级 skills
- 这些 skills 内可选的脚本与参考资料
- 当同一工作流需要在 CI 中运行时，使用 [Codex GitHub Action](https://developers.openai.com/codex/github-action)

这套配置为 Codex 提供了关于仓库如何运作的稳定上下文，从而提升反复出现的工程工作的速度与准确性。

如果你维护着一个公开的开源项目，请查看 [Codex for OSS](https://developers.openai.com/community/codex-for-oss)。符合条件的维护者可以申请附带 Codex 的 ChatGPT Pro、API 额度，以及有条件的 Codex Security 访问权限。

## 把工作流留在仓库里

在这些仓库中，我们使用 skills 来沉淀仓库专属的工作流。一个 skill 是一小包运维知识：一份 `SKILL.md` 清单，加上可选的 `scripts/`、`references/` 与 `assets/`。[Codex 自定义文档](https://developers.openai.com/codex/customization/overview#skills)解释了为什么这种方式行之有效：skills 非常适合可重复的工作流，因为它们可以承载更丰富的指令、脚本与参考资料，而不会一开始就撑爆智能体的上下文。

这与 skills 所采用的渐进式披露（progressive-disclosure）模型相吻合：

- 它先看到 `name`、`description` 等元数据
- 只在选中某个 skill 时才加载 `SKILL.md`
- 只在需要时才阅读参考资料或运行脚本

两个 SDK 仓库都把这些工作流放在紧邻代码的位置：

- [openai-agents-python 中的 .agents/skills](https://github.com/openai/openai-agents-python/tree/main/.agents/skills)
- [openai-agents-js 中的 .agents/skills](https://github.com/openai/openai-agents-js/tree/main/.agents/skills)

Python 仓库是较简单的基线：

- `code-change-verification`：当代码或构建行为发生变化时，运行必需的格式化、lint、类型检查与测试栈。
- `docs-sync`：对照代码库审计文档，找出缺失、错误或过时的文档。
- `examples-auto-run`：以自动模式运行示例，并配有日志与重跑辅助。
- `final-release-review`：将上一个发布标签与当前发布候选进行比较，并检查发布就绪状态。
- `implementation-strategy`：在编辑运行时或 API 变更之前，确定兼容性边界与实现方案。
- `openai-knowledge`：通过官方 Docs MCP 工作流获取最新的 OpenAI API 与平台文档。
- `pr-draft-summary`：在交接时准备分支名建议、PR 标题与草稿描述。
- `test-coverage-improver`：运行覆盖率分析，找出最大的缺口，并提出高影响力的测试。

JavaScript 仓库遵循相同的大致模式，然后针对其 npm monorepo 与发布流程增加了几个仓库专属的 skills：

- `changeset-validation`：检查 changesets 与版本提升（bump）级别是否确实与包的 diff 相符。
- `integration-tests`：把包发布到本地 Verdaccio registry，并验证在受支持的各种运行时中的安装与运行行为。
- `pnpm-upgrade`：以协调一致的方式更新 pnpm 工具链与 CI 中的版本锁定。

比具体清单更重要的是模式。每个 skill 都有一个狭窄的契约、一个清晰的触发条件和一个具体的输出。

一些最有用的 skills 并不是硬性关卡。`docs-sync` 与 `test-coverage-improver` 是「先出报告」的工作流：它们检查当前的 diff 或覆盖率产物，排定轻重缓急，并在进行编辑之前请求批准。在 Python 仓库中，`docs-sync` 还把源码中的 docstring 与注释当作生成参考文档的唯一事实来源，而不是手工修补生成结果。JavaScript 独有的 `pnpm-upgrade` skill 则是狭窄维护工作流的又一个好例子：它把本地 pnpm 版本、`packageManager` 与工作流版本锁定作为一个整体一起更新，而不是退回到大范围搜索替换。

## 让工作流成为强制要求

当仓库在恰当的时机强制要求使用 skills 时，它们会变得更有用。这正是 `AGENTS.md` 发挥作用的地方。

[AGENTS.md 指南](https://developers.openai.com/codex/agent-configuration/agents-md#layer-project-instructions)把这些文件描述为随代码库一起移动、并在智能体开始工作之前生效的仓库级指令。它还建议保持这些文件精简。在 Agents SDK 仓库中，我们用这个空间存放 Codex 每次都应遵循的规则，并把价值最高的规则放在靠近顶部的位置。

在实践中，两个仓库都使用简短的 if/then 规则来规定强制性的 skill 使用。在编辑运行时或 API 变更之前，先调用 `$implementation-strategy` 来确定兼容性边界与实现方案。如果变更影响 SDK 代码、测试、示例或构建行为，调用 `$code-change-verification`。如果 JavaScript 包变更影响发布元数据，调用 `$changeset-validation`。如果工作涉及 OpenAI API 或平台集成，调用 `$openai-knowledge`。当工作完成、准备交接时，调用 `$pr-draft-summary`。

这一结构也与 [agents.md](https://agents.md/) 的建议一致：把项目概述、构建与测试命令、代码风格、测试指南、安全考量以及其他仓库专属规则放在同一个地方。Agents SDK 仓库遵循这一形态，但把日常工作中最重要的操作性触发条件放在最前面。一个精简版本如下：

```
# AGENTS.md

## Project overview

- Core SDK code lives under `src/agents/` or `packages/*/src/`.
- Tests live under `tests/` or `packages/*/test/`.
- Sample apps and integration surfaces live under `examples/`.

## Mandatory skill usage

- Use `$implementation-strategy` before editing runtime or API changes that may affect compatibility boundaries.
- Run `$code-change-verification` when runtime code, tests, examples, or build/test behavior changes.
- Use `$openai-knowledge` for OpenAI API or platform work.
- Use `$pr-draft-summary` when substantial code work is ready for review.

## Build and test commands

- Python: `make format`, `make lint`, `make typecheck`, `make tests`
- TypeScript: `pnpm i`, `pnpm build`, `pnpm -r build-check`, `pnpm lint`, `pnpm test`

## Compatibility rules

- Preserve positional compatibility for public constructors and dataclass fields.
```

真实的文件会在这个基线之上补充仓库专属细节，例如 JavaScript 仓库中的 `$changeset-validation`，以及两个文件中更详细的运行时、文档与发布指引。如果想看完整示例，请查看 [openai-agents-python 中的 AGENTS.md](https://github.com/openai/openai-agents-python/blob/main/AGENTS.md) 与 [openai-agents-js 中的 AGENTS.md](https://github.com/openai/openai-agents-js/blob/main/AGENTS.md)。

`AGENTS.md` 不只用于 skill 触发器。Python 仓库还在那里记录了一条公开 API 兼容性规则：保持导出的构造函数参数与 dataclass 字段的位置含义不变，尽可能把新的可选参数追加到末尾，如果重排不可避免，则添加兼容性测试。这是另一个好模式：把发布关键型的兼容性规则与 skill 触发器放在同一个地方。

### 验证规则

一个清晰的例子是 `$code-change-verification`。

在两个仓库中，这条规则都不是「总是运行一长串验证栈」。规则是「当运行时代码、测试、示例或构建/测试行为发生变化时运行它，并且在通过之前不得将工作标记为完成」。

条件部分让仅涉及文档的工作保持轻量。强制部分确保 SDK 代码变更经过仓库的标准验证步骤。

实际的验证栈编码在 skills 本身之中。

在 Python 仓库中，它要求：

```
make format
make lint
make typecheck
make tests
```

在 JavaScript 仓库中，该 skill 要求严格遵循以下顺序：

```
pnpm i
pnpm build
pnpm -r build-check
pnpm -r -F "@openai/*" dist:check
pnpm lint
pnpm test
```

这个 skill 编码了仓库对「已验证」的定义，而 `AGENTS.md` 让这一定义变得可强制执行。

### Changeset 校验

JavaScript 仓库对包变更多了一步强制要求：围绕 [Changesets](https://github.com/changesets/changesets) 构建的 `$changeset-validation`。

当 `packages/` 下有任何变化，或 `.changeset/` 发生变化时，模型要做的就不只是运行测试。它必须创建或更新正确的 changeset，校验版本提升级别，并确认 changeset 确实与 diff 相符。

这个 skill 不只是检查某个文件是否存在。它要求 Codex 判断 git diff，并把校验规则保存在一份共享提示词中，使本地运行与 GitHub Actions 使用同一套逻辑。它还编码了仓库专属政策，例如：

- 当分支上已有 changeset 时，使用现有的，而不是再创建一个
- 摘要保持一行，采用 Conventional Commit 风格，以便兼作提交标题
- 在 1.0 之前，常规功能工作避免 major 提升；对明确标注为仅预览（preview-only）的新增内容，如果不改变现有行为，则按 patch 变更对待
- 对照实际的包变更校验所需的版本提升级别

这让 Codex 在宣布工作完成之前，必须对自己创建的发布元数据负责并进行校验。

### 使用最新文档

当工作涉及 OpenAI API 或平台集成时，两个仓库也都要求使用 `$openai-knowledge`。

该 skill 是官方 [OpenAI Docs MCP](https://developers.openai.com/learn/docs-mcp) 的一个薄封装。它不让模型凭记忆回答，而是告诉 Codex 使用 OpenAI Developer Documentation MCP 服务器查阅 Responses API、工具、流式传输、Realtime 与 MCP 等接口面的最新文档。

如果本地 Codex 环境尚未配置 MCP 服务器，该 skill 会指引维护者查看 [Docs MCP 快速开始](https://developers.openai.com/learn/docs-mcp#quickstart)与[官方 MCP 服务器端点](https://developers.openai.com/mcp)。

### 准备 PR 交接

在实质性工作结束时，两个仓库都会使用 `$pr-draft-summary`。

该 skill 只在任务实质上已经完成或准备好接受审查、且变更触及了有意义的代码、测试、示例、有行为影响的文档或构建/测试配置时触发。随后它会自动收集分支名、工作树状态、变更文件、diff 统计与最近提交，并产出：

- 分支名建议
- PR 标题
- PR 草稿描述

输出格式刻意保持严格。一个典型的结果如下：

```
# Pull Request Draft

## Branch name suggestion

git checkout -b fix/tracing-lazy-init-fork-safety

## Title

fix: #2489 lazily initialize tracing globals to avoid import-time fork hazards

## Description

This pull request fixes import-time tracing side effects that could break fork-based process models by moving tracing bootstrap to lazy, first-use initialization.

It updates tracing setup so initialization happens once on first access while preserving the existing public tracing APIs.

It also adds regression tests for import-time behavior, one-time bootstrap, and custom provider handling.

This pull request resolves #2489.
```

一旦你信任模型能够校验并总结它自己的工作，让它产出 PR 草稿便是自然的最后一步。它让交接保持一致，并减少了编码工作完成之后的重复性写作。

## 写出更好的描述

skill 的 `SKILL.md` frontmatter 中的 `description` 字段是路由契约的一部分。

这是结构性的，而不是风格性的。[Agent Skills 规范](https://agentskills.io/specification)把 `name` 与 `description` 定为 `SKILL.md` frontmatter 的必填字段，并且其渐进式披露模型规定，启动时会为所有 skills 加载的正是这些字段。完整的 `SKILL.md` 正文以及任何 `scripts/`、`references/` 或 `assets/` 只会在之后、即 skill 真正被激活时才加载。

[Codex skills 文档](https://developers.openai.com/codex/build-skills)与[自定义文档](https://developers.openai.com/codex/customization/overview#skills)从 Codex 一侧描述了同样的行为：Codex 从每个 skill 的元数据开始做发现，只在选中该 skill 时才加载 `SKILL.md`，只在需要时才阅读参考资料或运行脚本。[Skills in OpenAI API cookbook](https://developers.openai.com/cookbook/examples/skills_in_api/#what-is-a-skill) 同样明确地描述了托管 shell（hosted shell）一侧：OpenAI 先读取每个 skill 的 `name`、`description` 与路径，模型利用这些信息决定何时读取完整的 `SKILL.md`。其 [SKILL.md frontmatter 部分](https://developers.openai.com/cookbook/examples/skills_in_api/#skillmd-frontmatter)把这个观点说得更直接：`name` 与 `description` 对发现与路由非常重要。

在 Agents SDK 仓库中，这使得 `description` 成为 Codex 读取 skill 其余部分之前的主要路由信号之一。

下面是来自 `code-change-verification` 的一个具体例子。

过于含糊：

```
description: Run the mandatory verification stack in the OpenAI Agents JS monorepo.
```

更好（实际的描述）：

```
description: Run the mandatory verification stack when changes affect runtime code, tests, or build/test behavior in the OpenAI Agents JS monorepo.
```

较短的那个版本已经告诉 Codex 这个 skill 做什么，但仍然没有说明它何时适用、什么样的变更应当触发它，以及这些检查是否可选。更具体的那个版本把这三点都告诉了模型。

同样的模式也出现在 `pr-draft-summary` 中。

```
description: Create a PR title and draft description for a pull request.
```

```
description: Create a PR title and draft description after substantive code changes are finished. Trigger when wrapping up a moderate-or-larger change (runtime code, tests, build config, docs with behavior impact) and you need the PR-ready summary block with change summary plus PR draft text.
```

同样，实际的描述就是路由元数据。它告诉 Codex：

- 这是一个任务收尾型 skill
- 它面向实质性变更，而不是每一次对话轮次
- 输出是可直接用于 PR 的文本块，而不只是一段散文式总结

从这些仓库中得到的一条实用经验是：在 `description` 上花时间。如果路由感觉不可靠，先修元数据，再考虑加更多代码。

## 把机械性工作放进脚本

接下来要回答的问题是：什么属于模型，什么应该下沉到脚本里。

一个可靠的划分是：

- 解释、比较与汇报留在模型侧
- 确定性的、重复的 shell 工作放进 `scripts/`

这与公开的指导一致。[Codex 自定义文档](https://developers.openai.com/codex/customization/overview#skills)把 skills 描述为一种为可重复工作流向 Codex 提供更丰富指令、脚本与参考资料、而不让上下文一开始就膨胀的方式。这符合「模型优先」的设定：让 Codex 处理工作中依赖上下文的部分，只在需要时才引入脚本来处理确定性部分。[Skills in OpenAI API cookbook](https://developers.openai.com/cookbook/examples/skills_in_api/#operational-best-practices) 也建议把 skill 脚本设计成微型 CLI：从命令行运行、打印确定性的 stdout、在失败时清楚地报出用法或错误信息、并在需要时把输出写到已知的文件路径。

在 Agents SDK 仓库中，我们尽量把模型用在它的智能真正有用的地方，例如：

- 阅读源代码以推断预期行为
- 将日志与预期行为进行比较
- 判断发布 diff 是否包含真实的兼容性风险
- 产出维护者可以据此行动的解释

脚本则处理围绕这些工作的机械性部分，例如：

- 以固定顺序运行仓库要求的验证命令
- 启动示例运行、收集每个示例的日志，并为失败写入重跑文件
- 在发布就绪性审查之前获取上一个发布标签
- 暴露 `start`、`stop`、`status`、`logs`、`tail`、`collect`、`rerun` 等辅助命令，使同一工作流易于反复运行

如果模型每次都得重新摸索同一套 shell 配方，这通常说明该配方应当成为脚本。如果任务依赖上下文、权衡或解释，那部分就应该留给模型。

## 自动化集成测试

两个仓库中最有用的工作流领域之一是自动化集成测试。这里有两个相关层次：在两个仓库中自动校验仓库内示例；以及在 JavaScript 仓库中，另外校验已发布的包在按用户实际消费方式安装后是否仍然可用。

在这套配置之前，示例校验有一部分靠手工。你可以运行示例，但「最后一公里」往往取决于肉眼检查日志，或凭观察判断输出看起来对不对。这对单个示例是可控的，但在一个不断增长的 SDK 仓库里则难以扩展。

第一层是 `examples-auto-run`，但 skill 是在运行器（runner）之后才出现的。要想让示例校验完全自动化，我们首先得在两个仓库中为非交互式示例执行构建底层支持。这意味着要让示例脚本能够以自动模式运行，包括那些通常需要提示或批准的示例。

这项基础工作包括：

- 自动应答常见的交互式提示
- 在运行器支持的地方，自动批准 HITL、MCP、`apply_patch` 与 shell 操作
- 把仍不适合自动化的示例保留在自动跳过清单中，例如需要额外运行时配置的 realtime 或 Next.js 应用示例
- 为每次示例运行写入结构化日志
- 生成重跑文件，让失败可以在不重跑全部内容的情况下重试

一旦这些基础就位，我们把它组织成一个 skill，让工作流变得可复用、易于调用。在 Python 仓库中，`examples-auto-run` 封装了 `uv run examples/run_examples.py --auto-mode --write-rerun --main-log ... --logs-dir ...`。在 JavaScript 仓库中，它先封装构建检查，然后在自动模式下运行 `pnpm examples:start-all`，并带每示例日志与重跑支持。

为了提升校验质量，运行器的职责是执行示例并把它们的 stdout 与 stderr 保存到每示例日志中。然后，该 skill 让 Codex 逐份通读这些日志，并与源代码进行比对：

- 阅读示例源码与注释
- 推断预期流程
- 打开对应的日志
- 将预期行为与实际的 stdout 和 stderr 进行比较
- 对每个成功的示例都这样做，而不是只抽查一个

这比试图把正确性编码为固定的脚本级断言更准确、更灵活。成功的退出码有用，但对于那些要调用真实 API、使用工具或产出结构化输出的示例来说还不够。通过先记录实际输出，再对照源代码仔细检查，我们可以按照每个示例的真实意图来校验它。

在 JavaScript 仓库中，还有第二层：独立的 `integration-tests` skill。该工作流超越了在原位运行源码示例。它把包发布到本地 Verdaccio registry，并在多种环境中测试安装与运行，包括 Node.js、Bun、Deno、Cloudflare Workers 以及一个 Vite React 应用。这捕获的是另一类问题：不是「示例在仓库里能跑吗？」，而是「包在发布、安装与运行时集成之后是否仍然行为正确？」

综合来看，这些工作流展示了为什么把 skills、脚本与模型判断结合起来是有用的。脚本让运行可重复、捕获证据，并覆盖那些手工检查起来枯燥乏味的安装路径。Codex 随后利用这些证据做出比简单的脚本通过/失败检查更细致的比较。

## 增加发布检查

发布准备是这一模式同样能帮上忙的另一个领域。

两个仓库中的发布审查工作流，都是先找到上一个发布标签，将其与最新的 `main` 做 diff，然后让 Codex 检查这个 diff 中是否存在：

- 公开 API 与面向用户的 SDK 行为中的向后兼容性问题
- 回归，包括预期行为中的细微变化
- 需要迁移说明或发布说明更新的变更却缺少相应内容

基于这些发现，该 skill 做出整体的发布就绪判定。

一个具体的例子是 [openai/openai-agents-python#2480](https://github.com/openai/openai-agents-python/pull/2480)，其中的发布审查整体保持绿色，同时仍指出移除 Python 3.9 支持及所需的发布说明后续工作：

```
Release readiness review (excerpt)

Release call:
🟢 GREEN LIGHT TO SHIP. Minor-version bump includes expected breaking change
(Python 3.9 drop) with no concrete regressions found.

Scope summary:

- 38 files changed (+1450/-789); key areas touched: `src/agents/tool.py`,
  `src/agents/extensions/`, `src/agents/realtime/`, `tests/`,
  `pyproject.toml`, `uv.lock`.

Python 3.9 support removed

- Risk: 🟡 MODERATE. Users pinned to Python 3.9 will be unable to install the
  0.9.0 release.
- Evidence: `pyproject.toml` now sets `requires-python = ">=3.10"` and drops
  the Python 3.9 classifier; CI skip logic for 3.9 was removed.
- Action: Ensure release notes clearly call out the Python 3.9 drop and that
  packaging metadata remains `>=3.10`.
```

该 skill 还定义了关卡判定如何做出。审查从「可以安全发布」出发，只有当 diff 显示出真实问题的具体证据时才切换为阻塞（blocked）判定。每个阻塞判定都必须附带一份具体的解除阻塞清单。这让输出更容易使用：绿色结果意味着 diff 中未发现阻塞发布的问题，而阻塞结果意味着存在一个有着明确下一步的真实问题。

这比一句泛泛的「请审查这次发布」有用得多。它迫使模型针对具体的 diff 进行推理，并用可操作的术语解释结果。如果发布是安全的，就直说。如果不是，就指出确切的证据与确切的后续工作。

## 在 CI 中运行工作流

一旦某个 skill 在本地证明有用，[Codex GitHub Action](https://developers.openai.com/codex/github-action) 就能让在 CI 中自动化同一工作流变得容易。当本地工作流已经稳定时效果最好，因为手动使用正是你调试指令、打磨脚本并发现真实边界情况的地方。

对于公开仓库，触发器设计与 skill 本身同样重要。[GitHub Action 安全清单](https://developers.openai.com/codex/github-action#security-checklist)建议：限制谁可以启动工作流，优先使用可信事件或显式批准，对来自 PR、提交、issue 或评论的提示词输入进行清洗，用 `drop-sudo` 或非特权用户保护 `OPENAI_API_KEY`，并把 Codex 作为任务中的最后一步运行。

如果一个工作流具备写能力且接受不可信的公开输入，风险通常出在围绕该 skill 的触发器设计、输入处理与运行时权限上。

## 在 PR 审查中使用 Codex

skills 是这些仓库生产力故事的一部分。[Codex GitHub PR 自动审查](https://developers.openai.com/codex/third-party/github)是另一部分。

自 Codex GitHub PR 自动审查可用以来，Codex 一直是这些仓库中大多数代码变更的有用审查者。我们把它当作审查的常规组成部分，而不是一个特殊场景工具。

对于直接的程序 bug、回归与缺失的测试，把 Codex 作为必需审查路径在实践中已经足够可靠。它在反复检查同样的正确性模式方面非常一致，并且已经消除了小型修复与常规改进的一大瓶颈。

同行评审仍然重要，但针对的是另一类变更。

当主要问题不是「这段代码正确吗？」而是「几个都可行的方案中应该选哪个，以及我们应该怎么发布它？」时，人类审查仍然不可或缺。这包括：

- 存在多个合理设计、维护者需要做出明确选择的 API 或架构变更
- 影响产品预期、向后兼容承诺或灰度发布策略的行为变更
- 命名、迁移与发布沟通决策，其难点在于选择对用户与贡献者来说最清晰的表达
- 需要在维护者或团队之间达成一致的变更，例如界定工作范围、安排先后顺序，或决定什么现在发布、什么以后发布

在上述所有情况中，Codex 仍然可以有用地贡献力量，但这些情况仍然受益于人类决策者与直接讨论。

`AGENTS.md` 也可以编码这种分工：仓库可以告诉 Codex 什么对正确性审查算重要，而 Codex 可以一致地应用这些指导。

这也是吞吐量的一个重要来源。重复性的审查与验证工作不再为每一个低风险变更占用稀缺的审查者时间，而维护者可以把精力集中在他们的判断最有价值的高上下文审查上。这一转变帮助我们更快地消化积压的 bug 与较小的功能改进。

## 结语

在 OpenAI Agents SDK 仓库中，当 skills 成为仓库日常工作配置的一部分时，它们才能发挥最大效用。

`AGENTS.md` 告诉 Codex 哪些工作流是必需的。`description` 告诉它何时路由进入这些工作流。`scripts/` 处理确定性的部分。模型处理依赖上下文的部分。一旦某个工作流在本地足够稳固，[Codex GitHub Action](https://developers.openai.com/codex/github-action) 就能把同样的流程带进 CI。

这让这些仓库中的日常工程工作更加明确、更加可靠。它也让更快地交付小改进变得更容易，因为验证、发布审查与 PR 交接如今遵循同一个可重复的流程。

## 资源

- [面向 Python 的 OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- [面向 JS 的 OpenAI Agents SDK](https://github.com/openai/openai-agents-js)
- [Codex 中的 Skills](https://developers.openai.com/codex/customization/overview#skills)
- [使用 AGENTS.md 的自定义指令](https://developers.openai.com/codex/agent-configuration/agents-md)
- [Codex GitHub Action](https://developers.openai.com/codex/github-action)
- [在 GitHub 中使用 Codex](https://developers.openai.com/codex/third-party/github)
- [Skills in OpenAI API cookbook](https://developers.openai.com/cookbook/examples/skills_in_api)
- [Agent Skills 规范](https://agentskills.io/specification)
- [Skills in OpenAI API：运维最佳实践](https://developers.openai.com/cookbook/examples/skills_in_api/#operational-best-practices)
