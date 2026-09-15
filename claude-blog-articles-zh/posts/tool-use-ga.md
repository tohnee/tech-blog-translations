---
title: "Claude 现在可以使用工具了"
title_en: "Claude can now use tools"
source: https://claude.com/blog/tool-use-ga/
crawled: 2026-09-14
translated: 2026-09-14
---

# Claude 现在可以使用工具了

> 原文：[Claude can now use tools](https://claude.com/blog/tool-use-ga/) · Claude 博客

工具使用（tool use）让 Claude 能够与外部工具和 API 交互，现已在 Anthropic Messages API、Amazon Bedrock 与 Google Cloud 的 Vertex AI 上，面向整个 Claude 3 模型家族正式发布（GA）。借助工具使用，Claude 可以执行任务、操作数据，并给出更具动态性——也更准确——的响应。

## 工具使用

为 Claude 定义一套工具集，并用自然语言说明你的请求。Claude 随后会选择合适的工具来完成任务，并在适当时执行相应的操作：

- **从非结构化文本中提取结构化数据**：从发票中提取姓名、日期和金额，减少人工数据录入。
- **把自然语言请求转换为结构化的 API 调用**：让团队通过简单命令自助完成常见操作（例如"取消订阅"）。
- **通过搜索数据库或调用 Web API 回答问题**：在客服聊天机器人中即时、准确地响应客户咨询。
- **通过软件 API 自动化简单任务**：在数据录入或文件管理中节省时间、减少错误。
- **编排多个快速 Claude 子智能体处理细粒度任务**：根据与会者的空闲时间自动找到最优会议时间。

## 更好的开发者体验

为了让开发者更容易借助工具发挥 Claude 3 模型的智能，我们还内置了一些功能，帮助开发者进一步定制终端用户的体验。

- **带流式输出的工具使用缩短等待时间，创造更有互动感的交互**：流式输出让客服聊天机器人这类应用能够实时响应，实现更流畅、更自然的对话。
- **强制工具使用（forced tool use）让开发者可以指示 Claude 选择哪个工具**：开发者可以指定 Claude 应使用的工具，或把选择权留给 Claude，帮助打造更有针对性、更高效的应用。
- **工具同样支持图像**：Claude 可以在实时应用中融入图像输入。

在 beta 期间，许多开发者用 Opus 构建了复杂的面向用户的助手。为了进一步增强这种体验，Opus 现在会在输出中包含 `<thinking>` 标签，澄清 Claude 的推理过程，简化开发者的调试工作。我们的 Claude 3 模型目前尚无法支持并行工具调用。

## 客户聚焦：StudyFetch

AI 原生学习平台 [StudyFetch](https://www.claude.com/customers/studyfetch) 使用 Claude 的工具使用能力来驱动其个性化 AI 导师 Spark.E。通过集成工具来跟踪学生进度、导航课程材料与讲座，并创建交互式用户界面，StudyFetch 为全球学生打造了一个更有互动感的教育环境。

"配备工具使用的 Claude 准确且划算，如今驱动着我们的实时语音 AI 辅导课程。我们只用了几天时间就把工具集成进了平台。"StudyFetch CTO 兼联合创始人 Ryan Trattner 说，"于是，我们的 AI 导师 Spark.E 开始以智能体的方式行动——展示交互式 UI、在上下文中跟踪学生进度、在讲座和材料之间导航。自采用配备工具使用的 Claude 以来，我们观察到正面人工反馈增长了 42%。"

## 客户聚焦：Intuned

浏览器自动化平台 Intuned 使用 Claude 在其云平台内驱动数据提取。借助 AI 驱动的数据提取，Intuned 大幅改善了构建与执行更可靠浏览器自动化的开发者体验。

"配备工具使用的 Claude 3 Haiku 对我们来说是一个颠覆性的改变。在接入该模型并运行我们的基准测试之后，我们意识到它的质量、速度与价格组合无可匹敌。"Intuned 联合创始人 Faisal Ilaiwi 说，"Haiku 正帮助我们把客户的数据提取任务扩展到一个全新的水平。"

## 客户聚焦：Hebbia

[Hebbia](https://www.claude.com/customers/hebbia) 正在为领先的金融与法律服务公司打造 AI 知识工作者。他们使用 Claude 3 Haiku 来驱动多个复杂的多步骤客户工作流。

"我们利用 Claude 3 Haiku 生成实时建议、自动化提示词撰写，并从长文档中提取关键元数据。"Hebbia 产品经理 Divya Mehta 分享道，"Claude 3 Haiku 的工具使用功能为我们的平台解锁了实时生成可靠建议与提示的能力与速度。"

## 开始使用

你今天就可以在 Anthropic Messages API、Amazon Bedrock 与 Google Cloud 的 Vertex AI 上开始使用工具使用。想了解更多，请探索我们的[文档](https://docs.anthropic.com/en/docs/tool-use)、[工具使用教程](https://github.com/anthropics/courses/tree/master/tool_use)与 [Anthropic 工具使用 Cookbook](https://platform.claude.com/cookbook/tool-use-calculator-tool)。

FAQ（常见问题）
