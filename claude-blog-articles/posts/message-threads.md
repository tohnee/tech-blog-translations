---
title: "Make long-running agents faster with message threads"
date: 2026-11-02
source: https://claude.com/resources/articles/message-threads
crawled: 2026-11-17
---

# Make long-running agents faster with message threads

New in the Messages API, send your conversation once, and the API receives only what’s new with every turn.

* Category[Product updates](/resources/product-updates)
* ProductClaude Platform
* DateNovember 2, 2026
* Reading time3 min
* ShareCopy link

Message threads is now available in public beta on the Claude Platform. With message threads, agents no longer need to resend the full conversation history on every turn, reducing latency for long-running sessions.

### How message threads works

A coding agent might make hundreds of requests in one session, and each request resends every earlier message and tool result. Once a conversation reaches hundreds of thousands of tokens, resending all of it adds time before Claude starts responding. With message threads, agents send only what’s new since the last turn, which reduces time to first token (TTFT).

With message threads on by default for most Claude Code users, requests with 500k to 1M tokens see median TTFT drop by about 35%.

To use message threads, add the `thread` parameter to Messages API requests. The first request includes the full conversation and starts a thread. Each request after that includes only the new messages and the ID of the previous response. Between turns, we hold each thread in memory, where it’s encrypted and not written to disk. A thread expires 5 minutes after its last request and your client then resends the full conversation to start a new one. While each request is smaller with message threads, Claude still reads the full conversation on every turn, so token usage stays the same.

Message threads is best for active sessions where latency matters, including:

* **Long-running coding agents**,where each tool result or file edit adds to the conversation.
* **Computer use agents**,where screenshots stay with the thread instead of being re-uploaded on every turn.
* **Document and image-heavy workflows**, where requests are made smaller.

The more context an agent carries, the more message threads can reduce time to first token.

### Getting started

Message threads is available now in public beta on the native Claude Platform, and on Claude Platform on AWS, Claude in Microsoft Foundry, and on [Claude Models on Google Cloud (Anthropic managed)](https://claude.com/resources/articles/claude-models-on-google-cloud-anthropic-managed). Standard Claude token rates and existing rate limits apply. See the [documentation](https://platform.claude.com/docs/en/build-with-claude/message-threads) to get started.

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
