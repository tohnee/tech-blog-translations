---
title: "为什么预训练 LLM 难以遵循指令"
title_en: "Why Pretrained LLMs Struggle to Follow Instructions"
source: https://sebastianraschka.com/faq/docs/pretrained-answer-questions-but-bad-instructions.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 为什么预训练 LLM 难以遵循指令

一个预训练的基座（base）模型能够回答许多问题，因为下一 token 预训练让它接触到了事实性陈述、解说、对话、代码以及问答模式。但它遵循指令的表现仍可能不稳定，因为预训练目标并不会特别奖励"满足用户请求"、"尊重每一条约束"或"返回特定格式"。

考虑一个以"Question: What is the capital of France? Answer:"结尾的提示。这类似于一种常见的文本模式，因此基座模型可能接着写出"Paris."。这个答案可以从普通的文本延续中自然产生。但如果请求要求返回一个只含一个字段、键名精确、不附带任何多余文本的 JSON 对象，模型就必须识别并遵守若干行为约束。宽泛的预训练数据中可能包含这类模式的例子，但当模型忽略其中某条约束时，预训练并不会施加专门的惩罚。

这个区别更容易被理解为**能力与响应策略的对比**。预训练提供了大部分语言能力、事实关联和任务知识。后训练（post-training）则改变当输入来自用户时，这些能力被选择和呈现的方式。

在预训练期间，每个文档都贡献下一 token 的训练目标。模型学习延续教程、新闻文章、论坛帖子、访谈记录以及许多其他格式。这些来源并不共享同一种助手策略。有些包含直接的答案，另一些则包含辩论、未完结的问题、被引用的错误，或多个相互矛盾的观点。预训练目标要求模型逼近这个宽泛的文本分布。

![Next-token pretraining maps a text prefix to likely continuations, which can include question-answer patterns without defining a single assistant behavior.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/gpt-process.webp)

这解释了基座模型几种常见的行为。模型可能重复问题、继续同时撰写对话的双方、追加第二个问题，或模仿某个网页的风格。即使这些输出对用户意图来说是糟糕的回应，它们仍可能是合理的文本延续。基座检查点对特定聊天应用所使用的系统、用户和助手角色标记也没有确定的解释方式。

提示往往能激发出更多预训练能力。一个问答式前缀、几个示例，或一个清晰的补全模式，都为模型提供了可延续的局部格式。这就是上下文学习（in-context learning）。它可以在不改变权重的情况下改善行为，尽管可靠性仍然取决于提示本身和模型的能力。

**监督指令微调**提供了更直接的训练信号。每个样本包含一条格式化指令和一条期望的响应。优化目标通常仍是下一 token 预测，但高质量的响应 token 如今恰好在推理时期望的"提示到响应"上下文中获得概率。

![Instruction finetuning teaches a formatted user request to lead to an appropriate assistant response.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/instruction-following.webp)

在大量样本的作用下，模型学到反复出现的行为模式。它更可能直接回答问题、尊重要求的格式、在恰当的位置停止，并根据指令在不同任务之间切换。底层的知识通常主要来自预训练。指令微调让这些知识更容易通过面向用户的界面被引导出来。

**聊天模板**是这一训练分布的一部分。它将角色和分隔符序列化为 token。如果推理时使用了不同的模板，或遗漏了必需的控制 token，一个 instruct 检查点的表现可能会大打折扣。提示的可见文字可能正确，但其 token 层面的组织方式对模型来说却是陌生的。

![A consistent prompt template connects the instruction records used during finetuning with the format supplied at inference time.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/prompt-style.webp)

许多流水线在监督微调之后加入**偏好优化**。偏好数据集对多个候选响应进行比较，并指出哪一个更符合诸如有帮助、简洁或语气等标准。[DPO](https://sebastianraschka.com/faq/docs/dpo-vs-supervised-finetuning.html) 或强化学习等方法随后将概率向偏好的行为偏移。这一阶段处理的是单一参考响应可能无法很好刻画的那些选择。

各阶段之间并非截然分开。预训练数据可能包含指令，监督微调可以传授狭窄的事实或技能，偏好训练也会影响任务表现。尽管如此，这种分解仍然有用：

- 预训练学习宽泛的文本模型并提供通用能力
- 监督指令微调教会"提示到响应"的行为
- 基于偏好或强化学习的训练调整模型在各种可接受行为之间的偏好

指令微调无法保证完全合规。当指令相互冲突、上下文很长、任务超出模型能力，或所要求的格式在微调数据中很少出现时，模型仍可能漏掉某条约束。它也可能产出一个格式漂亮但内容错误的答案。因此，事实准确性和指令遵循应当分开评估。

要做实用对比，请使用同一家族、同一分词器的 base 与 instruct 检查点，在各自的预期模板下测试直接的事实性问题、陌生措辞、多部分约束和精确的输出格式。这样就能区分本来就存在的知识，与经后训练变得更可靠的行为。

相关 FAQ[指令微调在实践中如何让基座模型更有用？](https://sebastianraschka.com/faq/docs/instruction-finetuning-practical-usefulness.html)更详细地跟进这套训练设置。[基座模型、instruct 模型和推理模型之间有什么区别？](https://sebastianraschka.com/faq/docs/base-vs-instruct-vs-reasoning-model.html)则把这些检查点放进更广泛的模型开发流程之中。
