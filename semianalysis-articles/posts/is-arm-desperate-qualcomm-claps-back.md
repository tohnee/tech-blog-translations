---
title: "Is Arm Desperate? Qualcomm Claps Back At Arm’s Potentially Frivolous Lawsuit"
subtitle: "Licensing Details Revealed"
date: 2022-10-09
source: https://newsletter.semianalysis.com/p/is-arm-desperate-qualcomm-claps-back
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
---

# Is Arm Desperate? Qualcomm Claps Back At Arm’s Potentially Frivolous Lawsuit

**Licensing Details Revealed**

Unless you’ve been living under a rock, you’d know that Qualcomm was being sued by Arm. Recently Qualcomm clapped back with their counterclaims. We started off our Sunday by begrudgingly reading Qualcomm’s defense, but oddly, this is one of the [most entertaining legal documents we have ever read](https://storage.courtlistener.com/recap/gov.uscourts.ded.79892/gov.uscourts.ded.79892.15.0.pdf). Only 2/3’s of the 80 pages were boring! There were some interesting details about the lawsuit and Arm licensing in general that can be revealed. We will summarize them here and add our takes on the situation.

Imagine being an IP licensing firm that is hemorrhaging talent, legally gave away control of your largest growth market (Arm China), forced to IPO in a bear market, and your course of action is to sue one of your largest partners, who just so happens to have the best lawyers in the industry.

To start off with, some context. Arm was bankrolled by Softbank which enabled them to increase their spending to enter markets such as datacenter and automotive. These markets involve a lot of purpose-built engineering, but Arm hasn’t received major payback from them yet. This made their profitability tank. From 2015 to 2020, headcount doubled, and adjusted EBITDA went from higher than total expenses to nearly negative.

Then Nvidia attempted to acquire Arm. Part of that deal included a sweetheart low-margin 20-year license that persists despite the failure of that acquisition. Arm is stuck in a very tough place. RISC-V is eating up the embedded core world with billions of cores shipped already, and the datacenter still has not reached critical mass.

Furthermore, some Arm’s largest customers like Qualcomm are working on custom core architectures. Most customers utilize Arm’s off-the-shelf cores through a technology licensing agreement (TLA). These earn much higher royalties than a custom core which is developed through an architecture licensing agreement (ALA). Some of Arm’s most important Arm customers such as Apple, Nvidia, and Qualcomm all have ALA custom architectures and/or sweetheart deals which limits Arm’s future growth and profitability.

> **Royalty rates are generally lower under ALAs and higher under TLAs**, because the TLA royalties account for ARM’s work in developing complete CPUs, whereas the licensees under an ALA make the significant investment to develop their own CPUs.
>
> With the Phoenix (custom) Core, Qualcomm will begin incorporating more of its own custom CPUs in its products. Qualcomm is making this change because it believes its own innovation will generate better performing cores than ARM’s cores. This paradigm change will mean **Qualcomm will in the future pay to ARM the lower royalty rate** under its ALA for these custom CPUs, rather than the higher royalty rates under Qualcomm’s TLA.

We believe this lawsuit by Arm is primarily attempting to renegotiate with Qualcomm in order to extract higher licensing revenue.

> ARM’s demands for additional payments from Qualcomm made little sense and were inconsistent with Qualcomm’s long-standing agreements. As ARM acknowledges in its complaint, NUVIA was focused on developing a CPU for use in low-volume, high-cost SoCs for the server market, whereas Qualcomm intended to use the technology NUVIA had started developing to build high-volume, lower cost SoCs for Qualcomm’s traditional markets, such as the “mobile” and “compute” markets. For its data center and server products—which would be of a lower volume and higher per-unit cost than, for example, Qualcomm’s higher volume and lower cost mobile products—**NUVIA and ARM had negotiated a royalty rate that was many multiples higher than Qualcomm’s rate**. ARM’s strategy, in light of Qualcomm’s more favorable terms, has been to ignore Qualcomm’s license rights and royalty rates and attempt to force upon Qualcomm NUVIA’s substantially higher royalty rate established for its server product.

It's very noteworthy that Nuvia’s royalty rate is higher, not lower than Qualcomm’s. Many initial takes of the lawsuit stated that Qualcomm wanted to pay Nuvia’s lower royalty instead of their higher royalty. That is clearly wrong based on this filing.

> create the **illusion of ARM achieving greater profitability**—either by effectively strongarming Qualcomm into paying additional, unjustified royalties or through eliminating Qualcomm as a competitor in the custom CPU and server SoC space

Another aspect of the rampant speculation from the initial lawsuit is regarding Arm v9 licensing. The filing redacted the exact version, but Qualcomm says its license includes this ISA.

> At the time of the acquisition, NUVIA and Qualcomm had separate, but broadly overlapping, license agreements with ARM. Qualcomm’s ALA included all the rights granted to NUVIA, as well as additional rights. Both ALAs granted rights to use version 8 of the ARM instruction set architecture, including the ARM [redacted] instruction set architecture (“ISA”) with which the Phoenix Core was compatible. Qualcomm’s ALA is also broader, granting Qualcomm rights to the next generation v9 ISA.

Arm’s demands against Qualcomm are spelled out here.

> Qualcomm must: (i) incorporate the much higher royalty rates from NUVIA’s licenses into Qualcomm’s pre-existing licenses; (ii) restrict the ability of Qualcomm employees from working on Qualcomm’s custom CPU designs such that “at a minimum” any individual with access to ARM Confidential Information wait three years before working on “any architecture CPU design” at Qualcomm; (iii) “discuss and decide on the design transfer fee associated with such CPU design transfer”; and (iv) enter into a separate license for implementation IP and software tools, which would include another undisclosed “design transfer fee.”

Qualcomm claims all these demands are not part of Nuvia’s or Qualcomm’s license agreement. We hear the point about data access is a very important one for Arm.

> Moreover, to the extent ARM seeks damages, ARM’s damages are limited pursuant to [Redacted] of the ALA

It should be noted that Qualcomm does potentially admit that the Nuvia license does contain some elements the Qualcomm license does not. We have heard Qualcomm is attempting to license out the Orion server platform based on the Pheonix core to hyperscalers rather than sell it as a merchant silicon platform.

In this context, it makes sense that Nuvia negotiated its architecture license in a way that would allow them to relicense its custom core architecture to other companies, while Qualcomm’s did not.

While mentions of this were redacted in many places, speaking to our sources plus reading between the lines on the filing makes us believe that this is the case.

> Qualcomm also notified ARM that, to the extent NUVIA was utilizing any ARM Technology not currently covered under Qualcomm’s then-current ALA and TLA, Qualcomm would work with the ARM team to complete any necessary license annexes to cover such items.

We believe that item that is not currently covered by Qualcomm’s license is re-licensing.

> ARM’s position is a threat to the industry generally. Unless this Court rejects ARM’s arguments, ARM’s extreme position could be weaponized against all of its licensees, allowing ARM to claim ownership over all its licensees’ innovations.

Arm’s main argument boils down to a few areas. That Qualcomm is infringing on Arm by continuing the development of its custom core. Qualcomm is making the point that the core architecture is owned by them and the only thing Arm owns is the ability to say who is implementing the Arm ISA and what fees they paid.

> ARM’s threats are baseless. ARM apparently contends that it has rights over all technology developed at NUVIA, including technology that had absolutely nothing to do with ARM. But ARM has no right to demand destruction of that technology. ARM does not own CPU and/or SoC designs of its licensees, as ARM’s license agreements make clear.

Qualcomm believes they are freely able to pass the Phoenix core microarchitecture between the acquired Nuvia entity and themselves, which is a very strong argument. The IP that Qualcomm acquired was the core architecture implementation, which is owned by them, not Arm.

> While many in the industry see in this pivotal moment the opportunity for technological advancement, ARM sees an opportunity to strongarm Qualcomm into renegotiating the financial terms of the parties’ longstanding license agreements, using this baseless lawsuit as leverage. With this lawsuit, ARM makes clear to the marketplace that it will act recklessly and opportunistically, threatening the development of new and innovative products as a negotiating tactic, not because it has valid license and trademark claims.

This was probably the spiciest quote from the entire document.

> In February 2021, ARM contended that “any transfer of designs, rights, or licenses under NUVIA’s agreements with ARM to Qualcomm will require and be subject to ARM’s prior consent.” ARM insisted, without basis, that Qualcomm needed ARM’s consent to “any transfer of designs, rights or licenses under NUVIA’s agreements” to Qualcomm.

Qualcomm’s claim is they do not need their consent as Arm does not own or have any rights to the IP that was transferred from Nuvia to Qualcomm.

> First, it was attempting to secure supplemental payments and royalties for rights for which Qualcomm had already paid or was continuing to pay under its own license agreements. Qualcomm’s license agreements, on their face, make clear that Qualcomm’s use of ARM Technology in connection with the further development of the technology it acquired from NUVIA would be covered by Qualcomm’s pre-existing license agreements. For example, Therefore, NUVIA’s technology was fully licensed under Qualcomm’s license agreements as soon as Qualcomm acquired NUVIA. Nonetheless, and although not necessary, Qualcomm sought ARM’s consent to assign NUVIA’s ARM licenses to Qualcomm.
>
> Second, ARM was claiming a right to control the transfer of NUVIA technology when NUVIA’s ALA provided no such rights to ARM
>
> Third, ARM was trying to interfere with Qualcomm’s business by preventing Qualcomm engineers from working for three years with absolutely no basis for such a demand in NUVIA’s or Qualcomm’s license agreements.

These are some very large demands Arm has. Most likely they are overbearing in order to get Qualcomm to come back to the negotiation table.

> After the acquisition closed, ARM doubled down, asserting that Qualcomm needed to destroy NUVIA’s engineering work and start over unless it agreed to ARM’s demands, including tens of millions of dollars in both additional “transfer” payments and increased royalties.

Qualcomm claimed that Arm has no right to those of course

> While the parties had intermittent discussions to resolve the dispute, in or about September 2021, ARM stopped communicating with Qualcomm about the dispute. Meanwhile, throughout 2021 to the present day and with full knowledge by ARM, Qualcomm continued development work on the Phoenix Core and SoCs incorporating the Phoenix Core, as was its right under Qualcomm’s own license agreements with ARM.

Qualcomm claims Arm knew full well they were continuing to develop the core.

> First, ARM waited until Qualcomm had expended a year of engineering effort and hundreds of millions of dollars to further develop and integrate Phoenix Core technology into multiple SoCs, in addition to the $1.4 billion Qualcomm spent to acquire NUVIA. ARM was seeking to maximize whatever leverage it had to threaten Qualcomm’s investment and Qualcomm’s SoC roadmap and extract exorbitant royalty payments.

Qualcomm is seemingly claiming that ARM knowingly delayed its actions and negotiated in bad faith.  The purpose was so that when the grievances were brought up, Qualcomm would have already changed its roadmap, spent hundreds of millions, and suffer maximum damages if it didn’t bend to ARM’s will. Qualcomm claims ARM was trying to force Qualcomm to renegotiate their existing architecture license to much higher fees.

> ARM terminated the NUVIA agreements just three days before ARM publicly announced the failure of its merger transaction with NVIDIA—a deal that Qualcomm and many others in the industry had opposed. This timing suggests that, in part, ARM was seeking payback for Qualcomm’s public opposition to the NVIDIA deal.

Talk about spicy!

> February 1, 2022 (but not received by Qualcomm until February 4, 2022), ARM terminated, effective March 1, 2022, the NUVIA ALA and TLA license agreements and demanded that NUVIA and Qualcomm destroy all ARM Confidential Information, and certify by April 1, 2022 that they had complied with ARM’s demands. Prior to the February 2022 letter, it had been over six months since ARM last suggested that NUVIA or Qualcomm violated NUVIA’s license agreements. ARM’s demand came out of nowhere, especially as ARM had continued to support Qualcomm in the development of the technology acquired from NUVIA.

A bit of a timeline.

> on April 1, 2022, NUVIA certified that it had destroyed and quarantined all NUVIA-acquired ARM Confidential Information.
>
> on April 12, 2022, just a few weeks after NUVIA made its certification, ARM accepted test results verifying that the implementation of the Phoenix Core in the Server SoC complied with the requirements necessary to execute the ARM instruction set. ARM confirmed that “Qualcomm . . . has validated their CPU core in accordance with the Verification requirements set out in the Architecture agreement.” ARM explicitly confirmed that the validation testing was conducted under Qualcomm’s ALA. Therefore, ARM was not only well aware that Qualcomm was working on the Phoenix Core under Qualcomm’s license agreements, but ARM also affirmed this work and understood that Qualcomm had implemented of the ISA.

Qualcomm is arguing that Arm had full knowledge and even acted in a way that approved their development of the core and validated it as a rightful use of the license.

> ARM explicitly told regulators in December 2021, in connection with the proposed NVIDIA acquisition, that technology created by its ALA licensees belongs to the licensees, not ARM, stating: “architectural licensees do not use ARM’s CPU designs. ARM architectural licensees create their own proprietary CPU designs using their own engineering teams.” ARM specifically referred regulators to Qualcomm’s acquisition of NUVIA as an example of Qualcomm’s efforts to create its own proprietary CPU.

This is a big deal. Arm may have shot themselves in the foot here. While it was well understood that the ALA’s owned their core design and implementation, Arm is now stating that publicly.

> Qualcomm is licensed to use ARM Technology in connection with Qualcomm’s CPU core technology, even if any aspects trace back to NUVIA’s work.

More about the ownership of IP in an Arm license.

> Rather than litigate its case in court, ARM attempted to maximize the negative impact of its filing this lawsuit by campaigning with members of the media and customers to generate additional publicity for ARM’s positions.

This is true. We know of an analyst who is paid to amplify ARM’s message including about the lawsuit and multiple members of the media who were explicitly paraded this story by an ARM representative. Knowing who pays analysts and sources for media is important to consider. We believe Qualcomm also pays analysts (more) to amplify messaging and pumps stories through to the media as well.

The use of Arm’s trademarks was also part of the lawsuit. Qualcomm’s defense throughout the document is compelling.

> ARM’s trademark infringement and false-origin claims are also meritless

> Qualcomm’s license agreements with ARM give Qualcomm the right to utilize ARM’s trademarks

> ARM’s website also publicly grants “any . . . third party” the right to use ARM’s trademarks pursuant to various guidelines.

> Qualcomm engages in limited use of the ARM Marks, such as in marketing materials, product specifications, and technical documentations, to convey accurately that Qualcomm’s products are compatible with the ARM architecture.

An interesting point on the licensing fees. If Arm wants Qualcomm to pay the Nuvia licensing fees, then they should offer additional rights and benefits that Nuvia got. We believe those additional rights are relicensing.

> Qualcomm explained that ARM’s demand that Qualcomm pay the NUVIA licensing rates was not appropriate because “ARM has not proposed giving Qualcomm any additional rights or benefits in exchange for” its demand for additional payments and because there was no contractual support for ARM’s imposition of NUVIA’s royalty rates on Qualcomm.

> Qualcomm also explained that ARM’s proposed restrictions on Qualcomm’s engineers were inappropriate, as the proposed three-year restriction period would make it nearly impossible to develop products, thus endangering Qualcomm development work and would adversely impact ARM through the loss of licensing revenue.

Weekly calls for verification testing with Arm engineers is more proof Arm agreed that Qualcomm’s use of Nuvia-acquired IP in their custom core was valid.

> in July 2021, ARM delivered to Qualcomm four design-only licenses for Qualcomm internal testing. It also delivered to Qualcomm twelve single-use licenses, allowing the development of a single chipset design using the licensed ARM Technology. Subsequently, in October 2021, ARM delivered three perpetual licenses allowing for use of some of that same ARM Technology in unlimited designs. Like other licenses from ARM, Qualcomm paid for these licenses.

Arm worked closely with Qualcomm. Seems like Arm delayed the suit because they wanted to exact as much damage as possible.

> Moreover, ARM waited to terminate the NUVIA agreement until Qualcomm had already completed the design of the Phoenix Core for its Server SoC—and even after ARM had accepted Qualcomm’s core design as ISA compatible.

Qualcomm complied with Arm’s request.

> Qualcomm and NUVIA removed NUVIA-acquired ARM Confidential Information from its designs and redesigned its products to replace it with information acquired under Qualcomm’s license—even though it was the exact same information—then quarantined a copy. Qualcomm also removed NUVIA-acquired ARM Confidential Information from its design environment and systems and quarantined it.

> During this period, Qualcomm’s engineers were not working on further development of products because their attention was focused on the removal of NUVIA-acquired ARM Confidential Information.

Seems like in May, Arm realized their validation test was shooting themselves in the foot for this lawsuit.

> Similarly, in May of 2022, Qualcomm received an email from ARM stating that the Compute SoC—which integrated technology acquired from NUVIA and was first developed after Qualcomm’s acquisition of NUVIA—had passed all relevant tests and was ARM-compatible. Yet, ARM’s engineering team noted that it could not yet send a formal compliance waiver because ARM’s legal team was withholding it.

If you found this informative, please share, it helps!

[Share](https://newsletter.semianalysis.com/p/is-arm-desperate-qualcomm-claps-back?utm_source=substack&utm_medium=email&utm_content=share&action=share)

As a reminder, SemiAnalysis has no practicing lawyers on staff. SemiAnalysis is a boutique semiconductor research and consulting firm specializing in the semiconductor supply chain from chemical inputs to fabs to design IP and strategy.

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
