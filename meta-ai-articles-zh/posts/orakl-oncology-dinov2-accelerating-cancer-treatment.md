---
title: "Orakl Oncology 如何用 DINOv2 加速癌症治疗发现"
title_en: "How Orakl Oncology is using DINOv2 to accelerate cancer treatment discovery"
date: 2025-02-20
source: https://ai.meta.com/blog/orakl-oncology-dinov2-accelerating-cancer-treatment
crawled: 2026-09-22
translated: 2026-09-22
---

# Orakl Oncology 如何用 DINOv2 加速癌症治疗发现

> 原文：[How Orakl Oncology is using DINOv2 to accelerate cancer treatment discovery](https://ai.meta.com/blog/orakl-oncology-dinov2-accelerating-cancer-treatment) · Meta AI（Wayback 存档）

Orakl Oncology 是从欧洲著名的居斯塔夫·鲁西研究所（Gustave Roussy Institute） spinoff 出来的公司，致力于把实验室的实验洞见与机器学习相结合，加速癌症研究和药物开发。他们的使命是帮助研究人员和开发者识别对癌症患者有效的疗法，简化发现流程。为此，Orakl Oncology 对实验室培养的癌细胞（即类器官）进行测试，以模拟药物在真实患者身上的表现。

得益于来自 Jaulin 实验室和 CentraleSupelec 的学术合作者的工作，并作为 RHU ORGANOMIC 计划的一部分，团队意识到他们需要定量化的解决方案来解读其产生的海量成像数据，于是他们寻找一个快速且准确的高效模型。Meta 的 DINOv2 脱颖而出，成为理想选择——得益于其从海量图像集合中学习并赋能高性能计算机视觉模型的能力。虽然研究人员此前使用的是专为类器官定制的模型，但他们发现 DINOv2 更为有效。作为一个开源模型，DINOv2 迅速产生了重大影响：为 Orakl Oncology 团队节省了时间、提升了效率——他们得以及时在类器官图像上训练 DINOv2，从而基于实验室数据更准确地预测患者在临床环境中的反应。

（用 DINOv2 分析类器官得到的注意力图；图片由 Jaulin 实验室的 Emilie Gontran 博士生成。）

「我们的想法基本上是利用这些类器官的图像提取尽可能多的信息，使预测尽可能准确。」Orakl Oncology 联合创始人兼 CTO Gustave Ronteix 说，「我们正在从图像的定性描述，转向可以输入给下游模型的定量描述。」

受益于开源社区的集体知识和贡献，团队得以快速解决早期技术问题，克服了本可能阻碍进展的挑战。「DINOv2 优于其他模型，与其他技术相比准确率提升了 26.8%。」Leo Fillioux 说——他是 MICS 实验室（CentraleSupelec 与巴黎萨克雷大学联合实验室）的博士生，也是该项目的主要贡献者。

DINOv2 的可用性为研究开辟了新途径，消除了团队工作中一些最耗时的环节。例如，此前从视频中提取相关信息需要对单帧或序列做劳动密集型分析；现在有了 DINOv2，这些数据可以直接从视频中提取，让研究人员专注于下游任务。Orakl Oncology 快速开发了他们的平台，在短时间内实现了其他生物医学技术机构耗时多年才建成的东西。「它把焦点从工程上移开，让我们能够直奔科学本身，去寻找到底是什么让你能够预测患者的结局。」Ronteix 说。
