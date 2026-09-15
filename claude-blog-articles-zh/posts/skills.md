---
title: "推出 Agent Skills"
title_en: "Introducing Agent Skills"
source: https://claude.com/blog/skills/
crawled: 2026-09-14
translated: 2026-09-14
---

# 推出 Agent Skills

> 原文：[Introducing Agent Skills](https://claude.com/blog/skills/) · Claude 博客

***更新：**我们新增了[面向整个组织的技能管理](https://claude.com/blog/organization-skills-and-directory)、一个收录合作伙伴构建技能的[目录](https://claude.com/connectors)，并将 [Agent Skills](https://agentskills.io) 发布为开放标准，以实现跨平台可移植性。（2025 年 12 月 18 日）*

Claude 现在可以使用 *Skills*（技能）来改进它执行特定任务的方式。Skills 是一些文件夹，其中包含 Claude 可以按需加载的指令、脚本和资源。

只有当 skill 与手头任务相关时，Claude 才会访问它。在使用时，skills 能让 Claude 更擅长处理专门任务，比如操作 Excel 或遵循你组织的品牌规范。

你已经在 Claude 应用中见过 Skills 的身影——Claude 用它们创建电子表格、演示文稿等文件。现在，你可以构建自己的 skills，并在 Claude 应用、Claude Code 和我们的 API 中使用。

## Skills 的工作原理

在处理任务时，Claude 会扫描可用的 skills，寻找相关匹配。一旦匹配，它只加载所需的最少信息和文件——既保持 Claude 的速度，又能获取专门知识。

Skills 具有以下特点：

- **可组合**：Skills 可以叠加使用。Claude 会自动判断需要哪些 skills，并协调它们的使用。
- **可移植**：Skills 在所有地方使用同一格式。一次构建，即可在 Claude 应用、Claude Code 和 API 中使用。
- **高效**：只在需要时加载所需内容。
- **强大**：Skills 可以包含可执行代码，用于那些传统编程比 token 生成更可靠的任务。

不妨把 Skills 想象成定制的入职培训材料，让你把专业知识打包，使 Claude 成为你最关心领域的专家。想深入了解 Agent Skills 的设计模式、架构和开发最佳实践，请阅读我们的[工程博客](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)。

## Skills 适用于每一款 Claude 产品

### **Claude 应用**

Skills 面向 Pro、Max、Team 和 Enterprise 用户开放。我们为文档创建等常见任务提供了现成 skills、可供你自定义的示例，以及创建自定义 skills 的能力。

Claude 会根据你的任务自动调用相关 skills——无需手动选择。Claude 工作时，你甚至能在它的思维链（chain of thought）中看到这些 skills。

创建 skill 很简单。"skill-creator" skill 提供交互式引导：Claude 会询问你的工作流，生成文件夹结构，编排 SKILL.md 文件的格式，并打包你所需的资源。无需手动编辑文件。

在[设置](https://claude.ai/redirect/website.v1.51f73c97-b077-44e7-85ba-8b27a025dfdf/settings/features)中启用 Skills。Team 和 Enterprise 用户需要管理员先在整个组织范围内启用 Skills。

### **Claude 开发者平台（API）**

Agent Skills（我们常简称为 Skills）现在可以添加到 Messages API 请求中，新的 `/v1/skills` 端点让开发者能够以编程方式控制自定义 skill 的版本管理。Skills 需要使用 [Code Execution Tool](https://docs.claude.com/en/docs/agents-and-tools/tool-use/code-execution-tool) 测试版，它为 skills 的运行提供所需的安全环境。

使用 Anthropic 创建的 skills，可以让 Claude 读取并生成带公式的专业 Excel 电子表格、PowerPoint 演示文稿、Word 文档和可填写的 PDF。开发者可以创建自定义 Skills，为特定用例扩展 Claude 的能力。

开发者还可以通过 Claude Console 轻松创建、查看和升级 skill 版本。

欢迎探索[文档](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)、我们的 [skills cookbook](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction) 或 [Anthropic Academy](https://www.anthropic.com/learn/build-with-claude)，了解更多。

Skills 教会 Claude 如何处理 Box 内容。用户可以把存储的文件转换成符合其组织标准的 PowerPoint 演示文稿、Excel 电子表格和 Word 文档——省下数小时的工作量。

Canva 计划利用 Skills 定制智能体并扩展其能力。这为把 Canva 更深入地融入智能体工作流开辟了新途径——帮助团队捕捉其独特上下文，轻松创作令人惊艳的高质量设计。

借助 Skills，Claude 与 Notion 无缝协作——让用户更快地从提问走向行动。在复杂任务上更少折腾提示词，结果更加可期。

Skills 简化了我们的管理会计和财务工作流。Claude 处理多份电子表格、捕捉关键异常，并按照我们的流程生成报告。过去需要一天完成的工作，现在一小时就能搞定。

### **Claude Code**

Skills 把你团队的专业知识和工作流带入 Claude Code。通过 anthropics/skills 插件市场（marketplace）的插件安装 skills，Claude 会在相关时自动加载。你可以通过版本控制与团队共享 skills，也可以手动把 skills 添加到 `~/.claude/skills` 来安装。Claude Agent SDK 为构建自定义智能体提供同样的 Agent Skills 支持。

## 开始使用

- **Claude 应用：**[用户指南](https://support.claude.com/en/articles/12580051-teach-claude-your-way-of-working-using-skills)与[帮助中心](https://support.claude.com/en/articles/12512176-what-are-skills)
- **API 开发者：**[文档](https://docs.claude.com/en/api/skills-guide)
- **Claude Code：**[文档](https://docs.claude.com/en/docs/claude-code/skills)
- **可自定义的示例 Skills：**[GitHub 仓库](https://github.com/anthropics/skills)

## 接下来

我们正在简化 skill 创建工作流，并打造面向整个企业的部署能力，让组织更容易把 skills 分发到各个团队。

请记住，这项功能让 Claude 可以执行代码。虽然强大，但也意味着你需要注意使用哪些 skills——坚持使用可信来源，保护你的数据安全。[了解更多](https://support.claude.com/en/articles/12512180-using-skills-in-claude#h_2746475e70)。

FAQ（常见问题）
