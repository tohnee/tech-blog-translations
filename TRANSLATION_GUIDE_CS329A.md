# 翻译规范（Stanford CS329A《Self-Improving AI Agents》课程材料中文化）

适用于 `cs329a-articles/`（课程页面 `pages/` + 指定阅读论文 `papers/`，共 2 页面 + 34 篇论文，约 450 万字符）的翻译。论文翻译的「arXiv 论文附加约定」沿用 `TRANSLATION_GUIDE_AI_VENDORS.md`，本文件只补充 CS329A 特有内容。

## 输出位置与文件头

- 译文目录：`cs329a-articles-zh/pages/` 与 `cs329a-articles-zh/papers/`，文件名与英文归档一一对应。
- frontmatter：保留英文归档全部字段，新增 `title_en` 与 `translated: <日期>`，`title` 换中文译名。
- 正文以 `# 中文标题` 开头；论文第二行 `> 原文：[English Title](https://arxiv.org/abs/<id>) · Stanford CS329A 指定阅读`；DeepMind 技术报告（AlphaCode 2 / AlphaEvolve）用 `· DeepMind 技术报告（CS329A 指定阅读）`。

## 课程页面（pages/）

- `index.md` 是单页课程站（介绍/人员/日程/评分/政策）：完整翻译，日程表转 Markdown 表格（课次/日期/主题/阅读/截止），阅读列表的论文标题保留英文原名（括注中文或直接中文均可，但链接 URL 原样）。
- `pastprojects.md` 过往项目列表：项目名与团队名保留原文，描述翻译。

## 论文翻译要点（沿用 AI_VENDORS 规范 + 以下补充）

1. **参考文献列表整体保留英文**，节标题写「参考文献」。
2. **LaTeX 公式原样保留**；arXiv HTML 的 Unicode+LaTeX 重复伪影按语义清理为单一 LaTeX。
3. **提示词/模型输出展品**（ReAct 轨迹、 Constitutional AI 的红队提示、Math-Shepherd 的过程奖励模板、AI Scientist 的代码补丁等）**整块保留英文**，仅翻译周边说明；代码块不译。
4. **超长论文分片**：>150KB 按章节边界分片（首片写文件头，后续片对齐术语后追加）；Darwin Gödel Machine（428KB）至少三片。
5. AlphaEvolve/AlphaCode2 为 PDF 抽取的纯文本（无图片/公式排版）：数学符号按语义恢复（如 ∇→∇ 保留 unicode、上下标写 `x^2`），无法恢复的照抄；附录数据表保留数字。

## 术语（本课程高频）

| English | 中文 |
|---|---|
| self-improving agent | 自我改进智能体 |
| test-time compute | 测试时计算 |
| repeated sampling | 重复采样 |
| verifier / verification | 验证器 / 验证 |
| process reward model (PRM) | 过程奖励模型（PRM） |
| outcome reward model (ORM) | 结果奖励模型（ORM） |
| best-of-N (BoN) | best-of-N（不译） |
| self-consistency | 自洽性 |
| tree search (MCTS/ToT) | 树搜索 |
| rejection sampling | 拒绝采样 |
| bootstrapping | 自举 |
| synthetic data | 合成数据 |
| multi-step RL | 多步强化学习 |
| tool use / tool calling | 工具调用 |
| agentic framework | 智能体框架 |
| long-horizon task | 长时程任务 |
| scaffold | 脚手架（scaffold，首次括注） |
| open-ended evolution | 开放式进化 |
| automated design of agentic systems | 智能体系统的自动化设计 |
| deep research agent | 深度研究智能体 |
| memory augmentation | 记忆增强 |
| KV cache | KV 缓存 |
| RAG | RAG（不译） |
| long context | 长上下文 |
| benchmark | 基准测试 |
| contamination | 数据污染 |
| scaling law | 缩放定律 |

人名（Aakanksha Chowdhery、Melvin Johnson、Denny Zhou、Thang Luong、Misha Laskin、Danny Driess、Junchen Jiang 等）与机构名保留英文。
