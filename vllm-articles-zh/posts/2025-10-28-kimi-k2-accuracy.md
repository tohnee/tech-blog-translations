---
title: "追求 100% 准确率：深入排查 Kimi K2 在 vLLM 上的工具调用问题"
title_en: "Chasing 100% Accuracy: A Deep Dive into Debugging Kimi K2's Tool-Calling on vLLM"
source: https://vllm.ai/blog/2025-10-28-kimi-k2-accuracy
crawled: 2026-09-12
translated: 2026-09-13
---

# 追求 100% 准确率：深入排查 Kimi K2 在 vLLM 上的工具调用问题

> 原文：[Chasing 100% Accuracy: A Deep Dive into Debugging Kimi K2's Tool-Calling on vLLM](https://vllm.ai/blog/2025-10-28-kimi-k2-accuracy) · vLLM 博客

作者：Linian Wang（北京大学）

[#模型支持](https://vllm.ai/blog/tags/model-support)[#开发者](https://vllm.ai/blog/tags/developer)

**TL;DR：** 为获得与 vLLM 的最佳兼容性，请使用聊天模板在 commit 94a4053eb8863059dd8afc00937f054e1365abbd（[Kimi-K2-0905](https://huggingface.co/moonshotai/Kimi-K2-Instruct-0905)）或 commit 0102674b179db4ca5a28cd9a4fb446f87f0c1454（[Kimi-K2](https://huggingface.co/moonshotai/Kimi-K2-Instruct)）之后更新的 Kimi K2 模型。这些更新是按模型分别提交的。

### 引言

智能体工作流正在重塑我们与大语言模型的交互方式，而健壮的工具调用正是驱动这场革命的引擎。Moonshot AI 的 Kimi K2 模型以其出色的工具调用能力著称。为了验证它在高性能 vLLM 服务引擎上的表现，我选用了官方的 [K2-Vendor-Verifier](https://github.com/MoonshotAI/K2-Vendor-Verifier) 基准测试。

我的目标颇具雄心：复现 Moonshot AI 原生 API 上近乎完美的表现。他们的官方端点树立了很高的标杆：执行数千次工具调用而 schema 校验错误为零——这是可靠性的黄金标准。

**基准测试：Moonshot AI API 上的 K2-Vendor-Verifier**

| 模型名称 | 提供方 | finish\_reason: stop | finish\_reason: tool\_calls | finish\_reason: others | Schema 校验错误 | 成功的工具调用 |
| --- | --- | --- | --- | --- | --- | --- |
| `Moonshot AI` | MoonshotAI | 2679 | 1286 | 35 | **0** | **1286** |
| `Moonshot AI Turbo` | MoonshotAI | 2659 | 1301 | 40 | **0** | **1301** |

然而，我最初在 vLLM 上运行 K2 的尝试得到了令人震惊的不同结果。开箱即用的表现不仅仅是欠佳，简直是坏的。

**vLLM 上的初始测试结果**

- **vLLM 版本：**`v0.11.0`
- **HF 模型：**`moonshotai/Kimi-K2-Instruct-0905`，commit `09d5f937b41ae72c90d7155c9a901e2b5831dfaf`

| 模型名称 | finish\_reason: stop | finish\_reason: tool\_calls | finish\_reason: others | Schema 校验错误 | 成功的工具调用 |
| --- | --- | --- | --- | --- | --- |
| `Kimi-K2-Instruct-0905`（HF 初始版本） | 3705 | 248 | 44 | 30 | **218** |

1200 多次潜在的工具调用中，只有 218 次被成功解析——成功率不足 20%。这不只是一个小 bug，而是模型与服务引擎之间通信的根本性断裂。这篇博客记录了我深入排查这一差异的过程，揭示了 Kimi K2 的 `chat_template` 与 vLLM 之间的三个关键兼容性问题。这段经历不仅帮助我们大幅提升了性能，也为任何想把复杂模型与现代服务框架集成的人提供了宝贵经验。

### 排查历程：揭示三个核心问题

### 问题 1：缺失的 `add_generation_prompt`

第一个线索是模型行为的根本性异常。在基准测试中，本应触发工具调用的请求却以 `finish_reason: stop` 结束。但根本问题更广泛：模型根本没有生成结构化的 assistant 回复。它不是在回应用户，而是用纯文本继续「接话」——这种行为在任何聊天场景中都会降低性能，而不仅仅是工具调用。

**排查过程：**

为了隔离问题，我设计了一个关键实验：不使用 vLLM 的高层 `/v1/chat/completions` 端点，而是执行两步手动流程——先在外部调用 tokenizer 的 `apply_chat_template` 函数生成完整的提示字符串，再把该字符串发送给更低层的 `/v1/completions` 端点。这个手动流程绕过了 vLLM 内部的模板应用，关键在于它解决了绝大多数失败。问题显然出在 vLLM *使用*聊天模板的方式上。

**根本原因：**

深入观察后发现，Kimi tokenizer 的 `apply_chat_template` 函数签名包含 `**kwargs`，用于接受额外的、特定于模型的参数。其中一个参数 `add_generation_prompt=True` 对于正确格式化提示、标识 assistant 回合开始并引导其生成工具调用至关重要。

正确的提示应当以特殊 token 结尾，让模型准备好以 assistant 身份行动：

```
Correct Prompt Suffix: ...<|im_assistant|>assistant<|im_middle|>

```

然而，由于 vLLM 没有传入 `add_generation_prompt=True`，提示在用户消息之后就被截断了。
这个畸形的提示让模型缺少开始自己回合的关键指令。结果，它不知道该生成工具调用、文本回复还是任何结构化响应，完全跑偏了。
之所以会发生这种情况，是因为出于 [PR #25794](https://github.com/vllm-project/vllm/pull/25794) 中详述的安全考虑，vLLM 会检查函数签名，只传递显式定义的参数。由于 `add_generation_prompt` 藏在 `**kwargs` 中，vLLM 把它丢弃了，导致提示格式化静默失败。

**修复：**

查明根本原因后，我与 Kimi 团队展开合作。他们的响应非常迅速，根据我的发现更新了 Hugging Face Hub 上模型的 `tokenizer_config.json`。修复方式是在聊天模板中显式声明 `add_generation_prompt` 为受支持的参数。这让 vLLM 能够正确传递该参数，解决了工具调用失败的主要来源。此外，我还提交了[这个 PR](https://github.com/vllm-project/vllm/pull/27622)：当 tokenizer 通过 `**kwargs` 接受参数时，将标准聊天模板参数加入白名单，防止工具调用静默失败。

### 问题 2：空的 `content` 如何让提示跑偏

第一个问题解决后，出现了一类更隐蔽的新提示格式错误。

**排查过程：**

我把这些错误追溯到了包含历史工具调用、且 `content` 字段为空字符串（`''`）的对话。我发现了一个微妙但关键的转换：vLLM 为了追求标准化的内部表示，会自动把简单的空字符串 `content: ''` 提升为更复杂的字典列表结构：`content: [{'type': 'text', 'text': ''}]`。

**根本原因：**

Kimi 基于 Jinja 的聊天模板是为渲染字符串类型的 `content` 设计的。当它意外地收到一个列表时，无法正确处理，把列表的字面字符串表示插入到了最终提示中。

**错误的提示片段：**

```
...<|im_end|><|im_assistant|>assistant<|im_middle|>[{'type': 'text', 'text': ''}]<|tool_calls_section_begin|>...

```

**正确的提示片段：**

```
...<|im_end|><|im_assistant|>assistant<|im_middle|><|tool_calls_section_begin|>...

```

这一关键的格式错误造成了一个畸形提示，足以打乱模型的生成逻辑。

**修复：**

我提议修改 `chat_template` 逻辑使其更具弹性。Kimi 团队表示同意并迅速实施了更新。模板现在会显式检查 `content` 字段的类型：如果是字符串就直接渲染；如果是可迭代对象（如列表）就正确处理，从而避免该格式错误。

### 问题 3：过于严苛的工具调用 ID 解析器

最后，我注意到即使模型生成了语法正确的工具调用，vLLM 有时也无法解析。这个问题尤其隐蔽，因为它往往并非源于当前轮次，而是源于提供给模型的对话历史。

**排查过程：**

通过检查 vLLM 的原始 `text_completion` 输出，罪魁祸首一目了然。我发现在某些边缘情况下——尤其是被畸形的对话历史误导时——模型会生成不完全符合 Kimi 官方规范的工具调用 ID。例如下面这个输出：

```
...<|tool_calls_section_begin|><|tool_call_begin|>search:2<|tool_call_argument_begin|>...

```

这里模型输出的 ID 是 `search:2`。但 [Kimi 官方文档](https://huggingface.co/moonshotai/Kimi-K2-Instruct-0905/blob/main/docs/tool_call_guidance.md)规定的格式是 `functions.func_name:idx`。

**根本原因：**

模型为什么会生成不合规的 ID？正如 Kimi 团队解释的，一个常见原因是被对话历史「带偏」。Kimi-K2 模型期望历史消息中所有工具调用 ID 都遵循 `functions.func_name:idx` 格式。但如果来自其他系统的历史消息里包含一个 ID 畸形（如 `search:0`）的工具调用，Kimi 模型可能被这种陌生格式迷惑，在响应中试图生成一个「类似」但不正确的 ID。

有趣的是，这在使用 Kimi 官方 API 时并不是问题，因为在调用 K2 模型之前，他们的 API 会自动把所有历史工具调用 ID 重命名为符合 `functions.func_name:idx` 标准的格式。这个预处理步骤就像一道护栏，而我的直接 vLLM 设置中缺少了它。

vLLM 的工具调用解析器逻辑过于脆弱，无法处理这种偏差。它严格依赖官方格式，用等价于 `function_id.split('.')[1].split(':')[0]` 的代码提取函数名。当遇到 `search:2` 时，第一次按 `.` 的切分就失败了，抛出 `IndexError`，导致整个本来有效的工具调用被丢弃。

**修复：**

Kimi 团队推荐的最有效修复，是让用户和厂商采取类似的预处理步骤：在把历史工具调用 ID 发送给模型之前，确保它们都被规范化为 `functions.func_name:idx` 格式。就我而言，修复前两个提示格式问题也显著降低了这类不合规 ID 出现的频率，因为格式正确的上下文会让模型更有可能生成正确的输出。此外，我还向 vLLM 社区提议增强解析器的健壮性，以更好地处理轻微的格式偏差（见[这个 PR](https://github.com/vllm-project/vllm/pull/27565)）。

### 最终结果与新发现

Kimi 团队应用所有修复并更新 Hub 上的 tokenizer 之后，我重新运行了 K2-Vendor-Verifier，看到了显著的改善。

**vLLM 上的最终测试结果（修复后）**

| 指标 | 数值 | 说明 |
| --- | --- | --- |
| 工具调用 F1 分数 | 83.57% | 精确率与召回率的调和平均，衡量模型是否在正确时机触发工具调用。 |
| 精确率 | 81.96% | TP / (TP + FP)。 |
| 召回率 | 85.24% | TP / (TP + FN)。 |
| Schema 准确率 | 76.00% | 语法正确且通过校验的工具调用所占比例。 |
| 成功的工具调用 | 1007 | 成功解析并通过校验的工具调用总数。 |
| 触发的工具调用总数 | 1325 | 模型尝试调用工具的总次数。 |
| Schema 校验错误 | 318 | 解析或校验失败的被触发工具调用数量。 |
| 整体成功率 | 99.925% | 4,000 个请求中成功完成的比例（3997/4000）。 |

成功解析的工具调用数量从 **218** 飙升至 **971**——**4.4x** 的提升，让我们距离官方 API 的表现更近了一步。然而，一个新问题浮出水面：316 次 `schema_validation_error_count`。深入挖掘后我发现，vLLM 上的模型有时会调用**当前请求中未声明的工具**（例如，即使当前轮次没有提供 `img_gen` 工具，也会从聊天历史中使用它）。

这是一个已知的模型幻觉问题。Moonshot AI API 等专有服务部署了一个名为 **「Enforcer」** 的关键防护组件。它充当守门员，实现受限解码（constrained decoding），确保模型*只能*生成与请求中明确提供的工具相对应的 token。vLLM 目前缺少这一特性，为开源社区未来的贡献提供了一个令人期待的切入点。Kimi 团队正在与 vLLM 团队积极合作，将 **「Enforcer」** 组件集成到 vLLM 中。

### 关键经验与最佳实践

这次深入排查为所有在 LLM 与服务基础设施交叉领域工作的人提供了几条宝贵经验：

1. **细节藏在聊天模板里：** `chat_template` 是模型与服务框架之间的关键握手。集成新模型时，要对照框架的具体行为与假设，细致验证模板逻辑的每一部分。
2. **揭开抽象层：** `/chat/completions` 这样的高层 API 很方便，但可能掩盖根本原因。调试时不要犹豫，直接下沉到 `/completions` 这类更低层的端点。手动构造输入是隔离问题的利器。
3. **进阶技巧：Token ID 是终极的事实依据：** 对于最微妙的问题，检查发送给模型的最终 token ID 序列是唯一能确定真相的方法。虽然上述问题我没有动用这一招，但它是工具箱中的关键工具。使用 OpenAI 兼容 API 返回 token ID 的技术可以救急。有兴趣的读者，我们在 [Agent Lightning 一文](https://blog.vllm.ai/2025/10/22/agent-lightning.html)中也重点介绍过这一点。
4. **理解框架的设计哲学：** vLLM 对 `**kwargs` 的严格处理不是 bug，而是出于安全考虑的刻意选择。理解这些设计决策有助于快速定位根本原因，而不是被意外行为卡住。
5. **开放生态的挑战：** 工具调用「Enforcer」这类高级特性是成熟的专有服务的标志。在 vLLM 这样的开源项目中健壮而优雅地实现这些能力，是社区必须应对的重要挑战。

### 结论

通过系统性的协作调试，我们成功解决了 Kimi K2 模型在 vLLM 上的关键工具调用兼容性问题，将其成功率提升了 4 倍以上，性能达到了预期水平。这个过程不仅是一次技术挑战，也印证了在复杂软件生态中谨慎、有条理的调查的力量。

希望这份详细记录能为其他把复杂模型集成到 vLLM 及其他平台的开发者提供有用的路线图。随着开源社区不断成熟，我们期待为大家带来更顺畅的模型集成体验和更强大的智能体能力。

![](https://vllm.ai/blog-assets/figures/kimi-k2-accuracy/k2-vendor-verifier.jpeg)

### 致谢

我要向 Kimi 团队的工程师们致以诚挚的谢意。他们深厚的专业功底对定位根本原因至关重要，而且在问题确认后迅速在 Hugging Face Hub 上实施了必要的修复。没有他们的积极协作与支持，这段旅程和它的圆满结局都不可能发生。

此外，我还要感谢 vLLM 团队的 Kaichao You 和 Chauncey Jiang，他们帮助我上手 vLLM 项目，并讲解了 vLLM 工具调用功能的种种细节。vLLM 在 LLM 服务中扮演着重要角色，深入钻研 vLLM 也帮助我理解了 LLM 的方方面面。
