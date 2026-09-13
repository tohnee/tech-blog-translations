---
title: "用于探索的简单传感器意图"
title_en: "Simple Sensor Intentions for Exploration"
source: https://deepmind.google/blog/simple-sensor-intentions-for-exploration/
site: deepmind
date: 2020-05-12
crawled: 2026-09-13
translated: 2026-09-13
---

# 用于探索的简单传感器意图

> 原文：[Simple Sensor Intentions for Exploration](https://deepmind.google/blog/simple-sensor-intentions-for-exploration/) · Google DeepMind

![一段四个分格的动态图。第一格中，一只抓取器抓起一个绿色方块。第二格内容相同，但背景为黑色。第三格和第四格分别显示沿 x 轴和 y 轴移动的绿色柱状图。随后画面拉远，以不同颜色显示同样的四分格情形。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6228c5d829a96fa1b5f53db5_Fig201.gif)

通过简单的颜色掩蔽，可以得到高层的图像统计量。奖励智能体刻意改变这些统计量，会带来多样化的探索和有趣的行为，例如抓取或举起物体。

## 技能示例

完全从零开始学习，且仅从像素和本体感觉（proprioception）学习。外部奖励是稀疏的，简单传感器意图（Simple Sensor Intentions, SSI）被用作唯一的辅助任务。

![并排的两个视频。左侧，一台橙色机械臂的机器人从平坦的灰色表面上抓取不断变化的多个物体。右侧，同一台机器人在一个大杯子里接住一个黄色的球。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6228c5ead7858131e4ad7dd2_Fig202.gif)
