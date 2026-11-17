---
title: "在前沿工作：Cognition 为何信任 Claude Fable 5 彻夜工作"
title_en: "Working at the frontier: How Cognition trusts Claude Fable 5 to work through the night"
date: 2026-07-10
source: https://claude.com/resources/articles/working-at-the-frontier-how-cognition-trusts-claude-fable-5-to-work-through-the-night
crawled: 2026-11-17
translated: 2026-11-17
---

# 在前沿工作：Cognition 为何信任 Claude Fable 5 彻夜工作

> 原文：[Working at the frontier: How Cognition trusts Claude Fable 5 to work through the night](https://claude.com/resources/articles/working-at-the-frontier-how-cognition-trusts-claude-fable-5-to-work-through-the-night) · Claude 博客

*Cognition 研究高级副总裁 Silas Alberti 在该公司自家的 AI 软件工程师 Devin 中测试过几乎每一个 Claude 模型。Claude Fable 5 是他第一个愿意让它整夜跑下去的模型。*

Cognition 即便以硅谷的标准来衡量也很年轻。它在 2024 年初打造了自己的自主 AI 软件工程师 Devin，当时智能体的基本机制才刚刚勉强站得住脚。

Devin 接手的是工程师们始终抽不出手去做的工作：[代码库迁移](https://claude.com/resources/articles/ai-code-migration)、积压的 bug、一再被推迟的功能。客户从高增长初创公司到《财富》500 强企业不一而足，标准也因此很高。Devin 写的代码必须可靠、可以直接上生产；一个悄悄引入的小 bug 就可能在后续环节造成真正的问题。

Alberti 的团队负责训练和测试 Devin 背后的模型，几乎从最早开始就运行过每一代 Claude。他把第一次真正的跃迁追溯到 2024 年底的 Claude 3.6 Sonnet——那是第一个能够可靠地串联工具、并保持多步骤任务连贯性的模型。当团队把它接入 Devin 后，内部使用量增长到了原来的三倍。

正是这段历史让他很难被打动。Cognition 见过太多次模型在基准测试上表现优异、然后在工程师真正上手的那一刻崩塌。"这种事我们被坑过很多回了，"Alberti 说。所以团队信任自己的工程师胜过任何分数。最有品味的开发者会让每个新模型经历真实的一天工作，标准就是：它写出的代码他们是否真的愿意保留。

用 Alberti 的话说："我们不信任何评估。"

## 早期模型的天花板在哪里

尽管进步如此之大，仍有一道天花板横在那里：一个智能体在失去任务主线的连贯性之前，究竟能跑多久？

"在 Fable 之前，你可以委派智能体去做一件事，它能保持专注几分钟，也许一小时，"Alberti 说。再往后，会话就开始飘移了。让早期模型同时权衡五个想法，它就会跟丢线索、陷入混乱。在一次数据库迁移中，先前的一个 Opus 模型从技术上讲完成了任务，但一路引入了一系列隐蔽的 bug。

事故分诊呈现出同样的形态。早期模型倾向于停留在日志的表面，而不是深挖到相关的那一行；而且它们被训练成无论如何都要给出答案——于是它们会"自信地宣称自己发现的第一件看似合理的事，然后停下"。工程师们学会了不去理会它们。

![](https://assets.claude.com/aba77cdcbd02f2d3747def7ee6ab3bffea6d5e0b.jpg)

Cognition 用一系列基准测试来评估前沿模型，其中包括 Frontier Code。

## Claude Fable 5 通过了 Cognition 自己的标准

Cognition 用 Frontier Code 给模型打分——这是他们自建的基准，因为现有基准总是在奖励那些能通过测试、却活不过真实代码库的代码。Alberti 称其为"反劣质产出（anti-slop）"的标准。在其最难的子集上，先前的 Opus 模型得分约为 10%，Claude Fable 5 则约为 30%。

团队的第一反应是怀疑。"是不是有 bug？这不可能是真的。"通常基准分数的跃升会伴随着工程师们长达数周的争论：这个模型在实践中真的更好吗？但这一次，内部试用与数字得出了同样的结论。"说实话，这挺让人震惊的，"Alberti 说。

"我们注意到的最重要的一点是它的时间跨度，它能自主运转多久，"他说。"有些任务，我正准备去睡觉，心里想，'好吧，请你就继续干，别停，直到我醒来。'然后我醒了，它已经连续工作了八个小时，而且确实在取得实质进展。这我以前没见过。"

时间跨度之所以撑得住，是因为 Claude Fable 5 在杂乱的上下文中依然保持头脑清醒。它是第一个能正确使用 Cognition 内部调试工具的模型——在浏览器里逐页翻看日志，并在一片噪声中得出结论。在一次曾让早期模型栽跟头的迁移中，它先声明自己将坚守的不变量，然后严格按这些不变量执行。在分诊中，它锁定了根因，并说明了自己不知道什么——Alberti 说，后者恰恰才是真正重建信任的东西。

他把这次跃迁归入少见的真正阶跃式变化之列，那种大约一年才出现一次的跃迁。

![](https://assets.claude.com/b18dad0104113d740bdaeed8459dacb01a522c5b.jpg)

Silas 和他的团队正在构建 Devin，由 Claude 等模型驱动，以应对更复杂、运行时间更长的工作负载。

## 下一步

Cognition 创立时的赌注是：智能体应当在云端一次连续运行数小时。在公司成立的第一年里，模型还达不到这个要求。

Alberti 说，Claude Fable 5 让这一赌注的完整版本变得可行，其中一部分已经体现在产品中。Devin 可以盯着一个 Slack 频道，无需被 @ 就主动介入某个 issue；也可以监控生产环境，自行对突发异常做分诊。当它把这类事情做对时，他说，感觉"就像团队里有一位真正的工程师"。

他预计这将成为工程团队的默认形态。他说，一两年内，90% 的智能体会话将是主动型的：发现问题、扫描代码库，然后带着修复方案来通知你。

"很多我们一直想在公司里做的东西，现在都变得可能了，"Alberti 说。

从 [Claude Fable 5](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5) 开始使用。

本系列更多内容：[Rakuten](/resources/articles/working-at-the-frontier-rakuten) 与 [Hebbia](/resources/articles/working-at-the-frontier-how-hebbia-builds-ai-for-financial-diligence-that-cant-miss-a-detail)
