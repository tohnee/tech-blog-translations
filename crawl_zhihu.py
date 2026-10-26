#!/usr/bin/env python3
"""知乎 AI 文章批量抓取管线（直接调用 zhihu-toolkit 库，无子进程）。

流程：关键词搜索文章 → 去重入清单 → 逐篇抓取转 Markdown → 归档 zhihu-articles/posts/。
可断点续传：状态存 zhihu-articles/_state.json，已归档的文章自动跳过。
前置条件：`zhihu auth paste` 或 `zhihu auth import` 已写入凭据缓存。

用法（需用 /tmp/zhihu-venv/bin/python3.12 运行）：
  python3 crawl_zhihu.py --limit 200          # 发现+下载，本次最多 200 篇
  python3 crawl_zhihu.py --discover-only      # 只刷新发现清单不下载
  python3 crawl_zhihu.py --download-only      # 只下载清单里未归档的
"""
import argparse
import json
import random
import re
import sys
import time
from datetime import date
from pathlib import Path

sys.path.insert(0, "/tmp/zhihu-venv/lib/python3.12/site-packages")

from zhihu_cli.content.download_contents import ContentDownloader  # noqa: E402
from zhihu_cli.content.handlers.search import search_articles  # noqa: E402

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "zhihu-articles"
POSTS = OUT / "posts"
STATE = OUT / "_state.json"
TODAY = date.today().isoformat()
RNG = random.SystemRandom()

# AI 相关关键词组（中文语境 + 英文专名）
KEYWORDS = [
    "大模型", "人工智能", "LLM", "深度学习", "机器学习",
    "AI Agent", "智能体", "多模态", "强化学习", "RAG",
    "生成式AI", "AIGC", "DeepSeek", "GPT", "Claude",
    "Gemini", "开源模型", "推理模型", "AI 芯片", "模型微调",
    "提示词工程", "上下文工程", "MCP", "智能体编排", "具身智能",
]

# 知乎文章 URL 白名单：仅允许 zhuanlan.zhihu.com/p/<数字> 或 zhihu.com/p/<数字>
URL_RE = re.compile(r"^https://(?:zhuanlan\.)?zhihu\.com/p/(\d+)/?$")

DOWNLOAD = None  # 全局 ContentDownloader（main 里初始化）


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"discovered": {}, "downloaded": [], "failed": {}}


def save_state(st: dict) -> None:
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=1))


def parse_article_url(url: str) -> str | None:
    """校验并提取文章 id；非白名单 URL 一律拒绝。"""
    m = URL_RE.match(str(url).strip())
    return m.group(1) if m else None


def sleep_jitter(lo: float = 3.0, hi: float = 6.0) -> None:
    time.sleep(RNG.uniform(lo, hi))


def discover(st: dict, per_kw: int) -> int:
    """搜索全部关键词，返回新增条数。"""
    new = 0
    for kw in KEYWORDS:
        print(f"[discover] {kw}", flush=True)
        try:
            items = search_articles(kw, limit=20, max_items=per_kw) or []
        except Exception as e:  # noqa: BLE001
            print(f"  search error: {str(e)[:90]}", flush=True)
            items = []
        for it in items:
            if not isinstance(it, dict):
                continue
            url = it.get("url", "")
            aid = parse_article_url(url)
            if not aid or aid in st["discovered"]:
                continue
            author = it.get("author")
            st["discovered"][aid] = {
                "title": it.get("title", ""),
                "url": url,
                "author": author.get("name", "") if isinstance(author, dict) else (author or ""),
                "kw": kw,
            }
            new += 1
        save_state(st)
        sleep_jitter()
    return new


def normalize_and_save(url: str, meta: dict, markdown: str) -> str | None:
    """按项目规范写 zhihu-articles/posts/<id>.md，返回文章 id。"""
    aid = parse_article_url(url)
    if not aid:
        return None
    title = (meta.get("title") or "untitled").replace('"', "'")
    front = [
        "---",
        f'title: "{title}"',
        f"source: {url}",
        f"crawled: {TODAY}",
    ]
    for k in ("author", "created"):
        if meta.get(k):
            front.append(f"{k}: {meta[k]}")
    front.append("---")
    body = re.sub(r"\n{3,}", "\n\n", markdown).strip()
    dest = POSTS / f"{aid}.md"
    dest.write_text("\n".join(front) + "\n\n" + body + "\n", encoding="utf-8")
    return aid


def download(st: dict, limit: int) -> int:
    """逐篇抓取清单中未归档的文章，返回成功数。"""
    done = 0
    fails = 0
    pending = [aid for aid in st["discovered"]
               if aid not in st["downloaded"]
               and not (POSTS / f"{aid}.md").exists()
               and st["failed"].get(aid, 0) < 3]
    print(f"[download] pending: {len(pending)}, limit: {limit}", flush=True)
    for aid in pending[:limit]:
        url = st["discovered"][aid]["url"]
        if not parse_article_url(url):
            continue
        try:
            meta, markdown = DOWNLOAD.fetch_article(url)
            saved = normalize_and_save(url, meta, markdown)
            if not saved:
                raise RuntimeError("normalize failed")
            st["downloaded"].append(aid)
            done += 1
            fails = 0
            print(f"  [{done}] {aid} {(meta.get('title') or '')[:40]}", flush=True)
        except Exception as e:  # noqa: BLE001
            st["failed"][aid] = st["failed"].get(aid, 0) + 1
            fails += 1
            print(f"  FAIL {aid}: {str(e)[:90]}", flush=True)
            if fails >= 5:
                print("  连续 5 次失败，停止本轮（疑似风控/掉登录）", flush=True)
                break
            time.sleep(60 if fails >= 2 else 15)
        save_state(st)
        sleep_jitter(3.5, 6.5)
    return done


def main() -> None:
    global DOWNLOAD
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=200)
    ap.add_argument("--per-kw", type=int, default=60)
    ap.add_argument("--discover-only", action="store_true")
    ap.add_argument("--download-only", action="store_true")
    args = ap.parse_args()
    POSTS.mkdir(parents=True, exist_ok=True)
    if not args.discover_only:
        DOWNLOAD = ContentDownloader(output_dir=None, with_media=False)
        if not DOWNLOAD.load_headers_from_curl(quick_mode=True):
            print("[auth] 未找到缓存凭据，请先运行 zhihu auth paste / zhihu auth import", flush=True)
            sys.exit(2)
    st = load_state()
    if not args.download_only:
        n = discover(st, args.per_kw)
        print(f"[discover] new: {n}, total: {len(st['discovered'])}", flush=True)
    if not args.discover_only:
        n = download(st, args.limit)
        print(f"[download] done: {n}, total downloaded: {len(st['downloaded'])}", flush=True)
    save_state(st)


if __name__ == "__main__":
    sys.exit(main())
