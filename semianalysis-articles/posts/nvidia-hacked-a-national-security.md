---
title: "Nvidia Hacked - A National Security Disaster"
date: 2022-03-02
source: https://newsletter.semianalysis.com/p/nvidia-hacked-a-national-security
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
---

# Nvidia Hacked - A National Security Disaster

Nvidia was hacked for a vast sum of data and this hack is not only a disaster for Nvidia, but all chip companies and the national security of all “western” governments. A black hat group known as Lapsus$ has claimed responsibility for the attack, and states they are not a nation state actor.

Lapsus$ demands are odd. The initial demand was for a payment, but later they tacked on many more demands including pushing driver updates, open sourcing much of their software, and fully removing any cryptocurrency limiters. Nvidia has yet to agree to any of these demands, and law enforcement has been involved. The contents of this hack that have already been released have major implications, but the threatened release on Friday would be a national security disaster.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ad7aa7e0-58b3-497e-a0ae-9903d5f2deb7_542x678.png)

After the initial hack, Lapsus$ announced they had over 1TB of data. The group claimed that [Nvidia attempted to hack them back.](https://twitter.com/vxunderground/status/1497484483494354946?s=20&t=Xi7NvYlFXXlzyHEWmml3Og) The hackers responded by [releasing a file](https://twitter.com/darktracer_int/status/1497464801877839872?s=20&t=laV__odCAmU7zFfmH5LMCQ) that included password hashes of all Nvidia employees. This was severe blow, but relatively minor compared the other data they have released. Alongside the initial announcement, they also stated they were selling “full LHR V2.”

In February of 2021, Nvidia implemented LHR (Lite Hash Rate) on their newest RTX 3060 GPU which halved the rate at which popular crypto currencies such as Ethereum were mined. As the year progressed, they implemented this on all of their gaming GPUs as a way to make GPUs less attractive to crypto currency miners and more affordable for gamers. The “full LHR V2” is supposed to circumvent all mining performance limiters on Nvidia’s gaming GPUs.

The group used their source code access to recompile the driver without these mining limiters and immediately began selling it for $10. They later revised this price to $1,000,000.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/dd51390a-7cd9-4849-9286-235821557a28_542x677.png)

They also then released a file containing a large amount of data. This included all source code for drivers so other firms can recompile drivers. This source code included not only the gaming drivers, but also datacenter and AI GPU drivers, Nvidia’s proprietary AI upscaling technology known as DLSS, Ansel, Nvidia documentation, and Nvidia AI libraries such as NV-Torch and NV-Caffe. In addition, the file contains all of Nvidia’s GPU architectural configuration files for their next generation GPUs known as Hopper and Lovelace. Lastly, it also included Nvidia’s testers and simulation files.

This data alone shows Nvidia’s plans down to architectural decisions and configurations for the GPUs that Nvidia will launch later this year. Nvidia has a 2-year cycle, so the data leaked is what Nvidia will still be selling as their top products well into 2024... A complete disaster.

Nvidia’s proprietary software is considered to be its edge over its competitors. Part of this includes the testers and simulator files. This shows how Nvidia simulates their chip design and weighs various architectural decisions. In short, this is a critical part of Nvidia’s proprietary design process, and it is now in the public domain. With this data, the multiple Chinese AI and GPU firms can kickstart and catch up massively on the design of their GPUs. Western competitors would not touch this with a 10 foot pole due to being illegal and unethical, but as shown by Huawei in the last two decades, many others will blatantly violate these norms.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/7d730d91-6b2f-4b18-989d-0804579d6be8_530x560.png)

The group is now threatening to release a hardware folder that is 250GB. They allege this folder contains critical silicon design documents and code including the Verilog. With this access, there would be direct access to Nvidia’s design. In addition, they claim to have all details related to Nvidia’s Falcon control and security processor. Malicious semiconductor firms could look through these files, learn as much as possible and directly apply these learnings to their future products. They could go as far as reverse engineering the designs for SMIC’s 14nm process node. The only silver lining is that Verilog files may potentially be encrypted.

In the past, a malicious actor [hacked AMD](https://wccftech.com/amd-stolen-gpu-ip-exclusive/) and gained access to their Navi 21 GPU Verilog files. The hacker demanded $100 million, but they were not complete and gibberish. The level of access that Lapsus$ seems to have would make it plausible that they have access to the entire Verilog file in an unencrypted format. Semiconductor architecture designers and firms will likely have to deal with increased levels of IT security given the gravity of the Nvidia hack. Even intra-company sharing is likely to be impacted by new security practices that must be implemented in the wake of these security vulnerabilities.

The release of complete Verilog data would be a complete disaster for Nvidia and western national security. In essence, the blueprint of these chips, the product of a $580 billion company and $30 billion of research and development could be in the hands of hostile actors. The hacked data, which could have been sold to a nation-state actor, could very well prove the most strategically significant act of corporate espionage in a generation. With direct access to designs of the world's most advanced GPUs and AI processors, Chinese design firms could be able to dramatically increase the speed with which they catch up to their western competitors in all fields related to artificial intelligence and semiconductors. If, on the off chance that this data is not already in China's hands, the US Government should mobilize its cybersecurity arsenal to prevent PRC firms' ability to access this data. This intellectual property must be defended.

[Share](https://newsletter.semianalysis.com/p/nvidia-hacked-a-national-security?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)

Edit: Nvidia's reached out and referred us to [their official statement.](https://nvidia.custhelp.com/app/answers/detail/a_id/5333) We agree and do not believe this is related to the Russia-Ukraine conflict. The importance of the security breach isn't really up for discussion given the materials, which do pertain to national security interest. Nvidia’s technology is core to the western dominance in many aspects of semiconductors and computing.

> We have no evidence of ransomware being deployed on the NVIDIA environment or that this is related to the Russia-Ukraine conflict.

*This article was originally published on [SemiAnalysis](https://semianalysis.com/nvidia-hacked-a-national-security-disaster/) on March 3rd 2022.*
