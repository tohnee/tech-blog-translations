---
title: "指令微调如何改进基础模型"
title_en: "How Instruction Finetuning Improves Base Models"
source: https://sebastianraschka.com/faq/docs/instruction-finetuning-practical-usefulness.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 指令微调如何改进基础模型

指令微调教会模型「一条格式化的用户消息应当对应一个恰当的回复」，从而让基础模型更易用。基础检查点已从海量文本中学到了下一 token 预测。如果一个提示看起来像某个网页或论坛帖子的开头，模型可能会延续那个模式，而不是直接回答请求。

微调数据提供示范。每条记录包含一条指令、可选的上下文，以及一个目标回复。训练之前，这些字段会按模型的对话模板序列化，使角色标记和分隔符与推理时出现的完全一致。

![指令记录在被用于监督微调之前，先被转换成一致的提示-回复格式](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/04.webp)

优化目标仍然是下一 token 预测。给定格式化后的提示和之前的回复 token，监督微调会提高示范回复出现的概率。许多实现只对助手 token 计算直接损失。系统 token 和用户 token 仍然作为条件影响回复，但训练目标并不要求模型复现这些提示 token。

![可以对提示 token 的目标做掩码，使损失直接为期望的助手回复打分](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/13.webp)

这带来若干实际变化。模型更倾向于回答提问而不是继续续写提示，更愿意遵循诸如「返回合法 JSON」之类的约束，并使用预期的对话角色。一个多样的指令数据集还能教会同一个检查点在摘要、信息抽取、改写、分类和问答之间切换，而无需为每项任务单独微调。

回复的分布反映了示范数据。如果数据集中简洁回答占主导，模型往往会变得简洁。如果记录一贯包含标题或分步解答，这些模式出现的概率就会上升。这正是为什么[数据集构造](https://sebastianraschka.com/faq/docs/build-instruction-dataset.html)和对话模板与训练循环本身同等重要。如果推理时使用的模板与微调时不同，检查点的表现可能很差。

指令微调主要改变的是预训练能力被引导和呈现的方式。它可以教会回复中包含的狭窄领域信息，但不能可靠地替代大规模预训练或检索。它也不能消除幻觉，或保证被要求的约束总能得到遵守。

[DPO](https://sebastianraschka.com/faq/docs/dpo-vs-supervised-finetuning.html) 等偏好方法往往在之后进行。监督式指令微调向模型展示一个可供模仿的回复。偏好优化则比较多个备选回复，调整模型偏好哪些回复特征。工具使用训练和推理训练是额外的维度，而不是指令微调自动带来的结果。

微调的数量和质量仍然需要控制。重复的样本可能让无用的短语留下烙印，狭窄的数据会削弱领域之外的性能，激进的优化则可能使检查点偏离有用的预训练行为过远。应使用留出集（held-out set）检验指令遵循、格式、事实准确性，以及需要保留的原有能力。
