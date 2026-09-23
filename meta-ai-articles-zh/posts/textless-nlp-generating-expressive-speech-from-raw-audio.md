---
title: "无文本 NLP：从原始音频生成富有表现力的语音"
title_en: "Textless NLP: Generating expressive speech from raw audio"
date: 2021-09-09
source: https://ai.facebook.com/blog/textless-nlp-generating-expressive-speech-from-raw-audio
crawled: 2026-09-22
translated: 2026-09-22
---

# 无文本 NLP：从原始音频生成富有表现力的语音

> 原文：[Textless NLP: Generating expressive speech from raw audio](https://ai.facebook.com/blog/textless-nlp-generating-expressive-speech-from-raw-audio) · Meta AI（Wayback 存档）

2021 年 9 月 9 日

BERT、RoBERTa 和 GPT-3 等基于文本的语言模型近年来取得了巨大进步。给定书面文字输入，它们几乎能就任何主题生成极其逼真的文本。此外，它们还提供了有用的预训练模型，只需少量标签或示例即可微调用于各种困难的自然语言处理（NLP）应用，包括情感分析、翻译、信息检索、推理和摘要（例如 BART 和 XLM-R）。但存在一个重要局限：这些应用主要局限于拥有适合训练 AI 模型的超大规模文本数据集的语言。

我们正在介绍生成式口语语言模型（Generative Spoken Language Model，GSLM）——首个摆脱对文本依赖的高性能 NLP 模型。GSLM 利用表示学习方面的最新突破，直接仅从原始音频信号工作，无需任何标签或文本。它为地球上可能每一种口语（包括那些没有大规模文本数据集的语言）开启无文本 NLP 应用新时代打开了大门。GSLM 还让开发能够涵盖口语全部表现力的 NLP 模型成为可能。以往，要把 NLP 应用连接到语音输入，研究者必须先训练一个自动语音识别（ASR）系统——这项资源密集的操作会引入错误、难以编码随意的语言交互，而且只有少数语言可用。借助无文本 NLP，我们希望让 ASR 成为过去，以端到端的方式从语音输入直达语音输出。我们认为，学龄前儿童仅凭原始感官输入和语音交互就能学习语言的能力，为这项研究可能带来的未来进步提供了一个激动人心的模板。

我们现在分享基线 GSLM 模型，它包含三个组件：一个把语音转换为表示口语中频繁复现声音的离散单元的编码器；一个自回归的、基于单元的语言模型，训练其根据已见内容预测下一个离散单元；以及一个把单元转换回语音的解码器。

## 无文本 NLP 的广泛益处

NLP 领域几乎总是用书面文本来训练模型。这对英语等拥有适合训练的海量文本数据集的语言效果很好。但世界上大多数语言缺乏这样的大规模数据集，这意味着它们基本无法受益于 NLP 技术。颠覆这一格局是一个激动人心的挑战，需要一个由信号处理、语音处理、NLP 和心理语言学专家组成的 Facebook AI 多学科研究团队的共同努力。

我们的研究以无文本输入训练语言模型，开辟了新天地。这在根本上有几方面重要性。第一，无文本 NLP 技术应能让 AI 更具包容性，建模比今天更丰富的语言多样性——这种方式为训练任何口语的模型打开了可能。第二，由于能获取口语的全部表现力，模型应能纳入细微差别和语调，编码讽刺、愤怒和不确定，并使用笑声、哈欠和咂嘴等发声。由于口语的丰富表现力，即使在英语这类文本丰富的语言中，无文本 NLP 实际上可能比用文本训练模型效果更好。第三，研究者应能直接在「音频优先」的内容上训练模型，如播客、电台节目和语音社交应用，无需标注、也无需训练 ASR。无文本 NLP 开启了一系列此前从未设想过的应用，例如多人在线电子游戏的表情化实时翻译，或从音频档案中进行内容检索与摘要。最后，这些模型可以帮助发展心理学家以及言语与语言临床医生，预测婴儿学习说话和理解言语的能力如何受不同语言可用语言输入差异的影响。

除了推动这些更广泛的研究目标，GSLM 还为当今 NLP 从业者提供了切实的好处。研究者将能用简单的「下一个声音单元预测」任务预训练模型，并微调用于端到端任务而完全不需要文本。例如，我们的工作实现了首个纯音频的语音到语音翻译系统。后续工作将处理标准 NLP 任务的无文本版本，如情感分析、文档检索、摘要等。

## 构建并评估基线模型

GSLM 的第一步是构建基线模型并在两个简单的端到端任务上评估。第一个是离散再合成（discrete resynthesis）：把输入波形编码为一系列离散单元（我们称之为伪文本，pseudo-text），再用模型的「声音」重新合成输入。第二个任务是语音生成：用语言模型采样新的伪文本，可以是无条件的，也可以通过编码器以输入提示为条件。

模型架构：编码器把语音波形转换为离散单元（S2u），解码器做相反的映射（u2S），基于单元的语言模型建模单元序列（伪文本）的分布。

我们测试了三种最先进的编码器：CPC、wav2vec 2.0 和 HuBERT，之后接 k 均值聚类与去重（移除连续相同的单元）。语言建模采用标准因果 Transformer，解码器采用 Tacotron 2（标准文本转语音系统）。编码器和基于单元的语言模型（uLM）在 6000 小时的 Libri-Light 和 Librispeech（大型有声书合集）上训练，解码器在 Librispeech 和 LJspeech 上训练。整个技术栈都从原始音频自监督训练，不使用文本或标签；语言模型和文本转语音组件在由原始音频得到的伪文本上训练。

在比较这些不同模型时，我们无法直接分析生成的伪文本，因为这些单元与字母或音素并非一一对应。好的模型通常使用 100 个或更多单元，它们通常编码比音素更短的语音片段。因此我们用预训练 ASR 把生成的音频转回文本。这样我们就能用音素错误率（PER）——比较原始输入的音素与 ASR 重新转录的音素——来度量再合成音频的可懂度，并用曲线下面积（AUC）指标度量条件或无条件生成音频的语言质量和多样性。AUC 通过在一系列「temperature」下采样句子得到，我们把 temperature 定义为语言模型的创造程度：temperature 越低，模型越刻板；temperature 越高，模型越多变。

在执行这些测量的过程中，我们有若干发现。第一，量化器使用多少离散单元很重要：数量更多在声学层面带来更好的结果，但代价是更高的比特率。第二，在语言层面也有类似趋势，但在某些情况下，使用过多单元反而有害。第三，不同编码器产生的结果差异很大，HuBERT 提供了最佳整体结果。第四，自动生成指标与人类评价高度相关。第五，这些指标可以通过 Zero Resource Speech 基准中计算更快的零样本指标来预测，后者可作为快速迭代的有效代理。

以下是我们最佳模型（在 100 个单元上的 CPC 或 HuBERT，训练于 Libri-Light 6k）的一些无条件生成样本（转录由 ASR 完成）。更多样本见此处。低 temperature 下，句子是重复性的：

**生成（temperature: 0.3）**
THE PROPERTY BY JAMES RESELL RED FOR LIBERATA OR BY JASON DOWNY THE PROPERTY BY JASON DOWNY THE PROPERTY THE PROPERTY THE PROPERTY THE PROPERTY

中等 temperature 下，句子变得局部连贯（几个词之内）且更多样：

**生成（temperature: 1.0）**
BUT IT IS ATTENDANT FROM THE PEOPLE TO DEFEND HIMSELF FROM THIS INFORMATION PRIDE OF THE POTENTIAL IN CRIMINAL ACTIVITY A CURIOSITY AND IMPETUOSITY OF THE WORLD A WAR SOON ACQUIRED

高 temperature 下，句子相当多样但变得不连贯，有些段落并非真实词语：

**生成（temperature: 1.5）**
ATION OF PURE BLUE HE SAID AT ONCE A LICKING STREAMY AT HER WARM SPOT OF HALF PERFORMED NOTE WAS A RAGING OATH LET IT AS BIR OF AMOLE IN MOOD STROLLING ER CRASS

这是一个以提示「This reality begins to explain the dark pow[..]」（出自 P.F Walter 译介的儒勒·凡尔纳《海底两万里》导言）为条件、使用中等 temperature（HuBERT 100）生成的续写示例。模型能补全不完整的词（pow[..] → POWER），并用与整体氛围一致的词继续（dark → BLACKNESS），也有自我重复的倾向（MAGICAL）：

**提示**：THIS REALITY BEGINS TO EXPLAIN THE DARK POW[..]
**续写**：ER OF THE MAGICAL BLACKNESS AND IN THE MIDST OF IT IS MAGICAL AS A SINGLE BLACKNESS OF THE PAIN

## 编码与解码韵律

虽然我们的编码器发现的单元不是音素，但它们具有许多相同属性：它们编码语音对比（如区分「pa」和「ba」），同时忽略说话人和信道信息。此外，与音素一样，它们往往忽略一些虽然富有表现力但更全局的语音属性，如语调和节奏——这被称为韵律（prosody）。因此，第二步我们通过改进编码器和解码器来捕捉韵律。为此，我们训练了一个利用向量量化的变分自编码器来获得独特的潜在表示。这个所谓的 VQ-VAE 系统的输入包括：音高（F0）信息，连同上文所述离散（未去重）伪音素单元的简化文本转语音系统、来自 VQ-VAE 的量化音高，以及一个学习到的说话人嵌入。

我们在 LJspeech（单说话人）和 VCTK（多说话人）上评估了这一架构，再次发现基于 HuBERT 的单元在客观指标和主观评分上都提供了非常好的结果。我们从三个维度——内容、F0 和说话人——用自动技术评估再合成结果，并用人类评估者做整体评估（平均意见分，MOS）。由于语音单元和韵律单元实现了高度的说话人无关性，我们的模型能够在保留原始输入的语音单元和韵律的同时，通过更改输出说话人嵌入来实现声音转换（voice transfer）。它还可以用作语音编解码器，只传输一个声音嵌入以及单元与韵律的离散码。与当前语音编解码器相比，我们的系统在低得多的比特率下表现相当。具体来说，与压缩质量相近的标准编解码器 Opus 相比压缩倍率约为 20 倍，与使用向量量化变分自编码器的最新研究语音编解码器相比约为 2 倍。不过，虽然我们的系统实现了高压缩率，它专用于语音，无法编码音乐等其他形式的音频。声音转换与语音编解码用例的示例见此处。

## 联合建模内容与韵律

最后一步是把富有表现力的韵律纳入语言模型，联合建模语音的内容层面和韵律层面。我们引入了多流因果 Transformer，其输入和输出层有多个头，我们选择建模的每个语音通道各对应一个。这里我们使用了三个通道：伪音素单元、时长和量化音高。

与基线模型一样，这个韵律 GSLM（prosodic-GSLM）从有声书的原始波形训练。增加这些额外的通道和任务，在单元的困惑度分数上提升了语言模型性能。我们还展示了该系统现在可以为同一提示生成多种逼真的韵律「补全」（inpainting）——我们固定语音内容，只采样时长和音高。这个训练好的模型还能够与提示的表达风格相一致地联合生成新内容和新韵律。以下是以提示「When an aristocracy carries on public affairs, its [..]」（出自 Alexis de Tocqueville 政治论文《论美国的民主》一个相当正式的朗读版本）生成的续写，以及以提示「She was quite shocked when I asked her whether wine was allowed [..]」（出自简·奥斯汀小说《曼斯菲尔德庄园》一个富有表现力的朗读版本）生成的续写。更多示例见：https://speechbot.github.io/pgslm

## 下一步走向哪里

随着研究的继续，我们的下一个目标是把 GSLM 应用于随意、自发语音和对话的数据集——这正是基于文本的方法和 ASR 最吃力的地方。此外，我们希望证明 GSLM 可以成为预训练下游任务的有效方法，这些任务只有少量可用标注数据，如口语摘要、口语情感分析和信息检索任务。我们的目标是发挥口语相对于书面语在表现力和意义微妙性上的巨大优势。同时，我们想让世界上任何语言都能训练模型成为可能，从而为理解人类思想打开几乎无限的潜在数据宝库。我们希望随着进展分享这项工作的更新。

本博文讨论的工作反映了以下人员的贡献（按字母顺序排列）：Yossi Adi、Jade Copet、Emmanuel Dupoux、Wei Ning Hsu、Evgeny Kharitonov、Kushal Lakhotia、Ann Lee、Abdelrahman Mohamed、Tu Anh Nguyen、Adam Polyak 和 Morgane Rivière。

获取第一步 GSLM 论文 | 获取第二步表情化再合成论文 | 获取第三步韵律感知 GSLM 论文 | 获取代码与预训练模型
