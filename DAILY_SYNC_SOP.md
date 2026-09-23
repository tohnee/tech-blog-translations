# 每日同步作业指导书（DAILY SYNC SOP）

> 本文件是定时任务与人工执行的唯一依据。每天按顺序执行：**检测新文章 → 归档英文原文 → 翻译 → 更新索引 → 提交推送**。
> 工作目录：仓库根目录（本文件所在目录）。

## 通用规则

1. **幂等**：所有步骤以「文件已存在即跳过」为准，重复执行不产生副作用。
2. **串行**：翻译逐篇进行，不并发派发子代理（本机并发配额 ≈1）。
3. **限量**：单日新增文章翻译上限 **10 篇**；如有存量未译（按 `python3 -c` 比对 *-articles 与 *-articles-zh 文件集），每日另补译 **5 篇**；超出部分记入待办，次日继续。（2026-09-14 存量冲刺后：Raschka articles/faq 已全部译完，当前无存量。）
4. **翻译规范**：各来源遵循对应 `TRANSLATION_GUIDE_*.md`（全文完整翻译、术语一致、公式保留 LaTeX、代码块不译）；译文文件名与英文归档一一对应。
5. **归档格式**：英文 markdown 存 `<来源>-articles/posts/<slug>.md`，译文存 `<来源>-articles-zh/posts/<slug>.md`（sglang/claudecode 为平铺无 posts 子目录）。
6. **网络**：本机 curl/WebFetch 对 github/raw/archive.org 经常失败；失败时改用浏览器页面上下文 fetch + node:fs 落盘，或稍后重试一次。禁止使用 webReader 抓正文（会摘要化/幻觉化）。
   - **SOCKS 代理**：系统代理 `127.0.0.1:10808`（scutil --proxy 可查）。curl 加 `--socks5-hostname 127.0.0.1:10808` 可访问 archive.org 等被直连阻断的站点（Wayback CDX 会 504/429 过载，改用 availability API 或稍后重试）。openai.com 直连 403（Cloudflare），走代理也会拿到挑战页，检测以 Wayback 快照为准。
   - kexue.fm 若本网与代理出口均 SSL EOF（IP 封禁），当日跳过。
7. **空跑**：若所有来源均无新文章且无存量待译，直接结束，不做空提交。

## 各来源操作手册（23 源）

### 0a. Claude 博客（claude-blog-articles，86 篇已收）

- 检测：`https://claude.com/sitemap.xml` 中 `/blog/<slug>` 与 `claude-blog-articles/` 比对（claude.com 直连可抓）。
- 抓取：`crawl_claude_fetch.py`；只收技术类文章（筛除客户故事/产品发布/企业合规/活动类，判定标准见 `claude-blog-articles-zh/README.md` 建库说明）。
- 翻译规范：`TRANSLATION_GUIDE_CLAUDE_BLOG.md`。

### 0b. OpenAI 开发者博客（openai-dev-articles，14 篇已收）

- 检测：`developers.openai.com/blog` 直连常被拒——走 SOCKS 代理抓列表或 `index.xml`；仍失败则 Wayback。
- 抓取：`crawl_devcrawl.py`；28 篇中只收技术文（清单见 `openai-dev-articles/titles.md`）。

### 1. OpenAI（openai-articles，71 篇已收）

- 检测（CDX 首抓法，2026-09-14 验证可行）：
  ```bash
  # 走 SOCKS 代理；取每个 URL 的首次抓取时间，≥上次同步日且未收录的才是新文
  curl -sS --socks5-hostname 127.0.0.1:10808 --max-time 240 \
    "https://web.archive.org/cdx/search/cdx?url=openai.com%2Findex%2F*&output=text&fl=original,timestamp&collapse=urlkey&filter=statuscode:200&filter=mimetype:text/html&limit=8000"
  ```
  注意：CDX 默认按时间升序 + collapse=urlkey 取首条=首次抓取；`from=` 窗口查询会混入老文重抓，不可用于判新。limit 截断时对个别候选单独查 `url=openai.com/index/<slug>`。CDX 会间歇 504/429，退避重试（间隔 ≥10s）。
- 归档：取 Wayback 快照 `https://web.archive.org/web/<ts>id_/https://openai.com/index/<slug>/`（curl 需 `--compressed`），正文在嵌套 div（非单一 article），用"按文档序收集 h1/h2/h3/blockquote/div.max-w-none>p"的抽取器；转 markdown 后 `crawl_openai_finalize.py <slug> <url> <category>` 补 frontmatter，再清理尾部 "Keep reading" 等导航段。
- 坑：openai.com 直连 403（Cloudflare，走代理也是挑战页）；webReader 禁用。

### 2. Google 三源（crawl_google.py）

- **DeepMind** `https://deepmind.google/blog/`，已收清单 `deepmind-articles/meta.json`。**注意：2026-09 起 DeepMind 文章迁移到 blog.google/innovation-and-ai/models-and-research/google-deepmind/<slug>/，deepmind.google 旧域 URL 返回 404**——检测需同时看列表页里的 blog.google 交叉链接（detect_new.py 已实现）；抓取用 `crawl_google.extract_bloggoogle`（blog.google 页面 DOM），meta 记 blog.google URL。
- **Gemini** `https://blog.google/products-and-platforms/products/gemini/` 及 `innovation-and-ai/models-and-research/gemini-models/`，清单 `gemini-articles/meta.json`。
- **Google Blog** `https://blog.google/innovation-and-ai/`，清单 `google-blog-articles/meta.json`。
- 检测：**blog.google 列表页是 JS 渲染，裸 HTML 只有栏目链接（检测是盲的）**——必须走 sitemap（`blog.google/sitemap.xml`，需 SOCKS 代理，直连 SSL 断）或 DeepMind 列表页交叉链接兜底。新文章按 `crawl_google.py` 流程抓正文，meta.json 追加条目。

### 3. vLLM（vllm-articles，134 篇已收）

- 检测：`https://blog.vllm.ai/` 列表页 vs `vllm-articles/meta.json`。
- 抓取：`crawl_vllm.py`；原文 HTML 存 `vllm-articles/html/`（工作数据，不入库），转 markdown 存 `posts/`。
- 公式：vLLM 博客用 MathJax SVG，抓取后运行 `regen_vllm_math.py` 把 SVG 还原为 LaTeX 再翻译。

### 4. SGLang / LMSYS（sglang-articles，96 篇已收）

- 检测：`https://lmsys.org/blog/` 索引页 vs 现有 `2024-xx-xx-*.md` 文件名。**已知盲区：列表页 JS 渲染（裸 HTML 无文章链接）、无 feed/sitemap（index.xml/feed.xml/sitemap.xml 均 404 或空）**——检测失败时改用浏览器渲染页面人工核对，或对比近期已知 slug 前缀（日期-开头）。
- 抓取：LMSYS 博客为 GitHub Pages，优先从其 GitHub 源取 markdown；`blog.sglang.io` 长期不可达，不要依赖。

### 5. Claude Code / Anthropic（claudecode-articles，25 篇已收）

- 检测：anthropic.com 工程/新闻页 vs `claudecode-articles/_crawl_report.json`。
- 抓取：参照 `build_claudecode_archive.py`。

### 6. Lilian Weng（lilianweng-articles，52+FAQ 已收）

- 检测：GitHub 仓库 `lilianweng/lilianweng.github.io` 的 `_posts/` 目录（比网页源更早更新）。
- 抓取：直接取仓库内 markdown 原文（jekyll frontmatter 保留），新文归档到 `lilianweng-articles/posts/` 后翻译。

### 7. Sebastian Raschka（sebastianraschka-articles，319 篇已收、已全部译完）

- 检测：`https://sebastianraschka.com/sitemap.xml` 中 `/(blog|articles)/<年>/<slug>.html` 与归档文件（按年份子目录、无 .html 后缀）比对，参见 `detect_new.py`。
- 抓取：`crawl_raschka.py`（`fetch_one(url)` 可直接复用）。
- faq/ 是问答短文（中位 3KB），批量翻译时可 15 篇/子代理。

### 8. 苏剑林《科学空间》（sujianlin-articles，1336 篇已收，中文原文）

- 检测：`https://kexue.fm/archives/` 归档页翻到最新，对比 `sujianlin-articles/INDEX.md`。
- 抓取：`fetch_sujianlin.py`；**严格串行、每请求间隔 ≥3 秒**，遇到 403 Cookie 挑战或 SSL EOF 立即停止当日抓取（已被封），次日再试。
- 仅归档不翻译；新文按分类放入对应子目录（文件名 `文章ID-标题.md`），更新 `INDEX.md` 与 `README.md`（`build_sujianlin_index.py` / `build_sujianlin_readme.py`）。

### 9. SemiAnalysis（semianalysis-articles，330 篇已收，2026-09-15 建库）

- 站点结构：`semianalysis.com`（WordPress 旧站）全站 301 到 **newsletter.semianalysis.com**（Substack 自定义域，直连可抓）；WP 的 `sitemap.xml` 是遗留数据，不要用它判新。`semianalysis.substack.com` 本网 SSL 不通，勿用。
- 检测：`https://newsletter.semianalysis.com/api/v1/archive?sort=new&offset=<N>&limit=12` 翻页枚举，对比 `semianalysis-articles/src/_index.json` 里的 slug 集；新 slug 即新文。
- 抓取：`crawl_semianalysis.py`（幂等可续传；单篇 API `/api/v1/posts/<slug>`）→ `convert_semianalysis.py` 转 markdown 并更新 `meta.json`。
- **付费墙**：`audience: only_paid` 的文章 API 只给付费墙前的公开预览（SemiAnalysis 预览很长，中位 ~21KB），归档与译文均带 🔒/⚠️ 标注；`audience: everyone` 才是全文。判新时两类都收。
- 翻译规范：`TRANSLATION_GUIDE_SEMIANALYSIS.md`；索引 `semianalysis-articles-zh/README.md`（`build_semianalysis_readme.py`）。

### 10. 大模型厂商十源（2026-09-22 建库，`TRANSLATION_GUIDE_AI_VENDORS.md` 统一规范）

| 源 | 目录 | 检测与抓取 |
|---|---|---|
| Qwen | qwen-articles | GitHub `QwenLM/QwenLM.github.io` tarball（Hugo 双语：`index.md`+`index.zh.md` 官方中文，零翻译） |
| DeepSeek | deepseek-articles | `api-docs.deepseek.com/sitemap.xml` 的 `/news/`；中文版 `/zh-cn/news/<slug>`（官方双语） |
| Thinking Machines | thinkingmachines-articles | `thinkingmachines.ai/sitemap.xml`（直连可抓） |
| MiniMax | minimax-articles | `minimax.io/blog`（SSR）；minimaxi.com 为 SPA 不可抓 |
| 智谱 | zhipu-articles | HF `zai-org/<model>/raw/main/README.md` + `api.github.com/repos/THUDM/<repo>/readme`；chat.z.ai/bigmodel.cn 均为 SPA |
| 小米 MiMo | xiaomi-articles | GitHub `XiaomiMiMo` org README + releases |
| StepFun | stepfun-articles | GitHub `stepfun-ai` org（官网/stepfun.ai 均不可抓） |
| Ling | ling-articles | GitHub `inclusionAI` org |
| xAI | xai-articles | x.ai/news 直连 403，走 Wayback CDX（`filter=mimetype:text/html`） |
| Meta AI | meta-ai-articles | ai.meta.com 断连；老模板快照在 **ai.facebook.com 域**（2021-2023 `_7g40` 容器有效），2024+ 新模板 h1 锚定文本抽取；`crawl_meta_ai.py` 可续传 |

- arXiv 旗舰论文：`arxiv.org/html/<id>` 转 md 归档 `<源>-articles/papers/`；参考文献整体保留英文。
- 索引与校验：`build_ai_vendors_readme.py`（EN/ZH 对应 + 各源 README 一键生成）。

## 收尾（每次必做）

1. 重新生成索引：`python3 build_master_index.py`（根 README + Google 三源 README）；SGLang/vLLM/OpenAI 等其余 README 有新文时手工追加条目。
2. 校验：新译文与英文归档文件名一一对应、非空、无「TODO/占位」残留。
3. 提交推送：
   ```bash
   git add -A && git commit -m "daily sync: <日期> 新增 N 篇归档 / M 篇翻译" && git push
   ```
4. 输出当日报告：各来源新增归档数、新译数、存量剩余、失败与跳过原因。
