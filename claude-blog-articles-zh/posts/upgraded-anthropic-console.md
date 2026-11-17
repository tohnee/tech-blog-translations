---
title: "借助升级版 Anthropic Console 更快进入生产环境"
title_en: "Get to production faster with the upgraded Anthropic Console"
date: 2025-03-06
source: https://claude.com/resources/articles/upgraded-anthropic-console
crawled: 2026-11-17
translated: 2026-11-17
---

# 借助升级版 Anthropic Console 更快进入生产环境

> 原文：[Get to production faster with the upgraded Anthropic Console](https://claude.com/resources/articles/upgraded-anthropic-console) · Claude 博客

我们重新设计了 Anthropic Console，让它成为一个统一的地方，供你和团队成员一起用 Claude 构建、测试并迭代你的 AI 部署。

开发者现在可以在 [Anthropic Console](https://console.anthropic.com/) 中分享提示词，直接与团队成员协作。我们还新增了对最新模型 Claude 3.7 Sonnet 的支持，以及控制扩展思考预算的能力。

### 构建可靠的 AI 应用

提示词的质量在很大程度上决定模型在特定任务上的回答效果。Anthropic Console 已经通过更高效地编写、评估和优化提示词的工具，简化了 AI 开发流程。

**编写提示词：**在用于测试 API 调用的交互式环境中，使用 Workbench 高效组织提示词、加入示例并集成外部工具。

![Workbench 的截图](https://assets.claude.com/a09a0522f7056915148dce60751921dcc830159a.jpg)

**自动生成提示词：**描述你希望达成的目标，Claude 会运用思维链推理等提示词工程技巧，生成一个有效、精确且可靠的提示词。

![提示词生成器的截图](https://assets.claude.com/a3b51909c7d5b4706ba2e8a1ae33c8e03a7835c7.jpg)

**评估模型回答：**通过自动生成测试用例和并排对比输出，在真实场景中评估你的提示词。轻松运行测试套件、为回答质量评分，并基于数据决定要部署哪些提示词。

![两张截图：两个提示词正在并排对比中接受评估。](https://assets.claude.com/befa032fd80a7016569b1b163808aa89fb3219d5.jpg)

**改进提示词：**使用高级提示词工程技巧自动优化提示词。这非常适合改造最初为其他 AI 模型编写的提示词，也适合优化手写的提示词。

提示词定稿后，你可以点击“Get Code”，获得一段可直接部署、可用于生产的 API 调用代码。

### 通过可分享的提示词协作

开发者、领域专家、产品经理和 QA 专家常常需要围绕提示词协作，才能取得最佳效果。过去，团队不得不在文档或聊天应用之间复制粘贴提示词，导致版本控制混乱和知识孤岛。

![一张已分享提示词的截图。](https://assets.claude.com/e5894d731f30051c03c31949a3084b7d5406de3d.jpg)

Anthropic Console 中的可分享提示词现在提供了一种集中化的方式，在整个组织内开发、优化和标准化提示词。团队成员可以访问共享的提示词库并协作，从而更容易建立最佳实践，确保所有由 Claude 驱动的应用保持一致的品质。

### 针对扩展思考优化提示词

[Claude 3.7 Sonnet](https://www.anthropic.com/news/claude-3-7-sonnet) 是我们迄今最新、最智能的模型，它既能近乎即时地给出回答，也能进行扩展的逐步思考，并将思考过程呈现给用户。

![一张截图](https://assets.claude.com/b6c3a5bc6c6375a0084247c6cf5e93f0fb8d4ec1.jpg)

启用扩展思考后，编写提示词的方式总体不变，但我们让优化提示词变得更简单，以便充分利用这一新能力。只需指明该提示词将在开启扩展思考的情况下使用，Claude 就会尽可能生成最佳回答。你也可以用 Anthropic Console 设置思考 token 的上限，从而控制思考的*预算*。

### 开始使用

升级版 Anthropic Console 现已向所有用户开放。[登录](https://console.anthropic.com/)即可开始使用，或查阅我们的[文档](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)了解更多。
