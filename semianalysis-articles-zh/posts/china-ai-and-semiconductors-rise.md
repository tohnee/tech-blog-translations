---
title: "中国 AI 与半导体的崛起：美国制裁已然失效"
title_en: "China AI & Semiconductors Rise: US Sanctions Have Failed"
subtitle: "华为、SMIC、7nm、H800、本土 AI 能力、ASML、联发科、高通、苹果、射频能力、潜在制裁"
date: 2023-09-12
source: https://newsletter.semianalysis.com/p/china-ai-and-semiconductors-rise
crawled: 2026-09-15
authors: ["Dylan Patel", "Afzal Ahmad", "Myron Xie"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 中国 AI 与半导体的崛起：美国制裁已然失效

> 原文：[China AI & Semiconductors Rise: US Sanctions Have Failed](https://newsletter.semianalysis.com/p/china-ai-and-semiconductors-rise) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**华为、SMIC、7nm、H800、本土 AI 能力、ASML、联发科、高通、苹果、射频能力、潜在制裁**

随着[10 月 7 日对华制裁](https://www.semianalysis.com/p/china-and-usa-are-officially-at-economic)临近一周年，出口管制正在失效这一点已经昭然若揭。拜登政府宣称的目标是限制中国企业制造最高端芯片的能力，包括 AI 芯片以及其他可能被中国共产党用于恶意用途的技术。美国的理由陈述如下。

> 中华人民共和国（PRC）正在迅速发展百亿亿次（Exascale）超算能力，并已宣布其意图在 2030 年前成为世界 AI 领域的领导者。

> 这些系统正被 PRC 用于其军事现代化建设，以提升其军事决策、规划与后勤以及其自主军事系统（例如用于认知电子战、雷达、信号情报与干扰的系统）的速度与准确性。此外，这些先进计算物项与「超级计算机」正被 PRC 用于改进武器设计与测试（包括大规模杀伤性武器（WMD），如核武器、高超声速武器及其他先进导弹系统）中的计算，并用于分析战场效果。另外，依托对海量数据的高效处理而实现的先进 AI 监控工具，正被 PRC 无视基本人权地用于监控、追踪与监视公民等目的。

> 限制 PRC 获取先进计算芯片、或进一步发展违背美国国家安全与外交政策利益的用途的 AI 与「超级计算机」能力。

> [美国 2022 年 10 月管制措施](https://www.federalregister.gov/documents/2022/10/13/2022-21658/implementation-of-additional-export-controls-certain-advanced-computing-and-semiconductor)

然而，华为在 SMIC N+2（7nm）制程上发布的新旗舰芯片、中国企业持续进口数十亿美元的先进半导体制造设备，以及[采购数十万颗强大的 NVIDIA H800 与 A800 芯片](https://www.semianalysis.com/p/nvidias-ramp-volume-asp-cloud-pricing)，都清楚表明：商务部所设定的标准，处在一个最终无法阻止中国突破去年秋天所设壁垒的水平。

在本报告中，我们将探讨华为这颗芯片所集中折射出的中国本土半导体制造与 AI 能力的走向。我们将覆盖：

- 华为的芯片及其与国外芯片的竞争力对比。
- 华为芯片自研自供对苹果、高通与联发科的市场份额/ASP/营收影响。
- SMIC N+2（7nm）工艺技术、当前产能与扩产计划。
- 他们使用的光刻设备，以及为什么现行限制形同虚设。
- SMIC 未来 5nm 制程节点的可能性。
- 使用英伟达等境外生产芯片的本土 AI 能力。
- 使用本土制造的 AI 芯片。
- 用于无人机与探测 F-35 的射频能力。
- 最后，如果美国及其盟友对这一总体走向感到不安，还有一揽子针对前端设备、化学品、先进封装与 IP 授权的西方对华潜在反制选项，足以将中共彻底排除在外。

## **华为麒麟 9000S**

让我们直接从当下的焦点话题开始：由 SMIC 生产的华为麒麟 9000S。该芯片采用定制 Armv9 核心以及华为自研的定制 GPU 架构。能够在中国设计出先进架构，意义重大。虽然美国过去曾阻止 [AMD](https://en.wikipedia.org/wiki/AMD%E2%80%93Chinese_joint_venture) 与 [Intel](https://www.theregister.com/2015/04/10/us_intel_china_ban/) 的多项对华 CPU 交易，但未能对 Arm 做到这一点。部分原因在于 Arm 在中国设有一家[不受其直接控制的合资企业](https://www.reuters.com/markets/deals/arms-china-relationship-complicates-ipo-2023-08-22/#:~:text=Arm%20itself%20holds%20an%20effective,48%25%20of%20the%20Chinese%20subsidiary.)。另一个原因是 Armv9 指令集出自英国剑桥的 Arm。此外，他们使用了 Arm 授权的 A510 核心，该核心由 Arm 位于法国索菲亚（Sophia）的研发中心与剑桥的团队设计。

这颗芯片在技术上令人惊叹。[多项测试中的性能与功耗表现](https://twitter.com/tphuang/status/1698299732060262676)使其与 1 至 2 年前的高通芯片（S888 与 S8G1）处于同一水平。其射频部分极为出色，集成调制解调器与高通当前最佳水平相当。鉴于华为在被禁止使用台积电之前曾略微领先高通，这并不令人意外。最重要的一点是，其射频前端芯片同样为本土生产，而这一能力曾被许多人认为是中国所欠缺的。

最令人震惊的发现是：[在完全相同的 IP 上直接对比，即 Arm A510](https://twitter.com/tphuang/status/1698885806545387705)——华为麒麟 9000S 基于 SMIC N+2（7nm），2022 年高通 S8G1 基于三星 4LPX 工艺——尽管存在制程代差，两者 Arm A510 核心的性能与功耗实际上不相上下，这表明 SMIC N+2 比西方多数人认识到的更好。这些芯片如此接近的部分原因，在于[三星的糟糕良率](https://www.semianalysis.com/p/samsung-electronics-cultural-issues)与 SMIC 的良好[良率](https://www.semianalysis.com/p/embracing-chaos-the-imperfect-art)。

简而言之，麒麟 9000S 是一颗设计得比西方所认知的更为出色的芯片，性能与功耗都很扎实。即便出口管制乏善可陈，这仍是一颗先进制程芯片，放在 2021 年也接近第一梯队——而它是在无法获得 EUV、无法获得尖端美国 IP、且被刻意设限的情况下完成的。我们无论怎样强调这件事的严重性都不为过。

## **对联发科、高通与苹果的影响**

量化对苹果的影响相当容易。2019 年末的华为禁令直接为苹果带来了约 3,500 万至 4,500 万部 iPhone 销量。如果华为能够重拾昔日地位，这笔每年轻松超过 200 亿美元的苹果营收便可能化为乌有。这还只是智能手机；对苹果而言，平板电脑、智能手表与笔记本电脑所受的影响会更大。

对联发科与高通的冲击更甚。华为禁令之后，每年 1.9 亿颗华为 SoC 销量从市场上蒸发，高通与联发科是主要受益者。从 2020 年至今，这部分份额转移到了小米、OPPO、vivo 等其他中国厂商手中。若华为恢复元气，我们测算对联发科与高通的营收影响最高可达 76 亿美元。

![](https://substack-post-media.s3.amazonaws.com/public/images/81134e50-75fc-4d17-88d5-9b90f8e08437_1376x366.png)

当然，这发生在一个年出货 14 亿部智能手机的市场，而当前的运行率不足 12 亿部。针对上述问题的更细致分析，以及射频前端（RFFE）对 Skyworks、Qorvo、Murata、高通等公司的影响分析，已向我们的客户开放。

华为能否重拾状态，主要取决于 SMIC 的制造能力，而我们相信其实力非常强。

## **SMIC N+2：真正的 7nm，良率良好**

就密度而言，这是一个真正的 7nm 工艺。尽管在具体层间距（pitch）上的工程决策与台积电 2018 年的 7nm 不同，它仍应被视为同级别的工艺技术，SMIC 最多只落后台积电几年。甚至可以说，尽管受到限制，SMIC 距离英特尔与三星至多也只有几年之遥。由于 SMIC 是在复制他人已走过的路，加上中国大陆优秀的工程师人才库，以及许多从台积电跳槽而来、被大力招揽的台湾工程师，差距可能更小。

如前所述，它在性能与功耗上与三星 4LPX 相当。关键问题是[良率](https://www.semianalysis.com/p/embracing-chaos-the-imperfect-art)与产量。虽然一些评论人士声称良率只有 10%，我们不相信。事实上，我们认为 SMIC 的工艺良率良好。这里没有确切的数字，但有一些数据点可以佐证。

为什么？我们从中国的消息人士那里听到了一些软性说法，称良率不错。据称其 D0 目前约为 ~0.14。作为参照，台积电的 N5 与 N6 节点大约是这个数字的一半。台积电当然是黄金标准，三星/英特尔的「7nm」更接近一些，但仍领先于 SMIC 当前达到的水平。良率已经达到这样的水平，是一个强烈的信号，表明 SMIC N+2 工艺技术是健康的且在持续进步。参数良率（parametric yield）则是更重要却未知的指标。但仅凭传闻还不够。

更实在的证据是，其 FinFET 的沟道、栅极与源漏，以及接触孔和下层金属层看起来相当干净。良率低的工艺不太可能呈现如此均匀的形貌。参见 [TechInsights](https://techinsights.com/) 公开简报中的这些图片。我们建议阅读其完整拆解报告，以获取更多图片与精确的层间距数据。

最后一个原因与该芯片明显的分档（binning）策略有关。半导体制造中的「binning」（分档）是指集成电路（如 CPU 或 GPU）在制造并测试完成后，按性能与质量进行分拣归类的过程。芯片可能存在缺陷晶体管（即灾难性良率损失），但在很多情况下，功能完好的晶体管仍无法通过各种性能与功耗测试，这被称为参数良率。如果一种工艺的参数良率偏低，负责芯片良率管理的厂商可以放宽分档标准来「改善」参数良率——更多芯片能通过各种测试，但也会带来更大的个体差异。

过去那些良率不佳的移动芯片就曾这样处理，例如三星 4LPX 上的高通 S8G1。就 S8G1 而言，同一颗芯片的不同设备在完全热饱和、相同环境条件下差异可超过 10%。虽然我们尚未见到对多台设备在相同环境下的严格测试，但中国各大论坛上的信息足以表明设备间的差异相当小。

以上没有一条是铁证，但我们认为 SMIC 良率良好，某些评论人士所说的 10% 良率是无稽之谈，是在刻意淡化这件事的意义。这是一个真正的大规模量产工艺技术。正如苹果充当台积电新制程节点的「小白鼠」、帮助其爬坡并实现高良率一样，华为也将以同样的方式帮助 SMIC。

提醒一下，华为曾发布[台积电 N5 量产的首颗芯片](https://www.anandtech.com/show/16156/huawei-announces-mate-40-series)，所以这是他们完全有能力扮演的角色。两年之内，SMIC 很可能能够为 AI 与网络应用生产大面积单片裸片。这与[博通](https://www.semianalysis.com/p/broadcoms-google-tpu-revenue-explosion)和英伟达转向新制程技术的时间尺度相当。

要更好地理解良率，请阅读我们的入门科普与其他相关文章：[1](https://www.semianalysis.com/p/lam-research-tokyo-electron-jsr-battle)、[2](https://www.semianalysis.com/p/die-size-and-reticle-conundrum-cost?utm_source=%2Fsearch%2Fasml&utm_medium=reader2)、[3](https://www.semianalysis.com/p/i-semiconductor-the-regionalization?utm_source=%2Fsearch%2Fasml&utm_medium=reader2)、[4](https://www.semianalysis.com/p/lithography-intensity-and-long-term?utm_source=%2Fsearch%2Fasml&utm_medium=reader2)、[5](https://www.semianalysis.com/p/asml-and-the-semiconductor-market?utm_source=%2Fsearch%2Fasml&utm_medium=reader2)、[6](https://www.semianalysis.com/p/the-gaps-in-the-new-china-lithography?utm_source=%2Fsearch%2Fasml&utm_medium=reader2)、[7](https://www.semianalysis.com/p/austrias-silent-monopolies-on-advanced)。

## **SMIC 的设备与工具**

这源于他们能够使用与台积电、英特尔「7nm」工艺几乎完全相同的设备。虽然理论上存在设备管制（[参见我们去年对美国芯片制裁的深度解析](https://www.semianalysis.com/p/nvidias-ramp-volume-asp-cloud-pricing)），实际上却形同虚设。

尽管 SMIC 的 N+1 工艺技术已经违反制裁，美国仍继续向使用美国技术的半导体制造设备公司发放许可证。SMIC、CXMT 以及许多与解放军直接合作、追求超越制裁限制的工艺技术的中国公司，仍在继续进口他们需要的任何设备。实际上禁令形同不存在，美国商务部工业与安全局（BIS）与国务院的最终用途核查正在失效。

应用材料（Applied Materials）、泛林半导体（Lam Research）、东京电子（Tokyo Electron）、KLA、Screen、ASM International、Kokusai 等设备公司，基本上在向中国销售其全部产品线。这是因为用于 7nm 甚至 5nm 的大多数沉积、刻蚀、量测、清洗、涂胶显影、离子注入、外延等设备，同样可以合理地用于 28nm。这些设备以「28nm」名义卖给 SMIC，但实际上 SMIC 当着这些公司的面撒谎，将其用于 7nm。

虽然 SMIC 在扩产 28nm 及其他成熟制程，但实际规模远小于其宣称，因为这些设备被调往了先进制程。甚至这些设备公司内部可能有人知道正在发生什么，却睁一只眼闭一只眼。

出口管制正在失效。它们没有得到执行，现状仍在延续。

## **光刻设备**

光刻领域与上述其他设备略有不同。对特定 DUV 光刻机确实存在一些限制，但问题在于，这些限制对阻止 7nm 毫无意义。[我们在今年 1 月曾详细讨论过这些问题](https://www.semianalysis.com/p/the-gaps-in-the-new-china-lithography)，这里简要重述。

中国能够、也将能够用目前获准的光刻设备为 7nm 产能爬坡。NXT: 1980i 以及改进版 Di、Ei、Fi 机型在现行限制下仍可进口并可获得服务。最初的 1980i 正是台积电用于将 N7（7nm）以极高良率爬坡到每月超过 10 万片晶圆的机型。1980i 系列也曾被英特尔用于其「7nm」。

这个漏洞对熟悉这个行业的人来说一目了然。这是无效政策的完美例证：宣称的目标是阻止进一步发展，却给中国留下了一个可以随意利用的明显漏洞。ASML 继续从中受益，并规划大幅增加 DUV 出货，其中主要由这些「较老」的机型构成。

## **SMIC 产能并未受限**

SMIC 7nm 工艺有超过 60 层光刻层。其中只有约 40 层是关键层，但为稳妥起见，我们不妨假设 60 层全部需要最新的 1980 系列设备。实际上，较老的 ArFi 设备（例如尼康等厂商的机型）以及 ArF/KrF/I-Line 光刻机可用于其中若干层。

ASML 声称最新的 1980Fi 每小时可完成 330 层光刻，但我们认为这有点乐观，是按低曝光剂量计算的。保守起见，假设 [SMIC 使用的剂量是 ASML 所称的 2 倍](https://www.semianalysis.com/p/die-size-and-reticle-conundrum-cost)，且其机队以 Di 而非 Fi 为主。这意味着每台设备每小时可完成约 165 层。

我们听说 SMIC 已拥有远超 30 台来自 ASML 的先进 ArFi 设备，还有更多光刻机在订购中，包括最新的 1980Fi。这些设备支撑其全部制程节点，但可用于 7nm 和 5nm。我们还听说，其首座 7nm 晶圆厂将共配备 15 台 ArFi 设备，并在 2024 年二季度末完成全部装机，之后还需几个季度爬坡。传闻称其下一座晶圆厂规模更大。更多来自中国的传闻称，首座晶圆厂将拥有每月 5 万片（WPM）的 7nm 产能，但我们最初听到这一说法时觉得这个数字大得离谱。

虽然无法核实这些来自中国的说法，但 SMIC 在不从其他成熟制程厂调配设备的情况下，在其 7nm 厂爬坡到 3 万 WPM 的实际产量，看起来是非常轻松的。

![](https://substack-post-media.s3.amazonaws.com/public/images/552c0ab9-4423-4787-b87c-911450ab6134_2528x394.png)

这与乐观的 5 万 WPM 说法相吻合——前提是需要 1980i 的层数降到 50 层，且使用的剂量更接近 ASML 所称的水平。

即便良率只有 50%，每月 3 万片晶圆也足以每年支撑超过 1,000 万颗英伟达 H100 GPU ASIC 裸片。[先进封装](https://www.semianalysis.com/p/ai-expansion-supply-chain-analysis)（[类似 CoWoS](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and)）或[高带宽内存（HBM）](https://www.semianalysis.com/p/ai-expansion-supply-chain-analysis)所用的设备目前也均未受限。就产能而言，木已成舟。

## **5nm 是可能的**

ASML 正在将产能爬坡至每年出货超过 400 台 ArFi 设备，[并宣称到 2025 年 DUV 设备年产能达到 600 台](https://www.semianalysis.com/p/asml-and-the-semiconductor-market)。其中超过一半的产能已预留给来自中国晶圆厂的需求。虽然这些设备将广泛分发给众多公司，但 SMIC 是 ASML 在中国最大的单一客户。

[ASML 公开表示，这明确对应着到 2030 年每月超过 150 万片的过剩/低效晶圆产能](https://www.semianalysis.com/p/asml-and-the-semiconductor-market)，且每年新增 15 万 WPM 的过剩/低效产能。ASML 称这是[半导体供应链区域化](https://www.semianalysis.com/p/asml-and-the-semiconductor-market)所致，但这只是托辞，实情是[中国正在实现半导体自主](https://www.fabricatedknowledge.com/p/chinese-evs-and-the-lagging-edge)并用 DUV 冲击 5nm。

需要说得非常清楚：[根据 ASML 上一次投资者日的说法](https://www.semianalysis.com/p/asml-and-the-semiconductor-market)，[「中国将实现半导体自主」这一点已明确写入 ASML 的产能规划与预测](https://www.semianalysis.com/p/asml-and-the-semiconductor-market)——这里指的是半导体制造环节。当然，供应链的其余环节——设备、耗材与设计 IP——仍然高度交织。

用 ArFi 多重图形化（multi-patterning）实现每平方毫米超过 1.3 亿颗晶体管、且有高良率的「5nm」工艺，是完全可行的。[1980i 系列的套刻（overlay）精度足以以可接受的良率制造 5nm。](https://www.semianalysis.com/p/the-gaps-in-the-new-china-lithography)

考虑到政府补贴的力度，SMIC N+3「5nm」工艺的生产也将具有经济性。据我们估计，缺乏 EUV 将使总光刻成本增加 55% 至 60%，但请记住，[目前 5nm 的工艺总成本中光刻只占约 30%](https://www.semianalysis.com/p/die-size-and-reticle-conundrum-cost)。这意味着，相对使用 EUV 的 5nm，总工艺成本仅会高出约 20%。良率可能受损，因此实际数字会更高（每片晶圆的缺陷芯片更多），但这对中国而言并非不可逾越的障碍。

如果现行限制不变，我们预计华为与 SMIC 将在 2025 或 2026 年推出真正的 5nm 芯片，随后不久便会出现大规模 AI 芯片。现行出口管制并未限制中国的制造能力或产能。

## **中国的 AI 能力**

制造能力并非遥不可及，而即便没有这些本土制造能力，中国的 AI 能力也将极为强大。到 2024 年底，中国总计将拥有超过 100 万颗来自英伟达的 A100 级或更好的芯片。请记住，[GPT-4 是在约 24,000 颗 A100 上训练的](https://www.semianalysis.com/p/gpt-4-architecture-infrastructure)，而且[即便到明年年底，OpenAI 所拥有的先进 GPU 也将不足 100 万颗](https://www.semianalysis.com/p/google-gemini-eats-the-world-gemini)。

现行的 AI 管制充其量是松垮的。英伟达迅速推出了 A100 与 H100 的新版本——A800 与 H800——能力实际上不分上下。这些 GPU 没有削减总算力或内存带宽。虽然 NVLink 速度被砍到 400GB/s，但对于目前采用的多数并行策略——如 8 路张量并行、全分片数据并行（FSDP）与流水线并行——并不构成限制。这些削减同样无法通过最终用途核查来验证，而且如果硬件未做熔断，理论上可以像英伟达以前的挖矿算力限制器那样被逆向解除。

此外，对于部署数万颗 H100 的最高端系统，每颗 GPU 与本服务器之外网络中其他 GPU 之间仅使用 50GB/s 的以太网/InfiniBand IO。而管制的门槛是芯片间总 IO 达到 600GB/s。在现行有缺陷的制裁下，比 H100 更强的芯片完全可以在境外制造并合法进口。例如，一颗理论上的 3nm 芯片，FLOPS 为 H100 的 10 倍、内存带宽为 5 倍、配备 500GB/s 的以太网/Ultra Ethernet/InfiniBand，在现行限制下即可进口。晶圆级芯片/封装在现行限制下同样可以进口。

中国将获得西方公司的尖端芯片，并很快有能力训练 GPT-4 及更高级别的模型。

## **本土 AI 芯片能力**

众多已具规模的厂商与 AI 芯片初创公司很快就将交付与英伟达 A100 相当的芯片，包括华为、壁仞（Biren）、腾讯、阿里巴巴、百度、沐曦（MetaX）等。虽然今天我们不会逐一深入分析它们的能力，但它们完全能够在两年内于 SMIC 7nm 上以可观的数量交付 A100 级芯片。软件固然是挑战，但中国的软件开发者数量超过美国、加拿大与欧洲之和，这也不应是无法逾越的难关。

这些芯片大多使用 Cadence、Synopsys 与 Mentor Graphics（西门子）的美国 EDA IP 进行设计。[华为正通过巨额投资快速推进本土 EDA。](https://ieeexplore.ieee.org/xpl/conhome/10019319/proceeding)一些玩家如沐曦（MetaX）在公然抄袭英伟达，[让自家芯片兼容 CUDA](https://www.metax-tech.com/en/goods/prod.html?cid=3)。另一些如壁仞，拥有大量来自英伟达上海的设计师，[如果你眯起眼睛看，其架构与英伟达的极为相似](https://www.semianalysis.com/p/how-chinas-biren-is-attempting-to)，而且[这是一个好架构](https://www.semianalysis.com/p/how-chinas-biren-is-attempting-to)。壁仞还曾[试图规避制裁，这一点由我们独家披露。](https://www.semianalysis.com/p/how-chinas-biren-is-attempting-to)

凭借中国的本土半导体制造能力，微架构与系统设计将不断演进，比 H100 更强的芯片已清晰在望。中国还[有能力构建超大规模超级计算机并将其组网互联](https://www.tomshardware.com/news/china-builds-exascale-supercomputer-with-192-million-cores)。此外，中国拥有以中际旭创（Innolight）等公司为代表的领先光模块制造能力，先进封装也在快速发展。先进封装与光学的结合，将使中国即便被限制在 5nm 或 7nm 制程技术上，也能凭借本土生产的半导体保持竞争力。

仅明年一年，中国就会有多家公司有能力训练超过 GPT-4 的模型。这根本不成问题。而且，凭借军民融合体制，以及不存在陈旧、缓慢、极其昂贵的存量国防工业，中国或许能比西方更有效地将 LLM 武器化——正如他们在无人机领域已经做到的那样。

## **无线电与传感器**

顺带一提，在射频/传感器能力方面，除了少数无关痛痒的制裁之外几乎无所作为。至少在历史上，通信与传感器技术是战争中最重要的技术。虽然无人机的迅速普及可能正在改变这一点，但最有效的无人机所使用的硬件，实际上与手机硬件高度相似。此外，中国已经拥有能够探测 F-35 的雷达。

他们正借助各种先进化合物半导体持续改进这一能力。为其本土碳化硅与氮化镓产业进口的设备，同样被用于将在战争中派上用场的射频应用。此外，还有多家公司——如意法半导体（STMicroelectronics），其技术是 SpaceX Starlink 的核心——正积极开展合作并[进行合资/IP 转让](https://www.reuters.com/technology/stmicroelectronics-sanan-plan-silicon-carbide-venture-china-2023-06-07/)。

这类合资/IP 转让将以「该技术只能用于功率半导体应用」为幌子，大幅加速中国的能力提升——尽管通过合资获得的技术能力可以相对容易地转用于射频应用。

## **还能做什么**

美国政府显然将一个能够生产 14nm 以下芯片、以及 NAND 达 128 层以上、DRAM 半间距达 18nm 以下的存储 IC 的中国半导体产业，视为对全球安全的重大威胁（关于解放军打算如何使用 AI 芯片的开源分析，[见此处](https://cset.georgetown.edu/publication/silicon-twist/)）。而维持当前水平的出口管制，则对美国及其盟友的长期经济与国家安全构成重大威胁。

美国政府及其盟友可以让中国半导体产业就地止步。以下是一些可采取的步骤，以确保中国在未来几年无法发展出批量制造高端军事应用所需芯片的能力：

1. 限制 ArFi 浸没式光刻机。
2. 限制现有设备的维修服务。
3. 限制 ArFi 光刻胶。
4. 限制掩模版。
5. 限制掩模空白版、掩模写入器及其他相关基础设施。
6. 限制量测设备。
7. 限制 CMP 设备。
8. 限制外延设备。
9. 限制干法刻蚀设备。
10. 限制 CVD 与 ALD 设备。
11. 限制先进封装设备。
12. 限制离子注入设备。
13. 限制半导体制造设备的子系统与组件。
14. 限制刻蚀气体。
15. 限制沉积前驱体。
16. 限制 IO 超过 25.6Tbps 的芯片，即使其不含任何算力。
17. 限制性能超过 1000TOPS 的芯片。
18. 限制 [200G SerDes 的 IP 授权](https://www.reuters.com/markets/deals/republican-rubio-slams-us-approval-chip-deal-involving-firm-with-china-ties-2022-08-29/)。
19. 限制 EDA 工具。
20. 限制合资企业与对华入境投资。

半吊子的措施不会奏效，但全面出击将使中国在国内复制半导体供应链的成本高到近乎不可能。虽然我们并不专门主张其中任何一项，但有一点很清楚：如果采取果断行动，西方仍能阻止中国的崛起。

*感谢 Jordan 与 Doug 协助整理本文。请关注 [FabricatedKnoweledge](https://www.fabricatedknowledge.com/) 与 [ChinaTalk](https://www.chinatalk.media/)，它们都非常出色。也请留意本周晚些时候的 [ChinaTalk](https://www.chinatalk.media/) + Transistor Radio 节目，我们将继续围绕 SMIC 与华为展开讨论，进一步解释可用的政策工具箱，并回顾 Semicon Taiwan、中国电动车的全球影响等话题。*

[获取 8 折团购订阅](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
