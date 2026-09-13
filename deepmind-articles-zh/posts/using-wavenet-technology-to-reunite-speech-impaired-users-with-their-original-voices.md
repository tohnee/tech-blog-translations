---
title: "用 WaveNet 技术帮助言语障碍用户找回他们原本的声音"
title_en: "Using WaveNet technology to reunite speech-impaired users with their original voices"
source: https://deepmind.google/blog/using-wavenet-technology-to-reunite-speech-impaired-users-with-their-original-voices/
site: deepmind
date: 2019-12-18
crawled: 2026-09-13
translated: 2026-09-13
---

# 用 WaveNet 技术帮助言语障碍用户找回他们原本的声音

> 原文：[Using WaveNet technology to reunite speech-impaired users with their original voices](https://deepmind.google/blog/using-wavenet-technology-to-reunite-speech-impaired-users-with-their-original-voices/) · Google DeepMind

本文介绍了我们最近与 Google 以及渐冻症（ALS）公益倡导者 Tim Shaw 合作开展的一个项目，该项目是 Google Euphonia 项目的一部分。我们展示了文本转语音技术如何利用极少的录制语音数据合成高质量、自然发声的声音的早期概念验证。

少年时代的 Tim Shaw 把一切都投入到了橄榄球训练中：他的梦想是加入 NFL（美国国家橄榄球联盟）。在大学时代为宾州州立大学打球之后，他的抱负终于实现：23 岁时他被卡罗莱纳黑豹队选中，随后又先后效力于芝加哥熊队和田纳西泰坦队，并作为线卫屡破纪录。在 NFL 打了六年球、即将步入巅峰之际，他的状态开始下滑。他再也无法像从前那样擒抱；做引体向上时手臂会从单杠上滑落。在家里，他会掉落购物袋，双腿也开始发软支撑不住。2013 年，Tim 被泰坦队裁掉，但他决心要进入另一支球队。Tim 比以往任何时候都更加刻苦地训练，然而状态却持续下滑。五个月后，他终于找到了原因：他被诊断出患有[肌萎缩侧索硬化症](https://en.wikipedia.org/wiki/Amyotrophic_lateral_sclerosis)（ALS，俗称卢·格里克病）。在 ALS 患者体内，控制自主肌肉的神经元会逐渐死亡，最终导致对身体控制能力的完全丧失。ALS 的病因不明，且至今无法治愈。

如今，Tim 是 ALS 研究的一位[有力的倡导者](https://www.youtube.com/watch?v=BN8-r46Dt5Y)。今年早些时候，他发表了一封[写给年轻自己的信](https://www.theplayerstribune.com/en-us/articles/tim-shaw-titans-letter-to-my-younger-self)，建议学会接纳——「否则，你会把自己悲伤至死。」如今坐轮椅的他，时刻需要父母的照料。ALS 患者行动困难，这种疾病会让说话、吞咽、甚至自主呼吸变得困难，直至完全不可能。无法与人交流，可能是 ALS 患者及其家人面临的最艰难的事情之一。正如 Tim 所说：「无法表达我脑海中的想法，那种挫败感难以言表。我比以往任何时候都清醒，可就是说不出来。」

失去自己的声音可能带来沉重的社交打击。如今，人们保存自己声音的主要选择是[语音库备份（message banking）](http://www.childrenshospital.org/centers-and-services/programs/a-_-e/als-augmentative-communication-program/protocol-of-assessment-considerations/message-banking)，即 ALS 患者用自己原本的语气和语调，将对自己有特殊意义的短语录制并存储下来。语音库备份给 ALS 患者及其家人带来极大的慰藉，帮助他们在极度艰难的时期保住自己身份认同的核心部分——自己的声音。但语音库备份缺乏灵活性，最终得到的只是一个静态的短语数据集。想象一下，你被告知将永远无法再开口说话。再想象一下，你获得了一个机会，可以通过尽可能多地录音来保存自己的声音。你会决定录些什么？你要如何捕捉自己将来最想说的那些话？是一段有意义的故事，一句心爱的口头禅，还是一句简单的「我爱你」？这个过程可能既耗时又令人心力交瘁，尤其是当一个人的声音正在逐渐衰退时。而那些没能及时录制短语的人，只能选择一个千篇一律的电脑合成音——它缺乏本人声音所具有的那种情感连接的力量。

![前 NFL 球员 Tim Shaw 与家人和 Google 研究人员围坐在餐桌旁，互动并微笑。](https://lh3.googleusercontent.com/HiV62hD9rwcxJL03-OLrqe-nlgkjqfW-hploTbeGuBXAht_amAv7HEj8p5TnxbrHq460M4dvUQ9GUIPQ_eJDAmYykiXf68k9QMmb6dS3SdulZRz0-gs=w1440)

Tim 和他的家人与团队的部分成员聊天，这些人正致力于为言语障碍人群构建更好的技术。

## 构建更自然发声的语音技术

在 DeepMind，我们一直在与 Google 以及 Tim Shaw 这样的人合作，开发能让言语困难人群更轻松地交流的技术。这其中的挑战有两方面。首先，我们必须拥有能够识别发音不标准人群语音的技术——Google AI 正通过 [Project Euphonia](https://ai.googleblog.com/2019/08/project-euphonias-personalized-speech.html) 研究这一问题。其次，我们理想中希望人们能够用自己原本的声音进行交流。同样患有 ALS 的 Stephen Hawking（史蒂芬·霍金）所使用的文本转语音合成器，其声音之不自然众所周知。因此，第二个挑战是将文本转语音技术定制为用户自然的说话嗓音。

创造自然发声的语音被认为是 AI 领域的一项「[重大挑战](https://www.gov.uk/government/publications/industrial-strategy-the-grand-challenges/industrial-strategy-the-grand-challenges)」。凭借 [WaveNet](https://deepmind.com/blog/article/wavenet-generative-model-raw-audio) 和 [Tacotron](https://google.github.io/tacotron/)，我们见证了文本转语音系统质量的巨大突破。然而，尽管在某些场景下可以创造出听起来像特定真人的自然语音——正如我们去年与 [John Legend](https://www.blog.google/products/assistant/talk-like-a-legend/) 合作展示的那样——开发合成声音需要数小时的录音棚录制时间，而且要照着非常特定的脚本朗读——这对许多 ALS 患者来说是根本无法企及的奢侈。创建需要更少训练数据的机器学习模型是 DeepMind 的一个活跃研究方向，对于像这样的用例至关重要——在这里，我们只需凭借少量音频录音就能重建一个声音。我们通过发挥 [WaveNet](https://deepmind.com/blog/article/wavenet-generative-model-raw-audio) 方面的工作成果以及论文 [Sample Efficient Adaptive Text-to-Speech](https://arxiv.org/pdf/1809.10460.pdf)（TTS，样本高效自适应文本转语音）中展示的新方法来实现这一目标——我们在该论文中证明了利用少量语音数据创建高质量声音是可能的。

这就说回到 Tim 身上。Tim 和他的家人对我们最近的研究发挥了关键作用。我们的目标是给 Tim 和他的家人一个机会，让他们再次听到他原本的说话声音。得益于 Tim 在媒体聚光灯下的经历，留下了大约三十分钟的高质量音频录音，我们得以运用 WaveNet 和 TTS 的方法来重建他昔日的声音。

经过六个月的努力，Google 的 AI 团队拜访了 Tim 和他的家人，向他展示他们的工作成果。这次会面被记录下来，成为由 Robert Downey Jr. 主持的 YouTube Originals 学习系列节目「[The Age of A.I.](https://www.youtube.com/watch?v=V5aZjsWM2wo)」的一集。用 Tim 的 NFL 时期音频录音训练出的模型，朗读了[他最近写给年轻自己的那封信](https://www.theplayerstribune.com/en-us/articles/tim-shaw-titans-letter-to-my-younger-self)，Tim 和他的家人得以多年来第一次听到他原来的声音。

「我不记得这个声音了，」Tim 说道。他的父亲回答：「我们记得。」后来，Tim 回忆道：「我已经太久没有发出过那样的声音了，我感觉自己焕然一新。就好像缺失的一块重新归位了。太不可思议了。我只是很感激，这个世界上还有人愿意不断突破极限去帮助他人。」

你可以在「[The Age of A.I.](https://www.youtube.com/watch?v=V5aZjsWM2wo)」中进一步了解我们与 Tim 的合作以及他在研究中发挥的关键作用，该节目现已在 [YouTube.com/Learning](https://www.youtube.com/Learning) 上线。

## 这项技术是如何工作的

要理解这项技术的工作原理，首先需要理解 [WaveNet](https://deepmind.com/blog/article/wavenet-generative-model-raw-audio)。WaveNet 是一个生成模型，它使用来自不同说话人的数小时语音和文本数据进行训练。随后可以向它输入任意新文本，将其合成为自然发声的口语句子。

去年，在[样本高效自适应文本转语音](https://arxiv.org/abs/1809.10460)论文中，我们展示了通过一个称为微调（fine-tuning）的过程，只需几分钟而非几小时的录音就可以训练出一个新声音。具体做法是：首先用多达数千名说话人的数据训练一个大型 WaveNet 模型，这一步需要几天时间，直到它能够产出自然发声语音的基本形态。然后，我们拿到目标说话人的小规模语料，对模型进行智能化的适配，调整权重，从而创建出一个与目标说话人匹配的单一模型。微调的概念与人类的学习方式类似。例如，如果你想学习微积分，你应当先掌握基础代数的原理，然后运用这些更简单的概念去帮助求解更复杂的方程。

## 借助 WaveRNN 和 Tacotron 把研究再推进一步

在这篇论文发表之后，我们继续对模型进行迭代。首先，我们从 WaveNet 迁移到了 [WaveRNN](https://deepmind.com/research/publications/efficient-neural-audio-synthesis)，这是由 Google AI 与 DeepMind 联合开发的一种更高效的文本转语音模型。WaveNet 需要额外的蒸馏步骤才能加速到实时响应请求的程度，这让微调变得更加困难。而 WaveRNN 不需要第二次训练步骤，其语音合成速度远快于未经蒸馏的 WaveNet 模型。

除了通过换用 WaveRNN 来加速模型之外，我们还与 Google AI 合作提升模型质量。Google AI 的研究人员证明了类似的微调方法也可以应用于相关的 Google [Tacotron](https://google.github.io/tacotron/) 模型，我们将 Tacotron 与 WaveRNN 结合使用来合成逼真的声音。通过将这两项技术与 Tim Shaw NFL 时期的音频片段相结合进行训练，我们得以生成一个真实可信、酷似 Tim 言语功能退化之前声音的语音。虽然这个声音还不够完美——缺乏真实声音的表现力、独特韵味和可控性——但我们很兴奋，WaveRNN 与 Tacotron 的结合或许能帮助像 Tim 这样的人保住其身份认同中重要的一部分，我们希望有一天能将其集成到语音生成设备中。

> 我已经太久没有发出过那样的声音了，我感觉自己焕然一新。就好像缺失的一块重新归位了。太不可思议了。我只是很感激，这个世界上还有人愿意不断突破极限去帮助他人。

Tim Shaw

## 下一步计划

我们很荣幸能让 Tim 与他的声音短暂重聚。在这个阶段，我们的研究将走向何方还为时尚早，但我们正在探索将 Euphonia 语音识别系统与语音合成技术相结合的途径，让像 Tim 这样的人能够更轻松地交流。我们希望我们的研究最终能更广泛地分享给那些最需要它的人，帮助他们与所爱之人交流——全世界有数千人可能会在未来某一天从这项工作中受益。正如 Tim 在写给年轻自己的信中所说——归根结底，真正重要的是「你生命中那些爱你、关心你的关系和人」。

**合作者**

Zachary Gleicher、Luis C. Cobo、Yannis Assael、Brendan Shillingford、Nando de Freitas、Julie Cattiau、Philip Nelson、Ye Jia、Heiga Zen、Ron Weiss、Zhifeng Chen、Yonghui Wu、Tejas Iyer、Hadar Shemtov、Tim Shaw、Fernando Vieira、Maeve McNally、John Shaw、Sharon Shaw、John Costello
