---
title: "如何在 Claude Cowork 中使用 Claude Fable 5"
title_en: "Working with Claude Fable 5 in Claude Cowork"
date: 2026-07-16
source: https://claude.com/resources/articles/working-with-claude-fable-5-in-claude-cowork
crawled: 2026-11-17
translated: 2026-11-17
---

# 如何在 Claude Cowork 中使用 Claude Fable 5

> 原文：[Working with Claude Fable 5 in Claude Cowork](https://claude.com/resources/articles/working-with-claude-fable-5-in-claude-cowork) · Claude 博客

*Claude Fable 5 能独自承担漫长、复杂的工作。本文介绍如何在 Claude Cowork 中充分利用它——从一个想法起步，一路走到完成的工作。*

Claude Fable 5 是 Anthropic [能力最强的通用可用模型](https://www.anthropic.com/news/claude-fable-5-mythos-5)，为长时间运行、复杂、异步的工作而打造。在执行多步骤工作流时，Claude Fable 5 尤其高效——比如开展深度研究并把它融入一份初稿备忘录、在生成董事会演示材料前做尽职调查，或者遍历一个文件夹给多份合同做红线批注——它可以长时间自主推进，并在过程中测试、评估自己的结果。

要最大化模型的能力，需要改变你与它协作的方式。随着模型不断进步，我们也在持续完善让人们从 Claude 那里获得更多产出的建议，包括[提示工程最佳实践](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)、提供上下文，以及[构建 skills](https://claude.com/resources/tutorials/teach-claude-your-way-of-working-using-skills) 来固化可重复的流程，比如每周团队更新、销售电话准备或客户反馈分析。这些做法在 Claude Fable 5 上依然重要——事实上，有了这些做法，模型表现得更好。

Claude Fable 5 会把你的上下文、偏好和 [skills](https://claude.com/resources/articles/skills-explained) 应用到整个任务中，即使是耗时数天的任务；而此前的模型在长时段中可能会跟丢，需要提醒。与它协作就像与一位能力极强的同事共事：你说明情况，就“一个出色的最终结果长什么样”达成一致，然后让这位同事去做事。你花在逐步检查上的时间更少，于是能把更多时间用于决定这项工作应该是什么。

我们的 [Claude Fable 5 提示指南](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5) 提供了能力改进的详细清单，以及建议改变的行为和提示方式。本文将介绍其中一些如何适用于 Claude Cowork——Anthropic 面向知识工作的智能体式 AI 系统。

## Claude Fable 5 如何与 Claude Cowork 相辅相成

Claude Cowork 是为产出完成品而构建的。给它一个目标，其余的事情由它来管理，即使任务庞大而复杂。一个大任务会被拆成多个同时运行的部分，每个部分都有自己的子智能体——一个独立的 Claude 实例，负责完成任务的某一部分并回报结果。Claude 就是这样快速处理大量信息。Claude 管理大型任务的另一种方式，是开始时设定一份计划，并在过程中用自己的结果对照检查。

Claude Fable 5 在[长时间运行的复杂任务上大幅领先我们的其他模型](https://www.anthropic.com/news/claude-fable-5-mythos-5)，而 Claude Cowork 的任务往往正是这一类：几十个步骤，每一步都建立在上一步之上。以“根据今年的实际数据编制明年预算”这样的项目为例。Claude 获得并读取电子表格，提取运行率（run rate），对每一行做预测，把预测值与目标核对，并撰写摘要。如果它早期误读了一个运行率，错误会流入其后的每一项预测。Claude Fable 5 会在开工前规划工作流，并在过程中检查结果，因此能在任务运行期间发现误读的数字并纠正它。

## 决定何时使用 Claude Fable 5

Claude Fable 5 不是 Claude Cowork 的默认模型，需要你主动选择。截至本文发布时，默认模型是 Claude Sonnet 5，对于你自己快速过一遍就能处理的日常任务，它是合适的选择。Claude Opus 是处理形态清晰、你知道最终结果长什么样的深度工作的可靠选择。Claude Fable 5 适用于那些感觉最复杂或最模糊、此前模型可能无法胜任的项目。它会花更多时间思考，也会消耗你更多的用量限额，但对于耗时或出错代价高昂的工作，这可能是值得的。我们建议你把 Claude Fable 5 留给最重要的工作，尤其是需要使用多个工具、并做出一系列判断的任务。

你还可以通过 Claude 的努力等级（effort）设置进一步调整选择。努力等级越高，Claude Fable 5 在启动任务前规划得越多，在运行过程中检查得也越频繁。对于你期望 Claude 从头到尾完成的复杂或多步骤项目，把努力等级调高。努力等级较低时，你会得到更快的响应，同时仍能利用 Claude Fable 5 的智能。可以考虑把它用于那些仍需要前沿判断力、但不需要深度探索的任务，例如由许多简单步骤组成的智能体运行，或结果对 Claude 来说容易核对的工作。在我们的测试中，低努力等级的 Claude Fable 5 常常达到或超过更早模型最高努力等级下的表现。若想更详细地了解其内部机制，我们在这篇文章中解释了[模型选择与努力等级在 Claude Code 中如何相互作用](https://claude.com/resources/articles/claude-model-and-effort-level-in-claude-code)。

还值得说明的是，Claude Fable 5 配备了一套新的分类器：这些独立的 AI 系统会检测与网络安全或生物、化学相关的请求中潜在的滥用。当它们触发时，回答会自动改由 [Claude Opus 4.8](https://support.claude.com/en/articles/15363606-why-claude-switched-models-in-your-conversation-with-fable-5) 处理，并在每次发生时告知用户。Opus 4.8 本身就是一个能力很强的模型，此后对话会留在 Opus 上；要回到 Claude Fable 5，请开启一个新对话。我们保守地调校了这些防护措施，以便既安全又快速地让一个 [Mythos 级模型](https://www.anthropic.com/news/claude-fable-5-mythos-5) 面向大众开放，因此它们有时会拦下无害的请求，包括 Claude Cowork 中只是触及相关话题的措辞。随着我们不断完善这些防护措施，我们正在努力减少这类误报。

## 从一个想法开始就够了

启动一项任务时，你并不总是清楚自己想达成什么。前期这段摸索期，正是 Claude Fable 5 可以成为强大思考伙伴的地方；在 Claude Cowork 中，它会基于你的 skills、工具和知识来工作。

例如，如果你看到一条与所在行业或公司相关的新闻公告，你可以问 Claude：“这是那条公告，告诉我对我们意味着哪些变化，把你知道的关于我们组织的一切都考虑进来。”你阅读输出，而当你开始形成策略时，Claude 会制定一份计划来产出你需要的材料，而且就从头脑风暴发生的那个 Claude Cowork 对话里开始。

在 Claude Cowork 中做头脑风暴，等于把真实的材料交给模型去思考：它可以在你们交谈时读取你分享的文件、使用你已连接的工具，因此能给出相关的建议。它会在一个想法还容易改动的时候就注意到其中的缺口，并向你展示你没想到的方向。而当任务在同一个对话中开始时，Claude Fable 5 已经带着你们确定下来的目标、你指明的约束，以及过程中做出的各项决定。

例如，Anthropic 的一位数据科学家带着一个新分析仪表盘的想法来到 Claude Cowork，当时团队还在琢磨这个仪表盘该展示什么。因为 Claude Fable 5 能在对话期间读取团队的使用数据，它知道哪些问题要花几周才被发现，并据此排序出本可以更早发现这些问题的指标。到对话结束时，这位数据科学家已经拿到了一份值得新增的指标短名单，以及一个可点击的原型。

以下两条提示词可以帮你把想法推进成产出：

* **让 Claude 采访你**：“在开始之前，先把做对这件事所需知道的一切都问我。”
* **让它给方向**：“大致上我想要的是这个。给我三种你可以展开的方式，每种附一个快速样例。”

## 用约束来提供上下文

上下文是 Claude 工作的依据。在 Claude Cowork 中，它指的是你的提示词、你分享的文件和文件夹，以及你连接的任何工具，比如 Asana、Hubspot、Jira、Slack 或[其他工具](http://claude.com/connectors)。

当你在 Claude Cowork 中给 Claude Fable 5 布置任务时，想想你会怎样向同事交代一份报告。你不会递给他们一列规则，但多半会告诉他们这份报告给谁看、什么时候要、必须达成什么，然后相信他们在此基础上做出好的判断。Claude Fable 5 也是同样的工作方式。

约束依然有用：“控制在两页以内，用平实的语言”就是一条好指令。但约束只告诉 Claude 不要做什么。上下文告诉它这项工作是为了什么，这样在约束没有预料到的情况下，它也能做出正确的判断。

Claude Fable 5 之所以能处理好长时间、多步骤的任务，部分原因就在于这种上下文：当它在工作中遇到一个问题或决策点时，它会到你分享的上下文中寻找答案。它也会用这些上下文在过程中自我检查，所以给它一些具体的东西来对照判断，比如一份报告的早期草稿和最终版本，Claude 就会根据两者之间的变化推断出你的标准是什么。

上下文还能让 Claude 理解你的处境，从而推断或找出你在提示词中从未指定的细节。分享更多上下文，能让 Claude 在一个比你塞进提示词的知识库大得多的范围里检索。

关于上下文很多的对话，有一点需要注意：为了跟上进度，Claude 在你每发一条新消息时都会重新读取整个对话，因此长对话可能消耗更多用量。把新任务放在新的对话里开始会有帮助。定时任务也会计入你的限额，所以偶尔查看一下你的用量，并关掉不再需要的定时任务。

## 把更大、更复杂的任务委托给 Claude Fable 5

你可能已经习惯把任务拆成若干部分，逐一提示 Claude。Claude Fable 5 需要的这类中间提示词要少得多，因此你可以在 Claude Cowork 中委托完整的工作。

当流程本身对你很重要时，你仍然应当自己写出步骤，比如某个指标每次都必须以完全相同的方式计算。但如果重要的是结果，那就描述目标，让 Claude 做剩下的。分步提示词也可能把它限制在你想到的那些步骤上；而一个目标则给它空间去寻找更好的路径。

在 Claude Cowork 中做委托，意味着把一个你通常会自己做的决定交给 Claude。以下三种方式可以做到：

* **委托方法**：把材料给 Claude，描述你想要的结果，例如“这是上季度的客户反馈。找出取消量上升的原因，以及我们应该改变什么。”走完那个文件夹可以有好几条合理的路径，哪条正确取决于反馈里有什么。这正是 Claude Fable 5 擅长做的选择：它读完所有内容，选定一条路径，并在把结论带给你之前对照反馈做检查。你不需要指定它如何抵达，就能评判答案。
* **委托流程**：一个 skill 教 Claude 你团队使用的某套流程——你如何制作报告、排版演示文稿、做某项分析。你不需要说明该用哪些 skills、按什么顺序用。只说“按我们一贯的方式做季度回顾”，Claude Fable 5 就会在合适的时机选出合适的 skills。
* **委托时机**：对于你想重复进行的工作，描述结果，Claude 会设定日程并把它变成一项周期性任务：“我想每周一开工时就知道管道里发生了什么变化、哪些事需要决策。”

交给 Claude Fable 5 的工作，可以比你以往交给 AI 的更难，甚至可以是你原以为不可能的工作。即使工作杂乱、模糊，或者可能要花几小时、几天才能完成。描述它，看看模型能否在那个层次上工作。选一个你对其负责的结果，说明你会如何评判它，然后让 Claude 提出达成它的步骤。其中一些工作可能最终变成一项自行运行的定时任务。Claude 可以把流程保存为 skill 并放到日程上，通过你已经连接的工具来完成。

## 审查 Claude 的思考过程

Claude Fable 5 之所以能承担长时段的工作，部分原因在于它知道如何设定并很好地遵循计划。在 Claude Cowork 中，你可以在 Claude 工作时看到这份计划：对话旁边的面板会列出它打算做什么，随后展示它正在读写哪些文件、使用哪些工具和 skills。

这个面板正是你及早发现问题并重新引导的机会。原本你会在最终产出里发现的错误，现在会表现为计划中的某一步走错。你可以用一句话修正计划，Claude 会作出调整，而不必从头再来。

![](https://assets.claude.com/426b5a3d0277b94a87edc784ca2f496e3f175855.png)

工作完成后，像审查同事的产出那样审查它：打开 Claude 生成的文件读一读。如果有什么看起来不对，这次运行的记录仍在对话里。往回翻看 Claude 在工作过程中列出的步骤，包括它读取的文件和使用的工具，展开它的思考以查看某个决定背后的推理。或者直接问：“这个数字是从哪来的？”Claude 会指出它的来源。

从你知道如何验证的工作开始，比如为你团队做下季度计划的初稿。如果你很了解优先事项，就能很快判断 Claude 这一遍做得是否站得住。随着结果被证明可靠，再委托更大的工作。

## 投入建设你的 Claude Cowork 环境

一个能力更强的模型，会提升你所建立的每一项连接的价值——从你分享的文件夹，到你团队工作的工具。以下是我们关于如何给 Claude Fable 5 提供它发挥最佳水平所需上下文的建议：

* **连接你的工具**：先把你[日常使用的工具](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities)连上 Claude，比如邮件、日历、文档或团队的聊天工具。每一条连接都会拓宽 Claude 的能力，而无需你手动复制内容。Claude Fable 5 很擅长判断何时值得使用某个工具：在你的工具已连接的情况下，它注意到答案就在你的日历或某个聊天线程里，就会自己去取，而不是等着被指过去。
* **把写作调整成你的风格**：每个新模型都带着自己的写作默认值：语气、长度，以及输出中首先会想到的措辞。你可能会注意到 Claude Fable 5 有一些默认习惯，[比如在较长会话中写得更为简省或不易跟上](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)。语气、音调和风格很容易定制；你可以通过提示或把它们写进项目指令来贴合自己的偏好。例如，你可以加上类似“使用平实、直白、直接的语言”。如果你使用记忆功能，偶尔检查一下 Claude 保存了哪些关于你写作偏好的内容。对于需要特定语气的文档，用连接器或已有文件让 Claude 读你过去的写作，并把它的发现保存成一个 skill，供你下次做类似工作时调用。我们发现 Claude Fable 5 比更早的模型更严格地遵循常驻指令，也更善于在需要时使用已保存的材料。
* **重新审视你为更早模型所做的设置**：为更早模型写下的保存指令，比如 Skills 和记忆文件，往往包含那个模型需要的纠正。一路沿用下来，旧的纠正可能会约束新模型。请让 Claude Fable 5 做一次审计：“看看我的 skills 和保存的记忆。哪些仍然适用，哪些是为更老的模型写的？”

## 接下来

随着前沿智能持续进化，Claude Cowork 会越来越有能力，支持运行时间更长的工作，并解锁更多知识工作用例。学会如何提示、管理上下文、检查 Claude 的工作、委托任务，将帮助你充分利用 Claude Fable 5 和未来模型所能提供的一切。

*本文由 Anthropic 教育团队的 Josefina Albert 撰写。*

今天就[开始使用 Claude Cowork](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork)。
