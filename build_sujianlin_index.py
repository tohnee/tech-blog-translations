#!/usr/bin/env python3
"""解析科学空间归档页 content.html，生成全量文章索引 posts_index.json。"""
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
html = (BASE / "sujianlin-src" / "content_index.html").read_text(encoding="utf-8")

# 归档结构：<h3>YYYY年 (共N篇)</h3><ul><li><span>MM月</span><ul><li>DD日: <a href=".../archives/ID" target="_blank">TITLE</a> ...
year_re = re.compile(r"<h3>(\d{4})年[^<]*</h3>")
month_re = re.compile(r"<li><span>(\d{2})月</span><ul>(.*?)</ul></li>", re.S)
item_re = re.compile(
    r"<li>(\d{2})日:\s*<a href=\"https://kexue\.fm/archives/(\d+)\"[^>]*>(.*?)</a>", re.S
)

posts = []
for ym in year_re.finditer(html):
    year = int(ym.group(1))
    seg_end = html.find("<h3>", ym.end())
    seg = html[ym.end(): seg_end if seg_end != -1 else len(html)]
    for mm in month_re.finditer(seg):
        month = int(mm.group(1))
        for it in item_re.finditer(mm.group(2)):
            day = int(it.group(1))
            pid = int(it.group(2))
            title = re.sub(r"<[^>]+>", "", it.group(3)).strip()
            posts.append(
                {"id": pid, "title": title, "date": f"{year:04d}-{month:02d}-{day:02d}"}
            )

posts.sort(key=lambda p: (p["date"], p["id"]))
# 去重
seen = set()
unique = []
for p in posts:
    if p["id"] not in seen:
        seen.add(p["id"])
        unique.append(p)

out = BASE / "sujianlin-src" / "posts_index.json"
out.write_text(json.dumps(unique, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"indexed {len(unique)} posts, range {unique[0]['date']} .. {unique[-1]['date']}")
print("first:", unique[0])
print("last :", unique[-1])
