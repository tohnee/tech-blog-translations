#!/usr/bin/env python3
"""Fetch developers.openai.com/blog articles. The site 403s direct and via the
proxy (Vercel WAF), so fetch Wayback Machine raw snapshots through the SOCKS
proxy instead, then convert to Markdown.

Usage:
  crawl_devcrawl.py <job.json>     job: [{"slug","url"}]
  crawl_devcrawl.py --finalize <slug> <url>

Fetch -> /tmp/dev_html/<slug>.html ; Finalize -> openai-dev-articles/posts/<slug>.md
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parent
POSTS = (ROOT / "openai-dev-articles" / "posts").resolve()
HTML_DIR = Path("/tmp/dev_html").resolve()
CRAWLED = "2026-09-14"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
SOCKS = "127.0.0.1:10808"
INTER_SLEEP_S = 12


def safe(dirpath: Path, name: str) -> Path:
    p = (dirpath / name).resolve()
    if not p.is_relative_to(dirpath):
        raise ValueError(f"bad name: {name}")
    return p


def fetch(job):
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    for j in job:
        if not j["url"].startswith("https://developers.openai.com/blog/"):
            raise SystemExit(f"host not allowed: {j['url']}")
        out = safe(HTML_DIR, f"{j['slug']}.html")
        if out.exists() and out.stat().st_size > 30_000:
            print(f"SKIP {j['slug']}", flush=True)
            continue
        wb = f"https://web.archive.org/web/2026id_/{j['url']}"
        r = subprocess.run(
            ["curl", "-sL", "--compressed", "--socks5-hostname", SOCKS, "-A", UA,
             "--max-time", "90", "-o", str(out), wb],
            capture_output=True)
        size = out.stat().st_size if out.exists() else 0
        ok = r.returncode == 0 and size > 30_000
        if ok:
            txt = out.read_text(errors="replace")
            if "<article" not in txt or "Wayback Machine has not archived" in txt:
                ok = False
        print(("OK " if ok else "FAIL ") + f"{j['slug']} {size}", flush=True)
        import time
        time.sleep(INTER_SLEEP_S)


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
                    href = "https://developers.openai.com" + href
                txt = inline(c).strip()
                if not txt:
                    continue
                if href.startswith(("http", "mailto")):
                    parts.append(f"[{txt}]({href})")
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
        code = el.find("code")
        src = code if code is not None else el
        lang = ""
        for cls in src.get("class", []) or []:
            m = re.match(r"language-([\w+#.-]+)", cls)
            if m:
                lang = m.group(1)
                break
        return f"```{lang}\n{src.get_text()}\n```"
    inner = []
    for c in el.children:
        if isinstance(c, Tag):
            r = block(c)
            if r:
                inner.append(r)
    return "\n\n".join(inner) or None


def finalize(slug, url):
    html_path = safe(HTML_DIR, f"{slug}.html")
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    meta = lambda n: soup.find("meta", property=n)
    title = (meta("og:title")["content"].strip() if meta("og:title") and meta("og:title").get("content")
             else (soup.find("h1").get_text(strip=True) if soup.find("h1") else slug))
    date_str = ""
    if meta("article:published_time") and meta("article:published_time").get("content"):
        date_str = meta("article:published_time")["content"][:10]
    if not date_str:
        raw = html_path.read_text(encoding="utf-8")
        m = re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', raw)
        if m:
            date_str = m.group(1)
        else:
            MONTHS = {mm: i for i, mm in enumerate(
                ["January", "February", "March", "April", "May", "June", "July",
                 "August", "September", "October", "November", "December"], 1)}
            SHORT = {k[:3]: v for k, v in MONTHS.items()}
            m2 = re.search(r'\b([A-Za-z]{3,9}) (\d{1,2}), (20\d{2})\b', raw)
            if m2 and (m2.group(1) in MONTHS or m2.group(1) in SHORT):
                mon = (MONTHS | SHORT)[m2.group(1)]
                date_str = f"{m2.group(3)}-{mon:02d}-{int(m2.group(2)):02d}"

    art = soup.find("article")
    if art is None:
        print(f"ERROR {slug}: no <article>"); sys.exit(1)
    h1 = art.find("h1")
    if h1 is not None:
        title = h1.get_text(" ", strip=True)

    for junk in art.find_all(["script", "style", "form", "button", "nav",
                              "iframe", "svg", "video", "source", "noscript"]):
        junk.decompose()

    blocks, seen = [], set()
    for el in art.find_all(["h1", "h2", "h3", "h4", "p", "ul", "ol", "blockquote",
                            "figure", "table", "pre", "hr"], recursive=True):
        if el.find_parent(["li", "blockquote", "figure"]) is not None and el.name in ("p", "ul", "ol"):
            continue  # block() renders nested content via parents
        r = block(el)
        if not r or r in seen:
            continue
        seen.add(r)
        blocks.append(r)
    content = "\n\n".join(blocks).strip() + "\n"

    def yq(t):
        return t.replace("\\", "\\\\").replace('"', '\\"')

    fm = (f'---\ntitle: "{yq(title)}"\ndate: {date_str}\nsource: {url}\n'
          f"crawled: {CRAWLED}\n---\n\n")
    POSTS.mkdir(parents=True, exist_ok=True)
    out = safe(POSTS, f"{slug}.md")
    out.write_text(fm + content, encoding="utf-8")
    print(f"OK size={out.stat().st_size} title={title!r} date={date_str} blocks={len(blocks)}")


def main():
    if len(sys.argv) >= 4 and sys.argv[1] == "--finalize":
        finalize(sys.argv[2], sys.argv[3])
    else:
        fetch(json.loads(Path(sys.argv[1]).read_text()))


if __name__ == "__main__":
    main()
