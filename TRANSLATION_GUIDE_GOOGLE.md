# 翻译规范（Google / Google DeepMind / Gemini 博客中文化）

本文件是本项目所有翻译批次的统一规范。开始翻译前先读完本文件。通用原则与
[TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md)（Raschka 项目）一致，本文件补充本项目特有的约定与术语表。

## 项目信息

三个来源、三对目录，文件名（slug）逐篇镜像：

| 来源 | 英文存档 | 中文输出 |
|---|---|---|
| Google DeepMind 博客（deepmind.google/blog） | `deepmind-articles/posts/<slug>.md` | `deepmind-articles-zh/posts/<slug>.md` |
| Gemini 博客（blog.google 的 gemini 与 gemini-models 栏） | `gemini-articles/posts/<slug>.md` | `gemini-articles-zh/posts/<slug>.md` |
| Google 博客 AI/技术栏（blog.google 的 innovation-and-ai） | `google-blog-articles/posts/<slug>.md` | `google-blog-articles-zh/posts/<slug>.md` |

- 清单：各英文目录下 `meta.json`（slug、title、date、authors、tags、url）。
- 进度索引：`google-articles-zh-README.md`（每完成一篇更新，项目根目录）。
- 翻译顺序：先 DeepMind（技术性最强）→ Gemini → Google 博客；各来源内部按日期从新到旧。

## 英文存档文件头（已由爬虫写入，翻译时以此取元数据）

```markdown
---
title: "Original English Title"
source: <文章 URL>
site: deepmind | gemini | google-blog
date: YYYY-MM-DD
authors: A, B
crawled: 2026-09-13
---
```

## 中文输出文件头格式

```markdown
---
title: "中文标题"
title_en: "Original English Title"
source: <原文件的 source URL，保持不变>
site: <原文件 site，保持不变>
date: <原文件 date，保持不变>
crawled: <原文件 crawled，保持不变>
translated: <完成日期 YYYY-MM-DD>
---

# 中文标题

> 原文：[Original English Title](source URL) · Google DeepMind

（正文译文……）
```

引用行末尾的署名按 site 取：deepmind → Google DeepMind；gemini → Google；google-blog → Google。

## 翻译原则

1. **全文翻译，不得缩写或跳过段落**。开头的副标题/摘要、Acknowledgements 致谢、文末的 "Posted by" 署名行、更新说明（如 "Edit: …"，译为「编者注：……」）都要译。
2. **代码块原样保留**；代码内英文注释也保留。行内代码同样保留。
3. **图片链接 URL 原样保留**；图片 alt 与下方 caption/图注翻译。`*斜体 caption*` 保持斜体。
4. **Markdown 结构保持**：标题层级、列表、表格、引用块、粗斜体位置与原文一一对应；表格内容翻译。
5. **链接文本翻译，URL 不动**；站内相对链接原样保留。
6. **产品/模型/系统名不翻译**：Gemini、Bard、AlphaGo、AlphaFold、AlphaZero、AlphaProof、AlphaGeometry、AlphaEvolve、AlphaMissense、AlphaProteo、AlphaQubit、Genie、Veo、Imagen、Lyria、SynthID、Gemma、Gemma 3、Nano Banana、Jules、NotebookLM、Gems、Deep Research、Gemini Live、AI Studio、Vertex AI、Gemini CLI、Antigravity、Colab、Search、Chrome、Android、Pixel、Tensor、TPU、Ironwood、Trillium、Willow、Sycamore、WeatherNext、GraphCast、GenCast、GNoME、SigLIP、MuJoCo、XR 等，全文统一。
7. **人名保留英文**，首次出现可附通行中译：Demis Hassabis（德米斯·哈萨比斯）、John Jumper、David Silver、Jeff Dean（杰夫·迪恩）、François Chollet、Yann LeCun（杨立昆）、Geoffrey Hinton（杰弗里·辛顿）等；全文内一人统一。
8. **公司/机构名**：Google（谷歌，行文中一般保留 Google）、Google DeepMind（首次「Google DeepMind（谷歌 DeepMind）」，后文 DeepMind 或 Google DeepMind）、DeepMind 与 Google Brain 合并前的旧文按原文。
9. **日期/奖项/机构常引语**照常翻译；官方口号（如 "Bold, responsible AI"）翻译后可括注原文。
10. 语气：技术博客风格，面向中文 AI 研究者/工程师，流畅自然，不逐词直译；专有名词首次出现用「中文（English）」格式。

## 术语表（全文统一）

### 模型与架构

| English | 中文 |
|---|---|
| large language model (LLM) | 大语言模型（LLM） |
| multimodal / natively multimodal | 多模态 / 原生多模态 |
| mixture-of-experts (MoE) | 专家混合（MoE） |
| reasoning model | 推理模型 |
| chain-of-thought (CoT) | 思维链（CoT） |
| test-time compute | 测试时计算（test-time compute） |
| long context / context window | 长上下文 / 上下文窗口 |
| context caching | 上下文缓存 |
| token | token（不译） |
| embedding | 嵌入 |
| fine-tuning / pretraining | 微调 / 预训练 |
| distillation / knowledge distillation | 蒸馏 / 知识蒸馏 |
| quantization | 量化 |
| open model / open weights | 开放模型 / 开放权重 |
| sparse autoencoder (SAE) | 稀疏自编码器（SAE） |
| interpretability / mechanistic interpretability | 可解释性 / 机制可解释性 |
| world model | 世界模型 |
| foundation model | 基础模型 |
| generalization | 泛化 |
| hallucination | 幻觉 |
| benchmark / evals | 基准测试 / 评测 |

### 训练与智能体

| English | 中文 |
|---|---|
| reinforcement learning (RL) | 强化学习（RL） |
| RLHF / RLAIF | 人类反馈强化学习（RLHF）/ AI 反馈强化学习（RLAIF） |
| agent / agentic | 智能体 / 智能体化 |
| computer use | 计算机操作（computer use） |
| tool use / function calling | 工具使用 / 函数调用 |
| grounding | 锚定（grounding，指向真实来源校验） |
| prompt / prompt engineering | 提示词 / 提示词工程 |
| system instructions | 系统指令 |
| supervised fine-tuning (SFT) | 监督微调（SFT） |
| curriculum | 课程（训练课程） |
| self-play | 自我博弈 |
| reward hacking | 奖励作弊（reward hacking） |
| compute / FLOP | 算力 / FLOP（不译） |
| data center | 数据中心 |
| scaling law | 标度律（scaling law） |
| emergent capability | 涌现能力 |

### 安全与责任

| English | 中文 |
|---|---|
| frontier safety framework | 前沿安全框架 |
| critical capability levels (CCLs) | 关键能力等级（CCL） |
| red teaming | 红队测试 |
| watermarking | 水印 |
| deepfake | 深度伪造 |
| misuse / dual-use | 滥用 / 双重用途 |
| responsible AI | 负责任的 AI |
| alignment | 对齐 |
| safeguards | 防护措施 |
| policy / regulatory | 监管 / 政策（视语境） |
| provenance | 内容溯源 |

### 科学应用

| English | 中文 |
|---|---|
| protein structure prediction | 蛋白质结构预测 |
| protein folding | 蛋白质折叠 |
| drug discovery | 药物发现 |
| materials discovery / materials science | 材料发现 / 材料科学 |
| weather forecasting | 天气预报 |
| quantum computing / qubit | 量子计算 / 量子比特 |
| quantum error correction | 量子纠错 |
| quantum supremacy / beyond-classical computation | 量子计算优越性 / 超经典计算 |
| fusion / plasma control | 聚变 / 等离子体控制 |
| neuroscience / connectome | 神经科学 / 连接组 |
| mathematics / formal proof | 数学 / 形式化证明 |
| International Mathematical Olympiad (IMO) | 国际数学奥林匹克竞赛（IMO） |
| chip design / floorplanning | 芯片设计 / 布局规划 |
| nuclear magnetic resonance (NMR) | 核磁共振（NMR） |

### 产品与平台用语

| English | 中文 |
|---|---|
| AI Overviews | AI Overviews（不译） |
| Circle to Search | 圈选搜索（Circle to Search） |
| rolling out / generally available | 开始推送 / 正式发布（GA） |
| developer preview | 开发者预览版 |
| experimental / beta | 实验版 / 测试版 |
| workspace integration | Workspace 集成 |
| live demo | 现场演示 |
| waitlist | 候补名单 |
| free tier / paid tier | 免费档 / 付费档 |
| user research | 用户研究 |
| responsible scaling | 负责任的扩展 |
| frontier | 前沿 |
| AGI (artificial general intelligence) | 通用人工智能（AGI） |

## 流程约定

1. 每批由一个后台 agent 串行处理（并发额度≈1，禁止并行 dispatch），一次 8–10 篇。
2. Agent 每完成一篇立即写盘并更新进度索引 `google-articles-zh-README.md` 对应行。
3. 翻译完删除英文 frontmatter 中 `authors` 行，按上面「中文输出文件头格式」重排。
4. 若源文件正文明显残缺（<200 字符或只有导航文本），在进度索引标记 `⚠️ 源文异常` 并跳过，不要硬译。
