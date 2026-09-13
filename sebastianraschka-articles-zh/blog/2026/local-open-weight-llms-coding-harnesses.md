---
title: "本地开放权重 LLM 编程执行框架实测笔记"
title_en: "Local Open-Weight LLM Coding Harness Note"
source: https://sebastianraschka.com/blog/2026/local-open-weight-llms-coding-harnesses.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 本地开放权重 LLM 编程执行框架实测笔记

> 原文：[Local Open-Weight LLM Coding Harness Note](https://sebastianraschka.com/blog/2026/local-open-weight-llms-coding-harnesses.html)

我一直在不同的执行框架（harness）（Qwen-Code、Codex、Claude Code）中试驾不同的本地开放权重 LLM。

30B 的专家混合（MoE）模型算是一个不错的甜点位，能够解决有挑战性的问题。而且它们在 Mac 或 DGX Spark 上可以达到大约 40 tok/sec，与 Pro 订阅下的 GPT 5.5 相当，完全可用于日常工作。

更有意思的还有执行框架的选择！Claude Code 的 token 用量似乎是 Codex 的 2 倍。

Gemma 4 E2B 放在这里只是作为参照，用来表明这些任务无法被更小的模型轻易解决。

更详细的实测文章现已发布：[Using Local Coding Agents](https://magazine.sebastianraschka.com/p/using-local-coding-agents)。

[![柱状图：对比 Claude Code、Codex 和 Qwen Code 在本地智能体任务中的 token 用量与任务成功率](https://sebastianraschka.com/images/blog/2026/local-open-weight-llms-coding-harnesses/hero.webp)](https://substack.com/@rasbt/note/c-283141629)

图表来自原始的 [Substack note](https://substack.com/@rasbt/note/c-283141629)，对比了相同五个本地智能体任务中的 token 用量和任务成功率。

来源：我的 [Substack note](https://substack.com/@rasbt/note/c-283141629) 的网页版，略有编辑。
