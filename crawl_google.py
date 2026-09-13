#!/usr/bin/env python3
"""Download the Google / Google DeepMind / Gemini blogs and convert each post to Markdown.

Sources:
  - deepmind-articles   https://deepmind.google/blog/<slug>/        (Google DeepMind blog)
  - gemini-articles     https://blog.google/products-and-platforms/products/gemini/<slug>/
                        https://blog.google/innovation-and-ai/models-and-research/gemini-models/<slug>/
  - google-blog-articles https://blog.google/innovation-and-ai/{models-and-research,technology/ai,technology/research}/<slug>/

Security: fetch() only accepts https and an exact host allowlist, and blocks
loopback/private/reserved addresses after DNS resolution (same policy as crawl_vllm.py).
"""
import ipaddress
import json
import re
import socket
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

ROOT = Path(__file__).parent
TODAY = date.today().isoformat()

ALLOWED_HOSTS = {"deepmind.google", "blog.google"}

UA = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


def validate_url(url: str) -> None:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https":
        raise ValueError(f"scheme not allowed: {parsed.scheme}")
    if parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError(f"host not allowed: {parsed.hostname}")
    infos = socket.getaddrinfo(parsed.hostname, 443, proto=socket.IPPROTO_TCP)
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        # 198.18.0.0/15 is the fake-IP range local proxies hand out for public
        # hostnames; a bare public name resolving into it means the request is
        # going through the user's proxy, not hitting an internal host.
        if ip in ipaddress.ip_network("198.18.0.0/15"):
            continue
        if (
            ip.is_loopback
            or ip.is_private
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
            or ip.is_unspecified
        ):
            raise ValueError(f"address blocked: {ip}")


def fetch(url: str, retries: int = 5) -> str:
    validate_url(url)
    last_exc = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", errors="replace")
        except Exception as e:  # noqa: BLE001
            last_exc = e
            print(f"  retry {attempt + 1} for {url}: {e}", file=sys.stderr)
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"failed after {retries} tries: {url}: {last_exc}")


class MdConverter(MarkdownConverter):
    def convert_pre(self, el, text, parent_tags=None):
        code = el.find("code")
        src = code if code is not None else el
        lang = ""
        for cls in src.get("class", []) or []:
            m = re.match(r"language-([\w+#.-]+)", cls)
            if m:
                lang = m.group(1)
                break
        body = src.get_text()
        return f"\n```{lang}\n{body}\n```\n"

    def convert_code(self, el, text, parent_tags=None):
        if el.find_parent("pre") is not None:
            return el.get_text()
        return f"`{el.get_text()}`"


CONV = MdConverter(heading_style="ATX", bullets="-")

CHROME_PAT = re.compile(
    r"share|social|breadcrumb|tts|audio-player|related|newsletter|subscribe|"
    r"comment|cookie|consent|footer|nav|menu|sidebar|promo|banner|pagination",
    re.I,
)


def absolutize(tag, attr, soup, page_url):
    from urllib.parse import urljoin

    for el in soup.find_all(tag):
        val = el.get(attr) if el.attrs is not None else None
        if not val:
            continue
        if val.startswith("//"):
            el[attr] = "https:" + val
        elif val.startswith("/"):
            el[attr] = urljoin(page_url, val)
        elif not val.startswith(("http://", "https://", "#", "mailto:")):
            el[attr] = urljoin(page_url, val)


def strip_chrome(soup):
    for sel in ("script", "style", "noscript", "button", "nav", "footer", "form", "svg"):
        for el in soup.find_all(sel):
            el.decompose()
    for el in list(soup.find_all(True)):
        attrs = el.attrs if el.attrs is not None else {}
        classes = " ".join(attrs.get("class", []) or [])
        ident = attrs.get("id", "") or ""
        if CHROME_PAT.search(classes) or CHROME_PAT.search(ident):
            el.decompose()


def jsonld(soup):
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            d = json.loads(s.string or "")
        except Exception:  # noqa: BLE001
            continue
        if isinstance(d, list):
            d = next((x for x in d if isinstance(x, dict) and x.get("@type") in
                      ("BlogPosting", "NewsArticle", "Article")), {})
        if isinstance(d, dict) and d.get("@type") in ("BlogPosting", "NewsArticle", "Article"):
            return d
    return {}


def authors_of(ld):
    out = []
    a = ld.get("author")
    if isinstance(a, dict):
        a = [a]
    if isinstance(a, list):
        for x in a:
            if isinstance(x, dict) and x.get("name"):
                out.append(x["name"])
            elif isinstance(x, str):
                out.append(x)
    return out


def md_clean(body: str) -> str:
    body = re.sub(r"\n{3,}", "\n\n", body)
    body = re.sub(r"[ \t]+\n", "\n", body)
    return body.strip() + "\n"


def drop_empty_heads(body: str) -> str:
    # remove markdown headings left with no following text in their block
    body = re.sub(r"^#{1,6}[^\n]*\n(?=\n?#{1,6}|\Z)", "", body, flags=re.M)
    return body


# ---------------------------------------------------------------- deepmind

def extract_deepmind(html: str, url: str):
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main")
    if main is None:
        return None
    ld = jsonld(soup)
    if not ld:
        return None

    title = ld.get("headline") or ""
    h1 = main.find("h1")
    if h1 and not title:
        title = h1.get_text(" ", strip=True)
    date = (ld.get("datePublished") or "")[:10] or None
    authors = authors_of(ld)

    sections = list(main.find_all(recursive=False))
    content = []
    cover = None
    for sec in sections:
        h2 = sec.find("h2")
        if h2 and "related" in h2.get_text(strip=True).lower():
            break
        if sec.find("h1") is not None and cover is None:
            cover = sec
            continue
        content.append(sec)

    # reuse the soup only for content sections
    frag = BeautifulSoup("<div></div>", "html.parser")
    for sec in content:
        frag.div.append(sec.extract() if sec.decomposed is False else sec)
    strip_chrome(frag)
    absolutize("img", "src", frag, url)
    absolutize("a", "href", frag, url)
    for img in frag.find_all("img"):
        if img.get("alt", "").strip() == "" and img.get("src"):
            img["alt"] = ""
    body = CONV.convert_soup(frag.div)
    body = drop_empty_heads(md_clean(body))
    if len(body) < 200:
        return None
    return {"title": title, "date": date, "authors": authors, "body": body}


# ------------------------------------------------------------ blog.google

def extract_bloggoogle(html: str, url: str):
    soup = BeautifulSoup(html, "html.parser")
    ld = jsonld(soup)
    if not ld:
        return None
    art = soup.find("article")
    if art is None:
        return None

    title = ld.get("headline") or ""
    h1 = art.find("h1")
    if h1 and not title:
        title = h1.get_text(" ", strip=True)
    date = (ld.get("datePublished") or "")[:10] or None
    authors = authors_of(ld)

    # tags for meta
    tags = []
    tagbox = art.find(class_=re.compile("article-tags"))
    if tagbox:
        tags = [a.get_text(" ", strip=True) for a in tagbox.find_all("a")]

    # the body lives in .article-container__content (fallback: whole article)
    content = art.find(class_="article-container__content") or art
    frag = BeautifulSoup("<div></div>", "html.parser")
    for child in list(content.children):
        frag.div.append(child)
    strip_chrome(frag)
    # drop leftover h1 (goes to frontmatter) and hero media duplication
    hh = frag.find("h1")
    if hh:
        hh.decompose()
    absolutize("img", "src", frag, url)
    absolutize("a", "href", frag, url)
    body = CONV.convert_soup(frag.div)
    body = drop_empty_heads(md_clean(body))
    # leftover page chrome the class filters missed
    body = re.sub(
        r"^(Posted in:?|Copy link|Listen to article.*|\[\[duration\]\].*"
        r"|Your browser does not support the audio element\.*|Back to top)$\n?",
        "",
        body,
        flags=re.M,
    )
    body = md_clean(body)
    if len(body) < 200:
        return None
    return {"title": title, "date": date, "authors": authors, "tags": tags, "body": body}


# ------------------------------------------------------------------ main

def load_urls(path: Path):
    urls = []
    for line in path.read_text().splitlines():
        u = line.strip()
        if u:
            urls.append(u.rstrip("/") + "/")
    return urls


def is_index(url: str) -> bool:
    # blog.google section landing pages, e.g. .../gemini/ or .../gemini-models/
    # (deepmind URLs are /blog/<slug>/, only 2 segments — never index pages)
    segs = [s for s in urllib.parse.urlparse(url).path.split("/") if s]
    return len(segs) < 3 and "deepmind.google" not in url


SOURCES = [
    {
        "name": "deepmind",
        "urls": ROOT / ".urls-deepmind.txt",
        "out": ROOT / "deepmind-articles",
        "extract": extract_deepmind,
    },
    {
        "name": "gemini",
        "urls": ROOT / ".urls-gemini.txt",
        "out": ROOT / "gemini-articles",
        "extract": extract_bloggoogle,
    },
    {
        "name": "google-blog",
        "urls": ROOT / ".urls-google-blog.txt",
        "out": ROOT / "google-blog-articles",
        "extract": extract_bloggoogle,
    },
]


def main():
    only = sys.argv[1:] or None
    for src in SOURCES:
        if only and src["name"] not in only:
            continue
        posts_dir = src["out"] / "posts"
        posts_dir.mkdir(parents=True, exist_ok=True)
        urls = [u for u in load_urls(src["urls"]) if not is_index(u)]
        meta_path = src["out"] / "meta.json"
        meta = json.loads(meta_path.read_text()) if meta_path.exists() else []
        done = {m["url"] for m in meta}
        skipped = []
        for i, url in enumerate(urls):
            slug = [s for s in urllib.parse.urlparse(url).path.split("/") if s][-1]
            outfile = posts_dir / f"{slug}.md"
            if url in done or outfile.exists():
                continue
            try:
                html = fetch(url)
                rec = src["extract"](html, url)
            except Exception as e:  # noqa: BLE001
                print(f"[{src['name']} {i + 1}/{len(urls)}] FAIL {url}: {e}", flush=True)
                skipped.append(url)
                continue
            if rec is None:
                print(f"[{src['name']} {i + 1}/{len(urls)}] SKIP (no content) {url}", flush=True)
                skipped.append(url)
                continue
            soup = BeautifulSoup(html, "html.parser")
            desc = ""
            m = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", property="og:description")
            if m and m.get("content"):
                desc = m["content"].strip()
            authors = rec.get("authors") or []
            fm_authors = ", ".join(authors)
            fm = (
                "---\n"
                f'title: "{rec["title"].replace(chr(34), chr(39))}"\n'
                f"source: {url}\n"
                f"site: {src['name']}\n"
                f"date: {rec.get('date') or 'unknown'}\n"
                f"authors: {fm_authors}\n"
                f"crawled: {TODAY}\n"
                "---\n\n"
            )
            outfile.write_text(fm + rec["body"], encoding="utf-8")
            meta.append({
                "slug": slug,
                "title": rec["title"],
                "date": rec.get("date"),
                "authors": authors,
                "tags": rec.get("tags", []),
                "description": desc[:300],
                "url": url,
            })
            meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"[{src['name']} {i + 1}/{len(urls)}] ok {slug} ({rec.get('date')})", flush=True)
            time.sleep(0.8)
        print(f"== {src['name']}: {len(meta)} saved, {len(skipped)} skipped", flush=True)


if __name__ == "__main__":
    main()
