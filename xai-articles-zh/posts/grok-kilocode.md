---
title: "在 Kilo Code 中使用 Grok"
title_en: "Use Grok in Kilo Code"
date: 2026-05-27
source: https://x.ai/news/grok-kilocode
crawled: 2026-09-22
translated: 2026-09-22
---

# 在 Kilo Code 中使用 Grok

> 原文：[Use Grok in Kilo Code](https://x.ai/news/grok-kilocode) · xAI

[返回新闻列表](/news)

2026 年 5 月 27 日

在开源智能体编码平台 Kilo Code 中使用你的 SuperGrok 或 X Premium+ 订阅。

---

从今天起，你可以直接在 Kilo Code 中使用你的 Grok 订阅。

Kilo Code 是面向 VS Code、JetBrains IDE 和终端的开源智能体工程平台。它为规划、编码、调试和编排提供专用模式，还具备强大的工具调用、浏览器自动化、MCP 可扩展性，并支持 500 多个模型。Kilo 为真实软件工程工作流和智能体用例而设计。

凭你的 X Premium+ 或 SuperGrok 订阅，连接你的 Grok 账号，即可在 Kilo Code 中使用最新的 Grok 模型——包括用于智能体编码的 Grok Build——无需单独的 API 密钥。

### [设置](#setup)

Kilo Code 提供 IDE 扩展、CLI 和网页版。要连接你的 xAI 账号，请按照以下说明操作：

**VS Code：**

1. 从 VS Code 应用市场安装 [Kilo Code](https://marketplace.visualstudio.com/items?itemName=kilocode.Kilo-Code)。
2. 打开**设置**（齿轮图标），进入 **Providers（提供方）** 标签页。
3. 点击 **Show more providers（显示更多提供方）**，然后搜索或选择 **xAI**。
4. 选择 **xAI Grok OAuth（SuperGrok 订阅）** 登录选项，并在浏览器中完成 OAuth 流程。

在无头或远程环境（VPS、SSH、Docker、WSL）中，请改选 **xAI Grok OAuth（Headless / Remote / VPS）**。

**CLI：**

bash

```
npm install -g @kilocode/cli
```

在项目目录中运行 `kilo`，并使用 `/connect` 命令添加 xAI。

更多细节请参阅 [Kilo Code xAI 提供方文档](https://kilo.ai/docs/ai-providers/xai)。

更多开源智能体与集成即将推出。
