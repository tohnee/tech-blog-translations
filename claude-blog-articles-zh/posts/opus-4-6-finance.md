---
title: "用 Claude Opus 4.6 推动金融工作进阶"
title_en: "Advancing finance with Claude Opus 4.6"
date: 2026-02-05
source: https://claude.com/resources/articles/opus-4-6-finance
crawled: 2026-11-17
translated: 2026-11-17
---

# 用 Claude Opus 4.6 推动金融工作进阶

> 原文：[Advancing finance with Claude Opus 4.6](https://claude.com/resources/articles/opus-4-6-finance) · Claude 博客

借助 Claude Opus 4.6，金融团队在复杂分析上获得更强的推理能力、更干净的首轮交付物，以及为分析师真正投入时间之处打造的新工具。

[Claude Opus 4.6](https://www.anthropic.com/news/claude-opus-4-6)标志着金融 AI 向前迈进了一步。它可以帮助专业人士基于准确信息和清晰分析做出决策，并产出真正精致的交付物。该模型在金融推理、多任务处理以及在较长多步任务中保持专注方面，明显优于市场上的其他模型。

与 Claude Opus 4.6 一同，我们更新了部分现有产品，并推出一款新产品，把这些能力放到分析师花费大部分时间的地方。[Cowork](https://claude.com/product/cowork)现在首轮就能交付更精致的输出，如财务模型和演示文稿。[Claude in Excel](https://claude.com/claude-in-excel)现在更擅长处理长时间运行的任务，随着财务模型变得更复杂，Claude Opus 4.6 仍能保持专注和准确。我们还发布了 [Claude in PowerPoint](https://claude.com/claude-in-powerpoint)的研究预览版（beta），用于原生构建和迭代演示文稿。

我们的内部 Real-World Finance 评测衡量 Claude 在约 50 个投资与金融分析用例上的表现，涵盖电子表格、幻灯片和 Word 文档的生成与审阅。这些是投资银行、私募股权、公开市场投资和企业财务领域分析师常做的任务。Claude Opus 4.6 相比 Claude Sonnet 4.5——几个月前我们最先进的模型——提升超过 23 个百分点。

![](https://assets.claude.com/b7a4d8eeaf9ad8f394f7771b89873964e54c77fd.png)

该评测测试代码执行与工具使用智能体框架的组合，评分基于一组量规与偏好，考察金融领域知识、任务完整性与准确性，以及呈现质量。

这些更新共同使 Claude 成为金融服务和企业财务从业者强大得多的伙伴。

## 研究、分析、创作

金融专业人士用 AI 在多个数据源之间高效研究、支撑财务分析，并创建团队和客户可以据以行动的交付物。Claude Opus 4.6 在这三个维度上都处于同类最佳。

![](https://assets.claude.com/14a33fb672906936a3baaa484509fd39e050bb67.png)

在研究方面，Claude Opus 4.6 在 BrowseComp 和 DeepSearchQA 两项基准上均有提升，它们测试模型从大型非结构化数据源中提取特定信息的能力。在实践中，这意味着用户可以把一整套密集文档交给 Claude，得到具体、聚焦的答案，而不是一份简单的摘要。

在分析方面，Claude Opus 4.6 在 [Finance Agent](https://www.vals.ai/benchmarks/finance_agent)上达到 60.7%（较 Opus 4.5 提升 5.47%），处于最先进水平；这是 Vals AI 的外部基准，评测模型对上市公司 SEC 文件的研究能力。Opus 4.6 在 Vals AI 的 [TaxEval](https://www.vals.ai/benchmarks/tax_eval_v2)上同样以 76.0% 处于最先进水平。

在创作方面，除 Real-World Finance 评测外，我们还用 GDPval-AA 衡量 Claude 在复杂知识工作中的表现。使用 Claude Opus 4.6，电子表格和演示文稿等结构化输出首轮就正确的频率更高。下面的并排输出展示了从 Claude Opus 4.5 到 Opus 4.6 输出质量的提升。这些是 Claude 在商业尽职调查任务（评估一项潜在收购）上的首轮表现示例——这类工作通常需要资深分析师花两到三周完成。

![](https://assets.claude.com/82bcf86e07b6fa2d0988fa8b53e43b7a88f6ce9a.png)![](https://assets.claude.com/0484be28208d116d14d9329566510bc925c2a381.png)
> "借助 Claude Opus 4.6，过去要花几小时制作财务 PowerPoint，现在只需几分钟。我们看到在细节关注、空间布局和内容结构方面都有切实提升。"——Aabhas Sharma，Hebbia CTO

> "Claude Opus 4.6 的性能跃升几乎令人难以置信。过去对 Opus [4.5] 颇具挑战的真实任务，突然变得轻松。对 Shortcut 上的电子表格智能体来说，这感觉像是一个分水岭时刻。"——Nico Christie，Shortcut AI 联合创始人兼 CTO

## 更强的多任务处理与初稿

通过 Cowork 可以轻松使用 Claude Opus 4.6 的金融能力——这是我们桌面应用中[一种使用 Claude 的新方式](https://claude.com/blog/cowork-research-preview)。

在 Cowork 中，你让 Claude 访问你选定的一个桌面文件夹。Claude 可以直接在该文件夹中读取、编辑和创建新文件。对金融团队而言，这意味着你可以同时启动多项分析，同时在 Claude 制作每份交付物时引导其思路，使其符合你的标准。

Cowork 还可以[通过插件](https://claude.com/resources/articles/cowork-plugins)定制——插件是技能（规定如何完成一项任务）与连接其他平台数据的连接器的组合。例如，使用[我们的企业财务插件](https://claude.com/plugins/finance)，Claude 能立即知道如何完成日记账分录、差异分析和对账等常见工作流。你也可以[构建自己的插件](https://support.claude.com/en/articles/13345190-getting-started-with-cowork)，以匹配你喜欢的工作方式。

Cowork 作为仅桌面端的研究预览版（beta）在[所有付费 Claude 套餐中提供](https://support.claude.com/en/articles/13345190-getting-started-with-cowork)¹。

## 无需离开电子表格即可深入

Claude in Excel 把 Claude Opus 4.6 直接带到你的电子表格中。我们让它更擅长与用户一起规划并澄清假设，尤其是在任务变得更复杂时。它现在还支持数据透视表编辑、图表修改、条件格式、排序与筛选、数据验证，以及金融级格式设置。

最后，我们加入了一些易用性改进，包括长对话的自动压缩和多文件拖放支持。这意味着你在标签页之间复制粘贴的操作会大大减少。从财务模型到可交付客户的活页夹，你都可以在一个地方与 Claude 协作完成。

![](https://assets.claude.com/690b5a4255a334e2b64adbb31735584d0b2552ae.png)
> "由 Claude Opus 4.6 驱动的 Claude in Excel 是一次重大飞跃。从尽职调查到财务建模，它正被证明是我们团队极其强大的工具——接收非结构化数据，在极少提示下智能处理，以有意义的方式自动化复杂分析。这是 AI 以切实、省时的方式增强投资专业人士能力的一个绝佳例子。"——Lloyd Hilton，Hg Catalyst 负责人

> "作为加拿大最大的机构投资者之一，我们不断创新，并看到 AI 处在塑造我们未来的最前沿。Claude Opus 4.6 在速度、精度和复杂任务处理能力上的提升——例如 Claude in Excel 中的多标签页分析——为我们的工作方式解锁了令人兴奋的可能性。"——Ben Letalik，BCI 数字化转型与创新高级总监

## 直接在 Claude 中打磨你的演示文稿

我们同时将 Claude in PowerPoint 作为研究预览版（beta）推出。就像 Claude in Excel 一样，它把 Claude 带入你的 PowerPoint 侧边栏，让它先读取你现有的版式、字体和母版，然后再在线创建新内容。Claude 可以基于客户模板构建演示文稿，对现有幻灯片做针对性编辑，并从零生成一份出色的初版演示。

![](https://assets.claude.com/2f34a7c546be3ff8d564b9c3bda776140556c508.png)

Claude in PowerPoint 现已作为研究预览版，向所有 Max、Ultra、Team 或 Enterprise 套餐用户开放。

## 开始使用

Claude Opus 4.6 与我们最新的产品更新使一系列新任务成为可能。但金融 AI 仍是一片活跃的前沿。用户应继续审查 Claude 的输出，确保其符合自己的规范；尤其是高风险工作，人类判断仍然不可或缺。随着我们持续提升 Claude 的能力，我们的目标是不断为金融行业专业人士配备更强大的研究与分析工具，帮助他们专注于最重要的工作。

Claude Opus 4.6、Cowork 和 Claude in Excel 在所有付费 Claude 套餐中提供。如需了解 Claude in Excel 的更多信息，请浏览我们的[指南](https://support.claude.com/en/articles/12650343-claude-in-excel)和[视频教程](https://claude.com/resources/tutorials/getting-started-with-claude-in-excel)，并[从这里开始](https://claude.com/claude-in-excel)。Claude in PowerPoint 以研究预览形式向所有 Max、Ultra、Team 和 Enterprise 用户开放，你可以[从这里开始](https://claude.com/claude-in-powerpoint)。

想了解各类组织如何实际使用这些新功能，请[注册我们的网络研讨会](https://claude.com/resources/webinars/claude-in-excel-and-powerpoint)。

#### *Cowork 作为仅桌面端的研究预览版，在[所有付费 Claude 套餐中提供](https://support.claude.com/en/articles/13345190-getting-started-with-cowork)，首发于 Mac（Windows 版即将推出）。*
