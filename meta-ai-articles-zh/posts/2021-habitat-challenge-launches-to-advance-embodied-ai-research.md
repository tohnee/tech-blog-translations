---
title: "2021 Habitat 挑战赛启动，推进具身 AI 研究"
title_en: "2021 Habitat Challenge launches to advance embodied AI research"
date: 2021-02-17
source: http://ai.facebook.com/blog/2021-habitat-challenge-launches-to-advance-embodied-ai-research
crawled: 2026-09-22
translated: 2026-09-22
---

# 2021 Habitat 挑战赛启动，推进具身 AI 研究

> 原文：[2021 Habitat Challenge launches to advance embodied AI research](http://ai.facebook.com/blog/2021-habitat-challenge-launches-to-advance-embodied-ai-research) · Meta AI（Wayback 存档）

Facebook AI 很高兴启动第三届 Habitat 挑战赛，这是一项开放研究倡议，邀请世界各地的 AI 专家教机器在真实世界环境中导航。Habitat 挑战赛 2021 与佐治亚理工学院合作实施，要求参赛者训练具身智能体，使用 Habitat-Sim（Facebook AI 灵活、高性能的开源 3D 模拟器）执行 PointGoal 导航（「向北走 5 米，再向西走 3 米」）和 ObjectGoal 导航（「去找一把椅子」）任务。

Habitat 挑战赛在计算机视觉与模式识别会议（CVPR）的 2021 具身 AI 研讨会上启动，与另外八项由 15 家学术与研究机构支持的具身 AI 挑战赛协同举行。其中三项研究竞赛同样基于 Habitat-Sim，由 Facebook AI 研究者及我们的密切合作者提供支持。SoundSpaces 挑战赛由 Facebook AI 研究科学家 Kristen Grauman、Changan Chen（得克萨斯大学奥斯汀分校）和 Unnat Jain（伊利诺伊大学厄巴纳-香槟分校）支持，基于他们最近的论文，号召参赛者训练虚拟机器人在多房间 3D 环境中借助听觉与视觉感知导航至声源。类似地，由印度理工学院坎普尔分校、伊利诺伊大学和西蒙弗雷泽大学主办的 MultiON（多目标导航）挑战赛要求参赛者训练智能体在家庭环境中高效导航至一系列物体。Room-Across-Room Habitat 挑战赛（RxR-Habitat）由俄勒冈州立大学、Google 和 Facebook AI 主办，在物体导航任务的基础上要求智能体跟随人类生成的指令（「在拐角处左转，走到厨房」）。

PointGoal 导航任务测试 AI 智能体在逼真模拟空间中高效到达目的地的能力。今年这些挑战赛的联合启动，为具身 AI 研究社区提供了一个前所未有的机会，向着该领域的公共框架迈进——围绕统一的任务集、仿真平台和 3D 资产汇聚。组织者们将在 6 月的 CVPR 上集体分享所有这些挑战赛的结果，为具身 AI 研究的现状和这一子领域的新方向提供独特的观察视角。

当今 AI 研究的核心挑战之一，是教机器在物理世界的复杂情形中移动并智能地运作。这项工作的潜在收益远不止便利性（比如让机器人去厨房拿一串钥匙，或去楼上书桌上取一台笔记本电脑）。具身 AI 还可以帮助视障人士在陌生环境中导航，或在危险或艰难的环境中执行困难任务。AI Habitat 是达成这些目标的核心组件：一个面向具身研究的快速、照片级仿真器，其开放、模块化的设计足够强大和灵活，能为这一子领域带来可复现性和标准化基准。

今年，Habitat 挑战赛的 PointGoal 导航任务把智能体放置在未见过的环境中的随机起点位置和朝向上，要求它导航至目标坐标。没有真值地图可用，智能体只能使用 RGB-D 相机的传感器输入进行导航。在 ObjectGoal 导航中，智能体必须从未见过的环境中的随机位置和朝向出发，找到特定类别的物体（如桌子或椅子）。与另一项挑战一样，智能体没有地图，只能使用传感器输入导航。ObjectGoal 导航任务依赖智能体在模拟空间中移动的能力、其语义理解，以及关于物理空间的常识（例如，壁炉通常位于书房或客厅）。

参赛前请查阅提交指南，并注意参赛者必须向 EvalAI 提交作品。每个赛道获胜团队将受邀提名一名成员，在 CVPR 2021 虚拟活动中分享其工作，我们届时也将公布挑战赛排行榜。

**CVPR 2021 的合作伙伴与具身 AI 挑战赛：**

- iGibson Challenge，由斯坦福视觉与学习实验室和 Google 机器人团队主办
- Habitat Challenge 2021，由 Facebook AI Research（FAIR）和佐治亚理工学院主办
- Navigation and Rearrangement in AI2-THOR，由艾伦人工智能研究所主办
- ALFRED: Interpreting Grounded Instructions for Everyday Tasks，由华盛顿大学、卡内基梅隆大学、艾伦人工智能研究所和南加州大学主办
- Room-Across-Room Habitat Challenge（RxR-Habitat），由俄勒冈州立大学、Google 和 Facebook AI 主办
- SoundSpaces Challenge，由得克萨斯大学奥斯汀分校和伊利诺伊大学厄巴纳-香槟分校主办
- TDW-Transport，由麻省理工学院主办
- Robotic Vision Scene Understanding，由澳大利亚机器人视觉中心联合昆士兰科技大学机器人中心主办
- MultiON: Multi-Object Navigation，由印度理工学院坎普尔分校、伊利诺伊大学厄巴纳-香槟分校和西蒙弗雷泽大学主办

**作者**

- Dhruv Batra，研究科学家
