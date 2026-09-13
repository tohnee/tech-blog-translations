---
title: "GLM-5.3-Flash 架构笔记"
title_en: "GLM-5.3-Flash Architecture Notes"
source: https://sebastianraschka.com/blog/2026/glm-5-3-flash-architecture-notes.html
crawled: 2026-09-06
translated: 2026-09-06
---

# GLM-5.3-Flash 架构笔记

> 原文：[GLM-5.3-Flash Architecture Notes](https://sebastianraschka.com/blog/2026/glm-5-3-flash-architecture-notes.html)

现在真相大白了：广受欢迎的 Ox Alpha LLM 就是 GLM-5.3-Flash……

与 GLM-5.2 相比，这个新的 GLM-5.3-Flash 模型使用了：

- Kimi Linear 风格的 3:1（super\*）混合注意力模式，包含 34 个 Kimi Delta Attention 层（KDA）和 11 个多头潜在注意力（MLA）/ DeepSeek 稀疏注意力（DSA）层；
- 缩小版的 GLM-5.2 风格稀疏 MoE 骨干，从 744B-A40B 降至 320B-A18B；
- DeepSeek V4 风格的 mHC 残差路径，带四条并行流；
- 外加一个原生视觉编码器（图中未显示）。

我之所以在上面称它为"超级混合"，是因为 KDA 和 MLA/DSA 都是"高效"组件。例如，Kimi 只用 KDA + 完整注意力 MLA，DeepSeek V3.2 用的是 DSA + 完整注意力 MLA。

附言：这么多技术术语，抱歉了。所有这些组件（MLA、DSA、KDA、mHC 等）的讲解都在我的 [LLM Architecture Gallery](https://sebastianraschka.com/llm-architecture-gallery/) 里。

再附言：哈哈，这也许算是给自己买那台昂贵的 Mac Studio M5 Ultra 256 GB / 512 GB 来本地运行这个模型找了个理由……

![组合图：展示 GLM-5.3-Flash 架构，包括 Kimi Delta Attention、带 DeepSeek 稀疏注意力的多头潜在注意力、mHC 残差流，以及基准测试对比](https://sebastianraschka.com/images/blog/2026/glm-5-3-flash-architecture-notes/glm-5-3-flash.webp)

图 1. GLM-5.3-Flash 架构与发布时基准测试对比。更多细节请见架构图库中的 [GLM-5.3-Flash](https://sebastianraschka.com/llm-architecture-gallery/#card-glm-5-3-flash)。

来源：我的 [Substack note](https://substack.com/@rasbt/note/c-323088504) 的网页版。
