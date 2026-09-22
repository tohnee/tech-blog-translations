---
title: "Step-Audio：智能语音交互的统一理解与生成"
title_en: "Step-Audio: Unified Understanding and Generation in Intelligent Speech Interaction"
arxiv: 2502.11946
date: 2025-02-17
source: https://arxiv.org/abs/2502.11946
crawled: 2026-09-22
translated: 2026-09-22
---

# Step-Audio：智能语音交互的统一理解与生成

> 原文：[Step-Audio](https://arxiv.org/abs/2502.11946) · 阶跃星辰 StepFun arXiv

Step-Audio 团队
机构：StepFun

###### 摘要

实时语音交互作为人机协作的基础界面，蕴含着巨大潜力。然而，当前的开源模型面临语音数据采集成本高、动态控制能力弱以及智能水平有限等局限。为应对这些挑战，本文介绍 Step-Audio——首个可投入生产的开源解决方案。其主要贡献包括：1) 一个 1300 亿参数的语音-文本统一多模态模型，实现统一的理解与生成，并开源了其中的 Step-Audio-Chat 版本；2) 一个生成式语音数据引擎，建立了低成本的语音克隆框架，并通过蒸馏产出了开源的轻量级 Step-Audio-TTS-3B 模型；3) 一套由指令驱动的精细控制系统，支持对方言、情感、唱歌与 RAP 的动态调整；4) 一个经工具调用与角色扮演能力增强的认知架构，以有效处理复杂任务。基于我们全新的 StepEval-Audio-360 评估基准，Step-Audio 在人工评估中取得了最先进（SoTA）的性能，尤其是在指令遵循方面。在 LLaMA Question 等开源基准上，平均性能提升 9.3%，体现了我们推动开源多模态语言技术发展的承诺。我们的代码与模型见 <https://github.com/stepfun-ai/Step-Audio>。

## 1 引言

人工智能向通用系统的演进，使实时语音交互成为人机协作的关键接口。尽管近期的多模态大语言模型（LLM）加速了该领域的进展，但在 GPT-4o（[Hurst et al., 2024]）与豆包（[bytedance, 2024]）等专有系统取得突破的同时，开源社区仍面临持续的挑战。现有的开源模型，如 Qwen2-Audio（[Chu et al., 2024]）、Llama 3（[Dubey et al., 2024]）与 wavLLM（[Hu et al., 2024]），在三个根本性局限上苦苦挣扎：理解与生成过程的分离阻碍了端到端系统集成；依赖繁琐的人工语音数据获取方法限制了高效的语音复刻；在调控韵律特征、地区方言以及工具使用能力方面精度不足。这些局限凸显了对可部署框架的迫切需求——这类框架需将精简的架构与情感计算（精准的情绪感知与调节）和情境认知（情境推理与回应生成）的双重能力相协调。

当前的开源语音系统面临多重架构挑战。
传统框架采用级联式方法（[Huang et al., 2024]），组合自动语音识别（ASR）、LLM 处理与文本到语音（TTS）。该框架在模态转换中引入误差传播，同时增加了系统复杂度。纯端到端方法虽然在概念上优雅，却往往牺牲开放域对话质量（[Zeng et al., 2024]）。模块化设计与完全集成系统之间的张力仍未解决。此外，传统文本到语音流水线依赖人工整理的数据集，尤其是多语言、多方言场景——这一过程需要高昂的人工标注成本。现有解决方案也缺乏用于动态语音自适应的精细控制机制，例如实时调整语速、情感韵律或演唱式发声（如唱歌与 RAP 人声）。更关键的是，工具调用能力与上下文意识的缺失，使其无法处理诸如「获取实时天气数据并用粤语播报」之类的复杂查询，而只能依赖人工 API 集成。

本报告提出 Step-Audio，首个可投入生产的智能语音交互开源框架，通过四项关键创新协调理解与生成。

- 1300 亿参数多模态模型：单一统一模型集成理解与生成能力，执行语音识别、语义理解、对话、语音克隆、音频编辑与语音合成。我们已开源 130B 的 Step-Audio-Chat 变体。
- 生成式数据引擎：通过 1300 亿参数多模态模型生成高质量音频，消除了传统 TTS 对人工数据采集的依赖。利用这些数据训练并公开发布了资源高效的 Step-Audio-TTS-3B 模型，具备更强的指令遵循能力以实现可控语音合成。
- 细粒度语音控制：通过基于指令的控制设计实现精准调控，支持多种情感（愤怒、喜悦、悲伤）、方言（粤语、四川话等）与发声风格（RAP/唱歌、清唱哼鸣），满足多样化语音生成需求。
- 增强的智能水平：通过集成工具调用（ToolCall）机制与角色扮演增强，提升智能体在复杂任务中的表现。

在开源基准上，Step-Audio 展现了卓越性能。它在开放域问答与复杂指令任务（包括 LLaMA Question、TrivialQA 与 ComplexBench）上取得 SoTA 结果，相较最佳开源指标平均提升 9.3 分，验证了其在泛化深层语义理解能力上的优势。此外，为填补当前缺乏全面端到端语音对话评估体系的空白，我们引入了多维度 StepEval-Audio-360 评估框架，覆盖逻辑推理、创造力、语言能力、理解与控制等 9 个维度的关键能力。如图 1 所示，Step-Audio 在与 GLM-4-Voice、Qwen2-Audio 等开源模型的主观对比中于所有维度取得 SoTA 结果，在回应质量、回应相关性与事实准确性上分别提升 19.2%、23.7% 与 43.2%。特别是在情感理解、语速控制、RAP 人声与角色扮演等生成控制维度上，相较开源 SoTA 模型，IF（指令遵循）与 MOS（平均意见得分）指标分别提升 29.8% 与 27.1%，凸显其在复杂语音交互场景中的领先优势。

![Refer to caption](2502.11946v2/figure/improved_radar.png)

图 1：
端到端语音交互的人工评估。我们对 Step-Audio 与 GLM-4-Voice（[Zeng et al., 2024]）和 Qwen2-Audio（[Chu et al., 2024]）进行了全面的人工评估对比，覆盖九个关键维度：角色扮演、逻辑推理、创造力、歌唱语言能力、语音情感控制、游戏互动、语音指令遵循与语音理解。专业评估者使用 Likert 量表（1-5）就自然度与任务完成度对端到端对话会话进行评分。Step-Audio 在所有这些维度上都代表了当前最先进水平（SoTA）。它在语言能力上尤为突出，在语法、语义与语言生成上展现出高水平。在歌唱方面，Step-Audio 凭借自然的音高控制、节奏准确性以及整体和谐的人声输出胜过其他模型，使其成为这两个关键方面的顶级选手。

## 2 相关工作

端到端语音系统的近期进展显著改善了人机音频交互。早期方法依赖级联的 ASR-LLM-TTS 流水线（[Huang et al., 2024]），其中语音识别、语言建模与语音合成的不同模块被顺序连接。然而，这些系统存在延迟累积、误差传播与优化割裂的问题。后来的方法试图通过可训练的适配器将语音编码器直接连接到 LLM 以增强集成（[Kong et al., 2020; Chu et al., 2024; Das et al., 2024]），但音频输出仍需要单独的 TTS 模块。

完全端到端系统的出现标志着范式转变。Llama-Omni（[Fang et al., 2024]）等架构将非自回归（NAR）TTS 模块与语言模型集成，使用联结主义时序分类（CTC）损失。Freeze-Omni（[Wang et al., 2024]）使用自回归与 NAR 语音解码器的组合。这些系统展现了更低的延迟，但在处理情感细微差别与自然对话流方面存在局限。MinMo（[Q. Chen et al., 2025]）通过 CosyVoice2（[Du, Wang et al., 2024]）解码器引入自回归语音 token 预测，而交错建模方法（[Zeng et al., 2024; Nguyen et al., 2024]）则在序列层面交替生成文本与语音 token。

Moshi（[Défossez et al., 2024]）与 Mini-Omni（[Xie & Wu, 2024]）等并行解码架构通过同时生成文本与多个语音码本 token 代表了重大飞跃。这些系统通过压缩语音 token 序列实现了更低延迟，但在扩展语音 token 带宽时难以保持语言能力。现有系统通常专精于特定方面：GLM-4-Voice（[Zeng et al., 2024]）优先考虑延迟降低，而 Moshi 强调语音质量，但没有一个能全面兼顾情绪感知、对话自然度与实时知识整合。

近期的方法学进展系统地研究了情绪感知的交互范式，但它们与多模态框架的整合尚处于起步阶段。虽然一些系统（[Wang et al., 2024]）纳入了基本的情感分析，但它们缺乏双向的情感共鸣——既未检测用户语音中的副语言线索，也未生成符合上下文的情绪回应。由于 LLM 倾向于生成冗长、面向文本优化的输出（[Fang et al., 2024]），不适合口语对话，自然度差距依然存在。近期工作引入了任务特定的优化：LUCY（[H. Gao et al., 2025]）采用了 Mini-Omni（[Xie & Wu, 2024]）的架构框架，并辅以对话数据集上的专项微调，用于情绪控制与函数调用。

## 3 架构

![Refer to caption](2502.11946v2/stepAudio-20250217-ff.png)

图 2：Step-Audio 的架构。Step-Audio 主要由三个组件组成：语音 tokenizer、LLM 与语音解码器。语音 tokenizer 负责将输入语音离散化为 token。LLM 对文本与语音 token 进行建模，语音解码器则生成波形输出。

传统语音对话系统通常采用由 ASR、LLM 与 TTS 模块组成的级联架构。然而，我们提出的模型在预训练阶段经过了全面的多模态训练与文本-音频对齐，已具备端到端语音对话能力。尽管我们广泛探索了其他设计，最终仍采用 AQTA（音频输入、文本输出）+ TTS 框架用于实时语音对话，如图 2 所示，主要基于以下考量：

- 高质量纯语音对话数据的稀缺：纯语音对话数据的可用性有限且场景受限，制约了端到端语音对话模型的训练效率。
- 输出语音的可控性与可定制性：通过引入 TTS 模块，我们可以灵活控制音色、音高等语音参数，以满足用户的个性化需求，并持续增强模型的表现力。

我们的目标是将 Step-Audio 打造为一个无缝集成语音理解与合成的实时多模态模型，它由四个关键组件构成：(1) 双码本 tokenizer 框架，采用并行语言学 tokenizer（16.7Hz、1024 码本）与语义 tokenizer（25Hz、4096 码本），以 2:3 时间交错；(2) 基于 Step-1（[StepFun, 2024]）的 1300 亿参数 LLM，通过音频上下文化的持续预训练与后训练增强；(3) 结合 Flow Matching 与神经声码器的混合语音合成器，针对实时波形生成优化。此外，还采用语音活动检测（VAD）模块来提取发声片段。

### 3.1 Tokenizer

为克服传统语音 tokenizer 分别为理解或生成任务单独捕获信息的局限，我们在 Step-Audio 中提出了类似 ARCON（[Ming et al., 2024]）的双码本语音 tokenizer 框架。该方法采用两个不同的 tokenizer——语言学 tokenizer 与语义 tokenizer——以更好地表示语音特征。语言学 tokenizer 用于提取结构化的高层表示，包括音素与语言学特征；而语义 tokenizer 则设计用于同时编码语义与粗粒度声学特征。

对于语言学 token 化，我们使用 Paraformer（[Z. Gao et al., 2022]）编码器的输出，并以 16.7 Hz 的 token 率量化为离散表示。对于语义 token 化，我们采用 CosyVoice（[Du, Chen et al., 2024]）的 tokenizer，它专门设计用于高效编码生成自然、富有表现力的语音输出所需的特征，运行 token 率为 25 Hz。语言学 tokenizer 的码本大小为 1024，而语义 tokenizer 使用更大的 4096 码本以捕捉更精细的声学细节。

为了有效整合这两种 token 化方案，我们受 SpiritLM（[Nguyen et al., 2024]）启发实现了 token 级交错方法。鉴于两者 token 率不同，我们建立了 2:3 的时间对齐比例，即每两个语言学 token 与三个语义 token 配对。

### 3.2 LLM

为增强 Step-Audio 有效处理语音信息并实现精准语音-文本对齐的能力，我们基于 Step-1（一个 1300 亿参数的预训练文本 LLM）进行了音频持续预训练。Step-Audio 预训练与后训练过程的细节将在第 4 节与第 5 节中全面讨论。

在多轮对话系统中，音频 token 与文本 token 之间的巨大长度差异需要高效的处理策略。为此，历史信息在输入系统之前先由 ASR 模型转写为文本格式，从而优化计算效率。但需要指出的是，该模型架构在需要时仍保持处理和利用音频 token 作为历史上下文的能力。

### 3.3 语音解码器

语音解码器由一个 30 亿参数的语言模型、一个 flow-matching 模型与一个 mel-to-wave 声码器组成，主要设计用于接收文本或音频 token，并生成融合历史信息与指令的连续时域风格化波形。为优化合成语音的可懂度与自然度，语音解码器采用双码交错方式训练，确保语言学与语义特征在生成过程中的无缝整合。在参数量更大的语音解码器上，我们观察到了更强生成能力的涌现。更多细节请参阅 5.1 节。

### 3.4 实时推理

![Refer to caption](2502.11946v2/figure/pipeline-overview.png)

图 3：实时推理流水线的架构旨在实现实时交互。当音频输入时，流式音频 tokenizer 与语音活动检测模块并发处理。控制器管理状态转换。用户语音的停顿会触发推测式响应生成，发起多次调用但只提交一个响应。上下文管理器以文本格式处理对话历史以保证连续性。一旦用户说完，系统进入回复状态，提交一个推测式响应并输出音频。之后返回空闲状态，等待下一次交互。

为实现实时交互，我们设计了如图 3 所示的优化推理流水线。其核心是控制器（Controller）模块，管理状态转换、编排推测式响应生成，并确保关键子系统之间的无缝协调。这些子系统包括：用于检测用户语音的 VAD、用于实时处理音频的流式音频 tokenizer、用于处理并生成回应的 Step-Audio 语言模型与语音解码器，以及用于保持对话连续性的上下文管理器。

##### 推测式响应生成

为降低交互延迟，系统预先生成推测式（speculative）响应。这能最小化感知延迟、提升响应性，代价是推测式响应被丢弃时偶尔出现冗余计算。系统始于 Silence（静默）状态，等待用户输入。当 VAD 检测到有效语音时，系统转入 UserSpeaking（用户说话）状态。在该状态下，流式音频 tokenizer 开始将音频转换为 token。若用户短暂停顿，系统进入 UserPaused（用户暂停）状态，此时触发推测式响应生成。通过预期输入即将完成而抢先生成响应，系统在对话恢复时降低了延迟。若用户继续说话，推测式响应将被丢弃。一旦系统确定用户已经说完，便转入 BotReplying（机器人回复）状态，提交最近的推测式响应并输出其音频。若被用户语音打断，系统优先处理新输入，同时保持对话连续性。完成响应后，系统返回 Silence 状态，准备下一次交互。经验分析表明，约 40% 的推测式响应被成功提交。该机制相较非推测式方法将单次响应延迟降低约 500ms。

##### 上下文管理

我们的系统使用文本转写而非原始音频 token 作为历史上下文，因为它提供了更紧凑的表示（平均文本与音频 token 之比为 1:14），可提升性能，并支持更长的对话而质量损失极小。ASR 异步地将用户语音转写为文本，维持准确且最新的对话历史。

##### 流式音频 Tokenizer

输入音频流通过两条并行的 tokenizer 流水线处理，各自采用固定时长的分段。生成的 token 以 2:3 的交错比例无缝合并为单一序列。若没有流式音频 tokenizer，推理时间将显著变慢，且取决于音频输入的长度。

## 4 预训练

### 4.1 数据集

我们的多模态预训练数据集整合了三大类数据资源：音频、文本与图像。音频部分包括 1.1 万亿 token 的音频续写数据（约 7,300,000 小时）、1130 亿 token 的 TTS（文本到语音）合成语音数据（约 700,000 小时）、1050 亿 token 的 ASR（自动语音识别）数据（约 650,000 小时），以及 3500 亿 token 的音频-文本交替数据（约 2,000,000 小时）。文本数据共计 8000 亿 token，涵盖网页文档、书籍、代码与专有材料。图像部分包括 8000 亿 token 的图文配对/交替数据，来源于网页、书籍与专有资源。

### 4.2 训练细节

Step-Audio 是 Step-Omni 的组成部分，Step-Omni 旨在训练一个语音、图像与文本的统一预训练模型。该训练基于预训练文本模型与图像编码器进行持续预训练。整个过程共分为三个阶段。

- 阶段 1：我们为预训练文本模型扩充词表，新增 5,120 个音频 token，并集成预训练图像编码器，构成 Step-Omni 模型。训练期间，为确保文本模型能力的损失最小，文本模型骨干的学习率全程保持在较低水平（2e-5）。而 embedding 与语言模型（LM）head 的学习率设置为骨干的 5 倍，以加速新增 token 的收敛。同时，图像编码器在整个训练过程中保持冻结。在此阶段，音频、文本与图像数据以 2:1:1 的比例使用，其中音频数据仅包含纯音频续写任务。
- 阶段 2：在阶段 1 完成 1.2T token 的训练后，我们纳入音频-文本交错数据继续训练，音频续写数据与音频-文本交错数据的比例为 1:1。在此阶段，音频、文本与图像数据的比例保持 2:1:1。
- 阶段 3：在阶段 2 完成 800B token 的训练后，我们纳入 ASR 与 TTS 数据继续训练。音频续写数据、音频-文本交错数据、ASR 数据与 TTS 数据的比例设为 1:1:1:1。在此阶段，音频、文本与图像数据的比例调整为 4:3:3。此外，embedding 与 LM head 的学习率与骨干同步，采用从 2e-5 递减至 5e-6 的余弦调度。

我们在不同参数规模的模型上采用相同的预训练策略。

### 4.3 训练基础设施

我们在数千块 H800 GPU 上以 35% 的模型算力利用率（MFU）训练 Step-Omni。在采用定制 GPU kernel 与通信重叠等标准优化的同时，我们重点介绍两项进一步提升训练效率的创新方法。

##### 分离式数据处理

Step-Omni 训练中多模态数据的处理计算量巨大，往往需要大量 CPU 资源才能跟上模型训练速度。常规实现通常将数据处理任务与训练作业同置（co-locate），导致这些任务之间显著相互干扰，最终拖慢训练过程。为解决这一问题，我们引入了 StarWeaver，一个基于 RPC 的分布式数据处理库。StarWeaver 将 CPU 密集的数据预处理任务迁移到远程进程，从而减轻 GPU 训练侧的计算负担，提升整体训练效率。StarWeaver 还有助于增强数据并行维度的负载均衡，因为它可以作为基于全局负载信息重新分发数据的理想机制。

##### 分离式模型放置

对于 Step-Omni 这类多模态模型，训练通常不仅涉及 LLM，还涉及模态编码器（如视觉编码器）。整合这些异构组件挑战了训练框架关于「模型是同质且单体」的传统假设。这种错配常导致训练效率欠佳。为解决该问题，我们提出分离式模型放置（disaggregated model placement），为每个子模型分配专用资源并采用量身定制的并行策略。这一新颖方法有效最小化了由模型异构性引起的流水线气泡，从而实现最优训练效率。细节见（[Zhang et al., 2024]）。

### 4.4 面向音频预训练的 Tokenizer 探索

为实现语音理解与生成的统一，我们首先探索了语音 tokenizer 的使用。最初，我们研究了使用单一码本的训练方式。实验中我们发现，当仅使用语义 token 训练模型时，下一个 token 预测困惑度相对较低，生成内容与前文之间的语义连贯性良好。然而，由于丢弃过多语义 token 造成声学信息的显著损失，随后经声码器还原的音频在音色与韵律上严重退化，听感不佳。当仅使用语言学 token 训练时，模型续写经声码器恢复的音频听感不错，但下一个 token 预测困惑度非常高，续写与前文之间的语义连贯性很差。

![Refer to caption](2502.11946v2/figure/semantic_inguistic_merge.png)

图 4：双码本与单码本 tokenizer 的训练损失对比。

当以语义 token 与语言学 token 交错训练时，语义 token 保证续写与前文的语义连贯，而语言学 token 保证重建音频的听感质量。由于语义 token 与语言学 token 之间的相互参照，我们观察到，如图 4 所示，使用双码本训练时，语义 token 与语言学 token 的下一个 token 预测困惑度相较使用单一码本均有所下降。值得注意的是，语义 token 的困惑度下降更为显著。此外，ASR 消融结果表明，双码本模型在 ASR 测试集上取得了低于纯单码本模型的字符错误率（CER）（见 6.2.1 节）。

此外，以 2:3 的比例对语言学离散 token 与语义离散 token 进行分组与交错，有助于训练损失更快收敛。更重要的是，以语言学 token 扩展 CosyVoice 语义 token，增强了模型理解与遵循多轮历史指令的能力，也缓解了发音不清、吐字含糊等问题，显著提升了 CosyVoice 单码本的性能。

## 5 后训练

### 5.1 TTS

#### 5.1.1 数据集

高质量语音数据对 TTS 任务至关重要，它直接影响模型的性能与生成语音的表现力。特定语言数据、方言数据、说话风格、情感数据与副语言数据极为稀缺。构建此类数据集需要大量人力与资金，且过程通常跨越较长周期。

为填补这一空白，我们提出首个面向 TTS 系统的新型合成数据驱动框架，包含三个关键组成部分：

- 第一，我们使用 Step-2（[StepFun, 2024]）LLM 生成语言上多样、语义上丰富的文本内容。
- 第二，我们选择一个纳入了音频 token 冷却（cooldown）机制的 Step-Audio 预训练模型 checkpoint，它能够直接生成特定说话人、依赖特定语言、感知特定方言的音频数据。
- 第三，我们通过微调上述 checkpoint 开发了音频编辑（Audio-Edit）模型，专门用于生成细腻的情感表达与多样的说话风格。该模型架构在保持说话人一致性的同时，实现对副语言特征的精准控制。

![Refer to caption](2502.11946v2/TTS-data.png)

图 5：流程从文本输入开始，由 Step-2 LLM 生成多条改写文本。然后，Step-Audio 模型使用改写文本与既有音频 wav 数据生成目标说话人数据。最后，Audio-Edit 模型对数据进行精修，产出情感/风格数据，以解决 TTS 任务中高质量语音数据稀缺的问题。

##### 语言与方言

利用在海量说话人与语言数据上训练过的 Step-Audio 的强大续写能力，我们生成目标说话人、目标语言与方言数据。基于文本的 LLM Step-2 用于翻译并改写对话文本，使其符合目标语言或方言的语法与风格。我们收集母语者的录音与文本作为提示音频与提示文本，然后使用如下格式

[system prompt; prompt text; target text; prompt code; target code]

配合相应文本，用 Step-Audio 进行音频续写生成。这一方法只需少量高质量种子数据，即可快速创建大量目标语言与方言的母语者数据。

##### 情感与说话风格

情感与说话风格数据一直难以处理，原因在于情感类别及其强度的区分与界定都很困难，且准确描述与记录各类风格也十分复杂。为此，我们提出一种基于音频编辑模型的方法。它巧妙地将复杂的情感与风格描述转化为对比对（comparative pair）数据构建格式。Step-2 用于以特定情感与风格改写对话文本。收集同一说话人、相同文本的普通语音与情感语音样本，并使用 Step-Audio 进行克隆与续写生成，构造（文本、中性音频 token、情感与风格音频 token）数据。仅使用（中性音频 token，情感与风格音频 token）对，对音频冷却预训练模型进行 SFT，即得到音频编辑模型。使用该模型，输入中性风格语音即可生成情感或风格增强的音频，并可迭代产出不同情感或风格强度的数据。

##### 唱歌与 RAP

我们通过三个阶段构建歌词与人声片段的配对数据集：(1) 收集 10,000 小时以上带 LyRiCs（LRC）格式时间戳的唱歌 / RAP 音轨；(2) 使用 Demucs（[Rouard et al., 2023]）提取干声（dry vocals），并通过语音活动检测（VAD）去除静音区域；(3) 使用 LyRiCs 时间戳切分音频，并将歌词与音频片段对齐。在数据清洗上，我们执行了三个步骤：(1) RAP 分离：我们保留语速较高的片段，并使用流派分类模型识别嘻哈片段，从而分离出纯 RAP 片段；(2) 音频质量过滤：利用噪声检测与说话人分离（speaker diarization），我们保留低噪声、单说话人的片段；(3) 对齐校验：为应对 LyRiCs 时间戳不准确导致的错位，我们计算转写语音与真实歌词之间的字符错误率（CER），丢弃错位片段。最终，保留的音频片段总时长占原歌曲时长的 17.8%。该数据集支持双重训练目标：LLM 学习将歌词映射到语言学与语义 token，而语音解码器将这些 token 解码为音调精准、高保真的人声。

##### 目标说话人

仅依靠基础语言与方言数据的模型泛化，难以让目标说话人达到母语者水平地支持多种语言或方言。为缓解这一问题，我们采用由音色与韵律与目标说话人相近的母语者所生成音频中提取的双码。将这些双码与目标说话人的提示音频结合以重新生成新音频，再从中重新提取双码。通过这一简单流程，目标说话人讲新语言与方言的效果会更接近母语者。

数据质量评估是我们合成数据框架的关键组成部分。为确保种子数据与合成数据的可靠性和有效性，我们实施了包含多项客观指标的综合评估体系：ASR 准确率、语音活动检测（VAD）性能、说话人分离精度、情感识别一致性以及深度噪声抑制（DNS）有效性。这一多维度质量控制机制保证了生成合成数据的稳健性与实用价值。

#### 5.1.2 训练细节

与强调对说话人特征、情感表达、语言学特征与风格元素进行细粒度控制的传统 TTS 系统不同，我们的方法采用 LLM 的对话式范式与训练方法。这一战略性对接显著增强了系统灵活性，同时建立了一个可扩展的框架以支持未来的模型与数据扩充，从而解决语音合成系统的可扩展性难题。

##### 监督微调格式

SFT 格式包含三个基本组成部分：系统提示词、人类输入与助手回复，构成两轮对话配置。在该格式中，系统提示词作为基础元素，用于指定说话人属性并定义所支持的指令标签。人类输入与助手回复组件分别专门用于处理文本内容与双码本表示。第一轮的文本与音频 token 可用于保持域内说话人的音色与风格一致性，也可用于域外零样本克隆。

##### 指令标签

指令标签分为两个不同类别：描述性标签与比较性标签。描述性标签用于控制语言、方言、声音与风格等方面，而比较性标签用于情感与语速控制的层级区分。描述性标签的数据使用 Step-Audio 模型克隆生成，支持的语言与风格包括日语、韩语、粤语、四川话、萝莉音、RAP 与唱歌。比较性标签的数据使用音频编辑模型生成，支持的情感包括高兴、愤怒、悲伤，语速变化如快与慢，各划分为五个层级。

我们使用 5.1.1 节所述的 SFT 数据，并采用 30 亿参数模型，以 2×10^-5 的初始学习率训练一个 epoch。学习率采用余弦衰减策略调整，下界设为 2×10^-6。

### 5.2 AQTA

我们将基于人类反馈的强化学习（RLHF）应用于 AQTA 任务，由此得到 Step-Audio-Chat 模型，如图 6 所示。

![Refer to caption](2502.11946v2/RLHF.png)

图 6：在每个训练迭代中，我们从不同版本的模型收集多个回应。然后，通过人工打分以及 LLM 评估，选出高质量对来训练奖励模型。最后，我们使用 PPO 算法训练最终的 Step-Audio-Chat 模型。

#### 5.2.1 SFT 数据集

##### 数据类型

我们根据输入（Q）与输出（A）的性质，将 SFT 数据划分为若干类型：

- TQTA：该类型包括大量基于文本的问答（QA）数据。
- AQTA：该类型由音频输入配对文本输出组成。
- TAQTA：该类型旨在增强文本与语音之间的一致性。其中文本 Q 既作为输入（不参与损失计算），也作为输出（参与损失计算）。
- 其他类型：包括 audioQ-audioA（AQAA）、visionQ-audioQ-textA（VAQTA）等。纳入这些类型是为了给训练数据提供额外的多样性与复杂度，进一步提升模型的稳健性。

为增强语音识别能力，我们在既有数据集之外引入了额外以 ASR 格式标注的训练数据。这些 ASR 格式的资源包含语音信号的详细转写，使模型能够更好地解读语音模式与语言细节。引入此类补充的 ASR 标注数据，增强了模型对包括地区口音、语速波动与环境噪声干扰等声学变化的稳健性。

##### 数据处理

为优化 SFT 数据以实现有效的模型训练，我们实施了以下处理步骤：

- 单轮数据修改：对于单轮交互，我们对输入施加了文本长度过滤。这是因为真实用户的语音输入往往简洁。此外，我们修改输出，使其采用更口语化的文本风格，增强语音模型的人性化特质，避免僵硬、冗长或过度结构化的回应。
- 多轮数据处理：对于多轮交互，我们将先前轮次的语音输入替换为相应的文本转写，仅保留最后一轮的语音输入。此外，只有最后一轮的回应参与损失计算，使模型训练聚焦于针对最近输入生成准确、相关的回应。

通过这种系统化的 SFT 数据构建与处理方法，我们旨在创建一个多样化且具代表性的数据集，使我们的语音模型在真实场景中取得卓越表现，对用户输入给出自然、连贯且贴合语境的回应。

#### 5.2.2 监督微调细节

我们使用 5.2.1 节所述的 SFT 数据，模型微调 1 个 epoch，学习率从 $5.656\times 10^{-5}$ 到 $5.656\times 10^{-6}$。

#### 5.2.3 奖励模型数据集

##### TQTA 偏好数据构建

我们收集了由 TQTA 模型（如 Step-1 与 Step-2）生成的人类偏好数据，并移除了在语音对话中分布较少的类别，如代码与数学。我们主要保留了日常对话、角色扮演、安全与指令遵循等类别。

##### AQTA 偏好数据构建

对于微调数据集，我们首先收集了来自用户的真实音频提示，并使用 SFT 模型采样四个回应。然后，由人工标注者依据指令遵循、对话自然度与安全性的标准，对这四个回应按 1 到 5 分评分，构造 chosen/rejected（偏好/被拒）对。除这些人工生成的标签外，我们还采用 LLM-as-a-Judge 方法对模型在客观问题上的回应打分，并基于回应的正确性构造相应的 chosen/rejected 对。
为缓解 5.2.6 节所述的「装聋作弊」（"deaf hacking"）模式偏差，我们使用被作弊的 PPO 模型为带有清晰音频提示的输入音频生成回应。若回应表现出作弊行为，我们将其构造为被拒（rejected）回应。该流程旨在消除奖励模型训练数据中 chosen 回应仅存在「装聋作弊」所导致的模式偏差。

#### 5.2.4 奖励模型训练细节

我们为奖励模型训练实施了两阶段方法：先进行 TQTA 单模态偏好模型预训练，再进行 AQTA 跨模态微调。模型在 TQTA 上微调 1 个 epoch，在 AQTA 上微调 1 个 epoch。学习率采用余弦衰减策略调整，初始值为 $1.24\times 10^{-5}$，下界设为 $6\times 10^{-6}$。

奖励模型训练从 SFT 模型初始化，使用 Bradley-Terry 损失（[Bradley & Terry, 1952]）完成两阶段训练，在人类偏好测试集上取得了 70.51% 的成对准确率。

#### 5.2.5 PPO 数据集

对于 PPO 训练数据，我们使用了与奖励模型 AQTA 微调阶段相同的提示词种子。

#### 5.2.6 PPO 训练细节

获得奖励模型后，我们采用 PPO（[Schulman et al., 2017]）算法训练语音大语言模型。在 RLHF 训练阶段，critic 模型先以最初 80 个训练步进行预热。我们采用 $\epsilon=0.2$ 的 PPO 裁剪阈值与 $1\times 10^{-6}$ 的初始学习率，学习率以余弦策略衰减，最低学习率为 $2\times 10^{-7}$。此外，我们将 KL 惩罚系数设为 $\beta=0.05$。

与 TQTA 模型 RLHF 训练中观察到的奖励作弊（reward hacking）不同，我们发现仅在人工标注的 AQTA 偏好数据上训练的奖励模型会出现「装聋作弊」现象（即无论输入音频是否清晰，奖励模型都对包含「我没听清」之类短语的回应给予高奖励，在 RLHF 训练中无意间强化了装聋作弊模式）。我们将此问题归因于奖励模型训练数据中的模式偏差——该数据仅包含「装聋作弊」对：模型对不清晰或语义不完整的提示以「我没听清」作为 chosen 回应，但对清晰且语义完整的提示却缺少此类回应作为 rejected 样本。为缓解该偏差，我们按 5.2.3 节所述构造了相应数据。我们还计划在未来的 RLHF 训练中引入基于规则的奖励，以消除「装聋作弊」。

## 6 评估

### 6.1 基准设计

我们遵循一系列规则创建了一个名为 StepEval-Audio-360 的新基准（https://huggingface.co/datasets/stepfun-ai/StepEval-Audio-360）。在设计原则上，该基准旨在填补多模态语音交互评估的空白，系统地识别模型的优势与不足，并重视用户体验与安全性。在数据收集上，将真实用户录音与公开语料库结合使用。同时，对音频质量与语义标注进行严格控制，以确保符合隐私要求。

评估维度主要覆盖语言能力、情感智能、逻辑推理、创造力、多指令遵循、角色扮演、安全性等。人口统计学差异（年龄/性别/方言）、环境条件（噪声水平/麦克风类型）以及韵律特征（语速/发音模式）也被纳入考量。指标体系架构结合定量分析，使用脚本自动验证准确率、重复率等指标，同时也涉及大语言模型评估与人工评估。此外，基准按季度更新以避免落后，并根据用户反馈进行调整。

### 6.2 结果

#### 6.2.1 ASR

我们用 3B 模型进行了验证实验，比较语义码（Semantic Code）与双码（Dual-Code）在 ASR（自动语音识别）任务上的表现。在保持相同音频训练数据量的前提下，双码方法的字符错误率（CER）从 25.5 改善到 18.4。这表明双码方法显著提升了 ASR 任务的性能。

我们在两个阶段测试了模型的表现：一是预训练模型（Step-Audio Pretrain）；二是人类偏好对齐之后的对话模型（Step-Audio-Chat），使用系统提示词「请记录下你所听到的语音内容。」。评估数据集包括 Aishell1、Aishell2 ios、Wenetspeech test-net、Wenetspeech test-meeting、Librispeech test-clean 与 Librispeech test-other。评估指标方面，中文采用字符错误率（CER），英文采用词错误率（WER）。我们系统性地比较了以下两类主流大型语音模型：

- 隐藏特征建模：Whisper Large-v3（[Radford et al., 2023]）、Qwen2-Audio（[Chu et al., 2024]）、MinMo（[Q. Chen et al., 2025]）、LUCY（[H. Gao et al., 2025]）；
- 离散音频 token 建模：Moshi（[Défossez et al., 2024]）、GLM-4-voice（[Zeng et al., 2024]）、Step-Audio。

表 1：ASR 结果对比

|  | 隐藏特征建模 |  |  |  | 离散音频 token 建模 |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | Whisper Large-v3 | Qwen2-Audio | MinMo | LUCY | Moshi | GLM-4-voice Base | GLM-4-voice Chat | Step-Audio Pretrain | Step-Audio Chat |
| Aishell-1 | 5.14 | 1.53 | - | 2.4 | - | 2.46 | 226.47 | 0.87 | 1.95 |
| Aishell-2 ios | 4.76 | 3.06 | 2.69 | - | - | - | 211.3 | 2.91 | 3.57 |
| Wenetspeech test-net | 9.68 | 7.72 | 6.64 | 8.78 | - | - | 146.05 | 7.62 | 8.75 |
| Wenet test-meeting | 18.54 | 8.4 | 7.6 | 10.42 | - | - | 140.82 | 7.78 | 9.52 |
| Librispeech test-clean | 1.9 | 1.6 | 1.6 | 3.36 | 5.7 | 2.82 | 75.39 | 2.36 | 3.11 |
| Librispeech test-other | 3.65 | 3.6 | 3.82 | 8.05 | - | 7.66 | 80.3 | 6.32 | 8.44 |
| 平均 | 7.28 | 4.32 | - | - | - | - | 146.74 | 4.64 | 5.89 |

具体结果见表 1。在基于音频 token 的语音模型中，Step-Audio Pretrain 以 4.64 的平均 CER 取得最佳表现。与隐藏特征模型相比，Step-Audio Pretrain 优于 Whisper Large-v3，并与 Qwen2-Audio、MinMo 取得相当的结果，尤其是在 Aishell1、Aishell2 与 Librispeech test-clean 等干净测试集上，Step-Audio Pretrain（平均 CER 2.05）非常接近 Qwen2-Audio（平均 CER 2.06）。这表明 Step-Audio 通过其双码本压缩策略，在语音表示的离散化过程中有效保留了语义信息。

此外，我们比较了最终对话模型的 ASR 能力。在测试 GLM-4-voice Chat 模型时，我们尝试了多种提示词，最终选择提示词「请写下你听到的语音内容：」进行评估。然而，该模型仍难以有效遵循指令。相比之下，Step-Audio Chat 模型取得 5.89 的平均 CER，保持了强劲表现，反映了其稳健的指令遵循能力。

表 2：Step-Audio、GLM-4-Voice 与 MinMo 内容一致性性能比较。

| 模型 | test-zh | test-en |
| --- | --- | --- |
| CER (%) ↓ | WER (%) ↓ |
| GLM-4-Voice | 2.19 | 2.91 |
| MinMo | 2.48 | 2.90 |
| Step-Audio | 1.53 | 2.71 |

表 3：Step-Audio-TTS-3B 与近期基于 LLM 的 TTS 模型在 SEED 测试集上的结果。Step-Audio-TTS-3B-Single 表示双码本骨干配单码本声码器。Step-Audio-TTS 表示 1300 亿参数版本的 Step-Audio-TTS。

| 模型 | test-zh |  | test-en |  |
| --- | --- | --- | --- | --- |
| CER (%) ↓ | SS ↑ | WER (%) ↓ | SS ↑ |
| FireRedTTS | 1.51 | 0.630 | 3.82 | 0.460 |
| MaskGCT | 2.27 | 0.774 | 2.62 | 0.774 |
| CosyVoice | 3.63 | 0.775 | 4.29 | 0.699 |
| CosyVoice 2 | 1.45 | 0.806 | 2.57 | 0.736 |
| CosyVoice 2-S | 1.45 | 0.812 | 2.38 | 0.743 |
| Step-Audio-TTS-3B-Single | 1.37 | 0.802 | 2.52 | 0.704 |
| Step-Audio-TTS-3B | 1.31 | 0.733 | 2.31 | 0.660 |
| Step-Audio-TTS | 1.17 | 0.73 | 2.0 | 0.660 |

表 4：双码本重合成与 Cosyvoice 的性能比较。

| Token | test-zh |  | test-en |  |
| --- | --- | --- | --- | --- |
| CER (%) ↓ | SS ↑ | WER (%) ↓ | SS ↑ |
| Groundtruth | 0.972 | - | 2.156 | - |
| CosyVoice | 2.857 | 0.849 | 4.519 | 0.807 |
| Step-Audio-TTS-3B | 2.192 | 0.784 | 3.585 | 0.742 |

#### 6.2.2 TTS

为评估 Step-Audio 的 TTS 性能，我们使用了 SEED TTS 测试数据集（[Anastassiou et al., 2024]）。模型被要求复现原始输入文本。尽管这一做法无法保证输入与输出内容的一致性，我们认为错误的输出也在客观上反映了模型遵循指令的能力。因此，我们分别采用 Paraformer（[Z. Gao et al., 2022]）与 Whisper-Large-V3（[Radford et al., 2023]）计算中文与英文的错误率。结果汇总于表 2。Step-Audio 在开源口语模型中取得了最佳的 CER 与 WER 表现。

对于 TTS 任务，我们使用 Paraformer（[Z. Gao et al., 2022]）与 Whisper-Large-v3（[Radford et al., 2023]）在 SEED 测试集上评估开源 TTS 模型的表现，并采用 ERes2Net（[Y. Chen et al., 2023]）模型评估说话人相似度。结果汇总于表 3。我们采用双码本的 30 亿参数版本 Step-Audio-TTS-3B 在开源模型中于 CER 与 WER 上取得 SoTA 结果，同时展现出极具竞争力的相似度分数。值得注意的是，将 LLM 扩展到 1300 亿参数在 CER 与 WER 上均带来大幅提升，暗示进一步扩展合成数据与模型参数的潜在收益。

为评估双码本方法的收益，我们在上述 SEED 测试集上比较了各种 token 的重合成质量，包括：CosyVoice 单码本（[Du, Chen et al., 2024]）与双码本。测试语音首先被量化为离散 token，然后经 token2wav 过程重建为波形。我们从语音可懂度与说话人相似度两方面评估 token 的质量。比较结果见表 4，表明双码本方法在保持说话人相似度可接受的退化水平的同时，取得了更低的 CER。

#### 6.2.3 AQTA 对话

如表 5 所示，我们使用 6.1 节提到的 StepEval-Audio-360 基准比较了 Step-Audio 与开源模型的实时对话性能。各指标得分由 GPT-4o 自动评定。表中展示的是平均分，最佳结果以粗体显示。由于该基准的主要内容为中文，而 Moshi 几乎不具备中文理解能力，Moshi 的结果以「*」标注，仅供参考。结果表明 Step-Audio-Chat 在实时对话中表现出色。

- 事实性：Step-Audio-Chat 取得 66.4% 的最高分，显著超越其他模型。这表明 Step-Audio-Chat 提供的回应更准确、更可靠，紧密贴合事实信息。
- 相关性：以 75.2% 的得分，Step-Audio-Chat 在相关性上同样出色，展示了其针对用户查询生成贴合语境且有意义的回应的能力。
- 对话评分：以最高的整体对话评分（4.11），Step-Audio-Chat 提供了卓越的整体语音对话体验。该评分范围为 1（最低）到 5（最高），代表 GPT-4o 基于对话的文本输入与输出所做的综合评估。

表 5：StepEval-Audio-360 上语音对话基础能力比较。

| 模型 | 事实性（%）↑ | 相关性（%）↑ | 对话评分↑ |
| --- | --- | --- | --- |
| GLM4-Voice | 54.7 | 66.4 | 3.49 |
| Qwen2-Audio | 22.6 | 26.3 | 2.27 |
| Moshi* | 1.0 | 0 | 1.49 |
| Step-Audio-Chat | 66.4 | 75.2 | 4.11 |

表 6：语音对话模型在公开基准上的性能比较。Llama Question、Web Questions 与 TriviaQA 是公开可用的数据集，而 ComplexBench 与 HSK-6 的音频版本是本研究从公开文本语料库新构建的。由于缺少官方测试集，TriviaQA 的结果仅供参考并以「*」标注。Qwen2-Audio 与 Step-Audio-Chat 通过本地推理获得，其他模型（Moshi、Freeze-Omni、LUCY、MinMo）的结果取自其原始论文。值得注意的是，GLM4-Voice 在 HSK-6 与 ComplexBench 上的得分也通过本地推理生成。

| 模型 | Llama Question | Web Questions | TriviaQA* | ComplexBench | HSK-6 |
| --- | --- | --- | --- | --- | --- |
| GLM4-Voice | 64.7 | 32.2 | 39.1 | 66.0 | 74.0 |
| Moshi | 62.3 | 26.6 | 22.8 | - | - |
| Freeze-Omni | 72.0 | 44.7 | 53.9 | - | - |
| LUCY | 59.7 | 29.3 | 27.0 | - | - |
| MinMo | 78.9 | 55.0 | 48.3 | - | - |
| Qwen2-Audio | 52.0 | 27.0 | 37.3 | 54.0 | - |
| Step-Audio-Chat | 81.0 | 75.1 | 58.0 | 74.0 | 86.0 |

为进一步考察 Step-Audio-Chat 的表现，我们在若干公开可用数据集上进行了评估。其中，Web Questions、Llama Questions 与 TriviaQA 是知识型问答数据集，而 ComplexBench 与汉语水平考试（HSK-6）听力理解部分是综合性测试。我们对 Web Questions 与 Llama Questions 使用了完整测试集。对于缺少官方测试集真实答案的 TriviaQA，我们从开发集构建了一个 1000 样本的测试集。该子集分别包含来自 Wikipedia 与 Web 验证集的各 500 个样本，并辅以来自 Web 与 Wikipedia 开发集的数据。由于这一非标准测试集，TriviaQA 的结果应视为初步结果，仅供参考。Llama Questions 提供了语音形式的问题，而我们对 Web Questions、TriviaQA、ComplexBench 与 HSK-6 使用 TTS 生成了语音版本的问题，以进行音频问题-文本回答（AQTA）评估。

Moshi（[Défossez et al., 2024]）、Freeze-Omni（[Wang et al., 2024]）、LUCY（[H. Gao et al., 2025]）与 MinMo（[Q. Chen et al., 2025]）的性能数据取自其各自的论文。Step-Audio-Chat 与 Qwen2-audio（[Chu et al., 2024]）的结果通过本地 API 推理获得。对于 LUCY，我们报告其原文所呈现的阶段 2（S2）与阶段 3（S3）训练阶段中的最佳结果。GPT-4o 用于对照原始文本问题评估模型文本回应的准确性。表 6 给出了平均准确率分数，表明 Step-Audio-Chat 在所有开源基准上均取得最高准确率。Step-Audio-Chat 在 Llama Question 数据集上的准确率分数以斜体标示，表示我们修正了评估集中的若干错误。除自动化指标外，我们还进行了如图 1 所示的人工评估。结果与自动化评估相互印证，显示 Step-Audio 在所有评估维度上均具有清晰且一致的优势。

### 6.3 指令遵循

音频指令遵循反映了模型针对输入指令生成准确音频与文本内容的能力。为此，我们开发了音频指令遵循基准，涵盖语言、角色扮演、唱歌 / RAP 与语音控制等类别。评估包含指令遵循的准确性与生成语音的质量，均采用 1-5 的平均意见得分（MOS）量表。如表 7 所示，Step-Audio-Chat 分别在音频指令遵循与音频质量上展现出有竞争力的结果。

表 7：GLM4-Voice 与 Step-Audio-Chat 的音频指令遵循性能比较

| 类别 | 指令遵循 |  | 音频质量 |  |
| --- | --- | --- | --- | --- |
| GLM-4-Voice | Step-Audio | GLM-4-Voice | Step-Audio |
| 语言 | 1.9 | 3.8 | 2.9 | 3.3 |
| 角色扮演 | 3.8 | 4.2 | 3.2 | 3.6 |
| 唱歌 / RAP | 2.1 | 2.4 | 2.4 | 4 |
| 语音控制 | 3.6 | 4.4 | 3.3 | 4.1 |

### 6.4 工具调用

所提出的 Step-Audio 系统支持语音交互中的实时工具调用。由于实时文本回应与其对应音频流之间存在显著的比特率差异，我们的框架在保持无缝语音交互的同时实现了异步工具调用。如图 7 所示，该架构将基于文本的工具处理与音频生成流水线解耦，允许外部服务查询（如知识检索）与语音合成并行执行。这一设计消除了需要工具调用时等待音频渲染的时间，显著提升了交互流畅度。

![Refer to caption](2502.11946v2/figure/toolcall_2.drawio.png)

图 7：Step-Audio 中异步工具调用的架构。文本处理线程处理工具调用，而音频生成线程并发地产出语音流。

## 7 结论

本文提出了 Step-Audio，一个用于实时语音交互的创新框架。在预训练阶段，我们的双码本语音 tokenizer 使用 3.3T token 的多模态数据连接文本与声学模态，建立跨模态对齐。在后训练阶段，我们针对 TTS 与 ASR 任务进行了任务特定的 SFT，同时针对 AQTA 任务实施多样化高质量数据集的 SFT 结合 RLHF 以提升回应质量，实现了对情感调节、方言适配与韵律模式生成的细粒度控制。通过切片延迟补偿的推测式流式传输与高效的全双工协调等工程创新，Step-Audio 实现了流畅的对话动态。包括 ASR、TTS 与 AQTA 在内的各任务基准评估的性能指标，展示了 Step-Audio 在语音对话中的卓越能力。

## 8 未来工作

在本工作中，我们展示了 Step-Audio 当前在语音与文本跨模态集成方面的能力，这是 Step-Audio 面向三模态系统的初步实现的一部分。展望未来，三个关键领域值得进一步探索：第一，扩展框架以实现融合视觉、语音与文本的原生三模态理解；第二，通过在 AQAA 场景中消除中间跨模态转换来提升纯语音对话效率；第三，实现深度思考增强的工具调用，以增强与外部知识库的智能交互能力。

## 参考文献

- Anastassiou et al. ((2024))

  Anastassiou, P., Chen, J., Chen, J., Chen, Y., Chen, Z., Chen, Z.others
  (2024).
  Seed-tts: A family of high-quality versatile speech generation models.
  arXiv preprint arXiv:2406.02430 .
- Bradley & Terry ((1952))

  Bradley, R.A. & Terry, M.E.
  (1952).
  Rank analysis of incomplete block designs: I. the method of paired comparisons.
  Biometrika 39 324.
   <https://api.semanticscholar.org/CorpusID:125209808>
- bytedance ((2024))

  bytedance.
  (2024).
  doubaovoice.
  <https://team.doubao.com/zh/special/realtime_voice>.
  Accessed: 2024
- Q. Chen et al. ((2025))

  Chen, Q., Chen, Y., Chen, Y., Chen, M., Chen, Y., Deng, C.others
  (2025).
  Minmo: A multimodal large language model for seamless voice interaction.
  arXiv preprint arXiv:2501.06282 .
- Y. Chen et al. ((2023))

  Chen, Y., Zheng, S., Wang, H., Cheng, L., Chen, Q. & Qi, J.
  (2023).
  An enhanced res2net with local and global feature fusion for speaker verification.
  arXiv preprint arXiv:2305.12838 .
- Chu et al. ((2024))

  Chu, Y., Xu, J., Yang, Q., Wei, H., Wei, X., Guo, Z.others
  (20241).
  Qwen2-audio technical report.
  arXiv preprint arXiv:2407.10759 .
- Chu et al. ((2024))

  Chu, Y., Xu, J., Yang, Q., Wei, H., Wei, X., Guo, Z.others
  (20242).
  Qwen2-audio technical report.
  arXiv preprint arXiv:2407.10759 .
- Das et al. ((2024))

  Das, N., Dingliwal, S., Ronanki, S., Paturi, R., Huang, Z., Mathur, P.others
  (2024).
  Speechverse: A large-scale generalizable audio language model.
  arXiv preprint arXiv:2405.08295 .
- Défossez et al. ((2024))

  Défossez, A., Mazaré, L., Orsini, M., Royer, A., Pérez, P., Jégou, H.Zeghidour, N.
  (2024).
  Moshi: a speech-text foundation model for real-time dialogue.
  arXiv preprint arXiv:2410.00037 .
- Du, Chen et al. ((2024))

  Du, Z., Chen, Q., Zhang, S., Hu, K., Lu, H., Yang, Y.others
  (2024).
  Cosyvoice: A scalable multilingual zero-shot text-to-speech synthesizer based on supervised semantic tokens.
  arXiv preprint arXiv:2407.05407 .
- Du, Wang et al. ((2024))

  Du, Z., Wang, Y., Chen, Q., Shi, X., Lv, X., Zhao, T.others
  (2024).
  Cosyvoice 2: Scalable streaming speech synthesis with large language models.
  arXiv preprint arXiv:2412.10117 .
- Dubey et al. ((2024))

  Dubey, A., Jauhri, A., Pandey, A., Kadian, A., Al-Dahle, A., Letman, A.others
  (2024).
  The llama 3 herd of models.
  arXiv preprint arXiv:2407.21783 .
- Fang et al. ((2024))

  Fang, Q., Guo, S., Zhou, Y., Ma, Z., Zhang, S. & Feng, Y.
  (2024).
  Llama-omni: Seamless speech interaction with large language models.
  arXiv preprint arXiv:2409.06666 .
- H. Gao et al. ((2025))

  Gao, H., Shao, H., Wang, X., Qiu, C., Shen, Y., Cai, S.others
  (2025).
  Lucy: Linguistic understanding and control yielding early stage of her.
  arXiv preprint arXiv:2501.16327 .
- Z. Gao et al. ((2022))

  Gao, Z., Zhang, S., McLoughlin, I. & Yan, Z.
  (2022).
  Paraformer: Fast and accurate parallel transformer for non-autoregressive end-to-end speech recognition.
  arXiv preprint arXiv:2206.08317 .
- Hu et al. ((2024))

  Hu, S., Zhou, L., Liu, S., Chen, S., Meng, L., Hao, H.others
  (2024).
  Wavllm: Towards robust and adaptive speech large language model.
  arXiv preprint arXiv:2404.00656 .
- Huang et al. ((2024))

  Huang, R., Li, M., Yang, D., Shi, J., Chang, X., Ye, Z.others
  (2024).
  Audiogpt: Understanding and generating speech, music, sound, and talking head.
  In Proceedings of the aaai conference on artificial intelligence ( 38, 23802–23804).
- Hurst et al. ((2024))

  Hurst, A., Lerer, A., Goucher, A.P., Perelman, A., Ramesh, A., Clark, A.others
  (2024).
  Gpt-4o system card.
  arXiv preprint arXiv:2410.21276 .
- Kong et al. ((2020))

  Kong, Q., Cao, Y., Iqbal, T., Wang, Y., Wang, W. & Plumbley, M.D.
  (2020).
  Panns: Large-scale pretrained audio neural networks for audio pattern recognition.
  IEEE/ACM Transactions on Audio, Speech, and Language Processing 28 2880–2894.
- Ming et al. ((2024))

  Ming, R., Wu, J., Huang, Z., Ju, Z., Hu, J., Peng, L. & Zhou, S.
  (2024).
  Advancing auto-regressive continuation for video frames.
  arXiv preprint arXiv:2412.03758 .
- Nguyen et al. ((2024))

  Nguyen, T.A., Muller, B., Yu, B., Costa-Jussa, M.R., Elbayad, M., Popuri, S.others
  (2024).
  Spirit-lm: Interleaved spoken and written language model.
  arXiv preprint arXiv:2402.05755 .
- Radford et al. ((2023))

  Radford, A., Kim, J.W., Xu, T., Brockman, G., McLeavey, C. & Sutskever, I.
  (2023).
  Robust speech recognition via large-scale weak supervision.
  In International conference on machine learning ( 28492–28518).
- Rouard et al. ((2023))

  Rouard, S., Massa, F. & Défossez, A.
  (2023).
  Hybrid transformers for music source separation.
  In Icassp 23.
- Schulman et al. ((2017))

  Schulman, J., Wolski, F., Dhariwal, P., Radford, A. & Klimov, O.
  (2017).
  Proximal policy optimization algorithms.
  arXiv preprint arXiv:1707.06347 .
- StepFun ((2024))

  StepFun.
  (20241).
  Step-1: A 130b large language model.
  <https://platform.stepfun.com/docs/llm/text>.
  Accessed: February 2024
- StepFun ((2024))

  StepFun.
  (20242).
  Step-2.
  <https://platform.stepfun.com/docs/llm/text>.
  Accessed: February 2024
- Wang et al. ((2024))

  Wang, X., Li, Y., Fu, C., Shen, Y., Xie, L., Li, K.Ma, L.
  (2024).
  Freeze-omni: A smart and low latency speech-to-speech dialogue model with frozen llm.
  arXiv preprint arXiv:2411.00774 .
- Xie & Wu ((2024))

  Xie, Z. & Wu, C.
  (2024).
  Mini-omni: Language models can hear, talk while thinking in streaming.
  arXiv preprint arXiv:2408.16725 .
- Zeng et al. ((2024))

  Zeng, A., Du, Z., Liu, M., Wang, K., Jiang, S., Zhao, L.Tang, J.
  (2024).
  Glm-4-voice: Towards intelligent and human-like end-to-end spoken chatbot.
  arXiv preprint arXiv:2412.02612 .
- Zhang et al. ((2024))

  Zhang, Z., Zhong, Y., Ming, R., Hu, H., Sun, J., Ge, Z.Jin, X.
  (2024).
  Disttrain: Addressing model and data heterogeneity with disaggregated training for multimodal large language models.
  arXiv preprint arXiv:2408.04275 .

## 致谢

我们将核心贡献者定义为全程参与 Step-Audio 研发的人员，而贡献者则指参与早期版本或部分时间贡献的人员。所有贡献者按名字的字母顺序列出。

- 核心贡献者：

  - 音频模型与训练：Ailin Huang, Boyong Wu, Bruce Wang, Chao Yan, Chen Hu, Chengli Feng, Fei Tian, Feiyu Shen, Jingbei Li, Mingrui Chen, Peng Liu, Ruihang Miao, Wang You, Xi Chen, Xuerui Yang, Yechang Huang, Yuxiang Zhang, Zheng Gong, Zixin Zhang。
  - 基础模型与训练：Hongyu Zhou, Jianjian Sun。
  - 基础设施：Brian Li, Chengting Feng, Changyi Wan, Hanpeng Hu, Jianchang Wu, Jiangjie Zhen, Ranchen Ming, Song Yuan, Xuelin Zhang, Yu Zhou。
  - 数据与评估：Bingxin Li, Buyun Ma, Hongyuan Wang, Kang An, Wei Ji, Wen Li, Xuan Wen, Xiangwen Kong, Yuankai Ma, Yuanwei Liang, Yun Mou。
- 贡献者：
  Bahtiyar Ahmidi, Bin Wang, Bo Li, Changxin Miao, Chen Xu, Chenrun Wang, Dapeng Shi, Deshan Sun, Dingyuan Hu, Dula Sai, Enle Liu, Guanzhe Huang, Gulin Yan, Heng Wang, Haonan Jia, Haoyang Zhang, Jiahao Gong, Junjing Guo, Jiashuai Liu, Jiahong Liu, Jie Feng, Jie Wu, Jiaoren Wu, Jie Yang, Jinguo Wang, Jingyang Zhang, Junzhe Lin, Kaixiang Li, Lei Xia, Li Zhou, Liang Zhao, Longlong Gu, Mei Chen, Menglin Wu, Ming Li, Mingxiao Li, Mingliang Li, Mingyao Liang, Na Wang, Nie Hao, Qiling Wu, Qinyuan Tan, Ran Sun, Shuai Shuai, Shaoliang Pang, Shiliang Yang, Shuliang Gao, Shanshan Yuan, Siqi Liu, Shihong Deng, Shilei Jiang, Sitong Liu, Tiancheng Cao, Tianyu Wang, Wenjin Deng, Wuxun Xie, Weipeng Ming, Wenqing He, Wen Sun, Xin Han, Xin Huang, Xiaomin Deng, Xiaojia Liu, Xin Wu, Xu Zhao, Yanan Wei, Yanbo Yu, Yang Cao, Yangguang Li, Yangzhen Ma, Yanming Xu, Yaoyu Wang, Yaqiang Shi, Yilei Wang, Yizhuang Zhou, Yinmin Zhong, Yang Zhang, Yaoben Wei, Yu Luo, Yuanwei Lu, Yuhe Yin, Yuchu Luo, Yuanhao Ding, Yuting Yan, Yaqi Dai, Yuxiang Yang, Zhe Xie, Zheng Ge, Zheng Sun, Zhewei Huang, Zhichao Chang, Zhisheng Guan, Zidong Yang, Zili Zhang。
- 项目发起人：
  Binxing Jiao, Daxin Jiang, Heung-Yeung Shum, Jiansheng Chen, Jing Li, Shuchang Zhou, Xiangyu Zhang, Xinhao Zhang, Yibo Zhu。
- 通讯作者：Daxin Jiang（djiang@stepfun.com）、Shuchang Zhou（scotzhou@stepfun.com）、Chen Hu（hatcher@stepfun.com）、Bruce Wang（brucewang@stepfun.com）
