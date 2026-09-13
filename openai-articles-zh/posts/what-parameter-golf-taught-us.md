---
title: "Parameter Golf 教会了我们什么"
title_en: "What Parameter Golf taught us"
source: https://openai.com/index/what-parameter-golf-taught-us/
crawled: 2026-09-13
category: research
translated: 2026-09-13
---

# Parameter Golf 教会了我们什么

> 原文：[What Parameter Golf taught us](https://openai.com/index/what-parameter-golf-taught-us/) · OpenAI 博客

我们发起 Parameter Golf，是为了吸引并支持机器学习研究社区去探索一个全新的、约束极严的机器学习问题。我们希望这个挑战足够有趣，能奖励真正的技术创新，同时保持概念上的简单且易于验证。

参与者需要在固定的 FineWeb 数据集上最小化留出集损失（held-out loss），同时保持在 16 MB 的产物限制之内（模型权重与训练代码都计算在内），以及 8×H100 上 10 分钟的训练预算。我们提供了基线、数据集和评估脚本，参与者可以 fork 代码库、改进模型，并通过 GitHub 提交他们的结果。

在八周的时间里，我们收到了来自 1,000 多名参与者的 2,000 多份提交。这些提交在技术广度、创造力和「打规则擦边球」方面都让我们印象深刻——从细致的优化器调优和量化工作，到新的建模思路和测试时训练（test-time training）。

这个挑战最令人兴奋的一点，是看到参与者对 AI 编程智能体的广泛使用。智能体帮助降低了实验成本，让更多人更容易参与，并改变了比赛的节奏。它们也给提交评审、归属认定和评分带来了新的挑战。

这场挑战对我们而言也成为一个有意义的人才发掘渠道。这是我们举办 Parameter Golf 的目标之一；它也提供了一个有用的信号：开放式的技术挑战能够揭示出色的机器学习品味与毅力。

在本文中，我们将重点介绍一些让我们感到惊喜和有趣的提交，并分享在强大 AI 智能体时代举办编程比赛的心得。

## 技术观感

### 破纪录赛道

我们对破纪录赛道（record track）排行榜上的每份提交进行了评审并独立复现，并验证每份提交在其提交时确实是破纪录的。有几个主题尤为突出。

***训练优化***

一些最强的结果来自对现有组件的细致调优。

| **提交** | **贡献者** | **技术** | **为什么重要** |
|---|---|---|---|
| [#60](https://github.com/openai/parameter-golf/pull/60) | @notapplica | 整合了 [#50](https://github.com/openai/parameter-golf/pull/50)、[#42](https://github.com/openai/parameter-golf/pull/42) 以及很可能是 [#39](https://github.com/openai/parameter-golf/pull/39) 的既有成果，然后借助 Muon 权重衰减、谱嵌入初始化、残差混合调度（residual-mix scheduling）和编译评估，让更深的模型得以跑通。 | 律己的排行榜工作的有力范例：识别哪些既有改进真正有效，并把它们干净地组合起来。 |

***量化***

有几份提交在压缩与导出上发力很猛。

| **提交** | **贡献者** | **技术** | **为什么重要** |
|---|---|---|---|
| [#414](https://github.com/openai/parameter-golf/pull/414) | @signalrush | 训练后使用 GPTQ-lite 对权重进行量化。 | 第一份成功使用 GPTQ-lite 的排行榜提交，带来了更好的评估结果。 |
| [#1060](https://github.com/openai/parameter-golf/pull/1060) | @dexhunter | 在 @raahilshah 的 [#634](https://github.com/openai/parameter-golf/pull/634) 基础上成功使用完整 Hessian GPTQ。 | 把更早的量化工作扩展成一条更强的压缩路径。 |

***测试时与评估策略***

有几份提交把模型改进与评估策略之间的边界向外推了推。这些做法在规则之下是有效的，但作为组织者，我们需要对它们进行细致的审查。

| **提交** | **贡献者** | **技术** | **为什么重要** |
|---|---|---|---|
| [#77](https://github.com/openai/parameter-golf/pull/77) | @samacqua | 使用「先打分、按文档」的 LoRA 测试时训练：先打分，只在已打分的文本块上做适配，并在文档边界处重置。 | 在规则允许且可审查的前提下，把模型改进与评估策略之间的边界向外推了推。 |
| [#1019](https://github.com/openai/parameter-golf/pull/1019) | @abaybektursun | 使用自生成的 GPTQ 校准：从训练好的模型生成校准文本，再从这些激活构建 GPTQ Hessian。 | 一种有创意的校准策略，需要组织者仔细审查。 |

***新的建模与数据思路***

有几份提交引入了格外有创意的建模或数据思路。

| **提交** | **贡献者** | **技术** | **为什么重要** |
|---|---|---|---|
| [#1729](https://github.com/openai/parameter-golf/pull/1729) | @romeerp | 提出 CaseOps 分词器：无损的大小写操作符 token，辅以原始字节 BPB 的旁路（sidecar）记账。 | 一个有创意的分词器与数据表示思路。 |
| [#265](https://github.com/openai/parameter-golf/pull/265) | @unnir | 提出 XSA，一种高效的「部分独占自注意力」（partial Exclusive Self Attention）方法，带有 GQA 感知的分组视图。 | 为这场挑战引入了一个高效的注意力变体。 |
| [#65](https://github.com/openai/parameter-golf/pull/65) | @aquariouseworkman | 提出 SmearGate 和 BigramHash：可学习的前一 token 嵌入混合，加上相邻 token 对的哈希特征。 | 从零开始添加了新的特征机制。 |
| [#1204](https://github.com/openai/parameter-golf/pull/1204) | @msisovic | 提出 mini 深度循环（depth recurrence）：重复第 4、5 层，把循环的启用推迟到训练中段，并对重复的 MLP 做部分解绑。 | 第一条让循环层真正有效工作的被接受排行榜记录。 |

我们选择重点介绍这九份提交，因为它们代表了我们所期望这场挑战能够呈现的结果光谱。有的参与者通过细致调优找到收益；有的在量化和低秩技术上发力；有的探索了评估规则的边缘；还有几份提交引入了来自文献或从零构想的建模或数据思路，带来了意想不到的收益。

### 非破纪录赛道

非破纪录赛道汇集了许多有创意的提交。我们精选了 15 个最爱，方法涵盖从非自回归文本建模到动态分词。

由于这条赛道更具实验性质，我们较少关注原始性能，而更关注方法本身在技术上是否有趣。有三份提交尤为突出：

- [CiprianFlorim-Ifrim 的状态空间模型与 JEPA 结合提交](https://github.com/openai/parameter-golf/blob/main/records/track_non_record_16mb/2026-03-26_37M_LeWM_Jepa_Mamba2_10L_UNet_INT4FP8QAT_Brotli/README.md)
- [ddavidgao 的 Designator/引导注意力提交](https://github.com/openai/parameter-golf/blob/main/records/track_non_record_16mb/2026-03-23_DGAttention_DavidGao/README.md)
- [DariusFeher 的字节级 H-Net 提交](https://github.com/openai/parameter-golf/blob/main/records/track_non_record_16mb/2026-03-29_HNet_ByteVsSubword_Study/README.md)

这是我们最喜欢的三份非破纪录提交，尽管它们未必是性能上的前三名。

尽管如此，非破纪录赛道依然竞争激烈。一半的非破纪录排行榜条目击败了 1.22 BPB 的朴素基线，排名第一的条目达到了 1.12 BPB。

我们认为这令人鼓舞。即使面对强大的 transformer 基线，替代方法有时也能与主流架构一较高下。

我们还认为，这条赛道尤其受益于强大编程智能体的可得性。智能体让验证投机性想法的原型成本大大降低，包括那些在以往短周期比赛中可能让人觉得过于耗时或没有把握去尝试的方法。

## 收获

Parameter Golf 与此前同类比赛的一大区别在于编程智能体的广泛使用。绝大多数提交者都提到在其工作中使用了智能体。

这降低了参与门槛。参与者可以更快地搭建实验、查看不熟悉的代码、以更少的摩擦测试想法。Runpod 赞助的 1,000,000 美元算力也在让更多人能够参与这场挑战方面发挥了重要作用。

与此同时，智能体的使用给提交与评分带来了新问题。许多提交只是对现有高分方案的小改动，而非从根本上全新的方法。这往往是有益的：好的想法会迅速传播并被他人改进。但它也制造了噪音。当不符合比赛规则的提交获得了异常高的分数时，其他智能体有时会照搬这些想法，沿着同样无效的路径继续走下去。

提交量也改变了我们运营比赛的方式。我们无法人工检查每一份提交，还要让排行榜持续运转。在挑战期间，我们开发了一个基于 Codex 的内部分诊机器人来监控新提交，并把需要人工审查的标记出来。在我们每天收到数百份提交的时段，这一点变得尤为重要。

AI 智能体也成为围绕这场挑战的社区的一部分。在比赛的大部分时间里，@notapplica 和他们的编程智能体运营着一个「Live Updates」公告栏，追踪重大事件、解释排行榜上的方法，并帮助其他参与者跟上比赛进展。社区评审工具也相继出现，帮助经验较少的参与者检查自己的提交是否符合规则、避开常见的无效做法。

## 下一步是什么？

我们的首要目标是发起一个[符合条件的参与者](https://cdn.openai.com/pdf/d5caec5a-ee81-419d-b0d7-39f1424d819c/OpenAI%20Model%20Craft_%20Parameter%20Golf%20Challenge%20Terms%20and%20Conditions.pdf)都能参与并体验机器学习研究的挑战。Parameter Golf 带来了大量技术上扎实且有创意的提交，也让我们更清楚地看到，随着 AI 智能体变得更加强大和普及，开放式研究比赛可能会发生怎样的变化。

我们正在考虑未来发起更多这样的挑战。如果你感兴趣，请填写[挑战参与者表单](https://jobs.ashbyhq.com/openai/form/open-ai-challenge-parameter-golf)。
