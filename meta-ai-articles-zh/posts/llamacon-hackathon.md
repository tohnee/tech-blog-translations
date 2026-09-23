---
title: "首届 LlamaCon 黑客松获奖者揭晓"
title_en: "Meet the winners of our first-ever LlamaCon Hackathon"
date: 2025-05-13
source: https://ai.meta.com/blog/llamacon-hackathon
crawled: 2026-09-22
translated: 2026-09-22
---

# 首届 LlamaCon 黑客松获奖者揭晓

> 原文：[Meet the winners of our first-ever LlamaCon Hackathon](https://ai.meta.com/blog/llamacon-hackathon) · Meta AI（Wayback 存档）

继汇聚全球开发者的首届 AI 活动 LlamaCon 之后，我们在旧金山举办了首届 LlamaCon 黑客松。活动从 600 多名报名者中召集了 238 位才华横溢的开发者与创新者，进行一整天的构建。挑战内容是：在短短 24 小时内，使用 Llama API、Llama 4 Scout 或 Llama 4 Maverick（或这些前沿工具的任意组合）创建一个可演示的项目。赌注不低：总额 3.5 万美元的现金奖品，包括一、二、三等奖，以及最佳 Llama API 使用专项奖。来自 Meta 与赞助伙伴的评审团仔细评估了提交的 44 个项目。我们感谢合作伙伴 Groq、Crew AI、Tavus、Lambda、Nebius 和 SambaNova 在整个黑客松期间提供的宝贵支持。每家赞助商都提供了带额度的使用量、专家工作坊、导师、现场答疑展位、评委以及 Discord 远程支持。

## 获奖者

我们进行了两轮评审，从 44 个提交项目中筛选出六强，再决出一、二、三等奖与最佳 Llama API 使用奖。

**OrgLens——一等奖**

OrgLens 创建了一个 AI 驱动的专家匹配系统，帮你连接组织内合适的专业人士。通过分析来自 Jira 任务、GitHub 代码与 issue、内部文档和简历等多种来源的数据，OrgLens 为每位贡献者创建全面的知识图谱与详细画像。你可以用先进的 AI 搜索能力查找专家，甚至与某人的数字孪生对话提问，再决定是否联系。为演示其能力，团队用 React、Tailwind 和 Django 构建了演示 Web 应用，借助 GitHub API 与 Llama API 处理并存储数据。OrgLens 精简了专家匹配流程，让「合适的事找到合适的人」更加容易。（GitHub）

**Compliance Wizards——二等奖**

Compliance Wizards 创建了一个 AI 驱动的交易分析器，基于自定义风险评估算法检测欺诈并向用户告警。系统会向用户发送邮件通知，提示其对交易进行报告或确认。随后用户可以与 AI 语音助手对话完成报告与确认。利用 Llama API 的多模态能力，欺诈评估员可以上传客户信息并搜索与客户相关的新闻，协助判断客户是否卷入任何值得注意的犯罪活动。（GitHub）

**Llama CCTV Operator——三等奖**

由 Agajan Torayev 领衔的团队构建了一个 Llama CCTV AI 控制室操作员，无需任何模型微调即可自动识别自定义的监控视频事件。操作员可以用简单语言定义视频事件。借助 Llama 4 的多模态图像理解，系统每五帧捕获并检测一次运动，评估这些预定义事件并向操作员报告。（GitHub）

**Geo-ML——最佳 Llama API 使用奖**

地质学家 William Davis 使用 Llama 4 Maverick 和 GemPy，为可能的挖掘地点、地形图和矿藏生成 3D 地质模型。Geo-ML 的工作方式是：处理 400 页的地质报告，把信息整合为结构化的地质领域专用语言，再用它生成地下地质的 3D 表示。（GitHub）

「这是我第一次真正用 LLM API 从很长的地质研究论文中提取超长文本和图像，所以我利用 Llama Maverick 的超长上下文窗口以及文本和图像多模态能力来提取文本并转换为领域专用语言，把文档中存储的一切浓缩出来，」Davis 说，「我日常工作的大部分时间都在读地质文档。有一个 LLM 能在后台替我做这件事，真是太棒了。」

入围决赛的 Team Concierge 也令人瞩目——他们自带 GPU 参赛。「我们认为 Llama 4 Maverick 最出色的一点是其稀疏专家混合（MoE）的天性与开源可用性，使微调成为可能，」该团队说，「Meta 最近在 GitHub 上发布了一个出色的微调工具——合成数据生成（Synthetic Data Generation）工具。我们用 Llama API 从多个来源汇编数据，创建问答数据集，并微调了一个 Llama 4 Maverick 模型。我们计划把它提交到开放基准——目前还没有 Llama 4 编码模型，而凭借 100 万上下文窗口，它有望出类拔萃。」

你可以在 YouTube 上观看入围者的演示。开发者可申请下一届 Llama 黑客松，将于 2025 年 5 月 31 日至 6 月 1 日在纽约举行。
