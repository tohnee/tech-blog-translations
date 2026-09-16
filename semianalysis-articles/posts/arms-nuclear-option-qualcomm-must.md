---
title: "Arm’s Nuclear Option – Qualcomm Must Cancel Next-Generation Products If Arm Succeeds"
subtitle: "Arm denies allegations of changing its business model"
date: 2022-11-16
source: https://newsletter.semianalysis.com/p/arms-nuclear-option-qualcomm-must
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
---

# Arm’s Nuclear Option – Qualcomm Must Cancel Next-Generation Products If Arm Succeeds

**Arm denies allegations of changing its business model**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

If you have been keeping up with the biggest soap opera in the tech world, you know Arm sued Qualcomm. Qualcomm more recently made some [pretty big counterclaims](https://www.semianalysis.com/p/is-arm-desperate-qualcomm-claps-back) that, if true, [would mean that Arm is changing its entire business model.](https://www.semianalysis.com/p/arm-changes-business-model-oem-partners)

[![](https://substackcdn.com/image/fetch/$s_!HwSb!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F0150776c-9bf2-4bea-a9c2-41b24b7a0f15_1280x1280.png)SemiAnalysisArm Changes Business Model – OEM Partners Must Directly License From ArmThe Qualcomm-Arm saga is epic and there is a new massive update in the case. This update contains evidence that Arm is changing its entire business model and moving to require licenses from OEMs. It also contains evidence of some hints at anti-competitive licensing behavior around GPUs, NPUs, and ISPs…Read more4 years ago · 36 likes · 15 comments · Dylan Patel](https://www.semianalysis.com/p/arm-changes-business-model-oem-partners?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

In the newest installment in the divorce drama of the decade, Arm is answering and defending against Qualcomm’s counterclaims. Arm’s tone in their defense is very clear. Arm disagrees with Qualcomm’s counterclaims wholeheartedly, including denying the allegations that Arm is changing its business model.

We will summarize the defense with our opinions below, but the most significant development is that Arm is threatening the nuclear option. Arm’s nuclear option is the termination of Qualcomm’s architecture license agreement for breach of contract.

> Qualcomm is materially breaching its ALA, giving Arm the right to terminate, and the Qualcomm ALA does not provide a license for or right to continue development of the Nuvia technology.

Arm wants Qualcomm to stop developing the Nuvia Phoenix core, and Arm is threatening to terminate Qualcomm’s own architecture licensing agreement (ALA).

> Qualcomm and Nuvia must stop using and destroy any Arm-based technology developed under Nuvia’s ALA, and that neither Qualcomm nor Nuvia is licensed to continue developing this technology

Qualcomm argues that it can continue developing the Nuvia technologies under its own ALA. If Qualcomm’s ALA were terminated, it would torpedo multiple products currently in development at Qualcomm across the verticals of PC, smartphone, AR, VR, automotive, 5G base station, and the server Orion SoC.

> Qualcomm’s architected cores (including all further developments, iterations, or instantiations of the relevant technology that Qualcomm acquired from Nuvia), Server SoC, and Compute SoC are not fully licensed under Qualcomm’s ALA or TLA; instead, they must be discontinued and destroyed

Until now, Arm has been demanding Qualcomm destroy only the Nuvia-derived work, including the Phoenix core. This would also cause multiple product delays and a significant refactoring of the Qualcomm product roadmaps.

> In April and May 2022, Nuvia and Qualcomm expressly certified that they would comply with the obligation to destroy and not use the defined Arm technology and confidential information.

Qualcomm, in their filing, claimed to quarantine proprietary Arm IP under the Nuvia ALA and replace it with IP under the Qualcomm ALA. Arm claims they must destroy all derivative work made under the Nuvia ALA.

> Arm admits that Qualcomm sent Arm a letter dated May 23, 2022, asserting that Qualcomm’s own Arm licenses would permit it to incorporate Nuvia technologies “that are not subject to any removal or quarantine obligations” into Qualcomm products, without specifying what, if any, Nuvia technology fit that description. Arm admits that Qualcomm asserted that Nuvia had developed technologies that were not subject to the termination requirements without explaining whether these technologies were derived from Arm Technology delivered under the Nuvia licenses. Arm admits that Qualcomm’s letter indicated that Qualcomm would comply with the termination obligations to the same extent as would Nuvia, without objecting to Arm’s termination of the Nuvia licenses.

The center of the dispute is whether IPs such as branch predictor, FPU, Out of Order engine, Micro-Op Decoder, etc. are wholly the property of Qualcomm/Nuvia, or if Arm has rights to these pieces of IP. Qualcomm claims that only the instruction set is owned by Arm, but Arm believes that these elements of the core, derivative work, are also subject to the agreement.

> Arm denies that micro-architectural know-how and expertise required to build a CPU is not related to the ISA.

Qualcomm claims that the Nuvia IP transferred is not related to the ISA. This assertion is being rejected by Arm.

While we cannot read the actual architecture license due to its status as confidential information, Arm seems pretty certain of this provision.

> Qualcomm is not authorized to make, use, sell, or import a product incorporating designs or derivatives of the NuVia technology

Terminating the Qualcomm ALA would kill this custom core effort at Qualcomm, including ground-up designs that do not contain any acquired Nuvia IP. Even if Qualcomm were to win the argument that they can continue to develop the Phoenix core under their own ALA, they could not ship anything based on the core if the Qualcomm ALA is also terminated.

> Contrary to its allegations, Qualcomm cannot continue using Arm-based technology, including the Phoenix core.

Qualcomm believes they could freely pass the Phoenix core microarchitecture between the acquired Nuvia entity and themselves. Qualcomm claims they do not need Arm’s consent as Arm does not own or have any rights to the IP transferred from Nuvia to Qualcomm. Arm disagrees with Qualcomm’s argument.

> Qualcomm’s ALA with Arm expressly excludes any license to Arm technology that was not developed under that specific ALA. The Qualcomm ALA limits Qualcomm’s design and manufacture rights, and Arm’s verification, delivery, and support obligations, to chips
>
> (1) based on the technology Arm delivered to Qualcomm under that ALA,
>
> (2) created at Qualcomm, by Qualcomm engineers and Qualcomm subsidiaries during the period while those entities were subsidiaries of Qualcomm, and
>
> (3) licensed subject to the terms of that ALA.
>
> None of this is true of the Phoenix core or other designs developed by Nuvia engineers at Nuvia based on the technology and license granted to Nuvia by Arm when Nuvia was a standalone company. Thus, Qualcomm is not only trying to develop an unlicensed product, but is also **materially breaching its ALA with Arm.**

The last statement is incredibly important. The Nuvia ALA was terminated following the acquisition by Qualcomm because Arm’s consent is required for a change of control. Arm is now arguing that Qualcomm has breached its own ALA, which would give Arm the right to cancel Qualcomm’s ALA.

Qualcomm, of course, argues otherwise, but that is for the courts and jury to decide. Arm is demanding a trial by jury for all claims. Qualcomm and Arm are seemingly playing chicken and are ready to go to trial over this.

> Pursuant to D. Del. LR 38.1 and Fed. R. Civ. P. 38, Arm hereby demands a TRIAL BY JURY of all claims and issues presented in Defendants’ Counterclaim that are so triable

The rational path would be an eventual settlement, but it’s hard to see Arm or Qualcomm budging from their arguments, which is why Arm demands a trial by jury.

> Arm has no obligation to support Qualcomm’s further attempts to continue developing unlicensed technology originally developed at Nuvia using Arm’s architecture

This position by Arm could potentially delay the Phoenix core-based chips for the PC, smartphone, base station, automotive, AR, and VR markets. A trial likely takes years—especially given how lengthy the discovery process could be. Even if the court doesn’t grant Arm a temporary injunction, Arm-based chips need to be validated by Arm as being ISA compliant, which Arm claims they have no obligation to do.

> Arm’s consent was required but not obtained for the transfer of Nuvia’s rights, including through Qualcomm’s acquisition of the company. Because the Nuvia ALA expressly required prior consent from Arm to any assignment of the ALA, and expressly defined assignment to include any other company’s acquisition of Nuvia, Qualcomm’s acquisition of Nuvia without Arm’s prior consent breached the Nuvia ALA.

One part of Qualcomm’s counterclaim argument is that Arm purposely delayed their communications. Qualcomm argues, “ARM was seeking to maximize whatever leverage it had to threaten Qualcomm’s investment and Qualcomm’s SoC roadmap and extract exorbitant royalty payments.”

> Within days after Qualcomm first contacted Arm about its planned acquisition of Nuvia, Arm informed Qualcomm in writing that it would need to enter into a new agreement if it wished to continue using the designs and technology that had been created pursuant to the Nuvia ALA. Arm did not wait in the weeds; it openly and promptly identified and communicated Nuvia’s and Qualcomm’s obligations.

Arm argues that they were prompt in notifying Nuvia and Qualcomm of their obligations under their respective ALAs. For a timeline recap, [see our original report on this lawsuit.](https://www.semianalysis.com/p/is-arm-desperate-qualcomm-claps-back?utm_source=substack&utm_campaign=post_embed&utm_medium=web) Arm says they notified them within days, whereas Qualcomm and Nuvia waited for 2 weeks before notifying Arm of the acquisition.

One of Arm's core arguments, which we feel is powerful, is surrounding Qualcomm’s $2.5B acquisition of Cambridge Silicon Radio. Arm claims that Qualcomm received written consent as they were obligated to under their license agreement with Cambridge Silicon Radio, and that Qualcomm needs to do that with Nuvia as well.

> Qualcomm requested that Arm consent to the assignment of Nuvia’s license agreements with Arm by March 2, 2021, confirming Arm’s consent was required, to authorize “the transfer of certain information . . . from NUVIA to Qualcomm.”

The fact that Qualcomm requested Arm’s consent to the assignment of the Nuvia license is a powerful argument.

A part of Qualcomm’s counter-claim argument was that Arm’s engineering teams continued to help Qualcomm with instruction validation work after the termination of the Nuvia ALA. Qualcomm used this as proof that their continued work on Nuvia core-based products was valid.

> Qualcomm agreed in writing with Arm’s position that, even if Arm continued to support the Nuvia team in the interim, Arm’s “assistance does not expressly or impliedly waive any of Arm’s rights.”

Arm’s statement here makes this entire argument defunct. Even though Arm provided weekly meetings with Qualcomm for validating the Phoenix core, there was a written agreement with Qualcomm about Arm’s position on the topic.

> Arm admits that Qualcomm has licensed and paid for its own ALA, which expressly excludes a license to [REDACTED] such as Nuvia’s implementation of Arm architecture—[REDACTED]. For purposes of the Qualcomm ALA, the relevant Nuvia technology embodies and was derived from Arm technology delivered by Arm to Nuvia under Nuvia’s now-terminated ALA, and thus is expressly excluded from the Qualcomm ALA license.

Qualcomm argues that its ALA covers all the Nuvia tech. Arm disagrees.

One part of Qualcomm’s countersuit that we thought was odd was the mention that the Arm Architecture Reference Manual was available online. Qualcomm insists that the only Arm IP they deployed was the publicly available instruction set.

> Arm also admits that the Arm Architecture Reference Manual is available online, but denies that the manual is in the public domain; instead, the manual makes clear that “[n]o license, express or implied, by estoppel or otherwise to any intellectual property rights is granted by this document unless specifically stated.”

There is a big argument among the tech and analyst community about whether the lawsuit is only about money or if there is an element of vengeance and hubris as well. Qualcomm argues that Arm is both mad about the failed merger and that Qualcomm will move from a more lucrative technology license agreement (TLA) to a less lucrative architecture license agreement (ALA). Qualcomm claims that Arm wants to extract more money from Qualcomm to make the upcoming IPO look better.

> Arm denies the allegation that it is “[s]eeking additional leverage it can use to attain royalties from Qualcomm to which it is not entitled under the contracts” because even if it did not have to stop using and destroy the relevant Nuvia technology, Qualcomm would have been subject to Nuvia’s royalty rates under the Nuvia ALA in its capacity as Nuvia’s acquirer.
>
> For example, Section 6.2 of the Nuvia ALA says:
>
> [REDACTED]
>
> This royalty obligation for products that are based on or incorporate Arm-based technology developed in whole or in part under the Nuvia ALA survives termination of the Nuvia ALA. In contrast, Qualcomm improperly sought to bring the Nuvia technology under its own ALA to avoid paying Nuvia’s royalty rates, even though the Nuvia technology was not developed or licensed under Qualcomm’s ALA.

Currently, Arm is not asking for more money through the courts; they are asking for the Nuvia-derived IP to be destroyed. There is no claim for damages or money in the counterclaim, but we do believe that the ultimate goal of this posturing is to bring a settlement that includes higher royalty rates.

> Arm admits that its commercial proposal offered an amendment to Qualcomm’s ALA to “(a) align the terms of that agreement with those in NUVIA’s architecture license agreement including but not limited to the royalty rates

We believe the lawsuit is mostly about money and that it would go away if Qualcomm massively increased its royalty payments and made a separate one-time payment.

> Arm admits clause (ii) of the fourth sentence of this paragraph. Arm admits that its commercial proposal also offered to “discuss and decide on the **design transfer fee** associated with such CPU design transfer” and that, “[w]ith respect to NUVIA’s design(s) using Arm implementation IP and software tools, Qualcomm will enter into a separate license for such implementation IP and software tools.”

It’s eye-opening to see that Arm says they expected “hundreds of millions of dollars” of earnings from Nuvia-based chips expanding the market for Arm.

> Arm proposed that Qualcomm pay a design transfer fee and harmonize certain royalty rates with Nuvia’s rates in lieu of the **hundreds of millions of dollars Arm anticipated earning from Nuvia’s products** expanding the market for Arm-based chip

This bit about infrastructure networking is noteworthy.

> Arm admits that Qualcomm publicly announced plans to integrate Nuvia CPU cores into Qualcomm’s flagship smartphones, next-generation laptops, and digital cockpits, as well as Advanced Driver Assistance Systems, extended reality and **infrastructure networking solutions.**

We believe they are referring to the 5G base station SOC which is currently under development.

> Arm admits that at the time of Nuvia’s acquisition, Nuvia and Qualcomm had separate license agreements with Arm, each of which licensed separately defined Arm technology delivered to the relevant party. Arm admits that Nuvia’s and Qualcomm’s separate license agreements with Arm provided certain rights to use version 8 of the Arm architecture, including version [REDACTED]. Arm admits that the Phoenix core embodied and was derived from version [REDACTED] of the Arm architecture. Arm admits that Qualcomm has a license agreement with Arm that provides certain rights to use version 9 of the Arm architecture.

As we alluded to [in our original reporting](https://www.semianalysis.com/p/is-arm-desperate-qualcomm-claps-back), the Qualcomm license is generally broader and the Nuvia Phoenix core Arm ISA level is now basically public.

The filing contradicts [a recent speech from Masayoshi Son](https://www.theregister.com/2022/11/14/softbank_boss_devotes_himself_to/) about Arm and their multi-year commitment in the future.

> Arm admits that it is planning to issue an IPO in the future

Our interpretation of Masayoshi Son comments is that Softbank would still retain a significant ownership stake long after the IPO. The Arm IPO is likely similar to the GlobalFoundries IPO in this regard, low float, with the controlling entity retaining a significant ownership stake.

> Arm admits, as discovery is likely to show, that Qualcomm continued to develop Nuvia’s Phoenix core and Server SoC.

For those who claim Orion server chips are dead, Arm doesn’t think so.

The other major topic to discuss is surrounding [Qualcomm's claims that Arm is changing their business model](https://www.semianalysis.com/p/arm-changes-business-model-oem-partners)

The counterclaim/defense from Arm directly addresses them but doesn’t say much beyond stating they deny the allegations. Here’s a snippet of what it looks like.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/04203a14-c1b4-4443-8a95-0b9f96f9d9bd_580x390.png)

Discovery will reveal what proof (or lack thereof) Qualcomm has for its claims that the Arm business model is changing.

The OEMs we have spoken to haven’t heard a thing about Arm changing their business model to direct OEM licensing like Qualcomm claims. These OEMs are still concerned even though they haven’t heard anything about that potential change to licensing structure. They are also concerned about Qualcomm’s ability to continue to design and sell SOCs with Arm ISA CPU cores.

The uncertainty around the lawsuit means that OEMs must build contingency plans that include MediaTek and other SOC providers.

There is significant reputation loss with Qualcomm and their OEM partners, but there is also considerable reputation loss with Arm to their partners. This lawsuit is accelerating RISC-V efforts and roadmaps.

[Share](https://newsletter.semianalysis.com/p/arms-nuclear-option-qualcomm-must?utm_source=substack&utm_medium=email&utm_content=share&action=share)

It seems like Qualcomm is trying to distract Arm’s customers and win the court of public appeal with the accusations of the business model change. We need to see proof of Qualcomm’s extraordinary claims. Those claims have made Arm look like the bad guy in this situation.

> Qualcomm’s unreasonable, bad-faith demands that Arm comply with purported obligations for verification, delivery, and support and maintenance with respect to technology delivered and developed outside the scope of the Qualcomm ALA are contrary to the parties’ expectations and undermines the benefit to Arm from the Qualcomm ALA, thereby materially breaching that agreement’s terms and implied covenant of good faith and fair dealing and entitling Arm to terminate the Qualcomm ALA under Section 14.2.

Attached at the end of this report is the legal filing.

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
