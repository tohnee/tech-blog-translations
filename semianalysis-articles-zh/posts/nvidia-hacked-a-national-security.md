---
title: "英伟达遭黑客攻击——一场国家安全层面的灾难"
title_en: "Nvidia Hacked - A National Security Disaster"
date: 2022-03-02
source: https://newsletter.semianalysis.com/p/nvidia-hacked-a-national-security
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 英伟达遭黑客攻击——一场国家安全层面的灾难

> 原文：[Nvidia Hacked - A National Security Disaster](https://newsletter.semianalysis.com/p/nvidia-hacked-a-national-security) · SemiAnalysis

英伟达（Nvidia）遭遇黑客攻击，大量数据失窃。此次事件不仅对英伟达本身是一场灾难，对所有芯片公司以及所有「西方」政府的国家安全而言也是如此。一个名为 Lapsus$ 的黑帽组织声称对此次攻击负责，并表示自己并非国家级行为体（nation state actor）。

Lapsus$ 的诉求颇为奇特。最初的要求是支付赎金，随后又追加了多项要求，包括推送驱动更新、将大量软件开源，以及彻底移除所有加密货币挖矿限制器。英伟达尚未同意其中任何一项要求，执法部门已经介入。此次攻击中已经公开的内容就已有重大影响，而其威胁于周五发布的材料，将构成一场国家安全层面的灾难。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ad7aa7e0-58b3-497e-a0ae-9903d5f2deb7_542x678.png)

在最初攻击之后，Lapsus$ 宣称掌握了超过 1TB 的数据。该组织声称[英伟达曾试图反向攻击他们](https://twitter.com/vxunderground/status/1497484483494354946?s=20&t=Xi7NvYlFXXlzyHEWmml3Og)。作为回应，黑客[发布了一份文件](https://twitter.com/darktracer_int/status/1497464801877839872?s=20&t=laV__odCAmU7zFfmH5LMCQ)，其中包含英伟达全体员工的密码哈希。这是一次严重打击，但相较于他们此后发布的其他数据还算轻微。在最初的公告中，他们还表示正在出售「full LHR V2」。

2021 年 2 月，英伟达在其最新的 RTX 3060 GPU 上实施了 LHR（Lite Hash Rate，轻量哈希率）机制，将 Ethereum 等主流加密货币的挖矿速率减半。随着时间推进，他们将这一机制推广到全部游戏 GPU，以此降低 GPU 对矿工的吸引力，让玩家更能买得起。「full LHR V2」据称可以绕过英伟达游戏 GPU 上的全部挖矿性能限制器。

该组织利用所获得的源代码访问权限，重新编译了不含挖矿限制器的驱动程序，并立即以 $10 的价格出售。随后他们将价格调整为 $1,000,000。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/dd51390a-7cd9-4849-9286-235821557a28_542x677.png)

此后，他们又发布了一个包含大量数据的文件。其中包括驱动的全部源代码，使其他公司可以自行重新编译驱动。这些源代码不仅涵盖游戏驱动，还包括数据中心和 AI GPU 驱动、英伟达专有的 AI 超分辨率技术 DLSS、Ansel、英伟达文档，以及 NV-Torch 和 NV-Caffe 等英伟达 AI 库。此外，该文件包含英伟达面向下一代 GPU（即 Hopper 和 Lovelace）的全部 GPU 架构配置文件。最后，其中还包括英伟达的测试器（tester）和仿真文件。

仅凭这些数据，就可以看到英伟达直至架构决策层面的规划，以及其今年晚些时候将发布的 GPU 的具体配置。英伟达的产品周期为 2 年，因此泄露的数据所对应的，是英伟达直到 2024 年仍将作为顶级产品销售的东西……一场彻底的灾难。

英伟达的专有软件被认为是其对竞争对手的优势所在。其中一部分就是测试器和仿真器文件。这些文件展示了英伟达如何仿真其芯片设计、如何权衡各种架构决策。简而言之，这是英伟达专有设计流程中的关键部分，如今已进入公共领域。凭借这些数据，多家中国 AI 和 GPU 公司可以在 GPU 设计上实现跨越式追赶。西方竞争对手由于法律和伦理原因绝不会碰这些数据，但正如华为（Huawei）过去二十年所展示的那样，许多其他参与者会公然违反这些规范。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/7d730d91-6b2f-4b18-989d-0804579d6be8_530x560.png)

该组织目前正威胁发布一个大小为 250GB 的硬件文件夹。他们声称该文件夹包含关键芯片设计文档和代码，其中包括 Verilog。一旦获得这些访问权限，就等于直接接触到英伟达的设计。此外，他们声称掌握与英伟达 Falcon 控制和安全处理器相关的全部细节。心怀不轨的半导体公司可以翻阅这些文件，尽可能多地学习，并将这些心得直接应用到他们的未来产品中。他们甚至可以走得更远——为 SMIC 的 14nm 制程节点反向工程这些设计。唯一的慰藉是 Verilog 文件有可能是加密的。

过去，曾有一名恶意行为者[攻击了 AMD](https://wccftech.com/amd-stolen-gpu-ip-exclusive/)，获取了其 Navi 21 GPU 的 Verilog 文件。该黑客索要 $100 million，但那些文件并不完整、如同天书。而 Lapsus$ 所拥有的访问权限级别，使得他们很可能掌握完整且未加密的 Verilog 文件。鉴于此次英伟达被黑事件的严重性，半导体架构设计人员和各家公司很可能不得不提升 IT 安全等级。甚至公司内部的资料共享，也很可能因这些安全漏洞之后必须落实的新安全规程而受到影响。

完整的 Verilog 数据一旦发布，对英伟达和西方国家安全都将是彻底的灾难。本质上，这些芯片的蓝图——一家市值 $580 billion 的公司、投入 $30 billion 研发费用的成果——可能落入敌对行为体之手。这批失窃数据本可以出售给某个国家级行为体，很可能成为一代人时间里最具战略意义的企业间谍行为。中国的设计公司一旦直接接触到全球最先进 GPU 和 AI 处理器的设计，就有可能大幅提升其在人工智能和半导体各个相关领域追赶西方竞争对手的速度。如果这批数据尚未落入中国手中，美国政府应当动用其网络安全武器库，阻止中国（PRC）公司获取这些数据。这项知识产权必须得到捍卫。

[分享](https://newsletter.semianalysis.com/p/nvidia-hacked-a-national-security?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

编辑注：英伟达已联系我们，并让我们参考[其官方声明](https://nvidia.custhelp.com/app/answers/detail/a_id/5333)。我们同意其说法，不认为此次事件与俄乌冲突有关。就所涉材料而言，此次安全泄露事件的重大性其实无需讨论，这些材料确实关系到国家安全利益。英伟达的技术是西方在半导体和计算诸多领域主导地位的核心。

> 我们没有证据表明 NVIDIA 环境中部署了勒索软件，也没有证据表明此事与俄乌冲突有关。

*本文最初于 2022 年 3 月 3 日发布于 [SemiAnalysis](https://semianalysis.com/nvidia-hacked-a-national-security-disaster/)。*
