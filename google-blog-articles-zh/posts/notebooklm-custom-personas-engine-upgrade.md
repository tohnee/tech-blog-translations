---
title: "NotebookLM 聊天：强大而目标聚焦的 AI 研究伙伴"
title_en: "Chat in NotebookLM: A powerful, goal-focused AI research partner"
source: https://blog.google/innovation-and-ai/models-and-research/google-labs/notebooklm-custom-personas-engine-upgrade/
site: google-blog
date: 2025-10-29
crawled: 2026-09-13
translated: 2026-09-13
---

# NotebookLM 聊天：强大而目标聚焦的 AI 研究伙伴

> 原文：[Chat in NotebookLM: A powerful, goal-focused AI research partner](https://blog.google/innovation-and-ai/models-and-research/google-labs/notebooklm-custom-personas-engine-upgrade/) · Google

我们正在对 NotebookLM 推送一系列更新，让它从根本上更聪明、更强大。首先，一组后端改进大幅提升了性能与质量；其次，我们扩展了为笔记本设定目标的能力，让每个笔记本都能适应你的需求。以下是全部新特性。

## 获得更深入的洞见与更清晰的答案

我们对 NotebookLM 聊天的工作机制进行了根本性升级。这些由最新 Gemini 模型驱动的后端改进协同作用，提升了性能、质量与上下文理解能力。自开始测试这些改进以来，我们看到在处理大量来源的回复上，用户满意度提升了 50%。以下是我们改进的所有内容：

- **更流畅自然的对话。** 我们大幅扩展了 NotebookLM 的处理能力、对话上下文与历史记录。从今天起，我们将在所有方案中为 NotebookLM 聊天启用 Gemini 完整的 100 万 token 上下文窗口，显著提升分析大型文档合集时的性能。此外，我们还将多轮对话容量提升了六倍以上，让你在长时间交互中获得更连贯、更相关的结果。

![示意图，展示 RAG 模型的工作流程：一个原始提问（"什么是增长的主要战略驱动力及其财务影响？"）进入 NotebookLM 检索与排序过程（中间问题），最终生成 NotebookLM 输出（详细回答）。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/In-line_1920x1080_RAG.width-1200.format-webp.webp)

- **更深入的洞见。** 我们改进了 NotebookLM 在你的资料来源中查找信息的方式。为了帮助你发现新的关联，它现在会自动从多个角度探索你的来源，超越你的初始提示词，将发现综合成一个更细致入微的回答。这对于超大型笔记本尤其重要——在这些场景下，精心的上下文工程对于基于来源中最相关的信息、给出高质量且值得信赖的答案至关重要。
- **保存且安全的对话历史。** 为了支持长期项目，你的对话现在会自动保存。你可以关闭会话，稍后继续，而不会丢失对话历史。你可以随时删除聊天记录；在共享笔记本中，你的聊天内容仅你自己可见。该功能将在下周开始向用户推送。

![配置聊天（Configure Chat）对话框，选择"自定义（Custom）"为笔记本定义对话目标、风格或角色。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Opt1.width-1200.format-webp.webp)

## 用目标为你的聊天赋予个性化

现已面向所有用户开放：你可以自定义聊天采用特定的目标、语气或角色——从分析文献的博士生，到探索创意的讲故事者，皆可设定。开始使用时，只需点击聊天中的配置图标。

然后，写下你希望聊天如何表现、你想达成的目标。以下是一些可以尝试的示例：

- **把我当作博士生对待：** 你是我的研究导师。请严格挑战我的每一个假设。提出追问式的问题，指出逻辑谬误，迫使我从头开始为我的工作辩护。
- **扮演首席营销策略师：** 你的回答必须是一份即刻可执行的行动计划。保持分析性、直接了当，只聚焦于快速实现目标所需的具体策略与关键路径步骤。
- **从三个不同视角分析所提供的材料：** 作为关注证据与逻辑一致性的严谨学者；作为寻找非显而易见的关联与创新应用的创意策略师；以及作为积极寻找结论中的缺口、缺陷与潜在问题的怀疑派审稿人。
- **扮演一场文字模拟游戏的主持人（Game Master）。** 呈现一个带有具体目标和步骤上限（例如 10 步）的高风险场景。所有选择由我来做。用贴近场景的真实细节生动地叙述每个结果。

通过整合我们最新的模型改进，我们正在交付比以往更精准、更有洞见、更贴合上下文的回答。随着每位用户都能为对话设定目标，NotebookLM 现在能够更好地适应你的具体项目。我们希望这些更新能为你的工作解锁全新的生产力与创造力。
