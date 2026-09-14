#!/usr/bin/env python3
"""每日同步：检测 10 个来源的新文章（与已归档清单比对），输出 JSON 结果供后续归档/翻译。"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}


def validate_url(url: str) -> None:
    p = urllib.parse.urlparse(url)
    if p.scheme not in ("http", "https"):
        raise ValueError(f"scheme not allowed: {url}")
    host = (p.hostname or "").lower()
    if host in ("localhost", "127.0.0.1", "0.0.0.0", "::1") or host.startswith("192.168.") or host.startswith("10.") or host.startswith("172.16."):
        raise ValueError(f"host not allowed: {url}")


def fetch(url: str, retries: int = 3, delay: float = 2.0) -> str:
    validate_url(url)
    last = None
    for _ in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(delay)
    raise RuntimeError(f"fetch failed {url}: {last}")


def links(html: str, base: str, pattern: str):
    out = []
    for m in re.finditer(r'href="([^"]+)"', html):
        u = urllib.parse.urljoin(base, m.group(1))
        mo = re.match(pattern, u)
        if mo:
            slug = mo.group(1).rstrip("/")
            out.append((slug, u))
    return out


def dedup(seq):
    seen, out = set(), []
    for s, u in seq:
        if s not in seen:
            seen.add(s)
            out.append((s, u))
    return out


def meta_slugs(path: Path) -> set:
    if not path.exists():
        return set()
    return {p["slug"] for p in json.loads(path.read_text())}


def detect():
    result = {}
    # --- vLLM ---
    try:
        html = fetch("https://vllm.ai/blog/")
        have = meta_slugs(ROOT / "vllm-articles/meta.json")
        result["vllm"] = [(s, u) for s, u in dedup(links(html, "https://vllm.ai/blog/", r"https://blog\.vllm\.ai/([0-9a-zA-Z\-]+)/?$")) if s not in have]
    except Exception as e:  # noqa: BLE001
        result["vllm"] = f"ERROR: {e}"
    # --- SGLang / LMSYS ---
    try:
        html = fetch("https://lmsys.org/blog/")
        have = {p.stem.split("-", 3)[-1] for p in (ROOT / "sglang-articles").glob("*.md")}
        result["sglang"] = [(s, u) for s, u in dedup(links(html, "https://lmsys.org/blog/", r"https://lmsys\.org/blog/([0-9a-zA-Z\-]+)/?$")) if s not in have]
    except Exception as e:  # noqa: BLE001
        result["sglang"] = f"ERROR: {e}"
    # --- DeepMind ---
    try:
        html = fetch("https://deepmind.google/blog/")
        have = meta_slugs(ROOT / "deepmind-articles/meta.json")
        result["deepmind"] = [(s, u) for s, u in dedup(links(html, "https://deepmind.google/blog/", r"https://deepmind\.google/blog/([0-9a-zA-Z\-]+)/?$")) if s not in have]
    except Exception as e:  # noqa: BLE001
        result["deepmind"] = f"ERROR: {e}"
    # --- Gemini（两个栏目）---
    try:
        have = meta_slugs(ROOT / "gemini-articles/meta.json")
        raw = []
        for page in ("https://blog.google/products-and-platforms/products/gemini/", "https://blog.google/innovation-and-ai/models-and-research/gemini-models/"):
            raw += links(fetch(page), page, r"https://blog\.google/products/([0-9a-zA-Z\-/]+)/?$")
        # slug 取末段，且要求链接路径含 /products/
        result["gemini"] = [(s.split("/")[-1], u) for s, u in dedup(raw) if s.split("/")[-1] not in have]
    except Exception as e:  # noqa: BLE001
        result["gemini"] = f"ERROR: {e}"
    # --- Google Blog ---
    try:
        html = fetch("https://blog.google/innovation-and-ai/")
        have = meta_slugs(ROOT / "google-blog-articles/meta.json")
        result["google-blog"] = [(s.split("/")[-1], u) for s, u in dedup(links(html, "https://blog.google/", r"https://blog\.google/products/([0-9a-zA-Z\-/]+)/?$")) if s.split("/")[-1] not in have]
    except Exception as e:  # noqa: BLE001
        result["google-blog"] = f"ERROR: {e}"
    # --- Anthropic / Claude Code ---
    try:
        html = fetch("https://www.anthropic.com/news")
        have = {p.stem for p in (ROOT / "claudecode-articles").glob("*.md")}
        result["claudecode"] = [(s, u) for s, u in dedup(links(html, "https://www.anthropic.com/news", r"https://www\.anthropic\.com/news/([0-9a-zA-Z\-]+)/?$")) if s not in have]
    except Exception as e:  # noqa: BLE001
        result["claudecode"] = f"ERROR: {e}"
    # --- Lilian Weng（GitHub API）---
    try:
        html = fetch("https://api.github.com/repos/lilianweng/lilianweng.github.io/contents/_posts")
        files = {it["name"] for it in json.loads(html) if it["name"].endswith(".md")}
        have = {p.name for p in (ROOT / "lilianweng-articles/posts").glob("*.md")}
        result["lilianweng"] = sorted(f for f in files if f not in have)
    except Exception as e:  # noqa: BLE001
        result["lilianweng"] = f"ERROR: {e}"
    # --- Sebastian Raschka（sitemap + blog 页）---
    try:
        xml = fetch("https://sebastianraschka.com/sitemap.xml")
        urls = re.findall(r"<loc>([^<]+)</loc>", xml)
        have = {p.stem for p in (ROOT / "sebastianraschka-articles").rglob("*.md")}
        newp = [(m.group(2), u) for u in urls if (m := re.search(r"/(?:blog|articles)/(\d{4})/([a-zA-Z0-9_-]+)\.html$", u)) and m.group(2) not in have]
        result["raschka"] = dedup(newp)
    except Exception as e:  # noqa: BLE001
        result["raschka"] = f"ERROR: {e}"
    # --- OpenAI（Wayback CDX）---
    try:
        have = meta_slugs(ROOT / "openai-articles/meta.json")
        cdx = fetch("http://web.archive.org/cdx/search/cdx?url=openai.com/index/*&output=text&from=20260901&collapse=urlkey&fl=original&limit=500")
        slugs = [u.rstrip("/").split("/")[-1] for u in cdx.split() if u.startswith("http")]
        result["openai"] = [(s, f"https://openai.com/index/{s}/") for s in slugs if s and s not in have]
    except Exception as e:  # noqa: BLE001
        result["openai"] = f"ERROR: {e}"
    # --- 苏剑林 kexue.fm（单请求，严格限速）---
    try:
        time.sleep(3)
        html = fetch("https://kexue.fm/archives/", retries=1)
        have_idx = (ROOT / "sujianlin-articles/INDEX.md").read_text()
        items = re.findall(r'href="(https://kexue\.fm/archives/\d+\.html)"[^>]*>([^<]+)</a>', html)
        result["sujianlin"] = [(u, t.strip()) for u, t in items if u not in have_idx][:15]
    except Exception as e:  # noqa: BLE001
        result["sujianlin"] = f"ERROR: {e}"
    return result


if __name__ == "__main__":
    print(json.dumps(detect(), ensure_ascii=False, indent=1, default=str))
