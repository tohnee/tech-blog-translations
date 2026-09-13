---
title: "使用本地编程智能体"
title_en: "Using Local Coding Agents"
source: https://sebastianraschka.com/blog/2026/using-local-coding-agents.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 使用本地编程智能体

> 原文：[Using Local Coding Agents](https://sebastianraschka.com/blog/2026/using-local-coding-agents.html)

我整理了一篇新文章，讲如何用开放权重模型搭建本地编程智能体。所有环节 100% 本地运行。

我觉得把这些内容整理出来会很有用，因为过去很多人问过我的配置方案，而且我也希望这能激励大家开始动手，把本地模型用于真正严肃的工作。今年随着更好的 LLM 和更好的执行框架（harness）出现，本地方案的能力已经强得惊人。

所以，这里有[一篇手把手教程，讲如何把本地 LLM 接入本地编程执行框架](https://magazine.sebastianraschka.com/p/using-local-coding-agents)。它可以是 Claude Code 或 Codex——你可能已经对它们很熟悉了。

我还加入了一些评估要点，可以作为在多个 LLM 之间做出取舍时的检查清单：

1. 在长上下文下检查内存（RAM）占用，看模型是否适合真实工作
2. 测量 prefill 和解码的 tok/sec，看速度是否快到不让人心烦
3. 确认模型在理论上具备足够的工具调用能力
4. 对智能体框架做一次安全审计
5. 评估模型在编程执行框架中使用时能否解决一些更有挑战性的任务

当然，总有一些更专门的工具可以再榨出一点性能，但我希望这是一个保持灵活性的良好入门套装。也就是说，你可以随时轻松切换到更新的模型，甚至在当前模型不足以胜任某个任务时，直接在你熟悉的执行框架里接入云端模型。

完整文章在这里：[Using Local Coding Agents](https://magazine.sebastianraschka.com/p/using-local-coding-agents)。

[![Using Local Coding Agents 文章预览图：展示本地模型、运行时与编程执行框架](https://sebastianraschka.com/images/blog/2026/using-local-coding-agents/hero.webp)](https://substack.com/@rasbt/note/c-284837359)

来自原始 [Substack note](https://substack.com/@rasbt/note/c-284837359) 的预览图，链接到 [Using Local Coding Agents](https://magazine.sebastianraschka.com/p/using-local-coding-agents) 一文。

来源：我的 [Substack note](https://substack.com/@rasbt/note/c-284837359) 的网页版，略有编辑。
