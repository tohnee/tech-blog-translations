---
title: "Using Local Coding Agents"
source: https://sebastianraschka.com/blog/2026/using-local-coding-agents.html
crawled: 2026-09-06
---

# Using Local Coding Agents

I put together a new article on setting up local coding agents with open-weight models. Everything runs 100% locally.

I thought it might be useful to put this together because many people asked me about my setup in the past, and I thought it would also motivate people to get started tinkering with local models for serious work. Things got incredibly capable this year with better LLMs and better harnesses.

So, [here’s a walkthrough of how to connect a local LLM to a local coding harness](https://magazine.sebastianraschka.com/p/using-local-coding-agents). That could be Claude Code or Codex, which you may already be familiar with.

I also included some assessment notes that are useful as a checklist to select between and consider certain LLMs over others:

1. Checking RAM usage at long contexts to see if the model is suitable for real work
2. Measuring prefill and decoding tok/sec to see whether it’s fast enough to not be annoying
3. Making sure the model has sufficient tool-calling capabilities in theory
4. Doing a security audit of the agent framework
5. Assessing whether the model can solve some more challenging tasks when used in a coding harness

Of course, there are always more specialized tools that can squeeze a bit more performance out of things, but I hope this is a good starter kit that stays flexible. That is, you can easily switch to newer models as they are released or even tap into cloud models in your familiar harness if the current ones are not sufficient for a given task.

You can find the full article here: [Using Local Coding Agents](https://magazine.sebastianraschka.com/p/using-local-coding-agents).

[![Preview image for the Using Local Coding Agents article showing local models, runtimes, and coding harnesses](https://sebastianraschka.com/images/blog/2026/using-local-coding-agents/hero.webp)](https://substack.com/@rasbt/note/c-284837359)

Preview image from the original [Substack note](https://substack.com/@rasbt/note/c-284837359), linking the [Using Local Coding Agents](https://magazine.sebastianraschka.com/p/using-local-coding-agents) article.

Source: lightly edited website version of my [Substack note](https://substack.com/@rasbt/note/c-284837359).
