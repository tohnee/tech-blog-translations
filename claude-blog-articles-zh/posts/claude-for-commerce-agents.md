---
title: "用 Claude 构建电商智能体"
title_en: "Building commerce agents with Claude"
date: 2026-09-02
source: https://claude.com/resources/articles/claude-for-commerce-agents
crawled: 2026-11-17
translated: 2026-11-17
---

# 用 Claude 构建电商智能体

> 原文：[Building commerce agents with Claude](https://claude.com/resources/articles/claude-for-commerce-agents) · Claude 博客

在 Claude 上运行购物智能体的零售商，购物车规模最多提升了 35%，消费者完成购买的可能性提高了 60%。

全球许多大型[零售商](https://claude.com/resources/articles/j-crew-style-advisor-with-claude)、市场平台、电商平台和旅行公司都在用 Claude 构建让购物更轻松的智能体。Shopify、Priceline 等企业客户已经在用智能体，让消费者用自然语言描述需求，由 AI 搜索、找到、比较并购买。

今天，我们发布一套蓝图（blueprint），帮助大家在 Claude 上构建电商智能体。它包含工程团队让一个电商智能体在几天内跑起来所需的执行框架、模式和防护栏，并附有面向零售、旅行、电信和票务平台的购物智能体与商家智能体的参考实现。此外还提供一个 Claude Code 插件，帮你快速上手。

代码可以部署在你已经在用的 Claude 构建环境中，包括 Claude API、Amazon Bedrock、Microsoft Foundry 或 Google Cloud Vertex AI。你也可以与我们解决方案和生态合作伙伴（如 Accenture、Mastercard 和 Visa）合作——他们正与我们携手，帮助客户和商家社区用上这些蓝图。

它[现已开放获取](https://github.com/anthropics/commerce-agents)，每个垂直行业都有[在线演示](https://claude.com/solutions/commerce)，还有一篇讲解其构建方式的[工程深度文章](https://claude.com/resources/articles/the-anatomy-of-effective-commerce-agents)——正好赶上假日季的规划节奏。

![](https://assets.claude.com/b9ec1abf25aff70e3ad5f91895c78ad550cf92e3.jpg)

在 ACME 零售示例中运行的购物智能体。

## 蓝图包含什么

仓库中包含购物智能体和商家智能体的完整可运行实现，可以基于 [Messages API](https://platform.claude.com/docs/en/intro)、[Agent SDK](https://code.claude.com/docs/en/agent-sdk) 或 [Claude 托管智能体（Claude Managed Agents）](https://platform.claude.com/docs/en/managed-agents/overview)（beta）构建。你可以在写任何代码之前，先通过自助演示看它们运行，然后用 Claude Code 按自己的商品目录、政策、品牌等进行定制。

### 购物智能体

购物智能体运行在你的 App 或网站内。蓝图包含商品目录、购物车、结账、客户偏好和订单历史的集成点，支付环节则留给你自己——可以用现有的结账流程，也可以接入智能体支付服务商。

客户可以说"我要带孩子周末露营，需要一顶帐篷、一个睡袋和一个炉子"，智能体就能从这里接手。它能够：

* 搜索商品目录并组合出正确的商品集合，包括多商品请求。
* 记住客户偏好，并据此调整推荐。
* 在对话中直接展示商品、对比和购物车，而不只是纯文本。
* 构建购物车并交给结账流程。
* 在同一段对话里回答客服问题，比如订单物流、如何退货换货、退款政策怎么规定，而不必把客户打发到帮助页面。

该智能体内置防护栏，把价格和商品限制在真实的商品目录数据范围内，并避免操纵性的追加销售模式。在仓库中，这些能力以技能和工具的形式提供，涵盖商品目录搜索、多商品规划、深度研究、个性化、客户服务和会话内 UI。

### 商家智能体

商家智能体服务于经营店铺的人。用户问"清理上季库存应该给哪些商品打折？"，就能得到基于自身数据的答案。它能够：

* 回答销售表现问题，比如哪些好卖、哪些不好卖。
* 跟踪库存并主动标记问题，比如某件商品在促销开始前就要售罄。
* 基于店铺自身的销售历史推荐定价和促销方案。
* 起草营销活动，把需要动销的商品推出去。

当智能体主动提出变更建议时，需要有人批准才会生效——也就是说，智能体盯着店铺，用户拥有最终决定权。在仓库中，这些能力以技能的形式提供，涵盖销售分析、商品目录与库存管理、营销与促销，以及图表、仪表盘等门户内 UI。

![](https://assets.claude.com/045755d6e355214e83ca27b6378b2fb4dde6d3cf.png)

## 全行业信赖

服务消费者、旅客、订阅用户和商家的公司都在 Claude 上构建和运行智能体。以下是他们对用 Claude 构建电商智能体的评价：

![Zomato](https://assets.claude.com/7b06fdb76b1b2e350bd19549c430d46d8a147631.svg)

> "我们的工程师把蓝图跑起来了，全程没有阻碍；安装配置与文档完全一致。它内建的实践——从工具迭代上限到提示缓存——正是我们在构建 Zomato 自家智能体时总结出的那些。在 Claude 上搭建第一个智能体的团队，能省掉几周的试错时间。"

Akhil Bansal，高级工程经理

![Fetch](https://assets.claude.com/baf2ceeaaabf6636e392fb03b3796544fa67966a.svg)

> "我们的工程师在不到一小时内就把 Anthropic 蓝图中的两个电商智能体在本地跑了起来，实时对话第一次尝试就通了。我们把 Claude Code 工作流跑了两遍，得到两套不同的架构，各自都按我们的要求设计。对从零开始的团队来说，这把数天的智能体脚手架工作压缩到了几小时。"

Ashley Nader，Staff 产品经理

![Square](https://assets.claude.com/8054b096faa0b59ca686be2f59ac108fa0a98638.svg)

> "我们在 Square 做的很多事情，都是为了让卖家省回时间，而智能体让我们这项能力大幅跃升。我们在构建智能体工具，观察销售、人力和库存，给出真正的下一步行动，而不只是一个答案，同时让卖家始终掌控全局。信任是这项工作最难的部分，Claude 帮助我们达到了很高的标准。"

Willem Avé，产品负责人

![Visa](https://assets.claude.com/0e2431b0f4c10fb7cdaa4c5a08d3048cf0320583.svg)

> "AI 将从根本上重塑商业，但信任必须始终居于每一笔交易的中心。商家告诉我们，他们希望对 AI 如何触达其客户拥有更多控制权。我们与 Anthropic 在电商蓝图上的合作，把 Claude 的智能与 Visa 网络的信任、安全和全球覆盖结合起来，让商家能够提供更好的客户体验，同时维护推动其业务前行的客户关系。"

Jack Forestell，首席产品与战略官

![Mastercard](https://assets.claude.com/fe3fc522db9dc6e27e569e2275c67babeb168ff9.svg)

> "信任是商业的通行货币，在智能体时代更是如此。借助 Anthropic 的电商蓝图，我们帮助商家用 Claude 构建自己的智能体来驱动增长。把 AI 创新与可信的支付和商业基础设施结合起来，我们正在帮助消费者、商家和 AI 智能体以安全、无缝、规模化的方式连接。"

Sherri Haymond，执行副总裁、全球数字化商业负责人

![Accenture](https://assets.claude.com/eef8a51d4b99d31d65fa28d41f247f85bc363b45.svg)

> "对于希望提供当今消费者所期待的个性化、智能化客户体验的组织而言，电商智能体正迅速成为一项关键能力。我们最新的研究显示，85% 的消费者如今愿意与 AI 智能体协作，近四分之三的人愿意让个人 AI 智能体替自己完成购买，甚至比最亲密的朋友更信任它。这不仅是购物方式的变化。智能体电商正在改写品牌价值的规则——从根本上影响买什么、何时买、在哪买、由谁买。Anthropic 的电商智能体蓝图为组织提供了一个经过验证的起点，帮助加速部署并构建差异化体验，从而提升客户满意度、忠诚度和增长。结合 Accenture 在零售和消费品领域的深厚专长，我们可以帮助客户从概念走向生产，更快地从智能体 AI 中获得价值。"

Kath Gramling，全球消费品、零售与旅行负责人

![Priceline](https://assets.claude.com/8ddfae0a9bf7f1b17537d760f26449eac334f4cc.svg)

> "旅行是人们购买的最复杂的东西之一：航班、酒店、租车，以及几十个需要权衡的选项。我们的 AI 助手 Penny 能在一段对话里处理所有这些，并呈现最佳选项和最佳价值。我们在 Claude 上构建了最新一代 Penny，因为这类推理正是 Claude 模型擅长的。"

Cobus Kok，副总裁、AI 体验

![Intuit](https://assets.claude.com/b730fa6588d08aef3d1c1e12fbe768211c465c24.svg)

> "数百万消费者、企业和会计师在 Intuit 上管理财务。我们与 Anthropic 这样的伙伴合作，构建高度个性化的体验，让客户清楚理解其业务正在发生什么变化、为什么变化，从而能够充满信心地采取行动。我们把包括 Claude 在内的前沿 AI 推理能力，与我们专有的数据、能力、智能和人类专业知识结合起来，打造一个智能化的金融系统，为客户开启更高水平的繁荣。"

Chris Kasten，Intuit 首席架构师、工程高级副总裁，平台与开发加速事业部

![Shopify](https://assets.claude.com/33de1bc0b1b2c92e879e513e3c14ec213c311ff1.svg)

> "我们希望商家出现在消费者购物的任何地方，而这越来越多地意味着与智能体的一段对话。我们基于 Anthropic 的蓝图构建了一个参考店铺实现，通过 Catalog、UCP 和 Shop Sign-in 把智能体连接到商家的店铺。商家可以用 Claude 构建智能体，帮助客户找到商品、完成结账，并回答订单相关问题。"

Vanessa Lee，产品副总裁

![Klaviyo](https://assets.claude.com/6187fcdd66b66e7fc77047e18645f766fb5e2182.svg)

> "电商和出色的客户体验都需要个性化，而 Klaviyo 上的每个品牌都坐拥远超任何团队手工处理能力的客户数据和决策。Claude 弥合了这一差距，把消费者偏好和表现数据转化为驱动营收的洞察、营销活动和个性化。这正是我们持续与 Anthropic 共建的原因：智能体完成复杂的分析、设计和决策，企业则可以专注于取悦客户。"

Andrew Bialecki，创始人、联席 CEO

![Wix](https://assets.claude.com/31f3d282988b62d2920e9374b2e0571f60d5c3f9.svg)

> "Wix 的使命一直是让复杂技术变得简单、易用。对商家而言，这意味着在不增加运营复杂度的前提下提供强大的商业能力，而智能体是顺理成章的下一步。我们的工程师在十五分钟内就让一个电商智能体跑起来并接受提示词，试点展示了把 Anthropic 的 AI 能力与 Wix 的商业平台及我们在中小企业电商领域的深厚专长结合起来有多大的潜力。"

Dror Zalika，Wix 商业负责人

## 开始使用

蓝图现已可用。[联系我们的销售团队](https://claude.com/contact-sales)，了解更多信息、预约演示，或讨论如何在你的组织中落地。

1. 在 [github.com/anthropics/commerce-agents](https://github.com/anthropics/commerce-agents) Fork 仓库。
2. 阅读工程深度文章：[claude.com/blog/the-anatomy-of-effective-commerce-agents](https://claude.com/resources/articles/the-anatomy-of-effective-commerce-agents)。
3. 在 [claude.com/solutions/commerce](https://claude.com/solutions/commerce) 查看各垂直行业演示，并申请一次工作坊。

注册我们的[网络研讨会](https://claude.com/resources/webinars/building-claude-commerce-agents)，观看深度讲解——届时我们将分享现场演示、实操讲解，并介绍电商构建者如何最大化利用 Claude。
