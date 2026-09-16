# 优秀 AI / 技术博客文章归档与中文翻译

收录 13 个高质量技术博客来源的全量文章归档与完整中文翻译
（英文存档 `12` 源 + 中文原文 `1` 源；苏剑林博客为中文站点，仅归档）。

> 累计：英文/原文归档 **3170** 篇，中文译文 **1609** 篇。
> 每日自动同步：定时任务按 [DAILY_SYNC_SOP.md](DAILY_SYNC_SOP.md) 拉取各源新文章、归档并翻译，随后更新本索引并推送 GitHub。

## 项目总览

| 来源 | 原文站点 | 英文存档 | 中文翻译 | 篇数 | 索引 |
|---|---|---|---|---|---|
| OpenAI | openai.com/blog | [openai-articles/](openai-articles/)（71） | [openai-articles-zh/](openai-articles-zh/)（71） | 71 / 71 | [规范](TRANSLATION_GUIDE_OPENAI.md) · [目录](openai-articles-zh/README.md) |
| Google DeepMind | deepmind.google/blog | [deepmind-articles/](deepmind-articles/)（349） | [deepmind-articles-zh/](deepmind-articles-zh/)（349） | 349 / 349 | [规范](TRANSLATION_GUIDE_GOOGLE.md) · [目录](deepmind-articles-zh/README.md) |
| Gemini | blog.google（gemini 栏目） | [gemini-articles/](gemini-articles/)（123） | [gemini-articles-zh/](gemini-articles-zh/)（123） | 123 / 123 | [规范](TRANSLATION_GUIDE_GOOGLE.md) · [目录](gemini-articles-zh/README.md) |
| Google Blog | blog.google/innovation-and-ai | [google-blog-articles/](google-blog-articles/)（231） | [google-blog-articles-zh/](google-blog-articles-zh/)（231） | 231 / 231 | [规范](TRANSLATION_GUIDE_GOOGLE.md) · [目录](google-blog-articles-zh/README.md) |
| vLLM | blog.vllm.ai | [vllm-articles/](vllm-articles/)（134） | [vllm-articles-zh/](vllm-articles-zh/)（134） | 134 / 134 | [规范](TRANSLATION_GUIDE_VLLM.md) · [目录](vllm-articles-zh/README.md) |
| SGLang / LMSYS | lmsys.org/blog | [sglang-articles/](sglang-articles/)（96） | [sglang-articles-zh/](sglang-articles-zh/)（96） | 96 / 96 | [规范](TRANSLATION_GUIDE_SGLANG.md) · [目录](sglang-articles-zh/README.md) |
| Claude Code / Anthropic | anthropic.com（工程博客） | [claudecode-articles/](claudecode-articles/)（27） | [claudecode-articles-zh/](claudecode-articles-zh/)（27） | 27 / 27 | [规范](TRANSLATION_GUIDE_CLAUDECODE.md) · [目录](claudecode-articles-zh/README.md) |
| Claude 博客 | claude.com/blog | [claude-blog-articles/](claude-blog-articles/)（86） | [claude-blog-articles-zh/](claude-blog-articles-zh/)（86） | 86 / 86 | [规范](TRANSLATION_GUIDE_CLAUDE_BLOG.md) · [目录](claude-blog-articles-zh/README.md) |
| OpenAI 开发者博客 | developers.openai.com/blog | [openai-dev-articles/](openai-dev-articles/)（14） | [openai-dev-articles-zh/](openai-dev-articles-zh/)（14） | 14 / 14 | [规范](TRANSLATION_GUIDE_CLAUDE_BLOG.md) · [目录](openai-dev-articles-zh/README.md) |
| Lilian Weng | lilianweng.github.io | [lilianweng-articles/](lilianweng-articles/)（53） | [lilianweng-articles-zh/](lilianweng-articles-zh/)（53） | 53 / 53 | [规范](TRANSLATION_GUIDE_LILIANWENG.md) · [目录](lilianweng-articles-zh/README.md) |
| Sebastian Raschka | sebastianraschka.com | [sebastianraschka-articles/](sebastianraschka-articles/)（320） | [sebastianraschka-articles-zh/](sebastianraschka-articles-zh/)（320） | 320 / 320 | — · [目录](sebastianraschka-articles-zh/README.md) |
| SemiAnalysis | semianalysis.com | [semianalysis-articles/](semianalysis-articles/)（330） | [semianalysis-articles-zh/](semianalysis-articles-zh/)（105） | 330 / 105 | [规范](TRANSLATION_GUIDE_SEMIANALYSIS.md) · [目录](semianalysis-articles-zh/README.md) |
| 苏剑林《科学空间》 | kexue.fm | [sujianlin-articles/](sujianlin-articles/)（1336） | —（原文为中文） | 1336 | — · [目录](sujianlin-articles/README.md) |

## 说明

- **OpenAI**：含 Engineering 与 Research 两类文章
- **vLLM**：MathJax SVG 公式已还原为 LaTeX
- **SGLang / LMSYS**：SGLang 及生态（slime 等）全部技术博文
- **Claude 博客**：官方 sitemap 技术类筛选，2026-09-14 建库 86/86
- **OpenAI 开发者博客**：28 篇中筛选技术文 14/14，2026-09-14 建库
- **Lilian Weng**：52 篇 + FAQ，全部完成
- **Sebastian Raschka**：存量含 blog/专栏/FAQ/画廊/magazine，中文译文每日同步任务持续补译
- **SemiAnalysis**：Substack（newsletter.semianalysis.com）全量；付费文仅含公开预览（🔒 标注），2026-09-15 建库
- **苏剑林《科学空间》**：中文原文全量归档（1336 篇），无需翻译；细目见 INDEX.md

- 三个 Google 来源（DeepMind / Gemini / Google Blog）另有合并详表索引：[google-articles-zh-README.md](google-articles-zh-README.md)
- 翻译均为全文完整翻译，术语一致性由各 `TRANSLATION_GUIDE_*.md` 规范约束；公式保留原始 LaTeX，代码块不译
- 抓取与索引构建脚本（`crawl_*.py` / `build_*.py`）保留在仓库根目录，便于每日同步任务复用

## 目录结构

```
├── <来源>-articles/        # 英文原文归档（markdown）
├── <来源>-articles-zh/     # 中文翻译（文件名与原文一一对应）
├── TRANSLATION_GUIDE_*.md  # 各来源翻译规范
├── crawl_*.py              # 抓取脚本
├── build_*_index.py        # 索引构建脚本
├── build_master_index.py   # 主索引生成（本文件）
└── DAILY_SYNC_SOP.md       # 每日同步作业指导书
```

## 每日自动更新

本仓库由 ZCode 定时任务驱动，每天自动执行：

1. 检查各源站点是否有新文章发布
2. 新文章抓取归档为英文 markdown（`<来源>-articles/`）
3. 按对应翻译规范全文翻译（`<来源>-articles-zh/`）
4. 更新各项目 README 与本主索引
5. 提交并推送 GitHub

详细流程与各源抓取注意事项见 [DAILY_SYNC_SOP.md](DAILY_SYNC_SOP.md)。
