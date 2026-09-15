---
title: "Claude Tag 如何担任 Anthropic CI/CD 故障的第一响应者"
title_en: "How Claude Tag serves as Anthropic’s first responder for CI/CD failures"
source: https://claude.com/blog/ai-ci-cd-on-call/
crawled: 2026-09-14
translated: 2026-09-14
---

# Claude Tag 如何担任 Anthropic CI/CD 故障的第一响应者

> 原文：[How Claude Tag serves as Anthropic’s first responder for CI/CD failures](https://claude.com/blog/ai-ci-cd-on-call/) · Claude 博客

[*用我们的安装套件搭建你自己的 Claude 值班系统*](https://github.com/anthropics/oncall-kit)*。*

## 面向 CI/CD 的 AI 事故响应：在 Anthropic，Claude 随时待命

几周前的一个晚上 10 点，我正在值班，同事在 Slack 上给我发来消息：某个新服务上大约 44 个测试没有触发。

换作过去，我会停下手里的事，坐到笔记本电脑前，疲惫地叹口气，开始一个长达一小时的排查修复流程。但现在，我的工作流完全不同了：我把 @Claude 拉进来，问它看到了什么。

在这个案例中，Claude 发现这些测试是在当天上午某个功能开关（feature flag）被打开后消失的，并且回滚是安全的。我让同事回滚了这个开关。3 分钟后，Claude 在 Slack 上 ping 我，确认跳过规则确实已被移除、错误率已回到基线水平。

（为清晰起见，根据一次真实交流重新整理。）

过去几个月里，Claude Tag 一直是 Anthropic CI/CD 故障的值班第一响应者。这不仅改善了我们的社交生活，也让每一次 CI 事故都拥有一个即时的第一响应者：在近期每一起有情况报告的事故中，第一份报告都出自 Claude 之手，**通常在 15 分钟内就发布第一份分析。**

在本文中，我们会带你走一遍我们构建的东西及其工作原理，让你也能亲手搭建，从此不再害怕轮到自己值班。

## **我们的 Claude 值班配置**

在深入事故响应流程的各个阶段之前，我先在这里给出整体概览，让你在了解细节时心中有全局。

一个值班智能体需要**记忆**，以记住已经做过什么；需要**连接与访问权限**，以便调查、理解并采取行动；需要**日程安排**，知道何时该重新投入工作；还需要**指令**，知道该做什么。

[Claude Tag](https://claude.com/product/tag) 是我们值班智能体的主干。Claude Tag 在我们的值班 Slack 频道中保持记忆，并提供在事故期间逐轮下达指令的界面。Claude 还会实时响应值班频道及其他频道中的事件。例行任务（routines）——即 Claude 定期执行的动作——的调度也在这个频道上进行，只需自然语言提示，例如"每周一美国东部时间上午 9:00 运行 CI 交接"。

[Claude Tag 拥有自己的服务账户](https://claude.com/blog/agent-identity-access-model)，并有权访问 Anthropic CI 工程师所需的工具，如 Datadog 或 Grafana。这些由管理员为该频道一次性配置完成（[配置方法在此](https://claude.com/docs/claude-tag/admins/setup-overview#choose-which-tools-to-connect)）。

除了值班频道，我们还让 Claude 关注其他相关频道——这些频道同样有 Claude Tag 作为成员——以便它获取额外的上下文，例如服务告警、配置变更或 PR 更新。

长期指令以技能（Skills）的形式存放在 markdown 文件中，提交在 GitHub 仓库里。这样多位队友可以对它们持续迭代，我们也能像管理代码一样管理变更。其中还包括关键信息，例如路由指令、策略，以及作为自我改进回路一部分的经验教训日志。

这套配置花了我们几个小时，而不是几天。我们在 GitHub 上创建了一个通用的[值班安装套件（on-call setup kit）](https://github.com/anthropics/oncall-kit)，可以帮助你启动类似的智能体。它会把你们团队自己的事故历史转化为分诊手册（playbook），并在你们的事故频道里留下一个只读的 Claude，负责诊断、上报和学习。[你可以在大约十分钟内](https://github.com/anthropics/oncall-kit/blob/main/test-fixtures/RUNBOOK.md)看着它在一个虚构团队的历史数据上运行。

以 TL;DR 的方式总结步骤：

- 你需要一个 [Claude Team 或 Claude Enterprise](https://support.claude.com/en/collections/9387370-team-and-enterprise-plans) 方案
- 组织所有者需要通过 Claude Tag 把 Claude 加入值班 Slack 频道
- 组织所有者还需要协助把值班 Slack 频道中的 Claude 连接到相应的连接器（connectors）、GitHub 仓库，并设置 [Claude Code Remote](https://code.claude.com/docs/en/remote-control)。
- 把 Claude 加入你的事故频道，指示它监控事故并立即分诊

现在，让我们深入看看这场变革在事故的每个阶段分别是什么样子。

## **检测**

Claude 改变的不只是你响应事故的方式，它首先改变的是你发现事故的方式。此前，事故检测存在两种主要的失败模式。

人类很难始终都有先见之明，为每条规则设定完美的阈值。在数据不足以分析流量模式时尤其困难。

为此，我们让 Claude 在新服务上线后的头几天分析数据和涌入的告警，据此建议补充规则，并微调那些过宽或过窄的规则。

事故检测的第二种主要失败模式是告警疲劳：逐条检查和核实每条触发的告警非常枯燥。而 Claude 不会像人类那样感到疲劳。

Claude 监控每个告警频道中的每一条相关告警，并按照[根目录 oncall.md 文件](https://github.com/anthropics/oncall-kit/blob/main/templates/ONCALL.md)中的标准判断：是可以等到明天早上，还是需要立即呼叫值班人员。例如，经过数据分析调优后，文件中的某条规则可以是："如果错误率超过 2% 且持续超过 5 分钟，并且不在已知的部署窗口内，则呼叫值班人员，否则写入 lessons.md。"

Claude 值班告警流程还有另外两种触发方式：

- CI 团队的成员可以在值班频道中报告问题，就像开篇 44 个测试失踪的例子那样；或者
- 公司任何人都可以通过内部页面发起事故。如果它被标记为 CI 基础设施事故，就会为该事故创建一个 Slack 频道，我们的值班 Claude 会接手处理。

这里的关键在于：告警流程是确定性的，而值班升级既有确定性路径，也有智能体化（agentic）路径。

## **分诊**

让 Claude 过滤告警噪声是一回事，真正的节省来自调查。从事故开启算起，Claude 发布第一份基于证据的分析的中位时间是 14 分钟；最快的情形下，它在第一份报告里就能在 4 分钟内指出根本原因。

当一条告警升级为事故时，Claude 通常已经在我们的 Slack 频道里准备好了可以审阅的、有证据支撑的假设。Claude Tag 会启动一个[动态工作流](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code)，由一个编排智能体（orchestration agent）派生出执行者子智能体（executor subagent），分别调查每一处依赖和每一条事实来源。

对我们来说，那就是 Grafana、我们的日志存储、PagerDuty、GitHub、Kubernetes 和 Slack 事故频道——全部通过 [MCP Connectors](https://code.claude.com/docs/en/mcp) 接入。Claude 可以并行追查多条线索，帮助缩短 MTTR（平均恢复时间）。

执行者把发现汇报给编排智能体，由它综合整理，并以一份条理清晰的 SITREP（情况报告）呈现出来。

编排者和执行者智能体并非盲目搜索。它们受一套调查技能（investigation skill）的指引，[每种缺陷类别都配有更详细的参考 markdown 文件](https://github.com/anthropics/oncall-kit/tree/main/skills/triage)。

例如，一份 617 行的调查技能针对影子分歧（shadow divergence）类缺陷，编码了我在一次典型调查中采取的每一个步骤。它是我在一起事故中与 Claude 逐轮排查后，让它根据这段经历创建的。

lessons.md 也在引导 Claude 的排障过程。这个 markdown 文件是我们解决的每一起事故的滚动日志：发生了什么、根本原因、修复方法，以及值得记住的坑。Claude 会自动向其中追加内容。每一次新的调查都从阅读它开始，因此 Claude 的第一个假设是从最近发生过什么起步的。

如果同一个模式出现了足够多的次数，我们就把它晋升到调查技能本身。我最喜欢的一条记录是 Claude 写的关于我的：我曾经在没看指标之前就从配置文件里做了假设，现在 lessons.md 里写着："先查数据，再做理论。配置告诉你可能出什么问题；指标告诉你实际出了什么问题。"

即便有这些工具和上下文，Claude 也不总是第一次就答对。人类的直觉和经验依然重要。Claude Tag 让团队能以多人模式共同排障：我们任何一个人都可以实时引导调查方向或补充假设，一起协作。

（为清晰起见，根据一次真实对话重新整理。）

## **解决**

如果 Claude 能升级和排查告警，它能不能顺手修好？答案因团队而异，以下是我们的做法。

我们团队的大多数部署都在功能开关之后进行。我在 Claude Code 中创建了一个独立的智能体，它拥有我的权限，能够针对这些功能开关执行渐进式部署。

我们发布流程的第一阶段通常由 Claude 管理金丝雀流量、监控问题，并自动调高或调低某个功能开关。这本身可以单独成文，我就不在这里展开了。

Claude Tag 帮助我们团队的其他解决路径还有：

- 提醒我们是否需要清空（drain）或封锁（cordon）Kubernetes 集群的某些部分；
- 告诉我们如何扩容部分基础设施以应对需求激增（这种情况很少见，但当 Claude 准确带回我们能为缓解问题做些什么时非常有帮助）；以及最常见的，
- 以 PR 形式提交修复，由值班人员评审、合并再部署，快速了结问题。

## **验证、沟通与交接**

Claude 使用调查阶段用过的同一批 MCP Connectors 和工具来验证修复是否达到预期。作为 oncall.md 中长期指令的一部分，它会撰写一份事故复盘（post-mortem）写入 lessons.md，并写成交接用的 SITREP。

为了在多起事故之间传达全局图景，我们创建了一个名为 ci-weather 的智能体。它汇总每个事故 Slack 频道的信息、构建指标、合并队列统计和部署延迟，然后以新闻编辑室风格的报告发布到一个公司所有人都能阅读的公共频道。现在，工程师们想判断该不该暂缓合并，或想弄清"CI 到底怎么了"时，会直接去看那个频道，而不是来 ping 我们。

说句实话：我们迭代了好几版报告格式。Claude 可以一次性写出生成状态报告的技能，但让报告真正可读的，是团队特有的品味。这是人与人之间的沟通，不是管道工程。

最后，虽然 Claude 在 lessons.md 里为自己记日志，我们也希望每周一为人类产出交接报告。Claude 会生成每日和每周摘要，让团队的一名成员能接着另一名成员的工作继续。

## **从监控事故到监控事故响应系统**

我们的软件工程师平均[每季度交付的代码量是 2021 至 2025 年的 8 倍](https://www.anthropic.com/institute/recursive-self-improvement)。虽然我们始终把质量标准定得很高（每个 PR 都有指定的负责人，每处变更都必须经过批准才能合并，每处变更都要通过同一套 CI 门禁），但跟上智能体编码（agentic coding）步伐的唯一办法，就是智能体化的 CI。

Claude 吸收了我工作中最枯燥的部分——下班后的打扰和事故沟通——让我得以专注于那些真正提升系统可靠性的中长期架构改造。

我们所构建的东西最棒的一点，是它让人感觉并不零散。我们的值班流程本来就活在 Slack 里，而现在，Claude 也加入了这个频道。

如何开始：

*本文由 Anthropic 技术成员 Sachin Malhotra 撰写，Anthropic 员工 Michael Segner 参与贡献。*

FAQ（常见问题）
