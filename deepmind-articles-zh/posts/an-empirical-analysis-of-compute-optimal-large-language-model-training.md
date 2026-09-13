---
title: "算力最优的大语言模型训练的实证分析"
title_en: "An empirical analysis of compute-optimal large language model training"
source: https://deepmind.google/blog/an-empirical-analysis-of-compute-optimal-large-language-model-training/
site: deepmind
date: 2022-04-12
crawled: 2026-09-13
translated: 2026-09-13
---

# 算力最优的大语言模型训练的实证分析

> 原文：[An empirical analysis of compute-optimal large language model training](https://deepmind.google/blog/an-empirical-analysis-of-compute-optimal-large-language-model-training/) · Google DeepMind

过去几年，语言建模领域的焦点一直是通过增加基于 transformer 的模型的参数量来提升性能。这一方法在众多自然语言处理任务上取得了令人瞩目的成果和最先进的性能。

DeepMind 也沿着这条研究路线前进，最近展示了 [Gopher](https://arxiv.org/abs/2112.11446)——一个 2800 亿参数的模型，它在包括语言建模、阅读理解和问答在内的广泛任务上确立了领先性能。此后，一个更大的模型 [Megatron-Turing NLG](https://arxiv.org/abs/2201.11990) 也已发布，拥有 5300 亿参数。

由于训练这些大模型的成本高昂，估算出尽可能好的训练方案至关重要，以避免浪费资源。具体而言，transformer 的训练算力成本由两个因素决定：模型规模和训练 token 的数量。

当前一代大语言模型把增加的计算资源用于提高大模型的参数量，同时把训练数据规模固定在约 3000 亿 token 左右。在这项工作中，我们实证考察了在计算资源增加时，扩大模型规模与增加训练数据量之间的最优权衡。具体来说，我们要问的问题是："在给定的算力预算下，最优的模型规模和训练 token 数量是多少？"为回答这个问题，我们训练了不同规模、不同 token 数量的模型，并对这一权衡进行实证估计。
我们的主要发现是：当前的大语言模型相对于其算力预算而言太大了，训练数据则不足。事实上，我们发现，以训练 Gopher 所用的训练 FLOP 计，一个规模缩小 4 倍、训练数据增加 4 倍的模型才是更优选择。

![一张双对数坐标图，比较大语言模型在参数量与训练 token 数上的表现，实线为"我们估计的算力最优缩放"并标注了 FLOP。Megatron-Turing NLG（530B）、Gopher（280B）和 GPT-3（170B）等参数过多的模型远高于该线，而算力最优的 Chinchilla（70B）模型恰好落在线上。](https://lh3.googleusercontent.com/iPsfVUThNKaxHiz8VbAG4dnKxFVopLZHQ_7rV54wVuEh_jLDTKLn2yUAXXQHQYSFsH3wbnha-SffP9ssoc6sSBYRMN7nwGbkwygRH32qQ9ZqG9q-3vk=w1440)

**图 1：**基于我们的方法，我们展示了关于最优训练 token 数量和参数量的预测。图中标出了三个已发布的不同大语言模型的训练配置点，以及我们的新模型 Chinchilla。

我们[检验了数据缩放假设](https://arxiv.org/abs/2203.15556)：训练 Chinchilla——一个在 1.3 万亿 token 上训练的 700 亿参数模型。尽管 Chinchilla 与 Gopher 的训练算力成本相同，我们发现它在几乎所有受测任务上都优于 Gopher 和其他大语言模型，尽管它的 700 亿参数相比 Gopher 的 2800 亿少得多。

![柱状图，比较 Chinchilla（70B）、Gopher（280B）、GPT-3（175B）和 Megatron-Turing NLG（530B）在多个自然语言处理基准（MMLU、TriviaQA、LAMBADA、HellaSwag、PIQA、WinoGrande、BoolQ）上的准确率百分比。图表显示 Chinchilla 在几乎所有任务上都稳定优于更大的模型。](https://lh3.googleusercontent.com/tD2PbVfdzGYr-2Ip6KNKrOmOYaaJ2HYilB-G9RJeszjYOvI5d_uiGt8j0MDxN-66UJzIkH4_Kdd05buxgzoehSjngWxbdwAUQu5MBsi2QumQW538_A=w1440)

**图 2：**在多个常见基准上——包括问答（TriviaQA）、常识推理（HellaSwag、PIQA、Winogrande、BoolQ）、阅读理解（LAMBADA）以及大规模多任务语言理解（MMLU）通识基准——我们比较了 Gopher、Chinchilla、GPT-3 和 Megatron-Turing NLG 的表现。

Chinchilla 发布之后，一个名为 [PaLM](https://research.google/blog/pathways-language-model-palm-scaling-to-540-billion-parameters-for-breakthrough-performance/) 的模型随之发布，拥有 5400 亿参数，在 7680 亿 token 上训练。该模型的训练算力预算约为 Chinchilla 的 5 倍，并在一系列任务上超越了 Chinchilla。虽然训练语料不同，但我们的方法确实预测到：即便算力并非最优，用我们的数据训练出的这样一个模型也会优于 Chinchilla。按 PaLM 的算力预算，我们预测最优且推理更高效的选择是一个在 3 万亿 token 上训练的 1400 亿参数模型。

更小、性能更强的模型还有一个额外好处：推理时间和内存成本都降低了，使查询模型更快，所需的硬件也更少。在实践中，虽然 Gopher 与 Chinchilla 的训练 FLOP 相同，但使用 Chinchilla 的成本要低得多，而且性能更好。进一步的简单优化或许仍能带来巨大收益。
