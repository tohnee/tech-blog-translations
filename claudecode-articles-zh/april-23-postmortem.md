---
title: "关于近期 Claude Code 质量报告的更新"
title_en: "An update on recent Claude Code quality reports"
source: https://www.anthropic.com/engineering/april-23-postmortem
published: 2026-04-23
crawled: 2026-09-11
translated: 2026-09-11
---

# 关于近期 Claude Code 质量报告的更新

> 原文：[An update on recent Claude Code quality reports](https://www.anthropic.com/engineering/april-23-postmortem) · Anthropic Engineering Blog

过去一个月，我们一直在调查部分用户反馈的「Claude 回答质量变差」问题。我们把这些问题追溯到了三项彼此独立的变更，它们影响了 Claude Code、Claude Agent SDK 和 Claude Cowork。API 未受影响。

截至 4 月 20 日（v2.1.116），这三个问题均已解决。

在本文中，我们解释我们发现了什么、修复了什么，以及我们将如何改变做法以确保类似问题再次发生的可能性大大降低。

我们非常重视关于质量下降的报告。我们从不故意降低模型质量，并且我们能够立即确认 API 和推理层未受影响。

经过调查，我们确定了三个不同的问题：

1. 3 月 4 日，我们把 Claude Code 的默认推理力度（reasoning effort）从 `high` 改为 `medium`，以缩短部分用户在 `high` 模式下遇到的极长延迟——长到让 UI 看起来像卡死。这是一个错误的取舍。在用户告诉我们他们更希望默认更高智能、并为简单任务主动选择低力度之后，我们于 4 月 7 日撤销了这一变更。这影响了 Sonnet 4.6 和 Opus 4.6。
2. 3 月 26 日，我们发布了一项变更：清空闲置超过一小时的会话中 Claude 较早的思考内容，以降低用户恢复这些会话时的延迟。一个 bug 导致它在会话的其余部分每一轮都持续发生，而不是只发生一次，这让 Claude 显得健忘而重复。我们于 4 月 10 日修复。这影响了 Sonnet 4.6 和 Opus 4.6。
3. 4 月 16 日，我们在系统提示中加入了一条降低冗长度的指令。与其他提示变更叠加后，它损害了编码质量，于 4 月 20 日撤销。这影响了 Sonnet 4.6、Opus 4.6 和 Opus 4.7。

因为每项变更在不同的时间表上影响不同的流量切片，汇总效果看起来像大范围、不一致的质量劣化。虽然我们从 3 月初就开始调查相关报告，但起初它们很难与用户反馈的正常波动区分开，而且无论是我们的内部使用还是评估，最初都无法复现所发现的这些问题。

这不是用户应当从 Claude Code 得到的体验。自 4 月 23 日起，我们为所有订阅用户重置用量限额。

## Claude Code 默认推理力度的变更

2 月在 Claude Code 中发布 Opus 4.6 时，我们把默认推理力度设为 `high`。

不久之后，我们收到用户反馈：high 力度模式下的 Claude Opus 4.6 偶尔会思考过久，导致 UI 看似冻结，并给这些用户带来不成比例的延迟和 token 用量。

一般而言，模型思考越久，输出越好。力度档位是 Claude Code 让用户设置这一取舍的方式——更多思考 versus 更低延迟、更少触碰用量上限。在为模型校准力度档位时，我们会考虑这一取舍，在测试时计算曲线上挑出能给用户最佳选项范围的点。在产品层，我们再选择曲线上哪个点作为默认值——这就是我们发给 Messages API 的 effort 参数值；其他选项则通过 `/effort` 提供。

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fde3bcf9733b61f57234d8c45e663b1bd48677ea1-3840x2160.png&w=3840&q=75)

在我们的内部评估与测试中，medium 力度在大多数任务上以显著更少的延迟换取略低的智能。它也没有偶发性超长思考尾延迟的问题，还能帮助用户最大化用量限额。于是我们发布了把 medium 设为默认力度的变更，并通过产品内对话框解释了理由。

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F459b2a8a0baa88937eebcbe4566dde4d6cc7f185-3794x2260.png&w=3840&q=75)

发布后不久，用户开始反馈 Claude Code 变「笨」了。我们发布了多个设计迭代，让当前力度设置更醒目，提醒人们可以修改默认值（启动时通知、内联力度选择器，以及恢复 ultrathink），但大多数用户仍保持 medium 默认值。

在听取更多客户反馈后，我们于 4 月 7 日撤销了这一决定。现在所有用户对 Opus 4.7 默认 `xhigh` 力度，对其余所有模型默认 `high` 力度。

## 丢弃先前推理的缓存优化

当 Claude 对一个任务进行推理时，这些推理通常保留在对话历史中，这样在随后的每一轮，Claude 都能看到自己为什么做出那些编辑和工具调用。

3 月 26 日，我们针对该功能发布了一项本意是提效率的改进。我们用提示缓存让用户连续的 API 调用更便宜、更快。Claude 发起 API 请求时把输入 token 写入缓存；一段时间不活动后，提示被逐出缓存，为其他提示腾地方。缓存利用率是我们精心管理的东西（详见我们关于[方法](https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything)的文章）。

设计本应很简单：如果会话闲置超过一小时，我们可以通过清除旧的思考段来降低用户恢复会话的成本。反正该请求必然缓存未命中，我们可以从请求中裁掉不必要的消息，减少发送给 API 的未缓存 token 数量。然后恢复发送完整的推理历史。为此我们使用了 `clear_thinking_20251015` API 头并配合 `keep:1`。

实现里有个 bug。它没有只清除一次思考历史，而是在会话剩余的每一轮都清除。会话一旦越过闲置阈值，该进程剩余的每个请求都会告诉 API 只保留最近一块推理、丢弃之前的一切。这会滚雪球：如果你在 Claude 正在执行工具调用的中途发了一条后续消息，那会在坏标志下开启新的一轮，连当前轮的推理也被丢弃。Claude 会继续执行，但越来越不记得自己为什么选择做正在做的事。这就是用户报告的健忘、重复和奇怪的工具选择。

由于它会从后续请求中持续丢弃思考块，这些请求也导致缓存未命中。我们相信这正是「用量限额消耗快于预期」这类独立报告的成因。

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F332d9c487bb73c8078686068dcbe1b616720a8dd-3016x1198.png&w=3840&q=75)

两个不相关的实验让我们起初难以复现该问题：一个仅限内部的消息排队服务端实验；以及一个关于思考展示方式的无关联改动，它在大多数 CLI 会话中掩盖了这个 bug，因此即使测试外部构建版我们也未能发现。

这个 bug 位于 Claude Code 的上下文管理、Anthropic API 和扩展思考的交叉点。它引入的改动通过了多道人工与自动化代码评审，以及单元测试、端到端测试、自动化验证和内部吃狗粮。加上它只在一个角落案例（陈旧会话）中出现、且难以复现，我们花了超过一周才发现并确认根本原因。

作为调查的一部分，我们用 Opus 4.7 对涉事的 pull request 做了 [Code Review](https://code.claude.com/docs/en/code-review) 回溯测试。在提供了收集完整上下文所需的代码仓库后，Opus 4.7 找到了这个 bug，而 Opus 4.6 没有。为防止此类问题再次发生，我们正在落地对代码评审使用附加仓库作为上下文的支持。

我们于 4 月 10 日在 v2.1.101 中修复了这个 bug。

## 一项降低冗长度的系统提示变更

我们最新的模型 Claude Opus 4.7 相对其前任有一个显著的行为怪癖：正如我们在发布时[所写](https://www.anthropic.com/news/claude-opus-4-7)，它相当啰嗦。这让它在难题上更聪明，但也产生更多输出 token。

在发布 Opus 4.7 前几周，我们开始为它调优 Claude Code。每个模型的行为都略有不同，我们在每次发布前都会花时间为它优化 harness 与产品。

我们有一系列降低冗长度的工具：模型训练、提示，以及改进产品中的思考 UX。最终我们用上了所有这些，但系统提示中的一处添加对 Claude Code 的智能造成了超乎预期的影响：

> *“Length limits: keep text between tool calls to ≤25 words. Keep final responses to ≤100 words unless the task requires more detail.”*

经过数周内部测试、且在我们运行的一组评估中没有退化后，我们对这项变更有信心，并于 4 月 16 日随 Opus 4.7 一起发布。

作为本次调查的一部分，我们用更广的一组评估运行了更多消融实验（从系统提示中逐行移除以理解每行的影响）。其中一个评估显示 Opus 4.6 和 4.7 都下降 3%。我们立即在 4 月 20 日的发布中撤销了这条提示。

## 今后

为避免这些问题，我们将做出几项改变：我们会确保更大比例的内部员工使用与公众完全一致的 Claude Code 构建（而非我们用于测试新功能的版本）；我们会改进内部使用的 [Code Review](https://code.claude.com/docs/en/code-review) 工具，并把改进版发布给客户。

我们还会对系统提示变更施加更严格的控制。对 Claude Code 的每一次系统提示变更，我们都会运行广泛的按模型评估套件，持续进行消融实验以理解每行的影响，并且我们已构建新工具让提示变更更易评审与审计。我们还向我们的 CLAUDE.md 添加了指引，确保针对特定模型的变更只对该模型生效。对于任何可能与智能做交换的变更，我们将加入浸泡期（soak period）、更广的评估套件和渐进式发布，以便更早发现问题。

我们最近在 X 上创建了 @ClaudeDevs，为我们提供空间深入解释产品决策及其背后的理由。我们也会在 GitHub 的集中帖子里分享同样的更新。

最后，我们要感谢我们的用户：那些用 `/feedback` 命令向我们反馈问题的人（以及在网络上发布具体、可复现示例的人），正是他们让我们最终得以发现并修复这些问题。今天我们正在为所有订阅用户重置用量限额。

我们无比感谢你们的反馈与耐心。
