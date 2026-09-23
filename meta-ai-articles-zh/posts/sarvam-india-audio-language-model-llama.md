---
title: "借助 Llama 打造印度首个开源音频语言模型"
title_en: "Enlisting Llama in India’s first open source audio language model"
date: 2025-02-05
source: https://ai.meta.com/blog/sarvam-india-audio-language-model-llama
crawled: 2026-09-22
translated: 2026-09-22
---

# 借助 Llama 打造印度首个开源音频语言模型

> 原文：[Enlisting Llama in India’s first open source audio language model](https://ai.meta.com/blog/sarvam-india-audio-language-model-llama) · Meta AI（Wayback 存档）

2025 年 2 月 5 日 · 阅读时长约 5 分钟

Sarvam AI 的创立愿景，是通过构建全栈生成式 AI 方案赋能印度民众，改变全国超过十亿人与技术互动的方式。该公司使用 Llama 开发了推理能力更强、精通 10 种印度语言的企业语音 AI 智能体。

Sarvam 借助 Llama 开发了 Shuka v1——印度首个开源音频语言模型。Llama 在 Shuka 中担任解码器，处理由 Sarvam 音频编码器生成的音频 token。这些 token 捕捉音频输入中的语音学和语言学细节，由 Llama 解码为基于文本的回应。这一设置让 Shuka 能够准确高效地理解并回应印度语言的语音查询。

「Llama 对于确保 Shuka 的回应在语境上相关、语言上准确至关重要——即使在古吉拉特语、印地语、卡纳达语和马拉地语这些语音模型稀缺的语言中也是如此。」Sarvam AI 联合创始人 Pratyush Kumar 博士说，「在印度这样的国家，用户在某些应用中更喜欢用语音而非文字交互，开发语音优先的应用至关重要。」

Shuka 为区域语言的语音优先 AI 提供了可行路径，是多语言音频理解的突破。企业可以通过易用的语音交互，用古吉拉特语、印地语、卡纳达语、马拉地语和其他印度语言更轻松地与客户沟通。「因为该模型能原生解码多种语言的音频，它为教育和客户支持等对话式 AI 应用开辟了新的可能。」Kumar 说，「而且因为 Shuka 是开源的，政府部门和受监管行业可以把它部署在自己的场所内使用，不必担心敏感数据被分享给任何第三方。」

## 以可负担的方式解码语言

Sarvam 团队为 v1 模型选择了 Llama 3 的 8B-Instruct 版本，因为它在计算效率与准确性之间取得了平衡，非常适合在低资源环境下解码印度语言。团队最初对 Llama 的兴趣源于其在文本任务上的表现。他们探索把该模型与 Sarvam 面向印度语言的定制音频编码器结合、适配其解码音频输入——Llama 模型并未在印度语言音频上受过大量训练。目标是将 Llama 的能力从纯文本模型扩展为能理解印度语言语音的多模态方案。当 Llama 在音频应用上的潜力显现后，团队迅速执行了计划。通过把 Llama 与 Sarvam 的 Saaras v1 编码器以及一个 6000 万参数的定制投影层相结合，团队扩展了 Llama 处理音频输入的能力。

## 训练投影层以弥合差距

为了让 Llama 有效处理音频输入，团队训练了一个约 6000 万参数的投影层，弥合 Sarvam 音频编码器生成的音频表示与 Llama 文本嵌入之间的差距。投影层使音频数据能无缝变换为 Llama 可解释为文本的格式。由于训练资源有限，团队采取了节俭策略：只微调投影层，冻结 Llama 和 Saaras 的其余部分——这一策略把资源占用降到最低。「如果 Llama 没有以开源软件的形式提供，做出 Shuka 需要付出大得多的代价。」Kumar 说，「我们得以专注于音频编码器和投影层的创新，高效构建出一个最先进的音频-文本模型。」

微调涉及在涵盖印度语言的数据集上训练投影层，重点是创建与 Llama 嵌入空间兼容的音频 token。这一方法需要针对 Sarvam 的问答数据集生成高质量问答对，随后经 Llama 3 处理产生金标准答案。通过对投影层的精心微调，Shuka v1 在准确性与效率之间取得了平衡，无需重训整个 Llama 模型即可保持语言回应的准确性。随着 Llama 持续演进，Sarvam 计划利用更新的版本扩展 Shuka 的能力，有望支持更广泛的语言和更大的训练数据集。
