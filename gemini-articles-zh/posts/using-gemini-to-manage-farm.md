---
title: "Gemini Flash 智能体正在如何帮助一位密歇根州的奶农"
title_en: "How Gemini Flash agents are helping a Michigan dairy farmer"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/using-gemini-to-manage-farm/
site: gemini
date: 2026-07-28
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini Flash 智能体正在如何帮助一位密歇根州的奶农

> 原文：[How Gemini Flash agents are helping a Michigan dairy farmer](https://blog.google/innovation-and-ai/models-and-research/gemini-models/using-gemini-to-manage-farm/) · Google

奶牛养殖利润微薄，数据分析因此成为应对复杂生物与环境变量的关键。现代农场会产生海量的信息，挑战在于如何快速分析这些数据以作出决策。正因如此，Paul Windemuller 转向了 Gemini 3.6 Flash。

2014 年，Paul 和 Brittany 在密歇根州创办了 Dream Winds Dairy，最初只有 30 头租来的奶牛。12 年间，它发展成一座高度自动化的牧场，为 260 头荷斯坦牛挤奶。作为一名研究农业科技与 AI 的 2024 年 Nuffield International Farming Scholar（纳菲尔德国际农业学者），Paul 把奶牛养殖当作一项技术挑战来对待。

他的运营持续产生数据流：传感项圈追踪每一头牛，本地气象站记录气候指标，在线门户记录牛奶品质和出货。

然而，这些系统各自运行在彼此隔离的软件孤岛中。每天早晨，Paul 都要花几个小时下载文件、合并电子表格、计算绩效，这让他无法把时间真正花在照看牛群上。

## 把办公室工作委派给 AI 智能体

![仪表板总览](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/image1_4m3x82y.width-1200.format-webp.webp)

为了把时间夺回来，Paul 在 [Google Antigravity](https://antigravity.google/) 中用 [Gemini 3.6 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/) 搭建了一套本地多智能体 AI 系统，用以整合各自孤立的农场数据并计算每日盈利能力。

该系统没有采用 API 或网页抓取，而是使用基于本地目录的文件接口。当 CSV 数据导出文件，或纸质收据、PDF 和发票的照片被保存到受监控的文件夹时，Gemini 的多模态能力就会提取并合并视觉与数值指标——数据始终掌握在 Paul 自己手中。

一套专门的多智能体工作流用各司其职、相互协调的角色取代了冗长的提示词：

- **编排者（Orchestrator）：**管理整体的日常工作流。
- **摄取智能体（Ingestion Agents）：**对原始文件（挤奶机器人导出数据、饲料日志）进行标准化。
- **分析智能体（Analysis Agent）：**评估生物与天气的影响。
- **报告智能体（Reporting Agent）：**生成清晰的自然语言摘要。

这套系统会自动把原始文件转换成一份连贯的业务总览。

## 为小企业拉平竞争环境

归根结底，Paul 的抱负是让独立农户也能用上这些技术，以他自己经营业务的方式简化运营。对许多人来说，构建工具本身就是一道门槛；而即便有了工具，在农场规模上运行所带来的成本问题也必须解决。

这类需要持续推理、解析和工具执行的日常智能体化工作流，对像他这样的小企业来说过去成本过高。[Gemini 3.6 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-6-flash-3-5-flash-lite-3-5-flash-cyber/) 帮助 Paul 的日常运营变得更具成本效益。

Gemini 3.6 Flash 为高级推理、工具使用和编程而设计，配备 100 万 token 上下文窗口和 64,000 token 最大输出。[基准评测](https://artificialanalysis.ai/models/gemini-3-6-flash)显示，与 Gemini 3.5 Flash 相比，它的输出 token 减少约 17%，且每个输出 token 的成本更低，显著降低了运行智能体化循环的开销。

## 以静态变动毛利衡量成败

这套系统的设计目标是优化 Paul 的核心指标：每日静态变动毛利（Static Variable Margin，SVM）。与随牛奶和饲料价格波动而起伏的传统指标（如饲喂成本上收益 Income Over Feed Cost）不同，SVM 把市场价格固定不变，从而把真正的生物与运营效率从市场噪音中剥离出来。这让智能体化系统建立在 Paul 可以信赖的事实之上，为农场运营提供可付诸行动的洞察。

![各类饲喂与经济图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/image2_9p9esCS.width-1200.format-webp.webp)

## 智能体化工作流如何计算 SVM

- **生物表现**：摄取智能体解析产奶量、乳成分（乳脂/蛋白）、体细胞数和饲料数据。
- **静态收入**：根据历史支付标准（联邦第 33 号令 1 月价格）的固定价格，套算实际产出的牛奶固形物。
- **静态饲料成本**：使用固定的原料价格，以隔离实际饲料消耗量的变化。
- **静态饲喂成本上收益**：从静态收入中减去静态饲料成本。
- **变动成本**：减去每头牛的开销（替换牛、配种、兽医用品），同时不计间接费用（人工、水电、折旧），确保 SVM 的变化只反映生物效率和健康状况。

## 生成每日简报

算出数字只是成功的一半。忙碌的农户没时间每天凌晨 3 点去解读电子表格。为了节省时间，报告智能体会把结果翻译成一份每日「农场 CEO 简报」，突出当天的毛利驱动因素。例如，如果每头牛的 SVM 下降了 0.15 美元，它会精确指出具体原因：

- **干物质采食量**：-0.08 美元（湿度导致采食量下降）
- **体细胞数**：-0.04 美元（略有上升，提示潜在健康问题）
- **弃奶**：-0.03 美元（两头牛进入了治疗牛舍）

简报最后会给出可付诸行动的建议，比如调整通风以应对热应激。由于系统运行在本地文件导出之上，所有敏感数据都留在农场里。

## 帮独立小企业走出电子表格

Paul 在 Antigravity 中构建的智能体化系统，展现了小企业的一次重大转变。他希望这能启发并教会其他人，如何评估在日常工作中使用 AI。通过把多智能体架构与 Gemini 3.6 Flash 低成本的 token 效率相结合，他搭建了一个自动化运营层，消除了数小时的手工电子表格工作，让他得以走出办公室，专注于发展自己的事业。
