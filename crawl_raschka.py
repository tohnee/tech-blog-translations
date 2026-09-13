#!/usr/bin/env python3
"""Crawl all technical articles on sebastianraschka.com and convert to Markdown."""
import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

BASE = "https://sebastianraschka.com"
OUT_ROOT = Path(__file__).resolve().parent / "sebastianraschka-articles"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; personal-archive-bot/1.0)"}
TODAY = time.strftime("%Y-%m-%d")

session = requests.Session()
session.headers.update(HEADERS)

# Whitelist validation: directory segments allow only [A-Za-z0-9_-],
# the final file segment additionally allows a .md/.json extension.
# Any other character (including dots and slashes inside segments) is
# rejected before any filesystem operation happens.
_SEG = re.compile(r"^[A-Za-z0-9_-]+$")
_FILE = re.compile(r"^[A-Za-z0-9_-]+\.(md|json)$")


def safe_target(rel: str) -> Path:
    parts = rel.split("/")
    if not parts or any(not _SEG.match(p) for p in parts[:-1]) or not _FILE.match(parts[-1]):
        raise ValueError(f"unsafe relative path rejected: {rel!r}")
    root = OUT_ROOT.resolve()
    target = (root / Path(*parts)).resolve()
    if not target.is_relative_to(root):
        raise ValueError(f"resolved path outside output root: {rel!r}")
    return target


def load_sitemap():
    r = session.get(f"{BASE}/sitemap.xml", timeout=30)
    r.raise_for_status()
    urls = re.findall(r"<loc>([^<]+)</loc>", r.text)
    return [u for u in urls if u.startswith(BASE)]


def classify(url):
    path = urlparse(url).path
    if re.match(r"^/blog/\d{4}/[^/]+\.html$", path):
        return "blog"
    if path.startswith("/Articles/") and path.endswith(".html"):
        return "articles"
    if path.startswith("/faq/docs/") and path.endswith(".html"):
        return "faq"
    if re.match(r"^/llm-architecture-gallery/[^/]+/?$", path) and path != "/llm-architecture-gallery/":
        return "llm-architecture-gallery"
    return None


def extract_title(soup, fallback):
    if soup.title and soup.title.get_text(strip=True):
        t = soup.title.get_text(strip=True)
        for sep in (" | Sebastian Raschka, PhD", " | Sebastian Raschka",
                    " – Sebastian Raschka", " - Sebastian Raschka"):
            if t.endswith(sep):
                t = t[: -len(sep)]
        return t.strip()
    h1 = soup.find("h1")
    return h1.get_text(strip=True) if h1 else fallback


def pick_content(soup):
    for sel in ("article.post-content", "main#main-content", "main", "article"):
        node = soup.select_one(sel)
        if node:
            return node
    return soup.body or soup


def clean(node):
    for sel in ("script", "style", "nav", "footer", "header", "noscript",
                ".subscribe-section", ".cite-share", ".share-buttons", "form"):
        for el in node.select(sel):
            el.decompose()


def absolutize(node, base):
    """Rewrite relative hrefs/srcs to absolute URLs so links survive offline."""
    for tag, attr in (("a", "href"), ("img", "src")):
        for el in node.find_all(tag):
            val = el.get(attr)
            if val and not val.startswith(("http://", "https://", "mailto:", "#")):
                el[attr] = urljoin(base, val)


def html_to_markdown(html_bytes, url):
    soup = BeautifulSoup(html_bytes, "html.parser")  # bytes -> bs4 sniffs UTF-8 correctly
    title = extract_title(soup, os.path.basename(urlparse(url).path))
    content = pick_content(soup)
    clean(content)
    absolutize(content, url)
    text = md(str(content), heading_style="ATX", bullets="-", code_language="python")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return title, text


def fetch_one(url):
    path = urlparse(url).path
    if classify(url) == "blog":
        parts = [p for p in path.split("/") if p]  # blog, YEAR, file.html
        rel = f"blog/{parts[1]}/{parts[2][:-5]}.md"
    elif classify(url) == "faq":
        rel = f"faq/{os.path.basename(path)[:-5]}.md"
    elif classify(url) == "llm-architecture-gallery":
        slug = [p for p in path.split("/") if p][-1]
        rel = f"llm-architecture-gallery/{slug}.md"
    else:
        rel = f"articles/{os.path.basename(path)[:-5]}.md"

    out = safe_target(rel)
    if out.exists() and out.stat().st_size > 200:
        return rel, "cached"

    last_err = None
    for attempt in range(3):
        try:
            r = session.get(url, timeout=45)
            if r.status_code == 404:
                return rel, "404"
            r.raise_for_status()
            title, text = html_to_markdown(r.content, url)
            if len(text) < 80:
                return rel, "too-short"
            out.parent.mkdir(parents=True, exist_ok=True)
            safe_title = title.replace('"', "'")
            out.write_text(
                f"---\ntitle: \"{safe_title}\"\nsource: {url}\ncrawled: {TODAY}\n---\n\n# {title}\n\n{text}\n",
                encoding="utf-8",
            )
            return rel, "ok"
        except Exception as e:
            last_err = e
            time.sleep(1.5 * (attempt + 1))
    return rel, f"error: {last_err}"


def main():
    all_urls = load_sitemap()
    targets = sorted(u for u in all_urls if classify(u))
    print(f"sitemap urls: {len(all_urls)}, article targets: {len(targets)}")
    for cat in ("blog", "articles", "faq", "llm-architecture-gallery"):
        n = sum(1 for u in targets if classify(u) == cat)
        print(f"  {cat}: {n}")

    results = {}
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(fetch_one, u): u for u in targets}
        for i, fut in enumerate(as_completed(futs), 1):
            rel, status = fut.result()
            results[rel] = status
            if i % 25 == 0 or status not in ("ok", "cached"):
                print(f"[{i}/{len(targets)}] {status}: {rel}")

    counts = {}
    for s in results.values():
        key = s.split(":")[0]
        counts[key] = counts.get(key, 0) + 1
    print("summary:", json.dumps(counts, ensure_ascii=False))
    report = safe_target("_crawl_report.json")
    report.write_text(json.dumps(results, indent=1, sort_keys=True), encoding="utf-8")


if __name__ == "__main__":
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    main()
