---
title: "Samsung Electronics Cultural Issues Are Causing Disasters In Samsung Foundry, LSI, And Even DRAM Memory!"
date: 2022-04-17
source: https://newsletter.semianalysis.com/p/samsung-electronics-cultural-issues
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
---

# Samsung Electronics Cultural Issues Are Causing Disasters In Samsung Foundry, LSI, And Even DRAM Memory!

Samsung Electronics and more squarely Samsung’s various semiconductor branches, are on fire. At the turn of the last decade, Samsung was on top of the world. They were rapidly gaining share in foundry. Samsung was the fastest to multiple logic node transitions in the foundry space. Samsung LSI design teams were putting out the best mobile chip designs. Apple was completely reliant on Samsung for manufacturing all critical components. Samsung had a multi-year lead over the other DRAM manufacturers in cost of production. These technical advantages are all falling apart.

Samsung Electronics has a culture problem that has shaken it to its core. Samsung is slipping on all aspects of technology development including the one area they have historically crushed all competitors, DRAM. They do not produce a top 3 mobile SOC anymore, with even MediaTek passing them up. The foundry business has bled its two largest customers in short succession to TSMC. There are credible reports of lies and deceit within the Samsung Foundry operations. Even Intel’s fledgling new foundry business has been able to woo over a customer or two from Samsung Foundry!

This article is going to report on many of the symptoms that are reported in Korean media as well as some of our own research into the topic. To be clear, some details from the Korean media are unverified, but the overarching issues are evident.

Something is clearly wrong at Samsung Electronics.

These issues stem directly from the cultural makeup at Samsung. Before going too much further into the detail, we believe the general trend is that these issues have been bubbling for many years, but the boiling point has been reached.

First off let’s start with perhaps the tamest part of this story before progressing to the most damning. Samsung had a service known as [“Game Optimizing Service”](https://meeco.kr/ITplus/34754710) which throttled most applications except for common benchmarks, even [non-game apps such as Netflix and Instagram](https://meeco.kr/ITplus/34755550).  Admittedly, we weren’t outraged by this because Android OEMs have a [long history](https://www.anandtech.com/show/15703/mobile-benchmark-cheating-mediatek) of [cheating on benchmarking apps](https://www.anandtech.com/show/7187/looking-at-cpugpu-benchmark-optimizations-galaxy-s-4). Samsung is facing a [class action](https://www.asiatoday.co.kr/view.php?key=20220318010010413) lawsuit due to their behavior.

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

Why did Samsung initiate this “Game Optimizing Service”? To keep heat and power consumption in check of course. Heat and power consumption have been running rampant the last couple generations as node issues have cropped their heads at Samsung. Even going back years, all the way to Samsung’s in-house CPU, the design failed due to poor leadership. Samsung also had a GPU team that they canned. Both these instances are just yet more examples why developing your own silicon is much harder than it may appear. Cultures at a design house and fab are critical to success. These genius engineers need the correct motivation, direction, and leadership.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9106b83d-4bb1-4c19-90de-11268442955f_633x892.jpeg)

After the inhouse GPU architecture failure, many fans of Samsung were excited for the pivot to [adopting AMD’s RDNA based GPU IP.](https://www.anandtech.com/show/14492/samsung-amds-gpu-licensing-an-interesting-collaboration) This excitement was very short-lived. The issues related to foundry and process nodes really reared their heads with the current generation [Exynos 2200](https://drive.google.com/file/d/1Bj58pQPiwS4y6cXyk2SFle9e8zzoLzPm/view). Performance per watt is abysmal. The performance and power consumption of the RDNA based GPU weren't the only issues with this SOC.

Samsung initially planned to launch the Exynos chip more broadly across the world. Some analysts and trade publications were even projecting as high as 60% of total Galaxy S22 series volume to be Exynos 2200 based and 40% Qualcomm S8G1 based. Of course, this turned out to be a dud, and the actual Exynos volume ended up being less than 25%. While we don’t think the plan was ever to go up to 60%, we did hear Samsung wanted to move up the share of Exynos processors up to 40%. The shortfall in volume was mostly due to performance and yields.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/51804c13-f7d1-4af3-b3f6-3bd2521cb2f0_1024x655.png)

Samsung’s Exynos 2200 has been reported to have [abysmal yields](http://www.thelec.kr/news/articleView.html?idxno=16234). This is partially due to their use of the 4LPE node. This node innovated over the 7/5nm families of Samsung by [offering a 198nm UHD cell height](https://www.linkedin.com/posts/yuzo-fukuzaki-12408111_samsung-exynosabr2200-4lpe-activity-6917180674298761216-8yXC/?utm_source=linkedin_share&utm_medium=member_desktop_web) versus the prior node having 218nm UHD cell height. The yields for this node are rumored to be as low as 20%. These seem way too low, but we have heard the parametric yields were horrendous even though catastrophic yields were fine. Another source told us the final shipping chip came in with the higher power and lowered performance targets, resulting in around 80% parametric yields. Regardless, rumors say there is an [agreement between the executives](https://m.clien.net/service/board/park/16995380) to ship the newest node possible even if it doesn’t make economic or power/performance sense. Talk about top-down culture issues.

As a short explanation, catastrophic yield losses are when a transistor, via, or section of metal layer does not function at all. Parametric yield losses are when these function, but the question is whether it hits your targets for performance, power, voltage, etc. With parametric yields on Exynos 2200 so low, the chip’s targets had to be adjusted down. In fact, [rumors point](http://www.thelec.kr/news/articleView.html?idxno=16234) to Samsung cutting the clocks on the GPU from a planned [1.69GHz to 1.49GHz and eventually to 1.29GHz](https://n.news.naver.com/article/014/0004774178).

The issues don’t stop with the foundry and SOC teams missing their technical goals. The culture is quite toxic in the face of mistakes. These various units are allegedly [playing the blame game](https://www.greened.kr/news/articleView.html?idxno=295149) with each other. Samsung LSI (design) is blaming Samsung Foundry, while Samsung Mobile is blaming S.LSI.

In other cases, Samsung LSI executives even seem to be blaming [the change in Korean labor laws](http://m.thebell.co.kr/m/newsview.asp?svccode=00&newskey=202204091554435640102620). Rather than hitting crunch time and having engineers do absurd hours, employees are supposed to be limited to 52 hours a week, maximum. While we hear this is not being adhered to fully, it has cut down on the overworking of many Samsung engineers. The pushback from Samsung is so strong that there is even legislation being pushed to relax these labor laws.

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

The culture in Samsung semiconductor has gotten so toxic, that the foundry is even [allegedly lying about the yields.](https://www.fnnews.com/news/202202131249028377) Korean media reports that there is an ongoing management overview and audit. The result of this review is likely to be a reshuffling of management and teams similar to that of the reorganization of the wireless unit last year. [The later reports of lying](https://www.infostockdaily.co.kr/news/articleView.html?idxno=167041) even go as deep as alleging that Samsung Foundry lied to customers and the Samsung chairman on 5nm, 4nm, and 3nm yields. These various reports seem quite credible given how many media outlets in Korea are reporting it and how many local experts have chimed in. We won’t even be diving into the corporate espionage that [Samsung committed on TSMC](https://www.theregister.com/2015/08/25/tsmc_samsung_espionage_judgment/) during the transition to FinFET.

What we do know for sure, is that Qualcomm is angry with Samsung. Qualcomm used a variant of the Samsung 5nm node which was dubbed 4LPX rather than the denser 4LPE node like Exynos 2200 [according to TechInsights.](https://www.linkedin.com/posts/yuzo-fukuzaki-12408111_samsung-exynosabr2200-4lpe-activity-6917180674298761216-8yXC/?utm_source=linkedin_share&utm_medium=member_desktop_web) We also have been told by multiple sources that parametric yields for the S888 and S8G1 processors were quite poor leading to Qualcomm needing to push these SOCs to way higher power levels to achieve certain performance targets.

While the reported yields for Qualcomm’s S8G1 are not quite as low as the Exynos 2200, they aren’t anywhere near adequate. As a side note, this works out fine for Qualcomm (and Nvidia). We have been told these two customers have negotiated to pay per yielded die rather than per wafer fabricated.

Qualcomm decided to completely leave Samsung Foundry on their high end SOCs due to issues with the S765G, S780G, S888, and S8G1. Qualcomm has even had special teams working around the clock for months and months on prepping the S8G1+ for TSMC’s N4 process node. S8G2 and future high-end Qualcomm chips will be on TSMC for the foreseeable future. Despite the smartphone market slowing down in recent months, TSMC may still be able to maintain growth in the smartphone segment this year and next year due to the share shifts with Qualcomm and continued content growth.

Samsung Mobile has been racing to find alternatives with the S.LSI division struggling on smartphone SOCs. [Korean rumors](https://meeco.kr/mini/34835643) even state that Samsung has turned to evaluating the MediaTek Dimensity lineup for the Galaxy A series lineup. Dr. TM Roh, president of Samsung Mobile, has said there is a [new application processor only for Galaxy phones.](https://www.greened.kr/news/articleView.html?idxno=295149) This is quite odd because most S.LSI Exynos SOCs, while they are offered externally, are basically exclusive to Samsung Galaxy smartphones. This points to some more infighting and drama between Samsung Mobile and S.LSI.

Samsung Foundry issues run even deeper. [As we reported last year](https://semianalysis.substack.com/p/samsung-foundry-3nm-gate-all-around?s=w), foundry offerings of their 3nm GAP node do not even ship to external customers until as late as 2024. 3GAE, the first gate all around (GAA) node, has constantly been pushed back silently and [may even be canceled.](https://biz.sbs.co.kr/article/20000055654) Yields are allegedly abysmal. For anyone thinking Samsung could catch up to TSMC because of TSMC’s N3 issues and N2 starting production in late 2025, you are sorely mistaken.

Samsung has blundered and lost their largest foundry customer, Qualcomm, and their 2nd largest foundry customer, Nvidia. As we reported earlier this week in [our deep dive into Nvidia’s next generation Ada Lovelace gaming GPUs](https://semianalysis.substack.com/p/nvidia-ada-lovelace-leaked-specifications?s=w), the process technology is a custom TSMC N4 derivative called 4N.

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

Samsung LSI is not complete chaos though. They are gaining share in the 5G infrastructure market through well designed, efficient chips at reasonable prices. They are also winning quite a few automotive wins in infotainment systems such as with [Hyundai](https://m.sedaily.com/NewsViewAmp/260V2GIB89) and [Volkswagen](https://m.etnews.com/20211130000125). S.LSI seems to be well geared to working closely with customers such as with Google on the [Tensor smartphone SOC.](https://www.anandtech.com/show/17032/tensor-soc-performance-efficiency) Despite this success, S.LSI seems to be thwarted at every opportunity as Samsung Foundry seems to have cost them the contract for next generation [Cisco Silicon One networking ASICs, and that’s lost to Intel!](https://semianalysis.substack.com/p/intel-is-throwing-the-kitchen-sink?utm_source=url)

S.LSI has been working closely with Tesla for years on the self-driving/ADAS HW 3.0. This is a co-designed chip where Tesla was assisted by Samsung and [both contributed meaningful IP to the final chip design](https://en.wikichip.org/wiki/tesla_(car_company)/fsd_chip). This chip design has shipped millions of units into Tesla’s vehicles. HW 4.0 was scheduled for production at the end of last year, but delays seem to have snagged it to this year. Alongside Ambarella, Tesla is the only major external customer left for S.LSI/Foundry.

S.LSI has also hit other blunders recently, such as in the image sensor market. Their ISOCELL smartphone sensors have been slow to adopt hybrid bonding, unlike Sony, who has been [shipping it in volume since 2017.](https://semianalysis.substack.com/p/advanced-packaging-part-2-review) Furthermore, they have failed to gain share with Chinese smartphone makers who have elected to use Sony on the high end and Omnivision on the midrange and low end. The standalone camera sensors and cameras were into their own division called Samsung NX, but that has [since been canned too,](https://m.etnews.com/20170405000273?obj=Tzo4OiJzdGRDbGFzcyI6Mjp7czo3OiJyZWZlcmVyIjtOO3M6NzoiZm9yd2FyZCI7czoxMzoid2ViIHRvIG1vYmlsZSI7fQ%3D%3D) even after decades of Samsung’s investments in standalone cameras.

# **Samsung DRAM Catastrophe**

Samsung DRAM, the cash cow of Samsung Electronics, hasn’t been smooth sailing either. 5 years ago, Samsung was undoubtedly better than Micron and SK Hynix in density, performance, and cost structure. Some estimates put them as far as a year and a half ahead in those days. Now, Samsung is arguably behind Micron and SK Hynix in some of these metrics despite a much larger volume relative to these two peers. Samsung’s overly aggressive behavior with process development, which stems from cultural issues, is the culprit.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/39816318-fa7a-4f00-892f-323aceba6d4a_1024x587.png)

As a brief primer, DRAM density and cost scaling have slowed down tremendously as capacitor scaling has slowed. The 1Xnm generation was the first indication of this massive slowdown, but since then, cost scaling with each node has only been around 15%. Density gains have been so tepid, that the DRAM manufactures have turned to using letters as the suffix rather than numbers like they did in the pre-20nm generation. Samsung was quite a bit ahead at the 1Y generation relative to the competition in cost, power, and performance.

This all changed with the 1Z generation. Samsung had decided to be very aggressive on EUV adoption. This was a decision that was driven from the top down, not engineering. These top-down decisions have been quite common within Samsung electronics in general and they are the result of the cultural issue we have been pointing out. With 1Z, Samsung announced they would adopt EUV. This was done with lots of fanfare and press. Samsung was incredibly proud of this “achievement”.

Samsung dominated early shipments for EUV tools by soaking up ~50% of them. Samsung attempted to insert it in DRAM as well as their botched early 7nm logic attempt. The 1Z DRAM node never ramped fully. This trend has continued with the next generation 1 Alpha node, which increased EUV utilization further. This node reportedly took longer to develop. While Samsung has claimed 1 Alpha as in mass production for quite some time, it has still not ramped significantly either. Meanwhile, SK Hynix and Micron have been able to catch up on cost, performance, and power with their 1Z generation, which did not utilize EUV.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a38be212-9220-477d-82a4-3d78c14add6b_1024x526.jpeg)

Furthermore, with the 1 Alpha generation, Micron continues to push with DUV only while SK Hynix has started to insert EUV. As such, Micron is already ramping 1 Alpha while both SK Hynix and Samsung have been quite tepid with their volume ramps. SemiAnalysis estimates that Micron currently has the cost advantage with DRAM due to being able to shift all their volume to the 1 Alpha generation and achieve the best density and cost across their entire lineup.

Samsung and SK Hynix [are still shipping non-EUV 1Y for their first generation of DDR5](https://www.techinsights.com/blog/industry-leading-ddr5-technology), while Micron is crushing the competition and shipping their 1Z generation for the first generation of DDR5. Furthermore, Micron is doing a fast follow with the 2nd generation of DDR5 on the 1 Alpha generation process node. To be clear, EUV is not the only culprit at play, but it is one of the biggest technical differences.

This is where things take a turn for the worst for Samsung. They haven’t been able to ramp 1Z. They haven’t been able to ramp 1 Alpha, and now [reports are coming out](https://www.fnnews.com/ampNews/202204121844028873) that [they have canceled development of the next generation 1 Beta process node!](https://n.news.naver.com/article/014/0004819002) Others report that Samsung is driving another topdown hail Mary by pushing [straight to the 1 Gamma node.](https://laoyaoba.com/html/share/news?source=h5&news_id=814707) The cancellation report has a high degree of credibility as it is based on a disgruntled engineer at Samsung. He even posted a blog about this topic!

The engineer has been verified to be part of the technology development team for Samsung’s DRAM. He wrote a letter to the two heads of Samsung Electronics, Chairman Lee Jae-yong and CEO Kye Hyun Kyung describing the failure and issues. The blog was since taken down, but [Korean media has captured](http://news.tvchosun.com/mobile/svc/osmo_news_detail.html?contid=2022041390082) some quite concerning quotes from it.

> I've heard quite a few stories of 'crisis', but I think this moment is more dangerous than ever. In the midst of the successive occurrences, it seems that the top decision maker is not able to grasp the root cause of the problem.
>
> Samsung DRAM Technology Development Engineer (Google Translate)

We encourage you to check it out to truly grasp the gravity of the situation. For 4-year tenured engineer who is deeply passionate about his work to lash out so brazenly is a huge red flag. Doubly so due to the well-defined hierarchical manner of Korean work culture. We have also seen a handful of Samsung DRAM technology development employees moving to SK Hynix in the last month. This is more than the normal rate of attrition.

Cultural issues have rocked Samsung on a tremendous level. While many parts of Samsung Electronics are still well-oiled execution machines such as Samsung Display, NAND, Automotive, and Networking, the most important businesses are in trouble. These cultural issues have culminated in Samsung losing their technology and cost advantage in DRAM, falling way behind TSMC in the leading-edge process technology race, losing their biggest foundry customers, and losing to Qualcomm and MediaTek in smartphone SOC design.

[Share](https://newsletter.semianalysis.com/p/samsung-electronics-cultural-issues?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

*Clients and employees of SemiAnalysis may hold positions in companies referenced in this article*.
