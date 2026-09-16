---
title: "Groq 推理代币经济学：速度快，但代价是什么？"
title_en: "Groq Inference Tokenomics: Speed, But At What Cost?"
subtitle: "比 Nvidia 更快？拆解其经济学"
date: 2024-02-21
source: https://newsletter.semianalysis.com/p/groq-inference-tokenomics-speed-but
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Groq 推理代币经济学：速度快，但代价是什么？

> 原文：[Groq Inference Tokenomics: Speed, But At What Cost?](https://newsletter.semianalysis.com/p/groq-inference-tokenomics-speed-but) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**比 Nvidia 更快？拆解其经济学**

AI 硬件初创公司 Groq 近来频频亮相，原因是其演示令人印象极为深刻：在其[推理 API 上运行 Mistral Mixtral 8x7b](https://www.semianalysis.com/p/inference-race-to-the-bottom-make) 这一领先开源模型。他们实现了高达其他推理服务 4 倍的吞吐量，收费却不到 Mistral 自家的 1/3。

![](https://substack-post-media.s3.amazonaws.com/public/images/a8206116-08c4-45b0-b6fd-da72d829f5e8_1262x689.png)
*https://artificialanalysis.ai/models/mixtral-8x7b-instruct*

对单条序列而言，Groq 拥有货真价实的惊人性能优势。这可能让思维链（chain of thought）之类的技术在实际应用中变得远比现在可用。此外，随着 AI 系统走向自主化，智能体（agent）类应用对 LLM 输出速度的要求会更高。同样，代码生成也需要显著更低的 token 输出时延。实时化的 Sora 类模型则可能成为娱乐领域的一条惊人赛道。**如果时延太高，这些服务对终端市场客户来说甚至可能根本无法成立或无法使用。**

这让外界对 Groq 的硬件和推理服务大加追捧，称其将给 AI 行业带来革命。虽然对某些市场和应用而言它确实足以改变游戏规则，但**速度只是等式的一部分**。供应链多元化是另一个落在 Groq 有利一侧的因素：他们的芯片完全在美国制造和封装。而 Nvidia、Google、AMD 及其他 AI 芯片需要来自韩国的存储器，以及来自台湾的芯片/先进封装。

这些都是 Groq 的加分项，但评判一款硬件是否具有革命性的首要公式是性能/总拥有成本（TCO）。对此，Google 有着切身体会。

> AI 时代的黎明已经到来，关键在于理解：AI 驱动的软件，其成本结构与传统软件大相径庭。芯片微架构和系统架构在这些创新型软件的开发与规模化中扮演着至关重要的角色。与开发者成本占比更大的前几代软件相比，AI 软件所运行的硬件基础设施对资本开支和运营开支（进而对毛利率）的影响要大得多。因此，为了能够部署 AI 软件，更需要投入大量精力去优化 AI 基础设施。在基础设施上占优的公司，在部署和规模化 AI 应用的能力上同样会占优。
>
> [《Google AI 基础设施霸权：系统比微架构更重要》](https://www.semianalysis.com/p/google-ai-infrastructure-supremacy)

正是凭借基础设施霸权，Google 服务 Gemini 1.5 的成本显著低于 OpenAI 服务 GPT-4 Turbo 的成本，同时在许多任务上表现更好，尤其是长序列代码。Google 单套推理系统使用的芯片多得多，但换来的是更好的性能/TCO。

此处的性能并不只是单个用户的裸每秒 token 数（即时延优化）。评估 TCO 时，必须考虑硬件上并发服务的用户数量。这正是[为 LLM 推理改进边缘硬件的权衡非常勉强甚至不划算](https://www.semianalysis.com/p/on-device-ai-double-edged-sword)的主要原因。多数边缘系统无法摊销到海量用户头上，弥补不了正常运行 LLM 所增加的硬件成本。至于以超高批大小服务大量用户——也就是吞吐与成本优化——GPU 才是王者。

正如我们在[《推理的逐底竞争》分析](https://www.semianalysis.com/p/inference-race-to-the-bottom-make)中所讨论的，许多公司的 Mixtral API 推理服务是在实打实地亏钱，有些还设置了极低的速率限制来控制亏损。我们在[报告中深入分析了量化以及 MI300X 等其他 GPU 硬件选项](https://www.semianalysis.com/p/inference-race-to-the-bottom-make)，但关键结论是：提供未量化修改模型（FP16）服务的厂商需要 64 以上的批大小才能盈利。我们认为 Mistral、Together 和 Fireworks 服务 Mistral 模型处于盈亏平衡到微利之间。

![](https://substack-post-media.s3.amazonaws.com/public/images/1600d6ac-269a-4303-9c61-12da206617c4_1607x970.png)

其他提供 Mixtral API 的厂商就不好说了。他们要么在量化问题上撒谎，要么就是在烧风投的钱换取用户基础。Groq 的大胆之举是正面跟进这些厂商的定价——每百万 token 仅 0.27 美元的超低价格。

他们的定价是出于像 Together 和 Fireworks 那样的性能/TCO 测算吗？

还是靠补贴来制造声势？注意，Groq 的上一轮正式融资在 2021 年，去年做了一笔 5,000 万美元的 SAFE，目前正在融资中。

下面让我们逐一拆解 Groq 的芯片、系统、成本分析，以及他们如何实现这样的性能。

Groq 的芯片采用完全确定性的 VLIW 架构，没有缓冲区，在 GlobalFoundries 14nm 制程节点上做到了约 725mm2 的裸片面积。它没有外置内存，权重、KV 缓存和激活值等在处理过程中全部保留在片上。由于每颗芯片只有 230MB 的 SRAM，任何有用的模型都装不进单颗芯片。因此，他们必须用大量芯片来容纳模型，并把它们组网互联起来。

![](https://substack-post-media.s3.amazonaws.com/public/images/0ce1a99e-2e75-4fc1-8ec6-76582cd07929_1938x1264.png)

以 Mixtral 模型为例，Groq 需要连接 8 个机柜、每柜 9 台服务器、每台 8 颗芯片——总共 576 颗芯片，才能构成服务 Mixtral 模型的推理单元。对比 Nvidia：单颗 H100 在低批大小下即可容纳模型，两颗芯片的内存就足以支撑大批大小。

制造 Groq 芯片的晶圆成本很可能低于每片 6,000 美元。对比 Nvidia 的 H100：814mm2 裸片，采用台积电（TSMC）5nm 的定制版本 4N 制程，晶圆成本接近每片 16,000 美元。另一方面，在实施良率收割（yield harvesting）方面，Groq 的架构似乎不如 Nvidia 可行——Nvidia 对多数 H100 SKU 屏蔽约 15% 的裸片，因而拥有极高的参数良率。

此外，Nvidia 为每颗 H100 芯片向 SK hynix 采购 80GB HBM，花费约 1,150 美元。Nvidia 还得为[台积电的 CoWoS 付费并承受那里的良率损失](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and)，而 Groq 没有任何片外内存。Groq 芯片的物料清单（BOM）成本显著更低。不过，Groq 也是一家初创公司，芯片出货量小得多、相对固定成本更高，而且[这还包括必须为 Marvell 的定制 ASIC 服务支付可观利润](https://www.semianalysis.com/p/broadcoms-google-tpu-revenue-explosion)。

下表列出了三种部署方案：一种是 Groq，采用其当前的流水线并行、批大小为 3——我们听说他们下周就会在生产环境上线；另外两种分别是带投机采样（speculative decoding）的时延优化 H100 推理部署，以及吞吐优化的 H100 推理部署。

![](https://substack-post-media.s3.amazonaws.com/public/images/f61a6c18-b094-487e-9fd8-5a63d4a26fef_1365x637.png)

上表大幅简化了经济学（忽略了大量系统级成本——我们稍后会深入展开——也忽略了 Nvidia 的巨额利润率）。这里的重点在于表明：与时延优化的 Nvidia 系统相比，Groq 在「每 token 输出所分摊的硅片 BOM 成本（美元）」上具有芯片架构优势。

8 颗 A100 可以服务 Mixtral，达到每用户约每秒 220 个 token 的吞吐；8 颗 H100 不用投机采样可达每用户约每秒 280 个 token。加上投机采样后，8xH100 推理单元可以达到接近每用户每秒 420 个 token 的吞吐。吞吐量还能更高，但在 MoE 模型上实现投机采样颇具挑战。

时延优化的 API 服务目前并不存在，因为经济性太差。API 提供商目前看不到有人愿意为更低时延多付 10 倍价钱的市场。一旦智能体和其他超低时延任务普及起来，基于 GPU 的 API 提供商很可能会在现有吞吐优化 API 之外，另行推出时延优化 API。

等下周 Groq 上线其批处理系统后，即便采用投机采样的时延优化 Nvidia 系统，在吞吐和成本上仍远逊于不用投机采样的 Groq。更何况，Groq 用的是老得多的 14nm 制程，还要向 Marvell 支付可观的芯片利润。如果 Groq 拿到更多融资并能爬坡生产其下一代 4nm 芯片（预计 2025 年下半年左右问世），经济性可能开始显著改观。注意，Nvidia 绝非坐以待毙——我们认为他们将在不到一个月内[发布下一代 B100](https://www.semianalysis.com/p/nvidias-plans-to-crush-competition)。

在吞吐优化的系统里，经济性截然不同。以 BOM 计，Nvidia 系统的每美元性能高出一个数量级，只是每用户吞吐较低。在吞吐优化场景下，Groq 的架构完全没有竞争力。

**然而，对于真金白银购买并部署系统的人而言，上述简化分析并不是评估商业案例的正确方式，**因为该分析忽略了系统成本、利润率、功耗等众多因素。下面我们改用性能/总拥有成本分析。

把这些因素计入后，代币经济学（Tokenomics，感谢 swyx 造了这个时髦新词）看上去就大不一样了。Nvidia 这边，我们将采用[此处](https://www.semianalysis.com/p/gpu-cloud-economics-explained-the)讲解并如下图所示的 GPU 云经济学。

![](https://substack-post-media.s3.amazonaws.com/public/images/0cc61d8b-27a4-486e-b557-15488db10ab7_1912x1365.png)
*资本成本包含了门槛收益率（hurdle rate），即——计入提出该商业方案的人为匹配项目风险所期望赚取的投资回报。*

Nvidia 在其 GPU 基板上叠加了巨额毛利率。此外，这台服务器 35 万美元的售价——远高于超大规模厂商拿 H100 服务器的成本——还包含可观的内存成本、8 块合计带宽 3.2Tbps 的 InfiniBand 网卡（本推理应用并不需要），以及在 Nvidia 利润率之上再叠加的可观 OEM 利润率。

对 Groq，我们估算系统成本时计入了芯片、封装、网络、CPU、内存等细节，并假设整体 ODM 利润率较低。我们同样没有计入 Groq 销售硬件所收取的利润率，所以这看起来虽然像拿苹果比橘子，但作为 Groq 成本与推理 API 提供商成本的对比仍是公平的——毕竟双方提供的是同一种产品/模型。

![](https://substack-post-media.s3.amazonaws.com/public/images/3bd31f8d-5815-4e0c-90d9-688f4e19ae21_1900x1318.png)

值得注意的是，8 颗 Nvidia GPU 只需要 2 颗 CPU，而 Groq 的 576 芯片系统目前要用 144 颗 CPU 和 144TB 内存。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
