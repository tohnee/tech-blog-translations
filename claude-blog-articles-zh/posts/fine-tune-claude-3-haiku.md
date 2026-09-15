---
title: "在 Amazon Bedrock 中微调 Claude 3 Haiku"
title_en: "Fine-tune Claude 3 Haiku in Amazon Bedrock"
source: https://claude.com/blog/fine-tune-claude-3-haiku/
crawled: 2026-09-14
translated: 2026-09-14
---

# 在 Amazon Bedrock 中微调 Claude 3 Haiku

> 原文：[Fine-tune Claude 3 Haiku in Amazon Bedrock](https://claude.com/blog/fine-tune-claude-3-haiku/) · Claude 博客

***更新：在 Amazon Bedrock 中微调 Claude 3 Haiku 现已正式可用。（2024 年 11 月 1 日）***

客户现在可以在 [Amazon Bedrock](https://aws.amazon.com/bedrock/claude/) 中微调（fine-tune）Claude 3 Haiku——我们速度最快、性价比最高的模型——为自己的业务定制模型的知识与能力，让它在专门任务上更加高效。

## 微调概览

微调是一种常用的提升模型性能的技术。通过创建模型的定制版本，你可以训练模型在高度定制化的工作流中表现出色。

要微调 Claude 3 Haiku，你首先要准备一组高质量的提示-补全（prompt-completion）对——即你希望 Claude 针对给定任务给出的理想输出。现已开启预览的微调 API 将使用你的数据来创建你自己的定制版 Claude 3 Haiku。借助 Amazon Bedrock 控制台或 API，你可以测试并打磨你的定制 Claude 3 Haiku 模型，直到它达到你的性能目标、可以部署为止。

## 收益

微调让你能够定制 Claude 3 Haiku，使其习得专门的业务知识，从而提升准确性与一致性。收益包括：

- **在专门任务上取得更好的结果**：提升领域特定动作的表现，例如分类、与自定义 API 的交互，或行业数据的解读。通过编码公司与领域知识，微调让 Claude 3 Haiku 在对你业务至关重要的领域胜过更通用的模型。
- **更快的速度、更低的成本**：在可以用 Claude 3 Haiku 替代 Sonnet 或 Opus 的生产部署中降低成本，同时更快地返回结果。
- **一致且符合品牌调性的格式**：按照你的精确规格生成结构一致的输出，例如标准化报告或自定义 schema，确保符合监管要求与内部规范。
- **易于使用的 API**：各种规模的公司都能高效创新，而无需深厚的内部 AI 专业能力或资源。任何人都可以顺畅地微调模型，不需要深厚的技术功底。
- **安全可靠**：专有训练数据始终保留在客户的 AWS 环境之内。Anthropic 的微调技术延续了 Claude 3 模型家族有害输出风险低的特性。

我们对 Haiku 进行了微调，用于审核网络论坛上的在线评论¹，包括识别侮辱、威胁和露骨内容。微调将分类准确率从 81.5% 提升到 99.6%，同时把每次查询的 token 消耗降低了 85%。

## 客户聚焦

[SK Telecom](https://www.claude.com/customers/skt) 是韩国最大的电信运营商之一，它训练了一个定制 Claude 模型，借助其行业专属的专业知识来改进支持工作流、带来更好的客户体验。

"把微调后的 Claude 嵌入我们的客户支持运营后，我们的内部流程和整体客户满意度都有了可量化的改善。**通过定制 Claude，我们看到客户代表回复的正面反馈提升了 73%，电信相关任务的关键绩效指标改善了 37%**。微调后的模型现在能够从客户通话记录中高效生成主题、行动项和摘要，并把复杂的客户问题拆解成可管理的步骤，从而更好地解决问题。"AI Tech Collaboration Group 副总裁 Eric Davis 表示。

[Thomson Reuters](https://www.claude.com/customers/thomson-reuters) 是一家全球性的内容与科技公司，已经在 Claude 3 Haiku 上看到了积极成果。这家公司服务于法律、税务、会计、合规、政府和媒体领域的专业人士，预期通过用其行业专业知识微调 Claude，获得更快、更相关的 AI 结果。

"我们很高兴能在 Amazon Bedrock 中微调 Anthropic 的 Claude 3 Haiku 模型，进一步提升我们由 Claude 驱动的解决方案。Thomson Reuters 的目标是提供准确、快速且一致的用户体验。通过围绕我们的行业专业知识和具体要求来优化 Claude，我们预期会带来可量化的改进，以更快的速度交付高质量结果。**我们已经在 Claude 3 Haiku 上看到了积极成果，而微调将让我们能够更精准地定制 AI 辅助**。"Thomson Reuters AI 与 Labs 负责人 Joel Hron 表示。

## 如何开始使用

Amazon Bedrock 中 Claude 3 Haiku 的微调现已在美国西部（俄勒冈）AWS 区域开启预览。发布时我们支持基于文本的微调，上下文长度最高 32K token，并计划在未来引入视觉能力。更多细节请参阅 [AWS 发布博客](https://aws.amazon.com/blogs/machine-learning/fine-tune-anthropics-claude-3-haiku-in-amazon-bedrock-to-boost-model-accuracy-and-quality/)与[文档](https://docs.aws.amazon.com/bedrock/latest/userguide/custom-model-supported.html)。

如需申请访问权限，请联系你的 AWS 客户团队，或在 [AWS Management Console](https://console.aws.amazon.com/bedrock/) 中提交支持工单。

FAQ（常见问题）
