---
title: "GLM-4-Voice：迈向智能拟人的端到端语音交互"
title_en: "GLM-4-Voice: Towards Intelligent and Human-Like End-to-End Spoken Chatbot"
arxiv: 2412.02612
date: 2024-12-03
source: https://arxiv.org/abs/2412.02612
crawled: 2026-09-22
translated: 2026-09-22
---

# GLM-4-Voice：迈向智能拟人的端到端语音交互

> 原文：[GLM-4-Voice](https://arxiv.org/abs/2412.02612) · 智谱 Z.ai arXiv

Aohan Zeng‡§*　Zhengxiao Du‡§*　Mingdao Liu‡　Kedong Wang§　Shengmin Jiang§　Lei Zhao§

机构：Yuxiao Dong‡、Jie Tang‡

机构：§Zhipu.AI（智谱 AI）　‡清华大学

机构：<https://github.com/THUDM/GLM-4-Voice>

###### 摘要

我们推出 GLM-4-Voice，一个智能、拟人的端到端语音对话机器人。它支持中英双语，可进行实时语音对话，并能根据用户指令调整情感、语调、语速、方言等语音细节。GLM-4-Voice 使用超低比特率（175bps）、单码本、帧率 12.5Hz 的语音分词器（speech tokenizer），该分词器由自动语音识别（ASR）模型在编码器中引入矢量量化瓶颈改造而来。为了高效地将知识从文本模态迁移到语音模态，我们使用文本到 token（text-to-token）模型从现有文本预训练语料中合成语音-文本交错数据。我们从预训练文本语言模型 GLM-4-9B 出发继续预训练，混合使用无监督语音数据、语音-文本交错数据与监督语音-文本数据，规模扩展至 1 万亿 token，在语音语言建模与语音问答两项任务上均取得当前最优（state-of-the-art）表现。随后，我们使用高质量对话语音数据对预训练模型进行微调，在对话能力与语音质量两方面均取得优于现有基线的表现。开源模型可通过 <https://github.com/THUDM/GLM-4-Voice> 与 <https://huggingface.co/THUDM/glm-4-voice-9b> 获取。

> 注：\* 表示同等贡献，联系邮箱：{zah22,zx-du20}@mails.tsinghua.edu.cn；本工作完成于 Mingdao Liu 与 Lei Zhao 在智谱 AI（Zhipu.AI）实习期间。

## 1 引言

大语言模型（LLM）的成功推动了对话式 AI 的显著进步，使基于文本的聊天机器人与数字助手得以发展。然而，LLM 主要被设计为处理文本输入并生成文本输出，聚焦于语义与逻辑层面的交流。相比之下，人类的交流超越了语义，往往还传递情感与微妙的细节。因此，基于语音的交互为人机交互提供了更自然、更直观的媒介，带来更丰富、更具吸引力的用户体验。传统语音对话机器人通常依赖一条由自动语音识别（ASR）、LLM 处理与文本转语音（TTS）合成组成的流水线。这种方案虽然可用，但常受制于高延迟、ASR 与 TTS 阶段引入的误差累积，以及捕获与表达情感细腻度的能力有限。

语音语言模型（SpeechLM）以端到端方式同时处理语音输入与输出，为构建语音对话机器人提供了一条有前景的路径。[24, 17] 等工作探索了以类似大语言模型的方式在语音数据上进行预训练。类似地，Défossez 等 [12] 将语音数据扩展到 700 万小时用于模型训练。然而，这些方法面临一个重大局限：与互联网上庞大的文本语料相比，语音数据相对稀缺。这种数据失衡使得模型难以充分借助基于文本的 LLM 的能力，最终制约了 SpeechLM 的智能水平。另一些方法致力于对齐语音与文本模态 [15, 42]，将语音编码器与文本转语音模块接入现有 LLM，并在口语对话数据集上微调。这种方式虽然提供了从 LLM 出发构建语音到语音模型的直接途径，但由于缺乏专门的语音预训练，无法生成真正拟人的语音输出。这一局限阻碍了模型捕捉人类语音中固有的丰富细节与表现力。

本文推出 GLM-4-Voice，一个智能、拟人的语音对话机器人。我们使用帧率 12.5Hz 的单码本监督语音分词器来高效表示语音，并采用基于流匹配（flow matching）的语音解码器将语音 token 转换为自然动听的语音。为弥合文本与语音模态之间的鸿沟，我们使用 1 万亿 token 进行大规模语音-文本预训练，其中包括由文本预训练数据合成的交错语音-文本语料，以及无监督语音数据和监督语音-文本数据集（如 ASR 与 TTS）。所得基座模型在语音语言建模、语音问答、ASR、TTS 等多种任务上均表现出色。为进一步增强对话机器人的对话能力，我们使用「流式思考（Streaming Thoughts）」模板在高质量对话数据集上对基座模型进行微调。该模板交替输出文本与语音 token，提升了模型生成无缝、低延迟响应的能力，同时保持高质量的表现。

## 2 相关工作

### 2.1 语音分词

语音分词器将一段音频片段转换为离散 token，可分为两个方向。神经声学编解码器 [44, 11, 23, 20] 旨在以低比特率重建高质量音频。语义 token [19, 10] 则从在语音数据上以自监督方式学习到的语音表示中提取。近来，SpeechTokenizer [48] 与 Mimi [12] 将语义 token 与声学 token 统一为不同的残差矢量量化（RVQ）层，但它们在相同位置仍会产生多个 token，导致要么需要对语义与声学 token 进行并行预测，要么在用于语言模型时退化为语义分词器。CosyVoice [14] 提出了由语音识别模型导出的监督语义分词器，并成功将该分词器应用于文本转语音合成，但尚未探索该分词器在语音语言建模中的应用。

### 2.2 语音语言建模

语音语言模型是在无监督语音数据上预训练的自回归模型。Lakhotia 等 [24] 首次提出生成式口语语言建模（GSLM），在自监督学习产生的离散语义 token 上训练下一 token 预测目标。AudioLM [5] 提出混合分词方案，将这些语义 token 与来自神经音频编解码器 [44] 的声学 token 相结合。TWIST [17] 使用预训练文本语言模型 OPT [47] 热启动（warm-start）训练语音语言模型。Moshi [12] 将 TWIST 中自然语音数据的规模扩大到 700 万小时。Spirit-LM [32] 在 TWIST 的基础上进一步加入从语音-文本平行语料中整理的语音-文本交错数据。然而，语音-文本平行语料的稀缺限制了交错数据的规模。

### 2.3 端到端语音对话机器人

早期的语音到语音模型工作主要聚焦于语音翻译等处理任务 [8, 2]。自 ChatGPT 在文本聊天机器人上取得成功以来，许多工作探索了开发能够以语音理解并以语音应答的语音聊天机器人的方法。SpeechGPT [46] 提出将现有大语言模型（LLM）与离散语音表示相结合，以获得语音对话能力。Moshi [12] 基于其预训练语音语言模型提出全双工口语对话框架。Qwen-Audio [9] 通过对齐 Whisper [36] 编码器的语音表示，改造预训练文本语言模型以实现语音理解。该模型能够理解语音，但无法生成语音。Llama-Omni [15] 与 Freeze-Omni [41] 在该方法基础上于语言模型之后添加文本转语音模型，将文本输出转换为语音输出。这样一来，语言模型只能控制语音的内容，而无法控制风格与韵律。Mini-Omni [42] 仅用指令数据集直接微调语言模型，使其同时生成文本与语音响应。正如我们将在实验中展示的，若没有语音预训练，文本与语音响应的质量都会受到严重限制。

## 3 模型架构

本节介绍 GLM-4-Voice 的架构。我们的目标是构建一个智能水平高的拟人端到端语音对话机器人。为此，模型必须：1) 理解用户语音并给出语义准确的响应；2) 遵循用户的口语指令，生成具备符合用户期望的副语言（paralinguistic）特征的语音。受 LLM 成功的「预训练 + 微调」范式启发，我们相信语音对话机器人的这些能力最好通过在多样化语音语料上的大规模预训练来培养，而非像近来的语音对话机器人方案 [15, 42] 那样，简单地用语音问答数据微调现有 LLM。

为实现这一目标，GLM-4-Voice 在自回归 Transformer 架构的基础上仅做最小改动。在语音分词方面，我们使用监督语音分词器，以超低比特率（175bps）有效捕获语义信息，同时保持高质量的语音重建。此外，语音分词采用单码本方案，避免了多层语音 token 生成 [12, 42] 常需要的复杂架构调整。这一做法有助于在实现高效语音建模的同时保留模型的文本处理能力。而且，模型对输入与输出采用统一的语音表示，可对语音数据执行下一 token 预测，从而在无监督语音语料上高效预训练。

我们使用与 Zeng 等 [45] 中所述相同的语音分词器与语音解码器。为实现低延迟交互，我们将语音解码器改造为支持流式推理，并设计了能够在监督微调阶段交替输出文本与语音 token 的流式思考模板，详见 3.3 节与 3.2 节。

### 3.1 语音分词器

图 1：GLM-4-Voice 的语音分词器与语音解码器架构。

语音分词器将连续波形转换为离散语音 token，这些 token 保留语义信息与部分声学信息。以往方法可分为两个方向。声学分词器以语音波形的重建/对抗目标训练。声学 token 保留了足以重建原始音频的信息，但若要表示额外信息，要么依赖较高的采样率（即每秒 token 数），要么依赖残差矢量量化 [44]（即多个堆叠的码本）。语义 token 则从在自动发现的语音单元上通过自监督学习得到的表示中提取 [19]。语义 token 丢弃了表示语音语义含义所不需要的额外信息，但也导致语音合成质量下降与声学细节的丢失 [31]。面向语音-文本语言建模的理想语音分词器应具备若干关键特性：1) 采样率低且单码本，以支持自回归生成；2) 与文本对齐，以迁移预训练语言模型的知识；3) 支持高质量语音合成。

我们采用 Zeng 等 [45] 中描述的 12.5Hz 语音分词器变体。为使本文自洽，我们简要介绍语音分词器的架构。受文本转语音合成中监督语义分词器 [14] 的启发，我们在预训练自动语音识别模型（我们使用 Whisper 家族中的 whisper-large-v3 [36]）的编码器中部加入额外的池化层与矢量量化层 [40] 进行微调。码本向量以指数移动平均（EMA）方式学习，并参照 Dhariwal 等 [13] 的做法，将平均使用率低于某一阈值的向量在量化前重置为随机选取的连续表示，以克服码本坍缩（codebook collapse）。

##### 面向流式推理的因果性

为了在推理时支持输入语音的流式编码，我们参照 [45] 改造 Whisper 编码器的架构以引入因果性。具体而言，我们将编码器 Transformer 之前的卷积层替换为因果卷积 [39]，并将编码器中的双向注意力替换为块因果注意力（block causal attention）。

表 1：语音分词器与解码器的评测结果。LS 表示 LibriSpeech。LibriSpeech（英语）以词错误率（WER）度量，AISHELL-1（中文）以字符错误率（CER）度量。我们对 ASR 模型 whisper-large-v3 施加矢量量化并配合各种池化层进行微调，得到不同采样率的分词器。在 GLM-4-Voice 的后续研发中，我们选择了 12.5Hz 变体。

| 分词器 | 帧率 | 比特率（bps） | ASR：LS-clean ↓ | ASR：LS-other ↓ | ASR：AISHELL-1 ↓ | 重建：WER ↓ | 重建：VisQOL ↑ | 重建：MOSNet ↑ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SpeechTokenizer | 50Hz | 1.50K | ∅ | ∅ | ∅ | 9.97 | 1.53 | 2.67 |
| SpeechTokenizer | 50Hz | 4.00K | ∅ | ∅ | ∅ | 6.32 | 3.07 | 3.10 |
| Moshi (Mimi) | 12.5Hz | 1.10K | ∅ | ∅ | ∅ | 8.36 | 2.82 | 2.89 |
| whisper-large-v3 | 50Hz | - | 2.50 | 4.53 | 9.31 | ∅ | ∅ | ∅ |
| SenseVoice-Large | 50Hz | - | 2.57 | 4.28 | 2.09 | ∅ | ∅ | ∅ |
| GLM-4-Voice-Tokenizer | 12.5Hz | 175 | 2.10 | 4.90 | 3.02 | 8.43 | 2.52 | 3.39 |
|  | 50Hz | 600 | 1.85 | 3.78 | 2.70 | 6.24 | 2.67 | 3.38 |
|  | 25Hz | 300 | 1.94 | 4.16 | 2.86 | 6.80 | 2.60 | 3.33 |
|  | 6.25Hz | 100 | 14.41 | 2.34 | 3.24 | 14.41 | 2.34 | 3.24 |

##### 训练细节

我们用一组 ASR 数据集微调矢量量化的 Whisper 模型，包括 LibriSpeech [34]、GigaSpeech [7]、MLS-Eng [35]、Wenet [43]、CommonVoice [3]、AISHELL-1 [6]，以及一个 1 万小时的专有中文 ASR 数据集。我们还纳入 70 万小时的无监督语音数据，其伪标签由 whisper-large-v3 [36]（英语）与 paraformer-large [1]（中文）生成。我们所有的语音分词器均从 whisper-large-v3 微调 2 个 epoch，批大小为 4096，学习率为 1e-5。监督样本与伪标签样本的比例为 1:3。码本向量以衰减系数 0.99 的指数移动平均更新，承诺损失（commitment loss）系数为 10.0。为减少平均池化带来的信息损失，我们在采样率降低时增大码本尺寸。

##### 评测

我们通过微调后 ASR 模型的准确率来度量语音 token 中语义信息的保留程度。LibriSpeech [34] 与 AISHELL-1 [6] 上的结果见表 1，并以 whisper-large-v3 [36] 与 SenseVoice-Large [1] 为基线。总体而言，各分词器都保留了足够的语义信息，可实现准确的 ASR 表现。结合下一节的重建结果，我们为 GLM-4-Voice 选择了 12.5Hz 分词器。

### 3.2 语音解码器

语音解码器从离散语音 token 合成语音波形，对确保生成语音的质量与表现力至关重要。为尽量降低语音交互的延迟，解码器还必须支持流式推理。与 Zeng 等 [45] 一致，我们采用 CosyVoice [14] 的解码器架构，它由语音 token 编码器、条件流匹配模型 [28] 与 HiFi-GAN 声码器 [22] 组成。

##### 训练细节

我们从零开始训练语音 token 编码器与流匹配模型，采用两阶段训练范式，以充分利用质量参差的海量语音数据。预训练阶段使用各种说话人、各种质量的无监督语音数据中的全部语音样本；微调阶段使用单一说话人的高质量语音样本。

##### 对流式推理的支持

为支持流式推理并降低延迟，我们在微调阶段加入截断的音频样本（即音频的前 $n\cdot b$ 秒，其中 $n=1,2,3,\ldots$，$b$ 为块大小），使模型能有效应对流式场景。推理时，解码器处理音频前 $n\cdot b$ 秒对应的语音 token，以前 $(n-1)b$ 秒的语音作为提示（prompt），预测 $(n-1)b$ 秒至 $n\cdot b$ 秒之间的语音内容。这种做法使模型能够以最低 $b$ 秒的延迟生成语音 token。基于经验研究，我们为 GLM-4-Voice 设定 $b=0.8$，这意味着至少需要 10 个语音 token 才能生成初始语音输出。

##### 评测

我们引用 Zeng 等 [45] 的重建结果来展示我们的语音解码器在低比特率语音 token 下的表现。我们在 LibriSpeech [34] 的语音重建任务上评测语音解码器，并将我们的分词器与 SpeechTokenizer [48] 和 Mimi [12] 进行比较。参照 Défossez 等 [12]，我们还评测了仅保留前 3 层 RVQ 以获得 1.5kbps 比特率的 SpeechTokenizer 变体。表 1 表明，我们的语音解码器在各采样率下均表现良好，其中 12.5Hz 变体在效率与质量之间取得最佳平衡：它在显著降低比特率（175）的同时，保持了较高的质量得分（MOSNet 3.39）与内容保留度（WER 8.43）。

### 3.3 推理

##### 语音到语音任务的解耦

![图 2](2412.02612v1/overall-arch.png)

图 2：左：GLM-4-Voice 两个训练阶段的数据构建。右：GLM-4-Voice 的模型架构。

理想的语音语言模型应仅在语音 token 上运行，直接完成语音到语音任务。然而，鉴于大语言模型的成功，以及「文本表达了大多数语音的语义内容」这一假设，我们将语音到语音任务解耦为两个子任务：语音到文本，以及语音加文本到语音。给定用户语音输入 $Q_{s}$、对应文本响应 $A_{t}$ 与语音输出 $A_{s}$，任务定义如下：

- 语音到文本：模型根据用户语音输入 $Q_{s}$ 生成文本响应 $A_{t}$。
- 语音加文本到语音：模型同时利用 $Q_{s}$ 与 $A_{t}$，生成语音输出 $A_{s}$，并自适应地调整音调与韵律，以保证对话的连贯性。

我们在推理过程中采用这一解耦策略：模型先根据用户输入 $Q_{s}$ 生成文本答案 $A_{t}$，再同时利用 $Q_{s}$ 与 $A_{t}$ 生成 $A_{s}$。这样，语音响应 $A_{s}$ 的生成受文本响应 $A_{t}$ 的引导，从而提升表现。然而，这种做法会带来较高的首 token 延迟，因为必须等待 $A_{t}$ 完整生成后才能开始生成 $A_{s}$。为此，我们应用名为「流式思考（Streaming Thoughts）」的模板。如图 2 所示，给定 $Q_{s}$，模型按指定比例交替输出文本与语音 token，再将二者分别拼接为 $A_{t}$ 与 $A_{s}$。具体而言，基于我们的 12.5Hz 分词器，我们交替生成 13 个文本 token 与 26 个语音 token。选择 1:2 的比例是为了保证文本生成始终快于语音，否则生成的语音 token 将缺乏文本 token 提供的必要上下文。选择 26 个语音 token 则基于经验观察，使模型先产出一部分连贯的内容再进行合成，以确保合成语音的准确性。

##### 总体延迟

生成首个语音波形的总体响应延迟可按如下方式计算：

- 语音分词：用户语音输入由语音分词器以流式方式处理，分词器按固定大小 $t_{\text{block}}$ 的块进行操作。得益于流式设计，分词器立即开始处理，且无论语音总时长如何，只需花费处理当前块的时间。因此，分词延迟为：

$$T_{\text{speech\_tokenize}}=f_{\text{speech\_tokenize}}(t_{\text{block}})$$

- LLM 预填充（Prefilling）：分词器生成的语音 token 数 $N_{\text{speech\_tokens}}$ 取决于用户语音时长 $T_{\text{user\_speech}}$ 与帧率 $fr=12.5$（每秒 token 数）。LLM 的预填充延迟由下式给出：

$$T_{\text{llm\_prefill}}=f_{\text{llm\_prefill}}\left(fr\cdot T_{\text{user\_speech}}\right)$$

- LLM 解码：对于初始的语音响应，LLM 生成 13 个文本 token 与 10 个语音 token，共计 $N_{\text{first\_speech}}=13+10=23$ 个 token。这一步的解码延迟为：

$$T_{\text{llm\_decode}}=f_{\text{llm\_decode}}\left(N_{\text{first\_speech}}\right)$$

- 语音解码：$N_{\text{speech}}=10$ 个音频 token 由语音解码器处理，以生成首个音频块。这一步的延迟为：

$$T_{\text{speech\_decode}}=f_{\text{speech\_decode}}\left(N_{\text{speech}}\right)$$

总响应延迟为：

$$T_{\text{total}}=T_{\text{speech\_tokenize}}+T_{\text{llm\_prefill}}+T_{\text{llm\_decode}}+T_{\text{speech\_decode}}$$

## 4 训练流程

### 4.1 阶段一：语音-文本联合预训练

我们采用与 Zeng 等 [45] 相同的预训练数据与流程。这一阶段的主要目标是通过大规模语音预训练为 LLM 扩展语音建模能力。我们使用三类语音数据：

- 语音-文本交错数据：按 Zeng 等 [45] 所述由文本预训练数据合成，这类数据集促进文本与语音之间的跨模态知识迁移。
- 无监督语音数据：包含 70 万小时的语音数据，促使模型从真实世界的语音中学习。
- 监督语音-文本数据：同时包括 ASR 与 TTS 数据，提升模型在基础语音任务上的能力。

我们还混入文本预训练数据集，以保持文本性能。训练数据的统计见表 2。

#### 4.1.1 超参数

表 2：训练数据统计。

| 数据 | token 数（语音） | token 数（文本） | epoch 数 |
| --- | --- | --- | --- |
| Speech-Text | 455B | 279B | 0.90 |
| Speech-Only | 31B | - | 2.10 |
| ASR + TTS | 11B | 3.5B | 2.07 |
| Text-only | - | 10T | 0.03 |

我们从 GLM-4-9B-Base [16] 初始化 GLM-4-Voice，并扩展其词表以纳入语音 token。我们在 1 万亿 token 上进行预训练：文本数据固定采样占比 30%，无监督语音与监督语音-文本数据各训练一个 epoch，其余由语音-文本交错数据组成。训练语料的构成详见表 2。我们使用 AdamW [27] 优化器，$\beta_{1}=0.9$，$\beta_{2}=0.95$。模型以 8192 的序列长度训练，学习率从 $6\times 10^{-5}$ 线性衰减至 $6\times 10^{-6}$。

### 4.2 阶段二：监督微调

#### 4.2.1 数据构建

为打造拟人的语音对话机器人，我们使用以下两类数据：

- 多轮口语对话：这些对话主要派生自文本数据，经过仔细过滤以确保质量。我们排除了代码与数学相关的内容，以聚焦适合口语交互的对话材料。响应经过精修：缩短过长的文本、避免不适合口头表达的输出，并为精修后的对话合成对应的语音输出。为增强真实语音聊天场景中语音输入的多样性，标注人员朗读并录制了多种语音输入。
- 语音风格受控的口语对话：这一类别包含按特定语音风格要求定制的高质量多轮口语对话，例如语速、情感或方言。

#### 4.2.2 训练细节

如 3.3 节所述，我们将语音到语音任务解耦为两个子任务，并采用流式思考模板降低延迟。每个对话轮次由用户语音输入 $Q_{s}$、对应文本输入 $Q_{t}$、文本输出 $A_{t}$ 与对应语音输出 $A_{s}$ 组成。

我们观察到两个子任务的学习曲线存在差异：给定用户语音输入 $Q_{s}$，模型学习文本输出 $A_{t}$ 比学习语音输出 $A_{s}$ 更快。为弥合这一差异，我们将每个训练样本拆分为两部分：一部分掩蔽语音输出的损失，专注于从语音输入学习文本输出；另一部分掩蔽文本输出的损失，专注于从语音输入与文本输出共同学习语音输出。

模型在语音输出上微调 20 个 epoch，在文本输出上微调 4 个 epoch。学习率从 $1\times 10^{-5}$ 逐渐降低至 $1\times 10^{-6}$。为缓解过拟合，我们施加 0.1 的权重衰减，将隐藏层的 dropout 率设为 0.5，并将梯度裁剪至最大值 1.0。

## 5 评测

### 5.1 基座模型评测

我们用两个语音-文本任务评测基座模型：语音语言建模 [5] 与语音问答 [30]。对这两个任务，我们考虑两种设定：从语音上下文到语音生成（记作 S→S），以及从语音上下文到文本生成（记作 S→T）。对所有任务，我们使用火山引擎（VolcEngine）提供的多说话人 TTS API 合成上下文与后续内容（<https://www.volcengine.com/docs/6561/79820>）。

表 3：语音语言建模结果。Spirit-LM 的结果取自 Nguyen 等 [32]，其余结果取自 Défossez 等 [12]。

| 模型 | 模态 | 参数量 | Topic-StoryCloze | StoryCloze |
| --- | --- | --- | --- | --- |
| TWIST | S→S | 7B | 66.6 | 53.3 |
| Spirit-LM | S→S | 7B | 82.9 | 61.0 |
| Spirit-LM | S→T | 7B | 88.6 | 64.6 |
| Moshi | S→S | 7B | 83.0 | 60.8 |
| GLM-4-Voice | S→T | 9B | 93.6 | 76.3 |
| GLM-4-Voice | S→S | 9B | 82.9 | 62.4 |

##### 语音语言建模

该任务评测预训练模型对交错语音与文本的建模能力。给定上下文，模型需依据预测似然选出正确的后续内容。我们使用 Hassid 等 [17] 提出的两个数据集：口语版 StoryCloze 与口语版 Topic-StoryCloze，二者均由 StoryCloze 文本基准 [29] 转换而来。口语版 Topic-StoryCloze 比口语版 StoryCloze 更容易。基线结果取自 Défossez 等 [12]。

表 4：语音问答结果。基线结果取自 Défossez 等 [12]。

| 模型 | 模态 | 参数量 | Web Questions | Llama Questions | TriviaQA |
| --- | --- | --- | --- | --- | --- |
| TWIST | S→S | 7B | 1.5 | 4.0 | - |
| SpeechGPT | S→T | 7B | 6.5 | 21.6 | 14.8 |
| Spectron | S→T | 1B | 6.1 | 21.9 | - |
| Moshi | S→T | 7B | 26.6 | 62.3 | 22.8 |
| Moshi | S→S | 7B | 9.2 | 21.0 | 7.3 |
| GLM-4-Voice | S→T | 9B | 32.2 | 64.7 | 39.1 |
| GLM-4-Voice | S→S | 9B | 15.9 | 50.7 | 26.5 |

##### 语音问答

与 NLP 中的闭卷问答类似，语音问答要求语音语言模型在不访问外部知识库的情况下，回答关于广泛事实性知识的口语问题。我们在 Défossez 等 [12] 使用的 3 个数据集上评测模型：Web Questions [4]、Llama Questions [30] 与 TriviaQA [21]。基线结果取自 Défossez 等 [12]。

##### 结果

语音语言建模的结果见表 3，语音问答的结果见表 4。可以观察到，除 S→S 设定下的 Topic-StoryCloze 外，GLM-4-Voice 在 S→S 与 S→T 两种设定的所有评测任务上均优于基线。与同样同时支持语音与文本两种模态的 Moshi [12] 相比，无论答案是文本还是语音，我们的模型在语音问答上均更胜一筹。另一个观察是，S→T 设定的准确率总是优于 S→S 设定，在语音问答上尤为明显。因此，文本引导对于智能语音聊天机器人而言仍然必要。不过，我们的方法显著缩小了语音问答中口语答案与文本答案之间的差距（在 Llama Questions 上尤为明显），展现出发展直接语音到语音聊天机器人的潜力。

##### ASR / TTS

我们以预训练中 ASR / TTS 任务所用的相同提示格式提示基座模型。在 TTS 任务中，分别采用 Whisper-Large-V3 [36] 与 Paraformer-Large [38] 为英语与中文识别生成文本预测。在计算错误率之前，ASR 与 TTS 任务的文本预测分别使用 whisper-large-v3 的 tokenizer 与 CosyVoice [14] 流水线进行归一化。结果汇总于表 5。GLM-4-Voice 实现了与 whisper-large-v3 [36] 和 CosyVoice [14] 基线相当的 ASR 与 TTS 能力。

表 5：ASR 与 TTS 结果。LibriSpeech（英语）以词错误率（WER）度量，AISHELL-1（中文）以字符错误率（CER）度量。TTS 任务以 WER 度量。我们用 ∅ 表示模型不支持的任务与模态。

| 模型 | LibriSpeech test-clean | LibriSpeech test-other | AISHELL-1 test | LibriTTS test-clean | Seed-TTS test-en | Seed-TTS test-zh |
| --- | --- | --- | --- | --- | --- | --- |
| CosyVoice | ∅ | ∅ | ∅ | 3.17 | 3.39 | 3.10 |
| whisper-large-v3 | 2.50 | 4.53 | 9.31 | ∅ | ∅ | ∅ |
| GLM-4-Voice | 2.82 | 7.66 | 2.46 | 5.64 | 2.91 | 2.10 |

### 5.2 对话模型评测

##### ChatGPT 评分

为评测微调后对话模型的问答能力与知识记忆，我们使用 GPT-4o [33]（具体为 gpt-4o-2024-05-13）来评估模型响应的质量或正确性。对于通用问答（General QA）任务，我们采用 AlpacaEval [25] 中 helpful base 与 vicuna 子集的问题并去除数学相关题目，这与 Llama-Omni [15] 的对话评测数据集保持一致。我们请 GPT-4o 参照 MT-Bench [49] 的评测方法评估响应质量，并按 1 到 10 打分。对于知识（Knowledge）任务，我们从 Web Questions、Llama Questions 与 TriviaQA 中选取 100 道问题，向 GPT-4o 提供真实答案（ground-truth answer），请其判断模型的响应是否正确。表 6 中报告的分数是答案准确率，归一化到 0（0%）至 10（100%）的区间。用于评判的所有文本均为 Whisper-Large-V3 [36] 产生的音频转写，评分所用提示词见附录 A.1。

##### 语音质量

我们使用 UTMOS [37] 模型预测平均意见分（MOS），以评估生成语音的自然度。

##### 语音-文本一致性

为评测生成的文本响应与语音响应之间的对应关系，我们用 Whisper-Large-V3 [36] 将通用问答任务的语音响应转写为文本，然后计算转写文本与文本响应之间的词错误率（WER），即表 6 中的 ASR-WER(%)。GLM-4-Voice 是一个双语模型，有时会用中文响应回答英语提问，其 WER 无法直接计算。为了与仅支持英语的基线模型公平比较，在表 6 所报告的任务上评测时，我们将 GLM-4-Voice 的输出限制为英语 token。

表 6：对话模型评测结果。基线结果取自 Zeng 等 [45]。

| 模型 | ChatGPT 评分：通用问答 ↑ | ChatGPT 评分：知识 ↑ | UTMOS ↑ | ASR-WER ↓ |
| --- | --- | --- | --- | --- |
| SpeechGPT [46] | 1.40 | 2.20 | 3.86 | 66.57 |
| Mini-Omni [42] | 2.44 | 1.10 | 3.17 | 25.28 |
| Llama-Omni [15] | 3.50 | 3.90 | 3.92 | 9.18 |
| Moshi [12] | 2.42 | 3.60 | 3.90 | 7.95 |
| GLM-4-Voice | 5.40 | 5.20 | 4.45 | 5.74 |

## 6 结论

本文推出了 GLM-4-Voice，一个面向自然且富有表现力的语音交互而设计的端到端语音对话机器人。通过整合 12.5Hz 监督语音分词器、基于流匹配的语音解码器，以及在 1 万亿 token 语音-文本数据上的大规模预训练，GLM-4-Voice 有效弥合了文本与语音模态。它在语音语言建模、ASR、TTS 与语音问答等任务上取得强劲表现。以高质量对话数据集进行微调，进一步增强了其生成流畅、低延迟且富有细腻表现的响应的能力。GLM-4-Voice 的开放发布，将鼓励构建实用、可访问的语音 AI 系统的进一步探索。

## 参考文献

- [1]

  Keyu An, Qian Chen, Chong Deng, Zhihao Du, Changfeng Gao, Zhifu Gao, Yue Gu, Ting He, Hangrui Hu, Kai Hu, Shengpeng Ji, Yabin Li, Zerui Li, Heng Lu, Haoneng Luo, Xiang Lv, Bin Ma, Ziyang Ma, Chongjia Ni, Changhe Song, Jiaqi Shi, Xian Shi, Hao Wang, Wen Wang, Yuxuan Wang, Zhangyu Xiao, Zhijie Yan, Yexin Yang, Bin Zhang, Qinglin Zhang, Shiliang Zhang, Nan Zhao, and Siqi Zheng.
  Funaudiollm: Voice understanding and generation foundation models for natural interaction between humans and llms.
  *CoRR*, abs/2407.04051, 2024.
  URL <https://doi.org/10.48550/arXiv.2407.04051>.
- [2]

  Junyi Ao, Rui Wang, Long Zhou, Chengyi Wang, Shuo Ren, Yu Wu, Shujie Liu, Tom Ko, Qing Li, Yu Zhang, et al.
  Speecht5: Unified-modal encoder-decoder pre-training for spoken language processing.
  In *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 5723–5738, 2022.
- [3]

  Rosana Ardila, Megan Branson, Kelly Davis, Michael Kohler, Josh Meyer, Michael Henretty, Reuben Morais, Lindsay Saunders, Francis M. Tyers, and Gregor Weber.
  Common voice: A massively-multilingual speech corpus.
  In *Proceedings of The 12th Language Resources and Evaluation Conference, LREC 2020, Marseille, France, May 11-16, 2020*, pages 4218–4222. European Language Resources Association, 2020.
- [4]

  Jonathan Berant, Andrew Chou, Roy Frostig, and Percy Liang.
  Semantic parsing on freebase from question-answer pairs.
  In *Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing, EMNLP 2013, 18-21 October 2013, Grand Hyatt Seattle, Seattle, Washington, USA, A meeting of SIGDAT, a Special Interest Group of the ACL*, pages 1533–1544. ACL, 2013.
- [5]

  Zalán Borsos, Raphaël Marinier, Damien Vincent, Eugene Kharitonov, Olivier Pietquin, Matthew Sharifi, Dominik Roblek, Olivier Teboul, David Grangier, Marco Tagliasacchi, and Neil Zeghidour.
  Audiolm: A language modeling approach to audio generation.
  *IEEE ACM Trans. Audio Speech Lang. Process.*, 31:2523–2533, 2023.
- [6]

  Hui Bu, Jiayu Du, Xingyu Na, Bengu Wu, and Hao Zheng.
  AISHELL-1: an open-source mandarin speech corpus and a speech recognition baseline.
  In *20th Conference of the Oriental Chapter of the International Coordinating Committee on Speech Databases and Speech I/O Systems and Assessment, O-COCOSDA 2017, Seoul, South Korea, November 1-3, 2017*, pages 1–5. IEEE, 2017.
- [7]

  Guoguo Chen, Shuzhou Chai, Guan-Bo Wang, Jiayu Du, Wei-Qiang Zhang, Chao Weng, Dan Su, Daniel Povey, Jan Trmal, Junbo Zhang, Mingjie Jin, Sanjeev Khudanpur, Shinji Watanabe, Shuaijiang Zhao, Wei Zou, Xiangang Li, Xuchen Yao, Yongqing Wang, Zhao You, and Zhiyong Yan.
  Gigaspeech: An evolving, multi-domain ASR corpus with 10, 000 hours of transcribed audio.
  In *22nd Annual Conference of the International Speech Communication Association, Interspeech 2021, Brno, Czechia, August 30 - September 3, 2021*, pages 3670–3674. ISCA, 2021a.
- [8]

  Yi-Chen Chen, Po-Han Chi, Shu-wen Yang, Kai-Wei Chang, Jheng-hao Lin, Sung-Feng Huang, Da-Rong Liu, Chi-Liang Liu, Cheng-Kuang Lee, and Hung-yi Lee.
  Speechnet: A universal modularized model for speech processing tasks.
  *arXiv preprint arXiv:2105.03070*, 2021b.
- [9]

  Yunfei Chu, Jin Xu, Xiaohuan Zhou, Qian Yang, Shiliang Zhang, Zhijie Yan, Chang Zhou, and Jingren Zhou.
  Qwen-audio: Advancing universal audio understanding via unified large-scale audio-language models.
  *CoRR*, abs/2311.07919, 2023.
- [10]

  Yu-An Chung, Yu Zhang, Wei Han, Chung-Cheng Chiu, James Qin, Ruoming Pang, and Yonghui Wu.
  w2v-bert: Combining contrastive learning and masked language modeling for self-supervised speech pre-training.
  In *IEEE Automatic Speech Recognition and Understanding Workshop, ASRU 2021, Cartagena, Colombia, December 13-17, 2021*, pages 244–250. IEEE, 2021.
- [11]

  Alexandre Défossez, Jade Copet, Gabriel Synnaeve, and Yossi Adi.
  High fidelity neural audio compression.
  *Trans. Mach. Learn. Res.*, 2023, 2023.
- [12]

  Alexandre Défossez, Laurent Mazaré, Manu Orsini, Amélie Royer, Patrick Pérez, Hervé Jégou, Edouard Grave, and Neil Zeghidour.
  Moshi: a speech-text foundation model for real-time dialogue.
  Technical report, Kyutai, September 2024.
  URL <http://kyutai.org/Moshi.pdf>.
- [13]

  Prafulla Dhariwal, Heewoo Jun, Christine Payne, Jong Wook Kim, Alec Radford, and Ilya Sutskever.
  Jukebox: A generative model for music.
  *CoRR*, abs/2005.00341, 2020.
- [14]

  Zhihao Du, Qian Chen, Shiliang Zhang, Kai Hu, Heng Lu, Yexin Yang, Hangrui Hu, Siqi Zheng, Yue Gu, Ziyang Ma, Zhifu Gao, and Zhijie Yan.
  Cosyvoice: A scalable multilingual zero-shot text-to-speech synthesizer based on supervised semantic tokens, 2024.
  URL <https://arxiv.org/abs/2407.05407>.
- [15]

  Qingkai Fang, Shoutao Guo, Yan Zhou, Zhengrui Ma, Shaolei Zhang, and Yang Feng.
  Llama-omni: Seamless speech interaction with large language models, 2024.
  URL <https://arxiv.org/abs/2409.06666>.
- [16]

  Team GLM, Aohan Zeng, Bin Xu, Bowen Wang, Chenhui Zhang, Da Yin, Dan Zhang, Diego Rojas, Guanyu Feng, Hanlin Zhao, Hanyu Lai, Hao Yu, Hongning Wang, Jiadai Sun, Jiajie Zhang, Jiale Cheng, Jiayi Gui, Jie Tang, Jing Zhang, Jingyu Sun, Juanzi Li, Lei Zhao, Lindong Wu, Lucen Zhong, Mingdao Liu, Minlie Huang, Peng Zhang, Qinkai Zheng, Rui Lu, Shuaiqi Duan, Shudan Zhang, Shulin Cao, Shuxun Yang, Weng Lam Tam, Wenyi Zhao, Xiao Liu, Xiao Xia, Xiaohan Zhang, Xiaotao Gu, Xin Lv, Xinghan Liu, Xinyi Liu, Xinyue Yang, Xixuan Song, Xunkai Zhang, Yifan An, Yifan Xu, Yilin Niu, Yuantao Yang, Yueyan Li, Yushi Bai, Yuxiao Dong, Zehan Qi, Zhaoyu Wang, Zhen Yang, Zhengxiao Du, Zhenyu Hou, and Zihan Wang.
  Chatglm: A family of large language models from glm-130b to glm-4 all tools, 2024.
  URL <https://arxiv.org/abs/2406.12793>.
- [17]

  Michael Hassid, Tal Remez, Tu Anh Nguyen, Itai Gat, Alexis Conneau, Felix Kreuk, Jade Copet, Alexandre Défossez, Gabriel Synnaeve, Emmanuel Dupoux, Roy Schwartz, and Yossi Adi.
  Textually pretrained speech language models.
  In *Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023*, 2023.
- [18]

  Andrew Hines, Jan Skoglund, Anil Kokaram, and Naomi Harte.
  Visqol: an objective speech quality model.
  *EURASIP Journal on Audio, Speech, and Music Processing*, 2015 (13):1–18, 2015.
- [19]

  Wei-Ning Hsu, Benjamin Bolte, Yao-Hung Hubert Tsai, Kushal Lakhotia, Ruslan Salakhutdinov, and Abdelrahman Mohamed.
  Hubert: Self-supervised speech representation learning by masked prediction of hidden units.
  *IEEE ACM Trans. Audio Speech Lang. Process.*, 29:3451–3460, 2021.
- [20]

  Shengpeng Ji, Ziyue Jiang, Xize Cheng, Yifu Chen, Minghui Fang, Jialong Zuo, Qian Yang, Ruiqi Li, Ziang Zhang, Xiaoda Yang, Rongjie Huang, Yidi Jiang, Qian Chen, Siqi Zheng, Wen Wang, and Zhou Zhao.
  Wavtokenizer: an efficient acoustic discrete codec tokenizer for audio language modeling.
  *CoRR*, abs/2408.16532, 2024.
- [21]

  Mandar Joshi, Eunsol Choi, Daniel S. Weld, and Luke Zettlemoyer.
  Triviaqa: A large scale distantly supervised challenge dataset for reading comprehension.
  In *Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics, ACL 2017, Vancouver, Canada, July 30 - August 4, Volume 1: Long Papers*, pages 1601–1611. Association for Computational Linguistics, 2017.
- [22]

  Jungil Kong, Jaehyeon Kim, and Jaekyoung Bae.
  Hifi-gan: Generative adversarial networks for efficient and high fidelity speech synthesis.
  In H. Larochelle, M. Ranzato, R. Hadsell, M.F. Balcan, and H. Lin, editors, *Advances in Neural Information Processing Systems*, volume 33, pages 17022–17033. Curran Associates, Inc., 2020.
  URL <https://proceedings.neurips.cc/paper_files/paper/2020/file/c5d736809766d46260d816d8dbc9eb44-Paper.pdf>.
- [23]

  Rithesh Kumar, Prem Seetharaman, Alejandro Luebs, Ishaan Kumar, and Kundan Kumar.
  High-fidelity audio compression with improved RVQGAN.
  In *Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023*, 2023.
- [24]

  Kushal Lakhotia, Eugene Kharitonov, Wei-Ning Hsu, Yossi Adi, Adam Polyak, Benjamin Bolte, Tu-Anh Nguyen, Jade Copet, Alexei Baevski, Abdelrahman Mohamed, and Emmanuel Dupoux.
  On generative spoken language modeling from raw audio.
  *Transactions of the Association for Computational Linguistics*, 9:1336–1354, 2021.
- [25]

  Xuechen Li, Tianyi Zhang, Yann Dubois, Rohan Taori, Ishaan Gulrajani, Carlos Guestrin, Percy Liang, and Tatsunori B. Hashimoto.
  Alpacaeval: An automatic evaluator of instruction-following models.
  <https://github.com/tatsu-lab/alpaca_eval>, 5 2023.
- [26]

  Chen-Chou Lo, Szu-Wei Fu, Wen-Chin Huang, Xin Wang, Junichi Yamagishi, Yu Tsao, and Hsin-Min Wang.
  Mosnet: Deep learning-based objective assessment for voice conversion.
  In Gernot Kubin and Zdravko Kacic, editors, *20th Annual Conference of the International Speech Communication Association, Interspeech 2019, Graz, Austria, September 15-19, 2019*, pages 1541–1545. ISCA, 2019.
  doi: 10.21437/INTERSPEECH.2019.2003.
  URL <https://doi.org/10.21437/Interspeech.2019-2003>.
- [27]

  Ilya Loshchilov and Frank Hutter.
  Decoupled weight decay regularization, 2019.
  URL <https://arxiv.org/abs/1711.05101>.
- [28]

  Shivam Mehta, Ruibo Tu, Jonas Beskow, Éva Székely, and Gustav Eje Henter.
  Matcha-TTS: A fast TTS architecture with conditional flow matching.
  In *Proc. ICASSP*, 2024.
- [29]

  Nasrin Mostafazadeh, Nathanael Chambers, Xiaodong He, Devi Parikh, Dhruv Batra, Lucy Vanderwende, Pushmeet Kohli, and James F. Allen.
  A corpus and evaluation framework for deeper understanding of commonsense stories.
  *CoRR*, abs/1604.01696, 2016.
- [30]

  Eliya Nachmani, Alon Levkovitch, Roy Hirsch, Julian Salazar, Chulayuth Asawaroengchai, Soroosh Mariooryad, Ehud Rivlin, R. J. Skerry-Ryan, and Michelle Tadmor Ramanovich.
  Spoken question answering and speech continuation using spectrogram-powered LLM.
  In *The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024*. OpenReview.net, 2024.
- [31]

  Tu Anh Nguyen, Wei-Ning Hsu, Antony D’Avirro, Bowen Shi, Itai Gat, Maryam Fazel-Zarandi, Tal Remez, Jade Copet, Gabriel Synnaeve, Michael Hassid, Felix Kreuk, Yossi Adi, and Emmanuel Dupoux.
  Expresso: A benchmark and analysis of discrete expressive speech resynthesis.
  In Naomi Harte, Julie Carson-Berndsen, and Gareth Jones, editors, *24th Annual Conference of the International Speech Communication Association, Interspeech 2023, Dublin, Ireland, August 20-24, 2023*, pages 4823–4827. ISCA, 2023.
- [32]

  Tu Anh Nguyen, Benjamin Muller, Bokai Yu, Marta R. Costa-jussa, Maha Elbayad, Sravya Popuri, Paul-Ambroise Duquenne, Robin Algayres, Ruslan Mavlyutov, Itai Gat, Gabriel Synnaeve, Juan Pino, Benoit Sagot, and Emmanuel Dupoux.
  Spirit-lm: Interleaved spoken and written language model, 2024.
  URL <https://arxiv.org/abs/2402.05755>.
- [33]

  OpenAI.
  Hello gpt-4o, 2024.
  URL <https://openai.com/index/hello-gpt-4o/>.
- [34]

  Vassil Panayotov, Guoguo Chen, Daniel Povey, and Sanjeev Khudanpur.
  Librispeech: An asr corpus based on public domain audio books.
  In *2015 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, pages 5206–5210, 2015.
  doi: 10.1109/ICASSP.2015.7178964.
- [35]

  Vineel Pratap, Qiantong Xu, Anuroop Sriram, Gabriel Synnaeve, and Ronan Collobert.
  MLS: A large-scale multilingual dataset for speech research.
  In *21st Annual Conference of the International Speech Communication Association, Interspeech 2020, Virtual Event, Shanghai, China, October 25-29, 2020*, pages 2757–2761. ISCA, 2020.
- [36]

  Alec Radford, Jong Wook Kim, Tao Xu, Greg Brockman, Christine McLeavey, and Ilya Sutskever.
  Robust speech recognition via large-scale weak supervision.
  In Andreas Krause, Emma Brunskill, Kyunghyun Cho, Barbara Engelhardt, Sivan Sabato, and Jonathan Scarlett, editors, *International Conference on Machine Learning, ICML 2023, 23-29 July 2023, Honolulu, Hawaii, USA*, volume 202 of *Proceedings of Machine Learning Research*, pages 28492–28518. PMLR, 2023.
- [37]

  Takaaki Saeki, Detai Xin, Wataru Nakata, Tomoki Koriyama, Shinnosuke Takamichi, and Hiroshi Saruwatari.
  Utmos: Utokyo-sarulab system for voicemos challenge 2022.
  *Interspeech 2022*, 2022.
- [38]

  Xian Shi, Yexin Yang, Zerui Li, and Shiliang Zhang.
  Seaco-paraformer: A non-autoregressive asr system with flexible and effective hotword customization ability.
  *arXiv preprint arXiv:2308.03266 (accepted by ICASSP2024)*, 2023.
- [39]

  Aäron van den Oord, Sander Dieleman, Heiga Zen, Karen Simonyan, Oriol Vinyals, Alex Graves, Nal Kalchbrenner, Andrew W. Senior, and Koray Kavukcuoglu.
  Wavenet: A generative model for raw audio.
  In *The 9th ISCA Speech Synthesis Workshop, SSW 2016, Sunnyvale, CA, USA, September 13-15, 2016*, page 125. ISCA, 2016.
- [40]

  Aäron van den Oord, Oriol Vinyals, and Koray Kavukcuoglu.
  Neural discrete representation learning.
  In Isabelle Guyon, Ulrike von Luxburg, Samy Bengio, Hanna M. Wallach, Rob Fergus, S. V. N. Vishwanathan, and Roman Garnett, editors, *Advances in Neural Information Processing Systems 30: Annual Conference on Neural Information Processing Systems 2017, December 4-9, 2017, Long Beach, CA, USA*, pages 6306–6315, 2017.
- [41]

  Xiong Wang, Yangze Li, Chaoyou Fu, Lei Xie, Ke Li, Xing Sun, and Long Ma.
  Freeze-omni: A smart and low latency speech-to-speech dialogue model with frozen llm, 2024.
  URL <https://arxiv.org/abs/2411.00774>.
- [42]

  Zhifei Xie and Changqiao Wu.
  Mini-omni: Language models can hear, talk while thinking in streaming, 2024.
  URL <https://arxiv.org/abs/2408.16725>.
- [43]

  Zhuoyuan Yao, Di Wu, Xiong Wang, Binbin Zhang, Fan Yu, Chao Yang, Zhendong Peng, Xiaoyu Chen, Lei Xie, and Xin Lei.
  Wenet: Production oriented streaming and non-streaming end-to-end speech recognition toolkit.
  In *22nd Annual Conference of the International Speech Communication Association, Interspeech 2021, Brno, Czechia, August 30 - September 3, 2021*, pages 4054–4058. ISCA, 2021.
- [44]

  Neil Zeghidour, Alejandro Luebs, Ahmed Omran, Jan Skoglund, and Marco Tagliasacchi.
  Soundstream: An end-to-end neural audio codec.
  *IEEE ACM Trans. Audio Speech Lang. Process.*, 30:495–507, 2022.
  doi: 10.1109/TASLP.2021.3129994.
  URL <https://doi.org/10.1109/TASLP.2021.3129994>.
- [45]

  Aohan Zeng, Zhengxiao Du, Mingdao Liu, Lei Zhang, Shengmin Jiang, Yuxiao Dong, and Jie Tang.
  Scaling speech-text pre-training with synthetic interleaved data, 2024.
  URL <https://arxiv.org/abs/2411.17607>.
- [46]

  Dong Zhang, Shimin Li, Xin Zhang, Jun Zhan, Pengyu Wang, Yaqian Zhou, and Xipeng Qiu.
  Speechgpt: Empowering large language models with intrinsic cross-modal conversational abilities, 2023.
  URL <https://arxiv.org/abs/2305.11000>.
- [47]

  Susan Zhang, Stephen Roller, Naman Goyal, Mikel Artetxe, Moya Chen, Shuohui Chen, Christopher Dewan, Mona T. Diab, Xian Li, Xi Victoria Lin, Todor Mihaylov, Myle Ott, Sam Shleifer, Kurt Shuster, Daniel Simig, Punit Singh Koura, Anjali Sridhar, Tianlu Wang, and Luke Zettlemoyer.
  OPT: open pre-trained transformer language models.
  *CoRR*, abs/2205.01068, 2022.
- [48]

  Xin Zhang, Dong Zhang, Shimin Li, Yaqian Zhou, and Xipeng Qiu.
  Speechtokenizer: Unified speech tokenizer for speech language models.
  In *The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024*. OpenReview.net, 2024.
- [49]

  Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, and Ion Stoica.
  Judging llm-as-a-judge with mt-bench and chatbot arena, 2023.
  URL <https://arxiv.org/abs/2306.05685>.

## 附录 A

### A.1 语音对话机器人评测提示词

通用问答（General QA）

```
[Instruction]
Please act as an impartial judge and evaluate the quality of the response provided by an AI assistant to the user question displayed below. Your evaluation should consider factors such as the helpfulness, relevance, accuracy, depth, creativity, and level of detail of the response. Begin your evaluation by providing a short explanation. Be as objective as possible. After providing your explanation, you must rate the response on a scale of 1 to 10 by strictly following this format: "[[rating]]", for example: "Rating: [[5]]".

[Question]
{instruction}

[The Start of Assistant's Answer]
{response}
[The End of Assistant's Answer]
```

知识（Knowledge）

```
Your will be given a question, the reference answers to that question, and an answer to be judged. Your tasks is to judge whether the answer to be judged is correct, given the question and reference answers. An answer considered correct expresses or contains the same meaning as at least **one of** the reference answers. The format and the tone of the response does not matter.

You should respond in JSON format. First provide a one-sentence concise analysis for the judgement in field 'analysis', then your judgment in field 'judgment'. For example,
'''json
{{"analysis": <a one-sentence concise analysis for the judgement>, "judgment": <your final judgment, "correct" or "incorrect">}}
'''

# Question
{instruction}

# Reference Answer
{targets}

# Answer To Be Judged
{answer_to_be_judged}
```
