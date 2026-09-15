#!/usr/bin/env python3
"""SemiAnalysis Substack 全量抓取器。

数据源：newsletter.semianalysis.com 的 Substack 公开 API（固定域名白名单）。
- 列表接口 /api/v1/archive 分页枚举全部文章元数据；
- 单篇接口 /api/v1/posts/<slug> 取正文 body_html（免费文=全文，付费文=公开预览）。
产物：semianalysis-articles/src/<slug>.json（含元数据+正文），幂等可续传。
"""
import ipaddress
import json
import re
import socket
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC_DIR = (ROOT / "semianalysis-articles" / "src").resolve()
SRC_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_HOSTS = {"newsletter.semianalysis.com"}
LIST_URL = "https://newsletter.semianalysis.com/api/v1/archive?sort=new&offset={o}&limit=12"
POST_URL = "https://newsletter.semianalysis.com/api/v1/posts/{s}"


def assert_safe_url(url: str) -> None:
    """仅允许 https + 固定域名，且解析后 IP 不得为私网/环回/链路本地。"""
    parts = urllib.parse.urlsplit(url)
    if parts.scheme != "https" or parts.hostname not in ALLOWED_HOSTS:
        raise ValueError(f"blocked url: {url}")
    for af in (socket.AF_INET, socket.AF_INET6):
        try:
            info = socket.getaddrinfo(parts.hostname, None, af)
            break
        except socket.gaierror:
            info = None
    if info:
        # 198.18.0.0/15 是本机代理 fake-ip 模式对所有域名返回的合成地址，
        # 实际出口仍由 URL 主机白名单约束；其余私网/环回/链路本地一律阻断。
        fake_ip_range = ipaddress.ip_network("198.18.0.0/15")
        for family, _, _, _, sockaddr in info:
            ip = ipaddress.ip_address(sockaddr[0])
            if ip in fake_ip_range:
                continue
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
                raise ValueError(f"blocked resolved address {ip} for {url}")


def fetch_json(url: str, retries: int = 4) -> dict:
    for i in range(retries):
        try:
            assert_safe_url(url)
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=40) as resp:
                if resp.geturl():
                    assert_safe_url(resp.geturl())  # 限制重定向落点
                return json.load(resp)
        except Exception as e:  # noqa: BLE001
            wait = 5 * (i + 1)
            print(f"  retry {i+1}/{retries} after {wait}s: {e}", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"failed: {url}")


def safe_path_for(slug: str) -> Path:
    """slug 白名单化后仍校验落点必须位于 SRC_DIR 内，杜绝路径穿越。"""
    name = re.sub(r"[^A-Za-z0-9_-]", "_", slug)[:150] or "untitled"
    p = (SRC_DIR / f"{name}.json").resolve()
    if not p.is_relative_to(SRC_DIR):
        raise ValueError(f"path escapes archive dir: {slug}")
    return p


def main() -> None:
    index_path = SRC_DIR / "_index.json"
    if index_path.exists():
        posts = json.load(open(index_path))
        print(f"index cached: {len(posts)} posts")
    else:
        posts, offset, seen = [], 0, set()
        while True:
            batch = fetch_json(LIST_URL.format(o=offset))
            if not batch:
                break
            for p in batch:
                if p["id"] not in seen:
                    seen.add(p["id"])
                    posts.append(p)
            offset += len(batch)
            time.sleep(0.3)
        index_path.write_text(json.dumps(posts, ensure_ascii=False))
        print(f"indexed {len(posts)} posts")

    todo = [p for p in posts if not safe_path_for(p["slug"]).exists()]
    print(f"to fetch: {len(todo)}")
    for i, p in enumerate(todo, 1):
        try:
            path = safe_path_for(p["slug"])
            full = fetch_json(POST_URL.format(s=urllib.parse.quote(p["slug"])))
        except (RuntimeError, ValueError) as e:
            print(f"[{i}/{len(todo)}] FAILED {p['slug']}: {e}", file=sys.stderr)
            continue
        body = full.get("body_html") or p.get("body_html") or ""
        full["_list_meta"] = {"post_date": p.get("post_date"), "audience": p.get("audience")}
        path.write_text(json.dumps(full, ensure_ascii=False))
        print(f"[{i}/{len(todo)}] {p['post_date'][:10]} {path.stem} aud={p.get('audience')} body={len(body)}")
        time.sleep(0.35)
    print("done")


if __name__ == "__main__":
    main()
