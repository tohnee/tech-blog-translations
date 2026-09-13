---
title: "衡量 AI 模型中的感知能力"
title_en: "Measuring perception in AI models"
source: https://deepmind.google/blog/measuring-perception-in-ai-models/
site: deepmind
date: 2022-10-12
crawled: 2026-09-13
translated: 2026-09-13
---

# 衡量 AI 模型中的感知能力

> 原文：[Measuring perception in AI models](https://deepmind.google/blog/measuring-perception-in-ai-models/) · Google DeepMind

基于真实世界的视频、音频与文本数据，为评估多模态系统建立新基准测试

从[图灵测试](https://en.wikipedia.org/wiki/Turing_test)到 [ImageNet](https://www.image-net.org/)，基准测试在塑造人工智能（AI）方面功不可没：它们帮助定义研究目标，并让研究者能够衡量朝这些目标取得的进展。过去 10 年中令人瞩目的突破，例如计算机视觉领域的 [AlexNet](https://proceedings.neurips.cc/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf) 和蛋白质折叠领域的 [AlphaFold](https://www.deepmind.com/research/highlighted-research/alphafold)，都与使用基准测试数据集密切相关——研究者借此为模型设计与训练方案排序，并不断迭代改进模型。在我们朝着构建通用人工智能（AGI）的目标迈进时，开发能够拓展 AI 模型能力的稳健而有效的基准测试，与开发模型本身同等重要。

感知——通过感官体验世界的过程——是智能的重要组成部分。构建对世界具备人类水平感知理解的智能体，是一项核心却充满挑战的任务，它在机器人、自动驾驶汽车、个人助理、医学影像等领域正变得日益重要。因此今天，我们推出 [Perception Test](https://storage.googleapis.com/dm-perception-test/perception_test_report.pdf)——一个使用真实世界视频的多模态基准测试，帮助评估模型的感知能力。

## 开发感知基准测试

目前 AI 研究中已经使用了许多与感知相关的基准测试，例如用于视频动作识别的 [Kinetics](https://www.deepmind.com/open-source/kinetics)、用于音频事件分类的 [Audioset](https://research.google.com/audioset/)、用于目标跟踪的 [MOT](https://motchallenge.net/)，以及用于图像问答的 [VQA](https://visualqa.org/)。这些基准测试推动了 AI 模型架构与训练方法构建和发展上的惊人进步，但每一个都只针对感知的有限方面：图像基准测试排除了时间维度；视觉问答倾向于聚焦高层语义的场景理解；目标跟踪任务通常只捕捉单个物体较低层次的外观特征，例如颜色或纹理。而同时在音频与视觉两种模态上定义任务的基准测试更是凤毛麟角。

多模态模型，例如 [Perceiver](https://deepmind.google/blog/building-architectures-that-can-handle-the-worlds-data/)、[Flamingo](https://deepmind.google/blog/tackling-multiple-tasks-with-a-single-visual-language-model/) 或 [BEiT-3](https://arxiv.org/pdf/2208.10442.pdf)，志在成为更通用的感知模型。但由于此前没有专用基准测试可用，它们的评估只能基于多个专门数据集。这一过程缓慢、昂贵，而且对记忆等通用感知能力的覆盖不完整，使研究者难以比较不同方法。

为了解决其中许多问题，我们创建了一个由专门设计的真实世界活动视频组成的数据集，并按照六种不同类型的任务进行标注：

1. **目标跟踪：** 视频早期给出某个物体的边界框，模型必须返回贯穿整个视频的完整轨迹（包括遮挡期间）。
2. **点跟踪：** 视频早期选定一个点，模型必须跟踪该点贯穿整个视频（同样包括遮挡期间）。
3. **时序动作定位：** 模型必须在时间上定位并分类一组预定义的动作。
4. **时序声音定位：** 模型必须在时间上定位并分类一组预定义的声音。
5. **多选题式视频问答：** 关于视频的文本问题，每题有三个选项供选择答案。
6. **锚定式视频问答：** 关于视频的文本问题，模型需要返回一条或多条物体轨迹。

我们从发展心理学中评估儿童感知的方式中汲取灵感，也借鉴了 [CATER](https://rohitgirdhar.github.io/CATER/) 和 [CLEVRER](http://clevrer.csail.mit.edu/) 等合成数据集，设计了 37 个视频脚本，每个脚本包含不同变体以确保数据集的均衡。每个变体由至少十多名众包参与者拍摄（与此前的 [Charades](https://prior.allenai.org/projects/charades) 和 [Something-Something](https://developer.qualcomm.com/software/ai-datasets/something-something) 工作类似），共有超过 100 名参与者，最终得到 11,609 个视频，平均时长 23 秒。

这些视频展示了简单的游戏或日常活动，使我们能够定义需要以下技能才能求解的任务：

- **语义知识：** 测试任务完成情况，以及对物体、动作或声音的识别。
- **物理理解：** 碰撞、运动、遮挡、空间关系。
- **时序推理或记忆：** 事件的时序排序、随时间计数、检测场景中的变化。
- **抽象能力：** 形状匹配、相同/不同概念、模式检测。

众包参与者为视频添加了空间与时间标注（物体边界框轨迹、点轨迹、动作片段、声音片段）。我们的研究团队针对每个脚本类型设计了多选题与锚定式视频问答任务的问题，以确保所测技能的良好多样性，例如探测反事实推理能力或对给定情境提供解释能力的问题。每个视频对应的答案同样由众包参与者提供。

## 用 Perception Test 评估多模态系统

我们假定模型已在外部数据集和任务上完成预训练。Perception Test 包含一个小型微调集（20%），模型创建者可以选择用它向模型传达任务的性质。其余数据（80%）由公开的验证集和一个保留的测试集组成，后者只能通过我们的评估服务器来评估性能。

这里我们展示评估设置的示意图：输入是一段视频和音频序列，外加一个任务说明。任务可以是高层文本形式的视觉问答，也可以是低层输入，例如目标跟踪任务中物体边界框的坐标。

![在我们基准测试上评估的模型输入与输出流程图。](https://lh3.googleusercontent.com/ke9eHkI90XHD-N1MzaGyI6Wn61IBaYXSj8kH4ZvGZ_4_hO20lW_zlx_fkRwuV_lmQkb6y1iE_4rFMXeSOIR-wnlQLcrP9fLSnzcqAhf6oSBhfrRr1A=w1440)

在我们基准测试上评估的模型的输入（视频、音频，以及文本或其他形式的任务说明）与输出。

评估结果沿多个维度详细呈现，我们在六项计算任务上衡量各项能力。对于视觉问答任务，我们还提供了问题与视频中情境类型以及答题所需推理类型之间的映射，以便进行更细致的分析（更多细节见[我们的论文](https://storage.googleapis.com/dm-perception-test/perception_test_report.pdf)）。理想的模型应当在所有雷达图和所有维度上都取得最高分。这是对模型技能的细致评估，让我们能够定位需要改进的领域。

![三张雷达图，分别按计算任务、领域和推理类型划分。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/634d53562d6ff7e92bbe527c_Perception_Fig_5_Amended.svg)

感知模型按计算任务、领域和推理类型给出的多维诊断报告。还可以进一步细分诊断到运动、碰撞、计数、动作完成等子领域。

确保视频中的参与者与场景的多样性，是开发该基准测试时的一项关键考量。为此，我们从不同国家挑选了不同族裔与性别的参与者，并力求在每种视频脚本类型内部都实现多元的代表性。

![一幅世界地图，标注了若干国家，以展示参与拍摄的众包参与者的地理位置。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/63443fa08c26680347106a0a_Perception_Fig_1.svg)

参与拍摄的众包参与者的地理分布。

## 进一步了解 Perception Test

Perception Test 基准测试已在[这里](https://github.com/deepmind/perception_test/)公开提供，更多细节见[我们的论文](https://storage.googleapis.com/dm-perception-test/perception_test_report.pdf)。排行榜和挑战服务器也将很快上线。

2022 年 10 月 23 日，我们将在特拉维夫举行的欧洲计算机视觉大会（[ECCV 2022](https://eccv2022.ecva.net/)）上举办一场[关于通用感知模型的研讨会](https://computerperception.github.io/)，届时我们将与该领域的其他顶尖专家讨论我们的方法，以及如何设计与评估通用感知模型。

我们希望 Perception Test 能激励并引导面向通用感知模型的进一步研究。未来，我们希望与多模态研究社区合作，为这一基准测试引入更多标注、任务、指标，乃至新的语言。

如果你有兴趣参与贡献，请发邮件至 [perception-test@google.com](mailto:perception-test@google.com) 与我们联系！
