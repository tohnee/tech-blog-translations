---
title: "Marvell 的下一个 $1B 业务是安全——硬件安全模块（HSM）"
title_en: "Marvell's Next $1B Business Is Security – Hardware Security Modules HSMs"
subtitle: "云端 LiquidSecurity HSM 将吞噬世界"
date: 2022-12-05
source: https://newsletter.semianalysis.com/p/marvells-next-1b-business-is-security
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Marvell 的下一个 $1B 业务是安全——硬件安全模块（HSM）

> 原文：[Marvell's Next $1B Business Is Security – Hardware Security Modules HSMs](https://newsletter.semianalysis.com/p/marvells-next-1b-business-is-security) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**云端 LiquidSecurity HSM 将吞噬世界**

Marvell 有多个常被谈论的重要市场：存储控制器、电光器件、网络交换、网络处理器，以及面向超大规模云厂商的定制芯片。但 Marvell 有一个很少被讨论的市场——硬件安全模块，而它很可能成为 Marvell 一项 $1B 级别的业务。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/5866093a-ff16-4c75-a1c1-d296df862764_2000x972.png)

硬件安全模块（HSM）顾名思义，是用于防止敏感资料遭未授权访问的独立硬件设备。HSM 的设计目的是安全管理签名、加密和认证所用密钥的整个生命周期。密码学生命周期包含 6 项关键任务：

- 密钥生成（Provisioning）——HSM 创建密钥。密钥必须完全随机，否则攻击者就有可能通过分析硬件行为来预测密钥，进而攻破受保护的数据。
- 备份与存储——应制作并保存密钥副本，以防密钥泄露或丢失。密钥还必须被安全存储，并能抵御物理篡改。
- 部署——HSM 仅将密钥部署到经过授权的设备，并允许该设备用这把密钥去访问其被授权访问的数据。

- 管理——必须对密钥进行监控并在到期时轮换。已被攻破的设备必须撤销其访问权限。
- 归档——退役密钥放入离线长期存储，以便日后为冷存储中已加密的数据重新取用。
- 销毁——密钥被安全且永久地销毁，并应验证其确已销毁、未在任何其他地方留存。

传统 HSM 价格动辄数万美元，且主要部署在本地机房。它们并不太适合云以及大型多站点本地部署场景。它们通常是 1U 机箱设备，由企业自行管理。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/f687487b-88b4-41e1-9f63-ab254d892260_1871x967.png)

云计算让敏感数据的保护变得更加复杂。HSM 系统必须接入云的网络。云厂商最初提供的是自家的密钥管理服务，但这些服务无法跨混合云和多云环境使用。拥有混合云与多云基础设施的企业不得不应付多套密钥管理工具带来的复杂性，包括由此可能产生的安全漏洞。而如果继续使用本地 HSM，其基础设施又无法抵御宕机事故。

于是各大云厂商开始推出「密钥管理即服务」。HSM 成为托管在云计算平台上的虚拟设备，通过互联网访问，并在整个网络中部署缓存的 HSM。它能提供与物理 HSM 同等水平的安全性，同时兼具云服务带来的便利性与灵活性。由于企业无需购买昂贵的基础设施、也无需配备技术人员来维护，这种方式非常划算。借助这些服务化系统，加密密钥管理功能可以在数字边缘节点完成，从而将时延降到最低、提升应用性能。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/bf76270b-707e-449b-bc1a-19f47df42d4f_1801x979.png)

这正是 Marvell 凭借其 LiquidSecurity 产品线切入的地方。他们以 PCIe 卡的形式提供 HSM 硬件，可以取代传统的 1U HSM 模块，且资本开支与运营成本都大幅降低。通过云厂商部署的 Marvell 方案，企业可以按小时（约 $2）或按交易量（10,000 次更新约 3 美分，具体视云厂商而定）购买 HSM 服务。即便对许多大企业而言，这一成本也低于传统 HSM 基础设施。那些拥有自建基础设施的大型企业同样可以自行部署 Marvell LiquidSecurity PCIe 卡。

LiquidSecurity 产品线非常成功，客户覆盖 10 大云服务商中的 6 家、排名前 5 的社交媒体网站、多数头部 SaaS 公司以及多数领先的 OEM 和 ISV。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2aac0f92-5f16-4615-9f1c-0ab06cd2542e_1833x845.png)

Marvell 近期发布了 LiquidSecurity 2，带来了一些非常有趣的改进。从半导体的角度看，令人兴奋之处在于它与 Marvell 的 Octeon DPU 网络扩展卡以及 Octeon Fusion 5G 网络处理器共享大量架构设计。

这使得 Marvell 远远领先于其他硬件供应商。作为参照：去年 HSM 市场规模约为每年 $700M，其中云端 HSM 的份额约为 $120M。到 2027 年，HSM 市场应能轻松超过 $1B，而云端 HSM 份额应会接近 $600M。Marvell 主导着云端路线，非云端路线则很可能向私有云方向演进。这意味着到本十年末，Marvell 的 HSM 业务规模可能高达 $1B。

[分享](https://newsletter.semianalysis.com/p/marvells-next-1b-business-is-security?utm_source=substack&utm_medium=email&utm_content=share&action=share)

值得一提的是，这里所说的 HSM 不应与许多服务器主板上自带的本地 HSM 混为一谈。本文严格指的是服务于众多服务器的 HSM。顺带一提，这个领域有家很酷的初创公司 Axiado，他们正把管理 NIC、RoT（可信根）、本地 HSM 缓存和 BMC 集成到一颗芯片中，装进每一台服务器。

我们还希望简要讨论存储控制器、电光业务（DSP、TIA、驱动器）以及云端定制芯片业务上的出货量和/或市场份额流失。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
