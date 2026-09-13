---
title: "Build with Jules, your asynchronous coding agent"
source: https://blog.google/innovation-and-ai/models-and-research/google-labs/jules/
site: google-blog
date: 2025-05-20
authors: Kathy Korevec
crawled: 2026-09-13
---

We introduced [Jules](http://jules.google/) last December in Google Labs as an early glimpse of what a true coding agent could become. Not a co-pilot, not a code-completion sidekick, but an autonomous agent that reads your code, understands your intent, and gets to work.

Today, Jules is entering public beta, available to *everyone*. No waitlist. Worldwide, everywhere where the [Gemini model is available](https://ai.google.dev/gemini-api/docs/available-regions).

### What is Jules?

Jules is an asynchronous, agentic coding assistant that integrates directly with your existing repositories. It clones your codebase into a secure Google Cloud virtual machine (VM), understands the full context of your project, and performs tasks such as:

- Writing tests
- Building new features
- Providing audio changelogs
- Fixing bugs
- Bumping dependency versions

Jules operates asynchronously, allowing you to focus on other tasks while it works in the background. Upon completion, it presents its plan, reasoning and a diff of the changes made. Jules is private by default, it doesn’t train on your private code, and your data stays isolated within the execution environment.

Jules updates the codebase to a new version of Node.js

We’re at a turning point: agentic development is shifting from prototype to product and quickly becoming central to how software gets built. Jules uses Gemini 2.5 Pro, giving it access to some of the most advanced coding reasoning available today. Paired with its cloud VM system, it can handle complex, multi-file changes and concurrent tasks with speed and precision.

Here's a look at what you get with Jules:

- **Works on real codebases**: Jules doesn’t need a sandbox. It takes the full context of your existing project to reason about changes intelligently.
- **Parallel execution:** Tasks run inside a cloud VM, enabling concurrent execution. It can handle multiple requests simultaneously.
- **Visible workflow:** Jules shows you its plan and reasoning before making changes.
- **GitHub integration**: Jules works where you already do, directly inside your GitHub workflow. No context-switching, no extra setup.
- **User steerability**: Modify the presented plan before, during, and after execution to maintain control over your code.
- **Audio summaries:** Jules offers an audio changelog of recent commits, turning your project history into a contextual changelog you can listen to.

![Set up your dev environment](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/set_up_environment.width-100.format-webp.webp)

Set up your dev environment

![Connect to Github and create branch](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/connect_github_and_create_branch_.width-100.format-webp.webp)

Connect to Github and create branch

![Prompt a task and approve Jules’ plan](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/approve_plan.width-100.format-webp.webp)

Prompt a task and approve Jules’ plan

![Give feedback as Jules performs tasks](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/give_feedback.width-100.format-webp.webp)

Give feedback as Jules performs tasks

![Manage all your Jules tasks from the panel](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/repoview.width-100.format-webp.webp)

Manage all your Jules tasks from the panel

During this public beta phase, access is free of charge, though usage limits do apply. Details can be found [here](https://jules-documentation.web.app/). We expect to introduce pricing after this beta as the platform matures.

[Get started with Jules](http://jules.google/) and explore the [documentation](https://jules.google/docs).
