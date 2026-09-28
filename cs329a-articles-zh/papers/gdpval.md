---
title: "GDPval：评估 AI 模型在真实世界经济有价值任务上的表现"
title_en: "GDPval: Evaluating AI Model Performance on Real-World Economically Valuable Tasks"
arxiv: 2510.04374
source: https://arxiv.org/abs/2510.04374
crawled: 2026-09-23
translated: 2026-09-23
---

# GDPval：评估 AI 模型在真实世界经济有价值任务上的表现

> 原文：[GDPval: Evaluating AI Model Performance on Real-World Economically Valuable Tasks](https://arxiv.org/abs/2510.04374) · Stanford CS329A 指定阅读

Tejal Patwardhan、Rachel Dias†、Elizabeth Proehl†、Grace Kim†、Michele Wang†、Olivia Watkins†、Simón Posada Fishman†、Marwan Aljubeh†、Phoebe Thacker†、Laurance Fauconnet、Natalie S. Kim、Patrick Chao、Samuel Miserendino、Gildas Chabot、David Li、Michael Sharman、Alexandra Barr、Amelia Glaese、Jerry Tworek

（OpenAI）

注：† 表示同等贡献。联系方式：tejal@openai.com。

###### 摘要

我们提出 GDPval，一个评估 AI 模型在真实世界经济有价值任务上能力的基准。GDPval 覆盖美国劳工统计局工作活动中对 GDP（国内生产总值）贡献前 9 大部门的 44 个职业的多数工作活动。任务由行业专业人士的代表性工作构建，他们平均拥有 14 年经验。我们发现，前沿模型在 GDPval 上的表现随时间大致线性提升，当前最佳的前沿模型在交付物质量上正在接近行业专家。我们分析了前沿模型在与人类监督配合时，以比未获辅助的专家更便宜、更快速地完成 GDPval 任务的潜力。我们还证明，提高推理努力（reasoning effort）、增加任务上下文与增强脚手架都能改进模型在 GDPval 上的表现。最后，我们开源了一个含 220 个任务的黄金子集，并在 [evals.openai.com](https://evals.openai.com) 提供公开的自动评分服务，以促进未来对真实世界模型能力的研究。

|  |
| --- |
|  |

## 1 引言

关于能力日益增强的 AI 模型可能如何影响劳动力市场——是通过自动化特定任务、取代整个职业，还是创造全新类型的工作——争议日益增多（Brynjolfsson et al., 2025；Chen et al., 2025）。当前衡量 AI 经济影响的方法聚焦于采用率、使用模式以及归因于 AI 的 GDP 增长等指标（Chatterji et al., 2025；Tamkin et al., 2024；Appel et al., 2025；Acemoglu, 2025；Bick et al., 2024）。然而，电力、飞机与计算机等技术变革的历史证据表明，从发明到渗透整个经济往往需要数年甚至数十年，需要监管、文化与流程上的改变（David, 1990；Brynjolfsson & Hitt, 2000；Brynjolfsson et al., 2017；Dwivedi et al., 2021；Solow, 1987）。因此，这些方法虽然在有数据时具有参考价值，却属于 AI 影响的滞后指标。我们考虑理解 AI 潜在经济影响的另一种方法：直接测量 AI 模型的能力。AI 能力评估可以提供更清晰、更直接可归因的模型能力证据，使我们能够在广泛采用之前评估经济相关性。

![Refer to caption](2510.04374v1/exampletasksscreenshot.png)

图 1：完整任务集中的 GDPval 示例任务。

本文提出 GDPval 的第一版，一个评估 AI 模型在真实世界经济有价值任务上表现的基准。GDPval 覆盖对美国 GDP（国内生产总值）贡献前 9 的部门，完整集中每个职业至少 30 个任务（黄金子集中每个职业 5 个任务），共 44 个职业。每个任务基于专家专业人士创造的实际工作成果构建。鉴于自动评分这些任务的复杂性，我们的主要评估指标是与人类专家的正面对比。我们还为 220 个开源黄金子集任务提供一个实验性自动评分器服务。未来的 GDPval 迭代将纳入更广的覆盖面、更强的真实性、交互性与上下文细节。

GDPval 的初始版本相较现有 AI 模型评估有若干优势：

- 真实性：不同于聚焦推理难度的学术考试式 AI 基准（例如 Phan et al., 2025；Hendrycks et al., 2020；Rein et al., 2023；Liu et al., 2023），任务基于行业专家的实际工作成果，经多轮验证与评审，并与完成所需的时间及成本挂钩。

- 代表性广度：不同于聚焦软件工程等特定领域的 AI 评估（例如 Miserendino et al., 2025），GDPval 完整集覆盖 44 个职业的 1,320 个任务，其来源覆盖 O*NET 为每个职业追踪的多数工作活动（U.S. Department of Labor, Employment and Training Administration, 2024）。这种自顶向下的方法保证了任务在各职业间的代表性。我们还基于生产环境 AI 使用分析（例如 Tamkin et al., 2024；Chatterji et al., 2025；Appel et al., 2025）覆盖模型采用仍处于早期的领域。

- 计算机使用与多模态：任务需要操作多种格式（例如 CAD 设计文件、照片、视频、音频、社交媒体帖子、图表、幻灯片、电子表格与客户支持对话）。黄金子集中每个任务还需要解析最多 17 个参考文件，完整集中最多 38 个。

- 主观性：除正确性外，专家评分者通常还考虑结构、风格、格式、美观与相关性等主观因素。因此我们的数据集也可作为评估自动评分器表现的有用试验台。

- 没有「上限」：与可能很快饱和的指标不同，我们的主要指标是胜率（win rate），允许持续评估。目前我们把模型输出与人类专家基线比较，但随时间推移可以用越来越强的模型替换基线并继续评估。

- 长时程难度：任务需要专家专业人士平均 7 小时的工作才能完成。高端任务的工作量可达数周。

## 2 任务创建

我们首先识别对美国 GDP 贡献最大的部门，然后从这些部门中收入最高的知识工作职业里采集任务。

### 2.1 职业优先级排序

GDPval 覆盖 9 个部门、44 个职业的任务，这些职业的从业者合计年收入 3 万亿美元。下面详述我们初始版本背后的方法论。

为选择初始职业，我们：

1. 选择对美国 GDP 贡献超过 5% 的部门，依据是 2024 年第二季度「按行业增加值占国内生产总值百分比」（见 Federal Reserve Bank of St. Louis, 2025）。这 9 个部门见表 1。

2. 在每个部门中选择对总工资与薪酬贡献最大且以数字化为主的 5 个职业[注1](#fn1)。我们采用基于任务的方法判断一个职业是否应被归类为「以数字化为主」。具体而言，我们从 O*NET——美国劳工部的职业数据库、定义与任务库——识别一个职业的所有任务。与 Eloundou et al.（2023）类似，我们提示 GPT-4o 把每个任务分类为数字化或非数字化，然后当一个职业的组成任务至少 60% 为数字化时，把该职业整体归类为数字化。为计算这一比例，我们用 O*NET 任务评分中每个任务报告的「相关性」（relevance）、「重要性」（importance）与「频率」（frequency）分数对任务加权。

   注 1：我们使用美国劳工统计局（U.S. Bureau of Labor Statistics, 2025a）的 2023 年 BLS 全国就业矩阵，通过识别每个职业就业人数最多的部门，把职业映射到部门。更多细节见第 A.7 节。

我们进一步把数字化任务度量的代表性与 Acemoglu & Autor（2011）的任务内容框架做了基准对比。我们观察到的相关性——数字化任务随非常规认知内容增加、随常规与手工内容减少——表明其与既有经济学工作度量一致，见第 A.7.1 节。

关于工资与职业数据，我们使用 O*NET 2024 年 5 月的全国就业与工资估计计算 831 个职业的总工资（U.S. Bureau of Labor Statistics, 2025b），详见第 A.7 节。

![Refer to caption](2510.04374v1/assets/occs_0922_f.png)

图 2：GDPval 包含来自 44 个职业的真实世界工作。

| 部门 | GDP 占比 | 顶级职业与总薪酬（十亿美元） |
| --- | --- | --- |
| 房地产与租赁 | 13.8% | Property/RE/Community Association Managers — $24.54B |
|  |  | Counter and Rental Clerks — $17.42B |
|  |  | Real Estate Sales Agents — $13.53B |
|  |  | Real Estate Brokers — $4.55B |
|  |  | Concierges — $1.80B |
| 制造业 | 10.0% | First-Line Supervisors of Production and Operating Workers — $51.07B |
|  |  | Buyers and Purchasing Agents — $39.79B |
|  |  | Shipping, Receiving, and Inventory Clerks — $38.50B |
|  |  | Industrial Engineers — $37.79B |
|  |  | Mechanical Engineers — $31.57B |
| 专业、科学与技术服务 | 8.1% | Software Developers — $239.18B |
|  |  | Lawyers — $136.66B |
|  |  | Accountants and Auditors — $135.44B |
|  |  | Computer and Information Systems Managers — $121.44B |
|  |  | Project Management Specialists — $108.77B |
| 政府 | 11.3% | Compliance Officers — $33.80B |
|  |  | Administrative Services Managers — $32.03B |
|  |  | Child, Family, and School Social Workers — $24.10B |
|  |  | First-Line Supervisors of Police and Detectives — $17.00B |
|  |  | Recreation Workers — $11.51B |
| 医疗健康与社会援助 | 7.6% | Registered Nurses — $323.05B |
|  |  | First-Line Supervisors of Office/Admin Support — $107.02B |
|  |  | Medical & Health Services Managers — $77.93B |
|  |  | Nurse Practitioners — $40.58B |
|  |  | Medical Secretaries & Admin Assistants — $37.87B |
| 金融与保险 | 7.4% | Financial Managers — $147.74B |
|  |  | Customer Service Representatives — $123.70B |
|  |  | Securities, Commodities, and Financial Services Sales Agents — $52.14B |
|  |  | Personal Financial Advisors — $43.33B |
|  |  | Financial and Investment Analysts — $39.67B |
| 零售贸易 | 6.3% | General & Operations Managers — $477.16B |
|  |  | 1st-Line Supervisors of Retail Sales Workers — $58.27B |
|  |  | Pharmacists — $45.12B |
|  |  | Private Detectives & Investigators — $2.39B |
| 批发贸易 | 5.8% | Sales Reps, Wholesale & Mfg (Except Tech/Scientific) — $103.21B |
|  |  | Sales Managers — $97.16B |
|  |  | Sales Reps, Wholesale & Mfg (Tech/Scientific) — $33.66B |
|  |  | 1st-Line Supervisors of Non-Retail Sales Workers — $21.43B |
|  |  | Order Clerks — $3.86B |
| 信息业 | 5.4% | Producers & Directors — $16.60B |
|  |  | Editors — $8.18B |
|  |  | News Analysts, Reporters, and Journalists — $4.41B |
|  |  | Audio & Video Technicians — $4.30B |
|  |  | Film & Video Editors — $2.41B |

表 1：各部门及其对美国 GDP 的增加值占比（2024 年第二季度），以及代表性顶级职业与总薪酬（十亿美元）。

### 2.2 专家招募

我们招募行业专家专业人士，基于其职业工作经验创建真实任务。专家须在其职业拥有至少 4 年专业经验，并有体现专业认可、晋升与管理职责的出色履历。专家平均拥有 14 年经验。我们进一步要求专家通过视频面试、背景调查、培训与测验才能参与项目。专家的时间与经验获得了优厚报酬。我们的行业专家曾任职的部分雇主包括：Accenture、Aetna、Apple、AXA Advisors、Bank of America、Barclays、BBC News、Boeing、Budget Rent a Car、Capital One、Centers for Disease Control and Prevention、Citigroup、Condé Nast、CVS Pharmacy、U.S. Department of Defense、Disney、Douglas Elliman、E*TRADE、Federal Trade Commission、General Electric、Goldman Sachs、Google、Guggenheim Partners、HBO、IBM、JPMorgan Chase、Johnson & Johnson、Kmart、Kirkland & Ellis LLP、LinkedIn、Lockheed Martin、Macy's、Massachusetts General Hospital、Meta、Microsoft、Morgan Stanley、National Park Service、NFL Network、Oracle、Paul, Weiss, Rifkind, Wharton & Garrison LLP、Prudential、PwC、Raytheon、Sally Beauty、Samsung、SAP、Scientific American、Sotheby's、Telegraph Media Group、Thermo Fisher Scientific、TIME、Twilio、U.S. Department of Justice、United States Air Force、United States Postal Service、Walgreens、Wells Fargo、White & Case LLP 与 Whole Foods。

### 2.3 任务创建

每个 GDPval 任务由两个主要部分组成：一个请求（通常带参考文件）与一个交付物（工作成果）。专家将其请求对照其职业的 O*NET 职业任务分类，以确保对任务的广泛、有代表性的覆盖（U.S. Bureau of Labor Statistics, 2025a）。任务特征的更多细节见第 A.4 节。为评估任务质量，我们请职业专家按难度、代表性、完成时间以及相对其职业真实世界标准的整体质量为每个任务评分。每个任务的美元价值通过平均估计完成时间乘以 OEWS 数据（U.S. Bureau of Labor Statistics, 2025b）中相应职业的中位时薪估算。

### 2.4 任务质量控制流水线

![Refer to caption](2510.04374v1/assets/reviewdiagram_0923.png)

图 3：任务经过多轮评审以确保真实性与质量。

GDPval 完整集的全部 1,320 个任务都经过一个迭代评审流水线，其中既有基于模型的自动筛查，也有多阶段的人类专家评审。每个任务平均获得五次人类评审（最少三次）。

![Refer to caption](2510.04374v1/assets/no_logo_grading.png)

（a）两两对比评分设置

![Refer to caption](2510.04374v1/agreement_with_humans.png)

（b）与人类的一致性

图 4：GDPval 使用两两专家对比进行评分。我们还创建了一个实验性自动评分器。我们发现自动评分器与人类的一致性在 GDPval 黄金子集上与人类评分者之间的一致性相差不到 5%。

在所有评审阶段，专家都提供详细意见，任务在后续评审前被迭代修改以提升质量与代表性，详见第 A.5 节。

### 2.5 人类专家评分与自动评分

为给 220 个开源黄金子集评分，我们进行了盲评专家两两对比：相关职业的专家看到请求与参考文件，并被要求对两个或更多未标注的工作交付物排序。

平均而言，黄金子集的每次对比评分耗时超过一小时。我们另请了职业专家为人类与模型的交付物评分。专家为其选择与排序提供了详细理由，使我们能够计算各模型相对人类专家完成结果的核心胜率。

对黄金子集，我们训练了一个实验性评分模型，以行业专业专家的风格执行两两对比。尽管能力有限，自动评分器比专家评分更快更便宜，与人类专家评分者的一致性为 66%，仅比人类专家相互之间 71% 的一致性低 5%。更多细节见第 A.6 节。

## 3 实验与结果

### 3.1 核心结果

![Refer to caption](2510.04374v1/assets/gdpval_winrates.png)

图 5：在人类两两对比中，模型正开始在 GDPval 黄金子集上接近行业专家的水平。

![Refer to caption](2510.04374v1/assets/gdpval_openai_frontier_model_performance_over_time.png)

图 6：OpenAI 前沿模型在 GDPval 黄金子集上的表现随时间大致线性提升。

我们使用职业行业专家的盲评两两对比评估了 GPT-4o、o4-mini、o3、GPT-5、Claude Opus 4.1、Gemini 2.5 Pro 与 Grok 4[注2](#fn2)。Claude Opus 4.1 是 GDPval 黄金子集上表现最佳的模型，尤其在美观性（例如文档排版、幻灯片布局）上出色，而 GPT-5 尤其在准确性（例如严格遵循指令、执行正确计算）上出色，见图 8。这一区别也体现在第 A.2.4 节：GPT-5 在纯文本上表现更好，而 Claude 在 .pdf、.xlsx、.ppt 等文件类型上表现更好，展示了更强的视觉与审美能力[注3](#fn3)。在图 5 中，在 GDPval 黄金子集上，Claude Opus 4.1 的交付物有 47.6% 被评为好于（获胜）或等同于（平局）人类交付物。模型交付物在刚好过半的任务上胜过或追平了专家人类的交付物。

注 2：我们力求让对比尽可能盲评，但模型样本仍可能因风格差异被识别。OpenAI 输出常用破折号，Claude 输出常用第一人称表述，Grok 偶尔自称 Grok。虽然文件名已抹去模型标识，但为保持样本原貌，我们没有改动风格或内容，因此专家仍可能推断出模型的来源。我们通过 UI 对 Claude 采样以启用最多的 GDPval 相关功能。例如对 Claude，我们想评估其「升级版文件创建与分析」功能（https://www.anthropic.com/news/create-files）。对 OpenAI 模型，我们启用了网络搜索工具与代码解释器工具，并使用后台采样。我们还预装了基础镜像中没有的若干库，见第 A.6.4 节。对展示的图表，我们对每个提示采样每个模型 3 次，然后让 3 位不同的人类评分者为每个样本评分（即 220 个任务上每个提示、每个模型共 9 次对比）。

注 3：我们还要提醒，纯文本覆盖的职业与任务类型往往不同于涉及多模态的那些。

### 3.2 速度与成本比较

我们在第 A.2.1 节分析了若干场景，以理解前沿模型在 GDPval 黄金子集任务上的潜在速度与成本节省比[注4](#fn4)。在所分析的场景中，把前沿 AI 模型纳入专家工作流相对于无辅助的专家显示了节省时间与金钱的潜力。图 7 总结了「先试用模型，若仍不满意就自己修」设置下的预期节省。这里，专家人类从模型采样、审查输出，若不满意则重新采样并重复。若始终未获得满意的输出，则由人类自己完成任务。在这一设置以及其他设置（例如直接使用模型输出、动手前只试一次模型）下，模型辅助都可能为专家节省时间与金钱。

注 4：我们无法获得 Claude、Gemini 与 Grok 的成本估计。

![Refer to caption](2510.04374v1/assets/speed_cost_mult_no_v0.png)

图 7：在我们分析的场景中，模型展示了通过把 AI 辅助与专家人类监督相结合来节省时间与金钱的潜力。这里我们展示「试 $n$ 次，若仍不满意就自己修」方法的速度与成本节省，详见第 A.2.1 节。

### 3.3 模型的强项与弱项

我们构建了一个聚类流水线，分析专家为何偏好或拒绝 GPT-5 high、Claude Opus 4.1、Gemini 2.5 Pro 与 Grok 4 的交付物，如图 8 所示[注5](#fn5)。Claude、Grok 与 Gemini 最常因指令遵循失败而落败，而 GPT-5 high 主要因格式错误失分，指令遵循问题最少。Gemini 与 Grok 经常承诺却未能提供交付物、忽略参考数据或使用错误格式。GPT-5 与 Grok 的准确性错误最少，不过所有模型都偶尔捏造数据或算错。

注 5：样本用专家理由聚类；标签互斥，理由不清楚时留空。

![Refer to caption](2510.04374v1/assets/failure_modes_by_model.png)

图 8：在各模型中，专家最常因为模型未能完全遵循 GDPval 任务的指令而偏好人类交付物。

### 3.4 提高推理努力与脚手架

为理解推理努力对模型表现的影响，我们在低、中、高推理努力下对 o3 与 GPT-5 运行了 GDPval。我们发现额外的推理努力提升了表现。

我们还想衡量通过提示能多容易地提升模型能力。例如，观察到的许多 GPT-5 失败模式源于明显的格式错误。我们创建了一个提示，鼓励 GPT-5 严格检查交付物的正确性、通过把文件渲染为图像检查排版、避免非标准 Unicode 字符并避免过度冗长。该提示普遍适用于多模态经济任务，并未对任何特定问题过拟合（详见第 A.3 节）。我们还改进了智能体脚手架：在容器中启用 GET 请求，并用 GPT-5 评审做 N=4 的 best-of-N 采样。

该提示彻底消除了 GPT-5 回复中的黑方块伪影（此前影响超过一半的生成 PDF），并把 PowerPoint 文件中严重格式错误的比例从 86% 降到 64%。这在一定程度上归功于智能体使用其多模态能力检查交付物的比例急剧上升（15% → 97%）。该提示还把图 9(b) 中的人类偏好胜率提升了 5 个百分点。这些轻易取得的性能提升表明，通过训练或脚手架让智能体更彻底、更充分利用其多模态能力，是提升其在 GDPval 任务上表现的路径。

![Refer to caption](2510.04374v1/assets/reasoning_effort.png)

（a）推理努力实验

![Refer to caption](2510.04374v1/assets/prompt_tuning.png)

（b）提示调优实验

图 9：模型表现随推理努力的增加可预测地提升。提示调优与脚手架改进也提升了 GPT-5 的表现。

## 4 开源

我们开源 220 个任务黄金子集中的提示与参考文件。虽然人类专家对比仍是我们推荐的评分方法，但我们在 [evals.openai.com](https://evals.openai.com) 公开提供了一个实验性自动评分器。请注意，开源集中的任务已抹去可用于识别任务作者专家的信息。我们还要说明，受自动评分器限制所限，我们不为黄金子集中的所有任务提供自动评分结果。关于开源黄金子集的更多免责声明见第 A.1.3 节。

## 5 局限

##### 数据集规模：

GDPval 完整集目前仅包含 44 个职业、每职业 30 个任务。因此它只是知识工作任务的一个有限的初始切片，并非对所有可能职业任务的全面评估。我们正在扩大数据集规模。

##### 聚焦自包含的知识工作：

GDPval 初始版的任务围绕可在计算机上执行的知识工作，尤其是数字化交付物。体力劳动与实物任务不包括在当前版本中。此外，涉及大量默会知识、访问个人身份信息、使用专有软件工具或人际沟通的任务不在当前评估范围内。我们计划在未来版本的评估中在此基础上扩展。

##### 任务是精确规约的、一次性的，非交互式：

对 GDPval，我们在提示中提供任务的完整上下文，但现实中往往需要花力气弄清任务的完整上下文、理解该做什么。我们正在改进 GDPval，加入更多交互性与上下文真实感。与此同时，「上下文不足的 GDPval」一节的实验（第 A.2.7 节）展示了模型表现如何随上下文减少而下降。

##### 评分器表现：

与人类专家评分者相比，我们当前的自动评分器有若干局限。关于自动评分器的更多细节见第 A.6.2 节。

##### 成本：

构建并运行我们的评估很昂贵，尤其是使用行业专家评分者时。因此我们提供自动评分器代理，但不认为它可以完全替代行业专家评分者。

## 6 结论

在 GDPval 中，我们贡献如下：

1. 数据集：我们创建了衡量真实世界经济有价值任务的新评估数据集（GDPval）。

2. 能力基准：我们分析了人类行业专家与前沿 AI 模型在交付物质量、速度与成本上的对比。

3. 实验：我们测试了结果如何随推理努力、提示、脚手架与上下文的不同而变化。

4. 开源：我们开源了黄金子集的 220 个任务，包括提示与参考文件。

5. 自动评分器：我们在 [evals.openai.com](https://evals.openai.com) 发布自动评分器以提升评分的可及性。

我们希望本工作有助于追踪模型进展的科学，让我们有更好的数据评估 AI 模型的社会影响。

## 致谢

我们感谢 Abhishek Bhardwaj、Addea Gupta、AJ Ostrow、Aleksander Madry、Alexander Wei、Ally Bennett、Becky Waite、Ben Gaffney、Brad Lightcap、Casey Chu、Cassandra Duchan Solis、Charlotte Cole、Dane Stuckey、Eric Wallace、Erik Ritter、Evan Mays、Fidji Simo、Gideon Myles、Hannah Wong、Isa Fulford、Jakub Pachocki、James Lennon、Jared Pochtar、Jason Kwon、Jordan Frand、Julie Steele、Justin Wang、Kai Chen、Karthik Rangarajan、Kevin Liu、Larry Summers、Leo Liu、Leon Maksin、Leyton Ho、Lindsay McCallum、Livvy Pierce、Manoli Liodakis、Mark Chen、Max Schwarzer、Miles Palley、Miles Wang、Nakul Khanna、Nat McAleese、Natalie Kim、Nicholas Carlini、Nick Otis、Nick Ryder、Noam Brown、Noel Bundick、Paul Radulovic、Phillip Guo、Prashanth R、Rachel Brown、Raoul de Liedekerke、Robert Rotsted、Ronnie Chatterji、Ryan Kaufman、Ryan Rotsted、Sam Altman、Sam Bowman、Sherwin Wu、Tom Cunningham、Tom Stasi、Tony Song、Trevor Creech、Wenda Zhou、Wenlei Xie、Wyatt Thompson 与 Yara Khakbaz 的讨论、协助与评审。我们也感谢供应商合作伙伴在整个研究过程中的协作与支持，并特别感谢为 GDPval 贡献时间与专业知识的行业专家，没有他们本工作不可能完成。

## 参考文献

- Acemoglu (2025)

  Daron Acemoglu.
  The simple macroeconomics of ai.
  *Economic Policy*, 40(121):13–58, 2025.
- Acemoglu & Autor (2011)

  Daron Acemoglu and David Autor.
  Skills, tasks and technologies: Implications for employment and
  earnings.
  In *Handbook of labor economics*, volume 4, pp. 1043–1171.
  Elsevier, 2011.
- Appel et al. (2025)

  Ruth Appel, Peter McCrory, Alex Tamkin, Michael Stern, Miles McCain, and Tyler
  Neylon.
  Anthropic economic index report: Uneven geographic and enterprise ai
  adoption.
  *Anthropic Research*, 2025.
  URL
  <https://www.anthropic.com/research/anthropic-economic-index-september-2025-report>.
- Bick et al. (2024)

  Alexander Bick, Adam Blandin, and David J Deming.
  The rapid adoption of generative ai.
  Technical report, National Bureau of Economic Research, 2024.
- Brynjolfsson & Hitt (2000)

  Erik Brynjolfsson and Lorin M. Hitt.
  Beyond computation: Information technology, organizational
  transformation and business performance.
  *Journal of Economic Perspectives*, 14(4):23–48, 2000.
  doi: 10.1257/jep.14.4.23.
  URL <https://www.aeaweb.org/articles?id=10.1257/jep.14.4.23>.
- Brynjolfsson et al. (2017)

  Erik Brynjolfsson, Daniel Rock, and Chad Syverson.
  Artificial intelligence and the modern productivity paradox: A clash
  of expectations and statistics.
  Working Paper 24001, National Bureau of Economic Research, November
  2017.
  URL <http://www.nber.org/papers/w24001>.
- Brynjolfsson et al. (2025)

  Erik Brynjolfsson, Danielle Li, and Lindsey Raymond.
  Generative ai at work.
  *The Quarterly Journal of Economics*, 140(2):889–942, 2025.
- Chatterji et al. (2025)

  Aaron Chatterji, Thomas Cunningham, David J Deming, Zoe Hitzig, Christopher
  Ong, Carl Yan Shan, and Kevin Wadman.
  How people use chatgpt.
  Working Paper 34255, National Bureau of Economic Research, September
  2025.
  URL <http://www.nber.org/papers/w34255>.
- Chen et al. (2025)

  Wilbur Xinyuan Chen, Suraj Srinivasan, and Saleh Zakerinia.
  Displacement or complementarity?: The labor market impact of
  generative ai.
  *Harvard Business School*, 2025.
- David (1990)

  Paul A. David.
  The dynamo and the computer: An historical perspective on the modern
  productivity paradox.
  *American Economic Review*, 80(2):355–361,
  1990.
  URL
  <https://econpapers.repec.org/RePEc:aea:aecrev:v:80:y:1990:i:2:p:355-61>.
- Dwivedi et al. (2021)

  Yogesh K Dwivedi, Laurie Hughes, Elvira Ismagilova, Gert Aarts, Crispin Coombs,
  Tom Crick, Yanqing Duan, Rohita Dwivedi, John Edwards, Aled Eirug, et al.
  Artificial intelligence (ai): Multidisciplinary perspectives on
  emerging challenges, opportunities, and agenda for research, practice and
  policy.
  *International journal of information management*, 57:101994, 2021.
- Eloundou et al. (2023)

  Tyna Eloundou, Sam Manning, Pamela Mishkin, and Daniel Rock.
  Gpts are gpts: An early look at the labor market impact potential of
  large language models, 2023.
  URL <https://arxiv.org/abs/2303.10130>.
- Federal Reserve Bank of St. Louis (2025)

  Federal Reserve Bank of St. Louis.
  Value added by industry as a percentage of gross domestic product.
  FRED Release Tables, 2025.
  URL
  <https://fred.stlouisfed.org/release/tables?rid=331&eid=211>.
  Accessed: 2025-09-03.
- Hendrycks et al. (2020)

  Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn
  Song, and Jacob Steinhardt.
  Measuring massive multitask language understanding.
  *arXiv preprint arXiv:2009.03300*, 2020.
  doi: 10.48550/arXiv.2009.03300.
  URL <https://arxiv.org/abs/2009.03300>.
- Liu et al. (2023)

  Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu,
  Hangliang Ding, Kaiwen Men, Kejuan Yang, Shudan Zhang, Xiang Deng, Aohan
  Zeng, Zhengxiao Du, Chenhui Zhang, Sheng Shen, Tianjun Zhang, Yu Su, Huan
  Sun, Minlie Huang, Yuxiao Dong, and Jie Tang.
  Agentbench: Evaluating llms as agents.
  *arXiv preprint arXiv:2308.03688*, 2023.
  doi: 10.48550/arXiv.2308.03688.
- Miserendino et al. (2025)

  Samuel Miserendino, Michele Wang, Tejal Patwardhan, and Johannes Heidecke.
  Swe-lancer: Can frontier LLMs earn $1 million from real-world
  freelance software engineering?
  *arXiv preprint arXiv:2502.12115*, 2025.
- Panickssery et al. (2024)

  Arjun Panickssery, Samuel R. Bowman, and Shi Feng.
  Llm evaluators recognize and favor their own generations, 2024.
  URL <https://arxiv.org/abs/2404.13076>.
- Phan et al. (2025)

  Long Phan et al.
  Humanity's last exam.
  *arXiv preprint arXiv:2501.14249*, 2025.
- Rein et al. (2023)

  David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe
  Pang, Julien Dirani, Julian Michael, and Samuel R. Bowman.
  GPQA: A graduate-level google-proof q&a benchmark.
  *arXiv preprint arXiv:2311.12022*, 2023.
  doi: 10.48550/arXiv.2311.12022.
  URL <https://arxiv.org/abs/2311.12022>.
- Solow (1987)

  Robert M. Solow.
  We'd better watch out.
  *New York Times Book Review*, pp.  36, July 1987.
  URL
  <https://www.standupeconomist.com/pdf/misc/solow-computer-productivity.pdf>.
- Tamkin et al. (2024)

  Alex Tamkin, Miles McCain, Kunal Handa, Esin Durmus, Liane Lovitt, Ankur Rathi,
  Saffron Huang, Alfred Mountfield, Jerry Hong, Stuart Ritchie, Michael Stern,
  Brian Clarke, Landon Goldberg, Theodore R. Sumers, Jared Mueller, William
  McEachen, Wes Mitchell, Shan Carter, Jack Clark, Jared Kaplan, and Deep
  Ganguli.
  Clio: Privacy-preserving insights into real-world ai use.
  *arXiv preprint arXiv:2412.13678*, 2024.
  doi: 10.48550/arXiv.2412.13678.
  URL <https://arxiv.org/abs/2412.13678>.
- U.S. Bureau of Labor
  Statistics (2025a)

  U.S. Bureau of Labor Statistics.
  Occupational outlook – occupational data.
  <https://www.bls.gov/emp/data/occupational-data.htm>,
  2025a.
  Accessed: 2025-09-03.
- U.S. Bureau of Labor
  Statistics (2025b)

  U.S. Bureau of Labor Statistics.
  Occupational employment and wage statistics: May 2024 national
  tables.
  <https://www.bls.gov/oes/tables.htm>, 2025b.
  Data reference May 2024; accessed: 2025-09-03.
- U.S. Department of Labor, Employment and Training
  Administration (2024)

  U.S. Department of Labor, Employment and Training Administration.
  Work activities - o⁢net 28.3 data dictionary.
  <https://www.onetcenter.org/dictionary/28.3/excel/task_ratings.html>,
  2024.
  Accessed: 2025-04-20.

## 附录 A 附录

### A.1 免责声明

#### A.1.1 AI 使用声明

我们使用 AI 模型协助文献综述与论文语言的润色。我们也在日常工程工作流中使用了 AI 编程助手（例如帮助查找与修复 bug）。

#### A.1.2 敏感内容与政治内容声明

GDPval 中的一些任务包含 NSFW 内容，涉及性、酒精、粗俗语言与政治等主题。我们选择保留这些任务，因为它们反映了各种职业（例如电影、文学、法律、政治）真实面对的主题。我们不认可任何内容中的具体行为或观点。

#### A.1.3 第三方引用声明

GDPval 包含对第三方品牌与商标的有限引用，仅用于研究与评估目的。无意暗示任何隶属或背书关系。所有商标均为其各自所有者的财产。本数据集中的部分图像与视频包含 AI 生成的个体以及已获得授权的真实人物。GDPval 中私人个体的姓名与识别性引用均属虚构。与真实人物或实体的任何相似纯属巧合。

### A.2 实验结果的更多细节

#### A.2.1 速度与成本分析（续）

我们使用以下定义：

1. 人类专家完成时间 $H_{T}$ 是人类专家完成一个任务所需的时间，基于经核实的自报完成时间[注6](#fn6)。为计算人类专家完成成本 $H_{C}$，我们把每个职业自报的任务完成小时数乘以该职业的中位时薪（U.S. Bureau of Labor Statistics, 2025b）[注7](#fn7)。平均而言，在我们的 220 个黄金子集上 $H_{T}=404$ 分钟、$H_{C}=\$361$。

   注 6：提交时，专家自报完成每个任务所需的现实世界时间。多位职业评审者独立核验了这些时间并纠正了错误。由于时间是自报的，专家可能低估或高估了所花时间。

   注 7：由于我们的专家是因其领域内的丰富经验而被专门招募的，这些工资估计可能低估了他们真实的市场成本。

2. 人类专家审查时间 $R_{T}$ 是人类专家评分者评估一个模型交付物所需时间的估计。我们从任务监控软件观察到这一点，取每位人类专家第一次被要求给该题评分所花时间的平均值。平均而言 $R_{T}=109$ 分钟，相应的人类专家审查成本 $R_{C}$ 平均为 86 美元，$R_{C}$ 同样基于所花时间乘以中位工资数据计算。

3. 模型完成时间 $M_{T}$ 是模型完成一个交付物所花的时间，$M_{C}$ 是相应的完成成本，基于给定提示时模型完成交付物的实测 API 速度与成本[注8](#fn8)。

   注 8：对每个任务，我们为每个模型收集三次 API 补全，并对 API 元数据中记录的响应时间取平均。我们还记录了每个任务的平均计费成本。

4. 模型胜率 $w$ 是模型交付物被人类专家评分者评为好于人类交付物的频率。

然后我们计算以下比率：

1. 朴素比率：为衡量人类交付物与模型交付物的比率，不考虑任何质量差异或实施时间，我们直接用人类的平均任务完成时间除以模型的平均采样时间：$H_{T}/M_{T}$，成本同理：$H_{C}/M_{C}$。

2. 试 1 次再自己修比率：用这一方法计算时间时，我们取模型的采样时间，加上专家评估质量的审查时间 $R_{T}$，然后以概率 $(1-w_{i})$ 加上该模型在任务 $i$ 上所需修复的人类完成时间，得到 $T_{1,i}$，成本同理得到 $C_{1,i}$：

   $$\mathbb{E}[T_{1,i}] = M_{T,i}+R_{T,i}+(1-w_{i})H_{T,i} \tag{1}$$

   $$\mathbb{E}[C_{1,i}] = M_{C,i}+R_{C,i}+(1-w_{i})H_{C,i} \tag{2}$$

   平均花费时间为 $T_{1}=\mathbb{E}[T_{1,i}]$，对所有任务 $i$ 边际化，$C_{1}$ 同理。这近似于这样的设置：人类尝试用 GPT-5 完成一个任务，评估其质量，若交付物质量低于其质量标准则自己完成任务。我们对时间节省比的代入估计为：$H_{T}/(M_{T}+R_{T}+(1-w)H_{T})=H_{T}/\hat{T}_{1}$，其中使用经验均值 $\hat{T}_{1}$。相应的成本比为 $H_{C}/(M_{C}+R_{C}+(1-w)H_{C})$。

3. 试 $n$ 次再自己修比率：用这一方法计算时间时，我们取模型的采样时间，加上专家评估质量的审查时间 $R_{T}$，再加上该模型所需修复的人类完成时间（基于 $1-w_{i}$）[注9](#fn9)。在人类介入修复之前，我们跨 $n$ 次重采样与重新评估重复这一过程：

   注 9：这里我们对模型惩罚过重，因为每次完成后的胜率可能上升（因为专业人士会调整给模型的提示来修复错误），而且随着专业人士对任务越来越熟悉，审查时间也会下降。

   $$\mathbb{E}[T_{n,i}] =\sum_{k=1}^{n}\bigl((1-w_{i})^{\,k-1}(M_{T,i}+R_{T,i})\bigr)\;+\;(1-w_{i})^{\,n}H_{T,i} \tag{3}$$

   $$=\left(M_{T,i}+R_{T,i}\right)\frac{1-(1-w_{i})^{n}}{w_{i}}+(1-w_{i})^{n}H_{T,i} \tag{4}$$

   $$\mathbb{E}[C_{n,i}] =\sum_{k=1}^{n}\bigl((1-w_{i})^{\,k-1}(M_{C,i}+R_{C,i})\bigr)\;+\;(1-w_{i})^{\,n}H_{C,i} \tag{5}$$

   $$=\left(M_{C,i}+R_{C,i}\right)\frac{1-(1-w_{i})^{n}}{w_{i}}+(1-w_{i})^{n}H_{C,i} \tag{6}$$

   这近似于这样的设置：人类对一个任务尝试 $n$ 轮 GPT-5，每次评估其质量，若所有尝试后模型质量仍低于其质量标准则自己完成。如前所述，平均花费时间为 $T_{n}=\mathbb{E}[T_{n,i}]$，对所有任务 $i$ 边际化，$C_{n}$ 同理。因此，当 $n\to\infty$ 且 $w>0$ 时，时间节省为 $H_{T}/((M_{T}+R_{T})/w)$ 倍快，成本节省为 $H_{C}/((M_{C}+R_{C})/w)$ 倍便宜（相对人类专家）。

表 2：不同审查策略下的速度与成本改进。

|  |  | 速度改进 |  |  | 成本改进 |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 模型 | 胜率 | 朴素 | 试 1x | 试 $n$x | 朴素 | 试 1x | 试 $n$x |
| gpt-4o | 12.5% | 327x | 0.87x | 0.46x | 5172x | 0.90x | 0.53x |
| o4-mini | 29.1% | 186x | 1.02x | 1.06x | 1265x | 1.06x | 1.22x |
| o3 | 35.2% | 161x | 1.08x | 1.28x | 480x | 1.13x | 1.47x |
| gpt-5 | 39.0% | 90x | 1.12x | 1.39x | 474x | 1.18x | 1.63x |

当把审查与重做工作的时间纳入考虑后，使用模型的回报缩小了。我们没有考虑审查人类专业交付物所需的时间，尽管这在 GDPval 的任务中通常会发生（专业人士对自身工作的自查，或主管对团队成员工作的审查）。我们也没有考虑人类交付物同样不合人意的可能性。这一分析的另一个局限是没有捕捉灾难性错误的代价，而后者在某些领域可能代价极高。

#### A.2.2 按部门的胜率

我们在图 10 中提供部门层面的胜率分解。各行业结果不同。一些部门所有模型的胜率都低，而在另一些部门（例如政府、零售贸易与批发贸易），最强模型在 GDPval 任务上接近持平。

![Refer to caption](2510.04374v1/assets/gdpval_pairwise_expert_preferences_by_sector_3x3.png)

图 10：按部门的胜率

#### A.2.3 按职业的胜率

我们在图 11 中提供按职业的详细胜率分解。结果各异：一些职业在所有模型上胜率持续偏低，而另一些职业在多个模型间接近持平。

![Refer to caption](2510.04374v1/assets/gdpval_pairwise_expert_preferences_by_occupation_grid.png)

图 11：按职业的胜率

#### A.2.4 按交付物的胜率

我们在图 12 中报告按交付物类型的胜率。不同格式表现各异，Claude 在除纯文本外的所有交付物上取得最佳结果。GPT-5 high 在纯文本输出上领先，但总体胜率仍然偏低。

![Refer to caption](2510.04374v1/assets/model_winrate_by_deliverable_file_extension.png)

图 12：按交付物文件类型的胜率

#### A.2.5 按完成时间的胜率

我们在图 13 中报告按任务时长的胜率。较短任务（0-2 小时）的胜率最高，并随完成时间增加而稳步下降。这表明模型在较快、时间密集度较低的任务上表现最好。

![Refer to caption](2510.04374v1/assets/gdpval_model_winrate_by_time_to_complete.png)

图 13：按任务完成时间的胜率

#### A.2.6 模型失败分析的更多细节

我们选取 GPT-5 模型失败的子集（GPT-5 交付物输给人类专家的任务），然后请其他职业专家评分者把这些子集样本评为：

1. 灾难性：模型完成结果若在现实中使用将是灾难性的，因为它有害或危险地错误（例如侮辱客户、给出错误诊断、推荐欺诈或建议会造成人身伤害的行动）。

2. 恶劣：完成结果糟糕且不适用，但无冒犯性或危险性（例如语无伦次的胡言乱语、完全无关或前后矛盾的回答）。

3. 可接受但欠佳：完成结果可接受（可以使用），但人类产出了更强的回答（例如模型回答相比人类缺少有用的细节）。

4. N/A：不认同原专家评分者；模型完成结果好于人类完成结果。

![Refer to caption](2510.04374v1/assets/failures_analysis.png)

图 14：专家按失败严重程度对 GPT-5 模型失败进行分类评分。

GPT-5 模型失败最常见的归类是「可接受但欠佳」。另有约 29% 的评分属于恶劣或灾难性（其中约 3% 的失败被标为灾难性）。23% 的「模型更好」评分大致对应我们在图 4(b) 中观察到的评分者之间的一致性水平。

#### A.2.7 上下文不足的 GDPval

为评估模型如何处理任务歧义，我们创建了故意降低上下文提示的 GDPval 修改版。这些更短的提示省略了额外上下文，例如在参考文件中到哪里找特定数据、如何着手解决问题或最终交付物的详细格式期望；模型必须「自己想明白」。平均而言，修改后的提示长度（按 token 数）为原提示的 42%。

这一设置帮助衡量了此前评估未涉及的一项专业知识工作能力：通过弄清该做什么、从哪里获得必要输入来驾驭歧义。我们收集了 GPT-5 的完成结果并由专家人类评分者评分，发现模型在规约不足的提示上表现更差。特别是，模型难以弄清上下文。

需要说明：该实验是在 GDPval 黄金子集的较早版本上运行的，因此观察到的胜率与论文正文中的不一致。

![Refer to caption](2510.04374v1/assets/underspecified_gdpval.png)

图 15：在 GDPval 的规约不足版本上，GPT-5 表现更差，因为它难以弄清所需的上下文。

### A.3 提示调优的更多细节

以下是我们给智能体以激发能力的提示（略作编辑，去除了我们脚手架设置的一些具体细节）。

提示

```text
Special characters
- Never use the character ‑ (U+2011), since it will render poorly on some people’s computers. Instead, always use - (U+002D) instead.
- Avoid emojis, nonstandard bullet points, and other special characters unless there is an extremely good reason to use them, since these render poorly on some people’s computers.
Graphics embedded within PDFs/slides
- Make sure that any diagrams or plots are large enough to be legible (though not so large that they are ugly or cut off). In most cases they should be at least half the page width.
- Plots and charts to visualize data are good. Simple graphics (like a flowchart with arrows) are good. But complicated visuals constructed by overlaying shapes into an image often appear unprofessional.
PDFs
- Always use LibreOffice to create the PDF (it must be LibreOffice! If LibreOffice is not installed, you can install it yourself). Other libraries sometimes show weird artifacts on some computers.
Fonts
- Always use fonts which are available across all platforms. We recommend Noto Sans / Noto Serif unless there is an extremely good reason to use something else. If you must use another font, embed the font in the pptx/word/etc doc.
Deliverable text
- Do not link to submitted files in the deliverable text (links are not supported on the interface where these will be viewed).
- Ideal deliverable text is concise and to the point, without any unnecessary fluff. 4 sentences max.
- Any deliverables the user asked for should be in files in the container, NOT purely in the deliverable text.
- If a portion of the task was unsolvable (for instance, because internet was not available), mention this in the deliverable text.
- Your submission should be complete and self-contained. Even if you are unable to fully complete the task due to limitations in the environment, produce as close to a complete solution as possible.
Verbosity
Always be clear and comprehensive, but avoid extra verbosity when possible.
Filetypes
If the prompt does not request a specific filetype, use ”standard” filetypes like PDF, PPTX, DOCX, XLSX, MP4, ZIP, etc.
Video files (mp4, mov)
Extract a string of images from the video files and check the images to see whether the visual elements are corrupted.
Mandatory formatting checks
Before you submit your deliverable, you MUST perform the following mandatory formatting checks. Take your time, do these thoroughly, they are extremely important!
STEP 1: Convert all visual deliverables to PNGs using LibreOffice. This includes pptx, docx, pdf, xlsx, etc. Convert it so that each page or slide is a separate PNG. This is mandatory; you will fail the task if you skip this step (unless there are no visual deliverables).
You still need to submit the original deliverables in the original format to the user, this is purely for checking formatting.
STEP 2: Display the PNGs. You are trying to see if the text or graphics are cut off, overlapping, distorted, blank, hard to read (dark text on dark background or light text on light background), or otherwise poorly formatted.
Look at each image thoroughly, zoom in if you need to see more closely.
Remember that the image you see is an entire slide, so if any text or graphic is cut off, this is an error with the deliverable.
STEP 3: Programmatic formatting checks. For highly visual submissions (e.g. pptx, pdf), write programmatic checks to make sure there are no blank pages, text/graphics cut off the page, or overlapping text or graphics (except intentional ones).
Also check that if there is a page or slide limit, it is respected.
STEP 4: Summarize the prompt’s deliverable instructions, and match that to the portion of the deliverable that addresses it.
STEP 5: Right before submitting, check that the deliverables you have produced are exactly what you want to submit: deliverables should contain exactly the files you want to submit, with no extra files.
Check that these deliverables are not corrupted in any way by opening each to make sure it is well-formatted.
If any of these checks reveal a formatting issue, fix them and go through steps 1-5 again. Take your time, be thorough, remember you can zoom in on details.
This is IMPORTANT and MANDATORY, go through each step one-by-one meticulously! Every formatting error is a MAJOR ISSUE THAT YOU NEED TO FIX! There is no time limit, be thorough, go slide by slide or page by page.
Finally – on the last line of your output text, add CONFIDENCE[XX], where XX is an integer between 0 and 100, inclusive, indicating your confidence that the submission is correct, follows instructions, and is well-formatted.
```

我们按如下方式执行 best-of-N 采样：用提示、参考文件与交付物文件提示一个 GPT-5 评分器，提供四个不同的提交，然后让它选出最好的一个。

### A.4 更多任务特征

表 3：GDPval 黄金子集任务的汇总统计

|  | 均值 | 标准差 | 最小 | 25% | 50% | 75% | 最大 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 整体质量（1–5） | 4.47 | 0.32 | 3.18 | 4.30 | 4.50 | 4.70 | 5.00 |
| 难度（1–5） | 3.32 | 0.95 | 1.00 | 3.00 | 3.00 | 4.00 | 5.00 |
| 代表性（1–5） | 4.50 | 0.74 | 2.00 | 4.00 | 5.00 | 5.00 | 5.00 |
| 平均完成时间（小时） | 9.49 | 13.75 | 0.50 | 2.38 | 5.00 | 10.00 | 100.00 |
| 任务美元价值 | $398.46 | $599.45 | $12.59 | $93.72 | $174.81 | $386.03 | $4,114.20 |

表 4：GDPval 完整集任务的汇总统计

|  | 均值 | 标准差 | 最小 | 25% | 50% | 75% | 最大 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 整体质量（1–5） | 4.55 | 0.43 | 2.00 | 4.33 | 4.56 | 5.00 | 5.00 |
| 难度（1–5） | 3.20 | 0.92 | 1.00 | 3.00 | 3.00 | 4.00 | 5.00 |
| 代表性（1–5） | 4.43 | 0.76 | 1.00 | 4.00 | 5.00 | 5.00 | 5.00 |
| 平均完成时间（小时） | 8.63 | 24.70 | 0.25 | 2.00 | 4.00 | 8.00 | 605.00 |
| 任务美元价值 | $391.44 | $1,296.67 | $8.53 | $70.70 | $147.31 | $354.12 | $32,028.70 |

#### A.4.1 文件与附件

许多传统评估依赖文本进、文本出的任务格式。GDPval 任务纳入了广泛的真实世界文件类型（例如电子表格、文档、演示文稿、图像、音频、视频以及 CAD 等专用格式）。67.7% 的任务需要与至少一个参考文件交互。

表 5：GDPval 黄金集任务的文件数量

|  | 均值 | 标准差 | 最小 | 25% | 50% | 75% | 最大 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 参考文件 | 1.92 | 3.47 | 0.00 | 0.00 | 1.00 | 2.00 | 38.00 |
| 交付物文件 | 1.54 | 2.64 | 0.00 | 1.00 | 1.00 | 1.00 | 36.00 |

#### A.4.2 O*NET 任务、技能与工作活动

为确保广泛的职业代表性，我们分析了 GDPval 任务所代表的 O*NET [任务](https://www.onetcenter.org/dictionary/28.3/excel/task_statements.html)、[技能](https://www.onetcenter.org/dictionary/28.3/excel/skills.html)与通用[工作活动](https://www.onetcenter.org/dictionary/28.3/excel/work_activities.html)。数据集覆盖了 208 个唯一的 O*NET 任务、25 项职业技能与 26 项工作活动。

大多数 GDPval 任务涉及多个 O*NET 任务、技能与工作活动。

表 6：黄金集中 O*NET 任务、技能与工作活动的覆盖情况

|  |  |  |  |
| --- | --- | --- | --- |
|  | O*NET 中唯一总数 | 黄金子集中总数 | 覆盖率（%） |
| O*NET 技能 | 35 | 25 | 71.4% |
| O*NET 工作活动 | 41 | 26 | 63.4% |
| O*NET 任务 | 1,470 | 208 | 14.15% |

#### A.4.3 任务规约程度

执行人类评分的职业专家为每个提示中指令的明确程度评分。89.07% 的任务被评为规约良好，表明指令在清晰度与细节上接近现实世界的期望。

表 7：任务规约程度得分

| 标签 | %，黄金集 | %，完整集 |
| --- | --- | --- |
| 规约不足 | 8.28% | 8.41% |
| 规约良好 | 89.07% | 89.34% |
| 规约过度 | 2.66% | 2.26% |

#### A.4.4 任务代表性

专业服务
:   资质：技术与知识产权律师，曾在纽约与加州多家 AmLaw 100 律所担任合伙人，拥有 15 年以上就新兴技术、广告、反垄断与跨境争议及交易为客户提供咨询的经验。

    引语：「法律任务包含的细节贴近真实执业，比如有歧义的事实模式、把相关法律考量与非法律商业目标一同披露，以及真实的参考文档。」

医疗健康
:   资质：护理专业人士，18 年以上急诊医学、肾脏管理、护理协调与医疗运营经验。擅长质量保证、病例管理与专业教育。

    引语：「这些任务捕捉了该角色的复杂性，不仅需要敏锐地听懂医生的话，还要仔细注意临床准确性与专业格式。」

零售贸易
:   资质：战略零售高管，15 年通过全国大客户领导、10 亿美元以上损益管理与数据驱动全渠道战略做大高端与小众美妆品牌的经验。

    引语：「这些任务映射了我定期执行的工作，包括制定营收预测、进行竞争分析、构建高管级演示文稿，以及在全球组织内为关键零售合作伙伴推动战略举措。」

金融
:   资质：金融科技与华尔街领导者，20 年以上在全球机构与初创公司从事财富管理、资产管理与资本市场的经验。

    引语：「它们反映了细腻且个性化的真实世界场景，只有在该领域有多年经验的人才能完全理解。任务中使用的语言和细节直接取自实际行业实践，使其真实且有现实应用根基。」

批发贸易
:   资质：面向美国零售商销售的美国、中国、瑞典品牌/工厂的全国大客户销售经理，25 年以上经验。

    引语：「所有任务实际上都基于真实世界任务，配有备份参考文件与真实数据。」

制造业
:   资质：首席工业工程师，5 年以上管理大型项目并领导 10 人以上工程师团队进行工业运营的经验。

    引语：「重新设计任务尤其贴近真实实践，因为它们包含具体的设计组件与区块，以及带精确尺寸的详细图纸。它们强调可视性与优化步行距离等实用性考量以提高整体生产率，正是反映实际工程与运营优先级的那种注重细节的焦点。」

政府
:   资质：高管领导者，15 年以上在政府与非营利部门的住房、公共服务和劳动力市场项目的战略与运营层面工作。

    引语：「许多任务要求整合多种信息来源、做细腻的决策，并针对我们在职场上服务的不同受众量身定制工作。」

房地产与租赁
:   资质：资深商业地产经纪人，10 年投资销售、租赁以及管理地产办公室与经纪人的经验。

    引语：「这些任务捕捉了特定部门与环境所独有的动态与专业知识。」

信息业
:   资质：资深记者与内容领导者，20 年以上在顶级媒体、全球公司与高增长初创公司的经验。

    引语：「最重要的是，这些任务锚定于真实世界的挑战与职场目标。它们克服障碍、达成职场目标，并交付真实世界的解决方案与产品。」

关于专家资质的更多细节
少于 10% 的申请者被选中为完整集贡献任务。行业专家还带来职业多样性，代表不同的公司规模、地点与细分专业。每个职业至少有 5 名合格专业人士。

每个职业的专家都须依据 O*NET 职业定义（U.S. Bureau of Labor Statistics, 2025a），具备该具体职业与部门的从业经验。

### A.5 任务质量控制的更多细节

#### A.5.1 模型在环的任务评审

我们使用 OpenAI 模型按多项标准自动筛查每个任务提交，并标记可能的错误或遗漏，包括：确保任务与所选 O*NET 职业相关、验证请求涉及主要在计算机上执行的任务、标记任务复杂度过简（例如任务看似 5 分钟工作量而非较长期的工作）、以及指出未附交付物与参考文件。

因为模型可能出错，我们指导专家把模型反馈当作建议而非指令。专家对任务的准确性与完整性保有最终责任；模型不会自主改动任务。

#### A.5.2 人类专家评审者

人类评审者对每个任务进行多轮评审。评审者主要从原始专家池中选拔，依据是其在任务创建上表现出的卓越能力。最初，我们的研究人员人工评审所有任务，以识别持续产出高质量任务的专家；这些人接受培训并晋升为评审者。最熟练的评审者进一步培训为首席评审者，负责从专家池内识别、指导并晋升更多合格评审者。整个评审过程中，研究团队定期对评审者放行的任务做质量抽查，确保持续对齐质量标准。

#### A.5.3 迭代评审流程

迭代评审流程至少包括以下 3 个阶段：

1. 通才初审：一名通才评审者确认任务符合项目要求。

2. 职业专属专家评审：一名职业专属评审者评估任务对该职业的代表性，并确认在给定上下文下该职业的另一名成员可以完成该任务。

3. 最终迭代评审者反馈循环：第三名专家评审者提供迭代反馈，并与专家协作直到任务达到我们严格的质量标准。

### A.6 自动评分器细节

#### A.6.1 自动评分器一致性指标

为衡量自动评分器的表现，我们测量了自动评分器与人类专家评分者对同一样本给分之间的一致率。我们还比较了给同一样本评分的人类专家之间的评分一致性。

##### 人类-自动评分器一致性。

对给定样本 $s$，设人类分数 $H$ 与自动评分器分数 $A$ 取值于 $\{0,0.5,1\}$，其中 $1$ 表示偏好模型交付物，$0$ 表示偏好人类交付物，$0.5$ 表示平局。人类与自动评分器的一致性定义为

$$A_{s}^{\mathrm{HA}}=\mathbb{E}\bigl[1-|H-A|\bigr].$$

模型层面的人类-自动评分器一致性是该模型所有样本的 $A_{s}^{\mathrm{HA}}$ 的均值。

##### 人类评分者间一致性。

对给定样本 $s$，设人类分数 $H_{1}$ 与 $H_{2}$ 取值于 $p\in\{0,0.5,1\}$。我们把人类评分者间一致性测量为对两个随机抽取的人类评分的以下期望

$$A_{s}^{\mathrm{HH}}=\mathbb{E}\bigl[1-|H_{1}-H_{2}|\bigr].$$

对给定样本，我们用该样本所有评分对的样本均值估计这一量。一个模型的最终人类评分者间一致性是至少有两名人类评分者的所有样本的这些样本级分数的均值。既有的评分者信度统计量（如 Cohen's kappa、Fleiss' kappa 与 Krippendorff's alpha）在这里不那么直接适用，因为我们的评分者输出 $\{0,0.5,1\}$ 中的序数分数。

#### A.6.2 自动评分器相关性结果

在我们数据集的三轮自动评分器扫描中[注10](#fn10)，人类-自动评分器平均一致性为 65.7%，人类评分者间一致性为 70.8%。下图展示了自助法（对每个样本可用的自动评分器分数或人类评分做有放回重采样、计算每样本均值、再对所有样本或指定模型取平均）得到的 95% 置信区间。

注 10：指标在自动评分器未遇到系统错误且返回有效分数的所有样本上计算。我们还排除了 12 个任务（在我们 220 个开源评估集之外计）——由于后文描述的局限，自动评分器经常无法给这些任务评分或较不可能可靠评分。

我们的基于 GPT-5-high 的自动评分器在评估能力强的 OpenAI 模型的输出时，与人类专家评分者的相关性较低。这与模型往往偏好自身回答的经验证据相符（Panickssery et al., 2024）。对能力较弱的模型，两项一致性指标都最高，因为它们的输出更容易与人类交付物区分，也更不容易被偏好。

![Refer to caption](2510.04374v1/assets/agreement_with_humans_by_model.png)

图 16：对非 OpenAI 模型，人类-自动评分器平均一致性与人类评分者间一致性最接近。对能力较弱的模型，两项一致性指标都最高，因为它们更容易与人类交付物区分，也更不容易被选择。

#### A.6.3 自动评分器的局限

在开源集中，由于自动评分器的局限，我们把 220 个任务中的 12 个标记为不可评分。

1. 互联网访问：严格需要互联网的任务（例如要求智能体在线找音乐并下载的任务）无法评分，因为评分器没有互联网访问。

2. Python：自动评分器在一个只允许运行 Python 的容器中运行。因此我们排除了 3 个需要运行其他语言并下载外部依赖才能正确测试的软件开发者任务。

3. 字体包：尽管自动评分器有大多数度量上等同的字体（例如用 Liberation Sans 替代 Arial），人类交付物中使用的某些字体包仍会导致某些交付物的渲染与装有这些字体的计算机上的呈现不同。

4. 语音转文字：自动评分器在容器内的语音转文字功能有限，且难以处理非人声。

#### A.6.4 自动评分器软件包

为确保模型能处理 GDPval 中种类繁多的文件类型，以下软件包预装在基础生产 Docker 镜像中。这些软件包在 OpenAI 模型采样期间同样对智能体开放。

```
jupyter-client==8.6.1
jupyter-core==5.5.1
jupyter-server==2.14.0
jupyterlab==4.1.8
jupyterlab-pygments==0.3.0
jupyterlab-server==2.27.1
aiohttp==3.9.5
hypercorn==0.14.3
notebook==6.5.1
nbclassic==0.4.5
pydantic==1.10.2
fastapi[all]==0.95.2
websockets==10.3
tqdm==4.64.0
matplotlib==3.6.3
matplotlib-venn==0.11.6
numpy==1.24.0
numpy-financial==1.0.0
scipy==1.14.1
pandas==1.5.3
statsmodels==0.13.5
sympy==1.13.1
seaborn==0.11.2
scikit-learn==1.1.3
nltk==3.9.1
plotnine==0.10.1
shapely==1.7.1
fiona==1.9.2
geopandas==0.10.2
ffmpeg-python==0.2.0
pydub==0.25.1
moviepy==1.0.3
opencv-python==4.5.5.62
Pillow==9.1.0
python-docx==0.8.11
python-pptx==0.6.21
openpyxl==3.0.10
xml-python==0.4.3
geopy==2.2.0
scikit-image==0.20.0
folium==0.12.1
wordcloud==1.9.2
faker==8.13.2
fpdf2==2.8.3
soundfile==0.10.2
kerykeion==2.1.16
pdfkit==0.6.1
pycountry==20.7.3
countryinfo==0.1.2
tabulate==0.9.0
shap==0.39.0
pylog==1.1
pyprover==0.5.6
pytesseract==0.3.8
qrcode==7.3
basemap==1.3.9
pygraphviz==1.7
networkx==2.8.8
pyttsx3==2.90
nashpy==0.0.35
docx2txt==0.8
typing-extensions==4.10.0
torch==2.5.1
torchaudio==2.5.1
torchtext==0.18.0
torchvision==0.20.1
PyMuPDF==1.21.1
pdf2image==1.16.3
pyth3==0.7
h5py==3.8.0
tables==3.8.0
rarfile==4.0
odfpy==1.4.1
pymc==4.0.1
jax==0.2.28
pyxlsb==1.0.8
keras==2.6.0
xgboost==1.4.2
loguru==0.5.3
plotly==5.3.0
graphviz==0.17
fuzzywuzzy==0.18.0
pydot==1.4.2
gensim==4.3.1
pypandoc==1.6.3
einops==0.3.2
reportlab==3.6.12
gradio==2.2.15
mutagen==1.45.1
librosa==0.8.1
svglib==1.1.0
gtts==2.2.3
textblob==0.15.3
rasterio==1.3.3
rdflib==6.0.0
rdkit==2024.9.6
biopython==1.84
cairosvg==2.5.2
markdownify==0.9.3
anytree==2.8.0
pdfplumber==0.6.2
trimesh==3.9.29
svgwrite==1.4.1
pdfrw==0.4
pyzbar==0.1.8
dlib==19.24.2
mtcnn==0.1.1
imgkit==1.2.2
chardet==3.0.4
bokeh==2.4.0
tabula==1.0.5
camelot-py==0.10.1
exchange_calendars==3.4
weasyprint==53.3
pronouncing==0.2.0
cryptography==3.4.8
spacy==3.4.4
requests==2.31.0
mne==0.23.4
pyopenssl==21.0.0
snowflake-connector-python==2.7.12
databricks-sql-connector==0.9.1
ddtrace~=2.8.1
datadog~=0.49.1
pytest~=8.2.0
pytest-cov~=5.0.0
pytest-json-report~=1.5.0
coverage~=7.5.1
pytest-asyncio~=0.23.6
catboost~=1.2.7
lightgbm~=4.5.0
imblearn~=0.0
imbalanced-learn~=0.12.3
rapidfuzz~=3.10.1
```

我们还安装了以下额外软件包，并在提示中告知模型可以使用这些额外软件包：

```
libreoffice
aspose-words==25.8.0
av==11.0.0
cadquery==2.4.0
cadquery-ocp==7.7.0
pedalboard==0.9.9
pyloudnorm==0.1.1
srt==3.5.3
xlrd==2.0.1
```

### A.7 职业选择的更多方法论细节

把职业分配到部门。
我们使用美国劳工统计局（U.S. Bureau of Labor Statistics, 2025a）的 2023 年 BLS 全国就业矩阵，通过识别每个职业就业人数最多的部门把职业分配到部门。具体包括：筛选出「Line Item」职业、取 NAICS 代码前两位、剔除「总就业」行、汇总 2023 年就业、并把每个职业分配到就业份额最大的部门。

关于 O*NET 数据来源的细节

##### GDPval 中的职业。

我们通过筛选 2024 年 5 月 OEWS 全国就业与工资统计（U.S. Bureau of Labor Statistics, 2025b）中的「Detailed」职业得到 831 个职业，以排除任何汇总性就业类别。我们去掉了「All Other」职业——它们是一个较宽组别内的兜底类别，把不属于该组任何细分职业的职业捆在一起。去掉「All Other」职业后剩下 761 个职业。

##### 职业总工资的计算。

估计总工资对年薪岗位按总就业 × 平均年薪计算，对只有时薪的岗位按总就业 × 时薪 × 典型工作年 2080 小时计算。哪些岗位是年薪还是时薪的判定包含在 O*NET 数据中。2080 小时被劳工统计局（BLS）引为「典型工作年」，假设每周工作 40 小时。这是一个不完美的估计（例如 BLS 承认演员「通常并非全年每周工作 40 小时」），但是 BLS 提供的最精确估计。

##### 把职业分类为数字化。

为把职业分类为以数字化为主，我们采用基于任务的方法。对许多职业，O*NET 数据库包含任务陈述与评分，列出该职业从业者的所有任务[注11](#fn11)。O*NET 数据按 6 位 SOC 职业代码（SOC-6）层级提供。我们把 O*NET 的 SOC-6 职业及相应任务映射到按 4 位 SOC 层级（「SOC-4」）报告工资的 OEWS 数据集职业。对每个 SOC-4 职业，我们用同时接收职业与任务的 GPT-4o 提示模型把其任务分类为数字化或非数字化。然后我们计算每个职业数字化任务的加权占比。数字化占比超过 0.60 阈值的职业被分类为数字化。

注 11：注意虽然 O*NET 在任务数据中区分核心（Core）与补充（Supplemental）任务，我们在任务份额计算中同等对待这两类任务。

为计算加权任务份额的权重，我们使用 O*NET 调查的任务评分数据，其中包括该职业每个任务的相关性、频率与重要性[注12](#fn12)。我们首先为每个 6 位 SOC 职业与任务的组合计算「调整任务得分」（Adjusted Task Score）。该得分定义为三个归一化任务评分（任务频率、任务重要性、任务相关性）的简单平均。每个评分相对观察到的最大评分归一化（例如重要性满分为 5）[注13](#fn13)。

注 12：对没有 O*NET 28.3 任务评分的两个职业（「Facilities Managers」与「Medical Dosimetrists」），我们使用了 O*NET 29.0 的任务评分。

注 13：频率最大值为 7，重要性最大值为 5，相关性最大值为 100。若某任务缺少其中一项评分，我们用同一职业所有任务该项评分的均值插补。例如，若某任务缺少频率评分，我们赋予它该职业所有任务的平均归一化频率评分。

然后我们把这些 SOC-6 调整任务得分聚合为 SOC-4 调整任务得分（对每个 4 位 SOC 职业与任务的组合）。做法是对每个任务，把一个 SOC-4 职业内各 SOC-6 职业的 SOC-6 调整任务得分相加[注14](#fn14)。

注 14：若一个 SOC-4 职业只映射到一个 SOC-6 职业，则 SOC-6 与 SOC-4 调整任务得分相同。例如，SOC-4 职业 Computer Occupations, All Other 合并了两个 6 位 SOC 职业（Information Security Engineers 与 Penetration Testers），它们有一个共同任务：「Identify security system weaknesses, using penetration tests.」该任务有两个 SOC-6 调整任务得分，相加即得 SOC-4 调整任务得分。

接下来，我们对每个 4 位 SOC 职业与任务的组合计算「加权任务份额」（Weighted Task Share）。加权任务份额是该职业-任务对的调整任务得分除以该职业所有调整任务得分之和。对每个职业，其所有任务的加权任务份额之和为一。加权任务份额给出每个任务对给定职业相对重要性的度量。这些加权任务份额就是用于计算每个职业数字化任务加权占比的权重。

##### 缺失数据的处理。

1. 缺失任务陈述。OEWS 中一些职业缺少关联的任务陈述或评分。其中 47 个是没有组成任务的宽泛「All Other」类别[注15](#fn15)；另外 12 个在 O*NET 29.0（截至 2025 年 8 月）中被拆分为更细的子职业。对后者，我们纳入了其子职业在 O*NET 29.0 中的全部组成任务。我们如何映射这 12 个职业的具体对应关系如下：

   注 15：这些职业是：Entertainers and Performers, Sports and Related Workers, All Other；Postsecondary Teachers, All Other；Production Workers, All Other；Office and Administrative Support Workers, All Other；Teachers and Instructors, All Other；Surgeons, All Other；Information and Record Clerks, All Other；Community and Social Service Specialists, All Other；Educational Instruction and Library Workers, All Other；Sales and Related Workers, All Other；Education Administrators, All Other；Social Workers, All Other；Legal Support Workers, All Other；Food Preparation and Serving Related Workers, All Other；Personal Care and Service Workers, All Other；Food Processing Workers, All Other；Motor Vehicle Operators, All Other；Financial Clerks, All Other；Media and Communication Workers, All Other；Counselors, All Other；Social Sciences Teachers, Postsecondary, All Other；First-Line Supervisors of Protective Service Workers, All Other；Dentists, All Other Specialists；Material Moving Workers, All Other；Helpers, Construction Trades, All Other；Drafters, All Other；Media and Communication Equipment Workers, All Other；Metal Workers and Plastic Workers, All Other；Cooks, All Other；Designers, All Other；Life Scientists, All Other；Building Cleaning Workers, All Other；Precision Instrument and Equipment Repairers, All Other；Grounds Maintenance Workers, All Other；Religious Workers, All Other；Artists and Related Workers, All Other；Textile, Apparel, and Furnishings Workers, All Other；Gambling Service Workers, All Other；Transportation Workers, All Other；Extraction Workers, All Other；Entertainment Attendants and Related Workers, All Other；Woodworkers, All Other；Underground Mining Machine Operators, All Other；Agricultural Workers, All Other；Logging Workers, All Other；Rail Transportation Workers, All Other；Communications Equipment Operators, All Other。

   1. (a) Tour and Travel Guides：该 SOC 代码拆分为两个职业：[Tour Guides and Escorts](https://www.onetonline.org/link/summary/39-7011.00.) 与 [“Travel Guides”](https://www.onetonline.org/link/summary/39-7012.00)。我们把两个职业的任务相加。

   2. (b) Miscellaneous Construction and Related Workers：该 SOC 代码拆分为三个职业：[“Segmental Pavers”](https://www.onetonline.org/link/summary/47-4091.00)、[“Weatherization Installers and Technicians”](https://www.onetonline.org/link/summary/47-4099.03) 与 [“Construction and Related Workers, All Other”](https://www.onetonline.org/link/summary/47-4099.00)。我们加入了 “Segmental Pavers” 与 “Weatherization Installers” 的全部任务。“Construction and Related Workers, All Other” 是没有组成任务的通用职业类别。

   3. (c) Teaching Assistants：该 SOC 代码拆分为三个职业：[Teaching Assistants, Preschool, Elementary, Middle, and Secondary School, Except Special Education](https://www.onetonline.org/link/summary/25-9043.00)、[Teaching Assistants, Special Education](https://www.onetonline.org/link/summary/25-9044.00) 与 [Teaching Assistants, All Other](https://www.onetonline.org/link/summary/25-9049.00)。我们加入了前两者的任务。Teaching Assistants, All Other 是没有组成任务的通用职业类别。

   4. (d) Buyers and Purchasing Agents：该 SOC 代码拆分为三个职业：[Buyers and Purchasing Agents, Farm Products](https://www.onetonline.org/link/summary/13-1021.00)、[Wholesale and Retail Buyers, Except Farm Products](https://www.onetonline.org/link/summary/13-1022.00) 与 [Purchasing Agents, Except Wholesale, Retail, and Farm Products](https://www.onetonline.org/link/summary/13-1023.00)。我们把三个职业的任务相加。

   5. (e) Substance Abuse, Behavioral Disorder, and Mental Health Counselors：该 SOC 代码拆分为两个职业：[Substance Abuse and Behavioral Disorder Counselors](https://www.onetonline.org/link/summary/21-1011.00) 与 [Mental Health Counselors](https://www.onetonline.org/link/summary/21-1014.00)。我们把两个职业的任务相加。

   6. (f) Clinical Laboratory Technologists and Technicians：该 SOC 代码拆分为六个职业：[Medical and Clinical Laboratory Technologists](https://www.onetonline.org/link/summary/29-2011.00)、[Cytogenetic Technologists](https://www.onetonline.org/link/summary/29-2011.01)、[Cytotechnologists](https://www.onetonline.org/link/summary/29-2011.02)、[Histotechnologists](https://www.onetonline.org/link/summary/29-2011.04)、[Medical and Clinical Laboratory Technicians](https://www.onetonline.org/link/summary/29-2012.00) 与 [Histology Technicians](https://www.onetonline.org/link/summary/29-2012.01)。我们加入了所有这些职业的任务。

   7. (g) Special Education Teachers, Kindergarten and Elementary School：该 SOC 代码拆分为两个职业：[Special Education Teachers, Kindergarten](https://www.onetonline.org/link/summary/25-2055.00) 与 [Special Education Teachers, Elementary School](https://www.onetonline.org/link/summary/25-2056.00)。我们把两个职业的任务相加。

   8. (h) Home Health and Personal Care Aides：该 SOC 代码拆分为两个职业：[Home Health Aides](https://www.onetonline.org/link/summary/31-1121.00) 与 [Personal Care Aides](https://www.onetonline.org/link/summary/31-1122.00)。我们把两个职业的任务相加。

   9. (i) Property Appraisers and Assessors：该 SOC 代码拆分为两个职业：[Appraisers and Assessors of Real Estate](https://www.onetonline.org/link/summary/13-2023.00) 与 [Appraisers of Personal and Business Property](https://www.onetonline.org/link/summary/13-2022.00)。我们把两个职业的任务相加。

   10. (j) Miscellaneous Assemblers and Fabricators：该 SOC 代码拆分为两个职业：[Assemblers and Fabricators, All Other](https://www.onetonline.org/link/summary/51-2099.00) 与 [Team Assemblers](https://www.onetonline.org/link/summary/51-2092.00)。我们匹配到 Team Assemblers，因为 Assemblers and Fabricators, All Other 是没有组成任务的通用职业类别。

   11. (k) Electrical, Electronic, and Electromechanical Assemblers, Except Coil Winders, Tapers, and Finishers：该 SOC 代码拆分为两个职业：[Electrical and Electronic Equipment Assemblers](https://www.onetonline.org/link/summary/51-2022.00) 与 [Electromechanical Equipment Assemblers](https://www.onetonline.org/link/summary/51-2023.00)。我们把两个职业的任务相加。

   12. (l) First-Line Supervisors of Transportation and Material Moving Workers, Except Aircraft Cargo Handling Supervisors：该 SOC 代码拆分为四个职业：[First-Line Supervisors of Helpers, Laborers, and Material Movers, Hand](https://www.onetonline.org/link/summary/53-1042.00)、[First-Line Supervisors of Material-Moving Machine and Vehicle Operators](https://www.onetonline.org/link/summary/53-1043.00)、[First-Line Supervisors of Passenger Attendants](https://www.onetonline.org/link/summary/53-1044.00) 与 [First-Line Supervisors of Transportation Workers, All Other](https://www.onetonline.org/link/summary/53-1049.00)。我们加入了前三者的任务。First-Line Supervisors of Transportation Workers, All Other 是没有组成任务的通用职业类别。

2. 缺失任务评分。有 36 个 SOC-6 职业在 O*NET 28.3 或 29.0 中没有任何任务评分，对应 34 个 SOC-4 职业[注16](#fn16)。其中 2 个 SOC-4 职业（Data Scientists 与 Web and Digital Interface Designers）的部分组成 SOC-6 职业有任务评分，使我们能计算调整与加权任务份额。对其余 32 个没有 O*NET 任务评分的 SOC-4 职业，我们无法计算调整或加权任务份额。我们转而如下代理加权任务份额：对每个 4 位 SOC 职业与任务的组合，计算该任务在该职业中出现的次数（即任务频次）并除以该职业所有任务的任务频次之和。例如，4 位 SOC 职业「Special Education Teachers, Kindergarten and Elementary School」合并了两个 6 位 SOC 职业（Special Education Teachers, Elementary School 与 Special Education Teachers, Kindergarten），有 43 个唯一任务，其中 17 个出现两次。因此 43 个任务的任务频次之和为 60。对每个只出现一次的任务，代理加权任务份额为 1/60 = 0.0017；对每个出现两次的任务，代理加权任务份额为 2/60 = 0.0033。

   注 16：这些 SOC-4 职业是：Aircraft Service Attendants；Bus Drivers, School；Calibration Technologists and Technicians；Cardiologists；Crematory Operators；Data Scientists；Disc Jockeys, Except Radio；Emergency Medical Technicians；Emergency Medicine Physicians；Entertainment and Recreation Managers, Except Gambling；Financial and Investment Analysts；Financial Risk Specialists；First-Line Supervisors of Entertainment and Recreation Workers, Except Gambling Services；First-Line Supervisors of Security Workers；Fundraising Managers；Health Information Technologists and Medical Registrars；Hydrologic Technicians；Legislators；Lighting Technicians；Medical Records Specialists；Orthopedic Surgeons, Except Pediatric；Paramedics；Pediatric Surgeons；Project Management Specialists；Public Relations Managers；Sales Representatives of Services, Except Advertising, Insurance, Financial Services, and Travel；School Bus Monitors；Shuttle Drivers and Chauffeurs；Software Developers；Special Education Teachers, Kindergarten and Elementary School；Substitute Teachers, Short-Term；Taxi Drivers；Teaching Assistants, Except Postsecondary；Web and Digital Interface Designers。

#### A.7.1 验证数字化任务度量

我们把「知识工作」分类方法与 Acemoglu & Autor（2011）的任务内容框架做基准对比。

Acemoglu & Autor（2011）的框架基于美国劳工部的 O*NET 调查，该调查收集每个职业的活动、工作「内容」与所需能力的数据。该框架把这些度量聚合为五个分数：

1. 非常规认知：分析型。

2. 非常规认知：人际型。

3. 常规认知。

4. 常规手工。

5. 非常规手工体力。

每个分数由选定的 O*NET「重要性」量表组合计算。例如，每个职业的「非常规认知：分析型」分数由「分析数据/信息」工作活动、「创造性思考」工作活动与「为他人解读信息」工作活动的（归一化）值相加计算。一个职业某分数的数值高表明该职业重度依赖该类型工作。

我们为每个职业计算 Acemoglu & Autor（2011）分数，然后与我们的知识工作度量（即每个职业的数字化任务份额与二元的「知识工作」指示变量）比较。

在第一组结果中，我们把每个 Acemoglu & Autor（2011）任务内容分数与职业的数字化任务份额比较。模式很清晰：数字化任务份额较高的职业在非常规认知维度上系统性得分更高，在手工维度上更低。换言之，一个职业越依赖数字化任务，它就越像认知型、非常规的工作。

![Refer to caption](2510.04374v1/assets/acemoglu_task_scatterplot.png)

图 17：职业与任务内容的分布

在第二组结果中，我们考察 Acemoglu & Autor（2011）分数与我们的二元「知识工作」度量的关系。在下图中，我们绘出每个职业每个分数的取值，并按本文的知识工作分类给职业上色：蓝色为被识别为知识工作的职业，红色为其余职业。模式同样清晰——知识工作职业聚集在非常规认知分布的顶部以及常规与手工分布的底部。综合来看，这些结果表明我们的数字化任务分类与认知/手工工作的经济学文献高度一致。

![Refer to caption](2510.04374v1/assets/acemoglu_occupationcontent.png)

图 18：数字化任务与任务内容的散点图
