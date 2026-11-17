---
title: "Anthropic 财务团队如何用 Claude 塑造数字背后的叙事"
title_en: "How Anthropic's finance team uses Claude to shape the narrative behind the numbers"
date: 2026-05-22
source: https://claude.com/resources/articles/how-anthropics-finance-team-uses-claude-to-shape-the-narrative-behind-the-numbers
crawled: 2026-11-17
translated: 2026-11-17
---

# Anthropic 财务团队如何用 Claude 塑造数字背后的叙事

> 原文：[How Anthropic's finance team uses Claude to shape the narrative behind the numbers](https://claude.com/resources/articles/how-anthropics-finance-team-uses-claude-to-shape-the-narrative-behind-the-numbers) · Claude 博客

Anthropic 公司财务与战略团队的 Alice Fong 分享了她如何用 Claude 为 CFO 和董事会维护一套连贯一致的财务叙事，并每周腾出 10 到 20 小时用于影响更大的工作。

在财务工作中，你的职责是塑造数字背后的故事：解释某个关键指标为何变化，基于市场趋势设定预期，把财务结果与产品战略联系起来。但你很容易把大部分时间花在确保数字正确上——在数字又一次刷新后第四次重读同一份演示文稿——而不是去思考这些数字意味着什么。

举例来说，我负责运行分析、提取指标，用于我们团队为 CFO 准备的季度董事会演示文稿。通常，一份演示文稿发出去时，我已经改了好几版。数字会一直刷新到演示文稿发出的当天早上，而每一次刷新都意味着评述要与最新数字核对。除此之外，这份文稿是协作完成的，同事们同时在更新各自的幻灯片。每次更新都意味着整个叙事要重新校准：第 4 页的评述是否还和第 17 页的数字对得上？有没有人引入了一个指标却没有定义？我得反复通读整份文稿，确认故事仍然自洽。

现在，Claude 为我完成了所有这些：它守住了工作底层的完整性，让我把时间花在上层的叙事上。它也是我月度审查流程和模型审计的一部分，把时间还给我——我可以用来与团队协作，或者用于创造性思考和那些需要判断力的财务工作。

## 俯瞰一家快速变化的公司

我在 2025 年 3 月加入 Anthropic 的公司财务与战略团队。公司财务位于财务组织的中心：其他财务团队直接与业务结对——比如 GTM 财务与销售结对——他们了解到的一切都会流回我们这里。我们的工作是准备好 CFO 和董事会需要看到的叙事：收入表现如何、利润率在发生什么变化、现金如何部署，以及对全年剩余时间意味着什么。

这套叙事必须在底下的业务不断变化时保持连贯。在 Anthropic，这意味着产品发布、模型发布、定价调整，以及销售动作分层方式的改变等等，而且常常全都发生在同一周。公司财务必须吸收公司全部的变化速率，同时仍能交给董事会一个自洽的故事。

## 我如何在各项工作中使用 Claude

我并行使用 [Claude Cowork](https://claude.com/product/cowork) 和 [Claude for Excel](https://claude.com/claude-for-microsoft-365)：Claude Cowork 帮我在文档或演示文稿中写作和综合信息，而 Claude for Excel 让我直接在财务模型里与 Claude 一起编辑。

在处理前面提到的董事会演示文稿时，我把文件交给 Claude Cowork，请它验证每一个数字和论断都与单一事实来源对得上。我还会让它像董事会成员那样阅读整套叙事，标出其中自相矛盾的地方，或假设读者拥有其实并不具备的背景的地方。Claude 能抓住我本来会漏掉的东西，而且每次数字变动它都会做，不只是做一次。

另一个例子是我们的月度财务审查——一个 Google Doc，每个月一个标签页，结构是对照预测的差异分析。当我准备撰写某个月的总结时，会把模型里相关的财务表放进文档，链接支撑性上下文，然后请 Claude Cowork 用我们既有的语气写出初稿：收入为 A，对比 B，偏差 C%，由 D 驱动。我再在此基础上修改。逐月之间语气的一致性，与数字本身同样重要，而当我引用上个月的文档时，Claude 能够实现这一点。

随着 Claude 和我们的产品界面不断改进，我与它们协作的方式也在改进。比如，Claude for Excel 从无法跟踪跨标签页的引用，进化到能在一个不平的资产负债表里跨多个标签页追溯，找到根本原因。当我打开一个没见过的模型时，会先请 Claude 总结关键驱动因素、标出结构性问题，然后再投入时间。

在所有这些工作流中——董事会材料的叙事完整性、Sheets 和 Excel 中的模型诊断、Claude Cowork 中的初稿评述——我夺回了数小时的时间，现在直接投入到真正需要判断力的工作上：框架搭建、情景问题，以及前瞻性分析。

| 工作流 | 频率 | 工具 | Claude 做什么 |
| --- | --- | --- | --- |
| 董事会演示文稿 | 每季度 | Claude Cowork | 核对跨幻灯片数字，检查叙事一致性 |
| 月度财务审查 | 每月 | Claude Cowork | 用既定语气起草初稿评述 |
| 财务模型工作 | 按需 | Claude for Excel | 跨标签页追溯引用，诊断模型问题 |
| 跨团队上下文 | 持续 | Google Workspace 和 Slack 连接器 | 从文档、邮件和 Slack 中提取决策与推理过程 |

## 上下文让一切成立

Claude Cowork 之所以有效，是因为它看到的上下文和我一样：文档和本地文件、邮件、Slack，这只是团队知识来源中的几个。当我遇到一份重要的文档，会把它提交到项目记忆中。当某个决定在漫长的跨职能讨论串中做出，我会让 Claude 把结论和推理提取出来，这样下次这个话题在董事会周期中出现时，它就随时可用。

我还为不同的受众维护不同的项目：一个用于月度审查，一个用于董事会演示文稿。语气和惯例不同，记忆也就不同，Claude 会相应地生成内容。

## Claude Cowork 在财务组织中的应用

在整个财务组织中，我的同事们使用许多如今已打包进 Claude Cowork [金融服务插件](https://www.anthropic.com/news/finance-agents)的[技能](https://support.claude.com/en/articles/12512180-use-skills-in-claude)。以下是 CFO 组织如今使用 Claude Cowork 的几个例子：

* **财务与战略**：由分析师自己通过提示构建的交互式预测和群组仪表盘：无需 SQL 或工程介入。每天上午 7 点，一份收入与指标摘要会送到领导层的 Slack。
* **会计**：总账到子分类账（GL-to-subledger）及银行对账，差额被分类，审阅人评述起草为初稿。三大财务报表都运行波动（Flux）分析。团队任何人都可以在 Slack 中向 Claude 提问并得到有来源的答案。
* **企业发展与投资者关系**：每天针对三到四个收购目标生成筛选报告，基于笔记和公开数据构建，几分钟内汇总成备忘录。团队把时间花在判断和拍板上，而不是初稿上。
* **税务与资金**：转让定价、研发税收抵免和关联（nexus）问题，以一手来源引用作答。间接税和现金对账沿用与会计相同的技能模式。

## 给财务团队上手 Claude 的建议

一年前我加入 Anthropic 时，AI 工具大多还是 LLM：擅长文本，不太擅长数字。真正吸引我的是看着 Claude for Excel 不断进步。我几乎可以逐版追踪模型变好带来的差异。

如果你还在犹豫，从简单开始：让 Claude 读一份文档并总结，然后不断把边界往外推。它在重复发生的工作流上价值最大，包括董事会周期和月度审查——在这些场景中，一致性会复利式累积，项目记忆也每一轮都更丰富。你不需要复杂的工具栈；我几乎完全依靠 Claude Cowork [项目](https://support.claude.com/en/articles/14116274-organize-your-tasks-with-projects-in-claude-cowork)、Claude for Excel 和 Google Workspace 连接器运行。

如果你不知道该用 Claude 的哪个入口，直接问 Claude 就好。有了 Claude 参与其中，我能跟上工作底下变化的节奏。我更快地得到洞见，意外和瓶颈更少，也能把更多时间花在框架搭建和前瞻性分析上。

*今天就上手 [Claude Cowork](https://claude.com/product/cowork)。*
