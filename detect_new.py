#!/usr/bin/env python3
"""每日同步：检测 23 个来源的新文章（与已归档清单比对），输出 JSON 结果供后续归档/翻译。

源分三组：
  - 原有 12 源（detect()）：OpenAI/Google 系/vLLM/SGLang/Claude 系/Lilian Weng/Raschka/kexue.fm 等
  - 大模型厂商十源（detect_vendors()）：Qwen/DeepSeek/ThinkingMachines/MiniMax/智谱/小米/StepFun/Ling/xAI/Meta AI
  - SemiAnalysis（detect_vendors() 内）：Substack API
"""
import json
import re
import subprocess
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


def proxy_fetch(url: str, use_http1: bool = True) -> str:
    """走本机 SOCKS 代理抓取（archive.org / 直连被断的站点）。仅允许 http/https 外部主机。"""
    validate_url(url)
    cmd = ["curl", "-sSL", "--compressed", "--max-time", "90", "-A", UA["User-Agent"],
           "--socks5-hostname", "127.0.0.1:10808"]
    if use_http1:
        cmd.append("--http1.1")
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if r.returncode != 0 or len(r.stdout) < 200:
        raise RuntimeError(f"proxy fetch failed: {r.stderr[:100]}")
    return r.stdout


def _have(src_dir: str) -> set:
    """已收 slug 集：meta.json slug ∪ posts/ 文件名（去 .md）。"""
    root = ROOT / src_dir
    have = set()
    mp = root / "meta.json"
    if mp.exists():
        try:
            have |= {m["slug"] for m in json.loads(mp.read_text()) if isinstance(m, dict) and m.get("slug")}
        except Exception:  # noqa: BLE001
            pass
    pd = root / "posts"
    if pd.exists():
        have |= {p.stem for p in pd.glob("*.md")}
    return have


def detect_vendors():
    """大模型厂商十源 + SemiAnalysis。检测入口与 SOP 第 10 节一致。"""
    result = {}

    # Qwen：GitHub QwenLM/QwenLM.github.io（Hugo 源）git tree
    try:
        tree = json.loads(fetch("https://api.github.com/repos/QwenLM/QwenLM.github.io/git/trees/HEAD?recursive=1", retries=2))
        names = {t["path"].split("/")[-2] for t in tree.get("tree", [])
                 if re.match(r"content/posts/[^/]+/index(\.zh)?\.md$", t.get("path", ""))}
        result["qwen"] = sorted(names - _have("qwen-articles"))
    except Exception as e:  # noqa: BLE001
        result["qwen"] = f"ERROR: {e}"

    # DeepSeek：api-docs sitemap /news/
    try:
        xml = fetch("https://api-docs.deepseek.com/sitemap.xml", retries=2)
        slugs = {m.group(1) for m in re.finditer(r"<loc>https://api-docs\.deepseek\.com/news/([a-z0-9\-]+)/?</loc>", xml)}
        result["deepseek"] = sorted(slugs - _have("deepseek-articles"))
    except Exception as e:  # noqa: BLE001
        result["deepseek"] = f"ERROR: {e}"

    # Thinking Machines：sitemap
    try:
        xml = fetch("https://thinkingmachines.ai/sitemap.xml", retries=2)
        slugs = {u.rstrip("/").split("/")[-1] for u in re.findall(r"<loc>([^<]+)</loc>", xml) if "/blog/" in u}
        result["thinkingmachines"] = sorted(s for s in slugs - _have("thinkingmachines-articles") if s not in ("blog", "index"))
    except Exception as e:  # noqa: BLE001
        result["thinkingmachines"] = f"ERROR: {e}"

    # MiniMax：minimax.io/blog（SSR）
    try:
        html = fetch("https://minimax.io/blog", retries=2)
        slugs = {m.group(1) for m in re.finditer(r'href="(?:https://minimax\.io)?/blog/([a-z0-9\-]+)/?"', html)}
        result["minimax"] = sorted(slugs - _have("minimax-articles"))
    except Exception as e:  # noqa: BLE001
        result["minimax"] = f"ERROR: {e}"

    # 智谱：HF API 模型列表（slug 归一化：GLM-5.2 → hf-glm-5-2；建库口径=GLM-5+ 主力模型卡）
    try:
        models = json.loads(fetch("https://huggingface.co/api/models?author=zai-org&limit=200", retries=2))
        have = {h.lower() for h in _have("zhipu-articles")}
        names = {m["modelId"].split("/")[-1] for m in models}
        result["zhipu"] = sorted(n for n in names if re.match(r"(?i)^GLM-[5-9]", n)
                                 and not re.search(r"(?i)[-_](fp8|bf16|int8|int4|awq|gptq)$", n)
                                 and f"hf-{n.lower().replace('.', '-')}" not in have)
    except Exception as e:  # noqa: BLE001
        result["zhipu"] = f"ERROR: {e}"

    # 小米 / StepFun / Ling：GitHub org repos（只报近 7 日新建 repo；存量未收 repo 属建库口径，见 SOP 待定清单）
    AUX = re.compile(r"(?i)(awesome|\.github|benchmark|bench|gebench|eval|lmms|demo|training|skills|docs|site|web|homepage|blog|examples|tutorial|comfyui|discord|resources|cookbook|scripts?|utils?$|hub$|agents?$)")
    week_ago = time.strftime("%Y-%m-%d", time.gmtime(time.time() - 7 * 86400))
    for key, org, main_pat in (("xiaomi", "XiaomiMiMo", r"^MiMo"), ("stepfun", "stepfun-ai", r"^Step"), ("ling", "inclusionAI", None)):
        try:
            repos = json.loads(fetch(f"https://api.github.com/orgs/{org}/repos?per_page=100&sort=pushed", retries=2))
            have = _have(f"{key}-articles")
            cand = [r["name"] for r in repos if r["name"] not in have and not AUX.search(r["name"])
                    and r.get("created_at", "")[:10] >= week_ago
                    and (main_pat is None or re.match(main_pat, r["name"]))]
            result[key] = sorted(cand)
        except Exception as e:  # noqa: BLE001
            result[key] = f"ERROR: {e}"

    # xAI：x.ai/news 直连 403 → CDX（走代理；未收录 slug 即候选，老文重抓已全在库）
    try:
        cdx = proxy_fetch("https://web.archive.org/cdx/search/cdx?url=x.ai%2Fnews%2F*&output=text&fl=original&collapse=urlkey&filter=statuscode:200&filter=mimetype:text/html&limit=2000")
        slugs = {u.rstrip("/").split("/")[-1] for u in cdx.split() if u.startswith("http")}
        result["xai"] = sorted(s for s in slugs if re.fullmatch(r"[a-z0-9][a-z0-9\-]{4,}", s) and s not in _have("xai-articles") and s not in ("news", "success", "blog", "index"))
    except Exception as e:  # noqa: BLE001
        result["xai"] = f"ERROR: {e}"

    # Meta AI：ai.meta.com 直连断 → CDX 首抓时间法（首抓≥近 7 日且未收录才是新文；老 Facebook 博客文为存量口径待定）
    try:
        cdx = proxy_fetch("https://web.archive.org/cdx/search/cdx?url=ai.meta.com%2Fblog%2F*&output=text&fl=original,timestamp&collapse=urlkey&filter=statuscode:200&filter=mimetype:text/html&limit=2000")
        week_ts = time.strftime("%Y%m%d000000", time.gmtime(time.time() - 7 * 86400))
        have = _have("meta-ai-articles")
        seen, cand = set(), []
        for line in cdx.split("\n"):
            parts = line.strip().split(" ")
            if len(parts) != 2:
                continue
            url, ts = parts
            s = url.rstrip("/").split("/")[-1]
            if not re.fullmatch(r"[a-z0-9][a-z0-9\-]{4,}", s) or re.search(r"-\d{8,}$", s):
                continue
            if ts >= week_ts and s not in have and s not in seen:
                seen.add(s)
                cand.append(s)
        result["meta-ai"] = sorted(cand)
    except Exception as e:  # noqa: BLE001
        result["meta-ai"] = f"ERROR: {e}"

    # SemiAnalysis：Substack archive API（最近 24 篇足够日常增量）
    try:
        items = json.loads(fetch("https://newsletter.semianalysis.com/api/v1/archive?sort=new&offset=0&limit=24", retries=2))
        result["semianalysis"] = sorted({it["slug"] for it in items} - _have("semianalysis-articles"))
    except Exception as e:  # noqa: BLE001
        result["semianalysis"] = f"ERROR: {e}"

    return result


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
    # --- DeepMind（直连正常；2026-09 起文章迁移至 blog.google/google-deepmind/，两处都要查）---
    try:
        have = meta_slugs(ROOT / "deepmind-articles/meta.json")
        raw = []
        html = fetch("https://deepmind.google/blog/")
        raw += links(html, "https://deepmind.google/blog/", r"https://deepmind\.google/blog/([0-9a-zA-Z\-]+)/?$")
        # 迁移后的交叉链接（列表页指向 blog.google，URL 常带 ?utm 参数，不能锚定结尾引号）
        for m in re.finditer(r'href="(https://blog\.google/[a-z0-9\-/]+)', html):
            u = m.group(1)
            if "/google-deepmind/" in u:
                raw.append((u.rstrip("/").split("/")[-1], u))
        result["deepmind"] = [(s, u) for s, u in dedup(raw) if s not in have]
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
    # --- Claude 博客（claude.com 直连可抓）---
    try:
        xml = fetch("https://claude.com/sitemap.xml")
        urls = re.findall(r"<loc>([^<]+)</loc>", xml)
        have = {p.stem for p in (ROOT / "claude-blog-articles").rglob("*.md") if p.name != "README.md"}
        seen, out = set(), []
        for u in urls:
            m = re.search(r"/blog/([a-z0-9\-]+)/?$", u)
            if m and m.group(1) not in have and m.group(1) not in seen:
                seen.add(m.group(1))
                out.append((m.group(1), u))
        result["claude-blog"] = out  # 注意：含建库时按口径筛除的非技术文（产品/客户故事），需人工甄别
    except Exception as e:  # noqa: BLE001
        result["claude-blog"] = f"ERROR: {e}"
    # --- OpenAI 开发者博客（直连常被拒，SOP 走 Wayback+SOCKS；此处先直连尝试）---
    try:
        have = {p.stem for p in (ROOT / "openai-dev-articles/posts").glob("*.md")}
        newp = []
        for base in ("https://developers.openai.com/blog/index.xml",):
            try:
                xml = fetch(base)
                newp += [(m.group(1), m.group(0)) for m in re.finditer(r"https://developers\.openai\.com/blog/([a-z0-9\-]+)/?", xml) if m.group(1) not in have]
            except Exception:  # noqa: BLE001
                continue
        result["openai-dev"] = dedup(newp)
    except Exception as e:  # noqa: BLE001
        result["openai-dev"] = f"ERROR: {e}"
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
    only_legacy = "--legacy" in sys.argv
    only_vendors = "--vendors" in sys.argv
    if only_legacy:
        out = detect()
    elif only_vendors:
        out = detect_vendors()
    else:
        out = detect()
        out.update(detect_vendors())
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
