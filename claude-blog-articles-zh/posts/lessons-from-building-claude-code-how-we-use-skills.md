---
title: "构建 Claude Code 的经验教训：我们如何使用 Skills"
title_en: "Lessons from building Claude Code: How we use skills"
source: https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills/
crawled: 2026-09-14
translated: 2026-09-14
---

# 构建 Claude Code 的经验教训：我们如何使用 Skills

> 原文：[Lessons from building Claude Code: How we use skills](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills/) · Claude 博客

Skills（技能）已成为 Claude Code 中使用最广泛的扩展点之一。它们灵活、易创建、易分发。

但这种灵活性也让人难以判断什么做法最有效。哪类 Skills 值得做？该如何组织一个 Skill 的结构？什么时候该与他人分享？

在 Anthropic，我们一直在 Claude Code 中大量使用 Skills，有数百个正处于活跃使用中。以下是我们在用 Skills 加速开发的过程中学到的经验。

## 什么是 Skills？

Skills 是由说明、脚本和资源组成的文件夹，智能体可以发现并使用它们，从而更准确、更高效地完成任务。本文假设你已经熟悉 Skills 的基础知识；如果你是新手，请从我们的 [Skilljar 上的智能体技能入门课程](https://anthropic.skilljar.com/introduction-to-agent-skills)开始。

我们常听到一种对 Skills 的误解，认为它们「不过是 markdown 文件」。实际上它们是文件夹，可以包含脚本、素材、数据等，供智能体去发现、探索和操作。

在 Claude Code 中，Skills 还有[丰富多样的配置选项](https://code.claude.com/docs/en/skills#frontmatter-reference)，包括注册动态 hooks。

我们发现，Claude Code 中一些最有效的 Skills 正是充分利用了这些配置选项和文件夹结构。

## Skills 的类型

在为 Anthropic 内部所有 Skills 编目之后，我们发现它们聚集成九个类别。最好的 Skills 干净地落在其中一类；试图包办太多的 Skills 则横跨多类，会让智能体感到困惑。这并不是一份定论式清单，但对于发现你自己 Skills 库中的空白来说，是一个有用的框架。

Claude Code 团队对内部 Skills 做了归类，发现它们可以划分为九个不同的类别。

### **1. 库与 API 参考**

这类 Skills 解释如何正确使用某个库、CLI 或 SDK。它们既可能面向内部库，也可能面向 Claude Code 有时难以驾驭的常见库。这类 Skills 通常包含一个参考代码片段文件夹，以及一份 Claude 在编写脚本时应避开的坑（gotchas）清单。

例如：

- `billing-lib` — 你的内部计费库：边界情况、易踩的坑等
- `internal-platform-cli` — 内部 CLI 封装的每个子命令，附使用时机示例
- `sandbox-proxy` — 为开发工作配置你组织的出站网关：哪些主机可达、如何排查「connection refused」错误、如何添加允许列表条目

### **2. 产品验证**

这类 Skills 描述如何测试或验证你的代码确实在正常工作。它们通常与 playwright、tmux 或其他外部验证工具搭配使用。

在内部，验证类 Skills 对 Claude 输出质量的可衡量影响最大。让一位工程师花整整一周把你的验证 Skills 打磨到极致，可能是值得的。

可以考虑这样一些技巧：让 Claude 把它的输出录制成视频，让你能确切看到它测试了什么；或者在每一步都对状态做强制的程序化断言。这些通常通过在 Skill 中放入各种脚本来实现。

- `signup-flow-driver` — 在无头浏览器中跑通注册 → 邮箱验证 → 上手引导流程，带逐步断言状态的 hooks
- `checkout-verifier` — 用 Stripe 测试卡驱动结账 UI，验证账单确实落在正确的状态
- `tmux-cli-driver` — 用于交互式 CLI 测试，适合被验证对象需要 TTY 的场景

### **3. 数据获取与分析**

这类 Skills 连接你的数据和监控体系。它们可能包含带凭据获取数据的库、特定的仪表板 id 等，以及关于常见工作流或取数方式的说明。

- `funnel-query` — 「要看到 注册 → 激活 → 付费，我该 join 哪些事件」，外加真正存放规范 user_id 的那张表
- `cohort-compare` — 比较两个群组的留存或转化，标记统计显著差异，并链接到分群定义
- `grafana` — 数据源 UID、集群名称、问题 → 仪表板查找表
- `datadog` — 字段参考（@request_id 与 trace_id 的区别）、服务清单、指标前缀约定

### **4. 业务流程与团队自动化**

这类 Skills 把重复性工作流自动化为一条命令。它们通常只是相当简单的说明，但可能对其他 Skills 或 MCP 有较复杂的依赖。对这类 Skills 而言，把之前的结果保存到日志文件中有助于模型保持一致，并反思该工作流之前的执行情况。

- `standup-post` — 汇总你的工单系统、GitHub 动态和此前的 Slack 消息 → 生成格式化的站会汇报，只包含增量
- `create-<ticket-system>-ticket` — 强制 schema（合法枚举值、必填字段）加创建后的工作流（提醒审查者、在 Slack 里贴链接）
- `weekly-recap` — 合并的 PR + 关闭的工单 + 部署 → 格式化的周报

### **5. 代码脚手架与模板**

这类 Skills 为代码库中的特定功能生成框架样板代码。你可以把这些 Skills 与可组合的脚本搭配使用。当你的脚手架包含无法纯靠代码覆盖的自然语言要求时，它们尤其有用。

- `new-<framework>-workflow` — 按照你的注解生成新的服务/工作流/处理器脚手架
- `new-migration` — 你的迁移文件模板加常见注意事项
- `create-app` — 预先接好你的身份验证、日志和部署配置的全新内部应用

### **6. 代码质量与审查**

这类 Skills 在组织内部强制执行代码质量标准，并辅助代码审查。为了最大稳健性，其中可以包含确定性的脚本或工具。你可能希望把它们作为 hooks 的一部分自动运行，或放进 GitHub Action 里。

- `adversarial-review` — 派出一个全新视角的子智能体（subagent）来挑刺、落实修复、持续迭代，直到发现的问题降级为吹毛求疵
- `code-style` — 强制执行代码风格，尤其是 Claude 默认做不好的那些风格
- `testing-practices` — 关于如何写测试、该测什么的说明

### **7. CI/CD 与部署**

这类 Skills 帮助你在代码库内拉取、推送和部署代码。它们可能会引用其他 Skills 来收集数据。

- `babysit-pr` — 盯着一个 PR → 重试不稳定的 CI → 解决合并冲突 → 开启自动合并
- `deploy-<service>` — 构建 → 冒烟测试 → 结合错误率对比的渐进式流量放量 → 出现回归自动回滚
- `cherry-pick-prod` — 隔离的 worktree → cherry-pick → 冲突解决 → 用模板创建 PR

### **8. Runbook（运维手册）**

这类 Skills 接收一个症状（比如一条 Slack 讨论串、一条告警或一个错误签名），走完一套多工具的调查流程，并产出结构化报告。

- `<service>-debugging` — 为你流量最高的服务建立 症状 → 工具 → 查询模式 的映射
- `oncall-runner` — 拉取告警 → 排查常见嫌疑 → 汇总结论
- `log-correlator` — 给定一个请求 ID，从每一个可能经手过它的系统中拉取匹配的日志

### **9. 基础设施运维**

这类 Skills 执行例行维护和运维流程，其中一些涉及破坏性操作，需要防护栏（guardrails）兜底。它们让工程师在关键操作中更容易遵循最佳实践。

- `<resource>-orphans` — 找到孤立的 pod/卷 → 发到 Slack → 观察期 → 用户确认 → 级联清理
- `dependency-management` — 你组织的依赖审批工作流
- `cost-investigation` — 「为什么我们的存储/出站流量账单暴涨」，附带具体的存储桶和查询模式

## 制作 Skills 的技巧

确定了要做的 Skill 之后，该怎么写？以下是 Claude Code 团队制作 Skills 的一些最佳实践、技巧与窍门。

### 不要陈述显而易见的事

Claude 本来就会写代码，也能阅读你的代码库。一个只是复述 Claude 默认就会做的事情的 Skill，只会增加上下文而不增加价值。如果你发布的 Skill 以知识为主，请聚焦于那些能把 Claude 推出其常规思维方式的信息。

[前端设计 Skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) 就是一个绝佳例子；它由 Anthropic 的一位工程师通过与客户反复迭代打造，用来提升 Claude 的设计品味，避开 Inter 字体和紫色渐变这类经典俗套。

### 建一个「坑」清单（Gotchas）

任何 Skill 中信息密度最高的内容都是 Gotchas（坑）部分。这些部分应当从 Claude 使用你的 Skill 时常遇到的失败点逐步积累而来。理想情况下，你会随着时间推移不断更新 Skill，把这些坑记录下来。

例如：

「`subscriptions` 表是只追加的。你要的那一行是 version 最高的那行，而不是 `created_at` 最新的那行。」「这个字段在 API 网关里叫 `@request_id`，在计费服务里叫 `trace_id`。它们是同一个值。」「即使 Stripe webhook 实际上没有处理成功，staging 环境也会返回 200。去 `payment_events` 里查真实状态。」

### 善用文件系统与渐进式披露

SKILL.md 文件会指向另外几个文件，供 Claude 在特定情况下参考。例如，如果某个任务处于挂起状态，它就应该去参考 stuck-jobs.md。

正如我们前面所说，一个 Skill 是一个文件夹，而不只是一个 markdown 文件。你应该把整个文件系统视为一种上下文工程和渐进式披露（progressive disclosure）。告诉 Claude 你的 Skill 里有哪些文件，它就会在合适的时机去读取它们。

渐进式披露最简单的形式，就是指向其他 markdown 文件供 Claude 使用。例如，你可以把详细的函数签名和使用示例拆分到 `references/api.md` 中。

另一个例子：如果你的最终产出是一个 markdown 文件，可以在 `assets/` 里放一个模板文件供复制使用。

你可以建立 references、scripts、examples 等文件夹，帮助 Claude 更高效地工作。

### 不要把 Claude 框死在轨道上

Claude 通常会尽力遵循你的指令，而正因为 Skills 的可复用性如此之强，你要小心不要把指令写得太死。给 Claude 它需要的信息，同时给它根据具体情况灵活调整的空间。

### 想清楚初始化设置

上面的 Skill 就被写成在配置中未包含 Slack 频道时向用户询问。

有些 Skills 可能需要结合用户提供的上下文来完成初始设置。例如，如果你在做一个把站会汇报发到 Slack 的 Skill，你可能希望 Claude 询问要发到哪个 Slack 频道。

一个不错的模式是把这类设置信息存放在 Skill 目录下的 config.json 文件中，就像上面的例子一样。如果配置尚未设置，智能体就可以向用户询问信息。

如果你希望智能体以结构化的多选题形式提问，可以指示 Claude 使用 AskUserQuestion 工具。

### 为模型写描述，而不是为人

当 Claude Code 启动会话时，它会构建一份包含每个可用 Skill 及其描述的清单。Claude 正是扫描这份清单来判断「这个请求有没有对应的 Skill？」这意味着 description 字段不是摘要，而是对「何时触发这个 Skill」的描述。

在描述中写明 Skill 的触发词会很有帮助，比如「babysit」。

### 帮 Claude 记住

这个文本日志文件帮助 Claude 记住过去的事件，比如审查过 Sarah 的身份验证 PR。

有些 Skills 可以通过在其中存储数据来实现某种形式的记忆。你可以把数据存在任何足够简单的地方——一个只追加的文本日志文件或 JSON 文件——也可以复杂到用一个 SQLite 数据库。

例如，一个 `standup-post` Skill 可以维护一个 standups.log，记录它写过的每一次汇报。这样下次运行时，Claude 会读取自己的历史，并能说出从昨天以来发生了什么变化。

你可以使用环境变量 `${CLAUDE_PLUGIN_DATA}` 获得一个可持久存放数据的稳定目录，关于在 Skills 中持久化数据的更多信息见此：[https://code.claude.com/docs/en/plugins-reference#persistent-data-directory](https://code.claude.com/docs/en/plugins-reference#persistent-data-directory)。

### 存放脚本、生成代码

你能给 Claude 的最强大的工具之一就是代码。给 Claude 脚本和库，能让 Claude 把它的轮次花在组合与决策上——决定下一步做什么，而不是重新拼装样板代码。

例如，在你的 `data-science` Skill 里，可以有一个从事件源取数的函数库。为了让 Claude 完成复杂分析，你可以给它一组这样的辅助函数：

然后 Claude 就能即时生成脚本来组合这些功能，针对「周二发生了什么？」这样的提示完成更高级的分析。

### 按需启用的 hooks

Skills 可以包含仅在 Skill 被调用时才激活、且只在会话期间生效的 hooks。把这种机制用于那些你不想一直运行、但某些时候极其有用的强主张 hooks。

- **`/careful`** — 通过 Bash 上的 PreToolUse 匹配器拦截 rm -rf、DROP TABLE、force-push、kubectl delete。你只想在明知要碰生产环境时启用它——一直开着会把人逼疯。
- **`/freeze`** — 拦截任何不在指定目录内的 Edit/Write。调试时很有用：「我想加几行日志，却总在无意中『顺手修好』无关的代码。」

## 分发 Skills

Skills 最大的好处之一，就是可以分享给团队的其他成员。

与他人分享 Skills 有两种方式：

- 把你的 Skills 提交进仓库（放在 `./.claude/skills` 下）
- 制作一个**插件（plugin）**，并建一个 Claude Code Plugin marketplace，让用户可以上传和安装插件（详情见[文档](https://code.claude.com/docs/en/plugin-marketplaces)）

对于在相对较少的仓库上协作的小团队，把 Skills 提交进仓库就很好用。但每个提交进仓库的 Skill 都会给模型的上下文增加一点负担。随着规模扩大，内部插件市场让你能够分发 Skills，让团队自行决定安装哪些，还可以附带一个安装引导流程。

## 管理 Skills 市场

如何决定哪些 Skills 进入市场？大家如何提交？

在 Anthropic，我们没有哪个中心化团队来做决定；相反，我们尝试让最有用的 Skills 自然浮现。如果有人做了一个想让别人试用的 Skill，可以把它上传到 GitHub 上的沙箱文件夹，然后在 Slack 或其他论坛里告诉大家。

一旦某个 Skill 获得了一定的使用量（由 Skill 作者自行判断），就可以提交 PR 把它移入市场。

## 组合 Skills

你可能需要让 Skills 彼此依赖。例如，你也许有一个负责上传文件的 Skill，另一个生成 CSV 并上传的 Skill。这种依赖管理目前还没有内置于市场或 Skills 之中，但你可以直接按名称引用其他 Skills，只要它们已安装，模型就会调用它们。

## 度量 Skills

为了解某个 Skill 的使用情况，我们用一个 PreToolUse hook 在公司内部记录 Skill 的使用（[示例代码在此](https://gist.github.com/ThariqS/24defad423d701746e23dc19aace4de5)）。这样我们就能找出哪些 Skills 很受欢迎、哪些相对于我们的预期触发不足。

## 开始使用

Skills 的最佳实践仍在不断演进。我们最好的那些 Skills，大多起始于寥寥几行和一条注意事项，随后随着 Claude 撞上新的边界情况、大家不断补充而变得越来越好。

理解 Skills 的最好方式就是动手开始、多做实验，看看什么最适合你。

- 查看[我们的 Skills 文档](https://code.claude.com/docs/en/skills)
- [寻找可自定义的示例 Skills](https://github.com/anthropics/skills)

*本文由 Anthropic Claude Code 团队成员 Thariq Shihipar 撰写。*

FAQ（常见问题）
