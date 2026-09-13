#!/usr/bin/env python3
"""Build a categorized README index from the crawled markdown files."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "sebastianraschka-articles"

FM_TITLE = re.compile(r'^title:\s*"(.+)"\s*$', re.M)
FM_SRC = re.compile(r"^source:\s*(\S+)\s*$", re.M)


def meta(path):
    text = path.read_text(encoding="utf-8")
    end = text.find("---", 4)
    head = text[: end if end != -1 else 800]
    t = FM_TITLE.search(head)
    s = FM_SRC.search(head)
    return (t.group(1) if t else path.stem), (s.group(1) if s else "")


def collect(subdir, pattern):
    files = sorted((ROOT / subdir).glob(pattern)) if (ROOT / subdir).exists() else []
    return [(str(f.relative_to(ROOT)), *meta(f)) for f in files]


def bullet(rel, title):
    return f"- [{title}]({rel})"


lines = [
    "# Sebastian Raschka 网站技术文章完整存档",
    "",
    f"> 来源：[sebastianraschka.com](https://sebastianraschka.com) · 抓取日期：2026-09-06 · 共 317 篇",
    ">",
    "> 每篇均为 Markdown 文件，头部含 `title` / `source`（原文链接）/ `crawled` 元数据。",
    "> 图片与外部链接已转为绝对 URL，正文中的站内链接指向原网站。",
    "",
]

# --- Blog by year ---
blog = collect("blog", "*/[!_]*.md")
lines += ["## 博客文章（Blog，79 篇）", ""]
years = {}
for rel, title, _ in blog:
    year = rel.split("/")[1]
    years.setdefault(year, []).append((rel, title))
for year in sorted(years):
    lines += [f"### {year}（{len(years[year])} 篇）", ""]
    lines += [bullet(rel, title) for rel, title in years[year]]
    lines += [""]

# --- Legacy Articles ---
arts = collect("articles", "*.md")
lines += ["## 经典教程（Articles，27 篇）", "", "2013–2015 年的早期长文教程：Python、NumPy、PCA、朴素贝叶斯、集成方法等。", ""]
lines += [bullet(rel, title) for rel, title, _ in arts] + [""]

# --- FAQ ---
faq = collect("faq", "*.md")
lines += ["## 机器学习 FAQ（180 篇）", "", "简明问答式技术条目：ML 基础、深度学习、优化、评估、LLM 概念等。", ""]
lines += [bullet(rel, title) for rel, title, _ in faq] + [""]

# --- Gallery ---
gal = collect("llm-architecture-gallery", "*.md")
lines += ["## LLM 架构图解（31 篇）", "", "注意力机制、MoE、归一化等现代 LLM 架构组件的图解教程。", ""]
lines += [bullet(rel, title) for rel, title, _ in gal] + [""]

# --- Magazine (Ahead of AI) ---
mag = collect("magazine", "*/[!_]*.md")
if mag:
    lines += ["## Ahead of AI 专栏（Magazine）", "", "Substack 专栏文章，按发布年份存放。", ""]
    lines += [bullet(rel, title) for rel, title, _ in mag] + [""]

total = len(blog) + len(arts) + len(faq) + len(gal) + len(mag)
lines[2] = f"> 来源：[sebastianraschka.com](https://sebastianraschka.com) · 抓取日期：2026-09-06（2026-09-11 增补专栏） · 共 {total} 篇"

out = ROOT / "README.md"
out.write_text("\n".join(lines), encoding="utf-8")
print(f"README.md written: {total} entries")
