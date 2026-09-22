---
title: "Introducing /goal"
date: 2026-06-22
source: https://x.ai/news/introducing-goal
crawled: 2026-09-22
---

[Back to news](/news)

Jun 22, 2026

# Introducing /goal

Use /goal for long-running autonomous task execution in Grok Build.

---

Today we're introducing `/goal` in Grok Build. This new mode yields long-running, autonomous execution, helping you hand off larger implementation tasks to the agent.

Available now in Grok Build. Install the CLI with a single command and sign in with your account:

`$ curl -fsSL https://x.ai/cli/install.sh | bash`

[Upgrade](https://grok.com/supergrok?referrer=introducing-goal)

Introducing /goal

Most coding sessions require back-and-forth execution and verification. With `/goal`, the agent continues until a task is completed and verified, whether that means reviewing code, inspecting webpages, or executing scripts.

## [Set a goal in one line](#set-a-goal-in-one-line)

Give `/goal` an objective and Grok Build takes it from there:

Copy

```
/goal Migrate the auth module to the new API
```

bash

It plans an approach, breaks the work into a progress checklist, and starts executing. You can keep sharing additional instructions with the agent as it works.

The new mode offers additional commands for monitoring and steering long-running tasks:

Copy

```
/goal status     # see the live progress panel
/goal pause      # stop work, keep the goal
/goal resume     # pick back up
/goal clear      # drop the goal entirely
```

bash

When the goal is finished, the panel flips to **Complete** with every checklist item checked.

## [Getting started](#getting-started)

Install Grok Build with the command above, then invoke `/goal` to hand off your first long-running task.
