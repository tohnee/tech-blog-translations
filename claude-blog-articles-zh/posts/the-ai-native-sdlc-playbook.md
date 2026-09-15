---
title: "AI 原生 SDLC 实战手册"
title_en: "The AI-Native SDLC playbook"
source: https://claude.com/blog/the-ai-native-sdlc-playbook/
crawled: 2026-09-14
translated: 2026-09-14
---

# AI 原生 SDLC 实战手册

> 原文：[The AI-Native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook/) · Claude 博客

## 代码不再是瓶颈

各组织已经开始用 AI 以一年前不可想象的速度编写代码，然而围绕代码的流程却没有以同样的速度改变。

许多工程团队仍然沿用同样的审批关卡、评审、交接与政策，使 [Claude Code](https://claude.com/product/claude-code) 这类智能体编码方案带来的生产力提升停滞不前。

软件开发生命周期（SDLC）是将软件从想法带到生产环境的过程。大多数组织运行的流程都是同样六个阶段的某种变体：规划、设计、构建、测试、部署与维护软件。传统上，每个阶段都是由不同角色负责的离散阶段：产品经理撰写需求，技术架构师将其转化为设计，工程师按设计实现，受监管企业的 QA 团队进行验证，发布团队负责上线，运维团队监控运行中的系统。工作在不同阶段之间通过文档、工单和签核流转。

传统软件开发生命周期（SDLC）流程繁重，为的是确保每个环节都有问责与控制。然而，传统 SDLC 是为一个"编写与实现代码是最耗时、最昂贵的环节"的时代设计的，而这种情况已不复存在。PRD（产品需求文档）、工作量估算仪式和产品安全评审，全都是为了让人们在可能持续数周、数月甚至数个季度的开发工作中强制达成一致而存在的。

传统 SDLC 还带有"每一步都由人来执行"的假设。产出价值最高的组织已经围绕智能体 AI（agentic AI）现在能做到的事情重建了流程，同时确保人类始终在环。在本指南中，我们将结合服务客户的经验，逐一介绍 Applied AI 团队在 SDLC 各个阶段内部集成 Claude、以加速开发并让流程更快运转的若干最佳实践。

当代码不再是瓶颈、构建阶段的速度快于传统 SDLC 所允许的速度时，有三件事成为现实：

- 瓶颈转移到了构建阶段左右两侧的步骤上。主要是规划、评审/测试和部署，它们仍然以人类速度运行。
- 各种控制措施不再匹配现实，变得难以执行。逐行人工评审在代码由人编写时是合理的，但一旦大部分 diff 由智能体写出，它就跟不上了。
- 治理成本上升，因为例外情况仍然要走那些每周或每月才开一次的会议和委员会。

构建不再是约束——围绕它的人类速度步骤才是。人类速度的阶段保持原有时长，而构建阶段坍缩到几个小时。

让我们以安全瓶颈为例。安全团队的规模是按人类产出配置的，所以当智能体让代码产出成倍增长时，要么评审队列越积越多，要么代码在评审不足的情况下上线。受监管的组织无法接受其中任何一种结果，因此它的安全与政策检查必须跟上智能体的速度。

为了更好地实现智能体 AI 的生产力收益并保障其安全，传统 SDLC 生命周期需要经历与实现阶段同等程度的转型。

1. 代码不再是瓶颈
2. 打法（Plays）
3. 第 1 阶段——规划（Plan）
4. 第 2 阶段——设计（Design）
5. 第 3 阶段——构建（Build）
6. 第 4 阶段——测试（Test）
7. 第 5 阶段——部署（Deploy）
8. 第 6 阶段——维护（Maintain）
9. 结语

## 什么是 AI 原生 SDLC？

AI 原生 SDLC 是一个重新构想的过程，它把旧的控制目标与新的执行手段结合在一起。流程不再是线性流转，而是变成一个循环，并且 AI 嵌入在每一个节点上。AI 原生 SDLC 推动自动化的交接与后续打法的触发，帮助解决传统 SDLC 各阶段之间人工且笨重的交接问题。

你也会听到这种转变被称为智能体 SDLC（agentic SDLC）、AI SDLC，或干脆叫智能体软件开发——叫法不同，描述的是同一件事。

### AI 原生 SDLC 六个阶段中的转变

下表突出展示了传统 SDLC 与 AI 原生 SDLC（由 Claude 支撑）这两个光谱端点。大多数组织都处在这两列之间的某个位置。

| 阶段 | 传统 SDLC | AI 原生 SDLC |
|---|---|---|
| 规划（Plan） | 需求由委员会收集，经研讨会与签核提炼，再由人工撰写 | Claude 直接从源头综合痛点，并将其捕获在 `intent.md` 中——该文件人类可读、机器可执行 |
| 设计（Design） | 规格说明由分析师撰写、由设计师解读 | 需求与设计被压缩进与智能体的一次工作会话，以编码为 skills 的标准为指导，并在 git 中版本化 |
| 构建（Build） | 测试与代码由人工手写，文档在主要开发完成之后补写 | 测试与代码由 AI 生成，机构知识以版本化的机器可读 `CLAUDE.md` 文件与 skills 维护 |
| 测试（Test） | 在阶段边界设置 QA 关卡 | 持续的 eval 编织进实现过程 |
| 部署（Deploy） | 人工评审每一行代码，治理发生在评审周期中，且往往执行不一致 | 多层智能体评审，人工评审只保留给受监管与关键代码。治理在 AI 行动时即被强制执行，hooks 充当审批关卡 |
| 维护（Maintain） | 人工盯守生产环境找 bug | 智能体监控线上部署。任何被突破的控制带（control band）都会被诊断，并作为新的 `intent.md` 写回循环 |

贯穿右列的主线是"已提交的工件（artifact）"。每个阶段都以向版本控制写入一个工件收尾（包括 `intent.md`、`spec.md`、`plan.md`、diff 及其测试、连同评审意见的 PR，以及事故记录），下一个阶段则以读取它开始。在早期阶段，.md 文件是主要的工件，因为产品负责人和智能体可以读取同一个文件并据其行动。从构建阶段开始，工件变成代码及其记录。这条提交链同时也是审计线索：谁提出了什么请求、智能体产出了什么、谁批准了它。

对于每一个需要判断力的决策，人类仍然负有责任。在智能体 SDLC 的世界里，人类的注意力随必须评审的工件而转移。

## 打法（Plays）

这些打法（play）是整本实战手册的核心，被划分为六个非线性的阶段（规划、设计、构建、测试、部署、维护），共同覆盖完整的生命周期。

每一条打法都涵盖：

- 哪些东西会改变；
- 如何上手；
- 具体的实施步骤；
- 治理方面的考量；以及
- 如何衡量它是否奏效。

这些步骤是模块化的，组织可以基于自身独特需求，选择在不同时间优先转型不同的阶段。每条打法都在"前置条件"（Prerequisites）下列出它的依赖，依赖关系图对此作了进一步说明。

一个阶段以提交一个工件收尾，而这次提交会启动下一个阶段。一份被接受的 `intent.md` 触发需求与设计环节；一份被批准的 `spec.md` 触发计划模式；一个被合并的 PR 触发流水线；生产环境中一条被突破的控制带写出下一份 `intent.md`——如此循环往复。

起初，你为每一步手动输入提示；最终状态则是一个循环，其中每一份被接受的工件都会触发下一道关卡。人类的注意力集中在关卡上，评审智能体标记的内容，而不是从零开始启动每个阶段。

这些打法按阶段列出；箭头给出的是采纳它们的顺序。两者并不是一回事。从 Plan 打法入手即可——没有任何箭头指向它，所以它不需要任何前置。对于其他任何打法，指向它的箭头就是应当先于它采纳的打法。

## 规划（Plan）

### 捕获为 intent.md

启动软件开发流程的 `intent.md` 可以通过不同的路径进入流程。某个人有了一个想法，有人提交了一个工单，或者一次事故通过告警浮出水面（见第 6 阶段：维护）。

当一个人有了想法时，他会与 Claude 一起头脑风暴，产出一份 markdown 原始规格（proto-spec）。在传统 SDLC 中，同一个人接下来还得说服产品团队的某个成员与他一起撰写这个想法，或者代笔。

Claude 生成的原始规格人类可读、受版本控制，并且可以被下一个阶段立即消费。原始规格被保存为 `intent.md`。

无论意图源自事件触发还是智能体，步骤都是一样的：产品负责人在 `intent.md` 提交之前评审并修正智能体写好的内容。

完成这项设置是平台团队或工程团队的一次性任务。需要一名技术团队成员搭起 intent 的存放地（intent home）并决定谁有权写入，因为贡献者将来自整个组织。

仓库建立之后，没有 git 经验的贡献者不需要直接使用 git。通过一个连接到版本控制系统（例如 GitHub）的连接器，Claude 可以在 claude.ai 或 Cowork 中代表他们提交 markdown 文件。

#### 如何执行

1. 发起人用自己的话向 Claude 描述问题。发起人可以描述他们今天做不到什么、这个想法影响到谁、更好是什么样子，以及哪些内容不在范围内。不需要任何正式语言。
2. 头脑风暴，直到想法变得具体。Claude 会提出分析师会问的问题：范围、用户、约束，以及成功是什么样子。
3. 让 Claude 使用组织的模板把结果写成 `intent.md`，该模板可以编码为由技术团队成员创建、由负责人签核的一个 skill。内容可以涵盖问题、期望的成果、受影响的用户与系统、约束以及未决问题。
4. 发起人修正 Claude 理解错误的地方。
5. 把 `intent.md` 提交到共享的存放地。作者与时间戳会进入记录，产品负责人从这里接手这个想法。

```
# Intent: claims status self-service
Author: J. Ortiz (claims operations). Status: draft.

## Problem
Customers phone the contact center to ask where their claim is.
Handlers spend roughly a third of call time on status-only queries.

## Proposed outcome
Customers see claim status, next step and expected date in the portal.

## Affected users and systems
Claims handlers, portal team, claims-core API.

## Constraints
No new PII in the portal session. Existing authentication only.

## Open questions
Do third-party loss adjusters need access too?
```

#### 治理考量

证据就是已提交的 `intent.md`，其中列有作者、时间戳和完整的修订历史。它记录在 intent 存放地的 git 历史中。产品负责人进行审批，把意图送入第 2 阶段：设计的接受或拒绝决策则以合并或结项评审的形式被记录下来。

## 设计（Design）

### 需求与设计

一旦产品负责人批准，Claude 就会接受这份 `intent.md` 并产出需求与设计规格说明。这一过程由组织在品牌、安全、合规与 UX 方面的 [skills](https://code.claude.com/docs/en/skills) 加以指导。

产品负责人评审这份规格，但不亲自撰写。这一流程的目标是产出一份工程团队可以据此制定计划的规格说明，并标出值得关注的区域。

前端工作是最直观的例子。一旦 `intent.md` 被接受，产品负责人就可以在 [Claude Design](https://claude.com/product/design)（beta）中根据 `intent.md` 制作设计稿原型，反复迭代，然后把它导出到 Claude Code 中进行构建。

1. 产品负责人打开一个加载了组织 skills 的会话，并附上 `intent.md`。
2. 产品负责人的提示指向 `intent.md`，点明约束条件，并要求标出值得关注的问题。先手动运行，然后把它固化为一个组织级的斜杠命令（slash command）。再往后，把 intent 存放地中 `intent.md` 的接受动作设为触发器，用一个在合并时启动的非交互式任务、加载组织 skills 运行这一流程，并把 `spec.md` 作为拉取请求（pull request）提交（第 5 阶段：部署中的 CI/CD 打法涵盖了这些管道工作）。从那时起，产品负责人的第一次介入就是评审。
3. 同一位产品负责人对照原始想法评审规格。这份规格是否解决了陈述的问题？`intent.md` 中的未决问题是被回答了还是被顺延了？
4. 先处理那些被标记的问题，因为它们正是分析师会上报的点。在工程团队看到规格之前，产品负责人要与对应的政策负责人逐一解决它们。
5. 把 `spec.md` 与 `intent.md` 一起提交。这对文件记录了要过什么、决定了什么。
6. 产品负责人决定规格与意图是否进入构建阶段，凡组织归类为较高风险的内容都要咨询技术负责人。这个决定永远由一位人类队友做出，而接受这份规格正是第 3 阶段：构建中计划模式打法的启动点。

#### 实际示例（提示词）

```
Read the attached intent.md and produce a requirements and design spec for integrating it into our existing codebase. Apply the skills available to you so the plan conforms to our brand guidelines, security policies and UX standards. Document the spec fully as spec.md, ready to hand to the engineering team. Describe clearly any areas of concern, especially where you cannot satisfy contradicting policies.
```

策略不再是在数周后的评审中才被发现，而是在规格撰写的同时就被读取并应用。组织的 skills 作为约束被套用到规格上。规格本身、产生它的提示词以及当时生效的 skill 版本，全部记录在版本控制中。产品负责人签核规格，并把被标记的问题分派给指定的政策负责人。

## 构建（Build）

### 以 Claude Code 计划模式作为默认起点

工程师以[计划模式（plan mode）](https://code.claude.com/docs/en/permission-modes)启动 Claude Code 会话，把第 2 阶段：设计中已批准的 `spec.md` 交给 Claude，让它向自己提问，不断迭代计划，直到工程师满意为止。

1. 工程师以计划模式与 Claude 开始会话。
2. 工程师把 `intent.md` 与 `spec.md` 交给 Claude，要求产出一份实现计划，其中要点名哪些文件会改动、工作的先后顺序，以及证明改动成立的测试。
3. 通过提问来拷问这份计划：这个改动可能破坏什么？哪一步风险最大？Claude 选择了不做哪些其他方案？
4. 持续迭代，直到一位从未看过这段对话的工程师也能仅凭这份计划实现该改动。
5. 把批准的计划提交为 `plan.md`。计划进入审计线索，PR 评审打法（第 5 阶段：部署）会对照它检查最终的 diff。
6. 接受计划，让 Claude 实现。有了扎实的计划，实现往往一轮就能完成。
7. 当实现偏离计划时，在同一次提交中更新 `plan.md`。可以考虑用一个 hook 来强制两者保持同步。

#### 实际示例（plan.md）

```
# Plan: claims status self-service (from intent.md 2026-06-02)

## Files that change
portal/src/claims/StatusPanel.tsx (new), claims-api/routes/status.py,
claims-api/tests/test_status.py

## Order of work
1. Add the status endpoint behind existing auth.
2. Panel against the endpoint.
3. Wire into the portal nav.

## Risks
The claims-core API rate-limits at 50 rps; the panel must cache.

## Proof
test_status.py covers the four claim states; screenshot matches the
approved mock.
```

设计评审发生在任何代码生成之前，此时改变方向仍只是编辑一份文档的事。计划模式本身就在强制这一点，因为在工程师接受计划之前，Claude 无法编辑文件。计划及其修订都被记录在案，连同批准它的人。常规修改由工程师批准，凡组织归类为较高风险的内容则交给技术负责人或架构师。

### Claude Code 的自动模式（auto mode）

Claude Code 也可以在自动模式（auto mode）下运行：工程师批准计划，反复迭代到满意之后，Claude 无需逐次编辑提示即可应用每一处修改。随着后续打法中的防护栏逐渐成熟（一份调校好的 `CLAUDE.md`、把政策编码进去的 skills、能拦截不安全操作的 hooks，以及一套 Claude 可以运行的测试套件），自动接受会成为常规工作的默认：一份紧凑的 `spec.md`、一个很小的影响半径（blast radius），以及测试已经覆盖的代码。

转变的方向从此前"用户盯着智能体做编辑、逐一审查操作"，转向"在更长的自主会话之后评审工件"。自动接受模式配合 git worktree 使用时，还能进一步实现个人与团队层面的并行，并且是让 SDLC 自主运行、在第 6 阶段：维护中闭合循环的基础。

### 遗留系统与事实来源

### CLAUDE.md

[`CLAUDE.md`](https://code.claude.com/docs/en/memory) 为 Claude 提供新入职者所需的上下文，涵盖约定、命令、架构，以及团队最常犯的错误。过去存放在人们脑中和 wiki 上的知识，变成了智能体在每次会话开始时都会读取的一个文件，由整个团队共同维护，并且每当出现错误时就迭代一次。

1. 在仓库中运行 `/init`。Claude 会根据它发现的内容生成一份初始的 `CLAUDE.md`。
2. 把生成的文件裁剪到新人在第一天需要知道的内容。保留构建、测试和 lint 命令，重要的约定，以及 Claude 反复出错的地方。
3. 把 `CLAUDE.md` 提交到仓库根目录的 git 中，这样整个团队共享同一个版本，修改也像代码一样被评审。
4. 这里有一条行之有效的工作规则：当 Claude 犯了第二次同样的错误时，就把纠正写进 `CLAUDE.md`。
5. 控制在一页以内，因为 Claude 会在会话开始时通读全文，任何过时的内容都在白白占用上下文。

#### 实际示例（CLAUDE.md）

```
# Payments service

## Commands
- Build: make build
- Test: make test (unit), make itest (integration, needs docker)
- Lint: make lint (runs in CI; fix before pushing)

## Conventions
- Java 21, Spring Boot 3. No new Lombok.
- Money is always BigDecimal, never double.
- Every endpoint needs an integration test in src/itest.

## Architecture
- api/ holds REST controllers, core/ holds domain logic,
  adapters/ talks to external systems.
- Kafka events are defined in schemas/; never edit generated classes.

## Things Claude gets wrong
- Do not bump dependency versions; the platform team owns them.
- The legacy v1/ package is frozen; changes go in v2/.
```

`CLAUDE.md` 受版本控制，因此智能体遵循的指令是可评审、可审计的。团队约定通过这个文件被强制执行，对它的修改记录在 git 历史中，代码所有者（code owner）在 PR 评审中批准这些修改。

### 作为机构知识的 Skills

Skills 是组织让机构知识真正运转起来的方式。指令是显式的、受版本控制的、被广泛应用的，并且在政策变化时集中更新。经验法则：凡必须被一致执行的机构知识，就写成 skill；凡属于 `CLAUDE.md` 或一条提示的内容，就不要写成 skill。

1. 选一条今天执行得不一致的知识。它可能是一条安全标准、一个 API 设计约定，或一条品牌规则。
2. 把它写成一个 skill——一个包含 `SKILL.md` 的文件夹，其 frontmatter 说明何时触发，正文说明要做什么。由工程师从政策负责人的事实来源出发撰写，借助 Claude 协助。
3. 把 skill 放进仓库的 `.claude/skills/<name>/` 目录，让它随代码一起发布，或通过[插件（plugin）](https://code.claude.com/docs/en/plugin-marketplaces)在组织范围内分发。
4. 测试 skill 是否会触发。用不同的方式让 Claude 执行相关任务，确认每次都能加载这个 skill。
5. 当政策变化时，更新 skill，并让政策负责人签核这次变更。
6. 工程师在下一次会话中自动拿到新版本。

#### 实际示例（.claude/skills/secure-api-review/SKILL.md）

```
---
name: secure-api-review
description: Apply the API security standard. Use whenever creating or
  modifying an external-facing endpoint, reviewing API code, or
  generating an OpenAPI spec.
---
# Secure API review

When you create or change an API endpoint:
1. Authentication: every endpoint requires the gateway JWT;
   no anonymous routes outside /health.
2. Input validation: validate request bodies against the OpenAPI
   schema and reject unknown fields.
3. Audit: every state-changing endpoint emits an audit event with
   actor, action, entity and timestamp.
4. Data classification: fields tagged pii in the schema must never
   appear in logs or error messages.

Run scripts/check-endpoints.sh and include its output in your summary.
```

skill 是一种控制，尽管是建议性的。它让 Claude 在编写代码时倾向于执行政策，但没有任何东西强制会话遵守它。一条必须始终成立的政策，需要在 skill 背后有某种确定性机制，比如一个拦截操作的 hook，或在 PR 处重新核查政策的评审环节。skill 让违规变得罕见，hook 让违规几乎不可能。skill 的调用记录在会话轨迹中，政策负责人像评审代码一样评审 skill 的变更。

### 作为构建期防护栏的 hooks

skill 是建议性控制，而 [hook](https://code.claude.com/docs/en/hooks) 是它背后的确定性层。Claude 在实现期间的大多数操作是文件编辑和 shell 命令，因此构建阶段是 hooks 触发最频繁的地方。

构建阶段的 hooks 可以：

- 拦截对受保护路径的编辑，例如生成的类或被冻结的包；
- 在文件编辑后运行格式化工具和 linter，让偏移永不累积；
- 把凭据挡在 diff 之外。

凡政策必须无条件成立的 skill，都要用 hook 兜底。hook 在每一条匹配的操作上运行，因此构建阶段的 hooks 应当快速，且只作用于发生变更的文件。更重的检查（例如完整测试套件）应放在提交或 PR 环节。

需要向人类请求批准的 hook 属于第 5 阶段：部署中的关卡，因为构建期间弹出的批准提示会把一个人重新拉回所有并行会话的关键路径上。

### 并行会话与子智能体

一名工程师可以同时驱动多条工作流。

并行会话（parallel session）是另一个完整的 Claude Code 实例，在自己的 [git worktree](https://code.claude.com/docs/en/worktrees) 中处理一项独立的任务。每个独立会话对其他会话一无所知，驾驭它们的工程师是它们唯一的交集。

[子智能体（subagent）](https://code.claude.com/docs/en/sub-agents)则运行在单个会话内部，是一个拥有自己上下文窗口和工具限制的范围化助手，适合那些在多个任务中反复出现的工作，例如验证应用按预期运行。

并行会话提高了一名工程师可以同时推进的任务数量，而子智能体让每个会话专注于自己的任务。工程师的职责是驾驭并评审所有这些工作。

1. 工程师把工作拆成触及不同文件的任务，借助计划模式打法（第 3 阶段：构建）得到的计划判断哪些工作相互独立。共享文件的任务在单个会话中依次运行。
2. 每个并行任务拥有自己的 worktree，例如在一个终端运行 `claude --worktree feature-auth`，在另一个终端运行 `claude --worktree fix-rate-limit`。worktree 是独立分支上的独立检出，可以避免会话在文件上相互冲突。
3. 两到三个会话是合理的起点。实际的上限是一个人能够认真评审的工作流数量，所以只要评审还跟得上，就可以增加会话。
4. 把重复性的工作变成子智能体，以 markdown 文件的形式定义在 `.claude/agents/` 中，每个都有名字、何时使用的描述，以及允许使用的工具。例如：一个在主智能体完成后剥离多余复杂度的代码简化器，一个运行应用并检查行为的验证器，一个探索代码库并汇报结果而不淹没主上下文的研究员。把这些定义提交进 git，让整个团队共享。

#### 实际示例（.claude/agents/verifier.md）

```
---
name: verifier
description: Runs the app and checks the change works before the session
  reports done
tools: Bash, Read
---
Start the app with make run. Exercise the changed behavior and the two
nearest neighboring flows. Report what you ran, what you saw, and any
behavior that does not match plan.md. Do not fix anything; report only.
```

更多的会话意味着更多的产出，因此控制必须来自仓库中的配置。那里的 hooks 与权限设置适用于所有会话，会话所做的操作都会被记录并归因到运行它的工程师。

## 测试（Test）

### 给 Claude 一个反馈回路

永远要给 Claude 一种验证自己工作的方式，无论是测试、构建还是截图对比。这样，会话会自己检查工作、在工程师看到之前修好自己的错误。

反馈回路不要与验证器子智能体（第 3 阶段：构建）混淆。反馈回路贯穿整个任务，随工作反复运行。而验证器子智能体是打包最终检查的一种方式：在会话认为工作已完成时，用一个全新的上下文窗口运行一次。这样，结论就不会被产生代码的那些假设所染色。

1. 如果今天检查工作需要一串命令和一些环境知识，就把它包装成一个单一目标，例如 "make test" 或 "npm test"，失败时以非零值退出。
2. 在 `CLAUDE.md` 的 Commands 部分，为每条命令附上一个正常输出的示例。
3. 给出目标并让它可量化，这样 Claude 无须问你就能自查工作，例如："test_status.py 中的所有测试通过"、"截图与附带的稿子一致"，或"端点返回 200 且带新字段"。
4. 对于 bug 修复，先写失败的测试。让 Claude 把这个 bug 复现为一个测试，运行它，确认它因你预期的原因而失败。提交这个测试。然后才让 Claude 在不编辑测试的前提下让它通过，由最后一步中的测试文件 hook 来强制这一限制。一个在修复之前就存在、且智能体无法改写的测试，就是 bug 已被消灭的证明。
5. 对于 UI 工作，用视觉检查来闭合回路。给 Claude 一个浏览器或截图工具，把设计稿给它，让它迭代。实现、截图、对比、调整。两到三轮是正常的，且结果应当一轮比一轮好。
6. 把验证纳入"完成"的定义。指令写在 `CLAUDE.md` 里。在报告任务完成之前先运行测试，并展示输出。
7. 最后，回路本身也需要保护，因为一个修复代码的智能体绝不能有能力削弱针对该代码的检查。用一个在修复任务期间阻止编辑测试文件的 hook 就能做到这一点。另一种做法是在评审时检查 diff，拒绝任何触及测试的改动。

#### 实际示例（CLAUDE.md 验证块）

```
## Verifying your work

- Build: make build (must finish with "Build succeeded")
- Test: make test (all green; never skip or delete a failing test)
- Lint: make lint (zero warnings)

Run all three before reporting any task complete, and paste the output.
If a test fails, fix the code, not the test.
```

### CI 中的持续 eval

eval（评估）是阶段门 QA 的 AI 原生等价物。在实践中，这意味着一套只要智能体的配置发生变化就会运行的套件。当换入一个新模型或重写一条提示时，eval 套件会告诉你智能体是否仍以同样的水准完成工作。

eval 应当被看作一套活的测试。随着模型改进，曾经有区分力的用例会逐渐失效，必须根据持续监控新增用例。

根据使用场景，一些团队可能更愿意按固定节奏离线运行这些 eval，而不是在每次变更时运行。以下步骤针对的是持续评估。

1. 平台工程师从近期工作中收集 20 到 50 个真实任务及其预期/可接受的产出。
2. 把每个任务写成一个 eval，即提示词加上定义"可接受"的检查（测试通过、lint 干净、行为不变、政策得到遵守）。
3. 套件在 CI 中以非交互方式运行，按计划执行，并在 `CLAUDE.md`、skills 或 hooks 发生任何变更时触发，因为这些配置引导着智能体，理应获得与代码同等的回归测试。
4. 以结果作为配置变更的门槛。一条导致通过率下降的 skill 变更，要在合并前接受评审。
5. 每一次生产事故都对应一个 eval，由负责该事故的团队撰写，并作为回归测试留在套件中。

#### 实际示例（.github/workflows/agent-evals.yml）

```
name: Agent evals
on:
  pull_request:
    paths: ['CLAUDE.md', '.claude/**']
  schedule:
    - cron: '0 2 * * *'
jobs:
  evals:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install -g @anthropic-ai/claude-code
      - name: Run eval suite
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          for eval in evals/*.json; do
            claude -p "$(jq -r '.prompt' $eval)" \
              --allowedTools "Read,Edit,Bash(make test)" \
              --output-format json > result.json
            ./evals/check.sh "$eval" result.json
          done
```

eval 让 QA 拥有一个跟得上智能体产出的关卡。通过率阈值作为合并检查被强制执行，每次运行都有日志以便长期比较结果，且拥有该配置变更的团队负责批准它。

## 部署（Deploy）

### PR 评审回路中的 AI

Claude 既做评审者也被评审。它依据组织的政策评审收到的 PR，也会处理自己 PR 上的评审意见。这让工程师可以在 PR 评审中聚焦于行为层面，而行为归结起来就是判断意图与风险。

1. 托管的 Code Review 服务是最快的起步方式。由管理员启用并选择仓库。当你需要掌控流水线，或希望 API 调用走你们自己的云协议时，可以在自己的 CI 中用 claude-code-action 运行评审（CI/CD 打法涵盖了这些管道工作）。
2. 技术负责人把评审政策写成仓库根目录的 `REVIEW.md`，按组织关心的评审轮次（passes）划分：bug 与逻辑错误；安全与漏洞；对照规格（需求打法中的 `spec.md`）、实现计划（计划模式打法中的 `plan.md`）与设计原则的合规检查。`REVIEW.md` 还定义了什么算 Important（重要）而非 Nit（琐碎），以及什么应当跳过。
3. 技术负责人设定人工介入阈值。评审发现本身不会批准或阻止 PR，分支保护仍然要求代码所有者的批准。想在合并环节以发现为门槛的平台工程师，可以把检查运行发布的严重度计数当作机器可读的统计来读取。
4. 当评审者或作者在评审意见中 @ `@claude` 时，Claude 会处理该意见并推送修复。PR 线程同时记录请求与改动。这个修复循环通过 claude-code-action 运行。在托管服务中，评论 `@claude review` 则会请求一次全新的评审。对于 Claude 自己开的 PR，还可以更进一步，让 Claude 把 PR 一路盯到合并。团队会把这一循环封装成一个自定义斜杠命令，扫清 PR 上未解决的评审意见与失败的检查，逐项处理并推送修复，直到 PR 变绿、只等代码所有者批准。
5. 评审发现会回流到 `CLAUDE.md`。当评审第二次标记同一个错误时，纠正就会随该次评审写进 `CLAUDE.md`，而且由于评审会读取 `CLAUDE.md`，从下一个 PR 起这个错误就会被抓住。评审也会在某次变更使 `CLAUDE.md` 过时时将其标记出来。
6. 每月一次，技术负责人通过给发现评级来调校配置，让评审者持续改进，并在 `REVIEW.md` 中为 Nit 的数量设上限。生成的路径以及 CI 已经强制的内容被排除在外。

#### 实际示例（REVIEW.md）

```
# Review instructions

## Passes
Run three passes and tag each finding with its pass:
- Bugs: logic errors, broken edge cases, subtle regressions
- Security: injection risks, authentication gaps, PII in logs
- Compliance: the change matches spec.md, plan.md and our design principles

## What Important means here
Reserve Important for findings that would break behavior, leak data
or breach a policy. Style and naming are nits.

## Cap the nits
Report at most five nits per review; summarize the rest as a count.

## Do not report
Generated files under src/gen/ and anything CI already enforces.
```

职责分离得以保留，因为写代码的那个智能体无法批准它。`REVIEW.md` 中的评审政策适用于所有 PR，发现、修复、评级与批准都记录在 PR 历史中，因此 PR 本身就是审计记录。批准来自人类，通过分支保护实现，并以评审发现作为参考。

关于这些控制在生产规模下如何组合，请参阅[Anthropic 如何保护其 AI 原生 SDLC](https://claude.com/blog/how-anthropic-secures-its-ai-native-software-development-lifecycle)。

### 作为审批关卡的 hooks

构建阶段把 hooks 用作防护栏，在没有任何人参与的情况下允许或拦截操作（第 3 阶段：构建）。hook 也可以"询问"——暂停操作，直到特定的人批准，这正是发布门控所需要的。

这条打法位于第 5 阶段：部署，因为发布关卡是最典型的场景，但 hooks 并不专属于部署：Claude 在哪里行动，它们就在哪里运行。例如，hooks 可以在第 3 阶段：构建中阻止在没有变更工单的情况下编辑迁移与基础设施，在第 4 阶段：测试中阻止智能体在修复任务期间编辑测试文件。

1. 工程管理层会同变更管理与合规部门，列出必须保留的人工审批关卡，例如变更管理签核、发布授权，以及对受保护路径的编辑。
2. 平台工程师把每一道关卡表达为一个 hook——一段在 Claude 行动之前运行的脚本，可以允许、询问或拦截。
3. 团队级 hooks 放在 git 中的 `.claude/settings.json`；不可协商的 hooks 放在由平台或 IT 管理员持有的托管设置（managed settings）中，个别工程师无法在那里把它们关掉。
4. 拦截应当自我解释：当 hook 拦下某个操作时，原因和批准路径会出现在 Claude 的输出里。

#### 实际示例（.claude/settings.json）

```
{
    "hooks": {
      "PreToolUse": [
        {
          "matcher": "Bash",
          "hooks": [
            { "type": "command",
              "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/production-gate.sh" }
          ]
        }
      ]
    }
}
```

#### 关卡脚本本身（.claude/hooks/production-gate.sh）

```
#!/bin/bash
# Production deploys require a named release authorization
cmd=$(jq -r '.tool_input.command' < /dev/stdin)
if [[ "$cmd" == *"deploy"* && "$cmd" == *"production"* ]]; then
   if [ -z "$RELEASE_APPROVAL" ]; then
     echo "Production deploys need a release authorization." >&2
     exit 2 # exit 2 blocks the action; the message goes to Claude
   fi
fi
exit 0
```

hooks 就是审批关卡。关卡条件对每个人、每次都强制执行。允许与拦截的决策都带时间戳记录。关卡还定义了什么算作批准——无论是一张已批准的变更工单，还是发布经理的签核。

### 面向受监管企业的托管设置

### CI/CD 集成与部署

在 CI/CD 流水线中以非交互方式运行 Claude Code，对执行做沙箱化处理让长时间运行的智能体安全地跑，通过 MCP 集成暴露部署能力，并在智能体真正需要回滚路径之前就反复演练它们。

1. 平台工程师从只读的判断类步骤开始。在流水线作业中使用 `claude -p` 来分诊失败的构建、总结一个不稳定的测试，或起草变更日志。
2. 在既有关卡之后加入写操作步骤，用于修复 lint、更新生成的文档，或通过 `@claude` 提及处理评审意见等工作。智能体写入的任何内容都经由分支保护以 PR 的形式抵达，智能体没有任何直推 main 的通道。
3. 执行是沙箱化的。智能体作业在容器中运行，处于网络策略之下，使用短时效的范围化令牌，默认不持有任何生产凭据。
4. 通过 MCP 暴露部署。部署、状态与回滚都成为工具，按环境划定范围，这样智能体的部署能力就是一份允许列表，而不是一个带着凭据的 shell 脚本。
5. 按环境划分自主性层级。在开发环境中，智能体可以自由部署。在生产环境中，智能体准备发布、由发布经理授权，并由一个 hook 强制生产关卡。预发布环境介于两者之间。
6. 回滚应当是流水线中演练最充分的路径——一条智能体可以运行的单一命令，并在预发布环境中定期演练。闭环打法（第 6 阶段：维护）在控制带被突破时会调用这条回滚，因此它必须提前被验证过。

#### 实际示例（流水线步骤）

```
- name: Triage failed build
  if: failure()
  run: >
    claude -p "Read the build log at out/build.log. Identify the most
    likely cause, say whether the failure looks flaky or real, and write a
    three-line summary for the PR thread." >> triage.md
```

统领性的原则是：智能体可以行动到生产关卡为止，但无法越过它。以下控制强制执行这一原则。

- 分支保护把智能体写入的一切都变成 PR，没有任何直达 main 的路径。
- 生产部署 hook 在一名指定的发布经理授权之前阻止发布。每次非交互运行都以智能体自己的身份执行，因此流水线日志能把智能体做了什么与触发它的工程师做了什么区分开来。
- 按环境划分的权限层级决定了智能体在抵达关卡之前能做多少。

## 维护（Maintain）

### 维护与闭环

到目前为止，我们讨论的是如何把 Claude 加进 SDLC 流程的每个阶段，每个阶段都需要一个人来启动最初的步骤。而这一阶段把焦点转向让 Claude 自主运行，闭合整个循环。

例如，一个持续运行的监控智能体可以在一个 bug 工单被提出之后创建一份 `intent.md`，然后流经需求、计划、构建、测试与评审各阶段。第 6 阶段：维护以无头（headless）方式运行，在阶段之间设置独立的置信关卡——一个确定性检查或一个对抗性评审智能体——来决定上一阶段的产出是继续流转还是升级给人类。

### 闭环

一个确定性脚本盯着生产环境，当某条控制带被突破时调用 Claude。对突破的监控是这种自主循环模式的一个有用示例，而本阶段末尾的 [Claude Tag](https://claude.com/product/tag)（公开测试版）一节则涵盖了经由不同渠道抵达的工作。

1. 服务负责人或平台工程师挑选一个拥有稳定滚动基线的指标，例如 CI 测试失败率、部署后 5xx 率或 PR 周转时间。
2. 他们编写检测脚本，通常是在滚动窗口上计算均值与标准差，并配以规则（Western Electric 或类似规则），让控制带既能捕捉缓慢漂移也能捕捉尖峰。脚本受版本控制并有单元测试，检测保持完全确定性，不涉及任何模型。
3. 响应层级在受版本控制的配置中定义（下文的 `bands.yaml`）。在 1σ 时脚本只记录日志；在 2σ 时以只读方式调用 Claude 进行诊断；在 3σ 时 Claude 可以行动，但只能通过向评审关卡提交 PR 或触发预先批准的运行手册（runbook）。
4. 触发层可以是 GitHub 或 GitLab 中的定时工作流、来自既有监控栈的 webhook，或网络内部的 Cron 作业。Claude 以无状态方式运行，或者作为 CI runner 上的非交互步骤，或者作为沙箱化容器中的 Agent SDK 服务；CI/CD 打法涵盖了部署与模型访问选项。由于运行是无状态且非交互的，一个循环可以在没有任何人启动它的情况下开始和结束。
5. 智能体按第 1 阶段：规划的格式把诊断写成 `intent.md`，涵盖异常及其证据、期望的成果、受影响的系统以及任何未决问题。从这里开始，这个发现像其他任何工作一样进入流水线。
6. 服务负责人或值班工程师对队列进行分诊，把面向产品的发现转给产品负责人。立即修复、排期，或驳回。驳回会调校控制带，帮助降低噪声。
7. 当修复上线时，为这次事故添加一个 eval（持续 eval 打法），确保此类问题今后得到防护。

#### 实际示例（例如一份监控 CI 测试失败率的 bands.yaml）

```
metric: ci_test_failure_rate
baseline: rolling_30d
rules: western_electric
tiers:
  1sigma: { action: log }
  2sigma: { action: diagnose,
            tools: "Read,Grep,Bash(gh run view *)" }
  3sigma: { action: propose,
            routes: [pull_request, runbook:rollback-deploy] }
```

层级边界由受版本控制的配置强制执行，权限与托管设置拒绝生产访问。调用、发现与分诊决策都带时间戳记录。服务负责人对发现进行分诊和批准，由此产生的变更走正常的 PR 评审关卡，而智能体可以触发的运行手册都是预先批准过的。

#### 示例

- 当 CI 测试失败率突破 3σ 时，智能体会隔离那个不稳定的测试或打开一个回退 PR，由评审关卡裁决。
- 当部署后 5xx 率在窗口内有一次部署的情况下突破 3σ 时，智能体会触发既有的回滚流水线。
- 当 PR 周转时间触发漂移规则时，智能体会为工程管理层写一份报告，说明这套执行框架对流程指标与生产指标同样有效。

### 定期代码库扫描

安全扫描是关于某个代码库在特定模型下的一份时点性陈述，而这两半都会过时：代码每周都在变，每一代模型都会发现上一代漏掉的漏洞。AI 原生的答案是按计划运行扫描，调用路径中没有人，并把扫描发现送进与其他任何代码库变更相同的关卡。

[Claude Security](https://claude.com/product/claude-security) 是定时扫描的托管形态。连接一个 GitHub 仓库，扫描就会在 Anthropic 基础设施上的 Claude Mythos 5 上运行，每条发现在报告之前都经过验证，并附有置信度评级。建议的补丁在网页版 Claude Code 中评审并应用。组织无需访问模型本身即可获得发现结果。

1. 安全负责人连接仓库，并按仓库、服务或团队把它们组织成项目，让发现结果的责任归属从一开始就清晰。
2. 对最关键的仓库运行第一轮全量扫描，包括那些曾被其他工具或早期模型扫描过的仓库。把第一轮扫描当作基线。第一轮扫描很可能在被视为干净的代码中发现问题。
3. 为每个项目设定扫描计划。对活跃开发的服务，每周一次是合理的默认；仓库较大或混合时，把扫描范围限定到某个目录或分支。
4. 带着置信度评级对发现进行分诊。驳回时要写明理由，这样驳回会被记录下来，同一条发现不会在下一轮以新面目再次出现。
5. 对于范围有限的发现，在网页版 Claude Code 中打开建议的补丁，评审后像其他任何变更一样送入 PR 评审关卡。提出修复的那个智能体没有任何批准它的通道。
6. 对于任何比单个补丁更宽的问题，例如架构性弱点或在多个服务中重复出现的模式，按第 1 阶段的格式写成 `intent.md`，从规划阶段启动。
7. 当某个修复发布到生产时，把这一漏洞类别对应的 eval 加入持续 eval 打法的套件，从此引导智能体的配置就会针对这一类别接受测试。
8. 把发现导出为 CSV 或 Markdown，或使用 webhook，让组织既有的跟踪与审计系统继续充当权威记录系统（system of record），审计人员也早已习惯在那里找到它们。

扫描在组织的管理控制下运行：连接哪些仓库、谁持有扫描席位、支出上限是多少，全部集中设置。每条发现都有验证结果与置信度评级，每次驳回都有理由，因此扫描历史就是一份关于什么被发现、什么被修复、什么被有意识接受的审计记录。

修复经由 PR 评审关卡与分支保护抵达生产，而不是来自扫描本身。Claude Security 是对既有静态分析与依赖扫描的增强。确定性检查留在 CI 中，模型驱动的扫描则覆盖那些检查机制天生无法发现的、依赖上下文的漏洞。

### 用 Claude Tag 让 Claude 参与值班

事故也可以经由其他渠道抵达，例如 Slack 或 Teams 等职场沟通应用。事故可能表现为晚上 10 点事故频道里一条请求紧急修复的 Slack 消息，而现在它可以被立即处置。Claude Tag（公开测试版，当前在 Slack 中可用）让 Claude 以自己的身份成为这些频道的一员，因此每起新事故都有一名第一响应者，而响应本身也成为循环的一部分，并成为未来事故的记忆。

对话与机构知识留在频道里，频道中的任何人都可以引导并处置响应。任何团队成员都可以实时检验假设、探索新选项并进行调查，频道历史则增强了可审计性。通过访问 MCP，Claude 会核实指标已回到基线并在线程中确认，把事故复盘写入受版本控制的 lessons 文件，供未来的调查读取。

事故并不是 Claude Tag 接手的唯一工作。通过 MCP 在工单上被 @，或在频道中被提问，Claude 会以同样的方式对工作进行分诊。小而有清晰边界的修复经由评审关卡以 PR 形式抵达，更大的事项则写成 `intent.md` 进入第 1 阶段：规划——此时循环开始自我供血。参见：[Claude Tag 如何在 Anthropic 为 CI/CD 值班](https://claude.com/blog/ai-ci-cd-on-call)。

频道就是审计线索：请求、诊断、人工授权与修复，全部留在事故被处置的地方。

## 结语

模型与执行框架（harness）已经变得更加先进，让组织不仅可以变革代码的生产方式，还能变革整个软件开发生命周期。

这场变革让人类判断始终处于流程的核心，并兼顾了大型企业组织的治理与监管要求。

本指南汇总了 Applied AI 团队日常为客户执行的众多真实最佳实践，希望它是一份实用且可落地的资源。

### 资源与致谢

下面的文档是一个平台团队搭建这些控制所需的全部内容，大致按你会采用的上线顺序排列。

感谢 Jim Blackhurst、Will Steuk 和 Jamal Arif 对本指南的贡献，本指南深受他们此前工作启发，并建立在其中大量工作之上。

FAQ（常见问题）
