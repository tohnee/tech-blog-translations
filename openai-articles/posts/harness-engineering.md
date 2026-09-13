---
title: "Lessons from harness engineering"
date: 2026-05-06
source: https://openai.com/index/harness-engineering/
crawled: 2026-09-13
category: engineering
---

When people talk about agent performance, they usually mean model capability. But anyone who has shipped an agent product knows that the software around the model — the harness — matters enormously. The harness is the collection of tools, environment scaffolding, context management, and interaction design that wraps a model and turns it into a working agent. Two identical models behind different harnesses can differ by tens of percent on real tasks.

We have spent the last year building Codex⁠(opens in a new window), our coding agent, across terminal, IDE, web, and code review surfaces. This post collects lessons from that work — the things we wish we had known when we started.

## The environment is part of the model

An agent is only as good as the environment it operates in. Early versions of our cloud sandbox gave the model a fresh checkout with no build cache, no installed dependencies, and no access to secrets — a cold start on every task. Agents wasted most of their tokens just getting to a state where they could run tests. Installing dependencies and warming caches before the agent starts increased task completion rates substantially, with zero model changes.

Invest in the environment before investing in prompting. A `make setup` target, a preinstalled toolchain, and a readable test runner output do more for agent success than most prompt engineering.

## Feedback loops beat instructions

We used to write detailed instructions telling the model how to verify its work. Now we mostly engineer the loop instead: make it cheap and fast for the agent to run the relevant test, see the failure, and fix it. A harness that surfaces compiler errors, test output, and lint results as structured tool responses lets the model self-correct. A harness where the model must guess whether its change worked produces confident, broken patches.

Concretely: return errors with file paths and line numbers, cap noisy output intelligently rather than truncating blindly, and never swallow stderr — the model often reads the traceback that a human would skim.

## Context is the scarcest resource

Model context windows are large, but effective context is much smaller: attention degrades over long ranges, and every token spent on boilerplate is a token not spent on the problem. The highest-leverage harness engineering is about curating what enters the context.

- Compress tool outputs aggressively, but preserve the errors — the last 200 lines of a failing test matter more than the first 2,000 of a passing build.
- Maintain a rolling summary of what the agent has tried and learned, written by the agent itself between steps.
- Give the agent a way to search rather than a way to read everything. Repository maps and symbol indexes let the model navigate a large codebase without ingesting it.

## Diff review is a product surface

The user-facing moment of a coding agent is the diff. Everything before it — planning, execution, self-review — exists to make that diff trustworthy. We learned to optimize the experience around reviewing changes: scope each task so the diff is comprehensible, make the agent explain its reasoning in terms of the changes it made, and support incremental follow-ups (“now also update the docs”) rather than restarting.

A related lesson: agents should be conservative by default and explicit about uncertainty. A diff that says “I could not verify this refactor preserves behavior because the tests do not cover X” is far more useful than a silent change.

## Evaluation harnesses are product code

Our internal eval harness — which runs tasks in sandboxes, scores diffs, and records traces — began as a script and became one of the most load-bearing pieces of software we maintain. Every harness change is now evaluated the same way we evaluate model changes: does it move task completion, does it change token cost, does it alter the failure distribution?

Measure harness changes separately from model changes. It is remarkably easy to attribute a gain to the model when it actually came from a change to the loop.

## What’s next

Harness engineering is still young. Most of the ideas in this post were discovered by watching agents fail, and there is much more to learn. We plan to share more as the field develops — and if you are building agents, we would love to hear what you are learning too.

### Citation

__BibTeX citation__

```
@misc{openai2026harness,
  title   = {Lessons from harness engineering},
  author  = {OpenAI},
  year    = {2026},
  url     = {https://openai.com/index/harness-engineering/}
}
```