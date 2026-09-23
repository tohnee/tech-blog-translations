---
title: "构建为人们穿搭选择提供建议的 AI"
title_en: "Building AI to inform people's fashion choice"
date: 2019-03-15
source: https://ai.meta.com/blog/building-ai-to-inform-peoples-fashion-choice
crawled: 2026-09-22
translated: 2026-09-22
---

# 构建为人们穿搭选择提供建议的 AI

> 原文：[Building AI to inform people's fashion choice](https://ai.meta.com/blog/building-ai-to-inform-peoples-fashion-choice) · Meta AI（Wayback 存档）

**这项研究是什么：**一套 AI 系统，通过对个人穿搭提出简单改动使其更加时尚。我们的 Fashion++ 系统使用深度图像生成神经网络来识别服装，并就哪些该去掉、添加或替换给出建议。它还能推荐调整某件衣物的穿法，比如把衬衫下摆塞进裤子或挽起袖子。该领域此前的工作探索过推荐整套全新穿搭或识别相似服装的方法，而 Fashion++ 的目标是建议对现有穿搭做细微改动，让它更有型。

**工作原理：**Fashion++ 专注于最小化编辑，所建议的调整比买一整套新衣服更现实、更实用。该系统使用一个判别式时尚度分类器，它在数千张被判定为有型的公开穿搭图像上训练。这些图像充当时尚穿搭的真值（ground truth）样本；而不时尚的样本则通过把时尚样本中的服装替换成最不相似的对应项来自举（bootstrap）生成。分类器训练完成后，我们的系统会逐步调整穿搭使其更时尚。一个图像生成神经网络渲染调整后的新造型：用变分自编码器（variational auto-encoder）生成轮廓，再用条件生成对抗网络（cGAN）生成颜色与图案。该生成器学到的潜在编码还被进一步用于识别其库存中哪些服装最能实现这种风格。

配图展示了 Fashion++ 可以推荐的对穿搭的此类细微改动。实验表明，系统的推荐让图像更接近真值样本，人类评估者也认为 Fashion++ 的建议不仅时尚而且易于落实。

**为什么重要：**这项工作展示了更有用的 AI 辅助技术的潜力——建议微小、实用却能带来有意义影响的改动。我们自举不时尚样本的方法展示了 AI 系统即使没有耗费大量资源的人工标注也能学习。通过专注于易于实现的改动，Fashion++ 或许能催生帮助消费者轻松改造现有穿搭的应用。

Fashion++ 是 AI 在时尚这样一个有人可能认为过于创意化、主观化的领域中也能派上用场的例证。它不是去规定或重新定义什么是时尚，而是从示例中学习，以提供实用的时尚建议。这样的研究有朝一日可能让人们以新的方式创造和分享自己最喜欢的风格，甚至帮助时装设计师创造新造型。通过分享我们的工作，我们希望帮助研究社区中的其他人用 AI 应对美学与创意类挑战。

阅读完整论文：Fashion++: Minimal edits for outfit improvement
