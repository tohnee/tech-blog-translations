---
title: "Llama 如何帮助 Biofy Technologies 对抗抗生素耐药性"
title_en: "How Llama helps Biofy Technologies in the fight against antibiotic resistance"
date: 2025-08-07
source: https://ai.meta.com/blog/llama-helps-biofy-fight-antibiotic-resistance
crawled: 2026-09-22
translated: 2026-09-22
---

# Llama 如何帮助 Biofy Technologies 对抗抗生素耐药性

> 原文：[How Llama helps Biofy Technologies in the fight against antibiotic resistance](https://ai.meta.com/blog/llama-helps-biofy-fight-antibiotic-resistance) · Meta AI（Wayback 存档）

抗生素耐药性对全球健康构成重大威胁，也是医院中常见的死因。为应对其祖国巴西的这一挑战，生物科技公司 Biofy Technologies 用 Llama 开发了一个突破性平台，把抗生素耐药性的诊断时间从五天缩短到不足四小时。

Biofy 开发了一套用向量数据库识别细菌及其抗生素耐药性的系统，数据库中每条细菌 DNA 都链接到一条数据库记录。原系统基于 NCBI 基因组数据库构建，其中约有 72 万条细菌 DNA 样本。由于细菌 DNA 变异极为频繁，Biofy 需要加入更多 DNA 变体。为此，Biofy 团队定制了 Llama 3.2 90B 模型，让它与原基因组数据库协作、生成新的合成 DNA 样本。成果就是 Biofy 的 Abby Recommender。该解决方案运行在 Oracle 云基础设施（OCI）与专用 GPU 上。Abby Recommender 可以分析 DNA、识别细菌，并基于细菌耐药性推荐正确的抗生素。

「一个能快速识别耐药细菌并提出有效治疗方案的平台可以挽救生命，」Biofy CEO Paulo Perez 说，「Llama 是我们为解决方案创建基因组向量数据库所用的基础组件。我们选择它，因为它是开源的、完全可定制，而且适合我们要解决的问题。」

## 与 Llama 协作

Biofy 将 Llama 与 OCI Generative AI 和 Oracle AI Vector Search 配合使用。团队开发了一个专有模型，用带向量数据库（Vector DB）的 Oracle Autonomous 23ai 数据库来转换 DNA。对 Biofy 团队而言，开源路线很重要，因为他们需要自由地调整模型，以满足创建 DNA 合成数据的要求。「若要靠自主研发取得类似的解决方案，需要多年投资，」Perez 说。Biofy 的算法会检查一个基因组对细菌 DNA 是否有效且稳定，团队随后测试了 Llama 3.2 90B 模型创建的合成数据。「显然，AI 的用武之地远不止聊天机器人和销售方案这些传统应用，」Perez 说，「我们可以用它来帮助挽救生命、提升生活质量。」

分享你的 Llama 故事
