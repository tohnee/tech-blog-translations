---
title: "Claude in Chrome 侧边栏现在是 Claude Cowork"
title_en: "The Claude in Chrome side panel is now Claude Cowork"
date: 2026-08-12
source: https://claude.com/resources/articles/cowork-chrome-side-panel
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude in Chrome 侧边栏现在是 Claude Cowork

> 原文：[The Claude in Chrome side panel is now Claude Cowork](https://claude.com/resources/articles/cowork-chrome-side-panel) · Claude 博客

在浏览器中把任务交给 Claude，跨标签页工作，并在桌面端、移动端和 Web 应用中继续对话。

[Claude in Chrome](https://claude.com/resources/articles/claude-for-chrome) 侧边栏现在就是一个 [Claude Cowork](https://claude.com/product/cowork) 会话。对话会保存到你的历史记录中，你的技能和连接器可在浏览器中工作，你在某个标签页中开始的任务可以在 Claude 桌面端、Web 端和移动应用中完成。该功能今天已在 Max 和 Team 套餐上线，并将在未来几周向 Pro 用户推出。

Claude in Chrome 是一款浏览器扩展，让 Claude 能看到你所在的页面并在其中执行操作，包括点击链接、输入文字、在页面之间跳转和填写表单，并使用你现有的登录状态。

你日常使用的许多工具都[直接连接到 Claude](http://claude.com/connectors)，但另一些则不能，比如内部仪表盘、遗留系统和供应商门户。借助 Claude in Chrome，Claude 可以通过浏览器在这些应用中工作。

在此之前，侧边栏中的会话与 Claude 各应用中的会话是分开的，因此上下文和对话无法在两者之间延续。现在，侧边栏运行的是你在桌面端、Web 端和移动端用于更长、多步骤工作的同一个 Claude Cowork 会话。由于会话跟随你的账号而非单台设备，你可以在浏览器中开始工作，之后在其他地方接着做。

![](https://assets.claude.com/cfb4072a7ab00b6aa3bc7dc0eb8deca9aa3f5a05.png)

举个例子，假设你正在制作一份预算表格，需要从几个供应商门户中提取发票。现在，你可以让 Claude in Chrome 收集金额和日期，它会打开这些标签页、读取每张发票并生成表格。之后，你可以在桌面应用中接着这个会话，添加电脑上的文件，或导入上个月的预算并询问哪些地方发生了变化，让你在工作过程中跨不同界面保持上下文。

## 理解风险

Claude in Chrome 承载着与任何在浏览器中行动的 AI 智能体相同的风险，主要是[提示注入](https://www.anthropic.com/research/prompt-injection-defenses)。恶意行为者会把指令隐藏在网页内容中，比如网页、电子邮件或文档里。这些指令可能对你不可见，但它们可以诱导 Claude 执行你从未意图的操作。

[自试点以来](https://claude.com/resources/articles/claude-for-chrome)，我们增加了一项对 Claude 自身操作的检查。使用“自动批准”后，Claude 会在不逐步请求许可的情况下完成一项任务。在提交表单、发送消息或下载文件等任何有后果的操作之前，一项独立的检查会将这一操作与你最初提出的要求进行比对，并阻止任何不匹配的操作。这样在保持监督的同时减少了打断。

在某些不可逆或代价高昂的操作之前，Claude 仍会先询问，比如进行购买或共享个人数据。这些措施能显著降低风险，但无法彻底消除。提示注入是一个不断变化的目标，因此我们会持续寻找新的攻击方式，并把学到的内容构建进我们发布的每一个模型中。我们建议从你信任的站点开始，我们的[安全指南](https://support.claude.com/en/articles/12902428-use-claude-in-chrome-safely)中有更多最佳实践。

## 开始使用

要开始使用 Claude in Chrome，请从 [Chrome Web Store](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) 安装、登录并打开侧边栏。新的侧边栏今天已在 Max 和 Team 套餐上线，并将在未来几周向 Pro 用户推出。在 Enterprise 套餐中，Claude in Chrome 默认关闭。管理员可以开启它，并将其限制在已批准的域名中。请参阅[管理员设置指南](https://support.claude.com/en/articles/13065128-claude-in-chrome-admin-controls#h_bdb63199e1)。

你仍然需要使用 Claude 桌面应用来处理电脑上的文件或与其他应用协作。Claude in Chrome 目前尚不支持其他 Chromium 浏览器，也不支持移动端。
