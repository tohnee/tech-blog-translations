#!/usr/bin/env python3
"""Convert cached Anthropic engineering article pages to Markdown archive.

Input: /tmp/cc_meta/<slug>.html (fetched from anthropic.com/engineering/<slug>)
Output: claudecode-articles/<slug>.md with frontmatter.
"""
import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "claudecode-articles"
CACHE = Path("/tmp/cc_meta")
BASE = "https://www.anthropic.com"
TODAY = time.strftime("%Y-%m-%d")

SLUGS = [
    "how-we-contain-claude",
    "april-23-postmortem",
    "managed-agents",
    "claude-code-auto-mode",
    "harness-design-long-running-apps",
    "infrastructure-noise",
    "building-c-compiler",
    "AI-resistant-technical-evaluations",
    "demystifying-evals-for-ai-agents",
    "effective-harnesses-for-long-running-agents",
    "advanced-tool-use",
    "code-execution-with-mcp",
    "claude-code-sandboxing",
    "equipping-agents-for-the-real-world-with-agent-skills",
    "effective-context-engineering-for-ai-agents",
    "a-postmortem-of-three-recent-issues",
    "writing-tools-for-agents",
    "desktop-extensions",
    "multi-agent-research-system",
    "claude-code-best-practices",
    "claude-think-tool",
    "swe-bench-sonnet",
    "building-effective-agents",
    "contextual-retrieval",
    "eval-awareness-browsecomp",
]

_SEG = re.compile(r"^[A-Za-z0-9_-]+$")
_FILE = re.compile(r"^[A-Za-z0-9_-]+\.md$")


def safe_target(name: str) -> Path:
    if not _FILE.match(name):
        raise ValueError(f"unsafe filename rejected: {name!r}")
    target = (OUT / name).resolve()
    if not target.is_relative_to(OUT.resolve()):
        raise ValueError(f"resolved path outside output root: {name!r}")
    return target


def fetch_html(slug: str) -> str:
    f = CACHE / f"{slug}.html"
    if f.exists() and f.stat().st_size > 10000:
        return f.read_text(encoding="utf-8", errors="ignore")
    r = requests.get(f"{BASE}/engineering/{slug}", timeout=45,
                     headers={"User-Agent": "Mozilla/5.0 (compatible; personal-archive-bot/1.0)"})
    r.raise_for_status()
    return r.text


def clean(node):
    for sel in ("script", "style", "nav", "footer", "header", "noscript", "form"):
        for el in node.select(sel):
            el.decompose()


def absolutize(node):
    for tag, attr in (("a", "href"), ("img", "src")):
        for el in node.find_all(tag):
            v = el.get(attr)
            if v and not v.startswith(("http://", "https://", "mailto:", "#", "data:")):
                el[attr] = urljoin(BASE, v)


def extract_title(soup):
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(" ", strip=True)
    t = soup.title.get_text(strip=True) if soup.title else ""
    return t.split(" \\| ")[0].strip()


def extract_date(soup):
    # "Published | Mar 25, 2026" pattern near the h1
    m = re.search(r"Published\s*\|?\s*([A-Z][a-z]{2}\s+\d{1,2},\s+\d{4})",
                  soup.get_text(" ", strip=True))
    if not m:
        return ""
    from datetime import datetime
    for fmt in ("%b %d, %Y", "%B %d, %Y"):
        try:
            return datetime.strptime(m.group(1), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return ""


def extract_subjects(soup):
    html = str(soup)
    found = []
    for m in re.finditer(r'"subjects":\[(.*?)\]', html):
        for lbl in re.findall(r'"label":"([^"]+)"', m.group(1)):
            if lbl not in found:
                found.append(lbl)
    return found


def convert(slug):
    html = fetch_html(slug)
    soup = BeautifulSoup(html, "html.parser")
    art = soup.find("article")
    if art is None:
        raise RuntimeError(f"no <article> in {slug}")
    clean(art)
    absolutize(art)
    title = extract_title(soup)
    date = extract_date(soup)
    subjects = extract_subjects(soup)
    text = md(str(art), heading_style="ATX", bullets="-")
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if len(text) < 500:
        raise RuntimeError(f"content too short for {slug}: {len(text)}")

    fm = [f'title: "{title.replace(chr(34), chr(39))}"',
          f"source: {BASE}/engineering/{slug}"]
    if date:
        fm.append(f"published: {date}")
    if subjects:
        fm.append(f"subjects: {json.dumps(subjects, ensure_ascii=False)}")
    fm.append(f"crawled: {TODAY}")
    out = safe_target(f"{slug}.md")
    out.write_text("---\n" + "\n".join(fm) + "\n---\n\n"
                   f"# {title}\n\n> 原文：[{title}]({BASE}/engineering/{slug}) · Anthropic Engineering Blog\n\n{text}\n",
                   encoding="utf-8")
    return title, date, len(text)


def main():
    OUT.mkdir(exist_ok=True)
    report = {}
    for slug in SLUGS:
        try:
            title, date, n = convert(slug)
            report[slug] = {"title": title, "published": date, "chars": n, "status": "ok"}
            print(f"ok   {slug:55s} {date}  {n:>7d}  {title[:60]}")
        except Exception as e:
            report[slug] = {"status": f"error: {e}"}
            print(f"ERR  {slug}: {e}")
    (OUT / "_crawl_report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    n_ok = sum(1 for r in report.values() if r["status"] == "ok")
    print(f"done: {n_ok}/{len(SLUGS)}")


if __name__ == "__main__":
    main()
