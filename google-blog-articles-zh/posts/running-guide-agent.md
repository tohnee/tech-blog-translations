---
title: "跑步指导智能体：迈向无拘无束奔跑的一步"
title_en: "Running Guide agent: A step towards running unbounded"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/running-guide-agent/
site: google-blog
date: 2026-05-20
crawled: 2026-09-13
translated: 2026-09-13
---

# 跑步指导智能体：迈向无拘无束奔跑的一步

> 原文：[Running Guide agent: A step towards running unbounded](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/running-guide-agent/) · Google

对视障与低视力（BLV）运动员来说，跑步历来需要一根有形的绳索——无论是人类领跑员，还是画好的跑道线。今天，我们很高兴分享我们如何用跑步指导智能体（Running Guide agent）朝着改变这一现状迈出步伐：这是一个无障碍智能体，利用实时环境理解帮助低视力运动员跑步。它标志着从简单的路径跟随到先进的实时空间推理的一次巨大飞跃。在我们努力完善这项技术的过程中，目标很简单：让每一位跑者都能获得无需他人协助的独立。

## 为安全不打折扣而生的混合架构

在我们此前 [Project Guideline](https://youtu.be/C_h4HnKVptk?si=MoQceUkIRkP4wbPr) 工作的基础上，跑步指导智能体使用一台胸挂式 Pixel 10 Pro 手机观察前方的道路，并通过听觉反馈引导用户。由于高速运动对系统可信度要求极高，我们构建了一套混合双通道架构：

- **端上分割（on-device segmentation）：** 该模型完全离线运行在 Pixel 10 的定制芯片上，保证超低时延的安全保障。它会立即发出「停止（STOP）」警报和转向提示——以带有方向性的嘀嗒声呈现——即使没有蜂窝网络连接，跑者也能保持可靠的方向感。
- **Gemma 4 的高级推理：** 这条通路由 [Gemma 4 E4B](https://huggingface.co/google/gemma-4-E4B) 驱动，完全在设备端处理复杂的多模态输入（图像和文本），实现高层次的场景理解。为了保持低时延，我们采用了「更聪明的帧选择」（Smarter Frame Selection）：模型不再处理每一帧，而是只分析「高熵」帧——比如地形突变或新障碍物——从而提供更快、更切题的指导。

![跑步指导智能体架构图。流程图把输入感知（视频、音频、Pixel 10 Pro）映射到端上分析（分割）和多个智能体（Planner、Coach、Break），最终产出输出反馈（部分音频与语音指导）](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Architecture.width-1200.format-webp.webp)

## 多智能体框架

跑步指导智能体是一个协作式多智能体框架，旨在帮助 BLV 用户实现跑步体验：

- **Planner 智能体：** 利用 Gemma 4 的函数调用能力，这个智能体获取天气和 Google Maps 数据，与跑者对话确定训练目标，并校准他们的数字起跑线。
- **Coach 智能体：** 在跑步过程中运行，以简明扼要的电报式语音提醒进行提示。它把反馈按严格的层级分类：DANGER（危险，需立即规避）、WARNING（警告，附近有跑者或障碍物）和 NOTICE（提示，前方赛道弯道）。
- **Break 智能体：** 管理休息间隔，让运动员可以随时暂停并恢复训练。

## 智能眼镜与社区合作

虽然胸挂式 Pixel 10 Pro 已是一个坚实的基础，但我们正在智能眼镜上对跑步指导智能体进行原型开发。可穿戴眼镜提供更宽、更稳定的视野，能大幅优化输入多模态模型的数据。眼镜直接向 Pixel 设备串流，把硬件与环境 AI 无缝融合。

通过智能眼镜看到的跑者视角

为了确保我们是与社区并肩构建，我们与新加坡残障与融合事务主管机构 [SG Enable](https://www.sgenable.sg/about-us/our-story) 建立了合作。通过让我们的工程团队与 BLV 跑者直接对接、开展真实世界测试，我们得以迭代设计一款真正满足他们需求的工具。

跑步指导智能体是 Google AI 智能体新篇章的一次有力展示。运动员们将能够使用这款结合零时延边缘计算与深层世界理解的工具，突破自身极限，以完全独立、毫无依赖的自信穿行于世界。
