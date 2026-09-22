---
title: "Step-Audio 2 技术报告"
title_en: "Step-Audio 2 Technical Report"
arxiv: 2507.16632
date: 2025-07-22
source: https://arxiv.org/abs/2507.16632
crawled: 2026-09-22
translated: 2026-09-22
---

# Step-Audio 2 技术报告

> 原文：[Step-Audio 2 Technical Report](https://arxiv.org/abs/2507.16632) · 阶跃星辰 StepFun arXiv

StepFun 音频团队

###### 摘要

本文提出 Step-Audio 2，一个面向工业级音频理解与语音对话的端到端多模态大语言模型。通过整合潜在音频编码器与以推理为中心的强化学习（RL），Step-Audio 2 在自动语音识别（ASR）与音频理解上取得了出色的表现。为实现真正的端到端语音对话，Step-Audio 2 将离散音频 token 的生成纳入语言建模，显著增强了其对说话风格、情感等副语言信息的响应能力。为有效利用真实世界数据中丰富的文本与声学知识，Step-Audio 2 集成了检索增强生成（RAG），并能够调用网络搜索等外部工具以缓解幻觉、调用音频搜索以切换音色。Step-Audio 2 基于数百万小时的语音与音频数据训练而成，在多样化的对话场景中兼具智能与表现力。评测结果表明，相较于其他开源与商业方案，Step-Audio 2 在多个音频理解与对话基准上取得了最先进（SoTA）的性能。更多信息请访问 <https://github.com/stepfun-ai/Step-Audio2>。

|  |
| --- |
|  |

图 1：GPT-4o Audio¹、Kimi-Audio²、Qwen-Omni³ 与 Step-Audio 2 在多个基准上的性能比较。

> 注 1：GPT-4o Audio 的 ASR 任务通过 gpt-4o-transcribe 评测，其余任务通过官方 API 的 gpt-4o-audio-preview-2025-06-03 评测。
> 注 2：Kimi-Audio 在翻译评测中被排除，因为它始终忽略提示词。
> 注 3：Qwen-Omni 在 MMAU 与语音到文本翻译任务上使用 Qwen2.5-Omni 评测，其余任务通过官方 API 的 qwen-omni-turbo-2025-03-26 评测。

## 1 引言

随着大语言模型与音频处理技术的快速发展，大型音频语言模型（LALM）已在各类语音与音频处理任务中展现出相对传统方法的显著优势。GPT-4o 率先问世，开创了无需中间文本转换的端到端语音交互的先河。随后，众多开源 LALM（[9, 13, 16, 18, 21, 31, 32, 49, 71, 72, 74, 77]）相继涌现，推动了多模态大语言模型在各类语音与音频领域的能力进步。在这些方法中，Qwen-Audio（[12]）与 Qwen2-Audio（[13]）对音频进行分析并针对语音指令生成文本回应；Qwen2.5-Omni（[74]）实现了 thinker-talker 架构，以支持语音对话中的全双工输入输出。近期，Kimi-Audio（[18]）在多个语音与音频理解基准上取得了亮眼成绩。与此同时，我们推出了 Step-Audio（[32]）与 Step-Audio-AQAA（[31]），它们是最早通过离散音频 token 在 1300 亿参数规模上统一语音理解与生成的 LALM。

然而，现有 LALM 在实现自然且智能的语音交互方面仍面临挑战。早期的 LALM，如 Spirit LM（[49]）与 GLM-4-Voice（[77]），主要关注将语音输入中的语义信息对齐到文本模态，忽略了对于意图理解同样至关重要的副语言信息。尽管 Qwen-Audio（[12]）、Qwen2-Audio（[13]）与 Audio Flamingo 系列（[24, 25, 43]）等 LALM 已能理解此类信息，它们通常只生成文本输出，未能进一步利用这一能力在语音对话中产生连贯且富有表现力的回应。此外，受多模态建模复杂性的影响，现有 LALM 频繁出现幻觉，可选音色与说话风格有限（[16, 18]），且缺乏对真实世界文本与声学知识的访问能力。

为解决这些问题并迈向下一代多模态大语言模型，我们提出 Step-Audio 2——一个具备工业级音频感知与语音交互能力的端到端大型音频语言模型。Step-Audio 2 直接以原始音频作为输入，输出离散的文本与音频 token，参数量少于 Step-Audio（[32]）。除了捕捉语音中的语义信息外，该模型还能理解音频中的副语言与非发声信息。借助思维链（CoT）推理与强化学习（RL），Step-Audio 2 进一步利用这类多模态信息，生成与不同对话场景相连贯、富有表现力的语音回应。为了让模型扎根于真实世界知识，Step-Audio 2 引入了检索增强生成（RAG），并具备使用网络搜索、音频搜索等多种外部工具的能力，以提供更可靠、更具表现力的回应。具体而言，我们提出了音频搜索这一 LALM 独有的工具，支持通过语音指令进行无缝语音检索，使模型能够基于检索到的语音切换音色与说话风格。

为了确保模型在多样化对话场景中的智能性与表现力，我们精心设计了多阶段训练策略，在 6800 亿 token 的文本数据与 800 万小时的真实及合成音频数据上训练 Step-Audio 2。图 1 所示的评测结果表明，Step-Audio 2 在一系列音频任务上取得最先进性能，包括多语言自动语音识别（ASR）、音频理解、语音到语音翻译与语音到语音对话。Step-Audio 2 的典型用法如图 2 所示。

![Refer to caption](2507.16632v3/usage.png)

图 2：Step-Audio 2 在各类语音对话场景中的应用示意。

## 2 相关工作

### 2.1 语音与音频理解

大语言模型（[4, 29, 50, 51]）的最新进展已将其应用扩展到广泛的语音与音频理解任务，例如音频描述、声音事件检测、自动语音识别、音频分类以及音频驱动的创意生成。一种主流方法（[13, 17, 27, 28, 48, 61]）是将语音编码器与轻量级可训练适配器配对，将音频特征投影到与 LLM 兼容的文本嵌入空间。在此基础上，近期研究进一步探索如何融入情感、语调与说话人风格等副语言信息，使 LLM 超越纯粹的语言理解。例如，ParalinGPT（[48]）专注于通过整合连续语音嵌入来增强强大的文本语言模型，使其能够捕捉情感与韵律等副语言信号。SALMONN（[61]）采用多模态策略，冻结语音编码器 Whisper（[53]）与 BEATs（[10]），并通过窗口级 Q-Former 将其输出连接到 LLM，实现语言与声学特征的联合建模。Seed-ASR（[5]）将基于 LUISE 的语音表示与指令及上下文相结合，利用上下文感知的 SFT 捕捉语义信息。AudioPaLM（[57]）结合 PaLM-2（[2]）与 AudioLM（[7]），将语言知识与说话人身份、语调等副语言特征统一起来。基于 LLM 的方法（[12, 13]）日益依赖 Wav2Vec（[3]）、HuBERT（[30]）、Whisper（[53]）与 WavLM（[11]）等预训练音频编码器从语音中提取丰富的语义表示。与此同时，LLM 中存储的海量文本知识与上下文推理能力，可以为理解任务提供宝贵的语义引导。

### 2.2 文本到语音合成

文本到语音（TTS）技术近年来取得了显著进步，从传统的拼接式与统计参数方法（[52, 55, 59, 68]）演进为基于编解码器（codec）的 TTS 系统。编解码器语言模型利用语音编解码器提取语音的离散表示（[15, 16, 36, 60, 73, 76, 81, 82]），并采用自回归（[18, 80]）或掩码语言模型（[67]）来预测相应的语音 token，随后通过编解码器声码器将这些 token 合成为波形。VALL-E（[64]）标志着该领域的重大突破，它使用自回归模型生成粗粒度编解码码，再用非自回归模型生成细粒度编码。与从音素预测声学 token 且需要转写文本的 VALL-E 不同，SPEAR-TTS（[40]）采用带自监督音频提示的两阶段架构，只需 3 秒语音即可克隆未见过的人声。SparkTTS（[65]）提出 BiCodec，一种单流语音编解码器，将语言学内容编码为紧凑的语义 token，将说话人特征编码为定长的全局 token。TorToiseTTS（[6]）、CosyVoice（[20]）、CosyVoice 2（[19]）、MiniMax-Speech（[79]）与 SEED-TTS（[1]）等方法不依赖非自回归模型预测残差离散码，而是采用扩散或 flow-matching 技术作为第二阶段，重建富含细粒度声学与语义细节的梅尔频谱或连续表示。近期工作 Kimi-Audio（[18]）结合 Whisper 特征与语义 token 以实现高效建模，配备双头结构、flow-matching 解码器与 BigVGAN（[46]），实现低延迟、富有表现力的合成。

### 2.3 语音到语音翻译

语音到语音翻译（S2ST）是消除跨语言沟通障碍的关键技术。传统 S2ST 系统（[62, 70]）通常采用由自动语音识别（ASR）、机器翻译（MT）与 TTS 模块组成的级联流水线。早期研究（[38, 39, 44, 45]）已转向绕过中间文本表示的直接方法，旨在降低延迟并更好地保留韵律与说话人特征。直接 S2ST 方法主要分为两类：语音到频谱图翻译与语音到单元翻译，二者都直接从源语音生成目标语音表示而不依赖文本转写。前一类的代表是 Translatotron（[38]），首个将源语音直接翻译为目标频谱图的端到端模型。Translatotron 2（[39]）通过两遍解码机制（[45]）进一步提升了翻译质量。相比之下，语音到单元模型预测的是离散声学 token 而非频谱图，这些 token 通常由 HuBERT（[30]）或 WavLM（[11]）等自监督语音编码器提取。例如，TransVIP（[44]）采用联合编码器-解码器架构，在首层生成目标文本与残差矢量量化（RVQ）码，再由非因果语言模型在后续层中精炼 RVQ 预测。

### 2.4 语音到文本与语音到语音对话

根据 LLM 能否直接理解并生成语音表示，现有系统可分为端到端大型音频语言模型与级联式大型音频语言模型。前者在统一框架内直接建模音频输入与输出，而后者依赖由独立 ASR、LLM 与 TTS 组件构成的模块化流水线。传统语音到文本与语音到语音系统通常采用级联架构，例如 AudioGPT（[33]）与 Spoken-LLM（[47]）。然而，ASR + LLM + TTS 流水线会带来高延迟与模块失配问题，这激发了人们对统一端到端架构的兴趣，以实现更快、更无缝的集成。这一方向的重要里程碑是 GPT-4o（[34]），它支持直接的端到端语音交互而无需中间文本转换。近期，多种面向语音到语音对话的端到端 LALM（[16, 21, 71, 72, 74]）相继出现。例如，Moshi（[16]）借助可同时生成文本与音频 token 的 RQ-Transformer 提升效率。类似地，Mini-Omni（[71]）采用与 MusicGen（[14]）类似的策略并行生成语音与文本回应，相比交错生成设计实现了更低的首 token 延迟。LUCY（[22]）在 Mini-Omni 架构基础上，针对语音生成中的情感表现力、自然度与信息量进行了增强，利用精心制作的合成数据并优化训练与解码流水线，以处理多轮对话与函数调用场景。Mini-Omni2（[71]）进一步扩展了 Mini-Omni 框架，集成了多模态理解与全双工交互能力。LLaMA-Omni（[21]）引入基于联结主义时序分类（CTC）的流式非自回归语音解码器，无需逐步预测即可直接高效地生成离散音频 token。Freeze-Omni（[66]）则在训练期间冻结 LLM 参数，在保留其原有能力的同时，通过流式处理与解码器集成实现低延迟语音到语音交互。Qwen2.5-Omni（[74]）通过 thinker-talker 架构支持多模态输入与文本-语音同步输出，并使用 TMRoPE 通过显式时间编码改善音画同步。

![Refer to caption](2507.16632v3/architecture5.png)

图 3：Step-Audio 2 的架构。

## 3 方法

### 3.1 架构

与我们之前的 Step-Audio（[32]）不同，Step-Audio 2 进一步将音频 token 的生成纳入语言建模，实现了端到端的音频感知与生成。如图 3 所示，Step-Audio 2 由音频编码器、音频适配器、LLM 解码器与音频 detokenizer（解码器）组成。

音频编码器在多种语音与音频理解任务上预训练，包括 ASR、说话人年龄与性别预测、音频事件检测等。音频编码器的输出帧率为 25 Hz，并在整个训练过程中保持冻结。我们采用下采样率为 2 的音频适配器将音频编码器连接到 LLM，从而将音频编码器的输出帧率降至 12.5 Hz。

LLM 解码器直接以来自音频适配器的潜在音频特征作为输入，输出离散文本与音频 token 的交错序列。我们采用 CosyVoice 2（[19]）的 tokenizer 作为音频 tokenizer。文本与音频 token 以固定比例交错（[31, 32, 77]），并在末尾填充以满足该比例。随后，音频 token 从交错序列中被提取出来，交由音频 detokenizer 生成输出波形。输入音频特征与输出交错序列随后会被作为历史信息预填充到下一轮对话中。

为了提供更准确的回应并扩展交互能力，我们设计了一组工具，支持以显式或隐式的语音输入直接检索音频、当前日期时间、天气预报与网页内容。值得注意的是，我们提出了音频搜索工具，这是一个新颖的工具，配备一个包含数十万条语音及其对应转写与描述的语音库。借助音频搜索检索到的语音，Step-Audio 2 能够模仿说话风格或根据该语音切换音色。推理时，检索到的信息会被附加在输入音频特征之后，再生成语音输出。

与 Step-Audio（[32]）和 Step-Audio-AQAA（[31]）类似，Step-Audio 2 的音频 detokenizer 同样由 Flow Matching 模块与 HiFi-GAN（[42]）声码器组成。Flow Matching 模块从输出的音频 token 生成梅尔频谱，声码器再将梅尔频谱转换为波形。对于 Flow Matching，我们在 transformer 块内的每个自注意力模块之后加入一层基于 CNN 的编码器层，并在 20 万小时的高质量语音上训练模型。这一增强显著提升了其梅尔频谱重建能力，使发音准确度与音色相似度均获得大幅提升。

Step-Audio 2 采用与 Step-Audio（[32]）和 Step-Audio-AQAA（[31]）相同的部署基础设施，包括用于过滤输入语音的语音活动检测（VAD）模块，并实现了实时语音对话。

### 3.2 预训练

Step-Audio 2 模型由一个文本 LLM 初始化，随后在 1.356T token 的文本与音频数据上持续预训练 21 天。

我们首先使用 1000 亿 token 的 ASR 数据，促进适配器内语音与文本特征空间的有效对齐。在此阶段，音频编码器与 LLM 均被冻结，仅训练适配器。我们以 8,192 的序列长度训练 12K 步，学习率从 $10^{-4}$ 衰减至 $2\times 10^{-5}$。

接着，我们为文本 LLM 的 tokenizer 扩充 6.6K 个音频 token。为了恰当嵌入新音频 token 并保留模型的文本能力，模型随后在 1280 亿 token 的文本数据与 1280 亿 token 的音频数据上训练。具体而言，音频数据包括 800 亿、320 亿与 160 亿 token 的 TTS、语音到语音对话与语句级文本-语音交错续写数据。序列长度提升至 16,384。LLM、适配器、embedding 层与输出层的学习率分别设为 $2\times 10^{-5}$、$5\times 10^{-5}$、$5\times 10^{-5}$ 与 $4\times 10^{-5}$。

然后，我们进入主要的预训练过程，在另外 8000 亿 token 的文本与音频数据上继续训练。我们将学习率统一为 $2\times 10^{-5}$，并使用 4000 亿 token 的文本数据，以及 420 亿、1200 亿、80 亿、300 亿、50 亿、450 亿与 1500 亿 token 的 ASR、TTS、语音到文本翻译、文本到语音翻译、语音到文本续写、语句级文本-语音交错续写与语音到语音对话数据。

最后，我们使用 2000 亿 token 的高质量文本与音频数据引入更丰富的任务并对模型进行退火（cooldown）。我们使用 246 亿、124 亿、24 亿与 36 亿 token 的音频数据，分别用于多语言与方言 ASR、TTS、副语言信息理解以及语音到文本翻译。此外，我们开发了对话式语音合成流水线，为语音到语音翻译、语句级文本-语音交错对话与语音到语音对话合成了 60 亿、150 亿与 360 亿 token 的音频数据。为确保合成语音的发声多样性，该系统参考了一个约包含 5 万名独特说话人的语音库。我们以 1000 亿 token 的高质量文本数据来平衡音频数据，学习率从 $2\times 10^{-5}$ 衰减至 $5\times 10^{-6}$。

经过这一全面的预训练流程，模型在保持初始文本 LLM 所赋予的文本性能的同时，获得了强大的音频理解与生成能力。

### 3.3 监督微调

随后，我们执行大规模、多任务的监督微调（SFT）流程（[69]），以指导模型在流畅对话中遵循人类意图并掌握核心任务。我们从开源与专有数据中筛选音频数据，以确保广泛的覆盖面与高质量。模型在 40 亿 token 的文本与音频数据上训练一个 epoch，学习率从 $10^{-5}$ 衰减至 $10^{-6}$。

具体而言，我们利用 GigaSpeech（[8]）、WenetSpeech（[78]）及其他内部数据等大规模语料，增强模型在多语言与多方言 ASR 场景下的表现。我们将音频事件分类与音频描述的既有数据集（如 AudioSet（[23]）与 AudioCaps（[41]））重新组织为语音问答对，用于音频理解。为了捕捉语义之外的副语言信息，我们引入了细致的语音描述（speech captioning）任务并构建了内部数据集，要求模型生成涵盖 11 个副语言与环境方面的完整文本描述。

TTS 方面，我们采用内部收集的高质量专业标注数据。语音到语音翻译方面，我们使用 CoVoST 2（[63]）数据集中的中译英与英译中子集。

经典文本到文本对话方面，我们利用高质量的内部文本数据。随后使用多个 LLM 将这些文本对话改写为更自然、更口语化的对话脚本。我们在生成的脚本中随机插入情感与语速指令，以实现基础的情感与说话风格控制。然后使用我们的对话合成流水线将这些脚本合成为语音对话。

我们为每类外部工具构建了约 1K 条文本对话脚本。在这些脚本中，带有显式或隐式工具调用意图的指令及其对应的话术被插入到常见对话里。随后使用我们的对话合成流水线将这些脚本合成为语音对话。

此外，我们在 SFT 期间构建并使用了两个以推理为中心的数据集，用于为后续强化学习过程冷启动。首先，我们通过混合来自 AudioSet 与 AudioCaps 的多段音频构建了一个数据集，以在复杂声学场景中实现稳健的音频理解。为了更好地应对与回应语音对话中的副语言信息，我们基于文本 LLM 生成的带有恰当情感描述的对话脚本，利用对话合成流水线合成了一个语音对话数据集。随后，借助一个具备推理能力的文本 LLM，根据音频混合配方或生成的对话脚本，产出带有显式逐步推理轨迹的问答对。

### 3.4 强化学习

为增强模型在音频理解与语音交互中的推理能力，我们实施了多阶段强化学习策略。我们利用 SFT 阶段构建的以推理为中心的数据集，采用两阶段近端策略优化（PPO）（[54]）来优化推理效率，以满足实时音频交互的需求。第一阶段采用二元奖励函数，将思考序列长度限制在预设的最大值以内。该奖励函数对恰当简洁（既非空也非过长）的推理赋值 1，否则赋值 0。训练进行 60 轮迭代，全局 batch size 为 64，actor 学习率为 $1\times 10^{-6}$，critic 学习率为 $2.5\times 10^{-6}$。第二阶段从二元奖励过渡到习得的偏好评分，利用训练好的奖励模型评估回应质量。该阶段在保持相同 batch size 与学习率设置的情况下再进行 120 轮迭代。最后，我们采用组相对策略优化（GRPO）（[54]）进行 400 轮迭代，以进一步提升模型的音频感知能力。

## 4 评测

### 4.1 自动语音识别

作为音频理解与语音交互最关键的组成部分，我们首先评估模型的自动语音识别能力。我们在六个中文测试集、四个英文测试集、三个多语种测试集（日语、粤语、阿拉伯语）以及六个内部中文方言与带口音普通话测试集上评估 Step-Audio 2。

作为对比，我们选用开源与商业领域中表现最佳的模型作为基线，包括 Doubao LLM ASR¹、GPT-4o Transcribe²、Kimi-Audio（[18]）与 Qwen-Omni。我们优先选择 GPT-4o Transcribe 而非 GPT-4o Audio，因为前者能提供更强的结果。值得注意的是，Doubao LLM ASR 与 GPT-4o Transcribe 代表了性能领先的专业 ASR 系统。

> 注 1：Doubao LLM ASR 指 <https://www.volcengine.com/docs/6561/1354868>。
> 注 2：GPT-4o Transcribe 通过其官方 API 的最新模型 gpt-4o-transcribe 进行评测。

我们在不指定语言的情况下评估所有模型³，并将结果汇总于表 1。Step-Audio 2 在通用英语与中文识别上超越了现有开源与商业 ASR 模型，在英语测试集上取得 3.14% 的平均词错误率（WER），在中文测试集上取得 3.08% 的平均字错误率（CER）。此外，Step-Audio 2 在阿拉伯语与日语识别上取得与 GPT-4o Transcribe 相当的结果，在粤语识别上与 Qwen-Omni 相当，展现了其多语言语音识别能力。另外，在 4 个内部中文带口音普通话测试集与 2 个方言测试集上，Step-Audio 2 取得了最低的平均 CER。这些结果凸显了 Step-Audio 2 在理解语音语义信息方面的优越性。

> 注 3：我们在不指定语言的情况下评测以确保公平比较。值得注意的是，Qwen-Omni 缺乏与语言无关的测试方式，指定语言可能会得到更好的结果。

表 1：Doubao LLM ASR、GPT-4o Transcribe、Kimi-Audio、Qwen-Omni 与 Step-Audio 2 在多个 ASR 测试集上的字错误率（中文、粤语与日语）与词错误率（阿拉伯语与英语）比较。N/A 表示不支持该语言。

| 类别 | 测试集 | Doubao  LLM ASR | GPT-4o  Transcribe | Kimi-  Audio | Qwen-  Omni | Step-  Audio 2 |
| --- | --- | --- | --- | --- | --- | --- |
| 英语 | Common Voice | 9.20 | 9.30 | 7.83 | 8.33 | 5.95 |
| FLEURS English | 7.22 | 2.71 | 4.47 | 5.05 | 3.03 |
| LibriSpeech clean | 2.92 | 1.75 | 1.49 | 2.93 | 1.17 |
| LibriSpeech other | 5.32 | 4.23 | 2.91 | 5.07 | 2.42 |
| 平均 | 6.17 | 4.50 | 4.18 | 5.35 | 3.14 |
| 中文 | AISHELL | 0.98 | 3.52 | 0.64 | 1.17 | 0.63 |
| AISHELL-2 | 3.10 | 4.26 | 2.67 | 2.40 | 2.10 |
| FLEURS Chinese | 2.92 | 2.62 | 2.91 | 7.01 | 2.68 |
| KeSpeech phase1 | 6.48 | 26.80 | 5.11 | 6.45 | 3.63 |
| WenetSpeech meeting | 4.90 | 31.40 | 5.21 | 6.61 | 4.75 |
| WenetSpeech net | 4.46 | 15.71 | 5.93 | 5.24 | 4.67 |
| 平均 | 3.81 | 14.05 | 3.75 | 4.81 | 3.08 |
|  | FLEURS Arabian | N/A | 11.72 | N/A | 25.13 | 14.22 |
| 多语种 | Common Voice yue | 9.20 | 11.10 | 38.90 | 7.89 | 7.90 |
|  | FLEURS Japanese | N/A | 3.27 | N/A | 10.49 | 3.18 |
|  | 安徽口音 | 8.83 | 50.55 | 22.17 | 18.73 | 10.61 |
|  | 广东口音 | 4.99 | 7.83 | 3.76 | 4.03 | 3.81 |
|  | 广西口音 | 3.37 | 7.09 | 4.29 | 3.35 | 4.11 |
| 内部 | 山西口音 | 20.26 | 55.03 | 34.71 | 25.95 | 12.44 |
|  | 四川方言 | 3.01 | 32.85 | 5.26 | 5.61 | 4.35 |
|  | 上海方言 | 47.49 | 89.58 | 82.90 | 58.74 | 17.77 |
|  | 平均 | 14.66 | 40.49 | 25.52 | 19.40 | 8.85 |

### 4.2 副语言信息理解

接下来，我们评估 Step-Audio 2 对语音中语义信息之外的副语言信息的理解能力。为此，我们推出 StepEval-Audio-Paralinguistic，一个通过单轮问答评估模型对 11 个维度副语言信息理解能力的语音到语音基准。

StepEval-Audio-Paralinguistic 包含 550 个语音样本，均匀分布于 11 个任务。我们最初从公开播客录音中为其中 8 个任务收集了 400 条中文语音片段，涵盖性别、年龄、音色、情感、音高、节奏、语速、说话风格以及发声活动预测或描述。针对声音事件、场景与人声的检测或描述，我们分别从 AudioSet（[23]）、CochlScene（[35]）与 VocalSound（[26]）中选取 50 条事件相关、50 条环境声与 50 条人声。所有原始录音均短于 30 秒，并统一重采样至 24,000 Hz，标注由专业团队以开放集自然语言提供。

随后，我们基于每个任务的真实标注，用文本 LLM 生成文本问答。对于前 8 个任务，我们以输入语音作为提示克隆合成问题语音，并随机将问题拼接在原始语音之前或之后。对于其余 3 个任务，我们在拼接问题之前进一步将这些音频与合成语音混合，构建更具挑战性的测试样本。

我们还为 StepEval-Audio-Paralinguistic 建立了自动评测协议：先使用 ASR 将模型输出转写为文本，再由文本 LLM 进行自动评判。更多信息以及完整的 StepEval-Audio-Paralinguistic 测试集与评测代码可在 <https://github.com/stepfun-ai/Step-Audio2> 获取，以推动副语言信息理解的进一步研究。

我们使用 StepEval-Audio-Paralinguistic 基准评估了 GPT-4o Audio、Kimi-Audio、Qwen-Omni、Step-Audio-AQAA 与 Step-Audio 2，结果见表 2。实验结果凸显了 Step-Audio 2 在理解各类副语言信息上的全面能力，取得 83.09 的平均准确率，显著超越其他基线模型。

表 2：GPT-4o Audio、Kimi-Audio、Qwen-Omni、Step-Audio-AQAA 与 Step-Audio 2 在 StepEval-Audio-Paralinguistic 上的比较。

| 模型 | 平均 | 性别 | 年龄 | 音色 | 场景 | 事件 |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-4o Audio | 43.45 | 18 | 42 | 34 | 22 | 14 |
| Kimi-Audio | 49.64 | 94 | 50 | 10 | 30 | 48 |
| Qwen-Omni | 44.18 | 40 | 50 | 16 | 28 | 42 |
| Step-Audio-AQAA | 36.91 | 70 | 66 | 18 | 14 | 14 |
| Step-Audio 2 | 83.09 | 100 | 96 | 82 | 78 | 60 |
| 模型 | 情感 | 音高 | 节奏 | 语速 | 风格 | 人声 |
| GPT-4o Audio | 82 | 40 | 60 | 58 | 64 | 44 |
| Kimi-Audio | 66 | 56 | 40 | 44 | 54 | 54 |
| Qwen-Omni | 76 | 32 | 54 | 50 | 50 | 48 |
| Step-Audio-AQAA | 40 | 38 | 48 | 54 | 44 | 0 |
| Step-Audio 2 | 86 | 82 | 86 | 88 | 88 | 68 |

### 4.3 音频理解

随后，我们使用最新版本的 MMAU 基准（[58]）⁴评估 Step-Audio 2 在声音、语音与音乐上的通用音频理解能力。

> 注 4：MMAU v05.15.25 test-mini。

作为基线，我们采用 Audio Flamingo 3、Gemini 2.5 Pro、GPT-4o Audio、Kimi-Audio、Omni-R1（[56]）、Qwen2.5-Omni 与 Step-Audio-AQAA。Audio Flamingo 3、Omni-R1 与 Qwen2.5-Omni 的结果取自其原始论文，Gemini 2.5 Pro 的结果取自 MMAU 官网。由于 MMAU 基准近期更新，我们重新评测了 GPT-4o Audio、Kimi-Audio 与 Step-Audio-AQAA。

结果汇总于表 3。Step-Audio 2 取得 78.0 的最高平均分，其后是 Omni-R1 与 Audio Flamingo，二者均为音频理解方面的专门方法。具体而言，Step-Audio 2 在声音与语音赛道取得最佳结果，在音乐赛道与最佳结果持平，展现了其在不同音频领域的多样性与稳健性。

表 3：Audio Flamingo 3、Gemini 2.5 Pro、GPT-4o Audio、Kimi-Audio、Omni-R1、Qwen2.5-Omni、Step-Audio-AQAA 与 Step-Audio 2 在 MMAU 上的比较。

| 模型 | 平均 | 声音 | 语音 | 音乐 |
| --- | --- | --- | --- | --- |
| Audio Flamingo 3 | 73.1 | 76.9 | 66.1 | 73.9 |
| Gemini 2.5 Pro | 71.6 | 75.1 | 71.5 | 68.3 |
| GPT-4o Audio | 58.1 | 58.0 | 64.6 | 51.8 |
| Kimi-Audio | 69.6 | 79.0 | 65.5 | 64.4 |
| Omni-R1 | 77.0 | 81.7 | 76.0 | 73.4 |
| Qwen2.5-Omni | 71.5 | 78.1 | 70.6 | 65.9 |
| Step-Audio-AQAA | 49.7 | 50.5 | 51.4 | 47.3 |
| Step-Audio 2 | 78.0 | 83.5 | 76.9 | 73.7 |

### 4.4 语音翻译

我们使用两个基准评估模型的中英双向语音翻译能力：CoVoST 2（[63]）上的语音到文本翻译（S2TT）与 CVSS（[37]）上的语音到语音翻译（S2ST）。此外，CoVoST 2 上使用 Qwen2.5-Omni 的报告结果，而 CVSS 上采用 Qwen-Omni 作为基线。Kimi-Audio 被排除在外，因为它始终忽略提示词、执行 ASR 而非翻译。以 BLEU 作为评测指标，表 4 的结果表明 Step-Audio 2 在中英双向翻译中表现优越，在 CoVoST 2 与 CVSS 测试集上均取得最高平均分。

表 4：GPT-4o Audio、Qwen2.5-Omni、Qwen-Omni、Step-Audio-AQAA 与 Step-Audio 2 在语音到文本与语音到语音翻译上的 BLEU 分数比较。

| 模型 | CoVoST 2（语音到文本翻译） | | |
| --- | --- | --- | --- |
| 平均 | 英译中 | 中译英 |
| GPT-4o Audio | 29.61 | 40.20 | 19.01 |
| Qwen2.5-Omni | 35.40 | 41.40 | 29.40 |
| Step-Audio-AQAA | 28.57 | 37.71 | 19.43 |
| Step-Audio 2 | 39.26 | 49.01 | 29.51 |
| 模型 | CVSS（语音到语音翻译） | | |
| 平均 | 英译中 | 中译英 |
| GPT-4o Audio | 23.68 | 20.07 | 27.29 |
| Qwen-Omni | 15.35 | 8.04 | 22.66 |
| Step-Audio-AQAA | 27.36 | 30.74 | 23.98 |
| Step-Audio 2 | 30.87 | 34.83 | 26.92 |

### 4.5 工具调用

为填补语音对话中工具调用合适测试集的空白，我们推出 StepEval-Audio-Toolcall，一个在中文语音对话下评估模型工具调用、选择与参数提取能力的测试集。

我们使用文本 LLM 为每类工具生成 200 个多轮对话脚本。每个脚本包含 3-6 轮输入与输出，其中先前的轮次可能包含也可能不包含工具调用话术，但最后一轮输入必须包含对某个外部工具的调用意图。随后，我们为每类工具配以等量的负样本以平衡数据，负样本的最后一轮语音输入要么没有工具调用意图，要么意图调用其他类型的工具。接着，我们用对话合成流水线将这些脚本合成为语音。我们提出一套自动评测协议，使用 Qwen3-32B 自动检查输出与工具调用话术。我们在 <https://github.com/stepfun-ai/Step-Audio2> 发布了 StepEval-Audio-Toolcall，包括原始脚本、合成的语音对话及相应评测脚本。

尽管目前没有其他 LALM 提供自定义工具调用，我们仍采用 Qwen3-32B 作为基线，以说明 Step-Audio 2 与文本 LLM 相比如何管理外部工具。如表 5 所示，即使以语音作为输入，Step-Audio 2 的工具调用准确率也与文本 LLM 相当。值得注意的是，Step-Audio 2 在准确调用我们创新的音频搜索工具上显著优于 Qwen3-32B，凸显了其作为多模态 LLM 相对文本 LLM 的独特优势。

表 5：Step-Audio 2 与 Qwen3-32B 在 StepEval-Audio-Toolcall 上的比较。†Qwen3-32B 使用文本输入评测。‡日期和时间工具无参数。

| 模型 | 目标 | 指标 | 音频搜索 | 日期和时间‡ | 天气 | 网络搜索 |
| --- | --- | --- | --- | --- | --- | --- |
|  | 触发 | 准确率 / 召回率 | 67.5 / 98.5 | 98.4 / 100.0 | 90.1 / 100.0 | 86.8 / 98.5 |
| Qwen3-32B† | 类型 | 准确率 | 100.0 | 100.0 | 98.5 | 98.5 |
|  | 参数 | 准确率 | 100.0 | N/A | 100.0 | 100.0 |
|  | 触发 | 准确率 / 召回率 | 86.8 / 99.5 | 96.9 / 98.4 | 92.2 / 100.0 | 88.4 / 95.5 |
| Step-Audio 2 | 类型 | 准确率 | 100.0 | 100.0 | 90.5 | 98.4 |
|  | 参数 | 准确率 | 100.0 | N/A | 100.0 | 100.0 |

### 4.6 语音到语音对话

最后，我们采用 URO-Bench（[75]）评估 Step-Audio 2 与其他开源及商业 LALM，包括 GPT-4o Audio、Kimi-Audio、Qwen-Omni 与 Step-Audio-AQAA。URO-Bench 由两个难度赛道上的多个数据集组成，评估模型的理解、推理与口语对话能力，例如 ASR、指令遵循、常识知识、数学，以及语音自然度、情感与说话风格表达。我们遵循 URO-Bench 的 ASR 中介流程进行评测，采用 Whisper 做 ASR、GPT-4o-mini 做自动评判。

如表 6 所示，Step-Audio 2 在中文语音到语音对话场景中显著超越现有大型音频语言模型（包括 GPT-4o Audio），在基础赛道取得 83.32 的最高平均分，在专业赛道取得 68.25 的最高平均分。在英语语音到语音对话中，虽然 Step-Audio 2 略逊于 GPT-4o Audio，但其结果极具竞争力，超越了其他方法。

表 6：GPT-4o Audio、Kimi-Audio、Qwen-Omni、Step-Audio-AQAA 与 Step-Audio 2 在 URO-Bench 上的比较。U. R. O. 分别代表理解（Understanding）、推理（Reasoning）与口语对话（Oral conversation）。

| 模型 | 语言 | 基础 | | | | 专业 | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 平均 | U. | R. | O. | 平均 | U. | R. | O. |
| GPT-4o Audio | 中文 | 78.59 | 89.40 | 65.48 | 85.24 | 67.10 | 70.60 | 57.22 | 70.20 |
| Kimi-Audio | 73.59 | 79.34 | 64.66 | 79.75 | 66.07 | 60.44 | 59.29 | 76.21 |
| Qwen-Omni | 68.98 | 59.66 | 69.74 | 77.27 | 59.11 | 59.01 | 59.82 | 58.74 |
| Step-Audio-AQAA | 74.71 | 87.61 | 59.63 | 81.93 | 65.61 | 74.76 | 47.29 | 68.97 |
| Step-Audio 2 | 83.32 | 91.05 | 75.45 | 86.08 | 68.25 | 74.78 | 63.18 | 65.10 |
| GPT-4o Audio | 英语 | 84.54 | 90.18 | 75.90 | 90.41 | 67.51 | 60.65 | 64.36 | 78.46 |
| Kimi-Audio | 60.04 | 83.36 | 42.31 | 60.36 | 49.79 | 50.32 | 40.59 | 56.04 |
| Qwen-Omni | 70.58 | 66.29 | 69.62 | 76.16 | 50.99 | 44.51 | 63.88 | 49.41 |
| Step-Audio-AQAA | 71.11 | 90.15 | 56.12 | 72.06 | 52.01 | 44.25 | 54.54 | 59.81 |
| Step-Audio 2 | 83.90 | 92.72 | 76.51 | 84.92 | 66.07 | 64.86 | 67.75 | 66.33 |

## 5 结论

我们推出 Step-Audio 2，一个面向企业级语音与音频理解以及智能语音交互的端到端大型音频语言模型。Step-Audio 2 利用潜在音频编码器与强化学习增强其语音与音频理解能力。此外，通过将离散音频 token 的生成纳入语言建模，Step-Audio 2 实现了真正的端到端语音交互，并提升了其对说话风格、情感等副语言信息的响应能力。Step-Audio 2 还能够利用网络搜索与音频搜索等外部工具进行多模态 RAG。Step-Audio 2 基于 800 万小时的语音与音频训练而成，在 ASR、音频理解、语音翻译与通用语音对话等多种任务上展现出最先进的性能，超越了开源与商业方案。

## 参考文献

- [1]
  Philip Anastassiou et al.
  “Seed-tts: A family of high-quality versatile speech generation models”
  In *arXiv preprint arXiv:2406.02430*, 2024
- [2]
  Rohan Anil et al.
  “PaLM 2 Technical Report”, 2023
  arXiv: <https://arxiv.org/abs/2305.10403>
- [3]
  Alexei Baevski, Henry Zhou, Abdelrahman Mohamed and Michael Auli
  “wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations”, 2020
  arXiv: <https://arxiv.org/abs/2006.11477>
- [4]
  Jinze Bai et al.
  “Qwen Technical Report”, 2023
  arXiv: <https://arxiv.org/abs/2309.16609>
- [5]
  Ye Bai et al.
  “Seed-asr: Understanding diverse speech and contexts with llm-based speech recognition”
  In *arXiv preprint arXiv:2407.04675*, 2024
- [6]
  James Betker
  “Better speech synthesis through scaling”, 2023
  arXiv: <https://arxiv.org/abs/2305.07243>
- [7]
  Zalán Borsos et al.
  “Audiolm: a language modeling approach to audio generation”
  In *IEEE/ACM transactions on audio, speech, and language processing* 31
  IEEE, 2023, pp. 2523–2533
- [8]
  Guoguo Chen et al.
  “GigaSpeech: An Evolving, Multi-Domain ASR Corpus with 10,000 Hours of Transcribed Audio”
  In *Interspeech 2021*
  ISCA, 2021
  DOI: [10.21437/interspeech.2021-1965](https://dx.doi.org/10.21437/interspeech.2021-1965)
- [9]
  Qian Chen et al.
  “Minmo: A multimodal large language model for seamless voice interaction”
  In *arXiv preprint arXiv:2501.06282*, 2025
- [10]
  Sanyuan Chen et al.
  “BEATs: Audio Pre-Training with Acoustic Tokenizers”, 2022
  arXiv: <https://arxiv.org/abs/2212.09058>
- [11]
  Sanyuan Chen et al.
  “WavLM: Large-Scale Self-Supervised Pre-Training for Full Stack Speech Processing”
  In *IEEE Journal of Selected Topics in Signal Processing* 16.6
  Institute of ElectricalElectronics Engineers (IEEE), 2022, pp. 1505–1518
  DOI: [10.1109/jstsp.2022.3188113](https://dx.doi.org/10.1109/jstsp.2022.3188113)
- [12]
  Yunfei Chu et al.
  “Qwen-audio: Advancing universal audio understanding via unified large-scale audio-language models”
  In *arXiv preprint arXiv:2311.07919*, 2023
- [13]
  Yunfei Chu et al.
  “Qwen2-audio technical report”
  In *arXiv preprint arXiv:2407.10759*, 2024
- [14]
  Jade Copet et al.
  “Simple and Controllable Music Generation”, 2024
  arXiv: <https://arxiv.org/abs/2306.05284>
- [15]
  Alexandre Défossez, Jade Copet, Gabriel Synnaeve and Yossi Adi
  “High fidelity neural audio compression”
  In *arXiv preprint arXiv:2210.13438*, 2022
- [16]
  Alexandre Défossez et al.
  “Moshi: a speech-text foundation model for real-time dialogue”
  In *arXiv preprint arXiv:2410.00037*, 2024
- [17]
  Soham Deshmukh, Benjamin Elizalde, Rita Singh and Huaming Wang
  “Pengi: An audio language model for audio tasks”
  In *Advances in Neural Information Processing Systems* 36, 2023, pp. 18090–18108
- [18]
  Ding Ding et al.
  “Kimi-audio technical report”
  In *arXiv preprint arXiv:2504.18425*, 2025
- [19]
  Zhihao Du et al.
  “Cosyvoice 2: Scalable streaming speech synthesis with large language models”
  In *arXiv preprint arXiv:2412.10117*, 2024
- [20]
  Zhihao Du et al.
  “CosyVoice: A Scalable Multilingual Zero-shot Text-to-speech Synthesizer based on Supervised Semantic Tokens”, 2024
  arXiv: <https://arxiv.org/abs/2407.05407>
- [21]
  Qingkai Fang et al.
  “Llama-omni: Seamless speech interaction with large language models”
  In *arXiv preprint arXiv:2409.06666*, 2024
- [22]
  Heting Gao et al.
  “LUCY: Linguistic Understanding and Control Yielding Early Stage of Her”, 2025
  arXiv: <https://arxiv.org/abs/2501.16327>
- [23]
  Jort. Gemmeke et al.
  “Audio Set: An ontology and human-labeled dataset for audio events”
  In *2017 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, 2017, pp. 776–780
  DOI: [10.1109/ICASSP.2017.7952261](https://dx.doi.org/10.1109/ICASSP.2017.7952261)
- [24]
  Sreyan Ghosh et al.
  “Audio Flamingo 2: An Audio-Language Model with Long-Audio Understanding and Expert Reasoning Abilities”, 2025
  arXiv: <https://arxiv.org/abs/2503.03983>
- [25]
  Arushi Goel et al.
  “Audio Flamingo 3: Advancing Audio Intelligence with Fully Open Large Audio Language Models”, 2025
  arXiv: <https://arxiv.org/abs/2507.08128>
- [26]
  Yuan Gong, Jin Yu and James Glass
  “Vocalsound: A Dataset for Improving Human Vocal Sounds Recognition”
  In *ICASSP 2022 - 2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, 2022, pp. 151–155
  DOI: [10.1109/ICASSP43922.2022.9746828](https://dx.doi.org/10.1109/ICASSP43922.2022.9746828)
- [27]
  Yuan Gong et al.
  “Joint audio and speech understanding”
  In *2023 IEEE Automatic Speech Recognition and Understanding Workshop (ASRU)*, 2023, pp. 1–8
  IEEE
- [28]
  Yuan Gong et al.
  “Listen, think, and understand”
  In *arXiv preprint arXiv:2305.10790*, 2023
- [29]
  Aaron Grattafiori et al.
  “The Llama 3 Herd of Models”, 2024
  arXiv: <https://arxiv.org/abs/2407.21783>
- [30]
  Wei-Ning Hsu et al.
  “HuBERT: Self-Supervised Speech Representation Learning by Masked Prediction of Hidden Units”, 2021
  arXiv: <https://arxiv.org/abs/2106.07447>
- [31]
  Ailin Huang et al.
  “Step-Audio-AQAA: a Fully End-to-End Expressive Large Audio Language Model”
  In *arXiv preprint arXiv:2506.08967*, 2025
- [32]
  Ailin Huang et al.
  “Step-audio: Unified understanding and generation in intelligent speech interaction”
  In *arXiv preprint arXiv:2502.11946*, 2025
- [33]
  Rongjie Huang et al.
  “Audiogpt: Understanding and generating speech, music, sound, and talking head”
  In *Proceedings of the AAAI Conference on Artificial Intelligence* 38.21, 2024, pp. 23802–23804
- [34]
  Aaron Hurst et al.
  “Gpt-4o system card”
  In *arXiv preprint arXiv:2410.21276*, 2024
- [35]
  Il-Young Jeong and Jeongsoo Park
  “CochlScene: Acquisition of acoustic scene data using crowdsourcing”
  In *2022 Asia-Pacific Signal and Information Processing Association Annual Summit and Conference (APSIPA ASC)*, 2022, pp. 17–21
  DOI: [10.23919/APSIPAASC55919.2022.9979822](https://dx.doi.org/10.23919/APSIPAASC55919.2022.9979822)
- [36]
  Shengpeng Ji et al.
  “Wavtokenizer: an efficient acoustic discrete codec tokenizer for audio language modeling”
  In *arXiv preprint arXiv:2408.16532*, 2024
- [37]
  Ye Jia, Michelle Ramanovich, Quan Wang and Heiga Zen
  “CVSS Corpus and Massively Multilingual Speech-to-Speech Translation”, 2022
  arXiv: <https://arxiv.org/abs/2201.03713>
- [38]
  Ye Jia et al.
  “Direct speech-to-speech translation with a sequence-to-sequence model”
  In *arXiv preprint arXiv:1904.06037*, 2019
- [39]
  Ye Jia, Michelle Ramanovich, Tal Remez and Roi Pomerantz
  “Translatotron 2: High-quality direct speech-to-speech translation with voice preservation”
  In *International conference on machine learning*, 2022, pp. 10120–10134
  PMLR
- [40]
  Eugene Kharitonov et al.
  “Speak, Read and Prompt: High-Fidelity Text-to-Speech with Minimal Supervision”, 2023
  arXiv: <https://arxiv.org/abs/2302.03540>
- [41]
  Chris Kim, Byeongchang Kim, Hyunmin Lee and Gunhee Kim
  “Audiocaps: Generating captions for audios in the wild”
  In *Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)*, 2019, pp. 119–132
- [42]
  Jungil Kong, Jaehyeon Kim and Jaekyoung Bae
  “HiFi-GAN: Generative Adversarial Networks for Efficient and High Fidelity Speech Synthesis”, 2020
  arXiv: <https://arxiv.org/abs/2010.05646>
- [43]
  Zhifeng Kong et al.
  “Audio Flamingo: A Novel Audio Language Model with Few-Shot Learning and Dialogue Abilities”, 2024
  arXiv: <https://arxiv.org/abs/2402.01831>
- [44]
  Chenyang Le et al.
  “Transvip: Speech to speech translation system with voice and isochrony preservation”
  In *Advances in Neural Information Processing Systems* 37, 2024, pp. 89682–89705
- [45]
  Ann Lee et al.
  “Textless speech-to-speech translation on real data”
  In *arXiv preprint arXiv:2112.08352*, 2021
- [46]
  Sang-gil Lee et al.
  “BigVGAN: A Universal Neural Vocoder with Large-Scale Training”, 2023
  arXiv: <https://arxiv.org/abs/2206.04658>
- [47]
  Guan-Ting Lin, Cheng-Han Chiang and Hung-yi Lee
  “Advancing large language models to capture varied speaking styles and respond properly in spoken conversations”
  In *arXiv preprint arXiv:2402.12786*, 2024
- [48]
  Guan-Ting Lin et al.
  “Paralinguistics-enhanced large language modeling of spoken dialogue”
  In *ICASSP 2024-2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, 2024, pp. 10316–10320
  IEEE
- [49]
  Tu Nguyen et al.
  “Spirit LM: Interleaved Spoken and Written Language Model”, 2024
  arXiv: <https://arxiv.org/abs/2402.05755>
- [50]
  OpenAI
  “GPT-4 Technical Report” Accessed: 2025-07-11, <https://openai.com/research/gpt-4>, 2023
- [51]
  OpenAI
  “Introducing ChatGPT” Accessed: 2025-07-11, 2022
  URL: <https://openai.com/blog/chatgpt>
- [52]
  Wei Ping et al.
  “Deep voice 3: 2000-speaker neural text-to-speech”
  In *proc. ICLR* 79, 2018, pp. 1094–1099
- [53]
  Alec Radford et al.
  “Robust speech recognition via large-scale weak supervision”
  In *International conference on machine learning*, 2023, pp. 28492–28518
  PMLR
- [54]
  Rafael Rafailov et al.
  “Direct preference optimization: Your language model is secretly a reward model”
  In *Advances in Neural Information Processing Systems* 36, 2023, pp. 53728–53741
- [55]
  Yi Ren et al.
  “Fastspeech 2: Fast and high-quality end-to-end text to speech”
  In *arXiv preprint arXiv:2006.04558*, 2020
- [56]
  Andrew Rouditchenko et al.
  “Omni-R1: Do You Really Need Audio to Fine-Tune Your Audio LLM?”
  In *arXiv preprint arXiv:2505.09439*, 2025
- [57]
  Paul Rubenstein et al.
  “Audiopalm: A large language model that can speak and listen”
  In *arXiv preprint arXiv:2306.12925*, 2023
- [58]
  S Sakshi et al.
  “Mmau: A massive multi-task audio understanding and reasoning benchmark”
  In *arXiv preprint arXiv:2410.19168*, 2024
- [59]
  Jonathan Shen et al.
  “Natural tts synthesis by conditioning wavenet on mel spectrogram predictions”
  In *2018 IEEE international conference on acoustics, speech and signal processing (ICASSP)*, 2018, pp. 4779–4783
  IEEE
- [60]
  Hubert Siuzdak, Florian Grötschla and Luca Lanzendörfer
  “Snac: Multi-scale neural audio codec”
  In *arXiv preprint arXiv:2410.14411*, 2024
- [61]
  Changli Tang et al.
  “Salmonn: Towards generic hearing abilities for large language models”
  In *arXiv preprint arXiv:2310.13289*, 2023
- [62]
  Wolfgang Wahlster
  “Verbmobil: foundations of speech-to-speech translation”
  Springer Science & Business Media, 2013
- [63]
  Changhan Wang, Anne Wu and Juan Pino
  “CoVoST 2 and Massively Multilingual Speech-to-Text Translation”, 2020
  arXiv: <https://arxiv.org/abs/2007.10310>
- [64]
  Chengyi Wang et al.
  “Neural codec language models are zero-shot text to speech synthesizers”
  In *arXiv preprint arXiv:2301.02111*, 2023
- [65]
  Xinsheng Wang et al.
  “Spark-tts: An efficient llm-based text-to-speech model with single-stream decoupled speech tokens”
  In *arXiv preprint arXiv:2503.01710*, 2025
- [66]
  Xiong Wang et al.
  “Freeze-omni: A smart and low latency speech-to-speech dialogue model with frozen llm”
  In *arXiv preprint arXiv:2411.00774*, 2024
- [67]
  Yuancheng Wang et al.
  “Maskgct: Zero-shot text-to-speech with masked generative codec transformer”
  In *arXiv preprint arXiv:2409.00750*, 2024
- [68]
  Yuxuan Wang et al.
  “Tacotron: Towards end-to-end speech synthesis”
  In *arXiv preprint arXiv:1703.10135*, 2017
- [69]
  Jason Wei et al.
  “Finetuned language models are zero-shot learners”
  In *arXiv preprint arXiv:2109.01652*, 2021
- [70]
  Yonghui Wu et al.
  “Google’s neural machine translation system: Bridging the gap between human and machine translation”
  In *arXiv preprint arXiv:1609.08144*, 2016
- [71]
  Zhifei Xie and Changqiao Wu
  “Mini-omni: Language models can hear, talk while thinking in streaming”
  In *arXiv preprint arXiv:2408.16725*, 2024
- [72]
  Zhifei Xie and Changqiao Wu
  “Mini-omni2: Towards open-source gpt-4o with vision, speech and duplex capabilities”
  In *arXiv preprint arXiv:2410.11190*, 2024
- [73]
  Detai Xin, Xu Tan, Shinnosuke Takamichi and Hiroshi Saruwatari
  “Bigcodec: Pushing the limits of low-bitrate neural speech codec”
  In *arXiv preprint arXiv:2409.05377*, 2024
- [74]
  Jin Xu et al.
  “Qwen2.5-Omni Technical Report”, 2025
  arXiv: <https://arxiv.org/abs/2503.20215>
- [75]
  Ruiqi Yan et al.
  “URO-Bench: A Comprehensive Benchmark for End-to-End Spoken Dialogue Models”, 2025
  arXiv: <https://arxiv.org/abs/2502.17810>
- [76]
  Neil Zeghidour et al.
  “Soundstream: An end-to-end neural audio codec”
  In *IEEE/ACM Transactions on Audio, Speech, and Language Processing* 30
  IEEE, 2021, pp. 495–507
- [77]
  Aohan Zeng et al.
  “Glm-4-voice: Towards intelligent and human-like end-to-end spoken chatbot”
  In *arXiv preprint arXiv:2412.02612*, 2024
- [78]
  Binbin Zhang et al.
  “WenetSpeech: A 10000+ Hours Multi-domain Mandarin Corpus for Speech Recognition”, 2022
  arXiv: <https://arxiv.org/abs/2110.03370>
- [79]
  Bowen Zhang et al.
  “Minimax-speech: Intrinsic zero-shot text-to-speech with a learnable speaker encoder”
  In *arXiv preprint arXiv:2505.07916*, 2025
- [80]
  Dong Zhang et al.
  “Speechgpt: Empowering large language models with intrinsic cross-modal conversational abilities”
  In *arXiv preprint arXiv:2305.11000*, 2023
- [81]
  Xiangyu Zhang et al.
  “Distinctive Feature Codec: Adaptive Segmentation for Efficient Speech Representation”
  In *arXiv preprint arXiv:2505.18516*, 2025
- [82]
  Xin Zhang et al.
  “Speechtokenizer: Unified speech tokenizer for speech large language models”
  In *arXiv preprint arXiv:2308.16692*, 2023

## 附录

## 附录 A 贡献者

贡献者按字母顺序列出。

### A.1 核心贡献者

#### 模型

Boyong Wu,
Chao Yan,
Chen Hu,
Cheng Yi,
Chengli Feng,
Fei Tian,
Feiyu Shen,
Gang Yu,
Haoyang Zhang,
Jingbei Li,
Mingrui Chen,
Peng Liu,
Wang You,
Xiangyu (Tony) Zhang,
Xingyuan Li,
Xuerui Yang,
Yayue Deng,
Yechang Huang,
Yuxin Li,
Yuxin Zhang,
Zhao You

#### 基础设施

Brian Li, Changyi Wan,
Hanpeng Hu,
Jiangjie Zhen,
Siyu Chen,
Song Yuan,
Xuelin Zhang,
Yimin Jiang,
Yu Zhou,
Yuxiang Yang

#### 数据与评估

Bingxin Li, Buyun Ma, Changhe Song, Dongqing Pang, Guoqiang Hu, Haiyang Sun, Kang An, Na Wang, Shuli Gao, Wei Ji, Wen Li, Wen Sun, Xuan Wen, Yong Ren, Yuankai Ma, Yufan Lu

### A.2 贡献者

Bin Wang, Bo Li, Changxin Miao, Che Liu, Chen Xu, Dapeng Shi, Dingyuan Hu, Donghang Wu, Enle Liu, Guanzhe Huang, Gulin Yan, Han Zhang,
Hao Nie, Haonan Jia, Hongyu Zhou, Jianjian Sun, Jiaoren Wu, Jie Wu, Jie Yang, Jin Yang, Junzhe Lin, Kaixiang Li, Lei Yang,
Liying Shi, Li Zhou, Longlong Gu, Ming Li, Mingliang Li, Mingxiao Li, Nan Wu, Qi Han,
Qinyuan Tan, Shaoliang Pang, Shengjie Fan, Siqi Liu, Tiancheng Cao, Wanying Lu, Wenqing He, Wuxun Xie, Xu Zhao, Xueqi Li, Yanbo Yu, Yang Yang, Yi Liu, Yifan Lu, Yilei Wang, Yuanhao Ding, Yuanwei Liang, Yuanwei Lu, Yuchu Luo, Yuhe Yin, Yumeng Zhan, Yuxiang Zhang, Zidong Yang, Zixin Zhang

### A.3 项目发起人

Binxing Jiao,
Daxin Jiang,
Heung-Yeung Shum,
Jiansheng Chen,
Jing Li,
Xiangyu Zhang,
Yibo Zhu

### A.4 外部贡献者

#### 新加坡南洋理工大学（NTU）

Eng Siong Chng,
Hexin Liu

## 附录 B Step-Audio 2 mini 的介绍与评测结果

我们很高兴发布 Step-Audio 2 mini，Step-Audio 2 的一个特别开源版本，可在 <https://github.com/stepfun-ai/Step-Audio2> 获取。Step-Audio 2 mini 采用 Qwen2-Audio 的编码器作为其音频编码器，并以 Qwen2.5-7B 初始化。Step-Audio 2 mini 在与 Step-Audio 2 相同的数据集上训练，但仅限使用网络搜索工具。

Step-Audio 2 mini 是更贴近开发者的 Step-Audio 2 变体，其参数量便于与 Qwen-Omni、Kimi-Audio 等开源模型进行公平比较。评测结果⁵表明，Step-Audio 2 mini 取得与 Step-Audio 2 相当的结果，超越了包括 GPT-4o Audio 在内的大多数开源与商业模型。

> 注 5：评测结果通过我们的 vLLM 后端获得，可能与 transformers 后端的结果有所不同。

### B.1 自动语音识别

表 7：Doubao LLM ASR、GPT-4o Transcribe、Kimi-Audio、Qwen-Omni、Step-Audio 2 与 Step-Audio 2 mini 在多个 ASR 测试集上的字错误率（中文、粤语与日语）与词错误率（阿拉伯语与英语）比较。N/A 表示不支持该语言。

| 类别 | 测试集 | Doubao  LLM ASR | GPT-4o  Transcribe | Kimi-  Audio | Qwen-  Omni | Step-  Audio 2 | Step-Audio  2 mini |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 英语 | Common Voice | 9.20 | 9.30 | 7.83 | 8.33 | 5.95 | 6.76 |
| FLEURS English | 7.22 | 2.71 | 4.47 | 5.05 | 3.03 | 3.05 |
| LibriSpeech clean | 2.92 | 1.75 | 1.49 | 2.93 | 1.17 | 1.33 |
| LibriSpeech other | 5.32 | 4.23 | 2.91 | 5.07 | 2.42 | 2.86 |
| 平均 | 6.17 | 4.50 | 4.18 | 5.35 | 3.14 | 3.50 |
| 中文 | AISHELL | 0.98 | 3.52 | 0.64 | 1.17 | 0.63 | 0.78 |
| AISHELL-2 | 3.10 | 4.26 | 2.67 | 2.40 | 2.10 | 2.16 |
| FLEURS Chinese | 2.92 | 2.62 | 2.91 | 7.01 | 2.68 | 2.53 |
| KeSpeech phase1 | 6.48 | 26.80 | 5.11 | 6.45 | 3.63 | 3.97 |
| WenetSpeech meeting | 4.90 | 31.40 | 5.21 | 6.61 | 4.75 | 4.87 |
| WenetSpeech net | 4.46 | 15.71 | 5.93 | 5.24 | 4.67 | 4.82 |
| 平均 | 3.81 | 14.05 | 3.75 | 4.81 | 3.08 | 3.19 |
|  | FLEURS Arabian | N/A | 11.72 | N/A | 25.13 | 14.22 | 16.46 |
| 多语种 | Common Voice yue | 9.20 | 11.10 | 38.90 | 7.89 | 7.90 | 8.32 |
|  | FLEURS Japanese | N/A | 3.27 | N/A | 10.49 | 3.18 | 4.67 |
|  | 安徽口音 | 8.83 | 50.55 | 22.17 | 18.73 | 10.61 | 11.65 |
|  | 广东口音 | 4.99 | 7.83 | 3.76 | 4.03 | 3.81 | 4.44 |
|  | 广西口音 | 3.37 | 7.09 | 4.29 | 3.35 | 4.11 | 3.51 |
| 内部 | 山西口音 | 20.26 | 55.03 | 34.71 | 25.95 | 12.44 | 15.60 |
|  | 四川方言 | 3.01 | 32.85 | 5.26 | 5.61 | 4.35 | 4.57 |
|  | 上海方言 | 47.49 | 89.58 | 82.90 | 58.74 | 17.77 | 19.30 |
|  | 平均 | 14.66 | 40.49 | 25.52 | 19.40 | 8.85 | 9.85 |

### B.2 副语言信息理解

表 8：GPT-4o Audio、Kimi-Audio、Qwen-Omni、Step-Audio-AQAA、Step-Audio 2 与 Step-Audio 2 mini 在 StepEval-Audio-Paralinguistic 上的比较。

| 模型 | 平均 | 性别 | 年龄 | 音色 | 场景 | 事件 |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-4o Audio | 43.45 | 18 | 42 | 34 | 22 | 14 |
| Kimi-Audio | 49.64 | 94 | 50 | 10 | 30 | 48 |
| Qwen-Omni | 44.18 | 40 | 50 | 16 | 28 | 42 |
| Step-Audio-AQAA | 36.91 | 70 | 66 | 18 | 14 | 14 |
| Step-Audio 2 | 83.09 | 100 | 96 | 82 | 78 | 60 |
| Step-Audio 2 mini | 80.00 | 100 | 94 | 80 | 78 | 60 |
| 模型 | 情感 | 音高 | 节奏 | 语速 | 风格 | 人声 |
| GPT-4o Audio | 82 | 40 | 60 | 58 | 64 | 44 |
| Kimi-Audio | 66 | 56 | 40 | 44 | 54 | 54 |
| Qwen-Omni | 76 | 32 | 54 | 50 | 50 | 48 |
| Step-Audio-AQAA | 40 | 38 | 48 | 54 | 44 | 0 |
| Step-Audio 2 | 86 | 82 | 86 | 88 | 88 | 68 |
| Step-Audio 2 mini | 82 | 82 | 68 | 74 | 86 | 76 |

### B.3 音频理解

表 9：Audio Flamingo 3、Gemini 2.5 Pro、GPT-4o Audio、Kimi-Audio、Omni-R1、Qwen2.5-Omni、Step-Audio-AQAA、Step-Audio 2 与 Step-Audio 2 mini 在 MMAU 上的比较。

| 模型 | 平均 | 声音 | 语音 | 音乐 |
| --- | --- | --- | --- | --- |
| Audio Flamingo 3 | 73.1 | 76.9 | 66.1 | 73.9 |
| Gemini 2.5 Pro | 71.6 | 75.1 | 71.5 | 68.3 |
| GPT-4o Audio | 58.1 | 58.0 | 64.6 | 51.8 |
| Kimi-Audio | 69.6 | 79.0 | 65.5 | 64.4 |
| Omni-R1 | 77.0 | 81.7 | 76.0 | 73.4 |
| Qwen2.5-Omni | 71.5 | 78.1 | 70.6 | 65.9 |
| Step-Audio-AQAA | 49.7 | 50.5 | 51.4 | 47.3 |
| Step-Audio 2 | 78.0 | 83.5 | 76.9 | 73.7 |
| Step-Audio 2 mini | 73.2 | 76.6 | 71.5 | 71.6 |

### B.4 语音翻译

表 10：GPT-4o Audio、Qwen2.5-Omni、Qwen-Omni、Step-Audio-AQAA、Step-Audio 2 与 Step-Audio 2 mini 在语音到文本与语音到语音翻译上的 BLEU 分数比较。

| 模型 | CoVoST 2（语音到文本翻译） | | |
| --- | --- | --- | --- |
| 平均 | 英译中 | 中译英 |
| GPT-4o Audio | 29.61 | 40.20 | 19.01 |
| Qwen2.5-Omni | 35.40 | 41.40 | 29.40 |
| Step-Audio-AQAA | 28.57 | 37.71 | 19.43 |
| Step-Audio 2 | 39.26 | 49.01 | 29.51 |
| Step-Audio 2 mini | 39.29 | 49.12 | 29.47 |
| 模型 | CVSS（语音到语音翻译） | | |
| 平均 | 英译中 | 中译英 |
| GPT-4o Audio | 23.68 | 20.07 | 27.29 |
| Qwen-Omni | 15.35 | 8.04 | 22.66 |
| Step-Audio-AQAA | 27.36 | 30.74 | 23.98 |
| Step-Audio 2 | 30.87 | 34.83 | 26.92 |
| Step-Audio 2 mini | 29.08 | 32.81 | 25.35 |

### B.5 语音到语音对话

表 11：GPT-4o Audio、Kimi-Audio、Qwen-Omni、Step-Audio-AQAA、Step-Audio 2 与 Step-Audio 2 mini 在 URO-Bench 上的比较。U. R. O. 分别代表理解（Understanding）、推理（Reasoning）与口语对话（Oral conversation）。

| 模型 | 语言 | 基础 | | | | 专业 | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 平均 | U. | R. | O. | 平均 | U. | R. | O. |
| GPT-4o Audio | 中文 | 78.59 | 89.40 | 65.48 | 85.24 | 67.10 | 70.60 | 57.22 | 70.20 |
| Kimi-Audio | 73.59 | 79.34 | 64.66 | 79.75 | 66.07 | 60.44 | 59.29 | 76.21 |
| Qwen-Omni | 68.98 | 59.66 | 69.74 | 77.27 | 59.11 | 59.01 | 59.82 | 58.74 |
| Step-Audio-AQAA | 74.71 | 87.61 | 59.63 | 81.93 | 65.61 | 74.76 | 47.29 | 68.97 |
| Step-Audio 2 | 83.32 | 91.05 | 75.45 | 86.08 | 68.25 | 74.78 | 63.18 | 65.10 |
| Step-Audio 2 mini | 77.81 | 89.19 | 64.53 | 84.12 | 69.57 | 76.84 | 58.90 | 69.42 |
| GPT-4o Audio | 英语 | 84.54 | 90.18 | 75.90 | 90.41 | 67.51 | 60.65 | 64.36 | 78.46 |
| Kimi-Audio | 60.04 | 83.36 | 42.31 | 60.36 | 49.79 | 50.32 | 40.59 | 56.04 |
| Qwen-Omni | 70.58 | 66.29 | 69.62 | 76.16 | 50.99 | 44.51 | 63.88 | 49.41 |
| Step-Audio-AQAA | 71.11 | 90.15 | 56.12 | 72.06 | 52.01 | 44.25 | 54.54 | 59.81 |
| Step-Audio 2 | 83.90 | 92.72 | 76.51 | 84.92 | 66.07 | 64.86 | 67.75 | 66.33 |
| Step-Audio 2 mini | 74.36 | 90.07 | 60.12 | 77.65 | 61.25 | 58.79 | 61.94 | 63.80 |
