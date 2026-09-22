---
title: "Grok Build 中的 Workflows"
title_en: "Workflows in Grok Build"
date: 2026-07-23
source: https://x.ai/news/workflows
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok Build 中的 Workflows

> 原文：[Workflows in Grok Build](https://x.ai/news/workflows) · xAI

[返回新闻列表](/news)

2026 年 7 月 23 日

Grok Build 现在可以编写并运行工作流（workflow）：一种编排脚本，能把一个任务分发给数百个并行智能体、验证结果，并在一次后台运行中汇总报告。

---

`$ curl -fsSL https://x.ai/cli/install.sh | bash`

[免费试用](/cli)

Grok Build 现在可以运行 **workflows** 了：用平实的语言描述一个大任务，Grok 会规划它、在后台把它分发给数百个并行智能体，并在一切完成后向你汇报。期间你的会话始终空闲。

~/dev/relay

|8.42%|

❯can you create and run a workflow to review https://github.com/acme-corp/relay/pull/4821

─Workflows─

[✗]

⋅pr-review0/0 agents · agents 0/128 (128 left) · 12s

Multi-subagent GitHub PR review: fetch context, fan out specialist reviewers, adversarially verify findings, synthesize a ranked report

Phases

❯1Context

2Review

3Verify

4Synthesize

Context · 0 agents

↑↓ phase · enter agent│p pause│x stop│s save│esc close

Grok 4.5click to replay

## [什么时候该用工作流](#when-to-use-a-workflow)

工作流为单个对话装不下的复杂、多面任务而生：审查一个大 PR 里的每一项功能、分诊最近 100 个 issue、对代码库做某一类 bug 的审计。如果工作能拆成许多独立的部分，并且最终应产出一份清晰的报告，那就请求一个工作流。

## [工作原理](#how-it-works)

Grok 会把任务规划成一个小脚本：工作的各个阶段、每个阶段中的智能体，以及它们的结果如何逐级汇总。每个智能体都从干净、聚焦的上下文启动，而且计划中可以内置单次执行做不到的检查——比如让独立的「怀疑者」在每条结论进入最终报告前先行验证。

每次运行的智能体预算为 128 个，大型任务最多可达 1,024 个。进度随运行实时保存，暂停和恢复绝不会重做已完成的工作。运行 `/workflows` 可以逐阶段实时观看，还能看到每个智能体的 token 计数。

## [保存与复用工作流](#saving-and-reusing-workflows)

Grok 根据你的请求撰写工作流、启动前先做冒烟检查，并在多次运行之间持续改进；你从不需要亲手写脚本。哪个好用了就留下来：放在 `.grok/workflows/` 里的工作流会与你的团队共享，放在 `~/.grok/workflows/` 里的则跟着你走遍任何项目。每个保存的工作流都会变成自己的斜杠命令并接受参数——只要你留下了上面演示中的 PR 审查，下一次审查就只是 `/pr-review 5137`。

`/deep-research` 为内置命令：它把研究问题分发给并行调查员，对每条论断逐一核对来源，并返回一份带引用的报告。

## [今天就试试](#try-it-today)

一些可以尝试的例子：

- 「用工作流审查这个 PR 里的每一项功能」
- 「分诊最近 100 个 Linear issue，给我一份前十的行动清单」
- 「审计每一个路由处理器是否缺少鉴权检查，并逐条验证发现的问题」

`$ curl -fsSL https://x.ai/cli/install.sh | bash`

[免费试用](/cli)
