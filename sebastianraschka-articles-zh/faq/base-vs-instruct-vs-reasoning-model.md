---
title: "基座模型、指令模型与推理模型的对比"
title_en: "Base, Instruct, and Reasoning Models Compared"
source: https://sebastianraschka.com/faq/docs/base-vs-instruct-vs-reasoning-model.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 基座模型、指令模型与推理模型的对比

> 原文：[Base, Instruct, and Reasoning Models Compared](https://sebastianraschka.com/faq/docs/base-vs-instruct-vs-reasoning-model.html) · Sebastian Raschka's FAQ

**基座模型（base model）**、**指令模型（instruct model）**与**推理模型（reasoning model）**通常属于同一个模型家族。这些标签表明了一个检查点是如何产生的、它预期如何被使用，以及我们应该对它抱有怎样的行为预期。

**基座模型**

基座模型是通过大规模的下一 token 预训练得到的检查点。它能够补全文本，并具备从训练语料中学到的通用能力。然而，一个原始的基座模型可能会继续顺着提示词的措辞往下写，而不是把它当作用户的请求来处理。这使得基座检查点适合用于研究和进一步微调，但通常不便于直接用于聊天应用。

**指令模型**

指令模型通常从基座检查点出发，在指令及期望回复上接受额外训练。许多训练流程还会在指令微调阶段之后使用偏好数据。得到的模型更有可能直接回答问题、遵循指定的格式，并使用该模型家族所预期的聊天模板。

**推理模型**

推理模型是一个标准化程度较低的类别。在当前的模型家族中，它通常指为需要若干中间步骤的问题而塑造的检查点或推理模式。其后训练方案可能包括在可验证任务上的强化学习、从另一个推理模型蒸馏，或两者兼有。在推理阶段，这些模型往往会在给出最终答案之前使用更大的 token 预算。

这笔额外的预算有助于解决数学、编程及其他多步任务。但它也会增加延迟和 token 成本，而且对于一个简单请求来说，可能带来不必要的开销。

![The Qwen overview in the repo shows how a modern family can expose multiple behavioral variants rather than just one monolithic model type](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/qwen/qwen-overview.webp)

仓库中的 Qwen 材料提供了一个具体例子。有些发布版本提供了独立的基座与指令检查点，而另一些则通过聊天模板或生成设置来提供思考（thinking）模式。尽管这种宽泛的区分始终有用，但具体的包装方式在不同发布版本之间会有变化。

![The repo's Qwen materials also include variants such as coder and flash-style models, which reinforces that modern model families are increasingly packaged around distinct use cases and response behaviors](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/qwen/qwen3-coder-flash-overview.webp)

诸如 *Coder* 或 *Flash* 这样的名称描述的是另一个维度，即预期用途或部署权衡。一个 coder 模型仍然可以是基座、指令或面向推理的检查点。因此，模型家族的标签并不构成严格的三格分类法。

在选择检查点时，我使用以下经验法则：

- 需要自定义微调、表示研究或原始文本续写时，选择**基座模型**
- 普通聊天和遵循提示词的任务，选择**指令模型**
- 当困难任务能从更大的推理预算中受益时，选择**推理模型**
