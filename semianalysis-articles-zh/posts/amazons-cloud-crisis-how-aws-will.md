---
title: "亚马逊的云危机：AWS 将如何输掉计算的未来"
title_en: "Amazon’s Cloud Crisis: How AWS Will Lose The Future Of Computing"
subtitle: "Nitro、Graviton、EFA、Inferentia、Trainium、Nvidia Cloud、Microsoft Azure、Google Cloud、Oracle Cloud、基础设施竞争力评估、AI 即服务、企业自动化、Meta、Coreweave、TCO"
date: 2023-03-20
source: https://newsletter.semianalysis.com/p/amazons-cloud-crisis-how-aws-will
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 亚马逊的云危机：AWS 将如何输掉计算的未来

> 原文：[Amazon’s Cloud Crisis: How AWS Will Lose The Future Of Computing](https://newsletter.semianalysis.com/p/amazons-cloud-crisis-how-aws-will) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Nitro、Graviton、EFA、Inferentia、Trainium、Nvidia Cloud、Microsoft Azure、Google Cloud、Oracle Cloud、基础设施竞争力评估、AI 即服务、企业自动化、Meta、Coreweave、TCO**

尽管内部需求远小于 Google、Microsoft、Meta 和腾讯，亚马逊拥有的服务器数量仍超过世界上任何一家公司。Amazon Web Services（AWS）长期以来一直是云计算的代名词。AWS 通过同时服务初创公司和企业客户、提供可扩展、可靠、低成本的算力与存储解决方案，主导了整个市场。这台引擎把亚马逊推上了全球最卓越的计算公司之位，但情况正在起变化。

亚马逊是一家了不起的技术公司，但他们在某些方面有所欠缺。技术实力、文化以及/或者商业决策，将阻碍他们像抓住前两波浪潮那样抓住下一波云计算。本报告将覆盖云计算的这三个阶段，并说明亚马逊在前两个阶段的持续主导地位，并不必然为他们在计算未来之争中赢得先机。

我们将概述亚马逊各项自研芯片设计，包括 Nitro、Graviton、SSD、Inferentia 和 Trainium。这一概述将从技术与总拥有成本（TCO）两个视角审视亚马逊的自研芯片野心。我们还将讨论亚马逊正在做出哪些有意为之、却损害其 AI 与企业自动化地位并最终导致其计算市场份额流失的事情。我们还会解释 Microsoft Azure、Google Cloud、Nvidia Cloud、Oracle Cloud、IBM Cloud、Equinix Fabric、Coreweave、Cloudflare 和 Lambda 如何在多条战线上、以不同程度对抗亚马逊的统治地位。

在深入我们的论点之前，先需要补一点历史课。

## **AWS 的崛起**

随着零售业务规模急剧膨胀，亚马逊开始撞上其 90 年代单体式软件实践的极限。梅特卡夫定律（Metcalfe's law）多少适用于这里：每新增一项服务或一名开发者，复杂度都以 n^2 的速度增长。哪怕是最简单的改动或增强，也会波及大量下游应用和使用场景，需要海量的沟通协调。因此，亚马逊每年到了某个时点就不得不冻结绝大部分代码变更，以便假日销售季能够专注于修 bug 和保证稳定性。

亚马逊在重复劳动和资源浪费上也有严重问题——仅仅是为了搭一个简单的关系型数据库或计算服务就要大费周章。雪上加霜的是，最聪明的工程师往往不是最好的沟通者，当不同团队之间没有共同目标时这一点尤为明显。大型软件项目往往会达到一个临界点：组织规模和应用体量导致生产力和新功能的交付变得异常缓慢。

Microsoft 是最早遇到这个问题的公司之一，他们最初的解决方案是引入「程序经理」（program manager）这一角色。安排一名专职人员对接一个开发者团队，负责组织、沟通和规格文档等工作，这在当时闻所未闻，但确实是一件有效的工具。但仅靠这一点并不能解决所有问题。

亚马逊在多年之后也遇到了同样的问题，但他们采取的应对方式截然不同。亚马逊没有去促进团队之间的沟通，而是试图借助「固化接口」（hardened interfaces）来减少沟通。他们从单体式软件开发范式转向了面向服务的架构。需要说明的是，其他公司和学术界当时也在实践这一理念，但没有一家像亚马逊那样如此坚决地投入这项技术。

亚马逊早期员工 Steve Yegge 回忆了亚马逊的这一关键时刻。下面是他跳槽到 Google 之后吐槽亚马逊的一份备忘录的节选，后来被意外传到了网上。

> 于是在某一天，Jeff Bezos 下达了一道圣旨。这种事他当然一直在干，每次一发生，人们就像被橡皮锤猛砸的蚂蚁一样乱作一团。但有一次——大概是在 2002 年前后，误差不超过一年——他下达的命令是如此离谱、如此庞大、如此让人瞠目结舌，以至于他其他所有命令跟它一比都像是主动奉上的同侪奖金。
>
> 他的「大圣旨」大致内容如下：
>
> 1. 从今以后，所有团队都必须通过服务接口对外暴露其数据和功能。
> 2. 团队之间必须通过这些接口进行通信。
> 3. 不允许任何其他形式的进程间通信：不许直接链接、不许直接读取其他团队的数据存储、不许共享内存模型、不许留任何后门。唯一允许的通信方式就是通过网络的服务接口调用。
> 4. 用什么技术不重要。HTTP、Corba、Pubsub、自定义协议——都无所谓。Bezos 不在乎。
> 5. 所有服务接口，无一例外，都必须从头开始按照可对外开放（externalizable）来设计。也就是说，团队必须规划和设计到能够把这个接口暴露给外部世界的开发者。没有例外。
> 6. 任何不这么做的人都会被解雇。
> 7. 谢谢；祝你今天愉快！
>
> 哈哈！在座的 150 来号亚马逊前员工当然会立刻意识到，第 7 条是我加的小玩笑，因为 Bezos 压根儿不在乎你今天过得愉不愉快。
>
> *[吐槽全文](https://gist.github.com/chitchcock/1281611)*

这段吐槽里影响最深远的是第 5 条：这些固化接口必须能够对外开放。这正是打造 AWS 的起点……在 **2002 年**。

从那以后便一发不可收拾！顺理成章的下一步，是以类似的方式把计算和存储硬件也抽象掉。当众多团队时刻都在构建服务，又被警告「跟别的团队说话就会被开除」时，IT 部门根本不可能集中规划服务器需求和计算、存储需求的增长。随着各团队的服务在内部人气高涨，他们必须能够为手头的任务自行配置硬件。

把这些想法变成最终成为 AWS 的公有服务，又花了大约 4 年时间。[想了解更多历史，推荐这个精彩的播客。](https://www.youtube.com/watch?v=APvj15_YCqk)

我们将快进过这段起步期，重点谈谈这个时代延续至今的意义。早期，亚马逊收拢了几乎所有初创公司，让它们得以真正建立自己的业务。虽然大多数早期采用者是 Netflix、Twitch 这类软件领域非传统的新创公司，但富有创新精神的硬件公司也全都跳上了云计算这列势不可挡的货运列车。

> 这实在太方便了。对于像我们这样的新公司，你再也不会想去自建一个传统数据中心了。
>
> [Andy Bechtolsheim，2010 年](https://www.nytimes.com/2010/04/19/technology/19cloud.html)——Arista 和 Sun Microsystems 的创始人，也是 Google 和 VMware 最早的投资者之一。

亚马逊于 2006 年推出了存储服务 S3，紧接着推出了计算服务 EC2。2009 年推出了关系型数据库服务，随后又有 Redshift 和 Dynamo DB。在任何一个竞争对手哪怕接近之前，亚马逊**与客户一起**发布的重量级产品足足有数百项。重点是，这个时代的特征就是 AWS 的产品/应用/服务比任何对手都更好、更多，文档也更完善。每当 Google Cloud 或 Microsoft Azure 做出点什么，亚马逊都已领先好几步，和/或更易用。

这一点在过去、尤其是云计算初期确实成立，在某些品类中至今依然如此。AWS 崛起的故事和生命周期仍在延续，尽管差距已大幅缩小。亚马逊「让人们刷信用卡付款」的模式，颠覆了以六位数、七位数服务合同为主的传统生意，并且仍在继续颠覆。云计算第一波浪潮的长尾仍在展开。

## **AWS 的统治级规模**

随着上一个十年中期推移，绝大多数财富 500 强公司也开始向云端迁移。随着云计算市场走向成熟，其他公司意识到这一机遇，开始在自己的云业务上重金投入。特别是 Microsoft Azure，凭借其对企业友好的策略脱颖而出，成为强有力的竞争者。Google Cloud Platform 起初因缺乏商业化聚焦而难以获取市场份额，但此后已改进其产品，很快将实现盈利。

竞争只会愈发激烈、愈发认真，但亚马逊手里还握有一张王牌。

#### **规模。**

可以从两个角度来看这种规模优势。第一，从字面意义上讲，亚马逊就是比其他任何公司都更大，在云领域的布局也更多。云服务商需要一定的规模，才能把体量转化为更低的硬件采购价格，并摊薄其软硬件设计成本。

云服务商还需要保有随时可供客户使用的富余容量。这一点尤其重要，因为云服务商无法对服务器的使用率搞集中计划。即便是长期合同，额度何时消耗完毕也往往存在高度不确定性。与此同时，云厂商必须维持高稼动率才能获得足够的已投入资本回报率（RoIC）。体量越大，就越容易在保持足够富余容量供客户弹性扩缩的同时，实现那些高稼动率。

随着云市场规模扩大，多家公司都能达到最低可行临界规模，这一视角的优势在时间上是有限的。亚马逊大约在 2010 年代早中期迎来了那个冰球杆时刻。2012 年，亚马逊自成立以来累计对 AWS 降价 23 次，到 2015 年累计已达 51 次。尽管 2017 年之后竞争开始升温，公开降价却明显放缓，不过私下给予两位数百分比的折扣非常普遍。至少，Microsoft 和 Google 早已达到同等规模。在专门应用领域，其他云也形成了可观的规模，例如 CDN 领域的 Cloudflare、AI 服务器领域的 Oracle。

规模更重要得多的一个角度，是自研（in-house）专用芯片，无论是自研还是与生态伙伴合作。亚马逊和 Google 是这一转变最领先的实践者，但每一家超大规模云厂商都已开始部署至少一部分自研芯片。范围涵盖[网络](https://www.semianalysis.com/p/google-apollo-the-3-billion-game)、[通用计算](https://www.semianalysis.com/p/amazon-graviton-3-uses-chiplets-and)到 [ASIC](https://www.semianalysis.com/p/google-new-custom-silicon-replaces)。

亚马逊从定制芯片中获得巨大的成本节约，竞争对手难以复制，尤其是在标准 CPU 计算和存储应用上。定制芯片为云厂商带来三大核心收益：

1. 针对自身独特工作负载进行芯片工程优化，通过架构创新获得更高性能。
2. 对特定工作负载的战略性控制与锁定。
3. 剔除无厂设计公司的层层利润加成（margin stacking），实现成本节约。

在涉足新业务单元、新业务板块或基础设施变革时，亚马逊过去乃至现在都以一种非常创业式的方式运营。他们的团队在很多方面保持敏捷、精干，但背后仍有这个庞然大物般的组织的全力支持。与此相关，我们最喜欢的故事是他们在定制芯片领域的发端。

[Share](https://newsletter.semianalysis.com/p/amazons-cloud-crisis-how-aws-will?utm_source=substack&utm_medium=email&utm_content=share&action=share)

## **Amazon Nitro**

早在 2012 年前后，AWS 的一位工程师有了一个想法：为什么不在每个 EC2 实例与外部世界之间放置一个「加密狗」（dongle）——一块专用硬件——让所有数据都流经它？这个加密狗将承担安全、网络以及虚拟机管理程序（hypervisor）等虚拟化任务。它的直接好处是提升 EC2 实例的性能、降低成本并增强安全性，同时还能支持裸金属实例。这个小小的点子最终演变成亚马逊整个定制芯片事业——如今设计着多种不同的芯片，每年为亚马逊节省数百亿美元。

AWS 为支持这一加密狗设想定制芯片制定了规格。需求很简单：一款双核 Arm 架构的系统级芯片（SoC），可以通过 PCIe 接入。在接洽了几家公司后，AWS 与 [Cavium](https://www.semianalysis.com/p/marvelldeepdive2022) 合作，挑战以不至于显著推高每台 EC2 服务器成本的价格打造一颗定制 SoC。Cavium 的芯片随后很快交付。整套系统——位于独立 PCIe 卡上的定制 SoC 加上配套软件——被命名为「Nitro 系统」。它最早出现在（尽管当时并未公开谈论）C3、R2 和 I2 这几代 EC2 实例中。

到 2022 年 8 月，AWS 已在四代产品中部署了超过 2,000 万颗 Nitro 芯片，每一台新的 EC2 服务器都会安装至少一颗 Nitro。

这个「加密狗」最主要的成本收益，是把亚马逊的管理软件即 hypervisor 从原本要占用的 CPU 上卸载下来。亚马逊基础设施中部署最广的 CPU 过去是、现在仍然是 Intel 的 14nm 24 核 CPU。时至今日，Microsoft Azure 等其他云在工作负载上仍要[吃掉多达 4 个 CPU 核心](https://learn.microsoft.com/en-us/azure/virtual-machines/hbv3-series)，而这些算力并非客户的工作负载。如果这一情况存在于亚马逊的全部基础设施，那将意味着现有服务器的虚拟机数量减少约 15%，收入也随之减少。

即便按照每颗 Nitro 节省 2 个 CPU 核心这种保守得多的估算，以[每个核心的成本按预留实例标价的 1/4 估算](https://aws.amazon.com/ec2/dedicated-hosts/pricing/)，Nitro 每年节省的成本也超过 70 亿美元。

![](https://substack-post-media.s3.amazonaws.com/public/images/015f611c-8735-4e2e-9924-346c8aa5ffb8_2436x396.png)

把这些工作负载从服务器 CPU 核心移到定制 Nitro 芯片上，不仅大幅改善成本，还[消除了与 hypervisor 相关联的「吵闹邻居」问题](https://www.semianalysis.com/p/is-ampere-computings-cloud-native)（如共享缓存、IO 带宽和功耗/散热预算的争抢），从而提升性能。

此外，通过在 hypervisor 管理层与服务器之间加入[物理隔离区（air gap）](https://en.wikipedia.org/wiki/Air_gap_(networking))，客户也获得了更高的安全性。这种物理隔离[消除了恶意租户发起侧信道提权攻击的可能途径](https://www.semianalysis.com/i/57527407/cloud-native-is-it-marketing-fluff)。

除了 hypervisor 卸载带来的节约，随着 Nitro 的演进，它还在许多网络工作负载中扮演核心角色。例如 IPsec 可以被卸载到 Nitro 上，仅此一项就可能为亚马逊的每个大客户节省数百万美元。

![](https://substack-post-media.s3.amazonaws.com/public/images/24ad1614-08e2-40d2-a406-1a1c94059def_1248x769.png)

亚马逊定制芯片事业的核心直接源于他们与 Annapurna Labs 的合作，以及 2015 年对后者的收购。Annapurna 专注于面向网络和存储的服务器 SoC。需要指出，Nitro 并不只是一颗芯片，尽管我们在这里如此统称。它有多个世代、多个面向不同使用场景的变种。

在 EC2 之外，亚马逊最大的几项服务大多与存储和数据库相关。Nitro 是亚马逊在这些工作负载中建立持久竞争优势的主要支撑。经典服务器架构会在每一台服务器里放置至少一部分存储，这会导致[大量闲置资源的搁浅浪费](https://www.semianalysis.com/p/cxl-enables-microsoft-azure-to-cut)。

![](https://substack-post-media.s3.amazonaws.com/public/images/6bb942cd-5803-45a4-bbc2-7baafa0abba7_2607x1352.png)

亚马逊能够把存储从每台服务器中抽走，集中到专用服务器上。客户租用的服务器随后可以从网络存储启动。Nitro 使得即便对高性能 NVMe SSD 也能做到这一点。这种存储架构的转变帮助亚马逊大幅节省存储成本，因为客户不必为超出其用量的存储付费，还可以无缝地动态伸缩其高性能存储池。

若用通用硬件实现，这在计算和网络角度都极其昂贵，但 Nitro 凭借其面向自家工作负载的专用 ASIC，能以更低成本向租户的虚拟机提供虚拟磁盘等服务。

![](https://substack-post-media.s3.amazonaws.com/public/images/349ee4a4-0393-4b32-9d2e-285563124e4a_1248x645.png)

亚马逊对存储的重视还延伸到与 [Marvell](https://www.semianalysis.com/p/marvelldeepdive2022) 联合设计「AWS Nitro SSD」控制器。这些 SSD 致力于避免延迟尖峰和延迟抖动，并通过由 Amazon 管理的先进磨损均衡算法最大限度延长 SSD 寿命。[未来的版本还将加入一些计算卸载](https://www.semianalysis.com/p/marvelldeepdive2022)，以提升查询性能。

另外两大云厂商也想走同样的路，但他们落后数年，而且需要一个赚取利润的合作伙伴。Google 选择了与 Intel 联合设计的定制芯片 Intel Mount Evans IPU；Microsoft 则采用 AMD Pensando DPU，并[最终将部署基于内部研发的 Fungible DPU 用于存储场景](https://www.semianalysis.com/p/fungible-dpus-are-dead-carcass-acquired)。这两家竞争对手在未来几年内都只能用第一代或第二代的商用（merchant）芯片。

亚马逊正在部署其第五代、完全由内部设计的 Nitro。Nitro 在基础设施成本层面带来的优势怎么强调都不为过。它让亚马逊的成本大幅降低，进而让利于客户或转化为更高的利润率。话虽如此，亚马逊的 Nitro 也有一些重大短板，后文详述。

[Share](https://newsletter.semianalysis.com/p/amazons-cloud-crisis-how-aws-will?utm_source=substack&utm_medium=email&utm_content=share&action=share)

## **Arm 在 AWS**

虽然 Nitro 确实使用了 Arm 架构的 CPU 核心，但关键在于其种类繁多的固定功能专用加速。AWS 对 Arm 定制芯片的兴趣并不止于把自己的工作负载卸载到专用硬件上。2013 年，AWS 对使用自研芯片的思考更进一步。工程师 James Hamilton 在一份题为《AWS Custom Hardware》的文件中提出了两个关键论点：

1. 移动和 IoT 平台上 Arm CPU 的巨大出货量，足以支撑打造优秀 Arm 服务器 CPU 的投资——正如 Intel 当年借助 x86 在客户端业务上的规模，在 90 年代和 2000 年代夺下服务器 CPU 业务那样。
2. 服务器功能最终会收敛到单一 SoC 之中。因此，要在云上创新，AWS 就必须在芯片上创新。

最终的结论是：AWS 必须做一颗定制 Arm 服务器处理器。顺带一说，如果这份文件能在十周年之际公开，让大家看看它多么有远见，那将妙不可言。

让我们展开 James Hamilton 的论点，看看 AWS 自主设计的 Arm CPU 相对外购 CPU 有哪两个关键优势。

首先，它们让 AWS 得以降低成本，并向客户提供更高性价比。如何做到？顺着 James Hamilton 的思路展开：AWS 可以借助 Arm 在移动端的规模，采用 Arm 设计的 Neoverse 核心；还可以利用 TSMC（台积电）的制造规模——主要得益于智能手机市场，其规模远超 Intel。选择 TSMC 当然还意味着用上先进制程节点，领先于 Intel 的制造能力。

我们估算，亚马逊自研的 Graviton 2 和 Graviton 3 CPU 在 2022 年的出货量接近 100 万颗。仅这一出货量就足以支撑一个核心设计外包给 Arm 的自研 CPU 项目，尤其是亚马逊还在持续用自研 CPU 替代采购 AMD 和 Intel 的产品。亚马逊的垂直整合是一步显而易见的棋，哪怕唯一的收益只是更便宜的 CPU。

![](https://substack-post-media.s3.amazonaws.com/public/images/f8d535ce-7d99-458f-95de-6572c7eda961_1822x656.png)

把亚马逊 Graviton 的出货量与整个市场对比，其体量与 Intel 和 AMD 相比仍相形见绌。尽管我们认为亚马逊凭借内部部署，在 Arm 服务器领域的出货量已超过 [Ampere Computing](https://www.semianalysis.com/p/is-ampere-computings-cloud-native)，但与 x86 厂商相比仍有很大差距。

![](https://substack-post-media.s3.amazonaws.com/public/images/fe74bb9c-c353-43ea-ba91-2b1ef8ea866c_2262x658.png)

再看平均售价（ASP）：凭借其高比例的 48 核与 64 核服务器 CPU 和无与伦比的 IO 能力，AMD 拿到了全行业最高的售价。Intel 与 [Ampere Computing 的 ASP 相近](https://www.semianalysis.com/p/is-ampere-computings-cloud-native)，大致在 600 美元上下。我们对 Graviton 2 和 Graviton 3 采用了自行的制造、封装和测试成本估算。注意，这里没有计入 IP 授权费用，不过[鉴于 Amazon 与 Arm 有一份优厚的协议](https://www.semianalysis.com/p/arms-nuclear-option-qualcomm-must)，这部分费用大概不会太高。

![](https://substack-post-media.s3.amazonaws.com/public/images/b93d4df5-544b-417c-923f-6abf00294920_1801x655.png)

如果假设 CPU 可以一比一替换，那么亚马逊转向自研芯片每年为其节省数亿美元。当然，并非所有 CPU 都生而平等。即便是 AMD 的上一代 Milan，在许多方面仍然比 Intel、Amazon 或 [Ampere](https://www.semianalysis.com/p/is-ampere-computings-cloud-native) 的当代产品更快。即使忽略 AMD 这个离群值，Graviton 在 2022 年的潜在节约也超过 3 亿美元。再叠加一个事实：亚马逊的 CPU [性能高于 Intel](https://www.phoronix.com/review/graviton3-amd-intel/9)，同时[功耗更低](https://www.semianalysis.com/p/amazon-graviton-3-uses-chiplets-and)，节约便开始迅速放大。我们认为 Graviton 的总研发成本大约在每年 1 亿美元的量级，这意味着净节约超过 2 亿美元。

商用芯片供应商正在不可逆地失去数亿美元、并很快将是数十亿美元规模的 TAM。Intel 是这里最大的输家：从一家向云端出售数百万颗 CPU 的芯片公司，沦为一家为这些 Graviton3 CPU 做[利润率低得多的封装业务](https://www.semianalysis.com/p/amazon-graviton-3-uses-chiplets-and)的制造公司。

同样重要的是，自研 CPU 让亚马逊能够以最大化密度、最小化服务器与系统能耗为目标来设计 CPU，这在总拥有成本（TCO）层面帮助巨大。一个容易理解的工程决策是：尽管芯片面积和功耗还有充足的扩展空间，亚马逊仍刻意把 Graviton 3 架构限制在 64 核。

对比 [AMD 的 96 核 Epyc——它快得多](https://www.semianalysis.com/p/amd-genoa-detailed-architecture-makes)，但功耗也更高。亚马逊刻意的工程决策使其能够[在 1U 服务器中放下 3 颗 CPU](https://www.semianalysis.com/p/amazon-graviton-3-uses-chiplets-and)；而 [AMD Genoa](https://www.semianalysis.com/p/amd-genoa-detailed-architecture-makes) 服务器在 1U 内最多 2 颗 CPU，而且受功耗限制，最终往往得做成 2U 尺寸的服务器。Graviton 与 AMD、Intel 不同的另一些更微妙的工程选择，围绕其[云原生（cloud-native）特性展开，我们在此有更详细的探讨。](https://www.semianalysis.com/p/is-ampere-computings-cloud-native)

当然，我们不应忘记，竞争本身也加大了 Intel 和 AMD 的 CPU 降价压力，AWS 在 x86 CPU 上的采购支出同样在省！AMD 和 Intel 必须在工程上大幅领先亚马逊，才能证明其商用芯片上丰厚利润率的合理性。我们毫不怀疑 AMD 在 CPU 核心和 SoC 工程上更强，Intel 也可能赶上，但他们能做到 2 倍以上的领先、以支撑其约 60% 的数据中心业务利润率吗？这可不好办。

Microsoft 和 Google 都有进行中的内部服务器 CPU 项目，但尚未批量部署。即便将来部署，也很难想象他们能一举追上亚马逊已经迭代到第 3、第 4 代的水平。

亚马逊的巨大规模，尤其是在通用计算和存储相关垂直领域，怎么强调都不为过。这将在未来许多年里持续为它在云端带来持久的优势。

*推荐阅读 [The Chip Letter](https://thechipletter.substack.com/)，那里有大量精彩的半导体历史课。Babbage 协助我们撰写了本文的部分历史内容，他很快也将发布自己的文章，更全面地回顾亚马逊自研半导体的历史。*

## **计算的下一个时代**

到目前为止，我们对亚马逊只有溢美之词，但在能开始谈论云服务商的未来之前，必须先交代清楚亚马逊优势的来龙去脉与现实。

亚马逊、半导体以及整个科技行业，本质上都是一条条 S 曲线叠加的故事。亚马逊作为一家公司，天生为持续增长而生，他们从未真正退出过投资周期。在许多方面，他们的文化天生擅长找到下一个大热点，而不一定擅长在咬住猎物之后榨取最大价值。

亚马逊的文化、围绕其云服务商模式做出的种种自觉商业决策，以及在定制计算与网络芯片上的技术选择，可能让他们在计算的下一个时代陷入干涸。前两个云时代仍将继续演绎，亚马逊也将继续从这家寡头格局市场中不受监管的头号公用事业公司身上攫取巨大价值，但下一个时代未必唾手可得。来自现有竞争者和一路狂奔的新进入者的竞争压力不容小觑。

[Share](https://newsletter.semianalysis.com/p/amazons-cloud-crisis-how-aws-will?utm_source=substack&utm_medium=email&utm_content=share&action=share)

本报告的后半部分为订阅者专享，将深入剖析亚马逊芯片战略的重大技术缺陷，以及他们如何正在错过 AI 与服务领域下一轮爆发式增长。我们将对比多家竞争对手的芯片、服务器和云战略，包括 Microsoft Azure、Nvidia Cloud、Google Cloud、Oracle Cloud、IBM Cloud、Equinix Fabric、Coreweave 和 Lambda。此外，我们还将讨论服务业务，以及为什么竞争对手在那里更有资格领跑。我们将分享多种视角的观点，以及最终我们预计市场格局将如何洗牌。同时，我们也会就云、AI 和服务给出一些短期点评。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
