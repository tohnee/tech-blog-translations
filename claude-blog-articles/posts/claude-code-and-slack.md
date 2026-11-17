---
title: "Claude Code and Slack"
date: 2025-12-08
source: https://claude.com/resources/articles/claude-code-and-slack
crawled: 2026-11-17
---

# Claude Code and Slack

* Category[Product updates](/resources/product-updates)
* ProductClaude Code
* DateDecember 8, 2025
* Reading time3 min
* ShareCopy link

Today, we're introducing the ability to delegate tasks to Claude Code directly from Slack. Now in beta as a research preview, Claude makes it easy to move context from Slack conversations to coding sessions.

## **From discussion to implementation**

The critical context around engineering work often lives in Slack, including bug reports, feature requests, and engineering discussion. When a bug report appears or a teammate needs a code fix, you can now tag Claude in Slack to automatically spin up a Claude Code session using the surrounding context. Use it for:

* **Bug investigation and fixes**: Ask Claude to investigate and fix bugs as soon as they’re reported.
* **Quick code reviews and modifications**: Have Claude implement small features or refactor code based on team feedback.
* **Collaborative debugging**: When team discussion provides crucial context—error reproductions or user reports—Claude can use that information to inform its debugging approach.

## **Route tasks to Claude Code automatically**

This functionality expands on our existing [Claude app for Slack](https://claude.com/resources/articles/claude-and-slack), allowing Claude to relay tasks back to Claude Code on the web. When you mention @Claude in Slack, Claude reviews your message to determine if it’s a coding task. If it is, a new Claude Code session will automatically be created. You can also manually tell Claude to handle requests as coding tasks.

Claude gathers context from recent channel and thread messages in Slack to feed into the Claude Code session. It will use this context to automatically choose which repository to run the task on based on the repositories you’ve authenticated to Claude Code on the web.

As the Claude Code session progresses, Claude posts status updates back to your Slack thread. Once complete, you'll find a link to the full session where you can review changes, and a direct link to open a pull request.

## **Getting started**

To get started, ensure the Claude app is installed in your Slack workspace via the [Slack App Marketplace](https://slack.com/marketplace/A08SF47R6P4). Once installed, authenticate with your Claude account and start mentioning @Claude for coding tasks. You’ll need access to [Claude Code on the web](https://claude.com/resources/articles/claude-code-on-the-web) for Claude to route coding tasks.

[Explore documentation](https://code.claude.com/docs/en/slack) to learn more.

‍

## Related articles

Explore more product news and best practices for teams building with Claude.

[ArticleNov 12, 2026

### Operate Claude Managed Agents inside your security perimeter

Introducing self-hosted Claude Managed Agents. Now you can run agents in your own environment, whether that’s in your own cloud or on-premise. You host the agents, credentials, and session history, and choose where requests to Claude are sent.

Claude PlatformClaude Managed Agents](/resources/articles/self-hosted-claude-managed-agents)[ArticleNov 12, 2026

### Introducing Claude for Manufacturing

A new plugin with 17 skills and four connectors helps manufacturers draft quotes, quality reports, and supplier requests from the systems they already run.](/resources/articles/claude-for-manufacturing)[ArticleNov 12, 2026

### Introducing Claude Meetings

Add Claude to your video call and get the work started while you talk](/resources/articles/claude-meetings)[ArticleNov 10, 2026

### Your apps can now open in Claude, and Claude can work in them

Our partners can now embed their apps directly in Claude, so you and Claude can work in the same tool, on the same screen, without switching tabs.

Claude appsMCP](/resources/articles/interactive-connectors-full-tool)
