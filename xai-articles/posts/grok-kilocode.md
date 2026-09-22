---
title: "Use Grok in Kilo Code"
date: 2026-05-27
source: https://x.ai/news/grok-kilocode
crawled: 2026-09-22
---

[Back to news](/news)

May 27, 2026

# Use Grok in Kilo Code

Use your SuperGrok or X Premium+ subscription inside Kilo Code, the open-source agentic coding platform.

---

Starting today, you can use your Grok subscription directly inside Kilo Code.

Kilo Code is the open-source agentic engineering platform for VS Code, JetBrains IDEs, and the terminal. It offers specialized modes for planning, coding, debugging, and orchestration, along with powerful tool use, browser automation, MCP extensibility, and support for 500+ models. Kilo is designed for real software engineering workflows and agentic use cases.

With your X Premium+ or SuperGrok subscription, connect your Grok account to use the latest Grok models — including Grok Build for agentic coding — inside Kilo Code with no separate API key.

### [Setup](#setup)

Kilo Code offers IDE extensions, a CLI, and a web surface. To connect your xAI account, follow the instructions below:

**VS Code:**

1. Install [Kilo Code](https://marketplace.visualstudio.com/items?itemName=kilocode.Kilo-Code) from the VS Code Marketplace.
2. Open **Settings** (gear icon) and go to the **Providers** tab.
3. Click **Show more providers**, then search for or select **xAI**.
4. Choose the **xAI Grok OAuth (SuperGrok Subscription)** sign-in option and complete the OAuth flow in your browser.

For headless or remote environments (VPS, SSH, Docker, WSL), choose **xAI Grok OAuth (Headless / Remote / VPS)** instead.

**CLI:**

bash

```
npm install -g @kilocode/cli
```

Run `kilo` in your project directory and use the `/connect` command to add xAI.

For more details, see the [Kilo Code xAI provider documentation](https://kilo.ai/docs/ai-providers/xai).

More open-source agents and integrations are coming soon.
