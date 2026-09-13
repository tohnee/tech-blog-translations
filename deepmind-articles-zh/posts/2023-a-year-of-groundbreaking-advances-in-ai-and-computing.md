---
title: "2023：AI 与计算领域取得突破性进展的一年"
title_en: "2023: A Year of Groundbreaking Advances in AI and Computing"
source: https://deepmind.google/blog/2023-a-year-of-groundbreaking-advances-in-ai-and-computing/
site: deepmind
date: 2023-12-22
crawled: 2026-09-13
translated: 2026-09-13
---

# 2023：AI 与计算领域取得突破性进展的一年

> 原文：[2023: A Year of Groundbreaking Advances in AI and Computing](https://deepmind.google/blog/2023-a-year-of-groundbreaking-advances-in-ai-and-computing/) · Google DeepMind

这是人工智能（AI）研究及其实际应用取得惊人进展的一年。

随着持续的研究把 AI 推向更远处，我们回顾今年 1 月发布的[观点文章](https://ai.google/static/documents/google-why-we-focus-on-ai.pdf)《Why we focus on AI (and to what end)》（我们为何专注 AI，以及目的何在），其中我们写道：

我们致力于在开发和发布有用且有益的应用方面引领并树立标准，践行以人类价值观为基础的伦理原则，并随着我们从研究、经验、用户以及更广泛社群中学习而不断改进我们的方法。

我们还相信，把 AI 做对——对我们而言，这意味着在创新并向人们和社会交付广泛可得的福祉的同时，缓减其风险——必须是一项集体努力，需要我们与其他各方共同参与，包括研究人员、开发者、用户（个人、企业和其他组织）、政府、监管者和公民。

我们坚信，我们专注于大胆而负责任地开发和交付的 AI 驱动创新是有用的、有吸引力的，并有可能帮助和改善世界各地人们的生活——这正是激励我们的力量。

在这篇年度回顾中，我们将回顾 Google Research 和 Google DeepMind 在 2023 年全年把这些段落付诸安全实践的一些努力。

## 产品与技术进展

这一年，生成式 AI 抓住了全世界的目光：它创造出图像、音乐、故事，以及关于一切可以想象之事的引人入胜的对话，其创造力和速度在几年前还几乎难以置信。

2 月，我们[首次推出](https://blog.google/technology/ai/bard-google-ai-search-updates/)[Bard](https://bard.google.com/)——一个你可以用来探索创意点子、简单明了地解释事物的工具。它可以生成文本、翻译语言、撰写各种类型的创意内容等等。

![PaLM2 标志](https://lh3.googleusercontent.com/rh5fK4isbeaUJCxrqFuxqpABIa37Ju9s2_CQBeBMxfewmHYdsOMmlRgMGdtZbfhMcXiXbjqwzAu-rY4zH83w1Ml1VHoOJuf4GlHSCayD-vcWJd8Qjk8=w1440)

5 月，我们在[ Google I/O](https://blog.research.google/2023/05/google-research-at-io-2023.html) 的舞台上见证了数月乃至数年的基础与应用工作成果的发布。其中最重要的是 [PaLM 2](https://ai.google/discover/palm2/)——一个大语言模型（LLM），它集成了计算最优标度、改进的数据集配比和模型架构，在高级推理任务上表现出色。

通过针对不同目的对 PaLM 2 进行微调和指令微调，我们得以把它集成到众多 Google 产品与功能中，包括：

- Bard 的一次更新，使其具备多语言能力。自最初发布以来，Bard 目前已支持[超过 40 种语言、覆盖 230 多个国家和地区](https://support.google.com/bard/answer/13575153?hl=en)；借助[扩展功能](https://blog.google/products/bard/google-bard-new-features-update-sept-2023/)，Bard 可以查找并显示来自 Gmail、Google Maps、YouTube 等日常使用的 Google 工具中的相关信息。
- [Search Generative Experience](https://blog.google/products/search/generative-ai-search/)（SGE），它利用 LLM 重新构想如何组织信息以及如何帮助人们在信息中导航，为核心搜索产品创造了一个更流畅的对话式交互模型。这项工作把搜索引擎体验从主要聚焦于信息检索，扩展为远不止于此的能力——能够检索、综合、创造性生成并延续之前的搜索——同时继续充当用户与其所寻找的网页内容之间的连接点。
- [MusicLM](https://google-research.github.io/seanet/musiclm/examples/)，一个由 [AudioLM](https://ai.googleblog.com/2022/10/audiolm-language-modeling-approach-to.html) 和 [MuLAN](https://arxiv.org/abs/2208.12415) 驱动的文本生成音乐模型，可以从文本、哼唱、图像或视频生成音乐，以及为歌声生成伴奏。
- Duet AI，我们的 AI 驱动协作者，在用户使用 Google Workspace 和 Google Cloud 时提供帮助。例如，[Google Workspace 中的 Duet AI](https://workspace.google.com/blog/product-announcements/duet-ai) 帮助用户写作、创建图像、分析电子表格、起草和总结邮件与聊天消息，以及总结会议。[Google Cloud 中的 Duet AI](https://cloud.google.com/blog/products/application-modernization/introducing-duet-ai-for-google-cloud) 帮助用户编写、部署、扩展和监控应用，并识别和加速解决网络安全威胁。
- 以及许多[其他进展](https://blog.google/technology/developers/google-io-2023-100-announcements/)。

6 月，继去年发布文本生成图像模型 [Imagen](https://imagen.research.google/) 之后，我们发布了 [Imagen Editor](https://blog.research.google/2023/06/imagen-editor-and-editbench-advancing.html)，它提供使用区域掩码和自然语言提示词对生成图像进行交互式编辑的能力，从而对模型输出实现更精确的控制。

![一个四步序列，演示 Imagen Editor 迭代修改一张草地上的小白狗图像。第一步，在狗的身上放置掩码，输入提示词「A red spacesuit with a white star」（一件带有白色星星的红色宇航服）来生成宇航服。第二步，在右侧放置掩码，输入提示词「A rocket made out of cardboard」（一个纸板做的火箭）来生成玩具火箭。第三步，在狗的耳朵上放置掩码，输入提示词「Blue gaming headphones」（蓝色游戏耳机），最终得到这只狗身穿宇航服、戴着耳机、站在纸板火箭旁边的图像。](https://lh3.googleusercontent.com/nndwcFBrH8Wk7V3E0PzBe2cexCy6xvU7zbM9tZGfmbwmVrYY7majZc_kDXEDQNNwchg82L4N-ikQe_Vk3gN4XLCXavDL_u43C-7R2flNFBMBwrjf9g=w1440)

今年晚些时候，我们发布了 Imagen 2，它通过一个基于人类对良好光照、构图、曝光和锐度等品质偏好的专用图像美学模型，改进了输出效果。

10 月，我们推出了一个[帮助人们练习口语并提升语言能力](https://blog.research.google/2023/10/google-search-can-now-help-with-english-speaking-practice.html)的功能。实现该功能的关键技术是与 Google 翻译团队合作开发的一个新型深度学习模型，名为 Deep Aligner。这个单一的新模型使所有受测语言对的对齐质量大幅提升，与基于[隐马尔可夫模型](https://aclanthology.org/C96-2141/)（HMM）的对齐方法相比，平均对齐错误率从 25% 降至 5%。

11 月，我们与 [YouTube](https://blog.youtube/inside-youtube/ai-and-music-experiment/) 合作，宣布推出 [Lyria](https://deepmind.google/discover/blog/transforming-the-future-of-music-creation/)——我们迄今最先进的 AI 音乐生成模型。结合 [YouTube 与音乐行业就 AI 技术开展合作的原则](https://blog.youtube/inside-youtube/partnering-with-the-music-industry-on-ai/)，我们发布了两个旨在为创造力开辟新游乐场的实验：DreamTrack 和音乐 AI 工具。

到了 12 月，我们发布了 [Gemini](https://blog.google/technology/ai/google-gemini-ai/)——我们能力最强、最通用的 AI 模型。Gemini 从底层设计之初就是多模态的，横跨文本、音频、图像和视频。

![「Gemini」一词以浅蓝到紫色的渐变字体书写，字母「i」上方有一颗小小的四角星，背景为黑色，下半部分横贯数条彩色发光的波浪状水平线。](https://lh3.googleusercontent.com/xChvvYgj64SaRm6eFMEXQ_8x0nyVH4u-iY5sC86qGeKuxdE5IrHLQoxfLRjYOsPCxA2iUKZc995Va0uFJ314JvqApKvSt-kP7DTlRJZ82v0Yp3NNBPY=w1440)

我们最初的 Gemini 模型家族有三种不同规格：Nano、Pro 和 Ultra。Nano 模型是我们最小、最高效的模型，用于为 Pixel 等产品中的端侧体验提供动力。Pro 模型能力很强，最适合跨广泛任务扩展。Ultra 模型是我们最大、能力最强的模型，面向高度复杂的任务。

在一份关于 [Gemini 模型](https://deepmind.google/technologies/gemini)的[技术报告](https://storage.googleapis.com/deepmind-media/gemini/gemini_1_report.pdf)中，我们展示了 Gemini Ultra 的性能在 LLM 研发中广泛使用的 32 个学术基准中的 30 个上超越了当前最先进的结果。凭借 90.04% 的得分，Gemini Ultra 成为第一个在 [MMLU](https://arxiv.org/abs/2009.03300) 上超越人类专家的模型，并在新的 [MMMU](https://arxiv.org/abs/2009.03300) 基准上取得了 59.4% 的最先进成绩。

基于 AlphaCode——首个在竞技编程中达到中位数参赛者水平的 AI 系统——我们[推出了 AlphaCode 2](https://storage.googleapis.com/deepmind-media/AlphaCode2/AlphaCode2_Tech_Report.pdf)，由一个 Gemini 专用版本驱动。在与原版 AlphaCode 相同的平台上评测时，我们发现 AlphaCode 2 解出的问题多了 1.7 倍，表现优于 85% 的参赛者。

与此同时，[Bard 迎来了其史上最大升级](https://blog.google/products/bard/google-bard-try-gemini-ai/)，开始使用 Gemini Pro 模型，在理解、总结、推理、编程和规划等方面能力大幅提升。在八个基准中的六个上，Gemini Pro 的表现优于 GPT-3.5，其中包括衡量大型 AI 模型的关键标准之一 MMLU，以及衡量小学数学推理的 [GSM8K](https://huggingface.co/datasets/openai/gsm8k)。Gemini Ultra 将于明年初通过 Bard Advanced——一种全新的尖端 AI 体验——登陆 Bard。

Gemini Pro 也在 [Vertex AI](https://cloud.google.com/blog/products/ai-machine-learning/gemini-support-on-vertex-ai) 上提供——这是 Google Cloud 的端到端 AI 平台，赋能开发者构建能够跨文本、代码、图像和视频处理信息的应用。[Gemini Pro 也于 12 月在 AI Studio 上开放](https://blog.google/technology/ai/gemini-api-developers-cloud/)。

为了最好地展示 Gemini 的一些能力，我们制作了一[系列短视频](https://deepmind.google/technologies/gemini/#hands-on)，讲解 Gemini 如何：

- [解锁科学文献中的洞见](https://www.youtube.com/watch?v=sPiOP_CB54A)
- [在竞技编程中出类拔萃](https://www.youtube.com/watch?v=LvGmVmHv69s&t=1s)
- [处理并理解原始音频](https://www.youtube.com/watch?v=D64QD7Swr3s)
- [解释数学和物理中的推理](https://www.youtube.com/watch?v=K4pX1VAxaAI)
- [推理用户意图以生成定制化体验](https://www.youtube.com/watch?v=v5tRc_5-8G4)

## 机器学习/AI 研究

除了产品与技术方面的进展，我们还在更广泛的机器学习与 AI 研究领域取得了一系列重要突破。

最先进 ML 模型的核心是 Transformer 模型架构，[由 Google 研究人员于 2017 年开发](https://blog.research.google/2017/08/transformer-novel-neural-network.html)。它最初为语言而设计，如今已被证明在[计算机视觉](https://blog.research.google/2020/12/transformers-for-image-recognition-at.html)、[音频](https://deepmind.google/discover/blog/transforming-the-future-of-music-creation/)、[基因组学](https://deepmind.google/discover/blog/a-catalogue-of-genetic-mutations-to-help-pinpoint-the-cause-of-diseases/)、[蛋白质折叠](https://deepmind.google/technologies/alphafold/)等众多领域都有用。今年，我们[扩展视觉 Transformer 规模](https://blog.research.google/2023/03/scaling-vision-transformers-to-22.html)的工作在广泛的视觉任务上展示了最先进的结果，并且对构建[能力更强的机器人](https://blog.research.google/2023/03/palm-e-embodied-multimodal-language.html)也有所帮助。

扩展模型的多面性需要具备执行更高层级、多步推理的能力。今年，我们沿着多条研究路径逼近这一目标。例如，[算法提示词](https://blog.research.google/2023/08/teaching-language-models-to-reason.html)是一种通过演示一串算法步骤来教会语言模型推理的新方法，模型随后可以把这些步骤应用到新的情境中。这一方法把模型在一个中学数学基准上的准确率从 25.9% 提升到了 61.1%。

![](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/Algorithmic_Prompts.gif)

通过提供算法提示词，我们可以借助上下文内学习教会模型算术规则。

在视觉问答领域，在与 UC Berkeley 研究人员的合作中，我们展示了如何通过把视觉模型与一个通过综合程序执行多步推理来回答视觉问题的语言模型相结合，[更好地回答复杂的视觉问题](https://blog.research.google/2023/07/modular-visual-question-answering-via.html)（「马车在马的右边吗？」）。

我们现在正在使用一个[理解软件开发生命周期诸多方面的通用模型](https://blog.research.google/2023/05/large-sequence-models-for-software.html)，自动生成代码评审意见、回复代码评审意见、为代码片段提出性能改进建议（通过学习其他情境中过去的此类改动）、响应编译错误修复代码等等。

在与 Google Maps 团队的一项多年研究合作中，我们得以扩展逆向强化学习的规模，并将其应用于为超过 10 亿用户改进路线建议这一世界级规模的问题。我们的工作最终使全球路线匹配率相对提升了 16–24%，帮助确保路线更符合用户偏好。

我们还持续研究提升机器学习模型推理性能的技术。在[面向计算的神经网络剪枝方法](https://blog.research.google/2023/08/neural-network-pruning-with.html)的工作中，我们设计出了计算上难以处理的最优子集选择问题的一个近似算法，能够从一个图像分类模型中剪除 70% 的边，同时保留几乎全部原始准确率。

在[加速端侧扩散模型](https://blog.research.google/2023/06/speed-is-all-you-need-on-device.html)的工作中，我们还对注意力机制、卷积核和算子融合应用了多种优化，使在设备上运行高质量图像生成模型成为现实；例如，让「一张可爱的周围环绕着鲜花的幼犬照片级高分辨率图像」在智能手机上仅需 12 秒即可生成。

![一个移动设备上 MediaPipe 界面的动画 GIF，逐步展示依据提示词「a photorealistic and high-resolution image of a cute puppy with surrounding flowers」（一张可爱的周围环绕着鲜花的幼犬照片级高分辨率图像）在设备端生成图像的过程。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/YiR-StableDiffusion.gif)

能力强大的语言与多模态模型的进展也让我们的机器人研究受益。我们把分别训练的语言、视觉和机器人控制模型组合成 [PaLM-E](https://blog.research.google/2023/03/palm-e-embodied-multimodal-language.html)——一个面向机器人的具身多模态模型，以及 [Robotic Transformer 2](https://deepmind.google/discover/blog/rt-2-new-model-translates-vision-and-language-into-action/)（RT-2）——一个新颖的视觉-语言-动作（VLA）模型，它[从网络和机器人数据中学习](https://deepmind.google/discover/blog/robocat-a-self-improving-robotic-agent/)，并把知识转化为用于机器人控制的通用指令。

![示意图展示 RT-2 视觉-语言-动作模型如何在互联网规模的 VQA 数据和机器人动作数据上联合微调，随后被部署用于闭环机器人控制任务，比如把一颗草莓放进碗里。](https://lh3.googleusercontent.com/jzFHbKVOSCN0zHZQXGcgqjD5_RErmBz5fPlAfVbBm6WZDGx7vQFFlmeX3IC0xsC37tUrye1nJ7BDmFKYFEdLS6Q-1FsBNk64uEPuEr_PV6Kg_F559OQ=w1440)

RT-2 架构与训练：我们在机器人数据和网络数据上对预训练的视觉-语言模型进行联合微调。得到的模型接收机器人相机图像，直接预测机器人要执行的动作。

此外，我们展示了[语言也可以用来控制四足机器人的步态](https://blog.research.google/2023/08/saytap-language-to-quadrupedal.html)，并探索了[利用语言帮助制定更明确的奖励函数](https://blog.research.google/2023/08/language-to-rewards-for-robotic-skill.html)，以弥合人类语言与机器人动作之间的鸿沟。随后，在 [Barkour](https://blog.research.google/2023/05/barkour-benchmarking-animal-level.html) 中，我们对四足机器人的敏捷性极限进行了基准测试。

## 算法与优化

设计高效、稳健、可扩展的算法依然是高优先级工作。今年，我们的工作包括：应用型与可扩展算法、市场算法、系统效率与优化，以及隐私。

我们推出了 [AlphaDev](https://deepmind.google/discover/blog/alphadev-discovers-faster-sorting-algorithms/)——一个使用强化学习发现改进版计算机科学算法的 AI 系统。AlphaDev 发现了一个更快的排序算法——一种给数据排序的方法——为 LLVM libc++ 排序库带来了改进：对较短序列最高快 70%，对超过 25 万元素的序列约快 1.7%。

我们开发了一个新颖的模型来[预测大图的属性](https://arxiv.org/abs/2305.12322)，使得估算大型程序的性能成为可能。我们发布了一个新数据集 [TPUGraphs](https://arxiv.org/abs/2308.13490)，以加速该领域的[开放研究](https://www.kaggle.com/competitions/predict-ai-model-runtime)，并展示了如何[用现代 ML 提升 ML 效率](https://blog.research.google/2023/12/advancements-in-machine-learning-for.html)。

![散点图，将 TPUGraphs 数据集与其他数据集进行比较，横轴为图的总数，纵轴为平均节点数。](https://lh3.googleusercontent.com/Tf2Z-lCjtkVgPdWMiYCy0VQ7cTzBmlQ1taHSiC05JH9G_AIfahA_WluCt0L7X7r04RtwuWlNZ1T9l65pVfD7sGadW2s7PjmAzrDNR7cIaIX1xTnopM4=w1440)

TPUGraphs 数据集包含 4400 万个图，用于 ML 程序优化。

我们开发了一个新的[负载均衡](https://en.wikipedia.org/wiki/Load_balancing_(computing))算法，用于把查询分发到服务器，名为 [Prequal](https://arxiv.org/abs/2312.10172)，它最小化「在途请求数」与延迟估计的组合。在多个系统中的部署显著节省了 CPU、延迟和 RAM。我们还为带容量预留的经典缓存问题设计了一个新的[分析框架](https://arxiv.org/abs/2305.02508)。

![一张折线图，展示使用 Prequal 带来的 CPU 利用率节省，绘制了归一化 CPU 利用率随时间的变化。](https://lh3.googleusercontent.com/oLYcTypb8b3YkyZ5BxZgWAwMdN8-BFct7PUL93MYTQiREWGl1s0HM8-7Z3mgiJYUDiySoHbw-B77t_XEZGUtjus2M-pvBbkBjZwIVfJCFDosG-iepg=w1440)

归一化 CPU 使用率热力图：08:00 切换到 Prequal。

我们通过开发[计算最小割](https://arxiv.org/abs/2106.05513)、[近似相关聚类](https://arxiv.org/abs/2309.17243)和[大规模并行图聚类](https://arxiv.org/abs/2308.00503)的新技术，改进了聚类和[图算法](https://en.wikipedia.org/wiki/Graph_neural_network)的最先进水平。此外，我们推出了 [TeraHAC](https://arxiv.org/abs/2308.03578)——一种面向万亿边图的新型层次聚类算法；设计了一种[文本聚类算法](https://blog.research.google/2023/11/best-of-both-worlds-achieving.html)，在保持质量的同时实现更好的可扩展性；并设计了最高效的[近似 Chamfer 距离算法](https://arxiv.org/abs/2307.03043)——它是多嵌入模型的标准相似度函数——相比高度优化的精确算法提速超过 50 倍，并可扩展到数十亿点。

我们继续优化 Google 的大型嵌入模型（LEM），它们支撑着我们的许多核心产品和推荐系统。一些新技术包括面向网络级 ML 系统中久经考验的特征表示的 [Unified Embedding](https://arxiv.org/abs/2305.12102)，以及使用注意力机制在训练期间发现高质量稀疏模型架构的 [Sequential Attention](https://arxiv.org/abs/2209.14881)。

在自动出价系统之外，我们还研究了其他复杂环境中的拍卖设计，例如[多次购买机制](https://arxiv.org/abs/2204.01962)、[面向异构竞拍者的拍卖](https://arxiv.org/abs/2207.09429)、[合同设计](https://arxiv.org/abs/2309.10766)，并在[稳健在线出价算法](https://dl.acm.org/doi/10.5555/3618408.3618478)上进行了创新。受生成式 AI 在协作创作（如广告主的联合广告）中应用的启发，我们提出了[一个新颖的 token 拍卖模型](https://arxiv.org/abs/2310.10826)，让 LLM 在协作式 AI 创作中竞标影响力。最后，我们展示了如何在实验设计中[缓解个性化效应](https://dl.acm.org/doi/pdf/10.1145/3580507.3597702)——这种效应可能导致推荐随时间漂移。

Chrome 隐私沙盒（Privacy Sandbox）是 Google Research 与 Chrome 之间多年的合作项目，已公开发布多个 API，包括 [Protected Audience](https://privacysandbox.com/intl/en_us/learning-hub/#protected-audience)、[Topics](https://privacysandbox.com/intl/en_us/learning-hub/#topics) 和 [Attribution Reporting](https://privacysandbox.com/intl/en_us/learning-hub/#attribution-reporting)。这是在支持开放自由的网络生态系统的同时保护用户隐私的重要一步。这些工作得益于关于[再识别风险](https://arxiv.org/abs/2304.07210)、[私密流式计算](https://arxiv.org/abs/2301.05605)、隐私上限与预算的[优化](https://blog.research.google/2023/12/summary-report-optimization-in-privacy.html)、[层次聚合](https://arxiv.org/pdf/2308.13510.pdf)以及带[标签隐私](https://arxiv.org/pdf/2312.05659.pdf)训练模型的基础研究。

## 科学与社会

在不太遥远的将来，AI 应用于科学问题很有可能把某些领域的发现速度提升 10 倍或 100 倍乃至更多，并在生物工程、[材料科学](https://deepmind.google/discover/blog/millions-of-new-materials-discovered-with-deep-learning)、[天气预测](https://deepmind.google/discover/blog/graphcast-ai-model-for-faster-and-more-accurate-global-weather-forecasting/)、[气候预测](https://blog.google/outreach-initiatives/sustainability/google-ai-climate-change-solutions/)、[神经科学](https://blog.research.google/2023/09/google-research-embarks-on-effort-to.html)、[遗传医学](https://blog.research.google/2023/04/an-ml-based-approach-to-better.html)和[医疗保健](https://health.google/health-research/publications/)等多元领域带来重大进展。

### 可持续发展与气候变化

在 [Project Green Light](https://blog.google/outreach-initiatives/sustainability/google-ai-reduce-greenhouse-emissions-project-greenlight/) 中，我们与全球 13 座城市合作，帮助改善十字路口的交通流量、减少走走停停造成的排放。这些合作早期的数据显示，停顿次数最高可减少 30%，排放最高可减少 10%。

在[航迹云（contrails）工作](https://sites.research.google/contrails/)中，我们分析了大规模天气数据、历史卫星图像和过往航班。我们[训练了一个 AI 模型](https://blog.google/technology/ai/ai-airlines-contrails-climate-change/)来预测航迹云的形成位置并相应改道飞机。与美国航空（American Airlines）和 Breakthrough Energy 合作，我们用这一系统演示了航迹云减少 54% 的效果。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

使用 AI 与 GOES-16 卫星图像在美国上空检测到的航迹云。

我们还在开发新颖的技术驱动方法，[帮助社区应对气候变化的影响](https://blog.google/outreach-initiatives/sustainability/google-ai-climate-change-solutions/)。例如，我们[把洪水预报覆盖范围扩展到 80 个国家](https://blog.google/outreach-initiatives/sustainability/flood-hub-ai-flood-forecasting-more-countries/)，直接影响超过 4.6 亿人。我们发起了[多项研究工作](https://blog.research.google/2023/10/looking-back-at-wildfire-research-in.html)以帮助缓解日益严重的野火威胁，包括使用卫星图像[实时追踪野火边界](https://blog.research.google/2023/02/real-time-tracking-of-wildfire.html)，以及帮助面临快速蔓延野火风险的社区[改进应急疏散方案](https://blog.research.google/2023/10/improving-traffic-evacuations-case-study.html)的工作。我们与 American Forests 的[合作](https://www.americanforests.org/article/american-forests-unveils-updates-for-tree-equity-score-tool-to-address-climate-justice/)把我们 [Tree Canopy](https://insights.sustainability.google/places/ChIJVTPokywQkFQRmtVEaUZlJRA/trees?hl=en-US) 项目的数据运用到他们的 [Tree Equity Score](https://treeequityscore.org/) 平台，帮助社区识别并解决树木资源获取不平等的问题。

最后，我们继续为更长时间尺度的天气预测开发更好的模型。在 [MetNet](https://blog.research.google/2020/03/a-neural-weather-model-for-eight-hour.html) 和 [MetNet-2](https://blog.research.google/2021/11/metnet-2-deep-learning-for-12-hour.html) 的基础上，今年 [MetNet-3](https://blog.research.google/2023/11/metnet-3-state-of-art-neural-weather.html) 的工作使我们在最长 24 小时的预报上超越了传统数值天气模拟。在中期全球天气预报领域，我们 [GraphCast](https://deepmind.google/discover/blog/graphcast-ai-model-for-faster-and-more-accurate-global-weather-forecasting/) 的工作在最长 10 天的预报上显示出显著更好的预测准确度，超过了由[欧洲中期天气预报中心](https://www.ecmwf.int/)（ECMWF）产出的最精确业务化确定性预报 [HRES](https://en.wikipedia.org/wiki/Integrated_Forecast_System)。与 ECMWF 合作，我们发布了 [WeatherBench-2](https://blog.research.google/2023/08/weatherbench-2-benchmark-for-next.html)——一个在统一框架中评估天气预报准确度的基准。

GraphCast 的部分预测结果滚动展示 10 天内 700 百帕（约地表以上 3 公里）处的比湿、地表温度和地表风速。

### 健康与生命科学

AI 大幅改进医疗保健流程的潜力是巨大的。我们最初的 [Med-PaLM](https://www.nature.com/articles/s41586-023-06291-2) 模型是首个能够在美国医师执业资格考试中达到及格分数的模型。我们较新的 [Med-PaLM 2 模型](https://blog.google/technology/health/ai-llm-medpalm-research-thecheckup/)又提升了 19%，达到 86.5% 的专家级准确率。这些 [Med-PaLM 模型](https://sites.research.google/med-palm/)基于语言，让临床医生能够就复杂病情提问并展开对话，并作为 [MedLM](https://cloud.google.com/vertex-ai/docs/generative-ai/medlm/overview) 的一部分通过 Google Cloud 向医疗机构[提供](https://cloud.google.com/blog/topics/healthcare-life-sciences/introducing-medlm-for-the-healthcare-industry)。

正如我们的通用语言模型正演进为可处理多种模态，我们最近展示了一项关于[多模态版 Med-PaLM](https://blog.research.google/2023/08/multimodal-medical-ai.html) 的研究，它能够解读医学图像、文本数据及其他模态，并[描述了一条路径](https://arxiv.org/abs/2307.14334)，说明我们如何实现 AI 模型帮助推进真实世界临床护理的激动人心的潜力。

![](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/MedPaLMM.gif)

Med-PaLM M 是一个大型多模态生成模型，能够用同一套模型权重灵活地编码和解读包括临床语言、影像和基因组学在内的生物医学数据。

我们还在研究[如何在临床工作流中最好地运用 AI 模型](https://deepmind.google/discover/blog/codoc-developing-reliable-ai-tools-for-healthcare/)。我们已表明，[将深度学习与可解释性方法相结合](https://blog.research.google/2023/03/learning-from-deep-learning-case-study.html)能为临床医生带来新的洞见。我们还表明，在审慎考虑隐私、安全、公平与伦理的前提下，自监督学习[可以将训练临床相关医学影像模型所需的去标识化数据量减少](https://blog.research.google/2023/04/robust-and-efficient-medical-imaging.html) 3 到 100 倍，降低模型在真实临床环境中落地的门槛。我们还发布了一个[开源移动数据采集平台](https://blog.research.google/2023/11/enabling-large-scale-health-studies-for.html)，供慢性病患者使用，为社群提供工具来开展他们自己的研究。

AI 系统还能在既有形式的医疗数据中发现全新的信号和生物标志物。在[从视网膜图像中发现的新型生物标志物](https://blog.research.google/2023/03/detecting-novel-systemic-biomarkers-in.html)的工作中，我们证明了可以从外部眼部照片预测跨越多个器官系统（如肾、血液、肝）的多种全身性生物标志物。在另一项工作中，我们展示了结合[视网膜图像与基因组信息](https://blog.research.google/2023/04/developing-aging-clock-using-deep.html)有助于识别衰老的一些潜在因素。

在基因组学领域，我们与来自 60 个机构的 119 位科学家合作，绘制了一张[新的人类基因组图谱](https://blog.research.google/2023/05/building-better-pangenomes-to-improve.html)，即泛基因组。这个更公平的泛基因组更好地代表了全球人群的基因组多样性。在我们开创性的 [AlphaFold](https://www.nature.com/articles/s41586-021-03819-2) 工作基础上，今年我们在 [AlphaMissense](https://deepmind.google/discover/blog/a-catalogue-of-genetic-mutations-to-help-pinpoint-the-cause-of-diseases/) 上的工作为 7100 万个可能的[错义变异](https://en.wikipedia.org/wiki/Missense_mutation)中的 89% 提供了「可能致病」或「可能良性」的预测目录。

![下一代 AlphaFold 预测的分子可视化对比图：左侧为血红蛋白亚基 β（HBB）蛋白结构，带有红蓝高亮；右侧为更大的囊性纤维化跨膜传导调节蛋白（CFTR）结构，呈现类似的红蓝带状模型。](https://lh3.googleusercontent.com/2Xv68Pq52z-IeCvsSEOUic5U6rQgarhXaEceGOzHOINkgFJmFhPCc-PYaMkUM8v9EJP7fSGcPcXMWkzKJ4xpkOQQMJocvM2EZrg5hN1FsLtdc-qFgA=w1440)

AlphaMissense 预测叠加在 AlphaFold 预测结构上的示例（红色——预测为致病；蓝色——预测为良性；灰色——不确定）。红点代表已知的致病错义变异，蓝点代表已知的良性变异。**左：** HBB 蛋白。该蛋白的变异可导致镰状细胞贫血。**右：** CFTR 蛋白。该蛋白的变异可导致囊性纤维化。

我们还分享了关于[下一代 AlphaFold 进展的最新情况](https://deepmind.google/discover/blog/a-glimpse-of-the-next-generation-of-alphafold/)。我们的最新模型现在可以为 [Protein Data Bank](https://www.wwpdb.org/)（PDB）中的几乎所有分子生成预测，并常常达到原子级精度。这开启了新的理解，并显著提升了多个关键生物分子类别的预测精度，包括配体（小分子）、蛋白质、核酸（DNA 和 RNA），以及包含翻译后修饰（PTM）的分子。

在神经科学方面，我们[宣布了一项新的合作](https://blog.research.google/2023/09/google-research-embarks-on-effort-to.html)，与哈佛、普林斯顿、美国国立卫生研究院（NIH）等合作，以突触分辨率绘制完整的小鼠大脑，第一阶段将聚焦[海马结构](https://en.wikipedia.org/wiki/Hippocampal_formation)——大脑中负责记忆形成、空间导航和其他重要功能的区域。

### 量子计算

量子计算机有潜力解决科学与工业界的大型现实问题。但要实现这一潜力，它们必须比今天大得多，并且必须可靠地执行经典计算机无法完成的任务。

今年，我们在开发大规模、有用的量子计算机的道路上迈出了重要一步。我们的突破是[量子纠错](https://blog.research.google/2023/02/suppressing-quantum-errors-by-scaling.html)的首次演示，展示了在增加量子比特数量的同时降低错误率是可能的。为了支持现实应用，这些量子比特构建模块必须更可靠地运行，把错误率从目前常见的约 1/103 降到约 1/108。

### 负责任设计

生成式 AI 正在医疗保健、教育、安全、能源、交通、制造和娱乐等广泛领域产生变革性影响。鉴于这些进展，按照我们的 [AI 原则](https://ai.google/responsibility/principles/)设计技术的重要性依然是首要事项。我们最近还发布了[以社会为中心的 AI 的新兴实践](https://blog.research.google/2023/11/emerging-practices-for-society-centered.html)案例研究。在年度 [AI 原则进展报告](https://storage.googleapis.com/gweb-uniblog-publish-prod/documents/2023_Google_AI_Principles_Progress_Update.pdf)中，我们详细介绍了负责任的 AI 研究如何被整合进产品与风险管理流程。

主动的负责任 AI 设计始于识别并记录潜在危害。例如，我们最近[推出了](https://deepmind.google/discover/blog/evaluating-social-and-ethical-risks-from-generative-ai/)一个[三层](https://arxiv.org/abs/2310.11986)的基于情境的框架，用于全面评估 AI 系统的社会与伦理风险。在模型设计阶段，可以借助[负责任的数据集](https://blog.research.google/2023/11/responsible-ai-at-google-research_16.html)来缓解危害。

我们正[与霍华德大学（Howard University）合作](https://blog.google/technology/research/project-elevate-black-voices-google-research/)构建高质量的非裔美国人英语（AAE）数据集，以改进我们的产品，使其为更多人良好服务。我们关于[全球包容性文化表征](https://dl.acm.org/doi/10.1145/3593013.3594016)的研究以及 [Monk 肤色量表](https://skintone.google/)的发布，进一步践行了我们对所有人公平表征的承诺。我们获得的洞见和开发的技术不仅帮助我们改进自己的模型，还为[流行媒体中表征的大规模研究](https://blog.google/intl/en-in/company-news/using-ai-to-study-demographic-representation-in-indian-tv/)提供了动力，启发世界各地更具包容性的内容创作。

![Monk 肤色量表，水平渐变展示 10 个 3D 着色球体，从极浅的粉白色（标注 1）到极深的棕色（标注 10）。](https://lh3.googleusercontent.com/tmaD49ZT0xrT4WZdNPDcoPyD1l7AjtecQlaR0TB99w-4Zj6vdvUcOrn_s5uTZzpVbszMxmeF_JFDlJvk78B1h-NhkQc5hV4mw3qgiVZm6Y-v8JYpeA=w1440)

Monk 肤色（MST）量表。详见 skintone.google。

随着生成式图像模型的进步，[对人物的公平与包容性表征](https://blog.research.google/2023/08/responsible-ai-at-google-research.html)依然是首要优先事项。在开发流程中，我们致力于[放大代表性不足群体的声音、更好地整合社会情境知识](https://blog.research.google/2023/07/using-societal-context-knowledge-to.html)。我们主动使用[分类器与过滤器](https://arxiv.org/pdf/2306.06135.pdf)、[审慎的数据集分析](https://arxiv.org/pdf/2311.17259.pdf)以及模型内缓解措施（如微调、[推理](https://arxiv.org/abs/2310.16523)、[少样本提示](https://arxiv.org/abs/2306.14308)、[数据增强](https://arxiv.org/abs/2310.16959)和[受控解码](https://arxiv.org/abs/2310.17022)）来应对潜在危害与偏见；我们的研究表明，生成式 AI 使[开发更高质量的安全分类器](https://arxiv.org/abs/2302.06541)所需数据大幅减少。我们还发布了一种[用更少数据更好调优模型的强大方法](https://developers.googleblog.com/2023/10/make-with-makersuite-part-2-tuning-llms.html)，让开发者对生成式 AI 中的责任挑战拥有更多掌控。

我们开发了新的[最先进可解释性方法](https://arxiv.org/abs/2303.08114)来识别训练数据对模型行为的作用。通过[将训练数据归因方法与敏捷分类器相结合](https://arxiv.org/abs/2302.06598)，我们发现可以识别被错误标注的训练样本。这使得降低训练数据中的噪声成为可能，进而显著提升模型准确率。

我们发起了多项旨在提升在线内容安全性与透明度的工作。例如，我们推出了 [SynthID](https://deepmind.google/discover/blog/identifying-ai-generated-images-with-synthid/)——一个为 AI 生成图像添加水印并进行识别的工具。SynthID 的水印人眼无法察觉，不会损害图像质量，并且即使经过添加滤镜、改变颜色、以各种有损压缩方案保存等修改，水印仍可被检测到。

我们还推出了 [About This Image](https://blog.google/products/search/google-search-new-fact-checking-features/)，帮助人们评估图像的可信度，显示诸如图像的历史、它在其他页面上的使用情况以及可用的元数据等信息。我们还[探索了其他领域开发的安全方法](https://arxiv.org/abs/2210.03535)，从那些低风险容忍度的成熟场景中学习。

![一张山景中奶牛的动画图像，画面从中间一分为二，对比左侧的「Watermarked（有水印）」版本与右侧的「Non-watermarked（无水印）」版本，展示 SynthID 水印的不可察觉性。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/Watermarking.gif)

SynthID 为 AI 生成图像生成人眼无法察觉的数字水印。

隐私仍然是我们对负责任 AI 承诺的核心。我们持续改进我们最先进的隐私保护学习算法 [DP-FTRL](https://arxiv.org/abs/2103.00039)，开发了 DP 交替最小化算法（[DP-AM](https://arxiv.org/pdf/2310.15454.pdf)）以在严格隐私保护下实现个性化推荐，并定义了一个新的[通用范式](https://blog.research.google/2023/09/differentially-private-median-and-more.html)来降低许多聚合与学习任务的隐私成本。我们还提出了一套[审计差分隐私机器学习系统](https://openreview.net/pdf?id=q15zG9CHi8)的方案。

在应用层面，我们证明了 [DP-SGD 在大模型微调场景下提供了实用的解决方案](https://arxiv.org/pdf/2308.10888.pdf)，并表明 DP 扩散模型生成的图像[对一系列下游任务有用](https://arxiv.org/pdf/2302.13861.pdf)。我们[提出](https://blog.research.google/2023/12/sparsity-preserving-differentially.html)了一种用于大型嵌入模型 DP 训练的新算法，可在 TPU 上高效训练而不牺牲准确率。

我们还与广泛的学术界和产业界研究人员联合，组织了[首届机器遗忘挑战赛](https://unlearning-challenge.github.io/)，以应对为保护个人隐私或权利而遗忘训练图像的场景。我们分享了一种[可提取记忆化](https://arxiv.org/pdf/2311.17035.pdf)的机制，以及让用户对自己的敏感数据拥有更多掌控的[参与式系统](https://arxiv.org/abs/2302.03874)。

我们继续扩展世界上最大的非典型语音录音语料库，在 [Project Euphonia](https://sites.research.google/euphonia/about/) 中把它扩展到超过 100 万条语句，这使我们得以训练一个[通用语音模型](https://blog.research.google/2023/03/universal-speech-model-usm-state-of-art.html)，在真实世界基准上把[非典型语音的识别效果提升 37%](https://blog.research.google/2023/06/responsible-ai-at-google-research-ai.html)。

我们还为患有诵读困难等阅读障碍的学生构建了一个[有声读物推荐系统](https://blog.research.google/2023/08/study-socially-aware-temporally-causal.html)。

### 对抗性测试

我们在对抗性测试方面的工作[吸纳了历史上处于边缘地位的社群的声音](https://blog.research.google/2023/03/responsible-ai-at-google-research.html)。我们与 [Equitable AI Research Round Table](https://arxiv.org/abs/2303.08177)（EARR）等团体合作，确保我们代表使用我们模型的多元社群，并[与外部用户互动](https://dynabench.org/tasks/adversarial-nibbler)来识别生成模型输出中的潜在危害。

我们[设立了一支专门的 Google AI 红队](https://blog.research.google/2023/11/responsible-ai-at-google-research_16.html)，专注于测试 AI 模型与产品的安全、隐私和滥用风险。我们表明，「[投毒](https://arxiv.org/pdf/2302.10149.pdf?isApp=1)」或[对抗样本](https://arxiv.org/pdf/2306.15447.pdf)等攻击可以作用于生产模型，并暴露出[图像](https://www.usenix.org/system/files/usenixsecurity23-carlini.pdf)与[文本生成模型](https://arxiv.org/pdf/2311.17035.pdf)中的记忆化等额外风险。我们还证明了防御此类攻击可能充满挑战，因为仅仅应用防御措施本身就可能引发其他[安全与隐私泄露](https://arxiv.org/pdf/2309.05610.pdf)。我们还引入了针对[极端风险](https://arxiv.org/abs/2305.15324)的模型评估，例如攻击性网络作战能力或强操纵能力。

### 通过工具与教育普及 AI

在推进 ML 和 AI 最先进水平的同时，我们也希望确保人们能够理解 AI 并将其应用于具体问题。我们发布了 [MakerSuite](https://makersuite.google.com/)（现 [Google AI Studio](https://makersuite.google.com)），一个让 AI 开发者快速迭代、构建轻量 AI 应用的网页工具。为帮助 AI 工程师更好地理解和调试 AI，我们发布了 [LIT 1.0](https://pair-code.github.io/lit/)——一个最先进的开源机器学习模型调试器。

[Colab](https://colab.google/)——我们的帮助开发者和学生在浏览器中直接使用强大计算资源的工具——用户数已突破 1000 万。我们刚刚为所有用户免费添加了 [AI 驱动的代码辅助](https://blog.google/technology/ai/democratizing-access-to-ai-enabled-coding-with-colab/)，让 Colab 在数据和 ML 工作流中提供更强大、更整合的体验。

![Google Colab 界面截图，展示导入 pandas、定义一个简单字典、创建 DataFrame 并打印它的 Python 代码。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/pd_explainerror.gif)

最常用的功能之一是「解释错误（Explain error）」——每当用户在 Colab 中遇到执行错误时，代码辅助模型都会提供解释以及一个潜在的修复方法。

为确保 AI 在投入使用时产生准确的知识，我们最近还推出了 [FunSearch](https://deepmind.google/discover/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/)——一种使用演化方法和大语言模型在数学科学中生成可验证真知识的新方法。

对于 AI 工程师和产品设计师，我们正在用生成式 AI 最佳实践更新 [People + AI Guidebook](https://pair.withgoogle.com/guidebook/)，并继续设计 [AI Explorables](https://pair.withgoogle.com/explorables/)，其中包括[模型为何以及如何有时会自信地做出错误预测](https://pair.withgoogle.com/explorables/uncertainty-ood/)。

### 社区参与

我们通过发表大部分研究工作、参与并组织会议，持续推动 AI 与计算机科学领域的发展。今年以来我们已发表了 500 多篇论文，并深度参与 ICML（见 [Google Research](https://blog.research.google/2023/07/google-at-icml-2023.html) 和 [Google DeepMind](https://deepmind.google/discover/blog/google-deepmind-research-at-icml-2023/) 的博文）、ICLR（[Google Research](https://blog.research.google/2023/04/google-at-iclr-2023.html)、[Google DeepMind](https://deepmind.google/discover/blog/deepminds-latest-research-at-iclr-2023/)）、NeurIPS（[Google Research](https://blog.research.google/2023/12/google-at-neurips-2023.html)、[Google DeepMind](https://deepmind.google/discover/blog/google-deepmind-at-neurips-2023/)）、[ICCV](https://blog.research.google/2023/10/google-at-iccv-2023.html)、[CVPR](https://blog.research.google/2023/06/google-at-cvpr-2023.html)、[ACL](https://blog.research.google/2023/07/google-at-acl-2023.html)、[CHI](https://blog.research.google/2023/04/google-at-chi-2023.html) 和 [Interspeech](https://blog.research.google/2023/08/google-at-interspeech-2023.html) 等会议。我们还致力于支持世界各地的研究人员，参加 [Deep Learning Indaba](https://deeplearningindaba.com/2023/google-outreach-mentorship-programme/)、[Khipu](https://khipu.ai/khipu2023/khipu-2023-speakers2023/) 等活动，支持[拉丁美洲的博士奖学金计划](https://blog.google/around-the-globe/google-latin-america/phd-fellowship-research-latin-america/)等等。我们还与来自 33 个学术实验室的合作伙伴合作，汇集 22 种不同机器人类型的数据，创建了 [Open X-Embodiment 数据集和 RT-X 模型](https://deepmind.google/discover/blog/scaling-up-learning-across-many-different-robot-types/)，以更好地推进负责任的 AI 发展。

Google 在 [MLCommons](https://mlcommons.org/) 标准组织下牵头开展了一项行业范围的[ AI 安全基准](https://mlcommons.org/working-groups/ai-safety/ai-safety/)工作，OpenAI、Anthropic、Microsoft、Meta、Hugging Face 等生成式 AI 领域的主要参与者均有参与。我们还与业内其他机构共同[发起](https://blog.google/outreach-initiatives/public-policy/google-microsoft-openai-anthropic-frontier-model-forum/)了[前沿模型论坛](https://www.frontiermodelforum.org/)（FMF），专注于确保前沿 AI 模型的安全与负责任开发。我们与 FMF 伙伴及其他公益组织一道，启动了 1000 万美元的 [AI 安全基金](https://blog.google/outreach-initiatives/public-policy/google-microsoft-anthropic-open-ai-frontier-model-forum-executive-director/)，推动相关工具的持续开发研究，帮助社会有效测试和评估能力最强的 AI 模型。

与 [Google.org](http://google.org/) 紧密合作，我们[与联合国携手](https://blog.google/technology/ai/google-ai-data-un-global-goals/)构建了 [UN Data Commons for the Sustainable Development Goals](https://unstats.un.org/UNSDWebsite/undatacommons/sdgs)——一个追踪 17 项[可持续发展目标](https://sdgs.un.org/goals)各项指标的工具，并[支持](https://globalgoals.withgoogle.com/globalgoals/supported-organizations)来自非政府组织、学术机构和社会企业、旨在[用 AI 加速 SDG 进展](https://blog.google/outreach-initiatives/google-org/httpsbloggoogleoutreach-initiativesgoogle-orgunited-nations-global-goals-google-ai-/)的项目。

本文重点介绍的内容只是我们过去一年研究工作的一小部分。欲了解更多，请访问 [Google Research](https://blog.research.google/) 和 [Google DeepMind](https://deepmind.google/discover/blog/) 博客，以及我们的[出版物列表](https://research.google/pubs/)。

## 未来愿景

随着多模态模型变得更加强大，它们将赋能人们在从科学到教育再到全新知识领域的各个方面取得惊人进展。

进步仍在加速。随着年份推进、产品与研究不断前行，人们将为 AI 找到更多有趣的创造性用途。

以我们开始的地方来结束这篇年度回顾，正如我们在[《Why We Focus on AI (and to what end)》](https://ai.google/static/documents/google-why-we-focus-on-ai.pdf)中所说：

如果能大胆而负责任地追求，我们相信 AI 可以成为一项改变各地人们生活的基础技术——这正是让我们兴奋不已的地方！

本年度回顾同时发布于 [Google Research 博客](https://blog.research.google/2023/12/2023-year-of-groundbreaking-advances-in.html)与 [Google DeepMind 博客](https://deepmind.google/discover/blog/2023-a-year-of-groundbreaking-advances-in-ai-and-computing/)。
