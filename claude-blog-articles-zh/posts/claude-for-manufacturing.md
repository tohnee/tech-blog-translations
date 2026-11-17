---
title: "Claude for Manufacturing 正式发布"
title_en: "Introducing Claude for Manufacturing"
date: 2026-11-12
source: https://claude.com/resources/articles/claude-for-manufacturing
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude for Manufacturing 正式发布

> 原文：[Introducing Claude for Manufacturing](https://claude.com/resources/articles/claude-for-manufacturing) · Claude 博客

一个包含 17 项技能和四个连接器的新插件，帮助制造商基于其现有系统中运行的数据，起草报价单、质量报告和供应商询价。

今天我们正式发布 [Claude for Manufacturing（在新标签页中打开）](http://claude.com/solutions/manufacturing)。这是一个插件，其中的技能覆盖从给新工单定价到诊断停机设备的各类工作。现在，估价员可以让 Claude 读取客户的需求、比对类似工单的成本，并起草报价单。该插件通过连接器接入 Autodesk Fusion、Infor、Microsoft 365 和 Oracle NetSuite，直接基于制造商自己的记录工作。Claude for Manufacturing 的设计原则是：在成果送达客户或供应商之前，由相应负责人进行审阅和批准。

制造团队每天可能有大量时间都花在收集信息上。在 2025 年 Manufacturing Leadership Council 的一项调查中，79% 的制造商表示他们[手动录入数据（在新标签页中打开）](https://manufacturingleadershipcouncil.com/survey-october/)。有了 Claude 把每个流程推进到待审阅环节，估价员可以专注于价格，质量工程师可以专注于修复方案，技术员可以专注于先检查什么。

## **为制造商打造的技能**

该插件的 17 项技能覆盖销售、质量、运营、供应链、设计和设置。有些技能处理单一任务，有些则按顺序执行多个任务，因此 Claude 可以把一项工作推进好几个步骤，直到需要人工审阅为止。这些技能可以运行的流程包括：

* **为新工单报价：** 估价员可以让 Claude 读取客户的需求、列出缺失的信息、比对类似工单的成本，并起草报价单以供发布。
* **调查检验失败：** 质量工程师可以让 Claude 记录失败情况、检索以往报告中的同类问题、对可能原因排序，并起草纠正措施报告。
* **诊断故障停机：** 技术员可以让 Claude 读取传感器导出数据、维修记录、照片和手册，然后对可能原因排序，供技术员核查并决定下一步。
* **向其他供应商寻源：** 采购员可以让 Claude 准备询价请求，然后比对收到的各方报价。
* **用 Autodesk Fusion 比较设计：** 工程师可以让 Claude 基于现有模型生成多个变体，按工程师设定的目标为其打分，并起草决策备忘。
* **报送生产情况：** 工厂经理可以让 Claude 把生产数据汇总成一份报告，呈现实际产出与目标的对比、设备停机情况，以及停机与产出缺口造成的成本。

这些技能只是一个起点。组织可以在此基础上扩展，以适配自身的具体运营，我们也计划随时间推移不断增加新的制造业技能。

## **连接制造业系统**

Claude for Manufacturing 与制造业运营核心的软件协同工作，而这些软件始终是团队经营业务的核心：

* **Autodesk Fusion：** 工程师可以在做出选择之前比较更多设计方案，因为 Claude 能基于他们现有的模型生成多个变体。
* **Infor：** 采购员和计划员可以在行动之前核对采购订单和库存，因为 Claude 会在 Infor 中查询这些信息。
* **Microsoft 365：** 质量工程师可以把作业规程、供应商邮件和导出的报告放进同一项工作中，因为 Claude 会在共享文件夹和收件箱里找到它们。
* **Oracle NetSuite：** 估价员可以对照实际订单、库存、生产工序和工单成本为新工作定价，因为 Claude 在起草报价单时会调取这些记录。

制造商也可以把该插件与没有连接器的系统配合使用。他们把这类系统的定期导出文件保存到 Microsoft 365，Claude 便能基于这些文件起草报价单或汇总生产报告。

## **用 Claude 在 Infor 中做出变更**

为制造商提供核心软件的 Infor 也[发布了自己的插件（在新标签页中打开）](https://claude.ai/directory/infor)。借助 Claude for Manufacturing 中的 Infor 连接器，团队可以查询记录；而借助 Infor 的插件，他们还可以从 Claude 中在 Infor 里做出变更。

例如，如果一批钢材的交付推迟了两周，采购员可以问 Claude 哪些客户订单会受影响、其他工厂还有多少钢材。采购员批准后，Claude 可以向另一家供应商下达采购订单，并在 Infor 中重新安排受影响的生产计划。Claude 的访问权限沿用该采购员在 Infor 中的权限。

## **制造团队始终掌握控制权**

技能在设计上都会以用户审阅作为终点：估价员核对并放行报价单，质量工程师核验纠正措施报告中的修复方案。为支持这一审阅，Claude 可以把数字和论断链接回底层的原始数据和文档。

Claude for Manufacturing 不操作设备。为此，Anthropic 正在开发 [Model Hardware Standard（在新标签页中打开）](https://www.anthropic.com/news/model-hardware-standard-research-preview)，这是一个研究预览版，为可编程设备提供一种标准方式，用来描述其测量值、设置和安全限值。

## **如何开始**

在 Team 或 Enterprise 套餐中，[安装该插件（在新标签页中打开）](https://claude.ai/customize/plugins/id/45112ff2-6233-4954-b8ec-c448ef2d1e59%40anthropic-plugin-directory)，然后对 Claude 说"帮我们配置好"。Claude 会询问团队使用哪些系统、测试各个连接器，并报告哪些技能目前还无法完整运行。

想看看插件的实际效果，请[报名参加我们的技术网络研讨会（在新标签页中打开）](https://claude.com/resources/webinars/claude-for-manufacturing-put-your-plants-know-how-to-work)，时间是 11 月 17 日美国东部时间上午 11:00。想详细讨论公司的制造系统，请[联系我们的销售团队（在新标签页中打开）](https://claude.com/contact-sales)。
