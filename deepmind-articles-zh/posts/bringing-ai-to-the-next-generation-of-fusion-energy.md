---
title: "把 AI 带入下一代聚变能源"
title_en: "Bringing AI to the next generation of fusion energy"
source: https://deepmind.google/blog/bringing-ai-to-the-next-generation-of-fusion-energy/
site: deepmind
date: 2025-10-16
crawled: 2026-09-13
translated: 2026-09-13
---

# 把 AI 带入下一代聚变能源

> 原文：[Bringing AI to the next generation of fusion energy](https://deepmind.google/blog/bringing-ai-to-the-next-generation-of-fusion-energy/) · Google DeepMind

我们正在与 Commonwealth Fusion Systems（CFS）合作，让清洁、安全、近乎无限的聚变能源更接近现实。

聚变是太阳的能量来源，有望提供清洁、充沛且不产生长寿命放射性废料的能源。要让聚变在地球上真正可用，意味着要让被称为等离子体的电离气体在超过 1 亿摄氏度的温度下保持稳定——并且全程不超出聚变能源装置的运行极限。这是一个极为复杂的物理问题，我们正在用人工智能（AI）求解。

今天，我们宣布与聚变能源领域的全球领导者 [Commonwealth Fusion Systems](https://cfs.energy/)（CFS）建立研究合作关系。CFS 正凭借其紧凑而强大的托卡马克装置 [SPARC](https://cfs.energy/technology/sparc)，开创一条更快的路径，通往清洁、安全、实际上近乎无限的聚变能源。

SPARC 利用强大的高温超导磁体，目标是成为历史上第一台产生净聚变能量的磁约束聚变装置——即聚变输出的功率超过维持聚变所需的功率。这一里程碑式的成就被称为跨越「能量持平点」（breakeven），是实现可行聚变能源道路上的关键节点。

这次合作建立在[我们此前利用 AI 成功控制等离子体的开创性工作](https://deepmind.google/discover/blog/accelerating-fusion-science-through-learned-plasma-control/)之上。我们与[洛桑联邦理工学院（EPFL）瑞士等离子体中心](https://www.epfl.ch/research/domains/swiss-plasma-center/)的学术伙伴合作，证明了深度强化学习可以控制托卡马克的磁体，以稳定复杂的等离子体形态。为了覆盖更广的物理范围，我们开发了 [TORAX](https://torax.readthedocs.io/)，一个用 JAX 编写的快速可微分等离子体模拟器。

现在，我们把这项工作带到 CFS，以加快向电网输送聚变能源的时间表。到目前为止，我们已在三个关键领域展开合作：

- 对聚变等离子体进行快速、准确、可微分的模拟。
- 寻找最高效、最稳健的路径，以最大化聚变能量。
- 使用强化学习发现新颖的实时控制策略。

我们的 AI 专长与 CFS 的尖端硬件相结合，使这次合作成为推动聚变能源基础性发现的理想组合，惠及全球研究界，并最终造福整个世界。

## 模拟聚变等离子体

要优化托卡马克的性能，我们需要模拟热量、电流和物质如何流经等离子体核心，并与周围的系统相互作用。去年，我们发布了 TORAX——一个为优化与控制而构建的开源等离子体模拟器，把我们能处理的物理问题范围扩展到了磁模拟之外。TORAX 基于 JAX 构建，因此可以轻松地在 CPU 和 GPU 上运行，并能平滑集成 AI 模型[包括我们自己的模型](https://github.com/google-deepmind/fusion_surrogates/)，以实现更佳性能。

TORAX 将帮助 CFS 团队在 SPARC 尚未启动之前，通过运行数百万次虚拟实验来检验和改进运行方案。当第一批真实数据到来时，它也让他们能够灵活快速地调整方案。

这套软件已成为 CFS 日常工作流程中的关键一环，帮助他们理解等离子体在不同条件下的行为，节省宝贵的时间和资源。

> TORAX 是一个专业、开源的等离子体模拟器，为我们搭建和运行 SPARC 仿真环境节省了大量时间。

Devon Battaglia

CFS 物理运行高级经理

## 寻找通往最大能量的最快路径

运行托卡马克涉及对各种「旋钮」的无数次调整选择，例如磁体线圈电流、燃料注入和加热功率。若靠人工寻找托卡马克产生最多能量、同时不超出运行极限的最优设置，效率可能非常低下。

将 TORAX 与强化学习或 [AlphaEvolve](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) 这类进化搜索方法结合使用，我们的 AI 智能体可以在模拟中探索海量的潜在运行场景，快速识别产生净能量的最高效、最稳健的路径。这能帮助 CFS 聚焦于最有希望的策略，从第一天起就提高成功概率——甚至在 SPARC 完全调试完毕、满功率运行之前就已开始。

我们一直在构建基础设施，用于研究各种 SPARC 场景。我们可以在不同约束下最大化聚变功率，或者随着对装置了解的深入，针对稳健性进行优化。

下面我们展示了在 TORAX 中模拟的标准 SPARC 脉冲示例。我们的 AI 系统可以评估许多可能的脉冲，找出我们预期表现最好的设置。

![一幅动画示意图，展示在 TORAX 中模拟的 SPARC 聚变脉冲场景：左侧是带有发光品红色等离子体的托卡马克横截面，右侧是一个黄色等离子体，最右侧是两个更小的带蓝色色调的备选场景。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/SPARC-cross-section.gif)

SPARC 横截面的可视化。左：品红色的等离子体。右：在 TORAX 中模拟的一个等离子体脉冲示例，展示等离子体压强的变化。最右：我们展示调整控制指令会改变等离子体性能，产生不同的等离子体脉冲。

随着我们在聚变研究界合作网络的不断扩大，我们将能够利用过往托卡马克数据和高保真模拟来验证和校准 TORAX。这些信息将为模拟精度提供信心，并帮助我们在 SPARC 开始运行后迅速适应。

## 开发用于实时控制的 AI「飞行员」

在[我们之前的工作](https://deepmind.google/discover/blog/accelerating-fusion-science-through-learned-plasma-control/)中，我们证明了强化学习可以控制托卡马克的磁体位形。现在，我们正在增加复杂度，同时优化托卡马克性能的更多方面，例如最大化聚变功率或管理 SPARC 的热负荷，使其能以更高性能运行，并相对装置极限留出更大裕度。

满功率运行时，SPARC 会把巨大的热量集中释放到很小的区域上，必须精心管理，以保护最靠近等离子体的固体材料。SPARC 可以采用的一种策略是用磁体沿壁面扫掠这些排出能量，如下图所示。

![一幅动画示意图，说明 SPARC 托卡马克中的热管理：左侧为装置横截面，蓝色圆圈标出下偏滤器区域；放大的插图展示偏滤器瓦片的排布；右侧的 3D CAD 渲染图展示一列蓝色瓦片上的热力图，红橙色斑点上下移动，演示对等离子体排出物的磁体扫掠。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/fusion-energy-plasma-changes.gif)

左：SPARC 内部右侧所描绘的面向等离子体材料的位置。右：当等离子体位形变化时，能量沉积到面向等离子体材料上的速率的三维动画（不代表 SPARC 上的实际脉冲）。图像使用 HEAT 渲染（<https://github.com/plasmapotential/HEAT)>，由 CFS 的 Tom Looby 提供。

在合作的初始阶段，我们正在研究强化学习智能体如何学会动态控制等离子体，以有效分配这些热量。未来，AI 可能学会比工程师所能设计的任何方案都更复杂的自适应策略，尤其是在平衡多重约束与目标时。我们还可以利用强化学习针对特定脉冲快速调优传统控制算法。脉冲优化与最优控制的结合，可以推动 SPARC 更快、更远地实现其历史性目标。

## 让 AI 与聚变携手，共建更清洁的未来

在研究之外，[Google 也投资了 CFS](https://blog.google/outreach-initiatives/sustainability/our-latest-bet-on-a-fusion-powered-future/)，支持他们在有前景的科学和工程突破上的工作，推动其技术走向商业化。

展望未来，我们的愿景不止于优化 SPARC 的运行。我们正在奠定基础，让 AI 成为未来聚变发电厂核心中一个智能、自适应的系统。这只是我们共同旅程的开始，我们希望在达成新的里程碑时分享更多合作细节。

通过汇聚 AI 与聚变的革命性潜力，我们正在构建一个更清洁、更可持续的能源未来。

**进一步了解我们的工作**

[进一步了解 TORAX](https://torax.readthedocs.io/en/v1.1.1/)[下载 TORAX 代码](https://github.com/google-deepmind/torax)[阅读 CFS 博客](https://blog.cfs.energy/with-ai-alliance-google-deepmind-and-cfs-take-fusion-to-the-next-level/)

**致谢**

这项工作是 Google DeepMind 与 Commonwealth Fusion Systems 的合作成果。

Google DeepMind 贡献者：David Pfau、Sarah Bechtle、Sebastian Bodenstein、Jonathan Citrin、Ian Davies、Bart De Vylder、Craig Donner、Tom Eccles、Federico Felici、Anushan Fernando、Ian Goodfellow、Philippe Hamel、Andrea Huber、Tyler Jackson、Amy Nommeots-Nomm、Tamara Norman、Uchechi Okereke、Francesca Pietra、Akhil Raju 和 Brendan Tracey。

Commonwealth Fusion Systems 贡献者：Devon Battaglia、Tom Body、Dan Boyer、Alex Creely、Jaydeep Deshpande、Christoph Hasse、Peter Kaloyannis、Wil Koch、Tom Looby、Matthew Reinke、Josh Sulkin、Anna Teplukhina、Misha Veldhoen、Josiah Wai 和 Chris Woodall。

我们还要感谢 Pushmeet Kohli 和 Bob Mumgaard 的支持。

*致谢来源：SPARC 设施图片、SPARC 渲染图以及偏滤器瓦片的 CAD 渲染图版权归 2025 年 Commonwealth Fusion Systems 所有。*
