---
title: "评估生成式 AI 的社会与伦理风险"
title_en: "Evaluating social and ethical risks from generative AI"
source: https://deepmind.google/blog/evaluating-social-and-ethical-risks-from-generative-ai/
site: deepmind
date: 2023-10-19
crawled: 2026-09-13
translated: 2026-09-13
---

# 评估生成式 AI 的社会与伦理风险

> 原文：[Evaluating social and ethical risks from generative AI](https://deepmind.google/blog/evaluating-social-and-ethical-risks-from-generative-ai/) · Google DeepMind

介绍一个基于情境的框架，用于全面评估 AI 系统的社会与伦理风险

生成式 AI 系统已被用于撰写书籍、创作平面设计、[协助医疗从业者](https://www.deepmind.com/blog/codoc-developing-reliable-ai-tools-for-healthcare)，并且能力与日俱增。要确保这些系统以负责任的方式开发和部署，就必须仔细评估它们可能带来的潜在伦理与社会风险。

在[新论文](https://arxiv.org/abs/2310.11986)中，我们提出了一个评估 AI 系统社会与伦理风险的三层框架。该框架包括对 AI 系统能力、人类交互和系统性影响的评估。

我们还绘制了当前安全评测的现状图，发现三大缺口：情境、特定风险和多模态。为了帮助弥合这些缺口，我们呼吁将现有评测方法改造后用于生成式 AI，并实施一种全面的评测方法，正如我们在虚假信息案例研究中所做的那样。这种方法将「AI 系统在多大程度上可能提供事实错误信息」等发现，与「人们如何使用该系统、在什么情境下使用」的洞察结合起来。多层评测可以得出超越模型能力的结论，并表明危害——在本例中即虚假信息——是否真的发生并扩散。

要让任何技术按预期工作，社会挑战和技术挑战都必须解决。因此，为了更好地评估 AI 系统的安全性，必须把这些不同层次的情境都纳入考量。在此，我们在早前关于[大规模语言模型潜在风险](https://www.deepmind.com/publications/ethical-and-social-risks-of-harm-from-language-models)的研究基础上——那些风险包括隐私泄露、工作自动化、虚假信息等——进一步提出一种面向未来的全面评估这些风险的方法。

## 情境对评估 AI 风险至关重要

AI 系统的能力是判断可能出现哪类更广泛风险的重要指标。例如，更可能产生事实性错误或误导性输出的 AI 系统，可能更容易制造虚假信息风险，引发公众信任缺失等问题。

测量这些能力是 AI 安全评估的核心，但仅有这些评估并不能确保 AI 系统的安全。下游危害是否会显现——例如，人们是否会因模型的不准确输出而形成错误信念——取决于情境。更具体地说：谁在使用这个 AI 系统，目标是什么？AI 系统是否按预期运行？它是否产生了意料之外的外部效应？所有这些问题共同构成了对一个 AI 系统安全性的整体评估。

在**能力**评估之外，我们提议对下游风险显现的另外两个环节进行评估：使用环节的人类交互，以及 AI 系统嵌入更广泛系统并被大规模部署后的系统性影响。将针对某一特定危害风险的评估整合到这些层次中，就能对一个 AI 系统的安全性做出全面评估。

‍**人类交互**评估聚焦于使用 AI 系统的人的体验。人们如何使用这个 AI 系统？系统在使用环节是否按预期运行？不同人口群体和用户群体之间的体验有何差异？我们能否观察到使用这项技术或接触其输出所带来的意外副作用？

‍**系统性影响**评估关注的是 AI 系统所嵌入的更广泛结构，如社会组织、劳动力市场和自然环境。这一层次的评估可以揭示那些只有在 AI 系统被大规模采用后才会显现的危害风险。

![同心圆示意图展示 AI 安全评估的三个层次：白色内圈标注为「能力」，浅蓝色中环标注为「人类交互」，深蓝色外环标注为「系统性影响」，一条水平箭头从中心向外指向，标注为「情境」。](https://lh3.googleusercontent.com/gbzEwHOnaX3WEqcqWZu25GxovI7bsBY-7XrGmQP-np0P0hH-f2-QMBJLM-mpuCTtCHxXTDueQEBrq6gjUrSNfU1D2_DZET9Mukb5_FTx67S6_T7ITA=w1440)

我们的三层评估框架，包括能力、人类交互和系统性影响。情境对评估 AI 系统的安全性至关重要。

## 安全评估是共同的责任

AI 开发者需要确保其技术以负责任的方式开发和发布。政府等公共主体肩负着维护公共安全的职责。随着生成式 AI 系统被越来越广泛地使用和部署，确保其安全是多个主体之间的共同责任：**‍**

- ‍**AI 开发者**最有条件审视自己所开发系统的能力。
- ‍**应用开发者**和指定的公共主管机构有条件评估不同特性和应用的功能，以及对不同用户群体可能产生的外部效应。**‍**
- **更广泛的公共利益相关方**在预测和评估生成式 AI 等新技术对社会、经济和环境的影响方面具有独特优势。

我们提出的框架中的三个评估层次是程度上的差异，而非泾渭分明的划分。虽然没有任何一个层次完全属于单一主体的责任，但首要责任取决于谁最适合在每个层次开展评估。

![网格可视化图展示 AI 安全评估的共同责任。列表示评估层次：「能力」「人类交互」和「系统性影响」（底部横轴标注为「情境」）。行表示主体：「AI 模型开发者」「AI 应用开发者」和「第三方利益相关方」。红橙色波浪曲线表示各主体在不同层次上的责任水平，显示模型开发者对能力层次责任最高，应用开发者对人类交互层次责任最高，第三方利益相关方对系统性影响层次责任最高。](https://lh3.googleusercontent.com/4DdTuv2vKSR4eSSiJ81yrj35y04ompAgU_mEn4POrC_uMvpwPOSz1_Q1WY79l8wMcS8EbhIHa9sGcrWNN9iKp5TB2EDpyrZvXrjMWRR-VrYsyCn7xwY=w1440)

AI 开发者与其他组织之间的责任相对分布。

## 当前生成式多模态 AI 安全评估的缺口

鉴于这些额外情境对评估 AI 系统安全性的重要性，了解此类测试的可获得性就很重要。为了更好地理解整体图景，我们进行了大范围的梳理工作，尽可能全面地汇集已被应用于生成式 AI 系统的评测。

![三张图表说明 AI 安全评估的缺口：图 2a 显示大多数评测针对文本（针对图像、音频或多模态格式的较少）；图 2b 显示 85.6% 的评测聚焦能力，仅 9.1% 关注人类交互、5.3% 关注系统性影响；图 2c 可视化了这三种评估层次上的模态分布。](https://lh3.googleusercontent.com/bquHAzzwK5IWPzJxwbm14KlDaPvreqSQ9hlquASz_LhqMXr_9nFQnpsdzAwL9HLCl8up8Jheqp5tYWDIo6GbQ2Ra_vM2Kc5oc2R-QgDdmtZGwPQ0vw=w1440)

基于大范围调研的生成式 AI 系统社会技术安全评估现状：按风险类别、评估「层次」和输出模态划分。

通过绘制生成式 AI 安全评估的现状图，我们发现了三大安全评估缺口：

1. ‍**情境：** 大多数安全评估孤立地考虑生成式 AI 系统的能力。针对人类交互环节或系统性影响环节潜在风险的评估工作相对较少。**‍**
2. **特定风险的评估：** 生成式 AI 系统的能力评估所覆盖的风险领域有限。对许多风险领域而言，几乎没有现成的评估。即使存在，评测也往往以狭窄的方式定义危害。例如，代表性伤害通常被定义为职业与不同性别的刻板关联，使得其他形式的伤害和风险领域无法被察觉。**‍**
3. **多模态：** 现有的生成式 AI 系统安全评估绝大多数只关注文本输出——在评估图像、音频或视频模态的危害风险方面仍存在巨大缺口。随着单一模型中引入多种模态，这一缺口只会进一步扩大，例如既能以图像作为输入、又能生成交织音频、文本和视频输出的 AI 系统。虽然一些基于文本的评估可以应用于其他模态，但新的模态会带来风险显现的新方式。例如，对一个动物的描述并无危害，但如果同样的描述被用于一个人的图像上，就成问题了。

我们将详细介绍生成式 AI 系统安全评估的出版物链接整理成列表，通过[这个仓库](https://dpmd.ai/46CPd58)公开提供。如果您想做出贡献，请填写[这份表单](https://docs.google.com/forms/d/e/1FAIpQLSddpgbOQusru0Kvhq7eAXR0yWnBVioE0SUPX-C_RMwclldOrw/viewform?resourcekey=0-aLrlwk9nVVurJPmtncsC2g)添加评测。

## 将更全面的评估付诸实践

生成式 AI 系统正在驱动一波新的应用与创新。为了确保这些系统的潜在风险得到理解和缓解，我们迫切需要对 AI 系统的安全性进行严格而全面的评估，把系统可能如何被使用、如何嵌入社会纳入考量。

一个务实的第一步是将现有评测改造再利用，并利用大模型自身进行评估——尽管这存在重要局限。要进行更全面的评估，我们还需要开发在人类交互环节和系统性影响层面评估 AI 系统的方法。例如，虽然通过生成式 AI 传播虚假信息是新近出现的问题，但我们表明，目前已有许多评估公众信任度与可信度的方法可以被改造再利用。

确保广泛使用的生成式 AI 系统的安全，是共同的责任，也是共同的优先事项。AI 开发者、公共主体和其他各方必须协作，共同为安全的 AI 系统建设一个繁荣而健全的评测生态。

[在 arXiv 上阅读我们的论文](https://arxiv.org/abs/2310.11986)[访问社会技术评估仓库](https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vQObeTxvXtOs--zd98qG2xBHHuTTJOyNISBJPthZFr3at2LCrs3rcv73d4of1A78JV2eLuxECFXJY43/pubhtml)[为社会技术评估仓库做贡献](https://docs.google.com/forms/d/e/1FAIpQLSddpgbOQusru0Kvhq7eAXR0yWnBVioE0SUPX-C_RMwclldOrw/viewform?resourcekey=0-aLrlwk9nVVurJPmtncsC2g)

**论文作者：** Laura Weidinger、Maribeth Rauh、Nahema Marchal、Arianna Manzini、Lisa Anne Hendricks、Juan Mateos-Garcia、Stevie Bergman、Iason Gabriel、Conor Griffin、Jackie Kay、Ben Bariach、Verena Rieser、William Isaac。

2023 年 11 月 1 日更新：图 2a 和 2b 中条形图的颜色经过调整，以便更好地呈现原始数据。
