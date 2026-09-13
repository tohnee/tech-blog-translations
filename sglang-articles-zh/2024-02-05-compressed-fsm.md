---
title: "利用压缩有限状态机为本地 LLM 实现快速 JSON 解码"
title_en: "Fast JSON Decoding for Local LLMs with Compressed Finite State Machine"
author: "Liangsheng Yin, Ying Sheng, Lianmin Zheng"
date: "Feb 5, 2024"
previewImg: /images/blog/compressed_fsm/demo.gif
source: https://lmsys.org/blog/2024-02-05-compressed-fsm/
translated: 2026-09-12
---

# 利用压缩有限状态机为本地 LLM 实现快速 JSON 解码

> 原文：[Fast JSON Decoding for Local LLMs with Compressed Finite State Machine](https://lmsys.org/blog/2024-02-05-compressed-fsm/) · LMSYS Blog · Liangsheng Yin, Ying Sheng, Lianmin Zheng

约束 LLM 使其始终生成符合特定 schema 的有效 JSON 或 YAML，是许多应用的一项关键功能。在这篇博文中，我们介绍一项能显著加速这类受限解码（constrained decoding）的优化。我们的方法利用压缩有限状态机（compressed finite state machine），兼容任意正则表达式，因此可支持任意 JSON 或 YAML schema。与每步只解码一个 token 的现有系统不同，我们的方法会分析正则表达式的有限状态机，压缩其中的单一转移路径，并在可行时<u>单步解码多个 token</u>。与最先进的系统（guidance + llama.cpp、outlines + vLLM）相比，我们的方法可将延迟最高降低 2 倍、吞吐量最高提升 2.5 倍。这项优化还使受限解码变得比普通解码更快。你现在就可以在 [SGLang](https://github.com/sgl-project/sglang/tree/main?tab=readme-ov-file#json-decoding) 上试用它。

<img src="/images/blog/compressed_fsm/demo.gif" style="width: 100%; max-width: 100%; margin-left: auto; margin-right: auto; margin-bottom: auto"></img>
<p style="color:gray; text-align: center;">
图 1：SGLang 与 Outlines + vLLM 在 JSON 解码上的对比
</p>

## 背景

[JSON](https://en.wikipedia.org/wiki/JSON) 是最重要的数据交换格式之一。要求 LLM 始终生成有效的 JSON，可以让模型输出易于以结构化方式解析。OpenAI 也认识到了它的重要性，推出了 [JSON mode](https://platform.openai.com/docs/guides/text-generation/json-mode)，约束模型始终返回有效的 JSON 对象。然而，通常还需要更细粒度的控制，以确保生成的 JSON 对象符合特定的 [schema](https://json-schema.org/)，例如

<img src="/images/blog/compressed_fsm/json_schema.png" style="width: 100%; max-width: 80%; margin-left: auto; margin-right: auto; margin-bottom: auto"></img>
<p style="color:gray; text-align: center;">
图 2：遵循 JSON Schema 进行受限生成的示例
</p>

对于本地 LLM，主要有两种方法可以引导模型生成遵循特定 schema 的 JSON 对象。

### 方法一：基于有限状态机

这种方法需要先将 JSON schema 转换为正则表达式，然后基于该正则表达式构建[有限状态机（FSM）](https://en.wikipedia.org/wiki/Finite-state_machine)，并用它来引导 LLM 生成。对于 FSM 中的每个状态，我们都可以计算出允许的状态转移，并确定可接受的下一个 token。这样就能在解码过程中跟踪当前状态，并通过对输出施加 logit bias 来过滤掉无效 token。想深入了解这种方法，可以阅读 [outlines](https://arxiv.org/abs/2307.09702) 论文。

<img id = "figure3" src="/images/blog/compressed_fsm/method1.png" style="width: 100%; max-width: 100%; margin-left: auto; margin-right: auto; margin-bottom: auto"></img>
<p style="color:gray; text-align: center;">
图 3：基于 FSM 与 logits 掩码的受限解码。第一轮受限解码只允许
<code>age</code>。第二轮中，由于正则表达式要求数字，<code>0</code> 和 <code>1</code> 都被允许，但 LLM 会以更高的概率采样 <code>1</code>。
</p>

基于 FSM 的方法使用通用正则表达式来定义底层规则，可适用于广泛的语法，例如 JSON schema、IP 地址和电子邮件。

**局限性：**  
由于 FSM 是在 token 层面构建的，每一步只能让状态转移一个 token。因此，它一次只能解码一个 token，导致解码速度缓慢。

### 方法二：交错式（Interleaved-Based）

除了把整个 JSON schema 转换为正则表达式之外，另一种做法是采用交错式解码。在这种方法中，给定的 JSON schema 会被拆分为若干部分，每部分要么是分块预填充（chunked prefill）部分，要么是受限解码部分。这些不同的部分由推理系统交错执行。由于分块预填充可以在一次前向传播中处理多个 token，因此它比逐 token 解码更快。

[Guidance](https://github.com/guidance-ai/guidance?tab=readme-ov-file#guidance-acceleration) 以 llama.cpp 为后端，为交错式解码提供了一套语法规则。

<img src="/images/blog/compressed_fsm/method2.png" style="width: 100%; max-width: 85%; margin-left: auto; margin-right: auto; margin-bottom: auto"></img>
<p style="color:gray; text-align: center;">图 4：Guidance 中的交错式 JSON 解码</p>

**局限性：**  
- 交错式方法需要自定义语法，因此不如独立的正则表达式通用，表达能力也不如后者。
- 由于解码片段与分块预填充片段之间可能存在冲突，它难以正确处理分词边界。
- 解释器与后端之间频繁的通信会带来额外开销。

## 我们的方法：基于压缩有限状态机的前跳解码（Jump-Forward Decoding）

通过引入一种新的解码算法——基于压缩有限状态机的**前跳（jump-forward）解码**，我们可以把基于 FSM 的方法与交错式方法的优点结合起来。

在由 JSON schema 转换而来的正则表达式所引导的解码过程中，当我们到达某些特定节点时，就可以预测接下来会出现的字符串：

- 在[图 3](#figure3)中，解码开始时，根据正则表达式可以预判即将出现的字符串是：
    ```json
    {
      "name":
    ```
    接下来才进入真正的解码部分。
- 类似地，当 LLM 在填写某个角色的学院（house）属性时输出了 `G`，我们就可以确定地预测接下来的字符串是 `ryffindor`，从而补全完整的字符串 `Gryffindor`。

这正是前跳解码算法加速解码的原理。在前跳算法中，我们检查给定正则表达式的有限状态机，识别出所有单一转移边（singular transition edges），并把连续的单一转移边压缩在一起，构成**单一路径（singular paths）**。对这些单一路径，我们不再逐 token 解码，而是直接对它们进行预填充（扩展，extend），一路前跳，直到下一个分支点。

<img src="/images/blog/compressed_fsm/compare.png" style="width: 100%; max-width: 100%; margin-left: auto; margin-right: auto; margin-bottom: auto"></img>
<p style="color:gray; text-align: center;">图 5：基于压缩 FSM 的前跳解码与普通解码的对比</p>

SGLang 的 RadixAttention 机制极大地简化了前跳解码算法的实现。执行前跳时，我们只需终止当前请求，再入队一个新请求。SGLang 运行时中的 RadixAttention 和高效的 **extend** 原语会自动复用之前 token 的 KV 缓存，从而避免冗余计算。

### 分词边界处理

在实现受限解码时，由于字符与 token 之间可能存在复杂的映射关系，分词边界的处理一直是个棘手的问题。

在 LLM 解码过程中，模型可能更倾向于（即以更高的概率）把多个字符合并为一个 token。例如，在 JSON 解码场景中解码 <code style="color: black; background-color: lightblue;">"Hello"</code> 时，LLM 可能输出这样的 token：

<code style="color: black; background-color: lightblue;">"</code> <code style="color: black; background-color: lightblue;">He</code> <code style="color: black; background-color: lightblue;">llo</code> <code style="color: black; background-color: lightblue;">",</code>

对于最后一个 <code style="color: black; background-color: lightblue;">"</code>，模型总是倾向于把它与后面的 <code style="color: black; background-color: lightblue;">,</code> 合并成一个更常见的 token <code style="color: black; background-color: lightblue;">",</code>，而不是单独解码它。这种效应可能导致一些奇怪的行为。例如，在上面的例子中，如果把正则表达式设为 <code style="color: black; background-color: lightblue;">"[\w\d\s]*"</code>（不含最后的 <code style="color: black; background-color: lightblue;">,</code>），就可能导致无限解码，因为 LLM 想用 <code style="color: black; background-color: lightblue;">",</code> 结束，但这个 token 是不被允许的。

此外，在前跳解码过程中，我们发现对前跳部分采用不同的分词策略，可能导致后续 token 具有不同的 logit 分布。简单地把前跳部分分词后的结果追加到当前 token 序列中，可能会产生意想不到的结果。

为了解决这些问题，我们提出了以下方案：
- 我们在前跳阶段实现了一个重新分词（re-tokenization）机制：先追加字符串本身（而非 token），再对整个文本重新分词。这种方法有效解决了大部分分词问题，而计算开销只略有增加，约为 4\%。
- 优先使用一个完整的正则表达式来引导整个解码过程，而不是使用多个拼接的正则表达式。这种做法能确保 FSM 和 LLM 都了解整个解码过程，从而尽可能减少与边界相关的问题。

你还可以阅读这篇[博客文章](http://blog.dottxt.co/coalescence.html)，了解更多相关讨论。

## 基准测试结果

我们在两个任务上对前跳解码进行了基准测试：

- 根据一段简短的提示词，以 JSON 格式生成一个角色的数据。
- 从长文档中提取一座城市的信息，并以 JSON 格式输出。

我们在 NVIDIA A10 GPU（24GB）上测试了 llama-7B，使用的版本为 vllm v0.2.7、guidance v0.1.0、outlines v0.2.5 和 llama.cpp v0.2.38（Python 绑定）。下图展示了这些方法的吞吐量（使用各系统支持的最大批大小）和延迟（批大小为 1）：

<img src="/images/blog/compressed_fsm/result.png" style="width: 100%; max-width: 60%; margin-left: auto; margin-right: auto; margin-bottom: auto"></img>
<p style="color:gray; text-align: center;">
图 6：基准测试结果
</p>

结果表明，采用我们解码算法的 SGLang 显著优于所有其他系统，可将延迟最高降低 2 倍、吞吐量最高提升 2.5 倍。在角色生成任务中，即使不启用 Jump-Forward，SGLang 的吞吐量也高于 Outlines+vLLM；我们怀疑这是由于 Outlines 存在一定开销。

## 应用案例

我们与 [Boson.ai](https://boson.ai/) 一起测试了这项功能两周，他们正在把它引入生产用例，因为它能以更高的解码吞吐量保证响应的稳定可靠。

此外，还有用户利用视觉语言模型 LLaVA，借助这项功能从图像中提取结构化信息。

<img src="/images/blog/compressed_fsm/llava_demo.gif" style="width: 100%; max-width: 100%; margin-left: auto; margin-right: auto; margin-bottom: auto"></img>
<p style="color:gray; text-align: center;">
图 7：使用 SGLang 与 LLaVA 从图像中提取结构化信息
</p>

## 链接
- 你现在就可以在 [SGLang](https://github.com/sgl-project/sglang/tree/main?tab=readme-ov-file#json-decoding) 中试用这项功能。
- 基准测试代码见[这里](https://github.com/sgl-project/sglang/tree/main/benchmark/json_jump_forward)。
- 我们感谢 [outlines](https://github.com/outlines-dev/outlines) 开源了它的 FSM 实现，我们的压缩 FSM 正是基于它构建的。
