---
title: "投机解码如何将 vLLM 性能提升至多 2.8x"
title_en: "How Speculative Decoding Boosts vLLM Performance by up to 2.8x"
source: https://vllm.ai/blog/2024-10-17-spec-decode
crawled: 2026-09-12
translated: 2026-09-12
---

# 投机解码如何将 vLLM 性能提升至多 2.8x

> 原文：[How Speculative Decoding Boosts vLLM Performance by up to 2.8x](https://vllm.ai/blog/2024-10-17-spec-decode) · vLLM 博客

vLLM 团队

[#投机解码](https://vllm.ai/blog/tags/speculative-decoding)[#性能](https://vllm.ai/blog/tags/performance)

vLLM 中的投机解码（Speculative Decoding）是一项强大的技术，它通过大小模型协同工作来加速 token 生成。在这篇博客中，我们将拆解 vLLM 中的投机解码、它的工作原理，以及它带来的性能提升。

*本文内容来自我们双周一次的 vLLM Office Hours 中的一个场次，我们在其中讨论优化 vLLM 性能的技术与更新。你可以[在此查看该场次幻灯片](https://docs.google.com/presentation/d/1wUoLmhfX6B7CfXy3o4m-MdodRL26WvY3/edit#slide=id.p1)。如果你更喜欢观看，可以[在 YouTube 上查看完整录像](https://youtu.be/eVJBFajJRIU?si=9BKjcFkhdOwRcIiy)。欢迎你[参加未来的场次](https://neuralmagic.com/community-office-hours/?utm_campaign=vLLM%20Office%20Hours&utm_source=vllm-blog)——请注册！*

## 投机解码简介

投机解码（[Leviathan et al., 2023](https://arxiv.org/abs/2211.17192)）是降低大语言模型（LLM）token 生成延迟的关键技术。这种方法利用较小的模型处理较简单的 token 预测，同时使用较大的模型来验证或修正这些预测。通过这种方式，投机解码在不牺牲精度的情况下加速生成，是一种无损且高效的 LLM 性能优化方法。

**为什么投机解码能降低延迟？** 传统上，LLM 以自回归方式逐个生成 token。例如，给定一个提示，模型生成三个 token T1、T2、T3，每个都需要单独一次前向传播。投机解码改变了这一过程，允许在一次前向传播中提出并验证多个 token。

其流程如下：

1. **草稿模型（Draft Model）**：一个更小、更高效的模型逐个提出候选 token。
2. **目标模型验证（Target Model Verification）**：更大的模型在单次前向传播中验证这些 token，确认正确的 token 并修正错误之处。
3. **一次传播生成多个 token**：这种方法不是每次传播生成一个 token，而是同时处理多个 token，从而降低延迟。

![](https://vllm.ai/blog-assets/figures/spec-decode/figure8.png)
如上图所示，草稿模型提出了五个 token：["I", "like", "cooking", "and", "traveling"]。它们随后被送入目标模型做并行验证。在这个例子中，第三个 token "cooking"（应为 "playing"）预测不准确。因此，这一步只生成了前三个 token ["I", "like", "playing"]。

通过这种方式，投机解码加速了 token 生成，使其成为小规模和大规模语言模型部署都适用的有效方法。

## 投机解码在 vLLM 中的工作方式

在 vLLM 中，投机解码与系统的**连续批处理**（Continuous Batching）架构集成在一起：不同请求在同一批中一起处理，以实现更高吞吐量。vLLM 使用两个关键组件来实现这一点：

- **Draft Runner**：该 runner 负责执行较小的模型来提出候选 token。
- **Target Runner**：target runner 通过运行较大的模型来验证这些 token。

vLLM 的系统经过优化，可以高效处理这一流程，让投机解码与连续批处理无缝协作，从而提升整体系统性能。

![](https://vllm.ai/blog-assets/figures/spec-decode/figure1.png)
示意图：draft runner 与 target runner 在 vLLM 批处理系统中的交互方式。

为了在 vLLM 中实现投机解码，必须修改两个关键组件：

1. **调度器（Scheduler）**：调度器经过调整，以处理单次前向传播中的多个 token 槽位，实现多个 token 的同时生成与验证。
2. **内存管理器（Memory Manager）**：内存管理器现在要同时管理草稿模型和目标模型的 KV 缓存，确保投机解码过程中的平滑处理。

![](https://vllm.ai/blog-assets/figures/spec-decode/figure9.png)
vLLM 中投机解码的系统架构。

## vLLM 支持的投机解码类型

vLLM 支持三种类型的投机解码，各自针对不同的工作负载和性能需求：

### 基于草稿模型的投机解码

![](https://vllm.ai/blog-assets/figures/spec-decode/figure2.png)

这是最常用的投机解码形式：由较小的模型预测后续 token，较大的模型进行验证。一个常见示例是使用 Llama 68M 模型为 Llama 2 70B 模型预测 token。这种方式需要精心选择草稿模型，以平衡精度与开销。

选择正确的草稿模型对于最大化投机解码的效率至关重要。草稿模型必须足够小以避免产生显著开销，同时又要足够准确以带来有意义的性能提升。

然而，挑选合适的草稿模型可能颇具挑战。例如，在 Llama 3 等模型中，由于词表大小的差异，很难找到合适的草稿模型。投机解码要求草稿模型与目标模型共享同一词表，在某些情况下这会限制投机解码的使用。因此，我们在接下来的章节中介绍几种无需草稿模型的投机解码方法。

### Prompt Lookup Decoding（提示查找解码）

![](https://vllm.ai/blog-assets/figures/spec-decode/figure3.png)
prompt lookup decoding 示例。给定提示，我们构建所有 2-gram 作为查找键（key），值（value）为该查找键后面的三个 token。在生成过程中，我们会检查当前 2-gram 是否匹配任何键。若匹配，我们就用对应的值提出后续 token。

这种方法又称 n-gram 匹配，对摘要和问答等提示与答案存在大量重叠的使用场景非常有效。系统不使用小模型来提出 token，而是根据提示中已有的信息进行推测。当大模型在答案中重复提示的部分内容时，这种方法效果尤佳。

### Medusa/Eagle/MLPSpeculator

![](https://vllm.ai/blog-assets/figures/spec-decode/figure4.png)
*图片来自 https://github.com/FasterDecoding/Medusa*。在该示例中，三个头（head）被用来为接下来的三个位置提出 token。头 1 为第一个位置提出 ["is", "\'", "the"]。头 2 为第二个位置提出 ["difficult", "is", "\'"]。头 3 为第三个位置提出 ["not", "difficult", "a"]。所有头都以最后一个 transformer 块的输出作为输入。

在这种方法中，大模型自身会添加额外的层（或头），使其能够在单次前向传播中预测多个 token。这不再需要单独的草稿模型，而是利用大模型自身的能力进行并行 token 生成。虽然尚处于初步阶段，但随着更多优化内核的开发，这种方法在提升效率方面展现出前景。

## 投机解码的性能洞察：加速与取舍

投机解码在**低 QPS（每秒查询数）**环境中能带来显著的性能收益。例如，在 ShareGPT 数据集的测试中，vLLM 使用基于草稿模型的投机解码时，token 生成实现了最高 1.5x 的加速。类似地，将 prompt lookup decoding 应用于 CNN/DailyMail 等摘要数据集时，加速最高可达 2.8x。

![](https://vllm.ai/blog-assets/figures/spec-decode/figure5.png)   ![](https://vllm.ai/blog-assets/figures/spec-decode/figure6.png)
性能对比：在 QPS=1、4xH100 上，Llama3-70B 使用草稿模型（turboderp/Qwama-0.5B-Instruct）在 ShareGPT 上投机解码带来最高 1.5x 加速；使用 n-gram 在 CNN Dailymail 上带来最高 2.8x 加速。

然而，在**高 QPS 环境**中，投机解码可能引入性能取舍。当系统本就受计算限制（compute-bound）时（如每秒请求数增加时所见），提出和验证 token 所需的额外计算有时反而会拖慢系统。在这些情况下，投机解码的开销可能超过其收益，导致性能下降。

![](https://vllm.ai/blog-assets/figures/spec-decode/figure7.png)
在高 QPS 下，我们观察到 4xH100 上 Llama3-70B 在 ShareGPT 上有 1.4x 减速、在 CNN Dailymail 上有 1.8x 减速。

## 路线图：动态调整以获得更好性能

为克服投机解码在高 QPS 场景下的局限，vLLM 正在实现**动态投机解码**（dynamic speculative decoding）。详情欢迎查阅[论文](https://arxiv.org/abs/2406.14066)。这也是 vLLM 的活跃研究方向之一！该特性将让 vLLM 根据系统负载和草稿模型的准确率调整投机 token 的数量。大体而言，当系统负载较高时，动态投机解码会缩短提议长度；但当平均 token 接受率较高时，这种缩减会不那么明显，如下图所示。

![](https://vllm.ai/blog-assets/figures/spec-decode/figure10.png)

未来，系统将能够自动调整每一步的投机程度，确保投机解码无论在何种工作负载下都始终有益。这将让用户可以放心启用投机解码，而无需担心它是否会拖慢系统。

## 如何在 vLLM 中使用投机解码

在 vLLM 中配置投机解码非常简单。启动 vLLM 服务器时，只需包含必要的标志来指定投机模型、token 数量和张量并行大小。

以下代码将 vLLM 配置为离线模式，使用草稿模型进行投机解码，一次推测 5 个 token：

```
from vllm import LLM

llm = LLM(
    model="facebook/opt-6.7b",
    speculative_model="facebook/opt-125m",
    num_speculative_tokens=5,
)
outputs = llm.generate("The future of AI is")

for output in outputs:
    print(f"Prompt: {output.prompt!r}, Generated text: {output.outputs[0].text!r}")
```

以下代码将 vLLM 配置为投机解码时通过匹配提示中的 n-gram 来生成提议：

```
from vllm import LLM

llm = LLM(
    model="facebook/opt-6.7b",
    speculative_model="[ngram]",
    num_speculative_tokens=5,
    ngram_prompt_lookup_max=4,
    ngram_prompt_lookup_min=1,
)
outputs = llm.generate("The future of AI is")

for output in outputs:
    print(f"Prompt: {output.prompt!r}, Generated text: {output.outputs[0].text!r}")
```

有时，你可能希望草稿模型使用与目标模型不同的张量并行大小以提升效率。这让草稿模型占用更少的资源、承担更少的通信开销，而把更消耗资源的计算留给目标模型。在 vLLM 中，你可以将草稿模型配置为张量并行大小 1，而目标模型使用大小 4，如下例所示。

```
from vllm import LLM

llm = LLM(
    model="meta-llama/Meta-Llama-3.1-70B-Instruct",
    tensor_parallel_size=4,
    speculative_model="ibm-fms/llama3-70b-accelerator",
    speculative_draft_tensor_parallel_size=1,
)
outputs = llm.generate("The future of AI is")

for output in outputs:
    print(f"Prompt: {output.prompt!r}, Generated text: {output.outputs[0].text!r}")
```

未来的更新（[论文](https://arxiv.org/abs/2406.14066)、[RFC](https://github.com/vllm-project/vllm/issues/4565)）将让 vLLM 自动选择投机 token 的数量，免去手动配置之需，进一步简化流程。

请跟随我们的文档《[vLLM 中的投机解码](https://docs.vllm.ai/en/v0.6.0/models/spec_decode.html)》上手使用。[欢迎参加我们的双周 Office Hours 提问并给出反馈](https://neuralmagic.com/community-office-hours/)。

## 结语：vLLM 中投机解码的未来

vLLM 中的投机解码带来了显著的性能提升，尤其是在低 QPS 环境中。随着动态调整机制的引入，它即使在高 QPS 环境下也将成为极为有效的工具，成为降低 LLM 推理延迟、提高效率的通用且不可或缺的特性。
