---
title: "塑造先进机器人技术的未来"
title_en: "Shaping the future of advanced robotics"
source: https://deepmind.google/blog/shaping-the-future-of-advanced-robotics/
site: deepmind
date: 2024-01-04
crawled: 2026-09-13
translated: 2026-09-13
---

# 塑造先进机器人技术的未来

> 原文：[Shaping the future of advanced robotics](https://deepmind.google/blog/shaping-the-future-of-advanced-robotics/) · Google DeepMind

介绍 AutoRT、SARA-RT 和 RT-Trajectory，以改进真实世界机器人数据收集、速度与泛化能力

想象这样一个未来：只需对你的个人机器人助手说一句「整理房子」或「给我们做一顿美味健康的饭菜」，这些活儿就都办妥了。这些对人类来说轻而易举的任务，对机器人而言需要对世界的高层次理解。

今天，我们宣布机器人研究领域的一系列进展，让我们离这个未来更近一步。AutoRT、SARA-RT 和 RT-Trajectory 建立在我们具有历史意义的 [Robotics Transformers](https://deepmind.google/discover/blog/rt-2-new-model-translates-vision-and-language-into-action/) 工作之上，帮助机器人更快地决策，并更好地理解和适应它们的环境。

## AutoRT：利用大模型更好地训练机器人

我们介绍 [AutoRT](https://auto-rt.github.io/)，一个 harness 大型基础模型潜力的系统，这对创造能够理解人类实际目标的机器人至关重要。通过收集更多经验性训练数据——以及更多样化的数据——AutoRT 可以帮助扩展机器人学习规模，更好地训练面向真实世界的机器人。

AutoRT 将大型基础模型（如大语言模型（LLM）或视觉语言模型（VLM））与机器人控制模型（RT-1 或 RT-2）相结合，创建出一个可以将机器人部署到新颖环境中收集训练数据的系统。AutoRT 可以同时指挥多台机器人——每台配备一个摄像头和一个末端执行器——在一系列场景中执行多样化任务。对于每台机器人，系统使用 VLM 理解其环境和视野内的物体。接着，LLM 会建议一份机器人可以执行的创意任务清单，例如「把零食放到台面上」，并扮演决策者的角色，为机器人挑选一项合适的任务来执行。

在长达七个月的大规模真实世界评估中，该系统在多座办公楼中安全地同时协调多达 20 台机器人、总计多达 52 台不同的机器人，收集了包含 77,000 次机器人试验、覆盖 6,650 个独特任务的多样化数据集。

![一幅流程图，展示 AutoRT 数据收集的五个步骤：1. 探索（绘制环境地图）；2. 任务生成（用 VLM 描述物体、用 LLM 生成诸如擦拭台面之类的任务）；3. 任务过滤（用 LLM 根据可行性与安全性过滤任务）；4. 数据收集（机器人执行所选任务）；5. 数据多样性评分（将数据绘制在散点图上，然后重复该过程）。](https://lh3.googleusercontent.com/WooC0XNhBLULqzULW_Bv7CS0DtTqdEmOV7u_GtY8OcIxRq5m19-m8_Y_YmtUxf5lfX5xg0hahuGexU8_tnXL78MGPfKMF4YLTEJ1kwg_xlDUCK-BxA=w1440)

（1）一台自主轮式机器人找到一个放置着多个物品的位置。（2）VLM 向 LLM 描述场景与物体。（3）LLM 为机器人建议多样化的操作任务，并判断哪些任务机器人可以独立完成、哪些需要人类遥控、哪些不可能完成，然后做出选择。（4）尝试执行所选任务，收集经验数据，并对数据的多样性/新颖性进行评分。重复以上过程。

## 分层安全协议至关重要

在机器人融入我们的日常生活之前，它们需要以负责任的方式开发，并用扎实的研究证明其真实世界安全性。

虽然 AutoRT 是一个数据收集系统，但它也是面向真实世界应用的自主机器人的一次早期示范。它具备安全防护栏，其中之一是为其基于 LLM 的决策者提供一部「机器人宪法」（Robot Constitution）——一套在为机器人挑选任务时必须遵守的、以安全为先的提示词。这些规则部分受到艾萨克·阿西莫夫（Isaac Asimov）机器人三定律的启发——首要的一条是机器人「不得伤害人类」。进一步的安全规则要求任何机器人不得尝试涉及人类、动物、尖锐物体或电器的任务。

但即使大模型通过自我批判的方式获得了正确的提示，仅凭这一点也无法保证安全。因此 AutoRT 系统还包含来自经典机器人技术的多层实用安全措施。例如，协作机器人被设定为当关节受力超过给定阈值时自动停止，并且所有在役机器人都处于人类监督者的视线范围内，后者配有物理断电开关。

## SARA-RT：让 Robotics Transformers 更精简、更快速

我们的新系统 [Self-Adaptive Robust Attention for Robotics Transformers](https://sites.google.com/corp/view/rtsara/)（SARA-RT），可将 Robotics Transformer（RT）模型转换为更高效的版本。

我们团队开发的 RT 神经网络架构被用于最新的机器人控制系统，包括我们最先进的 [RT-2 模型](https://deepmind.google/discover/blog/rt-2-new-model-translates-vision-and-language-into-action/)。在提供一小段图像历史之后，最好的 SARA-RT-2 模型比 RT-2 模型准确率高 10.6%、速度快 14%。我们相信这是首个能够在不损失质量的前提下提供计算改进的可扩展注意力机制。

虽然 Transformer 功能强大，但它们可能受制于拖慢决策的计算需求。Transformer 在关键上依赖二次复杂度的注意力模块。这意味着，如果 RT 模型的输入翻倍——例如给机器人增加额外的或更高分辨率的传感器——处理该输入所需的计算资源将增加四倍，从而拖慢决策。

SARA-RT 使用一种我们称为「上训练」（up-training）的新型模型微调方法让模型更高效。上训练将二次复杂度转化为线性复杂度，大幅降低计算需求。这种转换不仅提高了原始模型的速度，还保持了其质量。

我们以易用性为目标设计了这个系统，并希望许多研究者和从业者能将其应用于机器人学及其他领域。由于 SARA 提供了一个为 Transformer 提速的通用配方，且无需计算昂贵的预训练，这一方法有望大规模扩展 Transformer 技术的使用。SARA-RT 不需要任何额外的代码，因为可以使用各种开源的线性变体。

当我们将 SARA-RT 应用于拥有数十亿参数的最先进 RT-2 模型时，它带来了更快的决策速度，并在广泛的机器人任务上取得更好的表现。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

用于操作任务的 SARA-RT-2 模型。机器人的动作以图像和文本命令为条件。

凭借扎实的理论基础，SARA-RT 可以应用于多种 Transformer 模型。例如，将 SARA-RT 应用于[点云 Transformer](https://arxiv.org/abs/2012.09688)（Point Cloud Transformers，用于处理机器人深度摄像头的空间数据）后，其速度提高了一倍以上。

## RT-Trajectory：帮助机器人泛化

对人类来说，理解如何擦桌子是直观的，但机器人将一条指令转化为实际物理运动的方式有许多种可能。

我们开发了一个名为 [RT-Trajectory](https://rt-trajectory.github.io/) 的模型，它会自动在训练视频中添加描述机器人运动的视觉轮廓线。RT-Trajectory 对训练数据集中的每个视频进行叠加，绘制机械臂夹爪执行任务时的 2D 轨迹草图。这些以 RGB 图像形式呈现的轨迹，在模型学习机器人控制策略时为其提供低层次的、实用的视觉提示。

在训练数据中未见的 41 个任务上进行测试时，由 RT-Trajectory 控制的机械臂的表现是现有最先进 RT 模型的两倍以上：任务成功率达到 63%，而 RT-2 为 29%。

传统上，训练机械臂依赖于将抽象自然语言（「擦桌子」）映射到具体动作（合拢夹爪、向左移动、向右移动），这使得模型难以泛化到新任务。相比之下，RT-Trajectory 模型通过解读视频或草图中包含的具体机器人运动，让 RT 模型理解任务的「如何去做」。

该系统用途广泛：RT-Trajectory 还可以通过观看人类演示期望的任务来创建轨迹，甚至可以接受手绘草图。它也可以方便地适配到不同的机器人平台。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![您的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

左：一台由仅用自然语言数据集训练的 RT 模型控制的机器人，在面对「清洁桌子」这一新任务时束手无策。而由 RT-Trajectory 控制的机器人——在经过 2D 轨迹增强的同一数据集上训练——成功规划并执行了擦拭轨迹。

右：经过训练的 RT-Trajectory 模型在面对新任务（「清洁桌子」）时，可以通过多种方式创建 2D 轨迹，既可以借助人类协助，也可以利用视觉语言模型自主完成。

RT-Trajectory 利用了所有机器人数据集中都存在、但当前未被充分利用的丰富机器人运动信息。RT-Trajectory 不仅代表了在打造能够在新情境中高效精准移动的机器人道路上迈出的又一步，也是对既有数据集知识的一次解锁。

## 为下一代机器人奠定基础

通过在我们最先进的 RT-1 和 RT-2 模型的基础上继续构建，以上每一项成果都有助于创造能力更强、更有帮助的机器人。我们展望这样一个未来：这些模型与系统能够被整合起来，打造兼具 RT-Trajectory 的运动泛化能力、SARA-RT 的高效率以及 AutoRT 等模型的大规模数据收集能力的机器人。我们将继续应对当今机器人技术的挑战，并适应更先进机器人技术的新能力与新技术。

**了解更多**

[AutoRT 论文](https://auto-rt.github.io/static/pdf/AutoRT.pdf)[AutoRT GitHub](https://auto-rt.github.io/)[SARA-RT 论文](https://arxiv.org/abs/2312.01990)[SARA-RT 网站](https://sites.google.com/corp/view/rtsara/)[RT-Trajectory 论文](https://arxiv.org/abs/2311.01977)[RT-Trajectory GitHub](https://rt-trajectory.github.io/)[访问 Open X-Embodiment 数据集](https://github.com/google-deepmind/open_x_embodiment)

**补充说明**

我们感谢 Krzysztof Choromanski、Keerthana Gopalakrishnan、Alex Irpan 和 Ted Xiao 对本博客的贡献。

我们还要感谢三篇论文的所有 contributing 作者。

AutoRT：Michael Ahn, Debidatta Dwibedi, Chelsea Finn, Montse Gonzalez Arenas, Keerthana Gopalakrishnan, Karol Hausman, Brian Ichter, Alex Irpan, Nikhil Joshi, Ryan Julian, Sean Kirmani, Isabel Leal, Edward Lee, Sergey Levine, Yao Lu, Sharath Maddineni, Kanishka Rao, Dorsa Sadigh, Pannag Sanketi, Pierre Sermanet, Quan Vuong, Stefan Welker, Fei Xia, Ted Xiao, Peng Xu, Steve Xu, Zhuo Xu

SARA-RT：Isabel Leal, Krzysztof Choromanski, Deepali Jain, Avinava Dubey, Jake Varley, Michael Ryoo, Yao Lu, Frederick Liu, Vikas Sindhwani, Quan Vuong, Tamas Sarlos, Ken Oslund, Karol Hausman, Kanishka Rao

RT-Trajectory：Jiayuan Gu, Sean Kirmani, Paul Wohlhart, Yao Lu, Montserrat Gonzalez Arenas, Kanishka Rao, Wenhao Yu, Chuyuan Fu, Keerthana Gopalakrishnan, Zhuo Xu, Priya Sundaresan, Peng Xu, Hao Su, Karol Hausman, Chelsea Finn, Quan Vuong, Ted Xiao

最后，我们感谢 Vincent Vanhoucke 对这些论文研究所给予的支持。
