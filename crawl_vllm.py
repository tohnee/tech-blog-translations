#!/usr/bin/env python3
"""Download the vLLM blog archive (vllm.ai/blog) and convert each post to Markdown.

Security: fetch() only accepts https and an exact host allowlist, and blocks
loopback/private/reserved addresses after DNS resolution.
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
OUT = ROOT / "vllm-articles" / "posts"
SLUGS_FILE = Path("/tmp/vllm_slugs.txt")
BASE = "https://vllm.ai/blog/"
ALLOWED_HOSTS = {"vllm.ai", "blog.vllm.ai"}

OUT.mkdir(parents=True, exist_ok=True)

UA = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
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


def fetch(url: str, retries: int = 3) -> str:
    validate_url(url)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", errors="replace")
        except Exception as e:  # noqa: BLE001
            if attempt == retries - 1:
                raise
            print(f"  retry {attempt + 1} for {url}: {e}", file=sys.stderr)
            time.sleep(3 * (attempt + 1))
    raise RuntimeError("unreachable")


class VllmConverter(MarkdownConverter):
    """markdownify tuned for the vLLM Next.js pages."""

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
        # inside <pre> we already handled it; inline code keeps backticks
        if el.find_parent("pre") is not None:
            return el.get_text()
        return f"`{el.get_text()}`"


def absolutize(tag, attr, soup, page_url):
    from urllib.parse import urljoin

    for el in soup.find_all(tag):
        val = el.get(attr)
        if not val:
            continue
        if val.startswith("//"):
            el[attr] = "https:" + val
        elif val.startswith("/"):
            el[attr] = "https://vllm.ai" + val
        elif not val.startswith(("http://", "https://", "#", "mailto:")):
            el[attr] = urljoin(page_url, val)


_LATEX_MAP = {
    "\u00d7": r"\times", "\u00f7": r"\div", "\u2212": "-", "\u2217": r"\ast",
    "\u22c5": r"\cdot", "\u2264": r"\le", "\u2265": r"\ge", "\u2260": r"\ne",
    "\u2248": r"\approx", "\u221e": r"\infty", "\u2211": r"\sum",
    "\u220f": r"\prod", "\u2211n": r"\sum",
}


def _recon_mjx(el) -> str:
    """Reconstruct one MathJax SVG subtree to approximate LaTeX text."""
    import unicodedata

    node = el.get("data-mml-node", "")
    kids = [
        c for c in el.children
        if getattr(c, "name", None) in ("g", "svg")
    ]
    if node in ("math", "mrow", "mstyle", "merror", "mpadded", "mphantom"):
        return "".join(_recon_mjx(k) for k in kids)
    if node == "msub" and len(kids) >= 2:
        return f"{_recon_mjx(kids[0])}_{{{_recon_mjx(kids[1])}}}"
    if node == "msup" and len(kids) >= 2:
        return f"{_recon_mjx(kids[0])}^{{{_recon_mjx(kids[1])}}}"
    if node == "msubsup" and len(kids) >= 3:
        return (f"{_recon_mjx(kids[0])}_{{{_recon_mjx(kids[1])}}}"
                f"^{{{_recon_mjx(kids[2])}}}")
    if node == "mfrac" and len(kids) >= 2:
        return f"\\frac{{{_recon_mjx(kids[0])}}}{{{_recon_mjx(kids[1])}}}"
    if node == "msqrt":
        return "\\sqrt{" + "".join(_recon_mjx(k) for k in kids) + "}"
    out = []
    for c in el.descendants:
        if getattr(c, "name", None) != "use":
            continue
        try:
            ch = chr(int(c["data-c"], 16))
        except (KeyError, ValueError):
            continue
        ch = unicodedata.normalize("NFKC", ch)
        out.append(_LATEX_MAP.get(ch, ch))
    return "".join(out)


def restore_math(article) -> int:
    """Replace MathJax SVG containers with $...$ reconstructed math.

    Returns the number of formulas restored.
    """
    from bs4 import NavigableString

    n = 0
    for cont in article.find_all("mjx-container"):
        root = cont.find("g", attrs={"data-mml-node": "math"})
        text = _recon_mjx(root) if root is not None else ""
        # keep macro names from swallowing the next letter: \timesC -> \times C
        text = re.sub(
            r"(\\(?:times|div|cdot|ast|le|ge|ne|approx|sum|prod))(?=[A-Za-z])",
            r"\1 ", text,
        )
        cont.replace_with(NavigableString(f"${text}$"))
        n += 1
    return n


def unescape_inline_math(body: str) -> str:
    """markdownify escapes _ * # etc. inside $...$; undo that within spans."""
    def fix(m: re.Match) -> str:
        inner = m.group(1)
        for esc, raw in (("\\_", "_"), ("\\*", "*"), ("\\#", "#"),
                         ("\\[", "["), ("\\]", "]"), ("\\(", "("),
                         ("\\)", ")")):
            inner = inner.replace(esc, raw)
        return f"${inner}$"

    return re.sub(r"\$([^$\n]+)\$", fix, body)


def restore_embeds(article) -> None:
    """markdownify drops iframe/video/audio; keep them as markdown links."""
    from urllib.parse import urljoin

    from bs4 import NavigableString

    for tag, label in (("iframe", "Interactive figure"),
                       ("video", "Video"),
                       ("audio", "Audio")):
        for el in article.find_all(tag):
            src = el.get("src") or ""
            if src.startswith("/"):
                src = "https://vllm.ai" + src
            elif src and not src.startswith(("http://", "https://")):
                src = urljoin(BASE, src)
            el.replace_with(NavigableString(f"\n\n[{label}]({src})\n\n"))


def parse_post(slug: str, html: str) -> dict | None:
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("article")
    if article is None:
        return None

    # drop site chrome that lives inside the article shell
    for sel in ("nav", "footer", "script", "style", "noscript", "button"):
        for el in article.find_all(sel):
            el.decompose()

    restore_math(article)
    restore_embeds(article)

    absolutize("img", "src", article, BASE + slug)
    absolutize("a", "href", article, BASE + slug)

    # title: first h1, else og:title
    h1 = article.find("h1")
    title = None
    if h1:
        title = h1.get_text(" ", strip=True)
        h1.extract()
    if not title:
        og = soup.find("meta", property="og:title")
        title = og["content"].strip() if og else slug

    conv = VllmConverter(heading_style="ATX", bullets="-")
    body = conv.convert_soup(article)

    # cleanup
    body = re.sub(r"\n{3,}", "\n\n", body)
    body = re.sub(r"[ \t]+\n", "\n", body)
    body = unescape_inline_math(body)
    # drop the glued "June 20, 20238 min read" byline (date lives in frontmatter)
    body = re.sub(
        r"^\s*[A-Z][a-z]+ \d{1,2}, \d{4}\s*\d* min read\n\n", "", body
    )
    body = body.strip() + "\n"

    # metadata: date from slug, description from meta tags
    mdate = re.match(r"(\d{4}-\d{2}-\d{2})-", slug)
    post_date = mdate.group(1) if mdate else ""
    desc = ""
    ogd = soup.find("meta", property="og:description")
    if ogd:
        desc = ogd.get("content", "").strip()

    return {
        "slug": slug,
        "title": title,
        "date": post_date,
        "description": desc,
        "url": BASE + slug,
        "body": body,
    }


def parse_existing(path: Path) -> dict:
    text = path.read_text()
    m = re.match(r"---\ntitle: \"(.*?)\"\ndate: (\S+)\nsource: (\S+)", text)
    body = text.split("---", 2)[2] if text.startswith("---") else text
    return {
        "slug": path.stem,
        "title": m.group(1) if m else path.stem,
        "date": m.group(2) if m else "",
        "url": m.group(3) if m else "",
        "description": "",
        "body": body,
    }


def main():
    slugs = [s.strip() for s in SLUGS_FILE.read_text().splitlines() if s.strip()]
    print(f"{len(slugs)} slugs")
    only = sys.argv[1:] if len(sys.argv) > 1 else None

    meta_path = ROOT / "vllm-articles" / "meta.json"
    index = []
    if meta_path.exists():
        index = json.loads(meta_path.read_text())

    for i, slug in enumerate(slugs, 1):
        outfile = OUT / f"{slug}.md"
        if only and slug not in only:
            continue
        if outfile.exists() and outfile.stat().st_size > 1000 and not only:
            continue
        try:
            html = fetch(BASE + slug)
            post = parse_post(slug, html)
            if post is None:
                print(f"  !! no <article> in {slug}")
                continue
            fm = (
                "---\n"
                f'title: "{post["title"].replace(chr(34), chr(39))}"\n'
                f"date: {post['date']}\n"
                f"source: {post['url']}\n"
                f"crawled: {date.today().isoformat()}\n"
                "---\n\n"
            )
            outfile.write_text(fm + post["body"])
            index.append({k: v for k, v in post.items() if k != "body"})
            print(f"[{i}/{len(slugs)}] {slug} ok ({len(post['body'])} chars)")
        except Exception as e:  # noqa: BLE001
            print(f"[{i}/{len(slugs)}] {slug} FAILED: {e}", file=sys.stderr)
        time.sleep(0.4)

    index.sort(key=lambda p: p["slug"])
    meta_path.write_text(json.dumps(index, ensure_ascii=False, indent=2))
    print(f"done, meta has {len(index)} posts")


if __name__ == "__main__":
    main()
