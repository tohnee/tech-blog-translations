---
title: "推理逐底竞争——薄利多销能回本吗？"
title_en: "Inference Race To The Bottom - Make It Up On Volume?"
subtitle: "Mixtral 在 H100、MI300X、H200、A100 上的推理成本与投机解码"
date: 2023-12-18
source: https://newsletter.semianalysis.com/p/inference-race-to-the-bottom-make
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 推理逐底竞争——薄利多销能回本吗？

> 原文：[Inference Race To The Bottom - Make It Up On Volume?](https://newsletter.semianalysis.com/p/inference-race-to-the-bottom-make) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Mixtral 在 H100、MI300X、H200、A100 上的推理成本与投机解码**

如今，除 OpenAI 之外已有五家公司的模型能在多种基准测试中击败 GPT-3.5：Mistral Mixtral、Inflection-2、Anthropic Claude 2、Google Gemini Pro 和 X.AI Grok。更惊人的是，Mistral 和 X.AI 都是以不到 20 人的团队取得这些耀眼成绩的。此外，我们还预计 Meta、Databricks、01.AI（Yi）、百度（Baidu）和字节跳动（Bytedance）也很快会达到超越 GPT-3.5 的水平。当然，这只是基准测试，而且其中几家据说拿评测集当训练集……不过这个**小**细节就先不提了。

帮还在记分的读者算一下：再过几个月，这样的公司总共会有 11 家。显然，GPT-3.5 水准模型的预训练已经彻底大宗商品化。OpenAI 凭 GPT-4 仍是山头之王，但领先优势已被大幅压缩。我们相信大部分长期价值将被最高端的模型捕获，但同样清楚的是，质量和成本低一档的模型将撑起一个数十亿美元的利基市场，微调之后尤甚。

可如果这些模型满地都是，谁还能真正靠它们赚钱？

通过完整的软件即服务或社交媒体直接触达客户、因而拥有独特分发渠道的公司，将拥有独特优势。为他人提供完整训练或微调服务、帮助其走完从数据到部署每个环节来处理专有数据的公司，将拥有独特优势。能提供数据保护、确保所有模型用途合法合规的公司，将拥有独特优势。而单纯托管开放模型的公司，不会有任何竞争优势。

Microsoft 的 Azure GPT API 与 OpenAI 自家 API 的对比，正好体现了其中一些优势。Microsoft 在公有和私有实例上驱动的推理量都超过 OpenAI 自家 API。对于风险厌恶型企业，Microsoft 提供的安全性、数据保障和服务合同打包非常重要。此外，这些保护也让不良行为者更容易钻空子不当使用——[字节跳动用 Azure GPT-4 训练其即将发布的 LLM](https://www.theverge.com/2023/12/15/24003151/bytedance-china-openai-microsoft-competitor-llm) 就是一例。

现实是：如果你不是市场领导者，就必须采取亏本引流（loss leader）策略来赢得生意。[Google 在 Gemini Pro（其 GPT-3.5 竞品）上免费送出每分钟 60 次 API 请求](https://console.cloud.google.com/freetrial/signup/tos)。补贴潜在客户的并不止 Google 一家。事实上，如今几乎所有人做 LLM 推理都在亏钱。

纯粹托管开放模型已完全大宗商品化。提供推理服务的初始资本门槛并不高，尽管算力开销最终会成为任何规模化服务的主要支出。市面上有[几十家二线云厂商](https://www.semianalysis.com/p/gpu-cloud-economics-explained-the)提供漂亮的报价（[主要是因为它们对投入资本回报率的假设相当可疑](https://www.semianalysis.com/p/gpu-cloud-economics-explained-the)），但你得能接受潜在的安全风险。

公司租几块 GPU、用 vLLM 和 TensorRT-LLM 之类的库在 Nvidia 和 AMD GPU 上托管开源模型，是轻而易举的事。[PyTorch](https://github.com/pytorch-labs/gpt-fast#tensor-parallelism) 的推理速度也开始变得非常快，因此进入门槛还在不断跳水。顺带一提，可以围观一下 Nvidia 与 AMD 就 MI300 和 H100 LLM 推理性能爆发的[激烈公开互撕](https://x.com/dylan522p/status/1735773540916269551?s=20)。AMD 的回击让先发了[误导性博文](https://developer.nvidia.com/blog/achieving-top-inference-performance-with-the-nvidia-h100-tensor-core-gpu-and-nvidia-tensorrt-llm/)的 Nvidia [相当难堪](https://community.amd.com/t5/instinct-accelerators/competitive-performance-claims-and-industry-leading-inference/ba-p/652304)。

随着 Mistral Mixtral 的发布，推理成本彻底陷入了逐底竞争，而这场比赛主要由烧风险投资的初创公司买单，指望的是把量做起来。OpenAI 的 GPT-3.5 Turbo 模型固有运行成本就比 Mixtral 低不少，而且 OpenAI 利润率相当可观，主要得益于它能做到极高的批规模（batch size）。这种高批规模的奢侈，用户 base 较小的其他玩家可享受不到。

OpenAI 每百万输入 token 收 $1.00，每百万输出 token 收 $2.00。Mistral 的模型虽然质量更高，但运行成本也更贵，为了获客仍必须定价比 OpenAI 低。于是 Mistral 的价格是每百万输入 token $0.65、每百万输出 token $1.96。他们实际上是价格接受者：这一价格主要由市场力量决定，而不是 Mistral 自身的推理成本和目标投入资本回报率。请注意，下文性能数据基于定制推理栈在现有模型上能达到的水平，而非 TensorRT-LLM 或 vLLM——据我们与大批量部署方的交流，后两者目前仍未优化到位。Mistral 尚未开发出深度优化的定制推理栈，因此其实际表现比下表还差。

![](https://substack-post-media.s3.amazonaws.com/public/images/65d6d6c3-3a5b-4c45-8346-50167a216b01_2135x551.png)

我们稍后会结合下面的数字展开，但先给出大结论：即便在极其乐观的场景下——假设 2 块 H100 以 BF16 满载 7x24 小时运行，每 GPU 每小时 $1.95——Mistral 用相当高的批规模也只是勉强打平。当然，你只需测一下他们的 API，就会发现其可观的 token 吞吐意味着他们并没有用那么高的批规模，所以其 API 极可能是亏本引流——面对强大的在位者，逻辑上也必须如此。Mistral 的中期目标大概率是先把量做起来，再指望硬件/软件降本最终实现盈利。

不过，谁也不肯被 Mistral 比下去，一时间各路豪杰一窝蜂地以越来越低的价格提供 Mixtral 推理服务。每隔几个小时就有一家公司宣布新定价。先是 Fireworks.ai，每百万输出 token $1.60、每百万输入 $0.40。接着是 [Together](https://www.together.ai/blog/mixtral)，输出 $0.60、输入免费；然后是 [Perplexity](https://docs.perplexity.ai/docs/pricing)，输入 $0.14 / 输出 $0.56；neets.ai 输出 $0.55；[Anyscale](https://docs.endpoints.anyscale.com/) 输出 $0.50。最后 [Deepinfra](https://twitter.com/DeepInfra/status/1735468890413776932) 杀到输出 $0.27……我们以为牌局结束了……结果 [OpenRouter 直接免费](https://twitter.com/OpenRouterAI/status/1736451053691007391)！要说清楚：他们宣传的每秒 token 数根本不可能实现，而且限流严苛到你几乎没法测试。

今天，所有这些推理服务都在亏钱。

需要指出，2x H100 其实并不是 Mixtral 推理的最佳系统。事实上，2x A100 80GB 更划算，因为假设内存带宽利用率相近，它每美元能买到多约 32% 的带宽。A100 低得多的 FLOPS 对推理性能的影响也没那么大。注意，在已经崩塌的价格水平下，就算是 2x A100 也基本上没有任何赚钱的可能。在本报告后文，我们还会展示 H200 和 MI300X 给推理带来的巨大优势。

![](https://substack-post-media.s3.amazonaws.com/public/images/54f1971b-d666-4358-b1a0-da895a304eb9_1607x970.png)

由于 Mixtral 是混合专家（MoE）模型，批规模增大时其行为方式大不相同。批规模为 1 时，每次前向传播只激活一小部分参数，使模型以低得多的每 token 带宽和 FLOPS 获得强得多的能力。但这个最佳场景只有在批规模为 1、且内存容量装得下整个模型时才成立。

而随着批规模增大，更多专家会被激活，迫使每次前向传播都要读入所有专家的全部模型参数。与此同时，每个解码 token 仍然只经过两个专家。因此，Mixtral 和 GPT-4 这类 MoE 模型比稠密模型更吃带宽。

![](https://substack-post-media.s3.amazonaws.com/public/images/671c460f-c32e-4f76-aa41-61b3b28ca321_2065x452.png)

这对 LLM 推理影响巨大，因为其成本伸缩规律与稠密模型差异显著。简言之，对 MoE 模型来说，提高批规模虽然仍能降低成本，但由于所需内存带宽的增加，降幅远不及稠密模型。这也是基础模型不能永远无脑堆更多更多专家的主要原因之一。规模化推理理应始终运行在高批规模下，但 MoE 从中获得的收益不如稠密模型。

[分享](https://newsletter.semianalysis.com/p/inference-race-to-the-bottom-make?utm_source=substack&utm_medium=email&utm_content=share&action=share)

在上述逐底竞赛的玩家中，Together 显然拥有最好的推理引擎：首 token 时间稳定可靠、每秒 token 数最高、没有人为压低的限流，并且与其他提供商不同，坚定承诺[不背着用户偷偷量化模型](https://www.together.ai/blog/together-inference-engine-v1)。因此我们想深入研究他们的方案，作为基准档。

过去几天我们对他们的 playground 和 API 做了性能剖析。将温度设为 0 并使用高度可预测的长序列时，单序列峰值可达约 170 token/秒；而用长度相近但难度高的查询、温度设为 2 时，只有约 80 token/秒。

注意，实际数字通常比上面提到的差得多，因为 Together 实际服务着大量用户，达到了还算可观的批规模。上面的每秒 token 数试图展示的是低批规模的最佳情形。我们的模型显示，Together 用 2x A100 80GB 系统比用基于 H100 的系统更划算。温度与性能测试也指向 Together 在使用投机解码。

## **投机解码 / Medusa**

我们此前[写过关于投机解码的更详细笔记](https://www.semianalysis.com/i/134355860/speculative-decoding)，这里快速回顾：投机解码是指在你原本要运行的大而慢的模型前面，再跑一个小而快的草稿模型。草稿模型向更大、更慢的审校模型输入多条预测，一次向前生成多个 token。大模型随后一次性审校所有这些前瞻预测，而不必自回归地逐个生成 token。审校模型要么接受草稿模型的某条建议，从而一次生成多个 token；要么拒绝建议，按常规生成一个 token。

投机解码的全部意义在于降低生成每个 token 所需的内存带宽。遗憾的是，在 Mixtral 这类混合专家模型上，投机解码类技术的性能提升没那么大，因为随着批规模增大，草稿模型的不同建议会路由到不同专家，内存带宽需求随之上升。类似地，混合专家模型的预填充 token 也比稠密模型相对更贵。

再回到上面提到的温度。对 LLM 来说，温度本质上是一个调节创造力或随机性的输入滑块。我们之所以分别测试低温和高温场景，是因为低温下草稿模型生成审校模型会接受的 token 的概率要高得多。而在高温场景下，审校模型的行为更加飘忽，草稿模型几乎猜不中当前的 token。调整温度是测量模型真实每秒 token 数的众多技巧之一——否则投机解码这类聪明招数会搅乱一切逆向工程或性能剖析的尝试。

## **量化**

虽然量化会大幅提升运行这些模型的速度并降低成本，但若不倾注大量心血，量化会带来巨大的质量损失。一般来说，对这类模型量化之后必须微调，而眼下一些低价逐底型供应商恰恰没有做这样的微调。他们只是敷衍了事地量化，完全不关心精度。试一试这些逐底型提供商你就会发现，他们的模型根本生成不出 16 位 Mixtral 那样的优质输出。

![](https://substack-post-media.s3.amazonaws.com/public/images/0e27f719-08f2-4e42-9f05-637a2882a184_1622x972.png)

我们总体上相信研究者能让 FP8 推理在不毁掉质量的前提下跑通，但我们不认为他们能让这些超大模型在 INT4 上进行推理。此外，用 H100 和/或 A100 跑 FP8 仍需要 2 块 GPU，因为总每秒 token 吞吐远低于大多数聊天类应用所需的约 40-50+ 用户量，而且 KVCache 大小也受限。

## H200 与 MI300X 性能

即将上市的 H200 和 MI300X 改变了局面。它们分别配备 141GB 和 196GB 内存，内存带宽也显著高于 H100 和 A100。在我们的模型中，H200 和 MI300X 的每 token 成本对比在位的 A100 和 H100 要有利得多。鉴于 Nvidia 当前 NCCL 实现的 all-reduce 表现实在糟糕，我们看到了摆脱张量并行的巨大好处。

[领取团体订阅 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

下面，我们将分享各系统的成本表现。注意，这些系统才刚开始部署。我们假设的是某些主要提供商基于 H100 系统所使用的那种高度优化的定制推理栈。目前，无论 Nvidia 闭源的 TensorRT-LLM 还是 AMD 相对更开放的 vLLM 集成策略，都还不能直接达到这一水平，但我们预计它们会随时间推移做到。
