---
title: "Claude 文本水印的工作原理"
title_en: "How Claude's Text Watermarking Works"
source: https://sebastianraschka.com/blog/2026/claude-text-watermarking.html
crawled: 2026-09-06
translated: 2026-09-06
---

# Claude 文本水印的工作原理

> 原文：[How Claude's Text Watermarking Works](https://sebastianraschka.com/blog/2026/claude-text-watermarking.html)

本文简要图解 Claude 的文本水印机制是如何工作的（基于我对[他们发布的材料](https://www.anthropic.com/news/claude-text-watermark)的阅读）。

一般来说，在生成 token 时，某些"下一个词"位置上可能存在多个高分 token。通常我们会采用 [top-k 或 top-p 采样](https://sebastianraschka.com/faq/docs/temperature-topk-topp-sampling.html)，因此得分最高的 token 会被最常选中（如果把采样重复多次），但其他 token 也可能被选中。

而有了水印之后，就存在一个密钥来影响我们选择哪个高分 token。（水印密钥 + 最近的 token 上下文 → 伪随机种子 → 候选 token 的伪随机分数 → 采样过程向分数有利的候选 token 倾斜。）

或者更具体地说，密钥和之前的 token（的一个窗口）会影响这里的随机性。现在，如果我们在很多 token 位置上重复这一过程，就形成了水印，因为它会构成一种统计上不太可能自然出现的模式（统计相关性）——这是由组合数学决定的。

![图示：密钥和前序 token 如何影响 token 采样，从而创建可统计检测的文本水印](https://sebastianraschka.com/images/blog/2026/claude-watermarking-explained/claude-watermarking.webp)

图 1. 有水印与无水印情况下 token 采样的示意图，随后是一个示例，展示重复的、依赖密钥的 token 选择如何产生可检测的模式。

关于 Claude 文本水印的更多信息，请看我下面的较长视频。幻灯片 PDF 可从这里获取：[Claude text watermarking slides](https://sebastianraschka.com/pdf/slides/2026-08-18-claude-watermarking.pdf) 和 [From Conventional LLMs to Reasoning Models to Agents slides](https://sebastianraschka.com/pdf/slides/2026-08-llms-to-reasoning-to-agents.pdf)。

当然，通过中等到重度的编辑和改写——用另一个不带水印的 LLM——这个水印是可以被去除的。但这可能会让文本质量变差，因为这需要在文本中做出多处改动来替换词语（由于我们不知道水印位置在哪里，一个好的去水印工具必须编辑很多位置）。

有一点让我感到困惑：他们基本是说，由于欧盟的法规，他们必须对所有用户都这样做。为什么？当然，法规确实存在，但这是一个推理时的技术，不需要重新训练或训练单独的模型，所以如果他们愿意的话，可以只对欧盟用户这样做？

**后记**：

有人向我指出：

> 关于为什么这不只适用于欧盟用户的问题，回答是：
>
> Anthropic 是一家服务提供者，因为它在欧盟市场提供 Claude（第 2 条），且其输出可能位于欧盟境内，所以受欧盟 AI 法案约束。这意味着遵守透明度法规（第 50 条）的义务在提供者身上。在生成时，Anthropic 无法知道输出最终会出现在哪里。合规的唯一可靠方式是在生成时就对文本做标记，并且在全球范围内统一执行，而不是按用户或地区进行区分。

我的反驳是：

> 不过总体而言，我觉得这条法规过于严格。比如，我想象这样一个场景：一家制药厂商不能为美国患者生产和提供某种药品，仅仅因为有人可能把它出口到尚未批准该药品的欧盟。也就是说，这种情况下难道不应该追究出口商的责任，而不是制造商吗？

来源：我的 [Substack note](https://substack.com/@rasbt/note/c-315339554) 的网页版。
