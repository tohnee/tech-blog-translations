# 翻译规范（OpenAI 技术博客中文化）

本文件是 OpenAI 官方技术博客（openai.com，engineering 与 research 两个分类）翻译项目的统一规范，所有翻译批次开始前先读完。通用原则与 [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md)（Raschka 项目）一致，本文件补充本项目特有的约定与术语表。

## 项目信息

- 英文存档：`openai-articles/posts/<slug>.md`（engineering 20 篇 + research 49 篇，共 69 篇；清单见 `openai-articles/meta.json`，权威来源为 https://openai.com/sitemap.xml/engineering/ 与 /research/）
- 输出目录：`openai-articles-zh/posts/<slug>.md`（与源文件同名镜像）
- 进度索引：`openai-articles-zh/README.md`（每完成一篇更新）

## 输出文件头格式

源文件 frontmatter 为：

```markdown
---
title: "..."
date: YYYY-MM-DD
source: https://openai.com/index/<slug>/
crawled: 2026-09-13
category: engineering|research
---
```

译文 frontmatter 与输出格式：

```markdown
---
title: "中文标题"
title_en: "Original English Title"
source: <原文件 source URL，保持不变>
crawled: 2026-09-13
category: <原样保留>
translated: <完成日期 YYYY-MM-DD>
---

# 中文标题

> 原文：[Original English Title](source URL) · OpenAI 博客

（正文译文……）
```

## 翻译原则（在通用规范基础上补充）

1. **全文翻译，不得缩写或跳过**：TL;DR、图表说明、引言、结论、附录、致谢、文末 Citation 段全部翻译。文末「Citation」引用格式段（如 `OpenAI (2025)` 样式的著录）保留原文著录信息，说明文字翻译。
2. **代码块原样保留**：``` 包裹的代码、命令、配置、SQL 一字不改，代码内英文注释保留。
3. **数学公式原样保留**：`$...$` 与 `$$...$$` 中的 LaTeX 一个字符都不改。
4. **图片链接 URL 原样保留**（多为 `images.ctfassets.net` 或 openai.com 域），alt 文本翻译；图注翻译。
5. **表格**：表头与单元格文字翻译；数字、符号、单位保留。
6. **脚注/参考文献**：`[1]` 等引用标记位置保持；脚注列表条目可译则译，URL 与著录信息保留。正文中的 `⁠(opens in a new window)` 之类的抓取残留噪音直接删除，不影响语义。
7. **人名**：保留英文，不做转写（如 Sam Altman、Greg Brockman、Jakub Pachocki）。
8. **性能声明以原文为准**：倍数、百分比、延迟数字、硬件型号、规模数字（TPS/QPS、用户数、token 数）一字不差。
9. **中英混排空格**：中文与英文/数字之间加一个空格。
10. 站内链接 URL 不动，链接文字翻译。
11. **不要添加原文没有的内容**（译者注如确有必要，用「（译注：……）」且尽量克制）。
12. 模型与产品名一律保留官方写法：GPT-1/2/3/4/4o/4.1/5/5.1/5.6、o1/o3/o4-mini、ChatGPT、Codex、Sora、DALL·E、DALL-E 2/3、Whisper、Operator、Deep Research、GPT-OSS、gpt-rosalind、Aardvark 等，不译。

## 术语表（全文统一）

### 研究与对齐

| English | 中文 |
|---|---|
| alignment / misalignment | 对齐 / 不对齐 |
| emergent misalignment | 涌现不对齐 |
| alignment research | 对齐研究 |
| chain of thought (CoT) | 思维链（CoT） |
| reasoning model / reasoning | 推理模型 / 推理 |
| frontier model | 前沿模型 |
| post-training | 后训练 |
| pretraining | 预训练 |
| RLHF | RLHF（不译） |
| reinforcement learning (RL) | 强化学习（RL） |
| reward hacking | 奖励作弊（reward hacking） |
| reward model | 奖励模型 |
| scheming / deceptive alignment | 图谋 / 欺骗性对齐 |
| hallucination | 幻觉 |
| system card | 系统卡片 |
| eval / evals | 评测（eval，首次出现标注英文；evals 套件可保留 evals） |
| benchmark | 基准测试 |
| red teaming / red teamer | 红队测试 / 红队成员 |
| jailbreak / prompt injection | 越狱 / 提示注入 |
| instruction hierarchy | 指令层级 |
| Model Spec | 模型规范（Model Spec） |
| Preparedness Framework | Preparedness 框架 |
| safety / safeguards | 安全 / 安全防护机制 |
| misuse | 滥用 |
| biosecurity / biodefense | 生物安全 / 生物防御 |
| confidence / calibration | 置信度 / 校准 |
| interpretability | 可解释性 |
| sparse circuits / features | 稀疏回路 / 特征 |
| steering / activation steering | 引导 / 激活引导 |
| verifiability | 可验证性 |
| confession | 忏悔（confessions 机制，首次出现标注英文） |
| monitorability | 可监控性 |
| oversight / human oversight | 监督 / 人类监督 |
| copilot / assistant | 副驾驶 / 助手 |

### 工程与基础设施

| English | 中文 |
|---|---|
| scaling / scale out | 扩展 / 横向扩展 |
| read replica | 读副本 |
| connection pool / pooling | 连接池 / 连接池化 |
| sharding / shard | 分片 |
| rate limiting / rate limit | 速率限制 / 速率限制阈值 |
| hot key / cache stampede | 热点键 / 缓存击穿 |
| query planner | 查询规划器 |
| bloat / VACUUM | 膨胀 / VACUUM（不译） |
| primary / standby | 主库 / 备库 |
| failover | 故障转移 |
| throughput / latency / p99 | 吞吐量 / 延迟 / p99 |
| sandbox | 沙箱 |
| agent loop | 智能体循环 |
| harness | 执行框架（harness，首次出现标注英文） |
| tool call / function call | 工具调用 / 函数调用 |
| websocket / SSE | WebSocket / SSE（不译） |
| rollout / canary | 灰度发布 / 金丝雀发布 |
| observability / tracing | 可观测性 / 追踪 |
| incident / postmortem | 事故 / 复盘 |
| on-call | 值班 |
| idempotent | 幂等 |
| cache invalidation | 缓存失效 |
| voice engine / Realtime API | 语音引擎 / Realtime API |
| compute / cluster / datacenter | 算力 / 集群 / 数据中心 |
| GPU / HBM / InfiniBand / RoCE | 保留原名 |
| supercomputer / network fabric | 超级计算机 / 网络织网（fabric 首现标注英文，后文可用「网络结构」） |
| inference stack | 推理栈 |
| container / orchestration | 容器 / 编排 |

### 产品与研究载体

| English | 中文 |
|---|---|
| Codex / ChatGPT / Sora / Operator | 保留原名 |
| deep research | 深度研究（Deep Research 产品名保留英文） |
| agent / coding agent / data agent | 智能体 / 编程智能体 / 数据智能体 |
| workflow / pipeline | 工作流 / 流水线 |
| enterprise / workspace | 企业 / 工作区 |
| API / endpoint | API（不译）/ 端点 |
| SDK / CLI | 保留原名 |
| scaling law | 扩展定律 |
| distillation | 蒸馏 |
| fine-tuning / SFT | 微调 / 监督微调（SFT） |
| synthetic data | 合成数据 |
| test-time compute | 测试时计算 |
| long context | 长上下文 |
| multimodal | 多模态 |
| embodiment / robotics | 具身 / 机器人 |

## 特殊约定

- OpenAI 文中常以第一人称「we」指代公司团队，统一译为「我们」；「OpenAI」保留不译。
- 「GPT-5.6」「o4-mini」等版本号严格保留。
- 文章若含 TL;DR 段，译文同样放在正文开头。
- 标题若为问句、双关，优先意译通顺，可失之字面。

## 存档格式差异与译者处理（重要）

抓取通道（webReader）对所有文章都会剥离超链接 URL（链接文字保留为纯文本），约一半文章的标题层级和列表标记在源文件中已被展平（标题已由 `fix_openai_headings.py` 恢复为 `##`）。译者需注意：

1. **列表还原**：若某段以冒号结尾（如 `…it is shared across:`），其后紧随的多个短段落是列表项，译文应渲染为 Markdown 列表（`- `）。判断依据是语义，不确定时保持段落即可。
2. **加粗引导句**：原文形如 `The model knows things no one taught it. Train a model…` 的段落，首句常是加粗的列表/条目引导句，译文可用 `**……**` 标出首句再接正文。
3. **残留噪音**：正文中可能有 `⁠`（不可见锚点字符）、`GPT‑5.6` 中的 U+2011 连字符等，保留原字符；`(opens in a new window)` 之类残留删除。
4. **update notice**：部分文首有 `___Update on …:___ _…_` 样式的更新说明（下划线/星号混用），统一规范为 `**Update on …：** *……*`（保留英文日期格式）或直接以粗体段落呈现，语义不变。
