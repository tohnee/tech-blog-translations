---
title: "Claude 发现具有类 CRISPR 重复序列的新型酶系统"
title_en: "Claude discovers a novel enzyme system with CRISPR-like repeats"
source: https://www.anthropic.com/news/claude-discovers-novel-enzyme-system
published: 2026-09-23
crawled: 2026-09-24
translated: 2026-09-24
---

# Claude 发现具有类 CRISPR 重复序列的新型酶系统

> 原文：[Claude discovers a novel enzyme system with CRISPR-like repeats](https://www.anthropic.com/news/claude-discovers-novel-enzyme-system) · Anthropic News

科学

# Claude 发现具有类 CRISPR 重复序列的新型酶系统

2026 年 9 月 23 日

![视频封面图](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F4zrzovbb%2Fwebsite%2F394de337d8a5d8db93a1c048fa1cb53e16a09625-2048x1240.jpg&w=3840&q=75)

*我们在 Anthropic 成立了一个新的生命科学研究团队和实验室。我们的重点是利用 Claude 开展基础生物学研究：探索 DNA 数据集以识别未表征的蛋白质家族，大规模生成假设，并通过实验室实验加以检验。本文介绍了这项工作背后的团队，并分享早期成果——在科学家仅提供高层次方向性指导的情况下，Claude 发现了一种性质令人联想到 CRISPR 的新型酶系统。*许多彻底改变了生物学与医学的发现，都始于科学家在自然界令人惊叹的分子机器多样性中注意到某种异样之物。限制性内切酶（restriction enzyme）是一类在特定短序列处切割 DNA 的蛋白质，发现于细菌免疫系统之中——在那里，它们摧毁入侵病毒的 DNA。研究人员意识到，可以用这些酶在选定的位置切割 DNA，把一个生物体的基因拼接进另一个生物体，生物技术产业由此诞生。Taq 聚合酶是一种能在高温下复制 DNA 的酶，是从黄石公园一处温泉中的细菌里鉴定出来的。它后来成为 PCR 的基础——这种 DNA 复制方法被大量用于现代诊断。CRISPR 最初只是被注意到是某些细菌 DNA 中一段不同寻常的重复序列，如今已成为基于基因编辑的药物的基石。

2026 年春，我们组建了一个研究团队，想看看通用 AI 模型能否将这类发现系统化并[加速此类发现](https://darioamodei.com/essay/machines-of-loving-grace#1-biology-and-health)。我们相信，这种加速将来自建立一种全新的生物学研究方式——智能体（agent）在流程的每一步都与人类协作。而要发展这种新的工作方式，就需要我们建立自己的实验室，并组建一支单一团队，负责从训练 Claude 的生物学能力到在实验室里开展实验的所有环节。

今天，我们分享首批研究项目之一的早期成果：Claude 自主发现了一种与一串 DNA 重复序列相关联的新型酶系统——这一模式令人联想到 CRISPR。虽然我们还不知道它的功能，但 Claude 发现的这个系统具备一组特征，此前只有在寥寥几个其他系统中才同时出现过，而所有这些系统都是可编程的，能够执行切割、复制和粘贴 DNA 之类的操作。除了已经变革了科学与医学的 CRISPR 之外，还有若干此类系统正作为前景可期的工具处于研发之中。

Claude 发现的这个系统基于逆转录酶（reverse transcriptase，RT）——一类把 RNA 复制成 DNA 的酶。虽然这个作为核心的 RT 此前已在一种巨型噬菌体（jumbo phage）中被鉴定出来，但 Claude 似乎是第一个注意到该系统决定性特征的：一段相关联的非编码 DNA 序列阵列，以及一个功能未知的额外辅助蛋白。

在审阅预印本之后，CRISPR 基因组编辑的先驱之一、MIT 与 Broad 研究所教授 Feng Zhang 表示：

> *这是一个 AI 智能体助力生物学发现的激动人心的例证。识别出与逆转录酶相关联的 RNA 重复序列阵列确实引人入胜，值得进一步研究。我希望这项工作能鼓励更多科学家去探索 AI 如何支持他们的研究。*

我们给 Claude 下达的提示，是让它在庞大的 DNA 序列数据库中搜索有趣的新 RT 实例。我们的参与仅限于最初的提示和实验室工作；而 Claude 智能体梳理数据库、考察各个不同的 RT 家族，并运用自己的判断来识别有价值的候选者。在大约 950 个智能体、耗费 2.1 亿个 token、历时 21 小时的数据搜索之后，其中一个智能体注意到了不同寻常的东西：一种重复出现的 DNA 序列模式，紧挨着一个样子古怪的 RT 的基因。经过进一步的分析和我们实验室中的测试，我们认识到这一模式标志着一个此前未表征的酶系统——它存在于噬菌体（即感染细菌的病毒）中，我们称之为阵列关联逆转录酶（array-associated reverse transcriptase，ART）。

我们理解 ART 主要功能的工作仍在继续。不过，我们认为尽早分享这类发现十分重要——既是为了展示 Claude 的能力，也是为了让更广泛的社区了解我们正在做的工作。我们已发布一篇预印本（[此处](https://www-cdn.anthropic.com/22573675ada52a8ca8a97a1a4b4326b2f208a071.pdf)），对其进行了更详细的讨论。

## **关于我们的实验室**

我们是一支由科学家组成的团队，整个职业生涯都在探索不寻常的蛋白质，尤其擅长运用计算方法系统地读取 DNA、解读其演化，并挑选出值得进一步表征的生物学系统。在加入 Anthropic 之前，我们的研究曾帮助更深入地理解 CRISPR 系统的[演化](https://www.science.org/doi/10.1126/science.aei0498)与[调控](https://www.nature.com/articles/s41586-018-0557-5)，发现可用于下一代[细胞与基因疗法](https://www.science.org/doi/10.1126/science.adz0276)的新[酶](https://www.nature.com/articles/s41586-024-07552-4)，并构建了加速识别 DNA 异常（例如人类致病变异）的[工具](https://www.nature.com/articles/s41586-026-10176-5)。我们是 Anthropic 生命科学组织的一员，与从事药物研发以及训练 Claude 生物学和化学能力的多个团队并肩工作。

我们的实验室位于旧金山湾区，看上去就是一个典型的分子生物学实验室。我们只开展生物安全风险等级中较低级别（BSL-1 和 BSL-2）的研究，不处理能够感染人类的病原体。所有实验室工作均由人类科学家完成。虽然我们尝试过通过 [Model Hardware Standard](https://www.anthropic.com/news/model-hardware-standard-research-preview) 之类的举措用 AI 加速实验室工作，但这种方式对我们分子生物学研究中涉及的那类即兴工作流程帮助不大。

## **我们的工作方式**

我们的许多工作流程，都是让 Claude 去搜索浩如烟海的、与功能未知蛋白质相关联的 DNA 序列。一种典型模式始于对某个特定蛋白质家族的普查。Claude 阅读相关文献，并用公开数据复现已确立的结果，以检验自己的方法。随后，它搜索那些不属于任何已描述系统的家族成员或基因组邻近序列，并为每个候选者撰写一份简短、人类可读的报告，提出功能假设并描述支持其论断的证据。在后续分析中，Claude 会批判性地评估证据——通常大多数候选者都会在这一阶段被淘汰。一次普查的结局，可能只剩下一个值得测试的候选者，也可能一无所获。

当一个候选者通过了我们的评审，我们就会在实验室中检验它：在标准实验室菌株中表达该蛋白，并对它进行生化和结构表征，同时由 Claude 协助解读数据。我们在 [Claude Science](https://claude.com/product/claude-science) 和 [Claude Code](https://claude.com/product/claude-code) 中开展工作——任何科学家都可以使用同样的工具——有时还会借助自研的执行框架（harness）来协调大量并行运行的 Claude 会话。

由于 Claude 生成假设又快又多，这些假设本身也成了我们的研究对象。一次研究行动会产出数百到数千份候选报告，我们一直在追问：那些被我们判定值得检验的提议，与我们搁置一旁的提议之间，区别究竟在哪里？我们学到的东西会回馈到给 Claude 的指令之中，教它模仿我们自己的科学品味。

## **Claude 发现 ART**

过去几年，研究人员发现了更多的逆转录酶（RT），其中大多数存在于细菌中，作为免疫系统的一部分发挥作用。几乎所有 RT 家族都是通过基因组分析（即基因组挖掘，genome mining）发现的——这要求研究者在序列数据库中搜索尚无人表征的基因，留意其中不寻常的成员，并弄清它们的功能。

Claude 智能体收集了超过 20 万个 RT，从中挑出 3500 个新的候选系统，再收窄到 20 个最具说服力的候选者进行分析，并生成人类可读的报告。对一位专家级科学家来说，这类分析可能需要数周到数月的工作量。

在研究过程中，Claude 注意到一个不同寻常的 RT 家族，决定对它做更细致的考察。在梳理该 RT 附近的原始 DNA 序列时，这个智能体惊呼："[RT 旁边的 DNA] 太壮观了：我一眼就能看出一个串联重复序列阵列……那是个类 CRISPR……重复序列阵列？！"

![Claude 在 DNA 中识别模式的示意图](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F0f6064436a364b73ce0d2a80848ac56be7ae9ddd-1360x1160.gif&w=3840&q=75)

*Claude 检测到无人注意过的重复模式时正在阅读的原始 DNA*

接下来，它的做法与面对潜在发现的人类科学家几乎如出一辙。它清点重复序列的数目、测量它们的间距，把这种排布与已知的 RT 系统进行比较，并检索文献，查找此前是否有人报道过这一模式。经过彻底的分析，它确信自己发现了一个新的生物学系统，于是提交了一份报告供人类审阅。

它发现的这个系统——ART——主要存在于噬菌体中，由三部分组成：RT、紧邻其旁的一个搭档基因，以及一长串等间距排布的 DNA 重复序列。这种重复排布类似 CRISPR 阵列——后者保存着一批不同的 RNA 序列，正是它们让 CRISPR-Cas 系统成为可编程的生物技术工具。我们的首批实验表明，ART 阵列同样会被表达为一组各不相同的短 RNA，这暗示该系统可能也在以类似的方式发挥作用。

进一步的实验正在进行，以确定 ART 的工作机制。我们分享这些早期发现，是想向社区展示：Claude 能够自主检测异常并主导分析，从而开启生物学发现。

更多细节请参阅我们的技术报告（[此处](https://www-cdn.anthropic.com/22573675ada52a8ca8a97a1a4b4326b2f208a071.pdf)）。

## **加入我们**

我们希望这项工作能向更广泛的科学社区展示 AI 驱动的假设生成的价值，也希望与其他科学家合作，把这一方法拓展到基因组学以及其他领域的各种问题上。如果你有关于研究问题的提案，我们乐意倾听。

## 相关内容

### 与 Accenture 合作开展嵌入式评估

[阅读更多](https://www.anthropic.com/news/accenture-embedded-evaluation)

### 介绍生命科学验证计划

生命科学验证计划（Life Sciences Verification Program，LSVP）让生命科学从业者能够使用 Claude Mythos、Opus 和 Sonnet 模型，并配备一套经过细化调整、对生物学相关工作更为宽松的防护措施。

[阅读更多](https://www.anthropic.com/news/life-sciences-verification-program)

### 与客户共同开发企业级前沿防护措施

[阅读更多](https://www.anthropic.com/news/enterprise-frontier-safeguards)

## 订阅 Anthropic Science

聚焦 AI 辅助的科学发现、实用工作流程，以及横跨各门科学的实地手记。
