---
title: "用 Codex 运行长时程任务"
title_en: "Run long horizon tasks with Codex"
source: https://developers.openai.com/blog/run-long-horizon-tasks-with-codex/
crawled: 2026-09-14
translated: 2026-09-14
---

# 用 Codex 运行长时程任务

> 原文：[Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex/) · OpenAI 开发者博客

2025 年 9 月，OpenAI 推出了 GPT-5-Codex，这是第一个针对智能体编程优化的 GPT-5 版本。2025 年 12 月，我们发布了 5.2，从那一刻起，人们开始相信使用自主编程智能体是可以做到可靠的。尤其是，我们看到模型能够可靠遵循指令的时长有了巨大跃升。

我想对这一阈值做一次压力测试。于是我给了 Codex 一个空白仓库、完全访问权限，以及一项任务：从零开始构建一个设计工具。然后我让它以 GPT-5.3-Codex「Extra High」推理强度运行。Codex 不间断运行了约 25 小时，消耗了约 1300 万 token，生成了约 3 万行代码。

这是一次实验，不是生产上线。但它在长时程工作真正重要的那些环节上表现出色：遵循规格说明、保持专注于任务、运行验证，以及在过程中修复失败。

## 一次长时程 Codex 会话是什么样子

我让 Codex 为会话数据生成一个摘要页面：

下面是 CLI 会话统计与 token 用量的一个视图：

这些截图很有用，因为它们让核心转变清晰可见：智能体编程日益关乎时间跨度（time horizon），而不再只是一次性的聪明。

## 真正的转变是时间跨度

这不仅仅是「模型变聪明了」。实际的变化在于：智能体能够在更长的时间内保持连贯、端到端地完成更大块的工作，并从错误中恢复而不丢掉主线。

METR 关于时间跨度基准的工作为这一趋势提供了一个有益的框架：前沿智能体能以约 50% 与 80% 可靠性完成的软件任务长度正在快速攀升，大约每 7 个月翻一倍。参见 [Measuring AI Ability to Complete Long Tasks (METR)](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)。

我们最近的 GPT-5.3-Codex [发布公告](https://openai.com/index/introducing-gpt-5-3-codex/)在两个方面进一步推动了智能体工作：

1. 它更擅长多步骤执行（计划 → 实现 → 验证 → 修复）。
2. 更容易在中途进行转向而无需重置整个运行（路线修正不会抹掉已有进展）。

我也受到了 Cursor 关于长时间运行自主编程系统文章的启发，包括他们的浏览器构建实验：[How Cursor built a web browser (Scaling agents)](https://cursor.com/blog/scaling-agents)。

Cursor 团队写道，OpenAI 模型「在长时间自主工作方面好得多：遵循指令、保持专注、避免漂移，以及精确而完整地实现事物」。

## 为什么 Codex 能在长任务中保持连贯

长时间运行的工作，关键不在于一个巨大的提示词，而在于模型所运行其中的智能体循环（agent loop）。

在 Codex 中，这个循环大致是：

1. 制定计划
2. 修改代码
3. 运行工具（测试/构建/lint）
4. 观察结果
5. 修复失败
6. 更新文档/状态
7. 重复

这个循环之所以重要，是因为它为智能体提供了：

- 真实反馈（错误、diff、日志）
- 外化的状态（仓库、文件、文档、worktree、输出）
- 随时间的可转向性（你可以根据结果进行路线修正）

这也是为什么 Codex 模型在 Codex 各界面上比在通用聊天窗口里表现感觉更好的原因：执行框架（harness）提供结构化上下文（仓库元数据、文件树、diff、命令输出），并执行一套有纪律的「何时算完成」例程。

我们最近发布了一篇[关于 Codex 智能体循环的文章](https://openai.com/index/unrolling-the-codex-agent-loop/)，其中有更多细节。

除此之外，我们还推出了 Codex 应用，让这个循环可以日常使用：

- [跨项目并行线程](https://developers.openai.com/codex/projects)（长时间的工作不会阻塞你的日常工作）
- [Skills](https://developers.openai.com/codex/build-skills)（将计划/实现/测试/报告标准化）
- [Automations](https://developers.openai.com/codex/automations/)（在后台处理例行工作）
- [Git worktrees](https://developers.openai.com/codex/environments/git-worktrees/)（隔离运行、保持 diff 可审阅、减少混乱折腾）

## 我为这次测试所做的设置

我为这次「实验」选择了一个设计工具，因为它是一个不留情面的测试：UI + 数据模型 + 编辑操作 + 大量边界情况。你糊弄不了它。如果架构错了，它很快就会崩溃。

我给 GPT-5.3-Codex 一份内容充实的规格说明，以「Extra High」推理强度运行，它最终不间断运行了约 25 小时，并能够保持连贯、交付高质量代码。模型还在它完成的每个里程碑上都运行了验证步骤（测试、lint、类型检查）。

## 关键思路：持久的项目记忆

最重要的技术是持久的项目记忆。我把规格说明、计划、约束和状态写在 markdown 文件里，Codex 可以反复回顾它们。这防止了漂移，并保持了「完成」定义的稳定。

仓库链接见下文，文件栈如下：

#### [Prompt.md](https://github.com/derrickchoi-openai/design-desk/blob/main/docs/prompt.md)（规格说明 + 交付物）

目的：冻结目标，避免智能体「构建出令人印象深刻但错误的东西」。

文件中的关键章节：

- 目标 + 非目标
- 硬性约束（性能、确定性、UX、平台）
- 交付物（完成时必须存在什么）
- 「何时算完成」（检查项 + 演示流程）

初始提示词告诉 Codex 把 prompt/spec 文件当作完整的项目规格说明，并生成一份基于里程碑的计划：

#### [Plan.md](https://github.com/derrickchoi-openai/design-desk/blob/main/docs/plans.md)（里程碑 + 验证）

目的：把开放式的工作变成一串智能体能够完成并验证的检查点。

- 里程碑足够小，能在一个循环内完成
- 每个里程碑都有验收标准 + 验证命令
- 停下修复规则：如果验证失败，先修复再继续
- 决策记录，避免来回摇摆
- 代码库的预期架构

*请注意，我们最近为 Codex 应用、CLI 与 IDE 扩展加入了原生的计划模式（plan mode）。它有助于在动手修改之前，把较大的任务拆解成清晰、可审阅的步骤序列，让你可以提前就方法达成一致。如果还需要进一步澄清，Codex 会提出追问。要开启它，请使用 /plan 斜杠命令。*

#### [Implement.md](https://github.com/derrickchoi-openai/design-desk/blob/main/docs/implement.md)（引用计划的执行指令）

目的：这是操作手册（runbook）。它确切地告诉 Codex 如何运作：遵循计划、保持 diff 范围受控、运行验证、更新文档。

- 计划 markdown 文件是唯一事实来源（逐个里程碑推进）
- 每个里程碑之后运行验证（立即修复失败）
- 保持 diff 范围受控（不要扩大范围）
- 持续更新文档 markdown 文件

#### [Documentation.md](https://github.com/derrickchoi-openai/design-desk/blob/main/docs/documentation.md)（交付过程中的状态 + 决策）

目的：这是共享记忆与审计日志。正因如此，我才能离开几个小时，回来仍然明白发生了什么。

- 当前里程碑状态（什么已完成、接下来做什么）
- 已做的决策（以及为什么）
- 如何运行 + 演示（命令 + 快速冒烟测试）
- 已知问题 / 后续事项

以下是这次运行期间里程碑验证实际的样子：

### 每个里程碑都做验证

Codex 不是写完代码就祈祷它能用。每个里程碑之后，它都会运行验证命令，并在继续之前修复失败。

下面是指示它使用的质量命令示例：

以及一个 Codex 在 lint 失败后修复问题的例子：

## 智能体构建了什么

结果并不完美，也谈不上生产可用，但它是真实且可测试的。这次运行的标准不是「它能编译」，而是「它是否遵循了指令？它真的能用吗？」

实现的高层能力：

1. 画布编辑（画框、分组、形状、文本、图片/图标、按钮、图表）
2. 实时协作（在线状态、光标、选区、跨标签页同步编辑）
3. 检查器控件（几何、样式、文本）
4. 图层管理（搜索、重命名、锁定/隐藏、重新排序）
5. 参考线/对齐/吸附
6. 历史快照 + 恢复
7. 重放时间线 + 从先前某个时点分叉
8. 原型模式（热区 + 流程导航）
9. 评论（可置顶的讨论串，支持解决/重开）
10. 导出（保存/导入/导出 + 通过 CLI 导出到 JSON 与 React + Tailwind）

## 长时程 Codex 任务的经验总结

让这次运行成功的不是某一条聪明的提示词，而是以下要素的组合：

- 清晰的目标与约束（spec 文件）
- 带验收标准的检查点式里程碑（`plans.md`）
- 说明智能体应如何运作的操作手册（`implement.md`）
- 持续验证（测试/lint/类型检查/构建）
- 实时的状态/审计日志（`documentation.md`），让整个运行始终可检查

这就是长时程编程工作正在走向的方向：更少的看管，更多带护栏的委托。

## 在你自己的长时程任务上试试 Codex

这次 25 小时的 Codex 运行，预示了用代码构建软件的未来走向。我们正在超越一次性提示词和紧密的结对编程循环，迈向能够端到端承担一段真实工作的长期队友——你在里程碑处掌舵，而不是微观管理每一行代码。

我们在 Codex 上的方向很简单：更强的队友行为、与你真实上下文更紧密的集成，以及让工作可靠、可审阅、易于上线的护栏。我们已经看到，当智能体接管了例行的实现与验证，开发者的速度变得更快，人类得以解放出来去做最重要的部分：设计、架构、产品决策，以及那些没有模板可循的全新问题。

这一切不会止步于开发者。随着 Codex 在捕捉意图与提供安全脚手架（计划、验证、预览、回滚）方面越来越好，更多非开发者也将能够在不驻留 IDE 的情况下构建并迭代。Codex 各界面与模型方面还有更多即将到来，但北极星始终未变：让智能体感觉不像一个需要你时刻看管的工具，而更像一个在长时程工作中值得信赖的队友。

如果你想亲自尝试，可以从这里开始：

- [Codex 概览](https://developers.openai.com/codex/)
- [Codex 快速上手](https://developers.openai.com/codex/quickstart/)
- [Codex 模型](https://developers.openai.com/codex/models/)
- [Codex 功能](https://developers.openai.com/codex/features/)
