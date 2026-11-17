---
title: "顾问策略：为智能体注入智力增益"
title_en: "The advisor strategy: Give agents an intelligence boost"
date: 2026-04-09
source: https://claude.com/resources/articles/the-advisor-strategy
crawled: 2026-11-17
translated: 2026-11-17
---

# 顾问策略：为智能体注入智力增益

> 原文：[The advisor strategy: Give agents an intelligence boost](https://claude.com/resources/articles/the-advisor-strategy) · Claude 博客

让 Opus 担任顾问、Sonnet 或 Haiku 担任执行器，就能以一小部分成本，为智能体带来接近 Opus 级别的智能。

希望更好地平衡智能与成本的开发者，已经逐渐汇聚到我们称之为“顾问策略”的做法上：让 Opus 担任顾问（advisor），让 Sonnet 或 Haiku 担任执行器（executor）。这能为智能体带来接近 Opus 级别的智能，同时将成本保持在接近 Sonnet 的水平。

今天，我们在 Claude Platform 上推出顾问工具（advisor tool），让顾问策略在你的 API 调用中只需改一行代码。

## 用顾问策略构建高性价比智能体

![](https://assets.claude.com/8f630cd9ff3ec9f706e977e7b91143743c04221d.png)

采用顾问策略时，Sonnet 或 Haiku 作为执行器端到端地执行任务：调用工具、读取结果，并不断迭代直至找到解决方案。当执行器遇到无法合理解决的决策时，它会向作为顾问的 Opus 寻求指导。Opus 访问共享上下文，返回一份计划、一次纠正或一个停止信号，然后执行器继续推进。顾问从不调用工具，也不产生面向用户的输出，只向执行器提供指导。

这颠倒了常见的子智能体模式——由更大的编排模型拆解工作，再委派给更小的 worker 模型。在顾问策略中，更小、更具成本效益的模型驱动整个过程，并在需要时升级求助，无需任务拆解、worker 池或编排逻辑。前沿级推理只在执行器需要时启用，其余运行过程仍保持执行器级别的成本。

在我们的评测中，以 Opus 作为顾问的 Sonnet 在 [SWE-bench Multilingual](https://www.swebench.com/multilingual.html)¹ 上比单独使用 Sonnet 提升了 2.7 个百分点，同时将每项智能体任务的成本降低了 11.9%。

![](https://assets.claude.com/fe28fc77f04a26f04870c65c3f36204f69a23e49.png)

## **顾问工具**

我们通过[**顾问工具**](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool)把顾问策略带到 API 中。这是一个服务端工具，Sonnet 和 Haiku 知道在需要针对特定任务获得指导或帮助时调用它。

在我们的评测中，配备 Opus 顾问的 Sonnet 在 BrowseComp² 和 Terminal-Bench 2.0³ 基准上的得分都有提升，而每项任务的成本低于单独使用 Sonnet。

![](https://assets.claude.com/c01f1490dc3cfe7d5995541fc3fbd64d55d0dffe.png)

顾问策略同样适用于以 Haiku 作为执行器。在 BrowseComp 上，配备 Opus 顾问的 Haiku 得分为 41.2%，是单独使用 Haiku 时 19.7% 的两倍多。配备 Opus 顾问的 Haiku 得分比单独使用 Sonnet 低 29%，但每项任务成本低 85%。相比单独使用 Haiku，顾问会增加成本，但合计价格仍只是 Sonnet 的一小部分，因此对于需要兼顾智能与成本的高并发任务而言，它是一个很有吸引力的选择。

![](https://assets.claude.com/ea472c56f2d583b9d09c85e5c6539864e4dd9ab4.png)

在 Messages API 请求中声明 advisor\_20260301，模型交接会在单个 /v1/messages 请求内部完成——无需额外的往返或上下文管理。由执行器模型决定何时调用它。调用时，我们会把整理好的上下文路由给顾问模型，返回计划，然后执行器继续执行，全部发生在同一个请求内。

```
response = client.messages.create(
    model="claude-sonnet-4-6",  # executor
    tools=[
        {
            "type": "advisor_20260301",
            "name": "advisor",
            "model": "claude-opus-4-6",
            "max_uses": 3,
        },
        # ... your other tools
    ],
    messages=[...]
)

# Advisor tokens reported separately
# in the usage block.
```

**定价**。顾问 token 按顾问模型的费率计费；执行器 token 按执行器模型的费率计费。由于顾问只生成一份简短计划（通常为 400–700 个文本 token），而执行器以更低的费率处理全部输出，整体成本远低于端到端运行顾问模型。

**内置成本控制。** 设置 max\_uses 可限制每次请求的顾问调用次数。顾问 token 会在用量块（usage block）中单独报告，因此你可以按层级跟踪支出。

**可与现有工具协同工作。** 顾问工具只是 Messages API 请求中的又一个条目。你的智能体可以在同一个循环中[搜索网络](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)、[执行代码](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)并咨询 Opus。

![Bolt](https://assets.claude.com/c47ae719ec15794844da97bc7651c0081ce5a4e2.svg)

> “在复杂任务上，它能做出更好的架构决策，而在简单任务上不会增加任何开销。有它和没它，计划和执行轨迹完全是天壤之别。”

Eric Simmons，Bolt 首席执行官兼创始人

![Genspark (square)](https://assets.claude.com/b1e42f1b17a4c1b366adb56b71934a19f5b0c621.svg)

> “我们看到智能体轮次、工具调用和整体得分都有明显改善——比我们自己构建的规划工具还要好。”

Kay Zhu，Genspark 联合创始人兼 CTO

![Eve Legal](https://assets.claude.com/f1efc487a08ab700dd2f0a0d09e717745da3e2d0.svg)

> “在结构化文档抽取任务上，顾问工具让 Haiku 4.5 能够根据复杂度动态咨询 Opus 4.6 来扩展智能水平，达到前沿模型的质量，成本却只有其五分之一。”

Anuraj Pandey，Eve Legal 机器学习工程师

## 开始使用

顾问工具目前已在 Claude Platform 上以原生测试版提供。开始使用：

1. 添加测试版功能请求头：anthropic-beta: advisor-tool-2026-03-01
2. 在 Messages API 请求中添加 advisor\_20260301 工具
3. 根据你的用例修改[系统提示词](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool#suggested-system-prompt-for-coding-tasks)

我们建议用现有评测套件分别运行单独 Sonnet、Sonnet 执行器 + Opus 顾问，以及单独 Opus。查阅[文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool)了解更多。

## 脚注

1. **SWE-bench Multilingual：** 单独运行 Sonnet 4.6 时使用自适应思考。Sonnet 4.6 + 顾问使用我们建议的编码系统提示词，并关闭思考。两组运行均使用高努力等级，并配备 bash 和文件编辑工具。得分是在九种语言的 300 道题上进行的五次试验的平均值。所有运行均使用 Opus 4.6 作为顾问模型。
2. **BrowseComp：** 所有运行均关闭思考，并使用网络搜索和网页抓取工具。Sonnet 4.6 的运行使用中等努力等级。Sonnet 4.6 + 顾问使用我们建议的编码系统提示词；Haiku 4.5 + 顾问未使用。未使用程序化工具调用或上下文压缩。得分基于 1,266 道题，每道题仅尝试一次。所有运行均使用 Opus 4.6 作为顾问模型。
3. **Terminal-Bench 2.0：** 所有运行均关闭思考，并使用 bash 和文件编辑工具。Sonnet 4.6 的运行使用中等努力等级。两组顾问运行均未使用我们建议的编码系统提示词。每个任务都在隔离的 pod 中运行，资源分配为 3 倍，超时时间为 1 倍。得分是 89 个任务中每个任务五次尝试的平均值。所有运行均使用 Opus 4.6 作为顾问模型。
