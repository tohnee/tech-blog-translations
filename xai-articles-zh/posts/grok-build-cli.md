---
title: "Grok Build 早期测试版发布"
title_en: "Introducing Grok Build Early Beta"
date: 2026-05-14
source: https://x.ai/news/grok-build-cli
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok Build 早期测试版发布

> 原文：[Introducing Grok Build Early Beta](https://x.ai/news/grok-build-cli) · xAI

2026 年 5 月 14 日

现面向 SuperGrok Heavy 订阅用户开启早期测试——Grok Build 是一个可直接在终端中运行的全新编码智能体。

---

今天我们发布 Grok Build 的早期测试版（early beta），这是一个面向专业软件工程和复杂编码工作的强大编码智能体与 CLI。

首批面向 SuperGrok Heavy 订阅用户开放。通过这次早期测试，我们将根据你的反馈改进模型和产品。只需一条命令即可安装 Grok Build，并使用你的 SuperGrok Heavy 账号登录：

`curl -fsSL https://x.ai/cli/install.sh | bash`

[升级订阅](https://grok.com/supergrok?referrer=grok-build)

~/Documents/GitHub/xai

|4.2%|

◆Thought for 3.8s

❯

grok-build

Enter:run│Esc:reset│Tab:next example│Type:custom command

## [规划、审查、批准](#plan-review-approve)

对于复杂任务，可以让 Grok Build 以规划模式启动。你可以在执行开始前批准计划、对单个步骤发表意见，或者干脆整个重写。
计划一经批准，每一处改动都会以干净的 diff 呈现。

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

6. Document `-p` headless mode and ACP compatibility

73. Point users to `config.toml` for models and API keys

84. Cross-link the auth and feedback sections

#1 review diff

[turn: 21s, ↕16.8k]

❯

grok-build

Enter:run│Type:swap prompt│Esc:clear input

## [兼容你现有的一切](#works-with-what-you-already-use)

你的 AGENTS.md、插件、hooks、skills 和 MCP 服务器都开箱即用。在代码仓库里启动 Grok Build，它会立刻识别你的约定。

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

## [并行工作的子智能体](#subagents-that-work-in-parallel)

对于更大的任务，Grok Build 会把工作委派给多个并行运行的专用子智能体。Grok Build 还支持深度 worktree 集成，你可以在各自的 worktree 中启动子智能体。

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

## [为融入你的工作流而设计](#built-to-fit-your-workflow)

无头模式（`-p`）让你可以轻松地在脚本和自动化流程中运行智能体。CLI 还提供完整的 ACP 支持，用于构建你自己的机器人和智能体编排应用。

## [立即试用](#try-it-today)

这还是早期测试版，你的反馈是让它变好的最快途径。在 CLI 中输入 `/feedback`，即可将 bug、需求和意见直接发送给团队。

SuperGrok Heavy 订阅用户可以用上面的命令安装 Grok Build 并开始构建。如果你还不是 SuperGrok Heavy 用户，请到 [这里升级](https://grok.com/supergrok?referrer=grok-build)——我们期待看到你的作品。

`curl -fsSL https://x.ai/cli/install.sh | bash`

[升级订阅](https://grok.com/supergrok?referrer=grok-build)

在以下平台试用 Grok

[Web](https://grok.com)

[iOS](https://apps.apple.com/app/apple-store/id6670324846?pt=126952307&ct=x.ai%20Direct%20Link&mt=8)

[Android](https://play.google.com/store/apps/details?id=ai.x.grok&hl=en)

[X 上的 Grok](https://x.com/i/grok)

产品

[Grok](/grok)

[𝕏](https://x.com)

[Grok 企业版](/grok/business)

[Grokipedia](https://grokipedia.com)

API

[概览](/api#capabilities)

[语音 API](/api/voice)

[Imagine API](/api/imagine)

[定价](https://docs.x.ai/developers/models?cluster=us-east-1#detailed-pricing-for-all-grok-models)

[API 控制台登录](https://console.x.ai)

[文档](https://docs.x.ai)

公司

[公司介绍](/company)

[招聘](/careers)

[联系我们](/contact)

[新闻](/news)

资源

[隐私政策](/privacy-policy)

[隐私门户](/privacy-portal)

[安全](/security)

[安全中心](/safety)

[法律](/legal)

[状态](https://status.x.ai)
