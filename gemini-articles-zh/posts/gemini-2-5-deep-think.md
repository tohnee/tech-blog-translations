---
title: "在 Gemini 应用中体验 Deep Think"
title_en: "Try Deep Think in the Gemini app"
source: https://blog.google/products-and-platforms/products/gemini/gemini-2-5-deep-think/
site: gemini
date: 2025-08-01
crawled: 2026-09-13
translated: 2026-09-13
---

# 在 Gemini 应用中体验 Deep Think

> 原文：[Try Deep Think in the Gemini app](https://blog.google/products-and-platforms/products/gemini/gemini-2-5-deep-think/) · Google

今天，我们在 [Gemini 应用](https://gemini.google/)中向 [Google AI Ultra 订阅用户](https://one.google.com/about/google-ai-plans/)开放 Deep Think——这是专为该订阅用户独家提供的、能力极强的一系列 AI 工具与功能中的最新一员。

此次新版本吸纳了早期可信测试者的反馈与研究突破。无论是关键基准的提升，还是可信测试者的反馈，都表明它相比在 [I/O 上首次发布](https://blog.google/technology/google-deepmind/google-gemini-updates-io-2025/#deep-think)的版本有了显著改进。它是[不久前在今年国际数学奥林匹克竞赛（IMO）上达到金牌水准](https://deepmind.google/discover/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/)的模型的一个变体。那个模型需要耗费数小时来推理复杂的数学问题，而今天的版本速度更快、日常可用性更强，同时根据内部评估，在 2025 年 IMO 基准上仍能达到铜牌水平的成绩。

Deep Think 可以成为创造性解决问题的强大工具：

在我们把 Deep Think 交到 Google AI Ultra 订阅用户手中的同时，我们也在向一小群数学家和学者分享[达到金牌水准](https://deepmind.google/discover/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/)的 Gemini 2.5 Deep Think 模型官方版本。我们期待听到它如何助力他们的研究探索，并将利用他们的反馈持续改进这项服务。

此次发布代表我们在构建更有帮助、更强大 AI 的使命上迈出的重要一步，也进一步践行了我们以 Gemini 推动人类知识前沿的承诺。

## Deep Think 的运作方式：延长 Gemini 的并行"思考时间"

正如人们会花时间从不同角度探索复杂问题、权衡各种可能的解法、再打磨出最终答案，Deep Think 通过并行思考（parallel thinking）技术拓展了思考能力的前沿。这一方法让 Gemini 同时生成大量想法并同步加以考量，甚至随着时间推移不断修订或组合不同的想法，最终得出最佳答案。

此外，通过延长推理时间或"思考时间"，我们让 Gemini 有更多时间去探索不同的假设，为复杂问题找到富有创造性的解法。

我们还开发了新颖的强化学习技术，鼓励模型充分利用这些更长的推理路径，从而让 Deep Think 随时间推移成为更出色、更直觉化的问题解决者。

## Deep Think 的表现：最先进的性能

Deep Think 可以帮助人们解决需要创造力、战略规划和逐步改进的问题，例如：

- **迭代式开发与设计：** Deep Think 在需要逐块构建复杂成果的任务上的表现令我们印象深刻。例如，我们观察到 Deep Think 能够同时提升 Web 开发任务的美观度与功能性。

Gemini 应用中的 Deep Think 运用并行思考技术，给出更细致、更有创意、更深思熟虑的回答。

![三幅 AI 生成的体素（voxel）艺术场景对比图。每张图片都展示了花园中一座带树木和樱花的宝塔，从左到右细节和复杂度逐级提升。图片分别标注为"Gemini 2.5 Flash"、"Gemini 2.5 Pro"和"Gemini 2.5 Deep Think"。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/2-5-deep-think_blog-image_pagoda.width-1200.format-webp.webp)

- **科学与数学发现：** 由于能够推理高度复杂的问题，Deep Think 可以成为研究人员的有力工具。它可以帮助提出并探索数学猜想，或梳理复杂的科学文献，有望加速通往发现的路径。
- **算法开发与代码：** Deep Think 尤其擅长[高难度编程问题](https://x.com/GoogleDeepMind/status/1925676461651791992)——这类问题中，问题的形式化定义以及对权衡取舍与时间复杂度的仔细考量至关重要。

Deep Think 的实力也体现在衡量编程、科学、知识与推理能力的高难度基准测试中。例如，与不使用工具的其他模型相比，Gemini 2.5 Deep Think 在 LiveCodeBench V6（衡量竞赛级编程表现）和 Humanity's Last Exam（一项衡量包括科学和数学在内多领域专业水平的高难度基准）上均取得了最先进的成绩。

![四张柱状图组成的图表，对比各 AI 模型的性能。Gemini 2.5 在推理、代码和数学基准上领先 Gemini 2.5 Pro、OpenAI o3 和 Grok 4。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/all_benchmarks_blog.width-1200.format-webp.webp)

## 我们如何负责任地推进 Gemini

在训练和部署的整个生命周期中，我们持续为 Gemini 注入安全性与责任感。测试显示，Gemini 2.5 Deep Think 在内容安全性和语气客观性方面优于 Gemini 2.5 Pro，但拒绝良性请求的倾向也更高。

随着 Gemini 问题解决能力的提升，我们也更加深入地审视复杂度增加所带来的风险，包括开展前沿安全评估，以及针对关键能力等级（CCL）落实既定的缓解措施。

有关 Gemini 2.5 Deep Think 安全结果的更多细节，请参阅[模型卡](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-2-5-Deep-Think-Model-Card.pdf)。

## 今天如何在 Gemini 应用中使用 Deep Think

如果你是 Google AI Ultra 订阅用户，今天就可以在 Gemini 应用中使用 Deep Think：在模型下拉菜单中选择 2.5 Pro 后，在提示词输入栏切换打开"Deep Think"即可，每天有固定的使用次数。Deep Think 会自动配合代码执行和 Google 搜索等工具，并能生成篇幅长得多的回答。

未来几周，我们还将通过 Gemini API 向一组可信测试者发布带工具和不带工具的 Deep Think 版本，以便更好地了解它在开发者和企业用例中的可用性。

从研究到部署，几乎每一层的团队都为让 Deep Think 对 Gemini 应用用户更快、更可靠、更易用付出了努力。我们迫不及待想看到你用它创造出什么。
