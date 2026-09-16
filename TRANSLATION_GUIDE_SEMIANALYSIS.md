# 翻译规范（SemiAnalysis 文章中文化）

本文件是 SemiAnalysis（semianalysis.com，Substack：newsletter.semianalysis.com）全部文章翻译批次的统一规范。开始翻译前先读完本文件。

## 来源与范围

- 数据源：Substack 公开 API（`/api/v1/posts/<slug>`），英文归档在 `semianalysis-articles/posts/<slug>.md`，元数据在 `semianalysis-articles/meta.json`。
- `audience: only_paid` 的文章为付费订阅文，API 只返回付费墙前的公开预览（正文截断）。译文同样只译公开预览部分，并保留归档文件中的「⚠️ 付费订阅文章」标注，**不得**假装译完了全文。
- `audience: everyone` 的文章为全文，必须完整翻译。

## 输出位置与文件头

- 输出目录：`semianalysis-articles-zh/posts/`，文件名与英文归档一一对应（`<slug>.md`）。
- 文件头 frontmatter：保留英文归档的全部字段（title_en 存原题），`title` 换中文译名，增加 `translated`：

```markdown
---
title: "中文标题"
title_en: "English Title"
subtitle: "中文副标题"
date: 2025-03-18
source: https://newsletter.semianalysis.com/p/...
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: ["Nvidia"]
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 中文标题

> 原文：[English Title](source URL) · SemiAnalysis

**中文副标题**

（正文译文……）
```

付费文额外在 `> 原文：…` 行后保留一行：
`> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。`

## 翻译原则

1. **全文翻译，不得缩写或跳过段落**。导语、表格、图注、脚注、结尾免责声明都要译。
2. **代码块原样保留**；行内代码保留。文末合规/免责声明（compliance disclosure）必须翻译，不得删除。
3. **图片链接与图片 URL 原样保留**；`![alt](url)` 的 alt 可译可留，图注（斜体行）翻译。
4. **Markdown 结构一一对应**：标题层级、列表、表格、引用块位置不变。表格单元格内容翻译；表格中的数字、股票代码（NVDA、TSM 等）、单位保持原样。
5. **数字、单位、型号不改动**：$1,000、100k、1M、10GW、3nm、HBM3E、GB200 NVL72、CoWoS-S 等原样保留（货币符号 $ 可保留，必要时译作「美元」）。
6. **语气**：面向中文半导体/AI 行业研究员与投资者的研究简报风格，信息密度高、句式干脆；不逐词直译，但不删减内容。
7. 公司/产品/人名不翻译：NVIDIA、TSMC、ASML、AMD、Intel、Samsung、SK hynix、Micron、Broadcom、Marvell、Google TPU、AWS Trainium、Meta MTIA、Dylan Patel 等。常见中文定名公司可加中文：美光（Micron）、三星（Samsung）、台积电（TSMC）、英特尔（Intel）——首次出现时「中文（英文）」，后文用其一即可。

## 术语表（全文统一）

### 半导体制造与工艺

| English | 中文 |
|---|---|
| wafer / wafer capacity | 晶圆 / 晶圆产能 |
| node / process node | 制程节点 |
| leading-edge / trailing-edge | 先进制程 / 成熟制程 |
| foundry / fabless / IDM | 代工厂 / 无厂设计公司 / IDM（垂直整合制造商） |
| EUV / DUV / High-NA EUV | EUV / DUV / High-NA EUV（不译） |
| lithography / scanner / immersion | 光刻 / 光刻机 / 浸没式 |
| gate-all-around (GAA) / nanosheet | 环栅晶体管（GAA）/ 纳米片 |
| FinFET | FinFET（不译） |
| backside power delivery (BSPDN) | 背面供电（BSPDN） |
| die / die shot / die size | 裸片（die）/ 裸片图（die shot）/ 裸片面积 |
| reticle / reticle limit | 光罩 / 光罩极限 |
| yield / yield learning | 良率 / 良率爬坡学习 |
| ramp / capacity ramp | 爬坡 / 产能爬坡 |
| WFE (wafer fab equipment) | 晶圆厂设备（WFE） |
| advanced packaging | 先进封装 |
| CoWoS / InFO / SoIC | 不译 |
| chiplet | 小芯片（chiplet） |
| interposer / substrate | 中介层 / 封装基板 |
| hybrid bonding | 混合键合 |
| TSV (through-silicon via) | 硅通孔（TSV） |
| OSAT | OSAT（封测代工，不译） |
| design rule / design win | 设计规则 / 设计导入（design win） |
| allocation / lead time / pull-in | 产能配给 / 交期 / 提前拉货 |
| tape-out | 流片 |
| NRE | NRE（一次性工程费用，不译） |
| DRAM / NAND / HBM | DRAM / NAND / HBM（不译） |
| 3D NAND / stacking / 4-hi / 8-hi / 12-hi | 3D NAND / 堆叠 / 4 层 / 8 层 / 12 层堆叠 |
| bit growth | 位元增长 |
| wafer start / fab utilization | 晶圆投片 / 产线稼动率 |
| silicon photonics / CPO (co-packaged optics) | 硅光子学 / 共封装光学（CPO） |
| silicon carbide (SiC) / GaN | 碳化硅（SiC）/ 氮化镓（GaN） |

### AI 计算与网络

| English | 中文 |
|---|---|
| training / pretraining / finetuning | 训练 / 预训练 / 微调 |
| inference / prefill / decode | 推理 / 预填充（prefill）/ 解码（decode） |
| agentic inference | 智能体推理 |
| token / tokens per second (TPS) | token（不译）/ 每秒 token 数 |
| FLOPS / PFLOPS / EFLOPS | 原样保留 |
| tensor core | 张量核心 |
| KV cache | KV 缓存 |
| context window | 上下文窗口 |
| MIG / GPU instance | 原样保留 |
| cluster / supercluster | 集群 / 超级集群 |
| scale-up / scale-out domain | 纵向扩展域 / 横向扩展域 |
| NVLink / NVSwitch / InfiniBand / RoCE / Ultra Ethernet | 不译 |
| NIC / DPU / SmartNIC | NIC / DPU / SmartNIC（不译） |
| switch / radix / hop | 交换机 / 端口数（radix）/ 跳数 |
| optics / transceiver / pluggable | 光模块 / 收发器 / 可插拔 |
| rack / rack-scale | 机柜 / 机柜级 |
| GB200 NVL72 / Vera Rubin 等产品名 | 不译 |
| GPU / TPU / ASIC / FPGA / IPU | 不译 |
| HBM bandwidth / memory bandwidth | HBM 带宽 / 内存带宽 |
| power delivery / vertical power delivery | 供电 / 垂直供电 |
| TDP / power envelope | TDP / 功耗包络 |

### 数据中心与能源

| English | 中文 |
|---|---|
| datacenter / hyperscaler / neocloud / GPU cloud | 数据中心 / 超大规模云厂商 / 新兴 GPU 云（neocloud）/ GPU 云 |
| capex / opex | 资本开支（capex）/ 运营开支（opex） |
| TCO (total cost of ownership) | 总拥有成本（TCO） |
| PUE | PUE（不译） |
| chiller / free cooling / liquid cooling | 冷水机组 / 自然冷却 / 液冷 |
| direct-to-chip / cold plate / CDU | 冷板式直冷 / 冷板 / 冷量分配单元（CDU） |
| rear-door heat exchanger | 后门热交换器 |
| MW / GW / IGW | 原样保留（兆瓦/吉瓦可在首次括注） |
| substation / transformer / grid interconnect | 变电站 / 变压器 / 电网并网 |
| behind-the-meter / front-of-the-meter | 表后（自备电源）/ 表前并网 |
| gigawatt campus / AI campus | 吉瓦级园区 / AI 园区 |
| diesel generator / UPS / BESS | 柴油发电机 / UPS / 电池储能系统（BESS） |

### 财务与市场

| English | 中文 |
|---|---|
| revenue / billings / backlog | 营收 / 开单 / 在手订单 |
| gross margin / operating margin | 毛利率 / 营业利润率 |
| ASP (average selling price) | 平均售价（ASP） |
| TAM (total addressable market) | 总可服务市场（TAM） |
| BOM (bill of materials) | 物料清单（BOM） |
| CoGS / cost of goods sold | 销售成本（CoGS） |
| supply chain | 供应链 |
| inventory / inventory correction | 库存 / 库存调整 |
| cycle / downturn / upcycle | 周期 / 下行周期 / 上行周期 |
| short interest / squeeze | 空头仓位 / 轧空 |
| guidance / consensus | 业绩指引 / 市场一致预期 |
| earnings call | 财报电话会 |
| CAGR | CAGR（不译） |
| NPV / IRR | 不译 |
| strategic misallocation / capital discipline | 战略性错配 / 资本纪律 |
| national security / export controls | 国家安全 / 出口管制 |
| China restrictions / entity list | 对华管制 / 实体清单 |

### 其他

| English | 中文 |
|---|---|
| die shot annotation | 裸片图标注 |
| teardown | 拆解 |
| deep dive | 深度解析 |
| roadmap | 路线图 |
| supply-demand balance | 供需平衡 |
|比特缩写（GB/TB/PB）| 原样保留 |
| die-per-wafer | 每片晶圆裸片数 |

## 特别注意

1. SemiAnalysis 文章含大量自绘图表（Substack 图床 PNG），图注必须翻译；图表内文字不译（在图里）。
2. 财务数字密集段落翻译时逐个核对数字，**不得四舍五入或改写数量级**。
3. 原文中「We believe / We think」等第一人称研究观点保留第一人称「我们认为」。
4. 文末若有 "Disclosures" / 合规声明 / 免责声明段落，完整翻译。
5. 站内链接（`newsletter.semianalysis.com/p/...`）URL 不动，链接文字可译。
