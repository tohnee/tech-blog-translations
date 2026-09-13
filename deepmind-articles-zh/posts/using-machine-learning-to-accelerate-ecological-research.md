---
title: "用机器学习加速生态学研究"
title_en: "Using machine learning to accelerate ecological research"
source: https://deepmind.google/blog/using-machine-learning-to-accelerate-ecological-research/
site: deepmind
date: 2019-08-08
crawled: 2026-09-13
translated: 2026-09-13
---

# 用机器学习加速生态学研究

> 原文：[Using machine learning to accelerate ecological research](https://deepmind.google/blog/using-machine-learning-to-accelerate-ecological-research/) · Google DeepMind

塞伦盖蒂是世界上仅存的少数仍保有完整大型哺乳动物群落的地区之一。这些动物在广袤的土地上漫步，其中一些会跟随季节性降雨跨越多个国家迁徙数千英里。随着人类对该区域周边的开发日益加剧，这些物种被迫改变自身的行为以求生存。农业扩张、偷猎和气候异常都在推动动物行为与种群动态发生变化，但这些变化发生的空间与时间尺度，用传统研究方法很难监测。在人类压力不断增长的当下，理解这些动物群落如何运转已刻不容缓——这既是为了理解这最后几片原始生态系统的动态，也是为了制定有效的管理方案，以保护和维系这一独特生物多样性热点的完整性。

为此，DeepMind 正与生态学家和自然保护工作者合作，开发机器学习方法，帮助研究坦桑尼亚塞伦盖蒂国家公园与 Grumeti 保护区内整个非洲动物群落的行为动态。塞伦盖蒂—马拉生态系统的生物多样性在全球无与伦比，拥有约 70 种大型哺乳动物和 500 种鸟类，这在一定程度上要归功于其独特的地质条件与多样的栖息地类型。近十年前，塞伦盖蒂狮子研究计划在保护区核心地带安装了数百台运动感应相机。这些相机由路过的野生动物触发，能够在广阔的空间尺度上频繁捕捉动物影像，让研究者能够以很高的时空分辨率研究动物的行为、分布与种群统计。

![一张红外触发相机拍摄的猎豹特写照片，猎豹望向画面之外，背景是长满青草的稀树草原与蓝天。](https://lh3.googleusercontent.com/9bnhBbcx7g-0J514I7L7EEhzsnzqsZuIPv29BvoomJYaSMecv-ty7rEC9yLZtvqzoxvw-Zsd9pbFKWhBRABiFSwSD2_Rj0RDBLf9JSf92InlMie2=w1440)

红外触发相机中的运动传感器会在不干扰动物日常活动的情况下触发拍摄，记录下自然状态下的动物。照片可能是空的——由误报触发——也可能拍到处于不同距离和姿态的数十个个体。被监测的物种从土豚到斑马，无所不包。

过去九年里，团队已经收集并存储了数百万张类似上文的照片。此前，来自世界各地的志愿者一直借助 [Zooniverse](https://www.zooniverse.org/projects/zooniverse/snapshot-serengeti) 网络平台人工识别并清点照片中的物种，该平台托管着许多面向公民科学家的类似项目。这项工作产出了一个内容丰富的[数据集](https://datadryad.org/resource/doi:10.5061/dryad.5pt92)——[Snapshot Serengeti](https://www.nature.com/articles/sdata201526)，包含约 50 个不同物种的标签和数量统计。目前的标注过程费时费力：从相机被触发到从志愿者那里收集到标签，最长需要一年。这一瓶颈不仅妨碍了科学家开展基础研究的能力，也让自然保护工作者难以针对扰乱生态系统的挑战与扰动做出灵活应对。为了帮助研究者更高效地释放这批数据的价值，我们使用 [Snapshot Serengeti 数据集](https://www.nature.com/articles/sdata201526)训练机器学习模型，实现对动物的自动检测、识别与计数。

![一张红外触发相机拍摄的非洲水牛特写照片，水牛把鼻子凑到了镜头正前方。](https://lh3.googleusercontent.com/d_hM5xc3o_d8buOYiwGBbRH3KWalGlsaH4tkXWfeZL1uDozVDET9UR9fZYnn7THVKAAhOhWg8NQhNgnc86Ac_XmXmlvvkOhCFV5q9A0K7MoY7avablI=w1440)

运动感应相机拍到的正在觅食的水牛。注意，标注照片中的物种并非易事——有时动物全身被遮挡，或只拍到身体的某一部分，或只有一部分是清晰的。我们的系统目前在正确识别约 50 个大型物种方面的准确率已与人工标注者相当。

将机器学习用于自然保护并非新事。例如，此前有研究者利用[游客照片](https://www.cell.com/current-biology/fulltext/S0960-9822(19)30626-8?dgcid=raven_jbs_etoc_email)和 [YouTube 视频](https://www.nationalgeographic.co.uk/animals/2018/11/how-artificial-intelligence-changing-wildlife-research)追踪动物，也有利用[音频录音](https://www.nature.com/articles/d41586-019-00746-1)通过叫声识别物种的。红外触发相机数据很难处理——动物可能失焦，相对于相机可能处于各种不同的距离和位置（如上图所示）。在顶尖生态学家、自然保护工作者 Meredith Palmer 博士的专业指导下，我们的项目迅速成形，如今我们拥有的模型在该地区大多数物种上的表现已达到甚至超过人工标注者的水平。重要的是，这一方法将数据处理流程最多缩短了 9 个月，对野外研究者而言潜力巨大。

当然，野外工作充满挑战，也潜伏着种种意想不到的困难，比如供电线路故障以及网络受限或完全无法联网。我们目前正准备将该软件部署到野外，并研究如何在硬件要求有限、互联网接入很少的情况下安全地运行我们的预训练模型。我们与野外合作者紧密协作，确保我们的技术得到[负责任的](https://www.nature.com/articles/s42256-019-0022-7)使用。一旦部署到位，塞伦盖蒂的研究者将能够直接使用这一工具，帮助他们获得最新的物种信息，更好地支持他们的保护工作。

![一张红外触发相机拍摄的雄性鸵鸟照片，它有着亮粉色的脖颈和腿，站在塞伦盖蒂长满青草的稀树草原上。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62272fab3d02a35aa8b88d73_Serengeti204.gif)

一只漫步塞伦盖蒂的鸵鸟。

今年 8 月下旬，我们将在肯尼亚举行的 [Deep Learning Indaba](http://www.deeplearningindaba.com/) 上进一步介绍该项目及相关工作。DeepMind 是 Deep Learning Indaba 的创始合作伙伴——这是一场旨在加强非洲机器学习（ML）与 AI 研究及应用的全洲性运动，多位 DeepMind 研究人员担任这一独特盛会的主要组织者。“Indaba” 是祖鲁语，意为重要的社区集会。今年，作为 8 月下旬在肯尼亚肯雅塔大学举行的主会 [Deep Learning Indaba](http://www.deeplearningindaba.com/) 的前奏，社区自办的 IndabaX AI 会议已在 26 个非洲国家举行。整整一周里，研究者、学生与社区成员将齐聚一堂分享知识与最佳实践，专家们将主持涵盖机器学习与 AI 众多话题的论坛、工作坊与讨论。会议期间，DeepMind 与其他 Indaba 志愿者将共同举办一场黑客马拉松，供所有对 ML 与自然保护感兴趣的人使用 [Snapshot Serengeti](https://www.zooniverse.org/projects/zooniverse/snapshot-serengeti) 数据集开发自己的模型。生态学专业的学生将学会理解并把 ML 模型用于保护工作，还将学习如何开发自己的模型。通过 Indaba 这样的聚会，我们希望让更多当地专家有能力运用 AI 技术解决他们自己社区的问题。非洲的 AI 社区正在壮大，这场黑客马拉松将有助于培养本地专家，并把自然保护作为核心对话的一部分。

![一张红外触发相机拍摄的照片：清晨的金色草地上，一头年轻的雄狮和一只幼狮坐在塞伦盖蒂。](https://lh3.googleusercontent.com/5PwngeLDjj3V8Xb87LuRvLKOde4pl3dlVqcQYlPY8k--Xz28K4w0PZ5HFtq4-0FDUiA4QVuGMUWOHBpnsgDwsYyN_GgXMXN7be5cFgSSPVBVgSo3NA=w1440)

一头狮子与一只幼狮。

DeepMind 科学团队致力于利用 AI 应对影响世界的重大科学挑战。我们已经开发出一个稳健的模型，用于在野外数据中检测和分析动物种群，并协助整合数据，让不断壮大的非洲机器学习社区能够构建用于自然保护的 AI 系统——我们希望这些系统能推广到其他保护区。接下来，我们将通过实地部署来验证模型并跟踪其进展。我们希望为让 AI 研究更具包容性贡献力量——无论是在其应用的领域类型上，还是在开发它的人群上。因此，参加 Indaba 这样的会议，对于建设一支能够把机器学习应用于多样化项目的全球 AI 从业者队伍至关重要。

![一张红外触发相机拍摄的照片：塞伦盖蒂的斑马扬起一片尘土。](https://lh3.googleusercontent.com/VOVDRDF-g62l8Ksy9VPl9PHwdQPWxdZbmD6jFcxvjVz8qONR2BgovsiGUpRgMpU4fNwG4Tz7xOUAWSMQsBZCoBK4qdn_99PUThO8Qv8JA5kbQIY4Aps=w1440)

一匹斑马疾驰穿过草原。

**项目致谢**

Jean-baptiste Alayrac、Sam Blackwell、Joao Carreira、Reena Chopra、Sander Dieleman、Brian McWilliams、Sofia Miñano、Sanjana Narayanan、Meredith Palmer、Ulrich Paquet、Stig Petersen、Roman Werpachowski、Michal Zielinski。

其他致谢

Razia Ahamed、Andrea Banino、Pushmeet Kohli、Drew Purves、Andrew Zisserman

本工作有赖于 Snapshot Serengeti 提供的数据。图像依据[知识共享署名 4.0 国际许可协议（Creative Commons Attribution 4.0 International License）](https://creativecommons.org/licenses/by/4.0/)提供，可在[这里](https://datadryad.org/resource/doi:10.5061/dryad.5pt92)获取。数据相关咨询请联系 [Meredith Palmer 博士](mailto:palme516@umn.edu)。

Swanson AB, Kosmala M, Lintott CJ, Simpson RJ, Smith A, Packer C (2015) Snapshot Serengeti, high-frequency annotated camera trap images of 40 mammalian species in an African savanna. Scientific Data 2: 150026
