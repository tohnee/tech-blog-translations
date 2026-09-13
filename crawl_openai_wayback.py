#!/usr/bin/env python3
"""Fetch openai.com articles via Wayback Machine snapshots (no Cloudflare).

Usage: crawl_openai_wayback.py <job.json>
  job.json: [{"slug":..., "url":...}, ...]

For each slug:
  1. goto https://web.archive.org/web/2026id_/<url>  (redirects to latest 2026 snapshot)
  2. if snapshot exists, save article HTML + meta to /tmp/oai_html/<slug>.*
  3. skip slugs already fetched (html > 5KB)

Also verifies: page must contain <article>; otherwise the snapshot is
considered missing.
"""
import json, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

job_path = sys.argv[1]
jobs = json.loads(Path(job_path).read_text())
for j in jobs:
    if not j["url"].startswith("https://openai.com/index/"):
        raise SystemExit(f"host not allowed: {j['url']}")

OUTDIR = Path("/tmp/oai_html").resolve()
OUTDIR.mkdir(parents=True, exist_ok=True)
INTER_FETCH_SLEEP_MS = 8000


def safe_path(slug: str, suffix: str) -> Path:
    p = (OUTDIR / f"{slug}{suffix}").resolve()
    if not p.is_relative_to(OUTDIR):
        raise ValueError(f"bad slug: {slug}")
    return p


def pending(j):
    p = safe_path(j["slug"], ".html")
    return not (p.exists() and p.stat().st_size > 5000)


EXTRACT = """() => {
    const meta = (n) => document.querySelector(`meta[property="${n}"]`)?.content || document.querySelector(`meta[name="${n}"]`)?.content || '';
    let art = document.querySelector('article')
           || document.querySelector('main')
           || document.querySelector('[class*="post-body"]')
           || document.querySelector('body');
    const h1 = document.querySelector('h1')?.innerText || '';
    return {html: art.outerHTML, h1: h1, title: meta('og:title') || document.title,
            published: meta('article:published_time') || meta('article:publishedDate'),
            desc: meta('og:description'), titleTag: document.title};
}"""

with sync_playwright() as pw:
    browser = pw.chromium.launch(channel="chrome", headless=False)
    ctx = browser.new_context(viewport={"width": 1440, "height": 900},
        locale="en-US",
        extra_http_headers={"Accept-Language": "en-US,en;q=0.9"})
    page = ctx.new_page()
    for j in jobs:
        if not pending(j):
            print(f"SKIP {j['slug']} (exists)", flush=True)
            continue
        slug, url = j["slug"], j["url"]
        print(f"FETCH {slug} ...", flush=True)
        ok = False
        for attempt in range(2):
            try:
                page.goto(f"https://web.archive.org/web/2026id_/{url}",
                          wait_until="domcontentloaded", timeout=60000)
                time.sleep(5)
                html = page.content()
                title = page.title() or ""
                if "<article" in html and len(html) > 20000 and "Wayback Machine" not in title:
                    data = page.evaluate(EXTRACT)
                    safe_path(slug, ".html").write_text(data["html"], encoding="utf-8")
                    safe_path(slug, ".meta.json").write_text(json.dumps(
                        {k: data[k] for k in ("h1", "title", "published", "desc", "titleTag")},
                        ensure_ascii=False, indent=1), encoding="utf-8")
                    print(f"OK {slug} html={len(data['html'])} title={data['title']!r} published={data['published']!r} snap={page.url[:80]}", flush=True)
                    ok = True
                    break
                print(f"  attempt {attempt}: no snapshot (title={title[:60]!r} len={len(html)})", flush=True)
            except Exception as e:
                print(f"  attempt {attempt} error: {str(e)[:160]}", flush=True)
            time.sleep(10)
        if not ok:
            print(f"FAIL {slug}", flush=True)
        page.wait_for_timeout(INTER_FETCH_SLEEP_MS)
    browser.close()
