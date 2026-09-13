---
title: "GPT-6 Astra、循环 Transformer 与隐藏推理"
title_en: "GPT-6 Astra, Looped Transformers, and Hidden Reasoning"
subtitle: "浅析循环深度、隐藏思维链，以及循环 Transformer 模块的最新研究"
source: https://magazine.sebastianraschka.com/p/gpt-6-astra-looped-transformers-and
published: 2026-09-09
crawled: 2026-09-11
translated: 2026-09-11
---

# GPT-6 Astra、循环 Transformer 与隐藏推理

> 浅析循环深度、隐藏思维链，以及循环 Transformer 模块的最新研究
>
> 原文：[GPT-6 Astra, Looped Transformers, and Hidden Reasoning](https://magazine.sebastianraschka.com/p/gpt-6-astra-looped-transformers-and)

过去几周发生了很多事。我相信此刻每个人都在关注 OpenAI 的 GPT-6 Astra。尤其是关于它的性能表现、循环 Transformer/循环深度（recurrent depth）相关设计，以及 Astra 是否在"隐藏"其推理轨迹（即思维链）的传闻。

所以在这篇文章中，我想先简要谈谈我对 Astra 的初步印象，以及对这一趋势走向的一些看法。然后，我会详细讨论"循环 Transformer（looped transformer）"到底是什么，以及它与隐藏思维链之间的关系（或者更准确地说，它到底有没有这种关系）。

最后，在讲完循环 Transformer 的基础知识之后，我还想分享近期研究论文在这个话题上的一些新见解。

## 1. GPT-6 Astra 初印象

先说正事。在深入架构传闻和相关研究文献之前，先简要总结一下我观察到的 GPT-6 Astra 的若干细节和花絮。

上周，OpenAI 高调发布了新的 GPT-6 Astra。过去几天我一直在用它，它是一个非常出色的模型，就本文撰写之时而言，很可能是我用过的最好的模型。但它究竟在哪些方面有所改进，又是如何做到的？

### 1.1 Astra 的基准测试

Astra 是我迄今为止用过的最好的模型，而且在 3D 渲染和动画任务上表现得尤其突出（相对于其他模型而言）。我的意思是，虽然它在几乎所有类别（写作、数学、编程等等）上都大幅超越其前代 GPT-5.6，但在图形演示方面的超越尤其明显。

这一点在基准测试中也有体现。例如，GPT-6 Astra 在数学和编程方面非常强，如下所示。

[![benchmarks-1](https://substackcdn.com/image/fetch/$s_!J4zO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7647174-392d-4637-a1ab-baf3b24a3704_8765x7510.png "benchmarks-1")](https://substackcdn.com/image/fetch/$s_!J4zO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc7647174-392d-4637-a1ab-baf3b24a3704_8765x7510.png)

图 1：三个热门编程基准测试和一个有挑战性的数学基准测试。更多基准测试结果见 Astra 发布博客：<https://openai.com/index/gpt-6-astra/>

一个亮点（图中未展示）是 Astra 在 [ARC-AGI-3 基准测试](https://arcprize.org/arc-agi/3)上取得了 99.9% 的成绩（GPT-5.6 Sol 仅为 7.8%），该基准衡量的是解逻辑谜题与泛化能力的混合。不过，数学、编程和计算机使用方面的基准测试更有意思，因为它们更贴近真实世界中的使用场景。

再回到[Artificial Analysis Coding Agent Index v1.4](https://artificialanalysis.ai/agents/coding-agents#coding-agents-index)（见前图右下角），它综合了多个智能体编程任务。GPT-6 Astra 显然处于前沿，但并没有一骑绝尘。这一点在下图更通用的 [Artificial Analysis Intelligence Index](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index) 中也能看到，该指数综合了不同类型的任务，而不仅仅是编程任务。

[![artificial-intelligence](https://substackcdn.com/image/fetch/$s_!W5FA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd02ced21-56da-4b5b-a520-33f0a20567cf_8058x5120.png "artificial-intelligence")](https://substackcdn.com/image/fetch/$s_!W5FA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd02ced21-56da-4b5b-a520-33f0a20567cf_8058x5120.png)

图 2：Artificial Analysis Intelligence Index，来自 https://artificialanalysis.ai/#intelligence

Artificial Analysis 基准测试的一大优势在于它是独立第三方的，因此可能比模型开发商自己做的评测更可信一些。

[执行框架（harness）的设置取决于具体基准测试](https://artificialanalysis.ai/methodology/intelligence-benchmarking)。例如，GDPval-AA 和 AA-Briefcase 在其对比的所有 LLM 上都使用他们开源的、极简的 [Stirrup](https://github.com/ArtificialAnalysis/Stirrup) 执行框架。在上面展示的 Intelligence Index v4.2 中，Terminal-Bench v2.1 使用的是 Terminus 2，τ³-Banking 使用的是 τ-Bench 执行框架。单独的 Coding Agent Index 则还比较了不同的编程智能体执行框架。

对于使用同一执行框架的评测来说，这更接近于公平的同口径对比。但同时，在模型训练期间，模型通常是以某一个主力执行框架为核心来开发的（在其他执行框架上的微调较少）。而且，主力执行框架往往就是围绕模型的长处来设计、用来放大其优势的。

因此，一些智能体评测可能低估了 Astra 在其主力执行框架中的实际表现。这对它 Intelligence Index 得分的影响有多大，需要在相同任务上跨不同执行框架对比 Astra 才能验证。

顺便说一句，正如一位同事最近向我建议的那样（Claude Code 负责人也推荐过），删掉（或归档）一部分现有的 `AGENTS.md` 内容和 `SKILL.md` 文件也许不是个坏主意，因为新一代 LLM 在理解提示词和解决手头问题方面已经高效得多。这些额外的"手把手指导"可能会不必要地束缚新模型，反而导致更差的解决方案。

当然，我并不是说从此不要再使用 `SKILL.md` 文件——对某些工作流来说它们仍然有用，因为复用已描述过的流程可以提升效率，模型不必重新摸索。但我想说的是：有些工作流根本不需要描述，而"旧"的描述可能已经不再理想，LLM 或许能想出更好的解法。所以，也许是时候更新或重新生成这些指令文件了。

### 1.2 计算机使用能力

GPT-6 Astra 在图像和渲染任务上似乎异常强大。当这些任务涉及与图形用户界面交互时，也就展示了它的计算机使用（computer use）能力，即模型通过 Codex/ChatGPT 应用在你的本地电脑上操作软件。

与其他模型相比，计算机使用正是这款模型真正大放异彩的地方，而且任何与图形相关的内容在社交媒体平台上都容易成为有趣又直观的演示。令人印象深刻的例子比比皆是，从[在 Blender 中渲染纽约市](https://x.com/higgsfield_ai/status/2096495974734794840?s=20)到[虚拟看房](https://x.com/Dimillian/status/2095596700815516004?s=20)都有。

举个例子，下面是一个对比：我让 GPT-6 Astra 的 Medium 和 High 档用我电脑上的鼠标，在[浏览器版 MS Paint](https://jspaint.app/#local:aa1757d4bc6008) 中重画了一张我的照片（没用 Extra High 和 Max，因为我不想把 token 额度全花光 :)）。

这不仅展示了模型的"艺术"能力，更重要的是展示了它操作电脑上各种工具的能力（这个例子中是 Paint；你可以看到模型通过鼠标光标操作界面）。

这并不是第一款在执行框架内具备通用计算机使用能力的模型。例如，今年年初以来，我就成功用 GPT 模型处理过一些 UI 任务（比如 Excel 里与报销相关的操作）等。不过，计算机使用是一项相对较新的能力，依赖执行框架来实现，而且通常感觉还不够成熟。这很合理：LLM 本质上是文本模型，所以顺理成章的低垂果实是写作、编程以及调用 API 和 CLI。

与此同时，许多工具和软件（目前）并不提供 CLI。与其等着有人为它们设计命令行接口，为什么不直接改进模型去使用图形用户界面呢（而且如前所述，这反正也能做出漂亮又令人惊叹的演示）？这在某种程度上类似于正在兴起的人形机器人浪潮：诚然，人形机器人并不是最高效的机器人，比如在装配线上有专用机械设备存在；但它们胜在通用。

因此，我预计接下来的几个月（或几年）也会是一个在 LLM 和智能体执行框架两个层面持续打磨计算机使用能力的时代。也就是说，除了现有能力以及不断扩展的数学、编程能力之外，模型训练中将越来越多地纳入计算机使用场景。这也会让 LLM 在科技圈之外的日常电脑任务中变得更容易上手（"嘿 ChatGPT，帮我报个税" :)）

### 1.3 计算机使用的训练

这一计算机使用趋势也与[近期的报道](https://finance.yahoo.com/technology/ai/articles/apple-suddenly-ai-infrastructure-stock-130223938.html)相吻合：OpenAI 为强化学习购置了数万台 Mac Mini 和 Mac Studio。这里的 Mac 并不是真正用来训练模型的（那还是用 GPU 更好），而是在模型训练期间提供 macOS 环境，让模型学会使用该操作系统及其中的各种工具。

那么，在这些 Mac 上进行计算机使用训练是如何运作的？简单来说，这些 Mac（更准确地说，是它们的 macOS 操作系统）充当了模型在训练期间可以与之交互的环境。

基本工作流程如下：

1. 给模型一个任务作为提示，例如"打开应用 xyz 并完成 abc"。
2. 为它提供 macOS 界面的截图（这一步通常由执行框架完成）。
3. LLM 随后预测鼠标/键盘动作（点击、按键、滚动等）。
4. 在 Mac 上执行这些动作（同样由执行框架完成）。
5. 在执行上一步的动作后，把更新后环境的新截图再喂给模型。
6. 重复步骤 2-5，直到任务成功或失败。
7. 将成功/失败信号以及验证器（verifier，或称评分器 grader）作为训练反馈，包括后训练阶段的强化学习；这与常规的带可验证奖励的强化学习（RLVR）类似。

[![computer-use-flow](https://substackcdn.com/image/fetch/$s_!f_sZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F105c079e-822e-4de9-bd16-2afe56286541_4879x2744.png "computer-use-flow")](https://substackcdn.com/image/fetch/$s_!f_sZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F105c079e-822e-4de9-bd16-2afe56286541_4879x2744.png)

图 3：计算机使用训练流程概览。

再强调一次，这里的 Mac 主要充当环境，而不是训练期间运行或更新模型的机器。模型很可能部署在 NVIDIA GPU 上，并通过 API 与上述 Mac 交互。顺带一提，[NVIDIA CEO 提到](https://x.com/JensenHuang/status/2096700264569090384?s=20)，GPT-6 Astra 是在约 10 万块 Grace Blackwell GPU 上训练的。

### 1.4 GPT-6 Astra 仍是一个推理模型

上一节讨论的对计算机使用训练的重视，并不是训练流程上的根本范式转变。GPT-6 Astra（以及可预见未来的任何 LLM）仍然是一个推理模型。这意味着该 LLM 通过带可验证奖励的强化学习（RLVR）来训练，并会产生中间推理轨迹（思维链）。

不过，GPT-6 Astra 作为推理模型的那一面（尤其是关于隐藏思维链的部分），我会在本文稍后再讨论。

## 2. 循环 Transformer

话虽如此，就在模型正式发布前约两天，新闻杂志 The Information 发表了一篇[文章](https://www.theinformation.com/articles/secret-technique-behind-openais-astra-model-sparks-security-concerns)，报道称据一些内部消息，Astra 使用了一种名为"循环深度（recurrent depth）"或"循环 Transformer（looped transformer）"的概念。

[![the-information](https://substackcdn.com/image/fetch/$s_!1E15!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb5611bff-b063-4082-8ed5-bed48619cd1b_3674x3073.png "the-information")](https://substackcdn.com/image/fetch/$s_!1E15!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb5611bff-b063-4082-8ed5-bed48619cd1b_3674x3073.png)

图 4：The Information 的报道摘录（来源：<https://www.theinformation.com/articles/secret-technique-behind-openais-astra-model-sparks-security-concerns>）

由于 LLM 架构既是我的专业领域也是我的热情所在，我制作了一个简短的讲解视频，解释循环 Transformer 的一般机制，并回应了关于隐藏推理链的说法，视频见下。

在接下来的小节中，我会先解释什么是循环 Transformer；至于隐藏思维链的说法，本文稍后会再回到这个话题。

（循环 Transformer 的讲解可能显得有点长，但我真心认为这有助于建立对该技术的基础理解，而这对于评判"它会掩盖推理轨迹或思维链"这一说法很有用。）

### 2.1 复用 Transformer 块

那么，什么是循环 Transformer？

循环 Transformer 本质上是一种架构上的小改动，核心思想是让中间表示多次通过同一组 Transformer 块（而不是只过一次）。与单纯堆更多块相比，这里的"诀窍"在于：这些往返过程中权重保持不变。

---

**术语与定义**

在本文中，我将使用以下术语：

- **Transformer 块（transformer block）**：一个包含注意力、前馈模块、归一化和捷径连接（shortcut connection）的单元。论文中常把这些块称为"transformer 层"。
- **堆叠（stack）**：一连串 Transformer 块组成的序列。
- **块应用（block application）**：指让输入通过某个 Transformer 块一次。

---

循环 Transformer 并不是什么新事物，其基本思想早在 2018 年的 [Universal Transformers](https://arxiv.org/abs/1807.03819) 论文中就已出现。不过在讨论 Universal Transformer 之前，我们先从一个更简单的例子说起：[Nanbeige4.2-3B](https://arxiv.org/abs/2607.22083)，这是一个今年 7 月发布的开放权重 LLM，今年夏天早些时候我在 Substack [Notes](https://substack.com/@rasbt/note/c-302083551) 和我的 [LLM 架构画廊](https://www.sebastianraschka.com/llm-architecture-gallery/looped-depth-sharing/)中都介绍过它。

下图所示的 Nanbeige 架构，乍看就是一个普通的 Transformer。但请注意，它多出一条（橙色）箭头，绕回到 Transformer 堆叠的开头。

[![nanbeige](https://substackcdn.com/image/fetch/$s_!v0Tz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd41d18af-38d4-4925-97c3-175a1b9443cd_2682x2664.png "nanbeige")](https://substackcdn.com/image/fetch/$s_!v0Tz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd41d18af-38d4-4925-97c3-175a1b9443cd_2682x2664.png)

图 5：Nanbeige4.2-3B 将同一组 22 个 Transformer 块的堆叠应用了两次。橙色箭头标出了中间表示被传回堆叠开头的位置。

我们自底向上走一遍。首先，与任何其他基于 Transformer 的 LLM 一样，输入文本被分词并转换为嵌入向量。这些向量随后通过 22 个 Transformer 块，这 22 个块各有自己的权重。

而这里的循环 Transformer 要点在于：第一轮通过之后，隐藏状态会被再次喂回同样的 22 个块。也就是说，块 1 再次被应用，接着是块 2，依次到块 22。

如果把这一计算展开，我们总共会得到 44 次 Transformer 块应用。但与拥有 44 个不同块的常规 Transformer 相比，第二轮的 22 次块应用复用的是第一轮的权重。例如，第 23 次块应用使用的是块 1 的权重，第 24 次块应用使用的是块 2 的权重，依此类推。

[![nanbeige-two-passes](https://substackcdn.com/image/fetch/$s_!Q34R!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c447af3-6466-473a-8ba3-0759b798e187_1867x3427.png "nanbeige-two-passes")](https://substackcdn.com/image/fetch/$s_!Q34R!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c447af3-6466-473a-8ba3-0759b798e187_1867x3427.png)

图 6：Nanbeige4.2-3B 展开为两次通过同样的 22 个 Transformer 块，共 44 次块应用。

所以，这里的整体思路是：在不增加另一套 Transformer 权重的情况下，把有效深度从 22 次块应用提升到 44 次。

顺带一问：为什么是 2 轮，而不是 3 轮、4 轮或更多？Nanbeige 论文没有给出太多细节，但他们表示这基本上就是效率最高的配置。把循环次数从 2 增加到 3 可以提升建模性能，但额外的计算成本并不划算。

### 2.2 循环的代价

那么，我们为什么要做这种循环？这本质上是在"靠增加更多 Transformer 块来把模型做大"之外的一种替代方案。

举例来说，把 22 个 Transformer 块用两次的模型，其（Transformer 块）参数量大约是拥有 44 个常规块的模型的一半。

这就减少了存储权重所需的内存。顺带一提，嵌入层和输出层通常很大、在总参数中占相当大比例，它们不在这个对比范围之内。（以 Nanbeige 4.2 3B 为例，嵌入层和输出层约占 3B 总参数的 25%；如果在这两层之间共享权重，可以将其降到 12.5%。）

[![hypothetical-size](https://substackcdn.com/image/fetch/$s_!kism!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c43d5a9-a977-49ef-a3f8-6e643c381f13_4708x2488.png "hypothetical-size")](https://substackcdn.com/image/fetch/$s_!kism!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1c43d5a9-a977-49ef-a3f8-6e643c381f13_4708x2488.png)

图 7：传统方案与循环方案所需参数量的并排对比。

当然，循环中复用同样的块仍然需要计算。更准确地说，前向传播中我们要让中间输入通过 44 次块应用。而且在训练时，梯度要反向流过共享堆叠的两次重复。所以，与只用一次这 22 个块相比，这增加了相当可观的工作量。实际上，它的开销与拥有 44 个不同块的情形差不多（区别只是优化器需要更新的不同参数更少；反向传播仍然要穿过全部 44 次块应用）。

此外还有 KV 缓存的问题。KV 缓存存储先前 token 的注意力键和值，供常规 Transformer 和循环 Transformer 在每一步下一 token 生成时复用。顺带一提，如果用得上，我这里有一篇关于 KV 缓存的独立文章：

[## 从零理解并编写 LLM 中的 KV 缓存（Understanding and Coding the KV Cache in LLMs from Scratch）](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms)

[Sebastian Raschka, PhD](https://substack.com/profile/27393275-sebastian-raschka-phd)

·

2025 年 6 月 17 日

[![Understanding and Coding the KV Cache in LLMs from Scratch](https://substackcdn.com/image/fetch/$s_!lRr3!,w_1300,h_650,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1045ae83-d2ba-4b44-ac93-4159d8a610a1_3659x2622.png)](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms)

KV 缓存是生产环境中实现 LLM 高效推理的最关键技术之一。KV 缓存是生产环境中计算高效 LLM 推理的重要组成部分。这篇文章从概念和代码两个层面解释 KV 缓存的工作原理，并给出一份从零开始、人类可读的实现。

[阅读全文](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms)

回到正题。尽管循环 Transformer 中存在权重共享，但第二轮进入块的中间状态与第一轮不同。因此，在 KV 缓存中，两个 Transformer 堆叠所产生的键和值也各不相同（与不循环的情形一样）。所以，KV 缓存方面也没有任何节省。

说得更具体些：在循环 Transformer 设置中，第 1 次和第 23 次块应用都用到了块 1，但每次应用仍然需要各自独立的 KV 缓存条目。既然两轮必须各存一份缓存，这组重复使用的 22 个块的 KV 缓存需求，就与拥有 44 个不同块的常规 Transformer 完全相同。

有意思的是，Nanbeige 研究者在论文中报告说，他们尝试过在两轮之间共享 KV 缓存。这固然让 KV 缓存大小减半，但模型表现比使用独立缓存的版本更差（他们最终发布的正是独立缓存的版本）。

在继续讨论其他循环 Transformer 设计之前，为了把 Nanbeige 的话题讲完整，他们的[技术报告](https://arxiv.org/html/2607.22083v1#S2.SS1)还讨论了另外两个选择或权衡：

1. 从零训练循环架构的效果，优于通过 upcycling（升级改造）把已经预训练好的 Transformer 转换过来。
2. 如上一节所述，两次通过是他们偏好的权衡点。更多次通过只带来很小的额外收益，却拖慢训练并让优化更不稳定。

所以，通过次数是我们必须做出的又一个架构选择。如前所述，Nanbeige 把它固定为 2。但我们也可以让它依 token 而定，下面就会看到。

### 2.3 Universal Transformers 与灵活的循环次数

现在回到 [Universal Transformers](https://arxiv.org/abs/1807.03819)。在 Nanbeige 中，我们把 22 个 Transformer 块组成的堆叠应用两次。而在 2018 年的 Universal Transformer 论文中，反复应用的是同一个 Transformer 块，而不是重复一个 Transformer 块堆叠。不过主要思想是类似的。

此外，步数可以是固定的，但该论文还探索了自适应暂停（adaptive halting）。例如，某个特定位置上的 token 可能只经过一两轮循环，另一个则可能经过三四轮，依此类推。这让模型可以灵活地把算力分配给那些能从额外计算中获益的 token。

循环次数是如何决定的？这里，模型使用一个训练得到的小函数，在每一步为每个位置输出一个所谓的暂停概率（halting probability）。模型把这些概率在连续的循环中累加，一旦某个位置的累加值超过阈值，就在该位置停止循环。另外，为了保险起见，还有一个最大循环次数上限来约束计算。

[![adaptive-halting](https://substackcdn.com/image/fetch/$s_!p9bV!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2a0d4a0f-621b-4f6e-a7cd-7778c7346efb_4694x2256.png "adaptive-halting")](https://substackcdn.com/image/fetch/$s_!p9bV!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2a0d4a0f-621b-4f6e-a7cd-7778c7346efb_4694x2256.png)

图 8：Universal Transformer 中的自适应暂停。

循环 Transformer 的另一个例子是 ByteDance 的 [Ouro](https://arxiv.org/abs/2510.25741)，我也在我的 [LLM 架构画廊](https://sebastianraschka.com/llm-architecture-gallery/looped-depth-sharing/)中介绍过它。例如，Ouro-Thinking 2.6B 把同一组 48 个 Transformer 块的堆叠应用了四次，即 192 次块应用，而存储的只是 48 个不同块的权重。基本上，这是一个比 Nanbeige 更极端的案例。此外，一个学习得到的退出门（exit gate）为不同的退出点分配概率，累积概率的阈值决定由哪一轮提供输出。所以，它也借鉴了 Universal Transformer 的自适应暂停思想，而 Nanbeige 没有用。（不过这里有一个实践层面的细节：发布的 [Hugging Face 实现](https://huggingface.co/ByteDance/Ouro-2.6B-Thinking/blob/main/modeling_ouro.py)会先算完所有配置的轮次再选择输出，所以循环次数实际上像是被硬编码为 4。）

### 2.4 用路由实现灵活的循环次数

另一种方法是 [Mixture-of-Recursions](https://arxiv.org/abs/2507.10524)，这是 2025 年的一篇论文，本质上是前面讨论的 Universal Transformer 的更精致版本。与 Universal Transformer 类似，各个 token 会通过 Transformer 块一次或多次，如下图所示。但它的创新在于：这个循环次数是如何以逐 token 的方式确定的。

在这篇论文的下图中，被循环（重复）使用的堆叠在这里被称为递归块（recursion block）。它包含若干 Transformer 块，并夹在各自独立的首尾两个 Transformer 块之间（分别标记为 Layer 0 和 Layer L-1）。

[![mor](https://substackcdn.com/image/fetch/$s_!yd6s!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb9850015-07f9-4f73-9034-5d7a3224d767_6922x4628.png "mor")](https://substackcdn.com/image/fetch/$s_!yd6s!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb9850015-07f9-4f73-9034-5d7a3224d767_6922x4628.png)

图 9：Mixture-of-Recursions 在不同 token 位置以不同次数应用共享堆叠。高亮文字展示了一个 1、2、3 次通过的例子。图改编自 [Mixture-of-Recursions 论文](https://arxiv.org/abs/2507.10524)。

模型如何决定一个 token 应该通过递归块多少次？前面讨论的 Universal Transformer 依据的是每一步学习得到的暂停概率。而这里的 Mixture-of-Recursions 方法使用的是一个学习得到的小型路由器（router）。这与专家混合（MoE）模型中的路由思想类似，只不过这里的路由决策决定的是共享堆叠被应用的次数。

路由器作用于 token 的隐藏表示，其中也包含上下文信息。所以，我们不应把它理解为给某个特定 token 的每一次出现都分配相同的通过次数（也就是说，上图中的"People"一词并不总是走 3 轮循环）。这个决策会随该词出现的位置及其前文而变化。

那么，路由具体是如何工作的？论文探索了做出这一路由决策的两种方式，如下图所示。

[![mor-routing](https://substackcdn.com/image/fetch/$s_!f2pT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F971afd67-da8b-4d14-8aac-36279754b7c5_6312x2851.png "mor-routing")](https://substackcdn.com/image/fetch/$s_!f2pT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F971afd67-da8b-4d14-8aac-36279754b7c5_6312x2851.png)

图 10：选择递归深度的两种方式。左图：路由器在每一步选择哪些 token 继续参与。右图：单一路由器在开头就分配好通过次数。图来自 [Mixture-of-Recursions 论文](https://arxiv.org/abs/2507.10524)。

上图左侧子图展示的是*专家选择路由（expert-choice routing）*：每个递归步选择自己要处理哪些 token，退出的 token 不再参与后续步骤。右侧展示的是 *token 选择路由（token-choice routing）*：路由器在开头做一次性决策，把每个 token 分配到 1 次、2 次或 3 次通过的路径上。

在这两种方式中，Transformer 权重都在各轮之间复用，与 Nanbeige 等类似。额外的灵活性来自为每个 token 选择获得多少计算量。模型与其路由器是一起训练的，所以模型会在训练过程中学会适应这些不同路径。

### 2.5 实际效果如何？

下面这张来自 Mixture-of-Recursions 论文的图，比较了不同模型规模和计算预算（横轴）下的三种方案：常规 Transformer（Vanilla）、固定递归的 Transformer（Recursive）和 Mixture-of-Recursions（MoR）。

[![mor-results](https://substackcdn.com/image/fetch/$s_!zvn3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa7d21ed3-cf75-45a1-ac2f-dc1a0ba705fb_8617x2565.png "mor-results")](https://substackcdn.com/image/fetch/$s_!zvn3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa7d21ed3-cf75-45a1-ac2f-dc1a0ba705fb_8617x2565.png)

图 11：四种模型规模、三种训练计算预算下的验证损失。图来自 [Mixture-of-Recursions 论文](https://arxiv.org/abs/2507.10524)。

在最小的模型规模上，常规 Transformer 表现最好。而在更大的模型上，Mixture-of-Recursions 追了上来且常常表现更好，尤其是在训练预算较小的情况下。在最大预算下，几条曲线非常接近。所以，其优势取决于模型规模以及我们在训练上投入多少算力。

这里还有一个细节：相同的训练计算量并不一定意味着相同的训练 token 数。通过跳过一部分计算，Mixture-of-Recursions 能在相同预算内处理更多 token。

我认为这是一个有趣的例子，因为它表明在循环 Transformer 这一思想内部还存在多种选择：每个位置循环多少次，以及这个次数如何决定。

简而言之，我们可以说：在固定计算预算下，如果模型足够大，使用循环 Transformer 可以提升模型质量。（这也说明了做一些大规模实验的重要性；比如，如果只看较小的 135M 参数模型，我们就会得出相反的结论。）

## 3. 题外话：循环神经网络（RNN）

顺带一提，如果你有深度学习背景（甚至 20 世纪 90 年代的人工神经网络背景），循环或"循环深度"的思想应该会让你觉得似曾相识。还记得循环神经网络（RNN）吗？RNN 的核心思想正是复用上一轮迭代的层（权重）。

[![rnn](https://substackcdn.com/image/fetch/$s_!ABM6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb12eda20-8fb1-4c5c-a9fa-6212d0abb759_4088x3398.png "rnn")](https://substackcdn.com/image/fetch/$s_!ABM6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb12eda20-8fb1-4c5c-a9fa-6212d0abb759_4088x3398.png)

图 12：RNN 示意图（出自我的 2022 年著作《Machine Learning with PyTorch and Scikit-Learn》，<https://amzn.to/3YzRnPR>）

主要区别在于：RNN 是跨时间步复用权重，也就是说，隐藏状态从一个 token 传递到下一个 token。而在循环 Transformer 中，token 的循环是沿架构深度方向进行的。

换句话说，在常规 RNN 中，每一步取输入序列的下一个元素和上一步的隐藏状态。因此，当 RNN 处理一段文本时，它一次只读一个词或 token，并把前文的信息通过隐藏状态向前携带。

而在循环 Transformer 中，某个给定 token 的中间表示会多次通过 Transformer 堆叠。模型仍然使用注意力在 token 之间传递信息。

如果这个类比让你有点晕，也不必太纠结。理解循环 Transformer 或许更简单的方式是：把它看作复用 Transformer 块，就像把模型做大，只是带上了权重共享。

[![rnn-vs-looped-transformer](https://substackcdn.com/image/fetch/$s_!r_Ux!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a37b812-26b3-4d55-846a-2c86c28e518a_5055x2663.png "rnn-vs-looped-transformer")](https://substackcdn.com/image/fetch/$s_!r_Ux!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a37b812-26b3-4d55-846a-2c86c28e518a_5055x2663.png)

图 13：RNN 中的"循环"与循环 Transformer 的并排对比。

## 4. Astra 到底有没有用循环 Transformer？

在讨论循环 Transformer 机制是否如前面 The Information 引文所传的那样掩盖了推理轨迹之前，先要问：GPT-6 Astra 到底有没有用循环 Transformer 的概念？

[![the-information-2](https://substackcdn.com/image/fetch/$s_!F61i!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59a0eb95-7843-40d9-bd59-ee79f0cf2022_3674x3073.png "the-information-2")](https://substackcdn.com/image/fetch/$s_!F61i!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59a0eb95-7843-40d9-bd59-ee79f0cf2022_3674x3073.png)

图 14：The Information 的报道摘录（来源：<https://www.theinformation.com/articles/secret-technique-behind-openais-astra-model-sparks-security-concerns>）

我们要记住，这目前仍只是传闻或独家爆料，没有官方确认。如果模型是开放权重的，我们当然可以自己去验证，但在这个案例中，我们只能依赖未经证实的报道。

不过，我认为 GPT-6 Astra 使用循环 Transformer 相关设计的可能性很高。第一，有上面提到的报道。第二，这是一项在过往研究中已展现出潜力的技术（如前所述），为什么不用呢？第三，OpenAI 首席科学家[说了下面这段话](https://x.com/merettm/status/2095023204993490967?s=20)：

> [...] 包括 Astra 在内，我们当前前沿模型的计算图深度与 GPT-4 相差不到两倍。 [...]

不过，这句话并没有明确确认循环 Transformer 架构，它也可能只是意味着他们使用了双倍数量的常规 Transformer 块。

在我看来，Astra 的成功（即良好的建模性能）主要可能归因于其他因素，也就是改进的训练配方和训练数据。

循环 Transformer 这一改动或许有点帮助，但我认为 The Information 高估了它的贡献。

## 5. 隐藏思维链

接下来，终于要直面房间里的大象了：循环 Transformer 到底会不会掩盖推理轨迹？

首先，OpenAI 从一开始（至少从 OpenAI o1 起）就在对用户隐藏（大部分）推理轨迹。所以对最终用户来说，应该没有太大区别。

因此，这种"可解释性担忧"主要是针对模型开发者而言的。

无论如何，我都不认为循环 Transformer 是隐藏或模糊思维链的重要因素。为了解释我自己的推理过程（无意玩双关），我们先退一步，讲讲推理模型是如何工作的。

### 5.1 推理简述

推理模型通常会在给出最终答案之前先生成中间步骤。这些步骤使用的是普通文本 token（在某些用户界面中可以选择对用户隐藏），被称为推理轨迹（reasoning trace）或思维链（chain of thought）。

举个例子，假设我们要求两个数，其和为 10、积为 21。在下图中，模型先尝试 5 和 5。虽然和是对的，但积是 25 而不是 21。接着，它又尝试 3 和 7，并再次检查这两个条件。

[![backtracking](https://substackcdn.com/image/fetch/$s_!nZf1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e45da87-e3ca-47cd-b84f-c1a10c102e34_2942x1521.png "backtracking")](https://substackcdn.com/image/fetch/$s_!nZf1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e45da87-e3ca-47cd-b84f-c1a10c102e34_2942x1521.png)

图 15：一个示例性的 LLM 回复，标注出了中间步骤、回溯和最终答案。

这张图展示了推理模型是如何"推理"的，包括回溯。也就是说，模型注意到一个错误，然后回到早先的选择，再换一种思路继续。

注意，模型仍然是一次生成一个 token，并以提示词和之前的 token 作为上下文。所以，这些中间步骤相当于一块草稿纸，在最终答案之前增加了计算量。

因此，最终答案可以比它前面的推理轨迹短得多，如上例所示。（OpenAI 倾向于对用户隐藏大部分推理轨迹。）

关于理解和开发推理模型的更多细节，我推荐我的书 [Build a Reasoning Model From Scratch](https://amzn.to/4aAKiFY)（《从零构建推理模型》）。

[![reasoning-book](https://substackcdn.com/image/fetch/$s_!c9rH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e53a1b1-4d0d-47f1-baa8-e9a0f0269d27_4545x3015.png "reasoning-book")](https://substackcdn.com/image/fetch/$s_!c9rH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8e53a1b1-4d0d-47f1-baa8-e9a0f0269d27_4545x3015.png)

图 16：我的 [Build a Reasoning Model From Scratch](https://amzn.to/4aAKiFY) 一书涵盖了推理模型的基础知识。

### 5.2 Token 用量与更短的思维链

如前所述，推理轨迹中额外的 token 会带来更多计算。循环 Transformer 也会增加计算量，因为 token 要通过更多 Transformer 块。有人可能会说：既然带循环的模型在内部使用了更多计算，它就不需要那么多"外显"的思考 token 了。

下面是 [GPT-6 基准测试](https://openai.com/index/gpt-6-astra/)的一部分，横轴为输出 token 数量。

[![output-tokens](https://substackcdn.com/image/fetch/$s_!JamS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3faf505f-8ea7-477b-af46-d7b355f5e3d4_7645x6659.png "output-tokens")](https://substackcdn.com/image/fetch/$s_!JamS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3faf505f-8ea7-477b-af46-d7b355f5e3d4_7645x6659.png)

图 17：精选的 GPT-6 Astra 基准测试，来自 <https://openai.com/index/gpt-6-astra/>

可以看到，总体而言，在各努力档位（effort level）下，GPT-6 Astra 不一定都比其前代 GPT 5.6 Sol 用更少的 token。不过，在相同准确率下，GPT-6 Astra 的确比 GPT 5.6 Sol 用更少的 token。

这是否是一个可解释性方面的隐忧？不一定。用更少的 token 也可能仅仅意味着模型能力更强、犯错更少、回溯更少，等等。也就是说，它可能就是一次成功率更高。在我看来，这并不会直接引发可解释性方面的担忧。

说到底，之前的模型也是如此。我不认为有谁会强烈担忧 GPT 5.6 Sol 比更小的 GPT 5.6 Luna 模型难解释得多——后者在达到相同任务表现时要使用多得多的 token，如下所示。

[![luna-sol-token-usage](https://substackcdn.com/image/fetch/$s_!2hY2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e048a54-2b50-423c-a7e7-87edd933cb1f_5324x2149.png "luna-sol-token-usage")](https://substackcdn.com/image/fetch/$s_!2hY2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e048a54-2b50-423c-a7e7-87edd933cb1f_5324x2149.png)

图 18：Luna 与 Sol 在相近任务表现水平下的 token 用量。数据来自 [Artificial Intelligence Index v4.3](https://artificialanalysis.ai/#intelligence)。

事实上，正如我们所看到的，在相近建模性能下，Luna 使用的 token 比 Sol 多 80%。这会让 Sol 的可解释性大打折扣吗？

更合理的答案反而是：能力更强的模型（更大、训练充分、使用更多算力的模型）能够更高效地解决问题，这里的"高效"指的就是用更少的 token。

同样值得记住的是，推理轨迹[并不保证忠实描述](https://arxiv.org/abs/2305.04388)模型内部发生的一切。在我看来，唯一站得住脚的担忧是：循环 Transformer 会比常规 Transformer 更频繁地用"伪造"的推理轨迹来有意误导用户。但我认为我们没有任何强有力的证据表明这种情况正在发生。

不过，Astra 的系统卡（system card）确实指出，有证据表明其推理轨迹的可监控性有所下降，相对 Sol 也有一定退步。这主要与更短、信息量更少的轨迹相关。但再强调一次，这并不能确立"循环"就是根本原因。这可能只是轨迹整体变短所致，与上面 Luna 对比 Sol 的例子类似。

在我分享了关于循环 Transformer 与隐藏推理链的[看法](https://x.com/rasbt/status/2095141254958858496?s=20)几个小时后，Jakub Pachocki（OpenAI 首席科学家）也[发布了如下澄清](https://x.com/merettm/status/2095023204993490967?s=20)：

> 我想防止因混乱的报道而引发一场滑向不可监控（unmonitorability）的竞赛。包括 Astra 在内，我们当前前沿模型的计算图深度与 GPT-4 相差不到两倍。从我们最早的推理模型开始，OpenAI 就一直在努力保留并利用思维链监控。我们非常看重这项技术，因为它能让我们洞察模型的对齐能力如何从其训练分布向外泛化。我确实认为它是脆弱的，而且不幸的是，它正朝着消极的方向发展——原因并不取决于架构变更，这一点我很快会撰文详述。但我们可以做一些事情来强化它，而这也是我们当前研究计划的核心目标之一。

这里所说的"混乱的报道"，很可能就是指前文提到的那段 The Information 的报道。这句话是在说明：循环这一特性与思维链的变化其实没有任何关系。

## 6. 循环 Transformer 研究

最后，除了已经讨论过的那些，我还想分享一些与循环 Transformer 架构相关的有趣论文。

### 6.1 潜在推理

与 Universal Transformer 相关的是 2025 年的论文 [Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach](https://arxiv.org/abs/2502.05171)，它研究了模型如何在推理时利用额外的循环。为此，他们在 800B 个 token 上训练了一个 3.5B 参数的模型——规模相对适中，但也算不上超小。

它不像 Universal Transformer 那样一遍遍复用同一个块，而是像 Nanbeige 那样重复一个堆叠；不过与 Nanbeige 不同的是，它把这个 4 块的共享堆叠夹在 2 个初始块和 2 个最终块之间。

与 Nanbeige 的另一个不同之处在于：共享堆叠在每一轮循环开始时，除了接收上一轮的隐藏状态外，还会接收初始块的输出。二者被拼接起来，经过一个学习得到的线性投影，再进入那四个共享块。你可以把它理解为：让这个堆叠在每一轮都能访问同样的初始输入表示。整个布局概括在下图中。

简而言之，这是一个额外的、也很有意思的循环 Transformer 变体。

[![latent-reasoning](https://substackcdn.com/image/fetch/$s_!0qA7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F825fc53f-1111-40a6-b264-17bc092c6ea0_7393x3148.png "latent-reasoning")](https://substackcdn.com/image/fetch/$s_!0qA7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F825fc53f-1111-40a6-b264-17bc092c6ea0_7393x3148.png)

图 19：[Geiping 等人](https://arxiv.org/abs/2502.05171)潜在推理模型的概念性总结。

一个有趣的细节是，研究者在训练期间让循环次数变化。这让模型为推理时使用不同数量的计算做好了准备。

在这里，训练时循环次数是随机采样的。推理时，由运行模型的人选择一个固定预算，比如 8、32 或 64 轮循环。此外，他们还基于下一 token 概率分布为每个 token 设计了自适应停止机制：如果相邻两轮之间的 KL 散度低于某个阈值——也就是说分布过于相似——就停止循环。

总体收益取决于任务。在他们的评测中，HellaSwag 的性能大约在 8 轮循环后就基本趋于平稳，而 GSM8K 和 HumanEval 则能从更多轮循环中获益。

不过，尽管论文标题提到了"潜在推理（latent reasoning）"，这个模型仍然可以生成文本形式的思维链。循环只是在每个输出 token 之前给它额外的计算。

### 6.2 知识检索 vs. 推理

存储信息与用信息解决问题之间有一个很有用的区分。例如，2025 年 6 月的论文 [Beyond Parameters: Exploring Virtual Logic Depth for Scaling Laws](https://arxiv.org/abs/2506.18233) 就通过分别测量 LLM 中的记忆与推理来研究这一点。

首先，在记忆实验中，当参数量固定时，循环几乎不改变可存储的信息量。增加不同参数的数量确实会提升这一容量。由此我们可以得出结论：循环既不会增加、也不会让模型检索到更多知识。这说得通：信息一旦存好，检索就是相对简单的任务；而且循环本身是一种计算机制，而不是"存储"机制。

其次，在单独的推理实验中，复用块可以在不增加参数的情况下提升多步数学问题的表现。这一点很有意思。由此我们可以得出结论：即便模型没有更多空间来存储信息，额外的计算也能帮助它解决问题。不过再强调一次，更大的模型同样能提升推理能力（尽管它们同时也会增加参数）。

[![capacity](https://substackcdn.com/image/fetch/$s_!RtTH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92b8a84b-b032-45b7-bdfe-8bc0ea30dc39_8185x5312.png "capacity")](https://substackcdn.com/image/fetch/$s_!RtTH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92b8a84b-b032-45b7-bdfe-8bc0ea30dc39_8185x5312.png)

图 20：在这项记忆测试中，容量随参数量增长，但额外的块应用几乎不带来变化。标注图来自 [Zhu 等人](https://arxiv.org/html/2506.18233v3)。

### 6.3 计算量匹配条件下的循环

2026 年 9 月刚刚发布的论文 [SMELT: Scaling Laws for Compute-Matched MoE Looped Transformers](https://arxiv.org/abs/2609.01343) 重新回到了 2.2 节的成本比较。如果我们拿循环 Transformer 和常规 Transformer 来比较，并让二者的每 token 计算量、非嵌入参数总量和 KV 缓存需求都大致相同，会发生什么？

研究者使用专家混合（MoE）架构，把中间一半的 Transformer 块应用两次，有点类似于 Nanbeige，只是加上了 Latent Reasoning 中那种三明治式的夹层结构。

不过，他们收窄了隐藏维度，以补偿额外块应用所需的计算。然后，由于这使参数量变小了，他们又增加专家数量来补回总参数量。他们还调整了注意力头的配置，使 KV 缓存保持可比。

[![SMELT worked example comparing model width, experts, block applications, parameters, compute, and KV cache](https://substackcdn.com/image/fetch/$s_!R2wv!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4fb8b33b-9a12-4a86-97fd-62e9ce4a4637_6724x2983.png "SMELT worked example comparing model width, experts, block applications, parameters, compute, and KV cache")](https://substackcdn.com/image/fetch/$s_!R2wv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4fb8b33b-9a12-4a86-97fd-62e9ce4a4637_6724x2983.png)

图 21：来自 [SMELT 第 3.2 节](https://arxiv.org/html/2609.01343v1)示例的 SMELT 概览。

实验的规模最大扩展到 54B 非嵌入参数等等。然后，根据拟合出的缩放曲线，研究者估计：在所研究的计算量范围内，SMELT 达到相同验证损失所需的训练计算量少约 6.8%–18%。

所以，这回答了"循环 Transformer 在计算上是否值得"的问题：值得！在相同的计算预算下，它们能给我们带来略好一点的模型。

### 6.4 Full-bandwidth transformer（全带宽 Transformer）

最后，同样非常新的是 2026 年 8 月的 [Full-bandwidth transformer](https://arxiv.org/abs/2608.08888) 论文，它研究的是跨 token 位置的循环。在每个解码步，它通过一个学习得到的门，把上一个 token 的最终隐藏状态与新采样 token 的嵌入结合起来，作为下一次前向传播的输入。

这样一来，下一个 token 的计算就能从堆叠底部访问上一个 token 的最终表示，这在某种程度上与 Latent Reasoning 类似。

在使用 1B 基座模型时，他们发现这种潜在反馈（latent feedback）方法在 MATH500 上输出更短的推理轨迹，同时保持甚至提升了准确率。不过，这种缩短效应在指令微调之后消失了。

[![length](https://substackcdn.com/image/fetch/$s_!Zkhe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d348be9-2792-4405-9325-adab29ce5323_7946x4070.png "length")](https://substackcdn.com/image/fetch/$s_!Zkhe!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d348be9-2792-4405-9325-adab29ce5323_7946x4070.png)

图 22：潜在反馈缩短了基座模型的推理轨迹，但这一效应在指令微调后消失。改编自 [Wang 等人，图 6](https://arxiv.org/html/2608.08888v1)，[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。添加了定义与注意事项。

无论如何，这个结果很有意思，因为它直接呼应了前面关于"循环是否会导致更短推理轨迹"的讨论。当然，这一结果同时取决于反馈机制和模型的训练方式。另外，该实验也并未证明那些更短的轨迹是否更不忠实。

此外，这项研究的一大局限在于：他们没有测试用常规方式增大模型（增加更多 Transformer 块而非循环）是否会对推理轨迹长度产生类似影响。

## 结语

总结一下：是的，OpenAI GPT-6 Astra 是一个非常强的模型，而且它在计算机使用上取得了特别大的飞跃。我相信，在接下来的几个月里，计算机使用将成为开源和专有执行框架的下一个重点领域。在计算机使用这件事上，我觉得开源尤其重要——"能力越大，责任越大"，在让执行框架接触我的主力电脑之前，能先审计一下它总是件好事。

此外，GPT-6 Astra 很可能使用了循环 Transformer 的某种变体。循环 Transformer 就是在固定计算预算下能带来更好的建模性能。

另外，更好的建模性能可能伴随更短的推理链。但这并不是什么新趋势。在同一个模型家族中不同规模的模型之间，我们一直能看到这种现象（例如 GPT 5.6 Luna 与 Sol 的对比）。

在我看来，更短的推理轨迹是模型更"聪明"、能力更强带来的副作用：这样的模型犯错更少，并且能在架构内部调用更多计算，而不那么依赖把推理轨迹当作草稿纸。从某种意义上说，人类也是如此。在一场线下大学数学考试中，一个聪明且准备充分的学生，很可能更少用到草稿纸，也更少需要回溯检查，等等。

---

**感谢阅读并支持我的工作！**

如果你想学习如何亲手构建推理模型，欢迎看看我的书 [Build a Reasoning Model (From Scratch)](https://amzn.to/4aAKiFY)（《从零构建推理模型》）。我们从预训练 LLM 出发，一步步加入推理能力，并配有可以动手运行和实验的代码。这件事既有趣又有收获，也是为未来的自己打好基础、跟上 AI 领域步伐的一项好投资。

另外，如果你读过我的书，欢迎在 Amazon 上写一条简短而真诚的评价。评论能帮助其他读者判断一本书是否适合自己，也是支持作者的一种简单方式。

[![scratch](https://substackcdn.com/image/fetch/$s_!n5TA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe6fb7c68-790c-47c7-8324-05f100efb90b_4410x2252.png "scratch")](https://substackcdn.com/image/fetch/$s_!n5TA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe6fb7c68-790c-47c7-8324-05f100efb90b_4410x2252.png)

图 23：选自我的 *[Build a Reasoning Model (From Scratch)](https://amzn.to/4aAKiFY)* 一书的插图，涵盖推理时扩展、蒸馏和强化学习。
