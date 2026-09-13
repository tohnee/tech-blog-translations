#!/usr/bin/env python3
"""Re-fetch all vLLM blog posts' HTML to a local cache and report MathJax usage.

Also reconstructs MathJax SVG formulas back to plain math text (using the
data-c Unicode codepoints and data-mml-node structure in each mjx-container)
so the converter can emit proper $...$ inline math.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from crawl_vllm import ALLOWED_HOSTS, fetch, validate_url  # noqa: E402

ROOT = Path(__file__).parent
CACHE = ROOT / "vllm-articles" / "html"
CACHE.mkdir(parents=True, exist_ok=True)


def main():
    slugs = [s.strip() for s in Path("/tmp/vllm_slugs.txt").read_text().splitlines() if s.strip()]
    report = {}
    for i, slug in enumerate(slugs, 1):
        out = CACHE / f"{slug}.html"
        if not out.exists() or out.stat().st_size < 1000:
            try:
                out.write_text(fetch("https://vllm.ai/blog/" + slug))
            except Exception as e:  # noqa: BLE001
                print(f"[{i}] {slug} FETCH FAILED: {e}", file=sys.stderr)
                continue
            time.sleep(0.3)
        html = out.read_text()
        n = html.count("<mjx-container")
        report[slug] = n
        if n:
            print(f"{slug}: {n} formulas")
    (ROOT / "vllm-articles" / "mathjax_report.json").write_text(
        json.dumps(report, indent=2)
    )
    affected = {s: n for s, n in report.items() if n}
    print(f"total {len(report)} fetched, {len(affected)} posts contain math, "
          f"{sum(affected.values())} formulas total")


if __name__ == "__main__":
    main()
