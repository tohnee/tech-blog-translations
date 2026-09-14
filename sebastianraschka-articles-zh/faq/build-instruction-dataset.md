---
title: "从零构建指令数据集有哪些好方法？"
title_en: "What are good ways to build an instruction dataset from scratch?"
source: https://sebastianraschka.com/faq/docs/build-instruction-dataset.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 从零构建指令数据集有哪些好方法？

> 原文：[What are good ways to build an instruction dataset from scratch?](https://sebastianraschka.com/faq/docs/build-instruction-dataset.html) · Sebastian Raschka's FAQ

首先要写下微调后模型应当学会的行为。一个用于总结科学文章的数据集，所需要的提示词和答案与客服或代码生成的数据集不同。这个范围决定了哪些任务应纳入数据集，以及什么样的回答算是好回答。

接下来，选定一种记录格式并始终保持一致。仓库中第 7 章的示例使用了 `instruction`、`input` 和 `output` 等字段。当指令本身已包含全部所需上下文时，input 字段可以留空。在预处理时，每条记录都应映射到同一个聊天模板，这样模型才能可靠地区分请求与期望的回答。

我会先构建一个仍然便于逐行检查的小型种子集。这些示例应当来自模型预期要处理的真实任务。在此范围内，让提示词措辞、回答长度和难度有所变化会很有帮助。这些变化应当反映实际使用情形，而不是为了多样性而人为制造多样性。

![Instruction tuning works best when examples consistently teach the model what a user request looks like and what a good response should look like](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/instruction-following.webp)

尽早划分训练集和评估集。来自同一来源或同一提示词模板的示例应留在同一个划分中。否则，训练提示词的一个合成改写版本可能泄漏到评估集中，使结果看起来比实际更好。

一旦种子数据质量过关，就可以用 LLM 来帮助扩充。仓库第 7 章的工具中包含了用 Llama 3 和 Ollama 生成指令数据、创建变体、以及通过反思微调（reflection tuning）改进回答的示例。合成输出仍然需要质量控制。我会检查事实性错误、被忽略的约束、格式损坏，以及仅仅复述提示词的回答。

去重应在训练之前完成。精确字符串匹配可以抓出重复记录，而基于相似度的检查对于改写和轻度编辑的副本很有用。重复的提示词会让某一种行为被过度加权，而跨划分的重复会污染评估结果。

![The repo's reflection-tuning material shows an iterative dataset workflow in which generated responses are inspected and refined](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/reflection-tuning/reflection-tuning.webp)

在开始长时间的微调之前，我会再做一次人工通读。随机抽样有助于发现系统性的格式问题。困难示例则适合用来检查期望的答案是否真的正确。此外，核实数据中不含隐私材料、且数据来源允许预期用途，也是值得做的事。

一组规模适中、经过审阅的示例就是合理的第一个版本。训练之后，错误分析可以指出缺少哪些任务类型或回答模式。这能让下一轮数据收集有明确的目标，而不是盲目地增加行数。
