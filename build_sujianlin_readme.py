#!/usr/bin/env python3
"""根据转换报告生成 sujianlin-articles/README.md 与 INDEX.md。"""
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUT = BASE / "sujianlin-articles"

report = json.loads((BASE / "sujianlin-src" / "convert_report.json").read_text(encoding="utf-8"))
rows = sorted(report["rows"], key=lambda r: (r.get("date") or "", r["id"]))

by_cat = defaultdict(list)
for r in rows:
    by_cat[r.get("category") or "未分类"].append(r)

years = defaultdict(int)
for r in rows:
    y = (r.get("date") or "未知")[:4]
    years[y] += 1

total_chars = sum(r.get("chars", 0) for r in rows)

readme = f"""# 苏剑林《科学空间》技术博客全量归档

- **作者**：苏剑林（[科学空间 | Scientific Spaces](https://kexue.fm)），NLP/深度学习研究者，GitHub [bojone](https://github.com/bojone)，[bert4keras](https://github.com/bojone/bert4keras) 等开源库作者
- **抓取日期**：{date.today().isoformat()}
- **文章总数**：{len(rows)} 篇（{rows[0].get("date")} ～ {rows[-1].get("date")}）
- **正文总字数**：约 {total_chars // 10000} 万字符
- **格式**：Markdown（含 YAML frontmatter），公式保留原始 LaTeX（`$...$` / `\\begin{{equation}}`），图片与站内链接已绝对化并指向原站
- **抓取方式**：全站归档页枚举 + 单篇页面转换；评论区、打赏、引用样板未收录

## 目录结构

按博客分类分目录，文件名格式 `文章ID-标题.md`：

| 分类 | 篇数 |
|---|---:|
{chr(10).join(f"| {c} | {len(ps)} |" for c, ps in sorted(by_cat.items(), key=lambda x: -len(x[1])))}

## 按年分布

{ "、".join(f"{y}年 {n} 篇" for y, n in sorted(years.items())) }

## 使用说明

- 完整清单见 [INDEX.md](INDEX.md)（按分类分组、组内按时间排序，含标签与原文链接）
- 原始 HTML 存于 `../sujianlin-src/posts/`
- 公式渲染需支持 MathJax/KaTeX 的 Markdown 查看器（如 Typora、Obsidian、VS Code + Markdown Preview Enhanced）
"""

OUT.joinpath("README.md").write_text(readme, encoding="utf-8")

index_lines = ["# 科学空间全站文章索引（按分类分组，组内按时间排序）", ""]
cur_cat = None
for r in rows:
    cat = r.get("category") or "未分类"
    if cat != cur_cat:
        cur_cat = cat
        index_lines += ["", f"## {cat}（{len(by_cat[cat])} 篇）", "", "| 日期 | 标题 | 标签 |", "|---|---|---|"]
    tags = " ".join(f"`{t}`" for t in (r.get("tags") or []))
    title = (r.get("title") or "").replace("|", "｜")
    index_lines.append(
        f'| {r.get("date","")} | [{title}](https://kexue.fm/archives/{r["id"]}) | {tags} |'
    )
OUT.joinpath("INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
print(f"README.md + INDEX.md written, {len(rows)} rows, {len(by_cat)} categories")
