---
title: "Arm 是否气急败坏？Qualcomm 强势回击 Arm 可能纯属滥诉的诉讼"
title_en: "Is Arm Desperate? Qualcomm Claps Back At Arm’s Potentially Frivolous Lawsuit"
subtitle: "授权细节曝光"
date: 2022-10-09
source: https://newsletter.semianalysis.com/p/is-arm-desperate-qualcomm-claps-back
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# Arm 是否气急败坏？Qualcomm 强势回击 Arm 可能纯属滥诉的诉讼

> 原文：[Is Arm Desperate? Qualcomm Claps Back At Arm’s Potentially Frivolous Lawsuit](https://newsletter.semianalysis.com/p/is-arm-desperate-qualcomm-claps-back) · SemiAnalysis

**授权细节曝光**

除非你与世隔绝，否则应该知道 Qualcomm 正被 Arm 起诉。最近，Qualcomm 提交反诉状进行了回击。我们周日起床后勉为其难地读起了 Qualcomm 的答辩状，但说来奇怪，这是我们读过的[最有趣的法律文件之一](https://storage.courtlistener.com/recap/gov.uscourts.ded.79892/gov.uscourts.ded.79892.15.0.pdf)。80 页的内容里只有三分之二很无聊！文件披露了一些关于本案以及 Arm 授权业务的有趣细节。我们将在本文中加以总结，并附上我们对此局势的看法。

想象一下：你是一家人才大量流失的 IP 授权公司，曾在法律意义上把自家最大增长市场（Arm China）的控制权拱手让人，又在熊市里被迫 IPO，而你的应对之策竟是起诉自家最大的合作伙伴之一——而且这家合作伙伴恰好拥有全行业最好的律师团队。

先交代一些背景。Arm 背后有 Softbank 输血，使其得以加大投入进入数据中心、汽车等市场。这些市场需要大量定制化工程，但 Arm 至今尚未从中获得可观的回报。这导致其盈利能力一落千丈。2015 年到 2020 年，Arm 的员工数翻倍，调整后 EBITDA 从高于总费用一路跌至接近转负。

随后 Nvidia 试图收购 Arm。那笔交易中包含一份条件优厚的低版税 20 年期授权，即便收购失败，这份授权依然有效。Arm 如今进退维谷。RISC-V 正在蚕食嵌入式核心市场，出货核心数已达数十亿颗，而 Arm 的数据中心业务仍未形成规模。

不仅如此，Arm 的一些大客户（如 Qualcomm）正在自研核心架构。大多数客户通过技术授权协议（TLA）使用 Arm 的现成核心，这类协议产生的版税远高于通过架构授权协议（ALA）自研核心的模式。而 Arm 最重要的一些客户——如 Apple、Nvidia 和 Qualcomm——全都持有 ALA 自研架构和/或条件优厚的特殊协议，这限制了 Arm 未来的增长和盈利能力。

> **ALA 之下的版税率通常更低，TLA 之下则更高**，因为 TLA 的版税对应的是 ARM 在开发完整 CPU 上的投入；而 ALA 下的被授权方需要自己投入大量资金开发自己的 CPU。
>
> 借助 Phoenix（自研）核心，Qualcomm 将开始在产品中融入更多自己的定制 CPU。Qualcomm 做出这一转变，是因为它相信自己的创新能造出性能优于 ARM 核心的核心。这一范式转变意味着，**未来 Qualcomm 将按照其 ALA 为这些定制 CPU 向 ARM 支付较低的版税率**，而不是按其 TLA 支付更高的版税率。

我们认为，Arm 提起这起诉讼，主要是想逼迫 Qualcomm 重新谈判，以榨取更高的授权收入。

> ARM 向 Qualcomm 索要额外付款的要求毫无道理，且与 Qualcomm 的长期协议相抵触。正如 ARM 在起诉状中承认的，NUVIA 当时专注于为服务器市场开发用于低出货量、高成本 SOC 的 CPU；而 Qualcomm 打算利用 NUVIA 已着手开发的技术，为 Qualcomm 的传统市场（如「移动」和「计算」市场）打造高出货量、低成本的 SOC。对于数据中心和服务器产品——其出货量低于、单位成本高于例如 Qualcomm 出货量更高、成本更低的移动产品——**NUVIA 与 ARM 谈定的版税率是 Qualcomm 版税率的许多倍**。ARM 面对 Qualcomm 更优厚的条款，其策略是无视 Qualcomm 的授权权利和版税率，企图把 NUVIA 为其服务器产品设定的远高于 Qualcomm 的版税率强加给 Qualcomm。

非常值得注意的是：Nuvia 的版税率比 Qualcomm 的高，而不是低。外界对本案的许多最初解读称，Qualcomm 是想按 Nuvia 较低的版税率付费、以逃避自己较高的版税率。这份文件清楚地表明那种说法是错的。

> ……制造一种 **ARM 盈利能力改善的假象**——要么通过强行逼迫 Qualcomm 支付额外、无据可依的版税，要么通过把 Qualcomm 从定制 CPU 和服务器 SOC 领域中直接消灭为竞争对手

关于最初起诉时铺天盖地的猜测，另一个话题是 Arm v9 授权。文件中虽然隐去了确切版本，但 Qualcomm 表示其授权覆盖这一 ISA。

> 收购发生时，NUVIA 和 Qualcomm 与 ARM 各自持有独立但高度重叠的授权协议。Qualcomm 的 ALA 涵盖了授予 NUVIA 的全部权利以及更多额外权利。两份 ALA 均授予使用第 8 版 ARM 指令集架构的权利，包括 Phoenix 核心兼容的 ARM [已删节] 指令集架构（「ISA」）。Qualcomm 的 ALA 范围还更广，授予了 Qualcomm 下一代 v9 ISA 的权利。

Arm 对 Qualcomm 的各项要求在下面这段里写得明明白白。

> Qualcomm 必须：(i) 把 NUVIA 协议中高得多的版税率并入 Qualcomm 既有的授权协议；(ii) 限制 Qualcomm 员工参与 Qualcomm 定制 CPU 设计的能力，即「至少」任何接触过 ARM 保密信息的个人须等待三年方可参与 Qualcomm 的「任何架构 CPU 设计」；(iii) 「讨论并决定与此类 CPU 设计转让相关的设计转让费」；以及 (iv) 就实现 IP（implementation IP）和软件工具另行签署一份授权协议，其中还包含另一笔未披露的「设计转让费」。

Qualcomm 声称，这些要求统统不在 Nuvia 或 Qualcomm 的授权协议之内。我们听说，关于数据访问权限的那一条对 Arm 非常重要。

> 此外，在 ARM 寻求损害赔偿的范围内，ARM 的可获赔偿额受 ALA 第 [已删节] 条的限制。

值得注意的是，Qualcomm 其实潜在承认了 Nuvia 的授权中确实包含一些 Qualcomm 授权所没有的内容。我们了解到，Qualcomm 正在尝试把基于 Phoenix 核心的 Orion 服务器平台授权给超大规模云厂商使用，而不是作为商用硅平台对外销售。

在这个背景下就说得通了：Nuvia 当年谈判其架构授权时，会特意谈下把自己的定制核心架构再授权（relicense）给其他公司的权利，而 Qualcomm 的协议里没有。

虽然相关表述在文件多处被删节，但结合我们的消息来源以及对文件字里行间的解读，我们相信事实就是如此。

> Qualcomm 还通知 ARM：对于 NUVIA 正在使用的、当时未落入 Qualcomm 现行 ALA 和 TLA 覆盖范围的任何 ARM 技术，Qualcomm 愿意与 ARM 团队合作完成任何必要的授权附件，以覆盖这些项目。

我们认为，Qualcomm 现有授权未覆盖的那一项，正是「再授权」。

> ARM 的立场对整个行业都是威胁。除非本法院驳回 ARM 的论点，否则 ARM 的极端立场可能被用于对付其所有被授权方，让 ARM 得以宣称拥有其所有被授权方创新成果的所有权。

Arm 的核心论点可以归结为几个方面：Qualcomm 继续开发其定制核心就是对 Arm 的侵权。而 Qualcomm 的观点是：核心架构归 Qualcomm 所有，Arm 唯一拥有的是决定谁在实施 Arm ISA 以及他们付多少费的权利。

> ARM 的威胁毫无根据。ARM 显然主张自己对 NUVIA 开发的所有技术都拥有权利，包括与 ARM 毫无关系的技术。但 ARM 无权要求销毁这些技术。ARM 并不拥有其被授权方的 CPU 和/或 SOC 设计，ARM 自己的授权协议对此写得清清楚楚。

Qualcomm 认为，自己可以在收购来的 Nuvia 实体与 Qualcomm 之间自由传递 Phoenix 核心微架构——这是一个非常有力的论点。Qualcomm 收购的 IP 是核心架构的实现（implementation），归 Qualcomm 所有，而非 Arm。

> 业界许多人在这个关键时刻看到的是技术进步的契机，ARM 看到的却是向 Qualcomm 强行施压、重谈双方长期授权协议财务条款的机会，而这场毫无依据的诉讼就是它的筹码。通过这起诉讼，ARM 向市场表明：它会肆无忌惮、机会主义地行事，把威胁新型、创新产品开发的做法当作谈判战术，而不是因为它真的握有有效的授权和商标主张。

这大概是整份文件中火药味最浓的一段。

> 2021 年 2 月，ARM 主张「NUVIA 与 ARM 协议项下的任何设计、权利或授权向 Qualcomm 的转让，均须事先取得 ARM 同意并受其约束」。ARM 毫无根据地坚持称，Qualcomm 需要 ARM 同意才能完成「NUVIA 协议项下任何设计、权利或授权」向 Qualcomm 的转让。

Qualcomm 的主张是：他们不需要 ARM 同意，因为 Arm 并不拥有、也不对从 Nuvia 转移到 Qualcomm 的 IP 享有任何权利。

> 首先，ARM 试图就 Qualcomm 已付费或正在依据自身授权协议持续付费的权利索取补充付款和版税。Qualcomm 的授权协议白纸黑字写明：Qualcomm 在进一步开发其从 NUVIA 收购的技术过程中对 ARM 技术的使用，将受 Qualcomm 既有授权协议覆盖。例如，因此，Qualcomm 一完成对 NUVIA 的收购，NUVIA 的技术即已依据 Qualcomm 的授权协议获得完全授权。尽管如此，尽管并非必要，Qualcomm 仍寻求 ARM 同意将 NUVIA 的 ARM 授权转让给 Qualcomm。
>
> 其次，ARM 声称有权控制 NUVIA 技术的转让，而 NUVIA 的 ALA 并未授予 ARM 任何此类权利。
>
> 第三，ARM 企图阻止 Qualcomm 的工程师工作三年，以此干扰 Qualcomm 的业务——而 NUVIA 或 Qualcomm 的授权协议中完全不存在支持这一要求的任何依据。

Arm 开出的这些价码非常大。最可能的解释是：故意漫天要价，好把 Qualcomm 拽回谈判桌。

> 收购交割后，ARM 变本加厉，声称除非 Qualcomm 答应 ARM 的要求——包括数千万美元的额外「转让」付款和提高后的版税——否则就必须销毁 NUVIA 的工程成果、从头再来。

Qualcomm 当然主张 Arm 对此毫无权利。

> 双方虽有断断续续的协商，但在 2021 年 9 月前后，ARM 停止就争议与 Qualcomm 沟通。与此同时，从 2021 年全年直至今日，在 ARM 完全知情的情况下，Qualcomm 持续推进 Phoenix 核心及搭载 Phoenix 核心的 SOC 的开发工作——这是 Qualcomm 依据其与 ARM 的授权协议享有的权利。

Qualcomm 主张，Arm 对其持续推进核心开发心知肚明。

> 首先，ARM 一直等到 Qualcomm 耗费了一整年工程努力、投入数亿美元将 Phoenix 核心技术进一步开发并集成到多款 SOC 中之后才出手——这还没算 Qualcomm 收购 NUVIA 花掉的 14 亿美元。ARM 试图将其手中筹码最大化，以威胁 Qualcomm 的投资和 SOC 路线图，榨取高昂的版税。

Qualcomm 的言下之意是：ARM 明知故晚、恶意谈判。目的就是等摊牌时，Qualcomm 已经改了路线图、花了数亿美元，若不向 ARM 屈服就将承受最大损失。Qualcomm 主张，ARM 一直在试图迫使 Qualcomm 以高得多的费用重签其现有架构授权。

> ARM 终止 NUVIA 协议的时间，恰在其公开宣布与 NVIDIA 的合并交易失败前三天——那笔交易曾遭到 Qualcomm 和业内许多公司的反对。这一时机表明，ARM 的动机之一是报复 Qualcomm 对 NVIDIA 交易的公开反对。

这可真够劲爆的！

> 2022 年 2 月 1 日（但 Qualcomm 直到 2022 年 2 月 4 日才收到），ARM 发函终止 NUVIA 的 ALA 和 TLA 授权协议，自 2022 年 3 月 1 日生效，并要求 NUVIA 和 Qualcomm 销毁全部 ARM 保密信息，且在 2022 年 4 月 1 日前出具证明其已遵照执行。而在 2022 年 2 月这封信之前，ARM 上一次暗示 NUVIA 或 Qualcomm 违反 NUVIA 授权协议已是六个多月前的事了。ARM 的这一要求来得莫名其妙，尤其是一直以来 ARM 都在支持 Qualcomm 开发从 NUVIA 收购的技术。

梳理一下时间线。

> 2022 年 4 月 1 日，NUVIA 出具证明，称其已销毁并隔离了所有 NUVIA 取得的 ARM 保密信息。
>
> 2022 年 4 月 12 日，就在 NUVIA 出具证明几周后，ARM 接受了测试结果，确认 Phoenix 核心在服务器 SOC 中的实现满足执行 ARM 指令集所需的合规要求。ARM 确认「Qualcomm……已按照架构协议规定的验证要求完成了其 CPU 核心的验证」。ARM 明确确认，验证测试是依据 Qualcomm 的 ALA 进行的。由此可见，ARM 不仅清楚地知道 Qualcomm 正在依据 Qualcomm 的授权协议开发 Phoenix 核心，ARM 还对这项工作予以认可，并且知道 Qualcomm 已经实现了该 ISA。

Qualcomm 的论点是：Arm 知情，甚至以行动认可了他们对核心的开发，并验证了这属于对授权的正当使用。

> 2021 年 12 月，ARM 在 NVIDIA 收购案中向监管机构明确表示：其 ALA 被授权方创造的技术属于被授权方而非 ARM，并称：「架构被授权方并不使用 ARM 的 CPU 设计。ARM 的架构被授权方使用自己的工程团队创造自己专有的 CPU 设计。」ARM 还专门把 Qualcomm 收购 NUVIA 一事作为 Qualcomm 打造自有专有 CPU 的例证引述给监管机构。

这一条分量很重。Arm 可能在这里搬起石头砸了自己的脚。业界本来就很清楚 ALA 被授权方拥有其核心设计与实现，但 Arm 现在把这话说在了明面上、留在了监管记录里。

> Qualcomm 有权在与 Qualcomm 的 CPU 核心技术相关的用途中使用 ARM 技术——即便其中某些方面可以追溯到 NUVIA 的工作成果。

关于 Arm 授权中 IP 归属的更多内容。

> ARM 不是在法庭上打这场官司，而是四处游说媒体成员和客户，为自家立场制造额外声量，企图把这纸诉状的杀伤力放到最大。

此言不虚。我们知道有一位分析师收钱替 ARM 放大声音（包括关于本案的言论），也知道有多位媒体人被 Arm 的代表明确带着报道这个故事。搞清楚谁在给分析师和媒体信源付钱，非常重要。我们相信 Qualcomm 同样付钱给分析师（而且付得更多）来放大自己的声音、向媒体放风。

Arm 商标的使用也是诉讼的一部分。Qualcomm 在文件中的抗辩很有说服力。

> ARM 的商标侵权和虚假来源指控同样站不住脚。

> Qualcomm 与 ARM 的授权协议赋予 Qualcomm 使用 ARM 商标的权利。

> ARM 官网也公开授予「任何……第三方」在各项指引框架下使用 ARM 商标的权利。

> Qualcomm 对 ARM 商标的使用非常有限，例如在营销材料、产品规格和技术文档中，用于准确传达 Qualcomm 产品与 ARM 架构兼容这一事实。

关于授权费还有一个有意思的观点。如果 Arm 想让 Qualcomm 按 Nuvia 的费率付费，那就应该同时提供 Nuvia 拿到的额外权利和好处。我们相信那些额外权利就是再授权（relicensing）。

> Qualcomm 解释说，ARM 要求 Qualcomm 按 NUVIA 的授权费率付费并不恰当，因为「ARM 并未提议向 Qualcomm 提供任何额外权利或好处以换取」其额外付款要求，而且 ARM 把 NUVIA 的版税率强加给 Qualcomm 也没有任何合同依据。

> Qualcomm 还解释说，ARM 对 Qualcomm 工程师提出的限制也不恰当：拟议的三年限制期将使产品开发几乎不可能进行，从而危及 Qualcomm 的开发工作，并将因授权收入流失而对 ARM 自身造成不利影响。

与 Arm 工程师每周举行验证测试通话，是 Arm 认可 Qualcomm 在其定制核心中使用 Nuvia 收购 IP 之正当性的又一证据。

> 2021 年 7 月，ARM 向 Qualcomm 交付了四份仅供设计用途的授权，供 Qualcomm 内部测试使用。ARM 还交付了十二份一次性授权，允许使用授权的 ARM 技术开发单个芯片设计方案。随后在 2021 年 10 月，ARM 又交付了三份永久授权，允许在无限多的设计中使用其中部分相同的 ARM 技术。与 ARM 的其他授权一样，Qualcomm 为这些授权支付了费用。

Arm 与 Qualcomm 合作密切。看起来 Arm 之所以推迟起诉，是想把伤害做到最大。

> 况且，ARM 是一直等到 Qualcomm 完成了服务器 SOC 的 Phoenix 核心设计之后——甚至是在 ARM 已接受 Qualcomm 的核心设计并确认其与 ISA 兼容之后——才终止 NUVIA 协议的。

Qualcomm 照办了 Arm 的要求。

> Qualcomm 和 NUVIA 从设计中移除了 NUVIA 取得的 ARM 保密信息，重新设计产品、以依据 Qualcomm 授权获得的信息取而代之——尽管两者是一模一样的信息——然后隔离了一份副本。Qualcomm 还将其设计环境和系统中的 NUVIA 取得的 ARM 保密信息移除并隔离。

> 在此期间，Qualcomm 的工程师无法继续推进产品开发，因为他们的全部注意力都集中在移除 NUVIA 取得的 ARM 保密信息上。

到了 5 月，Arm 似乎意识到自己的验证测试正在给这起官司帮倒忙。

> 同样，在 2022 年 5 月，Qualcomm 收到 ARM 的电子邮件，称集成 NUVIA 收购技术、且在 Qualcomm 收购 NUVIA 之后才首次开发的计算 SOC 已通过全部相关测试、与 ARM 兼容。然而，ARM 的工程团队表示，它尚无法发出正式的合规豁免文件，因为 ARM 的法务团队扣着不发。

如果你觉得这篇文章有料，请帮忙分享，这对我们很重要！

[分享](https://newsletter.semianalysis.com/p/is-arm-desperate-qualcomm-claps-back?utm_source=substack&utm_medium=email&utm_content=share&action=share)

提醒一句：SemiAnalysis 团队中没有执业律师。SemiAnalysis 是一家精品半导体研究与咨询公司，专注于从化学品原料、晶圆厂到设计 IP 与战略的半导体供应链。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
