---
title: "预训练 vs. 微调 vs. 指令微调"
title_en: "Pretraining vs. finetuning vs. instruction finetuning"
source: https://sebastianraschka.com/faq/docs/pretraining-vs-finetuning-vs-instruction-finetuning.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 预训练 vs. 微调 vs. 指令微调

**预训练（pretraining）**从宽泛的语料创建一个通用基座模型。**微调（finetuning）**是把预训练检查点适配到更窄用途的统称。**指令微调（instruction finetuning）**是监督微调的一种，使用"提示-响应"示范来教会类助手的行为。

这一层级关系很重要。指令微调并不是与微调并列的另一种选择，而是更宽泛的微调类别之下一种特定的数据格式与训练目标。

| 阶段 | 典型起点 | 训练数据 | 常见输出与损失 | 结果 |
| --- | --- | --- | --- | --- |
| 预训练 | 随机初始化的模型 | 大规模分词文本语料 | 词表 logit 上的下一 token 交叉熵 | 基座模型 |
| 任务微调 | 预训练检查点 | 带标签或目标输出的任务输入 | 类别损失或目标文本损失 | 专用模型 |
| 指令微调 | 预训练检查点 | 格式化提示与期望响应 | 通常只作用于响应 token 的下一 token 损失 | Instruct 模型 |

**预训练**使用自监督。一段文本序列自己提供标签，因为每个被观测的 token 都成为其前文的预测目标。对于纯解码器 LLM，模型在每个序列位置产生词表 logit，并最小化平均下一 token 交叉熵。[下一 token 预测 FAQ](https://sebastianraschka.com/faq/docs/next-token-prediction.html)详细跟进了这一计算。

![During pretraining, a GPT-style model maps token prefixes to vocabulary distributions for next-token prediction.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/gpt-process.webp)

预训练通常在非常庞大且多样的语料上更新整个模型。得到的基座检查点学到了语言结构、事实关联、代码模式以及数据中的其他规律性。它仍然是为文本延续而非为某个应用或一致的助手策略而优化的。

**任务微调**从这个预训练表示出发，在更聚焦的数据集上继续基于梯度的训练。输出接口取决于任务。代码仓库的第 6 章将一个 GPT 模型适配为垃圾邮件分类器，做法是把词表头替换为两分类输出头。交叉熵随后将这些类别 logit 与"垃圾邮件/非垃圾邮件"标签进行比较。

![Classification finetuning maps an input document to a fixed label set without requiring an instruction in the input.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch06_compressed/03.webp)

分类只是一个例子，而不是微调的定义。摘要或翻译微调可以保留词表头并在输入-输出文本对上训练。面向特定领域的继续预训练也可以从现有检查点出发，在原始的法律、医学或代码数据上保持原有的下一 token 目标。后一种做法常被称为**继续预训练（continued pretraining）**或**领域自适应预训练（domain-adaptive pretraining）**，因为它是在任务特定阶段之前调整模型的通用文本分布。

**指令微调**在 LLM 后训练中通常称为监督微调（SFT），同样保留词表输出。每条记录包含一条指令、可选的输入上下文，以及一条目标响应。聊天模板用推理时预期的相同角色标记和分隔符将这些字段序列化。

![Instruction finetuning presents a task as a user request and trains the model to generate the desired response.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch06_compressed/02.webp)

优化目标仍可以是下一 token 交叉熵。许多实现会对系统提示和用户提示的目标位置做掩码，使得只有助手响应的 token 直接贡献损失。提示仍然作为条件上下文可见。这些数据教会模型解读请求、选择合适的任务行为，并产出预期的响应格式。

指令数据集通常混合多种任务。一个检查点可能见到抽取、改写、分类、问答和结构化输出的样本。这不同于专用的垃圾邮件分类器——后者把每个输入映射到同一个固定标签空间。[指令微调 FAQ](https://sebastianraschka.com/faq/docs/instruction-finetuning-practical-usefulness.html)更详细地解释了提示格式化与损失掩码。

这些边界有用但并不绝对。指令微调可以引入其响应中包含的狭窄领域知识。任务微调也可以使用自然语言指令。最可靠的区分来自预期行为和监督目标的结构。

还有两个维度常与这些阶段混淆。**全参数微调与 LoRA 之分**描述的是更新哪些参数，而不是学习什么任务。同一个分类或指令数据集既可以配全参数权重更新，也可以配[LoRA 这类参数高效方法](https://sebastianraschka.com/faq/docs/lora-vs-full-finetuning.html)。**偏好优化**使用被接受和被拒绝的响应或奖励信号。[DPO](https://sebastianraschka.com/faq/docs/dpo-vs-supervised-finetuning.html) 等方法通常排在 SFT 之后，但它们使用的目标函数不同于基于示范的指令微调。

数据量也不是形式上的分界。预训练通常比微调规模大得多、成本高得多，尽管一次很长的继续预训练可能比小模型最初的训练语料还大。关键在于这个过程是在创建一个宽泛的基座模型，还是在把现有检查点适配到某个目标分布或行为上。

在实际选择时：当模型需要广泛接触新领域时用继续预训练；当期望输出有狭窄的任务定义时用任务微调；当希望一个生成模型响应多样的用户请求时用指令微调。一个生产级 instruct 模型之后还可能接受偏好训练或面向推理的训练，作为额外的后训练阶段。
