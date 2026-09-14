---
title: "直接偏好优化（DPO）与监督微调"
title_en: "Direct Preference Optimization vs. Supervised Finetuning"
source: https://sebastianraschka.com/faq/docs/dpo-vs-supervised-finetuning.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 直接偏好优化（DPO）与监督微调

> 原文：[Direct Preference Optimization vs. Supervised Finetuning](https://sebastianraschka.com/faq/docs/dpo-vs-supervised-finetuning.html) · Sebastian Raschka's FAQ

**监督微调（SFT）**与**直接偏好优化（Direct Preference Optimization，DPO）**的区别在于它们所使用的训练样本，以及各自损失函数所优化的概率关系。

两种方法都使用带标签的数据和梯度下降。在本文的比较中，*监督微调*指的是基于示范数据的常规 SFT，而不是在暗示 DPO 是无监督的。

对 SFT 来说，一条记录包含一个提示（prompt）和一个目标响应。训练会提高该响应在 token 级别上的似然。例如，如果提示要求对梯度下降做一段简短解释，那么目标就向模型展示它应该学会复现的那个特定答案。

DPO 使用针对同一提示的两个响应。一个被标记为**被选中（chosen）**，另一个被标记为**被拒绝（rejected）**。标签表达的是这一对响应之间的偏好。它们并不要求被选中的响应是唯一正确的答案。

DPO 训练期间，模型会比较被选中和被拒绝响应的序列对数概率。它学习扩大有利于被选中响应的差距。一个冻结的参考模型（通常是 DPO 开始前该模型的副本）提供锚点，使更新后的策略不会从其初始行为自由漂移。

![DPO 的出发点是：多个响应可能都有效，但其中一些比另一些更受偏好](https://sebastianraschka.com/images/LLMs-from-scratch-images/dpo/2.webp)

这种设定在多个响应都合理、而差异关乎质量时非常有用。一个答案可能更贴合所要求的格式，把某一步解释得更清楚，或者避免了没有依据的论断。SFT 可以从一条精心打磨的示范中学习。DPO 还会额外学习在给定的一对响应中，是什么特征让其中一个比另一个更可取。

常见的训练顺序是：基础模型预训练，随后 SFT，然后 DPO。SFT 先让模型获得一个合理的指令遵循策略；DPO 再对模型已经能够生成的响应之间的相对偏好进行调整。这一顺序是通行做法，而非 DPO 损失函数的硬性要求。

与经典的 RLHF 流水线相比，DPO 去掉了两大块机制。它既不必拟合一个单独的奖励模型再用强化学习算法去优化语言模型，而是把偏好目标通过普通的基于梯度的训练直接施加在语言模型上。

![仓库中的 DPO 概览强调直接从偏好对进行优化，而非完整的 RLHF 流水线](https://sebastianraschka.com/images/LLMs-from-scratch-images/dpo/5.webp)

偏好标签需要仔细解读。如果被选中的答案只是两个孱弱候选中较好的那个，它本身仍可能存在问题。对冗长、特定措辞或单一响应格式的反复偏好，也可能被学得比预期更强。因此，配对的构造与审查和优化方法本身同样重要。

仓库中第 7 章的 DPO notebook 使用了较小的学习率和适度的训练时长。这些保守的设置是合理的，因为过于激进的偏好优化会损害整体的响应质量。在实践中，我会用 SFT 建立所需的任务行为，当「选中 vs 拒绝」的对比能提供单一目标响应无法直接传达的信息时，再加入 DPO。
