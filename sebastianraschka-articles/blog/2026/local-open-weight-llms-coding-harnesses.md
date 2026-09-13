---
title: "Local Open-Weight LLM Coding Harness Note"
source: https://sebastianraschka.com/blog/2026/local-open-weight-llms-coding-harnesses.html
crawled: 2026-09-06
---

# Local Open-Weight LLM Coding Harness Note

I have been taking different local open-weight LLMs for a test drive in different harnesses (Qwen-Code, Codex, Claude Code).

30B Mixture-of-Experts models are kind of a nice sweet spot and can solve challenging problems. And they get roughly 40 tok/sec on a Mac or DGX Spark, which is similar to GPT 5.5 in a Pro subscription and totally usable for everyday work.

More interesting is also the harness choice! Claude Code seems to be using 2x as many tokens as Codex.

Gemma 4 E2B is here just for reference to show that the tasks can’t be trivially solved by smaller models.

The longer write-up is now available at [Using Local Coding Agents](https://magazine.sebastianraschka.com/p/using-local-coding-agents).

[![Bar chart comparing Claude Code, Codex, and Qwen Code token use and task success across local-agent tasks](https://sebastianraschka.com/images/blog/2026/local-open-weight-llms-coding-harnesses/hero.webp)](https://substack.com/@rasbt/note/c-283141629)

Chart from the original [Substack note](https://substack.com/@rasbt/note/c-283141629), comparing token use and task success across the same five local-agent tasks.

Source: lightly edited website version of my [Substack note](https://substack.com/@rasbt/note/c-283141629).
