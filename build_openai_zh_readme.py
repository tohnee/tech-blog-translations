#!/usr/bin/env python3
"""Generate openai-articles-zh/README.md progress index from meta.json + files."""
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
meta = json.loads((ROOT / "openai-articles" / "meta.json").read_text())
posts = ROOT / "openai-articles" / "posts"
zh = ROOT / "openai-articles-zh" / "posts"

CATS = {"engineering": "工程", "research": "研究"}

def fm_field(p: Path, key: str) -> str:
    try:
        m = re.search(rf"^{key}:\s*(.+)$", p.read_text().split("---", 2)[1], re.M)
        return (m.group(1).strip().strip('"') if m else "")
    except Exception:
        return ""

rows_en, rows_zh, rows_missing = [], [], []
for m in sorted(meta, key=lambda x: (x["category"], x["slug"])):
    slug = m["slug"]
    en = posts / f"{slug}.md"
    z = zh / f"{slug}.md"
    title_en = fm_field(en, "title") if en.exists() else ""
    link = m["url"]
    name = f"[{title_en or slug}]({link})"
    if en.exists() and z.exists():
        t = fm_field(z, "title").strip('"')
        rows_zh.append(f"| {CATS[m['category']]} | [{t}](posts/{slug}.md) | {name} | {fm_field(z, 'translated') or '—'} |")
    elif en.exists():
        rows_en.append(f"| {CATS[m['category']]} | {name} | {fm_field(en, 'date') or '—'} |")

total_en = len([p for p in posts.glob("*.md")])
total_zh = len([p for p in zh.glob("*.md")])
eng_n = sum(1 for m in meta if m["category"] == "engineering")
res_n = sum(1 for m in meta if m["category"] == "research")

lines = [
    "# OpenAI 技术博客中文化（openai-articles-zh）",
    "",
    f"> 进度：**中文 {total_zh} / {total_en}**（英文存档 {total_en}/69：工程 {eng_n} + 研究 {res_n}）。英文权威清单来自 openai.com 官方 sitemap 的 engineering 与 research 分类（{date.today().isoformat()} 抓取）。",
    "> 通用规范见 [TRANSLATION_GUIDE_OPENAI.md](../TRANSLATION_GUIDE_OPENAI.md)。",
    "",
    "## 已翻译",
    "",
    "| 分类 | 中文标题 | 英文原文（openai.com） | 翻译日期 |",
    "|---|---|---|---|",
    *rows_zh,
    "",
]
if rows_en:
    lines += [
        "## 待翻译",
        "",
        "| 分类 | 英文原文 | 发布日期 |",
        "|---|---|---|",
        *rows_en,
        "",
    ]
    lines += [
        "## 来源与保真说明",
        "",
        "- 英文存档：`../openai-articles/posts/<slug>.md`（含 frontmatter：title/date/source/crawled/category）。",
        "- 抓取通道：本机 Chrome 直抓 + Wayback Machine 快照（openai.com 有 Cloudflare 挑战）。约 24 篇早期经由第三方阅读器的存档被证实不完整（截断/改写甚至虚构段落），已全部用原文重抓替换并重译；对照备份在 `posts_webreader_backup/`。",
        "- **未终验 4 篇**：`affective-use-study`、`browsecomp`、`core-dump-epidemiology-data-infrastructure-bug`、`harness-engineering` 因线上限频未能完成与当前页面的比对，存档为项目早期版本，内容可能与线上最新版有出入。复验：`python3 crawl_openai_final5_driver.py`。",
        "- OpenAI 会原地大幅改写已发布文章（如 Beyond rate limits、An alien mind、Advancing independent research），本存档为 2026-09-13 时点快照。",
        "- 链接、图片 URL、代码、公式均原样保留；图片未存档（正文保留原站 URL）。",
        "",
    ]
out = ROOT / "openai-articles-zh" / "README.md"
out.write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {out}: zh={total_zh} en={total_en} pending={len(rows_en)}")
