---
title: "Claude Managed Agents 的内置记忆"
title_en: "Built-in memory for Claude Managed Agents"
date: 2026-04-23
source: https://claude.com/resources/articles/claude-managed-agents-memory
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude Managed Agents 的内置记忆

> 原文：[Built-in memory for Claude Managed Agents](https://claude.com/resources/articles/claude-managed-agents-memory) · Claude 博客

[Claude Managed Agents](https://claude.com/resources/articles/claude-managed-agents) 的记忆功能现已开放公测。你的智能体现在可以从每个会话中学习，这得益于一个为智能而优化的记忆层，它在性能与灵活性之间取得平衡。由于记忆以文件形式存储，开发者可以导出记忆、通过 API 管理它们，并完全掌控智能体保留了什么。

![](https://assets.claude.com/f55bb71c387d00c0604c391b77605382df1cfff6.png)

## Claude Managed Agents 中的记忆如何工作

Claude Managed Agents 的记忆是一个内置的、为智能而优化的记忆层，让智能体能够从每个会话中学习。记忆是通过内部基准测试来优化的，这些基准针对的是长期运行的智能体——它们能跨会话不断改进，并彼此分享学到的东西。

我们发现，当记忆建立在智能体已经在用的工具之上时，效果最好。Claude Managed Agents 的记忆直接挂载到文件系统，因此 Claude 可以依赖那些让它在智能体任务中表现出色的同一套 bash 与代码执行能力。借助基于文件系统的记忆，[我们的最新模型](https://www.anthropic.com/news/claude-opus-4-7#:~:text=Memory.%20Opus%204.7%20is%20better%20at%20using%20file%20system%2Dbased%20memory.%20It%20remembers%20important%20notes%20across%20long%2C%20multi%2Dsession%20work%2C%20and%20uses%20them%20to%20move%20on%20to%20new%20tasks%20that%2C%20as%20a%20result%2C%20need%20less%20up%2Dfront%20context.)能保存更全面、组织更好的记忆，也更懂得判断对给定任务应记住什么。

## 面向生产级智能体的可移植记忆

记忆功能是为企业级部署而构建的，具备作用域权限、审计日志和完整的程序化控制。存储（store）可以在多个智能体之间共享，并具有不同的访问作用域。例如，组织级的存储可以是只读的，而每个用户的存储则允许读写。多个智能体可以同时对同一个存储工作，彼此不会覆盖。

记忆是可以导出、并可通过 API 独立管理的文件，开发者因此拥有完全控制权。所有变更都会通过详细的审计日志追踪，你可以分辨某条记忆来自哪个智能体、哪个会话。你可以回滚到更早的版本，或从历史中删除（redact）内容。更新也会以会话事件的形式出现在 [Claude Console](https://platform.claude.com/) 中，开发者可以追溯智能体学到了什么、从何而来。

## **团队正在构建什么**

各团队一直在用记忆来闭合反馈循环、加速验证，并替代自建的检索基础设施：

* **Netflix** 的智能体会跨会话携带上下文，包括需要多轮才发现的洞见，以及对话过程中人类做出的纠正，无需再手动更新提示词和技能（skills）。
* **Rakuten** 基于任务的长期运行智能体用记忆从每个会话中学习、避免重蹈覆辙，将首次通过错误率降低 97%，而这一切都在工作区作用域内、可观测的边界中完成。
* **Wisedocs** 在 Managed Agents 上构建了文档验证流水线，利用跨会话记忆发现并记住反复出现的文档问题，使验证速度提升 30%。**‍**
* **Ando** 正在 Managed Agents 上构建其职场通讯平台，记录每个组织如何交互，而无需自行搭建记忆基础设施。

![Rakuten](https://assets.claude.com/5463fa5a44d12868ceec5ae30bfc8c412cafdeae.svg)

> 「Claude Managed Agents 的记忆功能让我们能够大规模地把持续学习投入生产。我们的智能体从每个会话中提炼经验，首次通过错误减少 97%，成本降低 27%，延迟降低 34%，用户无需再花时间提醒智能体去修正系统早已学会避免的错误。而且由于记忆具有工作区作用域且可观测，持续学习始终在我们的掌控之中。」

Yusuke Kaji，Rakuten 业务 AI 总经理

![Ando](https://assets.claude.com/9d0ae4950cad063b171ca1e5a983f38f34493562.svg)

> 「Ando 的许多工作就是理解团队与其智能体之间那些快速流动、杂乱无章的对话。记忆功能让我们不必再自建记忆基础设施，而能专注于产品本身。」

Sara Du，创始人

![Wisedocs](https://assets.claude.com/3af81b32b07b671a26e887260609c5b8747f2c3b.svg)

> 「一个好的记忆 API 能消除许多基础设施方面的麻烦，在跨智能体、跨会话构建时尤其如此。在基于 Claude Managed Agents 的文档验证流水线中，我们用跨会话记忆让智能体识别并记住常见问题——包括我们没想到的问题。它让验证速度提升了 30%。」

Denys Linkov，机器学习负责人

## 开始使用

Managed Agents 的记忆功能现已在 Claude Platform 上开放公测。访问 [Claude Console](https://platform.claude.com/workspaces/default/memory-stores)，或使用我们新的 CLI 来部署你的第一个带记忆的智能体。查阅[文档](https://platform.claude.com/docs/en/managed-agents/memory)了解更多。
