#!/usr/bin/env python3
"""Regenerate google-articles-zh-README.md from the crawl manifests and zh folders."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
README = ROOT / "google-articles-zh-README.md"

SOURCES = [
    ("Google DeepMind 博客", "deepmind-articles", "deepmind-articles-zh"),
    ("Gemini 博客", "gemini-articles", "gemini-articles-zh"),
    ("Google 博客 AI/技术栏", "google-blog-articles", "google-blog-articles-zh"),
]


def year_of(datestr):
    return (datestr or "unknown")[:4]


def main():
    lines = [
        "# Google / Google DeepMind / Gemini 博客中文翻译",
        "",
        "三个来源的完整中文翻译，术语遵循项目 [翻译规范](TRANSLATION_GUIDE_GOOGLE.md)：",
        "Google DeepMind 博客（deepmind.google/blog）、Gemini 博客（blog.google 的 gemini 与",
        "gemini-models 栏）、Google 博客 AI/技术栏（blog.google 的 innovation-and-ai）。",
        "",
    ]
    total_en = total_zh = 0
    for label, en, zh in SOURCES:
        meta_path = ROOT / en / "meta.json"
        posts_en = ROOT / en / "posts"
        posts_zh = ROOT / zh / "posts"
        meta = json.loads(meta_path.read_text()) if meta_path.exists() else []
        en_files = {p.stem for p in posts_en.glob("*.md")} if posts_en.exists() else set()
        zh_files = {p.stem for p in posts_zh.glob("*.md")} if posts_zh.exists() else set()
        # meta 中缺的 slug 也算已存档（兜底）
        for s in en_files:
            if s not in {m["slug"] for m in meta}:
                meta.append({"slug": s, "title": s, "date": None, "url": f"https://{en.split('-')[0]}.google/"})
        total_en += len(en_files)
        total_zh += len(zh_files)
        lines.append(f"## {label}：{len(zh_files)} / {len(en_files)}")
        lines.append("")
        by_year = {}
        for m in meta:
            if m["slug"] not in en_files:
                continue
            by_year.setdefault(year_of(m.get("date")), []).append(m)
        for year in sorted(by_year, reverse=True):
            lines.append(f"### {year} 年")
            for m in sorted(by_year[year], key=lambda x: x.get("date") or "", reverse=True):
                slug = m["slug"]
                zh_rel = f"{zh}/posts/{slug}.md"
                if slug in zh_files:
                    box = "x"
                    link = f"[{m.get('title', slug)}]({zh_rel})"
                else:
                    box = " "
                    link = m.get("title", slug)
                url = m.get("url") or ""
                lines.append(f"- [{box}] {link} · [EN]({url})")
            lines.append("")
    lines.insert(4, f"## 总进度：{total_zh} / {total_en}")
    lines.insert(5, "")
    README.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {README.name}: {total_zh}/{total_en}")


if __name__ == "__main__":
    main()
