---
title: "推出 Grok 4.7"
title_en: "Introducing Grok 4.7"
date: 2026-09-21
source: https://x.ai/news/grok-4-7
crawled: 2026-10-01
translated: 2026-10-01
---

# 推出 Grok 4.7

> 原文：[Introducing Grok 4.7](https://x.ai/news/grok-4-7) · xAI

2026 年 9 月 21 日

推出 Grok 4.7

SpaceXAI 面向编码和知识工作的最强大模型。速度翻倍，价格仅为同级模型的一半。

免费试用

开始构建

Grok 4.7 是我们面向编码和知识工作的最强模型。它能在困难任务上坚持工作更久，更仔细地检查自己的工作，并配备我们迄今校准最好的安全保障。它以与

Grok 4.6

相同的价格和速度提供服务，在其同级中极具竞争力。

一张散点图和折线图，比较 Fable 5.1、Opus 5、Grok 4.7、GPT-5.6 Sol 和 Sonnet 5 的得分与平均每任务成本。

55

%

CursorBench 4.0 得分

50%

45%

40%

35%

30%

25%

20%

$18

$15

$12

$9

$6

$3

$0

平均每任务成本

Fable 5.1

Opus 5

GPT-5.6 Sol

Sonnet 5

Grok 4.7

成本

Token 数

步数

在强调长时间运行编码任务的 CursorBench 4.0 上，Grok 4.7 的性价比处于前沿水平。

模型改进

与

Grok 4.6

相比，Grok 4.7 采用了全新的、更大的基础模型。它经过更长的强化学习训练，任务组合更难，并向需要多个小时才能完成的问题倾斜。该模型更擅长验证自己的工作和管理更长的上下文。我们还训练 Grok 4.7 原生理解

Grok Bot

harness（运行框架），使其在对话任务和一般知识工作上表现更好。

Grok 4.7

xHigh

Grok 4.6

High

GPT-5.6 Sol

Max

Fable 5.1

Max

输入 token 价格

每百万美元数

$2

$2

$4

$10

输出 token 价格

每百万美元数

$6

$6

$20

$50

软件工程

CursorBench 4.0

46.3%

40.4%

41.7%

51.8%

软件工程

DeepSWE v1.1

71.0%*

65.2%

72.7%

70.0%

电气工程

EEBench

64.0%

53.0%

39.4%

56.4%

多小时办公工作

AA Briefcase v1.1

1,657

1,546

1,487

1,678

多小时终端工作

Terminal-Bench 4.0

37.6%

20.3%

37.3%

57.9%

法律工作

Harvey Legal Agent Benchmark

19.6%

15.8%

2.5%

6.7%

临床推理

HealthBench Professional

56.7%

48.5%

60.5%

62.1%

* 高投入（high effort）

Grok 4.7、Grok 4.6、GPT-5.6 Sol 和 Fable 5.1 的 token 价格与基准得分。基准包括 CursorBench 4.0、DeepSWE v1.1、EEBench、AA Briefcase v1.1、Terminal-Bench 4.0、Harvey Legal Agent Benchmark 和 HealthBench Professional。Grok 4.7 在 DeepSWE 上的星号表示高投入（high effort）得分。

Grok 4.7 在创建文档和演示文稿方面表现更好。在 GDPval 和 AA Briefcase 中，AI 需要完成律师、护士和金融分析师等专业人士所做的工作。Grok 4.7 在这两项基准上均较 Grok 4.6 有所提升，表现与其他前沿模型相当。

专业知识工作

多小时办公工作

电气工程

专业知识工作

GDPval

0

500

1000

1500

Elo 分数

1735

Fable 5.1

（max）

1695

Grok 4.7

（xhigh）

1605

Grok 4.6

（high）

1542

GPT-6 Astra

（max）

比较 Grok 4.7 与 Grok 4.6、Fable 5.1 和 GPT-6 Astra 的 GDPval、AA Briefcase 和 EEBench 得分。

安全与网络安全

Grok 4.7 采用全新的安全保障体系构建。它是我们测试过的在拒绝能力和越狱抵抗方面最强的模型。在网络安全和生物学工作等双用途领域，它在良性任务上的实用性和对危险任务的安全拒绝两方面均处于领先，以 62.4% 的成绩登顶 LatchBio 的生物安全基准。

Grok 4.7 在强大的网络防御能力与合法使用的低拒绝率之间取得了平衡。它在 HackerBench v0.3（我们针对有风险和恶意网络任务的基准）上展现出最高的安全性，仅放行 3.3% 的风险双用途提示，同时极少阻断合法的安全工作。我们还开始向部分精选网络安全合作伙伴提供仅限邀请的 Grok 4.7 红队能力访问权限，用于防御研究。

定价与可用性

Grok 4.7 现已在

Cursor

和

Grok Build

中可用。它也可以通过

Grok API

、第三方编码 harness（运行框架），以及模型路由器和云平台使用。

该模型定价为每百万输入 token 2 美元起，每百万输出 token 6 美元。我们还提供快速变体，输出速度翻倍，价格也翻倍。

控制台

创建 API 密钥

docs.x.ai

阅读文档

在 Grok Build 中免费试用

立即开始，请访问

x.ai/build

。

$

curl -fsSL https://x.ai/cli/install.sh

| bash

© 2026 SpaceXAI LLC
