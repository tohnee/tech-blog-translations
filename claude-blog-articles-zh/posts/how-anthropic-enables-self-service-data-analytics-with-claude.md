---
title: "Anthropic 如何用 Claude 实现自助式数据分析"
title_en: "How Anthropic enables self-service data analytics with Claude"
date: 2026-06-03
author: Josh Cherry
source: https://claude.com/resources/articles/how-anthropic-enables-self-service-data-analytics-with-claude
crawled: 2026-11-17
translated: 2026-11-17
---

# Anthropic 如何用 Claude 实现自助式数据分析

许多数据科学与数据工程团队都有同感：实现自助式数据分析，历来是件苦差事。

通过宽表、反规范化的表让技术水平较低的同事更容易使用数据模型，往往会随着业务扩张而产生大量定义不一致、彼此重叠的视图（对于不想学 SQL 的员工，这几乎没什么帮助）。另一种做法是为用户搭建更多"围栏式"环境，但这通常覆盖不到业务问题的长尾，而且随着各团队各自为政，指标和仪表盘也会膨胀。

LLM 的兴起为自助式分析提供了另一条避开这些难题的路径。然而，把 Claude 直接指向数据仓库、让智能体去执行查询，会制造出一种虚假的精确感。

最初那种"终于摆脱临时取数请求"的喜悦，会随着一个认识转变为恐惧：这种配置把利益相关者与其底层基础设施、文档和专业能力隔离开了——而过去正是这些东西把他们引向精心整理的数据集。

在 Anthropic，95% 的业务分析查询由 Claude 自动完成，总体准确率约 95%。把这类往往机械重复的工作交给 Claude 之后，我们的数据科学团队可以专注于更具战略性的工作，比如因果建模、预测和机器学习。

在与数十位 Anthropic 最资深的 Claude Code 用户交流、并见识了大量分析智能体的设计模式之后，我们总结出一些适用于其他与 LLM 协作的数据团队的最佳实践。本文将分享这些技巧与方法，帮助你最大化 Claude 驱动自助式业务洞察的能力，包括：

* 为什么分析准确性是关于上下文与验证的问题，而不是代码生成问题；
* 导致大多数错误的三类失效模式；
* 我们为解决这些错误而构建的智能体分析栈；
* 我们如何衡量效果；以及
* 我们创建大多数技能（skill）所用模板的基础版本（见附录）

## **数据不是软件**

LLM 的生成能力是一把双刃剑：那些让模型能创造性解决复杂问题的机制，也可能产生错误的输出（幻觉）。要完整理解分析智能体面临的挑战，把它们与编程智能体做比较会很有帮助。

编程是一个开放式的解空间，模型的创造力在此能获得回报，而文档和测试提供了抵御幻觉的天然护栏。相比之下，在分析用例中，往往只有唯一正确答案、对应唯一正确来源，而且没有确定性的方式来证明其正确性。

![](https://assets.claude.com/21d2ac79b6483d9c14944a94123ea9ffe7fd2f9b.png)

对于自助式智能体业务分析，复杂性主要在于数据的歧义。核心问题归结为一点：我们能否把用户的问题映射到数据模型中具体且最新的实体，并知道与之交互的正确方式。如果能做到这一点，后续的执行和 SQL 就变得微不足道。

我们识别出这一问题的三个特征，它们解释了绝大多数不准确的回答：

1. **概念与实体的歧义**：数据模型中可能有数百万字段、其中数百个是可行选项，智能体无法选出最能回答用户问题的正确字段。例如，统计活跃用户数时：哪些行为才算"活跃"？是否包含欺诈用户？使用多长的回溯窗口？
2. **数据陈旧**：数据源、业务定义和 schema 在不断变化；资产和智能体知识会过时，并开始返回细微错误的答案。
3. **检索失败**：正确的信息其实就在数据模型中、也做了恰当的标注，但面对浩瀚的搜索空间，智能体就是找不到。

## **我们的智能体自助分析栈**

在 Anthropic，我们减少这三类错误的主要方式是我们的智能体数据栈。每一层的主要存在意义，就是攻克其中一个或多个问题：

1. **实体歧义**：数据基础与可信来源把"可能的实体"空间收窄，直到只剩一个受治理的答案。
2. **陈旧**：维护与验证流程让一切不会随业务变化而腐坏。
3. **检索失败**：技能（skill）确保智能体能可靠地找到并正确使用那个答案。

本节我们讨论每一层是如何构建的。

![](https://assets.claude.com/9f76b807b5c27e806bb3995890888675b8325c67.png)

*关于直接在 Slack 中提出的临时问题，参见[我们的数据团队如何用 Claude Tag 部署数据分析智能体](https://claude.com/resources/articles/self-service-data-analytics-in-slack-how-anthropic-deploys-claude-tag-for-ad-hoc-questions)。*

### **数据基础**

确保分析智能体准确，最重要的方面是扎实的数据基础，其中包括数据仓库中的数据模型、转换、测试和表，以及描述它们的元数据。标准的数仓工程与数据质量实践依然适用（我们不再赘述），例如[维度建模](https://en.wikipedia.org/wiki/Dimensional_modeling)、左移测试，以及对关键管道的新鲜度和完整性检查。

![](https://assets.claude.com/05e220dc1de7b0ce4a20b4926aba1bec84963d5d.png)

维度建模这类标准数仓工程实践，和以往一样重要。

真正变化的是：你数据模型的最终用户不再是数据专家（比如数据科学家），而是代表用户行事的智能体，而这些用户的数据专业水平、对底层基础设施的理解程度各不相同。这一转变带来的挑战是：不能要求用户去验证底层正确性，因为最终用户根本不懂。

数据基础层主要针对歧义：举例来说，如果*收入*能解析到一个受治理的数据集，而不是四十个看似可行的候选，那么在智能体开始搜索之前，问题基本就消失了。这里也是第一道抗陈旧防线的所在，因为定义规范模型的那个仓库，自然也是强制它们保持最新的地方。

我们看到有几种做法效果特别好：

* **创建规范数据集（canonical dataset）**：迄今为止最常见的失效，是智能体无法把某个概念（"产品 X 的收入"）映射到唯一正确的表、列和指标定义，通常是因为存在多个实现细节略有差异的可行候选。解决之道是更少、治理更重的逻辑模型：整理出一小组规范的、单一可信来源的数据集，它们归属清晰、可消费、可发现，然后激进地弃用近似重复项。物理汇总和缓存在成本和性能上仍然重要，但它们应从规范模型机械地派生出来，而不是作为替代方案与之并存。目标是：当智能体搜索某个概念时，它只能找到一个受治理的答案。
* **强制执行标准**：我们发现，只有当规范模型和指标定义被*工具*（智能体被结构性地优先路由到它们；详见下文）、*CI*（绕过它们的变更无法通过评审）和*授权*（下游团队要么在受治理层之上构建，要么解释为什么不）三方强制时，基础才能立得住。没有强制执行，治理很快会退回到"多候选"问题。
* **把各类产物放在一起（colocate）**：我们对抗数据模型与业务逻辑持续变化的主要防御手段是"同址存放"。几乎所有数据代码（即建模、语义层、参考文档、规范仪表盘定义）都在同一个仓库里，并用 CI 检查保护跨层完整性。如果某个建模变更会破坏下游仪表盘，或让某个已记录的指标失效，CI 会标记出来，修复在同一个 PR 中一起交付。（我们会在下文**技能**一节回到这里的机制。）
* **把元数据当作一等产品**：编程智能体表现好，部分是因为代码库是*可读的*：README、类型签名、docstring 等等。你的数据仓库同样可以做到可读，但前提是列和表的描述、规范指标定义、粒度文档、有效取值范围、血缘、归属以及模型分层，都与转换逻辑本身一样严谨地维护。这并非新洞见，但良好的治理提供的正是帮助智能体选对数据集的关键上下文。

### **可信来源**

如果说数据基础是数据仓库本身，那么可信来源（sources of truth）就是智能体为了在其中导航而查阅的参考界面。这一层减少"概念与实体"的歧义，把利益相关者问题中的"周活跃用户"转化为数据模型中一个具体、受治理的实体。大致按可信度从高到低排列：

* **语义层**：编译后的指标与维度定义。如果一个能干净地映射到某个已定义指标，智能体就调用一个函数，得到一个数字——与公司其他所有界面产出的数字一致。我们的智能体被（skill 指令）*结构性要求*优先使用语义层（见附录）。我们试过但*没能*奏效的一个想法是：用 LLM 从原始表和查询日志自动生成指标定义，来引导（bootstrap）语义层。它产出的定义看似合理，却把我们要消除的那些歧义都编码了进去；与更小的人工整理层相比，在评测上净值为负。因此我们建议用 Claude 生成*文档*，但由人来拥有*定义*。
* **血缘与转换图**：当语义层覆盖不到某个问题时，血缘与表排名（按被引用次数）让智能体能够推断：哪些上游模型支撑某个概念、哪些已废弃、哪些共享同一粒度。这把"我不知道这个指标"变成了"我知道该从哪个受治理的模型去聚合"。它也是我们在下文**在线验证**中呈现的新鲜度与来源信号的骨架。
* **查询语料**：来自仪表盘、notebook 和既往分析的历史 SQL。直觉上这应该价值很高：它是每一个已被正确回答过的问题的记录。*但在实践中，我们发现给智能体对数千条历史查询的原始检索访问，准确率提升不到一个百分点*（我们在下文单独一节复盘了那次消融实验）。非结构化检索无法把新问题映射到正确的先例。真正有效的是把该语料蒸馏成结构化的、按领域划分的参考文档，以及**技能**中描述的可复用分析范式。要把查询历史当作整理的原材料，而不是智能体直接读取的可信来源。
* **业务上下文**：大多数团队会跳过的一层，也是我们长期低估的一层。一个不理解你业务的智能体，会回答用户所问，而不是用户所指。它不会知道"Q2 发布"指的是某个特定产品，不会知道两个团队用同一个词却定义不同，也不会知道某个问题被提出是因为周四有董事会。我们接入了一个由索引化文档、路线图、决策日志和组织结构构成的公司知识图谱，让智能体能消解这些环境中的指代，并提出更好的澄清问题。

这四者共同的失效模式，与数据基础层里的那个一样：**文档质量差或已过时**。Claude 在弥合差距方面特别好用（起草列描述、从查询模式中提议指标文档、在 CI 中标记未文档化的模型），但整理与归属仍由人管理。

接下来两节，我们讨论如何让这种归属的成本足够低，从而真正发生。

### **技能**

如果说可信来源是智能体的*陈述性*知识（即某个指标是什么意思），那么技能（skill）就是它的*程序性*知识：按什么顺序查阅哪些来源、如何在有歧义的数据中导航，以及一份完成的分析长什么样。

在 Claude Code 中，[技能](https://code.claude.com/docs/en/skills)是一个 markdown 文件夹，智能体按需读取。在 Anthropic，我们开发的技能带来了巨大的增量价值。没有技能时，Claude 准确回答分析问题的能力在我们的评测中不超过 21%。加入技能后，这些数字在总体上稳定高于 95%，在某些领域中经常达到 99% 左右。附录给出了我们创建大多数技能所用的骨架。

一些最佳实践：

**成对创建技能：** *知识（knowledge）*技能充当一个轻量的顶层路由，让更多领域细节按需加载。它说的是："先试语义层，但如果没有覆盖，这里有该领域约 30 个参考文件，描述相关的表、列、连接和坑。"这个路由实际上就是我们对检索失败的答案：与其让智能体在一个百万字段的仓库里搜索，不如在写出任何查询之前，就把空间收窄到几十个精选文件。*运行手册（runbook）*技能编码了资深分析师会遵循的流程：澄清问题、找到来源（通过知识技能）、执行查询，然后让结果经过对抗性评审子智能体的循环。它还打包了十几种可复用的分析范式（留存曲线、比率拆解、漏斗分析），这样常见请求就不必每次重新发明。

**编写恰当的参考文档**：为 LLM 检索而写。我们的参考文档描述表（粒度、范围、排除项）、坑的机制（例如"排除已知的免费邮箱域名，但保留 anthropic.com 这类自定义域名"），以及明确的路由触发条件（例如"如果问题是关于实验提升幅度……不要用于原始事件计数"），而不写会过时的规定性配方。下面是我们创建参考文档所用的骨架。

```
# [Domain] Tables

## Quick Reference
### Business Context — [what this domain means in plain words]
### Entity Grain — [what one row represents]
### Standard Hygiene Filter — [the filter every query in this domain applies]

## Dimensions
- [How the key dimensions are encoded, and how the same concept is named
  differently across tables]

## Key Tables
### [table_name]
- **Grain**: [...] · **Scope/exclusions**: [...]
- **Usage**: [when to use it, when NOT to, join keys, required filters]
[... one short section per governed table ...]

## Gotchas
- [The wrong-answer modes a senior analyst would warn you about]

## Best Practices / Common Query Patterns
- [Default choices, standard cuts, worked patterns where the exact query
  form is the hard part]

## Cross-References
- [Neighboring domain docs that own adjacent questions]
```

**把技能维护当作一等公民**：技能文档描述的是每天都在变化的数据模型，所以没有主动维护，它们几周内就会变成错的。我们眼看着离线准确率从发布时的约 95% 在一个月内漂移到约 65%，然后我们才把它当作工程问题来处理。这意味着把技能 markdown 文件放到与转换模型相同的仓库里，让"改模型的 PR"就是"更新描述它的文档的 PR"。一个代码评审钩子会标记任何触及报表模型、却没有触及技能文件的变更。现在约 90% 的数据模型 PR 都在同一个 diff 中包含技能变更。我们还会随着模型进步、旧失效模式不再适用，定期修剪技能脚手架。

**在所有界面上创建一致且无缝的体验**：同一个技能*必须*对 Slack、IDE、仪表盘工具和独立智能体会话中的问题给出相同答案。我们的做法是确保只有一个规范来源（数据仓库），并让技能变更自动同步。合并时，技能会同步到插件市场（供 IDE 用户）、同步到云存储 blob（供读取单个文件的托管应用），并通过 MCP 直接作为资源提供。我们还从一开始就为可移植性做设计，避免硬编码仓库路径和特定界面的命名空间。

### **验证**

最后，验证是你发现三类失效模式中还有哪一类在漏过去的方式。

#### **离线评测**

我们常见的一个模式是：数据团队搭建了精细的分析环境，却没有任何流程去了解其分析智能体的准确率。

弥合这一缺口的一种方式是离线评测，也就是简单的问答对。你可以把离线评测类比为 ML 模型的离线测试：它们不会告诉你线上智能体的表现，但能让你很好地感知是否存在关键缺口。

在 Anthropic，我们部署两种离线评测。**基于仪表盘的评测**由 Claude 自动生成（再由人验证），覆盖利益相关者最常见的问题。**长尾评测**则是我们把业务上下文（路线图、表文档）喂给 Claude，让它在领域其余部分生成看似合理的问题。我们还会持续收集每一次利益相关者在对话线程中纠正智能体的情形，因为这种纠正本身就是候选评测。

其他最佳实践包括：

* **锚定基准真值，使其无法漂移**：针对实时数据写的评测，底层数字一动就会过时。把每个评测固定到某个快照日期、写在稳定的 fact 表上，或者让评分器评判智能体的*查询*而不是它的数字。把评测套件接入 CI，让触及依赖的 PR 重新运行受影响的评测。
* **像遥测一样存储结果，而不是像测试日志**：每次运行都落进一张仓库表，记录技能版本、git SHA、模型 ID、每个断言的通过/失败、token 数以及实际耗时。"那个改动有帮助吗？"变成一个查询，你还能得到时间序列，用来捕捉单次 CI 运行发现不了的缓慢退化。
* **按领域设发布门槛**：领域负责人必须等到自己那一部分评测集越过某个阈值（我们最初用约 90%），才能向自己的利益相关者宣布智能体可用。这会迫使用户看到失败*之前*就完成参考文档的修复。
* **创建数量恰当的评测**：应该有多少评测，取决于业务领域的复杂度和底层数据模型的复杂度。通过跟踪离线准确率能多好地预测在线准确率来校准：我们发现每个主题（例如"增长"）超过几十个之后收益递减，而且这个上限随着每一代新模型而下降。
* **离线评测准确率应接近 100%**；每个正确答案也应当命中你的语义层（如果你有的话）。同样，这个准确率水平并不能说明系统不会产出错误答案，只说明——假设评测覆盖到位——没有明显缺口。

#### **消融技术**

关于技能的每一个结构性决策（例如暴露哪些来源、某个子智能体是否值得其带来的延迟、是否把两个技能合并成一个），都是通过固定离线评测集来做的。

我们只改变一个组件，比较通过率。每次运行只需一小时，却能替代大量争论。方法论比任何单个结果都重要：

* **为"无效果"设计**。我们最有用的消融是一个负结果。我们给智能体直接 grep 访问我们全部仪表盘、转换和分析师 notebook SQL（数千个文件）的权限。然后我们在会话记录中验证：它在每次回答前确实读了这些内容。准确率向任一方向变动都不到一个百分点。接着我们检查了明显的混淆因素：对于它答错的问题，答案是否真的在语料里？大约 80% 的情况下答案是"是"。"答案存在"能预测"现在答对"吗？不能，翻转率是平的。信息在那里，智能体看到了，它仍然没用。那一个实验告诉我们：瓶颈不是*获取*历史工作，而是*结构*（即把问题映射到正确实体）。这个洞见重新定向了我们几个月的路线图。
* **在 PR 粒度上做消融**。每一次有意义的技能编辑，都在相关评测切片上跑一次前后对比，并把差值写进 PR 描述。这让"我改进了文档"保持诚实，也能抓住一个令人惊讶地常见的情况：出于好意的补充反而让情况更糟。
* **保留一份"什么没奏效"的短清单**。我们的两条：在某个点之后继续叠加更多轮文档打磨（我们连续三个迭代净值为负：文档变得更长，而不是更好）；以及把对抗性评审者换成更便宜的模型以降低延迟（大部分准确率收益都丢了，速度并没有真正提升）。负结果记录成本很低，却能防止下一个人重跑同一个实验。

#### **在线验证**

最后一步是确保实际在线系统的表现尽可能准确。我们采取的一些步骤包括：

* **对抗性评审**：我们发现，用一个 Claude 技能激进地挑战某个候选最终答案的所有底层假设，能在评测集中把准确率提升 6%，但代价是 token 增加 32%、延迟增加 72%。
* **溯源脚注（provenance footer）**：每个回答都带一个脚注，说明它来自哪一层来源（语义层 › 精选参考 › 原始表）、底层数据有多新，以及模型由谁负责。它不会让答案更正确，但能帮助使用者判断该答案有多可信。"原始表，新鲜度未知"这一脚注，是转发给上游之前需要先核实的信号，也是我们针对静默失效为数不多的缓解措施之一。
* **数据质量检查**：智能体可能以正确的方式使用了正确的字段，但数据本身是错的。加入基础的数据质量检查，确保被引用字段是最新的、完整的、没有异常，通常是一种良好的卫生习惯。
* **被动监控**：我们持续跟踪两个生产信号：通过语义层解析的智能体查询占比，以及使用纠正性措辞（"那是错的表""你漏了欺诈过滤条件"）的回答占比。两者都进入一个每周与离线通过率一起复核的仪表盘。
* **主动收集纠正**：这是闭环的一环。一个定时智能体每隔几小时扫描利益相关者频道，寻找类似的纠正性措辞，起草针对相关参考文档的一行修复，并向领域负责人提交一个打了标签的 PR。修复路径刻意做得很无聊——编辑一个 markdown 文件、合并、到处自动同步——这样领域负责人在这个任务上不会花太多时间。同样的纠正也会回流到离线评测集。

这一切都没能完全抓住的失效模式是**静默**失效：答案是错的，但看起来合理，并且被无异议地使用了。我们的缓解措施是溯源脚注、任何面向领导层的内容都必须由人明确签字，以及为每个领域的头部 KPI 设一套常驻评测，每天与"受祝福的"仪表盘做一致性校验——不过我们还没有稳健的解决方案。

## **开始做自助式分析**

如果你从零开始，几套规范数据集、几十个离线评测，再加一个轻量的知识技能，就能抓住大部分收益；本文其余的都是在这些建成之后我们才加上的。

我们还分享了许多最佳实践，并非所有都适合每个数据团队。请就几个会影响你方式的原理与组织达成一致，方法是问：

* **"今天答对"与"未来答对"分别有多重要？** AI 模型进步飞快。我们常看到公司为弥补当前模型短板而搭建大量基础设施，而这些短板随着模型改进会变得无关紧要。清楚模型在哪里不足、并等待模型改进来填补缺口，开销显著更低，但可能不符合你公司的风险承受度。
* **你预期业务的复杂度会如何随时间变化？** 如果你产出的数据不多、输出的消费者很少，或数据模型可能长期保持简单，我们讨论的一些流程可能就过度设计了。
* **输出的目标受众技术程度如何？** 换个说法：如果你是为能识别答案错误的数据科学家构建这套分析系统，相比受众完全不熟悉底层数据模型的情形，你可以容忍更多错误。
* **你愿意为提升准确率花多少钱？** 我们发现对抗性验证这类流程能显著提升准确率，但往往以更高的成本和延迟为代价。
* **你对访问控制和内部数据隐私的舒适区在哪里？** 智能体拥有的上下文越多，表现往往越好；然而，广泛的数据访问与大多数公司的治理姿态相冲突。这决定了你是建一个智能体，还是建许多个作用域受限的智能体。

无论你走哪条路，我们最大的收益都来自逐一应对那三类失效模式：把歧义收敛成单一受治理的答案、让答案易于被发现，以及在任一方面过时时发出标记。

*本文由数据科学与数据工程团队的 Chen Chang、Clement Peng、Justin Leder、Johanne Jiao 和 Josh Cherry 撰写。作者感谢 Michael Segner 的贡献。*

## **附录**

#### **技能文件骨架**

以下是我们主数据仓库技能（warehouse skill）的骨架：真实文件的结构，内部细节替换为[方括号占位符]。它不是让你照抄的，而是用来展示我们认为值得写下来的那些小节。

```
---
name: [warehouse-skill]
version: [x.y.z]
description: "IF the user asks to query [the company]'s data warehouse for any
  [list of business domains] question — THEN invoke this skill. DO NOT invoke
  for [adjacent engineering tasks] or questions with no data-warehouse component."
---

# [Warehouse] Skill Instructions

## Description
The single source of truth for safe and effective [warehouse] querying.
Referenced by other skills [listed] for query execution guidance.

Act as a Data Analyst, providing strategic insights and data-driven
recommendations but seek guidance along the way.

**Out-of-scope decisions**: [product areas, etc.] → surface data only,
state "decision is [owning team]'s call", do NOT take a position or author
code fixes.

## Executing queries
Priority:
1. **[Managed connection]** (if available): [query tool] / [schema tool]
2. **[CLI fallback]** (if installed): [default project, fallback project]
3. **Neither** — ask the user to authenticate, then stop

---

# Semantic Layer (REQUIRED first step)

The governed semantic layer is the **mandatory default path** for every data
question — same numbers as [the BI tool], joins/grain/filters baked in. Raw SQL
via the reference docs below is the **fallback**, used only after the
semantic-layer path is shown not to cover the ask.

## Required workflow
1. **Load** — [how to load the semantic layer in each runtime, with fallbacks]
2. **Discover** — search measures/dimensions by keyword; **always check
   segments** (the named canonical population filters — hand-rolled WHERE
   clauses for these are the dominant wrong-answer mode)
3. **Compile + run** — build the spec → compile to SQL → execute
4. **Fallback** — only if discovery finds no relevant metric or compile fails
   → raw SQL via `references/*.md` (PART 3 below)

> **Don't bail early.** Do NOT fall back to raw SQL on these grounds:
> - "[custom date filtering / cohorts]" → [covered by time-dimension specs]
> - "[needs a join]" → [the metric layer already encapsulates its joins]
> - [3–4 more pre-rebutted excuses agents use to skip the semantic layer]

### Date windows & timezone — decide before you query
- **As-of date vs trailing-N days**: [convention for each]
- **"Last week/month"** → the last *complete* calendar week/month, not trailing-7/30
- **Timezone default**: [TZ]; [exception for certain reporting rollups]
- **Freshness lag**: [some] tables settle late — anchor on MAX(date), not "yesterday"

---

# PART 1: MUST KNOW (Read First for Every Request)

## 🚀 Quick Start Workflow
1. **Check for red flags first**: [restricted/PII requests, gated domains,
   high-stakes asks that need extra validation]
2. **Out of scope — escalate, don't guess**: [access requests, pipeline
   troubleshooting, stale dashboards, root-cause assertions, product/pricing
   recommendations] → redirect to [the owning team], don't answer
3. **Clarify the request**: time period, segment, the business decision it informs
4. **Check for existing dashboards**: [per-domain dashboard catalogs]
5. **Identify the data source**: [navigation map below; prefer governed/aggregated tables]
6. **Execute the analysis**: [required filters + adversarial review]
7. **Deliver insights**: show methodology, differentiate observations from interpretations

## 🏢 Business Context

### Entity Disambiguation (MUST CLARIFY)
- **"[Term A]" can mean**: [entity 1] or [entity 2] — always clarify which
- **"[Term B]" can mean**: [entity 1] → [entity 2] → [entity 3] (one-to-many chain)
- **"Users"**: [which identifier gives accurate counts, and which ones inflate them]

### Business Terminology
- [Current product names vs deprecated aliases that still appear as frozen
  values in the data layer — write with the new names, filter with the old]
- [Key internal acronyms]
- **[Headline metric] calculations**: [monthly / default window / leading indicator]
- **Unfamiliar terms — search [internal docs], don't guess**

### Data Integrity Requirements ⚠️
- **NEVER**: make up data/columns; make speculative assertions beyond what data shows
- **ALWAYS**: use safe division; differentiate observations ("data shows X")
  from interpretations ("this suggests Y"); flag limitations

---

# PART 2: HOW TO DO (Follow During Execution)

## 🔧 Technical Execution Guide
- [Managed-connection tools and CLI invocation details]
- **PII protection**: for restricted data, return the SQL for the user to run
  themselves — do not return results

## 📊 Analysis Best Practices Guide
1. Clarify the ask before querying
2. Show your work (filters, inclusions/exclusions, freshness)
3. Clarify denominators
4. Consider sample bias
5. Connect to business impact
6. **Adversarial SQL review (MANDATORY)** — spawn the [sql-reviewer] sub-agent
   for every query before the final answer; blocking findings must be fixed
   and re-reviewed; do not self-certify
7. **Report with provenance** — every answer ends with a footer:
   > **Source:** [semantic layer | governed table | raw exploration] ·
   > **Confidence:** [tier] · **Reviewed:** [reviewer ✓, round N] ·
   > **Freshness:** [max date in the data] · **Owner:** [owning team]

---

# PART 3: DATA REFERENCES & RESOURCES

## 📚 Knowledge Base Navigation
### [Domain A] → `references/[domain_a].md`
- **Use for**: [kinds of questions]
- **Key tables**: [...]
- **Dashboards**: `references/[domain_a]_dashboards.json`

### [Domain B] → `references/[domain_b].md`
- **Use for**: [...]

[... one entry per business domain — a few dozen in total ...]

## ⚠️ Troubleshooting Guide

### When Information Is Missing
- [missing tables / access denied / outdated docs / unknown enum values → what to do]

### Field Naming Gotchas
- Use `[field_x_v2]` NOT `[field_x]`
- [Two similarly-named tables report the same metric at different grains — which to use]
- [Which of two plausible sources is canonical for the headline metric]
- [… a dozen more hard-won one-liners …]
```
