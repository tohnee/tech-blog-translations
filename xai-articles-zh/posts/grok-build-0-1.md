---
title: "Grok Build 0.1 登陆 API"
title_en: "Grok Build 0.1 on API"
date: 2026-05-29
source: https://x.ai/news/grok-build-0-1
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok Build 0.1 登陆 API

> 原文：[Grok Build 0.1 on API](https://x.ai/news/grok-build-0-1) · xAI

[返回新闻列表](/news)

2026 年 5 月 29 日

Grok Build 0.1 是我们最快的编码模型，现已在 xAI API 上开启公测。

---

我们最新的编码模型 `grok-build-0.1` 现已在 xAI API 上开启公测。

`grok-build-0.1` 是一个专为智能体（agentic）编码任务训练的编码模型，涵盖 Web 开发、调试和 MCP 支持。它与驱动 [Grok Build CLI](https://docs.x.ai/build/overview#getting-started) 的是同一个模型。

该模型以超过 100 token/秒的惊人速度提供服务，定价为每百万输入 token 1 美元、每百万输出 token 2 美元。在编码之外，它也是通用智能体与工具调用用例中一个快速又经济的选择。

[立即试用](https://console.x.ai/team/default/chat-playground?model=grok-build-0.1&campaign=grok-build-0-1-blog)[创建 API 密钥](https://console.x.ai/team/default/api-keys?campaign=grok-build-0-1-blog)

bash

```
curl https://api.x.ai/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -d '{
    "model": "grok-build-0.1",
    "input": [
        {
            "role": "user",
            "content": "Generate a clean, tasteful, and minimalist personal website design with elegant typography"
        }
    ]
}'
```

`grok-build-0.1` 在智能体框架中表现最佳，例如 [Grok Build](https://docs.x.ai/build/overview)、Cursor、[Hermes Agent](https://x.ai/news/grok-hermes)、[OpenClaw](https://x.ai/news/grok-openclaw)、[Kilo Code](https://x.ai/news/grok-kilocode) 或 [OpenCode](https://x.ai/news/grok-opencode)。它也可以通过 [OpenRouter](https://openrouter.ai/x-ai/grok-build-0.1) 和 [Vercel AI Gateway](https://vercel.com/changelog/grok-build-0-1-now-available-on-vercel-ai-gateway) 使用。
