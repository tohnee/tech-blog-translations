---
title: "Grok Build 插件市场"
title_en: "Grok Build Plugin Marketplace"
date: 2026-06-11
source: https://x.ai/news/grok-plugin-marketplace
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok Build 插件市场

> 原文：[Grok Build Plugin Marketplace](https://x.ai/news/grok-plugin-marketplace) · xAI

[返回新闻列表](/news)

2026 年 6 月 11 日

为 Grok Build 推出内置插件市场。

---

今天我们推出 [Grok Build 插件市场](https://github.com/xai-org/plugin-marketplace)——一组面向 [Grok Build](https://x.ai/cli) 的内置插件。

一个插件（plugin）将 [skills](/news/grok-skills)、斜杠命令、智能体、hooks、MCP 服务器和 LSP 打包成一个可安装的单元。该市场内置于 Grok Build 之中，因此你无需离开终端即可浏览、安装和更新插件。

## [上线即可用](#available-at-launch)

市场上线之初就带来了来自全栈各类合作伙伴的插件：

- **[MongoDB](https://www.mongodb.com/docs/mcp-server/overview/)**——探索数据、管理集合、优化查询。
- **[Vercel](https://github.com/vercel/vercel-plugin)**——管理部署、查看构建状态、配置域名。
- **[Sentry](https://github.com/getsentry/sentry-for-ai)**——分析堆栈跟踪并调试生产环境错误。
- **[Chrome DevTools](https://github.com/ChromeDevTools/chrome-devtools-mcp)**——控制真实的浏览器、录制性能轨迹、检查网络请求。
- **[Cloudflare](https://github.com/cloudflare/skills)**——面向 Workers、Durable Objects 等的 skills。
- **[Superpowers](https://github.com/obra/superpowers)**——广受欢迎的智能体驱动工作流。

## [几秒内完成安装](#install-in-seconds)

在 Grok Build 中输入 `/marketplace` 浏览插件目录，按 `i` 即可安装插件。也可以直接使用 CLI：

Copy

```
grok plugin marketplace list
grok plugin install <name> --trust
```

bash

目录中的每个远程插件都固定（pin）到特定的 commit SHA，Grok Build 会在安装时校验该固定版本。

## [发布你自己的插件](#publish-your-own)

这个市场是一个开放的目录。如果你开发了想要分享的插件，可以向 [xai-org/plugin-marketplace](https://github.com/xai-org/plugin-marketplace) 提交 pull request。

## [快速上手](#getting-started)

刚接触 Grok Build？前往 [x.ai/cli](https://x.ai/cli) 安装并开始使用。
