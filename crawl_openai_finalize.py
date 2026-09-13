#!/usr/bin/env python3
"""Convert /tmp/oai_html/<slug>.html to posts/<slug>.md with YAML frontmatter.

Usage: crawl_openai_finalize.py <slug> <url> <category>
"""
import json, re, sys, datetime
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag

slug, url, category = sys.argv[1], sys.argv[2], sys.argv[3]
if not url.startswith("https://openai.com/index/"):
    raise SystemExit(f"host not allowed: {url}")

ROOT = Path(__file__).resolve().parent
POSTS = (ROOT / "openai-articles" / "posts").resolve()
HTML_DIR = Path("/tmp/oai_html").resolve()
if not url.rstrip("/").startswith("https://openai.com/index/"):
    raise SystemExit(f"bad url: {url}")
html_path = (HTML_DIR / f"{slug}.html").resolve()
if not html_path.is_relative_to(HTML_DIR):
    raise SystemExit(f"bad slug: {slug}")
out_path = (POSTS / f"{slug}.md").resolve()
if not out_path.is_relative_to(POSTS):
    raise SystemExit(f"bad slug: {slug}")

s = html_path.read_text(encoding="utf-8")
soup = BeautifulSoup(s, "html.parser")
art = soup.find("article")
if art is None:
    print("ERROR: no <article>"); sys.exit(1)

MONTHS = {m: i for i, m in enumerate(
    ["January","February","March","April","May","June","July","August",
     "September","October","November","December"], 1)}
SHORT = {m[:3]: i for m, i in MONTHS.items()}

def parse_date(text):
    text = text.replace("\u2060", "").strip()
    m = re.match(r"^([A-Z][a-z]+)\.?\s+(\d{1,2}),\s*(\d{4})$", text)
    if m and m.group(1) in (MONTHS | SHORT):
        mon = (MONTHS | SHORT)[m.group(1)]
        return f"{m.group(3)}-{mon:02d}-{int(m.group(2)):02d}"
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", text)
    if m:
        return m.group(0)
    return None

# --- hero: first direct child div containing date + h1 ---
date = None
h1 = art.find("h1")
if h1 is None:
    print("ERROR: no <h1>"); sys.exit(1)
title = h1.get_text(" ", strip=True)
# date: search article text top region for a date string
for el in art.find_all(string=True):
    t = str(el).strip()
    if t and re.match(r"^(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)", t) and re.search(r"\d{1,2},?\s*\d{4}$|^\d{4}-\d{2}-\d{2}$", t):
        date = parse_date(t)
        break

# --- body container: direct child div/section of article with most descendants ---
best, best_n = None, -1
for child in art.find_all(["div", "section"], recursive=False):
    n = len(child.find_all(True))
    if n > best_n:
        best, best_n = child, n
if best is None:
    print("ERROR: no body container"); sys.exit(1)

# --- cleaning ---
for junk in best.find_all(["script", "style", "img", "video", "source", "button", "svg", "iframe", "noscript", "form"]):
    junk.decompose()
for el in best.find_all("span"):
    if el.get_text(strip=True) in ("(opens in a new window)", "opens in a new window", "⁠"):
        el.decompose()

def clean_text(t):
    t = t.replace("\u2060", "").replace("\u200b", "").replace("\u00ad", "")
    return t

def inline(el, raw=False):
    parts = []
    for c in el.children:
        if isinstance(c, NavigableString):
            parts.append(clean_text(str(c)))
        elif isinstance(c, Tag):
            name = c.name
            if name in ("strong", "b"):
                inner = inline(c, raw=True).strip()
                if inner: parts.append(f"**{inner}**")
            elif name in ("em", "i"):
                inner = inline(c, raw=True).strip()
                if inner: parts.append(f"*{inner}*")
            elif name == "code":
                parts.append(f"`{c.get_text()}`")
            elif name == "a":
                href = c.get("href") or ""
                if href.startswith("/"):
                    href = "https://openai.com" + href
                txt = inline(c, raw=True).strip()
                if not txt:
                    continue
                if href.startswith(("http", "mailto")):
                    parts.append(f"[{txt}]({href})")
                else:
                    parts.append(txt)
            elif name == "br":
                parts.append("\n")
            else:
                parts.append(inline(c, raw=True))
    # collapse whitespace but preserve intentional \n
    out = re.sub(r"[ \t\r\u00a0]+", " ", "".join(parts))
    out = re.sub(r" +\n", "\n", out)
    out = re.sub(r"\n +", "\n", out)
    # ensure space between word chars and link/bold markers (e.g. "see[the" -> "see [the")
    out = re.sub(r"(?<=[A-Za-z,;])\[(?=[A-Za-z])", " [", out)
    out = re.sub(r"\](?=[A-Za-z])", "] ", out)
    out = re.sub(r"(?<=[A-Za-z,;:])\*\*(?=[A-Za-z(\u201c])", "** ", out)
    out = re.sub(r"(?<=[A-Za-z,;])\*(?=[A-Za-z])", " *", out)
    return out.strip() if not raw else out

def block(el, depth=0):
    name = el.name
    if name in ("nav", "aside"):
        return None
    if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
        level = int(name[1])
        txt = inline(el)
        if not txt: return None
        return "#" * level + " " + txt
    if name == "p":
        return inline(el) or None
    if name == "figure":
        cap = el.find("figcaption")
        return inline(cap) if cap else None
    if name == "figcaption":
        return inline(el) or None
    if name in ("ul", "ol"):
        items = []
        idx = 0
        for li in el.find_all("li", recursive=False):
            idx += 1
            txt = inline(li)
            if txt:
                items.append(("- " if name == "ul" else f"{idx}. ") + txt)
        return "\n".join(items) or None
    if name == "blockquote":
        txt = inline(el)
        if not txt: return None
        return "\n".join("> " + line for line in txt.split("\n"))
    if name == "hr":
        return "---"
    if name == "table":
        rows = []
        for tr in el.find_all("tr"):
            cells = [inline(td) or "" for td in tr.find_all(["td", "th"])]
            rows.append("| " + " | ".join(cells) + " |")
        return "\n".join(rows) or None
    if name == "pre":
        return "```\n" + el.get_text() + "\n```"
    # container: recurse into block children
    inner = []
    for c in el.children:
        if isinstance(c, Tag):
            r = block(c, depth + 1)
            if r: inner.append(r)
    return "\n\n".join(inner) or None

blocks = []
for child in best.children:
    if isinstance(child, Tag):
        r = block(child)
        if r and r.strip():
            blocks.append(r.strip())
content = "\n\n".join(blocks).strip() + "\n"

def yq(t):
    return t.replace("\\", "\\\\").replace('"', '\\"')

crawled = "2026-09-13"
fm = (f'---\ntitle: "{yq(title)}"\ndate: {date or ""}\n'
      f'source: {url}\ncrawled: {crawled}\ncategory: {category}\n---\n\n')
POSTS.mkdir(parents=True, exist_ok=True)
out_path.write_text(fm + content, encoding="utf-8")
size = out_path.stat().st_size
print(f"OK size={size} title={title!r} date={date} blocks={len(blocks)} chars={len(content)}")
