---
title: "华为 AI CloudMatrix 384——中国对标 Nvidia GB200 NVL72 的答卷"
title_en: "Huawei AI CloudMatrix 384 – China's Answer to Nvidia GB200 NVL72"
subtitle: "中国电力充裕、100% 光互连、0% 铜互连、能效欠佳、每瓦 FLOP 低 2.6 倍、每芯片 14 个收发器、线性可插拔光学（LPO）"
date: 2025-04-16
source: https://newsletter.semianalysis.com/p/huawei-ai-cloudmatrix-384-chinas-answer-to-nvidia-gb200-nvl72
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball", "Myron Xie", "Patrick Zhou", "Ivan Chiam", "AJ", "Christopher Seifel", "Doug"]
tags: ["Hardware Architecture", "Accelerators", "Export Controls"]
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 华为 AI CloudMatrix 384——中国对标 Nvidia GB200 NVL72 的答卷

> 原文：[Huawei AI CloudMatrix 384 – China's Answer to Nvidia GB200 NVL72](https://newsletter.semianalysis.com/p/huawei-ai-cloudmatrix-384-chinas-answer-to-nvidia-gb200-nvl72) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**中国电力充裕、100% 光互连、0% 铜互连、能效欠佳、每瓦 FLOP 低 2.6 倍、每芯片 14 个收发器、线性可插拔光学（LPO）**

华为（Huawei）正凭借其新的 AI 加速器与机柜级架构引发关注。这是中国最新、最强大的国产方案——基于昇腾（Ascend）910C 构建的 CloudMatrix 384。该方案与 GB200 NVL72 直接竞争，在某些指标上甚至比 Nvidia 的机柜级方案更为先进。其工程优势体现在系统层面，而不只是芯片层面，在网络、光学与软件层均有创新。

![](https://substack-post-media.s3.amazonaws.com/public/images/c395d1e6-7a89-4eb5-b54d-10a13df2347e_1080x524.png)
*来源：华为*

华为 Ascend 芯片对 SemiAnalysis 并不陌生，但在[一个系统比微架构更重要的世界](https://semianalysis.com/2023/04/12/google-ai-infrastructure-supremacy/)里，华为正在冲击 AI 系统性能的极限。这里存在取舍，但考虑到出口管制与平淡的国产良率，显然对华出口管制之中仍有更多漏洞可钻。

虽然 Ascend 芯片*可以*在中芯国际（SMIC）制造，但我们要指出：这是一颗全球化芯片——[HBM 来自韩国](https://www.semianalysis.com/p/accelerator-model)，[晶圆主力产出台积电（TSMC）](https://semianalysis.com/accelerator-industry-model/)，制造它的是[来自美国、荷兰、日本的价值数百亿美元的晶圆厂设备（WFE）](https://semianalysis.com/wafer-fab-model/)。我们将深入分析：中国国内生产哪些环节是可行的、哪些属于对出口管制的激进规避，以及为什么美国政府需要聚焦这些关键新领域来限制中国的 AI 能力。

华为在芯片上落后一代，但其纵向扩展（scale-up）方案可以说领先 Nvidia 与 AMD 当前市售产品一代。那么，华为 CloudMatrix 384（CM384）的规格究竟如何？

CloudMatrix 384 由 384 颗 Ascend 910C 芯片组成，通过全互联（all-to-all）拓扑连接。取舍逻辑很简单：Ascend 的数量五倍于对手，足以抵消并反超每颗 GPU 性能仅为 Nvidia Blackwell 三分之一的劣势。

![](https://substack-post-media.s3.amazonaws.com/public/images/ec70db4a-8695-4864-a756-e740da2fece7_794x528.png)
*来源：SemiAnalysis、Nvidia、华为*

一套完整的 CloudMatrix 系统如今可提供**300 PFLOPs 的稠密 BF16 算力，几乎是 GB200 NVL72 的两倍**。再加上**3.6 倍以上的总内存容量**与**2.1 倍的内存带宽**，华为和中国如今拥有了能够胜过 Nvidia 的 AI 系统能力。

更重要的是，CM384 恰好契合中国的强项：国产网络设备产能、用于防止网络故障的基础设施软件，以及随着良率进一步提升、向更大规模域扩展的能力。

其短板在于功耗：为 GB200 NVL72 的 **4.1 倍**，**每 FLOP 功耗差 2.5 倍**，每 TB/s 内存带宽功耗差 1.9 倍，每 TB HBM 内存容量功耗差 1.2 倍。

**功耗上的劣势确实存在，但在中国这并非制约因素。**

## 中国没有电力约束，只有硅的约束

西方常挂嘴边的论调是 [AI 受电力限制](https://www.semianalysis.com/p/datacenter-model)，但在中国情况恰好相反。过去十年，西方把以煤为主的电力基础设施转向更清洁的天然气与可再生能源发电，并配套提升人均能源使用效率。中国则相反：生活水平提升与持续的重资产投资，意味着庞大的发电需求。

![](https://substack-post-media.s3.amazonaws.com/public/images/7b977aa8-9e8b-4996-ac88-6a67c69953c7_1855x598.png)
*来源：SemiAnalysis Datacenter Model*

其中大部分仍由燃煤驱动，但中国也拥有全球最大的光伏、水电、风电装机规模，如今还是核电部署的领跑者。美国则仅仅维持着 1970 年代部署的核电。简而言之，升级并扩充美国电网的能力已经"生疏"；而中国自 2011 年以来——大约最近 10 年——新增了相当于整个美国电网规模的容量。

当相对充裕的电力供给使你不受功耗约束时，放弃功率密度、扩大纵向扩展规模、把光互连纳入设计就是合理选择。CM384 的设计考虑了甚至超出机柜之外的系统级约束，而我们相信，制约中国 AI 雄心的并不只是相对电力可得性这一项。我们认为，华为的方案还有多条继续扩展的路径。

## 中国能造多少 Ascend 910C 与 CloudMatrix 384？

一个常见的误解是华为 910C 完全在中国制造。它的设计确实全部在中国完成，但生产上中国仍严重依赖国外。无论是三星（Samsung）的 HBM、台积电的晶圆，还是美国、荷兰、日本的设备，对外国产业的依赖都不小。

中国最大的代工厂中芯国际虽然拥有 7nm 工艺，但绝大多数 Ascend 910B 与 910C 都由台积电 7nm 制造。事实上，美国政府、TechInsights 等机构已取得 Ascend 910B 与 910C，每一颗用的都是台积电裸片。华为通过另一家公司算能（Sophgo）采购了约 5 亿美元的 7nm 晶圆，从而绕开了禁止其使用台积电的制裁。

![](https://substack-post-media.s3.amazonaws.com/public/images/a1896a04-96ed-4eaa-a0a2-d0a8d818d5c6_927x590.png)
*来源：SemiAnalysis Datacenter Model*

[TSMC 将因这一明目张胆的违反制裁行为被处以 10 亿美元罚款](https://www.reuters.com/technology/tsmc-could-face-1-billion-or-more-fine-us-probe-sources-say-2025-04-08/)，仅为其获利金额的 2 倍。有传言称华为仍在经由另一家第三方公司从 TSMC 获得晶圆，但我们无法核实这一传言。

## 华为的 HBM 获取渠道

先进制程上的对外依赖只是等式的一部分，中国在 HBM 上的依赖更甚。中国尚无法可靠地制造 HBM——长鑫存储（CXMT）距离任何可观的量产爬坡仍有一年之遥。所幸三星伸出了援手：作为中国 HBM 的头号供应商，在 HBM 禁令出台之前，华为借助它已囤积总计 1,300 万颗 HBM 堆栈，足以供应 160 万颗 Ascend 910C 封装。

此外，这些被禁的 HBM 仍在被转出口至中国。HBM 出口禁令专门针对裸 HBM 封装；只要不超过 FLOPS 管制上限，带 HBM 的芯片仍可出货。CoAsia Electronics 是三星 HBM 在大中华区的独家分销商，他们一直在把 HBM2E 发货给 ASIC 设计服务公司智原科技（Faraday），后者再让 SPIL（矽品）把 HBM 与一颗廉价的 16nm 逻辑裸片"封装"在一起。

随后 Faraday 把这种系统级封装（SiP）发货到中国——这在技术层面属于合规——但中国公司随后可以通过拆焊回收 HBM。我们认为他们采用了让 HBM 极易从封装中取出的手法，例如使用强度极低的低温焊料凸点，所以当我们说"封装"时，取的是最宽松不过的含义。

![](https://substack-post-media.s3.amazonaws.com/public/images/73215cc0-7d0f-4900-a0a8-69818f3b5a3e_1648x978.png)
*来源：CoAsia Electronics*

CoAsia 的营收自 2025 年起爆炸式增长，恰好在这些出口管制生效之后——这绝非巧合。

## 中国本土代工厂仍在爬坡

国外生产环节仍然不可或缺，但中国本土半导体供应链的能力已快速提升，且仍被低估。我们一直在就中芯国际与长鑫存储的制造能力发出警示。良率与产出仍是问题，但真正的悬念在于中国 GPU 量产爬坡的长期走向。

中芯国际与长鑫存储都已获得[价值数百亿美元的设备](https://semianalysis.com/2024/10/28/fab-whack-a-mole-chinese-companies/)，而且尽管存在制裁，它们仍在接收[数量可观的独家供应化学品与材料](https://semianalysis.com/2024/10/28/fab-whack-a-mole-chinese-companies/)。

![](https://substack-post-media.s3.amazonaws.com/public/images/d0abc690-f0d0-4459-8b4a-298f89941032_1294x433.png)
*来源：SemiAnalysis*

中芯国际正在上海、深圳、北京扩充先进制程节点产能。今年其产能将达到近每月 50,000 片晶圆，而且由于仍能获得国外设备、加之制裁与执法缺乏实效，扩张仍在继续。若良率进一步提升，华为 Ascend 910C 封装量可以达到可观的量级。

台积电在 2024 与 2025 两年间已交付 290 万颗裸片，足够制造 80 万颗 Ascend 910B 与 105 万颗 Ascend 910C；而如果 HBM、晶圆制造设备、设备维保服务以及光刻胶等化学品未被有效管制，中芯国际的产量还有大幅增长的潜力。

## CloudMatrix 384 系统架构

接下来深入 CloudMatrix 384 的架构、纵向扩展网络、横向扩展（scale-out）网络、功耗预算与成本。

一套完整的 CloudMatrix 系统分布在 16 个机柜中，其中 12 个计算机柜各含 32 颗 GPU。这 16 个机柜的中间是 4 个纵向扩展交换机机柜。为了提升 world size，华为跨多个机柜做纵向扩展，而要做到这一点，华为必须使用光互连。像华为这样把数百颗 GPU 以全互联方式纵向扩展，绝非易事。

![](https://substack-post-media.s3.amazonaws.com/public/images/44796b8e-8a32-4b20-ae39-c4c0f50cefec_2560x884.png)
*来源：SemiAnalysis*

## 与 DGX H100 NVL256 "Ranger" 的相似之处

[早在 2022 年，Nvidia 就发布过 DGX H100 NVL256 "Ranger" 平台](https://pytorchtoatoms.substack.com/p/why-dgx-h100-nvl256-never-shipped)，但最终决定不将其量产——由于所需的大量光收发器与两层网络结构，该平台成本高得离谱、功耗惊人且可靠性欠佳。CloudMatrix Pod 需要数量惊人的 6,912 个 400G LPO 收发器用于组网，其中绝大多数用于纵向扩展网络。

![](https://substack-post-media.s3.amazonaws.com/public/images/803dd96a-d9ca-41d4-8de8-871ac8a3ab03_1430x804.png)
*来源：Nvidia HotChips*

## CloudMatrix384 纵向扩展拓扑估算

以下章节将深入讲解：这 384 颗芯片之间对标 NVLink 的纵向扩展机柜架构、其横向扩展网络、整个系统的功耗预算拆解，以及海量光模块与无铜缆设计所带来的影响。
