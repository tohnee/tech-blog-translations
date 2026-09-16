#!/usr/bin/env python3
"""生成 semianalysis-articles-zh/README.md 索引，并校验中英文件一一对应。"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EN = ROOT / "semianalysis-articles" / "posts"
ZH = ROOT / "semianalysis-articles-zh" / "posts"
meta = json.load(open(ROOT / "semianalysis-articles" / "meta.json"))
by_slug = {m["slug"]: m for m in meta}

en_files = {p.stem for p in EN.glob("*.md")}
zh_files = {p.stem for p in ZH.glob("*.md")}

missing_en = en_files - set(by_slug)
extra_meta = set(by_slug) - en_files
not_translated = sorted(en_files - zh_files)
orphans = sorted(zh_files - en_files)

print(f"EN posts: {len(en_files)} | ZH posts: {len(zh_files)} | 未译: {len(not_translated)} | 多余译文: {len(orphans)}")
if missing_en:
    print("meta 缺失:", missing_en)
if extra_meta:
    print("meta 多余:", extra_meta)
if orphans:
    print("多余译文:", orphans[:20])

items = sorted(meta, key=lambda m: m["date"], reverse=True)
lines = [
    "# SemiAnalysis 文章中文翻译索引",
    "",
    "> 来源：[SemiAnalysis](https://semianalysis.com)（[Substack: newsletter.semianalysis.com](https://newsletter.semianalysis.com)），半导体与 AI 基础设施研究机构。",
    f"> 归档：英文 {len(en_files)} 篇（`semianalysis-articles/posts/`），中文翻译 {len(zh_files)} 篇（本目录 `posts/`）。",
    "> 翻译规范：`TRANSLATION_GUIDE_SEMIANALYSIS.md`。",
    "",
    "**付费墙说明**：标有 🔒 的文章为付费订阅文，Substack 公开 API 仅提供付费墙之前的预览正文；",
    "其归档与译文均只含公开预览部分（文内有显式标注），并非全文。无标记的文章为官方全文。",
    "",
    "| 日期 | 标题（中文） | 原文标题 | 作者 | 篇幅 |",
    "|---|---|---|---|---|",
]
zh_readme_titles = {}
for m in items:
    slug = m["slug"]
    lock = " 🔒" if m["paywalled"] else ""
    zh_path = ZH / f"{slug}.md"
    zh_title = m["title"]
    if zh_path.exists():
        text = zh_path.read_text(errors="replace")
        for ln in text.splitlines():
            if ln.startswith("title:"):
                zh_title = ln[6:].strip().strip('"')
                break
        link = f"[译文](posts/{slug}.md) · [EN](../../semianalysis-articles/posts/{slug}.md)"
    else:
        link = f"[EN](../../semianalysis-articles/posts/{slug}.md)（未译）"
    zh_readme_titles[slug] = zh_title
    lines.append(
        f"| {m['date']} | {zh_title}{lock} | {m['title']} | {', '.join(m['authors'][:3])} | {link} |"
    )
(ROOT / "semianalysis-articles-zh").mkdir(parents=True, exist_ok=True)
(ROOT / "semianalysis-articles-zh" / "README.md").write_text("\n".join(lines) + "\n")
print("README.md written:", len(items), "entries")
sys.exit(1 if (not_translated or orphans or missing_en) else 0)
