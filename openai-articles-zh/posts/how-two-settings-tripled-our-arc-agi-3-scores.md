---
title: "开启两个设置，如何让我们的 ARC-AGI-3 基准得分提升至三倍"
title_en: "How enabling two settings tripled our scores on the ARC-AGI-3 benchmark"
source: https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/
crawled: 2026-09-13
category: research
translated: 2026-09-13
---

# 开启两个设置，如何让我们的 ARC-AGI-3 基准得分提升至三倍

> 原文：[How enabling two settings tripled our scores on the ARC-AGI-3 benchmark](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/) · OpenAI 博客

*GPT‑5.6 Sol 尝试解出 ARC-AGI-3 基准中谜题的加速视频：左侧为官方执行框架（harness），右侧为我们的 Responses API 执行框架——后者保留推理并启用压缩（compaction）。在[这款游戏](https://arcprize.org/tasks/cd82)的排行榜上，没有任何前沿模型能通过第一关之后的任何关卡。而在我们的执行框架下，GPT‑5.6 Sol 通过了全部六关。*

当我们第一次看到 GPT‑5.6 Sol 在 [ARC-AGI-3](https://arcprize.org/arc-agi/3) 基准测试上的低分时，我们感到十分困惑。

GPT‑5.6 Sol 已经解决了[圈双覆盖猜想](https://cdn.openai.com/pdf/04d1d1e4-bc75-476a-97cf-49055cd98d31/cdc_proof.pdf)这样的数学领域长期悬而未决的难题，并在《Pokémon FireRed》（宝可梦 火红）等游戏中获胜。但在 ARC-AGI-3——一个由 2D 益智游戏构成的基准测试上，GPT‑5.6 Sol 仅得到 7.8%，而 GPT‑5.5 几乎完全玩不动这些游戏，得分只有可怜的 0.4%。

2D 益智游戏对我们的模型来说格外困难吗？还是另有原因？

基准测试很少单独衡量 AI 模型本身，它们同时也在衡量一些不那么显眼的选择：API 设置、执行框架设计与提示词。就 ARC-AGI-3 而言，我们发现，开启我们在 ChatGPT 与 Codex 中使用的两个 API 设置——保留推理（retained reasoning）与压缩（compaction）——能让公开任务集上的得分提升至三倍，同时把输出 token 数量减少为原来的 1/6。

*在官方执行框架下，GPT‑5.6 Sol 在 ARC-AGI-3 公开集上得分为 13.3%；启用保留推理与压缩后，得分为 38.3%。分数衡量的是相对人类动作效率（Relative Human Action Efficiency，[RHAE](https://docs.arcprize.org/methodology)）——一种将模型表现与人类基线进行比较的指标。基于[官方游戏日志](https://huggingface.co/datasets/magic-sword/arc_agi_3_public_demo_human_testing)，我们估计人类测试者的平均得分为 48%。模型不会被告知自己的计分方式，且全程无法看到自己的分数——每次动作只会返回每一帧的文本表示以及当前所处的关卡。*

## ARC-AGI-3

ARC-AGI-3 是一个旨在衡量 AI 智能体学习与推理能力的基准测试。智能体需要探索陌生的 2D 游戏，在没有明确说明的情况下推断游戏如何运作。你可以在 [arcprize.org/tasks](https://arcprize.org/tasks) 上试玩 25 个演示游戏。

ARC-AGI-3 有意采用一个通用的执行框架，不提供工具或特殊功能。ARC 的考量是：简单的执行框架能让模型的短板更加显眼，也让模型之间的比较更加公平。相比之下，商业开发者则会针对每个模型的特性与脾气优化执行框架。

在游戏方面，GPT‑5.6 Sol 曾以纯视觉执行框架通关《Pokémon FireRed》（由 [GPT_Plays_Pokemon](https://www.twitch.tv/gpt_plays_pokemon) 直播）、借助 Codex 计算机使用通关《Slay the Spire》（杀戮尖塔，由 [EpochAI](https://www.twitch.tv/epochaiplays) 直播），并通关了《Baba Is You》的前几关（由 [Piotr Migdał & Piotr Grabowski](https://quesma.com/blog/baba-is-bench/) 分享）。ARC-AGI-3 究竟有何不同？

*Ethan Mollick [展示](https://x.com/emollick/status/2075950897029374334)了 GPT‑5.6 Sol 在 Codex 中通关《Slay the Spire 2》随机每日挑战的画面，该游戏发布于 GPT‑5.6 Sol 的知识截止日期之后。*

受 [ARC 对 GPT‑5.5 短板的分析](https://arcprize.org/blog/arc-agi-3-gpt-5-5-opus-4-7-analysis)启发，我们检查了 GPT‑5.6 Sol 的一些尝试。与 ARC 一样，我们看到模型的表现并不怎么聪明：它在每个动作上停留很久，难以取得进展。

但随着我们深入调查，我们发现模型的大部分困惑并非源于模型本身，而是由执行框架中的设置所致。

首先，我们注意到每次游戏动作之后，所有私有推理都会被丢弃。这意味着每做一个动作，GPT‑5.6 Sol 都要重新摸索这个游戏，无法记住自己过去的思考。模型仍能看到过去动作的记录及简短的附带说明，却看不到导向这些动作的计划、洞见或想法。

其次，我们发现该执行框架使用了滚动截断窗口，随着历史增长，较早的动作会变得不可见。于是，GPT‑5.6 Sol 不仅记不住自己过去的思考，连过去的动作也在逐渐遗忘。

执行框架的这两个特性——丢弃推理与滚动截断——合在一起解释了 GPT‑5.6 Sol 为何难以随时间学习。

## 智能体在记得自己做过什么时表现最好

我们的模型被训练为在输出回复或工具调用之前，先以私有推理消息进行思考。这些私有思考消息会作为对话历史的一部分被保留。如果对话变得过长，我们会对其进行摘要并继续。

这既是我们的模型的训练方式，也是它们在 ChatGPT 与 Codex 中的部署方式。为了更好地贴合我们的生产环境设置，我们用 [Responses API](https://developers.openai.com/blog/responses-api) 实现了 ARC-AGI-3 执行框架。我们的 API 让上下文管理变得简单：对 GPT‑5.6 而言，传入上一次响应的 ID 即可自动在工具调用与多轮对话之间保留推理。

保留推理之后，我们注意到两个显著变化。第一，GPT‑5.6 Sol 在每个动作前的思考时间变短了，因为它不再需要每轮都从零开始解读游戏。第二，当它能够记住自己过去的想法时，GPT‑5.6 Sol 在随时间学习与采用连贯策略方面表现得好了很多。

下一个改进来自用 Responses API 中的另一项设置[压缩（compaction）](https://developers.openai.com/api/docs/guides/compaction)替换滚动截断。

ARC-AGI-3 执行框架通过滚动截断来应对上下文限制：当对话上下文超过 175,000 字符时，最老的消息就会被丢弃。

滚动截断有两个缺点。第一，模型会丢失较早的观察与动作。第二，在任务的大部分时间里，模型都在接近满载的上下文窗口下运行，这可能会轻微损害性能。

当我们在 ARC-AGI-3 上启用压缩后，GPT‑5.6 Sol 在更长程的运行中能更好地保留它对每个游戏所学到的内容，并以更少的输出 token 取得了更高的分数。

为了说明保留推理与启用压缩的效果，下面这段动画展示了 GPT‑5.6 Sol 在两种执行框架下解一系列 ARC-AGI-3 谜题时，其 175K 上下文窗口的使用情况。

*中间两列展示了各执行框架对模型上下文窗口的不同使用方式。由于对自己过去的记忆更好，GPT‑5.6 Sol 每个动作的思考更少、推进快得多。注：我们的实现使用 175,000 token 而非字符作为上限，但两者最终相当接近，因为绝大多数文本是动作网格，我们的分词器会以 1:1 的比例对其进行分词。*

保留推理与压缩相结合，使 GPT‑5.6 Sol（max）以大约 1/6 的输出 token 取得约 3 倍的得分。

## 结论与建议

我们希望这些实验能提醒大家：评测（evals）很少单独衡量模型——它们衡量的还有一整束不那么显眼的选择：API 设置、执行框架设计与提示词。这已经不是我们第一次在公开基准上惊讶于低分，然后才发现评测运行器使用的是会丢弃推理消息的通用执行框架。

如果你是希望最大化性能的 API 开发者，我们建议使用与我们自己产品中部署相同的设置：

- 使用我们的 Responses API，而非旧版 Chat Completions API
- 保留推理
- 使用压缩

如果你正在比较不同模型，我们建议依赖使用上述设置的评测，它们最贴近 ChatGPT 与 Codex 中的真实使用方式。

我们感谢 ARC 多年来在 AGI 评测上富有创造性的工作，也感谢他们的分析促使我们对此进行更深入的审视。

如果你想与前沿模型一较高下，可以在 [arcprize.org/tasks](https://arcprize.org/tasks) 上亲自试试这些公开游戏。
