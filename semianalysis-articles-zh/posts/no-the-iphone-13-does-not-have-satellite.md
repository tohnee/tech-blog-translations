---
title: "不，iPhone 13 并没有卫星上网功能｜频段 n53 与 Globalstar（GSAT）解析"
title_en: "No, The iPhone 13 Does Not Have Satellite Internet | Band n53 & Globalstar (GSAT) Explained"
date: 2021-09-02
source: https://newsletter.semianalysis.com/p/no-the-iphone-13-does-not-have-satellite
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 不，iPhone 13 并没有卫星上网功能｜频段 n53 与 Globalstar（GSAT）解析

> 原文：[No, The iPhone 13 Does Not Have Satellite Internet | Band n53 & Globalstar (GSAT) Explained](https://newsletter.semianalysis.com/p/no-the-iphone-13-does-not-have-satellite) · SemiAnalysis

最近有传闻冒出来说 iPhone 13 将支持卫星上网。互联网和苹果粉丝圈为之疯狂，各种猜测满天飞，科技媒体也发布了一大堆文章。卫星服务公司 Globalstar 的股价从 8 月中旬的低点飙升了 90%。SemiAnalysis 已经听腻了围绕下一款 iPhone 卫星能力的那些荒唐臆想，所以下面我们把技术细节摊开来讲。

这个传闻的源头是郭明錤（Ming Chi Kuo），最优秀的苹果供应链分析师，但其他人把它发酵到失控。iPhone 13 的调制解调器将支持 n53 频段。这本身什么都不是。3GPP——5G 及其他电信标准的标准化组织——已将该频段纳入不断演进的 5G 标准。3GPP 之所以增加这个 n53 频段（2483.5MHz 至 2495MHz 共 11.25MHz 频谱），并非为了显式的卫星连接，而是因为 Globalstar 正推动将其用于地面用途。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/94ae3d16-4a28-417c-b6d4-f6a57b01e498_1023x769.png)

因此，高通已在其下一代调制解调器中实现了对该频段的支持。苹果的调制解调器由高通供应，虽然他们不一定使用高通市面上在售的调制解调器，但拿到的定制版本遵循同样的路线图。iPhone 拿到一颗支持该频段的调制解调器，本身并不稀奇。几十年来，2.4GHz WiFi 路由器只要稍作修改就能使用这一频段，因为其工作频谱与之极为接近。这段频谱本来就干扰横行：越出正常工作范围的 WiFi 和蓝牙，还有微波炉泄漏。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c786cad6-e3b0-40b2-99b2-bcd93512c31d_1024x895.png)

就算调制解调器乃至射频前端支持 n53 频段，也不意味着它就能连接到任何在该频率上广播的东西。把信号发送到手机、并被手机天线接收，是非常困难的。要让手机原生、可靠地连接卫星，卫星必须大幅提升发射功率和接收灵敏度。这对 Globalstar 来说不可能做到——他们已经很久没有发射任何新卫星了，目前也没有发射计划。

另一条路是手机必须配备增益显著更高的天线。射频天线设计在不断演进，但把这类天线塞进智能手机的机身里，目前不在可行范围之内。在满足手机约束的前提下部分接近是可能的，但这种设计无法达到持续连接所需的可靠性。[彭博社指出，该服务的连接极其不可靠。](https://www.bloomberg.com/news/articles/2021-08-30/apple-plans-to-add-satellite-features-to-iphones-for-emergencies)

> 苹果设计了一套机制，会提示用户走到户外并朝特定方向走动，以帮助 iPhone 连上卫星。连接网络也不会总是即刻完成，对该功能的测试显示，有时需要长达一分钟才能奏效。

最可能的出路，也是 Globalstar 自己宣称的那条，是将这段频谱授权用于地面用途。他们已经获得美国 FCC 及全球其他监管机构对地面服务的批准。如果 Globalstar 与某家大型运营商达成协议，后者就可以把 n53 频段加到现有基础设施上。大量基站和小基站上的设备需要做一些改造，但它的用法会和你手机目前使用的任何其他 sub-6GHz 频段一模一样。他们还瞄准利用这段频谱进行专网部署。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/966cf0a2-cb8b-49d2-90b4-4820a573c85f_1024x778.png)

Globalstar 相信，其超过一半的营收将来自地面频谱授权。这家「卫星公司」实际上只是一家无线频谱分销商和套利者。其卫星基础设施在他们未来营收预测中只占少数。苹果与 Globalstar 达成交易的可能性当然存在，但这并未被计入他们未来的营收。iPhone 13 不使用 Globalstar 卫星的铁证，正是那些卫星本身。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/12057979-4673-43eb-b70d-82a184ce3d0b_1024x768.png)

Globalstar 的卫星发射于 2010 年至 2013 年。其网络早已建成，设计寿命 15 年。这意味着它们的设计寿命不会超过 2025 年至 2028 年。当然有可能撑得更久，但 Globalstar 没有发射更多卫星的计划。更何况，这些现有卫星的能力也十分有限。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/de62b83c-7bbc-4d3b-a114-10de0504c140_1024x768.png)

根据 Globalstar 自己的说法，其能力最高可达 256kbps（32KB/s）。这还是要在无遮挡的理想条件、配合高功率高增益天线的情况下。即使在这个射频子系统被微型化塞进智能手机的完美世界里，也远远不够用现代互联网。我们上面链接了一篇彭博社的文章。仅仅打开它并滚动阅读，就下载了 10.4MB 数据——这还没算播放内嵌视频。在完美条件下，下载一篇简单的文章需要 5 分 25 秒。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/42eda311-febf-405b-a1f9-d0ffb8d2682c_916x617.png)

任何有射频经验的人都知道，峰值能力通常——或者说从来——达不到。这个 256kbps 是一个极其乐观的读数。更何况 Globalstar 的卫星网络已接近使用寿命的终点。他们的长期营收预测主要归于将 n53 频段授权用于地面服务。很显然，苹果在长期上确实在研发卫星上网能力，但这不会来自 Globalstar 现有的卫星。Globalstar 股价近期的一飞冲天，几乎完全站不住脚。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

[分享](https://newsletter.semianalysis.com/p/no-the-iphone-13-does-not-have-satellite?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[发表评论](https://newsletter.semianalysis.com/p/no-the-iphone-13-does-not-have-satellite/comments)

*本文最初于 2021 年 9 月 2 日发布于 [SemiAnalysis](https://semianalysis.com/no-the-iphone-13-does-not-have-satellite-internet-band-n53-globalstar-gsat-explained/)。*

*SemiAnalysis 的客户及员工可能持有本文所提及公司的仓位。*
