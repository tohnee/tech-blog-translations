---
title: "不让一个 token 掉队：解密 Miles 中的 Token-In-Token-Out（TITO）"
title_en: "No Token Left Behind: Demystifying Token-In-Token-Out in Miles"
author: "Miles Team: Jiajun Li, Yuzhen Zhou, Shi Dong, Yanbin Jiang, Mao Cheng, Yusheng Su, Yueming Yuan, Zhichen Zeng, Banghua Zhu"
date: "June 5, 2026"
source: https://lmsys.org/blog/2026-05-13-no-token-left-behind/
previewImg: /images/blog/tito/definition.png
translated: 2026-09-12
---

# 不让一个 token 掉队：解密 Miles 中的 Token-In-Token-Out（TITO）

> 原文：[No Token Left Behind: Demystifying Token-In-Token-Out in Miles](https://lmsys.org/blog/2026-05-13-no-token-left-behind/) · LMSYS Blog · Miles 团队：Jiajun Li, Yuzhen Zhou, Shi Dong, Yanbin Jiang, Mao Cheng, Yusheng Su, Yueming Yuan, Zhichen Zeng, Banghua Zhu

在智能体强化学习（agentic RL）中，一次 rollout 并不是单次的生成，而是由模型调用、工具输出、执行框架（harness）消息和续写生成串成的一条链。Token-In-Token-Out（TITO）是一项设计原则，用于解决这一过程中训练-推理失配的一个关键来源：训练器所评估的 token 序列，是否与推理引擎在 rollout 期间实际消费和生成的 token 序列完全一致。在这篇博客中，我们希望阐明 TITO 原则的定义方式、它在 RL 训练中为何重要，以及该原则是如何在 Miles 框架中落地的。

## TITO 的定义

在一次 agentic rollout 中，模型会与外部环境反复交互。在一个简化的设定下，模型首先收到一段任务描述并生成 token，其中可能包含推理内容和一次工具调用。agent 运行时解析该工具调用，将其发送给对应的环境或工具后端，并把结果作为新的观察（observation）返回。模型接着从该观察继续生成，可能再发起一次工具调用。这个循环不断重复，直到任务完成。

注意，这一过程包含多次对推理引擎的独立调用，人们通常将其俗称为*轮（turn）*。在每一轮中，引擎接收一个 token 序列作为输入，并生成另一个 token 序列。如果对任意 $n$，第 $n-1$ 轮的完整 token 序列（prompt + response）都是第 $n$ 轮 prompt token 序列的**位级完全一致前缀（bit-perfect prefix）**，我们就说 TITO 原则得到了满足。下图展示了这一思想。

![TITO 定义示意图](/images/blog/tito/definition.png)

## 为什么 TITO 重要？

### 训练效率：每任务一个样本

在智能体强化学习中，单个任务可能包含几十轮交互，为 RL 训练器打包数据时，我们基本上有两种选择：

1. **每轮一个样本（One Sample Per Turn）：** 把每一轮当作一个独立的训练样本。
2. **每任务一个样本（One Sample Per Task）：** 把所有轮次"粘接"成一个连续序列。

我们来比较这两种选择。选项 1 中，训练器收到的样本数等于一条轨迹中的轮数；而选项 2 中，无论轮数多少，训练器对每个任务实例总是只收到一个样本。对一个典型的 SWE-Bench 类任务，一条轨迹通常由 30-50 轮组成，这意味着要摄取同样多的信息，选项 2 相比选项 1 只需付出少一个数量级的计算量。计算成本的这种大幅降低，使选项 2 在扩大智能体强化学习训练规模时格外有吸引力。

**2026 年 8 月 18 日更新：** 在 [TITO](https://miles.radixark.com/docs/user-guide/agentic-rollout) 的基础上，Miles 正在为 Claude Code 和 Codex 这类黑盒智能体执行框架开发训练支持。在各个模型家族上，CPU 往返测试与真实的 SGLang GPU 会话都验证了 R3、OPD 和 zero-KL 对齐所需的 token 级精确性。子智能体（subagent）与上下文压缩使得每个任务的轨迹数量是动态的。Session Server V2 会记录包含精确 token ID、logprob 和损失掩码的完整轨迹树，然后尽力（best-effort）将样本与其掩码合并；最终可能会保留多个样本。训练在由此形成的动态全局 batch 上进行损失归一化。

### 数学正确性：保持 on-policy 特性

一个训练样本要成为 on-policy 样本，其中每个被采样的 token 都应当在训练器中、于产生它的那个条件分布下被评估。在 Transformer 模型中，该条件分布完全取决于该 token 之前的前文。如果 TITO 被破坏，就可能存在某个 token $x_t$，使得

- 在训练器中，模型基于前序序列 $\mathbf{x}$ 评估 $x_t$；
- 在推理引擎中，模型基于略有不同的前序序列 $\tilde{\mathbf{x}}$ 采样出 $x_t$。

即便训练器与推理引擎共享完全相同的权重，条件概率 $\pi(x_t|\mathbf{x})$ 与 $\pi(x_t|\tilde{\mathbf{x}})$ 也可能出现巨大差异。这种差异最终会导致更新行为失常，危及 RL 训练的稳定性。

## TITO 可能如何被破坏

尽管概念上很简单，TITO 原则却相当脆弱。下面我们给出三个常见的场景（实际远不止这些），在这些场景中该原则可能被破坏。

### 场景 1：反分词-再分词失配（Detokenize-Retokenize Mismatch）

在多轮 RL rollout 中，人们可能把模型生成的 token 反分词（detokenize）成字符串再存储，然后在构建第 $n$ 轮的 prompt 时再将其重新分词（retokenize）。这可能会破坏 TITO 原则，因为**模型生成的 token 未必能在"反分词-再分词"的往返过程中原样保留**。

根本原因在于分词器编码文本的方式与模型生成 token 的方式之间存在不对称：

- **`encode`（文本 → token）是一对一的**：对给定输入字符串，分词器总是选择一种标准切分（通常是贪心/最长匹配）。
- **`decode`（token → 文本）是多对一的**：多个不同的 token 序列可以解码出完全相同的字符串。模型能够——有时也确实会——生成一个合法但非标准的 token 序列。

![反分词-再分词失配](/images/blog/tito/scenario1-retokenize.png)

**示例**：假设模型生成了两个独立的 token `Hel(3)` 和 `lo(7)`。把它们解码会得到字符串 `"Hello"`。然而，当你对 `"Hello"` 重新编码时，分词器会按规范把它编码成单个 token `Hello(4)`。原来的 `Hel(3)` + `lo(7)` 序列就永远丢失了，导致训练器评估的是一个模型从未真正采样过的 token 序列。

### 场景 2：推理内容被对话模板剪掉

对话模板（chat template）把一个类似 JSON 的消息列表转换成发给推理引擎的一段 prompt 字符串。一些推理模型的模板引入了我们所说的**思考截断边界（cut-thinking boundary）**：对话中的某个位置，位于该位置之前的历史 assistant 推理内容会从渲染出的 prompt 中被移除。在 [Qwen3](https://huggingface.co/spaces/huggingfacejs/chat-template-playground?modelId=Qwen%2FQwen3-4B&example=tool-usage) 和 [Kimi K2](https://huggingface.co/spaces/huggingfacejs/chat-template-playground?modelId=moonshotai%2FKimi-K2-Instruct&example=tool-usage) 这类推理模型的默认对话模板中，这个边界由最后一条 `User` 消息决定。模板渲染对话时，会丢弃出现在最后一条 `User` 消息之前的 `Assistant` 推理内容，只保留该边界之后的推理内容。

然而，智能体执行框架经常在任务中途注入 `User` 消息——例如，Terminus-2 执行框架用 `User` 消息传递终端输出，而其他一些执行框架则用它来传递"Parse failed"这类引擎重试提示。每一次注入都会把思考截断边界向前推进，悄无声息地抹掉模型实际采样得到的推理内容，破坏轮次之间的位级一致前缀。下图展示了这种行为。

![思考截断边界被破坏](/images/blog/tito/scenario2-cut-think.png)

### 场景 3：对话模板重渲染带来的有损转换

许多推理引擎接受消息列表作为输入，并在每次调用时重新应用对话模板加分词器来构建 prompt。这很方便，但也很危险：对话模板是在*字符串*层面工作的——裁剪空白、处理转义、重新打包推理内容——因此对同一条消息，模板产出的 token ID 可能取决于这条消息是*何时*、与*哪些消息一起*被渲染的。

因此，在消息层面重新应用对话模板也会引入意料之外的文本漂移。下面是一个具体的失败模式。在第 $n-1$ 轮，assistant 发出一次工具调用，其流式 token 解码出来是一段紧凑的 JSON——逗号和冒号后没有空格，键的顺序是模型自己选定的：

```json
{"name":"bash","arguments":{"cmd":"ls"}}
```

引擎解析这个字符串，并将其作为结构化的 `tool_calls` 字段存储在 assistant 消息上。到了第 $n$ 轮，当模板重新渲染对话时，它会通过 `tojson` 过滤器把 `tool_calls` 重新序列化。由于这种"先解析再序列化"的往返过程天然会丢失原始的字节级格式（空格、换行），过滤器会套用自己默认的空格风格，输出：

```json
{"name": "bash", "arguments": {"cmd": "ls"}}
```

注意每个逗号和冒号后面多出来的空格。语义相同，字节*不同*，token ID 也*不同*。位级一致前缀就这样被破坏了。

## TITO 在 Miles 中的实现

Miles 用四个组件实现了 TITO，其设计目标是：核心不变量可以被机械化地验证，同时接入新模型的成本很低。

### （1）推理会话服务器

*推理会话（inference session）*是单条轨迹与推理引擎之间的交互——属于同一任务的轮次序列，共享一个不断增长的 token 缓冲区。[推理会话服务器](https://github.com/radixark/miles/blob/3270915550fcd69dce788f382fa8c12548a63618/miles/rollout/session/session_server.py#L24)是一个薄薄的服务层，以会话 id 为键维护每条轨迹的状态。在每个 id 下，它持有一个不断增长的 token 缓冲区 `P`，每一轮都原地追加。该 token 缓冲区保留了每个样本精确的 token 级信息（logprob、路由专家），因此可以直接发送给训练。

![推理会话服务器架构](/images/blog/tito/session-server.png)
<p style="text-align: left; color: #666; font-style: italic;">TITO 推理会话服务器的流程。</p>

### （2）在三个层级上保证只追加（append-only）

*只追加（append-only）*意味着每一轮都在上一轮数据的基础上延伸，而不改写任何更早的字节。Miles 在三个层级上强制这一点：

**层级 1——消息列表。** 第 $n$ 轮的消息列表是在第 $n-1$ 轮的消息列表尾部追加新消息得到的；更早的消息字典从不被修改。

**层级 2——对话模板渲染。** 对话模板可能通过剪掉更早的内容（场景 2），或者根据执行框架追加了哪些消息角色而渲染出不同结果，来破坏 append-only。为防止剪裁，Miles 提供了[固定的 jinja 模板](https://github.com/radixark/miles/blob/95e3208ff583938fbffbe3e58d9495e9dafa2a7c/miles/utils/chat_template_utils/templates/qwen3_fixed.jinja#L43)，通过 `clear_thinking: false` 关键字参数禁用思考截断，从而在轮次之间保留历史推理内容。为防止依赖角色的渲染漂移，用户通过 `--tito-allowed-append-roles` 声明预期追加的消息角色，Miles 会为该角色集合自动选择前缀稳定的模板配置。

**层级 3——token 序列。** 对这些渲染结果做分词，必须产生符合 TITO 定义的位级一致 token 前缀。即使层级 2 成立，朴素的重新分词也会破坏这一点。Miles 完全避免重新分词：每一轮只对新追加的消息做分词，并把得到的 ID 原地追加。下一节介绍的可插拔 TITO 分词器，正是让这种只追加分词得以实现的关键。

### （3）可插拔的 TITO 分词器

每当执行框架追加一条新的非 assistant 消息时，TITO 分词器负责扩展 `P`——即推理会话服务器为每条轨迹维护的 token 缓冲区。它会计算需要拼接（splice）到 `P` 上的增量 token，以及部分模型在拼接点所需的边界补丁。

**基本思路——dummy-prefix（哑前缀）增量分词。** 具体做法（灵感来自[这篇博客](https://jybsuper.github.io/posts/multiturn_tokenization/)）是：

1. 构造一个合成的最小上下文。
2. 分别在有新消息和没有新消息的情况下各渲染一次对话模板。
3. 对字节差异进行编码。

得到的差异（delta）就是新序列化的内容，Miles 从中推导出要追加到 `P` 上的增量 token。

举例来说，假设 `P` 中已经持有截至第 $n-1$ 轮的分词前缀，而执行框架现在追加了一条工具响应：

```python
old_messages = [system, user, assistant]
new_messages = old_messages + [
    {"role": "tool", "content": "file1.txt\nfile2.txt"},
]
```

以 Qwen3 的模板为例，该工具响应对应的字节差异是：

```
<|im_start|>user
<tool_response>
file1.txt
file2.txt
</tool_response><|im_end|>
```

对它进行编码，就得到要追加到 `P` 上的增量 token。

**拼接点补丁（splice-point patches）。** 上面介绍的基本做法假设引擎放入 `P` 的 token，已经与标准模板在该位置的渲染结果一致。然而，真实模型常常违反这一假设，需要在拼接点做少量针对具体模型的补丁。Miles 通过 TITO 分词器中的一个 hook 来处理：

- **Qwen3。** 模型在 `<|im_end|>` 处停止生成，但对话模板以 `<|im_end|>\n` 结束每一轮，因此 `P` 缺少结尾的换行 token。Miles 在拼接增量 token 之前，先把缺失的 `\n` token 补上。
- **GLM-4.7。** 模型把 `<|user|>` 或 `<|observation|>` 同时当作停止 token 和下一条消息的起始 token 采样，而执行框架接下来可能注入另一种角色，导致 `P` 末尾留下错误的边界 token。Miles 在拼接增量 token 之前，会用与即将到来的角色相匹配的正确边界 token 覆盖那个错误 token——同时把被替换位置的损失掩码置零，保证这次替换不会被训练到。

下面的示意图展示了 Qwen3 和 GLM-4.7 的拼接点补丁是如何工作的。

![Qwen3 拼接点补丁](/images/blog/tito/qwen3-splice.png)
<p style="text-align: left; color: #666; font-style: italic;">Qwen3 拼接点补丁。引擎在 <code>&lt;|im_end|&gt;</code> 处停止，但标准对话模板以 <code>&lt;|im_end|&gt;\n</code> 结束每一轮。Miles 在为下一条消息拼接增量 token 之前，先把缺失的 <code>\n</code> 追加到 <code>P</code>。</p>

![GLM-4.7 拼接点补丁](/images/blog/tito/glm47-splice.png)
<p style="text-align: left; color: #666; font-style: italic;">GLM-4.7 拼接点补丁。模型把 <code>&lt;|user|&gt;</code> 或 <code>&lt;|observation|&gt;</code> 同时当作停止与下一条消息起始 token 采样，但执行框架接下来可能注入另一种角色。Miles 在拼接增量 token 之前，先用与即将到来的角色相匹配的正确 token 覆盖 <code>P</code> 中错误的边界 token（损失掩码置零，因此不会被训练到）。</p>

### （4）通过 token 序列比较器做验证

每次 rollout 之后，我们都会检查 token 缓冲区 `P` 是否与从头渲染完整消息列表时对话模板会产出的结果一致。如果 `P` 不一致，训练器读到的就是模型从未真正见过的上下文——训练会悄无声息地漂离 on-policy。Miles 提供了 [`TokenSeqComparator`](https://github.com/radixark/miles/blob/3270915550fcd69dce788f382fa8c12548a63618/miles/utils/chat_template_utils/token_seq_comparator.py#L57) 来执行这项检查。

记 `actual` 为 `P`，`expected` 为把消息列表重新经过对话模板渲染得到的 token。我们不能简单地逐 token 比较：如场景 1 所述，同一段文本可以编码成不同的 token ID，因此严格的相等检查会把无害的重新分词误判为失败。

为了跳过这些无害的重新分词、同时仍然抓住真正的 bug，Miles 采用了一种文本-token 混合检查：

1. **结构检查**：在消息边界特殊 token 处（例如 Qwen3 的 `<|im_start|>` / `<|im_end|>`，但不包括 `<think>` / `</think>`）切分 `actual` 和 `expected`，并验证两者的特殊 token 序列一致。
2. **文本检查**：把特殊 token 之间的片段解码回文本并比较字符串，因此那些解码后文本完全相同的重新分词差异可以通过。

即便有了上述检查，模型仍然可能产生偏离对话模板预期格式的输出。`Assistant` 文本一致性被破坏的几种常见方式包括：

- 工具调用边界周围的空格或换行（场景 3）
- 未闭合的 `<think>` 块
- `<think>` 周围的换行被剥离或多余

![Assistant 文本异常](/images/blog/tito/assistant-anomalies.png)

由于这类情况的存在，assistant token 上的失配不可避免；Miles 会记录它们并标记为非关键。所有其他失配——特殊 token 序列和非 assistant 文本——必须保持为零，因为这些区域是确定性的，任何偏差都意味着 TITO 存在真正的 bug。

两个验证脚本在所有受支持的（模型，追加角色集合）组合上运行这个比较器：一个 [CPU/快速层](https://github.com/radixark/miles/blob/89b0683dd8f5cbcb108215df9b04cd53e687d562/scripts/tools/verify_chat_template.py)作用于渲染出的 token 序列，另一个 [GPU/端到端层](https://github.com/radixark/miles/blob/95e3208ff583938fbffbe3e58d9495e9dafa2a7c/scripts/tools/verify_session_tito_tokenizer.py)在真实模型推理下重复同样的检查。任何一层失败，都会在该改动进入训练之前将其拦下。

## 支持的模型

TITO 流水线目前原生支持以下模型（思考与非思考模式变体均支持）：

- **Qwen**：Qwen3、Qwen3.5、Qwen3-Next
- **GLM**：GLM-4.7、GLM-5、GLM-5.1
- **Kimi**：Kimi-K2、Kimi-K2.5、Kimi-K2.6
- **Nemotron**：Nemotron-3
- **Minimax**：Minimax-M2.5、Minimax-M2.7
- **Deepseek**：Deepseek-v3.2、Deepseek-v4

对每个模型（Deepseek-v3.2 和 Deepseek-v4 除外），TITO 都经过验证，能够处理执行框架在第一条 assistant 消息之后可能追加的下列消息角色组合：

- `{tool}`：只注入工具输出的执行框架。
- `{tool, user}`：还会注入 `User` 角色消息的执行框架，例如终端输出（如 Terminus-2）或解析器重试提示。
- `{tool, user, system}`：还会在任务中途注入 `System` 角色提醒的执行框架。

Deepseek-v3.2 和 Deepseek-v4 目前仅支持 `{tool}` 这一种组合；扩展它们——就像接入任何新模型一样——通常只需要一份固定的 Jinja 模板加上一个小小的 [`merge_tokens`](https://github.com/radixark/miles/blob/3270915550fcd69dce788f382fa8c12548a63618/miles/utils/chat_template_utils/tito_tokenizer.py) 覆盖。如此低的成本正是设计的核心所在：TITO 在让每一次 rollout 都对训练保持位级精确的同时，保持了低廉的扩展成本，从而不让任何一个 token 掉队。

**如果你想在 Miles 中试用 TITO，请参阅[这里](https://miles.radixark.com/docs/user-guide/agentic-chat-template)的文档。**
