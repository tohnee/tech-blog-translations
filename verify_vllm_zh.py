#!/usr/bin/env python3
"""Verify the zh translation archive and build vllm-articles-zh/README.md."""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
EN = ROOT / "vllm-articles"
ZH = ROOT / "vllm-articles-zh"


def fm_field(text: str, field: str) -> str:
    m = re.search(rf"^{field}: (.*)$", text.split("---", 2)[1], re.M)
    if not m:
        return ""
    val = m.group(1).strip()
    if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
        val = val[1:-1]
    return val


def main() -> None:
    meta = json.loads((EN / "meta.json").read_text())
    meta.sort(key=lambda p: (p["slug"][:4], p["slug"]))
    problems: list[str] = []
    rows = []
    by_year: dict[str, list] = defaultdict(list)

    for p in meta:
        slug = p["slug"]
        zh_path = ZH / "posts" / f"{slug}.md"
        en_path = EN / "posts" / f"{slug}.md"
        if not zh_path.exists():
            problems.append(f"MISSING zh file: {slug}")
            continue
        zh = zh_path.read_text()
        en = en_path.read_text()
        title = fm_field(zh, "title")
        if not title:
            problems.append(f"NO title in zh: {slug}")
        if "translated: 2026-09-1" not in zh:
            problems.append(f"NO translated date: {slug}")
        if "<!--TRANSLATION-CONTINUES-->" in zh:
            problems.append(f"LEFTOVER sentinel: {slug}")
        ratio = len(zh) / max(len(en), 1)
        if ratio < 0.25:
            problems.append(f"SUSPICIOUSLY SHORT ({ratio:.2f}): {slug}")
        # math preservation check on the known formula-heavy posts
        en_math = re.findall(r"\$[^$\n]+\$", en)
        zh_math = re.findall(r"\$[^$\n]+\$", zh)
        if len(en_math) > 3 and len(zh_math) < len(en_math) * 0.9:
            problems.append(
                f"MATH LOSS: {slug} en={len(en_math)} zh={len(zh_math)}")
        year = slug[:4]
        by_year[year].append((slug, title, p["url"]))
        rows.append((slug, title))

    done = len(rows)
    print(f"translated: {done}/{len(meta)}")
    print(f"problems: {len(problems)}")
    for pr in problems:
        print("  !!", pr)

    # README
    lines = [
        "# vLLM 官方博客中文翻译",
        "",
        "vLLM 官方博客 [vllm.ai/blog](https://vllm.ai/blog) 全部文章的完整中文翻译"
        "（术语遵循本项目[翻译规范](../TRANSLATION_GUIDE_VLLM.md)）。",
        "",
        f"## 进度：{done} / {len(meta)}",
        "",
    ]
    for year in sorted(by_year):
        lines.append(f"## {year} 年")
        lines.append("")
        for slug, title, url in by_year[year]:
            lines.append(
                f"- [x] [{title}](posts/{slug}.md) · [EN]({url})")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("英文原文存档见 [`vllm-articles/`](../vllm-articles/)；"
                 "翻译规范与术语表见 [`TRANSLATION_GUIDE_VLLM.md`](../TRANSLATION_GUIDE_VLLM.md)。")
    (ZH / "README.md").write_text("\n".join(lines))
    print(f"README written with {done} entries")


if __name__ == "__main__":
    main()
