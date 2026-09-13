---
title: "New ways to build with Jules, our AI coding agent"
source: https://blog.google/innovation-and-ai/models-and-research/google-labs/jules-tools-jules-api/
site: google-blog
date: 2025-10-02
authors: Kathy Korevec
crawled: 2026-09-13
---

We're giving you more control and flexibility by expanding where and how you can use [Jules](https://jules.google/), Google’s AI-powered coding agent. Jules helps developers go from idea to working code faster by assisting with tasks across the software development workflow: generating code, fixing bugs, writing tests, improving performance and more. Jules is designed to act like a collaborator, working alongside you as you build your project.

Today, we’re introducing Jules Tools, our new lightweight, command-line interface, and we’re sharing an early look at the Jules API, which will allow you to integrate Jules directly into your own systems and workflows.

### Jules Tools

[Jules Tools](https://developers.googleblog.com/en/meet-jules-tools-a-command-line-companion-for-googles-async-coding-agent) is our new command-line interface, allowing you to bring Jules directly into your terminal, where you can start, stop and verify tasks right next to your own commands. It’s the simplest way to move from talking to Jules in chat to running alongside it in your actual workflow.

### Jules API

This week, we’re opening up access to the Jules API, which makes it possible to integrate Jules into your own systems and workflows. You can trigger tasks when a bug is filed in Slack, wire Jules into your CI/CD pipeline and extend to new surfaces where you want Jules to be present. The API puts Jules closer to the way you already build.

These launches are about control and flexibility, two things we’ve heard you ask for repeatedly. Jules Tools and the API give you more ways to make Jules fit into your workflow, while the recent work helps it run dependably when you need it.

## More new updates

Over the past few weeks, we’ve been heads down on improving Jules’ reliability and quality. We’ve seen improvements in reducing latency and shipped fixes for some of the most common environment setup and file system issues. These releases have laid the groundwork for what was coming next. We’ve already rolled out:

- **File selector:** Call out specific files in chat to tighten context.
- **Memory:** Jules now remembers preferences over time and automatically applies them to future tasks.
- **Environment Variables management**: A structured way to grant Jules access to environment variables during task execution.

### Get started

The future of coding with agents isn’t something abstract. It’s happening now, and it’s happening with you. Start building with directions with all these updates and more from the [Jules changelog](https://jules.google/docs/changelog) and share what you build with us on [Discord](https://discord.gg/googlelabs).
