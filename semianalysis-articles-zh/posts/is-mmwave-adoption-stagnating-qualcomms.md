---
title: "毫米波普及停滞了吗？高通 $6B 机会更新与 $QCOM EPS 预估"
title_en: "Is mmWave Adoption Stagnating? Qualcomm's $6B Opportunity Update, $QCOM EPS Estimates"
subtitle: "iPhone 14、Jio、三星与 Meta 更新"
date: 2022-09-08
source: https://newsletter.semianalysis.com/p/is-mmwave-adoption-stagnating-qualcomms
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 毫米波普及停滞了吗？高通 $6B 机会更新与 $QCOM EPS 预估

> 原文：[Is mmWave Adoption Stagnating? Qualcomm's $6B Opportunity Update, $QCOM EPS Estimates](https://newsletter.semianalysis.com/p/is-mmwave-adoption-stagnating-qualcomms) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**iPhone 14、Jio、三星与 Meta 更新**

毫米波（mmWave）曾被吹捧为能带来惊人网络吞吐量的技术，但迄今为止的普及情况乏善可陈。毫米波技术的领导者高通（Qualcomm）在射频前端坐拥高达 $6B 的机会。这 $6B 需要毫米波在日本、中国、韩国、欧洲和印度广泛普及才能兑现。尽管机会巨大，毫米波手机却始终被局限于美国市场。昨天发布的 iPhone 14 再次印证了毫米波「只有美国在用」的现状，但近期 Jio 的公告指向了一种可能的加速。我们还将分享一些关于高通与三星、Meta 关系及销售的独家细节，包括芯片层面的信息，以及 Meta 自研 SoC 的最新进展。

今年早些时候，[我们报道了高通在今明两年 iPhone 的调制解调器、收发器、包络跟踪器、PMIC、滤波器和毫米波天线设计竞标中的处境](https://semianalysis.substack.com/p/qualcomm-rffe-update-8b-by-2025-2023)。苹果（Apple）每年在连接芯片上的支出约 ~$14.4B。如果每部 iPhone 都搭载毫米波，将为高通带来约 ~$3B 的 RFFE 营收。当然，2021 年只有约 4,400 万部 iPhone 搭载毫米波出货，另有约 1.96 亿部没有。2021 年苹果出货约 2.4 亿部 iPhone，加权平均每部手机的连接芯片内容价值约 ~$58.3。约 4,400 万部 iPhone 搭载毫米波出货，约 1.96 亿部没有。每部 iPhone 的毫米波内容价值约 ~$12.10。在安卓阵营，高通在部分机型上见过高达 $18.4 的内容价值，但平均值更低。特别感谢移动行业分析最细致的 [Sravan Kundojjala](https://twitter.com/SKundojjala) 帮我们框定其中一些数字。

我们还抓取了各国 Apple.com 网站，以确定哪些 iPhone 14 机型支持毫米波。

不意外，还是只有美国版机型才有毫米波。

毫米波的普及前景依然不妙，因为许多人原本预期日本会采用毫米波。说到日本，瑞萨（Renesas）有一些有意思的毫米波前端产品，随着联发科（MediaTek）进军支持毫米波的基带，这些产品可能开始抢占一些份额。反过来看，毫米波普及也有一些边际向好的消息。

印度最炙手可热的电信公司 Jio 上周发布重磅公告，将投资 $25B 于 5G 和毫米波。Jio 于 2016 年下半年上线，其现代化 4G 网络建立在 O-RAN 等理念之上。到 2020 年，他们已迅速攀升为印度第一大移动运营商，用户超过 4 亿。印度移动数据每 GB 成本全球最低，正是拜 Jio 所赐。他们靠的是向网络砸下数百亿美元。近来其投资有所放缓，但基于最新消息，他们看起来要重新踩下油门。

[Jio 的频谱极度匮乏。](https://dot.gov.in/sites/default/files/Access%20Spectrum%20Holdings%20of%20TSPs%20as%20on%2008-07-2022.pdf)在最近的频谱拍卖之前，人们常这么说美国的 Verizon。而 Verizon 是全球最大的毫米波部署方。有意思的是，若按低频与中频频谱的每 MHz 客户数或数据量计算，Jio 反而是领头羊。印度的移动数据消费增长极快，Jio 的网络容量正撞上砖墙。他们要么收购更多低频和中频频谱，要么转向毫米波。

Jio 近期拍下了相当大一块 700MHz 频谱，但他们在频谱充裕且便宜的毫米波上也选择张开双臂拥抱。他们将在印度 1,000 个城市部署 5G，包括利用毫米波小基站提供高出数个量级的网络容量，目标是 1 亿户[固定无线宽带](https://onlytech.com/jio-airfiber-home-gateway-unveiled-at-reliance-agm-can-it-replace-wired-home-broadband/)家庭连接。

随着 Jio 斥资 $25B 的巨额投资，印度看来要在高端市场开始采用毫米波。而高端市场正是高通的天下。从 2023 到 2025 年，毫米波将开始在印度、日本和韩国部署，这一点似乎已经清晰。中国的毫米波计划我们仍无把握——我们的观点几乎每周都在「会做」与「不会做」之间摇摆。

如果你喜欢我们的内容，请分享！帮忙传出去！

[分享](https://newsletter.semianalysis.com/p/is-mmwave-adoption-stagnating-qualcomms?utm_source=substack&utm_medium=email&utm_content=share&action=share)

我们还想聊聊高通的股票。它已被打趴，移动行业销售显著放缓，促使我们的咨询客户要求对该股做更深入的分析。这不是独家委托，所以我们可以分享一部分我们关于未来两年营收和 EPS 预估的内容。我们还会对部分业务板块做一些点评，包括与三星和 Meta 关系以及未来 SoC 的独家细节。

[团体订阅享 8 折](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
