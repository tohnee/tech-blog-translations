---
title: "亚马逊云服务基础设施效率低下，迫使 Twitch 削减分成，把创作者推向谷歌 YouTube"
title_en: "Amazon Web Services Infrastructure Inefficiencies Cause Cuts To Twitch Driving Creators To Google's YouTube"
subtitle: "超大规模云厂商各有不同的软硬件优势"
date: 2022-10-05
source: https://newsletter.semianalysis.com/p/amazon-web-services-infrastructure
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 亚马逊云服务基础设施效率低下，迫使 Twitch 削减分成，把创作者推向谷歌 YouTube

> 原文：[Amazon Web Services Infrastructure Inefficiencies Cause Cuts To Twitch Driving Creators To Google's YouTube](https://newsletter.semianalysis.com/p/amazon-web-services-infrastructure) · SemiAnalysis

**超大规模云厂商各有不同的软硬件优势**

亚马逊旗下的 Twitch.tv 视频流媒体平台近日宣布重磅变更，将创作者的分成从 [70/30 的收入分成砍至 50/50](https://blog.twitch.tv/en/2022/09/21/a-letter-from-twitch-president-dan-clancy-on-subscription-revenue-shares/)，引发轩然大波。此轮削减主要针对年平台收入超过 $100,000 的大型内容创作者。除了从创作者手中拿走更多收入之外，Twitch 还[限制特定地区的直播流质量，例如韩国](https://blog.twitch.tv/ko-kr/2022/09/28/%ED%95%9C%EA%B5%AD-twitch-%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8/)——而韩国拥有全球最好、成本最低的网络基础设施之一。令人震惊的是，在这两份公告中，Twitch 都把基础设施成本列为限制因素。与此同时，谷歌的 YouTube 不仅向创作者支付 70/30 的收入分成，还提供最高 4K 的更高质量和更高码率。

> 向全世界几乎每一个角落交付高清、低延迟、全天候可用的直播视频，成本高昂。把话题拉回到本博客的主题：我们没法在一个不赚钱的服务上继续运转。这不是缺陷，而是设计使然。
>
> —— Twitch 总裁 Dan Clancy

Twitch 最受欢迎的主播们已因此[掀起强烈反弹，多人表示将因此转投 YouTube](https://www.theverge.com/2022/9/26/23369070/twitch-revenue-split-70-30-streamers-reaction-amazon)。这些头部内容创作者与 Twitch 之间颇有对峙之势。我们不是媒体行业分析师，对此不作深入评论，但确实想谈谈亚马逊为何被迫采取这些激进措施。此外，我们还想解释为什么 YouTube 能够在提供 4 倍码率（每路视频流的数据量）的同时，仍有能力以更高的 70/30 分成盈利。

首先讨论亚马逊的通用视频流基础设施模型。主播将视频上传至 Twitch，视频随之被转码为多种格式，以适配用户观看 Twitch 内容的各类设备。

亚马逊根据其基础设施容量、直播观看人数及其他因素，动态选择转码方案。头部主播的直播流会被转码为多个不同画质档位，而低观看量的主播往往只能给观众提供单一画质预设。虽然没有公开资料说明亚马逊如何运营其内容分发网络，但我们了解到，他们在转码和服务条款审查的 AI 推理上混用 CPU、GPU 和 FPGA。这些视频以直播形式交付，并按创作者设置为提供 7 至 60 天的点播回放，到期后即从平台删除。

> 按亚马逊云服务 Interactive Video Service（IVS）——本质上就是 Twitch 视频——公布的费率，一位 100 CCU、每月直播 200 小时的主播，其直播视频成本每月超过 $1,000。我们通常不谈这个，因为坦率说，你本不必操心此事。我们更希望你专注于自己最擅长的事。但要完整回答「为什么不能 70/30」这个问题，无视交付 Twitch 服务的高昂成本就无法给出完整的答案。
>
> —— Twitch 总裁 Dan Clancy

谷歌与 YouTube 则采用截然不同的基础设施与产品模型。无论创作者体量大小，他们把收到的所有视频一律转码为多种格式。这些转码后的视频由自然语言模型自动生成字幕，而且永不删除。表面上看，这比亚马逊和 Twitch 的做法成本高得多，但在通用视频内容分发市场上，YouTube 的规模和盈利能力都超过亚马逊的 Twitch 平台。YouTube 在其直播业务和常规点播视频业务上均提供这些服务。

我们认为谷歌之所以能压低成本，靠的是更优的服务基础设施。首先，谷歌拥有[自研转码芯片](https://semianalysis.substack.com/p/google-new-custom-silicon-replaces)。正如我们过去所报道的，该芯片已迭代到第二代，[让他们得以削减数以百万计的 CPU 用量](https://semianalysis.substack.com/p/google-new-custom-silicon-replaces)！凭借这颗转码成本比 CPU 低 40 倍、比 GPU 低 20 倍的自研 ASIC，YouTube 始终能落在视频质量与码率（文件大小）曲线的最优点上，同时持续提供更好的观看体验。Twitch 则因为视频编码基础设施的限制，必须依赖计算强度较低的转码方式，因此经常在画质和观看体验上妥协。谷歌的服务条款审查与字幕生成也运行在[第二代及以后的自研转码芯片](https://semianalysis.substack.com/p/google-new-custom-silicon-replaces)上。

在给定码率下，YouTube 的视频画质几乎总是胜过 Twitch。这进而意味着，当 YouTube 内容分发网络提供的低码率流已能满足用户的主观画质要求时，用户往往会选择更低码率的 YouTube 而非 Twitch。由于拥有更专业的 ASIC 算力，YouTube 能节省数据中心方向的南北向带宽。[提醒一下，南北向带宽是数据中心最高昂的开销之一。](https://www.fabricatedknowledge.com/p/r2-what-it-means-to-be-1-less-than)谷歌 YouTube 的更高效率也使其基础设施比亚马逊 Twitch 更绿色、更环境友好。

YouTube 与 Twitch 盈利能力差异的另一面——这很可能也影响了二者功能差异与分成比例（70/30 对 50/50）——则要归结于 YouTube 的广告投放与推荐引擎质量。谷歌在其自研 TPU AI 芯片上训练的深度学习推荐系统（DLRS）是行业内最好的之一。虽然亚马逊也有自己的 DLRS 模型，但其定向精度似乎不及谷歌，这直接影响了广告费率。在我们看来，这更多归因于 AI 实力而非芯片本身，但值得注意的是，谷歌的 TPU 相比亚马逊的 Trainium 和 Inferentia AI 芯片要成熟得多。我们相信亚马逊正在开发自己的视频转码 ASIC，不过亚马逊也可以转向[第三方供应商 NetInt](https://semianalysis.substack.com/p/meet-netint-the-startup-selling-to)。

对超大规模云厂商而言，硬件是软件的延伸。虽然亚马逊凭借 AWS 云服务及自研芯片——例如[自研 Nitro DPU](https://semianalysis.substack.com/p/amazon-graviton-3-uses-chiplets-and) 和 [Graviton CPU](https://semianalysis.substack.com/p/amazon-graviton-3-uses-chiplets-and)——在云服务方面无疑成熟得多，但谷歌在 AI 与视频内容分发网络上明显领先。这些公司从不同的根基成长而来，其软硬件协同优化的路径自然大相径庭。有趣的是，谷歌正在补齐这套能力组合，以便在云业务上更有竞争力；而亚马逊则试图在视频内容分发网络以及面向广告网络的搜索/推荐 AI 上追赶。

如果你喜欢我们的内容，请分享！

[分享](https://newsletter.semianalysis.com/p/amazon-web-services-infrastructure?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[团体订阅享 8 折](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
