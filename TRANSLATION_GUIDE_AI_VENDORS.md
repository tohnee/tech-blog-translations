# 翻译规范（大模型厂商技术文档中文化）

适用于本批新增的厂商源：`thinkingmachines-articles`、`minimax-articles`、`xai-articles`、`meta-ai-articles`，以及 GitHub/HF 型源（`xiaomi-articles`、`stepfun-articles`、`ling-articles`、`zhipu-articles`）中需要翻译的英文文档。Qwen（`qwen-articles(-zh)`）与 DeepSeek（`deepseek-articles(-zh)`）为官方双语，`*-zh/` 直接收录官方中文版（frontmatter 带 `zh_source: official`），**无需翻译**。

## 输出位置与文件头

- 译文目录：`<来源>-articles-zh/posts/`，文件名与英文归档一一对应。
- frontmatter：保留英文归档全部字段，新增 `title_en`（原英文标题）与 `translated: <日期>`；`title` 换中文译名。
- 正文以 `# 中文标题` 开头，第二行 `> 原文：[English Title](source URL) · <厂商名>`；若有中文官方名（如「阶跃星辰」「智谱」）用官方名，否则用英文品牌名。

## 翻译原则

1. **全文完整翻译**，不跳段；模型卡中的 benchmark 表格、训练配置、许可证段落（License/Acceptable Use）都要译；`Usage` 代码示例整块保留不译。
2. **代码块、命令、pip/npm 安装行、API 参数名原样保留**；表格中数字、模型名、许可证名（Apache 2.0、MIT、MXS-L1 等）不动。
3. 图片 URL 原样保留；图注翻译。
4. 术语表沿用 `TRANSLATION_GUIDE_SEMIANALYSIS.md` 的 AI/基础设施部分，另见下表补充。
5. 模型卡中的英文小节名（Model Scope / Quickstart / Evaluation / License）译为：模型范围 / 快速开始 / 评测 / 许可证。
6. HF 模型卡中的 YAML 元数据块（`---` 包裹的 license/library_name 等）原样保留在最前，翻译其后的 README 正文。

## 术语补充表

| English | 中文 |
|---|---|
| model card | 模型卡 |
| open weights | 开放权重 |
| context length | 上下文长度 |
| mixture-of-experts (MoE) | 专家混合（MoE） |
| agentic | 智能体（agentic，形容词首次出现括注） |
| tool use / function calling | 工具调用 / 函数调用 |
| RL post-training | 强化学习后训练 |
| thinking mode / reasoning mode | 思考模式 / 推理模式 |
| temperature / top_p | temperature（不译）/ top_p（不译） |
| vLLM / SGLang / TensorRT-LLM | 不译 |
| benchmark suite | 基准测试套件 |
| long-horizon task | 长时程任务 |
| self-evolution | 自我进化 |
| music generation / video generation | 音乐生成 / 视频生成 |
| distillation | 蒸馏 |
| open-source release | 开源发布 |

## xAI / Meta 特有

- xAI 文多为 Grok 产品与安全/研究公告：Grok 不译；Colossus 译「Colossus 超算集群」（首现括注）；safety 公告按原文语气译。
- Meta AI 博客含大量历史研究短讯：人名保留原文；FAIR 译「FAIR（Meta 基础人工智能研究院）」首现一次；若原文含 2016-2019 旧链接失效，URL 照抄不修。
- Meta 博客快照取自 Wayback：译文开头 `> 原文：` 行照常给原始 URL，可加注「（Wayback 存档）」。

## 校验

每篇译文完成后自查：模型名/数字/表格行数与英文一致；无整句英文残留（代码块与专有名词除外）；文末若有 License 声明需完整译出。

## arXiv 论文（`<源>-articles/papers/`）附加约定

- 译文输出到 `<源>-articles-zh/papers/<同名>.md`；frontmatter 保留原字段并加 `title_en`、`translated:`，正文以 `# 中文标题` 开头 + `> 原文：[English Title](https://arxiv.org/abs/<id>) · <机构> arXiv` 一行。
- **摘要（Abstract）完整翻译**；章节标题译中文（1 引言 / 2 相关工作 / 3 方法 / 4 实验 / 5 结论 等通行译法）。
- **公式保留 LaTeX 原样**（`$$...$$` 与行内 `$...$` 不动）；数学符号、变量名不译。
- **表格整体保留数据**：表头译中文，模型名/数字原样；超大结果表可保留原表仅译表题与说明文字。
- **参考文献列表（References/Bibliography）整体保留英文不译**，仅在节标题写「参考文献」。
- 图表说明（Figure N: / Table N: caption）翻译；正文中「Figure 3 shows...」译为「图 3 展示了……」。
- 脚注内容翻译；附录（Appendix）同样完整翻译。
- arXiv HTML 版的排版伪影（公式重复、LTX 符号）按语义清理，数学内容不得改动。
