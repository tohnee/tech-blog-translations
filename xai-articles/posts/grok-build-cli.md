---
title: "Introducing Grok BuildEarly Beta"
date: 2026-05-14
source: https://x.ai/news/grok-build-cli
crawled: 2026-09-22
---

May 14, 2026

# Introducing Grok Build Early Beta

Now in early beta for SuperGrok Heavy subscribers — Grok Build is a new coding agent that runs right from your terminal.

---

Today we're launching an early beta of Grok Build, a powerful new coding agent and CLI for professional software engineering and complex coding work.

Available first for SuperGrok Heavy subscribers. Through this early beta, we will improve the model and product based on your feedback. Install Grok Build with a single command and sign in with your SuperGrok Heavy account:

`curl -fsSL https://x.ai/cli/install.sh | bash`

[Upgrade](https://grok.com/supergrok?referrer=grok-build)

~/Documents/GitHub/xai

|4.2%|

◆Thought for 3.8s

❯

grok-build

Enter:run│Esc:reset│Tab:next example│Type:custom command

## [Plan, review, approve](#plan-review-approve)

For complex tasks, start Grok Build in plan mode. You can approve the plan, comment on individual steps, or rewrite it entirely before execution begins.
Once a plan is approved, every change shows up as a clean diff.

~/Documents/GitHub/xai

|3.91%|

❯tighten install docs for headless mode

◆Editdocs/install.md

plan.md

1Install Docs Refresh Plan

2Quick Assessment

3• docs/install.md skips headless mode and ACP entirely, so the install path should be rewritten to cover the bootstrap, the `-p` flag, and config.toml in one pass.

4Implementation Plan

51. Replace the install snippet with the curl bootstrap

62. Document `-p` headless mode and ACP compatibility

73. Point users to `config.toml` for models and API keys

84. Cross-link the auth and feedback sections

#1 review diff

[turn: 21s, ↕16.8k]

❯

grok-build

Enter:run│Type:swap prompt│Esc:clear input

## [Works with what you already use](#works-with-what-you-already-use)

Your AGENTS.md, plugins, hooks, skills, and MCP servers all work out of the box. Start Grok Build in your repo and it picks up your conventions instantly.

~/Documents/GitHub/xai

|3.95%|

◆Thought for 9.2s

I'll search the marketplace and install the browser-review plugin.

❯install browser-review and open its skills

HooksPluginsMarketplaceSkillsMCP Servers

/browserAll ⌄

›browser-review v0.8.2(community)

[preview]

Scroll this example into view to watch the plugin install flow.

[turn: 31s, ↕39.1k]

❯

grok-build

Click:take over│Enter:run│Tab:switch tabs│Esc:clear input

## [Subagents that work in parallel](#subagents-that-work-in-parallel)

For larger tasks, Grok Build delegates work to specialized subagents that run in parallel. Grok Build also supports deep worktree integrations, and you can launch subagents in their own worktrees.

~/Documents/GitHub/xai

|4.32%|

⠋explore

Explore checkout flowexplore · grok-build

⠋explore

Explore infra and CIexplore · grok-build

⠋explore

Explore shared Go librariesexplore · grok-build

⠋explore

Explore order servicesexplore · grok-build

⠋explore

Explore fulfillment jobsexplore · grok-build

⠋explore

Explore pricing engineexplore · grok-build

❯find the source of the p99 latency regression

|Diff recent deploysexplore · grok-build

[running]

|Rank slowest endpointsexplore · grok-build

[running]

|Pull slow query plansgeneral · grok-build

[running]

Splitting deploys, slow endpoints, DB plans, and cache hit rates into parallel digs.

[turn: 54s, ↕39.8k]

[turn: 54s, ↕39.8k]

❯

grok-build

Enter:launch│Click:pin agent│Type:change task│Esc:clear input

## [Built to fit your workflow](#built-to-fit-your-workflow)

Headless mode (`-p`) allows easily running agents inside scripts and automations. The CLI also provides full ACP support to build your own  bots and agent orchestration apps.

## [Try it today](#try-it-today)

This is an early beta, and your feedback is the fastest way to make it better. Type `/feedback` in the CLI to send bugs, requests, and reactions straight to the team.

SuperGrok Heavy subscribers can install Grok Build with the command above and start building. If you're not on SuperGrok Heavy yet, [upgrade here](https://grok.com/supergrok?referrer=grok-build) — we're excited to see what you create.

`curl -fsSL https://x.ai/cli/install.sh | bash`

[Upgrade](https://grok.com/supergrok?referrer=grok-build)

Try Grok On

[Web](https://grok.com)

[iOS](https://apps.apple.com/app/apple-store/id6670324846?pt=126952307&ct=x.ai%20Direct%20Link&mt=8)

[Android](https://play.google.com/store/apps/details?id=ai.x.grok&hl=en)

[Grok on X](https://x.com/i/grok)

Products

[Grok](/grok)

[𝕏](https://x.com)

[Grok Enterprise](/grok/business)

[Grokipedia](https://grokipedia.com)

API

[Overview](/api#capabilities)

[Voice API](/api/voice)

[Imagine API](/api/imagine)

[Pricing](https://docs.x.ai/developers/models?cluster=us-east-1#detailed-pricing-for-all-grok-models)

[API Console Login](https://console.x.ai)

[Documentation](https://docs.x.ai)

Company

[Company](/company)

[Careers](/careers)

[Contact](/contact)

[News](/news)

Resources

[Privacy policy](/privacy-policy)

[Privacy portal](/privacy-portal)

[Security](/security)

[Safety](/safety)

[Legal](/legal)

[Status](https://status.x.ai)
