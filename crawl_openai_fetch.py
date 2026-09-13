#!/usr/bin/env python3
"""Fetch openai.com article pages with Playwright Chromium (Cloudflare-safe).

Usage: crawl_openai_fetch.py <mode> <job.json>
  mode: headless | headed | chrome
  job.json: [{"slug":..., "url":...}, ...]
Saves /tmp/oai_html/<slug>.html containing article region HTML,
plus /tmp/oai_html/<slug>.meta.json with og:title/published_time/description.
Skips slugs whose .html already exists and is > 5KB.

URLs come only from the curated meta.json job list (https, host openai.com).
"""
import json, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

mode, job_path = sys.argv[1], sys.argv[2]
jobs = json.loads(Path(job_path).read_text())
for j in jobs:
    if not j["url"].startswith("https://openai.com/index/"):
        raise SystemExit(f"host not allowed: {j['url']}")

OUTDIR = Path("/tmp/oai_html").resolve()
OUTDIR.mkdir(parents=True, exist_ok=True)
INTER_FETCH_SLEEP_MS = 15000


def safe_path(slug: str, suffix: str) -> Path:
    p = (OUTDIR / f"{slug}{suffix}").resolve()
    if not p.is_relative_to(OUTDIR):
        raise ValueError(f"bad slug: {slug}")
    return p


def pending(j):
    p = safe_path(j["slug"], ".html")
    return not (p.exists() and p.stat().st_size > 5000)


def solve_wait(page, slug, deadline):
    """Wait until Cloudflare challenge clears and content present."""
    while time.time() < deadline:
        try:
            title = page.title()
        except Exception:
            title = ""
        if "just a moment" not in (title or "").lower():
            html = page.content()
            if len(html) > 20000 and ("<article" in html or "index-hero" in html or "post-hero" in html or len(page.text_content("body") or "") > 3000):
                return True
        page.wait_for_timeout(1500)
    return False


with sync_playwright() as pw:
    if mode == "chrome":
        browser = pw.chromium.launch(channel="chrome", headless=False)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900},
            locale="en-US",
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"})
    elif mode == "headed":
        browser = pw.chromium.launch(headless=False)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    else:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
    page = ctx.new_page()
    for j in jobs:
        if not pending(j):
            print(f"SKIP {j['slug']} (exists)", flush=True)
            continue
        slug, url = j["slug"], j["url"]
        print(f"FETCH {slug} ...", flush=True)
        ok = False
        for attempt in range(1):
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                if solve_wait(page, slug, time.time() + 75):
                    ok = True
                    break
                print(f"  attempt {attempt}: challenge not cleared", flush=True)
            except Exception as e:
                print(f"  attempt {attempt} error: {e}", flush=True)
            page.wait_for_timeout(30000)
        if not ok:
            print(f"FAIL {slug}")
            continue
        data = page.evaluate("""() => {
            const meta = (n) => document.querySelector(`meta[property="${n}"]`)?.content || document.querySelector(`meta[name="${n}"]`)?.content || '';
            let art = document.querySelector('article')
                   || document.querySelector('main')
                   || document.querySelector('[class*="post-body"]')
                   || document.querySelector('body');
            const h1 = document.querySelector('h1')?.innerText || '';
            return {html: art.outerHTML, h1: h1, title: meta('og:title') || document.title,
                    published: meta('article:published_time') || meta('article:publishedDate'),
                    desc: meta('og:description'), titleTag: document.title};
        }""")
        safe_path(slug, ".html").write_text(data["html"], encoding="utf-8")
        meta_path = safe_path(slug, ".meta.json")
        meta_path.write_text(json.dumps(
            {k: data[k] for k in ("h1", "title", "published", "desc", "titleTag")},
            ensure_ascii=False, indent=1), encoding="utf-8")
        blen = len(page.text_content("body") or "")
        print(f"OK {slug} html={len(data['html'])} body_text={blen} title={data['title']!r} published={data['published']!r}", flush=True)
        page.wait_for_timeout(INTER_FETCH_SLEEP_MS)
    browser.close()
