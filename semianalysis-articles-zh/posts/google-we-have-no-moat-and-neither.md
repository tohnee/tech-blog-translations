---
title: "Google「我们没有护城河，OpenAI 也没有」"
title_en: "Google 'We Have No Moat, And Neither Does OpenAI'"
subtitle: "谷歌内部泄露文件称开源 AI 将击败 Google 和 OpenAI"
date: 2023-05-04
source: https://newsletter.semianalysis.com/p/google-we-have-no-moat-and-neither
crawled: 2026-09-15
authors: ["Dylan Patel", "Afzal Ahmad"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Google「我们没有护城河，OpenAI 也没有」

> 原文：[Google "We Have No Moat, And Neither Does OpenAI"](https://newsletter.semianalysis.com/p/google-we-have-no-moat-and-neither) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**谷歌内部泄露文件称开源 AI 将击败 Google 和 OpenAI**

###### *以下文字是一份近期泄露的文件，由一位匿名人士在一个公开 Discord 服务器上分享，该人士已授权我们转载。文件出自 Google 内部的一位研究员。我们已核实其真实性。唯一的改动是格式调整以及删除了指向内部网页的链接。该文件仅代表一位 Google 员工的个人观点，不代表整个公司。我们并不认同下文观点，我们征询过的其他研究员也不认同，但我们将在另一篇面向订阅者的文章中发布我们自己的看法。我们只是充当分享这份文件的载体——它提出了一些非常值得玩味的观点。*

# 我们没有护城河

### OpenAI 也一样

我们一直在提防 OpenAI。谁会率先跨过下一个里程碑？下一步棋会是什么？

但令人不安的真相是，*我们并没有在这场军备竞赛中占据赢面，OpenAI 也一样*。就在我们还在互相缠斗的时候，第三股势力已经悄悄把我们打得落花流水。

我说的当然是开源。直白地讲，他们已经把我们套圈了。**那些我们视为「重大开放难题」的东西，如今已经被解决并落到普通人手里。**随便举几个例子：

- **手机上跑 LLM：**[有人在 Pixel 6 上运行基础模型](https://twitter.com/thiteanish/status/1635678053853536256)，速度达到每秒 5 个 token。
- **可扩展的个人 AI：**[你可以在一个晚上用自己的笔记本电脑微调出一个个性化 AI。](https://github.com/tloen/alpaca-lora)
- **负责任的发布：**这一条与其说是「解决了」，不如说是「被架空了」。[有整站整站的绘画模型网站，毫无任何使用限制](https://civitai.com/)，文本模型也[紧随其后](https://medium.com/geekculture/list-of-open-sourced-fine-tuned-large-language-models-llm-8d95a2e0dc76)。
- **多模态：**[当前多模态 ScienceQA 的 SOTA 只训练了一个小时](https://arxiv.org/pdf/2303.16199.pdf)。

虽然我们的模型在质量上仍略占上风，但[差距正在以惊人的速度缩小](https://arxiv.org/pdf/2303.16199.pdf)。开源模型更快、更可定制、更私密，单位参数量的能力更强。他们用 $100 和 130 亿参数[做到的事情](https://lmsys.org/blog/2023-03-30-vicuna/)，我们用 $1000 万和 5400 亿参数都举步维艰。而且他们只用了几周，而不是几个月。这对我们有着深远的影响：

- **我们没有秘方。**我们最大的希望是向 Google 之外的人所做的事情学习并与之协作。我们应当优先做第三方（3P）集成的开放能力。
- **当免费且不受限制的替代品质量相近时，人们不会为受限模型付费。**我们应该想清楚自己的增值到底在哪里。
- **巨型模型正在拖我们的后腿。**长远看，最好的模型是能够快速迭代的模型。既然我们已经看到 <200 亿参数区间里能做到什么，小型变体就不该再只是陪衬，而应当被认真对待。

![](https://substack-post-media.s3.amazonaws.com/public/images/241fe3ef-3919-4a63-9c68-9e2e77cc2fc0_1366x588.png)
*https://lmsys.org/blog/2023-03-30-vicuna/*

## 事情经过

3 月初，开源社区[拿到了](https://www.vice.com/en/article/xgwqgw/facebooks-powerful-large-language-model-leaks-online-4chan-llama)他们第一个真正堪用的基础模型——Meta 的 LLaMA 泄露到了公众手中。它没有经过指令微调或对话微调，也没有 RLHF。尽管如此，社区立刻意识到了他们手中这个东西的分量。

随之而来的是井喷式的创新，重大进展之间只隔几天（完整梳理见后文时间线）。这才过了一个多月，就已经出现了带[指令微调](https://crfm.stanford.edu/2023/03/13/alpaca.html)、[量化](https://github.com/ggerganov/llama.cpp)、[质量提升](https://lmsys.org/blog/2023-03-30-vicuna/)、[人工评测](https://arxiv.org/pdf/2303.16199.pdf)、[多模态](https://arxiv.org/pdf/2303.16199.pdf)、[RLHF](https://drive.google.com/file/d/10iR5hKwFqAKhL3umx8muOWSRm7hs5FqX/view)等能力的各种变体，而且很多变体是在彼此基础上叠加构建的。

最重要的是，[他们已经把扩展性问题解决到任何人都能上手折腾的程度](https://github.com/tloen/alpaca-lora)。许多新想法出自普通人。训练和实验的准入门槛，已经从一个大型研究机构的全部产出，降低到一个人、一个晚上、一台高性能笔记本电脑。

## 为什么我们本该预见这一切

从很多方面看，这对任何人都不应该意外。当前开源 LLM 的复兴紧随图像生成的复兴而来。社区对两者的相似性看得一清二楚，很多人把这称为 LLM 的「[Stable Diffusion 时刻](https://simonwillison.net/2023/Mar/11/llama/)」。

这两个案例中，让低成本公众参与成为可能的，都是一种便宜得多、名为[低秩适应](https://arxiv.org/abs/2106.09685)（LoRA）的微调机制，再加上一次规模上的重大突破（图像合成是[隐扩散](https://arxiv.org/abs/2112.10752)，LLM 是 [Chinchilla](https://arxiv.org/abs/2203.15556)）。两个案例中，都是一个质量足够高的开放模型引爆了全球个人和机构的思想与迭代热潮。两个案例中，这件事都迅速甩开了大玩家。

这些贡献在图像生成领域起到了决定性作用，让 Stable Diffusion 走上了一条与 Dall-E 不同的路。模型的开放带来了[产品集成](https://github.com/AbdullahAlfaraj/Auto-Photoshop-StableDiffusion-Plugin)、[市场](https://civitai.com/)、[用户界面](https://github.com/AUTOMATIC1111/stable-diffusion-webui)和[创新](https://stablediffusionweb.com/ControlNet)，而这些在 Dall-E 身上都没有发生。

效果是显而易见的：对比 OpenAI 的方案，Stable Diffusion 在文化影响力上[迅速占据统治地位](https://trends.google.com/trends/explore?date=2022-08-01%202023-04-10&q=Stable%20Diffusion,Dall-E&hl=en)，后者日渐边缘化。同样的事情会不会在 LLM 上重演还有待观察，但宏观的结构性要素是一样的。

## 我们错过了什么

推动开源近期成功的那些创新，恰恰直接解决了我们仍在苦苦挣扎的问题。多关注他们的工作，能帮我们避免重复造轮子。

#### LoRA 是一项极其强大的技术，我们或许应该更加重视

[LoRA](https://arxiv.org/abs/2106.09685) 的原理是将模型更新表示为低秩分解，从而把更新矩阵的尺寸压缩最多几千倍。这让模型微调只需原先成本和时间的一小部分。能在消费级硬件上几个小时就完成一个语言模型的个性化，意义重大，*尤其是*对于[那些希望在近实时状态下吸收新而多样化知识的目标](http://www.internalgooglesitescrubbedbyus.com)而言。尽管这项技术直接影响着我们一些最宏大的项目，它在 Google 内部仍被严重低估和利用不足。

## 从头重训模型是一条艰难的路

LoRA 之所以如此有效，部分原因在于——和其他微调形式一样——它是可叠加的。指令微调这类改进可以先落地，再随着其他贡献者陆续叠加对话、推理或工具使用能力而被继续放大。虽然单次微调是低秩的，但它们加总起来不必是低秩的，这让满秩的模型更新可以随时间不断累积。

这意味着，随着更新、更好的数据集和任务出现，模型可以以低廉的成本保持更新，永远不必支付一次完整训练的代价。

相比之下，从零训练巨型模型不仅扔掉了预训练，还扔掉了在它之上做出的一切迭代改进。在开源世界，这些改进很快就会占据主导地位，让完整重训的代价变得极高。

我们应该认真想一想，每个新应用、新点子是否真的需要一个全新模型。如果我们真的有了重大架构改进、无法直接复用模型权重，那我们就该投资更激进的蒸馏方法，尽可能保留上一代模型的能力。

## 如果我们在小模型上迭代更快，大模型从长远看并不会更强

对于最主流的模型尺寸，产出一个 LoRA 更新的成本非常低（约 $100）。这意味着几乎任何有想法的人都能生成一个并分发出去。训练时间不到一天是常态。以这种节奏，所有这些微调的累积效应很快就会抵消初始的尺寸劣势。事实上，按工程师工时计，这些模型的改进速度远超我们用最大变体所能达到的速度，其中最好的那些[已经和 ChatGPT 大体难分伯仲](https://bair.berkeley.edu/blog/2023/04/03/koala/)。**执着于维护一些全球最大的模型，实际上让我们处于劣势。**

## 数据质量的扩展性优于数据规模

这些项目中有许多在[小型、高度精选的数据集](https://bair.berkeley.edu/blog/2023/04/03/koala/)上训练以节省时间。这暗示数据缩放定律存在一定弹性。这类数据集的存在是[《Data Doesn't Do What You Think》（数据并不像你想的那样）](http://www.internalgooglesitescrubbedbyus.com)一文思路的必然结果，而且它们正迅速成为 Google 之外训练的标准做法。这些数据集用合成方法（例如从现有模型中筛出最佳回答）和从其他项目捡漏构建，这两种做法在 Google 都不占主流。**幸运的是，这些高质量数据集是开源的，可以免费使用。**

## 与开源正面竞争是一场必输之局

近期的这些进展对我们的商业战略有着直接而即时的影响。**如果存在免费、高质量、无使用限制的替代品，谁还会为带使用限制的 Google 产品付费？**

而且我们不应指望能追上去。[现代互联网运行在开源之上](https://openuk.uk/wp-content/uploads/2021/07/State-of-Open-Phase-Two.pdf)，这不是没有原因的。开源有一些我们无法复制的显著优势。

## 我们对他们的需要超过他们对我们的需要

对我们技术保密从来都是一个脆弱的主张。Google 研究员在源源不断地跳槽去其他公司，所以我们可以假定，他们知道我们所知道的一切，而且只要这条管道还开着，就会一直如此。

而如今 LLM 前沿研究的成本已经可以负担，守住技术优势变得更加困难。世界各地的研究机构在彼此的工作之上构建，以广度优先的方式探索解空间，其广度远远超过我们自身的能力。我们可以死死守住秘密，任外界的创新稀释其价值；也可以尝试互相学习。

## 个人受许可证的约束远小于公司

这波创新有很多是建立在 Meta 泄露的模型权重之上的。随着[真正开放的模型](https://bigscience.huggingface.co/blog/bloom)越来越好，这迟早会改变，但关键在于他们不必等。「个人使用」提供的法律庇护，加上起诉个人在实操上不现实，意味着个人正在这些技术最炙手可热的时候就能用上它们。

## 自己就是自己的客户，意味着你真正理解使用场景

浏览一下人们在图像生成领域创造的模型，你会发现井喷的创造力，从动漫生成器到 HDR 风景。这些模型的使用者和创造者都深度浸淫在各自的细分流派中，带着我们无法企及的知识深度与共情。

## 拥有生态系统：让开源为我们所用

吊诡的是，这一切中唯一的明确赢家是 Meta。因为泄露的模型是他们的，他们实际上白得了整整一个星球的免费劳动力。既然大多数开源创新都发生在他们的架构之上，没有什么能阻止他们把这些创新直接整合进自己的产品。

**拥有生态系统的价值怎么强调都不为过。**Google 自己就曾在开源产品上成功运用这一范式，比如 Chrome 和 Android。通过拥有创新发生的平台，Google 把自己固化为思想领袖和方向制定者，赢得了塑造那些比自身更宏大的议题叙事的能力。

**我们把模型管得越紧，就让开源替代品越有吸引力。**Google 和 OpenAI 都防御性地倾向于那种能对模型使用方式保持紧控制的发布模式。但这种控制是虚幻的。任何想将 LLM 用于未授权目的的人，大可以在免费可得的模型里随便挑一个用。

Google 应当在开源社区中确立领导者地位，主动融入而非无视更广泛的讨论，以此抢占先机。这可能意味着要迈出一些不舒服的步子，比如公布小型 ULM 变体的模型权重。这必然意味着放弃一部分对我们模型的控制。但这种妥协不可避免。我们不可能既驱动创新，又控制创新。

## 尾声：那 OpenAI 呢？

考虑到 OpenAI 当前的封闭政策，以上这些关于开源的言论可能显得不公平。如果他们不分享，凭什么我们要分享？但事实是，我们早就在通过源源不断被挖走的资深研究员，与他们分享一切。在不堵住这股潮流之前，保密毫无意义。

而归根结底，*OpenAI 无关紧要*。他们在对待开源的姿态上正在犯与我们相同的错误，他们维持领先的能力必然要打上问号。除非改变立场，开源替代品可以也终将令他们黯然失色。至少在这一点上，我们可以先行一步。

# 时间线

### 2023 年 2 月 24 日——LLaMA 发布

[Meta 发布 LLaMA](https://ai.facebook.com/blog/large-language-model-llama-meta-ai/)，开源了代码但没有开放权重。此时 LLaMA 尚未做指令或对话微调。与当下的许多模型一样，它是一个相对较小的模型（提供 7B、13B、33B 和 65B 参数版本），训练时间相对较长，因此相对其体量相当能打。

### 2023 年 3 月 3 日——不可避免的事情发生了

不到一周，[LLaMA 即遭公开泄露](https://www.vice.com/en/article/xgwqgw/facebooks-powerful-large-language-model-leaks-online-4chan-llama)。这对社区的冲击怎么强调都不为过。现有许可证禁止将其用于商业目的，但一夜之间任何人都能上手实验。从这时起，创新开始又猛又快地涌现。

### 2023 年 3 月 12 日——烤面包机上跑语言模型

一周多之后，Artem Andreenko [让模型在 Raspberry Pi 上跑了起来](https://github.com/ggerganov/llama.cpp/issues/58)。此时模型慢到不具实用价值，因为权重必须在内存中反复换入换出。尽管如此，这为一连串的模型小型化努力拉开了帷幕。

### 2023 年 3 月 13 日——笔记本电脑上做微调

第二天，斯坦福发布 [Alpaca](https://crfm.stanford.edu/2023/03/13/alpaca.html)，为 LLaMA 增加了指令微调。不过比权重本身更重要的是 Eric Wang 的 [alpaca-lora](https://github.com/tloen/alpaca-lora) 仓库，它用[低秩微调](https://arxiv.org/abs/2106.09685)「在单张 RTX 4090 上数小时内」完成训练。

一夜之间，任何人都能把模型微调成任何用途，低预算微调项目开启了逐底竞赛。论文们骄傲地宣称总开销只有几百美元。更重要的是，低秩更新可以独立于原始权重单独轻松分发，使其不受 Meta 原始许可证约束。任何人都可以分享并使用它们。

### 2023 年 3 月 18 日——这下快了

Georgi Gerganov [用 4 比特量化](https://github.com/ggerganov/llama.cpp)在 MacBook 的 CPU 上运行 LLaMA。这是第一个快到具备实用性的「无 GPU」方案。

### 2023 年 3 月 19 日——13B 模型与 Bard「打平」

次日，一个跨大学合作项目发布 [Vicuna](https://lmsys.org/blog/2023-03-30-vicuna/)，并使用 GPT-4 驱动的评测对模型输出做定性比较。虽然评测方法存疑，但模型确实比之前的变体明显更好。**训练成本：$300。**

值得注意的是，他们绕过了 ChatGPT API 的使用限制却仍用上了 ChatGPT 的数据——他们只是采集了发布在 [ShareGPT](https://sharegpt.com/) 等网站上那些「令人惊艳」的 ChatGPT 对话样本。

### 2023 年 3 月 25 日——任选你的模型

Nomic 推出 [GPT4All](https://github.com/nomic-ai/gpt4all)，它既是一个[模型](https://s3.amazonaws.com/static.nomic.ai/gpt4all/2023_GPT4All_Technical_Report.pdf)，更重要的是一个[生态系统](https://github.com/nomic-ai/gpt4all#gpt4all-compatibility-ecosystem)。我们第一次看到多个模型（包括 Vicuna）被汇聚到一处。**训练成本：$100。**

### 2023 年 3 月 28 日——开源版 GPT-3

Cerebras（不要与我们内部的 Cerebra 混淆）使用 Chinchilla 隐含的最优算力调度和 [μ-参数化](https://arxiv.org/abs/2203.03466)隐含的最优缩放来训练 GPT-3 架构。它大幅超越现有的 GPT-3 复制品，并代表了 μ-参数化在「实战中」的首次得到确认的使用。这些模型从零训练，意味着社区不再依赖 LLaMA。

### 2023 年 3 月 28 日——一小时多模态训练

借助一种新颖的参数高效微调（PEFT）技术，[LLaMA-Adapter](https://arxiv.org/pdf/2303.16199.pdf) 仅用一小时训练就引入了指令微调和多模态。更厉害的是，只用了 120 万可学习参数。该模型在多模态 ScienceQA 上取得新的 SOTA。

### 2023 年 4 月 3 日——真人分不清 13B 开放模型和 ChatGPT 的差别

伯克利发布 [Koala](https://bair.berkeley.edu/blog/2023/04/03/koala/)，一个完全使用免费可得数据训练的对话模型。

他们迈出了关键一步：测量真实人类在其模型与 ChatGPT 之间的偏好。虽然 ChatGPT 仍略占上风，但超过 50% 的情况下用户要么更偏好 Koala，要么没有偏好差异。**训练成本：$100。**

### 2023 年 4 月 15 日——达到 ChatGPT 水准的开源 RLHF

[Open Assistant](https://open-assistant.io/) 发布了[一个模型，更重要的是一个数据集](https://drive.google.com/file/d/10iR5hKwFqAKhL3umx8muOWSRm7hs5FqX/view)，用于通过 RLHF 做对齐。在人类偏好上，他们的模型已接近（48.3% 对 51.7%）ChatGPT。除 LLaMA 之外，他们还展示该数据集可应用于 Pythia-12B，让人们可以选择用一套完全开放的技术栈来运行模型。而且，由于数据集公开可得，RLHF 对小体量的实验者来说，从遥不可及变成了便宜又容易。
