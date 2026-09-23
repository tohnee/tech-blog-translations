---
title: "用 AI 扩大欠发达社群的医疗服务可及性"
title_en: "Extending healthcare access to underserved communities with AI"
date: 2024-12-02
source: https://ai.meta.com/blog/bimedix-built-with-llama
crawled: 2026-09-22
translated: 2026-09-22
---

# 用 AI 扩大欠发达社群的医疗服务可及性

> 原文：[Extending healthcare access to underserved communities with AI](https://ai.meta.com/blog/bimedix-built-with-llama) · Meta AI（Wayback 存档）

2024 年 12 月 2 日 · 阅读约 5 分钟

BiMediX2 是一个阿拉伯语—英语医疗大多模态模型，其团队能够解读医学图像并支持远程医疗平台上的双语交互，目标是扩大非洲和中东地区的医疗服务可及性。阿布扎比穆罕默德·本·扎耶德人工智能大学（MBZUAI）的研究者对 Llama 3.1 进行微调，产出了 BiMediX2——它能解读 X 光、CT、MRI 等医学图像。团队还把它作为聊天机器人集成到了消息平台 Telegram 上。BiMediX2 近期获得了首届 Llama Impact 创新奖，并在今年的迪拜 GITEX 和第 79 届联合国大会（UNGA79）上展示，因其远程医疗应用的潜力受到联合国关注。

「凭借阿拉伯语—英语双语交互，我们的模型把医疗服务延伸到超过 4 亿阿拉伯语使用者，是一个包容而全面的医疗解决方案。」MBZUAI 的 Hisham Cholakkal 教授说，「我们相信它是首个基于 Llama 3.1 构建的医疗大多模态模型。」

## 自诞生起就基于 Llama 构建

MBZUAI 是一所研究生层次、以研究为基础的 AI 大学，参与过其他有影响力的基础模型（如 Vicuna 和 Jais）的开发，也参与 LLM360 和 MobiLlama 等旨在创建完全透明 LLM 的项目。该团队开发了多个开源模型，包括多语言视觉—语言模型 PALO、接地（grounding）大多模态模型 GlaMM、阿拉伯语 Mini-Climate GPT 等气候专用 LLM，以及面向大多模态模型的综合评测基准，例如评估模型在 100 种不同语言与文化下表现的 All Languages Matter。团队从早期 Llama 模型发布起就接触并采纳了其各个新版本，原因是其开源可用性和强大的社区支持。「现在，我们正在推进它们的应用：把基于 Llama 的模型专门适配到医疗领域，并支持包括医学图像分析在内的多模态交互。」Cholakkal 博士说。在另一个进行中的项目里，他们还在为 Llama 集成视觉与语音能力。

团队为 BiMediX2 精修了 Llama：使用半自动化流水线（借助 Llama3-70B 和 GPT-3.5）生成高质量的阿拉伯语—英语医疗指令集，再对有限子集进行人工核验。对于 BiMediX2 模型的视觉部分，他们整理了覆盖多种医学影像形式的更大数据集的图文对。Cholakkal 博士表示，这一过程让 BiMediX2 在纯文本和视觉—语言两类医疗任务上都表现出色，使其成为适合欠发达社群医疗应用的强大工具。

## 借开源加速进展

公开可得的代码和开源社区的支持，帮助团队克服了基于 Llama 3.1 构建视觉能力（VLM）时的挑战，尤其是新的 rope-scaling 和旋转嵌入（rotary embeddings）框架。「我们的团队从开源方式中受益匪浅，」Cholakkal 博士说，「开源社区在克服 rope-scaling 和旋转嵌入难题上的贡献至关重要。这种协作环境加速了我们的进展，使我们能够构建一个稳健的双语医疗模型。」

他指出，能获取 Llama 这样的开放权重模型，让组织可以把这些模型适配到医疗等特定领域，而无需投入大量资源从零训练像 Llama 3.1 这样强大的模型。随着 Llama 生态的演进，MBZUAI 的研究者预期将扩大对 Llama 模型的使用。未来的迭代可能会增强处理更复杂医疗数据的能力、集成更多语言和模态，并提升模型整体性能。「我们计划利用这些进展进一步打磨 BiMediX2，通过应对新兴医疗需求来扩大其影响。」Cholakkal 博士说。

我们谨此感谢以下 MBZUAI 师生对 BiMediX2 项目的贡献：Sahal Shaji Mullappilly（第一作者）、Mohammed Irfan K（共同第一作者）、Sara Pieri、Fahad Shahbaz Khan、Rao Muhammad Anwer、Salman Khan、Timothy Baldwin 和 Hisham Cholakkal；阿联酋谢赫·沙赫布特医疗城（SSMC）的 Saeed Yahya Alseiari 博士；印度科泽科德政府医学院的 Shanavas Cholakkal；以及阿联酋塔瓦姆医院的 Khaled Aldahmani。

分享你的 Llama 故事
