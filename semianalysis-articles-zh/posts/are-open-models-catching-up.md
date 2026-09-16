---
title: "开源模型正在迎头赶上吗？"
title_en: "Are Open Models Catching Up?"
subtitle: "在各代前沿模型的演进阶段中对比开源与闭源模型：差距正在缩小吗？"
date: 2026-08-21
source: https://newsletter.semianalysis.com/p/are-open-models-catching-up
crawled: 2026-09-15
authors: ["Evan Cloutier", "Max Kan", "Jordan Nanos", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 开源模型正在迎头赶上吗？

> 原文：[Are Open Models Catching Up?](https://newsletter.semianalysis.com/p/are-open-models-catching-up) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**在各代前沿模型的演进阶段中对比开源与闭源模型：差距正在缩小吗？**

过去两个月是开源 AI 的爆发期。没错，2025 年 1 月确实有过「DeepSeek 时刻」，但当时并没有人真正用 R1 去完成任何有经济价值的工作。相比之下，**GLM 5.3 和 Kimi K3 这类模型，已经真正能够胜任许多曾让 Anthropic 一飞冲天、做到 $65B+ ARR 的编码与智能体任务**。与其他虚报 ARR 的公司不同，[我们给出的数字要接近现实得多。](https://semianalysis.com/tokenomics-model/)

![](https://substack-post-media.s3.amazonaws.com/public/images/071b0427-31a2-42ce-9aae-7af8499352fa_3200x1800.png)
*来源：SemiAnalysis*

对 token 消费者来说，这是一个激动人心的时代。竞争正在升温，各家不断派发用量额度重置，争夺你 token 的战场已经延伸到 OpenAI-Anthropic 双寡头之外。仅 Fireworks 一家，每天处理的 token 就超过 [40T](https://fireworks.ai/blog/series-d-announcement)——是 3 月底 OpenAI API [吞吐量](https://openai.com/index/accelerating-the-next-phase-ai/)的两倍。

然而，开源模型的成功也催生了**严重的 FUD（恐惧、不确定、怀疑）**：如果开源模型能以极低的成本维持相对于闭源前沿足够强的能力，模型层岂不是会走向商品化？这一结局对前沿实验室的利润率显然是灾难性的。关于 Anthropic 与 OpenAI 财务状况的完整细节，请参阅我们的 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)。

要预测未来开源与闭源的能力差距将如何演变，我们首先需要度量过去。想得简单一点，你可能会挑一组单一基准测试去衡量所有历史模型，但这是个错误。**每一个基准测试都是特定时代的产物。** 有人创建一个新基准测试时，目标是分辨当时模型能力之间的差异。如果他们成功了，模型厂商就会沿着这个基准一路爬分，直到它被刷到饱和。一旦饱和，所有人都不再关心这个基准，循环再次上演。

**迄今为止，LLM 的历史经历了三个时代：早期扩展（early scaling）、推理（reasoning）与智能体（agentic）**。每个时代都代表着模型实用性的一次阶跃式提升；与其试图拟合一条单一的连续趋势线，我们认为更好的做法是分别评估各个时代的模型与基准测试。

从这个视角看，**开源与闭源的差距呈周期性波动**这一点变得清晰。在每个时代开启时，某家前沿实验室完成一项有前景的研究，训练出一个令人瞩目的模型，大规模部署给自己的用户，从而一跃领先。随后，其他实验室识别出关键进展，逆向工程前沿实验室的做法，在自己的模型中复现，进而弥合差距。没有什么能永远保密——尤其是把蒸馏也算在内的时候。问题只在于需要多长时间。

为了回答这个问题，我们选取了每个时代的所有相关模型，运行一组精选基准测试，得出综合能力得分。**结果呈现出清晰的趋势：每过一个时代，开源模型追平该时代第一款闭源模型所需的时间都会减半。**

![](https://substack-post-media.s3.amazonaws.com/public/images/6f661308-2050-4dab-8a3c-16647523b34b_2048x1152.png)
*来源：SemiAnalysis*

当然，基准测试并不能反映全貌，我们会在下文列出所有相关注意事项。最后，我们会把这一分析延伸到未来，并解释为什么情况并不如你最初想的那样对前沿模型悲观。

# 我们如何度量

以下是我们为每个时代选定的模型与基准测试概览：

![](https://substack-post-media.s3.amazonaws.com/public/images/398dbca6-c628-4a13-b22d-df1362c02434_2048x1280.png)
*来源：SemiAnalysis*

在某个特定时间点挑选单一的 SOTA 闭源模型和开源模型带有主观性，但我们的选择反映了 AI 专家群体的一般共识。在存在争议的案例中——比如如今的 Fable 5 与 GPT 5.6——我们从保守出发，两款都测了。

在基准测试的选择上，我们综合了个人品味与流行程度。例如 Humanities Last Exam（HLE）虽然公认存在诸多[问题](https://www.futurehouse.org/research/hle-exam)，但它确实是推理时代最具定义性的基准测试之一，没有近似替代品。另一方面，SWE-bench Pro 同样流行、同样[有问题](https://openai.com/index/separating-signal-from-noise-coding-evaluations/)，但可以用 DeepSWE 较好地近似。

这里的多数基准分数由我们使用 [Prime Intellect](https://www.primeintellect.ai/) 的评测技术栈自行运行得出，具体是其环境中心（environments hub）以及 [Prime-RL](https://github.com/PrimeIntellect-ai/prime-rl) 中包含的评测 harness。其余分数来自我们的朋友 [Artificial Analysis](https://artificialanalysis.ai/) 与 Datacurve 的 [DeepSWE 排行榜](https://deepswe.datacurve.ai/)的运行结果。开源模型按其发布时的服役方式提供服务：当时的 vLLM 版本、当时在用的硬件、以及模型卡上的采样设置。闭源模型则针对其锁定的 API 版本运行。当我们的数字与第三方数值同处一张图表时，我们对齐了对方的规则集。

**我们要向 Prime Intellect 的 Florian Brand（[@xeophon](https://x.com/xeophon?s=20)）致以巨大感谢**，感谢他帮助我们挑选基准测试/模型、实现评测并核对正确性。

# 时代 1 | 早期扩展（2022-2024）

时间是 2023 年 6 月。全世界正在消化 ChatGPT 带来的冲击，马克·扎克伯格刚刚同意在罗马斗兽场和埃隆·马斯克干一架。但当扎克伯格还在练柔术、做 Murph 训练时，他的公司也在做自己的「训练」。FAIR 即将走出 Mistral 人才出走及其他种种风波，成功发布 Llama-2-70B——第一款接近前沿水平的开源模型。

它落后前沿多远？当时有四项基准共同定义了 SOTA：GSM8K、HumanEval、TriviaQA 和 MMLU-Pro：

![](https://substack-post-media.s3.amazonaws.com/public/images/bb674a44-63d5-4960-a9b7-4f602ab8f8b3_2048x1152.png)
*来源：SemiAnalysis*

这些基准代表了当时前沿模型的能力边界：简单的选择题、应用题，以及限定在单个函数范围内的编程题。时代真是变了！下面是 Llama-2 与 GPT-3.5 Turbo 在一场「笼中格斗」中的对比：

![](https://substack-post-media.s3.amazonaws.com/public/images/99e69460-de7f-48db-b750-b6ce87fde19b_2048x1152.png)
*来源：SemiAnalysis*

为消除基准测试难度差异的影响，我们对分数做了归一化。每个时代的最佳成绩设为 100，其他模型据此相对计分。综合得分是四项基准的等权平均：前沿的 GPT-3.5 Turbo 为 75.7，Llama-2-70B 为 39.9。差距温和，但相当可观。这一初始落后为时代余下的剧情定下主线：2023 年 12 月发布的 Mixtral-8x7B 掀起了向 GPT-4 能力冲刺的势头，结果却被 GPT-4 Turbo 和 GPT-4o 甩在身后：

![](https://substack-post-media.s3.amazonaws.com/public/images/232b9c60-4520-4ad7-b333-41398cff3f0c_2048x1152.png)
*来源：SemiAnalysis*

直到 2024 年 7 月 Llama-3.1-405B 发布，开源模型才追平 GPT-3.5 Turbo，综合得分 86。时代最后一款前沿模型 GPT-4o，则在 2024 年 12 月被 DeepSeek V3 追平能力，两者得分分别为 95.5 和 94.1。Qwen2.5-72B 以 405B 参数量的六分之一、基于 18T token 预训练，落在了 GPT-4o 触手可及的范围之内。

这是差距第一次被弥合。整个时代里，我们并没有看到前沿能力大幅超越 GPT-4，但这主要是优先级使然：Turbo 和 4o 的定位是让 GPT-4 更便宜、更快速，而不是更聪明。

与此同时，OpenAI 一直在攻关另一种类型的模型。[过程奖励论文](https://arxiv.org/abs/2305.20050)和[招入 Noam Brown](https://x.com/polynoamial/status/1676971503261454340)都指向推理，到 2024 年年中，[每家主要实验室都在发表测试时计算（test-time-compute）研究](https://arxiv.org/abs/2408.03314)。在 405B 发布七周后的 2024 年 9 月 12 日，OpenAI 推出了 o1-preview：一款点燃了创新新时代的模型。

# 时代 2 | 推理（2024-2025）

o1 重置了基准测试的选择，也重置了差距。时代 1 的那些入门级评测已经难以考验 o1 的全部能力。小学数学题被 AIME 取代。Scale AI 收集了世界上最冷僻的一批博士级选择题，并挑衅地将其命名为 Humanity's Last Exam。

![](https://substack-post-media.s3.amazonaws.com/public/images/7676e5dd-379e-49d4-ba17-25652fc3e5ad_2048x1152.png)
*来源：SemiAnalysis*

o1 的发布在科技圈的意义怎么强调都不为过。许多人认为那一天「我们确信一定能实现 AGI」。然而，与 Llama-2-70B 对阵 GPT-4 不同，时代 2 中开源与闭源的起始差距要小得多。幕后功臣？一款当时名不见经传的模型——DeepSeek R1。

![](https://substack-post-media.s3.amazonaws.com/public/images/891cbf92-d756-4015-ba25-936c5fe533e6_2048x1152.png)
*来源：SemiAnalysis*

12.1 分的差距，而上一时代开局时是 35.8 分。市场闻讯「吐了」。所幸 AI 资本开支交易迅速收复失地，而 R1 树立的「我们回来了」的开源模型声势，很快被 Meta 的 Llama-4 Maverick 扑灭。

![](https://substack-post-media.s3.amazonaws.com/public/images/700c6b14-aaea-4e05-ac7e-edb6480d5fca_2048x1152.png)
*来源：SemiAnalysis*

Gemini 2.5 Pro 和 o3 持续推进推理前沿，而 R1-0528 检查点在 2025 年 5 月以 78 分的成绩弥合了初始差距。用 8.5 个月的时间窗口追平 12.1 分的差距：

![](https://substack-post-media.s3.amazonaws.com/public/images/bd00db9e-d73b-4e72-82ac-b7eab611446d_2048x1152.png)
*来源：SemiAnalysis*

值得注意的是，到目前为止的图表中缺席者是 Anthropic。他们的模型卡和其他人一样披露这些基准成绩，但在这个时代他们从未争夺排行榜榜首。当 OpenAI 和 Google 轮流加冕时，Anthropic 正在把 Claude 打造成默认的编码智能体。这为下一个时代定下了规则：如今真正重要的基准测试，是在终端里运行的。

# 时代 3 | 智能体（2025 至今）

在 Claude Code 之前，智能体也有过高光时刻（比如 Cognition 2024 年 3 月[刷屏的 Devin 演示](https://x.com/cognition/status/1767548763134964000)），但 Anthropic 是第一个把「模型 + harness」产品做到位的——这也获得了丰厚回报。自 2025 年 5 月 Claude Code 正式发布以来，Anthropic 的 ARR 已经增加了超过 $65B。关于 Anthropic 与 OpenAI ARR 的深入预测，请参阅我们的 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)。

随着智能体而来的又是一套全新基准。花哨的数学题不再是检验模型能力的最佳方式。人们转而想知道模型写代码、做网络搜索、以及像人一样使用电脑的能力有多强。

![](https://substack-post-media.s3.amazonaws.com/public/images/e082580f-2b7d-4877-a6bd-b712eeec3e0c_2048x1280.png)
*来源：SemiAnalysis*

Terminal-Bench 2.1、BrowseComp-Plus、𝜏³-banking 和 DeepSWE 覆盖了当今智能体承担的长时程工作：软件工程、深度研究和知识工作。我们还特意挑选了设计上更新、更晚出现的基准，以限制记忆效应。

![](https://substack-post-media.s3.amazonaws.com/public/images/02ce4e10-36e6-4db4-ab09-99beac72cdff_2048x1152.png)
*来源：SemiAnalysis*

多数 AI 专家认为 Opus 4.5 是智能体时代的正式起点，因为这款模型的可靠性。有趣的是，GPT-5.2（当时的 OpenAI 旗舰）在我们的基准套件上表现更好，但这并不对应更好的用户体验。此时真正重要的是完整的智能体产品（模型 + harness），而 Anthropic 一直高度专注地迭代出一个擅长通用智能体工作的 harness。相比之下，Codex 要粗糙得多，而 OpenAI 同时还在忙着支线任务，比如[网页浏览器](https://openai.com/index/introducing-chatgpt-atlas/)。

两家前沿实验室之间的模型发布节奏也被压缩了。在整个时代 3，OpenAI 和 Anthropic 平均每 51 天发布一款模型，以此构筑起双寡头格局。相比之下，时代 1 和时代 2 的平均发布间隔分别为 213 天和 120 天，这是一次巨大的提速。

![](https://substack-post-media.s3.amazonaws.com/public/images/021545e4-9386-4738-8dff-ba1cebd218c4_3200x1800.png)
*来源：SemiAnalysis*

**然而，尽管前沿模型创造的经济价值出现了大爆炸式增长，时代 3 的差距弥合速度仍快于此前的任何一个时代。** Kimi K2.6 用 4.8 个月以 56.3 分超越 Opus 4.5，GLM-5.2 用 6 个月以 72.4 分迈过 GPT-5.2。追平时间每个时代减半的趋势惊人地一致。

![](https://substack-post-media.s3.amazonaws.com/public/images/b272b3ef-7f89-4f4a-a44d-9be5a279da5c_2048x1152.png)
*来源：SemiAnalysis*

# 展望未来

那么，这一切对闭源与开源模型的未来意味着什么？

首先，我们要承认，**基准测试并非评判一切的唯一标准**。在我们精选的综合评分上，Kimi K3 或许比 Fable 5 得分更高，但在 SemiAnalysis 的日常工作中，我们仍然更偏爱使用 Fable。部分原因在于 Anthropic 通过 Claude Code、Claude Tag 之类的东西把模型产品化做得更好，但很大程度上也是因为基准测试并不是实际工作的完美代理指标。**公开基准尤其如此——模型厂商只需创建一堆高度模仿基准任务的 RL 环境，就能轻松刷高这些分数。**

其次，你可能会争辩说，时代 3 的追平时间被人为压低了，因为 Anthropic 和 OpenAI 在安全测试上花的时间比月之暗面（Moonshot）和智谱（Zhipu）更多，但这并不是什么新现象。例如 GPT-4 在发布前 218 天就完成了训练。即便我们假设 Mythos 在 2 月中旬完成训练，距离 Fable 发布也只间隔了 114 天。

## 即将到来的时代
