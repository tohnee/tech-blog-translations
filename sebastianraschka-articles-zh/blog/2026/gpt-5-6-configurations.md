---
title: "GPT 5.6 的配置与默认选择"
title_en: "GPT 5.6 Configurations and Defaults"
source: https://sebastianraschka.com/blog/2026/gpt-5-6-configurations.html
crawled: 2026-09-06
translated: 2026-09-06
---

# GPT 5.6 的配置与默认选择

> 原文：[GPT 5.6 Configurations and Defaults](https://sebastianraschka.com/blog/2026/gpt-5-6-configurations.html)

是的，GPT 5.6 发布中可供选择的选项大概有点太多了。

不过，放在推理模型的语境下，我觉得有意思的是这些选项如何映射到训练时扩展与[推理时扩展](https://sebastianraschka.com/glossary/#inference-time-scaling "Inference-Time Scaling")。如果我们把这些选项粗略地映射到经典的 o1 图表上，那么 Sol、Terra 和 Luna 代表训练计算轴上的三种模型规模和训练预算，而 effort（推理力度）设置则位于推理时计算轴上。

![标注图解：将 GPT 5.6 的模型选项映射到训练计算扩展，将 effort 等级映射到推理时扩展](https://sebastianraschka.com/images/blog/2026/gpt-5-6-configurations/hero.webp)

图 1. 从 OpenAI 经典的 [o1 scaling plots](https://openai.com/index/learning-to-reason-with-llms/) 到 GPT 5.6 选项的粗略映射。三个模型选项代表不同的模型规模和训练预算，而 effort 设置代表推理时计算。

完整的列表包含三个模型选择和六个推理力度等级（Light、Medium、High、Extra High、Max 和 Ultra）。再加上 Work 与 Codex、Standard 与 Fast 之分，完整的配置矩阵就变成了

`Work/Codex × Sol/Terra/Luna × Light/Medium/High/Extra High/Max/Ultra × Standard/Fast`

也就是 `2 × 3 × 6 × 2 = 72` 种可能的配置。

那么，现在什么是好的默认选择？Luna 配 High effort？Sol 配 Light effort？还是 Terra 配 Medium effort？

当然，一张性能-成本对比图可以帮助找出性价比高的组合。例如，Luna 配 Extra High effort 可能比 Sol 配 Medium effort 更好且更便宜。

![Artificial Analysis Coding Agent Index 分数与 API 成本的散点对比图，涵盖 GPT 5.6 与多个对比模型](https://sebastianraschka.com/images/blog/2026/gpt-5-6-configurations/coding-agent-index-cost.webp)

图 2. Artificial Analysis Coding Agent Index v1.1 分数与 API 成本的对照，涵盖 GPT 5.6 及若干对比模型。图基于 [OpenAI 在 X 上的 GPT 5.6 发布帖](https://x.com/OpenAI/status/2075271425548795909)。

不过嘛，72 种可能的配置确实给我们留下了太多选择 🤯。
