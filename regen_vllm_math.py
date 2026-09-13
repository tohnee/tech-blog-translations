#!/usr/bin/env python3
"""Regenerate EN markdown for posts that contain MathJax formulas.

Uses the HTML cache written by scan_vllm_math.py and the math-restoring
converter in crawl_vllm.parse_post, then rewrites vllm-articles/posts/<slug>.md
and refreshes the corresponding meta.json entry.
"""
import json
from datetime import date
from pathlib import Path

from crawl_vllm import parse_post

ROOT = Path(__file__).parent
CACHE = ROOT / "vllm-articles" / "html"
POSTS = ROOT / "vllm-articles" / "posts"
META = ROOT / "vllm-articles" / "meta.json"


def main() -> None:
    report = json.loads((ROOT / "vllm-articles" / "mathjax_report.json").read_text())
    affected = [s for s, n in report.items() if n]
    print(f"{len(affected)} posts contain math")
    meta = json.loads(META.read_text())
    by_slug = {p["slug"]: p for p in meta}

    for slug in affected:
        html = (CACHE / f"{slug}.html").read_text()
        post = parse_post(slug, html)
        if post is None:
            print(f"  !! no <article>: {slug}")
            continue
        fm = (
            "---\n"
            f'title: "{post["title"].replace(chr(34), chr(39))}"\n'
            f"date: {post['date']}\n"
            f"source: {post['url']}\n"
            f"crawled: {date.today().isoformat()}\n"
            "---\n\n"
        )
        (POSTS / f"{slug}.md").write_text(fm + post["body"])
        if slug in by_slug:
            by_slug[slug] = {k: v for k, v in post.items() if k != "body"}
        print(f"  regenerated {slug} ({report[slug]} formulas)")

    META.write_text(json.dumps(sorted(meta, key=lambda p: p["slug"]),
                               ensure_ascii=False, indent=2))
    print("meta refreshed")


if __name__ == "__main__":
    main()
