---
title: "CodeRabbit、Power Digital 与 ThoughtSpot 如何在 Claude Marketplace 上借助 Snowflake 和 Vercel 扩展业务"
title_en: "How CodeRabbit, Power Digital, and ThoughtSpot scale with Snowflake and Vercel on Claude Marketplace"
date: 2026-09-23
source: https://claude.com/resources/articles/how-coderabbit-power-digital-and-thoughtspot-scale-with-snowflake-and-vercel-on-claude-marketplace
crawled: 2026-11-17
translated: 2026-11-17
---

# CodeRabbit、Power Digital 与 ThoughtSpot 如何在 Claude Marketplace 上借助 Snowflake 和 Vercel 扩展业务

> 原文：[How CodeRabbit, Power Digital, and ThoughtSpot scale with Snowflake and Vercel on Claude Marketplace](https://claude.com/resources/articles/how-coderabbit-power-digital-and-thoughtspot-scale-with-snowflake-and-vercel-on-claude-marketplace) · Claude 博客

*CodeRabbit 通过 Claude Marketplace 扩展了其 Vercel 方案；Power Digital 和 ThoughtSpot 则用各自已有的 Anthropic 承诺用量扩展了 Snowflake 容量。*

用 Claude 构建产品的公司，也会依赖其他软件来完成工作，比如用 Snowflake 存储和分析数据，或用 Vercel 运行应用。Claude Marketplace 让拥有 Anthropic 承诺用量的企业可以将其中一部分用于团队本就依赖的工具，这样一笔投入就能覆盖团队日常使用的更多东西，而无需再申请新预算。

以下是 CodeRabbit、Power Digital 和 ThoughtSpot 如何借助 Claude Marketplace 扩展它们在 Vercel 和 Snowflake 上的工作。

## **Power Digital 在 Snowflake 上运行客户数据**

[Power Digital](https://powerdigitalmarketing.com/)是一家营销机构，为其团队和客户构建了平台 Nova。客户通过 Nova 接入自己的数据，而 Nova 运行在 Snowflake 上，支撑报表、内部工具以及提升营销表现的模型。Snowflake 让 Power Digital 能快速为每位客户搭建安全的数据环境；借助 Snowflake Cortex AI，它可以在客户现有的治理框架内，直接对这些数据运行 Claude 等模型。

如今，Claude 已在 Power Digital 全面运行，从客户交付物、财务运营，到内置于其自身产品中的模型。使用规模已从 1 月的约 12 名工程师增长到今天的 800 多人。

Power Digital 作为 Snowflake 客户已有五年，今年通过 Claude Marketplace 扩展了其 Snowflake 承诺用量。由于这笔支出来自已经获批的预算，其团队可以快速扩大 Snowflake 的使用规模。

> “我们把大量基于 Claude 的运营方式集中了起来，并在全公司管理着数百种工具。Claude Marketplace 让我们能把承载客户数据的 Snowflake 纳入同一份 Anthropic 承诺用量。等我们开口时，合同已经在起草了。”Power Digital 创新高级副总裁 John Saunders 表示。

## **ThoughtSpot 在 Snowflake 上构建 AI 分析**

[ThoughtSpot 的智能体分析平台](https://www.thoughtspot.com/)为业务用户提供可直接用于决策的洞察，这些洞察以企业的语义层和上下文层为基础，通过确定性、可验证的查询给出可信答案。

为了支撑其 AI 功能，ThoughtSpot 使用 Snowflake 的推理 API，在 Snowflake 内部直接对客户数据运行 Claude 等模型，让数据、业务上下文、访问控制和 AI 都留在同一个生态系统中。ThoughtSpot 将其对 Snowflake 推理 API 的采购计入已有的 Anthropic 承诺用量，因此产品团队可以在已经预留的预算内立即开始基于该 API 构建。

> “我们的智能体分析平台运行在 Claude 上，所以通过 Claude Marketplace 购买 Snowflake 的推理 API 是顺理成章的选择。我们用上了已经做出的承诺，这笔采购来自已经获批的预算。”ThoughtSpot 产品管理高级副总裁 Francois Lopitaux 表示。

ThoughtSpot 也在与 Claude 一同成长。其 AI 分析师 [Spotter](https://claude.com/connectors/thoughtspot-spotter)已作为 Claude 的连接器提供，用户无需离开 Claude，就能分析数据、构建和探索仪表盘并执行操作。

> “我们的 AI 分析师 Spotter 已经进入 Claude 的连接器目录，我们还希望自己通过 Marketplace 销售智能体产品，让客户能够做成我们刚刚做过的事。”Lopitaux 补充道。

## **CodeRabbit 在 Vercel 上运行编码智能体**

[CodeRabbit](https://claude.com/platform/marketplace/coderabbit)基于 Claude 构建，用于[验证 AI 生成的代码](https://claude.com/resources/articles/how-coderabbit-used-claude-to-build-an-agent-orchestration-system)，让工程团队掌控最终上线的内容。它的智能体负责编写和测试代码，因此需要一个安全的运行环境。[Vercel Sandbox](https://vercel.com/sandbox)会把每个智能体的代码放在独立的 Linux microVM 中运行，拥有独立的文件系统和网络，与其他任务以及 CodeRabbit 自身系统隔离。[Vercel Workflows](https://vercel.com/workflows)负责协调这些工作，让长时间运行的任务可以暂停、恢复并最终完成，而不会触及时间限制。

当 CodeRabbit 的工程和产品负责人希望从按量付费的 Vercel 方案转为承诺方案时，公司用最近扩展的 Anthropic 承诺用量为这次升级提供了资金。由于预算已经获批，交易在一周内就完成了。

> “对我们来说，价值在于灵活性：用已经获批的预算，支持工程师信任的工具。而且我们能把同样的价值直接通过 Claude Marketplace 交付给客户，这是最终的双赢。”CodeRabbit 全球合作负责人 Blair Pierson 表示。

## **Snowflake 与 Vercel 随基于 Claude 构建的客户一同成长**

对于 [Snowflake](https://claude.com/platform/marketplace/snowflake)和 [Vercel](https://claude.com/platform/marketplace/vercel)这样的卖家而言，Claude Marketplace 是一种触达已经在 Claude 上构建的客户的方式，也为拥有 Anthropic 承诺用量的客户提供了更快的购买途径。

> “AI 只有扎根于数据和上下文才值得信任。Claude 直接运行在 Snowflake 中，因此客户的治理、上下文和权限从第一天起就已经就位，成为可信洞察的基础。Claude Marketplace 让这种关系得以轻松延伸，客户可以把 Anthropic 承诺用量的一部分直接用于 Snowflake 的 AI 工作负载。我们正与 Anthropic 在共同客户中推进这一模式。”Snowflake 企业技术合作总监 Omar Bed-Mohamed 表示。

> “Claude Marketplace 让 CodeRabbit 这样的客户能够快速采购 Vercel 的智能体基础设施并扩展其平台。我们期待帮助每一家在 Claude 上构建的公司运行智能体。”Vercel 产品合作负责人 Zack Ciesinski 表示。

## **通过 Claude Marketplace 采购**

用 Claude 构建产品，往往意味着要接入团队已经依赖的数据平台和基础设施。[Claude Marketplace](https://claude.com/marketplace)让客户可以将部分 Anthropic 承诺用量用于 Vercel、Snowflake 等合作伙伴，从而让团队少花时间在采购上，多花时间在构建上。

以这种方式使用 Anthropic 承诺用量目前处于限量预览阶段。如果你拥有承诺用量，请联系你的客户团队或[提交申请](https://claude.com/marketplace-contact-sales)，确认是否符合条件。[进一步了解 Claude Marketplace](https://claude.com/resources/articles/claude-marketplace)。
