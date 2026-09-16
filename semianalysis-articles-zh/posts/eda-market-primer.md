---
title: "EDA 市场入门指南——市场动态、Cadence、Synopsys、Siemens 与中国 EDA 的崛起"
title_en: "EDA Market Primer - Market Dynamics, Cadence, Synopsys, Siemens, China EDA Rise"
subtitle: "EDA 市场规模、份额、商业模式、增长驱动因素、客户结构变迁、竞争动态、IP、硬件、CoT、锁定经济学与颠覆性力量"
date: 2026-05-21
source: https://newsletter.semianalysis.com/p/eda-market-primer
crawled: 2026-09-15
authors: ["Sravan Kundojjala", "Dylan Patel", "Gerald Wong"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# EDA 市场入门指南——市场动态、Cadence、Synopsys、Siemens 与中国 EDA 的崛起

> 原文：[EDA Market Primer - Market Dynamics, Cadence, Synopsys, Siemens, China EDA Rise](https://newsletter.semianalysis.com/p/eda-market-primer) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**EDA 市场规模、份额、商业模式、增长驱动因素、客户结构变迁、竞争动态、IP、硬件、CoT、锁定经济学与颠覆性力量**

当今世上每一颗先进芯片，都是用三家公司提供的电子设计自动化（EDA）软件设计出来的。Synopsys、Cadence 和 Siemens EDA 在「芯片要实现的功能」与「代工厂能制造的东西」之间架起桥梁，把数十亿颗晶体管翻译成可制造的硅片。

三巨头合计占据超过 85% 的市场份额（Ansys 现已并入 Synopsys），而且这个行业已连续十多年每年都实现营收正增长。Synopsys 在 2025 日历年实现 $8B 营收（含 Ansys），Cadence 为 $5.30B，Siemens EDA 估计为 $2.2-2.5B，三巨头在 EDA 工具、半导体 IP、硬件仿真（emulation）设备和仿真（simulation）软件上的合计营收约 $16B。若把较小的厂商和中国 EDA 公司也计算在内，更广义的 EDA+IP 行业总规模达 $18B。

EDA 以 13% 的 CAGR 增长，而半导体研发支出的增速只有 7%。2018 年之后，这 6 个百分点的差距进一步拉大，原因是超大规模云厂商的 AI 芯片项目、硬件仿真设备的经济学以及先进制程节点的验证成本，共同创造了增长快于传统研发基数的 EDA 需求。

EDA 软件工具大约占半导体研发总支出的 9-12%，具体取决于分子和分母各自的统计口径。若把 EDA 厂商的半导体 IP 授权收入计入（Synopsys IP 为 $1.7B，Cadence IP 超过 $0.7B），EDA 厂商收入占半导体研发支出的比例将升至 12-15%。

Synopsys CEO Sassine Ghazi 在 2025 年初指出，在 AI 工作负载复杂性的驱动下，半导体研发强度正从约占行业收入的 6% 向 9% 上升。EDA 厂商从这一趋势中双重受益：一方面，半导体公司在设计上投入更多，他们所切入的研发预算总盘在增长；另一方面，凭借验证强度、AI 工具溢价和制程节点切换定价，他们在这份预算中的份额也在扩大。

我们 EDA 入门系列的[第一部分](https://newsletter.semianalysis.com/p/the-eda-primer-from-rtl-to-silicon)讲解了从 RTL 到签核（signoff）的全流程。第二部分聚焦于让这一流程成为可能的工具背后的生意。第三部分将探讨 AI 如何开始重塑整个芯片设计技术栈。

在本篇（第二部分）中，我们将覆盖：

- 市场规模测算（当前约 $18B，扩展后 TAM 为 $28-31B）、市场份额与工具层面的统治力
- 授权模式：席位（seat）、令牌（token）、ELA、硬件、地区定价差异以及并购的影响
- Synopsys 深度解析：$35B 豪赌 Ansys、近期逆风、先进制程 100% 份额
- Cadence 深度解析：从濒临死亡到 44.6% 的利润率、三层次（three-horizon）战略、2026 年展望
- Siemens EDA：Release 8.0 的教训、Calibre 的封锁地位、Altair 收购
- 竞争动态：2026 年 Cadence 对阵 Synopsys、仿真军备竞赛、IP 战场
- 竞争护城河：锁定架构、王牌工具（franchise tool）、设计启动（design start）与 PDK 优势
- 从 28nm 到 3nm 的设计成本，附客户案例研究（NVIDIA 超 $100M、Apple $170-260M）
- 财务画像：利润率、增长数学与周期韧性
- EDA 公司规模超 $3B 的 IP 业务：授权模式、ARM CSS 与全包式（turnkey）ASIC 设计公司
- 中国：厂商财务、出口管制时间线（2019-2025）、能力差距评估
- 按客户划分的 R 平方（R-squared）锁定强度
- 颠覆风险

### **EDA 存在的意义**

**缩短上市时间。** 一颗用 18 个月而非 24 个月设计出来的芯片，能多锁定 6 个月受保护期的收入。对一个 $200M 的产品来说，这就是 $100M+ 的价值，因为 EDA 将布局、布线和验证任务自动化了，而这些工作若靠工程师人工完成，需要 10-100 倍的时间。

**优化 PPA（性能、功耗、面积）。** 每一颗芯片设计都是「跑多快、耗多少电、占多少硅面积」之间的三方权衡。EDA 工具会运行数千次自动化迭代，在给定制程节点下寻找这三个维度之间的最优平衡。面积改善 5%，意味着每片晶圆多产出 5% 的芯片，在规模效应下节省数百万美元制造成本；功耗降低 10%，则决定了一颗移动 SoC 能否塞进它的热功耗包络。PPA 优化是 EDA 最核心的技术价值主张。

**管理超出人类能力的复杂度。** 一颗现代旗舰芯片包含 500 亿到 2000 亿颗晶体管，在多裸片封装中还会更多。在 3nm，代工厂规定了 25,000+ 条设计规则，每一条都代表一个必须同时满足的制造约束。需要签核的工艺-电压-温度（PVT）角点数量，已从 28nm 时的 5-7 个增长到 3nm 时的 20-30+ 个。手工设计在 65nm 时就已不再可能，自动化优化是先进制程节点上通往可用硅片的唯一路径。

**防止流片失败。** 在先进节点上，一次重新流片（respin）耗资 $50-100M，并使产品推迟 6-12 个月。在投入一套 $40M 的光罩之前证明设计正确，是设计周期中 ROI 最高的活动。

### 谁在购买 EDA 工具

七类客户构成了这个约 $18B 的 EDA+IP 市场。

**无厂芯片设计公司**（NVIDIA、Qualcomm、AMD、Broadcom、MediaTek）是最大的传统客户群体，每名工程师每年在工具、IP 和验证上花费 $80-150K。这些公司设计芯片但没有自己的晶圆厂，EDA 因此成为它们的核心技术基础设施。

**系统公司**如今已占 EDA 需求的 45%（Cadence 数据）。这是增长最快、影响最深远的客户类别。超大规模云厂商（Google、Amazon、Microsoft、Meta）各自运行着多个定制芯片项目，并在先进节点上配备完整的 EDA 工具栈。Apple 在 M 系列、A 系列和基带芯片项目上雇佣了 8,000+ 芯片设计师。Tesla 自主设计 FSD 和 Dojo 芯片。汽车 OEM 和 Tier-1 供应商（Continental、Bosch、Denso）正首次进入芯片设计领域。这些公司是在过去十年内才成为 EDA 客户的，它们的支出是在传统半导体研发基数之外的增量。

**IDM（垂直整合制造商）**（Intel、TI、Analog Devices、Infineon、STMicroelectronics）每名工程师的花费较低（$40-80K），但在设计和制造两侧维持着更大的团队。它们谈判的是覆盖数千个席位的企业级协议，并自研部分内部 IP，从而降低外部授权成本。

**存储器公司**（Samsung、SK Hynix、Micron、Kioxia）使用专门化工具进行 DRAM、NAND 和 HBM 设计。随着堆叠层数和中介层布线要求逐代提升，HBM 验证的复杂度如今已接近逻辑芯片。

**代工厂**（TSMC、Samsung Foundry、Intel Foundry、GlobalFoundries、Rapidus）既是客户也是合作伙伴。它们在量产前 24 个月与 EDA 厂商共同开发 PDK，并指定客户流片时必须使用哪些工具，实际上等于替整个生态系统钦点了特定的签核软件。

**全包式（turnkey）ASIC 设计公司**（Broadcom ASIC 部门、Marvell Custom Silicon、Alchip、GUC）是按单客户计 EDA 支出最大的群体之一。它们代超大规模云厂商客户持有 EDA 授权，并在先进节点上并行运行多个流片项目。仅 Broadcom 的 ASIC 部门，估计每年在 EDA 工具、IP 授权和硬件仿真上的全口径支出就达 $200-500M。

**IP 公司**（ARM、Rambus、Alphawave）购买 EDA 工具授权，用于设计最终随其他公司芯片一起出货的 IP 模块。它们每名工程师的支出较低，因为设计一次即可反复授权。

### 是什么在驱动 EDA 营收增长

四股结构性力量把 EDA 营收增速推到半导体研发增速之上。

**制程节点切换。** 每个新制程节点都会增加设计规则、验证角点和工具需求。3nm 工具的价格是 28nm 工具的 3-5 倍，而客户照付不误，因为通往先进制程硅片没有第二条路。

**验证强度。** 在制造之前证明芯片能正常工作要消耗 60-70% 的设计时间，且以每年 15%+ 的速度增长。仅硬件仿真一项就是一个 $1.5B+ 的市场。每一种新协议（PCIe Gen6、HBM4、UCIe）都会增加验证面，并与既有工作负载复合叠加。

**AI 加速器的扩散。** 超大规模云厂商的定制芯片创造了 $15B-$20B 的新增芯片设计活动，而五年前这些活动几乎不存在。Google TPU、Amazon Trainium、Microsoft Maia、Meta MTIA，每一个都需要先进节点上的完整 EDA 工具栈，且都是在传统研发预算之外的增量。

**锁定带来的定价权。** 95%+ 的客户留存率叠加每年 3-7% 的合同自动上调条款，意味着 EDA 厂商在不增加席位的情况下，每年都能从存量客户身上获得营收增长。2020 年签署的 $10M ELA，到 2025 年续约时变为 $12-14M，工程师人数一个没加。

这一分化始于 2018 年。在那之前，EDA 营收与晶圆厂研发支出是 1:1 同步的。超大规模云厂商的 AI 芯片开发、硬件仿真设备的经济学以及先进节点验证成本，增长都快于设计复杂度本身，把 EDA 营收拉出了研发支出的趋势线。随着 Synopsys 以 $35B 收购 Ansys，可服务市场扩大到 **$310 亿**（$18B EDA+IP + $100 亿仿真 + $30 亿系统软件），这意味着这个寡头格局刚刚吞并了它唯一相邻的市场。

![A graph with blue and orange lines
Description automatically generated](https://substack-post-media.s3.amazonaws.com/public/images/b957535a-34b7-417b-a2a2-74ad5ccaba2f_1600x835.png)

资料来源：SemiAnalysis，公司报告

*Synopsys 与 Cadence 营收（2012-2025）。Synopsys：从 $1.76B 增至 $7.05B（CAGR 约 11%）。Cadence：从 $1.15B 增至 $5.30B（CAGR 约 12%）。十三年间穿越每一轮周期、从未间断的增长。*

### EDA 工具到底在做什么：从 RTL 到硅片的 12-24 个月

EDA 工具通过一条顺序流水线，把抽象的硬件描述转化为可制造的硅片。工程师编写 RTL 代码（Verilog 或 VHDL），综合工具（Synopsys Design Compiler，份额 84-85%）将其映射到代工厂优化过的标准单元上。布局布线（Synopsys Fusion Compiler 或 Cadence Innovus）在 2-3 个月内经过数十轮迭代，安放逻辑门并布设数十亿根连线。

签核分析（Synopsys PrimeTime，份额 90%+，以及 StarRC、Redhawk）在所有 PVT 角点上验证时序、寄生参数和电源完整性。物理验证（Siemens Calibre，份额 85%+）依据代工厂规则执行 DRC 检查，并用 LVS 确认版图与电路一致。代工厂强制要求流片时使用这些签核与验证工具，详见下文竞争护城河一节。流片（tape-out）即把 GDSII 文件交付给代工厂。

![A screenshot of a computer
Description automatically generated](https://substack-post-media.s3.amazonaws.com/public/images/d61bd5de-efb4-4a65-a29c-22e1adc63c62_1600x972.png)

资料来源：SemiAnalysis，公司报告

*从 RTL 到流片的芯片设计流水线。每个阶段的输出是下一阶段的输入；更换其中一个工具，就意味着其下游所有步骤都要重跑。7nm/5nm/3nm 需要 12-24 个月。*

**验证是设计时间和预算的大头所在**，如前文增长驱动因素一节所述。功能仿真（Synopsys VCS 份额 45-50%，Cadence Xcelium 40-45%）要跑数十亿条测试向量。硬件仿真（Cadence Palladium 份额 55-60%，Synopsys ZeBu 35-40%）把设计映射到物理硬件上做全 SoC 验证，一颗旗舰 AI 芯片需要 6-12 个月的连续硬件仿真。这种顺序依赖关系比任何单一工具的优劣都更重要——换了综合工具，就必须重跑布局布线、签核和物理验证。流程本身，就是锁定。

![A screenshot of a graph
Description automatically generated](https://substack-post-media.s3.amazonaws.com/public/images/c0b3895a-770b-45b1-987b-92fd6274d34c_1600x1117.png)

资料来源：SemiAnalysis，公司报告

*设计时间拆分。验证：65%（8-15 个月）。实现：30%（4-7 个月）。物理验证：5%。同等逻辑门数量下，一颗 7nm 芯片所需的验证算力是 28nm 芯片的 10-50 倍。*

## EDA 市场：规模、份额与结构

总市场：$18B（2025 年），到 2030 年增至 $28-30B

![](https://substack-post-media.s3.amazonaws.com/public/images/7da7971f-63fb-47a5-8c6b-66f0b9a0805b_1390x412.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/ea5ecb4d-750a-4d7a-bcb6-f68f4840e2a8_1403x480.png)

其余 10-15% 的份额分散在数十家厂商手中，其中最大的独立厂商是（并入 Synopsys 之前的）Ansys、Keysight（$1.5B，部分业务重叠）和 Zuken（$500M，PCB/IC 封装）。三巨头之外，没有任何厂商在任何一个核心 EDA 品类中拿到超过 5% 的份额。

Renesas 以 $5.9B 收购了 Altium（2024 年），目的是借助 Altium 的 PCB 设计软件推广其元器件产品组合并做物料清单（BOM）优化。Altium 的 PCB 设计业务年营收 $280M，在这一具体品类中位居较大的独立 EDA 厂商之列。

工具层面市场份额（先进节点，7nm 及以下）

![](https://substack-post-media.s3.amazonaws.com/public/images/37bca036-9dcd-4560-8034-0949436d42cf_1475x482.png)

这些份额十年来大体稳定。唯一出现实质性变化的品类是布局布线：2015-2020 年间，Cadence Innovus 从 Synopsys ICC2（IC Compiler II，Synopsys 的旗舰布局布线工具）手中夺走了 10-15 个百分点，随后随着 Synopsys 推出 Fusion Compiler 而趋于稳定。其他所有品类都被锁得纹丝不动。

![A graph of a stock market
Description automatically generated with medium confidence](https://substack-post-media.s3.amazonaws.com/public/images/7b7a8cee-bb4c-4b89-8c1c-13ed46fa0460_1600x831.png)

资料来源：SemiAnalysis，公司报告

*SNPS+CDNS 合计市场份额持续上行，设计复杂度推动市场向两大巨头集中。*

## EDA 授权的真实运作方式：席位、令牌、硬件与续约机器

EDA 定价在刻意保持不透明。厂商不公布价目表，每一单都是单独谈出来的。

### 模式一：按席位授权（传统模式）

一个授权对应一名工程师在同一时间运行一个工具，席特定价目前仍用于小客户和特定工具。

![](https://substack-post-media.s3.amazonaws.com/public/images/cf295c08-92cf-4d3d-b151-680ccc4ec355_902x355.png)

席特定价的规模随人数线性增长，简单直接，但厂商的上行空间也被限制在人数增长这一项上。

### 模式二：令牌/容量授权（现代模式）

令牌把授权与具体席位解耦。客户购买一个计算容量池，任何工程师都可以使用任何工具、从共享池中扣减额度，峰值用量则会被限流或按超额费率计费。

![](https://substack-post-media.s3.amazonaws.com/public/images/6a583865-f1cd-4e66-ac0a-69f5d32043ff_1113x331.png)

令牌授权是 EDA 厂商的增长模式，有四个动因可以解释为什么。

1. **总支出更高** —— 客户按预期峰值用量购买令牌，但平均利用率只有 60-70%。这 30-40% 的闲置就是厂商的纯增量收入。
2. **用量扩张毫无摩擦** —— 增加席位不需要采购审批。工程师直接多用令牌，财务部门按季度看到账单。
3. **AI 工具烧令牌很快** —— Synopsys DSO.ai 和 Cadence Cerebrus 会运行数百次自动化设计迭代，每一次都在消耗令牌。AI 功能可以把单个设计项目的令牌消耗放大 3-5 倍。
4. **云端放大消耗** —— 云端 EDA（Synopsys 上 AWS、Cadence 上 Azure）按计算小时计量。流片冲刺期的突发工作负载产生的用量尖峰，是席位授权模式永远捕捉不到的收入。

从席位到令牌的转移是 EDA 行业最重要的定价动态。Synopsys 在 2024 年投资者日上表示，AI 增强工具的续约为合同基线价值带来 **约 20% 的收入提升**。这一提升来自令牌消耗的增长，而同期人数一个没变。

### 模式三：企业授权协议（ELA）

对于最大的 50-100 家客户，实际的销售单元是 ELA——一种打包提供大部分产品组合访问权限的多年期合同。

![](https://substack-post-media.s3.amazonaws.com/public/images/e4030a44-250d-45a5-8c8f-40496e71e02a_1182x441.png)

这些授权结构是根据厂商公开披露、客户访谈以及季度财报电话会点评拼合还原出来的，因为 Synopsys 和 Cadence 都不公布定价细节。

ELA 制造了四个巩固寡头格局的动态。

5. **捆绑力** —— 次要工具免费可用，让评估竞争对手的动力归零。如果综合、布局布线和签核都在 Synopsys 的 ELA 里，就没有任何理由去评估 Cadence Genus。
6. **用量不透明** —— 财务只看到一笔年度付款，逐工具的 ROI 分析根本无从做起。没人知道在一个 $50M 的 ELA 里，综合工具到底「花」了多少钱。
7. **切换成本放大** —— 退出一个 ELA 意味着把一揽子合同拆开，就 20 多个工具逐一重新谈判。光是行政负担就足以让人打消念头。
8. **信息不对称** —— 厂商掌握着逐工具、逐工程师的详细使用数据，客户通常没有。厂商确切知道哪些工具是命脉，而客户的采购团队不知道。

ARM 的 Flexible Access 计划用的是类似模式：客户支付一笔年费，即可对 ARM 全线 IP 组合进行无限量评估，只在量产时才按芯片颗数触发版税。自 2019 年以来，ARM 的新签授权协议中已有 70%+ 采用这一模式。

### 硬件授权：硬件仿完全是另一门生意

硬件仿真设备（Cadence Palladium、Synopsys ZeBu）遵循的是资本设备的经济学：实体系统、折旧周期、安装团队和散热要求一应俱全。

![](https://substack-post-media.s3.amazonaws.com/public/images/47100909-ce26-41ae-855b-d78e96cbc21e_1443x451.png)

客户一旦装上 $50M 的 Palladium 系统，就有四股力量把它们锁死在硬件的整个生命周期里：为 Palladium API 编写的测试平台（testbench）长达数百万行；工程师专精于 Palladium 特有的调试工作流；5-7 年的折旧周期构成一笔财务承诺；每套系统每年 $3-5M 的软件/维护费用又不断强化与厂商的关系。每套 Palladium 系统，在硬件投资之外，每年还要拉动 $2-3M 的软件授权收入。

### 地区定价差异

![](https://substack-post-media.s3.amazonaws.com/public/images/635bdcc6-620f-476c-9721-9d3797d8de60_1342x388.png)

### 客户合并时会发生什么：EDA 授权的意外之财（与风险）

#### *情形一：主供应商相同（例如双方都用 Synopsys）*

合并后的实体手握两份 ELA，会在续约时合并。规模更大的公司借助量价折扣谈下更低的单席位价格，总支出通常比两份独立协议之和**下降 10-20%**。这一结果对 EDA 厂商短期不利。

#### *情形二：主供应商不同（例如收购方用 Synopsys，被收购方用 Cadence）*

收购方把自己偏好的平台标准化，被收购方的工程师接受再培训，落败厂商的合同在 2-3 年内自然到期出清，因为团队无法在项目中途换工具。赢家拿走席位，输家丢掉席位，总支出大体持平。

#### *情形三：过渡期创造评估窗口*

AMD 收购 Xilinx（$49B，2022 年）时，合并后的实体存在重叠的 EDA 协议，并购倒逼整合。Synopsys 和 Cadence 都为合并后的总合同展开激烈争夺，结果是赢家以竞争性报价抢下整合单子，拿到更大的合同额，但利润率被压缩。

#### *近期的例子：*

![](https://substack-post-media.s3.amazonaws.com/public/images/39bd9732-e251-4f3d-8af0-95f201b91dd8_1306x397.png)

半导体行业整合对 EDA 营收的净影响略微为负，因为独立的客户变少意味着独立的 ELA 变少。但幸存下来的实体规模更大、设计的芯片更复杂、每名工程师花的钱更多。从历史上看，复杂度的增长完全盖过了整合带来的折扣。

#### *不靠增加席位，营收增长从哪里来*

EDA 营收以 12-15% 的 CAGR 增长，而全球半导体设计人员总数只以 3-5% 的速度增长。差额来自六个来源。

![](https://substack-post-media.s3.amazonaws.com/public/images/c33a9d25-ba59-439a-af8f-b808e1c28bfe_1260x433.png)

这份拆分解释了一个关键点：**EDA 厂商在每一次节点切换时卖的都是真正的新能力**——7nm 的多重图形感知布线、2nm 的背面供电（BSPDN）、先进封装节点的 3D-IC 集成。客户获得了新功能，同时也为此支付更高的价格。就单个工具层面而言这个定价是站得住的，但垄断格局决定了这份价值有多少归厂商、有多少留给客户。

#### *客户要为更新付费吗？*

在旧的永久授权模式下，客户为更新支付每年 15-20% 的维护费，而且可以选择不更新、继续用旧版本凑合（下行周期里很多公司就这么干）。在当前的按时段授权（time-based license，TBL）模式下，更新已包含在年费中，不再单独收费。客户永远运行最新版本，而一旦停止付款就意味着完全失去访问权限。这就是为什么从永久授权向 TBL 的转型对厂商如此重要——它消灭了客户在下行周期里使用的「维护费假期」。

如今 Synopsys 和 Cadence 都有 **70-83% 的收入来自按时段/订阅安排，其余来自硬件提前交付、IP 里程碑和永久授权。随着硬件仿真设备销售扩大，提前确认收入所占的份额近年来实际上还在上升。** 从永久授权到时段授权的转型花了十年时间（大约 2005-2015 年），并永久性地改善了这门生意的质量。

![](https://substack-post-media.s3.amazonaws.com/public/images/cd9c1916-0e29-4cca-a85d-21fa996b40a6_1137x338.png)

#### *续约机器*

EDA 营收是一台自我强化的续约引擎，续约的算术很直白。

- Synopsys 在手订单 $11.4B / 年营收 $7.05B = 已提前锁定 1.6 年的收入（FY2025）
- Cadence 在手订单 $7.8B / 年营收 $5.30B = 已提前锁定 1.5 年（FY2025）
- 客户留存率：核心工具每年 95%+，签核和模拟工具 99%+
- 合同自动上调条款：每年 3-7%
- AI 工具带来的续约提升：在自动上调条款之上再加约 20%

2020 年签署 $10M/年 ELA（企业授权协议）的客户，到 2025 年续约时付 $12-14M，推手是合同自动上调、AI 溢价和验证需求扩张。2025 年续约 $10M ELA 的客户，为同样的人数支付 $12-14M，换来的是升级的工具、AI 功能和更大的验证容量。管理层把这包装成价值创造，采购团队看到的是年年涨价——两边都没说错。

![A screenshot of a graph
Description automatically generated](https://substack-post-media.s3.amazonaws.com/public/images/af73600f-2185-4968-81a9-10748aee707c_1600x917.png)

资料来源：SemiAnalysis，公司报告

*EDA 定价能力指数。合同自动上调、AI 溢价与验证扩张，在被锁定的客户基数上复利叠加。*

#### *竞争性定价动态*

![](https://substack-post-media.s3.amazonaws.com/public/images/0e65f091-f7a3-49a0-a477-c9c47a99955f_783x265.png)

大多数 EDA 竞争性评估只是谈判筹码，而非真心要换供应商。典型剧本是：客户宣布启动评估，在位厂商随即报出 15-25% 的折扣，客户照单全收，评估半途而废。Synopsys 和 Cadence 的销售团队已经学会分辨真评估与假评估——真评估中客户会派出专职工程团队并提供真实设计数据，而假评估只是披着技术评估外衣的价格谈判。

#### *按工具品类划分的留存率*

![](https://substack-post-media.s3.amazonaws.com/public/images/fc4f321d-cbcd-4669-b314-0a9a27d295f1_881x331.png)

## Synopsys：$35B 的平台豪赌

*「Fusion Compiler 体现了打破综合、布局布线与签核之间的高墙之后会发生什么。正是那个统一的数据模型给了我们结构性优势。竞争对手可以把工具拼装在一起，但无法复制一个统一的架构。」—— Sassine Ghazi（总裁兼 CEO），Synopsys 2024 年投资者日*

![](https://substack-post-media.s3.amazonaws.com/public/images/1ef7bbd2-8690-4d7b-8467-3e987cca8662_1352x372.png)

Synopsys 的战略是平台最大化：拥有设计流程中的每一个工具、交叉销售 IP、并向相邻的仿真领域扩张。$35B 收购 Ansys（2025 年 7 月完成）把这套逻辑从芯片设计延伸到了覆盖热、结构、电磁和 CFD（计算流体力学，用于散热分析）分析的系统级仿真。

现代芯片不是孤立存在的。一颗 700W 的数据中心 GPU 必须通过复杂的散热方案把热量带走，一颗车规 SoC 必须在振动的发动机缸体上满足 EMC（电磁兼容）要求。传统 EDA 止步于封装边界。Synopsys 与 Ansys 的组合打造出一个从器件到系统的仿真栈：TCAD（Technology Computer-Aided Design，器件物理仿真）负责器件物理，EDA 负责芯片设计，Ansys 负责封装散热、系统 EMC、CFD 和结构应力。没有竞争对手能提供这样的广度。

**协同效应的账**（出自 2024 年投资者日）：第 3 年实现 $400M 运行率（run-rate）成本协同，第 4 年实现 $400M 运行率收入协同，长期年收入协同 $1B+。在 2026 年 3 月的 Morgan Stanley TMT 大会上，Ghazi 表示协同兑现进度领先于原计划。合并后公司的目标包括：non-GAAP 营业利润率处于 mid-40s%（40% 出头到中段）、无杠杆自由现金流利润率处于 mid-30s%、EPS 增速达 high-teens（高十几）个百分点。Ansys 还带来终端市场多元化：半导体/高科技占 31%，航空航天占 22%，汽车占 18%。

**风险**包括整合复杂度（客户群、销售打法、企业文化都不同）、杠杆（交割时约 3.9 倍，目标是两年内降到 2 倍以下）、估值（$35B 相当于 12 倍营收），以及管理层精力被从核心 EDA 竞争上分散。

### 利润率阶梯：从 14% 到 37.3%（FY2006-FY2024）

这就是锁定不断加深的财务证据。

![](https://substack-post-media.s3.amazonaws.com/public/images/28f93ea0-d78c-4ae3-91cd-38997948fdf7_802x353.png)

这一模式二十年来一以贯之。大型并购（Magma、Coverity、Black Duck）会暂时压缩利润率 100-200 个基点，随后被系统性地修复。管理层 2011 年对分析师说过：*「如果我们看到机会能让营收再多增长一些，我们想做；如果出于某种原因，营收增长变得更困难，我们会立刻转而对营业利润率施加更高压力。」*

23 个百分点的利润率扩张来自四个结构性因素：(1) 从永久授权转向时段授权；(2) 验证/IP 的组合向更高利润率产品迁移；(3) AI 工具拿到 15-25% 的溢价而增量成本微乎其微；(4) 平台交叉销售降低了获客成本。

### CEO 交接：从创始人到职业经理人

Aart de Geus（1986-2023 年任 CEO，现任执行董事长）把公司交给了 Sassine Ghazi（2024 年 1 月起任 CEO），语气的转变微妙却实质。

- **De Geus 说的是愿景宣言。** *「我认为我们的使命，是成为开启智慧万物世界的关键催化剂。」*
- **Ghazi 说的是财务框架。** *「我们布局公司产品组合时心中只有一个战略终点：在无处不在的智能时代，把我们交付给客户的价值最大化。」*

Ghazi 上任第一年的两大动作证明了这次转向。软件完整性部门（Software Integrity Group）以 $2.1B 剥离（理由是*「设计自动化与设计 IP 领域存在极具吸引力的投资机会，预期增长和回报特征要高得多」*），Ansys 以 $35B 收入囊中。区分 AI 基础设施客户与传统半导体客户的「双城记」框架，是典型的 Ghazi 式分析方法，传递的信号是运营纪律优先于愿景式扩张。

![A screenshot of a computer screen
Description automatically generated](https://substack-post-media.s3.amazonaws.com/public/images/1960b207-9cfa-482d-ab40-92280efac033_1600x840.png)

资料来源：SemiAnalysis，公司报告

*Synopsys 收购时间线。「买优于造」的战略在 2024 年的 Ansys（$35B）上骤然提速。*

### 在手订单堡垒

![](https://substack-post-media.s3.amazonaws.com/public/images/44402bb9-eb6a-478b-a2fc-1551e094c808_1291x391.png)

$11.3B 的在手订单，为一家软件公司提供了非同寻常的前向收入能见度。

![A graph on a screen
Description automatically generated](https://substack-post-media.s3.amazonaws.com/public/images/e69dff93-8394-46d9-beec-9fc00761593b_1600x839.png)

资料来源：SemiAnalysis，公司报告

*Synopsys 与 Cadence 在手订单。分别为 $11.4B 和 $7.8B（FY2025 年末），提供 1.5-1.6 年的前向收入能见度。*

### 先进节点 100% 市场份额，已获验证

历季财报电话会记录勾勒出的历史弧线，显示了十年出头的稳步积累。

- **2013Q1**：*「Synopsys 投入 FinFET 使能已有五年，我们至少领先一年。」*
- **2014Q3**：150+ 个 FinFET 设计，份额 >95%
- **2016Q1**：286 个活跃 FinFET 设计，份额 95%。*「迄今为止完成的所有 10nm 和 7nm 流片，100% 使用了 Synopsys 设计工具。」*
- **2019Q2**：*「12nm 及以下节点市场份额 100%。」*
- **2023Q1**：3nm。*「约三分之二的设计完全使用 Synopsys 流程。」* 按设计启动数计仍宣称 95% 份额。
- **2025Q1**：2nm。*「一家美国超大规模云厂商完全使用 Synopsys 设计流程流片了一颗 2 纳米测试芯片。」*

支撑这些说法的完整设计启动数据见下文竞争护城河一节。2019 年之后不再披露设计启动数据并不代表份额流失——这些数据变成了反垄断层面的负担，而此后营收的持续增长用另一种方式支持了同样的结论。

![A screenshot of a graph
Description automatically generated](https://substack-post-media.s3.amazonaws.com/public/images/6a83117d-2c82-4760-9391-f89266178361_1600x899.png)

资料来源：SemiAnalysis，公司报告

*Synopsys 分业务营收。IP 收入从 $200M（2011）增长到 $1.91B（2024），13 年增长 9.5 倍。IP 业务占 FY2024（并入 Ansys 之前）营收的 31%，在更大的 FY2025 基数下降至约 25%。*

![A graph of blue and orange bars
Description automatically generated](https://substack-post-media.s3.amazonaws.com/public/images/25bcdf07-0aa3-4ce1-8d56-d2ce8a587b56_1600x824.png)

资料来源：SemiAnalysis，公司报告

*Synopsys 分业务营收。IP 收入从 $200M（2011）增长到 $1.91B（2024）；随着 Ansys 收入摊大分母，IP 占比从 31%（FY2024）降至约 25%（FY2025）。*

### 近期逆风：FY2026 过渡之年

在被 Ansys 推高的表观数字之下，Synopsys 的有机业务正在减速。Ansys 并购掩盖了 FY25 独立 EDA+IP 业务的放缓：剔除 Ansys 后有机营收同比仅增长约 3%，而报表口径为 15%。FY26 同样的态势延续，剔除 Ansys 后有机增速约 7-8%，报表口径则为 36%。报表增速与有机增速之间的差距达到历史最大。

最大的拖累是 IP。FY25 四个季度中有三个季度设计 IP 收入环比下降，脱离了 FY20-FY24 期间 13% 的历史 CAGR。两个具体的缺口导致了下滑。其一，Intel 挪动了外部代工节点的门柱。Synopsys 的 IP 是以 18A 为基线开发的，但 Intel 把外部客户推向了 18A-P（再往后是 14A），把 Synopsys 按原计划配置好产能的放量窗口往后推。Sassine 确认这些 IP 在其开发所面向的节点上是可用的，但随着外部 18A 走量推迟到 18A-P 重新调校版，第三方 IP 的变现被延后。其二，公司在 HPC IP 品类上存在覆盖缺口，预计 2HFY26 补齐。

管理层对 FY26 IP 增速的指引是「平淡」（低个位数百分比），并预计逐季改善，远低于公司 mid-teens（百分之十几中段）的长期 IP 目标。处理器 IP 解决方案业务正在剥离给 GlobalFoundries，此举让公司更聚焦互连和基础 IP，但造成近期收入的真空期。4QCY25 设计 IP 调整后营业利润率跌至 16.2%，远低于 IP 业务规模化时 30%+ 的水平。

中国因素放大了有机业务的疲软。剔除 Ansys，FY25 中国区收入下降 22%，原因是出口管制收紧，以及本土 EDA 公司在成熟节点抢占份额。管理层直接承认：*「我们无法向其销售的那些公司正在寻找替代方案，而这些替代方案通常是本土 EDA 或 IP 公司。」* 中国区敞口从 FY24 占营收的 16% 降到 FY25 的 12%，管理层预计 FY26 还将进一步放缓至低于公司平均增速。

核心 EDA（剔除 IP 和 Ansys）FY25 增长 8%，低于公司两位数的长期目标；管理层对 FY26 核心 EDA 的指引仅为 9%。硬件业务（ZeBu/HAPS）在 AI 芯片需求带动下创下纪录，但无论市场份额还是收入规模，都仍明显落后于 Cadence 的 Palladium。Cadence 正谋求在 Intel 打开局面——那里历来是 Synopsys 的堡垒。

Synopsys 正尝试把 IP 商业模式从「固定 NRE 加使用费」改造为包含版税的模式，以回应日益要求定制 IP 的超大规模云厂商客户。这一模式转换带来近期收入逆风：旧合同到期出清，而版税收入流的建立需要时间。首批 Synopsys-Ansys 联合物理方案预计 1H26 推出，可能带来定价上行空间，但整合风险依然真实存在。FY26 全年值得盯的关键催化剂是：年中前后 IP 收入企稳、基于版税的 IP 模式在超大规模云厂商客户中起势的证据、以及有机 EDA 增速重新向两位数目标加速。

### Intel 客户集中度：二十年的依赖

二十多年来，Intel 一直是 Synopsys 的最大客户。集中度最高的 FY2017 年，Intel 占总营收的 17.9%（在当时的收入基数上为 $363M）。到 FY2024，Intel 占比回落至 12.6%（$772M），这更多反映 Synopsys 收入的多元化，而非 Intel 支出的减少。FY2025，Synopsys 历史上首次没有单一客户占比超过 10%，不过这一里程碑更多归功于 Ansys 摊大了分母，而不是 Intel 支出下滑。

Intel 仍是其第一大客户。Cadence 如今也瞄准了 Intel——相对于其在 TSMC 和 Samsung 的强势，这历来是 Cadence 的短板。Intel Foundry 的重组和领导层更迭，在整个 EDA 技术栈上创造了以往不存在的评估窗口。每一次代工厂转型都会打开竞争性重评估的窗口，而 Intel 眼下的转型是十年来最大的一扇。

![A graph with red and yellow bars
Description automatically generated](https://substack-post-media.s3.amazonaws.com/public/images/4f2682ac-22ce-4d7b-9445-8c25741dc4fd_1600x839.png)

资料来源：SemiAnalysis，公司报告

*Synopsys 的 Intel 客户集中度（20 年）。Intel 在 FY2017 达到营收占比 17.9% 的峰值，FY2025 随着 Ansys 扩大营收基数降至 10% 以下。*

## Cadence：从濒临死亡到最高利润率

![](https://substack-post-media.s3.amazonaws.com/public/images/d0fc0ac9-a4a7-40a6-ad69-49b75c755d9a_1640x395.png)

IP 业务板块是增长引擎。SDA 的增长包含 BETA CAE 收购（$1.24B，2024 年 Q2），后者把结构分析能力带给了全球前 10 大车企和 F1 车队。进入 2026 年，硬件在手订单处于创纪录水平。

![](https://substack-post-media.s3.amazonaws.com/public/images/7cd5e175-2bf4-4266-9ea2-d632daf583db_1015x227.png)

### 2026 年展望：全面隐含上行

创纪录的 $7.8B 在手订单（环比 +11%），在没有任何新签单之前已覆盖 FY26 营收的 67%。硬件业务的风险已经解除，下半年加权的交付排期均已锁定。中国区指引为营收的 12-13%，且已计入下半年谨慎假设——FY25 时同样的保守框架最后被证明过于谨慎，当年中国区增速超出了指引。Hexagon Design & Engineering 收购（年化收入约 $200M）完全没有计入 $5.9-6.0B 的指引。增量利润率指引为 51%，远低于 Cadence FY25 实际交付的 59%。指引中嵌入的每一个假设都偏保守，为上行留出了多条路径。

系统公司目前占 Cadence EDA 需求的 45%，高于两年前的 40%。一家头部超大规模云厂商采用 Cadence 数字全流程完成了其首个完整 COT（Customer-Owned Tooling，客户自有工具）AI 芯片流片，这一里程碑验证了 Cadence 数字工具在要求最苛刻客户处的竞争力。2025 年 Cadence 新增 25 家数字全流程客户（logo），延续从 2014 年每年 10 单到如今持续两位数年度新增的轨迹。IP 产品组合以 HBM4、224G SerDes 和 LPDDR6 为关键品类，达到了临界规模。IP 收入 2025 年增长近 25%，已是连续第三年强劲增长。TSMC、Samsung、Intel、Rapidus 之间的多家代工厂格局是结构性顺风，Cadence 的卡位比 Synopsys 更好——后者已承认 FY26 的 IP 将是平淡的一年。

硬件业务再创纪录：新增 30+ 客户，来自 AI 和超大规模云厂商项目的重复需求大幅上升。前 10 大硬件客户中有 7 家是「动感二人组」（Dynamic Duo，仿真 + 原型验证）客户，Cadence 由此嵌入了整个验证工作流。管理层表示公司在所有主要产品细分都在夺取份额。CFO John Wall 给出了智能体（agentic）AI 的三层变现框架：订阅是锚定收入基盘；基于用量的定价捕捉 AI 驱动的算力强度；虚拟工程师层级则把智能体按「等效新增人头」定价。完整变现需要两个合同续约周期，因此这是 FY27-28 的收入故事，但架构已经就位。

Hexagon Design & Engineering 收购（年化收入约 $200M）于 2026 年 2 月完成交割，新增的物理 AI 和汽车仿真能力在系统仿真领域与 Synopsys-Ansys 正面竞争。Cadence 还扩大了与 TSMC 在 N2 和 A16 工艺流程上的合作，深化了与 Broadcom 在智能体 AI 工作流上的伙伴关系，并与日本政府支持的代工厂 Rapidus 正式建立新伙伴关系。每一段代工厂关系都会带来 IP 移植收入、工具认证费用和长期设计生态粘性。

![A graph on a screen
Description automatically generated](https://substack-post-media.s3.amazonaws.com/public/images/e602e427-d9f9-443c-a122-beafcc3d95d2_1600x831.png)

资料来源：SemiAnalysis，公司报告

*Cadence 分业务营收。SDA 从 $500M（2019）增长到 $1.5B+（2024），驱动力是 Palladium 硬件和 BETA CAE。*

### 定义一切的濒死体验

在 CEO Mike Fister 任内（2004-2008），Cadence 激进扩张相邻业务，还试图恶意收购 Mentor Graphics，结果是灾难性的。

![](https://substack-post-media.s3.amazonaws.com/public/images/fc355908-606b-4c19-bdd5-798cf042860f_777x301.png)

营收一年内下滑 36%，录得每股 $6.57 的 GAAP 亏损和 $200M 的商誉减值。

### 陈立武（Lip-Bu Tan）的翻身仗（2009-2024）

Lip-Bu Tan（陈立武）于 2009 年 1 月在最低谷接任 CEO。2014 年他在财报电话会上总结道：*「2009 到 2013 年，营收增长 71%。non-GAAP 营业利润率从接近零扩张到 24%，经营现金流从区区 $26 million 增长到 $368 million。」*

从 -11% 到 42.5% 的利润率阶梯，走了 15 年。

![](https://substack-post-media.s3.amazonaws.com/public/images/0d1f6a28-a5d4-47d5-9bf5-f47a195be0a7_1067x358.png)

15 年 53 个百分点的利润率扩张，靠的是 Tan 的运营法则：*「增量收入的 50% 直接落到营业利润。」* Cadence 连续 7 年以上达成这一目标。

### Virtuoso：没人能杀死的工具

Cadence 通过 Virtuoso 垄断了模拟设计。这个工具没有像样的竞争对手，因为模拟设计方法论是在 Virtuoso 里演化了四十年的。这个工具沉淀着关于匹配、噪声和线性度的经验直觉（tribal knowledge），靠写更好的算法复制不来——它需要把几十年的客户反馈一层层叠进产品里。

- **2008Q4**：45 家量产客户，70 次流片，全球前 50 大半导体公司全部在使用 Virtuoso
- **2016Q3**：100+ 家客户用于 FinFET 节点
- **2024Q4**：客户总数 450+，业内最大的模拟设计客户群
- **2024Q1**：Virtuoso Studio 发布；前 20 大半导体公司中有 18 家在第一年内完成迁移

450+ 家客户，有据可查的重大客户流失为零。几十年公开财报披露中竞争性丢单的缺席，印证了市场份额数字所暗示的一切。

### Palladium：10 年的硬件领先

- **2007Q3**：*「尚未出现竞争性丢单。」* 单季度通过升级出货 1 亿门。
- **2012**：Palladium XP 装机量达到前两代总和的 4 倍
- **2014Q3**：前 20 大半导体公司中的 15 家、前 10 大应用处理器公司中的 9 家在用
- **2020**：创纪录之年。硬件业务 40% 来自系统公司（超大规模云厂商、汽车 OEM）
- **2024Q1**：Palladium Z3 发布。480 亿门容量，定制 ASIC，液冷。管理层称*「最接近的竞争对手是 Palladium Z2」*
- **2024**：近 200 家复购客户。30 个新客户（logo）。
- **2025**：*「AI 使能流片远超 1,000 次。」* Cadence 宣称在定制仿真专用芯片上拥有*「10 年领先优势」*。

每年 200 家复购客户，加上一套需要竞争对手花大约十年才能跨越的定制 ASIC 架构开发护城河。

### 不断收窄的数字工具差距

- **2014**：每年 10 个数字全流程赢单
- **2015**：Innovus 发布。*「PPA 改善 10-20%，周转时间缩短 10 倍。」* 获得 ARM Cortex-A72 背书。
- **2019**：50 单，重大拐点，为上一年的 2 倍
- **2022Q4**：全球前 20 大半导体公司全部在使用 Cadence 数字软件
- **2024**：36 家新数字全流程客户（仅 Q4 就有 17 家）
- **2025Q1**：核心 EDA 收入同比增长 16%

从 2014 年的 10 单，到 2024 年单年 36 单。Cadence 从不正面反驳 Synopsys 的「95% 先进节点」说法，而是援引 TSMC 年度合作伙伴奖，让营收数字自己说话。

### Cerebrus AI：8 个季度 1,000+ 次流片

- **2023Q1**：180 次流片
- **2024Q4**：750 次流片（仅 Q4 就有 300 次）
- **2025Q1**：1,000+ 次流片。*「Q1 新增近 50 家客户（logo）。」*

不到 2 年增长 5.6 倍，前 10 大数字客户 100% 渗透。Cadence 的打法是先铺开渗透率，之后再通过 ACV（年度合同价值）增长兑现定价。

点名客户成绩讲清了技术故事。MediaTek 实现裸片（die）面积缩减 5%、功耗降低 6%+。Renesas 在先进节点 CPU 上总负时序裕量（negative slack）改善 75%。Samsung SARC 获得 4 倍生产力提升，Samsung India（SSIR）实现 8-11% 的 PPA 改善。IBM 正在部署 Cadence AI 使能的数字实现工具。Cerebrus 之下的 JedAI（Joint Enterprise Data and AI）平台把波形、覆盖率报告、时序分析和物理版图汇聚成统一的训练数据仓库，构成复利式数据护城河，让 Cadence 的 AI 工具随着每次部署不断变强。

![A graph with a line and a graph
Description automatically generated with medium confidence](https://substack-post-media.s3.amazonaws.com/public/images/5547f724-f5bf-494c-a644-09e8bdd5db42_1600x899.png)

资料来源：SemiAnalysis，公司报告

*Cerebrus AI 流片轨迹。8 个季度从 180 次到 1,000+ 次，前 10 大数字客户 100% 渗透。*

### CEO 交接与三层次战略

Anirudh Devgan 于 2021 年 12 月出任 CEO，把 Cadence 重新定义为一家「计算软件公司」，并提出三个扩张层次。

**第一层（当下 - 3 年）：数据中心 AI。** 面向 AI 加速器设计的核心 EDA、IP 与硬件仿真，已是最大的收入驱动力。

**第二层（3 - 7 年）：汽车与「物理 AI」。** BETA CAE（$1.24B，2024 年 Q2）带来服务于全球前 10 大车企和 F1 车队的结构分析。MSC Software（$3.25B，2025 年 9 月）补上机械仿真。加上 Cadence 既有的 CFD 能力（NUMECA，2021 年收购）和 Pointwise（网格生成，2021 年），Cadence 如今拥有面向汽车的完整多物理场技术栈。收购顺序是刻意为之：先下小注（NUMECA $189M、Pointwise $31M），验证后再上规模（BETA CAE $1.24B、MSC $3.25B）。

**第三层（5 - 10+ 年）：生命科学。** OpenEye Scientific（$500M，2022 年 9 月）提供计算分子建模，全球前 20 大制药公司中有 19 家在用。其核心论点是：优化晶体管布局的同一套算法，也可以优化分子对接，TAM 估计为 $2B，以约 15% 的 CAGR 增长。**这是 Devgan 最非共识的一笔押注，如果成功，Cadence 将彻底超越 EDA 这个品类**。

2024 年 Lip-Bu Tan 曾探讨回归公司，董事会最终确认留任 Devgan，Lip-Bu 转而出任 Intel CEO。这场交接异常公开，传递出公司治理的稳健以及对 Devgan 战略的信心。

![A screenshot of a graph
Description automatically generated](https://substack-post-media.s3.amazonaws.com/public/images/1e16adf1-eefb-498e-ae60-368cab160415_1600x836.png)

资料来源：SemiAnalysis，公司报告

*Cadence 收购时间线。NUMECA、Pointwise、OpenEye、BETA CAE、MSC Software——系统性地向核心 EDA 之外扩张。*

![A graph of a graph with numbers and lines
Description automatically generated with medium confidence](https://substack-post-media.s3.amazonaws.com/public/images/11a60a0c-370a-4b6c-a047-a0b230f25cc6_1600x1229.png)

资料来源：SemiAnalysis，公司报告

*利润率大逆转。Cadence：从 -11%（2009）到 42.5%（2024）。Synopsys：从 14%（2006）到 37%（2024）。Cadence 虽然规模更小，如今却是盈利能力更强的那一家。这个翻身故事是企业软件史上最伟大的逆转之一。*

## 封锁位：Siemens EDA

![](https://substack-post-media.s3.amazonaws.com/public/images/ae59347b-ce09-449a-b633-c4fc863e70f9_1140x322.png)

Calibre 物理验证是行业标准。TSMC 指定流片必须通过「Calibre-clean」的 DRC/LVS，Samsung 和 Intel 同样如此。仅凭这一个工具，无论其他工具品类如何演变，Siemens EDA 在这个市场中的地位都难以撼动。

### Mentor 如何沦为第三：Release 8.0 灾难

Mentor Graphics 在 1980 年代末曾是最大的 EDA 厂商，1989 年营收 $380M、净利润 $44.8M。随后管理层尝试对整个软件套件做一次彻底的推倒重写（「Release 8.0」），事态随即失控。项目延期数年，Cadence 趁乱在软件收入上反超 Mentor。Mentor 于 1991 年 4 月录得首个季度亏损，接着是 $61.6M 的年度亏损和 15% 的裁员。1992 年 Release 8.0 终于发布时，又慢又满是 bug。

这是 EDA 行业最经典的警示故事，它解释了三个延续至今的现实。其一，它解释了 Mentor 为什么从第一跌到第三、再也没能翻身。其二，它解释了为什么三巨头全都靠收购而不是从零自建（Synopsys-Ansys、Cadence-BETA CAE、Siemens-Altair）。其三，它解释了为什么没有任何创业公司能靠从零重写复刻一个 EDA 平台——代码库的复杂度每次都能击败白纸起家的方案。

CEO Wally Rhines（1993-2017）转而通过并购重建 Mentor，把 Calibre、PCB 工具、嵌入式软件和汽车电子整合成一个连贯的产品组合。Carl Icahn（2011 年）和 Elliott Management（2016 年）的激进投资者压力最终把 Mentor 推向出售，Siemens 于 2017 年以 $4.5B 将其收购，并在 2021 年更名为 Siemens EDA。

### 归属 Siemens 是一把双刃剑。

**好处**包括：获得工业集团内部的交叉补贴；EDA 与 Teamcenter PLM、Opcenter MES 打包销售；以及 Siemens 面向汽车 OEM 供货，而 Siemens EDA 服务于给这些 OEM 供货的芯片设计师。

**弊端**也实实在在。EDA 占 Siemens 收入不到 5%；没有可用于并购的独立上市股票；业绩报告埋在 Digital Industries Software 里面、不透明；投资还要与自动化、医疗和能源等板块争夺母公司资本。

### 仿真军备竞赛：Siemens 收购 Altair

2024-2025 年间，三巨头不约而同地收购仿真/CAE 公司，上演了一轮针锋相对的升级。

![](https://substack-post-media.s3.amazonaws.com/public/images/d29ea7e3-39c7-4a3a-bb30-45d9b66264a1_1207x297.png)

EDA 与 CAE 的边界正在永久性消融，Siemens 的 Altair 交易是「从硅片到系统」仿真栈三方竞逐的第三条腿。

### Siemens AI 产品：奋力追赶

在 DAC 2025 上，Siemens 发布了三个 AI 产品家族：面向数字实现的 Aprisa AI、面向 DRC 违例聚类（把调试时间砍半）的 Calibre Vision AI、以及面向定制/模拟设计的 Solido AI。这些产品瞄准 Siemens 85%+ 的 Calibre 装机基数，是该公司首次认真借助 AI 杀入由 Synopsys 和 Cadence 领跑的领域。与 NVIDIA 的合作则利用 NIM 微服务做 EDA 专用 AI 推理。

### PAVE360：系统级数字孪生打法

Siemens 应对芯片级竞争的差异化回应是 PAVE360：提供整车仿真、软硬件协同验证和量产整车集成测试。与 AMD、Elektrobit、KPIT、TIER IV 和 Qt 的伙伴关系，构建了从系统需求到量产验证的端到端工作流。

系统级汽车验证的 TAM 与 EDA 相邻（到 2030 年为 $800M-1.2B 的机会），但买家不同，具体是整车集成团队和 Tier-1 供应商。Siemens 可以吃下这块相邻机会，而不必与 Synopsys、Cadence 在芯片级工具位上正面竞争。

### FY2026 第一季度更新（2026 年 2 月）：EDA 跑赢集团组合

FY2026 第一季度，Siemens 的 Digital Industries 软件业务增长 11%，其中 EDA 和仿真在该板块内实现了健康的双位数增长。Altair 整合进展顺利，与 NVIDIA 在芯片设计软件上的合作持续扩大。PLM（不含仿真）增长 7%，这意味着 EDA 和仿真的增速明显跑赢 Siemens 更庞大的软件组合。这种分化很重要：它表明半导体设计复杂度和汽车仿真需求拉动 Siemens EDA 的速度，已超过工业 PLM 基本盘，进一步印证了 Altair 和 Mentor 两笔收购背后的战略逻辑。

![A graph with lines and numbers
Description automatically generated with medium confidence](https://substack-post-media.s3.amazonaws.com/public/images/6e022ad7-eb89-4e3d-90b0-0262ec270ba6_1600x1002.png)

资料来源：SemiAnalysis，公司报告

*研发强度：Synopsys 为 34%，Cadence 为 30%，Siemens EDA 估计为 25-28%。支出差距解释了技术差距，但 Siemens 强度较低也反映出 Calibre 的地位根深蒂固、无需太多研发来防守。*

*完整报告中，订阅用户可以读到：竞争动态分析（2026 年 Cadence 在有机增长上拉开对 Synopsys 的领先）、包含王牌工具与 PDK 护城河证据的六层锁定架构、NVIDIA Blackwell 与 Apple Silicon 的设计成本拆解、来自财报电话会记录的中国厂商财务与出口管制取证、我们独家的 R 平方（R-squared）锁定强度矩阵（按 EDA 依赖度对 20+ 家无厂设计公司排名）、附带 2026 年 2 月财报电话会 CEO 引语的 AI 颠覆风险评估，以及催化剂清单。全部数据可在我们按季度更新的交互式 EDA Dashboard 中查阅。*
