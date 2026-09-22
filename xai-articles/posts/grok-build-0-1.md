---
title: "Grok Build 0.1 on API"
date: 2026-05-29
source: https://x.ai/news/grok-build-0-1
crawled: 2026-09-22
---

[Back to news](/news)

May 29, 2026

# Grok Build 0.1 on API

Grok Build 0.1, our fastest coding model, is now available via the xAI API in public beta.

---

Our latest coding model, `grok-build-0.1`, is now available via the xAI API in public beta.

`grok-build-0.1` is a coding model specifically trained for agentic coding tasks, including web development, debugging, and MCP support. It's the same model that powers the [Grok Build CLI](https://docs.x.ai/build/overview#getting-started).

The model is served at a blazing-fast 100+ tokens/second and is priced at $1/m tokens in and $2/m tokens out. Outside of coding, it’s also a speedy, economical option for general-purpose agentic and tool calling use cases.

[Try it now](https://console.x.ai/team/default/chat-playground?model=grok-build-0.1&campaign=grok-build-0-1-blog)[Create API key](https://console.x.ai/team/default/api-keys?campaign=grok-build-0-1-blog)

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

`grok-build-0.1` performs best in agentic harness like [Grok Build](https://docs.x.ai/build/overview), Cursor, [Hermes Agent](https://x.ai/news/grok-hermes), [OpenClaw](https://x.ai/news/grok-openclaw), [Kilo Code](https://x.ai/news/grok-kilocode), or [OpenCode](https://x.ai/news/grok-opencode). It’s also available via [OpenRouter](https://openrouter.ai/x-ai/grok-build-0.1) and [Vercel AI Gateway](https://vercel.com/changelog/grok-build-0-1-now-available-on-vercel-ai-gateway).
