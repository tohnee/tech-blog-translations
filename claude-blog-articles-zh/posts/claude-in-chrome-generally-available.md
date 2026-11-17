---
title: "Claude in Chrome 正式可用"
title_en: "Claude in Chrome is generally available"
date: 2026-08-26
source: https://claude.com/resources/articles/claude-in-chrome-generally-available
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude in Chrome 正式可用

> 原文：[Claude in Chrome is generally available](https://claude.com/resources/articles/claude-in-chrome-generally-available) · Claude 博客

在浏览器里把任务交给 Claude，跨多个标签页工作，并在桌面端、移动端和网页版应用中继续这段对话。

[添加到 Chrome](https://claude.com/chrome)

Claude in Chrome 现已在所有付费 Claude 套餐中正式可用。Claude 现在还能在浏览器中自主执行操作，而不必每一项都等待批准。每个操作执行前都会经过安全分类器校验，以确保其安全且符合你的请求。

![](https://assets.claude.com/3c2048e47bcb81b96259929282f3477f560760cc.png)

你日常使用的许多工具都能[连接 Claude](http://claude.com/connectors)。但还有很多工具并未接入，例如内部仪表盘、遗留系统和供应商门户。Claude in Chrome 让 Claude 能够访问这些系统：它可以查看你当前所在的页面，并使用你现有的登录状态，执行读取和输入文本、点击链接、在页面之间跳转、填写表单等操作。

我们去年首次以试点形式发布了 Claude in Chrome，以便在测试它的同时加固我们针对[提示注入](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks)的防御：这类攻击把恶意指令藏在网站、邮件或文档中，试图诱骗 AI 智能体做出违背用户意愿的行为。下文所述的这些防御措施，让我们有信心将 Claude in Chrome 正式开放。

## 防范提示注入

正如我们在公布试点时所[说明](https://claude.com/resources/articles/claude-for-chrome)的，在浏览器中工作的 AI 智能体同样容易受到提示注入攻击。因此在更大范围发布 Claude in Chrome 之前，我们一直在努力改进防护措施。

在提示注入攻击中，恶意行为者会把指令藏在网页、邮件或表单字段等网络内容里。你可能根本看不到它们，但这些指令可以引导智能体去做你从未要求过的事。例如，如果你让 Claude 起草邮件回复，某封邮件里的一条隐藏指令就可能反而让 Claude 把你的其他邮件转发给攻击者。

发布时，我们介绍了如何测试 Claude 对这些攻击的防御能力，以及当时已有的防护措施；后来我们又发布了对[浏览器使用防护措施](https://www.anthropic.com/research/prompt-injection-defenses)更详细的说明。自那以后，我们改进了对模型和[探针](https://www.anthropic.com/research/next-generation-constitutional-classifiers)（probes）的训练方式，并新增了一组分类器，使 Claude 能够在 Chrome 中安全地执行更多自主操作。下一节我们将讨论评估结果，这些结果展示了上述防护措施的有效性。

**Claude 能识别更多攻击。** 我们用不断扩充的提示注入攻击库来训练 Claude，这些攻击来自我们的内部自动化攻击程序、外部红队测试人员以及真实世界监控。当一种新攻击成功攻破当前模型时，它就会被加入该库，用于指导未来模型的训练和已部署防护措施的学习，使它们学会识别这种攻击。自 2025 年 11 月我们首次撰文介绍[浏览器使用的提示注入防御](https://www.anthropic.com/research/prompt-injection-defenses)以来，Claude 抵御这类攻击的能力已大幅提升。

**探针会在 Claude 依据网页内容行动之前先行筛查。** 网页内容通过工具结果到达 Claude。要执行阅读页面或打开邮件之类的操作，模型会发起一次工具调用；工具结果让模型得以读取输出（在这里就是页面或邮件的内容）。我们训练探针扫描这些结果，以发现潜在的提示注入。当探针检测到疑似攻击时，Claude 会收到警告，要对该内容保持怀疑，并在必要时先与你确认再采取行动。我们最初是在 Claude Opus 4.5 上部署这些探针的，此后又扩大了它们覆盖的攻击类型。

**操作在执行前会经过验证。** 在 Claude in Chrome 中，Claude 现在会自动批准它判定为安全的操作，所用机制与 Claude Code 中的[自动模式](https://claude.com/resources/articles/auto-mode-default-in-claude-code)（auto mode）相同。（如果你更愿意继续手动批准 Claude 的操作，可以在设置中关闭该功能。）分类器会审查 Claude 即将执行的操作——例如访问新网站或向页面中输入文本——并对照你最初的请求进行检查。如果操作与你的请求不符，就会被阻止。

## 衡量 Claude 抵御提示注入的稳健性

我们对这些防护措施进行了测试，以确保 Claude in Chrome 可以安全地用于基于浏览器的工作。下面我们报告最近几次评估的结果。

在我们[最初的评估](https://claude.com/resources/articles/claude-for-chrome)中（该评估用于测试 Claude Cowork 对提示注入攻击的抵御能力，最早在发布 Claude in Chrome 试点时开发），在 [Cowork 执行框架](https://claude.com/resources/articles/cowork-chrome-side-panel)（harness）里，即使没有上述探针和分类器，也没有任何攻击能攻破 Claude Fable 5、Claude Opus 5 或 Claude Sonnet 5。

![](https://assets.claude.com/e04793e88e09e6b6d52c8e8c9ed288425d28bac2.png)

提示注入攻击对 Claude Opus 4.5、Sonnet 5、Opus 5 和 Fable 5 的成功率。Opus 4.5 以扩展思考（extended thinking）运行，因为它不支持我们较新的默认设置——自适应思考（adaptive thinking）。其他所有模型都以中等努力等级的自适应思考作为默认配置运行。我们 2025 年 11 月博文中讨论的结果是在未启用扩展思考的情况下跑出的；但由于 Fable 5 无法关闭思考，这里报告的是启用思考后的结果。11 月所用的评分模型也不再可用，因此我们改用了能力更强的评分流程，并配合对成功攻击的人工复核，从而减少了误报。

由于那套评估已被打满（成功率为 0% 即是明证），我们决定将其停用。在我们[当前的评估](https://www-cdn.anthropic.com/b514064af1408018e64b1ad24e7d5e75850b4ffd/Claude%20Opus%205%20System%20Card.pdf#page=76.73)中，攻击由专业红队人员提供、强度更高。在未加任何额外防护的情况下，到达模型的攻击对 Opus 4.5 的成功率为 17.6%，对 Opus 5 为 3.8%。使用 2025 年 11 月可用的最强防护时，针对启用了探针的 Opus 4.5 的攻击成功率为 16.7%。对于 Opus 4.8 及之后的所有模型，在同时启用探针和安全分类器的情况下，没有任何攻击能攻破 Claude Sonnet 5、Claude Opus 5 或 Claude Mythos 5。对 Fable 5 我们观察到的攻击成功率为 0.3%。我们已人工核实，所有成功攻破都发生在低严重程度的场景中，并正在努力缓解这些问题。

![](https://assets.claude.com/ae0ae4a995879f570a786bf1a42d04fd868a450e.png)

在同时启用探针和自动批准安全分类器的情况下，没有任何攻击能攻破 Claude Sonnet 5 或 Opus 5，对 Fable 5 的攻击成功率为 0.3%。Opus 4.5 的模型行为使到达模型的攻击数量较少，但其攻击成功率仍然最高。

提示注入始终是一个移动靶。这套方法能防御当前的攻击，但我们还需要确保防护措施始终领先于攻击者不断演进的手法。每发布一个模型，我们都会持续投入，开发更先进的自动化系统，用于攻击发现、红队测试以及构建更强的分类器。

## 开始使用

要开始使用 Claude in Chrome，请从 [Chrome 应用商店](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn)安装。在 Enterprise 套餐中，管理员可以在组织设置中管理该扩展，并将其限制在已批准的域名内。请参阅[管理员设置指南](https://support.claude.com/en/articles/13065128-claude-in-chrome-admin-controls#h_bdb63199e1)。

若要处理你电脑上的文件或与其他应用程序协作，你仍然需要使用 Claude 桌面应用。Claude in Chrome 目前还不能在其他 Chromium 浏览器或移动端上运行。

‍

*¹ 并非所有攻击都会到达——即被模型看到。在某些情况下，Claude 采取的操作使它根本不会遇到那些恶意指令。*
