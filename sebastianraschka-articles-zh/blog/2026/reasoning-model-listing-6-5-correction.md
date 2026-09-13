---
title: "推理模型一书清单 6.5 勘误"
title_en: "Reasoning Book Listing 6.5 Correction"
source: https://sebastianraschka.com/blog/2026/reasoning-model-listing-6-5-correction.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 推理模型一书清单 6.5 勘误

> 原文：[Reasoning Book Listing 6.5 Correction](https://sebastianraschka.com/blog/2026/reasoning-model-listing-6-5-correction.html)

感谢大家的支持和反馈。很高兴你们喜欢 *Build a [Reasoning Model](https://sebastianraschka.com/glossary/#reasoning-model "Reasoning Model") (From Scratch)*（《从零构建推理模型》）！

不巧的是，第 198 页的清单 6.5（Listing 6.5）里有一个小笔误（见下方视频）。`torch.manual_seed(0)` 这一行应该是 `torch.manual_seed(5)`。

这是一个很小的改动，但它是复现清单 6.5 中的生成响应以及第 6 章后面相应 log 概率输出所必需的。如果用 0，代码当然仍然是正确的，但数值结果可能略有不同，这可能会造成困惑。总之，这就是一个 1 个字符的小改动 :)。

这个问题将在下一次印刷中修正。

对这一疏漏我深表歉意，希望这篇说明能帮你省下一些调试时间。

来源：我的 [Substack note](https://substack.com/@rasbt/note/c-301484736) 的网页版，略有编辑。
