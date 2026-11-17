---
title: "在前沿工作：Base44 为何把最具挑战性的工程工作托付给 Claude Fable 5"
title_en: "Working at the frontier: Why Base44 trusts Claude Fable 5 with their most challenging engineering work"
date: 2026-07-15
source: https://claude.com/resources/articles/working-at-the-frontier-why-base44-trusts-claude-fable-5-with-their-most-challenging-engineering-work
crawled: 2026-11-17
translated: 2026-11-17
---

# 在前沿工作：Base44 为何把最具挑战性的工程工作托付给 Claude Fable 5

> 原文：[Working at the frontier: Why Base44 trusts Claude Fable 5 with their most challenging engineering work](https://claude.com/resources/articles/working-at-the-frontier-why-base44-trusts-claude-fable-5-with-their-most-challenging-engineering-work) · Claude 博客

*Yoav Orlev 是 Base44 的产品负责人，作为该 vibe coding 平台的第一名员工加入，见证了自己的团队在 Sonnet 4 之后的每一个 Claude 模型上构建产品。以下是他为何认为 Claude Fable 5 是第一个像资深工程师那样思考软件的模型，以及这为团队其他人释放出了什么。*

Base44 是一个 vibe coding 平台，无论技术能力如何，任何人都能用它构建全栈应用和网站。其客户既包括没有开发人员的小企业，也包括用它构建完整 SaaS 产品的公司。

Yoav Orlev 作为第一名员工加入 Base44，现在负责产品。他说，工作中最有成就感的部分之一，是看到小企业用这个平台做出他们原本因缺少时间、预算或技术知识而做不到的事——无论是搭建一个数字店面，还是为餐厅员工开发一个排班管理应用。他团队的使命是不断拓宽产品能力，同时保持它对所有人都易于使用。

Base44 的产品和工程团队一向行动迅速，尤其是在交付中小规模功能时。但任何涉及多个相互依赖部分的平台核心变更，只能交给最资深的工程师。

其中一个瓶颈是 Base44 的系统提示词及其数百种排列——它们会因用户是第一次做应用还是第五次、是免费用户还是订阅用户，以及所构建应用的类别和功能而不同。另一个瓶颈是改动原生移动端基础设施，这只有具备移动端专业能力的工程师才能做。

Orlev 认为，此前为 Base44 应用生成引擎提供支持的 Claude 模型（自 2025 年初该引擎上线以来一直如此）无法被托付这类工作。比如，当一个模型卡在某个错误上时，它会一直死磕眼前这一处，而不会意识到修复方案很可能已经存在于代码库的其他地方，并去搜索它。

"决定下一步做什么是至关重要的一步，而大多数时候，[此前的]模型会采取——我会说——一种天真的做法，"他说。

Orlev 说，Claude Fable 5 是团队测试过的第一个能像理解软件是如何构建的那样去推理的模型。

## 把最复杂的产品和工程工作托付给 Fable 5

Base44 会让每一个新的 Claude 模型跑一遍覆盖不同应用类型的评估（evals），测量延迟、成本和构建错误。团队还会做诸如构建一个《Minecraft》克隆版之类的测试，看模型如何处理游戏物理和机制。

在 Claude Fable 5 身上，有两点很突出：它用少得多的轮次完成任务，并且在首次提示词后就构建出更完整的应用，包括早期模型会跳过的边界情况。

于是，团队把它指向一项此前只留给最资深工程师的任务：重建 Base44 的系统提示词。经过大约一小时的往复提问后，Claude Fable 5 自主运行了四个小时，交回了他们所需成果的 90% 到 95%。借助其 A/B 测试基础设施，团队当天下午就得以测量并发布这些改动。而且在 Claude Fable 5 工作期间，它甚至指出了 Base44 自身评估中的一个盲点：团队没有测试缓存命中，而提示词的改动可能破坏缓存，在数百万用户的规模下这会推高成本。模型指出了一个盲点，并纠正了它。

当 Claude Fable 5 卡在 Base44 应用内智能体背后的运行框架（harness）的一处改动上时，它推理出同样的问题很可能已在代码库的其他地方解决过，于是去调查那一部分，并带回了修复方案。"这种'这个问题很可能在别处已经解决过，所以我应该去那里调查'的推理，我们在其他模型身上见得没那么多，"Orlev 说。

Orlev 把与 Claude Fable 5 协作比作与一位资深工程师协作。初级工程师需要你指定每一个步骤、并不断检查；而资深工程师，你只需要交代目标和缘由。

这类工作也延伸到了工程团队之外。当一位产品经理希望把原生移动应用构建能力引入 Base44 时，他把这项工作交给了 Claude Fable 5，大约两个半小时后，就得到了一个完成了团队投入生产所需约 90% 的可用环境。

在 Claude Fable 5 之前，这类工作必须等 Base44 最顶尖的三位工程师或某位专家腾出手来。现在，模型执行任务，而 Orlev 的团队在发布前审阅、测试并批准代码。

![](https://assets.claude.com/5f96b37adfbd2583eb00586a900e7b6e7890a14b.jpg)

Claude Fable 5 让 Base44 的产品、工程和设计团队有信心去构建其 Superagents 平台中更具雄心的部分。

## 下一步

随着 Claude 模型能力提升，Base44 团队对平台的目标也在提升。团队的目标是把 Base44 从一个构建应用的工具，变成一个还能帮助人们管理和壮大他们所构建之物的平台。Base44 Superagents 现已公开发布，围绕这些应用运行各种工作流。

由于知道可以把复杂任务托付给 Fable 5，Orlev 现在鼓励产品经理和设计师去改造平台中那些他们此前因为担心搞坏东西而不愿触碰的部分。

"Fable 给了我们信心，让我们在业务上做出更大胆的动作，"Orlev 说。"它把产品带向了一个全新的领域和种种可能性，而这些在此前，我会说，是我们不敢去做的。"

***从 [Claude Fable 5](https://www.anthropic.com/claude/fable) 开始使用。***
