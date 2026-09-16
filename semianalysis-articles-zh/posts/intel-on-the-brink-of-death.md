---
title: "英特尔濒临死亡 | 文化腐朽、聚焦产品的战略有缺陷、代工业务必须活下去"
title_en: "Intel on the Brink of Death | Culture Rot, Product Focus Flawed, Foundry Must Survive"
subtitle: "董事会短路、文化腐朽、x86 无护城河、卖掉 PC 业务、NVIDIA 进军 PC CPU、路线图评估"
date: 2024-12-09
source: https://newsletter.semianalysis.com/p/intel-on-the-brink-of-death
crawled: 2026-09-15
authors: ["Dylan Patel", "Doug", "Myron Xie", "Jeremie Eliahou Ontiveros", "Sravan Kundojjala"]
tags: ["Chip Design", "Semiconductors", "Foundries"]
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 英特尔濒临死亡 | 文化腐朽、聚焦产品的战略有缺陷、代工业务必须活下去

> 原文：[Intel on the Brink of Death | Culture Rot, Product Focus Flawed, Foundry Must Survive](https://newsletter.semianalysis.com/p/intel-on-the-brink-of-death) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**董事会短路、文化腐朽、x86 无护城河、卖掉 PC 业务、NVIDIA 进军 PC CPU、路线图评估**

英特尔（Intel）的董事会不称职，其数十年来的糟糕决策正把它推向死亡。解雇 Pat Gelsinger、让一位 [CFO](https://www.linkedin.com/in/dzinsner/) 加一位[职业销售与营销高管](https://www.linkedin.com/in/michellejohnstonholthaus/)掌舵，并削减晶圆厂开支、转而重新聚焦 x86——这一连串决定正是不称职的样本，并将终结英特尔。*Fabricated Knowledge* 最近撰文[《英特尔之死：当董事会失灵》（The Death of Intel: When Boards Fail）](https://www.fabricatedknowledge.com/p/the-death-of-intel-when-boards-fail)，解释了董事会在领导力与规划上的问题如何葬送了这家公司。简单说，英特尔董事会已经逃避了十多年失败的责任。这十年的失败以一个终极错误收场：解雇 CEO Pat Gelsinger。

细看之下，这些失败毫不意外。11 名成员中有 7 人*毫无相关半导体经验*。另有两人虽在领域内颇有建树，但身份是学者而非产业操盘者。他们没有做出艰难决策的经验，不理解关键的商业拐点，其资历不足以应对当下的赌注。唯一履历强劲且对口的成员 Stacy J. Smith，今年才刚刚加入，接替 Lip-Bu Tan。

过去十年是英特尔历史上最糟糕的十年，其中大部分伤害是在 2010 年代造成的。Pat Gelsinger 过去几年一直在纠偏，但让泰坦尼克号调头不是一蹴而就的事。英特尔的衰落中有一个不变量：**七名董事会成员**。他们今天仍稳坐董事会。

让我们把解雇 Gelsinger 的董事会成员们的履历合起来，与他的履历对比：你会选谁来拯救英特尔？我们认为从当下出发仍有路可走，但绝不在现任董事会手里。

![](https://substack-post-media.s3.amazonaws.com/public/images/7918e786-9ceb-43d9-a892-8f8490456db1_982x1024.png)

除非把名字改成 Grove、Noyce 或 Moore，否则很难想象还有谁比 Gelsinger 更适合这份工作。遗憾的是，董事会在 Gelsinger 的反转大业迎来黎明之前就丧失了勇气。半导体是最复杂的行业之一，纠偏需要许多年。在最后一次董事会上，Gelsinger 提交了更新后的资本开支计划：维持对 Intel Foundry Services 的大额投入。但董事会对该计划极为不满，以至于把他逼走了。

无疑，Gelsinger 作为 CEO 本可以做得更好。他有些非理性乐观，但这正是英特尔所需要的。他也有过失误，例如英特尔当前的 AI 战略依然是残缺的——有 Gaudi 3 和 Falcon Shores 在，英特尔永远拿不到多少 GenAI 推理或训练市场份额。主要酿成 10nm 问题的文化腐朽，从技术角度看已大体修复，但对外部客户的服务依然不到位。Tower Semiconductor（高塔半导体）收购本可带来急需的面向客户的专业能力，但在监管导致交易告吹之后，没有 B 计划。英特尔背负着“难于合作”的名声，缺乏以客户为中心的视角；与此同时，台积电（TSMC）连给客户涨价都要犹豫再三——谁赢谁输毫无悬念。Gelsinger 著名的主题演讲前俯卧撑，可丝毫没能练出以客户为中心的肌肉。

尽管如此，Gelsinger 是一位真正想要这份工作、且够格的候选人。在这一点上，他大概是独一无二的那一个。而今天，董事会手里的选项大都不如他。

## 英特尔的失败

英特尔的问题始于 10nm 制程节点（也可以说是 14nm）。2016 年，台积电与英特尔都计划将各自的 10nm 制程导入量产。台积电按期执行（尽管节点性能略逊），而英特尔强推激进微缩，需要四重图形化（quadruple patterning）、新型钴互连（Cobalt interconnect），以及有源栅上的接触孔（contact over active gate）。良率糟糕，这个节点花了三年才修复。等到英特尔批量出货 10nm 产品时，台积电已售出超过 50 万片 N7 晶圆，并开始送样 N5。

随后，英特尔的产品因制程技术停滞而受损。AMD 等竞争对手坐拥台积电制造的优势，许多情况下芯片设计/架构也更优。数据中心市场份额开始流失，英特尔的经营问题雪球越滚越大。

![](https://substack-post-media.s3.amazonaws.com/public/images/67cbee1c-166a-46b4-9d7f-8c21bec3d916_1024x595.png)

这是英特尔历史上广为人知的一段。然而不知为何，董事会的不称职与领导层的决策通常不在叙事之中。这家史上最伟大公司之一的真正坠落，早在此前十多年就已开始——它始于英特尔在文化上不再是英特尔。

## 文化腐朽——烂到核心

英特尔文化腐朽的故事要追溯到 Paul Otellini。Paul 与 Pat Gelsinger 是 CEO 职位的领跑者。这是“生意人 vs 技术人”的经典领导力抉择。结果是，英特尔选出了首位非工程师 CEO。

Paul 最终胜出，靠的是他狠辣的反竞争商业决策——这些决策把 AMD 锁在 CPU 市场之外，并让英特尔的垄断地位稳固了十多年。Paul 推行了一项政策：向各家 OEM 与系统集成商付钱，让它们不用 AMD，这掐断了 AMD 的营收、研发与晶圆厂投入。[仅 Dell 一家就收了约 $4.3 billion](https://money.cnn.com/2010/07/23/technology/dell_intel/index.htm)，这也是 Dell 在此期间能盈利的唯一原因。英特尔与欧盟至今仍在法庭上就这些反竞争行为缠斗。

从那时起，商业决策凌驾于技术之上。英特尔老员工认为，正是 Paul 让这家组织变成了政治炼狱。在 Paul 之前，英特尔拥有 Andy Grove 式的文化：“建设性对峙”、数据驱动的决策制定、对执行的极致专注、极端的责任制。[关于这段历史有许多好书](https://a.co/d/3PKtQqu)；只要让一位英特尔老将打开话匣子，他们会告诉你：那时人们总能拿数字支撑自己的观点，决策过程中经常互相吼，但路线一经选定，全公司就拧成一股绳向前推进。那时的英特尔，是一列势不可挡的货运列车。

英特尔做事方式严苛，但那是一种高产出的文化。Paul Otellini 改变了这一切。技术决策为政治权力让路，全公司上下的发展之路变成了各封建领地之间的权力斗争。这种文化腐朽始于 Paul Otellini，并持续恶化，直到 Pat Gelsinger 到来。

除了改变文化之外，董事会还放行了无数糟糕决策，比如一场愚蠢的收购狂欢——买下 McAfee 等完全不相干的公司；再如[iPhone 的生意送上门来都不去争取。错失移动市场与 Arm 的崛起——我们在此有详述](https://x.com/SemiAnalysis_/status/1857472836618825844)——这是一个将永远纠缠英特尔的决策。Paul 的继任者只会更糟。

**Brian Krzanich** 是一场 CEO 灾难。10nm 惨败就发生在他任内。对晶圆厂的这种管理不善，是公司所面临的最大单一问题，因为晶圆厂就是英特尔的核心。尽管如此，Krzanic 最终被解雇，还是因为一段违规的职场恋情曝光。提名他的董事会里包括 John Donahoe——那位让 Nike 不再酷的 CEO——以及后来的董事长 Frank Yeary。关于 Brian 作为领导者的失败、糟糕的收购、AI 上的失误与技术领导力的腐化，大可以写上几本书，但现实是：他本身就是这种毒性文化的产物，又极大地加速了它。他大概会被记为英特尔史上最差 CEO。

## 财务工程铺就通往地狱之路

不甘示弱的 2018 届董事会，用英特尔历史上第一位真正意义上的非技术型 CEO 替换了 Krzanich：**Bob Swan**。严格说，Paul Otellini 才是第一位领导英特尔的非工程师，但他在公司效力 30 余年，包括担任传奇人物 Andy Grove 的技术顾问，以及执掌微处理器部门。

Swan 是职业 CFO——英特尔是他的*第 10 个* CFO 岗位——于是工艺工程让位于财务工程。Swan 任内，英特尔在股票回购上的花费与晶圆厂资本开支相当：回购投入超过 $36 billion，而 Capex 为 $38 billion。在一家资本密集型公司市场份额不断流失、制程落后主要对手两个节点以上时，这是失职。

Brian Krzanich、Bob Swan 和英特尔董事会不仅砍 Capex，还成批裁减技术人才。2013 到 2020 年间，7 年中有 4 年员工人数萎缩，而此时公司正丢失技术领导地位，利润率却漂亮得很。他们外行又怠惰的目光催生了技术上的无能，也让 Navin Shenoy、Murthy Renduchintala、Aicha Evans、Remi El-Ouazzane 等政客式人物在全组织内驱动糟糕决策。这还只是一份简短名单。Pat Gelsinger 就是解药，他清除了这些经理人的诸多封建领地与无能。我们对文化层面的唯一批评是：他太心慈手软，总给人机会，动作也不够快。

那些纵容此类行为的董事们呢？董事会十名成员中的五位刚刚解雇了 Pat Gelsinger。解雇之后，董事长 Frank Yeary 在新闻稿中表示：“**作为董事会，我们首先深知，必须把我们的产品集团置于我们所做一切工作的中心。**”

这是一条倒退的战略，救不了英特尔。董事会又在犯它似乎最擅长的那种短视错误。董事会是瞎的，但新的联席 CEO——CFO David Zinsner 与 Michelle Johnston Holthaus——同样如此。Michelle 是前销售、营销与传播负责人及首席营收官，Zinsner 则于 2022 年加入。英特尔在这个关键时刻需要的是领导力，而这二位联席 CEO 并非合适人选。下面读一读 Michelle 的一些言论——与现实、业务和营销战略脱节：

## x86 与产品集团没有护城河

英特尔的黄金年代，是先进制程技术与 x86 护城河相结合的年代。x86 的护城河也是双重的：英特尔在 x86 上有护城河，而 x86 在计算领域有护城河。今天，这两道护城河都已失守。

智能手机时代之前，x86 是通用 CPU 中占主导地位的指令集。几乎每台 PC 和服务器都必然搭载基于 x86 的 CPU，因为软件都是为兼容 x86 指令集而编写的。这由“Wintel”（Windows + Intel）联盟推动——Windows 是仅在 x86 上运行的主导操作系统。软件开发者自然会理性地把精力集中在为最大用户群开发软件上：Windows，而这就意味着为 x86 做软件。这是一个经典生态：用户因为更丰富的软件阵容而想要 Windows PC，而用 Windows 就意味着买 x86 CPU。

这些 x86 CPU 大多是英特尔 CPU。虽然 AMD 也拥有设计 x86 CPU 的 IP 权利，但 AMD 很长一段时间被自己的晶圆厂（现已分拆为 GlobalFoundries）绑住，制程技术逊于英特尔，缺乏竞争力。讽刺的是，这正是英特尔今天的处境。英特尔晶圆厂的失败与台积电的无情进军，让 AMD 得以凭借[更优的架构](https://semianalysis.com/2021/12/15/advanced-packaging-part-1-pad-limited/)与制程技术终于发起反击。

在缺乏 OS 与软件支持、又没有平台切换的情况下，基于其他架构的 CPU 几乎没有胜算。而智能手机时代带来的恰恰就是这场平台切换。智能手机范式催生了 iOS 与 Android 两个新软件生态和全新的应用集合，这意味着 x86 在个人计算中的历史护城河没能延续到智能手机上。

[英特尔确实尝试过智能手机 AP，但为时已晚、三心二意，还带着 PC 思维的错误战略](https://x.com/SemiAnalysis_/status/1857472836618825844)。他们不懂如何在天鹅金蛋之外创新。关键在于，受电池约束，能效对智能手机远比对 PC 关键（对 PC 而言这几乎不是问题），而英特尔正是在这里输给了基于 ARM 的智能手机 SoC 对手。

可以说这并不算灾难，因为英特尔只是错失了一个新市场机会，并没有失去 PC 大本营。但智能手机的崛起加速了客户端 CPU 市场的成熟。智能手机的便利、无处不在与功能性，让消费者把更多时间花在手机上，而手机已达到或超越 PC 的许多能力。这自然侵蚀了客户端 PC 市场——许多消费者的个人计算主力是智能手机，而非专用 PC。

## 就连 x86 客户端 CPU 也将迎来竞争

这开启了 Windows 与英特尔相关性的衰落，取而代之的是 Apple 与 Arm 的时代。这一组合已经侵蚀到英特尔产品集团的核心：Apple 把设计 iPhone A 系列 SoC 所积累的知识与经验，成功转化为 2020 年面向自家客户端笔记本与台式机、大获成功的基于 Arm 的 M 系列 SoC。在向 x86（对 IBM PowerPC 的统治）屈服十五年之后，Apple 终结了与英特尔的合作。

这一转型之所以可能，靠的是将 x86 软件移植到 Arm 的巨大工程。关键的拼图是 Rosetta 2 模拟器：它在应用安装时对其重编译以适配 Apple 芯片，实现了无缝切换。Apple M1 带来了巨大性能提升——配有英特尔未曾提供的各类加速引擎，外加续航的大幅改善。它一炮而红。对 Apple 而言，这意味着更高性能与更好利润率。虽然英特尔新的 Lunar Lake 在加速器与续航竞赛中追了上来，但为时已晚；船已经开走了。更何况，由于采用台积电的先进制程技术，英特尔的成本结构缺乏竞争力。

x86 的软件锁定正在被打破。这激励其他芯片厂商利用开放的（付费的）Arm ISA，进攻成熟但利润丰厚的客户端 CPU 市场。连前 Wintel 联盟中的 Microsoft 也推出 Windows for Arm 作为回应，补全了非 x86 生态。

Qualcomm 于 2024 年发布了面向 Windows PC 的 Snapdragon X，后续还会有更多玩家入场。NVIDIA 与 MediaTek 都在独立开发 Arm 客户端 PC 芯片，后文将给出这些芯片的更多细节。AMD 虽是 x86 生态的受益者，但也看到了墙上的字迹，正在为 Microsoft 以半定制（semi-custom）芯片的形式开发一款基于 Arm 的 CPU。

是的，Arm PC 还有许多磕绊要平，所以 Qualcomm 的 Snapdragon X 尚未抢下多少份额。重要的是堤坝已溃，洪水即将到来。Arm PC 会成真，因为生态中已形成一批关键玩家（Microsoft、Arm、Qualcomm、Nvidia、Mediatek）的法定多数——他们想要、并已下定决心让 Arm PC 成真。

总结英特尔在客户端 CPU 上护城河的流失：曾经的单人市场，如今有五位重量级竞争者（Intel、AMD、Nvidia、Qualcomm、Apple）。x86 在移动 PC 上的护城河已岌岌可危。

## 数据中心 TAM 永久性流向**超大规模云厂商、AI 与加速计算**

虽然客户端 PC 市场因智能手机而放缓，x86 CPU 在服务器 CPU 与数据中心负载中仍在增长。英特尔依赖其数据中心产品分部带来增长，尤其依赖超大规模云厂商与云服务客户。但服务器 x86 的故事与客户端 x86 如出一辙：所有锚定客户都在转向 Arm。前线早已被攻破，先锋就是 AWS 基于 Arm 的 Graviton 系列 CPU 服务器。

AWS Re:Invent 上一个惊人的数据点，概括了 Graviton 的成功：

> 过去两年，**落地我们数据中心的全部 CPU 容量中，超过 50% 是 AWS Graviton**。想想这意味着什么。Graviton 处理器的数量超过了其余所有处理器类型的总和。
>
> *Dave Brown，AWS EC2 计算与网络负责人*

其他超大规模云厂商看在眼里，正在跟进：Google 有 Axion，Microsoft 有 Cobalt，阿里巴巴有倚天（Yitian），Meta 也在开发基于 Arm 的 CPU。[Arm 正通过其 CSS 方案，让客户设计定制芯片变得极其容易](https://www.semianalysis.com/p/microsoft-infrastructure-ai-and-cpu)。

与此同时，Arm 在夺取 CPU 份额，加速计算负载也在从通用 CPU 手中夺取份额。GenAI 正在催生史上最大的计算基础设施建设，以 GPU 与其他 AI 加速器为中心。连 x86 在这轮建设中的微小参与也在萎缩。Nvidia 最抢手的下一代 Blackwell SKU——GB200——使用 NVIDIA 的 Grace CPU（基于 Arm）来为 GPU 供数，而不是这一代最常见 AI 服务器配置 Hopper HGX 所用的 x86 Xeon CPU。英特尔的 Gaudi 3、Falcon Shores 等，连 AMD 的路线图都竞争不过，更遑论 NVIDIA 的。

而且不只是 AI，其他负载也在被加速。[AWS Nitro](https://semianalysis.com/2023/03/20/amazons-cloud-crisis-how-aws-will/#amazon-nitro)、[Google Argos VPU](https://semianalysis.com/2021/06/02/google-new-custom-silicon-replaces/)、[Meta MSVP](https://www.semianalysis.com/p/meta-custom-silicon-whats-old-is) 等芯片的设计初衷，都是在通用 CPU 未优化的大规模专用负载中部署高性价比芯片。它们在削减 x86 CPU 的 TAM，正如 NVIDIA 的加速计算战略所做的那样。

与客户端 PC 一样，数据中心里的 x86 正在多线失血：Arm 与加速计算。这无法阻止，连英特尔的新产品也解决不了。后文我们会详谈：除非晶圆厂带来巨大的成本优势，否则英特尔的数据中心路线图即便到 2026 年也毫无竞争力。

不，x86 不会一夜消失。它仍是一个大市场，并可能成为一门现金牛生意。但现金牛地位只有在裁掉大批员工、长期扼杀创新的前提下才会出现。即便如此，AMD 和各路 Arm 玩家夺取份额的速度，很可能快过英特尔董事会的想象。董事会的“聚焦产品”战略听起来就是一条死路。

## 没有晶圆厂，英特尔产品无法具备竞争力

然而问题在于，失去昔日的制造实力之后，英特尔的 x86 已无法与 AMD 竞争，更别说与基于 Arm 的选项竞争。英特尔可以硬着头皮承受毛利率损失，把制造外包给台积电。这能拉平与 AMD 的起跑线，却解决不了“英特尔的设计赢不了 AMD”这个问题。

这就是为什么 Lunar Lake 这类主要外包给台积电的产品无法放量——它们的毛利率只有十几个百分点。董事会不理解这一点，因为*他们不懂半导体制造*。客户端 CPU 组织至今仍主要出货由英特尔自家晶圆厂制造的单片（monolithic）Raptor Lake 裸片，这是有原因的。若非如此，英特尔亏钱的速度会更快。

英特尔产品集团几十年来被独享的先进制程宠坏了，这掩盖了其微架构上的一切缺陷。后果是：今天英特尔的产品所用的硅面积，约为一流同行（AMD、Nvidia、Qualcomm）的 2 倍。这听起来不像一家领先的设计公司，英特尔的产品集团本就不该是重心。它不过是英特尔在逻辑制造上的技术领导地位、以及 x86 ISA 在通用 CPU 中统治地位的遗产。而这一切在今天已不再重要。

Intel Foundry 是这家公司最重要的部分，必须被拯救。

## Intel Foundry 是英特尔最重要的部分

Intel Foundry 是英特尔的未来。它对美国和西半球具有巨大的战略价值。先进制程半导体对消费、工业与军事应用至关重要，而西方世界并不具备大规模生产它们的能力。

台积电是唯一的大批量制造商，而台湾当局已明确表示，不会允许最新制程在岛外生产。亚利桑那项目在 5nm 与 3nm 上的产能，不到台湾的五分之一。而且，台积电亚利桑那很快将落后先进制程前沿两个节点。要实现任何程度的国家安全，都需要更多供给，而危机之下这毫无保障。

唯一勉强能够填补这一空缺的实体就是 Intel Foundry。英特尔曾率先将更多制造技术推向市场，例如高 K 金属栅极（high-K metal gate）、FinFET 等等。他们把 EUV 输给了台积电，但按其当前路线图，他们将在环栅晶体管（GAA）、背面供电、High NA EUV 与 DSA 上先于台积电上市。

18A 在明年（如果）爬坡进入大批量生产后，很可能是除台积电之外的最佳选择，而 14A 在 2027 年前后有实实在在的机会击败台积电最新制程。需要说明，英特尔也遭遇了一些挑战，包括 18A 的 PDK 1.0 延迟，以及被 Broadcom 泄露的 1.0 之前版本 PDK 的良率问题；但他们将在环栅晶体管与背面供电两项上都先于台积电上市。与步履蹒跚的产品集团不同，IFS 是一门具备竞争优势的生意。当然，这一切都以 Intel Foundry 能活到那个时候为前提。

Intel Foundry 将需要帮助。英特尔很可能被拆分出售；董事会已声明产品优先，而代工业务最坚定的拥护者刚被扫地出门。这门生意是个资本开支黑洞：我们估算，即便产能建设大幅缩水，Intel Foundry 未来 3 年仅晶圆厂设备（WFE）一项就需要 $36.5B。晶圆厂厂房（fab shell）及其他开支还要再加 $15-20B+。由于产品集团的失职，英特尔没有支撑这一切的现金流，即便有《芯片法案》（CHIPS Act）补贴也不够。

但失去先进芯片供应渠道的代价，还要再高一个数量级。据美国国家经济委员会主任称，2021 年的芯片短缺让当年美国 GDP 损失了 1%——约 $240B。那还只是一场持续数月、主要集中于*成熟制程芯片*的中断。从零开始恢复先进逻辑能力需要数十年。如果说 2021 年的短缺是一场 10 英尺的涌浪，先进逻辑供给归零就是一场 100 英尺的海啸。

除了成本风险，还有国家安全上的紧迫性。如果你相信国家安全顾问 Jake Sullivan 所说的——“未来几年，可能没有任何其他技术比先进 AI 系统对我们的国家安全更关键”——那么你必须相信，作为美国保障先进逻辑供应的最佳选项，Intel Foundry 同样至关重要。想象一下，失去生产下个世纪最关键技术的手段会怎样。Intel Foundry 必须被拯救。

## 如何拯救 Intel Foundry

那么，Intel Foundry 怎样才能活下来？最低限度的可生存形态，是作为台积电先进制程的第二供应商（second-source），并获得多家顶级超大规模云厂商与无厂设计公司的可观产品量。客户*想要*为自身的台积电/台湾敞口去险，正如国家安全界所做的那样。

目前，转向 Intel Foundry 做第二供应商，意味着用地缘政治风险去换性能与成本。18A 生态并不成熟——PDK 不如台积电的好、经过流片验证（silicon-proven）的 IP 库很小、EDA 支持也不强（EDA 公司把支持台积电的精力所获得的回报，目前远高于支持 Intel Foundry）。

总体而言，把一个设计移植到 Intel 18A 的成本，即使不超过、也接近于在 N2 上做一次全新设计。市场已经给出了答案：太贵、太险。否则，我们早该看到无厂公司为旗舰产品做第二供应商了。

Intel Foundry 应当死死聚焦于两点：1) 有竞争力的制程技术；2) 让设计从台积电切换过来尽可能便宜、尽可能容易。前者在轨，后者则前景不明。与英特尔母体分拆，可以减少干扰、提高专注度。基于国家安全立场的政府支持是必要的。面对中国策动的台湾政变或入侵，Intel Foundry 是美国手中唯一的最佳对冲。

但请注意：若不向 Intel Foundry 注入约 $50B 量级的可观资本，英特尔出售 Intel Foundry 的方案是行不通的。AMD 曾尝试分拆晶圆厂，结果是灾难。Mubadala（穆巴达拉）从 AMD 手中买下晶圆厂并创立了 GlobalFoundries。此后十年，GlobalFoundries 累计亏损 $22.4 billion。

这还没完：IBM 付给 GlobalFoundries $1.5 billion，换来“由 GlobalFoundries 收购 IBM 晶圆厂”这份“殊荣”。AMD 还背上了长期晶圆供应协议，导致其无法使用其他晶圆厂。即便如此，GlobalFoundries 仍不得不在 14nm 停止制程研发，转而运行授权自 Samsung 的制程 + 一个来自 IBM 的特殊用途 14nm。GlobalFoundries 跳过了 10nm，并在 7nm 处彻底退出。要重演这一幕，需要有谁愿意烧掉 $50B+，把 Intel Foundry 维持下去。

不，正确的做法是：英特尔应把客户端 x86、Mobileye、Altera 等产品集团出售给私募股权公司，以及 Broadcom 和 Qualcomm 等“秃鹫”，并捆绑长期代工协议。

虽然 Trump 政府多半对任何看起来像“企业福利”的东西过敏，但许多关键官员是国家安全鹰派，深知本土拥有先进逻辑制造能力的重要性。一家完成注资、并握有美国最大的两家半导体公司长期制造协议的独立 Intel Foundry，政府在金额上和政治上都更容易给予支持。

Intel Foundry 不会背负英特尔拖后腿的产品团队、Mobileye 或 Altera。Intel Foundry 将只有一个清晰的使命，而它对美国与西方的国家安全和未来至关重要。

谁来牵头？也许是一位肩负恢复美国逻辑制造雄风使命的“芯片沙皇”。我们正好认识一位履历漂亮、刚刚空出时间寻找新机会的人选……

下文将讨论：在 David Zinsner 与 Michelle Johnston Holthaus 领衔、现任董事会坐镇之下，英特尔产品集团的接下来会发生什么；英特尔的客户端 CPU 问题；以及他们在 Bartlett Lake 上的绝望一搏。我们还将深入 NVIDIA 的定制 PC 芯片及其激进的三芯片 Tegra 战略——该战略很可能从英特尔手中夺走可观的份额。随后，我们将讨论英特尔当前的数据中心 CPU 路线图，从 Sierra Forest 和 Granite Rapids，一直到 Clearwater Forest、Diamond Rapids 与 Rogue River Forest。然后，我们将讨论为什么“系统代工厂”（Systems Foundry）路径才是拯救英特尔的那条路，以及为什么必须卖掉 PC 业务。
