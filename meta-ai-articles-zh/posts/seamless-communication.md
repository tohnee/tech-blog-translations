---
title: "Seamless：一套保留表达力并改进流式传输的 AI 语言翻译模型"
title_en: "Introducing a suite of AI language translation models that preserve expression and improve streaming"
date: 2023-11-30
source: https://ai.meta.com/blog/seamless-communication
crawled: 2026-09-22
translated: 2026-09-22
---

# Seamless：一套保留表达力并改进流式传输的 AI 语言翻译模型

> 原文：[Introducing a suite of AI language translation models that preserve expression and improve streaming](https://ai.meta.com/blog/seamless-communication) · Meta AI（Wayback 存档）

2023 年 11 月 30 日 · 7 分钟阅读

在我们这个日益互联的世界里，语言差异可能成为沟通的障碍，而翻译系统能让不同语言背景的人们更顺畅地分享知识与经验。然而，当今许多这类系统并不能保留语音中那些让人类沟通之所以为「人」的关键要素。更具体地说，传达我们想说什么的不仅仅是我们的措辞，还有我们说话的方式。语调、停顿和重音携带着重要信号，帮助我们传达情感和意图。此外，人类 speech 与翻译对轮替（turn-taking）和时序控制等细微之处十分敏感。举个例子，想想人类口译员是如何工作的：他们在低延迟和准确翻译之间找到恰到好处的平衡。等得太久会扼杀交流的流畅性，而走得太快又会损害翻译的整体质量。能够支持真实对话的翻译系统，应当在这些沟通要素上都表现出色。

今天，我们很高兴地分享 Seamless——首个公开可用、可实时解锁富有表现力的跨语言交流的系统。为了构建 Seamless，我们开发了 SeamlessExpressive（一个在语音到语音翻译中保留表达力的模型）和 SeamlessStreaming（一个以约两秒延迟交付业界领先结果的流式翻译模型）。所有这些模型都构建在我们 8 月发布的基础模型最新版本 SeamlessM4T v2 之上。SeamlessM4T v2 在自动语音识别、语音到语音、语音到文本和文本到语音能力上均有性能提升。与此前富有表现力语音研究的工作相比，SeamlessExpressive 处理了韵律中一些探索不足的方面，如语速和节奏性停顿，同时还保留情感与风格。该模型目前支持英语、西班牙语、德语、法语、意大利语和中文之间的语音到语音翻译并保留这些要素。SeamlessStreaming 通过在说话者仍在讲话时生成翻译，解锁了与说不同语言者的实时对话。与说话者说完句子后才翻译的传统系统不同，SeamlessStreaming 在说话者还在讲话时就开始翻译。这意味着与之对话的人可以以更接近实时的方式听到翻译——延迟只有几秒——而不必等到说话者说完句子。SeamlessStreaming 支持近 100 种输入和输出语言的自动语音识别和语音到文本翻译，以及近 100 种输入语言和 36 种输出语言的语音到语音翻译。秉承我们开放科学的方针，我们公开发布全部四个模型，供研究者在此基础上继续构建。

## 发布元数据、数据与数据对齐工具

今天，除模型之外，我们还在发布元数据、数据及数据对齐工具来协助研究社区，包括：

- SeamlessAlign 扩展版的元数据，在既有 47 万小时之外新增约 11.5 万小时的语音与文本对齐。除了更多小时数，最新版 SeamlessAlign 还覆盖了更广泛的语言（从之前的 37 种扩展到 76 种）。就总体规模和语言覆盖而言，该语料库是迄今最大的公开语音/语音和语音/文本平行语料库。
- SeamlessAlignExpressive 的元数据，即上述数据集以表达力为核心的版本。在这个数据集中，数据对从语义和韵律两个角度都是平行的。SeamlessAlignExpressive 作为基准发布，用于验证我们的表达力对齐方法。为了训练我们的表达力模型，我们将对齐方法应用于一个专有数据集。
- mExpresso 的翻译文本数据——这是 Expresso（一个高质量表达性语音数据集，包含以不同风格呈现的朗读语音和即兴对话）中朗读语音的多语言平行扩展。该文本基准支持对从英语到其他语言的表达性翻译系统进行基准评测。
- 协助研究社区收集更多翻译数据集的工具。具体而言，我们更新了 stopes 库和 SONAR 编码器。借助这些工具，任何人都可以通过平行数据对齐方法，从自己的语音和/或文本单语数据中自动创建多模态翻译对。

## 我们的方法

我们所有的模型都运行在 fairseq2 上——这是我们的序列建模工具包的最新更新。与我们在 SeamlessM4T 上的此前工作类似，fairseq2 为构建流式和表达力更新提供了理想的框架，因为它轻量、易于与 PyTorch 生态的其他库组合，并且拥有更高效的建模与数据加载器 API。UnitY2 这一新架构（带有非自回归 text-to-unit 解码器）对我们的工作也至关重要。在 SeamlessM4T v2 中，我们使用 multitask-UnitY2 来支持文本输入（从 v1 的 multitask-UnitY 升级而来）。我们也在 SeamlessStreaming 和 SeamlessExpressive 中使用了这一架构。作为我们的下一代多任务模型，UnitY2 通过改进的 text-to-unit 模型拥有更出色的语音生成能力。与 SeamlessM4T v1 模型相比，这一实现使文本输出与语音输出之间的一致性得到改善。我们没有像 UnitY 那样使用自回归 text-to-unit 模型，而是使用了非自回归模型。自回归模型基于先前生成的 token 来预测下一个 token。虽然自回归模型能自然地对语音建模，但随着序列长度增加，其扩展性很差，也更容易出现重复退化。非自回归模型预测每个片段的时长，使每个片段可以并行解码。这使它们对长序列更加稳健，我们也看到了相比 UnitY 初始迭代版本的改进。由于该模型本身就预测时长，它更容易适配流式使用场景，因为我们确切地知道每段文本需要生成多少语音，而自回归模型做不到这一点。

Streaming EMMA 是我们的核心流式算法，它让我们能够智能地判断何时已拥有足够的信息来生成下一个语音片段或目标文本。它改进了此前最先进的算法，尤其是对长输入序列（语音到文本或语音到语音翻译正属于这种情况）。此外，该算法允许我们从离线模型进行微调，从而使我们得以受益于 SeamlessM4T v2 基础模型。最后，我们从经验上表明该算法在许多不同语言对之间都能良好泛化，这对流式模型尤其具有挑战性，因为不同语言对的结构可能不同。

## 表达力

保留表达力同样需要一种新方法。我们在 SeamlessM4T v2 中用 PRETSSEL（一个富有表现力的 unit-to-speech 生成器）替换了 unit HiFi-GAN 声码器。PRETSSEL 以源语音为条件生成波形，以传递音调、情绪表达和声音风格特质。我们从 SeamlessM4T v2 初始化模型，以实现高翻译质量——这是语音到语音翻译系统最根本的需求。我们还开发了 Prosody UnitY2，在 SeamlessM4T v2 中集成一个表达力编码器，以恰当的节奏、语速和停顿来引导 unit 生成。此外，我们发布了一套评测工具，用于捕捉表达力这些方面的保留情况。

## 结果

UnitY2 的更新在多种任务上带来了翻译质量的提升。SeamlessM4T v2 在 100 种语言的语音到语音和语音到文本翻译上达到了业界最佳水平。同一个模型在自动语音识别上也平均优于 Whisper v3，尤其是对低资源语言。在语音到文本翻译上，SeamlessM4T v2 相比我们 8 月发布的模型提升了 10%，译入英语时比最强的级联模型提升超过 17%。在语音到语音翻译上，译入英语时 SeamlessM4T v2 比 SeamlessM4T（v1）提升超过 15%，从英语译出时提升 25%。在其他任务上，SeamlessM4T v2 在文本到文本翻译方面与 No Language Left Behind（NLLB）持平；在自动语音识别（ASR）上平均与 MMS 持平（在中高资源语言上表现更好，而 MMS 在低资源语言上表现更好），并且比最近发布的 Whisper-Large-v3 提升超过 25%。在文本到语音翻译这一零样本任务上，SeamlessM4T v2 译入英语时与强大的级联模型持平，并且译出英语时比这些基线提升 16%。

我们将 SeamlessExpressive 与一个级联的语音到文本加文本到语音流水线进行了对比，其中语音到文本来自 SeamlessM4T v2，文本到语音来自一个支持声音风格和情感迁移的强大开源跨语言文本到语音系统。结果表明，SeamlessExpressive 对源语音中的噪声更稳定——输出语音保持了很高的内容翻译质量，并更好地保留了风格和语速。SeamlessStreaming 则在语音到语音翻译上实现了业界领先的低延迟质量。

## 我们如何负责任地构建 AI 翻译系统：毒性缓解

准确性在翻译系统中至为重要。翻译错误或非预期的毒性可能在不讲同一种语言的两个人之间造成误解。秉承我们对构建负责任 AI 的承诺，我们进一步研究了幻觉毒性（hallucinated toxicity）问题。我们的工作聚焦于 SeamlessM4T v2——它是 SeamlessStreaming、SeamlessExpressive 以及统一的 Seamless 模型的基础。幻觉毒性的主要根源往往在于训练数据。训练样本可能带有噪声，且毒性分布不均衡。例如，输入语言侧和目标语言侧可能因失误而含有不同量的毒性词。在训练之前，我们丢弃了任何表现出这种失衡迹象的样本。然而，过滤只是一种被动手段，并不能完全防止幻觉毒性。这一次我们更进一步，实现了一种主动缓解这种现象的新方法。在翻译生成过程中，我们的系统通过自动检测生成的毒性词并显示错误消息来减少毒性生成。这在推理时即可生效，不需要对翻译模型做任何微调。通过这种方式，我们在保持翻译质量的同时显著减少了新增毒性。最后，在我们过去毒性与偏见评估工作的基础上，我们用一个全新的幻觉毒性检测工具扩展了评测框架。以前的方法依赖中间转录模型（ASR），而现在我们能够直接在语音信号中检测毒性。这在毒性并非通过单个词语、而是通过语调或整体风格传达的情况下非常有用。这让我们得以更精确地把握模型潜在的毒性画像。机器翻译的负责任 AI 方面仍需更多研究，但我们相信这些措施让我们更接近实现更安全、更以人为中心的翻译系统。

## 音频水印

AI 工具可以帮助世界更紧密地联系在一起，但同样重要的是我们要纳入防范冒充和其他形式滥用风险的措施。与被动判别器相比，我们的水印方法提供了更高水平的可靠性——随着语音保留技术的进步，被动判别器在区分合成语音与人声方面正变得越来越低效。水印会主动嵌入一个人耳无法察觉、但仍可由检测器模型在音频中检测到的信号。通过这一水印，可以准确追溯音频的来源。这有助于通过建立可验证的音频溯源来促进语音保留技术的负责任使用，并帮助防止潜在滥用。除了纯粹的检测准确性，我们的水印解决方案还需要对各种攻击保持稳健。例如，恶意行为者可能尝试通过添加噪声、回声或过滤某些频率来修改音频，以稀释水印并绕过检测。我们在广泛的攻击类型上测试了我们的水印方法，结果表明它比当前最先进的方法更稳健。我们的方法还能在音频中将 AI 生成的片段精确定位到帧级别，超越了此前最先进方法（仅提供一秒的分辨率）。与任何基于神经网络的安全机制一样，水印模型可以被单独微调以遗忘其核心属性。然而，出于翻译目的对 SeamlessExpressive 和 Seamless 进行微调不会涉及对水印模型本身的任何更新，后者对翻译质量不起任何作用。

## 开放我们的技术

我们在 Seamless 上取得的突破表明，通用实时翻译器的梦想并非科幻——它正在成为技术现实。我们邀请每个人试用我们的表达性翻译演示。我们也在向研究社区开放我们的代码、模型和数据。

试用表达性翻译演示 / 下载代码、模型和数据 / 阅读论文 / 访问 Seamless 网站

这篇博文得益于以下同事的工作：Loïc Barrault、Yu-An Chung、Mariano Coria Meglioli、David Dale、Ning Dong、Mark Duppenthaler、Paul-Ambroise Duquenne、Brian Ellis、Hady Elsahar、Justin Haaheim、John Hoffman、Min-Jae Hwang、Hirofumi Inaguma、Christopher Klaiber、Ilia Kulikov、Pengwei Li、Daniel Licht、Jean Maillard、Ruslan Mavlyutov、Alice Rakotoarison、Kaushik Ram Sadagopan、Abinesh Ramakrishnan、Tuan Tran、Guillaume Wenzek、Yilin Yang、Ethan Ye、Ivan Evtimov、Pierre Fernandez、Cynthia Gao、Prangthip Hansanti、Elahe Kalbassi、Amanda Kallet、Artyom Kozhevnikov、Gabriel Mejia、Robin San Roman、Christophe Touret、Corinne Wong、Carleigh Wood、Bokai Yu、Pierre Andrews、Can Balioglu、Peng-Jen Chen、Marta R. Costa-jussà、Maha Elbayad、Hongyu Gong、Francisco Guzmán、Kevin Heffernan、Somya Jain、Justine Kao、Ann Lee、Xutai Ma、Alex Mourachko、Benjamin Peloquin、Juan Pino、Sravya Popuri、Christophe Ropers、Safiyyah Saleem、Holger Schwenk、Anna Sun、Paden Tomasello、Changhan Wang、Jeff Wang、Skyler Wang 和 Mary Williamson。
