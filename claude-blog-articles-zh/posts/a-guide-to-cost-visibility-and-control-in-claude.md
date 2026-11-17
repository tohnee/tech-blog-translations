---
title: "Claude 成本可见性与控制指南"
title_en: "A guide to cost visibility and control in Claude"
date: 2026-08-04
source: https://claude.com/resources/articles/a-guide-to-cost-visibility-and-control-in-claude
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude 成本可见性与控制指南

> 原文：[A guide to cost visibility and control in Claude](https://claude.com/resources/articles/a-guide-to-cost-visibility-and-control-in-claude) · Claude 博客

了解 IT 管理员如何使用成本控制功能优化 Claude Enterprise 的开支。

企业使用 Claude 的方式多种多样：从向数千名员工推广，到初创公司和单一团队在 Claude Platform 上构建应用。对所有这些用户来说，成本都很重要。

本文将介绍 IT 管理员如何使用目前已有的控制功能来查看和管理 Claude 的成本，并分享一些关于在何处投入的最佳实践。

### **思考成本的几个有用角度**

把“每次成果的成本”（cost-per-outcome）而不是 token 消耗作为衡量价值的主要指标，会更有帮助。关于一个项目，可以问两个问题：

1. 如果没有 AI，这项工作要花多少成本——无论是资源、时间，还是根本不尝试这个项目？
2. 模型完成的是困难、需要判断与推理的任务，还是仅仅规模很大、即大量直截了当的工作？

第一个问题的答案取决于你的业务和需求——没有哪家供应商能替你衡量。第二个问题可以通过让模型与工作相匹配来解决。把复杂推理交给更便宜的模型，往往会让最终任务更贵，因为它会在重试上消耗 token，还需要更多人工纠正。把前沿模型用于基础文档处理，则是在为任务根本用不到的能力付费。

Claude 的[模型家族](https://claude.com/resources/articles/claude-models-explained-choosing-the-best-model-for-your-use-case)为你提供了选择：

* **Fable** 用于最难的问题；
* **Opus** 用于长周期工作和编码；
* **Sonnet** 用于日常工作与分析；
* **Haiku** 用于高并发和常规任务。

对于上述任一模型，[努力等级控制](https://platform.claude.com/docs/en/build-with-claude/effort)可以调高或调低模型在解决问题时“思考”的程度；[顾问工具](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool)则让较小的模型只在遇到瓶颈时咨询前沿模型。

许多组织会使用多个模型，而且常常用在同一个项目中。例如，一家保险公司可能让前沿模型帮助理赔员评估复杂的商业索赔，同时由 Haiku 对接入其中的文档进行打标和分诊。

### **如何查看并控制支出**

你能使用哪些控制手段，取决于 Claude 是作为面向员工的产品运行，还是作为支撑应用的 API 运行。前者由管理员控制，后者由在其上构建应用的工程师控制，而大多数大型客户两者都会使用。

**Claude Enterprise 的成本控制**

我们通常建议按以下顺序逐步实施，因为在看到一个月真实用量之前，很难设定合理的限额。

* [**访问权限门控**](https://support.claude.com/en/articles/13930452-manage-custom-roles-on-enterprise-plans)让管理员决定哪些群组和自定义角色可以使用 Claude Code、Claude Cowork 等产品，而不是一刀切地全面开放。从一个团队开始，观察结果，再逐部门扩展。
* **模型控制**分为两个层面。[权限授予](https://support.claude.com/en/articles/15694740-manage-model-access-for-your-organization)决定团队可以访问哪些模型，[默认模型](https://support.claude.com/en/articles/15330088-set-a-default-model-for-your-organization)则决定新对话从哪个模型开始。管理员可以为承担最困难工作的团队授予最强模型的使用权限，并把其他人的默认模型设为 Sonnet。
* [**硬性支出上限**](https://support.claude.com/en/articles/11526368-how-am-i-billed-for-my-enterprise-plan#h_deb29b5a4f)为用量设定天花板。可以在了解整个组织的基线后设置，也可以针对单个用户或群组设置——针对群组时，每位成员各自获得该限额。上限会立即生效。

管理员还可以自动处理支出限额提升申请的审批，识别接近支出限额的成员，并找出用量快速变化的成员。

**观察 Claude 用量的工具**

用量数据可以在管理员仪表盘中查看、发送到你自己的系统，或直接向 Claude 询问。以下是 IT 管理员可以用来更好地理解组织内 Claude 使用情况的三个功能：

* [**用量分析**](https://support.claude.com/en/articles/12883420-view-usage-analytics-for-team-and-enterprise-plans)按人员、团队和模型拆分支出。导出的数据与发票高度一致，便于更好地核对用量与账单。
* [**Analytics API**](https://platform.claude.com/docs/en/manage-claude/analytics-api)让同样的数据可以接入团队已经在用的系统。把它连接到商业智能工具、财务系统和内部仪表盘，Claude 支出就能与预算、预测等其他成本一起评估。
* [**通过分析对话进行分析**](https://support.claude.com/en/articles/14729354-use-analytics-chat-to-ask-claude-about-usage)让管理员用自然语言询问用量情况。比如问“这个月支出最高的是谁？”或“这个季度哪个团队的用量增长最快？”，无需拉取完整报告。

### **在 API 上构建时的控制手段**

Claude Console 为在 Claude Platform 上构建应用的组织和开发者提供了控制手段。工作区按产品、团队或环境隔离 API 用量，并在成本与用量报告中单独占一行。

Claude Platform 上实用的成本杠杆包括：

* [**提示缓存**](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)会存储跨请求重复使用的内容，这样模型就不必每次都重新处理。如果你每次调用都发送相同的参考资料，就应开启它——缓存命中时，输入成本可降至正常输入费率的 10%。
* [**批处理**](https://platform.claude.com/docs/en/build-with-claude/batch-processing)以半价运行不需要立即响应的任务，比如电商公司整夜对其商品目录进行分类。凡是能等待的工作都可以迁移过来；批量折扣还可以与缓存叠加。
* [**努力等级参数**](https://platform.claude.com/docs/en/build-with-claude/effort)控制模型在给定调用中进行多少推理。对路由和抽取类任务调低，对最终建议调高，这样你只在真正需要峰值的调用上支付峰值费率。
* [**顾问策略**](https://platform.claude.com/docs/en/build-with-claude/effort)让 Sonnet 这类较小的模型在关键时刻调用前沿模型，例如在交付前评估工作成果。让任务的大部分由较小模型运行，只在需要其判断力时为大模型付费。

这些功能组合使用时，通常能在任何人动预算之前，就大幅降低生产工作负载的成本。

### **开始使用**

成本控制功能现已在 Claude Enterprise 中提供。查看方案与定价，请访问 [claude.com/pricing](https://claude.com/pricing)。企业组织可以通过 [Claude Enterprise](https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan)方案[直接开始使用](http://claude.ai/create/enterprise)。开发者可以在 [docs.claude.com](https://docs.claude.com) 找到工作区、缓存和批处理的文档。
