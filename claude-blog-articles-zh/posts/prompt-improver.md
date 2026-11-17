---
title: "在开发者控制台中改进你的提示词"
title_en: "Improve your prompts in the developer console"
date: 2024-10-14
source: https://claude.com/resources/articles/prompt-improver
crawled: 2026-11-17
translated: 2026-11-17
---

# 在开发者控制台中改进你的提示词

> 原文：[Improve your prompts in the developer console](https://claude.com/resources/articles/prompt-improver) · Claude 博客

Claude 现在可以在开发者控制台中自动优化提示词，所用技术包括思维链推理和示例增强等。

今天，我们推出在 [Anthropic Console](https://console.anthropic.com/) 中直接改进提示词、管理示例的能力。这些功能让你更容易运用提示词工程的最佳实践，构建更可靠的 AI 应用。

## 更好的提示词，更好的补全结果

提示词质量在很大程度上决定模型在给定任务中的回答有多成功。然而，落实提示词最佳实践需要时间，而且不同模型提供商的实践往往各不相同。

提示词改进器（prompt improver）让开发者拿现有提示词，借助 Claude 使用高级提示词工程技术自动优化。这非常适合改造最初为其他 AI 模型编写的提示词，也适合优化手写的提示词。

[](https://assets.claude.com/fb1afd8b4dd4831fd1e700ad23affda9cf70d666.mp4)

提示词改进器通过以下方式强化现有提示词：

1. **思维链推理：**为 Claude 增加一个专门的部分，让它在回答前系统地思考问题，以提高准确性和可靠性。
2. **示例标准化：**把示例转换为一致的 XML 格式，以提升清晰度和处理效果。
3. **示例增强：**用与新结构化提示词一致的思维链推理来扩充现有示例。
4. **重写：**重写提示词以厘清结构，并纠正细微的语法或拼写问题。
5. **添加预填充：**预填充 Assistant 消息，以引导 Claude 的行为并强制输出格式。

生成新提示词后，你可以就哪些地方有效、哪些无效向 Claude 提供反馈，进一步改进提示词。

**我们的测试显示，提示词改进器让一个多标签分类测试的准确率提升了 30%¹，并让一个摘要任务的字数遵循度达到 100%²。**

## 管理多轮示例

在提示词中添加示例是提升模型回答质量最有效的方法之一，尤其是在让 Claude 精确遵循特定输出格式方面。现在，你可以直接在 Workbench 中以结构化格式管理示例。这样既能更轻松地添加带有清晰输入/输出对的新示例，也能编辑现有示例来优化回答质量。

![Anthropic Console 界面，展示某个提示词的示例](https://assets.claude.com/dc5899475f8c28aad0d45a35d7477d0c8ab620ca.jpg)

如果你的提示词没有示例，可以用 Claude 驱动的示例生成功能来添加。Claude 能自动创建合成的示例输入并起草输出，从而简化这一流程。

添加示例有助于提升：

* **准确性：**减少对指令的误解。
* **一致性：**确保输出格式符合预期。
* **表现：**增强 Claude 处理复杂任务的能力。

## 用理想输出评估提示词

我们的[提示词评估器](https://www.anthropic.com/news/evaluate-prompts)让你能在各种场景下测试提示词。为帮助基准衡量并改进提示词表现，我们在 Evaluations 标签页中新增了可选的「理想输出」（ideal output）列。该列帮助用户以 5 分制有效且一致地为模型输出评分。

测试新提示词后，你可以在提示词改进器中就仍不奏效的地方向 Claude 提供更多反馈，并重复这一过程，直到你对结果满意。提示词改进器还可以根据任意要求修改提示词和示例。例如，你可以让 Claude 把提示词和示例改为 JSON 格式输出，而不是 XML 格式输出。

## 客户聚焦：Kapa.ai

[Kapa.ai](https://www.kapa.ai/) 是一家把你的技术知识库转化为可直接投产的 AI 助手的技术公司，他们使用提示词改进器将多个关键 AI 工作流迁移到 Claude。

「Anthropic 的提示词改进器简化了我们向 Claude 3.5 Sonnet 的迁移，让我们更快进入生产环境，」Kapa.ai 联合创始人 Finn Bauer 表示。

## 开始使用

Anthropic Console 中的所有用户均可使用提示词改进器、示例管理和理想输出功能。

想进一步了解如何用 Claude 改进和评估提示词，请查阅我们的[文档](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-improver)。

#### 脚注

[1] 我们给 Claude 3 Haiku 提供 500 篇维基百科文章及其标题，测试它将文章标题与从文章中随机抽取的一句话相匹配的能力。与原始提示词相比，Claude 3 Haiku 的准确率提升了 30%。

[2] 我们给 Claude 提供十篇维基百科文章，在提示词改进器处理后，Claude 对「在指定字数范围内写摘要」这一指令的遵循度达到 100%。
