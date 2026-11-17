---
title: "面向金融业的 Cowork 与插件"
title_en: "Cowork and plugins for finance"
date: 2026-02-24
source: https://claude.com/resources/articles/cowork-plugins-finance
crawled: 2026-11-17
translated: 2026-11-17
---

# 面向金融业的 Cowork 与插件

> 原文：[Cowork and plugins for finance](https://claude.com/resources/articles/cowork-plugins-finance) · Claude 博客

为金融工作的实际运作方式而打造的新插件，以及随你从 Excel 到 PowerPoint 再到最终交付物的跨应用工作流。

今天我们宣布 [Cowork](https://claude.com/product/cowork) 的更新，其中包括[新插件](https://claude.com/resources/articles/cowork-plugins)，让企业内各团队能够按自己想要的工作方式塑造 Claude。作为其中一环，我们在[近期更新](https://claude.com/resources/articles/opus-4-6-finance)的基础上继续拓展 Claude 在金融服务领域的能力。

Claude 现在可以[跨 Excel 与 PowerPoint 工作](https://claude.com/resources/articles/claude-excel-powerpoint-updates)——在应用之间携带上下文，端到端完成多步骤金融任务。我们还推出五款新的金融插件、面向 FactSet 和 MSCI 的新 MCP 连接器，以及来自 LSEG 和 S&P Global 的合作伙伴插件。

对金融从业者而言，这意味着一个端到端工作流——从跨市场数据提供商做研究，到更新模型、再到搭建演示文稿——现在可以在单次会话中完成，无需切换工具，也不会在中途丢失上下文。

## 从数据到交付物

金融相关的工作散落在许多不同的地方。交易备忘录取自一个模型，模型取自数据，数据又回流到演示文稿里。Claude 现在可以在 Excel 与 PowerPoint 之间来回切换而不丢失上下文——把检索数据、更新模型和构建交付物当作一个连续任务来完成。

股票分析师可以让 Claude 分析财报、更新财务模型并制作摘要幻灯片——全程无需切换工具。当输入发生变化时，Claude 会自动更新工作流中其余的部分。

跨 Excel 与 PowerPoint 工作的 Claude 现已在研究预览版中向所有付费套餐开放，支持 Mac 和 Windows。

![](https://assets.claude.com/1e053b413b77d9b75ca10eac96e371e77e8dd3a7.png)

## 新的金融插件

我们推出五款由 Anthropic 构建的新插件，以及若干由合作伙伴构建的插件。每款插件都带入了与该职能实际运作方式相匹配的领域专业知识、预期的输出质量和工作流模式。

这 5 款由 Anthropic 开发的插件现已在我们的[公开仓库](https://github.com/anthropics/financial-services-plugins)中全部可用。

* 首先，**financial analysis** 插件支持所有金融分析师都需要的基础工作流，涵盖市场与竞争研究、财务建模，以及 PowerPoint 模板创建与质量检查。

其他插件则支持关键金融职能特有的工作流：

* **investment banking** 帮助投行人士处理交易工作流：审阅交易文件、构建可比公司分析，以及准备推介材料。
* **equity research** 加速研究流程——解析财报电话会文字记录、依据新的业绩指引更新财务模型，以及起草研究报告。
* **private equity** 专为项目寻源与尽职调查而构建。Claude 可以审阅大量文档、提取标准化财务数据、对情景建模，并按照投资标准对机会打分。
* **wealth management** 帮助顾问分析投资组合、识别偏离和税务敞口，并大规模生成再平衡建议。

在这五款插件之外，金融从业者还依赖专有数据和专用平台，这些是任何通用插件都无法复制的。我们的合作伙伴构建了自己的连接器和插件，把机构数据直接带入 Claude 的上下文，使用户的工作流建立在其团队本就信任的确切数据源之上。

## 合作伙伴主导的连接器与插件

除了我们已支持的现有金融 MCP [连接器](https://claude.com/connectors#connectors)之外，两个新的 MCP 连接器让 Claude 可以直接访问机构数据平台。

* **FactSet** 连接器把实时市场数据、基本面分析、盈利预测和研究洞察带入 Claude，用可信的机构级数据增强用户的财务分析与投资研究工作流。
* **MSCI** 连接器把 MSCI 值得信赖的指数数据带入 Claude，使用户可以访问 MSCI 的专有指数数据，并快速获得关于指数表现、敞口、成分股和方法论的洞察。

若干合作伙伴也在推出自己的插件，可在上文同一个[金融服务插件仓库](https://github.com/anthropics/financial-services-plugins)中找到。

* **S&P Global** 插件把 Capital IQ Pro 带入 Claude 的上下文。其技能包括公司速览表（tear sheets）、行业交易概览，以及财报电话会前瞻。
* **LSEG** 插件让金融从业者可以在 Claude 内直接访问 LSEG 的市场数据与分析能力。用实时收益率曲线构建 DCF 模型、用实时新闻起草晨报、用当前跨资产定价进行组合再平衡，以及用真实的融资经济性分析交易。该插件面向拥有有效 LSEG 数据权限的用户提供。

## 开始使用

所有由 Anthropic 开发的插件——financial analysis、investment banking、equity research、private equity 和 wealth management——今日即可使用，可在我们的[公开金融插件仓库](https://github.com/anthropics/financial-services-plugins)中找到，来自 LSEG 和 S&P Global 的合作伙伴插件也在其中。你可以直接安装它们，也可以把它们作为起点，按贵公司特定的工作流、术语和需求进行定制。

要将 Claude 连接到 FactSet、MSCI 或其他企业数据源，请访问 Claude 设置中的连接器目录。管理员可以在那里授权连接，并把它们打包成插件供团队使用。

要开始使用跨 Excel 与 PowerPoint 工作的 Claude，请下载 Claude in Excel 和 Claude in PowerPoint 加载项。想更全面地了解 Cowork 与各职能的插件更新，请参阅[配套博文](https://claude.com/resources/articles/cowork-plugins-across-enterprise)。
