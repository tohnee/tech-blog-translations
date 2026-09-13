---
title: "Gemma Scope：帮助安全社区看清语言模型的内部运作"
title_en: "Gemma Scope: helping the safety community shed light on the inner workings of language models"
source: https://deepmind.google/blog/gemma-scope-helping-the-safety-community-shed-light-on-the-inner-workings-of-language-models/
site: deepmind
date: 2024-07-31
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemma Scope：帮助安全社区看清语言模型的内部运作

> 原文：[Gemma Scope: helping the safety community shed light on the inner workings of language models](https://deepmind.google/blog/gemma-scope-helping-the-safety-community-shed-light-on-the-inner-workings-of-language-models/) · Google DeepMind

宣布推出一套全面开放的稀疏自编码器套件，用于语言模型可解释性研究。

要创建一个人工智能（AI）语言模型，研究者需要构建一个从海量数据中学习、无需人类指导的系统。因此，语言模型的内部运作往往是一个谜，就连训练它们的研究者也不例外。机制可解释性（mechanistic interpretability）是一个专注于破解这些内部运作的研究领域。这一领域的研究者把稀疏自编码器当作一种"显微镜"，让他们得以观察语言模型的内部，更好地理解其工作原理。

今天，[我们宣布推出 Gemma Scope](https://developers.googleblog.com/en/smaller-safer-more-transparent-advancing-responsible-ai-with-gemma/)，这是一套新工具，帮助研究者理解 Gemma 2——我们的轻量级开放模型家族——的内部运作。Gemma Scope 是一个包含数百个免费开放的稀疏自编码器（SAE）的合集，覆盖 [Gemma 2 9B](https://huggingface.co/google/gemma-2-9b) 和 [Gemma 2 2B](https://huggingface.co/google/gemma-2-2b)。我们还在开源 [Mishax](https://github.com/google-deepmind/mishax)，这是我们构建的一个工具，它支撑了 Gemma Scope 背后的大部分可解释性工作。

我们希望今天的发布能推动更有雄心的可解释性研究。进一步的研究有潜力帮助这一领域构建更稳健的系统，针对模型幻觉开发更好的防护措施，并防范自主 AI 智能体带来的欺骗或操纵等风险。

[试用我们的 Gemma Scope 交互式演示](https://www.neuronpedia.org/gemma-scope)，由 Neuronpedia 提供。

## 解读语言模型内部发生了什么

当你向语言模型提问时，它会把你的文本输入转换为一系列"激活"（activations）。这些激活映射出你所输入词语之间的关系，帮助模型在不同词语之间建立联系，进而用它来写出回答。

在模型处理文本输入的过程中，模型神经网络中不同层的激活表示着多个越来越高级的概念，这些概念被称为"特征"（features）。

例如，模型的早期层可能学会[回忆事实](https://arxiv.org/abs/2202.05262)，比如 [Michael Jordan 打篮球](https://www.alignmentforum.org/posts/iGuwZTHWb6DFY3sKB/fact-finding-attempting-to-reverse-engineer-factual-recall)，而后面的层则可能识别更复杂的概念，比如[文本的事实性](https://arxiv.org/abs/2310.06824)。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

一张风格化的示意图，展示使用稀疏自编码器解读模型在回忆"光之城是巴黎"这一事实时的激活过程。我们可以看到与法语相关的概念出现了，而无关的概念没有出现。

然而，可解释性研究者面临一个关键问题：模型的激活是许多不同特征的混合体。在机制可解释性的早期，研究者曾希望神经网络激活中的特征能与单个神经元——即信息节点——一一对应。但不幸的是，在实践中，神经元会因许多不相关的特征而被激活。这意味着没有明显的办法判断哪些特征是激活的一部分。

**这正是稀疏自编码器大显身手的地方。**

一个给定的激活只会是少数特征的混合，尽管语言模型可能能够检测数百万甚至数十亿种特征——也就是说，模型稀疏地使用特征。例如，语言模型在回答关于爱因斯坦的提问时会考虑相对论，在写关于煎蛋卷的内容时会考虑鸡蛋，但在写煎蛋卷时大概不会考虑相对论。

稀疏自编码器利用这一事实来发现一组可能的特征，并把每个激活分解为其中少数几个。研究者希望，稀疏自编码器完成这一任务的最佳方式，就是找出语言模型实际使用的底层特征。

重要的是，在这一过程中，我们研究者自始至终都没有告诉稀疏自编码器要寻找哪些特征。因此，我们能够发现我们没有预料到的丰富结构。不过，由于我们无法立即知道所发现特征的含义，我们会在稀疏自编码器标记某特征"激活"（fire）的文本样例中寻找[有意义的模式](https://transformer-circuits.pub/2023/monosemantic-features/index.html)。

下面是一个示例，特征激活的 token 按强度以深浅不同的蓝色高亮显示：

![一幅标题为"The Idiom Feature"（习语特征）的示意图，展示稀疏自编码器如何在不同句子中检测与习语相关的特征。各个 token 按激活强度以深浅不同的蓝色高亮，包括"hot cakes"中的"hot"、"rich like Croesus"中的"Croesus"、"knock their socks off"中的"socks"，以及"hit the nail on the head"中的"nail"。](https://lh3.googleusercontent.com/SgZETU9GmYp3bu_qHnh-aySzh5ItRdvkrWdsPlwqjutxKlW0VbQrStFsH_WO2MlrVpnD4iZ__Kj7w1agoFO20NiIHh-IGZh_TZLjmIkjbjCt9pkffQ=w1440)

我们的稀疏自编码器发现的某个特征的激活示例。每个气泡是一个 token（词或词片段），深浅不一的蓝色显示该特征出现的强度。在这个例子中，该特征显然与习语相关。

## Gemma Scope 的独特之处

以往使用稀疏自编码器的研究主要聚焦于[微型模型](https://arxiv.org/abs/2403.19647)或[较大模型中的单个层](https://transformer-circuits.pub/2024/scaling-monosemanticity/index.html)的内部运作。但更有雄心的可解释性研究涉及解码较大模型中分层、复杂的算法。

我们在 [Gemma 2 2B](https://huggingface.co/google/gemma-2-2bb) 和 [9B](https://huggingface.co/google/gemma-2-9b) 的每一层和每个子层的输出上都训练了稀疏自编码器，构建出 Gemma Scope，共产生了 400 多个稀疏自编码器、总计超过 3,000 万个学到的特征（尽管许多特征可能相互重叠）。这一工具将使研究者能够研究特征如何在整个模型中演化，如何相互作用和组合形成更复杂的特征。

Gemma Scope 还采用了我们新的、最先进的 [JumpReLU SAE 架构](https://arxiv.org/abs/2407.14435)进行训练。最初的稀疏自编码器架构难以平衡双重目标：检测哪些特征存在，以及估计它们的强度。JumpReLU 架构让这一平衡更容易恰当地达成，显著降低了误差。

训练如此多的稀疏自编码器是一项重大的工程挑战，需要大量算力。我们使用了约等于 Gemma 2 9B 训练算力 15% 的计算量（不包括生成蒸馏标签的算力），把约 20 PiB（Pebibytes）的激活保存到磁盘（大约相当于[一百万份英文维基百科](https://dumps.wikimedia.org/enwiki/20240720/)），总共产生了数千亿个稀疏自编码器参数。

## 推动领域向前

通过发布 Gemma Scope，我们希望把 Gemma 2 打造为开放机制可解释性研究的最佳模型家族，并加速社区在这一领域的工作。

到目前为止，可解释性社区已经在使用稀疏自编码器理解小模型、以及开发相关技术方面取得了巨大进展，例如[因果干预](https://arxiv.org/abs/2004.12265)（[interventions](https://proceedings.neurips.cc/paper_files/paper/2021/file/4f5c422f4d49a5a807eda27434231040-Paper.pdf)）、[自动电路分析](https://arxiv.org/abs/2304.14997)（[automatic circuit analysis](https://arxiv.org/abs/2403.19647)，[见此](https://arxiv.org/abs/2403.00745)）、[特征解释](https://openaipublic.blob.core.windows.net/neuron-explainer/paper/index.html)，以及[评估](https://arxiv.org/abs/2406.04093)[稀疏自编码器](https://transformer-circuits.pub/2023/monosemantic-features/index.html)。有了 Gemma Scope，我们希望看到社区将这些技术扩展到现代模型，分析思维链等更复杂的能力，并找到可解释性的现实世界应用，例如解决只有较大模型才会出现的幻觉和越狱等问题。

[阅读 Gemma Scope 技术报告](https://storage.googleapis.com/gemma-scope/gemma-scope-report.pdf)[查看由 Neuronpedia 提供的交互式演示](https://www.neuronpedia.org/gemma-scope)[试用我们的 Gemma Scope 编程教程](https://colab.research.google.com/drive/17dQFYUYnuKnP6OwQPH9v_GSYUW5aj-Rp?usp=sharing)[下载 Gemma Scope](https://huggingface.co/google/gemma-scope)[查看 Mishax](https://github.com/google-deepmind/mishax)

**致谢**

Gemma Scope 是 Tom Lieberum、Sen Rajamanoharan、Arthur Conmy、Lewis Smith、Nic Sonnerat、Vikrant Varma、Janos Kramar 和 Neel Nanda 的集体成果，由 Rohin Shah 和 Anca Dragan 担任顾问。我们特别感谢 Neuronpedia 的 Johnny Lin、Joseph Bloom 和 Curt Tigges 为交互式演示提供的协助。我们感谢 Phoebe Kirk、Andrew Forbes、Arielle Bier、Aliya Ahmad、Yotam Doron、Tris Warkentin、Ludovic Peran、Kat Black、Anand Rao、Meg Risdal、Samuel Albanie、Dave Orr、Matt Miller、Alex Turner、Tobi Ijitoye、Shruti Sheth、Jeremy Sie、Tobi Ijitoye、Alex Tomala、Javier Ferrando、Oscar Obeso、Kathleen Kenealy、Joe Fernandez、Omar Sanseviero 和 Glenn Cameron 的帮助与贡献。
