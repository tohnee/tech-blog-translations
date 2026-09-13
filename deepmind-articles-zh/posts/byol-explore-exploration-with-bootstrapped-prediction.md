---
title: "BYOL-Explore：基于自举预测的探索"
title_en: "BYOL-Explore: Exploration with Bootstrapped Prediction"
source: https://deepmind.google/blog/byol-explore-exploration-with-bootstrapped-prediction/
site: deepmind
date: 2022-06-20
crawled: 2026-09-13
translated: 2026-09-13
---

# BYOL-Explore：基于自举预测的探索

> 原文：[BYOL-Explore: Exploration with Bootstrapped Prediction](https://deepmind.google/blog/byol-explore-exploration-with-bootstrapped-prediction/) · Google DeepMind

![分屏游戏画面：左侧是红色平台的第一人称 3D 视角，右侧是来自 DM-HARD-8 任务的俯视图，展示色彩缤纷的迷宫式关卡布局。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62b068d95af4f802873938ec_throw_across_first_1.gif)

BYOL-Explore 智能体在 DM-HARD-8 的 Throw-Across 关卡中的第二人称视角与俯视视图；而纯强化学习和其他基线探索方法在 Throw-Across 关卡上未能取得任何进展。

好奇心驱动的探索（curiosity-driven exploration）是一种主动寻求新信息以增进智能体对环境理解的过程。假设智能体已经学习了一个世界模型，能够根据过往事件的历史预测未来的事件。好奇心驱动的智能体便可以利用世界模型的预测误差作为内在奖励（intrinsic reward），引导其探索策略去寻求新信息。随后，智能体可以用这些新信息来改进世界模型本身，从而做出更好的预测。这一迭代过程可以让智能体最终探索世界中所有的新奇之处，并利用这些信息构建一个准确的世界模型。

受 [bootstrap your own latent](https://arxiv.org/abs/2006.07733)（BYOL）成功的启发——它已被应用于[计算机视觉](https://arxiv.org/abs/2103.16559)、[图表示学习](https://arxiv.org/abs/2102.06514)和 [RL 中的表示学习](https://arxiv.org/abs/2007.05929)——我们提出了 BYOL-Explore：一个概念上简单却通用的、好奇心驱动的 AI 智能体，用于解决高难度探索任务。BYOL-Explore 通过预测自己未来的表示来学习世界的表示。然后，它以表示层面的预测误差作为内在奖励来训练好奇心驱动的策略。因此，BYOL-Explore 仅通过优化表示层面的预测误差，就能同时学习世界表示、世界动力学和好奇心驱动的探索策略。

![BYOL-Explore 架构示意图：较早时间步的 BYOL 世界表示预测未来的 BYOL 表示，预测误差被用作内在奖励来训练 RL 策略。](https://lh3.googleusercontent.com/eh6U_VCPkqhxv9fQhebe9jMV-NqTm5S1eGtTH9KWpG2v2adUWOy8NvTbS5waRkhjL7gS9s4hVvnduLSUEIS4eZO_48KOC7M2BuFAL2ei_ujHeRc284E=w1440)

![多面板动画 GIF，展示 AI 智能体在来自 DM-HARD-8 套件的视觉复杂 3D 环境中以第一人称视角导航，画面中有彩色方块、带纹理的物体和几何障碍物。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62b06901690bcc5c64c64fa7_fp_hard_8_1.gif)

BYOL-Explore、随机网络蒸馏（Random Network Distillation，RND）、内在好奇心模块（Intrinsic Curiosity Module，ICM）与纯 RL（无内在奖励）的比较，以平均截断人类归一化分数（CHNS）衡量。

尽管设计简单，在应用于 [DM-HARD-8](https://arxiv.org/abs/1909.01387) 这组具有挑战性的三维、视觉复杂且难以探索的任务时，BYOL-Explore 以所有任务上测得的平均截断人类归一化分数（CHNS）衡量，胜过了 [随机网络蒸馏](https://arxiv.org/abs/1810.12894)（RND）和[内在好奇心模块](https://arxiv.org/abs/1705.05363)（ICM）等标准好奇心驱动探索方法。值得注意的是，BYOL-Explore 仅用一个同时在所有任务上训练的网络就取得了这一成绩；而此前的相关工作仅限于单任务设置，且只有在提供人类专家演示的情况下才能在这些任务上取得有意义的进展。

作为其通用性的进一步证据，BYOL-Explore 在十个最难探索的 [Atari 游戏](https://arxiv.org/abs/1207.4708)中达到了超越人类的水平，同时其设计比 [Agent57](https://arxiv.org/abs/2003.13350) 和 [Go-Explore](https://arxiv.org/abs/2004.12919) 等其他有竞争力的智能体更为简单。

![折线图对比 BYOL-Explore、BYOL-Explore（big）、RND、ICM 和 RL 在 DM-HARD-8 套件上的平均 CHNS（截断人类归一化分数）百分比随学习步数的变化。两种 BYOL-Explore 变体均优于 RND、ICM 和标准 RL，其中 BYOL-Explore（big）的平均 CHNS 达到 100%。](https://lh3.googleusercontent.com/GIhn_FTvaO-_cY6GhhgHxkmU-8e4xiMNIyWT-w-hqkq-HiRv5_mbOE5K57xddipsHpRVJGBXyuOl3HVO2pv4sUgTmocwn0O0f_3jkuTsgRb_berGqQ=w1440)

BYOL-Explore、随机网络蒸馏（RND）、内在好奇心模块（ICM）与纯 RL（无内在奖励）的比较，以平均截断人类归一化分数（CHNS）衡量。

![折线图展示平均 CHNS（百分比）随学习步数的变化，对比 BYOL-Explore 与 RND、ICM 及标准 RL，BYOL-Explore 显著优于其他方法，峰值约为 70%。](https://lh3.googleusercontent.com/iquw7UVx-hMaTG8ISixsBq6pgYZzY8YVF-cX9HCRZhOhi1lZXYCLQzq2LQRO40gsHC2YIFGNulAmRb9HMTK6kjN9Ig52Iz-VB0-EOALuy0dqMaWsjl8=w1440)

展望未来，我们可以通过学习一个可用于生成未来事件轨迹的概率世界模型，把 BYOL-Explore 推广到高度随机的环境中。这将使智能体能够对环境中可能存在的随机性建模、避开随机陷阱，并规划探索行动。
