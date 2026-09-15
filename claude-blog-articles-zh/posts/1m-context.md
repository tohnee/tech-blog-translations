---
title: "Claude Sonnet 4 现已支持 1M token 上下文"
title_en: "Claude Sonnet 4 now supports 1M tokens of context"
source: https://claude.com/blog/1m-context/
crawled: 2026-09-14
translated: 2026-09-14
---

# Claude Sonnet 4 现已支持 1M token 上下文

> 原文：[Claude Sonnet 4 now supports 1M tokens of context](https://claude.com/blog/1m-context/) · Claude 博客

***更新：****现已上线 Google Cloud 的 Vertex AI（2025 年 8 月 26 日）*

Claude Sonnet 4 现已在 Anthropic API 上支持最高 100 万 token 的上下文——容量提升 5 倍，让你可以在单次请求中处理超过 75,000 行代码的完整代码库，或数十篇研究论文。

Sonnet 4 的长上下文支持现已在 Claude Developer Platform 上原生进入公测（public beta），并同步登陆 Amazon Bedrock 和 Google Cloud 的 Vertex AI。

### 更长上下文，更多使用场景

借助更长的上下文，开发者可以借助 Claude 运行更全面、更数据密集的使用场景，包括：

- **大规模代码分析：** 加载完整代码库，包括源码文件、测试与文档。Claude 能够理解项目架构、识别跨文件依赖，并基于完整的系统设计提出改进建议。
- **文档综合：** 处理大量文档集合，如法律合同、研究论文或技术规范。在保持完整上下文的同时，分析数百份文档之间的关系。
- **上下文感知智能体：** 构建能够在数百次工具调用和多步骤工作流中保持上下文的智能体。纳入完整的 API 文档、工具定义和交互历史，而不会丢失连贯性。

### API 定价

为应对更高的计算需求，超过 200K token 的[提示](https://www.anthropic.com/pricing#api)将按如下方式计价：

Anthropic API 上 Claude Sonnet 4 的定价

|  | 输入 | 输出 |
| 提示 ≤ 200K | $3 / MTok | $15 / MTok |
| 提示 > 200K | $6 / MTok | $22.50 / MTok |

结合[提示缓存](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)（prompt caching），用户可以进一步降低长上下文场景下 Claude Sonnet 4 的延迟与成本。1M 上下文窗口也可以配合[批处理](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing)使用，再节省 50% 的成本。

### 客户聚焦：Bolt.new

Bolt.new 将 Claude 集成到其基于浏览器的开发平台中，变革了 Web 开发方式。

"Claude Sonnet 4 依然是我们代码生成工作流的首选模型，在生产环境中持续超越其他领先的模型。借助 1M 上下文窗口，开发者现在可以处理规模大得多的项目，同时保持真实世界编码所需的较高准确性。"Bolt.new 的 CEO 兼联合创始人 Eric Simons 如是说。

### 客户聚焦：iGent AI

总部位于伦敦的 iGent AI 正借助 Maestro 推进软件开发领域的发展——Maestro 是一位能把对话转化为可执行代码的 AI 伙伴。

"曾经不可能的事情如今成为了现实：拥有 1M token 上下文的 Claude Sonnet 4 极大增强了我们 iGent AI 软件工程智能体 Maestro 的自主能力。这一跃迁解锁了真正的生产级工程——在真实代码库上开展持续数天的会话——确立了智能体软件工程的新范式。"iGent AI 的 CEO 兼联合创始人 Sean Ward 如是说。

### 开始使用

Sonnet 4 的长上下文支持现已在 Claude Developer Platform 上面向 Tier 4 及自定义速率限制的客户开放公测，并将在未来几周内逐步扩大可用范围。长上下文现也可在 Amazon Bedrock 和 Google Cloud 的 Vertex AI 上使用。我们也在探索如何把长上下文带到其他 Claude 产品中。

要进一步了解 Sonnet 4 与 1M 上下文窗口，请参阅我们的[文档](https://docs.anthropic.com/en/docs/build-with-claude/context-windows#1m-token-context-window)与[定价页面](https://www.anthropic.com/pricing#api)。

FAQ（常见问题）
