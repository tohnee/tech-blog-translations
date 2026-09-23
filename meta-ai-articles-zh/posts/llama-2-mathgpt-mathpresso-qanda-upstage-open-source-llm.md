---
title: "MathGPT：利用 Llama 2 打造高度个性化学习平台"
title_en: "MathGPT: Leveraging Llama 2 to create a platform for highly personalized learning"
date: 2024-04-15
source: https://ai.meta.com/blog/llama-2-mathgpt-mathpresso-qanda-upstage-open-source-llm
crawled: 2026-09-22
translated: 2026-09-22
---

# MathGPT：利用 Llama 2 打造高度个性化学习平台

> 原文：[MathGPT: Leveraging Llama 2 to create a platform for highly personalized learning](https://ai.meta.com/blog/llama-2-mathgpt-mathpresso-qanda-upstage-open-source-llm) · Meta AI（Wayback 存档）

AI 的突破有望造福全球社区——前提是更多人拥有利用它们的教育与渠道。由于 STEM 教育仍是经济流动性与创新的关键因素，Mathpresso 正通过其学习平台 QANDA 贡献力量，让 50 个国家的人都能获取个性化学习内容。当这家总部位于首尔的公司与韩国领先 AI 初创公司 Upstage 合作，打造一个高精度数学专用 LLM 时，Meta 的开源模型 Llama 2 成了合适之选。「我们的主攻方向一直是数学，」Mathpresso 联合创始人 Jake Yongjae Lee 说。他补充道，QANDA 最适合那些通常以结构化课程教授的科目，如讲授与习题集。然而他说：「ChatGPT 这类商业 LLM 缺乏复杂教育场景所需的定制能力。」据 Lee 介绍，学生的学习受超本地化因素影响，包括课程大纲、学区、考试趋势、教学风格等等。穿越这层复杂性，Llama 2 正帮助 Mathpresso 构想一个人人都能获得优质教育的世界。有了 Llama 2 这样的开源模型，团队既能创建灵活的领域专用教育产品，又能充分利用自己独有的专业数据与技术。成果就是 MathGPT——一个以 Llama 2 为基座、拥有强大而精准数学能力的 LLM。Upstage 负责模型的引擎与微调，Mathpresso 与 QANDA 则为模型学习提供专业数学数据。今年早些时候，MathGPT 在评估中小学数学水平的基准上刷新了世界纪录。

## 用 MathGPT 帮学生深化数学理解

Mathpresso 从训练较小模型起步，逐步过渡到更大模型来测试其数学表现。在此过程中，团队用大模型生成的数据训练其他模型，发现应用于小模型的方法论在大模型上同样有效。如今，团队正基于 QANDA 自有的数学数据，用 Llama 2 构建微调模型，并通过监督微调与数据增强生成训练数据。MathGPT 的与众不同之处在于，它着力培养学生对解题过程的理解，而不是仅仅给出数学题的答案。因此，它提供的详细讲解还会拆解为分步流程，帮助培育比一般讲解更深层次的理解。Mathpresso 团队用从 QANDA 平台收集的数据做全量微调。由于这些数据通常以「题目-解答」对的形式存在，训练过程就是向模型呈现问题、训练其生成正确答案。这些数据为 QANDA 专有，因此团队断定，开源模型优于闭源或托管模型——因为它让他们能掌控自己的数据。Mathpresso 需要一个在解读数学表达式方面能力出众的模型。为此，团队选择性地融入了专门针对数学表达式的数据，强化了 Llama 2 的 laTeX 文档准备系统表达式能力。

## 在 Open LLM 排行榜上胜出

对 Upstage 而言，Llama 之旅始于对一种多功能语言模型的追求——既要在英语及韩语等其他语言上出类拔萃，又能无缝适配各种公司需求。为衡量进展，它瞄准了 HuggingFace Open LLM 排行榜的头名，目标是超越 GPT-3.5 的基准分数。在考虑过基于 BERT 的模型之后，Upstage 发现一些学术论文表明 Llama 2 提供了更高的基准性能。「要在 Open LLM 排行榜上打造一个冠军语言模型，我们需要一个强有力的起点——Llama 2 应运而来，」Upstage CEO Sung Kim 说，「作为开源 LLM 世界里的顶尖选手与首选，Llama 2 是我们项目的完美基座。」该公司首先用 Llama 2 微调以参加排行榜竞争，即调整现有模型在该基准上表现出色。其 Llama2-70b 模型成功登上第一，使 Upstage 成为全球首家在 Open LLM 排行榜上超越 GPT-3.5 的公司。随后，Upstage 利用更小的 Llama2-7b 研究韩语支持并开发自己的基础模型，借此探索韩语能力并构建定制基座模型。由于 Llama 2 架构在开源库中获得广泛支持，该公司将其采纳为默认架构。此后，公司与 Mathpresso 的合作（属于与电信巨头 KT 战略合作的一部分）造就了 MathGPT 的纪录。Upstage 还开发了自己的首个预训练 LLM——SOLAR-10.7B（Specialized and Optimized LLM and Applications with Reliability 的缩写），去年 12 月同样登顶 Open LLM 排行榜。与动辄数千亿参数的大模型相比，Solar 是一个参数不到 200 亿的轻量模型。由于训练数据集更小，该模型的推理成本更低、速度约为 GPT-3.5 的 2.5 倍。「如果 Llama 2 没有以开源形式发布，我们不可能实现这样的快速崛起，」Kim 说，「我们的故事正是开源之力对于生成式 AI 新星的最好例证。」

## Llama 2 开源对教育的现实影响

对 Mathpresso 而言，通过 AI 导师让每个人都能享受 1:1 个性化教育是长期目标。「通过 QANDA 平台，我们得以细致地收集并数字化每个学生学习路径与需求的独有数据，」Lee 说，「借助 Llama 2 这样的开源模型，我们能灵活地打造经济实惠的教育工具，利用我们独有的洞察，帮助全世界的学生充分发挥潜能。」Mathpresso 与 Upstage 都相信，Llama 2 这样的开源模型能深刻影响大大小小的公司。「获取前沿的开源工具与库可以拉平竞争场，」Kim 说，「让组织得以利用原本可能遥不可及的先进技术与方法论。」

分享你的 Llama 故事
