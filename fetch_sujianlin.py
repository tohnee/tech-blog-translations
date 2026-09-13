#!/usr/bin/env python3
"""批量抓取科学空间文章原始 HTML 到 sujianlin-src/posts/ID.html，支持断点续传。"""
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

BASE = Path(__file__).resolve().parent
SRC = BASE / "sujianlin-src" / "posts"
SRC.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
local = threading.local()


def get_session() -> requests.Session:
    if not hasattr(local, "s"):
        s = requests.Session()
        s.headers.update({"User-Agent": UA})
        local.s = s
    return local.s


def fetch(url: str, tries: int = 8) -> str:
    """带 Cookie 挑战处理的 GET；被限流/封禁则长退避（SSL EOF 视为 IP 封禁）。"""
    s = get_session()
    last = None
    for k in range(tries):
        try:
            r = s.get(url, timeout=40)
        except requests.RequestException as e:
            # TLS 层被掐断 = IP 级封禁，长等待
            print(f"  [blocked?] {e.__class__.__name__}, sleeping 300s", flush=True)
            time.sleep(300)
            last = e
            continue
        if r.status_code == 200 and "window.location.href" not in r.text[:300]:
            return r.text
        last = RuntimeError(f"status={r.status_code}")
        # 触发限流：指数退避
        time.sleep(min(30 * 2**k, 600))
    raise last if last else RuntimeError("unknown")


def fetch_one(post: dict):
    out = SRC / f"{post['id']}.html"
    if out.exists() and out.stat().st_size > 5000:
        return "skip", None
    try:
        html = fetch(f"https://kexue.fm/archives/{post['id']}")
        out.write_text(html, encoding="utf-8")
        return "ok", None
    except Exception as e:
        return "fail", str(e)


def main():
    posts = json.loads((BASE / "sujianlin-src" / "posts_index.json").read_text(encoding="utf-8"))
    todo = [p for p in posts if not (SRC / f"{p['id']}.html").exists()]
    print(f"total {len(posts)}, to fetch {len(todo)}", flush=True)

    done = fails = 0
    failures = []
    t0 = time.time()
    for p in todo:  # 串行，避免触发限流
        status, err = fetch_one(p)
        done += 1
        if status == "fail":
            fails += 1
            failures.append((p["id"], err))
        elif status == "ok":
            time.sleep(3.0)  # 成功请求间保持礼貌间隔，避免再触发封禁
        if done % 25 == 0:
            rate = done / (time.time() - t0)
            print(f"{done}/{len(todo)} rate={rate:.2f}/s fails={fails}", flush=True)
    print(f"DONE fetched={done} fails={fails} elapsed={time.time()-t0:.0f}s", flush=True)
    if failures:
        (BASE / "sujianlin-src" / "fetch_failures.json").write_text(
            json.dumps(failures, ensure_ascii=False, indent=1), encoding="utf-8")
        print("failures written to sujianlin-src/fetch_failures.json", flush=True)


if __name__ == "__main__":
    main()
