---
title: "无监督学习：好奇心旺盛的学生"
title_en: "Unsupervised learning: The curious pupil"
source: https://deepmind.google/blog/unsupervised-learning-the-curious-pupil/
site: deepmind
date: 2019-06-25
crawled: 2026-09-13
translated: 2026-09-13
---

# 无监督学习：好奇心旺盛的学生

> 原文：[Unsupervised learning: The curious pupil](https://deepmind.google/blog/unsupervised-learning-the-curious-pupil/) · Google DeepMind

*本系列文章解释我们研究所依托的理论基础。*

过去十年间，机器学习在图像识别、自动驾驶汽车以及围棋等复杂游戏等截然不同的领域取得了前所未有的进展。这些成功主要通过用两种学习范式之一——监督学习和强化学习——来训练深度神经网络而实现。这两种范式都需要由人类设计训练信号并传递给计算机：在监督学习中，这些信号是「目标」（例如图像的正确标签）；在强化学习中，它们是成功行为的「奖励」（例如在 Atari 游戏中拿到高分）。因此，学习的边界是由人类训练者界定的。

一些科学家认为，一个足够包罗万象的训练方案——例如完成种类极其繁多的任务的能力——就足以催生通用智能；另一些人则相信，真正的智能将需要更独立的学习策略。想想幼儿是如何学习的：她的祖母可能会坐在旁边，耐心地为她指出鸭子的例子（充当监督学习中起教导作用的信号），或者在她拼好木块拼图时以掌声奖励她（如同强化学习）。但幼儿绝大部分时间是在天真地探索世界，通过好奇心、玩耍和观察来理解周围的环境。无监督学习是这样一种范式：它奖励智能体（即计算机程序）去学习它们所观察到的数据，而不预设某个特定任务，以此塑造自主的智能。换句话说，智能体是为学习而学习。

无监督学习的一个关键动机在于：传给学习算法的数据在内部结构上极其丰富（例如图像、视频和文本），而用于训练的目标与奖励通常非常稀疏（例如「狗」这一标签——它指代那个形态千变万化的物种；或用一个单独的 1 或 0 来表示游戏中成功与否）。这表明，算法学到的东西必然大部分在于理解数据本身，而不是把这种理解应用于特定任务。

## 解码视觉的要素

2012 年是深度学习的里程碑之年，AlexNet（以其首席设计者 Alex Krizhnevsky 命名）横扫了[ImageNet 图像分类竞赛](http://image-net.org/challenges/LSVRC/2012/index)。AlexNet 的图像识别能力前所未有，但更令人惊叹的是它幕后发生的事情。当研究者分析 AlexNet 的所作所为时，他们发现它是通过构建越来越复杂的[输入内部表示](https://distill.pub/2017/feature-visualization/)来解读图像的：纹理和边缘等低层特征在底部各层中被表示出来，随后被组合起来，在更高的层中形成轮子和狗等高层概念。

这与我们大脑处理信息的方式惊人地相似：初级感觉加工区域中的简单边缘和纹理，在更高级的区域中被组装成人脸等复杂物体。因此，复杂场景的表示可以由视觉基元构建而成，就像句子的意义从组成它的单个词语中涌现出来一样。AlexNet 的各层在没有任何显式指引的情况下，发现了视觉的一套基本「词汇」，以解决其任务。在某种意义上，它学会了玩维特根斯坦所说的[「语言游戏」](https://en.wikipedia.org/wiki/Language_game_(philosophy))——在像素与标签之间进行迭代式的翻译。

![网格图，展示不同神经网络层的特征可视化：从第 1 层的简单纹理开始，逐步构建到第 4d 层的复杂物体，如「狗鼻子」「灵长类动物」和「房屋」。](https://lh3.googleusercontent.com/JkWJM2K7CX8h5dVR-tugoGTYt7d48mF37G3g8IAZ6PqDQugyurQozN10W3xFPmNYWteuvJsHTvT_jlRKTYwj1d_XhoWLJ-8IGeBLhvnEK90Jp1BpWg8=w1440)

卷积神经网络的视觉词汇。对网络的每一层，生成能够最大限度激活特定神经元的图像。这些神经元对其他图像的响应，随后可以被解读为视觉「词语」（纹理、书架、狗鼻子、鸟）的有或无。出自《特征可视化》（Feature Visualization），Olah 等人（2017）。

## 迁移学习

从通用智能的视角看，AlexNet 词汇最有趣的地方在于，它可以被复用，即迁移到它受训任务之外的视觉任务上，例如识别[整个场景而非单个物体](https://arxiv.org/abs/1310.1531)。在一个不断变化的世界中，迁移至关重要，而人类在这方面出类拔萃：我们能够快速调整从经验中获得的技能与理解（即我们的「世界模型」），以应对眼前的任何情境。例如，一位受过古典音乐训练的钢琴家可以相对轻松地学会爵士钢琴。按这一思路推理，形成正确的世界内部表示的人工智能体，应当也能做到类似的事情。

尽管如此，像 AlexNet 这样的分类器所学到的表示仍有局限。特别是，由于网络只被训练为给图像标注单一的类别（猫、狗、汽车、火山），任何推断标签所不需要的信息——无论它对其他任务可能多么有用——都很容易被忽略。例如，如果标签总是指向前景，表示中就可能捕捉不到图像的背景。一种可能的解决方案是提供更全面的训练信号，比如[描述图像的详细说明文字](https://www.cv-foundation.org/openaccess/content_cvpr_2015/papers/Vinyals_Show_and_Tell_2015_CVPR_paper.pdf)：不只是「狗」，而是「一只柯基在阳光明媚的公园里接飞盘」。然而，这类目标标签提供起来十分费力，尤其在大规模场景下，而且仍可能不足以捕捉完成任务所需的全部信息。无监督学习的基本前提是：学习丰富且可广泛迁移的表示的最佳方式，是尝试学习关于数据的所有可学之物。

如果通过表示学习实现迁移这一概念显得过于抽象，不妨想想一个学会了用火柴人画人的小孩。她发现了人体形态的一种表示方式，既高度紧凑，又能快速调整。通过为每个火柴人补充细节，她可以画出全班同学：最好的朋友戴上的眼镜，同桌身上他最爱的红色 T 恤。她发展出这项技能，并不是为了完成某个特定任务或获得奖励，而是出于她反映周围世界的基本冲动。

## 通过创造来学习：生成模型

无监督学习也许最简单的目标，就是训练算法生成属于自己的数据样本。所谓的生成模型不应只是复现其受训数据（那是一种乏味的死记硬背），而应构建出数据所来自的底层类别本身的模型：不是某一张特定的马的或彩虹的照片，而是所有马的与彩虹的照片的集合；不是某位说话者的某一次发声，而是口语发声的总体分布。生成模型的指导原则是：能够构造出一个令人信服的数据样本，是理解该数据的最有力证据。正如理查德·费曼（Richard Feynman）所言：「凡我不能创造，我就不能理解。」

就图像而言，迄今最成功的生成模型是[生成对抗网络](https://en.wikipedia.org/wiki/Generative_adversarial_network)（Generative Adversarial Network，简称 GAN）。其中两个网络——生成器与判别器——进行着一场鉴别力的大比拼，宛如艺术伪造者与侦探之间的较量。生成器制造图像，目标是骗过判别器、使其信以为真；而判别器则因识别出赝品而获得奖励。最初杂乱随机的生成图像经过多次迭代被不断精炼，两个网络之间持续的博弈造就了越来越逼真的图像，在许多情况下已[与真实照片无法区分](https://medium.com/syncedreview/gan-2-0-nvidias-hyperrealistic-face-generator-e3439d33ebaf)。生成对抗网络还能根据[用户勾画的粗糙草图](https://blogs.nvidia.com/blog/2019/03/18/gaugan-photorealistic-landscapes-nvidia-research/)「脑补」出风景的细节。

只需看一眼下面的图像，我们就足以相信：该网络已经学会了表示其受训照片的许多关键特征，例如动物身体的结构、草地的纹理，以及光影的精细效果（即便是透过肥皂泡折射的光影）。仔细观察则会发现一些细微的异常，比如那只白狗似乎多出的一条腿，以及喷泉中某一股水流诡异呈直角的水流。生成模型的创造者们力求避免这类瑕疵，但它们的可见性恰恰凸显了重建图像这类熟悉数据的一个好处：通过检视样本，研究者可以推断模型学到了什么、又没学到什么。

![由 AI 生成的八张图像组成的网格，展示不同主体，包括白狼、红蘑菇、肥皂泡、饮料、意大利面、喷泉、小狗和火箭发射。](https://lh3.googleusercontent.com/Y0ghE_oxKdcqYvrnWlbg3VKFGmVidK-gm2r3ALh9g5Qa_B9SgIdfcukUvfPkIii_6yPyNrGqF_aub-sRdpH5Ncem_soaDnppBXVZEjVAAqtpa0mJPA=w1440)

BigGAN 构想出的场景与生物（Brock、Donahue 与 Simonyan，2018）。

## 通过预测来创造

无监督学习中另一个值得注意的家族是自回归模型：数据被切分成一串小片段，每个片段依次被预测。这类模型可以通过连续猜测接下来会出现什么来生成数据——把一个猜测作为输入，再猜下一个。语言模型是其中最广为人知的例子，它根据前面的词语预测每个词；某些邮件与即时通讯应用中弹出的文字预测功能正由这类模型驱动。语言建模的最新进展已能生成非常逼真的段落，例如下面这段出自 [OpenAI 的 GPT-2](https://openai.com/blog/better-language-models/) 的文字。

![GPT-2 生成文本的示例：开头是人类撰写的系统提示，讲安第斯山脉会讲英语的独角兽，随后是机器续写的「奥维德的独角兽」以及一位演化生物学家发现独角兽群的经过。](https://lh3.googleusercontent.com/Z0eioWhn8_2B_oteipogO3aKlWwi5wESbdB7B1xJYMeBT9XYH4TQ3lwce1_LVBUc6bubCYJ4p6pucv64vnEZzlA0nxGxpIksbwRnm6Xpxi2lCDb83Q=w1440)

文中一个有趣的破绽是，独角兽被描述为「四角」的：同样地，探究网络理解能力的局限令人着迷。

通过控制用于为输出预测设定条件的输入序列，自回归模型还可用于把一个序列变换为另一个序列。这个[演示](http://www.cs.toronto.edu/~graves/handwriting.html)使用条件自回归模型把文本转换成逼真的手写体。[WaveNet](https://deepmind.com/blog/article/wavenet-generative-model-raw-audio) 将文本转换成自然流畅的语音，如今已被用于[为 Google 助手生成声音](https://deepmind.com/blog/article/wavenet-launches-google-assistant)。类似的「条件设定 + 自回归生成」流程也可用于[从一种语言翻译成另一种语言](https://ai.googleblog.com/2017/08/transformer-novel-neural-network.html)。

自回归模型通过按特定顺序预测数据的每一部分来学习数据。而预测「数据的任意部分」可以由「其他任意部分」得出，由此可以构建出一类更一般的无监督学习算法。例如，这可以是从句子中去掉一个词，然后[尝试用剩余的部分预测它](https://ai.googleblog.com/2018/11/open-sourcing-bert-state-of-art-pre.html)。通过学习做出大量局部预测，系统被迫去学习数据作为整体的知识。

围绕生成模型的一个担忧是它们被滥用的可能性。虽然利用照片、视频和音频编辑来操纵证据早已可行，但生成模型可能让出于恶意目的编辑媒体变得更加容易。我们已经见过所谓的「深度伪造」（deepfake）的演示——例如这段[伪造奥巴马总统视频的片段](https://www.bbc.co.uk/news/av/technology-40598465/fake-obama-created-using-ai-tool-to-make-phoney-speeches)。令人欣慰的是，应对这些挑战的多项重要工作已经在进行之中，包括使用统计技术帮助[检测](https://arxiv.org/pdf/1807.04919.pdf)[合成媒体](https://arxiv.org/abs/1803.09179)并验证真实媒体、[提高公众意识](https://blog.witness.org/2018/07/deepfakes/)，以及围绕限制已训练生成模型的可得性展开的讨论。此外，生成模型本身也可用于检测合成媒体与异常数据——例如[检测伪造语音](https://www.blog.google/outreach-initiatives/google-news-initiative/advancing-research-fake-audio-detection/)，或识别支付异常以保护客户免受欺诈。研究者需要对生成模型开展研究，以便更好地理解它们并缓解下游风险。

## 重新想象智能

生成模型本身就引人入胜，但 DeepMind 对它们的主要兴趣，在于把它们视为通往通用智能的一块垫脚石。赋予智能体生成数据的能力，就是赋予它想象力，从而赋予它[对未来的规划与推理能力](https://deepmind.com/blog/article/agents-imagine-and-plan)。即便没有显式的生成，我们的研究也表明，[学会预测](https://deepmind.com/blog/article/reinforcement-learning-unsupervised-auxiliary-tasks)环境的[不同方面](https://deepmind.com/research/publications/neural-predictive-belief-representations/)能够丰富智能体的[世界模型](https://arxiv.org/abs/1803.10760)，进而提升其解决问题的能力。

这些结果与我们关于人类心智的直觉相互呼应。在没有显式监督的情况下学习关于世界的知识，正是我们所谓智能的根本所在。乘火车时，我们可能无精打采地望着窗外，用手指抚过座椅的天鹅绒，打量坐在对面的乘客。我们做这些观察并没有什么议程：我们几乎情不自禁地在收集信息，我们的大脑不知疲倦地运转，努力理解我们周围的世界，以及我们在其中的位置。
