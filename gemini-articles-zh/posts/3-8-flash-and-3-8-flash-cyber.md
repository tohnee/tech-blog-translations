---
title: "Gemini 3.8 Flash 与 3.8 Flash Cyber 现已发布"
title_en: "Introducing Gemini 3.8 Flash and 3.8 Flash Cyber"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/
site: gemini
date: 2026-09-02
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini 3.8 Flash 与 3.8 Flash Cyber 现已发布

> 原文：[Introducing Gemini 3.8 Flash and 3.8 Flash Cyber](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/) · Google

继三周前的 [3.7 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/) 之后，这也是我们在短短六周内发布的第三个 Flash 版本。今天，我们推出 Gemini 3.8——迄今我们最出色的推理与编程模型，同时保持与 3.7 相同的速度和低成本。Gemini 3.8 提供两个变体：

- **Gemini 3.8 Flash：**我们最智能的主力模型，相较 3.7 Flash 在软件工程、智能体化任务以及专业领域关键的多步推理方面都有显著提升。它以与 3.7 Flash 相同的入门价格提供
  [1](#footnote-1)
  ，即每百万输入 token 0.75 美元、每百万输出 token 3.75 美元。
- **Gemini 3.8 Flash Cyber：**我们能力最强的网络安全模型，在漏洞检测与自动化修补方面达到前沿级表现，通过我们全新的 [Fairwind Program](https://deepmind.google/fairwind-program/) 向受信任的防御者开放。

虽然这两个发布版本面向不同的部署环境，但它们都由同一套基础智能驱动，并借助长期运行的智能体化循环（该循环会对底层模型进行递归评估与改进）进一步加速。这一共享核心在编程与推理能力上的大幅提升，源自多项创新，其中包括在高要求网络安全领域的严格训练。

## Gemini 3.8 Flash：为长程编程与自主智能体而生

Gemini 3.8 Flash 相较 3.7 Flash 带来了大幅提升，其表现常常逼近成本更高的前沿模型。

![展示 Gemini 3.8 Flash 与其他模型对比的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.8-flash__evals__table_l.width-1200.format-webp_2pLdBp5.webp)

**在 DeepSWE v1.1（长程软件工程）上**，3.8 Flash 以端到端自主解决复杂工程问题的能力超越了大多数更大的前沿模型，而成本仅为其一小部分。

![展示 Gemini 3.8 Flash DeepSWE v1.1 成绩的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-flash__evals__deepswe.width-1200.format-webp.webp)

此外，3.8 Flash 在专业知识领域展现了对关键企业自主化至关重要的可靠性。在需要高级分析与报告的量化金融和专业法律等领域，3.8 Flash 在 [Vals Finance Agent V2](https://www.vals.ai/benchmarks/fabv2) 和 [Harvey's Legal Agent Benchmark](https://www.vals.ai/benchmarks/hlab) 等基准测试中超越了 3.7 Flash 和其他前沿模型。3.8 Flash 在 HLE-Verified 上还取得了 54.9% 的成绩，展示了其跨 STEM、人文与专业领域进行多步推理的能力。

![展示 Gemini 3.8 Flash Vals Finance Agent v2 成绩的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.8-flash_evals_vals-finan.width-100.format-webp.webp)

![展示 Gemini 3.8 Flash Harvey's Legal Agent Benchmark 成绩的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.8-flash_evals_harveys-le.width-100.format-webp.webp)

![展示 Gemini 3.8 Flash HLE-Verified 成绩的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.8-flash_evals_HLE_light.width-100.format-webp.webp)

这些性能提升源于一个核心设计选择：3.8 Flash 会更加卖力。在复杂任务上，它表现出更强的勤勉——执行额外的推理步骤，并迭代式地调用工具。有时，模型可能会消耗更多 token 以最大化性能，尤其是在更高的努力等级（effort level）下。

对于以计算效率为首要约束的应用，开发者可以使用更低的努力等级来最小化 token 开销，或继续使用 Gemini 3.7 Flash——它在效率优先的工作负载中仍获得完整支持。

Gemini 3.8 Flash 在 Google Antigravity 中仅凭一条包含循环指令的简单提示词就构建了这款游戏。游戏运用谜题、环境叙事以及用 Nano Banana 生成的纹理，打造出一个沉浸式 3D 关卡，玩家在其中扮演一位在城堡中穿行的巫师。

Gemini 3.8 Flash 在 Google Antigravity 中用一条提示词构建了功能完整的 DOS 版 Google Maps，包含地点、路线导航和街景，完全可玩。

借助 Gemini 3.8 Flash 在 Google Antigravity 中制作的名胜地理地形图，可以实时浏览剖面、2D 投影和科学讲解，数据来自美国地质调查局（U.S. Geological Survey）的真实数据集。

Hardware Anatomy 是一款用 Gemini 3.8 Flash 在 Google AI Studio 中构建的交互式 3D 可视化工具，可为硬件设备生成符合物理比例的拆解 Three.js 渲染图。它会自动把设备分解为多个图层，你可以用一个拆解滑块将其展开并检视。

## Gemini 3.8 Flash Cyber：专家级网络安全表现

Gemini 3.8 Flash Cyber 通过 [Fairwind Program](https://blog.google/innovation-and-ai/technology/safety-security/fairwind-program) 向一组受信任的防御者开放，在当今复杂的网络安全格局中提供决定性优势，同时具备 Flash 级的速度与成本，便于快速迭代。

### 自主漏洞发现

在查找漏洞的标准行业基准 CyberGym 上，Gemini 3.8 Flash Cyber 展现出前沿级的自主漏洞发现能力。它超越了 3.5 Flash Cyber，也超越了规模明显更大的前沿模型。

![展示 Gemini 3.8 Flash Cyber CyberGym Pass@1 成绩的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.8-cyber__evals__cybergy.width-1200.format-webp.webp)

为了更好地反映真实世界的防御需求——这些需求并不像 CyberGym 那样仅限于 C/C++ 代码库——我们还在一个综合性内部基准上评估了 Gemini 3.8 Flash Cyber，模型需要在跨 20 种编程语言的复杂代码库中发现各类漏洞。在这里，该模型相较我们之前的模型实现了令人瞩目的跃升，成功率超过 70%。

![展示 Gemini 3.8 Flash Cyber 真实世界漏洞发现能力的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.8-cyber__evals__rw-vuln.width-1200.format-webp.webp)

### 自动化修补

在 Gemini 3.8 Flash Cyber 上，我们专门聚焦于为防御者配备专家级能力，使其在与攻击者的对抗中占据优势。这也是我们从一开始就投入漏洞修复、并将其优先级置于漏洞利用等攻击性能力之上的原因。

由 Collinear 运营的 [CWE-Bench](https://cwe-bench.com/#leaderboard) 是一项颇具挑战性的外部修补能力基准。在这个基准上，Gemini 3.8 Flash Cyber 处于帕累托前沿：pass@1 为 47.2%，而某个领先的前沿模型为 47.8%，但前者的成本要低得多。

![展示 Gemini 3.8 Flash Cyber StaticBench Pass@1 与每次 rollout 成本对比的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-cyber__evals__cwe-ben.width-1200.format-webp.webp)

### 真实世界影响：保护 Google 的代码

我们已经在用 Gemini 3.8 Flash Cyber 保护 Google 全公司的代码。例如：

- Chrome 安全团队发现，3.8 Flash Cyber 为 Chrome 漏洞生成的正确补丁数量是体积大得多的最佳商业模型的 2.6 倍。
- Wiz 发现，与其他领先的前沿模型相比，Gemini 3.8 Flash Cyber 在其内部渗透测试基准上的召回率高出 7.5–9.7%，而成本仅为 1/5.2 至 1/2.3。
- Google 云漏洞研究团队借助 3.8 Flash Cyber 模型在不到 2 小时内发现了一个关键的基础性漏洞，而这类漏洞的研究与发现通常需要数月时间。

## 我们的 Fairwind Program 伙伴怎么说

![来自 Armadin 创始人兼首席架构师 David Slater 的引言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-flash__testimonial__ar.width-100.format-webp.webp)

![来自 Palo Alto Networks CTO 办公室总监 Charlie Sestito 的引言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-flash__testimonial__pa.width-100.format-webp.webp)

![来自 Snowflake CSTO Mayank Upadhyay 的引言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-flash__testimonial__sn.width-100.format-webp.webp)

![来自 Wiz 威胁暴露负责人 Gal Nagli 的引言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-flash__testimonial__wi.width-100.format-webp.webp)

## 以安全为本的构建

按照我们的[前沿安全框架](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/)，3.8 Flash 随附针对化学、生物、放射与核（CBRN）领域以及网络攻击滥用的防护措施，同时支持有益的使用场景。3.8 Flash Cyber 随附针对网络安全更为宽松的一套缓解措施，因此仅向需要更全面网络能力的受信任防御者开放。

按 Gray Swan 的测量，Gemini 3.8 系列模型在提示词注入鲁棒性方面也实现了显著跃升，可保护 Gemini 模型用户免受与提示词注入相关的恶意攻击。

![展示 Gemini 3.8 Flash Cyber Gray Swan IPI 基准成绩的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.8-flash_evals_attack__l.width-1200.format-webp.webp)

## 立即开始使用 Gemini 3.8 Flash 与 Cyber

- **开发者**：使用 3.8 Flash 构建，并在 [Google Antigravity](https://antigravity.google/) 中探索智能体优先的工作流，或立即通过 [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-3.8-flash) 和 [Android Studio](https://developer.android.com/studio) 在 Gemini API 中开始构建，也可以在 [Stitch](http://stitch.withgoogle.com/) 中生成 UI。请从我们的[开发者文档](https://ai.google.dev/gemini-api/docs/latest-model)入手。
- **企业**：在 [Gemini Enterprise](https://console.cloud.google.com/agent-platform/studio/multimodal?mode=prompt&model=gemini-3.8-flash) 中使用 3.8 Flash。
- **消费者**：3.8 Flash 面向 Google AI Pro 和 Ultra 订阅用户开放，覆盖 [Gemini 应用](http://gemini.google.com/)、Google Search 中的 [AI Mode](http://google.com/ai) 以及 [Google Sheets](http://sheets.new/) 中的 Gemini。
- **网络安全**：通过我们全新的 [Fairwind Program](https://blog.google/innovation-and-ai/technology/safety-security/fairwind-program)，我们为受信任的政府机构以及关键基础设施运营方和软件维护方提供 Gemini 3.8 Flash Cyber 的优先访问。[申请访问权限](https://deepmind.google/fairwind-program/)。
