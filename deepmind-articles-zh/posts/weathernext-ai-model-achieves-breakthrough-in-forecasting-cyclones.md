---
title: "WeatherNext：AI 模型在气旋预报上取得突破"
title_en: "WeatherNext: AI model achieves breakthrough in forecasting cyclones"
source: https://deepmind.google/blog/weathernext-ai-model-achieves-breakthrough-in-forecasting-cyclones/
site: deepmind
date: 2026-08-06
crawled: 2026-09-13
translated: 2026-09-13
---

# WeatherNext：AI 模型在气旋预报上取得突破

> 原文：[WeatherNext: AI model achieves breakthrough in forecasting cyclones](https://deepmind.google/blog/weathernext-ai-model-achieves-breakthrough-in-forecasting-cyclones/) · Google DeepMind

WeatherNext 能够提供精准的气旋预报，相当于多出一天的预警时间。现在，我们正在将该模型开源。

预测危险气旋如何演变是一项长期的挑战，而在这场挑战中，每一个小时都至关重要。热带气旋——也被称为飓风或台风——是地球上最具破坏力的天气现象之一，过去 50 年间在全球造成了超过 70 万人死亡和 1.4 万亿美元的经济损失。对预报员而言，及时、准确地发布预警是一场与时间的持续赛跑。

今天，在发表于[*《自然》*（*Nature*）](https://www.nature.com/articles/s41586-026-10953-2)的一篇论文中，我们展示了 WeatherNext AI 模型在预测气旋路径、强度和风场结构方面达到了业界最先进的精度。平均而言，我们的模型为预报员多争取了一整天的预测精度：我们 3 天预报的准确度，相当于以往模型只能对未来 2 天提供的水平。这一幅度的提升大致相当于气象学十年积累的进步。

这项合作汇聚了 Google DeepMind 和 Google Research 的 AI 研究人员与工程师，以及[国家飓风中心](https://www.nhc.noaa.gov/)（NHC）、[大气研究合作研究所](https://www.cira.colostate.edu/)（CIRA）、[英国气象局](https://www.metoffice.gov.uk/)和世界各地气象机构的专家预报员。

我们的研究已经产生了真实世界的影响。在 2025 年飓风季，我们的模型帮助 NHC 对飓风 Melissa 做出了[历史性的预报](https://deepmind.google/blog/how-weathernext-helped-the-national-hurricane-center-better-predict-hurricane-melissas-historic-landfall-in-jamaica/)，预测了这场风暴的快速增强及其在牙买加的登陆。这使 NHC 能够提前发布预警，为地面团队争取到了关键的准备时间。今年，我们将继续携手合作，现在会对每个气旋预测 1,000 种可能的情景，以支持预报员的决策。

天气影响每一个人。鉴于其影响之广泛，我们现已[开源](https://github.com/google-deepmind/weathernext)飓风季期间使用的 WeatherNext 2 和 WeatherNext Cyclones 模型。通过开放这项技术，我们希望赋能研究社区，放大 AI 在建设更有韧性的社区方面的影响力——无论是为当地预报员提供[应对自然灾害](https://blog.google/innovation-and-ai/technology/research/helping-communities-prepare-for-natural-disasters/)所需的工具、支持可再生能源的发展，还是预判极端天气。

## WeatherNext 如何预测天气与气旋

![示意图：WeatherNext 气旋预报流程，展示 4 天内带有风强圆圈的预报风暴路径，以及热带风暴、强热带风暴和 1 级气旋大风的基于集合预报的概率地图。](https://lh3.googleusercontent.com/xw7fqPrHFQaCk_4-7bA9XDE2gxqFvrLVZ6JiBthyxDhDHSq_UoLAnFFk3vWfOnT6Gk1bT8CFFy2INB69XLFsXEiRDC4nfCEjAajfPE61OJqNcqlaxw=w1440)![示意图：WeatherNext 气旋预报流程，展示 4 天内带有风强圆圈的预报风暴路径，以及热带风暴、强热带风暴和 1 级气旋大风的基于集合预报的概率地图。](https://lh3.googleusercontent.com/7CvJfAfpG6c1aP_B0UVFZWLwpaD-kykSV-M8IUgA80Guo8CQ1CLTCH-nwzESRhi7jIRjswH1A0BT_zOcaZFq_1MDGjpCg6PJdLzDuw4H9Nr88XVv=w1440)

从飓风 Milton（2024 年 10 月）期间的全球大气状态出发，WeatherNext Cyclones 可以迭代地预测全球天气格局以及精细尺度的气旋路径，提前期最长可达 15 天。运行一个 1,000 成员的集合预报，可以生成热带风暴至飓风级大风的本地化概率地图。

预测气旋通常面临一种权衡，需要两种不同的建模技术。气旋的路径（它往哪里去）由大规模的全球大气环流引导，在此之前，对这类环流的最佳建模方式是较粗分辨率的全球模型。然而，气旋的强度（它会变得多强）则由其核心周围高度局部化、精细尺度的热力学物理过程驱动，这类过程最适合由专业化、更高分辨率的本地模型来建模。

我们的 WeatherNext 模型弥合了这一鸿沟，同时改进了对全球天气整体和气旋的预报。它是一个单一的 AI 模型，能以业界最先进的精度预测热带气旋的路径、强度和风场结构。这一突破得益于其训练方式、架构以及处理低分辨率输入方法的独特结合。

![三幅折线图，比较 5 天内路径、强度和风场范围的预报误差。在全部三项指标上，WeatherNext Cyclones 模型（由最下方的蓝色线表示）始终保持最低的误差率，水平箭头突出显示其相对其他模型约一天的预测精度优势。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/KVYBfGrBNy54BoGq/WeatherNext-Cyclones__figure-2_light.svg)![三幅折线图，比较 5 天内路径、强度和风场范围的预报误差。在全部三项指标上，WeatherNext Cyclones 模型（由最下方的蓝色线表示）始终保持最低的误差率，水平箭头突出显示其相对其他模型约一天的预测精度优势。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/KVYBfGrBNy54BoGq/WeatherNext-Cyclones__figure-2_dark.svg)

我们在 2023 至 2024 年的历史气旋上评估了 WeatherNext Cyclones，将其确定性预报和概率预报的表现与其他顶级天气模型进行基准对比。平均而言，WeatherNext Cyclones 在预测气旋路径、强度和风场结构方面获得了一天以上（24 小时）的提前期优势。

该模型在两种不同的数据模态上进行了联合训练：全球天气动力学和由专家整理的历史气旋观测数据。通过在近 20 TB 的全球大气数据和涵盖近 5,000 场历史风暴的 IBTrACS 历史数据库上进行端到端训练，模型学会了复杂的天气模式以及如何为极端天气建模。

![两幅图，比较逐年 3 天气旋预报误差。图 A 显示 2023 至 2025 年间，WeatherNext Cyclones（蓝色）的位置误差（约 100 公里）显著低于 ENS（黄色）。图 B 显示同一时期，WeatherNext Cyclones 的强度误差（约 11 节）低于 HWRF（红色）。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/KVYBfGrBNy54BoGq/WeatherNext-Cyclones__figure-3_light.svg)![两幅图，比较逐年 3 天气旋预报误差。图 A 显示 2023 至 2025 年间，WeatherNext Cyclones（蓝色）的位置误差（约 100 公里）显著低于 ENS（黄色）。图 B 显示同一时期，WeatherNext Cyclones 的强度误差（约 11 节）低于 HWRF（红色）。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/KVYBfGrBNy54BoGq/WeatherNext-Cyclones__figure-3_dark.svg)

近几十年来，气旋预报精度一直在稳步提升。图中展示了 ECMWF-ENS 路径预报（a）和 HWRF 强度预报（b）多年来的 3 天准确度，以及 WeatherNext Cyclones 如何为路径和强度预报都带来了阶梯式的精度跃升。按照过去 20 年的趋势衡量，这一提升相当于十年的进步。

我们的模型使用[函数生成网络（FGN）](https://arxiv.org/pdf/2506.10772)来高效生成不同预测的集合，从而捕捉天气固有的不确定性。现在，我们可以在 TPU 上用不到一分钟生成一次 15 天的预报，让预报员能够快速评估潜在毁灭性尾部风险的概率分布。去年，我们的系统一次可以生成 50 个预测，与全球物理模型相当。今年，我们将集合规模扩大到 1,000 个成员，以捕捉罕见但影响重大的情景，例如 2025 年飓风 Melissa 期间出现的快速增强事件。

迄今为止，人们一直认为，以极高的空间分辨率运行是做出精准强度预报的主要驱动力。然而，WeatherNext Cyclones 只需要 28x28 公里分辨率的数据，比传统模型粗糙 100 倍。该模型的一个更小版本 WeatherNext 2-mini 在更粗糙的 111x111 公里分辨率下运行，同样表现出色。这一点令科学家们感到惊讶，要完全理解我们的模型为何能在这种分辨率下做出如此精准的预测，仍然是一个开放的研究问题。我们希望能与研究社区一道找到答案。

## 向研究社区开放 WeatherNext

伴随着我们的*《自然》*论文，我们正在[开源](https://github.com/google-deepmind/weathernext)代码和模型权重，供任何人自由使用和构建。这包括学术研究、业务化预报，或开发更专业化、更本地化的模型。我们希望以此加速全球天气社区的进步，赋能气象机构、研究人员和非营利组织，更好地预测各类天气事件，并做出保护生命与基础设施的关键决策。

我们同时发布两组相近的模型：飓风季期间运行的 WeatherNext Cyclones（结果见论文）；以及在 10 月投入业务化运行的后续更新版本 WeatherNext 2。此外，我们还发布了 WeatherNext 2-mini，这是该模型的紧凑版本，可以在免费的公开 [Colab notebook](https://colab.research.google.com/github/google-deepmind/weathernext/blob/master/docs/weathernext2/wn2_demo.ipynb) 中于单个 TPU 上运行。

你可以在 [Weather Lab](https://deepmind.google.com/science/weatherlab/) 上探索我们最新的气旋预报。我们最近刚为它刷新了新界面，并将其扩展为除气旋路径外还包含全球天气预报。Weather Lab 现在让你可以在同一个视图中可视化 WeatherNext 对温度、降水、风速等的预测。Weather Lab 和 WeatherNext 模型都是 [Google Earth AI](https://ai.google/earth-ai/) 的组成部分。

## 推进天气预报的 AI 前沿

我们通过在气旋预测上获得一天以上的提前期优势，实现了历史性的突破——相当于交付了十年气象学进步的成果。随着我们为未来的风暴季做准备，我们邀请研究人员、气象机构和专家与我们合作，在我们的开源模型之上构建，并在 Weather Lab 上探索我们的预报。通过将先进的机器学习与人类预报员不可或缺的现实世界专业知识相结合，我们致力于打造一个协作式的天气预报生态系统，以拯救生命，并帮助社区适应不断变化的气候。

**注意：官方天气预报和预警请以你所在地的气象机构或国家天气服务为准。**

[阅读我们的*《自然》*论文](https://www.nature.com/articles/s41586-026-10953-2)[下载代码](https://github.com/google-deepmind/weathernext)[探索 Weather Lab](https://deepmind.google.com/science/weatherlab)[阅读 NHC 2025 年验证报告](https://www.nhc.noaa.gov/verification/pdfs/Verification_2025.pdf)

## 致谢

本研究由 Google DeepMind 和 Google Research 团队共同开发。

我们感谢合作伙伴 NOAA/NWS/NCEP 国家飓风中心、大气研究合作研究所（CIRA）和英国气象局对本论文的合作与贡献。

这项工作凝聚了论文全体共同作者的贡献：Ferran Alet、Tom Andersson、Ilan Price、Stratis Markou、Andrew El-Kadi、Dominic Masters、Amy Li、Samier Merchant、Natalie Williams、Gregory Thornton、Ken MacKay、Olivia Graham、Akib Uddin、Ben Gaiarin、Devaja Shah、Elinor Kruse、Wallace Hogsett、David Zelinsky、John Cangialosi、Jonathan Martinez、James Franklin、Mark DeMaria、Kate Musgrave、Caroline L. Bain、Helen Titley、Jacklynn Stott、Remi Lam、Aaron Bell、Paul Komarek、Matthew Willson、Alvaro Sanchez-Gonzalez 以及 Peter Battaglia。
