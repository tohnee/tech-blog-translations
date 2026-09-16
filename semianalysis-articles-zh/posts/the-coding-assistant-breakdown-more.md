---
title: "编程助手大拆解：请再多来点 token"
title_en: "The Coding Assistant Breakdown: More Tokens Please"
subtitle: "上手体验 GPT 5.5、Opus 4.7、DeepSeek V4，基准测试为何靠不住，以及谁将赢得最终胜利"
date: 2026-04-24
source: https://newsletter.semianalysis.com/p/the-coding-assistant-breakdown-more
crawled: 2026-09-15
authors: ["Max Kan", "Jordan Nanos", "Samuel Kruse", "Crystal Huang", "Sam Harshe", "Dylan Patel", "Doug"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 编程助手大拆解：请再多来点 token

> 原文：[The Coding Assistant Breakdown: More Tokens Please](https://newsletter.semianalysis.com/p/the-coding-assistant-breakdown-more) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**上手体验 GPT 5.5、Opus 4.7、DeepSeek V4，基准测试为何靠不住，以及谁将赢得最终胜利**

自我们在 2 月 5 日提出 [Claude Code 拐点](https://newsletter.semianalysis.com/p/claude-code-is-the-inflection-point)以来，模型发布接连不断：Opus、Mythos、Codex、Gemini、DeepSeek、Kimi、Qwen、GLM、MiniMax、Composer、Muse Spark 等等。今天我们将拆解这些重要的模型发布，说明基准测试什么时候可信、什么时候不可信，并给出我们对智能体编程市场未来的预测。

首先必须重点谈 OpenAI 的 GPT-5.5。在我们看来，GPT-5.5 如今在某些任务上已**显著优于**其他所有模型。我们认为 GPT-5.5 已经跻身前沿。这与 11 月 Opus 4.5 发布时相比是巨大转变。那时起、乃至之后的 6 个月里，OpenAI 的编程模型在多数指标上都不属于世界一流，Opus 因而成为我们的日常主力。而现在，GPT-5.5 已经融入了我们的日常工作。

## 认识这些模型

过去 3 个月，每周都至少有一家主要实验室发布专为编程打造的新 checkpoint。GLM-5.1、Qwen3.6-Plus、Kimi K2.6、Composer 2 和 Gemini 3.1 Pro 都在标题里强调「智能体编程」「长程任务」或类似能力。2 月尤其热闹。

![](https://substack-post-media.s3.amazonaws.com/public/images/ef75e40e-4090-4254-85cb-a7af143a298e_1107x465.png)
*来源：SemiAnalysis Tokenomics 仪表盘*

新 checkpoint 固然不错，但全新的预训练模型才能真正让人兴奋。进入 4 月，旧金山的小道消息圈因 Capybara 和 Spud 的传闻炸开了锅。这是 Anthropic 和 OpenAI 最新预训练模型的代号。随着昨天 [GPT-5.5](https://openai.com/index/introducing-gpt-5-5/) 的发布，我们终于有了可以具体讨论的东西。

### **GPT 5.5**

GPT-5.5 是基于「Spud」的首个公开发布。作为 OpenAI 自失败的 GPT-4.5 以来（抱歉，「garlic」不算数）首次在预训练上真正扩大规模的模型，外界期望显然很高。而且，尽管 NVIDIA 和 OpenAI 都用精准的措辞宣称该模型是在一个 100k GB200 NVL72 集群上「训练」的，但这种「训练」仅指后训练（RL）而已。预训练从未达到那个规模。

OpenAI 的旗舰模型历来比 Anthropic 的便宜，但 GPT-5.5 的 API 定价为每百万输入 token $5、每百万输出 token $30，比 GPT-5.4 贵 2 倍，也略贵于 Opus 4.7。出于安全考虑，该 API 在短暂仅限 ChatGPT/Codex 使用的窗口期之后，已于[今早上线](https://openai.com/api/pricing/)。我们在 alpha 测试期间已通过 Codex 和 API 对该模型进行了测试，相关体验将在本文后面描述。

与其所有其他模型一样，OpenAI 也将为 GPT-5.5 提供 [priority 档位](https://openai.com/api-priority-processing/)，价格为标准费率的 2.5 倍。想办法让用户为更快的 token 支付更多费用正变得越来越重要。值得澄清的是，priority 与 fast 模式完全不同。fast 模式只给出一些模糊的保证，比如「快 2.5 倍，价格 6 倍」；而 priority 提供更保守、具体的 SLA（例如 > 99% 的时间保持 > 50 tokens/sec）。Anthropic 和 OpenAI 都提供 fast 模式和 priority 档位，但我们认为 Opus 4.6 Fast 是唯一真正获得市场认可的 SKU。

另外，OpenAI 还提供 [GPT-5.3-Codex-Spark](https://openai.com/index/introducing-gpt-5-3-codex-spark/)，但那是一个完全不同的模型，专为在 Cerebras 上运行而打造。具体来说，它是 GPT-5.3 的蒸馏版本。在不改变底层模型的前提下，通过减小 batch size、调整推理深度、把请求路由到优先队列来提供更快的 token（priority 与 fast 模式），与运行一个更笨、更小的模型（codex spark）之间，有本质区别。

![](https://substack-post-media.s3.amazonaws.com/public/images/847872ae-0100-4fe7-9795-ab9a32bb7350_2048x1245.png)
*来源：SemiAnalysis*

同时发布的还有 GPT-5.5 Pro，仅通过 ChatGPT 和 API 提供。它面向科学研究和长程推理任务，而非日常智能体工作。GPT-5.5 Pro 在 [BrowseComp](https://llm-stats.com/benchmarks/browsecomp) 和 [FrontierMath](https://epoch.ai/benchmarks/frontiermath-tiers-1-3?view=graph&tab=leaderboard) 上取得了 SOTA 分数，定价与 GPT-5.4 Pro 相同，为 $30/180。我们预计很快就会看到更多关于 GPT-5.5 Pro 做出科学发现的公告。

标准版和 Pro 版都提供不同档位的推理强度：xhigh、high、medium、low 和 non-reasoning，这是成本与能力之间的权衡。自 strawberry/o1 发布以来，这一点已经很清楚：更高的推理档位带来更好的输出，但需要更多 token，用户也得等更久才能收到回复。

与此相关，OpenAI 在模型卡中宣传 GPT-5.5 的基准分数高于 5.4，同时消耗的 token 更少。换言之，它的「token 效率」更高。这是一个极其重要、值得理解的概念，我们相信它将成为今年的重要议题。正如我们上周向 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)订户[解释和量化](https://semianalysis.com/institutional/mythos-might-be-66-cheaper-than-opus/)的那样：**决定模型定价的真正北极星指标是每任务成本（cost per task），而不是每 token 成本**。按每 token 计算，Mythos 可能比 Opus 贵 5 倍，但由于 Mythos 能用更少的 token 解决同样的问题，这部分涨价大半被抵消。而且其端到端响应可能还更快。

![](https://substack-post-media.s3.amazonaws.com/public/images/84462fd4-241b-4b43-b82c-a27c828373df_1344x1032.png)
*来源：OpenAI*

### **Opus 4.7**

这一切发生在 Anthropic 发布 [Claude Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7)——Opus 4.6 的直接替代品——之后短短一周。Opus 一直是 SemiAnalysis 大多数人的日常主力，而 Opus 4.7 是一次小幅改进。虽然它在许多基准上的分数有所提升、体验依旧可靠地好，但并非阶跃式变化，团队成员对 4.7 的接纳颇为勉强。为什么？因为它还没有 fast 模式。我们第一次发现，许多工程师愿意为更快的速度牺牲一点质量（但不能太多），他们声称「快 2.5 倍、价格 6 倍」的交换让他们能进入「心流状态」。

![](https://substack-post-media.s3.amazonaws.com/public/images/ac858d28-1f4e-45c3-b85b-aaffdb155b79_605x523.png)
*来源：我们的怨念（即 Dylan 在 X 上的吐槽）*

实际使用中，从 Opus 4.6 升级到 Opus 4.7 的可感知变化主要来自功能/特性而非原始性能。总体而言，这些模型已经好到绝大多数日常任务都能顺利完成，我们的工程师对某次代码修改或 PR 的批评，更多是关于风格、思路、架构决策和 token 效率（也就是速度），而不是能否通过功能测试。这些编程模型彻底失控、搞砸一次提交的情况越来越罕见。

因此，这次换代中值得注意的变化是：

1. 支持高分辨率图像，并且 RL 训练目标明显增加——包括用截图来做前端样式判断，而不是通过无头浏览器和 playwright 等工具以编程方式跑测试
2. 新增「xhigh」推理强度选项，位于努力程度层级（即模型花多少时间思考一项任务，前文已述）中「high」与「max」之间
3. 思考（thinking）内容默认隐藏。当然，这些 token 照样计费，但你得主动选择才能看到它们。
4. 任务预算（task budgets，beta 阶段，仅限 API）：给模型一个关于以多高效率完成任务的提示。如果给模型的任务预算限制太紧，它可能抄近路或直接拒绝。这与 max_tokens 不同——后者是对输出长度的硬性限制
5. 更新了 token 计数方式，这是定价方面最关键的变化。4.7 使用了新的分词器（tokenizer），以更细粒度 token 计数带来的性能提升，换取总 token 用量的增加。他们直接承认这将导致 token 用量最多增加 35%。言下之意，这就是变相涨价 35%！

在模型行为变化方面，我们在测试中注意到的最大一点是：4.7 默认使用更少的工具调用、更多的推理。此举利弊尚无定论，但总体上我们不喜欢。Anthropic 建议把推理强度从 high 提高到 xhigh 或 max 以增加工具使用。而我们的用户似乎正是这么做的——好让模型带入足够的上下文，成功完成复杂任务或制定完整的多步计划。这与发布公告里宣称的 token 效率权衡可不太一样。

值得注意的是，许多人一直指控 Anthropic 在 4.7 发布前故意劣化 4.6 模型。Anthropic 断然否认了这些说法，但 SemiAnalysis 的多位工程师独立表示，过去几周 4.6 性能的变化让他们「感觉自己有点精神错乱」。而当然，他们是对的。

4 月 23 日，即 Opus 4.7 发布一周后，Anthropic 发布了一篇事后复盘（postmortem），详述了他们在 3 月/4 月发现的三个 bug。这三个 bug 都存在了数周之久，基本影响了所有 Claude Code 用户。其中一个 bug 很琐碎，两个很有意思，而且都是真实存在的。当 harness 本身就是产品的一部分时，背锅的就成了模型。

![](https://substack-post-media.s3.amazonaws.com/public/images/b9ec3283-81eb-42be-b1e8-7e407ee9de01_669x520.png)
*来源：Anthropic 事后复盘*

值得注意的是，三个时间线分别是 3 月 4 日至 4 月 7 日、3 月 26 日至 4 月 10 日，以及 4 月 16 日至 4 月 20 日。这是好几周、好几周无人察觉的 bug。这些 bug 由 Claude 引入，也很可能是由 Claude 定位到根因的。成也萧何，败也萧何。

### **DeepSeek V4**

期待已久的 DeepSeek v4 终于来了。去年 DeepSeek 凭 R1 的发布[震撼了全世界](https://newsletter.semianalysis.com/p/deepseek-debrief-128-days-later)，此后 AI 社区一直有一个严肃的问题：开源模型是否会把智能商品化。给还在记分的读者补一句：当年 DeepSeek 把市场砸得如此之惨，以至于各大 CEO 们手忙脚乱地出来解释杰文斯悖论（Jevons paradox）。此后 16 个月，情况似乎已相当明了——[GPU 大短缺](https://newsletter.semianalysis.com/p/the-great-gpu-shortage-rental-capacity)如今就摆在我们面前。

V4 相比 V3 有所改进，但它今天并没有让市场崩盘。话虽如此，DeepSeek 的成就不应被低估。他们开源了[权重](https://huggingface.co/collections/deepseek-ai/deepseek-v4)、一份[详尽的技术报告](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/DeepSeek_V4.pdf)，并更新了 [DeepEP](https://github.com/deepseek-ai/DeepEP)、[DeepGEMM](https://github.com/deepseek-ai/DeepGEMM)、[FlashMLA](https://github.com/deepseek-ai/FlashMLA) 等被全球实验室广泛使用的库。讽刺的是，DeepSeek 正在帮助美国的开源 AI 存活下去。

本次发布包含两个模型：DeepSeek-V4-Pro 和 DeepSeek-V4-Flash。前者总参数量 1.6T / 激活 49B，后者总参数量 284B / 激活 13B。Pro 相比 V3（总参数量 671B / 激活 37B）是上探一步，而 Flash 则是下探一步。我们认为，无论按总参数量还是激活参数量，这两个架构在前沿水平上仍明显落后于对应的闭源模型。关于我们如何建模领先闭源前沿模型的架构，详见我们的 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)。

V4 相对 V3 的核心进展是上下文窗口从 128k 扩展到 1M。因此，所有主要技术进展都围绕长上下文性能展开，包括：

- 压缩稀疏注意力（Compressed Sparse Attention，CSA）
- 重度压缩注意力（Heavily Compressed Attention，HCA）
- 流形约束超连接（Manifold-Constrained Hyper-Connections，mHC）

并带来了如下结论：「在百万 token 上下文设置下，与 DeepSeek-V3.2 相比，DeepSeek-V4-Pro 的单 token 推理 FLOPs 仅需 27%，KV 缓存仅需 10%。」这相当于 KV 缓存减少 90%，比 Google 上个月的 TurboQuant 论文影响力大得多！NAND Flash 的投资者们，可要当心了。

在基准测试方面，DeepSeek 认为标准基准无法很好捕捉真实世界的任务能力，因此推出了一套自有的智能体基准，来衡量 V4 与其他 SOTA 模型的差距：中文写作、检索增强搜索、一组长程白领任务，以及编程。V4 Pro 在所有这些任务上都能与顶级模型掰手腕，但在关键领域仍落后。例如，在特别困难的中文写作任务上，Claude Opus 4.7 仍然击败 DeepSeek V4 Pro。Claude 用中文碾压了中文模型。

遗憾的是，把公开发布的模型性能基准当作真实世界表现的代理指标并不靠谱。相互冲突的利益动机导致这些实验室只发布某些基准、不发布另一些。比如下面这个例子，DeepSeek 顺手 diss 了一下 Kimi 和 GLM 的 API：

![](https://substack-post-media.s3.amazonaws.com/public/images/97798772-78d3-4415-9666-b861589ae8f2_883x478.png)
*来源：DeepSeek V4 技术报告*

这正是 [SemiAnalysis Tokenomics 仪表盘](https://semianalysis.com/tokenomics-model/)以不偏不倚的方式追踪所有主要模型性能宣称、定价、发布日期、使用披露的原因。我们也对所有主要模型做自己的上手测试。下面是我们对各主要模型发布中有意义的基准表现的追踪示例。我们稍后会解释基准测试为什么靠不住。

![](https://substack-post-media.s3.amazonaws.com/public/images/7b7a31e7-1c77-485e-9fbc-dffe0705391e_1223x622.png)
*来源：Tokenomics 模型*
![](https://substack-post-media.s3.amazonaws.com/public/images/62119119-1b7c-424f-a660-3209869e178c_1223x622.png)
*来源：Tokenomics 模型*

DeepSeek 还开源了 DeepGEMM 内部的一个 Mega-Kernel，同时支持 NVIDIA GPU 和**华为昇腾（Huawei Ascend）NPU**。官方宣称支持 NPU，但公开发布的只有 SM90（Hopper）和 SM100（Blackwell）GPU 的代码。他们的目标很可能是让未来相当一部分推理流量跑在昇腾上。不过值得注意的是，该模型的参数规模恰好能塞进 8x H20 HGX 在 FP4 下的内存空间。

![](https://substack-post-media.s3.amazonaws.com/public/images/5db5e469-039f-41d4-9d34-213d7d08dd76_626x140.png)
*来源：DeepSeek V4 技术报告*

Mega MoE 在各种 batch size 下的性能在一个 PR（pull request）中有描述：

![](https://substack-post-media.s3.amazonaws.com/public/images/4aa387b6-3c0d-4a90-b871-7d140f7fbc3b_879x833.png)
*来源：DeepGEMM 仓库*

当然，DeepSeek V4 最关键的贡献在于它是开源的。多亏了一个通宵，我们的 InferenceX 团队与来自 vLLM/Inferact 和 NVIDIA 的 10 倍工程师（10x engineers）协作，已在我们的 H200 集群上发布了 day-zero 支持。基于 vLLM、SGLang 和 TRT-LLM 加 Dynamo 对 Blackwell 和 AMD GPU 的支持仍在推进中。

![](https://substack-post-media.s3.amazonaws.com/public/images/4065c980-ace4-4cf3-b483-7813612220f4_993x891.png)
*来源：inferencex.com*

有意思的是，day-zero 支持下，该模型在 H200 上的 FP8[1](#footnote-1) 性能达到了在 20 tok/sec 交互性、8k 输入 1k 输出的条件下每 GPU 约 150 tok/sec 的吞吐量。作为参照，V3 在相同条件（20 tok/sec 交互性、8k 输入 1k 输出）下每 GPU 吞吐量约为 1.3k 到 2.3k tok/sec。这是一个新模型，我们预计未来几周会有显著的优化。请关注 [inferencex.com](https://inferencex.semianalysis.com/) 获取实时进展。

![](https://substack-post-media.s3.amazonaws.com/public/images/5575d5a3-8183-44e7-affb-7a82e96c4abb_688x428.png)
*来源：Huggingface 上的 DeepSeek V4 模型卡*

总体而言，DeepSeek 是一次卓越的工程发布，紧随 SOTA 前沿之后。它将成为闭源模型的最低成本替代品，但其能力并不处于最前沿。SemiAnalysis 的工作流大概率不会被 DeepSeek 蚕食。

## **VIBEZ：我们对 GPT-5.5 与 Opus 4.7 的上手印象**

SemiAnalysis 以无脑吹 Claude 而闻名（还是臭名昭著？），过去几周我们一直在参与 OpenAI 的 alpha 项目测试 GPT-5.5。

我们认为，GPT-5.5 尤其在 Codex 之中是一次显著改进。此前，我们的工程师几乎清一色只用 Claude，ChatGPT 模型在编程上的使用仅限于 Cursor 之类的套壳。现在，大多数工程师会根据任务和 IDE 偏好在 Codex 和 Claude 模型之间切换。以下是一些原话：

> *「我最近真正欣赏 Codex 的一点是，它在改代码之前会拉取大量上下文。不是那种纯结构性的修改，而是确实需要非平凡『思考』的修改。4.7 常常感觉只是快速 Explore 一下就 #yolo 式地乱改，而 Codex 会从互联网和代码库中拉取多得多的细粒度上下文，然后有针对性地完成你的要求」*

> *「目前我用 Codex 来审查 PR/找 bug、解释现有代码、创建/修订文档。它更擅长理解代码结构并对其进行推理。」*

不过，OpenAI 这边也不全是好消息。另一些工程师抱怨，在推断你的真实意图方面，Codex 仍不如 Claude Code。人类在给编程智能体下指令时，天然会给出简短、且没怎么深思熟虑的指示，而 Codex 常常听得过于字面化。

与此相关，另一位工程师评论说，GPT-5.5 在真正动手改代码时显得过于保守。没错，这提升了 token 效率，但代价是正确性。正如我们前文所述，4.6 → 4.7 也发生过类似的权衡。现在，输出中一旦出现「narrow fix」（窄幅修复）字样，就是需要复核模型工作的信号。

下面这个具体例子能很好地说明我们对 Codex 与 Claude Code 优劣的整体印象。我们让 Opus 4.6 和 GPT-5.5 分别为我们的加速器模型做一个新仪表盘，并把现有的 [tokenomics](https://semianalysis.com/tokenomics-model/) 仪表盘作为示例给它们。我们的机构订户都知道，这个仪表盘包含一个链接到所有不同标签页的主页。

![](https://substack-post-media.s3.amazonaws.com/public/images/71b56470-9c8a-4c4c-ac48-16df0b781f3a_980x765.png)
*来源：SemiAnalysis*

Opus 4.6 做出了一个外观一致的主页，而 Codex 完全无视了它。

![](https://substack-post-media.s3.amazonaws.com/public/images/8e45427c-0853-40b0-8f9a-be2aa5b76dd9_2048x624.png)
*来源：SemiAnalysis*

如果我们特意在提示词里要求 Codex 复刻主页，我们确信它做得到，但它无法自行推断出这一意图。

话虽如此，Codex 放进仪表盘的实际数据比 Claude 准确得多（不过要说清楚，两者第一轮都不完美）。这表明 Codex 对一个相对复杂的 Excel 文件中的数据结构和关系有更强的推理能力。相比之下，Claude 的许多数字纯属幻觉，还犯了把 NVIDIA GPU 放进 TPU 图表这样的错误。这与我们的整体印象一致：Codex 更「聪明」，更擅长通过复杂推理解决更难、范围更窄的任务；而 Claude 更适合更开放、从零开始（greenfield）的问题。

正因如此，我们的一些工程师已固定采用如下工作流：

1. 先用 Claude 为新应用或新功能创建初始计划/脚手架，并完成第一步实现/POC
2. 再切换到 Codex 来真正解决问题或修 bug

重要的是，在 GPT-5.5 发布之前，SemiAnalysis 几乎所有人在两步里都只用 Claude Code。我们对 ChatGPT 模型的使用已萎缩到网页版 Deep Research 和 Cursor Bugbot 之类的套壳。

更关键的是，插件/CLI 中的功能特性正在拖 Codex 的后腿。例如，我们的许多工程师喜欢在 1M 上下文下用 fast 模式，并用远程控制/沙箱插件在笔记本、手机之间无缝接力会话。这两点目前在 Claude Code 的 CLI、VSCode 插件、网页版和移动版 App 上都能做到，但 Codex 的 CLI、VSCode 插件、桌面版、网页版和移动版 App 都不行。

即便 GPT-5.5 是更好的模型，OpenAI 也需要更快地发布功能特性，才能赶上 Anthropic 并提高采用率。

## **基准测试很糟糕，但我们还是得继续用**

每次新模型发布中永远摆在显眼位置的，就是那张在各种基准上比较性能的表格。

![](https://substack-post-media.s3.amazonaws.com/public/images/f43f3ea7-dc3f-4abc-bc72-318d17340c8a_1840x1520.png)
*来源：每次发布都是这套，唉*

能拿出一小组数字来证明新发布的模型「客观」更强，这种诱惑很大；但 AI 社区里许多人早就哀叹，基准测试已不再是真实世界效用的有效代理。我们倾向于认同这一观点。声称在测量模型的编程/金融/推理能力，与真正以任何有意义的方式测量这些能力，是两回事。

话虽如此，我们预计所有实验室未来发布新模型时仍会继续突出基准成绩的提升，下面几节将帮你把信号从噪声中分离出来。

### **基准测试的解剖**

每个基准由三样东西构成：

1. **任务（Tasks）**：实际要求模型做什么
2. **评测方法（The evaluation method）**：模型实际上如何被打分
3. **harness**：给模型配备了什么工具、指令、界面等来解题

真正理解前两者，才能判断一个基准到底靠不靠谱。为了说明，下面我们按大致的时间顺序过一遍一些著名的基准测试。这也能让你感受基准测试随时间的演变。

#### **MMLU 与选择题/简单答案类基准**

[Measuring Massive Multitask Language Understanding](https://arxiv.org/pdf/2009.03300)（MMLU）由学术界研究者于 2020 年发布，是一套共 15,908 道选择题、覆盖 57 个学科的题库。这些题目由大学生从标准化考试、大学考试/习题集等在线来源人工收集而来。所有题目都恰好有 4 个选项且公开可得，难度从「小学」级一直到「高级专业」级。

![](https://substack-post-media.s3.amazonaws.com/public/images/7101c7dd-afeb-4d70-b187-1b7db80f6197_869x445.png)
*MMLU 示例题目。来源：MMLU*

MMLU 的 harness 极简，基本只是把题目格式化成提示词。不包括网络搜索等工具。**选择题格式至关重要，因为它让判分变得轻而易举——只需检查模型是否输出了正确的字母**。

2023 年 3 月，[GPT-4](https://openai.com/index/gpt-4-research/) 以 86.4% 的得分实际上攻克（即「饱和」）了 MMLU。实践中，基准测试的真实满分通常低于 100%，因为有些任务含糊不清、表述拙劣，或干脆是错的。例如[这篇论文](https://arxiv.org/pdf/2406.04127)估计 MMLU 有 6.49% 的题目包含错误。

同一时期的其他基准包括：

- [GSM8K](https://arxiv.org/pdf/2110.14168)：由拥有 STEM 学位的承包商创建的多步数学题。为了让评测简单，所有答案都是单个数字。
- [HellaSwag](https://arxiv.org/pdf/1905.07830)：让 AI 预测日常情景最可能后续发展的选择题。任务取材自视频字幕和 WikiHow 文章。
- [MMMU](https://mmmu-benchmark.github.io)：与 MMLU 基本相同，只是题目还包含图片，因此模型需要视觉能力。第三个 M 代表「multimodal（多模态）」。
- [GPQA](https://arxiv.org/pdf/2311.12022)：由 61 位博士级承包商创建的「防 Google」选择题科学题。

随着这些基准逐一饱和，其创建者又推出了更难的版本（如 [MMLU-Pro](https://arxiv.org/pdf/2406.01574)、[MMMU-Pro](https://arxiv.org/pdf/2409.02813)、[GPQA-Diamond](https://epoch.ai/benchmarks/gpqa-diamond/)）。手段包括：从上一版中筛掉简单题、用 LLM 把选项从 4 个增加到 10 个、付钱让承包商出更难的题，等等。

当今最相关的简单答案类基准是 [Humanity's Last Exam](https://agi.safe.ai)（HLE）。它由 Scale AI 于 2025 年 1 月发布，从全球请来 1000 多位专家，出了 2500 道题，覆盖从代数几何到古典芭蕾的方方面面。80% 的题目要求精确匹配的简答，20% 为选择题。harness 方面，你可以选择让模型带或不带工具（如网络搜索和代码执行）运行。

![](https://substack-post-media.s3.amazonaws.com/public/images/41974b8e-2daf-485b-8315-89df5e16fb4f_866x561.png)
*HLE 示例题目。来源：Scale AI*

这些题目显然不能代表真实世界的 LLM 使用场景，而且本身也问题缠身。例如，[一项研究](https://www.futurehouse.org/research-announcements/hle-exam)发现 HLE 化学/生物题目中有 30% 的答案与同行评审文献直接冲突。

然而，各实验室在训练的 RL 阶段依然绝对会「爬山式」（hillclimb）地刷高所有这些基准。例如，Google 在 2025 年专门为 HLE 风格的 STEM 题目拨出了 9 位数预算，付给 Mercor、Surge、Handshake 等数据供应商。Gemini 3 Pro 在该基准上取得阶跃式提升，绝非巧合。

![](https://substack-post-media.s3.amazonaws.com/public/images/d0f08d1f-18de-4b3c-b1f5-8f99f62d3ae6_1217x123.png)
*来源：Google*

对实验室为何在意 HLE 之类的东西，往好了解释：解决冷僻选择题所获得的能力会迁移到其他用例。往坏了说：企业副总裁们想拿一个单一数字来证明自己在干活，而 Scale 恰恰擅长营销 HLE，赢得了足够的心智份额。

#### **SWE-bench 与编程基准**

编程是最重要的 AI 能力，而 [SWE-bench](https://arxiv.org/pdf/2310.06770)（2023 年发布）是第一个大型编程基准。

任务是从 12 个 **Python** 仓库自动抓取的，包括 [django](https://github.com/django/django)、[scikit-learn](https://github.com/scikit-learn/scikit-learn) 和 [seaborn](https://github.com/mwaskom/seaborn)。他们采用了以下三步筛选流程：

1. 从 12 个仓库共约 93k 个已合并 PR 起步
2. 缩减到约 11k 个——条件是关联了某个 GitHub issue 且引入了新测试
3. 仅保留 2294 个 PR——条件是把新测试应用到该 PR 之前一个提交上时，至少有一个新测试失败

换言之，GitHub issue 就是任务，而解决该 issue 的 PR 则证明任务可行。评测（eval）是仓库中所有旧测试加上 PR 中包含的新测试。AI 成功的标准是：没有任何旧测试被破坏（pass-to-pass），且所有新测试通过（fail-to-pass）。重要的是，模型在解题过程中不允许看到任何新测试。harness 方面，模型可以检查代码库，但不能实际运行任何代码。

值得强调的是，任务创建过程的任何环节都**没有人工核验**。GitHub issue 往往含糊不清、规格不明。此外，开发者在 PR 中附带的测试通常不全面，且局限于特定实现细节。这带来两大问题：

1. 如果题目允许多种解法，而你的测试只针对某一种正确解法，那么一些正确的答案会被错误地拒判
2. 如果测试不全面，那么即使 AI 只完成了需求的一个子集，也会被错误地判为通过

简而言之，SWE-bench 的许多任务完全是坏的。例如，有一个任务要求 AI 在评测中逐字匹配一条 19 个单词的错误消息，而题目描述对此只字未提。

![](https://substack-post-media.s3.amazonaws.com/public/images/c8f9c79d-c547-4e61-a1e8-1b1b7864dfba_1750x914.png)
*SWE-bench 任务描述示例（左）与一个不公平的测试（右）。来源：SWE-bench*

OpenAI 试图通过 2024 年 8 月发布 [SWE-bench verified](https://openai.com/index/introducing-swe-bench-verified/) 来解决这些问题。他们雇了 93 位 Python 开发者**人工复审**所有任务描述和评测的含糊/不公平之处。筛掉所有问题题目后，最初的 2294 道题缩减为 500 道「verified」任务。OpenAI 还在 harness 中加入了 bash 工具，让 AI 可以执行代码——使该基准更具智能体属性——并把每个任务打包成 Docker 容器，提升了基础设施的可靠性。

2026 年 2 月，OpenAI [宣布](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)将不再报告 SWE-bench verified 的成绩，理由有二：

1. 在 o3 稳定答错的 138 道题中，超过半数*仍然*存在不公平的评测——要么局限于题目描述中根本没提到的特定实现细节，要么是检验题目描述中未提及功能的额外测试。换言之，「verified」子集仍然不怎么样
2. 由于所有 PR 都来自肯定被每个模型训练数据收录的热门开源仓库，他们发现 GPT-5.2、Opus 4.5 和 Gemini 3 Flash 都记住了一部分答案（即「污染 / contamination」）。

他们转而建议模型厂商报告 [SWE-bench pro](https://labs.scale.com/leaderboard/swe_bench_pro_public) 的成绩。SWE-bench pro 同样出自 Scale 之手。主要区别（除了把题目变难之外）在于：他们使用了许可证限制更严的公开仓库和私有仓库来避免污染；还雇了承包商为这些提交撰写评测和题目描述，而不是完全依赖 GitHub issue 和已有的 PR。这些都是好的举措，但肯定没有彻底解决 SWE-bench verified 被指出的任何一个问题。你到现在大概也已经明白了：没有哪个基准是完美的。

时至今日，SWE-bench pro 和 verified 仍常见于各模型的发布卡。其他流行的编程基准包括：

- [SWE-bench multilingual](https://www.swebench.com/multilingual.html)：基本就是 SWE-bench verified，但从只有 Python 扩展到 9 种语言
- [Terminal-bench](https://www.tbench.ai)：任务和评测都靠众包，凡是终端里能做的事都算数。例如[破解密码保护的文件](https://www.tbench.ai/registry/terminal-bench-core/head/crack-7z-hash)或[构建 Linux 内核](https://www.tbench.ai/registry/terminal-bench-core/head/build-linux-kernel-qemu)。
- [NL2Repo](https://arxiv.org/pdf/2512.12730)：人类标注者把 104 个开源 Python 仓库逆向工程成一份自然语言需求文档。AI 的任务是依据这份文档重建整个仓库

#### **GDPval 与非编程类智能体基准**

如今智能体 AI 早已远不止编程，智能体基准也是如此。最著名的例子是 OpenAI 的 [GDPval](https://openai.com/index/gdpval/)。它于 2025 年 9 月发布，旨在测量 AI 完成 44 种不同职业（从金融分析师到执业护士）中具有真实经济价值的任务的能力。

为了出题，OpenAI 从每种职业聘请了专家承包商——例如金融任务请了一位[前美银（BofA）银行家](https://www.mercor.com/stories/matt/)——并要求他们为每道题提供三样东西：

1. 题目描述，除纯文本外还可附参考文件
2. 问题的一份示例解答，交付物形式涵盖 pdf、电子表格、视频等
3. 一份**评分细则（rubric）**，说明如何给任意一份解答打分

harness 比编程基准又上了一个台阶。智能体可以使用 LibreOffice（Microsoft Office 的克隆）和 CAD 软件等应用，外加标准的网络搜索和代码执行工具。虽然 GDPval 还没先进到这个程度，但较新的智能体基准还包含伪造的日历、邮件、Slack 消息、Google Drive 等，AI 需要在其中穿行才能成功完成任务。

最后，在评测环节，OpenAI 另外聘请专家承包商将 AI 的输出与人类提供的解答进行对比。他们还造了一个按 rubric 给解答排名的 AI 评分器，但承认它仍不如人类专家可靠。因此，官方成绩仍由人类专家评定——尽管这样要慢得多、也贵得多。

![](https://substack-post-media.s3.amazonaws.com/public/images/f1a476f7-dd53-4b0c-ae6c-d06b642c831c_1738x874.png)
*GDPval 任务示例。来源：OpenAI*

不过，对于无法客观核验的任务，「LLM-as-a-judge」（用 LLM 当裁判）是其他智能体基准的流行做法。例如 [GDPval-aa](https://artificialanalysis.ai/evaluations/gdpval-aa) 就是把公开的 GDPval 任务配上了 LLM 裁判。

理论上，rubric 让你可以测量风格之类重要的定性特质，但它有明显的局限。例如，当 rubric 由承包商撰写或由 AI 生成时，质量难以保证。用 LLM 来评判质量本身也天然可疑，尤其是最终裁决环节没有人类参与时。

GDPval 的另一大局限是那些定义清晰、规格得反常「整齐」的提示词。真实世界的任务通常带有一定模糊性，而这在该基准中完全缺失。人类工作还包含基于反馈的迭代，而 GDPval 是严格单轮的。

话虽如此，GDPval 肯定比 HLE 之类更接近真实的知识工作。其他流行的智能体基准包括：

- [Apex Agents](https://www.mercor.com/blog/introducing-apex-agents/)：Mercor 推出的基准，专注于银行、咨询和法律。任务由其承包商创建。智能体被置于一个配齐伪造文件、邮件等的 Google Workspace 环境中。评分使用 LLM 裁判。
- [Finance Agent](https://arxiv.org/pdf/2508.00828)：任务由人类专家创建，涉及分析近期的 SEC 文件。rubric 由 GPT-4o 生成、再经人工复审。评分使用 LLM 裁判。
- [BrowseComp](https://openai.com/index/browsecomp/)：任务是承包商创建的、难以用 Google 搜到答案的问题。例如：「在 1990 至 1994 年（含）之间，哪些球队踢了一场足球比赛：该比赛由巴西裁判执法，共出示四张黄牌（每队各两张，且四张中的三张并非在上半场出示），并发生了四次换人（其中一次是比赛第 25 分钟前因伤病换人）？」
- [OSWorld](https://arxiv.org/pdf/2404.07972)：计算机使用类基准，测试 AI 使用 LibreOffice、GIMP、VLC 等应用的能力。任务由 9 位计算机专业学生人工创建，他们因此被列为论文共同作者。评测是自定义脚本，检查计算机是否处于正确的状态
- [Tau-bench](https://arxiv.org/pdf/2406.12045)：客服类基准，测试 AI 完成取消订单、改签航班等任务的能力。环境和任务由 Sierra 的研究员创建，但伪造数据生成等环节使用了 AI。评测既检查应用状态，也检查 AI 输出是否精确匹配字符串。

### **OpenAI 的一些基准报告小动作**

希望前面几节已让你相信：基准测试往往与其声称测量的能力相去甚远。但它们也绝非一无是处——在所有人都以为 SWE-bench verified 已经饱和之后还能提升 10% 以上（Mythos 就做到了），依然是有分量的。

看一家公司选择**不**报告哪些基准，同样能说明问题。例如，OpenAI 在 [GPT-5.4 发布公告](https://openai.com/index/introducing-gpt-5-4/)中几乎没放什么基准，也没与任何 Anthropic 模型对比。我们认为原因在于：它会被早一个月发布的 Opus 4.6 碾压。这与我们对该模型的整体观感一致。直到昨天，OpenAI 的模型在几乎所有智能体任务上都不如 Anthropic 的。

![](https://substack-post-media.s3.amazonaws.com/public/images/769da563-e416-490a-b822-cf4f4f6872da_714x345.png)
*来源：OpenAI*

有了 GPT-5.5，他们终于重返前沿，这也是基准表格里重新纳入 Claude 和 Gemini 的原因。

![](https://substack-post-media.s3.amazonaws.com/public/images/60be0d68-55e2-4037-ac6a-0e33afcf3388_1174x540.png)
*来源：OpenAI*

然而，仍有一个基准可疑地缺席了。编程是最重要的模型能力，而 OpenAI 2 月还专门写了[一篇博客](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/)，主张 SWE-bench Pro 成为业界新的事实基准。那为什么他们这次用的是这个莫名其妙的「Expert-SWE」基准？

一路滚到博客最底部，答案揭晓：

![](https://substack-post-media.s3.amazonaws.com/public/images/bf83b10e-7aad-4258-bf49-f651337c21c2_1159x348.png)
*来源：OpenAI*

GPT-5.5 被 Opus 4.7 碾压（更别提拿了 77.8% 的 Mythos 了）。这印证了我们对这三个模型的定性印象。GPT-5.5 在部分编程任务上优于 Opus 4.7，但并非全面显著占优。Mythos 相比这两者应该才是真正的台阶式提升，只是 Anthropic 还没给我们开通权限 :(

### **为什么不该用同一个 harness 做苹果对苹果的比较**

作为 alpha 测试的一部分，我们也在 GPT-5.5、5.4 与 Opus 4.6 之间跑了一批基准测试。结果如下：

![](https://substack-post-media.s3.amazonaws.com/public/images/67cab2de-bb45-4356-a045-8aa70ca5ddf2_1308x1020.png)
*来源：SemiAnalysis Tokenomics 团队*

我们的数字总体低于 OpenAI 和 Anthropic 的，原因有二：

1. 这两家实验室跑基准时都使用定制的闭源 harness，以拉高性能
2. 为了省钱，大多数基准我们只跑了任务的一个子集。某些情况下这些子集并不具有代表性。例如 MCP atlas 我们只测了 21/36 个 MCP 服务器，并忽略了需要 MongoDB、twelvedata 或 alchemy 之类服务的任务。

你可以说我们的基准数字比 OpenAI/Anthropic 的更可信，因为我们用同一个 harness，比较更「苹果对苹果」。但如今 harness 显然已是产品的一部分。人们真正关心的是 Codex 与 Claude Code 谁更强，而不是 GPT-5.5 与 Opus 4.7 谁更强。

回到 token 效率的重要性上，值得强调的是：**harness 对最终的每任务成本有巨大影响**。提示词缓存、输入/输出比、工具使用模式，很大程度上都由 harness 决定。SemiAnalysis 目前正在采集价值数百万美元的智能体 AI 轨迹（trace）数据，以更好地理解不同 harness（如 Claude Code、Codex、Cursor、OpenCode）如何改变每任务成本。初步分析显示，Codex 的 token 效率可能高于 Claude Code，平均输入/输出比为 80:1 对 100:1。没错，更高的输入/输出比意味着更低的每 Mtok 价格，但 Codex 最终仍更便宜，因为它总体消耗的输入 token 更少。对完整结果感兴趣的读者请订阅 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)。

## **智能体编程大战，谁将胜出？**

那么这一切对编程智能体的未来意味着什么？在付费墙之后，我们将给出对这一即将达到数万亿美元规模产业的预测。
