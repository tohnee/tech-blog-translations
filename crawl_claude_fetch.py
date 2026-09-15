#!/usr/bin/env python3
"""Fetch claude.com/blog articles with plain curl (site is CF-free) and
convert the Webflow rich-text body to Markdown.

Usage:
  crawl_claude_fetch.py <job.json>
    job.json: [{"slug":..., "url":...}, ...]
  crawl_claude_fetch.py --finalize <slug>

Fetch stage saves /tmp/claude_html/<slug>.html (+ .meta.json with og title/date).
Finalize converts to posts/<slug>.md (mirrors crawl_openai_finalize.py output
format). Skips already-fetched/finalized slugs (resumable).
"""
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parent
POSTS = (ROOT / "claude-blog-articles" / "posts").resolve()
HTML_DIR = Path("/tmp/claude_html").resolve()
CRAWLED = "2026-09-14"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def safe(dirpath: Path, name: str) -> Path:
    p = (dirpath / name).resolve()
    if not p.is_relative_to(dirpath):
        raise ValueError(f"bad name: {name}")
    return p


def fetch(job):
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    for j in job:
        if not j["url"].startswith("https://claude.com/blog/"):
            raise SystemExit(f"host not allowed: {j['url']}")
        out = safe(HTML_DIR, f"{j['slug']}.html")
        if out.exists() and out.stat().st_size > 50_000:
            print(f"SKIP {j['slug']}", flush=True)
            continue
        r = subprocess.run(
            ["curl", "-sL", "-A", UA, "--max-time", "90", "-o", str(out), j["url"]],
            capture_output=True)
        size = out.stat().st_size if out.exists() else 0
        ok = r.returncode == 0 and size > 50_000
        print(("OK " if ok else "FAIL ") + f"{j['slug']} {size}", flush=True)


def clean_text(t):
    return t.replace("\u2060", "").replace("\u200b", "").replace("\u00ad", "")


def inline(el):
    parts = []
    for c in el.children:
        if isinstance(c, NavigableString):
            parts.append(clean_text(str(c)))
        elif isinstance(c, Tag):
            n = c.name
            if n in ("strong", "b"):
                inner = inline(c).strip()
                if inner:
                    parts.append(f"**{inner}**")
            elif n in ("em", "i"):
                inner = inline(c).strip()
                if inner:
                    parts.append(f"*{inner}*")
            elif n == "code":
                parts.append(f"`{c.get_text()}`")
            elif n == "a":
                href = c.get("href") or ""
                if href.startswith("/"):
                    href = "https://claude.com" + href
                txt = inline(c).strip()
                if not txt:
                    continue
                if href.startswith(("http", "mailto", "#")):
                    parts.append(f"[{txt}]({href})" if not href.startswith("#") else txt)
                else:
                    parts.append(txt)
            elif n == "br":
                parts.append("\n")
            else:
                parts.append(inline(c))
    out = re.sub(r"[ \t\r\u00a0]+", " ", "".join(parts))
    out = re.sub(r" +\n", "\n", out)
    return re.sub(r"\n +", "\n", out).strip()


def block(el):
    n = el.name
    if n in ("nav", "aside", "form", "button"):
        return None
    if n in ("h1", "h2", "h3", "h4", "h5", "h6"):
        txt = inline(el)
        return (f"{'#' * int(n[1])} {txt}") if txt else None
    if n == "p":
        return inline(el) or None
    if n in ("ul", "ol"):
        items, idx = [], 0
        for li in el.find_all("li", recursive=False):
            # skip nested list duplication: only top-level items
            idx += 1
            txt = inline(li)
            if txt:
                items.append(("- " if n == "ul" else f"{idx}. ") + txt)
        return "\n".join(items) or None
    if n == "blockquote":
        txt = inline(el)
        return "\n".join("> " + ln for ln in txt.split("\n")) if txt else None
    if n == "figure":
        cap = el.find("figcaption")
        return inline(cap) if cap else None
    if n == "figcaption":
        return inline(el) or None
    if n == "hr":
        return "---"
    if n == "table":
        rows = []
        for tr in el.find_all("tr"):
            cells = [inline(td) or "" for td in tr.find_all(["td", "th"])]
            rows.append("| " + " | ".join(cells) + " |")
        return "\n".join(rows) or None
    if n == "pre":
        return "```\n" + el.get_text() + "\n```"
    inner = []
    for c in el.children:
        if isinstance(c, Tag):
            r = block(c)
            if r:
                inner.append(r)
    return "\n\n".join(inner) or None


def finalize(slug):
    html_path = safe(HTML_DIR, f"{slug}.html")
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    meta = lambda n: (soup.find("meta", property=n) or soup.find("meta", attrs={"name": n}))
    title = (meta("og:title")["content"].strip() if meta("og:title") else
             (soup.find("h1").get_text(strip=True) if soup.find("h1") else slug))
    title = re.sub(r"\s*\|\s*Claude by Anthropic\s*$", "", title)
    date_str = ""
    for s in soup.find_all("script", type="application/ld+json"):
        txt = s.string or ""
        m = re.search(r'"datePublished"\s*:\s*"([A-Za-z]+ \d{1,2}, \d{4})"', txt)
        if m:
            MONTHS = {mm: i for i, mm in enumerate(
                ["January", "February", "March", "April", "May", "June", "July",
                 "August", "September", "October", "November", "December"], 1)}
            SHORT = {k[:3]: v for k, v in MONTHS.items()}
            mm = re.match(r"([A-Za-z]+) (\d{1,2}), (\d{4})", m.group(1))
            if mm and (mm.group(1) in MONTHS or mm.group(1) in SHORT):
                mon = (MONTHS | SHORT)[mm.group(1)]
                date_str = f"{mm.group(3)}-{mon:02d}-{int(mm.group(2)):02d}"
            break
    if not date_str:
        m = re.search(r'"(?:publishedAt|datePublished|firstPublishedAt)"\s*:\s*"(\d{4}-\d{2}-\d{2})', html_path.read_text(encoding="utf-8"))
        date_str = m.group(1) if m else ""

    # body: the <section> inside <main> with the most <p> (blog body section)
    main = soup.find("main")
    if main is None:
        print(f"ERROR {slug}: no <main>"); sys.exit(1)
    best, best_n = None, -1
    for sec in main.find_all("section", recursive=False):
        n = len(sec.find_all("p"))
        if n > best_n:
            best, best_n = sec, n
    if best is None or best_n < 1:
        print(f"ERROR {slug}: no body section"); sys.exit(1)

    for junk in best.find_all(["script", "style", "form", "button", "nav",
                               "iframe", "svg", "video", "source", "noscript"]):
        junk.decompose()

    blocks, seen = [], set()
    for el in best.find_all(["h1", "h2", "h3", "h4", "p", "ul", "ol", "blockquote",
                             "figure", "table", "pre", "hr"], recursive=True):
        r = block(el)
        if not r or r in seen:
            continue
        seen.add(r)
        blocks.append(r)
    content = "\n\n".join(blocks).strip() + "\n"

    def yq(t):
        return t.replace("\\", "\\\\").replace('"', '\\"')

    fm = (f'---\ntitle: "{yq(title)}"\ndate: {date_str}\nsource: https://claude.com/blog/{slug}/\n'
          f"crawled: {CRAWLED}\n---\n\n")
    POSTS.mkdir(parents=True, exist_ok=True)
    out = safe(POSTS, f"{slug}.md")
    out.write_text(fm + content, encoding="utf-8")
    print(f"OK size={out.stat().st_size} title={title!r} date={date_str} blocks={len(blocks)}")


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--finalize":
        finalize(sys.argv[2])
    else:
        fetch(json.loads(Path(sys.argv[1]).read_text()))


if __name__ == "__main__":
    main()
