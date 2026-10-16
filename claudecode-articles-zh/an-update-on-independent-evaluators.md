---
title: "关于独立评估者的最新进展"
title_en: "An update on independent evaluators"
source: https://www.anthropic.com/news/an-update-on-independent-evaluators
published: 2026-10-15
crawled: 2026-10-16
translated: 2026-10-16
---

# 关于独立评估者的最新进展

> 原文：[An update on independent evaluators](https://www.anthropic.com/news/an-update-on-independent-evaluators) · Anthropic News

公告

# 关于独立评估者的最新进展

2026 年 10 月 15 日

![关于独立评估者的最新进展](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fc2af6aeedb4995d202c7543f3d59c6bbbd5352f1-2000x1125.jpg&w=3840&q=75)

上个月，我们承诺对我们的模型和安全实践开展[更有力的独立第三方评估](https://darioamodei.com/post/we-must-pace-the-frontier)。我们还签署了《白宫超级智能协议》（White House Accord on Super Intelligence），各签署公司均承诺与独立外部审计者或评估者合作。今天，我们要宣布：我们已开始给予 [METR](https://metr.org/) 一个团队「类员工」级别的访问权限。METR 是一家评估前沿 AI 模型的非营利机构。

METR 将公布其风险评估的结果。过去一年里，我们与 METR 合作，对我们的《风险报告》进行了[多轮审查](https://metr.org/risk-assessment/)。我们还在与 [SecureBio](https://securebio.org/) 和 [Accenture](https://www.anthropic.com/news/accenture-embedded-evaluation) 开展评估合作，并与包括 [Hugging Face](https://huggingface.co/) 在内的其他几家机构进行早期洽谈。

在本文中，我们将说明我们与评估者合作的思路。

## 我们为什么要与独立评估者合作

随着模型能力越来越强，它们也需要更坚固的防护措施和更具挑战性的风险评估。我们希望就自己正在做出的决定接受公众问责。但我们无法公开分享与安全工作相关的全部信息——其中一些可能被恶意行为者利用，另一些则属于商业敏感信息，例如算力或训练方面的信息。因此，我们选择让第三方评估者深度访问我们的信息，并请他们就构建我们的模型所涉及的风险分享证据和有理有据的结论。我们的目标是缩小这一差距：评估者对一家前沿 AI 公司系统的理解，与该公司自身理解之间的差距。

要评估前沿模型，评估者需要具备以下条件：

- *专业能力*：评估前沿模型能力方面的专业知识，包括理解评估可能出错的各种方式，例如[对齐伪装](https://www.anthropic.com/research/alignment-faking)（alignment faking）。
- *独立性*：他们不应持有被评估公司的股权，也不应在财务或运营上依附于该公司。
- 足够的*访问权限*，以便切实有效地评估风险。除了能够访问最新模型之外，评估者还需要了解这些模型是如何训练的、我们的防护措施如何运作等等。
- *公开发表的自由*：可以自由发布对某个模型或某项流程的观察与评估。

这个类比虽然并不完全贴切，但银行监管的运作逻辑与此类似。银行对自身风险头寸的了解多于外部人士，因此监管机构会派驻现场检查官进入规模最大的银行内部工作。如果一家银行的风险行为可能危及公众，第三方会力图提前察觉。

对 AI 行业而言，这是朝着[强健的安全监督](https://www-cdn.anthropic.com/files/4zrzovbb/website/0a58d567024a8b448ff15158ebc3625328dfcc1f.pdf)迈出的一步。我们正在与多家评估者快速推进，并积极总结哪类合作方式行之有效。我们承诺在此过程中持续分享进展。

## 我们所说的「类员工访问权限」是什么意思

我们已为六名 METR 成员办理了入职，为他们配备公司硬件和办公空间，并开放内部工具与系统的访问权限，其水平与我们自己的风险评估团队所拥有的权限大体相当。除了少数几个明确界定的类别（例如客户数据、受律师-客户保密特权保护的信息，或与我们模型架构有关的信息）之外，我们鼓励 Anthropic 员工像对待从事对齐风险研究的同事一样与他们共享信息。[1](#footnote-1)

METR 将公布它对我们的风险水平、事故或实践的分析。Anthropic 无法否决其发表，但如果相关信息属于上述那类狭窄且预先界定的类别，我们可以要求 METR 对信息进行删节。METR 可以自由地公开评价我们的删节行为，也可以说明它是否认为这些删节正当，前提是不披露被删节的信息本身。

我们与 METR 的合作仅限于一个小团队，其运作受可强制执行的协议约束。METR 的其他员工与该团队的工作相互隔离，包括在其他项目上与我们合作的研究人员。嵌入式评估（embedded evaluation）让少数具备资质、在 Anthropic 安全标准下工作的人员得以近距离观察我们的运作方式。它并不是其他组织获取我们的信息、或我们客户与合作伙伴信息的渠道。

## 我们的其他评估者合作

我们正在推进另外几项合作。由于这些合作仍处于早期阶段，我们向这些评估者提供的信息更为有限，它们的公开发表权限也更有限。这些早期合作的目标，是确认我们的合作伙伴能够保护机密信息，并具备评估我们模型所需的资源和专业能力。随着合作推进、信任建立，我们希望让更多独立评估者完整嵌入。

我们正在为评估者设计三个层级的访问权限。假以时日，我们希望有多家评估者进入第三层级，每个团队都公布各自对我们风险态势和关键决策的分析。

**第一层级**，评估者开展范围严格限定的风险调查。由我们决定向第一层级评估者提供哪些访问权限，评估者可以在获得我们批准后发表其发现。

**第二层级**，评估者无需我们的批准即可发表，而且能够访问更多信息。我们仍然可以要求移除特定类别的信息，不过评估者可以发表他们对我们的删节是否正当的看法。

**第三层级**就是我们上文与 METR 所描述的那种安排：拥有类员工级别的访问权限，公开发表权限则与第二层级类似。

**SecureBio** 正在审查我们[八月风险报告](https://www-cdn.anthropic.com/f61d49fa5596956a5dec75fea0e973bf6a6a8378/Redacted%20Risk%20Report%20August%202026%20.pdf)中的化学与生物武器章节；此前它已完成对我们上一份风险报告的[试点审查](https://securebio.org/resources/anthropic_feb_2026_risk_review.pdf)并公开发布。本轮审查完成后，我们将考虑推进访问权限更高的项目。[2](#footnote-2)

**与 Accenture** 和 Faculty，我们正在[推进一项雄心勃勃的合作](https://www.anthropic.com/news/accenture-embedded-evaluation)，内容包括对模型进行评估和红队测试（red-teaming）、开展对齐评估、测试模型防护措施，并在双方组织内建设相关能力。

我们是自愿嵌入评估者的，我们也相信每一家前沿 AI 公司都应当如此。

#### 脚注

1. 由于这些评估者（和银行检查官一样）可能同时与其他公司合作，我们对无意泄露的可能性保持谨慎。架构信息发生无意泄露的风险较高，而其与风险评估的相关性通常较低。当架构信息与风险评估高度相关时，我们一般会设法分享，但这需要经过明确的内部批准。
2. 2026 年 10 月 15 日更新，以澄清 SecureBio 与 Anthropic 当前项目的条款。

## 相关内容

### 为 2026 年美国中期选举做准备

今年早些时候，我们分享了选举防护措施的更新。本文概述了在今年美国中期选举临近之际，我们如何继续强化这些防护措施。

[阅读全文](https://www.anthropic.com/news/2026-us-midterms)

### Anthropic 开设新加坡办事处并与新加坡政府签署谅解备忘录

Anthropic 在新加坡开设了办事处，并与该国政府签署了谅解备忘录（MOU），以推动安全、负责任的 AI 应用。

[阅读全文](https://www.anthropic.com/news/singapore-office-opening)

### 2026 年使用政策更新

我们正在发布新一版《使用政策》（Usage Policy）。在这篇文章中，我们总结了所做的变更。

[阅读全文](https://www.anthropic.com/news/2026-usage-policy-update)
