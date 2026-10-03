---
title: "Gemini 4 Argon：我们前沿智能的新时代"
title_en: "Gemini 4 Argon: our next era of frontier intelligence"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/
site: gemini
date: 2026-09-30
crawled: 2026-10-03
translated: 2026-10-03
---

# Gemini 4 Argon：我们前沿智能的新时代

> 原文：[Gemini 4 Argon: our next era of frontier intelligence](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/) · Google

今天，我们发布全新的前沿模型 Gemini 4 Argon，它正通过我们的 [Fairwind Program](https://deepmind.google/fairwind-program/) 向一批受信任的网络防御者推送。Argon 专为在复杂的长程工作流中持续进行深度推理而打造，正在从根本上改变我们在 Google 的工作与构建方式。它在真实世界软件工程、法律与金融等企业知识工作以及网络安全防御等复杂工作流中，均能交出前沿水准的表现。

要安全地发布这一级别的前沿能力，需要采取分阶段推进的方式。我们正积极参与美国政府面向发布前模型访问的自愿性流程，同时逐步扩大访问范围。我们将持续收集早期测试者的反馈，不断完善防护措施，尽快让开发者、企业和消费者都能用上 Argon。

Argon 将以入门价格
[1](#footnote-1)
上线：每百万输入 token 2 美元、每百万输出 token 10 美元，缓存输入 token 在输入 token 价格基础上减免 95%。

## 改变我们在 Google 的工作与构建方式

Gemini 4 Argon 已经在我们的内部工作流中投入使用，数千名 Google 员工都强调了它在专业编程任务、开展更深入的研究以及写作质量方面的优势。它正帮助团队更快地构建、突破工程生产力的边界，并加速各项突破：

- **量子算法优化：**Argon 正在帮助我们的量子计算研究人员优化那些制约重要应用性能的子程序的时空资源（量子比特 × 门操作）。在一个例子中，它仅用几分钟就在已发表的基线结果的基础上提升了 40%。

- **内存效率：**一队 Argon 智能体分析了整个服务器机群的性能剖析遥测数据，自主识别内存优化机会并在 Google 的各个数据中心加以应用，全部上线后可释放超过 300 TiB 内存，预计总共可节省 500 TiB 到 1 PiB。

- **大规模代码库迁移与优化：**Argon 智能体正在 Google 内部推进 C/C++ 代码库向 Rust 的迁移——规模从 re2、libgav1 等核心库的数万行代码，一直到 Fuchsia Zircon 内核的 80 万行以上代码。鉴于其中许多系统的关键地位，这类大规模重写在上生产环境之前，都要经过严格的自动化与人工审计、仿真测试和评审。

  以 libgav1（Google 的开源视频解码软件）为例，Argon 智能体在已有的 Rust 移植版基础上，通过多轮性能剖析导向的实验、研究编译器的输出、编写安全的 Rust 代码让编译器自动向量化，替换了 3.2 万行 SIMD 代码。最终成果是一个内存安全的视频解码器：比原 Rust 移植版快 2.7 倍，视频输出完全一致，性能进一步逼近优化版 C++ 实现。

## 全力攻克你最复杂的问题

为支撑 Gemini 4 Argon 在更长、更复杂场景下的能力，我们将模型的输出 token 上限从之前的 64K 大幅提升至行业领先的 1M。当模型拥有充分的空间深入思考、在单次生成中产出数十万 token 时，它便能在推理上达到全新的深度，一次性解决棘手难题。

![展示 Gemini 4 Argon 各项能力的基准测试图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini-4-argon_table_blog.gif)

## 支撑跨领域的编程与企业工作流

Gemini 4 Argon 在编程、推理与多模态方面的能力，加上其驾驭长程多步骤任务的本领，使其在一系列企业工作流中表现卓越。

Google 工程师已将 Argon 用于日常任务，从日常调试到大规模代码库迁移和算法设计。它在 DeepSWE v1.1 上创下新的最先进成绩（77.9%），该基准衡量模型在真实世界长程软件工程任务中的表现。

在编程之外，Argon 是 [Vals Index](https://www.vals.ai/benchmarks/vals_index) 上排名第一的模型。该指数衡量模型在金融、编程、法律和税务工作中创造的经济影响，并按各行业对美国 GDP 的贡献加权。在其他领域专项评测中，我们也看到了同样领先的表现，例如 Vals Finance Agent v2（多步骤金融研究）和 Harvey 的 Legal Agent Benchmark（法律研究与文书起草）。在 Zapier 用于衡量核心业务职能端到端执行能力的基准 AutomationBench 上，Argon 以 51.3% 的得分排名第一。

当知识工作需要视觉理解时，Argon 的表现同样出类拔萃。它能够进行专业的图表分析、从长视频中识别细节，并根据一系列文档采取行动。例如，在衡量长视频理解能力的 LVBench 上，Argon 以 91.7% 的得分达到最先进水平。

![DeepSWE 评测图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_4_cyber_evals_deepswe.gif)

![Vals Index 图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_4_cyber_evals_vals_index.gif)

![Vals 金融基准图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_4_cyber_evals_vals_finance.gif)

![Harvey 基准图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_4_cyber_evals_harveys.gif)

![AutomationBench 图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_4_cyber_evals_automationbench.gif)

## 领先的防御性网络安全能力

为了让网络防御者更好地武装起来、应对新时代的网络攻击，我们将 Gemini 4 Argon 训练得具备强大的网络安全防御能力。Argon 能够自主发现、验证并修补关键软件漏洞。对于受信任的防御者以及 Google 自己的内部团队，我们将提供不带网络防护限制的 Argon，让他们得以充分发挥其前沿级的网络安全防御能力。

[Wiz](https://www.wiz.io/) 已经通过其 [Scan for Good](https://www.wiz.io/scan-for-good) 计划将 Argon 用于网络安全防御——该计划致力于通过发现并修复高风险暴露面，免费保护关键公共基础设施。在早期的一次实际影响展示中，该模型发现了一个关键漏洞，全球各地医院使用的医疗软件中的敏感个人信息因之暴露——这是一个以往前沿模型都未能发现的严重风险。

在评估模型安全漏洞修复能力的 [CWE-bench v1](https://cwe-bench.com/) 上，Argon 以最高分 68% 并列第一，在 3.8 Flash Cyber 于 [CWE-bench v0](https://cwe-bench.com/?v=v0) 上取得的前沿成绩基础上更进一步。

![CWE 基准图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini_4_cyber_evals_cwe_bench.width-1200.format-webp.webp)

在漏洞发现方面，Gemini 4 Argon 相较 3.8 Flash Cyber 实现了令人瞩目的飞跃。例如：

- 在 Google 内部的综合漏洞基准上，Argon 在覆盖 20 种编程语言的复杂代码库中发现了种类繁多的暴露面。
- 在 Wiz 内部的黑盒渗透测试基准上（该基准测试模型在没有源代码的情况下分析在线 Web 系统的能力），Argon 在发现攻击面、识别漏洞以及生成概念验证证据以验证漏洞等方面均优于 3.8 Flash Cyber。

![安全漏洞图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini_4_cyber_evals_security_vu.width-1200.format-webp.webp)

## 在广泛开放前强化前沿防护措施

在向更大范围推送 Gemini 4 Argon 之前，我们将继续从四个主要方面强化关键的前沿防护措施：

**防范滥用：**为防止不法分子利用 Argon 发动网络攻击或化学、生物、放射和核（CBRN）攻击，模型被设计为拒绝有害请求，同时依据我们的[前沿安全框架](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/)保留正当的双重用途科学研究。我们正在为这次发布强化防护措施的鲁棒性，包括改进监测模型[内部激活](https://arxiv.org/abs/2601.11516)以发现滥用的技术。这些防护措施已经由内外部红队采用人工与自动化攻击相结合的方式完成了鲁棒性测试。

**防范提示词注入攻击：**Argon 也是我们迄今对间接提示词注入最具韧性的模型——这类攻击利用恶意指令或上下文来劫持模型的行为。此类攻击十分复杂，需要时刻保持警惕并构筑多层防御。通过自动化红队测试与对抗训练，Gemini 4 Argon 在 Gray Swan 的间接提示词注入（IPI）基准上的注入鲁棒性处于领先地位。

![Gray Swan 评测图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini_4_cyber_evals_gray_swan_i.width-1200.format-webp.webp)

**监测失对齐：**为防止 Argon 越界行事、以超出用户意图的方式去完成任务，我们正在部署失对齐缓解措施，对 Argon 的思维链和行动进行监测，并在必要时中止执行。

我们曾用类似的系统监测训练过程，并向专门的事件响应团队发送警报，同时谨慎避免把监测结果回馈到训练之中，以防 Argon 的推理被塑造成会规避我们的监测。在能力不断增强的关键时刻，我们[强烈建议业界同行](https://institute.deepmind.com/essays/the-case-for-reasoning-transparency/)在应对对齐风险的同时保留推理透明度，让模型的思考内容继续有助于识别和诊断失对齐问题。

**加固系统：**随着前沿模型的能力日益增强，要安全地测试它们，就需要能跟上这些系统本身步伐的安全环境。按照我们的[智能体控制路线图](https://deepmind.google/blog/securing-the-future-of-ai-agents/)，我们正在加固沙箱环境，在高风险训练或评测开始之前对其进行隔离与封存。我们致力于与合作伙伴分享这些智能体安全最佳实践，共同提升整个生态系统的安全性。

## 即将推出

我们打造 Gemini 4 Argon，让它在编程、知识工作、网络安全防御和创意写作方面具备前沿级能力，成为开发者、专业人士和企业攻克最难难题时的伙伴。我们感谢首批网络防御者与受信任测试者——他们的真实世界评测与反馈将帮助我们在正式发布之前强化系统。发布将首先面向付费 API 客户和 Google AI Ultra 订阅用户，随后陆续面向开发者、企业和消费者。
