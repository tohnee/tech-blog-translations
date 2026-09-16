---
title: "AMD 2.0——全新的紧迫感 | MI450X 击败 Nvidia 的机会 | Nvidia 的新护城河"
title_en: "AMD 2.0 - New Sense of Urgency | MI450X Chance to Beat Nvidia | Nvidia's New Moat"
subtitle: "快速进步、开发者优先策略、AMD AI 软件工程师薪酬偏低、Python DSL、UALink 灾难、MI325x、MI355x、MI430X UL4、MI450X 架构、IF64/IF128、Flexible IO、UALink、IFoE"
date: 2025-04-23
source: https://newsletter.semianalysis.com/p/amd-2-0-new-sense-of-urgency-mi450x-chance-to-beat-nvidia-nvidias-new-moat
crawled: 2026-09-15
authors: ["Dylan Patel", "Kimbo Chen", "Daniel Nishball", "Wega Chu", "Ivan Chiam"]
tags: ["Hardware Architecture", "Accelerators", "Semiconductors"]
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# AMD 2.0——全新的紧迫感 | MI450X 击败 Nvidia 的机会 | Nvidia 的新护城河

> 原文：[AMD 2.0 - New Sense of Urgency | MI450X Chance to Beat Nvidia | Nvidia's New Moat](https://newsletter.semianalysis.com/p/amd-2-0-new-sense-of-urgency-mi450x-chance-to-beat-nvidia-nvidias-new-moat) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**快速进步、开发者优先策略、AMD AI 软件工程师薪酬偏低、Python DSL、UALink 灾难、MI325x、MI355x、MI430X UL4、MI450X 架构、IF64/IF128、Flexible IO、UALink、IFoE**

*SemiAnalysis 正在扩充 AI 工程团队！如果你具备 PyTorch、训练、推理、系统建模、SLURM/Kubernetes 方面的经验，请将简历和 5 条能证明你工程卓越能力的要点发送至 [letsgo@semianalysis.com](mailto:letsgo@semianalysis.com)。*

自 [SemiAnalysis 于 2024 年 12 月发表文章、详述 AMD 软件平庸且可用性欠佳](https://semianalysis.com/2024/12/22/mi300x-vs-h100-vs-h200-benchmark-part-1-training/)以来，AMD 已切换到更高的挡位，在过去四个月里对我们列出的许多问题项都取得了快速进展。我们将 AMD 这种全新的紧迫感视为其追赶 Nvidia 征程上的重大利好。AMD 如今已进入战时状态，但前方仍有许多硬仗要打。

在本报告中，我们将讨论 AMD 已做出的诸多积极变化。他们走在正确的道路上，但需要增加用于 GPU 时数的研发预算，并进一步投资 AI 人才。我们将提出更多建议，并详细阐述 AMD 管理层的一个盲点：由于薪酬结构对标了错误的公司群体，他们在 AI 软件工程师的争夺战中缺乏竞争力。

我们还将讨论 AMD 的产品发布节奏如何使其当代产品与 Nvidia 的下一代产品正面相撞。MI325X 与 B200 同期发布，导致客户兴趣平平。客户如今正把 8 GPU 的 MI355X 与机柜级的 72 GPU GB200 NVL72 方案放在一起比较。[我们加速器模型（Accelerator Model）中的需求观点早在 2024 年初就追踪到微软的失望情绪，以及 AMD GPU 后续订单的缺位](https://semianalysis.com/accelerator-industry-model/)。

我们现在认为，[OpenAI 经由 Oracle](https://semianalysis.com/accelerator-industry-model/) 以及[其他几家大客户](https://semianalysis.com/accelerator-industry-model/)对 AMD GPU 重燃兴趣，但依旧没有微软——前提是他们能与 AMD 达成极为优惠的定价。**我们还将勾勒 AMD 全面追赶 NVIDIA 的窗口如何在 2026 年下半年打开——届时 AMD 终于会把一款机柜级方案推向量产。这些 SKU，即 MI450X IF64 与 MI450X IF128，有望与 NVIDIA 2026 年下半年量产的机柜级方案（VR200 NVL144）一较高下。**

SemiAnalysis 正在与 NVIDIA 和 AMD 积极合作，在 Hopper 与 CDNA3 级 GPU 上进行推理基准测试，并将在未来几个月内发布一篇全面的基准测试与对比文章。

## 执行摘要

1. 我们与 Lisa Su 会面，呈报了[12 月 AMD 文章](https://semianalysis.com/2024/12/22/mi300x-vs-h100-vs-h200-benchmark-part-1-training)中的发现，她承认了 ROCm 软件栈的诸多缺口，并表达了强烈的改进意愿。
2. 过去四个月，AMD 在其 AI 软件栈上进展迅速。
3. 2025 年 1 月，AMD 启动了开发者关系（devrel）职能，主要由 AMD 的 AI 软件掌门人 Anush Elangovan 牵头。他的工作重心是在 Tech Twitter 和线下（In Real Life）活动上与外部开发者互动。
4. 2025 年 1 月，AMD 认识到外部开发者社区正是 CUDA 之所以伟大的原因，并自此采纳了"开发者优先"（Developer First）战略。
5. 在 SemiAnalysis 12 月发表 AMD 文章之前，[参与 PyTorch 持续集成/持续交付（CI/CD）的 MI300X 数量为零](https://x.com/AnushElangovan/status/1877342554842345479)。此后 AMD 已将 MI300 加入 PyTorch CI/CD。过去四个月，AMD 在 CI/CD 上取得了长足进步。
6. AMD 计划借鉴[谷歌 TPU Research Cloud（TRC）](https://sites.research.google/trc/about/)的打法，在 6 月即将举行的 Advancing AI 活动上推出一个开发者云。衡量成功的标准，是 AMD 社区开发者云上能否出现一个["GPT-J 时刻"](https://arankomatsuzaki.wordpress.com/2021/06/04/gpt-j/)。
7. AI 软件工程岗位的薪酬是 AMD 管理层的盲点。其总薪酬显著逊色于那些擅长 AI 软件的公司，例如 NVIDIA 和各 AI 实验室。
8. 过去四个月，AMD 内部开发集群已显著改善，但与长期 GPU 开发竞争格局下有效作战所需的水平相比仍有差距。
9. AMD 应大幅增加并优先把投资分配到研发（R&D）的资本开支（capex）与运营开支（opex）项目上，为其团队提供多得多的软件开发 GPU 资源。当前对季度盈利的短视专注正在损害其长期竞争力。AMD 需要投入多得多的 GPU——他们拥有的 GPU 总量还不到 Nvidia 的 1/20。
10. 让整个 CUDA 生态在 Python 上成为一等公民，一直是 Jensen 的头等要务。NVIDIA 如今在栈的每一层都有 Python 化（pythonic）接口，而 ROCm 没有。这对 AMD 面向开发者的长期可用性构成严重威胁。
11. 尽管 RCCL 已取得一些像样的进展，但由于 [GTC 2025 上公布的 NCCL 新改进与新特性](https://www.nvidia.com/en-us/on-demand/session/gtc25-s72583/)，NCCL 与 RCCL 之间的差距仍在显著拉大。
12. 过去四个月，AMD 在软件基础设施层（即 Kubernetes、SDC 检测器、健康检查、SLURM、Docker、指标导出器）上取得了一些进展，但进步速度远赶不上 AMD 机器学习库的进步速度。
13. AMD 目前缺乏对许多推理特性的支持，例如对分离式预填充（disaggregated prefill）、智能路由（Smart Routing）与 NVMe KV 缓存分层的良好支持。NVIDIA [开源了分布式推理框架 Dynamo](https://github.com/ai-dynamo/dynamo)，进一步普及了 NVIDIA GPU 上的分离式服务。
14. MI355X 仍无法与 NVIDIA 机柜级 GB200 NVL72 方案竞争。AMD 转而将 MI355X 定位为与 NVIDIA 风冷 HGX 方案竞争的产品，但大多数客户在采购时做的并不是这种比较。
15. 到 2026 年下半年，AMD 的 MI450X 机柜级方案如果执行得当，有望与 Nvidia 的 VR200 NVL144 一较高下。
16. SemiAnalysis 正在扩充 AI 工程团队！如果你具备 PyTorch、训练、推理、系统建模、SLURM/Kubernetes 方面的经验，请将简历和 5 条能证明你工程卓越能力的要点发送至 [letsgo@semianalysis.com](mailto:letsgo@semianalysis.com)。
17. AMD 正在整个软件栈范围内招聘工程师。可以给 Anush 发邮件：[anush+letsgo@amd.com](mailto:anush+letsgo@amd.com)。

## 自我们 12 月 AMD 文章以来有哪些新变化？

AMD 文章发布数小时后，Lisa Su 便主动联系我们，安排与我们工程团队通话，逐条详细讨论我们的每项发现与建议。[就在第二天太平洋时间上午 7 点](https://x.com/dylan522p/status/1871287937268383867)，我们向 Lisa 呈报了发现，并向她复盘了此前五个月与 AMD 团队合作、尝试修复其软件以执行各类工作负载基准测试的经历。

我们向她展示了团队提交给 AMD 工程对接人的数十份 bug 报告。她对在 ROCm 上遭遇糟糕体验的最终用户表示同情，并承认了 ROCm 软件栈的诸多缺口。此外，Lisa Su 与她的团队表达了让 AMD 做得更好的强烈意愿。为此，在接下来一个半小时里，Lisa 就我们的经历和关键建议，向她的工程团队和我们的工程师提出了大量细致的问题。

![](https://substack-post-media.s3.amazonaws.com/public/images/cea36a0e-95e6-4689-add4-a09080b760ac_952x1024.png)
*来源：X*

来自最高层的这种基调转变已在整个组织引起共鸣。**AMD 如今处于战时模式**，正在正视软件缺口并努力补齐。与 2024 年 AMD 公关部门*拒不公开承认*软件存在任何重大问题时的情形相比，这是一个巨大转变。

2025 年至今，AMD 已承认其软件的 bug 远多于 Nvidia 当前水平，但正在快速改进，并动员社区力量推动 ROCm 达到同等水平。尤其是 AMD 的 AI 软件掌门人 Anush Elangovan，一直在积极处理 AMD 的这些问题。

![](https://substack-post-media.s3.amazonaws.com/public/images/80d0fd27-c2ac-4831-89ad-f63cbce159ad_1024x632.png)
*来源：X*

## AMD 的文化转变——重燃的紧迫感

接受，是悲伤的最后一个阶段。AMD 终于接受了自身巨大的软件差距，现在可以着手解决这些问题，为自己赢得在软件与硬件竞赛中击败 NVIDIA 的机会。AMD 已重振旗鼓，[但 Nvidia 仍在全力冲刺](https://nypost.com/2024/08/26/business/nvidia-employees-can-work-7-days-a-week-until-2-a-m-but-few-leave-because-of-ai-chip-giants-lavish-pay-report/)，AMD 必须与之匹敌甚至更快，才能实现追赶。Nvidia 的员工显然明白，Nvidia 要在竞争激烈的市场中保持领先，有时[需要加班加点](https://nypost.com/2024/08/26/business/nvidia-employees-can-work-7-days-a-week-until-2-a-m-but-few-leave-because-of-ai-chip-giants-lavish-pay-report/)。AMD 要想赢，至少要和 Nvidia 一样努力、一样聪明，甚至更努力、更聪明。我们看到了这种情况开始显现的清晰迹象。

![](https://substack-post-media.s3.amazonaws.com/public/images/55518b58-c994-4df1-a886-b1a9d1dced75_1024x929.png)
*来源：X*

专注而饥饿的团队实现追赶的例子比比皆是。xAI 对阵 OpenAI 就是一个例子：文化上转向紧迫感、进入战时姿态，可以让一家公司以惊人的速度追上竞争对手。

![](https://substack-post-media.s3.amazonaws.com/public/images/4c90564f-6e0e-43ee-b752-5e554d659e3a_1024x530.png)
*来源：xAI*

我们看到许多具体例子表明这种态势正在 AMD 内部上演。AMD 执行落地较好的一个领域是其产品路线图，目标是机柜级方案与 Nvidia 拉平。我们会在后文解释对其机柜级 MI450X 方案的估算。

另一个例子是 AMD 过去四个月在 AI 软件栈上的快速进步。他们的[训练](https://rocm.blogs.amd.com/artificial-intelligence/training_rocm_pt/README.html)与[推理性能](https://rocm.blogs.amd.com/artificial-intelligence/DeepSeekR1_Perf/README.html)以及开箱体验都在显著提升。[他们甚至在训练基准中采用了 SemiAnalysis 的代码](https://www.linkedin.com/feed/update/urn:li:activity:7292299941761187840)。

2025 年 1 月，AMD 启动了开发者关系（devrel）职能——它终于明白，开发者才是成就 Nvidia CUDA 伟大的关键，并承认赢得开发者之心对 ROCm 的成功至关重要。目前，开发者关系团队由 Anush Elangovan 领导，他既是 AMD 在线下活动上的唯一 devrel，也活跃于[Tech Twitter 等社交媒体论坛](https://x.com/AnushElangovan)。

在开发者层面，AMD 走得更远。6 月，AMD 将推出一个开发者云，专注于与广大社区互动。这是 SemiAnalysis 建议 AMD 弥合差距的直接成果。

![](https://substack-post-media.s3.amazonaws.com/public/images/e11cfc7e-8974-4304-ac05-e0f9300e7f09_1024x396.png)
*来源：SemiAnalysis、AMD*

在基准测试与性能宣称的可复现性上，AMD 如今胜过 Nvidia。AMD 开始发布易于遵循的操作说明，让用户和开发者能够复现其基准测试运行，而不是发布无法验证的、不切实际或有偏向性的性能宣称。一个绝佳例子是 [AMD 发布了一篇关于如何复现其 MLPerf Inference 5.0 提交的精彩博客](https://rocm.blogs.amd.com/artificial-intelligence/reproducing-amd-mlperf-inference-submission/README.html)。NVIDIA 在最近一轮 MLPerf 测试中并未提供此类说明。

## 是什么成就了 CUDA 的伟大？

CUDA 最大的优势不仅在于其内部软件开发者，还在于其生态系统：包括 400 万在 CUDA 平台上开发的外部开发者、数千家企业以及众多 AI 实验室和初创公司。这形成了一个自我强化的飞轮——工具、教程与现成内核（kernel）降低了每个新人的采用门槛，也让老手保持高速。凭借如此庞大的开发者基数，圈内经验（tribal knowledge）得以快速传递给新人。

这一繁荣生态的结果是：突破性想法——无论是新的注意力算法、状态空间模型（state-space model）还是高吞吐服务引擎——几乎总是先出现在 CUDA 上，更早获得反馈，并在 CUDA 上被更深度地调优，进而吸引下一波开发者。

这种集体能量的回报显而易见：当研究人员发布一款改变格局的内核时，CUDA 版本通常当天就能问世。Tri Dao 的 FlashAttention 发布了参考 CUDA 代码，而 ROCm 花了多个季度才实现自己的优化版注意力。选择性状态空间模型（selective-state-space model）同样如此，作者只发布了 CUDA 实现，作者本人既不支持也未将其移植到 ROCm。ROCm 版 Mamba 的移植出自 AMD 内部工程师之手，而非原作者。在服务侧，UC Berkeley 的 vLLM 与 SGLang 的维护者主要在 NVIDIA GPU 上开发，只有当 CUDA 路径稳定后，维护者才会帮助 AMD 内部开发者移植到 ROCm。

另一个例子是，得益于数以百万计的 CUDA 生态外部开发者，bug 的发现与修复更快。相比之下，在 ROCm 上，一个 bug 可能要几个月才被发现——我们去年发现并报告的众多 bug 便是如此。例如 2024 年 ROCm 的 torch.scaled_dot_product_attention API。注意力（attention）是最先进（state-of-the-art）transformer 模型中最重要的一层。

## 开发者，开发者，开发者

自 2025 年 1 月起，AMD 一直高调宣扬开发者优先的做法，呼应 Steve Ballmer 的著名口号，也与 Jensen 的做法如出一辙。在 [TensorWave 的 "Beyond CUDA 2025" 峰会](https://www.youtube.com/watch?v=RAK3Ce0RXgM&ab_channel=TensorWave)上，AMD 的 AI 软件掌门人 Anush 用三个词勾勒了 ROCm 的未来——"**[开发者，开发者，开发者](https://www.youtube.com/watch?v=Vhh_GeBPOhs&ab_channel=MrWueb007)**"。我们相信，这种开发者优先的思路与信息将在 AMD 6 月的主题演讲活动上被放到更大的舞台上放大。AMD 终于明白，让 CUDA 不可战胜的不仅是出色的芯片，还有蜂拥而至的外部开发者。我们对 AMD 新的开发者优先策略感到非常积极。

![](https://substack-post-media.s3.amazonaws.com/public/images/3db26059-86f9-4fb7-87a6-d0139522cd42_240x180.gif)
*来源：Microsoft*

2025 年 1 月，Anush 践行了这种开发者优先的做法：在 Tech Twitter 与 GitHub 上同外部 ROCm 开发者互动收集反馈，在 ROCm 掉链子（这经常发生）时充当客服，并亲自解答问题。这种亲力亲为的互动是实实在在的进步，但 AMD 的开发者关系仍靠极简人手运转；除 Anush 之外，AMD 基本上没有全职 dev-rel 工程师。AMD 已开始招聘[全职开发者关系工程师](https://careers.amd.com/careers-home/jobs/63017?lang=en-us)，但要弥合与 NVIDIA 布道者大军的差距，公司至少需要 20 名以上的 devrel 工程师，定期举办线下黑客松与见面会。

NVIDIA 一年一度的 GTC 开发者大会——"AI 界的超级碗"——在短短一周内塞入 500 多场面向开发者的深度专场与上机实验。这些议程覆盖栈的每一层——从 PyTorch 到 JAX、CUTLASS、CUDA C++、汇编，再到性能分析工具——为外部开发者提供了学习并推进前沿的可靠场所。

相比之下，AMD 仍缺乏一个拥有大量开发者专场、GTC 式的开发者大会。公司 6 月的"Advancing AI"活动很适合发布路线图，但本质上只是几场产品主题演讲加上少量预录演讲——远不及 GTC 上开发者所能获得的多轨道专场与代码实验深度。如果 AMD 对新的开发者优先立场是认真的，就应创办一年一度、线下举办的 ROCm 开发者大会：三到四天的并行议程，涵盖内核编写、图编译器、HIP/Triton 迁移、MI300 集群调优以及用 ROCm 工具链实时调试。再配上由扩充后（20 人以上）的 devrel 团队在现场运作的黑客松，以及后续的地区路演，ROCm 用户终于将有一个分享实战故事、暴露阻塞性 bug、编织社交网络的场所——正是这种社交网络让 GTC 成为 CUDA 社区不可或缺的一环。

![](https://substack-post-media.s3.amazonaws.com/public/images/72b092ea-fde3-4ba6-b237-1e7a7ae556b8_1024x562.png)
*来源：NVIDIA*

尽管 George Hotz 本可接受 AMD 早前提出的、提供完整 BMC 访问权限的云端托管 MI300X 系统，他仍坚持要物理硬件，以便直接*"hack the metal"*（直捣金属层）。AMD 起初不情愿——尽管 Hotz 的目标正是帮助其 GPU 上的开源工具建设。当备受尊敬的 PyTorch 联合创始人 Soumith Chintala 发推支持 Geohotz 获得实体机箱后，这场僵局演变成了一场公开大戏。

![](https://substack-post-media.s3.amazonaws.com/public/images/049c7cb0-0422-45a0-beb7-a508493ebad5_1024x519.png)
*来源：X*

我们相信这一推波助澜起了作用：[Geohotz 3 月 8 日的博客](https://geohot.github.io/blog/jekyll/update/2025/03/08/AMD-YOLO.html)披露，AMD 已松口，给他寄去了两台 MI300X 主机。至此，AMD 终于通过了 *Geohotz 的"文化测试"*。对 AMD 而言，这可以说是一场声誉上的胜利，意义大于技术层面——向一位高知名度的黑客寄出真芯片，标志着一种营销经费买不来的、全新的开发者优先风气，也终于把一场难堪的 Twitter 风波变成了展示 AMD 新开发者优先理念的故事。

除了给 Geohotz 寄机器，我们认为 AMD 还可以轻松再赢一场声誉与营销的胜利：向学术实验室捐赠 AMD GPU 实体机。[Jensen 与 Ian Buck 向学术实验室捐赠 GPU 的历史可以追溯到 2014 年](https://x.com/haozhangml/status/1914439713332863348?s=46)。今年，Jensen 继续支持 [CMU 的 Catalyst Labs](https://x.com/scsatcmu/status/1912910889566490821?s=46)、[伯克利的 Sky labs](https://x.com/vllm_project/status/1893001644037566610)、[UCSD 的 HaoAI Lab](https://x.com/haoailab) 等学术实验室已有一段时间——既向它们捐赠镀金 B200 实体机，又提供 NVIDIA GPU 的免费云访问。

## 持续集成/持续部署（CI/CD）

在 SemiAnalysis 12 月发表 AMD 文章之前，[参与 PyTorch CI/CD 的 MI300X 数量为零](https://x.com/AnushElangovan/status/1877342554842345479)。此后 AMD 已将 MI300 加入 PyTorch CI/CD。AMD 一直因提供多 bug 的软件而"闻名"——把 MI300 加入 PyTorch CI，将大大有助于持续清除 AMD 软件中的 bug！

此前，AMD 不愿花钱投资 CI/CD 资源，但我们相信这一立场在过去四个月已经转变。在 ROCm SF（旧金山）开发者活动上，一位 AMD 软件工程师走到我们面前致谢，并告诉我们，正是得益于我们的努力，他们现在有了 CI 资源。

除单元测试 CI 外，AMD 还在 TorchInductor 性能 CI 上启用了 MI300X，从而[在 inductor /torch.compile 提交中跟踪性能](https://x.com/AnushElangovan/status/1884727132477382915)。[据一位 Meta CI 工程师所述](https://x.com/_seemethere/status/1924526179463397425)，MI300X 节点由 AMD 提供，而 NVIDIA 没有提供任何资源，Meta 的全部 A100 与 H100 容量都是自掏腰包。就这一具体的编译 CI 而言，AMD 领先于 NVIDIA。不过——仍有很大进步空间：AMD 的 dynamic shapes torch.compile 通过率只有 77%，而 Nvidia 超过 90%。

![](https://substack-post-media.s3.amazonaws.com/public/images/5c173e03-c664-47d1-a6ea-48bdc3c64918_1024x559.png)
*来源：PyTorch*

AMD 应在此基础上更进一步：开源并公开其全部 CI/CD 与仪表盘，让任何人都能查看 AMD 软件在所有 ROCm 库（HipBLASLt、Sglang、vLLM、TransformerEngine 等）上的通过率。[目前，其机器学习库中唯一可公开访问的 ROCm CI 只有 PyTorch](https://hud.pytorch.org/benchmark/compilers)。

## 即将推出的社区开发者云

Google TPU 之所以能获得外部开发者采用，原因之一是 TPU 的免费 Colab 访问，以及通过 [TPU Research Cloud](https://sites.research.google/trc/about/)（TRC）提供大型集群访问。这让社区能够快速、免费地用上 TPU，催生了 [TRC 聚焦页面](https://sites.research.google/trc/spotlight/)上展示的许多有趣项目，以及[作为 TRC 一部分发表的众多论文](https://sites.research.google/trc/publications/)。事实上，早在 2020 年、ChatGPT 时刻远未到来的年代，一名高中生就能在一个相当庞大的 TPU pod 上免费训练出与 GPT-2 一较高下的模型。除了提供大量 8-16 芯片的小型 pod 外，TRC 还定期向研究者提供 1000+ 芯片 pod 的 1-2 周免费访问。

[著名的开源 GPT-J 模型](https://arankomatsuzaki.wordpress.com/2021/06/04/gpt-j/)同样在 TPU 上免费训练而成，由此产生了一个完整开源仓库讲解如何用 JAX 使用 TPU，进一步推动了外部社区对 TPU 的采用。TRC 在推广 TPU、支持开源社区方面大获成功。

AMD 的开发者云计划实质上就是照搬 Google 的剧本。我们相信，如果 AMD 为该开发者云计划投入足够多的 GPU、让其 GPU 可以轻松且免费地被使用，这个开发者云将帮助 AMD 扩大 GPU 的采用面。这是 AMD 与 NVIDIA 竞赛中必须打赢的关键一役。

**衡量成功的标准，是 AMD 社区开发者云上能否出现一个"GPT-J 时刻"。**

![](https://substack-post-media.s3.amazonaws.com/public/images/3f186274-2562-43aa-b31e-5bb1f03e0fcf_1024x396.png)
*来源：SemiAnalysis、AMD*

## AMD 管理层的盲点——AMD AI 软件工程师薪酬

由于薪酬缺乏竞争力，AMD 的 AI 软件部门面临严峻挑战，这严重影响其吸引和留住顶尖人才的能力。其他以开发优秀 AI 软件著称的公司，薪酬水平显著优于 AMD。

薪酬虽非一切，但仍是影响工程师决策的重要因素。工程师评估职业机会时往往会综合考量多重因素，包括技术挑战、职场文化与成长空间。然而，有竞争力的薪酬依然关键，在 AI 软件工程这类高度专业化的领域尤其如此。

在 AI 工程师圈内众所周知：AMD 的总薪酬包（包括基本工资、RSU 限制性股票单位与奖金）明显落后于 NVIDIA、Tesla Dojo、[OpenAI 芯片团队](https://openai.com/careers/hardwaresoftware-co-design-engineer/)、Google TPU、xAI 等竞争对手。

在与顶尖 AI 软件工程师谈及为何不选择 AMD 时，许多人强调：在 AMD 做软件，感觉像是在移植 NVIDIA 工程师两年前开发的功能。相比之下，NVIDIA 让工程师有机会从事前沿软件工作，为 o3 等最先进模型所用的芯片编写软件——训练与推理皆然。

此外，被"大卫对歌利亚"叙事中"大卫"一角吸引的工程师，往往会选择 Google TPU 或 [OpenAI 芯片团队](https://openai.com/careers/hardwaresoftware-co-design-engineer/)而非 AMD。这些团队薪酬明显更高，而且由于这些公司拥有海量的内部工作负载、可以自己当自己的客户，在挑战 NVIDIA 这件事上的胜算可以说也更大。对雄心勃勃的工程师而言，这些是更有吸引力的选择。

AMD 内部对其薪酬结构的对标，似乎是在挑肥拣瘦地选择可比公司。通过向 Juniper Networks、Cisco、ARM 这些不以软件见长的半导体公司看齐，AMD 可能误以为自己的薪酬具有竞争力。然而，一旦正确地与那些以 AI 软件闻名的领域对标——GPU 内核、GEMM、PyTorch 内部机制、分布式训练基础设施、推理引擎——薪酬差距便暴露无遗。

当进行严格的对等比较时——例如把 NVIDIA 的 PyTorch Lead 与 AMD 的 PyTorch Lead 相比、NVIDIA 的 NCCL 工程师与 AMD 的 RCCL 工程师相比——NVIDIA 的薪酬显著更高，因而能够吸引并留住顶尖人才。

这一问题是 AMD 管理层战略中的一个关键盲点。我们认为，AMD 明白软件工程师对其长期竞争力与创新何等重要，也想把他们置于战略核心，但这个盲点源自不准确的对标和大而化之的比较——可谓一种"战争迷雾"。不幸的是，这导致对软件价值的持续低估，有可能进一步加剧公司相对直接竞争对手的软件弱势。

AMD 应保持 AI 软件工程岗位基本工资稳定，但大幅提高 RSU。通过让工程师薪酬与 AMD 的未来增长更紧密地挂钩，公司可以更直接地把顶尖人才的利益与组织的长期业绩绑定在一起。

鉴于 AMD 拥有超过 50 亿美元的现金储备，公司完全有充足的财力对软件人才进行战略性投资。管理层现在必须下定决心，通过有分量的薪酬提升来优先留住和吸引高素质工程师。若不采取行动，AMD 恐将长期陷于落后 NVIDIA 的境地，动摇其在快速演进的 AI 市场中的进展。

## 内部开发集群需要更多预算

过去四个月，AMD 的内部开发集群已有显著改善，但与长期 GPU 开发竞争格局下有效作战所需的水平相比仍有差距。

目前，AMD 声称从云服务商（CSP）处租用了合计约 8,000 颗 MI300 GPU 的容量，分布于多个集群，其中最大的单一集群约含 2,000 颗 MI300 GPU。然而更深入的检视表明，由于 AMD 内部按"突发（burst）"模式运营，全公司范围内可持续获得的真实可用容量可能更接近合计 3,000 到 4,000 颗。内部开发者现在获取单节点开发资源已足够，但多节点与整集群级别的开发仍受掣肘。这一限制严重影响大型项目与协作开发，GPU 可用性在绝对数量与稳定性上都仍需大幅提升。

更何况，随着数据中心级分离式预填充优化成为推理领域新的行业标准做法，如今即便是开发推理解决方案也需要集群级资源。AMD 当前为内部单个开发者提供的集群级资源有限，这进一步削弱了其在不断演进的格局中有效创新与竞争的能力。

AMD 进一步扩张与创新的一大障碍，是以短期、突发为导向的内部集群采购模式——大多数合同期限不足一年。这与 NVIDIA 的策略形成鲜明对比：NVIDIA 采用常驻的、多年期的集群部署，赋予工程师更大的自由去探索创意与高风险项目，而无须财务管控人员持续盯着。例如，NVIDIA 运营着庞大的内部 GPU 资源，包括拥有数千颗 GPU 的 A100 Selene 集群、两个 EOS 集群（一个 4,600 颗 H100，另一个 11,000 颗 H100），以及数十个规模在 64-1024 颗之间的 H100/H200 小集群——既有本地部署，也有从 OCI、Azure、CoreWeave、Nebius 等云服务商租用。今年他们还将拿到规模庞大的 GB200 集群。上述数字还不包括他们为 DGX Cloud 所拥有的数十亿美元集群。

AMD 当前的设置——每个 GPU 时数实际上都直接挂钩损益考量——抑制了必要的探索性项目与战略性长期开发。

AMD 必须尽快从目前不足一年的集群策略，转向签署长期、多年期的承诺，并且应当专门投资一个由 10,000+ 颗旗舰级 GPU 组成的大型集群。这样的投入将展示 AMD 对每一代 GPU 的投入决心，正如 NVIDIA 对每一代 GPU 都提供跨越多年的稳健长期软硬件支持。现有的突发模式正在严重损害 AMD 的内部开发努力、限制创新潜力。转向持续的多年期投资方式，才能让 AMD 有效地追求战略性创新与竞争优势。

手握超过 50 亿美元的可用现金储备，AMD 显然具备转向更具战略性的长期投资方式的财务弹性。当前对季度盈利的短视专注，正在削弱 AMD 未来的创新与领导能力。对 GPU 各代际作出多年期承诺将显著增强长期支持，使 AMD 的内部能力更贴近客户期望。这一战略调整还将让客户对 AMD 持续支持与创新的承诺感到安心，从而强化市场信心与长期伙伴关系。

## ROCm 缺乏一等公民级的 Python 支持

过去 12 个月，让整个 CUDA 生态在 Python 上获得一等公民体验一直是 NVIDIA 的头等要务，而且正是 Jensen 本人亲自介入并主导这项工作。2010 年代，Jensen 最先意识到投资让 CUDA 软件在 AI 上变得伟大终将获得回报。2025 年，Jensen 的关键洞见是认清 AI 的事实标准语言就是 Python，把 NVIDIA 现有 C++ CUDA 栈的每一层都带入 Python 世界将带来高投资回报。在今年的 GTC 上，NVIDIA 发布了数十个 Python 库——从 nvmath-python 这类 GEMM 库，到 cuda.binding 的 cuBLASLt 绑定，再到 cuTile、Warp、Triton、CuTe Python 等内核 DSL。遗憾的是，ROCm 各库的 Python 支持与 NVIDIA 相去甚远。**NVIDIA 在栈的每一层都有 Python 接口，AMD 没有做到这一点。**

![](https://substack-post-media.s3.amazonaws.com/public/images/eddb5bf0-2350-4224-9805-270fd7257b65_1024x557.png)
*来源：NVIDIA*

通过在 CUDA 中把 Python 作为一等公民支持，最终用户可以花更少时间获得同等性能，或者花同样时间获得更佳性能。CUDA Python 实际上把"应用性能 vs. 优化投入时间"的帕累托前沿曲线整体推移。

![](https://substack-post-media.s3.amazonaws.com/public/images/632dac3f-4f52-4e0f-8ef6-86146a0046f5_1024x596.png)
*来源：NVIDIA*

举一个简单的例子：过去，开发者若想以自定义 epilogue 调用 cuBLASLt，需要编写 C++ 扩展再通过 Pybind 绑定到 Python，过程有些绕，还增添了一层 ML 工程师需要操心的间接性。如今用 nvmath-python，同样的任务只需 **3 行 Python 代码即可完成并自动调优。这项任务已从 30 分钟的活儿变成 2 分钟的活儿。**NVIDIA 的这些 Python 库绝非半成品绑定，而是把性能放在首位的一等公民实现。

![](https://substack-post-media.s3.amazonaws.com/public/images/bcb30bba-d5bd-4708-b3f3-c7afaecec424_1024x547.png)
*来源：NVIDIA*

再举一例：借助 cuda.cooperative 设备侧库，现在可以通过 Python 接口访问"光速级"（speed of light）CUDA 预置算法，例如 block reduce。这一级别的性能过去只能通过 [CUB](https://docs.nvidia.com/cuda/cub/index.html) 在 C++ CUDA 中获得。

![](https://substack-post-media.s3.amazonaws.com/public/images/52432d38-3103-4617-ab33-b1f06c0c23c6_1024x559.png)
*来源：NVIDIA*

对于想要 1:1 Python 绑定而非更高级 Pythonic 库的最终用户，NVIDIA 也通过 cuda.binding 与 cuda.core 提供了这种选择。**NVIDIA 在栈的每一层都有 Python 接口，AMD 没有做到这一点。**

![](https://substack-post-media.s3.amazonaws.com/public/images/92ec8da0-6bde-48e4-9f8a-f3e04cc848b9_1024x614.png)
*来源：NVIDIA*

AMD 最近为 [AITER](https://github.com/ROCm/aiter)（相当于 cuDNN-python）推出了 Python 接口，并支持 OAI Triton 用于内核编写，但对于栈的其余各层，ROCm 没有可比产品，甚至还没开始考虑提供一等公民级的 Python 体验。

## Python GPU 内核编写 DSL

在 GTC 2025 上，除了首发整套 Python CUDA 库，NVIDIA 还发布了 Python 内核编写 DSL——即 Python CuTe 4.0、cuTile Python 与 Warp。这还是叠加在 Nvidia 现有 Triton DSL 支持之上的！**在 Python 内核 DSL 领域，AMD 匮乏且缺乏竞争力——以至于 Nvidia 的多个团队如今已凭借多种已公开发布的 NVIDIA DSL 相互竞争**。目前 NVIDIA 已有五种不同的 Python DSL（OAI Triton、CuTe Python、cuTile Python、Numba、Warp），内部还有更多尚未公开发布的在研项目。

按抽象单元划分，Python 内核 DSL 可分为两类。在基于线程（thread-based）的语言中，程序员描述单线程行为；而在基于分块（tile-based）的语言中，程序员描述的是对矩阵分区的操作。

CuTe Python 是 NVIDIA 推荐的路径，用于在基于线程的 Python 内核 DSL 中编写"光速级"内核。它提供低层原语作为自定义内核的构建模块，并使用强大的抽象 cuTe（CUDA Tensor）来描述数据与线程布局。CUTLASS Python 的 API 设计基于 CUTLASS，新用户可以借助 CUTLASS 详尽的概念与用法文档快速上手。AMD 虽有对标 CUTLASS 的 C++ 库 CK（Composable Kernel），但其概念与用法文档相对稀少且不清晰。CK 的高层接口将迎来 Python 接口，但其对标 CuTe 的 atom 层则没有任何在研计划。

**更重要的是，AMD 目前总体上没有任何面向基于线程内核编程的 Python DSL，而这正是达到光速性能所必需的。**

![](https://substack-post-media.s3.amazonaws.com/public/images/9f42354a-d080-4dc1-8112-433fd04cfdbc_1024x400.png)
*来源：NVIDIA*

在基于分块、基于 SIMT 以及分块/SIMT 混合的 Python 内核编写 DSL 方面，NVIDIA 在 GTC 2025 发布了 cuTile。cuTile 的目标不是 100% 光速性能，而是以 10% 的内核编写时间换取 98% 的光速性能。**用 cuTile 编写内核相当容易。遗憾的是，AMD 没有任何混合 SIMT/分块的 Python 内核 DSL 产品。**

![](https://substack-post-media.s3.amazonaws.com/public/images/6f6b19e6-4f67-43a6-a1fa-d8c5dacb3927_1024x542.png)
*来源：NVIDIA*

Triton 在张量核心时代普及了基于分块的编程模型——在这个时代，有效的抽象层级是 Tile 而非单线程。除 cuTile 分块 DSL 外，Nvidia 将继续全面支持 Triton 的分块 DSL。

![](https://substack-post-media.s3.amazonaws.com/public/images/3fc3d1cd-10f9-462e-9f5b-1651f860952b_1024x637.png)
*来源：Nvidia*

面向可微分仿真 AI，NVIDIA 发布了 Warp Python DSL。Warp 是分块与 SIMT 混合的编程模型，适合编写仿真与几何处理。相对 cuTile，Warp 的巨大优势在于可自动微分（automatically differentiable），这在仿真中极有用处，可以自动生成反向传播。**AMD 同样没有任何这种混合 SIMT/分块、可微分的 Python 内核 DSL 产品。**

除新发布的各 Python DSL 外，Nvidia 仍全面支持 OpenAI Triton Python DSL。Triton 的主要维护者是 OpenAI，其使命是构建安全的 AGI。事实上，在 [SemiAnalysis Blackwell PTX Hackathon 2025](https://semianalysis.com/2025-hackathon-eol/) 上，**Triton 的 OpenAI 首席维护者 Phil Tilet 甚至说过"AGI 不会来自快 10% 的矩阵乘法"**——这正是 Triton 决定功能优先级时围绕的精神。因此，如果 AI 芯片厂商想要最快的 AI 芯片，Triton 并非唯一应当支持的平台。我们认为，AI 芯片厂商在支持其他 Python DSL 的同时，仍应全面支持 Triton。

![](https://substack-post-media.s3.amazonaws.com/public/images/5ef71117-a094-4525-94b4-047e37aa43a1_1024x196.png)
*来源：OpenAI、SemiAnalysis Blackwell PTX Hackathon*

这一立场导致了目标错位：OpenAI Triton 并不在乎达到绝对的光速峰值性能，而 Nvidia、MTIA、MAIA、AMD 等 AI 芯片阵营却非常在乎在其内核语言中获得峰值性能。

Nvidia 的 Triton 性能尚远未接近光速，而 AMD 的 Triton 性能离光速更远。AMD 需要大力招聘并投资，让 Triton 性能大幅增强，同时支持/自创其他 Python 内核 DSL。

AMD 有一个实验性内核语言 [wave](https://github.com/iree-org/iree-turbine/tree/main/iree/turbine/kernel/wave)，采用基于 warp 的编程模型，但似乎仍处于非常早期的阶段，也没有获得公司层面的全力支持。这与 cuTile、CuTe、Warp 相差甚远——后者全都得到 Jensen 与 Nvidia 的全力背书，而 Nvidia 正全力以赴让 CUDA Python 变得伟大。此外，考虑到行业正转向基于 warp-group 的 MMA 硬件与 2-CTA MMA 硬件而非基于 warp 的 MMA，基于 warp 的内核 DSL 是否提供了恰当的抽象层也存疑。

## AMD RCCL 与 NVIDIA NCCL 之间不断拉大的差距

集合通信库对 AI 训练与推理极其重要，因为它们让多颗 GPU 协同处理同一工作负载。Nvidia 的集合通信库叫 NCCL，AMD 的库则是对 NCCL"ctrl+c, ctrl+v"式的复刻分支（fork），名为 RCCL。自我们在 [2024 年 12 月的文章](https://semianalysis.com/2024/12/22/mi300x-vs-h100-vs-h200-benchmark-part-1-training/)中分享对 RCCL 的看法以来，RCCL 团队取得了些像样的进展。在 MI300X 量产超过一年之后，RCCL 团队如今终于在 MI300X 上支持了 [LL128 协议](https://github.com/ROCm/rccl/pull/1549)。这是重大改进，但相比之下，Blackwell 第一天就支持全部三种集合通信协议（SIMPLE、LL、LL128）。

此外，RCCL 终于支持了轨道优化树（rail-optimized trees），通过减少经由 spine 交换机的流量来提升网络性能，从而减少路径冲突。这一特性 NCCL 早已支持了无数年。

![](https://substack-post-media.s3.amazonaws.com/public/images/ac743225-694a-4afe-b80b-51d61dc9f491_861x1024.png)
*来源：Github*

**尽管 RCCL 取得了一些像样的进展，但由于 [GTC 2025 公布的 NCCL 新改进与新特性](https://www.nvidia.com/en-us/on-demand/session/gtc25-s72583/)，NCCL 与 RCCL 之间的差距仍在显著拉大。**RCCL 团队需要更多正经资源的接入，比如大型计算集群，才能追上 NCCL。应当给他们一个至少 1,024 颗 MI300 级 GPU 的常驻集群的独占使用权。此外，AMD 领导层需要投资大幅提高 RCCL 工程师的 RSU 薪酬，以便在这个最关键软件库之一的领域吸引并留住核心人才。

由于 AMD 的 RCCL 库是 Nvidia NCCL 的原样复刻分支，NCCL 2.27 与 2.28 的大规模重构将持续扩大 CUDA 护城河，迫使 AMD 的 RCCL 团队耗费数千工程时把 Nvidia 的重大重构同步进 RCCL。当 AMD 工程团队被迫花数千工程时同步这些变更时，Nvidia 却会把这段时间用于继续推进集合通信软件栈与算法的前沿。这种动态使得 AMD 几乎不可能在维持 RCCL 现有开发的同时追平 NCCL，更遑论超越 NCCL。

AMD 表示，他们目前正处于从零重写 RCCL、摆脱 NCCL 分支身份的规划阶段。

在他的 GTC 2025 演讲上，我们半开玩笑地问 NCCL 掌门人 Sylvain Jeaugey：本着开源开发的精神，他是否愿意向 RCCL 伸出援手——毕竟它目前基本上是个复制粘贴库。

他回绝了我们的提议：

*SemiAnalysis：鉴于即将发布的 2.28 有如此大规模的重构，Nvidia 会不会向 AMD 团队的 RCCL 分支提供支持？
Sylvain：我们也会帮 RCCL 迁移过去吗？我不这么认为——通常我们并不参与那边的开发。
来源：[Nvidia](https://www.nvidia.com/en-us/on-demand/session/gtc25-s72583/?start=2025) – 时间戳 33:48*

在这场演讲中，Sylvain 还公布了即将到来的大重构中的许多 NCCL 新特性，包括在 NCCL 中原生支持对称内存（symmetric memory），以及运行速度快得多、占用 SM 更少的新算法——从而把更多 SM 留给计算。

![](https://substack-post-media.s3.amazonaws.com/public/images/54bd2315-6097-424a-b08f-ae4242ef30a0_1024x609.png)
*来源：NVIDIA*

[PyTorch 推出了 SymmetricMemory API](https://dev-discuss.pytorch.org/t/pytorch-symmetricmemory-harnessing-nvlink-programmability-with-ease/2798)，让用户能轻松驾驭多 GPU 纵向扩展的可编程性，并[用 CUDA 或 Triton 编写集合通信或计算/通信融合内核](https://github.com/yifuwang/symm-mem-recipes)。以往编写多 GPU 计算/通信融合内核需要大量工作，而借助 PyTorch SymMem，所需工作量已大幅减少。one-shot 与 two-shot 集合通信等高性能推理内核，以及 all-gather 融合矩阵乘内核，现在都可以方便地用 SymmetricMemory 编写。

![](https://substack-post-media.s3.amazonaws.com/public/images/5e1f7b17-388f-49bc-8739-54be3d68c5ed_1024x567.jpeg)
*来源：PyTorch*

该特性在 NVIDIA GPU 上已可用 8 个月，而 AMD GPU 仍不支持。AMD 表示，将在 2025 年第二季度落地对 PyTorch SymmetricMemory API 的初步支持。

![](https://substack-post-media.s3.amazonaws.com/public/images/c5748b2c-13ab-4f69-83b1-fc230f3f14b0_831x1024.png)
*来源：PyTorch、YiFu*

在即将发布的 2.27 版本中，相同消息大小下 allreduce 的规约量降低 4 倍，并在消息大小小 4 倍时仍达到相同的算法带宽。

![](https://substack-post-media.s3.amazonaws.com/public/images/d54dcf51-7427-410a-8708-9f57626d7447_1024x620.png)
*来源：NVIDIA*

在即将发布的 2.28 版本中，NCCL 提供设备侧 API，让最终用户能轻松编写自定义通信/计算融合内核。

![](https://substack-post-media.s3.amazonaws.com/public/images/c51b21f2-0ab0-461c-8dee-0b91070ab7f8_1024x619.png)
*来源：NVIDIA*

即将发布的 NCCL 2.28 还将在 InfiniBand 与 RoCEv2 以太网上同时支持 [GPUDirect Async](https://developer.nvidia.com/blog/improving-network-performance-of-hpc-systems-using-nvidia-magnum-io-nvshmem-and-gpudirect-async/)（IBGDA）。目前，NCCL 与 RCCL 中横向扩展通信的控制流由一个 CPU 代理负责。尽管数据流不经过 CPU，但控制流经由 CPU 仍限制了实际达到的性能。借助 NVIDIA NCCL 2.28 与 IBGDA 的集成——RoCEv2 与 InfiniBand 均支持——控制流由 GPU 发起、不经 CPU，从而在中小消息大小上为 all2all 及基于 all2all 的算法带来更好性能。

另一个目前仅 Nvidia 提供的特性是用户缓冲区注册（user buffer registration）。该特性避免在用户张量与 NCCL 内部缓冲区之间产生额外拷贝，有助于减少集合通信所需的 SM 数量并缓解内存压力，带来 5-20% 的端到端训练提升。

![](https://substack-post-media.s3.amazonaws.com/public/images/5329093c-48c5-485e-8f1e-1370e09cfb23_1024x576.png)
*来源：NVIDIA*

大多数有经验的 ML 工程师都见过可怕的 NCCL_TIMEOUT/RCCL_TIMEOUT 或 NCCL/RCCL 卡死。NVIDIA NCCL 支持 [ncclras](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting/ras.html)，可以简化这类问题的调试。遗憾的是，RCCL 目前不包含任何有助于调试的特性。

![](https://substack-post-media.s3.amazonaws.com/public/images/7fa2ea5c-a6ee-4a40-93b2-fc5089973420_1024x571.png)
*来源：NVIDIA*

## 基础设施软件的进步没那么快

过去四个月，AMD 在其软件基础设施层（即 Kubernetes、SDC 检测器、健康检查、SLURM、Docker、指标导出器）上取得了有意义的进展，但进步速度远赶不上 AMD 机器学习库的进步速度。

直到七个月前，AMD 还完全没有 GPU 指标导出功能，这意味着集群运营者无法对其 GPU 建立可观测性。尽管 ROCM 自称开源生态，AMD 的 GPU 指标导出器却一直不开源——直到 SemiAnalysis 就此与 AMD 高管交涉，敦促他们以紧迫感践行其宣称的"开源"生态承诺。

所幸，经过多次跟进，AMD 终于开源了其 GPU 导出器。请注意，该导出器仍在开发中，许多特性仍缺失，尚未与 NVIDIA 的 GPU 开源指标导出器拉平。例如，AMD 的 GPU 导出器目前仍不支持矩阵核心活动（matrix core activity）、CU 占用率（CU occupancy）或 CU 活跃度（CU active）指标。这些是衡量工作负载表现极其重要的代理指标。AMD GPU 导出器目前唯一的利用率指标是 GPU_UTIL，而[大多数有经验的 ML 工程师都知道，无论 Nvidia 还是 AMD 的 GPU，它实际上根本没有衡量利用率](https://x.com/memorypaladin/status/1817689501113979357)。

[正如我们 12 月的 AMD 文章所述](https://semianalysis.com/2024/12/22/mi300x-vs-h100-vs-h200-benchmark-part-1-training/#amd%e2%80%99s-forked-libraries)，与 Nvidia 的用户体验相比，AMD 的 Docker 用户体验极其糟糕。AMD 已承认这一短板，并告诉我们正在着手解决。他们表示将在本季度晚些时候公布相关路线图。

![](https://substack-post-media.s3.amazonaws.com/public/images/936ac9c8-0ea8-4b8a-a7bf-a6197eaafdbd_1024x377.png)
*来源：SemiAnalysis*

与 Nvidia 栈上的体验不同，AMD 栈上 Slurm+Container 的现状令人失望。[在 Nvidia 上配合开源的 pyxis Slurm](https://github.com/NVIDIA/pyxis)，通过 Slurm 启动容器只需运行"srun –container-name=pytorch"这么简单。相比之下，在 AMD 上工作必须经过一套极其繁琐、层层间接的流程。

想到 AMD 所有内部 AI 工程师都在以这种方式将 SLURM 与容器搭配使用，看到所需的间接层次之多、当前 AMD Slurm+Container 用户体验之差，实在令人痛心。

![](https://substack-post-media.s3.amazonaws.com/public/images/61e5a9a2-e3e6-4c85-8417-44ecb1f7d863_1024x575.png)
*来源：GitHub、AMD*

我们已多次建议 AMD 优先解决这一问题，出钱聘请 SchedMD（Slurm 的维护者）的咨询服务，专注打造一等公民级的 Slurm+容器体验。迄今为止，我们尚未看到 AMD 计划何时修复此问题的具体时间表或路线图。

此外，Nvidia 的数据中心管理工具（DCGM）已直接集成 NVVS（Nvidia Validation Suite），运行诊断只需"sudo dcgmi diag -r <diag_level>"一条命令。相比之下，AMD 的 RVVS（ROCm Validation Suite）与其数据中心工具（RDC）相互独立，逼得最终用户再下载一个库。我们建议 AMD 把 RVVS 集成进 RDC，让用户体验像 Nvidia 的 DCGM 一样简单。

另外，AMD 的用户体验与验证覆盖面也不如 DCGM。[Nvidia 的 DCGM 采用标记区分不同级别（r1、r2、r3、r4）](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html#run-levels-and-tests)，而 AMD 的 NVVS 没有任何此类标记。

![](https://substack-post-media.s3.amazonaws.com/public/images/aa8ee03d-de4a-4608-a916-8aec310a78fb_1024x504.png)
*来源：NVIDIA*

## AMD 缺失分离式预填充推理与 NVMe KV 缓存分层

AMD 目前缺乏对许多推理特性的支持，例如分离式预填充（disaggregated prefill）、智能路由（Smart Routing）与 NVMe KV 缓存分层。分离式服务多年来一直是行业标准，上个月 NVIDIA [开源了分布式推理框架 Dynamo](https://github.com/ai-dynamo/dynamo)，进一步普及了分离式服务。分离式预填充把预填充阶段与解码（decode）阶段拆分到不同的 GPU 上。就连 Google 也推出了自己的[分离式推理框架](https://cloud.google.com/ai-hypercomputer/docs/workloads/pathways-on-cloud/multihost-inference#disaggregated_inference)。

![](https://substack-post-media.s3.amazonaws.com/public/images/f4244b1a-2acc-4edb-9ee8-c041950ae28a_1024x649.png)
*来源：北京大学*

NVIDIA Dynamo 的 Smart Router 在多 GPU 推理部署中，把每个 token 智能地路由到两个可用实例。对预填充阶段而言，这意味着确保传入 token 均匀分布到服务预填充的不同 GPU 上，避免预填充阶段任何特定专家（expert）出现瓶颈。

同样，在解码阶段，重要的是确保序列长度与请求在服务解码的 GPU 之间分布均衡。对于流量更集中的专家，也可以由 Dynamo 提供的 GPU Planner 加以复制，以帮助保持负载均衡。

该路由器还能在服务模型的各个副本之间做负载均衡——这是 AMD 的 vLLM 与许多其他推理引擎都不支持的。

![](https://substack-post-media.s3.amazonaws.com/public/images/77ae5735-0828-4180-93c9-312b9d8c3b22_1024x611.png)
*来源：NVIDIA*

Dynamo 的 GPU Planner 是预填充与解码节点的自动扩缩器，会随一天中自然出现的需求波动拉起额外节点。它可以在预填充与解码节点上，对 MoE 模型中的众多专家实现一定程度的负载均衡。GPU Planner 会为高负载专家拉起额外 GPU、提供更多算力，还能按需在预填充与解码节点之间动态重新分配节点，进一步最大化资源利用率。

它还支持改变用于解码与预填充的 GPU 比例——这对 Deep Research 这类场景尤其有用：这些应用需要审阅海量上下文、却只生成相对少量的内容，因此需要的预填充多于解码。

![](https://substack-post-media.s3.amazonaws.com/public/images/0cf5891f-e6cd-4808-a98d-69d46d8ae7f9_1024x554.png)
*来源：NVIDIA*

NVIDIA Dynamo 的 KV-Cache Offload Manager 把先前用户对话产生的 KV 缓存保存到 NVMe 存储而非直接丢弃，从而让预填充的整体执行更为高效。

当用户与 LLM 进行多轮持续对话时，LLM 需要把对话中早先的问题与回答纳入考量，将其也作为输入 token。在朴素实现中，推理系统会丢弃原本用于生成那些早先问答的 KV 缓存，这意味着这些 KV 缓存必须重新计算，重复同一批运算。

而借助 Dynamo 的 NVMe KVCache 卸载特性，当用户暂时离开时，KV 缓存可以卸载到 NVMe 存储系统，直到用户回到对话。当用户在对话中提出后续问题时，KV 缓存可以迅速从 NVMe 存储系统取回，免去了重新计算 KV 缓存的需要。

这释放了预填充节点的容量去承接更多流入流量，或者反过来可以缩减所需的预填充部署规模。用户体验也会大幅改善——首 token 时间（time to first token）更快，因为取回 KV 缓存所需的时间远少于重新计算。

![](https://substack-post-media.s3.amazonaws.com/public/images/db44fab1-aabf-4e48-b3fd-8be71401570d_1014x683.png)
*来源：NVIDIA*

随着 RLVR（基于可验证奖励的强化学习）与带工具调用的多智能体系统日益普及，这些 KVCache 卸载特性将变得越来越重要。

## 对 AMD 建议的汇总

**我们真心希望看到 Nvidia 之外出现又一位有力的竞争者，也愿意帮助 AMD 走到那个位置**。过去四个月，AMD 进步巨大，但要与 Nvidia 竞争，仍需做出许多改变。本文前文已向 Lisa Su 与 AMD 领导团队详细列出我们的建议，在此汇总如下：

1. AMD 需要保持（乃至强化）他们的紧迫感，才有一丝与 NVIDIA 拉平的机会。
2. AMD 领导团队最大的盲点，是其 AI 软件工程师总薪酬（基本工资 + RSU + 奖金）偏低，原因是薪酬结构错误地对标半导体公司，而非那些擅长 AI 软件的公司。我们已讨论我们的建议如何帮助把工程师薪酬与 AMD 的成败更紧密地对齐。**我们坚信，如果 AMD 不大幅提高 AI 软件工程师薪酬，AMD 将持续败给 Nvidia。**
3. 我们建议 AMD 重金投入，在 ROCm 栈的每一层打造 Python 接口，而不只是 Python 内核编写 DSL。
4. AMD 需要重金打造一支 20 人以上的开发者关系工程师团队，举办线下活动并与社区更深入地互动。
5. 与 NVIDIA GTC 不同，AMD 不举办任何以开发者为主题的大会，只办产品发布主题演讲活动，例如"Advancing AI"。我们建议 AMD 举办线下的"ROCm 开发者大会"。
6. NVIDIA 已发布 [Dynamo 分离式预填充推理框架](https://github.com/ai-dynamo/dynamo)和[其 NIXL 推理 KV 缓存分层库](https://github.com/ai-dynamo/nixl)。AMD 对分离式预填充和 NVMe KVCache 分层都没有一等公民级支持。他们需要快速推进，否则将在推理上掉队。
7. AMD 应给 ROCm 集合通信工程师一个至少 1,024 颗 MI300 级 GPU 的常驻集群，供该团队独占使用。这将大大帮助 RCCL 追赶 NCCL。
8. Nvidia 在其芯片规格中标高了 TFLOP/s，但 AMD 标得更高。[甚至在 AMD 自己的博客中，他们也承认其宣传 TFLOP/s 与实际可达性能之间的差距明显更大](https://rocm.blogs.amd.com/software-tools-optimization/Understanding_Peak_and_Max-Achievable_FLOPS/README.html)，超过用户在 NVIDIA 上可能遇到的水平。
9. AMD 每当公开发布新的自研模型训练成果时，都应公布模型算力利用率（MFU）与 TFLOP/s/GPU。[AMD 目前没有这样做](https://rocm.blogs.amd.com/artificial-intelligence/introducing-instella-3B/README.html)。我们已多次询问 AMD 其 MFU，但至今未得到令人满意的回答。这难免让人猜测其 MFU 相当低。
10. 与 [Nvidia 的 Pyxis 方案](https://github.com/NVIDIA/pyxis)相比，AMD SLURM 对容器的一等公民支持根本不存在。AMD 应投资 [SchedMD（SLURM 的维护者）](https://www.schedmd.com/)的咨询服务，帮助 AMD SLURM 的容器体验拉平 NVIDIA。
11. AMD 应开源并公开其所有 ROCm 库（HipBLASLt、Sglang、vLLM、TransformerEngine 等）的 CI/CD 与仪表盘。[目前其机器学习库中唯一可公开访问的 ROCm CI 只有 PyTorch](https://hud.pytorch.org/benchmark/compilers)。
12. 目前 AMD 的内部集群按短期突发模式租用。但由于算力需求与可用供给相匹，这意味着许多开发项目和工作无法开展。工程师无法说服容量把关者提供突发算力来开展研究的情况屡有发生。症结在于每个 GPU 时数都实际挂着一个损益。Nvidia 的情况完全不同：其内部集群是常驻且多年期的。这给了 Nvidia 工程师很大的自由度，可以在集群空闲容量上发挥创意、做高风险项目，而没有会计在旁边盯着。**AMD 手握超过 50 亿美元现金，有能力在内部集群上加大投入。**
13. AMD 大多数内部集群租期不足一年。这意味着到 2027 年、客户仍在使用 MI300 时，AMD 内部的 MI300 数量会因合同到期而变得非常少，导致对"老一代"GPU 的长期支持很差。AMD 应把内部集群采购策略改为多年期承诺，从而实现对每代 GPU 的长期支持。**如果 AMD 连内部集群都不愿对每代 GPU 作出多年承诺，凭什么要求客户对 AMD GPU 作出长期持有的承诺？**
14. AMD 的软件基础设施层（即 Kubernetes、SDC 检测器、健康检查、SLURM、Docker、指标导出器）过去四个月有所进步，但进步速度远慢于 AMD 机器学习库的进步速度。我们建议 AMD 高管研究向 AMD 的 AI 软件基础设施层投入更多工程资源。
15. Jensen 一直在向学术实验室捐赠 DGX B200 主机，例如 [Berkeley Sky lab](https://x.com/vllm_project/status/1893001644037566610)、[CMU Catalyst Research Group](https://x.com/scsatcmu/status/1912910889566490821?s=46) 和[许多其他大学实验室](https://x.com/haoailab/status/1914402516420440072)。我们建议 AMD 也支持学术生态。寄出机器、再贴出博士生们咧嘴笑着一台崭新 AMD 主机的合影，对 AMD 市场营销而言是极其轻松的胜利。

## 对 NVIDIA 的建议

过去几年，NVIDIA 领导层内部一直把[华为](https://semianalysis.com/2025/04/16/huawei-ai-cloudmatrix-384-chinas-answer-to-nvidia-gb200-nvl72/)视为[最有概率与 NVIDIA 竞争](https://semianalysis.com/2025/04/16/huawei-ai-cloudmatrix-384-chinas-answer-to-nvidia-gb200-nvl72/)的公司。鉴于 AMD 的快速进步与紧迫感，我们认为 NVIDIA 也应把 AMD 视作主要竞争对手。如果他们想继续当市场领导者，我们向 Jensen 提出以下建议：

1. 继续快速扩张 API 表面积，推出有用的新特性。只要 NVIDIA 扩张 API 表面积的速度快于 AMD 复制/移植并适配 ROCm 的速度，NVIDIA 就将继续领跑。近期 CUDA Python 全栈的一系列发布，就是 NVIDIA 大规模扩充 API 表面积、增加有用新特性的绝佳例证。
2. 对许多开发者而言，在 Nvidia 消费级 GPU 上开发是进入更广阔 CUDA 生态的入口。遗憾的是，由于 NVIDIA 消费级 EULA 的限制，PyTorch 和大多数其他 ML 库无法在 CI/CD 中托管消费级 NVIDIA GPU，导致 NVIDIA GPU 上的体验欠佳。我们建议 NVIDIA 探索把消费级 GPU 纳入 PyTorch CI/CD 的策略。
3. [NCCL 用户缓冲区注册](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/bufferreg.html)可降低内存压力，从而支持更大批大小（batch size）、减少激活重计算，带来约 5-10% 的性能提升。尽管[已支持与底层 PyTorch API 的基本集成](https://github.com/pytorch/pytorch/pull/133603)，但目前尚未集成到 DistributedDataParallel（DDP）、DTensors、FullyShardedDataParallel（FSDP）等常用 API。我们建议 NVIDIA 把用户缓冲区注册特性集成到整个 PyTorch 栈。
4. 尽管 NVIDIA 的开箱体验优于 AMD，仍有改进空间。[例如，开发者要获得 RMSNorm 的最优性能，需要使用 NVIDIA/apex 库，而 PyTorch 并未开箱提供](https://github.com/pytorch/pytorch/pull/146388)。RMSNorm 是 SOTA 大语言模型中极其常见的一层。我们建议 NVIDIA 与 Meta PyTorch 团队合作，制定将快速 RMSNorm 内核及其他 cuDNN 内核直接集成进 PyTorch 的策略。
5. NVIDIA 需要出资提供额外的 CI 用 H100，让 PyTorch 能为 [TorchInductor Benchmark CI](https://hud.pytorch.org/benchmark/compilers) 启用 H100。连 AMD 都已为该 Benchmark CI 启用了 MI300。
6. 过去四个月，AMD 在让多数基准测试可被社区轻松复现方面做得很出色。例如，[AMD 写了一篇关于如何复现其 MLPerf Inference 5.0 提交的精彩博客](https://rocm.blogs.amd.com/artificial-intelligence/reproducing-amd-mlperf-inference-submission/README.html)。如果 NVIDIA 希望 ML 社区信任其发布的基准结果，我们建议 NVIDIA 每次发布基准结果时都提供可复现说明和一篇解释性博客文章。
7. NVIDIA 相当一部分开源库很不守"开源"精神，每次发布都是一次性代码倾倒（code dump），NCCL 和 CUTLASS 就是例子。我们也看到一些开源库的进步，例如 [trt-llm 转向 GitHub-first 方式](https://github.com/NVIDIA/TensorRT-LLM/pull/2980)。我们建议 NVIDIA 在所有开源库中践行开源精神。
8. 停止宣传[营销性质的"Jensen 数学"2:4 稀疏 FLOPs 规格，收敛未经宣布的双向带宽惯例的使用，以减少整个生态的混乱](https://semianalysis.com/2025/03/19/nvidia-gtc-2025-built-for-reasoning-vera-rubin-kyber-cpo-dynamo-inference-jensen-math-feynman/#jensen-math-changes-every-year)。避免夸大稠密 FLOP/s 规格，转而发布能反映真实世界正常输入分布下可达性能的 FLOP/s 指标，而非基于[不切实际的 [-4, 4] 均匀离散整数分布](https://github.com/NVIDIA/cutlass/blob/main/media/images/cutlass-3.8-blackwell-gemm-peak-performance.svg)的结果。
9. 研究挖角 AMD 中为 [RCCL](https://github.com/ROCm/rccl/graphs/contributors)、[ComposableKernels](https://github.com/ROCm/composable_kernel/graphs/contributors)、[hipBLASLt](https://github.com/ROCm/hipBLASLt/graphs/contributors)、[ROCm/PyTorch](https://github.com/pytorch/pytorch/pulls?q=is%3Apr+is%3Aopen+%5BROCm%5D) 等库做贡献的工程师——方法是[查看 Github 上的贡献者页签](https://github.com/ROCm/rccl/graphs/contributors)，并在 [Github 上搜索 "[ROCm]" PR 标签](https://github.com/pytorch/pytorch/pulls?q=is%3Apr+is%3Aopen+%5BROCm%5D)。

## MI325X 与 MI355X 的客户兴趣

[正如我们一年来反复所言，客户对购买 MI325X 缺乏兴趣](https://semianalysis.com/accelerator-industry-model/)。它本应是 H200 的竞争对手，但 MI325X 直到 2025 年第二季度才开始出货，比 H200 晚了约三个季度，又恰逢 Blackwell 量产。性能单价低得多的 Blackwell 显然是客户的不二之选，因此 MI325X 的发布可谓杯水车薪、为时已晚，AMD 只卖出了少量 MI325。

[我们加速器模型中的需求观点在 2024 年初就追踪到微软的失望，以及整个 2024 年后续订单的缺位](https://semianalysis.com/accelerator-industry-model/)。我们相信，[OpenAI 经由 Oracle](https://semianalysis.com/accelerator-industry-model/) 和[其他几家大客户](https://semianalysis.com/accelerator-industry-model/)对 AMD GPU 重燃兴趣，但依旧没有微软——前提是他们能与 AMD 谈成极为优惠的价格。需要说明的是，MI355X 仍无法与 NVIDIA 机柜级 GB200 NVL72 方案竞争，因为 MI355X 的纵向扩展域（scale-up world size）仍只有 8 颗 GPU，而 NVIDIA GB200 NVL72 的 world size 是 72 颗 GPU。

AMD 对 MI355X 竞争力的宣传，主打它不需要冷板式直冷液冷（DLC）。这在一定程度上确有道理，但颇具讽刺意味的是：AMD 仍在把下一代 MI355X 定位为 Nvidia 上一代"经济舱"产品的竞争对手。由于上述更小的纵向扩展域，AMD 的 MI355X 无法在前沿推理（frontier reasoning inferencing）上与 NVIDIA 旗舰 GB200 NVL72 正面竞争，因此它被定位为与风冷 HGX B200 NVL8 和风冷 HGX B300 NVL16 竞争。

话虽如此，[这一细分产品仍将出货可观的量](https://semianalysis.com/accelerator-industry-model/)。取决于 MI355X 的软件质量与 AMD 愿意的售价，在与 NVIDIA HGX 对比时，MI355X 在每 TCO 性能上有望具备相当的竞争力。对那些无法受益于大纵向扩展域的中小模型来说尤其如此。不过我们认为，在真正受益于大规模分离式部署的推理模型与前沿推理任务、以及最能发挥大型纵向扩展网络的混合专家（MoE）场景下，GB200 NVL72 将在性能和每 TCO 性能上胜出。

下文将讨论我们在 MI355X、MI420X、MI450X、UALink、Infinity Fabric over Ethernet 以及定价方面的观察。
