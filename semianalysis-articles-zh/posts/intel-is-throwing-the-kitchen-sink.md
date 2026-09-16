---
title: "英特尔是不是在病急乱投医：翻身计划合理吗？"
title_en: "Intel Is Throwing The Kitchen Sink, But Is The Turn Around Plan Reasonable?"
subtitle: "深度解析 Tower Semiconductor 晶圆厂与 IP、英特尔文化转型、各业务部门未来产品与路线图竞争力"
date: 2022-02-18
source: https://newsletter.semianalysis.com/p/intel-is-throwing-the-kitchen-sink
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 英特尔是不是在病急乱投医：翻身计划合理吗？

> 原文：[Intel Is Throwing The Kitchen Sink, But Is The Turn Around Plan Reasonable?](https://newsletter.semianalysis.com/p/intel-is-throwing-the-kitchen-sink) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**深度解析 Tower Semiconductor 晶圆厂与 IP、英特尔文化转型、各业务部门未来产品与路线图竞争力**

# **英特尔文化翻身**

英特尔的投资者日非常精彩，超过 10 位高管登台亮相并发表讲话。Pat Gelsinger 当然光彩夺目，他那神采飞扬、兴致勃勃的姿态展露无遗。毫无疑问，他已经带来了一场文化变革：从彻底重组各业务部门，到一年内招聘超过 17,000 名员工，再到提高关键设计与晶圆厂员工的股权激励。如今英特尔的士气已大幅提振。

> 首先，我们正在重建我们所说的「（Andy）Grove 式」执行力，找回 Andy Grove 的那股精气神——自信、以工程为中心的传统、纪律和竞争精神。

我们 SemiAnalysis 之所以愿意认真考虑「技术上翻身」这个想法，唯一的原因就是这家公司发生了清晰可见的文化转变。稍后我们会更多谈及技术层面——以我们批判性的视角来看，对那部分我们并不那么乐观——但先来聊聊这场文化转变。

> 我们做出了一些根本性的改变。如果你听了上午（Dr.) Ann (Kelleher) 的环节，就会知道我们在拥抱 EUV 上实现了巨大飞跃。我们建立了深度合作伙伴关系。**过去我们跟设备厂商说：把机器卸在收货码头就行，剩下的我们自己搞定。**

这是一个不应被低估的关键点。过去，由于 Sohail Ahmed 和 Brian Krzanich 这样的人物，英特尔的晶圆厂存在着一种有毒的文化。晶圆厂自认为是王者，为所欲为。在很长一段时间里这确实说得通，因为他们远远强于地球上任何其他团队。晶圆厂团队傲慢到甚至会对设备厂商置之不理。

一个真实的例子就是英特尔的 10nm 节点。英特尔 10nm 的（众多）问题之一与在通孔和互连中使用钴有关。长话短说、省去技术细节：当时的种子沉积和退火工艺尚未成熟，这会引发严重问题。Applied Materials 曾告知英特尔这项技术还没有完全准备好登场，但英特尔无视警告仍执意推进。故事的结局我们都知道了——花了整整数年时间，良率才真正达标并实现爬坡。曾担任 Applied Materials 半导体业务总经理的 Dr. Randhir Thakur，如今执掌英特尔的代工服务与供应链。英特尔如今对其供应商的尊重程度已大不相同。

> 现在我们与他们深度合作。尤其是**与 ASML 的关系堪称绝佳**。我们重建了领导团队。

当前这轮翻身中被低估的一个方面，是与设备供应商的关系。2010 年代，设备厂商并不太喜欢英特尔：英特尔自以为比你聪明，对你指手画脚。而这些设备厂商也不希望尖端制程成为一家独大的独角戏。

直到 2010 年代中期，站在先进制程最前沿的只有英特尔一家，其他所有人落后数年。英特尔现在落后 TSMC（台积电）大约两年，但它可以借助设备厂商的经验教训来更快地爬坡。设备厂商清楚自己的设备用在哪里、怎么用。与设备厂商紧密合作极其重要。

例如，英特尔与 ASML 的关系就是一大优势。ASML 正在帮助英特尔学习如何爬坡 EUV，向其多家晶圆厂发运大量 EUV 设备，甚至会把第一台量产型 High NA EUV 设备交给英特尔。其他设备厂商也在给予英特尔类似的优待。我们还看到三星在其即将推出的环栅（GAA）制程上也获得了某种类似的待遇，我们将在后续文章中详细介绍。订阅本报，即可在该文发布时收到提醒。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

> 我们正在借助的**不仅是设备行业的专业力量，还有 EDA 行业，并转向行业标准的设计工具和 PDK。经常与业界和设备厂商交流的朋友，对此一定深有共鸣。**这是一个全新的英特尔，比以往任何时候都**更开放、更投入、更主动**。

我们可以印证这一说法。关于行业标准设计工具和 PDK，后文 Tower Semiconductor 一节会详述。抛弃陈旧迟缓的内部工具、转而采用远更高效精简的工具，是重要、必要且关键的举措。不过要说清楚：采纳这一切技术并不能保证英特尔一定赶上。

> 我们重新加大了投入。我掏出了支票簿。Andy Grove 曾对我说过一句话：我以为给你的是无限预算，你居然还能超支。**嗯，某种程度上，我们给了（Dr.) Ann (Kelleher) 无限预算，并对她说：把我们的制程拉回正轨。**为此我们在设备和工程上投入了重金。

负责路径探索和制程节点开发的英特尔器件研究（components research）与长期开发团队，获得的资源大幅增加。此外，他们可以使用所有半导体设备厂商最先进的工具；人员更多、薪酬更高，管理结构也大为改善。这一组织架构调整，尤其是在长期开发部门内部，是一个值得关注的转变。「制程节点」一节会详细展开。

Auguste Philip Richard 提出了一个关于人员招聘的绝佳问题。如果你像我们一样追踪 LinkedIn 上的工程师流动，就会看到大批优秀工程师从生态系统的四面八方涌向英特尔——无论是英特尔的竞争对手、供应商、客户、云计算厂商，还是苹果，无处不在。

> 一个简单的问题。Pat，你招了一批了不起的人，而且他们看起来并不是冲着钱来的。那你的「推销话术」是什么？你是怎么把这些人才招进门的？难道就凭那个「不可能完成的使命」吗？任何补充信息都会非常有帮助。
>
> 正如我之前所说，我们身处一场使命之中。对「**英特尔作为硅谷、作为整个行业、作为全世界的基础性科技公司**」这一信念，我们几乎有着一种非理性的执着。我们正在组建的这支团队，我喜欢称之为我的「五年之队」——我们亲密无间、团结一致，因为我们即将共同踏上征程，去**恢复这个行业中最具标志性的公司**，去把握眼前这一系列非凡的机遇，去为未来开创具有颠覆性的新业务。这段旅程正在激发公司内部 12 万名员工的惊人能量，而领导团队同样看到了这份机遇与热情。
>
> 具体落地来说，我们得照顾好我们的员工，对吧？**我们必须给他们优厚的报酬，但顶尖人才加盟是因为他们相信这项使命。**然后他们会说，**我想攻克最艰难的问题。**再然后，**我想和最优秀的人共事**，**我想要一个自己愿意融入的文化和环境。**最后才是——哦对了，我也想获得丰厚的回报。顺序就是如此。我们正在组建的，是一支相信这项使命的团队：英特尔是那家能够交付改善地球上每一个人生活的技术的公司。这就是我们的使命，而我们拥有完成它的一整套独特资产。

这里面当然有 CEO「推销自家股票」的成分，但不妨去和那些重返英特尔的人聊聊。确实有不少人发自内心地认为英特尔必须复兴，否则「西方世界」将失去其全部硬件技术优势。在某种程度上，我们同意这些人的看法。

> 我们已将其推广到整个组织。我们重建了决策流程。**我们恢复了 OKR（目标与关键成果）。**为什么当初停用？这可是我们发明的。硅谷其他公司都 embrace 了它，我们却弃之不用——现在我们重新用起来了。**公司里每个人的部分财务回报都与他们的 OKR 及个人执行情况挂钩。**「文化正在重建」。

另一项巨大变革是回归 OKR。我们不会深入展开 OKR 是什么，简言之，它是跟踪目标与成果的重要框架。它让人保持责任心，由 Andy Grove 发明。当年废除 OKR、改用其他绩效指标的正是 Brian Krzanich。回归 OKR 应有助于让人们负起责任、接受监督，也让绩效考核更加公平。

> 我回到公司时，**我们正在流失人才**，你们当中许多人都在写文章讨论**人才外流**。现在情况变了，我们如今看到**人才回流**。2021 年我们招聘了 17,000 名技术人员，其中许多人来自主要竞争对手，他们说：「哇，这挺酷的，让我去加入他们正在做的事情吧。」还有许多是回流的老员工，他们回来说：英特尔回来了，我要参与其中。乐队重组了，魔力回来了。英特尔之所以闻名，正是凭借这种纪律、创新与执行的强大文化——我称之为我们所要的 Grove 式文化。

# **英特尔制程技术**

英特尔翻身中最庞大、最艰巨的任务是制程技术。从 Intel 7 到 Intel 4 的爬坡大约落后 TSMC 的 N7 到 N5 制程节点爬坡 2 年。如前所述，英特尔正处于追赶期，无需重复发明轮子，这应该能让 Intel 4 和 Intel 3 的爬坡更顺利。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/b149a966-38c5-437b-af5d-0ce0aee7fbc6_1024x533.png)

Intel 20A 才是真正的考验。英特尔必须交付 RibbonFET 和 PowerVia 这类巨变——这两项特性在整个行业中都尚未量产。为达成目标，他们引入了一种新的模块化设计架构，称之为「Tick-Tock（嘀嗒）」。看起来，主要的前端晶体管间距微缩随 tick 节点而来，而 tock 则是在该基础上的优化与进一步增强。

英特尔正在简化开发用的工艺流程，并审慎权衡创新、执行力与可预测性这一多变量问题。Tick-Tock 模式让工艺开发管线的各个环节拥有更强的独立性，可以单独监测和管理，而不影响整个工艺。例如，不同团队可以分别负责信号互连、供电和晶体管。这些划分与断点被称为工艺模块。每个团队承担更高程度的责任，学习速度也随之加快，因为不同特性可以视情况引入或移除。

英特尔给出的例子是 PowerVia，也就是行业所称的背面供电网络（BSPDN）。如今在所有代工厂中，电力层和信号层都包含在同一个互连堆栈里。PowerVia 把全部供电抽取出来放到晶圆背面，使信号互连和电力互接可以针对各自任务进行更高度的优化。

英特尔有一个定制版的 Intel 3 工艺节点，用来测试这套工艺流程：先构建晶体管层，再构建信号互连，然后与支撑晶圆键合，翻转组合后的晶圆，露出原始晶圆上的纳米级 TSV，最后构建供电网络。工艺中的这个模块可以完全独立于晶体管架构变革（RibbonFET）之外进行测试和调试。针对这些高风险工艺变更，英特尔已备有主动的风险评估和应急方案，确保某个模块的延迟不会拖累整个制程节点。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a1cb2161-32b0-49ac-abce-9f46a7e7ab50_1024x532.png)

在代工服务模式下，只向外部提供 tock 节点。正如 TSMC 总是用苹果来首发其最新节点（如 N5），之后其他客户才陆续上车，英特尔似乎也将在 tick 节点上先行内部设计。TSMC 在 N5P、N4 这类节点上迎来的客户潮要大得多；同样的逻辑适用于英特尔的 tock——向代工客户提供更完善的 tock 节点。这对代工客户而言是多一层的风险消除，因为他们知道，早在自己爬坡之前一年，英特尔已在内部把该节点的大部分风险化解掉了。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/4e871d6c-ec41-4c1b-bc57-b69c7adae6b8_1024x539.png)

英特尔正在 Intel 4 上爬坡多款产品，包括 Meteor Lake 和一款定制网络 ASIC。与此同时，Intel 3 将伴随 2 款 Xeon 产品爬坡，这将在数据中心一节讨论。今年下半年，英特尔将在晶圆厂为这些 2024 年产品流片并运行测试晶圆。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d2c792a4-e1fb-478a-9d67-7ea6e4fda270_1023x499.png)

英特尔也在用不同团队并行开发 20A 和 18A。这两代节点将引入前述的 RibbonFET、PowerVia 以及 High NA EUV 光刻。英特尔表示，今年下半年将为一款 2024 年客户端产品运行 IP 测试晶圆。18A 将于今年上半年向代工客户交付一些测试芯片，下半年进行 IP shuttle（多项目晶圆试制）。这些都不是完整芯片，但足以让潜在客户逐步熟悉该制程节点。Pat Gelsinger 甚至在台上直接展示了一张 18A SRAM 测试晶圆！

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c1284284-c9d8-4c5c-9f02-aa892f0d08ea_1024x576.jpeg)

发布会上还分享了一些封装方面的信息，但对于读过我们先进封装系列文章的读者来说，这次演示的内容可以说毫无新意。

[先进封装 第 1 部分——焊盘受限设计、半导体尺寸微缩经济性解析、异构计算与小芯片](https://semianalysis.substack.com/p/advanced-packaging-part-1-pad-limited)

[先进封装 第 2 部分——Intel、TSMC、Samsung、AMD、ASE、Sony、Micron、SKHynix、YMTC、Tesla、Nvidia 的选项与应用盘点](https://semianalysis.substack.com/p/advanced-packaging-part-2-review)

[先进封装 第 3 部分——英特尔对热压键合的奇怪豪赌，以及 ASM Pacific、Kulicke and Soffa、Besi 的 TCB 设备格局](https://semianalysis.substack.com/p/advanced-packaging-part-3-intels)

如果你希望在第 4 部分发布时收到通知，请订阅本报。届时我们将深度解析混合键合生态：从当前所有应用，到未来数代的路线图，再到从设备到 IP 授权的供应链参与公司。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

# **英特尔代工**

代工业务对英特尔维持规模、稼动率和运营效率至关重要。老模式是让一个主力节点爬坡，然后把大部分设备转移给下一代节点，这并不高效。英特尔特别提到，在 14nm 到 10nm 节点转换中，90% 的设备可以转移——这意味着 10% 的设备会随着老节点退坡而不得不出售。此外，英特尔还得做额外的工程工作，确保旧设备能够转移。

很多时候，设备厂商会发布更适合当前任务的新版设备，但英特尔不去购买新设备，而是围绕旧设备改造工艺。在「Copy Exact（精确复制）」模式下——爬坡期间所有厂区使用相同的设备和工艺——英特尔会加订更多旧设备，单位美元的效率未必划算。我们在[上个月的这篇文章](https://semianalysis.substack.com/p/is-intel-shipping-tools-out-of-us)中更详细地讨论过这个话题。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ba6260f8-f976-48b1-bc8a-b2ea2826f2ec_1024x565.png)

除了让老节点持续生产带来的资本效率收益外，英特尔还受益于持续高位的晶圆投片量。在半导体制造中，稼动率就是王道。GlobalFoundries 就是绝佳例子——十年间[穆巴达拉（Mubadala）在它身上亏损超过 $22.4B](https://semianalysis.substack.com/p/globalfoundries-gfs-ipo-mubadala)。它曾长期被低稼动率拖累，而如今满产运行（稼动率 100%），且未来几年都将如此。仅这一项改变，就让它蜕变为一家盈利公司、一笔值得的投资。

英特尔需要代工业务带来的规模，才能持续投入后续节点。它目前的体量尚可支撑接下来几次节点转换的资金，但 TSMC 的规模和产量会持续增长，尖端制程的开发成本终将高到难以承受。

英特尔进军代工不仅是多元化，更是必然之举。IDM（垂直整合制造）模式无法永远延续。英特尔要走上代工之路，需要投入大量资金。途径之一是兴建更多晶圆厂。英特尔表示，这些新厂的资金将部分来自现有业务、更多债务、出售 Mobileye 小部分股权、政府补助以及客户预付款。

英特尔还提到了合作共建的可能性，并与 Brookfield Asset Management 签署了谅解备忘录（MOU），为晶圆厂建设提供资金。Brookfield Asset Management 是一家国际房地产和私募股权公司，业务触角广泛。我们认为，这类合作的设计正是为了利用当前市场——投资者已把基础设施和房地产售后回租的回报率压到了极低水平。许多公司自建总部大楼，转手卖给 Brookfield 这类公司，再长期租回。我们完全可以设想这样的方案：英特尔建好晶圆厂外壳，连同数十年的租约一起卖给 Brookfield。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/43e1bfd8-9c5a-45ad-9390-70e75db559b8_1024x554.png)

与其他年份相比，英特尔 2022 年的支出明显向技术开发倾斜。2022 和 2023 年将包括晶圆厂外壳的大规模建设。这些厂壳可以选择空置待用，让英特尔在产能爬坡上更具灵活性。2022 和 2023 年设备支出也在上升，但真正的重头戏要到 2025 和 2026 年——届时代工业务将开始大举采购设备。

英特尔的长期模型是，资本开支约占营收的 25%。这低于 2022 和 2023 年的 35%，但高于英特尔历史上的水平。资本密集度上行，对 Applied Materials、ASML、Lam Research、KLA、Tokyo Electron、Onto、Nova、Entegris 等公司是重大利好。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/72da144c-92d8-4e81-99f4-74406f1dafa8_1024x565.png)

英特尔特别说明，这些资本开支数字是净值。也就是说，如果英特尔能通过政府补助和补贴、与 Brookfield Asset Management 的潜在合作以及客户预付款来冲抵支出，那么它的（总）支出只会更高。英特尔保守地将这些冲抵按 10% 计入，但实际数字可能远高于此——如果美国和欧盟终于认识到，没有能与亚洲各国税法和政府预算中既有半导体补贴相匹敌的补助，他们将在硬科技领域被彻底甩在身后的话。

英特尔在代工雄心上夸下海口，但 SemiAnalysis 对其入局存有许多疑问。收购一家代工厂，是加速 Intel Foundry Services 发展的必要之举。

我们曾十分看好传闻中收购 GlobalFoundries 背后的战略。我们的消息来源显示，英特尔确实发出过收购要约，而穆巴达拉确实因监管和时间问题拒绝了。客户不会乐见英特尔获得那样程度的信息披露，而且即使能获得监管批准，这桩收购也很可能需要 18 个月。18 个月后，GlobalFoundries 的翻身早已全面展开，其价值将远高于英特尔的报价。

收购落空后，英特尔只得将目光转向其他代工厂。GlobalFoundries 之后规模最大的是 UMC（联电），但台湾方面不会放行；SMIC（中芯国际）位列第五，在中国同样行不通。再往下数，Powerchip（力积电）、Vanguard International Semiconductor（世界先进）和 Hua Hong（华虹）都存在同样的问题。剩下唯一具备合理产量和规模的，就是总部位于以色列的 Tower Semiconductor。

# **Tower Semiconductor**

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1b093bba-9b84-456c-898f-56f824ff3f42_1023x554.png)

收购 Tower Semiconductor，填补了英特尔在先进 FinFET 之外各制程节点代工产品线的诸多缺口。Tower 为英特尔带来了成功服务多个外部客户、且盈利运营特色工艺技术的团队。英特尔在代工领域最大的短板，是缺乏创建和维护简洁而灵活的工艺设计套件（PDK）的能力。老英特尔使用的多为高度定制、只满足内部需求的流程，拉长了芯片设计的开发周期——这在代工业务中是致命伤。随着英特尔努力采用更多行业标准流程，PDK 能力是它极需外援的领域。Tower 在特色利基工艺上的能力，切实提升了其打造并提供灵活、可扩展 PDK 的能力。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/94174de9-f98f-4fa0-ab06-574e7c6200ee_1024x408.png)

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

Tower Semiconductor 提供广泛的技术组合：RF CMOS、SiGe 功率 IC、分立器件、CMOS 图像传感器、光子学、RFID、双极 CMOS（BiCMOS）、绝缘体上硅（SOI）、LDMOS 晶体管、MEMS、晶圆键合、Y-Flash 忆阻器以及高性能模拟。松下（Panasonic）是 Tower 最大的客户，但它还有众多其他客户。以下是我们对 Tower 技术组合的拆解。

- **硅光子学**——Tower 利用其 SiGe BiCMOS 工艺集成光学器件，面向数据中心通信市场。该平台可将光电探测器、光调制器和激光器集成到单一裸片上。
- **RF CMOS**——用于高集成度收发器、功率放大器和调谐器。集成电感、可变电容和横向扩散 MOS 晶体管都可在单一裸片上制造。
- **绝缘体上硅（SOI）**——Tower 制造天线开关和前端模块，常见于智能手机。
- **RF BiCMOS**——类似 RF CMOS 但功能更多，主要销售给专用收发器和调谐器。可集成高速双极晶体管，设备要求也更为专用。
- **SiGe BiCMOS 与模拟**——比标准 BiCMOS 功能更多，面向更先进的射频应用。瞄准高性能模拟半导体，用于高速、低噪声、高集成度的多频段无线收发器、光网络器件、车载雷达、硬盘前置放大器、功率放大器和低噪声放大器。集成性能高得多的硅锗双极晶体管。该工艺系与一家半导体资本设备供应商深度合作开发，为 Tower 独有。Tower 是 SiGe 出货量最大的厂商。我们好奇 Tower 的工程师能否帮助英特尔在未来的先进节点上实现 SiGe 沟道。
- **CMOS 图像传感器与晶圆堆叠**——Tower 的 CMOS 图像传感器常见于尼康相机，但也用于车载传感器和智能手机等许多高端应用。其图像传感器有 2 个主力工艺节点：200mm 晶圆上的 110nm 和 300mm 晶圆上的 65nm，像素尺寸最小可达 1.12 微米。Tower 支持双光管（dual light pipe）、卷帘快门和全局快门。Tower Semiconductor 还提供背面照明（BSI），这是 3D 晶圆堆叠的一种形式——将数字 CMOS 晶圆堆叠在减薄后的图像传感器晶圆之下。
- **X 射线与光罩拼接**——在 X 射线领域，Tower 开发了光罩拼接（reticle stitching）能力，使芯片可以超出单张光刻光罩的尺寸。该技术在 0.18 微米节点和 65nm 节点提供。X 射线芯片销往牙科、CARM（C 臂）、血管造影、乳腺摄影以及工业无损检测领域。所产 X 射线传感器可以大到用一整片 300mm 晶圆只切出一个裸片。
- **其他传感器**——Tower 还能制造用于手势识别的红外传感器和光谱敏感度传感器。它还提供间接和直接飞行时间（ToF）3D 传感器，用于 VR、AR 和智能手机。这些传感器也可用于人脸识别。单光子雪崩二极管（SPAD）和 LiDAR 也由 Tower 制造。
- **MEMS**——Tower 在 MEMS 麦克风领域份额很高，该产品无处不在——从真无线耳机到手机再到工业应用。
- **Micro-LED 与 Micro-OLED**——Tower 的光罩拼接能力还使其成为 Micro-LED 领域的新兴供应商，用于 micro-OLED 和 LCOS 显示的单片阵列。它还在开发基于 GaN 纳米管的 LED，随后可放置到背板上。这是 Tower 特别指出需要更多投资才能扩产的机会。我们希望英特尔继续投资 Tower 的 Micro-LED 技术。
- **电源管理 IC**——产品包括低压 BCD 和高压产品。低压方面，BCD 是技术优势所在，包括 5V、8V、12V、40V 和 60V 器件，用于电压调节器、电池充电器、电源管理产品和音频放大器等电源与驱动类半导体。高压方面，提供 140V Resurf、200V SOI 和 700V 技术，用于汽车、工业、AC 适配器和照明市场中分立高功率晶体管的栅极驱动器。
- **非易失性存储**——Tower 开发了名为 Y-Flash 的非易失性存储方案。它可以集成到电源管理产品中——在严苛工况下，其他形式的存储器会失效。

收购 Tower 使英特尔能够提供更完整的技术组合，并借自身规模加以交付。Tower 则需要英特尔帮助其扩产晶圆厂，从而有能力供应电动汽车电池管理系统、硅光子学等大型垂直市场。英特尔则可以借助 Tower 与代工客户的既有关系直接起步，并将其转化为 Intel Foundry Services 的更多业务。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/04974cba-0acd-4f68-a89a-db0a66e4a040_1024x569.png)

Tower 与英特尔联手后将聚焦计算、移动和汽车三大板块。英特尔宣称，自己是全球仅有的两家产品线覆盖从微米级节点一直到 10nm 以下节点的代工厂之一——另一家是 TSMC。英特尔试图把自己定位成唯一竞争者。这套说辞无视了一个事实：即便有了 Tower，英特尔在 45nm 到 28nm 制程节点区间的缺口依然严重。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/458fabf4-1fe1-4dd0-98d9-d347821388b7_1024x512.jpeg)

英特尔宣布了又一位代工客户：思科（Cisco）。Cisco Silicon One 一直是一项有趣的战略，从带深缓冲区的服务提供商网络路由器，到功耗与成本优化的互联网规模（web-scale）机柜顶层交换机，从线卡到交换机全覆盖。Cisco Silicon One 一直是 Samsung Foundry 的大客户，但看起来英特尔把这笔生意抢走了。[Achronix](https://semianalysis.com/achronix-goes-public-the-only-independent-leading-edge-fpga-silicon-and-ip-provider/) 和 [Amazon](https://semianalysis.substack.com/p/amazon-graviton-3-uses-chiplets-and?r=cyw3q) 也早已是英特尔的代工客户——英特尔向其发货并确认收入，我们过去曾撰文介绍过。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

英特尔还是美国政府 RAMP-C 项目的代工承约方，该项目包括与 Qualcomm、IBM、Synopsys、Cadence 和 Microsoft 的合作。他们宣称拥有超过 5 个「处于设计导入阶段的锚定客户」，以及 2022 年超过 30 款测试芯片。英特尔正瞄准 ADAS、射频、传感器和电源管理方面的汽车市场，甚至在代工服务业务内部设有一支专攻该市场的团队。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/7504f132-f145-4fe1-93be-019c2001acd7_1023x541.png)

英特尔宣称现有代工业务 2021 年营收为 $800M。即便算上 [Achronix](https://semianalysis.com/achronix-goes-public-the-only-independent-leading-edge-fpga-silicon-and-ip-provider/) 和 [Amazon](https://semianalysis.substack.com/p/amazon-graviton-3-uses-chiplets-and?r=cyw3q) 的业务，这个数字看来也偏高。我们不确定其余收入从何而来。即便在最乐观的情形下，我们对 Achronix 和 Amazon 合计的估计仍低于 $500M。也许英特尔已经开始从国防部获取收入。

# **数据中心与 AI**

把话说清楚：至少到 2024 年、甚至更久，英特尔在服务器市场都会被碾压。而 Icelake 对阵 Milan，差距已经坏到无以复加。Sapphire Rapids 对阵 Genoa 依然差距巨大，只是没有前者那么夸张。再往后，Emerald Rapids 要同时迎战 Genoa 和 Bergamo，而且两者都打不过。最有看点的是 2024 年的产品。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/187373a5-7025-48f0-9e9f-8c7c901fc5f1_624x416.png)

Granite Rapids（GNR）再次被重新定义，Sierra Forest 也是。Granite Rapids 最初是 2022 年产品，被推迟到 2023 年并调整了规格；如今成了 2024 年产品，CPU 核心转移到 Intel 3 节点。Sierra Forest（SRF）亦然。从第一次重新定义起，我们就知道二者都将属于采用 LGA7529 插槽的 Birch Stream 平台。不过制程节点并非一成不变：英特尔似乎也把 Sierra Forest 从 TSMC N3 转到了 Intel 3。这对内部节点的健康度是一个非常积极的信号。即便如此，Granite Rapids 对阵 AMD 的 Turin 仍无竞争力，Sierra Forest 恐怕也敌不过 Bergamo +1。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d5704e3c-1c64-40ac-964d-7aef1f1db9ea_800x201.png)

AI 部分还要更糟。Habana 软件孱弱，市场渗透几乎为零。英特尔买下的这个团队，其第一代产品就因软件问题多次推迟；基于 TSMC N7 的第二代产品也从当初向英特尔承诺的去年年底推迟到了今年晚些时候。总而言之，英特尔在这桩收购中显然没有做好尽职调查，而后果已经显现。

# **网络与边缘**

这是英特尔内部最有前景的业务部门，也最有可能达成甚至超越其营收目标。它的硬件竞争格局远远好于其他部门；在适用之处对外部与内部代工的运用也最为先进，包括用 TSMC N7 生产 DPU（IPU）、用 Intel 4 生产定制网络 ASIC；软件套件维护得最好，正在重新架构网络的管理方式。英特尔的网络与边缘团队还与客户最紧密地合作开发硬件平台。固定功能硬件正在被替换为软件可编程模型，同时在合理之处保留固定功能硬件。凭借 OpenVino，网络与边缘团队站在了 AI 推理革命的前沿。

1. 经济学定律——把数据搬到云端的成本可能过于高昂。
2. 物理学定律——工作负载可能没有时间（延迟预算）把数据送到云端处理。
3. 法规定律——监管或安全原因可能要求数据留在本地、不得上云。

英特尔的网络硬件有助于化解上述三方面的顾虑，同时提供边缘算力。边缘算力往往能带来更优的 TCO。针对云数据中心，英特尔拥有从硅光子学、以太网交换机、NIC 到 DPU（IPU）的解决方案。英特尔正在为其 DPU 打造开源软件平台，这与 Nvidia、Marvell、Fungible、Pensando 和 Amazon 各自 DPU 的做法截然不同。英特尔拥有全球最好的硅光子学工艺，而[共封装光学（CPO）正是它杀入代工业务的特洛伊木马](https://semianalysis.substack.com/p/intels-trojan-horse-into-the-foundry?utm_source=url)。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

英特尔还有面向核心网络的产品：用于核心路由器和 NFV 工作负载的 CPU、NIC 和可编程交换机。托管（Colocation）边缘指大型数据中心之外的服务器托管，CPU 和 NIC 销往这一垂直市场。英特尔还面向网络边缘销售 CPU、NIC 以及用于 RAN 汇聚和边缘计算的 FlexRAN 软件。SnowRidge 是一款面向网络边缘和 5G 基站出售的 SOC。最后，本地（on-premises）边缘包括 Xeon/Atom CPU、Movidius VPU、FPGA 以及 OpenVino 等各类软件。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/53921636-2f8f-442f-a85e-46fc5aefb45e_1024x581.png)

该市场 TAM 以 12% 的速度增长，而英特尔预计网络与边缘将以 mid-teens（15% 上下）的速度增长。他们将持续抢占份额，成为边缘领域的大赢家。Nick McKeown 是这个行业的巨星，创办过许多成功的公司和产品。他最近一家被英特尔收购的公司 Barefoot 领先于时代——提供可编程交换机，并率先推出带共封装光学的交换机。我们预计，在 >100Tbps 交换机时代，英特尔将开始迅速蚕食网络交换机份额。Pat Gelsinger 似乎暗示当初是他亲自游说对方来执掌该部门，而能拥有他，是英特尔之幸。

# **加速计算与图形（AXG）**

我们对网络与边缘部门非常乐观，但对 AXG 则完全不乐观。他们必须打造一套庞大的软件栈；OneAPI 虽已超过 AMD 的 GPU 软件，但与 Nvidia 相比仍相去甚远。带 HBM 的 Xeon 产品只在极小的利基市场有用武之地。GPU IP 任重道远，同时对抗 Nvidia 和 AMD 将异常艰难。更糟的是，英特尔的游戏 GPU 采用外部制程节点，无法利用 IDM 优势打成本战。其较弱的架构会直接体现在裸片面积和 BOM 上。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1888914e-aa7d-48db-8ac1-3ff54f30601b_1024x593.png)

雪上加霜的是，英特尔的幻灯片还有点误导性。有没有人对「2022 年出货 4M 颗 GPU」和「营收 >$1B」的数字感到兴奋？说实话，我们一开始也是……直到开始细看脚注。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/311438a7-ba5d-41cd-b463-cee19cf18144_1024x189.png)

看出来了吗？

> AXG 营收包含部门间图形授权费，该费用在英特尔合并报表中会被抵销。这笔授权费 2021 年约为 $700M，到 2026 年将增长到约 $1B。

实际情况是：英特尔预计出货 400 万颗 GPU，但由此获得的营收只有 $300M，其余都是凭空记账的公司内部授权费？

这相当于约 $75 的平均售价（ASP）。

英特尔难道只是靠卖低端 GPU 来换取市场份额？

他们将销售 2 款裸片，其中较小的一款只有 128 个执行单元（EU）。作为参照：上一代 Tiger Lake 的集成 GPU 是 96 个 EU，下一代 Meteor Lake 提升到 192 个 EU。英特尔 GPU 销量中的绝大多数将以 ~$75 甚至更低的 ASP 投放市场，性能不如 AMD 的集成显卡，也不如英特尔自家的下一代 iGPU。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c85151f9-dd70-4ae5-8373-8968a3022a31_1024x513.png)

我们唯一能想到的解释是，英特尔声称的「出货 4M 颗」并不等于「确认收入的出货」。对于第一代独立 GPU，英特尔可能正在转向「超市模式」——直到 ODM 把笔记本电脑或 GPU 真正卖给终端用户或渠道之前，英特尔不确认收款。这一招其实相当聪明：英特尔可以用性能较差的 GPU 塞满渠道，而 ODM 即使卖不掉，资产负债表上也不承担任何风险。鉴于惊人的投入资本回报率，ODM 反而会有动力去推销英特尔 GPU。

我们尊重执掌英特尔 AXG 的 Raja Koduri，但他在这里的执行之路异常艰难。他接手的是全行业最差的 iGPU 架构——与 Nvidia、AMD、Arm、Imagination、Qualcomm、Apple 相比皆然——然后被要求化腐朽为神奇。我们最终希望英特尔的 AXG 能达到水准，但我们看不到任何理由让 AXG 在 2026 年实现 $10B 营收——即便算上 $1B 的公司内部授权收入。

这里唯一的亮点是 AV1 编码 GPU 和区块链加速器，两者看起来确实不错。我们不是币圈人，但一直密切跟踪性能、网络规模、算力（hashing power）和半导体需求。定制设计服务有可能成功，但这里存在一个大大的问号：到底什么样的半定制生意会落在这里。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/91edb70b-6229-41b8-8189-d1cf672ff0f4_1024x546.png)

Falcon Shores 是一款有趣而有雄心的产品，将 GPU 和 CPU 封装在同一基板上，但它将晚于 Nvidia 的 Grace Hopper 和 AMD 的下一代 HPC 处理器。

# **客户端**

到了这里，情况是每况愈下。客户端是英特尔最大的业务板块，但这里的一些预测非常值得商榷。英特尔预计 2022 年 PC 出货量超过 350M 台，并在未来几年继续增长。要说清楚：没有任何分析师或市场研究机构预测 PC 出货量会持续维持这么高。就连 AMD 也认为 2022 年总出货量持平。多数机构预计 2022 年持平于 350M 台，随后回归均衡水平。英特尔的数据非常偏离市场共识。顺便说一句，这些假设会直接计入它的财务模型……

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c86b86a1-6ecd-408e-acaa-fcb5f12f3a30_1023x565.png)

就竞争力而言，英特尔的移动端路线图还算有一定竞争力。Alder Lake 并没有像英特尔宣称的那样统治 AMD，但确有一番像样的缠斗。我们预计 AMD 和英特尔的性能领先地位会轮流坐庄。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/79fc346d-dc2e-4816-82c1-3a557862f8d6_1024x574.png)

# **软件与 Mobileye**

本文已经够长了，尽管我们过去对这两个板块做过大量研究且仍在持续跟踪，这里就不再展开。Mobileye 及其 IPO 会很有意思。我们喜欢这家公司，但一切取决于估值。软件方面：软件部门去年营收刚过 $100M，今年的目标是 $150M。软件的重要性更甚，因为它直接带动 AXG、数据中心以及网络与边缘的销售。

我们对财务指引的分析将放在付费订阅墙之后，包括我们认为英特尔股票究竟值不值得买。我们也会稍稍讨论代工业务和潜在的客户赢单。

[分享](https://newsletter.semianalysis.com/p/intel-is-throwing-the-kitchen-sink?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[立即订阅](https://newsletter.semianalysis.com/subscribe?)
