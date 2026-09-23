---
title: "EgoMimic：佐治亚理工博士生用 Project Aria 研究眼镜帮助训练人形机器人"
title_en: "EgoMimic: Georgia Tech PhD student uses Project Aria Research Glasses to help train humanoid robots"
date: 2025-02-19
source: https://ai.meta.com/blog/egomimic-project-aria-georgia-tech-ego4d-robotics-embodied-ai
crawled: 2026-09-22
translated: 2026-09-22
---

# EgoMimic：佐治亚理工博士生用 Project Aria 研究眼镜帮助训练人形机器人

> 原文：[EgoMimic: Georgia Tech PhD student uses Project Aria Research Glasses to help train humanoid robots](https://ai.meta.com/blog/egomimic-project-aria-georgia-tech-ego4d-robotics-embodied-ai) · Meta AI（Wayback 存档）

2025 年 2 月 19 日

今天，我们重点介绍来自佐治亚理工的新研究：利用 Meta Project Aria 研究眼镜佩戴者的自我中心录像，帮助训练机器人执行日常基本任务。观看下方视频、阅读完整报道，或申请你自己的 Project Aria 研究套件。

想象一下，在家中完成洗衣、洗碗和修理等日常任务时有人帮忙。我们已经在用工具协助这些任务，比如洗衣机、洗碗机和电钻。但如果你能拥有一件更强大、更灵活的工具——一个能向你学习、加速你待办清单上各种体力项目的人形机器人呢？即使你拥有可用的硬件系统，教会机器人做日常任务也只能通过一种缓慢笨重的数据收集方法——机器人遥操作（teleoperation）——来实现。现在有了新办法。借助 Project Aria 研究套件，佐治亚理工的 Danfei Xu 教授及其机器人学习与推理实验室（Robotic Learning and Reasoning Lab）利用 Aria 眼镜上的自我中心传感器，为他们希望人形机器人复现的任务创建所谓的「人类数据」。他们用人类数据大幅减少训练机器人策略所需的遥操作数据量——这一突破有朝一日可能让人形机器人学会人类能够演示的任意数量的任务。

（原文此处附图：Kareer 遥操作机器人为 EgoMimic 采集协同训练数据。遥操作难以规模化，且需要大量人力。）

「传统上，为机器人收集数据意味着创建演示数据，」佐治亚理工交互计算学院的博士生 Simar Kareer 说。「你用控制器操纵机器人的关节让它移动、完成任务，一边录制传感器数据一边重复数百次，然后训练模型。这既缓慢又困难。打破这一循环的唯一办法，就是把数据收集与机器人本身解耦。」

如今，机器人策略模型是用大量针对每个狭窄任务的高成本定向演示数据训练的。Kareer 假设，来自许多研究者的被动收集数据——比如 Aria 眼镜采集的数据——可以转而用于为广泛得多的任务创建数据，在未来造就更通用的机器人。受 Project Aria 和 Ego-Exo4D（包含超过 3000 小时日常生活活动自我中心视频的大型数据集）的启发，Kareer 开发了 EgoMimic——一个利用人类数据和机器人数据开发人形机器人的新算法框架。「当我看到 Ego4D 时，我发现它与我们要收集的所有大型机器人数据集一模一样，只不过主体是人类，」Kareer 解释道。「你只要戴上一副眼镜，然后去做事情。数据不需要来自机器人。它应该来自某种更可扩展、能被动生成的东西——也就是我们。」

在 Kareer 的研究中，Aria 眼镜被用于创建协同训练 EgoMimic 框架的人类数据。

（原文此处附图：Kareer 一边叠 T 恤一边用 Aria 眼镜录制，创建协同训练的人类数据。）

在佐治亚理工的研究中，Aria 眼镜不仅用于人类数据收集，还被用作机器人实时运行设置的组成部分。Aria 眼镜像一双眼睛一样安装在人形机器人平台上，充当集成传感器包，使机器人能够实时感知环境。Aria Client SDK 用于将 Aria 的传感器数据直接流入运行在所连接 PC 上的机器人策略，后者进而控制机器人的驱动。将 Aria 眼镜同时用于数据收集和实时感知流水线，最小化了人类演示者与机器人之间的域差距，为未来机器人任务训练的规模化人类数据生成铺平了道路。

（原文此处附图：安装在机器人顶部的 Aria 眼镜为系统提供传感器数据，使机器人能够感知并与空间交互。）

得益于 EgoMimic，Kareer 仅用 90 分钟的 Aria 录像，就使其机器人在多种任务上的表现相比以往方法提升了 400%。机器人还能在从未见过的环境中成功完成这些任务。未来，人形机器人或许可以用自我中心数据大规模训练，从而像人类一样完成各种任务。

「我们把 Aria 视为对研究社区的一项投资，」Meta Reality Labs Research 产品经理 James Fort 说。「自我中心研究社区越标准化，研究者就越能展开协作。正是通过与社区像这样一起扩展，我们才能开始解决关于未来事物将如何运作的更大问题。」

Kareer 将在亚特兰大举行的 2025 年 IEEE 机器人与自动化工程师国际会议（ICRA）上展示他关于 EgoMimic 的论文。

**了解更多关于 Project Aria 的信息**　**申请 Project Aria 研究套件**
