---
title: "对话 Facebook AI 驻留学者 Tatiana Likhomanenko 与 Siddharth Karamcheti"
title_en: "Q&A with Facebook AI residents Tatiana Likhomanenko and Siddharth Karamcheti"
date: 2019-03-15
source: https://ai.facebook.com/blog/qa-with-facebook-ai-residents-tatiana-likhomanenko-and-siddharth-karamcheti
crawled: 2026-09-22
translated: 2026-09-22
---

# 对话 Facebook AI 驻留学者 Tatiana Likhomanenko 与 Siddharth Karamcheti

> 原文：[Q&A with Facebook AI residents Tatiana Likhomanenko and Siddharth Karamcheti](https://ai.facebook.com/blog/qa-with-facebook-ai-residents-tatiana-likhomanenko-and-siddharth-karamcheti) · Meta AI（Wayback 存档）

2019 年 3 月 15 日

Facebook 的人工智能（AI）驻留计划（AI Residency Program）是一项为期一年的全职研究培训机会，旨在让参与者在 Facebook AI 内部工作期间获得机器学习研究的实战产业经验。该计划提供了与 Facebook 研究员和工程师结对、就共同感兴趣的研究问题展开协作的独特机会，并设计新的深度学习技术来解决这些问题——这些技术往往能应对现实世界的挑战。我们最近与该计划的两位现任驻留学者 Tatiana Likhomanenko 和 Siddharth Karamcheti 聊了聊，进一步了解他们。

Tatiana 于 2018 年 9 月加入 Facebook，在加州门洛帕克担任 AI 驻留学者，在 Facebook AI 研究院（FAIR，Meta 基础人工智能研究院）语音团队与 Ronan Collobert 和 Gabriel Synnaeve 共事。她拥有莫斯科国立罗蒙诺索夫大学（MSU）计算机科学硕士学位，并毕业于 Yandex 数据分析学校。她在 Yandex（一家俄罗斯搜索引擎公司）与 CERN 的联合科学实验室担任研究员四年，从事机器学习在高能物理中的应用。2017 年，她在 MSU 计算机科学系答辩获得了混合型偏微分方程方向的博士学位。Siddharth 在罗德岛州布朗大学读本科，同时修读计算机科学与文学艺术（创意写作——小说）两个方向。「因为热爱计算机科学又热爱语言/文学，我大学头几年一直在寻找融合两者的途径，自然语言处理（NLP）就是我的入口。」他解释道。Siddharth 是驻纽约的 AI 驻留学者，与 Rob Fergus、Jason Weston、Dhruv Batra、Douwe Kiela 和 Arthur Szlam 合作。

以下是我们与二人的问答。

**问：你们目前的研究兴趣是什么？**

**Tatiana：** 我的研究兴趣是语音合成、视频识别、泛函分析、高能物理和天体物理。博士期间我研究了用混合型偏微分方程描述的亚音速与超音速过程的模型方程，通过构造此类问题本征函数的闭式解。这项研究的主要成果属于泛函分析，例如所构造本征函数的 Riesz 基性质。我从小就热爱数学和物理，充满热情地学习量子力学和微分几何，想弄明白宇宙如何运转。在 CERN 参与研究让我理解了我们如何研究宇宙。

**Siddharth：** 我的目标是构建能有效与人类沟通、并在不同环境中安全行事的智能体。我也对语言在确保安全、可解释行为方面的作用感兴趣。在指令式场景中使用时，语言为行动提供了有意义的约束——有时指定要达成的具体目标，有时则明确规定任务应如何完成。我非常感兴趣的是如何对「语言到行为」的映射进行推理，以便保证或验证智能体确实在按照语言指令行事（而不是只遵循其中一部分，或干脆无视它）。驻留年结束后，我将进入斯坦福大学攻读计算机科学博士，希望继续机器学习和自然语言处理方向的工作。

**问：你们目前在做些什么？**

**Tatiana：** 借助 AI 驻留计划，我有机会加入一个对我而言全新的领域的研究：自动语音识别（ASR）系统。如今，大多数最先进的 ASR 系统使用大词表，只能识别词表内的词。构建能识别词表之外单词的 ASR 系统是我目前的主要研究重点。另一个重点是：当有大量文本和声学数据但转录文本有限时，用无监督学习改进 ASR 系统。学习这类表示对低资源语言的语音识别非常有用。

**Siddharth：** 我的主要项目聚焦于在强化学习场景中利用语言辅助高效泛化。作为动机，设想一个负责帮忙处理各种日常家务的家庭机器人——比如早上煮咖啡或茶、打扫卫生、倒垃圾。这些家务虽然千差万别，但每个任务都可拆解为简单组件（如打开橱柜、打开开关），而不同组件会出现在多个不同任务中。除了帮助简化行为，我们还可以把这些小组件以新方式组合，去完成全新任务。这带来了高效的跨任务泛化：与其从头教机器人执行新任务（可能耗时巨大），我们只需教它如何组合已学会的组件（效率高得多）。虽然这项工作仍在进行中，但核心思路是通过观察教师如何用语言教学生新技能，来学习如何把任务拆解为这些组件。我们的初步研究表明，在此类场景中，教师会把高级任务拆解为大致对应各个简单组件的小块语言指令。我们希望通过学习如何把高级任务分解为所需的语言指令，让智能体以高效且稳健的方式习得新行为。

**问：为什么选择 Facebook 的计划？**

**Tatiana：** 我选择到 Facebook 做驻留学者，是因为开放和分享新想法的价值观是 Facebook 文化的主要组成部分之一，这对高效研究非常有利。我喜欢在 FAIR 参与 AI 驻留计划，因为这里的研究不仅有趣，还能立即应用于现实生活。例如，语音识别和机器翻译方面的研究意味着能够以任何语言准确转录音频和视频。打破语言障碍、改善信息无障碍，能让我们与听障人士和世界各地的其他语言使用者分享我们的知识、梦想和经历。

**Siddharth：** 是这里的人。有那么多极具才华的研究员在做我关心的问题——接地（grounding）、基于语言的交互、强化学习、涌现交流……不胜枚举。而且我觉得，与我合作的研究员们会教我大量新技能，让我了解到人们正在研究的极其宽广的问题空间——这正是我在博士阶段聚焦单一领域之前真正想要的。

想进一步了解如何成为 Facebook 的 AI 驻留学者，请访问 AI 驻留计划页面。
