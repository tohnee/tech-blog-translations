---
title: "为什么提示模板对 LLM 很重要"
title_en: "Why prompt templates matter for LLMs"
source: https://sebastianraschka.com/faq/docs/why-prompt-templates-matter.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 为什么提示模板对 LLM 很重要

提示模板（prompt template）之所以重要，是因为指令微调作用于 token 序列，而不是抽象的聊天消息。模板把 `system`、`user`、`assistant` 这类结构化字段转换成模型看到的角色标记、分隔符、空白符和回合结束 token。推理应当复现同样的 token 级惯例。

模型在格式不匹配时仍可能作答，尤其当可见请求很简单时。但可靠性往往会下降，因为此时的提示属于与微调所用不同的分布。典型症状包括复述用户内容、同时续写对话两侧、泄漏角色标记、无视系统消息，或在错误的位置停止。

## 提示与聊天模板是不同的对象

*提示模板*这个词被用于两个相关的概念。

- **指令模板（instruction template）**把指令、可选输入和目标回复等字段组合成一条文本记录。它可能使用诸如 `### Instruction` 和 `### Response` 的普通标题。
- **聊天模板（chat template）**把一系列带角色标签的消息序列化。它通常使用模型专用的控制 token 来表示消息开始、角色名和回合结束。

系统提示是消息内容。聊天模板决定的是这段内容及其角色如何被编码。修改系统消息改变的是指令；修改模板则可能改变每条消息四周的所有边界。

![同一条指令记录可以用普通文本标题序列化，也可以用模型专用的用户和助手标记序列化](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/prompt-style.webp)

一个简化渲染后的对话可能像这样：

```python
<|system|>
Answer concisely.<|end|>
<|user|>
What is gradient descent?<|end|>
<|assistant|>
Gradient descent is ...<|end|>
```

另一个检查点可能使用 `[INST]` 分隔符，或另一套头部与结束 token。这些格式不可互换，哪怕解码后的文本在人看来可以理解。特殊 token 的 ID 具有与该检查点共同学习得到的含义。

## 模板定义了预测边界

在有监督指令微调期间，一个序列通常包含提示和一条示范的助手回复。模型把系统和用户片段当作预测回复的上下文。许多训练管线把这些提示位置从损失中掩蔽掉，但这些 token 仍保留在输入中。

助手头部标记回复开始的位置。回合结束 token 教会模型回复在哪里结束。如果任一边界出错，模型可能学会生成一个本应由应用插入的头部，或者继续写进下一轮用户消息而不是停下。

损失掩码是与模板化相互独立的操作。一个正确的模板仍可能配一个错误的标签掩码。对于仅回复的 SFT，损失应按所选目标覆盖助手内容及其结束 token。[提示 token 掩蔽 FAQ](https://sebastianraschka.com/faq/docs/when-mask-prompt-tokens.html) 逐一分析了单轮、多轮、填充和打包的例子。

![指令微调学习的是从格式化请求到期望回复的映射，而不是从孤立指令字符串到回复的映射](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/instruction-following.webp)

## 训练与生成使用相关的结尾方式

训练样本已经包含助手回复。它们应当被渲染为完整对话，包括助手回合及其正确的结束标记。

在推理时，应用的对话通常以一条用户消息结尾。渲染出的序列可能需要一个助手起始标记，使生成在助手角色内开始。在当前的 [Hugging Face 聊天模板 API](https://huggingface.co/docs/transformers/chat_templating) 中，这一行为由 `add_generation_prompt=True` 控制。确切效果依模板而异，有些模型格式不需要额外的标记。

一次最小检查像这样：

```python
messages = [
    {"role": "system", "content": "Answer concisely."},
    {"role": "user", "content": "What is gradient descent?"},
]

input_ids = tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_tensors="pt",
)

print(tokenizer.decode(input_ids[0]))
```

对于数据集预处理，消息列表会包含助手回复，并且通常使用 `add_generation_prompt=False`。在一条完整回复之后再追加一个助手起始标记，描述的就是另一条序列了。

还有一种单独的情形叫回复预填充（response prefilling），此时最后一条助手消息包含一个应由生成继续补全的部分答案。这种情况下不应再添加新的助手起始标记。运行时需要区分"开始一个新的助手回合"与"继续当前的助手回合"。

## 特殊 token 可能被静默重复

聊天模板常常自行插入序列开始、序列结束或回合结束 token。随后的分词器调用如果把渲染好的聊天当作普通文本处理，可能再插入一份副本。

Hugging Face 文档建议尽可能在应用模板时使用 `tokenize=True`。如果先把模板渲染成文本、再单独调用分词器，就必须在第二步禁用特殊 token 的插入。否则，重复的开始或结束 token 可能改变模型行为，尽管解码后的提示看起来几乎一模一样。

空白符同样值得关注。助手回复前的一个换行、分隔符内的一个空格、或重复的模板套话都会改变分词。一个稳健的模型可能容忍一些变化，但没有理由在训练与服务之间引入意外的差异。

| 模板组成部分 | 作用 | 出错时的可能症状 |
| --- | --- | --- |
| 角色标记 | 标识系统、用户、助手或工具内容 | 模型以错误角色作答或复述另一轮 |
| 回合结束 token | 分隔已完成的消息 | 生成延续到新的发言者或提前停止 |
| 助手起始标记 | 把推理定位到回复边界 | 模型续写用户文本而不是作答 |
| 开始/结束 token | 标记序列级边界 | 空输出、重复的控制 token 或异常续写 |
| 空白符与分隔符 | 保留学到的序列化模式 | 较小但可重复的质量或格式变化 |

## 多轮和工具使用模板承载更多结构

对于多轮聊天，模板序列化的是消息的完整顺序。截断必须保留有效的角色边界。删掉一条旧的助手消息却保留依赖它的用户回复，可能产生语法有效但会话语义破碎的序列。

使用工具的模型增加更多字段。模板可能序列化工具定义、助手的工具调用、环境提供的工具结果，以及最终的助手回复。这些 schema 和控制 token 是模型专用的。在检查点期望专用工具调用片段的地方传入一个普通 JSON 字符串，可能降低工具使用的准确性，即使这个 JSON 本身是合法的。

同一边界对损失掩码也很重要。助手的工具调用 token 可以是训练目标。环境返回的工具结果通常是上下文。对 `assistant` 或 `tool` 这类词做子串搜索是不安全的，因为这些词也可能出现在消息内容中。预处理产生的 token 片段更可靠。

模板还影响上下文占用和成本。重复的角色头、系统文本、工具定义和分隔符在每个请求都消耗 token。简洁的格式可以为原始材料和生成输出留出更多空间。对于一个已有的指令检查点，缩短模板就改变了学到的格式。省 token 的改动应设计进训练，或通过受控微调和评估加以验证。

## 训练前检查渲染后的 token

我会把分词器和聊天模板视为模型工件的一部分。与检查点一起固定它们的版本，并为数据集预处理、评估和服务使用同一个序列化函数。

在长时间的微调运行之前，按以下顺序检查若干渲染样例：

1. 打印渲染文本并用转义显示空白符，使每个换行都可见。
2. 打印每个角色和回合边界附近的 token ID 或 token 字符串。
3. 确认开始和结束 token 恰好出现在预期位置。
4. 核对每个助手片段和最终结束 token 的损失掩码。
5. 渲染不带回复的推理版本，确认助手起始边界。
6. 在几个保留提示上运行贪心生成，在后处理之前检查原始 token 输出。
7. 在模型支持时，测试一次多轮对话和一次工具调用。

这些检查能在模板 bug 被误认为模型质量、学习率或解码问题之前把它们抓住。底层的规则是：让检查点、分词器、模板、标签掩码和停止配置在整个工作流中保持一致。

[指令微调 FAQ](https://sebastianraschka.com/faq/docs/instruction-finetuning-practical-usefulness.html) 解释了提示-回复示范如何改变基座模型。[指令数据集 FAQ](https://sebastianraschka.com/faq/docs/build-instruction-dataset.html) 涵盖数据集范围、格式化、评估划分和评审。
