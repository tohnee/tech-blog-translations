---
title: "上下文检索（Contextual Retrieval）介绍"
title_en: "Introducing Contextual Retrieval"
source: https://www.anthropic.com/engineering/contextual-retrieval
published: 2024-09-19
crawled: 2026-09-11
translated: 2026-09-11
---

# 上下文检索（Contextual Retrieval）介绍

> 原文：[Introducing Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) · Anthropic Engineering Blog

AI 模型要在特定场景中发挥作用，往往需要获取背景知识。例如，客服聊天机器人需要了解其服务的具体业务，法律分析机器人则需要掌握大量过往案例。

开发者通常使用检索增强生成（Retrieval-Augmented Generation，RAG）来增强 AI 模型的知识。RAG 是一种从知识库中检索相关信息并将其附加到用户提示上的方法，能显著提升模型的回答质量。问题在于，传统的 RAG 方案在编码信息时会把上下文丢掉，这常常导致系统无法从知识库中检索到相关信息。

在这篇文章中，我们介绍一种能大幅改进 RAG 检索环节的方法。该方法名为「上下文检索」（Contextual Retrieval），包含两项子技术：上下文化嵌入（Contextual Embeddings）和上下文化 BM25（Contextual BM25）。这种方法可以把检索失败的数量降低 49%，与重排序（reranking）结合使用时更能降低 67%。这些都是检索准确率上的显著提升，并直接转化为下游任务表现的改善。

你可以借助[我们的 cookbook](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide)，用 Claude 轻松部署自己的上下文检索方案。

### 关于「直接用更长的提示」的一点说明

有时候最简单的方案就是最好的方案。如果你的知识库小于 200,000 token（约 500 页材料），你完全可以把整个知识库直接放进给模型的提示里，无需 RAG 或类似方法。

几周前，我们为 Claude 发布了[提示缓存（prompt caching）](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)功能，让这种方法在速度和成本上都显著更优。开发者现在可以在多次 API 调用之间缓存常用提示，将延迟降低 2 倍以上、成本最多降低 90%（阅读我们的 [prompt caching cookbook](https://platform.claude.com/cookbook/misc-prompt-caching) 可以了解其工作原理）。

不过，随着知识库规模增长，你需要更具扩展性的方案。这正是上下文检索的用武之地。

## RAG 入门：扩展到更大的知识库

对于超出上下文窗口容量的更大知识库，RAG 是典型解决方案。RAG 通过以下步骤对知识库进行预处理：

1. 把知识库（文档「语料库」）切分成较小的文本分块（chunk），通常不超过几百个 token；
2. 使用嵌入模型（embedding model）把这些分块转换为编码了语义的向量嵌入；
3. 把这些嵌入存入向量数据库，以便按语义相似度检索。

运行时，当用户向模型输入查询时，系统利用向量数据库根据与查询的语义相似度找到最相关的分块，然后把这些最相关的分块加入发送给生成模型的提示中。

嵌入模型虽然擅长捕捉语义关系，但可能错过关键的字面精确匹配。所幸有一种更老的技术可以在这些情况下补位。BM25（Best Matching 25）是一种利用词法匹配来寻找精确词或短语匹配的排序函数，对于包含唯一标识符或专业术语的查询尤其有效。

BM25 建立在 TF-IDF（词频-逆文档频率）概念之上。TF-IDF 衡量一个词对集合中某篇文档的重要程度；BM25 对其做了改进，考虑文档长度并对词频应用饱和函数，以防常见词主导结果。

下面是 BM25 在语义嵌入失效之处成功的例子：假设用户在技术支持数据库中查询「错误代码 TS-999」。嵌入模型可能找到关于错误代码的一般性内容，却可能错过「TS-999」这个精确匹配；BM25 则会查找这个特定字符串，从而定位相关文档。

通过以下步骤结合嵌入与 BM25 两种技术，RAG 方案可以更准确地检索到最适用的分块：

1. 把知识库（文档「语料库」）切分成较小的文本分块，通常不超过几百个 token；
2. 为这些分块创建 TF-IDF 编码和语义嵌入；
3. 用 BM25 依据精确匹配找出排名靠前的分块；
4. 用嵌入依据语义相似度找出排名靠前的分块；
5. 用排序融合（rank fusion）技术合并步骤 (3) 和 (4) 的结果并去重；
6. 把排名前 K 的分块加入提示以生成回答。

通过同时利用 BM25 和嵌入模型，传统 RAG 系统能够给出更全面、更准确的结果，在精确的词面匹配与更宽泛的语义理解之间取得平衡。

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F45603646e979c62349ce27744a940abf30200d57-3840x2160.png&w=3840&q=75)

一个标准的检索增强生成（RAG）系统，同时使用嵌入和最佳匹配 25（BM25）来检索信息。TF-IDF（词频-逆文档频率）衡量词的重要性，是 BM25 的基础。

这种方案让你能够以划算的成本扩展到极其庞大的知识库，远超单个提示所能容纳的规模。但这些传统 RAG 系统有一个重大局限：它们常常破坏上下文。

### 传统 RAG 中的上下文难题

在传统 RAG 中，文档通常被切成较小的分块以便高效检索。这种做法对许多应用行之有效，但当单个分块缺乏足够的上下文时会出问题。

例如，假设你的知识库里嵌入了一批金融信息（比如美国 SEC 备案文件），你收到这样一个问题：*「ACME 公司 2023 年第二季度的营收增长是多少？」*

一个相关分块可能包含这样的文字：*「该公司营收较上一季度增长 3%。」*然而，这个分块本身没有说明指的是哪家公司、哪个时间段，这使得检索正确信息或有效利用该信息变得困难。

## 上下文检索登场

上下文检索通过在嵌入之前（「上下文化嵌入」）和建立 BM25 索引之前（「上下文化 BM25」），为每个分块前置（prepend）一段针对该分块的说明性上下文来解决这个问题。

回到 SEC 备案文件的例子。下面是一个分块被转换后的样子：

```
original_chunk = "The company's revenue grew by 3% over the previous quarter."

contextualized_chunk = "This chunk is from an SEC filing on ACME corp's performance in Q2 2023; the previous quarter's revenue was $314 million. The company's revenue grew by 3% over the previous quarter."
```

值得注意的是，利用上下文改进检索的其他方法过去也有人提出，包括：[为分块添加通用文档摘要](https://aclanthology.org/W02-0405.pdf)（我们实验后发现收益非常有限）、[假设性文档嵌入（hypothetical document embedding）](https://arxiv.org/abs/2212.10496)以及[基于摘要的索引](https://www.llamaindex.ai/blog/a-new-document-summary-index-for-llm-powered-qa-systems-9a32ece2f9ec)（我们评估后发现表现不佳）。这些方法与本文提出的方法不同。

### 实现上下文检索

当然，要为知识库中成千上万甚至数百万个分块手工标注上下文，工作量实在太大了。为了实现上下文检索，我们求助于 Claude。我们写了一个提示，指示模型结合整篇文档的语境，为每个分块提供简明的、针对该分块的上下文说明。我们用下面的 Claude 3 Haiku 提示为每个分块生成上下文：

```
<document> 
{{WHOLE_DOCUMENT}} 
</document> 
Here is the chunk we want to situate within the whole document 
<chunk> 
{{CHUNK_CONTENT}} 
</chunk> 
Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk. Answer only with the succinct context and nothing else.
```

生成的上下文文本通常为 50-100 token，在嵌入和建立 BM25 索引之前被前置到分块上。

实际的预处理流程如下图所示：

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F2496e7c6fedd7ffaa043895c23a4089638b0c21b-3840x2160.png&w=3840&q=75)

*上下文检索是一种提升检索准确率的预处理技术。*

如果你想使用上下文检索，可以从[我们的 cookbook](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide) 开始。

### 用提示缓存降低上下文检索的成本

得益于前面提到的提示缓存特性，只有在 Claude 上才能以低成本实现上下文检索。有了提示缓存，你无需为每个分块都传入参考文档：只需把文档加载进缓存一次，之后引用先前缓存的内容即可。假设每个分块 800 token、每篇文档 8k token、上下文指令 50 token、每个分块生成 100 token 上下文，**生成分块上下文的一次性成本为每百万文档 token 1.02 美元**。

#### 实验方法

我们在多种知识领域（代码库、小说、ArXiv 论文、科学论文）、多种嵌入模型、多种检索策略和多种评估指标上做了实验。我们在[附录 II](https://assets.anthropic.com/m/1632cded0a125333/original/Contextual-Retrieval-Appendix-2.pdf) 中列出了每个领域所用的部分问答示例。

下图给出了表现最好的嵌入配置（Gemini Text 004）、取 top-20 分块时在所有知识领域上的平均表现。我们用 1 减 recall@20 作为评估指标，它衡量的是相关文档未能进入前 20 个分块的百分比。完整结果见附录——在我们评估的每一种「嵌入模型 × 知识来源」组合中，加上上下文都能提升表现。

#### 性能提升

我们的实验表明：

- **上下文化嵌入把 top-20 分块检索失败率降低了 35%**（5.7% → 3.7%）。
- **上下文化嵌入与上下文化 BM25 结合，把 top-20 分块检索失败率降低了 49%**（5.7% → 2.9%）。

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F7f8d739e491fe6b3ba0e6a9c74e4083d760b88c9-3840x2160.png&w=3840&q=75)

*上下文化嵌入与上下文化 BM25 相结合，可将 top-20 分块检索失败率降低 49%。*

#### 实现时的注意事项

实现上下文检索时，有几点需要留意：

1. **分块边界：** 留意文档切分成块的方式。分块大小、分块边界和分块重叠的选择都会影响检索表现。
2. **嵌入模型：** 虽然上下文检索在我们测试的所有嵌入模型上都能提升表现，但有些模型获益更多。我们发现 [Gemini](https://ai.google.dev/gemini-api/docs/embeddings) 和 [Voyage](https://www.voyageai.com/) 的嵌入尤为有效。
3. **定制上下文生成提示：** 我们提供的通用提示已经很好，但如果针对你的具体领域或用例定制提示，可能取得更好的效果（例如，附上一份关键术语表——某些术语可能只在知识库的其他文档中定义）。
4. **分块数量：** 往上下文窗口里放更多分块，能提高包含相关信息的概率。但信息过多也会干扰模型，所以存在上限。我们试过送入 5、10 和 20 个分块，发现 20 个是其中表现最好的选项（对比见附录），但仍值得在你的用例上做实验。

**务必运行评估（eval）：** 把加上上下文的分块传给模型、并区分哪部分是上下文、哪部分是分块本身，可能进一步改善回答生成。

## 用重排序进一步提升性能

最后一步，我们可以把上下文检索与另一种技术结合，获得更大的性能提升。在传统 RAG 中，AI 系统搜索知识库找出潜在相关的信息分块。当知识库很大时，这个初始检索往往会返回大量分块——有时多达数百个——相关性和重要性参差不齐。

重排序（reranking）是一种常用的过滤技术，用于确保只有最相关的分块被送给模型。重排序能带来更好的回答，同时降低成本和延迟，因为模型要处理的信息变少了。关键步骤如下：

1. 执行初始检索，得到潜在相关的头部分块（我们取前 150 个）；
2. 把头部 N 个分块连同用户查询一起送入重排序模型；
3. 由重排序模型根据每个分块与提示的相关性和重要性打分，选出前 K 个分块（我们取前 20 个）；
4. 把前 K 个分块作为上下文传入模型，生成最终结果。

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F8f82c6175a64442ceff4334b54fac2ab3436a1d1-3840x2160.png&w=3840&q=75)

*将上下文检索与重排序结合，最大化检索准确率。*

### 性能提升

市面上有多种重排序模型。我们使用 [Cohere 重排序器](https://cohere.com/rerank)进行测试。Voyage 也[提供重排序器](https://docs.voyageai.com/docs/reranker)，但我们没来得及测试。实验表明，在各个领域加入重排序环节都能进一步优化检索。

具体来说，我们发现重排序后的上下文化嵌入与上下文化 BM25 把 top-20 分块检索失败率降低了 67%（5.7% → 1.9%）。

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F93a70cfbb7cca35bb8d86ea0a23bdeeb699e8e58-3840x2160.png&w=3840&q=75)

*重排序后的上下文化嵌入与上下文化 BM25，可将 top-20 分块检索失败率降低 67%。*

#### 成本与延迟的考量

使用重排序的一个重要考量是对延迟和成本的影响，尤其是对大量分块做重排序时。由于重排序在运行时增加了一个额外环节，即便重排序器并行给所有分块打分，也不可避免地增加少量延迟。为更好的表现对更多分块重排序，与为更低延迟和成本对更少分块重排序，二者之间存在内在权衡。我们建议在你的具体用例上试验不同设置，找到恰当的平衡点。

## 结语

我们运行了大量测试，在不同数据集类型上比较了上述各种技术的组合（嵌入模型、是否用 BM25、是否用上下文检索、是否用重排序器、检索返回的 top-K 结果总数）。以下是我们发现的要点：

1. 嵌入 + BM25 优于单独使用嵌入；
2. 在我们测试的模型中，Voyage 和 Gemini 的嵌入最好；
3. 给模型送前 20 个分块比只送前 10 个或前 5 个更有效；
4. 为分块补充上下文能大幅提升检索准确率；
5. 有重排序优于无重排序；
6. **这些收益全部可以叠加**：要最大化性能提升，可以把（来自 Voyage 或 Gemini 的）上下文化嵌入与上下文化 BM25 相结合，再加上重排序环节，并把 20 个分块放进提示。

我们鼓励所有处理知识库的开发者使用[我们的 cookbook](https://platform.claude.com/cookbook/capabilities-contextual-embeddings-guide) 试验这些方法，解锁新的性能高度。

## 附录 I

下表按数据集、嵌入提供商、是否在嵌入之外使用 BM25、是否使用上下文检索、是否使用重排序，列出了 Retrievals @ 20 的结果明细。

[附录 II](https://assets.anthropic.com/m/1632cded0a125333/original/Contextual-Retrieval-Appendix-2.pdf) 提供 Retrievals @ 10 和 @ 5 的明细，以及每个数据集的示例问答。

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F646a894ec4e6120cade9951a362f685cd2ec89b2-2458x2983.png&w=3840&q=75)

*各数据集与嵌入提供商的 1 减 recall @ 20 结果。*

## 致谢

研究与写作：Daniel Ford。感谢 Orowa Sikder、Gautam Mittal 和 Kenneth Lien 提供关键反馈，Samuel Flamini 实现 cookbook，Lauren Polansky 协调项目，以及 Alex Albert、Susan Payne、Stuart Ritchie 和 Brad Abrams 对本文的打磨。
