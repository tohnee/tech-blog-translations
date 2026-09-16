---
title: "Arm 的核选项——若 Arm 得手，高通必须取消下一代产品"
title_en: "Arm’s Nuclear Option – Qualcomm Must Cancel Next-Generation Products If Arm Succeeds"
subtitle: "Arm 否认有关其更改商业模式的指控"
date: 2022-11-16
source: https://newsletter.semianalysis.com/p/arms-nuclear-option-qualcomm-must
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Arm 的核选项——若 Arm 得手，高通必须取消下一代产品

> 原文：[Arm’s Nuclear Option – Qualcomm Must Cancel Next-Generation Products If Arm Succeeds](https://newsletter.semianalysis.com/p/arms-nuclear-option-qualcomm-must) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Arm 否认有关其更改商业模式的指控**

如果你一直在追科技圈这场最盛大的连续剧，就知道 Arm 起诉了高通。高通最近提出了[相当重磅的反诉](https://www.semianalysis.com/p/is-arm-desperate-qualcomm-claps-back)，如果属实，[将意味着 Arm 正在改变其整个商业模式](https://www.semianalysis.com/p/arm-changes-business-model-oem-partners)。

[![](https://substackcdn.com/image/fetch/$s_!HwSb!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F0150776c-9bf2-4bea-a9c2-41b24b7a0f15_1280x1280.png)SemiAnalysisArm Changes Business Model – OEM Partners Must Directly License From ArmThe Qualcomm-Arm saga is epic and there is a new massive update in the case. This update contains evidence that Arm is changing its entire business model and moving to require licenses from OEMs. It also contains evidence of some hints at anti-competitive licensing behavior around GPUs, NPUs, and ISPs…Read more4 years ago · 36 likes · 15 comments · Dylan Patel](https://www.semianalysis.com/p/arm-changes-business-model-oem-partners?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

在这场十年一遇的「离婚大戏」的最新一集里，Arm 正在对高通的反诉作出答复与抗辩。Arm 在抗辩中的语气非常明确：Arm 全盘不接受高通的反诉主张，包括否认「Arm 正在更改其商业模式」的指控。

下面我们将带我们的观点总结这份抗辩，但最重大的进展是：Arm 正在威胁动用核选项。Arm 的核选项，就是以违约为由终止高通的架构许可协议。

> 高通实质性违反了其 ALA，这赋予 Arm 终止协议的权利；且高通的 ALA 并未为 Nuvia 技术的继续开发提供许可或权利。

Arm 要求高通停止开发 Nuvia Phoenix 核心，并威胁终止高通自己的架构许可协议（ALA）。

> 高通与 Nuvia 必须停止使用并销毁依据 Nuvia ALA 开发的任何基于 Arm 的技术，且高通与 Nuvia 均未获得继续开发该技术的许可。

高通主张其可以在自己的 ALA 之下继续开发 Nuvia 技术。如果高通的 ALA 被终止，将击沉高通目前正在开发的多款产品，横跨 PC、智能手机、AR、VR、汽车、5G 基站以及服务器 Orion SoC 等多条业务线。

> 高通的自主架构核心（包括高通从 Nuvia 收购的相关技术的所有进一步开发、迭代或具体实现）、服务器 SoC 与计算 SoC，均未在高通 ALA 或 TLA 下获得完整许可；相反，它们必须停用并销毁。

直到现在，Arm 此前还只是要求高通销毁 Nuvia 衍生的工作成果（包括 Phoenix 核心）。这本身就将导致多款产品延期以及高通产品路线图的大幅重构。

> 2022 年 4 月和 5 月，Nuvia 与高通明确承诺将履行销毁且不使用所界定的 Arm 技术与保密信息的义务。

高通在其诉讼文件中声称，已将 Nuvia ALA 下的专有 Arm IP 隔离，并用高通 ALA 下的 IP 取而代之。Arm 则主张，他们必须销毁在 Nuvia ALA 下做出的全部衍生成果。

> Arm 承认高通曾向 Arm 发送一封日期为 2022 年 5 月 23 日的函件，主张高通自身的 Arm 许可将允许其把「不受任何移除或隔离义务约束」的 Nuvia 技术整合进高通产品，但未说明有哪些（如果有的话）Nuvia 技术符合该描述。Arm 承认高通曾主张 Nuvia 已开发出不受终止要求约束的技术，但未解释这些技术是否衍生自在 Nuvia 许可下交付的 Arm 技术。Arm 承认高通的函件表明高通将在与 Nuvia 相同的程度上遵守终止义务，且未对 Arm 终止 Nuvia 许可提出异议。

争议的核心在于：分支预测器、FPU、乱序执行引擎、微操作解码器（Micro-Op Decoder）等 IP 究竟完全属于高通/Nuvia 的财产，还是 Arm 对这些 IP 拥有权利。高通主张只有指令集归 Arm 所有，而 Arm 认为 CPU 核心的这些组成部分（即衍生成果）同样受协议约束。

> Arm 否认「构建 CPU 所需的微架构知识与专长与 ISA 无关」这一主张。

高通声称所转移的 Nuvia IP 与 ISA 无关。这一主张正被 Arm 驳回。

虽然由于架构许可属于保密信息、我们无法阅读其原文，但 Arm 对这一条款似乎相当有把握。

> 高通未被授权制造、使用、销售或进口任何包含 Nuvia 技术之设计或衍生成果的产品。

终止高通的 ALA 将扼杀高通的自研核心计划，包括那些不含任何所收购 Nuvia IP 的从零开始的设计。即便高通能赢下「可在自己的 ALA 下继续开发 Phoenix 核心」这一论点，一旦高通的 ALA 同样被终止，他们也无法出货任何基于该核心的产品。

> 与其主张相反，高通无法继续使用基于 Arm 的技术，包括 Phoenix 核心。

高通认为他们可以在被收购的 Nuvia 实体与自身之间自由转移 Phoenix 核心微架构。高通声称无需 Arm 同意，因为 Arm 并不拥有、也无权干涉从 Nuvia 转移至高通的 IP。Arm 不同意高通的论点。

> 高通与 Arm 的 ALA 明确排除了对任何并非在该特定 ALA 下开发的 Arm 技术的许可。高通 ALA 将高通的设计与制造权利，以及 Arm 的验证、交付与支持义务，限定于满足以下条件的芯片：
>
> (1) 基于 Arm 依据该 ALA 交付给高通的技术，
>
> (2) 由高通工程师及高通子公司在相关实体作为高通子公司期间在高通内部创造，且
>
> (3) 在该 ALA 条款之下获得许可。
>
> 对于 Phoenix 核心或 Nuvia 工程师在 Nuvia 作为独立公司期间、基于 Arm 授予 Nuvia 的技术与许可所开发的其他设计，上述条件均不成立。因此，高通不仅是在试图开发一款未经许可的产品，而且正在**实质性违反其与 Arm 的 ALA**。

最后这段陈述极为重要。Nuvia 的 ALA 之所以在 Qualcomm 完成收购后被终止，是因为控制权变更需要 Arm 的同意。Arm 现在主张高通违反了它自己的 ALA，这将赋予 Arm 取消高通 ALA 的权利。

高通当然持相反意见，但这要由法院和陪审团裁决。Arm 已就全部诉求申请陪审团审理。高通与 Arm 看起来在玩胆小鬼游戏，且都准备好为此对簿公堂。

> 依据特拉华联邦地区法院本地规则 D. Del. LR 38.1 及《联邦民事诉讼规则》Fed. R. Civ. P. 38，Arm 特此就被告反诉中所有可由陪审团审理的诉求与争议申请陪审团审理（TRIAL BY JURY）。

理性的路径是最终和解，但很难想象 Arm 或高通会在各自立场上让步——这正是 Arm 申请陪审团审理的原因。

> Arm 没有义务支持高通进一步尝试利用 Arm 架构继续开发最初在 Nuvia 形成的未经许可的技术。

Arm 的这一立场可能导致基于 Phoenix 核心的芯片在 PC、智能手机、基站、汽车、AR 与 VR 市场全部延期。一场审判很可能耗时数年——尤其考虑到证据开示（discovery）过程可能极其漫长。即使法院不批准 Arm 的临时禁令请求，基于 Arm 架构的芯片也需要通过 Arm 的验证以确认符合 ISA 规范，而 Arm 声称它没有义务做这件事。

> Nuvia 权利的转移（包括高通对 Nuvia 的收购）需要 Arm 的同意，但未获得同意。由于 Nuvia ALA 明确要求任何转让须事先取得 Arm 同意，并明确将「转让」定义为包括任何其他公司对 Nuvia 的收购，高通在未取得 Arm 事先同意的情况下收购 Nuvia，违反了 Nuvia ALA。

高通反诉论点的一部分是指控 Arm 故意拖延沟通。高通称：「Arm 试图将其手中的一切杠杆最大化，以威胁高通的投资与高通的 SoC 路线图，并榨取高额版税。」

> 在高通首次就其计划收购 Nuvia 与 Arm 接触后的数日内，Arm 即书面告知高通：若希望继续使用依据 Nuvia ALA 创造的设计与技术，需要签订一份新协议。Arm 并未躲在暗处观望，而是公开且及时地指明并告知了 Nuvia 与高通各自的义务。

Arm 主张其已及时通知 Nuvia 与高通各自 ALA 下的义务。关于时间线回顾，[请参阅我们对这场诉讼的最初报道](https://www.semianalysis.com/p/is-arm-desperate-qualcomm-claps-back?utm_source=substack&utm_campaign=post_embed&utm_medium=web)。Arm 说他们在数日内就通知了对方，而高通与 Nuvia 却等了 2 周才告知 Arm 这笔收购。

Arm 的核心论点之一（我们认为颇具分量）围绕高通 $2.5B 收购 Cambridge Silicon Radio 一案。Arm 主张，高通当时按其与 Cambridge Silicon Radio 的许可协议要求取得了书面同意，因此对 Nuvia 也应当照办。

> 高通曾请求 Arm 同意在 2021 年 3 月 2 日前完成 Nuvia 与 Arm 许可协议的转让，这证实了 Arm 的同意是必需的，以授权「某些信息……从 NUVIA 转移至高通」。

高通曾就 Nuvia 许可转让请求 Arm 同意这一事实，是一个有力的论据。

高通反诉论点的另一部分是：在 Nuvia ALA 终止后，Arm 的工程团队仍继续协助高通做指令验证工作。高通以此证明其继续开发基于 Nuvia 核心的产品是正当的。

> 高通曾书面认可 Arm 的立场：即便 Arm 在过渡期继续支持 Nuvia 团队，Arm 的「协助并不明示或默示放弃 Arm 的任何权利」。

Arm 的这一陈述令上述论点彻底失效。尽管 Arm 曾每周与高通开会验证 Phoenix 核心，但双方就 Arm 在此事上的立场存在书面约定。

> Arm 承认高通已为其自身的 ALA 支付许可费，该 ALA 明确排除对 [已删节]（例如 Nuvia 对 Arm 架构的实现——[已删节]）的许可。就高通 ALA 而言，相关的 Nuvia 技术体现并衍生自 Arm 依据 Nuvia 现已终止的 ALA 向 Nuvia 交付的 Arm 技术，因此被明确排除在高通 ALA 许可范围之外。

高通主张其 ALA 覆盖全部 Nuvia 技术。Arm 不认可。

高通反诉中让我们觉得奇怪的一点，是提到 Arm Architecture Reference Manual（Arm 架构参考手册）可在网上获取。高通坚称其部署的唯一 Arm IP 只有公开可得的指令集。

> Arm 亦承认 Arm 架构参考手册可在线获取，但否认该手册属于公有领域；相反，手册明确写道：「本文档不授予任何明示或默示、禁止反言或其他方式下的知识产权许可，除非另有明确声明。」

科技界与分析师圈对此有一场大争论：这场诉讼究竟只是为了钱，还是也掺杂了报复心与傲慢。高通主张，Arm 既对当年合并失败怀恨在心，又不满高通将从更有利可图的技术许可协议（TLA）转向不那么有利可图的架构许可协议（ALA）。高通声称 Arm 想从高通身上榨取更多钱，让即将到来的 IPO 更好看。

> Arm 否认其「寻求额外杠杆以向高通索取合同规定其无权获得的版税」的指控，因为即便高通无须停止使用并销毁相关 Nuvia 技术，作为 Nuvia 的收购方，高通本也应按 Nuvia ALA 下的版税率向 Arm 支付费用。
>
> 例如，Nuvia ALA 第 6.2 条规定：
>
> [已删节]
>
> 对于基于或包含全部或部分在 Nuvia ALA 下开发的 Arm 架构技术的产品，该版税义务在 Nuvia ALA 终止后仍然存续。相比之下，高通不当试图把 Nuvia 技术纳入其自身 ALA 之下，以规避支付 Nuvia 的版税率，尽管该 Nuvia 技术并非在高通 ALA 下开发或许可。

目前，Arm 并没有通过法庭索要更多钱；他们要求的是销毁 Nuvia 衍生 IP。反诉中没有损害赔偿或金钱诉求，但我们确实认为，这种姿态的终极目标仍是达成一份包含更高版税率的和解。

> Arm 承认其商业提案曾提议修订高通的 ALA，以「(a) 使该协议的条款与 NUVIA 架构许可协议的条款对齐，包括但不限于版税率」

我们认为这场诉讼主要关乎金钱，如果高通大幅提高其版税支付并另行支付一笔一次性款项，官司就会烟消云散。

> Arm 承认本段第四句的第 (ii) 项。Arm 承认其商业提案还提出「讨论并确定与该 CPU 设计转移相关的**设计转移费**」，并且「对于 NUVIA 使用 Arm 实现 IP 与软件工具的设计，高通将就该实现 IP 与软件工具另行签订许可」。

令人大开眼界的是，Arm 表示其曾预期从 Nuvia 芯片扩展 Arm 市场中获得「数亿美元」收益。

> Arm 提议高通支付一笔设计转移费，并将某些版税率与 Nuvia 的费率对齐，以代替 **Arm 预期从 Nuvia 产品扩展 Arm 架构芯片市场中赚取的数亿美元**。

关于基础设施网络（infrastructure networking）的这一段值得一提。

> Arm 承认高通曾公开宣布计划将 Nuvia CPU 核心整合进高通的旗舰智能手机、下一代笔记本电脑与数字座舱，以及高级驾驶辅助系统（ADAS）、扩展现实和**基础设施网络解决方案**。

我们相信这指的是目前正在开发中的 5G 基站 SoC。

> Arm 承认，在高通收购 Nuvia 之时，Nuvia 与高通分别与 Arm 签有许可协议，各自许可交付给相关方的、分别界定的 Arm 技术。Arm 承认，Nuvia 与高通各自和 Arm 签订的独立许可协议均提供使用 Armv8 架构某些版本（包括版本 [已删节]）的特定权利。Arm 承认 Phoenix 核心体现并衍生自 Arm 架构的版本 [已删节]。Arm 承认高通与 Arm 签有提供 Armv9 架构特定使用权利的许可协议。

正如我们[在最初报道中所暗示的](https://www.semianalysis.com/p/is-arm-desperate-qualcomm-claps-back)，高通的许可范围总体更宽，而 Nuvia Phoenix 核心所处的 Arm ISA 层级如今基本已公开。

这份诉讼文件与[孙正义（Masayoshi Son）最近一次演讲](https://www.theregister.com/2022/11/14/softbank_boss_devotes_himself_to/)中关于 Arm 及其未来多年承诺的说法相矛盾。

> Arm 承认其计划在未来进行 IPO。

我们对孙正义言论的解读是：Softbank 在 IPO 之后很久仍将保留可观的持股。在这方面，Arm IPO 可能与 GlobalFoundries IPO 类似——流通盘低、控股方保留大量股份。

> Arm 承认，正如证据开示很可能显示的那样，高通仍在继续开发 Nuvia 的 Phoenix 核心与服务器 SoC。

那些宣称 Orion 服务器芯片已死的人，Arm 可不这么认为。

另一个要讨论的重大话题，是[高通关于 Arm 正在更改商业模式的指控](https://www.semianalysis.com/p/arm-changes-business-model-oem-partners)。

Arm 的反诉答辩/抗辩直接回应了这些指控，但除了声明否认之外并未多说什么。以下是其中一段的样子。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/04203a14-c1b4-4443-8a95-0b9f96f9d9bd_580x390.png)

证据开示将揭示高通对其「Arm 商业模式正在改变」的主张究竟握有什么证据（或者根本没有）。

我们交谈过的 OEM 厂商都没有听到任何关于 Arm 将商业模式改为直接向 OEM 授权的风声——与高通的说法相反。尽管没有听说过授权结构可能出现这种变化，这些 OEM 仍然感到担忧。他们同样担心高通继续设计与销售搭载 Arm ISA CPU 核心 SoC 的能力。

这场诉讼带来的不确定性意味着，OEM 必须制定包含 MediaTek 及其他 SoC 供应商在内的应急预案。

高通与其 OEM 伙伴之间出现重大的信誉损失，但 Arm 在其合作伙伴那里的信誉损失同样可观。这场诉讼正在加速 RISC-V 的投入与路线图。

[分享](https://newsletter.semianalysis.com/p/arms-nuclear-option-qualcomm-must?utm_source=substack&utm_medium=email&utm_content=share&action=share)

高通似乎想借「商业模式改变」的指控分散 Arm 客户的注意力，并赢下舆论法庭。我们需要看到高通那些惊人主张的证据。这些主张已经让 Arm 在这场纠纷中扮演了坏人的角色。

> 高通不合理、恶意地要求 Arm 履行所谓的高通 ALA 范围之外交付与开发之技术的验证、交付、维护与支持义务，这有悖双方的合理预期，损害了 Arm 从高通 ALA 中获得的利益，从而实质性违反该协议的条款及诚信与公平交易的默示契约，并使 Arm 有权依据第 14.2 条终止高通 ALA。

本报告末尾附有该法律文件。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
