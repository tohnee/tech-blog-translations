---
title: "vLLM 中的结构化解码：一篇入门介绍"
title_en: "Structured Decoding in vLLM: a gentle introduction"
source: https://vllm.ai/blog/2025-01-14-struct-decode-intro
crawled: 2026-09-12
translated: 2026-09-12
---

# vLLM 中的结构化解码：一篇入门介绍

> 原文：[Structured Decoding in vLLM: a gentle introduction](https://vllm.ai/blog/2025-01-14-struct-decode-intro) · vLLM 博客

客座文章，作者：BentoML 与 Red Hat

[#性能](https://vllm.ai/blog/tags/performance)

**TL/DR**：

- 结构化解码（Structured Decoding）可以精确控制 LLM 的输出格式
- vLLM 现已同时支持 [outlines](https://github.com/dottxt-ai/outlines) 和 [XGrammar](https://github.com/mlc-ai/xgrammar) 两种结构化解码后端
- 近期的 XGrammar 集成在高负载下可将每输出 token 耗时（TPOT）提升至多 5x
- 即将发布的 v1 版本聚焦于增强性能，以及用于支持混合请求批处理的调度器级 mask 广播

*[vLLM](https://blog.vllm.ai/2023/06/20/vllm.html) 是用于运行**大语言模型**（LLM）的高吞吐、高效推理引擎。在本文中，我们将梳理语言模型的历史脉络，介绍 vLLM 中结构化解码的现状、近期与 [XGrammar](https://github.com/vllm-project/vllm/pull/10785) 的集成，并[分享我们关于未来改进的初步路线图](https://github.com/vllm-project/vllm/issues/8779)。*

> 我们也邀请读者从哲学视角阅读这篇博文，并在此过程中尝试论证：结构化解码代表了我们看待 LLM 输出方式的根本转变。它在构建复杂智能体（agentic）系统中也扮演着重要角色。

欲了解更多关于 vLLM 的信息，请查阅我们的[文档](https://docs.vllm.ai/en/latest/)。

## 语言模型：一段简短的历史背景

1950 年，Alan Turing 提出这样一个观点：用规则编程的高速数字计算机可以展现出智能的涌现行为（Turing, 1950）。这催生了 AI 发展的两大主要路径：

1. 传统人工智能（Good Old-Fashioned AI，GOFAI）：这一范式在 20 世纪 50 年代的研究者中迅速兴起，人们设计专家系统来复制人类专家的决策能力[1](#user-content-fn-1)（或称符号推理系统），Haugland 将其称为 Good Old-Fashioned AI（GOFAI）（Haugeland, 1997）。然而，由于其语义表示无法扩展到通用任务，它很快遭遇了资金问题（即所谓的"AI 寒冬"（Hendler, 2008））。
2. 新式人工智能（New-Fangled AI，NFAI）：与此同时，Donald Norman 的并行分布式处理（Parallel Distributed Processing）（Rumelhart et al., 1986）研究组考察了 Rosenblatt 感知机（Rosenblatt, 1958）的各种变体，提出在网络中、输入与输出之外加入*隐藏层*，基于训练过程中学到的内容推断合适的响应。这些连接主义网络通常构建在统计方法之上[2](#user-content-fn-2)。鉴于数据的充裕和摩尔定律[3](#user-content-fn-3)带来的空前算力，我们看到连接主义网络在研究和生产用例中全面占主导地位，最突出的就是用于*文本生成*任务的 *decoder-only* transformer 变体[4](#user-content-fn-4)。因此，大多数现代 transformer 变体都被视为 **NFAI** 系统。

总结来说：

- GOFAI 是*确定性*的、基于规则的，因为其意向性（intentionality）通过显式编程注入
- NFAI 通常被视为"黑箱"模型（输入：input - 输出：某个 output），由于其内部表示的网络化复杂性，是数据驱动的

## 为什么我们需要结构化解码？

![](https://vllm.ai/blog-assets/figures/struct-decode-intro/shogoth-gpt.png)

Shogoth 即 GPT。从某种意义上说，RLHF 或任何训练后（post-training）方法，都是向任何大型复合 AI 系统中注入规则（一个 GOFAI 系统）

LLM 擅长以下启发式任务：给定一段文本，模型会生成一段连续的文本，即它预测出的最可能的 token。例如，如果你给它一篇 Wikipedia 文章，模型应生成与该文章剩余部分一致的文本。

这些模型能良好工作基于以下假设：输入提示必须连贯且结构良好，围绕用户想要完成的给定问题。换言之，当你需要特定格式的输出时，LLM 可能不可预测。设想让模型生成 JSON——如果没有引导，它可能生成合法的文本却违反 JSON 规范[5](#user-content-fn-5)。

这就是结构化解码发挥作用的地方。它使 LLM 能够生成遵循期望结构的输出，同时保留系统的非确定性本质。

OpenAI 等公司已经认识到了这一需求，实现了 [JSON mode](https://platform.openai.com/docs/guides/structured-outputs#json-mode) 等特性来约束[6](#user-content-fn-6)输出格式。如果你曾经使用这些功能做过开发（如智能体工作流、函数调用、编程助手），那么你在底层大概率就在使用结构化解码。

> 引导解码之于 LLM，正如**校验**之于 API——它是一种保证，确保输出的内容与你的期望相符。引导解码确保了结构完整性，让开发者可以轻松将 LLM 集成到他们的应用中！

## 结构化解码与 vLLM

简而言之，结构化解码为 LLM 提供了一个可遵循的"模板"。用户提供一个模式（schema）来"影响"模型的输出，确保符合期望的结构：

![结构化解码的顶层视图](https://vllm.ai/blog-assets/figures/struct-decode-intro/mermaid-intro.svg)

结构化解码的顶层视图

从技术角度来看，推理引擎可以通过对来自任意给定 schema 的所有 token 施加偏置（通常通过 logit mask）来修改下一个 token 的概率分布。为施加这些偏置，[outlines](https://github.com/dottxt-ai/outlines) 提出了针对任意给定 schema、通过有限状态机（FSM）进行引导生成的方法（Willard & Louf, 2023）。这让我们能够在解码过程中跟踪当前状态，并通过向输出施加 logit 偏置来过滤掉无效 token。

![](https://vllm.ai/blog-assets/figures/struct-decode-intro/constrained-json-fsm.webp)

图片来自 [LMSys, 2024](https://lmsys.org/blog/2024-02-05-compressed-fsm/)，特此致谢。

*在 vLLM 中，你可以通过向采样参数传递 JSON schema 来使用它（通过 Python SDK 或 HTTP 请求均可）。*

> 注意：在某些情况下，它甚至可以[提升](https://blog.dottxt.co/coalescence.html) LLM 的原生解码性能！

### vLLM 此前的局限

vLLM 当前对 Outlines 后端的支持存在以下几点局限：

1. **解码慢**：FSM 必须在 token 级别构建，这意味着它每步只能转移一个 token 的状态。因此，它一次只能解码*一个* token，导致解码缓慢。
2. **批处理瓶颈**：[vLLM](https://github.com/vllm-project/vllm/blob/80c751e7f68ade3d4c6391a0f3fce9ce970ddad0/vllm/model_executor/guided_decoding/outlines_logits_processors.py) 中的实现严重依赖 logit processor[7](#user-content-fn-7)。因此，它位于采样过程的关键路径上。在批处理用例中，为每个请求编译 FSM 以及同步计算 mask，意味着任何给定批次中的**所有请求**都会被阻塞，导致较高的首 token 延迟（TTFT）和较低的吞吐量。
   - 我们发现 FSM 编译被证明是一项相对昂贵的任务，是 TTFT 增加的重要成因。
3. **CFG 模式的性能问题**：在 outlines 集成中，虽然 JSON 模式相对较快，但 CFG 模式的运行速度明显更慢，偶尔还会使引擎[崩溃](https://github.com/vllm-project/vllm/issues/10081)。
4. **高级特性支持有限**：像 [jump-forward decoding](https://lmsys.org/blog/2024-02-05-compressed-fsm/) 这样的技术在 logit-processor 方案下目前无法实现。它需要预填充一组 k 个后续 token，而 logit processor 只能处理下一个 token。

### 与 XGrammar 的集成

[XGrammar](https://github.com/mlc-ai/xgrammar) 引入了一种新技术，通过下推自动机（PDA）实现批量受约束解码。你可以把 PDA 想象成"一组 FSM 的集合，每个 FSM 代表一个上下文无关文法（CFG）"。PDA 的一个显著优势是它的递归本质，让我们能够执行多个状态转移。它还包含额外的[优化](https://blog.mlc.ai/2024/11/22/achieving-efficient-flexible-portable-structured-generation-with-xgrammar)（供有兴趣的读者参考）以降低文法编译开销。

这一进步将文法编译从 Python 移到了使用 `pthread` 的 C 代码中，从而解决了**局限 (1)**。此外，XGrammar 为未来版本解决**局限 (4)** 奠定了基础。下面是 XGrammar 后端与 Outlines 后端的性能对比：

![](https://vllm.ai/blog-assets/figures/struct-decode-intro/vllm-new-xgrammar.png)
![](https://vllm.ai/blog-assets/figures/struct-decode-intro/vllm-xgrammar-decode-time-per-output-token.png)

图片来自 Michael Goin（Red Hat），特此致谢。

在 vLLM 的 v0 架构中，我们将 XGrammar 实现为一个 [logit processor](https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/guided_decoding/xgrammar_decoding.py)，并通过对分词器数据进行缓存来优化它。虽然性能提升令人鼓舞，但我们认为仍有很大的优化空间。

XGrammar v0 集成在覆盖所有用例以实现特性对齐方面，仍存在一些可用性顾虑：

- 尚不支持 GBNF 格式之外的文法（vLLM 上的 PR：[github](https://github.com/vllm-project/vllm/pull/10870)）
- 尚不支持 regex
- 尚不支持使用 regex 模式或数值范围的复杂 JSON
  - 目前有几个 PR 试图覆盖这一用法。有一个 [vLLM 上的 bugfix PR](https://github.com/vllm-project/vllm/pull/10899) 和一个[上游 PR](https://github.com/mlc-ai/xgrammar/pull/106)

> vLLM 现在默认提供对 XGrammar 的基础支持。当我们知道 XGrammar 不足以服务某个请求时，会回退到 Outlines。
>
> 请注意，vLLM 也包含对 lm-format-enforcer 的支持。然而，根据我们的测试，在一些长上下文测试用例中，lm-format-enforcer 无法强制产生正确输出，性能也不及 Outlines。

## v1 的初步计划

随着 [v1](https://github.com/vllm-project/vllm/issues/8779) 发布在即，我们正在为结构化解码制定初步计划：

1. 将引导解码向调度器级别推进：
   - 原因：在调度器级别，我们对哪些请求使用结构化解码有更多上下文，因此它不应阻塞批次内的其他请求（初步解决**局限 (2)**）。从某种意义上说，这将引导解码移出关键路径。
   - 这也将允许与 jump-forward decoding 进行更自然的垂直整合（解决**局限 (4)**）。
2. 允许在一个进程中计算位掩码（bit-mask），而不是在每个 GPU worker 中重复计算
   - 原因：我们可以将这个位掩码广播给每个 GPU worker，而不是在每个 GPU worker 上重复这一过程。
   - 我们将仔细分析为每个使用引导解码的请求的每次采样广播 mask 的带宽影响。
3. 为投机解码和工具调用提供良好基线
   - 原因：XGrammar 计划支持工具调用，这样我们就可以摆脱 Python 的[工具解析器](https://github.com/vllm-project/vllm/tree/main/vllm/entrypoints/openai/tool_parsers)。
   - 投机解码中的树评分（tree scoring）随后可以使用与 jump-forward decoding 相同的 API（这依赖于引导解码在调度器级别的集成）。

*注意：如果你有任何更多建议，我们非常乐意予以考虑。欢迎通过 `#feat-structured-output` 加入 [vLLM slack](https://www.notion.so/bentoml/slack.vllm.ai)。*

## 致谢

我们感谢 vLLM 团队、XGrammar 团队、[Aaron Pham (BentoML)](https://github.com/aarnphm)、[Michael Goin (Red Hat)](https://github.com/mgoin)、[Chendi Xue (Intel)](https://github.com/xuechendi) 和 [Russell Bryant (Red Hat)](https://github.com/russellb) 在将 XGrammar 引入 vLLM 以及持续改进 vLLM 结构化解码方面提供的宝贵反馈与协作。

## 参考文献

- Bahdanau, D., Cho, K., & Bengio, Y. (2016). *Neural Machine Translation by Jointly Learning to Align and Translate*. arXiv preprint arXiv:1409.0473
- Haugeland, J. (1997). *Mind Design II: Philosophy, Psychology, and Artificial Intelligence*. The MIT Press. <https://doi.org/10.7551/mitpress/4626.001.0001>
- Hendler, J. (2008). Avoiding Another AI Winter. *IEEE Intelligent Systems*, *23*(2), 2–4. <https://doi.org/10.1109/MIS.2008.20>
- Hochreiter, S., & Schmidhuber, J. (1997). Long Short-Term Memory. *Neural Computation*.
- Kaplan, J., McCandlish, S., Henighan, T., Brown, T. B., Chess, B., Child, R., Gray, S., Radford, A., Wu, J., & Amodei, D. (2020). *Scaling Laws for Neural Language Models*. arXiv preprint arXiv:2001.08361
- Mikolov, T., Chen, K., Corrado, G., & Dean, J. (2013). *Efficient Estimation of Word Representations in Vector Space*. arXiv preprint arXiv:1301.3781
- Rosenblatt, F. (1958). The perceptron: A probabilistic model for information storage and organization in the brain. *Psychological Review*, *65*(6), 386–408. <https://doi.org/10.1037/h0042519>
- Rumelhart, D. E., McClelland, J. L., & Group, P. R. (1986). *Parallel Distributed Processing, Volume 1: Explorations in the Microstructure of Cognition: Foundations*. The MIT Press. <https://doi.org/10.7551/mitpress/5236.001.0001>
- Shortliffe, E. H. (1974). *MYCIN: A Rule-Based Computer Program for Advising Physicians Regarding Antimicrobial Therapy Selection* (Technical Report STAN-CS-74-465). Stanford University.
- Statistical Machine Translation. (n.d.). *IBM Models*. Statistical Machine Translation Survey. <http://www2.statmt.org/survey/Topic/IBMModels>
- Turing, A. M. (1950). i.—Computing Machinery And Intelligence. *Mind*, *LIX*(236), 433–460. <https://doi.org/10.1093/mind/LIX.236.433>
- Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., & Polosukhin, I. (2023). *Attention Is All You Need*. arXiv preprint arXiv:1706.03762
- Willard, B. T., & Louf, R. (2023). *Efficient Guided Generation for Large Language Models*. arXiv preprint arXiv:2307.09702

---

## 脚注

1. Allen Newell 和 Herbert Simon 在 RAND 公司的工作最初证明了计算机可以模拟智能的重要方面。

   另一个著名的应用出现在医学领域（Haugeland, 1997）。斯坦福大学在 20 世纪 70 年代开发的 MYCIN 可以为血液感染进行诊断并推荐治疗方案（Shortliffe, 1974）。MYCIN 的开发者认识到为推荐提供依据的重要性，实现了所谓的"规则轨迹"（rule traces），以人类可理解的方式解释系统的推理。[↩](#user-content-fnref-1)
2. 20 世纪 90 年代，IBM 发布了一系列复杂的统计模型，训练用于执行机器翻译[任务](https://en.wikipedia.org/wiki/IBM_alignment_models)（Statistical Machine Translation, n.d.）（另见：康奈尔大学的这堂[讲座](https://www.cs.cornell.edu/courses/cs5740/2017sp/lectures/08-alignments.pdf)）。

   2001 年，词袋（Bag of words，BoW）变体模型在 0.3B token 上训练，被视为当时的 SOTA（Mikolov et al., 2013）。这些早期工作向研究界证明：鉴于统计建模能够捕捉大规模文本语料的总体模式，它在语言处理上胜过符号方法。[↩](#user-content-fnref-2)
3. 2017 年，里程碑式论文"Attention is all You Need"为神经机器翻译任务引入了 Transformers 架构（Vaswani et al., 2023），它基于（Bahdanau et al., 2016）最先提出的注意力机制。

   随后，OpenAI 提出了神经语言模型的缩放定律（scaling law）（Kaplan et al., 2020），掀起了基于基础语言模型构建这类系统的竞赛。[↩](#user-content-fnref-3)
4. 在基于注意力的 transformer 出现之前，seq-to-seq 模型使用 RNN，因为它具有更长的上下文长度和更好的记忆能力。然而，与前馈网络相比，它们更容易出现梯度消失/爆炸问题，因此 LSTM（Hochreiter & Schmidhuber, 1997）被提出以解决这一问题。但 LSTM 的主要问题之一是，对于很多步之前见过的数据，它们的记忆召回往往很差。

   注意力论文通过向输入编码额外的位置数据解决了这一问题。该论文还额外提出了一种面向翻译任务的编码器-解码器架构，不过如今大多数文本生成模型都是 decoder-only 的，因为其在零样本（zero-shot）任务上表现更优。

   基于注意力的 transformer 之所以比 LSTM 工作得更好，原因之一在于 transformer 非常可扩展且对硬件友好（你不能随意堆叠更多 LSTM 块然后指望获得更好的长期记忆）。欲了解更多信息，请参阅原论文。[↩](#user-content-fnref-4)
5. 有人可能会说，我们可以通过少样本提示（few-shot prompting）可靠地实现这一点，例如"给我一个生成用户地址的 JSON。示例输出可以是……"。然而，这并不能保证生成的输出是合法的 JSON。这是因为这些模型是概率系统，它们基于训练数据的分布来"采样"下一个结果。

   也有人可能会说，这类场景应该使用专门微调的 JSON 输出模型。然而，微调通常需要大量训练以及更多的人力来整理数据、监控进度和执行评估，这是一笔并非人人都负担得起的巨大资源投入。[↩](#user-content-fnref-5)
6. 注意，"structured/constrained/guided decoding"这几个说法可以互换使用，但它们都指同一种机制——"使用一种格式让模型按结构采样输出"。[↩](#user-content-fnref-6)
7. 关于使用 logit processor 控制生成过程，请参阅 HuggingFace 的这篇[博文](https://huggingface.co/blog/logits-processor-zoo)。[↩](#user-content-fnref-7)
