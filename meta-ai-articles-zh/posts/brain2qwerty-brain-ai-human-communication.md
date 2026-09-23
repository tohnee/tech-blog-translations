---
title: "从脑波到文字：Brain2Qwerty 开辟无需手术的交流新路径"
title_en: "From Brain Waves to Words: Brain2Qwerty Offers a New Path to Communication Without Surgery"
date: 2026-06-29
source: https://ai.meta.com/blog/brain2qwerty-brain-ai-human-communication
crawled: 2026-09-22
translated: 2026-09-22
---

# 从脑波到文字：Brain2Qwerty 开辟无需手术的交流新路径

> 原文：[From Brain Waves to Words: Brain2Qwerty Offers a New Path to Communication Without Surgery](https://ai.meta.com/blog/brain2qwerty-brain-ai-human-communication) · Meta AI（Wayback 存档）

去年，我们发布了 Brain2Qwerty v1——一项用 AI 将大脑活动解码为文字且无需任何外科植入的研究。现在，我们分享它的下一步：Brain2Qwerty v2，这是性能最高的端到端流水线，能够从非侵入式脑记录中进行实时句子解码，准确率正在逼近此前唯有依赖脑部手术的技术才能达到的水平。

为了帮助加速神经科学突破，我们发布了 Brain2Qwerty v1 与 v2 的完整训练代码，我们的合作伙伴——巴斯克认知、大脑与语言中心（BCBL）——也发布了 v1 数据集。我们相信，这项研究有可能为数百万因脑部病变而无法交流的人带来真实的改变。

立体定向脑电图和皮层脑电图等侵入式手段已经证明，向 AI 解码器馈送信号的神经假体可以恢复交流，但它们难以规模化。我们的非侵入式方法可以帮助弥合这一差距。

我们在九名志愿参与者的大约 22000 个句子上训练 Brain2Qwerty v2，每名参与者在主动打字时佩戴脑磁图（MEG）设备记录 10 个小时。我们不依赖手工设计的流水线来检测神经事件，而是使用端到端深度学习直接从原始脑信号进行解码。在神经数据上微调大语言模型，使系统能够利用语义上下文，弥合嘈杂脑记录与连贯语言之间的鸿沟。我们还部署了 AI 智能体（agentic）来探索解码流水线的优化方案，最终训练配置由工程师人工选定。

结果：Brain2Qwerty v2 能够从嘈杂的神经输入中连贯地恢复句子，词准确率达到 61%，显著优于其他非侵入式方法 8% 的词准确率。对于我们表现最好的参与者，我们达到了 78% 的词准确率，超过一半的句子解码后只有一个词以内的错误。我们还发现，解码准确率随数据量呈对数线性提升，这表明与手术方法之间剩余的性能差距，仅靠扩大数据规模就有望进一步缩小。

这项工作有助于我们构建大脑的开放基础模型：包括用于感知编码的 Tribev2 模型、用于大规模处理大脑数据的 NeuralSet，以及用于系统评估模型的 NeuralBench。我们通过与社区的紧密合作来完成这些工作，包括近期在「数字大脑项目」（Digital Brain Project）中投入 500 万美元基金以刺激开放数据集的建设。

我们希望这项公开进行的工作能够推动神经科学更快地识别、诊断和治疗神经系统疾病，而不是在各自为战中发现。

阅读 Brain2Qwerty v2 论文 · 下载代码 · 下载数据 · 阅读 Brain2Qwerty v1 博文 · 阅读 Nature Neuroscience 上关于 Brain2Qwerty 的文章
