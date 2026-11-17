---
title: "Claude 在 Cowork 中有了自己的浏览器"
title_en: "Claude gets its own browser in Cowork"
date: 2026-08-26
source: https://claude.com/resources/articles/cowork-built-in-browser
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude 在 Cowork 中有了自己的浏览器

> 原文：[Claude gets its own browser in Cowork](https://claude.com/resources/articles/cowork-built-in-browser) · Claude 博客

Claude 在桌面应用中打开自己的浏览器来浏览网站、阅读页面并填写表单。

在桌面版 Claude Cowork 中，Claude 现在拥有内置浏览器。当任务需要用到某个网站时，侧边栏会打开一个浏览器，Claude 会在其中浏览网页、阅读内容、点击并输入。现在，你可以把任务中涉及网页的部分交出去，自己留在原地：Claude 可以填写表单、从仪表盘中提取数字，或者在一个没有连接器的门户中完成操作。无需扩展程序，无需设置，除非你主动选择，否则不会共享你个人浏览器中的任何内容。

在此之前，要让 Claude 在 Cowork 中使用 Web，需要通过 [Claude in Chrome](http://claude.com/claude-in-chrome) 扩展授予它访问你浏览器的权限。当工作就在你已经打开的页面上时，这仍然是正确的选择。但许多 Web 任务并不需要*你的*浏览器，只需要*一个*浏览器——现在 Claude 有了自己的浏览器。

该功能本周起在 Claude 桌面应用中向 Pro、Max、Ultra 和 Team 套餐推出。Enterprise 管理员可以从今天起为其组织开启该功能。

## 用哪个浏览器，何时用

这是 Claude 的浏览器，不是你的。内置浏览器与你的浏览器相互独立。Claude 永远看不到你的标签页、书签或密码。为了保持网站登录状态，你可以逐个站点导入登录信息：在 macOS 上可从 Chrome、Edge 或 Firefox 导入，在 Windows 和 Linux 上可从 Firefox 导入。除非你主动选择包含，否则银行、电子邮件和单点登录站点不在导入范围内。

这也正是 Claude 使用 Web 的两种方式之间的区别。内置浏览器用于在你继续工作的同时把 Web 任务交给 Claude：为报告收集研究资料，或从供应商门户收集本月的发票。Claude in Chrome 则用于你已经打开的那个页面，使用你已经登录的账号，例如更新 CRM、处理收件箱，或编辑眼前的文档。

如果你已经在使用 Claude in Chrome，它会继续可用并保持为你的默认选项；否则 Claude 会使用内置浏览器。你可以随时在 Settings → Cowork → Preferred browser 中切换。

## 保持掌控

与任何在浏览器中行动的 AI 智能体一样，内置浏览器也面临[提示注入](https://www.anthropic.com/research/prompt-injection-defenses)风险：页面中隐藏的指令会试图把 Claude 引向别处。它采用与 Claude in Chrome 相同的防护措施，包括根据你提出的要求审查 Claude 行为的检查。我们在 [Claude in Chrome 博客文章](https://claude.com/resources/articles/claude-in-chrome-generally-available)中对此作了说明。这些措施能显著降低风险，但无法完全消除，因此我们建议先从你信任的站点开始。更多内容请阅读我们的[安全指南](https://support.claude.com/en/articles/12902428-use-claude-in-chrome-safely)。

## 开始使用

内置浏览器将在接下来一周内陆续向 Claude 桌面应用（macOS、Windows 和 Linux，Linux 为 beta）上的 Pro、Max、Ultra 和 Team 套餐推出。一旦可用，它默认开启：给 Claude 一个涉及网站的任务，浏览器就会自行打开。在 Enterprise 套餐中，它现已可用，管理员可在 Organization settings → Cowork → Built-in browser 中管理。

内置浏览器运行在桌面应用中。只要你的桌面应用保持打开并联网，你就可以从 Web 或手机端驱动它。在没有桌面应用的 Web 端，Claude in Chrome 仍然是给 Claude 提供浏览器的方式。
