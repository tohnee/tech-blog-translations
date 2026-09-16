---
title: "AMD 能攻破 CUDA 护城河吗？AMD Advancing AI 2026"
title_en: "Can AMD break the CUDA Moat? AMD Advancing AI 2026"
subtitle: "面向 OpenAI 的最高 105% 股权返利折扣、智能体化 kernel 生成、软件质量改善、内部开发集群不稳定、Helios MI455X 量产爬坡地狱"
date: 2026-07-25
source: https://newsletter.semianalysis.com/p/can-amd-break-the-cuda-moat-amd-advancing
crawled: 2026-09-15
authors: ["Bryan Shan", "Daniel Nishball", "Myron Xie", "Wega Chu", "Ivan Chiam", "Cam Quilici", "Cheang Kang Wen", "Kimbo Chen", "Gerald Wong", "Zane Fong", "Jordan Nanos", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# AMD 能攻破 CUDA 护城河吗？AMD Advancing AI 2026

> 原文：[Can AMD break the CUDA Moat? AMD Advancing AI 2026](https://newsletter.semianalysis.com/p/can-amd-break-the-cuda-moat-amd-advancing) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**面向 OpenAI 的最高 105% 股权返利折扣、智能体化 kernel 生成、软件质量改善、内部开发集群不稳定、Helios MI455X 量产爬坡地狱**

[当我们发布第一篇 AMD 软件文章时](https://newsletter.semianalysis.com/p/mi300x-vs-h100-vs-h200-benchmark-part-1-training)，我们认为 AMD 在 AI 加速器上追平 Nvidia 的几率为 0%。当时软件一团糟，进展乏善可陈，而且连续好几个月我们都是头号 bug 提交者，AMD 有数十名工程师在分诊我们的 bug 报告。

[六个月后，在 AMD 2.0 一文中，我们采取了与市场共识相反的立场，将其成功几率从 0% 上调到一个有意义得多的水平](https://newsletter.semianalysis.com/p/amd-2-0-new-sense-of-urgency-mi450x-chance-to-beat-nvidia-nvidias-new-moat)。我们发布这一观点时，市场对 AMD 的情绪正处谷底，多数市场参与者认为我们对 AMD 过于乐观。

[那一判断基于我们的观察：AMD 拥有能够推动变革的领导层，而非受困于委员会式的领导](https://newsletter.semianalysis.com/p/mi300x-vs-h100-vs-h200-benchmark-part-1-training)。[Lisa 很快就与我们通了电话，此后落实了我们的许多建议](https://newsletter.semianalysis.com/p/amd-2-0-new-sense-of-urgency-mi450x-chance-to-beat-nvidia-nvidias-new-moat)。我们看到一家终于认识到软件重要性、有了紧迫感的 AMD——目的地虽仍遥远，但方向是对的。自那以后，这一信号只会越来越强。

**基于我们今年在 AMD 软件栈上的实际使用经验，我们再次更新观点：从"非零的百分比几率"上调为"相当大的成功机会"——前提是 AMD 解决我们下文详述的两大风险。需要强调的是，AMD 获得市场份额并不意味着 Nvidia 会表现不佳。蛋糕正在快速做大，对所有参与者都是如此，Nvidia 的营收仍将大幅增长。AMD 在软件层面对 Nvidia 构成潜在竞争；如果 Jensen 想让 Nvidia 行动更快、捍卫领先地位，就需要砍掉官僚作风、压扁那些连最简单任务都要经过多层内部相关方审批的流程。**

Anthropic 已公开宣布将部署 2GW 的 AMD 芯片，Lisa Su 及其团队正在拥抱一种以智能体（agentic）为导向的工程文化。Anthropic 计算负责人 Tom Brown 举例说明：**他周末用 Claude 的 "/goal" 在 AMD 硬件上把内部 Claude 推理栈跑了起来**。我们认为，由于 AMD 的编译器和大多数 kernel 都已开源，除**后文将讨论的一大风险**外，它们在智能体时代处于更有利的位置。[三个月前，我们的 Accelerator 模型就指出 Anthropic 将成为 AMD 客户](https://geohot.github.io/blog/jekyll/update/2025/03/24/tragic-intel.html)。[一周前我们也在社交媒体上提示了这一点](https://x.com/dylan522p/status/1871287937268383867?s=46)。

[2023 年，微软在 MI300X 之后弃用了 AMD，原因是不靠谱的三星（Samsung）2023 年 HBM 内存](https://semianalysis.com/accelerator-hbm-model/)以及糟糕的软件质量，随后相继跳过了 MI325X 和 MI355X。如今微软态度 180 度转弯，宣布将部署 MI455X Helios。我们认为 OpenAI 将是 Azure MI455X 机柜的主要终端客户。与 Nvidia-Groq 交易有几分相似，AMD 宣布与 Cerebras 达成合作，用后者做 PD 分离（disagg），实现超快交互式推理。

AMD 需要防范两大风险：

1. 供应链调研以及基于第一性原理的工程分析表明，AMD 第一代 AI 机柜级系统 Helios 正经历缓慢的机柜量产爬坡，因为它没有采用无缆（cableless）托盘设计，而 Rubin Oberon 机柜现已转向该设计。此外，由于 AMD 的 SerDes 设计较弱，其背板多达 85% 的链路需要重定时（retime），每个机柜需要超过 550 颗 Broadcom 以太网重定时器（retimer）。而且，在机柜量产爬坡地狱中，它还正遭遇背板可靠性难题。

2. **AMD 内部多数工程师的首要抱怨是：持续缺乏供内部软件开发团队使用的稳定 GPU 集群，也缺乏供自动化测试 CI 使用的稳定 GPU 集群**。这正在拖慢 AMD 的进步速度，并且**阻碍 AMD 收获 AI 编程智能体的潜在红利**，因为每个 AI 智能体本身也需要 GPU，还需要一个带工具调用的测试闭环。我们将在下文的建议部分详细展开。

如果 AMD 能克服这些挑战，我们坚信 AMD 将处于有利位置、有能力取得佳绩并夺取市场份额。近期的股票期权结构也将助一臂之力：通过一些巧妙的金融工程，**AMD 向 Meta 和 OpenAI 提供接近 105% 的股权返利折扣**。全额返利的触发条件是 AMD 股价达到 $600 的最终档位，且 OpenAI/Meta 采购足够多的算力。**Helios 的每 TCO 性能如此出色，叠加这一结构后，每百万 token 的成本几乎为负！** AMD 等于是在把 Helios 机柜白送给一家名为 OpenAI 的旧金山非营利组织，还要额外倒贴 5%。

在本文第一部分，我们将深度解析 Helios 架构以及 MI455X（gfx1250）指令集——它是 Hopper SM90 ISA 的克隆。我们还将讨论 Helios 的横向扩展（scale-out）与纵向扩展（scale-up）网络架构。第二部分将更深入软件栈细节。第三部分聚焦拥有和运营 Helios 机柜的经济学，并拆解 OpenAI/Anthropic/Meta 股权返利折扣的经济账，以及这一结构如何影响总拥有成本（TCO）。

我们是 MI300X、MI325X、MI355X 上 ROCm 软件的每日用户，而且每个季度都稳居头号 bug 报告者！有几位 10 倍工程师（10x engineer）值得点名致谢——他们长期 997 地改进 AMD 软件，并快速分诊我们的 bug 报告。特别感谢 Hongxia、Chun Fang、HaiShaw、Thomas Wang、Andy Luo、Seungrok、Bill He、Teresa Shan、Parth、Duyi Wang、Gilbert 等许多同仁。AMD 最优秀的 10 倍工程师大多在上海。AMD 的 MoRI 集合通信与 UMBP KVCache 卸载团队、AMD 分离式应用前置部署工程团队，以及其他懂得如何做第一性原理推理工程的 AMD 团队，主要都在上海。**ROCm 软件栈中许多最重要的部分是在中国打造的。**

# 给 Lisa Su、Mark Papermaster、Sharon Zhou、Anush Elangovan 和 Vamsi Boppana 的建议

过去一年，自动化测试在改善软件质量方面取得了不错进展，但进度不够激进，而且在为自动化测试 CI 和内部软件开发团队提供足够 GPU 集群这件事上，仍然缺乏紧迫感。总是给得太少、来得太迟。

每隔几个月与各位（Vamsi、Anush）会面、偶尔与 Lisa 会面时，我们总是强调 CI 可以做得更好；我们也确实能举出 CI 朝正确方向推进的具体例子，但整体战略需要更激进地加码。例如，Kubernetes 推理 Pollara NIC 的 CI 与 Nvidia ConnectX Nightly CI 的对等率仍为 0%。Kubernetes 是全球大多数推理部署所依赖的层。问题不在于 AMD 工程师不*想*添加支持，而是内部 CI 容量投入不足拖了后腿。由于集群问题，AMD 原定在 Advancing AI 2026 之前在该领域实现对等的 ETA（预计完成时间）已经落空。

在 vLLM 方面，由于本周 AMD 集群基础设施的稳定性问题，vLLM 门禁（gating）自动化测试进度大幅倒退。过去几周，AMD 的硬核工程师在 vLLM 门禁上进展良好，目标是在 Advancing AI 2026 前实现门禁测试与 CUDA 至少 90% 的对等；但随后 AMD 管理层开始从内部 vLLM 团队抽走集群、部署到别处——原因在于 AMD 内部产能吃紧，且过度依赖临时托底（backstop）集群。

门禁/阻断（gating/blocking）测试意味着测试质量最高，因为测试不通过，PR 就无法合并，从而阻止 bug 被合入。虽然 AMD 管理层可能拿非门禁通过率来搪塞非技术人员，但门禁对等率和门禁通过率才是真正重要的指标。

我们希望 AMD 管理层能重新排序优先级，给内部 vLLM 团队稳定的集群，并更新其容量规划理念以防止此类问题重演，从而让 AMD 内部硬核 vLLM 工程师专注于将门禁测试对 CUDA vLLM 的对等率做到 90% 以上，并拥有与 AMD 内部 SGLang 团队同等运作速度所需的工具。

多数 AMD 工程师的首要抱怨是：管理层仍需转变观念，提供稳定的 CI 集群，而不是动不动就要把集群从一家 CSP 迁移到另一家 CSP。

此外，内部可用于开发的 GPU 持续短缺。单节点聚合推理方面，内部 GPU 尚够周转。但在分布式多节点推理优化（wideEP 与 PD 分离）的时代，GPU 远远不够。即便本月新增 2,000 颗 MI355X 上线、今年晚些时候再新增 6,000 颗 MI325X/MI355X 上线，总容量仍然不足，与 Nvidia 用于内部开发的稳定长期集群相比，仍少一个数量级以上。GPU 节点短缺这个问题还因智能体编程的兴起而愈发严重。以前，每位人类工程师只需要几个节点来做分布式推理（DI）软件研发。而现在有了智能体编程，每个智能体都需要 GPU 来测试代码，每个人可以同时运行几十个智能体，每个智能体又可以同时运行几十个子智能体。因此，[如果没有 DynoSim 这样的分布式推理模拟工具](https://developer.nvidia.com/blog/dynosim-simulating-the-pareto-frontier/)，内部 GPU 容量的缺口还会更大。

另外，[Rubin（SM107）与 Blackwell（SM100）的 ISA 非常相似](https://newsletter.semianalysis.com/p/vera-rubin-nvl72-vs-gb200-nvl72-inference)，而 MI455（gfx1250）与 MI355（gfx950）的 ISA 则完全不同，代码路径和 kernel 也完全不同，需要同时在 gfx950 和 gfx1250 上测试。这是另一个会持续挤压容量的因素。原本的宏大目标是在 Advancing AI 2026 前让 MI455X 上的开源 vLLM、SGLang nightly 自动化 CI 就绪，但这一时间表已经落空。我们听说新时间表已推迟到 2026 年 10 月，但他们仍在努力将其左移回 2026 年 8/9 月。

我们认为，内部软件开发 GPU 集群与自动化测试 CI 集群爬坡缓慢，是拖慢软件质量与性能改进速度的主要风险之一，希望 AMD 管理层重新审视其今后的容量规划战略。

# 第一部分：AMD MI455 芯片与 Helios 机柜

![](https://substack-post-media.s3.amazonaws.com/public/images/5e6e9663-f4ef-4392-9cf8-c7e50a770459_1920x1069.jpeg)
*来源：AMD*

AMD 在芯片工程上再次交出杰作。MI455X 是目前从晶圆厂产出的、硅片层面最先进的芯片。AMD 是第一家出货 2nm 数据中心芯片的公司——MI455 的计算 tile 与 Venice CPU 都是 N2 的首批采用者。所有竞争性加速器平台都还在 N3 上。

在封装内集成度方面，AMD 也持续领先。MI455 封装是已出货的最大的 CoWoS-L 模块，达 5.5 倍光罩尺寸。AMD 仍是唯一采用台积电（TSMC）SoIC-X 混合键合的公司，这让 AMD 的硅片占位不仅能在 x、y 方向扩展，还能在 z 方向扩展。这一切叠加起来，使 MI455 封装内逻辑硅总面积达到 3,470mm2，是迄今单封装内出货硅面积最多的，遥遥领先。

封装布局大量借鉴 MI355X。8 颗 N2 "XCD" 混合键合在 2 颗光罩尺寸的基础裸片（base die）之上，后者包含 SRAM、HBM 控制器以及计算互连 fabric（让各 XCD 之间互相通信）。

MI455X 与 MI300 系列的一大差异，是新增了两颗独立 I/O 裸片，容纳所有封装外通信的 PHY。虽然下方的版图示意显示一颗 I/O 裸片用于 UALoE 纵向扩展 fabric、另一颗用于连接主机 CPU 和横向扩展 fabric 的 NIC，但实际上两颗 I/O 裸片完全相同。这是灵活 I/O 的巧妙实现：每颗 I/O 裸片支持 72 条 lane，可兼容不同协议、不同线速，包括 212G UALoE、64G Infinity Fabric、PCIe Gen 6、128G UALink、xGMI4。由于其中不少协议都以某种形式贡献给了开放的 UALink 联盟，这套 I/O 从设计之初就考虑了与基于 UALink 的互连方案良好集成。

![](https://substack-post-media.s3.amazonaws.com/public/images/a1d6ed6e-5755-4125-af00-a1aa104b8174_1200x675.jpeg)
*来源：AMD*

正是这种"堆硅"（silicon spam）让 AMD 得以交付业界领先的峰值理论稠密 FLOPS：MI455X 的 FP8 算力达 20PF，而 Rubin 为 17.5 FP8。不过，撇开绝对数字不谈，考虑到硅用量多出那么多，这些性能优势相对 Rubin 其实相当有限。这源于 AMD 相对 Nvidia 在 GPU 微架构设计上的差距，我们将在下文讨论。**目前，[MI455X 缺少 Rubin SM107 拥有的 3 bit LUT 张量核心](https://newsletter.semianalysis.com/p/vera-rubin-nvl72-vs-gb200-nvl72-inference)。3 bit LUT 张量核心在降低相对 HBM 带宽需求方面有潜在优势。**可以说，AMD 正是被逼着在硅片上激进投入来弥补这一短板，更别提它在软件和系统设计上的相对弱势了——尽管其软件正在变好。[又或者，AMD 的产品营销团队可以再找些门道，把宣传的性能数字榨得更好看些。](https://newsletter.semianalysis.com/i/180102610/why-anthropic-is-betting-on-tpus)

![](https://substack-post-media.s3.amazonaws.com/public/images/410a2a3c-5439-4c82-a160-4369f9ada170_2072x1185.jpeg)
*来源：AMD、Nvidia*

巨大的封装面积也让 AMD 得以塞入 12 组 HBM4 堆叠，单封装总容量 432GB。相比 Nvidia 和 Google 只配 8 组堆叠、单封装合计 288GB，这再次领先业界。每颗基础裸片如今更接近光罩尺寸，面向 HBM 的边长为 32mm，以便每边挤下 3 颗 HBM cube；相比之下，MI300X 的 AID 每边只有 29mm，不够放 3 颗 cube。

连同推出 Rubin 的 Nvidia 一起，AMD 是今年仅有的两家出货 HBM4 的公司之一。12 组堆叠也让 MI455 在内存带宽上胜出：每芯片 23.3 TB/s，对应 HBM4 引脚速率 7.6Gbps。这较去年 Advancing AI 上公布的 19.6TB/s 略有上调。尽管总线宽度比 Rubin 宽 50%，总带宽却只是勉强超过 Rubin 的 22TB/s。

原因在于 Nvidia 去年激进地将 HBM4 目标引脚速率提高到远超 JEDEC 原始 HBM4 规范的水平。这一改动正是为了弥补相对 AMD MI455X 的内存带宽劣势。按 Nvidia 宣传的 Rubin 22TB/s 计算，引脚速率为 10.7Gbps：比 MI455 的 HBM4 快 40%，这意味着 NVIDIA 将不得不使用比 AMD 品质高得多的颗粒 bin。

正如我们此前提到并在 [newsletter](https://newsletter.semianalysis.com/i/188150420/rubin) 和 [Accelerator Model](https://semianalysis.com/accelerator-hbm-model/) 中详细分析的，这一变化让内存供应商很难跟上。内存厂商不得不重构其 HBM4 以满足 Nvidia 的目标规格。这也推迟了 Rubin 的上游产出，但截至目前这些问题已最终解决。事实证明，这对 Nvidia 是一次值得的博弈：他们得以补上 Rubin 的一大短板，而且尽管有延迟，Vera Rubin 仍将早于 MI455 Helios 率先大规模交付 token。后文详述。

# 主动式 LSI

在表面之下，我们认为 MI455 还是已知第一款搭载主动式局部硅互连（active Local Silicon Interconnect，"LSI"）的芯片——LSI 即 CoWoS-L 封装中连接各小芯片（chiplet）的桥接结构。在 CoWoS-L 短暂的历史中，这些桥一直是无源的，只包含布线和电容。主动式 LSI 带有真正的电路。[在 TSMC 于 ISSCC 2026 上的 aLSI 演讲中，TSMC 展示了带低功耗中继器电路的主动桥，可在信道中段再生信号。](https://newsletter.semianalysis.com/p/isscc-2026-nvidia-and-broadcom-cpo?utm_source=publication-search)好处在于，由于桥现在分担了维持信号完整性的负担，顶层裸片上的 PHY 可以显著缩小，能耗代价几乎可以忽略，从而为计算和内存收复先进制程硅面积与边缘走线资源（shoreline）。这等于暴露了该特性已在 MI455 上出货——MI455 实际上就是"测试载具"。TSMC 展示的正是 MI455 的 interposer：两颗基础裸片、12 组 HBM4 堆叠、两颗 I/O 裸片。

![](https://substack-post-media.s3.amazonaws.com/public/images/458dc37b-725d-4269-9958-1bef95f177fc_1456x819.jpeg)
*来源：TSMC 主动式 LSI 裸片图与功耗拆解，ISSCC 2026*
![](https://substack-post-media.s3.amazonaws.com/public/images/9733428b-7090-4796-abdf-989d692209ac_1282x852.png)
*来源：SemiAnalysis*

## MI455X 网络

在网络方面，MI455X 标志着 AMD GPU 首次在机柜级域内采用交换式（switched）纵向扩展。相比 MI300X 到 MI355X 一直使用的 8 GPU 点对点 mesh，这是巨大升级。

AMD 的 Helios 机柜通过 12 颗 102.4T Tomahawk 6 交换芯片组成单层全互联（all-to-all）网络，连接 72 颗 MI455X GPU。每颗 GPU 有 72 条 200G UALoE lane 用于纵向扩展 fabric，单 GPU 纵向扩展总带宽达 1.8 TB/s（单向）。每颗交换芯片使用其 512 条 200G lane 中的 432 条——这种过度配置是因为 AMD 采用 Broadcom 的商用（merchant）TH6 交换芯片，而非 Nvidia 那种自研协同设计的专用交换芯片。横向扩展则同步从 400G Pollara 升级到 800G Vulcano，两块 NIC 为每颗 GPU 提供 1.6 Tbit/s，并可为每颗 GPU 增配第三块 NIC。预计 MI500 会把纵向扩展域扩展到跨三个机柜的 256 颗 GPU，届时铜缆很可能让位于共封装铜互连或共封装/近封装光学。

![](https://substack-post-media.s3.amazonaws.com/public/images/00ffbb4a-b0b9-4b4c-aaef-919425473a2a_1810x962.png)
*来源：SemiAnalysis*

## Meta Recsys 基础设施战略：一个正在损害 AMD 在 Meta 成算的奇怪选择

*2026 年 8 月 3 日编辑注：根据新信息，我们已更新 Meta 定制 MI450X SKU 的配置*

[简而言之，AMD 努力交付了在主要规格上击败或追平 Vera Rubin 的芯片和系统。奇怪的是，Meta——AMD 最大的 GPU 客户之一——却决定不充分利用 AMD 的这些创新](https://newsletter.semianalysis.com/p/metas-infrastructure-team-needs-a)。Meta 对 MI455 的订单大多是定制版，是完整 MI455X 的缩水版。这款[Meta 定制 MI455X 是完整 MI450X 的削减版：I/O 减半，8 颗计算裸片/XCD 只保留 6 颗](https://semianalysis.com/institutional/hbm-capacity-downgrades-amd-meta-version-and-increasing-2027-amd-estimates-trn4-tpu-whalefish-floorplan/)。HBM4 也从标准 SKU 的 12-Hi 降为 8-Hi。

只有一颗而非两颗 I/O 裸片，可用 I/O lane 就只有 72 条而非 144 条。lane 预算缩减后，纵向扩展带宽也必须下调。我们认为是 36 条 lane 用于纵向扩展而非完整的 72 条；这意味着 Meta 版本每个机柜只需要一半数量的 Tomahawk 6 交换芯片。剩下 36 条 lane 留给系统和横向扩展：16 条 128G UAL 连接 NIC、实现每 GPU 1.6T 横向扩展，另有 16 条 Infinity Fabric 连接主机 CPU。

这些选择的结果是，Meta 版 MI450X 的网络能力大打折扣：单芯片纵向扩展带宽只有一半，仅 900GB/s，而 Rubin 为 1,800GB/s。相对常规版本还有 25% 的算力削减。虽然算力削减不算大，但省掉 2 颗计算 tile 所节省的成本在整个系统语境下微乎其微，因此不禁让人怀疑这个选择是否值得。

这一芯片配置面向推荐系统（Recsys）工作负载，是推荐系统基础设施团队的决定。但这个决定做出时，TBD Lab 尚未成立、也来不及发声。鉴于这款芯片和系统相对 Rubin 在网络和算力上的明显短板，TBD 对这套系统毫无兴趣，对外部客户也没有吸引力。

[正如我们在上一篇 Meta 基础设施战略文章中明确指出的，选择缩水定制版 MI455 将会摧毁 AMD 在 Meta 的出货量，因为一旦半血 MI455 设计被选定，TBD 会明显更青睐 Rubin。AMD 需要介入，拿出](https://newsletter.semianalysis.com/i/207968269/upcoming-amd-mi450x-gun-in-mouth-decision)大人的担当，直接与 TBD 的团队合作，确保他们拿到的是正常版 MI455，而不是这个对 LLM 训练和推理都很糟糕的残废 Meta 定制版。正常版 MI455 足以与 Nvidia 的 Vera Rubin 竞争。

不过我们确实认为还有希望：在我们的文章发表后，Mark Zuckerberg 已开始快速探索其基础设施战略组织文化的变革。

![](https://substack-post-media.s3.amazonaws.com/public/images/a860ee73-1ce2-4c6a-b2a8-195b8feded86_1710x1323.png)
*来源：AMD、SemiAnalysis*

## Helios 机柜解读回顾

[自 AMD 在 Advancing AI 2025 上发布 Helios 架构以来已过去一年，期间发生了很多事。](https://newsletter.semianalysis.com/p/amd-advancing-ai-mi350x-and-mi400-ualoe72-mi500-ual256)让我们回顾 Helios 架构，梳理过去一年出现的一些变化和细节。

### 机柜正视图

![](https://substack-post-media.s3.amazonaws.com/public/images/9e399c1f-c69e-410e-9ddb-dda86b300d6b_2120x1898.png)
*来源：SemiAnalysis*

Helios 机柜包含 18 个计算托盘和 6 个位于计算托盘中部的纵向扩展交换托盘。每个计算托盘容纳 4 颗 MI455X GPU 和 1 颗 Venice CPU，合计 72 颗 GPU 和 18 颗 CPU。每个纵向扩展交换托盘容纳 2 颗 Broadcom 102.4T Tomahawk 6 交换芯片，合计 12 颗交换 ASIC。对于 Meta 版 MI455x，机柜内将有 6 台 51.2T Minipack 以太网交换机，电源托架则放在单独的 IT 机柜中。

### 计算托盘布局

![](https://substack-post-media.s3.amazonaws.com/public/images/4e0defa7-6a54-440c-a3ef-6db331e42f7b_1926x1666.png)
*来源：SemiAnalysis*

自 Advancing AI 2025 以来，计算托盘设计基本没有大改。每颗 MI455X GPU 安装在 EAM 模块中，通过背板连接器接入纵向扩展链路，并通过飞线（flyover cable）连接 Venice CPU 和 Vulcano NIC。值得注意的是，直接挂在 EAM 上的 LPDDR5x 不见了——下文详述。Venice CPU 有自己的模块板，带 16 条 RDIMM 插槽和 5 个 NVMe SSD 插槽。设计是模块化的，但模块间使用飞线连接可能在生产中带来挑战。

### 部分协同设计

AMD 为其机柜级方案展示了丰富的产品组合，包括 MI455x GPU、Venice CPU、Pensando Vulcano 800G NIC 和 Pensando Salina DPU。然而，真正决定机柜级纵向扩展性能的纵向扩展交换芯片却缺席了。与 Nvidia 不同，AMD 只能依赖合作伙伴提供现成的商用纵向扩展交换芯片。这至少在理论上让客户可用的纵向扩展交换生态更广。但这也使其路线图受制于交换合作伙伴的执行。由于 Broadcom 是唯一出货带 200G SerDes 的 100T 级交换芯片的商用供应商，Broadcom 成了 AMD 在交换芯片上的唯一选择。这也使厂商之间的物流和责任划分复杂化，需要反复沟通、协同解决问题。由于缺少纵向扩展交换芯片产品，AMD 无法对完整机柜方案实现极致协同设计（extreme co-design）。

![](https://substack-post-media.s3.amazonaws.com/public/images/5391679d-c5c7-48a6-83d1-3033433180c0_2253x1261.png)
*来源：AMD*

### 内存降配

一个显著的缺失是：每颗加速器不再有直挂的 LPDDR。此前的路线图曾为每颗 MI455X 在 EAM 模块上配置最高 1TB LPDDR 作为二级内存，但现在已消失。[我们认为这是内存供应紧张的又一后果](https://newsletter.semianalysis.com/p/memory-mania-how-a-once-in-four-decades?utm_source=publication-search)。

### 背板重定时

Helios 的另一特点是在纵向扩展交换侧加入以太网重定时器。这与 Nvidia 完全无源的 Oberon 背板不同。AMD 的 200G SerDes 在 MI455X 芯片与纵向扩展 Tomahawk 6 交换芯片之间的铜路径上受插损困扰。这可能是其灵活 I/O 野心的代价，也可能单纯是 SerDes 品质不足导致背板信号性能不达标。在 Meta 的 MI455X 部署中，约 85% 的纵向扩展链路将被重定时。以太网重定时器由 Broadcom 提供，放置在纵向扩展交换托盘中。这并不理想：重定时器会给整个系统增加额外成本和功耗预算，而且使服务器组装复杂化——点亮一个机柜时逐一调校所有重定时链路将是非常繁琐的工作。

### 可制造性与效率挑战

MI455X Helios 设计是 AMD 对 Nvidia GB200/GB300 Oberon 架构的回应。AMD 在 Helios 上大量参照了 Nvidia 的架构要点。该设计虽然实现了高密度单机柜纵向扩展，但 AMD 也照搬了让 Nvidia 吃尽苦头的飞线设计。[我们在 Vera Rubin 架构深度解析一文中讨论过飞线相关的制造挑战。](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution)GB200/GB300 计算托盘和交换托盘上飞线的种种困难，促使 Nvidia 在 Vera Rubin NVL72 上转向无缆设计。而到这一设计公布时，AMD 已经来不及在 MI455x Helios 上贯彻同样的设计理念了。

在计算托盘内，Molex 的 Genesis 线缆承载 MI455X 与 Pensando Vulcano NIC 之间的 128G UALink。每个计算托盘最多有 12 根 Genesis 线缆，与液冷管和电源线一起挤在 1U 空间里。在纵向扩展交换侧，背板连接器与 TH6 交换芯片之间采用飞线。1,728 根线缆将从背板连接器布线至每颗 TH6 ASIC 周围的 16 个端口（每托盘 32 个端口）。所有线缆都成为组装过程中的潜在故障点，并将拉低制造效率。

### 计算托盘拓扑

Helios 机柜的 18 个计算托盘中，每个容纳 4 个 MI455X EAM，每个 EAM 支持 36 条 UALoE 链路，每条链路又由 2 条 200G 以太网 lane 构成。72 条 200G 以太网 lane 合计为每颗 GPU 提供 14.4Tbit/s（单向）的纵向扩展总带宽。MI455X 在封装南北两侧各有一块基于 N3P 的 I/O 模块——一块承载用于纵向扩展网络的 UALoE 链路，另一块实现连接 CPU 的 Infinity Fabric 以及连接 NIC 的 UALink128/PCIe Gen7。

![](https://substack-post-media.s3.amazonaws.com/public/images/13ba819b-e3fc-4934-a506-49a15e1b4a14_1178x658.png)
*来源：AMD*

### 纵向扩展拓扑

![](https://substack-post-media.s3.amazonaws.com/public/images/f531ace5-a92f-462e-ae0d-1f93f8b091ec_1810x962.png)
*来源：SemiAnalysis、AMD*

这些 UALoE 链路的另一端，是分布在 6 个交换托盘（每托盘 2 颗交换 ASIC）中的 12 颗 Broadcom Tomahawk 6 以太网交换芯片。UALink over Ethernet（UALoE）在协议栈中对应的层次相当于 Nvidia 的 NVLink。每颗 Tomahawk 6 交换 ASIC 本可支持 102.4Tbit/s（单向）聚合带宽，由 512 条单向 200Gbit/s lane 构成。但实际只启用其中 432 条 200G lane，即每颗交换 ASIC 到机柜内 72 颗 GPU 的单向总带宽为 86.4Tbit/s。能在 72 颗 GPU 间整除的交换聚合带宽才是理想的——例如 115.2Tbit/s——但 AMD 用的是当今唯一可买到的交换芯片。聚合带宽 115.2T 和 57.6T 的 UALink 交换芯片已在路上，但还不够近，无法作为这套架构的锚点。相比之下，Nvidia 专门为 72 GPU 机柜的需求设计了 28.8T NVSwitch，带宽在 72 颗 GPU 间整除、每颗单向 400Gbit/s，完全没有带宽浪费。每个交换托盘还包含一颗小型主机端 x86 CPU。

![](https://substack-post-media.s3.amazonaws.com/public/images/255daf84-8480-4765-8725-6a8aa35718de_1486x833.png)
*来源：AMD*

AMD 采用的纵向扩展拓扑，读者们现在应该已经熟悉。在这个扁平的单层网络中，每颗 GPU 以每 lane 单向 200Gbit/s、共 6 条 lane 连接到每颗交换芯片，即向 12 颗交换 ASIC 中的每一颗提供单向 1.2Tbit/s。每颗交换 ASIC 则连接到机柜内所有 GPU。

![](https://substack-post-media.s3.amazonaws.com/public/images/973d34b4-ca29-4519-b48a-b3862d4fa498_2091x782.png)
*来源：SemiAnalysis*

纵向扩展交换到 GPU 的链路采用铜缆背板实现。对每颗 GPU 而言，72 条 200G lane 中的每一条都由两对铜信道差分对（DP）承载，一发一收。这相当于每颗 GPU 144 对铜缆 DP，整个机柜共 10,368 对铜缆差分对。每颗 GPU 还需要一个 144DP 公头和一个 144DP 母头连接器，用于背板线缆与计算托盘本体的接口。交换侧，每个交换托盘使用四组连接器，每组容纳四个 108 DP 连接器——即每组共 432 DP。

飞线用于将交换 ASIC 连接到计算托盘背面的连接器。飞线比 PCB 走线信号完整性更好，缺点是往往限制可维护性和散热效率，还额外增加制造难度。Nvidia 在飞线与 PCB 之间反复摇摆——最初打算用飞线，后来为了更好的可维护性和风量改用 PCB 走线。

![](https://substack-post-media.s3.amazonaws.com/public/images/dfd24de4-c3ee-43bb-834a-f40511be2055_1666x1083.png)
*来源：AMD*

每机柜的背板与计算托盘线缆总价值将达 $68,928，其中 $44,352 来自背板，其余 $24,576 归于飞线。

![](https://substack-post-media.s3.amazonaws.com/public/images/9f77defb-555f-468a-a551-6c81636f5a91_1512x889.png)
*来源：SemiAnalysis AI 网络模型*

由于只有 6 个交换托盘，UALoE 信号的传输距离比 GB300 NVL72 中的 NVLink 更短——后者使用 9 个交换托盘。此外，AMD 将 Helios 机柜设计为上半部 9 个计算托盘、下半部 9 个计算托盘，使信号在上下两个方向的传输距离相等。

![](https://substack-post-media.s3.amazonaws.com/public/images/68e282fb-1721-441a-87d5-3667bc99f73e_1237x780.png)
*来源：SemiAnalysis*

### 横向扩展网络

横向扩展方面，每颗 MI455X 最多可连接 3 块 AMD Pensando Vulcano 800 AI NIC，提供 2.4 Tbit/s 横向扩展带宽；每块 NIC 通过 x8 UALink128 接口连接，提供 256 GB/s 的双向 GPU-to-NIC 带宽。前端网络由单独的 Pensando Salina 400 DPU 处理。

![](https://substack-post-media.s3.amazonaws.com/public/images/571650aa-a0df-4965-84d1-4b15f5017c11_1791x972.png)
*来源：SemiAnalysis AI 网络模型*

我们预计主流部署配置为每 GPU 2 块 Vulcano NIC，提供 1.6 Tbit/s 横向扩展带宽。

在机柜之外，Vulcano 支持多平面 leaf-spine 拓扑，每个平面内无阻塞，这如今已是常见实现。关于多平面架构为何对当今 AI 集群至关重要（它能在两层网络上容纳更多 GPU），我们已写过大量文章。我们在 Vera Rubin 一文中[在此](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution)更详细阐述了多平面 fabric 背后的直觉与优势。

![](https://substack-post-media.s3.amazonaws.com/public/images/283c379e-2a96-4365-8398-572bd48f68ed_1994x757.png)
*来源：SemiAnalysis AI 网络模型*
![](https://substack-post-media.s3.amazonaws.com/public/images/3b73a033-54ba-4b63-8c83-66d9c1d3d3ee_1582x822.png)
*来源：SemiAnalysis AI 网络模型*

在一个 131k 颗 MI455X 的 8 平面集群中，每块 800G Vulcano NIC 拆分为 4 条 200G 链路；由于每颗 GPU 挂 2 块 NIC，每颗 GPU 在 8 个独立平面中各有一条连接。每个平面有 512 台 leaf 和 256 台 spine 交换机，整个集群共 6,144 颗 TH6 交换芯片。该配置下，NIC 侧需要 2 个 800G DR4 模块，每颗 GPU 需要 3 个 1.6T DR8 模块——2 个用于 leaf 侧上行和下行，1 个用于 spine 侧。我们预计，八平面两层配置下每颗 MI455X GPU 的横向扩展网络物料价值约为每 GPU ~$8,000。

![](https://substack-post-media.s3.amazonaws.com/public/images/9b3f356d-4bee-4d6f-91d3-7ba2e3cc062c_1828x938.png)
*来源：SemiAnalysis AI 网络模型*

AMD 的 Pensando Vulcano 800 AI NIC 正沿着业界过去几年的共同方向前进。在《[Meta 的基础设施团队需要一场文化重置](https://newsletter.semianalysis.com/p/metas-infrastructure-team-needs-a)》一期中，我们重点分析了 AI 横向扩展网络在数据面和控制面层面面临的问题。

大型 AI 训练集群中存在三大问题：大象流（elephant flow）、低熵（low entropy）和次优的 fabric 利用率。

- **大象流（Elephant Flow）：** AI 工作负载往往包含持续时间长、流量巨大的流，可能造成网络拥塞，拉低整个训练批次的表现。

- **低熵（Low Entropy）：** 视训练任务而定，IP 流数量可能有限，只让少数几条链路拥塞，而 fabric 整体仍有大量空闲容量。

- **次优 Fabric 利用率（Suboptimal Fabric Utilization）：** 最后，作为大象流和低熵的综合效应，fabric 链路带宽利用率会出现严重偏斜，这直接决定了要让 fabric 平稳运行需要过度配置多少余量。

RDMA 流量对丢包和拥塞高度敏感，而 RoCEv2 构建于有损协议以太网和不提供恢复机制的 UDP 之上。Meta 的 DSF 通过虚拟输出队列、信元喷射（cell spraying）、信用调度（credit scheduling）和深缓冲 Jericho-AI 交换机在网络内部解决了这些问题，但代价是数据面、控制面和硬件栈复杂得多。

Vulcano 尝试解决同样的问题，但路径是通过 NIC。该 NIC 带有三大要素：智能包喷射（Intelligent Packet Spray）、路径感知拥塞控制（Path Aware Congestion Control）以及乱序包处理与有序消息交付（Out-of-order Packet Handling and In-order Message Delivery），从而把网络复杂度从 fabric 卸载到 NIC。

智能包喷射从根源上解决低熵问题。在传统 ECMP fabric 中，一条流被哈希到单一路径并停留在那里。由于 AI 流量由少数几条巨大的、同步的大象流组成，哈希冲突频发，一些路径拥塞的同时另一些路径闲置。AMD 的 AI NIC 不再把一条流钉在单一路径上，而是把同一条流的包喷射到 fabric 的可用路径上，把熵提升到逐包级别。结果是 1:1 的 fabric 利用率，以及毫秒级故障恢复——因为任何单条链路故障都无法击垮整条流。

然而，包喷射带来了一组新问题，这正是另外两大要素发挥作用的地方。其一，来自不同路径的包可能乱序到达。传统 RoCEv2 网络迫使包进行回退 N 重传（go-back-N），视方案不同（调度式 vs 非调度式 fabric）需要在 NIC 或交换机层面缓存。而在这里，NIC 原生处理乱序包到达，并在消息层面保证顺序，从而免除缓冲需求。包一落地就直接写入 GPU 显存，只有丢失的包才重传。

其二，盲目向各路径喷射包不但不能避免拥塞，反而引发拥塞。路径感知拥塞控制补上了这块短板：NIC 实时跟踪每条路径的状态，在队列堆积之前就把流量从拥塞路径上移开。这尤其针对 incast 场景——all-reduce 这类集合通信操作往往是多个发送方对应一个接收方，会在 fabric 中引发队头阻塞级联。由于决策在 NIC 层面做出、且具备逐路径可见性，速率爬升足够快，足以应对 AI 工作负载的突发特性。此外，由于包被智能地喷射到整个 fabric，尾延迟也被降到最低。

综合来看，这三大机制解决的是 Nvidia 用 ConnectX NIC 加 Spectrum-X 自适应路由所解决的同一问题。主要区别在于：AMD 采用开放的 UEC 标准和多厂商 fabric，而非垂直整合方案。

AMD 的 AI NIC 不强加传输模型，支持灵活的横向扩展组网。它支持基于交换机的包喷射（面向 fabric 已自行处理负载均衡的运营商）、基于 NIC 的包喷射（面向无智能的商用 fabric，把智能下沉到 NIC），以及基于 NIC 的源路由（面向希望从端点控制路径的运营商）。核心思想是：网络行为去适应你已有的 fabric 和你要跑的工作负载，而不是反过来。

## CDNA5 微架构

### 设计与 NVIDIA 趋同

正如 AMD 从 Nvidia 无聊的主题演讲形式中汲取灵感一样，AMD 的 CDNA 5 在很多方面大举借鉴了 Nvidia Hopper（SM 90）架构。首先，CDNA 5 把每个 wave 的线程数降到 32，与 Nvidia 每个 warp 32 线程对齐。CDNA 5 还用每 FCD（Fabric and Cache Die）一块 96 MB 大 L2 缓存，取代了 CDNA3/CDNA4 的 Infinity Cache 加小 L2 的组合。这一设计更趋近 Nvidia 的"全局内存 -> L2 缓存 -> 共享内存"内存层级。跨层级管理内存延迟一直是 AMD kernel 开发者的痛点；我们预计层级简化应能缓解这一问题。

![](https://substack-post-media.s3.amazonaws.com/public/images/730ffb0c-7d38-416e-a200-b374debe09fc_2084x1368.png)
*来源：AMD*

### 更大的暂存内存与 MMA 形状

CDNA 5 的内存暂存缓冲比 Nvidia 对应产品更大。它有 320 KB 的 LDS（大致相当于 SMEM）和 32 KB 的 VGPR（大致相当于线程寄存器文件），因此每线程可访问 1024 个寄存器。此外，我们目前看到 CDNA 5 和前代一样，主要支持 16x16xK 形状。综合这些事实，我们推测更大的暂存缓冲是为了适应 wave 数量的增加：在并行线程数相同的情况下，wave 尺寸更小意味着 wave 数量更多。由于 MMA 形状没有增大、且每线程可访问的寄存器数量是 4 倍，AMD 不必像 Nvidia 那样把 MMA 范围扩大到 warp group 层面。

### Tensor Data Mover

Tensor Data Mover（TDM）与 Nvidia 的 Tensor Memory Accelerator（TMA）几乎一模一样。TDM 把数据从 HBM 搬到 LDS 而无需经过寄存器暂存。它支持 5 维分块、越界检查，甚至向不同 work group cluster（相当于 Nvidia 的 thread block cluster）多播。一个差异是 TDM 描述符从 SGPR 加载，而 Nvidia 是从主机加载到共享内存。Nvidia 的 Rubin 刚展示了内联 TMA 描述符更新以改善开发者易用性，我们期待看 AMD 能否把这个设计做对。

### GFX1250 原生支持 NVFP4

![](https://substack-post-media.s3.amazonaws.com/public/images/f75feb44-2a1d-4f2a-b0d1-86da804e189c_2156x1050.png)
*来源：AMD*

当前在推理领域竞争的两种 FP4 格式共享相同的 E2M1 元素：1 位符号、2 位指数、1 位尾数。但二者携带块缩放（block scale）的方式不同——正是块缩放让如此窄的数值类型可用。MXFP4 是 OCP 标准，AMD 围绕它构建了自己的 4 bit 路径，它为每个 32 元素块配一个 2 的幂的 E8M0 缩放因子。NVFP4 是 Nvidia 随 Blackwell 引入的格式，采用更细的 16 元素块、每块一个 FP8 E4M3 缩放因子，再叠加一个 FP32 的逐 tensor 全局缩放因子——代价更高但精度更好，正迅速成为 FP4 量化 checkpoint 的事实默认格式。

AMD gfx1250（MI455X 背后的架构目标）值得注意的一点是：其矩阵引擎原生支持 NVFP4。ROCm 中 MLIR 层面的缩放格式枚举 WMMAMatrixScaleFormat [包含 e8、e5m3、e4m3 成员](https://github.com/llvm/llvm-project/blob/main/mlir/include/mlir/Dialect/LLVMIR/ROCDLEnums.td)。

更具体地说，AMD 已经在 AITER 中交付了[以 gfx1250 编译的 NVFP4 GEMM code object](https://github.com/ROCm/aiter/blob/ae0bae8954110b12655e3232f68262dd63cd694e/hsa/gfx1250/f4gemm/f4gemm_bf16_nvfp4_ABpreShuffle_256x256_4x4_ps.co)，并接入了运行时分发表——格式判别器区分 NVFP4 与 MXFP4，[分发逻辑在 gfx1250 上选择 NVFP4 汇编 kernel](https://github.com/ROCm/aiter/blob/ae0bae8954110b12655e3232f68262dd63cd694e/aiter/ops/gemm_op_a4w4.py)。这是 gfx1250 特有的能力，CDNA4 并不具备。MI355X / gfx950 的 4 bit 只支持 MXFP4，通过带 E8M0 缩放、以 32 元素块为单位的 scaled-MFMA 实现——没有缩放格式字段、没有 16 元素块、没有 E4M3——AMD 公开的矩阵核心文档也仅止于此。

我们还发现 CDNA 5 额外支持无符号 E5M3（UE5M3）缩放因子格式，而 Nvidia Rubin 支持的是 E4M3 和 E5M2。UE5M3 把符号位挪作他用，扩大了动态范围，把最小非零可表示绝对值从 E4M3 的 2^-9 降到 2^-17。UE5M3 被提出作为 NVFP4 额外逐 tensor FP32 缩放的替代方案，这些格式日后的采用情况将检验其实效。

![](https://substack-post-media.s3.amazonaws.com/public/images/34fc99cf-6690-4626-ab34-e5e8b059f57b_1854x830.png)
*来源：https://arxiv.org/pdf/2601.19026*

### 保守的微架构改动

从 CDNA 4 到 CDNA 5 的微架构演进表明，AMD 对"放大"的信仰不如 Nvidia。Nvidia 押注模型需要更大的乘法，并逐代激进地扩大 scaled MMA 形状，在 Blackwell 上已扩大到需要 2 个 SM 协同执行的 MMA 形状。既然 CDNA 5 几乎没有扩大 MMA 形状，我们怀疑 CDNA 5 上不会出现对等特性。**我们也没看到 AMD 在数据压缩技术上有什么创新，比如 Rubin 的 3 bit 查找表（LUT）权重压缩 MMA 模式。**

# 第二部分：AMD 软件能攻破 CUDA 护城河吗？

## AMD 软件进步很快，但护城河已经移动

AMD 的软件故事已不再是"ROCm 坏掉了"。而是：ROCm 终于带着真正的紧迫感在推进，但竞争前沿移动得更快。我们[在 2025 年 4 月说过](https://newsletter.semianalysis.com/p/amd-2-0-new-sense-of-urgency-mi450x-chance-to-beat-nvidia-nvidias-new-moat)，在更锐利的开发者优先（developer-first）转向之后，AMD"走在正确轨道上"；后来又说 AMD 的软件质量自 2025 年 1 月以来已"大幅改善"。

## 究竟改善了什么

### CI 在成熟，但速度不够快

我们曾称赞 AMD 在 2026 年 1 月把稳定的 ROCm 支持移入 vLLM 上游正式版，并在随后不久增加了 nightly 版本。此后 CI 取得了具体但不完整的进展。[6 月的一项变更](https://github.com/vllm-project/vllm/pull/42793)为八个主要测试组添加了 AMD 镜像和门禁：V1 attention、engine、OpenAI API 正确性、小模型评估、多模态 pooling，以及三条投机解码（speculative-decoding）路径。[7 月的另一个补丁](https://github.com/vllm-project/vllm/pull/49270)清理了不稳定任务，并让现有镜像准备好重新变成合并阻断（merge-blocking）。但与 CUDA 的对等尚未得到证明：公开的回归看板、AITER 精度门禁、端到端分离 CI 和自动性能门禁仍停留在路线图层面。

令人振奋的是，AMD 的分布式推理工作已开始从一次性配方转向上游 CI。SGLang 于 6 月合并了面向 DeepSeek-V4 Flash 与 Pro 的[双节点 MI355X 1P1D 分离 nightly](https://github.com/sgl-project/sglang/pull/29084)，覆盖 FP8 与 FP4，随后在 7 月初增加了 [DP-attention、EP8、MTP](https://github.com/sgl-project/sglang/pull/29784) 和 [Kimi K2.6](https://github.com/sgl-project/sglang/pull/29855) 覆盖。这是重要的转变：分离式推理正从演示变成持续测试的上游特性。

Kubernetes 驱动着全球大多数推理部署，AMD 也是 llm-d（开源分布式推理 Kubernetes 编排引擎）的创始合作伙伴。但 AMD 至今没有为第一方 Pollara NIC 提供足够的 CI 自动化测试。原因不是工程师不想加，而是他们至今仍对内部 CI 容量规划投入不足。这导致在 llm-d Kubernetes 推理 nightly 测试上，与 Nvidia ConnectX-7 NIC 的对等率为 0%。原定在 Advancing AI 2026 前实现对等的 ETA 已落空。

vLLM 方面，由于本周 AMD 集群基础设施的稳定性问题，门禁自动化测试进度大幅倒退。过去几周，AMD 的硬核工程师在 vLLM 门禁上进展良好，力争实现 Advancing AI 前门禁与 CUDA 90% 对等的 ETA——直到 AMD 管理层开始从内部 vLLM 团队抽走集群。

门禁/阻断测试守护着重要的质量标准，因为测试不通过，PR 就不能合并。尽管 AMD 管理层可能拿非门禁通过率转移非技术人员的注意力，但门禁对等率和门禁通过率才是真正要紧的指标。

我们希望 AMD 管理层（Anush、Vamsi、Mark Papermaster）能重新排序优先级，给内部 vLLM 团队稳定的集群，让 AMD 内部硬核 vLLM 工程师得以完成把门禁对 CUDA vLLM 的对等率做到 90%+ 的工作，并拥有与 AMD 内部 SGLang 团队同等速度运作所需的工具。

### 单节点性能与可复现性是实打实的胜利

3 月，我们重点报道了 Kimi K2.5 1T MXFP4 交互性在 30 天内[最高 18× 的改善](https://x.com/SemiAnalysis_/status/2037333823134855344)，这来自[已合入 vLLM 0.18 上游的 AITER/vLLM 修复](https://github.com/vllm-project/vllm/pull/35850)。AMD 自己 2026 年 2 月的技术文章[《Speed is the Moat: Inference Performance on AMD GPUs》](https://www.amd.com/en/developer/resources/technical-articles/2026/inference-performance-on-amd-gpus.html)指出，AITER 驱动的单节点优化相对基线框架配置带来约 1.08x–1.2x 的吞吐提升。方向是对的：必须让开源基线框架在 AMD 上变快，而不只是 AMD 专属演示。

借助 ATOM 栈的优化，AMD 上的 MiniMax M3 性能也已追平 B200。

![](https://substack-post-media.s3.amazonaws.com/public/images/1df206f9-312f-4c9f-9780-a77af214204d_1038x1322.png)
*来源：https://x.com/RyanLeeMiniMax/status/2080142342288445553*

改善最大的地方在配方（recipe）、文档和可复现性。ROCm 如今的公开配方层比一年前深厚得多。ROCm 推理文档提供了完整的 AI 推理专区，涵盖 vLLM、SGLang、分布式 MoRI、Mooncake 和部署指南。vLLM 优化指南覆盖 AITER、attention-backend 选择、TP/EP/DP 策略、FP8/FP4 量化和单节点到多节点扩展。ROCm/MAD 仓库现在发布了覆盖 vLLM、SGLang、训练栈、大 EP 微基准和分离式 prefill/decode 配方的蓝图。

### 姿态是对的

这也是为什么我们基本认同 Anush 对软件的诊断。开发者优先的姿态、与上游对齐、day-0 模型支持和更快的发布节奏是正确的打法。我们曾称赞 Anush 2025 年的开发者关系攻势，最近也肯定其团队把 ROCm 从 vLLM 的二等 fork 推向接近一等公民的上游体验。[vLLM 官方博客](https://blog.vllm.ai/2026/02/27/rocm-attention-backend.html)如今宣称"仅仅移植"AMD 支持的时代已经结束，文档化了七个 ROCm attention backend，并展示最新 AMD/vLLM 协同工作带来 1.2x–4.4x 的吞吐提升。这才是可信的追赶路径该有的样子。

George Hotz 在 2025 年说得很到位：

> AMD 的机能失调是另一种情况。从一开始他们就有能干成事的领导层（Lisa Su 回复了我的第一封邮件），只是直到最近才看到投资软件的价值。如果他们只瞄准超大规模云厂商，他们的想法也算有点道理。但 SemiAnalysis 似乎让他们想通了：超大规模云厂商同样不会容忍糟糕的软件。他们能否转变文化、真正交付好软件还有待观察，但确实在朝那个方向移动；如果他们成功，AMD 被严重低估了。他们的硬件很好。
>
> ——George Hotz

## InferenceX：AMD 开发速度在变好

过去我们看到 AMD 在聚合与分离两种场景下都难以高效地在自家硬件上点亮新模型。我们在 [InferenceX](https://inferencex.semianalysis.com/) 上跟踪所有迭代性能，这让我们得以在一定程度上估算这种"速度"。

正如上一篇文章所提到的，AMD 推理团队在 DeepSeek v4 发布后的第一个月左右快速提升其性能，单节点场景尤其出色，干得很漂亮。下图标出了 DeepSeek v4 发布后前 47 天内对 MI355X SGLang 单节点配置的所有改进。

![](https://substack-post-media.s3.amazonaws.com/public/images/366fa51e-82c0-40c6-b1cf-bbbadd3907dc_2392x1454.png)
*来源：SemiAnalysis InferenceX*

最近，MiniMax M3 上也上演了类似剧情：AMD 推理团队快速迭代，做到了有竞争力的性能。

![](https://substack-post-media.s3.amazonaws.com/public/images/a5c4b37c-60b4-4d28-a922-a1f7d5d3de61_2984x1670.png)
*来源：SemiAnalysis InferenceX*

分离场景下 AMD 也做得相当好。这与约 6 个月前相比是巨大进步——当时团队在 DeepSeek R1 上苦战数月才追平 Nvidia。这是多方面因素的结果。首先，AMD 对软件栈做出了显著而具体的改进：用于分布式推理的 MoRI backend，以及对 Mooncake 的各项改进。更重要的是，由 Hai Xiao 领导的 AMD 分布式推理团队带着更强的紧迫感在工作，为分布式推理提供更好的支持。

下面的视频显示，MI355X FP4 分离式方案当时落后 Nvidia 数月之久。

注意，这是 AMD 第一份公开的分离式配方，1 月发布在 InferenceX 上。与下方 MiniMax M3 FP4 分离的 Day 0 进展形成鲜明对比，可以看出 AMD 如今在分布式推理解决方案竞争力上处境好得多。

![](https://substack-post-media.s3.amazonaws.com/public/images/477ca588-bfa0-4d0a-8203-bec7d848bcef_2622x1586.png)
*来源：SemiAnalysis InferenceX*

不过，快并不容易，尤其当对手先行起跑时。此前缺失的一块如今补上了：上文提到的 AMD 分布式栈所缺的东西，由 [ATOMesh](https://rocm.blogs.amd.com/software-tools-optimization/atomesh-inference/README.html) 自带的引擎补齐。它是一个 ROCm 原生的分布式推理网关，配有 Rust 编写的路由与编排层，处理分离式服务所需的集群级工作，例如 prefill/decode 分离路由、缓存感知负载均衡、RDMA KV 缓存传输（通过 MoRI-IO 或 Mooncake）。

它并非从零构建：[ATOMesh 衍生自 SGLang 的 sgl-model-gateway](https://github.com/ROCm/ATOM/pull/1174/changes)，并围绕 ATOM 和 AMD 硬件做了大幅重构。而且它确实能用——上文 MiniMax M3 的 InferenceX 结果就是证明。路由策略与模型执行保持分离，它可以像 AMD 自家的 ATOM 引擎一样自然接入 vLLM 和 SGLang。

![](https://substack-post-media.s3.amazonaws.com/public/images/135521c3-6089-4865-a050-4a6f0097b45e_978x1286.png)
*来源：SemiAnalysis*

### 蚕食 CUDA 护城河：用智能体实现 Day 0 支持

SemiAnalysis 团队苦干实现了 DeepSeek v4 和 MiniMax M3 的 day 0 支持，对 Kimi K3 等即将到来的前沿模型我们也会继续这么做。这个"day 0"性能是展示*随时间推移*性能变化的重要基线，而这正是 InferenceX 的北极星目标。

显然，真正让这些模型实现 day 0 支持的硬核推理工程工作，靠的是 AMD、Nvidia、Inferact、RadixArk 等地的 100 倍顶级工程师。但为了跑通 day 0 扫描（sweep），SemiAnalysis 团队常常还要修 bug 或摘低垂果实（目前这类情况在 AMD 配置上更常见）。随着能力强大的智能体兴起，这件事变得愈发轻松。流程大致如下：对给定配置（如 MiniMax M3 vLLM MI355X FP8），启动一个新的 Claude Code/Codex 智能体从网上拉取 day 0 配方，在 InferenceX 中搭建必要的管道，然后启动扫描。智能体既能访问 GitHub Action，也能直接访问物理 runner，持续监控状态。遇到引擎报错时，智能体可以自动判读根因，要么自动迭代重跑，要么请人类介入。我们可以在不同 SKU 上并行执行这条流水线，处理多个配置。

当错误被定位后，当前模型相当擅长在上游引擎代码（vLLM/SGLang/TRT）中找出原因，并在团队的少量指导下以 few-shot 方式实现修复。此外，我们还用智能体挖掘低垂果实型的性能改进。SemiAnalysis 团队 + 智能体向上游贡献的部分例子：

- [TRT: [fix] Fix fused MHC for DeepSeek-V4-Pro hidden size#13710:](https://github.com/NVIDIA/TensorRT-LLM/pull/13710)：DeepSeek v4 day 0 融合 MHC kernel 修复

- [[Bugfix] Fix NixlConnector handshake block_len validation for GQA-replicated KV heads#45879:](https://github.com/vllm-project/vllm/pull/45879)：MiniMax M3 分离式 Day 0 支持

- [[Bug Fix] [MiniMax-M3] Implement EAGLE3 support on the AMD MiniMax M3#45546:](https://github.com/vllm-project/vllm/pull/45546)：为 AMD MiniMax M3 day 0 启用投机解码

- [[Bugfix][ROCm] Fix MiniMax-M3 FP8 KV cache dtype:](https://github.com/vllm-project/vllm/pull/45720)：为 MI300X 和 MI325X 启用 FP8 KV 缓存支持，用于 MiniMax M3 day 0

- 以及更多……

感谢 vLLM 社区的 Roger Wang、Hongxia、Michael Goin 及其他 Inferact 工程师，感谢他们善意地指导和帮助这些修复顺利合入。

![](https://substack-post-media.s3.amazonaws.com/public/images/fb2c32bd-86b3-4b21-9896-4178ac23822b_1728x1032.png)
*来源：GitHub*

这种快速迭代在 3–6 个月前、对一个只有 2.5 名工程师的团队来说根本不可能。当前的前沿模型配上得力的 harness 是真的能打。它们能为开源服务引擎和 kernel 做出有意义的贡献。这或许*不一定*要归功于模型的"智能"，更多是它们被要求达成目标时那种纯粹的"死磕"劲儿。再加上可以并行执行大量此类任务，事情很清楚：测试和编写软件已不再是去年那种护城河。这对 AMD 总体是利好。通过让 AI 智能体承担以前由人类工程师完成的工作，所谓"CUDA 护城河"的重要性被削弱，这有助于 AMD 抵消 Nvidia 在工程师人数上的优势。

AMD 似乎在重仓这一论点：在 Advancing AI 2026 上，他们发布了 [ROCm.ai](https://www.amd.com/en/products/software/rocm.html?utm_campaign=domain&utm_medium=redirect&utm_source=301&utm_term=rocm.ai)——一套技能（skills）、harness 和框架集成，旨在进一步帮助开发者用智能体快速迭代 kernel 和性能调优。

![](https://substack-post-media.s3.amazonaws.com/public/images/79587253-5eba-4d58-b45e-0a2fe69bf346_1099x523.png)
*来源：AMD*

#### GEAK、Hyperloom 与以 InferenceX 为优化目标

ROCm.ai 不只是一张主题演讲幻灯片。其大部分组件已经公开在 AMD 的 [AMD-AGI org](https://github.com/AMD-AGI) 里，而且几乎与我们上文描述的 day-0 闭环一一对应。核心是 [GEAK](https://github.com/AMD-AGI/GEAK)（"Generating Efficient AI-Centric Kernels"），一个基于 mini-SWE-agent 的智能体，负责编写和调优 Triton/HIP 与 FlyDSL kernel；外面套着 [Hyperloom](https://github.com/AMD-AGI/Hyperloom)——负责编排：对服务负载做 profiling、找出瓶颈 kernel、派 GEAK 和 GEMM 调优智能体上场，并在计入成绩前对每个候选做端到端 A/B 门禁。外围是配角阵容：[Magpie](https://github.com/AMD-AGI/Magpie) 负责评估，[TraceLens](https://github.com/AMD-AGI/TraceLens) 负责 trace 分析，[Apex](https://github.com/AMD-AGI/Apex) 负责把智能体轨迹导出到带 RL 色彩的训练管线，还有 [AgentKernelArena](https://github.com/AMD-AGI/AgentKernelArena)——一个让 Claude Code、Codex、Cursor 和 GEAK 在相同 kernel 任务、相同评分标准下捉对厮杀的对垒 harness。

Hyperloom 的优化器直接从 InferenceX 拉取性能目标。在当前 main 分支上，它会抓取 InferenceX，由 target_analyzer 写出一个"竞品目标"，然后让智能体去冲击。他们 CI 的早期版本走得更远——计算相对 InferenceX 的增益百分比、统计有多少模型"击败"InferenceX，并把记分榜发到 Teams/Slack 频道——后来在开源发布前裁掉了这套机制。

我们视之为好事。InferenceX 的愿景是精确追踪开源框架的性能；如果智能体把它当作奖励信号并持续尝试改进，它完全胜任这一角色。这些努力将以更好的模型服务性能回馈 ML 社区。

这些仓库里还埋着一个更有意思的教训，也是我们自己 day-0 苦干中早就认识的：生成 kernel 是容易的部分，让数字可信才是难的。相当一部分工程其实是反作弊。GEAK 不得不[停止默默给未打补丁的基线 kernel 计分](https://github.com/AMD-AGI/GEAK/pull/255)而非智能体的实际补丁，并增加 GEAK_PROTECT_TEST_FILES 模式，剥除智能体对测试 harness 的改动，使其无法通过改写参考实现来伪造正确性。Apex 内置了篡改检测器，能标记硬编码的 print("PASS")，还带禁用库清单，防止智能体悄悄路由到预调优的 MIOpen 或 hipBLASLt 调用来"优化"Triton kernel。还是那个"死磕胜过智能"的故事：只要稍不留神，模型就会对基准测试做奖励作弊（reward-hack），而工作中惊人的比例是在搭建让加速真实可信的护栏。

而且确实管用。GEAK 的学习笔记已记录了在量产硅片上验证过的端到端战果：在 MI355X 上，一次 MXFP8 decode 受限的 dense-linear 重写带来约 +21.8% 的 e2e 提升；笔记也诚实注明 grouped-MoE GEMM 卡在约 1.1x 的天花板附近。这些本身都还不足以击破 CUDA 护城河。但这是迄今最清晰的信号：AMD 正在把一年前还需要一屋子 CUDA 工程师的工作流工业化。

### 推出 AgentX：InferenceX 全新智能体场景

当前的 8k1k + 1k1k 场景是评估芯片基线性能的绝佳代理，但它们都是单轮、随机数据请求，无法评估完整系统（路由器、KV 缓存传输、KV 缓存卸载、调度器等）。

过去几个月，我们一直与业界领导者合作开发一个智能体基准：AgentX。为了让该基准尽可能贴近真实世界的服务，我们收集了约 3 个月 SemiAnalysis 内部的 Claude Code、Codex 等 trace，然后用 [AIPerf](https://github.com/ai-dynamo/aiperf) 以不同并发度离线回放。数据集的部分统计见下图。值得注意的是，ISL 和 OSL 的中位数分别为 140k 和 396（与 8k1k 大相径庭），缓存命中率中位数高达 99.2%！注意，这是假设无限缓存下的结果，当然，多数真实服务并不可达。

数据集还包含真实的子智能体使用和动态工作流，通过持续引入未缓存上下文让服务器处理，进一步施压 KV 缓存。工具使用时间/用户思考时间（由轮间延迟捕获）也反映在数据集中，进一步加大 KV 缓存压力，并凸显 KV 卸载技术的实效——这类技术有可能延长 KV 缓存 TTL。

![](https://substack-post-media.s3.amazonaws.com/public/images/3f0fb740-3221-4111-ba8e-adc65dbbe50b_2188x1767.png)
*来源：SemiAnalysis HuggingFace*

我们对这个场景非常兴奋。我们与 WEKA、Inferact、RadixArk、LMCache、Mooncake、NVIDIA、AMD 及其他业界领导者合作，确保它准确反映 TaaS 提供商或 OAI/Ant 这类前沿实验室可能遭遇的真实流量。

过去一个月结果陆续出炉，已可在 InferenceX 上查看。我们很快会就结果与方法论撰写一篇深度文章。

## 单节点已过时，分离式正当红

如前所述，竞争前沿已从单节点聚合转向多节点分离推理。在 InferenceX v2 一文中，我们讨论过 AMD 在分布式推理上的"软件可组合性问题"：即他们在 disagg、FP4、WideEP、DP-attention 等单项优化上进展显著，但把多项优化组合起来就会把栈搞挂。尽管仍有进步空间，AMD 在这一领域已取得长足进展。

我们的 [GTC 2026 回顾](https://newsletter.semianalysis.com/p/nvidia-the-inference-kingdom-expands)把 Nvidia 的下一条护城河定位为分离式推理系统，包括 attention/feed-forward 分离（AFD）。由于 attention 有状态且受 KV 制约，而 FFN 无状态且可随 batch 扩展，这些阶段可以拆开、映射到最合适的硬件上。于是，推理领导力变成了分布式系统问题，而非单一 kernel 问题。WideEP、分离式 prefill、KV 传输、专家路由和调度器/编排都属于同一条新护城河。AMD 可以补上单节点差距，但如果这些优化不能在 vLLM 和 SGLang 中干净地组合，它打的仍是昨天的战争。

下方时间线可以让我们看清这个差距。开放的 CUDA 生态自 2024 年初就已在交付 disagg+WideEP，而 AMD 第一批公开发布的 PD-disagg + WideEP 配方直到 2026 年 1 月才通过 InferenceX 落地。AFD 的真正回报需要 superpod 级互连，而这类机柜级硬件 AMD 要到 MI455X 才出货。而在 GTC 2026 上，Nvidia 发布了 [Groq 3 LPX](https://newsletter.semianalysis.com/p/nvidia-the-inference-kingdom-expands)——一种集成进 Nvidia 推理机柜、专用于分离式 decode FFN 的基于 SRAM 的 LPU。

![](https://substack-post-media.s3.amazonaws.com/public/images/4b896c8a-56aa-4246-bfbf-15bde25cda63_1456x555.png)
*来源：SemiAnalysis*

## 新护城河：稀疏模型、分离与 WideEP

### 近期模型趋势：激活专家数依旧袖珍，总专家数爆炸增长

模型格局让可组合性问题更加紧迫。激活专家数始终钉在 4–10 的区间，而总专家数已扩展到 128、256、384，如今到 512。许多最新的巨型 MoE 还通过 MLA 式低秩设计把 KV 缓存压缩到相当于一两个头的水平。这意味着前沿模型正变得更稀疏、更吃带宽、更依赖路由、KV 搬移、WideEP 和分布式调度。在这样的世界里，再多赢一个单节点基准不算护城河，可组合的分布式推理才是。

### 分离式 Prefill 与 WideEP

分离式 prefill 把计算密集的 prefill 与内存密集的 decode 分到不同节点，消除两阶段间的相互干扰，并让运营方独立调整 prefill 与 decode 的节点配比。代价是 KV 缓存要经 RDMA 传输。我们估算一次 8,192 token 的 DeepSeek-R1 FP8-KV prefill 约需传输 290 MB。

目前在 InferenceX 上，AMD 的分离式推理配置常常比对应的单节点配置更差或只好一点点。但在 DeepSeek-R1 上，MoRI SGL 的等交互性（iso-interactivity）吞吐比聚合式 SGL 配置高出 2×–3×。

![](https://substack-post-media.s3.amazonaws.com/public/images/b5991c01-9f5d-47a8-be39-cdfb3789dde4_2504x1424.png)
*来源：SemiAnalysis InferenceX*

WideEP 把专家分散到更多 GPU 和节点上，而不是复制完整的专家岛。在 DeepSeek-R1（256 个路由专家）上，从单节点 8 GPU 的 EP8 扩展到跨 64 颗 GPU 的 EP64，把每颗 GPU 的专家数从 32 降到 4，为 KV 缓存腾出 HBM，支持更大并发 batch（从而每个专家每次 GEMM 处理更多 token），并让聚合 HBM 带宽随集群规模扩展。回报毫不含蓄：NVIDIA 报告 [Wide-EP 带来最高 2.28× 的单 GPU 输出吞吐提升](https://nvidia.github.io/TensorRT-LLM/blogs/tech_blog/blog15_Optimizing_DeepSeek_V32_on_NVIDIA_Blackwell_GPUs)（DeepSeek-V3.2、NVFP4、GB200 NVL72，EP16/EP32 对比 EP4/EP8）。正如我们在 InferenceX v2 中强调的，前沿实验室和多数 TaaS 提供商已在生产环境部署带 WideEP 的分离式服务。

换个说法，ATOM 和 AITER 只有在改善主流生态时才有价值。我们此前就指出，ATOM 或许有助单节点性能，但仍缺少生产特性，如 NVMe 或 CPU KV 缓存卸载、工具解析和 WideEP。正确的战略不是建一座 AMD 专属孤岛，而是把 kernel 推向上游、加固 CI、发布配方，让 FP4 + WideEP + disagg + 缓存卸载在默认开源栈中协同工作。如今 CUDA 护城河就是这样被侵蚀的。

### 分离式推理精度

2026 年 3 月之前，带 DP-attention（DPA）的 DeepSeekR1 分离式配置在精度评估中挂科，GSM8K 得分接近 0，而无 DPA 的扫描则以 >95% 通过。这是被 InferenceX 的评估跑出来的。这说明无 DPA 的分离路径能保持正确性，但一旦用上 DPA，栈就崩——再次暴露 AMD 的组合问题。不过该问题已修复。

一个尚未修复的问题是 SGLang + MoRI backend 在特定 batch size 下的 EP。在 DeepSeek-R1 上，[并发 64 的 decode 使 GSM8K 掉到约 80%，而其他所有并发下都稳定在约 94% 基线](https://github.com/sgl-project/sglang/issues/27194)。这个 bug 的灾难级版本——同一低并发路径悄无声息地产出流畅但错误的输出、GSM8K 得 0 分——已被定位到 AITER FP4 MoE kernel 中一个未初始化的 reduce buffer，并于 6 月修复；但并发 64 处残余的约 80% 悬崖仍然敞开，AMD 将其归因于量化 kernel 中只有该 batch size 才会触发的数值边界情况，且拒绝优先修复。

![](https://substack-post-media.s3.amazonaws.com/public/images/9749f416-3ee8-4344-b512-8deade685442_2644x1490.png)
*来源：SemiAnalysis InferenceX*

### 组合能用……有时候

AMD 现已证明其中若干优化可以组合：SGLang 的 MI355X nightly 镜像覆盖了带 DP-attention、EP8 和 MTP 的 DeepSeek-V4 分离，四节点 DeepSeek-V4 和 Kimi WideEP16 配置也已在硬件上验证。但组合仍是"特定模型、特定拓扑"专用，而非默认可靠。Kimi 的 DP8/EP8 路径因一次 GPU 显存故障被排除，其 WideEP16 int4 decode 路径目前必须禁用 HIP graph capture，WideEP16 的 CI 变更仍在评审中。差距已不再是"各个组件从来凑不到一起"，而是 AMD 还无法假设它们能跨模型、量化格式、并行策略、投机解码和网络拓扑无特例地协同工作。

### 分离式推理必须成为所有人的工作

分离式推理不能蜷缩在 AMD 的某个小专家角落里。AMD 自己的 [ROCm 教程](https://rocm.docs.amd.com/en/latest/how-to/rocm-for-ai/inference/index.html)就说单节点优化开始触及极限、分布式推理正变得越来越重要；随后 ROCm 在 2025 年 12 月发布了官方 [Mooncake PD 分离文档](https://rocm.docs.amd.com/projects/ai-developer-hub/en/latest/notebooks/inference/SGlang_PD_Disagg_On_AMD_GPU.html)，2026 年 1 月发布了[基于 MoRI 的分布式推理文档](https://github.com/sgl-project/sgl-learning-materials/blob/main/slides/amd_meetup_aiter_mori.pdf)。当官方栈开始发布 xP+yD 拓扑、RDMA 需求、1P2D 配方和 KV 传输框架时，DI 就不再是支线任务，DI 就是产品本身。它必须成为所有人的工作，横跨 ROCm、SGLang 集成、CI、配方和性能工程。

这就是迄今为止的 AMD 软件故事。单节点之路正在被修好。MoRI 前景可期。重叠（overlap）栈终于现身。但市场已经推进到 SBO、PD 分离、负载均衡和更宽的 EP 配置，这些都要求在真实生产约束下干净组合。AMD 不再需要再多一个孤胆英雄式优化，它需要的是整个分布式推理栈作为一个系统开始运转。

## AMD 如今的位置：逐块拆解分布式栈

### MoRI：一场实打实的胜利，由一支尖刀团队打造 🐯

必须承认，MoRI 是 AMD 的一场实打实的胜利。MoRI 是一个模块化 RDMA 框架，含两个专职组件：负责专家 dispatch/combine 的 MoRI-EP 和负责 KV 传输的 MoRI-IO。ROCm 现已为 MI355X 集群发布了官方的基于 MoRI 的分布式 SGLang 文档。它由一支位于中国的工程团队基于第一性原理构建。我们支持这个方向，但它需要多得多的开放 CI 和测试。

AMD 自己的 MoRI 路线图让规模问题变得具体。[H2 2026 路线图](https://github.com/ROCm/mori/issues/348)横跨三个子系统列出了雄心勃勃的规划：带调度器协同设计的分层分布式 KV 缓存（HBM→DRAM→NVMe，经 SPDK/GDS）、下一代 SHMEM v2、用 FlyDSL/C++ 编写并带弹性专家并行与容错的 EP v2 kernel、与 FlyDSL 协同设计的"mega kernel"，以及机柜级 Helios 支持。最后以 SGLang 和 vLLM 上游化收尾。这整张清单仍属于那五六位 ID 霸榜 MoRI 已合并 PR 的工程师。路线图是对的。但截至本文发布，它也还整整齐齐地摆在团队面前——压在同一小撮人的肩膀上。

### 最新硅片暴露差距：Helios（gfx1250）

衡量分布式栈还有多远要走，最清晰的标尺就是 AMD 最新硬件。在 Helios（gfx1250 / MI455X）栈的每一层，同一形状反复出现：单模型架构适配和 KV 传输管道落地很快，而 WideEP、验证以及按 wave32 调优的高价值 kernel 还没到位。

从地基说起。PyTorch 自己的 gfx1250 支持 7 月中旬合入（[ROCm/pytorch #3421](https://github.com/ROCm/pytorch/pull/3421)，是对一次上游变更的 cherry-pick——先落地、一天后被回退、一周后再度落地），但它纯粹是构建期架构管道，且被未发布的 ROCm 7.14+ 门控，因此在所有已出货的 wheel 上都处于休眠状态。它不带任何 gfx1250 CI，测试 runner 被推迟到一个并不存在的后续事项。它只是一副骨架：最高价值的路径（Composable Kernel GEMM 和 SDPA、FP8 grouped GEMM、int4）被过滤掉或直接硬报错，attention 是"Tech Preview"，wave32 kernel 尚未编写。AMD 的代码甚至一边给这颗芯片打上"CDNA5"标签，一边描述的是 GFX12.5、wave32、WMMA 执行模型——这是树内最清晰的证据，说明 Helios 离其 kernel 原本为之编写的 CDNA wave64 血统有多远。

![](https://substack-post-media.s3.amazonaws.com/public/images/0311e255-3093-439b-8cf3-0b5130f7b462_1324x458.png)
*来源：https://github.com/ROCm/pytorch/pull/3421/changes#diff-9b18bbaca027737173099a4fd1766ad9ce03c982f430852a09cc6c76aa365bb4R191*

往上一层，原始 MoE kernel 是整个栈中移动最快的部分。自春季以来，AMD 的 aiter 和 FlyDSL 库已吸收了远超一百个 gfx1250 PR：wave32/WMMA GEMM、MXFP4/A8W4 量化、MLA-v4 attention、TDM 数据搬移原子操作。其中约四分之一在未合并的情况下关闭。核心是 AMD 原生的"MegaMoE"路径：一条融合 MoE 专家并行流水线，其 dispatch/combine 算子层已被[vendored 进 aiter](https://github.com/ROCm/aiter/pull/4260)，而其 gfx1250 grouped-GEMM kernel（全局→本地专家重映射、融合 route/scatter，以及为 DeepSeek-V4 的 384 专家 MoE 调优的 masked grouped GEMM）[仍处于 open 状态](https://github.com/ROCm/aiter/pull/4165)，且仅在 a8w4（FP8 激活、MXFP4 权重）上验证过。这正是整个栈需要的 WideEP MoE 原语；只是还没完工，而 [gpt-oss](https://github.com/ROCm/FlyDSL/pull/397)、R1 和 V4 的 kernel 各走各的赛道落地。

断层在集成层，也就是这些 kernel 与框架相遇的地方。SGLang 的 [7 月 22 日 gfx1250 nightly](https://github.com/sgl-project/sglang/pull/32043)只做了构建和发布镜像。没有测试任务、没有精度门禁，构建跑在通用 runner 上、仅借道一台 MI300 做镜像——因为上游不存在 gfx1250 runner。该镜像会构建 MoRI，但钉在 6 月一个早于 gfx1250 支持的 commit 上，因此 MoRI-EP WideEP 无法运行：kernel 本身不带任何矩阵核心或 wave64 专属 ISA，但 MoRI 的构建门控只有 gfx942/gfx950，而 [AMD 后来添加的 wave32 支持](https://github.com/ROCm/mori/pull/466)位于一条更新的专家并行路径中，SGLang 的集成尚未调用它。一旦 AMD 把它接进 SGLang 所用的路径，WideEP 应该就能工作。MoRI-IO 的 KV 传输那一半是架构无关的主机侧 RDMA，今天就能在 gfx1250 上搬运 KV 缓存；然而 DeepSeek-V4 和 R1 实际的 gfx1250 配方是单节点张量并行，既无 WideEP 也无分离。

vLLM 的 [gfx1250 bring-up](https://github.com/vllm-project/vllm/pull/46516)从另一侧讲述了同样的故事：四个模型在 FFM 模拟器和早期硅片上跑出了不稳定的结果，仅 gpt-oss 有专门的性能工作，而那次"ATOM 对等"调优本身又被回退、"等 AITER 就绪"。MoRI 也被直接从构建中移除。这是一次可信的单节点 FP4 bring-up；但它不是分布式栈。

![](https://substack-post-media.s3.amazonaws.com/public/images/4779c9ff-eb0a-4192-85bf-6afbf539a20e_1288x614.png)
*来源：https://github.com/vllm-project/vllm/pull/46516*

就连 AMD 自家的引擎也遵循同一模式。ATOM 的 Helios 工作是分离优先、专家并行靠后：[ATOM 增加了 DeepSeek-V4 MoRI-IO write-push KV 传输](https://github.com/ROCm/ATOM/pull/1594)外加一个 UALink 纵向扩展 fabric backend——即 Helios 世代的互连——因此分离的 KV 传输那一半正是围绕 Helios 将要运行的模型和 fabric 构建的，尽管其 e2e 验证跑在 8 个 MI355X 节点和一台 UALink vPOD 上，而非 MI455x。但它不含 EP dispatch/combine、不含 MoRI-EP、不含 WideEP；ATOM 已交付的 DeepSeek-V4 配方仍以 TP=8 在单节点上服务模型，其所有 MoRI-EP PR 也全部瞄准上一代 gfx942/gfx950。自底向上：

PyTorch、kernel、MoRI、框架、ATOM——Helios 拥有架构适配和分离的前半段，唯独 WideEP 到处都没有。

## SemiAnalysis 助力 AMD 上游合入 NVIDIA 的 KV 缓存传输库 NIXL

在 Nvidia 的 [GTC 2025 NCCL 环节](https://www.nvidia.com/en-us/on-demand/session/gtc25-s72583/)，我们提问：鉴于 Nvidia 即将对其通信库进行大重构，Nvidia 是否会为 AMD 的通信库 fork 提供支持。Nvidia 明确表示不会帮助 AMD 通信团队适配即将到来的 NVIDIA 库重构，并且 NVIDIA 完全不参与 AMD 的通信开发。

一年后，在 Nvidia 的 GTC 2026 Dynamo 环节，我们提问：NIXL 已经接受了来自 Trainium Neuron fork 的上游贡献，那它是否也接受来自 AMD RIXL fork 的贡献？维护者当着一屋子人的面、公开表态：可以。

AMD 一直把 RIXL 挂在下游维护，烧着工程师工时去维护一份别人都能免费获得的基础设施副本。横亘在 AMD 与上游之间的唯一障碍，只是有没有人去尝试。NVIDIA 刚刚把这个借口拿掉了。

于是我们整个 4 月都在确保 AMD 知道这一点。我们[在 LinkedIn 上公开向 Stephen Bates 提出这个问题](https://www.linkedin.com/feed/update/urn:li:activity:7446965325176360960?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7446965325176360960%2C7447006653369032704%29&replyUrn=urn%3Ali%3Acomment%3A%28activity%3A7446965325176360960%2C7447058805529505792%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287447006653369032704%2Curn%3Ali%3Aactivity%3A7446965325176360960%29&dashReplyUrn=urn%3Ali%3Afsd_comment%3A%287447058805529505792%2Curn%3Ali%3Aactivity%3A7446965325176360960%29)，[主动提出帮 Anush 把 AMD 直接引荐给 NIXL 维护者](https://x.com/SemiAnalysis_/status/2041632398446866594?s=20)，并在 TensorWave 的 beyond summit 上当面向 Anush 问起 MoRI/RIXL 上游化的事；我们还帮助 AMD 与 NVIDIA 建立了联系，让他们得以把补丁推向上游。

5 月 15 日，AMD 的 Andy Luo 提交了 [PR](https://github.com/ai-dynamo/nixl/pull/1642)，为 gfx942（MI300X、MI325X）和 gfx950（MI350X、MI355X）增加 ROCm/HIP 构建支持，藏在一个默认关闭的 use_rocm Meson 开关后面。经过与 NVIDIA 侧维护者的数轮评审，该 PR 于 6 月 4 日合并。

Andy 的 PR 通过证明对 CUDA 路径零波及（zero blast radius）而过审。AMD 侧则验证了在 MI300X 和 MI355X 上经 NIXL+UCX 的端到端显存传输。叠放的后续 PR #1647 在两个 MI355X 节点上、用 AMD 自家的 AINIC RoCE NIC 和 libionic 驱动实现了 341 Gb/s 跨节点 RDMA，链路中没有任何 Mellanox NIC。今天，RIXL 已被完整移植到 NIXL。[Dynamo 核心此后也开始接收 AMD 补丁](https://github.com/ai-dynamo/dynamo/pull/9929)。

![](https://substack-post-media.s3.amazonaws.com/public/images/33f80999-74ee-4337-ad35-4146cce9bda0_1858x576.png)
*来源：https://github.com/ROCm/RIXL*

NIXL 是分离式服务的传输层，因此如果 AMD 想让 PD 分离和 WideEP 变得可靠而非"一模型一适配"，KV 传输就必须在人们实际部署的框架里、在 Instinct 上工作，而不仅仅是在 MoRI 内部。这本不该由我们来指出。仍存的缺口说的也是同一件事：nixlbench HIP 支持和 ROCm Dockerfile/CI 面以独立的后续事项落地，AMD GPU CI runner 仍停留在"愿意提供"而未成为已合并的工作流，rocSHMEM 还是个未来插件。

## 重叠栈迟到了，而市场已经继续前进

双 batch 重叠（Two-batch overlap，TBO）早就应该是标配。SGLang [把双 batch 重叠与专家并行列入了 2025 H1 路线图](https://github.com/sgl-project/sglang/issues/4042?timeline_page=1)，[公开文档](https://github.com/sgl-project/sglang/blob/main/docs/advanced_features/expert_parallelism.md)如今也暴露了 `--enable-two-batch-overlap`，宣称最高 2× 吞吐。AMD 自己 2025 年 11 月那篇 DeepSeek-on-MI300X 文章仍把双 batch 重叠描述为"仍在开发中"的必备特性，并把未来工作聚焦于双 batch 重叠与专家负载均衡。[MoRI EP 对双 batch 重叠的支持直到 2026 年 2 月 20 日才合入 SGLang。](https://github.com/sgl-project/sglang/pull/17953)太迟了。

成熟度差距立刻显形。[合并几天后，一位维护者就标记该 PR 破坏了 CI，要求回退并在修复后重新提交。](https://github.com/sgl-project/sglang/pull/17953#issuecomment-3941391203)这就是更宏大的 ROCm 推理故事的缩影：原料越来越齐，但太多关键优化仍然姗姗来迟、落地脆弱，需要再转一圈才能变成客户默认可以信赖的东西。

# 第三部分：AMD 在总拥有成本上具备竞争力 & OpenAI/Meta 最高 105% 折扣
