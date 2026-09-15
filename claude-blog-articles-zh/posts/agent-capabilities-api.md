---
title: "Anthropic API 上构建智能体的新能力"
title_en: "New capabilities for building agents on the Anthropic API"
source: https://claude.com/blog/agent-capabilities-api/
crawled: 2026-09-14
translated: 2026-09-14
---

# Anthropic API 上构建智能体的新能力

> 原文：[New capabilities for building agents on the Anthropic API](https://claude.com/blog/agent-capabilities-api/) · Claude 博客

今天，我们宣布 Anthropic API 上的四项新能力，帮助开发者构建更强大的 AI 智能体：代码执行工具（code execution tool）、MCP 连接器（MCP connector）、Files API，以及最长一小时的提示缓存（prompt caching）。

### 构建更好的 AI 智能体

结合 [Claude Opus 4 和 Sonnet 4](https://www.anthropic.com/news/claude-4)，这些 beta 功能让开发者能够构建这样的智能体：执行代码以完成高级数据分析、通过 MCP 服务器连接外部系统、跨会话高效地存储和访问文件，并借助经济高效的缓存将上下文维持长达 60 分钟——而且无需自建定制基础设施。

例如，一个项目管理 AI 智能体可以用 MCP 连接器对接 Asana 来查看任务和分配工作，通过 Files API 上传相关报告，用代码执行工具分析进度与风险，并在全程保持完整上下文——同时通过扩展提示缓存把成本压在低位。

这些新能力与[网络搜索](https://www.anthropic.com/news/web-search-api)、[引用](https://www.anthropic.com/news/introducing-citations-api)等既有功能一起，构成一套完整的 AI 智能体构建工具箱。请继续阅读，深入了解每一项新能力。

### 代码执行工具

我们在 Anthropic API 上推出了[代码执行工具](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/code-execution-tool)，让 Claude 能够在沙箱环境中运行 Python 代码，产出计算结果和数据可视化。这使 Claude 从一个"写代码的助手"转变为一名数据分析师：它可以在 API 调用内部迭代可视化效果、清洗数据集并直接提炼洞见。

借助代码执行工具，Claude 可以加载数据集、生成探索性图表、识别模式，并根据执行结果迭代优化输出——全部在单次交互中完成。这意味着 Claude 可以端到端地处理复杂的分析任务，而不是仅仅建议一段代码让你自己去运行。

关键使用场景包括：

- **金融建模**：生成财务预测、分析投资组合、计算复杂的金融指标。
- **科学计算**：执行仿真、处理实验数据、分析研究数据集。
- **商业智能**：创建自动化报告、分析销售数据、生成性能仪表板。
- **文档处理**：跨格式提取和转换数据、生成排版好的报告、自动化文档工作流。
- **统计分析**：对数据集执行回归分析、假设检验和预测建模。

每个组织每天可获得 50 小时的代码执行工具免费用量，超出部分按每容器每小时 $0.05 计费。请查阅[文档](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/code-execution-tool)进一步了解定价。

### MCP 连接器

Anthropic API 上的 [MCP 连接器](https://docs.anthropic.com/en/docs/agents-and-tools/mcp-connector)让开发者无需编写任何客户端代码，就能把 Claude 连接到任何远程 Model Context Protocol（MCP）服务器。

此前，连接 MCP 服务器需要自己构建客户端执行框架（harness）来处理 MCP 连接。现在，Anthropic API 会自动处理所有连接管理、工具发现和错误处理。只需在 API 请求中添加一个远程 MCP 服务器 URL，即可立即使用强大的第三方工具，大幅降低构建具备工具调用能力智能体的复杂度。

当 Claude 收到配置了 MCP 服务器的请求时，它会自动：

- 连接到指定的 MCP 服务器
- 获取可用工具
- 推理应该调用哪个工具、传入哪些参数
- 以智能体方式执行工具调用，直到获得足够好的结果
- 管理身份验证与错误处理
- 返回整合了数据之后的增强响应

日益壮大的远程 MCP 服务器生态意味着，你可以轻松地为 AI 应用增加能力，而不必构建一次性的集成。你可以接入任何远程 MCP 服务器，包括来自 [Zapier](https://zapier.com/mcp) 和 [Asana](https://developers.asana.com/docs/using-asanas-model-control-protocol-mcp-server) 的服务器。更多远程 MCP 服务器请参见我们的[文档](https://docs.anthropic.com/en/docs/agents-and-tools/remote-mcp-servers)。

### Files API

[Files API](https://docs.anthropic.com/en/docs/build-with-claude/files) 简化了开发者在使用 Claude 构建时存储和访问文档的方式。你不必再在每次请求中管理文件上传，而是只需上传一次文档，即可在多轮对话中反复引用。

这精简了开发工作流，对于需要处理大规模文档集合的应用尤其有用，例如知识库、技术文档或数据集。

Files API 将与代码执行工具集成，使 Claude 能够在代码执行期间直接访问和处理已上传的文件，并把图表等文件作为响应的一部分产出。这意味着开发者只需通过 Files API 上传一次数据集，Claude 就能在多个会话中反复分析它，无需重新上传。

### 扩展提示缓存

开发者现在可以在[提示缓存](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)标准的 5 分钟生存时间（TTL）与[扩展的 1 小时 TTL](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching#1-hour-cache-duration-beta)之间选择，后者需支付[额外费用](https://docs.claude.com/en/docs/build-with-claude/prompt-caching#pricing)——这是 12 倍的时长提升，可以降低长时间运行智能体工作流的开销。借助扩展缓存，客户可以向 Claude 提供大量背景知识与示例，同时把长提示的成本降低最多 90%、延迟降低最多 85%。

这让构建长时间保持上下文的智能体变得切实可行——无论是处理多步骤工作流、分析复杂文档，还是与其他系统协调。此前因成本高得离谱而无法落地的长时运行智能体应用，如今可以高效地规模化运行。

### 开始使用

所有这些功能现已在 Anthropic API 上开放公测（public beta）。[访问我们的文档](https://docs.anthropic.com/en/docs/overview)了解更多，或[观看我们开发者大会的主题演讲](https://www.youtube.com/live/EvtPBaaykdo)，看看这些能力的实际演示。

FAQ（常见问题）
