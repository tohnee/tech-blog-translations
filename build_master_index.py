#!/usr/bin/env python3
"""生成主索引：根 README.md + Google 三源中文目录 README（数据来自各 meta.json）。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

GOOGLE_SOURCES = [
    ("deepmind", "Google DeepMind 博客", "https://deepmind.google/blog/"),
    ("gemini", "Gemini 博客", "https://blog.google/products-and-platforms/products/gemini/"),
    ("google-blog", "Google 博客（AI/技术栏）", "https://blog.google/innovation-and-ai/"),
]


def count_md(base: Path, exclude=("README.md", "INDEX.md", "_PROGRESS.md", "titles.md")) -> int:
    if not base.exists():
        return 0
    return sum(1 for p in base.rglob("*.md") if p.name not in exclude)


def build_google_readme(key: str, name: str, site: str) -> int:
    meta = json.loads((ROOT / f"{key}-articles" / "meta.json").read_text())
    meta.sort(key=lambda p: p.get("date") or "", reverse=True)
    zh_dir = ROOT / f"{key}-articles-zh" / "posts"
    missing = [p for p in meta if not (zh_dir / f"{p['slug']}.md").exists()]
    lines = [
        f"# {name} 中文翻译",
        "",
        f"[{site}]({site}) 全部文章的完整中文翻译，术语遵循项目 [翻译规范](../TRANSLATION_GUIDE_GOOGLE.md)。",
        "",
        f"- 英文存档：[`../{key}-articles/`](../{key}-articles/)",
        f"- 译文目录：本目录 `posts/`，文件名与原文 slug 一一对应",
        f"- 三源合并总索引：[`../google-articles-zh-README.md`](../google-articles-zh-README.md)",
        "",
        f"## 进度：{len(meta) - len(missing)} / {len(meta)}",
        "",
    ]
    year = None
    for p in meta:
        d = p.get("date") or ""
        y = d[:4] if d else "未知日期"
        if y != year:
            year = y
            lines += [f"## {y} 年", ""]
        mark = "x" if (zh_dir / f"{p['slug']}.md").exists() else " "
        lines.append(
            f"- [{mark}] [{p['title']}](posts/{p['slug']}.md) · [EN]({p['url']})"
        )
    if missing:
        lines += ["", f"> 未翻译：{len(missing)} 篇"]
    (ROOT / f"{key}-articles-zh" / "README.md").write_text("\n".join(lines) + "\n")
    return len(meta)


def main() -> None:
    total_en, total_zh = 0, 0

    for key, name, site in GOOGLE_SOURCES:
        n = build_google_readme(key, name, site)
        print(f"{key}: {n} 篇 → {key}-articles-zh/README.md")

    projects = [
        {
            "name": "OpenAI", "site": "openai.com/blog",
            "en": "openai-articles", "zh": "openai-articles-zh",
            "guide": "TRANSLATION_GUIDE_OPENAI.md",
            "readme": "openai-articles-zh/README.md",
            "note": "含 Engineering 与 Research 两类文章",
        },
        {
            "name": "Google DeepMind", "site": "deepmind.google/blog",
            "en": "deepmind-articles", "zh": "deepmind-articles-zh",
            "guide": "TRANSLATION_GUIDE_GOOGLE.md",
            "readme": "deepmind-articles-zh/README.md",
            "note": "",
        },
        {
            "name": "Gemini", "site": "blog.google（gemini 栏目）",
            "en": "gemini-articles", "zh": "gemini-articles-zh",
            "guide": "TRANSLATION_GUIDE_GOOGLE.md",
            "readme": "gemini-articles-zh/README.md",
            "note": "",
        },
        {
            "name": "Google Blog", "site": "blog.google/innovation-and-ai",
            "en": "google-blog-articles", "zh": "google-blog-articles-zh",
            "guide": "TRANSLATION_GUIDE_GOOGLE.md",
            "readme": "google-blog-articles-zh/README.md",
            "note": "",
        },
        {
            "name": "vLLM", "site": "blog.vllm.ai",
            "en": "vllm-articles", "zh": "vllm-articles-zh",
            "guide": "TRANSLATION_GUIDE_VLLM.md",
            "readme": "vllm-articles-zh/README.md",
            "note": "MathJax SVG 公式已还原为 LaTeX",
        },
        {
            "name": "SGLang / LMSYS", "site": "lmsys.org/blog",
            "en": "sglang-articles", "zh": "sglang-articles-zh",
            "guide": "TRANSLATION_GUIDE_SGLANG.md",
            "readme": "sglang-articles-zh/README.md",
            "note": "SGLang 及生态（slime 等）全部技术博文",
        },
        {
            "name": "Claude Code / Anthropic", "site": "anthropic.com（工程博客）",
            "en": "claudecode-articles", "zh": "claudecode-articles-zh",
            "guide": "TRANSLATION_GUIDE_CLAUDECODE.md",
            "readme": "claudecode-articles-zh/README.md",
            "note": "",
        },
        {
            "name": "Claude 博客", "site": "claude.com/blog",
            "en": "claude-blog-articles", "zh": "claude-blog-articles-zh",
            "guide": "TRANSLATION_GUIDE_CLAUDE_BLOG.md",
            "readme": "claude-blog-articles-zh/README.md",
            "note": "官方 sitemap 技术类筛选，2026-09-14 建库 86/86",
        },
        {
            "name": "OpenAI 开发者博客", "site": "developers.openai.com/blog",
            "en": "openai-dev-articles", "zh": "openai-dev-articles-zh",
            "guide": "TRANSLATION_GUIDE_CLAUDE_BLOG.md",
            "readme": "openai-dev-articles-zh/README.md",
            "note": "28 篇中筛选技术文 14/14，2026-09-14 建库",
        },
        {
            "name": "Lilian Weng", "site": "lilianweng.github.io",
            "en": "lilianweng-articles", "zh": "lilianweng-articles-zh",
            "guide": "TRANSLATION_GUIDE_LILIANWENG.md",
            "readme": "lilianweng-articles-zh/README.md",
            "note": "52 篇 + FAQ，全部完成",
        },
        {
            "name": "Sebastian Raschka", "site": "sebastianraschka.com",
            "en": "sebastianraschka-articles", "zh": "sebastianraschka-articles-zh",
            "guide": None, "readme": "sebastianraschka-articles-zh/README.md",
            "note": "存量含 blog/专栏/FAQ/画廊/magazine，中文译文每日同步任务持续补译",
        },
        {
            "name": "苏剑林《科学空间》", "site": "kexue.fm",
            "en": "sujianlin-articles", "zh": None,
            "guide": None, "readme": "sujianlin-articles/README.md",
            "note": "中文原文全量归档（1336 篇），无需翻译；细目见 INDEX.md",
        },
    ]

    rows = ["| 来源 | 原文站点 | 英文存档 | 中文翻译 | 篇数 | 索引 |",
            "|---|---|---|---|---|---|"]
    for p in projects:
        if p["en"] == "openai-articles":
            en_n = count_md(ROOT / p["en"] / "posts")
        elif p["en"] == "lilianweng-articles":
            en_n = count_md(ROOT / p["en"] / "posts") + 1  # + faq.md
        else:
            en_n = count_md(ROOT / p["en"])
        total_en += en_n
        if p["zh"]:
            zh_n = count_md(ROOT / p["zh"])
            if p["zh"] == "lilianweng-articles-zh":
                zh_n = count_md(ROOT / p["zh"] / "posts") + 1
            total_zh += zh_n
            zh_cell = f"[{p['zh']}/]({p['zh']}/)（{zh_n}）"
            cnt = f"{en_n} / {zh_n}"
        else:
            zh_cell = "—（原文为中文）"
            cnt = f"{en_n}"
        guide_cell = f"[规范]({p['guide']})" if p["guide"] else "—"
        rows.append(
            f"| {p['name']} | {p['site']} | [{p['en']}/]({p['en']}/)（{en_n}） | {zh_cell} | {cnt} | {guide_cell} · [目录]({p['readme']}) |"
        )

    notes = [p for p in projects if p["note"]]

    readme = f"""# 优秀 AI / 技术博客文章归档与中文翻译

收录 {len(projects)} 个高质量技术博客来源的全量文章归档与完整中文翻译
（英文存档 `{len(projects) - 1}` 源 + 中文原文 `1` 源；苏剑林博客为中文站点，仅归档）。

> 累计：英文/原文归档 **{total_en}** 篇，中文译文 **{total_zh}** 篇。
> 每日自动同步：定时任务按 [DAILY_SYNC_SOP.md](DAILY_SYNC_SOP.md) 拉取各源新文章、归档并翻译，随后更新本索引并推送 GitHub。

## 项目总览

{chr(10).join(rows)}

## 说明

"""
    for p in notes:
        readme += f"- **{p['name']}**：{p['note']}\n"
    readme += """
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
"""
    (ROOT / "README.md").write_text(readme)
    print(f"根 README.md 已生成：EN {total_en} / ZH {total_zh}")


if __name__ == "__main__":
    main()
