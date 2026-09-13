---
title: "一个面向长程记忆的新模型与数据集"
title_en: "A new model and dataset for long-range memory"
source: https://deepmind.google/blog/a-new-model-and-dataset-for-long-range-memory/
site: deepmind
date: 2020-02-10
crawled: 2026-09-13
translated: 2026-09-13
---

# 一个面向长程记忆的新模型与数据集

> 原文：[A new model and dataset for long-range memory](https://deepmind.google/blog/a-new-model-and-dataset-for-long-range-memory/) · Google DeepMind

本博文介绍一个新的长程记忆模型——[Compressive Transformer](https://arxiv.org/abs/1911.05507)，以及一个面向书籍级语言建模的新基准 [PG19](https://github.com/deepmind/pg19)。我们将结合记忆模型与语言建模的最新进展，提供理解这项新研究所需的概念性工具。

在一生中，我们建立起能在多种时间尺度上保持的记忆——从几分钟到几个月、几年乃至几十年。读一本书时，我们能想起许多章之前登场的人物，或同一系列更早一本书中的人物，并推理他们在当前情境下的动机和可能的行动。我们甚至可以在忙碌的一周里把书放下，之后接着上次的地方读下去而不忘剧情。

我们并不是通过把一生中接收到的关于世界的感官输入的每个细节都存储下来才做到这些的。[我们的大脑会根据相关性、意外程度、感知到的危险和重复性等因素](https://www.ncbi.nlm.nih.gov/pubmed/28641107)对输入刺激进行选择、过滤和整合。换言之，我们把一生的经历压缩成一组突出的记忆，帮助我们理解过去、更好地预期未来。AI 研究人员的一个主要目标，就是找到在计算系统中实现这类能力的方法，以及那些需要在长时间跨度上进行复杂推理的基准。

人工神经网络的记忆系统在过去二十年中取得了长足进步。在这篇博文中，我们回顾过往进展，探讨为什么这是一个如此困难的任务，并思考自然语言建模如何能提供一种设计更好长程记忆系统的有效手段。我们反思了更好的压缩式记忆架构和稀疏记忆访问机制的必要性，以朝着把终身推理纳入我们计算系统的目标迈进。

## 深度学习中记忆的简史

> 没有哪种记忆或保持能力是基于持久印象的。我们所谓的记忆，不过是对重复刺激的反应性增强。

Nikola Tesla

当今最早、也最广泛使用的记忆架构之一，是一种称为[长短期记忆网络](https://www.bioinf.jku.at/publications/older/2604.pdf)（LSTM）的循环神经网络（RNN）。LSTM 以一个数字向量的形式维护一份紧凑的记忆，并通过带门控的读取、写入和遗忘操作来访问和修改它。它最初是在一组涉及学习比特流上的逻辑运算的合成任务上开发的。然而，此后它成为序列数据上无处不在的模型：从识别手写笔记到预测肾损伤的早期发作。

LSTM 以及许多同期 RNN 的一个弱点是容量。它们的设计使每单位记忆都能以可学习的权重影响记忆中的所有其他单位。但这导致系统计算效率低下：模型中可学习参数的数量随记忆大小呈二次增长。例如，一个记忆大小为 64KB 的 LSTM 会产生 8GB 的参数。绕过这一记忆容量瓶颈一直是活跃的研究领域。

![一张示意图，展示一个智能体随时间与外部记忆系统交互：先把观察到的钥匙写入记忆，之后再读取记忆以打开一个宝箱。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62274c1dcce30901e65d1115_Fig201.svg)

图 1. 长程推理对通用智能至关重要。图中，一个智能体在很长一段时间里记住了钥匙的存在与位置，并在发现宝箱时回想起这一信息——促使它返回记忆中的地点取回钥匙。

DeepMind 的研究人员提出了一种新颖架构——[可微分神经计算机](https://deepmind.com/blog/article/differentiable-neural-computers)（DNC），它用一个规模大得多的记忆矩阵来增强 LSTM，以弥补这些不足。DNC 使用注意力操作从这个记忆矩阵中读取。在视觉注意力中，我们的目光会被视觉场景中相关的物体吸引——例如，在一次情绪激动的对话中，人们通常会用更多时间观察朋友的面孔，而不太会注意他们的鞋。类似地，记忆模型可以关注过去特定的事件/数据。这种注意力操作所需的参数数量是固定的、与记忆大小无关，因此模型的记忆容量可以显著增加。

与 DNC 同期，带有额外注意力机制的循环神经网络在[翻译](https://arxiv.org/abs/1409.0473)和[问答](https://arxiv.org/abs/1410.3916)领域展现出前景。这些模型能够使用两种记忆结构随时间进行推理：一个小而紧凑的 LSTM 记忆和一个大的外部记忆。然而，最近 Google Brain 团队的研究人员提出了 Transformer，它移除了 LSTM，只使用注意力来[跨时间传递信息](https://arxiv.org/abs/1706.03762)。

![「the agreement on the European Economic Area was signed in August 1992」这句话在上方被翻译成法语，图中线条把英文中的每个词与其法语对应词连接起来。](https://lh3.googleusercontent.com/4-K4RqcoDw0FRzBhqYgUMhUkaAcJ8nLJ-H4QHp3tjxPQaNQ1HRwQDbuOylvPjjzOxJC3__ME35ccTz3pzWj8LGT-ZYl-eJKoIdJlvKL5HNoePUUVgkU=w1440)

图 2. 神经网络在英译法翻译中的注意力可视化。来源：Attention and Augmented Recurrent Neural Networks, Olah & Carter, 2016

Transformer 最初被证明在机器翻译任务上显著优于循环神经网络。此后它被应用于自然语言处理的众多应用，包括问答、文档摘要、情感分类和自然语言建模——后者在过去一年里出现了尤为令人兴奋的进展。

## 为自然语言建模

找到既能推动更好记忆架构的发展、又能让我们向通用人工智能更进一步推进的机器学习任务是具有挑战性的。统计语言建模是这样一项我们相信对两个目的都有价值的任务。语言模型的工作方式是顺序预测文本流中的下一个词。它们既可以用于为既有文本建模，也可以生成新文本。随着它们对过去建模得越来越好，预测变得更准确，生成的文本也变得更逼真。

在克劳德·香农 1948 年发表的开创性论文「[A Mathematical Theory of Communication](https://onlinelibrary.wiley.com/doi/10.1002/j.1538-7305.1948.tb01338.x)」——该文创立了信息论领域——中，他讨论了原始的语言模型，并展示了增加上下文如何提升生成文本的质量与真实感。他通过引入最简单的英语文本模型来做到这一点，这种模型完全没有上下文建模——一个把每个字符独立对待的字符级模型。按相对频率采样字符（'a' 占 8%，'b' 占 1.5%，等等），我们得到一串无意义的字符串：

**XFOML RXKHRJFFJUJ ZLPWCFWKCYJ FFJEYVKCQSGHYD QPAAMKBZAACIBZLHJQD.**

然而，他指出，如果改为对单词的概率独立建模，样本质量会得到改进。此时建模的上下文大约扩大了 7 倍（一个单词的平均字符数）：

**REPRESENTING AND SPEEDILY IS AN GOOD APT OR COME CAN DIFFERENT NATURAL HERE HE THE A IN CAME THE TO OF TO EXPERT GRAY COME TO FURNISHES THE LINE MESSAGE HAD BE THESE.**

通过对词对的概率建模——上下文长度再扩大 2 倍——生成的文本甚至更加真实：

**THE HEAD AND IN FRONTAL ATTACK ON AN ENGLISH WRITER THAT THE CHARACTER OF THIS POINT IS THEREFORE ANOTHER METHOD FOR THE LETTERS THAT THE TIME OF WHO EVER TOLD THE PROBLEM FOR AN UNEXPECTED**

换言之，上下文长度的增加会带来生成文本质量的提升。香农对自己生成的样本质量有所评论，并猜想自然文本样本可能出自一个足够复杂的统计模型：「attack on an English writer that the character of this 这个由十个词组成的特定序列完全不显得不合理。这样看来，一个足够复杂的随机过程将能对离散信源给出令人满意的表示」。

对语言建模作为长程推理任务的一种批评是：模型可以从局部上下文中捕捉其预测的很大一部分。神经语言模型传统上忽略更宽的上下文，主要聚焦于短期。例如，2017 年 [Dailuk 等人](https://arxiv.org/abs/1702.04521)发现他们的神经语言模型很少关注前五个词之外的内容。然而在过去一年里，大型 Transformer 模型已被证明能够利用数百个词的上下文来生成愈发真实、连贯范围更长的文本。来自 [OpenAI 的 GPT-2](https://openai.com/blog/better-language-models/)（一个 1.5B 参数的 Transformer）的演示表明，该模型能够生成真实的文本，并在多个段落之间保留关键实体（例如 Dr Jorge Pérez 和独角兽）：

**The scientist named the population, after their distinctive horn, Ovid's Unicorn. These four-horned, silver-white unicorns were previously unknown to science.**

**Now, after almost two centuries, the mystery of what sparked this odd phenomenon is finally solved.**

**Dr. Jorge Pérez, an evolutionary biologist from the University of La Paz, and several companions, were exploring the Andes Mountains when they found a small valley, with no other animals or humans. Pérez noticed that the valley had what appeared to be a natural fountain, surrounded by two peaks of rock and silver snow.**

**Pérez and the others then ventured further into the valley. "By the time we reached the top of one peak, the water looked blue, with some crystals on top," said Pérez.**

**Pérez and his friends were astonished to see the unicorn herd. These creatures could be seen from the air without having to move too much to see them – they were so close they could touch their horns.**

**While examining these bizarre creatures the scientists discovered that the creatures also spoke some fairly regular English. Pérez stated, "We can see, for example, that they have a common 'language,' something like a dialect or dialectic."**

**Dr. Pérez believes that the unicorns may have originated in Argentina, where the animals were believed to be descendants of a lost race of people who lived there before the arrival of humans in those parts of South America.**

**While their origins are still unclear, some believe that perhaps the creatures were created when a human and a unicorn met each other in a time before human civilization. According to Pérez, "In South America, such incidents seem to be quite common."**

**However, Pérez also pointed out that it is likely that the only way of knowing for sure if unicorns are indeed the descendants of a lost alien race is through DNA. "But they seem to be able to communicate in English quite well, which I believe is a sign of evolution, or at least a change in social organization," said the scientist.**

## 知识迁移

距离香农早期的语言模型实验已过去 70 年，这样的样本很可能会让他大为惊叹。然而，强大的神经语言模型真正的好处——以及它们与 AGI 目标的相关性——在于它们把知识迁移到一系列任务上的能力。在学习如何为文本建模的过程中，神经语言模型似乎构建了一个关联的知识库，以及大量技能。

例如，OpenAI 的研究人员展示出 GPT-2 可以被应用于问答、复述或情感分析等自然语言处理任务，并取得了出奇好的表现——尤其是考虑到这是一个从未被显式训练执行此类任务的模型。当大型 Transformer 语言模型针对问答等特定任务进行微调时，所得性能显著优于那些专为问答设计与训练的模型。Google 著名的自然语言模型 [BERT](https://arxiv.org/abs/1810.04805) 在一系列 NLP 基准上取得最先进的性能，如今已是 [Google 搜索的一部分](https://www.blog.google/products/search/search-language-understanding-bert/)。而更近一些，有工作表明 GPT-2 可以通过在[对局着法序列](https://slatestarcodex.com/2020/01/06/a-very-unlikely-chess-game/)上训练来学会下初级国际象棋。

## 为语言模型设置基准

一个流行的长程语言模型基准是 [WikiText-103](https://www.salesforce.com/products/einstein/ai-research/the-wikitext-dependency-language-modeling-dataset/)，它由英语维基百科文章组成，由 [Salesforce AI](https://arxiv.org/abs/1609.07843) 的研究人员开发。文章平均约 3,600 词，在数据集创建之时，这已远超最先进模型的记忆窗口。

不过，Google 的研究人员最近展示了一个名为 TransformerXL 的 Transformer 变体——它维护着过去网络激活的记忆，并在 WikiText-103 上最近取得了最先进的结果——能够利用跨越[一千多个词](https://arxiv.org/abs/1901.02860)的上下文。这引出了一个问题：模型很快会让这些基准饱和吗？因此，我们整理并发布了一个新的、更长程的、基于书籍的语言模型基准。

## 一个面向长期记忆研究的新数据集

为了支持对长程序列模型日益增长的兴趣，我们正在发布一个新的语言建模基准 [**PG-19**](https://github.com/deepmind/pg19)，它取材于 [Project Gutenberg 在线图书馆](https://www.gutenberg.org/)中的书籍。

书籍为长程记忆模型的开发提供了丰富的上下文。我们从 Project Gutenberg 中选择了约 28,000 本 1919 年之前出版的书籍。与以往语言建模数据集发布不同，我们对文本只做了极少的预处理。例如，我们不限制数据的词表大小，也不对数字做屏蔽处理，以避免把有用信息过滤掉。

PG-19 的规模是以往语言建模基准（如 [Billion Word Benchmark](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/41880.pdf)）的两倍以上，其文本的上下文长度是以往长程语言模型基准 WikiText-103 的 10 倍以上。我们在下面提供了一张现有语言建模基准的对比表：

![一张语言建模基准的对比表，包括 1B Word、Penn Treebank、WikiText-103 和 PG-19，突出显示 PG-19 明显更大的平均上下文长度（69K 词）和开放词表规模。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62274ca26f79eae3412a2cbf_Fig203.svg)

## Compressive Transformer

除了新基准之外，我们还提出了一个称为 [Compressive Transformer](https://arxiv.org/abs/1911.05507) 的长程记忆模型。我们从睡眠在[巩固情景记忆](https://www.ncbi.nlm.nih.gov/pubmed/28641107)形成中所扮演的角色中获得灵感。众所周知，睡眠对记忆至关重要；人们认为睡眠的作用是压缩并巩固记忆，从而提高记忆任务的推理能力。在 Compressive Transformer 中，类似情景记忆的细粒度记忆会在模型遍历输入序列时在线收集；随着时间推移，它们最终会被压缩。

Compressive Transformer 像 Transformer 一样使用注意力从过去中选择信息。它以与最近提出的 [TransformerXL](https://arxiv.org/abs/1901.02860) 相同的方式维护一份过去激活的短期记忆。区别在于：TransformerXL 在激活变旧时将其丢弃，而 Compressive Transformer 则把它们压缩进一份压缩记忆。压缩由一个神经网络执行，该网络由一个辅助损失引导，促使其保留与任务相关的信息。它可以学会过滤掉无关记忆，以及组合记忆，使突出的信息得以在更长时间内被保留和检索。

![一张示意图，展示 Compressive Transformer 的记忆结构：时间轴上有三段，「序列」和「记忆」由橙色圆点表示，「压缩记忆」由青色圆点表示，覆盖一段密集得多的时间轴。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62274cba2b4e7e19932faaf2_Fig204.gif)

图 3. Compressive Transformer：一个长程序列注意力序列模型，它用一份细粒度的短期记忆和一份粗粒度的压缩记忆来刻画过去。

我们发现，在不使用额外训练数据来源的[已发表结果](http://nlpprogress.com/english/language_modeling.html)之列的条件下，Compressive Transformer 在两个广泛使用的长程基准 **WikiText-103** 和 **Enwik8** 的自然语言建模上拥有最先进的性能。我们还展示了它可以有效用于语音建模，对生僻词的处理尤为出色，并且可以在强化学习智能体中用于解决记忆任务。

![一张对比表，展示各词频区间的语言模型困惑度，证明 Compressive Transformer 优于 LSTM 和 TransformerXL 模型，且在预测生僻词（频率 < 1K）时提升百分比最大。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62274cd01da7d8a1f9b80635_Fig204.svg)

我们发现，Compressive Transformer 在对来自 PG-19 基准的长上下文书籍文本建模时产生了最大的性能增益。该模型的条件采样可用于撰写类似书籍的文段。下面我们展示一个示例：我们向模型提供一段文本作为上下文（取自 Ralph Connor 的《The Patrol of the Sun Dance》，模型此前从未见过该书）。

**来自 Ralph Connor《The Patrol of the Sun Dance Trail》的上下文**

**Along the tote-road, which ran parallel to the steel, a man, dark of skin, slight but wiry, came running, his hard panting, his streaming face, his open mouth proclaiming his exhaustion. At a little trail that led to the left he paused, noted its course toward the flaunting flag, turned into it, then struggled up the rocky hillside till he came to the wooden shack, with a deep porch running round it, and surrounded by a rustic fence which enclosed a garden whose neatness illustrated a characteristic of the British soldier. The runner passed in through the gate and up the little gravel walk and began to ascend the steps...**

**Compressive Transformer 的续写**

**...As though by mutual consent, all the three members of the Superintendent Force were standing on the veranda watching his progress, a man came strolling slowly down the path, stopping often to gaze curiously about him, then stopping once more when he saw the four standing on the veranda. His face was dark, his eyes prominent, and the lines that furrowed his forehead showed marks of many woes, yet his step was alert and he began to mount the steps with steady strides.**

**The man's attention was diverted by the unexpected appearance of the two policemen; a third man came slipping up, grumbling under his breath, and stopped long enough to look doubtfully around him, then slipped away again. In the meantime, the four on the veranda continued to watch the approach of the new arrival. In spite of himself, the Superintendent Force became conscious of a curious feeling–uneasiness that was almost fear–in the presence of that strange man. He would not allow himself to admit the fact, yet he felt it in his bones. But to the watchers, the plain, everyday features of that stranger and his coming, seemed only just what the Seven White Shee owed him–their weight, their hurry, their blast...**

Compressive Transformer 能够以多种风格生成叙事，从多角色对话、第一人称日记到第三人称散文。虽然该模型并没有扎根于真实世界的语言理解，也不理解真实世界中发生的事件——但通过捕捉更长程的相关性，我们看到文本连贯性的提升。

## 记忆架构的未来

当我们努力创造能够运行数天、数周甚至数年的智能体时，在每个时间步对所有原始输入数据进行计算将是不切实际的。即使计算能力持续增长，我们也需要开发压缩且稀疏的记忆架构来构建表示并对行动进行推理。

能够跨越数天、数月甚至数年经验捕捉相关关联的模型已近在眼前。我们相信，随时间进行更强推理的路径，将来自对过去更好的选择性注意，以及更有效的压缩机制。随着我们探索这一领域的想法，我们需要跨越越来越长时间间隔的任务和数据集。PG-19 数据集可以帮助研究人员朝这个方向前进：它以人类通常消费的最长文本形式呈现数据——完整篇幅的书籍。我们希望它的发布能够激发对新模型的兴趣——那些压缩过去、以预测未来并在当下有效行动的模型。

延伸阅读

[Compressive Transformer 论文](https://arxiv.org/abs/1911.05507)

[PG-19 基准](https://github.com/deepmind/pg19)
