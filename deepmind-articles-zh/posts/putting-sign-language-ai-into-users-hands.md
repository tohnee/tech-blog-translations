---
title: "把手语 AI 交到用户手中"
title_en: "Putting sign language AI into users’ hands"
source: https://deepmind.google/blog/putting-sign-language-ai-into-users-hands/
site: deepmind
date: 2026-08-12
crawled: 2026-09-13
translated: 2026-09-13
---

# 把手语 AI 交到用户手中

> 原文：[Putting sign language AI into users’ hands](https://deepmind.google/blog/putting-sign-language-ai-into-users-hands/) · Google DeepMind

介绍手语转文本（sign-language-to-text, SL2T）——我们的突破性模型，为听障及重听用户驱动全新的手语功能。

近几十年来，AI 处理口语的能力突飞猛进，实现了让听人用户感觉毫不费力的自动翻译、听写和对话式界面。然而这场技术革命还没有触及世界上 200 多种手语——以及估计 7000 万使用手语的听障及重听人群。

今天，我们推出一个大规模多语言手语转文本（SL2T）翻译模型，它在质量和通用性上都是一个突破。借助它，我们首次将手语 AI 带出实验室、进入消费级产品：SL2T 为 [Pixel 11](https://store.google.com/magazine/google_pixel_11) 上的 Gboard 和 Live Transcribe 中的手语转文本听写功能提供支持，首先支持美国手语（ASL）到英语。更多设备即将支持，更多语言也将陆续跟进。

就像听人用户可以用听写来代替打字一样，这一功能让听障用户在通常需要打字的任何地方都可以对着手机打手语。你可以打手语来搜索网页、起草消息或文档，并让 Gemini 解决查询或执行任务。在 Live Transcribe 中，你可以在对话中打手语回应，而不必来回打字。据我们的测试者反映，用 ASL 打手语比用英文打字更快、更自然、也更令人愉悦。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

由 SL2T 驱动的手语转文本功能，让用户在通常需要打字的任何地方都可以对着手机打手语。

## 手语为什么重要

手语是世界各地听障社区的主要语言，也是听障文化认同的基石。听障人士在打手语、说话、阅读和写作方面的熟练程度差异很大，因此支持所有模态的访问非常重要。听障人士可以从手语处理中获益，正如听人从口语处理中获益一样；此外，这项技术为弥合听障社区与听人社区之间的沟通鸿沟开辟了新的可能。尽管有如此积极的社会影响机会，手语 AI 的进展却一直缓慢——既因为为手语构建 AI 存在复杂的挑战，也因为对手语本身如何运作存在普遍的误解。

与口语转写相比，手语翻译面临两个核心挑战。首先，转写语音是同一语言内从声音到文本的顺序映射，而手语是独立的自然语言，拥有自己独特的语法和词汇。因此，手语需要真正的机器翻译，而不是手语到词语的顺序转换过程。其次，模型必须学会「看」并理解身体动作。手语通过双手、手臂、躯干、头部和面部的同步动作来传达意义。以高帧率准确追踪这些动作是一项困难且计算量大的计算机视觉任务。

有了这样的背景，就容易理解为什么一些早期的手语技术尝试（如手语手套）存在根本性局限：手语并不只是「戴在手上的英语」。它们需要对细粒度全身动作的复杂视觉感知，以及成熟的语言翻译。SL2T 的设计目标就是同时做到这两点。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

SL2T 将手语输入视为打手语者身体上的关键点，并将其翻译为流式文本输出。示例来自 FLEURS-ASL 基准测试。

## SL2T 的工作原理

我们构建 SL2T 的方式，是将以用户为中心、具有文化意识的方法与大规模数据扩展相结合。该模型在超过 50 种手语、超过 100,000 小时的数据上训练——其中大约四分之一是 ASL 数据。在多种语言、方言和熟练程度的数据上联合训练，使模型学到共享的底层结构，在我们的实验中优于单语言模型。

为了保护用户隐私，SL2T 将手语视为一组姿态关键点位置的序列，而不是原始摄像头画面。一个设备端模型（[MediaPipe Holistic](https://research.google/blog/mediapipe-holistic-simultaneous-face-hand-and-pose-prediction-on-device/)）追踪打手语者身上各点的位置，只有这些几何坐标会被发送到服务器进行翻译，从而使原始视频可以被立即丢弃。

SL2T 将这一坐标序列直接翻译为文本，绕过了此前手语翻译研究广泛使用的、被称为「gloss」的中间标注。Gloss 无法捕捉手语丰富而非线性的方面，例如非手控标记（non-manual markers）和空间构式。直接从关键点进行翻译消除了人为的词表限制，并让翻译质量随数据直接扩展。

根据 [FLEURS-ASL](https://www.kaggle.com/datasets/googleai/fleurs-asl)（sd-test）等评估 ASL 到英语翻译质量的关键基准，SL2T 是迄今能力最强的手语翻译模型。SL2T 取得了 70 BLEURT 的显著零样本（zero-shot）分数，远高于此前任何已报告的分数。但只优化学术基准并不能保证在真实应用中的可用性，因此我们在实际问题上下了很大功夫，例如最小化流式延迟、防止在非手语输入上产生幻觉、为 10% 左撇子打手语者确保公平性，以及改善单手打手语（即另一只手拿着智能手机时使用的方式）的性能。

| 原始英文 | SL2T 的 ASL → 英文输出 |
| --- | --- |
| The Cook Islands do not have any cities but are composed of 15 different islands. The main ones are Rarotonga and Aitutaki. | The Cook Islands have no cities and consist of 15 islands. The two main islands are Rarotonga and Aitutaki. |
| The games kicked off at 10:00am with great weather and apart from mid morning drizzle which quickly cleared up, it was a perfect day for 7's rugby. | Games start at 10 a.m. in great weather. There is a light rain in the morning that clears up. It's a perfect day for 7v7 rugby. |
| In some federal countries, such as the United States and Canada, income tax is levied both at the federal level and at the local level, so the rates and brackets can vary from region to region. | In some federal countries, like the US and Canada, income tax is collected at both the federal and local levels. This means that the rates and brackets vary depending on your region. |
| This fully feathered, warm blooded bird of prey was believed to have walked upright on two legs with claws like the Velociraptor. | This creature is warm-blooded, eats grey, and is covered in feathers. It is believed that it walks on two legs like a velociraptor. |
| Maybe one day, your great grandchildren will be standing atop an alien world wondering about their ancient ancestors? | Maybe one day your great-grandchildren will stand on an alien world and reflect on their ancestors. |

FLEURS-ASL 基准测试中的示例。SL2T 将复杂的 ASL 准确翻译为流畅的英语。偶发错误仍存在于罕见手语、快速手指拼写（"prey" → "grey"）、被动结构、类标记描绘（丢失了 "claws"）以及缺乏上下文的时态（"kicked off" → "start"）中。

## 与社区共同构建

我们相信是*与*听障社区共同构建，而不仅仅是*为*它构建。听障视角塑造了这一项目的每一个阶段——从听障 Googler Sam Sepah 的概念构思，到与听障伙伴共同收集数据、在听障用户研究中进行评估，以及与听障专家一起评估技术影响。

为了指导负责任的现实部署，我们成立了 AI 手语咨询委员会（AI Sign Language Advisory Committee, AISLAC），汇聚了众多全球听障组织和领域专家。通过这一参与式治理模式，受我们技术影响最大的社区可以直接影响我们的开发优先级。我们为 SL2T 1.0 在 Gboard 和 Live Transcribe 中的发布共同撰写了一份[联合影响报告](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/putting-sign-language-ai-into-users-hands/aislac-joint-impact-report-for-sl2t-1-0.pdf)，透明地详述了该技术的能力和当前局限——我们计划在所有重大手语版本发布中延续这种协作方式。

## 展望未来

SL2T 建立在学术界和工业界数十年的基础研究之上，但将 ASL 输入带到用户的手机上只是开始。Google 的使命是整合全球信息，使人人皆可访问并从中受益。实现普适可访问性意味着要达到与口语和书面语完全对等的水平。我们的团队正努力将这项技术扩展到更多手语、手语生成以及前沿 AI 能力。我们期待负责任地分享我们的进展，让通过手语进行访问成为整个数字领域的标准。

你可以在 [Pixel 11](https://store.google.com/magazine/google_pixel_11) 上率先在 Gboard 和 Live Transcribe 中体验 SL2T，更多设备即将支持——全部无需额外付费。

## 致谢

这项工作由 Google DeepMind 和 Android 的团队共同完成。开发 SL2T 模型的核心团队是：Garrett Tanzer, Benoit Brard, Elizabeth Clark, Tim Dozat, Sebastian Ebert, Dan Garrette, Manfred Georg, Vicky Holgate, Shankar Kumar, Mohammad Saboorian, Miloš Stanojević, Megh Umekar, John Wieting, Andy Zhang 和 Chris Dyer。

将模型集成到 Gboard 和 Live Transcribe 的 Android 团队是：Ausmus Chang, Sai Aditya Chitturu, Dayle Chiu, Anna Chou, Ajay Dudani, Angana Ghosh, Alex Huang, Joanne Kim, Ed Lee, Thomas Lin, James Su, Yanchao Su 和 Sharlene Yuan。

我们感谢以下人员提供的额外支持：Anelia Angelova, Abhishek Bapna, Sara Basson, Glenn Cameron, Scott Crowell, Trevor Cohn, Noah Fiedel, Zoubin Ghahramani, Raia Hadsell, Tom Hudson, Alexander Hauerslev Jensen, Kazuya Kawakami, Phoebe Kirk, Peike Li, Liam McCafferty, Caroline Pantofaru, Abhinav Parashar, Christopher Patnoe, Laura Rimell, Sagar Savla, Sam Sepah, Thad Starner, Dave Uthus 和 Biao Zhang。

我们还要感谢 MediaPipe Holistic（Google AI Edge）团队：Ivan Grishchenko, Artsiom Ablavatski, Valentin Bazarevsky, Esha Uboweja, George Sung, Jonathan Baccash, Gregory Karpiak, Sebastian Schmidt, Suril Shah, Raman Sarokin 和 Juhyun Lee。

同时衷心感谢参与我们模型早期测试的所有人。
