---
title: "在多种不同机器人类型之间扩展学习"
title_en: "Scaling up learning across many different robot types"
source: https://deepmind.google/blog/scaling-up-learning-across-many-different-robot-types/
site: deepmind
date: 2023-10-03
crawled: 2026-09-13
translated: 2026-09-13
---

# 在多种不同机器人类型之间扩展学习

> 原文：[Scaling up learning across many different robot types](https://deepmind.google/blog/scaling-up-learning-across-many-different-robot-types/) · Google DeepMind

我们与来自 33 个学术实验室的合作伙伴一起，汇集了 22 种不同机器人的数据，创建了 Open X-Embodiment 数据集和 RT-X 模型

机器人是出色的专家，却是糟糕的通才。通常情况下，你必须为每一个任务、每一台机器人和每一个环境分别训练模型。改变哪怕一个变量，往往都要从零开始。但如果我们能融合机器人学领域的知识，创造一种训练通用机器人的方法呢？

今天，我们发布一套面向不同机器人类型（即不同形态，embodiment）的[通用机器人学习新资源](https://arxiv.org/abs/2310.08864)。我们与来自 33 个学术实验室的合作伙伴一起，汇集了 22 种不同机器人的数据，创建了 Open X-Embodiment 数据集。我们还发布了 RT-1-X——一个由 [RT-1](https://blog.research.google/2022/12/rt-1-robotics-transformer-for-real.html) 衍生、在我们的数据集上训练的机器人 Transformer（RT）模型——它展示了技能在多种机器人形态之间的迁移。

在这项工作中，我们证明：在来自多种形态的数据上训练单一模型，其在众多机器人上的表现显著优于在单一形态数据上训练的模型。我们在五个不同的研究实验室测试了 RT-1-X 模型，与为每台机器人独立开发的方法相比，它在五种不同的常用机器人上平均取得了 50% 的成功率提升。我们还证明，在我们的视觉-语言-动作模型 [RT-2](https://www.deepmind.com/blog/rt-2-new-model-translates-vision-and-language-into-action) 上使用多种形态的数据进行训练，使其在真实世界机器人技能上的表现提升了三倍。

我们开发这些工具，是为了与机器人学界共同推进跨形态研究。得益于世界各地共享数据、并帮助评估我们模型的机器人实验室为开放、负责任地开发这项技术所做的工作，Open X-Embodiment 数据集和 RT-1-X 模型检查点现已向更广泛的研究社区开放。我们相信，这些工具将改变机器人的训练方式，并加速这一领域的研究。

## Open X-Embodiment 数据集：为训练 AI 机器人收集数据

数据集以及在其上训练的模型，在推进 AI 发展中发挥了关键作用。正如 [ImageNet](https://www.image-net.org/index.php) 推动了计算机视觉研究，我们相信 Open X-Embodiment 也能同样推动机器人学。构建一个由多样化机器人演示组成的数据集，是训练一个能够控制多种不同类型机器人、遵循多样化指令、对复杂任务进行基本推理并有效泛化的通才模型的关键一步。然而，收集这样的数据集对任何单个实验室来说都过于耗费资源。

为构建 Open X-Embodiment 数据集，我们与来自 20 多个机构的学术研究实验室合作，汇集了 22 种机器人形态的数据，涵盖超过 500 种技能、15 万个任务，总计超过 100 万个回合（episode）。这是同类中最全面的机器人数据集。

![由 24 张视频截图组成的网格，展示各种类型的机械臂执行不同任务。](https://lh3.googleusercontent.com/IY4K4inaQaBbeElljOAXs7m3CIJMTl9OpDz4CgrtlzkTEfn_HHq02c88BbRagmTewAz68ImKt7sPRy4hcm29zNFTRs9nFBrXlR9tSVjBJYPLrDlKow=w1440)

Open X-Embodiment 数据集样本，涵盖超过 500 种技能和 15 万个任务。

![两张条形图说明 Open X-Embodiment 数据集的构成。图 (a)「每种机器人形态的数据集数量」显示 Franka 是代表性最高的机器人，其次是 xArm 和 Sawyer。图 (b)「常见数据集技能」显示数据集中技能的分布，其中「抓取」「移动」「推动」是最高频的动作。](https://lh3.googleusercontent.com/DT05E5se1pTEj1EkJlf0yBAEcSbRUC3q9iyjOmfmb14i_6HTJBhwiVMYDoy7pqK5yGG2WJKk5H8WnhWbeAPAc5RmTTsyPaTEtqpuag_QH2qamrxXs28=w1440)

Open X-Embodiment 数据集融合了跨形态、跨数据集、跨技能的数据。

## RT-X：通用机器人模型

RT-X 建立在我们两个机器人 Transformer 模型之上。我们用 [RT-1](https://blog.research.google/2022/12/rt-1-robotics-transformer-for-real.html)——我们面向大规模真实世界机器人控制的模型——训练了 RT-1-X，并在 [RT-2](https://www.deepmind.com/blog/rt-2-new-model-translates-vision-and-language-into-action)——我们从网络数据和机器人数据中共同学习的视觉-语言-动作（VLA）模型——之上训练了 RT-2-X。由此我们证明：在相同的模型架构下，RT-1-X 和 RT-2-X 之所以能取得更好的性能，得益于它们所训练的数据远为多样化、跨形态。我们还证明，它们超越了在特定领域内训练的模型，展现出更好的泛化能力和新能力。

为了在合作高校中评估 RT-1-X，我们将其与那些为各自特定任务（如开门）开发、并在相应数据集上训练的模型进行比较。使用 Open X-Embodiment 数据集训练的 RT-1-X 平均比原始模型高出 50%。

![条形图显示 RT-1-X 模型在五个不同的大学机器人实验室中持续超越原始方法，平均成功率为 63%，而基线平均为 41%。](https://lh3.googleusercontent.com/UpRLdhH270shlq6EYSQBg0KARHtV4ZRbDNjU2HWn6_n3mvU-8LCfhjryVEHFSgckdgQ9_77WNU1ORhAGoOhJS0ExWYc47B5OhTQ3MfYXtz_q6YHstg=w1440)

RT-1-X 的平均成功率比相应的原始方法高 50%。

![五段简短循环视频片段的合集，展示不同机械臂在各大学实验室执行任务：机械臂与桌面物体交互（CLVR，南加州大学）、将白色线缆穿过金属导槽（RAIL，加州大学伯克利分校）、打开白色橱柜门（CILVR，纽约大学）、用抹布擦拭木质表面（AUTOLab，加州大学伯克利分校）、与纸箱上的按钮交互（AiS，弗莱堡大学）。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/651bf88fe2241d17b4fc187c_Fig3B_RT-X.gif)

在不同合作高校运行的 RT-1-X 评估视频

## RT-X 的涌现技能

为了研究知识在不同机器人之间的迁移，我们用我们的辅助机器人在一些任务上做了实验，这些任务涉及的物体和技能并不存在于 RT-2 数据集中，但存在于另一个面向不同机器人的数据集中。具体来说，在涌现技能方面，RT-2-X 的成功率是我们此前最佳模型 RT-2 的三倍。

我们的结果表明，与其他平台的数据共同训练，为 RT-2-X 带来了原始数据集中不存在的额外技能，使其能够执行新任务。

![条形图显示 RT-2 的平均成功率约为 25%，而 RT-2-X 约为 75%，证明在涌现技能评估中提升了 3 倍。](https://lh3.googleusercontent.com/mKX3hCLy0YOzzwd4gXaM0_K2Mypupwx53B-yBmDrNvgNvmMDCju-4muw4IdSXoiBT4vl925vYWWyZ641qdRIUfAh-RXCx574ujCQ8J85ZLPYSvLV=w1440)

![一段短动画，显示机械臂把一个苹果移动到罐头和橙子之间。然后把苹果移动到一块布的旁边。再把苹果移动到锅的上面。这展示了它理解空间关系的能力。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/651bf8dc08ece07a453c6cdb_Fig5_RT-X.gif)

RT-2-X 展示了对物体之间空间关系的理解。

RT-2-X 展示了 RT-2 模型此前不具备的技能，包括更好的空间理解。例如，如果我们要求机器人「把苹果移到布的旁边」而不是「把苹果移到布上」，轨迹会截然不同。通过把介词从「旁边」换成「上面」，我们就能调节机器人采取的动作。

RT-2-X 表明，把来自其他机器人的数据并入训练，即使对已经拥有大量数据的机器人，也能扩大其可执行任务的范围——但前提是使用容量足够大的架构。

![机械臂识别出一根位于塑料胡萝卜和塑料冰淇淋筒之间的塑料辣椒。然后它拿起辣椒，放进一个黄色篮子里。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/651bf921492f377d1e2866a2_Fig6_RTX.gif)

RT-2-X（55B）：迄今最大的模型之一，在学术实验室中执行未见过的任务

## 负责任地推进机器人研究

机器人研究正处于一个令人振奋但尚早的阶段。新的研究表明，通过用更多样化的数据和更好的模型来扩展学习，有望开发出更有用的辅助机器人。与世界各地的实验室协作并共享资源，对于以开放、负责任的方式推进机器人研究至关重要。我们希望，开源数据并提供安全但功能有限的模型，能够降低门槛、加速研究。机器人学的未来取决于让机器人彼此学习，更重要的是，让研究者相互学习。

这项工作证明了跨形态泛化的模型是可行的，无论是在 Google DeepMind 的机器人上，还是在世界各地不同大学的机器人上，性能都有显著提升。未来的研究可以探索如何将这些进展与 [RoboCat](https://www.deepmind.com/blog/robocat-a-self-improving-robotic-agent) 的自我改进特性相结合，使模型能够凭借自身经验不断改进。另一个未来的方向是进一步探究不同的数据集配比如何影响跨形态泛化，以及这种泛化的提升如何具体体现。

**与我们合作：** [open-x-embodiment@googlegroups.com](mailto:open-x-embodiment@googlegroups.com)

[阅读我们的论文](https://arxiv.org/abs/2310.08864)[访问我们的数据与模型](https://robotics-transformer-x.github.io/)

**注**

我们感谢这项工作的共同作者：Abhishek Padalkar、Acorn Pooley、Ajinkya Jain、Alex Bewley、Alex Herzog、Alex Irpan、Alexander Khazatsky、Anant Rai、Anikait Singh、Anthony Brohan、Antonin Raffin、Ayzaan Wahid、Ben Burgess-Limerick、Beomjoon Kim、Bernhard Schölkopf、Brian Ichter、Cewu Lu、Charles Xu、Chelsea Finn、Chenfeng Xu、Cheng Chi、Chenguang Huang、Christine Chan、Chuer Pan、Chuyuan Fu、Coline Devin、Danny Driess、Deepak Pathak、Dhruv Shah、Dieter Büchler、Dmitry Kalashnikov、Dorsa Sadigh、Edward Johns、Federico Ceola、Fei Xia、Freek Stulp、Gaoyue Zhou、Gaurav S. Sukhatme、Gautam Salhotra、Ge Yan、Giulio Schiavi、Hao Su、Hao-Shu Fang、Haochen Shi、Heni Ben Amor、Henrik I Christensen、Hiroki Furuta、Homer Walke、Hongjie Fang、Igor Mordatch、Ilija Radosavovic、Isabel Leal、Jacky Liang、Jaehyung Kim、Jan Schneider、Jasmine Hsu、Jeannette Bohg、Jeffrey Bingham、Jiajun Wu、Jialin Wu、Jianlan Luo、Jiayuan Gu、Jie Tan、Jihoon Oh、Jitendra Malik、Jonathan Tompson、Jonathan Yang、Joseph J. Lim、João Silvério、Junhyek Han、Kanishka Rao、Karl Pertsch、Karol Hausman、Keegan Go、Keerthana Gopalakrishnan、Ken Goldberg、Kendra Byrne、Kenneth Oslund、Kento Kawaharazuka、Kevin Zhang、Keyvan Majd、Krishan Rana、Krishnan Srinivasan、Lawrence Yunliang Chen、Lerrel Pinto、Liam Tan、Lionel Ott、Lisa Lee、Masayoshi Tomizuka、Maximilian Du、Michael Ahn、Mingtong Zhang、Mingyu Ding、Mohan Kumar Srirama、Mohit Sharma、Moo Jin Kim、Naoaki Kanazawa、Nicklas Hansen、Nicolas Heess、Nikhil J Joshi、Niko Suenderhauf、Norman Di Palo、Nur Muhammad Mahi Shafiullah、Oier Mees、Oliver Kroemer、Pannag R Sanketi、Paul Wohlhart、Peng Xu、Pierre Sermanet、Priya Sundaresan、Quan Vuong、Rafael Rafailov、Ran Tian、Ria Doshi、Roberto Martín-Martín、Russell Mendonca、Rutav Shah、Ryan Hoque、Ryan Julian、Samuel Bustamante、Sean Kirmani、Sergey Levine、Sherry Moore、Shikhar Bahl、Shivin Dass、Shuran Song、Sichun Xu、Siddhant Haldar、Simeon Adebola、Simon Guist、Soroush Nasiriany、Stefan Schaal、Stefan Welker、Stephen Tian、Sudeep Dasari、Suneel Belkhale、Takayuki Osa、Tatsuya Harada、Tatsuya Matsushima、Ted Xiao、Tianhe Yu、Tianli Ding、Todor Davchev、Tony Z. Zhao、Travis Armstrong、Trevor Darrell、Vidhi Jain、Vincent Vanhoucke、Wei Zhan、Wenxuan Zhou、Wolfram Burgard、Xi Chen、Xiaolong Wang、Xinghao Zhu、Xuanlin Li、Yao Lu、Yevgen Chebotar、Yifan Zhou、Yifeng Zhu、Ying Xu、Yixuan Wang、Yonatan Bisk、Yoonyoung Cho、Youngwoon Lee、Yuchen Cui、Yueh-hua Wu、Yujin Tang、Yuke Zhu、Yunzhu Li、Yusuke Iwasawa、Yutaka Matsuo、Zhuo Xu、Zichen Jeff Cui。

作者们还要感谢 Arielle Bier、Dimple Vijaykumar、Gabriella Pearl、Jane Park、Katie McAtackney、Juanita Bawagan、Eleanor Tomlinson、Dex Hunter-Torricke 为本博客内容创作提供的帮助。我们还要感谢 John Guilyard 为本网站制作的精彩动画。我们感谢 Sanah Choudhry、Michael Griessel、Jon Small 提供法律咨询。我们感谢 Yuheng Kuang、Ning Hou、Utsav Malla、Sarah Nguyen、Rochelle Dela Cruz、Justice Carbajal、Brianna Zitkovich、Emily Perez、Elio Prado、Jodilyn Peralta、Tran Pham、Deeksha Manjunath、Samuel Wan、Jaspiar Singh 以及更广泛的 Google DeepMind 团队的反馈与贡献。
