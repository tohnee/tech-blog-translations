---
title: "大语言模型阅读清单"
title_en: "Large Language Models Reading List"
source: https://sebastianraschka.com/blog/2023/llm-reading-list.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 大语言模型阅读清单

> 原文：[Large Language Models Reading List](https://sebastianraschka.com/blog/2023/llm-reading-list.html)

大语言模型已经席卷了公众的注意力——这里并不是在玩谐音梗。
在短短五年间，大语言模型——Transformer——几乎彻底改变了自然语言处理领域。此外，它们也已开始革新计算机视觉和计算生物学等领域。

由于 Transformer 对每个人的研究议程都有如此大的影响，我想为刚入门的机器学习研究人员和从业者整理一份简短的阅读清单（[我昨天那条评论](https://www.linkedin.com/feed/update/urn:li:activity:7028449312300834816?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7028449312300834816%2C7028519126105030656%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287028519126105030656%2Curn%3Ali%3Aactivity%3A7028449312300834816%29)的扩展版）。

下面的清单基本上应按时间顺序阅读，我完全聚焦于学术研究论文。当然，还有许多其他有用的资源。例如：

- Jay Alammar 的 [Illustrated Transformer](http://jalammar.github.io/illustrated-transformer/)；
- Lilian Weng 的一篇[更偏技术性的博客文章](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/)；
- Xavier Amatriain 整理的[迄今为止所有主要 Transformer 的目录与家族树](https://amatriain.net/blog/transformer-models-an-introduction-and-catalog-2d1e9039f376/)；
- Andrej Karpathy 面向教学的生成式语言模型[极简代码实现](https://github.com/karpathy/nanoGPT)；
- 还有在下本人的一个[系列讲座](https://sebastianraschka.com/blog/2021/dl-course.html#l19-self-attention-and-transformer-networks)和[书章](https://github.com/rasbt/machine-learning-book/tree/main/ch16)。

附言：这份原始清单的扩展版（包含更多论文）可以在这里找到：<https://magazine.sebastianraschka.com/p/understanding-large-language-models>。

## 理解主要架构与任务

如果你是 Transformer / 大语言模型的新手，从头开始是最合理的。

**(1)** *Neural Machine Translation by Jointly Learning to Align and Translate*（2014），Bahdanau、Cho 和 Bengio，<https://arxiv.org/abs/1409.0473>

如果你有几分钟空闲，我建议从上面这篇论文开始。它为循环神经网络（RNN）引入了注意力机制，以提升长程序列建模能力。这让 RNN 能够更准确地翻译更长的句子——这也正是后来开发原始 Transformer 架构背后的动机。

![Llm reading list attention rnn](https://sebastianraschka.com/images/blog/2023/llm-reading-list/attention-rnn.webp)

来源：<https://arxiv.org/abs/1409.0473>

---

**(2)** *Attention Is All You Need*（2017），Vaswani、Shazeer、Parmar、Uszkoreit、Jones、Gomez、Kaiser 和 Polosukhin，<https://arxiv.org/abs/1706.03762>

上面这篇论文介绍了原始 Transformer 架构，它由编码器和解码器两部分组成，这两部分在后来会作为独立模块变得重要。此外，这篇论文引入了缩放点积注意力机制、多头注意力块和位置输入编码等概念，它们至今仍是现代 Transformer 的基础。

![Llm reading list transformer](https://sebastianraschka.com/images/blog/2023/llm-reading-list/transformer.webp)

来源：<https://arxiv.org/abs/1706.03762>

---

**(3)** *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*（2018），Devlin、Chang、Lee 和 Toutanova，<https://arxiv.org/abs/1810.04805>

在原始 Transformer 架构之后，大语言模型研究开始分化为两个方向：面向文本分类等预测建模任务的编码器式 Transformer，以及面向翻译、摘要和其他文本创作等生成式建模任务的解码器式 Transformer。

上面这篇 BERT 论文引入了掩码语言建模的原始概念，其下一句预测仍然是一个有影响力的编码器式架构的一部分。如果你对这一研究分支感兴趣，我建议接着阅读 [RoBERTa](https://arxiv.org/abs/1907.11692)，它通过移除下一句预测任务简化了[预训练](https://sebastianraschka.com/glossary/#pretraining "Pretraining")目标。

![Llm reading list bert](https://sebastianraschka.com/images/blog/2023/llm-reading-list/bert.webp)

来源：<https://arxiv.org/abs/1810.04805>

---

**(4)** *Improving Language Understanding by Generative Pre-Training*（2018），Radford 和 Narasimhan，<https://www.semanticscholar.org/paper/Improving-Language-Understanding-by-Generative-Radford-Narasimhan/cd18800a0fe0b668a1cc19f2ec95b5003d0a5035>

最初的 GPT 论文介绍了流行的解码器式架构，以及通过下一词预测进行的预训练。由于掩码语言模型预训练目标的缘故，BERT 可以被视为双向 Transformer，而 GPT 是单向的自回归模型。虽然 GPT 嵌入也可以用于分类，但 GPT 路线是当今最具影响力的 LLM（例如 ChatGPT）的核心。

如果你对这一研究分支感兴趣，我建议接着阅读 [GPT-2](https://www.semanticscholar.org/paper/Language-Models-are-Unsupervised-Multitask-Learners-Radford-Wu/9405cc0d6169988371b2755e573cc28650d14dfe) 和 [GPT-3](https://arxiv.org/abs/2005.14165) 论文。这两篇论文说明 LLM 具备零样本和[少样本学习](https://sebastianraschka.com/glossary/#few-shot-prompting "Few-Shot Prompting")能力，并凸显了 LLM 的涌现能力。GPT-3 也仍然是训练当前一代 LLM（如 ChatGPT）时常用的基线和基础模型——我们稍后会作为一个独立条目介绍通向 ChatGPT 的 InstructGPT 方法。

![Llm reading list gpt](https://sebastianraschka.com/images/blog/2023/llm-reading-list/gpt.webp)

来源：<https://www.semanticscholar.org/paper/Improving-Language-Understanding-by-Generative-Radford-Narasimhan/cd18800a0fe0b668a1cc19f2ec95b5003d0a5035>

---

**(5)** *BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension*（2019），Lewis、Liu、Goyal、Ghazvininejad、Mohamed、Levy、Stoyanov 和 Zettlemoyer，<https://arxiv.org/abs/1910.13461>。

如前所述，BERT 型的编码器式 LLM 通常更适合预测建模任务，而 GPT 型的解码器式 LLM 更擅长生成文本。为了集两家之所长，上面这篇 BART 论文把编码器和解码器两部分结合了起来（与本清单第二篇论文中的原始 Transformer 颇为相似）。

![Llm reading list bart](https://sebastianraschka.com/images/blog/2023/llm-reading-list/bart.webp)

来源：<https://arxiv.org/abs/1910.13461>

## 缩放定律与效率提升

如果你想进一步了解提升 Transformer 效率的各种技术，我推荐先阅读 [2020 年的 *Efficient Transformers: A Survey*](https://arxiv.org/abs/2009.06732)，再读 [2023 年的 *A Survey on Efficient Training of Transformers*](https://arxiv.org/abs/2302.01107)。

此外，以下是我发现特别有趣、值得阅读的论文。

**(6)** *[FlashAttention](https://sebastianraschka.com/glossary/#flashattention "FlashAttention"): Fast and Memory-Efficient Exact Attention with IO-Awareness*（2022），Dao、Fu、Ermon、Rudra 和 Ré，<https://arxiv.org/abs/2205.14135>。

虽然大多数 Transformer 论文都懒得替换原始的缩放点积机制来实现[自注意力](https://sebastianraschka.com/glossary/#mha "Multi-Head Attention (MHA)")，但 FlashAttention 是我最近最常看到被引用的机制之一。

![Llm reading list flash attention](https://sebastianraschka.com/images/blog/2023/llm-reading-list/flash-attention.webp)

来源：<https://arxiv.org/abs/2205.14135>

---

**(7)** *Cramming: Training a Language Model on a Single GPU in One Day*（2022），Geiping 和 Goldstein，<https://arxiv.org/abs/2212.14034>。

在这篇论文中，研究人员在单块 GPU 上训练了一个掩码语言模型 / 编码器式 LLM（此处为 BERT）24 小时。作为对比，2018 年最初的 BERT 论文在 16 块 TPU 上训练了四天。
一个有趣的洞见是：虽然更小的模型具有更高的吞吐量，但小模型的学习效率也更低。因此，较大的模型反而不需要更多训练时间就能达到特定的预测性能门槛。

![Llm reading list cramming](https://sebastianraschka.com/images/blog/2023/llm-reading-list/cramming.webp)

来源：<https://arxiv.org/abs/2212.14034>

---

**(8)** *Scaling Down to Scale Up: A Guide to Parameter-Efficient Fine-Tuning*（2022），Lialin、Deshpande 和 Rumshisky，<https://arxiv.org/abs/2303.15647>。

在大型数据集上预训练的现代大语言模型展现出涌现能力，并在包括语言翻译、摘要、编程和问答在内的各种任务上表现出色。然而，如果我们想提升 Transformer 在领域特定数据和专门任务上的能力，对 Transformer 进行微调是值得的。这篇综述回顾了 40 多篇关于[参数高效微调](https://sebastianraschka.com/glossary/#lora "LoRA (Low-Rank Adaptation)")方法的论文（包括前缀调优、适配器和低秩适配等流行技术），让微调在计算上（非常）高效。

![Llm reading list peft](https://sebastianraschka.com/images/blog/2023/llm-reading-list/peft.webp)

来源：<https://arxiv.org/abs/1910.13461>

---

**(9)** *Training Compute-Optimal Large Language Models*（2022），Hoffmann、Borgeaud、Mensch、Buchatskaya、Cai、Rutherford、de Las Casas、Hendricks、Welbl、Clark、Hennigan、Noland、Millican、van den Driessche、Damoc、Guy、Osindero、Simonyan、Elsen、Rae、Vinyals 和 Sifre，<https://arxiv.org/abs/2203.15556>。

这篇论文介绍了 700 亿参数的 Chinchilla 模型，它在生成式建模任务上优于广受欢迎的 1750 亿参数 GPT-3 模型。不过，它的主要亮点在于指出当代大语言模型都"训练得明显不足"。

这篇论文定义了大语言模型训练的线性缩放定律（scaling law）。例如，虽然 Chinchilla 只有 GPT-3 的一半大小，它却胜过了 GPT-3，因为它是在 1.4 万亿（而不是仅仅 3000 亿）个 token 上训练的。换句话说，训练 token 的数量与模型规模同等重要。

![Llm reading list chinchilla](https://sebastianraschka.com/images/blog/2023/llm-reading-list/chinchilla.webp)

来源：<https://arxiv.org/abs/2203.15556>

## 对齐——引导大语言模型迈向预期目标与利益

近年来，我们已经见到许多相对有能力、能够生成逼真文本的大语言模型（例如 GPT-3 和 Chinchilla 等）。看起来，在常用预训练范式所能达到的成就上，我们已经触及了天花板。

为了让语言模型更有帮助、减少错误信息和有害语言，研究人员设计了额外的训练范式来微调预训练的基础模型。

**(10)** *Training Language Models to Follow Instructions with Human Feedback*（2022），Ouyang、Wu、Jiang、Almeida、Wainwright、Mishkin、Zhang、Agarwal、Slama、Ray、Schulman、Hilton、Kelton、Miller、Simens、Askell、Welinder、Christiano、Leike 和 Lowe，<https://arxiv.org/abs/2203.02155>。

在这篇所谓的 InstructGPT 论文中，研究人员使用了人在回路的强化学习机制（RLHF）。他们从一个预训练的 GPT-3 基础模型开始，先使用监督学习在人类生成的提示-响应配对上进一步微调（步骤 1）。接着，他们请人类对模型输出进行排序，以训练一个[奖励模型](https://sebastianraschka.com/glossary/#rlhf "RLHF (Reinforcement Learning from Human Feedback)")（步骤 2）。最后，他们使用奖励模型，通过近端策略优化进行强化学习来更新预训练并微调过的 GPT-3 模型（步骤 3）。

顺便一提，这篇论文也因描述了 ChatGPT 背后的想法而闻名——根据近期的传闻，ChatGPT 是 InstructGPT 的放大版本，在更大的数据集上做过微调。

![Llm reading list instruct gpt](https://sebastianraschka.com/images/blog/2023/llm-reading-list/instruct-gpt.webp)

来源：<https://arxiv.org/abs/2203.02155>

---

**(11)** *Constitutional AI: Harmlessness from AI Feedback*（2022），Yuntao、Saurav、Sandipan、Amanda、Jackson、Jones、Chen、Anna、Mirhoseini、McKinnon、Chen、Olsson、Olah、Hernandez、Drain、Ganguli、Li、Tran-Johnson、Perez、Kerr、Mueller、Ladish、Landau、Ndousse、Lukosuite、Lovitt、Sellitto、Elhage、Schiefer、Mercado、DasSarma、Lasenby、Larson、Ringer、Johnston、Kravec、El Showk、Fort、Lanham、Telleen-Lawton、Conerly、Henighan、Hume、Bowman、Hatfield-Dodds、Mann、Amodei、Joseph、McCandlish、Brown 和 Kaplan，<https://arxiv.org/abs/2212.08073>。

在这篇论文中，研究人员把对齐的想法又向前推进了一步，提出了一种用于创建"无害"AI 系统的训练机制。研究人员没有采用直接的人类监督，而是提出了一种基于规则清单（由人类提供）的自训练机制。与上面提到的 InstructGPT 论文类似，该方法使用了强化学习路线。

![Llm reading list constitutional ai](https://sebastianraschka.com/images/blog/2023/llm-reading-list/constitutional-ai.webp)

来源：<https://arxiv.org/abs/2212.08073>

## 附赠：基于人类反馈的强化学习（RLHF）入门

虽然 RLHF（基于人类反馈的强化学习）可能无法完全解决当前 LLM 的所有问题，但它目前被认为是可用的最佳选项，尤其是与上一代 LLM 相比。我们很可能会看到把 RLHF 创造性地应用到 LLM 之外更多领域的做法。

上面两篇论文（InstructGPT 和 Constitutional AI）都利用了 RLHF，由于它在不久的将来会是一种有影响力的方法，本节提供了额外的资源供你想深入了解 RLHF 时参考。（严格来说，Constitutional AI 论文使用的是 AI 反馈而非人类反馈，但它遵循使用强化学习的类似概念。）

**(12)** *Asynchronous Methods for Deep Reinforcement Learning*（2016），Mnih、Badia、Mirza、Graves、Lillicrap、Harley、Silver 和 Kavukcuoglu（<https://arxiv.org/abs/1602.01783>）介绍了策略梯度方法，作为基于深度学习的强化学习中 Q-learning 的替代方案。

**(13)** *Proximal Policy Optimization Algorithms*（2017），Schulman、Wolski、Dhariwal、Radford 和 Klimov（<https://arxiv.org/abs/1707.06347>）提出了一种改进的基于近端策略的强化学习流程，比上面的原始策略优化算法更具数据效率且更可扩展。

**(14)** *Fine-Tuning Language Models from Human Preferences*（2020），Ziegler、Stiennon、Wu、Brown、Radford、Amodei、Christiano 和 Irving（<https://arxiv.org/abs/1909.08593>）展示了把 PPO 和奖励学习的概念应用于预训练语言模型的做法，包括使用 KL 正则化来防止策略偏离自然语言过远。

**(15)** *Learning to Summarize from Human Feedback*（2022），Stiennon、Ouyang、Wu、Ziegler、Lowe、Voss、Radford、Amodei 和 Christiano（<https://arxiv.org/abs/2009.01325>）介绍了流行的 RLHF 三步流程：

1. 预训练 GPT-3；
2. 以监督方式对它进行微调；
3. 同样以监督方式训练一个奖励模型。随后用近端策略优化，基于这个奖励模型训练微调后的模型。

这篇论文还表明，使用近端策略优化的强化学习能得到比单纯使用常规监督学习更好的模型。

![Llm reading list rlhf 1](https://sebastianraschka.com/images/blog/2023/llm-reading-list/rlhf-1.webp)

来源：<https://arxiv.org/abs/2009.01325>

**(16)** *Training Language Models to Follow Instructions with Human Feedback*（2022），Ouyang、Wu、Jiang、Almeida、Wainwright、Mishkin、Zhang、Agarwal、Slama、Ray、Schulman、Hilton、Kelton、Miller、Simens、Askell、Welinder、Christiano、Leike 和 Lowe（<https://arxiv.org/abs/2203.02155>，也称为 *InstructGPT 论文*）使用了与上面类似的 RLHF 三步流程，但不是摘要文本，而是聚焦于根据人类指令生成文本。此外，它使用标注员把输出从最好到最差进行排序（而不只是在人类生成文本与 AI 生成文本之间做二元比较）。

## 结论与延伸阅读

我尽力让上面的清单保持精炼，聚焦于理解当代大语言模型的设计、约束与演进的十佳论文（外加 3 篇关于 RLHF 的附赠论文）。

关于延伸阅读，我建议顺着上述论文中的参考文献继续挖掘。或者，给你一些额外的指引，这里还有一些其他资源：

**GPT 的开源替代品**

- *BLOOM: A 176B-Parameter Open-Access Multilingual Language Model*（2022），<https://arxiv.org/abs/2211.05100>
- *OPT: Open Pre-trained Transformer Language Models*（2022），<https://arxiv.org/abs/2205.01068>

**ChatGPT 替代品**

- *LaMDA: Language Models for Dialog Applications*（2022），<https://arxiv.org/abs/2201.08239>
- (Sparrow) *Improving Alignment of Dialogue Agents via Targeted Human Judgements*（2022），<https://arxiv.org/abs/2209.14375>
- *BlenderBot 3: A Deployed Conversational Agent that Continually Learns to Responsibly Rngage*，<https://arxiv.org/abs/2208.03188>

**计算生物学中的大语言模型**

- *ProtTrans: Towards Cracking the Language of Life's Code Through Self-Supervised Deep Learning and High Performance Computing*（2021），<https://arxiv.org/abs/2007.06225>
- *Highly Accurate Protein Structure Prediction with AlphaFold*（2021），<https://www.nature.com/articles/s41586-021-03819-2>
- *Large Language Models Generate Functional Protein Sequences Across Diverse Families*（2023），<https://www.nature.com/articles/s41587-022-01618-2>
