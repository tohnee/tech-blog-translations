---
title: "DeepSeek 研究简报：>128 天之后"
title_en: "DeepSeek Debrief: >128 Days Later"
subtitle: "流量与用户僵尸化、GPU 充裕的西方新兴 GPU 云、token 经济学（Tokenomics）决定竞争格局"
date: 2025-07-03
source: https://newsletter.semianalysis.com/p/deepseek-debrief-128-days-later
crawled: 2026-09-15
authors: ["Wei Zhou", "AJ", "Dylan Patel"]
tags: ["LLMs", "Tokenomics", "Inference"]
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# DeepSeek 研究简报：>128 天之后

> 原文：[DeepSeek Debrief: >128 Days Later](https://newsletter.semianalysis.com/p/deepseek-debrief-128-days-later) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**流量与用户僵尸化、GPU 充裕的西方新兴 GPU 云、token 经济学（Tokenomics）决定竞争格局**

SemiAnalysis 正在纽约为 Core Research（我们面向金融行业的世界级研究产品）招聘一名分析师。[请在此申请](https://app.dover.com/apply/SemiAnalysis/6ec0e8df-3da0-469c-9422-0c8d5dd624a7/?rs=76643084)

中国大模型 DeepSeek R1 的发布震动股市与西方 AI 世界，至今已过去 150 多天。R1 是首个公开发布、比肩 OpenAI 推理行为的模型。然而，这些成绩很大程度上被一种担忧掩盖：鉴于[极低的定价](https://api-docs.deepseek.com/quick_start/pricing)——$0.55 输入/$2.19 输出，输出 token 定价比当时的 SOTA 模型 o1 低 90% 以上——市场担心 DeepSeek（以及中国）会让 AI 模型商品化。此后推理模型价格已显著下探，OpenAI 最近也将旗舰模型价格下调了 80%。

![](https://substack-post-media.s3.amazonaws.com/public/images/9908f718-4a2e-4bcf-bf37-d3a068f0ccbc_1157x623.png)
*来源：SemiAnalysis，各公司价格*

R1 在发布后获得了一次更新，DeepSeek 在发布后持续扩大 RL 规模。这使模型在多个领域持续进步，尤其是编程。这种持续的开发与改进，是我们此前介绍过的新范式的标志。

今天我们来审视 DeepSeek 对 AI 模型竞赛的影响以及 AI 市场份额现状。

### 先暴涨……后退潮？

发布后，DeepSeek 消费级应用流量激增，市场份额急剧上升。由于中国的使用情况缺乏有效追踪、且西方实验室被挡在中国市场之外，下图数字低估了 DeepSeek 的总触达。然而，这一爆发式增长未能跟上其他 AI 应用的步伐，DeepSeek 的市场份额此后回落。

![](https://substack-post-media.s3.amazonaws.com/public/images/347d92fd-80bf-460c-9e72-698e245a1606_1230x736.png)
*来源：SemiAnalysis，SensorTower*

网页端流量的数据更为黯淡：以绝对值计，DeepSeek 流量自发布以来不增反降。同一时期，其他头部 AI 模型厂商的用户增长都相当可观。

![](https://substack-post-media.s3.amazonaws.com/public/images/9946944b-b37c-4bc7-b255-afe3822a29f0_1656x798.png)
*来源：SemiAnalysis，SimilarWeb*

DeepSeek 自营模型用户动能疲软，与第三方托管的 DeepSeek 实例形成鲜明反差。R1 和 V3 在第三方托管平台上的总用量持续快速增长，自 R1 首发以来已增长近 20 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/ef102cb8-67dc-4bb1-8ca3-ce6cc59620c1_1099x598.png)
*来源：SemiAnalysis，OpenRouter*

进一步拆解数据，将 DeepSeek 的 token 中由其自行托管的部分单独分离，可以看到 DeepSeek 自营部分占总 token 的份额逐月下滑。

![](https://substack-post-media.s3.amazonaws.com/public/images/78132000-3afb-4a11-800e-3337f4a82c09_1044x589.png)
*来源：SemiAnalysis，OpenRouter*

那么，为什么在 DeepSeek 模型人气走高、价格看似极其便宜的情况下，用户却在远离 DeepSeek 自家的网页应用与 API 服务，转向其他开源服务商？

答案在于 token 经济学（tokenomics），以及模型服务各项 KPI 之间的大量权衡。这些权衡意味着，模型的每 token 价格是这些 KPI 决策的输出（OUTPUT）结果，可依据模型提供商的硬件与模型配置进行调节。

### Tokenomics 基础

token 是 AI 模型的基本构件。AI 模型通过阅读 token 形式的互联网来学习，并以文本、音频、图像或动作 token 的形式产出结果。token 只是被大语言模型用来计数和处理的小块文本（如 "fan"、"tas"、"tic"），而非完整的单词或字母。

当 Jensen（黄仁勋）谈论数据中心变成 AI 工厂时，这些工厂的输入与输出就是 token。与实体工厂一样，AI 工厂靠 P x Q 的等式赚钱：P 是每 token 价格，Q 是输入与输出 token 的数量。

与普通工厂不同的是，token 价格是模型提供商可以基于模型其他属性*求解*的变量。我们列出关键 KPI 如下：

1. **延迟或首 token 时间（Time-to-First-Token）**：模型生成一个 token 所需的时间。也称「首 token 时间」，约等于模型完成预填充阶段（即将输入 token 编码进 KV 缓存）并开始产出解码阶段第一个 token 所需的时间。

2. **交互性（Interactivity）**：每个 token 产出的速度，常以每用户每秒 token 数衡量。一些提供商也使用交互性的倒数——每个输出 token 之间的平均时间（每输出 token 时间，TPOT）。人类阅读速度约为每秒 3-5 个词，但大多数模型提供商把输出速度定在约 20-60 token/秒。

3. **上下文窗口**：在较早的 token 被逐出、模型「忘记」对话较早内容之前，模型「短期记忆」中能容纳的 token 数量。不同用例需要不同的上下文窗口。大型文档与代码库分析受益于更大的上下文窗口，使模型能够对数据连贯推理。

对任一给定模型，都可以通过调节这 3 项 KPI 得到几乎任意的每 token 价格。因此，单纯按每百万 token 价格（$/Mtok）来讨论 token 并不总是有意义或实际，因为这忽略了负载的性质和 token 用户的需求。

### DeepSeek 的权衡

现在来看 DeepSeek 服务其 R1 模型的 token 经济学，理解为什么他们会在自家模型上持续丢失市场份额。

![](https://substack-post-media.s3.amazonaws.com/public/images/bb15c40e-0472-44f1-8759-371f04698860_1385x809.png)
*来源：https://openrouter.ai/，2025 年 5 月访问。混合 $/Mtok 按 3:1 输入:输出比计算*

将延迟与价格绘图对比，可以看到 DeepSeek 自家服务在其延迟档位上已不再是最便宜的选择。事实上，DeepSeek 能够把产品定得如此便宜的一个重要原因，是迫使用户等待数秒才收到模型的首个 token。相比之下，一些其他服务商以相同价格提供服务，但延迟要短得多。token 消费者只需付 $2-4，就可在 Parasail 或 Friendli 等服务商处获得几乎为零的延迟。Microsoft Azure 的价格比 DeepSeek 高 2.5 倍，但延迟少 25 秒。自我们拉取这份数据以来，DeepSeek 的处境进一步严峻：几乎所有 R1 0528 实例现在都以[低于 5 秒的延迟](https://openrouter.ai/deepseek/deepseek-r1-0528)提供服务。

![](https://substack-post-media.s3.amazonaws.com/public/images/f34f16fa-64b4-4d59-9274-1a7930329bfc_1385x810.png)
*来源：https://openrouter.ai/，2025 年 5 月访问。混合 $/Mtok 按 3:1 输入:输出比计算，气泡大小代表上下文窗口大小*

沿用同一张图并加入上下文窗口的气泡尺寸，可以看到 DeepSeek 以有限推理算力交付超低价模型的另一重权衡：他们运行 64K 上下文窗口，是主要模型提供商中最小的之一。更小的上下文窗口限制了编程等用例——这类用例需要模型跨代码库连贯记住大量 token 才能进行推理。在上图中，以相同价格可以在 Lambda、Nebius 等服务商处获得 2.5 倍以上的上下文大小。

![](https://substack-post-media.s3.amazonaws.com/public/images/ede5f394-a33a-4129-8b82-643800be96b1_907x614.png)
*来源：SemiAnalysis 基准测试*

深入到硬件层面，通过上文对 AMD 与 NVDA 芯片运行 DeepSeek V3 的[基准测试](https://semianalysis.com/2025/05/23/amd-vs-nvidia-inference-benchmark-who-wins-performance-cost-per-million-tokens/)，可以看到服务商如何求解 $/Mtok：通过在单张 GPU 或 GPU 集群上同时批处理更多用户，模型提供商可以提高终端用户承受的总等待时间（更高延迟、更慢交互性，以 x 轴的每用户端到端延迟中位数衡量），从而降低每 token 总成本。更高的批处理规模与更慢的交互性会降低每 token 成本，代价是糟糕得多的用户体验。

需要明确，这是 DeepSeek 的主动决策。他们对从用户身上赚钱、或通过聊天应用和 API 服务向用户提供大量 token 并无兴趣。该公司专注于抵达 AGI 这一个目标，不在乎终端用户体验。

以极高速率批处理，让他们能用尽可能少的算力完成推理和对外服务，从而把尽可能多的算力留在内部用于研发。[正如我们此前讨论过的](https://semianalysis.com/2025/06/08/scaling-reinforcement-learning-environments-reward-hacking-agents-scaling-data/#rl-is-an-inference-game-but-china-lacks-the-chips)，出口管制限制了中国生态的服务模型能力。因此，对 DeepSeek 来说，开源是合理选择：手头的算力留作自用，其他云厂商可以托管其模型，从而赢得心智份额与全球普及。尽管出口管制大大限制了中国大规模推理模型的能力，我们并不认为它同等程度地阻碍了其训练有用模型的能力——[腾讯](https://github.com/Tencent-Hunyuan/Hunyuan-A13B)、[阿里巴巴](https://qwenlm.github.io/blog/qwen3/)、[百度](https://ernie.baidu.com/blog/posts/ernie4.5/)乃至 [Rednote（小红书）](https://github.com/rednote-hilab/dots.llm1)近期的发布都是例证。

### Anthropic 与 DeepSeek 的相似度，超出其愿意承认的程度

在 AI 的世界里，唯一要紧的东西是算力。与 DeepSeek 一样，Anthropic 也受算力约束。Anthropic 将产品开发聚焦于代码，并在 Cursor 等编程应用中获得强劲采用。我们认为 Cursor 用量是终极评测，因为它代表了用户最在乎的两样东西：**成本**与**体验**。Anthropic 已连续一年多排名第一——按 AI 行业的时间尺度，这相当于数十年。

注意到 Cursor 这类 token 消费者的成功后，该公司推出了 Claude Code——一款内置于终端的编程工具。Claude Code 用量一路飙升，把 OpenAI 的 codex 远远甩在身后。

Google 随之也发布了自己的工具：Gemini CLI。虽然它与 Claude Code 是类似的编程工具，但 Google 利用其 TPU 算力优势，向用户提供免费且大到难以置信的请求额度。

![](https://substack-post-media.s3.amazonaws.com/public/images/c41d41f8-18c0-4abd-ab31-894c98a5a0ef_1403x737.png)
*来源：Google*

Claude Code 性能与设计俱佳，但**昂贵**。在许多方面，Anthropic 模型在代码领域的成功反而给公司带来了巨大压力。**他们的算力已被挤到极限。**

这一点在 Claude 4 Sonnet 的 API 输出速度上最为明显。自 Claude 4 Sonnet 发布以来，其速度已下降 40%，降至略高于 45 token/秒。原因与 DeepSeek 如出一辙——要用现有算力消化所有涌入的请求，就必须以更高速率批处理。编程用途的对话往往 token 数也更大，相比低 token 量的闲聊应用进一步加剧了算力资源的紧张。无论如何，o3 和 Gemini 2.5 Pro 等可比模型的运行速度显著更快，反映出 OpenAI 和 Google 大得多的算力资源。

![](https://substack-post-media.s3.amazonaws.com/public/images/b89ab9f0-6877-4763-b4ec-2992efcb6d94_1718x1005.png)
*来源：SemiAnalysis，Artificial Analysis*

Anthropic 正专注于获取更多算力，与 Amazon 达成了一笔重大交易，我们此前已有报道。

Anthropic 将获得超过 50 万颗 Trainium 芯片，用于推理和训练。这一合作仍在推进中——与大众认知相反，Claude 4 并非在 AWS Trainium 上预训练，而是在 GPU 和 TPU 上训练的。

Anthropic 还向另一家主要投资方 Google 求助算力。Anthropic 从 GCP 租用大量算力，具体是 TPU。在这一成功之后，Google Cloud 正把服务扩展到其他 AI 公司，并与 OpenAI 达成协议。与此前报道不同，Google 只向 OpenAI 出租 GPU——不包括 TPU。

### 速度短板可以弥补

Claude 的速度反映了其算力约束，但总体上 Anthropic 的用户体验优于 DeepSeek。第一，其速度虽低，仍快于 DeepSeek 的 25 token/秒。第二，Anthropic 模型回答一个问题所需的 token 显著少于其他模型。这意味着尽管速度不快，用户经历的端到端响应时间却明显更短。

虽然这取决于负载，Gemini 2.5 Pro 和 DeepSeek R1-0528 的啰嗦程度是 Claude 的 3 倍以上。Gemini 2.5 Pro、Grok 3 和 DeepSeek R1 运行 Artificial Analysis 智能指数（聚合多项不同基准分数）所用的 token 明显更多。事实上，在头部推理模型中，Claude 的总输出 token 量最低，且相比 Claude 3.7 Sonnet 有令人印象深刻的改进。

token 经济学的这一面表明，提供商正在多个维度上改进模型。不只是更多智能，而是每产出一个 token 带来的更多智能。

![](https://substack-post-media.s3.amazonaws.com/public/images/ffa08b1a-03d2-4148-9f7e-c3304a806fec_2560x1245.png)
*来源：Artificial Analysis 智能指数，SemiAnalysis*

### 推理云的崛起

随着 Cursor、Windsurf、Replit、Perplexity 等「GPT 套壳」或 AI token 驱动应用一路飙升、进入主流视野，我们看到越来越多的公司效仿 Anthropic，把 token 作为服务销售，而非像 ChatGPT 那样打包成月度订阅。

接下来，我们将探讨 DeepSeek 的下一步动向，并回应 R2 推迟的传闻。
