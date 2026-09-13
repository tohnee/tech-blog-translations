---
title: "Gemini 正式发布：我们最大、能力最强的 AI 模型"
title_en: "Introducing Gemini: our largest and most capable AI model"
source: https://blog.google/innovation-and-ai/technology/ai/google-gemini-ai/
site: google-blog
date: 2023-12-06
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini 正式发布：我们最大、能力最强的 AI 模型

> 原文：[Introducing Gemini: our largest and most capable AI model](https://blog.google/innovation-and-ai/technology/ai/google-gemini-ai/) · Google

*来自 Google 与 Alphabet CEO Sundar Pichai（桑达尔·皮查伊）的一则说明：*

每一次技术变革都是一个推进科学发现、加速人类进步、改善生活的机会。我相信，我们当下正在经历的 AI 转型将是我们这代人一生中最深刻的变革，远超此前向移动或向网络的转变。AI 有潜力为世界各地的人们创造机会——从日常琐事到非凡伟业。它将带来新一轮的创新浪潮与经济进步，以前所未有的规模推动知识、学习、创造力和生产力的发展。

这正是让我兴奋的地方：让 AI 对世界上每一个角落的每一个人都有帮助。

作为一家「AI 优先」的公司，我们的旅程已近八年，前进的步伐仍在不断加快：如今，数百万人正在我们的产品中使用生成式 AI，完成一年前还无法做到的事情——从寻找更复杂问题的答案，到使用新工具进行协作和创作。与此同时，开发者正在使用我们的模型和基础设施构建新的生成式 AI 应用，世界各地的初创公司和企业正借助我们的 AI 工具成长。

这是令人惊叹的势能，然而，我们才刚刚触及可能性的皮毛。

我们以大胆而负责任的方式推进这项工作。这意味着在研究中保持雄心，追求将为人们和社会带来巨大益处的能力，同时内置防护措施，并与政府和专家协作，在 AI 能力不断增强的同时应对风险。我们继续投资最好的工具、基础模型和基础设施，并将其带给我们自己的产品和其他人，这一切都以我们的 [AI 原则](https://ai.google/responsibility/principles/)为准绳。

现在，我们将在旅程中迈出下一步：Gemini——我们迄今能力最强、最通用的模型，在众多领先基准测试中实现了最先进的性能。我们的第一个版本 Gemini 1.0 针对不同规格进行了优化：Ultra、Pro 和 Nano。这些是 Gemini 时代的第一批模型，也是我们今年早些时候组建 Google DeepMind 时所怀愿景的第一次实现。这一全新的模型时代，代表着我们公司有史以来规模最大的科学与工程努力之一。我由衷地为前方的道路、为 Gemini 将为世界各地的人们解锁的机遇感到兴奋。

—— Sundar

## Gemini 正式发布

*作者：Google DeepMind CEO 兼联合创始人 Demis Hassabis（德米斯·哈萨比斯），代表 Gemini 团队*

对我以及我的许多研究同事来说，AI 是毕生工作的重心。从少年时代为电脑游戏编写 AI，到后来作为神经科学研究者试图理解大脑工作机制的岁月，我一直相信：如果我们能制造出更聪明的机器，就能以令人难以置信的方式利用它们造福人类。

「由 AI 以负责任的方式赋能的世界」这一愿景持续驱动着我们在 Google DeepMind 的工作。很长时间以来，我们一直想构建新一代 AI 模型，其灵感来自人们理解和与世界互动的方式。这样的 AI 不太像一段聪明的软件，而更像某种有用且直观的东西——一位专家帮手或助手。

今天，随着 [Gemini 的发布](https://deepmind.google/technologies/gemini)——我们构建过的能力最强、最通用的模型——我们离这一愿景又近了一步。

Gemini 是 Google 各团队大规模协作的成果，其中包括 Google Research 的同事们。它从底层设计之初就是多模态的，这意味着它能够泛化并无缝地理解、处理和组合不同类型的信息，包括文本、代码、音频、图像和视频。

Gemini 也是我们迄今最灵活的模型——能够高效运行在从数据中心到移动设备的各种平台上。其最先进的能力将显著改善开发者和企业客户利用 AI 进行构建和扩展的方式。

我们将第一个版本 Gemini 1.0 针对三种不同规格进行了优化：

- **Gemini Ultra** — 我们最大、能力最强的模型，面向高度复杂的任务。
- **Gemini Pro** — 我们最佳的模型，可在广泛任务中扩展。
- **Gemini Nano** — 我们最高效的模型，面向端侧（on-device）任务。

## 最先进的性能

我们一直在严格测试 Gemini 模型，并在多种多样的任务上评估其性能。从自然的图像、音频和视频理解到数学推理，在大语言模型（LLM）研发中广泛使用的 32 个学术基准测试中，Gemini Ultra 的性能在其中 30 个上超越了当前最先进的结果。

Gemini Ultra 以 90.0% 的成绩成为首个在 [MMLU](https://arxiv.org/abs/2009.03300)（大规模多任务语言理解）上超越人类专家的模型。MMLU 综合数学、物理、历史、法律、医学和伦理学等 57 个学科，同时测试世界知识与问题解决能力。

我们对 MMLU 采用的新基准测试方法，让 Gemini 能够运用其推理能力，在回答难题之前更仔细地思考，与仅凭第一印象作答相比取得了显著提升。

Gemini 在包括文本和编程在内的多个基准测试上超越了最先进的性能。

![图表显示 Gemini Ultra 在常用文本基准测试上的表现，与 GPT-4 对比（在缺少公布数字的情况下使用 API 计算的数字）。](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_final_text_table_amendment_13_12_23.gif)

Gemini Ultra 在新的 [MMMU](https://arxiv.org/abs/2311.16502) 基准测试上也取得了 59.4% 的最先进成绩，该基准由跨越不同领域、需要深思熟虑推理的多模态任务组成。

在我们测试的图像基准上，Gemini Ultra 无需借助光学字符识别（OCR）系统——即从图像中提取文本供后续处理的系统——的辅助，就超越了以往最先进的模型。这些基准凸显了 Gemini 的原生多模态特性，并显示出 Gemini 更复杂推理能力的早期迹象。

更多细节请参阅我们的 [Gemini 技术报告](https://goo.gle/GeminiPaper)。

Gemini 在一系列多模态基准测试上超越了最先进的性能。

![图表显示 Gemini Ultra 在多模态基准测试上与 GPT-4V 的对比，在 GPT-4V 不支持相应能力之处列出了此前的最先进（SOTA）模型。](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_final_multimodal_table_bigger_font_amendment_lines.gif)

## 下一代能力

在此之前，创建多模态模型的标准做法，是为不同模态分别训练组件，再把它们拼接起来，以粗略模仿其中部分功能。这类模型有时能较好地执行某些任务，例如描述图像，但在更具概念性、更复杂的推理上则显得吃力。

我们将 Gemini 设计为原生多模态，从一开始就在不同模态上进行预训练。随后，我们用额外的多模态数据对其进行微调，进一步打磨其效果。这帮助 Gemini 从根本上无缝理解和推理各类输入，远胜现有的多模态模型——而且它的能力在几乎所有领域都是最先进的。

进一步了解 [Gemini 的能力及其工作原理](https://deepmind.google/technologies/gemini)。

### 精密的推理

Gemini 1.0 精密的多模态推理能力可以帮助理解复杂的书面与视觉信息。这使它特别擅长从海量数据中发掘难以辨别的知识。

它通过阅读、过滤和理解信息，从数十万份文档中提取洞见的非凡能力，将帮助从科学到金融的许多领域以数字速度实现新的突破。

### 理解文本、图像、音频及更多

Gemini 1.0 经训练可以同时识别和理解文本、图像、音频等，因此它能更好地理解细微的信息，并回答与复杂主题相关的问题。这使它尤其擅长解释数学和物理等复杂学科的推理过程。

### 先进的编程能力

Gemini 的第一个版本能够理解、解释和生成世界上最流行编程语言（如 Python、Java、C++ 和 Go）的高质量代码。它跨语言工作并推理复杂信息的能力，使其成为全球领先的编程基础模型之一。

Gemini Ultra 在多个编程基准测试中表现出色，其中包括 [HumanEval](https://arxiv.org/abs/2107.03374)（评估编程任务性能的重要行业标准），以及 Natural2Code——我们的内部保留数据集，它使用作者生成的来源而非网络信息。

Gemini 也可以作为更先进编程系统的引擎。两年前，我们发布了 [AlphaCode](https://deepmind.google/discover/blog/competitive-programming-with-alphacode/)，这是首个在编程竞赛中达到竞技水平表现的 AI 代码生成系统。

利用 Gemini 的一个特化版本，我们创建了更先进的代码生成系统 [AlphaCode 2](https://goo.gle/AlphaCode2)，它擅长解决超越编程本身、涉及复杂数学和理论计算机科学的竞赛编程问题。

在与原版 AlphaCode 相同的平台上评估时，AlphaCode 2 表现出巨大的进步，解决的问题数量接近原来的两倍；我们估计它的表现优于 85% 的参赛者——而 AlphaCode 当年的这一比例约为 50%。当程序员通过为代码样例定义某些需要遵循的属性来与 AlphaCode 2 协作时，它的表现还会更好。

我们期待程序员越来越多地把高能力 AI 模型用作协作工具，帮助他们对问题进行推理、提出代码设计并协助实现——从而更快地发布应用、设计更好的服务。

更多细节请参阅我们的 [AlphaCode 2 技术报告](https://goo.gle/AlphaCode2)。

## 更可靠、更可扩展、更高效

我们使用 Google 自主设计的[张量处理单元](https://cloud.google.com/tpu?hl=en)（TPU）v4 和 v5e，在我们为 AI 优化的基础设施上大规模训练了 Gemini 1.0。我们把它设计成训练起来最可靠、最可扩展，服务起来也最高效的模型。

在 TPU 上，Gemini 的运行速度显著快于更早、更小、能力更弱的模型。这些定制设计的 AI 加速器一直是 Google 服务数十亿用户的 AI 产品（如 Search、YouTube、Gmail、Google 地图、Google Play 和 Android）的核心。它们也让世界各地的公司能够经济高效地训练大规模 AI 模型。

今天，我们宣布迄今最强大、最高效、最可扩展的 TPU 系统 [Cloud TPU v5p](https://cloud.google.com/blog/products/ai-machine-learning/introducing-cloud-tpu-v5p-and-ai-hypercomputer)，它专为训练前沿 AI 模型而设计。这一代 TPU 将加速 Gemini 的开发，帮助开发者和企业客户更快地训练大规模生成式 AI 模型，让新产品与新能力更快地触达客户。

Google 数据中心内一排 Cloud TPU v5p AI 加速器超级计算机。

![Google 数据中心内一排 Cloud TPU v5p AI 加速器超级计算机。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/final_keyword_tpu.width-1200.format-webp.webp)

## 以责任与安全为核心构建

在 Google，我们致力于在所做的一切事情中推进大胆而负责任的 AI。在 Google [AI 原则](https://ai.google/responsibility/principles/)和全线产品健全安全政策的基础上，我们正在添加新的防护措施，以应对 Gemini 的多模态能力。在开发的每个阶段，我们都在考虑潜在风险，并努力测试和缓解这些风险。

Gemini 拥有迄今所有 Google AI 模型中最全面的安全评估，包括针对偏见和毒性的评估。我们对网络攻击、说服和自主性等潜在风险领域进行了[新颖的研究](https://deepmind.google/discover/blog/an-early-warning-system-for-novel-ai-risks/)，并应用了 Google Research 一流的[对抗测试技术](https://blog.research.google/2023/11/responsible-ai-at-google-research_16.html)，帮助在 Gemini 部署之前识别关键安全问题。

为了找出我们内部评估方法的盲点，我们正与多元化的外部专家和合作伙伴群体合作，围绕一系列问题对我们的模型进行压力测试。

为了在 Gemini 的训练阶段诊断内容安全问题，并确保其输出遵循我们的政策，我们使用了 [Real Toxicity Prompts](https://allenai.org/data/real-toxicity-prompts) 等基准测试——这是由 Allen Institute for AI 的专家开发的一组从网络抓取、毒性程度不一的 10 万条提示词。关于这项工作的更多细节即将公布。

为了限制伤害，我们构建了专用的安全分类器，用于识别、标记和分拣例如涉及暴力或负面刻板印象的内容。结合强大的过滤器，这种分层方法旨在让 Gemini 对每个人都更安全、更包容。此外，我们将继续应对模型已知的一些挑战，例如事实性、锚定（grounding）、出处归属和交叉佐证。

责任与安全将始终是我们模型开发与部署的核心。这是一项需要协作构建的长期承诺，因此我们正与行业和更广泛的生态系统合作，通过 [MLCommons](https://mlcommons.org/)、[Frontier Model Forum](https://blog.google/outreach-initiatives/public-policy/google-microsoft-openai-anthropic-frontier-model-forum/) [及其](https://blog.google/outreach-initiatives/public-policy/google-microsoft-openai-anthropic-frontier-model-forum/) [AI Safety Fund](https://blog.google/outreach-initiatives/public-policy/google-microsoft-anthropic-open-ai-frontier-model-forum-executive-director/)，以及我们专为帮助缓解公共和私营部门 AI 系统特有安全风险而设计的 [Secure AI Framework（SAIF）](https://blog.google/technology/safety-security/introducing-googles-secure-ai-framework/)等组织，来定义最佳实践并制定安全基准。在开发 Gemini 的过程中，我们将继续与世界各地的研究人员、政府和公民社会组织合作。

## 让全世界用上 Gemini

Gemini 1.0 正在一系列产品和平台上推送：

### Google 产品中的 Gemini Pro

我们正通过 Google 产品把 Gemini 带给数十亿人。

从今天开始，[Bard 将使用 Gemini Pro 的微调版本](https://blog.google/products/bard/google-bard-try-gemini-ai)来实现更先进的推理、规划、理解等能力。这是 Bard 发布以来最大的一次升级。它将以英语在超过 170 个国家和地区可用，我们计划在不久的将来扩展到不同模态，并支持新的语言和地区。

我们也在[把 Gemini 带到 Pixel](https://blog.google/products-and-platforms/devices/pixel/pixel-feature-drop-december-2023/)。Pixel 8 Pro 是首款为运行 Gemini Nano 而打造的智能手机。Gemini Nano 正为 Recorder 应用中的「摘要」（Summarize）等新功能提供支持，并正在 Gboard 的智能回复（Smart Reply）中推送，首先支持 WhatsApp、Line 和 KakaoTalk
[1](#footnote-1)
——明年还会有更多消息应用加入。

在未来几个月里，Gemini 将在更多我们的产品和服务中可用，例如 Search、Ads、Chrome 和 Duet AI。

我们已经开始在 Search 中试验 Gemini：它让我们的[生成式搜索体验](https://labs.google/sge/)（SGE）对用户来说更快，美国的英语延迟降低了 40%，同时质量也有所提升。

### 用 Gemini 构建

从 12 月 13 日开始，开发者和企业客户可以通过 [Google AI Studio](https://ai.google.dev/) 或 [Google Cloud Vertex AI](https://cloud.google.com/vertex-ai) 中的 Gemini API 访问 Gemini Pro。

Google AI Studio 是一款免费的网页端开发者工具，可使用 API 密钥快速构建应用原型并上线。当需要全托管的 AI 平台时，Vertex AI 支持在完全掌控数据的情况下定制 Gemini，并能受益于 Google Cloud 面向企业安全、隐私以及数据治理与合规的额外功能。

Android 开发者也将能够使用 Gemini Nano——我们面向端侧任务最高效的模型——通过 AICore 进行构建。AICore 是 Android 14 中提供的一项全新系统能力，从 Pixel 8 Pro 设备开始支持。注册 [AICore 的抢先预览](https://android-developers.googleblog.com/2023/12/a-new-foundation-for-ai-on-android.html)。

### Gemini Ultra 即将推出

对于 Gemini Ultra，我们目前正在完成广泛的信任与安全检查，包括由可信外部方进行的红队测试，并在广泛推出之前，使用微调和人类反馈强化学习（RLHF）进一步打磨模型。

作为这一过程的一部分，我们会先让选定的客户、开发者、合作伙伴以及安全与责任专家提早试用 Gemini Ultra 并提供反馈，然后于明年初向开发者和企业客户推出。

明年初，我们还将推出 [Bard Advanced](https://blog.google/products/bard/google-bard-try-gemini-ai)——一种全新的尖端 AI 体验，让你可以用上我们最好的模型与能力，首先从 Gemini Ultra 开始。

## Gemini 时代：开启创新的未来

这是 AI 发展中的一个重要里程碑，也是我们在 Google 开启的新时代——我们将继续快速创新，并以负责任的方式推进模型的能力。

到目前为止，我们在 Gemini 上已经取得了巨大进展，我们也正在努力在未来的版本中进一步扩展其能力，包括在规划和记忆方面的进步，以及扩大上下文窗口以处理更多信息、给出更好的回答。

「由 AI 以负责任方式赋能的世界」所蕴含的惊人可能性令我们兴奋不已——那是一个创新的未来，将提升创造力、拓展知识、推进科学，并改变全世界数十亿人的生活与工作方式。
