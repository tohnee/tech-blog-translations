---
title: "Compliance API coverage extends to Claude Cowork and Claude Code"
date: 2026-08-11
source: https://claude.com/resources/articles/compliance-api-cowork-and-claude-code
crawled: 2026-11-17
---

# Compliance API coverage extends to Claude Cowork and Claude Code

* Category[Product updates](/resources/product-updates)
* ProductClaude Enterprise, Claude apps, Claude Code, Claude Cowork
* DateAugust 11, 2026
* Reading time3 min
* ShareCopy link

***Update: Compliance API: Cowork (desktop, web, and mobile) and Claude Code (CLI and desktop) coverage are now generally available; Microsoft 365 add-ins (Excel, Word, PowerPoint, and Outlook) and Claude Science coverage are in beta (August 26, 2026)***

Claude's Compliance API now covers Cowork across the desktop app, web, and mobile, as well as Claude Code in the CLI and desktop app. Coverage is in beta for Claude Enterprise customers. Compliance and security teams can pull session content and metadata from both products through the same Compliance API interface they already use for Claude chats.

The new endpoints are additive: nothing changes about the data you already pull from the Compliance API today.

Security and compliance teams rely on the Compliance API to see how Claude is used across their organization — for audits and eDiscovery — without deploying separate logging infrastructure for each surface. Extending coverage to Cowork and Claude Code closes a gap: those sessions now show up alongside Claude chats.

## How it works

The new session endpoints return a consolidated, server-hosted transcript for each Cowork and Claude Code session, so prompts, responses, and tool activity come back together in a single session record.

Each session record carries two kinds of data:

* **Session content:** prompts and responses, tool calls content (web and MCP), and skills and artifacts content captured as transcript text.
* **Session metadata:** verified user ID and email address, organization ID, session and per-message IDs, and timestamps.

This beta doesn't include Claude Code on the web, Claude Code accessed through the Claude Platform, or sessions run on Amazon Bedrock, Google Cloud's Vertex AI, or Microsoft Foundry.

Organizations already exporting OpenTelemetry data can keep it running: the Compliance API can work alongside it with no infrastructure required on your side.

## Getting started

Coverage for Cowork and Claude Code is available today and included with the Compliance API using your existing Compliance Access Key – there’s no separate integration to build. If it's already enabled for your organization, query the new session endpoints directly. If not, review the Compliance API [documentation](https://platform.claude.com/docs/en/manage-claude/compliance-api) to enable it.

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
