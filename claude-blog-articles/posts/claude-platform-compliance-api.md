---
title: "Audit Claude Platform activity with the Compliance API"
date: 2026-03-30
source: https://claude.com/resources/articles/claude-platform-compliance-api
crawled: 2026-11-17
---

# Audit Claude Platform activity with the Compliance API

The Compliance API gives admins programmatic access to audit logs across their Claude Platform organization.

* Category[Product updates](/resources/product-updates)
* ProductClaude Platform
* DateMarch 30, 2026
* Reading time3 min
* ShareCopy link

## Audit Claude Platform activity with the Compliance API

The Compliance API is now available on the Claude Platform, giving admins programmatic access to audit logs across their organization. Security and compliance teams can track user activity, monitor configuration changes, and integrate Claude usage data into their existing compliance infrastructure.

## Audit logging for your organization

Organizations in regulated industries—like financial services, healthcare, legal—need detailed records of who accessed what, when, and what changed. Without programmatic access to this data, compliance teams need to rely on manual exports and periodic reviews, which don't scale.

The Compliance API provides an activity feed that logs security-relevant events across your organization. Admins can fetch activity logs filtered by time range, specific users, or API keys.

The API currently tracks two categories of activity:

* **Admin and system activities:** Actions that modify access or configuration of resources, like adding a member to a workspace, creating an API key, updating account settings, or modifying entity access.
* **Resource activities:** User-driven actions that create or modify resource data, such as creating a file, downloading a file, or deleting a skill. These cover actions that may affect data or allow resources to access sensitive information, excluding direct interactions with the model.

Together, these cover user login and logout events, account setting updates, workspace changes, and other organizational audit events. The API does not log inference activities, such as user interactions with the model or model activities.

## Getting started

Contact your account team to enable the Compliance API for your organization. Once enabled, create an admin API key and use it to query the activity feed endpoint. Note that logging begins once the API is enabled—historical activities prior to that point aren't available.

Organizations that already use the Compliance API for Claude Enterprise can add their Claude API organization to the same parent organization and filter activity across both from a single feed.

Read the documentation on the [Anthropic Trust Center](https://trust.anthropic.com/resources?s=tob70gqyan60x3dwb7nkap&name=anthropic-compliance-api) to learn more.

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
