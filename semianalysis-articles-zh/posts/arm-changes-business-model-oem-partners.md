---
title: "Arm 改变商业模式——OEM 合作伙伴必须直接向 Arm 取得授权"
title_en: "Arm Changes Business Model – OEM Partners Must Directly License From Arm"
subtitle: "基于 Arm 的 SOC 将不再允许使用外供 GPU、NPU 或 ISP"
date: 2022-10-28
source: https://newsletter.semianalysis.com/p/arm-changes-business-model-oem-partners
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# Arm 改变商业模式——OEM 合作伙伴必须直接向 Arm 取得授权

> 原文：[Arm Changes Business Model – OEM Partners Must Directly License From Arm](https://newsletter.semianalysis.com/p/arm-changes-business-model-oem-partners) · SemiAnalysis

**基于 Arm 的 SOC 将不再允许使用外供 GPU、NPU 或 ISP**

Qualcomm 与 Arm 之间的连环大戏堪称史诗级，如今案件又有了重大新进展。这次更新包含的证据显示，Arm 正在彻底改变其商业模式，转向要求 OEM 厂商直接取得授权。其中还包含一些暗示 GPU、NPU 和 ISP 领域存在反竞争性授权行为的证据。

先回顾一下背景：Arm 起诉了 Qualcomm，Qualcomm 随后提起反诉，[约 3 周前我们做过详细报道。](https://www.semianalysis.com/p/is-arm-desperate-qualcomm-claps-back)

[![](https://substackcdn.com/image/fetch/$s_!HwSb!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F0150776c-9bf2-4bea-a9c2-41b24b7a0f15_1280x1280.png)SemiAnalysis《Arm 是否气急败坏？Qualcomm 强势回击 Arm 可能纯属滥诉的诉讼》除非你与世隔绝，否则你应该知道 Qualcomm 正被 Arm 起诉。最近 Qualcomm 提交反诉进行了回击。我们周日起床后勉强读完了 Qualcomm 的答辩状，但说来奇怪，这是我们读过的最有趣的法律文件之一……阅读全文 4 年前 · 33 个赞 · 1 条评论 · Dylan Patel](https://www.semianalysis.com/p/is-arm-desperate-qualcomm-claps-back?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

根据 Qualcomm 更新后的反诉状，2024 年之后，Arm 将不再依据技术授权协议（TLA）向 Qualcomm 等半导体公司授权其 CPU，而是只向设备制造商授权。据称 Arm 正告知各 OEM：想获得基于 Arm 架构的芯片，唯一途径就是接受 Arm 的新授权条款。Qualcomm 声称，Arm 就 Qualcomm 的授权条款向其 OEM 合作伙伴撒了谎。

此外，Qualcomm 声称，Arm 还告诉这些 OEM：半导体厂商将无法再提供其基于 Arm 的 SOC 中 Arm 同时也作为授权产品出售的其他组件——包括 GPU、NPU 和 ISP。看起来 Arm 实际上是在以「要么全要、要么拉倒」的模式将其其他 IP 与 CPU IP 捆绑。这意味着 2024 年之后，Samsung 与 AMD 的 GPU 授权合作、Mediatek 与 Imagination GPU 的合作都将不再被允许。而且，无论这些厂商自家的 ISP 或 NPU 比 Arm 的好多少，它们都将无法继续使用。

如果属实，Arm 对 Qualcomm 和 OEM 的威胁手段可谓相当肮脏。Mediatek、Samsung 以及 Arm 的其他合作伙伴应该感到非常害怕。这将迅速加速 RISC-V 路线图的推进，而且这种行为散发着浓浓的反竞争味道。Nvidia 手握一份 20 年期的 Arm 授权，因此不受影响。Apple 由于是 Arm 的创始股东之一，显然拥有极为优厚的授权条款。我们了解到 Broadcom 的条款也相当有利。

如果你不相信我们、觉得这一切听起来太疯狂，我们理解。以下是我们阅读法律文件后的理解。不妨亲自读读 Qualcomm 昨天向法院提交的反诉状节选。文件全文附在文末。

> 自 2022 年 8 月 31 日在本案中提交起诉状以来，ARM 一直在持续性地、不正当地产出关于 Qualcomm ARM 授权性质的错误信息，向购买 Qualcomm ARM 兼容核心和芯片组的客户散布不实之词，企图破坏 Qualcomm 的业务和客户关系。
>
> ARM 的这场虚假信息运动，由其管理层亲自实施，也由其所有者 SoftBank 的管理层代表 ARM 实施，目的在于损害 Qualcomm、诋毁其产品、破坏 Qualcomm 与客户的关系，并在本不存在不确定性的地方制造不确定性。
>
> 至少早在 2022 年 10 月，ARM 便向 Qualcomm 的一家或多家长期原始设备制造商（"OEM"）客户虚假陈述：除非他们接受 ARM 的一份新的直接授权（依据该授权，他们须按其自身产品销售额向 ARM 支付版税），否则自 2025 年起他们将无法获得 ARM 兼容芯片。ARM 还威胁至少一家 OEM：如果它不这样做，ARM 将转而授权该 OEM 的大型竞争对手——言下之意是，该 OEM 将被排除在市场之外，既无法从 Qualcomm 也无法从任何其他供应商那里获得 ARM 兼容芯片，包括依据 TLA 获得的 ARM「现货」芯片。ARM 之所以这么做，是尽管其早已带着直接授权方案接触过该 OEM 的竞争对手，却摆出一副只有在受威胁的 OEM 拒绝授权之后才会去接触竞争对手的姿态。
>
> ARM 还告诉 Qualcomm 的一家或多家客户：当现有 TLA 协议到期后，ARM 将停止依据 ARM TLA 向所有半导体公司（包括 Qualcomm）授权 CPU。ARM 声称其正在改变商业模式，今后将只向设备制造商本人提供授权。ARM 向各 OEM 解释说，设备制造商要获得 ARM 兼容芯片，直接与 OEM 签署授权将是唯一途径。
>
> ARM 正试图通过虚假断言来胁迫这些客户接受其直接授权，包括：Qualcomm 的 ARM 授权协议将于 2024 年终止，因此自 2025 年起 Qualcomm 将无法向他们提供 ARM 兼容芯片；ARM 不会延长与 Qualcomm 的授权；ARM 不会允许 Qualcomm 自 2025 年起出货产品。

> 这些陈述毫无争议地是虚假的，其目的在于损害 Qualcomm 与客户的关系——并为 ARM 自己从这些客户手中攫取利润丰厚的合同——手段是质疑 Qualcomm 在 2024 年之后维持其 ARM 授权并向客户供货的能力，尽管依据其 ARM 授权，Qualcomm 在未来多年内都明确拥有这样的权利。
>
> 依据其 ALA，Qualcomm 的授权有效期直至 2025 年之后数年，且该协议赋予 Qualcomm 单方面将合同在初始期限基础上再延长数年的权利。具体而言，ALA 中写道：

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9fed9dde-5e4c-4cb5-8078-62f92882e6db_932x238.png)

遗憾的是，该部分内容被删节了。

> 因此，鉴于 Qualcomm 的 ALA 并未终止——且未发生任何足以产生终止权利的事件——本授权的初始期限将持续至 [已删节]。此后 Qualcomm 有权将授权延长至 [已删节]。因此，ARM 无权拒绝延长 Qualcomm 的授权，也无权阻止 Qualcomm 在 2025 年出货其产品。
>
> 此外，ARM 无权向 Qualcomm 的客户索取额外版税。Qualcomm 的 ALA 赋予 Qualcomm 一项穷尽性授权（exhaustive license），这意味着 ARM 无权就 Qualcomm 已支付过版税的同一产品，再去向 Qualcomm 的客户索取另一份版税。
>
> ARM 的胁迫行径并不止于这些关于 Qualcomm 授权协议的虚假陈述。为了施加更大压力，ARM 进一步声称，Qualcomm 和其他半导体制造商也将无法向 OEM 客户提供 SOC 的其他组件（例如图形处理器（"GPU"）、神经网络处理器（"NPU"）和图像信号处理器（"ISP"）），因为 ARM 计划将这些组件的授权与设备制造商的 CPU 授权捆绑。
>
> ARM 还声称其已就要求与 OEM 直接签署授权的新商业模式知会了 Qualcomm。该陈述是虚假的。ARM 并未通知 Qualcomm 它将要求设备制造商直接取得授权。ARM 没有告诉 Qualcomm 它打算停止将 CPU 技术作为独立授权对外许可，没有说它将不再向半导体公司授权 CPU 技术，也没有说它将要求被授权方只能从 ARM 获取其他技术（尤其是 ARM 的 GPU 和 NPU 技术）。如上所述，ARM 商业模式上这些已实施或威胁要实施的变更，完全没有把 Qualcomm 与 ARM 之间的现有协议考虑在内。
>
> 尽管 ARM 关于 Qualcomm 的陈述毫无事实依据，它们已造成重大的声誉损害，并伤害了 Qualcomm 的客户关系。而且，虽然 ARM 的目标可能是损害 Qualcomm——并在其已通过合同授予 Qualcomm 完全穷尽性权利的情况下，胁迫 Qualcomm 的客户签订不必要的合同——但其手法将给整个行业内 ARM 的客户和被授权方带来伤害。

这表明这场诉讼短期内不可能和解。要在短期内了结，唯一的途径是法院裁决。

我们原本以为这场诉讼归根结底是为了钱，但现在我们开始觉得，这场诉讼掺杂了远比钱更多的个人恩怨。

Softbank/Arm 是在因为 Qualcomm 促成监管机构否决了 Nvidia 的收购而恼羞成怒吗？

Arm 会试图讨回它的「一磅肉」，哪怕这意味着它过往的良好名声会被拖进泥潭。我们认为 Arm 正在犯一个巨大的错误，这将加速竞争架构的崛起。

感谢阅读 SemiAnalysis。本文为公开文章，欢迎分享。

[分享](https://newsletter.semianalysis.com/p/arm-changes-business-model-oem-partners?utm_source=substack&utm_medium=email&utm_content=share&action=share)

> Qualcomm 在收购 NUVIA 之时起，NUVIA 技术中所使用的任何 ARM 技术之使用，均已依据 Qualcomm 的授权协议获得完全授权。
>
> NUVIA-ARM 协议和 Qualcomm-ARM 协议中均不存在以下任何条款：
>
> a.      禁止 Qualcomm 收购 NUVIA 或获取 NUVIA 的技术；
>
> b.      要求 Qualcomm 在收购 NUVIA 或使用 NUVIA 的技术前须取得 ARM 同意；
>
> c.      要求 Qualcomm 停止使用其已获取的任何 NUVIA 技术；
>
> d.      要求 Qualcomm 销毁 NUVIA 的技术；
>
> e.      禁止向 Qualcomm 转让或披露 NUVIA 的技术或保密信息；
>
> f.       将 NUVIA 技术的使用仅限于 NUVIA 一方；或
>
> g.      要求 Qualcomm 就继续开发任何在研
>
> h.      设计或技术（即 Qualcomm 从 NUVIA 获取的部分）取得 ARM 同意。

Arm Qc Answer And Defenses And Amended Cc 删节版（Arm Qc Answer And Defenses And Amended Cc Redacted Version）366KB ∙ PDF 文件 下载下载

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

[赠送订阅](https://newsletter.semianalysis.com/subscribe?&gift=true)

[特别感谢 Ravi 向我们指出了这场法律大战的这一最新进展。](https://twitter.com/Ravi_711/status/1585815463338348544?s=20&t=6TxURMLTOnMs3uAHXEkaMQ)
