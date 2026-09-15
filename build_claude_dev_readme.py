#!/usr/bin/env python3
"""Generate README progress indexes for claude-blog-articles-zh and
openai-dev-articles-zh from their meta/lists + existing files."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def fm_field(p: Path, key: str) -> str:
    try:
        fm = p.read_text().split("---", 2)[1]
        m = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
        return (m.group(1).strip().strip('"') if m else "")
    except Exception:
        return ""


def build(meta_rows, en_dir, zh_dir, out_path, title, source_line, site_label):
    done, pending = [], []
    for m in meta_rows:
        slug = m["slug"] if isinstance(m, dict) else m
        en = en_dir / f"{slug}.md"
        z = zh_dir / f"{slug}.md"
        title_en = fm_field(en, "title") if en.exists() else slug
        src = fm_field(en, "source") if en.exists() else ""
        if z.exists():
            t = fm_field(z, "title").strip('"') or slug
            done.append(f"| [{t}](posts/{slug}.md) | [{title_en}]({src}) | {fm_field(z, 'translated') or '—'} |")
        else:
            pending.append(f"| [{title_en}]({src}) | {fm_field(en, 'date') or '—'} |")
    lines = [
        f"# {title}",
        "",
        f"> 进度：**中文 {len(done)} / {len(meta_rows)}**。{source_line}",
        "> 通用规范见仓库内对应 TRANSLATION_GUIDE_*.md。",
        "",
        "## 已翻译",
        "",
        "| 中文标题 | 英文原文 | 翻译日期 |",
        "|---|---|---|",
        *done,
        "",
    ]
    if pending:
        lines += ["## 待翻译", "", "| 英文原文 | 发布日期 |", "|---|---|", *pending, ""]
    lines += [
        "## 来源与保真说明",
        "",
        f"- 英文存档：`{en_dir.name}/posts/<slug>.md`（frontmatter：title/date/source/crawled）。",
        f"- {site_label}",
        "- 链接、代码、公式原样保留；图片未存档（正文保留原站 URL）。",
        "",
    ]
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out_path}: done={len(done)} pending={len(pending)}")


# claude
claude_meta = json.loads((ROOT / "claude-blog-articles" / "meta.json").read_text())
build(claude_meta, ROOT / "claude-blog-articles" / "posts",
      ROOT / "claude-blog-articles-zh" / "posts",
      ROOT / "claude-blog-articles-zh" / "README.md",
      "Claude 博客技术文章中文化（claude-blog-articles-zh）",
      "清单来自 claude.com 官方 sitemap，筛除客户故事/产品发布/企业合规/活动类，保留技术文章（2026-09-14 抓取）。",
      "抓取通道：claude.com 无反爬，curl 直抓 Webflow 页面并按富文本结构转 Markdown。")

# dev
dev_meta = json.loads((ROOT / "openai-dev-articles" / "meta.json").read_text())
tech = [j["slug"] for j in json.loads(Path("/tmp/dev_job_tech.json").read_text())] \
    if Path("/tmp/dev_job_tech.json").exists() else []
rows = [m for m in dev_meta if m["slug"] in set(tech)] if tech else dev_meta
build(rows, ROOT / "openai-dev-articles" / "posts",
      ROOT / "openai-dev-articles-zh" / "posts",
      ROOT / "openai-dev-articles-zh" / "README.md",
      "OpenAI 开发者博客中文化（openai-dev-articles-zh）",
      "developers.openai.com/blog 共 28 篇，筛选技术文章 14 篇（2026-09-14 抓取；清单全量见 ../openai-dev-articles/titles.md）。",
      "抓取通道：站方 Vercel WAF 对直连/代理均 403，经 Wayback Machine 原始快照（id_ 模式）获取。")
