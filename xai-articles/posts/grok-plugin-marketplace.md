---
title: "Grok Build Plugin Marketplace"
date: 2026-06-11
source: https://x.ai/news/grok-plugin-marketplace
crawled: 2026-09-22
---

[Back to news](/news)

Jun 11, 2026

# Grok Build Plugin Marketplace

Launching the built-in plugin marketplace for Grok Build.

---

Today we're launching the [Grok Build Plugin Marketplace](https://github.com/xai-org/plugin-marketplace) - a set of built-in plugins for [Grok Build](https://x.ai/cli).

A plugin bundles [skills](/news/grok-skills), slash commands, agents, hooks, MCP servers, and LSPs into one installable package. The marketplace is built into Grok Build, so you can browse, install, and update plugins without leaving your terminal.

## [Available at launch](#available-at-launch)

The marketplace opens with plugins from partners across the stack:

- **[MongoDB](https://www.mongodb.com/docs/mcp-server/overview/)** — Explore data, manage collections, and optimize queries.
- **[Vercel](https://github.com/vercel/vercel-plugin)** — Manage deployments, check build status, and configure domains.
- **[Sentry](https://github.com/getsentry/sentry-for-ai)** — Analyze stack traces and debug production errors.
- **[Chrome DevTools](https://github.com/ChromeDevTools/chrome-devtools-mcp)** — Control a live browser, record performance traces, and inspect network requests.
- **[Cloudflare](https://github.com/cloudflare/skills)** — Skills for Workers, Durable Objects, and more.
- **[Superpowers](https://github.com/obra/superpowers)** — Popular agent-driven workflows.

## [Install in seconds](#install-in-seconds)

Inside Grok Build, type `/marketplace` to browse the catalog and press `i` to install a plugin. Or use the CLI directly:

Copy

```
grok plugin marketplace list
grok plugin install <name> --trust
```

bash

Every remote plugin in the catalog is pinned to a specific commit SHA, and Grok Build verifies the pin at install time.

## [Publish your own](#publish-your-own)

The marketplace is an open catalog. If you've built a plugin you want to share, submit a pull request to [xai-org/plugin-marketplace](https://github.com/xai-org/plugin-marketplace).

## [Getting started](#getting-started)

New to Grok Build? Head to [x.ai/cli](https://x.ai/cli) to install it and get started.
