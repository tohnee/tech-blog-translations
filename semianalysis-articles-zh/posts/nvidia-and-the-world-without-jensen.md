---
title: "Nvidia 与没有黄仁勋的世界"
title_en: "Nvidia and the World Without Jensen"
subtitle: "NVIDIA 是否已经完了？出口管制、RASA、开源影响、供应链影响、绯闻、美国仍依赖中国"
date: 2026-11-12
source: https://newsletter.semianalysis.com/p/nvidia-and-the-world-without-jensen
crawled: 2026-11-16
authors: ["Dylan Patel", "Doug", "Wayne Ma", "Jordan Nanos"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-11-16
---

# Nvidia 与没有黄仁勋的世界

> 原文：[Nvidia and the World Without Jensen](https://newsletter.semianalysis.com/p/nvidia-and-the-world-without-jensen) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**NVIDIA 是否已经完了？出口管制、RASA、开源影响、供应链影响、绯闻、美国仍依赖中国**

[黄仁勋（Jensen Huang）已不再是 Nvidia 的 CEO](https://nvidianews.nvidia.com/news/nvidia-announces-ceo-transition)。Nvidia 董事会此前一直在调查黄仁勋的行为操守，并权衡他在自己创办的这家公司的去留；显然，行为问题确实存在——与一个身为中共资产的中国客户、以及多名下属保持关系，在道德上是有问题的。

此外，我们认为他在短短四天后辞职，背后还有更多因素。我们认为这与大规模的 GPU 走私直接相关。我们的[加速器模型](https://semianalysis.com/accelerator-hbm-model/)追踪每一颗 AI 芯片的生产与去向，[数据显示超过 1.5GW](https://semianalysis.com/accelerator-hbm-model/) 的受限 Nvidia 芯片最终仍流入了中国。这个数字甚至还不包括 [Nvidia 为规避美国规则而专门设计的芯片——那篇报道最初正是由我们独家披露的](https://newsletter.semianalysis.com/p/nvidias-new-china-ai-chips-circumvent)。

我们认为，美国情报界是推动黄仁勋离开 Nvidia 的重要力量。具体而言，我们相信已在众议院通过的《远程访问安全法案》（Remote Access Security Act，RASA）或类似立法很可能继续推进。随着黄仁勋这位最大的辩护者离场，针对中国的 AI 与芯片限制将大大加速。我们坚定支持实施某些限制，但设计拙劣的限制会损害美国利益。

这类立法将带来后果，而我们认为政客们并未想清楚。

以下是当前体制的明显好处——中国实验室可以远程（而非在中国境内）使用 GPU：

- 利润流向美国公司。
- 美国可以监控中国实验室的动向。
- 只要愿意，美国几乎可以瞬间通过政治手段或强制手段切断它们对 GPU 的访问。
- Nvidia、AMD、Broadcom、Google、Amazon、Microsoft、Meta、Supermicro 和 Dell 等美国公司，其供应链都依赖中国公司。
- Nvidia 和 AMD 等美国公司雇佣中国工程师（明确一点：他们住在中国）为 GPU 系统开发硬件与底层软件。没有这些工程师，我们确信这些 GPU 的用户体验会明显不如今天。
- 美国公司，尤其是整个创业生态，受益于中国公司、学生和独立研究者今天使用这些 GPU 所发表的开源研究。
- 中国使用国产加速器的动力（哪怕只是略微）更低。
- 来自中国的创新通过宽专家并行（wide expert parallelism）、开源内核库（MSA、DeepEP、DeepGEMM 等）等开放创新流向全球。

话虽如此，我们确实支持对华实施部分 AI 限制，但其形态应更接近 MATCH Act 而非 RASA。拜登式的扩散规则最合理。

也许最重要的一点是：**开源正遭受攻击**。Nvidia 直接与中国实验室合作开源、帮助他们优化 GPU 与模型，这已是公开的秘密。这些实验室使用 Blackwell GPU，而 Nvidia 心知肚明。美国的开源生态和许多创业公司依赖中国的 AI 模型。随着黄仁勋离场、对华鹰派获胜，这一点将受到严重削弱。

但对股东（以及 AI 供应链）真正重要的问题是另一个：没有黄仁勋的 Nvidia 是什么？

我们的看法是：这家公司从来就不是为「他不在」而建的。他掌舵 33 年，即便董事会施压让他离开（或者是他「辞职」），黄仁勋留任对 Nvidia 而言仍会明显好于离开。这家公司是专门为这个人量身打造的，独一无二。没有这个人的公司，可能完全是另一头怪兽。SpaceX 和 Tesla 离开 Elon 就运转不了，Nvidia 离开黄仁勋也运转不了。

## 一位国王，60 名直接下属

对于这种规模和体量的公司，Nvidia 的公司结构相当古怪。根据黄仁勋的公开表态，他大约有 60 名直接下属。他曾说过，CEO 应该拥有最多的直接下属，因为这些人需要的管理最少，而且他不与他们进行一对一会议。

但其中很少有人能在没有黄仁勋的情况下做事。公司像一个王国一样运作，只有一位国王，其他人无论资历多高，都是听命于他的小卒。黄仁勋说过，谁向谁汇报并不重要，因为头衔与工作的重要性无关；这也是 Nvidia 成为「世界上最小的大公司」、员工人数少得多（约 42,000 人）却拥有巨大市值的原因之一。因此，Nvidia 内部的办公室政治更少。黄仁勋说，这种扁平网络赋予员工权力，让公司能够更快适应，因为其技术也在快速演进。

这是 Nvidia 行动迅速的原因之一。一旦黄仁勋定下方向，所有人便一起朝那个方向行动。前员工告诉我们，产品开发和工程工作常常持续到最后一刻，这样公司在需要时可以改变主意。例如，一位前高管告诉我们，GB200 的设计定稿时间比任何人希望的都更接近产品周期。黄仁勋说过，他希望能把公司永远保持在创业公司模式。

然而，这种结构的代价是 Nvidia 没有深厚的接班人选储备。看看 Nvidia 的网站：在他的直接下属中，只有五人被突出展示，其中两人是法务和财务高管。他的大多数直接下属没有受过面对聚光灯的训练，也被积极劝阻去寻求关注。很少有人离开去担任其他大公司的 CEO，Arm 的 Rene Haas 是罕见的例外。Nvidia 内部很少有人有机会在外部大放异彩，因为所有重大决策都由黄仁勋做出。但 Nvidia 高管团队的多数人并不介意，因为「欲戴王冠，必承其重」，而且许多人乐于待到退休年龄，因为他们薪酬优厚、受到善待，并且相信使命和自己的领袖。

## 没人想要这份工作

Colette Kress 已被任命为临时 CEO，但 Nvidia 正在寻找一位正式 CEO。这个人不能有财务背景。技术方面浮出水面的明显内部人选是 Ian Buck 和 Jonah Alben。Buck 在斯坦福读博期间的研究催生了 CUDA，他于 2004 年加入 Nvidia，目前作为超大规模与高性能计算副总裁负责数据中心业务。黄仁勋出差时，他经常被委以负责事务，也经常在会议上演讲。

Alben 自 1997 年起就在 Nvidia，是 GPU 工程高级副总裁，负责公司 GPU 的设计。但现实地说，没有人能独自掌管一切。我们认为 Buck 没有能力掌管技术硬件工程那一摊。Alben 及其团队中的其他人拥有技术自主权，但即便是他，也无法控制整个芯片侧——那里还有其他负责多个主要技术和业务部门的高级领导也直接向黄仁勋汇报。两人都很出色，但恐怕都无法施展黄仁勋那种对供应链的掌控力。

还有一个问题：是否有人想做 CEO 这份工作。今年早些时候，一位高管告诉我们：「Ian 宁可死也不愿接替 Jensen，他不想干那份工作。Jonah 更受尊敬，人们说他有能力，但话说回来，没有人真的想要那份工作。」不过，情况显然已经改变。Kress 是临时 CEO，但要让 60 多位副总裁拧成公司的一个统一愿景，需要特定类型的人，否则公司的方向就有消解为噪音的风险。

## 创始人式赌注熬不过职业经理人

黄仁勋是最后一批老派科技创始人之一，与 Elon Musk 同代，比 Mark Zuckerberg 稍年长。与 Nvidia 一同成长起来的其他公司——AMD、Google、Microsoft、Apple 和 Amazon——都已过渡到职业经理人管理。

Nvidia 的成功依赖于需要数年乃至十年才能回报的大赌注。得到董事会全力支持的创始人可以承担这些风险，而不必担心被造反。CUDA 亏损多年，华尔街分析师不断质疑，但黄仁勋坚持住了，这个赌注获得了巨大回报。正如一位前员工所说：「Jensen 把整个公司押在可编程着色器、CUDA 和张量核心上，尽管当时很多人反对把晶体管花在用途有限的这些东西上。」

Omniverse 和自动驾驶是 Nvidia 内部的新赌注。前员工告诉我们，黄仁勋在内部称它们为「零亿美元赌注」。它们今天不赚钱，但他认为它们和 CUDA 一样大。他还基于「Nvidia 需要理解客户才能设计更好的产品」这一理念，打造了 Shield TV 消费娱乐盒子和 DGX Cloud 服务——即便这两项业务几乎或完全不赚钱，最终也被搁置。

不是创始人的 Nvidia 继任者，无论在公司待了多久，都会以不同的方式对董事会和股东负责。这类长期赌注和信念将变得远不那么可能；而最大的问题之一，是黄仁勋传奇般的「造王」与交易能力，这很难复制。

## 客户买的是黄仁勋，不只是 GPU

在向超大规模云厂商及其他所有人分配芯片这件事上，黄仁勋是最终决定者。客户总是在争夺配额、争取 Nvidia 的关注，而 Nvidia 越来越多的交易需要它提供大量支持。正如我们[在 7 月所写](https://newsletter.semianalysis.com/p/nvidia-gpu-debt-backstop-unleashes)，Nvidia 可以选择把更多产能分配给超大规模云厂商、新兴 GPU 云（neocloud），还是分配给参与其兜底计划的新兴 GPU 云——在该计划中，它为集群提供信用支持，并分享云收入的一部分。这家「Nvidia 央行」以黄仁勋的全部信用为后盾。下一任 CEO 不太可能做出黄仁勋那样的豪赌。

Nvidia 喜欢基于「什么是可行的」来做决定，但很多决定最终取决于「什么具有战略意义」。跳过超大规模云厂商，或者与它们合作并给予优待，并不总是具有战略意义。这些客户中的许多人现在需要得到保证：他们将继续通过财务担保或配额获得 Nvidia 的支持。Nvidia 披露，截至其财年第二季度，[表外担保总额为 $530B](https://newsletter.semianalysis.com/p/nvidias-backstop-universe-heads-i)，高于上一季度的 $184B，其中包括新兴 GPU 云产能下 $36B 的照付不议下限；此外它还持有 $99B 的股权账本。

许多客户想与黄仁勋达成交易，原因也超出数字本身。世界各地的新兴 GPU 云能融到钱，是因为黄仁勋为它们背书，而不是因为它们比较了芯片之后选择了 Nvidia。[Nvidia 的兜底](https://newsletter.semianalysis.com/p/nvidias-backstop-universe-heads-i)让新兴 GPU 云和新兴实验室（neolab）无需超大规模云厂商就能融资：它在第一天以全额利润卖出 GPU，然后为买方的收入兜底、为买方的房东提供担保，或干脆自己签下租约，让没有投资级评级的运营商也能以投资级定价借款。如果没有「黄仁勋看跌期权」（Jensen put），这个生态可能会大幅收缩。

## 供应链的扼喉之手松动

Nvidia 对其供应商拥有扼喉般的控制。如果竞争对手能拿到供应，它们的出货量会高得多。但它们拿不到，因为黄仁勋亲自锁定了韩国的存储器和台湾的芯片。正如我们在[《AI 硅短缺大危机》](https://newsletter.semianalysis.com/p/the-great-ai-silicon-shortage)中所写，Nvidia 已锁定逻辑晶圆、存储器及其他多种必需组件的大部分供应；黄仁勋 2025 年的韩国之行就是为了确保存储器供应——那时其他高管还没完全意识到存储器短缺有多严重。我们的产业客户曾认为我们[对 2026 年的预测](https://semianalysis.com/memory-model/)过于激进，但后来他们意识到我们是对的。Nvidia 的供应与产能承诺[在单个季度内从 $119B 跃升至 $279B](https://newsletter.semianalysis.com/p/nvidias-backstop-universe-heads-i)，主要用于存储器。

这种扼喉是私人关系式的。这些交易是黄仁勋以 CEO 对 CEO 的方式，与全球主要供应链公司谈成的。在韩国，[我们估计](https://newsletter.semianalysis.com/p/koreas-trillion-dollar-sovereign) SK 海力士 2027 年 HBM4 对 Nvidia 的定价约为每 Gb $3.0 至 $3.3，而对 AMD、Broadcom、Amazon 和 Google 等其他一级客户为每 Gb $3.7 至 $4.1；我们相信存在一种默契：作为回报，Nvidia 给予 SK 集团优先的 GPU 配额。没有他，这些公司将不再以同等程度优先考虑 Nvidia，其他厂商也会更容易获得产能。我们认为，[2028 年总产能中可能有超过 70% 属于非 Nvidia](https://semianalysis.com/accelerator-hbm-model/)。

更重要的是，除了扼住供应，正是黄仁勋的愿景推动台湾供应链比任何人都更用力地投资、更坚定地相信这轮建设潮。黄仁勋传奇般的供应链晚宴与承诺，推动台湾供应商交付在技术和物流上都极具野心的计划。

## AI 产业失去其开源代言人

没有黄仁勋，AI 产业就失去了首席代言人。他无处不在，作为 AI 的首席拥护者为其发声。他是 AI 的门面，无人可以替代。

黄仁勋还制定了 Nvidia 的中国政策，并主导推动开源 AI 模型——这些模型让国家、企业和新兴 GPU 云有理由购买 GPU，而不只是那几家如今正在自研芯片的前沿实验室。

正如我们[在 9 月所写](https://newsletter.semianalysis.com/p/koreas-trillion-dollar-sovereign)，没有人比 Nvidia 更需要开源 AI：它正走向一个只有两个真正客户（Anthropic 和 OpenAI）、或者算上超大规模云厂商共七个客户的世界，而这七家除 SpaceX 外都在试图自研 XPU，以蚕食 Nvidia 的利润率。AI 模型与应用是其 GPU 的互补品。

中国前沿实验室使用 Blackwell GPU、NVIDIA DevTech 与中国前沿实验室密切合作并从其终端用户身上学到很多——这已是公开的秘密；由此产生了宽专家并行、DeepGEMM、DeepEP 等 CUDA 生态创新。这些创新随后传播到西方开源社区和创业公司。这些创业公司将因他的离开受到巨大的负面影响。

**没有黄仁勋作为代言人、并为开放模型提供财务和工程支持，中国实验室可能无法开源** MiniMax MSA、DeepGEMM、DeepEP、Moonshot 的 FlashKDA 等内核库——这些显然都是针对 NVIDIA Blackwell GPU 优化的。SGLang、vLLM 等全球广泛使用的许多生产级引擎都在使用中国实验室的这些创新。中国实验室可能不得不回到直接否认自己拥有任何 NVIDIA GPU 的状态，并把 NVIDIA 软件仅保留在内部，而不是开源 Blackwell 软件。

从根本上说，中国的创新不再在 NVIDIA 生态和整个机器学习生态中共享，这是糟糕的。这对闭源 AI 实验室是好事，对创业公司则是坏事。

[一家由职业经理人领导的公司，可能会降低表现不佳的 Nemotron 的优先级](https://x.com/SemiAnalysis_/status/2080005628177662109)。随着美国前沿实验室的许多模型转向闭源，Nvidia 曾凭借一己之力支撑着美国其他开源模型——通过投资 Reflection、Thinking Machines、Poolside 等公司，以及收购 Hugging Face。

Nvidia 是推动与中国持续接触的一方，其论点是：中国应当使用并依赖美国技术。正如我们[去年所写](https://newsletter.semianalysis.com/p/huawei-ascend-production-ramp)，在美国政府禁止 H20 进入中国、随后又表示将授予 Nvidia 出口许可之后，美国需要在「让中国留在美国 AI 技术栈上」与「减缓中国自研进度」之间取得平衡，同时还要限制流入中国的芯片质量与数量。那么，如果他推动这件事的出发点本身就已被攻破呢？这要由调查来判断。显然，对华鹰派正在获胜，所以我们不得不问一个有点奇怪的问题：为什么是现在？

## 为什么是现在，黄仁勋的私生活被曝光？

我们不是搞阴谋论的人，但同一时间前后发生的几件事，似乎构成了一个难以忽视的叙事。情报界从中获益良多。《纽约时报》关于此事的[第二篇报道](https://www.nytimes.com/2026/11/08/technology/nvidia-investigation-jensen-huang-china.html?unlocked_article_code=1.PFE.fo7y.MkcvWie9C2BI&smid=url-share)明确（五次）指出，其报道依据是美国情报界。Trump、Rubio 和 Lutnick 在 5 月访华之前就已知道这一切。更有报道称，[Lutnick 曾拖延对华芯片的打击行动](https://www.reuters.com/world/china/lutnick-stalled-trump-crackdown-diversion-nvidia-chips-china-axios-reports-2026-11-11/)。那段关系中的某些东西已经改变，如今风向正吹向另一边。

**我们其实并不认为 Alice Huang 是传统意义上的间谍。她是一位人脉广泛的商界女性。和中国任何其他人脉广泛的商界人士一样，她与中共有接触。**

我们的[加速器模型](https://semianalysis.com/accelerator-hbm-model/)追踪到超过 1.5GW 本不该出现在中国的 Nvidia GPU；美国商务部如今也终于相信，中国境内有超过 1.5GW 本不该在那里的 NVIDIA 芯片。现在，随着中期选举倒向民主党，有人认定是时候重拳出击了——既要阻止对现有出口管制的蓄意规避，也要扩大管制，彻底切断中国获取前沿芯片的渠道。

需要明确的是，Trump 政府在这个问题上存在分歧，但 Trump 此前在为 Lutnick 提供掩护。Trump 不再提供这种掩护。更重要的是，有一项关键法案《远程访问安全法案》（"RASA"）已在众议院通过，但尚未在参议院投票，而那场投票正在此刻进行。

## RASA 进入表决

RASA 于 1 月 12 日以 369 对 22 在众议院通过。它是以暂停议事规则动议的方式通过的，这需要三分之二多数。众议院外交事务委员会于 2025 年 4 月以 51 对 0 通过。尽管它被提交至参议院银行委员会，但尚未获得表决。我们知道 [NVIDIA 和 Oracle 一直在大力游说反对它](https://www.theinformation.com/articles/commerce-department-finalizing-long-awaited-ai-remote-access-rule)。

当然，RASA 不是美国政府阻止中国公司远程访问 GPU 的唯一方式。但 RASA 是当下华盛顿讨论的热门法案。它显然很受欢迎——已在众议院通过——而且法案的实质性条款在人们看来简直理所当然：凭什么允许中国公司远程访问它们不被允许进口的 GPU？

顺带一提，我们知道亚洲、澳大利亚、中东、北欧、欧洲、加拿大甚至美国的新兴 GPU 云都在积极向中国公司出售算力。它们都将受到这项法案的冲击。这是又一项全球性出口管制法案，且影响深远。黄仁勋——很可能还有 Lutnick——并**不**希望这件事发生。

所以，让我们逆着主流叙事，探讨一种可能性：尽管最近的头条新闻铺天盖地，**通过 RASA（或类似法案）将带来意想不到的后果**。按照关于美国政治的古老谚语，我们相信：如果所有政客都同意某件事，那它多半是个坏主意。

正如我们前面所说，以下是当前体制的明显好处——中国实验室可以远程使用 GPU：

- 利润流向美国公司。
- 美国可以监控中国实验室的动向。
- 只要愿意，美国几乎可以瞬间通过政治手段或强制手段切断它们对 GPU 的访问。
- Nvidia、AMD、Broadcom、Google、Amazon、Microsoft、Meta、Supermicro 和 Dell 等美国公司，其供应链都依赖中国公司。
- Nvidia 和 AMD 等美国公司雇佣中国工程师（明确一点：他们住在中国）为 GPU 系统开发硬件与底层软件。没有这些工程师，我们确信这些 GPU 的用户体验会明显不如今天。
- 美国公司受益于中国公司、学生和独立研究者今天使用这些 GPU 所发表的开源研究。
- 中国使用国产加速器的动力（哪怕只是略微）更低。
- 来自中国的创新通过宽专家并行、开源内核库（MSA、DeepEP、DeepGEMM 等）等开放创新流向全球。

明确一点：在一个中国实验室被完全切断 NVIDIA GPU 访问的世界里，它们都会更有动力摆脱 NVIDIA GPU，转向国产加速器。

而这在今天已经在发生。

- 2 月，Z.ai 宣称 GLM-5 已在七种国产加速器上支持推理。
- 4 月，DeepSeek 发表了 V4 论文，随后开源了面向华为昇腾 NPU 上 V4 Pro 模型的推理超大内核（megakernel）。
- 6 月，美团发布 LongCat 2.0，声称其完全在华为昇腾 910B NPU 上预训练。

![](https://substackcdn.com/image/fetch/$s_!UtrJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff874723d-e3ec-4d45-a21b-62f727d210fd_1794x274.png)

来源：[Z.ai 的 GLM-5 论文](https://arxiv.org/pdf/2602.15763)（[z.ai](http://z.ai)）

政客们始终没有意识到中国、台湾与美国之间的关系实际上有多么盘根错节。许多中国公民在前沿实验室工作。许多中国工程师受雇于 NVIDIA 和 AMD，编写底层代码以点亮新芯片。许多美国人从中国的开源贡献中学习。生产这些芯片所需的许多原材料来自中国。许多 L1-6 ODM 板卡与组件供应商都是中资企业。

紧张局势升级必将导致芯片产量减少，所有人的 AI 进展速度都会放慢。

我们认为，美国应当限制或管控向中国实验室交付多少算力；禁止对华出口、同时允许受信任的云提供远程访问，是实现这一目标的最佳方式。

拜登式的扩散规则最合理。

## 出口管制违规与执法

对于那些说 GPU 不可能被走私到中国、还在小红书上打广告出租的人——理由是它们太重、塞不进背包——我们不同意。

![](https://substack-post-media.s3.amazonaws.com/public/images/a6c503ef-733a-4d99-99e1-c5727322a277_648x668.png)
*来源：小红书上的广告，一个是出租 800 颗 RTX 5090 的 GPU 集群，另一个是中国境内最低 1,024 颗 GPU 起购。*

> *「我们已经研究过他们对我们 GPU 的所有部署，并逐一清点。没有任何 AI 芯片转移的证据。这些是庞然大物。Grace Blackwell 系统重近两吨，你不可能很快把它塞进口袋或背包里。重要的是，我们销售对象的国家和公司都认识到，转移是不被允许的，而且所有人都希望继续购买 Nvidia 技术。」——黄仁勋，2025 年 5 月 Computex*

自那以后，至少有两个高调的反例：价值 $2.5B 的服务器被 Supermicro 的 3 人走私；价值 $65M 的服务器被 NVIDIA、Supermicro、Albatron、Flying Tiger 和 Chief Telecom（一家台湾分销商、经销商兼数据中心运营商）的 9 人走私。

第一起 $2.5B 的案子主角是 Wally Liaw，SuperMicro 的联合创始人兼销售负责人。Wally 于 2026 年 3 月 17 日被起诉（US v. Liaw, 1:26-cr-00100, SDNY），同案被诉的还有 Steven Chang（台湾销售负责人）和 Willy Sun（台湾本地承包商）。起诉书称，价值 $2.5B 的服务器被卖给东南亚的一家公司，其中 $510M 随后被走私到中国。起诉书还称，Wally、Steven 和 Willy 在 2025 年 8 月的公司审计和 2025 年 12 月的商务部审计中，用假服务器摆样子蒙混过关。

起诉书里甚至附了一张照片：Willy Sun 和他的朋友用吹风机把标签和序列号贴纸从真服务器转移到假服务器上，以便通过审计。

![](https://substack-post-media.s3.amazonaws.com/public/images/8cdeed7d-9043-4c50-bfa4-cbf8eeeba2cd_1288x1256.png)

来源：<https://storage.courtlistener.com/recap/gov.uscourts.nysd.660027/gov.uscourts.nysd.660027.2.0.pdf>

![](https://substackcdn.com/image/fetch/$s_!Dn4S!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6206e8a-da41-4897-aac7-cedc8ac0397c_1294x234.png)

来源：<https://storage.courtlistener.com/recap/gov.uscourts.nysd.660027/gov.uscourts.nysd.660027.2.0.pdf>

自 3 月被起诉以来：

- Wally 已作无罪抗辩，将于明年 3 月 29 日受审（原定 11 月 2 日开始，但在 Supermicro 被纽约南区联邦检察官办公室传唤后延期，如其在 8 月 31 日提交的 [10-K](https://www.sec.gov/ix?doc=/Archives/edgar/data/1375365/000137536526000022/smci-20260630.htm) 中所述）。
- Willy 已就四项罪名认罪，包括布置假服务器、冒充名叫 Michael 的法律助理、在 2025 年 12 月的审计中对商务部官员撒谎，以及在被捕当天（3 月 19 日）从手机中删除一款加密通讯应用。他于 10 月 8 日认罪，量刑定于明年 9 月 8 日。
- Steven 目前被视为在逃。

![](https://substackcdn.com/image/fetch/$s_!elEx!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b13115e-614c-48e8-98a8-9d9a6cc4496d_1142x216.png)

来源：Supermicro 8 月提交的 [10-K](https://www.sec.gov/ix?doc=/Archives/edgar/data/1375365/000137536526000022/smci-20260630.htm)

接下来是台湾基隆的第二起案件。9 人（截至目前）因走私 130 台 B300 服务器被起诉，其中 74 台已于今年早些时候运抵中国：

- Chang Teng-lung，NVIDIA 台湾高级经理（关键人物）
- Lin 与 Wang，Supermicro 台湾销售经理
- Lu，Albatron（Supermicro 分销商）CEO
- Chen，Flying Tiger（服务器经销商）总裁
- Tsai，Chief Telecom（数据中心运营商）项目经理
- Yu，一家清关公司负责人
- Wang（第二位），一家服务器经销公司负责人
- 未具名的第九名被告，涉嫌从 Albatron 抽走资金

事情经过是：台湾海巡署在今年 5 月的一次缉毒调查中偶然发现这些服务器，并拘留了三人。随后他们搜查了另外 12 处地点，查扣 56 台服务器、豪车以及 NT$9M（约 $275k 美元）现金。

此后，来自 Supermicro、Albatron 和 Chief Telecom 的人员于 6 月被起诉，7 月 NVIDIA 的 Chang 被起诉，到 8 月 9 人全部到案。Chang 的首次听证会于 10 月 16 日举行。

被告被控使用空壳公司、伪造审计、伪造文件（包括伪造一个 Supermicro 网站用于申请出口许可），并将出口目的地申报为日本，再从那里转运至中国。

顺带一提，现行流程中，超过八台服务器的订单会触发 Supermicro 的现场检查。海巡署显然是在追查一起无关的缉毒案时偶然发现了这些服务器。这次检查发生在 Flying Tiger 于 2025 年 9 月申请并获得从 Supermicro 购买 130 台服务器的许可（以自己为最终用户）之后，且其在 Chief Telecom 的一个数据中心通过了现场检查。检查本应确认他们有足够的机架空间和电力来容纳这些服务器，但检方称该站点显然不满足这些要求——他们甚至连租约都没签。

以下是起诉书中的一张照片：托盘上的 Supermicro 服务器被警戒线围住，旁边有现金和一辆保时捷。

![](https://substack-post-media.s3.amazonaws.com/public/images/1c9d9a6e-5810-425b-b263-187a06f8c091_1284x950.png)

来源：基隆起诉书

![](https://substack-post-media.s3.amazonaws.com/public/images/765d9763-92a2-4904-bc7d-bcc842d5c033_952x656.png)

来源：基隆起诉书

这两起案件都在诉讼中。

## 情况可能比我们想的更糟

所以，如果一定要说「为什么是现在」，那很可能是为了扫清对一项极其鹰派的对华出口管制法案的反对：在国会大幅转向、并进入跛脚鸭会期之际，最好先把反对者挪开，好让法案通过。这是我们对局势最好的阴谋论式解读，而且与华盛顿传出的涟漪相吻合。那么，现在让我们回到最初的问题。

## 没有黄仁勋的 Nvidia 会是什么样？
