---
title: "Use, build, and optimize a single agent system across five assignments"
source: https://cs2680.seas.harvard.edu/assignments/index.html
crawled: 2026-11-16
---

# Use, build, and optimize a single agent system across five assignments

> 原文：[Use, build, and optimize a single agent system across five assignments](https://cs2680.seas.harvard.edu/assignments/index.html) · Harvard CS2680

CS2680 Modern AI Systems: Agents and System Optimizations

Assignments

# Use, build, and optimize a single agent system across five assignments

The assignments are not five unrelated exercises. They are one system that you progressively take apart and take control of.
You will first use an existing coding agent to build an agent application, then replace the agent runtime with your own loop
and build the evaluation set the rest of the sequence is graded on, then optimize everything around a black-box model API,
then replace that API with a model you serve yourself, and finally optimize the entire agent stack.

Assignments 1, 2, and 5 are worth 10% each. Assignments 3 and 4 are worth 20% each.
Together, the assignments account for 70% of the course grade. There is no exam.
The remaining major build is the [final project](../project.html) (20%), where you choose the problem yourself.

Assignments 1, 2 and 4 include a writeup, committed to the repository alongside the code. Assignments 3 and 5 each include a [published blog post](https://blog.cs2680.com/publish/). **All five are individual.** Estimated effort runs 4–6 hours for Assignment 1, 10–12 for Assignment 2, 10–15 for Assignment 3, 10–14 for Assignment 4, and 12–18 for Assignment 5.

All five assignments submit code through one **private GitHub repository**. Create it once, and keep each assignment's code, write-up files, benchmark outputs, and session archives under `assignmentN/`, where `N` is the assignment number (`assignment1/` through `assignment5/`). Keep the repository private, and add the instructor and the four TFs as collaborators so they can access it: [`1a1a11a`](https://github.com/1a1a11a), [`LauYeeYu`](https://github.com/LauYeeYu), [`SeverinaZheng`](https://github.com/SeverinaZheng), [`G6KlayWang`](https://github.com/G6KlayWang), and [`AdvaithRavishankar`](https://github.com/AdvaithRavishankar).

  

[Assignment 1 · out Wed Sep 2 · due Sun Sep 20 · 10%

Mads-Lens1: Watch the agent work

Start as an agent user. Use Claude Code to build a web UI for Claude Code itself, a browser front end that drives a real agent session: submit a prompt, watch the trajectory stream live (every tool call, with its input and result), see it branch into a tree when the agent spawns subagents, see when a run fails, continue the session, and see what each run cost. Serve it on your own machine (a public CloudLab or AWS deployment is optional), and write up what you learned. The assignment is deliberately small, and it is the one assignment nothing later in the course is measured against.](assignment1.html)
[Assignment 2 · out Mon Sep 21 · due Sun Oct 4 · 10%

Mads-Loop: Build the loop

Build the loop yourself around a model API from provided starter code: tool calling with machine-readable schemas, context management, retries, termination, and graceful failure under malformed output and broken tools. Evaluate on a provided benchmark, find whether the agent can help with your own tasks, and understand where the agent limit is. Hidden tests probe the runtime, not the model.](assignment2.html)
[Assignment 3 · out Mon Oct 5 · due Tue Oct 20 · 20%

Mads-Opt: Make every token count

The model is still a black-box API, so optimize everything around it. Reduce unnecessary tokens and calls, choose cheaper models where they are sufficient, overlap tool execution, compress or restructure context, and redesign the control flow. Hold task success fixed while driving cost and latency down.](assignment3.html)
[Assignment 4 · out Wed Oct 21 · due Tue Nov 10 · 20%

Mads-Serve: Own the serving engine

Remove the frontier API. Serve the model yourself on one RTX PRO 4500 (32 GB), run your Assignment 3 agent against it, and find what limits the run. Then make it faster by changing the serving engine or the agent, with the model held fixed. The leaderboard ranks submissions on tasks solved and end-to-end time.](assignment4.html)
[Assignment 5 · out Wed Nov 11 · due Tue Nov 24 · 10%

Mads-Stack: Optimize the full stack

Builds on Assignment 4. Make your own agent strong: fix what held it back and take good ideas from other agent designs. You may also change the model and the serving engine on one RTX PRO 4500 (32 GB). The leaderboard runs Terminal-Bench 2.0, and a submission that meets its baseline gets full leaderboard points. Your rank on Assignment 4's 26 tasks earns a bonus. You also publish a blog post on what you learned from Assignments 2-5.](assignment5.html)

1 “Mads” abbreviates Modern Agent Design and Systems, the arc of this course, and nods to [MaDSys](https://madsys.seas.harvard.edu/), Harvard’s Measurement and Design of Systems research group, which teaches and supports it.

---

# Related

* [Computing setup](../computing/index.html). Claude Code, the model API, the HPC (GPU nodes), and AWS.
* [Late days](../policy.html#late-days). Four for the semester, usable across all assignments.
* [AI use policy](../policy.html#ai-policy). AI use is encouraged and must be disclosed.
