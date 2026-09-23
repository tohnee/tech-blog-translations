---
title: "Llama 如何帮助 CodeGPT 成为顶级 AI 编程助手之一"
title_en: "How Llama helped CodeGPT become one of the top AI-powered coding assistants"
date: 2024-10-16
source: https://ai.meta.com/blog/codegpt-built-with-llama
crawled: 2026-09-22
translated: 2026-09-22
---

# Llama 如何帮助 CodeGPT 成为顶级 AI 编程助手之一

> 原文：[How Llama helped CodeGPT become one of the top AI-powered coding assistants](https://ai.meta.com/blog/codegpt-built-with-llama) · Meta AI（Wayback 存档）

CodeGPT 是一款广受欢迎的编程助手，以 Visual Studio Code 扩展或 JetBrains 集成开发环境（IDE）插件的形式提供。它集成了 Llama 这样的大语言模型，从多个方面提升开发者与 CTO 的生产力——不仅生成代码，还回答关于代码库的问题、协助调试代码，以及帮助新开发者上手现有项目。自 2023 年 3 月上线以来，CodeGPT 的下载量已超过 140 万次，用户遍布 180 多个国家，且每月新增数十万。

CodeGPT 上线几个月后，Meta 发布了 Code Llama——一个基于 Llama 2、专为响应文本提示生成代码而设计的 LLM。这立刻引起了 CodeGPT 团队的注意。「Llama 的性能和灵活性给我们留下了深刻印象。」CodeGPT 的 CTO 兼联合创始人 Daniel Avila 说。于是团队开始试验用对话式模型和填充中间内容（fill-in-the-middle）模型与代码仓库交互。实验非常成功，他们决定把 Llama 集成到 CodeGPT 平台中，用它为客户提供 AI 驱动的辅助。此后公司在这个基础上不断构建：加入了精通 API 和框架的 AI 智能体（agentic），并将 LLM 升级到 Llama 3.2（90B）。

CodeGPT 与 Llama 合作带来的影响是显著的。使用 CodeGPT 的开发者生产力至少提升 30%，因为它减少了花在调试、搜索解决方案和生成代码上的时间。该公司的客户还能大幅加快新开发者上手速度——从数月缩短到数天。

自最初提供代码建议和自动补全以来，CodeGPT 显著扩大了对 Llama 的使用。平台如今能够自主生成项目文件夹和文件，还包含一个代码库图机制，让 Llama 完整理解整个仓库的结构。开发者因此可以向 CodeGPT 提问，并借助 Llama 有效地与自己的仓库「对话」。这让任何加入项目的人都能更容易理解代码的用途，也简化了开发者在编写代码过程中的调试和信息查找。

实施过程并非没有挑战。最大的挑战是把 Llama 集成到需要 LLM 理解大型代码库的复杂工作流中。CodeGPT 通过创建上述基于图的机制解决了这个问题，使 Llama 能更整体地理解代码库。团队还优化了 Llama 以处理多步任务（例如生成代码并通过 API 调用外部工具），并花了大量时间为每个用例微调 LLM。微调的工作是把 Llama 模型优化以处理特定编程任务，比如代码自动补全、缺陷检测和探索代码仓库。为此，团队需要在广泛的代码库、编程语言和调试场景上训练模型，还整合了外部知识源，比如技术文档和热门编程论坛上的讨论。

「Llama 改变了开发者与代码库交互的方式，让编程更直观、更高效。」Avila 说，「这些模型潜力巨大，不仅在加速编程任务方面，更在从根本上重塑软件开发工作流。」

开源一直是 CodeGPT 开发过程的关键方面：CodeGPT 团队得以借助全球开发者社区的专业知识来解决问题——这带来了更快的迭代和更迅速的新功能开发。此外，Avila 说，他们的客户青睐使用开源 LLM 的能力。「我们看到用户对开源模型的巨大需求。开发者出于多种原因喜欢有开源选项，包括数据隐私。」

对于 CodeGPT 这样规模较小的公司来说，Llama 这样的开源模型让它们得以接触前沿 AI 技术，无需大规模研发预算即可快速创新。开源方案让初创公司能够构建世界级的项目。正如 Avila 所说：「CodeGPT 是开发者 AI 领域的顶尖选手之一，而 Llama 模型在其中功不可没。」

CodeGPT 对未来有宏大的计划。随着其 LLM 与开发者工具生态的演进，团队计划把最新的 Llama 模型融入更高级的功能，包括实时代码协作和 AI 驱动的重构工具。他们还在探索让 Llama 在更大规模项目中扩展应用的方式，进一步增强其仓库理解与调试能力。

分享你的 Llama 故事
