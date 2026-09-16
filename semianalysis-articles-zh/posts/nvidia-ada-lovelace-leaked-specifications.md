---
title: "Nvidia Ada Lovelace 泄露规格、裸片面积、架构、成本与性能分析"
title_en: "Nvidia Ada Lovelace Leaked Specifications, Die Sizes, Architecture, Cost, And Performance Analysis"
date: 2022-04-16
source: https://newsletter.semianalysis.com/p/nvidia-ada-lovelace-leaked-specifications
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# Nvidia Ada Lovelace 泄露规格、裸片面积、架构、成本与性能分析

> 原文：[Nvidia Ada Lovelace Leaked Specifications, Die Sizes, Architecture, Cost, And Performance Analysis](https://newsletter.semianalysis.com/p/nvidia-ada-lovelace-leaked-specifications) · SemiAnalysis

Nvidia 在 2 月底成为一次网络攻击的受害者，被黑客窃取了海量数据。这次攻击不仅对 Nvidia 是灾难，对[所有芯片公司以及所有「西方」国家的国家安全](https://semianalysis.substack.com/p/nvidia-hacked-a-national-security)亦是如此。在被窃数据中，有 Nvidia 下一代 GPU——Hopper 与 Ada——的详细规格与仿真数据。Hopper 现已出货，并由 Nvidia 在 GTC 上正式发布，其规格与此次泄露完全吻合；而以 Ada Lovelace 命名的 Ada 距离亮相还有数月。

Ada，即下一代客户端与视频专业 GPU，将是本文的主题。基于泄露的规格与仿真数据，SemiAnalysis 与 [Locuza](https://twitter.com/Locuza_/) 联手分析了其架构、各芯片的裸片面积，并对 GPU ASIC 做了成本分析。SemiAnalysis 与 [Locuza](https://twitter.com/Locuza_) 并未下载任何来自 LAPSUS$ 攻击的泄露文件，但网络上已有许多人分享了节选。

基于泄露内容的[这些](https://twitter.com/xinoassassin1/status/1498736671965077505)[节选](https://twitter.com/Xaymar/status/1499142875413721094)[片段](https://twitter.com/xinoassassin1/status/1498737774920232966)[摘录](https://twitter.com/xinoassassin1/status/1498850983052341249)，我们得以提取出 Nvidia 下一代 Ada Lovelace GPU 产品线的以下规格，并将其与当代 Ampere GPU 产品线对比。本文还有[一段配套视频](https://www.youtube.com/watch?v=cLMx5G8fpx0)，不想阅读的话可以去看！

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1414765a-6d42-4436-9158-e4071bcca163_1024x619.jpeg)

本文余下部分将展示每颗芯片的框图、架构分析、裸片面积估算、我们如何得出这些面积，以及一些成本与定位分析。鉴于 [Locuza](https://twitter.com/Locuza_) 与 SemiAnalysis 都直接依靠订阅者的支持，如果你能读完这篇无广告文章、订阅免费邮件列表、付费订阅或在财务上支持我们，我们将不胜感激！

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

[订阅 Locuza](https://www.patreon.com/locuza)

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/dcc2794c-0990-4910-92d6-4c7bf66d9a05_1024x597.jpeg)

Ada 架构的旗舰是 AD102，估算约 ~611.3mm2。相较上一代 GA102 是一次巨大跨越，新增 5 个 GPC 带来多 70% 的 CUDA 核心。显存位宽维持 384-bit 不变，不过我们预计显存速率会小幅提升到 21Gbps 至 24Gbps 一带。尽管有所提升，这仍不足以喂饱这头巨兽。AD102 拥有 96MB L2 缓存，远高于上代 GA102 的 6MB L2 缓存。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/4777d123-64cd-4bf2-8642-e6911d9134ed_1023x542.jpeg)

有意思的是，这与 AMD Navi 22 GPU 的「Infinity Cache」容量恰好相同。顺带一提，我们希望 Nvidia 把他们的大 L2 命名为「Nfinity Cache」，好捉弄一下所有人。AMD 的 Infinity Cache 是 L3 缓存，但尽管两家厂商的缓存层级不同，我们预计命中率的大趋势是一致的。在 AMD 的情况下，命中率为 1080p 下 78%、1440p 下 69%、4K 下 53%。这些高命中率有助于降低内存带宽需求。如果 Nvidia 的大 L2 以类似方式起作用，那么即便内存带宽增幅有限，也将极大地帮助喂饱 AD102。Ada 的顶级配置应搭载 24GB GDDR6X，但我们预计会有在此基础上阉割的配置。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c6c112c5-ba1d-4f52-9eaa-c35a59d1e463_1024x869.jpeg)

AD103 作为一款估算约 ~379.69mm2 的配置相当有意思。相比 AD102，这是一次大幅缩水。这可能是近年记忆中 GPU 一代里旗舰裸片与第二裸片之间最大的差距——AD102 的 CUDA 核心比 AD103 多出 70% 以上。

另一件有意思的事是，其 CUDA 核心数与当代旗舰 GA102 完全一致。显存位宽为 256-bit，远小于 AD102 的 384-bit 位宽。因此，基于 AD103 的游戏 GPU 显存上限为 16GB，但很可能存在阉割变体。尽管显存带宽远低于 GA102，64MB L2 缓存的加入仍将保证这颗 GPU 能被喂饱。

鉴于 Nvidia 将采用 TSMC 定制的「4N」节点，我们预计其频率能够高于 GA102。频率提升叠加架构进步，将使 AD103 的性能超过当代旗舰 RTX 3090 Ti——前提是 Nvidia 把它带到桌面端并放开功耗。值得注意的是，GA103 从未登陆桌面端，只出现在笔记本 GPU 的顶配上，因此这一幕在 Ada 一代也可能重演。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/124dc03a-abbd-45e2-9798-466ca279f916_933x1024.jpeg)

AD104 估算约 ~300.45mm2，是 Ada 产品线的甜点位，兼顾性能与成本效益。192-bit 位宽为游戏 GPU 带来 12GB 显存，容量足够高，同时把物料清单（BOM）控制在合理水平。与此同时，Nvidia GPU 的 104 设计往往拥有与上一代 102 相当的性能。如果这一趋势延续，其成本/性能比将非常出色。事实上甚至可能更强，因为 Nvidia 很可能相当大幅度地拉高频率，以超越 3090 的性能水平。我们预计 Nvidia 会把顶级 AD104 桌面 GPU（搭载 GDDR6X）推到 350W 乃至 400W。因此，我们预计这将是大多数发烧友最终购买的 GPU。这颗 GPU 也可以做到非常高效——在去掉 G6X 显存、频率回调之后。它在约 ~90W 到 ~135W 的笔记本战场上也应表现不俗。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/b9ad37db-8849-4b7d-a59b-0e97ec1ffb22_1024x682.jpeg)

AD106 是真正的大众市场 GPU，估算约 ~203.21mm2。它很可能是该产品线中出货量最大的 GPU，因为在 Pascal、Turing 和 Ampere 三代中，106 级 GPU 都是出货量最大的。由于 128-bit 位宽，它大多将搭载 8GB 显存。在顶级配置下，我们预计其性能与 GA104 相当，后者的顶配是 3070 Ti。鉴于 AD106 只有 3 个 GPC，而 GA104 有 6 个 GPC，这一假设可能有点过于乐观。这颗 GPU 也将是移动端出货量最大的 GPU。凭借 32MB L2 缓存，其缓存命中率很可能与 AMD 的 Navi 23 类似：1080p 下约 55%、1440p 下约 38%、4K 下约 27%。

在介绍本代最小的 AD107 之前，需要先铺垫一些背景。推特上来自泄露文件的数据并未标明这颗 GPU 的缓存大小。对于前述几颗 GPU，我们都按每个 64-bit 显存控制器/帧缓冲分区（FBP）配同样的 16MB 来假设。但对 AD107 这么假设说不通，因为其 GPC 数量与位宽完全相同，每 GPU 的 TPC 数也只降到了 4。如果 L2 缓存保持不变，裸片面积只会从 ~203.21mm2 降到 ~184.28mm2。这么小的降幅不足以在产品梯队中把两颗 GPU 拉开差距。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d617e1ad-8c55-4d49-8af0-48516d422cd6_1024x474.jpeg)

我们转而假设它与 Turing 代 GPU 的 TU116 和 TU106 之间存在类似关系。TU116 的每个 FBP 只有 0.5MB 的 L2 缓存，而非 TU10x 裸片的 1MB。如果我们套用每个 FBP 配 50% L2 缓存的同样模式，AD107 的估算面积约为 ~145.54mm2。这对于产品定位与成本来说合理得多。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/303c6a0e-c24f-4e51-b539-f35ea781ffd0_1024x941.jpeg)

基于这些假设，AD107 看起来是一颗优秀的移动 GPU。其 PCIe 被下调至 8 通道，因为用不到更多通道，而且 Nvidia 通常会把最底端的 GPU 降到这一通道数。它的性能足以碾压 Intel 最好的 Meteor Lake iGPU 配置，同时又足够便宜，能够进入一些成本更低的笔记本。

总体来看，Ada 是一条相当有意思的产品线。在梯队顶端，性能（与功耗）增幅相当大。AD102 的裸片面积与 GA102 相近，但采用的是更昂贵的 TSMC 定制 4N 工艺，而非更便宜的三星定制 8N 工艺。

相对三星的 8nm 衍生工艺，TSMC N4 衍生工艺带来的密度提升相当大，这足以证明其成本的合理性。有意思的是，尽管是更新得多的节点，SemiAnalysis 的消息源表示，在灾难性良率相近的情况下，TSMC N4 的参数良率实际上还略优于三星的 8nm 节点。这对 GPU 基本不构成问题，因为几乎每颗裸片都能通过良率分级加以收割利用。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/5aae4a3d-2141-4a55-ae66-9f689cc9eb2f_1024x359.jpeg)

Ada 产品线的其余部分，在裸片面积与整体 BOM 上则温和得多。在相同功耗下，性能普遍应高于 Ampere，而且尽管晶圆成本高得多，其制造成本反而更低。我们摆弄了许久的晶圆成本与裸片计算器，得出了一些成本估算，但 Nvidia 的成本终究只是终端售价的一部分。Nvidia 在裸片上加上自己的加价出售，并替 ODM/AIB 谈定显存价格。ODM/AIB 合作伙伴仍需购买并集成显存、供电元件与散热，且利润率想必微薄。

Nvidia 似乎在 L2 缓存容量与显存位宽之间实现了最优平衡。显存容量将保持合理，因为大多数 GPU 将搭载 16Gb 的 G6X 或 G6 显存颗粒。总体而言，AD104 在性能档位上接替 GA102，AD106 接替 GA104。显存成本相同，裸片的制造费用更低。得益于整体更佳的能效与更小的板卡，封装、散热与供电元件等板级组件更便宜。当我们在产品梯队中比较同一层级的裸片，例如 GA104 对 AD104，显存容量有所增加，但这是必要的——8GB 对该档位太少，而 16GB 又太贵。

不过，对高功耗的担忧需要被纳入考量。Nvidia 很可能像上一代那样，给每颗裸片猛灌功耗。实际上，我们可以想象他们会把功耗推到梯队中上一级裸片的水平，也就是说，顶级 AD104 配置达到 3080 的功耗水平，顶级 AD106 配置达到 3070 的功耗水平。传闻指向顶级 AD102 将打破 GPU 功耗的新纪录。

接下来，我们将拆解这些裸片面积估算的推导过程。裸片面积分析的第一步，是收集 Ada 相对 Ampere 的架构变化。SM 架构版本为 8.9 而非 8.6，因此大体上属于一代级别的改进。为此，我们假设 SM 面积增加 10%。我们并不确定 SM 架构的改动是什么，但可能包括 192KB 的 L1 缓存与张量核心。在我们看来，概率最高的变化是新增第三代 RT core。在 IO 方面，泄露表明 NVLink 已从产品线中完全移除，这表明 Nvidia 不打算把 Ada 产品线推向多 GPU 数据中心与专业可视化应用。我们预计将包含 PCIe 4.0/5.0、为更高速 GDDR6X 改进的显存控制器，以及 DisplayPort 2.0。更新版的 NVENC 和 NVDEC 很可能也在其中，应会把 AV1 编码带入阵容。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/e4d46186-41cd-477a-8aaa-019eb4cde502_1024x791.png)

Ada 最大的变化当然在于 L2 缓存。Nvidia 似乎不再沿用小 L2 缓存，而是取经 AMD 的 Infinity Cache 之道，在全线采用大得多的缓存。既然我们掌握了大部分规格，就可以用 Ampere GA102 的 IP 模块，拼出一颗规格与 AD102 相当的假想 GPU 裸片。这还没有计入某些变化，例如 SM 架构改动、更大的编码器模块、改用 PCIe 5.0、DisplayPort 2.0，或为 GDDR6X 调整过的显存控制器。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/e378b56b-3721-4089-b386-7c1d5a4b0f09_1024x585.jpeg)

用 GA102 的积木，我们得出这颗与 AD102 同配置、但采用 8nm 的假想 Ampere GPU 裸片面积为 1629.60mm2。你一眼就能注意到：L2 缓存大得惊人。AMD 在其 Navi 21 GPU 上有容量更大的 L3 Infinity Cache，但他们并没有为这块缓存分配这么大的面积。是的，AMD 用的是密度更高的 N7 节点，但那只是谜题的一小部分。密度差异的主要部分来自该 L2 缓存的版图与配置。

GA102 使用 48 个 128KB 的 SRAM 切片，每个 64-bit 显存控制器/帧缓冲分区（FBP）配 1MB L2。而 GA100 使用 80 个 512KB 的 SRAM 切片。这些更大的切片似乎大幅改善了密度，与 AMD L2 缓存的对比中可见一斑。GA100 的密度提升远不止工艺节点收缩所能解释的部分。AMD 的 L3 Infinity Cache 上也能看到同样的效应。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/0172902f-c75f-4881-8c5a-6ff3d3e6d0a3_1024x735.jpeg)

尽管 AMD 在设计的许多方面不如 Nvidia，我们相信他们在某些领域无疑更强，例如缓存与封装。我们认为这很大程度上源自他们 CPU 团队的血统。AMD 非常擅长为 GPU 打造极密的高性能缓存，其 Infinity Cache 即是明证。事实上，在我们的最终裸片面积估算中，Nvidia 的 96MB L2 在密度上仍远不及 AMD 的 96MB L3 Infinity Cache。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/68e56e2f-263b-413d-adec-a27cef7e5657_1023x490.png)

无论如何，仅靠从三星 8nm 缩到 TSMC 4nm，不足以让 GA102 的积木达到合理的裸片面积。相反，缓存设计需要一次架构上的重构。泄露告诉我们，AD102 现在每个 FBP 的 64-bit 显存控制器配 16MB L2。我们估计 Nvidia 将改用 48 个 2048KB 的 SRAM 切片。

有了这一缓存配置，我们就可以用这些数字计算理论缓存带宽。AMD 的 Navi 21 在 1.94GHz 下拥有 1.99TB/s 的 Infinity Cache 带宽。如果我们假设 Nvidia 在 AD102 上运行同样的 1.94GHz，那么其 L2 可实现 5.96TB/s 的带宽。最终产品的频率会有出入，但我们预计桌面端 Ada 大约在 2.25GHz 比较现实。我们预计 RDNA3 桌面端频率将超过 2.5GHz。Nvidia 做出的设计选择，是牺牲一部分密度来换取高带宽缓存。Nvidia 本可以引入每切片 8-16MB 的更高密度缓存，那大概能让其 L2 密度接近 AMD 的 Infinity Cache，但那会使 L2 带宽跌到低于 Ampere 的水平。归根结底，那恐怕不是一个选项。

我们估算出这种不同的缓存架构会对 AD102 积木中 L2 的面积造成何种影响，然后对 TSMC N7 应用一个收缩系数，再对 TSMC N4 应用另一个。SRAM 部分看来采用 60:40 的 SRAM 与逻辑比例，这影响了我们所采用的 SRAM 收缩系数。我们对 SM 施加了 10% 的放大系数，以计入 SM 处可能的架构变化，并根据各数字逻辑模块通常 30:70 的 SRAM 与逻辑构成，施加了不同的收缩系数。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/fb6203b2-e3d1-4b98-aca0-8b30f86cf1c0_1024x547.jpeg)

最后，我们保持裸片的模拟部分不变，因为其收缩会很小，而这些会被 PCIe 5.0、GDDR6X 显存速率和 DisplayPort 2.0 等会增加面积的潜在升级所抵消。这些数字中已移除 NVLink。最终，我们得出了 ~611.3mm2。这一结果与 [kopite7kimi 所称](https://twitter.com/kopite7kimi/status/1498860027754729477)裸片面积约 600mm2 的说法独立吻合。

获得整体概览之后，我们就可以着手配置产品线的其余部分。GPC 数量、TPC 数量、L2 容量、命令缓冲、各种 PHY、交叉开关等，都可以根据 GPU 配置动态缩放。我们选择的各收缩系数多少有些主观，是基于我们对 TSMC 官方说法与真实产品的反复揣摩，因此最终结果多少有点像是盲射。对于 AD107，我们略微回调了不同缓存架构的假设，因为它每个 FBP 的缓存更少。

总体而言，Ada Lovelace 在架构上似乎并未大幅偏离当前的 Ampere 架构，但它带来的改动——改进的光线追踪核心、改进的编码器以及更大的 L2 缓存——将大幅拉升性能，同时尽管采用更昂贵的 TSMC 定制 N4 基础节点，成本仍得以控制。Nvidia 延续传统，让整条产品梯队的显存容量保持均衡、逐级适度提升。L2

对比 AMD，传闻指向其梯队顶端性能非常之高，但成本也高。我们对他们的 Navi33 芯片更感兴趣，其定位应落在 AD104 与 AD106 之间。区间很大，但泄露指向它将在大众市场上成为一名有力的竞争者。AMD 目前在光线追踪性能上大幅落后，而且缺少 DLSS、Broadcast 等差异化软件功能，这确实损害其竞争力，但我们认为这将是十年来竞争最激烈的一代 GPU。

随着 Ethereum 2.0 给挖矿需求踩下刹车、消费者把支出组合从商品转向服务，GPU 价格正在快速下跌。这些因素叠加更高的通胀，意味着我们预测 Ada Lovelace（以及 RDNA 3）GPU 在 $400 到 $1,000 市场将提供相当不错的性价比。梯队顶端的产品大概率会有惊人的性能水平，但价格更高。简而言之：消费者赢了！

[分享](https://newsletter.semianalysis.com/p/nvidia-ada-lovelace-leaked-specifications?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

既然你读到了这里，如果喜欢这篇文章，不妨看看其他芯片分析，例如[我们对 Tenstorrent 及其硬件/软件路线图的深度解析](https://semianalysis.substack.com/p/tenstorrent-blackhole-grendel-and?s=w)。Tenstorrent 正是大名鼎鼎的 Jim Keller 目前担任 CEO 的公司！

[Tenstorrent Blackhole、Grendel 与 Buda——面向稀疏性、条件执行与动态路由的横向扩展架构](https://semianalysis.substack.com/p/tenstorrent-blackhole-grendel-and?s=w)

Locuza 在 GPU 裸片面积分析中功不可没。我强烈建议我们来自各半导体公司竞争分析团队的订阅者与他联系、与他合作！

[分享](https://newsletter.semianalysis.com/p/nvidia-ada-lovelace-leaked-specifications?utm_source=substack&utm_medium=email&utm_content=share&action=share)
