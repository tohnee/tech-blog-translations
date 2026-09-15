---
title: "通过动态过滤改进网络搜索"
title_en: "Improved Web Search with Dynamic Filtering"
source: https://claude.com/blog/improved-web-search-with-dynamic-filtering/
crawled: 2026-09-14
translated: 2026-09-14
---

# 通过动态过滤改进网络搜索

> 原文：[Improved Web Search with Dynamic Filtering](https://claude.com/blog/improved-web-search-with-dynamic-filtering/) · Claude 博客

随着 Claude [Opus 4.6](https://www.anthropic.com/news/claude-opus-4-6) 和 [Sonnet 4.6](https://www.anthropic.com/news/claude-sonnet-4-6) 的发布，我们还推出了全新版本的[网络搜索](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)与[网页抓取](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool)（web fetch）工具。Claude 现在可以在网络搜索过程中原生地编写并执行代码，在搜索结果进入上下文窗口之前先对其进行过滤，从而提升准确率和 token 效率。

## **带动态过滤的网络搜索**

网络搜索是一项高度消耗 token 的任务。使用基础网络搜索工具的智能体需要发起查询、把搜索结果拉入上下文、从多个网站抓取完整 HTML 文件，并在对全部内容进行推理之后才能给出回应。但从搜索中拉入的上下文常常包含大量无关内容，这会降低回答的质量。

为了提升 Claude 在网络搜索上的表现，我们的网络搜索与网页抓取工具现在会自动编写并执行代码，对查询结果进行后处理。Claude 无需再对完整 HTML 文件进行推理，而是可以在把搜索结果加载进上下文之前动态过滤，只保留相关内容、丢弃其余部分。

我们此前已[发现](https://www.anthropic.com/engineering/advanced-tool-use)这项技术在其他智能体工作流中同样有效，并且已经添加了[代码执行](http://docs.anthropic.com/en/docs/agents-and-tools/tool-use/code-execution-tool)和[程序化工具调用](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)等工具，以便在我们的 API 上提供原生支持。现在，我们将同样的技术引入网络搜索和网页抓取。

## **评估 Claude 的网络搜索能力**‍

我们在 Sonnet 4.6 和 Opus 4.6 上对网络搜索进行了评估，分别在启用与不启用动态过滤、且不启用其他工具的条件下进行。在 [BrowseComp](https://cdn.openai.com/pdf/5e10f4ab-d6f7-442e-9508-59515c65e35d/browsecomp.pdf) 和 [DeepsearchQA](https://storage.googleapis.com/deepmind-media/DeepSearchQA/DeepSearchQA_benchmark_paper.pdf) 这两个基准测试上，动态过滤平均带来了 11% 的性能提升，同时输入 token 减少了 24%。

**BrowseComp：在网上搜索以找到一个答案**‍

BrowseComp 测试智能体能否浏览众多网站，找到一条刻意被隐藏得难以在线获取的特定信息。动态过滤显著提升了 Claude 的准确率：Sonnet 4.6 从 33.3% 提升到 46.6%，Opus 4.6 从 45.3% 提升到 61.6%。
‍

**DeepsearchQA：在网上搜索以找到多个答案**‍

DeepsearchQA 向智能体提出有多个正确答案的研究型查询，所有正确答案都必须通过网络搜索找到。它测试智能体能否系统地规划并执行多步搜索，且不遗漏任何答案。该基准以「F1 分数」来衡量，它平衡了精确率与召回率——同时反映返回答案的准确性和搜索的完整性。

动态过滤将 Claude 的 F1 分数在 Sonnet 4.6 上从 52.6% 提升到 59.4%，在 Opus 4.6 上从 69.8% 提升到 77.3%。

Token 成本会因模型为过滤上下文所需编写的代码量而异。按价格加权的 token 数在 Sonnet 4.6 的两个基准上均有所下降，但在 Opus 4.6 上有所上升。为了更好地了解你自身的成本，我们建议用一组具有代表性的、你的智能体在生产环境中可能遇到的网络搜索查询来评估这一工具。

## 客户聚焦：Quora

[Quora](https://quora.com) 旗下的 [Poe](https://poe.com) 是最大的多模型 AI 平台之一，让数百万用户通过单一界面访问 200 多个模型。Quora 内部团队发现，启用动态过滤的 Opus 4.6「在与其他前沿模型对比测试时，在我们内部评估中取得了最高准确率」，产品与研究负责人 Gareth Jones 表示。「这个模型表现得像一个真正的研究员：它会编写 Python 来解析、过滤和交叉验证结果，而不是在上下文中对着原始 HTML 进行推理。」

## 网络搜索与网页抓取工具中的动态过滤

在 Claude API 上将新版网络搜索和网页抓取工具与 Sonnet 4.6 及 Opus 4.6 搭配使用时，动态过滤将默认开启。对于复杂的网络搜索查询，例如梳理技术文档或核查引用，你可以期待获得与上文所示类似的性能提升。

在 API 中的用法如下：

```
{
  "model": "claude-opus-4-6",
  "max_tokens": 4096,
  "tools": [
    {
      "type": "web_search_20260209",
      "name": "web_search"
    },
    {
      "type": "web_fetch_20260209",
      "name": "web_fetch"
    }
  ],
  "messages": [
    {
      "role": "user",
      "content": "Search for the current prices of AAPL and GOOGL, then calculate which has a better P/E ratio."
    }
  ]
}

```

## 代码执行、记忆等更多工具正式发布

我们还将几款工具正式推向全面可用（general availability），帮助智能体在各种高 token 消耗的任务中表现更佳：

- [代码执行](http://docs.anthropic.com/en/docs/agents-and-tools/tool-use/code-execution-tool)：为智能体提供一个沙箱，使其能在对话过程中运行代码，以过滤上下文、分析数据或执行计算。
- [记忆](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)：通过持久化文件目录跨对话存储和检索信息，让智能体无需把所有内容都保留在上下文窗口中也能维持上下文。
- [程序化工具调用](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)：以代码方式执行复杂的多工具工作流，让中间结果不进入上下文窗口。
- [Tool Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)：无需将全部定义加载到上下文窗口，即可从大型工具库中动态发现工具。[‍](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use#providing-tool-use-examples)
- [工具使用示例](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use#providing-tool-use-examples)：直接在工具定义中提供示例工具调用，展示使用模式并减少参数错误。

### **开始使用**

改进后的网络搜索与网页抓取，以及代码执行、记忆、程序化工具调用、Tool Search Tool 和工具使用示例，现已在 Claude Platform 上可用。阅读我们的 [API 文档](https://platform.claude.com/docs/en/build-with-claude/overview)开始使用。

FAQ（常见问题）
